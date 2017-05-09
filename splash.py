#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import lcd as lcd


def show_splash():
    # Send some test
    lcd.print_lcd(lcd.LCD_LINE_1, "Arild Langseid")
    lcd.print_lcd(lcd.LCD_LINE_2, "Raspberry PI")
    lcd.print_lcd(lcd.LCD_LINE_3, "GPIO-version: " + GPIO.VERSION)
    lcd.print_lcd(lcd.LCD_LINE_4, "GPIO-revision: " + str(GPIO.RPI_REVISION))

#    time.sleep(2)
