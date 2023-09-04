import pymysql
import pandas as pd
# 读到一个pandas的dataframe数据类型中
df=pd.read_csv()
data=df.values

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1453', charset='utf8')
cursor = conn.cursor()

# check
cursor.execute('show databases')
print(cursor.fetchall())

# establish
cursor.execute('create database if not exists Cainiao default charset utf8 collate utf8_general_ci')
# add\delete\revise need commit()
conn.commit()

# enter one database
cursor.execute('use mysql')
cursor.execute('show tables')
cursor.execute('use Cainiao')
cursor.execute('create table if not exists customers( \
          name varchar(16) ,\
          phone varchar(16),\
          location varchar(16))')
conn.commit()
cursor.execute('show tables')
tables=cursor.fetchall()
print(tables)