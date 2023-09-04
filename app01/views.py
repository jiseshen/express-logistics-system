from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import datetime, time
from django.http import JsonResponse
from django.db import connection, transaction
from django.db.models import Q, Count, Max, Min
import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
from app01.models import UserLogin, Identity, Manager, Package, StaffLogin, Store, Station, Service, Courier, Driver, \
    Map
import re

# Create your views here.

def main(request):
    # UserLogin.objects.filter(phone='19665397717').update(password=make_password('123456'))
    return render(request, "homepage.html")


def userregister(request):
    if request.method == "GET":
        return render(request, 'userregister.html', context={'error_msg': ''})
    phone = request.POST.get('phone')
    pattern = re.compile(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")
    if not pattern.match(phone):
        return render(request,'userregister.html',{'error_msg':'请输入真实的手机号'})
    if UserLogin.objects.filter(phone=phone):
        return render(request, 'userregister.html', context={'error_msg': '该用户已注册'})
    password = request.POST.get('password')
    pattern2 = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    if not pattern2.match(password):
        return render(request, 'userregister.html', context={'error_msg':'请设置合理的密码'})
    password = make_password(password)
    new_id = UserLogin.objects.all().aggregate(Max('id'))['id__max'] + 1
    UserLogin.objects.create(phone=phone, password=password, id=new_id)
    return render(request, 'jumpage2.html')


def userlogin(request):
    if request.method == "GET":
        return render(request, "userlogin.html", context={"error_msg": ""})
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    user = UserLogin.objects.filter(phone=phone)
    if user:
        encoded = user.first().password
        id = user.first().id
        if check_password(password,encoded):
            return redirect(userpage, id=id, page=1, role=1)
        else:
            return render(request, 'userlogin.html', {'error_msg': '密码输入有误'})
    else:
        return render(request, 'userlogin.html', context={"error_msg": "该用户不存在"})


def identityregister(request, id):
    if request.method == "GET":
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'identityregister.html',
                      context={'map': mapdic, 'city': city, 'error_msg': '', 'id': id, 'search': 0})
    set = request.POST.get('set')
    phone = request.POST.get("phone")
    name = request.POST.get("name")
    city = request.POST.get('city')
    location = request.POST.get("location")
    address = request.POST.get("address")
    if Identity.objects.filter(uid=id,iset=set):
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'identityregister.html',
                      context={'map': mapdic, 'city': city, 'error_msg': "该身份标识已注册", 'id': id, 'search': 0})
    location_id = Map.objects.filter(district=location, city=city).first().id
    Identity.objects.create(iphone=phone, iset=set, iname=name, ilocation=location_id, iaddress=address, uid=id)
    return render(request, 'jumpage1.html', locals())


@transaction.non_atomic_requests
def userpage(request, id, role=1, page=1):
    if request.method == 'POST':
        packageinfo = Package.objects.filter(pid=request.POST.get("pid")).values('pdeparture', 'pdestination','arrival_time',
                                                                                 'start_time', 'expected_time','status').first()
        if packageinfo:
            departure = Map.objects.filter(id=packageinfo['pdeparture']).first()
            depacity = departure.city
            depadist = departure.district
            destination = Map.objects.filter(id=packageinfo['pdestination']).first()
            destcity = destination.city
            destdist = destination.district
            if packageinfo['status']=='已到站' or packageinfo['status']=='已收货':
                return HttpResponse('该物流从'+depacity+depadist+'到' + destcity + destdist + ",开始时间为" + packageinfo[
                'start_time'].strftime('%Y-%m-%d %H') + '时，已于'+ packageinfo['arrival_time'].strftime(
                '%Y-%m-%d %H') + '时到达')
            return HttpResponse('该物流从' + depacity + depadist + '到' + destcity + destdist + ",开始时间为" + packageinfo[
                'start_time'].strftime('%Y-%m-%d %H') + '时，预计送达时间为' + packageinfo['expected_time'].strftime(
                '%Y-%m-%d %H') + '时')
        else:
            return HttpResponse('暂无该物流信息')
    cur = connection.cursor()
    cur.callproc('receiver_view', [id])
    receiver_view = cur.fetchall()
    cur.nextset()
    cur.callproc('sender_view', [id])
    sender_view = cur.fetchall()
    paginator_r = Paginator(receiver_view, 10)
    paginator_s = Paginator(sender_view, 10)
    search = 1
    if int(role) == 1:
        page_r = paginator_r.page(page)
        return render(request, 'receiverpage.html', locals())
    if int(role) == 2:
        page_s = paginator_s.page(page)
        return render(request, 'senderpage.html', locals())


def depaheatmap(request):
    map=Map.objects.all()
    data = [[item.latitude,
             item.longitude,
             Package.objects.filter(pdeparture=item.id).count()] for item in map]
    map_osm = folium.Map(location=[35, 110], zoom_start=5)
    HeatMap(data,annot=True).add_to(map_osm)
    file_path = r"D:\物流公司系统\templates\depaheatmap.html"
    map_osm.save(file_path)
    return render(request, 'depaheatmap.html')


def destheatmap(request):
    map = Map.objects.all()
    data = [[item.latitude,
             item.longitude,
             Package.objects.filter(pdestination=item.id).count()] for item in map]
    map_osm = folium.Map(location=[35, 110], zoom_start=5)
    HeatMap(data).add_to(map_osm)
    file_path = r"D:\物流公司系统\templates\destheatmap.html"
    map_osm.save(file_path)
    return render(request, 'destheatmap.html')


