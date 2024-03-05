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
CREATE DATABASE IF NOT EXISTS my_schema;

USE my_schema;
--
-- Table structure for table `bluetooth`
--

DROP TABLE IF EXISTS `bluetooth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bluetooth` (
  `Token` varchar(256) NOT NULL,
  `PointID` varchar(256) NOT NULL,
  `MAC` varchar(45) NOT NULL,
  `RSSI` int DEFAULT NULL,
  PRIMARY KEY (`Token`,`PointID`,`MAC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bluetooth`
--

LOCK TABLES `bluetooth` WRITE;
/*!40000 ALTER TABLE `bluetooth` DISABLE KEYS */;
/*!40000 ALTER TABLE `bluetooth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `magnetic_field`
--

DROP TABLE IF EXISTS `magnetic_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `magnetic_field` (
  `Token` varchar(256) NOT NULL,
  `PointID` varchar(256) NOT NULL,
  `Y` double DEFAULT NULL,
  `X` double DEFAULT NULL,
  `Z` double DEFAULT NULL,
  `M` double DEFAULT NULL,
  PRIMARY KEY (`PointID`,`Token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `magnetic_field`
--

LOCK TABLES `magnetic_field` WRITE;
/*!40000 ALTER TABLE `magnetic_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `magnetic_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `point`
--

DROP TABLE IF EXISTS `point`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `point` (
  `Token` varchar(256) NOT NULL,
  `PointID` varchar(256) NOT NULL,
  `CoordX` int DEFAULT NULL,
  `CoordY` int DEFAULT NULL,
  `Long` decimal(9,6) DEFAULT NULL,
  `Lat` decimal(8,6) DEFAULT NULL,
  PRIMARY KEY (`Token`,`PointID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `point`
--

LOCK TABLES `point` WRITE;
/*!40000 ALTER TABLE `point` DISABLE KEYS */;
/*!40000 ALTER TABLE `point` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wifi`
--

DROP TABLE IF EXISTS `wifi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wifi` (
  `Token` varchar(256) NOT NULL,
  `PointID` varchar(256) NOT NULL,
  `MAC` varchar(45) NOT NULL,
  `SSID` varchar(45) DEFAULT NULL,
  `Channel` int NOT NULL,
  `Frequency` varchar(45) NOT NULL,
  `Quality` varchar(45) NOT NULL,
  `RSSI` int DEFAULT NULL,
  PRIMARY KEY (`Token`,`PointID`,`MAC`,`Channel`,`Frequency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wifi`
--

LOCK TABLES `wifi` WRITE;
/*!40000 ALTER TABLE `wifi` DISABLE KEYS */;
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

-- Dump completed on 2024-01-08  9:39:43
