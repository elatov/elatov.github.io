---
published: true
layout: post
title: "Migrate MariaDB from Debian 8 to FreeBSD 10"
author: Karim Elatov
categories: [os]
tags: [linux,debian,freebsd,mariadb]
---
Recently I migrated my MySQL instance to MariaDB and everything was working as expected. I was moving some resources around and I decided to free up my Debian machine. So I decided to move the **mariadb** instance to my FreeBSD machine.

### Install MariaDB on FreeBSD
The Debian version of **mariadb** was the following (**10.0.23**):

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-17 03:50:50]
	└─[0] <> dpkg -l | grep mariadb-server-10.0
	ii  mariadb-server-10.0                   10.0.23-0+deb8u1                     amd64        MariaDB database server binaries

Luckily FreeBSD had that version as well (**10.0.23**):

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 03:51:49]
	└─[0] <> pkg search mariadb | grep server
	mariadb100-server-10.0.23      Multithreaded SQL database (server)
	mariadb101-server-10.1.13      Multithreaded SQL database (server)
	mariadb55-server-5.5.47        Multithreaded SQL database (server)

It looks like it has a later version as well (maybe I will update later), but for now I will install the same version of **mariadb** so the migration has less changes/risks. To install I just ran the following:

	sudo pkg install mariadb100-server

Then I added the following to the **/etc/rc.conf** file:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 03:47:20]
	└─[0] <> grep mysql /etc/rc.conf
	mysql_enable="YES"
	mysql_optfile=/usr/local/my.cnf
	mysql_pidfile=/var/run/mysqld/mysqld.pid

To make sure the **mysql** user can create/write the pid file, I created the directory under **/var/run** and made sure the **mysql** user owns it:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 03:55:14]
	└─[0] <> ls -ld /var/run/mysqld
	drwxr-xr-x  2 mysql  wheel  512 Apr 17 15:27 /var/run/mysqld

I had some options on the Debian machine that I decided to move over. The **/usr/local/my.cnf** file was pretty empty so at the bottom I added an **include** statement to point to where all the configs were. Here is how the file looked like:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 03:56:11]
	└─[0] <> grep -vE '^$|^#' /usr/local/my.cnf
	[mysqld]
	sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
	!includedir /usr/local/etc/mysql/conf.d/

Then I copied most of the settings over from the Debian machine and broke them down by file:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 03:59:27]
	└─[0] <> ls /usr/local/etc/mysql/conf.d
	client.cnf            mysqld_log.cnf
	mysql_innodb_data.cnf mysqld_safe.cnf
	mysqld.cnf            mysqldump.cnf

Here is the main config that I just copied from Debian (don't forget to open port **3306** if you are running a firewall):

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:02:30]
	└─[0] <> grep -vE '^$|^#' /usr/local/etc/mysql/conf.d/mysqld.cnf
	[mysqld]
	user        = mysql
	pid-file    = /var/run/mysqld/mysqld.pid
	socket      = /tmp/mysql.sock
	port        = 3306
	basedir     = /usr/local
	datadir     = /var/db/mysql
	tmpdir      = /tmp
	skip-external-locking
	bind-address        = 0.0.0.0
	key_buffer_size     = 16M
	max_allowed_packet  = 16M
	thread_stack        = 192K
	thread_cache_size       = 8
	query_cache_limit   = 1M
	query_cache_size        = 16M

The *log* config put all of the log files under **/var/log/mysql**, so I created the directory just like the **/var/run** one:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:00:10]
	└─[0] <> ls -ld /var/log/mysql
	drwxr-xr-x  2 mysql  wheel  512 Apr 17 12:30 /var/log/mysql

Then I created a **newsyslogd** config as well just to make sure they don't take that much space over time:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:01:12]
	└─[0] <> cat /etc/newsyslog.conf.d/mysql
	/var/log/mysql/mysql-slow.log mysql:mysql 644 3 100 * JC  /var/run/mysqld/mysqld.pid
	/var/log/mysql/mysql.log mysql:mysql 644 3 100 * JC  /var/run/mysqld/mysqld.pid
	/var/log/mysql/mysql_error.log mysql:mysql 644 3 100 * JC  /var/run/mysqld/mysqld.pid
	
