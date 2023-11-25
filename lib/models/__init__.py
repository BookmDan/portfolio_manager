import sqlite3
# from models.user import User
CONN = sqlite3.connect('portfolio.db')
CURSOR = CONN.cursor()

# User.create_table()