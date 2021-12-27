import os
from tkinter import *
from os.path import basename
import string
import imdb #run 'pip install IMDbPY' if you do not have the api
from PIL import ImageTk, Image  # pip install pillow
import requests
import pathlib
import os

#this program creates season folders of a tv show in the plex format
#and fills the season folders with mock episode files to test the eSuffixV2.py

ia = imdb.IMDb() #calls the IMDb function to get an access object through which IMDB data can be retrieved

#function that combines the directory name with the subfolder name so the subfolder is the new directory
def addToPath(currentDirectory, subFolder):
	return "{currentDirectory}/{subFolder}".format(currentDirectory=currentDirectory, subFolder=subFolder)
	

#uses the IMDB api to find and store information on the show
def seriesInfo(showName, r):
    series = ia.search_movie(showName) #searches for the series
    id = series[r].getID() #stores the ID of the first result of the search
    series = ia.get_movie(id) #gets the series
    numberOfSeasons = series['number of seasons'] #stores the number of seasons the series has
    return series,numberOfSeasons

#Takes a file and adds the episode name as a suffix to the file
#credit to user "Łukasz Rogalski" on stack overflow for the majority of this function
def combineName(showName, epName): #showName is the file, epName is the name of the episode
    name, ext = os.path.splitext(showName)
    return "{name} {suffix}{ext}".format(name=name, suffix = epName, ext=ext)		

#adds a leading zero to season and episode numbers less than 10 and returns the file name in Plex standard
def fileName(showName, s, e, ext):
    fileN =f'{series} S{str(s).zfill(2)}E{str(e).zfill(2)}{ext}' # concatenate the file together in Plex format
    return fileN

#creates folders for each season in the form 'Season 1', 'Season 2" ect
def createSeasonFolders(s):
	for x in range(1,s+1):
		folderName = "{season} {x}".format(season = 'Season', x = x)
		#print(folderName)
		os.makedirs(folderName) #creates a folder for each season in the season	
	
	#finds the file extention
def findExtention(directory):
	extentions = [] #empty list that will hold extentions
	for roots, dirs, files in os.walk(spath):
		for file in files:
			name, ext = os.splitext(file)
			print("extention = %s" % ext)
			extentions.append(file)

#function that asks the user if the show found on IMDB is the correct one
def verifySeries(showName,r):
	if r > 4:	#(BASE CASE) recursively loops through the firt 5 IMDB search results
		print('Series now found')
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
	#print(series.keys())
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
	icon()
	canvas = Canvas(root, width = 500, height = 0)
	canvas.pack()
	my_img = ImageTk.PhotoImage(Image.open((requests.get(coverURL, stream=True).raw)))
	my_label = Label(image=my_img)
	my_label.pack()
	root.mainloop()

def icon():
	file = 'IMDB.ico'
	if os.path.isfile(file):
		root.iconbitmap(file)
	else:
		print('IMDB.ico not found')

	#asks the user yes or no until until they respond with an appropriate string
def yesNoExit(answer):
	if answer == 'n' or answer == 'no' or answer == 'No' or answer == 'NO' or answer == 'N':
		return False
	elif answer == 'y' or answer == 'yes' or answer == 'Yes' or answer == 'YES' or answer == 'Y':
		return True
	elif answer == 'exit' or answer == 'Exit' or answer == 'EXIT' or answer == 'e' or answer == 'E':
		exit()
	else:
		yesNoExit(input('Wrong input, type y for Yes, n for No, and e for Exit: '))

OperatingSystem = os.name

originalDir = os.getcwd() #current directory
root = Tk()
showName = basename(originalDir) #gets the show name based on the current folder
extention = '.mkv' #the extention of the dummy files
result = verifySeries(showName, 0)
series, sNum = seriesInfo(showName, result) #gets the series info set and the number of seasons
ia.update(series, 'episodes') #fetches the episode infoset
createSeasonFolders(sNum)

d = '.'	#https://www.tutorialspoint.com/How-to-get-a-list-of-all-sub-directories-in-the-current-directory-using-Python  --credit
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))] #array of all immediate subdirectories

for s in range(1,sNum+1): #for loop that goes through each season
	newDir = addToPath(originalDir, subdirs[s-1]) #sets the directory to a subfolder of the original show directory
	os.chdir(newDir)
	#print(os.getcwd())
	epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
	for e in range(1,epCount+1): #for loop that goes through each episode
		fileN = fileName(series,s,e,extention) #gets the name of the file
		cPath = os.getcwd() #gets the current directory path
		#print('cPath = ',cPath)
		#print(fileN) #prints what the finished file will look like
		if OperatingSystem == 'posix': # Linux
			file = open(r"{path}/{fileName}".format(path = cPath, fileName = fileN),'w') #creates dummy file named as if it is an episode of the show
		elif OperatingSystem == 'nt': # Windows
			file = open(r"{path}\{fileName}".format(path = cPath, fileName = fileN),'w') #creates dummy file named as if it is an episode of the show
		else:
			print('Unsupported Operating System')
			quit()

		file.close() #closes the file created in the previous line

os.chdir(originalDir) #sets the directory to the directory used when the program is called