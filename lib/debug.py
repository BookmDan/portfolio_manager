#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from lib.models.cryptocoin import CryptoCoin, Portfolio, Transaction
import ipdb


def reset_database():
    Transaction.drop_table()
    Portfolio.drop_table()
    CryptoCoin.drop_table()

    CryptoCoin.create_table()
    Portfolio.create_table()
    Transaction.create_table()

    # Create seed data
    bitcoin = CryptoCoin.create(name='Bitcoin', symbol='BTC')
    ethereum = CryptoCoin.create(name='Ethereum', symbol='ETH')

    joe_portfolio = Portfolio.create(user_name='Joe', crypto_coin_id=bitcoin.id, amount=0.5)
    bud_portfolio = Portfolio.create(user_name='Bud', crypto_coin_id=ethereum.id, amount=1.2)

    Transaction.create(portfolio_id=joe_portfolio.id, transaction_type='buy', amount=0.2, timestamp='2023-11-20T15:00:00')
    Transaction.create(portfolio_id=bud_portfolio.id, transaction_type='buy', amount=0.5, timestamp='2023-11-20T16:30:00')

reset_database()
ipdb.set_trace()

