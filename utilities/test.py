from queue import Queue
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
import pandas as pd
from models import dbscan

model = dbscan.Model()
print(model.model.get_params())
print(len(model.model.core_sample_indices_))
print(model.model.components_)

# df = pd.read_csv('../training data/training_data_pos.csv')
# df.drop(columns=['time', 'eth_src', 'eth_dst', 'priority', 'class', 'out-port-1', 'out-port-2', 'out-port-3', 'out-port-4', 'out-port-5', 'out-port-6', 'class'], inplace=True)
#
# data = [
#     {'time': '1611143725', 'datapath': '1', 'in-port': '4', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x01'", 'out-port': '3', 'total_packets': '54740', 'total_bytes': '82766880', 'duration': '3', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'}
# ]
#
# data.append({'time': '1611143765', 'datapath': '1', 'in-port': '4', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x01'", 'out-port': '3', 'total_packets': '499826', 'total_bytes': '755736912', 'duration': '43', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'})
# data.append({'time': '1611143736', 'datapath': '1', 'in-port': '4', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x01'", 'out-port': '3', 'total_packets': '231860', 'total_bytes': '350572320', 'duration': '13', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'})
# data.append({'time': '1611143736', 'datapath': '1', 'in-port': '2', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x03'", 'out-port': '5', 'total_packets': '91', 'total_bytes': '137592', 'duration': '0', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'})
# data.append({'time': '1611143745', 'datapath': '1', 'in-port': '4', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x01'", 'out-port': '3', 'total_packets': '400488', 'total_bytes': '605537856', 'duration': '23', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'})
# data.append({'time': '1611143745', 'datapath': '1', 'in-port': '2', 'eth_src': "b'\x00\x00\x00\x00\x00\x00'", 'eth_dst': "b'\x00\x00\x00\x00\x00\x03'", 'out-port': '5', 'total_packets': '149776', 'total_bytes': '226461312', 'duration': '8', 'priority': '32768', 'out-port-1': '[]', 'out-port-2': '[]', 'out-port-3': '[]', 'out-port-4': '[]', 'out-port-5': '[]', 'out-port-6': '[]', 'class': '0'})
#
# df = pd.DataFrame(data)
# print(df)
# df = model.preprocess(df)
# n = len(df.columns)
#
# pca = PCA(n_components=n)
# pca.fit(df)
# xvector = pca.components_[0]
# yvector = pca.components_[1]
#
# xs = pca.transform(df)[:,0]
# ys = pca.transform(df)[:,1]
#
# for i in range(len(xvector)):
#     plt.arrow(0, 0, xvector[i]*max(xs), yvector[i]*max(ys), color='r', width=0.0005, head_width=0.0025)
#     plt.text(xvector[i]*max(xs)*1.2, yvector[i]*max(ys)*1.2, list(df.columns.values)[i], color='r')
#
# for i in range(len(xs)):
#     plt.plot(xs[i], ys[i], 'bo')
#     plt.plot(xs[i]*5.0, ys[i]*5.0, list(df.index)[i], color='b')
#
# plt.show()


# df.drop(columns=['time', 'eth_src', 'eth_dst', 'priority', 'class'], inplace=True)
# df = model.preprocess(df)
# print(model.predict(df))
# x_columns = df.columns.drop('class')
# x = df[x_columns].values
# y = df['class'].values
# res = model.predict(x)
# print('records : ' + str(x))
# print('response from model : ' + str(res))
# print('actuall result : ' + str(y))
