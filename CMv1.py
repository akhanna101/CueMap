import numpy as np
from pygame import *
import pygame, time, numpy, pygame.sndarray
import time as time
import RPi.GPIO as GPIO


global NPs

NPs = ([], [])

#Input output pins for the dipper and nosepoke
dipper = 18
nosePoke = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(nosePoke, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(nosePoke, GPIO.BOTH, callback=IOD, bouncetime=100)
GPIO.setup(dipper, GPIO.OUT) # UPDATE PIN OUT FOR DIPPER
GPIO.output(dipper, 0)

cueTime_ms = 4000
sample_rate = 44100
bits = 16
max_sample = 2**(bits - 1) - 1

pixels = 12

Map = numpy.empty((pixels,2),dtype=object)

def IOD(a):
    
    if GPIO.input(nosePoke):
        print('ON')
        
        NPs[0].append(time.time())
##        tf = open("TT","a")
##        tf.write(str(time.time()) + "   " + "F" + '\n')
##        
    else:
        print('OFF')
        NPs[1].append(time.time())
##        tf = open("TT","a")
##        tf.write(str(time.time()) + "   " + "R" + '\n')
    


def savedata(Event):
    global NPs
    t = time.time()
    tf = open(filename,"a")
    for x in NPs[0]:
        
        tf.write(str(x-st) + "   " + "F" + '\n')
        
    for x in NPs[1]:
        
        tf.write(str(x-st) + "   " + "R" + '\n')
        
    NPs = ([],[])
    
    tf.write(str(t-st) + "   " + Event + '\n')
        
    tf.close()
    
    



def getsin(sample_rate,freq,max_sample):
    length = sample_rate / float(freq)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    f = numpy.int16(max_sample * numpy.sin(xvalues))
    #f = numpy.stack((f, f),axis=1)
    #return (numpy.int16(max_sample * numpy.sin(xvalues)))
    return (numpy.stack((f, f),axis=1))

def getclick(sample_rate,freq,max_sample):
    length = sample_rate / float(freq)
    f = numpy.zeros(int(length),dtype=numpy.int16)
    f[:10] = max_sample
    #f = numpy.stack((f, f),axis=1)
    #return (numpy.int16(max_sample * numpy.sin(xvalues)))
    return (numpy.stack((f, f),axis=1))

def play_for(sample_array_r,sample_array_c, volLeft, volRight):
    soundr = pygame.sndarray.make_sound(sample_array_r)
    soundc = pygame.sndarray.make_sound(sample_array_c)
    #beg = time.time()
    #channelr = pygame.mixer.Channel(0).play(soundr,loops=-1)
    pygame.mixer.Channel(0).play(soundr,loops=-1)
    pygame.mixer.Channel(0).set_volume(0,volRight)
    #channelc = pygame.mixer.Channel(1).play(soundr,loops=-1)
    pygame.mixer.Channel(1).play(soundc,loops=-1)
    #channelc.set_volume(volLeft,0)
    pygame.mixer.Channel(1).set_volume(volLeft,0)
    pygame.mixer.Channel(2).play(soundc,loops=-1)
    #channelc.set_volume(volLeft,0)
    pygame.mixer.Channel(2).set_volume(volLeft,0)
    
    #pygame.time.delay(ms)
    #sound.stop()
    
def trunc_divmod(a, b):
    q = a / b
    q = -int(-q) if q<0 else int(q)
    r = a - b * q
    return q, r

def trajectoryInput():
    animal = input("What animal is this?")
    day = input("What day of training is this?")
    filename = str(animal_) + str(day) + '.txt' # Determine the filename for the traininglist trajectory
    
    with open (filename, 'r') as f:
        training_list = f.readlines()
        #training_list = [x.strip() for x in training_list] 
        #This opens the trajectory list file for that day and turns it into a list
    
    #Find the Rewarded Pixels based on the pixels that fall between % in our training list.
    rewardIndices = []
    for i, elem in enumerate(training_list):
        if '%' in elem:
            rewardIndices.append(i)
    rew = training_list[((rewardIndices[0])+1):rewardIndices[1]]
    rew = list(map(int,Rew))
    
    #Separates trajectory list from reward list and turns it into pos. pos is a list of integers indicating which pixels to play
    pos = training_list[((rewardIndices[1])+1):-1]
    pos = list(map(int, pos))
    
    return (filename, rew, pos)


#This fills the tones first
#start frequency
freq = 400
cfreq = 2
spacing = 4/3
for p in range(pixels):
    Map[p][0] = getsin(sample_rate,freq,max_sample)
    Map[p][1] = getclick(sample_rate,cfreq,max_sample)
    freq = freq*spacing
    cfreq = cfreq*spacing
    
print(Map[3][0].shape)
print(Map[3][0].shape)
pygame.mixer.pre_init(sample_rate, -16, 2) # 44.1kHz, 16-bit signed, stereo
pygame.init()

_running = True

filename, rew, pos = trajectoryInput()

tf = open(filename,"w")
tf.write('START' +'\n')
tf.close()


#pos = [1,2,14,15,27,132,144] # 
volt = [0.8,0.5,0.45,0.42,0.4,0.4,0.4,0.42,0.45,0.5,0.6,0.7]
volc = [1,1,0.99,0.98,0.97,0.95,0.93,0.90,0.87,0.83,0.79,0.74]

st = time.time()

for p in pos:    
    start = time.time()
    c,r = trunc_divmod(p-1,pixels)
    #play_for(numpy.stack((Map[r][0], Map[c][1]),axis=1),4000,0.5,0.5)
    play_for(Map[r][0],Map[c][1],volc[c],volt[r])
    savedata(str(p))
    #play_for(Map[c][1],4000,1,0)
    print(time.time()-start)
    if p in rew:  
        GPIO.output(dipper, 1)
    pygame.time.delay(cueTime_ms)
    GPIO.output(dipper, 0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break
     
savedata("end")      
pygame.quit()    