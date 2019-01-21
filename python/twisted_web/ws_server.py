import sys
sys.path.insert(0, '../')
import code
import neopxl as npx

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

		msg=payload.decode('utf8')
		try:
                        msg=payload.decode('utf8')
			msg=msg.split('#')
			ctrl = int(msg[-2])
			val = int(msg[-1])
			npx.ws_message(ctrl, val)
		except:
			pass
        
	def onClose(self, wasClean, code, reason):
		print("WebSocket connection closed: {0}".format(reason))

if __name__ == "__main__":
	log.startLogging(sys.stdout)

	# static file server seving index.html as root
	root = File(".")

	factory = WebSocketServerFactory(u"ws://0.0.0.0:8081")
	factory.protocol = SomeServerProtocol
	resource = WebSocketResource(factory)
	# websockets resource on "/ws" path
	root.putChild(u"ws", resource)

	site = Site(root)
	reactor.listenTCP(8080, site)
	reactor.listenTCP(8081, factory)
	reactor.run()
	
