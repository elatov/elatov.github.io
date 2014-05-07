---
title: Determine vCenter IP from ESX host via CLI
author: Joe Chan
layout: post
permalink: /2012/03/determine-vcenter-ip-from-esx-host-via-cli/
HMMultipostMU_children:
  - 's:15:"a:1:{i:1;i:15;}";'
dsq_thread_id:
  - 1410225993
categories:
  - VMware
  - vTip
tags:
  - cli
---
ESXi 5  

	~ # grep serverIp /etc/vmware/vpxa/vpxa.cfg  
	10.131.11.183  

ESX and ESXi 4.x and prior  

	~ # grep serverIp /etc/opt/vmware/vpxa/vpxa.cfg  
	10.131.11.183  

Note: The location of the vpxa configuration directory changed from /etc/**opt**/vmware/vpxa to /etc/vmware/vpxa in ESXi 5.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="How to Update the AWS CLI Tools (Linux)" href="http://virtuallyhyper.com/2013/04/how-to-update-the-aws-cli-tools-linux/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/how-to-update-the-aws-cli-tools-linux/']);" rel="bookmark">How to Update the AWS CLI Tools (Linux)</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" href="http://virtuallyhyper.com/2012/08/using-a-custom-ca-with-vsphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/using-a-custom-ca-with-vsphere-replication/']);" rel="bookmark">Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Register All VMs on a Datastore to an ESX/ESXi host" href="http://virtuallyhyper.com/2012/03/register-all-vms-on-a-datastore-to-an-esxesxi-host/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/register-all-vms-on-a-datastore-to-an-esxesxi-host/']);" rel="bookmark">Register All VMs on a Datastore to an ESX/ESXi host</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/determine-vcenter-ip-from-esx-host-via-cli/" title=" Determine vCenter IP from ESX host via CLI" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:cli,blog;button:compact;">ESXi Register all VMs on a single datastore. ~ # find /vmfs/volumes/<datastorename>/ -maxdepth 2 -name '*.vmx' -exec vim-cmd solo/registervm "{}" \; Register all VMs on all datastores. ~ # find...</a>
</p>
