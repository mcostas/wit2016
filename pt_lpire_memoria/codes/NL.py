import os, shutil
import argparse
# from termcolor import colored  ### Python 3
from subprocess import Popen, PIPE
from time import sleep

#  Inicialization =============================================================
parser = argparse.ArgumentParser(prog='NL.py',
	description='Lancer: General launcher for Breogan queue system. Includes some optimization and sampling capabilities.',
	prefix_chars='-', # for optional values
	)

# Arguments -------------------------------------------------------------------
parser.add_argument('-cpu', type=int, default=16, nargs=1, required=False, action='store')
parser.add_argument('geom', 	choices=['SQR', 'HEX', '_'], 								default='SQR', 	nargs='?')
parser.add_argument('union',	choices=['ADS', 'SW', 'HYBRID', '_'], 						default='ADS', 	nargs='?')
parser.add_argument('fill', 	choices=['FULL', 'FOAM', 'FOAM6', 'GFRP', 'NONE', '_'], 	default='NONE', nargs='?')
# parser.add_argument('-v', help='Changes lancer verbosity.')

excl_parser1 = parser.add_mutually_exclusive_group(required=False)
excl_parser1.add_argument('-DO', action='store_true',
	help='Runs the analysis for design optimization. Check variables in parametrized model and analysis drivers.')
excl_parser1.add_argument('-SAMP', action='store_true',
	help='Runs model sampling.')
excl_parser1.add_argument('-reSAMP', action='store_true',
	help='Re-runs model sampling only at points with errors.')
excl_parser1.add_argument('-SOGA', action='store_true',
	help='Runs model sampling and surrogate model based optimization.')

args = parser.parse_args()

# General parameters ----------------------------------------------------------
try:
	cpu = args.cpu[0]
except:
	cpu = args.cpu
mem = 12000

# Colors for logging ----------------------------------------------------------
class tag:
	info = '\033[94m' + 'INFO' + '\033[0m' + ': '
	warn = '\033[93m' + 'WARN' + '\033[0m' + ': '
	error= '\033[91m' + 'ERROR'+ '\033[0m' + ': '
	head = '\033[95m'
	endhead = '\033[0m'
	GREEN = '\033[92m'

# Defining n_split function
def n_split(iterable, n, fillvalue=None):
	num_extra = len(iterable) % n
	zipped = zip(*[iter(iterable)] * n)
	return zipped if not num_extra else zipped + [iterable[-num_extra:], ]

# Treatments ------------------------------------------------------------------
# Geometry treatment
geom = args.geom
if geom == '_':
	geom = ['SQR', 'HEX']
else:
	geom = [geom]

# Union treatment
union = args.union
if union == '_':
	union = ['ADS', 'SW', 'HYBRID']
else:
	union = [union]
# Adhesive union
if ('ADS' in union) or ('HYBRID' in union):
	try:
		espads = float(raw_input('Especify adhesive thickness (leave blank for default): '))
	except ValueError:
		print tag.info+'Using default adhesive thickness: 0.0003 mm'
		espads = 0.0003
	if espads <= 0.:
		raise InvalidAdsThick('Adhesive thickness equal or lower than 0.')
	espads = [espads]
else:
	espads = [0.]
# SW union
if ('SW' in union) or ('HYBRID' in union):
	try:
		nptos = int(raw_input('Especify number of SW points: '))
	except ValueError:
		print tag.info+'Using default number of SW points: 6'
		nptos = 6
	if nptos <= 0:
		raise InvalidSWNumber('Number of SW points equal or lower than 0.')
	nptos = [nptos]
else:
	nptos = [0]

# Fill treatment
fill = args.fill
if fill == '_':
	fill = ['FULL', 'FOAMHEX', 'FOAM6', 'GFRP', 'NONE']
else:
	fill = [fill]

# v = args.v
DO 		= args.DO
SAMP 	= args.SAMP
reSAMP 	= args.reSAMP
if reSAMP:
	SAMP = True
SOGA 	= args.SOGA
if SOGA:
	SAMP = True