def userchange(request, id):
    if request.method == 'GET':
        return render(request, 'userchange.html', {'error_msg': '', 'id': id})
    phone = request.POST.get("phone")
    origin = request.POST.get("origin_pass")
    new = request.POST.get("new_pass")
    pattern2 = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    if not pattern2.match(new):
        return render(request, 'userchange.html', context={'error_msg':'请设置合理的密码','id':id})
    new_confirm = request.POST.get("new_pass_confirm")
    if not UserLogin.objects.filter(phone=phone).first():
        return render(request, 'userchange.html', context={"error_msg": "该账号不存在！", 'id': id})
    encode = UserLogin.objects.filter(phone=phone).first().password
    if new == new_confirm:
        if check_password(origin, encode):
            new_encode = make_password(new)
            UserLogin.objects.filter(phone=phone).update(password=new_encode)
            return render(request, 'jumpage6.html')
        else:
            return render(request, 'userchange.html', context={"error_msg": "原密码输入错误！", 'id': id})
    else:
        return render(request, 'userchange.html', context={"error_msg": "新密码与再次输入不符！", 'id': id})


def usersend(request, id):
    if request.method == "GET":
        return render(request, 'sendform.html', {'error_msg': '', 'id': id, 'search': 0})
    aset = request.POST.get('sender_set')
    bphone = request.POST.get('receiver_phone')
    bset = request.POST.get('receiver_set')
    aid = Identity.objects.filter(uid=id, iset=aset).first()
    bid = Identity.objects.filter(iphone=bphone, iset=bset).first()
    if aid and bid:
        content = request.POST.get('content')
        aiid = aid.iid
        biid = bid.iid
        r_id = bid.uid
        departure = Identity.objects.filter(iid=aiid).first().ilocation
        destination = Identity.objects.filter(iid=biid).first().ilocation
        service = Service.objects.filter(departure=departure, destination=destination).first()
        unit_price = service.unit_price
        duration = service.duration
        station = Station.objects.filter(slocation=destination).first().sid
        Package.objects.create(start_time=timezone.now(), sender_id=id, sender_iid=aiid, pdeparture=departure,
                               pdestination=destination, receiver_id=r_id, receiver_iid=biid, content=content,
                               station_id=station, expected_time=timezone.now() + datetime.timedelta(hours=duration),
                               status='未发货')

        return render(request, 'jumpage3.html', locals())
    return render(request, 'sendform.html', {'error_msg': '输入的身份标识或收件人手机有误，系统尚未存入该数据。', 'id': id, 'search': 0})


def stationpage(request, myid, id, type=1, page=1):
    type = int(type)
    if type == 1:
        station_package = Package.objects.filter(station_id=id, status="配送中").order_by('start_time').values("pid", "weight", "size")
        paginator_a = Paginator(station_package, 10)
        page_a = paginator_a.page(page)
        return render(request, 'stationpagea.html', locals())
    elif type == 2:
        station_package = Package.objects.filter(station_id=id, status="已到站").values("pid", "shelf", "layor",
                                                                                     "arrival_time", "pick_id",
                                                                                     "picker_id").order_by(
            "arrival_time")
        paginator_b = Paginator(station_package, 10)
        page_b = paginator_b.page(page)
        return render(request, 'stationpageb.html', locals())
    else:
        station_package = Package.objects.filter(station_id=id, status="已收货").values("pid", "arrival_time", "pick_time",
                                                                                     "station_price")
        paginator_c = Paginator(station_package, 50)
        page_c = paginator_c.page(page)
        return render(request, 'stationpagec.html', locals())


@transaction.non_atomic_requests
def stationstore(request, myid, sid, pid):
    if Package.objects.filter(pid=pid).first().status!='配送中':
        return redirect(stationpage,myid=myid,id=sid,type=1,page=1)
    cur = connection.cursor()
    cur.callproc('station_arrangement', [int(sid), int(pid), 1, 1])
    store_location = cur.fetchone()
    shelf = store_location[0]
    layor = store_location[1]
    return render(request, 'stationstore.html', locals())


def stationcheck(request, myid, sid, pid):
    if request.method == "GET":
        return render(request, "stationcheck.html", context={"error_msg": "", 'pid': pid, 'myid': myid})

    picker_id = request.POST.get("picker_id")
    id = Package.objects.filter(pid=pid, picker_id=picker_id)
    if id:
        return redirect(stationpick, myid=myid, sid=sid, pid=pid)
    else:
        return render(request, 'stationcheck.html', context={"error_msg": "身份码有误", "pid": pid, 'myid': myid})


@transaction.non_atomic_requests
def stationpick(request, myid, sid, pid):
    cur = connection.cursor()
    shelf = Package.objects.filter(pid=pid).first().shelf
    layor = Package.objects.filter(pid=pid).first().layor
    cur.callproc('station_pricing', [pid, 1])
    time_price = cur.fetchone()
    arrival_time = time_price[0]
    pick_time = time_price[1]
    station_price = time_price[2]
    return render(request, 'stationpick.html', locals())


def stafflogin(request):
    if request.method == "GET":
        return render(request, "stafflogin.html", context={"error_msg": ""})

    phone = request.POST.get("phone")
    password = request.POST.get("password")
    type = request.POST.get('type')
    encoded = StaffLogin.objects.filter(phone=phone, class_field=type).first()
    if encoded:
        if check_password(password, encoded.password):
            if type == "驿站管理员":
                id = encoded.sid
                sid = Manager.objects.filter(mid=id).first().station_id
                return redirect(stationpage, myid=id, id=sid, type=1, page=1)
            if type == "快递员":
                id = encoded.sid
                return redirect(courierpage, id=id,page=1)
            else:
                id = encoded.sid
                return redirect(driverpage, id=id,page=1)
        else:
            return render(request, 'stafflogin.html', context={"error_msg": "用户名或密码有误"})
    else:
        return render(request, 'stafflogin.html', context={"error_msg": "用户名或密码有误"})


