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

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM users
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
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
    def create_user(cls, username):
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
    
    # displays to cli or helper // or returns stuff. 
    # get_all 
    # index, show, create, and edit 

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
