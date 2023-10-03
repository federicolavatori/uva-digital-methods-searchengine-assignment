# TO DO
# implement bing --> requires azure account, which requires creditcard...
# check browser differences / headings?
# check language options (all ac are nog in english)
# get screenshots from images tab --> html2image cookie issues

# optionally:
#   automatically get new vpn location

# local imports
from datetime import datetime
import json
import requests

# 3rd party imports
from html2image import Html2Image
import pandas as pd
from pprint import pprint



def add_to_data(df, query, engine, ac, type):
  new_row = {
     'query': query,
     'engine': engine,
     'ac': ac,
     'type': type,
     'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
  }
  df = df._append(new_row, ignore_index=True)
  return df

# initiate dataframe
df = pd.DataFrame(columns = ['query', 'engine', 'ac', 'country', 'timestamp'])

# get current location
# https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
location_response = requests.get('http://ipinfo.io/json')
location_data = json.loads(location_response.text)
print(f"searching from {location_data['country']}...\n")

lang = 'english'

# get urls from url_list_file
queries_file = f'queries_{lang}_small.txt'
queries = []
try:
  print(f'processing urls from {queries_file}...\n')
  with open(queries_file, 'r') as file:
    queries = file.readlines()
  file.close()
  queries = list(q[:q.rindex('\n')] if '\n' in q else q for q in queries) # remove \n (???)
except Exception as e:
  print('could not open url_list_file:', e)
  exit()

# get autocompletes per query
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582",
    # "languageCode": 'IT', # google header for different languages
}

for q in queries:
  q = q.split(',')
  print(type(q))
  print(q)
  # print(q, q[0], q[1])
  # q_type = q[0]
  # q = q[1]
  # print(q, q_type)
  exit()

  print(f'[{q}] query produces auto complete suggestions:')

  q_post = q.replace(' ', '%20') # replace space with %20 for query

  # google
  google_response = requests.get(f'http://google.com/complete/search?client=chrome&q={q_post}', headers = headers)
  google_response = json.loads(google_response.text)[1]
  print('\tgoogle:')
  for result in google_response:
    print('\t\t', result)
    df = add_to_data(df, q, 'Google', result, location_data['country'])
  print('')

  # ddg
  print('\tddg:')
  # https://github.com/theabbie/suggest <- found /ac/ path here
  ddg_response = requests.get(f'https://duckduckgo.com/ac/?kl=wt-wt&q={q_post}&format=json', headers = headers)
  ddg_response = json.loads(ddg_response.text)
  for result in ddg_response:
    print('\t\t', result['phrase'])
    df = add_to_data(df, q, 'DuckDuckGo', result['phrase'], location_data['country'])
  print('')

  # Yahoo
  print('\tyahoo:')
  # yahoo_url = f'https://search.yahoo.com/sugg/gossip/gossip-us-fastbreak/?pq=&command={q}&t_stmp=1696318693&callback=YAHOO.SA.apps%5B0%5D.cb.sacb17&l=1&bm=3&output=sd1&nresults=10&appid=syc&geoid=727232&ll=4.893189%2C52.373119&bck=28povfphqscki%26b%3D3%26s%3Dvf&csrcpvid=q0Ja0jEwLjIkZx9.Y64ykgUjMTQ2LgAAAAD20.Y8&vtestid=&mtestid=32369%3DNOUGEO03R%2628121%3DUNIOM02R%2628306%3DWTW000%2630405%3DGOGA01%2631718%3DWTDAI_PC_T%2631818%3DTNSRP01%2632671%3DVM25784C%2632722%3DPEOPLEPOPTEST%2633118%3DCCDD_S1%2633719%3D25810SLC%2633939%3DQRYC&spaceId=1197804867'
  yahoo_url = f'https://search.yahoo.com/sugg/gossip/gossip-us-fastbreak/?pq=&command={q_post}&output=json&callback=YAHOO.SA.apps%5B0%5D.cb.sacb17'
  yahoo_response = requests.get(yahoo_url)
  yahoo_response = json.loads(yahoo_response.text)['gossip']
  for result in yahoo_response['results']:
    print('\t\t', result['key'])
    df = add_to_data(df, q, 'Yahoo', result['key'], location_data['country'])

final_results = {
  'Google': {
    'male': 0,
    'female': 0},
  'DuckDuckGo': {
    'male': 0,
    'female': 0},
  'Yahoo': {
    'male': 0,
    'female': 0},
    }

for index, row in df.iterrows():
  if 'male' in row['query']:
    final_results[row['engine']]['male'] += 1
  else:
    final_results[row['engine']]['female'] += 1

pprint(final_results, sort_dicts=False)

# export results to xlsx
filename = str(location_data['country'])
filename += '_' + str(datetime.now().strftime('%d-%m-%Y'))
print(f'exporting data to {filename}_{lang}...')
df.to_excel(f'{filename}_{lang}.xlsx')
