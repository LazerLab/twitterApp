#!/apps/python/2.7.13/bin/python

##==============================================================================
# file:                 generateStats.py
# date:                 Thu Jan 25 00:31:03 GMT 2018
# author(s):            Thalita Coleman  <thalitaneu@gmail.com>
# abstract:             Contains functions that reads tweets from json file and 
#			process data.
#------------------------------------------------------------------------------
# requirements: python 2.7
#------------------------------------------------------------------------------
##==============================================================================

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
# lists: returns a list of screen names 
# of accounts retweeted, replied to, and
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
				# extract the reference handle from the tweet text
				else: 
					tweetText = tweet["text"]
                                        tweetText = tweetText.replace('RT @', '')
                                        referenceHandle = re.sub(r':.*$', '', tweetText)
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
# topTenRetweeted: returns the 10 screen names 
# of accounts the user retweets the most
#------------------------------
def topTenRetweeted(list_users):
	data = Counter(list_users)
	counter = 1
	mostCommon_screenName = []
	mostCommon_value = []
	for x in data.most_common(10):
		mostCommon_screenName.append(x[0])
		mostCommon_value.append(x[1])
		counter += 1
	if len(mostCommon_screenName) >= 1:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> Here are the people you retweet the most:']
	else:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> Well, it seems like you don&#39;t retweet a lot.']
	mostCommon.append('</div>\n</center>')
	mostCommon_screenName += [' '] * (10 - len(mostCommon_screenName))	#fills the list with ' ' until it has 10 items
	mostCommon_value += [0] * (10 - len(mostCommon_value))		#fills the list with 0 until it has 10 items
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value



#------------------------------
# topTenReplied: returns the 10 screen names 
# of accounts the user retweets to the most
#------------------------------
def topTenReplied(list_users, screenName):
	list_users = list(filter(lambda x: x!= screenName, list_users))
	data = Counter(list_users)
	counter = 1
	mostCommon_screenName = []
	mostCommon_value = []
	for x in data.most_common(10):
		mostCommon_screenName.append(x[0])
		mostCommon_value.append(x[1])
		counter += 1
	if len(mostCommon_screenName) >= 1:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> You frequently reply to:']
	else:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> Replying is not your thing. That&#39;s ok!']
	mostCommon.append('</div>\n</div>\n</center>')
	mostCommon_screenName += [' '] * (10 - len(mostCommon_screenName))	#fills the list with ' ' until it has 10 items
	mostCommon_value += [0] * (10 - len(mostCommon_value))	#fills the list with 0 until it has 10 items
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value

#------------------------------
# topFiveMentioned: returns the 5 screen names 
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
		mostCommon = ['<center><div class="section-header" style="position: relative; height:5vh; width: 80vw; border: 0px solid black"><br> You usually mention:']
	else:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> Mmm... we&#39;ve found that you usually don&#39;t mention other users in your tweets.']
	mostCommon.append('</div>\n</center>')
	mostCommon_screenName += [' '] * (5 - len(mostCommon_screenName))
	mostCommon_value += [0] * (5 - len(mostCommon_value))
	return ' '.join(mostCommon), mostCommon_screenName, mostCommon_value


#------------------------------
# topTenHashtags: returns the 10 most common
# hashtags mentioned by the user
#------------------------------
def topTenHashtags(list):
	data = Counter(list)
	counter = 1
	mostCommon_hashtag = []
	mostCommon_value = []
	for x in data.most_common(10):
		if counter >= 1:
			mostCommon_hashtag.append(x[0])
			mostCommon_value.append(x[1])
			counter += 1
	if len(mostCommon_hashtag) >= 1:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> And your top hashtags are...']
	else:
		mostCommon = ['<center><div class="section-header" style="position: relative; height:3vh; width: 80vw; border: 0px solid black"><br> We didn&#39;t find any hashtags in your posts']
	mostCommon.append('</div>\n</center>')
	mostCommon_hashtag += [' '] * (10 - len(mostCommon_hashtag))	#fills the list with ' ' until it has 10 items
	mostCommon_value += [0] * (10 - len(mostCommon_value))	#fills the list with 0 until it has 10 items
	return ' '.join(mostCommon), mostCommon_hashtag, mostCommon_value


