-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 13, 2023 at 12:13 PM
-- Server version: 8.0.31
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Naato`
--

-- --------------------------------------------------------

--
-- Table structure for table `Answers`
--

CREATE TABLE `Answers` (
  `ID` int NOT NULL,
  `questionID` varchar(100) NOT NULL,
  `text` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Answers`
--

INSERT INTO `Answers` (`ID`, `questionID`, `text`) VALUES
(11, '9099503176827751137', 'Water onto himself half economic. Information window possible style science fill goal.'),
(12, '9099503176827751137', 'Prevent gas reduce lay. Show treat work worry.'),
(13, '9099503176827751137', 'History good case represent use assume check.'),
(14, '9099503176827751137', 'Table chance single. Different believe picture second.');

-- --------------------------------------------------------

--
-- Table structure for table `facts`
--

CREATE TABLE `facts` (
  `ID` int NOT NULL,
  `userID` int NOT NULL,
  `text` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `facts`
--

INSERT INTO `facts` (`ID`, `userID`, `text`) VALUES
(1, 40, 'The above exception was the direct cause of the following exception:'),
(2, 41, 'About plant vote if political source probably. Vote coach light view employee. Reason future various well.'),
(3, 41, 'Face all stock.');

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `ID` int NOT NULL,
  `group_Hash` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `group_name` varchar(90) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `open` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`ID`, `group_Hash`, `group_name`, `open`) VALUES
(23, '38c9d6a1ef1ab30d0c1612cb36d08510', 'David Alvarado', 0),
(24, 'ef362674ae79e5b91595ac8b7dade5bb', 'Toni Stokes', 0);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `ID` int NOT NULL,
  `question_Hash` varchar(50) NOT NULL,
  `groupID` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `text` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`ID`, `question_Hash`, `groupID`, `text`) VALUES
(8, '9099503176827751137', '', 'Ago its image within try voice. Opportunity room ask first argue probably. Yeah off provide think charge me marriage course.');

-- --------------------------------------------------------

--
-- Table structure for table `score_scope`
--

CREATE TABLE `score_scope` (
  `ID` int NOT NULL,
  `length` int NOT NULL,
  `groupID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int NOT NULL,
  `name` varchar(70) NOT NULL,
  `username` varchar(90) NOT NULL,
  `user_Hash` varchar(200) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `groupID` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `points` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `name`, `username`, `user_Hash`, `nickname`, `groupID`, `points`) VALUES
(33, 'Pamela Newman', 'dblack', '63229a67fcd525366f77cfb1224687c6', 'narrator', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(34, 'Alyssa Mcknight', 'matthewnguyen', '05e7f102842fa1a3367af73bbd0843a2', '', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(35, 'Allen Hoffman', 'smithcheryl', 'a2a4a5d9f790b65c2b03e1ebd97297dc', '', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(36, 'Devin Hudson', 'pnorman', '690cd652a88add502711a47bee3f26ec', '', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(37, 'James Martin', 'johnsondillon', '4060789ae9e8dd840b9740bc000769eb', '', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(38, 'Marcus Moore', 'amanda86', 'cd34d952580e903df4d9aebd192d14db', '', '38c9d6a1ef1ab30d0c1612cb36d08510', 15),
(39, 'Christopher Macdonald DDS', 'david97', '5d0b53f0fc13a1634a4244ee313e18b4', 'narrator', 'ef362674ae79e5b91595ac8b7dade5bb', 15),
(40, 'Anita Stewart', 'nfowler', 'ebdca6aa109dc34c788090f15a786229', '', 'ef362674ae79e5b91595ac8b7dade5bb', 15),
(41, 'Lance Watts', 'floresricky', 'c7df8ece9a01703ad8f17026db862278', '', 'ef362674ae79e5b91595ac8b7dade5bb', 15),
(42, 'Allen Perez', 'michelle80', 'ed6f938c45696ec666dec9cf8db87649', '', 'ef362674ae79e5b91595ac8b7dade5bb', 15),
(43, 'Tanya Ellis', 'carrollkenneth', 'a14f67907f2054ca3ae3c6bb6d99157d', '', 'ef362674ae79e5b91595ac8b7dade5bb', 15),
(44, 'Antonio Walters', 'dennis60', 'ea31d8c46a4c0f3098a8cc91c1058b93', '', 'ef362674ae79e5b91595ac8b7dade5bb', 15);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Answers`
--
ALTER TABLE `Answers`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `questionID` (`questionID`);

--
-- Indexes for table `facts`
--
ALTER TABLE `facts`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `group_Hash` (`group_Hash`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `question_Hash` (`question_Hash`),
  ADD KEY `groupID` (`groupID`);

--
-- Indexes for table `score_scope`
--
ALTER TABLE `score_scope`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `groupID` (`groupID`),
  ADD KEY `groupID_2` (`groupID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Answers`
--
ALTER TABLE `Answers`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `facts`
--
ALTER TABLE `facts`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `score_scope`
--
ALTER TABLE `score_scope`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Answers`
--
ALTER TABLE `Answers`
  ADD CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`questionID`) REFERENCES `questions` (`question_Hash`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`group_Hash`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
