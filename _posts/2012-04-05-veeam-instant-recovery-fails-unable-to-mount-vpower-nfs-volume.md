---
title: 'VEEAM Instant Recovery Fails: Unable to mount vPower NFS volume'
author: Joe Chan
layout: post
permalink: /2012/04/veeam-instant-recovery-fails-unable-to-mount-vpower-nfs-volume/
dsq_thread_id:
  - 1406660292
categories:
  - Storage
  - VMware
tags:
  - nfs
  - veeam
  - vpower nfs
---
I had a customer recently who was trying to perform a VEEAM Instant Recovery operation and it was failing with the following error:

	  
	Failed to publish VM &quot;test vm&quot;  
	Unable to mount vPower NFS volume  
	(VEEAMBOX:/VeeamBackup_VEEAMBOX). veeambox.domain.local  
	An error occurred during host configuration.  
	

Looking at the vmkernel log on the ESX(i) host, we saw:

	  
	2012-04-03T17:24:25.522Z cpu21:3239)NFS: 190: NFS mount <VEEAMBOX\_IP\_ADDRESS>:/VeeamBackup_VEEAMBOX failed: The mount request was denied by the NFS server. Check that the export exists and that the client is permitted to mount it.  
	

It turns out he was running Microsoft Services for NFS in on his VEEAM server, and when VEEAM was telling the host to mount from the VEEAM server, it would try to mount from the MS NFS services. You could have also run:

	  
	netstat -nba  
	

to determine which process was listening on the NFS ports, and per <a title="VEEAM KB 1055" href="http://www.veeam.com/kb_articles.html/KB1055" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.veeam.com/kb_articles.html/KB1055']);" target="_blank">VEEAM KB 1055</a>, if everything was running properly, you should expect to see something like:

	  
	Proto Local Address Foreign Address State  
	TCP 0.0.0.0:111 0.0.0.0:0 LISTENING  
	[VeeamNFSSvc.exe]  
	TCP 0.0.0.0:135 0.0.0.0:0 LISTENING  
	RpcSs  
	TCP 0.0.0.0:1058 0.0.0.0:0 LISTENING  
	[VeeamNFSSvc.exe]  
	TCP 0.0.0.0:2049 0.0.0.0:0 LISTENING  
	[VeeamNFSSvc.exe]  
	

We stopped the Microsoft NFS service and restarted the VEEAM vPower NFS Service, and was able to perform the Instant Recovery operation successfully.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 15 – NFS" href="http://virtuallyhyper.com/2014/04/rhcsa-rhce-chapter-15-nfs/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/04/rhcsa-rhce-chapter-15-nfs/']);" rel="bookmark">RHCSA and RHCE Chapter 15 – NFS</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" href="http://virtuallyhyper.com/2014/01/installing-lsi-cim-providers-megaraid-8704elp-local-controller-esxi/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/01/installing-lsi-cim-providers-megaraid-8704elp-local-controller-esxi/']);" rel="bookmark">Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Lost NFS Connectivity from ESX(i) Host when NAS is Another Subnet" href="http://virtuallyhyper.com/2012/11/lost-nfs-connectivity-from-esxi-host-when-nas-is-another-subnet/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/lost-nfs-connectivity-from-esxi-host-when-nas-is-another-subnet/']);" rel="bookmark">Lost NFS Connectivity from ESX(i) Host when NAS is Another Subnet</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Configure Windows 2008 as NFS share for VMware ESX" href="http://virtuallyhyper.com/2012/06/configure-windows-2008-nfs-share-vmware-esx/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/06/configure-windows-2008-nfs-share-vmware-esx/']);" rel="bookmark">Configure Windows 2008 as NFS share for VMware ESX</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VMs are Experiencing High Latency to NetApp FAS 6240" href="http://virtuallyhyper.com/2012/06/vms-experiencing-high-latency-netapp-fas-6270/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/06/vms-experiencing-high-latency-netapp-fas-6270/']);" rel="bookmark">VMs are Experiencing High Latency to NetApp FAS 6240</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/veeam-instant-recovery-fails-unable-to-mount-vpower-nfs-volume/" title=" VEEAM Instant Recovery Fails: Unable to mount vPower NFS volume" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:nfs,veeam,vpower nfs,blog;button:compact;">I was recently presented with the following environment: VMware ESX NetAPP ESX 4.1P03 FAS 6240 With this setup all the VMs from the ESX that resided on the NFS Datastores...</a>
</p>