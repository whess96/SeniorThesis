################################################################################
# run_contol_loop.sh
#
# Runs the full control loop for the plane. Involves running several python
# scripts in parallel.
#
# Inspired by: 
# https://spin.atomicobject.com/2017/08/24/start-stop-bash-background-process/
################################################################################

trap "exit" INT TERM ERR
trap "kill 0" EXIT

./ViconDataStreamSDK/streamPlaneData > vicon_eflite_logs.txt &
# python observer.py &
python controller.py &
python serial_writer.py &

wait