---
title: Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL
author: Karim Elatov
layout: post
permalink: /2013/06/install-splunk-and-send-logs-to-splunk-with-rsyslog-over-tcp-with-ssl/
dsq_thread_id:
  - 1405505941
categories:
  - Home Lab
  - VMware
tags:
  - Rsyslog
  - Splunk
  - SSL
---
## Splunk

There are a couple of components of Splunk. From <a href="http://docs.splunk.com/Documentation/Splunk/latest/Installation/ComponentsofaSplunkdeployment" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.splunk.com/Documentation/Splunk/latest/Installation/ComponentsofaSplunkdeployment']);">Components of a Splunk deployment</a>:

> **Indexer**  
> Splunk indexers, or index servers, provide indexing capability for local and remote data and host the primary Splunk datastore, as well as Splunk Web. Refer to "How indexing works" in the Managing Indexers and Clusters manual for more information.
> 
> **Search peer**  
> A search peer is an indexer that services requests from search heads in a distributed search deployment. Search peers are also sometimes referred to as indexer nodes.
> 
> **Search head**  
> A search head is a Splunk instance configured to distribute searches to indexers, or search peers. Search heads can be either dedicated or not, depending on whether they also perform indexing. Dedicated search heads don't have any indexes of their own (other than the usual internal indexes). Instead, they consolidate results that originate from remote search peers.
> 
> **Forwarder**  
> Forwarders are Splunk instances that forward data to remote indexers for indexing and storage. In most cases, they do not index data themselves. Refer to the "About forwarding and receiving" topic in the Distributed Deployment manual.
> 
> **Deployment server**  
> Both indexers and forwarders can also act as deployment servers. A deployment server distributes configuration information to running instances of Splunk via a push mechanism which is enabled through configuration. Refer to "About deployment server" in the Distributed Deployment Manual for additional information about the deployment server.

I will just setup our server as an *indexer* which we can search. From the same document:

> The simplest deployment is the one you get by default when you install Splunk: indexing and searching on the same server. Data comes in from the sources you've configured, and you log into Splunk Web or the CLI on this same server to search, monitor, alert, and report on your IT data.

Here is good table of the functions:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/functions.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/functions.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/functions.png" alt="functions Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="499" height="207" class="alignnone size-full wp-image-8976" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

Also here are the processes that splunk starts up, from Splunk architecture and processes:

> **Processes**  
> A Splunk server runs two processes (installed as services on Windows systems) on your host, **splunkd** and **splunkweb**:
> 
> *   **splunkd** is a distributed C/C++ server that accesses, processes and indexes streaming IT data. It also handles search requests. **splunkd** processes and indexes your data by streaming it through a series of pipelines, each made up of a series of processors.
>     
>     *   Pipelines are single threads inside the splunkd process, each configured with a single snippet of XML.
>     *   Processors are individual, reusable C or C++ functions that act on the stream of IT data passing through a pipeline. Pipelines can pass data to one another via queues. splunkd supports a command line interface for searching and viewing results.
> 
> *   **splunkweb** is a Python-based application server based on CherryPy that provides the Splunk Web user interface. It allows users to search and navigate data stored by Splunk servers and to manage your Splunk deployment through a Web interface.
> 
> **splunkweb** and **splunkd** can both communicate with your Web browser via Representational state transfer (REST):
> 
> *   **splunkd** also runs a Web server on port 8089 with SSL/HTTPS turned on by default.
> *   **splunkweb** runs a Web server on port 8000 without SSL/HTTPS by default.

Lastly, here is a pretty good picture of all the components:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/arch_diag.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/arch_diag.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/arch_diag.png" alt="arch diag Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="623" height="334" class="alignnone size-full wp-image-8983" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

### Splunk Free

Here are some differences between the free and enterprise versions of splunk. From <a href="http://docs.splunk.com/Documentation/Splunk/5.0.3/Admin/MoreaboutSplunkFree" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.splunk.com/Documentation/Splunk/5.0.3/Admin/MoreaboutSplunkFree']);">More about Splunk Free</a>:

