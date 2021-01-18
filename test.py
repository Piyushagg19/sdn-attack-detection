from dbscan import Model
import pandas as pd
import os

# model = Model()
# rec = {"time" : "1610450294", "datapath": "2", "in-port": "4", "eth_src": "b'\x00\x00\x00\x00\x00\x00'", "eth_dst": "b'\x00\x00\x00\x00\x00\x08'", \
# 	"out-port": "2", "total_packets": "200841", "total_bytes": "303671592", "duration": "12", "priority": "32768", "out-port-1": "[1, 2]", \
# 	"out-port-2": "[4, 9]", "out-port-3": "[4, 9]", "out-port-4": "[7]", "out-port-5": "[1]", "out-port-6": "[2]", "class": "0"}

# df = pd.read_csv('./training data/training_data_pos.csv')

# #df = pd.DataFrame(rec, index=[0])
# df = df[100:200]
# df = model.preprocess(df)
# res = model.predict(df)
# print('records : ' + str(df))
# print('response from model : ' + str(res))
print(os.listdir('configs/'))

# def reverse_readline(filename, buf_size=8192):
# 	"""A generator that returns the lines of a file in reverse order"""
# 	with open(filename) as fh:
# 		segment = None
# 		offset = 0
# 		fh.seek(0, os.SEEK_END)
# 		file_size = remaining_size = fh.tell()
# 		while remaining_size > 0:
# 			offset = min(file_size, offset + buf_size)
# 			fh.seek(file_size - offset)
# 			buffer = fh.read(min(remaining_size, buf_size))
# 			remaining_size -= buf_size
# 			lines = buffer.split('\n')
# 			# The first line of the buffer is probably not a complete line so
# 			# we'll save it and append it to the last line of the next buffer
# 			# we read
# 			if segment is not None:
# 				# If the previous chunk starts right from the beginning of line
# 				# do not concat the segment to the last line of new chunk.
# 				# Instead, yield the segment first 
# 				if buffer[-1] != '\n':
# 					lines[-1] += segment
# 				else:
# 					yield segment
# 			segment = lines[0]
# 			for index in range(len(lines) - 1, 0, -1):
# 				if lines[index]:
# 					yield lines[index]
# 		# Don't yield None if the file was empty
# 		if segment is not None:
# 			yield segment


# for line in reverse_readline('traffic.log'):
# 	print(line)