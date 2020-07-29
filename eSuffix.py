#plans for version 4
	#1: add verification to subfolders that checks if they are seasons example 'Season 1' or 's1' 
	#2: show the user information based on the IMDB search to verify it is the correct show. Information like cast, year, cover art
	#3: make sure the extention is a valid video file extention based on what VLC is compatable with
	#4:

import os #used primarily to rename the files
from os.path import basename #used to retrieve the TV show name from the current directory
import string
from tkinter import * #used to display the cover image of the TV show
from PIL import ImageTk, Image  # pip install pillow
import imdb #run 'pip install IMDbPY' if you do not have the api
from collections import Counter
from PIL import Image #pip install pillow
import requests #used to open the cover image from a URL
import pathlib #used to verify if 'IMDB.ico' is found

ia = imdb.IMDb() #calls the IMDb function to get an access object through which IMDB data can be retrieved

	#adds a leading zero to season and episode numbers less than 10 and returns the file name in Plex standard
def fileName(showName, s, e, ext):
    file =f'{series} S{str(s).zfill(2)}E{str(e).zfill(2)}{ext}' # concatenate the file together in Plex format
    return file
   
	#In windows you can't name files with certain chars, chars like ':' so this function removes any of those illegal chars 
def removeChars(episodeName, illegal_chars):
	episodeName = str(episodeName) #makes the episodeName a string
	for c in illegal_chars: #for loop that goes through illegal chars
		episodeName = episodeName.replace(c,'') #replaces illegal char with empty space
	return episodeName  
 
	#function that combines the directory name with the subfolder name so the subfolder is the new directory
def addToPath(currentDirectory, subFolder):
	return "{currentDirectory}/{subFolder}".format(currentDirectory=currentDirectory, subFolder=subFolder)
	
   #Takes a file and adds the episode name as a suffix to the file
   #credit to user "Łukasz Rogalski" on stack overflow for the majority of this function
def combineName(showName, epName): #showName is the file, epName is the name of the episode
    name, ext = os.path.splitext(showName)
    return "{name} {suffix}{ext}".format(name=name, suffix = epName, ext=ext)

	#uses the IMDB api to find and store information on the show
def seriesInfo(showName, r):
    series = ia.search_movie(showName) #searches for the series
    id = series[r].getID() #stores the ID of the first result of the search
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
	print('----------')
	answer = yesNoExit(input('Do you want to rename your files like the above file names? y for yes n for no: '))
	if answer == False:
		exit()
	elif answer == True:
		return


	#similar to the ranameFiles() function but this just prints the results so it can show the user how the files will look once renameFiles() is called
def testRun(series, sNum, originalDir):
	for s in range(1,sNum+1): #for loop that goes through each season
		print("S = ",s-1)
		newDir = addToPath(originalDir, subdirs[s-1]) #sets the directory to a subfolder of the original show directory
		extention = findExtention(newDir) #finds the extention for the files
		epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
		print(f'-----Season {s}-----') #prints the season number
		for e in range(1,epCount+1): #for loop that goes through each episode
			episodeName = series['episodes'][s][e]
			episodeName = removeChars(str(episodeName),illegalChars) #retrieves the episode name in season s episode e and removes illegal chars
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
			episodeName = series['episodes'][s][e]
			episodeName = removeChars(str(episodeName),illegalChars) #retrieves the episode name in season s episode e and removes illegal chars
			file = fileName(series,s,e,extention) #gets the name of the file
			os.rename(file, combineName(file, episodeName)) #renames the file with the episode suffix		
	os.chdir(originalDir) #sets the directory to the directory used when the program is called

#function that asks the user if the show found on IMDB is the correct one
def verifySeries(showName,r):
	if r > 4:	#(BASE CASE) recursively loops through the firt 5 IMDB search results
		exit()
	else:		#searches IMDB for the showName  
		series = ia.search_movie(showName) #searches for the series
		id = series[r].getID() #stores the ID of the r result of the search (if r == 0 it's the first result and so on)
		series = ia.get_movie(id) #gets the series
		if series['kind'] != 'tv series': #if the IMDB search result is not a TV show, try next result
			print(r,') ',series,' Is not a TV show, it is a',series['kind'],'trying next result in IMDB')
			verifySeries(showName,r+1)
		else: #if the IMDB search result is a TV show, ask the user if it is the right show
			displaySeriesInfo(series)
			answer = yesNoExit(input('Is this the show you want? y for Yes, n for No e for Exit:')) #gets a yes or no from user
			if answer == False:
				verifySeries(showName,r+1)
			else:
				return r

	#prints a variety of information about the TV show
def displaySeriesInfo(series): #not printing in a legible format, fix later
	print(series.keys())
	print('----------')
	print('TV show name		:',series)
	print('Release year		:',series['year'])
	print('Number of seasons	:',series['number of seasons'])
	print('Cast 			:', end =' ') 
	for x in range(2):
		print(series['cast'][x], end =', ')
	print(series['cast'][3])
	displayCover(series)

	#function that displays the IMDB cover for the series
def displayCover(series):#credit to user 'Giovanni Cappellotto' on StackOverflow for this function 
	coverURL = series['cover url']
	longName = series['long imdb title']
	root.title(longName)
	icoPath = '' #path to where your 'IMDB.ico' is, totally optional
	icon(icoPath)
	canvas = Canvas(root, width = 500, height = 0)
	canvas.pack()
	my_img = ImageTk.PhotoImage(Image.open((requests.get(coverURL, stream=True).raw)))
	my_label = Label(image=my_img)
	my_label.pack()
	root.mainloop()

#if 'IMDB.ico' is found it will use it as the icon, if not the icon will be default
def icon(p):
	file = addToPath(p,'IMDB.ico')
	path = pathlib.Path(file)
	if path.exists() == True and path.is_file() == True:
		root.iconbitmap(file)
	else:
		print('IMDB.ico not found')

	#asks the user yes or no until until they respond with an appropriate string
def yesNoExit(answer):
	print('---------')
	if answer == 'n' or answer == 'no' or answer == 'No' or answer == 'NO' or answer == 'N':
		return False
	elif answer == 'y' or answer == 'yes' or answer == 'Yes' or answer == 'YES' or answer == 'Y':
		return True
	elif answer == 'exit' or answer == 'Exit' or answer == 'EXIT' or answer == 'e' or answer == 'E':
		exit()
	else:
		yesNoExit(input('Wrong input, type y for Yes, and n for No, e for Exit: '))

originalDir = os.getcwd() #current directory
d = '.'	#https://www.tutorialspoint.com/How-to-get-a-list-of-all-sub-directories-in-the-current-directory-using-Python  --credit
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))] #array of all immediate subdirectories
showName = basename(originalDir) #gets the show name based on the current folder

root = Tk()

result = verifySeries(showName, 0) #finds which IMDB search result is the correct one
series, sNum = seriesInfo(showName, result) #gets the series info set and the number of seasons
ia.update(series, 'episodes') #fetches the episode infoset

illegalChars = ['\\','/',':','*','?','"','<','>','|'] #list of illegal chars for Windows
testRun(series, sNum, originalDir) #prints what the files will look like
renameFiles(series, sNum, originalDir) #if the users accepts the file format it will rename all the files
