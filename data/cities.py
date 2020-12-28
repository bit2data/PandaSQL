import sqlite3
# making lots of assumptions
# only TEXT and INTEGER
# more than 1 line
# no escping of ,
def can_be_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def sql_datatype_from_str(s):
  if can_be_int(s):
    return 'INTEGER'
  return 'TEXT'

# String String String -> String
# Table CSV CSV -> SQL
def create_table(table, cols, vals):
    return 'CREATE TABLE {} ({})'.format(table, ','.join(['{} {}'.format(k, sql_datatype_from_str(v)) for k, v in zip(cols.split(','), vals.split(','))]))
  
def import_csv(pth, table):
  with sqlite3.connect(':memory:') as conn:
    with open(pth, 'r') as fin:
      first = fin.readline() #header to be used as column names
      second = fin.readline() #first row of data to determine DATA type
      sql = create_table(table, first, second) 
      print(sql)
      conn.execute(sql)
      sql = 'INSERT INTO cities VALUES (?,?)'
      conn.execute(sql, second.split(','))
      for row in fin: 
        conn.execute(sql, row.split(','))
      for row in conn.execute('SELECT * FROM cities'):
        print(row)
  return 'done'

import_csv('city.csv', 'cities')

