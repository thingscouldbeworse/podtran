# Podcast Transcribing
This repository contains a tool used to:
  - Download podcast episodes from Soundcloud or an RSS feed
  - Convert all episodes to .mp4
  - upload all episodes to Youtube
  - Wait for Youtube to transcribe it for us, adding auto captions
  - Download the auto-generated captions

# Requirements
## Youtube API
Follow the guide for credentials here: https://developers.google.com/youtube/v3/quickstart/python

save your secrets.json file in the podtran directory

## Python
Python3 and pip is required. The Python dependencies can be installed with `pip install -r requirements.txt`

## Soundscrape
If you want to transcribe a podcast hosted on Soundcloud, the scraping tool Soundscrape is required. It can be installed from your distro's package manager. Ex, on Ubunut, `sudo apt-get install soundscrape`.

RSS FEED SCRAPING SUPPORT COMING SOON

## Thumbnail JPEG
You need an image to use as a flat thumbnail for the videos. Create or download some `.jpeg` and save it as `thumb.jpeg`.

# Running
Everything can be invoked in order by running the `download_convert_upload` script, eg `./download_convert_upload.sh`. All episodes will be downloaded, converted to mp4, and then uploaded. I recommend running this on another machine, such as a Raspberry Pi, inside a tmux session so you can check in with it as needed. 

Each step can be invoked on its own with the corresponding Python script. The required arguments will be printed upon invoking the script with empty arguments.

5 videos will be uploaded each day (the limit of the YouTube API). You can create a new project through the same steps outlined in the quickstart tutorial, and use multiple projects and multiple credentials to upload more than 5 videos each day, by splitting the number of episodes between each parallel project.
