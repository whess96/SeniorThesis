################################################################################
# testControlLoop.sh
#
# Runs the control loop without vicon or arduino and with fake data
################################################################################

trap "exit" INT TERM ERR
trap "kill 0" EXIT

python produceTestData.py &
python controller.py &
python writeLogs.py &
# python serialWriter.py &

wait