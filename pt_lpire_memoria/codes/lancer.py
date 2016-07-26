# Lancer.py

#cpu = 16
#mem = 12000

import sys
import os, re
from subprocess import call
from subprocess import Popen

def direr(codigo, tipolancer='C'):
	#	La estructura de carpetas es creaca mediante una funcion propia para
	# garantizarla existencia de directorios padre al anadir niveles
	dirname = '/home/lpire/model/'+codigo
	dkt_dirname = dirname+'/dakota'
	try:
		os.mkdir(dirname)
		os.chdir(dirname)
	except:
		pass
	if tipolancer == 'D':
		try:
			os.mkdir(dkt_dirname)
			os.chdir(dkt_dirname)
		except:
			pass

def wlancer(seccion, union, relleno, codigo, espads=0., nptos=0, tipolancer='C', cpu=16, mem=12000):
	# dirname = '/home/lpire/model/'+codigo
	fname = 'lancer' + codigo + '.sh'
	if tipolancer == 'D':
		# dirname = dirname + '/dakota'
		fname = 'lancer_abaqus_dkt.sh'

	#os.chdir(dirname)
	f = open(fname, 'w')

	f.write('#!/bin/bash\n')
	f.write('\n')
	f.write('# ------ Configuracion del sistema de colas ------\n')
	f.write('#$ -S /bin/bash\n')
	f.write('#$ -A Abaqus\n')
	f.write('#$ -P Abaqus\n')
	f.write('#$ -N ' + codigo + '\n')
	f.write('#$ -l vf=11000M\n')
	f.write('#$ -v CONFIG_FILE=abaqus_v6.env,PROYECTO=Abaqus,ABAQUSVERSION=abq6132,MEM=' + str(mem) + '\n')
	f.write('#$ -j y\n')
	f.write('#$ -m n\n')
	f.write('#$ -cwd\n')
	f.write('#$ -o $JOB_NAME.o$JOB_ID\n')
	f.write('#$ -notify\n')
	f.write('#$ -q normal.q\n')
	f.write('#$ -pe abaqus_pe ' + str(cpu) + '\n')
	f.write('\n')

	f.write('# ------------ Configuracion del entorno\n')
	f.write('\n')
	f.write('source /share/apps/environment.sh\n')
	f.write('module use /opt/modulefiles\n')
	f.write('module load abaqus/6.13.2\n')
	f.write('module load compilers/gcc/4.7.2_Cgcc_4.4.7\n')
	f.write('\n')
	f.write('\n')
	f.write('echo "cpus=$NSLOTS" >> $CONFIG_FILE\n')
	#f.write('echo "parallel=DOMAIN" >> $CONFIG_FILE\n')
	f.write('echo "parallel=LOOP" >> $CONFIG_FILE\n')
	f.write('echo "double_precision=BOTH" >> $CONFIG_FILE\n')
	f.write('\n')

	f.write('# ------------ Ejecucion del trabajo\n')
	if tipolancer != 'P' and tipolancer == 'C':
		f.write('abaqus cae noGUI=/home/lpire/pt_lpire_memoria/codes/mymodel.py -- BREOGAN ' + codigo + ' ' + seccion + ' ' + union + ' ' + str(espads) + ' ' + str(nptos) + ' ' + relleno + '\n')
		f.write('tiempo "abaqus analysis interactive input=' + codigo + '.inp job=' + codigo + '-$JOB_ID user=/home/lpire/pt_lpire_memoria/codes/v_ALUM" $JOB_NAME.t$JOB_ID\n')
	elif tipolancer != 'P' and tipolancer == 'D':
		f.write('abaqus cae noGUI=model_dakota.py -- BREOGAN ' + codigo + ' ' + seccion + ' ' + union + ' ' + str(espads) + ' ' + str(nptos) + ' ' + relleno + '\n')
		f.write('tiempo "abaqus analysis interactive input=' + codigo + '.inp job=' + codigo + '-$JOB_ID user=/home/lpire/pt_lpire_memoria/codes/v_ALUM" $JOB_NAME.t$JOB_ID\n')
	f.write('abaqus cae noGUI=/home/lpire/pt_lpire_memoria/codes/HC_post.py -- ' + codigo + '-$JOB_ID\n')
	f.write('\n')
	f.write('# module load anaconda/2.0.1\n')
	f.write('\n')
	f.write('# python postprocess.py\n')
	f.write('\n')
	f.write('# popd\n')
	f.write('# mv $TMPDIR/*.mass .\n')
	f.write('# mv $TMPDIR/*.sea .\n')
	f.write('# mv $TMPDIR/*.dat .\n')
	f.write('# mv $TMPDIR/*.energy .\n')
	f.write('# mv $TMPDIR/*.lr .\n')
	f.write('# mv $TMPDIR/*.peak .\n')
	f.write('# mv $TMPDIR/*.t$JOB_ID .\n')

	f.close()

	if tipolancer != 'D':
		qsub = Popen(["qsub" , fname])
		qsub.wait()