def customservice(request):
    mapdic = {}
    for city in Map.objects.values('city').distinct():
        mapdic[city['city']] = []
        for district in Map.objects.filter(city=city['city']).values('district'):
            mapdic[city['city']].append(district["district"])
    city = mapdic.keys()
    if request.method == "GET":
        return render(request, "customservice.html", {'map': mapdic, 'city': city, 'message': ''})
    depacity = request.POST.get('city1')
    depadist = request.POST.get('location1')
    destcity = request.POST.get('city2')
    destdist = request.POST.get('location2')
    if not depadist or not destdist:
        return render(request, "customservice.html", {'map': mapdic, 'city': city, 'message': '请选择'})
    departure = Map.objects.filter(city=depacity, district=depadist).first().id
    destination = Map.objects.filter(city=destcity, district=destdist).first().id
    duration = Service.objects.filter(departure=departure, destination=destination).first().duration
    up = Service.objects.filter(departure=departure, destination=destination).first().unit_price
    message = '从' + depacity + depadist + '到' + destcity + destdist + '的预计运送周期为' + str(duration) + '小时,每公斤价格为' + str(
        up) + '元'
    return render(request, "customservice.html", {'map': mapdic, 'city': city, 'message': message})


def customstation(request):
    mapdic = {}
    for city in Map.objects.values('city').distinct():
        mapdic[city['city']] = []
        for district in Map.objects.filter(city=city['city']).values('district'):
            mapdic[city['city']].append(district["district"])
    city = mapdic.keys()
    if request.method == "GET":
        return render(request, 'customstation.html', {'map': mapdic, 'city': city, 'message': ''})
    aimcity = request.POST.get('city')
    district = request.POST.get('location')
    if not district:
        return render(request, 'customstation.html', {'map': mapdic, 'city': city, 'message': '请选择'})
    location = Map.objects.filter(city=aimcity, district=district).first().id
    address = Station.objects.filter(slocation=location).first().saddress
    sid = Station.objects.filter(slocation=location).first().sid
    phone = Manager.objects.filter(station_id=sid).first().mphone
    message = str(sid) + '号驿站地址为' + address + '，联系电话为' + phone
    return render(request, 'customstation.html', {'map': mapdic, 'city': city, 'message': message})


def identity(request, id):
    if request.method == 'POST':
        packageinfo = Package.objects.filter(pid=request.POST.get("pid")).values('pdeparture', 'pdestination',
                                                                                 'start_time', 'expected_time').first()
        if packageinfo:
            departure = Map.objects.filter(id=packageinfo['pdeparture']).first()
            depacity = departure.city
            depadist = departure.district
            destination = Map.objects.filter(id=packageinfo['pdestination']).first()
            destcity = destination.city
            destdist = destination.district
            return HttpResponse('该物流从' + depacity + depadist + '到' + destcity + destdist + ",开始时间为" + packageinfo[
                'start_time'].strftime('%Y-%m-%d %H') + '时，预计送达时间为' + packageinfo['expected_time'].strftime(
                '%Y-%m-%d %H') + '时')
        else:
            return HttpResponse('暂无该物流信息')
    identities = Identity.objects.filter(uid=id).values('iid', 'iset', 'iname', 'iphone', 'iaddress')
    search = 1
    return render(request, 'identity.html', locals())


def identityedit(request, iid):
    identity = Identity.objects.filter(iid=iid).first()
    if request.method == 'GET':
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'identityedit.html',
                      context={'map': mapdic, 'city': city, 'error_msg': '', 'identity': identity, 'id': identity.uid,
                               'search': 0})
    set = request.POST.get('set')
    phone = request.POST.get("phone")
    name = request.POST.get("name")
    city = request.POST.get('city')
    location = request.POST.get("location")
    address = request.POST.get("address")
    if Identity.objects.filter(~Q(iid=iid), iset=set):
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'identityedit.html',
                      context={'map': mapdic, 'city': city, 'error_msg': "该身份标识已注册", 'identity': identity,
                               'id': identity.uid, 'search': 0})
    else:
        location_id = Map.objects.filter(district=location, city=city).first().id
        Identity.objects.filter(iid=iid).update(iphone=phone, iname=name, iset=set, ilocation=location_id,
                                                iaddress=address)
        return render(request, 'jumpage4.html', {"id": identity.uid})


def identitydelete(request, iid):
    id = Identity.objects.filter(iid=iid).first()
    if Package.objects.filter(sender_iid=iid) or Package.objects.filter(receiver_iid=iid):
        return render(request, 'jumpage11.html',{'id':id})
    if request.method == "GET":
        return render(request, 'jumpage5.html', {'id': id})
    Identity.objects.filter(iid=iid).delete()
    return redirect(identity, id=id.uid)


