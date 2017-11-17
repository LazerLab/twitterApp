#!/apps/python/2.7.13/bin/python


import os
import cgi
import cgitb; cgitb.enable()
import requests
from requests_oauthlib import OAuth1Session
import io
import json
import gzip


from topRetweets import *

print 'Content-type: text/html\n\n'

form = cgi.FieldStorage()

client_key = '0XjfIpYCYq9Ve2FLaO5MOVoEv'
client_secret = '2ne1n8nqsCg6eN20RPg0Nbuyt83coyTSGYu6SahqKnPePd8XYF' 
callback_uri = 'http://www.codewithaheart.com/authkeys/2authkey.cgi?action=step3'

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
 	#print '<br> resource_owner_key: ' + resource_owner_key
	#print '<br> resource_owner_secret: ' + resource_owner_secret

# STEP 4: Access protected resources. OAuth1 access tokens typically do not expire and may be re-used until revoked by the user or yourself.
	tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
	credentials_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

	# Using OAuth1Session
	oauth = OAuth1Session(client_key,
			      client_secret=client_secret,
			      resource_owner_key=resource_owner_key,
			      resource_owner_secret=resource_owner_secret)
	r = oauth.get(tweets_url)
	c = oauth.get(credentials_url)

	# retrieving screen name
	credentials =  c.json()
	screenName =  credentials["screen_name"]	
	
	# saving keys to file:
	keyToFile = open('/www/codewithaheart.com/docs/authkeys/keys/' + screenName + '.txt', 'a') 
	keyToFile.write(screenName + ',' + resource_owner_key + ',' + resource_owner_secret + ',\n')

# STEP 5: writes tweets to a json file and analyses results:

	jsonFileName = '/www/codewithaheart.com/docs/authkeys/json/' + screenName + '.json.gz'
	
	with gzip.GzipFile(jsonFileName, 'w') as outfile:
		for obj in r.json():
        		outfile.write(json.dumps(obj) + '\n')
	
	# analysing user's data
	list_usersRetweeted = retweetedUser(jsonFileName)
	top5Retweeted = topFiveRetweeted(list_usersRetweeted)	
	list_usersReplied = repliedUser(jsonFileName)
	top5Replied = topFiveReplied(list_usersReplied)	
	
	html = """
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="/authkeys/style.css" />
	</head>
	<body>
	<br><br><br><br>
	<h1> I've found some interesting data for @{screenName}... </h1>
	<p><br><br>{top5Retweeted}
	<br><br>
	<p> {top5Replied}
	</body>
	</html>
	"""

	html = html.format(screenName=screenName, top5Retweeted=top5Retweeted, top5Replied=top5Replied)
	print html

	debugFile = open('/www/codewithaheart.com/docs/authkeys/debug/debug.txt', 'a') 
	debugFile.write(html + '\n\n\n\n\n')
