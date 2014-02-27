#!usr/env/python

import requests
import facebook
import json
from uclassify import uclassify
from pyechonest import config, song
import random
import urllib, urllib2
import time


a = uclassify("own key here")
'''get your own '''
a.setReadApiKey("own key here")
a.setWriteApiKey("own key here")


#need to update the token every so often for now, about every hour
oauth_access_token = "own key here"
graph = facebook.GraphAPI(oauth_access_token)
newf = graph.get_connections("TuftsConfessions", "feed")



#schools to troll
schools = [
	 #MIT
	"CornellEdufess", #Cornell
	"521835501190847", #CMU
	"NYUSecrets" #NYU
	]

# array of message dictionaries
messg = []


#adds messages and other info into list of dictionaries
#returns the url of the next page to get
def addData(json_body):
	for i in json_body['data']:
		#creates a dictionary with the message and time
		post = {
			'message': i['message'],
			'created_time': i['created_time'], 
			'id' : i['id']
		}
		idList = []
		try:
			for j in i['comments']['data']:
				idList.append(j['from']['id']) #adds id onto lists
		except Exception:
			pass
		post['ids'] = idList 
		messg.append(post)

	#return messages #json_body['paging']['next']


#returns true if it would be fucked up to comment
def hasBuzzWords(status):

	triggers = ["rape", "abuse", "assault", "september 11", "9/11", 
		"holocaust", "suicide", "cancer"]

	for i in triggers:
		if i in status:
			return True

	return False





def isHappy(status):
	d = a.classify([status.encode('ascii', 'ignore')],"HappyorSad")
	happiness = d[0][2][0][1]
	if happiness >= 0.85:
		
		try:
			happiness = float(happiness)
			return happiness
		except Exception as e:
			print "Not a float ", e
			return 0
	else:
		return 0


#gets a shitload of data
#change value of xrange to get all teh dataz
#for x in xrange(1,450):
#	url = addData(newf)
#	r = requests.get(url)
#	if r.status_code != 200:
#		break
#	newf = json.loads(r.text)





def isSad(status):
	d = a.classify([status.encode('ascii', 'ignore')],"HappyorSad")
	sadness = d[0][2][1][1]
	if sadness >= 0.85:
		
		try:
			sadness = float(sadness)
			return sadness
		except Exception as e:
			print "Not a float ", e
			return 0
	else:
		return 0


def isHorny(status):

	d = a.classify([status.encode('ascii', 'ignore')],"HornyorNot")
	horniness = d[0][2][0][1]
	if horniness >= 0.85:
		try:
			horniness = float(horniness)
			return horniness
		except Exception as e:
			print "Not a float ", e
			return 0
	else:
		return 0


#figures out the dominant emotion
def largestEmotion(x, y, z):
	#x = happy
	#y = sad
	#z = horny

	bad = " "
	retVal = ""
	if x == y and x == z:
		retVal = bad
	if x > y and x > z:
		retVal = "happy"
	if y > x and y > z:
		retVal = "sad"
	if z > x and z > y:
		retVal = "horny"
	if x == y and x > z:
		retVal = bad
	if x == z and x > y:
		retVal = bad
	if y == z and y > x:
		retVal = bad

	return retVal

#uses echonest api to get songs based on mood
def _getSongUrl(mood):
	if mood == 'horny':
		mood = 'sensual'

	config.ECHO_NEST_API_KEY="BZWQIXTMDR70QO4YF"

	url = 'http://developer.echonest.com/api/v4/song/search/'

	mood_test = song.search(mood=mood, results=30)
	s = mood_test[random.randint(0,29)]

	data = {
		'api_key': config.ECHO_NEST_API_KEY,
		'format': 'json',
		'results': '1',
		'artist': s.artist_name,
		'title': s.title,
		'bucket': 'id:spotify-WW',
		}
	data2 = {
		'bucket': 'tracks'
	}


	data = urllib.urlencode(data)
	data2 = urllib.urlencode(data2)
	url = url + '?' + data + '&' + data2

	response = urllib2.urlopen(url)

	data = json.loads(response.read())

	song_id = data['response']['songs'][0]['tracks'][0]['foreign_id']
	info = song_id.split(':')
	spotify_id = info[len(info)-1]

	spotify_url = "http://play.spotify.com/track/" + spotify_id

	return spotify_url



#keeps getting until valid url is found
def getSongUrl(mood):
	foundSong = False
	retVal = ''
	while( not foundSong):
		try:
			retVal = _getSongUrl(mood)
			foundSong = True
		except Exception:
			foundSong = False

	return retVal


#returns what to comment
def filterStatus(status):
	time.sleep(1)
	emotion = largestEmotion(isHappy(status), isSad(status), isHorny(status))
	comment = " "
	url = getSongUrl(emotion)
	if emotion == "happy":
		comment = "You seem happy, give this a listen:  " + url

	if emotion == "sad":
		comment = "You seem sad, give this a listen: " + url

	if emotion == "horny":
		comment = "You seem horny, give this a listen: " + url
	
	return comment


#comments on messages
def comment(messg):
	for i in messg:
		data = filterStatus(i['message'])
		print "message :", data
		if i['id'] not in i['ids'] and not hasBuzzWords(i['message']) and data != " ":
			graph.put_object(i['id'], "comments", message=data)
		
			
			

if __name__ == '__main__':
	addData(newf)
	comment(messg)




