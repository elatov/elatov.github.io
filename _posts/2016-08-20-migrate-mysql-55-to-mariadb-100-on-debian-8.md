---
published: true
layout: post
title: "Migrate MySQL 5.5 to MariaDB 10.0 on Debian 8"
author: Karim Elatov
categories: [os]
tags: [linux,debian,mysql,mariadb]
---
I kept hearing good things about **mariadb** and it seems like a lot of OSes are using **mariadb** by default now adays (like [Redhat](http://www.zdnet.com/article/red-hat-will-switch-from-oracle-mysql-to-mariadb-reports/)). There are also a couple of sites that talk about the benefits to moving to mariadb ([10 reasons to migrate to MariaDB (if still using MySQL)](https://seravo.fi/2015/10-reasons-to-migrate-to-mariadb-if-still-using-mysql)). So I decided to migrate my MySQL install to MariaDB. 

### Backup Database
It's of course recommended to backup your databases. Here is the command that should grab everything you need:

	mysqldump -u root -p -A --events --routines > mysqldump.sql

### In Place Upgrade
Since MariaDB is a replacement for MySQL we can just install it on top of MySQL and it automatically migrate all the DBs. Here is how it looked like on the Debian machine:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-10 08:59:27]
	└─[0] <> sudo apt-get install mariadb-server
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following packages were automatically installed and are no longer required:
	  dbconfig-common libconfig-inifiles-perl libsnmp-perl snmptt
	Use 'apt-get autoremove' to remove them.
	The following extra packages will be installed:
	  mariadb-client-10.0 mariadb-client-core-10.0 mariadb-common
	  mariadb-server-10.0 mariadb-server-core-10.0
	Suggested packages:
	  mariadb-test tinyca
	The following packages will be REMOVED:
	  mysql-client mysql-client-5.5 mysql-server mysql-server-5.5
	  mysql-server-core-5.5
	The following NEW packages will be installed:
	  mariadb-client-10.0 mariadb-client-core-10.0 mariadb-common mariadb-server
	  mariadb-server-10.0 mariadb-server-core-10.0
	0 upgraded, 6 newly installed, 5 to remove and 0 not upgraded.
	Need to get 11.8 MB of archives.
	After this operation, 37.3 MB of additional disk space will be used.
	Do you want to continue? [Y/n] Y
	Get:1 http://ftp.us.debian.org/debian/ jessie/main mariadb-client-10.0 amd64 10.0.23-0+deb8u1 [1,144 kB]
	Get:2 http://ftp.us.debian.org/debian/ jessie/main mariadb-common all 10.0.23-0+deb8u1 [16.6 kB]
	Get:3 http://ftp.us.debian.org/debian/ jessie/main mariadb-client-core-10.0 amd64 10.0.23-0+deb8u1 [798 kB]
	Get:4 http://ftp.us.debian.org/debian/ jessie/main mariadb-server-core-10.0 amd64 10.0.23-0+deb8u1 [4,251 kB]
	Get:5 http://ftp.us.debian.org/debian/ jessie/main mariadb-server-10.0 amd64 10.0.23-0+deb8u1 [5,573 kB]
	Get:6 http://ftp.us.debian.org/debian/ jessie/main mariadb-server all 10.0.23-0+deb8u1 [16.3 kB]
	Fetched 11.8 MB in 38s (308 kB/s)                                              
	Preconfiguring packages ...
	(Reading database ... 101816 files and directories currently installed.)
	Removing mysql-server (5.5.47-0+deb8u1) ...
	Removing mysql-server-5.5 (5.5.47-0+deb8u1) ...
	Removing mysql-client (5.5.47-0+deb8u1) ...
	dpkg: mysql-client-5.5: dependency problems, but removing anyway as you requested:
	 zabbix-server-mysql depends on mysql-client | virtual-mysql-client; however:
	  Package mysql-client is not installed.
	  Package mysql-client-5.5 which provides mysql-client is to be removed.
	  Package virtual-mysql-client is not installed.
	  Package mysql-client-5.5 which provides virtual-mysql-client is to be removed.
	 zabbix-server-mysql depends on mysql-client | virtual-mysql-client; however:
	  Package mysql-client is not installed.
	  Package mysql-client-5.5 which provides mysql-client is to be removed.
	  Package virtual-mysql-client is not installed.
	  Package mysql-client-5.5 which provides virtual-mysql-client is to be removed.
	
	Removing mysql-client-5.5 (5.5.47-0+deb8u1) ...
	Processing triggers for man-db (2.7.0.2-5) ...
	Selecting previously unselected package mariadb-client-10.0.
	(Reading database ... 101678 files and directories currently installed.)
	Preparing to unpack .../mariadb-client-10.0_10.0.23-0+deb8u1_amd64.deb ...
	Unpacking mariadb-client-10.0 (10.0.23-0+deb8u1) ...
	Selecting previously unselected package mariadb-common.
	Preparing to unpack .../mariadb-common_10.0.23-0+deb8u1_all.deb ...
	Unpacking mariadb-common (10.0.23-0+deb8u1) ...
	Selecting previously unselected package mariadb-client-core-10.0.
	Preparing to unpack .../mariadb-client-core-10.0_10.0.23-0+deb8u1_amd64.deb ...
	Unpacking mariadb-client-core-10.0 (10.0.23-0+deb8u1) ...
	Processing triggers for man-db (2.7.0.2-5) ...
	(Reading database ... 101726 files and directories currently installed.)
	Removing mysql-server-core-5.5 (5.5.47-0+deb8u1) ...
	Processing triggers for man-db (2.7.0.2-5) ...
	Selecting previously unselected package mariadb-server-core-10.0.
	(Reading database ... 101638 files and directories currently installed.)
	Preparing to unpack .../mariadb-server-core-10.0_10.0.23-0+deb8u1_amd64.deb ...
	Unpacking mariadb-server-core-10.0 (10.0.23-0+deb8u1) ...
	Processing triggers for man-db (2.7.0.2-5) ...
	Setting up mariadb-common (10.0.23-0+deb8u1) ...
	Selecting previously unselected package mariadb-server-10.0.
	(Reading database ... 101720 files and directories currently installed.)
	Preparing to unpack .../mariadb-server-10.0_10.0.23-0+deb8u1_amd64.deb ...
	Unpacking mariadb-server-10.0 (10.0.23-0+deb8u1) ...
	Selecting previously unselected package mariadb-server.
	Preparing to unpack .../mariadb-server_10.0.23-0+deb8u1_all.deb ...
	Unpacking mariadb-server (10.0.23-0+deb8u1) ...
	Processing triggers for man-db (2.7.0.2-5) ...
	Processing triggers for systemd (215-17+deb8u4) ...
	Setting up mariadb-client-core-10.0 (10.0.23-0+deb8u1) ...
	Setting up mariadb-client-10.0 (10.0.23-0+deb8u1) ...
	Setting up mariadb-server-core-10.0 (10.0.23-0+deb8u1) ...
	Setting up mariadb-server-10.0 (10.0.23-0+deb8u1) ...
	Installing new version of config file /etc/apparmor.d/usr.sbin.mysqld ...
	Installing new version of config file /etc/init.d/mysql ...
	Installing new version of config file /etc/logrotate.d/mysql-server ...
	
	Configuration file '/etc/mysql/conf.d/mysqld_safe_syslog.cnf'
	 ==> Modified (by you or by a script) since installation.
	 ==> Package distributor has shipped an updated version.
	   What would you like to do about it ?  Your options are:
	    Y or I  : install the package maintainer's version
	    N or O  : keep your currently-installed version
	      D     : show the differences between the versions
	      Z     : start a shell to examine the situation
	 The default action is to keep your current version.
	*** mysqld_safe_syslog.cnf (Y/I/N/O/D/Z) [default=N] ? Y
	Installing new version of config file /etc/mysql/conf.d/mysqld_safe_syslog.cnf ...
	Installing new version of config file /etc/mysql/debian-start ...
	160410  9:06:03 [Note] /usr/sbin/mysqld (mysqld 10.0.23-MariaDB-0+deb8u1-log) starting as process 15654 ...
	160410  9:06:03 [Note] InnoDB: Using mutexes to ref count buffer pool pages
	160410  9:06:03 [Note] InnoDB: The InnoDB memory heap is disabled
	160410  9:06:03 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
	160410  9:06:03 [Note] InnoDB: Memory barrier is not used
	160410  9:06:03 [Note] InnoDB: Compressed tables use zlib 1.2.8
	160410  9:06:03 [Note] InnoDB: Using Linux native AIO
	160410  9:06:03 [Note] InnoDB: Using CPU crc32 instructions
	160410  9:06:03 [Note] InnoDB: Initializing buffer pool, size = 2.0G
	160410  9:06:03 [Note] InnoDB: Completed initialization of buffer pool
	160410  9:06:03 [Note] InnoDB: Highest supported file format is Barracuda.
	160410  9:06:04 [Note] InnoDB: 128 rollback segment(s) are active.
	160410  9:06:04 [Note] InnoDB: Waiting for purge to start
	160410  9:06:04 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.26-76.0 started; log sequence number 286222197
	160410  9:06:04 [Note] Plugin 'FEEDBACK' is disabled.
	160410  9:06:04 [Note] InnoDB: FTS optimize thread exiting.
	160410  9:06:04 [Note] InnoDB: Starting shutdown...
	160410  9:06:06 [Note] InnoDB: Shutdown completed; log sequence number 286222207
	Setting up mariadb-server (10.0.23-0+deb8u1) ...
	Processing triggers for systemd (215-17+deb8u4) ...

During the install a prompt popped up asking if I wanted to migrate:

![mariadb-upgrade-screen](https://seacloud.cc/d/480b5e8fcd/files/?p=/mig-mysql-to-mariadb/mariadb-upgrade-screen.png&raw=1)

I ended up choosing the **Migrate** option.

### Checking Mysql_Upgrade Results

By default the install will run **mysql_upgrade** automatically, if want to check out the results you can check out the logs (**/var/log/syslog**) and you should see something similar to this:

	Apr 10 09:06:12 kerch mysqld_safe: Starting mysqld daemon with databases from /var/lib/mysql
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] /usr/sbin/mysqld (mysqld 10.0.23-MariaDB-0+deb8u1-log) starting as process 15971 ...
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Using mutexes to ref count buffer pool pages
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: The InnoDB memory heap is disabled
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Memory barrier is not used
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Compressed tables use zlib 1.2.8
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Using Linux native AIO
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Using CPU crc32 instructions
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Initializing buffer pool, size = 2.0G
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Completed initialization of buffer pool
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Highest supported file format is Barracuda.
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: 128 rollback segment(s) are active.
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB: Waiting for purge to start
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.26-76.0 started; log sequence number 286222227
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] Plugin 'FEEDBACK' is disabled.
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] Server socket created on IP: '0.0.0.0'.
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [ERROR] Incorrect definition of table mysql.event: expected column 'sql_mode' at position 14 to have type set('REAL_AS_FLOAT','PIPES_AS_CONCAT','ANSI_QUOTES','IGNORE_SPACE','IGNORE_BAD_TABLE_OPTIONS','ONLY_FULL_GROUP_BY','NO_UNSIGNED_SUBTRACTION','NO_DIR_IN_CREATE','POSTGRESQL','ORACLE','MSSQL','DB2','MAXDB','NO_KEY_OPTIONS','NO_TABLE_OPTIONS','NO_FIELD_OPTIONS','MYSQL323','MYSQL40','ANSI','NO_AUTO_VALUE_ON_ZERO','NO_BACKSLASH_ESCAPES','STRICT_TRANS_TABLES','STRICT_ALL_TABLES','NO_ZERO_IN_DATE','NO_ZERO_DATE','INVALID_DATES','ERROR_FOR_DIVISION_BY_ZERO','TRADITIONAL','NO_AUTO_CREATE_USER','HIGH_NOT_PRECEDENCE','NO_ENGINE_SUBSTITUTION','PAD_CHAR_TO_FULL_LENGTH'), found type set('REAL_AS_FLOAT','PIPES_AS_CONCAT','ANSI_QUOTES','IGNORE_SPACE','NOT_USED','ONLY_FULL_GROUP_BY','NO_UNSIGNED_SUBTRACTION','NO_DIR_IN_CREATE','POSTGRESQL','ORACLE','MSSQL','DB2','MAXDB','NO_KEY_OPTIONS','NO_TABLE_OPTIONS','NO_FIELD_OPTIONS','MYSQL323','MYSQL40','ANSI','NO_AUTO_VALUE_ON_ZERO','NO_BACKSLASH_ESCAPES','STRICT
	Apr 10 09:06:12 kerch mysqld: _TRANS_TABLES','STRICT_A
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [ERROR] mysqld: Event Scheduler: An error occurred when initializing system tables. Disabling the Event Scheduler.
	Apr 10 09:06:12 kerch mysqld: 160410  9:06:12 [Note] /usr/sbin/mysqld: ready for connections.
	Apr 10 09:06:12 kerch mysqld: Version: '10.0.23-MariaDB-0+deb8u1-log'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  (Debian)
	Apr 10 09:06:13 kerch mysql[15780]: Starting MariaDB database server: mysqld.
	Apr 10 09:06:13 kerch /etc/mysql/debian-start[16020]: Upgrading MySQL tables if necessary.
	Apr 10 09:06:13 kerch mysqld: 160410  9:06:13 [Note] View `snorby`.`aggregated_events`: the version is set to 100023
	Apr 10 09:06:13 kerch mysqld: 160410  9:06:13 [Note] View `snorby`.`events_with_join`: the version is set to 100023
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: /usr/bin/mysql_upgrade: the '--basedir' option is always ignored
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Looking for 'mysql' as: /usr/bin/mysql
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Looking for 'mysqlcheck' as: /usr/bin/mysqlcheck
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: MySQL upgrade detected
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 1/6: Checking and upgrading mysql database
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Processing databases
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.column_stats                                 OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.columns_priv                                 OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.db                                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.event                                        OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.func                                         OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.gtid_slave_pos                               OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.help_category                                OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.help_keyword                                 OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.help_relation                                OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.help_topic                                   OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.host                                         OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.index_stats                                  OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.innodb_index_stats                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.innodb_table_stats                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.ndb_binlog_index                             OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.plugin                                       OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.proc                                         OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.procs_priv                                   OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.proxies_priv                                 OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.roles_mapping                                OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.servers                                      OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.table_stats                                  OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.tables_priv                                  OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.time_zone                                    OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.time_zone_leap_second                        OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.time_zone_name                               OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.time_zone_transition                         OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.time_zone_transition_type                    OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql.user                                         OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 2/6: Fixing views from mysql
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Processing databases
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: information_schema
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: performance_schema
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby.aggregated_events                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby.events_with_join                            OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 3/6: Running 'mysql_fix_privilege_tables'
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 4/6: Fixing table and database names
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Processing databases
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: information_schema
	Apr 10 09:06:14 kerch rsyslogd-2007: action 'action 26' suspended, next retry is Sun Apr 10 09:06:44 2016 [try http://www.rsyslog.com/e/2007 ]
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: mysql
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: performance_schema
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 5/6: Checking and upgrading tables
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Processing databases
		Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: information_schema
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: performance_schema
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby.agent_asset_names                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby.asset_names                                 OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: snorby.users                                       OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress.wp_commentmeta                           OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress.wp_comments                              OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: wordpress.wp_wpo_log                               OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix.acknowledges                                OK
		Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix.graphs                                      OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: zabbix.valuemaps                                   OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: Phase 6/6: Running 'FLUSH PRIVILEGES'
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16023]: OK
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16074]: Checking for insecure root accounts.
	Apr 10 09:06:14 kerch /etc/mysql/debian-start[16078]: Triggering
	myisam-recover for all MyISAM tables

