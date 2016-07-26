# driver.py
import sys, os
from subprocess import Popen
from time import sleep
from datetime import datetime
from re import search

pf = sys.argv[1] 			# Parameters File
pmf = 'paramodel.py' 		# Parametrized Model File
rmf = 'paramodel.py.tmp'	# Running Model File
la = 'l-abaqus.sh' 			# queue Launcher for Abaqus

# Finding yourself
mdl = os.getcwd()
smp = search('(.*)sample\.(.*)', mdl).group(2)
smp = 'samp'+smp
mdl = search('(.*)/model/(.*)', mdl).group(1)
mdl = mdl+'/model'
rep = mdl+'/report.er'

# Job status check file
with open('checkRun.status', 'w') as rs:
	rs.write('True')
cRs = os.path.isfile('checkRun.status')

# Variables substitution
dpp = Popen(["dprepro", pf, pmf, rmf])
dpp.wait()

# Job launching
initime = datetime.today()
qa = Popen(["qsub", la])
qa.wait()

# Job status check
while cRs:
	sleep(10)
	cRs = os.path.isfile('checkRun.status')

endtime = datetime.today()
tdelta = endtime - initime

# Search & read the .oNN file
for f in os.listdir(os.getcwd()):
	found = f.find('.o')
	if (found != (-1)) and (f[-3:] != "odb"):
		oNN = f
		break

result = 'Unknown'
with open(oNN, "r") as o:
	for line in o:
		if "THE ANALYSIS HAS COMPLETED SUCCESSFULLY" in line:
			result = 'Success'
			break
		elif "THE ANALYSIS HAS NOT BEEN COMPLETED" in line:
			result = 'Failure'
			break

# os.remove(oNN)

# Write the report
with open(rep, "a") as r:
	r.write('\n'+smp+'\t'+str(tdelta)+'\t'+result)
