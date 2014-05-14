---
title: Installing and Configuring Fail2Ban on OmniOS
author: Jarret Lavallee
layout: post
permalink: /2013/04/installing-and-configuring-fail2ban-on-omnios/
dsq_thread_id:
  - 1405432749
categories:
  - Home Lab
  - Networking
  - OS
tags:
  - fail2ban
  - OmniOS
---
<a href="http://www.fail2ban.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.fail2ban.org']);">Fail2Ban</a> is a program that will trigger actions based on patterns found in logs. I am setting up fail2ban to stop ssh brute forcing on my external ssh port. With the configuration below a user that fails to log in 5 times within 10 minutes will have all traffic to and from their IP blocked for 24 hours.

Fail2ban has been built in this <a href="http://pkg.cs.umd.edu/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pkg.cs.umd.edu/']);">repo</a>, so let&#8217;s add it.

    root@megatron:~# pkg set-publisher -g http://pkg.cs.umd.edu/ cs.umd.edu
    

The repo that we enabled above has fail2ban already built, so we can just install it with **pkg**.

    jarret@megatron:~$ sudo pkg install fail2ban
    

Let&#8217;s edit the default configuration file to whitelist the local subnets and define a new rule. The new rule, called *sshd-ipfilter* will search the *authlog* for any failed logins and then block the rule with ipfilter. Edit the */ets/fail2ban/jail.conf* file and add the following lines.

    ignoreip = 127.0.0.1 192.168.5.0/24 10.0.1.0/24
    ...
    [sshd-ipfilter]
    enabled  = true
    filter   = sshd
    action   = ipfilter
    logpath  = /var/log/authlog
    maxretry = 5
    bantime  = 84600
    findtime = 600
    

We need to change the path in the *ipfilter.conf* so that it points to the correct **ipf** binary. The command below will update the file with the new path.

    jarret@megatron:~$ sudo sed -i 's/\/sbin\/ipf/\/usr\/sbin\/ipf/' /etc/fail2ban/action.d/ipfilter.conf
    

The default configuration for *syslog* does not log the *auth.info* to the authlog. Luckily *sshd* logs to *auth.info* by default, so we can change the */etc/syslog.conf* and add the following line.

    auth.info                                     /var/log/authlog
    

After making the change to the *syslog.conf* file, we need to restart the *system-log* service.

    jarret@megatron:/etc/fail2ban/action.d$ sudo svcadm restart system-log
    

The problem with the fail2ban **pkg** install is that it does not come with an SMF service. So we would either have to start it manually or write up a script to put in */etc/init.d*. I went searching and found that someone else has already written the necessary files for SMF for fail2ban.

Let&#8217;s get the XML file.

    jarret@megatron:/tmp$ wget https://github.com/fail2ban/fail2ban/raw/master/files/solaris-fail2ban.xml
    

There is one thing I want to change in the XML file. It has dependencies listed, but **ipfilter** is not one of them. Edit the **solaris-fail2ban.xml** file and add the following lines under the other dependencies. **Note:** if you want to change the user that fail2ban runs as, you can do that in this file.

    <dependency name='net'
            grouping='require_all'
            restart_on='none'
            type='service'>
            <service_fmri value='svc:/network/ipfilter'></service_fmri>
    </dependency>
    

Let&#8217;s go a head and import the XML file.

    jarret@megatron:/tmp$ sudo svccfg import solaris-fail2ban.xml
    

Now the second part of the service is the *methods* script. Let&#8217;s download that as well.

    jarret@megatron:/tmp$ wget https://raw.github.com/fail2ban/fail2ban/master/files/solaris-svc-fail2ban
    

The script has different paths in it for the fail2ban binaries. We need to update it to look in */usr/bin*.

    jarret@megatron:/tmp$ sed -i 's/\/usr\/local\/bin\/fail2ban/\/usr\/bin\/fail2ban/g' solaris-svc-fail2ban
    

Now we can put it into place and change the permissions on it.

    jarret@megatron:/tmp$ sudo cp solaris-svc-fail2ban /lib/svc/method/svc-fail2ban
    jarret@megatron:/tmp$ sudo chown root:root /lib/svc/method/svc-fail2ban
    jarret@megatron:/tmp$ sudo chmod 755 /lib/svc/method/svc-fail2ban
    

Let&#8217;s check the service definition and make sure that our dependencies list is there.

    jarret@megatron:/tmp$ svcs -d fail2ban
    STATE          STIME    FMRI
    disabled       22:50:44 svc:/network/ipfilter:default
    online         22:50:46 svc:/network/loopback:default
    online         22:51:47 svc:/system/filesystem/local:default
    

It all looks good, so we can start the services.

    jarret@megatron:/tmp$ sudo svcadm enable ipfilter
    jarret@megatron:/tmp$ sudo svcadm enable fail2ban
    

I went ahead and made some invalid log in attempts to verify that the IPs would get blocked. Here is the line that is in the */var/log/fail2ban.log* when it banned the IP.

    2013-03-18 14:56:28,188 fail2ban.actions: WARNING [sshd-ipfilter] Ban 69.85.89.211
    

Below are the rules that fail2ban put in place for banning the IP.

    jarret@megatron:/var/log$ sudo ipfstat -io
    ...
    block in quick from 69.85.89.232/32 to any
    

Everything works as we expected.

