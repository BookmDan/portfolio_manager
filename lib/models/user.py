from models.__init__ import CURSOR, CONN
from models.portfolio import Portfolio
from models.cryptocoin import CryptoCoin

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

    def display_all_portfolios(self):
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
            print("This user has no portfolios.")

    def create_portfolio(self, coin_symbol, amount):
        crypto_coin = CryptoCoin.find_by_symbol(coin_symbol)

        if crypto_coin:
            portfolio = Portfolio.create(self, crypto_coin, amount)
            self.portfolios.append(portfolio)
            return portfolio
        else:
            raise ValueError(f"Coin symbol '{coin_symbol}' not found.")


    @classmethod
    def find_by_id(cls, user_id):
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (user_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
User.create_table()