from mpu6050 import mpu6050
from multiprocessing import Value, Array
from adafruit_servokit import ServoKit
import gpiozero

kit = ServoKit(channels=8)
imu = mpu6050(0x68)

# servo_angles = Array('i', [90] * 4)
# imu_data = Array('d', [0] * 6)
# left_ground = Value('b', False)
# right_ground = Value('b', False)

left_input = gpiozero.Button(pin=27, pull_up=False)
right_input = gpiozero.Button(pin=17, pull_up=False)


def main(servo_angles, imu_data, left_ground, right_ground):
    while True:
        updateServos(servo_angles)
        imu_data[0], imu_data[1], imu_data[2], imu_data[3], imu_data[4], imu_data[5], left_ground.value, right_ground.value = readSensors()


def updateServos(servo_angles):
    for i in range(4):
        kit.servo[i].angle = servo_angles[i]


def readSensors():
    accel_data = imu.get_accel_data()
    gyro_data = imu.get_gyro_data()
    return accel_data['x'], accel_data['y'], accel_data['z'], gyro_data['x'], gyro_data['y'], gyro_data['z'], right_input.value, right_input.value
