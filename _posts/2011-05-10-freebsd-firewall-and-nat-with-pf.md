---
published: true
title: FreeBSD Firewall and NAT with PF
author: Karim Elatov
layout: post
categories: [os, networking]
tags: [freebsd, pf, nat]
---
**PF** (Packet Filter) is a BSD licensed stateful packet filter, a central piece of software for firewalling. It is comparable to **iptables**, **ipfw** and **ipfilter**.

Let's say you have the following physical setup:

![NAT](https://dl.dropboxusercontent.com/u/24136116/blog_pics/pf_nat/NAT.jpg)

And you want to use FreeBSD as your firewall and NAT'ing device, here is a small guide on how to set that up.

On your freebsd machine add the following into your **/etc/rc.conf** file:


	defaultrouter="100.138.196.1"  
	gateway_enable="YES"  
	hostname="thewall.domain.com"  
	ifconfig_xl0="inet 192.138.196.100 netmask 255.255.255.0"  
	ifconfig_bge0="inet 100.168.196.100 netmask 255.255.255.0"  
	ifconfig_xl0_alias0="inet 100.138.196.2 netmask 255.255.255.0"  
	ifconfig_xl0_alias1="inet 100.138.196.3 netmask 255.255.255.0"  
	ifconfig_xl0_alias2="inet 100.138.196.4 netmask 255.255.255.0"  
	pf_enable="YES"  
	pf_flags=""  
	pf_program="/sbin/pfctl"  
	pf_rules="/etc/pf.conf"  
	pflog_enable="YES"  
	pflog_flags=""  
	pflog_logfile="/var/log/pflog"  
	pflog_program="/sbin/pflogd"  
  
Reboot the host and check to make sure **pf** is running:

	ps aux | grep pf

then create the **/etc/pf.conf** file and place the following into the file:

	##### lists/macros/tables##  
	# macros  
	# hosts  
	thewall_public = "100.138.196.100/32"  
	thewall_private = "192.168.196.100/32"  
	distrib_host = "100.138.2.253/32"  
	host1_private = "192.168.196.2/32"  
	host2_public = "100.138.196.3/32"  
	host2_private = "192.168.196.3/32"  
	host3_public="100.138.196.196.4/32"  
	host3_private="192.138.196.4/32"  
	outside_network = "100.138.0.0/16"  
	the_world = "0.0.0.0/0"

	# interfaces  
	public_interface = "xl0"  
	private_interface = "bge0"

	# networks  
	private_network = "192.168.196.0/24"  
	public_network = "100.138.196.0/24"  
	outside_128_network = "100.138.128.0/24"  
	outside_110_network = "100.138.110.0/24"

	#tables  
	# monitoring hosts  
	table {  
	100.138.1.2/32  
	100.138.1.3/32  
	100.138.1.4/32 }

	# domain name servers  
	table {  
	100.138.2.2/32  
	100.138.2.3/32  
	100.138.2.4/32  
	100.138.2.5/32 }

	# ip addresses assigned to nics  
	table { self }

	## options##  
	set skip on lo0  
	set state-policy if-bound  
	set timeout { interval 1 }

	## normalization##  
	scrub in all fragment reassemble

	## static nat addresses. these all have a 1:1 relationship between  
	# public and private addresses and do not use port translation.  
	# host1  
	binat on $public_interface from 192.168.196.2/32 to any -> 100.138.196.2/32

	# host2  
	binat on $public_interface from 192.168.196.3/32 to any -> 100.138.196.3/32

	# host3  
	binat on $public_interface from 192.168.196.4/32 to any -> 100.138.196.4/32

	# all other private addresses use regular nat, which means traffic  
	# that exits the public interface appears to come from freebsd machine and  
	# is subject to port translation.

	nat on $public_interface from $private_network to any -> $thewall_public

	# hack! redirect systems trying to talk to host2:smtp from the  
	# private network to host3:smtp.

	rdr on { $private_interface $public_interface }  proto tcp from $private_network to $host2_public port smtp -> $host2_public port smtp

	rdr on $private_interface proto tcp from $private_network to $public_interface port smtp -> $host2_public  
	no nat on $private_interface proto tcp from $private_interface to $private_network

	nat on $private_interface proto tcp from $private_network to $host2_public port smtp -> $private_interface  
	nat on $private_interface from $private_network to $private_network -> $private_interface

	### filtering##

	#default deny  
	#block and log traffic entering all interfaces  
	block return in log all

	# pass traffic exiting all interfaces  
	pass out all keep state

	# traffic exiting public interface should use modulate state  
	pass out on $public_interface all keep state

	### traffic entering private interface (leaving private network) ###

	# allow all traffic from private hosts out  
	pass in quick on $private_interface proto { icmp tcp udp } from { $private_network $public_network } to any modulate state

	# broadcast traffic  
	pass in on $private_interface from $private_network to $private_network keep state  
	pass in on $private_interface from $private_network to $private_interface:broadcast keep state

	# alow smtp from host2 to anywhere  
	pass in quick on $private_interface proto tcp from $host2_private to any port smtp modulate state

	# allow traffic to smtp  
	pass in on $private_interface inet proto tcp from $private_network to $host2_private port smtp synproxy state flags S/SA

	#allow broadcasts  
	pass in quick on $private_interface proto { tcp, udp } from $private_interface:network  to $private_interface:broadcast keep state  
	pass in quick on $private_interface from any to 100.138.196.127

	#### traffic entering public interface (private network)#####

	#allow ports 22,25,80,443,993,995 globally on host2  
	pass in quick on { $public_interface $private_interface } proto tcp from any to $host2_private port {22 smtp 80 443 993 995} keep state

	# allow all traffic from on outside_network to host2_private  
	pass in quick on $public_interface proto { tcp udp icmp } from $outside_network to $host2_private keep state

	# allow icmp echo from monitoring_hosts to thewall and private network #  
	pass in quick on $public_interface proto icmp from { } to { $private_network } keep state

	# allow icmp echo from anywhere  
	pass in quick on $public_interface proto icmp from any to { $private_network } keep state

	# allow ssh from distrib host, public network and Nagios hosts to firewall  
	pass in quick on $public_interface proto tcp from { $distrib_host $public_network } to port ssh keep state

	# allow ssh from outside_network wide hosts to private network  
	pass in quick on $public_interface proto tcp from $outside_network to $private_network port ssh keep state

	# allow http from public_subnet and distrib host to private network  
	pass in quick on $public_interface proto tcp from { $outside_network } to $private_network port http keep state

	# allow https from public_subnet and distrib host to private network  
	pass in quick on $public_interface proto tcp from { $outside_network } to $private_network port https keep state

	# allow IMAPS from public_subnet and distrib host to private network  
	pass in quick on $public_interface proto tcp from { $outside_network } to $private_network port 993 keep state

	# allow 995 from public_subnet and distrib host to private network  
	pass in quick on $public_interface proto tcp from { $outside_network } to $private_network port 995 keep state

	# allow smtp from public_subnet and distrib host to private network  
	pass in quick on $public_interface proto tcp from { $outside_network } to $private_network port smtp keep state

	# allow port 902 from public_subnet to private host host1  
	pass in quick on $public_interface proto tcp from $public_network to $host1_private port 902 keep state

	# allow port 443 from public_subnet to private host host1  
	pass in quick on $public_interface proto tcp from $public_network to $host1_private port 443 keep state

	### Allow NFS mouting from privating network  
	# allow sunrpc TCP and UDP port from public_subnet to private nework  
	pass in quick on $public_interface proto { tcp udp } from { $public_network $outside_128_network $outside_110_network } to $private_network port sunrpc keep state

	# allow 755 UDP port from public_subnet to private nework  
	pass in quick on $public_interface proto udp from $public_network to $private_network port 755 keep state

	# allow nfsd TCP and UDP port from public_subnet to private nework  
	pass in quick on $public_interface proto { tcp udp } from { $public_network $outside_128_network $outside_110_network } to $private_network port nfsd keep state

	# allow uuidgen port from public_subnet to private nework  
	pass in quick on $public_interface proto tcp from $public_network to $private_network port uuidgen keep state

	# allow lanserver port from public_subnet to private nework  
	pass in quick on $public_interface proto tcp from $public_network to $private_network port lanserver keep state

	# allow entrust-aaas port from public_subnet to private nework  
	pass in quick on $public_interface proto tcp from $public_network to $private_network port entrust-aaas keep state

	# allow xmpp-client port from public_subnet to private nework  
	pass in quick on $public_interface proto tcp from $public_network to $private_network port xmpp-client keep state

	# allow rsh from distrib host to firewall and private network  
	pass in quick on $public_interface proto tcp from $distrib_host to { $private_network } port shell keep state (tcp.closed 1)

	# allow nrpe from monitoring hosts to firewall and private network  
	pass in quick on $public_interface proto tcp from to { $private_network } port nrpe keep state

	# allow broadcast icmp from public_subnet to private nework and public IPs  
	pass in quick on $public_interface proto { tcp udp icmp } from $public_network to any keep state

	# garbage to ignore (do not log; silently discard traffic)  
	# ignore dhcp requests, ipp, microsoft broadcasts, rip  
	block return in quick proto tcp from any to any port auth block drop in quick proto udp from any to any port { bootps dantz ipp netbios-dgm netbios-ns ntp router 2222 9960 }  

After you have that all setup, you can use the following commands to test out your setup:  

- Parse Rules

		pfctl -nf /etc/pf.conf

- Load rules

		pfctl -f /etc/pf.conf

- Watch the logs for blocked packets

		tcpdump -n -e -ttt -i pflog0

The RHEL hosts behind the NAT should have the the following under **/etc/hosts**


	192.168.196.2 host1.domain.com host1  
	192.168.196.3 host2.domain.com host2  
	192.168.196.4 host3.domain.com host3  

and the following under **/etc/sysconfig/network**


	NETWORKING=yes  
	NETWORKING_IPV6=no  
	HOSTNAME=host#.domain.com  
	GATEWAY=192.168.196.100  

and of course set it's IPs as the private ip. 

I have also done a similar setup with **iptables**, and I will post my example on that next.
