from .__init__ import CURSOR, CONN
from .portfolio import Portfolio
from .cryptocoin import CryptoCoin

class User:

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS users
        """
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.portfolios = []

    def __repr__(self):
        return f'<User {self.user_id}: Username: {self.username}>'

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if isinstance(username, str) and len(username):
            self._username = username
        else:
            raise ValueError('Username must be a non-empty string')

    @classmethod
    def create(cls, username):
        if isinstance(username, str) and len(username) > 0:
            sql = """
                INSERT INTO users (username)
                VALUES (?)
            """
            CURSOR.execute(sql, (username,))
            CONN.commit()

            user_id = CURSOR.lastrowid
            user = cls(user_id, username)
            return user
        else:
            raise ValueError("Username must be a non-empty string")

    @classmethod
    def delete(self, user):
        if user and user.user_id:
            Portfolio.delete_user_portfolios(user.user_id)
            sql = """
                DELETE FROM users
                WHERE id = ?
            """
            CURSOR.execute(sql, (user.user_id,))
            CONN.commit()

    @classmethod
    def delete_portfolio(cls, portfolio):
        sql = """
            DELETE FROM portfolios
            WHERE user_id = ? AND id =? 
        """
        CURSOR.execute(sql, (portfolio.user_id, portfolio.portfolio_id))
        CONN.commit()


    def view_portfolios(self):
        sql = """
            SELECT *
            FROM portfolios
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        if rows:
            for row in rows:
                print(f"Portfolio ID: {row[0]}, User ID: {row[1]}, Coin ID: {row[2]}, Amount: {row[3]}")
        else:
            print("This user has no portfolios.")

    @classmethod
    def find_by_id(cls, user_id):
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (user_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        user = cls(row[0], row[1]) if row else None
        return user
    
    @classmethod
    def display_all(cls):
        cls.create_table()

        sql = """
            SELECT *
            FROM users
        """
        rows = CURSOR.execute(sql).fetchall()
        for row in rows:
            print(f"User ID: {row[0]}, Username: {row[1]}")

    @staticmethod
    def display_all_portfolios():
        sql = """
            SELECT *
            FROM portfolios
        """
        rows = CURSOR.execute(sql).fetchall()
        if rows:
            for row in rows:
                print(f"User ID: {row[1]}, Portfolio ID: {row[0]}, Coin ID: {row[2]}, Amount: {row[3]}")
        else:
            print("No portfolios found.")

    def display_portfolios_by_user(self):
        sql = """
            SELECT *
            FROM portfolios
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (self.user_id,)).fetchall()
        if rows:
            for row in rows:
                print(f"Portfolio ID: {row[0]}, Coin ID: {row[2]}, Amount: {row[3]}")
        else:
            print("No portfolios found for this user.")

    def create_portfolio(self, coin_symbol, amount):
        crypto_coin = CryptoCoin.find_by_symbol(coin_symbol)

        if crypto_coin:
            portfolio = Portfolio.create(self, crypto_coin, amount)
            self.portfolios.append(portfolio)
            return portfolio
        else:
            raise ValueError(f"Coin symbol '{coin_symbol}' not found.")

    @classmethod
    def find_portfolio_by_symbol(cls, user_id, coin_symbol):
        crypto_coin_id = CryptoCoin.find_crypto_id_by_symbol(coin_symbol)

        if crypto_coin_id is not None:
            sql = """
                SELECT id, user_id, crypto_coin_id, amount
                FROM portfolios
                WHERE user_id = ? AND crypto_coin_id = ?
            """
            row = CURSOR.execute(sql, (user_id, crypto_coin_id)).fetchone()
            # print("Debug: Row from the database:", row) 

            if row is not None:
                return Portfolio(*row)
            else:
                print(f"No portfolio found for {coin_symbol}.")
        else:
            print(f"No crypto coin found for symbol {coin_symbol}.")

        return None


    @classmethod
    def find_by_id(cls, user_id):
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (user_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def find_portfolio_by_id(self, portfolio_id):
        sql = """
            SELECT *
            FROM portfolios
            WHERE user_id = ? AND id = ?
        """
        row = CURSOR.execute(sql, (self.user_id, portfolio_id)).fetchone()
        if row:
            return Portfolio(row[0], row[1], row[2], row[3])
        else:
            return None
    

User.create_table()
# User.find_portfolio_by_symbol(user_id=13, coin_symbol='BTC')