#------------------------------
# popularWeekdays: returns the day of the week
# the user is more active on Twitter
#------------------------------
def getPopularWeekdays(times):
	# date of the 1st tweet on the list
        firstTweet = times[-1] # Mon Jan 16 06:56:18 -0800 2017
        dateFirstTweet = firstTweet.split() # ['Mon', 'Jan', '16', '06:56:18', '-0800', '2017']
        dateFirstTweet = dateFirstTweet[1] + ' ' + dateFirstTweet[2] + ', ' + dateFirstTweet[5] # Jan 16, 2017

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
        return popularDay, dateFirstTweet



#------------------------------
# popularHour: returns the hours of the  day 
# the user is more active on Twitter
#------------------------------
def getPopularHours(times):
	hour = [11,12]  # the hour is the 11,12 elements in Mon Mar 28 15:59:45 +0000 2011
	hours = []
	hourFormat = {'01': '1 A.M.', '02': '2 A.M.', '03': '3 A.M.', '04': '4 A.M.', '05': '5 A.M.', '06': '6 A.M.', '07': '7 A.M.', '08': '8 A.M.', '09': '9 A.M.', '10': '10 A.M.', '11': '11 A.M.', '12': 'noon', '13': '1 P.M.', '14': '2 P.M.', '15': '3 P.M.', '16': '4 P.M.', '17': '5 P.M.', '18': '6 P.M.', '19': '7 P.M.', '20': '8 P.M.', '21': '9 P.M.', '22': '10 P.M.', '23': '11 P.M.', '00': 'midnight'} 
	sundayMorning = []
	sundayAfternoon = []
	sundayEvening = []
	sundayNight = []
	mondayMorning = []
	mondayAfternoon = []
	mondayEvening = []
	mondayNight = []
	tuesdayMorning = []
	tuesdayAfternoon = []
	tuesdayEvening = []
	tuesdayNight = []
	wednesdayMorning = []
	wednesdayAfternoon = []
	wednesdayEvening = []
	wednesdayNight = []
	thursdayMorning = []
	thursdayAfternoon = []
	thursdayEvening = []
	thursdayNight = []
	fridayMorning = []
	fridayAfternoon = []
	fridayEvening = []
	fridayNight = []
	saturdayMorning = []
	saturdayAfternoon = []
	saturdayEvening = []
	saturdayNight = []

	for t in times:
	# appends the hours to the list
        	hours.append(''.join(itemgetter(*hour)(t)))
		time = ''.join(itemgetter(*hour)(t))

	# appends hours to all the sunday lists. 	
		if t[0] == 'S' and t[1] == 'u':  # identifies that the day of the week is Sunday	
			if int(time) >= 06 and int(time) <= 11:
				sundayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				sundayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				sundayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				sundayNight.append(time)


	# appends hours to all the monday lists. 	
		if t[0] == 'M' and t[1] == 'o':  # identifies that the day of the week is Monday	
			if int(time) >= 06 and int(time) <= 11:
				mondayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				mondayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				mondayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				mondayNight.append(time)


	# appends hours to all the tuesday lists. 	
		if t[0] == 'T' and t[1] == 'u':  # identifies that the day of the week is Tuesday	
			if int(time) >= 06 and int(time) <= 11:
				tuesdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				tuesdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				tuesdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				tuesdayNight.append(time)


	# appends hours to all the wednesday lists. 	
		if t[0] == 'W' and t[1] == 'e':  # identifies that the day of the week is Wednesday	
			if int(time) >= 06 and int(time) <= 11:
				wednesdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				wednesdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				wednesdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				wednesdayNight.append(time)


	# appends hours to all the thursday lists. 	
		if t[0] == 'T' and t[1] == 'h':  # identifies that the day of the week is Thursday	
			if int(time) >= 06 and int(time) <= 11:
				thursdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				thursdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				thursdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				thursdayNight.append(time)


	# appends hours to all the friday lists. 	
		if t[0] == 'F' and t[1] == 'r':  # identifies that the day of the week is Friday	
			if int(time) >= 06 and int(time) <= 11:
				fridayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				fridayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				fridayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				fridayNight.append(time)


	# appends hours to all the saturday lists. 	
		if t[0] == 'S' and t[1] == 'a':  # identifies that the day of the week is Saturday	
			if int(time) >= 06 and int(time) <= 11:
				saturdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				saturdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				saturdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				saturdayNight.append(time)


        popularHour =  str(max(set(hours), key=hours.count))
        popularHour = hourFormat[str(popularHour)]

	return len(sundayMorning), len(sundayAfternoon), len(sundayEvening), len(sundayNight), len(mondayMorning), len(mondayAfternoon), len(mondayEvening), len(mondayNight), len(tuesdayMorning), len(tuesdayAfternoon), len(tuesdayEvening), len(tuesdayNight), len(wednesdayMorning), len(wednesdayAfternoon), len(wednesdayEvening), len(wednesdayNight), len(thursdayMorning), len(thursdayAfternoon), len(thursdayEvening), len(thursdayNight), len(fridayMorning), len(fridayAfternoon), len(fridayEvening), len(fridayNight), len(saturdayMorning), len(saturdayAfternoon), len(saturdayEvening), len(saturdayNight), popularHour