# Codes directory check -------------------------------------------------------
def pre(direc='/home/lpire'):
	if os.path.isdir(direc+'/pt_lpire_memoria/codes') and os.path.isdir(direc+'/model'):  # Checks if the codes folder exists
		pass
	else:
		direc = raw_input('Especify new codes and model directory from "/" (terminate if blank):')
		if direc == '':
			raise NoCodeDir('Unespecified model and codes directory')
		try:
			os.mkdir(direc+'/pt_lpire_memoria/codes')
			os.mkdir(direc+'/pt_lpire_memoria/codes')
		except:
			pass
	return direc

home = pre()

# Git -------------------------------------------------------------------------
try:
	os.chdir(home+'/pt_lpire_memoria/codes')
	gitpull = Popen(['git' , 'pull'])
	gitpull.wait()
except:
	print tag.warn+"unable to update Git repository"
else:
	print tag.info+"updated Git repository"

# Jobs ========================================================================

# Coder -----------------------------------------------------------------------
def coder(g, u, r, e, n):
	if g == 'HEX':
		gc = '-Hx'
	elif g == 'SQR':
		gc = '-Sq'
	uc = u[0:2]				# Dos primeras letras del tipo de union
	nc = str(n)				# Numero de ptos de soldadura
	ec = '-' + str(e)[-2:]	# Dos ultimas cifras espesor adhesivo (decimas de mm)
	rc = r 					# Tipo relleno
	if r == 'FOAM':
		rc = 'FF'
	elif r == 'FOAM6':
		rc = 'F6'

	code = uc
	if u == 'HYBRID' or u == 'SW':
		code = code + nc
	if u == 'ADS' or u == 'HYBRID':
		code = code + ec
	code = code + gc + rc

	return code

# Abaqus ----------------------------------------------------------------------
def qa(g, u, r, e, n, cpu=cpu, mem=12000, DO=False, SAMP=False, reSAMP=False, SOGA=False, code=None):
	import shutil
	if (SAMP or reSAMP or SOGA):  # Reduce CPU load
		cpu = 4
	if not (DO or SAMP or reSAMP or SOGA):  # Take already parametrized file
		shutil.copy(home+'/pt_lpire_memoria/codes/paramodel.py', 'paramodel.py.tmp')
	shutil.copy(home+'/pt_lpire_memoria/codes/commons.dat', 'commons.dat')

	aname = 'l-abaqus.sh'
	a = open(aname, 'w')

	a.write('#!/bin/bash\n')
	a.write('\n')
	a.write('# ------ Configuracion del sistema de colas ------\n')
	a.write('#$ -S /bin/bash\n')
	a.write('#$ -A Abaqus\n')
	a.write('#$ -P Abaqus\n')
	a.write('#$ -N ' + code + '\n')
	a.write('#$ -l vf='+str(mem)+'\n')
	a.write('#$ -v CONFIG_FILE=abaqus_v6.env,PROYECTO=Abaqus,ABAQUSVERSION=abq6132,MEM=' + str(mem) + '\n')
	a.write('#$ -j y\n')
	a.write('#$ -m n\n')
	a.write('#$ -cwd\n')
	a.write('#$ -o $JOB_NAME.o$JOB_ID\n')
	a.write('#$ -notify\n')
	#a.write('#$ -q normal.q@compute-1-40\n') # 37, 38, 39 o 40 (nodos intel)
	a.write('#$ -q normal.q\n')
	a.write('#$ -pe abaqus_pe ' + str(cpu) + '\n')
	a.write('\n')

	a.write('# ------------ Configuracion del entorno\n')
	a.write('\n')
	a.write('source /share/apps/environment.sh\n')
	a.write('module use /opt/modulefiles\n')
	a.write('module load abaqus/6.13.2\n')
	a.write('module load compilers/gcc/4.7.2_Cgcc_4.4.7\n')
	a.write('module load dakota/6.2.0_Cgcc_4.7.2_Mopenmpi_1.6.4_Lacml_5.3.0\n')
	a.write('\n')
	a.write('\n')
	a.write('echo "cpus=$NSLOTS" >> $CONFIG_FILE\n')
	#a.write('echo "parallel=DOMAIN" >> $CONFIG_FILE\n')
	a.write('echo "parallel=LOOP" >> $CONFIG_FILE\n')
	a.write('echo "double_precision=BOTH" >> $CONFIG_FILE\n')
	a.write('\n')

	# if not (DO or SOGA):  # Reporter in optimization differently implemented
		# a.write('echo "$JOB_ID\\t$(TZ=CET date)\\t'+code'" >> '+home+'/model/report.er')

	a.write('# ------------ Ejecucion del trabajo\n')
	a.write('dprepro commons.dat paramodel.py.tmp rmf.py\n')
	a.write('abaqus cae noGUI=rmf.py -- BREOGAN '+code+' '+g+' '+u+' '+str(e)+' '+str(n)+' '+r+'\n')
	a.write('tiempo "abaqus analysis interactive input='+code+'.inp job='+code+'-$JOB_ID user='+home+'/pt_lpire_memoria/codes/v_ALUM" $JOB_NAME.t$JOB_ID\n')
	a.write('abaqus cae noGUI='+home+'/pt_lpire_memoria/codes/HC_post.py -- ' + code + '-$JOB_ID\n')

	a.close()

	if not (DO or SAMP or reSAMP or SOGA):
		qsub = Popen(["qsub" , aname])
		qsub.wait()

