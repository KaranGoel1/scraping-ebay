import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Download info from ebay and convert to JSON')
parser.add_argument('search_term')
parser.add_argument('- -num_pages', default=10)
args = parser.parse_args()
print('args.search_term=', args.search_term)


for page_number in range(1,int(parser.num_pages + 1)):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url += args.search_term
    url += '&_sacat=0&_pgn='
    url += str(page_number)

r = requests.get(url)
status = r.status_code
print('status=', status)
html = r.text

soup = BeautifulSoup(html, 'html.parser')
tags = soup.select('.s-item__title')

for tag in tags:
    print('tag.text=', tag.text)
