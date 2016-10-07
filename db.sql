CREATE DATABASE IF NOT EXISTS novel DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

USE novel ;

CREATE TABLE IF NOT EXISTS `novel_info` ( 
  `novel_id` int(11) NOT NULL AUTO_INCREMENT,
  `novel_name` varchar(30) DEFAULT NULL,
  `novel_author` varchar(30) DEFAULT NULL,
  `novel_category` varchar(30) DEFAULT NULL,
  `novel_image` varchar(100),
  `last_update` varchar(100),  
  `novel_abstract` text,
  `novel_status` int(1) NOT NULL DEFAULT '0',
  `novel_booknum` int(11),
  PRIMARY KEY (`novel_id`),
  KEY `nbooknum_fk` (`novel_booknum`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `chapter_info` ( 
  `chapter_id` int(11) NOT NULL AUTO_INCREMENT,
  `chapter_name` varchar(100),
  `chapter_order` int(11),
  `chapter_content` text,
  `chapter_booknum` int(11),
  PRIMARY KEY (`chapter_id`),
  KEY `cbooknum_fk` (`chapter_booknum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;