import os
from os.path import basename
import string
import imdb #run 'pip install IMDbPY' if you do not have the api

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
		

originalDir = os.getcwd() #current directory

d = '.'	#https://www.tutorialspoint.com/How-to-get-a-list-of-all-sub-directories-in-the-current-directory-using-Python  --credit
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))] #array of all immediate subdirectories

showName = basename(originalDir) #gets the show name based on the current folder
extention = input('What is the file extention? For example .mp4 or .mkv include the period: ') #gets the file extention from the user

series, sNum = seriesInfo(showName) #gets the series info set and the number of seasons
ia.update(series, 'episodes') #fetches the episode infoset

for s in range(1,sNum+1): #for loop that goes through each season
	newDir = addToPath(originalDir, subdirs[s-1]) #sets the directory to a subfolder of the original show directory
	os.chdir(newDir)
	epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
	for e in range(1,epCount+1): #for loop that goes through each episode
		episodeName = (series['episodes'][s][e]) #retrieves the episode name in season s episode e
		file = fileName(series,s,e,extention) #gets the name of the file
		#print(combineName(file, episodeName)) #prints what the finished file will look like
		os.rename(file, combineName(file, episodeName)) #renames the file with the episode suffix		

os.chdir(originalDir) #sets the directory to the directory used when the program is called
