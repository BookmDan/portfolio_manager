# crypto_model.py
from rich.style import Style
from rich.console import Console
from models.__init__ import CURSOR, CONN

class Portfolio:
    def __init__(self, id, user_id, coin_symbol, amount):
        self.id = id
        self.user_id = user_id
        self.coin_symbol = coin_symbol
        self.amount = amount

    def __repr__(self):
        return f'<CryptoPortfolio {self.id}: User: {self.user.username}, Coin: {self.coin_symbol}, Amount: {self.amount}>'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                coin_symbol TEXT, 
                amount REAL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def delete_user(self, user):
        if user and user.user_id:
            Portfolio.delete_user_portfolios(user.user_id)
            sql = """
                DELETE FROM users
                WHERE id = ?
            """
            CURSOR.execute(sql, (user.user_id,))
            CONN.commit()

    @classmethod
    def create_portfolio(cls, user, coin_symbol, amount):

        if coin_symbol:
            portfolio = Portfolio.create(user, coin_symbol, amount)
            # self.portfolios.append(portfolio)
            return portfolio
        else:
            raise ValueError(f"Coin symbol '{coin_symbol}' not found.")
        
        
    @classmethod
    def delete_portfolio(cls, portfolio):
        sql = """
            DELETE FROM portfolios
            WHERE user_id = ? AND id =? 
        """
        CURSOR.execute(sql, (portfolio.user_id, portfolio.id))
        CONN.commit()
    
    @classmethod
    def delete_user_portfolios(cls, user_id):
        sql = """
            DELETE FROM portfolios
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (user_id,))
        CONN.commit()

  
    @classmethod
    def create(cls, user, coin_symbol, amount):
        sql = """
            INSERT INTO portfolios (user_id, coin_symbol, amount)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (user.user_id, coin_symbol, amount))
        CONN.commit()

        portfolio_id = CURSOR.lastrowid
        portfolio = cls(portfolio_id, user, coin_symbol ,amount)
        return portfolio
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS portfolios
        """
        CURSOR.execute(sql)
        CONN.commit()

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
    
    def display_all_portfolios(self):
        for portfolio in self.portfolios:
            print(f"Portfolio ID: {portfolio.id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")

    @staticmethod
    def display_all_portfolios(user):
        sql = """
            SELECT *
            FROM portfolios
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (user.user_id,)).fetchall()
        portfolios = []
        if rows:
            for row in rows:
                portfolio_data = {
                    'id': row[0],
                    'coin_id': row[2],
                    'amount': row[3]
                }
                portfolios.append(portfolio_data)
        return portfolios
    
    @classmethod 
    def display_portfolios_by_user(cls, user_id):
        sql = """
            SELECT *
            FROM portfolios
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (user_id,)).fetchall()
        if rows:
            for row in rows:
                print(f"Portfolio ID: {row[0]}, Coin Symbol: {row[2]}, Amount: {row[3]}")
        else:
            print("No portfolios found for this user.")

    @classmethod
    def coin_symbol_exists(cls, user_id, coin_symbol):
        sql = """
            SELECT COUNT(*)
            FROM portfolios
            WHERE user_id = ? AND coin_symbol = ?
        """
        count = CURSOR.execute(sql, (user_id, coin_symbol)).fetchone()[0]
        return count > 0

