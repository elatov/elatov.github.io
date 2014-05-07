---
title: Restore vCenter from VDR onto a Host Being Managed by vCenter
author: Joe Chan
layout: post
permalink: /2012/04/restore-vcenter-from-vdr-onto-a-host-being-managed-by-vcenter/
dsq_thread_id:
  - 1404673056
categories:
  - VMware
tags:
  - restore
  - vcenter
  - vdr
  - virtualcenter
  - vmware data recovery
  - vpxa
---
I recently had an issue where I was unable to restore vCenter (running in a virtual machine) to a host that vCenter was managing (quite the catch-22 situation).

Here is the error we were getting:

	  
	Access to resource settings on the host is restricted to the server 'x.x.x.x' which is managing it.  
	

So we need to trick the hosts into thinking they aren&#8217;t being managed by vCenter. This may or may not be supported officially by VMware, but it worked for me.

- backup vpxa.cfg

**NOTE**: Check your version of ESX/ESXi to determine where the vpxa.cfg file is actually located. The location of the vpxa configuration directory changed from /etc/**opt**/vmware/vpxa to /etc/vmware/vpxa in ESXi 5. Here is a quick reference.

ESX and ESXi 4.x and prior:  
/etc/opt/vmware/vpxa/vpxa.cfg

ESXi 5:  
/etc/vmware/vpxa/vpxa.cfg

	  
	~ # cp /etc/vmware/vpxa/vpxa.cfg /etc/vmware/vpxa/vpxa.cfg.bak  
	~ # ls /etc/vmware/vpxa  
	dasConfig.xml vpxa.cfg vpxa.cfg.bak  
	

- edit vpxa.cfg with the command-line text editor, &#8220;vi&#8221; (how to use vi is outside the scope of this post, but there are plenty of resources online if you would like to learn more about it):

	  
	~ # vi /etc/vmware/vpxa/vpxa.cfg  
	

- and replace

	  
	<vpxa>  
	<bundleVersion>1000000</bundleVersion>  
	<datastorePrincipal>root</datastorePrincipal>  
	<hostIp>192.168.1.200</hostIp>  
	<hostKey>52137432-cb9e-05d5-3bbf-001ffd2baa57</hostKey>  
	<hostPort>443</hostPort>  
	<licenseExpiryNotificationThreshold>15</licenseExpiryNotificationThreshold>  
	<memoryCheckerTimeInSecs>30</memoryCheckerTimeInSecs>  
	<serverIp>192.168.1.2</serverIp>  
	<serverPort>902</serverPort>  
	</vpxa>  
	

with:

	  
	<vpxa>  
	</vpxa>  
	

essentially removing everything between:

	
	
	and
	
	

- restart the management agents (other ways to do this in ESX and ESXi are shown in <a title="Restarting the Management agents on an ESX or ESXi Server" href="http://kb.vmware.com/kb/1003490" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1003490']);" target="_blank">VMware KB 1003490 &#8211; Restarting the Management agents on an ESX or ESXi Server</a>, but what I show below is for an ESXi host:

	  
	~ # /sbin/services.sh restart  
	

- Proceed with restore of vCenter server from VDR to the host that was managed by that very vCenter

**NOTE:** Prior to booting up vCenter again after the restore, I highly recommend you restore vpxa.cfg:

	  
	~ # cp /etc/vmware/vpxa/vpxa.cfg.bak /etc/vmware/vpxa/vpxa.cfg  
	

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing vCenter 5.5 fails with Invalid Credentials" href="http://virtuallyhyper.com/2013/10/installing-vcenter-fails-invalid-credentials/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/10/installing-vcenter-fails-invalid-credentials/']);" rel="bookmark">Installing vCenter 5.5 fails with Invalid Credentials</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Lowering the Memory Usage on the vCenter Appliance" href="http://virtuallyhyper.com/2013/04/lowering-the-memory-usage-on-the-vcenter-appliance/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/lowering-the-memory-usage-on-the-vcenter-appliance/']);" rel="bookmark">Lowering the Memory Usage on the vCenter Appliance</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="vCenter 5.1 Service Fails to Start" href="http://virtuallyhyper.com/2013/02/vcenter-5-1-service-fails-to-start/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/vcenter-5-1-service-fails-to-start/']);" rel="bookmark">vCenter 5.1 Service Fails to Start</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VDR Appliance Fails to Complete Integrity Check and Fails to Backup Certain VMs" href="http://virtuallyhyper.com/2012/09/vdr-appliance-fails-to-complete-integrity-check-and-fails-to-backup-certain-vms/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vdr-appliance-fails-to-complete-integrity-check-and-fails-to-backup-certain-vms/']);" rel="bookmark">VDR Appliance Fails to Complete Integrity Check and Fails to Backup Certain VMs</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESXi Host Shows as Disconnected from vCenter due to Heap Depletion" href="http://virtuallyhyper.com/2012/08/esxi-host-shows-as-disconnected-from-vcenter-due-to-heap-depletion/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/esxi-host-shows-as-disconnected-from-vcenter-due-to-heap-depletion/']);" rel="bookmark">ESXi Host Shows as Disconnected from vCenter due to Heap Depletion</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/restore-vcenter-from-vdr-onto-a-host-being-managed-by-vcenter/" title=" Restore vCenter from VDR onto a Host Being Managed by vCenter" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:restore,vcenter,vdr,virtualcenter,vmware data recovery,vpxa,blog;button:compact;">I recently had a very interesting issue. An ESXi host was showing up as disconnected in vCenter, however going directly to the host worked fine. Trying to reconnect the host...</a>
</p>