#!/bin/bash
EPISODES_DIR='episodes/'
EPISODES_OUT='episodes_convert/'
POD_NAME=$1 
SECRETS=$2

cd $EPISODES_DIR && soundscrape $POD_NAME

./convert.sh

python3 upload_vids.py "$2"