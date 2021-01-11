import shortestpath
import malicious_controller

import logging
logging.basicConfig(filename='app.log', filemode='a', 
    		format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', 
    		datefmt='%H:%M:%S')
from datetime import datetime
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import csv
import os

#training dataset file
CSV_FILE = 'train_data.csv'

class Monitor(shortestpath.ProjectController):

    def __init__(self, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.fields = {'time':'','datapath':'','in-port':'','eth_src':'','eth_dst':'','out-port':'','total_packets':0,'total_bytes':0,\
         'duration':0, 'priority':0, 'class':0}
        self.train = True


    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                logging.info('register datapath: ' + str(datapath.id))
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                logging.info('unregister datapath: ' + str(datapath.id))
                del self.datapaths[datapath.id]


    def _monitor(self):
        #logging.info('time\tdatapath\tin-port\teth-src\teth-dst\tout-port\ttotal_packets\ttotal_bytes')
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)


    def _request_stats(self, datapath):
        #logging.info("send stats request: " + str(datapath.id))
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath, flags=0, match=parser.OFPMatch(), table_id=0xff, out_port=ofproto.OFPP_NONE)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_NONE)
        datapath.send_msg(req)


    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        #logging.info(body)
        #storing switch table flow entries as training data
        for stat in body:
        	if len(stat.actions) > 0 and stat.actions[0].port != 65533:
	        	self.fields['time'] = datetime.utcnow().strftime('%s')
	        	self.fields['datapath'] = str(ev.msg.datapath.id)
	        	self.fields['in-port'] = str(stat.match.in_port)
	        	self.fields['eth_src'] = str(stat.match.dl_src)
	        	self.fields['eth_dst'] = str(stat.match.dl_dst)
	        	self.fields['out-port'] = str(stat.actions[0].port)
	        	self.fields['total_packets'] = str(stat.packet_count)
	        	self.fields['total_bytes'] = str(stat.byte_count)
	        	self.fields['duration'] = str(stat.duration_sec)
	        	self.fields['priority'] = str(stat.priority)
	        	#0 = normal traffic
	        	self.fields['class'] = str(0)
	        	#1 = malicious traffic
	        	#self.fields['class'] = str(1)

	        	if(self.train):
	        		#logging.info('trainning enabled')
	        		flag = os.path.isfile(CSV_FILE)
	        		with open(CSV_FILE, 'a') as f:
	        			header = list(self.fields.keys())
	        			writer = csv.DictWriter(f, fieldnames=header)
	        			
	        			#writing header if file is being created for first time
	        			if not flag:
	        				writer.writeheader()

	        			logging.info(self.fields)
	        			writer.writerow(self.fields)
	        	else:
	        		return
	        		# ML thingy
