import sys
sys.path.insert(0, '../')
import code
import neopxl as npx

#import socket
#UDP_IP = "192.168.1.15"
#UDP_PORT = 5005

def sUDP(msg):
    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(msg, (UDP_IP, UDP_PORT))
    sock.close()


import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class SomeServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("some request connected {}".format(request))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.sendMessage("message received")
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)
        #sUDP(payload.decode('utf8'))
        clr=payload.decode('utf8')
        #code.interact(local=locals())
        #clr = clr.split(' ')
        #print clr[-1]
        try:
            clr=int(clr.split('#')[1])
            npx.scfence(clr)
        except:
            pass
        
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File(".")

    factory = WebSocketServerFactory(u"ws://0.0.0.0:8080")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()

