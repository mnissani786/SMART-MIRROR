#prints random quote
"""
import requests
import json

api_url = 'https://api.api-ninjas.com/v1/quotes'
headers = {'X-Api-Key': 'XbIJXr6qNj3Cl3sZw7v5oQ==QephRx1PSyj683q8'}

response = requests.get(api_url, headers=headers)

if response.status_code == requests.codes.ok:
    try:
        data = response.json()  # Parse JSON response
        quote = (json.dumps(data, sort_keys= True, indent=1))  # Pretty print JSON
    except json.JSONDecodeError:
        print("Error: Could not parse JSON response")
else:
    print("Error:", response.status_code, response.text)

print(quote)


for i in quote:
    if i != '"':
        print(i, end = "")

"""

import requests

api_url = 'https://api.api-ninjas.com/v1/quotes'
headers = {'X-Api-Key': 'XbIJXr6qNj3Cl3sZw7v5oQ==QephRx1PSyj683q8'}

response = requests.get(api_url, headers=headers)

if response.status_code == requests.codes.ok:
        data = response.json()  # Parse JSON response
        quote = data[0]['quote']  # Extract the quote text
        print(quote)
        
        
else:
    print("Error:", response.status_code, response.text)
