DROP TABLE IF EXISTS `hosts`;
CREATE TABLE `hosts` (
  `mac` varchar(17) NOT NULL,
  `name` varchar(255) default NULL,
  UNIQUE KEY `mac` (`mac`)
);

DROP TABLE IF EXISTS `machine`;
CREATE TABLE `machine` (
  `mac` varchar(17) NOT NULL,
  `descr` varchar(255) default NULL,
  `pxeconfig` varchar(255) default NULL,
  `save_name` varchar(255) default NULL,
  `restore_name` varchar(255) default NULL,
  UNIQUE KEY `mac` (`mac`)
);

DROP TABLE IF EXISTS `backup`;
CREATE TABLE `backup` (
  `idx` int(10) unsigned NOT NULL auto_increment,
  `backup_name` varchar(255) NOT NULL,
  `disk` varchar(32) NOT NULL,
  `dir` varchar(255) NOT NULL,
  `check_ptable_md5` int(1) NOT NULL default '0',
  `dombr` int(1) NOT NULL default '1',
  `doptable` int(1) NOT NULL default '0',
  `backup_details_id` int(10) unsigned NOT NULL,
  UNIQUE KEY `idx` (`idx`)
);

DROP TABLE IF EXISTS `backup_details`;
CREATE TABLE `backup_details` (
  `idx` int(10) unsigned NOT NULL auto_increment,
  `backup_details_id` int(10) unsigned NOT NULL,
  `partition` varchar(255) NOT NULL,
  `backupfile` varchar(255) NOT NULL,
  UNIQUE KEY `idx` (`idx`)
);
