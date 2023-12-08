import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
except:
    print("Mode already in a different setting")
GPIO.setwarnings(False)
#red
GPIO.setup(12, GPIO.OUT)
#green
GPIO.setup(16, GPIO.OUT)
#yellow
GPIO.setup(18, GPIO.OUT)


def rosso(func):
    if func == 'ON':
        GPIO.output(12,True)
    else:
        GPIO.output(12,False)
        
def verde(func):
    if func == 'ON':
        GPIO.output(16,True)
    else:
        GPIO.output(16,False)
        

def giallo(func):
    if func == 'ON':
        GPIO.output(18,True)
    else:
        GPIO.output(18,False)