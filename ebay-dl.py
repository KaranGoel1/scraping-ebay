import argparse
import requests
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser(description='Download info from ebay and convert to JSON')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default=11)
args = parser.parse_args()
print('args.search_term=', args.search_term)

items = []
for page_number in range(1,int(args.num_pages) + 1):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url += args.search_term
    url += '&_sacat=0&_pgn='
    url += str(page_number)
    print('url=', url)

    r = requests.get(url)
    status = r.status_code
    print('status=', status)
    html = r.text
    print('html=', html[:50])

    soup = BeautifulSoup(html, 'html.parser')
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:
        #print('tag_item=', tag_item)

        tags_name = tag_item.select('.s-item__title')
        name = None
        for tag in tags_name:
            name = tag.text

        tags_freereturns = tag_item.select('.s-item__free-returns')
        freereturns = False
        for tag in tags_freereturns:   
            freereturns = True

        item = {
            'name': name,
            'free_returns': freereturns
        }
        items.append(item)
    print('len(tags_items)=', len(tags_items))
    
    print('len(items)=', len(items))

    #for item in items:
     #   print('item=', item)

    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))
    '''
    tags_name = soup.select('.s-item__title')
    for tag in tags_name:
        items.append({
            'name': tag.text
        })
    
    tags_freereturns = soup.select('.s-item__free-returns')
    for tag in tags_freereturns:
        print('tag=', tag)

    print('len(tags_name)=', len(tags_name))
    print('len(tags_free-returns)=', len(tags_freereturns))
    '''