# Dakota ----------------------------------------------------------------------
def qd(g, u, r, e, n, DO, SAMP, reSAMP, SOGA):
	cpu = 1
	# Choose files
	if DO:
		shutil.copy(home+'/pt_lpire_memoria/codes/do.in', 'do.in')
		d_in = 'do.in'
	if SAMP and not reSAMP:
		shutil.copy(home+'/pt_lpire_memoria/codes/sampling.in', 'sampling.in')
		d_in = 'sampling.in'
	if reSAMP:
		avp_rp()
		d_in = 're_sampling.in'
	if SOGA:
		shutil.copy(home+'/pt_lpire_memoria/codes/soga.in', 'soga.in')
		d_in = 'soga.in'
	shutil.copy(home+'/pt_lpire_memoria/codes/paramodel.py', 'paramodel.py')
	shutil.copy(home+'/pt_lpire_memoria/codes/driver.py', 'driver.py')

	# Dakota launcher ---------------------------------------------------------
	dname = 'l-dakota.sh'
	dkt = open(dname, 'w')

	dkt.write('#!/bin/bash\n')
	dkt.write('#$ -S /bin/bash\n')
	dkt.write('#$ -A General\n')
	dkt.write('#$ -P General\n')
	dkt.write('#$ -N dkt\n')  # Try to make it sample number
	dkt.write('#$ -l vf=2000M\n')
	dkt.write('#$ -v CONFIG_FILE=,PROYECTO=General,OMPIRUN=/opt/openmpi/bin/mpirun\n')
	dkt.write('#$ -j y\n')
	dkt.write('#$ -m n\n')
	dkt.write('#$ -cwd\n')
	dkt.write('#$ -o $JOB_NAME.o$JOB_ID\n')
	dkt.write('#$ -q normal.q\n')
	dkt.write('#$ -pe orte '+str(cpu)+'\n')

	dkt.write('module use /opt/modulefiles\n')
	dkt.write('module load dakota/6.2.0_Cgcc_4.7.2_Mopenmpi_1.6.4_Lacml_5.3.0\n')

	dkt.write('if [ "\$NSLOTS" -gt "1" ]; then \n')
	dkt.write('  \$OMPIRUN -np \$NSLOTS --mca btl_if_exclude eth0 dakota -i '+d_in+'\n')
	dkt.write('else\n')
	dkt.write('  dakota -i '+d_in+'\n')
	dkt.write('fi\n')

	dkt.close()

	# Launch ------------------------------------------------------------------
	permisos = Popen(["chmod", "a+x", "driver.py"])
	permisos.wait()

	qsub = Popen(["qsub" , dname])
	qsub.wait()

