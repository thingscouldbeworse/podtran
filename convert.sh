#!/bin/bash
for PATHNAME in episodes/*.mp3
do
  ffmpeg -y -i "$PATHNAME" thumb.jpeg
  FILENAME="${PATHNAME##*/}"
  ffmpeg -n -loop 1 -i thumb.jpeg -i "$PATHNAME" -c:a copy -c:v libx264 -shortest "episodes_convert/${FILENAME%.mp3}.mp4"
done

