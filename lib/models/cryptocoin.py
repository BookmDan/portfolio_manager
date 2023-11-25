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

    def __init__(self, coin_id, symbol=None, name=None):
        self.coin_id = coin_id
        self.symbol = symbol
        self.name = name

    def __repr__(self):
        return f'<CryptoCoin {self.coin_id}: Symbol: {self.symbol}, Name: {self.name}>'

    @classmethod
    def insert_initial_data(cls):
      sql = """
        SELECT COUNT(*)
        FROM crypto_coins
      """
      # checks to make sure there is only one copy of each crypto
      count = CURSOR.execute(sql).fetchone()[0]
      if count == 0:
        coins_data = [
            ("BTC", "Bitcoin"),
            ("ETH", "Ethereum"),
            ("LTC", "Litecoin"),
            ("ETC", "Ethereum Classic"),
            ("DOGE", "Dogecoin"),
            ("LINK", "Chainlink"),
            ("ADA", "Cardano"),
            ("SOL", "Solana"),
            ("XRP", "Ripple"),
            ("USDT", "Tether"),
            ("SHIB", "Shiba Inu"),
            ("MATIC", "Polygon"),
        ]

        CURSOR.executemany("INSERT INTO crypto_coins (symbol, name) VALUES (?, ?)", coins_data)

        CONN.commit()
        coin_id = CURSOR.lastrowid

        coin = cls(coin_id)
        return coin

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
        with CONN, CONN.cursor() as cursor: 
          rows = cursor.execute(sql).fetchall()
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
    def find_by_symbol(cls, symbol):
        sql = """
            SELECT *
            FROM crypto_coins
            WHERE symbol = ?
        """
        row = CURSOR.execute(sql, (symbol,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1], row[2]) if row else None
    
    @classmethod
    def get_all_symbols(cls):
        cls.create_table()

        sql = """
            SELECT symbol
            FROM crypto_coins
        """

        # with CONN, CONN.cursor() as cursor:
        rows = CURSOR.execute(sql).fetchall()
        return [row[0] for row in rows]

CryptoCoin.create_table()
# CryptoCoin.insert_initial_data()