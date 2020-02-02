from picamera import PiCamera
from time import sleep
import Image
import ImageChops


camera = PiCamera()
camera.start_preview()

for i in range(50):
    camera.capture("image1.jpg")
    sleep(3)
    camera.capture("image2.jpg")
    diff = ImageChops.difference(Image.open("image1.jpg"), Image.open("image2.jpg"))
    print("\nDifference: ", diff)
    sleep(3)

camera.stop_preview()

