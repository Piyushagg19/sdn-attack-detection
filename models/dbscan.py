from sklearn.cluster import DBSCAN
import sklearn.utils
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
import pandas as pd

pd.options.mode.chained_assignment = None
import pickle

MODEL_FILE = 'models/trained_dbscan.pkl'
SS_FILE = 'models/trained_ss.pkl'


class Model:

    def __init__(self):
        # self.model = pickle.load(open(MODEL_FILE, 'rb'))
        # print("params : " + str(self.model.get_params()))
        self.model = DBSCAN(eps=2.5, min_samples=9, algorithm='ball_tree')

    def preprocess(self, df):
        # assigning weights based on out-port
        for indx, r in df.iterrows():
            weight_col = 'out-port-' + str(df.loc[indx, 'out-port'])
            weights = df.loc[indx, weight_col][1:-1]
            weights = weights.split(",")
            l = []
            for w in weights:
                if w != '':
                    l.append(int(w.strip()))

            df.loc[indx, 'weight'] = max(l, default=10)

        df.drop(columns=['out-port-1', 'out-port-2', 'out-port-3', 'out-port-4', 'out-port-5', 'out-port-6'],
                inplace=True)

        # normalizing data
        cols = ['total_packets', 'total_bytes', 'duration', 'weight']
        self.normalize(df, cols)
        return df

    def normalize(self, df, cols):
        df[cols] = df[cols].apply(pd.to_numeric)
        for col in cols:
            mean = df[col].mean()
            sd = df[col].std()
            if sd == 0:
                df[col] = 0
            else:
                df[col] = (df[col] - mean) / sd

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
    df = df[1000:5000]
    # df = df[2000:2501]
    # df = obj.preprocess(df)
    # obj.fit(df)
    # n_clusters = len(set(obj.labels)) - (1 if -1 in obj.labels else 0)
    # print('clusters : ' + str(n_clusters))
    # n_outliers = list(obj.labels).count(-1)
    # print('outliers : ' + str(n_outliers))
    N = df.shape[0]
    i = 0
    while i < N:
        temp_df = df[i: min(N, i + 100)]
        i += 100
        temp_df = obj.preprocess(temp_df)
        print(temp_df.shape)
        obj.fit(temp_df)
        n_clusters = len(set(obj.labels)) - (1 if -1 in obj.labels else 0)
        print('clusters : ' + str(n_clusters))
        n_outliers = list(obj.labels).count(-1)
        print('outliers : ' + str(n_outliers))

    pickle.dump(obj.model, open('../' + MODEL_FILE, 'wb'))
