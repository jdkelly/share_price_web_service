"""
Scrape current prices for all stocks in an index.
Supported indexes:
    UK:
        FTSE-100:   Hargreaves Lansdown
"""
import time
import pandas as pd
from web_scrapers import scrape_page


def parse_hl_uk_index_prices(index_id):
    """
    Parse current stock price information from an index page on Hargreaves Lansdown
    """
    url = 'http://www.hl.co.uk/shares/stock-market-summary/{}'.format(index_id)
    soup = scrape_page(url)
    data = soup.find('div', attrs={'id': 'view-constituents'})

    time_dt = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    siblings = data.find(text='EPIC').parent.parent.parent.find_next_sibling()

    stock_dict = {}
    for sibling in siblings.find_all('tr'):
        stock_id = sibling.find_all('td')[0].text
        price = sibling.find_all('td')[2].text
        stock_dict[stock_id] = [time_dt, price]

    df = pd.DataFrame(stock_dict).T
    df.columns = ['time_dt', 'price']

    return df
