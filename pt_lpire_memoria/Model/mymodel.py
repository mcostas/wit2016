from abaqus import *
from abaqusConstants import *

from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=234.330017089844,
    height=202.0537109375)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
#==============================================================================
#==============================================================================
#
# Inicializacion
#
#==============================================================================
#==============================================================================

host = 'BREOGAN'   # LOCAL / BREOGAN
union = 'HYBRID'   # HYBRID / ADS / SW / NONE

#==============================================================================
# Datos base
#==============================================================================

# Medidas en [m]
lado = 0.1
# ladohex = lado/2
ladohex = 0.0667

aleta = 0.02
espesor = 0.001
longitud = 0.35
longcomp = 0.345
pasopuntos = 0.03
sepcordones = 0.01

# Adhesivo
espads = 0.0003
adsmod = 'SOLID'  # SOLID / SHELL
unionmod = 'TIE'  # TIE / CC [Cohesive Contact]
matads = 'Loctite Hysol 9514'  # Loctite Hysol 9514
intmatads = 'Int_' + matads

tcomp = 0.0025

# Dimensiones GFRP
#longitud definida arriba
anchocomp = 0.128
surco = tcomp*sqrt(3)

# DynProps
delta = 0.25
velocidad = 15.  # velocidad en [m/s]

steptime = delta/velocidad

geometria = 'hex'   # hex / cuad

trigger = 'SIM'   # SIM / ANTIM
dtrigger = 0.003

#==============================================================================

# Malla y seeds
if host == 'BREOGAN':
    espuma_seed_size = 0.005
    GFRP_seed_size = 0.003
    chapa_seed_size = 0.004
    ads_seed_size = 0.004
    ads_seed_nesp = 5
    interv = 20
elif host == 'LOCAL':
    espuma_seed_size = 0.01
    GFRP_seed_size = 0.005
    chapa_seed_size = 0.01
    ads_seed_size = 0.01
    ads_seed_nesp = 1
    interv = 50

if union == 'HYBRID' or union == 'ADS':
    adhesivo = True
else:
    adhesivo = False
    espads = 0.0  # para definir espaciado entre chapas

soldadura = (union == 'HYBRID' or union == 'SW')

s30 = 0.5
c30 = cos(30*pi/180)

#==============================================================================
#==============================================================================
#
# Inicio del modelo
#
#==============================================================================
#==============================================================================

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=234.330017089844,
    height=202.0537109375)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)

#==============================================================================
# Geometria base
#==============================================================================

# Definicion de la chapa mediante un shell-extrude
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(ladohex/2, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(ladohex/2, 0.0), point2=(ladohex, ladohex*c30 - espesor/2))
s.Line(point1=(ladohex, ladohex*c30 - espesor/2), point2=(ladohex + aleta, ladohex*c30 - espesor/2))
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

# Definicion de la espuma mediante un solid-extrude
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(ladohex/2, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(ladohex/2, 0.0), point2=(ladohex, ladohex*c30))
s.Line(point1=(0.0, 0.0), point2=(0.0, 0.0287604592740536))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)
s.copyMirror(mirrorLine=g[4], objectList=(g[2], g[3]))
s.Line(point1=(ladohex, ladohex*c30), point2=(0.0312079340219498,
    ladohex*c30))
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


# Definicion del GFRP-U mediante un shell
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

# Idem con GFRP-H
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

# Creacion del adhesivo
if adhesivo == True:
	if adsmod == 'SOLID':
		s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.1)
		g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
		s.sketchOptions.setValues(decimalPlaces=3)
		s.setPrimaryObject(option=STANDALONE)
		s.rectangle(point1=(0.0, 0.0), point2=(aleta, longitud))
		p = mdb.models['Model-1'].Part(name='Adhesivo', dimensionality=THREE_D,
		    type=DEFORMABLE_BODY)
		p = mdb.models['Model-1'].parts['Adhesivo']
		p.BaseSolidExtrude(sketch=s, depth=espads)
		s.unsetPrimaryObject()
		p = mdb.models['Model-1'].parts['Adhesivo']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		del mdb.models['Model-1'].sketches['__profile__']
	elif adsmod == 'SHELL':
		s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.1)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.sketchOptions.setValues(decimalPlaces=3)
		s1.setPrimaryObject(option=STANDALONE)
		s1.rectangle(point1=(0.0, 0.0), point2=(aleta, longitud))
		p = mdb.models['Model-1'].Part(name='Adhesivo', dimensionality=THREE_D,
	    	type=DEFORMABLE_BODY)
		p = mdb.models['Model-1'].parts['Adhesivo']
		p.BaseShell(sketch=s1)
		s1.unsetPrimaryObject()
		p = mdb.models['Model-1'].parts['Adhesivo']
		del mdb.models['Model-1'].sketches['__profile__']



