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
This is the last post from the "Network Monitoring Software Comparison" series. As I mentioned in the <a href="http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zenoss" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zenoss']);">previous</a> post, I was going to expand the series to one more post to discuss **Zabbix**. Let's get to it, from Zabbix's <a href="https://www.zabbix.com/documentation/2.0/manual/introduction" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/documentation/2.0/manual/introduction']);">main</a> page here is what Zabbix is about:

> Zabbix is an enterprise-class open source distributed monitoring solution.
> 
> Zabbix is software that monitors numerous parameters of a network and the health and integrity of servers. Zabbix uses a flexible notification mechanism that allows users to configure e-mail based alerts for virtually any event. This allows a fast reaction to server problems. Zabbix offers excellent reporting and data visualisation features based on the stored data. This makes Zabbix ideal for capacity planning.
> 
> Zabbix supports both polling and trapping. All Zabbix reports and statistics, as well as configuration parameters, are accessed through a web-based front end. A web-based front end ensures that the status of your network and the health of your servers can be assessed from any location. Properly configured, Zabbix can play an important role in monitoring IT infrastructure. This is equally true for small organisations with a few servers and for large companies with a multitude of servers.

So let's try it out.

## Install Zabbix Server on Ubuntu

Most of the instructions can be found in this <a href="https://www.zabbix.com/documentation/2.0/manual/installation" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/documentation/2.0/manual/installation']);">Zabbix</a> page. First let's install the software:

    kerch:~>sudo apt-get install zabbix-server-mysql zabbix-frontend-php
    

Now we need to setup the MySQL database. Instructions for the setup can be found online <a href="https://www.zabbix.com/documentation/doku.php?id=2.0/manual/appendix/install/db_scripts" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/documentation/doku.php?id=2.0/manual/appendix/install/db_scripts']);">here</a>, or in the **/usr/share/doc/zabbix-server-mysql/README.Debian** file (after the **zabbix-server** package has been installed). Here are the commands I ran to setup the MySQL database for Zabbix:

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_end_setup_page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_end_setup_page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_end_setup_page.png" alt="zabbix web front end setup page Monitor Different Systems with Zabbix" width="827" height="539" class="alignnone size-full wp-image-7216" title="Monitor Different Systems with Zabbix" /></a>

I then clicked "Next" and I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbic_web_front_php_setting_fail.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbic_web_front_php_setting_fail.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbic_web_front_php_setting_fail.png" alt="zabbic web front php setting fail Monitor Different Systems with Zabbix" width="809" height="524" class="alignnone size-full wp-image-7217" title="Monitor Different Systems with Zabbix" /></a>

It looks like some of my PHP options were not up to Zabbix's standards. So I edited the **/etc/php5/apache2/php.ini** file and fixed all of the above options, then I restarted Apache like so:

    kerch:~>sudo service apache2 restart
    * Restarting web server apache2 
    ... waiting [ OK ]
    

Then clicking **Retry**, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_php_settings_pass.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_php_settings_pass.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_php_settings_pass.png" alt="zabbix web front php settings pass Monitor Different Systems with Zabbix" width="831" height="523" class="alignnone size-full wp-image-7218" title="Monitor Different Systems with Zabbix" /></a>

then I clicked "Next" and saw the database page, I filled out the settings and clicked "Test Connection" and it was successful, like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_mysql_settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_mysql_settings.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_mysql_settings.png" alt="zabbix web front mysql settings Monitor Different Systems with Zabbix" width="809" height="517" class="alignnone size-full wp-image-7219" title="Monitor Different Systems with Zabbix" /></a>

Then, I filled out the server connection details:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_server_details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_server_details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_server_details.png" alt="zabbix web front server details Monitor Different Systems with Zabbix" width="793" height="514" class="alignnone size-full wp-image-7220" title="Monitor Different Systems with Zabbix" /></a>

And then I saw the pre-installation summary page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_summary_detail.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_summary_detail.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_summary_detail.png" alt="zabbix web front summary detail Monitor Different Systems with Zabbix" width="815" height="512" class="alignnone size-full wp-image-7222" title="Monitor Different Systems with Zabbix" /></a>

it then tried to auto create a configuration file under **/etc/zabbix** but it failed:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file.png" alt="zabbix web front install config file Monitor Different Systems with Zabbix" width="796" height="505" class="alignnone size-full wp-image-7221" title="Monitor Different Systems with Zabbix" /></a>

So I downloaded it manually and copied the file to the appropriate location:

    kerch:~>sudo cp zabbix.conf.php /etc/zabbix/.
    

Then hitting "Retry" I saw the following page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file_pass.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file_pass.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_install_config_file_pass.png" alt="zabbix web front install config file pass Monitor Different Systems with Zabbix" width="796" height="513" class="alignnone size-full wp-image-7223" title="Monitor Different Systems with Zabbix" /></a>