I think the error about the **event** table is because the **mysql_upgrade** hasn't been executed yet, as per [this](https://www.allscoop.com/mariadb-incorrect-definition-table-mysql-event-expected-column-sql_mode.php) page. Plus I double checked the service, and I noticed that's it was already running:

	┌─[elatov@kerch]  - [/home/elatov] - [2016-04-10 09:24:29]
	└─[0] <> sudo systemctl enable mysql
	Synchronizing state for mysql.service with sysvinit using update-rc.d...
	Executing /usr/sbin/update-rc.d mysql defaults
	Executing /usr/sbin/update-rc.d mysql enable
	┌─[elatov@kerch] - [/home/elatov] - [2016-04-10 09:24:40]
	└─[0] <> sudo systemctl status mysql
	● mysql.service - LSB: Start and stop the mysql database server daemon
	   Loaded: loaded (/etc/init.d/mysql)
	   Active: active (running) since Sun 2016-04-10 09:06:13 MDT; 18min ago
	   CGroup: /system.slice/mysql.service
	           ├─15804 /bin/bash /usr/bin/mysqld_safe
	           ├─15805 logger -p daemon.err -t /etc/init.d/mysql -i
	           ├─15971 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/mysql/plugin --user=mysql --skip-log-error --open-files-l...
	           └─15972 logger -t mysqld -p daemon.error

