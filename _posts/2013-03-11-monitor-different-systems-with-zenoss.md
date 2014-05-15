---
title: Monitor Different Systems with Zenoss
author: Karim Elatov
layout: post
permalink: /2013/03/monitor-different-systems-with-zenoss/
dsq_thread_id:
  - 1404672919
categories:
  - Home Lab
  - Networking
tags:
  - Monitoring
  - Zenoss
---
<p>This is the third part and continuation of the 'Network Monitoring Software Comparison' series. Here is the link to the <a href="http://virtuallyhyper.com/2013/02/monitor-different-systems-with-collectd" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/monitor-different-systems-with-collectd']);">first</a> part and here is the <a href="http://virtuallyhyper.com/2013/03/monitor-different-systems-with-munin" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/monitor-different-systems-with-munin']);">second</a> one. Let's check out what <strong>Zenoss</strong> is about. From their <a href="http://wiki.zenoss.org/Main_Page" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.zenoss.org/Main_Page']);">wiki</a> page, we see the following:</p>
<blockquote>
<p>What is Zenoss?</p>
<p>Zenoss Core is award-winning Open Source IT monitoring software that offers visibility over the entire IT stack, from network devices to applications. Features include automatic discovery, inventory via CMDB, availability monitoring, easy-to-read performance graphs, sophisticated alerting, an easy-to-use web portal, and much, much more. It is Free Software, released under the GNU General Public License version 2. Zenoss has a very active community.</p>
</blockquote>
<p>Now to start the install. Reading over the <a href="http://community.zenoss.org/community/documentation/official_documentation/installation-guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/community/documentation/official_documentation/installation-guide']);">Installation Guide</a>, I saw that there is section on how to compile the software from source. This sparked an interest to install the software on my FreeBSD system.</p>
<h3>1. Setup a MySQL Database for the Zenoss Install</h3>
<p>I decided to setup Zenoss on my FreeBSD machine, since my Ubuntu box was already running the other monitoring applications and I knew that the source for Zenoss was available. Zenoss uses MySQL for it's database, I actually had a MySQL instance running on the Ubuntu machine, hence I decided to allow remote access for root to MySQL. I would rarely do this, but since this was a test setup, I decided to just go all out <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Monitor Different Systems with Zenoss" class="wp-smiley" title="Monitor Different Systems with Zenoss" /> </p>
<p>Before any changes, I was able to login as <strong>root</strong> locally:</p>
	kerch:~&gt;mysql -u root -p
	Enter password: 
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 115
	Server version: 5.5.29-0ubuntu0.12.10.1 (Ubuntu)
	Copyright (c) 2000, 2012, Oracle and/or its affiliates. All rights reserved.
	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	mysql&gt;
	
<p>But trying to connect to the IP would fail like so:</p>
	kerch:~$ mysql -h 192.168.1.100 -u root -p 
	Enter password:
	ERROR 2003 (HY000): Can't connect to MySQL server on '192.168.1.100' (111)
	
<p>So let's login to the MySQL server and check out the current settings:</p>
	mysql&gt; use mysql;
	Reading table information for completion of table and column names
	You can turn off this feature to get a quicker startup with -A
	Database changed
	mysql&gt; select host,user from user;
	+-----------+------------------+
	| host      | user             |
	+-----------+------------------+
	| 127.0.0.1 | root             |
	| ::1       | root             |
	| localhost | debian-sys-maint |
	| localhost | root             |
	| localhost | wordpress        |
	+-----------+------------------+
	5 rows in set (0.02 sec)
	
<p>I don't use IPv6, so let's replace that entry with "%" (allowing any host to connect):</p>
	mysql&gt; update user set host='%' where user='root' and host='::1'; 
	Query OK, 1 row affected (0.05 sec)
	Rows matched: 1 Changed: 1 Warnings: 0
	
<p>Flush the privileges to apply the settings:</p>
	mysql&gt; flush privileges;
	Query OK, 0 rows affected (0.04 sec)
	
<p>By default the MySQL install binds the server to the <strong>localhost</strong> interface for security reasons. To allow remote connections we need to bind the instance to a non-local IP. This is done by editing the <strong>/etc/mysql/my.cnf</strong> file and changing this line:</p>
	bind-address = 127.0.0.1
	
<p>to this:</p>
	bind-address = 192.168.1.100
	
<p>To apply the above changes, restart the <strong>mysql</strong> service:</p>
	kerch:~&gt;sudo service mysql restart 
	mysql stop/waiting
	mysql start/running, process 371
	
<p>Then I was able to login to the MySQL server by connecting to the IP:</p>
	kerch:~&gt;mysql -h 192.168.1.100 -u root -p
	Enter password: 
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 116
	Server version: 5.5.29-0ubuntu0.12.10.1 (Ubuntu)
	Copyright (c) 2000, 2012, Oracle and/or its affiliates. All rights reserved.
	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	mysql&gt; 
	
<p>Lastly I had to open up port <strong>3306</strong> on the firewall as well. This is done by editing <strong>/etc/iptables/rule.v4</strong> and adding the following line:</p>
	-A INPUT -s 192.168.1.0/24 -p tcp -m state --state NEW -m tcp --dport 3306 --tcp-flags FIN,SYN,RST,ACK SYN -j ACCEPT
	
<p>To apply the changes to the filewall, just restart the <strong>iptables</strong> service:</p>
	kerch:~&gt;sudo service iptables-persistent restart 
	* Loading iptables rules... 
	* IPv4...
	* IPv6... [ OK ]
	
<p>I was even able to connect from another machine:</p>
	moxz:~&gt;mysql -h 192.168.1.100 -u root -p
	Enter password: 
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 117
	Server version: 5.5.29-0ubuntu0.12.10.1 (Ubuntu)
	Copyright (c) 2000, 2012, Oracle and/or its affiliates. All rights reserved.
	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	mysql&gt; 
	
<p>There are better ways to go about this. Like to create a dedicated user for the Zenoss setup. But since this was a test setup, this was okay for me. Now on the FreeBSD machine, let’s install Zenoss.</p>
<h3>2. Install Zenoss on FreeBSD</h3>
	freebsd:~&gt;cd /usr/ports/net-mgmt/zenoss
	freebsd:/usr/ports/net-mgmt/zenoss&gt;sudo make install clean
	