> Splunk Free is a totally free (as in beer) version of Splunk. It allows you to index up to 500 MB/day and will never expire. This 500 MB limit refers to the amount of new data you can add (we call this indexing) per day, but you can keep adding more and more data every day, storing as much as you want. For example, you could add 500 MB of data per day and eventually have 10 TB of data in Splunk. If you need more than 500 MB/day, you'll need to purchase a license.

From the same document here are the functions that are not available:

> **What is included**  
> Splunk Free is a single-user product. All of Splunk's features are supported with the exception of:
> 
> *   Multiple user accounts and role-based access controls (there's no authentication when using Splunk Free) 
> *   Distributed search 
> *   Forwarding in TCP/HTTP formats (you can forward data to other Splunk instances, but not to non-Splunk instances) 
> *   Deployment management 
> *   Alerting/monitoring 
> 
> A Free instance can be used as a forwarder (to a Splunk indexer) but may not be a client of a deployment server.

So we are just limited to processing/indexing 500MB of logs. For a local setup at home, this is more than enough.

## Install Splunk

The install is pretty straight forward. Just download the RPM from <a href="http://www.splunk.com/download" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.splunk.com/download']);">here</a>. We will want the Linux 64 bit version:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_download.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_download.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_download.png" alt="splunk download Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="987" height="380" class="alignnone size-full wp-image-8985" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

BTW here is the OS that I am using:

    [root@splunk ~]# lsb_release -a
    LSB Version:    :base-4.0-amd64:base-4.0-noarch:core-4.0-amd64:core-4.0-noarch
    Distributor ID: CentOS
    Description:    CentOS release 6.4 (Final)
    Release:    6.4
    Codename:   Final
    
    [root@splunk ~]# uname -a
    Linux splunk.elatov.local 2.6.32-358.6.2.el6.x86_64 #1 SMP Thu May 16 20:59:36 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
    

Here is how the install looked like:

    [root@splunk ~]# rpm -Uvh splunk-5.0.3-163460-linux-2.6-x86_64.rpm 
    warning: splunk-5.0.3-163460-linux-2.6-x86_64.rpm: Header V3 DSA/SHA1 Signature, key ID 653fb112: NOKEY
    Preparing...                ########################################### [100%]
       1:splunk                 ########################################### [100%]
    -------------------------------------------------------------------------
    Splunk has been installed in:
            /opt/splunk
    
    To start Splunk, run the command:
            /opt/splunk/bin/splunk start
    
    
    To use the Splunk Web interface, point your browser to:
    
    http://splunk.elatov.local:8000
    
    Complete documentation is at http://docs.splunk.com/Documentation/Splunk
    -------------------------------------------------------------------------
    

### Start Splunk and Make Sure it's Running

During the start-up process you have to accept the license agreement:

    [root@splunk ~]# /opt/splunk/bin/splunk start
    Splunk rev. 8. 7. 2012
    Do you agree with this license? [y/n]: y
    
    This appears to be your first time running this version of Splunk.
    Copying '/opt/splunk/etc/openldap/ldap.conf.default' to '/opt/splunk/etc/openldap/ldap.conf'.
    Generating RSA private key, 1024 bit long modulus
    ...............++++++
    ..............................++++++
    e is 65537 (0x10001)
    writing RSA key
    
    Generating RSA private key, 1024 bit long modulus
    .....++++++
    .............++++++
    e is 65537 (0x10001)
    writing RSA key
    
    Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
    
    Splunk> 4TW
    
    Checking prerequisites...
        Checking http port [8000]: open
        Checking mgmt port [8089]: open
        Checking configuration...  Done.
        Checking indexes...
            Creating: /opt/splunk/var/lib/splunk
            Creating: /opt/splunk/var/run/splunk
            Creating: /opt/splunk/var/run/splunk/appserver/i18n
            Creating: /opt/splunk/var/run/splunk/appserver/modules/static/css
            Creating: /opt/splunk/var/run/splunk/upload
            Creating: /opt/splunk/var/spool/splunk
            Creating: /opt/splunk/var/spool/dirmoncache
            Creating: /opt/splunk/var/lib/splunk/authDb
            Creating: /opt/splunk/var/lib/splunk/hashDb
            Validated databases: _audit _blocksignature _internal _thefishbucket history main summary
        Done
    New certs have been generated in '/opt/splunk/etc/auth'.
        Checking filesystem compatibility...  Done
        Checking conf files for typos...    Done
    All preliminary checks passed.
    
    Starting splunk server daemon (splunkd)...  Done
                                                               [  OK  ]
    Starting splunkweb...  Generating certs for splunkweb server
    Generating a 1024 bit RSA private key
    .................++++++
    ........++++++
    writing new private key to 'privKeySecure.pem'
    -----
    Signature ok
    subject=/CN=splunk.elatov.local/O=SplunkUser
    Getting CA Private Key
    writing RSA key
                                                               [  OK  ]
    Done
    
    If you get stuck, we're here to help.  
    Look for answers here: http://docs.splunk.com
    
    The Splunk web interface is at http://splunk.elatov.local:8000
    

Splunk is supposed to be running on port **8000** and **8089**, so let's make sure that is case:

    [root@splunk ~]# netstat -antp | grep -E '8000|8089'
    tcp        0      0 0.0.0.0:8089                0.0.0.0:*                   LISTEN      1356/splunkd        
    tcp        0      0 0.0.0.0:8000                0.0.0.0:*                   LISTEN      1414/python   
    

Let's open up the firewall for those ports. Edit **/etc/sysconfig/iptables** and add the following to the file:

    -A INPUT -m state --state NEW -m tcp -p tcp --dport 8000 -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 8089 -j ACCEPT
    

then restart the **iptables** services:

    [root@splunk ~]# service iptables restart
    iptables: Flushing firewall rules:                         [  OK  ]
    iptables: Setting chains to policy ACCEPT: filter          [  OK  ]
    iptables: Unloading modules:                               [  OK  ]
    iptables: Applying firewall rules:                         [  OK  ]
    

Lastly, confirm the **iptables** rules are in place:

    [root@splunk ~]# iptables -L -n | grep -E '8000|8089'
    ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:8000 
    ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:8089 
    

Finally point your browser to the splunk server: **http://IP:8000**, here is how it will look:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_first_login.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_first_login.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_first_login.png" alt="splunk first login Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="789" height="520" class="alignnone size-full wp-image-8986" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

After you login, you will be asked to change your password:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_change_passwd.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_change_passwd.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_change_passwd.png" alt="splunk change passwd Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="770" height="423" class="alignnone size-full wp-image-8987" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

After that is done, you will see the *SplunkWeb* portal:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logged_in.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logged_in.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logged_in.png" alt="splunk logged in Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="970" height="386" class="alignnone size-full wp-image-8988" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

### Add Remote Syslog Data Type

From the Home screen, click "Add Data":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_add_data.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_add_data.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_add_data.png" alt="splunk add data Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="835" height="521" class="alignnone size-full wp-image-8989" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

Then Click "Syslog":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/add_syslog_data.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/add_syslog_data.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/add_syslog_data.png" alt="add syslog data Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="862" height="654" class="alignnone size-full wp-image-8990" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

Click "Next" under the **Consume syslog over TCP section**. And then put the port you want to use and select the source to be "syslog":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/syslog_tcp_remote.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/syslog_tcp_remote.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/syslog_tcp_remote.png" alt="syslog tcp remote Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="905" height="717" class="alignnone size-full wp-image-8991" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

After you click "Save", you should see the following success page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/success-add-syslog_tcp.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/success-add-syslog_tcp.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/success-add-syslog_tcp.png" alt="success add syslog tcp Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="860" height="366" class="alignnone size-full wp-image-8992" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

At this point if you go back to the splunk server, you will see it listening on port **514**:

    [root@splunk ~]# netstat -antp | grep 514
    tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN      1356/splunkd   
    

You can also query the splunk server directly to make sure it's collecting over TCP:

    [root@splunk ~]# /opt/splunk/bin/splunk list tcp
    Splunk username: admin
    Password: 
    Splunk is listening for data on ports:
        514 for data from any host
    

Lastly let's open up port **514** on the splunk server. Edit **/etc/sysconfig/iptables** and add the following:

    -A INPUT -m state --state NEW -m tcp -p tcp --dport 514 -j ACCEPT
    

and restart the firewall service:

    [root@splunk ~]# service iptables restart
    iptables: Flushing firewall rules:                         [  OK  ]
    iptables: Setting chains to policy ACCEPT: filter          [  OK  ]
    iptables: Unloading modules:                               [  OK  ]
    iptables: Applying firewall rules:                         [  OK  ]
    

## Configure Rsyslog to Send Logs to Splunk Server

I will use my laptop for the test, my laptop is running Fedora:

    [elatov@klaptop ~]$ lsb_release -a
    LSB Version:    :core-4.1-ia32:core-4.1-noarch:cxx-4.1-ia32:cxx-4.1-noarch:desktop-4.1-ia32:desktop-4.1-noarch:languages-4.1-ia32:languages-4.1-noarch:printing-4.1-ia32:printing-4.1-noarch
    Distributor ID: Fedora
    Description:    Fedora release 18 (Spherical Cow)
    Release:    18
    Codename:   SphericalCow
    
    [elatov@klaptop ~]$ uname -a
    Linux klaptop.elatov.local 3.9.4-200.fc18.i686.PAE #1 SMP Fri May 24 20:24:58 UTC 2013 i686 i686 i386 GNU/Linux
    

To send the logs, edit **/etc/rsyslog.conf** and add the following line:

    *.* @@192.168.56.101:514
    

Then restart the **rsyslog** service:

    [elatov@klaptop ~]$ sudo service rsyslog restart
    Redirecting to /bin/systemctl restart  rsyslog.service
    

And of course make sure it's back up and running:

    [elatov@klaptop ~]$ sudo service rsyslog status
    Redirecting to /bin/systemctl status  rsyslog.service
    rsyslog.service - System Logging Service
       Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled)
       Active: active (running) since Sat 2013-06-08 16:26:23 MDT; 2s ago
     Main PID: 7720 (rsyslogd)
       CGroup: name=systemd:/system/rsyslog.service
               └─7720 /sbin/rsyslogd -n
    
    Jun 08 16:26:23 klaptop.elatov.local systemd[1]: Starting System Logging Se...
    Jun 08 16:26:23 klaptop.elatov.local systemd[1]: Started System Logging Ser...
    

