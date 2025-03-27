from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

# while True:
#     kit.servo[0].angle = 180
#     sleep(1)
#     kit.servo[0].angle = 0
#     sleep(1)
#
while True:
    for i in range(4):
        kit.servo[i].angle = 180
    sleep(1)
    for i in range(4):
        kit.servo[i].angle = 0
    sleep(1)
