from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()
from numpy import arctan
from numpy import cos
from numpy import sin
# from numpy import pi


# VARIABLES -----------------
scal = .6 #1 #scalling factor for hc
impact_velocity = 10 #impact velocity (m/s)
rsphere = .02
dtube = .5  #tube depth (m)
#dfactor=1  #.24/.25  #free space factor between cover and hc
ltube=.15    #tube side length
rcover=.025+1.5*ltube/2  #cover radius
ttube= 2 #.0015     #tube shell thickness (mm)
ttube = ttube / 1000. #mm to m
thc= 1  #honeycomb shell thickness (mm)
thc = thc / 1000. #mm to m
lhc=.005/scal    #honeycomb cell fourth length (m)
hhc=.00866/scal  #honeycomb cell half heigth (m)
hcd= .48 #{hcd}     #honeycomb cell depth (m)
# hcd = hcd / 1. #dm to m
hfill = hcd
# hfill = hfill / 10.
lcell=6*lhc  #honeycomb cell module length (m)
lfill=(ltube-ttube-thc)/2  #effective length to be filled (m)
noutput=600    #number of output requests (#)
delta=.30   #Distance travelled by impacting mass (m)
steptime=(delta/impact_velocity) #step time (s)
impactmass=0.6  # Weight of impacting mass (tons)
ltotal=0
ndomains=8
ncpus=ndomains
removefiles=1
msizehc = .002
msizefil = .002
msizetube = .002
back = 0
lsq = lhc*(1-back)
tube_edge = (ltube / 2) - (ttube / 2) - 0.0005

# Further calculations

beta = arctan(lsq/hhc)
l_offset = (1/(cos(beta))) * ((thc + 0.0004)/2)
l_offset2 =l_offset - (l_offset * sin(beta))


# Change of units

mdb.models.changeKey(fromName='Model-1', toName='HC')
model = mdb.models['HC']

# SPHERE ---------------------

s = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
s.FixedConstraint(entity=g[2])
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, rsphere), point2=(0.0, -rsphere), 
    direction=CLOCKWISE)
s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
s.Line(point1=(0.0, -rsphere), point2=(0.0, rsphere))
s.VerticalConstraint(entity=g[4], addUndoState=False)
p = model.Part(name='SPHERE', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
part_sph = model.parts['SPHERE']
part_sph.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
del model.sketches['__profile__']


# s = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
# g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
# s.setPrimaryObject(option=STANDALONE)
# s.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
# s.FixedConstraint(entity=g[2])
# s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -0.08), point2=(0.0, 0.08), 
#     direction=COUNTERCLOCKWISE)
# s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
# s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
# s.CoincidentConstraint(entity1=v[1], entity2=g[2], addUndoState=False)
# s.Line(point1=(0.0, 0.08), point2=(0.0, -0.08))
# s.VerticalConstraint(entity=g[4], addUndoState=False)
# s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
# p = model.Part(name='Part-1', dimensionality=THREE_D, 
#     type=DISCRETE_RIGID_SURFACE)
# p = model.parts['Part-1']
# p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
# s.unsetPrimaryObject()
# del model.sketches['__profile__']

# TUBE ----------------------



s4 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s4.setPrimaryObject(option=STANDALONE)
s4.rectangle(point1=(-(ltube/2), -(ltube/2)), point2=((ltube/2), (ltube/2)))
part_tube = model.Part(name='TUBE', dimensionality=THREE_D, type=DEFORMABLE_BODY)
part_tube.BaseShellExtrude(sketch=s4, depth=dtube)
s4.unsetPrimaryObject()
part_tube = model.parts['TUBE']
del model.sketches['__profile__']

p = model.parts['TUBE']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.49)
f = p.faces
d = p.datums
pickedFaces = f.findAt(((-0.016667, ltube/2, 0.333333), ))

