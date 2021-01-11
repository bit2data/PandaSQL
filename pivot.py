import sqlite3
import json
import urllib.request as urlreq

conn = sqlite3.connect(':memory:')
conn.execute('''
CREATE TABLE 
  scores (
    sID INTEGER, 
    sName TEXT,
    exam TEXT,
    score INTEGER)
''')

url = 'https://bitbucket.org/datada/rdb/raw/d55fb7e7a48f3438a3b6a30788b885b9b97fc3dc/data/Score.json'
with urlreq.urlopen(url) as fin:
  rows = json.load(fin)
  for row in rows:
    conn.execute('INSERT INTO scores VALUES (?, ?, ?, ?);', row)

for row in conn.execute('SELECT * FROM scores LIMIT 10'):
  print(row)

sql = '''
SELECT 
  S1.sID, S1.sName, S1.score, S2.score, S3.score 
FROM 
  scores S1, scores S2, scores S3 
WHERE 
  S1.sID = S2.sID AND 
  S2.sID = S3.sID AND 
  S1.exam = 'Mid1' AND 
  S2.exam = 'Mid2' AND 
  S3.exam = 'Final';
'''
print('sID', 'sName', 'Mid1', 'Mid2', 'Final')
for row in conn.execute(sql):
  print(row)


conn.close()