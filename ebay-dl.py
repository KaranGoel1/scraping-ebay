import argparse
from pandas._libs.missing import NA
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def parse_itemssold(text):
    '''
    Takes in a string and returns number of items sold as specified in string.

    >>> parse_itemssold('137 sold')
    137
    >>> parse_itemssold('11 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''

    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    '''
    Converts dollar value of price into cents
    '''

    if 'to' in text:
        text = text.replace(text[:text.index('o') + 2], '')
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if len(numbers) > 0:
        return int(numbers)
    else:
        return None

def parse_shipping(text):
    '''
    Converts dollar value of shipping into cents
    '''

    if 'Free' in text:
        return 0
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    return int(numbers)

def filename(text: str):
    '''
    Creates appropriate filename for json and csv files
    '''

    if ' ' in text:
        text = text.replace(' ', '_')
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download info from ebay and convert to JSON')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action='store_false')
    args = parser.parse_args()
    #print('args.search_term=', args.search_term)

    if args.csv == True:
        items = []
        for page_number in range(1,int(args.num_pages) + 1):
            url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
            url += args.search_term
            url += '&_sacat=0&_pgn='
            url += str(page_number)
            #print('url=', url)

            r = requests.get(url)
            status = r.status_code
            #print('status=', status)
            html = r.text
            #print('html=', html[:50])

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

                tags_itemssold = tag_item.select('.s-item__hotness')
                items_sold = None
                for tag in tags_itemssold:
                    items_sold = parse_itemssold(tag.text)

                tags_price = tag_item.select('.s-item__price')
                price = None
                for tag in tags_price:
                    price = parse_price(tag.text)

                tags_status = tag_item.select('.s-item__subtitle')
                status = None
                for tag in tags_status:
                    status = tag.text

                tags_shipping = tag_item.select('.s-item__shipping')
                shipping = None
                for tag in tags_shipping:
                    shipping = parse_shipping(tag.text)

                item = {
                    'name': name,
                    'price': price,
                    'status': status,
                    'shipping': shipping,
                    'free_returns': freereturns,
                    'items_sold': items_sold,
                }
                if len(name) > 0:
                    items.append(item)
            print('Page ' + str(page_number) + ' scraped')
            #print('len(tags_items)=', len(tags_items))
            
            #print('len(items)=', len(items))

        file_name = filename(args.search_term) + '.json'
        with open(file_name, 'w', encoding='ascii') as f:
            f.write(json.dumps(items))
    else:
        items = pd.DataFrame(columns=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
        for page_number in range(1,int(args.num_pages) + 1):
            url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
            url += args.search_term
            url += '&_sacat=0&_pgn='
            url += str(page_number)
            #print('url=', url)

            r = requests.get(url)
            status = r.status_code
            #print('status=', status)
            html = r.text
            #print('html=', html[:50])

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

                tags_itemssold = tag_item.select('.s-item__hotness')
                items_sold = None
                for tag in tags_itemssold:
                    items_sold = parse_itemssold(tag.text)

                tags_price = tag_item.select('.s-item__price')
                price = None
                for tag in tags_price:
                    price = parse_price(tag.text)

                tags_status = tag_item.select('.s-item__subtitle')
                status = None
                for tag in tags_status:
                    status = tag.text

                tags_shipping = tag_item.select('.s-item__shipping')
                shipping = None
                for tag in tags_shipping:
                    shipping = parse_shipping(tag.text)

                item = {
                    'name': name,
                    'price': price,
                    'status': status,
                    'shipping': shipping,
                    'free_returns': freereturns,
                    'items_sold': items_sold,
                }

               
                items = items.append(item, ignore_index=True)
            print('Page ' + str(page_number) + ' scraped')
            #print('len(tags_items)=', len(tags_items))
            
            #print('len(items)=', len(items))
        items = items.dropna(thresh=4)
        file_name = filename(args.search_term) + '.csv'
        items.to_csv(file_name)