<p>After the install is done, let’s enable the service by editing the <strong>/etc/rc.conf</strong> file and adding the following:</p>
	zenoss_enable="YES"
	
<p>Now let’s initialize the Zenoss service:</p>
	freebsd:~&gt;sudo service zenoss init 
	MySQL server hostname [localhost]: 192.168.1.100 
	MySQL server root username [root]: 
	MySQL server root password []: 
	MySQL event database name [events]: 
	MySQL username for Zenoss events database [zenoss]: 
	MySQL password for zenoss [zenoss]: 
	MySQL server port [3306]: 
	+-------------------------+
	| VERSION()               |
	+-------------------------+
	| 5.5.29-0ubuntu0.12.10.1 |
	+-------------------------+
	Wrote file /usr/local/zenoss/etc/zeo.conf 
	Wrote file /usr/local/zenoss/bin/zeoctl 
	Changed mode for /usr/local/zenoss/bin/zeoctl to 755 
	Wrote file /usr/local/zenoss/bin/runzeo 
	Changed mode for /usr/local/zenoss/bin/runzeo to 755 
	Starting Zope Object Database . 
	daemon process started, pid=24007 
	Loading initial Zenoss objects into the Zeo database (this can take a few minutes) 
	ZentinelPortal loaded at zport 
	Starting Zope Server .
	daemon process started, pid=24771
	
	=========================================================
	zensocket must be setuid. As root, execute the following:
	chown root:zenoss /usr/local/zenoss/bin/zensocket
	chmod 04750 /usr/local/zenoss/bin/zensocket
	=========================================================
	Successfully installed Zenoss
	
<p>Then following the instructions and setting the <strong>suid</strong> bit properly:</p>
	freebsd:~&gt;sudo chown root:zenoss /usr/local/zenoss/bin/zensocket
	freebsd:~&gt;sudo chmod 04750 /usr/local/zenoss/bin/zensocket
	
<p>Lastly, let’s start all the necessary services:</p>
	freebsd:~&gt;sudo service zenoss start
	Daemon: zeoctl daemon process already running; pid=24007
	Daemon: zopectl daemon process already running; pid=24771
	Daemon: zenhub starting...
	Daemon: zenjobs starting...
	Daemon: zenping starting...
	Daemon: zensyslog starting...
	Daemon: zenstatus starting...
	Daemon: zenactions starting...
	Daemon: zentrap starting...
	Daemon: zenmodeler starting...
	Daemon: zenperfsnmp starting...
	Daemon: zencommand starting...
	Daemon: zenprocess starting...
	Daemon: zenwin starting...
	Daemon: zeneventlog starting...
	
<p>Then confirming they are all running:</p>
	freebsd:~&gt;sudo service zenoss status
	Daemon: zeoctl program running; pid=24007
	Daemon: zopectl program running; pid=24771
	Daemon: zenhub program running; pid=25147
	Daemon: zenjobs program running; pid=25172
	Daemon: zenping program running; pid=25245
	Daemon: zensyslog not running
	Daemon: zenstatus program running; pid=25302
	Daemon: zenactions program running; pid=25397
	Daemon: zentrap program running; pid=25513
	Daemon: zenmodeler program running; pid=25489
	Daemon: zenperfsnmp program running; pid=25525
	Daemon: zencommand program running; pid=25549
	Daemon: zenprocess program running; pid=25573
	Daemon: zenwin program running; pid=25604
	Daemon: zeneventlog program running; pid=25633
	
<p>One service (<strong>zensyslog</strong>) didn’t start, but that is okay. Checking out the active connections for Zenoss, there were a lot:</p>
	freebsd:~&gt;sudo sockstat -4 | grep zenoss
	zenoss   python2.6  25633 6  tcp4   127.0.0.1:18493       127.0.0.1:8789
	zenoss   python2.6  25604 6  tcp4   127.0.0.1:32636       127.0.0.1:8789
	zenoss   python2.6  25573 4  tcp4   127.0.0.1:47321       127.0.0.1:8789
	zenoss   python2.6  25549 6  tcp4   127.0.0.1:17865       127.0.0.1:8789
	zenoss   python2.6  25525 6  tcp4   127.0.0.1:37259       127.0.0.1:8789
	zenoss   python2.6  25513 4  udp4   *:162                 *:*
	zenoss   python2.6  25513 6  udp4   *:162                 *:*
	zenoss   python2.6  25513 9  tcp4   127.0.0.1:29149       127.0.0.1:8789
	zenoss   python2.6  25489 6  tcp4   127.0.0.1:25461       127.0.0.1:8789
	zenoss   python2.6  25397 8  tcp4   127.0.0.1:41130       127.0.0.1:8100
	zenoss   python2.6  25397 18 tcp4   192.168.1.101:35744   192.168.1.100:3306
	zenoss   python2.6  25302 6  tcp4   127.0.0.1:48225       127.0.0.1:8789
	zenoss   python2.6  25245 8  tcp4   127.0.0.1:40793       127.0.0.1:8789
	zenoss   python2.6  25172 8  tcp4   127.0.0.1:37563       127.0.0.1:8100
	zenoss   python2.6  25172 18 tcp4   192.168.1.101:32699   192.168.1.100:3306
	zenoss   python2.6  25147 6  tcp4   127.0.0.1:56578       127.0.0.1:8100
	zenoss   python2.6  25147 15 tcp4   *:8789                *:*
	zenoss   python2.6  25147 19 tcp4   *:8081                *:*
	zenoss   python2.6  25147 20 tcp4   192.168.1.101:52771   192.168.1.100:3306
	zenoss   python2.6  25147 21 tcp4   127.0.0.1:8789        127.0.0.1:40793
	zenoss   python2.6  25147 22 tcp4   127.0.0.1:8789        127.0.0.1:48225
	zenoss   python2.6  25147 23 tcp4   127.0.0.1:8789        127.0.0.1:25461
	zenoss   python2.6  25147 24 tcp4   127.0.0.1:8789        127.0.0.1:29149
	zenoss   python2.6  25147 25 tcp4   127.0.0.1:8789        127.0.0.1:37259
	zenoss   python2.6  25147 26 tcp4   127.0.0.1:8789        127.0.0.1:17865
	zenoss   python2.6  25147 27 tcp4   127.0.0.1:8789        127.0.0.1:47321
	zenoss   python2.6  25147 28 tcp4   127.0.0.1:8789        127.0.0.1:32636
	zenoss   python2.6  25147 29 tcp4   127.0.0.1:8789        127.0.0.1:18493
	zenoss   python2.6  24771 3  tcp4   *:8080                *:*
	zenoss   python2.6  24771 12 tcp4   127.0.0.1:35025       127.0.0.1:8100
	zenoss   python2.6  24007 7  tcp4   127.0.0.1:8100        *:*
	zenoss   python2.6  24007 8  tcp4   127.0.0.1:8100        127.0.0.1:35025
	zenoss   python2.6  24007 9  tcp4   127.0.0.1:8100        127.0.0.1:56578
	zenoss   python2.6  24007 16 tcp4   127.0.0.1:8100        127.0.0.1:37563
	zenoss   python2.6  24007 17 tcp4   127.0.0.1:8100        127.0.0.1:41130
	
