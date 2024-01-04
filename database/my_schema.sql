-- MySQL dump 10.13  Distrib 8.2.0, for Win64 (x86_64)
--
-- Host: localhost    Database: my_schema
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bluetooth`
--

DROP TABLE IF EXISTS `bluetooth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bluetooth` (
  `ID` varchar(256) NOT NULL,
  `MAC` varchar(80) NOT NULL,
  `RSSI` int DEFAULT NULL,
  PRIMARY KEY (`ID`,`MAC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bluetooth`
--

LOCK TABLES `bluetooth` WRITE;
/*!40000 ALTER TABLE `bluetooth` DISABLE KEYS */;
INSERT INTO `bluetooth` VALUES ('8w9ts6NaKS1ykxp','49:53:23:c4:35:8e',-54),('8w9ts6NaKS1ykxp','63:32:a7:be:e0:30',-63),('8w9ts6NaKS1ykxp','6a:04:5b:be:da:df',-63),('eoChryHTO7DZVj7','49:53:23:c4:35:8e',-70),('eoChryHTO7DZVj7','6a:04:5b:be:da:df',-54),('eoChryHTO7DZVj7','cc:db:a7:e6:44:ba',-53),('LJp4JOzMHkkz4LS','49:53:23:c4:35:8e',-63),('LJp4JOzMHkkz4LS','6a:04:5b:be:da:df',-54),('tBwmH8L5d9lYMqO','49:53:23:c4:35:8e',-63),('tBwmH8L5d9lYMqO','63:32:a7:be:e0:30',-55),('tBwmH8L5d9lYMqO','6a:04:5b:be:da:df',-55),('tBwmH8L5d9lYMqO','cc:db:a7:e6:44:ba',-58);
/*!40000 ALTER TABLE `bluetooth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `magnetic_field`
--

DROP TABLE IF EXISTS `magnetic_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `magnetic_field` (
  `ID` varchar(256) NOT NULL,
  `X` double DEFAULT NULL,
  `Y` double DEFAULT NULL,
  `Z` double DEFAULT NULL,
  `M` double DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `magnetic_field`
--

LOCK TABLES `magnetic_field` WRITE;
/*!40000 ALTER TABLE `magnetic_field` DISABLE KEYS */;
INSERT INTO `magnetic_field` VALUES ('8w9ts6NaKS1ykxp',549.477054192516,-1366.668953012914,2153.454130048267,2609.0369392623475),('eoChryHTO7DZVj7',569.1929908805162,-1374.776714576914,2156.589736704267,2620.089877898959),('LJp4JOzMHkkz4LS',573.8523451745164,-1362.9312458929137,2171.9864394662673,2627.6250090754684),('tBwmH8L5d9lYMqO',526.8279856105163,-1345.6747399689139,2149.539998134267,2590.156450060865);
/*!40000 ALTER TABLE `magnetic_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measure`
--

DROP TABLE IF EXISTS `measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measure` (
  `Token` varchar(256) NOT NULL,
  `PointID` varchar(256) NOT NULL,
  PRIMARY KEY (`Token`,`PointID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measure`
--

LOCK TABLES `measure` WRITE;
/*!40000 ALTER TABLE `measure` DISABLE KEYS */;
INSERT INTO `measure` VALUES ('77ce5c714f444016908b1ba927b2e4cc_Misura40_20240104','8w9ts6NaKS1ykxp'),('77ce5c714f444016908b1ba927b2e4cc_Misura40_20240104','eoChryHTO7DZVj7'),('77ce5c714f444016908b1ba927b2e4cc_Misura40_20240104','LJp4JOzMHkkz4LS'),('77ce5c714f444016908b1ba927b2e4cc_Misura40_20240104','tBwmH8L5d9lYMqO');
/*!40000 ALTER TABLE `measure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `point`
--

