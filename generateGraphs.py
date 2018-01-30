#!/apps/python/2.7.13/bin/python

##==============================================================================
# file:                 generateGraphs.py 
# date:                 Thu Jan 25 00:31:03 GMT 2018
# author(s):            Thalita Coleman  <thalitaneu@gmail.com>
# abstract:             Call functions that contains user's processed data and
#			generates javascript graphs.
#------------------------------------------------------------------------------
# requirements: python 2.7, generateStats.py 
#------------------------------------------------------------------------------
##==============================================================================

import os

from generateStats import *


# call functions that contains user's processed data
def generateGraphs(screenName, jsonFileName, tzinfo_name):
	total_count, tweet_count, retweet_count, reply_count, list_usersRetweeted, list_usersReplied, list_usersMentioned, list_hashtags, list_times = lists(jsonFileName, tzinfo_name) 

	top5Retweeted, mostCommonRetweeted, mostCommonRetweetedValue = topFiveRetweeted(list_usersRetweeted)	
	top5Replied, mostCommonReplied, mostCommonRepliedValue = topFiveReplied(list_usersReplied, screenName)	

	mentions, mostCommonMentioned, mostCommonMentionedValue  = topFiveMentioned(list_usersMentioned)

	hashtags, mostCommonHashtag, mostCommonHashtagValue = topFiveHashtags(list_hashtags)

	popularDay, dateFirstTweet = getPopularWeekdays(list_times)

	sundayMorning, sundayAfternoon, sundayEvening, sundayNight, mondayMorning, mondayAfternoon, mondayEvening, mondayNight, tuesdayMorning, tuesdayAfternoon, tuesdayEvening, tuesdayNight, wednesdayMorning, wednesdayAfternoon, wednesdayEvening, wednesdayNight, thursdayMorning, thursdayAfternoon, thursdayEvening, thursdayNight, fridayMorning, fridayAfternoon, fridayEvening, fridayNight, saturdayMorning, saturdayAfternoon, saturdayEvening, saturdayNight, popularHour = getPopularHours(list_times)

	sundayMorningNormalized, sundayAfternoonNormalized, sundayEveningNormalized, sundayNightNormalized, mondayMorningNormalized, mondayAfternoonNormalized, mondayEveningNormalized, mondayNightNormalized, tuesdayMorningNormalized, tuesdayAfternoonNormalized, tuesdayEveningNormalized, tuesdayNightNormalized, wednesdayMorningNormalized, wednesdayAfternoonNormalized, wednesdayEveningNormalized, wednesdayNightNormalized, thursdayMorningNormalized, thursdayAfternoonNormalized, thursdayEveningNormalized, thursdayNightNormalized, fridayMorningNormalized, fridayAfternoonNormalized, fridayEveningNormalized, fridayNightNormalized, saturdayMorningNormalized, saturdayAfternoonNormalized, saturdayEveningNormalized, saturdayNightNormalized, popularHour = getPopularHoursNormalized(list_times)

	#======================================================================	
 	#   Python HereDoc for PieChart
	#======================================================================	
	html = """
	<!DOCTYPE html>
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="css/style.css" />
		<link rel="stylesheet" type="text/css" href="css/piechart.css">
		<script src="js/chartjs/Chart.bundle.js"></script>
		<script src="js/chartjs/utils.js"></script>
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
                                        window.chartColors.green,
                                        window.chartColors.blue,
                                        window.chartColors.orange,
                                        window.chartColors.yellow,
                                        window.chartColors.purple, 
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
			maintainAspectRatio: false,
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
                backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
                //backgroundColor: color(window.chartColors.grey).alpha(0.5).rgbString(),
                //backgroundColor: 000000,
                //borderColor: window.chartColors.blue,
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
		    maintainAspectRatio: false,
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
                			fontSize: 14
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
                backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
                //borderColor: window.chartColors.red,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s ]
            }]

        };

    </script>

        <!-- ================================ -->
        <!--     End Bar Chart2 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonReplied[0], mostCommonReplied[1], mostCommonReplied[2], mostCommonReplied[3], mostCommonReplied[4], mostCommonRepliedValue[0], mostCommonRepliedValue[1], mostCommonRepliedValue[2], mostCommonRepliedValue[3], mostCommonRepliedValue[4])



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
                backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
                //borderColor: window.chartColors.red,
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
                backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
                //borderColor: window.chartColors.red,
                borderWidth: 1,
                data: [%s, %s, %s, %s, %s]
            }]

        };

    </script>


        <!-- ================================ -->
        <!--     End Bar Chart4 JavaScript    -->
        <!-- ================================ -->
""" % (mostCommonHashtag[0], mostCommonHashtag[1], mostCommonHashtag[2], mostCommonHashtag[3], mostCommonHashtag[4], mostCommonHashtag[0], mostCommonHashtag[1], mostCommonHashtag[2], mostCommonHashtag[3], mostCommonHashtag[4], mostCommonHashtagValue[0], mostCommonHashtagValue[1], mostCommonHashtagValue[2], mostCommonHashtagValue[3], mostCommonHashtagValue[4])


	#======================================================================	
	# Python Heredoc for Stacked Bar Chart - Hours
	#======================================================================	
	html += """
        <!-- ======================================= -->
        <!--   Begin Stacked Bar Chart JavaScript    -->
        <!-- ======================================= -->
	<script>
        var barChartData = {
            labels: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            datasets: [{
                label: 'Morning (6-11 AM)',
                backgroundColor: window.chartColors.orange,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Afternoon (12-5 PM)',
                backgroundColor: window.chartColors.blue,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Evening (6-11 PM)',
                backgroundColor: window.chartColors.green,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Night (Midnight-5 AM)',
                backgroundColor: window.chartColors.purple,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }]

        };

	function drawStackedChart() {
            var ctx = document.getElementById("stackedBarChart").getContext("2d");
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    title:{
                        display:true,
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false
                    },
                    responsive: true,
		    maintainAspectRatio: false,
                    scales: {
                        xAxes: [{
                            stacked: true,
			    ticks: {
             			   beginAtZero: true
            			   }
                        }],
                        yAxes: [{
                            stacked: true,
			    ticks: {
             			   beginAtZero: true
            			   }
                        }]
                    }
                }
            });
        };

	</script>






        <!-- ======================================= -->
        <!--     End Stacked Bar Chart JavaScript    -->
        <!-- ======================================= -->
""" % (sundayMorning, mondayMorning, tuesdayMorning, wednesdayMorning, thursdayMorning, fridayMorning, saturdayMorning, sundayAfternoon, mondayAfternoon, tuesdayAfternoon, wednesdayAfternoon, thursdayAfternoon, fridayAfternoon, saturdayAfternoon, sundayEvening, mondayEvening, tuesdayEvening, wednesdayEvening, thursdayEvening, fridayEvening, saturdayEvening, sundayNight, mondayNight, tuesdayNight, wednesdayNight, thursdayNight, fridayNight, saturdayNight)



	#======================================================================	
	# Python Heredoc for Stacked Bar Chart 2 - Normalized Hours
	#======================================================================	
	html += """
        <!-- ================================================ -->
        <!--   Begin Stacked Bar Chart Normalized JavaScript  -->
        <!-- ================================================ -->
	<script>
        var barChartDataNormalized = {
            labels: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            datasets: [{
                label: 'Morning (6-11 AM)',
                backgroundColor: window.chartColors.orange,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Afternoon (12-5 PM)',
                backgroundColor: window.chartColors.blue,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Evening (6-11 PM)',
                backgroundColor: window.chartColors.green,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }, {
                label: 'Night (Midnight-5 AM)',
                backgroundColor: window.chartColors.purple,
                stack: 'Stack 0',
                data: [%s, %s, %s, %s, %s, %s, %s]
            }]

        };

	function drawStackedChartNormalized() {
            var ctx = document.getElementById("stackedBarChartNormalized").getContext("2d");
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartDataNormalized,
                options: {
                    title:{
                        display:true,
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false
                    },
                    responsive: true,
		    maintainAspectRatio: false,
                    scales: {
                        xAxes: [{
                            stacked: true,
			    ticks: {
             			   beginAtZero: true
            			   }
                        }],
                        yAxes: [{
                            stacked: true,
			    ticks: {
             			   beginAtZero: true
            			   }
                        }]
                    }
                }
            });
        };

	</script>






        <!-- ================================================== -->
        <!--     End Stacked Bar Chart Normalized JavaScript    -->
        <!-- ================================================== -->
""" % (sundayMorningNormalized, sundayAfternoonNormalized, sundayEveningNormalized, sundayNightNormalized, mondayMorningNormalized, mondayAfternoonNormalized, mondayEveningNormalized, mondayNightNormalized, tuesdayMorningNormalized, tuesdayAfternoonNormalized, tuesdayEveningNormalized, tuesdayNightNormalized, wednesdayMorningNormalized, wednesdayAfternoonNormalized, wednesdayEveningNormalized, wednesdayNightNormalized, thursdayMorningNormalized, thursdayAfternoonNormalized, thursdayEveningNormalized, thursdayNightNormalized, fridayMorningNormalized, fridayAfternoonNormalized, fridayEveningNormalized, fridayNightNormalized, saturdayMorningNormalized, saturdayAfternoonNormalized, saturdayEveningNormalized, saturdayNightNormalized)


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
		drawStackedChart();
		drawStackedChartNormalized();
	}
    </script>


	</head>
	<body>
	<div dir="auto">
	<br>
	<h1> We've found some interesting data for @%s... </h1>
	<h2> We analyzed %s tweets going back to %s. <br> %s were retweets and %s were replies. </h2> 
        <center>
	   <div id="canvas-holder" style="position: relative; height:20vh; width: 40vw; border:0px solid black">
		<canvas id="chart-area" width="200" height="200"></canvas>
		<div id="chartjs-tooltip">
			<table></table>
		</div>
	   </div>
        </center>
	<p> %s
	<!-- BarChart 1 -->
        <center>
	   <div style="position: relative; height:20vh; width: 40vw; border:0px solid black"> 
              <canvas id="barChart1Canvas"></canvas>
           </div>
        </center>
	<p> %s
	<!-- BarChart 2 -->
        <center>
	   <div style="position: relative; height:20vh; width: 40vw; border:0px solid black"> 
              <canvas id="barChart2Canvas"></canvas>
           </div>
        </center>
	<p> %s
	<!-- BarChart 3 -->
        <center>
	   <div style="position: relative; height:20vh; width: 40vw; border:0px solid black"> 
              <canvas id="barChart3Canvas"></canvas>
           </div>
        </center>
	<p> %s
	<!-- BarChart 4 -->
        <center>
	   <div style="position: relative; height:20vh; width: 40vw; border:0px solid black"> 
              <canvas id="barChart4Canvas"></canvas>
           </div>
        </center>
	<p> <center><div class="section-header" style="position: relative; height:8vh; width: 60vw; border: 0px solid black"><br> %s is the day of the week you are most active. On any given day, %s (%s time) is your favorite time to tweet :) </div>
	</center>
	<!-- Stacked Bar Chart -->
        <p><center>
	   <div style="position: relative; height:25vh; width: 70vw; border: 0px solid black"> 
              <canvas id="stackedBarChart"></canvas>
           </div>
        </center>

	<p> <center><div class="section-header" style="position: relative; height:3vh; width: 60vw; border: 0px solid black"><br> Here is your normalized data... </div>
	</center>
	<!-- Stacked Bar Chart Normalized -->
        <p><center>
	   <div style="position: relative; height:25vh; width: 70vw; border: 0px solid black"> 
              <canvas id="stackedBarChartNormalized"></canvas>
           </div>
        </center>
	<pre>


	</pre>
	</div>
	</body>
	</html>
	""" % (screenName,total_count, dateFirstTweet, retweet_count,reply_count, top5Retweeted, top5Replied, mentions, hashtags, popularDay, popularHour, tzinfo_name)

	print html
	
	debugFile = open('/www/codewithaheart/docs/twitterApp/debug/' + screenName + '.txt', 'a') 
	#debugFile = open('/www/default/docs/twitterApp/debug/' + screenName + '.txt', 'a') 
	debugFile.write(html + '\n\n\n\n\n')

