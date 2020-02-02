import math
from functools import reduce
import operator
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageChops


camera = PiCamera()
camera.start_preview()

for i in range(50):
    img1 = camera.capture("image1.jpg")
    sleep(3)
    img2 = camera.capture("image2.jpg")
    diff = ImageChops.difference(Image.open(img1), Image.open(img2)).histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda diff, i: diff * (i**2), diff, range(256))) / (float(img1.size[0]) * img1.size[1]))
    print("\nDifference: ", rms)
    sleep(3)

camera.stop_preview()

