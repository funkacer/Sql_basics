import pandas as pd
from sqlalchemy import create_engine

'''
#DESKTOP-NO9U58U\SQLEXPRESS
import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-NO9U58U\SQLEXPRESS;'
                      'Database=dbMoje;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM Moje')

for row in cursor:
    print(row)
'''

import urllib


quoted = urllib.parse.quote_plus("Driver={SQL Server};Server=DESKTOP-G1G1GTD\SQLEXPRESS;Database=dbMoje;Trusted_Connection=yes;")
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
df = pd.read_sql_table(con=engine, table_name = "Table_1")
print(df)

