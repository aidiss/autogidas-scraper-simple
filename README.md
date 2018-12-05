# Simple autogidas.lt scraper

This scraper collects car listing information from autogidas.lt

This module can scrape any car brand, save it to json.

Implemented fields are:

- price

Future fields:

- Name
- Seller price
- Photo url
- Photo

## Instalation

Dependencies:

- requests
- bs4

## How to us it

Make sure you are using Python3.

### Commandline use

```bash
# Scrape bmw and write it to json
python autogidas_scraper.py --brand="bmw" --output="data.json"
# Scrape audi and print it to commandline
python autogidas_scraper.py --brand="audi"
```

### Python module

You can also use it as a simple module.

#### Scraper

```py
from autogidas_scraper import Scraper
Scrape('bmw')
```

#### Parser

```py
from autogidas_scraper import Parser

# Parse whole listing html
page = '<html>...</html>'
clean_dict = Parser.parse_listing_page(page)

# Parse price html element
price_element = price_element
clean_price = Parser.parse_listing_price(price_element)
```

### Web api

```bash
# Launch the server by
python autogidas_scraper --server
```

Then you should be able to schedule a run by making a request to http://localhost:8877/scrape/audi