<p>Most are for local communication. Visiting <strong>127.0.0.1:8080</strong> showed the following page:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_page_zenoss.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_page_zenoss.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_page_zenoss.png" alt="setup page zenoss Monitor Different Systems with Zenoss" width="1296" height="455" class="alignnone size-full wp-image-6579" title="Monitor Different Systems with Zenoss" /></a></p>
<p>I then setup the users and passwords:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_user_zenoss.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_user_zenoss.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/setup_user_zenoss.png" alt="setup user zenoss Monitor Different Systems with Zenoss" width="869" height="317" class="alignnone size-full wp-image-6580" title="Monitor Different Systems with Zenoss" /></a></p>
<p>And then I skipped adding devices and went to the dashboard:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_dashboard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_dashboard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_dashboard.png" alt="zenoss dashboard Monitor Different Systems with Zenoss" width="1306" height="661" class="alignnone size-full wp-image-6581" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Looking over the <a href="http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide']);">Administration Guide</a>, I saw this:</p>
<blockquote>
<p>Servers are organized by operating system. If the system discovers Windows devices, for example, you might choose to relocate them to /Server/Windows. Similarly, you might choose to classify discovered Linux devices in / Server/Linux (if you want to monitor and model using SNMP), or /Server/SSH/Linux (if you want to monitor and model using SSH)</p>
</blockquote>
<p>So you can monitor your machine with SNMP or SSH. There are actually other ways, like APIs. From the <a href="http://wiki.zenoss.org/Prepare_Remote_Device" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.zenoss.org/Prepare_Remote_Device']);">wiki</a>:</p>
<blockquote>
<p>Before we can monitor a device in Zenoss, we need to ensure that is is properly set up to be monitored. Zenoss does not use agents, but it needs to query the device using some protocol. The "classical" way to monitor devices with Zenoss is to use the Simple Network Management Protocol, also known as SNMP. SSH is also supported for Linux systems, and WMI is supported for Microsoft Windows-based systems.</p>
<p>We also support various APIs, such as the Amazon EC2 and CloudStack API, for monitoring cloud services.</p>
</blockquote>
<p>I decided to use SNMP for the FreeBSD and Fedora Machines, and SSH for the Ubuntu machine.</p>
<p>Now let’s start monitoring our nodes.</p>
<h3>3. Monitor our Ubuntu Machine with Zenoss via SSH</h3>
<p>To get any useful information from SSH it’s recommended to install the <em>LinuxMonitor ZenPack</em>, more information is seen in <a href="http://community.zenoss.org/docs/DOC-3435" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-3435']);">this</a> community page. Instructions on how to install <em>ZenPacks</em> are found in <a href="http://community.zenoss.org/docs/DOC-2935" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-2935']);">this</a> community page. Similar instructions are found in the <a href="http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide']);">Admin Guide</a>. Here is a description of ZenPacks from that guide:</p>
<blockquote>
<p><strong>13.1. About ZenPacks</strong><br />
  ZenPacks extend and modify the system to add new functionality. This can be as simple as adding new device classes or monitoring templates, or as complex as extending the data model and providing new collection daemons.</p>
<p>You can use ZenPacks to add:</p>
<ul>
<li>Monitoring templates </li>
<li>Data sources</li>
<li>Graphs</li>
<li>Event classes</li>
<li>Event and user commands</li>
<li>Reports</li>
<li>Model extensions</li>
<li>Product definitions</li>
</ul>
</blockquote>
<p>I uploaded the ZenPack file to the <strong>Products</strong> directory of the Zenoss install:</p>
	freebsd:~&gt;sudo cp ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg.zip ~zenoss/Products/.
	freebsd:~&gt;sudo chown zenoss:zenoss ~zenoss/Products/ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg 
	
<p>and then I switched to the <strong>zenoss</strong> user and installed the ZenPack:</p>
	freebsd:~&gt;sudo su - zenoss
	$ zenpack --install Products/ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg
	2013-02-22 21:19:33,994 INFO zen.ZPLoader: Loading /usr/local/zenoss/ZenPacks/ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg/ZenPacks/zenoss/LinuxMonitor/objects/objects.xml
	2013-02-22 21:19:37,280 INFO zen.AddToPack: End loading objects
	2013-02-22 21:19:37,280 INFO zen.AddToPack: Processing links
	2013-02-22 21:19:38,630 INFO zen.AddToPack: Loaded 65 objects into the ZODB database
	2013-02-22 21:19:38,636 INFO zen.HookReportLoader: loading reports from:/usr/local/zenoss/ZenPacks/ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg/ZenPacks/zenoss/LinuxMonitor/reports
	
