from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class Tse_Etf_Detail(Base):
    __tablename__ = 'tsepcfdetail'
    etf_code = Column(String(50), primary_key=True)
    code = Column(String(100), primary_key=True)
    name = Column(String(255))
    istn = Column(String(12))
    exchange = Column(String(10))
    currency = Column(String(3))
    shere_amount = Column(DECIMAL(15, 2))
    stock_price = Column(DECIMAL(15, 2))
    dt = Column(Integer, primary_key=True)
    update_source = Column(String(255), default='jpxwebetfpcfinfo')
    update_time = Column(TIMESTAMP, default='CURRENT_TIMESTAMP', server_default='CURRENT_TIMESTAMP')
 
class Tse_Etf_Summary(Base):
    __tablename__ = 'tsepcfsummary'
    etf_code = Column(String(50), primary_key=True)
    etf_name = Column(String(255))
    cash_oth = Column(DECIMAL(20, 2))
    outstanding = Column(DECIMAL(20, 2))
    fund_date = Column(Date)
    amount = Column(DECIMAL(20, 2))
    dt = Column(Integer, primary_key=True)
    update_source = Column(String(255), default='jpxwebetfpcfinfo')
    update_time = Column(TIMESTAMP, default='CURRENT_TIMESTAMP', server_default='CURRENT_TIMESTAMP')