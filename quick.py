import json
import urllib.request as urlreq

url = 'https://iroironaweb.datada.repl.co/usagov_bitly_data2012-03-16-1331923249.txt'
with urlreq.urlopen(url) as incoming:
  for chunk in incoming:
    print(json.loads(chunk)['tz'])
