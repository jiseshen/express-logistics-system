import pandas as pd
import numpy as np
import random
sample_size=81

#area=pd.read_csv('location.csv',header=0,encoding='gbk')
area=pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\location_coordinate.csv',header=0,encoding='gbk')
code=area['code']

phone=[]
pheaders=['136','150','139','189','196']
ph=random.choices(pheaders,k=sample_size)

name=[]
lastname='赵钱孙李周吴郑王刘关张陈林邓江胡习沈冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
lastname=list(lastname)
ln=random.choices(lastname,k=sample_size)
firstname='数据库及其实现上海卫健维高等线性代数'
firstname=list(firstname)
fn=random.choices(firstname,k=sample_size)

sex=['男','女']
sex=random.choices(sex,k=sample_size)

money=list(range(3000,5001,100))
salary=list(range(100,1001,50))
cmoney=random.choices(money,k=sample_size)
csalary=random.choices(salary,k=sample_size)

for i in range(sample_size):
    name.append(ln[i]+fn[i])
print(lastname)
for i in range(sample_size):
    phone.append(ph[i])
    for j in range(8):
        phone[i]=phone[i]+str(random.randint(0,9))

#print(phone)
#sample_codes=random.choices(code.values,k=sample_size)
courier=pd.DataFrame(code)
courier['cname']=name
courier['csex']=sex
courier['cphone']=phone
courier['cmoney']=cmoney
courier['csalary']=csalary
courier=courier.rename({'code':'clocation'},axis=1)
print(courier)

#courier.to_csv('courier.csv')
courier.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\courier_gbk.csv',encoding='gbk')