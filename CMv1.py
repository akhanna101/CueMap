import numpy as np
##from pygame import *
import pygame, time, numpy, pygame.sndarray
import time as time
import RPi.GPIO as GPIO
import os
os.nice = -10
global NPs

NPs = ([], [])

#Input output pins for the dipper and nosepoke
dipper = 23
nosePoke = 22

#this sets the pins for plexon events
strobe = 4
videoTTL = 2
plx_word = [5,6,12,13,15,17,24,25]
npout = 27
rstart = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(nosePoke, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#this dictionary keeps track of the different list folders
ListFolders = {
    0: 'Random Walk Only',
    1: 'Trajectories Only',
    2: 'Random Jump Only',
    3: 'RW and Traj',
    4: 'RW and RJ',
    }

ListTrackTypes = ['RW', 'Traj', 'RJ', 'RW+Traj', 'RW+RJ']

#ListTypes

def IOD(a):
    NPs[0].append(time.time())
    
    if GPIO.input(nosePoke):
        NPs[1].append('I')
        GPIO.output(npout, True)
    else:
        NPs[1].append('O')
        GPIO.output(npout, False)
  
GPIO.add_event_detect(nosePoke, GPIO.BOTH, callback=IOD, bouncetime=10)
GPIO.setup(dipper, GPIO.OUT) 
GPIO.output(dipper, 0)

GPIO.setup(strobe, GPIO.OUT)
GPIO.output(strobe, 0)
#Below is setup for video TTL 
GPIO.setup(videoTTL, GPIO.OUT)
GPIO.output(videoTTL, 0)

GPIO.setup(npout, GPIO.OUT)
GPIO.output(npout, 0)

GPIO.setup(rstart, GPIO.OUT)
GPIO.output(rstart, 1)

for i in range(8):
    GPIO.setup(plx_word[i], GPIO.OUT)
    GPIO.output(plx_word[i], 0)

    

cueTime_ms = 3000
FeederOn_ms = 500
sample_rate = 44100
bits = 16
max_sample_t = 2**(bits*(0.7) - 1) - 1
max_sample_c = 2**(bits - 1) - 1

pixels = 12

Map = numpy.empty((pixels,2),dtype=object)  
Freq = numpy.zeros((pixels,2),dtype=float)

def savedata(Event):
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

def  getlistfilename(day,route,ListFolder,ListTrackTypes):
    #fiirst determine which list the current rat is on
    f = open('Lists/ExperimentLists.txt','r') 
  
    rlist = f.readlines()
        #This loops through each line
    for line in rlist:
        sep = line.split(",")
            #check whether the day matches the first value in the line
        if str(day) == sep[0]:
                #second value is the list number and the third input is the list type
            listnum = sep[1]
            listtype = sep[2]
                
            for li,LTT in enumerate(ListTrackTypes):
                if listtype == LTT + '\n':
                    listfile = 'Lists/' + ListFolders.get(li) +'/List_' + str(route) + '_' + str(day) + '.txt' # Determine the filename for the traininglist trajectory
                    break      
            break
    f.close()     
    return(listfile)

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


def send_plx_word(vertex):

    #check to make this faster
    for i in range(8):
        GPIO.output(plx_word[i], bool(vertex & (1<<i)))
    #to keep the code faster, the strobe will be sent at a different time then the bit setting,
        #so the following lines are commented out
##    GPIO.output(strobe, True)    
##    time.sleep(0.0001)
##    GPIO.output(strobe, False)  



def trajectoryInput():
    animal = input("What animal is this?")
    day = input("What day of training is this?") 
    Rew_Batch = input("What batch of rewards is this?")
    
##    # allows animals 9-16 to pull trajectories from 1-8:
##    if animal != 't':
##        route = int(animal)
##        if route > 8:
##            route %= 8
        
    #this is added to allow for testing...
    if animal == 't' and day == 't':
        filename_save = 'Data/Run_0319/Test.txt'
        route = 1
        day = 1
        listtype = 1 
        
    else:
        route = int(animal)
        if route >8:
            route %= 8
        filename_save = 'Data/Run_0319/CM'+str(animal) + '_' + str(day) + '.txt' # Determine the filename for the traininglist trajectory
        
    
    #check to make sure there isn't a filename already with that name
    filename = checkfilename(filename_save)
    
    
    filename_in = getlistfilename(day,route,ListFolders,ListTrackTypes)

        
    with open (filename_in, 'r') as f:
        training_list = f.readlines()
        #training_list = [x.strip() for x in training_list] 
        #This opens the trajectory list file for that day and turns it into a list
    
    filename_rew = 'Lists/Rew_Batch_' + str(Rew_Batch) + '.txt'
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
sc_size = (200,200)
display_surf = pygame.display.set_mode(sc_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

_running = True

filename, rew, pos = trajectoryInput()
print(rew)

tf = open(filename,"w")
tf.write('Reward Zones: ' + str(rew) +'\n')
tf.close()

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

#This gets the buffer ready to send to Plexon
send_plx_word(pos[0]-1)

##delay start of the session, but not for testing
if not('Data/Run_0319/Test.txt' == filename):
    pygame.time.delay(120000)
    
st = time.time()

endprog = False

for p in range(len(pos)):    
    start = time.time()
    
    #print(p)
    #print(pos[p])
    #print(c*12+r)
    #play_for(numpy.stack((Map[r][0], Map[c][1]),axis=1),4000,0.5,0.5)
    savedata(str(pos[p]))
    GPIO.output(strobe, True) 
    GPIO.output(videoTTL, True) 
    adjust_vol(rchan,cchan,volt[r],volc[c],rp == r, cp == c)
    #play_for(soundr,soundc,volc[c],volt[r],rp == r, cp == c,int(Freq[c][1] - offset))
    #start = time.time()
    _,offset = trunc_divmod(cueTime_ms,Freq[c][1])
    GPIO.output(strobe, False) 
    GPIO.output(videoTTL, False)
    #print(r,c)
    #play_for(Map[c][1],4000,1,0)
    #print(time.time()-start)
    if pos[p] in rew:
        GPIO.output(dipper, 1)
        savedata('F')
        print('pellet')
        
        pygame.time.delay(FeederOn_ms)
        GPIO.output(dipper, 0)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            _running = False
            endprog = True
            savedata('USER ENDED PROGRAM')
            print("user ended program")
            break
            
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            endprog = True
            savedata('USER ENDED PROGRAM')
            print("user ended program")
            break

    print('tone:',r,' click:',c,' position:',p)
    
    cp = c
    rp = r
    #this gets the next position
    if not p + 1 == len(pos):
        c,r = trunc_divmod(pos[p+1]-1,pixels)

        #This gets the sound buffer ready for the next position
        rchan,cchan = sound_load(Map[r][0], Map[c][1], volt[r], volc[c],rp == r,cp == c,int(Freq[c][1] - offset),rchan,cchan)
##        soundr = pygame.sndarray.make_sound(Map[r][0])
##        soundc = pygame.sndarray.make_sound(Map[c][1])
        #time.sleep(cueTime_ms/1000 - .001*(time.time() - start))

        #This sets the output but word for Plexon for the next position. The strobe channel sends this buffer.
        send_plx_word(pos[p+1]-1)
        
    if endprog:
        break
    pygame.time.delay(cueTime_ms - int(1000*(time.time() - start)))
    #print(time.time() - start)    
savedata("end")      
pygame.quit()    

GPIO.output(rstart, 0)

###############################
##The following code backs the data up to a USB Drive
import shutil

dest = "/media/pi/STORE N GO"

shutil.copy(filename, dest)
