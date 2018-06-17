#!/usr/bin/env python

import wiringpi

import gaugette.switch

import time

# buttons
SW_UP_PIN = 3 #3 # 14
SW_DOWN_PIN = 0 #0 # 12
SW_PIN = 2 #2 # 13

exitFlag = 0
lastDirection = 0
lastUpdated = 0

gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

switch_up = gaugette.switch.Switch(SW_UP_PIN, gpio)
switch = gaugette.switch.Switch(SW_PIN, gpio)
switch_down = gaugette.switch.Switch(SW_DOWN_PIN, gpio)
last_state = None

print_delta = True
delta_zero = 0


def init():
    # Main program block

    print "setup buttons..."

    print "setup buttons done."


if __name__ == '__main__':

    print "start"

    init()


 #   continueMe = not switch.get_state()
 #   while continueMe:
 #       continueMe = not switch.get_state()
 #       if lastUpdated:
 #           lastUpdated = 0
 #           if lastDirection:
 #               print "Right"
 #           else:
 #               print "Left"
 #       time.sleep(0.3)

    exitFlag = 1

    print("Main End")
