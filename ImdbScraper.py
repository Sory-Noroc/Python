# Imdb Scraper done by Sory
# Python 3.6.9

import requests
from bs4 import BeautifulSoup
from time import sleep

class Scraper:
	imdb_link = 'https://www.imdb.com'

	def __init__(self):

		self.movie = input("What movie are you searching for? ") # Asking for movie name
		self.page = requests.get(f'{self.imdb_link}/find?q={self.movie}') # Getting the website url with the movie

		soup = BeautifulSoup(self.page.text, 'lxml') # Parsing the web page to the scraper

		found_movies = soup.find('table', class_='findList') # Finding the movies

		# Getting the links out of the movie table
		movie_links = [link.find('a').get('href') for link in found_movies.find_all('td', class_='result_text')]

		for link in movie_links:
			movie_page = requests.get(self.imdb_link + link)
			new_soup = BeautifulSoup(movie_page.text, 'lxml')
			# print(new_soup.prettify())
			print(new_soup.find('h1', class_='').text)
			if new_soup.find('span', itemprop='ratingValue'):
				print(f"Rating: {new_soup.find('span', itemprop='ratingValue').text}")
			print(f"Sumarry: {new_soup.find('div', class_='summary_text').text.strip()}")
			print()
			sleep(2)

		self.search_again = input("That's it. Search again? [Yes/No] ")

the_scraper = Scraper()

if the_scraper.search_again == 'Yes':
	the_scraper = Scraper()
else:
	print('Thank you for your attention!')
