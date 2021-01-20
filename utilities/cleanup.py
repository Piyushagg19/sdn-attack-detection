import pandas as pd

data = pd.read_csv('train_data.csv')
vdata = pd.read_csv('attack_logs.csv')

count = 0
for indx, row in vdata.iterrows():
	vtime = row['time']
	vdpid = row['datapath']
	vin_port = row['in-port']
	vaction = row['action']
	vout_port = row['out-port']

	if vaction == []:
		continue

	fltrd = data.loc[(data['time'] >= vtime - 15) & (data['time'] <= vtime + 15) & (data['datapath'] == vdpid) & (data['in-port'] == vin_port) & (data['out-port'] == vout_port)]
	count += len(fltrd)
	for i, r in fltrd.iterrows():
		print('updating' + str(i))
		data.at[i, 'class'] = 1

print(count)
data.to_csv('train_data.csv', index=False)