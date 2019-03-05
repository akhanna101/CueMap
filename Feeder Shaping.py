import time as time
import RPi.GPIO as GPIO
import random

nosePokePin = 27
feederPin = 23
global NPs
NPs = ([],[])  

GPIO.setmode(GPIO.BCM)
GPIO.setup(feederPin, GPIO.OUT)
GPIO.output(feederPin,0)

GPIO.setup(nosePokePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

animal = input("What animal is this?")
date = input("What is today's date?")
day = input("What day of training is this?")
filename = str(animal) + '_' + str(date)+ '_' + str(day) + '.txt'

def NosePoke(a):
    if GPIO.input(nosePokePin):
        NPs[0].append('on')
        NPs[1].append(time.time())
    else:
        NPs[0].append('off')
        NPs[1].append(time.time())

GPIO.add_event_detect(nosePokePin, GPIO.BOTH, callback=NosePoke, bouncetime=100)

for i in range(40):
    time.sleep(random.randint(1,3))
    GPIO.output(feederPin,1)
    time.sleep(1)
    GPIO.output(feederPin,0)

pokeData = open(filename,"w")
pokeData.write(NPs)
pokeData.close()

len(NPs[0])
exit()
