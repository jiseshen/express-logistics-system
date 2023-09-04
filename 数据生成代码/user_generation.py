import pandas as pd
import numpy as np
import random

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

settings.configure()
sample_size = 1000
password_length_interval = [8, 20]

phone = []
phone.append('11451419198')
pheaders = ['136', '150', '139', '189', '196']
ph = random.choices(pheaders, k=sample_size)
for i in range(sample_size):
    phone.append(ph[i])
    for j in range(8):
        phone[i + 1] = phone[i + 1] + str(random.randint(0, 9))


# the first is 123456
passwords = [make_password('123456')]
for i in range(sample_size):
    length = random.randint(password_length_interval[0], password_length_interval[1])
    passwords.append(str(random.randint(0, 9)))
    for j in range(length - 1):
        passwords[i + 1] = passwords[i + 1] + str(random.randint(0, 9))
    passwords[i + 1] = make_password(passwords[i + 1])

# print(phone)
# sample_codes=random.choices(code.values,k=sample_size)
user = pd.DataFrame(phone)
user['password'] = passwords
user = user.rename({0: 'phone'}, axis=1)
print(user)

# user.to_csv('user.csv')
user.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\user_gbk.csv', encoding='gbk')
