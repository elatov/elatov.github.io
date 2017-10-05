---
published: true
layout: post
title: "Migrating MariaDB to Docker"
author: Karim Elatov
categories: [containers]
tags: [docker,mariadb,freebsd]
---
So a while back I [moved my Mariadb instance to my FreeBSD](/2016/09/migrate-mariadb-from-debian-8-to-freebsd-10/) VM. Now that I was playing around with **docker**, I wanted to move the **mariadb** install to **docker** and see how it fares.

### Update Mariabdb On FreeBSD
Before the migration I wanted to update **mariadb** to the latest version and then export the DBs and import them to the latest **docker** image which was **10.1.x**. The current version on the FreeBSD VM was **10.0.x**:

    <> pkg info | grep maria
    mariadb100-client-10.0.29_1    Multithreaded SQL database (client)
    mariadb100-server-10.0.29_1    Multithreaded SQL database (server)

And here was the latest available version:

    <> pkg search mariadb101
    mariadb101-client-10.1.21      Multithreaded SQL database (client)
    mariadb101-server-10.1.21      Multithreaded SQL database (server)

So first let's stop all the applications that are using the database and get a dump of all the databases. After I shut down my **zabbix** and other serivices, I confirmed nothing was connected:

    MariaDB [(none)]> show processlist;
    +-------+------+-----------+------+---------+------+-------+------------------+----------+
    | Id    | User | Host      | db   | Command | Time | State | Info             | Progress |
    +-------+------+-----------+------+---------+------+-------+------------------+----------+
    | 23600 | root | localhost | NULL | Query   |    0 | init  | show processlist |    0.000 |
    +-------+------+-----------+------+---------+------+-------+------------------+----------+
    1 row in set (0.00 sec)

#### Backup MariaDB 10.0.x Databases on FreeBSD

I used a similar approach as [I did in the past](/2016/09/migrate-mariadb-from-debian-8-to-freebsd-10/) and I just ran the following:

    $ mysqldump --events --routines --triggers --all-databases -u root -p > freebsd-mdb-03-18-17.sql
    $ mysqldump -u root -p mysql user > freebsd-user_table-03-18-17.sql

Now let's do the update, first let's stop the service:

    <> sudo service mysql-server stop
    Stopping mysql.
    Waiting for PIDS: 933.

For good measure, let's also get a file-level back up. So I just **tar**'ed up the data dir:

    $ cd /var/db
    $ sudo tar cpjf mysql-data-dir-03-18-17.tar.bz2 mysql

Let's also get the configs (we can use these on the **docker** instance later):

    $ cd /usr/local/etc/mysql
    $ sudo tar cpjf mariadb-confd-03-18-17.tar.bz2 conf.d

#### Update MariaDB 10.0.x to 10.1.x on FreeBSD

