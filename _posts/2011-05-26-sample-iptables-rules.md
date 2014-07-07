---
title: Sample IPtables rules
author: Karim Elatov
layout: post
categories: [os, networking]
tags: [linux, iptables]
published: true

---
**IPtables** is a firewall program that comes with Linux distributions which allows applications and clients to connect through the network and stop unwanted applications and clients from communicating to the operating system.

Here is a small example of a simple **iptables** configuration.


	# Firewall configuration written by redhat-config-securitylevel  
	*filter  
	:INPUT ACCEPT [0:0]  
	:FORWARD ACCEPT [0:0]  
	:OUTPUT ACCEPT [0:0]  
	:RH-Firewall-1-INPUT - [0:0]  
	# Uncomment for logging  
	## :LOG-AND-REJECT - [0:0]  
	-A INPUT -j RH-Firewall-1-INPUT  
	-A FORWARD -j RH-Firewall-1-INPUT  
	-A RH-Firewall-1-INPUT -i lo -j ACCEPT  
	# Uncomment for logging  
	##-A LOG-AND-REJECT -j LOG --log-tcp-options --log-ip-options --log-level debug --log-prefix "mymachine_firewall : "  
	##-A LOG-AND-REJECT -j REJECT --reject-with icmp-host-prohibited  
	#  
	# Allow return packets from established outbound connections  
	-A RH-Firewall-1-INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  
	#  
	# Permit ssh  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT  
	#  
	# Permit ping  
	-A RH-Firewall-1-INPUT -p icmp --icmp-type echo-reply -j ACCEPT  
	-A RH-Firewall-1-INPUT -p icmp --icmp-type echo-request -j ACCEPT  
	#  
	# Open up holes for tripwire to the tripwire servers  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.10.15/32 --dport 9898 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.10.15/32 --dport 8080 --syn -j ACCEPT  
	#  
	# Permit SMTP connections from anywhere  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 100.138.10.11/32 --dport 25 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 100.138.10.11/32 --dport 587 --syn -j ACCEPT  
	#  
	# Permit HTTP and HTTPS connections from anywhere  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 0/0 --dport 80 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 0/0 --dport 443 --syn -j ACCEPT  
	#  
	# Permit POP3S connections from anywhere  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 100.138.10.15/32 --dport 995 --syn -j ACCEPT  
	#  
	# Permit IMAPS connections from anywhere  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 100.138.10.15/32 --dport 993 --syn -j ACCEPT  
	#  
	# Permit SAMBA shares to the 100.138.0.0/16 network  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.0.0/16 -d 100.138.10.15/32 --dport 137 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp -s 100.138.0.0/16 -d 100.138.10.15/32 --dport 138 -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.0.0/16 -d 100.138.10.15/32 --dport 139 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.0.0/16 -d 100.138.10.15/32 --dport 445 --syn -j ACCEPT  
	#  
	# Permit ftp (plus ports for passive xfers) from anywhere  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 0/0 --dport 21 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 0/0 -d 0/0 --dport 50000:51000 --syn -j ACCEPT  
	#  
	# Permit MySQL connections  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.10.16/32 -d 0/0 --dport 3306 --syn -j ACCEPT  
	#  
	# Permit access to the Dell OMSA port from 100.138.16.x for management  
	-A RH-Firewall-1-INPUT -i eth0 -p tcp -m tcp -s 100.138.16.0/24 -d 0/0 --dport 1311 --syn -j ACCEPT  
	#  
	# Permit access to the Internet Printing Protocol (IPP) to share printers on a server  
	-A RH-Firewall-1-INPUT -i eth0 -p tcp -m tcp -s 100.138.0.0/16 -d 0/0 --dport 631 --syn -j ACCEPT  
	#  
	# Allow X11 connections  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.0.0/16 --dport 6000:6009 --syn -j ACCEPT  
	#  
	# Allow the 100.138.16.0/24 subnet to mount nfs  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.16.0/24 --dport 2049 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp -s 100.138.16.0/24 --dport 2049 -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.16.0/24 --dport 111 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp -s 100.138.16.0/24 --dport 111 -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.16.0/24 --dport 32765:32768 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp -s 100.138.16.0/24 --dport 32765:32768 -j ACCEPT  
	#  
	# Allow clients on same subnet full access  
	-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 100.138.16.0/24 -d 0/0 --syn -j ACCEPT  
	-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp -s 100.138.16.0/24 -d 0/0 -j ACCEPT  
	# Deny rest  
	-A RH-Firewall-1-INPUT -j REJECT --reject-with icmp-host-prohibited  
	COMMIT  
