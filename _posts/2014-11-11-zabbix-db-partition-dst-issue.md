---
published: true
layout: post
title: "Zabbix DB Partition DST Issue"
author: Karim Elatov
categories: [os]
tags: [linux,debian,zabbix,monitoring,mysql]
---
All of a sudden I started receiving errors on the maintenance scripts for the Zabbbix MySQL partitions (check out [my previous post](/2014/08/partition-zabbix-22-mysql-database/) on the configuration). Here is the error I received:

	partition_create(zabbix,history,p201411090000,1415602800)
	ERROR 1493 (HY000) at line 1: VALUES LESS THAN value must be strictly increasing for each partition

The issue is discussed [here](https://www.zabbix.com/forum/showthread.php?t=47048). It's an issue with Daylight Savings time and  It seems that the fix is to remove the future partitions and then re-run the maintenance scripts. So first you can see which partitions actually have data by running the following:

	mysql> SELECT partition_name, table_rows, PARTITION_ORDINAL_POSITION, PARTITION_METHOD FROM information_schema.PARTITIONS  WHERE TABLE_SCHEMA = 'zabbix' AND TABLE_NAME = 'history_log';
	+----------------+------------+----------------------------+------------------+
	| partition_name | table_rows | PARTITION_ORDINAL_POSITION | PARTITION_METHOD |
	+----------------+------------+----------------------------+------------------+
	| p201410050000  |       4032 |                          1 | RANGE            |
	| p201410060000  |       4036 |                          2 | RANGE            |
	| p201410070000  |       4040 |                          3 | RANGE            |
	| p201410080000  |       4053 |                          4 | RANGE            |
	| p201410090000  |       4089 |                          5 | RANGE            |
	| p201410100000  |       4036 |                          6 | RANGE            |
	| p201410110000  |       4044 |                          7 | RANGE            |
	| p201410120000  |       4048 |                          8 | RANGE            |
	| p201410130000  |       4042 |                          9 | RANGE            |
	| p201410140000  |       4044 |                         10 | RANGE            |
	| p201410150000  |       4046 |                         11 | RANGE            |
	| p201410160000  |       4040 |                         12 | RANGE            |
	| p201410170000  |       4030 |                         13 | RANGE            |
	| p201410180000  |       4040 |                         14 | RANGE            |
	| p201410190000  |       4036 |                         15 | RANGE            |
	| p201410200000  |       4032 |                         16 | RANGE            |
	| p201410210000  |       4040 |                         17 | RANGE            |
	| p201410220000  |       4039 |                         18 | RANGE            |
	| p201410230000  |       4078 |                         19 | RANGE            |
	| p201410240000  |       4050 |                         20 | RANGE            |
	| p201410250000  |       4083 |                         21 | RANGE            |
	| p201410260000  |       4174 |                         22 | RANGE            |
	| p201410270000  |       4170 |                         23 | RANGE            |
	| p201410280000  |       4152 |                         24 | RANGE            |
	| p201410290000  |       4154 |                         25 | RANGE            |
	| p201410300000  |       4160 |                         26 | RANGE            |
	| p201410310000  |       4159 |                         27 | RANGE            |
	| p201411010000  |       4156 |                         28 | RANGE            |
	| p201411020000  |       3970 |                         29 | RANGE            |
	| p201411022300  |       4036 |                         30 | RANGE            |
	| p201411032300  |       4034 |                         31 | RANGE            |
	| p201411042300  |       4044 |                         32 | RANGE            |
	| p201411052300  |       4040 |                         33 | RANGE            |
	| p201411062300  |       4048 |                         34 | RANGE            |
	| p201411072300  |       2789 |                         35 | RANGE            |
	| p201411082300  |       1676 |                         36 | RANGE            |
	| p201411092300  |          0 |                         37 | RANGE            |
	| p201411102300  |          0 |                         38 | RANGE            |
	| p201411112300  |          0 |                         39 | RANGE            |
	| p201411122300  |          0 |                         40 | RANGE            |
	| p201411132300  |          0 |                         41 | RANGE            |
	| p201411142300  |          0 |                         42 | RANGE            |
	+----------------+------------+----------------------------+------------------+
	42 rows in set (0.00 sec)

We can see that no data is in the 11-09 partition and the error we saw is for that date, here is manual call:

	mysql> CALL partition_maintenance('zabbix', 'history_log', 28, 24, 14);
	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411090000,1415602800) |
	+---------------------------------------------------------------+
	1 row in set (0.02 sec)

	ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