def courierpage(request, id,page):  # 快递员界面
    fetched = Package.objects.filter(
        Q(courier_a_id=id,pick_time__isnull=True) | Q(courier_b_id=id, pick_time__isnull=True)).values('sender_id',
                                                                                                           'sender_iid',
                                                                                                           'receiver_iid',
                                                                                                           'receiver_id',
                                                                                                           'pid',
                                                                                                           'weight',
                                                                                                           'size',
                                                                                                           'pdeparture',
                                                                                                           'pdestination',
                                                                                                           'start_time',
                                                                                                           'courier_a_id',
                                                                                                           'courier_b_id',
                                                                                                       'station_id')
    target_loc = []
    names=[]
    phones=[]
    name = Courier.objects.filter(cid=id).first().cname
    paginator = Paginator(fetched, 10)
    currentpage = paginator.page(page)
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    for item in currentpage:
        if item['courier_a_id'] == int(id):
            sender_identity = Identity.objects.filter(iid=item['sender_iid']).first()
            loc = sender_identity.iaddress
            target_loc.append(loc)
            thisname=sender_identity.iname
            names.append(thisname)
            thisphone=sender_identity.iphone
            phones.append(thisphone)
        elif item['courier_b_id'] == int(id):
            sender_identity = Identity.objects.filter(iid=item['receiver_iid']).first()
            loc = Station.objects.filter(sid=item['station_id']).first().saddress
            target_loc.append(loc)
            thisname = sender_identity.iname
            names.append(thisname)
            thisphone = sender_identity.iphone
            phones.append(thisphone)
    return render(request, 'courierpage.html', {"fetched": zip(currentpage, target_loc,names,phones),'page_range':page_range, "id": int(id), "name": name})


def morepackages(request, id,page):  # 快递员接单界面
    location = Courier.objects.filter(cid=id).first().clocation
    tofetch = Package.objects.filter(
        Q(courier_a_id__isnull=True, pdeparture=location,status='未发货') | Q(courier_b_id__isnull=True, pdestination=location,status="运输中")).order_by('start_time').values(
        'sender_id','sender_iid','receiver_iid', 'receiver_id', 'pid', 'weight', 'size', 'pdeparture', 'pdestination', 'start_time', 'courier_a_id',
        'courier_b_id','station_id','status')
    name = Courier.objects.filter(cid=id).first().cname
    target_loc = []
    paginator = Paginator(tofetch, 10)
    currentpage = paginator.page(page)
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    for item in currentpage:
        if item['status']=='未发货' and item['pdeparture'] == location:
            sender_id = item['sender_iid']
            loc = Identity.objects.filter(iid=sender_id).first().iaddress
            target_loc.append(loc)
        else:
            rec_id = item['station_id']
            loc = Station.objects.filter(sid=rec_id).first().saddress
            target_loc.append(loc)
    return render(request, "morepackages.html",
                  {"tofetch": zip(currentpage, target_loc), "page_range":page_range,"id": int(id), "loc": location, "name": name})


def packageshist(request, id,page):  # 历史接单界面
    name = Courier.objects.filter(cid=id).first().cname
    hist = Package.objects.filter(Q(courier_a_id=id) | Q(courier_b_id=id),status='已收货').values('sender_id',
                                                                                  'sender_iid',
                                                                                  'receiver_iid',
                                                                                  'receiver_id', 'pid','station_id',
                                                                                  'weight', 'size', 'pdeparture',
                                                                                  'pdestination', 'start_time',
                                                                                  'courier_a_id', 'courier_b_id')
    target_loc = []
    paginator = Paginator(hist, 10)
    currentpage = paginator.page(page)
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    for item in currentpage:
        if item['courier_a_id'] == int(id):
            sender_id = item['sender_iid']
            loc = Identity.objects.filter(iid=sender_id).first().iaddress
            target_loc.append(loc)
        else:
            rec_id = item['station_id']
            loc = Station.objects.filter(sid=rec_id).first().saddress
            target_loc.append(loc)
    return render(request, "packageshist.html", {"hist": zip(currentpage, target_loc), 'page_range':page_range,"id": int(id), "name": name})


def courierpersonal(request, id):
    personal = Courier.objects.filter(cid=id).first()
    name = Courier.objects.filter(cid=id).first().cname
    salary = Courier.objects.filter(cid=id).first().csalary
    personal.clocation=Map.objects.filter(id=personal.clocation).first().district
    return render(request, "courierpersonal.html", {"item": personal, "id": int(id), "name": name})


def courierreceive(request):  # 接单操作
    pid = request.GET.get('pid')
    cid = request.GET.get('cid')
    flag = int(request.GET.get('door'))
    salary = Courier.objects.filter(cid=cid).first().csalary
    if flag:
            package=Package.objects.filter(pid=pid)
            if package.first().status=='未发货':
                package.update(courier_a_id=cid,send_time=timezone.now(),status='已发货')
                Courier.objects.filter(cid=cid).update(csalary=salary + 2)
            else:
                return HttpResponse('接单失败！请返回并刷新页面！')
    else:
            package=Package.objects.filter(pid=pid)
            if package.first().status=='运输中':
                Package.objects.filter(pid=pid).update(courier_b_id=cid,status='配送中')
                Courier.objects.filter(cid=cid).update(csalary=salary + 1)
            else:
                return HttpResponse('接单失败！请返回并刷新页面！')
    return HttpResponse('接单成功！请返回并刷新页面！')


def driverpage(request, id,page):  # 司机界面
    name = Driver.objects.filter(did=id).first().dname
    fetched = Package.objects.filter(driver_id=id, pick_time__isnull=True).values('station_id', 'pid', 'weight', 'size',
                                                                        'send_time')
    paginator = Paginator(fetched, 10)
    currentpage = paginator.page(page)
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'driverpage.html', {"fetched": fetched, "page_range":page_range, "id": int(id), "name": name})


def dmorepackages(request, id,page):  # 接单界面
    name = Driver.objects.filter(did=id).first().dname
    driver_dep = Driver.objects.filter(did=id).first().ddeparture
    driver_des = Driver.objects.filter(did=id).first().ddestination
    tofetch = Package.objects.filter(driver_id__isnull=True, status="已接单", pdeparture=driver_dep,
                                     pdestination=driver_des).order_by('start_time').values('station_id', 'pid', 'weight', 'size', 'send_time')
    paginator = Paginator(tofetch, 10)
    currentpage = paginator.page(page)
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'dmorepackages.html', {"name": name,"page_range":page_range, "tofetch": tofetch, "id": int(id)})


