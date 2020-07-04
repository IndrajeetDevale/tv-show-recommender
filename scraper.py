import requests
from requests import get
from bs4 import BeautifulSoup
from lxml import etree as et
from time import time, sleep
start_time = time()
from random import randint
from IPython.core.display import clear_output



headers = {"Accept-Language": "en-US, en;q=0.5"}
i =0
requests = 0
start = [str(i) for i in range(1,252,50)]
for startnum in start:
	page = get("https://www.imdb.com/search/title/?title_type=tv_series&user_rating=7.0,10.0&start="+ startnum , headers = headers)
	soup = BeautifulSoup(page.content, 'lxml')

	sleep(randint(8,15))

	requests += 1
	elapsed_time = time() - start_time
	print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	clear_output(wait = True)
		




