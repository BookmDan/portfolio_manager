from lib.models.cryptocoin import CryptoCoin, Portfolio, Transaction

# Drop existing tables
CryptoCoin.drop_table()
Portfolio.drop_table()
Transaction.drop_table()

# Create new tables
CryptoCoin.create_table()
Portfolio.create_table()
Transaction.create_table()

# Seed crypto coins
bitcoin = CryptoCoin.create(name='Bitcoin', symbol='BTC')
ethereum = CryptoCoin.create(name='Ethereum', symbol='ETH')
litecoin = CryptoCoin.create(name='Litecoin', symbol='LTC')

# Seed portfolios
joe_portfolio = Portfolio.create(user_name='Joe', crypto_coin_id=bitcoin.id, amount=0.5)
bud_portfolio = Portfolio.create(user_name='Bud', crypto_coin_id=ethereum.id, amount=1.2)
steph_portfolio = Portfolio.create(user_name='Steph', crypto_coin_id=litecoin.id, amount=5.0)
alice_portfolio = Portfolio.create(user_name='Alice', crypto_coin_id=bitcoin.id, amount=0.8)
jessica_portfolio = Portfolio.create(user_name='Jessica', crypto_coin_id=ethereum.id, amount=2.5)
remy_portfolio = Portfolio.create(user_name='Remy', crypto_coin_id=litecoin.id, amount=3.3)

# Seed transactions
Transaction.create(portfolio_id=joe_portfolio.id, transaction_type='buy', amount=0.2, timestamp='2023-11-20T15:00:00')
Transaction.create(portfolio_id=bud_portfolio.id, transaction_type='buy', amount=0.5, timestamp='2023-11-20T16:30:00')
Transaction.create(portfolio_id=steph_portfolio.id, transaction_type='sell', amount=1.0, timestamp='2023-11-21T10:45:00')
Transaction.create(portfolio_id=alice_portfolio.id, transaction_type='buy', amount=0.3, timestamp='2023-11-21T12:15:00')
Transaction.create(portfolio_id=jessica_portfolio.id, transaction_type='sell', amount=1.2, timestamp='2023-11-22T09:20:00')
Transaction.create(portfolio_id=remy_portfolio.id, transaction_type='buy', amount=1.5, timestamp='2023-11-22T14:40:00')

print('Seeding complete')