Now for the actual update:

    <> sudo pkg install mariadb101-server
    Updating FreeBSD repository catalogue...
    FreeBSD repository is up to date.
    All repositories are up to date.
    The following 2 package(s) will be affected (of 0 checked):

    New packages to be INSTALLED:
        mariadb101-server: 10.1.21
        mariadb101-client: 10.1.21

    Number of packages to be installed: 2

    The process will require 208 MiB more space.
    25 MiB to be downloaded.

    Proceed with this action? [y/N]: y
    [1/2] mariadb101-server-10.1.21.txz            :   0%  160 KiB 163.8kB/s    02:2[1/2] mariadb101-server-10.1.21.txz            :  39%    9 MiB   9.3MB/s    00:0[1/2] mariadb101-server-10.1.21.txz            : 100%   23 MiB  12.1MB/s    00:02
    [2/2] mariadb101-client-10.1.21.txz            :   1%   16 KiB  16.4kB/s    01:3[2/2] mariadb101-client-10.1.21.txz            : 100%    1 MiB   1.6MB/s    00:01
    Checking integrity... done (3 conflicting)
      - mariadb101-server-10.1.21 conflicts with mariadb100-server-10.0.29_1 on /usr/local/bin/aria_chk
      - mariadb101-client-10.1.21 conflicts with mariadb100-client-10.0.29_1 on /usr/local/bin/msql2mysql
      - mariadb101-client-10.1.21 conflicts with mariadb100-server-10.0.29_1 on /usr/local/lib/mysql/plugin/daemon_example.ini
    Checking integrity... done (0 conflicting)
    Conflicts with the existing packages have been found.
    One more solver iteration is needed to resolve them.
    The following 5 package(s) will be affected (of 0 checked):

    Installed packages to be REMOVED:
        mariadb100-client-10.0.29_1
        mariadb100-server-10.0.29_1

    New packages to be INSTALLED:
        mariadb101-client: 10.1.21
        mariadb101-server: 10.1.21

    Installed packages to be REINSTALLED:
        pkg-1.10.0_2

    Number of packages to be removed: 2
    Number of packages to be installed: 2
    Number of packages to be reinstalled: 1

    The process will require 9 MiB more space.

    Proceed with this action? [y/N]: y
    [1/5] Deinstalling mariadb100-server-10.0.29_1...
    [1/5] Deleting files for mariadb100-server-10.0.29_1:  15%
    pkg: /usr/local/etc/rc.d/mysql-server different from original checksum, not removing
    [1/5] Deleting files for mariadb100-server-10.0.29_1: 100%
    ==> You should manually remove the "mysql" user.
    ==> You should manually remove the "mysql" group
    [2/5] Deinstalling mariadb100-client-10.0.29_1...
    [2/5] Deleting files for mariadb100-client-10.0.29_1: 100%
    [3/5] Installing mariadb101-client-10.1.21...
    [3/5] Extracting mariadb101-client-10.1.21: 100%
    [4/5] Reinstalling pkg-1.10.0_2...
    [4/5] Extracting pkg-1.10.0_2: 100%
    [5/5] Installing mariadb101-server-10.1.21...
    ===> Creating groups.
    Using existing group 'mysql'.
    ===> Creating users
    Using existing user 'mysql'.
    [5/5] Extracting mariadb101-server-10.1.21: 100%
    Message from mariadb101-client-10.1.21:
    ************************************************************************

    MariaDB respects hier(7) and doesn't check /etc and /etc/mysql for
    my.cnf. Please move existing my.cnf files from those paths to
    /usr/local/etc and /usr/local/etc/mysql.

    ************************************************************************
    Message from mariadb101-server-10.1.21:
    ************************************************************************

    Remember to run mysql_upgrade (with the optional --datadir=<dbdir> flag)
    the first time you start the MySQL server after an upgrade from an
    earlier version.

    MariaDB respects hier(7) and doesn't check /etc and /etc/mysql for
    my.cnf. Please move existing my.cnf files from those paths to
    /usr/local/etc and /usr/local/etc/mysql.

    This port does NOT include the mytop perl script, this is included in
    the MariaDB tarball but the most recent version can be found in the
    databases/mytop port

    ************************************************************************


After the update I started the service:

    $ sudo service mysql-server start

