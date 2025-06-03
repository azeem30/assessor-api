/*M!999986\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: insightqa
-- ------------------------------------------------------
-- Server version	11.7.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `department_name` varchar(255) NOT NULL,
  PRIMARY KEY (`department_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `questions_and_answers`
--

DROP TABLE IF EXISTS `questions_and_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions_and_answers` (
  `id` varchar(255) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  KEY `id` (`id`),
  CONSTRAINT `questions_and_answers_ibfk_1` FOREIGN KEY (`id`) REFERENCES `tests` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `response_data`
--

DROP TABLE IF EXISTS `response_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `response_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `sample_answer` text NOT NULL,
  `user_answer` text DEFAULT NULL,
  `response_id` varchar(255) NOT NULL,
  `similarity` double NOT NULL,
  `marks` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `response_id` (`response_id`),
  CONSTRAINT `response_data_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `responses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `responses`
--

DROP TABLE IF EXISTS `responses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `responses` (
  `id` varchar(255) NOT NULL,
  `student_email` varchar(255) NOT NULL,
  `test_id` varchar(255) NOT NULL,
  `marks_obtained` int(11) NOT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `student_email` (`student_email`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `responses_ibfk_1` FOREIGN KEY (`student_email`) REFERENCES `students` (`email`),
  CONSTRAINT `responses_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `email` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `password` varchar(255) NOT NULL,
  `dept_name` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `is_verified` tinyint(4) DEFAULT 0,
  `verification_token` varchar(255) DEFAULT NULL,
  `token_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`email`),
  KEY `dept_name` (`dept_name`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`department_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `email` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `password` varchar(255) NOT NULL,
  `dept_name` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `is_verified` tinyint(4) DEFAULT 0,
  `verification_token` varchar(255) DEFAULT NULL,
  `token_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`email`),
  KEY `dept_name` (`dept_name`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`department_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tests` (
  `id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `marks` int(11) NOT NULL,
  `difficulty` varchar(255) NOT NULL,
  `scheduled_at` datetime DEFAULT current_timestamp(),
  `teacher_email` varchar(255) NOT NULL,
  `pairs` int(11) NOT NULL DEFAULT 1,
  `duration` int(11) DEFAULT 60,
  `dept_name` varchar(255) NOT NULL DEFAULT 'Information Technology',
  PRIMARY KEY (`id`),
  KEY `teacher_email` (`teacher_email`),
  KEY `dept_name` (`dept_name`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`teacher_email`) REFERENCES `teachers` (`email`),
  CONSTRAINT `tests_ibfk_2` FOREIGN KEY (`dept_name`) REFERENCES `department` (`department_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-06-03 12:32:41
