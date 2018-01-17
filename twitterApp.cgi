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
reload(sys)
sys.setdefaultencoding('utf8')


from generateGraphs import *
from topRetweets import *

print 'Content-type: text/html\n\n'

form = cgi.FieldStorage()

client_key = '0XjfIpYCYq9Ve2FLaO5MOVoEv'
client_secret = '2ne1n8nqsCg6eN20RPg0Nbuyt83coyTSGYu6SahqKnPePd8XYF' 
callback_uri = 'http://www.codewithaheart.com/twitterApp/twitterApp.cgi?action=step3'

# Endpoints found in the OAuth provider API documentation
request_token_url = 'https://api.twitter.com/oauth/request_token'
authorization_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'


# STEP 1: Obtain a request token which will identify you (the client)
# in the next step. At this stage you will only need your client key and secret.

oauth = OAuth1Session(client_key, client_secret=client_secret, callback_uri=callback_uri)
action = form["action"].value

if action=='step1':
	fetch_response = oauth.fetch_request_token(request_token_url)
	resource_owner_key = fetch_response.get('oauth_token')
	resource_owner_secret = fetch_response.get('oauth_token_secret')

# STEP 2: Obtain authorization from the user (resource owner) to access their protected resources (images, tweets, etc.). This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter. Note that not all services will give you a verifier even if they should. Also the oauth_token given here will be the same as the one in the previous step.
	
	authorize_url = oauth.authorization_url(authorization_url)
	#print authorize_url	

	print '<META http-equiv="refresh" content="0;URL=' + authorize_url + '">'

# STEP 3: Obtain an access token from the OAuth provider. Save this token as it can be re-used later. In this step we will re-use most of the credentials obtained uptil this point.
if action=='step3':
	oauth_token = form["oauth_token"].value
	oauth_verifier = form["oauth_verifier"].value
	#print oauth_token
	#print oauth_verifier

	oauth = OAuth1Session(client_key, client_secret=client_secret, resource_owner_key=oauth_token, verifier=oauth_verifier)

	oauth_tokens = oauth.fetch_access_token(access_token_url)
	resource_owner_key = oauth_tokens.get('oauth_token')
	resource_owner_secret = oauth_tokens.get('oauth_token_secret')

# STEP 4: Access protected resources. OAuth1 access tokens typically do not expire and may be re-used until revoked by the user or yourself.
	tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=3200'
	credentials_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
	settings_url = 'https://api.twitter.com/1.1/account/settings.json'

	# Using OAuth1Session
	oauth = OAuth1Session(client_key,
			      client_secret=client_secret,
			      resource_owner_key=resource_owner_key,
			      resource_owner_secret=resource_owner_secret)
	r = oauth.get(tweets_url)
	c = oauth.get(credentials_url)
	s = oauth.get(settings_url)

	# retrieving screen name and timezone
	#credentials =  c.json()
	#screenName =  credentials["screen_name"]	
	settings =  s.json()
        screenName =  settings["screen_name"]
        if "time_zone" in settings:
		tzinfo_name = settings["time_zone"]["tzinfo_name"] 
	else:
		tzinfo_name = 'UTC' 
		

	# saving keys to file:
	keyToFile = open('/www/codewithaheart.com/docs/twitterApp/kdata/' + screenName + '.txt', 'w') 
	
	# this will be used if collecting the data through oauth flow
	#keyToFile.write(screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 

	# this will be used only if using the twitter_dm library to collect the data
	keyToFile.write(client_key + ',' + client_secret + '\n' + screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 

# STEP 5: writes tweets to a json file:
	
	# ---- TWITTER_DM ----
	# this will be used only if using the twitter_dm library to collect the data
	usernameToFile = open('/www/codewithaheart.com/docs/twitterApp/usernames/' + screenName + '.txt', 'w')
	usernameToFile.write(screenName)
	subprocess.Popen('python /home/thalita/twitter_dm/examples/collect_user_data_full.py kdata/' + screenName + '.txt usernames/' + screenName + '.txt twitter_dm_json/ n n y', shell=True)
	jsonFileName = '/www/codewithaheart.com/docs/twitterApp/twitter_dm_json/json/' + screenName + '.json.gz'

	# ---- OAUTH FLOW ----
	# this will be used if collecting the data through oauth flow
	#jsonFileName = '/www/codewithaheart.com/docs/twitterApp/json/' + screenName + '.json.gz'

	with gzip.GzipFile(jsonFileName, 'w') as outfile:
		for obj in r.json():
        		outfile.write(json.dumps(obj) + '\n')
	

# STEP 6: analyses results and dysplays on webpage:
	generateGraphs(screenName, jsonFileName, tzinfo_name)


# ==================================================
# 		- TESTING - 
# ==================================================

if action == "testing":
	print """
	<html>
	<head>
	</head>
	<body>
	<p> This is a test
	<form action="twitterApp.cgi" method="POST">
	Select a json file to process:
	<br><br> 
	"""
	jsonPath = "/www/codewithaheart.com/docs/test/json"
	jsonFiles = [f for f in listdir(jsonPath) if isfile(join(jsonPath, f))]
	for file in jsonFiles:
		print '<br><input type="radio" name="jsonFile" value="' + file + '">' + file 

	print """		
	<input type="hidden" name="action" value="processTestFile"> 
	<br>
	<input type="submit" value="process file">
	</form> 
	</body>
	</html>
 	"""

if action == "processTestFile":
	jsonPath = "/www/codewithaheart.com/docs/test/json"
	screenName = str(form["jsonFile"].value).replace('.json.gz', '')
	jsonFileName = jsonPath + "/" + str(form["jsonFile"].value)
	
	tzinfo_name = 'Europe/Oslo' 
	
	# analysing user's data
	generateGraphs(screenName, jsonFileName, tzinfo_name)