def driverpersonal(request, id):
    personal = Driver.objects.filter(did=id).first()
    personal.ddeparture=Map.objects.filter(id=personal.ddeparture).first().district
    personal.ddestination = Map.objects.filter(id=personal.ddestination).first().district
    return render(request, "driverpersonal.html", {"item": personal, "id": int(id)})


def dpackageshist(request, id,page):  # 历史行程
    name = Driver.objects.filter(did=id).first().dname
    temp = Package.objects.filter(driver_id=id).all()
    hist = temp.filter(~Q(status="运输中")).values('pid', 'weight', 'size', 'status', 'pdeparture', 'pdestination')
    paginator = Paginator(hist, 10)
    currentpage = paginator.page(page)
    for item in currentpage:
        item['pdeparture']=Map.objects.filter(id=item['pdeparture']).first().district
        item['pdestination']=Map.objects.filter(id=item['pdestination']).first().district
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, "dpackageshist.html", {"hist": currentpage,'page_range':page_range, "id": int(id), "name": name})


def driverreceive(request):  # 接单操作
    pid = request.GET.get('pid')
    did = request.GET.get('did')
    thedriver=Driver.objects.filter(did=did).first()
    salary = thedriver.dcompensation
    Package.objects.filter(pid=pid).update(driver_id=did,status='运输中')
    depacity=Map.objects.filter(id=thedriver.ddeparture).first().city
    destcity=Map.objects.filter(id=thedriver.ddestination).first().city
    if depacity!=destcity:
        Driver.objects.filter(did=did).update(dcompensation=salary + 1)
    return redirect(dmorepackages, id=did,page=1)


def changeplace(request, id):  # 切换地点
    placedep = Driver.objects.filter(did=id).first().ddeparture
    placedes = Driver.objects.filter(did=id).first().ddestination
    depadist = Map.objects.filter(id=placedep).first().district
    destdist = Map.objects.filter(id=placedes).first().district
    if request.method == "GET":
        return render(request, "changeplace.html", {"id": id, "dep": depadist, "des": destdist})
    newplace = request.POST.get("newplace")
    if newplace == destdist:
        Driver.objects.filter(did=id).update(ddeparture=placedes)
        Driver.objects.filter(did=id).update(ddestination=placedep)
        return render(request, "changeplace.html",
                      {"id": id, "dep": destdist, "des": depadist, "error_msg": "修改成功，祝您一路顺风！"})
    else:
        return render(request, "changeplace.html",
                      {"id": id, "dep": depadist, "des": destdist, "error_msg": "您没有到达指定目的地或输入了无效的地址信息！"})


def staffchange(request):  # 员工修改密码
    if request.method == "GET":
        return render(request, 'staffchange.html', context={"error_msg": ""})
    phone = request.POST.get("phone")
    origin = request.POST.get("origin_pass")
    new = request.POST.get("new_pass")
    new_confirm = request.POST.get("new_pass_confirm")
    if not StaffLogin.objects.filter(phone=phone).first():
        return render(request, 'staffchange.html', context={"error_msg": "该账号不存在！"})
    encode = StaffLogin.objects.filter(phone=phone).first().password
    if new == new_confirm:
        if check_password(origin, encode):
            new_encode = make_password(new)
            StaffLogin.objects.filter(phone=phone).update(password=new_encode)
            return render(request, 'jumpage7.html')
        else:
            return render(request, 'staffchange.html', context={"error_msg": "原密码输入错误！"})
    else:
        return render(request, 'staffchange.html', context={"error_msg": "新密码与再次输入不符！"})


def courierinfo(request, id, page=1):
    if request.method=='POST':
        courier=Courier.objects.filter(cid=request.POST.get('staff_id')).first()
        if courier:
            courier.clocation=[Map.objects.filter(id=courier.clocation).first().city,Map.objects.filter(id=courier.clocation).first().district]
        return render(request,'couriersearch.html',{'item':courier,'id':id})
    courier_list = Courier.objects.all()
    paginator = Paginator(courier_list, 10)
    currentpage = paginator.get_page(page)
    # 获取当前页码
    for item in currentpage:
        item.clocation = [Map.objects.filter(id=item.clocation).first().city,Map.objects.filter(id=item.clocation).first().district]
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'courierinfo.html',
                  {'courier': currentpage, "id": id, 'paginator': paginator, 'page_range': page_range})


def staffpay(request,id,type,sid,page):
    if request.method == "GET":
        if int(type)==1:
            driver=Driver.objects.filter(did=sid).first()
            name=driver.dname
            money=driver.dcompensation
            salary=driver.dsalary
            job='货车司机'
        else:
            courier = Courier.objects.filter(cid=sid).first()
            name = courier.cname
            money = courier.csalary
            salary=courier.cmoney
            job = '快递员'
        return render(request,'jumpage12.html',locals())
    if int(type) == 1:
        Driver.objects.filter(did=sid).update(dcompensation=0)
        return redirect(driverinfo,id=id,page=page)
    else:
        Courier.objects.filter(cid=sid).update(csalary=0)
        return redirect(courierinfo,id=id,page=page)


