# Abaqus Python modules
from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from regionToolset import *
from odbAccess import *
from odbSection import *

import os
# os.chdir(r"C:\AbaqusTemp")

#---------------------------------------------------------------------------------------------
#Definicion de longitudes clave [m]
longlibre=0.1016
solape=0.0254
tr=0.002
ts=0.00013
ancho=0.0254

#Propiedades materiales [kN, m]
#Adhesivo
Poisson_ads=0.285
#matutil = 'Loctite EA 9514'
#matutil = 'Loctite EA 9514 Shear'
matutil = 'Loctite Hysol 9517'

#Adherente
E_adr=210000000.0
Poisson_adr=0.3

#Malla
tamanoads = 0.0005
tamanominadr = 0.0001
tamanomaxadr = 0.0005
nespadr = 3



#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


Mdb()
# a = mdb.models['Model-1'].rootAssembly


#--------------------------------------------------------------------------------------------
#Sketches y partes
#--------------------------------------------------------------------------------------------
#Definicion sketch y parte adhesivo
adssketch = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.0)
# adsg, adsv, adsd, adsc = adssketch.geometry, adssketch.vertices, adssketch.dimensions, adssketch.constraints
adssketch.setPrimaryObject(option=STANDALONE)
adssketch.rectangle(point1=(0.0, 0.0), point2=(solape, ts))
adspart = mdb.models['Model-1'].Part(name='Partads', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
# adspart = mdb.models['Model-1'].parts['Part-1']
adspart.BaseSolidExtrude(sketch=adssketch, depth=ancho)
adssketch.unsetPrimaryObject()
# adspart = mdb.models['Model-1'].parts['Part-1']
# session.viewports['Viewport: 1'].setValues(displayedObject=adspart)

#Definicion sketch y parte adherente
adrsketch = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.0)
# adrg, adrv, adrd, adrc = adrsketch.geometry, adrsketch.vertices, adrsketch.dimensions, adrsketch.constraints
adrsketch.setPrimaryObject(option=STANDALONE)
adrsketch.rectangle(point1=(0.0, 0.0), point2=(solape + longlibre, tr))
adrpart = mdb.models['Model-1'].Part(name='Partadr', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
# adrpart = mdb.models['Model-1'].parts['Part-2']
adrpart.BaseSolidExtrude(sketch=adrsketch, depth=ancho)
adrsketch.unsetPrimaryObject()
# adrpart = mdb.models['Model-1'].parts['Part-2']
# session.viewports['Viewport: 1'].setValues(displayedObject=adrpart)






#del mdb.models['Model-1'].sketches['__profile__']
#session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,engineeringFeatures=ON)
#session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)


#------------------------------------------------------------------------------------
#Definicion de materiales
#------------------------------------------------------------------------------------
#mdb.models['Model-1'].Material(name='mat_ads')
#mdb.models['Model-1'].materials['mat_ads'].Elastic(table=((E_ads, Poisson_ads), ))
#mdb.models['Model-1'].HomogeneousSolidSection(name='sec_ads', material='mat_ads', thickness=None)
#p = mdb.models['Model-1'].parts['Part-1']

if matutil == "Loctite EA 9514":
    mdb.models['Model-1'].Material(name='Loctite EA 9514')
    mdb.models['Model-1'].materials['Loctite EA 9514'].Elastic(table=((1460000.0, Poisson_ads), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='sec_ads', material='Loctite EA 9514', thickness=None)
elif matutil == "Loctite EA 9514 Shear":
    mdb.models['Model-1'].Material(name='Loctite EA 9514 Shear')
    mdb.models['Model-1'].materials['Loctite EA 9514 Shear'].Elastic(type=SHEAR, 
        temperatureDependency=ON, table=((48000.0, -20.0), (45000.0, 25.0),
        (39000.0, 75.0), (18000.0, 125.0), (5000.0, 150.0), (3000.0, 200.0)))
    mdb.models['Model-1'].HomogeneousSolidSection(name='sec_ads', material='Loctite EA 9514', thickness=None)
elif matutil == 'Loctite Hysol 9517':
    mdb.models['Model-1'].Material(name='Loctite Hysol 9517')
    mdb.models['Model-1'].materials['Loctite Hysol 9517'].Elastic(
        type=TRACTION, table=((1460000.0, 563706.0, 563706.0), )) # Enn from manufacturer spec (tensile modulus); Ess, Ett from Enn & nu from J.Diaz SLJ
    mdb.models['Model-1'].materials['Loctite Hysol 9517'].Density(table=((1.46, ), ))
    mdb.models['Model-1'].materials['Loctite Hysol 9517'].HashinDamageInitiation(
        table=((3300.0, 3300.0, 7000.0, 7000.0, 7000.0, 7000.0), ))
    mdb.models['Model-1'].materials['Loctite Hysol 9517'].hashinDamageInitiation.DamageEvolution(
        type=ENERGY, table=((0.33, 0.33, 0.8, 0.8), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='sec_ads', material='Loctite Hysol 9517', thickness=None)




mdb.models['Model-1'].Material(name='mat_adr')
mdb.models['Model-1'].materials['mat_adr'].Elastic(table=((E_adr, Poisson_adr), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='sec_adr', 
    material='mat_adr', thickness=None)



#Asignacion-------------------------------------------------------------------
adscells = adspart.cells
cells_ads = adscells.getSequenceFromMask(mask=('[#1 ]', ), )
region_ads = adspart.Set(cells=cells_ads, name='Set-Cells-ads')
adspart.SectionAssignment(region=region_ads, sectionName='sec_ads', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

adrcells = adrpart.cells
cells_adr = adrcells.getSequenceFromMask(mask=('[#1 ]', ), )
region_adr = adrpart.Set(cells=cells_adr, name='Set-Cells-adr')
adrpart.SectionAssignment(region=region_adr, sectionName='sec_adr', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

#p = mdb.models['Model-1'].parts['Part-1']
#a = mdb.models['Model-1'].rootAssembly
#session.viewports['Viewport: 1'].setValues(displayedObject=a)
#a1 = mdb.models['Model-1'].rootAssembly
#a1.DatumCsysByDefault(CARTESIAN)
#p = mdb.models['Model-1'].parts['Part-1']



#------------------------------------------------------------------------------------
#Ensamblado con posicionamiento
#------------------------------------------------------------------------------------
ads_inst = mdb.models['Model-1'].rootAssembly
ads_inst.DatumCsysByDefault(CARTESIAN)
ads_inst.Instance(name='instance_ads', part=adspart, dependent=OFF)
ads_inst = mdb.models['Model-1'].rootAssembly

adr_inst_sup = mdb.models['Model-1'].rootAssembly
adr_inst_sup.DatumCsysByDefault(CARTESIAN)
adr_inst_sup.Instance(name='instance_adr_sup', part=adrpart, dependent=OFF)
adr_inst_sup = mdb.models['Model-1'].rootAssembly
adr_inst_sup.translate(instanceList=('instance_adr_sup', ), vector=(0.0, ts, 0.0))

adr_inst_inf = mdb.models['Model-1'].rootAssembly
adr_inst_inf.DatumCsysByDefault(CARTESIAN)
adr_inst_inf.Instance(name='instance_adr_inf', part=adrpart, dependent=OFF)
adr_inst_inf = mdb.models['Model-1'].rootAssembly
adr_inst_inf.translate(instanceList=('instance_adr_inf', ), vector=(-longlibre, -tr, 0.0))

#ads_inst.translate(instanceList=('Part-1-1', ), vector=(1.0, 0.0, 0.0))
#: The instance Part-1-1 was translated by 1., 0., 0. with respect to the assembly coordinate system
#session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON)




#------------------------------------------------------------------------------------
#Step
#------------------------------------------------------------------------------------
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')



#------------------------------------------------------------------------------------
#Interaccion
#------------------------------------------------------------------------------------
#Particiones faces
#instancia = mdb.models['Model-1'].rootAssembly
#vert_ads = instancia.instances['instance_ads'].vertices
#edges_ads = instancia.instances['instance_ads'].edges
#instancia.DatumPlaneByPointNormal(point=vert_ads[2], normal=edges_ads[5])
##a = mdb.models['Model-1'].rootAssembly
##vert_inf = instancia.instances['instance_adr_inf'].vertices
##edges_inf = instancia.instances['instance_adr_inf'].edges
#instancia.DatumPlaneByPointNormal(point=vert_ads[1], normal=edges_ads[5])
##session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=('instance_adr_sup', ))
##session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=('instance_ads', ))
##a = mdb.models['Model-1'].rootAssembly
#cell_inf = instancia.instances['instance_adr_inf'].cells
#pickedRegions = cell_inf.getSequenceFromMask(mask=('[#3 ]', ), )
##a.deleteMesh(regions=pickedRegions)
##a = mdb.models['Model-1'].rootAssembly
#faces_inf = instancia.instances['instance_adr_inf'].faces
#pickedFaces = faces_inf.getSequenceFromMask(mask=('[#4 ]', ), )
#datum_inf = instancia.datums
#instancia.PartitionFaceByDatumPlane(datumPlane=datum_inf[10], faces=pickedFaces)
##session.viewports['Viewport: 1'].assemblyDisplay.showInstances(instances=('instance_adr_sup', ))
##session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=('instance_adr_inf', ))
##a = mdb.models['Model-1'].rootAssembly
#cell_sup = instancia.instances['instance_adr_sup'].cells
#pickedRegions = cell_sup.getSequenceFromMask(mask=('[#3 ]', ), )
##a.deleteMesh(regions=pickedRegions)
##a = mdb.models['Model-1'].rootAssembly
#faces_sup = instancia.instances['instance_adr_sup'].faces
#pickedFaces = faces_sup.getSequenceFromMask(mask=('[#10 ]', ), )
#datum_sup = instancia.datums
#instancia.PartitionFaceByDatumPlane(datumPlane=datum_sup[18], faces=pickedFaces)

#Creacion datums
instancia = mdb.models['Model-1'].rootAssembly
datpartadrsup = instancia.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=solape)
datpartadrinf = instancia.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)


cell_inf = instancia.instances['instance_adr_inf'].cells
pickedCells = cell_inf.getSequenceFromMask(mask=('[#1 ]', ), )
instancia.PartitionCellByDatumPlane(datumPlane=instancia.datums[datpartadrinf.id], cells=pickedCells)

cell_sup = instancia.instances['instance_adr_sup'].cells
pickedCells = cell_sup.getSequenceFromMask(mask=('[#1 ]', ), )
instancia.PartitionCellByDatumPlane(datumPlane=instancia.datums[datpartadrsup.id], cells=pickedCells)

#cell_inf = instancia.instances['instance_adr_inf'].cells
#pickedRegions = cell_inf.getSequenceFromMask(mask=('[#3 ]', ), )
#faces_inf = instancia.instances['instance_adr_inf'].faces
#pickedFaces = faces_inf.getSequenceFromMask(mask=('[#4 ]', ), )
#instancia.PartitionFaceByDatumPlane(datumPlane=instancia.datums[datpartadrinf.id], faces=pickedFaces)

#cell_sup = instancia.instances['instance_adr_sup'].cells
#pickedRegions = cell_inf.getSequenceFromMask(mask=('[#3 ]', ), )
#faces_inf = instancia.instances['instance_adr_sup'].faces
#pickedFaces = faces_inf.getSequenceFromMask(mask=('[#10 ]', ), )
#instancia.PartitionFaceByDatumPlane(datumPlane=instancia.datums[datpartadrsup.id], faces=pickedFaces)


#Propiedades del contacto
mdb.models['Model-1'].ContactProperty('interaccion')
mdb.models['Model-1'].interactionProperties['interaccion'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=OFF, 
    constraintEnforcementMethod=DEFAULT)
#: The interaction property "interaccion" has been created.
#session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=('instance_adr_sup', ))
#session.viewports['Viewport: 1'].assemblyDisplay.showInstances(instances=('instance_ads', ))
#a = mdb.models['Model-1'].rootAssembly

#Asignacion del contacto en superior
faces_sup = instancia.instances['instance_adr_sup'].faces
side1Faces_sup = faces_sup.getSequenceFromMask(mask=('[#1 ]', ), )
region1=instancia.Surface(side1Faces=side1Faces_sup, name='m_Surf-2')
#a = mdb.models['Model-1'].rootAssembly
faces_ads = instancia.instances['instance_ads'].faces
side1Faces_ads = faces_ads.getSequenceFromMask(mask=('[#2 ]', ), )
region2=instancia.Surface(side1Faces=side1Faces_ads, name='s_Surf-2')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='int_adrsup-ads', 
    createStepName='Initial', master=region1, slave=region2, sliding=FINITE, 
    thickness=ON, interactionProperty='interaccion', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-1" has been created.

#Asignacion del contacto en inferior
faces_inf = instancia.instances['instance_adr_inf'].faces
side1Faces_inf = faces_inf.getSequenceFromMask(mask=('[#8 ]', ), )
region1=instancia.Surface(side1Faces=side1Faces_inf, name='m_Surf-4')
#instancia = mdb.models['Model-1'].rootAssembly
faces_ads = instancia.instances['instance_ads'].faces
side1Faces_ads = faces_ads.getSequenceFromMask(mask=('[#8 ]', ), )
region2=instancia.Surface(side1Faces=side1Faces_ads, name='s_Surf-4')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='int_adrinf-ads', 
    createStepName='Initial', master=region1, slave=region2, sliding=FINITE, 
    thickness=ON, interactionProperty='interaccion', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-2" has been created.






#------------------------------------------------------------------------------------
#BCs + Loads
#------------------------------------------------------------------------------------
instancia = mdb.models['Model-1'].rootAssembly
f1 = instancia.instances['instance_ads'].faces
faces = f1.getSequenceFromMask(mask=('[#8 ]', ), )
region = instancia.Set(faces=faces, name='Set-1')
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
#session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
#instancia = mdb.models['Model-1'].rootAssembly
s = instancia.instances['instance_ads'].faces
side1Faces = s.getSequenceFromMask(mask=('[#2 ]', ), )
region = instancia.Surface(side1Faces=side1Faces, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=60.0, 
    amplitude=UNSET)
#session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, los=OFF, bcs=OFF, predefinedFields=OFF, connectors=OFF)
#session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)


#------------------------------------------------------------------------------------
#Mallado
#------------------------------------------------------------------------------------
#ensamblado = mdb.models['Model-1'].rootAssembly
instances_a_mallar =(instancia.instances['instance_ads'], )
instancia.seedPartInstance(regions=instances_a_mallar, size=tamanoads, deviationFactor=0.1, 
    minSizeFactor=0.1)
instances_a_mallar =(instancia.instances['instance_adr_sup'], )
instancia.seedPartInstance(regions=instances_a_mallar, size=tamanominadr, deviationFactor=0.1, 
    minSizeFactor=0.1)
instances_a_mallar =(instancia.instances['instance_adr_inf'], )
instancia.seedPartInstance(regions=instances_a_mallar, size=tamanominadr, deviationFactor=0.1, 
    minSizeFactor=0.1)

#-----------------------------------------------------------------------------------
#Refinado malla por zonas
"""
#Datums y particiones

#Datum superior
edges_sup = instancia.instances['instance_adr_sup'].edges
instancia.DatumPlaneByPointNormal(normal=edges_sup[4], 
    point=instancia.instances['instance_adr_sup'].InterestingPoint(edge=edges_sup[4], 
    rule=MIDDLE))
#a = mdb.models['Model-1'].rootAssembly

#Datum inferior
edges_inf = instancia.instances['instance_adr_inf'].edges
instancia.DatumPlaneByPointNormal(normal=edges_inf[4], 
    point=instancia.instances['instance_adr_inf'].InterestingPoint(edge=edges_inf[4], 
    rule=MIDDLE))
#a = mdb.models['Model-1'].rootAssembly

#Particion superior
cell_sup = instancia.instances['instance_adr_sup'].cells
pickedCells = cell_sup.getSequenceFromMask(mask=('[#1 ]', ), )
d = instancia.datums
instancia.PartitionCellByDatumPlane(datumPlane=d[15], cells=pickedCells)
#a = mdb.models['Model-1'].rootAssembly

#Particion inferior
cell_inf = instancia.instances['instance_adr_inf'].cells
pickedCells = cell_inf.getSequenceFromMask(mask=('[#1 ]', ), )
d = instancia.datums
instancia.PartitionCellByDatumPlane(datumPlane=d[16], cells=pickedCells)
"""

#Seeds globales para los adherentes
#a = mdb.models['Model-1'].rootAssembly
partInstances =(instancia.instances['instance_adr_sup'], )
instancia.seedPartInstance(regions=partInstances, size=tamanomaxadr, deviationFactor=0.1, 
    minSizeFactor=0.1)
partInstances =(instancia.instances['instance_adr_inf'], )
instancia.seedPartInstance(regions=partInstances, size=tamanomaxadr, deviationFactor=0.1, 
    minSizeFactor=0.1)

#a = mdb.models['Model-1'].rootAssembly
#e1 = a.instances['instance_adr_sup'].edges
#pickedEdges1 = e1.getSequenceFromMask(mask=('[#1010 ]', ), )
#pickedEdges2 = e1.getSequenceFromMask(mask=('[#10040 ]', ), )
#a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=0.0005, maxSize=0.0025, constraint=FINER)

#a = mdb.models['Model-1'].rootAssembly
#e1 = a.instances['instance_adr_sup'].edges
#pickedEdges1 = e1.getSequenceFromMask(mask=('[#10040 ]', ), )
#pickedEdges2 = e1.getSequenceFromMask(mask=('[#1010 ]', ), )
#a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=0.0005, maxSize=0.0025, constraint=FINER)


#Mallado fino junto a adhesivo
"""
#a = mdb.models['Model-1'].rootAssembly
#e1 = instancia.instances['instance_adr_sup'].edges
#e2 = instancia.instances['instance_adr_inf'].edges
pickedEdges1 = edges_sup.getSequenceFromMask(mask=('[#10040 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#280 ]', ), )
pickedEdges2 = edges_sup.getSequenceFromMask(mask=('[#1010 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#80400 ]', ), )
instancia.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
    end2Edges=pickedEdges2, minSize=0.0005, maxSize=0.0025, constraint=FINER)

#Again? preguntar
#a = mdb.models['Model-1'].rootAssembly
#e1 = a.instances['instance_adr_sup'].edges
#e2 = a.instances['instance_adr_inf'].edges
pickedEdges1 = edges_sup.getSequenceFromMask(mask=('[#10040 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#80400 ]', ), )
pickedEdges2 = edges_sup.getSequenceFromMask(mask=('[#1010 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#280 ]', ), )
instancia.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
    end2Edges=pickedEdges2, minSize=0.0005, maxSize=0.0025, constraint=FINER)

#Refinado malla adherentes paralelo a direccion extrusion
#a = mdb.models['Model-1'].rootAssembly
#e1 = a.instances['instance_adr_sup'].edges
#e2 = a.instances['instance_adr_inf'].edges
pickedEdges = edges_sup.getSequenceFromMask(mask=('[#a000 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#20100 ]', ), )
instancia.seedEdgeBySize(edges=pickedEdges, size=0.0005, deviationFactor=0.1, 
    minSizeFactor=0.1, constraint=FINER)



#Refinado malla en espesor
#pickedRegions = cell_sup+cell_inf
#a.deleteMesh(regions=pickedRegions)
#a = mdb.models['Model-1'].rootAssembly
#e1 = instancia.instances['instance_adr_sup'].edges
#e2 = instancia.instances['instance_adr_inf'].edges
pickedEdges = edges_sup.getSequenceFromMask(mask=('[#44820 ]', ), )+\
    edges_inf.getSequenceFromMask(mask=('[#44820 ]', ), )
instancia.seedEdgeByNumber(edges=pickedEdges, number=nespadr, constraint=FINER)

#Mallado adhesivo
#a = mdb.models['Model-1'].rootAssembly
#partInstances =(a.instances['instance_ads'], )
#a.deleteMesh(regions=partInstances)
#a = mdb.models['Model-1'].rootAssembly
#partInstances =(instancia.instances['instance_ads'], )
#instancia.seedPartInstance(regions=partInstances, size=0.00025, deviationFactor=0.1, minSizeFactor=0.1)
#a = mdb.models['Model-1'].rootAssembly
#partInstances =(instancia.instances['instance_ads'], )
#a.seedPartInstance(regions=partInstances, size=0.0025, deviationFactor=0.1, minSizeFactor=0.1)

#a = mdb.models['Model-1'].rootAssembly
partInstances =(instancia.instances['instance_ads'], )
instancia.seedPartInstance(regions=partInstances, size=0.0005, deviationFactor=0.1, 
    minSizeFactor=0.1)

#a = mdb.models['Model-1'].rootAssembly





"""






elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)

c1 = instancia.instances['instance_ads'].cells
cells = c1.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
instancia.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

partInstances =(instancia.instances['instance_ads'], instancia.instances['instance_adr_sup'], 
    instancia.instances['instance_adr_inf'], )
instancia.generateMesh(regions=partInstances)
#session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
#session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)




#------------------------------------------------------------------------------------
#Job
#------------------------------------------------------------------------------------
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
#mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#mdb.jobs['Job-1'].kill()
#: Error in job Job-1: Process terminated by external request (SIGTERM or SIGINT received).
#: Job Job-1: Analysis Input File Processor was terminated prior to analysis completion.
#: Error in job Job-1: Analysis Input File Processor exited with an error.
#mdb.saveAs(pathName='C:/Users/Luis/Documents/PruebaAbaqus/prueba')
#: The model database has been saved to "C:\Users\Luis\Documents\PruebaAbaqus\prueba.cae".