p.PartitionFaceByDatumPlane(datumPlane=d[2], faces=pickedFaces)
pickedFaces = f.findAt(((ltube/2, 0.016667, 0.333333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[2], faces=pickedFaces)
pickedFaces = f.findAt(((0.016667, -ltube/2, 0.333333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[2], faces=pickedFaces)
pickedFaces = f.findAt(((-ltube/2, -0.016667, 0.333333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[2], faces=pickedFaces)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
#pickedFaces = f.findAt(((-0.016667, 0.05, 0.326667), ))
#p.PartitionFaceByDatumPlane(datumPlane=d[7, faces=pickedFaces)
pickedFaces = f.findAt(((0.016667, ltube/2, 0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[7], faces=pickedFaces)
pickedFaces = f.findAt(((-0.016667, -ltube/2, 0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[7], faces=pickedFaces)
pickedFaces = f.findAt(((ltube/2, -0.016667, 0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[8], faces=pickedFaces)
pickedFaces = f.findAt(((-ltube/2, 0.016667, 0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[8], faces=pickedFaces)

p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-0.01)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.01)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.01)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-0.01)

pickedFaces = f.findAt(((0.016667, ltube/2, 0.496667), ), ((0.016667, -ltube/2, 0.493333), 
    ))
p.PartitionFaceByDatumPlane(datumPlane=d[14], faces=pickedFaces)
pickedFaces = f.findAt(((-0.016667, -ltube/2, 0.496667), ), ((-0.016667, ltube/2, 
    0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[13], faces=pickedFaces)
pickedFaces = f.findAt(((-ltube/2, 0.016667, 0.496667), ), ((ltube/2, 0.016667, 
    0.493333), ))
p.PartitionFaceByDatumPlane(datumPlane=d[15], faces=pickedFaces)
pickedFaces = f.findAt(((-ltube/2, -0.016667, 0.493333), ), ((ltube/2, -0.016667, 
    0.496667), ))
p.PartitionFaceByDatumPlane(datumPlane=d[16], faces=pickedFaces)


# COVER ---------------------

s1 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rcover, 0.0))
p = model.Part(name='COVER', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
part_cover = model.parts['COVER']
part_cover.BaseShell(sketch=s1)
s1.unsetPrimaryObject()

del model.sketches['__profile__']

# COVER Impact --------------

s3 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s3.setPrimaryObject(option=STANDALONE)
s3.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rcover, 0.0))
p = model.Part(name='COVER_IMP', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
part_cover_imp = model.parts['COVER_IMP']
part_cover_imp.BaseShell(sketch=s3)
s3.unsetPrimaryObject()

del model.sketches['__profile__']

# TOP ------------------------

s5 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s5.setPrimaryObject(option=STANDALONE)
s5.rectangle(point1=(-(ltube/2), -(ltube/2)), point2=((ltube/2), (ltube/2)))
p = model.Part(name='TOP', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_top = model.parts['TOP']
part_top.BaseShell(sketch=s5)
s5.unsetPrimaryObject()
del model.sketches['__profile__']

# HC1 -------------------

# First step of HC Cell construction

# Calculation of number of patterned base elements in vertical direction
ltotalb=0
ntimesbt=0
while ltotalb<lfill:
	ltotalb=ltotalb+(2*hhc)
	ntimesbt=ntimesbt+1
ntimesbtmx=ntimesbt
ntimesbt=0

# Calculation of number of patterned diagonal elements in vertical direction

ltotalb=hhc
ntimesdg=0
while ltotalb<lfill:
	ltotalb=ltotalb+(2*hhc)
	ntimesdg=ntimesdg+1
ntimesdgmx=ntimesdg
ntimesdg=0

# Calculation of number of patterned top elements in vertical direction

ntimestpmx=ntimesdgmx


# Contruction of the HC Cells


s2 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s2.setPrimaryObject(option=STANDALONE)
times=0
htotal=0


for times in range(0,ntimesbtmx):
	ltotal=0
	while ltotal<=lfill:
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lhc, htotal))     #bottom1-1
		if (ltotal+lhc)>=lfill:
			s2.undo()
			if (ltotal)>=tube_edge:
				break
			else:
				s2.Line(point1=(ltotal, htotal), point2=(tube_edge, htotal))
				s2.Line(point1=(-ltotal, htotal), point2=(-tube_edge, htotal))     #bottom1-2
				s2.Line(point1=(ltotal, -htotal), point2=(tube_edge, -htotal))     #bottom1-3
				s2.Line(point1=(-ltotal, -htotal), point2=(-tube_edge, -htotal))
				break
		else:
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lhc, htotal))     #bottom1-2
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lhc, -htotal))     #bottom1-3
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lhc, -htotal))     #bottom1-4
		ltotal=ltotal+3*lhc+2*lsq
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lhc, htotal))     #bottom2-1
		if (ltotal+lhc)>=lfill:
			s2.undo()
			if (ltotal)>=tube_edge:
				break
			else:
				s2.Line(point1=(ltotal, htotal), point2=(tube_edge, htotal))
				s2.Line(point1=(-ltotal, htotal), point2=(-tube_edge, htotal))     #bottom1-2
				s2.Line(point1=(ltotal, -htotal), point2=(tube_edge, -htotal))     #bottom1-3
				s2.Line(point1=(-ltotal, -htotal), point2=(-tube_edge, -htotal))
				break

		else:
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lhc, htotal))     #bottom2-2
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lhc, -htotal))     #bottom2-3
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lhc, -htotal))     #bottom2-4
		ltotal=ltotal+lhc
	
	times=times+1
	htotal=htotal+2*hhc

times=0
htotal=hhc

for times in range(0,ntimestpmx):
	ltotal=lhc+lsq
	while ltotal<=lfill:
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lhc, htotal))     #top1-1
		if (ltotal+lhc)>=lfill:
			s2.undo()
			if (ltotal)>=tube_edge:
				break
			else:
				s2.Line(point1=(ltotal, htotal), point2=(tube_edge, htotal))
				s2.Line(point1=(-ltotal, htotal), point2=(-tube_edge, htotal))     #bottom1-2
				s2.Line(point1=(ltotal, -htotal), point2=(tube_edge, -htotal))     #bottom1-3
				s2.Line(point1=(-ltotal, -htotal), point2=(-tube_edge, -htotal))
				break

		else:
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lhc, htotal))     #top1-2
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lhc, -htotal))     #top1-3
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lhc, -htotal))     #top1-4
		ltotal=ltotal+lhc
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lhc, htotal))     #top2-1
		if (ltotal+lhc)>=lfill:
			s2.undo()
			if (ltotal)>=tube_edge:
				break
			else:
				s2.Line(point1=(ltotal, htotal), point2=(tube_edge, htotal))
				s2.Line(point1=(-ltotal, htotal), point2=(-tube_edge, htotal))     #bottom1-2
				s2.Line(point1=(ltotal, -htotal), point2=(tube_edge, -htotal))     #bottom1-3
				s2.Line(point1=(-ltotal, -htotal), point2=(-tube_edge, -htotal))
				break

		else:
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lhc, htotal))     #top2-2
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lhc, -htotal))     #top2-3
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lhc, -htotal))     #top2-4
		ltotal=ltotal+3*lhc+2*lsq
	
	times=times+1
	htotal=htotal+2*hhc

