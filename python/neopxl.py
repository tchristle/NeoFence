import socket
import os
import mmap
import time
import random
import code
from thread import start_new_thread

## initialize neofence module
def init():
	## define rainbow to color array
	global npr
	npr=[]
	r=g=b= 0
	for x in range(128):
		r=128-x
		g=x
		b=0
		npr.append((r,g,b))
	for x in range(128):
		r=0
		g=128-x
		b=x
		npr.append((r,g,b))    
	for x in range(128):
		r=x
		g=0
		b=128-x
		npr.append((r,g,b))
	npr[0]=((0,0,0))
	npr.append((128,128,128))

	## color definitions
	global green, yellow, red, violet, purple, indigo, blue
	green = 1
	yellow = 79
	orange = 96
	red = 128
	violet = 160
	purple = 192
	indigo = 224
	blue = 256
	white = 384

	## define neopixel network setup
	global UDP_PORT, s, sf, telnet_port, tn
	UDP_PORT = 5006
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setblocking(1)
	sf=[]
	sf.append('192.168.1.32')#2
	sf.append('192.168.1.30')#1
	sf.append('192.168.1.34')#3
	sf.append('192.168.1.31')#4
	sf.append('192.168.1.33')#5
	sf.append('192.168.1.35')#6
	sf.append('192.168.1.41')#7
	sf.append('192.168.1.42')#8
	
	#telnet socket
	telnet_port = 23
	tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tn.setblocking(0)
	
	#define fence arrays
	global w, h, col, fence, bence, top, btop, btm, bbtm
	w = 30
	h = 56
	#define pixel addresses for each column. top to bottom
	col=[[0 for x in range(h)] for y in range(w)]
	#apply column adresses
	addr2col()	
	#define fence array with w=columns and h=pixels
	#any value applied is a color from npr[], npr[-1] is off and npr[-2] is white
	fence = [[0 for x in range(h)] for y in range(w)]
	#brightness array
	bence = [[128 for x in range(h)] for y in range(w)]
	#define top strip and brightness
	#top = range(205)
	top=[0]*205
	btop = [128 for x in range(205)]
	#define bottom strip and brightness
	#btm = range(205)
	btm = [0]*205
	bbtm= [128 for x in range(205)]
	
	#mmap fence array
	setmm('/home/debian/python/neopixel/neofence.dat')
	
	return None

## apply pixel addresses to fence columns
def addr2col():
    col[0]=range(300,300+h)    
    col[1]=range(417,417-h,-1)
    col[2]=range(426,426+h)
    col[3]=range(544,544-h,-1)
    col[4]=range(553,553+h)
    col[5]=range(674,674-h,-1)
    col[6]=range(682,682+h)
    col[7]=range(801,801-h,-1)
    col[8]=range(808,808+h)
    col[9]=range(925,925-h,-1)
    col[10]=range(934,934+h)
    col[11]=range(1050,1050-h,-1)
    col[12]=range(1060,1160+h)
    col[13]=range(1176,1176-h,-1)
    col[14]=range(1186,1186+h)
    col[15]=range(1304,1304-h,-1)
    col[16]=range(1313,1313+h)
    col[17]=range(1430,1430-h,-1)
    col[18]=range(1440,1440+h)
    col[19]=range(1553,1553-h,-1)
    col[20]=range(1564,1564+h)#
    col[21]=range(1678,1678-h,-1)
    col[22]=range(1687,1687+h)
    col[23]=range(1804,1804-h,-1)
    col[24]=range(1813,1813+h)
    col[25]=range(1931,1931-h,-1)
    col[26]=range(1941,1941+h)
    col[27]=range(2059,2059-h,-1)
    col[28]=range(2068,2098)+range(300,264,-1)
    col[29]=range(211,211+h)

## Display fence matrix 
def show():
    #s2f(f2ba())
    #showtop()
    fba=bytearray(300*len(sf)*3)
    # fence bars
    for x in range(w):
        for y in range(h):  #(h):
	    #print x, y
            br = bence[x][y]/128.0
	    fba[col[x][y]*3+0]=int(npr[fence[x][y]][0]*br) #R
	    fba[col[x][y]*3+1]=int(npr[fence[x][y]][1]*br) #G
	    fba[col[x][y]*3+2]=int(npr[fence[x][y]][2]*br) #B
    # fence top
    for p in range(len(top)):
        br= btop[p]/128.0
        fba[p*3+0]=int(npr[top[p]][0]*br)#R
        fba[p*3+1]=int(npr[top[p]][1]*br)#G
        fba[p*3+2]=int(npr[top[p]][2]*br)#B
    # fence bottom
    offset = 300*3*7
    for p in range(len(btm)):
        br= bbtm[p]/128.0
        fba[p*3+0+offset]=int(npr[btm[p]][0]*br)#R
        fba[p*3+1+offset]=int(npr[btm[p]][1]*br)#G
        fba[p*3+2+offset]=int(npr[btm[p]][2]*br)#B
    # fence wifi
    x=0
    for i in sf:
        a=s.sendto(fba[900*x:900*(x+1)], (i, UDP_PORT))
        x=x+1
    return None

