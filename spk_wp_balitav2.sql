CREATE DATABASE  IF NOT EXISTS `spk_wp_balitav2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `spk_wp_balitav2`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: spk_wp_balitav2
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `akun_ahli_gizi`
--

DROP TABLE IF EXISTS `akun_ahli_gizi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `akun_ahli_gizi` (
  `id_ahli_gizi` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) DEFAULT NULL,
  `nomor_str` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_ahli_gizi`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akun_ahli_gizi`
--

LOCK TABLES `akun_ahli_gizi` WRITE;
/*!40000 ALTER TABLE `akun_ahli_gizi` DISABLE KEYS */;
INSERT INTO `akun_ahli_gizi` VALUES (1,'pakar_gizi','gizi123','dr. Siti, S.Gz','STR-9988776655');
/*!40000 ALTER TABLE `akun_ahli_gizi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `akun_sppg`
--

DROP TABLE IF EXISTS `akun_sppg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `akun_sppg` (
  `id_sppg` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) DEFAULT NULL,
  `instansi` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_sppg`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akun_sppg`
--

LOCK TABLES `akun_sppg` WRITE;
/*!40000 ALTER TABLE `akun_sppg` DISABLE KEYS */;
INSERT INTO `akun_sppg` VALUES (1,'sppg_admin','sppg123','Budi Santoso','Satpel Gizi Bantul');
/*!40000 ALTER TABLE `akun_sppg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alternatif`
--

DROP TABLE IF EXISTS `alternatif`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alternatif` (
  `id_alternatif` int NOT NULL AUTO_INCREMENT,
  `kode_alternatif` varchar(10) NOT NULL,
  `jadwal_menu` varchar(100) NOT NULL,
  `nama_makanan` text,
  `catatan_rekomendasi` text,
  `is_selected` tinyint(1) NOT NULL DEFAULT '0',
  `skor_terpilih` double DEFAULT NULL,
  PRIMARY KEY (`id_alternatif`),
  UNIQUE KEY `kode_alternatif` (`kode_alternatif`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alternatif`
--

LOCK TABLES `alternatif` WRITE;
/*!40000 ALTER TABLE `alternatif` DISABLE KEYS */;
INSERT INTO `alternatif` VALUES (30,'A1','Senin, 14-04-2025','nasi putih, ayam goreng pasundan (boneless), tahu goreng, sayur sop, mangga manalagi',NULL,0,NULL),(31,'A2','Senin, 14-04-2025','nasi gurih, ayam goreng pasundan (boneless), tumis bayam bersantan, pepaya, susu sapi',NULL,0,NULL),(32,'A3','Senin, 14-04-2025','nasi putih, ayam goreng kentucky, sayur sop, saus tomat, jeruk manis',NULL,0,NULL),(33,'A4','Senin, 14-04-2025','nasi putih, ayam kentucky, sayur bayam, mangga manalagi, susu kedelai',NULL,0,NULL),(34,'A5','Senin, 14-04-2025','nasi gurih, ayam goreng kalasan, tahu goreng, sayur bayam, jeruk',NULL,0,NULL),(35,'A6','Senin, 14-04-2025','nasi putih, ayam goreng kalasan, tumis bayam bersantan, pepaya, susu kedelai',NULL,1,0.1235),(36,'A7','Senin, 14-04-2025','nasi putih, ayam goreng sukabumi, tempe goreng, capcay, pepaya',NULL,0,NULL),(37,'A8','Senin, 14-04-2025','nasi putih, ayam teriyaki, capcay, mangga manalagi, susu sapi',NULL,0,NULL),(38,'A9','Senin, 14-04-2025','nasi gurih, ayam taliwang, pelecing kangkung, jeruk manis, yogurt',NULL,0,NULL),(39,'A10','Senin, 14-04-2025','nasi putih, kalio ayam, tempe goreng, pelecing kangkung, mangga manalagi','energi ... kkal',0,NULL);
/*!40000 ALTER TABLE `alternatif` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bahan_baku`
--

DROP TABLE IF EXISTS `bahan_baku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bahan_baku` (
  `id_bahan` int NOT NULL AUTO_INCREMENT,
  `nama_bahan` varchar(255) NOT NULL,
  `tanggal_input` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_bahan`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bahan_baku`
--

LOCK TABLES `bahan_baku` WRITE;
/*!40000 ALTER TABLE `bahan_baku` DISABLE KEYS */;
INSERT INTO `bahan_baku` VALUES (19,'beras putih','2026-04-22 10:39:31'),(20,'ayam boneless','2026-04-22 10:39:35'),(21,'tempe','2026-04-22 10:39:43'),(22,'tahu','2026-04-22 10:39:44'),(23,'wortel','2026-04-22 10:39:45'),(24,'jagung','2026-04-22 10:39:47'),(25,'bayam','2026-04-22 10:39:58'),(26,'kubis','2026-04-22 10:39:59'),(27,'brokoli','2026-04-22 10:40:01'),(28,'kangkung','2026-04-22 10:40:09'),(29,'jeruk manis','2026-04-22 10:40:12'),(30,'mangga manalagi','2026-04-22 10:40:21'),(31,'pepaya','2026-04-22 10:40:28');
/*!40000 ALTER TABLE `bahan_baku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hasil_ranking`
--

DROP TABLE IF EXISTS `hasil_ranking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hasil_ranking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kode_alternatif` varchar(20) NOT NULL,
  `jadwal_menu` varchar(100) DEFAULT NULL,
  `nama_makanan` text,
  `skor_akhir` double NOT NULL,
  `peringkat` int NOT NULL,
  `waktu_hitung` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_peringkat` (`peringkat`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hasil_ranking`
--

LOCK TABLES `hasil_ranking` WRITE;
/*!40000 ALTER TABLE `hasil_ranking` DISABLE KEYS */;
INSERT INTO `hasil_ranking` VALUES (143,'A6','Senin, 14-04-2025','nasi putih, ayam goreng kalasan, tumis bayam bersantan, pepaya, susu kedelai',0.1235,1,'2026-04-29 12:35:51'),(144,'A7','Senin, 14-04-2025','nasi putih, ayam goreng sukabumi, tempe goreng, capcay, pepaya',0.1191,2,'2026-04-29 12:35:51'),(145,'A10','Senin, 14-04-2025','nasi putih, kalio ayam, tempe goreng, pelecing kangkung, mangga manalagi',0.1135,3,'2026-04-29 12:35:51'),(146,'A4','Senin, 14-04-2025','nasi putih, ayam kentucky, sayur bayam, mangga manalagi, susu kedelai',0.1079,4,'2026-04-29 12:35:51'),(147,'A2','Senin, 14-04-2025','nasi gurih, ayam goreng pasundan (boneless), tumis bayam bersantan, pepaya, susu sapi',0.1039,5,'2026-04-29 12:35:51'),(148,'A8','Senin, 14-04-2025','nasi putih, ayam teriyaki, capcay, mangga manalagi, susu sapi',0.1025,6,'2026-04-29 12:35:51'),(149,'A1','Senin, 14-04-2025','nasi putih, ayam goreng pasundan (boneless), tahu goreng, sayur sop, mangga manalagi',0.1,7,'2026-04-29 12:35:51'),(150,'A5','Senin, 14-04-2025','nasi gurih, ayam goreng kalasan, tahu goreng, sayur bayam, jeruk',0.0998,8,'2026-04-29 12:35:51'),(151,'A9','Senin, 14-04-2025','nasi gurih, ayam taliwang, pelecing kangkung, jeruk manis, yogurt',0.0703,9,'2026-04-29 12:35:51'),(152,'A3','Senin, 14-04-2025','nasi putih, ayam goreng kentucky, sayur sop, saus tomat, jeruk manis',0.0596,10,'2026-04-29 12:35:51');
/*!40000 ALTER TABLE `hasil_ranking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kriteria`
--

DROP TABLE IF EXISTS `kriteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kriteria` (
  `id_kriteria` int NOT NULL AUTO_INCREMENT,
  `kode_kriteria` varchar(10) NOT NULL,
  `nama_kriteria` varchar(100) NOT NULL,
  `tipe_kriteria` enum('Benefit','Cost') NOT NULL,
  `bobot_awal` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id_kriteria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kriteria`
--

LOCK TABLES `kriteria` WRITE;
/*!40000 ALTER TABLE `kriteria` DISABLE KEYS */;
INSERT INTO `kriteria` VALUES (1,'C1','Protein','Benefit',0.25),(2,'C2','Karbohidrat','Benefit',0.20),(3,'C3','Lemak Jenuh','Cost',0.10),(4,'C4','Vitamin','Benefit',0.15),(5,'C5','Kalsium','Benefit',0.30);
/*!40000 ALTER TABLE `kriteria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penilaian`
--

DROP TABLE IF EXISTS `penilaian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penilaian` (
  `id_alternatif` int NOT NULL,
  `nilai_c1` decimal(10,2) NOT NULL DEFAULT '0.00',
  `nilai_c2` decimal(10,2) NOT NULL DEFAULT '0.00',
  `nilai_c3` decimal(10,2) NOT NULL DEFAULT '0.00',
  `nilai_c4` decimal(10,2) NOT NULL DEFAULT '0.00',
  `nilai_c5` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id_alternatif`),
  CONSTRAINT `penilaian_ibfk_1` FOREIGN KEY (`id_alternatif`) REFERENCES `alternatif` (`id_alternatif`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penilaian`
--

LOCK TABLES `penilaian` WRITE;
/*!40000 ALTER TABLE `penilaian` DISABLE KEYS */;
INSERT INTO `penilaian` VALUES (30,3.00,5.00,3.00,2.00,2.00),(31,3.00,2.00,1.00,4.00,2.00),(32,3.00,3.00,3.00,1.00,1.00),(33,3.00,5.00,3.00,3.00,2.00),(34,4.00,2.00,1.00,2.00,2.00),(35,3.00,4.00,1.00,4.00,2.00),(36,4.00,3.00,1.00,3.00,2.00),(37,2.00,5.00,3.00,2.00,3.00),(38,3.00,2.00,1.00,2.00,1.00),(39,3.00,5.00,2.00,3.00,2.00);
/*!40000 ALTER TABLE `penilaian` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-29 12:39:07
