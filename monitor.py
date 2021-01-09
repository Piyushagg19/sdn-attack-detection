import shortestpath

import logging
from datetime import datetime
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

class Monitor(shortestpath.ProjectController):

    def __init__(self, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.fields = {'time':'','datapath':'','in-port':'','eth_src':'','eth_dst':'','out-port':'','total_packets':0,'total_bytes':0}
        logging.basicConfig(filename='log.txt', filemode='a', 
    		format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', 
    		datefmt='%H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger('urbanGUI')


    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]


    def _monitor(self):
        print('time\tdatapath\tin-port\teth-src\teth-dst\tout-port\ttotal_packets\ttotal_bytes')
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)


    def _request_stats(self, datapath):
        print("send stats request: %016x", datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath, flags=0, match=parser.OFPMatch(), table_id=0xff, out_port=ofproto.OFPP_NONE)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_NONE)
        datapath.send_msg(req)


    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        print(body)
        # for stat in sorted([flow for flow in body if flow.priority == 1],
        #                    key=lambda flow: (flow.match['in_port'],
        #                                      flow.match['eth_dst'])):
        #     #print details of flows
        #     self.fields['time'] = datetime.utcnow().strftime('%s')
        #     self.fields['datapath'] = ev.msg.datapath.id
        #     self.fields['in-port'] = stat.match['in_port']
        #     self.fields['eth_src'] = stat.match['eth_src']
        #     self.fields['eth_dst'] = stat.match['eth_dst']
        #     self.fields['out-port'] = stat.instructions[0].actions[0].port
        #     self.fields['total_packets'] = stat.packet_count
        #     self.fields['total_bytes'] = stat.byte_count

        #     print("data\t%s\t%x\t%x\t%s\t%s\t%x\t%d\t%d",self.fields['time'],self.fields['datapath'],self.fields['in-port'],self.fields['eth_src'],self.fields['eth_dst'],self.fields['out-port'],self.fields['total_packets'],self.fields['total_bytes'])