def driverinfo(request, id, page=1):
    if request.method=='POST':
        item = Driver.objects.filter(did=request.POST.get('staff_id')).first()
        if item:
            item.ddeparture = [Map.objects.filter(id=item.ddeparture).first().city,
                               Map.objects.filter(id=item.ddeparture).first().district]
            item.ddestination = [Map.objects.filter(id=item.ddestination).first().city,
                                 Map.objects.filter(id=item.ddestination).first().district]
        return render(request, 'driversearch.html', {'item': item, 'id': id})
    driver_list = Driver.objects.all()
    paginator = Paginator(driver_list, 10)
    currentpage = paginator.page(page)
    for item in currentpage:
        item.ddeparture=[Map.objects.filter(id=item.ddeparture).first().city,Map.objects.filter(id=item.ddeparture).first().district]
        item.ddestination = [Map.objects.filter(id=item.ddestination).first().city,
                           Map.objects.filter(id=item.ddestination).first().district]
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'driverinfo.html',
                  {'driver': currentpage, "id": id, 'paginator': paginator, 'page_range': page_range})


def managerinfo(request, id, page=1):
    if request.method=='POST':
        manager_list = Manager.objects.filter(mid=request.POST.get('staff_id')).all()
        loc_list = []
        for item in manager_list:
            loc = Station.objects.filter(sid=item.station_id).first().slocation
            loc = [Map.objects.filter(id=loc).first().city, Map.objects.filter(id=loc).first().district]
            loc_list.append(loc)
        return render(request, 'managersearch.html', {'manager': list(zip(manager_list,loc_list)), 'id': id})
    manager_list = Manager.objects.all()
    paginator = Paginator(manager_list, 10)
    currentpage = paginator.page(page)
    loc_list = []
    for item in currentpage:
        loc=Station.objects.filter(sid=item.station_id).first().slocation
        loc=[Map.objects.filter(id=loc).first().city,Map.objects.filter(id=loc).first().district]
        loc_list.append(loc)
    currentpagecontent = list(zip(currentpage,loc_list))
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'managerinfo.html',
                  {'manager': currentpagecontent, "id": id, 'paginator': paginator, 'page_range': page_range})


def packageinfo(request, id):
    mapdic = {}
    for city in Map.objects.values('city').distinct():
        mapdic[city['city']] = []
        for district in Map.objects.filter(city=city['city']).values('district'):
            mapdic[city['city']].append(district["district"])
    city = mapdic.keys()
    type = request.GET.get('type','')
    pid = request.GET.get('package_id','')
    thecity = request.GET.get('city','')
    district = request.GET.get('district','')
    if district =='不限制':
        district = ''
    status=request.GET.get('status','')
    page=request.GET.get('page',1)
    if not pid == '':
        packages=Package.objects.filter(pid=pid)
    elif not thecity == '':
        if not district == '':
            location = Map.objects.filter(city=thecity, district=district).first().id
            if type == '':
                if not status == '':
                    packages=Package.objects.filter(Q(pdeparture=location,status=status)|Q(pdestination=location,status=status)).order_by('-start_time')
                else:
                    packages = Package.objects.filter(Q(pdeparture=location) | Q(pdestination=location)).order_by(
                        '-start_time')
            if type == 'depa':
                if not status == '':
                    packages=Package.objects.filter(pdeparture=location,status=status).order_by('-start_time')
                else:
                    packages = Package.objects.filter(pdeparture=location).order_by(
                        '-start_time')
            if type == 'dest':
                if not status == '':
                    packages=Package.objects.filter(pdestination=location,status=status).order_by('-start_time')
                else:
                    packages = Package.objects.filter(pdestination=location).order_by(
                        '-start_time')
        else:
            cities = Map.objects.filter(city=thecity)
            if type =='':
                if status == '':
                    packages = Package.objects.filter(Q(pdeparture__in=list(cities.values_list('id',flat=True)))|Q(pdestination__in=list(cities.values_list('id',flat=True)))).order_by('-start_time')
                else:
                    packages=Package.objects.filter(Q(pdeparture__in=list(cities.values_list('id',flat=True)),status=status)|Q(pdestination__in=list(cities.values_list('id',flat=True)),status=status)).order_by('-start_time')
            if type =='depa':
                if status == '':
                    packages = Package.objects.filter(pdeparture__in=list(cities.values_list('id',flat=True))).order_by('-start_time')
                else:
                    packages=Package.objects.filter(pdeparture__in=list(cities.values_list('id',flat=True)),status=status).order_by('-start_time')
            if type =='dest':
                if status == '':
                    packages = Package.objects.filter(pdestination__in=list(cities.values_list('id',flat=True))).order_by('-start_time')
                else:
                    packages=Package.objects.filter(pdestination__in=list(cities.values_list('id',flat=True)),status=status).order_by('-start_time')
    elif not status=='':
        packages=Package.objects.filter(status=status).order_by('-start_time')
    else:
        packages = Package.objects.all().order_by('-start_time')
    paginator = Paginator(packages, 50)
    currentpage = paginator.page(page)
    for item in currentpage:
        item.pdeparture=[Map.objects.filter(id=item.pdeparture).first().city,Map.objects.filter(id=item.pdeparture).first().district]
        item.pdestination=[Map.objects.filter(id=item.pdestination).first().city,Map.objects.filter(id=item.pdestination).first().district]
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'packageinfo.html',
                  {'package': currentpage, "id": id, 'paginator': paginator, 'page_range': page_range,'waiting':1,'package_id':pid,'district':district,'thecity':thecity,'status':status,'map':mapdic,'city':city,'type':type})


