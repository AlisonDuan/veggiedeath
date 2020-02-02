import math
from functools import reduce
import operator
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageChops
from gpiozero import Motor

def stop_other_functions():
    motor_conveyor1 = Motor(1, 2)
    motor_conveyor1.stop()
    motor_conveyor2 = Motor(3, 4)
    motor_conveyor2.stop()
    motor_rotor = Motor(5, 6)
    motor_rotor.stop()

camera = PiCamera()
camera.start_preview()

rms = 10000

#  might need to change this threshold later depending on how well
#  the camera can distinguish a line of vegetables/targets from
#  being different vs. an empty conveyor belt
while rms > 50:
    camera.capture("image1.jpg")
    img1 = Image.open("image1.jpg")
    sleep(3)
    camera.capture("image2.jpg")
    img2 = Image.open("image2.jpg")
    diff = ImageChops.difference(img1, img2).histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda diff, i: diff * (i**2), diff, range(256))) / (float(img1.size[0]) * img1.size[1]))
    print("\nDifference: ", rms)
    sleep(3)

camera.stop_preview()
stop_other_functions()