def dakota(seccion, union, relleno, codigo, espads=0, nptos=0, cpu=1):
	import shutil

	#dkt_dir_name = '/home/lpire/model/'+codigo+'/dakota'
	dkt_in = '/home/lpire/pt_lpire_memoria/codes/do.in'
	fname = 'dkt-' + codigo + '.sh'

	shutil.copy(dkt_in, 'do.in')
	shutil.copy('/home/lpire/pt_lpire_memoria/codes/paramodel.py', 'paramodel.py')
	
	#  Lanzador para Breogan ==============================
	f = open(fname, 'w')

	f.write('#!/bin/bash\n')
	f.write('#$ -S /bin/bash\n')
	f.write('#$ -A General\n')
	f.write('#$ -P General\n')
	f.write('#$ -N Dkt'+codigo+'\n')
	f.write('#$ -l vf=2000M\n')
	f.write('#$ -v CONFIG_FILE=,PROYECTO=General,OMPIRUN=/opt/openmpi/bin/mpirun\n')
	f.write('#$ -j y\n')
	f.write('#$ -m n\n')
	f.write('#$ -cwd\n')
	f.write('#$ -o $JOB_NAME.o$JOB_ID\n')
	f.write('#$ -q normal.q\n')
	f.write('#$ -pe orte '+str(cpu)+'\n')

	f.write('module use /opt/modulefiles\n')
	#f.write('module load dakota/5.4.0_Cgcc_4.7.2_Mopenmpi_1.6.4_Lacml_5.3.0\n')
	f.write('module load dakota/6.2.0_Cgcc_4.7.2_Mopenmpi_1.6.4_Lacml_5.3.0\n')

	#f.write('tic=\$(date +%s)\n')
	f.write('if [ "\$NSLOTS" -gt "1" ]; then \n')
	f.write('  \$OMPIRUN -np \$NSLOTS --mca btl_if_exclude eth0 dakota -i do.in\n')
	f.write('else\n')
	f.write('  dakota -i do.in\n')
	#f.write('  tiempo \"$DAKOTA_PATH -i $DAKOTA_INPUT\" \$JOB_NAME.t\$JOB_ID')
	f.write('fi\n')
	#f.write('toc=\$(date +%s)\n')
	#f.write('let time=toc-tic\n')
	#f.write('echo \$time > $JOB_NAME.t$JOB_ID\n')

	f.close()

	#  Driver del analisis ================================
	d = open('driver.sh', 'w')

	d.write('PARAMETERS_FILE=$1\n')

	d.write('QSUB_COMMAND="/opt/gridengine/bin/linux-x64/qsub"\n')
	d.write('PARAMETERIZED_MODEL_FILE="paramodel.py"\n')
	#d.write('DEFAULT_VALUES_FILE="default.dat"\n')
	d.write('MODEL_FILE="model_dakota.py"\n')
	d.write('MODEL_FILE_INP=""\n')
	#d.write('MODEL_NAME="'+codigo+'"\n')
	d.write('QUEUE_LAUNCHER="lancer_abaqus_dkt.sh"\n')

	d.write('echo -en  "\\\n')
	d.write('True\n')
	d.write('" > checkRun.status\n') # Archivo para comprobar que el trabajo sigue corriendo

	d.write('# Sustitucion de las variables generadas por DAKOTA en el modelo parametrizado\n')
	#d.write('dprepro $PARAMETERS_FILE $PARAMETERIZED_MODEL_FILE ${MODEL_FILE}.tmp\n')
	#d.write('dprepro $DEFAULT_VALUES_FILE ${MODEL_FILE}.tmp $MODEL_FILE\n')
	d.write('dprepro $PARAMETERS_FILE $PARAMETERIZED_MODEL_FILE $MODEL_FILE\n')
	#d.write('MODELNAME=$(awk \'/ModelName /{print $4}\' $DEFAULT_VALUES_FILE)\n')
	#d.write('sed -i "s/{ModelName}/$MODELNAME/g" $MODEL_FILE\n')
	#d.write('rm -f ${MODEL_FILE}.tmp\n')

	d.write('# Ejecucion del analisis\n')
	d.write('touch checkRun.status\n')
	d.write('$QSUB_COMMAND $QUEUE_LAUNCHER\n')
	d.write('while [ -f checkRun.status ]; do sleep 1; done\n') # Comprobar cada segundo que existe el checkRun.status
	d.close()

	permisos = Popen(["chmod", "a+x", "driver.sh"])
	permisos.wait()

	qsub = Popen(["qsub" , fname])
	qsub.wait()
	
