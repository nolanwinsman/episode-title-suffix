#plans for version 4
	#1: add verification to subfolders that checks if they are seasons example 'Season 1' or 's1' 
	#2: show the user information based on the IMDB search to verify it is the correct show. Information like cast, year, cover art
	#3: make sure the extention is a valid video file extention based on what VLC is compatable with

import os
from os.path import basename
import string
import imdb #run 'pip install IMDbPY' if you do not have the api
from collections import Counter

ia = imdb.IMDb() #calls the IMDb function to get an access object through which IMDB data can be retrieved

#adds a leading zero to season and episode numbers less than 10 and returns the file name in Plex standard
def fileName(showName, s, e, ext):
    file =f'{series} S{str(s).zfill(2)}E{str(e).zfill(2)}{ext}' # concatenate the file together in Plex format
    return file
    
#function that combines the directory name with the subfolder name so the subfolder is the new directory
def addToPath(currentDirectory, subFolder):
	return "{currentDirectory}/{subFolder}".format(currentDirectory=currentDirectory, subFolder=subFolder)
	
   #Takes a file and adds the episode name as a suffix to the file
   #credit to user "Łukasz Rogalski" on stack overflow for the majority of this function
def combineName(showName, epName): #showName is the file, epName is the name of the episode
    name, ext = os.path.splitext(showName)
    return "{name} {suffix}{ext}".format(name=name, suffix = epName, ext=ext)

    #uses the IMDB api to find and store information on the show
def seriesInfo(showName):
    series = ia.search_movie(showName) #searches for the series
    id = series[0].getID() #stores the ID of the first result of the search
    series = ia.get_movie(id) #gets the series
    numberOfSeasons = series['number of seasons'] #stores the number of seasons the series has
    return series,numberOfSeasons
		
#finds the extention of the episode files based on the most frequent extentions in the season folder
def findExtention(directory):
	extentions = [] #list that will store all file extentions
	for roots, dirs, files in os.walk(directory): #nested for loop that goes through every file in the directory
		for file in files:
			name, ext = os.path.splitext(file) #gets the extention of the file
			extentions.append(ext) #adds the extention to the extentions list
	return most_frequent(extentions)

#function that finds the most frequent element in a list
def most_frequent(List): #https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/ --credit
    occurence_count = Counter(List) 
    return occurence_count.most_common(1)[0][0] 

#function that asks the user if they want to rename all the files in the previewed format
def verify_with_user():
	print('')
	answer = input('Do you want to rename your files like the above file names? y for yes n for no: ')
	if answer == 'n' or answer == 'no' or answer == 'No' or answer == 'NO':
		exit()
	elif answer == 'y' or answer == 'yes' or answer == 'Yes' or answer == 'YES':
		return
	else: #if the user inputs something other than yes or no it calls the function again
		verify_with_user()
		
#similar to the ranameFiles() function but this just prints the results so it can show the user how the files will look once renameFiles() is called
def testRun(series, sNum, originalDir):
	for s in range(1,sNum+1): #for loop that goes through each season
		newDir = addToPath(originalDir, subdirs[s-1]) #sets the directory to a subfolder of the original show directory
		extention = findExtention(newDir) #finds the extention for the files
		epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
		print(f'-----Season {s}-----') #prints the season number
		for e in range(1,epCount+1): #for loop that goes through each episode
			episodeName = (series['episodes'][s][e]) #retrieves the episode name in season s episode e
			file = fileName(series,s,e,extention) #gets the name of the file
			print(combineName(file, episodeName)) #prints what the file will look like with the episode name as the suffix
	verify_with_user()

#goes through each subdirectory and renames each file with the episode name, retrieved from IMDB, as the suffix of the file 
def renameFiles(series, sNum, originalDir):
	for s in range(1,sNum+1): #for loop that goes through each season
		newDir = addToPath(originalDir, subdirs[s-1]) #sets the directory to a subfolder of the original show directory
		os.chdir(newDir)
		extention = findExtention(os.getcwd()) #finds the extention for the files
		epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
		for e in range(1,epCount+1): #for loop that goes through each episode
			episodeName = (series['episodes'][s][e]) #retrieves the episode name in season s episode e
			file = fileName(series,s,e,extention) #gets the name of the file
			#print(combineName(file, episodeName)) #prints what the finished file will look like
			os.rename(file, combineName(file, episodeName)) #renames the file with the episode suffix		
	os.chdir(originalDir) #sets the directory to the directory used when the program is called
	
originalDir = os.getcwd() #current directory

d = '.'	#https://www.tutorialspoint.com/How-to-get-a-list-of-all-sub-directories-in-the-current-directory-using-Python  --credit
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))] #array of all immediate subdirectories

showName = basename(originalDir) #gets the show name based on the current folder
#extention = input('What is the file extention? For example .mp4 or .mkv include the period: ') #gets the file extention from the user

series, sNum = seriesInfo(showName) #gets the series info set and the number of seasons
ia.update(series, 'episodes') #fetches the episode infoset

testRun(series, sNum, originalDir) #prints what the files will look like
renameFiles(series, sNum, originalDir) #if the users accepts the file format it will rename all the files
