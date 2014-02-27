#!usr/env/python
# This program is a word frequency analyzer you can interact with it a
#and find interesting things about words!

import facebook
import simplejson as json
import requests


#gets a shitload of data
#change value of xrange to get all teh dataz


#need to update the token every so often for now, about every hour
oauth_access_token = "own key here"
graph = facebook.GraphAPI(oauth_access_token)
newf = graph.get_connections("TuftsConfessions", "feed")


#adds messages and other info into list of dictionaries
#returns the url of the next page to get

string_god_dayum = []

def addData(json_body):
	for i in json_body['data']:
		#creates a dictionary with the message and time
		string_god_dayum.append(i['message'])

	return json_body['paging']['next']

#gets data
for x in xrange(1,330):
	url = addData(newf)
	r = requests.get(url)
	if r.status_code != 200:
		break
	newf = json.loads(r.text)


word_dictionary = {}


def is_in(word, word_dictionary):
  for key in word_dictionary:
    if word in word_dictionary:
      return False
  return True

text_wordlist = []

for i in string_god_dayum:
	text_wordlist = i.split()
	for word in text_wordlist:
		if is_in(word, word_dictionary):
			word_dictionary[word] = 1
		else:
			word_dictionary[word] += 1
    
max_word = {}
max_word = sorted(word_dictionary, key=word_dictionary.get, reverse=True)[:100]

for key in max_word:
	print key
