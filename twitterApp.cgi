#!/apps/python/2.7.13/bin/python

##============================================================================== 
# file:                 twitterApp.cgi
# date:                 Thu Jan 25 00:31:03 GMT 2018
# author(s):            Thalita Coleman  <thalitaneu@gmail.com>
# abstract:             Obtains user twitter keys, calls functions tha retrieves 
#			tweets data from Twitter API, writes data to file, 
#			analyses results and dysplays on webpage.
#------------------------------------------------------------------------------ 
# requirements: python 2.7, generateGraphs.py, generateStats.py, collectTweets.py 
#------------------------------------------------------------------------------ 
##============================================================================== 

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

reload(sys)
sys.setdefaultencoding('utf8')


from generateGraphs import *
from generateStats import *
from collectTweets import *

print 'Content-type: text/html\n\n'

form = cgi.FieldStorage()

client_key = '0XjfIpYCYq9Ve2FLaO5MOVoEv'
client_secret = '2ne1n8nqsCg6eN20RPg0Nbuyt83coyTSGYu6SahqKnPePd8XYF' 
#callback_uri = 'http://www.codewithaheart.com/test/twitterApp.cgi?action=testing'
#callback_uri = 'http://www.codewithaheart.com/test/twitterApp.cgi?action=step3'
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

# STEP 2: Obtain authorization from the user (resource owner) to access their tweets. 
	
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
	settings_url = 'https://api.twitter.com/1.1/account/settings.json'

	# Using OAuth1Session
	oauth = OAuth1Session(client_key,
			      client_secret=client_secret,
			      resource_owner_key=resource_owner_key,
			      resource_owner_secret=resource_owner_secret)
	s = oauth.get(settings_url)

	# retrieving screen name and timezone
	settings =  s.json()
        screenName =  settings["screen_name"]
        if "time_zone" in settings:
		tzinfo_name = settings["time_zone"]["tzinfo_name"] 
	else:
		tzinfo_name = 'UTC' 
		

	# saving keys to file:
	keyToFile = open('/www/codewithaheart.com/docs/twitterApp/kdata/' + screenName + '.txt', 'w') 
	keyToFile.write(screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 


# STEP 5: Writes tweets to a json file:
	jsonFileName = '/www/codewithaheart.com/docs/twitterApp/json/' + screenName + '_web.json.gz'
	numberTweets = getTweets(client_key, client_secret, resource_owner_key, resource_owner_secret, screenName, jsonFileName)

	if numberTweets == 0:
		print '<META http-equiv="refresh" content="0;URL=noTweets.html">'
	

# STEP 6: Analyses results and dysplays on webpage:
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