#==============================================================================
# Definicion de secciones y materiales
#==============================================================================
# Aluminio chapas -------------------------------------------------------------
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

# Adhesivo --------------------------------------------------------------------
if adhesivo == True:
	if matads == 'Loctite Hysol 9514':
	    mdb.models['Model-1'].Material(name=matads)
	    #mdb.models['Model-1'].materials['Loctite Hysol 9514'].Elastic(table=((
	    #   1460000.0, 0.295), )) # E from manufacturer specifications (tensile modulus); nu from J.Diaz SLJ
	    #mdb.models['Model-1'].materials['Loctite Hysol 9514'].Plastic(table=((39000.0, 
	    #0.0), (40000.0, 0.01)))
	    mdb.models['Model-1'].materials[matads].Elastic(
	        type=TRACTION, table=((1460000.0, 563706.0, 563706.0), )) # Enn from manufacturer spec (tensile modulus); Ess, Ett from Enn & nu from J.Diaz SLJ
	    #mdb.models['Model-1'].materials['Loctite Hysol 9514'].QuadsDamageInitiation(
	    #    table=((44000.0, 45000.0, 45000.0), )) # From manufacturer specs (tensile strength & lap shear strength twice)
	    mdb.models['Model-1'].materials[matads].Density(table=((1.46, ), ))
	    # mdb.models['Model-1'].materials[matads].HashinDamageInitiation(
	    #     table=((3300.0, 3300.0, 7000.0, 7000.0, 7000.0, 7000.0), ))
	    # mdb.models['Model-1'].materials[matads].hashinDamageInitiation.DamageEvolution(
	    #     type=ENERGY, table=((0.33, 0.33, 0.8, 0.8), ))
	    #mdb.models['Model-1'].materials['Loctite Hysol 9514'].elastic.FailStress(
	    #    table=((9000.0, 62000.0, 0.0, 0.0, 50000.0, 0.0, 0.0), ))
	    # mdb.models['Model-1'].materials['Loctite Hysol 9514'].DuctileDamageInitiation(
		# 	table=((0.01, 0.33, 0.0001), ))
	    # mdb.models['Model-1'].materials['Loctite Hysol 9514'].ductileDamageInitiation.DamageEvolution(
		# 	type=DISPLACEMENT, table=((0.0, ), ))
	    mdb.models['Model-1'].materials['Loctite Hysol 9514'].MaxsDamageInitiation(
		    table=((44000.0, 45000.0, 45000.0), ))
	    mdb.models['Model-1'].materials['Loctite Hysol 9514'].maxsDamageInitiation.DamageEvolution(
		    type=ENERGY, mixedModeBehavior=POWER_LAW, power=2.0, table=((0.905, 0.905, 
		    0.905), ))

	    # mdb.models['Model-1'].ContactProperty(intmatads)
	    # mdb.models['Model-1'].interactionProperties[intmatads].TangentialBehavior(
	    #     formulation=ROUGH)
	    # mdb.models['Model-1'].interactionProperties[intmatads].NormalBehavior(
	    #     pressureOverclosure=HARD, allowSeparation=ON, 
	    #     constraintEnforcementMethod=DEFAULT)
	    # mdb.models['Model-1'].interactionProperties[intmatads].Damage(initTable=((
	    #     62000.0, 40000.0, 40000.0), ))

	if adsmod == 'SOLID':
	#	mdb.models['Model-1'].HomogeneousSolidSection(name='Seccion_Adhesivo',
	#    	material='Loctite Hysol 9514', thickness=None)
	#	mdb.models['Model-1'].CohesiveSection(name='Seccion_Adhesivo_cohesivo',
	#	    material='Loctite Hysol 9514', response=CONTINUUM,
	#	    outOfPlaneThickness=None) # Task: implement election on startup
	    # mdb.models['Model-1'].CohesiveSection(name='Seccion_Adhesivo_cohesivo', 
	    #     material=matads, response=TRACTION_SEPARATION, 
	    #     outOfPlaneThickness=None)
		# mdb.models['Model-1'].HomogeneousSolidSection(name='sec_ads', 
	    # 	material='Loctite Hysol 9514', thickness=None)
		mdb.models['Model-1'].CohesiveSection(name='sec_ads_coh', 
		    material='Loctite Hysol 9514', response=TRACTION_SEPARATION, 
		    outOfPlaneThickness=None)

		p = mdb.models['Model-1'].parts['Adhesivo']
		c = p.cells
		cells = c[0:1]
		region = p.Set(cells=cells, name='Set-1')
		p = mdb.models['Model-1'].parts['Adhesivo']
		p.SectionAssignment(region=region, sectionName='sec_ads_coh', offset=0.0,
	    	offsetType=MIDDLE_SURFACE, offsetField='',
	    	thicknessAssignment=FROM_SECTION)
	elif adsmod == 'SHELL':
	    mdb.models['Model-1'].CohesiveSection(name='Seccion_Adhesivo_cohesivo', 
	        material=matads, response=TRACTION_SEPARATION, 
	        outOfPlaneThickness=espads)
	#	mdb.models['Model-1'].HomogeneousShellSection(name='Seccion_Adhesivo',
	#    	preIntegrate=OFF, material='Loctite Hysol 9514', thicknessType=UNIFORM,
	#    	thickness=espads, thicknessField='', idealization=NO_IDEALIZATION,
	#    	poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
	#    	useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)

