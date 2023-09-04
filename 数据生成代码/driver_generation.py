import pandas as pd
import numpy as np
import random
sample_size=81*81
service=pd.read_csv('service.csv')
service=pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\service_csv.csv')
print(service.shape)
code1=service['0'].values
code2=service['to'].values



phone=[]
pheaders=['136','150','139','189','196']
ph=random.choices(pheaders,k=sample_size)

name=[]
lastname='赵钱孙李周吴郑王刘关张陈林邓江胡习沈冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
lastname=list(lastname)
ln=random.choices(lastname,k=sample_size)
firstname='焦金力强清爱国沐宸浩宇沐辰茗泽奕辰宇泽浩然奕泽宇轩沐阳'
firstname=list(firstname)
fn=random.choices(firstname,k=sample_size)

sex=['男','女']
sex=random.choices(sex,k=sample_size)


money=list(range(8000,12001,500))
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

driver=pd.DataFrame(name)
driver['sex']=sex
driver['phone']=phone
driver['ddeparture']=code1
driver['ddestination']=code2
driver['dsalary']=cmoney
driver['dcompensation']=csalary
driver=driver.rename({0:'dname'},axis=1)
print(driver)

#driver.to_csv('driver.csv')
driver.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\driver_gbk.csv',encoding='gbk')