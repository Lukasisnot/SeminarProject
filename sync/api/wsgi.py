import logging
import multiprocessing
import sys, os

sys.path.append(os.path.abspath('..'))
import roboControl.controller as robot_controller

from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager
from flask import Flask, render_template, request

app = Flask(__name__)

smm = SharedMemoryManager()
smm.start()
sl = smm.ShareableList([90, 90, 90, 90, 0, 0, 0, 0, 0, 0, 0, 0])

processes = []

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/manual")
def manualControl():
    return render_template('manual_control.html')

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
        sl[int(data['id'])] = int(data['servo'])
        logging.debug(data['servo'])
        return request.data
    # logger.debug(sl)

def newProcess(name, target, args):
    process = Process(target=target, args=args, name=name)
    process.start()
    processes.append(process)
    print("Made new control process: " + process.name)

def findProcessByName(name):
    for process in processes:
        if process.name == name:
            return process, True
    return None, False

def on_terminate():
    for p in processes:
        print("Terminating process: " + p.name)
        p.terminate()
        p.terminate()
        p.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)
    multiprocessing.log_to_stderr(logging.DEBUG)

    roboController = robot_controller.Controller()
    newProcess("robot_controller", roboController.controller_init, (sl.shm.name,))

    try:
        app.run(host='0.0.0.0', debug=False, port=5000)
    finally:
        on_terminate()
