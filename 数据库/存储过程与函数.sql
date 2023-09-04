DROP PROCEDURE IF EXISTS `receiver_view`;
DROP PROCEDURE IF EXISTS `sender_view`;
DROP PROCEDURE IF EXISTS `Service_Map`;
DROP PROCEDURE IF EXISTS `station_arrangement`;
DROP PROCEDURE IF EXISTS `station_pricing`;
DROP FUNCTION IF EXISTS `time_price`;
DELIMITER $$
CREATE PROCEDURE `receiver_view`(
    in myid int
)
begin
    
    select pid,content,iname,iphone,status,depacity,
    depadist, destcity,destdist,cname,cphone,
    arrival_time,saddress,pick_id,picker_id,station_price,expected_time from (select pid,content,identity.iname,identity.iphone,status,map.city as depacity,
    map.district as depadist,start_time,courier.cname,courier.cphone,
    arrival_time,station.saddress,pick_id,picker_id,pick_time,station_price,expected_time from (select * from package where receiver_id=myid) as mypackage
    left join map on pdeparture=map.id left join identity on sender_iid=identity.iid left join courier on courier_b_id=courier.cid left join station on station_id=station.sid)as depart 
    natural join (select pid,map.city as destcity,map.district as destdist from (select * from package where receiver_id=myid) as mypackage left join map on pdestination=map.id) as destin order by pid desc;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `sender_view`(
    in myid int
)
begin
    select pid, content,iname, iphone, status, depacity,depadist, destcity,destdist, express_price, start_time, courier_a_phone, pick_time,courier_b_phone,expected_time from (select pid, content,identity.iname, identity.iphone, status, map.city as depacity,map.district as depadist,express_price, start_time, courier.cname as courier_a_name, courier.cphone as courier_a_phone, expected_time,pick_time
    from (select * from package where sender_id=myid)as mypackage left join identity on receiver_iid=identity.iid left join map on pdeparture=map.id left join courier on courier_a_id=courier.cid)as courier_a_and_others
    natural join (select pid, courier.cname as courier_b_name, courier.cphone as courier_b_phone from (select * from package where sender_id=myid)as mypackage left join courier on courier_b_id=courier.cid)as courier_b 
    natural join (select pid,map.city as destcity,map.district as destdist from (select * from package where sender_id=myid) as mypackage left join map on pdestination=map.id) as dest order by pid desc;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `Service_Map`()
BEGIN
update service set 
duration=24+st_distance(point((select latitude from map where id=destination),
(select longitude from map where id=destination)),
point((select latitude from map where id=departure),
(select longitude from map where id=departure)))*5,
unit_price=5+ceiling(st_distance(point((select latitude from map where id=destination),
(select longitude from map where id=destination)),
point((select latitude from map where id=departure),
(select longitude from map where id=departure)))/10) 
where departure>=0 and destination>=0;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `station_arrangement`(
    in mysid int,
    in myp int,
    out shelf_num int,
    out layor_num int
)
begin
    declare mysize float;
    select size into mysize from package where pid=myp;
    case
    when mysize<0.5 then
    select shelf,layor into shelf_num,layor_num from store 
    where (layor=1 or layor=2) and station_id=mysid order by num limit 1;
    when mysize>1 then
    select shelf,layor into shelf_num,layor_num from store
    where station_id=mysid and (layor=3 or layor=4) order by num limit 1;
    else
    select shelf,layor into shelf_num,layor_num from store
    where station_id=mysid and (layor=5 or layor=6) order by num limit 1;
    end case;
    update package set arrival_time=now(), shelf=shelf_num, layor=layor_num, pick_id=concat(shelf_num,'-',layor_num,'-',ceiling(rand()*9000+1000)),picker_id=ceiling(rand()*9000000),status="已到站" where pid=myp;
    select shelf_num,layor_num;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `station_pricing`(
    in id int,
    out price float
)
begin
    declare t1 datetime;
    declare t2 datetime;
    update package set pick_time=now(),shelf=null,layor=null,status="已收货" where pid=id;
    select arrival_time,pick_time into t1,t2 from package where pid=id;
    set price=time_price(t1,t2);
    update package set station_price=price where pid=id;
    select arrival_time,pick_time,station_price from package where pid=id;