# Espuma relleno --------------------------------------------------------------
mdb.models['Model-1'].Material(name='ArmaFORM')
mdb.models['Model-1'].materials['ArmaFORM'].Density(table=((0.135, ), ))
mdb.models['Model-1'].materials['ArmaFORM'].Elastic(table=((90000.0, 0.1), ))
mdb.models['Model-1'].materials['ArmaFORM'].CrushableFoam(table=((1.1, 1.0), ))
mdb.models['Model-1'].materials['ArmaFORM'].crushableFoam.CrushableFoamHardening(
    table=((2300, 0.0), ))

mdb.models['Model-1'].HomogeneousSolidSection(name='sec_espuma',
    material='ArmaFORM', thickness=None)


# GFRP ------------------------------------------------------------------------
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


#==============================================================================
# Ensamblado
#==============================================================================
#
# Colocacion de las chapas en el ensamblado
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Chapa']
a.Instance(name='Chapa-1', part=p, dependent=ON)
a.Instance(name='Chapa-2', part=p, dependent=ON)
a.translate(instanceList=('Chapa-2', ), vector=(2*ladohex + 2*aleta, 0.0, 0.0))
a.rotate(instanceList=('Chapa-2', ), axisPoint=(2*ladohex + aleta, ladohex*c30 - espesor/2, longitud),
    axisDirection=(0.0, 0.0, -longitud), angle=-180.0)
a.translate(instanceList=('Chapa-2', ), vector=(-2*ladohex, 0.0, 0.0))
a.translate(instanceList=('Chapa-2', ), vector=(0.0, espesor + espads, 0.0))


# Creacion de las placas de impacto y colocacion
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

# Reference Points para movimiento posterior
e1 = a.instances['Placa-1'].edges
a.ReferencePoint(point=a.instances['Placa-1'].InterestingPoint(edge=e1[0],
    rule=CENTER))
a = mdb.models['Model-1'].rootAssembly
e11 = a.instances['Placa-1-lin-2-1'].edges
a.ReferencePoint(point=a.instances['Placa-1-lin-2-1'].InterestingPoint(
    edge=e11[0], rule=CENTER))

