import logging
# import multiprocessing
# import sys, os
# import atexit
# from multiprocessing.shared_memory import SharedMemory

# sys.path.append(os.path.abspath('..'))
# import roboControl.controller as RobotController
# from multiprocessing import Process, Value, Array, shared_memory
# from multiprocessing.managers import SharedMemoryManager, SyncManager
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

sl = [90, 90, 90, 90, 0, 0, 0, 0, 0, 0, 0, 0]

@app.route("/")
def index():
    return render_template('index_test.html')

@app.route("/robot_data", methods=['GET', 'POST'])
def getRobotData():
    if request.method == 'GET':
        return {
            "servo1": sl[0],
            "servo2": sl[1],
            "servo3": sl[2],
            "servo4": sl[3],
            "imuax": sl[4],
            "imuay": sl[5],
            "imuaz": sl[6],
            "imugx": sl[7],
            "imugy": sl[8],
            "imugz": sl[9],
            "groundl": sl[10],
            "groundr": sl[11],
        }
    if request.method == 'POST':
        data = request.json
        sl[0] =  int(data['servo'])
        logging.debug(data['servo'])
        return request.data
    # logger.debug(sl)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)

    app.run(host='0.0.0.0', debug=True, port=5000)

