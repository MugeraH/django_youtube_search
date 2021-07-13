from django.shortcuts import render,redirect
import requests
from isodate import parse_duration

from django.conf import settings



def Home(request):
    videos = []
    if request.method == 'POST':
    
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        
        search_params = {
            'part':'snippet',
            'q':request.POST['search'],
            'key': settings.YOUTUBE_API_KEY,
            'maxResults':9,
            'type':'video'
        }
    
        video_ids = []
        rr = requests.get(search_url,params=search_params)
        # print(rr.json()['items'][0]['id']['videoId'])
        results = rr.json()['items']
        for result in results:
            video_ids.append(result['id']['videoId'])
            
            # function to redirect directly
        # if request.POST['submit'] == 'lucky':
        #     return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
            
        video_params = {
            'part':'snippet,contentDetails',
            'id':','.join(video_ids),
            'key': settings.YOUTUBE_API_KEY,
            'maxResults':9,
        
        }
            
        rr= requests.get(video_url,params=video_params)
        results=rr.json()['items']
        
        
        for result in results:
            video_data ={
                'id':result['id'],
                'title':result['snippet']['title'],
                'url':f'https://www.youtube.com/watch?v={result["id"]}',
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail':result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
            
        
    ctx={
            'videos':videos
        }    
        
       
    return render(request,"home.html",ctx)