# Por visualizacion, se ocultan las placas de impacto
session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=(
    'Placa-1', 'Placa-1-lin-2-1', ))

# Puntos de soldadura
if soldadura == True:
	a = mdb.models['Model-1'].rootAssembly

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

	#vpr.append(puntosr[10])
	#vpr.append(puntosr[11])
	# Comprobar por q numera dos ReferencePoints en 10&11 y el resto normal

	for i in range(10, npuntos + 10):
	    vpr.append(puntosr[i])

	a1 = mdb.models['Model-1'].rootAssembly
	a1.Set(referencePoints=vpr, name='Puntos_sol')

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
	mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointFastener(
	    name='punto_sol', region=region, targetSurfaces=targetSurface, 
	    sectionName='punto', connectorOrientationLocalCsys1=datum1, 
	    physicalRadius=0.04, unsorted=OFF)

# Colocacion de los adhesivos en el ensamblado
if adhesivo == True:
	p = mdb.models['Model-1'].parts['Adhesivo']
	a.Instance(name='Adhesivo-1', part=p, dependent=ON)
	a.Instance(name='Adhesivo-2', part=p, dependent=ON)
	if adsmod == 'SOLID':
		a.translate(instanceList=('Adhesivo-1', ), vector=(ladohex, ladohex*c30 + espads, 0.0))
		a.translate(instanceList=('Adhesivo-2', ), vector=(-ladohex - aleta, ladohex*c30 + espads, 0.0))
		a.rotate(instanceList=('Adhesivo-1', 'Adhesivo-2', ), axisPoint=(0.0, ladohex*c30 + espads, 0.0),
		    axisDirection=(1.0, 0.0, 0.0), angle=90.0)
	elif adsmod == 'SHELL':
		a.translate(instanceList=('Adhesivo-1', ), vector=(ladohex, ladohex*c30 + espads/2, 0.0))
		a.translate(instanceList=('Adhesivo-2', ), vector=(-ladohex - aleta, ladohex*c30 + espads/2, 0.0))
		a.rotate(instanceList=('Adhesivo-1', 'Adhesivo-2', ), axisPoint=(0.0, ladohex*c30 + espads/2, 0.0),
		    axisDirection=(1.0, 0.0, 0.0), angle=90.0)



#==============================================================================
# Ensamblado y mallado de dependientes
#==============================================================================

# Espuma ----------------------------------------------------------------------
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
p.seedPart(size=espuma_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
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

# IDK
# Repetido mas adelante?

#mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
#    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A',
#    'RF', 'SF', 'CSTRESS', 'EVF'))


# Se disenho como un prisma hexagonal
# Se marcan los datums
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
# Se corta por los datums
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

# Se elimina el sobrante
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


v11 = a.instances['espuma_hex-1'].vertices
a.DatumPointByMidPoint(point1=v11[35], point2=v11[5])


#mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
#    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A',
#    'RF', 'SF', 'CSTRESS', 'EVF', 'STATUS'))


# Repetido mas atras?
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

# GFRP ------------------------------------------------------------------------
# Insercion y colocacion
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

# Mallado
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT,
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)