If you really want you can re-run the **mysql_upgrade** to make sure everything is okay:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-10 12:01:48]
	└─[1] <> mysql_upgrade -u root -p
	Enter password:
	Phase 1/6: Checking and upgrading mysql database
	Processing databases
	mysql
	mysql.column_stats                                 OK
	mysql.columns_priv                                 OK
	mysql.db                                           OK
	mysql.event                                        OK
	mysql.func                                         OK
	mysql.gtid_slave_pos                               OK
	mysql.help_category                                OK
	mysql.help_keyword                                 OK
	mysql.help_relation                                OK
	mysql.help_topic                                   OK
	mysql.host                                         OK
	mysql.index_stats                                  OK
	mysql.innodb_index_stats                           OK
	mysql.innodb_table_stats                           OK
	mysql.ndb_binlog_index                             OK
	mysql.plugin                                       OK
	mysql.proc                                         OK
	mysql.procs_priv                                   OK
	mysql.proxies_priv                                 OK
	mysql.roles_mapping                                OK
	mysql.servers                                      OK
	mysql.table_stats                                  OK
	mysql.tables_priv                                  OK
	mysql.time_zone                                    OK
	mysql.time_zone_leap_second                        OK
	mysql.time_zone_name                               OK
	mysql.time_zone_transition                         OK
	mysql.time_zone_transition_type                    OK
	mysql.user                                         OK
	Phase 2/6: Fixing views
	snorby.aggregated_events                           OK
	snorby.events_with_join                            OK
	Phase 3/6: Running 'mysql_fix_privilege_tables'
	Phase 4/6: Fixing table and database names
	Phase 5/6: Checking and upgrading tables
	Processing databases
	information_schema
	performance_schema
	snorby
	snorby.agent_asset_names                           OK
	snorby.users                                       OK
	wordpress
	wordpress.wp_wpo_campaign_post                     OK
	wordpress.wp_wpo_campaign_word                     OK
	wordpress.wp_wpo_log                               OK
	zabbix
	zabbix.acknowledges                                OK
	zabbix.actions                                     OK
	zabbix.valuemaps                                   OK
	Phase 6/6: Running 'FLUSH PRIVILEGES'
	OK

