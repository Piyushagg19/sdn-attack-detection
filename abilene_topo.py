from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from traffic import TrafficGenerator
import threading

switches = []
hosts = []
class AbileneTopo(Topo):

	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		
		# switches = []
		# hosts = []

		for s in range(11):
			switches.append(self.addSwitch('s%s' % (s + 1)))
			
		for h in range(33):
			hosts.append(self.addHost('h%s' % (h + 1)))
			
		for s in range(11):
			self.addLink(switches[s], switches[(s + 1) % 11])
		
		self.addLink(switches[1], switches[10])
		self.addLink(switches[3], switches[9])
		self.addLink(switches[4], switches[8])
		
		hi = 0
		si = 0
		while(hi < 33 and si < 11):
			self.addLink(hosts[hi], switches[si])
			hi += 1
			self.addLink(hosts[hi], switches[si])
			hi += 1
			self.addLink(hosts[hi], switches[si])
			hi += 1
			si += 1


if __name__ == '__main__':

	# c0 = RemoteController('c0', port = 6633)
	# c1 = RemoteController('c1', port = 6634)
	# c2 = RemoteController('c2', port = 6635)

	# cmap = {'s1' : c0, 's2' : c0, 's3' : c1, 's4' : c1, 's5' : c2, 's6' : c2, 's7' : c2, 's8' : c2, 's9' : c2, 's10' : c1, 's11' : c0}

	# class MultiSwitch(OVSSwitch):
	# 	def start(self, controllers):
	#  		return OVSSwitch.start(self, [cmap[self.name]])

	setLogLevel('info')
	topo = AbileneTopo()
	net = Mininet(topo = topo, controller=None, autoStaticArp=True, autoSetMacs=True)
	trafficGen = TrafficGenerator(net)

	c0 = net.addController(name='ryucontroller0', controller=RemoteController, ip='127.0.0.1', port=6633)
	net.start()
	CLI(net)
	net.stop()