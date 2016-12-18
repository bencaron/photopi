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

import os
from gpiozero import LED, Button
from time import sleep
from picamera import PiCamera
from signal import pause

save_path = os.path.join(os.environ['HOME'], 'photopi')
blink_time = 0.2
pin_green_led = 7
pin_red_led = 11
pin_photo = 15
#pin_off = 24
nb_pictures = 4


def takePictures(camera, batch):
    for x in range(0, nb_pictures):
        camera.capture(os.path.join(save_path, "photo_%s_%s.jpg" % (batch, x)))

def pictureButtonPress(camera, green, red):
    batch = time.time()
    green.off
    red.blink(blink_time, blink_time, 5, False)
    takePictures(camera, batch)
    red.blink(1, blink_time, 1, False)
    green.on


if __name__ == '__main__':
    print "hello"

    greenLed = LED(pin_green_led)
    redLed = LED(pin_red_led)
    button = Button(pin_photo)

    redLed.on
    greenLed.blink(blink_time, blink_time)

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()

    greenLed.on
    redLed.off

    button.when_pressed = pictureButtonPress(camera, greenLed, redLed)

    # loop
    pause()
