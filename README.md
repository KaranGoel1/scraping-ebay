# Ebay Scraper

The ```ebay-dl.py``` file downloads 6 key elements of Ebay items into either a csv file or a json file. The elements are: Name, Price (in cents), Status (Brand New, Pre-Owned, etc...), Shipping Price (in cents), Free Returns, and Items Sold. 

## Instructions
The file can be run through the terminal and has 3 arguments to input: ```search_term```, ```--num_pages```, and ```--csv```. ```search_term``` simply takes in a string value for the product you wish to find the items for, and the search term must be specified. ```--num_pages``` takes in an integer argument for how many pages of items you wish to download. If ```--num_pages``` is not specified, it automatically takes on a value of 10. Finally, ```--csv``` chooses whether the file to be downloaded is a csv file or a json file. If ```--csv``` is specified, then data will download as a csv, otherwise it will be a json download.

To download ```hammer.csv```:

```
$python3 ebay-dl.py 'hammer' --num_pages=10 --csv
```

To download ```hammer.json```:

```
$python3 ebay-dl.py 'hammer' --num_pages=10
```

To download ```headphones.csv```:

```
$python3 ebay-dl.py 'headphones' --num_pages=10 --csv
```

To download ```headphones.json```:

```
$python3 ebay-dl.py 'headphones' --num_pages=10
```

To download ```cricket_bat.csv```:

```
$python3 ebay-dl.py 'cricket bat' --num_pages=10 --csv
```

To download ```cricket_bat.json```:

```
$python3 ebay-dl.py 'cricket bat' --num_pages=10
```

[Project Instructions](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)
