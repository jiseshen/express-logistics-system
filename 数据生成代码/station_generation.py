import pandas as pd
import numpy as np
import random

data = pd.read_csv('data.csv')
df = pd.read_csv('area.csv', header=0)
df = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\location_coordinate.csv', header=0,
                 encoding='gbk')
area = df[['code', 'name']]
area['address'] = area.apply(
    lambda x: data[data['code'] == x['code']]['name'].iloc[1] + str(random.randint(100, 500)) + '号' if
    data[data['code'] == x['code']].shape[0] > 1 else '胜利路514号', axis=1)
# print(area)
print(area['name'].size)
print(area['name'].unique().size)
area = area.rename(columns={'name': 'location', 'address': 'address'})
# print(area)
# area[['code','address']].to_csv('station.csv',encoding='gbk')
area[['code', 'address']].to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\station.csv',
                                 encoding='gbk')
