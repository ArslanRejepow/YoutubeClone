from django.urls import path
from .views import index, video, download_video

urlpatterns = [
	path('search/', index, name='search'),
	path('video/<str:video_id>', video, name='video'),
	path('download/<str:video>', download_video, name='download'),
]