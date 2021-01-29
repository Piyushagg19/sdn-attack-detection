import threading
import pyshark
import sys
from datetime import datetime
flush = sys.stdout.flush

FILE_DIR = './logs/'


class TrafficCapture:
    def __init__(self, net):
        self.net = net
        self.threads = []
        self.files = {}
        for s in self.net.switches:
            for interface in s.nameToIntf.keys():
                if interface != 'lo':
                    th = threading.Thread(target=self.start, args=(interface,), daemon=True)
                    self.threads.append(th)
                    self.files[interface] = open(FILE_DIR + interface + ".log", 'w+')
                    th.start()

    def start(self, interface):
        capture = pyshark.LiveCapture(interface=interface, bpf_filter='udp')
        for pkt in capture.sniff_continuously():
            # print(pkt)
            self.files[interface].write(str(pkt.sniff_time) + " " + str(pkt.eth.get('src')) + " " + str(pkt.eth.get('dst')) + "\n")
            # flush()
