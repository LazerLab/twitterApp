#!/apps/python/2.7.13/bin/python



import gzip
import json
import json as simplejson 
import sys
import re

import itertools
import operator
from operator import itemgetter

from collections import Counter 

from datetime import datetime
import pytz
from pytz import timezone

#------------------------------
# lists: returns a list screen names 
# of accounts retweeted, replied to and
# mentioned by the user; also returns
# a list of hashtags and timestamps
#------------------------------
def lists(jsonFileName, tzinfo_name):
	total_count = 0
	retweeted_users = []
	replied_users = []
	user_mentions = []
	hashtags = []
        timestamps = []
	separator='\t'
	####### WORK ON TESTING FOR GZ FILE
	with gzip.open(jsonFileName) as in_file:
		for line in in_file:
			line = re.sub('[\r\n\t]', '', line)
			total_count += 1
			tweet = json.loads(line)
			regexTest = re.compile(r'full\_text')

			# ---- identifying twitter type ----
			# retweet
			if "retweeted_status" in tweet:
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

			# reply
			if tweet["in_reply_to_screen_name"] != None:
				tweetType = "Reply"
				referenceHandle = tweet["in_reply_to_screen_name"]
				referenceUrl = "unkkown" 
				retweets = tweet["retweet_count"]
				replied_users.append(referenceHandle)

			# user mentions
			if tweet["entities"]["user_mentions"] != []:
				referenceHandle = tweet["entities"]["user_mentions"][0]["screen_name"]
				user_mentions.append(referenceHandle)

			# hashtags
			if tweet["entities"]["hashtags"] != []:
				text = tweet["entities"]["hashtags"][0]["text"] 
				hashtags.append(text)


			# timestamp
			utc_tz = pytz.timezone('UTC')
			utc_time = tweet["created_at"]
			utc_time = datetime.strptime(utc_time, '%a %b %d %X +0000 %Y')
                        utc_time = utc_time.replace(tzinfo=utc_tz)
                        user_time = utc_time.astimezone(timezone(tzinfo_name))
			user_time = user_time.strftime('%a %b %d %X %z %Y')
			timestamps.append(user_time)

		retweet_count = len(retweeted_users)
		reply_count = len(replied_users)
		tweet_count = total_count - (retweet_count + reply_count)	
		return str(total_count), str(tweet_count), str(retweet_count), str(reply_count), retweeted_users, replied_users, user_mentions, hashtags, timestamps
		


