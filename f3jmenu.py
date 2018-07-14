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


# timer_name: P - pause, PR - Preparation Time, WT - Working Time
def my_timer(time_length, timer_name, sound1_time_all, sound1_file, sound2_time_all, sound2_file):
    global return_to_menu

    return_to_menu = False

    sound1_time_tens = "0"
    sound2_time_tens = "0"
    if len(sound1_time_all) == 7:
        sound1_time = sound1_time_all[:5]
        sound1_time_tens = sound1_time_all[6]
    else:
        sound1_time = sound1_time_all

    if len(sound2_time_all) == 7:
        sound2_time = sound2_time_all[:5]
        sound2_time_tens = sound2_time_all[6]
    else:
        sound2_time = sound2_time_all

    # print("sound1_time_all")
    #  print(sound1_time_all)
    #  print("len(sound1_tinme_all)")
    #  print(len(sound1_time_all))
    #  print("sound1_time_tens")
    #  print(sound1_time_tens)
    #  print("sound1_time")
    #  print(sound1_time)

    # 5400s on RaspberryPI is 5408s in the real world (90min)
    time_corr = float(float(5400) / float(5400))
    #  print("time_corr")
    #  print(time_corr)

    time_start = time.time()
    time_last = time.time() - time_start
    #  print("Time length:")
    #  print(time_length)
    #  print("Start time:")
    #  print(time_last);
    done = False
    sound1_played = False
    sound2_played = False

    while True:
        # calculate minutes and seconds left
        seconds = time_left = int(time_length + 1 - time_last)
        minutes = 0

        #    print (time_last)
        tens = (time_last - math.floor(time_last))
        tens = math.floor(tens * 10)
        #    print (int(tens))

        if time_left > 59:
            minutes = int(time_left / 60.0)
            seconds = time_left % 60

        if minutes > 9:
            m = str(minutes)
        else:
            m = "0" + str(minutes)

        if seconds > 9:
            s = str(seconds)
        else:
            s = "0" + str(seconds)

        time_output = m + ":" + s

        #    lcd.print_lcd(lcd.LCD_LINE_4, time_output)
        #    led.setTime(time_output, timer_name)

        if not sound1_played:
            if sound1_time_all != "-1":
                if time_output == sound1_time:
                    #          print("tens:")
                    #          print(int(tens))
                    #          print("sound1_time_tens:")
                    #          print(sound1_time_tens)
                    if int(tens) >= int(sound1_time_tens):
                        #            print("play ogg file")
                        #os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/' + sound1_file + '&')
                        #os.system('sudo /usr/bin/omxplayer /home/pi/f3jtimer/' + sound1_file + '&')
                        pygame.mixer.music.load("/home/pi/f3jtimer/" + sound1_file)
                        pygame.mixer.music.play()
                        sound1_played = True

        if not sound2_played:
            if sound2_time_all != "-1":
                if time_output == sound2_time:
                    if int(tens) >= int(sound2_time_tens):
                        #os.system('sudo /usr/bin/mplayer -msglevel all=-1 /home/pi/f3jtimer/' + sound2_file + '&')
                        #os.system('sudo /usr/bin/omxplayer /home/pi/f3jtimer/' + sound2_file + '&')
                        pygame.mixer.music.load("/home/pi/f3jtimer/" + sound2_file)
                        pygame.mixer.music.play()
                        sound2_played = True

        time_uncorrected = (float(time.time()) - float(time_start))
        time_last = time_uncorrected * time_corr

        #   if s == "00":
        #     if diff_printed == 0:
        #       print("time_last uncorrected")
        #       print(time_uncorrected)
        #       print("time_last corrected")
        #       print(time_last)
        #       print("difference")
        #       print(time_uncorrected - time_last)
        #       print(" ")
        #     diff_printed = 1
        #   else:
        #     diff_printed = 0

        button_pressed = buttons.switch.get_state()
        if button_pressed:
            while buttons.switch.get_state():
                pass
            done = True
            return_to_menu = True

        # if we're done
        if done:
            led.send_blank_all()
            break
        else:
            lcd.print_lcd(lcd.LCD_LINE_4, time_output)
            led.set_time(time_output, timer_name)
#            nrf24l01.nrf24_send(['H', 'E', 'L', 'O', '1'])
            nrf24l01.send(timer_name+time_output+' ')

        # loop once more so we get 0 seconds left in the end
        if time_last > time_length:
            done = True
        else:
            time.sleep(SLEEP)

            #  print("End time:")
            #  print(time_last)
            #  print(" ")
    return