times=0
htotal=0

for times in range(0,ntimesdgmx):
	ltotal=lhc

	while ltotal<=lfill:

		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq, htotal+hhc))     #diag1-1
		if (ltotal+lsq) >= lfill:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq, -htotal-hhc))     #diag1-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq, -htotal-hhc))     #diag1-3
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq, htotal+hhc))     #diag1-4
		ltotal=ltotal+lsq+2*lhc
	
	
		s2.Line(point1=(ltotal, htotal+hhc), point2=(ltotal+lsq, htotal))     #diag2-1
		if (ltotal+lsq) >= lfill:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal-hhc), point2=(ltotal+lsq, -htotal))     #diag2-2
			s2.Line(point1=(-ltotal, -htotal-hhc), point2=(-ltotal-lsq, -htotal))     #diag2-2
			s2.Line(point1=(-ltotal, htotal+hhc), point2=(-ltotal-lsq, htotal))     #diag2-2
		ltotal=ltotal+2*lhc+lsq
	htotal=htotal+2*hhc

htotalaux = htotal

# Fit on the side edge



if ltotal < tube_edge:
	aux = int(ntimesdgmx / 2)
	aux = 2 * aux
	if ntimesdgmx == aux:
		htotal = 0
	else:
		htotal = hhc
	lsq_red = tube_edge - ltotal
	reductionl = lsq_red / lsq
	hhc_red = reductionl * hhc
	inv_hhc_red = hhc - hhc_red
	while htotal < tube_edge:
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal+hhc_red))     #diag1-1
		if (htotal+lsq_red) > tube_edge:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal-hhc_red))     #diag1-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal-hhc_red))     #diag1-3
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal+hhc_red))     #diag1-4
		# htotal=htotal+hhc
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal-hhc_red))     #diag2-1
		if (ltotal+lsq_red) > tube_edge:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal+hhc_red))     #diag2-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal+hhc_red))     #diag2-2
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal-hhc_red))     #diag2-2

		htotal = htotal + 2 * hhc

# Fit on the top edge

htotal = htotalaux

if htotal < tube_edge:
	ltotal = lhc
	hhc_red = tube_edge - htotal
	reductionh = hhc_red / hhc
	lsq_red = reductionh * lsq
	inv_lsq_red = lsq - lsq_red
	while ltotal<=lfill:
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal+hhc_red))     #diag1-1
		if (ltotal + lsq_red) > tube_edge:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal-hhc_red))     #diag1-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal-hhc_red))     #diag1-3
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal+hhc_red))     #diag1-4
			ltotal=ltotal+lsq+2*lhc
		if ltotal < tube_edge:
			s2.Line(point1=(ltotal+inv_lsq_red, htotal+hhc_red), point2=(ltotal+lsq, htotal))     #diag2-1
			if (ltotal + lsq) > tube_edge:
				s2.undo()
				break
			else:
				s2.Line(point1=(ltotal+inv_lsq_red, -htotal-hhc_red), point2=(ltotal+lsq, -htotal))     #diag2-2
				s2.Line(point1=(-ltotal-inv_lsq_red, -htotal-hhc_red), point2=(-ltotal-lsq, -htotal))     #diag2-2
				s2.Line(point1=(-ltotal-inv_lsq_red, htotal+hhc_red), point2=(-ltotal-lsq, htotal))     #diag2-2
				ltotal=ltotal+2*lhc+lsq
		else:
			break
else:
	htotal = htotal - hhc
	if htotal < tube_edge:
		ltotal = lhc
		hhc_red = tube_edge - htotal
		reductionh = hhc_red / hhc
		lsq_red = reductionh * lsq
		inv_lsq_red = lsq - lsq_red
		# s2.Line(point1=(ltotal + inv_lsq_red, tube_edge), point2=(ltotal+lsq, htotal))     #diag3-1
		while ltotal < lfill:
			s2.Line(point1=(ltotal + inv_lsq_red, tube_edge), point2=(ltotal+lsq, htotal))     #diag3-1
			if (ltotal+lsq) >= lfill:
				s2.undo()
				break
			else:
				s2.Line(point1=(ltotal + inv_lsq_red, -tube_edge), point2=(ltotal+lsq, -htotal))     #diag3-2
				s2.Line(point1=(-ltotal - inv_lsq_red, -tube_edge), point2=(-ltotal-lsq, -htotal))     #diag3-3
				s2.Line(point1=(-ltotal - inv_lsq_red, tube_edge), point2=(-ltotal-lsq, htotal))     #diag3-4
			ltotal=ltotal+2*lhc+lsq
			if ltotal < tube_edge:
				s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal + hhc_red))     #diag4-1
				if (ltotal+lsq) >= lfill:
					s2.undo()
					break
				else:
					s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal - hhc_red))     #diag4-2
					s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal - hhc_red))     #diag4-3
					s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal + hhc_red))     #diag4-4
				ltotal=ltotal+2*lhc+lsq
			else:
				break



times=0
htotal=2*hhc

