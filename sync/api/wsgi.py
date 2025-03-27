import sys, os
sys.path.append(os.path.abspath('..'))
import roboControl.controller as roboController
from multiprocessing import Process, Value, Array
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

servo_angles = Array('i', [90] * 4)
imu_data = Array('d', [0.0] * 6)
left_ground = Value('b', False)
right_ground = Value('b', False)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/robot_data", methods=['GET'])
def show_name():
    return {
        "servo1": servo_angles[0],
        "servo2": servo_angles[1],
        "servo3": servo_angles[2],
        "servo4": servo_angles[3],
        "imuax": imu_data[0],
        "imuay": imu_data[1],
        "imuaz": imu_data[2],
        "imugx": imu_data[3],
        "imugy": imu_data[4],
        "imugz": imu_data[5],
        "groundl": left_ground.value,
        "groundr": right_ground.value,
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
    global robot_controller
    robot_controller = Process(target=roboController.main, args=(servo_angles, imu_data, left_ground, right_ground))
    robot_controller.start()