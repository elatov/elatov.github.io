---
title: 'Corosync Pacemaker running on RHEL 6 VMs Receiving "Failed To Receive" Messages'
author: Karim Elatov
layout: post
permalink: /2012/08/corosync-pacemaker-running-on-rhel-6-vms-receiving-failed-to-receive-messages/
dsq_thread_id:
  - 1408246501
categories:
  - Networking
  - OS
  - VMware
tags:
  - Corosync
  - IGMP
  - IGMPv3 Snooping
  - iperf
  - MSI
  - multicast
  - net.core.rmem_max
  - OS UDP Buffer
  - Pacemaker
  - Rx ring size
  - TCP
  - UDP
---
I ran into in an interesting issue with Corosync Pacemaker. Before we get down to the trouble shooting let's figure out what Corosync Pacemaker is, from the <a href="https://github.com/corosync/corosync/wiki/why-was-corosync-created" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/corosync/corosync/wiki/why-was-corosync-created']);">Corosync FAQ</a>:

> **Why was Corosync created?**  
> Corosync was created from a derivative work of the openais project.
> 
> For 6 years, the openais project operated to implement Service Availability Forum APIs. After 6 years of development of a few APIs, we found ourselves consumed by the challenging task of creating the infrastructure on which the APIs would run. The infrastructure, such as interprocess communication, network protocols, recovery synchronization, timers, logging and tracing, and other components turned out to be more challenging then implementing any APIs on top.
> 
> The Corosync Cluster Engine project was created to recognize the reality that the cluster infrastructure was deserving of its own project and unique community. We placed high priority on creating a resilient and compact design that met all of the gaps we had identified through our experiences working with openais, and later Pacemaker and Apache Qpid. In the process, we made a serious and successful attempt at unifying the various cluster infrastructure communities and users into one code base. We reused ~80% of the code from openais in the Corosync implementation. The remaining 20% was mostly focused around the actual APIs which are out of scope for Corosync's mission.
> 
> Other projects such as the OCFS2 and GFS filesystem integration layer, CLVM, Pacemaker and Apache Qpid further expand Corosync's field deployments, and directly improve its quality through a large deployment community.

It's basically clustering software used with Linux to load balance applications, like Apache and the sorts. Here is a step by step <a href="http://www.clusterlabs.org/doc/en-US/Pacemaker/1.1/html/Clusters_from_Scratch/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.clusterlabs.org/doc/en-US/Pacemaker/1.1/html/Clusters_from_Scratch/']);">guide</a> of how to set it up. I would also suggest checking out "<a href="http://www.clusterlabs.org/wiki/Main_Page#Architecture" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.clusterlabs.org/wiki/Main_Page#Architecture']);">Pacemaker Architecture</a>" page, from that page is an example of one setup:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/pacemaker_archi.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/pacemaker_archi.png']);"><img class="alignnone size-full wp-image-3102" title="pacemaker_archi" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/pacemaker_archi.png" alt="pacemaker archi Corosync Pacemaker running on RHEL 6 VMs Receiving Failed To Receive Messages" width="357" height="319" /></a>

The way that Corosync keeps track of nodes is by using Multicast Traffic. As a result certain configuration needs to be done on the physical switch. For more information check out "<a href="https://github.com/corosync/corosync/wiki/Corosync-and-Cisco-switches" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/corosync/corosync/wiki/Corosync-and-Cisco-switches']);">Corosync FAQ</a>". The multicast settings on the physical switch were complete, however we ran into issue described in <a href="http://web.archiveorange.com/archive/v/yYk4Bu2apcznJXy167SY" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://web.archiveorange.com/archive/v/yYk4Bu2apcznJXy167SY']);">this</a> page. At first we thought the vSwitch was not passing multicast traffic properly. We read over "<a href="http://www.vmware.com/files/pdf/technology/esx35_ip_multicast.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/technology/esx35_ip_multicast.pdf']);">Using IP Multicast with VMware ESX 3.5</a>" (even though we were using ESX 4.x, the way that multicast works is the same across 3.x or 4.x). From that article:

