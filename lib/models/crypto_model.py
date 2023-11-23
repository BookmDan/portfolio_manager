# lib/models/crypto_model.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from helpers import Base

class CryptoCoin(Base):
    __tablename__ = 'crypto_coins'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    price = Column(Float)  # Example field, you can add more as needed

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    coin_id = Column(Integer, ForeignKey('crypto_coins.id'))
    amount = Column(Float)
