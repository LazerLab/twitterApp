#!/apps/python/2.7.13/bin/python

##============================================================================== 
# file:                 collectTweets.py 
# date:                 Thu Jan 25 00:31:03 GMT 2018
# author(s):            Thalita Coleman  <thalitaneu@gmail.com>
# abstract:             Obtains user twitter keys, calls functions tha retrieves 
#			tweets data from Twitter API, writes data to file, 
#			analyses results and dysplays on webpage.
#------------------------------------------------------------------------------ 
# requirements: python 2.7
#------------------------------------------------------------------------------ 
##============================================================================== 

import os
import requests
from requests_oauthlib import OAuth1Session
import io
import json
import gzip
import sys

reload(sys)
sys.setdefaultencoding('utf8')

 
#------------------------------
# getLastTweetId: returns the id
# of the last tweet of a list
#------------------------------
def getLastTweetId(tweetList):
	lastTweetPosition = len(tweetList) -1
	lastTweet = tweetList[lastTweetPosition]
	lastTweetId = lastTweet['id'] - 1
	#print 'last tweet id: ' + str(lastTweetId)
	return lastTweetId


#------------------------------
# getTweets: retrieves tweets from 
# Twitter API and save it to 
# a json file.
#------------------------------
def getTweets(client_key, client_secret, resource_owner_key, resource_owner_secret, screenName, jsonFileName): 
	tweetList = []
	count = 200
	tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=' + str(count) + '&screen_name=' + screenName

	oauth = OAuth1Session(client_key,
			      client_secret=client_secret,
			      resource_owner_key=resource_owner_key,
			      resource_owner_secret=resource_owner_secret)
	r = oauth.get(tweets_url)
	
	for obj in r.json():
		tweetList.append(obj)

	while len(r.json()) != 0:  
		lastTweetId = getLastTweetId(tweetList)
		tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=' + str(count) + '&max_id=' + str(lastTweetId) + '&screen_name=' + screenName
		r = oauth.get(tweets_url)
		for obj in r.json():
			tweetList.append(obj)
		
	
	# writes tweets to a json file:
	with gzip.GzipFile(jsonFileName, 'w') as outfile:
		for tweet in tweetList:
        		outfile.write(json.dumps(tweet) + '\n')
	
	return len(tweetList)


