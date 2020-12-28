import sqlite3
import json
import urllib.request as urlreq

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE bitly (a text, tz text);')

url = 'https://iroironaweb.datada.repl.co/usagov_bitly_data2012-03-16-1331923249.txt'
url = 'https://raw.githubusercontent.com/wesm/pydata-book/2nd-edition/datasets/bitly_usagov/example.txt'
with urlreq.urlopen(url) as fin:
  for line in fin:
    # each line is {} but the file is not [{}]
    # json.loads({}) vs json.load(f)
    row = json.loads(line)
    #clean_tz = frame['tz'].fillna('Missing')
    row['tz'] = row.get('tz', 'Missing')
    #clean_tz[clean_tz == ''] = 'Unknown'
    row['tz'] = 'Unknown' if row['tz'] == '' else row['tz']
    conn.execute('INSERT INTO bitly VALUES (?, ?);', (row.get('a', 'NULL'), row['tz']))

#frame['tz'][:10]
for row in conn.execute('SELECT * FROM bitly LIMIT 10'):
  print(row)

#frame['tz'].value_counts()
for row in conn.execute('SELECT tz, count(tz) AS cnt FROM bitly GROUP BY tz ORDER BY cnt'):
  print(row)
  
#results = Series([x.split()[0] for x in frame.a.dropna()])
#print(results[:5])
results = [row[0].split()[0] for row in conn.execute('SELECT a FROM bitly WHERE a is NOT NULL')]
for row in results[:10]:
  print(row)

#print(results.value_counts()[:8])
for row in conn.execute("SELECT SUBSTR(a, 1, INSTR(a, ' ')-1) AS b, COUNT(*) AS ctn FROM bitly WHERE a is NOT NULL GROUP BY b ORDER BY ctn"):
  print(row)

#cframe = frame[frame.a.notnull()] # "selection"
#op_sys = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
#by_tz_os = cframe.groupby(['tz', op_sys])
#agg_counts = by_tz_os.size().unstack().fillna(0)
#print(agg_counts[:10])
#indexer = agg_counts.sum(1).argsort()
#print(indexer[:10])
#
#count_subset = agg_counts.take(indexer)[-10:]
#normed_subset = count_subset.div(count_subset.sum(1), axis=0)

# 1 indicates Windows
# not clear how to do unstack trick
for row in conn.execute("SELECT MIN(1, INSTR(a, 'Windows')) AS Windows, SUBSTR(a, 1, INSTR(a, ' ')-1) AS b, COUNT(*) AS ctn FROM bitly WHERE b is NOT NULL GROUP BY b, Windows ORDER BY ctn"):
  print(row)

conn.close()