### Confirm the Logs are Getting Indexed

From the home page click on "Launch search app":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/launch_search_app.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/launch_search_app.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/launch_search_app.png" alt="launch search app Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="570" height="211" class="alignnone size-full wp-image-8993" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/logs_getting_to_splunk_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/logs_getting_to_splunk_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/logs_getting_to_splunk_g.png" alt="logs getting to splunk g Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="1039" height="560" class="alignnone size-full wp-image-9010" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

If you click on one of the hosts from the bottom left pane, you should see something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/host_logs_splunk.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/host_logs_splunk.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/host_logs_splunk.png" alt="host logs splunk Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="1030" height="551" class="alignnone size-full wp-image-8995" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

## Enable Splunk to Receive Syslog over TCP with SSL

From <a href="http://docs.splunk.com/Documentation/Splunk/5.0.3/Data/Monitornetworkports" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.splunk.com/Documentation/Splunk/5.0.3/Data/Monitornetworkports']);">Get data from TCP and UDP ports</a>:

> **TCP over SSL**  
> [tcp-ssl:port]  
> Use this stanza type if you are receiving encrypted, unparsed data from a forwarder or third-party system. Set PORT to the port on which the forwarder or third-party system is sending unparsed, encrypted data.

We have to edit the **inputs.conf** file and add our stanza in:

