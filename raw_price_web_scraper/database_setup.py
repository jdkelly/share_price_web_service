import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine(os.environ['DATABASE_URL'])

class StockInformation(Base):
    __tablename__ = 'stock_information'

    id = Column(String(10), primary_key=True)
    stock_name = Column(String(250), nullable=False)
    description = Column(Text)
    sector = Column(String(50))
    stock_index =  Column(String(10))

class DailyStockPrices(Base):
    __tablename__ = 'daily_stock_price'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(10), ForeignKey('stock_information.id'))
    date_dt = Column(DateTime)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)

    stock_information = relationship(StockInformation)

class CurrentStockPrice(Base):
    __tablename__ = 'current_stock_price'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(10), ForeignKey('stock_information.id'))
    time_dt = Column(DateTime)
    price = Column(Float)

    stock_information = relationship(StockInformation)


Base.metadata.create_all(engine)
