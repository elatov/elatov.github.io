---
title: Simple FreeBSD PF firewall
author: Karim Elatov
layout: post
categories: [OS,networking]
tags: [pf,freebsd]
---

I wanted to have a very simple example of how to setup **pf** on your freebsd machine and here it it. 

First enable **pf** by adding the following to **/etc/rc.conf** and rebooting you BSD host to take affect:

	pf_enable="YES"  
	pf_rules="/etc/pf.conf"  
	pflog_enable="YES"  
	pflog_logfile="/var/log/pf.log"  

when the machine is back up and running make sure **pf** is loaded:

	moxz:~>kldstat | grep pf  
	2 1 0xffffffff81022000 a3c pflog.ko  
	3 1 0xffffffff81023000 2bd41 pf.ko  

next create the file **/etc/pf.conf** and place the following into it:

	#Macros  
	my_int = "em0"

	# Let's just trust localhost  
	set skip on lo

	# By default, we will block everyone and everything coming in  
	block in log all

	# accept ssh sessions  
	pass in on $my_int proto tcp from any to any port 22 keep state

	# accept http sessions  
	pass in on $my_int proto tcp from any to any port 80 keep state

	# accept icmp sessions  
	pass in quick on $my_int proto icmp all keep state

	# Outgoing traffic is OK, here we keep state so returning packets  
	# are accepted too.  
	pass out log proto { tcp, udp, icmp } all keep state  

you can test out your settings by running the following commands:

- Parse Rules  

		pfctl -nf /etc/pf.conf

- Load rules  

		pfctl -f /etc/pf.conf

- Watch the logs for blocked packets  

		tcpdump -n -e -ttt -i pflog0
