import logging
import os
from ..logger import CustomFormatter

# Logger configuration
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

from sqlalchemy import create_engine, Column, Integer, String, Float, DATE, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite database connection
engine = create_engine('sqlite:///database.db')

Base = declarative_base()

class checks(Base):
    """
    Represents the 'checks' table in the database.

    Attributes:
        check_number (int): The check number (primary key).
        products (str): The products included in the check.
    """

    __tablename__ = "checks"

    check_number = Column(Integer, primary_key=True)
    products = Column(String)

class companies(Base):
    """
    Represents the 'companies' table in the database.

    Attributes:
        company_id (int): The company ID (primary key).
        link (str): The company's website link.
        title (str): The company's title or name.
        phone (str): The company's phone number.
        address (str): The company's address.
        district (str): The district where the company is located.
        email (str): The company's email address.
        clicked (int): Indicator if the email has been clicked or not (default is 0).
    """

    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True)
    link = Column(String)
    title = Column(String)
    phone = Column(String)
    address = Column(String)
    district = Column(String)
    email = Column(String)
    clicked = Column(Integer, default=0)

class price_list(Base):
    """
    Represents the 'price_list' table in the database.

    Attributes:
        product_id (int): The product ID (primary key).
        product (str): The product name.
        price (int): The price of the product.
    """

    __tablename__ = "price_list"

    product_id = Column(Integer, primary_key=True)
    product = Column(String)
    price = Column(Integer)

Base.metadata.create_all(engine)
