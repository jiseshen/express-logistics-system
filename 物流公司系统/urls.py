"""物流公司系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),#管理员页面
    path('',views.main,name='homepage'),#主页
    path('custom/service/',views.customservice,name='custom_service'),#时效查询
    path('custom/station/',views.customstation,name='custom_station'),#驿站查询
    path('user/login/',views.userlogin,name='user_login'),#用户登录
    path('user/register/',views.userregister,name='user_register'),#用户注册
    path('user/identity/(?<id>[0-9]{4})',views.identity,name='identity'),#用户身份
    path('user/identity/add/(?<id>[0-9]{4})',views.identityregister,name='identity_register'),#用户新建身份
    path('user/identity/edit/(?<iid>[0-9]{4}',views.identityedit,name='identity_edit'),#用户编辑身份
    path('user/identity/delete/(?<iid>[0-9]{4}',views.identitydelete,name='identity_delete'),#用户删除身份
    path('admin/courier/',views.courierinfo,name='courier_info'),#管理员工信息
    path('user/page/(?<id>[0-9]{4})/<role>/<page>',views.userpage,name='user_page'),#用户界面
    path('user/change/(?<id>[0-9]{4})',views.userchange,name='user_change'),#用户修改密码
    path('user/send/(?<id>[0-9]{4})',views.usersend,name='user_send'),#订单发起
    path('station/page/(?<myid>[0-9]{4})/(?<id>[0-9]{4})/<type>/<page>',views.stationpage,name='station_page'),#驿站管理界面
    path('station/store/(?<myid>[0-9]{4})/(?<sid>[0-9]{4})/<pid>',views.stationstore,name='station_store'),#驿站存放界面
    path('station/check/(?<myid>[0-9]{4})/(?<sid>[0-9]{4})/<pid>',views.stationcheck,name='station_check'),#驿站核查界面
    path('station/pick/(?<myid>[0-9]{4})/(?<sid>[0-9]{4})/<pid>',views.stationpick,name='station_pick'),#驿站结算界面
    path('staff/login/',views.stafflogin,name="staff_login"),#员工登录
    path('staff/courierpage/(?P<id>[0-9]{4})/<page>', views.courierpage, name='courier_page'),  # 快递员界面
    path('staff/courierpage/morepackages/(?P<id>[0-9]{4})/<page>', views.morepackages, name='more_packages'),  # 继续接单
    path('staff/courierpage/packageshist/(?P<id>[0-9]{4})/<page>', views.packageshist, name='packages_hist'),  # 历史包裹
    path('staff/courierpage/courierpersonal/(?P<id>[0-9]{4}', views.courierpersonal, name='courier_personal'), # 快递员个人信息
    path('staff/courierpage/courierreceive/', views.courierreceive, name="courier_receive"),  # 快递员接收包裹
    path('staff/driverpage/(?P<id>[0-9]{4})/<page>', views.driverpage, name="driver_page"),  # 司机界面
    path('staff/driverpage/dmorepackages/(?P<id>[0-9]{4})/<page>', views.dmorepackages, name="dmore_packages"),  # 司机，继续接单
    path('staff/driverpage/driverpersonal/(?P<id>[0-9]{4}', views.driverpersonal, name="driver_personal"),  # 司机个人信息
    path('staff/driverpage/dpackageshist/(?P<id>[0-9]{4})/<page>', views.dpackageshist, name='dpackages_hist'),  # 历史包裹
    path('staff/driverpage/driverreceive/', views.driverreceive, name="driver_receive"),  # 司机接收包裹
    path('staff/driverpage/changeplace/(?P<id>[0-9]{4}', views.changeplace, name="change_place"),  # 司机修改所在地
    path('staff/staffchange/', views.staffchange, name="staff_change"),  # 员工修改密码
    path('admin1/adminlogin/', views.adminlogin, name="admin_login"),  # 超管登录
    path('admin1/driverinfo/(?P<id>[0-9]{4})/<page>', views.driverinfo, name="driver_info"),  # 管理司机信息
    path('admin1/managerinfo/(?P<id>[0-9]{4})/<page>', views.managerinfo, name="manager_info"),  # 管理驿站管理员
    path('admin1/courierinfo/(?P<id>[0-9]{4})/<page>', views.courierinfo, name='courier_info'),  # 管理员工信息
    path('admin1/pay/(?P<id>[0-9]{4})/<type>/<sid>/<page>',views.staffpay,name='staff_pay'),#奖金/补贴结算
    path('admin1/packageinfo/(?P<id>[0-9]{4})', views.packageinfo, name='package_info'),  # 管理物流信息
    path('admin1/waitingpackage/(?P<id>[0-9]{4})',views.waitinginfo,name='waiting_info'), #待核验物流
    path('admin1/packageedit/(?P<id>[0-9]{4})/(?P<pid>[0-9]{4})',views.packageedit,name='package_edit'), #物流核验
    path('admin1/packagedelete/(?P<id>[0-9]{4})/(?P<pid>[0-9]{4})',views.packagedelete,name='package_delete'), #物流删除
    path('admin1/addstaff/(?P<id>[0-9]{4}', views.addstaff, name='add_staff'),  # 添加员工信息
    path('admin1/deletestaff/(?P<sid>[0-9]{4})/(?P<id>[0-9]{4})/<who>', views.deletestaff, name='delete_staff'),  # 删除员工
    path('admin1/staffedit/(?P<sid>[0-9]{4})/(?P<id>[0-9]{4})/<who>', views.staffedit, name='staff_edit'),  # 编辑员工
    path('heatmap/departure',views.depaheatmap,name='depature_heatmap'), # 出发地热力图
    path('heatmap/destination',views.destheatmap,name='destination_heatmap'), # 目的地热力图
]
