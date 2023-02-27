from django.shortcuts import render
from youtubesearchpython import VideosSearch
import requests
from django.templatetags.static import static
from pytube import YouTube
import os
from django.http import HttpResponse
import mimetypes


def index(request):
	context = {'results' : 'hi'}
	if request.method == 'GET':
		if 'query' in request.GET:
		    search_query = request.GET['query']
		    results = VideosSearch(search_query).result()
		    thumbnails = results['result']
		    for items in thumbnails:
		        img_data = requests.get(items['thumbnails'][0]['url']).content
		        with open('search/static/'+items['id']+'.jpg', 'wb') as handler:
		            handler.write(img_data)
		        img_data2 = requests.get(items['channel']['thumbnails'][0]['url']).content
		        with open('search/static/'+items['channel']['id']+'.jpg', 'wb') as handler:
		            handler.write(img_data2)
		  
		    print(results)
		    context = {'results' : results}
	return render(request, 'home.html', context=context)
    
def video(request, video_id):
    link = "https://youtube.com/watch?v="+video_id
    print(link)
    path = YouTube(link).streams.get_audio_only().download(output_path = 'search/static/video')
    path = path.split('/')[-1:][0]
    context = {'data' : path}
    return render(request, 'video.html', context=context)

def download(request, video):
    file = video
    url = static('video/'+file)
    url = url.replace('%20', ' ')
    url = url[1:]
    
    with open(url, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="video/mp4")
        response['Content-Disposition'] = 'attachment; filename=h.mp4'
        return response
            
    return request.response

def download_video(request,video):
    file = video
    url = static('video/'+file)
    url = url.replace('%20', ' ')
    url = url[1:]
    filename = url.split('/')[-1:]

    fl = open(url, 'rb')
    mime_type, _ = mimetypes.guess_type(url)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response