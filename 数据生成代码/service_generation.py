import pandas as pd
import numpy as np
import random

# df=pd.read_csv('location.csv',header=0,encoding='gbk')
df = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\location_coordinate.csv', header=0,
                 encoding='gbk')
area = df['code']
l = area.shape[0]
av = area.values
print(area.shape)
num = 81
av = np.expand_dims(av, 0).repeat(num, axis=0)
av = np.reshape(av, (-1,), order='C')
durations = [24, 48, 72, 96, 120]
prices = np.array(list(range(8, 21)))
prices = np.divide(prices, 2)
d = np.array(random.choices(durations, k=num * num))
p = np.array(random.choices(prices, k=num * num))
# service=pd.DataFrame()
# service['from']=area.apply()
codes = area.values
codes = np.expand_dims(codes, 0).repeat(num, axis=0)
codes = np.reshape(codes, (-1, 1), order='F')
codes = pd.DataFrame(codes)

print(av.shape)
codes['to'] = pd.Series(av)
codes['duration'] = pd.Series(d)
codes['unit_price'] = pd.Series(p)
codes = codes.rename({0: 'departure', 'to': 'destination'})
# codes.to_csv('service.csv',index=False,encoding='gbk')
print(codes)

codes.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\service_csv.csv', index=False,
             encoding='gbk')
# codes_df=pd.DataFrame(codes)
# service=pd.DataFrame()
# service['from']=codes_df[0]
# for i in range(1,2846):
#     tmp=service['from']
#     service['from']=pd.concat([tmp,codes_df[i]],axis=0, ignore_index=True)
#
# print(service.shape)