At this point I started **mariadb** and it was okay:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 12:05:27]
	└─[0] <> sudo service mysql-server start
	Starting mysql.
	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 12:05:46]
	└─[0] <> sudo service mysql-server status
	mysql is running as pid 96398.

Here are all the parameters that ended up getting set for **mariadb**:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:03:02]
	└─[0] <> ps -auwwx | grep mysql
	mysql     8103   0.0  0.1   17100   2196  -  Is    3:27PM    0:00.01 /bin/sh /usr/local/bin/mysqld_safe --defaults-extra-file=/usr/local/my.cnf --user=mysql --datadir=/var/db/mysql --pid-file=/var/run/mysqld/mysqld.pid
	mysql     8353   0.0 12.8 2603132 264344  -  I     3:27PM    0:06.28 /usr/local/libexec/mysqld --defaults-extra-file=/usr/local/my.cnf --basedir=/usr/local --datadir=/var/db/mysql --plugin-dir=/usr/local/lib/mysql/plugin --log-error=/var/log/mysql/mysql_error.log --open-files-limit=15000 --pid-file=/var/run/mysqld/mysqld.pid --socket=/tmp/mysql.sock --port=3306

And here is what I saw the logs:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 12:40:33]
	└─[1] <> tail -f /var/log/mysql/mysql_error.log
	160417 12:30:31 mysqld_safe Starting mysqld daemon with databases from /var/db/mysql
	160417 12:30:31 [Note] /usr/local/libexec/mysqld (mysqld 10.0.23-MariaDB-log) starting as process 98767 ...
	160417 12:30:31 [Note] InnoDB: Using mutexes to ref count buffer pool pages
	160417 12:30:31 [Note] InnoDB: The InnoDB memory heap is disabled
	160417 12:30:31 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
	160417 12:30:31 [Note] InnoDB: Memory barrier is not used
	160417 12:30:31 [Note] InnoDB: Compressed tables use zlib 1.2.8
	160417 12:30:31 [Note] InnoDB: Using CPU crc32 instructions
	160417 12:30:31 [Note] InnoDB: Initializing buffer pool, size = 2.0G
	160417 12:30:31 [Note] InnoDB: Completed initialization of buffer pool
	160417 12:30:31 [Note] InnoDB: Highest supported file format is Barracuda.
	160417 12:30:32 [Note] InnoDB: 128 rollback segment(s) are active.
	160417 12:30:32 [Note] InnoDB: Waiting for purge to start
	160417 12:30:32 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.26-76.0 started; log sequence number 1026386743
	160417 12:30:32 [Note] Server socket created on IP: '0.0.0.0'.
	160417 12:30:32 [Note] /usr/local/libexec/mysqld: ready for connections.
	Version: '10.0.23-MariaDB-log'  socket: '/tmp/mysql.sock'  port: 3306  FreeBSD Ports


### Quick Performance Comparison
I installed **sysbench** on the Debian machine (`sudo apt-get install sysbench`) and first I created a test database in **mariadb**:

	MariaDB [(none)]> create database ptest;

Next I prepared the data:

	$ sysbench --test=oltp --oltp-table-size=1000000 --mysql-db=ptest --mysql-user=USER --mysql-password=PASSWORD prepare

And now for the run:

	$ sysbench --test=oltp --oltp-table-size=1000000 --oltp-test-mode=complex --oltp-read-only=off --num-threads=6 --max-time=60 --max-requests=0 --mysql-db=ptest --mysql-user=USER --mysql-password=PASSWORD run

And here is what I saw:

	sysbench 0.4.12:  multi-threaded system evaluation benchmark
	
	No DB drivers specified, using mysql
	Running the test with following options:
	Number of threads: 6
	
	Doing OLTP test.
	Running mixed OLTP test
	Using Special distribution (12 iterations,  1 pct of values are returned in 75 pct cases)
	Using "BEGIN" for starting transactions
	Using auto_inc on the id column
	Threads started!
	Time limit exceeded, exiting...
	(last message repeated 5 times)
	Done.
	
	OLTP test statistics:
	    queries performed:
	        read:                            375340
	        write:                           134050
	        other:                           53620
	        total:                           563010
	    transactions:                        26810  (446.80 per sec.)
	    deadlocks:                           0      (0.00 per sec.)
	    read/write requests:                 509390 (8489.18 per sec.)
	    other operations:                    53620  (893.60 per sec.)
	
	Test execution summary:
	    total time:                          60.0046s
	    total number of events:              26810
	    total time taken by event execution: 359.8723
	    per-request statistics:
	         min:                                  2.25ms
	         avg:                                 13.42ms
	         max:                                 40.72ms
	         approx.  95 percentile:              22.89ms
	
	Threads fairness:
	    events (avg/stddev):           4468.3333/6.50
	    execution time (avg/stddev):   59.9787/0.00

