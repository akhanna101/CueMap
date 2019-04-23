import pygame
import numpy
import time
import pygame.sndarray
import curses

#filename = str()
#file = open(filename, 'w')


amp_start = 0.2
increment = 0.02

amp = amp_start

sample_rate = 44100
bits = 16
max_sample_t = 2**((bits*(0.7)) - 1) - 1
max_sample_c = 2**((bits) - 1) - 1

size = (400,400)
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

pixels = 12
Map = numpy.zeros((pixels,2),dtype=object)
Freq = numpy.zeros((pixels,2),dtype=float)
amps = numpy.zeros((pixels,2), dtype = numpy.float)
amps[:,0] = amp
amps[:,1] = amp


#Import functions used to create/play map

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
                print(i)
                print(line)
            else:
                volc[i-12] = float(line)
                print(i)
            
    print(volc)
    print(volt)
    return (volt,volc)


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

def main():
    stdscr.nodelay(True)
    stdscr.clear
    stdscr.keypad(True)
    stdscr.idlok(1)
    stdscr.scrollok(1)
    
    #Clicker sound value is just max sample @ different frequencies

    #This fills the tones first
    #start frequency
    freq = 800 #400
    cfreq = 2
    spacing = 4/3

    volt, volc = Get_Volumes()
    amps[:,0] = volt
    amps[:,1] = volc

    for p in range(pixels):
        Freq[p][0] = freq
        Freq[p][1] = cfreq
        Map[p][0] = getsin(sample_rate,freq,max_sample_t)
        Map[p][1] = getclick(sample_rate,cfreq,max_sample_c)
        freq = freq*spacing
        cfreq = cfreq*spacing

    for i in range(2):
        for j in range(12):
            current = True
            stdscr.addstr(str(i) + ', ' + str(j))
            stdscr.addch('\n')
##            print(i)
##            print(j)
            sound = pygame.sndarray.make_sound(Map[j,i]) 
            pygame.mixer.Channel(0).play(sound,loops=-1)
            
            if i == 0:
                pygame.mixer.Channel(0).set_volume(0,amps[j][i])
                #print(Freq[j][0])
                stdscr.addstr(str(Freq[j][0]))
                stdscr.addch('\n')
            else:
                pygame.mixer.Channel(0).set_volume(amps[j][i],0)
                #print(Freq[j][1])
                stdscr.addstr(str(Freq[j][1]))
                stdscr.addch('\n')
            while current:
    ##            sound = pygame.sndarray.make_sound(Map[j,i]) 
    ##            pygame.mixer.Channel(0).play(sound,loops=-1)
                time.sleep(0.01)
                if i == 0:
                    pygame.mixer.Channel(0).set_volume(0,amps[j][i])
                else:
                    pygame.mixer.Channel(0).set_volume(amps[j][i],0)
                
                char = stdscr.getch()
                
                if char == curses.KEY_UP:
                    amps[j][i] = amps[j][i] + increment
                    #print(amps[j][i])
                    stdscr.addstr(str(amps[j][i]))
                    stdscr.addch('\n')
                    time.sleep(0.1)
                
                elif char == curses.KEY_DOWN:
                    amps[j][i] = amps[j][i] - increment
                    stdscr.addstr(str(amps[j][i]))
                    stdscr.addch('\n')
                    time.sleep(0.1)
                    
                elif char == curses.RETURN:
                    time.sleep(0.1)
    #               file.write(str(amps))
                    current = False
                
                elif char == curses.ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    file.close()
                    
##                for event in pygame.event.get(): 
##                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
##                        amps[j][i] = amps[j][i] + increment
##                        print(amps[j][i])
##                        time.sleep(0.1)
##                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
##                        amps[j][i] = amps[j][i] - increment
##                        print(amps[j][i])
##                        time.sleep(0.1)
##                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
##                        time.sleep(0.1)
##    #                    file.write(str(amps))
##                        current = False
##                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
##                        pygame.display.quit()
##                        pygame.quit()
##                        file.close()


    tone_click_volumes = amps.flatten(order='F')
    #volumes = open('Volumes.txt', 'w')
    numpy.savetxt('Volumes.txt', tone_click_volumes)

    pygame.mixer.Channel(0).stop
    pygame.display.quit()
    pygame.quit()
    stdscr.keypad(False)

curses.wrapper(main)
                    

                