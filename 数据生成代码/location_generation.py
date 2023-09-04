import pandas as pd
import numpy as np

# coordinate : bj0:17,tj18:23,sh786:802,sz1803:1808,wh1569:1580,cd2011:2019,sy503:510,xian2425:2433,zhengzhou1422:1433
data = pd.read_csv('data.csv')
area = pd.read_csv('area.csv')
# print(data[data['code']==110101])


area['pname'] = area['province'].apply(lambda x: data[data['code'] == x * 10000]['name'].values[0])
area['cname'] = area.apply(lambda x: data[data['code'] == x['province'] * 10000 + x['city'] * 100]['name'].values,
                           axis=1)
area['cname'] = area.apply(lambda x: x['cname'][0] if x['cname'] else x['pname'], axis=1)
# print(area['province'].apply(lambda x:x*10000))
# print(area['cname'])


# area[['code','name','cname']].to_csv('location_gbk.csv',index=False,encoding='gbk')
# area['code'].astype(np.object)
region = pd.read_csv('region.csv')
region = region.rename({'county': 'name'}, axis=1)
# region=region.drop(index = [1214,])
# tmp=(region['code'].values)
# tmp=tmp.astype(int)
# print(region[region['code']=='890至896'].index.values)
# region['code']=region['code'].astype(np.int64)
area = pd.merge(area, region, on='name')
print(area)

cities = ['北京市', '上海市', '深圳市', '成都市', '长春市', '西安市']

area[area['cname'].isin(cities)][['code', 'name', 'cname', 'longitude', 'latitude']].to_csv(
    'C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\location_coordinate.csv', index=False,
    encoding='gbk')
