#!/apps/python/2.7.13/bin/python

import os
from os import listdir #only used for action=="testing"
from os.path import isfile, join #only used for action=="testing"
import cgi
import cgitb; cgitb.enable()
import requests
from requests_oauthlib import OAuth1Session
import io
import json
import gzip
import sys
import subprocess #only needed to call twitter_dm
subprocess.__file__

reload(sys)
sys.setdefaultencoding('utf8')


from generateGraphs import *
from topRetweets import *


client_key = '0XjfIpYCYq9Ve2FLaO5MOVoEv'
client_secret = '2ne1n8nqsCg6eN20RPg0Nbuyt83coyTSGYu6SahqKnPePd8XYF' 
# Thalita keys
#resource_owner_key = '795387202863792128-PfY2EnjuLXl34koL9kzTBAjOwAoles6'
#resource_owner_secret = '6wO0bSi0wKr3hTYfVBENIOjsHcLzPkYooSEw7j3Odr1j7'
#screenName = 'thalita10th'

# OrenTsur keys
#resource_owner_key = '106028818-g469YUJ1KdB0DfbeNjtpAAY7W1ClloxwHCAdTb8E'
#resource_owner_secret = '4LzeEcqITFPXmdoR0EFNlRth2coKAiTj6FeKuQXIxeHxE'
#screenName = 'OrenTsur'

# davidlazer keys
resource_owner_key = '37213193-6gttiKlecIyuRLeSLMFF7coxRbR0XuDQVl4Rb3Hsh'
resource_owner_secret = 'A72uZjJsHBQuP1YedODsoTbRxSPvWycJYZUubE9Rn5l2V'
screenName = 'davidlazer'

# oren_data keys
#resource_owner_key = '2772110550-0lVA7IDnFO7jebnok7P8NTkqI5vao8SLeJAkpcM' 
#resource_owner_secret = 'Z1nL7FFAo6qDRRFYFVQTZeEUSKpGXH4z3RTDJPUWpUu7e'
#screenName = 'oren_data'

# josefinath1 keys
#resource_owner_key = '875318679856087040-ZQYDKlJ1QjctmnpmmcaK716r9TCCOVv'
#resource_owner_secret = 'jRCILp3zuykPClf678NK7yphluC3YwGmVXfgl7wbeXiyv'
#screenName = 'josefinath1'

print 'screenName: ' + screenName 
tweetList = []
 
def getLastTweetId(tweetList):
	lastTweetPosition = len(tweetList) -1
	lastTweet = tweetList[lastTweetPosition]
	lastTweetId = lastTweet['id'] - 1
	#print 'last tweet id: ' + str(lastTweetId)
	return lastTweetId


# STEP 4: Access protected resources. OAuth1 access tokens typically do not expire and may be re-used until revoked by the user or yourself.
def getTweets(): 
	count = 200
	tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=' + str(count) + '&screen_name=' + screenName

	# Using OAuth1Session
	oauth = OAuth1Session(client_key,
			      client_secret=client_secret,
			      resource_owner_key=resource_owner_key,
			      resource_owner_secret=resource_owner_secret)
	r = oauth.get(tweets_url)
	
	print "len r: " + str(len(r.json()))
	for obj in r.json():
		tweetList.append(obj)
	#print tweetList


	while len(r.json()) != 0:  
	#while len(r.json()) >= count - 10:  
		lastTweetId = getLastTweetId(tweetList)
		tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=' + str(count) + '&max_id=' + str(lastTweetId) + '&screen_name=' + screenName
		r = oauth.get(tweets_url)
		for obj in r.json():
			tweetList.append(obj)
		
	print 'len final tweetList: ' + str(len(tweetList))
	
	# this will be used if collecting the data through oauth flow
	#keyToFile.write(screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 

# STEP 5: writes tweets to a json file:
	
	# ---- OAUTH FLOW ----
	# this will be used if collecting the data through oauth flow
	jsonFileName = '/www/codewithaheart.com/docs/twitterApp/json/' + screenName + '_script.json.gz'

	with gzip.GzipFile(jsonFileName, 'w') as outfile:
		for tweet in tweetList:
        		outfile.write(json.dumps(tweet) + '\n')
	

	return len(tweetList)


print getTweets()

getLastTweetId(tweetList)
