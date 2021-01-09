import random
from mininet.net import Mininet
import sys
import threading, time
from os.path import expanduser
import subprocess

flush = sys.stdout.flush

class TrafficGenerator:
	def __init__(self, net):
		self.net = net
		th = threading.Thread(target=self.start)
		th.daemon = True
		th.start()


	def start(self):
		time.sleep(5)
		file_path = "/home/abhi/acn/project/log.txt"
		while True:
			while True:
				src, dst = random.randint(0, 32), random.randint(0, 32)
				if(src != dst):
					break

			src, dst = self.net.hosts[src], self.net.hosts[dst]
			
			f = open(file_path, "a+")
			f.write("testing between " + str(src.name) + " ---> " + str(dst.name) + "\n")
			res = dst.popen('iperf -s -u')
			#f.write(str(res) + "\n")

			res = src.popen("iperf -f m -c %s -u -b 200m -t 30" % (dst.IP()), stdout=subprocess.PIPE)
			#f.write(str(res) + "\n")
			time.sleep(20)
			f.close()
			#src.cmd('telnet', dst.IP(), '5001')
			#serverbw, clientbw = self.net.iperf([src, dst], seconds=5)
			flush()