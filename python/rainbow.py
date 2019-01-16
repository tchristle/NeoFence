import numpy as np
import math

c = np.arange(0,128)
ncosi = 64+64*np.cos(c*np.pi/127)
cosi = 64+64*np.cos(c*np.pi/127-np.pi)
high=np.ones(128)*128
low=np.zeros(128)

r = g = b = np.zeros(128*6)
###r = g = b = []
##N=128
##n=0
##a=n*N
##z=(n+1)*N-1
##r[a:z]=high #- \ _ _ / -
##print a,z,r
##g[a:z]=cosi #/ - - \ _ _
##b[a:z]=low  #_ _ / - - \
##n=1
##a=n*N
##z=(n+1)*N-1
##r[a:z]=ncosi#
##print a,z,r
##g[n*N:(n+1)*N-1]=high #
##b[n*N:(n+1)*N-1]=low  #
##n=2
##r[n*N:(n+1)*N-1]=low  #
##g[n*N:(n+1)*N-1]=high #
##b[n*N:(n+1)*N-1]=cosi #
##n=3
##r[n*N:(n+1)*N-1]=low  #
##g[n*N:(n+1)*N-1]=ncosi#
##b[n*N:(n+1)*N-1]=high #
##n=4
##r[n*N:(n+1)*N-1]=cosi #
##g[n*N:(n+1)*N-1]=low  #
##b[n*N:(n+1)*N-1]=high #
##n=5
##r[n*N:(n+1)*N-1]=high #
##g[n*N:(n+1)*N-1]=low  #
##b[n*N:(n+1)*N-1]=ncosi#
##
##R=G=B=[]
##for i in range(0,768):
##    R.append(int(r[i]))
##    G.append(int(g[i]))
##    B.append(int(b[i]))

npr=[]
r=0
b=0
g=0
for i in range(0,128):
    r=128
    #print r
    g=cosi[i]
    #print g
    b=0
    #print b
    npr.append((r,g,b))
    print i, npr[i]
for i in range(128,256):
    r=ncosi[i-128]
    g=128
    b=0
    npr.append((r,g,b))
    print i, npr[i]
for i in range(256,384):
    r=0
    g=128
    b=cosi[i-256]
    npr.append((r,g,b))
    print i, npr[i]
for i in range(384,512):
    r=0
    g=ncosi[i-384]
    b=128
    npr.append((r,g,b))
    print i, npr[i]
for i in range(512,640):
    r=cosi[i-512]
    g=0
    b=128
    npr.append((r,g,b))
    print i, npr[i]
for i in range(640,768):
    r=128
    g=0
    b=ncosi[i-640]
    npr.append((r,g,b))
    print i, npr[i]