> **Operation of Multicast on an ESX Virtual Switch**  
> IP multicast is fully supported by VMware ESX. The implementation and operation of multicast, however, differs slightly from the implementation and operation in a physical switch.
> 
> A virtual switch (vSwitch) does not need to perform IGMP snooping to learn which virtual machines have  
> enabled IP multicast. ESX dynamically learns multicast membership because it has authoritative knowledge of the attached virtual NICs (vNIC). When a vNIC attached to a virtual machine is configured for multicast, the vSwitch learns the multicast Ethernet group addresses associated with the virtual machine. When the virtual machine joins an IP multicast group, the virtual machine first converts the group to an Ethernet multicast group based on the IP address. The virtual machine then programs its own NIC filter on the vNIC to subscribe to the multicast traffic. The vNIC passes the multicast registration information down to the vSwitch through the hypervisorto update the multicast tables on the vSwitch and enable forwarding of frames for that IP multicast group to that virtual machine.

We were using IGMPv3 Snooping on the upstream switch and per "<a href="http://www.vmware.com/files/pdf/technology/cisco_vmware_virtualizing_the_datacenter.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/technology/cisco_vmware_virtualizing_the_datacenter.pdf']);">Cisco VMware Virtualizing the Datacenter</a>", we see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/igmp_snooping_vswitch.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/igmp_snooping_vswitch.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/08/igmp_snooping_vswitch.png" alt="igmp snooping vswitch Corosync Pacemaker running on RHEL 6 VMs Receiving Failed To Receive Messages" title="igmp_snooping_vswitch" width="551" height="287" class="alignnone size-full wp-image-3127" /></a>

The document makes it seem that the VMware Virtual Switches don't support IGMPv3 Snooping and that is not the case, if you keep reading the document, you will see the following:

> **Multicast:** Both vSwitch alternatives support multicast traffic and multicast group  
> membership through IGMP. The Cisco and VMware switches differ slightly in implementation.  
> The VMware vSwitches learn multicast membership through a nonflooding registration  
> process, and the Cisco Nexus 1000V Series uses IGMP snooping in a similar fashion on a  
> physical switch.

So it's not that the VMware Virtual Switch doesn't support IGMPv3 Snooping, it's more that it doesn't need to use it. The reason why it doesn't use it is mentioned in the first article. It keeps track of the IGMP traffic by using the virtual ports and there is not need to snoop IGMP traffic. But all IGMP versions are supported, from the first article:

> You can set the following parameters:
> 
> **IGMP Version** - Default is IGMP V3. This parameter determines whether IGMP V2 or IGMP V3  
> membership queries are sent to the virtualmachine afterit is moved with VMotion. Virtual machines with  
> an IGMP V2 implementation might ignore IGMP V3 queries. However, IGMP V3 hosts should respond  
> to IGMP V2 queries. This is an ESX host parameter and thus affects all virtual machines on that host. If  
> you have some virtual machines with V2 and some with V3, set this parameter to the lowest common  
> denominator of V2. Otherwise, leave this at V3.
> 
> **IGMP Queries** - Default is 2. This specifies how many IGMP V2 or V3 membership queries are sent to the virtual machine immediately after it is moved with VMotion to solicit the IGMP membership reports. Two queries are sent by default to reduce impact of any isolated packet drops.

So from the ESX side of things, there is nothing to be done when working with multicast traffic. For testing we set the "*IGMP Version*" setting on the ESX to '2' and changed the RHEL VMs to also use IGMP version 2, you can check the setting from the VM like this:

	  
	# cat /proc/net/igmp  
	Idx Device : Count Querier Group Users Timer Reporter  
	1 lo : 1 V3  
	010000E0 1 0:00000000 0  
	2 eth0 : 1 V3  
	010000E0 1 0:00000000 0  
	3 eth1 : 1 V3  
	010000E0 1 0:00000000 0  
	4 eth2 : 2 V3  
	150BC0EF 1 0:00000000 0  
	010000E0 1 0:00000000 0  
	

The above output is showing the VM using IGMP V3. After we changed to version to 2, it didn't make a difference. We checked out the VMware blog "<a href="http://blogs.vmware.com/performance/2011/08/multicast-performance-on-vsphere-50.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/performance/2011/08/multicast-performance-on-vsphere-50.html']);">Multicast Performance on vSphere 5.0</a>". There is a new setting called "splitRxMode", which can improve multicast traffic but we were running 4.x so this didn't apply to us. 

We knew that Multicast traffic uses the UDP protocol, so we decided to run two iperf tests to compare if there is a difference between tcp traffic and udp traffic. For UDP traffic we ran the following:

On node1:  
	  
	$ iperf --udp -p 333 -s  
	

On node2, run:

	  
	$ iperf -c node1 --udp -p 333 -b 2000M -l 4000  
	

And we did a similar test with TCP:

	  
	$ iperf -p 333 -s  
	$ iperf -c node1 -p 333  
	

