import pandas as pd
import numpy as np
import random
import datetime

sample_size = 10000

# datetime
# month=np.array(range(1,6))
day1 = np.array(range(1, 3))
day2 = np.array(range(3, 5))
day3 = np.array(range(5, 7))
day4 = np.array(range(7, 9))
hour = np.array(range(0, 24))
ms = np.array(range(0, 60))
# months=random.choices(month,k=sample_size)
days1 = random.choices(day1, k=sample_size)
days2 = random.choices(day2, k=sample_size)
days3 = random.choices(day3, k=sample_size)
days4 = random.choices(day4, k=sample_size)
hours = random.choices(hour, k=sample_size)
minutes = random.choices(ms, k=sample_size)
seconds = random.choices(ms, k=sample_size)

start_time = []
send_time = []
arrival_time = []
pick_time = []
for i in range(sample_size):
    start_time.append(datetime.datetime(2022, 5, days1[i], hours[i], minutes[i], seconds[i]))
    send_time.append(datetime.datetime(2022, 5, days2[i], hours[i], minutes[i], seconds[i]))
    arrival_time.append(datetime.datetime(2022, 5, days3[i], hours[i], minutes[i], seconds[i]))
    pick_time.append(datetime.datetime(2022, 5, days4[i], hours[i], minutes[i], seconds[i]))
# print(d)


# df.to_csv()

# weight,size
weight = list(range(1, 21))
weight = random.choices(weight, k=sample_size, weights=range(21, 1, -1))

size = list(range(1, 21))
size = random.choices(size, k=sample_size, weights=range(21, 1, -1))

content = '普通食品，文件，电子产品，玻璃制品，生鲜食品，生活用品'
content = content.split('，')
content = random.choices(content, k=sample_size)

# data=pd.read_csv('data.csv')
# df=pd.read_csv('area.csv',header=0)
# area=df[['code','name']]
# area['address']=area.apply(lambda x:data[data['code']==x['code']]['name'].iloc[1]+str(random.randint(100,500))+'号' if data[data['code']==x['code']].shape[0]>1 else '胜利路514号',axis=1)
# pdeparture=random.choices(area['address'].values,k=sample_size)
# pdeparture=

# id,iid,location
# df=pd.read_csv('identity.csv')
df = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\identity_gbk.csv', encoding='gbk')
sender_id = df['uid'].values
sender_id = random.choices(sender_id, k=sample_size)

receiver_id = df['uid'].values
receiver_id = random.choices(receiver_id, k=sample_size)
# for i in range(sample_size):
# if receiver_id[i]==sender_id[i]:
# if sender_id[i]!=1:
#     receiver_id[i]=sender_id[i]-1
# else:
#     receiver_id[i]=97


pdeparture = []
sender_iid = []
for i in range(sample_size):
    sender_iid.append(df[df['uid'] == sender_id[i]].index.values[0])
    pdeparture.append(df.iloc[sender_iid[i]]['ilocation'])
    # pdeparture.append(df[df['uid']==sender_id[i]]['ilocation'])

pdestination = []
receiver_iid = []
for i in range(sample_size):
    receiver_iid.append(df[df['uid'] == receiver_id[i]].index.values[0])
    # pdestination.append(df[df['uid']==receiver_id[i]]['ilocation'])
    pdestination.append((df.iloc[receiver_iid[i]]['ilocation']))

# courier
courier_a_id = []
courier_b_id = []
courier = pd.read_csv('courier.csv')
courier = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\courier_gbk.csv',
                      encoding='gbk')
# for i in range(sample_size):
# courier_a_id.append(courier[courier['clocation']==pdeparture[i]].index.values[0])
# courier_b_id.append(courier[courier['clocation'] == pdestination[i]].index.values[0])
# courier_a_id=(courier[courier['clocation'] in pdeparture].index)
spdeparture = pd.Series(pdeparture)
spdeparture.name = 'clocation'
spdestination = pd.Series(pdestination)
spdestination.name = 'clocation'
courier_a_id1 = pd.merge(courier, spdeparture)
courier_b_id1 = pd.merge(courier, spdestination)
for i in range(sample_size):
    courier_a_id.append(courier_a_id1[courier_a_id1['clocation'] == pdeparture[i]]['Unnamed: 0'].values[0])
    courier_b_id.append(courier_b_id1[courier_b_id1['clocation'] == pdestination[i]]['Unnamed: 0'].values[0])
# print(courier_a_id1)
# print(courier_b_id)

courier_b_id1 = pd.merge(courier, spdestination).iloc[:, 0]

