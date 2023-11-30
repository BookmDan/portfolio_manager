from models.__init__ import CURSOR, CONN

class Transaction:
  def __init__(self, transaction_id, user, crypto_coin, amount):
    self.transaction_id = transaction_id
    self.user = user
    self.crypto_coin = crypto_coin
    self.amount = amount

    # Other methods and properties...

  @classmethod
  def create(cls, user, crypto_coin, amount):
    sql = """
        INSERT INTO transactions (user_id, crypto_coin_id, amount)
        VALUES (?, ?, ?)
    """
    CURSOR.execute(sql, (user.user_id, crypto_coin.coin_id, amount))
    CONN.commit()

    transaction_id = CURSOR.lastrowid
    transaction = cls(transaction_id, user, crypto_coin, amount)
    return transaction
   
  @classmethod
  def create_table(cls):
    sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            crypto_coin_id INTEGER,
            coin_symbol TEXT,
            amount REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """

    # portfolio_id INTEGER,
    # transaction_type TEXT,
    # amount REAL,
    # timestamp TEXT,
    # FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
    CURSOR.execute(sql)
    CONN.commit()
  
Transaction.create_table()