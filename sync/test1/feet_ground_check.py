from time import sleep
import gpiozero

left_input = gpiozero.Button(pin=27, pull_up=False)
right_input = gpiozero.Button(pin=17, pull_up=False)

while True:
    print(f"left: {left_input.value}\n"
          f"right: {right_input.value}\n")
    sleep(.2)