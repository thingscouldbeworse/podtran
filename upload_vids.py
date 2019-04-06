import os
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_vids(video_body, video):

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = sys.argv[1]

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet, status",
        body=video_body,

        media_body=MediaFileUpload(video)
    )
    response = request.execute()

    print(response)


def main():
    
    title = sys.argv[2]
    body=dict(
      snippet=dict(
        title=title,
        description="",
        tags="transcription"
      ),
        status=dict(
        privacyStatus="private"
      )
    )

    upload_vids(body, title)

if __name__ == "__main__":
    main()

