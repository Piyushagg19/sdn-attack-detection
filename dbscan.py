from sklearn.cluster import DBSCAN
import sklearn.utils
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle

import matplotlib.pyplot as plt
import numpy as np


class Model:
	def __init__(self):
		self.model = DBSCAN(eps=3.0, min_samples=25)

	def preprocess(self, df):
		
		#assigning weights based on out-port
		for indx, r in df.iterrows():
			weight_col = 'out-port-' + str(df.loc[indx, 'out-port'])
			weights = df.loc[indx, weight_col][1:-1]
			weights = weights.split(",")
			l = []
			for w in weights:
				if w != '':
					l.append(int(w))

			df.loc[indx, 'weight'] = max(l, default=10)

		# label encoding dst mac addresses
		df = df[['in-port', 'eth_dst', 'out-port', 'total_packets', 'total_bytes', 'duration', 'weight']]
		ll = LabelEncoder()
		df['eth_dst'] = ll.fit_transform(df['eth_dst'])

		# normalizing data
		ss = StandardScaler()
		cols = ['total_packets', 'total_bytes', 'duration']
		scaled_values = ss.fit_transform(df[cols].values)
		df[cols] = scaled_values
		
		return df

	def predict(self, df):
		print('inside predict')
		res = self.model.fit(df)
		self.res = res
		self.labels = res.labels_


if __name__ == "__main__":
	print("inside")
	obj = Model()
	df = pd.read_csv('./training data/training_data_pos.csv')
	N = df.shape[0]
	i = 0
	while (i < N):
		temp_df = df[i : min(N, i + 50000)]
		i += 50000
		temp_df = obj.preprocess(temp_df)
		obj.predict(temp_df)
		n_clusters = len(set(obj.labels)) - (1 if -1 in obj.labels else 0)
		print('clusters : ' + str(n_clusters))
		n_outliers = list(obj.labels).count(-1)
		print('outliers : ' + str(n_outliers))
	
	filename = 'trained_dbscan.sav'
	pickle.dump(obj.model, open(filename, 'wb'))
