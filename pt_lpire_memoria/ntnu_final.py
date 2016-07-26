from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=234.330017089844, 
    height=202.0537109375)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()


lado = 0.1
# ladohex = lado/2
ladohex = 0.0667

aleta = 0.02
espesor = 0.001
longitud = 0.35
longcomp = 0.345
pasopuntos = 0.03
sepcordones = 0.01

mallaal=0.004

tcomp = 0.0025

# Dimensiones GFPR
#longitud definida arriba
anchocomp = 0.128
surco = tcomp*sqrt(3)

delta = 0.25
velocidad = 15.  # velocidad en m/s

steptime = delta/velocidad

geometria = 'hex'   # hex / cuad

trigger = 'SIM'   # SIM ANTIM
dtrigger = 0.003
s30 = 0.5
c30 = cos(30*pi/180)

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(ladohex/2, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(ladohex/2, 0.0), point2=(ladohex, ladohex*0.866025403784 - espesor/2))
s.Line(point1=(ladohex, ladohex*0.866025403784 - espesor/2), point2=(ladohex + aleta, ladohex*0.866025403784 - espesor/2))
s.HorizontalConstraint(entity=g[4], addUndoState=False)
s.Line(point1=(0.0, 0.0), point2=(0.0, 0.023143557831645))
s.VerticalConstraint(entity=g[5], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
s.copyMirror(mirrorLine=g[5], objectList=(g[2], g[3], g[4]))
s.delete(objectList=(g[5], ))
p = mdb.models['Model-1'].Part(name='Chapa', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Chapa']
p.BaseShellExtrude(sketch=s, depth=longitud)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Chapa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

p = mdb.models['Model-1'].parts['Chapa']
s = p.features['Shell extrude-1'].sketch
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['Model-1'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, 
    upToFeature=p.features['Shell extrude-1'], filter=COPLANAR_EDGES)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.39223, 
    farPlane=0.769408, width=0.140016, height=0.0666881, cameraPosition=(
    0.00133062, 0.0197941, 0.755819), cameraTarget=(0.00133062, 0.0197941, 0))
s1.delete(objectList=(g[6], c[16]))
s1.trimExtendCurve(curve1=g[2], point1=(0.00355016766116023, 
    -0.000465545803308487), curve2=g[7], point2=(-0.0351068116724491, 
    0.0019342303276062))
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Chapa']
p.features['Shell extrude-1'].setValues(sketch=s1)
del mdb.models['Model-1'].sketches['__edit__']
p = mdb.models['Model-1'].parts['Chapa']
p.regenerate()



s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(ladohex/2, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(ladohex/2, 0.0), point2=(ladohex, ladohex*0.866025403784))
s.Line(point1=(0.0, 0.0), point2=(0.0, 0.0287604592740536))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)
s.copyMirror(mirrorLine=g[4], objectList=(g[2], g[3]))
s.Line(point1=(ladohex, ladohex*0.866025403784), point2=(0.0312079340219498, 
    ladohex*0.866025403784))
s.HorizontalConstraint(entity=g[7], addUndoState=False)
s.copyMirror(mirrorLine=g[7], objectList=(g[2], g[3], g[5], g[6]))
s.delete(objectList=(g[4], g[7], c[9]))
s.offset(distance=(espesor/2)+0.001, objectList=(g[2], g[3], g[5], g[6], g[8], g[9], 
    g[10], g[11]), side=RIGHT)
