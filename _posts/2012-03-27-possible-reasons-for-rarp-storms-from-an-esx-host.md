---
title: Possible reasons for RARP storms from an ESX host
author: Karim Elatov
layout: post
permalink: /2012/03/possible-reasons-for-rarp-storms-from-an-esx-host/
dsq_thread_id:
  - 1405913417
categories:
  - Networking
  - VMware
tags:
  - beacon probing
  - GARP
  - Gratuitous ARP
  - multicast
  - pxe boot
  - RARP
  - RARP Flood
---
I see a lot of different reasons for a RARP storms from an ESX host. The biggest one that I ran into is a PXE boot environment (ie: Citrix Provisioning Server). During the PXE boot process the unicast mac-address changes and the ESX host sends a GARP to notify the switch (sometimes these GARPs show up as RARPs in Wireshark). If you see thousands of RARPs, then you may have run into some known issues that have been fixed with the following patch. For ESX 4.1 <a href="http://kb.vmware.com/kb/2009136" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2009136']);">2009136</a> and for ESXi 4.1 <a href="http://kb.vmware.com/kb/2009143" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2009143']);">2009143</a>, for both patches we see the following:

> An erroneous code sends out Reverse Address Resolution Protocol (RARP) broadcasts immediately after a unicast Address is changed. The issue is resolved by timing the RARP broadcasting in a timer to avoid RARP packets from flooding.

If you see a couple of RARPs, then that is normal. Another reason if RARPs is joining a Multicast group, again a couple are fine but an excessive amount is a known issue and for 4.1 the above patch fixes it. From the same articles:

UPDATE: This has been back ported into 4.0 and is included in P11 for ESX <a href="http://kb.vmware.com/kb/2011767" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2011767']);">2011767</a> and for ESXi <a href="http://kb.vmware.com/kb/2011768" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2011768']);">2011768</a>

> ESXi generates unnecessary and excessive Reverse Address Resolution Protocol (RARP) packets when virtual machines join or leave multicast groups.

ESXi 5.0 U1 fixes similar issues, from the <a href="https://www.vmware.com/support/vsphere5/doc/vsp_esxi50_u1_rel_notes.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/vsphere5/doc/vsp_esxi50_u1_rel_notes.html']);">ESXi 5.0 U1 Release Notes</a>:

<div>
</div>

> <div>
>   **ESXi host generates excessive RARP broadcasts with multicast traffic**<br /> ESXi host generates excessive Reverse Address Resolution Protocol (RARP) packets when virtual machines join or leave multicast groups.This issue is resolved in this release.
> </div>

And lastly, I have seen a lot of RARPs when you have Beacon probes enabled. Another person actually blogged about it already: <a href="http://virtualrj.wordpress.com/2009/01/14/beacon-probing-resulting-in-excessive-broadcasts/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtualrj.wordpress.com/2009/01/14/beacon-probing-resulting-in-excessive-broadcasts/']);">Beacon probing resulting in excessive broadcasts</a>.

Like I mentioned, some RARPs are actually okay. Whenever you have 'notify switch' set to yes on your virtual switch or your network port groups then you will send GARPs (which are seen as RARPs). A VMware document describes what the 'notify switch' option does, <a href="http://www.vmware.com/files/pdf/virtual_networking_concepts.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/virtual_networking_concepts.pdf']);">VMware Virtual Networking Concepts</a>:

> Using the Notify Switches policy setting, you determine how ESX Server communicates with the physical switch in the event of a failover. If you select Yes, whenever a virtual Ethernet  adapter is connected to the virtual switch or whenever that virtual Ethernet adapter’s traffic would be routed over a different physical Ethernet adapter in the team due to a failover event, a notification is sent out over the network to update the lookup tables on physical switches. In almost all cases, this is desirable for the lowest latency when a failover occurs

The way that an ESX host updates the switch is by sending a GARP (<a href="http://wiki.wireshark.org/Gratuitous_ARP" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.wireshark.org/Gratuitous_ARP']);">Gratuitous ARP</a>). Here is how it looks like from the ESXi host when I run tcpdump-uw (I fired a vMotion of a VM with the mac address of 00:50:56:9b:4f:0d):

	listening on vmk0, link-type EN10MB (Ethernet), capture size 96 bytes
	01:21:56.178929 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46
	01:21:56.964847 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46
	01:21:57.964780 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46
	01:21:58.964792 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46
	01:22:00.964920 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46
	01:22:03.964933 00:50:56:9b:4f:0d > ff:ff:ff:ff:ff:ff, ethertype Reverse ARP (0x8035), length 60: Reverse Request who-is 00:50:56:9b:4f:0d tell 00:50:56:9b:4f:0d, length 46

So you can see that the Mac address 00:50:56:9b:4f:0d (the mac address of the VM) is sending a GARP (but the packet capture shows it as a RARP) and you can see the target machine is itself (tell 00:50:56:9b:4f:0d). If you don't want to apply the patches above, you can just set the 'notify-switch' option to 'no'. Instructions can be found here: <a href="http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.vsphere.networking.doc_50/GUID-D5EA6315-5DCD-463E-A701-B3D8D9250FB5.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.vsphere.networking.doc_50/GUID-D5EA6315-5DCD-463E-A701-B3D8D9250FB5.html']);">Edit Failover and Load Balancing Policy for a vSphere Standard Switch</a>

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="VMs Setup to Use Windows NLB in Unicast Mode Lose Network Connectivity When HP Virtual Connect Module is Replaced" href="http://virtuallyhyper.com/2012/09/vms-setup-to-use-windows-nlb-in-unicast-mode-lose-network-connectivity-when-hp-virtual-connect-module-is-replaced/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vms-setup-to-use-windows-nlb-in-unicast-mode-lose-network-connectivity-when-hp-virtual-connect-module-is-replaced/']);" rel="bookmark">VMs Setup to Use Windows NLB in Unicast Mode Lose Network Connectivity When HP Virtual Connect Module is Replaced</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Corosync Pacemaker running on RHEL 6 VMs Receiving "Failed To Receive" Messages" href="http://virtuallyhyper.com/2012/08/corosync-pacemaker-running-on-rhel-6-vms-receiving-failed-to-receive-messages/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/corosync-pacemaker-running-on-rhel-6-vms-receiving-failed-to-receive-messages/']);" rel="bookmark">Corosync Pacemaker running on RHEL 6 VMs Receiving "Failed To Receive" Messages</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCD-NI Network Pools with the Cisco Nexus1000v Distributed Switch" href="http://virtuallyhyper.com/2012/08/vcd-ni-network-pools-with-the-cisco-nexus1000v/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/vcd-ni-network-pools-with-the-cisco-nexus1000v/']);" rel="bookmark">VCD-NI Network Pools with the Cisco Nexus1000v Distributed Switch</a>
    </li>
  </ul>
</div>

