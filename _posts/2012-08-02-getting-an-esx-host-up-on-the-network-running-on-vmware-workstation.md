---
title: Getting an ESX Host Up on the Network, Running on VMware Workstation
author: Karim Elatov
layout: post
permalink: /2012/08/getting-an-esx-host-up-on-the-network-running-on-vmware-workstation/
dsq_thread_id:
  - 1409908927
categories:
  - Home Lab
  - Networking
  - VMware
tags:
  - NAT
  - nested ESX
  - vswif
  - workstation
---
I was recently setting up an ESX and ESXi host on my local VMware Workstation, however whatever I tried I couldn't get the ESX host to reply to pings. I setup the ESX and ESXi host to use the NAT network from the VMware Workstation. Here is how the NAT settings looked like from the Virtual Network Editor:

![Virtual_network_Editor](http://virtuallyhyper.com/wp-content/uploads/2012/04/Virtual_network_Editor.png)

Here is the local interface on my laptop that is used for the NAT.

	[elatov@klaptop ~]$ ifconfig vmnet1
	vmnet1    Link encap:Ethernet  HWaddr 00:50:56:C0:00:01
	          inet addr:10.0.1.1  Bcast:10.0.1.255  Mask:255.255.255.0
	          inet6 addr: fe80::250:56ff:fec0:1/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:24 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)


Running a ping test from the ESX host just resulted in failures like so:

	[root@localhost ~]# ping -c 2 10.0.1.1
	PING 10.0.1.1 (10.0.1.1) 56(84) bytes of data.
	From 10.0.1.130 icmp_seq=1 Destination Host Unreachable
	From 10.0.1.130 icmp_seq=2 Destination Host Unreachable

	--- 10.0.1.1 ping statistics ---
	2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1008ms


Here is how the network setup looked like inside the ESX host:

	[root@localhost ~]# route -n
	Kernel IP routing table
	Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
	10.0.1.0        0.0.0.0         255.255.255.0   U     0      0        0 vswif0
	169.254.0.0     0.0.0.0         255.255.0.0     U     0      0        0 vswif0
	0.0.0.0         10.0.1.1        0.0.0.0         UG    0      0        0 vswif0

	[root@localhost ~]# esxcfg-nics -l
	Name    PCI   Driver  Link Speed     Duplex MAC Address       MTU    Description
	vmnic0  02:01 e1000   Up   1000Mbps  Full   00:0c:29:d3:3d:34 1500   Intel PRO/1000 MT Single Port Adapt.

	[root@localhost ~]# esxcfg-vswif -l
	Name     Port Group/DVPort   IP Family IP Address  Netmask        Broadcast    Enabled   TYPE
	vswif0   Service Console     IPv4      10.0.1.130  255.255.255.0  10.0.1.255   true      STATIC


So I just set a static IP of 10.0.1.130 with the default gateway of 10.0.1.1 and I am utilizing one uplink, which is the e1000 NIC (the 10.0.1.130 IP falls under the NAT network that I had defined). Doing a tcpdump on the vmnet1 interface during my ping test from above, I saw the following.

	[elatov@klaptop ~]$ sudo tcpdump -i vmnet1 -nne
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on vmnet1, link-type EN10MB (Ethernet), capture size 65535 bytes
	16:12:11.558123 00:50:56:4c:e5:09 > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 60: Request who-has 10.0.1.1 tell 10.0.1.130, length 46
	16:12:11.558156 00:50:56:c0:00:01 > 00:50:56:4c:e5:09, ethertype ARP (0x0806), length 42: Reply 10.0.1.1 is-at 00:50:56:c0:00:01, length 28
	16:12:12.573888 00:50:56:4c:e5:09 > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 60: Request who-has 10.0.1.1 tell 10.0.1.130, length 46
	16:12:12.573910 00:50:56:c0:00:01 > 00:50:56:4c:e5:09, ethertype ARP (0x0806), length 42: Reply 10.0.1.1 is-at 00:50:56:c0:00:01, length 28
	16:12:13.590891 00:50:56:4c:e5:09 > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 60: Request who-has 10.0.1.1 tell 10.0.1.130, length 46
	16:12:13.590923 00:50:56:c0:00:01 > 00:50:56:4c:e5:09, ethertype ARP (0x0806), length 42: Reply 10.0.1.1 is-at 00:50:56:c0:00:01, length 28
	6 packets captured
	6 packets received by filter
	0 packets dropped by kernel


So the vswif interface is ARP'ing out to find out the mac address of it's default gateway, and the vmnet1 interface is responding to the the request but the vswif0 interface is not getting it.

Now my ESXi host worked without any issues. Here is how the network looks like for the ESXi host:

	~ # esxcfg-vmknic -l
	Interface Port_Group         IP_Address Netmask       Broadcast  MAC Address       MTU  Enabled Type
	vmk0      Management Network 10.0.1.128 255.255.255.0 10.0.1.255 00:0c:29:2c:54:17 1500 true    STATIC

	~ # esxcfg-nics -l
	Name   PCI    Driver Link Speed    Duplex MAC Address       MTU  Description
	vmnic0 02:00  e1000  Up   1000Mbps Full   00:0c:29:2c:54:17 1500 Intel PRO/1000 MT Single Port Adapter


