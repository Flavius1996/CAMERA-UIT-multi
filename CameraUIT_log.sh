# Linux script for UIT CAMERA

CFG_FILE=$1
CAMERA_FILE=$2

LOG="./logs/CAMERAUIT_full_logs_`date +'%d_%m_%Y__%H-%M-%S'`.txt"
exec &> >(tee -a "$LOG")
echo Logging output to "$LOG"

python -u ./CameraUIT_v2.py --cfg ${CFG_FILE} --camera ${CAMERA_FILE}
