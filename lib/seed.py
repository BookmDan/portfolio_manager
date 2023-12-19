from lib.models.portfolio import  Portfolio
from lib.models.user import  User


# Drop existing tables
Portfolio.drop_table()
User.drop_table()

# Create new tables
Portfolio.create_table()
User.create_table()


# Seed portfolios
joe_portfolio = Portfolio.create(user_name='Joe', coin_symbol='bitcoin', amount=0.5)
bud_portfolio = Portfolio.create(user_name='Bud', coin_symbol="ethereum", amount=1.2)
steph_portfolio = Portfolio.create(user_name='Steph', coin_symbol="litecoin", amount=5.0)
alice_portfolio = Portfolio.create(user_name='Alice', coin_symbol="bitcoin", amount=0.8)
jessica_portfolio = Portfolio.create(user_name='Jessica', coin_symbol="ethereum", amount=2.5)
remy_portfolio = Portfolio.create(user_name='Remy', coin_symbol="litecoin", amount=3.3)


print('Seeding complete')