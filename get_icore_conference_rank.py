import requests
import pandas as pd

import multiprocessing as mp
from multiprocessing import Pool
from tqdm import tqdm

def get_conf_data(i):
    url = f'https://portal.core.edu.au/conf-ranks/{i}/'
    response = requests.get(url)

    data = dict()

    if response.status_code == 200:
        content = response.text  # or response.content for bytes
        index = content.find('<div id="detail">')
        content = content[index:]
        # get conference name
        index_start = content.find('<h2>')
        index_end = content.find('</h2>')
        conference_name = content[index_start+4:index_end]
        # get acronym
        index_start = content.find('Acronym: ')
        content = content[index_start:]
        index_end = content.find('</div>')
        acronym = content[9:index_end]
        # get rank
        index_start = content.find('Rank: ')
        content = content[index_start:index_start+500]
        index_end = content.find('</div>')
        rank = content[6:index_end]
        # add into data json
        data["index"] = i
        data["conference_name"] = conference_name
        data["acronym"] = acronym
        data["rank"] = rank
        data["url"] = url
    else:
        print(f"Request failed with status code {response.status_code} at {i}")
    return data

num_processes = 16
with Pool(num_processes) as p:
    data = list(tqdm(p.imap(get_conf_data, range(1,2325+1)), total=2325))

df = pd.DataFrame(data)
df.to_csv("icore-conf-rank.csv", index=False, encoding="utf-8")

print(df['rank'].value_counts())