So let's remove every partition after and including 11-09 (there is no data there any ways):

	mysql> alter table history_log drop partition
	p201411142300,p201411132300,p201411122300,p201411112300,p201411102300,p201411092300;
	Query OK, 0 rows affected (0.03 sec)
	Records: 0  Duplicates: 0  Warnings: 0

Then after that the maintenance script went through:

	mysql> CALL partition_maintenance('zabbix', 'history_log', 28, 24, 14);
	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411090000,1415602800) |
	+---------------------------------------------------------------+
	1 row in set (0.01 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411100000,1415689200) |
	+---------------------------------------------------------------+
	1 row in set (0.02 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411110000,1415775600) |
	+---------------------------------------------------------------+
	1 row in set (0.03 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411120000,1415862000) |
	+---------------------------------------------------------------+
	1 row in set (0.03 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411130000,1415948400) |
	+---------------------------------------------------------------+
	1 row in set (0.04 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411140000,1416034800) |
	+---------------------------------------------------------------+
	1 row in set (0.05 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411150000,1416121200) |
	+---------------------------------------------------------------+
	1 row in set (0.06 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411160000,1416207600) |
	+---------------------------------------------------------------+
	1 row in set (0.06 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411170000,1416294000) |
	+---------------------------------------------------------------+
	1 row in set (0.07 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411180000,1416380400) |
	+---------------------------------------------------------------+
	1 row in set (0.08 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411190000,1416466800) |
	+---------------------------------------------------------------+
	1 row in set (0.08 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411200000,1416553200) |
	+---------------------------------------------------------------+
	1 row in set (0.09 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411210000,1416639600) |
	+---------------------------------------------------------------+
	1 row in set (0.10 sec)

	+---------------------------------------------------------------+
	| msg                                                           |
	+---------------------------------------------------------------+
	| partition_create(zabbix,history_log,p201411220000,1416726000) |
	+---------------------------------------------------------------+
	1 row in set (0.11 sec)

	+--------------------+---------------------------------------------------------------------------------------------------+
	| table              | partitions_deleted                                                                                |
	+--------------------+---------------------------------------------------------------------------------------------------+
	| zabbix.history_log | p201410050000,p201410060000,p201410070000,p201410080000,p201410090000,p201410100000,p201410110000 |
	+--------------------+---------------------------------------------------------------------------------------------------+
	1 row in set (0.12 sec)

	Query OK, 0 rows affected (0.12 sec)

I had to do that for each of the zabbix DB  tables:

- history
- history_log
- history_str
- history_text
- history_uint
- trends
- trends_uint

But at least no data was lost. And at the end, I was able to run the **maintenance_all** procedure without any issues:

	mysql> CALL partition_maintenance_all('zabbix');
	+----------------+--------------------+
	| table          | partitions_deleted |
	+----------------+--------------------+
	| zabbix.history | N/A                |
	+----------------+--------------------+
	1 row in set (0.00 sec)

	+--------------------+--------------------+
	| table              | partitions_deleted |
	+--------------------+--------------------+
	| zabbix.history_log | N/A                |
	+--------------------+--------------------+
	1 row in set (0.02 sec)

	+--------------------+--------------------+
	| table              | partitions_deleted |
	+--------------------+--------------------+
	| zabbix.history_str | N/A                |
	+--------------------+--------------------+
	1 row in set (0.02 sec)

	+---------------------+--------------------+
	| table               | partitions_deleted |
	+---------------------+--------------------+
	| zabbix.history_text | N/A                |
	+---------------------+--------------------+
	1 row in set (0.04 sec)

	+---------------------+--------------------+
	| table               | partitions_deleted |
	+---------------------+--------------------+
	| zabbix.history_uint | N/A                |
	+---------------------+--------------------+
	1 row in set (0.04 sec)

	+---------------+--------------------+
	| table         | partitions_deleted |
	+---------------+--------------------+
	| zabbix.trends | N/A                |
	+---------------+--------------------+
	1 row in set (0.06 sec)

	+--------------------+--------------------+
	| table              | partitions_deleted |
	+--------------------+--------------------+
	| zabbix.trends_uint | N/A                |
	+--------------------+--------------------+
	1 row in set (0.08 sec)

	Query OK, 0 rows affected, 1 warning (0.08 sec)
	
Hopefully an updated *stored procedure* will come out of the zabbix forum to prevent this issue from coming up again.