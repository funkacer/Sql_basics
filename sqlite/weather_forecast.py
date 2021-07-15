import sqlite3

import datetime, math

import os

delta_hours = 1

script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)
db = os.path.join(script_directory, "Weather_db_20200118.db")

#exit()

import pandas as pd

def readDB():
    global conn, cursor, forecasts, fnames, conditions, cnames
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT * " \
                   " FROM forecast")
                   #" WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now','-1 day'))")
    forecasts = cursor.fetchall()         # načte všechnyřádky ze selectu
    fnames = list(map(lambda x: x[0], cursor.description))
    #print(cursor.description)

    cursor.execute("SELECT * FROM condition")
                   #" WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now','-1 day'))")
    conditions = cursor.fetchall()         # načte všechnyřádky ze selectu
    cnames = list(map(lambda x: x[0], cursor.description))

    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno


readDB()

print(fnames)
print(cnames)

print('Pocet forecasts:', len(forecasts))
print('Pocet conditions:', len(conditions))

for row in forecasts[:1]:
    for col in row:
        print(col)

forecasts_df = pd.DataFrame(forecasts, columns=fnames)
print(forecasts_df.iloc[:10,:])
print(forecasts_df.dtypes)
