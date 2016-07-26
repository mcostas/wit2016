PARAMETERS_FILE=$1
QSUB_COMMAND="/opt/gridengine/bin/lx26-amd64/qsub"
PARAMETERIZED_MODEL_FILE="/home/lpire/pt_lpire_memoria/codes/paramodel.py"
DEFAULT_VALUES_FILE="default.dat"
MODEL_FILE="model_dakota.py"
QUEUE_LAUNCHER="lancer_dakota.sh"
# Sustitucion de las variables generadas por DAKOTA en el modelo parametrizado
dprepro $PARAMETERS_FILE $PARAMETERIZED_MODEL_FILE ${MODEL_FILE}.tmp
dprepro $DEFAULT_VALUES_FILE ${MODEL_FILE}.tmp $MODEL_FILE
rm -f ${MODEL_FILE}.tmp
# Ejecucion del analisis
$QSUB_COMMAND $QUEUE_LAUNCHER