Then if want you can clean up the data:

	$ sysbench --test=oltp --mysql-db=ptest --mysql-user=USER --mysql-password=PASSWD cleanup

When I tried installing **sysbench** on FreeBSD it depended on **mysql56** package which would remove the **mariadb** package:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:15:36]
	└─[0] <> sudo pkg install sysbench
	Updating FreeBSD repository catalogue...
	FreeBSD repository is up-to-date.
	All repositories are up-to-date.
	
	Checking integrity... done (1 conflicting)
	Checking integrity... done (0 conflicting)
	The following 4 package(s) will be affected (of 0 checked):
	
	Installed packages to be REMOVED:
		mariadb100-client-10.0.23
		mariadb100-server-10.0.23
	
	New packages to be INSTALLED:
		sysbench: 0.4.12_3
		mysql56-client: 5.6.27
	
	The operation will free 150 MiB.
	
	Proceed with this action? [y/N]:

So I just downloaded the package:

	sudo pkg install --fetch-only sysbench

And then the package is stored under **/var/cache/pkg**:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:15:18]
	└─[0] <> ls -l /var/cache/pkg/sysbench-0.4.12_3*
	-rw-r--r--  1 root  wheel  51340 Mar 29 09:27 /var/cache/pkg/sysbench-0.4.12_3-563437926d.txz
	lrwxr-xr-x  1 root  wheel     32 Apr 16 20:40 /var/cache/pkg/sysbench-0.4.12_3.txz -> sysbench-0.4.12_3-563437926d.txz

At that point you can just extract it using **tar**. After that **sysbench** worked without issues:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:06:46]
	└─[0] <> which sysbench
	/usr/local/bin/sysbench
	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:17:35]
	└─[0] <> sysbench --version
	sysbench 0.4.12

Running the same **sysbench** commands as above I saw the following results:

	sysbench 0.4.12:  multi-threaded system evaluation benchmark
	
	No DB drivers specified, using mysql
	Running the test with following options:
	Number of threads: 6
	
	Doing OLTP test.
	Running mixed OLTP test
	Using Special distribution (12 iterations,  1 pct of values are returned in 75 pct cases)
	Using "BEGIN" for starting transactions
	Using auto_inc on the id column
	Threads started!
	Time limit exceeded, exiting...
	(last message repeated 5 times)
	Done.
	
	OLTP test statistics:
	    queries performed:
	        read:                            355194
	        write:                           126855
	        other:                           50742
	        total:                           532791
	    transactions:                        25371  (422.76 per sec.)
	    deadlocks:                           0      (0.00 per sec.)
	    read/write requests:                 482049 (8032.49 per sec.)
	    other operations:                    50742  (845.52 per sec.)
	
	Test execution summary:
	    total time:                          60.0124s
	    total number of events:              25371
	    total time taken by event execution: 359.8753
	    per-request statistics:
	         min:                                  3.24ms
	         avg:                                 14.18ms
	         max:                                267.57ms
	         approx.  95 percentile:              24.26ms
	
	Threads fairness:
	    events (avg/stddev):           4228.5000/35.88
	    execution time (avg/stddev):   59.9792/0.00

Debian performed a little better and I was okay with that, I didn't need crazy  query performance in my home lab. I just wanted to make sure the difference wasn't huge.

### Migrate all the DBs and other stuff
I ran into [this](http://dba.stackexchange.com/questions/46129/does-mysqldump-all-databases-include-all-objects) page which talked about the following command grabbing most of everything:

	mysqldump --events --routines --triggers --all-databases -u root -p > dbs-routines.sql

After that I copied the **sql** file over to the FreeBSD machine:

	rsync -avzP dbs-routines.sql moxz:

Then I imported all the information:

	mysql -u root -p < dbs-routines.sql

After that the databases were all there:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:17:38]
	└─[0] <> mysql -u root -p
	Enter password:
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 109
	Server version: 10.0.23-MariaDB-log FreeBSD Ports
	
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
	9 rows in set (0.00 sec)