p = mdb.models['Model-1'].parts['GFRP_H']
p.seedPart(size=GFRP_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
f = p.faces
pickedRegions = f[0:1]
p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
p.setElementType(regions=(pickedRegions, ), elemTypes=(elemType1, elemType2))
p.generateMesh()
p = mdb.models['Model-1'].parts['GFRP_U']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p.seedPart(size=GFRP_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
f = p.faces
pickedRegions = f[0:1]
p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
p.setElementType(regions=(pickedRegions, ), elemTypes=(elemType1, elemType2))
p.generateMesh()

# Chapas ----------------------------------------------------------------------
# Mallado (+ placas)
p = mdb.models['Model-1'].parts['Chapa']
p.seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Chapa']
#p.generateMesh()
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
a = mdb.models['Model-1'].rootAssembly
a.regenerate()

# Union adhesivo
if adhesivo == True:
	if unionmod == 'CC':
		mdb.models['Model-1'].ContactProperty('IntProp-2')
		mdb.models['Model-1'].interactionProperties['IntProp-2'].CohesiveBehavior(
	    	eligibility=INITIAL_NODES)

		if adsmod == 'SOLID':
			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-1')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[4:5]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-1')
			mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Ch1-Ads1',
	   			createStepName='Initial', master = region1, slave = region2,
	    		mechanicalConstraint=KINEMATIC, sliding=FINITE,
	    		interactionProperty='IntProp-2', initialClearance=OMIT, datumAxis=None,
	    		clearanceRegion=None)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-2')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[5:6]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-2')
			mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Ch2-Ads1',
	    		createStepName='Initial', master = region1, slave = region2,
	    		mechanicalConstraint=KINEMATIC, sliding=FINITE,
	    		interactionProperty='IntProp-2', initialClearance=OMIT, datumAxis=None,
	    		clearanceRegion=None)

			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-3')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[4:5]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-3')
			mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Ch1-Ads2',
	    		createStepName='Initial', master = region1, slave = region2,
	    		mechanicalConstraint=KINEMATIC, sliding=FINITE,
	    		interactionProperty='IntProp-2', initialClearance=OMIT, datumAxis=None,
	    		clearanceRegion=None)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-4')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[5:6]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-4')
			mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Ch2-Ads2',
	    		createStepName='Initial', master = region1, slave = region2,
	    		mechanicalConstraint=KINEMATIC, sliding=FINITE,
	    		interactionProperty='IntProp-2', initialClearance=OMIT, datumAxis=None,
	    		clearanceRegion=None)

	elif unionmod == 'TIE':
		if adsmod == 'SOLID':
			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-1')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[4:5]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-1')
			mdb.models['Model-1'].Tie(name='Ch1-Ads1', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-2')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[5:6]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-2')
			mdb.models['Model-1'].Tie(name='Ch2-Ads1', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-3')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[4:5]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-3')
			mdb.models['Model-1'].Tie(name='Ch1-Ads2', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-4')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[5:6]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-4')
			mdb.models['Model-1'].Tie(name='Ch2-Ads2', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

		elif adsmod == 'SHELL':
			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-1')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[0:1]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-1')
			mdb.models['Model-1'].Tie(name='Ch1-Ads1', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-2')
			f1 = a.instances['Adhesivo-1'].faces
			faces1 = f1[0:1]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-2')
			mdb.models['Model-1'].Tie(name='Ch2-Ads1', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-1'].faces
			faces1 = f1[0:1]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-3')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[0:1]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-3')
			mdb.models['Model-1'].Tie(name='Ch1-Ads2', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

			f1 = a.instances['Chapa-2'].faces
			faces1 = f1[4:5]
			region1=a.Surface(side1Faces=faces1, name='m_Surf-4')
			f1 = a.instances['Adhesivo-2'].faces
			faces1 = f1[0:1]
			region2=a.Surface(side1Faces=faces1, name='s_Surf-4')
			mdb.models['Model-1'].Tie(name='Ch2-Ads2', master=region1, slave=region2,
			    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)


# Particion para sujecion
p = mdb.models['Model-1'].parts['Chapa']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.3)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedRegions = f[0:5]
#p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Chapa']
f = p.faces
pickedFaces = f[0:5]
d = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d[5], faces=pickedFaces)
a = mdb.models['Model-1'].rootAssembly
p.generateMesh()
a.regenerate()


# Adhesivo (mallado) ----------------------------------------------------------
if adhesivo == True:
	p = mdb.models['Model-1'].parts['Adhesivo']
	p.seedPart(size=ads_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
	if adsmod == 'SOLID':
		e = p.edges
		pickedEdges = e[1:2]+e[3:4]+e[5:6]+e[8:9]
		p.seedEdgeByNumber(edges=pickedEdges, number=ads_seed_nesp, constraint=FINER)
		# elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
	    #     kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
	    #     hourglassControl=DEFAULT, distortionControl=DEFAULT)
		# elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
		# elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
		elemType1 = mesh.ElemType(elemCode=COH3D8, elemLibrary=EXPLICIT)
		elemType2 = mesh.ElemType(elemCode=COH3D6, elemLibrary=EXPLICIT)
		elemType3 = mesh.ElemType(elemCode=UNKNOWN_TET, elemLibrary=EXPLICIT)
		c = p.cells
		cells = c[0:1]
		pickedRegions =(cells, )
		p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
	    	elemType3))

	p.generateMesh()


