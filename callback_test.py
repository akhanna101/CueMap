import time as time
import RPi.GPIO as GPIO


tf = open("TT","w")
tf.write('START' +'\n')
tf.close()

global NPs

NPs = ([], [])


GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(4, GPIO.BOTH)

def IOD(a):
    
    if GPIO.input(4):
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
    
GPIO.add_event_callback(4, IOD)

def savedata(Event):
    global NPs
    t = time.time()
    tf = open("TT","a")
    for x in NPs[0]:
        
        tf.write(str(x-st) + "   " + "F" + '\n')
        
    for x in NPs[1]:
        
        tf.write(str(x-st) + "   " + "R" + '\n')
        
    NPs = ([],[])
    
    tf.write(str(t-st) + "   " + Event + '\n')
        
    tf.close()
    
    
st = time.time()

while True:
    time.sleep(10)
    savedata(str(1))

    
    a = 1
    