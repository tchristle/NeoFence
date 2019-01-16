sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
#print('waiting for connection')
#while not sta_if.isconnected():
#	pass
#ip_addr = sta_if.ifconfig()[0]
#print('connected. IP: ' + ip_addr)

import neop
neop.udp2np()
