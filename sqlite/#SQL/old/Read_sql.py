import os
import argparse
import sqlite3

def parseArgv():

    parser = argparse.ArgumentParser()
    parser.add_argument('database', metavar='Database_filename', type=str, nargs=1,
                    help='Database filename (string)')
    parser.set_defaults(database="")

    parser.add_argument('sql_files', metavar='SQL_filenames', type=str, nargs='*',
                    help='List of *.sql filenames (strings) separated by space')
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--verbose', dest='verbose', action='store_true')
    feature_parser.add_argument('--no-verbose', dest='verbose', action='store_false')
    parser.set_defaults(verbose=False)

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--interactive', dest='interactive', action='store_true')
    feature_parser.add_argument('--no-interactive', dest='interactive', action='store_false')
    parser.set_defaults(interactive='')

    return parser

def format_matrix(header, matrix,
                  top_format, left_format, cell_format, row_delim, col_delim):
    table = [[''] + header] + [[name] + row for name, row in zip(header, matrix)]
    table_format = [['{:^{}}'] + len(header) * [top_format]] \
                 + len(matrix) * [[left_format] + len(header) * [cell_format]]
    col_widths = [max(
                      len(format.format(cell, 0))
                      for format, cell in zip(col_format, col))
                  for col_format, col in zip(zip(*table_format), zip(*table))]
    return row_delim.join(
               col_delim.join(
                   format.format(cell, width)
                   for format, cell, width in zip(row_format, row, col_widths))
               for row_format, row in zip(table_format, table))

def get_sql_queries_dict(lst):
    sqls = {}
    for sql_file in lst:
        #print('SQL file:', sql_file)
        sql_file_exists = os.path.isfile(sql_file)
        #print('Check if file exists:', sql_file_exists)
        if sql_file_exists:
            sqls[sql_file] = []
            with open(sql_file, 'r') as f:
                sql = f.read()
                #print('SQL file query:')
                #print(sql.strip(), sql.count(';'))
                if sql.count(';') > 1:
                    for s in sql.split(';'):
                        if s.strip() != '': sqls[sql_file].append(s.strip())
                else:
                    sqls[sql_file].append(sql.strip())
        else:
            print('WAWNING!!! SQL file:', sql_file, 'does not exist!', '\n')

    return sqls

def main():

    parser = parseArgv()
    namespace = parser.parse_args()
    '''
    for k,v in vars(namespace).items():
        print(k, v)
    '''

    assert len(vars(namespace)['database']) == 1, 'Database_filename error'
    database_filename = vars(namespace)['database'][0]
    print('\n' + 'Database:', database_filename, '\n')

    if len(vars(namespace)['sql_files']) == 0 and (isinstance(vars(namespace)['interactive'], str) or not(vars(namespace)['interactive'])):
        parser.print_help()
        print()
    elif len(vars(namespace)['sql_files']) > 0:
        sqls = get_sql_queries_dict(vars(namespace)['sql_files'])
        #print(sqls, '\n')
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()
        for sqlf in sqls.keys():
            for i, sql in enumerate(sqls[sqlf]):
                print('SQL file {} query no {}:'.format(sqlf, str(i+1)))
                print(sql, '\n')
                c.execute('''{}'''.format(sql))
                data = c.fetchall()
                if data:
                    columns = [col[0] for col in c.description]
                    #print(data, '\n')
                    #print(list(list(a) for a in zip(*data)))
                    #print (format_matrix(columns, list(list(a) for a in zip(*data)), '{:^{}}', '{:<{}}', '{:>{}.3f}', '\n', ' | '))
                    #print (format_matrix(columns, list(list(a) for a in zip(*data)), '{:^{}}', '{:<{}}', '{:>{}}', '\n', ' | '))
                    for row in data:
                        for col in row:
                            #print(len(str(col)))
                            #TODO:pretty print
                            pass
                    row_format = "{:>15}" * (len(columns) + 1)
                    print(row_format.format("", *columns))
                    for i, row in enumerate(data):
                        #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                        print(row_format.format(str(i), *[str(r) for r in row]))    # Null to None
                    print()

    if vars(namespace)['interactive']:
        print('Entering interactive mode')

if __name__ == '__main__':
    main()