#==============================================================================
# Step
#==============================================================================

# Step Impacto
mdb.models['Model-1'].ExplicitDynamicsStep(name='Impacto', previous='Initial')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'EVF','LE','PE','PEEQ','PEEQVAVG','PEVAVG','RF','S','STATUS','SVAVG','U'))



#==============================================================================
# Interacciones + BC
#==============================================================================

# Evitar viajes al infinito y mas alla (mov base solo en dir extrusion)
f1 = a.instances['Chapa-2'].faces
faces1 = f1[0:4]+f1[5:6]
f2 = a.instances['Chapa-1'].faces
faces2 = f2[0:4]+f2[5:6]
region = regionToolset.Region(faces=faces1+faces2)
mdb.models['Model-1'].DisplacementBC(name='Clamp', createStepName='Impacto',
    region=region, u1=0.0, u2=0.0, u3=UNSET, ur1=0.0, ur2=0.0, ur3=0.0,
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',
    localCsys=None)

# Contacto general ------------------------------------------------------------
mdb.models['Model-1'].ContactProperty('Global-IntProp')
mdb.models['Model-1'].interactionProperties['Global-IntProp'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    0.05, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION,
    fraction=0.005, elasticSlipStiffness=None)
mdb.models['Model-1'].interactionProperties['Global-IntProp'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON,
    constraintEnforcementMethod=DEFAULT)
mdb.models['Model-1'].ContactExp(name='Global-Int', createStepName='Initial')
mdb.models['Model-1'].interactions['Global-Int'].includedPairs.setValuesInStep(
    stepName='Initial', useAllstar=ON)
mdb.models['Model-1'].interactions['Global-Int'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'Global-IntProp'), ))

# Mov placas ------------------------------------------------------------------
# Reference points para rig/mov placas (not working properly)
mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP,
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))

# Movimiento placa
f1 = a.instances['Placa-1'].faces
faces1 = f1[0:1]
region1=a.Set(faces=faces1, name='b_Set-6')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[11], )
region2 = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='PlacaMov-RP', refPointRegion=region2,
    bodyRegion=region1, refPointAtCOM=ON)
mdb.models['Model-1'].DisplacementBC(name='MovPlaca', createStepName='Impacto',
    region=region2, u1=0.0, u2=0.0, u3= (delta + 0.001), ur1=0.0, ur2=0.0, ur3=0.0,
    amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='',
    localCsys=None)

# Fijacion placa
f1 = a.instances['Placa-1-lin-2-1'].faces
faces1 = f1[0:1]
region1=a.Set(faces=faces1, name='b_Set-4')
a = mdb.models['Model-1'].rootAssembly
refPoints1=(r1[10], )
region2 = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='PlacaFij', refPointRegion=region2,
    bodyRegion=region1, refPointAtCOM=ON)
mdb.models['Model-1'].EncastreBC(name='FijPlaca', createStepName='Initial',
    region=region2, localCsys=None)

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=interv)

mdb.models['Model-1'].steps['Impacto'].setValues(timePeriod=steptime)
mdb.models['Model-1'].amplitudes['Amp-1'].setValues(timeSpan=STEP,
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (steptime, 1.0)))

# =============================================================================
# Job para localhost
# =============================================================================

if host == 'LOCAL':
	mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS,
    	atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
    	memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
    	nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
    	contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
    	parallelizationMethodExplicit=DOMAIN, numDomains=1,
    	activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)

# =============================================================================
# Visualizacion final
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
    predefinedFields=ON, connectors=ON, optimizationTasks=OFF,
    geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Impacto')

mdb.jobs['Job-1'].writeInput(consistencyChecking=OFF)