def waitinginfo(request, id):
    mapdic = {}
    for city in Map.objects.values('city').distinct():
        mapdic[city['city']] = []
        for district in Map.objects.filter(city=city['city']).values('district'):
            mapdic[city['city']].append(district["district"])
    city = mapdic.keys()
    page=request.GET.get('page',1)
    type=request.GET.get('type','')
    pid = request.GET.get('package_id','')
    thecity = request.GET.get('city','')
    district=request.GET.get('district','')
    if district == '不限制':
        district = ''
    if not pid == '':
        packages = Package.objects.filter(pid=pid,status='已发货')
    elif not thecity == '':
        if not district == '':
            location = Map.objects.filter(city=thecity, district=district).first().id
            if type == '':
                packages = Package.objects.filter(Q(pdeparture=location,status='已发货') | Q(pdestination=location,status='已发货')).order_by(
                        'send_time')
            if type == 'depa':
                packages = Package.objects.filter(pdeparture=location,status='已发货').order_by(
                        'send_time')
            if type == 'dest':
                packages = Package.objects.filter(pdestination=location,status='已发货').order_by(
                        'send_time')
        else:
            cities = Map.objects.filter(city=thecity)
            if type == '':
                packages = Package.objects.filter(Q(pdeparture__in=list(cities.values_list('id', flat=True)),status='已发货') | Q(
                        pdestination__in=list(cities.values_list('id', flat=True)),status='已发货')).order_by('send_time')
            if type == 'depa':
                packages = Package.objects.filter(
                        pdeparture__in=list(cities.values_list('id', flat=True)),status='已发货').order_by('send_time')
            if type == 'dest':
                packages = Package.objects.filter(
                        pdestination__in=list(cities.values_list('id', flat=True)),status='已发货').order_by('send_time')
    else:
        packages = Package.objects.filter(status='已发货').order_by('send_time')
    paginator = Paginator(packages, 10)
    currentpage = paginator.page(page)
    for item in currentpage:
        item.pdeparture = [Map.objects.filter(id=item.pdeparture).first().city,
                       Map.objects.filter(id=item.pdeparture).first().district]
        item.pdestination=[Map.objects.filter(id=item.pdestination).first().city,Map.objects.filter(id=item.pdestination).first().district]
    currentr_page_num = currentpage.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return render(request, 'waitinginfo.html',
                  {'package': currentpage, "id": id, 'paginator': paginator, 'page_range': page_range,'waiting':0,'city':city,'map':mapdic,'thecity':thecity,'district':district,'type':type,'package_id':pid})


def packageedit(request,id,pid):
    if request.method == "GET":
        return render(request,'packageedit.html',locals())
    weight=request.POST.get('weight')
    size=request.POST.get('size')
    package=Package.objects.filter(pid=pid).first()
    departure=package.pdeparture
    destination=package.pdestination
    unit_price=Service.objects.filter(departure=departure,destination=destination).first().unit_price
    price=float(weight)*float(unit_price)
    package.weight=weight
    package.size=size
    package.send_time=timezone.now()
    package.status='已接单'
    package.express_price=price
    package.save()
    # Package.objects.filter(pid=pid).update(weight=,size=size,send_time=timezone.now(),status='已接单',express_price=price)
    return redirect(waitinginfo,id=id,page=1)


def packagedelete(request,id,pid):
    if request.method == "GET":
        package=Package.objects.filter(pid=pid).values('content','start_time','sender_iid').first()
        phone=Identity.objects.filter(iid=package['sender_iid']).first().iphone
        content=package['content']
        start_time=package['start_time']
        return render(request,'jumpage10.html',locals())
    Package.objects.filter(pid=pid).delete()
    return redirect(waitinginfo,id=id,page=1)