As we doing the testing, using UDP, the server only received a maximum of around 800 Mbits/sec. We were seeing consistent results over 6Gbits/sec with the TCP test (VMs were on the same host, that is why it was so fast). We were sending at a rate of 4 Gbit/sec but the receiver was only handling 800 Mbits/sec maximum. Also checking out the netstat statistics, we saw the following:

	  
	$ netstat -su  
	IcmpMsg:  
	InType8: 1  
	OutType0: 1  
	OutType3: 7  
	Udp:  
	3461 packets received  
	4 packets to unknown port received.  
	1000 packet receive errors  
	3499 packets sent  
	0 receive buffer errors  
	0 send buffer errors  
	UdpLite:  
	IpExt:  
	InMcastPkts: 50  
	OutMcastPkts: 58  
	InOctets: 86818219  
	OutOctets: 32431252  
	InMcastOctets: 11803  
	OutMcastOctets: 12364  
	

So we were dropping a lot of the UDP traffic. We checked out Vmware blog "<a href="http://blogs.vmware.com/vsphere/2009/04/considerations-for-maximum-network-performance.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2009/04/considerations-for-maximum-network-performance.html']);">Considerations for Maximizing UDP Performance</a>". We checked all the recommendations:

> 1.  vNIC types: do not use vlance. vlance is our oldest vNIC and does not have good performance. If a VM has “Flexible” vNIC without VMware tools installed, the vNIC will end up being vlance (pcnet32).
> 2.  In addition, for UDP, use either e1000 vNIC, or with ESX 4, vmxnet3, in order to be able to configure a larger vNIC Rx ring size. Because UDP can be a lot more bursty (due to lack of flow-control), having a larger Rx ring size helps to provide buffering/elasticity to better absorb the bursts. Both e1000 vNIC and our new vmxnet3 allows resizing the vNIC’s Rx ring size, up to around 1 to 2 thousand buffers. As a side note, there is some negative performance impact with larger ring size due to larger memory foot print. The new vxmnet3 vNIC is more efficient than the e1000 vNIC. Also in general, ESX 4 has some performance improvements over ESX 3.5.
> 3.  In the past, we have seen better networking performance with RHEL than with Fedora Core.
> 4.  If there are many more Virtual CPUs than Physical CPUs in a server, there will be contention for Physical CPU cycles. During the time a Virtual CPU of a VM waits for its turn to run, network Rx processing cannot happen in the VM and will more likely cause network packet drops. A larger Rx ring size may help, but it has its limits depending on the degree of over-commit.
> 5.  Another note/question is the number of Virtual CPUs in a VM. Having more Virtual CPUs may have some detrimental effects due to the added coordination needed between the multiple Virtual CPUs. If a uniprocessor VM suffices, that sometimes performs better.
> 6.  Finally, if the customer can use the newest processors, e.g. Intel’s Nehalem (5500 series), the boost from hardware improvement is quite substantial.

Checking over Esxtop we didn't see any dropped packets, but we followed the intructions laid out in VMware KB <a href="http://kb.vmware.com/kb/1010071" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1010071']);">1010071</a> and increased our ring buffers:

	  
	ethtool -G eth1 rx 4096  
	

But that didn't make a difference. We then ran into VMware KB <a href="http://kb.vmware.com/kb/1026055" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026055']);">1026055</a>, it suggested to disable msi, by adding:

	  
	pci=nomsi  
	

to the kernel line of the grub menu, but it didn't help out either. We then saw "<a href="https://access.redhat.com/knowledge/docs/en-US/JBoss_Enterprise_Web_Platform/5/html/Administration_And_Configuration_Guide/jgroups-perf-udpbuffer.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://access.redhat.com/knowledge/docs/en-US/JBoss_Enterprise_Web_Platform/5/html/Administration_And_Configuration_Guide/jgroups-perf-udpbuffer.html']);">Improving UDP Performance by Configuring OS UDP Buffer Limits</a>", and we decide to increase our UDP Buffer limit from within the RHEL Guest. We ran this:

	  
	sysctl -w net.core.rmem_max=26214400  
	sysctl -w net.core.wmem_max=26214400  
	sysctl -w net.core.rmem_default=26214400  
	sysctl -w net.core.wmem_default=26214400  
	

The bottom 3 were just in case, and probably weren't needed. After we changed those values, the packets stopped dropping and were able to achieve above 4Gb/sec for UDP traffic. Also after that, the Corosync Pacemaker stopped having random disconnects.

