import math
import time
import machine, neopixel
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = '0.0.0.0'
UDP_PORT = 5006
s.bind((UDP_IP, UDP_PORT))

maxp = 60
np = neopixel.NeoPixel(machine.Pin(4), maxp)

purple=(50,250,0)
yellow=(70,0,110)

def ba2np(ba):
    i=0
    while i<(len(ba)-2):
        np[int(i/3)]=(ba[i],ba[i+1],ba[i+2])
        i=i+3
    np.write()

def udp2ba():
    ba=s.recv(3*maxp)
    #np=ba2np(ba)
    return ba

def udp2np():
    while 1:
        ba=udp2ba()
        #start=time.ticks_ms()
        ba2np(ba)
    #return time.ticks_ms()-start

def sc(r,g,b):
    for x in range(0,maxp):
        np[x]=(r,b,g)
    np.write()

def rainbow(pos):
    p=range(0,maxp)
    n, r, b = 0, 31, 0
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(r,b,int(math.sin(i/50*math.pi)*25))
        np[p[i-pos]]=(r,b,int(math.sin(i/2*maxp/6*math.pi)*maxp/6))
    n, g, b = 1, 31, 0
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(25-int(math.sin(i/50*math.pi)*25),b,g)
        np[p[i-pos]]=(25-int(math.sin(i/2*maxp/6*math.pi)*maxp/6),b,g)
    n, r, g = 2, 0, 31
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(r,int(math.sin(i/50*math.pi)*25),g)
        np[p[i-pos]]=(r,int(math.sin(i/2*maxp/6*math.pi)*maxp/6),g)
    n, r , b = 3, 0, 31
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(r,b,25-int(math.sin(i/50*math.pi)*25))
        np[p[i-pos]]=(r,b,25-int(math.sin(i/2*maxp/6*math.pi)*maxp/6))
    n, g, b = 4, 0, 31
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(int(math.sin(i/50*math.pi)*25),b,g)
        np[p[i-pos]]=(int(math.sin(i/2*maxp/6*math.pi)*maxp/6),b,g)
    n, r, g = 5, 31, 0
    for i in range(int(maxp/6)*n,int(maxp/6)*(n+1)):
        #np[p[i-pos]]=(r,25-int(math.sin(i/50*math.pi)*25),g)
        np[p[i-pos]]=(r,25-int(math.sin(i/2*maxp/6*math.pi)*maxp/6),g)
    np.write()

def twirl():
    i=0
    while 1:
        rainbow(i)
        i=i+1
        if i==maxp:
            i=0
            
def vike():
    i=0
    col=[]
    col.append(yellow)
    col.append(yellow)
    col.append(yellow)
    col.append(yellow)
    col.append(yellow)
    col.append(purple)                                                                                                                                                                                                                                                                                    
    col.append((128,128,128))
    while 1:
        for n in range(0,60):
            np[n]=col[(i+n)%6]
        np.write()
        i=i+1
        time.sleep(0.25)
        if i==7:
            i=0

def spin():
    i=0
    col=[]
    col.append((0,0,128))                                                                                                                           
    col.append((0,128,0))                                                                                                                           
    col.append((128,0,0))                                                                                                                           
    col.append((0,0,128))                                                                                                                           
    col.append((0,128,0))                                                                                                                           
    col.append((128,0,0))                                                                                                                           
    col.append((128,128,128))
    while 1:
        for n in range(0,60):
            np[n]=col[(i+n)%6]
        np.write()
        i=i+1
        if i==7:
            i=0

def blink(delay):
    while 1:
        sc(0,0,0)
        time.sleep(delay)
        sc(128,128,128)
        time.sleep(delay)

def rst():
    machine.reset()