s.delete(objectList=(g[11], g[6], g[2], g[3], g[5], g[9], g[8], g[10]))
p = mdb.models['Model-1'].Part(name='espuma_hex', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['espuma_hex']
p.BaseSolidExtrude(sketch=s, depth=longitud)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['espuma_hex']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(longcomp, 0.0))
s.Line(point1=(longcomp, 0.0), point2=(longcomp, (anchocomp/2)-(surco/2)))
s.Line(point1=(longcomp, (anchocomp/2)-(surco/2)), point2=(longcomp/3, (anchocomp/2)-(surco/2)))
s.Line(point1=(longcomp/3, (anchocomp/2)-(surco/2)), point2=(longcomp/3, (anchocomp/2)+(surco/2)))
s.Line(point1=(longcomp/3, (anchocomp/2)+(surco/2)), point2=(longcomp, (anchocomp/2)+(surco/2)))
s.Line(point1=(longcomp, (anchocomp/2)+(surco/2)), point2=(longcomp, anchocomp))
s.Line(point1=(longcomp, anchocomp), point2=(0.0, anchocomp))
s.Line(point1=(0.0, anchocomp), point2=(0.0, 0.0))
p = mdb.models['Model-1'].Part(name='GFRP_U', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['GFRP_U']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['GFRP_U']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(longcomp, 0.0))
s.Line(point1=(longcomp, 0.0), point2=(longcomp, (anchocomp/2)-(surco/2)))
s.Line(point1=(longcomp, (anchocomp/2)-(surco/2)), point2=(2*longcomp/3, (anchocomp/2)-(surco/2)))
s.Line(point1=(2*longcomp/3, (anchocomp/2)-(surco/2)), point2=(2*longcomp/3, (anchocomp/2)+(surco/2)))
s.Line(point1=(2*longcomp/3, (anchocomp/2)+(surco/2)), point2=(longcomp, (anchocomp/2)+(surco/2)))
s.Line(point1=(longcomp, (anchocomp/2)+(surco/2)), point2=(longcomp, anchocomp))
s.Line(point1=(longcomp, anchocomp), point2=(0.0, anchocomp))
s.Line(point1=(0.0, anchocomp), point2=(0.0, (anchocomp/2)+(surco/2)))
s.Line(point1=(0.0, (anchocomp/2)+(surco/2)), point2=(longcomp/3, (anchocomp/2)+(surco/2)))
s.Line(point1=(longcomp/3, (anchocomp/2)+(surco/2)), point2=(longcomp/3, (anchocomp/2)-(surco/2)))
s.Line(point1=(longcomp/3, (anchocomp/2)-(surco/2)), point2=(0.0, (anchocomp/2)-(surco/2)))
s.Line(point1=(0.0, (anchocomp/2)-(surco/2)), point2=(0.0, 0.0))
p = mdb.models['Model-1'].Part(name='GFRP_H', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['GFRP_H']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['GFRP_H']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']



# mdb.models['Model-1'].Material(name='AA5754H111_bl')
# mdb.models['Model-1'].materials['AA5754H111_bl'].Density(table=((2.56, ), ))
# mdb.models['Model-1'].materials['AA5754H111_bl'].Elastic(table=((70000000.0, 
#     0.33), ))
# mdb.models['Model-1'].materials['AA5754H111_bl'].Plastic(table=((139000.0, 
#     0.0), (227000.0, 0.226)))

mdb.models['Model-1'].Material(name='AA5754_JC')
mdb.models['Model-1'].materials['AA5754_JC'].Density(table=((2.56, ), ))
mdb.models['Model-1'].materials['AA5754_JC'].Elastic(table=((70000000.0, 0.33), 
    ))
mdb.models['Model-1'].materials['AA5754_JC'].Plastic(hardening=JOHNSON_COOK, 
    table=((67456.0, 471242.0, 0.424, 0.0, 0.0, 0.0), ))
mdb.models['Model-1'].materials['AA5754_JC'].plastic.RateDependent(
    type=JOHNSON_COOK, table=((0.003, 0.0033), ))


mdb.models['Model-1'].HomogeneousShellSection(name='sec1mm', preIntegrate=OFF, 
    material='AA5754_JC', thicknessType=UNIFORM, thickness=0.001, 
    thicknessField='', idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=5)

session.journalOptions.setValues(replayGeometry=INDEX, recoverGeometry=INDEX)

p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
faces = f[0:5]
region = regionToolset.Region(faces=faces)
p.SectionAssignment(region=region, sectionName='sec1mm', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='Chapa-1', part=p, dependent=ON)
a.Instance(name='Chapa-2', part=p, dependent=ON)
a.translate(instanceList=('Chapa-2', ), vector=(2*ladohex + 2*aleta, 0.0, 0.0))
a.rotate(instanceList=('Chapa-2', ), axisPoint=(2*ladohex + aleta, ladohex*0.866025403784 - espesor/2, longitud), 
    axisDirection=(0.0, 0.0, -longitud), angle=-180.0)
a.translate(instanceList=('Chapa-2', ), vector=(-2*ladohex, 0.0, 0.0))
a.translate(instanceList=('Chapa-2', ), vector=(0.0, espesor, 0.0))



x = ladohex+aleta/2
y=ladohex*0.866025403784
z=0.005
while z <= longitud:
    a.ReferencePoint(point=(x, y, z))
    z=z+pasopuntos
x = -(ladohex+aleta/2)
y=ladohex*0.866025403784
z=0.005
while z <= longitud:
    a.ReferencePoint(point=(x, y, z))
    z=z+pasopuntos

puntosr=mdb.models['Model-1'].rootAssembly.referencePoints
npuntos = len(puntosr)
vpr=[]

for i in range(6, 6+npuntos):
    vpr.append(puntosr[i])

a1 = mdb.models['Model-1'].rootAssembly
a1.Set(referencePoints=vpr, name='Puntos_sol')

p = mdb.models['Model-1'].parts['Chapa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.15, 0.0))
p = mdb.models['Model-1'].Part(name='Placa', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Placa']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Placa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Placa']
a.Instance(name='Placa-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Placa-1', ), vector=(0.0, lado/2, 0.0))

a.LinearInstancePattern(instanceList=('Placa-1', ), direction1=(0.0, 0.0, 1.0), 
    direction2=(0.0, 1.0, 0.0), number1=2, number2=1, spacing1=longitud + 0.001, 
    spacing2=0.3)
mdb.models['Model-1'].ExplicitDynamicsStep(name='Impacto', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Impacto')

mdb.models['Model-1'].ContactProperty('IntProp-1')
mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    0.05, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
    fraction=0.005, elasticSlipStiffness=None)
mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
mdb.models['Model-1'].ContactExp(name='Int-1', createStepName='Initial')
mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
    stepName='Initial', useAllstar=ON)
mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, lado/2, 0.0))
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, lado/2, longitud + 0.001))

f1 = a.instances['Placa-1-lin-2-1'].faces
faces1 = f1[0:1]
region2=regionToolset.Region(faces=faces1)
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[36], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=region1, 
    bodyRegion=region2)
f1 = a.instances['Placa-1'].faces
faces1 = f1[0:1]
region2=regionToolset.Region(faces=faces1)
r1 = a.referencePoints
refPoints1=(r1[35], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, 
    bodyRegion=region2)
mdb.models['Model-1'].ConnectorSection(name='punto', assembledType=BUSHING)
elastic_0 = connectorBehavior.ConnectorElasticity(components=(1, 2, 3, 4, 5, 
    6), table=((210000000.0, 210000000.0, 210000000.0, 210000000.0, 
    210000000.0, 210000000.0), ))
elastic_0.ConnectorOptions()
mdb.models['Model-1'].sections['punto'].setValues(behaviorOptions =(elastic_0, 
    ) )
a = mdb.models['Model-1'].rootAssembly
region=a.sets['Puntos_sol']
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Chapa-1'].faces
side1Faces1 = s1[0:1]+s1[4:5]
s2 = a.instances['Chapa-2'].faces
side1Faces2 = s2[0:1]+s2[4:5]
tSurface1=regionToolset.Region(side1Faces=side1Faces1+side1Faces2)
targetSurface=(tSurface1, )
datum1 = mdb.models['Model-1'].rootAssembly.datums[1]
# mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointFastener(
#     name='punto_sol', region=region, targetSurfaces=targetSurface, 
#     sectionName='punto', connectorOrientationLocalCsys1=datum1, 
#     physicalRadius=0.04, unsorted=OFF)

a2 = mdb.models['Model-1'].rootAssembly
r1 = a2.referencePoints
refPoints1=(r1[36], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)

mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
a2 = mdb.models['Model-1'].rootAssembly
r1 = a2.referencePoints
refPoints1=(r1[35], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='BC-3', createStepName='Impacto', 
    region=region, u1=0.0, u2=0.0, u3=delta + 0.001, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=500)