<p>You could do the same thing from the web page. Basically from the Dashboard go to “Advanced” -> "ZenPacks" -> “Gear” -> “Install ZenPack”, here is how it looks like:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_install_zenpack.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_install_zenpack.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_install_zenpack.png" alt="zenoss install zenpack Monitor Different Systems with Zenoss" width="723" height="308" class="alignnone size-full wp-image-6590" title="Monitor Different Systems with Zenoss" /></a></p>
<p>After the ZenPack is installed, we need to restart <strong>zenoss</strong>. Here is how that looks:</p>
	freebsd:~&gt;sudo service zenoss restart
	Password:
	Daemon: zeneventlog stopping...
	Daemon: zenwin stopping...
	Daemon: zenprocess stopping...
	Daemon: zencommand stopping...
	Daemon: zenperfsnmp stopping...
	Daemon: zenmodeler stopping...
	Daemon: zentrap stopping...
	Daemon: zenactions stopping...
	Daemon: zenstatus stopping...
	Daemon: zensyslog stopping...
	already stopped
	Daemon: zenping stopping...
	Daemon: zenjobs stopping...
	Daemon: zenhub stopping...
	Daemon: zopectl . . . . . . . . . . . 
	daemon process stopped
	Daemon: zeoctl . 
	daemon process stopped
	Daemon: zeoctl . 
	daemon process started, pid=30272
	Daemon: zopectl . 
	daemon process started, pid=30276
	Daemon: zenhub starting...
	Daemon: zenjobs is already running
	Daemon: zenping starting...
	Daemon: zensyslog starting...
	Daemon: zenstatus starting...
	Daemon: zenactions is already running
	Daemon: zentrap starting...
	Daemon: zenmodeler starting...
	Daemon: zenperfsnmp starting...
	Daemon: zencommand starting...
	Daemon: zenprocess starting...
	Daemon: zenwin starting...
	Daemon: zeneventlog starting.
	
<p>You can confirm if the ZenPack is installed by switching back to the <strong>zenoss</strong> user and running the following:</p>
	freebsd:~&gt;sudo su - zenoss
	$ zenpack --list
	ZenPacks.zenoss.LinuxMonitor (/usr/local/zenoss/ZenPacks/ZenPacks.zenoss.LinuxMonitor-1.1.5-py2.6.egg)
	
<p>Then go back to 'Infrastructure' Tab and expand the Hierarchy on the Left Panel to "Device Classes" -> "Server" -> "SSH" -> "Linux". At this point you will see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ssh-linux-device.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ssh-linux-device.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ssh-linux-device.png" alt="zenoss ssh linux device Monitor Different Systems with Zenoss" width="795" height="556" class="alignnone size-full wp-image-6547" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now click on the "Add Device" button, and select "Add a Single Device":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_button_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_button_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_button_g.png" alt="zenoss add device button g Monitor Different Systems with Zenoss" width="447" height="131" class="alignnone size-full wp-image-6585" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then fill out all the fields, here is how mine looked like:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_dialog.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_dialog.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_device_dialog.png" alt="zenoss add device dialog Monitor Different Systems with Zenoss" width="789" height="301" class="alignnone size-full wp-image-6552" title="Monitor Different Systems with Zenoss" /></a></p>
<p>After a little bit, you will see the device under the Infrastructure Tab:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_added_ubuntu.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_added_ubuntu.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_added_ubuntu.png" alt="zenoss added ubuntu Monitor Different Systems with Zenoss" width="936" height="484" class="alignnone size-full wp-image-6553" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now we need to add the SSH Login Credentials. Click on the newly added device and you will see this screen:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_details.png" alt="zenoss ubuntu details Monitor Different Systems with Zenoss" width="1236" height="564" class="alignnone size-full wp-image-6554" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Next let's confirm that the device will collect Linux information. Click on "Modeler Plugins" and you should see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_modeler_plugins.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_modeler_plugins.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_modeler_plugins.png" alt="zenoss ubuntu modeler plugins Monitor Different Systems with Zenoss" width="689" height="378" class="alignnone size-full wp-image-6555" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Notice the "Linux" Commands. Now select "Configuration Properties" and you will see this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_config_prop.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_config_prop.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_config_prop.png" alt="zenoss ubuntu config prop Monitor Different Systems with Zenoss" width="1224" height="449" class="alignnone size-full wp-image-6556" title="Monitor Different Systems with Zenoss" /></a></p>
<p>In this screen edit the <strong>zCommandPassword</strong> (SSH Password) and <strong>zCommandUsername</strong> (SSH User) properties accordingly. After you are done, click "Save" at the bottom of the screen. Now let's "model" the device; at the bottom left corner click on the "Gear" Icon and select "Model Device":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-model-device_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-model-device_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-model-device_g.png" alt="zenoss model device g Monitor Different Systems with Zenoss" width="1302" height="666" class="alignnone size-full wp-image-6586" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now you should see all the plugins getting executed:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenodd_model_device_terminal.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenodd_model_device_terminal.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenodd_model_device_terminal.png" alt="zenodd model device terminal Monitor Different Systems with Zenoss" width="768" height="477" class="alignnone size-full wp-image-6557" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Notice the "Using SSH Collection method" line (this is expected since we are using SSH). Now if you go back to the 'Infrastructure' tab and click on the device, under the device details you should see a new section called "Components". Selecting one of the components will show more information about the device:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu_components_int.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu_components_int.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu_components_int.png" alt="zenoss ubuntu components int Monitor Different Systems with Zenoss" width="1238" height="472" class="alignnone size-full wp-image-6558" title="Monitor Different Systems with Zenoss" /></a></p>
<p>You can also go to "Graphs" and see CPU, Memory, and Load graphs:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_graphs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_graphs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_ubuntu_graphs.png" alt="zenoss ubuntu graphs Monitor Different Systems with Zenoss" width="1141" height="541" class="alignnone size-full wp-image-6559" title="Monitor Different Systems with Zenoss" /></a></p>
<p>After everything have been configured, you should be able to see the device on the 'Infrastructure' tab without any issues:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu-no-issues.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu-no-issues.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-ubuntu-no-issues.png" alt="zenoss ubuntu no issues Monitor Different Systems with Zenoss" width="1238" height="375" class="alignnone size-full wp-image-6560" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now let's move to our FreeBSD machine.</p>
<h3>4. Monitor FreeBSD with Zenoss via SNMP</h3>
<p>Install instructions are found in <a href="http://community.zenoss.org/docs/DOC-9132" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-9132']);">this</a> Zenoss community page. First let's install the desired <strong>snmpd</strong> server:</p>
	freebsd:~&gt;cd /usr/ports/net-mgmt/bsnmp-ucd
	freebsd:/usr/ports/net-mgmt/bsnmp-ucd&gt;sudo make install clean
	freebsd:~&gt;cd /usr/ports/net-mgmt/bsnmptools
	freebsd:/usr/ports/net-mgmt/bsnmptools&gt;sudo make install clean
	
