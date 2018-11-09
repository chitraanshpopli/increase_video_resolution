# increase_video_resolution

I had downloaded videos from the time when internet wasn't very fast here. So videos were downloaded in a lower resolution. 
This finds youtube URLs of all the videos kept in a folder and stored them in a CSV file.
These links can then be put in a youtube downloader for batch download. 
I imported the CSV into 4K Youtube downloader to get all videos in high resolution in one go.

## Packages used:
os, sys, re, requests, bs4 and subprocess

## Working:
1. Takes path of folder containing the videos. Default path is the folder in which program is stored.
2. Creates a list of all video files in the folder.
3. Removes any files with resolution 720p or above.
4. Searches for remaining files on youtube and grabs the link of the first result.
5. Stores the link (along with the name) in song_URL_list.csv file in the folder containing the videos.

## Other info:
1. Minimum resolution, csv file name and video extensions can be changed from the variables in the beginning of the code.
2. It should work but hasn't been tested with all the video container formats.
3. res_flag can be set to False to grab links of all videos irrespective of resolution.
4. Try setting res_flag to False if it doesn't work with some video format.
5. Set file_flag to False if you don't need CSV file.
6. All URLs are also stored in video_URLs variable, if required.
