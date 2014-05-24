---
title: OSSEC on FreeBSD
author: Karim Elatov
layout: post
permalink: /2014/04/ossec-freebsd/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2598880222
categories:
  - Home Lab
  - OS
tags:
  - freebsd
  - OSSEC
  - Splunk
---
After trying out Samhain and Beltane (check out the [previous](/2014/03/install-samhain-beltane-freebsd) post on that setup), I decided to try out another HIDS. This time around I went with OSSEC.

### OSSEC

From their [home](http://www.ossec.net/) page, here is a quick summary of the software:

> OSSEC is an Open Source Host-based Intrusion Detection System that performs log analysis, file integrity checking, policy monitoring, rootkit detection, real-time alerting and active response.

From their [How It Works](http://www.ossec.net/?page_id=169) page, they describe the Server/Client approach. Here is a diagram from that page:

![ossec architecture OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-architecture.png)

#### Install OSSEC Server on FreeBSD

Let's go ahead with the centralized server approach. I checked out ports and I did find a port for OSSEC:

    moxz:~>cd /usr/ports
    moxz:/usr/ports>make search name=ossec
    Port:   ossec-hids-client-2.7
    Path:   /usr/ports/security/ossec-hids-client
    Info:   The client port of ossec-hids
    Maint:  ports@FreeBSD.org
    B-deps:
    R-deps:
    WWW:    http://www.ossec.net/

    Port:   ossec-hids-local-2.7
    Path:   /usr/ports/security/ossec-hids-local
    Info:   The client and server (local) port of ossec-hids
    Maint:  ports@FreeBSD.org
    B-deps:
    R-deps:
    WWW:    http://www.ossec.net/

    Port:   ossec-hids-server-2.7
    Path:   /usr/ports/security/ossec-hids-server
    Info:   A security tool to monitor and check logs and intrusions
    Maint:  ports@FreeBSD.org
    B-deps:
    R-deps:
    WWW:    http://www.ossec.net/


The port actually needs **gcc** to compile the software. I already had *gcc47* installed from the [Samhain](/2014/03/install-samhain-beltane-freebsd) install, so I was all ready. To install the software, I ran the following:

    moxz:~>cd /usr/ports/security/ossec-hids-server/
    moxz:/usr/ports/security/ossec-hids-server>sudo make install


After the install was finished, I saw the following:

    ===>  Installing for ossec-hids-server-2.7
    ===>   Generating temporary packing list
    ===>  Checking if security/ossec-hids-server already installed
    ===> Creating users and/or groups.
    Creating group `ossec' with gid `966'.
    Creating user `ossec' with uid `966'.
    Creating user `ossecm' with uid `967'.
    Creating user `ossecr' with uid `968'.
    ===> Staging rc.d startup script(s)
    After installation, you need to edit the ossec.conf file to reflect
    the correct settings for your environment.  All the files related
    to ossec-hids have been installed in /usr/local/ossec-hids and
    its subdirectories.

    For information on proper configuration, see http://www.ossec.net/.

    To enable the startup script, add ossechids_enable="YES" to
    /etc/rc.conf.  To enable database output, execute:

    /usr/local/ossec-hids/bin/ossec-control enable database

    Then check this documentation:

    http://www.ossec.net/doc/manual/output/database-output.html



Let's go ahead and enable the service:

    moxz:~>tail -1 /etc/rc.conf
    ossechids_enable="YES"


Now let's configure the server the configuration. I modified the file to contain the following:

      <global>
        <email_notification>yes</email_notification>
        <email_to>elatov@moxz.local.com</email_to>
        <smtp_server>127.0.0.1</smtp_server>
        <email_from>ossecm@local.com</email_from>
      </global>

     <rootcheck>
        <rootkit_files>/usr/local/ossec-hids/etc/shared/rootkit_files.txt</rootkit_files>
        <rootkit_trojans>/usr/local/ossec-hids/etc/shared/rootkit_trojans.txt</rootkit_trojans>
      </rootcheck>


I also cleaned up the **localfile** section and removed any log files that didn't exist on the system. I ended up just having the following:

    <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/auth.log</location>
      </localfile>

      <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/xferlog</location>
      </localfile>

      <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/maillog</location>
      </localfile>


Then I just started the service:

    moxz:~>sudo service ossec-hids start
    Starting OSSEC HIDS v2.7 (by Trend Micro Inc.)...
    Started ossec-maild...
    Started ossec-execd...
    Started ossec-analysisd...
    Started ossec-logcollector...
    Started ossec-remoted...
    Started ossec-syscheckd...
    Started ossec-monitord...
    Completed.


Lastly let's open up UDP 1514 on the host. This is the port the OSSEC server is listening on. I was running **pf** on the FreeBSD 10 machine. So I added the following to my **/etc/pf.conf** file:

    # accept osssec agent sessions
    pass in on $my_int proto udp from $priv_net to any port 1514 keep state


I then ran the following to apply the new **pf** settings:

    moxz:~>sudo pfctl -f /etc/pf.conf
    No ALTQ support in kernel
    ALTQ related functions disabled


#### Install OSSEC Agent on Fedora

The [Downloads](http://www.ossec.net/?page_id=19) page has instructions on how to add the **atomic** repository (which contains pre-compiled OSSEC packages). Run the following to add the repository:

    elatov@fed:~$wget -q -O - https://www.atomicorp.com/installers/atomic | sudo sh
    All atomic repository rpms are UNSUPPORTED.
    Do you agree to these terms? (yes/no) [Default: yes] yes

    Configuring the [atomic] yum archive for this system

    Installing the Atomic GPG key: OK
    Downloading atomic-release-1.0-18.fc20.art.noarch.rpm: OK



    The Atomic Rocket Turtle archive has now been installed and configured for your system
    The following channels are available:
      atomic          - [ACTIVATED] - contains the stable tree of ART packages
      atomic-testing  - [DISABLED]  - contains the testing tree of ART packages
      atomic-bleeding - [DISABLED]  - contains the development tree of ART packages


After the install is finished you should see the YUM repository added:

    elatov@fed:~$ls -l /etc/yum.repos.d/atomic.repo
    -rw-r--r-- 1 root root 763 Mar 22 18:36 /etc/yum.repos.d/atomic.repo


That repository also had a **zabbix** package, which I already had installed from the *updates* repository:

    elatov@fed:~$yum list installed | grep zabbix
    zabbix.x86_64                          2.0.10-2.fc20                    @updates
    zabbix-agent.x86_64                    2.0.10-2.fc20                    @updates


Instead of overriding those packages, I just **excluded** the *zabbix* packages from the **atomic** repository. This is done by adding the following to the **/etc/yum.repos.d/atomic.repo** file (under the **atomic** section):

    exclude = zabbix*


Then running the following installed the client:

    elatov@fed:~$ sudo yum install ossec-hids-client


If you don't want to install the repository, you can manually install the RPMs:

    elatov@fed:~$ wget http://www3.atomicorp.com/channels/atomic/fedora/19/x86_64/RPMS/ossec-hids-2.7.1-36.fc19.art.x86_64.rpm
    elatov@fed:~$ wget http://www3.atomicorp.com/channels/atomic/fedora/19/x86_64/RPMS/ossec-hids-client-2.7.1-36.fc19.art.x86_64.rpm
    elatov@fed:~$ sudo yum localinstall ossec-hids-2.7.1-36.fc19.art.x86_64.rpm ossec-hids-client-2.7.1-36.fc19.art.x86_64.rpm


Now let's configure the agent. I modified the **/var/ossec/etc/ossec.conf** file to have the following:

    <client>
        <server-ip>10.0.0.3</server-ip>
      </client>


And I also cleaned up which log files to monitor:

    <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/messages</location>
      </localfile>

      <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/secure</location>
      </localfile>

      <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/maillog</location>
      </localfile>


Now let's add the agent to the server and get his key:

    moxz:~> sudo /usr/local/ossec-hids/bin/manage_agents

    ****************************************
    * OSSEC HIDS v2.7 Agent manager.     *
    * The following options are available: *
    ****************************************
       (A)dd an agent (A).
       (E)xtract key for an agent (E).
       (L)ist already added agents (L).
       (R)emove an agent (R).
       (Q)uit.
    Choose your action: A,E,L,R or Q: a <----

    - Adding a new agent (use '\q' to return to the main menu).
      Please provide the following:
       * A name for the new agent: fed <----
       * The IP Address of the new agent: 10.0.0.4 <----
       * An ID for the new agent[001]:
    Agent information:
       ID:001
       Name:fed
       IP Address:10.0.0.4

    Confirm adding it?(y/n): y   <----
    Agent added.


    ****************************************
    * OSSEC HIDS v2.7 Agent manager.     *
    * The following options are available: *
    ****************************************
       (A)dd an agent (A).
       (E)xtract key for an agent (E).
       (L)ist already added agents (L).
       (R)emove an agent (R).
       (Q)uit.
    Choose your action: A,E,L,R or Q: E <----

    Available agents:
       ID: 001, Name: fed, IP: 10.0.0.4
    Provide the ID of the agent to extract the key (or '\q' to quit): 001 <---

    Agent key information for '001' is:
    MDAxIG1veHotbCAxMC4wLjAuNCAzNTc1MjUxZGU1NDI5NTJlZjlkZTNiNWRhMjhiMWQ4NTA5ZmQ5MDEzNDdhMTI5ODExZjA1NTE0OTMzODAzZjc4

    ** Press ENTER to return to the main menu.

    ****************************************
    * OSSEC HIDS v2.7 Agent manager.     *
    * The following options are available: *
    ****************************************
       (A)dd an agent (A).
       (E)xtract key for an agent (E).
       (L)ist already added agents (L).
       (R)emove an agent (R).
       (Q)uit.
    Choose your action: A,E,L,R or Q: q   <---

    ** You must restart OSSEC for your changes to take effect.

    manage_agents: Exiting ..


To apply the above settings let's restart the OSSEC Server:

    moxz:~> sudo service ossec-hids restart
    Killing ossec-monitord ..
    Killing ossec-logcollector ..
    ossec-remoted not running ..
    Killing ossec-syscheckd ..
    Killing ossec-analysisd ..
    Killing ossec-maild ..
    Killing ossec-execd ..
    OSSEC HIDS v2.7 Stopped
    Starting OSSEC HIDS v2.7 (by Trend Micro Inc.)...
    Started ossec-maild...
    Started ossec-execd...
    Started ossec-analysisd...
    Started ossec-logcollector...
    Started ossec-remoted...
    Started ossec-syscheckd...
    Started ossec-monitord...
    Completed.


Now on the client side, let's add the key:

    elatov@fed:~$ sudo /var/ossec/bin/manage_client

    ****************************************
    * OSSEC HIDS v2.7.1 Agent manager.     *
    * The following options are available: *
    ****************************************
       (I)mport key from the server (I).
       (Q)uit.
    Choose your action: I or Q: I <---

    * Provide the Key generated by the server.
    * The best approach is to cut and paste it.
    *** OBS: Do not include spaces or new lines.

    Paste it here (or '\q' to quit): MDAxIG1veHotbCAxMC4wLjAuNCAzNTc1MjUxZGU1NDI5NTJlZjlkZTNiNWRhMjhiMWQ4NTA5ZmQ5MDEzNDdhMTI5ODExZjA1NTE0OTMzODAzZjc4  <---

    Agent information:
       ID:001
       Name:fed
       IP Address:10.0.0.4

    Confirm adding it?(y/n): y <---
    Added.
    ** Press ENTER to return to the main menu.

    ****************************************
    * OSSEC HIDS v2.7.1 Agent manager.     *
    * The following options are available: *
    ****************************************
       (I)mport key from the server (I).
       (Q)uit.
    Choose your action: I or Q: q <---

    ** You must restart OSSEC for your changes to take effect.

    manage_agents: Exiting ..


Now enable the service:

    elatov@fed:~$sudo systemctl enable ossec-hids.service
    ossec-hids.service is not a native service, redirecting to /sbin/chkconfig.
    Executing /sbin/chkconfig ossec-hids on


and then start the service:

    elatov@fed:~$ sudo systemctl start ossec-hids.service


Then check out the client log to make sure it connected to the server without issues:

    elatov@fed:~$tail /var/ossec/logs/ossec.log
    2014/03/22 18:55:11 ossec-execd: INFO: Started (pid: 756).
    2014/03/22 18:55:11 ossec-agentd(1410): INFO: Reading authentication keys file.
    2014/03/22 18:55:11 ossec-agentd: INFO: No previous counter available for 'fed'.
    2014/03/22 18:55:11 ossec-agentd: INFO: Assigning counter for agent fed: '0:0'.
    2014/03/22 18:55:11 ossec-agentd: INFO: Assigning sender counter: 0:332
    2014/03/22 18:55:11 ossec-agentd: INFO: Started (pid: 765).
    2014/03/22 18:55:11 ossec-agentd: INFO: Server IP Address: 10.0.0.3
    2014/03/22 18:55:11 ossec-agentd: INFO: Trying to connect to server (10.0.0.3:1514).
    2014/03/22 18:55:11 ossec-agentd: INFO: Using IPv4 for: 10.0.0.3 .


On the server side you should see an *alert* similar to this:

    moxz:~>tail /usr/local/ossec-hids/logs/alerts/alerts.log
    ** Alert 1395535871.8825: mail  - ossec,
    2014 Mar 22 18:51:11 (fed) 10.0.0.4 ->ossec
    Rule: 501 (level 3) -> 'New ossec agent connected.'
    ossec: Agent started: 'fed->10.0.0.4'.


### Install Web-UI For OSSEC

Most of the instructions are [here](http://www.ossec.net/wiki/index.php/OSSECWUI:Install). First get the web-ui package:

    moxz:/opt/work>fetch http://www.ossec.net/files/ossec-wui-0.8.tar.gz
    ossec-wui-0.8.tar.gz                          100% of  158 kB  497 kBps 00m00s


I already had an apache/php server running (I setup it up for the [beltane/samhain](/2014/03/install-samhain-beltane-freebsd) configuration), so I just copied the file to the document root:

    moxz:/opt/work>sudo mv ossec-wui-0.8 /usr/local/www/apache22/data/os


Then added the **www** user to the **ossec** group:

    moxz:~> sudo pw group mod ossec -m www


Then fixed all the necessary permissions:

    moxz:~>sudo chmod 770 /usr/local/ossec-hids/tmp
    moxz:~>sudo chown ossec:www /usr/local/ossec-hids/tmp


And lastly update the web-ui to point to the ossec install:

    moxz:~>grep '^\$ossec_dir' /usr/local/www/apache22/data/os/ossec_conf.php
    $ossec_dir="/usr/local/ossec-hids";


Then restart apache:

    moxz:~>sudo service apache22 restart
    Password:
    Performing sanity check on apache22 configuration:
    Syntax OK
    Stopping apache22.
    Waiting for PIDS: 7523.
    Performing sanity check on apache22 configuration:
    Syntax OK
    Starting apache22.


Now if you visit **http://<OSSEC_SERVER/>/os**, you should see something like this:

![ossec web ui OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-web-ui.png)

It will have all the alerts on that page. You can also check out any files that have changed recently:

![ossec web ui integrity OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-web-ui-integrity.png)

#### Install OSSEC App for Splunk

I was already running **splunk** on my FreeBSD host (check out the instruction on that setup from [here](/2013/12/installing-splunk-freebsd/), extract it and move it to the *splunk* install:

    moxz:~> tar xvzf reporting-and-management-for-ossec_1189.tgz
    moxz:~> sudo mv ossec/ /opt/splunk/etc/apps/.


Change the permissions over to the **splunk** user:

    moxz:~> sudo chown -R splunk:splunk /opt/splunk/etc/apps/ossec


Let's update the **inputs** section to point to the correct log files:

    moxz:~> sudo vi /opt/splunk/etc/apps/ossec/default/inputs.conf


and modify the following:

    [monitor:///usr/local/ossec-hids/logs/alerts/alerts*]
    disabled = 0
    sourcetype = ossec_alerts

    [monitor:///usr/local/ossec-hids/logs/ossec.log]
    disabled = 0
    sourcetype = ossec_log

    [monitor:///usr/local/ossec-hids/logs/active-responses.log]
    disabled = 0
    sourcetype = ossec_ar


Also let's point the app to the correct location of the rules for ossec. Modify the **/opt/splunk/etc/apps/ossec/bin/parse_ossec_groups.py** file to contain the following:

    DEFAULT_RULES_DIR = "/usr/local/ossec-hids/rules/"


At this point go ahead and the **splunk** service:

    moxz:~> sudo service splunk restart


If you visit your splunk instance, you will see the OSSEC app:

![select splunk for ossec OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/select-splunk-for-ossec.png)

Upon the selecting the *OSSEC* App and selecting the dashboard you will see the following:

![ossec app splunk plots OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-app-splunk-plots.png)

You can also see any files that have been changed from here:

![ossec splunk file changes g OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-splunk-file-changes_g.png)

If you want to see agent status, you will have to do some additional configurations. First configure the **agent_control** command:

    moxz:~>grep ^AGENT_CONTROL /opt/splunk/etc/apps/ossec/default/ossec_servers.conf -B 1
    [_local]
    AGENT_CONTROL = /usr/local/bin/sudo /usr/local/ossec-hids/bin/agent_control -l


Then allow the **splunk** user to run that command without the need to enter a password. To accomplish that, add the following file (with the following contents):

    moxz:~>cat /usr/local/etc/sudoers.d/ossec-splunk
    Defaults:splunk !requiretty
    splunk  ALL=(ALL) NOPASSWD: /usr/local/ossec-hids/bin/agent_control -l


Do a quick test and make sure you can run that:

    moxz:~>sudo su - splunk -c '/usr/local/bin/sudo /usr/local/ossec-hids/bin/agent_control -l'

    OSSEC HIDS agent_control. List of available agents:
       ID: 000, Name: moxz.dnsd.me (server), IP: 127.0.0.1, Active/Local
       ID: 002, Name: fed, IP: 10.0.0.3, Active

    List of agentless devices:


Initially I kept seeing the following errors:

![out pty devices ossec splunk OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/out-pty-devices-ossec-splunk.png)

After looking into the issue, I realized I was missing the **/dev/ptmx** file. I ran into [this](http://forums.freebsd.org/viewtopic.php?t=43673) FreeBSD forum which recommended to load the following kernel module:

    moxz:~>sudo kldload pty


After that, I got another error: "**[Errno 6] Device not configured**". The issue ended up being with the version of python that splunk provides (**/opt/splunk/bin/python**) and the **pexect** python module. To get around the issue, I created a wrapper script which used the system python. Here is the script:

    moxz:~>cat /opt/splunk/etc/apps/ossec/bin/cmd.sh
    #!/bin/sh
    /usr/local/bin/python /opt/splunk/etc/apps/ossec/bin/ossec_agent_status.py


Then I modified the **inputs.conf** to use that script instead of the default one:

    moxz:~>tail -6 /opt/splunk/etc/apps/ossec/default/inputs.conf
    [script://./bin/cmd.sh ]
    disabled = 0
    source = ossec_agent_control
    sourcetype = ossec_agent_control
    interval = 300


Then restarting the splunk service:

    moxz:~> sudo service splunk restart


and checking out the logs in splunk, I saw the following:

![active clients ossec splunk OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/active-clients-ossec-splunk.png)

That looked good. Checking out the Agent status dashboard and I saw the following:

![ossec agent status OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-agent-status.png)

Then going to the Agent Coverage dashboard, I saw the following:

![agent coverage ossec splunk OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/agent-coverage-ossec-splunk.png)

There were a bunch of new reports created which provided a bunch of cool information:

![ossec splunk reports1 OSSEC on FreeBSD](https://github.com/elatov/uploads/raw/master/2014/03/ossec-splunk-reports1.png)

Last thing to note is that by default OSSEC installs a couple of active response script. If you are using PF as a firewall, you will need to a new table to make it work. For more information check out [this](http://taosecurity.blogspot.com/2008/12/ossec-and-pf-on-freebsd-to-limit-ssh.html) post.

