---
published: true
layout: post
title: "Upgrade Zabbix 2.4 to 3.0"
author: Karim Elatov
categories: [security,os]
tags: [zabbix,pogoplug,monitoring,linux]
---
### Upgrade Zabbix Server to 3.0 on Debian 8

The instructions are laid out in [Upgrade procedure](https://www.zabbix.com/documentation/3.0/manual/installation/upgrade). Also version specific notes are at [Upgrade notes for 2.4.7](https://www.zabbix.com/documentation/2.4/manual/installation/upgrade_notes_247), nothing note-worthy so I decided to go ahead with it. First let's stop the Zabbix services on the server:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 05:56:28]
	└─[1] <> sudo systemctl stop zabbix-server.service
	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 05:57:28]
	└─[0] <> sudo systemctl stop zabbix-agent.service

For safety, dump the zabbix db:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 05:56:41]
	└─[0] <> mysqldump --databases -u root -p zabbix > zabbix-03-26-16.mysql

Compress it to save space:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 05:58:38]
	└─[0] <> tar cpvfj zabbix-03-26-16_sql.tar.bz2 zabbix-03-26-16.mysql
	zabbix-03-26-16.mysql

Lastly let's send it over to another server for backups:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:04:15]
	└─[0] <> rsync -avzP zabbix-03-26-16_sql.tar.bz2 IP:/backups/db/.

Next we can follow instructions laid out in [Installation from packages](https://www.zabbix.com/documentation/3.0/manual/installation/install_from_packages#debianubuntu) to setup the **apt** repo. First let's get the package to update the repo:


	wget http://repo.zabbix.com/zabbix/3.0/debian/pool/main/z/zabbix-release/zabbix-release_3.0-1+jessie_all.deb

Next let's install it and overwrite the **sources.list** file from the older version:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:04:47]
	└─[0] <> sudo dpkg -i zabbix-release_3.0-1+jessie_all.deb
	(Reading database ... 101895 files and directories currently installed.)
	Preparing to unpack zabbix-release_3.0-1+jessie_all.deb ...
	Unpacking zabbix-release (3.0-1+jessie) over (2.4-1+jessie) ...
	Setting up zabbix-release (3.0-1+jessie) ...
	
	Configuration file '/etc/apt/sources.list.d/zabbix.list'
	 ==> Modified (by you or by a script) since installation.
	 ==> Package distributor has shipped an updated version.
	   What would you like to do about it ?  Your options are:
	    Y or I  : install the package maintainer's version
	    N or O  : keep your currently-installed version
	      D     : show the differences between the versions
	      Z     : start a shell to examine the situation
	 The default action is to keep your current version.
	*** zabbix.list (Y/I/N/O/D/Z) [default=N] ? Y
	Installing new version of config file /etc/apt/sources.list.d/zabbix.list ...

Next let's update the **apt** cache:

	apt-get update

And finally do the upgrade:

	apt-get upgrade zabbix-server-mysql zabbix-frontend-php

I then checked out the **/etc/zabbix/apache.conf** file and it looks like the
**api** directory is no longer shared and neither is the **class** one. So I commented out the old directories and added new ones:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:16:51]
	└─[1] <> cat /etc/zabbix/apache.conf
	# Define /zabbix alias, this is the default
	<IfModule mod_alias.c>
	    Alias /zab /usr/share/zabbix
	</IfModule>
	
	<Directory "/usr/share/zabbix">
	    Options FollowSymLinks
	    AllowOverride None
	    Order allow,deny
	    Allow from all
	   <IfModule mod_php5.c>
	     php_value max_execution_time 300
	     php_value always_populate_raw_post_data  -1
	     php_value memory_limit 128M
	     php_value post_max_size 16M
	     php_value upload_max_filesize 2M
	     php_value max_input_time 300
	     # php_value date.timezone Europe/Riga
	     php_value date.timezone America/Denver
	  </IfModule>
	</Directory>
	
	<Directory "/usr/share/zabbix/conf">
	    Order deny,allow
	    Deny from all
	    <files *.php>
	        Order deny,allow
	        Deny from all
	    </files>
	</Directory>
	
	#<Directory "/usr/share/zabbix/api">
	#    Order deny,allow
	#    Deny from all
	#    <files *.php>
	#        Order deny,allow
	#        Deny from all
	#    </files>
	#</Directory>
	
	<Directory "/usr/share/zabbix/app">
	    Order deny,allow
	    Deny from all
	    <files *.php>
	        Order deny,allow
	        Deny from all
	    </files>
	</Directory>
	
	<Directory "/usr/share/zabbix/include">
	    Order deny,allow
	    Deny from all
	    <files *.php>
	        Order deny,allow
	        Deny from all
	    </files>
	</Directory>
	
	#<Directory "/usr/share/zabbix/include/classes">
	#    Order deny,allow
	#    Deny from all
	#    <files *.php>
	#        Order deny,allow
	#        Deny from all
	#    </files>
	#</Directory>
	
	<Directory "/usr/share/zabbix/local">
	    Order deny,allow
	    Deny from all
	    <files *.php>
	        Order deny,allow
	        Deny from all
	    </files>
	</Directory>

