import os
import argparse
from googleapiclient.errors import HttpError

import upload_util

VIDEOS_DIR = 'episodes_convert/'

def build_metadata():
  videos = os.listdir(VIDEOS_DIR)
  metadata_list = []

  for vid in videos:
    if '.mp4' not in vid:
      continue
    metadata = {
      'title': vid[:-4],
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
    except HttpError as e:
      print(('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--secrets', required=True, help='JSON secrets file')
  args = parser.parse_args()

  metadata_total = build_metadata()

  upload_all(metadata_total, args)
  