#------------------------------
# popularHourNormalized: returns the hours of the  day 
# the user is more active on Twitter
#------------------------------
def getPopularHoursNormalized(times):
	# date of the 1st tweet on the list
        firstTweet = times[-1] # Mon Jan 16 06:56:18 -0800 2017
	firstTweet = re.sub('[\+-].{4}\s', '', firstTweet) # remove timezone. It can create problems when converting to datetime
	firstTweet = datetime.strptime(firstTweet, '%a %b %d %X %Y')

	# date of the last tweet on the list
	lastTweet = times[0]
	lastTweet = re.sub('[\+-].{4}\s', '', lastTweet) # remove timezone. It can create problems when converting to datetime
	lastTweet = datetime.strptime(lastTweet, '%a %b %d %X %Y')

	#calculate weets between 1st and last tweets
	dateDelta = lastTweet - firstTweet
	weeks = dateDelta.days/7.00
	if weeks < 1:
		weeks = 1


	hour = [11,12]  # the hour is the 11,12 elements in Mon Mar 28 15:59:45 +0000 2011
	hours = []
	hourFormat = {'01': '1 A.M.', '02': '2 A.M.', '03': '3 A.M.', '04': '4 A.M.', '05': '5 A.M.', '06': '6 A.M.', '07': '7 A.M.', '08': '8 A.M.', '09': '9 A.M.', '10': '10 A.M.', '11': '11 A.M.', '12': 'noon', '13': '1 P.M.', '14': '2 P.M.', '15': '3 P.M.', '16': '4 P.M.', '17': '5 P.M.', '18': '6 P.M.', '19': '7 P.M.', '20': '8 P.M.', '21': '9 P.M.', '22': '10 P.M.', '23': '11 P.M.', '00': 'midnight'} 
	sundayMorning = []
	sundayAfternoon = []
	sundayEvening = []
	sundayNight = []
	mondayMorning = []
	mondayAfternoon = []
	mondayEvening = []
	mondayNight = []
	tuesdayMorning = []
	tuesdayAfternoon = []
	tuesdayEvening = []
	tuesdayNight = []
	wednesdayMorning = []
	wednesdayAfternoon = []
	wednesdayEvening = []
	wednesdayNight = []
	thursdayMorning = []
	thursdayAfternoon = []
	thursdayEvening = []
	thursdayNight = []
	fridayMorning = []
	fridayAfternoon = []
	fridayEvening = []
	fridayNight = []
	saturdayMorning = []
	saturdayAfternoon = []
	saturdayEvening = []
	saturdayNight = []

	for t in times:
	# appends the hours to the list
        	hours.append(''.join(itemgetter(*hour)(t)))
		time = ''.join(itemgetter(*hour)(t))

	# appends hours to all the sunday lists. 	
		if t[0] == 'S' and t[1] == 'u':  # identifies that the day of the week is Sunday	
			if int(time) >= 06 and int(time) <= 11:
				sundayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				sundayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				sundayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				sundayNight.append(time)


	# appends hours to all the monday lists. 	
		if t[0] == 'M' and t[1] == 'o':  # identifies that the day of the week is Monday	
			if int(time) >= 06 and int(time) <= 11:
				mondayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				mondayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				mondayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				mondayNight.append(time)


	# appends hours to all the tuesday lists. 	
		if t[0] == 'T' and t[1] == 'u':  # identifies that the day of the week is Tuesday	
			if int(time) >= 06 and int(time) <= 11:
				tuesdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				tuesdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				tuesdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				tuesdayNight.append(time)


	# appends hours to all the wednesday lists. 	
		if t[0] == 'W' and t[1] == 'e':  # identifies that the day of the week is Wednesday	
			if int(time) >= 06 and int(time) <= 11:
				wednesdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				wednesdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				wednesdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				wednesdayNight.append(time)


	# appends hours to all the thursday lists. 	
		if t[0] == 'T' and t[1] == 'h':  # identifies that the day of the week is Thursday	
			if int(time) >= 06 and int(time) <= 11:
				thursdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				thursdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				thursdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				thursdayNight.append(time)


	# appends hours to all the friday lists. 	
		if t[0] == 'F' and t[1] == 'r':  # identifies that the day of the week is Friday	
			if int(time) >= 06 and int(time) <= 11:
				fridayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				fridayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				fridayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				fridayNight.append(time)


	# appends hours to all the saturday lists. 	
		if t[0] == 'S' and t[1] == 'a':  # identifies that the day of the week is Saturday	
			if int(time) >= 06 and int(time) <= 11:
				saturdayMorning.append(time)
			elif int(time) >= 12 and int(time) <= 17:
				saturdayAfternoon.append(time)
			elif int(time) >= 18 and int(time) <= 23:
				saturdayEvening.append(time)
			elif int(time) >= 00 and int(time) <= 05:
				saturdayNight.append(time)


        popularHour =  str(max(set(hours), key=hours.count))
        popularHour = hourFormat[str(popularHour)]
	

	return len(sundayMorning)/weeks, len(sundayAfternoon)/weeks, len(sundayEvening)/weeks, len(sundayNight)/weeks, len(mondayMorning)/weeks, len(mondayAfternoon)/weeks, len(mondayEvening)/weeks, len(mondayNight)/weeks, len(tuesdayMorning)/weeks, len(tuesdayAfternoon)/weeks, len(tuesdayEvening)/weeks, len(tuesdayNight)/weeks, len(wednesdayMorning)/weeks, len(wednesdayAfternoon)/weeks, len(wednesdayEvening)/weeks, len(wednesdayNight)/weeks, len(thursdayMorning)/weeks, len(thursdayAfternoon)/weeks, len(thursdayEvening)/weeks, len(thursdayNight)/weeks, len(fridayMorning)/weeks, len(fridayAfternoon)/weeks, len(fridayEvening)/weeks, len(fridayNight)/weeks, len(saturdayMorning)/weeks, len(saturdayAfternoon)/weeks, len(saturdayEvening)/weeks, len(saturdayNight)/weeks, popularHour
