import pygame
import numpy
import time
import pygame.sndarray


#filename = str()
#file = open(filename, 'w')


amp_start = 0.01
increment = 0.001
amp = amp_start

sample_rate = 44100
bits = 16
max_sample = 2**(bits - 1) - 1

size = (400,400)
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

pixels = 12
Map = numpy.zeros((pixels,2),dtype=object)  
amps = numpy.zeros((pixels,2), dtype = numpy.int16)


#Import functions used to create/play map

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


#Clicker sound value is just max sample @ different frequencies

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
    
for i in range(2):
    for j in range(12):
        current = True 
        print(i)
        print(j)
        while current:
            sound = pygame.sndarray.make_sound(Map[j,i]) 
            pygame.mixer.Channel(0).play(sound,loops=-1)
            time.sleep(0.01)
            if i == 0:
                pygame.mixer.Channel(0).set_volume(0,amps[j][i])
            else:
                pygame.mixer.Channel(0).set_volume(amps[j][i],0)
            for event in pygame.event.get(): 
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                    amps[j][i] = amps[j][i] + increment
                    time.sleep(0.1)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                    amps[j][i] = amps[j][i] - increment
                    time.sleep(0.1)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    time.sleep(0.1)
#                    file.write(str(amps))
                    current = False
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    pygame.quit()
                    file.close()

for event in pygame.event.get():
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.display.quit()
        pygame.quit()
        file.close()
                    

                