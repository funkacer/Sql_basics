import pymssql

# cmd, hostname

hostname = 'DESKTOP-G1G1GTD'
#conn = pymssql.connect(server='(local)', database='dbMoje')
conn = pymssql.connect(server='DESKTOP-G1G1GTD', database='dbMoje')
#conn = pymssql.connect(host='localhost', database='dbMoje')

cursor = conn.cursor()

cursor.execute('SELECT * FROM [Table_1]')
print(cursor.fetchone())

conn.close()

