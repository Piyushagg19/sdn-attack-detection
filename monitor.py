'''
ryu-manager --ofp-tcp-listen-port 6633 --observe-links monitor.py ryu.app.ofctl_rest
'''

import shortestpath
from dbscan import Model as DBSCAN
#from ann import Model as ANN
#from inspector import Inspector
from loghandler import Logger

from datetime import datetime
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.mac import haddr_to_bin
import pandas as pd
import csv
import os
from ryu import cfg

#training dataset file
CSV_FILE = 'train_data.csv'
log = Logger().getlogger()

class Monitor(shortestpath.ProjectController):

    def __init__(self, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.fields = {'time':'','datapath':'','in-port':'','eth_src':'','eth_dst':'','out-port':'','total_packets':0,'total_bytes':0,\
         'duration':0, 'priority':0, 'out-port-1':[], 'out-port-2':[], 'out-port-3':[], 'out-port-4':[], 'out-port-5':[], 'out-port-6':[], 'class':0}

        #self.inspector = Inspector()

        # reading config params from provided conf file
        CONF = cfg.CONF
        CONF.register_opts([
        	cfg.StrOpt('train', default='false'),
        	cfg.StrOpt('model', default='ann')])
        
        log.info('training param :' + str(CONF.train))
        
        log.info('model param : ' + str(CONF.model))

        # setting network state vars based on provided flags and values
        if(CONF.train == 'false'):
        	self.train = False
        else:
        	self.train = True

        if(CONF.model == 'ann'):
        	self.model = ANN()
        elif(CONF.model == 'dbscan'):
        	self.model = DBSCAN()
        else:
        	self.model = None


    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                log.info('register datapath: ' + str(datapath.id))
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                log.info('unregister datapath: ' + str(datapath.id))
                del self.datapaths[datapath.id]


    def _monitor(self):
        #log.info('time\tdatapath\tin-port\teth-src\teth-dst\tout-port\ttotal_packets\ttotal_bytes')
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)


    def _request_stats(self, datapath):
        #log.info("send stats request: " + str(datapath.id))
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath, flags=0, match=parser.OFPMatch(), table_id=0xff, out_port=ofproto.OFPP_NONE)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_NONE)
        datapath.send_msg(req)


    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        #log.info(body)
        #storing switch table flow entries as training data
        for stat in body:
        	if len(stat.actions) > 0 and stat.actions[0].port != 65533:
	        	self.fields['time'] = datetime.utcnow().strftime('%s')
	        	self.fields['datapath'] = str(ev.msg.datapath.id)
	        	self.fields['in-port'] = str(stat.match.in_port)
	        	self.fields['eth_src'] = stat.match.dl_src
	        	self.fields['eth_dst'] = stat.match.dl_dst
	        	self.fields['out-port'] = str(stat.actions[0].port)
	        	self.fields['total_packets'] = str(stat.packet_count)
	        	self.fields['total_bytes'] = str(stat.byte_count)
	        	self.fields['duration'] = str(stat.duration_sec)
	        	self.fields['priority'] = str(stat.priority)
	        	self.fields['out-port-1'] = []
	        	self.fields['out-port-2'] = []
	        	self.fields['out-port-3'] = []
	        	self.fields['out-port-4'] = []
	        	self.fields['out-port-5'] = []
	        	self.fields['out-port-6'] = []
	        	#0 = normal traffic
	        	self.fields['class'] = str(0)
	        	#1 = malicious traffic
	        	#self.fields['class'] = str(1)

	        	#getting out-edges for switch
	        	out_edges = list(self.net.out_edges(ev.msg.datapath.id, data=True))
	        	#log.info('out-edges : ' + str(out_edges))

	        	for e in out_edges:
	        		if e[2] and 'port' in e[2] and 'weight' in e[2]:
	        			fld = 'out-port-' + str(e[2]['port'])
	        			self.fields[fld].append(e[2]['weight'])

	        	if(self.train):
	        		# log.info('trainning enabled')
	        		flag = os.path.isfile(CSV_FILE)
	        		with open(CSV_FILE, 'a') as f:
	        			header = list(self.fields.keys())
	        			writer = csv.DictWriter(f, fieldnames=header)
	        			
	        			# writing header if file is being created for first time
	        			if not flag:
	        				writer.writeheader()

	        			log.info(self.fields)
	        			writer.writerow(self.fields)
	        	else:

	        		# chaging data type to match training data
	        		self.fields['out-port-1'] = str(self.fields['out-port-1'])
	        		self.fields['out-port-2'] = str(self.fields['out-port-2'])
	        		self.fields['out-port-3'] = str(self.fields['out-port-3'])
	        		self.fields['out-port-4'] = str(self.fields['out-port-4'])
	        		self.fields['out-port-5'] = str(self.fields['out-port-5'])
	        		self.fields['out-port-6'] = str(self.fields['out-port-6'])

	        		# predicting class of record with model
	        		df = pd.DataFrame(self.fields, index=[0])
	        		df = self.model.preprocess(df)
	        		res = self.model.predict(df)

	        		log.info('records : \n' + str(df))
	        		log.info('response from model : ' + str(res))

	        		# back verifying the record if its classified as malicious
	        		# if(len(res) > 0 and res[0] == -1):
	        		# 	self.inspector.verify(self.fields)