# courier_b_id=(courier[courier['clocation'] in pdestination].index.values)
# station
station_id = []
# station=pd.read_csv('station.csv')


# driver
driver_id = []
driver = pd.read_csv('driver.csv')
driver = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\driver_gbk.csv',
                     encoding='gbk')
driver_sample = pd.DataFrame(spdeparture)
driver_sample['ddestination'] = spdestination
driver_sample = driver_sample.rename({'clocation': 'ddeparture'}, axis=1)
driver = pd.merge(driver, driver_sample)
# print(driver['Unnamed: 0'])

for i in range(sample_size):
    # 必须用&
    driver_id.append(driver[(driver['ddeparture'] == pdeparture[i]) & (driver['ddestination'] == pdestination[i])][
                         'Unnamed: 0'].values[0])

# print(driver_id)


# pick_id
shelf = list(range(1, 21))
layer = list(range(1, 7))
shelf = random.choices(shelf, k=sample_size)
layer = random.choices(layer, k=sample_size)
pick_id = []
picker_id = []
for i in range(sample_size):
    pick_id.append(
        str(shelf[i]) + '-' + str(layer[i]) + '-' + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(random.randint(0, 9)))
    picker_id.append(
        str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(random.randint(0, 9)))
# service
# service=pd.read_csv('service.csv')
service = pd.read_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\service_csv.csv',
                      encoding='gbk')
driver_sample = driver_sample.rename({'ddeparture': '0', 'ddestination': 'to'}, axis=1)
service = pd.merge(service, driver_sample)
# print(service)

# station price
station_price = [0, 1, 2, 3]
station_price = random.choices(station_price, k=sample_size)

# price (depends on weight only)
price = []
for i in range(sample_size):
    price.append(
        service[(service['0'] == pdeparture[i]) & (service['to'] == pdestination[i])]['unit_price'].values[0] * weight[
            i])

# status
status = ['未发货', '已接单', '运输中', '配送中', '已发货', '已到站', '已收货']
# status=status.split('，')
status = random.choices(status, k=sample_size)
for i in range(sample_size):
    if status[i] != '已收货':
        pick_time[i] = np.nan
        station_price[i] = np.nan
        if status[i] != '已到站':
            shelf[i] = np.nan
            layer[i] = np.nan
            pick_id[i] = np.nan
            arrival_time[i] = np.nan
            if status[i] != '配送中':
                courier_b_id[i] = np.nan
                if status[i] != '运输中':
                    driver_id[i] = np.nan
                    if status[i] != '已接单':
                        weight[i] = np.nan
                        size[i] = np.nan
                        price[i] = np.nan
                        if status[i] != '已发货':
                            courier_a_id[i] = np.nan
                            send_time[i] = np.nan

    else:
        shelf[i] = np.nan
        layer[i] = np.nan

# expected arrival
expected_arrival_time = []
for i in range(sample_size):
    if start_time[i] != np.nan:
        # mind the []
        h = service[(service['0'] == pdeparture[i]) & (service['to'] == pdestination[i])]['duration'].values[0]
        h = int(h)
        print(h)
        expected_arrival_time.append(start_time[i] + datetime.timedelta(hours=h))
    else:
        expected_arrival_time.append(np.nan)

package = pd.DataFrame(weight)
package['size'] = size
package['content'] = content
package['sender_id'] = sender_id
package['receiver_id'] = receiver_id
package['sender_iid'] = sender_iid
package['receiver_iid'] = receiver_iid
package['pdeparture'] = pdeparture
package['pdestination'] = pdestination
package['express_price'] = price
package['station price'] = station_price
package['status'] = status
package['start_time'] = start_time
package['send_time'] = send_time
package['expected_arrival_time'] = expected_arrival_time
package['arrival_time'] = arrival_time
package['pick_time'] = pick_time
package['pick_id'] = pick_id
package['picker_id'] = picker_id
package['shelf'] = shelf
package['layer'] = layer
package['courier_a_id'] = courier_a_id
# if not arrived then no courier b or station
package['courier_b_id'] = courier_b_id
package['driver_id'] = driver_id
# station id is the same as courier b in my situation
package['station_id'] = courier_b_id
# one manager for each station
package['manager_id'] = courier_b_id
package = package.rename({'0': 'weight'}, axis=1)

# print(pick_id)
# package.to_csv('package.csv')
package.to_csv('C:\\Users\\Geralt\\PycharmProjects\\pythonProject\\database\\gbks\\package_gbk_allnan.csv',
               encoding='gbk')
