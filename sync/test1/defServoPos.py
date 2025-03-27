from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

for i in range(4):
    kit.servo[i].angle = 180 / 2