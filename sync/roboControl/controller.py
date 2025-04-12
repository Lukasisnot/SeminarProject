import multiprocessing
from multiprocessing import shared_memory

from mpu6050 import mpu6050
from adafruit_servokit import ServoKit
import gpiozero

class Controller:

    def __init__(self):
        self.kit = ServoKit(channels=8)
        self.imu = mpu6050(0x68)
        self.left_input = gpiozero.Button(pin=27, pull_up=False)
        self.right_input = gpiozero.Button(pin=17, pull_up=False)

    def controller_init(self, sharedListName):
        logger = multiprocessing.get_logger()
        global sl
        sl = shared_memory.ShareableList(name=sharedListName)
        # sl = shared_memory.ShareableList(sharedList)

        while True:
            self.updateServos()
            self.readSensors()
            # logger.debug(sl)

    def updateServos(self):
        for i in range(4):
            self.kit.servo[i].angle = sl[i]


    def readSensors(self):
        accel_data = self.imu.get_accel_data()
        gyro_data = self.imu.get_gyro_data()
        # sl[4:] = accel_data['x'], accel_data['y'], accel_data['z'], gyro_data['x'], gyro_data['y'], gyro_data['z'], self.right_input.value, self.left_input.value
        sl[4] = accel_data['x']
        sl[5] = accel_data['y']
        sl[6] = accel_data['z']
        sl[7] = gyro_data['x']
        sl[8] = gyro_data['y']
        sl[9] = gyro_data['z']
        sl[10] = self.right_input.value
        sl[11] = self.left_input.value