p = mdb.models['Model-1'].parts['Chapa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Chapa']
p.seedPart(size=mallaal, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Chapa']
p.generateMesh()
p = mdb.models['Model-1'].parts['Placa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Placa']
p.seedPart(size=0.042, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Placa']
p.generateMesh()
p = mdb.models['Model-1'].parts['Chapa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)

elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT, 
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
faces = f[0:5]
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
a3 = mdb.models['Model-1'].rootAssembly
a3.regenerate()

mdb.models['Model-1'].steps['Impacto'].setValues(timePeriod=steptime)
mdb.models['Model-1'].amplitudes['Amp-1'].setValues(timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (steptime, 1.0)))



a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Placa-1-lin-2-1', ), vector=(0.0, 0.0, -0.001))

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Placa-1', ), vector=(0.0, 0.0, -0.001))

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Placa-1-lin-2-1', ), vector=(0.0, 0.0, 0.00001))


mdb.models['Model-1'].Material(name='ArmaFORM')
mdb.models['Model-1'].materials['ArmaFORM'].Density(table=((0.135, ), ))
mdb.models['Model-1'].materials['ArmaFORM'].Elastic(table=((90000.0, 0.1), ))
mdb.models['Model-1'].materials['ArmaFORM'].CrushableFoam(table=((1.1, 1.0), ))
mdb.models['Model-1'].materials['ArmaFORM'].crushableFoam.CrushableFoamHardening(
    table=((2300, 0.0), ))


mdb.models['Model-1'].HomogeneousSolidSection(name='sec_espuma', 
    material='ArmaFORM', thickness=None)



    # a = mdb.models['Model-1'].rootAssembly
    # region=a.sets['Puntos_sol']
    # a = mdb.models['Model-1'].rootAssembly
    # s1 = a.instances['Chapa-2'].faces
    # side1Faces1 = s1[0:2]
    # s2 = a.instances['Chapa-1'].faces
    # side1Faces2 = s2[0:2]
    # tSurface1=regionToolset.Region(side1Faces=side1Faces1+side1Faces2)
    # targetSurface=(tSurface1, )
    # mdb.models['Model-1'].rootAssembly.engineeringFeatures.fasteners['punto_sol'].setValues(
    #     region=region, targetSurfaces=targetSurface)
    # a = mdb.models['Model-1'].rootAssembly
    # s1 = a.instances['Chapa-2'].faces
    # side1Faces1 = s1[0:1]+s1[4:5]
    # s2 = a.instances['Chapa-1'].faces
    # side1Faces2 = s2[0:1]+s2[4:5]
    # tSurface1=regionToolset.Region(side1Faces=side1Faces1+side1Faces2)
    # targetSurface=(tSurface1, )
    # mdb.models['Model-1'].rootAssembly.engineeringFeatures.fasteners['punto_sol'].setValues(
    #     targetSurfaces=targetSurface)

a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['espuma_hex']
a1.Instance(name='espuma_hex-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['espuma_hex']
c = p.cells
cells = c[0:1]
region = regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['espuma_hex']
p.SectionAssignment(region=region, sectionName='sec_espuma', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p.seedPart(size=0.005, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=ON, 
    lengthRatio=0.100000001490116)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
c = p.cells
cells = c[0:1]
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
    'RF', 'SF', 'CSTRESS', 'EVF'))




a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['espuma_hex']
v = p.vertices
d = p.datums
c = p.cells
f = p.faces
p.DatumPlaneByThreePoints(point1=v[8], point2=v[5], point3=v[4])
p.DatumPlaneByThreePoints(point1=v[6], point2=v[14], point3=v[15])
p.DatumPlaneByThreePoints(point1=v[1], point2=v[11], point3=v[12])
p.DatumPlaneByOffset(plane=d[5], flip=SIDE1, offset=tcomp/2)
p.DatumPlaneByOffset(plane=d[5], flip=SIDE2, offset=tcomp/2)
p.DatumPlaneByOffset(plane=d[6], flip=SIDE2, offset=tcomp/2)
p.DatumPlaneByOffset(plane=d[6], flip=SIDE1, offset=tcomp/2)
p.DatumPlaneByOffset(plane=d[7], flip=SIDE1, offset=tcomp/2)
p.DatumPlaneByOffset(plane=d[7], flip=SIDE2, offset=tcomp/2)

pickedRegions = c[0:1]
p.deleteMesh(regions=pickedRegions)

pickedCells = c[0:1]
p.PartitionCellByDatumPlane(datumPlane=d[11], cells=pickedCells)
pickedCells = c[1:2]
p.PartitionCellByDatumPlane(datumPlane=d[10], cells=pickedCells)
pickedCells = c[1:2]
p.PartitionCellByDatumPlane(datumPlane=d[13], cells=pickedCells)
pickedCells = c[2:3]
p.PartitionCellByDatumPlane(datumPlane=d[12], cells=pickedCells)
pickedCells = c[3:4]
p.PartitionCellByDatumPlane(datumPlane=d[8], cells=pickedCells)
pickedCells = c[4:5]
p.PartitionCellByDatumPlane(datumPlane=d[9], cells=pickedCells)
pickedCells = c[6:7]
p.PartitionCellByDatumPlane(datumPlane=d[12], cells=pickedCells)
pickedCells = c[7:8]
p.PartitionCellByDatumPlane(datumPlane=d[13], cells=pickedCells)
pickedCells = c[0:1]
p.PartitionCellByDatumPlane(datumPlane=d[8], cells=pickedCells)
pickedCells = c[1:2]
p.PartitionCellByDatumPlane(datumPlane=d[9], cells=pickedCells)

p.RemoveFaces(faceList = f[56:57], deleteCells=False)
p.RemoveFaces(faceList = f[42:43]+f[49:50]+f[51:53], deleteCells=False)
p.RemoveFaces(faceList = f[36:37]+f[49:50], deleteCells=False)
p.RemoveFaces(faceList = f[46:47], deleteCells=False)
p.RemoveFaces(faceList = f[21:22]+f[24:25]+f[26:27], deleteCells=False)
p.RemoveFaces(faceList = f[37:38], deleteCells=False)
p.RemoveFaces(faceList = f[4:5], deleteCells=False)
p.RemoveFaces(faceList = f[5:6]+f[12:13]+f[15:16]+f[41:42], 
    deleteCells=False)
p.RemoveFaces(faceList = f[11:12]+f[14:15]+f[21:22]+f[27:28]+f[34:35], 
    deleteCells=False)
p.RemoveFaces(faceList = f[8:9]+f[22:23]+f[33:34], deleteCells=False)
p.RemoveFaces(faceList = f[25:26]+f[30:31], deleteCells=False)
p.RemoveFaces(faceList = f[8:9], deleteCells=False)





from material import createMaterialFromDataString
createMaterialFromDataString('Model-1', 'Ultramid A3WG10', '6-13', 
    """{'name': 'Ultramid A3WG10', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((10160000.0, 0.4),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((1.55,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((254000.0, 0.0),), 'numBackstresses': 1}, 'materialIdentifier': '', 'ductileDamageInitiation': {'temperatureDependency': OFF, 'direction': NMORI, 'dependencies': 0, 'table': ((0.026, 1.0, 1.0),), 'alpha': 0.0, 'omega': 1.0, 'definition': MSFLD, 'fnt': 10.0, 'damageEvolution': {'temperatureDependency': OFF, 'dependencies': 0, 'softening': LINEAR, 'power': None, 'table': ((0.0,),), 'mixedModeBehavior': MODE_INDEPENDENT, 'type': DISPLACEMENT, 'modeMixRatio': ENERGY, 'degradation': MAXIMUM}, 'ks': 0.0, 'frequency': 1, 'feq': 10.0, 'fnn': 10.0, 'tolerance': 0.05, 'numberImperfections': 4}, 'description': ''}""")
mdb.models['Model-1'].HomogeneousShellSection(name='sec_gfrp', 
    preIntegrate=OFF, material='Ultramid A3WG10', thicknessType=UNIFORM, 
    thickness=tcomp, thicknessField='', idealization=NO_IDEALIZATION, 
    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
    useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)

p = mdb.models['Model-1'].parts['GFRP_H']
f = p.faces
faces = f[0:1]
region = regionToolset.Region(faces=faces)
p.SectionAssignment(region=region, sectionName='sec_gfrp', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['GFRP_U']
f = p.faces
faces = f[0:1]
region = regionToolset.Region(faces=faces)
p.SectionAssignment(region=region, sectionName='sec_gfrp', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)


v11 = a.instances['espuma_hex-1'].vertices
a.DatumPointByMidPoint(point1=v11[35], point2=v11[5])


mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
    'RF', 'SF', 'CSTRESS', 'EVF', 'STATUS'))

p = mdb.models['Model-1'].parts['espuma_hex']
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=0.15)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
p = mdb.models['Model-1'].parts['espuma_hex']
c = p.cells
cells = c[0:6]
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))



