-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 08, 2021 at 03:39 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel`
--

-- --------------------------------------------------------

--
-- Table structure for table `agent`
--

CREATE TABLE `agent` (
  `email` varchar(30) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `agent_ID` varchar(20) DEFAULT NULL,
  `commission` float DEFAULT NULL,
  `commission_amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `agent`
--

INSERT INTO `agent` (`email`, `password`, `agent_ID`, `commission`, `commission_amount`) VALUES
('abc@gmail.com', '12345', '010', 0, 0.15),
('blah@gmail.com', 'abc', '006', 0, 0.12),
('brandon@gmail.com', '12345', '003', 0, 0.25),
('kebob@gmail.com', '56789', '004', 0, 0.15),
('schen@nyu.edu', '13579ghi', '002', 0, 0.1),
('why@gmail.com', 'adfbc', '008', 0, 0.15);

-- --------------------------------------------------------

--
-- Table structure for table `agent_purchase`
--

CREATE TABLE `agent_purchase` (
  `ticket_ID` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `customer` varchar(20) NOT NULL,
  `date_purchased` date DEFAULT NULL,
  `commission_amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `agent_purchase`
--

INSERT INTO `agent_purchase` (`ticket_ID`, `email`, `customer`, `date_purchased`, `commission_amount`) VALUES
('1312', 'blah@gmail.com', 'Kai Bowes', '2021-02-27', 200),
('1312', 'kebob@gmail.com', 'Kai Bowes', '2021-01-19', 150),
('1312', 'schen@nyu.edu', 'Ping Chang', '2021-03-13', 130),
('1312', 'why@gmail.com', 'Sean Hsu', '2021-02-25', 300),
('1400', 'schen@nyu.edu', 'Kevin Renn', '2021-05-07', 230),
('1510', 'brandon@gmail.com', 'Kai Bowes', '2021-02-19', 210),
('1510', 'kebob@gmail.com', 'Ping Chang', '2021-03-19', 160),
('1510', 'schen@nyu.edu', 'Kevin Renn', '2021-03-25', 140),
('1510', 'schen@nyu.edu', 'Sean Chen', '2021-02-23', 100);

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `name` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`, `username`) VALUES
('China Eastern', '/'),
('West Virginia', '/');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `name` varchar(20) NOT NULL,
  `ID` varchar(20) NOT NULL,
  `seats` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`name`, `ID`, `seats`) VALUES
('China Eastern', '001', 300),
('China Eastern', '002', 350),
('China Eastern', '015', 444),
('China Eastern', '017', 900),
('China Eastern', '030', 120);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `city`) VALUES
('JFK', 'NYC'),
('PVG', 'Shanghai'),
('ORD', 'Chicago'),
('TPE', 'Taipei');

-- --------------------------------------------------------

--
-- Table structure for table `comment_rate`
--

CREATE TABLE `comment_rate` (
  `name` varchar(20) DEFAULT NULL,
  `flight_num` varchar(20) DEFAULT NULL,
  `comments` varchar(40) DEFAULT NULL,
  `rating` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comment_rate`
--

INSERT INTO `comment_rate` (`name`, `flight_num`, `comments`, `rating`) VALUES
('China Eastern', '150', 'N/A', '4'),
('China Eastern', '250', 'It was ok', '3'),
('China Eastern', '550', 'It was nice', '4');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(30) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `building_num` varchar(10) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `phone_num` varchar(10) DEFAULT NULL,
  `passport_num` varchar(20) DEFAULT NULL,
  `passport_exp` char(6) DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_num`, `street`, `city`, `state`, `phone_num`, `passport_num`, `passport_exp`, `passport_country`) VALUES
('hsuny@nyu.edu', 'Sean Hsu', '12345', '123', 'Main St.', 'BruhCity', 'BruhState', '1352463790', '1352467', '120512', 'USA'),
('kaiangbowes@gmail.com', 'Kai Bowes', 'abc', '510', 'Bowes St.', 'Vancouver', 'BC', '1453875491', '5801231', '220601', 'Canada'),
('krenn121@nyu.edu', 'Kevin Renn', '67890def', '245', 'Beach St.', 'New York', 'NY', '0987654321', '1351256', '220101', 'USA'),
('pingchang@gmail.com', 'Yu-Ping Chang', '12345', '000', 'Bro St.', 'Brocity', 'Brostate', '1112223345', '3567031', '120512', 'Canada'),
('ypc231@nyu.edu', 'Ping Chang', '12345abc', '145', 'King St.', 'Brooklyn', 'NY', '1234567890', '1212341', '220101', 'USA');