def f3j_innledende():
    global return_to_menu

    lcd.lcd_init()
    lcd.print_lcd(lcd.LCD_LINE_1, "Cirrus F3J Timer")
    lcd.print_lcd(lcd.LCD_LINE_2, "Preliminary 5+10min")
    lcd.print_lcd(lcd.LCD_LINE_3, "Start")
    my_timer(5, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

    if return_to_menu:
        return

    done = False
    while not done:
        lcd.print_lcd(lcd.LCD_LINE_3, "Preparation Time")
        my_timer(5 * 60 + 00, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:10.4",
                 "03_10min_workingtime_will_start_at_the_loooong_tone.ogg")

        if return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "PreparationTime Skip")
            my_timer(0 * 60 + 40, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:10.4",
                     "03_10min_workingtime_will_start_at_the_loooong_tone.ogg")

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Working Time")
            my_timer(10 * 60 + 00, "WT", "02:03.2", "04_eight_minutes.ogg", "00:11.1", "05_workingtime_countdown.ogg")

        if return_to_menu:
            break

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Pause")
            my_timer(30, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

        if return_to_menu:
            break

    return_to_menu = False
    return


def f3j_finale():
    global return_to_menu

    lcd.lcd_init()
    lcd.print_lcd(lcd.LCD_LINE_1, "Cirrus F3J Timer")
    lcd.print_lcd(lcd.LCD_LINE_2, "Final 5+15min")
    lcd.print_lcd(lcd.LCD_LINE_3, "Start")
    my_timer(5, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

    if return_to_menu:
        return

    done = False
    while not done:
        lcd.print_lcd(lcd.LCD_LINE_3, "Preparation Time")
        my_timer(5 * 60 + 00, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:11.4",
                 "06_15min_workingtime_will_start_at_the_loooong_tone.ogg")

        if return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "PreparationTime Skip")
            my_timer(0 * 60 + 40, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:11.4",
                     "06_15min_workingtime_will_start_at_the_loooong_tone.ogg")

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Working Time")
            my_timer(15 * 60 + 00, "WT", "02:04.0", "07_thirteen_minutes.ogg", "00:11.1",
                     "05_workingtime_countdown.ogg")

        if return_to_menu:
            break

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Pause")
            my_timer(30, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

        if return_to_menu:
            break

    return_to_menu = False
    return


def f3j_training():
    global return_to_menu

    lcd.lcd_init()
    lcd.print_lcd(lcd.LCD_LINE_1, "Cirrus F3J Timer")
    lcd.print_lcd(lcd.LCD_LINE_2, "Training 1+2min30")
    lcd.print_lcd(lcd.LCD_LINE_3, "Start")
    my_timer(5, "P", "00:03.0", "01a_preperation_time_will_start_at_the_beep.ogg", "-1", "")

    if return_to_menu:
        return

    done = False
    while not done:
        lcd.print_lcd(lcd.LCD_LINE_3, "Preparation Time")
        my_timer(1 * 60 + 00, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:10.4",
                 "03a_workingtime_will_start_at_the_loooong_tone.ogg")

        if return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "PreparationTime Skip")
            my_timer(0 * 60 + 40, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:10.4",
                     "03a_workingtime_will_start_at_the_loooong_tone.ogg")

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Working Time")
            my_timer(2 * 60 + 30, "WT", "02:03.2", "04a_two_minutes_left_of_working_time.ogg", "00:11.1", "05_workingtime_countdown.ogg")

        if return_to_menu:
            break

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Pause")
            my_timer(30, "P", "00:03.0", "01a_preperation_time_will_start_at_the_beep.ogg", "-1", "")

        if return_to_menu:
            break

    return_to_menu = False
    return




def f3j_demo():
    global return_to_menu

    lcd.lcd_init()
    lcd.print_lcd(lcd.LCD_LINE_1, "Cirrus F3X Timer")
    lcd.print_lcd(lcd.LCD_LINE_2, "Demonstration")
    lcd.print_lcd(lcd.LCD_LINE_3, "Start")

    my_timer(0 * 60 + 40, "WT", "00:34.0", "07_thirteen_minutes.ogg", "00:11.1", "05_workingtime_countdown.ogg")

    my_timer(5, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

    if return_to_menu:
        return

    done = False
    while not done:
        lcd.print_lcd(lcd.LCD_LINE_3, "Preparation Time")
        my_timer(0 * 60 + 40, "PR", "00:34.2", "02_workingtime_will_start_in_30_seconds.ogg", "00:11.4",
                 "06_15min_workingtime_will_start_at_the_loooong_tone.ogg")

        if return_to_menu:
            break

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Working Time")
            my_timer(0 * 60 + 40, "WT", "00:34.0", "07_thirteen_minutes.ogg", "00:11.1", "05_workingtime_countdown.ogg")

        if return_to_menu:
            break

        if not return_to_menu:
            lcd.print_lcd(lcd.LCD_LINE_3, "Pause")
            my_timer(15, "P", "00:03.5", "01_five_min_preparation_time.ogg", "-1", "")

        if return_to_menu:
            break

    return_to_menu = False
    return


# menu
# **** Innledende ****
# ****** Finale ******
# ******* Demo *******
# ******* Halt *******
main_menu_choice = 1


def update_menu():
    #  lcd.lcd_init()
    global main_menu_choice
    nrf24l01.setBlank()
    if main_menu_choice == 1:
        lcd.print_lcd(lcd.LCD_LINE_1, "**** Preliminary ***")
    else:
        lcd.print_lcd(lcd.LCD_LINE_1, "     Preliminary    ")
    if main_menu_choice == 2:
        lcd.print_lcd(lcd.LCD_LINE_2, "****** Finals ******")
    else:
        lcd.print_lcd(lcd.LCD_LINE_2, "       Finals       ")
    if main_menu_choice == 3:
        lcd.print_lcd(lcd.LCD_LINE_3, "***** Training *****")
    else:
        lcd.print_lcd(lcd.LCD_LINE_3, "      Training      ")
    if main_menu_choice == 4:
        lcd.print_lcd(lcd.LCD_LINE_4, "***** Main Menu ****")
    else:
        lcd.print_lcd(lcd.LCD_LINE_4, "      Main Menu     ")


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
                led.enable()
                f3j_innledende()
                led.disable()
                update_menu()

            if main_menu_choice == 2:
                led.enable()
                f3j_finale()
                led.disable()
                update_menu()

            if main_menu_choice == 3:
                led.enable()
                f3j_training()
                led.disable()
                update_menu()

            if main_menu_choice == 4:
                continue_program = False

                led.disable()

                lcd.print_lcd(lcd.LCD_LINE_1, "Going to MainMenu.  ")
                lcd.print_lcd(lcd.LCD_LINE_2, "                    ")
                lcd.print_lcd(lcd.LCD_LINE_3, "                    ")
                lcd.print_lcd(lcd.LCD_LINE_4, "                    ")

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
        GPIO.cleanup()
        # GPIO.cleanup()
        # main()
