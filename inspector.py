from loghandler import Logger

import os
import networkx as nx

LOG_FILE = 'traffic.log'
NETWORK_STATE_PATH = 'network_state'
log = Logger().getlogger(__name__)

class Inspector:
	# def __init__(self):
	# 	# init method

	# main method to verify if provided entry is malicious or not
	def verify(self, record):
		try:
			min_entry = self.get_entry_with_min_diff(record)
			log.info('entry to verify : ' + str(min_entry))
			if min_entry != None:
				network_state = self.get_network_state(int(min_entry[0]))
				if network_state != None:
					log.info('loading network from : ' + str(network_state))
					net = nx.read_gexf(NETWORK_STATE_PATH + "/" + network_state)
					src = min_entry[2]
					dst = min_entry[4]
					log.info("checking for source : " + str(src) + " & destination : " + str(dst))
					path = nx.shortest_path(net, src, dst)
					log.info('path : ' + str(path))
		except Exception as e:
			log.error(e)


	# method to fetch appropriate network state based on provided time instance
	def get_network_state(self, t):
		file_list = os.listdir(NETWORK_STATE_PATH)
		file_list.sort(reverse=True)
		res = None
		for file in file_list:
			ft = int(file.split(".")[0])
			if ft <= t:
				res = file
				break

		return res

	# method to fetch appropriate packet route based on provided time instance
	def get_entry_with_min_diff(self, record):
		#log.info('checking for time : ' + str(record['time']))
		logs = self.reverse_readline(LOG_FILE)
		min_diff = float('inf')
		min_entry = None
		for entry in logs:
			entry = entry.split(" ")
			#log.info('checking : ' + str(entry[0]))
			diff = abs(int(entry[0]) - int(record['time']))
			if diff < min_diff:
				min_entry = entry
				min_diff = diff
			else:
				break

		return min_entry

	# A generator that returns the lines of a file in reverse order
	def reverse_readline(self, filename, buf_size=8192):
		with open(filename) as fh:
			segment = None
			offset = 0
			fh.seek(0, os.SEEK_END)
			file_size = remaining_size = fh.tell()
			while remaining_size > 0:
				offset = min(file_size, offset + buf_size)
				fh.seek(file_size - offset)
				buffer = fh.read(min(remaining_size, buf_size))
				remaining_size -= buf_size
				lines = buffer.split('\n')
				# The first line of the buffer is probably not a complete line so
				# we'll save it and append it to the last line of the next buffer
				# we read
				if segment is not None:
					# If the previous chunk starts right from the beginning of line
					# do not concat the segment to the last line of new chunk.
					# Instead, yield the segment first 
					if buffer[-1] != '\n':
						lines[-1] += segment
					else:
						yield segment
				segment = lines[0]
				for index in range(len(lines) - 1, 0, -1):
					if lines[index]:
						yield lines[index]
			# Don't yield None if the file was empty
			if segment is not None:
				yield segment
