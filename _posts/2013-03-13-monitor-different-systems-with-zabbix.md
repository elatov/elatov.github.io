---
title: Monitor Different Systems with Zabbix
author: Karim Elatov
layout: post
permalink: /2013/03/monitor-different-systems-with-zabbix/
dsq_thread_id:
  - 1406357258
categories:
  - Home Lab
  - OS
tags:
  - Monitoring
  - Zabbix
---
This is the last post from the "Network Monitoring Software Comparison" series. As I mentioned in the [main](http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zenoss) page here is what Zabbix is about:

> Zabbix is an enterprise-class open source distributed monitoring solution.
>
> Zabbix is software that monitors numerous parameters of a network and the health and integrity of servers. Zabbix uses a flexible notification mechanism that allows users to configure e-mail based alerts for virtually any event. This allows a fast reaction to server problems. Zabbix offers excellent reporting and data visualisation features based on the stored data. This makes Zabbix ideal for capacity planning.
>
> Zabbix supports both polling and trapping. All Zabbix reports and statistics, as well as configuration parameters, are accessed through a web-based front end. A web-based front end ensures that the status of your network and the health of your servers can be assessed from any location. Properly configured, Zabbix can play an important role in monitoring IT infrastructure. This is equally true for small organisations with a few servers and for large companies with a multitude of servers.

So let's try it out.

## Install Zabbix Server on Ubuntu