def gen_seccion(seccion, tl):
	posib = ['HEX', 'SQR']
	if seccion == '_':
		if tl == 'D':
			sys.exit("ERROR: multioptimizacion (Dakota) polimorfa")
		seccion = posib
	else:
		if seccion not in posib:
			sys.exit("ERROR: seccion no reconocida")
		piv = seccion
		seccion = []
		seccion.append(piv)
	return seccion

def gen_union(union, tl):
	posib = ['ADS','HYBRID','SW']
	if union == '_':
		if tl == 'D':
			sys.exit("ERROR: multioptimizacion (Dakota) polimorfa")
		union = posib
	else:
		if union not in posib:
			sys.exit("ERROR: tipo de union no reconocido")
		piv = union
		union = []
		union.append(piv)
	return union

def gen_espads(espads, union, tl):
	posib = [0.0001, 0.0003, 0.0005, 0.001, 0.0025]
	if 'ADS' in union or 'HYBRID' in union:
		if espads == '_':
			if tl == 'D':
				sys.exit("ERROR: multioptimizacion (Dakota) polimorfa")
			espads = posib
		else:
			piv = float(espads)
			if piv <= 0.:
				sys.exit("ERROR: espesor de adhesivo no valido")
			espads = []
			espads.append(piv)
	else:
		espads = [0.0]
	return espads

def gen_nptos(nptos, union, tl):
	posib = [4, 6, 8, 10, 12]
	if 'SW' in union or 'HYBRID' in union:
		if nptos == '_':
			if tl == 'D':
				sys.exit("ERROR: multioptimizacion (Dakota) polimorfa")
			nptos = posib
		else:
			piv = int(nptos)
			if piv <= 0:
				sys.exit("ERROR: numero de puntos de soldadura igual a 0")
			nptos = []
			nptos.append(piv)
	else:
		nptos = [0]
	return nptos

def gen_relleno(relleno, tl):
	posib = ['FULL','FOAM','FOAM6','GFRP','NONE']
	if relleno == '_':
		if tl == 'D':
			sys.exit("ERROR: multioptimizacion (Dakota) polimorfa")
		relleno = posib
	else:
		if relleno not in posib:
			sys.exit("ERROR: relleno no reconocido")
		piv = relleno
		relleno = []
		relleno.append(piv)		
	return relleno