Hitting "Next" yielded the following page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_login_page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_login_page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_login_page.png" alt="zabbix web front login page Monitor Different Systems with Zabbix" width="631" height="289" class="alignnone size-full wp-image-7224" title="Monitor Different Systems with Zabbix" /></a>

You can login with Username: **Admin**, Password: **zabbix**. After you login, you can create another user; instruction on user setup and default password are <a href="https://www.zabbix.com/documentation/2.0/manual/quickstart/login" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/documentation/2.0/manual/quickstart/login']);">here</a>. After I logged in, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_dashboard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_dashboard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_front_dashboard.png" alt="zabbix web front dashboard Monitor Different Systems with Zabbix" width="813" height="576" class="alignnone size-full wp-image-7225" title="Monitor Different Systems with Zabbix" /></a>

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
    

That looks good. Now let's add the host to be monitored with Zabbix via the PHP frontend. Most of the instructions are laid out <a href="https://www.zabbix.com/documentation/2.0/manual/config/hosts/host" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/documentation/2.0/manual/config/hosts/host']);">here</a>. So in the Zabbix Dashboard go to "Configuration" -> "Hosts" and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_conf-hosts.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_conf-hosts.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_conf-hosts.png" alt="zabbix web conf hosts Monitor Different Systems with Zabbix" width="1225" height="330" class="alignnone size-full wp-image-7240" title="Monitor Different Systems with Zabbix" /></a>

Then click on "Create Host" and fill out all the information, mine looked like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host.png" alt="zabbix web create host Monitor Different Systems with Zabbix" width="1181" height="524" class="alignnone size-full wp-image-7241" title="Monitor Different Systems with Zabbix" /></a>

Under the template section choose "Template OS Linux":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host_add_template.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host_add_template.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_create_host_add_template.png" alt="zabbix web create host add template Monitor Different Systems with Zabbix" width="562" height="154" class="alignnone size-full wp-image-7242" title="Monitor Different Systems with Zabbix" /></a>

Then click "Save" and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_host_added.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_host_added.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_host_added.png" alt="zabbix web host added Monitor Different Systems with Zabbix" width="1225" height="213" class="alignnone size-full wp-image-7243" title="Monitor Different Systems with Zabbix" /></a>

At first I checked out a graph but the font was missing for some reason, I found a fix on the Zabbix forums from <a href="https://www.zabbix.com/forum/showthread.php?p=91923" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/forum/showthread.php?p=91923']);">here</a>. After I pointed to the appropriate path for the fonts, I was able to see the graphs like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_graph_cpu_usage.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_graph_cpu_usage.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_web_graph_cpu_usage.png" alt="zabbix web graph cpu usage Monitor Different Systems with Zabbix" width="1205" height="473" class="alignnone size-full wp-image-7244" title="Monitor Different Systems with Zabbix" /></a>

Also going to "Monitoring" -> "Overview" you can see current values for our hosts:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_monitoring_overview.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_monitoring_overview.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_monitoring_overview.png" alt="zabbix monitoring overview Monitor Different Systems with Zabbix" width="1249" height="541" class="alignnone size-full wp-image-7245" title="Monitor Different Systems with Zabbix" /></a>

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_freebsd_host.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_freebsd_host.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_freebsd_host.png" alt="zabbix add freebsd host Monitor Different Systems with Zabbix" width="1224" height="536" class="alignnone size-full wp-image-7246" title="Monitor Different Systems with Zabbix" /></a>

And under templates choose, "Template OS FreeBSD":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_os_template.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_os_template.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_os_template.png" alt="zabbix freebsd os template Monitor Different Systems with Zabbix" width="447" height="143" class="alignnone size-full wp-image-7247" title="Monitor Different Systems with Zabbix" /></a>

After a little bit of time you should see the host as monitored with a green **Z** under "Configuration" -> "Hosts":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_green_z.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_green_z.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_green_z.png" alt="zabbix freebsd green z Monitor Different Systems with Zabbix" width="1259" height="265" class="alignnone size-full wp-image-7248" title="Monitor Different Systems with Zabbix" /></a>

If you want to check what items will be monitored, you can go to "Configuration" -> "Host" -> Pick a Host -> "Items" and you will see a list of all the checks:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_monitored_items.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_monitored_items.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_freebsd_monitored_items.png" alt="zabbix freebsd monitored items Monitor Different Systems with Zabbix" width="1247" height="508" class="alignnone size-full wp-image-7249" title="Monitor Different Systems with Zabbix" /></a>

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_all_three_greenZ.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_all_three_greenZ.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_all_three_greenZ.png" alt="zabbix all three greenZ Monitor Different Systems with Zabbix" width="1263" height="298" class="alignnone size-full wp-image-7253" title="Monitor Different Systems with Zabbix" /></a>

## Monitor raid status on FreeBSD with Zabbix

