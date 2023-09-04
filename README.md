# Express-Logistics-System
Based on Django and MySQL, a deployable website featuring delivery management, temporary storage and user interface.

# 系统安装部署说明
环境需求：需要安装 Python 与 MySQL 的最新版本。Python 需要安装 Django,folium,pandas
宏包。数据库搭建：在 MySQL 平台运行数据库文件夹中的 sql 文件，创建数据库‘express’的
表结构，通过 csv 导入模拟数据。也可直接将 express 表复制到本地 MySQL 数据文件夹中并重
启 MySQL 服务。预设调整：在路径“/物流公司系统/物流公司系统”下的 setting.py 文件中，将
DATABASES 下的’USER’、’PASSWORD’、’HOST’ 及’PORT’改为运行主机的 MySQL 实例配
置（账户要有 express 表的所有权限）。TIME_ZONE 的属性改为公司当前所在地。在路径“/物
流公司系统/app01”下的 views.py 文件中，将视图 depaheatmap 和 destheatmap 下的 file_path
改为运行主机该项目的 templates 路径。 服务器启动：在 Python 平台运行 Django 项目‘物流
公司系统’，或在物流公司系统项目下输入指令’python manage.py runserver‘，便可部署系统。默
认的 IP 地址为 127.0.0.1，端口为 8000。