<p>Then edit the <strong>/etc/snmpd.conf</strong> file and add/modify the following lines:</p>
	read := "public"
	begemotSnmpdCommunityString.0.1 = $(read)
	begemotSnmpdPortStatus.192.168.1.101.161 = 1
	begemotSnmpdModulePath."mibII"  = "/usr/lib/snmp_mibII.so"
	begemotSnmpdModulePath."ucd" = "/usr/local/lib/snmp_ucd.so"
	
<p>Then let's enable the service, edit the <strong>/etc/rc.conf</strong> file an add the following:</p>
	bsnmpd_enable="YES"
	
<p>Then let's start up the <strong>bsmpd</strong> service:</p>
	freebsd:~&gt;sudo service bsnmpd start
	Starting bsnmpd.
	freebsd:~&gt;sudo service bsnmpd status
	bsnmpd is running as pid 77265.
	
<p>Then doing a quick test:</p>
	freebsd:~&gt;bsnmpwalk -v 2c -s public@192.168.1.101 system
	sysDescr.0 = freebsd.dnsd.me 2224368676 FreeBSD 9.1-RELEASE
	sysObjectId.0 = begemotSnmpdAgentFreeBSD
	sysUpTime.0 = 21234
	sysContact.0 = sysmeister@example.com
	sysName.0 = freebsd.dnsd.me
	sysLocation.0 = Room 200
	sysServices.0 = 76
	sysORLastChange.0 = 8
	sysORID[1] = begemotSnmpdTransUdp
	sysORID[2] = begemotSnmpdTransLsock
	sysORID[3] = snmpMIB
	sysORID[4] = begemotSnmpd
	sysORID[5] = ifMIB
	sysORID[6] = ipMIB
	sysORID[7] = tcpMIB
	sysORID[8] = udpMIB
	sysORID[9] = ipForward
	sysORID[10] = 1.3.6.1.4.1.2021
	sysORDescr[1] = udp transport mapping
	sysORDescr[2] = lsock transport mapping
	sysORDescr[3] = The MIB module for SNMPv2 entities.
	sysORDescr[4] = The MIB module for the Begemot SNMPd.
	sysORDescr[5] = The MIB module to describe generic objects for network interface sub-layers.
	sysORDescr[6] = The MIB module for managing IP and ICMP implementations, but excluding their management of IP routes.
	sysORDescr[7] = The MIB module for managing TCP implementations.
	sysORDescr[8] = The MIB module for managing UDP implementations.
	sysORDescr[9] = The MIB module for the display of CIDR multipath IP Routes.
	sysORDescr[10] = The MIB module for UCD-SNMP-MIB.
	sysORUpTime[1] = 0
	sysORUpTime[2] = 0
	sysORUpTime[3] = 8
	sysORUpTime[4] = 8
	sysORUpTime[5] = 8
	sysORUpTime[6] = 8
	sysORUpTime[7] = 8
	sysORUpTime[8] = 8
	sysORUpTime[9] = 8
	sysORUpTime[10] = 8
	freebsd:~&gt;
	
<p>Then going to the Zenoss dashboard and then going to the "Infrastructure" Tab, we can expand the left pane and go to "Device Classes" -> "Server" -> "Remote". Lastly we can click on "Add Device" -> "Add Single Device", and fill out all the options like so:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device_dialog_fb.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device_dialog_fb.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device_dialog_fb.png" alt="zenoss add device dialog fb Monitor Different Systems with Zenoss" width="791" height="546" class="alignnone size-full wp-image-6561" title="Monitor Different Systems with Zenoss" /></a></p>
<p>After the device is added we can see new components from the host:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd-device-details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd-device-details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd-device-details.png" alt="zenoss freebsd device details Monitor Different Systems with Zenoss" width="1243" height="477" class="alignnone size-full wp-image-6562" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Not as many as for Linux Host but still enough. Now let's monitor the Fedora Machine.</p>
<h3>5. Monitor the Fedora Machine with Zenoss via SNMP</h3>
<p>For regular Linux machines we can just use the <strong>net-snmp</strong> package, so let's go ahead and install that:</p>
	moxz:~&gt;sudo yum install net-snmp
	...
	...
	Installed:
	  net-snmp.i686 1:5.7.2-5.fc18                                                                                                           
	Dependency Installed:
	  net-snmp-agent-libs.i686 1:5.7.2-5.fc18                                                                                                
	Complete!
	
<p>Then let's set configure the service by editing the <strong>/etc/snmp/snmpd.conf</strong> file and adding/modifying the following lines (Most of these instructions are described in <a href="http://community.zenoss.org/docs/DOC-2502" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-2502']);">this</a> Zenoss community page):</p>
	view    systemview    included   .1
	rocommunity public
	
<p>Here is how the whole file looked like:</p>
	moxz:~&gt;grep -v -E '^#|^$' /etc/snmp/snmpd.conf
	com2sec notConfigUser   default         public
	group   notConfigGroup  v1           notConfigUser
	group   notConfigGroup  v2c           notConfigUser
	view    systemview    included   .1
	access  notConfigGroup ""      any       noauth    exact  systemview none none
	syslocation Unknown (edit /etc/snmp/snmpd.conf)
	syscontact Root &lt;root @localhost&gt; (configure /etc/snmp/snmp.local.conf)
	dontLogTCPWrappersConnects yes
	rocommunity public
	
<p>Now let's enable the <strong>snmpd</strong> service:</p>
	moxz:~&gt;sudo systemctl enable snmpd
	ln -s '/usr/lib/systemd/system/snmpd.service' '/etc/systemd/system/multi-user.target.wants/snmpd.service'
	