-- --------------------------------------------------------

--
-- Table structure for table `customer_purchase`
--

CREATE TABLE `customer_purchase` (
  `ticket_ID` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `date_purchased` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer_purchase`
--

INSERT INTO `customer_purchase` (`ticket_ID`, `email`, `date_purchased`) VALUES
('1312', 'ypc231@nyu.edu', '2021-02-25'),
('1400', 'ypc231@nyu.edu', '2021-05-07'),
('1510', 'kaiangbowes@gmail.com', '2021-02-26'),
('1510', 'ypc231@nyu.edu', '2021-02-27');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `name` varchar(20) NOT NULL,
  `flight_num` varchar(20) NOT NULL,
  `depart_date` date NOT NULL,
  `depart_time` time NOT NULL,
  `arrival_date` date DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `base_price` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `depart_airport` varchar(20) NOT NULL,
  `arrival_airport` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`name`, `flight_num`, `depart_date`, `depart_time`, `arrival_date`, `arrival_time`, `base_price`, `status`, `depart_airport`, `arrival_airport`) VALUES
('China Eastern', '150', '2021-03-30', '12:20:00', '2021-03-31', '13:10:00', '500', 'on-time', 'JFK', 'PVG'),
('China Eastern', '250', '2021-03-30', '13:20:00', '2021-03-31', '16:10:00', '400', 'on-time', 'PVG', 'JFK'),
('China Eastern', '350', '2021-06-01', '16:30:00', '2021-06-02', '17:20:00', '550', 'on-time', 'JFK', 'PVG'),
('China Eastern', '450', '2021-05-01', '09:00:00', '2021-05-02', '14:00:00', '250', 'on-time', 'ORD', 'JFK'),
('China Eastern', '550', '2021-07-15', '10:00:00', '2021-07-16', '13:00:00', '125', 'delayed', 'TPE', 'JFK');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`username`, `password`, `name`) VALUES
('Roselia', 'seanycheny', 'China Eastern'),
('Vanguard', '123', 'China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone`
--

CREATE TABLE `staff_phone` (
  `username` varchar(20) NOT NULL,
  `phone_number` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_ID` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `flight_num` varchar(20) NOT NULL,
  `depart_date` date DEFAULT NULL,
  `depart_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_ID`, `name`, `flight_num`, `depart_date`, `depart_time`) VALUES
('1312', 'China Eastern', '150', '2021-03-30', '12:20:00'),
('1400', 'China Eastern', '550', '2021-07-15', '10:00:00'),
('1510', 'China Eastern', '250', '2021-03-30', '13:20:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agent`
--
ALTER TABLE `agent`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `agent_purchase`
--
ALTER TABLE `agent_purchase`
  ADD PRIMARY KEY (`ticket_ID`,`email`,`customer`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`name`,`ID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `customer_purchase`
--
ALTER TABLE `customer_purchase`
  ADD PRIMARY KEY (`ticket_ID`,`email`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`name`,`flight_num`,`depart_date`,`depart_time`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD PRIMARY KEY (`username`,`phone_number`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_ID`,`name`),
  ADD KEY `name` (`name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agent_purchase`
--
ALTER TABLE `agent_purchase`
  ADD CONSTRAINT `agent_purchase_ibfk_1` FOREIGN KEY (`ticket_ID`) REFERENCES `ticket` (`ticket_ID`),
  ADD CONSTRAINT `agent_purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `agent` (`email`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`name`) REFERENCES `airline` (`name`);

--
-- Constraints for table `customer_purchase`
--
ALTER TABLE `customer_purchase`
  ADD CONSTRAINT `customer_purchase_ibfk_1` FOREIGN KEY (`ticket_ID`) REFERENCES `ticket` (`ticket_ID`),
  ADD CONSTRAINT `customer_purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`name`) REFERENCES `airline` (`name`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`name`) REFERENCES `airline` (`name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