There are good examples in <a href="https://www.zabbix.com/wiki/howto/monitor/os/linux/smart" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/wiki/howto/monitor/os/linux/smart']);">this</a> Zabbix page and also from <a href="http://lab4.org/wiki/Zabbix_adaptec_raidcontroller_ueberwachen" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://lab4.org/wiki/Zabbix_adaptec_raidcontroller_ueberwachen']);">this</a> post. We will have to use "User Parameters" to get this working. The first link from above describes the process pretty well. I will define two parameters

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_raid_online_drives_item.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_raid_online_drives_item.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_raid_online_drives_item.png" alt="zabbix add raid online drives item Monitor Different Systems with Zabbix" width="836" height="534" class="alignnone size-full wp-image-7254" title="Monitor Different Systems with Zabbix" /></a>

When finished, click "Save". Then from the same window click on "Graphs" -> "Create Graph" and fill out the information:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_raid_disks.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_raid_disks.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_raid_disks.png" alt="zabbix graph raid disks Monitor Different Systems with Zabbix" width="1244" height="546" class="alignnone size-full wp-image-7255" title="Monitor Different Systems with Zabbix" /></a>

Then checking out the graph (by going to "Monitoring" -> "Graphs" -> "Host" -> "FreeBSD" -> "Graph" -> "Raid_#_Disks_Online"), here is what I saw:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_disks_online.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_disks_online.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_graph_disks_online.png" alt="zabbix graph disks online Monitor Different Systems with Zabbix" width="1241" height="371" class="alignnone size-full wp-image-7256" title="Monitor Different Systems with Zabbix" /></a>

Now let's setup a new item for the controller status. Go to "Configuration" -> "Hosts" -> Select host -> "Items" -> "Create New Item" and fill out all the information:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_item_raid_cont_status.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_item_raid_cont_status.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_item_raid_cont_status.png" alt="zabbix item raid cont status Monitor Different Systems with Zabbix" width="938" height="503" class="alignnone size-full wp-image-7257" title="Monitor Different Systems with Zabbix" /></a>

Then from the same page, click on "Triggers" -> "Create Trigger". In the new window select "Add" under Trigger Expressions and make the follow expression:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_expression.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_expression.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_expression.png" alt="zabbix trigger expression Monitor Different Systems with Zabbix" width="583" height="206" class="alignnone size-full wp-image-7258" title="Monitor Different Systems with Zabbix" /></a>

then click "Save". Your final result will look like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_trigger.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_trigger.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_add_trigger.png" alt="zabbix add trigger Monitor Different Systems with Zabbix" width="785" height="426" class="alignnone size-full wp-image-7259" title="Monitor Different Systems with Zabbix" /></a>

You can go to "Monitoring" -> "Latest Data" and then expand the Name when you groupped your item, in my case I put it under OS. Expanding OS, I saw the latest value of that item:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_latest_data_controller_status.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_latest_data_controller_status.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_latest_data_controller_status.png" alt="zabbix latest data controller status Monitor Different Systems with Zabbix" width="1245" height="513" class="alignnone size-full wp-image-7260" title="Monitor Different Systems with Zabbix" /></a>

Also forcing a non-zero return value from that script yeilded the trigger to be fired. Here is what I saw under "Monitoring" -> "Triggers":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_fired.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_fired.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_trigger_fired.png" alt="zabbix trigger fired Monitor Different Systems with Zabbix" width="1259" height="273" class="alignnone size-full wp-image-7261" title="Monitor Different Systems with Zabbix" /></a>

and then fixing the script to return the correct value, allowed the trigger to be fixed. Here is what I saw under "Monitoring" -> "Events" after the issue was fixed:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_events_after_issue_fixed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_events_after_issue_fixed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_events_after_issue_fixed.png" alt="zabbix events after issue fixed Monitor Different Systems with Zabbix" width="1261" height="327" class="alignnone size-full wp-image-7262" title="Monitor Different Systems with Zabbix" /></a>

## Zabbix Vs. Zenoss, Munin, and Collectd

### PROs

*   Lightweight compared to Zenoss and for all the functionality that it provides
*   Doesn't Depend on Python or Perl
*   Supports MySQL, PSQL, and SQlite
*   Very easy to customize Triggers and Graphs
*   Has the capability to monitor with agents and without
*   Has great support for most OSes, even FreeBSD
*   Works like an Intrusion Detection System (IDS). I installed a new software and it automatically added a new user, I then saw the following under events: <a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_password_changed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_password_changed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/zabbix_password_changed.png" alt="zabbix password changed Monitor Different Systems with Zabbix" width="1252" height="328" class="alignnone size-full wp-image-7325" title="Monitor Different Systems with Zabbix" /></a>

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
      <a title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" href="http://virtuallyhyper.com/2013/12/configure-ipmi-supermicro-server-monitor-ipmi-sensors-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/12/configure-ipmi-supermicro-server-monitor-ipmi-sensors-zabbix/']);" rel="bookmark">Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor SMART Attributes with Zabbix" href="http://virtuallyhyper.com/2013/10/monitor-smart-attributes-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/10/monitor-smart-attributes-zabbix/']);" rel="bookmark">Monitor SMART Attributes with Zabbix</a>
    </li>
  </ul>
</div>