def codid(seccion, union, relleno, espads=0.0, nptos=0):
	if seccion == 'HEX':
		sec_code = '-Hx'
	elif seccion == 'SQR':
		sec_code = '-Sq'
	un_code = union[0:2]				# Dos primeras letras del tipo de union
	np_code = str(nptos)				# Numero de ptos de soldadura
	ea_code = '-' + str(espads)[-2:]	# Dos ultimas cifras espesor adhesivo (decimas de mm)
	rll_code = relleno 					# Tipo relleno
	if relleno == 'FOAM':
		rll_code = 'FF'
	elif relleno == 'FOAM6':
		rll_code = 'F6'

	cod = un_code
	if union == 'HYBRID' or union == 'SW':
		cod = cod + np_code
	if union == 'ADS' or union == 'HYBRID':
		cod = cod + ea_code
	cod = cod + sec_code + rll_code
	return cod

desfase_input = 0
if sys.argv[1] == 'P':					# Solo se requiere post-proceso
	desfase_input = 1
	tl = 'P'
elif sys.argv[1] == 'D':
	desfase_input = 1
	tl = 'D'
else:
	tl = 'C'

seccion = sys.argv[1+desfase_input]		# Seccion: Hexagonal, Cuadrada
seccion = gen_seccion(seccion, tl)

union = sys.argv[2+desfase_input]		# Union: Adhesiva, Hibrida, Soldadura
union = gen_union(union, tl)

espads = sys.argv[3+desfase_input]		# Espesor adhesivo: 0.1, 0.3, 0.5, 1.0, 2.5 [mm]
espads = gen_espads(espads, union, tl)

nptos = sys.argv[-2]					# Numero de puntos de soldadura
nptos = gen_nptos(nptos, union, tl)

relleno = sys.argv[-1]					# Relleno del tubo: Lleno, Espuma, Prismas de espuma, GFRP, Vacio
relleno = gen_relleno(relleno, tl)

try:
	os.chdir('/home/lpire/pt_lpire_memoria/codes')
	gitpull = Popen(['git' , 'pull'])
	gitpull.wait()
except:
	print "WARN: unable to update Git repository"
else:
	print "INFO: updated Git repository"

# Operacion de combinaciones
if tl != 'D':
	for sec in seccion:
		for rll in relleno:
			if sec == 'SQR' and (rll == 'FULL' or rll == 'GFRP'):
				continue 		# Se omiten los rellenos con GFRP para la seccion cuadrada (no implementada)
			for un in union:
				if un == 'ADS' or un == 'HYBRID':
					for ea in espads:
						if un == 'HYBRID':
							for np in nptos:
								cod = codid(seccion=sec, union=un, espads=ea, nptos=np, relleno=rll)
								direr(codigo=cod, tipolancer=tl)
								wlancer(seccion=sec, union=un, espads=ea, nptos=np, relleno=rll, codigo=cod, tipolancer=tl)
						elif un == 'ADS':
							cod = codid(seccion=sec, union=un, espads=ea, relleno=rll)
							direr(codigo=cod, tipolancer=tl)
							wlancer(seccion=sec, union=un, espads=ea, relleno=rll, codigo=cod, tipolancer=tl)
				elif un == 'SW':
					for np in nptos:
						cod = codid(seccion=sec, union=un, nptos=np, relleno=rll)
						direr(codigo=cod, tipolancer=tl)
						wlancer(seccion=sec, union=un, nptos=np, relleno=rll, codigo=cod, tipolancer=tl)
else:
	seccion = seccion[0] ; union = union[0] ; espads = espads[0] ; nptos = nptos[0] ; relleno = relleno[0]
	cod = codid(seccion=seccion, union=union, espads=espads, nptos=nptos, relleno=relleno)
	direr(codigo=cod, tipolancer=tl)
	wlancer(seccion=seccion, union=union, espads=espads, nptos=nptos, relleno=relleno, codigo=cod, tipolancer=tl)
	dakota(seccion=seccion, union=union, espads=espads, nptos=nptos, relleno=relleno, codigo=cod, cpu=1)
