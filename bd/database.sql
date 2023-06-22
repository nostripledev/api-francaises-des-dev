SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `API_francaises_des_dev` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `API_francaises_des_dev`;

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `member` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `mail` varchar(320) NOT NULL,
  `date_validate` datetime NOT NULL,
  `date_deleted` datetime NOT NULL,
  `url_portfolio` varchar(320) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `member_has_category` (
  `id_member` int(11) NOT NULL,
  `id_category` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `member_has_network` (
  `id_member` int(11) NOT NULL,
  `id_network` int(11) NOT NULL,
  `url` varchar(355) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `network` (
  `Id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `member`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `member_has_category`
  ADD KEY `id_member` (`id_member`),
  ADD KEY `id_category` (`id_category`);

ALTER TABLE `member_has_network`
  ADD KEY `id_member` (`id_member`),
  ADD KEY `id_network` (`id_network`);

ALTER TABLE `network`
  ADD PRIMARY KEY (`Id`);


ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `member`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `network`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `member_has_category`
  ADD CONSTRAINT `member_has_category_ibfk_1` FOREIGN KEY (`id_member`) REFERENCES `member` (`id`),
  ADD CONSTRAINT `member_has_category_ibfk_2` FOREIGN KEY (`id_category`) REFERENCES `category` (`id`);

ALTER TABLE `member_has_network`
  ADD CONSTRAINT `member_has_network_ibfk_1` FOREIGN KEY (`id_member`) REFERENCES `member` (`id`),
  ADD CONSTRAINT `member_has_network_ibfk_2` FOREIGN KEY (`id_network`) REFERENCES `network` (`Id`);
COMMIT;