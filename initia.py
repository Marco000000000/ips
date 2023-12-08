import RPi.GPIO as GPIO
import calendar
import time
import os
import display
import led


if __name__ == "__main__":
    led.rosso('ON')
    led.giallo('ON')
    led.verde('ON')
    time.sleep(5)
    led.rosso('OFF')
    led.giallo('OFF')
    led.verde('OFF')
    while True:
        display.scrivi("    IPS","","http://10.0.0.1","","")
    