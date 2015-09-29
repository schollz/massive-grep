import subprocess
import shlex
from multiprocessing import Pool
import os
import json
from glob import glob
import uuid

def isInteger(str):
	try:
		a = int(str)
		return True
	except:
		return False

dj = {}

def bzgrep(dat):
	data = {}
	p = subprocess.Popen(shlex.split('bzgrep %s %s' % (dat[0],dat[1])), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	data[dat[1]] = out.decode('utf-8')
	with open(dat[2],'w') as f:
		f.write(json.dumps(data))

files = [y for x in os.walk('./') for y in glob(os.path.join(x[0], '*.bz2'))]
dat = []
for file in files:
	dat.append(('tiger',file,str(uuid.uuid4())))
print(dat)

p=Pool(8)
p.map(bzgrep,dat)

for d in dat:
	print(json.load(open(d[2],'r')))
	os.system('rm %s' % d[2])



'''
import sqlite3
import json


data = json.load(open('data.json','r'))

conn = sqlite3.connect(':memory:')

c = conn.cursor()
#c.execute('CREATE TABLE data (body text, author text, score integer, subreddit text, created_utc integer)')
for dat in data:
    print "INSERT INTO data VALUES ('%s','%s',%s,'%s',%s)" % (dat['body'],dat['author'],dat['score'],dat['subreddit'],dat['created_utc'])
    c.execute("INSERT INTO data VALUES ('%s','%s',%s,'%s',%s)" % (dat['body'].replace("'",""),dat['author'],dat['score'],dat['subreddit'],dat['created_utc']))

conn.commit()
c.execute('SELECT * FROM data WHERE score>?', str(0))
print c.fetchall()
'''

data = {'bridge':'3','smile':'some text'}

cols = []
for key in data:
	if isInteger(data[key]):
		cols.append(key + " INTEGER")
	else:
		cols.append(key + " TEXT")

cmd = 'CREATE TABLE data (' + ','.join(cols) + ')'

for key in data:	


print(cmd)