# Sampling - Ask for points
def smp_a4p(u, n):  # This feature isn't writen into the sampling.in file yet (IMPLEMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!)
	vbles = ['GIc', 'GIIc', 'G_int']  # Should include help to define this things
	print tag.head+'Asking for sampling points'+tag.endhead
	print tag.info+'Available variables: '+(' '.join(vbles))
	sv = []  # Sampling variables
	while True:
		v = raw_input('Insert sampling variable (leave blank to break): ')
		if v:
			lb = raw_input('Set lower bound: ')
			ub = raw_input('Set upper bound: ')
			iv = raw_input('Set initial value (leave blank for mid-point): ')
			lb = float(lb); ub = float(ub)
			if not iv:
				iv = (lb+ub)/2
			else:
				iv = float(iv)
			v = {'Name': v, 'Lower': lb, 'Upper': ub, 'Initial': iv}
			sv = sv + v
			del lb, ub, iv, v
		else:
			break

# Parameter Variation Analysis - Read Points
def avp_rp():
	try:
		os.remove('re_sampling.in')
	except:
		pass

	nsuccess = 0
	ntotal = 0

	points_failure = []
	points_success = []

	print tag.info+"searching for unfinished jobs for new sampling"

	cd = os.getcwd()
	for subdir, dirs, files in os.walk(cd):
		for f in files:  # Every file in each subdir
			success = False
			found = f.find('.o')
			if (found != (-1)) and (f[-3:] != "odb") and ("driver.out" not in f):  # Found .oNNN file
				with open(os.path.join(subdir,f), "r") as o:
					for line in o:
						if "THE ANALYSIS HAS COMPLETED SUCCESSFULLY" in line:
							success = True
							nsuccess = nsuccess + 1
							break
						else:
							continue
				ntotal = ntotal + 1
				break
		values = []
		for f in files:
			found = f.find('.in.')  # Search the input values file
			if found != (-1):
				with open(os.path.join(subdir,f), "r") as i:
					for line in i:
						things = line.split()
						values.append(float(things[3]))  # Append all numbers (view 'points_success' later)
		if success:
			points_success.extend(values[1:4])
			for f in files:
				found = f.find('.sea')  # Search the .sea file
				if found != (-1):
					with open(os.path.join(subdir,f), "r") as f_sea:
						sea = float(f_sea.read())
			for f in files:
				found = f.find('.peak')  # Search the .peak file
				if found != (-1):
					with open(os.path.join(subdir,f), "r") as f_peak:
						peak = float(f_peak.read())
			points_success.append(sea)  # Get only interesting numbers
			points_success.append(peak)
		elif not success:
			points_failure.extend(values[1:4])  # GIc, GIIc, G_int

	# Writing success results to a file
	with open("succe.ss", "a") as ss:
		for ps in n_split(points_success, 5):
			ss.write(' '.join(str(p) for p in ps) +"\n")

	print tag.info+"found "+str(ntotal)+" jobs; "+("{0:.1f}%".format(100*float(nsuccess)/ntotal))+" success rate"

	# Ask to delete old jobs
	while True:
		doj = raw_input(tag.warn+"Delete old jobs? (Y/N) ")
		if doj == "Y" or doj == "y":
			ld = [("sample."+str(x)) for x in range(1,501)]
			print tag.warn+"Deleting old jobs"
			for d in ld:
				try:
					shutil.rmtree(d)
				except:
					pass
			break
		if doj == "N" or doj == "n":
			print tag.info+"No previous jobs were deleted"
			break

	#for ps in n_split(points_success, 5):
		#print ' '.join(str(p) for p in ps)

	with open('re_sampling.in', 'w') as rs:
		rs.write("environment,\n")
		rs.write("  # single_method\n")
		rs.write("  tabular_data\n")
		rs.write("	tabular_data_file = 'sampling_xy.dat'\n")
		rs.write("  output_precision = 10 # Default = 10 ; Max = 16\n")

		rs.write("method,\n")
		rs.write("  id_method = 'reSAMP_METHOD'\n")
		rs.write("  model_pointer = 'SURR_MODEL'\n")

		rs.write("list_parameter_study\n")

		rs.write("list_of_points=\n")
		for point in n_split(points_failure, 3):
			rs.write(str(point[0])+' '+str(point[1])+' '+str(point[2])+'\n')

		rs.write("model,\n")
		rs.write("  id_model = 'SURR_MODEL'\n")
		rs.write("  single\n")
		rs.write("	variables_pointer = 'SAMP_VARIABLES'\n")
		rs.write("	interface_pointer = 'SAMP_INTERFACE'\n")
		rs.write("	responses_pointer = 'SAMPLING_RESPONSES'\n")

		rs.write("variables,\n")

		rs.write("  id_variables = 'SAMP_VARIABLES'\n")
		rs.write("	  active all # 5.3.1 \n")
	
		rs.write("  continuous_design = 3\n")

		rs.write("  descriptors   'GIc' 'GIIc' 'G_int'\n")
		rs.write("	lower_bounds   1.0   1.0	1.0\n")
		rs.write("	initial_point  3.0   3.0	3.0\n")
		rs.write("	upper_bounds   7.0   7.0	7.0\n")


		rs.write("responses,\n")
		rs.write("  id_responses = 'SAMPLING_RESPONSES'\n")
		rs.write("  response_functions = 2 # Objective Function, Constraint 1, Constraint 2\n")
		rs.write("  response_descriptors 'SEA' 'PEAK'\n")
		rs.write("  no_gradients # Do not need graedients for sampling\n")
		rs.write("  no_hessians \n")


		rs.write("interface,\n")
		rs.write("  id_interface = 'SAMP_INTERFACE'\n")
		rs.write("  fork\n")
		rs.write("	analysis_driver = 'python driver.py'\n")
		rs.write("	# analysis_components = 'surr'\n")
		rs.write("	# output_filter   = 'HC_output_filter.sh'\n")
		rs.write("	parameters_file = 'driver.in'\n")
		rs.write("	results_file	= 'driver.out'\n")

		rs.write("	aprepro\n")
		rs.write("	deactivate\n")
		rs.write("		  # evaluation_cache  # Deactivation of the evaluation cache\n")
		rs.write("		  restart_file	  # Deactivation of the restart file\n")
		rs.write("		  # active_set_vector # Deactivation of ASV requests. Use for driver simplicity\n")
	  
		rs.write("	asynchronous\n")
		rs.write("	 # evaluation_concurrency = 25  # Concurrency of the evaluations\n")
		rs.write("	 analysis_concurrency = 1	  # Concurrency of the analysis drivers\n")

		rs.write("	work_directory\n")
		rs.write("	  named 'sample'\n")
		rs.write("	  directory_tag	 # Tag working directories with iteration number\n")
		rs.write("	  directory_save	# Save work directories\n")
		rs.write("	  file_tag		  # Tag parameters and results files with iteration number\n")
		rs.write("	  file_save		 # Save parameters and results files\n")
		rs.write("	  copy_files = 'driver.py' \n")
		rs.write("				   'paramodel.py'\n")
		rs.write("				   'l-abaqus.sh'\n")

