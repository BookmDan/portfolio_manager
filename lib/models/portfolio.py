# crypto_model.py
from models.__init__ import CURSOR, CONN

class Portfolio:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.portfolios = []

    def create_portfolio(self, coin_symbol, amount):
        portfolio = CryptoPortfolio.create(self, coin_symbol, amount)
        self.portfolios.append(portfolio)
        return portfolio

    def delete_portfolio(self, portfolio):
        if portfolio in self.portfolios:
            portfolio.delete()
            self.portfolios.remove(portfolio)
            return True
        return False

    def display_all_portfolios(self):
        for portfolio in self.portfolios:
            print(f"Portfolio ID: {portfolio.portfolio_id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")

    def find_portfolio_by_symbol(self, coin_symbol):
        for portfolio in self.portfolios:
            if portfolio.coin_symbol == coin_symbol:
                return portfolio
        return None

    @classmethod
    def create(cls, username):
        sql = """
            INSERT INTO users (username)
            VALUES (?)
        """
        CURSOR.execute(sql, (username,))
        CONN.commit()

        user_id = CURSOR.lastrowid
        user = cls(user_id, username)
        return user

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

    @classmethod
    def find_by_id(cls, portfolio_id):
        sql = """
            SELECT *
            FROM crypto_portfolios
            WHERE portfolio_id = ?
        """
        row = CURSOR.execute(sql, (portfolio_id,)).fetchone()
        return cls(row[0], User.find_by_id(row[1]), row[2], row[3]) if row else None
