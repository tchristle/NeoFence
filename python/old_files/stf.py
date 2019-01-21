import time
import neopxl as n
import code
n.scfence(0)
sba1=bytearray(5400)
sba1[0:2]=(128,128,128)
'''
while 1:
    try:
        start=time.time()
        n.s2f(sba1)
        print time.time()-start
        sba1=n.rotL(sba1)
        time.sleep(0.1)
    except KeyboardInterrupt:
        code.interact( local=locals() )
'''

x=0
while 1:
    n.scfence(x)
    x=x+1
    print x
    if x==767:
        x=0
    time.sleep(0.010)
