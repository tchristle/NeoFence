#!/usr/bin/env python
import time
import socket
UDP_PORT = 5006
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)

def brk(n):
	s.sendto(brkmsg,(sf[n],UDP_PORT))
	return None

sf=[]
sf.append('192.168.1.32')#1
sf.append('192.168.1.30')#2
sf.append('192.168.1.34')#3
sf.append('192.168.1.31')#4
sf.append('192.168.1.33')#5
sf.append('192.168.1.35')#6
sf.append('192.168.1.41')#7
sf.append('192.168.1.42')#8

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
