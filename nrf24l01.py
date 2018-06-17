import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
#import time
import spidev

# Writing, Reading pipes
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())


def init():
    GPIO.setmode(GPIO.BCM)
    print "setup nrf24l01..."


    print("nrf24l01 init 1")


    print("nrf24l01 init 2")


    radio.begin(0, 7)  #Set spi-ce pin10, and rf24-CE pin 8

    radio.setPayloadSize(32)
    radio.setChannel(0x76)
#    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setPALevel(NRF24.PA_MAX)

    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    #radio.setRetries(15,15)

    #radio.openReadingPipe(1, pipes[1])
    radio.openWritingPipe(pipes[0])

    radio.printDetails()
    print "setup nrf24l01 done."

def send(time_output):
    radio.write(time_output)

def setBlank():
    radio.write("       ")

def test():
    c=1
    while True:
        buf = ['H', 'E', 'L', 'O', c]
        c = (c + 1) & 255
        # send a packet to receiver
        radio.write(buf)
        print ("Sent:"),
        print (buf)
        # did it return with a payload?
    #    if radio.isAckPayloadAvailable():
    #        pl_buffer=[]
    #        radio.read(pl_buffer, radio.getDynamicPayloadSize())
    #        print ("Received back:"),
    #        print (pl_buffer)
    #    else:
    #        print ("Received: Ack only, no payload")
#        time.sleep(1)

