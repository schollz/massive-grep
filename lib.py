from multiprocessing import Pool
from glob import glob
import subprocess
import shlex
import os
import json
import time
import uuid

import sqlite3
from unidecode import unidecode

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
		print ('one processor')
		results = []
		tempfile = str(uuid.uuid4())
		os.system("find . | grep .bz2 | xargs bzgrep '%s' *bz2 > %s" % (word,tempfile))
		with open(tempfile,'r') as f:
			for line in f:
				if len(line) > 0:
					results.append(json.loads(line.split('bz2:')[1]))
		os.system("rm %s" % tempfile)
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
results = searchAll('speed of light',8)
print("Results took " + str(time.time()-start))

print(len(results))

start = time.time()
data = results[-1]
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
			vals.append(str(int(result[col])))
		else:
			if result[col] is None:
				vals.append("''")
			else:
				vals.append("'" + unidecode(result[col]).replace("'","") + "'")
        try:
            c.execute('INSERT INTO data (' + ','.join(result.keys()) + ') VALUES (' + ','.join(vals) + ')')
        except:
            pass

conn.commit()
print("Database building took " + str(time.time()-start))
c.execute('SELECT body,ups FROM data WHERE ups>100 order by ups desc limit 10')
for rows in c.fetchall():
    print(rows[0])
    print(rows[1])







