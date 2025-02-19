import requests

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
        print("Temperature: " + str(temp)) #will be celsius
        #print(data)
        
        
else:
    print("Error:", response.status_code, response.text)