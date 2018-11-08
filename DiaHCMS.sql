-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: DiaHCMS
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ANOMALY`
--

DROP TABLE IF EXISTS `ANOMALY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `ANOMALY` (
  `A_ID` varchar(10) NOT NULL,
  `DATE` date NOT NULL,
  `TIME` time NOT NULL,
  `BS` float NOT NULL,
  `DESCRIPTION` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`DATE`,`TIME`),
  CONSTRAINT `anomaly_ibfk_1` FOREIGN KEY (`DATE`) REFERENCES `patient` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ANOMALY`
--

LOCK TABLES `ANOMALY` WRITE;
/*!40000 ALTER TABLE `ANOMALY` DISABLE KEYS */;
INSERT INTO `ANOMALY` VALUES ('AN01','2018-11-01','14:13:03',45.2,'Fainted during exercise'),('AN02','2018-11-01','16:57:57',68,'Missed a meal'),('AN03','2018-11-06','19:42:17',54,'Something'),('AN04','2018-11-08','15:22:19',76,'Missed Lunch');
/*!40000 ALTER TABLE `ANOMALY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `INSULIN`
--

DROP TABLE IF EXISTS `INSULIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `INSULIN` (
  `I_ID` varchar(10) NOT NULL,
  `DATE` date NOT NULL,
  `TIME` time NOT NULL,
  `AMOUNT` float NOT NULL,
  `BS_PRE` float NOT NULL,
  PRIMARY KEY (`DATE`,`TIME`),
  CONSTRAINT `insulin_ibfk_1` FOREIGN KEY (`DATE`) REFERENCES `patient` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `INSULIN`
--

LOCK TABLES `INSULIN` WRITE;
/*!40000 ALTER TABLE `INSULIN` DISABLE KEYS */;
INSERT INTO `INSULIN` VALUES ('IN01','2018-11-01','14:07:41',4.5,5.4),('IN02','2018-11-01','14:08:56',5,45),('IN03','2018-11-01','14:09:23',6,56),('IN04','2018-11-01','14:09:33',99,76),('IN05','2018-11-06','18:05:47',54,45),('IN06','2018-11-06','18:06:54',87,78),('IN07','2018-11-06','21:50:43',65,56),('IN08','2018-11-07','14:09:51',79,69),('IN09','2018-11-07','14:10:18',41,14),('IN10','2018-11-07','14:58:54',123,34556),('IN11','2018-11-08','12:10:10',89,67),('IN12','2018-11-08','14:39:16',65,56),('IN13','2018-11-08','14:46:08',1,1),('IN14','2018-11-08','14:50:30',1,1),('IN15','2018-11-08','14:50:40',32,23),('IN16','2018-11-08','14:53:27',1,1),('IN17','2018-11-08','14:53:35',23,32),('IN18','2018-11-08','14:53:40',32,23),('IN19','2018-11-08','15:05:19',78,87);
/*!40000 ALTER TABLE `INSULIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEAL_PLAN`
--

DROP TABLE IF EXISTS `MEAL_PLAN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `MEAL_PLAN` (
  `MEAL_ID` varchar(10) NOT NULL,
  `TIME` time NOT NULL,
  `NUTRITION` float NOT NULL,
  PRIMARY KEY (`MEAL_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEAL_PLAN`
--

LOCK TABLES `MEAL_PLAN` WRITE;
/*!40000 ALTER TABLE `MEAL_PLAN` DISABLE KEYS */;
INSERT INTO `MEAL_PLAN` VALUES ('MP01','08:00:00',41),('MP02','10:00:00',18),('MP03','13:00:00',37),('MP04','16:00:00',16),('MP05','20:00:00',54);
/*!40000 ALTER TABLE `MEAL_PLAN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEAL_TAKEN`
--

DROP TABLE IF EXISTS `MEAL_TAKEN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `MEAL_TAKEN` (
  `MEAL_ID` varchar(10) NOT NULL,
  `BS_PRE` float NOT NULL,
  `BOLUS_ID` varchar(10) NOT NULL,
  `TAKEN_STATUS` varchar(1) NOT NULL,
  PRIMARY KEY (`MEAL_ID`),
  CONSTRAINT `meal_taken_ibfk_1` FOREIGN KEY (`MEAL_ID`) REFERENCES `meal_plan` (`meal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEAL_TAKEN`
--

LOCK TABLES `MEAL_TAKEN` WRITE;
/*!40000 ALTER TABLE `MEAL_TAKEN` DISABLE KEYS */;
/*!40000 ALTER TABLE `MEAL_TAKEN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medication`
--

DROP TABLE IF EXISTS `medication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `medication` (
  `MED_ID` varchar(10) NOT NULL,
  `NAME` varchar(20) NOT NULL,
  `TIME` time NOT NULL,
  `QUANTITY` varchar(15) NOT NULL,
  `TAKEN_STATUS` varchar(1) NOT NULL,
  PRIMARY KEY (`NAME`,`TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medication`
--

LOCK TABLES `medication` WRITE;
/*!40000 ALTER TABLE `medication` DISABLE KEYS */;
INSERT INTO `medication` VALUES ('ME01','AAA','07:00:00','1 Tablet','1'),('ME02','BBB','14:30:00','50 ML','1'),('ME05','CCC','22:00:00','75 ML','1'),('ME04','DDD','05:00:00','1 Tablet','1');
/*!40000 ALTER TABLE `medication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PATIENT`
--

DROP TABLE IF EXISTS `PATIENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `PATIENT` (
  `DATE` date NOT NULL,
  `BS_AM` float NOT NULL,
  `FOOD` varchar(1) NOT NULL,
  `MEDS` varchar(1) NOT NULL,
  `PE` varchar(1) NOT NULL,
  `BS_PM` float NOT NULL,
  `BMI` float NOT NULL,
  PRIMARY KEY (`DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PATIENT`
--

LOCK TABLES `PATIENT` WRITE;
/*!40000 ALTER TABLE `PATIENT` DISABLE KEYS */;
INSERT INTO `PATIENT` VALUES ('2018-10-30',0,'N','N','N',0,0),('2018-10-31',45,'N','N','N',0,0),('2018-11-01',0,'N','N','N',0,0),('2018-11-06',67,'N','N','Y',98,0),('2018-11-07',32,'N','N','N',0,0),('2018-11-08',0,'Y','Y','Y',54,0);
/*!40000 ALTER TABLE `PATIENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PE_DONE`
--

DROP TABLE IF EXISTS `PE_DONE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `PE_DONE` (
  `PE_ID` varchar(10) NOT NULL,
  `DATE` date NOT NULL,
  `TIME` time NOT NULL,
  `DURATION` int(11) NOT NULL,
  PRIMARY KEY (`DATE`,`TIME`),
  KEY `PE_ID` (`PE_ID`),
  CONSTRAINT `pe_done_ibfk_1` FOREIGN KEY (`DATE`) REFERENCES `patient` (`date`),
  CONSTRAINT `pe_done_ibfk_2` FOREIGN KEY (`PE_ID`) REFERENCES `pe_plan` (`pe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PE_DONE`
--

LOCK TABLES `PE_DONE` WRITE;
/*!40000 ALTER TABLE `PE_DONE` DISABLE KEYS */;
/*!40000 ALTER TABLE `PE_DONE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PE_PLAN`
--

DROP TABLE IF EXISTS `PE_PLAN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `PE_PLAN` (
  `PE_ID` varchar(10) NOT NULL,
  `TYPE` varchar(15) NOT NULL,
  PRIMARY KEY (`PE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PE_PLAN`
--

LOCK TABLES `PE_PLAN` WRITE;
/*!40000 ALTER TABLE `PE_PLAN` DISABLE KEYS */;
INSERT INTO `PE_PLAN` VALUES ('PP01','AEROBICS'),('PP02','BRISK WALKING'),('PP03','CARDIO'),('PP04','RUNNING'),('PP05','WEIGHTS');
/*!40000 ALTER TABLE `PE_PLAN` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-08 18:17:37