<p>Then let' start it:</p>
	moxz:~&gt;sudo systemctl start snmpd
	
<p>Lastly let's make sure it started fine:</p>
	moxz:~&gt;sudo systemctl status snmpd
	snmpd.service - Simple Network Management Protocol (SNMP) Daemon.
	          Loaded: loaded (/usr/lib/systemd/system/snmpd.service; enabled)
	          Active: active (running) since Sat 2013-02-23 17:24:15 PST; 4s ago
	        Main PID: 20879 (snmpd)
	          CGroup: name=systemd:/system/snmpd.service
	                  └─20879 /usr/sbin/snmpd -LS0-6d -f
	
<p>The only thing left to do is open up the firewall for UDP port <strong>161</strong>. Edit the <strong>/etc/sysconfig/iptables</strong> file and add the following line to it:</p>
	-A INPUT -m state --state NEW -m udp -p udp -s 192.168.1.0/24 --dport 161 -j ACCEPT
	
<p>Then restart <strong>iptables</strong> to apply the changes:</p>
	moxz:~&gt;sudo systemctl restart iptables
	
<p>Now let's do an <strong>snmpwalk</strong> from our Zenoss server:</p>
	freebsd:~&gt;snmpwalk -v 2c -c public 192.168.1.102 system
	SNMPv2-MIB::sysDescr.0 = STRING: Linux moxz.dnsd.me 3.7.8-202.fc18.i686 #1 SMP Fri Feb 15 17:57:07 UTC 2013 i686
	SNMPv2-MIB::sysObjectID.0 = OID: NET-SNMP-MIB::netSnmpAgentOIDs.10
	DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (46827) 0:07:48.27
	SNMPv2-MIB::sysContact.0 = STRING: Root &lt;/root&gt;&lt;root @localhost&gt; (configure /etc/snmp/snmp.local.conf)
	SNMPv2-MIB::sysName.0 = STRING: moxz.dnsd.me
	SNMPv2-MIB::sysLocation.0 = STRING: Unknown (edit /etc/snmp/snmpd.conf)
	SNMPv2-MIB::sysORLastChange.0 = Timeticks: (8) 0:00:00.08
	SNMPv2-MIB::sysORID.1 = OID: SNMP-MPD-MIB::snmpMPDCompliance
	SNMPv2-MIB::sysORID.2 = OID: SNMP-USER-BASED-SM-MIB::usmMIBCompliance
	SNMPv2-MIB::sysORID.3 = OID: SNMP-FRAMEWORK-MIB::snmpFrameworkMIBCompliance
	SNMPv2-MIB::sysORID.4 = OID: SNMPv2-MIB::snmpMIB
	SNMPv2-MIB::sysORID.5 = OID: TCP-MIB::tcpMIB
	SNMPv2-MIB::sysORID.6 = OID: IP-MIB::ip
	SNMPv2-MIB::sysORID.7 = OID: UDP-MIB::udpMIB
	SNMPv2-MIB::sysORID.8 = OID: SNMP-VIEW-BASED-ACM-MIB::vacmBasicGroup
	SNMPv2-MIB::sysORID.9 = OID: SNMP-NOTIFICATION-MIB::snmpNotifyFullCompliance
	SNMPv2-MIB::sysORID.10 = OID: NOTIFICATION-LOG-MIB::notificationLogMIB
	SNMPv2-MIB::sysORDescr.1 = STRING: The MIB for Message Processing and Dispatching.
	SNMPv2-MIB::sysORDescr.2 = STRING: The management information definitions for the SNMP User-based Security Model.
	SNMPv2-MIB::sysORDescr.3 = STRING: The SNMP Management Architecture MIB.
	SNMPv2-MIB::sysORDescr.4 = STRING: The MIB module for SNMPv2 entities
	SNMPv2-MIB::sysORDescr.5 = STRING: The MIB module for managing TCP implementations
	SNMPv2-MIB::sysORDescr.6 = STRING: The MIB module for managing IP and ICMP implementations
	SNMPv2-MIB::sysORDescr.7 = STRING: The MIB module for managing UDP implementations
	SNMPv2-MIB::sysORDescr.8 = STRING: View-based Access Control Model for SNMP.
	SNMPv2-MIB::sysORDescr.9 = STRING: The MIB modules for managing SNMP Notification, plus filtering.
	SNMPv2-MIB::sysORDescr.10 = STRING: The MIB module for logging SNMP Notifications.
	SNMPv2-MIB::sysORUpTime.1 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.2 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.3 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.4 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.5 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.6 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.7 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.8 = Timeticks: (7) 0:00:00.07
	SNMPv2-MIB::sysORUpTime.9 = Timeticks: (8) 0:00:00.08
	SNMPv2-MIB::sysORUpTime.10 = Timeticks: (8) 0:00:00.08
	
<p>Now let's go back to the Zenoss Dashboard and go to the Infrastructure tab, then expand "Device Classes" -> "Server" -> "Linux". Lastly click on "Add Device" -> "Add a Single Device" and fill out the information. Here is how mine looked like:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device-diag-fed2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device-diag-fed2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-device-diag-fed2.png" alt="zenoss add device diag fed2 Monitor Different Systems with Zenoss" width="791" height="545" class="alignnone size-full wp-image-6569" title="Monitor Different Systems with Zenoss" /></a></p>
<p>After the device was added and 'modeled', I saw similar information under the components section as I did for the other machines:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-fedora-device-details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-fedora-device-details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-fedora-device-details.png" alt="zenoss fedora device details Monitor Different Systems with Zenoss" width="844" height="491" class="alignnone size-full wp-image-6568" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now let's monitor our RAID on the FreebSD Machine.</p>
<h3>5. Add a Raid Check in Zenoss for the FreeBSD machine.</h3>
<p>Instructions on how to run commands and gather information from the output are in the <a href="http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/community/documentation/official_documentation/zenoss-guide']);">Admin Guide</a> (in the Chapter Entitled "Monitoring Using ZenCommand") and in <a href="http://community.zenoss.org/docs/DOC-3909" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-3909']);">this</a> community forum. I knew that Zenoss could use Nagios plugins, so I found two scripts online: one written in <a href="http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/Adaptec-RAID-Check-by-Anchor-Systems/details" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/Adaptec-RAID-Check-by-Anchor-Systems/details']);">Python</a> and the other in <a href="http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/check_aacraid-Adaptec-and-ICP-Controller-Monitoring/details" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/check_aacraid-Adaptec-and-ICP-Controller-Monitoring/details']);">Perl</a>. I downloaded the Perl script, made some changes to it (path changes and such), copied it to the Zenoss install, and ran a test:</p>
	freebsd:~&gt;sudo cp check_aacraid.pl /usr/local/zenoss/libexec/check_aacraid
	freebsd:~&gt;sudo su - zenoss
	$libexec/check_aacraid 
	controller status seems fine
	$ echo $?
	0
	
