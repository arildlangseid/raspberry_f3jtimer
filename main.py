#!/usr/bin/env python

# import
import RPi.GPIO as GPIO
import time
import os
import math
import sys
import lcd as lcd
import buttons as buttons
import led as led
import splash as splash
import pygame
import nrf24l01
import f3jmenu
import f5jmenu
import f3kmenu

def printf(print_format, *args):
    sys.stdout.write(print_format % args)


def init():
    # Main program block

    # Initialise display
    lcd.lcd_init()

#    buttons.init()

    led.init_gpio()
    led.init_max7219()
    led.send_blank_all()

    # time.sleep(2)

    pygame.mixer.init()

    nrf24l01.init()


SLEEP = 0.0001
return_to_menu = False
shutdown_on_exit = False


# menu
# ******** F3J *******
# ******** F5J *******
# ******** F3K *******
# ***** Power off ****
main_menu_choice = 1


def update_menu():
    #  lcd.lcd_init()
    global main_menu_choice
    nrf24l01.setBlank()
    if main_menu_choice == 1:
        lcd.print_lcd(lcd.LCD_LINE_1, "******** F3J *******")
    else:
        lcd.print_lcd(lcd.LCD_LINE_1, "         F3J        ")
    if main_menu_choice == 2:
        lcd.print_lcd(lcd.LCD_LINE_2, "******** F5J *******")
    else:
        lcd.print_lcd(lcd.LCD_LINE_2, "         F5J        ")
    if main_menu_choice == 3:
        lcd.print_lcd(lcd.LCD_LINE_3, "******** F3K *******")
    else:
        lcd.print_lcd(lcd.LCD_LINE_3, "         F3K        ")
    if main_menu_choice == 4:
        lcd.print_lcd(lcd.LCD_LINE_4, "***** Power off ****")
    else:
        lcd.print_lcd(lcd.LCD_LINE_4, "      Power off     ")


def main_menu():
    global main_menu_choice

    update_menu()
    buttons.init()

    led.disable()

    continue_program = True
    while continue_program:

        button_pressed = buttons.switch.get_state()
        if button_pressed:
            while buttons.switch.get_state():
                pass

            print("main_menu_choice=" + str(main_menu_choice))

            if main_menu_choice == 1:
		f3jmenu.main_menu()
		update_menu()

            if main_menu_choice == 2:
		f5jmenu.main_menu()
                update_menu()

            if main_menu_choice == 3:
                led.enable()
                f3kmenu.main_menu()
                led.disable()
                update_menu()

            if main_menu_choice == 4:
                continue_program = False

                led.disable()

                if shutdown_on_exit:
                    lcd.print_lcd(lcd.LCD_LINE_1, "!  SHUTTING DOWN!  !")
                    lcd.print_lcd(lcd.LCD_LINE_2, "!!!!!!!!!!!!!!!!!!!!")
                    lcd.print_lcd(lcd.LCD_LINE_3, "Wait 60 sec before  ")
                    lcd.print_lcd(lcd.LCD_LINE_4, "disconnecting power ")
                    os.system('sudo /sbin/halt')
#                else:
#                    lcd.print_lcd(lcd.LCD_LINE_1, "Timer Exit....      ")
#                    lcd.print_lcd(lcd.LCD_LINE_2, "                    ")
#                    lcd.print_lcd(lcd.LCD_LINE_3, "                    ")
#                    lcd.print_lcd(lcd.LCD_LINE_4, "                    ")

        button_up_pressed = buttons.switch_up.get_state()
        if button_up_pressed:
            while buttons.switch_up.get_state():
                pass
            if main_menu_choice == 1:
                main_menu_choice = 5
                print "Up - Bottom"
            if main_menu_choice > 1:
                main_menu_choice -= 1
                print "Up"
            update_menu()

        button_down_pressed = buttons.switch_down.get_state()
        if button_down_pressed:
            while buttons.switch_down.get_state():
                pass
            if main_menu_choice == 4:
                main_menu_choice = 0
                print "Down - Top"
            if main_menu_choice < 4:
                main_menu_choice += 1
                print "Down"
            update_menu()

        time.sleep(0.1)

    buttons.exitFlag = 1


def init_sounds():
    lcd.print_lcd(lcd.LCD_LINE_3, "Loading sounds")

    os.system('sudo amixer cset numid=3 1')

    os.system('sudo /usr/bin/amixer cset numid=1 -- 10%')
    #  os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/00_silence.ogg &')
    lcd.print_lcd(lcd.LCD_LINE_4, "01_five_min_preparat")
    os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/01_five_min_preparation_time.ogg &')
    time.sleep(5)
    lcd.print_lcd(lcd.LCD_LINE_4, "02_workingtime_will_")
    os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/02_workingtime_will_start_in_30_seconds.ogg &')
    time.sleep(5)
    lcd.print_lcd(lcd.LCD_LINE_4, "03_workingtime_will_")
    os.system(
        'sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/03_workingtime_will_start_at_the_loooong_tone.ogg &')
    time.sleep(14)
    lcd.print_lcd(lcd.LCD_LINE_4, "04_eight_minutes.ogg")
    os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/04_eight_minutes.ogg &')
    time.sleep(3)
    lcd.print_lcd(lcd.LCD_LINE_4, "05_workingtime_count")
    os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/05_workingtime_countdown.ogg &')
    time.sleep(15)


if __name__ == '__main__':
    try:
        init()

        splash.show_splash()

        # /etc/init.d/f3j is setting up an argument to make the boot finnish
        if len(sys.argv) == 2:
            shutdown_on_exit = True

        # initSounds()
        os.system('sudo /usr/bin/amixer cset numid=3 1')
        os.system('sudo /home/pi/f3jtimer/vol.sh 100')
        # set volume
        #    os.system('sudo /usr/bin/amixer cset numid=1 -- 20%')
        #    os.system('sudo /usr/bin/amixer set PCM -- -2200')
        #    os.system('sudo /usr/bin/amixer set PCM -- -3200')
        #    os.system('sudo /usr/bin/amixer set PCM,0 20%')

        if not buttons.switch.get_state():
            main_menu()
        else:
            if shutdown_on_exit:
                os.system('sudo /sbin/halt')
                print("Halt")

    finally:
        lcd.print_lcd(lcd.LCD_LINE_1, "Timer Exit....      ")
        lcd.print_lcd(lcd.LCD_LINE_2, "                    ")
        lcd.print_lcd(lcd.LCD_LINE_3, "                    ")
        lcd.print_lcd(lcd.LCD_LINE_4, "                    ")

        GPIO.cleanup()
        # GPIO.cleanup()
        # main()


