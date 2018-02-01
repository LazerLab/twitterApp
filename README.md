# twitterApp


## DESCRIPTION:
The Twitter App retrieves a user's tweets via the Twitter API and returns stats on their Twitter activities. It stores the user's API keys for future use. 

## TECHNOLOGIES USED:
- Apache Server (version 2.4.29)
- Python 2.7 with the following modules installed: requests, requests_oauthlib, pytz
- Twitter API

## GENERAL OVERVIEW:
- redirects user to Twitter authorization page and collects keys to access user data
- retrieves and analyses user data
- displays:	total number of tweets collected
		number of tweets, retweets, replies
		10 people the user retweets the most
		10 people the user replies to the most
		5 people the user mentions the most
		10 hashtags the user uses the most
		time of day and day of week the user is most active
- saves .json file with tweets and .txt file with api keys for future use

## PROGRAM FLOW:

```
(01) Homepage 
	user clicks 
	"login with Twitter"
	[index.html]
	|
	|
(02)	user redirected to 
	Twitter login/authorize app page.
	If user is already logged in, 
	he is directed to authorization page
	[twitterApp.cgi]
	|
	|
(03)	following twitter login/authorization
	user is redirected to TwitterApp
	|
	|
(04)	TwitterApp collects and analyses
	user tweets.
	[twitterApp.cgi, collectTweets.py, generateStats.py]
        |
        |
	User has tweets?
			|
	________________|_______________
	|				|	
	|				|	
	YES				NO
(05)	Results page displayed		No Tweets page displayed	(06)
	[twitterApp.cgi,		[twitterApp.cgi,
	collectTweets.py, 		noTweets.html]
	generateGraphs.py]
```


## APP SOURCE STRUCTURE:

```
/www/default/docs/twitterApp/	index.html		[Initial Page]
				twitterApp.cgi		[Manage oauth flow and calls functions that analyze and display data]
				collectTweets.py	[Retrieves tweets data from Twitter API, writes data to file]
				generateStats.py	[Analyses twitter data, returns raw data and some HTML]
				generateGraphs.py	[Generate graphs, returns HTML for results page, saves HTML to debug file]
				noTweets.html		[Result page if the user has 0 tweets]

/www/default/docs/twitterApp/css/indexStyle.css		[External style sheet for index.html and noTweets.html]
				piechart.css		[External style sheet for javascript charts]
				style.css		[External style sheet for results page]

/www/default/docs/twitterApp/js/chartjs/Chart.bundle.js [js for charts]
					utils.js	[js for charts]

/www/default/docs/twitterApp/json [json files will be stored here] **> This directory has to be created before running app on a new server. It has to be owned by the web server.

/www/default/docs/twitterApp/kdata [Twitter API keys will be stored here] **> This directory has to be created before running app on a new server. It has to be owned by the web server.

/www/default/docs/twitterApp/debug [debug files will be stored here] **> This directory has to be created before running app on a new server. It has to be owned by the web server.
```
				 
## TWITTER API:
The Twitter API is used to collect user twitter keys and tweets. To use the Twitter API the app must first be registered with Twitter. Once the app is registered, Twitter will provide the Consumer Keys and Consumer Secret for the application. The keys used in developing this app are hardcoded in the file twitterApp.cgi. 

## VARIABLES:
The following variables are hardcoded and in a second version should be placed in a config file:
```
File: twitterApp.cgi	Variables: hostname
				   pathToAppDir
				   client_key
				   client_secret
				   callback_uri
```

Variables that might need to be reviewed if the directory structure changes:
```
File: twitterApp.cgi	Variables: keyToFile
				   jsonFileName
File: generateGraphs.py Variables: debugFile
```

Variables that might need to be reviewed if the Twitter API updates its endpoints:		
```
File: twitterApp.cgi	Variables: request_token_url
				   authorization_url
				   access_token_url 
				   settings_url
File: collectTweets.py	Variables: tweets_url
``` 

## LANGUAGE DIRECTION:
The app is configured to display text in both right-to-left and left-to-right directions, enabling it to display text in languages such as Hebrew and Arabic. 
In css/style.css:
> dir: "auto";

Character encoding is 'Unicode', enabling it to handle multiple languages. 
In generateGraphs.py:
> \<meta charset="UTF-8"\>

