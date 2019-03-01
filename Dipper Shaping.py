# Shaping Script
#Make this operant. Need to use addeventdetect to get a list of NPs, then control the dipper based on NPs.

import time as time
import RPi.GPIO as GPIO


#NPs = ([], [])
nosePokePin = 11
dipperPin = 23
maxRewards = 50
dipperDelay = 5
timeEnd = 1800

GPIO.setmode(GPIO.BCM)

GPIO.setup(dipperPin, GPIO.OUT) 
GPIO.output(dipperPin, 1)

GPIO.setup(nosePokePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(noesPokePin, GPIO.FALLING, callback=dipperUp, bouncetime=100)

st = time.time()
st2 = st

def dipperUp():
    time.delay(dipperDelay)
    GPIO.output(dipperPin, 0)
    GPIO.output(dipperPin, 1)
   

running = True
n=0
while running:
    if GPIO.event_detected(nosePokePin):
        dipperUp()
        n = n+1
    if n > maxRewards or time.time() > timeEnd:
        running = False
    if time.time() - st2 > 60:
        print n 
        print time.time()
        st2 = time.time()
    time.sleep(0.0005)
print n 
print time.time()
