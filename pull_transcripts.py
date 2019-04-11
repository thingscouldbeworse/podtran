import os
import json
import sys
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

TRANSCRIPTS_DIR = 'transcripts/'

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

  existing_transcripts = os.listdir(TRANSCRIPTS_DIR)

  uploads = []
  for video in response["items"]:
    for existing in existing_transcripts:
      if video["snippet"]["title"] in existing:
        print("transcript exists for %s, skipping"%video["snippet"]["title"])
        continue
    if video["snippet"]["description"] == "podtran":
      uploads.append([
        video["contentDetails"]["videoId"],
        video["snippet"]["title"]
      ])

  for upload in uploads:
    transcript = get_one_transcript(upload[0], youtube)
    with open(TRANSCRIPTS_DIR + upload[1] + ".txt", 'w') as file_out:
      file_out.write(transcript)


def get_one_transcript(video_id, youtube):

  request = youtube.captions().list(
    part="id",
    videoId=video_id
  )
  response = request.execute()

  if (len(response["items"]) < 1):
    response = "No transcript avaliable"
  else:
    request = youtube.captions().download(
        id=response["items"][0]["id"]
    )
    response = request.execute().decode("utf8")
  return response
  

def main():
  youtube = auth_with_api(sys.argv[1])
  get_all_vids(youtube)


if __name__ == "__main__":
    main()

