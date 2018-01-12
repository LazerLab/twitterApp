#!/apps/python/2.7.13/bin/python

import os
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
        tzinfo_name = settings["time_zone"]["tzinfo_name"] 

	# saving keys to file:
	keyToFile = open('/www/codewithaheart.com/docs/twitterApp/kdata/' + screenName + '.txt', 'w') 
	
	# this will be used if collecting the data through oauth flow
	#keyToFile.write(screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 

	# this will be used only if using the twitter_dm library to collect the data
	keyToFile.write(client_key + ',' + client_secret + '\n' + screenName + ',' + resource_owner_key + ',' + resource_owner_secret + '\n') 

# STEP 5: writes tweets to a json file and analyses results:
	
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
	
	# analysing user's data
	total_count, tweet_count, retweet_count, reply_count, list_usersRetweeted, list_usersReplied, list_usersMentioned, list_hashtags, list_times = lists(jsonFileName, tzinfo_name) 

	top5Retweeted = topFiveRetweeted(list_usersRetweeted)	
	#print list_usersRetweeted
	#print top5Retweeted

	top5Replied = topFiveReplied(list_usersReplied)	
	#print list_usersReplied
	#print top5Replied

	mentions = top10Mentioned(list_usersMentioned)
	#print mentions

	hashtags = top10hashtags(list_hashtags)
	#print hashtags

	popularDay = getPopularWeekdays(list_times)
	#print popularDay

	popularHour = getPopularHours(list_times)
	#print popularHour 

	html = """
	<!DOCTYPE html>
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="/twitterApp/style.css" />
		<link rel="stylesheet" type="text/css" href="/css/piechart.css">
		<script src="/js/chartjs/Chart.bundle.js"></script>
		<script src="/js/chartjs/utils.js"></script>
	<meta charset="utf-8">
	<script type="text/javascript">
Chart.defaults.global.tooltips.custom = function(tooltip) {
                // Tooltip Element
                var tooltipEl = document.getElementById('chartjs-tooltip');

                // Hide if no tooltip
                if (tooltip.opacity === 0) {
                        tooltipEl.style.opacity = 0;
                        return;
                }

                // Set caret Position
                tooltipEl.classList.remove('above', 'below', 'no-transform');
                if (tooltip.yAlign) {
                        tooltipEl.classList.add(tooltip.yAlign);
                } else {
                        tooltipEl.classList.add('no-transform');
                }

                function getBody(bodyItem) {
                        return bodyItem.lines;
                }

                // Set Text
                if (tooltip.body) {
                        var titleLines = tooltip.title || [];
                        var bodyLines = tooltip.body.map(getBody);

                        var innerHtml = '<thead>';

                        titleLines.forEach(function(title) {
                                innerHtml += '<tr><th>' + title + '</th></tr>';
                        });
                        innerHtml += '</thead><tbody>';

                        bodyLines.forEach(function(body, i) {
                                var colors = tooltip.labelColors[i];
                                var style = 'background:' + colors.backgroundColor;
                                style += '; border-color:' + colors.borderColor;
                                style += '; border-width: 2px';
                                var span = '<span class="chartjs-tooltip-key" style="' + style + '"></span>';
                                innerHtml += '<tr><td>' + span + body + '</td></tr>';
                        });
                        innerHtml += '</tbody>';

                        var tableRoot = tooltipEl.querySelector('table');
                        tableRoot.innerHTML = innerHtml;
                }

                var positionY = this._chart.canvas.offsetTop;
                var positionX = this._chart.canvas.offsetLeft;

                // Display, position, and set styles for font
                tooltipEl.style.opacity = 1;
                tooltipEl.style.left = positionX + tooltip.caretX + 'px';
                tooltipEl.style.top = positionY + tooltip.caretY + 'px';
                tooltipEl.style.fontFamily = tooltip._fontFamily;
                tooltipEl.style.fontSize = tooltip.fontSize;
                tooltipEl.style.fontStyle = tooltip._fontStyle;
                tooltipEl.style.padding = tooltip.yPadding + 'px ' + tooltip.xPadding + 'px';
        };

        var config = {
                type: 'pie',
                data: {
                        datasets: [{
                                data: [%s, %s, %s],
                                backgroundColor: [
                                        window.chartColors.red,
                                        window.chartColors.orange,
                                        window.chartColors.yellow,
                                        window.chartColors.green,
                                        window.chartColors.blue,
                                ],
                        }],
                        labels: [
                                "Tweet",
                                "Retweet",
                                "Reply",
                        ]
                },
                options: {
                        responsive: true,
                        legend: {
                                display: true
                        },
                        tooltips: {
                                enabled: false,
                        }
                }
        };

        window.onload = function() {
                        var ctx = document.getElementById("chart-area").getContext("2d");
                        window.myPie = new Chart(ctx, config);
        };
	</script>
	</head>
	<body>
	<div dir="auto">
	<br><br><br><br>
	<h1> We've found some interesting data for @%s... </h1>
	<p> We analyzed %s tweets, from which %s were retweets, and %s were replies. 
        <center>
	<div id="canvas-holder" style="width: 300px;">
		<canvas id="chart-area" width="300" height="300"></canvas>
		<div id="chartjs-tooltip">
			<table></table>
		</div>
	</div>
        </center>
	<p> %s
	<p> %s
	<p> %s
	<p> %s
	<p><br> %s is the day of the week you are most active. <br>On any given day, %s (%s time) is your favorite time to tweet :) </p>
	</div>
	</body>
	</html>
	""" % (tweet_count,retweet_count,reply_count,screenName,total_count,retweet_count,reply_count, top5Retweeted, top5Replied, mentions, hashtags, popularDay, popularHour, tzinfo_name)

#	html = html.format(screenName=screenName, total_tweets=total_count, retweet_count=retweet_count, reply_count=reply_count, top5Retweeted=top5Retweeted, top5Replied=top5Replied, mentions=mentions, hashtags=hashtags, popularDay=popularDay, tzinfo_name=tzinfo_name, popularHour=popularHour)
	print html

	debugFile = open('/www/codewithaheart.com/docs/twitterApp/debug/debug.txt', 'a') 
	debugFile.write(html + '\n\n\n\n\n')
