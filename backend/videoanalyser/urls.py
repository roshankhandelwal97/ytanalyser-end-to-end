from django.urls import path
from .views import get_csrf_token, process_video, query_video

urlpatterns = [
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('process_video/', process_video, name='process_video'),
    path('query_video/', query_video, name='query_video'),
]