I then checked out the **/etc/zabbix/zabbix_server.conf** and I didn't have much
to change. The settings that I used were still there and a bunch of new TLS
options got added that I wasn't really using those so I just kept both files without changing them:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:18:08]
	└─[0] <> ls -l /etc/zabbix/zabbix_server.conf*
	-rw-r----- 1 zabbix root 13984 Nov 29 10:36 /etc/zabbix/zabbix_server.conf
	-rw-r----- 1 zabbix root 14890 Feb 28 01:03 /etc/zabbix/zabbix_server.conf.dpkg-dist

Same thing for the agent config:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:21:56]
	└─[0] <> ls -l /etc/zabbix/zabbix_agentd.conf*
	-rw-r--r-- 1 root root  7935 Nov  1  2014 /etc/zabbix/zabbix_agentd.conf
	-rw-r--r-- 1 root root 10341 Feb 28 01:03 /etc/zabbix/zabbix_agentd.conf.dpkg-dist

Then I started the zabbix server service:

	sudo systemctl start zabbix-server

And checking out the logs I saw the following:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:21:56]
	└─[0] <> tail -f /var/log/zabbix/zabbix-server.log
	1281:20160326:175641.237 Zabbix Server stopped. Zabbix 2.4.7 (revision 56694).
	879:20160326:182255.648 Starting Zabbix Server. Zabbix 3.0.1 (revision 58734).
	879:20160326:182255.648 ****** Enabled features ******
	879:20160326:182255.648 SNMP monitoring:           YES
	879:20160326:182255.648 IPMI monitoring:           YES
	879:20160326:182255.648 Web monitoring:            YES
	879:20160326:182255.648 VMware monitoring:         YES
	879:20160326:182255.648 SMTP authentication:       YES
	879:20160326:182255.648 Jabber notifications:      YES
	879:20160326:182255.648 Ez Texting notifications:  YES
	879:20160326:182255.648 ODBC:                      YES
	879:20160326:182255.648 SSH2 support:              YES
	879:20160326:182255.648 IPv6 support:              YES
	879:20160326:182255.648 TLS support:               YES
	879:20160326:182255.648 ******************************
	879:20160326:182255.648 using configuration file: /etc/zabbix/zabbix_server.conf
	879:20160326:182255.655 current database version (mandatory/optional): 02040000/02040000
	879:20160326:182255.655 required mandatory version: 03000000
	879:20160326:182255.655 starting automatic database upgrade
	879:20160326:182255.689 completed 0% of database upgrade
	879:20160326:182255.694 completed 1% of database upgrade
	879:20160326:182255.705 completed 2% of database upgrade
	...
	...
	879:20160326:182256.346 completed 100% of database upgrade
	879:20160326:182256.346 database upgrade fully completed
	879:20160326:182256.368 server #0 started [main process]
	889:20160326:182256.369 server #2 started [db watchdog #1]
	888:20160326:182256.373 server #1 started [configuration syncer #1]
	894:20160326:182256.374 server #7 started [poller #5]
	893:20160326:182256.374 server #6 started [poller #4]

And after that I started the agent:

	┌─[elatov@kerch] - [/home/elatov] - [2016-03-26 06:24:47]
	└─[130] <> sudo systemctl start zabbix-agent.service

Here is what I saw the logs (**/var/log/zabbix/zabbix_agentd.log**):

	31813:20160326:181950.899 Zabbix Agent stopped. Zabbix 3.0.1 (revision 58734).
	1040:20160326:182453.326 Starting Zabbix Agent [kerch.dnsd.me]. Zabbix 3.0.1 (revision 58734).
	1040:20160326:182453.326 **** Enabled features ****
	1040:20160326:182453.326 IPv6 support:          YES
	1040:20160326:182453.326 TLS support:           YES
	1040:20160326:182453.326 **************************
	1040:20160326:182453.326 using configuration file: /etc/zabbix/zabbix_agentd.conf
	1040:20160326:182453.326 agent #0 started [main process]
	1043:20160326:182453.327 agent #2 started [listener #1]
	1042:20160326:182453.329 agent #1 started [collector]
	
I also logged in and checked out the new UI:

