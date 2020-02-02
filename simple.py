import math
from functools import reduce
import operator
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageChops
import serial

def stop_other_functions():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(b'1')

# to add to Arduino code:
# void setup(){
#   Serial.begin(9600);
# }
# void loop(){
#   if(Serial.available()){         //From RPi to Arduino
#     if((Serial.read() - '0') = 1){  //conveting the value of chars to integer
#     Serial.println(Serial.read());
#     break;
#    }
#   }
# }
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

