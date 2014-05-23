---
title: Datastores show up as Snapshots after a host reboot with SRM installed
author: Karim Elatov
layout: post
permalink: /2012/04/datastores-show-up-as-snapshots-after-a-host-reboot-with-srm-installed/
dsq_thread_id:
  - 1406568646
categories:
  - Storage
  - VMware
tags:
  - EnableResignature
  - logs
  - Resignature
  - Snapshot LUN
  - srm
---
Today I ran into an interesting issue. A customer called in saying that his VMs are down and some of his Datastores are showing up as snapshots. Looking at the Datastore View from vCenter, we saw the following:

![datastore_snapshots_1](https://github.com/elatov/uploads/raw/master/2012/04/datastore_snapshots_1.png)

The original datastores showed up as Inactive in the same view and looked exactly as descibed in [KB 9453805](http://kb.vmware.com/kb/9453805). To get all the VMs up and running, we had to follow the intructions laid out in the above KB.

1.  <span style="line-height: 22px;">Click on the Inactive datastore and select the Virtual Machine Tab</span>
2.  <span style="line-height: 22px;">Power Off all the VMs listed in Virtual Machine Tab (after doing this, the VMs showed up inactive as well)</span>
3.  <span style="line-height: 22px;">Remove all the powered off VMs from Inventory (after removing the last VM from inventory, the inactive datastore will disappear from this view)</span>
4.  <span style="line-height: 22px;">Rename the snapshot'ed datastore to it's original name</span>
5.  <span style="line-height: 22px;">Re-register all the VMs back from this datastore back into inventory</span>
6.  <span style="line-height: 22px;">Repeat for all the "inactive" datastores</span>

We wanted to find out why this happened so the customer sent me the logs from all the hosts in the cluster. I wrote down one the datastore names that had the issue and from the logs I found what the naa of that datastores was. I then searched for that naa across all the logs:


	elatov@host ~$ find . -name 'vmkernel*' -exec grep 'naa.xxx' {} \;
	Mar 28 14:26:11 esx_host vmkernel: 259:19:17:51.738 cpu0:4110)LVM: 7404: Device naa.xxx:1 detected to be a snapshot:
	Mar 28 14:26:11 esx_host vmkernel: 259:19:17:51.738 cpu2:4110)LVM: 2710: Device naa.xxx:1 is detected as being in volume 497924f8-0ba43178-cffe-001517515780 (0x417f80077808)


And I saw the same logs across all the hosts. This LUN was showing up as snapshots, [KB 1011385](http://kb.vmware.com/kb/1011385) talks about how LUN snapshots are detected. I then wanted to see when the LUNs were resignatured (since the customer said they had not done so themselves). And I saw the following in the logs:


	elatov@host$ find . -name 'vmkernel*' -exec grep -i 'resig' {} \;
	Mar 28 15:26:29 esx_host vmkernel: 148:01:06:09.203 cpu16:4127)Vol3: 871: Begin resignaturing volume label: snap-6104d589-xxxx, uuid: 4f73356a-32ea5b26-5943-0015178085e8
	Mar 28 15:26:29 esx_host vmkernel: 148:01:06:09.353 cpu9:4127)Vol3: 952: End resignaturing volume label: snap-44d69109-xxx, uuid: 4f7373f5-6cb5476a-4156-842b2b5eee22
	Mar 28 15:26:25 esx_host vmkernel: 217:01:40:33.156 cpu9:4126)LVM: 4893: Snapshot LV <snap-634ad2b0-xxxx> successfully resignatured


Only one host was resignaturing the LUNs that were showing up as snapshots. I then wanted to check if the *EnableResignature* option has been enabled and I saw the following:


	elatov@host ~$ grep EnableResignature etc/vmware/esx.conf
	/adv/LVM/EnableResignature = "1"


That option was enabled, [KB 2010051](http://kb.vmware.com/kb/2010051) talks about what that option does:

> Setting the LVM.enableResignature flag on ESX hosts is a host-wide operation. If this flag is set to 1, all snapshot LUNs that are visible to the ESX host and can be resignatured, are resignatured during the host rescan or upon the next host reboot.

I asked the customer if anything had happened with that host and they had mentioned that the host been recently rebooted, and shortly after the reboot the issues started happening. So that answered the first question as to why we saw snapshot'ed datastores. Now the second question was, why was the *EnableResignature* option set? I asked the customer if they had introduced any new software to their environment, and they had recently installed SRM and had done a failover and failback. When doing an SRM failover that option is automatically set. More information regarding SRM setting the *EnableResignature* option can be seen at [KB 2010051](http://kb.vmware.com/kb/2010051)

Now the last question was why are we were seeing snapshot'ed LUNs in the environment. The answer was quite simple, the customer was using an EMC Symmetrix DMX SAN which had two different FAs presenting the same LUN with a different LUN ID. More information can be found in [KB 6482648](http://kb.vmware.com/kb/6482648) as to why that will cause issues. After I had forwarded that KB to the customer, he remembered that he had issues in the past with LUN presentation. He also mentioned that they are actually moving to a different SAN (EMC Symmetrix VMAX) and they will ensure that LUNs are presented properly from the new SAN to prevent the LUNs from showing up as snapshots.

All in all, we ran into 3 issues:

1.  <span style="line-height: 22px;">LUNs showing up as snapshots (will present LUNs in an appropriate manner to prevent that)</span>
2.  <span style="line-height: 22px;">LUNs were auto resignatured after a host reboot (had the *EnableResignature* option enabled)</span>
3.  <span style="line-height: 22px;">The *EnableResignature* Option is set automatically (when Using SRM this is expected behavior, customer will change option manually after an SRM failover)</span>

### Related Posts

- [Enabling disk.EnableUUID on a Nested ESX Host in Workstation](http://virtuallyhyper.com/2012/08/enabling-disk-enableuuid-on-a-nested-esx-host-in-workstation/)

