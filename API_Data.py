"""This document collects all APIs and organizes the data needed to be displayed"""
import requests



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
else:
    temp = "unavailable"

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
