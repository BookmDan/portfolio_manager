from models.__init__ import CURSOR, CONN

class Transaction:
  def __init__(self, transaction_id, user_id, crypto_coin, amount):
    self.transaction_id = transaction_id
    self.user_id = user_id
    self.crypto_coin = crypto_coin #id of the crypto coin 
    # self.coin_symbol = coin_symbol 
    self.amount = amount

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
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def create_transaction(cls, user_id, coin_symbol, amount):
      sql = """
          INSERT INTO transactions (user_id, coin_symbol, amount)
          VALUES (?, ?, ?)
      """
      CURSOR.execute(sql, (user_id, coin_symbol, amount))
      CONN.commit()

      transaction_id = CURSOR.lastrowid
      return cls(transaction_id, user_id, coin_symbol, amount)
  
  @classmethod
  def fetch_transactions_by_user(cls, user_id):
      sql = """
          SELECT id, user_id, coin_symbol, amount
          FROM transactions
          WHERE user_id = ?
      """
      rows = CURSOR.execute(sql, (user_id,)).fetchall()
      return [cls(*row) for row in rows]
  
Transaction.create_table()