a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
p = mdb.models['Model-1'].parts['espuma_hex']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['espuma_hex']
p.deleteMesh()
p = mdb.models['Model-1'].parts['espuma_hex']
p.seedPart(size=0.01, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['espuma_hex']
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=0.25)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
p = mdb.models['Model-1'].parts['espuma_hex']
c = p.cells
cells = c[0:6]
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
a.regenerate()
a.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.3)
p = mdb.models['Model-1'].parts['espuma_hex']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Chapa']
a = mdb.models['Model-1'].rootAssembly
a = mdb.models['Model-1'].rootAssembly
del a.features['Datum plane-1']
p = mdb.models['Model-1'].parts['Chapa']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.3)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedRegions = f[0:5]
p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedFaces = f[0:5]
d = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d[5], faces=pickedFaces)
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Chapa-2'].faces
faces1 = f1[0:4]+f1[5:6]
f2 = a.instances['Chapa-1'].faces
faces2 = f2[0:4]+f2[5:6]
region = regionToolset.Region(faces=faces1+faces2)
mdb.models['Model-1'].DisplacementBC(name='Clamp', createStepName='Impacto', 
    region=region, u1=0.0, u2=0.0, u3=UNSET, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
p = mdb.models['Model-1'].parts['Chapa']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Chapa']
p.generateMesh()





a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Chapa-1'].faces
side1Faces1 = s1[4:5]
region1=regionToolset.Region(side1Faces=side1Faces1)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Chapa-2'].faces
side1Faces1 = s1[9:10]
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Tie(name='laser', master=region1, slave=region2, 
    positionToleranceMethod=COMPUTED, adjust=OFF, tieRotations=ON, 
    thickness=ON)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Chapa-1'].faces
side1Faces1 = s1[9:10]
region1=regionToolset.Region(side1Faces=side1Faces1)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Chapa-2'].faces
side1Faces1 = s1[4:5]
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Tie(name='Constraint-4', master=region1, slave=region2, 
    positionToleranceMethod=COMPUTED, adjust=OFF, tieRotations=ON, 
    thickness=ON)



a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['GFRP_U']
a1.Instance(name='GFRP_U-1', part=p, dependent=ON)
a1.rotate(instanceList=('GFRP_U-1', ), axisPoint=(0.0, 0.00051, 0.0), 
    axisDirection=(0.0, 0.12749, 0.0), angle=-90.0)
a1.translate(instanceList=('GFRP_U-1', ), vector=(0.0, -0.006236, 0.35))
a1.rotate(instanceList=('GFRP_U-1', ), axisPoint=(0.0, 0.057764, 0.465), 
    axisDirection=(0.0, 0.0, -0.115), angle=30.0)
a1.rotate(instanceList=('GFRP_U-1', ), axisPoint=(-0.032, 0.002338, 0.35), 
    axisDirection=(0.064, 0.110851, 0.0), angle=180.0)
a1.translate(instanceList=('GFRP_U-1', ), vector=(0.0, 0.0, -0.0001))
p = mdb.models['Model-1'].parts['GFRP_H']
a1.Instance(name='GFRP_H-1', part=p, dependent=ON)
a1.rotate(instanceList=('GFRP_H-1', ), axisPoint=(0.0, 0.128, 0.0), 
    axisDirection=(0.0, -0.128, 0.0), angle=90.0)
a1.translate(instanceList=('GFRP_H-1', ), vector=(0.0, -0.006236, 0.0049))
a1.rotate(instanceList=('GFRP_H-1', ), axisPoint=(0.0, 0.057764, 0.2349), 
    axisDirection=(0.0, 0.0, -0.115), angle=-30.0)
p = mdb.models['Model-1'].parts['GFRP_U']
a1.Instance(name='GFRP_U-2', part=p, dependent=ON)
a1.rotate(instanceList=('GFRP_U-2', ), axisPoint=(0.0, 0.128, 0.0), 
    axisDirection=(0.0, -0.128, 0.0), angle=90.0)
a1.translate(instanceList=('GFRP_U-2', ), vector=(0.0, -0.006236, 0.0049))
a1.rotate(instanceList=('GFRP_U-2', ), axisPoint=(0.0, 0.057764, 0.3499), 
    axisDirection=(0.0, 0.0, -0.23), angle=90.0)


p = mdb.models['Model-1'].parts['GFRP_H']
p.seedPart(size=0.03, deviationFactor=0.1, minSizeFactor=0.1)
p.seedPart(size=0.003, deviationFactor=0.1, minSizeFactor=0.1)
f = p.faces
pickedRegions = f[0:1]
p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
p.generateMesh()
p = mdb.models['Model-1'].parts['GFRP_U']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p.seedPart(size=0.003, deviationFactor=0.1, minSizeFactor=0.1)
f = p.faces
pickedRegions = f[0:1]
p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
p.generateMesh()

# mass scaling (solo qs)

a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Chapa-1'].faces
faces1 = f1[0:10]
f2 = a.instances['Chapa-2'].faces
faces2 = f2[0:10]
c3 = a.instances['espuma_hex-1'].cells
cells3 = c3[0:6]
a.Set(faces=faces1+faces2, cells=cells3, name='set-ms')
# #: The set 'set-ms' has been created (6 cells, 20 faces).
# regionDef0=mdb.models['Model-1'].rootAssembly.sets['set-ms']
# mdb.models['Model-1'].steps['Impacto'].setValues(massScaling=((SEMI_AUTOMATIC, 
#     regionDef0, AT_BEGINNING, 3.0, 0.0, None, 0, 0, 0.0, 0.0, 0, None), ))




# Trigger

# Onda completa
"""
ltrigger = 0.01
lsujeccion = 2*ltrigger

distborde = 0.1*ladohex
ratioentero = distborde/mallaal
ratiotrunc = round(ratioentero,0)
dtruncborde = ratiotrunc*mallaal
splitparam1 = 1 -dtruncborde/ladohex
splitparam2 = dtruncborde/(splitparam1*ladohex)

p = mdb.models['Model-1'].parts['Chapa']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=ltrigger)
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=lsujeccion)

p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedRegions = f[0:1]+f[4:10]
p.deleteMesh(regions=pickedRegions)
pickedFaces = f[4:5]+f[6:10]
d = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d[7], faces=pickedFaces)
pickedFaces = f[0:4]+f[9:10]
d1 = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d1[8], faces=pickedFaces)


p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedRegions = f[2:3]+f[17:18]
p.deleteMesh(regions=pickedRegions)
e = p.edges
pickedEdges = e[9:10]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam1)
pickedEdges = e[9:10]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam2)
pickedRegions = f[3:4]+f[18:19]
p.deleteMesh(regions=pickedRegions)
pickedEdges = e[14:15]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam1)
pickedEdges = e[14:15]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam2)
pickedRegions = f[1:2]+f[16:17]
p.deleteMesh(regions=pickedRegions)
pickedEdges = e[6:7]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam1)
pickedEdges = e[6:7]
p.PartitionEdgeByParam(edges=pickedEdges, parameter=splitparam2)
a = mdb.models['Model-1'].rootAssembly
a.regenerate()

p = mdb.models['Model-1'].parts['Chapa']
p.generateMesh()




mdb.models['Model-1'].ExplicitDynamicsStep(name='Trigger', previous='Initial', 
    timePeriod=0.02)

mdb.models['Model-1'].TabularAmplitude(name='Trig', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.02, 1.0)))

if trigger == 'SIM':
	a = mdb.models['Model-1'].rootAssembly
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[12:13]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_1', 
	    createStepName='Trigger', region=region, u1=UNSET, u2=-dtrigger, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[12:13]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_2', 
	    createStepName='Trigger', region=region, u1=UNSET, u2=dtrigger, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[7:8]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_3', 
	    createStepName='Trigger', region=region, u1=dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[17:18]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_4', 
	    createStepName='Trigger', region=region, u1=dtrigger*c30, u2=-dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[17:18]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_5', 
	    createStepName='Trigger', region=region, u1=-dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[7:8]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_6', 
	    createStepName='Trigger', region=region, u1=-dtrigger*c30, u2=-dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)

if trigger == 'ANTIM':
	a = mdb.models['Model-1'].rootAssembly
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[12:13]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_1', 
	    createStepName='Trigger', region=region, u1=UNSET, u2=-dtrigger, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[12:13]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_2', 
	    createStepName='Trigger', region=region, u1=UNSET, u2=-dtrigger, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[7:8]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_3', 
	    createStepName='Trigger', region=region, u1=dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[17:18]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_4', 
	    createStepName='Trigger', region=region, u1=-dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-2'].edges
	edges1 = e1[17:18]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_5', 
	    createStepName='Trigger', region=region, u1=-dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)
	e1 = a.instances['Chapa-1'].edges
	edges1 = e1[7:8]
	region = regionToolset.Region(edges=edges1)
	mdb.models['Model-1'].DisplacementBC(name='Trigger_6', 
	    createStepName='Trigger', region=region, u1=dtrigger*c30, u2=dtrigger*s30, u3=UNSET, 
	    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='Trig', fixed=OFF, 
	    distributionType=UNIFORM, fieldName='', localCsys=None)


a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Chapa-2'].edges
edges1 = e1[4:5]+e1[9:10]+e1[14:15]+e1[48:49]+e1[50:51]+e1[52:53]
e2 = a.instances['Chapa-1'].edges
edges2 = e2[4:5]+e2[9:10]+e2[14:15]+e2[48:49]+e2[50:51]+e2[52:53]
region = regionToolset.Region(edges=edges1+edges2)
mdb.models['Model-1'].PinnedBC(name='Trigger_SUJ', createStepName='Trigger', 
    region=region, localCsys=None)

mdb.models['Model-1'].boundaryConditions['Trigger_1'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_2'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_3'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_4'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_5'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_6'].deactivate('Impacto')
mdb.models['Model-1'].boundaryConditions['Trigger_SUJ'].deactivate('Impacto')

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].move('Impacto', 
    'Trigger')
mdb.models['Model-1'].historyOutputRequests['H-Output-1'].move('Impacto', 
    'Trigger')

a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[35], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].EncastreBC(name='BC-4', createStepName='Impacto', 
    region=region, localCsys=None)
mdb.models['Model-1'].boundaryConditions['BC-4'].move('Impacto', 'Trigger')
mdb.models['Model-1'].boundaryConditions['BC-4'].move('Trigger', 'Initial')
mdb.models['Model-1'].boundaryConditions['BC-4'].deactivate('Impacto')


"""

# Media onda

mdb.models['Model-1'].ExplicitDynamicsStep(name='Trigger', previous='Initial', 
    timePeriod=0.02)

mdb.models['Model-1'].TabularAmplitude(name='Trig', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.02, 1.0)))
    
ltrigger = 0.01
p = mdb.models['Model-1'].parts['Chapa']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=ltrigger)

p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedRegions = f[0:10]
p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedFaces = f[4:5]+f[6:10]
d = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d[7], faces=pickedFaces)


















mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=10)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(
    stepName='Impacto', numIntervals=500)






mdb.models['Model-1'].materials['ArmaFORM'].crushableFoam.crushableFoamHardening.setValues(
    table=((1100.0, 0.0), ))
mdb.models['Model-1'].materials['AA5754_JC'].JohnsonCookDamageInitiation(
    table=((0.0261, 0.263, 0.349, 0.147, 16.8, 0.0, 0.0, 0.0005), ))
mdb.models['Model-1'].materials['AA5754_JC'].johnsonCookDamageInitiation.DamageEvolution(
    type=DISPLACEMENT, table=((0.0, ), ))






# Modelado de cordones de soldadura

p = mdb.models['Model-1'].parts['Chapa']
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=ladohex+aleta/2-sepcordones/2)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=ladohex+aleta/2+sepcordones/2)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-ladohex-aleta/2-sepcordones/2)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-ladohex-aleta/2+sepcordones/2)