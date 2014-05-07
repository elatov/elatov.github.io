---
title: SRM 5 Enable Array Pair Hangs at 46%
author: Jarret Lavallee
layout: post
permalink: /2012/03/log-review-srm-5-enable-array-pair-hangs-at-46/
dsq_thread_id:
  - 1413958951
categories:
  - SRM
  - Storage
  - VMware
tags:
  - array pair
  - dr
  - logs
  - sra
  - srm
---
This article is the first in a series that I plan on doing. Often times, it is difficult to decipher logs and it takes a long time to start to get a good feel for logs across different products. In this series, I will do a log review for a specific problem showing the process and logical steps needed to resolve the issue. This one is about <a href="http://www.vmware.com/products/site-recovery-manager/overview.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/products/site-recovery-manager/overview.html']);" target="_blank">SRM</a> array <a href="http://www.vmware.com/pdf/srm_admin_5_0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/srm_admin_5_0.pdf']);" target="_blank">pairing</a>. SRM is a product designed to fail VMs over to a Disaster Recovery site in the case of a disaster on the protected site.

I was recently asked to look at an issue where the pair array operation in SRM 5 was hanging at 46%. The task would stay there until both vCenter servers were restarted. The first place to identify these issues is to look at the logs on both the Protected and Disaster Recovery (DR) sites for the time frame of hanging process. The logs will give clues to what is actually occurring at that time.

For this issue, we start looking at the <a title="SRM log Locations" href="http://kb.vmware.com/kb/1021802" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021802']);" target="_blank">Protected site logs</a>. If we follow the sequence of events on the Protected Site, we will get the full idea of what is going on.

Let&#8217;s start where the Enable Array Pair is called. Since the issue occurs when the user selects the Enable Array Pair on the Protect site, we will look in that log file. The logs below indicate the start of the array pairing. It lists the two arrays that are to be Paired and what array manager called the array pairing.

