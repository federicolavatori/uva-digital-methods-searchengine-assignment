# local import
from pathlib import Path
from datetime import datetime

# 3rd party imports
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pprint import pprint

# read data from auto_complete_compare
data = Path('./../input_data/google images count.xlsx')
df = pd.read_excel(data)

# transform into format for grouped barchart
melted_df = pd.melt(df, id_vars = ['position', 'search engine'], var_name = 'type', value_name = 'count')
result_df = melted_df.groupby(['search engine', 'type'])['count'].sum().reset_index()
desired_order = ['male', 'female', 'both genders', 'genderless']
melted_df['type'] = pd.Categorical(melted_df['type'], categories = desired_order, ordered = True)
result_df = melted_df.sort_values(by = ['search engine', 'type']).reset_index(drop = True)

# plot data
sns.set_theme(style = 'whitegrid')
g = sns.catplot(
    data = result_df, kind = 'bar', errorbar = None,
    x = 'search engine', y = 'count', hue = 'type',
   	palette = ['#b9f2f0', '#fab0e4', '#8de5a1', '#d0bbff']) 

g.legend.set_visible(False)
plt.grid(visible = False)
plt.xlabel('Search engine')
plt.xticks(rotation = 45)
plt.ylabel('Count')
plt.yticks(rotation = 45)
plt.legend(loc = 'upper center', framealpha = 0.5)
plt.title('Distribution of focus of images')
plt.tight_layout()
filename = 'image_distribution_' + str(datetime.now().strftime('%H-%M_%d-%m-%Y'))
plt.savefig(f'./../output_data/{filename}.png', dpi = 160, format = 'png')
print(f'exporting figure to {filename}.png...')