def addstaff(request, id):  # 添加人员
    if request.method == "GET":
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'addstaff.html', {'map': mapdic, 'city': city, 'error_msg': '', 'id': id})
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    salary = int(request.POST.get("salary"))
    who = request.POST.get("who")
    depacity = request.POST.get("depacity")
    depadist = request.POST.get('depadist')
    sex = request.POST.get("sex")
    if StaffLogin.objects.filter(phone=phone).first():
        mapdic = {}
        for city in Map.objects.values('city').distinct():
            mapdic[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                mapdic[city['city']].append(district["district"])
        city = mapdic.keys()
        return render(request, 'addstaff.html', {'map': mapdic, 'city': city, "error_msg": "该手机号或用户名已存在！", "id": id})
    if who == '1':
        dep = Map.objects.filter(city=depacity, district=depadist).first().id
        Courier.objects.create(cname=name, cphone=phone, cmoney=salary, clocation=dep, csex=sex, csalary=0)
        sid = Courier.objects.filter(cphone=phone).first().cid
        encode = make_password("123456")
        StaffLogin.objects.create(class_field=who, phone=phone, sid=sid, password=encode)
        return redirect(courierinfo, id=id, page=1)
    if who == '2':
        destcity = request.POST.get("destcity")
        destdist = request.POST.get("destdist")
        dep = Map.objects.filter(city=depacity, district=depadist).first().id
        des = Map.objects.filter(city=destcity, district=destdist).first().id
        Driver.objects.create(dname=name, dphone=phone, dsalary=salary, ddeparture=dep, ddestination=des, dsex=sex,dcompensation=0)
        sid = Driver.objects.filter(dphone=phone).first().did
        encode = make_password("123456")
        StaffLogin.objects.create(class_field=who, phone=phone, sid=sid, password=encode)
        return redirect(driverinfo, id=id, page=1)
    if who == '3':
        dep = Map.objects.filter(city=depacity, district=depadist).first().id
        station_id = Station.objects.filter(slocation=dep).first().sid
        Manager.objects.create(mname=name, mphone=phone, msalary=salary, station_id=station_id, msex=sex)
        sid = Manager.objects.filter(mphone=phone).first().mid
        encode = make_password("123456")
        StaffLogin.objects.create(class_field=who, phone=phone, sid=sid, password=encode)
        return redirect(managerinfo, id=id, page=1)


def deletestaff(request, id, sid, who):
    if request.method == 'GET':
        if who == "快递员":
            name = Courier.objects.filter(cid=sid).first().cname
        if who == "货车司机":
            name = Driver.objects.filter(did=sid).first().dname
        if who == "驿站管理员":
            name = Manager.objects.filter(mid=sid).first().mname
        return render(request, 'jumpage9.html', locals())
    StaffLogin.objects.filter(sid=sid, class_field=who).delete()
    if who == "快递员":
        Courier.objects.filter(cid=sid).delete()
        return redirect(courierinfo, id=id, page=1)
    if who == "货车司机":
        Driver.objects.filter(did=sid).delete()
        return redirect(driverinfo, id=id, page=1)
    if who == "驿站管理员":
        Manager.objects.filter(mid=sid).delete()
        return redirect(managerinfo, id=id, page=1)


def staffedit(request, sid, id, who):
    if request.method == "GET":
        map = {}
        for city in Map.objects.values('city').distinct():
            map[city['city']] = []
            for district in Map.objects.filter(city=city['city']).values('district'):
                map[city['city']].append(district["district"])
        city = map.keys()
        error_msg = ''
        if who == "快递员":
            person = Courier.objects.filter(cid=sid).first()
            name = person.cname
            phone = person.cphone
            sex = person.csex
            salary = person.cmoney
            dep = person.clocation
            location = Map.objects.filter(id=dep).first()
            depacity = location.city
            depadist = location.district
        if who == "货车司机":
            person = Driver.objects.filter(did=sid).first()
            name = person.dname
            phone = person.dphone
            sex = person.dsex
            salary = person.dsalary
            dep = person.ddeparture
            des = person.ddestination
            departure = Map.objects.filter(id=dep).first()
            destination = Map.objects.filter(id=des).first()
            depacity = departure.city
            depadist = departure.district
            destcity = destination.city
            destdist = destination.district
        if who == "驿站管理员":
            person = Manager.objects.filter(mid=sid).first()
            station_id = Manager.objects.filter(mid=sid).first().station_id
            location = Station.objects.filter(sid=station_id).first().slocation
            name = person.mname
            phone = person.mphone
            sex = person.msex
            salary = person.msalary
            dep = location
        return render(request, "staffedit.html", locals())
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    salary = int(request.POST.get("salary"))
    who = request.POST.get("who")
    depacity = request.POST.get("depacity")
    depadist = request.POST.get("depadist")
    dep = Map.objects.filter(city=depacity, district=depadist).first().id
    sex = request.POST.get("sex")
    if StaffLogin.objects.filter(phone=phone, sid=sid).first():
        pass
    elif StaffLogin.objects.filter(phone=phone).first():
        error_msg = "该手机号或用户名已存在！"
        return render(request, 'staffedit.html', locals())
    if who == '快递员':
        Courier.objects.filter(cid=sid).update(cname=name, cphone=phone, cmoney=salary, clocation=dep, csex=sex)
        StaffLogin.objects.filter(sid=sid, class_field=who).update(class_field=who, phone=phone)
        return render(request, 'jumpage8.html', {'who': who, 'id': id})
    if who == '货车司机':
        destcity = request.POST.get("destcity")
        destdist = request.POST.get('destdist')
        if depacity == None or depadist == None:
            map = {}
            for city in Map.objects.values('city').distinct():
                map[city['city']] = []
                for district in Map.objects.filter(city=city['city']).values('district'):
                    map[city['city']].append(district["district"])
            city = map.keys()
            person = Driver.objects.filter(did=sid).first()
            name = person.dname
            phone = person.dphone
            sex = person.dsex
            salary = person.dsalary
            dep = person.ddeparture
            des = person.ddestination
            departure = Map.objects.filter(id=dep).first()
            destination = Map.objects.filter(id=des).first()
            depacity = departure.city
            depadist = departure.district
            destcity = destination.city
            destdist = destination.district
            error_msg = '请选择地区'
            return render(request, "staffedit.html", locals())
        des = Map.objects.filter(city=destcity, district=destdist).first().id
        Driver.objects.filter(did=sid).update(dname=name, dphone=phone, dsalary=salary, ddeparture=dep,
                                              ddestination=des, dsex=sex)
        StaffLogin.objects.filter(sid=sid, class_field=who).update(class_field=who, phone=phone)
        return render(request, 'jumpage8.html', {'who': who, 'id': id})
    if who == '驿站管理员':
        station_id = Station.objects.filter(slocation=dep).first().sid
        Manager.objects.filter(mid=sid).update(mname=name, mphone=phone, msalary=salary, station_id=station_id,
                                               msex=sex)
        StaffLogin.objects.filter(sid=sid, class_field=who).update(class_field=who, phone=phone)
        return render(request, 'jumpage8.html', {'who': who, 'id': id})


def adminlogin(request):  # 超管登录
    if request.method == "GET":
        return render(request, "adminlogin.html", context={"error_msg": ""})
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    if not StaffLogin.objects.filter(phone=phone).first():
        return render(request, 'adminlogin.html', context={"error_msg": "您没有账号，请先申请"})
    encoded = StaffLogin.objects.filter(phone=phone).first().password
    id = StaffLogin.objects.filter(phone=phone).first().sid
    if encoded and check_password(password, encoded) and StaffLogin.objects.filter(
            phone=phone).first().class_field == '超管':
        expire_bound = timezone.now() - datetime.timedelta(days=60)
        Package.objects.filter(pick_time__lt=expire_bound).all().delete()
        return redirect(courierinfo, id=id,page=1)
    else:
        return render(request, 'adminlogin.html', context={"error_msg": "用户名或密码有误"})
