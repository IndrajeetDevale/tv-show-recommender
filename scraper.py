import requests
from requests import get
from bs4 import BeautifulSoup
from lxml import etree as et
from time import time, sleep
start_time = time()
from warnings import warn
from random import randint
from IPython.core.display import clear_output
import pandas as pd

names = []
years = []
imdb_ratings = []
votes = []
descriptions = []

headers = {"Accept-Language": "en-US, en;q=0.5"}
i =0
requests = 0
start = [str(i) for i in range(1,252,50)]
for startnum in start:
	page = get("https://www.imdb.com/search/title/?title_type=tv_series&user_rating=7.0,10.0&start="+ startnum , headers = headers)
	

	sleep(randint(8,15))

	requests += 1
	elapsed_time = time() - start_time
	#print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	clear_output(wait = True)

	if page.status_code != 200:
		warn('Request: {}; Status code: {}'.format(requests, page.status_code))

	soup = BeautifulSoup(page.content, 'lxml')

	tv_containers = soup.find_all('div', class_= "lister-item mode-advanced")

	for container in tv_containers:

		name = container.h3.a.text
		names.append(name)

		year = container.h3.find('span', class_ = "lister-item-year text-muted unbold").text
		years.append(year)

		imdb = float(container.strong.text)
		imdb_ratings.append(imdb)

		vote = container.find('span', attrs = {'name':'nv'})['data-value']
		votes.append(int(vote))

		description = container.find_all('p')[1].text
		description = description.strip('\n')
		descriptions.append(description)



tv_ratings = pd.DataFrame({'tv series': names,
'year': years,
'imdb': imdb_ratings,
'votes': votes,	
'description': descriptions
})
#print(tv_ratings.info())
#print(tv_ratings.head(10))

tv_ratings = tv_ratings[['tv series','year','imdb','votes','description']]
print(tv_ratings.head())
