#!/usr/bin/python

import RPi.GPIO as GPIO
import time

DIN_PIN = 2  # gpio - pin 3 -> max7219 - pin 1
CSL_PIN = 3  # gpio - pin 5 -> max7219 - pin 12
CLK_PIN = 4  # gpio - pin 7 -> max7219 - pin 13

exitFlag = 0
lastDirection = 0
lastUpdated = 0


def init_gpio():
    print "setup GPIO..."

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIN_PIN, GPIO.OUT)
    GPIO.setup(CSL_PIN, GPIO.OUT)
    GPIO.setup(CLK_PIN, GPIO.OUT)

    GPIO.output(DIN_PIN, False)
    GPIO.output(CSL_PIN, True)
    GPIO.output(CLK_PIN, False)

    print "setup GPIO done."


E_PULSE = 0.0001
INIT_PULSE = 0.0000
BIT_PULSE = 0.000000000000


def send_bit(bit):
    GPIO.output(CLK_PIN, False)
    time.sleep(BIT_PULSE)
    GPIO.output(DIN_PIN, bit)
    time.sleep(BIT_PULSE)
    GPIO.output(CLK_PIN, True)
    time.sleep(BIT_PULSE)


def send_bit_print(bit):
    #  print (str(bit))
    send_bit(bit)


def send_command(address, data):
    GPIO.output(CSL_PIN, False)
    time.sleep(INIT_PULSE)

    outLed = ""

    send_bit_print((address >> 7) & 1)
    send_bit_print((address >> 6) & 1)
    send_bit_print((address >> 5) & 1)
    send_bit_print((address >> 4) & 1)
    send_bit_print((address >> 3) & 1)
    send_bit_print((address >> 2) & 1)
    send_bit_print((address >> 1) & 1)
    send_bit_print((address >> 0) & 1)

    #  outLed = str((address >> 7)&1) + str((address >> 6)&1) + str((address >> 5)&1) + str((address >> 4)&1)
    #  outLed = outLed + str((address >> 3)&1) + str((address >> 2)&1) + str((address >> 1)&1) + str((address >> 0)&1)

    send_bit_print((data >> 7) & 1)
    send_bit_print((data >> 6) & 1)
    send_bit_print((data >> 5) & 1)
    send_bit_print((data >> 4) & 1)
    send_bit_print((data >> 3) & 1)
    send_bit_print((data >> 2) & 1)
    send_bit_print((data >> 1) & 1)
    send_bit_print((data >> 0) & 1)

    #  outLed = outLed + " - " + str((data >> 7)&1) + str((data >> 6)&1) + str((data >> 5)&1) + str((data >> 4)&1)
    #  outLed = outLed + str((data >> 3)&1) + str((data >> 2)&1) + str((data >> 1)&1) + str((data >> 0)&1)

    #  print (outLed)

    GPIO.output(CSL_PIN, True)


def send_blank_all():
    send_command(1, 15)
    send_command(2, 15)
    send_command(3, 15)
    send_command(4, 15)
    send_command(5, 15)
    send_command(6, 15)
    send_command(7, 15)
    send_command(8, 15)


def init_max7219():
    print("Init max7219")

    send_command(12, 1)  # Wake up - 0 - Shutdown, 1 - Wake up
    send_command(10, 13)  # Intensity
    send_command(11, 3)  # Scan limit
    send_command(9, 15)  # Decode mode - 0 - all binary, 1 - Code 1, 15 - binary0-3 code4-7, 255 - all code
    send_command(15, 0)  # 0 - Normal mode, 1 - Display Test mode

    print("Init max7219 done.")


def enable():
    init_max7219()


def disable():
    send_command(12, 0)


def set_time(timeout, timer_name):
    if timer_name == "P":
        send_command(1, 15)
        send_command(2, 15)
    else:
        if timer_name == "PR":
            send_command(1, 10)
        else:
            if int(timeout[0]) == 0:
                send_command(1, 15)
            else:
                send_command(1, int(timeout[0]))
        send_command(2, int(timeout[1]))

    send_command(3, int(timeout[3]))
    send_command(4, int(timeout[4]))


if __name__ == '__main__':
    try:

        print "start"

        init_gpio()
        init_max7219()

        print "sendBlankAll"
        #    sendBlankAll()

        print "sleep"
        time.sleep(1)

        timeout = "18:45"
        #    setTime(timeout)
        print "display"
        send_command(1, 15)
        send_command(2, 8)
        send_command(3, 0)
        send_command(4, 6)

        print("done.")
    # sendBlankAll()

    finally:
        GPIO.cleanup()

    print("Main End")