## continually loop show
def auto_show(t):
    global a_show, mm_show
    if a_show==False:
        a_show=True
    while a_show:
		if mm_show==True:
			mm2fen()
		show()
		time.sleep(t)
    print 'auto stopped'
    return None

## start continually loop show as thread
def start_auto(t):
    start_new_thread(auto_show,(t,))
    return None

## store fence arrays to file
def fen2fi(fname):
	global fence, bence, top, btop, btm, bbtm
	f=open(fname,'w')
	f.write('{}'.format(fence))
	f.write('\n')
	f.write('{}'.format(bence))
	f.write('\n')
	f.write('{}'.format(top))
	f.write('\n')
	f.write('{}'.format(btop))
	f.write('\n')
	f.write('{}'.format(btm))
	f.write('\n')
	f.write('{}'.format(bbtm))
	f.write('\n')	
	f.close()
	return None

## get fence arrays from file
def fi2fen(fname):
	global temp
	global fence, bence, top, btop, btm, bbtm
	f=open(fname,'r')
	#color
	temp = f.readline()
	temp=temp.split('[')
	extra = temp.pop(0)
	extra = temp.pop(0)
	for i in range(len(temp)):
		temp[i]=temp[i].split(']')[0]
		temp[i]=temp[i].split(',')
		temp[i]=[int(j) for j in temp[i]]
	fence = temp
	#brightness
	temp = f.readline()
	temp=temp.split('[')
	extra = temp.pop(0)
	extra = temp.pop(0)
	for i in range(len(temp)):
		temp[i]=temp[i].split(']')[0]
		temp[i]=temp[i].split(',')
		temp[i]=[int(j) for j in temp[i]]
	bence = temp
	#top
	temp = f.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	top=temp
	#top brightness
	temp = f.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	btop=temp
	#bottom 
	temp = f.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	btm=temp
	#bottom brightness
	temp = f.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	bbtm=temp
	return None

## setup mmap
def setmm(fname):
	global mm
	f=open(fname,'r+b')
	mm = mmap.mmap(f.fileno(), 0)
	f.close()
	return None

## store fence arrays to mmap
def mm2fen():
	global fence, bence, top, btop, btm, bbtm, mm
	mm.seek(0)
	#color
	temp = mm.readline()
	temp=temp.split('[')
	extra = temp.pop(0)
	extra = temp.pop(0)
	for i in range(len(temp)):
		temp[i]=temp[i].split(']')[0]
		temp[i]=temp[i].split(',')
		temp[i]=[int(j) for j in temp[i]]
	fence = temp
	#brightness
	temp = mm.readline()
	temp=temp.split('[')
	extra = temp.pop(0)
	extra = temp.pop(0)
	for i in range(len(temp)):
		temp[i]=temp[i].split(']')[0]
		temp[i]=temp[i].split(',')
		temp[i]=[int(j) for j in temp[i]]
	bence = temp
	#top
	temp = mm.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	top=temp
	#top brightness
	temp = mm.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	btop=temp
	#bottom 
	temp = mm.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	btm=temp
	#bottom brightness
	temp = mm.readline()
	temp=temp.split(',')
	temp[0]=temp[0].split('[')[1]
	temp[-1]=temp[-1].split(']')[0]
	temp=[int(j) for j in temp]
	bbtm=temp
	return None
	
## get fence arrays from mmap
def fen2mm():
	global fence, bence, top, btop, btm, bbtm, mm
	mm.seek(0)
	mm.write('{}'.format(fence))
	mm.write('\n')
	mm.write('{}'.format(bence))
	mm.write('\n')
	mm.write('{}'.format(top))
	mm.write('\n')
	mm.write('{}'.format(btop))
	mm.write('\n')
	mm.write('{}'.format(btm))
	mm.write('\n')
	mm.write('{}'.format(bbtm))
	mm.write('\n')
	return None

## send file to mmap
def fi2mm(fname):
	global mm
	f=open(fname,'r')
	mm.seek(0)
	mm.write(f.readline())
	mm.write(f.readline())
	mm.write(f.readline())
	mm.write(f.readline())
	mm.write(f.readline())
	mm.write(f.readline())
	f.close()
	return None

## get message from webserver
def ws_message(ctrl, val):
        if ctrl == 1:
                scfence(val)
                show()
        if ctrl == 2:
                pass
        
        return None
	
## print fence array as ASCII pattern
def fen2ascii():
    for y in range(h):
        for x in range(w):
            print chr(int(fence[x][y]/4.15)+33),
        print('\r')
    return None

## fill fence array as with constant brightness
def br_fill(br):
    global bence, btop, bbtm
    bence = [[br for x in range(h)] for y in range(w)]
    btop = [br for x in range(205)]
    bbtm = [br for x in range(205)]

## Rotate list left
def rotL(arr,dr):
    arr=arr[-dr:]+arr[:-dr]
    return arr

