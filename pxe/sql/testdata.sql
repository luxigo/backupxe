INSERT INTO `hosts` VALUES ('00-12-ab-32-34-fd', 'poste1');
INSERT INTO `hosts` VALUES ('00-12-ab-32-34-fe', 'poste2');
INSERT INTO `hosts` VALUES ('00-12-ab-32-34-fc', NULL);

INSERT INTO `machine` VALUES ('00-12-ab-32-34-fd', NULL, NULL, 'default_save_type1', 'default_rest_type1');
INSERT INTO `machine` VALUES ('00-12-ab-32-34-fe', NULL, NULL, 'default_save_type2', 'default_rest_type2');

INSERT INTO `backup` VALUES (1, 'default_save_type1', 'sda', '/pxe/image/default/disk1', 0, 1, 1, 0);
INSERT INTO `backup` VALUES (2, 'default_rest_type1', 'sda', '/pxe/image/default/disk1', 0, 1, 0, 1);
INSERT INTO `backup` VALUES (3, 'default_save_type1', 'sdb', '/pxe/image/default/disk2', 0, 1, 1, 2);
INSERT INTO `backup` VALUES (4, 'default_rest_type1', 'sdb', '/pxe/image/default/disk2', 0, 1, 1, 2);
INSERT INTO `backup` VALUES (5, 'default_save_type2', 'hda', '/pxe/image/default/disk1', 0, 1, 1, 3);
INSERT INTO `backup` VALUES (6, 'default_rest_type2', 'hda', '/pxe/image/default/disk1', 0, 1, 0, 4);

INSERT INTO `backup_details` VALUES (1, 0, '/dev/sda1', '/dev/sda2');
INSERT INTO `backup_details` VALUES (2, 0, '/dev/sda1', 'part1');
INSERT INTO `backup_details` VALUES (3, 1, '/dev/sda1', '/dev/sda2');
INSERT INTO `backup_details` VALUES (4, 2, '/dev/sdb1', 'part1');
INSERT INTO `backup_details` VALUES (5, 2, '/dev/sdb2', 'part2');
INSERT INTO `backup_details` VALUES (6, 3, '/dev/hda1', '/dev/hda2');
INSERT INTO `backup_details` VALUES (7, 3, '/dev/hda1', 'part1');
INSERT INTO `backup_details` VALUES (8, 4, '/dev/hda1', '/dev/hda2');

