#!/usr/bin/env python
#
# Photo booth
# Listen to GPIO events:
#  - on button press, will:
#       blink an LED
#       take 4 pictures
#       save them
#       turn off the LED
# - on switch Off:
#       shutdown the Rapspi

import os, time
from gpiozero import LED, Button
from picamera import PiCamera
from signal import pause

save_path = os.path.join(os.environ['HOME'], 'photopi')
time_blink = 1
time_between_pics = 3
pin_green_led = 27
pin_red_led = 17
pin_photo = 22
#pin_off = 24
nb_pictures = 4


def takePictures(camera, batch, led):
    print "taking picture for batch %i" % batch
    for x in range(0, nb_pictures):
        led.toggle()
        camera.capture(os.path.join(save_path, "photo_%s_%s.jpg" % (batch, x)))
        led.toggle()
        time.sleep(time_between_pics)

def pictureButtonPress(camera, green, red):
    print "in pictureButtonPress"
    batch = time.time()
    green.off()
    red.on()
    takePictures(camera, batch, green)
    red.off()
    green.on()


if __name__ == '__main__':
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    greenLed = LED(pin_green_led)
    redLed = LED(pin_red_led)
    button = Button(pin_photo)

    redLed.on()
    greenLed.off()

    camera = PiCamera()
    #camera.resolution = (1024, 768)
    camera.resolution = (2592, 1944)
    camera.start_preview()
    greenLed.on()
    redLed.off()

    #while True:
    for x in range(0,2):
        print "Waiting for button...."
        button.wait_for_press()
        #time.sleep(10)
        pictureButtonPress(camera, greenLed, redLed)

    # loop
    #pause()
