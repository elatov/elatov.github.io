---
published: true
title: Seeing a High Number of Trespasses from a CLARiiON Array with ESX Hosts
author: Karim Elatov
layout: post
permalink: /2012/04/seeing-a-high-number-of-trespasses-from-a-clariion-array-with-esx-hosts/
categories: ['storage', 'vmware']
tags: ['fiber_channel', 'nmp', 'alua', 'tgp', 'lun_trespass', 'useano']
---

I was recently working with a customer who was experiencing a high number of Trespasses on his CLARiiON Array with 3 ESX 4.0 hosts. While this was happening I saw the following in the logs across all the hosts:


	Apr 19 09:25:54 ESX_Host vmkernel: 0:18:55:02.430 cpu2:4262)VMW_SATP_ALUA: satp_alua_activatePaths: Activation disallowed due to follow-over.
	Apr 19 09:36:36 ESX_Host vmkernel: 0:19:05:45.146 cpu0:4478)NMP: nmp_CompleteCommandForPath: Command 0x2a (0x410001032580) to NMP device 'naa.60060160467029002acca5f7836fe111' failed on physical path 'vmhba2:C0:T1:L3' H:0x0 D:0x2 P:0x0 Valid sense data: 0x6 0x2a 0x6.
	Apr 19 09:36:36 ESX_Host vmkernel: 0:19:05:45.146 cpu0:4478)WARNING: NMP: nmp_DeviceRetryCommand: Device 'naa.60060160467029002acca5f7836fe111': awaiting fast path state update for failover with I/O blocked. No prior reservation exists on the device.
	Apr 19 09:36:37 ESX_Host vmkernel: 0:19:05:46.147 cpu2:4222)WARNING: NMP: nmp_DeviceAttemptFailover: Retry world failover device 'naa.60060160467029002acca5f7836fe111' - issuing command 0x410001032580
	Apr 19 09:36:37 ESX_Host vmkernel: 0:19:05:46.147 cpu0:4096)NMP: nmp_CompleteRetryForPath: Retry world recovered device 'naa.60060160467029002acca5f7836fe111'


The customer had setup the CLARiiON to use ALUA (Assymetric Logical Unit Access) mode (fail over mode 4). From [EMC CLARiiON Integration with VMware ESX](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/clariion_wp_eng.pdf):

> On VMware 4.x servers with CX4 arrays, the FIXED or Round Robin policy is supported. The FIXED policy on the CX4 provides failback capability. To use the FIXED policy, you must be running FLARE release 28 version 04.28.000.5.704 or later. Also, the failovermode mode must be set to 4 (ALUA mode or Asymmetric Active/Active mode). The default failovermode for ESX 4.x is 1. Use the Failover Setup Wizard within Navisphere to change the failovermode from 1 to 4.