I also double checked and all the **stored procedures** were moved over as well:

	MariaDB [(none)]> SHOW PROCEDURE STATUS;
	+--------+---------------------------+-----------+----------------+---------------------+---------------------+---------------+---------+----------------------+----------------------+--------------------+
	| Db     | Name                      | Type      | Definer        | Modified            | Created             | Security_type | Comment | character_set_client | collation_connection | Database Collation |
	+--------+---------------------------+-----------+----------------+---------------------+---------------------+---------------+---------+----------------------+----------------------+--------------------+
	| zabbix | partition_create          | PROCEDURE | root@localhost | 2016-04-17 11:50:09 | 2016-04-17 11:50:09 | DEFINER       |         | utf8                 | utf8_general_ci      | utf8_general_ci    |
	| zabbix | partition_drop            | PROCEDURE | root@localhost | 2016-04-17 11:50:09 | 2016-04-17 11:50:09 | DEFINER       |         | utf8                 | utf8_general_ci      | utf8_general_ci    |
	| zabbix | partition_maintenance     | PROCEDURE | root@localhost | 2016-04-17 11:50:09 | 2016-04-17 11:50:09 | DEFINER       |         | utf8                 | utf8_general_ci      | utf8_general_ci    |
	| zabbix | partition_maintenance_all | PROCEDURE | root@localhost | 2016-04-17 11:50:09 | 2016-04-17 11:50:09 | DEFINER       |         | utf8                 | utf8_general_ci      | utf8_general_ci    |
	| zabbix | partition_verify          | PROCEDURE | root@localhost | 2016-04-17 11:50:09 | 2016-04-17 11:50:09 | DEFINER       |         | utf8                 | utf8_general_ci      | utf8_general_ci    |
	+--------+---------------------------+-----------+----------------+---------------------+---------------------+---------------+---------+----------------------+----------------------+--------------------+
	5 rows in set (0.01 sec)

I was pretty happy with that.

### Migrate Users and Privileges
I then ran into [this](http://dba.stackexchange.com/questions/100511/backup-restore-users-passwords-privileges) page and it talked about moving the **users** over. So then I dumped the **user** table:

	mysqldump -u root -p mysql user > user_table_dump.sql

Then copied it over:

	rsync -avzP user_table_dump.sql moxz:

Then on the other side I imported the table:

	mysql -u root -p mysql < user_table_dump.sql

After **flushing privileges**, I saw my **users** and the **grants** as well:

	MariaDB [mysql]> select Host, user from user ;
	+-----------+------------------+
	| Host      | user             |
	+-----------+------------------+
	| localhost | debian-sys-maint |
	| localhost | root             |
	| localhost | snorby           |
	| localhost | wordpress        |
	| localhost | zabbix           |
	+-----------+------------------+
	6 rows in set (0.00 sec)
	
	MariaDB [mysql]> show grants for 'zabbix'@'localhost';
	+-------------------------------------------------------------------------+
	| Grants for zabbix@localhost                                                                                   	|
	+-------------------------------------------------------------------------+
	| GRANT USAGE ON *.* TO 'zabbix'@'localhost' IDENTIFIED BY PASSWORD 'kjk' |
	| GRANT ALL PRIVILEGES ON `zabbix`.* TO 'zabbix'@'localhost'                                                    	|
	+-------------------------------------------------------------------------+
	2 rows in set (0.00 sec)

### Finishing up
I then modified *zabbix*, *wordpress*, and *snorby* to point to the remote database. I also added new **Grants** to allow remote access for the dedicated users. And lastly I ended up opening the remote port:

	┌─[elatov@moxz] - [/home/elatov] - [2016-04-17 04:35:11]
	└─[0] <> sudo pfctl -s rules | grep mysql
	pass in on em0 inet proto tcp from 10.0.0.0/24 to any port = mysql flags S/SA keep state

After all of that it worked out pretty well.