import os
import sys

# import pandas as pd
# from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, DateTime
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from web_scrapers import scrape_page
from web_scraper_current_prices import parse_hl_uk_index_prices
from web_scraper_stock_information import parse_sharesmagazine_fundamentals

from database_setup import StockInformation

Base = declarative_base()
engine = create_engine(os.environ['DATABASE_URL'])
DBSession = sessionmaker(bind=engine)
session = DBSession()

indexes = {'ftse-100': [parse_hl_uk_index_prices, parse_sharesmagazine_fundamentals]}


def load_stock_information(indexes_dict):
    for index in indexes_dict:
        df = indexes_dict[index][0](index)

        for share in df.iterrows():
            print('Getting data for', share)
            try:
                fundamentals = parse_sharesmagazine_fundamentals(share[0])
                fundamentals_row = StockInformation(
                                                    id=fundamentals['id'],
                                                    stock_name=fundamentals['stock_name'],
                                                    description=fundamentals['description'],
                                                    sector=fundamentals['sector'],
                                                    stock_index=fundamentals['stock_index']
                                                    )
                session.add(fundamentals_row)
            except IOError :
                print('IO Error apparently')
            else:
                print('Could not get data for', share)

        session.commit()

if __name__ == '__main__':
    load_stock_information(indexes_dict=indexes)

"""
Move stock_info collection into a function

Add function for historic prices

Update loop to populate stock info then historic prices
"""