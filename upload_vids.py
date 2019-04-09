import os
import sys
import argparse
import json
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
      print(error_json["error"]["errors"][0]["reason"])
      sys.exit(1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--secrets', required=True, help='JSON secrets file')
  args = parser.parse_args()

  metadata_total = build_metadata()

  upload_all(metadata_total, args)
  

