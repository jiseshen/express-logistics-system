import pandas as pd
import numpy as np
import random

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

settings.configure()
sample_size = 100
password_length_interval = [8, 20]

courier = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\courier_gbk.csv',
                      encoding='gbk')
courier = courier.rename({'cphone': 'phone'}, axis=1)
driver = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\driver_gbk.csv',
                     encoding='gbk')
manager = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\manager.csv', encoding='gbk')
a = ['123']
staff0 = pd.DataFrame(a)
staff0['id'] = 1
staff0['class'] = '超管'
staff0.rename({'0': 'phone'})

staff = pd.DataFrame(courier['phone'])
staff['id'] = courier.index.values
staff['class'] = '快递员'
staff1 = pd.DataFrame(driver['phone'])
staff1['id'] = driver.index.values
staff1['class'] = '货车司机'
staff2 = pd.DataFrame(manager['phone'])
staff2['id'] = manager.index.values
staff2['class'] = '驿站管理员'
staff = pd.concat([staff0, staff])
staff = pd.concat([staff, staff1])
staff = pd.concat([staff, staff2])
print(staff.info)

# phone=[]
# pheaders=['136','150','139','189','196']
# ph=random.choices(pheaders,k=sample_size)
# for i in range(sample_size):
#     phone.append(ph[i])
#     for j in range(8):
#         phone[i]=phone[i]+str(random.randint(0,9))
#
#
default_password = make_password('123456')
# # for i in range(sample_size):
# #     length=random.randint(password_length_interval[0],password_length_interval[1])
# #     passwords.append(str(random.randint(0,9)))
# #     for j in range(length-1):
# #         passwords[i]=passwords[i]+str(random.randint(0,9))
# #     passwords[i]=make_password(passwords[i])
#
# # class
# staff_class=['快递员','货车司机','驿站管理员','超管']
#
#
#
#
#
# user=pd.DataFrame(phone)
# user['password']=default_password
# #user['class']=
# user=user.rename({0:'phone'},axis=1)
# print(user)
# staff=['']
staff['password'] = default_password

staff = staff[['phone', 'password', 'class', 'id']]
staff.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\staff_gbk.csv', index=False,
             encoding='gbk')
