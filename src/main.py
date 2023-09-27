import requests, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
# client param could be replaced with firefox or other browser
response = requests.get('http://google.com/complete/search?client=chrome&q=minecraft is better than', headers=headers)
for result in json.loads(response.text)[1]:
    print(result)


import os
from serpapi import GoogleSearch
import configparser

cfg = configparser.ConfigParser()
cfg.read('credentials.ini')
api_key = cfg['KEYS']['serpapi_key']

params = {
  "engine": "google_autocomplete",
  "q": "minecraft",
  "api_key": api_key
} .get()

search = GoogleSearch(params)
results = search.get_dict()

for result in results["suggestions"]:
  print(result['value'])