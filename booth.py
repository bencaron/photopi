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
time_between_pics = 5
pin_green_led = 4
pin_red_led = 17
pin_photo = 22
#pin_off = 24
nb_pictures = 4


def takePictures(camera, batch, led):
    print "taking picture for batch %i" % batch
    #led.blink(time_blink, time_blink)
    for x in range(0, nb_pictures):
        led.on()
        camera.capture(os.path.join(save_path, "photo_%s_%s.jpg" % (batch, x)))
        time.sleep(time_between_pics)
        led.off()
    #led.off()

def pictureButtonPress(camera, green, red):
    print "in pictureButtonPress"
    batch = time.time()
    green.off()
    takePictures(camera, batch, red)
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
    redLed.off()

    while True:
        print "Waiting for button...."
        button.wait_for_press()
        pictureButtonPress(camera, greenLed, redLed)

    # loop
    #pause()