<p>No errors were reported and the correct status was returned. I didn't have a battery in the controller, so initially I remove that check but re-enabling the check and re-running the command I would get this:</p>
	$ libexec/check_aacraid
	battery status of controller 1 not optimal!&lt;br /&gt;
	$ echo $?
	1
	
<p>We can see that the status is now 1 (Warning), which is expected. So the script was working just fine. Now we need to create a local template for our device and add a new "Data Source" to the template. If we just add the Data Source to the original template, it would impact any Machine that is part of that template. So go to the "Infrastructure" tab and select our FreeBSD machine. We will see this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd_details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd_details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-freebsd_details.png" alt="zenoss freebsd details Monitor Different Systems with Zenoss" width="1227" height="603" class="alignnone size-full wp-image-6594" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then from the bottom left corner, select "Add Local Template":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template_button_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template_button_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template_button_g.png" alt="zenoss add local template button g Monitor Different Systems with Zenoss" width="273" height="490" class="alignnone size-full wp-image-6692" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then name the Template as you desire, here is how mine looked like:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_local_template.png" alt="zenoss add local template Monitor Different Systems with Zenoss" width="588" height="290" class="alignnone size-full wp-image-6595" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then you will see this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_new_local_template.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_new_local_template.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_new_local_template.png" alt="zenoss new local template Monitor Different Systems with Zenoss" width="683" height="440" class="alignnone size-full wp-image-6596" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Notice you new Template under the "Monitoring Templates" Section. Now click on the '+' button and name your command, here is how mine looked like:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_command.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_command.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_add_command.png" alt="zenoss add command Monitor Different Systems with Zenoss" width="304" height="125" class="alignnone size-full wp-image-6597" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Once added, select the "Data Source" and click on the Gear -> "View and Edit Detail":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_edit_details_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_edit_details_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_edit_details_g.png" alt="zenoss data source edit details g Monitor Different Systems with Zenoss" width="662" height="447" class="alignnone size-full wp-image-6693" title="Monitor Different Systems with Zenoss" /></a></p>
<p>then fill out all the fields like so:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_details_dialog.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_details_dialog.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_data_source_details_dialog.png" alt="zenoss data source details dialog Monitor Different Systems with Zenoss" width="788" height="486" class="alignnone size-full wp-image-6598" title="Monitor Different Systems with Zenoss" /></a></p>
<p>and "Save" the config. Go back to the Zenoss server and as the <strong>zenoss</strong> user run the following:</p>
	zencommand run -d 192.168.1.101 -v10
	
<p>There is a going to be a bunch of output, but here are the important snippets:</p>
	2013-02-24 15:50:15,451 DEBUG zen.SshClient: 192.168.1.101 SshClient has 1 commands to assign to channels (max = 10, current = 0)
	2013-02-24 15:50:15,452 DEBUG zen.SshClient: 192.168.1.101 channel 0 SshConnection added command /usr/local/zenoss/libexec/check_aacraid
	2013-02-24 15:50:15,453 DEBUG zen.SshClient: 192.168.1.101 channel 1 Opening command channel for /usr/local/zenoss/libexec/check_aacraid
	...
	...
	2013-02-24 15:50:47,237 DEBUG zen.SshClient: 192.168.1.101 channel 1 CommandChannel exit code for /usr/local/zenoss/libexec/check_aacrai
	d is 0: Success
	2013-02-24 15:50:47,238 DEBUG zen.SshClient: 192.168.1.101 channel 0 SshConnection closing
	2013-02-24 15:50:47,238 DEBUG zen.SshClient: 192.168.1.101 channel 1 CommandChannel closing command channel for command /usr/local/zenoss/libexec/check_aacraid with data: 'controller status seems fine'
	2013-02-24 15:50:47,239 DEBUG zen.zencommand: Process check_aacraid stopped (0), 33.26 seconds elapsed
	2013-02-24 15:50:47,239 DEBUG zen.zencommand: Queueing event {'manager': 'freebsd.dnsd.me', 'eventKey': 'Raid_Check', 'device': '192.168.1.101', 'eventClass': '/Cmd/Fail', 'summary': 'Cmd: /usr/local/zenoss/libexec/check_aacraid - Code: 0 - Msg: Success', 'component': 'Raid_Status', 'monitor': 'localhost', 'agent': 'zencommand', 'severity': 0}
	
<p>Looks like it went through just fine (the appropriate return status is seen). I then modified the script to output how many disks are in the raid. Here is how the output of the command looks like after the change:</p>
	$ libexec/check_aacraid 
	controller status seems fine|disks=2
	
