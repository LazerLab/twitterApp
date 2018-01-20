#!/apps/python/2.7.13/bin/python

import os
import requests
from requests_oauthlib import OAuth1Session
import io
import json
import gzip
import sys

reload(sys)
sys.setdefaultencoding('utf8')


 
def getLastTweetId(tweetList):
	lastTweetPosition = len(tweetList) -1
	lastTweet = tweetList[lastTweetPosition]
	lastTweetId = lastTweet['id'] - 1
	#print 'last tweet id: ' + str(lastTweetId)
	return lastTweetId


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


