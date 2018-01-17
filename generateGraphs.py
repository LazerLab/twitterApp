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

from topRetweets import *


def generateGraphs(screenName, jsonFileName, tzinfo_name):
	# analysing user's data
	total_count, tweet_count, retweet_count, reply_count, list_usersRetweeted, list_usersReplied, list_usersMentioned, list_hashtags, list_times = lists(jsonFileName, tzinfo_name) 

	top5Retweeted, mostCommonRetweeted, mostCommonRetweetedValue = topFiveRetweeted(list_usersRetweeted)	

	#print list_usersRetweeted
	#print top5Retweeted
	#print mostCommonRetweeted
	#print mostCommonRetweetedValue

	top5Replied, mostCommonReplied, mostCommonRepliedValue = topFiveReplied(list_usersReplied)	
	#print list_usersReplied
	#print top5Replied

	mentions, mostCommonMentioned, mostCommonMentionedValue  = topFiveMentioned(list_usersMentioned)
	#print mentions

	hashtags, mostCommonHashtag, mostCommonHashtagValue = topFiveHashtags(list_hashtags)
	#print hashtags

	popularDay = getPopularWeekdays(list_times)
	#print popularDay

	popularHour = getPopularHours(list_times)
	#print popularHour 



	#======================================================================	
 	#   Python HereDoc for PieChart
	#======================================================================	
	html = """
	<!DOCTYPE html>
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="/twitterApp/style.css" />
		<link rel="stylesheet" type="text/css" href="/css/piechart.css">
		<script src="/js/chartjs/Chart.bundle.js"></script>
		<script src="/js/chartjs/utils.js"></script>
	<meta charset="utf-8">

        <!-- ================================ -->
        <!--     Begin Pie Chart JavaScript   -->
        <!-- ================================ -->
	<script type="text/javascript">
        var config = {
                type: 'pie',
                data: {
                        datasets: [{
                                data: [%s, %s, %s],
                                backgroundColor: [
                                        window.chartColors.red, 
                                        window.chartColors.blue,
                                        window.chartColors.yellow,
                                        window.chartColors.orange,
                                        window.chartColors.green,
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
                                enabled: true,
                        }
                }
        };

        //window.onload = function() {
	function drawPieChart() {
                        var ctx = document.getElementById("chart-area").getContext("2d");
                        window.myPie = new Chart(ctx, config);
        };
	</script>

        <!-- ================================ -->
        <!--     End Pie Chart JavaScript     -->
        <!-- ================================ -->

	""" % (tweet_count,retweet_count,reply_count)




	#======================================================================	
 	#   Python HereDoc for BarChart1 - Retweets
	#======================================================================	
	html += """
        <!-- ================================ -->
        <!--   Begin Bar Chart1 JavaScript    -->
        <!-- ================================ -->
    <script type="text/javascript">
        var twitterHandles = ["%s", "%s", "%s", "%s", "%s"];
        var color = Chart.helpers.color;
        var horizontalBarChart1Data = {
            labels: ["%s", "%s", "%s", "%s", "%s"],
            datasets: [{
                label: 'retweets',
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                //backgroundColor: color(window.chartColors.grey).alpha(0.5).rgbString(),
                //backgroundColor: 000000,
                borderColor: window.chartColors.red,
                //borderColor: window.chartColors.blue,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s]
            }]

        };

	function drawBarChart() {
            var ctx = document.getElementById(arguments[0]).getContext("2d");
            window.myHorizontalBar = new Chart(ctx, {
                type: 'horizontalBar',
                data: arguments[1],
                options: {
                    // Elements options apply to all of the options unless overridden in a dataset 
                    // In this case, we are setting the border of each horizontal bar to be 2px wide
                    elements: {
                        rectangle: {
                            borderWidth: 2,
                        }       
                    },      
                    responsive: true,
                    legend: {
                        display: false,
                        position: 'right',
                    },      
                    title: {
                        display: true,
                        text: ''
                    },
		    scales: {
     			   xAxes: [{
        		    ticks: {
				 beginAtZero: true,
				 suggestedMin: 0,
               			 min: 0,
				 // limit x-axis steps to whole numbers
				 callback: function(value, index, values) {
                        		if(value %% 1 === 0) {
						return value;
					}
					else {
						return ' ';
					}
                    		 }
            	}
        }],
			yAxes: [{
				ticks: {
                			fontSize: 18
            				}
	}]
    }       
                }       
            });     

        };      

        var colorNames = Object.keys(window.chartColors);
    </script>

        <!-- ================================ -->
        <!--     End Bar Chart1 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonRetweeted[0], mostCommonRetweeted[1], mostCommonRetweeted[2], mostCommonRetweeted[3], mostCommonRetweeted[4], mostCommonRetweeted[0], mostCommonRetweeted[1], mostCommonRetweeted[2], mostCommonRetweeted[3], mostCommonRetweeted[4], mostCommonRetweetedValue[0], mostCommonRetweetedValue[1], mostCommonRetweetedValue[2], mostCommonRetweetedValue[3], mostCommonRetweetedValue[4])





	#======================================================================	
	# Python Heredoc for BarChart 2 - Replies
	#======================================================================	
	html += """
        <!-- ================================ -->
        <!--   Begin Bar Chart2 JavaScript    -->
        <!-- ================================ -->
    <script type="text/javascript">
        var twitterHandles2 = ["%s", "%s", "%s", "%s", "%s"];
        var color = Chart.helpers.color;
        var horizontalBarChart2Data = {
            labels: ["%s", "%s", "%s", "%s", "%s"],
            datasets: [{
                label: 'replies',
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.red,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s ]
            }]

        };

    </script>

        <!-- ================================ -->
        <!--     End Bar Chart2 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonRepliedValue[0], mostCommonRepliedValue[1], mostCommonRepliedValue[2], mostCommonRepliedValue[3], mostCommonRepliedValue[4])

