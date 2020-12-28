import sqlite3

with sqlite3.connect(':memory:') as conn:
  with open('chinook.sql', 'r') as fin:
    conn.executescript(fin.read())
  for row in conn.execute('SELECT * FROM employees;'):
    print(row)            