# Imports

import json
import requests
import smtplib
import imghdr
from datetime import datetime
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


# Setting up the Magicseaweed API
response = requests.get("http://magicseaweed.com/api/28c500e859576a4f8bbcbe09c83e2492/forecast/?spot_id=52")
data = json.loads(response.text)


# Function for going through forecast
def findGoodSwell():



	forecast = []
	dateList = []
	starList = []
	swellList = []
	windDirectionList = []
	windSpeedList = []

	for i in range(0, 40):

		# MSW Star Rating
		star = data[i]['solidRating']

		# Swell data
		minSwell = data[i]['swell']['minBreakingHeight']
		maxSwell = data[i]['swell']['maxBreakingHeight']
		swell = str(minSwell) + '-' + str(maxSwell) + 'ft'

		# Wind data
		windDirection = data[i]['wind']['compassDirection']
		windDegrees = data[i]['wind']['direction']
		windSpeed = data[i]['wind']['speed']

		# Date and Time data
		unixDate = data[i]['localTimestamp']
		current = data[0]['localTimestamp']
		forecastDay = datetime.utcfromtimestamp(current).strftime('%A')
		date = datetime.utcfromtimestamp(unixDate).strftime('%A %d/%m %H:00')
		day = datetime.utcfromtimestamp(unixDate).strftime('%A')
		time = datetime.utcfromtimestamp(unixDate).strftime('%H:00')

		# Conditions for sending the email
		if(star > 0):
			if(str(time) != '00:00' and str(time) != '03:00' and str(time) != '06:00'):	
				if(windDegrees > 101):
					print(day + ' at ' + time)
					forecast.append(day + ' at ' + time)
					dateList.append(day + ' at ' + time)
					print(str(star) + ' stars')
					forecast.append(str(star) + ' stars')
					starList.append(str(star) + ' stars')
					print(swell)
					forecast.append(swell)
					swellList.append(swell)
					print(windDirection)
					forecast.append(str(windDirection))
					windDirectionList.append(str(windDirection))
					print(windDegrees)
					forecast.append(str(windDegrees))
					print(str(windSpeed) + ' mph')
					forecast.append(str(windSpeed) + ' mph')
					windSpeedList.append(str(windSpeed) + ' mph')
					print(" ")

	# Returning the data 
	return forecast, dateList, starList, swellList, windDirectionList, windSpeedList, forecastDay


# Function to send the email
def sendEmail():

	# Email variables
	EMAIL_ADDRESS = 'cianomahony22@gmail.com'
	EMAIL_PASSWORD = 'qhvmdgbzospefrtr'
	contacts = ['ciaantonnta@gmail.com']
	emailForecast = []
	emailForecast, dateList, starList, swellList, windDirectionList, windSpeedList, forecastDay  = findGoodSwell();
	currentDay = datetime.today().strftime('%A')

	# Message properties
	msg = MIMEMultipart()
	msg['Subject'] = 'Surf Forecast'
	msg['From'] = EMAIL_ADDRESS
	msg['To'] = 'ciaantonnta@gmail.com'


	# HTML String for displaying the data
	forecastString = """<!DOCTYPE html>
							<html>
							<body>
							<head>
							<style>
							* {
							font-family: sans-serif;
							}
							.content-table {
							border-collapse: collapse;
							margin: 25px 0;
							font-size: 0.9em;
							border-radius: 5px 5px 0 0;
							min-width: 650px;
							overflow: hidden;
							}
							.content-table thead tr {
							background-color: #009879;
							color: #fff;
							text-align: left;
							font-weight: bold;
							}
							.content-table th, .content-table td {
			 				padding: 12px 15px;
			 				}
							.content-table tbody tr {
							border-bottom: 1px solid #000;
							}
							.content-table tbody tr:nth-of-type(even) {
							background-color: #f3f3f3;
							} 
							.content-table tbody tr:last-of-type {
							border-bottom: 2px solid #009879;
							}
							.webcam-image {
							height: 500px;
							}
							</style>
							</head> """
	print(currentDay)
	print(forecastDay)
	if(currentDay == forecastDay):
		forecastString = forecastString + """<h1 style="color:#009879;text-align:center;">Waves Are Good Today!</h1>
											  <img class="webcam-image" src="cid:image1"/>
											  <table class="content-table">
											  	<thead>
												<tr>
													<th>Date</th>
													<th>Stars</th>
													<th>Swell</th>
													<th>Wind</th>
													<th>Wind Speed</th>
												</tr>
												</thead>"""
	else:
		forecastString = forecastString + """ <h1 style="color:SlateGray;text-align:center;">Surf Forecast</h1>
											<table class="content-table">
											  	<thead>
												<tr>
													<th>Date</th>
													<th>Stars</th>
													<th>Swell</th>
													<th>Wind</th>
													<th>Wind Speed</th>
												</tr>
												</thead>"""

	# Loop for adding multiple forecasts
	for i in range(0, len(dateList)):
		
		forecastString = forecastString + """
				<tbody>
					<tr>
						<td>""" + dateList[i] + """</td>
						<td>""" + starList[i] + """</td>
						<td>""" + swellList[i] + """</td>
						<td>""" + windDirectionList[i] + """</td>
						<td>""" + windSpeedList[i] + """</td>
					</tr>
				"""

	
	forecastString = forecastString + """</tbody></table></body></html>"""
	print(forecastString)


	# Scraping the webcam image
	img_data = open('inchydoney.png', 'rb').read()
	text = MIMEText(forecastString, 'html')
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename('inchydoney.png'))
	
	image.add_header('Content-ID', '<image1>')

	msg.attach(image)

	# Sending the email
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		smtp.send_message(msg)




# Function to scrape the webcam image
def getWebcamImage():

	response = requests.get('http://92.60.192.245/record/current.jpg?forceRefresh=1598698711656')
	file = open('inchydoney.png', 'wb')
	file.write(response.content)
	file.close()


# Calling the functions
getWebcamImage();
findGoodSwell();
print(findGoodSwell());
sendEmail();















