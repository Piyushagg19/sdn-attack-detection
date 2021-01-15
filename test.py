from dbscan import Model
import pandas as pd

model = Model()
rec = {"time" : "1610450294", "datapath": "2", "in-port": "4", "eth_src": "b'\x00\x00\x00\x00\x00\x00'", "eth_dst": "b'\x00\x00\x00\x00\x00\x08'", \
	"out-port": "2", "total_packets": "200841", "total_bytes": "303671592", "duration": "12", "priority": "32768", "out-port-1": "[1, 2]", \
	"out-port-2": "[4, 9]", "out-port-3": "[4, 9]", "out-port-4": "[7]", "out-port-5": "[1]", "out-port-6": "[2]", "class": "0"}

df = pd.read_csv('./training data/training_data_pos.csv')

#df = pd.DataFrame(rec, index=[0])
df = df[100:200]
df = model.preprocess(df)
res = model.predict(df)
print('records : ' + str(df))
print('response from model : ' + str(res))