import sqlite3
import numpy as np
import traceback

conn = sqlite3.connect('a.db')

def read_table(conn, table_name):

    dic = {}
    
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cursor.close()
        
        dic[0]=columns
        
        if len(data) > 0:
            for i, col in enumerate(data):
                dic[i+1] = data[i]

    except Exception as e:

        traceback.print_exc()
        
    #print(data.__class__)
        
    return dic
    
    
def write_table(conn, table_name, rows, columns):
    
    if table_name == 'a':
    
        try:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE {table_name}')
            cursor.close()
        except Exception as e:
            traceback.print_exc()
        
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, t TEXT)')
        for i in range(48,1000):
            value = '"' + chr(i) + '"'
            #print(i, value)
            cursor.execute(f'INSERT INTO {table_name} VALUES(NULL, {value})')
        conn.commit()
        cursor.close()
        
    if table_name == 't1' or table_name == 't2':
    
        try:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE {table_name}')
            cursor.close()
        except Exception as e:
            traceback.print_exc()
        
        cursor = conn.cursor()

        sql = f'CREATE TABLE {table_name} (id INTEGER PRIMARY KEY ' 
        for i in range(columns):
            col = 'c' + str(i)
            sql += f', c{str(i)} REAL'
        sql += ')'
        
        cursor.execute(sql)
        for i in range(rows):
            value = np.random.randint(0,columns,columns)
            #print(i, value)
            sql = f'INSERT INTO {table_name} VALUES(NULL'
            for c in range(columns):
                sql += f', {value[c]}'
            sql += ')'
            #print(sql)
            cursor.execute(sql)
        conn.commit()
        cursor.close()
            
    return None


def main():
    
    #write_table(conn, 'a')
    #write_table(conn, 't2')
        
    print(read_table(conn, 'sqlite_master'))
    #print(read_table(conn, 'a'))

    tables = ['t1','t2']

    for table in tables:
        write_table(conn, table, 5, 5)

    
    arrs = []

    for table in tables:

        print('\n' + table)
        data = read_table(conn, table)

        arr = np.array([])
        for i in range(1,len(data)):
            # <class 'tuple'>
            #print(data[i])
            arr = np.append(arr, data[i], axis = 0)

        arrs.append(arr.reshape(int(len(arr)/6),6))

        print(arrs[-1])
    
    input('Done')


if __name__ == '__main__':
    main()
    
