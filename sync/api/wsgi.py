import logging
import multiprocessing
import sys, os

sys.path.append(os.path.abspath('..'))
import roboControl.controller as robot_controller
import roboControl.imu_calib as imu_calib

from multiprocessing import Process, Value, Array, shared_memory
from multiprocessing.managers import SharedMemoryManager, SyncManager
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

smm = SharedMemoryManager()
smm.start()
sl = smm.ShareableList([90, 93, 83, 90, 0, 0, 0, 0, 0, 0, 0, 0])
accel_offsets = [0.0,0.0,0.0]
gyro_offsets = [0.0,0.0,0.0]

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/robot_data", methods=['GET', 'POST'])
def getRobotData():
    if request.method == 'GET':
        return {
            "servo1": sl[0],
            "servo2": sl[1],
            "servo3": sl[2],
            "servo4": sl[3],
            "imuax": sl[4] - accel_offsets[0],
            "imuay": sl[5] - accel_offsets[1],
            "imuaz": sl[6] - accel_offsets[2],
            "imugx": sl[7] - gyro_offsets[0],
            "imugy": sl[8] - gyro_offsets[1],
            "imugz": sl[9] - gyro_offsets[2],
            "groundl": sl[10],
            "groundr": sl[11],
        }
    if request.method == 'POST':
        data = request.json
        sl[int(data['id'])] = int(data['servo'])
        logging.debug(data['servo'])
        return request.data
    # logger.debug(sl)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    multiprocessing.log_to_stderr(logging.DEBUG)
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)

    accel_offsets, gyro_offsets = imu_calib.imu_offsets()

    roboController = robot_controller.Controller()
    rcProcess = Process(target=roboController.controller_init, args=(sl.shm.name,))
    rcProcess.start()

    try:
        app.run(host='0.0.0.0', debug=False, port=5000)
    finally:
        rcProcess.terminate()
        rcProcess.join()

