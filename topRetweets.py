# 2topRetweets.py 

import gzip
import json
import json as simplejson 
import sys
import csv
from csv import writer
import re

import itertools
import operator

from collections import Counter 


def retweetedUser(jsonFileName):
	retweeted_users = []
	replied_users = []
	separator='\t'
	####### WORK ON TESTING FOR GZ FILE
	with gzip.open(jsonFileName) as in_file:
		for line in in_file:
			line = re.sub('[\r\n\t]', '', line)
			tweet = json.loads(line)
			regexTest = re.compile(r'full\_text')
			#print '<br><br>' + str(tweet)
			# ---- identifying twitter type ----
			# reply
			if tweet["in_reply_to_screen_name"] != None:
				tweetType = "Reply"
				referenceHandle = tweet["in_reply_to_screen_name"]
				referenceUrl = "unkkown" 
				retweets = tweet["retweet_count"]
				replied_users.append(referenceHandle)
				

			# retweet
			elif "retweeted_status" in tweet:
			#elif regexTest.search(tweet['text']):
				tweetType = "Retweet"
				if tweet["entities"]["user_mentions"] != []:
					referenceHandle = tweet["entities"]["user_mentions"][0]["screen_name"]
				else:
					referenceHandle = "testing"
				if tweet["entities"]['urls'] != []:
					referenceUrl = tweet["entities"]['urls'][0]["expanded_url"] 
				elif tweet["retweeted_status"]['entities']['urls'] != []:
					referenceUrl = tweet["retweeted_status"]['entities']['urls'][0]['expanded_url']
				else:
					referenceUrl = 'N/A' 
				retweets = tweet["retweeted_status"]["retweet_count"]		
				retweeted_users.append(referenceHandle)

		return (retweeted_users)
		

def repliedUser(jsonFileName):
	retweeted_users = []
	replied_users = []
	separator='\t'
	####### WORK ON TESTING FOR GZ FILE
	with gzip.open(jsonFileName) as in_file:
		for line in in_file:
			line = re.sub('[\r\n\t]', '', line)
			tweet = json.loads(line)
			regexTest = re.compile(r'full\_text')
			#print '<br><br>' + str(tweet)
			# ---- identifying twitter type ----
			# reply
			if tweet["in_reply_to_screen_name"] != None:
				tweetType = "Reply"
				referenceHandle = tweet["in_reply_to_screen_name"]
				referenceUrl = "unkkown" 
				retweets = tweet["retweet_count"]
				replied_users.append(referenceHandle)
				

			# retweet
			elif "retweeted_status" in tweet:
			#elif regexTest.search(tweet['text']):
				tweetType = "Retweet"
				if tweet["entities"]["user_mentions"] != []:
					referenceHandle = tweet["entities"]["user_mentions"][0]["screen_name"]
				else:
					referenceHandle = "testing"
				if tweet["entities"]['urls'] != []:
					referenceUrl = tweet["entities"]['urls'][0]["expanded_url"] 
				elif tweet["retweeted_status"]['entities']['urls'] != []:
					referenceUrl = tweet["retweeted_status"]['entities']['urls'][0]['expanded_url']
				else:
					referenceUrl = 'N/A' 
				retweets = tweet["retweeted_status"]["retweet_count"]		
				retweeted_users.append(referenceHandle)

		return (replied_users)


def topFiveRetweeted(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon = ['<br> Here are the people you retweet the most: ']
	#PLAYING WITH DIVS: 
	#mostCommon = ['<div style="width:300px; text-align: center; align: center;" ><br> Here are the people you retweet the most: <div align=left>']
	for x in data.most_common(5):
		if counter >= 1:
			mostCommon.append('<br>' + str(counter) + '. ' + x[0])
			counter += 1
		else:
			del mostCommon[:]
			mostCommon.append( "<br> Well, it seems like you don't retweet a lot.")
	#mostCommon.append('</div>\n</div>')
	return ' '.join(mostCommon)


def topFiveReplied(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon = ['<br> You frequently reply to: ']
	for x in data.most_common(5):
		if counter >= 1:
			mostCommon.append('<br>' + str(counter) + '. ' + x[0])
			counter += 1
		else:
			del mostCommon[:]
			mostCommon.append( "<br> Replying is not your thing. That's ok!")
	return ' '.join(mostCommon)

#quit()
#
#def topFive(list_users):
#	lU = sorted((x,i) for i, x in enumerate(list_users))
#	groups = itertools.groupby(lU, key=operator.itemgetter(0))
#	#print groups
#	#print lU
#	def _auxfun(g):
#		item, iterable = g
#		count =0
#		min_index = len(list_users)
#		for _, where in iterable:
#			count +=1
#			min_index = min(min_index, where)
#		#print count, -min_index
#		return count, -min_index
#	return max(groups, key=_auxfun)[0]

#print topFive(list_users)
