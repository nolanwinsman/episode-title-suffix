import os
from os.path import basename
import string
import imdb #run 'pip install IMDbPY' if you do not have the api

#this program creates season folders of a tv show in the plex format
#and fills the season folders with mock episode files to test the eSuffixV2.py

ia = imdb.IMDb() #calls the IMDb function to get an access object through which IMDB data can be retrieved

#function that combines the directory name with the subfolder name so the subfolder is the new directory
def addToPath(currentDirectory, subFolder):
	return "{currentDirectory}/{subFolder}".format(currentDirectory=currentDirectory, subFolder=subFolder)

#uses the IMDB api to find and store information on the show
def seriesInfo(showName):
    series = ia.search_movie(showName) #searches for the series
    id = series[0].getID() #stores the ID of the first result of the search
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

def findExtention(directory):
	extentions = []
	for roots, dirs, files in os.walk(spath):
		for file in files:
			name, ext = os.splitext(file)
			print("extention = %s" % ext)
			extentions.append(file)
		
originalDir = os.getcwd() #current directory

showName = basename(originalDir) #gets the show name based on the current folder
extention = '.mkv' #the extention of the dummy files

series, sNum = seriesInfo(showName) #gets the series info set and the number of seasons
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
		file = open("{path}\\{fileName}".format(path = cPath, fileName = fileN),'w') #creates dummy file named as if it is an episode of the show
		file.close() #closes the file created in the previous line

os.chdir(originalDir) #sets the directory to the directory used when the program is called