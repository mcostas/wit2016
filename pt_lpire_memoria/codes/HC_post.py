from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from math import *
from odbAccess import *
import random, re, os, shutil, time


ODBFileName = sys.argv[-1]
odb = openOdb(path = '{0}.odb'.format(ODBFileName))
session.viewports['Viewport: 1'].setValues(displayedObject=odb)

xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
    'RF', NODAL, ((COMPONENT, 'RF3'), )), ), nodePick=(('ASSEMBLY', 1, (
    '[#2 ]', )), ), )
session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF', 
    NODAL, ((COMPONENT, 'RF3'), )), ), nodePick=(('ASSEMBLY', 1, ('[#2 ]', )), 
    ), )
xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
    'U', NODAL, ((COMPONENT, 'U3'), )), ), nodePick=(('ASSEMBLY', 1, ('[#1 ]', 
    )), ), )
session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
    NODAL, ((COMPONENT, 'U3'), )), ), nodePick=(('ASSEMBLY', 1, ('[#1 ]', )), 
    ), )
xy1 = session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 2']
xy1 = session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 2']
xy2 = saeGeneralFilter(xyData=xy1, cutoffFrequency=500)
xy2.setValues(
    sourceDescription='saeGeneralFilter ( xyData="RF:RF3 PI: ASSEMBLY N: 2" , cutoffFrequency=350  )')
tmpName = xy2.name
session.xyDataObjects.changeKey(tmpName, 'XYData-1')
xy1 = session.xyDataObjects['U:U3 PI: ASSEMBLY N: 1']
xy2 = session.xyDataObjects['XYData-1']
xy3 = combine(xy1, -xy2)
xy1 = session.xyDataObjects['U:U3 PI: ASSEMBLY N: 1']
xy2 = session.xyDataObjects['XYData-1']
xy3 = combine(xy1, -xy2)
xy3.setValues(
    sourceDescription='combine ( "U:U3 PI: ASSEMBLY N: 1", -"XYData-1" )')
tmpName = xy3.name
session.xyDataObjects.changeKey(tmpName, 'FD')

x0 = session.xyDataObjects['FD']
session.writeXYReport(fileName=ODBFileName + 'results.dat', appendMode=OFF, xyData=(x0, ))

odb.close()

infilename = ODBFileName + 'results.dat'
ifile = open(infilename, 'r')
framerange=0

with open('resultado.mass') as f:
    for line in f:
        data = line.split()
        mass = float(data[0])

vx=[]  # Vector with displacements
va=[]  # Vector with accelerations
vd=[]  # Vector with displacements
vf=[]  # Vector with forces

for i in range(3):
	ifile.readline()

for line in ifile:
	framerange = framerange + 1
	par = line.split()
	if len(par) == 0: break
	val1 = float(par[0])
	val2 = float(par[1])
	vd.append(val1)
	vf.append(val2)

Energyint=0
for i in range (framerange-2):
	Energyint = Energyint + (vd[i+1]-vd[i])*((vf[i]+vf[i+1])/2)

Energyint_SEA=0
for i in range (framerange-2):
	if vd[i] >= vd[i+1]:
		break
	Energyint_SEA = Energyint_SEA + (vd[i+1]-vd[i])*((vf[i]+vf[i+1])/2)

Energy = float(Energyint)
Energy_SEA = float(Energyint_SEA)


SEA = -Energy_SEA/mass
Peak_force = max(vf)

ResultadoEnergy = open(ODBFileName + '.energy','w')
ResultadoEnergy.write('%-E' % float(Energy))
ResultadoEnergy.close()

ResultadoEnergySEA = open(ODBFileName + '.energySEA','w')
ResultadoEnergySEA.write('%-E' % float(Energy_SEA))
ResultadoEnergySEA.close()

ResultadoMasa = open(ODBFileName + '.mass','w')
ResultadoMasa.write('%-E' % float(mass))
ResultadoMasa.close()

ResultadoSEA = open(ODBFileName + '.sea','w')
ResultadoSEA.write('%-E' % float(SEA))
ResultadoSEA.close()

ResultadoPeak = open(ODBFileName + '.peak','w')
ResultadoPeak.write('%-E' % float(Peak_force))
ResultadoPeak.close()

try:
    iter_num = os.getcwd() # Work dir: 'iteration.xx'
    iter_num = re.search('\.(\d{1,5})', iter_num).group(1) # Find 'iteration.' & 1to5 digits afterwards (keep these digits)
    driverouttmp = open('driver.out.'+iter_num+'.tmp','w')
    objective = abs(SEA) - 10.3
    driverouttmp.write('%-E' % float(objective))
    driverouttmp.close()
    shutil.move('driver.out.'+iter_num+'.tmp', 'driver.out.'+iter_num)
except:
    pass

# Test for Dakota w/ random solutions
def ransol():
    import random, re, os, shutil, time
    iter_num = os.getcwd() # Work dir: 'iteration.xx'
    iter_num = re.search('iteration\.(\d{1,5})', iter_num).group(1) # Find 'iteration.' & 1to5 digits afterwards (keep these digits)
    driverouttmp = open('driver.out.'+iter_num+'.tmp','w')
    random.seed()  # Seed based on current time
    objective = random.triangular(-1.,1.)
    driverouttmp.write('%-E' % float(objective))
    driverouttmp.close()
    shutil.move('driver.out.'+iter_num+'.tmp', 'driver.out.'+iter_num)

removetermins = ['abq', 'com', 'mdl', 'msg', 'pac', 'pre', 'prt', 'res', 'sel', 'sta', 'stt', 'inp']
l = os.listdir(os.getcwd())
for f in l:
    if f[-3:] in removetermins:
        os.remove(f)

try:
    os.remove('checkRun.status')
    os.remove(ODBFileName+'.odb')  # Remove .odb for Dakota
except:
    pass

# os.remove('HC.odb')