And you'll see the version you are at:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-10 12:06:23]
	└─[1] <> sudo cat /var/lib/mysql/mysql_upgrade_info
	10.0.23-MariaDB%


### Confirm Connections

As a quick sanity check we can log into **mariadb** and make sure we can see all Databases:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-10 09:27:30]
	└─[0] <> mysql -u root -p
	Enter password:
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 154
	Server version: 10.0.23-MariaDB-0+deb8u1-log (Debian)
	
	Copyright (c) 2000, 2015, Oracle, MariaDB Corporation Ab and others.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	MariaDB [(none)]> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| mysql              |
	| performance_schema |
	| snorby             |
	| wordpress          |
	| zabbix             |
	+--------------------+
	8 rows in set (0.00 sec)
	
	MariaDB [(none)]>


Starting up all the old programs, I saw that they were making connections to
the DB:

	MariaDB [(none)]> show processlist;
	+------+--------+--------------------+--------+---------+------+-------+------------------+----------+
	| Id   | User   | Host               | db     | Command | Time | State | Info             | Progress |
	+------+--------+--------------------+--------+---------+------+-------+------------------+----------+
	|  131 | zabbix | localhost          | zabbix | Sleep   | 9955 |       | NULL             |    0.000 |
	|  148 | zabbix | localhost          | zabbix | Sleep   |  720 |       | NULL             |    0.000 |
	|  149 | zabbix | localhost          | zabbix | Sleep   |  821 |       | NULL             |    0.000 |
	|  150 | zabbix | localhost          | zabbix | Sleep   |  910 |       | NULL             |    0.000 |
	|  151 | zabbix | localhost          | zabbix | Sleep   |  864 |       | NULL             |    0.000 |
	|  153 | zabbix | localhost          | zabbix | Sleep   |   52 |       | NULL             |    0.000 |
	|  178 | snorby | localhost          | snorby | Sleep   |    0 |       | NULL             |    0.000 |
	|  181 | snorby | moxz.dnsd.me:15356 | snorby | Sleep   | 9213 |       | NULL             |    0.000 |
	| 1031 | root   | localhost          | NULL   | Query   |    0 | init  | show processlist |    0.000 |
	+------+--------+--------------------+--------+---------+------+-------+------------------+----------+
	25 rows in set (0.00 sec)

Overall I think the process went really well. I only had a couple of Databases and I was only using the InnoDB Engine so I didn't run into any trouble.