Since all CLARiiON arrays are active/passive, from [A couple important (ALUA and SRM) notes](http://virtualgeek.typepad.com/virtual_geek/2009/09/a-couple-important-alua-and-srm-notes.html):

> CLARiiON arrays are in VMware’s nomenclature an “active/passive” array – they have a LUN ownership
> model where internally a LUN is “owned” by one storage processor or the other. This is common in
> mid-range (“two brain” aka “storage processors”) arrays who’s core architecture was born in
> the 1990s (and is similar to NetApp’s Fibre Channel – but not iSCSI - implementation, HP EVA and others)

Setting it for ALUA mode is actually a good idea. Before we get too far ahead of our selves, first let's define what active/passive means and then we can figure out what ALUA is. From this great post, [Assymetric Logical Unit Access (ALUA) mode on CLARiiON](http://gestaltit.com/all/tech/storage/bas/assymetric-logical-unit-access-alua-mode-emc-clariion):

> Normally a path to a CLARiiON is considered active when we are connected to the service processor that is currently serving you the LUN. CLARiiON arrays are so called “active/passive” arrays, meaning that only one service processor is in charge of a LUN, and the secondary service processor is just waiting for a signal to take over the ownership in case of a failure. The array will normally receive a signal that tells it to switch from one service processor to the other one. This routine is called a “trespass” and happens so fast that you usually don’t really notice such a failover.

Now what does ALUA allow us to do, from the same post:

> To put it more simply, ALUA allows me to reach my LUN via the active and the inactive service
> processor. Oversimplified this just means that all traffic that is directed to the non-active service
> processor will be routed internally to the active service processor.
>
> On a CLARiiON that is using ALUA mode this will result in the host seeing paths that are in an optimal
> state, and paths that are in an non-optimal state. The optimal path is the path to the active storage
> processor and is ready to perform I/O and will give you the best performance, and the non-optimal path
> is also ready to perform I/O but won’t give you the best performance since you are taking a detour.

Now how does the array actually do this, from the article "[EMC CLARiiON Asymmetric Active/Active Feature](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/high-trespass-clariion/h2890-emc-clariion-asymm-active-wp.pdf):

> In dual-SP systems, such as a CLARiiON, I/O can be routed through either SP. For example, if I/O for a LUN is sent to an SP that does not own the LUN, that SP redirects the I/O to the SP that does own the LUN. This redirection is done through internal communication within the storage system. It is transparent to the host, and the host is not aware that the other SP processed the I/O. Hence, a trespass is not required when I/O is sent to the non-owning (or non- optimal) SP.
>
> Dual-SP storage systems that support ALUA define a set of target port groups for each LUN. One target port group is defined for the SP that currently owns the LUN, and the other target port group is defined for the SP that does not own the LUN. Standard ALUA commands enable the host failover software to determine the state of a LUN’s path.

Inside that same document there is an excellent picture that depicts how ALUA works. Check it out:

![ALUA](https://github.com/elatov/uploads/raw/master/2012/04/ALUA.png)

ALUA uses Target Port Groups (TGP) for multiple aspects, so it's very important to understand
what those are. There is a great picture of TGP in this article, [It All Started With This Question…](http://deinoscloud.wordpress.com/2011/07/04/it-all-started-with-this-question/):

![asymmetricaccessstate](https://github.com/elatov/uploads/raw/master/2012/04/asymmetricaccessstate.png)

Also from [EMC CLARiiON Asymmetric Active/Active Feature](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/high-trespass-clariion/h2890-emc-clariion-asymm-active-wp.pdf):

> Target port group — A set of target ports that are in either primary SP ports or secondary SP ports.

Now once you understand what those are, you can actually query TPGs and get information back regarding
the state of the Group, and the result is called Target Port Group Support (TGPS). From the same document:

> The Report Target Port Group command provides a report about the following three attributes:
>
> Preferred — Indicates whether this port group is the default (preferred) port group.
> Asymmetric access state — Indicates the state of the port group. *Port group states include Active/Optimal,Active/Non-optimal, Standby, and Unavailable.*
> Attribute — Indicates whether the current asymmetric access state was explicitly set by a command or
> was implicitly set or changed by the storage system.
>
> The SET TARGET PORT GROUP command allows the access state (*Active/Optimal, Active/Non-optimal, Standby,and Unavailable*) of each port group to be set or changed.
>
> Access states are:
>
> *Active/Optimal* — Best performing path, does not require upper level redirection to complete I/O
> *Active/Non-optimal* — Requires upper level redirection to complete I/O
> *Standby* — This state is not supported by CLARiiON
> *Unavailable* — Returned for port groups on a SP that is down. The user cannot set it by using set
> target port groups.
>
> Target port group commands are implemented in the ALUA layer of the storage system. However, host-
> based path management software executes the commands and manages the paths. The explicit ALUA approach is similar to the traditional path management mechanisms except that ALUA has standardized the previously vendor-specific mechanisms

In short, you define a port group that SPs are part of and these port groups can return status of LUNs depending the owner and preference.

Now that we got that out of the way let's back to logs, so we saw
the following sense code returned: *H:0x0 D:0x2 0x6 0x2a 0x6*. Translating that we get the following:


	ASC/ASCQ: 2Ah / 06h
	ASC Details: ASYMMETRIC ACCESS STATE CHANGED
	Status: 02h - CHECK CONDITION
	Hostebyte: 0x00 - DID_OK - No error
	Sensekey: 6h
	Sensekey MSG: UNIT ATTENTION


We are getting an *Access State Changed*, and that is expected since this was a trespass. Now looking at the output of the 'nmp device' we saw the following


	# esxcli nmp device list -d naa.600601604670290026cca5f7836fe111
	naa.600601604670290026cca5f7836fe111
	Device Display Name: DGC Fibre Channel Disk (naa.600601604670290026cca5f7836fe111)
	Storage Array Type: VMW_SATP_ALUA_CX
	Storage Array Type Device Config: {navireg=on, ipfilter=on}{implicit_support=on;explicit_support=on;explicit_allow=on;alua_followover=on;{TPG_id=1,TPG_state=ANO}{TPG_id=2,TPG_state=AO}}
	Path Selection Policy: VMW_PSP_FIXED
	Path Selection Policy Device Config: {preferred=vmhba2:C0:T1:L1;current=vmhba2:C0:T1:L1}
	Working Paths: vmhba2:C0:T1:L1


The most important line is the following:


	Storage Array Type Device Config: {navireg=on, ipfilter=on}{implicit_support=on;explicit_support=on;explicit_allow=on;alua_followover=on;{TPG_id=1,TPG_state=ANO}{TPG_id=2,TPG_state=AO}}


Definitions of all the settings can be found at VMware KB [1022030](http://kb.vmware.com/kb/1022030):

> implicit_support=on
>
> This parameter shows whether or not the device supports implicit ALUA. You cannot set this option as it is a property of the LUN.
>
> explicit_support
>
> This parameter shows whether or not the device supports explicit ALUA. You cannot set this option as it is a property of the LUN.
>
> explicit_allow
>
> This parameter shows whether or not the user allows the SATP to exercise its explicit ALUA capability
> if the need arises during path failure. This only matters if the device actually supports explicit ALUA
> (that is, explicit_support is on). This option is turned on using the esxcli command enable_explicit_alua
> and turned off using the esxcli command disable_explicit_alua.
>
> alua_followover
>
> This parameter shows whether or not the user allows the SATP to exercise the follow-over policy,
> which prevents path thrashing in multi-host setups. This option is turned on using the esxcli command
> enable_alua_followover and turned off using the esxcli command disable_alua_followover.

Just to elaborate, the article '[EMC CLARiiON Asymmetric Active/Active Feature](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/high-trespass-clariion/h2890-emc-clariion-asymm-active-wp.pdf)', has a good paragraph about implicit and explicit failover:

> Explicit and implicit failover software
> Explicit and implicit failover software should not be confused with the explicit and implicit trespass
> commands mentioned earlier.
>
> Failover software that supports *explicit* ALUA commands monitors and adjusts the active paths between optimal and non-optimal using the REPORT TARGET PORT GROUPS and SET TARGET PORT GROUPS commands, respectively. The SET TARGET PORT GROUPS command, when issued on one controller, trespasses the LUN to the other controller. PowerPath has the same net effect as an explicit trespass, although it uses traditional CLARiiON proprietary commands to initiate a trespass. Windows 2008 MPIO supports explicit ALUA commands.
> It is possible for host multipathing software to support *implicit* ALUA functionality. The host could redirect traffic to the non-optimal path for some reason that is not apparent to the storage system. In this case, the storage system must implicitly trespass once it detects enough I/O on the non-optimal paths. To get the optimal path information, the failover software uses the REPORT TARGET PORT GROUPS command. AIX MPIO only supports implicit ALUA commands.
> Both *explicit* and *implicit* failover software may or may not provide autorestore capability. Without the
> autorestore capability, after an NDU, all LUNs could end up on the same SP. Cluster software could also make use of this functionality.

Also, if you want to know what follow-over is, I would suggest reading this '[Configuration Settings for ALUA
Devices][1]' .

Lastly we also see the following from the *nmp device* command that we haven't defined yet:

	{TPG_id=1,TPG_state=AO}{TPG_id=2,TPG_state=ANO}

and from the above blog:

> There are two Target Port Groups. TPG_id=1 has all the Active Optomized paths (AO). TPG_id=2 has all the Active Non-Optomized paths (ANO)

Now running the *nmp path* commands, we saw the following:


	# esxcli nmp path list -d naa.600601604670290026cca5f7836fe111
	fc.20000000c96eb647:10000000c96eb647-fc.50060160bea038b6:5006016d3ea038b6-naa.600601604670290026cca5f7836fe111
	Runtime Name: vmhba2:C0:T1:L1
	Device: naa.600601604670290026cca5f7836fe111
	Device Display Name: DGC Fibre Channel Disk (naa.600601604670290026cca5f7836fe111)
	Group State: active
	Storage Array Type Path Config: {TPG_id=2,TPG_state=AO,RTP_id=14,RTP_health=UP}
	Path Selection Policy Path Config: {current: yes; preferred: yes}

	fc.20000000c96eb647:10000000c96eb647-fc.50060160bea038b6:500601643ea038b6-naa.600601604670290026cca5f7836fe111
	Runtime Name: vmhba2:C0:T0:L1
	Device: naa.600601604670290026cca5f7836fe111
	Device Display Name: DGC Fibre Channel Disk (naa.600601604670290026cca5f7836fe111)
	Group State: active unoptimized
	Storage Array Type Path Config: {TPG_id=1,TPG_state=ANO,RTP_id=5,RTP_health=UP}
	Path Selection Policy Path Config: {current: no; preferred: no}


So the top path is going through TGP2 and the state of that TPG is AO (active/optimal) and that is the preferred path. The bottom path is going through TPG1 and the state is ANO (Active/non-optimal) and that is not the preffered path. I checked the other hosts and they looked the same, so no user preffered paths have been set and all the host are going through the AO path.

I also found VMware KB [2005369](http://kb.vmware.com/kb/2005369)  and it talks about how with Round Robin you can allow the ESX host to use Active Non-Optimized paths:


	#esxcli nmp psp setconfig --config useANO=1 --device <device uid>


But we weren't using Round Robin and all the hosts were consistent in their preffered path to be the Active Optimized Path. The article [EMC CLARiiON Integration with VMware ESX](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/clariion_wp_eng.pdf), talks about some pros and cons of Round Robin Vs. FIXED:

> When using the FIXED policy, the auto-restore or failback capability distributes the LUNs to their respective default storage processors (SPs) after an NDU operation. This prevents the LUNs from all being on a single storage processor after an NDU (Non-Disruptive Upgrade). When using the FIXED policy, ensure the preferred path setting is configured to be on the same storage processor for all ESX hosts accessing a given LUN.
>
> With the FIXED policy, there is some initial setup that is required to select the preferred path; the preferred path should also be the optimal path when using the ALUA mode. If set up properly, there should not be any performance impact when using failovermode 4 (ALUA). Note that FIXED sends I/O down only a single path. However, if you have multiple LUNs in your environment, you could very well choose a preferred path for a given LUN that is different for other LUNs and achieve static I/O load balancing FIXED performs an automatic restore, hence LUNs won't end up on a single SP after an NDU.
>
> When using Round Robin there is no auto-restore functionality, hence after an NDU all LUNs will end up
> on a single SP. A user would need to manually trespass some LUNs to the other SP in order to balance the load. The benefit of Round Robin is that not too many manual setups are necessary during initial setup; by default it uses the optimal path and does primitive load balancing (however, it still sends I/O down only a single path at a time). If multiple LUNs are used in the environment, you might see some performance boost. If you had a script that takes care of the manual trespass issue, then Round Robin would be the way to avoid manual configuration.

It turned out that the SAN Admin was doing some maintenance on the array and was manually trespassing the LUN to perform updates on the SPs. So the above logs were expected and there was nothing to worry about :)

### Related Posts

- [ESX(i) Host Experiencing a lot of Active Path Changes and Disconnects to/from VNX 5300 over iSCSI](/2012/08/esxi-host-experiencing-a-lot-of-active-path-changes-and-disconnects-to-vnx-5300-over-iscsi/)


 [1]: https://blogs.vmware.com/vsphere/2012/02/configuration-settings-for-alua-devices.html
