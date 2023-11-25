from models.__init__ import CURSOR, CONN

class User:

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
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS portfolios
        """
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, user, crypto_coin, amount, id=None):
        self.id = id
        self.user = user
        self.crypto_coin = crypto_coin
        self.amount = amount

    def __repr__(self):
        return f'<Portfolio {self.id}: User ID: {self.user.id}, Coin ID: {self.crypto_coin.id}, Amount: {self.amount}>'

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        if isinstance(amount, float) and amount >= 0:
            self._amount = amount
        else:
            raise ValueError('Amount must be a non-negative float')

    @classmethod
    def create(cls, user, crypto_coin, amount):
        sql = """
            INSERT INTO portfolios (user_id, crypto_coin_id, amount)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (user.id, crypto_coin.id, amount))
        CONN.commit()

        portfolio_id = CURSOR.lastrowid
        portfolio = cls(user, crypto_coin, amount, portfolio_id)
        return portfolio

    @classmethod
    def delete(cls, portfolio):
        sql = """
            DELETE FROM portfolios
            WHERE id = ?
        """
        CURSOR.execute(sql, (portfolio.id,))
        CONN.commit()

    @classmethod
    def display_all(cls):
        sql = """
            SELECT *
            FROM portfolios
        """
        rows = CURSOR.execute(sql).fetchall()
        for row in rows:
            print(f"Portfolio ID: {row[0]}, User ID: {row[1]}, Coin ID: {row[2]}, Amount: {row[3]}")

    @classmethod
    def find_by_id(cls, portfolio_id):
        sql = """
            SELECT *
            FROM portfolios
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (portfolio_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        user = User.find_by_id(row[1])
        coin = CryptoCoin.find_by_id(row[2])
        portfolio = cls(user, coin, row[3], row[0])
        return portfolio