import os
import sys
import argparse
import json
import time
import datetime
from pathlib import Path
from googleapiclient.errors import HttpError

import upload_util

VIDEOS_DIR = 'episodes_convert/'

def build_metadata():
  videos = os.listdir(VIDEOS_DIR)
  metadata_list = []

  for vid in videos:
    title = vid[:-4]
    if '.mp4' not in vid:
      continue
    if title + ".lock" in videos:
      print("Skipping %s"%title)
      continue
    metadata = {
      'title': title,
      'file': VIDEOS_DIR + vid,
      'category': 22,
      'privacyStatus': 'private',
      'description': 'podtran',
      'keywords': 'transcription'
    }
    metadata_list.append(metadata)
  return metadata_list


def upload_all_with_pauses(metadata_list, args):
  upload_limit = 5
  upload_all(metadata_list[:upload_limit], args)
  date_begin = datetime.date.today()
  print("Sleeping until trying uploads again")
  done = False
  while not done:
    if (datetime.date.today() > date_begin):
      metadata_list = build_metadata()
      upload_all(metadata_list[:upload_limit], args)
    else:
      for i in range(8,0,-1): # 8*30mins = 4 hours
        print("retrying in " + str(i/2) + " hours", flush=True)
        time.sleep(60*30) # 30 minutes


def upload_all(metadata_list, args):
  youtube = upload_util.get_authenticated_service(args.secrets)
  for metadata in metadata_list:
    for key in metadata:
      setattr(args, key, metadata[key])
    try:
      upload_util.initialize_upload(youtube, args)
      Path(VIDEOS_DIR + metadata["title"] + ".lock").touch()
    except HttpError as e:
      try:
        error_json = json.loads(e.content.decode('utf8'))
      except:
        print(('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)))
        sys.exit(1)
      error_message = error_json["error"]["errors"][0]["reason"]
      print(error_message)
      return error_message


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--secrets', required=True, help='JSON secrets file')
  args = parser.parse_args()


  metadata_total = build_metadata()
  upload_all_with_pauses(metadata_total, args)
