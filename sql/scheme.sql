
CREATE DATABASE IF NOT EXISTS `abhdb`;
use `abhdb`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50),
  `password` VARCHAR(300),
  `email` VARCHAR(64),
  `create_time` DATETIME NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50),
  `password` VARCHAR(300),
  `email` VARCHAR(64),
  `create_time` DATETIME NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