for times in range(0,ntimesbtmx-1):
	ltotal=lhc

	while ltotal<=lfill:

		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq, htotal-hhc))     #diag3-1
		if (ltotal+lsq) >= lfill:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq, -htotal+hhc))     #diag3-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq, -htotal+hhc))     #diag3-3
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq, htotal-hhc))     #diag3-4
		ltotal=ltotal+2*lhc+lsq
	
	
		s2.Line(point1=(ltotal, htotal-hhc), point2=(ltotal+lsq, htotal))     #diag4-1
		if (ltotal+lsq) >= lfill:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal+hhc), point2=(ltotal+lsq, -htotal))     #diag4-2
			s2.Line(point1=(-ltotal, -htotal+hhc), point2=(-ltotal-lsq, -htotal))     #diag4-3
			s2.Line(point1=(-ltotal, htotal-hhc), point2=(-ltotal-lsq, htotal))     #diag4-4
		ltotal=ltotal+2*lhc+lsq
	htotal=htotal+2*hhc

ltotal = ltotal + 2 * lhc + lsq

if ltotal < tube_edge:
	htotal = 0
	lsq_red = tube_edge - ltotal
	reductionl = lsq_red / lsq
	hhc_red = reductionl * hhc
	inv_hhc_red = hhc - hhc_red
	while htotal < tube_edge:
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal+hhc_red))     #diag1-1
		if (htotal+lsq_red) > tube_edge:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal-hhc_red))     #diag1-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal-hhc_red))     #diag1-3
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal+hhc_red))     #diag1-4
		# htotal=htotal+hhc
	
		s2.Line(point1=(ltotal, htotal), point2=(ltotal+lsq_red, htotal-hhc_red))     #diag2-1
		if (ltotal+lsq_red) > tube_edge:
			s2.undo()
			break
		else:
			s2.Line(point1=(ltotal, -htotal), point2=(ltotal+lsq_red, -htotal+hhc_red))     #diag2-2
			s2.Line(point1=(-ltotal, -htotal), point2=(-ltotal-lsq_red, -htotal+hhc_red))     #diag2-2
			s2.Line(point1=(-ltotal, htotal), point2=(-ltotal-lsq_red, htotal-hhc_red))     #diag2-2

		htotal = htotal + 2 * hhc


