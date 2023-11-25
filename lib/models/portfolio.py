# crypto_model.py
from models.__init__ import CURSOR, CONN


class Portfolio:
    # def __init__(self, user_id, username):
    #     self.user_id = user_id
    #     self.username = username
    #     self.portfolios = []

    def __init__(self, portfolio_id, user, coin_symbol, amount):
        self.portfolio_id = portfolio_id
        self.user = user
        self.coin_symbol = coin_symbol
        self.amount = amount

    def __repr__(self):
        return f'<CryptoPortfolio {self.portfolio_id}: User: {self.user.username}, Coin: {self.coin_symbol}, Amount: {self.amount}>'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                crypto_coin_id INTEGER,
                amount REAL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (crypto_coin_id) REFERENCES crypto_coins (id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def create_portfolio(self, coin_symbol, amount):
        portfolio = CryptoPortfolio.create(self, coin_symbol, amount)
        self.portfolios.append(portfolio)
        return portfolio

    @classmethod
    def create(cls, user, crypto_coin, amount):
        sql = """
            INSERT INTO portfolios (user_id, crypto_coin_id, amount)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (user.user_id, crypto_coin.coin_id, amount))
        CONN.commit()

        portfolio_id = CURSOR.lastrowid
        portfolio = cls(portfolio_id, user, crypto_coin ,amount)
        return portfolio
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS portfolios
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def delete_user_portfolios(cls, user_id):
        sql = """
            DELETE FROM portfolios
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (user_id,))
        CONN.commit()


    def display_all_portfolios(self):
        for portfolio in self.portfolios:
            print(f"Portfolio ID: {portfolio.portfolio_id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")

    def find_portfolio_by_symbol(self, coin_symbol):
        for portfolio in self.portfolios:
            if portfolio.coin_symbol == coin_symbol:
                return portfolio
        return None

    @classmethod
    def get_all_symbols(cls):
        sql = """
            SELECT DISTINCT crypto_coin_id
            FROM portfolios
        """
        rows = CURSOR.execute(sql).fetchall()
        return [row[0] for row in rows]


    @classmethod
    def delete(cls, user):
        sql = """
            DELETE FROM users
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (user.user_id,))
        CONN.commit()

    @classmethod
    def display_all(cls):
        sql = """
            SELECT *
            FROM users
        """
        rows = CURSOR.execute(sql).fetchall()
        for row in rows:
            print(f"User ID: {row[0]}, Username: {row[1]}")

    @classmethod
    def find_by_id(cls, user_id):
        from models.user import User 
        sql = """
            SELECT *
            FROM users
            WHERE user_id = ?
        """
        row = CURSOR.execute(sql, (user_id,)).fetchone()
        return cls(row[0], row[1]) if row else None

class CryptoPortfolio:
    def __init__(self, portfolio_id, user, coin_symbol, amount):
        self.portfolio_id = portfolio_id
        self.user = user
        self.coin_symbol = coin_symbol
        self.amount = amount

    @classmethod
    def create(cls, user, coin_symbol, amount):
        sql = """
            INSERT INTO crypto_portfolios (user_id, coin_symbol, amount)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (user.user_id, coin_symbol, amount))
        CONN.commit()

        portfolio_id = CURSOR.lastrowid
        portfolio = cls(portfolio_id, user, coin_symbol, amount)
        return portfolio

    def delete(self):
        sql = """
            DELETE FROM crypto_portfolios
            WHERE portfolio_id = ?
        """
        CURSOR.execute(sql, (self.portfolio_id,))
        CONN.commit()

    @classmethod
    def display_all(cls):
        sql = """
            SELECT *
            FROM crypto_portfolios
        """
        rows = CURSOR.execute(sql).fetchall()
        for row in rows:
            print(f"Portfolio ID: {row[0]}, Coin: {row[2]}, Amount: {row[3]}, User ID: {row[1]}")