<p>After make that addition, here is how output from the above <strong>zencommand</strong> looked like:</p>
	2013-02-24 18:40:57,103 DEBUG zen.zencommand: Queueing event {'manager': 'freebsd.dnsd.me', 'eventKey': 'Raid_Check', 'device': '192.168.1.101', 'eventClass': '/Status', 'summary': 'Cmd: /usr/local/zenoss/libexec/check_aacraid - Code: 0 - Msg: Success', 'component': 'Raid
	_Status', 'monitor': 'localhost', 'agent': 'zencommand', 'severity': 0}
	2013-02-24 18:40:57,103 DEBUG zen.zencommand: Total of 1 queued events
	2013-02-24 18:40:57,104 DEBUG zen.zencommand: The result of "/usr/local/zenoss/libexec/check_aacraid" was "'controller status seems fine|disks=2'"
	2013-02-24 18:40:57,108 DEBUG zen.zencommand: Storing disks = 2.0 into Devices/192.168.1.101/Raid_Check_disks
	2013-02-24 18:40:57,108 DEBUG zen.RRDUtil: /usr/local/zenoss/perf/Devices/192.168.1.101/Raid_Check_disks.rrd: 2.0
	2013-02-24 18:40:57,109 DEBUG zen.zencommand: RRD save result: 2.0
	
<p>Now we can plot how many disks are online (we can see from the above output that a new RRD file has been generated), just like before. To plot it we first need to add a "Data Point" to our "Data Source". This is done by going to the "Data Source" view and clicking on the our "Data Source" (Raid_Check in our case) and then selecting "Add Data Point":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-button_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-button_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-button_g.png" alt="zenoss add data point button g Monitor Different Systems with Zenoss" width="628" height="148" class="alignnone size-full wp-image-6694" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then just call it "disks".</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss-add-data-point-dialog.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss-add-data-point-dialog.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss-add-data-point-dialog.png" alt="zenoss add data point dialog Monitor Different Systems with Zenoss" width="300" height="102" class="alignnone size-full wp-image-7439" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then under the "Graph Definitions", do the same thing and create a graph called "disks":</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-graph-definitions.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-graph-definitions.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-graph-definitions.png" alt="zenoss graph definitions Monitor Different Systems with Zenoss" width="305" height="113" class="alignnone size-full wp-image-6600" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Now click on the "Data Point" called "disks" and then click on "Add Data Point to Graph" like so:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-to-graph_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-to-graph_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-add-data-point-to-graph_g.png" alt="zenoss add data point to graph g Monitor Different Systems with Zenoss" width="624" height="136" class="alignnone size-full wp-image-6695" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Then select the graph "disks" from the drop down menu and click add:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss_select_graph_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss_select_graph_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zenoss_select_graph_g.png" alt="zenoss select graph g Monitor Different Systems with Zenoss" width="306" height="191" class="alignnone size-full wp-image-7440" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Lastly go the "Graphs" view and scroll down to the bottom and you will see a couple of plot points of our new graph:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_raid_graph.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_raid_graph.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_raid_graph.png" alt="zenoss raid graph Monitor Different Systems with Zenoss" width="885" height="518" class="alignnone size-full wp-image-6601" title="Monitor Different Systems with Zenoss" /></a></p>
<p>As a test, I made the script return a bad value and I saw the following in my "Infrastructure" view:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-device-warning.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-device-warning.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss-device-warning.png" alt="zenoss device warning Monitor Different Systems with Zenoss" width="1239" height="337" class="alignnone size-full wp-image-6602" title="Monitor Different Systems with Zenoss" /></a></p>
<p>Clicking on the warning showed me this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_broken_raid_events.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_broken_raid_events.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/zenoss_broken_raid_events.png" alt="zenoss broken raid events Monitor Different Systems with Zenoss" width="1234" height="159" class="alignnone size-full wp-image-6603" title="Monitor Different Systems with Zenoss" /></a></p>
<p>We can even see the message that was returned from the script.</p>
<h3>6. Zenoss Vs. Collectd and Munin</h3>
<h4>Pros</h4>
<ul>
<li>
<p>There is a command line tool to check status of the Zenoss system, it's called <strong>zendmd</strong>. More information can be seen in the <a href="http://community.zenoss.org/community/documentation/official_documentation/zenoss-dev-guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/community/documentation/official_documentation/zenoss-dev-guide']);">Development Guide</a>. Here is a quick example:</p>
	$ zendmd
	Welcome to the Zenoss dmd command shell!
	'dmd' is bound to the DataRoot. 'zhelp()' to get a list of commands.
	Use TAB-TAB to see a list of zendmd related commands.
	Tab completion also works for objects -- hit tab after an object name and '.'
	(eg dmd. + tab-key).
	&gt;&gt;&gt; d=find ('Ubuntu')
	&gt;&gt;&gt; for i in d.os.interfaces():
	...  for a in i.ipaddresses():
	...   print a.name(), a.getIpAddress()
	...
	eth0 192.168.1.100/24
	
<p>which is pretty cool</p>
</li>
</ul>
<p><!-- t --></p>
<ul>
<li>The Web Interface is rich and easy to use</li>
<li>Creating Custom Graphs is a breeze</li>
<li>Has the capability of using Nagios Plugins</li>
<li>'Agentless' monitoring of Nodes, mostly uses SSH and SNMP</li>
<li>Does it all: monitor, graph, notify, and much more</li>
<li>Doesn't depend on Apache, uses a Zope Instance for it's web management portal</li>
</ul>
<h4>Cons</h4>
<ul>
<li>
<p>It's a beast, the install comes with so many daemons installed</p>
	freebsd:~&gt;ps auxw | grep zenoss | grep -v grep | wc -l
	17
	
</li>
</ul>
<p><!-- t --></p>
<ul>
<li>Installs it's own components, it even installs it's own Python version</li>
<li>Requires an External Database (MySQL)</li>
<li>Doesn't provide as much monitoring for FreeBSD nodes as for the Linux nodes</li>
</ul>
<p>Other than being resource intensive, I actually liked the software. I also ran into other sites that mentioned <em>Zabbix</em> as being a good alternative and not as resource intensive:</p>
<ul>
<li><a href="http://www.serverfocus.org/nagios-vs-cacti-vs-zabbix-vs-zenoss" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.serverfocus.org/nagios-vs-cacti-vs-zabbix-vs-zenoss']);">Nagios vs Cacti vs Zabbix vs Zenoss</a> </li>
<li><a href="http://honglus.blogspot.com/2010/12/zabbix-vs-zenoss.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://honglus.blogspot.com/2010/12/zabbix-vs-zenoss.html']);">Zabbix VS Zenoss</a></li>
</ul>
<p>So I will extend this series to one more post <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Monitor Different Systems with Zenoss" class="wp-smiley" title="Monitor Different Systems with Zenoss" /> </p>
<p><root> </root></p>
