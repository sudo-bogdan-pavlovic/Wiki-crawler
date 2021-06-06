#>===============================================<
#===>IMPORTS
import sys
from termcolor import colored
from itertools import chain
import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
#>===============================================<
#===>BANNER
with open("banner.txt", "r") as f:
	banner=f.read()

print(colored(banner, "magenta"))
#>===============================================<
#===>MAIN
crawled_list = []

def ext_par(soup):
	invalid = chain(
		soup.find_all('i'),
		soup.find_all('div', class_='hatnote'),
		soup.find_all('table'),
	)
	for tag in invalid:
		tag.extract()
	for paragraph in chain(soup.find_all('p'), soup.find_all('li')):
		count = 0
		skip = False
		clean = ""

		for character in str(paragraph):
			if character == '<':
				skip = True
			elif character == '>':
				skip = False

			if skip is False:
				if character == '(':
					count += 1
				elif character == ')':
					count -= 1
					continue
			if count == 0:
				clean += character
		yield BeautifulSoup(clean, 'html.parser')


def crawler(page, n=0):
	if page == quote("/wiki/Philosophy"):
		print(colored(f"Philosophy article have been found on number {n}!", "green"))
		return

	if page in crawled_list:
		print(colored(f"Loop found on number {n}", "red"))
		return
	else:
		crawled_list.append(page)

	url = f"https://en.wikipedia.org{page}"
	resp = requests.get(url)
	html = resp.content

	soup = BeautifulSoup(html, 'html.parser')
	title = soup.find('h1', id='firstHeading')
	article = soup.find(id='mw-content-text')
	print(colored(f"Article number:{n}, Name of article:{title.text}", "blue"))

	cur = None
	for parag in ext_par(article):
		cur = parag.find('a', href=re.compile(r'^/wiki/[^\:]+$'))
		if cur is not None:
			next = dict(cur.attrs)['href']
			return crawler(next, n + 1)

if __name__ == '__main__':
	try:
		page = f"/wiki/{format(sys.argv[1])}"
		print(colored(f"Starting page:{page}", "cyan")) 
	except IndexError:
		page = '/wiki/Special:Random'
		print(colored(f"Starting page:{page}", "cyan"))
	crawler(page)


#>===============================================<
