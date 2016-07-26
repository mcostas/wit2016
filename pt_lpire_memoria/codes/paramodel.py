#==============================================================================
#==============================================================================
#
# Crash Box
#
#==============================================================================
#==============================================================================

# Opciones por defecto
opc = {
    'Host': 'BREOGAN',        # LOCAL | BREOGAN
    'Tipo de union': 'ADS',  # [HYBRID] | ADS | SW | NONE
    'Espesor adhesivo': 0.0003, # [m] 0.0001 | [0.0003] | 0.0005 | 0.001 | 0.0025
    'Relleno': 'NONE',        # [FULL] | FOAMHEX | FOAM6 | GFRP | NONE
    'N puntos de soldadura': 5, # 4 | [6] | 8 | 10 | 12
    'Geometria': 'SQR'        # [HEX] | SQR
}

#==============================================================================
# Datos base
#==============================================================================

halfm = False

# Dakota param
GIc     = 1.000000000000000e+00
GIIc    = 1.000000000000000e+00
G_int   = 1.000000000000000e+00

# Medidas en [m]
lado = 0.0667           # Lado del poligono base de la seccion. Default: 0.0667
aleta = 0.020           # Ancho de las aletas sobre las que se unen las chapas. Default: 0.02
espesor = 0.001         # Espesor de las chapas
longitud = 0.20         # Longitud total del tubo. Default: 0.35
sepcordones = 0.01      # Distancia de los SW del borde de la aleta
mats = 'PREDEF'         # USER | PREDEF ; Materiales por subrutina o predefinidos

# Adhesivo
adhesive_name = 'Loctite Hysol 9514'    # Loctite Hysol 9514
intadhesive_name = 'Int_' + adhesive_name

adherente = 'Al'        # Al | Acero

tcomp = 0.0025        # Espesor GFRP

# Dimensiones GFRP
holgura_GFRP = 0.005
longcomp = longitud - holgura_GFRP
anchocomp = 2*lado - holgura_GFRP      # Anchura del panel de GFRP (queda una ligera holgura)
surco = tcomp*sqrt(3)

# DynProps
delta = 0.15 #0.5*longitud  # Desplazamiento. Default: 0.25
velocidad = 10.         # Velocidad en [m/s]. Default: 15.

steptime = delta/velocidad

trigger = None
ltrigger = 0.015

#==============================================================================
#==============================================================================
#
# INDICE
#
# Opciones
# Datos base
# Indice
# Inicializacion
# Chapa:
#   Geometria base, Materiales, Ensamblado, Mallado, Superficies de contacto
# FOAM:
#   Geometria base, Materiales, Ensamblado, Mallado, Superficies de contacto
# GFRP:
#   Geometria base, Materiales, Ensamblado, Mallado, Superficies de contacto
# Adhesivo:
#   Geometria base, Materiales, Ensamblado, Mallado, Superficies de contacto
#
#
#==============================================================================
# Inicializacion
#==============================================================================

from abaqus import *
from abaqusConstants import *

from caeModules import *
from driverUtils import executeOnCaeStartup
import sys
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=234.330017089844,
    height=194.)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)

# Lectura de argumentos
if 'BREOGAN' in sys.argv:
    opc['Host'] = 'BREOGAN'
    opc['Relleno'] = sys.argv[-1]
    opc['N puntos de soldadura'] = int(sys.argv[-2])
    opc['Espesor adhesivo'] = float(sys.argv[-3])
    opc['Tipo de union'] = sys.argv[-4]
    opc['Geometria'] = sys.argv[-5]
    opc['Codigo'] = sys.argv[-6]
    mats = 'USER'

# Malla y seeds
if opc['Host'] == 'BREOGAN':
    espuma_seed_size = 0.005    # 0.005
    GFRP_seed_size = 0.003      # 0.003
    chapa_seed_size = 0.0035    # 0.002
    ads_seed_size = 0.0025      # 0.001
    ads_seed_nesp = 1           # 1
    interv = 500                # 500
elif opc['Host'] == 'LOCAL':
    espuma_seed_size = 0.01
    GFRP_seed_size = 0.005
    chapa_seed_size = 0.01
    ads_seed_size = 0.01
    ads_seed_nesp = 1
    interv = 50

imperfeccion = 0.#00025

if opc['Geometria'] == 'HEX':
    # angulo = 30.
    # ladoh = lado
    # ladov = lado
    x1 = lado
    y1 = lado*0.7071067812
    x2 = lado/2
    y2 = 0.
elif opc['Geometria'] == 'SQR':
    # El cuadrado no admite GFRP (todavia: problemas con dimensiones (ancho) y con giro (angulo))
    if opc['Relleno'] == 'FULL':
        opc['Relleno'] = 'FOAM6'
    elif opc['Relleno'] == 'GFRP':
        opc['Relleno'] = 'NONE'
    x1 = lado/2 - imperfeccion
    y1 = lado/2
    x2 = lado/2 + imperfeccion
    y2 = 0.

    # angulo = 0.00001
    # ladoh = lado
    # ladov = lado/2

# seno = sin(angulo*pi/180)
# coseno = cos(angulo*pi/180)

if opc['Tipo de union'] == 'HYBRID' or opc['Tipo de union'] == 'ADS':
    adhesivo = True
else:
    adhesivo = False
    opc['Espesor adhesivo'] = 0.0  # para definir espaciado entre chapas

soldadura = opc['Tipo de union'] == 'HYBRID' or opc['Tipo de union'] == 'SW'
if soldadura == True:
    pasopuntos = longitud / int(opc['N puntos de soldadura'])

GFRP = opc['Relleno'] == 'FULL' or opc['Relleno'] == 'GFRP'


#==============================================================================
#==============================================================================
#
# Inicio del modelo
#
#==============================================================================
#==============================================================================

modelo = mdb.models['Model-1']
a = modelo.rootAssembly

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=234.330017089844,
    height=194.)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.journalOptions.setValues(replayGeometry=INDEX, recoverGeometry=INDEX)

#==============================================================================
# Geometria
#==============================================================================

#------------------------------------------------------------------------------
# Chapa
#------------------------------------------------------------------------------
def creaChapa(modelo=modelo, opc=opc, x1=x1, y1=y1, x2=x2, y2=y2):
    espads = opc['Espesor adhesivo']

    # Geometria base ----------------------------------------------------------
    if not halfm:
        s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)

        s.Line(point1=(0.0, y2),                                    point2=(x2, y2))
        s.HorizontalConstraint(entity=g[2],                         addUndoState=False)

        s.Line(point1=(x2, y2),                                     point2=(x1, y1 - (espads + espesor)/2))
        s.Line(point1=(x1, y1 - (espads + espesor)/2),              point2=(x1 + aleta, y1 - (espads + espesor)/2))
        s.HorizontalConstraint(entity=g[4],                         addUndoState=False)

        s.Line(point1=(0.0, 0.0),                               point2=(0.0, 1.0))
        s.VerticalConstraint(entity=g[5],                       addUndoState=False)
        s.PerpendicularConstraint(entity1=g[2], entity2=g[5],   addUndoState=False)
        s.copyMirror(mirrorLine=g[5],                           objectList=(g[2], g[3], g[4]))
        s.delete(objectList=(g[5], ))

        p = modelo.Part(name='Chapa', dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = modelo.parts['Chapa']
        p.BaseShellExtrude(sketch=s, depth=longitud)
        s.unsetPrimaryObject()
        del modelo.sketches['__profile__']

        s1 = p.features['Shell extrude-1'].sketch
        modelo.ConstrainedSketch(name='__edit__', objectToCopy=s1)
        s = modelo.sketches['__edit__']
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)

        # p.projectReferencesOntoSketch(sketch=s, upToFeature=p.features['Shell extrude-1'], filter=COPLANAR_EDGES)
        # s.delete(objectList=(g[6], c[16]))
        # s.trimExtendCurve(
        #   curve1=g[2], point1=(0.00355016766116023, -0.000465545803308487),
        #   curve2=g[7], point2=(-0.0351068116724491, 0.0019342303276062))
        # s.unsetPrimaryObject()
        # p.features['Shell extrude-1'].setValues(sketch=s)

        del modelo.sketches['__edit__']
        p.regenerate()

    else:
        s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)

        s.Line(point1=(0.0, y2),                                    point2=(x2, y2))
        s.HorizontalConstraint(entity=g[2],                         addUndoState=False)

        s.Line(point1=(x2, y2),                                     point2=(x1, y1 - (espads + espesor)/2))
        s.Line(point1=(x1, y1 - (espads + espesor)/2),              point2=(x1 + aleta, y1 - (espads + espesor)/2))
        s.HorizontalConstraint(entity=g[4],                         addUndoState=False)

        ChapaBot = modelo.Part(name='partChapaBot', dimensionality=THREE_D, type=DEFORMABLE_BODY)
        ChapaBot.BaseShellExtrude(sketch=s, depth=longitud)
        s.unsetPrimaryObject()
        del modelo.sketches['__profile__']

        s1 = ChapaBot.features['Shell extrude-1'].sketch
        modelo.ConstrainedSketch(name='__edit__', objectToCopy=s1)
        s = modelo.sketches['__edit__']
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)

        # ChapaBot.projectReferencesOntoSketch(sketch=s, upToFeature=ChapaBot.features['Shell extrude-1'], filter=COPLANAR_EDGES)
        # s.delete(objectList=(g[6], c[16]))
        # s.trimExtendCurve(
        #   curve1=g[2], point1=(0.00355016766116023, -0.000465545803308487),
        #   curve2=g[7], point2=(-0.0351068116724491, 0.0019342303276062))
        # s.unsetPrimaryObject()
        # ChapaBot.features['Shell extrude-1'].setValues(sketch=s)

        del modelo.sketches['__edit__']
        ChapaBot.regenerate()

        ChapaTop = modelo.Part(name='partChapaTop', objectToCopy=ChapaBot, compressFeatureList=ON, mirrorPlane=XZPLANE)

    # Materiales --------------------------------------------------------------
    if adherente == 'Al' and mats == 'PREDEF':
        modelo.Material(name='AA5754_JC')
        modelo.materials['AA5754_JC'].Density(table=((2.56, ), ))
        modelo.materials['AA5754_JC'].Elastic(table=((70000000.0, 0.33), ))
        modelo.materials['AA5754_JC'].Plastic(hardening=JOHNSON_COOK,
            table=((67456.0, 471242.0, 0.424, 0.0, 0.0, 0.0), ))
        modelo.materials['AA5754_JC'].plastic.RateDependent(
            type=JOHNSON_COOK, table=((0.003, 0.0033), ))

        modelo.HomogeneousShellSection(name='sec1mm', preIntegrate=OFF,
            material='AA5754_JC', thicknessType=UNIFORM, thickness=espesor,
            thicknessField='', idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
            thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
            integrationRule=SIMPSON, numIntPts=5)

    elif adherente == 'Al' and mats == 'USER':
        modelo.Material(name='ALUM')
        mat_alum2 = modelo.materials['ALUM']
        mat_alum2.Density(table=((2.70, ), ))
        mat_alum2.Elastic(table=((70000000.0, 0.3), ))
        mat_alum2.Plastic(hardening=USER, table=((520000.0, ), (477000, ), (0.0005, ), (0.52, ), (0.001, )))
        modelo.HomogeneousShellSection(name='sec1mm', preIntegrate=OFF,
            material='ALUM', thicknessType=UNIFORM, thickness=espesor,
            thicknessField='', idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
            thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
            integrationRule=SIMPSON, numIntPts=5)

    elif adherente == 'Acero':
        modelo.Material(name='Acero')
        mat_alum2 = modelo.materials['Acero']
        mat_alum2.Elastic(table=((200000000.0, 0.3), ))
        mat_alum2.Plastic(hardening=ISOTROPIC, table=((190000.0, 0.0), (1140000.0, 1.0)))  # 1140MPa = 950 + 190
        mat_alum2.Density(table=((7.85, ), ))
        # mat_alum2.Plastic(hardening=JOHNSON_COOK, table=((211600., 516700., 0.300, 0.822, 0.0, 0.0), ))
        modelo.HomogeneousShellSection(name='sec1mm', preIntegrate=OFF,
            material='Acero', thicknessType=UNIFORM, thickness=espesor,
            thicknessField='', idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
            thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
            integrationRule=SIMPSON, numIntPts=5)

    if not halfm:
        region = regionToolset.Region(faces=p.faces[0:5])
        p.SectionAssignment(region=region, sectionName='sec1mm', offset=0.0,
            offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)
    else:
        region = regionToolset.Region(faces=ChapaBot.faces[:])
        ChapaBot.SectionAssignment(region=region, sectionName='sec1mm', offset=0.0,
            offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)
        region = regionToolset.Region(faces=ChapaTop.faces[:])
        ChapaTop.SectionAssignment(region=region, sectionName='sec1mm', offset=0.0,
            offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)

    # Ensamblado --------------------------------------------------------------
    if not halfm:
        a.DatumCsysByDefault(CARTESIAN)
        ChapaBot = a.Instance(name='Chapa-1', part=p, dependent=ON)

        ChapaTop = a.Instance(name='Chapa-2', part=p, dependent=ON)
        # a.rotate(instanceList=('Chapa-2', ),
        #    axisPoint=(0.0, ladov*coseno + espads/2, 0.0),
        #    axisDirection=(0.0, 0.0, 1.0), angle=180.0)
        a.rotate(instanceList=('Chapa-2', ),
            axisPoint=(0.0, y1, 0.0),
            axisDirection=(0.0, 0.0, 1.0), angle=180.0)
    else:
        a.DatumCsysByDefault(CARTESIAN)
        ChapaBot = a.Instance(name='Chapa-1', part=ChapaBot, dependent=ON)

        ChapaTop = a.Instance(name='Chapa-2', part=ChapaTop, dependent=ON)
        a.translate(instanceList=('Chapa-2', ), vector=(0., 2*y1, 0.))

        # a.rotate(instanceList=('Chapa-2', ),
        #    axisPoint=(0.0, ladov*coseno + espads/2, 0.0),
        #    axisDirection=(0.0, 0.0, 1.0), angle=180.0)
        # a.rotate(instanceList=('Chapa-2', ),
        #   axisPoint=(0.0, y1, 0.0),
        #   axisDirection=(0.0, 0.0, 1.0), angle=180.0)

    # Mallado -----------------------------------------------------------------
    if not halfm:
        p = modelo.parts['Chapa']
        p.seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)

        elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT,
            secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
        p.setElementType(regions=(p.faces[0:5], ), elemTypes=(elemType1, elemType2))
    else:
        p = modelo.parts['partChapaBot']
        p.seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)

        elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT,
            secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
        p.setElementType(regions=(p.faces[0:5], ), elemTypes=(elemType1, elemType2))

        p = modelo.parts['partChapaTop']
        p.seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)

        elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT,
            secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
        p.setElementType(regions=(p.faces[0:5], ), elemTypes=(elemType1, elemType2))

