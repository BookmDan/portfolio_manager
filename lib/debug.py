#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.portfolio import Portfolio
from models.user import User

import ipdb


def reset_database():
    Portfolio.drop_table()
    User.drop_table()

    User.create_table()
    Portfolio.create_table()



reset_database()
ipdb.set_trace()

