import numpy as np
##from pygame import *
import pygame, time, numpy, pygame.sndarray
import time as time
import RPi.GPIO as GPIO
import os
import curses
#a
os.nice = -40

NPs = ([], [])

#Input output pins for the dipper and nosepoke
dipper = 13
nosePoke = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(nosePoke, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def IOD(a):
    if len(NPs[0]) == 0:
        flag = False
    else: 
        flag = True
        
    if GPIO.input(nosePoke):
        if flag and NPs[1][-1] == 'O':
            return
        NPs[1].append('O')
        
    else:
        if flag and NPs[1][-1] == 'I':
            return
        NPs[1].append('I')
    
    NPs[0].append(time.time())
        
        
        
  
GPIO.add_event_detect(nosePoke, GPIO.BOTH, callback=IOD, bouncetime=10)
GPIO.setup(dipper, GPIO.OUT) # UPDATE PIN OUT FOR DIPPER
GPIO.output(dipper, 0)

cueTime_ms = 3000
FeederOn_ms = 500
sample_rate = 44100
bits = 16
max_sample_t = 2**(bits*(0.7) - 1) - 1
max_sample_c = 2**(bits - 1) - 1

pixels = 12

Map = numpy.empty((pixels,2),dtype=object)  
Freq = numpy.zeros((pixels,2),dtype=float)

SAVEFOLDER = 'Run_0519'

def savedata(Event,st):
    global NPs
    t = time.time()
    tf = open(filename,"a")
    for x in range(len(NPs[0])):

        tf.write(str(NPs[0][x]-st) + "   " + NPs[1][x] + '\n')

    NPs = ([],[])
    
    tf.write(str(t-st) + "   " + Event + '\n')
        
    tf.close()
    
#This function makes sure that any file on that day is not overwritten
def checkfilename(filename):

    filenameuse = filename
    n = 0
    while os.path.isfile(filenameuse):
        n += 1
        filenameuse = filename + '_' + str(n)
    return(filenameuse)    



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
    f[:2] = max_sample
    #f = numpy.stack((f, f),axis=1)
    #return (numpy.int16(max_sample * numpy.sin(xvalues)))
    return (numpy.stack((f, f),axis=1))

##def play_for(soundr, soundc, volLeft, volRight,rp,cp,delayc):
##    #pygame.mixer.Channel(1).stop
####    soundr = pygame.sndarray.make_sound(sample_array_r)
####    soundc = pygame.sndarray.make_sound(sample_array_c)
##    #beg = time.time()
##    #channelr = pygame.mixer.Channel(0).play(soundr,loops=-1)
##   
##        if not rp:
##            pygame.mixer.Channel(0).play(soundr,loops=-1)
##            pygame.mixer.Channel(0).set_volume(0,volRight)
##    #channelc = pygame.mixer.Channel(1).play(soundr,loops=-1)
##    #pygame.time.delay(delayc)
##        if not cp:
##            pygame.mixer.Channel(1).stop
##            pygame.time.delay(max(0,delayc))
##            pygame.mixer.Channel(1).play(soundc,loops=-1)
##            pygame.mixer.Channel(1).set_volume(volLeft,0)
##    #channelc.set_volume(volLeft,0)
##        #pygame.mixer.Channel(1).set_volume(volLeft,0)
####    pygame.mixer.Channel(2).play(soundc,loops=-1)
####    #channelc.set_volume(volLeft,0)
####    pygame.mixer.Channel(2).set_volume(volLeft,0)
##    
##    #pygame.time.delay(ms)
##    #sound.stop()

def sound_load(sample_array_r, sample_array_c, volLeft, volRight,rp,cp,delayc,rchan,cchan):
    
   
    soundr = pygame.sndarray.make_sound(sample_array_r)
    soundc = pygame.sndarray.make_sound(sample_array_c)
    #beg = time.time()
  
    if not rp:
        if rchan == 0:    
            pygame.mixer.Channel(2).play(soundr,loops=-1)
            pygame.mixer.Channel(2).set_volume(0,0)
        
            rchan = 2
        else:
            pygame.mixer.Channel(0).play(soundr,loops=-1)
            pygame.mixer.Channel(0).set_volume(0,0)
    
            rchan = 0
            
    if not cp:
        if cchan == 1:      
            pygame.mixer.Channel(3).stop
            pygame.time.delay(max(0,delayc))
            pygame.mixer.Channel(3).play(soundc,loops=-1)
            pygame.mixer.Channel(3).set_volume(0,0)
            cchan = 3
        else:
            pygame.mixer.Channel(1).stop
            pygame.time.delay(max(0,delayc))
            pygame.mixer.Channel(1).play(soundc,loops=-1)
            pygame.mixer.Channel(1).set_volume(0,0)
            cchan = 1
            
    return(rchan,cchan)

def adjust_vol(r_chan,c_chan,volr,volc,nochange_r, nochange_c):
    
    if not nochange_r:
        if r_chan == 0:
            pygame.mixer.Channel(2).set_volume(0,0)
            pygame.mixer.Channel(0).set_volume(volr,0)
        else:
            pygame.mixer.Channel(0).set_volume(0,0)
            pygame.mixer.Channel(2).set_volume(volr,0)
            
    if not nochange_c:
        if c_chan == 1:
            pygame.mixer.Channel(3).set_volume(0,0)
            pygame.mixer.Channel(1).set_volume(volc,0)
        else:
            pygame.mixer.Channel(1).set_volume(0,0)
            pygame.mixer.Channel(3).set_volume(volc,0)        


def trunc_divmod(a, b):
    q = a / b
    q = -int(-q) if q<0 else int(q)
    r = a - b * q
    return q, r

def trajectoryInput():
    animal = input("What animal is this?")
    day = input("What day of training is this?")
    Rew_Batch = input("What batch of rewards is this?")
    
    # allows animals 9-16 to pull trajectories from 1-8:
    route = int(animal)
    if route > 8:
        route %= 8
    
    #this is added to allow for testing...
    if animal == 't' and day == 't':
        filename_save = 'Data/' + SAVEFOLDER + '/Test.txt'
        animal = 1
        day = 1
    else:    
        filename_save = 'Data/' + SAVEFOLDER + '/CM'+str(animal) + '_' + str(day) + '.txt' # Determine the filename for the traininglist trajectory
    
    #check to make sure there isn't a filename already with that name
    filename = checkfilename(filename_save)
    

    filename_in = '/mnt/DataShare/Lists_RW/List_' + str(route) + '_' + str(day) + '.txt' # Determine the filename for the traininglist trajectory

        
    with open (filename_in, 'r') as f:
        training_list = f.readlines()
        #training_list = [x.strip() for x in training_list] 
        #This opens the trajectory list file for that day and turns it into a list

    filename_rew = '/mnt/DataShare/Rew_Lists/Rew_Batch_' + str(Rew_Batch) + '.txt' # Determine the filename for the traininglist trajectory

    with open (filename_rew, 'r') as r:
        rew_list = r.readlines()
    rew = list(map(int, rew_list))
    
#       
#    #Find the Rewarded Pixels based on the pixels that fall between # in our training list.
#    rewardIndices = []
#    for i, elem in enumerate(training_list):
#        if '#' in elem:
#            rewardIndices.append(i)
#    ##The first comment in the text file is the rat number and day, need to skip to the second line 
#    rew = training_list[((rewardIndices[1])+1):rewardIndices[2]]
#    rew = list(map(int,rew))
    
    #Separates vertices list from reward list and turns it into pos. pos is a list of integers indicating which pixels to play
    Vertices_Index =  training_list.index('##Vertices\n')                         
    pos = training_list[((Vertices_Index)+1):-1]
    pos = list(map(int, pos))
     
    return (filename_save, rew, pos)


def Get_Volumes():
    filename_vol = 'Volumes.txt' # Determine the filename for the traininglist trajectory
    amp = 0.2;
    
    with open (filename_vol, 'r') as fv:
        vols = fv.readlines()
    
    volt = [None]*12
    volc = [None]*12
    
    
    for i,line in enumerate(vols):
        if not '%' in line:
            if i < 12:
                volt[i] = float(line)
            else:
                volc[i-12] = float(line)
                #print(i)
            
           
    return (volt,volc)

def main(stdscr):

    #This sets the parameters for curses
    stdscr.nodelay(True)
    stdscr.clear
    stdscr.keypad(True)
    stdscr.idlok(1)
    stdscr.scrollok(1)

    
    #This fills the tones first
    #start frequency
    freq = 800
    cfreq = 2
    spacing = 1.3
    for p in range(pixels):
        Freq[p][0] = 1000*(1/freq)
        Freq[p][1] = 1000*(1/cfreq)
        Map[p][0] = getsin(sample_rate,freq,max_sample_t)
        Map[p][1] = getclick(sample_rate,cfreq,max_sample_c)
        freq = freq*spacing
        cfreq = cfreq*spacing
        
    #print(Map[3][0].shape)
    #print(Map[3][0].shape)
    pygame.mixer.pre_init(sample_rate, -bits, 2) # 44.1kHz, 16-bit signed, stereo
    pygame.init()
    #sc_size = (200,200)
    #display_surf = pygame.display.set_mode(sc_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    _running = True

##    filename, rew, pos = trajectoryInput()
##    print(rew)

    tf = open(filename,"w")
    tf.write('Reward Zones: ' + str(rew) +'\n')
    tf.close()

    stdscr.addstr("Reward Zones:" + str(rew))
    stdscr.addch('\n')
            
    #This gets the volume file for each tone and click
    volt,volc = Get_Volumes()
    ##volt = [0.8,0.5,0.45,0.42,0.4,0.4,0.4,0.42,0.45,0.5,0.6,0.7]
    ##volc = [1,1,0.99,0.98,0.97,0.95,0.93,0.90,0.87,0.83,0.79,0.74]


    offset = 0
    rp = -1
    cp = -1

    #these set what channels are currently being used
    rchan = 0
    cchan = 1

    #This loads the sound onto a set of channels

    c,r = trunc_divmod(pos[0]-1,pixels)
    ##soundr = pygame.sndarray.make_sound(Map[r][0])
    ##soundc = pygame.sndarray.make_sound(Map[c][1])
    ##play_for(soundr,soundc,volc[c],volt[r],rp == r, cp == c,int(Freq[c][1] - offset))

    rchan,cchan = sound_load(Map[r][0], Map[c][1], volt[r], volc[c],rp == r,cp == c,int(Freq[c][1] - offset),rchan,cchan)

    ##delay start of the session, but not for testing
    if not('Data/' + SAVEFOLDER + '/Test.txt' == filename):
        pygame.time.delay(120000)
        
    st = time.time()

    endprog = False

    for p in range(len(pos)):    
        start = time.time()
        
##        stdscr.addstr(str(pos[p]))
##        stdscr.addch('\n')
        savedata(str(pos[p]),st)
        adjust_vol(rchan,cchan,volt[r],volc[c],rp == r, cp == c)

        _,offset = trunc_divmod(cueTime_ms,Freq[c][1])
        #print(r,c)
        #print(time.time()-start)
        if pos[p]-1 in rew:
            GPIO.output(dipper, 1)
            savedata('F',st)
            stdscr.addstr("pellet")
            stdscr.addch('\n')
            
            pygame.time.delay(FeederOn_ms)
            GPIO.output(dipper, 0)

        char = stdscr.getch()

        if char == ord('x'):
            endprog = True
            savedata('USER ENDED PROGRAM',st)
            stdscr.addstr("user ended program")
            stdscr.addch('\n')
            break
                    
##        for event in pygame.event.get():
##
##            if event.type == pygame.QUIT:
##                _running = False
##                endprog = True
##                savedata('USER ENDED PROGRAM')
##                print("user ended program")
##                break
##                
##            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
##                endprog = True
##                savedata('USER ENDED PROGRAM')
##                print("user ended program")
##                break
##
##        print('tone:',r,' click:',c,' position:',p)
        stdscr.addstr('tone: %s, click: %s, vertex: %s, position: %s' % (r,c,pos[p]-1,p))
        stdscr.addch('\n')
            
        cp = c
        rp = r
        #this gets the next position
        if not p + 1 == len(pos):
            c,r = trunc_divmod(pos[p+1]-1,pixels)
            rchan,cchan = sound_load(Map[r][0], Map[c][1], volt[r], volc[c],rp == r,cp == c,int(Freq[c][1] - offset),rchan,cchan)

        if endprog:
            break
##        stdscr.addstr(cueTime_ms - int(1000*(time.time() - start)))
##        stdscr.addch('\n') 
        pygame.time.delay(cueTime_ms - int(1000*(time.time() - start)))
        #print(time.time() - start)    
    savedata("end",st)      
    pygame.quit()
    stdscr.keypad(False)

filename, rew, pos = trajectoryInput()
print(rew)

curses.wrapper(main)

###############################
##The following code backs the data up to a shared network folder
##if not (filename == 'Data/' + SAVEFOLDER + '/Test.txt'):

import shutil


    #dest = "/media/pi/STORE N GO"
dest = "/mnt/DataShare/"# + SaveFolder
shutil.copy(filename, dest)
