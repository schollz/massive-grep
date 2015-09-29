import subprocess
import shlex
from multiprocessing import Pool
import os
import json
from glob import glob

def bzgrep(dat):
	p = subprocess.Popen(shlex.split('bzgrep %s %s' % (dat[0],dat[1])), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	print(out.decode("utf-8") )

files = [y for x in os.walk('./') for y in glob(os.path.join(x[0], '*.bz2'))]
dat = []
for file in files:
	dat.append(('tiger',file))
print(dat)

p=Pool(8)
print(p.map(bzgrep,dat))