> Add a network input using inputs.conf  
> To add an input, add a stanza for it to inputs.conf in $SPLUNK_HOME/etc/system/local/

So let's edit our configuration file:

    [root@splunk ~]# vi /opt/splunk/etc/system/local/inputs.conf
    

And add the following :

    [tcp-ssl:515]
    sourcetype = syslog
    
    [SSL]
    password = 
    requireClientCert = false
    rootCA = /opt/splunk/certs/root-ca-elatov-local.pem
    serverCert = /opt/splunk/certs/elatov-local-wild-key-cert.pem
    

The certificates were generated using the instructions laid out <a href="http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment']);">here</a>. I had to concatenate my password less private key and certificate into one file:

    [root@splunk certs]# cat elatov-local-wild.pem elatov-local-wild-priv-pw.pem > elatov-local-wild-key-cert.pem
    

I then copied both files under the defined folder from the settings:

    [root@splunk ~]# ls -1 /opt/splunk/certs/
    elatov-local-wild-key-cert.pem
    root-ca-elatov-local.pem
    

To apply the above settings, let's restart the splunk instance:

    [root@splunk ~]# /opt/splunk/bin/splunk restart
    Stopping splunkweb...
                                                               [  OK  ]
    Stopping splunkd...
    Shutting down.  Please wait, as this may take a few minutes.
    .                                                          [  OK  ]
    Stopping splunk helpers...
                                                               [  OK  ]
    Done.
    
    Splunk> 4TW
    
    Checking prerequisites...
        Checking http port [8000]: open
        Checking mgmt port [8089]: open
        Checking configuration...  Done.
        Checking indexes...
            Validated databases: _audit _blocksignature _internal _thefishbucket history main summary
        Done
        Checking filesystem compatibility...  Done
        Checking conf files for typos...    Done
    All preliminary checks passed.
    
    Starting splunk server daemon (splunkd)...  Done
                                                               [  OK  ]
                                                               [  OK  ]
    Starting splunkweb...  Done
    
    If you get stuck, we're here to help.  
    Look for answers here: http://docs.splunk.com
    
    The Splunk web interface is at http://splunk.elatov.local:8000
    