DROP TABLE IF EXISTS `point`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `point` (
  `ID` varchar(256) NOT NULL,
  `CoordX` int DEFAULT NULL,
  `CoordY` int DEFAULT NULL,
  `Long` decimal(9,6) DEFAULT NULL,
  `Lat` decimal(8,6) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `point`
--

LOCK TABLES `point` WRITE;
/*!40000 ALTER TABLE `point` DISABLE KEYS */;
INSERT INTO `point` VALUES ('8w9ts6NaKS1ykxp',933,269,15.020367,37.612276),('eoChryHTO7DZVj7',813,288,15.020331,37.612266),('LJp4JOzMHkkz4LS',949,332,15.020372,37.612242),('tBwmH8L5d9lYMqO',876,351,15.020350,37.612232);
/*!40000 ALTER TABLE `point` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wifi`
--

DROP TABLE IF EXISTS `wifi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wifi` (
  `ID` varchar(256) NOT NULL,
  `SSID` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Channel` int DEFAULT NULL,
  `Frequency` varchar(45) DEFAULT NULL,
  `Quality` varchar(45) DEFAULT NULL,
  `RSSI` int DEFAULT NULL,
  PRIMARY KEY (`ID`,`Address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wifi`
--

LOCK TABLES `wifi` WRITE;
/*!40000 ALTER TABLE `wifi` DISABLE KEYS */;
INSERT INTO `wifi` VALUES ('8w9ts6NaKS1ykxp','Vodafone-A44331756','14:14:59:5B:62:2C',2,'2.417 GHz','30/70',-80),('8w9ts6NaKS1ykxp','WiFi-deco','40:ED:00:3A:E7:FA',7,'2.442 GHz','44/70',-66),('8w9ts6NaKS1ykxp','WiFi-deco','40:ED:00:3A:E7:FB',36,'5.18 GHz','42/70',-68),('8w9ts6NaKS1ykxp','WiFi-deco','40:ED:00:3A:E8:8A',7,'2.442 GHz','51/70',-59),('8w9ts6NaKS1ykxp','WiFi-deco','40:ED:00:3A:E8:8B',36,'5.18 GHz','37/70',-73),('8w9ts6NaKS1ykxp','','46:ED:00:3A:E7:FA',7,'2.442 GHz','44/70',-66),('8w9ts6NaKS1ykxp','','46:ED:00:3A:E7:FB',36,'5.18 GHz','42/70',-68),('8w9ts6NaKS1ykxp','','46:ED:00:3A:E8:8A',7,'2.442 GHz','52/70',-58),('8w9ts6NaKS1ykxp','','46:ED:00:3A:E8:8B',36,'5.18 GHz','36/70',-74),('8w9ts6NaKS1ykxp','POCO F3','4A:94:8A:18:A6:B7',7,'2.442 GHz','62/70',-48),('8w9ts6NaKS1ykxp','VodafoneMobileWiFi-B9C9C1','60:32:B1:BE:C1:69',2,'2.417 GHz','37/70',-73),('8w9ts6NaKS1ykxp','ibes2','62:32:B1:9E:C1:69',2,'2.417 GHz','34/70',-76),('8w9ts6NaKS1ykxp','','62:32:B1:AE:C1:69',2,'2.417 GHz','33/70',-77),('8w9ts6NaKS1ykxp','ABB-24-7d-4d-58-79-b7','90:9A:77:EC:3C:61',1,'2.412 GHz','26/70',-84),('8w9ts6NaKS1ykxp','TIM-69266544','D6:43:68:60:91:B6',11,'2.462 GHz','29/70',-81),('8w9ts6NaKS1ykxp','VodafoneMobileWiFi-B9C9C1-2G','E0:E1:A9:80:61:67',2,'2.417 GHz','34/70',-76),('eoChryHTO7DZVj7','Vodafone-A44331756','14:14:59:5B:62:2C',2,'2.417 GHz','32/70',-78),('eoChryHTO7DZVj7','WiFi-deco','40:ED:00:3A:E7:FA',7,'2.442 GHz','44/70',-66),('eoChryHTO7DZVj7','WiFi-deco','40:ED:00:3A:E7:FB',36,'5.18 GHz','36/70',-74),('eoChryHTO7DZVj7','WiFi-deco','40:ED:00:3A:E8:8A',7,'2.442 GHz','53/70',-57),('eoChryHTO7DZVj7','WiFi-deco','40:ED:00:3A:E8:8B',36,'5.18 GHz','39/70',-71),('eoChryHTO7DZVj7','','46:ED:00:3A:E7:FA',7,'2.442 GHz','44/70',-66),('eoChryHTO7DZVj7','','46:ED:00:3A:E8:8A',7,'2.442 GHz','52/70',-58),('eoChryHTO7DZVj7','POCO F3','4A:94:8A:18:A6:B7',7,'2.442 GHz','63/70',-47),('eoChryHTO7DZVj7','VodafoneMobileWiFi-B9C9C1','60:32:B1:BE:C1:69',2,'2.417 GHz','33/70',-77),('eoChryHTO7DZVj7','ibes2','62:32:B1:9E:C1:69',2,'2.417 GHz','32/70',-78),('eoChryHTO7DZVj7','','62:32:B1:AE:C1:69',2,'2.417 GHz','34/70',-76),('eoChryHTO7DZVj7','VodafoneMobileWiFi-B9C9C1-2G','E0:E1:A9:80:61:67',2,'2.417 GHz','38/70',-72),('LJp4JOzMHkkz4LS','Vodafone-A44331756','14:14:59:5B:62:2C',2,'2.417 GHz','30/70',-80),('LJp4JOzMHkkz4LS','WiFi-deco','40:ED:00:3A:E7:FA',7,'2.442 GHz','43/70',-67),('LJp4JOzMHkkz4LS','WiFi-deco','40:ED:00:3A:E7:FB',36,'5.18 GHz','42/70',-68),('LJp4JOzMHkkz4LS','WiFi-deco','40:ED:00:3A:E8:8A',7,'2.442 GHz','52/70',-58),('LJp4JOzMHkkz4LS','WiFi-deco','40:ED:00:3A:E8:8B',36,'5.18 GHz','37/70',-73),('LJp4JOzMHkkz4LS','','46:ED:00:3A:E7:FA',7,'2.442 GHz','44/70',-66),('LJp4JOzMHkkz4LS','','46:ED:00:3A:E7:FB',36,'5.18 GHz','42/70',-68),('LJp4JOzMHkkz4LS','','46:ED:00:3A:E8:8A',7,'2.442 GHz','52/70',-58),('LJp4JOzMHkkz4LS','POCO F3','4A:94:8A:18:A6:B7',7,'2.442 GHz','63/70',-47),('LJp4JOzMHkkz4LS','VodafoneMobileWiFi-B9C9C1','60:32:B1:BE:C1:69',2,'2.417 GHz','35/70',-75),('LJp4JOzMHkkz4LS','ibes2','62:32:B1:9E:C1:69',2,'2.417 GHz','35/70',-75),('LJp4JOzMHkkz4LS','','62:32:B1:AE:C1:69',2,'2.417 GHz','33/70',-77),('LJp4JOzMHkkz4LS','ABB-24-7d-4d-58-79-b7','90:9A:77:EC:3C:61',1,'2.412 GHz','26/70',-84),('LJp4JOzMHkkz4LS','TIM-69266544','D6:43:68:60:91:B6',11,'2.462 GHz','29/70',-81),('LJp4JOzMHkkz4LS','VodafoneMobileWiFi-B9C9C1-2G','E0:E1:A9:80:61:67',2,'2.417 GHz','36/70',-74),('tBwmH8L5d9lYMqO','Vodafone-A44331756','14:14:59:5B:62:2C',2,'2.417 GHz','32/70',-78),('tBwmH8L5d9lYMqO','WiFi-deco','40:ED:00:3A:E7:FA',7,'2.442 GHz','43/70',-67),('tBwmH8L5d9lYMqO','WiFi-deco','40:ED:00:3A:E7:FB',36,'5.18 GHz','41/70',-69),('tBwmH8L5d9lYMqO','WiFi-deco','40:ED:00:3A:E8:8A',7,'2.442 GHz','56/70',-54),('tBwmH8L5d9lYMqO','WiFi-deco','40:ED:00:3A:E8:8B',36,'5.18 GHz','41/70',-69),('tBwmH8L5d9lYMqO','','46:ED:00:3A:E7:FA',7,'2.442 GHz','42/70',-68),('tBwmH8L5d9lYMqO','','46:ED:00:3A:E8:8A',7,'2.442 GHz','52/70',-58),('tBwmH8L5d9lYMqO','POCO F3','4A:94:8A:18:A6:B7',7,'2.442 GHz','63/70',-47),('tBwmH8L5d9lYMqO','VodafoneMobileWiFi-B9C9C1','60:32:B1:BE:C1:69',2,'2.417 GHz','34/70',-76),('tBwmH8L5d9lYMqO','ibes2','62:32:B1:9E:C1:69',2,'2.417 GHz','34/70',-76),('tBwmH8L5d9lYMqO','','62:32:B1:AE:C1:69',2,'2.417 GHz','33/70',-77),('tBwmH8L5d9lYMqO','VodafoneMobileWiFi-B9C9C1-2G','E0:E1:A9:80:61:67',2,'2.417 GHz','37/70',-73);
/*!40000 ALTER TABLE `wifi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-04 16:18:25
