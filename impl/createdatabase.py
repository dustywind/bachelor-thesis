#!/usr/bin/env python3


import sqlite3

import informationretrieval

conn = sqlite3.connect('./database/narf.sqlite3')

dbm = informationretrieval.DatabaseManager(conn)

dbm.get_product_vector_manager()




