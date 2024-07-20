import os
from dotenv import load_dotenv
import yt_dlp as youtube_dl
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
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/audio',  # Name the output file as 'audio.mp3'
        'quiet': False,
        'noplaylist': True,
        'verbose': True
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=True)
            audio_file_path = 'downloads/audio.mp3'  # Directly reference the expected output file
            whisper_model = whisper.load_model("base")
            transcription = whisper_model.transcribe(audio_file_path)["text"].strip()

        with open("transcription.txt", "w") as file:
            file.write(transcription)

        loader = TextLoader("transcription.txt")
        text_documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        documents = text_splitter.split_documents(text_documents)
        embeddings = OpenAIEmbeddings()
        pinecone = PineconeVectorStore.from_documents(documents, embeddings, index_name="youtube-index")
        return pinecone
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def setup_chain_for_query(pinecone):
    if not pinecone:
        raise ValueError("Pinecone vector store must be initialized.")
    prompt_template = """
    Answer the question based on the context below.
    If you can't answer, reply 'Can't find the answer in the video.'
    Always summarize the {context} and answer the question as well.
    Context: {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    parser = StrOutputParser()
    setup = RunnableParallel(context=pinecone.as_retriever(), question=RunnablePassthrough())
    return setup | prompt | model | parser

def answer_question(pinecone, question):
    if not pinecone:
        return "Error: Pinecone context is not initialized."
    chain = setup_chain_for_query(pinecone)
    return chain.invoke(question)

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=example"
    pinecone_context = download_and_transcribe_video(youtube_url)
    if pinecone_context:
        question = "What is discussed in the video?"
        print(answer_question(pinecone_context, question))
    else:
        print("Failed to process video.")