![zab-new-ui](https://dl.dropboxusercontent.com/u/24136116/blog_pics/upgrade-zabbix-3/zab-new-ui.png)

### Update Zabbix Agent to 3.0 on FreeBSD
For my FreeBSD servers, I saw the new package available for 3.0 agent, so I
installed it. First let's stop the old/running one:

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:43:00]
	└─[1] <> sudo service zabbix_agentd stop
	Stopping zabbix_agentd.
	Waiting for PIDS: 542 544 545.

Then I removed the old agent:

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:44:34]
	└─[0] <> sudo pkg remove zabbix24-agent-2.4.7

Then I installed the 3.0 version:

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:44:42]
	└─[0] <> sudo pkg install zabbix3-agent-3.0.1

Then I copied the old config over since the options are so close (if you had any include statements pointing to the old directory don't forget to update those):

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:45:09]
	└─[0] <> sudo cp /usr/local/etc/zabbix24/zabbix_agentd.conf /usr/local/etc/zabbix3/.

Then I started the new service:

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:45:28]
	└─[0] <> sudo service zabbix_agentd start

And in the logs I saw the following:

	┌─[elatov@moxz] - [/home/elatov] - [2016-03-26 06:45:42]
	└─[0] <> tail -f /var/log/zabbix/zabbix_agentd.log
	542:20160326:184309.565 Zabbix Agent stopped. Zabbix 2.4.7 (revision 56694).
	36950:20160326:184535.162 Starting Zabbix Agent [moxz.dnsd.me]. Zabbix 3.0.1 (revision 58734).
	36950:20160326:184535.162 **** Enabled features ****
	36950:20160326:184535.162 IPv6 support:          YES
	36950:20160326:184535.162 TLS support:            NO
	36950:20160326:184535.162 **************************
	36950:20160326:184535.162 using configuration file: /usr/local/etc/zabbix3/zabbix_agentd.conf
	36950:20160326:184535.163 agent #0 started [main process]
	36951:20160326:184535.163 agent #1 started [collector]
	36952:20160326:184535.163 agent #2 started [listener #1]

### Update Zabbix Agent to 3.0 on OnmiOS

First let's download the new precompiled version:

	wget http://www.zabbix.com/downloads/3.0.0/zabbix_agents_3.0.0.solaris10.amd64.tar.gz

Then let's stop the running service:

	┌─[root@zfs] - [/root] - [2016-03-26 06:58:55]
	└─[0] <> svcadm disable zabbix-agent

Then let's move the original install out of the way:

	┌─[root@zfs] - [/root] - [2016-03-26 06:59:15]
	└─[0] <> mv /usr/local/zabbix /usr/local/zabbix24

And let's create a directory for the new version:

	┌─[root@zfs] - [/root] - [2016-03-26 06:59:32]
	└─[0] <> mkdir /usr/local/zabbix

Now let's extract the compiled version in that directory:

	┌─[root@zfs] - [/root] - [2016-03-26 06:59:44]
	└─[0] <> tar xvzf zabbix_agents_3.0.0.solaris10.amd64.tar.gz -C /usr/local/zabbix/

Let's move the default config out of the way:

	┌─[root@zfs] - [/root] - [2016-03-26 07:00:10]
	└─[0] <> mv /usr/local/zabbix/conf/zabbix_agentd.conf /usr/local/zabbix/conf/zabbix_agentd.conf.orig

And let's copy the original config:

	┌─[root@zfs] - [/root] - [2016-03-26 07:00:25]
	└─[0] <> cp /usr/local/zabbix24/conf/zabbix_agent.conf /usr/local/zabbix/conf/.

Then start the new version:

	┌─[root@zfs] - [/root] - [2016-03-26 07:01:23]
	└─[0] <> svcadm enable zabbix-agent

And in the logs I saw the following:

	┌─[root@zfs] - [/root] - [2016-03-26 07:01:31]
	└─[0] <> tail -f /var/adm/zabbix/zabbix_agentd.log
	455:20160326:185907.651 Zabbix Agent stopped. Zabbix 2.4.1 (revision 49643).
	21112:20160326:190131.030 Starting Zabbix Agent [zfs.dnsd.me]. Zabbix 3.0.0 (revision 58460).
	21112:20160326:190131.030 **** Enabled features ****
	21112:20160326:190131.030 IPv6 support:           NO
	21112:20160326:190131.030 TLS support:            NO
	21112:20160326:190131.030 **************************
	21112:20160326:190131.030 using configuration file: /etc/zabbix/zabbix_agentd.conf
	21112:20160326:190131.030 agent #0 started [main process]
	21113:20160326:190131.031 agent #1 started [collector]
	21114:20160326:190131.031 agent #2 started [listener #1]

### Upgrade Zabbix Agent to 3.0 On Pogoplug