So my ESXi host had the IP of 10.0.1.128, which also falls under my NAT network. Now whenever I did a ping test from the ESXi host, I saw the following:

	~ # vmkping -c 2 10.0.1.1
	PING 10.0.1.1 (10.0.1.1): 56 data bytes
	64 bytes from 10.0.1.1: icmp_seq=0 ttl=64 time=0.337 ms
	64 bytes from 10.0.1.1: icmp_seq=1 ttl=64 time=6.532 ms

	--- 10.0.1.1 ping statistics ---
	2 packets transmitted, 2 packets received, 0% packet loss
	round-trip min/avg/max = 0.337/3.434/6.532 ms


It worked just fine. Now looking at the packet capture as the pings were going, I saw the following:

	[elatov@klaptop ~]$ sudo tcpdump -i vmnet1 -nne
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on vmnet1, link-type EN10MB (Ethernet), capture size 65535 bytes
	16:17:22.749184 00:0c:29:2c:54:17 > 00:50:56:c0:00:01, ethertype IPv4 (0x0800), length 98: 10.0.1.128 > 10.0.1.1: ICMP echo request, id 52787, seq 0, length 64
	16:17:22.749227 00:50:56:c0:00:01 > 00:0c:29:2c:54:17, ethertype IPv4 (0x0800), length 98: 10.0.1.1 > 10.0.1.128: ICMP echo reply, id 52787, seq 0, length 64
	16:17:23.750021 00:0c:29:2c:54:17 > 00:50:56:c0:00:01, ethertype IPv4 (0x0800), length 98: 10.0.1.128 > 10.0.1.1: ICMP echo request, id 52787, seq 1, length 64
	16:17:23.750079 00:50:56:c0:00:01 > 00:0c:29:2c:54:17, ethertype IPv4 (0x0800), length 98: 10.0.1.1 > 10.0.1.128: ICMP echo reply, id 52787, seq 1, length 64


Looking at the packet captures I noticed that the ESXi host was using the following MAC address: 00:0c:29:2c:54:17 but looking at the ESX host it is using the following mac address: 00:50:56:4c:e5:09. You will notice the ESX host is using it's typical virtual MAC address starting with 00:50:56. Where the ESXi host is using the "physical" MAC address that was assigned to it. The physical mac address assigned to the ESX host can be seen from the esxcfg-nics output:

	[root@localhost ~]# esxcfg-nics -l
	Name   PCI   Driver Link Speed    Duplex MAC Address MTU Description
	vmnic0 02:01 e1000  Up   1000Mbps Full **00:0c:29:d3:3d:34** 1500 Intel PRO/1000 MT Single Port Adapt.


Now looking at the MAC Address of the vswif0 interface, we see the following:

	[root@localhost ~]# ifconfig vswif0
	vswif0    Link encap:Ethernet  HWaddr **00:50:56:4C:E5:09**
	          inet addr:10.0.1.130  Bcast:10.0.1.255  Mask:255.255.255.0
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:1 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:27 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:60 (60.0 b)  TX bytes:1158 (1.1 KiB)


Now looking at the ESXi host, we see the following:

	~ # esxcfg-nics -l
	Name   PCI    Driver Link Speed    Duplex MAC Address       MTU  Description
	vmnic0 02:00  e1000  Up   1000Mbps Full   **00:0c:29:2c:54:17** 1500 Intel PRO/1000 MT Single Port Adapter


In Bold is the physical MAC address assigned to the ESXi host. Now looking at the MAC address of the Vmk interface used for management I saw the following:

	# esxcfg-vmknic -l
	Interface Port_Group         IP_Address Netmask       Broadcast  MAC Address       MTU  Enabled Type
	vmk0      Management Network 10.0.1.128 255.255.255.0 10.0.1.255 **00:0c:29:2c:54:17** 1500 true    STATIC


So the management interface of the ESXi host uses the same MAC as the physical NIC. Where on the ESX host the management interface creates a virtual MAC address and uses that. This is actually expected and per KB [1031111](http://kb.vmware.com/kb/1031111) you can change the behavior with a setting.

So for security reasons VMware workstation is not allowing to send traffic with a MAC address other than what is assigned to the VM. I found a couple web pages which described how to get around the issue: [sanbarrow](http://kb.vmware.com/kb/1042). Supposedly setting the option *ethernetX.noForgedSrcAddr* to *False* should allow for MAC Address changes. I tried setting that option and many others, but whatever I tried to put into the VMX file of the ESX host VM, it would not work. So I j

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>

  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Use FWBuilder to Deploy an IPtables Firewall to a DD-WRT Router" href="http://virtuallyhyper.com/2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/" rel="bookmark">Use FWBuilder to Deploy an IPtables Firewall to a DD-WRT Router</a>
    </li>
  </ul>
</div>

