---
title: VMs Losing High Number of Pings When Consolidating Snapshots
author: Karim Elatov
layout: post
permalink: /2012/06/vms-losing-high-number-pings-when-consolidating-snapshots/
categories: ['storage', 'vmware']
tags: ['performance', 'cbt', 'equallogic', 'iometer', 'vm_snapshot', 'unstun_time']
---

I had an interesting issue that took a while to solve. Whenever we consolidated snapshots it would take a while and the VM would lose a high number of pings. Some ping loss is okay and is expected since we are stunning the VM during the commit of the snapshot. More information on snapshot consolidation can be found in VMware KB [1002836](https://knowledge.broadcom.com/external/article?legacyId=1002836).  However an excessive amount of ping loss should not be seen. Looking over the vmware.log file of the VM we saw the following messages:


	2012-03-23T16:22:51.876Z| vcpu-0| Checkpoint_Unstun: vm stopped for 3658889 us


That is the time it took for the VM to unstun. Looking over the history of VM and taking a look at how long some other unstun times looked like, we saw the following:


	$ grep Unstun vmware* | awk '{print $7}' | sort -nr | head
	237087978
	236039834
	206802872
	187750987
	184177029
	183631162
	179726671
	178677816
	177677873
	175575889


It looks like some snapshots took 237 seconds (237087978us) to unstun, that is a pretty long time. I asked the customer to test some other settings while doing a snapshot removal (disable cbt, no vmware tools, and local storage vs shared storage). Here is a table of our results (these are unstun times):


{:.kt}
|||||With VMware Tools||||Without VMware Tools|
|||Without CBT|| With CBT|| Without CBT|| With CBT|
|||-----------||---------||------------||---------|
||No_I/O| I/O| No_I/O| I/O| No_I/O| I/O| No_I/O| I/O|
|SAN|||||||||
|Create_Snapshot| 1| 1| 2| 2| 1| 1| 2| 2|
|Remove_Snapshot| |4| 4| 7| 1| 5| 4| 7|
|Local|||||||||
|Create_Snapshot|||1| 1| 0| 1| 1| 1|
|Remove_Snapshot|| 1| 0| 3| 1| 3| 1| 3|

VMware tools didn't make a difference, CBT did make a difference but that is expected. Doing I/O inside the VM also made a difference, this was expected as well. The most important data point was the fact that with Local storage it was actually working as expected while on the SAN it was not. Next we decided to run IOmeter tests between the two storage types, and here are the results:

{:.kt}
||Test_Type|Read_IOPS|Read_MB|Avg_Read_Resp|Write_IOPs|Write_MB|Avg_Write_Resp|
||---------|---------|-------|-------------|----------|--------|--------------|
|SAN| 4K_100%_Read |6125| 23| 5.22||||
|Local| 4K_100%_Read| 7754| 30| 4.12||||
|SAN |4K_0%_Read||||8258| 32| 3.8|
|Local| 4K_0%_Read|||| 30337| 118|1.05|
|SAN |16K_100%_Read|5214| 81| 6.13||||
|Local| 16K_100%_Read| 21885| 341|1.46||||
|SAN |16K_0%_Read|||| 5100| 79| 6.27|
|Local| 16K_0%_Read|||| 7889| 123| 4.05|
|SAN |32K_100%_Read|3469| 108| 9.22||||
|Local| 32K_100%_Read| 15789| 493| 2.02	||||
|SAN |32K_0%_Read ||||3195| 99| 10.01|
|Local |32K_0%_Read|||| 4054| 126 7.89|


Local Storage was out performing the SAN in every single test. We were using an Equallogic PS4100X Array, so we went ahead and engaged Dell and provided them with the diagnostics from the Array. After analyzing the logs, Dell provided us with the following update:

> After performing a deep analysis on the diags you provided, we have discovered the following. EQL SAN-2 is the group lead and is down to 1.5 % of pool space. EQL SAN-1 currently has 46.4% of free space. We are also not showing any snapshots or replicas on these members. At your earliest convenience, we would like to incorporate the action plan below.
>
> 1.  We would like to do a restart on the grouplead (EQL SAN-2), to fail it over to EQL SAN-1.
> 2.  Once this is completed, then free up any space possible on EQL SAN2.
> 3.  After this, we recommend upgrading the arrays firmware to 5.2.2
> 4.  Also please upgrade ESXi 5.0.0 version to build number 653509.

After we applied all the above changes the snapshot consolidation looked much better. The customer sent me a log bundle after the above changes were applied and I saw the following:


	2012-05-14T13:34:34.351Z| vcpu-0| DISKLIB-CBT : Shutting down change tracking for untracked fid 5277995.
	2012-05-14T13:34:34.351Z| vcpu-0| DISKLIB-CBT : Successfully disconnected CBT node.
	2012-05-14T13:34:34.366Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738354b180373f5105d/VM/VM_1-000002-delta.vmdk" : closed.
	2012-05-14T13:34:34.368Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-flat.vmdk" : closed.
	2012-05-14T13:34:34.377Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-000002-delta.vmdk" : open successful (1041) size = 34992128, hd = 0. Type 8
	2012-05-14T13:34:34.377Z| vcpu-0| DISKLIB-LIB : Resuming change tracking.
	2012-05-14T13:34:34.390Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-000002-delta.vmdk" : closed.
	2012-05-14T13:34:34.412Z| vcpu-0| CPT current = 2, requesting 6
	2012-05-14T13:34:34.412Z| vcpu-0| Checkpoint_Unstun: vm stopped for 4233332 us
	2012-05-14T13:34:34.412Z| vcpu-1| Done Sync monModules(6).
	2012-05-14T13:34:34.412Z| vcpu-0| Done Sync monModules(6).
	2012-05-14T13:34:34.412Z| vcpu-0| CPT: monitor ACKing mode 6


So the snapshot did happen and the unstun took 4 seconds, which was much better than ~230 seconds and is expected with active I/O and Change Block Tracking enabled.

### Related Posts

- [Check if Snapshot Consolidation is Occurring in the Background on an ESX(i) Host](/2012/09/check-if-snapshot-consolidation-is-occurring-in-the-background/)