Most of the instructions can be found in this [Zabbix](https://www.zabbix.com/documentation/2.0/manual/installation) page. First let's install the software:

    kerch:~>sudo apt-get install zabbix-server-mysql zabbix-frontend-php


Now we need to setup the MySQL database. Instructions for the setup can be found online [here](https://www.zabbix.com/documentation/doku.php?id=2.0/manual/appendix/install/db_scripts), or in the **/usr/share/doc/zabbix-server-mysql/README.Debian** file (after the **zabbix-server** package has been installed). Here are the commands I ran to setup the MySQL database for Zabbix:

    kerch:~>mysql -u root -p -e "create database zabbix character set utf8"
    kerch:~>mysql -u root -p -e "grant all on zabbix.* to 'zabbix'@'localhost' identified by 'password'"
    kerch:~>zcat /usr/share/zabbix-server-mysql/{schema,images,data}.sql.gz | mysql -uzabbix -ppassword zabbix


Now let's add the MySQL credentials to the Zabbix configuration files and enable the service. First edit the **/etc/zabbix/zabbix_server.conf** file, add the MySQL stuff, and set the IP of the Zabbix server. Here is how my configuration file looked like after I was done:

    kerch:~>grep -vE '^#|^$' /etc/zabbix/zabbix_server.conf
    SourceIP=192.168.1.100
    LogFile=/var/log/zabbix-server/zabbix_server.log
    PidFile=/var/run/zabbix/zabbix_server.pid
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=password
    AlertScriptsPath=/etc/zabbix/alert.d/
    FpingLocation=/usr/bin/fping
    Fping6Location=/usr/bin/fping6


Then let's enable the service by editing the **/etc/default/zabbix-server** file and modifying the following line to look like this:

    kerch:~>grep -vE '^#|^$' /etc/default/zabbix-server
    START=yes


Now let's start the service:

    kerch:~>sudo service zabbix-server start
    kerch:~>sudo service zabbix-server status
    * zabbix_server is running


Lastly let's enable the web front-end. First, create the directory where the files will be hosted:

    kerch:~>sudo mkdir /var/www/zab


then copy the PHP files:

    kerch:~>sudo rsync -avzP /usr/share/zabbix/. /var/www/zab/.


Lastly visit the site at **127.0.0.1/zab**. When I did, I saw the following:

![zabbix web front end setup page Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_end_setup_page.png)

I then clicked "Next" and I saw the following:

![zabbic web front php setting fail Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbic_web_front_php_setting_fail.png)

It looks like some of my PHP options were not up to Zabbix's standards. So I edited the **/etc/php5/apache2/php.ini** file and fixed all of the above options, then I restarted Apache like so:

    kerch:~>sudo service apache2 restart
    * Restarting web server apache2
    ... waiting [ OK ]


Then clicking **Retry**, I saw the following:

![zabbix web front php settings pass Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_php_settings_pass.png)

then I clicked "Next" and saw the database page, I filled out the settings and clicked "Test Connection" and it was successful, like so:

![zabbix web front mysql settings Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_mysql_settings.png)

Then, I filled out the server connection details:

![zabbix web front server details Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_server_details.png)

And then I saw the pre-installation summary page:

![zabbix web front summary detail Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_summary_detail.png)

it then tried to auto create a configuration file under **/etc/zabbix** but it failed:

![zabbix web front install config file Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file.png)

So I downloaded it manually and copied the file to the appropriate location:

    kerch:~>sudo cp zabbix.conf.php /etc/zabbix/.


Then hitting "Retry" I saw the following page:

![zabbix web front install config file pass Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file_pass.png)

Hitting "Next" yielded the following page:

![zabbix web front login page Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_login_page.png)

You can login with Username: **Admin**, Password: **zabbix**. After you login, you can create another user; instruction on user setup and default password are [here](https://www.zabbix.com/documentation/2.0/manual/quickstart/login). After I logged in, I saw the following:

![zabbix web front dashboard Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_dashboard.png)

Now let's start monitoring some systems.

## Monitor an Ubuntu Machine with Zabbix

First let's install the **zabbix-agent** package:

    kerch:~>sudo apt-get install zabbix-agent


then edit the **/etc/zabbix/zabbix_agentd.conf** file and add/modify the following:

    kerch:~>grep -vE '^#|^$' /etc/zabbix/zabbix_agentd.conf
    PidFile=/var/run/zabbix/zabbix_agentd.pid
    LogFile=/var/log/zabbix-agent/zabbix_agentd.log
    LogFileSize=0
    Server=192.168.1.100
    ListenIP=192.168.1.100
    ServerActive=192.168.1.100
    Hostname=kerch.dnsd.me
    Include=/etc/zabbix/zabbix_agentd.conf.d


Then start the agent and make sure it's running:

    kerch:~>sudo service zabbix-agent start
    kerch:~>sudo service zabbix-agent status
      * zabbix_agentd is running


This node is a special case since it will be both the server and a node. So make sure both are running:

    kerch:~>sudo netstat -antp | grep zabbix
    tcp        0      0 192.168.1.100:10050     0.0.0.0:*               LISTEN      683/zabbix_agentd
    tcp        0      0 0.0.0.0:10051           0.0.0.0:*               LISTEN      4784/zabbix_server


That looks good. Now let's add the host to be monitored with Zabbix via the PHP frontend. Most of the instructions are laid out [here](https://www.zabbix.com/documentation/2.0/manual/config/hosts/host). So in the Zabbix Dashboard go to "Configuration" -> "Hosts" and you will see the following:

![zabbix web conf hosts Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_conf-hosts.png)

Then click on "Create Host" and fill out all the information, mine looked like this:

![zabbix web create host Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host.png)

Under the template section choose "Template OS Linux":

![zabbix web create host add template Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host_add_template.png)

Then click "Save" and you will see the following:

![zabbix web host added Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_host_added.png)

At first I checked out a graph but the font was missing for some reason, I found a fix on the Zabbix forums from [here](https://www.zabbix.com/forum/showthread.php?p=91923). After I pointed to the appropriate path for the fonts, I was able to see the graphs like so:

![zabbix web graph cpu usage Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_graph_cpu_usage.png)

Also going to "Monitoring" -> "Overview" you can see current values for our hosts:

![zabbix monitoring overview Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_monitoring_overview.png)

Now let's add our FreeBSD machine to the mix.

### Monitor FreeBSD with Zabbix

First let's install the **zabbix-agent**:

    freebsd:~>cd /usr/ports/net-mgmt/zabbix2-agent/
    freebsd:/usr/ports/net-mgmt/zabbix2-agent/>sudo make install clean


after the install is finished enable the service by adding:

    zabbix_agentd_enable="YES"


to **/etc/rc.conf**. Next let's copy the default configuration file:

    freebsd:~>sudo cp /usr/local/etc/zabbix2/zabbix_agentd.conf.sample /usr/local/etc/zabbix2/zabbix_agentd.conf


Now edit the **/usr/local/etc/zabbix2/zabbix_agentd.conf** file and set it up to connect to our server. Here is how my file looked like at the end:

    freebsd:~>grep -vE '^#|^$' /usr/local/etc/zabbix2/zabbix_agentd.conf
    LogFile=/tmp/zabbix_agentd.log
    Server=192.168.1.100
    ListenIP=192.168.1.101
    ServerActive=192.168.1.100
    Hostname=freebsd.dnsd.me


Lastly start the agent:

    freebsd:~>sudo service zabbix_agentd start
    Starting zabbix_agentd.
    freebsd:~>sudo service zabbix_agentd status
    zabbix_agentd is running as pid 60263 60264 60265 60266 60267 60268.


Lastly ensure it's listening on the correct port:

    freebsd:~>sockstat -4 | grep zabbix
    zabbix zabbix_age 60268 4 tcp4 192.168.1.101:10050 *:*
    zabbix zabbix_age 60267 4 tcp4 192.168.1.101:10050 *:*
    zabbix zabbix_age 60266 4 tcp4 192.168.1.101:10050 *:*
    zabbix zabbix_age 60265 4 tcp4 192.168.1.101:10050 *:*
    zabbix zabbix_age 60264 4 tcp4 192.168.1.101:10050 *:*
    zabbix zabbix_age 60263 4 tcp4 192.168.1.101:10050 *:*


Now let's add the host to the Zabbix server. Go back to the dashboard (**127.0.0.1/zab**) and then go to "Configuration" -> "Hosts" -> "Create Host" and fill out all the necessary information:

![zabbix add freebsd host Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_freebsd_host.png)

And under templates choose, "Template OS FreeBSD":

![zabbix freebsd os template Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_os_template.png)

After a little bit of time you should see the host as monitored with a green **Z** under "Configuration" -> "Hosts":

![zabbix freebsd green z Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_green_z.png)

If you want to check what items will be monitored, you can go to "Configuration" -> "Host" -> Pick a Host -> "Items" and you will see a list of all the checks:

![zabbix freebsd monitored items Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_monitored_items.png)

From there you can add triggers and graphs depending on the items, but we will get into that later. Now let's add another machine to monitor.

## Monitor Fedora with Zabbix

As always, let's install the software:

    moxz:~>sudo yum install zabbix-agent


Now let's configure the agent by editing the **/etc/zabbix_agentd.conf** file. Here is how my file looked like:

    moxz:~>grep -vE '^#|^$' /etc/zabbix_agentd.conf
    PidFile=/var/run/zabbix/zabbix_agentd.pid
    LogFile=/var/log/zabbix/zabbix_agentd.log
    LogFileSize=0
    Server=192.168.1.100
    ListenIP=192.168.1.102
    ServerActive=192.168.1.100
    Hostname=moxz.dnsd.me


Now let's enable the agent and start it up:

    moxz:~>sudo service zabbix-agent enable
    Redirecting to /bin/systemctl enable zabbix-agent.service
    ln -s '/usr/lib/systemd/system/zabbix-agent.service' '/etc/systemd/system/multi-user.target.wants/zabbix-agent.service'
    moxz:~>sudo service zabbix-agent start
    Redirecting to /bin/systemctl start zabbix-agent.service
    moxz:~>sudo service zabbix-agent status
    Redirecting to /bin/systemctl status  zabbix-agent.service
    zabbix-agent.service - Zabbix Monitor Agent
          Loaded: loaded (/usr/lib/systemd/system/zabbix-agent.service; enabled)
          Active: active (exited) since Wed 2013-03-06 12:54:25 PST; 6h ago
         Process: 14065 ExecStart=/usr/sbin/zabbix_agentd (code=exited, status=0/SUCCESS)


Open up the firewall for TCP port **10050** by adding the following :

    -A INPUT -s 192.168.1.0/24 -p tcp -m state --state NEW -m tcp --dport 10050 -j ACCEPT


to the **/etc/sysconfig/iptables** file and restarting the **iptables** service like so:

    sudo service iptables restart


Lastly add the host using the Zabbix front-end and make sure "Template OS Linux" is selected. When it's all done we should see something like this under "Configuration" -> "Hosts":

![zabbix all three greenZ Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_all_three_greenZ.png)

## Monitor raid status on FreeBSD with Zabbix

There are good examples in [this](https://www.zabbix.com/wiki/howto/monitor/os/linux/smart) post. We will have to use "User Parameters" to get this working. The first link from above describes the process pretty well. I will define two parameters

*   raid.active_drives
*   raid.controller_status

First let's run the commands that will provide the above paramaters:

    freebsd:~>/usr/local/sbin/arcconf getconfig 1 PD | grep State | grep Online| /usr/bin/wc -l
    2


and here is the second one:

    freebsd:~>/usr/local/sbin/arcconf getconfig 1 AD | grep "Controller Status" | grep -vc Optimal
    0


if the value is non zero then we know we are not at an **Optimal** state. So let's add both to our **zabbix_agentd** config under **/usr/local/etc/zabbix2/zabbix_agentd.conf**:

    ## Return Number of online drives
    UserParameter=raid.active_drives,/usr/local/sbin/arcconf getconfig 1 PD | grep State | grep Online| /usr/bin/wc -l
    ## Return 1 if status of raid is not optimal
    UserParameter=raid.controller_status,/usr/local/sbin/arcconf getconfig 1 AD | grep "Controller Status" | grep -vc Optimal


Now let's restart the **zabbix-agentd** process:

    freebsd:~>sudo service zabbix_agentd restart
    Stopping zabbix_agentd. Waiting for PIDS: 60263 60264 60265 60266 60267 60268.
    Starting zabbix_agentd.


Now let's see if we can get those values locally as the zabbix user:

    freebsd:~>sudo su -m zabbix -c '/usr/local/sbin/arcconf getconfig 1 PD | grep State | grep Online| /usr/bin/wc -l'
    2
    freebsd:~>sudo su -m zabbix -c '/usr/local/sbin/arcconf getconfig 1 AD | grep "Controller Status" | grep -vc Optimal'
    0


That looks good. Now let's see if we do it via the **zabbix_agentd** process:

    freebsd:~>zabbix_agentd -t raid.active_drives
    Alarm clock


Initially it looks like I was getting a SIGARLM signal, I then updated the 'timeout' value to 30 seconds:

    freebsd:~>grep ^Time /usr/local/etc/zabbix2/zabbix_agentd.conf
    Timeout=30


and restarted the zabbix_agentd service and after that the command ran:

    freebsd:~>zabbix_agentd -t raid.active_drives
    raid.active_drives [/usr/local/sbin/arcconf getconfig 1 PD | grep State | grep Online| /usr/bin/wc -l] [t| 2]
    freebsd:~>zabbix_agentd -t raid.controller_status
    raid.controller_status [/usr/local/sbin/arcconf getconfig 1 AD | grep "Controller Status" | grep -vc Optimal] [t|0]


Both look good. Now trying the same thing from the Zaabix server:

    kerch:~>zabbix_get -s 192.168.1.101 -k raid.active_drives
    2
    kerch:~>zabbix_get -s 192.168.1.101 -k raid.controller_status
    0


That looks good. Now to add items for our new values. From the Zabbix front-end go to "Configuration" -> "Hosts" -> Select FreebSD -> "Items" -> "Create Item" and fill out all the settings:

![zabbix add raid online drives item Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_raid_online_drives_item.png)

When finished, click "Save". Then from the same window click on "Graphs" -> "Create Graph" and fill out the information:

![zabbix graph raid disks Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_raid_disks.png)

Then checking out the graph (by going to "Monitoring" -> "Graphs" -> "Host" -> "FreeBSD" -> "Graph" -> "Raid_#_Disks_Online"), here is what I saw:

![zabbix graph disks online Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_disks_online.png)

Now let's setup a new item for the controller status. Go to "Configuration" -> "Hosts" -> Select host -> "Items" -> "Create New Item" and fill out all the information:

![zabbix item raid cont status Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_item_raid_cont_status.png)

Then from the same page, click on "Triggers" -> "Create Trigger". In the new window select "Add" under Trigger Expressions and make the follow expression:

![zabbix trigger expression Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_expression.png)

then click "Save". Your final result will look like this:

![zabbix add trigger Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_trigger.png)

You can go to "Monitoring" -> "Latest Data" and then expand the Name when you groupped your item, in my case I put it under OS. Expanding OS, I saw the latest value of that item:

![zabbix latest data controller status Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_latest_data_controller_status.png)

Also forcing a non-zero return value from that script yeilded the trigger to be fired. Here is what I saw under "Monitoring" -> "Triggers":

![zabbix trigger fired Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_fired.png)

and then fixing the script to return the correct value, allowed the trigger to be fixed. Here is what I saw under "Monitoring" -> "Events" after the issue was fixed:

![zabbix events after issue fixed Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_events_after_issue_fixed.png)

## Zabbix Vs. Zenoss, Munin, and Collectd

### PROs

*   Lightweight compared to Zenoss and for all the functionality that it provides
*   Doesn't Depend on Python or Perl
*   Supports MySQL, PSQL, and SQlite
*   Very easy to customize Triggers and Graphs
*   Has the capability to monitor with agents and without
*   Has great support for most OSes, even FreeBSD
*   Works like an Intrusion Detection System (IDS). I installed a new software and it automatically added a new user, I then saw the following under events: ![zabbix password changed Monitor Different Systems with Zabbix](http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_password_changed.png)

### CONs

*   Depends on PHP, the front-end a little slow and not as cosmetic as Zenoss
*   Doesn't support Nagios plugins
*   Doesn't load multiple Graphs at ones, only one aspect at a time (CPU or Memory but not both)
*   Requires an external Database (MySQL)

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>

  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" href="http://virtuallyhyper.com/2013/12/configure-ipmi-supermicro-server-monitor-ipmi-sensors-zabbix/" rel="bookmark">Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor SMART Attributes with Zabbix" href="http://virtuallyhyper.com/2013/10/monitor-smart-attributes-zabbix/" rel="bookmark">Monitor SMART Attributes with Zabbix</a>
    </li>
  </ul>
</div>