[xml]2012-03-09T11:04:24.766+02:00 [06136 verbose 'Storage' opID=1F444FAC-0000002B] Posting event to VC: (dr.eventEx.StorageArrayPairDiscoveredEvent) {  
&#8211;>; dynamicType = ,  
&#8211;>; arrayManager = &#8216;dr.storage.ArrayManager:storage-arraymanager-33011&#8242;,  
&#8211;>; arrayManagerName = "Production SRA",  
&#8211;>; localArrayName = "000292601234",  
&#8211;>; remoteArrayId = "000292602345",  
&#8211;>; }[/xml]

The operation is starting on the Protected site.

[xml]2012-03-09T11:05:53.875+02:00 [06128 info 'Storage' opID=1F444FAC-00000041] Starting &#8216;dr.storage.addReplicatedArrayPair&#8217; operation for arrays &#8217;000292601234&#8242; &#8211; &#8217;000292602345&#8242;[/xml]

The DR site is called to do the array pairing as well.

[xml]2012-03-09T11:05:53.875+02:00 [06128 info 'MultiSiteOperationManager' opID=1F444FAC-00000041] Starting multi-site operation &#8216;dr.storage.addReplicatedArrayPair&#8217;, tag &#8221;  
2012-03-09T11:05:53.875+02:00 [06128 verbose 'MultiSiteOperationManager' opID=1F444FAC-00000041] Multi-site operation coordinator &#8216;coordinator-33030&#8242; created  
2012-03-09T11:05:53.875+02:00 [06128 verbose 'PropertyProvider' opID=1F444FAC-00000041] RecordOp ADD: coordinator["coordinator-33030"], MultiSiteOperationManager  
2012-03-09T11:05:53.875+02:00 [06128 info 'DrTask' opID=1F444FAC-00000041] Starting task &#8216;dr.storage.ArrayManager.addArrayPair5&#8242;  
2012-03-09T11:05:53.875+02:00 [06128 verbose 'PropertyProvider' opID=1F444FAC-00000041] RecordOp ASSIGN: info.progress, dr.storage.ArrayManager.addArrayPair5  
2012-03-09T11:05:53.875+02:00 [06132 verbose 'MultiSiteOperationManager' opID=1F444FAC-00000041] Cohort &#8216;cohort-33031&#8242; created associated with coordinator &#8216;coordinator-33030&#8242; on site &#8217;5a952a3c-c71e-48d7-bc32-f1231c8ecf7a&#8217;  
2012-03-09T11:05:53.875+02:00 [06132 verbose 'PropertyProvider' opID=1F444FAC-00000041] RecordOp ADD: cohort["cohort-33031"], MultiSiteOperationManager[/xml]

vCenter is notified.

[xml]2012-03-09T11:05:53.875+02:00 [06132 verbose 'DrTask' opID=1F444FAC-00000041] Starting VC task &#8216;com.vmware.vcDr.dr.storage.ArrayManager.addArrayPair&#8217;  
2012-03-09T11:05:53.875+02:00 [05900 verbose 'DrTask' opID=1F444FAC-00000041] Starting VC task &#8216;com.vmware.vcDr.dr.storage.ArrayManager.addArrayPair&#8217;[/xml]

The Protected Site created the pair and is waiting for the DR site.

[xml]2012-03-09T11:05:53.891+02:00 [02696 info 'Storage' ctxID=2381f90b opID=1F444FAC-00000041] Preparing dr.storage.addReplicatedArrayPair operation  
2012-03-09T11:05:53.891+02:00 [02696 verbose 'Storage' ctxID=2381f90b opID=1F444FAC-00000041] Acquiring operation lock for array manager &#8216;storage-arraymanager-33011&#8242;  
2012-03-09T11:05:53.891+02:00 [02696 verbose 'PerformanceMonitor' ctxID=2381f90b opID=1F444FAC-00000041] Performance monitor Token 0 of lock PersistableRWLock-33012 begin.  
2012-03-09T11:05:53.891+02:00 [02696 verbose 'PersistableRWLock' ctxID=2381f90b opID=1F444FAC-00000041] Lock PersistableRWLock-33012&#8242; obtained for Read  
2012-03-09T11:05:53.922+02:00 [05672 verbose 'DrTask' opID=1F444FAC-00000041] Created VC task &#8216;com.vmware.vcDr.dr.storage.ArrayManager.addArrayPair:task-5410&#8242;  
2012-03-09T11:05:53.922+02:00 [03024 info 'Storage' opID=1F444FAC-00000041] Prepared 2PC operation addReplicatedArrayPair for array pair &#8217;000292602338&#8242; &#8211; &#8217;000292602336&#8242;: &#8216;array-pair-33032&#8242;  
2012-03-09T11:05:53.938+02:00 [01936 verbose 'DrTask' opID=1F444FAC-00000041] Created VC task &#8216;com.vmware.vcDr.dr.storage.ArrayManager.addArrayPair:task-147276&#8242;  
2012-03-09T11:05:53.953+02:00 [03024 info 'Storage' opID=1F444FAC-00000041] Completed prepare phase of dr.storage.addReplicatedArrayPair operation for arrays &#8217;000292602338&#8242; -> &#8217;000292602336&#8242; and SRA &#8216;FD3D3A04-3DFB-4988-8B99-9A1292A2DD8B&#8217;: &#8216;array-pair-33032&#8242;[/xml]

Since the Protected site is pairing the arrays and waiting for the DR site to return, we have to look at the DR site. Let&#8217;s take a look at the sequence of events on the DR site. The logs below show the beginning of the pairing as we saw on the Protected site.

[xml]2012-03-09T11:05:31.842+02:00 [05828 verbose 'Storage' opID=6D8995D1-00000012] Posting event to VC: (dr.eventEx.StorageArrayPairDiscoveredEvent) {  
&#8211;>; dynamicType = ,  
&#8211;>; arrayManager = &#8216;dr.storage.ArrayManager:storage-arraymanager-21005&#8242;,  
&#8211;>; arrayManagerName = "Disaster SRA",  
&#8211;>; localArrayName = "000292602345",  
&#8211;>; remoteArrayId = "000292601234",  
&#8211;>; }[/xml]

We see the cohort made, so that we can work with the Protected site.

[xml]2012-03-09T11:05:54.013+02:00 [03276 info 'MultiSiteOperationManager' opID=1F444FAC-00000041] Creating cohort for remote operation &#8216;dr.storage.addReplicatedArrayPair&#8217; on site &#8217;5a952a3c-c71e-48d7-bc32-f1231c8ecf7a&#8217; with coordinator &#8216;coordinator-33030&#8242;  
2012-03-09T11:05:54.013+02:00 [03276 verbose 'MultiSiteOperationManager' opID=1F444FAC-00000041] Cohort &#8216;cohort-21024&#8242; created associated with coordinator &#8216;coordinator-33030&#8242; on site &#8217;5a952a3c-c71e-48d7-bc32-f1231c8ecf7a&#8217;  
2012-03-09T11:05:54.013+02:00 [03276 verbose 'PropertyProvider' opID=1F444FAC-00000041] RecordOp ADD: cohort["cohort-21024"], MultiSiteOperationManager  
2012-03-09T11:05:54.013+02:00 \[03276 verbose 'RemoteDR' opID=1F444FAC-00000041\] \[PCM\] Using token &#8217;5&#8242; for pending filter creation[/xml]

Then we see the actual error that is causing this operation to hang. The error is that we do not have permission to complete an operation. This message is actually an indication that the user on the DR site does not have enough permission to do certain operations on the Protected site. The user that does not have enough permissions is the user that was provided when connecting both the DR and Protected sites together.

[xml]2012-03-09T11:05:54.029+02:00 [07820 warning 'RemoteDR'] Missing property: commit fault:  
&#8211;>; (vim.fault.NoPermission) {  
&#8211;>; dynamicType = ,  
&#8211;>; faultCause = (vmodl.MethodFault) null,  
&#8211;>; object = &#8216;dr.multiSiteOperation.Coordinator:coordinator-33030&#8242;,  
&#8211;>; privilegeId = "VcDr.Internal.com.vmware.vcDr.InternalAccess",  
&#8211;>; msg = "",  
&#8211;>; }[/xml]

Now that we know that there is a permission problem, we just have to isolate it. I asked the customer to try to pair the arrays again, but this time try to pair it from the DR site. This resulted in a vim.fault.NoPermission error being thrown inside vCenter. It turns out that this error is not being returned to the protected site to fail the command, and it sits there at 46%.

The next thing to check is to have the user in the administrators group for both vCenter servers. This was set up correctly so we went on to vCenter roles. It turns out that the customer had inadvertently put this user into a read-only role on the datacenter. Since the user could log into the Protected site, SRM was able to launch, but could not do anything from the DR site. We removed the user from this role, and we were able to pair the arrays.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Datastores show up as Snapshots after a host reboot with SRM installed" href="http://virtuallyhyper.com/2012/04/datastores-show-up-as-snapshots-after-a-host-reboot-with-srm-installed/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/datastores-show-up-as-snapshots-after-a-host-reboot-with-srm-installed/']);" rel="bookmark">Datastores show up as Snapshots after a host reboot with SRM installed</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/log-review-srm-5-enable-array-pair-hangs-at-46/" title=" SRM 5 Enable Array Pair Hangs at 46%" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:array pair,dr,logs,sra,srm,blog;button:compact;">Today I ran into an interesting issue. A customer called in saying that his VMs are down and some of his Datastores are showing up as snapshots. Looking at the...</a>
</p>