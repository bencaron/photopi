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
blink_time = 1
pin_green_led = 4
pin_red_led = 17
pin_photo = 22
#pin_off = 24
nb_pictures = 4


def takePictures(camera, batch):
    print "taking picture for batch %i" % batch
    for x in range(0, nb_pictures):
        camera.capture(os.path.join(save_path, "photo_%s_%s.jpg" % (batch, x)))

def pictureButtonPress(camera, green, red):
    print "in pictureButtonPress"
    batch = time.time()
    green.off()
    red.blink(blink_time, blink_time, blink_time * nb_pictures, True)
    takePictures(camera, batch)
    red.off()
    green.on()


if __name__ == '__main__':
    print "hello"
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    greenLed = LED(pin_green_led)
    redLed = LED(pin_red_led)
    button = Button(pin_photo)

    redLed.on()
    greenLed.off()

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    greenLed.on()

    while True:
        print "Waiting for button...."
        greenLed.on()
        button.wait_for_press()
        pictureButtonPress(camera, greenLed, redLed)

    # loop
    #pause()
