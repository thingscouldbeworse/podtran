from youtube_transcript_api import YouTubeTranscriptApi
import json

with open('vlogs.json', 'r') as vlogs:
    videos = json.load(vlogs)
    for video in videos:
        print("reading transcript for " + video['title'])
        transcripts = YouTubeTranscriptApi.get_transcript(video['vid_id'])
        print('writing transcript')
        try:
            with open ('transcripts/' + video['title'], 'w') as transcript_f:
                transcript_f.write(str(transcripts))
        except Exception as e:
            print("failed to write " + str(video['title']))
            print(e)

