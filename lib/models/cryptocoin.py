# crypto_coin.py
from models.__init__ import CURSOR, CONN

class CryptoCoin:
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS crypto_coins (
                id INTEGER PRIMARY KEY,
                symbol TEXT,
                name TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS crypto_coins
        """
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, coin_id, symbol, name):
        self.coin_id = coin_id
        self.symbol = symbol
        self.name = name

    def __repr__(self):
        return f'<CryptoCoin {self.coin_id}: Symbol: {self.symbol}, Name: {self.name}>'

    @classmethod
    def create(cls, symbol, name):
        sql = """
            INSERT INTO crypto_coins (symbol, name)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (symbol, name))
        CONN.commit()

        coin_id = CURSOR.lastrowid
        coin = cls(coin_id, symbol, name)
        return coin

    @classmethod
    def delete(cls, coin):
        if coin.coin_id:
            sql = """
                DELETE FROM crypto_coins
                WHERE id = ?
            """
            CURSOR.execute(sql, (coin.coin_id,))
            CONN.commit()

    @classmethod
    def display_all(cls):
        cls.create_table()

        sql = """
            SELECT *
            FROM crypto_coins
        """
        rows = CURSOR.execute(sql).fetchall()
        for row in rows:
            print(f"CryptoCoin ID: {row[0]}, Symbol: {row[1]}, Name: {row[2]}")

    @classmethod
    def find_by_id(cls, coin_id):
        sql = """
            SELECT *
            FROM crypto_coins
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (coin_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        coin = cls(row[0], row[1], row[2])
        return coin

    @classmethod
    def find_by_symbol(cls, symbol):
        sql = """
            SELECT *
            FROM crypto_coins
            WHERE symbol = ?
        """
        row = CURSOR.execute(sql, (symbol,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
CryptoCoin.create_table()