#------------------------------
# topFiveRetweeted: returns the 5 screen names 
# of accounts the user retweets the most
#------------------------------
def topFiveRetweeted(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon_screenName = []
	mostCommon_value = []
	for x in data.most_common(5):
		mostCommon_screenName.append(x[0])
		mostCommon_value.append(x[1])
		counter += 1
	if len(mostCommon_screenName) >= 1:
		mostCommon = ['<center><div class="sectionHeader"><br> Here are the people you retweet the most: <div class="sectionBody">']
		#for x in mostCommon_screenName:
		#	mostCommon.append('<br>' + str(counter) + '. ' + x)
	else:
		mostCommon = ['<center><div class="sectionHeader"><br> Well, it seems like you don''t retweet a lot.']
	mostCommon.append('</div>\n</div>\n</center>')
	mostCommon_screenName += [' '] * (5 - len(mostCommon_screenName))
	mostCommon_value += [0] * (5 - len(mostCommon_value))
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value



#------------------------------
# topFiveReplied: returns the 5 screen names 
# of accounts the user retweets to the most
#------------------------------
def topFiveReplied(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon_screenName = []
	mostCommon_value = []
	for x in data.most_common(5):
		mostCommon_screenName.append(x[0])
		mostCommon_value.append(x[1])
		counter += 1
	if len(mostCommon_screenName) >= 1:
		mostCommon = ['<center><div class="sectionHeader"><br> You frequently reply to: <div class="sectionBody"> ']
		#for x in mostCommon_screenName:
		#	mostCommon.append('<br>' + str(counter) + '. ' + x)
	else:
		mostCommon = ["<center><div class='sectionHeader'><br><br> Replying is not your thing. That''s ok!"]
	mostCommon.append('</div>\n</div>\n</center>')
	mostCommon_screenName += [' '] * (5 - len(mostCommon_screenName))
	mostCommon_value += [0] * (5 - len(mostCommon_value))
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value

#------------------------------
# topMentioned: returns the 5 screen names 
# of accounts the user mentions the most
#------------------------------
def topFiveMentioned(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon_screenName = []
	mostCommon_value = []
	for x in data.most_common(5):
		mostCommon_screenName.append(x[0])
		mostCommon_value.append(x[1])
		counter += 1
	if len(mostCommon_screenName) >= 1:
		mostCommon = ["<center><div class='sectionHeader'><br> We've got a list of people who you usually mention: <div class='sectionBody'>"]
	else:
		mostCommon = [ "<center><div class='sectionHeader'><br><br> Mmm... we've found that you usually don't mention other users in your tweets."]
	mostCommon.append('</div>\n</div>\n</center>')
	mostCommon_screenName += [' '] * (5 - len(mostCommon_screenName))
	mostCommon_value += [0] * (5 - len(mostCommon_value))
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value


#------------------------------
# topHashtags: returns the 5 most common
# hashtags mentioned by the user
#------------------------------
def topFiveHashtags(list):
	data = Counter(list)
	counter = 1
	mostCommon_hashtag = []
	mostCommon_value = []
	for x in data.most_common(5):
		if counter >= 1:
			mostCommon_hashtag.append(x[0])
			mostCommon_value.append(x[1])
			counter += 1
	if len(mostCommon_hashtag) >= 1:
		mostCommon = ["<center><div class='sectionHeader'><br> And your top hashtags are... <div class='sectionBody'>"]
	else:
		mostCommon = [ "<center><div class='sectionHeader'><br><br> We didn't find any hashtags in your posts"]
	mostCommon.append('</div>\n</div>\n</center>')
	mostCommon_hashtag += [' '] * (5 - len(mostCommon_hashtag))
	mostCommon_value += [0] * (5 - len(mostCommon_value))
	return ' '.join(mostCommon), mostCommon_hashtag, mostCommon_value

def numberRetweets(list_users):
	number = len(list_users)
	return str(number)


#------------------------------
# popularWeekdays: returns the day of the week
# the user is more active on Twitter
#------------------------------
def getPopularWeekdays(times):
	weekday = [0, 1, 2] # weekday is the 0-2 elements in the Mon Mar 28 15:59:45 +0000 2011
	weekdays = []
	fullName = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'} 
	
	# appends the weekdays to the list
	for t in times:
        	weekdays.append(''.join(itemgetter(*weekday)(t)))

        week = {}
        for w in weekdays:
                week[w] = weekdays.count(w)
        popularDay = max(week.iteritems(), key=operator.itemgetter(1))[0]
        popularDay =  fullName[popularDay]
        return popularDay


#------------------------------
# popularHour: returns the hour of the  day 
# the user is more active on Twitter
#------------------------------
def getPopularHours(times):
	hour = [11,12]  # the hour is the 11,12 elements in Mon Mar 28 15:59:45 +0000 2011
	hours = []
	hourFormat = {'01': '1 A.M.', '02': '2 A.M.', '03': '3 A.M.', '04': '4 A.M.', '05': '5 A.M.', '06': '6 A.M.', '07': '7 A.M.', '08': '8 A.M.', '09': '9 A.M.', '10': '10 A.M.', '11': '11 A.M.', '12': 'noon', '13': '1 P.M.', '14': '2 P.M.', '15': '3 P.M.', '16': '4 P.M.', '17': '5 P.M.', '18': '6 P.M.', '19': '7 P.M.', '20': '8 P.M.', '21': '9 P.M.', '22': '10 P.M.', '23': '11 P.M.', '00': 'midnight'} 
	# appends the hours to the list
	for t in times:
        	hours.append(''.join(itemgetter(*hour)(t)))

        popularHour =  str(max(set(hours), key=hours.count))
        popularHour = hourFormat[str(popularHour)]
        return popularHour