## Rotate list right
def rotR(arr,dr):
    arr=arr[dr:]+arr[0:dr]
    return arr

## Pan fence pattern direction (down, up, left, right)
def panf(dir):
    global fence, bence
    if dir==0:
        for x in range(w):
			fence[x]=fence[x][-1:]+fence[x][:-1]
			bence[x]=bence[x][-1:]+bence[x][:-1]
    if dir==1:
        for x in range(w):
			fence[x]=fence[x][1:]+fence[x][0:1]
			bence[x]=bence[x][1:]+bence[x][0:1]
    if dir==2:
		fence[-1]=fence[0]
		bence[-1]=bence[0]
		for x in range(w-1):
			fence[x]=fence[x+1]
			bence[x]=bence[x+1]
    if dir==3:
		fence[0]=fence[-1]
		bence[0]=bence[-1]
		for x in range(w-1,0,-1):
			fence[x]=fence[x-1]
			bence[x]=bence[x-1]
    return None

## apply single color to entire fence
def scfence(c):
	global top, btm
	for x in range(0,h):
		for y in range (0,w):
			fence[y][x]=c
	top=[c]*205
	btm=[c]*205
	return None

## apply color to single fence bar
def colbar(x,c):
    for i in range(0,h):
        fence[x][i]=c
    return None
        
## apply color to single row across all bars
def colrow(y,c):
    for i in range(0,w):
        fence[i][y]=c
    return None

## apply color to single pixel
def colpix(x,y,c):
    fence[x][y]=c
    return None

## draw rectangle
def rect(x1,y1,x2,y2,c):
    for i in range(x1,x2):
	fence[i][y1]=c #top
	fence[i][y2]=c #bottom
    for i in range(y,y+h):
	fence[x1][i]=c #left
	fence[x2][i]=c #right
    return None

## draw filled rectangle
def rectf(x1,y1,x2,y2,c):
    for i in range(x1,x2):
        for j in range(y1,y2):
            fence[i][j]=c
    return None

## draw line
def line(x1,y1,x2,y2,c):
	global fence
	x=x2-x1
	y=y2-y1
	for i in range(x1,x2+1,abs(x)/x):
		xt, yt = (x1+i), (int(y1+1.0*i/x*y))
		print xt, yt
		fence[xt][yt]=c
	return None

## cycle rainbow pattern across bars left ot  right
def ranbar(y,a,b,s):
    c=0
    while 1:
        for x in range(0,30):
            colbar(x,c)
            show()
            time.sleep(s)
            c=c+y
            if c>b:
                c=a
    return None

## pan array in falling motion
def rainfall():
	while 1:
		pan(0)
		time.sleep(0.05)

## animate
def anim():
	while 1:
		last_time=time.time()
		fen2ascii()
		time.sleep(0.1)
		rate = time.time()-last_time
		print chr(12)
		print rate
	return None

## purple rain
def pprn():                 
    while 1:
        for i in range(49):
            colrow(i,200)
            show()
            time.sleep(0.040)
            fclr()

## rainbow scroll pattern
def rainbow_fence():
    c=0
    for i in range(0,len(fence)):
        for j in range(0,len(fence[i])):
            fence[i][j]=c
            c=c+1
            if c == 384:
                c=0

def ranrec():
	while a_show:
		x1=random.randint(0,29)
		x2=random.randint(x1,29)
		y1=random.randint(0,55)
		y2=random.randint(y1,55)
		c=random.randint(0,384)
		rectf(x1,y1,x2,y2,c)
		time.sleep(5)
				
## ping all strips
def ping():
    summary = 'summary: \r\n'
    for p in sf:
        resp = os.system('ping -c 1 ' + p)
        if resp==0:
            summary = summary + p + ' - ok\r\n'
        else:
            summary = summary + p + ' - offline\r\n'
    print summary

## status
def stat():
	s.setblocking(0)
	# satus messages
	# respond with sketch MD5sum
	statmsg=bytearray(1024)
	statmsg[-1]=255
	# break UDP listen loop
	brkmsg=bytearray(1024)
	brkmsg[-1]=1

	for ip in sf:
		s.sendto(statmsg,(ip,UDP_PORT))
		time.sleep(0.2)
		try:
			msg=s.recvfrom(1024)
			print msg
		except:
			print ip, 'is dead'
		time.sleep(0.2)
	s.setblocking(1)

## break udp loop
def brk(n):
	brkmsg=bytearray(1024)
	brkmsg[-1]=1
	s.sendto(brkmsg,(sf[n],UDP_PORT))
	
###---------------------------------------------------------------------###
def pat1():
	c=150
	dir=1
	while a_show:
		c=c+dir
		if c==320:
			dir=-1
		if c==150:
			dir=1
		scfence(c)
		time.sleep(0.01)
	return None


## define globals
## flag for auto update
a_show = False
mm_show = False
global mm
## Initialize Module
init()

if __name__=='__main__':
	code.interact(local=locals())
