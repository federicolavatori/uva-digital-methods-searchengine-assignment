# local import
from pathlib import Path
from datetime import datetime

# 3rd party imports
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pprint import pprint
import nltk
from nltk.corpus import stopwords
import squarify

# get stopwords
expanded_stopwords = ['likely', 'many', 'ceos', 'managers', 'often']
excluded_words = stopwords.words('english') + expanded_stopwords

# read data from auto_complete_compare
data = Path('./../output_data/data_15-07_05-10-2023.xlsx')
df = pd.read_excel(data)

# tokenize autosuggestions from male focussed queries
m_df = df.loc[df['query_type'] == 'm']
m_queries_tokens = {}
for index, query_data in m_df.iterrows():
	query = set(query_data['query'].split(' '))
	ac = set(query_data['ac'].split(' '))
	unique_words = ac.difference(query)
	for word in unique_words:
		if word not in excluded_words:
			if word not in m_queries_tokens:
				m_queries_tokens[word] = 1
			else:
				m_queries_tokens[word] += 1

# tokenize autosuggestions from female focussed queries
f_df = df.loc[df['query_type'] == 'f']
f_queries_tokens = {}
for index, query_data in f_df.iterrows():
	query = set(query_data['query'].split(' '))
	ac = set(query_data['ac'].split(' '))
	unique_words = ac.difference(query)
	for word in unique_words:
		if word not in excluded_words:
			if word not in f_queries_tokens:
				f_queries_tokens[word] = 1
			else:
				f_queries_tokens[word] += 1

# plot male data, save to fig
m_df = pd.DataFrame(m_queries_tokens.items(), columns=['word','count'])
m_df = m_df.sort_values('count', ascending = False)
m_df = m_df.head(10)
colors = sns.color_palette('pastel')

sns.set_style(style = 'whitegrid')
sizes = m_df['count'].values
label = m_df['word']
squarify.plot(sizes = sizes, label = label, alpha = 0.6,
			  color = colors).set(title = '10 Most used words in male queries')
plt.axis('off')
plt.tight_layout()

filename = 'treemap_' + str(datetime.now().strftime('%H-%M_%d-%m-%Y'))
plt.savefig(f'./../output_data/male_{filename}.png', dpi = 160, format = 'png')
print(f'exporting figure to {filename}.png...')

# reset plot
plt.clf()

# plot female data, save to fig
f_df = pd.DataFrame(f_queries_tokens.items(), columns=['word','count'])
f_df = f_df.sort_values('count', ascending = False)
f_df = f_df.head(10)
colors = sns.color_palette('pastel')

sns.set_style(style = 'whitegrid') # set seaborn plot style
sizes = f_df['count'].values # proportions of the categories
label = f_df['word']
squarify.plot(sizes = sizes, label = label, alpha = 0.6,
			  color = colors).set(title = '10 Most used words in female queries')
plt.axis('off')
plt.tight_layout()

filename = 'treemap_' + str(datetime.now().strftime('%H-%M_%d-%m-%Y'))
plt.savefig(f'./../output_data/female_{filename}.png', dpi = 160, format = 'png')
print(f'exporting figure to {filename}.png...')