Let's make sure all the ports are bound and listening:

    [root@splunk ~]# netstat -antp | grep -E '8000|8089|514|515'
    tcp        0      0 0.0.0.0:8089                0.0.0.0:*                   LISTEN      5688/splunkd        
    tcp        0      0 0.0.0.0:8000                0.0.0.0:*                   LISTEN      5758/python         
    tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN      5688/splunkd        
    tcp        0      0 0.0.0.0:515                 0.0.0.0:*                   LISTEN      5688/splunkd  
    

Let's make sure splunk shows both ports as well:

    [root@splunk ~]# /opt/splunk/bin/splunk list tcp
    Splunk is listening for data on ports:
        514 for data from any host
        515 for data from any host
    

Lastly let's open up the port for TCP over SSL:

    [root@splunk ~]# iptables -L -n | grep 515
    ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:515 
    

### Enable Rsyslog to Send over TCP with SSL

First let's copy the root CA Certificate onto the system:

    [root@klaptop ~]# ls -1 /etc/pki/CA/certs/
    root-ca-elatov-local.pem
    

Then edit **/etc/rsyslog.conf** and add the following:

    # certificate CA file for a client
    $DefaultNetstreamDriverCAFile /etc/pki/CA/certs/root-ca-elatov-local.pem
    
    # set up the action
    $DefaultNetstreamDriver gtls # use gtls netstream driver
    $ActionSendStreamDriverMode 1 # require TLS for the connection
    $ActionSendStreamDriverAuthMode anon # server is NOT authenticated
    *.* @@192.168.56.101:515
    

Then restart the **rsyslog** service:

    [elatov@klaptop ~]$ sudo service rsyslog restart 
    Redirecting to /bin/systemctl restart rsyslog.service
    

