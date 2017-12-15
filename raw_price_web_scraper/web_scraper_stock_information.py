import requests
import pandas as pd
import hashlib
from bs4 import BeautifulSoup
from web_scrapers import scrape_page

# parser for Shares Magazine stock data
def parse_sharesmagazine_fundamentals(stock_id):
    url = 'https://www.sharesmagazine.co.uk/shares/share/{}/fundamentals'.format(stock_id)
    soup = scrape_page(url)
    data = soup.find('div', attrs={'id': 'maincontent'})

    stock_name = data.find('h1').text.split(' (')[0]
    description = data.find(text='Activities').parent.find_next_sibling().text
    sector = data.find(text='Sector').parent.find_next_sibling().text
    stock_index =  data.find(text='Index').parent.find_next_sibling().text

    return {'id': stock_id,
            'stock_name': stock_name,
            'description': description,
            'sector': sector,
            'stock_index': stock_index}

