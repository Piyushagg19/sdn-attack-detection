from sklearn.model_selection import train_test_split
from sklearn import metrics
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle

from os import path

MODEL_FILE = 'trained_ann.h5'
LL_FILE = 'trained_ll.pkl'
SS_FILE = 'trained_ss.pkl'

class Model:
	def __init__(self):
		self.model = None
		if path.exists(MODEL_FILE):
			self.model = load_model(MODEL_FILE)
		else:
			self.model = Sequential()
			self.model.add(Flatten(input_shape=(7,)))
			self.model.add(Dense(10, activation='relu'))
			self.model.add(Dense(20, activation='relu'))
			self.model.add(Dense(10, activation='relu'))
			self.model.add(Dense(1, activation='sigmoid'))
			self.model.compile(loss='binary_crossentropy', optimizer='adam')
		
		self.ll = LabelEncoder()
		if path.exists(LL_FILE):
			self.ll = pickle.load(open(LL_FILE, 'rb'))

		self.ss = StandardScaler()
		if path.exists(SS_FILE):
			self.ss = pickle.load(open(SS_FILE, 'rb'))
		#self.model = DBSCAN(eps=3.0, min_samples=25)

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

		# label encoding dst mac addresses
		df = df[['in-port', 'eth_dst', 'out-port', 'total_packets', 'total_bytes', 'duration', 'weight', 'class']]
		df['eth_dst'] = self.ll.fit_transform(df['eth_dst'])

		# normalizing data
		cols = ['total_packets', 'total_bytes', 'duration', 'weight']
		scaled_values = self.ss.fit_transform(df[cols].values)
		df[cols] = scaled_values
		return df

	def fit(self, df):
		print('inside fit')
		self.model.fit(df)

	def predict(self, df):
		return self.model.predict(df)


if __name__ == "__main__":
	print("inside")
	obj = Model()
	df = pd.read_csv('../training data/training_data_neg_1.csv')
	# df1 = pd.read_csv('./training data/training_data_neg.csv')
	# df = df.append(df1, ignore_index=True)
	df = obj.preprocess(df)
	x_columns = df.columns.drop('class')
	x = df[x_columns].values
	y = df['class'].values

	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=53)

	obj.model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=50)
	
	filename = 'trained_ll.pkl'
	pickle.dump(obj.ll, open(filename, 'wb'))
	filename = 'trained_ss.pkl'
	pickle.dump(obj.ss, open(filename, 'wb'))

	obj.model.save(MODEL_FILE)
