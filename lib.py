from multiprocessing import Pool
from glob import glob
import subprocess
import shlex
import os
import json
import time

import sqlite3


def isInteger(str):
	try:
		a = int(str)
		return True
	except:
		return False

def bzgrep(dat):
	data = {}
	p = subprocess.Popen(shlex.split("bzgrep '%s' %s" % (dat[0],dat[1])), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	data = out.decode('utf-8')
	return data


def searchAll(word,processors):
	if processors == 1:
		results = []
		os.system("bzgrep '%s' *bz2 > foo" % word)
		with open('foo','r') as f:
			for line in f:
				if len(line) > 0:
					results.append(json.loads(line.split('bz2:')[1]))
		return results
	else:
		files = [y for x in os.walk('./') for y in glob(os.path.join(x[0], '*.bz2'))]
		dat = []
		for file in files:
			dat.append((word,file))

		p=Pool(processors)
		results  = p.map(bzgrep,dat)
		datas = []
		for result in results:
			for res in result.split('\n'):
				try:
					datas.append(json.loads(res))
				except:
					pass
		return datas


start = time.time()
results = searchAll('hat',4)
print("Results took " + str(time.time()-start))

start = time.time()
data = results[0]

cols = []
for key in data:
	if isInteger(data[key]):
		cols.append(key + " INTEGER")
	else:
		cols.append(key + " TEXT")


conn = sqlite3.connect(':memory:')

c = conn.cursor()
c.execute('CREATE TABLE data (' + ','.join(cols) + ')')
for result in results:
	vals = []
	for col in result:
		if isInteger(result[col]):
			vals.append(result[col])
		else:
			if result[col] is None:
				vals.append("''")
			else:
				vals.append("'" + result[col].replace("'","") + "'")
	c.execute('INSERT INTO data (' + ','.join(result.keys()) + ') VALUES (' + ','.join(vals) + ')')

conn.commit()
print("Database building took " + str(time.time()-start))
c.execute('SELECT body,ups FROM data WHERE ups>100 order by ups desc limit 10')
print(c.fetchall())







