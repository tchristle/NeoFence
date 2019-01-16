import socket
import time
#import matplotlib.pyplot as plt
import numpy as np
import select
from evdev import InputDevice, categorize, ecodes

#gpad=InputDevice('/dev/input/event0')
RockLamp='192.168.1.24'

def np2ba(np):
    ba=bytearray()
    for i in np:
        for j in i:
            ba.append(chr(j))
    return ba

def rotL(arr):
    arr=arr[-3:]+arr[:-3]
    return arr
    
def blink():
    while 1:
        a=s.sendto(zba, ('192.168.1.24', UDP_PORT))
        time.sleep(0.1)
        a=s.sendto(bigba, ('192.168.1.24', UDP_PORT))
        time.sleep(0.1)
	
def on():
    s.sendto(bigba, ('192.168.1.24', UDP_PORT))

def off():
    a=s.sendto(zba, ('192.168.1.24', UDP_PORT))

def twirl(n):
    i=0
    while 1:
        a=s.sendto(bar[i:i+180], (UDP_IP, UDP_PORT))
        i=i+n
        if i > 765:
            i=-768
        time.sleep(0.100)

def fill(r, g, b):
    npa=[]
    for i in range(0,60):
        npa.append((r,g,b))
    a=s.sendto(np2ba(npa), (UDP_IP, UDP_PORT))

def rotfill(delay):
    color=0
    while 1:
        fill(nprs[color][0],nprs[color][1],nprs[color][2])
        time.sleep(delay)
        color=color+1
        if color == 256:
            color=0

def fade2red(delay):
    offset = 60
    redba=bar[768-offset:768]+bar[0:180-offset]
    while 1:
        a=s.sendto(redba, ('192.168.1.24', UDP_PORT))
        time.sleep(delay)
        redba=rotL(redba)

def fade180(delay, offset):
    redba=bar[768-offset:768]+bar[0:180-offset]
    while 1:
        a=s.sendto(redba, ('192.168.1.24', UDP_PORT))
        time.sleep(delay)
        redba=rotL(redba)

def fade2(c1, c2, delay):
    cba=bar[768-c1:768]+bar[0:c2]
    while 1:
        a=s.sendto(cba, ('192.168.1.24', UDP_PORT))
        time.sleep(delay)
        cba=rotL(cba)

def fill2(color):
    fill(nprs[color][0],nprs[color][1],nprs[color][2])



def jpad():
    color=0
    while 1:
        r,w,x=select.select([gpad],[],[],0)
        if r:
            for event in gpad.read():
                if event.code==305:
                    print 'A = ',event.value, 'color = ', color
                    if event.value==1:
                        color=color+3
                        fill2(color)	
                    #A()
                if event.code==306:
                    print 'B = ',event.value, 'color = ', color
                    if event.value==1:
                        color=color-3
                        fill2(color)
                    #B()
                if event.code==304:
                    #X()
                    print 'X = ',event.value
                if event.code==307:
                    #Y()
                    print 'Y = ',event.value
                if event.code==17:
                    #UD()
                    print 'U/D = ',event.value
                if event.code==16:
                    #LR()
                    print 'L/R = ',event.value
                if event.code==308:
                    #LT()
                    print 'TL = ',event.value
                if event.code==309:
                    #RT()
                    print 'TR = ',event.value

def A():
    r,w,x=select.select([gpad],[],[],0)
    while not r:
        #gpad.read()
        time.sleep(0.1)
    print 'a'
    pass	
def B():
    r,w,x=select.select([gpad],[],[],0)
    while not r:
        #gpad.read()
        time.sleep(0.1)
    print 'b'
    pass
def X():
    pass
def Y():
    pass	
def UD():
    pass
def LR():
    pass
def LT():
    pass
def RT():
    pass


###---------------------------------------------------------------------###    

#ba = np2ba(arr)
#s.sendto(ba, (UDP_IP, UDP_PORT))

bigba=bytearray(180)
zba=bytearray(180)
for i in range(0,180):
	bigba[i]=chr(128)

c = np.arange(0,128)
ncosi = 64+64*np.cos(c*np.pi/127)
cosi = 64+64*np.cos(c*np.pi/127-np.pi)
high=np.ones(128)*128
low=np.zeros(128)
#plt.plot(c,cosi)
#plt.show()

UDP_IP = '192.168.1.24'
UDP_PORT = 5006
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

npr=[]
r=g=b = 0
for i in range(0,128):
    r=128
    g=int(cosi[i])
    b=0
    npr.append((r,g,b))
    #print i, npr[i]
for i in range(128,256):
    r=int(ncosi[i-128])
    g=128
    b=0
    npr.append((r,g,b))
    #print i, npr[i]
for i in range(256,384):
    r=0
    g=128
    b=int(cosi[i-256])
    npr.append((r,g,b))
    #print i, npr[i]
for i in range(384,512):
    r=0
    g=int(ncosi[i-384])
    b=128
    npr.append((r,g,b))
    #print i, npr[i]
for i in range(512,640):
    r=int(cosi[i-512])
    g=0
    b=128
    npr.append((r,g,b))
    #print i, npr[i]
for i in range(640,768):
    r=128
    g=0
    b=int(ncosi[i-640])
    npr.append((r,g,b))
    #print i, npr[i]
#npr.append((128,128,128))
#npr.append((0,0,0))
red=0
orange = 127
green = 255
yellow = 383
blue = 511
indigo = 639


nprs=[]
for x in range(0,768,3):
    nprs.append(npr[x])

bar = np2ba(nprs)

color=42
fill(nprs[color][0],nprs[color][1],nprs[color][2])