end$$
DELIMITER ;
DROP PROCEDURE IF EXISTS `receiver_view`;
DROP PROCEDURE IF EXISTS `sender_view`;
DROP PROCEDURE IF EXISTS `Service_Map`;
DROP PROCEDURE IF EXISTS `station_arrangement`;
DROP PROCEDURE IF EXISTS `station_pricing`;
DELIMITER $$
CREATE PROCEDURE `receiver_view`(
    in myid int
)
begin
    
    select pid,content,iname,iphone,status,depacity,
    depadist, destcity,destdist,cname,cphone,
    arrival_time,saddress,pick_id,picker_id,station_price,expected_time from (select pid,content,identity.iname,identity.iphone,status,map.city as depacity,
    map.district as depadist,start_time,courier.cname,courier.cphone,
    arrival_time,station.saddress,pick_id,picker_id,pick_time,station_price,expected_time from (select * from package where receiver_id=myid) as mypackage
    left join map on pdeparture=map.id left join identity on sender_iid=identity.iid left join courier on courier_b_id=courier.cid left join station on station_id=station.sid)as depart 
    natural join (select pid,map.city as destcity,map.district as destdist from (select * from package where receiver_id=myid) as mypackage left join map on pdestination=map.id) as destin order by pid desc;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `sender_view`(
    in myid int
)
begin
    select pid, content,iname, iphone, status, depacity,depadist, destcity,destdist, express_price, start_time, courier_a_phone, pick_time,courier_b_phone,expected_time from (select pid, content,identity.iname, identity.iphone, status, map.city as depacity,map.district as depadist,express_price, start_time, courier.cname as courier_a_name, courier.cphone as courier_a_phone, expected_time,pick_time
    from (select * from package where sender_id=myid)as mypackage left join identity on receiver_iid=identity.iid left join map on pdeparture=map.id left join courier on courier_a_id=courier.cid)as courier_a_and_others
    natural join (select pid, courier.cname as courier_b_name, courier.cphone as courier_b_phone from (select * from package where sender_id=myid)as mypackage left join courier on courier_b_id=courier.cid)as courier_b 
    natural join (select pid,map.city as destcity,map.district as destdist from (select * from package where sender_id=myid) as mypackage left join map on pdestination=map.id) as dest order by pid desc;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `Service_Map`()
BEGIN
update service set 
duration=24+st_distance(point((select latitude from map where id=destination),
(select longitude from map where id=destination)),
point((select latitude from map where id=departure),
(select longitude from map where id=departure)))*5,
unit_price=5+ceiling(st_distance(point((select latitude from map where id=destination),
(select longitude from map where id=destination)),
point((select latitude from map where id=departure),
(select longitude from map where id=departure)))/10) 
where departure>=0 and destination>=0;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `station_arrangement`(
    in mysid int,
    in myp int,
    out shelf_num int,
    out layor_num int
)
begin
    declare mysize float;
    select size into mysize from package where pid=myp;
    case
    when mysize<0.5 then
    select shelf,layor into shelf_num,layor_num from store 
    where (layor=1 or layor=2) and station_id=mysid order by num limit 1;
    when mysize>1 then
    select shelf,layor into shelf_num,layor_num from store
    where station_id=mysid and (layor=3 or layor=4) order by num limit 1;
    else
    select shelf,layor into shelf_num,layor_num from store
    where station_id=mysid and (layor=5 or layor=6) order by num limit 1;
    end case;
    update package set arrival_time=now(), shelf=shelf_num, layor=layor_num, pick_id=concat(shelf_num,'-',layor_num,'-',ceiling(rand()*9000+1000)),picker_id=ceiling(rand()*9000000),status="已到站" where pid=myp;
    select shelf_num,layor_num;
end$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `station_pricing`(
    in id int,
    out price float
)
begin
    declare t1 datetime;
    declare t2 datetime;
    update package set pick_time=now(),shelf=null,layor=null,status="已收货" where pid=id;
    select arrival_time,pick_time into t1,t2 from package where pid=id;
    set price=time_price(t1,t2);
    update package set station_price=price where pid=id;
    select arrival_time,pick_time,station_price from package where pid=id;
end$$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION `time_price`(
    t1 datetime,
    t2 datetime) RETURNS float
    READS SQL DATA
BEGIN
    declare d float;
    declare m float;
    set d = timestampdiff(hour,t1,t2);
    if d > 12 then set m = (d-12.0)/2.0;
      else set m = 0;
    end if;
    if m>5 then set m=5;
    end if;
    return m;
end$$
DELIMITER ;

