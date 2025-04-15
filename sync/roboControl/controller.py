# import multiprocessing
import os
import sys
import time
from multiprocessing import shared_memory
from mpu6050 import mpu6050
from adafruit_servokit import ServoKit
import gpiozero
sys.path.append(os.path.abspath('..'))
from roboControl.imu_calib import imu_offsets

class Controller:

    def __init__(self):
        self.kit = ServoKit(channels=8)
        self.imu = mpu6050(0x68)
        self.left_input = gpiozero.Button(pin=27, pull_up=False)
        self.right_input = gpiozero.Button(pin=17, pull_up=False)
        self.accel_offsets = [0.0, 0.0, 0.0]
        self.gyro_offsets = [0.0, 0.0, 0.0]
        self.servo_offsets = [-1, 3, -7, 5]

    def controller_init(self, sharedListName):
        # logger = multiprocessing.get_logger()
        global sl
        sl = shared_memory.ShareableList(name=sharedListName)
        self.updateServos()
        time.sleep(2)
        self.accel_offsets, self.gyro_offsets = imu_offsets()

        while True:
            self.updateServos()
            self.readSensors()
            # logger.debug(sl)

    def updateServos(self):
        for i in range(4):
            self.kit.servo[i].angle = sl[i] + self.servo_offsets[i]

    def readSensors(self):
        accel_data = self.imu.get_accel_data()
        gyro_data = self.imu.get_gyro_data()
        sl[4] = (accel_data['x'] - self.accel_offsets[0]) / -9.81
        sl[5] = (accel_data['y'] - self.accel_offsets[1]) / 9.81
        sl[6] = (accel_data['z'] - self.accel_offsets[2]) / 9.81
        sl[7] = gyro_data['x'] - self.gyro_offsets[0]
        sl[8] = gyro_data['y'] - self.gyro_offsets[1]
        sl[9] = gyro_data['z'] - self.gyro_offsets[2]
        sl[10] = self.right_input.value
        sl[11] = self.left_input.value
