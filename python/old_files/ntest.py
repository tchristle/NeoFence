import time
import neopxl as n
import code
n.scfence(0)
n.colpix(1,1,1)
code.interact(local=locals())

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

