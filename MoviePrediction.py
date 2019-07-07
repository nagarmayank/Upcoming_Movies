from urllib2 import Request, urlopen
import json
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

apikey = ""

def TMDbUpcomingMovie(apikey):
    headers = {"Accept": "application/json"}
    web_addr = "http://api.themoviedb.org/3/movie/upcoming?api_key=%s&language=en" % apikey
    request = Request(web_addr , headers=headers)
    response_body = urlopen(request).read()
    return response_body

def youtube_stats(video_id):
    headers = {"Accept": "application/json"}
    web_addr = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&key=%s" % (video_id , DEVELOPER_KEY)
    request = Request(web_addr , headers=headers)
    response_body = urlopen(request).read()
    return response_body
    
def youtube_search(movie_name):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=movie_name,
    part="id",
    order="relevance",
    maxResults=5,
    type="video"
  ).execute()
  
  f = search_response['items']
  
  for i in range(0,5):
      t = f[i]
      video_id = t['id']['videoId']
      stat_json = youtube_stats(video_id)
      stat_json_dict = json.loads(stat_json)
      print movie_name , '------>' , video_id , '------>' , stat_json_dict["items"][0]["statistics"]["viewCount"] , '------>' , stat_json_dict["items"][0]["statistics"]["likeCount"] , '------>' , stat_json_dict["items"][0]["statistics"]["dislikeCount"]

upcoming_movie = TMDbUpcomingMovie(apikey)
upcoming_movie_dict = json.loads(upcoming_movie)

for i in range(0,20):
    movie_name = upcoming_movie_dict["results"][i]["original_title"]
    youtube_search(movie_name)