The original setup for that is covered in my [old post](/2013/10/monitor-smart-attributes-zabbix/). First let's stop the current agent:

	pogo:~# /opt/etc/init.d/zabbix-agentd stop

Now let's get the source 

	pogo:~# wget https://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/3.0.1/zabbix-3.0.1.tar.gz

Now let's extract it:

	pogo:~# mv zabbix-3.0.1.tar.gz /opt/tmp/.
	pogo:~# cd /opt/tmp
	pogo:/opt/tmp# tar xzf zabbix-3.0.1.tar.gz ; cd zabbix-3.0.1
	pogo:/opt/tmp/zabbix-3.0.1# ./configure --enable-agent --prefix=/opt/zabbix

Initially during the **make** phase I ran into this error:

	./../src/libs/zbxmodules/libzbxmodules.a(modules.o): In function `unload_modules':
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:249: undefined reference to `dlclose'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:237: undefined reference to `dlsym'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:240: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:242: undefined reference to `dlclose'
	../../src/libs/zbxmodules/libzbxmodules.a(modules.o): In function `load_modules':
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:117: undefined reference to `dlopen'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:123: undefined reference to `dlsym'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:139: undefined reference to `dlsym'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:156: undefined reference to `dlsym'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:165: undefined reference to `dlsym'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:168: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:170: undefined reference to `dlclose'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:159: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:119: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:135: undefined reference to `dlclose'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:126: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:128: undefined reference to `dlclose'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:151: undefined reference to `dlclose'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:142: undefined reference to `dlerror'
	/opt/tmp/zabbix-3.0.1/src/libs/zbxmodules/modules.c:144: undefined reference to `dlclose'
	collect2: ld returned 1 exit status

I have run into that issue in the past and that's when there are 2 versions of the **libdl.so** file, here are the two files:

	pogo~# find / -name 'libdl.so*'
	/lib/libdl.so.2
	/tmp/.cemnt/mnt_sda1/opt/arm-none-linux-gnueabi/lib/libdl.so
	/tmp/.cemnt/mnt_sda1/opt/arm-none-linux-gnueabi/lib/libdl.so.2

The easiest thing to do is to temporarily move the other one out of the way:

	pogo~# mv /opt/arm-none-linux-gnueabi/lib/libdl.so /opt/arm-none-linux-gnueabi/lib/libdl.so.orig

And also link the one under **/lib**:

	pogo~# ln -s /lib/libdl.so.2 /lib/libdl.so

Then rebuilding worked:

	pogo:/opt/tmp/zabbix-3.0.1# make clean
	pogo:/opt/tmp/zabbix-3.0.1# ./configure --enable-agent --prefix=/opt/zabbix
	pogo:/opt/tmp/zabbix-3.0.1# make
	pogo:/opt/tmp/zabbix-3.0.1# unlink /opt/zabbix
	pogo:/opt/tmp/zabbix-3.0.1# ln -s /opt/zabbix_3_0_1 /opt/zabbix
	pogo:/opt/tmp/zabbix-3.0.1# make install

Then make a backup of the default config:

	pogo~# cp /opt/zabbix/etc/zabbix_agentd.conf /opt/zabbix/etc/zabbix_agentd.conf.orig

And let's copy the old one into place

	pogo~# cp /opt/zabbix_2_2_3/etc/zabbix_agentd.conf /opt/zabbix/etc/zabbix_agentd.conf

Then starting the service worked out:

	pogo:~# /opt/etc/init.d/zabbix-agentd start
	Starting zabbix agent:           Success
	pogo:~# ps -w | grep zab
	 2622 root      3020 S    /opt/zabbix/sbin/zabbix_agentd -c /opt/zabbix/etc/zabbix_agentd.conf
	 2623 root      3020 S    /opt/zabbix/sbin/zabbix_agentd: collector [idle 1 sec]
	 2624 root      3020 S    /opt/zabbix/sbin/zabbix_agentd: listener #1 [waiting for connection]
	pogo:~# tail -f /opt/var/log/zabbix/zabbix_agentd.log
	   726:20160327:030805.099 Zabbix Agent stopped. Zabbix 2.2.3 (revision 44105).
	  2622:20160327:034031.434 Starting Zabbix Agent [pogo.dnsd.me]. Zabbix 3.0.1 (revision 58734).
	  2622:20160327:034031.435 **** Enabled features ****
	  2622:20160327:034031.435 IPv6 support:           NO
	  2622:20160327:034031.435 TLS support:            NO
	  2622:20160327:034031.435 **************************
	  2622:20160327:034031.435 using configuration file: /opt/zabbix/etc/zabbix_agentd.conf
	  2622:20160327:034031.436 agent #0 started [main process]
	  2623:20160327:034031.438 agent #1 started [collector]
	  2624:20160327:034031.442 agent #2 started [listener #1]
