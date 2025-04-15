"""This document collects all APIs and organizes the data needed to be displayed"""
import requests
from datetime import datetime


"""Weather Data"""

#location = Oakland University
lat = 42.6744918823
lon = -83.2205200195
params = { "lat" : lat, "lon" : lon }
api_url = 'https://api.api-ninjas.com/v1/weather'
headers = {'X-Api-Key': 'XbIJXr6qNj3Cl3sZw7v5oQ==QephRx1PSyj683q8'}
response = requests.get(api_url, headers=headers, params = params)
if response.status_code == requests.codes.ok:
        data = response.json()  # Parse JSON response
        temp = data['temp']  # Extract the temp text
        clouds = data['cloud_pct'] #cloud coverage 
        wind_mph = data['wind_speed'] #wind speed
        humid = data['humidity'] #humididty
        low_temp = data['min_temp'] # low temp
        high_temp = data['max_temp'] #high temp 
        sunrise = data['sunrise'] #sunrise
        sunset = data['sunset'] #sunset
else:
    temp = "unavailable"    
    clouds = "unavailable"
    wind_mph = "unavailable"
    humid = "unavailable"
    low_temp = "unavailable"
    high_temp= "unavailable"
    sunrise = "unavailable"
    sunset = "unavailable"

sunsettime = datetime.fromtimestamp(sunset).strftime('%H:%M')
sunrisetime = datetime.fromtimestamp(sunrise).strftime('%H:%M')

weather_color = "light blue" #defines basic widget color
#adjusts color to match temp
if int(temp) > -20:
    weather_color = "blue"
if int(temp) > 0:
    weather_color = "yellow"
if int(temp) > 10:
    weather_color = "orange"
if int(temp) > 20:
    weather_color = "red"
if int(temp) > 34:
    weather_color = "dark red"

#symbols for weather
weather_symbol = "./images/sunny.webp" 
if int(clouds) > 50:
     weather_symbol = "./images/partlycloud.png"
if int(clouds) == 100:
     weather_symbol = "./images/Cloud_Icon.png"

"""Quotes"""
api_url = 'https://api.api-ninjas.com/v1/quotes'
headers = {'X-Api-Key': 'XbIJXr6qNj3Cl3sZw7v5oQ==QephRx1PSyj683q8'}

response = requests.get(api_url, headers=headers)

if response.status_code == requests.codes.ok:
        data = response.json()  # Parse JSON response
        saying = data[0]['quote']  # Extract the quote text
        author = data[0]['author'] #extract author
        quote = saying + "\n- " + author
else:
    quote = "Quote Unavailable"


"""News API"""
api_url = 'https://newsdata.io/api/1/latest?apikey=pub_7498696714b447bc7f0e004260a0cce46ee01&q=detroit&language=en&size=6'

response = requests.get(api_url)
news_list = "\n" * 2
if response.status_code == requests.codes.ok:
        data = response.json()  # Parse JSON response
        for article in data["results"]:
              title = article.get("title", "None")
              summary = article.get("description", "None")
              news = "Headline: "+ str(title) + ("\n" * 1) +"Description: " + str(summary) + ("\n" * 2)
              if len(str(summary)) > 500:
                    news = "Headline: "+ str(title) + ("\n" * 1)
              news_list += news
        
else:
    print("Error:", response.status_code, response.text)

news_pic = "./news_icon.png" #picture for news button
#https://game-icons.net/icons/ffffff/transparent/1x1/delapouite/newspaper.png


