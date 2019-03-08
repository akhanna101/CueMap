import time as time
import RPi.GPIO as GPIO
import random

nosePokePin = 22
feederPin = 23
global NPs
#NPs = ([],[])  
NPs = [];

GPIO.setmode(GPIO.BCM)
GPIO.setup(feederPin, GPIO.OUT)
GPIO.output(feederPin,0)

GPIO.setup(nosePokePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

animal = input("What animal is this?")
date = input("What is today's date?")
day = input("What day of training is this?")
filename = 'Data/Mag_Training/' + str(animal) + '_' + str(date)+ '_' + str(day) + '.txt'

def NosePoke(a):
    if GPIO.input(nosePokePin):
        NPs.append('on' + '   ' + str(time.time() - st))
    else:
        NPs.append('off' + '   ' + str(time.time() - st))


GPIO.add_event_detect(nosePokePin, GPIO.BOTH, callback=NosePoke, bouncetime=10)

def savedata():
    global NPs
    tf = open(filename,"w")
    for x in NPs:
        tf.write(x + '\n')
        
    tf.close

st = time.time()

for i in range(40):
    time.sleep(random.randint(60,180))
    GPIO.output(feederPin,1)
    time.sleep(0.5)
    GPIO.output(feederPin,0)

savedata()

