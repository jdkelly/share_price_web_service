import os
import sys

# import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from web_scraper_current_prices import parse_hl_uk_index_prices
from web_scraper_historic_prices import parse_historic_prices_uk_shareprices

from database_setup import StockInformation

Base = declarative_base()
engine = create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()

indexes = {'ftse-100': [parse_hl_uk_index_prices, parse_historic_prices_uk_shareprices]}

def load_historic_price_data(indexes_dict, start_day, start_month,
                             start_year, end_day, end_month, end_year):

    for index in indexes_dict:
        df = indexes_dict[index][0](index)

        for share in df.iterrows():
            print('Getting historic data for', share[0])

            try:
                historic_df = parse_historic_prices_uk_shareprices(share[0], start_day, start_month,
                                             start_year, end_day, end_month, end_year)

                historic_df.to_sql('daily_stock_price', con=conn, if_exists='append', index=False)
            except IOError :
                print('IO Error apparently')
            else:
                print('Could not get data for', share)
                session.commit()

if __name__ == '__main__':
    load_historic_price_data(indexes_dict=indexes, start_day=1, start_month=1,
                                         start_year=2010, end_day=15, end_month=12, end_year=2017)