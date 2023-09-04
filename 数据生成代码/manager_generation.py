import pandas as pd
import numpy as np
import random

# 我想的解释驿站id的方法是
sample_size = 81

phone = []
pheaders = ['136', '150', '139', '189', '196']
ph = random.choices(pheaders, k=sample_size)

name = []
lastname = '毛刘周朱陈林邓赵钱孙李周吴郑王江胡习'
lastname = list(lastname)
ln = random.choices(lastname, k=sample_size)
firstname = '荀彧利国家生以因福避趋之谈笑风生薄熙来'
firstname = list(firstname)
fn = random.choices(firstname, k=sample_size)

sex = ['男', '女']
sex = random.choices(sex, k=sample_size)

salary = list(range(5000, 7000, 200))
csalary = random.choices(salary, k=sample_size)

for i in range(sample_size):
    name.append(ln[i] + fn[i])
print(lastname)
for i in range(sample_size):
    phone.append(ph[i])
    for j in range(8):
        phone[i] = phone[i] + str(random.randint(0, 9))

# print(phone)
code = list(range(0, 81))
# sample_codes=random.choices(code,k=sample_size)
manager = pd.DataFrame()
manager['name'] = name
manager['sex'] = sex
manager['phone'] = phone
manager['station_id'] = code
manager['msalary'] = csalary

print(manager)

manager.to_csv('manager_gbk.csv', encoding='gbk')
