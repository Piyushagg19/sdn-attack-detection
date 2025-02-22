from sklearn.cluster import KMeans
import sklearn.utils
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle

import matplotlib.pyplot as plt
import numpy as np
from os import path

MODEL_FILE = 'trained_Kmeans.pkl'
LL_FILE = 'trained_ll.pkl'
SS_FILE = 'trained_ss.pkl'

class Model:
	def __init__(self):
		# self.model = pickle.load(open(MODEL_FILE, 'rb'))
		# print("params : " + str(self.model.get_params()))
		# kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42, }
		self.model = KMeans(init="random", n_clusters=4, n_init=10, max_iter=300, random_state=42)
		
		self.ll = LabelEncoder()
		if path.exists(LL_FILE):
			self.ll = pickle.load(open(LL_FILE, 'rb'))

		self.ss = StandardScaler()
		if path.exists(SS_FILE):
			self.ss = pickle.load(open(SS_FILE, 'rb'))

	def preprocess(self, df):
		
		#assigning weights based on out-port
		for indx, r in df.iterrows():
			weight_col = 'out-port-' + str(df.loc[indx, 'out-port'])
			weights = df.loc[indx, weight_col][1:-1]
			weights = weights.split(",")
			l = []
			for w in weights:
				if w != '':
					l.append(int(w.strip()))

			df.loc[indx, 'weight'] = max(l, default=10)

		df.drop(columns=['out-port-1', 'out-port-2', 'out-port-3', 'out-port-4', 'out-port-5', 'out-port-6'], inplace=True)

		# normalizing data
		cols = ['total_packets', 'total_bytes', 'duration', 'weight']
		scaled_values = self.ss.fit_transform(df[cols].values)
		df[cols] = scaled_values
		
		return df

	def fit(self, df):
		print('inside fit')
		res = self.model.fit(df)
		self.res = res
		self.labels = res.labels_

	def predict(self, df):
		return self.model.fit_predict(df)


if __name__ == "__main__":
	print("inside")
	obj = Model()
	df = pd.read_csv('../training data/training_data_pos.csv')
	df.drop(columns=['time', 'eth_src', 'eth_dst', 'priority', 'class'], inplace=True)
	#df = obj.preprocess(df)
	print(df.columns)
	N = df.shape[0]
	i = 0
	while (i < N):
		temp_df = df[i : min(N, i + 50000)]
		i += 50000
		temp_df = obj.preprocess(temp_df)
		obj.fit(temp_df)
		n_clusters = len(set(obj.labels)) - (1 if -1 in obj.labels else 0)
		print('clusters : ' + str(n_clusters))
		n_outliers = list(obj.labels).count(-1)
		print('outliers : ' + str(n_outliers))
	
	filename = 'trained_ll.pkl'
	pickle.dump(obj.ll, open(filename, 'wb'))
	filename = 'trained_ss.pkl'
	pickle.dump(obj.ss, open(filename, 'wb'))

	filename = 'trained_dbscan.pkl'
	pickle.dump(obj.model, open(filename, 'wb'))
