# crypto_model.py
from models.__init__ import CURSOR, CONN
from models.cryptocoin import CryptoCoin

class Portfolio:
    def __init__(self, portfolio_id, user_id, coin_symbol, amount):
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        # self.crypto_coin_id = crypto_coin_id
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
        crypto_coin = CryptoCoin.find_by_symbol(coin_symbol)

        if crypto_coin:
            portfolio = Portfolio.create(user, crypto_coin, amount)
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
        CURSOR.execute(sql, (portfolio.user_id, portfolio.portfolio_id))
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
    def find_portfolio_by_symbol(cls, user_id, coin_symbol):
        portfolios = []

        crypto_coin_id = CryptoCoin.find_crypto_id_by_symbol(coin_symbol)
        if crypto_coin_id is not None:
            sql = """
                SELECT id, user_id, crypto_coin_id, amount
                FROM portfolios
                WHERE user_id = ? AND crypto_coin_id = ?
            """
            rows = CURSOR.execute(sql, (user_id, crypto_coin_id)).fetchall()
            portfolios.extend([cls(*row) for row in rows])

        if portfolios:
            for portfolio in portfolios:
                print(f"Portfolio found: Portfolio ID: {portfolio.portfolio_id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")
        else:
            print(f"No portfolios found for {coin_symbol}.")
            return None
        
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
                    'portfolio_id': row[0],
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
                print(f"Portfolio ID: {row[0]}, Coin ID: {row[2]}, Amount: {row[3]}")
        else:
            print("No portfolios found for this user.")

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
