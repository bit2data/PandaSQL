path = 'data/usagov_bitly_data2012-03-16-1331923249.txt'
print(open(path).readline())

import json
#loads('{}') vs load(f)
records = [json.loads(line) for line in open(path)]
print(records[0])
print(records[0]['tz'])

#time_zones = [rec['tz'] for rec in records] #KeyError
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print(time_zones[:10])


def get_counts(seq):
    counts = {}
    for x in seq:
        counts[x] = counts.get(x, 0) + 1
    return counts


counts = get_counts(time_zones)
print(counts['America/New_York'])
assert 1251 == counts['America/New_York']
print(len(time_zones))
assert 3440 == len(time_zones)


def top_counts(count_dict, n=10):
    #{k:v} -> [(v,k)]
    v_k = [(count, tz) for tz, count in count_dict.items()]
    v_k.sort()
    return v_k[-n:]


print(top_counts(counts))

from pandas import DataFrame, Series
import pandas as pd

frame = DataFrame(records)
print(frame)
print(frame['tz'][:10])
tz_counts = frame['tz'].value_counts()
print(tz_counts[:10])

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print(tz_counts[:10])

#tz_counts[:10].plot(kind='barh', rot=0)

print(frame['a'][1])
print(frame['a'][50])
print(frame['a'][51])

results = Series([x.split()[0] for x in frame.a.dropna()])
print(results[:5])
print(results.value_counts()[:8])

import numpy as np 

print(frame.a.notnull()[:5]) #index to select
cframe = frame[frame.a.notnull()] # "selection"
op_sys = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
print(op_sys[:5])

by_tz_os = cframe.groupby(['tz', op_sys])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

indexer = agg_counts.sum(1).argsort()
print(indexer[:10])

count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)
# count_subset.plot(kind='barh', stacked=True)
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
print(normed_subset)
# normed_subset.plot(kind='barh', stacked=True)