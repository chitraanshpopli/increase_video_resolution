import os
import sys
import re
import requests
import bs4
import subprocess

ext_list = ('.mp4', '.mkv', '.avi', '.flv', '.mov', '.wmv', '.vob',
'.mpg','.3gp', '.m4v')		#List of extensions to be checked.

file_name = 'song_URL_list.csv'		#Name and extension of file for video URLs. 

min_pixels = 720*576 	#Videos with pixels (in a frame) count >= this will be excluded.
search_base = 'https://www.youtube.com/results?search_query='
video_base = 'https://www.youtube.com' 

def get_path(path_flag):
	#Sets the path for directory of video files.
	if path_flag == 'y':
		pass
	else:
		try:
			os.chdir(path_flag)
		except (FileNotFoundError,OSError):
			print('Invalid path. Quitting' )
			sys.exit()

def get_file_list():
	#Returns list of useful files.
	file_list = remove_nonvideo_files(os.listdir(os.getcwd()))
	return file_list
	
def remove_nonvideo_files(file_list):
	#Removes files whose extension is not mentioned in ext_list from list of files.
	for index,file_name in enumerate(file_list[:]):
		if file_name.endswith(ext_list):
			pass
		else:
			#print('Removed: ' + file_name + ' at index: ' + str(index))
			file_list.remove(file_name)
	return file_list

def remove_high_res(file_list):
	#Removes files with high resolution.
	for index,file_name in enumerate(file_list[:]):
		if pixel_count(index,file_list[:]):
			print('Excluding:\n' + file_name)
			file_list.remove(file_name)
		
	
def pixel_count(index, file_list):
	#Returns True if pixel count is >= min_pixels 
	#hachoir-metadata can read meta-data from video files  
	console_string = 'hachoir-metadata ' + '"'+file_list[index]+'"' 
	metadata = subprocess.run(console_string, shell=True,stdout=subprocess.PIPE)
	metadata_txt = metadata.stdout.decode('utf-8')

	width = re.search('width: ([0-9]*)', metadata_txt).group()
	width = int(re.search('([0-9]+)',width).group())
	height = re.search('height: ([0-9]*)', metadata_txt).group()
	height = int(re.search('([0-9]+)',height).group())	
	
	if (width*height) >= min_pixels:
		return True
	else:
		return False
	
def remove_extensions(file_list):
	#Removes extension (.abc) from file names from list of files.
	#This assumes extension is 3 character long (excluding the dot). 
	for index,file_name in enumerate(file_list):
		file_list[index] = file_name[:-4]
	return file_list

def get_video_URLs(search_URLs, file_flag,file_list):
	#Searches names in file list and stores the URL of first video in CSV file.
	#Also returns a list with all URLs.
	video_URLs = []
	for index in range(len(search_URLs)):
		page = (requests.get(search_URLs[index])).text
		soup = bs4.BeautifulSoup(page,'html.parser')
		for link in soup.find_all('a', href = True):
			link_string = str(link['href'])
			if link_string.startswith('/watch?v='):
				video_URL = video_base + link_string
				video_URLs.append(video_URL)
				if file_flag == True:
					with open(file_name, 'a') as URLs:
						URLs.write('\nName -- ' + file_list[index] + 
						'\nURL -- ' + video_URL + '\n')
						print('\nAdded:\nName -- ' + file_list[index] + 
						'\nURL -- ' + video_URL + '\n')
				break
	return video_URLs
	
def main():
	#Executes the program.
	print("""
	song_URL_list.csv file will be saved in the folder having the videos.
	If you have a file of this name in this folder, move it somewhere else.
	""")  
	print("""
	WARNING: This uses hachoir-metadata to extract resolution of video.
	While it should work for most video formats, it has not been tested.
	If something doesn't work, try disabling this. It will grab links for
	all videos.
	""") 
	
	hachoir_flag = True		#Set False if hachoir not to be used. 
	file_flag = True		#Set False if CSV file not needed. 
	res_flag = True        #Set False if no videos are to be excluded.
	
	path_flag = input(r"""
	If the program is running in the folder having the videos, press 'y' and enter.
	If you want to give a path then enter the path.
	""").lower()
	
	get_path(path_flag)

	file_list = get_file_list()

	if res_flag == True:
		remove_high_res(file_list)

	file_list = remove_extensions(file_list)

	search_URLs = [search_base+query for query in file_list]
	
	#Stores all URLs in a list. 
	video_URLs = get_video_URLs(search_URLs, file_flag,file_list)
	#print(video_URLs)
	qv = input('Done. Press enter to exit.') 

main()


