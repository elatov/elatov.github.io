---
title: Register All VMs on a Datastore to an ESX/ESXi host
author: Jarret Lavallee
layout: post
permalink: /2012/03/register-all-vms-on-a-datastore-to-an-esxesxi-host/
dsq_thread_id:
  - 1411095852
categories:
  - VMware
  - vTip
tags:
  - cli
  - register vm
  - vtip
---
### ESXi

Register all VMs on a single datastore.

<pre>~ # find /vmfs/volumes/&lt;datastorename&gt;/ -maxdepth 2 -name '*.vmx' -exec vim-cmd solo/registervm "{}" \;</pre>

Register all VMs on all datastores.

<pre>~ # find /vmfs/volumes/ -maxdepth 3 -name '*.vmx' -exec vim-cmd solo/registervm "{}" \;</pre>

### ESX

Register all VMs on a single datastore.

<pre>~ # find /vmfs/volumes/&lt;datastorename&gt;/ -maxdepth 2 -name '*.vmx' -exec vmware-cmd -s register "{}" \;</pre>

Register all VMs on all datastores.

<pre>~ # find /vmfs/volumes/ -maxdepth 3 -name '*.vmx' -exec vmware-cmd -s register "{}" \;</pre>

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Decrease Initial Replication Bandwidth and Time with vSphere Replication" href="http://virtuallyhyper.com/2012/08/save-initial-replication-bandwidth-with-vsphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/save-initial-replication-bandwidth-with-vsphere-replication/']);" rel="bookmark">Decrease Initial Replication Bandwidth and Time with vSphere Replication</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Resizing a VMDK that is protected by vSphere Replication" href="http://virtuallyhyper.com/2012/08/resizing-a-vmdk-that-is-protected-by-vsphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/resizing-a-vmdk-that-is-protected-by-vsphere-replication/']);" rel="bookmark">Resizing a VMDK that is protected by vSphere Replication</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Adding a Physical Disk as a Mirror to an Existing Zpool" href="http://virtuallyhyper.com/2012/08/adding-a-disk-as-a-mirror-to-an-existing-zpool/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/adding-a-disk-as-a-mirror-to-an-existing-zpool/']);" rel="bookmark">Adding a Physical Disk as a Mirror to an Existing Zpool</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Cloning a VM from the Command Line" href="http://virtuallyhyper.com/2012/04/cloning-a-vm-from-the-command-line/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/cloning-a-vm-from-the-command-line/']);" rel="bookmark">Cloning a VM from the Command Line</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VMW_PSP_FIXED vs. VMW_PSP_FIXED_AP" href="http://virtuallyhyper.com/2012/04/vmw_psp_fixed-vs-vmw_psp_fixed_ap/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vmw_psp_fixed-vs-vmw_psp_fixed_ap/']);" rel="bookmark">VMW_PSP_FIXED vs. VMW_PSP_FIXED_AP</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/register-all-vms-on-a-datastore-to-an-esxesxi-host/" title=" Register All VMs on a Datastore to an ESX/ESXi host" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:cli,register vm,vtip,blog;button:compact;">Recently a vendor asked me what the difference between VMW_PSP_FIXED and VMW_PSP_FIXED_AP is. Since VMW_PSP_FIXED_AP is not specifically listed on the HCL, the vendor was confused on why the SATP...</a>
</p>