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

#Lists to store scraped data in
names = []
years = []
imdb_ratings = []
votes = []
genres = []
descriptions = []

#accept results in english language
headers = {"Accept-Language": "en-US, en;q=0.5"}

#initialisation of values used in counter
i =0
requests = 0
start = [str(i) for i in range(1,252,50)]

#for every page based on index of TV show
for startnum in start:
	
	#get request
	page = get("https://www.imdb.com/search/title/?title_type=tv_series&user_rating=7.0,10.0&start="+ startnum , headers = headers)
	
	#Pausing loop
	sleep(randint(8,15))

	#monitoring requests, useful for debugging
	requests += 1
	elapsed_time = time() - start_time
	#print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	clear_output(wait = True)

	# Throw a warning for non-200 status codes
	if page.status_code != 200:
		warn('Request: {}; Status code: {}'.format(requests, page.status_code))

	#Parse content of page
	soup = BeautifulSoup(page.content, 'lxml')

	#select all containers from page
	tv_containers = soup.find_all('div', class_= "lister-item mode-advanced")

	#for TV show individual container
	for container in tv_containers:

		#scrape name
		name = container.h3.a.text
		names.append(name)

		#scrape date
		year = container.h3.find('span', class_ = "lister-item-year text-muted unbold").text
		years.append(year)

		#scrape imdb rating
		imdb = float(container.strong.text)
		imdb_ratings.append(imdb)

		#scrape number of votes
		vote = container.find('span', attrs = {'name':'nv'})['data-value']
		votes.append(int(vote))

		#scrape genre
		try:
			genre = container.p.find('span', class_ = "genre").text
			genre = genre.strip('\n')
			genres.append(genre)
		except:
			genres.append('none')
		
		#scrape description
		description = container.find_all('p')[1].text
		description = description.strip('\n')
		descriptions.append(description)


#create dataframe 
tv_ratings = pd.DataFrame({'tv series': names,
'year': years,
'imdb': imdb_ratings,
'votes': votes,	
'genres': genres,
'description': descriptions
})

#reordering the columns
tv_ratings = tv_ratings[['tv series','year','imdb','votes','genres','description']]
print(tv_ratings.head())
tv_ratings.loc[:'year'] = tv_ratings['year'].str[-5:-2].astype(int)
print(tv_ratings['year'].head(3))