If you see the following under **/var/log/messages**:

    Jun  8 17:00:09 klaptop systemd[1]: Stopping System Logging Service...
    Jun  8 17:00:09 klaptop systemd[1]: Starting System Logging Service...
    Jun  8 17:00:09 klaptop systemd[1]: Started System Logging Service.
    Jun  8 17:00:09 klaptop rsyslogd-2066: could not load module '/lib/rsyslog/lmnsd
    _gtls.so', dlopen: /lib/rsyslog/lmnsd_gtls.so: cannot open shared object file: N
    o such file or directory
    

Then we need to install the **rsyslog-gnutls** package:

    [elatov@klaptop ~]$ yum provides "*/lmnsd_gtls.so"
    Loaded plugins: langpacks, presto, refresh-packagekit
    rpmfusion-nonfree-updates/filelists_db                   | 175 kB     00:00     
    updates/filelists_db                                     |  13 MB     00:07     
    rsyslog-gnutls-7.2.4-1.fc18.i686 : TLS protocol support for rsyslog
    Repo        : fedora
    Matched from:
    Filename    : /lib/rsyslog/lmnsd_gtls.so
    

here is the actual install:

    [elatov@klaptop ~]$ sudo yum install rsyslog-gnutls
    ...
    ...
    Installed:
      rsyslog-gnutls.i686 0:7.2.6-1.fc18                                            
    
    Complete!
    

After it's installed, restart the **rsyslog** service one more time:

    [elatov@klaptop ~]$ sudo service rsyslog restart
    Redirecting to /bin/systemctl restart  rsyslog.service
    

and make sure you only see the following in the logs:

    Jun  8 17:05:22 klaptop systemd[1]: Stopping System Logging Service...
    Jun  8 17:05:22 klaptop systemd[1]: Starting System Logging Service...
    Jun  8 17:05:22 klaptop systemd[1]: Started System Logging Service.
    

and nothing else.

## Confirm SSL Data is getting Indexed

