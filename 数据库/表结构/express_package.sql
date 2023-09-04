CREATE DATABASE  IF NOT EXISTS `express` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `express`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: express
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `package`
--

DROP TABLE IF EXISTS `package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `package` (
  `pid` int NOT NULL AUTO_INCREMENT COMMENT '物流号',
  `weight` int DEFAULT NULL COMMENT '包裹重量',
  `size` int DEFAULT NULL COMMENT '包裹体积',
  `content` varchar(16) NOT NULL COMMENT '包裹内容',
  `sender_id` int NOT NULL COMMENT '发件人ID',
  `receiver_id` int NOT NULL COMMENT '收件人ID',
  `pdeparture` varchar(16) NOT NULL COMMENT '包裹出发地',
  `pdestination` varchar(16) NOT NULL COMMENT '包裹目的地',
  `start_time` datetime NOT NULL COMMENT '创建时间',
  `courier_a_id` int DEFAULT NULL COMMENT '上门取件快递员工号',
  `send_time` datetime DEFAULT NULL COMMENT '发货时间',
  `driver_id` int DEFAULT NULL COMMENT '货车司机工号',
  `courier_b_id` int DEFAULT NULL COMMENT '配送快递员工号',
  `station_id` int DEFAULT NULL COMMENT '寄存驿站编号',
  `arrival_time` datetime DEFAULT NULL COMMENT '到站时间',
  `shelf` int DEFAULT NULL COMMENT '存放货架号',
  `layor` int DEFAULT NULL COMMENT '存放层号',
  `pick_id` varchar(10) DEFAULT NULL COMMENT '取件码',
  `picker_id` char(11) DEFAULT NULL COMMENT '身份码',
  `pick_time` datetime DEFAULT NULL COMMENT '出站时间',
  `status` enum('未发货','已发货','已接单','运输中','配送中','已到站','已收货') NOT NULL DEFAULT '未发货' COMMENT '物流状态',
  `station_price` float DEFAULT NULL,
  `express_price` float DEFAULT NULL,
  `sender_iid` int NOT NULL,
  `receiver_iid` int NOT NULL,
  `expected_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `sender_index` (`sender_id`),
  KEY `receiver_index` (`receiver_id`),
  KEY `departure_index` (`pdeparture`),
  KEY `destination_index` (`pdestination`),
  KEY `courier_a_index` (`courier_a_id`),
  KEY `driver_index` (`driver_id`),
  KEY `station_index` (`station_id`),
  KEY `iid` (`sender_iid`) /*!80000 INVISIBLE */,
  KEY `iiid` (`receiver_iid`),
  CONSTRAINT `package_chk_1` CHECK ((`weight` < 100000)),
  CONSTRAINT `package_chk_2` CHECK ((`size` < 100000))
) ENGINE=InnoDB AUTO_INCREMENT=10015 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `store_count` AFTER UPDATE ON `package` FOR EACH ROW IF NOT (NEW.layor <=> OLD.layor AND NEW.shelf <=> OLD.shelf) THEN
    IF (NEW.layor <=> NULL) THEN
        UPDATE store SET num = num - 1 
        WHERE store.station_id = OLD.station_id AND store.layor = OLD.layor AND store.shelf = OLD.shelf;
	ELSE
        UPDATE store SET num = num + 1
        WHERE store.station_id = NEW.station_id AND store.layor = NEW.layor AND store.shelf = NEW.shelf;
	END IF;
END IF */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-06 12:27:23
