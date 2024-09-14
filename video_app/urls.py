from django.urls import path
from .views import VideoListView, VideoDetailView, videoCreateView

urlpatterns = [
    path('', VideoListView.as_view(), name='video_list'),  
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('upload/', videoCreateView.as_view(), name='video_upload'),
]