Login to SplunkWeb (**http://IP:8000**) and click on "Launch search app" and you should now see logs coming in on both "Sources":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logs_both_sources.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logs_both_sources.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/splunk_logs_both_sources.png" alt="splunk logs both sources Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" width="678" height="392" class="alignnone size-full wp-image-8997" title="Install Splunk and Send Logs to Splunk with Rsyslog over TCP with SSL" /></a>

### Encypted Data vs Non-Encrypted Data

Here is how **tcpdump** looks like without SSL:

    [root@splunk ~]# tcpdump -i eth3 tcp port 514 -X -s 0 -nn
    17:13:36.986560 IP 192.168.56.1.42147 > 192.168.56.101.514: Flags [P.], seq 1:360, ack 1, win 115, options [nop,nop,TS val 9803614 ecr 5967246], length 359
        0x0000:  4500 019b 2435 4000 4006 2371 c0a8 3801  E...$5@.@.#q..8.
        0x0010:  c0a8 3865 a4a3 0202 cbc7 b36f bb85 9872  ..8e.......o...r
        0x0020:  8018 0073 a233 0000 0101 080a 0095 975e  ...s.3.........^
        0x0030:  005b 0d8e 3c34 363e 4a75 6e20 2038 2031  .[..<46>Jun..8.1
        0x0040:  373a 3133 3a33 3620 6b6c 6170 746f 7020  7:13:36.klaptop.
        0x0050:  7273 7973 6c6f 6764 3a20 5b6f 7269 6769  rsyslogd:.[origi
        0x0060:  6e20 736f 6674 7761 7265 3d22 7273 7973  n.software="rsys
        0x0070:  6c6f 6764 2220 7377 5665 7273 696f 6e3d  logd".swVersion=
        0x0080:  2237 2e32 2e36 2220 782d 7069 643d 2231  "7.2.6".x-pid="1
        0x0090:  3134 3933 2220 782d 696e 666f 3d22 6874  1493".x-info="ht
        0x00a0:  7470 3a2f 2f77 7777 2e72 7379 736c 6f67  tp://www.rsyslog
        0x00b0:  2e63 6f6d 225d 2073 7461 7274 0a3c 3330  .com"].start.<30
        0x00c0:  3e4a 756e 2020 3820 3137 3a31 333a 3336  >Jun..8.17:13:36
        0x00d0:  206b 6c61 7074 6f70 2073 7973 7465 6d64  .klaptop.systemd
        0x00e0:  5b31 5d3a 2053 746f 7070 696e 6720 5379  [1]:.Stopping.Sy
        0x00f0:  7374 656d 204c 6f67 6769 6e67 2053 6572  stem.Logging.Ser
        0x0100:  7669 6365 2e2e 2e0a 3c33 303e 4a75 6e20  vice....<30>Jun.
        0x0110:  2038 2031 373a 3133 3a33 3620 6b6c 6170  .8.17:13:36.klap
        0x0120:  746f 7020 7379 7374 656d 645b 315d 3a20  top.systemd[1]:.
        0x0130:  5374 6172 7469 6e67 2053 7973 7465 6d20  Starting.System.
        0x0140:  4c6f 6767 696e 6720 5365 7276 6963 652e  Logging.Service.
        0x0150:  2e2e 0a3c 3330 3e4a 756e 2020 3820 3137  ...<30>Jun..8.17
        0x0160:  3a31 333a 3336 206b 6c61 7074 6f70 2073  :13:36.klaptop.s
        0x0170:  7973 7465 6d64 5b31 5d3a 2053 7461 7274  ystemd[1]:.Start
        0x0180:  6564 2053 7973 7465 6d20 4c6f 6767 696e  ed.System.Loggin
        0x0190:  6720 5365 7276 6963 652e 0a              g.Service..
    

And here is how it looks like with SSL enabled:

    [root@splunk ~]# tcpdump -i eth3 tcp port 515 -X -s 0 -nn
    17:10:39.387765 IP 192.168.56.1.54492 > 192.168.56.101.515: Flags [P.], seq 4709:4938, ack 1, win 160, options [nop,nop,TS val 9626015 ecr 5789647], length 229
        0x0000:  4500 0119 948a 4000 4006 b39d c0a8 3801  E.....@.@.....8.
        0x0010:  c0a8 3865 d4dc 0203 ec59 e04b 9ac6 0ad1  ..8e.....Y.K....
        0x0020:  8018 00a0 4d53 0000 0101 080a 0092 e19f  ....MS..........
        0x0030:  0058 57cf 1703 0100 e07a a3e7 8c4f e18c  .XW......z...O..
        0x0040:  765c f5cc 4bbb ce2e 1258 7dfc 68fd ec12  v\..K....X}.h...
        0x0050:  87f1 a68d 2e85 3f7f 9798 ae97 720c 27c4  ......?.....r.'.
        0x0060:  2398 ddc0 cc4d fe3f a0a8 2700 4707 74b5  #....M.?..'.G.t.
        0x0070:  f8af 5bc6 6381 3d61 96ac 550f 7ee0 aa96  ..[.c.=a..U.~...
        0x0080:  2541 8644 6734 b236 30ef fda3 38dc 6065  %A.Dg4.60...8.`e
        0x0090:  63ea d6b7 c51f 8005 5435 942a 1041 9910  c.......T5.*.A..
        0x00a0:  e8cb 9995 44ae e110 1d78 484f 88a2 a828  ....D....xHO...(
        0x00b0:  b684 2ed4 e621 8d92 e1af 45a9 eef5 cc0e  .....!....E.....
        0x00c0:  05f7 8a07 ac6b 60fc 7b0a 174e 09c3 ebc2  .....k`.{..N....
        0x00d0:  76d5 f273 6156 d759 5370 32fa 45b7 992e  v..saV.YSp2.E...
        0x00e0:  fe3e 148c ea01 2e29 0ff4 742a 2e0a 4c37  .>.....)..t*..L7
        0x00f0:  a8ce 3e0f cc1c 0b55 7b3b b0a4 ea52 a695  ..>....U{;...R..
        0x0100:  4bed 25eb a869 41b0 bbe5 e452 1773 e61b  K.%..iA....R.s..
        0x0110:  d363 bd6d 1f16 849b 4f                   .c.m....O
    