and I saw the followig in the logs:

    170318 11:35:06 mysqld_safe Starting mysqld daemon with databases from /var/db/mysql
    2017-03-18 11:35:06 2210488320 [Note] /usr/local/bin/mysqld (mysqld 10.1.21-MariaDB) starting as process 29452 ...
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Using mutexes to ref count buffer pool pages
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: The InnoDB memory heap is disabled
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Compressed tables use zlib 1.2.8
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Using SSE crc32 instructions
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Initializing buffer pool, size = 1
    .0G
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Completed initialization of buffer pool
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Highest supported file format is Barracuda.
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: 128 rollback segment(s) are active.
    2017-03-18 11:35:06 2210488320 [Note] InnoDB: Waiting for purge to start
    2017-03-18 11:35:06 2210488320 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.34-79.1 started; log sequence number 73665316000
    2017-03-18 11:35:06 3552271616 [Note] InnoDB: Dumping buffer pool(s) not yet started
    2017-03-18 11:35:06 2210488320 [Note] Plugin 'FEEDBACK' is disabled.
    2017-03-18 11:35:06 2210488320 [Note] Server socket created on IP: '0.0.0.0'.
    2017-03-18 11:35:06 d3bb7600 InnoDB: Error: Column last_update in table "mysql"."innodb_table_stats" is INT UNSIGNED NOT NULL but should be BINARY(4) NOT NULL (type mismatch).
    2017-03-18 11:35:06 d3bb7600 InnoDB: Error: Fetch of persistent statistics requested for table "mysql"."gtid_slave_pos" but the required system tables mysql.innodb_table_stats and mysql.innodb_index_stats are not present or have unexpected structure. Using transient stats instead.
    2017-03-18 11:35:06 2210488320 [Note] /usr/local/bin/mysqld: ready for connections.
    Version: '10.1.21-MariaDB'  socket: '/tmp/mysql.sock'  port: 3306  FreeBSD Ports

So now let's do the suggested update:

    <> sudo mysql_upgrade
    Phase 1/6: Checking and upgrading mysql database
    Processing databases
    mysql
    mysql.column_stats                                 OK
    mysql.columns_priv                                 OK
    mysql.db                                           OK
    ..
    mysql.user                                         OK
    Phase 2/6: Fixing views
    snorby.aggregated_events                           OK
    snorby.events_with_join                            OK
    Phase 3/6: Running 'mysql_fix_privilege_tables'
    Phase 4/6: Fixing table and database names
    Phase 5/6: Checking and upgrading tables
    Processing databases

    information_schema
    paperwork
    paperwork.attachment_version                       OK
    ..
    paperwork.versions                                 OK
    performance_schema
    ptest
    snorby
    snorby.agent_asset_names                           OK
    ..
    snorby.users                                       OK
    wordpress
    wordpress.wp_commentmeta                           OK
    ..
    wordpress.wp_wpo_log                               OK
    zabbix
    zabbix.acknowledges                                OK
    ..
    zabbix.usrgrp                                      OK
    zabbix.valuemaps                                   OK
    Phase 6/6: Running 'FLUSH PRIVILEGES'
    OK