creaChapa()

# Superficies de contacto -----------------------------------------------------
if not halfm:
    # Chapa 1
    Ch1_u2      = a.Surface(side1Faces=a.instances['Chapa-1'].faces[0:1],   name='Ch1_u2')   # Union 2
    Ch1_ext_u2  = a.Surface(side2Faces=a.instances['Chapa-1'].faces[0:1],   name='Ch1_ext_u2')
    Ch1_int5    = a.Surface(side1Faces=a.instances['Chapa-1'].faces[1:2],   name='Ch1_int5')
    Ch1_ext5    = a.Surface(side2Faces=a.instances['Chapa-1'].faces[1:2],   name='Ch1_ext5')
    Ch1_int4    = a.Surface(side1Faces=a.instances['Chapa-1'].faces[2:3],   name='Ch1_int4')
    Ch1_ext4    = a.Surface(side2Faces=a.instances['Chapa-1'].faces[2:3],   name='Ch1_ext4')
    Ch1_int3    = a.Surface(side1Faces=a.instances['Chapa-1'].faces[3:4],   name='Ch1_int3')
    Ch1_ext3    = a.Surface(side2Faces=a.instances['Chapa-1'].faces[3:4],   name='Ch1_ext3')
    Ch1_u1      = a.Surface(side1Faces=a.instances['Chapa-1'].faces[4:5],   name='Ch1_u1')   # Union 1
    Ch1_ext_u1  = a.Surface(side2Faces=a.instances['Chapa-1'].faces[4:5],   name='Ch1_ext_u1')
    Ch1_all = [Ch1_u2, Ch1_ext_u2, Ch1_int5, Ch1_ext5, Ch1_int4, Ch1_ext4, Ch1_int3, Ch1_ext3, Ch1_u1, Ch1_ext_u1]

    # Chapa 2
    Ch2_u1      = a.Surface(side1Faces=a.instances['Chapa-2'].faces[0:1],   name='Ch2_u2')   # Union 1
    Ch2_ext_u1  = a.Surface(side2Faces=a.instances['Chapa-2'].faces[0:1],   name='Ch2_ext_u1')
    Ch2_int2    = a.Surface(side1Faces=a.instances['Chapa-2'].faces[1:2],   name='Ch2_int2')
    Ch2_ext2    = a.Surface(side2Faces=a.instances['Chapa-2'].faces[1:2],   name='Ch2_ext2')
    Ch2_int1    = a.Surface(side1Faces=a.instances['Chapa-2'].faces[2:3],   name='Ch2_int1')
    Ch2_ext1    = a.Surface(side2Faces=a.instances['Chapa-2'].faces[2:3],   name='Ch2_ext1')
    Ch2_int6    = a.Surface(side1Faces=a.instances['Chapa-2'].faces[3:4],   name='Ch2_int6')
    Ch2_ext6    = a.Surface(side2Faces=a.instances['Chapa-2'].faces[3:4],   name='Ch2_ext6')
    Ch2_u2      = a.Surface(side1Faces=a.instances['Chapa-2'].faces[4:5],   name='Ch2_u1')   # Union 2
    Ch2_ext_u2  = a.Surface(side2Faces=a.instances['Chapa-2'].faces[4:5],   name='Ch2_ext_u2')
    Ch2_all = [Ch2_u1, Ch2_ext_u1, Ch2_int2, Ch2_ext2, Ch2_int1, Ch2_ext1, Ch2_int6, Ch2_ext6, Ch2_u2, Ch2_ext_u2]
else:
    # Chapa 1
    Ch1_int4    = a.Surface(side2Faces=a.instances['Chapa-1'].faces[2:3],   name='Ch1_int4')
    Ch1_ext4    = a.Surface(side1Faces=a.instances['Chapa-1'].faces[2:3],   name='Ch1_ext4')
    Ch1_int3    = a.Surface(side2Faces=a.instances['Chapa-1'].faces[1:2],   name='Ch1_int3')
    Ch1_ext3    = a.Surface(side1Faces=a.instances['Chapa-1'].faces[1:2],   name='Ch1_ext3')
    Ch1_u1      = a.Surface(side2Faces=a.instances['Chapa-1'].faces[0:1],   name='Ch1_u1')   # Union 1
    Ch1_ext_u1  = a.Surface(side1Faces=a.instances['Chapa-1'].faces[0:1],   name='Ch1_ext_u1')
    Ch1_all = [Ch1_int4, Ch1_ext4, Ch1_int3, Ch1_ext3, Ch1_u1, Ch1_ext_u1]

    # Chapa 2
    Ch2_u1      = a.Surface(side2Faces=a.instances['Chapa-2'].faces[0:1],   name='Ch2_u2')   # Union 1
    Ch2_ext_u1  = a.Surface(side1Faces=a.instances['Chapa-2'].faces[0:1],   name='Ch2_ext_u1')
    Ch2_int2    = a.Surface(side2Faces=a.instances['Chapa-2'].faces[1:2],   name='Ch2_int2')
    Ch2_ext2    = a.Surface(side1Faces=a.instances['Chapa-2'].faces[1:2],   name='Ch2_ext2')
    Ch2_int1    = a.Surface(side2Faces=a.instances['Chapa-2'].faces[2:3],   name='Ch2_int1')
    Ch2_ext1    = a.Surface(side1Faces=a.instances['Chapa-2'].faces[2:3],   name='Ch2_ext1')
    Ch2_all = [Ch2_u1, Ch2_ext_u1, Ch2_int2, Ch2_ext2, Ch2_int1, Ch2_ext1]



