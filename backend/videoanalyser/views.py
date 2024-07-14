from django.http import JsonResponse
from .forms import VideoQueryForm
from .rag import download_and_transcribe_video, answer_question
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse

# Global to store the pinecone context
pinecone_context = None

def get_csrf_token(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'csrfToken': csrf_token})

@csrf_exempt
def process_video(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        youtube_url = data.get('youtube_url')
        print(youtube_url)
        global pinecone_context
        pinecone_context = download_and_transcribe_video(youtube_url)
        return JsonResponse({"message": "Video processed successfully"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
@csrf_exempt 
def query_video(request):
    global pinecone_context
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')
        if pinecone_context and question:
            response = answer_question(pinecone_context, question)
            return JsonResponse({"answer": response}, status=200)
        else:
            return JsonResponse({"error": "Invalid request or context not set"}, status=400)

# Update urls.py accordingly to bind these views
