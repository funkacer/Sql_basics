import pandas as pd
from sqlalchemy import create_engine

conn = "mysql://root:admin@localhost/sakila"
df = pd.read_sql_table(con = conn, table_name = "actor")
print(df.head())

tables_df = pd.read_sql_query(con = conn, sql = "show tables")
print(tables_df)
print(tables_df.__class__)

input()