#------------------------------------------------------------------------------
# Foam
#------------------------------------------------------------------------------
# Pending update: referenced to x1, y1, x2, y2
if opc['Relleno'] == 'FULL' or opc['Relleno'] == 'FOAMHEX' or opc['Relleno'] == 'FOAM6':
    # Geometria base ----------------------------------------------------------
    s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(0.0, 0.0),               point2=(ladoh/2, 0.0))
    s.HorizontalConstraint(entity=g[2],     addUndoState=False)

    s.Line(point1=(ladoh/2, 0.0),           point2=(ladoh/2 + ladov*seno, ladov*coseno))
    s.Line(point1=(0.0, 0.0),               point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[4],       addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)
    s.copyMirror(mirrorLine=g[4],           objectList=(g[2], g[3]))

    s.Line(point1=(0.0, ladov*coseno),      point2=(1.0, ladov*coseno))
    s.HorizontalConstraint(entity=g[7],     addUndoState=False)
    s.copyMirror(mirrorLine=g[7],           objectList=(g[2], g[3], g[5], g[6]))

    s.delete(objectList=(g[4], g[7], c[9]))
    s.offset(distance=(espesor/2)+0.001,    objectList=(g[2], g[3], g[5], g[6], g[8], g[9], g[10], g[11]), side=RIGHT)
    s.delete(objectList=(g[11], g[6], g[2], g[3], g[5], g[9], g[8], g[10]))

    p = modelo.Part(name='espuma_hex', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = modelo.parts['espuma_hex']
    p.BaseSolidExtrude(sketch=s, depth=longitud)
    s.unsetPrimaryObject()
    del modelo.sketches['__profile__']


    # Material ----------------------------------------------------------------
    modelo.Material(name='ArmaFORM')
    mat_foam = modelo.materials['ArmaFORM']
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
    (50000, 400), ))

    modelo.HomogeneousSolidSection(name='sec_espuma',
        material='ArmaFORM', thickness=None)

    # Ensamblado, corte y mallado ---------------------------------------------
    p = modelo.parts['espuma_hex']
    v = p.vertices
    d = p.datums
    c = p.cells
    f = p.faces

    a.Instance(name='espuma_hex-1', part=p, dependent=ON)
    region = regionToolset.Region(cells=c[0:1])
    p.SectionAssignment(region=region, sectionName='sec_espuma', offset=0.0,
        offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)
    p.seedPart(size=espuma_seed_size, deviationFactor=0.1, minSizeFactor=0.1)

    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
        kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
        hourglassControl=COMBINED, weightFactor=0.5, distortionControl=ON, elemDeletion=ON, maxDegradation=0.4,
        lengthRatio=0.2)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
    p.setElementType(regions=(c[0:1], ), elemTypes=(elemType1, elemType2, elemType3))

    # Se disenho como un prisma hexagonal
    if opc['Relleno'] == 'FULL' or opc['Relleno'] == 'FOAM6':
        # Se marcan los datums
        p.DatumPlaneByThreePoints(point1=v[8], point2=v[5],  point3=v[4] )
        p.DatumPlaneByThreePoints(point1=v[6], point2=v[14], point3=v[15])
        p.DatumPlaneByThreePoints(point1=v[1], point2=v[11], point3=v[12])
        p.DatumPlaneByOffset(plane=d[5], flip=SIDE1, offset=tcomp/2)
        p.DatumPlaneByOffset(plane=d[5], flip=SIDE2, offset=tcomp/2)
        p.DatumPlaneByOffset(plane=d[6], flip=SIDE2, offset=tcomp/2)
        p.DatumPlaneByOffset(plane=d[6], flip=SIDE1, offset=tcomp/2)
        p.DatumPlaneByOffset(plane=d[7], flip=SIDE1, offset=tcomp/2)
        p.DatumPlaneByOffset(plane=d[7], flip=SIDE2, offset=tcomp/2)

        # Se corta por los datums
        p.PartitionCellByDatumPlane(cells=c[0:1], datumPlane=d[11])
        p.PartitionCellByDatumPlane(cells=c[1:2], datumPlane=d[10])
        p.PartitionCellByDatumPlane(cells=c[1:2], datumPlane=d[13])
        p.PartitionCellByDatumPlane(cells=c[2:3], datumPlane=d[12])
        p.PartitionCellByDatumPlane(cells=c[3:4], datumPlane=d[8])
        p.PartitionCellByDatumPlane(cells=c[4:5], datumPlane=d[9])
        p.PartitionCellByDatumPlane(cells=c[6:7], datumPlane=d[12])
        p.PartitionCellByDatumPlane(cells=c[7:8], datumPlane=d[13])
        p.PartitionCellByDatumPlane(cells=c[0:1], datumPlane=d[8])
        p.PartitionCellByDatumPlane(cells=c[1:2], datumPlane=d[9])

        # Se elimina el sobrante
        p.RemoveFaces(faceList = f[56:57],                                      deleteCells=False)
        p.RemoveFaces(faceList = f[42:43]+f[49:50]+f[51:53],                    deleteCells=False)
        p.RemoveFaces(faceList = f[36:37]+f[49:50],                             deleteCells=False)
        p.RemoveFaces(faceList = f[46:47],                                      deleteCells=False)
        p.RemoveFaces(faceList = f[21:22]+f[24:25]+f[26:27],                    deleteCells=False)
        p.RemoveFaces(faceList = f[37:38],                                      deleteCells=False)
        p.RemoveFaces(faceList = f[4:5],                                        deleteCells=False)
        p.RemoveFaces(faceList = f[5:6]+f[12:13]+f[15:16]+f[41:42],             deleteCells=False)
        p.RemoveFaces(faceList = f[11:12]+f[14:15]+f[21:22]+f[27:28]+f[34:35],  deleteCells=False)
        p.RemoveFaces(faceList = f[8:9]+f[22:23]+f[33:34],                      deleteCells=False)
        p.RemoveFaces(faceList = f[25:26]+f[30:31],                             deleteCells=False)
        p.RemoveFaces(faceList = f[8:9],                                        deleteCells=False)

        v1 = a.instances['espuma_hex-1'].vertices
        a.DatumPointByMidPoint(point1=v1[35], point2=v1[5])

    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
        kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
        hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=0.15)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
    p.setElementType(regions=(c[0:6], ), elemTypes=(elemType1, elemType2, elemType3))

    # Superficies de contacto -------------------------------------------------
    if opc['Relleno'] == 'FULL' or opc['Relleno'] == 'FOAM6':
        f = a.instances['espuma_hex-1'].faces

        # Sub-bloque 1
        ind = f.getClosest(coordinates=((0.0,                   2*ladov*coseno - espesor/2, longitud/2),    ))[0][0].index
        surf_foam_1 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1')
        ind = f.getClosest(coordinates=((ladoh/4 - 0.0001,      (3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_1a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1a')
        ind = f.getClosest(coordinates=((-ladoh/4 + 0.0001,     (3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_1b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1b')
        ind = f.getClosest(coordinates=((0.0,                   (3./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_1F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1F')
        ind = f.getClosest(coordinates=((0.0,                   (3./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_1R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1R')

        # Sub-bloque 2
        ind = f.getClosest(coordinates=((ladoh/2 + ladov*seno/2,(3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_2 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2')
        ind = f.getClosest(coordinates=((ladoh/2,               ladov*coseno + tcomp/2,     longitud/2),    ))[0][0].index
        surf_foam_2a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2a')
        ind = f.getClosest(coordinates=((ladoh/4 + 0.0001,      (3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_2b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2b')
        ind = f.getClosest(coordinates=((ladoh/2,               (3./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_2F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2F')
        ind = f.getClosest(coordinates=((ladoh/2,               (3./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_2R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2R')

        # Sub-bloque 3
        ind = f.getClosest(coordinates=((ladoh/2 + ladov*seno/2,(1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_3 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3')
        ind = f.getClosest(coordinates=((ladoh/4 + 0.0001,      (1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_3a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3a')
        ind = f.getClosest(coordinates=((ladoh/2,               ladov*coseno - tcomp/2,     longitud/2),    ))[0][0].index
        surf_foam_3b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3b')
        ind = f.getClosest(coordinates=((ladoh/2,               (1./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_3F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3F')
        ind = f.getClosest(coordinates=((ladoh/2,               (1./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_3R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3R')

        # Sub-bloque 4
        ind = f.getClosest(coordinates=((0.0,                   espesor/2,                  longitud/2),    ))[0][0].index
        surf_foam_4 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4')
        ind = f.getClosest(coordinates=((-ladoh/4 + 0.0001,     (1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_4a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4a')
        ind = f.getClosest(coordinates=((ladoh/4 - 0.0001,      (1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_4b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4b')
        ind = f.getClosest(coordinates=((0.0,                   (1./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_4F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4F')
        ind = f.getClosest(coordinates=((0.0,                   (1./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_4R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4R')

        # Sub-bloque 5
        ind = f.getClosest(coordinates=((-ladoh/2 -ladov*seno/2,(1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_5 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5')
        ind = f.getClosest(coordinates=((-ladoh/2,              ladov*coseno - tcomp/2,     longitud/2),    ))[0][0].index
        surf_foam_5a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5a')
        ind = f.getClosest(coordinates=((-ladoh/4 - 0.0001,     (1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_5b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5b')
        ind = f.getClosest(coordinates=((-ladoh/2,              (1./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_5F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5F')
        ind = f.getClosest(coordinates=((-ladoh/2,              (1./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_5R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5R')

        # Sub-bloque 6
        ind = f.getClosest(coordinates=((-ladoh/2 -ladov*seno/2,(3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_6 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6')
        ind = f.getClosest(coordinates=((-ladoh/4 - 0.0001,     (3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_6a = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6a')
        ind = f.getClosest(coordinates=((-ladoh/2,              ladov*coseno + tcomp/2,     longitud/2),    ))[0][0].index
        surf_foam_6b = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6b')
        ind = f.getClosest(coordinates=((-ladoh/2,              (3./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_6F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6F')
        ind = f.getClosest(coordinates=((-ladoh/2,              (3./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_6R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6R')

    elif opc['Relleno'] == 'FOAMHEX':
        f = a.instances['espuma_hex-1'].faces
        ind = f.getClosest(coordinates=((0.0,                   2*ladov*coseno - espesor/2, longitud/2),    ))[0][0].index
        surf_foam_1 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-1')
        ind = f.getClosest(coordinates=((ladoh/2 + ladov*seno/2,(3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_2 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-2')
        ind = f.getClosest(coordinates=((ladoh/2 + ladov*seno/2,(1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_3 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-3')
        ind = f.getClosest(coordinates=((0.0,                   espesor/2,                  longitud/2),    ))[0][0].index
        surf_foam_4 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-4')
        ind = f.getClosest(coordinates=((-ladoh/2 -ladov*seno/2,(1./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_5 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-5')
        ind = f.getClosest(coordinates=((-ladoh/2 -ladov*seno/2,(3./2)*ladov*coseno,        longitud/2),    ))[0][0].index
        surf_foam_6 = a.Surface(side1Faces=f[ind:ind+1], name='Foam-6')
        ind = f.getClosest(coordinates=((0.0,                   (1./2)*ladov*coseno,        longitud),      ))[0][0].index
        surf_foam_F = a.Surface(side1Faces=f[ind:ind+1], name='Foam-F')
        ind = f.getClosest(coordinates=((0.0,                   (1./2)*ladov*coseno,        0.0),           ))[0][0].index
        surf_foam_R = a.Surface(side1Faces=f[ind:ind+1], name='Foam-R')


#------------------------------------------------------------------------------
# GFRP
#------------------------------------------------------------------------------
# Pending update: referenced to x1, y1, x2, y2
if GFRP == True:
    # Geometria base ----------------------------------------------------------
    # GFRP-U
    anchocomp_U = sqrt((ladoh ** 2) + 4*((ladov*coseno)**2)) - holgura_GFRP
    s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)

    s.Line(point1=(longcomp/3,      surco/2),           point2=(longcomp,       surco/2))
    s.Line(point1=(longcomp,        surco/2),           point2=(longcomp,       anchocomp_U/2))
    s.Line(point1=(longcomp,        anchocomp_U/2),     point2=(0.0,            anchocomp_U/2))
    s.Line(point1=(0.0,             anchocomp_U/2),     point2=(0.0,            -anchocomp_U/2))
    s.Line(point1=(0.0,             -anchocomp_U/2),    point2=(longcomp,       -anchocomp_U/2))
    s.Line(point1=(longcomp,        -anchocomp_U/2),    point2=(longcomp,       -surco/2))
    s.Line(point1=(longcomp,        -surco/2),          point2=(longcomp/3,     -surco/2))
    s.Line(point1=(longcomp/3,      -surco/2),          point2=(longcomp/3,     surco/2))

    p = modelo.Part(name='GFRP_U', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = modelo.parts['GFRP_U']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    del modelo.sketches['__profile__']

    # GFRP-H
    anchocomp_H = 2*ladoh - holgura_GFRP
    s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)

    s.Line(point1=(2*longcomp/3,    surco/2),           point2=(longcomp,       surco/2))
    s.Line(point1=(longcomp,        surco/2),           point2=(longcomp,       anchocomp_H/2))
    s.Line(point1=(longcomp,        anchocomp_H/2),     point2=(0.0,            anchocomp_H/2))
    s.Line(point1=(0.0,             anchocomp_H/2),     point2=(0.0,            surco/2))
    s.Line(point1=(0.0,             surco/2),           point2=(longcomp/3,     surco/2))
    s.Line(point1=(longcomp/3,      surco/2),           point2=(longcomp/3,     -surco/2))
    s.Line(point1=(longcomp/3,      -surco/2),          point2=(0.0,            -surco/2))
    s.Line(point1=(0.0,             -surco/2),          point2=(0.0,            -anchocomp_H/2))
    s.Line(point1=(0.0,             -anchocomp_H/2),    point2=(longcomp,       -anchocomp_H/2))
    s.Line(point1=(longcomp,        -anchocomp_H/2),    point2=(longcomp,       -surco/2))
    s.Line(point1=(longcomp,        -surco/2),          point2=(2*longcomp/3,   -surco/2))
    s.Line(point1=(2*longcomp/3,    -surco/2),          point2=(2*longcomp/3,   surco/2))

    p = modelo.Part(name='GFRP_H', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = modelo.parts['GFRP_H']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    del modelo.sketches['__profile__']

    # Material ----------------------------------------------------------------
    if mats == 'PREDEF':
        mat_gfrp = modelo.Material(name='Ultramid A3WG10')
        mat_gfrp.Density(table=((1.55, ), ))
        mat_gfrp.Elastic(table=((10160000.0, 0.4), ))
        mat_gfrp.Plastic(hardening=USER, table=((254000.0, ), (0.0, )))
        mat_gfrp.DuctileDamageInitiation(table=((0.026, 1.0, 1.0), ))
        mat_gfrp.ductileDamageInitiation.DamageEvolution(type=DISPLACEMENT, table=((0.0, ), ))

        modelo.HomogeneousShellSection(name='sec_gfrp',
            preIntegrate=OFF, material='Ultramid A3WG10', thicknessType=UNIFORM,
            thickness=tcomp, thicknessField='', idealization=NO_IDEALIZATION,
            poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
            useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
    elif mats == 'USER':
        modelo.Material(name='GFRP')
        mat_gfrp = modelo.materials['GFRP']
        mat_gfrp.Density(table=((1.55, ), ))
        mat_gfrp.Elastic(table=((16247251.141291289, 0.4), ))
        mat_gfrp.Plastic(hardening=USER,
            table=((25000.0,    ),
                (0.0,           ),
                (124866.828374, ),
                (44221.2086877, ),
                (315.896358458, ),
                (5748.46332314, ),
                (0.0,           ),
                (3.25E-5,       )))
        mat_gfrp.DuctileDamageInitiation(table=((0.0111019107183, 0.33, 3.25E-5), ))
        mat_gfrp.ductileDamageInitiation.DamageEvolution(type=DISPLACEMENT, table=((0.0, ), ))

        modelo.HomogeneousShellSection(name='sec_gfrp',
            preIntegrate=OFF, material='GFRP', thicknessType=UNIFORM,
            thickness=tcomp, thicknessField='', idealization=NO_IDEALIZATION,
            poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
            useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)

    p = modelo.parts['GFRP_H']
    region = regionToolset.Region(faces=p.faces[0:1])
    p.SectionAssignment(region=region, sectionName='sec_gfrp', offset=0.0,
        offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)

    p = modelo.parts['GFRP_U']
    region = regionToolset.Region(faces=p.faces[0:1])
    p.SectionAssignment(region=region, sectionName='sec_gfrp', offset=0.0,
        offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)

    # Ensamblado --------------------------------------------------------------
    p = modelo.parts['GFRP_U']
    a.Instance(name='GFRP_U-1', part=p, dependent=ON)

    a.rotate(instanceList=('GFRP_U-1', ),       axisPoint=(0.0, 0.0,            0.0),   axisDirection=(0.0, 1.0, 0.0),  angle=90.0)
    a.translate(instanceList=('GFRP_U-1', ),    vector=(0.0,    ladov*coseno,   longitud - holgura_GFRP/2))
    a.rotate(instanceList=('GFRP_U-1', ),       axisPoint=(0.0, ladov*coseno,   0.0),   axisDirection=(0.0, 0.0, -1.0), angle=angulo)

    p = modelo.parts['GFRP_U']
    a.Instance(name='GFRP_U-2', part=p, dependent=ON)

    a.rotate(instanceList=('GFRP_U-2', ),       axisPoint=(0.0, 0.0,            0.0),   axisDirection=(0.0, 1.0, 0.0),  angle=-90.0)
    a.translate(instanceList=('GFRP_U-2', ),    vector=(0.0,    ladov*coseno,   holgura_GFRP/2))
    a.rotate(instanceList=('GFRP_U-2', ),       axisPoint=(0.0, ladov*coseno,   0.0),   axisDirection=(0.0, 0.0, -1.0), angle=-angulo)

    p = modelo.parts['GFRP_H']
    a.Instance(name='GFRP_H-1', part=p, dependent=ON)

    a.translate(instanceList=('GFRP_H-1', ),    vector=(0.0,    ladov*coseno,   0.0))
    a.rotate(instanceList=('GFRP_H-1', ),       axisPoint=(0.0, 0.0,            0.0),   axisDirection=(0.0, -1.0, 0.0), angle=90.0)
    a.translate(instanceList=('GFRP_H-1', ),    vector=(0.0,    0.0,            holgura_GFRP/2))
    a.rotate(instanceList=('GFRP_H-1', ),       axisPoint=(0.0, ladov*coseno,   0.0),   axisDirection=(0.0, 0.0, -1.0), angle=90.0)

    # Mallado -----------------------------------------------------------------
    elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=EXPLICIT,
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT)

    p = modelo.parts['GFRP_H']
    p.seedPart(size=GFRP_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
    p.setMeshControls(regions=p.faces[0:1], algorithm=MEDIAL_AXIS)
    p.setElementType(regions=(p.faces[0:1], ), elemTypes=(elemType1, elemType2))

    p = modelo.parts['GFRP_U']
    p.seedPart(size=GFRP_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
    p.setMeshControls(regions=p.faces[0:1], algorithm=MEDIAL_AXIS)
    p.setElementType(regions=(p.faces[0:1], ), elemTypes=(elemType1, elemType2))

    # Superficies -------------------------------------------------------------
    GFRP_U1 = a.Surface(side1Faces=a.instances['GFRP-U-1'].faces[0:1], side2Faces=a.instances['GFRP-U-1'].faces[0:1], name='GFRP_U1')
    GFRP_U2 = a.Surface(side1Faces=a.instances['GFRP-U-2'].faces[0:1], side2Faces=a.instances['GFRP-U-2'].faces[0:1], name='GFRP_U2')
    GFRP_H1 = a.Surface(side1Faces=a.instances['GFRP-H-1'].faces[0:1], side2Faces=a.instances['GFRP-H-1'].faces[0:1], name='GFRP_H1')


#------------------------------------------------------------------------------
# Adhesivo
#------------------------------------------------------------------------------
if adhesivo == True:
    espads = opc['Espesor adhesivo']
    # Geometria base ----------------------------------------------------------
    # Sketch
    s = modelo.ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)

    s.rectangle(point1=(0.0, 0.0), point2=(aleta, longitud))

    # Creacion parte
    p = modelo.Part(name='Adhesivo', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = modelo.parts['Adhesivo']
    p.BaseSolidExtrude(sketch=s, depth=opc['Espesor adhesivo'])

    s.unsetPrimaryObject()
    del modelo.sketches['__profile__']


    # Material ----------------------------------------------------------------
    if adhesive_name == 'Loctite Hysol 9514':
        matads = modelo.Material(name=adhesive_name)
        matads.Density(table=((1.46, ), ))  # Between 1.42 & 1.48 (catalog)

        # Elastic-plastic w/ ductile damage -----------------------------------
        # matads.Elastic(table=((1460000.0, 0.295), )) # E from manufacturer spec; nu from J.Diaz SLJ
        # matads.Plastic(table=((44000.0, 0.0), )) # Stress limit
        # matads.DuctileDamageInitiation(table=((0.001, 1.0, 1.0), )) # Small ductile branch
        # matads.ductileDamageInitiation.DamageEvolution(type=ENERGY, table=((0.905, ), )) # Sadowski-like

        # Coupled Traction w/ Quads damage ------------------------------------
        # matads.Elastic(type=COUPLED_TRACTION, table=((1460000.0, 1460000.0, 1460000.0, 563707.0, 563707.0, 563707.0), ))
        # matads.QuadsDamageInitiation(table=((44000.0, 45000.0, 45000.0), ))
        # matads.quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=POWER_LAW,
        #   power=2.0, table=((0.905, 0.905, 0.905), ))

        # Traction w/ Quads damage --------------------------------------------
        #matads.Elastic(type=TRACTION, table=((1795800./espads, 693359./espads, 693359./espads), ))  # From bulk moduli (manufacturer) & J.Diaz SLJ
        matads.Elastic(type=TRACTION, table=((5000000000., 80000000., 80000000.), ))
        #matads.QuadsDamageInitiation(table=((44000.0, 45000.0, 45000.0), )) # From manufacturer specs (tensile strength & lap shear strength twice)
        matads.QuadsDamageInitiation(table=((130000.0, 42500.0, 42500.0), )) # From manufacturer specs (tensile strength & lap shear strength twice)
        # matads.quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=POWER_LAW, power=2.0, table=((0.905, 0.905, 0.905), )) # From Sadowski, among others
        matads.quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=POWER_LAW, power=2.0, table=((2.028*G_int, 11.853*G_int, 11.853*G_int), )) # From Sadowski, among others
        matads.quadsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=0.0001)

        # Interaction ---------------------------------------------------------
        intadsprops = modelo.ContactProperty(intadhesive_name)
        #intadsprops.NormalBehavior(pressureOverclosure=HARD, allowSeparation=OFF, constraintEnforcementMethod=DEFAULT)
        #intadsprops.TangentialBehavior(formulation=ROUGH)
        intadsprops.CohesiveBehavior(eligibility=ALL_NODES)
        # intadsprops.Damage(criterion=QUAD_TRACTION, initTable=((9500.0, 40000.0, 40000.0), ), # From manufacturer specs for steel
           #  useEvolution=ON, evolutionType=ENERGY, useMixedMode=ON, # Evolution needed (manual: w/o it, it's computed, but not applied)
           #  mixedModeType=POWER_LAW, exponent=2.0,
           #  evolTable=((2.028, 11.853, 11.853), ))  # Scattina
        intadsprops.Damage(criterion=QUAD_TRACTION, initTable=((9500.0, 40000.0, 40000.0), ), # From manufacturer specs for steel
            useEvolution=ON, evolutionType=ENERGY, useMixedMode=ON, # Evolution needed (manual: w/o it, it's computed, but not applied)
            mixedModeType=POWER_LAW, exponent=2.0,
            evolTable=((2.028*GIc, 11.853*GIIc, 11.853*GIIc), ))  # Scattina

    # modelo.HomogeneousSolidSection(name='Sec_' + adhesive_name,
    #    material=adhesive_name, thickness=None)
    modelo.CohesiveSection(name='SecCoh_' + adhesive_name,
        material=adhesive_name, response=TRACTION_SEPARATION,
        initialThicknessType=GEOMETRY,
        outOfPlaneThickness=None)

    p = modelo.parts['Adhesivo']
    e = p.edges
    c = p.cells

    region = regionToolset.Region(cells=p.cells[0:1])
    # p.SectionAssignment(region=region, sectionName='Sec_' + adhesive_name, offset=0.0,
 #      offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    p.SectionAssignment(region=region, sectionName='SecCoh_' + adhesive_name,
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)


    p.assignStackDirection(referenceRegion=p.faces[4], cells=p.cells[0:1])
    p.MaterialOrientation(region=regionToolset.Region(cells=p.cells[0:1]),
        orientationType=GLOBAL, axis=AXIS_1, additionalRotationType=ROTATION_NONE,
        localCsys=None, fieldName='', stackDirection=STACK_3)

    # Mallado -----------------------------------------------------------------
    p.seedPart(size=ads_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
    pickedEdges = e[1:2]+e[3:4]+e[5:6]+e[8:9]
    p.seedEdgeByNumber(edges=pickedEdges, number=ads_seed_nesp, constraint=FINER)

    # elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
    #    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
    #    hourglassControl=DEFAULT, distortionControl=DEFAULT, elemDeletion=ON)
    # elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    # elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)

    elemType1 = mesh.ElemType(elemCode=COH3D8, elemLibrary=EXPLICIT, elemDeletion=ON, linearBulkViscosity=0.)
    elemType2 = mesh.ElemType(elemCode=COH3D6, elemLibrary=EXPLICIT, elemDeletion=ON, linearBulkViscosity=0.)
    elemType3 = mesh.ElemType(elemCode=UNKNOWN_TET, elemLibrary=EXPLICIT, elemDeletion=ON, linearBulkViscosity=0.)

    p.setElementType(regions=(c[0:1], ), elemTypes=(elemType1, elemType2, elemType3))

    # Ensamblado --------------------------------------------------------------
    if not halfm:
        a.Instance(name='Adhesivo-1', part=p, dependent=ON)
        a.Instance(name='Adhesivo-2', part=p, dependent=ON)
        #a.translate(instanceList=('Adhesivo-1', ), vector=(ladoh/2 + ladov*seno,        ladov*coseno + opc['Espesor adhesivo'],     0.0))
        #a.translate(instanceList=('Adhesivo-2', ), vector=(-ladoh/2 -ladov*seno - aleta, ladov*coseno + opc['Espesor adhesivo'],    0.0))
        a.translate(instanceList=('Adhesivo-1', ), vector=(x1,          y1 + espads/2,  0.0))
        a.translate(instanceList=('Adhesivo-2', ), vector=(-x1 - aleta, y1 + espads/2,  0.0))
        a.rotate(instanceList=('Adhesivo-1', 'Adhesivo-2', ),
            #axisPoint=(0.0, ladov*coseno + opc['Espesor adhesivo'], 0.0),
            axisPoint=(0.0, y1 + espads/2, 0.0),
            axisDirection=(1.0, 0.0, 0.0), angle=90.0)
    else:
        a.Instance(name='Adhesivo-1', part=p, dependent=ON)
        #a.translate(instanceList=('Adhesivo-1', ), vector=(ladoh/2 + ladov*seno,        ladov*coseno + opc['Espesor adhesivo'],     0.0))
        #a.translate(instanceList=('Adhesivo-2', ), vector=(-ladoh/2 -ladov*seno - aleta, ladov*coseno + opc['Espesor adhesivo'],    0.0))
        a.translate(instanceList=('Adhesivo-1', ), vector=(x1,          y1 + espads/2,  0.0))
        a.rotate(instanceList=('Adhesivo-1', ),
            #axisPoint=(0.0, ladov*coseno + opc['Espesor adhesivo'], 0.0),
            axisPoint=(0.0, y1 + espads/2, 0.0),
            axisDirection=(1.0, 0.0, 0.0), angle=90.0)


    # Superficies de contacto -------------------------------------------------
    if not halfm:
        Ads1_bot = a.Surface(side1Faces=a.instances['Adhesivo-1'].faces[4:5],   name='Ads1_bot')
        Ads1_top = a.Surface(side1Faces=a.instances['Adhesivo-1'].faces[5:6],   name='Ads1_top')
        Ads2_bot = a.Surface(side1Faces=a.instances['Adhesivo-2'].faces[4:5],   name='Ads2_bot')
        Ads2_top = a.Surface(side1Faces=a.instances['Adhesivo-2'].faces[5:6],   name='Ads2_top')
    else:
        Ads1_bot = a.Surface(side1Faces=a.instances['Adhesivo-1'].faces[4:5],   name='Ads1_bot')
        Ads1_top = a.Surface(side1Faces=a.instances['Adhesivo-1'].faces[5:6],   name='Ads1_top')

    # Set de elementos del adhesivo
    if not halfm:
        ads_elemSet = a.Set(elements=a.instances['Adhesivo-1'].elements + a.instances['Adhesivo-2'].elements, name='Ads_ElemSet')
        ads_set     = a.Set(cells=a.instances['Adhesivo-1'].cells[0:1] + a.instances['Adhesivo-2'].cells[0:1], name='Ads_Set')
    else:
        ads_elemSet = a.Set(elements=a.instances['Adhesivo-1'].elements, name='Ads_ElemSet')
        ads_set     = a.Set(cells=a.instances['Adhesivo-1'].cells[0:1], name='Ads_Set')



#==============================================================================
# Step
#==============================================================================

# Step Impacto
modelo.ExplicitDynamicsStep(name='Impacto', previous='Initial', timePeriod=steptime)

# Output Requests
modelo.HistoryOutputRequest(name='H/EO', variables=(
    'ALLAE',            # Artificial strain energy
    'ALLDMD',           # Damage dissipation energy
    'ALLIE',            # Internal energy
    'ALLKE',            # Kinetic energy
    'ALLPD',            # Plastic dissipation
    'ALLSE',            # Strain energy
    'ALLVD',            # Viscous dissipation
    'ALLWK',            # External work
    'ETOTAL',
    ), createStepName='Impacto')

if adhesivo == True:
    modelo.FieldOutputRequest(name='F/O', variables=(
        'RF',               # Reaction forces & moments
        'S',                # Stress components & invariants
        'STATUS',           # Status (some failure & plasticity models; VUMAT)
        'PEEQ',             # Equivalent plastic strain
        'E',                # Total strain components
        'U',                # Translations & rotations
        # 'CSQUADSCRT',     # Quadratic traction damage initiation criterion
        # 'CSDMG',          # Scalar stiffness degradation for cohesive surfaces
        # 'CSTRESS',        # Contact stresses
        ), createStepName='Impacto', numIntervals=interv)
    modelo.HistoryOutputRequest(name='H/Ads', variables=(
        'QUADSCRT',
        ), createStepName='Impacto', numIntervals=interv, region=ads_set,
        sectionPoints=DEFAULT, rebar=EXCLUDE)
else:
    modelo.FieldOutputRequest(name='F/O', variables=(
        'RF',               # Reaction forces & moments
        'S',                # Stress components & invariants
        'STATUS',           # Status (some failure & plasticity models; VUMAT)
        'PEEQ',             # Equivalent plastic strain
        'U'),               # Translations & rotations
        createStepName='Impacto', numIntervals=interv)


try:
    del modelo.fieldOutputRequests['F-Output-1']  # Se crea auto/ F-Output-1. Se elimina...
    del modelo.historyOutputRequests['H-Output-1']  # Idem
except:
    pass # ...o se pasa si no se puede


#==============================================================================
# Cargas
#==============================================================================

#------------------------------------------------------------------------------
# Placas de impacto
#------------------------------------------------------------------------------

# Geometria base --------------------------------------------------------------
s = modelo.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)

s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(2*lado, 0.0))

p = modelo.Part(name='Placa', dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
p = modelo.parts['Placa']
p.BaseShell(sketch=s)

s.unsetPrimaryObject()
del modelo.sketches['__profile__']

a.Instance(name='Placa-1', part=p, dependent=ON)
a.translate(instanceList=('Placa-1', ), vector=(0.0, y1+espads/2, 0.0))

a.LinearInstancePattern(instanceList=('Placa-1', ), direction1=(0.0, 0.0, 1.0),
    direction2=(0.0, 1.0, 0.0), number1=2, number2=1, spacing1=longitud + 0.001,
    spacing2=0.3)

# Se ocultan por visualizacion
session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=(
    'Placa-1', 'Placa-1-lin-2-1', ))

# Mallado ---------------------------------------------------------------------
p = modelo.parts['Placa']
p.seedPart(size=0.05, deviationFactor=0.1, minSizeFactor=0.1)

# Movimiento placas -----------------------------------------------------------
modelo.TabularAmplitude(name='Amp-1', timeSpan=STEP,
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (steptime, 1.0)))

# Placa con movimiento
e1 = a.instances['Placa-1'].edges
RP_mov = a.ReferencePoint(point=a.instances['Placa-1'].InterestingPoint(edge=e1[0], rule=CENTER))

region1 = a.Set(faces=a.instances['Placa-1'].faces[0:1], name='Placa_mov')
region2 = regionToolset.Region(referencePoints=(a.referencePoints[RP_mov.id], ))
modelo.RigidBody(name='PlacaMov-RP', refPointRegion=region2,
    bodyRegion=region1, refPointAtCOM=ON)

modelo.DisplacementBC(name='MovPlaca', createStepName='Impacto',    u1=0.0,             ur1=0.0,
    region=region2, distributionType=UNIFORM, amplitude='Amp-1',    u2=0.0,             ur2=0.0,
    fixed=OFF,  fieldName='', localCsys=None,                       u3=(delta + 0.001), ur3=0.0)


# Placa fija
e11 = a.instances['Placa-1-lin-2-1'].edges
RP_fixed = a.ReferencePoint(point=a.instances['Placa-1-lin-2-1'].InterestingPoint(edge=e11[0], rule=CENTER))

region1 = a.Set(faces=a.instances['Placa-1-lin-2-1'].faces[0:1], name='Plava_fix')
region2 = regionToolset.Region(referencePoints=(a.referencePoints[RP_fixed.id], ))
modelo.RigidBody(name='PlacaFij', refPointRegion=region2,
    bodyRegion=region1, refPointAtCOM=ON)
modelo.EncastreBC(name='FijPlaca', createStepName='Initial', region=region2, localCsys=None)


# Superficies
Placa_mov = a.Surface(side1Faces=a.instances['Placa-1'].faces[0:1],             name='Placa_mov')
Placa_fix = a.Surface(side2Faces=a.instances['Placa-1-lin-2-1'].faces[0:1],     name='Placa_fix')

#------------------------------------------------------------------------------
# Sujecion extremo opuesto
#------------------------------------------------------------------------------
if not halfm:
    # Particion
    p = modelo.parts['Chapa']
    f = p.faces
    d = p.datums

    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=longitud - 0.005)
    p.PartitionFaceByDatumPlane(datumPlane=d[5], faces=f[0:5])

    # Evitar viajes 'hasta el infinito y mas alla' (mov base solo en dir extrusion)
    f1 = a.instances['Chapa-2'].faces
    f2 = a.instances['Chapa-1'].faces
    region = regionToolset.Region(faces=f1[0:4]+f1[5:6]+f2[0:4]+f2[5:6])
    modelo.DisplacementBC(name='Clamp', createStepName='Impacto',   u1=0.0,     ur1=0.0,
        region=region, distributionType=UNIFORM, amplitude=UNSET,   u2=0.0,     ur2=0.0,
        fixed=OFF, fieldName='', localCsys=None,                    u3=UNSET,   ur3=0.0)
else:
    # Particion
    p = modelo.parts['partChapaBot']; f = p.faces; d = p.datums
    dp = p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=longitud - 0.005)
    p.PartitionFaceByDatumPlane(datumPlane=d[5], faces=f[:])

    p = modelo.parts['partChapaTop']; f = p.faces; d = p.datums
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=longitud - 0.005)
    p.PartitionFaceByDatumPlane(datumPlane=d[5], faces=f[:])

    # Evitar viajes 'hasta el infinito y mas alla' (mov base solo en dir extrusion)
    f1 = a.instances['Chapa-1'].faces
    f2 = a.instances['Chapa-2'].faces
    region = regionToolset.Region(faces=f1[0:2]+f1[3:4]+f2[3:6])
    modelo.DisplacementBC(name='Clamp', createStepName='Impacto',   u1=0.0,     ur1=0.0,
        region=region, distributionType=UNIFORM, amplitude=UNSET,   u2=0.0,     ur2=0.0,
        fixed=OFF, fieldName='', localCsys=None,                    u3=UNSET,   ur3=0.0)

# Symmetry --------------------------------------------------------------------
if halfm:
    e1 = a.instances['Chapa-1'].edges
    e2 = a.instances['Chapa-2'].edges
    region = regionToolset.Region(edges=e1[3:4]+e1[15:16]+e2[3:4]+e2[15:16])
    modelo.XsymmBC(name='SymBC', createStepName='Initial',
        region=region, localCsys=None)


#------------------------------------------------------------------------------
# Trigger
#------------------------------------------------------------------------------
if trigger == 'Holes':
    s = modelo.ConstrainedSketch(name='__profile__', sheetSize=0.05)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)

    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.002, 0.0))

    p = modelo.Part(name='Taladro', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = modelo.parts['Taladro']
    p.BaseSolidExtrude(sketch=s, depth=0.05)

    s.unsetPrimaryObject()
    del modelo.sketches['__profile__']

    if not halfm:
        a.Instance(name='T1_top', part=p, dependent=ON)
        a.rotate(instanceList=('T1_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T1_top', ), vector=(0.01, -0.005, 0.02))

        a.Instance(name='T2_top', part=p, dependent=ON)
        a.rotate(instanceList=('T2_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T2_top', ), vector=(-0.01, -0.005, 0.02))

        a.Instance(name='T3_top', part=p, dependent=ON)
        a.rotate(instanceList=('T3_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T3_top', ), vector=(-0.005, 0.03, 0.02))

        a.Instance(name='T4_top', part=p, dependent=ON)
        a.rotate(instanceList=('T4_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T4_top', ), vector=(-0.045, 0.03, 0.02))

        a.Instance(name='T1_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T1_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T1_bot', ), vector=(0.01, -0.005, 0.02))

        a.Instance(name='T2_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T2_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T2_bot', ), vector=(-0.01, -0.005, 0.02))

        a.Instance(name='T3_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T3_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T3_bot', ), vector=(-0.005, 0.01, 0.02))

        a.Instance(name='T4_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T4_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T4_bot', ), vector=(-0.045, 0.01, 0.02))

        ChapaTop = a.InstanceFromBooleanCut(name='ChapaTop', instanceToBeCut=a.instances['Chapa-2'], originalInstances=SUPPRESS,
            cuttingInstances=(a.instances['T1_top'], a.instances['T2_top'], a.instances['T3_top'], a.instances['T4_top'], ))
        ChapaBot = a.InstanceFromBooleanCut(name='ChapaBot', instanceToBeCut=a.instances['Chapa-1'], originalInstances=SUPPRESS,
            cuttingInstances=(a.instances['T1_bot'], a.instances['T2_bot'], a.instances['T3_bot'], a.instances['T4_bot'], ))

        modelo.parts['ChapaTop'].seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        modelo.parts['ChapaBot'].seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        a.regenerate()

        # Nuevas superficies de contacto -----------------------------------------------------
        # ChapaBot
        x1b = x1; y1b = y1-(espesor+espads)/2; x2b = x2; y2b = y2
        s = a.instances['ChapaBot-1'].faces.findAt(((x1b+aleta/2, y1b, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((x1b+aleta/2, y1b, longitud - 0.0025), ))
        Ch1_u1      = a.Surface(side1Faces=s,   name='Ch1_u1')   # Union 1
        Ch1_ext_u1  = a.Surface(side2Faces=s,   name='Ch1_ext_u1')
        s = a.instances['ChapaBot-1'].faces.findAt((((x1b+x2b)/2, (y1b+y2b)/2, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt((((x1b+x2b)/2, (y1b+y2b)/2, longitud - 0.0025), ))
        Ch1_int5    = a.Surface(side1Faces=s,   name='Ch1_int5')
        Ch1_ext5    = a.Surface(side2Faces=s,   name='Ch1_ext5')
        s = a.instances['ChapaBot-1'].faces.findAt(((0., y2b, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((0., y2b, longitud - 0.0025), ))
        Ch1_int4    = a.Surface(side1Faces=s,   name='Ch1_int4')
        Ch1_ext4    = a.Surface(side2Faces=s,   name='Ch1_ext4')
        s = a.instances['ChapaBot-1'].faces.findAt(((-(x1b+x2b)/2, (y1b+y2b)/2, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((-(x1b+x2b)/2, (y1b+y2b)/2, longitud - 0.0025), ))
        Ch1_int3    = a.Surface(side1Faces=s,   name='Ch1_int3')
        Ch1_ext3    = a.Surface(side2Faces=s,   name='Ch1_ext3')
        s = a.instances['ChapaBot-1'].faces.findAt(((-x1b-aleta/2, y1b, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((-x1b-aleta/2, y1b, longitud - 0.0025), ))
        Ch1_u2      = a.Surface(side1Faces=s,   name='Ch1_u2')   # Union 2
        Ch1_ext_u2  = a.Surface(side2Faces=s,   name='Ch1_ext_u2')
        Ch1_all = [Ch1_u2, Ch1_ext_u2, Ch1_int5, Ch1_ext5, Ch1_int4, Ch1_ext4, Ch1_int3, Ch1_ext3, Ch1_u1, Ch1_ext_u1]

        # ChapaTop
        x1t = x1; y1t = y1+(espesor+espads)/2; x2t = x2; y2t = 2*y1
        s = a.instances['ChapaTop-1'].faces.findAt(((x1t+aleta/2, y1t, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((x1t+aleta/2, y1t, longitud - 0.0025), ))
        Ch2_u1      = a.Surface(side1Faces=s,   name='Ch2_u2')   # Union 1
        Ch2_ext_u1  = a.Surface(side2Faces=s,   name='Ch2_ext_u1')
        s = a.instances['ChapaTop-1'].faces.findAt((((x1t+x2t)/2, (y1t+y2t)/2, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt((((x1t+x2t)/2, (y1t+y2t)/2, longitud - 0.0025), ))
        Ch2_int2    = a.Surface(side1Faces=s,   name='Ch2_int2')
        Ch2_ext2    = a.Surface(side2Faces=s,   name='Ch2_ext2')
        s = a.instances['ChapaTop-1'].faces.findAt(((0., y2t, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((0., y2t, longitud - 0.0025), ))
        Ch2_int1    = a.Surface(side1Faces=s,   name='Ch2_int1')
        Ch2_ext1    = a.Surface(side2Faces=s,   name='Ch2_ext1')
        s = a.instances['ChapaTop-1'].faces.findAt(((-(x1t+x2t)/2, (y1t+y2t)/2, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((-(x1t+x2t)/2, (y1t+y2t)/2, longitud - 0.0025), ))
        Ch2_int6    = a.Surface(side1Faces=s,   name='Ch2_int6')
        Ch2_ext6    = a.Surface(side2Faces=s,   name='Ch2_ext6')
        s = a.instances['ChapaTop-1'].faces.findAt(((-x1t-aleta/2, y1t, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((-x1t-aleta/2, y1t, longitud - 0.0025), ))
        Ch2_u2      = a.Surface(side1Faces=s,   name='Ch2_u1')   # Union 2
        Ch2_ext_u2  = a.Surface(side2Faces=s,   name='Ch2_ext_u2')
        Ch2_all = [Ch2_u1, Ch2_ext_u1, Ch2_int2, Ch2_ext2, Ch2_int1, Ch2_ext1, Ch2_int6, Ch2_ext6, Ch2_u2, Ch2_ext_u2]

    else:
        a.Instance(name='T1_top', part=p, dependent=ON)
        a.rotate(instanceList=('T1_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T1_top', ), vector=(0.01, -0.005, 0.02))

        a.Instance(name='T3_top', part=p, dependent=ON)
        a.rotate(instanceList=('T3_top', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T3_top', ), vector=(-0.005, 0.03, 0.02))

        a.Instance(name='T1_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T1_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(-1.0, 0.0, 0.0), angle=90.0)
        a.translate(instanceList=('T1_bot', ), vector=(0.01, -0.005, 0.02))

        a.Instance(name='T3_bot', part=p, dependent=ON)
        a.rotate(instanceList=('T3_bot', ), axisPoint=(0.0, 0.0, 0.0),  axisDirection=(0.0, 1.0, 0.0), angle=90.0)
        a.translate(instanceList=('T3_bot', ), vector=(-0.005, 0.01, 0.02))

        ChapaTop = a.InstanceFromBooleanCut(name='ChapaTop', instanceToBeCut=a.instances['Chapa-2'], originalInstances=SUPPRESS,
            cuttingInstances=(a.instances['T1_top'], a.instances['T3_top'], ))
        ChapaBot = a.InstanceFromBooleanCut(name='ChapaBot', instanceToBeCut=a.instances['Chapa-1'], originalInstances=SUPPRESS,
            cuttingInstances=(a.instances['T1_bot'], a.instances['T3_bot'], ))

        modelo.parts['ChapaTop'].seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        modelo.parts['ChapaBot'].seedPart(size=chapa_seed_size, deviationFactor=0.1, minSizeFactor=0.1)
        a.regenerate()

        # Nuevas superficies de contacto -----------------------------------------------------
        # ChapaBot
        x1b = x1; y1b = y1-(espesor+espads)/2; x2b = x2; y2b = y2
        s = a.instances['ChapaBot-1'].faces.findAt(((x1b+aleta/2, y1b, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((x1b+aleta/2, y1b, longitud - 0.0025), ))
        Ch1_u1      = a.Surface(side2Faces=s,   name='Ch1_u1')   # Union 1
        Ch1_ext_u1  = a.Surface(side1Faces=s,   name='Ch1_ext_u1')
        s = a.instances['ChapaBot-1'].faces.findAt(((0., y2b, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt(((0., y2b, longitud - 0.0025), ))
        Ch1_int4    = a.Surface(side2Faces=s,   name='Ch1_int4')
        Ch1_ext4    = a.Surface(side1Faces=s,   name='Ch1_ext4')
        s = a.instances['ChapaBot-1'].faces.findAt((((x1b+x2b)/2, (y1b+y2b)/2, longitud/2), )) +\
            a.instances['ChapaBot-1'].faces.findAt((((x1b+x2b)/2, (y1b+y2b)/2, longitud - 0.0025), ))
        Ch1_int3    = a.Surface(side2Faces=s,   name='Ch1_int3')
        Ch1_ext3    = a.Surface(side1Faces=s,   name='Ch1_ext3')
        Ch1_all = [Ch1_int4, Ch1_ext4, Ch1_int3, Ch1_ext3, Ch1_u1, Ch1_ext_u1]

        # ChapaTop
        x1t = x1; y1t = y1+(espesor+espads)/2; x2t = x2; y2t = 2*y1
        s = a.instances['ChapaTop-1'].faces.findAt(((x1t+aleta/2, y1t, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((x1t+aleta/2, y1t, longitud - 0.0025), ))
        Ch2_u1      = a.Surface(side2Faces=s,   name='Ch2_u2')   # Union 1
        Ch2_ext_u1  = a.Surface(side1Faces=s,   name='Ch2_ext_u1')
        s = a.instances['ChapaTop-1'].faces.findAt((((x1t+x2t)/2, (y1t+y2t)/2, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt((((x1t+x2t)/2, (y1t+y2t)/2, longitud - 0.0025), ))
        Ch2_int2    = a.Surface(side2Faces=s,   name='Ch2_int2')
        Ch2_ext2    = a.Surface(side1Faces=s,   name='Ch2_ext2')
        s = a.instances['ChapaTop-1'].faces.findAt(((0., y2t, longitud/2), )) +\
            a.instances['ChapaTop-1'].faces.findAt(((0., y2t, longitud - 0.0025), ))
        Ch2_int1    = a.Surface(side2Faces=s,   name='Ch2_int1')
        Ch2_ext1    = a.Surface(side1Faces=s,   name='Ch2_ext1')
        Ch2_all = [Ch2_u1, Ch2_ext_u1, Ch2_int2, Ch2_ext2, Ch2_int1, Ch2_ext1]

    # # Partition edges
    # p = modelo.parts['ChapaBot']
    # p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.04)
    # p.PartitionEdgeByDatumPlane(datumPlane=p.datums[4], edges=p.edges[14:15]+p.edges[25:26])

    # p = modelo.parts['ChapaTop']
    # p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.04)
    # p.PartitionEdgeByDatumPlane(datumPlane=p.datums[4], edges=p.edges[14:15]+p.edges[25:26])

    # # Impossed deformation
    # modelo.ExplicitDynamicsStep(name='Trigger', previous='Initial', timePeriod=0.005)
    # modelo.TabularAmplitude(name='Trig', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.005, 1.0)))

    # # In holes
    # region = regionToolset.Region(edges=a.instances['ChapaTop-1'].edges[22:24])
    # modelo.DisplacementBC(name='TriggerTop', createStepName='Trigger',        u1=UNSET,       ur1=UNSET,
    #   region=region, distributionType=UNIFORM, amplitude='Trig',          u2=-0.005,      ur2=UNSET,
    #   fixed=OFF, fieldName='', localCsys=None,                            u3=UNSET,       ur3=UNSET)

    # region = regionToolset.Region(edges=a.instances['ChapaBot-1'].edges[22:24])
    # modelo.DisplacementBC(name='TriggerBot', createStepName='Trigger',        u1=UNSET,       ur1=UNSET,
    #   region=region, distributionType=UNIFORM, amplitude='Trig',          u2=0.005,       ur2=UNSET,
    #   fixed=OFF, fieldName='', localCsys=None,                            u3=UNSET,       ur3=UNSET)

    # # In unions
    # region = regionToolset.Region(vertices=a.instances['ChapaTop-1'].vertices[11:12]+a.instances['ChapaBot-1'].vertices[19:20])
    # modelo.DisplacementBC(name='Trigger_U1', createStepName='Trigger',        u1=-0.005,      ur1=UNSET,
    #   region=region, distributionType=UNIFORM, amplitude='Trig',          u2=UNSET,       ur2=UNSET,
    #   fixed=OFF, fieldName='', localCsys=None,                            u3=UNSET,       ur3=UNSET)

    # region = regionToolset.Region(vertices=a.instances['ChapaTop-1'].vertices[19:20]+a.instances['ChapaBot-1'].vertices[11:12])
    # modelo.DisplacementBC(name='Trigger_U2', createStepName='Trigger',        u1=0.005,       ur1=UNSET,
    #   region=region, distributionType=UNIFORM, amplitude='Trig',          u2=UNSET,       ur2=UNSET,
    #   fixed=OFF, fieldName='', localCsys=None,                            u3=UNSET,       ur3=UNSET)

    # modelo.boundaryConditions['TriggerTop'].deactivate('Impacto')
    # modelo.boundaryConditions['TriggerBot'].deactivate('Impacto')
    # modelo.boundaryConditions['Trigger_U1'].deactivate('Impacto')
    # modelo.boundaryConditions['Trigger_U2'].deactivate('Impacto')

    # # Fixing during trigger
    # region = regionToolset.Region(referencePoints=(a.referencePoints[RP_mov.id], ))
    # modelo.EncastreBC(name='FijPlaca_mov-Trig', createStepName='Initial', region=region, localCsys=None)
    # modelo.boundaryConditions['FijPlaca_mov-Trig'].deactivate('Impacto')

    # nsurf = 0
    # for sur in [Ch1_ext_u1, Ch1_ext_u2, Ch2_ext_u2, Ch2_ext_u1]:
    #   region = regionToolset.Region(faces=(sur.faces) )
    #   modelo.DisplacementBC(name='Sarjentos'+str(nsurf), createStepName='Initial',    u1=UNSET,   ur1=0.,
    #       region=region, distributionType=UNIFORM, amplitude=UNSET,                   u2=UNSET,   ur2=0.,
    #       fixed=OFF, fieldName='', localCsys=None,                                    u3=0.,      ur3=0.)
    #   modelo.boundaryConditions['Sarjentos'+str(nsurf)].deactivate('Impacto')
    #   nsurf = nsurf + 1


elif trigger == 'Def':
    dtrigger = 0.001

    modelo.ExplicitDynamicsStep(name='Trigger', previous='Initial',
        timePeriod=0.02)

    modelo.TabularAmplitude(name='Trig', timeSpan=STEP,
        smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.02, 1.0)))

    p = modelo.parts['Chapa']
    f = p.faces
    d = p.datums
    e = p.edges

    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=ltrigger)
    p.PartitionFaceByDatumPlane(datumPlane=d[7], faces=f[4:5]+f[6:10])

    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
    p.PartitionEdgeByDatumPlane(datumPlane=d[9], edges=e[33:34])

    region = regionToolset.Region(vertices=a.instances['Chapa-2'].vertices[22:23])
    modelo.DisplacementBC(name='Trigger_1', createStepName='Trigger',       u1=UNSET,           ur1=UNSET,
        region=region, distributionType=UNIFORM, amplitude='Trig',          u2=-dtrigger,       ur2=UNSET,
        fixed=OFF,  fieldName='', localCsys=None,                           u3=UNSET,           ur3=UNSET)

    region = regionToolset.Region(vertices=a.instances['Chapa-1'].vertices[22:23])
    modelo.DisplacementBC(name='Trigger_2', createStepName='Trigger',       u1=UNSET,           ur1=UNSET,
        region=region, distributionType=UNIFORM, amplitude='Trig',          u2=dtrigger,        ur2=UNSET,
        fixed=OFF, fieldName='', localCsys=None,                            u3=UNSET,           ur3=UNSET)

    e1 = a.instances['Chapa-1'].edges
    edges1 = e1[4:5]+e1[7:8]+e1[10:11]
    e2 = a.instances['Chapa-2'].edges
    edges2 = e2[4:5]+e2[7:8]+e2[10:11]
    region = regionToolset.Region(edges=edges1+edges2)
    modelo.EncastreBC(name='Trigger_SUJ', createStepName='Trigger',
        region=region, localCsys=None)

    modelo.boundaryConditions['Trigger_1'].deactivate('Impacto')
    modelo.boundaryConditions['Trigger_2'].deactivate('Impacto')
    modelo.boundaryConditions['Trigger_SUJ'].deactivate('Impacto')

    # La placa_mov se mantiene quieta durante el step del trigger
    region = regionToolset.Region(referencePoints=(a.referencePoints[RP_mov.id], ))
    modelo.EncastreBC(name='FijPlaca_mov-Trig', createStepName='Initial',
        region=region, localCsys=None)
    modelo.boundaryConditions['FijPlaca_mov-Trig'].deactivate('Impacto')


#==============================================================================
# Union
#==============================================================================

#------------------------------------------------------------------------------
# Soldadura
#------------------------------------------------------------------------------
if soldadura == True:
    y = ladov*coseno  # Coord y de las aletas
    z = pasopuntos / 2  # Valor inicial

    vpr = []

    gotcha = False  # Obtener coords ptos_sol desde sys.argv para optimizacion (en principio no se sabe - False)
    for arg in sys.argv:  # Buscar entre los argumentos...
        if arg is list:  # ...si alguno es una lista
            zs = arg  # El que sea, lleva las coordenadas
            gotcha = True
    if gotcha == False:  # Si no es posible (no es optim), utilizar equiespaciadas
        zs = []
        while z < longitud:
            zs.append(z)
            z = z + pasopuntos

    # Una aleta
    x = (ladoh+aleta)/2 + ladov*seno
    for z in zs:
        current_RP = a.ReferencePoint(point=(x, y, z))
        vpr.append(a.referencePoints[current_RP.id])

    # La otra aleta
    x = -(ladoh+aleta)/2 - ladov*seno
    for z in zs:
        current_RP = a.ReferencePoint(point=(x, y, z))
        vpr.append(a.referencePoints[current_RP.id])

    a.Set(referencePoints=vpr, name='Puntos_sol')

    modelo.ConnectorSection(name='punto', assembledType=BUSHING)
    elastic_0 = connectorBehavior.ConnectorElasticity(components=(1, 2, 3, 4, 5, 6),
        table=((210000000.0, 210000000.0, 210000000.0, 210000000.0, 210000000.0, 210000000.0), ))
    elastic_0.ConnectorOptions()
    #modelo.sections['punto'].setValues(behaviorOptions =(elastic_0,) )

    failure_1 = connectorBehavior.ConnectorFailure(components=(3, ),
        releaseComponent=ALL, minMotion=-0.01, maxMotion=0.00002)
    modelo.sections['punto'].setValues(behaviorOptions =(elastic_0, failure_1, ) )

    # region = a.sets['Puntos_sol']
    # s1 = a.instances['Chapa-1'].faces
    # side1Faces1 = s1[0:1]+s1[4:5]
    # s2 = a.instances['Chapa-2'].faces
    # side1Faces2 = s2[0:1]+s2[4:5]
    # tSurface1=regionToolset.Region(side1Faces=side1Faces1+side1Faces2)
    # targetSurface=(tSurface1, )
    # datum1 = modelo.rootAssembly.datums[1]
    #   modelo.rootAssembly.engineeringFeatures.PointFastener(
    #    name='punto_sol', region=region, targetSurfaces=targetSurface,
    #    sectionName='punto', connectorOrientationLocalCsys1=datum1,
    #    physicalRadius=0.04, unsorted=OFF)
    #datum1 = modelo.rootAssembly.datums[1]
    a.engineeringFeatures.PointFastener(targetSurfaces=MODEL,
        name='punto_sol', region=a.sets['Puntos_sol'], sectionName='punto',
        connectorOrientationLocalCsys1=None,
        physicalRadius=0.04, unsorted=OFF)
    ts = (a.surfaces['Ch2_u1'], a.surfaces['Ch2_u2'], a.surfaces['Ch1_u1'], a.surfaces['Ch1_u2'], )
    a.engineeringFeatures.fasteners['punto_sol'].setValues(targetSurfaces=ts, unsorted=OFF)
    #  Don't ask me why, but it only works this way...


#------------------------------------------------------------------------------
# Contacto general
#------------------------------------------------------------------------------
modelo.ContactExp(name='Global-Int', createStepName='Initial')

modelo.ContactProperty('Global-IntProp')

modelo.interactionProperties['Global-IntProp'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
modelo.interactionProperties['Global-IntProp'].TangentialBehavior(
    formulation=ROUGH,
    # formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
    # pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    # 0.05, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION,
    # fraction=0.005, elasticSlipStiffness=None,
    )

if adhesivo == True:
    # Contactos entre partes de la chapa
    if not halfm:
        # Chapa 1
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch1_ext3, Ch1_ext_u1),
            (Ch1_ext5, Ch1_ext_u2),
            (Ch1_int4, Ch1_int3),
            (Ch1_int4, Ch1_int5),
            ))

        # Chapa 2
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch2_ext2, Ch2_ext_u1),
            (Ch2_ext6, Ch2_ext_u2),
            (Ch2_int1, Ch2_int2),
            (Ch2_int1, Ch2_int6),
            ))

        # Entre chapas
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch2_int2, Ch1_int3),
            (Ch1_int5, Ch2_int6),
            (Ch2_u1, Ch1_u1),
            (Ch1_u2, Ch2_u2),
            ))

        surf_chapa_int = [Ch2_int1, Ch2_int2, Ch1_int3, Ch1_int4, Ch1_int5, Ch2_int6]

    else:
        # Chapa 1
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch1_ext3, Ch1_ext_u1),
            (Ch1_int4, Ch1_int3),
            ))

        # Chapa 2
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch2_ext2, Ch2_ext_u1),
            (Ch2_int1, Ch2_int2),
            ))

        # Entre chapas
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (Ch2_int2, Ch1_int3),
            (Ch2_u1, Ch1_u1),
            ))

        surf_chapa_int = [Ch2_int1, Ch2_int2, Ch1_int3, Ch1_int4]

    surf_chapa_all = Ch1_all + Ch2_all

    for surf_chapa in surf_chapa_all:
        modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
            (surf_chapa, SELF),         # Cada una consigo misma
            (Placa_mov, surf_chapa),    # Con la placa de impacto
            (Placa_fix, surf_chapa),    # Con la placa fija
            ))

    for sc1 in surf_chapa_int:
        for sc2 in surf_chapa_int:
            if sc1 == sc2:
                pass
            else:
                modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', addPairs=(
                    (sc1, sc2), ))

    # Foam
    if opc['Relleno'] == 'FULL' or opc['Relleno'] == 'FOAMHEX' or opc['Relleno'] == 'FOAM6':
        surf_foam_ext = [surf_foam_1, surf_foam_2, surf_foam_3, surf_foam_4, surf_foam_5, surf_foam_6]

        # Foam con chapa
        for chapa, foam in zip(surf_chapa_int, surf_foam_ext):
            modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', addPairs=(
                (chapa, foam), ))

        # Partido en bloques
        if opc['Relleno'] == 'FULL' or opc['Relleno'] == 'FOAM6':
            surf_foam_a = [surf_foam_1a, surf_foam_2a, surf_foam_3a, surf_foam_4a, surf_foam_5a, surf_foam_6a]
            surf_foam_b = [surf_foam_1b, surf_foam_2b, surf_foam_3b, surf_foam_4b, surf_foam_5b, surf_foam_6b]
            surf_foam_F = [surf_foam_1F, surf_foam_2F, surf_foam_3F, surf_foam_4F, surf_foam_5F, surf_foam_6F]
            surf_foam_R = [surf_foam_1R, surf_foam_2R, surf_foam_3R, surf_foam_4R, surf_foam_5R, surf_foam_6R]

            # Entre partes del foam
            for surf_a, surf_b in zip(surf_foam_a, surf_foam_b[1:]+surf_foam_b[:1]):
                modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
                    (surf_a, surf_b), ))

            # Con las placas de impacto (si esta en partes)
            for surf_F, surf_R in zip(surf_foam_F, surf_foam_R):
                modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
                    (Placa_fix, surf_F),
                    (Placa_mov, surf_R),
                    ))

        # Bloque unico
        else:
            # Con las placas de impacto (si es un bloque unico)
            modelo.interactions['Global-Int'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=(
                (Placa_fix, surf_foam_F),
                (Placa_mov, surf_foam_R),
                ))

    if not halfm:
        modelo.Tie(name='T1-1', slave=Ads1_bot, master=Ch1_u1, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        modelo.Tie(name='T1-2', slave=Ads1_top, master=Ch2_u1, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        modelo.Tie(name='T2-1', slave=Ads2_bot, master=Ch1_u2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        modelo.Tie(name='T2-2', slave=Ads2_top, master=Ch2_u2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

    else:
        modelo.Tie(name='T1-1', slave=Ads1_bot, master=Ch1_u1, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        modelo.Tie(name='T1-2', slave=Ads1_top, master=Ch2_u1, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)


else:
    modelo.ContactProperty('Global-IntProp')
    modelo.ContactExp(name='Global-Int', createStepName='Initial')
    modelo.interactions['Global-Int'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    modelo.interactions['Global-Int'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'Global-IntProp'), ))



#==============================================================================
# Finalizacion
#==============================================================================

# Generacion de la malla
for key in modelo.parts.keys():
    p = modelo.parts[key]
    p.generateMesh()

# Calculo de la masa total
mass = modelo.rootAssembly.getMassProperties()['mass']*1000. # Mass of model in kg
print 'Masa total: ' + str(mass) + ' kg'
if 'BREOGAN' in sys.argv:
    ResultadoMasa = open('resultado.mass','w')
    ResultadoMasa.write('%-E' % float(mass))
    ResultadoMasa.close()

# Datos impacto
# print 'Datos del impacto:'
# acortamiento = delta/longitud
# print 'Se reducira la longitud un ' + str(acortamiento).format(%)


# Visualizacion
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
    predefinedFields=ON, connectors=ON, optimizationTasks=OFF,
    geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Impacto')


#==============================================================================
# Job
#==============================================================================

# Correr en local
if opc['Host'] == 'LOCAL':  # con parametros locales
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
        parallelizationMethodExplicit=DOMAIN, numDomains=1,
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
if (opc['Host'] == 'BREOGAN') and 'BREOGAN' not in sys.argv:  # con parametros de breogan
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
        parallelizationMethodExplicit=DOMAIN, numDomains=1,
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)

# Correr en Breogan
if 'BREOGAN' in sys.argv:
    trabajo = mdb.Job(name=opc['Codigo'], model='Model-1', description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
        parallelizationMethodExplicit=DOMAIN, numDomains=4,
        #parallelizationMethodExplicit=LOOP, numDomains=1,
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
    trabajo.setValues(userSubroutine='/home/lpire/k/v_ALUM.f')
    trabajo.writeInput(consistencyChecking=OFF)

