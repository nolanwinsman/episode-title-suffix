import os
import string
import imdb 

ia = imdb.IMDb() #calls the IMDb function to get an access object through which IMDB data can be retrieved

#adds a leading zero to season and episode numbers less than 10 and returns the file name in Plex standard
def fileName(showName, s, e, ext):
    file =f'{series} S{str(s).zfill(2)}E{str(e).zfill(2)}{ext}' # concatenate the file together in Plex format
    return file
    
   #Takes a file and adds the episode name as a suffix to the file
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

showName = input('What is the name of the show? Make sure it is spelled exactly the same as IMDB: ') #gets the show name from the user
extention = input('What is the file extention? For example .mp4 or .mkv include the period: ') #gets the file extention from the user

series, sNum = seriesInfo(showName) #gets the series info set and the number of seasons
ia.update(series, 'episodes') #fetches the episode infoset

for s in range(1,sNum+1): #for loop that goes through each season
    epCount = len(series['episodes'][s]) #retrieves the number of episodes in s season
    for e in range(1,epCount): #for loop that goes through each episode
        episodeName = (series['episodes'][s][e]) #retrieves the episode name in season s episode e
        file = fileName(series,s,e,extention) #gets the name of the file
        #print(combineName(file, episodeName)) #prints what the finished file will look like
        os.rename(file, combineName(file, episodeName)) #renames the file with the episode suffix