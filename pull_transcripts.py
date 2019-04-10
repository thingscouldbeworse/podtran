import os
import json
import sys
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def auth_with_api(client_secrets_file):
  # Disable OAuthlib's HTTPS verification when running locally.
  # *DO NOT* leave this option enabled in production.
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

  api_service_name = "youtube"
  api_version = "v3"

  # Get credentials and create an API client
  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
      client_secrets_file, scopes)
  credentials = flow.run_console()
  youtube = googleapiclient.discovery.build(
      api_service_name, api_version, credentials=credentials)
  
  return youtube


def get_all_vids(youtube):
  request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    mine=True
  )
  response = request.execute()
  uploads = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

  request = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId=uploads
  )
  response = request.execute()

  uploads = []
  for video in response["items"]:
    print(video["contentDetails"]["videoId"])
    if video["snippet"]["description"] == "podtran":
      uploads.append(video["contentDetails"]["videoId"])

  print(uploads)
  for upload in uploads:
    get_one_transcript(upload, youtube)


def get_one_transcript(video_id, youtube):

  request = youtube.captions().list(
    part="id",
    videoId=video_id
  )
  response = request.execute()

  request = youtube.captions().download(
      id=response["items"][0]["id"]
  )
  response = request.execute()
  print(response)
  


def main():
  youtube = auth_with_api(sys.argv[1])
  get_all_vids(youtube)
  #get_one_transcript('N7tDz_bCqSw', youtube)

if __name__ == "__main__":
    main()

