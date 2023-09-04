# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Courier(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=16)
    cphone = models.CharField(unique=True, max_length=11)
    clocation = models.IntegerField()
    csalary = models.IntegerField()
    cmoney = models.IntegerField()
    csex = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courier'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Driver(models.Model):
    did = models.AutoField(primary_key=True)
    dname = models.CharField(max_length=16)
    dphone = models.CharField(unique=True, max_length=11)
    ddeparture = models.CharField(max_length=16)
    ddestination = models.CharField(max_length=16)
    dsalary = models.IntegerField()
    dcompensation = models.IntegerField(blank=True, null=True)
    dsex = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver'


class Identity(models.Model):
    iid = models.AutoField(primary_key=True)
    iset = models.CharField(max_length=20)
    iphone = models.CharField(max_length=11)
    iaddress = models.CharField(max_length=200)
    ilocation = models.IntegerField()
    iname = models.CharField(max_length=20)
    uid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identity'
        unique_together = (('uid', 'iset'),)


class Manager(models.Model):
    mid = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=16)
    mphone = models.CharField(unique=True, max_length=11)
    station_id = models.IntegerField()
    msalary = models.IntegerField()
    msex = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager'


class Map(models.Model):
    district = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    latitude = models.CharField(max_length=45)
    longitude = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'map'
        unique_together = (('district', 'city'),)


class Package(models.Model):
    pid = models.AutoField(primary_key=True)
    weight = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=16)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    pdeparture = models.CharField(max_length=16)
    pdestination = models.CharField(max_length=16)
    start_time = models.DateTimeField()
    courier_a_id = models.IntegerField(blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    courier_b_id = models.IntegerField(blank=True, null=True)
    station_id = models.IntegerField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    shelf = models.IntegerField(blank=True, null=True)
    layor = models.IntegerField(blank=True, null=True)
    pick_id = models.CharField(max_length=10, blank=True, null=True)
    picker_id = models.CharField(max_length=11, blank=True, null=True)
    pick_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=3)
    station_price = models.FloatField(blank=True, null=True)
    express_price = models.FloatField(blank=True, null=True)
    sender_iid = models.IntegerField()
    receiver_iid = models.IntegerField()
    expected_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package'


class Service(models.Model):
    departure = models.IntegerField(primary_key=True)
    destination = models.IntegerField()
    duration = models.IntegerField()
    unit_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'service'
        unique_together = (('departure', 'destination'),)


class StaffLogin(models.Model):
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=200, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=5)  # Field renamed because it was a Python reserved word.
    sid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'staff_login'
        unique_together = (('sid', 'class_field'),)


class Station(models.Model):
    sid = models.AutoField(primary_key=True)
    slocation = models.IntegerField()
    saddress = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'station'


class Store(models.Model):
    lid = models.IntegerField(primary_key=True)
    station_id = models.IntegerField()
    shelf = models.IntegerField()
    layor = models.IntegerField()
    num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'store'
        unique_together = (('station_id', 'shelf', 'layor'),)


class UserLogin(models.Model):
    phone = models.CharField(primary_key=True, max_length=11)
    password = models.CharField(max_length=160, blank=True, null=True)
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_login'
