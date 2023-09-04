import pandas as pd
import numpy as np

package = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\package_gbk1.csv',
                      encoding='gbk')
package = package[package['status'] == '已到站'][['station_id', 'shelf', 'layer']]
package = package.astype(int)
print(package)
station = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\station.csv', encoding='gbk')

# p=package.groupby(['station_id','shelf','layer']).count().iloc[:,1]
# print(p)
# p.to_csv('p.csv')


s = station['Unnamed: 0'].values
shelf = list(range(1, 21))
shelf1 = []
for i in range(1, 21):
    for j in range(6):
        shelf1.append(i)

layer = list(range(1, 7))
num = len(shelf) * len(layer)
num1 = len(s)
num2 = len(s) * len(shelf)
s = np.expand_dims(s, 0).repeat(num, axis=0)
s = np.reshape(s, (-1,), order='F')
print(s.shape)
shelf1 = np.expand_dims(shelf1, 0).repeat(num1, axis=0)
shelf = np.reshape(shelf1, (-1,), order='C')
print(shelf)
layer = np.expand_dims(layer, 0).repeat(num2, axis=0)
layer = np.reshape(layer, (-1,), order='C')

store = pd.DataFrame(s)
store['shelf'] = shelf
store['layer'] = layer
store = store.rename({0: 'station_id'}, axis=1)
store['num'] = 0
print(store)
# using mask!!!!!!!!!!!!!!!!
for i in range(package.shape[0]):
    sta = package.iloc[i, :][['station_id', 'shelf', 'layer']]
    # print(sta)
    # v=store[(store['station_id']==sta[0])&(store['shelf']==sta[1])&(store['layer']==sta[2])].loc[:,'num'].values[0]
    # store1=store.copy()
    mask = (store['station_id'] == sta[0]) & (store['shelf'] == sta[1]) & (store['layer'] == sta[2])
    # store[(store['station_id'] == sta[0]) & (store['shelf'] == sta[1]) & (store['layer'] == sta[2])].loc[:,'num']=1
    store.loc[mask, 'num'] = store.loc[mask, 'num'] + 1

store.to_csv('store.csv', encoding='gbk')
print(store['num'].sum())
