import pandas as pd
import numpy as np
import random

sample_size = 1000
usize = 1000
# area=pd.read_csv('location.csv',header=0,encoding='gbk')
area = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\location_coordinate.csv',
                   header=0, encoding='gbk')
code = area['code']

phone = []
pheaders = ['136', '150', '139', '189', '196']
ph = random.choices(pheaders, k=sample_size)

name = []
lastname = '赵钱孙李周吴郑王刘关张陈林邓江胡习沈'
lastname = list(lastname)
ln = random.choices(lastname, k=sample_size)
firstname = '数据库及其实现上海卫健维高等线性代数'
firstname = list(firstname)
fn = random.choices(firstname, k=sample_size)
for i in range(sample_size):
    name.append(ln[i] + fn[i])
print(lastname)
for i in range(sample_size):
    phone.append(ph[i])
    for j in range(8):
        phone[i] = phone[i] + str(random.randint(0, 9))

set = ['家', '公司', '学校', '家2', '公司2', '学校2', '家3', '公司3', '学校3']
set = random.choices(set, k=sample_size)

data = pd.read_csv('data.csv')
df = pd.read_csv('area.csv', header=0)
area = df[['code', 'name']]
area['address'] = area.apply(
    lambda x: data[data['code'] == x['code']]['name'].iloc[1] + str(random.randint(100, 500)) + '号' if
    data[data['code'] == x['code']].shape[0] > 1 else '胜利路514号', axis=1)
address = random.choices(area['address'].values, k=sample_size)
uid = list(range(1, usize + 1))
uid = random.choices(uid, k=sample_size)

sample_codes = random.choices(code.values, k=sample_size)
identity = pd.DataFrame(set)
identity['phone'] = phone
identity['iaddress'] = address
identity['ilocation'] = sample_codes
identity['iname'] = name
identity['uid'] = uid
identity = identity.rename({0: 'iset'}, axis=1)
print(identity)

# identity.to_csv('identity.csv')
identity.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\identity_gbk.csv', encoding='gbk')
