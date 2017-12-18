"""
Scrape historic daily prices for a given share.
Supported indexes:
    UK:
        FTSE-100:   Shareprices.com
"""
import time
import pandas as pd
from web_scrapers import scrape_page


def parse_historic_prices_uk_shareprices(stock_id, start_day, start_month,
                                         start_year, end_day, end_month, end_year):
    url = ('http://shareprices.com/detail?tidm='
           + '{}'  # Stock_ID
           + '&chart_time_period=3_year&movingaveragetype=&chart_comparison_tickers=&'
           + 'startday={}'
           + '&startmonth={}'
           + '&startyear={}'
           + '&endday={}'
           + '&endmonth={}'
           + '&endyear={}'
           + '&frequency=daily#history').format(stock_id, start_day, start_month,
                                                start_year, end_day, end_month, end_year)

    soup = scrape_page(url)
    data = soup.find_all('tr', attrs={'class': ['alternate1', 'alternate2']})

    historic_data = []
    for date in data:
        stock_id = stock_id
        date_dt = date.find('td', attrs={'class': 'shareshistory date'}).text
        open_price = date.find('td', attrs={'class': 'shareshistory open'}).text
        close_price = date.find('td', attrs={'class': 'shareshistory close'}).text
        high = date.find('td', attrs={'class': 'shareshistory high'}).text
        low = date.find('td', attrs={'class': 'shareshistory low'}).text
        volume = date.find('td', attrs={'class': 'shareshistory volume'}).text
        price_data = [stock_id, date_dt, open_price, close_price, high, low, volume]
        historic_data.append(price_data)

    df = pd.DataFrame(historic_data, columns=['stock_id', 'date_dt', 'open_price', 'close_price',
                                        'high', 'low', 'volume'])

    return df