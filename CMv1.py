
from pygame import *
import pygame, time, numpy, pygame.sndarray

sample_rate = 44100
bits = 16
max_sample = 2**(bits - 1) - 1

pixels = 12

Map = numpy.empty((pixels,2),dtype=object)

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

def play_for(sample_array_r,sample_array_c, ms, volLeft, volRight):
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
    
    pygame.time.delay(ms)
    #sound.stop()
    
def trunc_divmod(a, b):
    q = a / b
    q = -int(-q) if q<0 else int(q)
    r = a - b * q
    return q, r


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

pos = [1,2,14,15,27,132,144]
volt = [0.8,0.5,0.45,0.42,0.4,0.4,0.4,0.42,0.45,0.5,0.6,0.7]
volc = [1,1,0.99,0.98,0.97,0.95,0.93,0.90,0.87,0.83,0.79,0.74]

n = 0
#while _running:
for p in pos:    
    start = time.time()
    c,r = trunc_divmod(p-1,12)
    #play_for(numpy.stack((Map[r][0], Map[c][1]),axis=1),4000,0.5,0.5)
    play_for(Map[r][0],Map[c][1],4000,volc[c],volt[r])
    #play_for(Map[c][1],4000,1,0)
    print(time.time()-start)
    #n = n+1
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break
        
pygame.quit()    