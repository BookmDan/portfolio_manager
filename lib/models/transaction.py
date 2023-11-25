from models.__init__ import CURSOR, CONN

class Transaction:
  @classmethod
  def create_table(cls):
    sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            portfolio_id INTEGER,
            transaction_type TEXT,
            amount REAL,
            timestamp TEXT,
            FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
        )
    """
    CURSOR.execute(sql)
    CONN.commit()