The update looked good by the above errors were still bothering me, so I ran into [this](http://dba.stackexchange.com/questions/139917/getting-innodb-internal-errors-on-every-query-run) site. It sounds like we can just export and import the **mysql** db to fix it. So I did that:

    <> mysqldump -u root -p --events --quick --single-transaction mysql > mysql-dump.sql
    Enter password:
    <> mysql -u root -p mysql < mysql-dump.sql
    Enter password:

Now let's restart:

    <> sudo service mysql-server restart
    Stopping mysql.
    Waiting for PIDS: 29452.
    Starting mysql.

And then after a restart the logs looked good:

    2017-03-18 11:42:50 3649155072 [Note] InnoDB: Shutdown completed; log sequence number 73666444387
    2017-03-18 11:42:50 3649155072 [Note] /usr/local/bin/mysqld: Shutdown complete
    170318 11:42:50 mysqld_safe mysqld from pid file /var/run/mysqld/mysqld.pid ended
    170318 11:42:50 mysqld_safe Starting mysqld daemon with databases from /var/db/mysql
    2017-03-18 11:42:50 2210488320 [Note] /usr/local/bin/mysqld (mysqld 10.1.21-MariaDB) starting as process 30390 ...
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Using mutexes to ref count buffer pool pages
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: The InnoDB memory heap is disabled
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Compressed tables use zlib 1.2.8
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Using SSE crc32 instructions
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Initializing buffer pool, size = 1.0G
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Completed initialization of buffer pool
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Highest supported file format is Barracuda.
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: 128 rollback segment(s) are active.
    2017-03-18 11:42:50 2210488320 [Note] InnoDB: Waiting for purge to start
    2017-03-18 11:42:51 2210488320 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.34-79.1 started; log sequence number 73666444387
    2017-03-18 11:42:51 3552271616 [Note] InnoDB: Dumping buffer pool(s) not yet started
    2017-03-18 11:42:51 2210488320 [Note] Plugin 'FEEDBACK' is disabled.
    2017-03-18 11:42:51 2210488320 [Note] Server socket created on IP: '0.0.0.0'.
    2017-03-18 11:42:51 2210488320 [Note] /usr/local/bin/mysqld: ready for connections.
    Version: '10.1.21-MariaDB'  socket: '/tmp/mysql.sock'  port: 3306  FreeBSD Ports

Then I started up the applications that use the DBs to make sure they can use the new version. I double checked that they are connected:

    MariaDB [(none)]> show processlist;
    +----+--------+---------------------+--------+---------+------+-------+------------------+----------+
    | Id | User   | Host                | db     | Command | Time | State | Info             | Progress |
    +----+--------+---------------------+--------+---------+------+-------+------------------+----------+
    |  2 | root   | localhost           | NULL   | Query   |    0 | init  | show processlist |    0.000 |
    |  6 | zabbix | kerch.kar.int:50895 | zabbix | Sleep   |   51 |       | NULL             |    0.000 |

### Migration to Docker
The plan will be to copy over the configs. Start a new **mariadb** **docker** container and import the new DBs. So let's get started.

#### Copy the MariaDB Configs
Since I will be user a **docker-compose** file to start the container, let's create a directory for that container:

    # mkdir maria
    # mkdir maria/{data,conf}
    
And now let's copy the configs over:

    $ rsync -avzP mariadb-confd-03-18-17.tar.bz2 core:maria/.

Now let's extract them:

    $ cd maria/
    $ tar xjf mariadb-confd-03-18-17.tar.bz2
    $ mv conf.d/* conf/*

#### Starting the MariaDB Docker Container

Next I created the following **docker-compose** config file:

    core ~ # cat maria/docker-compose.yml 
    version: '2'
    services:

        mariadb: 
           image: mariadb:latest
           container_name: mariadb
           hostname: mariadb
           restart: always
           volumes:
            - "./data:/var/lib/mysql"
            - "./conf:/etc/mysql/conf.d"
           ports:
            - "3306:3306"
           environment:
             - MYSQL_ROOT_PASSWORD=testing

and then I started up the docker container:

    core maria # docker-compose up -d
    Creating network "maria_default" with the default driver
    Pulling mariadb (mariadb:latest)...
    latest: Pulling from library/mariadb
    693502eb7dfb: Already exists
    08d0e9d74b1b: Pull complete
    e700ebfbe6bc: Pull complete
    f718f1976629: Pull complete
    b73d942a76fd: Pull complete
    6b34f02138e1: Pull complete
    b07f47800e46: Pull complete
    3a41e5a44cb3: Pull complete
    7bc4d10b3669: Pull complete
    fb4a11b7f1a0: Pull complete
    d4e3ae7d58b5: Pull complete
    64a2391497b7: Pull complete
    Digest: sha256:21afb9ab191aac8ced2e1490ad5ec6c0f1c5704810d73451dd124670bcacfb14
    Status: Downloaded newer image for mariadb:latest
    Creating mariadb

#### Migrating the User Table
Then I imported the **user** table just so I can keep the **grants** and **users** in place. So from the FreeBSD machine I ran the following:

    $ mysqldump -u root -p mysql user > user_table_dump_3-18.sql
    $ mysql -u root -h core -p mysql < user_table_dump_3-18.sql

Then I removed the **environment** variable from the **docker-compose** file (since I didn't want to reset the **root** user password) and restarted the container (to make sure everything is okay):

    core maria # docker-compose up -d

After the restart I made sure the logs look good:

    core maria # docker-compose logs
    Attaching to mariadb
    mariadb    | 2017-03-18 22:58:33 139800781416384 [Note] mysqld (mysqld 10.1.22-MariaDB-1~jessie) starting as process 1 ...
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Using mutexes to ref count buffer pool pages
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: The InnoDB memory heap is disabled
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Compressed tables use zlib 1.2.8
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Using Linux native AIO
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Using SSE crc32 instructions
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Initializing buffer pool, size = 1.0G
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Completed initialization of buffer pool
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Highest supported file format is Barracuda.
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: 128 rollback segment(s) are active.
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB: Waiting for purge to start
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] InnoDB:  Percona XtraDB (http://www.percona.com) 5.6.35-80.0 started; log sequence number 1616839
    mariadb    | 2017-03-18 22:58:34 139799277049600 [Note] InnoDB: Dumping buffer pool(s) not yet started
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] Plugin 'FEEDBACK' is disabled.
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] Server socket created on IP: '::'.
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Warning] 'proxies_priv' entry '@% root@mariadb' ignored in --skip-name-resolve mode.
    mariadb    | 2017-03-18 22:58:34 139800781416384 [Note] mysqld: ready for connections.
    mariadb    | Version: '10.1.22-MariaDB-1~jessie'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution

It looked good afrer the user table migration.

### Exporting MariaDB Databases from FreeBSD and Importing on Docker

I decided to export one database at a time and import it. This actually gave me a chance to clean up unused databases. So on the FreeBSD machine I ran the following:

    <> mysqldump --events --routines --triggers -u root -p zabbix > zabbix-03-18.sql
    Enter password: 

Then create the DB on the **docker** container:

    ┌─[elatov@moxz] - [/home/elatov] - [2017-03-18 05:02:58]
    └─[0] <> mysql -u root -p -h core
    Enter password: 
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 3
    Server version: 10.1.22-MariaDB-1~jessie mariadb.org binary distribution

    Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> create database zabbix;
    Query OK, 1 row affected (0.01 sec)

    MariaDB [(none)]> Bye

And then finally for the import:

    ┌─[elatov@moxz] - [/home/elatov] - [2017-03-18 05:04:42]
    └─[0] <> mysql -u root -h core -p zabbix < zabbix-03-18.sql 
    Enter password: 

Lastly I updated the application to use the new IP of the docker host for the **mysql** connection. I repeated that process for all of my applications and it worked out okay.

### Docker MariaDB Benchmark

I used the [same steps as before](/2016/09/migrate-mariadb-from-debian-8-to-freebsd-10/). Doing a quick benchmark, I got the following:

    <> sysbench --db-driver=mysql --test=oltp --oltp-table-size=1000000 --oltp-test-mode=complex --oltp-read-only=off --num-threads=6 --max-time=60 --max-requests=0 --mysql-db=ptest --mysql-user=root --mysql-password=become --mysql-host=core run
    sysbench 0.4.12:  multi-threaded system evaluation benchmark

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
            read:                            367626
            write:                           131295
            other:                           52518
            total:                           551439
        transactions:                        26259  (437.58 per sec.)
        deadlocks:                           0      (0.00 per sec.)
        read/write requests:                 498921 (8314.06 per sec.)
        other operations:                    52518  (875.16 per sec.)

    Test execution summary:
        total time:                          60.0093s
        total number of events:              26259
        total time taken by event execution: 359.9572
        per-request statistics:
             min:                                  7.36ms
             avg:                                 13.71ms
             max:                                141.39ms
             approx.  95 percentile:              19.92ms

    Threads fairness:
        events (avg/stddev):           4376.5000/40.67
        execution time (avg/stddev):   59.9929/0.00


This is using the default **bridge** network that **docker-compose** creates for the conatiner:

    elatov@core ~ $ docker network ls | grep mar
    6df70ed8f399        maria_default        bridge              local  

More information on docker networking is at [Docker container networking](https://docs.docker.com/engine/userguide/networking/). [Some folks](http://blog.balazspocze.me/2016/02/15/mysqldocker-performance-report-update/) had better luck using the docker **host** network type. But I was okay with the results, since they match my old local ones.