#("1", "2", "3", "4", "5", "1", "2", "3", "4", "5", 1,2,3,4,5)
#(mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonRepliedValue[0], mostCommonRepliedValue[1], mostCommonRepliedValue[2], mostCommonRepliedValue[3], mostCommonRepliedValue[4]) 






	#======================================================================	
	# Python Heredoc for BarChart 3 - Mentions
	#======================================================================	
	html += """
        <!-- ================================ -->
        <!--   Begin Bar Chart3 JavaScript    -->
        <!-- ================================ -->
    <script type="text/javascript">
        var twitterHandles3 = ["%s","%s","%s","%s","%s"];
        var color = Chart.helpers.color;
        var horizontalBarChart3Data = {
            labels: ["%s","%s","%s","%s","%s"], 
            datasets: [{
                label: 'mentions',
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.red,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s] 
            }]

        };

    </script>


        <!-- ================================ -->
        <!--     End Bar Chart3 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonMentioned[0], mostCommonMentioned[1], mostCommonMentioned[2], mostCommonMentioned[3], mostCommonMentioned[4], mostCommonMentioned[0], mostCommonMentioned[1], mostCommonMentioned[2], mostCommonMentioned[3], mostCommonMentioned[4], mostCommonMentionedValue[0], mostCommonMentionedValue[1], mostCommonMentionedValue[2], mostCommonMentionedValue[3], mostCommonMentionedValue[4])



	#======================================================================	
	# Python Heredoc for BarChart 4 - Hashtags
	#======================================================================	
	html += """
        <!-- ================================ -->
        <!--   Begin Bar Chart4 JavaScript    -->
        <!-- ================================ -->
    <script type="text/javascript">
        var twitterHandles4 = ["%s","%s","%s","%s","%s"];
        var color = Chart.helpers.color;
        var horizontalBarChart4Data = {
            labels: ["%s", "%s", "%s", "%s", "%s"],
            datasets: [{
                label: 'hashtags',
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.red,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s]
            }]

        };

    </script>


        <!-- ================================ -->
        <!--     End Bar Chart4 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonHashtag[0], mostCommonHashtag[1], mostCommonHashtag[2], mostCommonHashtag[3], mostCommonHashtag[4], mostCommonHashtag[0], mostCommonHashtag[1], mostCommonHashtag[2], mostCommonHashtag[3], mostCommonHashtag[4], mostCommonHashtagValue[0], mostCommonHashtagValue[1], mostCommonHashtagValue[2], mostCommonHashtagValue[3], mostCommonHashtagValue[4])

	html += """

        <!-- ==================================== -->
        <!--     Draw all charts on page load     -->
        <!-- ==================================== -->
    <script type="text/javascript">
        window.onload = function() {
		drawPieChart();
		drawBarChart("barChart1Canvas",horizontalBarChart1Data);
		drawBarChart("barChart2Canvas",horizontalBarChart2Data);
		drawBarChart("barChart3Canvas",horizontalBarChart3Data);
		drawBarChart("barChart4Canvas",horizontalBarChart4Data);
	}
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
        <center>
           <div id="container" style="width: 75%%;">
              <canvas id="barChart1Canvas"></canvas>
           </div>
        </center>
	<p> %s
        <center>
           <div id="container" style="width: 75%%;">
              <canvas id="barChart2Canvas"></canvas>
           </div>
        </center>
	<p> %s
        <center>
           <div id="container" style="width: 75%%;">
              <canvas id="barChart3Canvas"></canvas>
           </div>
        </center>
	<p> %s
        <center>
           <div id="container" style="width: 75%%;">
              <canvas id="barChart4Canvas"></canvas>
           </div>
        </center>
	<p><br> %s is the day of the week you are most active. <br>On any given day, %s (%s time) is your favorite time to tweet :) </p>
	<pre>


	</pre>
	</div>
	</body>
	</html>
	""" % (screenName,total_count,retweet_count,reply_count, top5Retweeted, top5Replied, mentions, hashtags, popularDay, popularHour, tzinfo_name)

#	html = html.format(screenName=screenName, total_tweets=total_count, retweet_count=retweet_count, reply_count=reply_count, top5Retweeted=top5Retweeted, top5Replied=top5Replied, mentions=mentions, hashtags=hashtags, popularDay=popularDay, tzinfo_name=tzinfo_name, popularHour=popularHour)
	print html

	debugFile = open('/www/codewithaheart.com/docs/twitterApp/debug/debug.txt', 'a') 
	debugFile.write(html + '\n\n\n\n\n')

