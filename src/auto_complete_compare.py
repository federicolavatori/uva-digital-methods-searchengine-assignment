# local imports
from datetime import datetime
import json
from pathlib import Path
import requests

# 3rd party imports
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pprint import pprint

def add_to_data(df, query, query_type, engine, ac, location):
  new_row = {
     'query': query,
     'query_type': query_type,
     'engine': engine,
     'ac': ac,
     'timestamp': datetime.now().strftime('%H:%M:%S %d-%m-%Y')
  }
  df = df._append(new_row, ignore_index=True)
  return df

# initiate dataframe
df = pd.DataFrame(columns = ['query', 'query_type', 'engine', 'ac', 'country', 'timestamp'])

# get current location
location_response = requests.get('http://ipinfo.io/json')
location_data = json.loads(location_response.text)
print(f"searching from {location_data['country']}...\n")

# get urls from url_list_file
queries_file = Path('./../input_data/queries_images.txt')
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

total_results_counter = 0

for q in queries:
  q = q.split(',')
  query_type = q[0]
  query = q[1]
  # print(f'type: [{query_type}]\tquery: [{query}]')
  query_post = query.replace(' ', '%20') # replace space with %20 for query

  # google
  google_response = requests.get(f'http://google.com/complete/search?client=chrome&q={query_post}', headers = headers)
  google_response = json.loads(google_response.text)[1]
  # print('\t\t\tgoogle results:', len(google_response))
  total_results_counter += len(google_response)
  for result in google_response:
    df = add_to_data(df, query, query_type, 'Google', result, location_data['country'])

  # ddg
  # https://github.com/theabbie/suggest <- found /ac/ path here
  ddg_response = requests.get(f'https://duckduckgo.com/ac/?kl=wt-wt&q={query_post}&format=json', headers = headers)
  ddg_response = json.loads(ddg_response.text)
  # print('\t\t\tddg results:', len(ddg_response))
  total_results_counter += len(ddg_response)
  for result in ddg_response:
    df = add_to_data(df, query, query_type, 'DuckDuckGo', result['phrase'], location_data['country'])

  # Yahoo
  yahoo_url = f'https://search.yahoo.com/sugg/gossip/gossip-us-fastbreak/?pq=&command={query_post}&output=json&callback=YAHOO.SA.apps%5B0%5D.cb.sacb17'
  yahoo_response = requests.get(yahoo_url)
  yahoo_response = json.loads(yahoo_response.text)['gossip']
  # print('\t\t\tyahoo results:', len(yahoo_response['results']))
  total_results_counter += len(yahoo_response['results'])
  for result in yahoo_response['results']:
    df = add_to_data(df, query, query_type, 'Yahoo', result['key'], location_data['country'])

# export total query results to xlsx
print(f'found a total of {total_results_counter} results')
filename = str(datetime.now().strftime('%H-%M_%d-%m-%Y'))
print(f'exporting data to data_{filename}...')
df.to_excel(f'./../output_data/data_{filename}.xlsx')

# transform dataframe to count types of queries per engine
df = pd.DataFrame(df.groupby(['engine', 'query_type'])['query_type'].count().rename('count')).reset_index()
print(df)
# create & style plot
sns.set(style = 'white')
sns.barplot(data = df, x = 'engine', y = 'count',
            hue = 'query_type', palette = ['#fab0e4', '#b9f2f0']
            )

plt.xlabel('Search engine')
plt.xticks(rotation = 45)
plt.ylabel('Autocomplete suggestions')
plt.yticks(rotation = 45)
plt.legend(loc = 'upper center', framealpha = 0.5)
plt.title('Amount of autocomplete suggestions based\non gender-focussed queries per search engine')
plt.tight_layout()
plt.savefig(f'./../output_data/queries_per_engine_{filename}.png', dpi = 160, format = 'png')
print(f'exporting figure to queries_per_engine_{filename}.png...')