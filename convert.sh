#!/bin/bash
THUMBNAIL=$1
for PATHNAME in episodes/*.mp3
do
  FILENAME="${PATHNAME##*/}"
  ffmpeg -loop 1 -i "$THUMBNAIL" -i "$PATHNAME" -c:a copy -c:v libx264 -shortest "episodes_convert/${FILENAME%.mp3}.mp4"
done

