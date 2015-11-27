---
published: false
layout: post
title: "Use WOL to Power On Dell Laptop"
author: Karim Elatov
categories: [os,networking]
tags: [wol,linux]
---

Luckily this laptop had this option available. So I enabled that:


Then after I powered it on, I confirmed it's enabled on the NIC:

elatov@gen ~ $ sudo ethtool enp0s25
Settings for enp0s25:
	Supported ports: [ TP ]
	Supported link modes:   10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Supported pause frame use: No
	Supports auto-negotiation: Yes
	Advertised link modes:  10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Advertised pause frame use: No
	Advertised auto-negotiation: Yes
	Speed: 1000Mb/s
	Duplex: Full
	Port: Twisted Pair
	PHYAD: 2
	Transceiver: internal
	Auto-negotiation: on
	MDI-X: off (auto)
	Supports Wake-on: pumbg
	Wake-on: g
	Current message level: 0x00000007 (7)
			       drv probe link
	Link detected: yes

Then I figure out what the MAC address is:

elatov@gen ~ $ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s25: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether AA:AA:AA:AA:AA:AA brd ff:ff:ff:ff:ff:ff

Then I just powered off the machine:

elatov@gen ~ $ sudo poweroff
WARNING: could not determine runlevel - doing soft poweroff
  (it's better to use shutdown instead of poweroff from the command line)

Broadcast message from root@gen.dnsd.me (pts/0) (Wed Nov 11 20:37:02 2015):
The system is going down for system halt NOW!

Then on my mac, I went ahead and installed the wol client:

elatov@macair:~$sudo port install wol

Then I went ahead and sent the magic packet:

elatov@macair:~$wol -i gen AA:AA:AA:AA:AA:AA
Waking up AA:AA:AA:AA:AA:AA...

and I kept a ping going and after some time the machine booted up:

elatov@macair:~$ping gen
PING gen.dnsd.me (192.168.1.114): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2
Request timeout for icmp_seq 3
64 bytes from 192.168.1.114: icmp_seq=4 ttl=64 time=697.877 ms
64 bytes from 192.168.1.114: icmp_seq=5 ttl=64 time=1.132 ms
64 bytes from 192.168.1.114: icmp_seq=6 ttl=64 time=1.146 ms
64 bytes from 192.168.1.114: icmp_seq=7 ttl=64 time=1.214 ms
64 bytes from 192.168.1.114: icmp_seq=8 ttl=64 time=1.724 ms
^C
--- gen.dnsd.me ping statistics ---
9 packets transmitted, 5 packets received, 44.4% packet loss
round-trip min/avg/max/stddev = 1.132/140.619/697.877/278.629 ms

On my CentOS machine I just ended using ether-wake which is part of the
net-tools rpm:

elatov@m2:~$rpm -qf /sbin/ether-wake
net-tools-2.0-0.17.20131004git.el7.x86_64

And executing the following accomplished the same thing:

elatov@m2:~$sudo ether-wake AA:AA:AA:AA:AA:AA

I was running the command from machines that were on the same subnet as the
destination host. If you
are traversing a switch or a router make sure those devices support passing
the magic packet across and allow directed broadcasts.
[Here](http://www.dd-wrt.com/wiki/index.php/WOL)  are some nice steps laid out
for dd-wrt. I will stick with local subnets :)

