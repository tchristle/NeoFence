import noepxl as n
import select
from evdev import InputDevice, categorize, ecodes
gpad=InputDevice('/dev/input/event0')

def jpad():
    color=0
    while 1:
        r,w,x=select.select([gpad],[],[],0)
        if r:
            for event in gpad.read():
                if event.code==305:
                    print 'A = ',event.value
                    if event.value==1:
                        A()
                if event.code==306:
                    print 'B = ',event.value
                    if event.value==1:
                        B()
                if event.code==304:
                    print 'X = ',event.value
                    if event.value==1:
                        X()
                if event.code==307:
                    print 'Y = ',event.value
                    if event.value==1:
                        Y()
                if event.code==17:
                    print 'U/D = ',event.value
                    #UD()
                if event.code==16:
                    print 'L/R = ',event.value
                    #LR()
                if event.code==308:
                    print 'TL = ',event.value
                    LT()
                if event.code==309:
                    print 'TR = ',event.value
                    RT()

def A():
    pass    
def B():
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
