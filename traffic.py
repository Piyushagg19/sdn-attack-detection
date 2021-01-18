import random
from mininet.net import Mininet
import sys
import threading, time
from os.path import expanduser
import subprocess
from datetime import datetime

flush = sys.stdout.flush
#log file
LOG_FILE = 'traffic.log'

#traffic generator script - called in abilene_topo.py script
class TrafficGenerator:
	def __init__(self, net):
		self.net = net
		th = threading.Thread(target=self.start)
		th.daemon = True
		th.start()

	# method for background process
	def start(self):
		time.sleep(5)

		while True:
			# selecting distinct src and dst randomly from available hosts
			while True:
				i, j = random.randint(0, 32), random.randint(0, 32)
				if(i != j):
					break


			src, dst = self.net.hosts[i], self.net.hosts[j]
			
			f = open(LOG_FILE, "a+")
			curr_timestamp = datetime.utcnow().strftime('%s')
			f.write(curr_timestamp + " src: " + str(i) + " dst: " + str(j) + "\n")

			# creating server at dst host
			res = dst.popen('iperf -s -u')

			# creating client at src host
			res = src.popen("iperf -f m -c %s -u -b 200m -t 30" % (dst.IP()), stdout=subprocess.PIPE)

			# sleeping for 10 seconds before another run
			time.sleep(10)

			f.close()
			flush()