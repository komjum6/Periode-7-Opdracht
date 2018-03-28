# Created Wednesday March 28th 2018
# By Teun van Duffelen, for HAN
# Version 1.0

import cx_Oracle

UN = "owe7_pg1"
PW = "blaat1234"
ADDR = "cytosine.nl"

def query(query):
    conn = cx_Oracle.connect(UN, PW, ADDR)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

result = query("""SELECT * FROM FRAME""")
for frame in result:
    print frame