# Iterator --------------------------------------------------------------------
if not os.path.isfile(home+'/model/report.er'):
	with open(home+'/model/report.er', 'w') as r:
		r.write('  # Job reporter')
else:
	with open(home+'/model/report.er', 'a') as r:
		r.write('-'*15)

for case in [(ge, un, rl, ea, np) for ge in geom for un in union for rl in fill for ea in espads for np in nptos]:
	g, u, r, e, n = case[0], case[1], case[2], case[3], case[4]
	if DO or SAMP or reSAMP or SOGA:  # Dakota optimization cases
		if SAMP:
			wdir = home+'/model/samp'
			if not reSAMP:
				try:
					os.mkdir(wdir)
				except:
					pass
			os.chdir(wdir)
			code = 'SAMP'
		if DO:
			wdir = home+'/model/optim'
			try:
				os.mkdir(wdir)
			except:
				pass
			os.chdir(wdir)
			code = 'DO'
		qa(g, u, r, e, n, code=code, DO=DO, SAMP=SAMP, SOGA=SOGA, cpu=cpu, mem=mem)
		qd(g, u, r, e, n, DO, SAMP, reSAMP, SOGA)
	else:  # Normal job
		code = coder(g, u, r, e, n)
		try:
			os.mkdir(home+'/model/'+code)
		except:
			pass
		os.chdir(home+'/model/'+code)
		qa(g, u, r, e, n, code=code)

sleep(5)
qs = Popen(["qs"])
qs.wait()