p = model.Part(name='HC', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_hc = model.parts['HC']
part_hc.BaseShellExtrude(sketch=s2, depth=hcd)
s2.unsetPrimaryObject()
del model.sketches['__profile__']


# FILLING ------------------------------------

thc = ((thc + 0.0004)/2)

s3 = model.ConstrainedSketch(name='__profile__', sheetSize=1.0)
s3.setPrimaryObject(option=STANDALONE)

ltotal = lhc
htotal = 0

# Central cell: right + left (1)
while (ltotal + (2*lsq) + (2*lhc)) < tube_edge:


	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, - htotal - hhc + thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, - htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))


	s3.Line(point1=(-ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(-ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, - htotal - hhc + thc))
	s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
	s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))
	s3.Line(point1=(-ltotal - lsq - l_offset2, htotal + hhc - thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
	s3.Line(point1=(-ltotal - lsq - l_offset2, - htotal - hhc + thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))

	ltotal = ltotal + (2*lsq) + (4*lhc)


ltotal = lhc
htotal = 0
countx = 0
county = 0
point = 2*lsq + 3*lhc

while point <= tube_edge:
	county = county + 1
	point = point + (2 * lsq) + (4 * lhc)

# (2)

while (htotal + (3 * hhc)) < tube_edge:
	htotal = htotal + (2*hhc)
	ltotal = lhc
	for countx in xrange(0,(county)):
	# while (ltotal + (2*lsq) + (2*lhc)) < tube_edge:
		s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal - hhc + thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))

		s3.Line(point1=(-ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(-ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, htotal - hhc + thc))
		s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal - hhc + thc))
		s3.Line(point1=(-ltotal - lsq - l_offset2, htotal + hhc - thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(-ltotal - lsq - l_offset2, htotal - hhc + thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal - hhc + thc))

		s3.Line(point1=(ltotal + l_offset, - htotal), point2=(ltotal + lsq + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + l_offset, - htotal), point2=(ltotal + lsq + l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, - htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, - htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, - htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, - htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal + hhc - thc))

		s3.Line(point1=(-ltotal - l_offset, - htotal), point2=(- ltotal - lsq - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(-ltotal - l_offset, - htotal), point2=(- ltotal - lsq - l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, - htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(-ltotal - (2*lsq) - (2*lhc) + l_offset, - htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(-ltotal - lsq - l_offset2, - htotal - hhc + thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(-ltotal - lsq - l_offset2, - htotal + hhc - thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal + hhc - thc))

		ltotal = ltotal + (2*lsq) + (4*lhc)
		countx = countx + 1



# (3)


ltotal = - (lhc) - (lsq)
htotal = hhc

while (htotal + (hhc)) < tube_edge:

	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal - hhc + thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))

	htotal =  htotal + (2 * hhc)

ltotal = - (lhc) - (lsq)
htotal = - hhc

while (htotal - (hhc)) > ( - tube_edge):

	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal - hhc + thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
	s3.Line(point1=(ltotal + lsq + l_offset2, htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))

	htotal =  htotal - (2 * hhc)

point = lhc + lsq
countz = 0
countx = 0

# (4)

while point <= tube_edge:
	countz = countz + 1
	point = point + (2*lsq) + (4*lhc)

htotal = - hhc

while (htotal + (3*hhc)) < tube_edge:

	htotal =  htotal + (2 * hhc)
	ltotal = (lsq) + (3*lhc)

	for countx in xrange(0,(countz-1)):

		s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + l_offset, htotal), point2=(ltotal + lsq + l_offset2, htotal - hhc + thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, htotal - hhc + thc))

		s3.Line(point1=(ltotal + l_offset, - htotal), point2=(ltotal + lsq + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + l_offset, - htotal), point2=(ltotal + lsq + l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, - htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + (2*lsq) + (2*lhc) - l_offset, - htotal), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, - htotal - hhc + thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(ltotal + lsq + l_offset2, - htotal + hhc - thc), point2=(ltotal + (lsq) + (2*lhc) - l_offset2, - htotal + hhc - thc))

		s3.Line(point1=(- ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, htotal + hhc - thc))
		s3.Line(point1=(- ltotal - l_offset, htotal), point2=(- ltotal - lsq - l_offset2, htotal - hhc + thc))
		s3.Line(point1=(- ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(- ltotal - (2*lsq) - (2*lhc) + l_offset, htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal - hhc + thc))
		s3.Line(point1=(- ltotal - lsq - l_offset2, htotal + hhc - thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal + hhc - thc))
		s3.Line(point1=(- ltotal - lsq - l_offset2, htotal - hhc + thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, htotal - hhc + thc))

		s3.Line(point1=(- ltotal - l_offset, - htotal), point2=(- ltotal - lsq - l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(- ltotal - l_offset, - htotal), point2=(- ltotal - lsq - l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(- ltotal - (2*lsq) - (2*lhc) + l_offset, - htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(- ltotal - (2*lsq) - (2*lhc) + l_offset, - htotal), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal + hhc - thc))
		s3.Line(point1=(- ltotal - lsq - l_offset2, - htotal - hhc + thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal - hhc + thc))
		s3.Line(point1=(- ltotal - lsq - l_offset2, - htotal + hhc - thc), point2=(- ltotal - (lsq) - (2*lhc) + l_offset2, - htotal + hhc - thc))
	
		ltotal = ltotal + (2*lsq) + (4*lhc)

		countx = countx + 1

p = model.Part(name='Filling', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_fill = model.parts['Filling']
part_fill.BaseSolidExtrude(sketch=s3, depth=hfill)
s3.unsetPrimaryObject()
del model.sketches['__profile__']

thc = 2*thc - 0.0002

# MATERIALS ----------------------------------

# - Steel -
model.Material(name='S-275-JC')
mat_steel = model.materials['S-275-JC']
mat_steel.Density(table=((7.85, ), ))
mat_steel.Elastic(table=((210000000.0, 0.3), 
    ))
mat_steel.Plastic(hardening=JOHNSON_COOK, 
    table=((275000.0, 50000.0, 0.4, 1.0, 0.0, 0.0), ))

# - Aluminium -
model.Material(name='AA7075-JC')
mat_alum = model.materials['AA7075-JC']
mat_alum.Density(table=((2.70, ), ))
mat_alum.Elastic(table=((70000000.0, 0.3), 
    ))
mat_alum.Plastic(hardening=JOHNSON_COOK, 
    table=((520000.0, 477000.0, 0.52, 1.0, 0.0, 0.0), ))
mat_alum.plastic.RateDependent(
    type=JOHNSON_COOK, table=((0.001, 0.0005), ))

# - Ultramide -
model.Material(name='Ultramide')
mat_ultramide = model.materials['Ultramide']
mat_ultramide.Density(table=((1.55, ), ))
mat_ultramide.Elastic(table=((10160000.0, 0.4), 
    ))
mat_ultramide.Plastic(table=((254000.0, 0.0), ))
mat_ultramide.DuctileDamageInitiation(table=((
    0.026, 1.0, 1.0), ))
mat_ultramide.ductileDamageInitiation.DamageEvolution(
    type=DISPLACEMENT, table=((0.0, ), ))

# - GFRP

model.Material(name='GFRP')
mat_gfrp = model.materials['GFRP']
mat_gfrp.Density(table=((1.55, ), ))
mat_gfrp.Elastic(table=((16247251.141291289, 0.4), 
    ))
mat_gfrp.Plastic(hardening=USER, table=((25000.0, ), (
    0.0, ), (124866.828374, ), (44221.2086877, ), (315.896358458, ), (
    5748.46332314, ), (0.0, ), (3.25E-5, )))
mat_gfrp.DuctileDamageInitiation(table=((0.0111019107183, 
    0.33, 3.25E-5), ))
mat_gfrp.ductileDamageInitiation.DamageEvolution(
    type=DISPLACEMENT, table=((0.0, ), ))

# - ALUM 2

model.Material(name='ALUM')
mat_alum2 = model.materials['ALUM']
mat_alum2.Density(table=((2.70, ), ))
mat_alum2.Elastic(table=((70000000.0, 0.3), 
    ))
mat_alum2.Plastic(hardening=USER, table=((520000.0, ), (
    477000, ), (0.0005, ), (0.52, ), (0.001, )))

# - Foam - 

# model.Material(name='ArmaFORM')
# mat_foam = model.materials['ArmaFORM']
# mat_foam.Density(table=((0.135, ), ))
# mat_foam.Elastic(table=((90000.0, 0.1), ))
# mat_foam.CrushableFoam(table=((1.1, 1.0), ))
# mat_foam.crushableFoam.CrushableFoamHardening(
#     table=((2300, 0.0), ))
# model.Material(name='ArmaFORM')
# mat_foam = model.materials['ArmaFORM']
# mat_foam.Density(table=((0.135, ), ))
# mat_foam.Elastic(table=((61686.5758, 0.1), ))
# mat_foam.CrushableFoam(hardening=ISOTROPIC, table=((1.0, 0.1), ))
# mat_foam.crushableFoam.CrushableFoamHardening(table=((2540,0.00),
# (2500, 0.41824335), (2475, 0.5), (910000, 0.860068),
# ))

model.Material(name='ArmaFORM')
mat_foam = model.materials['ArmaFORM']
mat_foam.Density(table=((0.135, ), ))
mat_foam.Elastic(table=((59006, 0.1), ))
mat_foam.CrushableFoam(hardening=ISOTROPIC, table=((0.6862, 0.1109181), ))
mat_foam.crushableFoam.CrushableFoamHardening(table=(
(2550, 0.0),
(2551, 0.006464146),
(2555,0.38054),
(2685,0.60697),
(2863,0.7678),
(3190, 0.92351),
(4142, 1.10342),
(5094, 1.23),
(90000000, 40), ))

# SECTIONS ------------------------------------

model.HomogeneousShellSection(name='Sect-HC', preIntegrate=OFF, 
    material='Ultramide', thicknessType=UNIFORM, thickness=thc, 
    thicknessField='', idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=3)
model.HomogeneousShellSection(name='Sect-Tube', 
    preIntegrate=OFF, material='ALUM', thicknessType=UNIFORM, 
    thickness=ttube, thicknessField='', idealization=NO_IDEALIZATION, 
    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
    useDensity=OFF, integrationRule=SIMPSON, numIntPts=3)
model.HomogeneousSolidSection(name='Section-Fil', 
    material='ArmaFORM', thickness=None)


# SECTION ASSIGNMENT ----------------------------

f_tube = part_tube.faces
nfaces_tube = len(f_tube)
faces_tube = f_tube[0:nfaces_tube]
region_tube = part_tube.Set(faces=faces_tube, name='Set-Tube-Faces')
part_tube.SectionAssignment(region=region_tube, sectionName='Sect-Tube', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

c_fill = part_fill.cells
ncells_fil = len(c_fill)
cells_fil = c_fill[0:ncells_fil]
region_fil = part_fill.Set(cells=cells_fil, name='Set-Fil-Faces')
part_fill.SectionAssignment(region=region_fil, sectionName='Section-Fil',  offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)


f_top = part_top.faces
nfaces_top = len(f_top)
faces_top = f_top[0:nfaces_top]
region_top = part_top.Set(faces=faces_top, name='Set-Top-Faces')
part_top.SectionAssignment(region=region_top, sectionName='Sect-Tube', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

f_hc = part_hc.faces
nfaces_hc = len(f_hc)
faces_hc = f_hc[0:nfaces_hc]
region_hc = part_hc.Set(faces=faces_hc, name='Set-HC-Faces')
part_hc.SectionAssignment(region=region_hc, sectionName='Sect-HC', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

f_cover = part_cover.faces
nfaces_cover = len(f_cover)
faces_cover = f_cover[0:nfaces_cover]
pickedRegions =(faces_cover, )

f_cover_imp = part_cover_imp.faces
nfaces_cover_imp = len(f_cover_imp)
faces_cover_imp = f_cover[0:nfaces_cover_imp]
pickedRegions =(faces_cover_imp, )

f_sph = part_sph.faces
nfaces_sph = len(f_sph)
faces_sph = f_cover[0:nfaces_sph]

# ASSEMBLY ------------------------------------

a = model.rootAssembly
a.Instance(name='Cover-1', part=part_cover, dependent=ON)
a.Instance(name='HC-1', part=part_hc, dependent=ON)
a.Instance(name='Tube-1', part=part_tube, dependent=ON)
a.Instance(name='Cover-IMP', part=part_cover, dependent=ON)
#a.Instance(name='Sphere', part=part_sph, dependent=ON)
a.Instance(name='Filling', part=part_fill, dependent=ON)
# a.Instance(name='Top', part=part_top, dependent=ON)
# a.Instance(name='Bottom', part=part_top, dependent=ON)
a.translate(instanceList=('Cover-IMP', ), vector=(0.0, 0.0, (dtube+.0001+(ttube))))
a.translate(instanceList=('Cover-1', ), vector=(0.0, 0.0, (-.0002-ttube)))
# a.translate(instanceList=('Top', ), vector=(0.0, 0.0, (dtube+(ttube/2)+0.0001)))
# a.translate(instanceList=('Bottom', ), vector=(0.0, 0.0, (-.0001-(ttube/2))))



# REF. POINTS -----------------------------------

e1 = a.instances['Cover-1'].edges
myRP1 = a.ReferencePoint(point=a.instances['Cover-1'].InterestingPoint(edge=e1[0], rule=CENTER))
e11 = a.instances['Cover-IMP'].edges
myRP2 = a.ReferencePoint(point=a.instances['Cover-IMP'].InterestingPoint(edge=e11[0], rule=CENTER))
refPoints = a.referencePoints

refPoints1=(refPoints[11], )
refPoints2=(refPoints[12], )

region_rp1 = a.Set(referencePoints=refPoints1, name='Set-rp1')
region_rp2 = a.Set(referencePoints=refPoints2, name='Set-rp2')

model.rootAssembly.engineeringFeatures.PointMassInertia(
    name='Inertia-RP2', region=region_rp2, mass=impactmass, i11=1000.0, i22=1000.0, 
    i33=1000.0, alpha=0.0, composite=0.0)


# BC ---------------------------------------------

model.EncastreBC(name='Encastre', createStepName='Initial', 
    region=region_rp1, localCsys=None)
model.TabularAmplitude(name='Amplitude', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (steptime, 1.0)))



# PREDEF. FIELDS ----------------------------------

# model.Velocity(name='InitialVelocity', region=region_rp2, field='', 
#    distributionType=MAGNITUDE, velocity1=0.0, velocity2=0.0, velocity3=-impact_velocity, 
#    omega=0.0)


# MESH --------------------------------------------

# - TUBE -
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT, 
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
pickedRegions =(faces_tube, )
part_tube.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part_tube.seedPart(size=msizetube, deviationFactor=0.1, minSizeFactor=0.1)
part_tube.generateMesh()

# - TOP - 

elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT, 
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
pickedRegions =(faces_top, )
part_top.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part_top.seedPart(size=msizetube, deviationFactor=0.1, minSizeFactor=0.1)
part_top.generateMesh()

# - HC -
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT, 
     kinematicSplit=ORTHOGONAL, secondOrderAccuracy=OFF, 
    hourglassControl=ENHANCED, distortionControl=ON, elemDeletion=ON, 
    maxDegradation=0.2)
elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
pickedRegions =(faces_hc, )
part_hc.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part_hc.seedPart(size=msizehc, deviationFactor=0.1, minSizeFactor=0.1)
part_hc.generateMesh()

# - COVER -
elemType1 = mesh.ElemType(elemCode=R3D4, elemLibrary=EXPLICIT)
elemType2 = mesh.ElemType(elemCode=R3D3, elemLibrary=EXPLICIT)
pickedRegions =(faces_cover, )
part_cover.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part_cover.seedPart(size=0.028, deviationFactor=0.1, minSizeFactor=0.1)
part_cover.generateMesh()

# - SPHERE -
elemType1 = mesh.ElemType(elemCode=R3D4, elemLibrary=EXPLICIT)
elemType2 = mesh.ElemType(elemCode=R3D3, elemLibrary=EXPLICIT)
pickedRegions =(faces_sph, )
part_sph.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part_sph.seedPart(size=0.001, deviationFactor=0.1, minSizeFactor=0.1)
part_sph.generateMesh()

# - FILLING

elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
hourglassControl=COMBINED, weightFactor=0.5, distortionControl=ON, lengthRatio=0.2)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
part_fill.setElementType(regions=region_fil, elemTypes=(elemType1, elemType2, 
      elemType3))
part_fill.seedPart(size=msizefil, deviationFactor=0.1, minSizeFactor=0.5)
part_fill.generateMesh()

# RP-COVER ------------------------------------

f1 = a.instances['Cover-1'].faces
faces1 = f1[0:1]
region2=a.Set(faces=faces1, name='Rigid-1')
model.RigidBody(name='Constraint-CV1', refPointRegion=region_rp1, 
    bodyRegion=region2)

f1 = a.instances['Cover-IMP'].faces
faces1 = f1[0:1]
region2=a.Set(faces=faces1, name='Rigid-2')
model.RigidBody(name='Constraint-CV2', refPointRegion=region_rp2, 
    bodyRegion=region2)

# STEP -------------------------------------------

model.ExplicitDynamicsStep(name='ForceCollapse', previous='Initial', 
    timePeriod=.001)

e1 = a.instances['Tube-1'].edges
v1 = a.instances['Tube-1'].vertices
edges1 = e1.findAt(((-ltube/2, -0.0125, 0.49), ), ((ltube/2, -0.0375, 0.49), ), ((
    -0.0375, -ltube/2, 0.49), ), ((-0.0125, ltube/2, 0.49), ), ((-ltube/2, 0.0375, 
    0.49), ), ((0.0125, -ltube/2, 0.49), ), ((ltube/2, 0.0125, 0.49), ), ((0.0375, 
    ltube/2, 0.49), ))
region = a.Set(edges=edges1, name='Set-encastre-top')
model.EncastreBC(name='Encastre_Top', 
    createStepName='ForceCollapse', region=region, localCsys=None)
model.TabularAmplitude(name='Amp-2', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.001, 1.0)))

edges1 = e1.findAt(((0.0025, ltube/2, 0.5), ), ((-0.0075, ltube/2, 0.5), ))
region = a.Set(edges=edges1, name='Set-11')
mdb.models['HC'].DisplacementBC(name='disp1', createStepName='ForceCollapse', 
    region=region, u1=UNSET, u2=0.002, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude='Amp-2', fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
edges1 = e1.findAt(((0.0075, -ltube/2, 0.5), ), ((-0.0025, -ltube/2, 0.5), ))
region = a.Set(edges=edges1, name='Set-12')
mdb.models['HC'].DisplacementBC(name='disp2', createStepName='ForceCollapse', 
    region=region, u1=UNSET, u2=-0.002, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude='Amp-2', fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
edges1 = e1.findAt(((-ltube/2, 0.0025, 0.5), ), ((-ltube/2, -0.0075, 0.5), ))
region = a.Set(edges=edges1, name='Set-13')
mdb.models['HC'].DisplacementBC(name='disp3', createStepName='ForceCollapse', 
    region=region, u1=0.002, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude='Amp-2', fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1.1494, 
    farPlane=1.64825, width=0.173532, height=0.13107, viewOffsetX=-0.0746414, 
    viewOffsetY=-0.0540726)
edges1 = e1.findAt(((ltube/2, 0.0075, 0.5), ), ((ltube/2, -0.0025, 0.5), ))
region = a.Set(edges=edges1, name='Set-14')
mdb.models['HC'].DisplacementBC(name='disp4', createStepName='ForceCollapse', 
    region=region, u1=-0.002, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude='Amp-2', fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
verts1 = v1.findAt(((ltube/2, -ltube/2, 0.5), ), ((ltube/2, -ltube/2, 0.0), ), ((ltube/2, ltube/2, 0.5), ), ((ltube/2, ltube/2, 0.0), ), ((-ltube/2, -ltube/2, 0.5), ), ((-ltube/2, -ltube/2, 0.0), ), ((-ltube/2, ltube/2, 0.5), ), ((-ltube/2, ltube/2, 0.0), ))
region = a.Set(vertices=verts1, name='Set-15')
mdb.models['HC'].DisplacementBC(name='point', createStepName='ForceCollapse', 
    region=region, u1=0.0, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

model.ExplicitDynamicsStep(name='Impact', previous='ForceCollapse', 
    timePeriod=steptime)
model.fieldOutputRequests['F-Output-1'].setValues(variables=('STATUS', 'U', 'S'), numIntervals=noutput)

e1 = a.instances['Tube-1'].edges
edges1 = e1.findAt(((-ltube/2, -0.0375, 0.5), ), ((ltube/2, -0.0125, 0.5), ), ((
    -0.0125, -ltube/2, 0.5), ), ((-0.0375, ltube/2, 0.5), ), ((-ltube/2, 0.0125, 0.5), 
    ), ((0.0125, ltube/2, 0.5), ), ((ltube/2, 0.0375, 0.5), ), ((0.0375, -ltube/2, 0.5), 
    ))
region = a.Set(edges=edges1, name='Set-10')
mdb.models['HC'].DisplacementBC(name='BC-7', createStepName='ForceCollapse', 
    region=region, u1=UNSET, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Impact')
# model.boundaryConditions['BC-7'].deactivate('Impact')

model.boundaryConditions['disp1'].deactivate('Impact')
model.boundaryConditions['disp2'].deactivate('Impact')
model.boundaryConditions['disp3'].deactivate('Impact')
model.boundaryConditions['disp4'].deactivate('Impact')
model.boundaryConditions['Encastre_Top'].deactivate('Impact')
model.boundaryConditions['BC-7'].deactivate('Impact')

Set_RP2=a.sets['Set-rp2']
model.HistoryOutputRequest(name='rp2', createStepName='Impact', 
    variables=('A3', 'U3'), numIntervals=600, 
    region=Set_RP2, sectionPoints=DEFAULT, rebar=EXCLUDE)

Set_RP1=a.sets['Set-rp1']
model.HistoryOutputRequest(name='rp1', createStepName='Impact', 
    variables=('RF3', ), numIntervals=600, region=Set_RP1, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

model.DisplacementBC(name='Displacement', createStepName='Impact', 
    region=region_rp2, u1=0.0, u2=0.0, u3=-delta, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude='Amplitude', fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

model.fieldOutputRequests['F-Output-1'].setValues(numIntervals=2)
model.fieldOutputRequests['F-Output-1'].setValuesInStep(
    stepName='Impact', numIntervals=noutput)


#model.steps['Impact'].AdaptiveMeshDomain(region=region_fil,
#    controls=None)
#model.steps['Impact'].adaptiveMeshDomains['Impact'].setValues(
#    frequency=10, meshSweeps=3)
#model.AdaptiveMeshControl(name='Ada-1', smoothingPriority=UNIFORM,
#    volumetricSmoothingWeight=1.0, equipotentialSmoothingWeight=0.0, momentumAdvection=HALF_INDEX_SHIFT)
#model.steps['Impact'].adaptiveMeshDomains['Impact'].setValues(
#    controls='Ada-1')
# INTERACTION ----------------------------------------

model.ContactProperty('IntProp-1')
model.interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    0.057, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
    fraction=0.005, elasticSlipStiffness=None)
model.interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
model.ContactExp(name='Interaction', createStepName='Initial')
model.interactions['Interaction'].includedPairs.setValuesInStep(
    stepName='Initial', useAllstar=ON)
model.interactions['Interaction'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))

# MASS -----------------------------------------------

mass = model.rootAssembly.getMassProperties()['mass']*1000 # Mass of model in kg

mass = mass - ( impactmass * 1000)  # Mass of piece in kg

ResultadoMasa = open('resultado.mass','w')
ResultadoMasa.write('%-E' % float(mass))
ResultadoMasa.close()

# JOB -----------------------------------                                   

job = mdb.Job(name='HC', model='HC', description='', type=ANALYSIS, 
    echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='/home/jpaz/phd/prueba2/cd prueba2prueba8/v_ALUM3.f',)
    
job.writeInput() 
