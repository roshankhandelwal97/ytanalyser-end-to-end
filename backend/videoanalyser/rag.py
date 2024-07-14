import os
import tempfile
from dotenv import load_dotenv
from pytube import YouTube
import whisper
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def download_and_transcribe_video(youtube_url):
    youtube = YouTube(youtube_url)
    audio = youtube.streams.filter(only_audio=True).first()
    whisper_model = whisper.load_model("base")
    print("Executing download_and_transcribe_video.... ")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file_path = audio.download(output_path=tmpdir)
        print("Converting Youtube video to Transcript.... ")
        transcription = whisper_model.transcribe(audio_file_path, fp16=False)["text"].strip()
    with open("transcription.txt", "w") as file:
        file.write(transcription)

    # Load the transcription into Pinecone Vector Store
    loader = TextLoader("transcription.txt")
    print("transcription.txt created.... ")
    text_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = text_splitter.split_documents(text_documents)
    embeddings = OpenAIEmbeddings()
    pinecone = PineconeVectorStore.from_documents(
        documents, embeddings, index_name="youtube-index"
    )
    return pinecone

def setup_chain_for_query(pinecone):
    prompt_template = """
    Answer the question based on the context below.
    If you can't answer, reply "Can't find the answer in the video"
    Always sumarrize the {context} and answer the question as well
    Context: {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    parser = StrOutputParser()
    setup = RunnableParallel(
        context=pinecone.as_retriever(), question=RunnablePassthrough()
    )
    chain = setup | prompt | model | parser
    return chain

def answer_question(pinecone, question):
    chain = setup_chain_for_query(pinecone)
    print(chain.invoke(question))
    return chain.invoke(question)

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=5t1vTLU7s40"
    print(download_and_transcribe_video(youtube_url))  # Just to test the download and transcription
