---
title: Reclaim Space in a VM on Thin or Thick VMDKs
author: Karim Elatov
layout: post
permalink: /2012/03/reclaim-space-in-a-vm-on-thin-or-thick-vmdks/
dsq_thread_id:
  - 1404703834
categories:
  - OS
  - Storage
  - VMware
tags:
  - sdelete
  - space reclam
  - thick provisioning
  - thin provisioning
  - vmdk
  - zerofree
---
# Reclaim Space in a VM on thin or thick VMDKs

There are many different scenarios where this comes into play, and there many different ways to get the desired results.

## Scenario 1: Reclaim unused space from a thick disk

**Solution 1:**

Storage vMotion the VM to another datastore and convert it to thin. See the following link on how to do that: [Blocksize Impact](http://www.thelowercasew.com/reclaiming-disk-space-with-storage-vmotion-and-thin-provisioning).

**Solution 2:**
Use VMware Converter and do a V2V of the VM and choose Thin for the destination disk type.

## Scenario 2: Reclaim previously used space from a thick disk

### WINDOWS

**Solution 1:**

When this happens we need to reclaim the deleted space using sdelete, which will just zero out the deleted space. The page '[Reclaiming disk Space with Storage vMotion and Thin Provisioning](http://www.thelowercasew.com/reclaiming-disk-space-with-storage-vmotion-and-thin-provisioning)' talks about how to do that. So first zero out the deleted space with sdelete and then use storage vMotion to convert the disk to thin.

**Solution 2:**
You can also use the shrink disk from vmware tools to reclaim the delete space. More information can be seen here '[Storage VMotion and moving to a Thin Provisioned disk](http://www.yellow-bricks.com/2009/07/31/storage-vmotion-and-moving-to-a-thin-provisioned-disk/)'.

**Solution 3:**
Use VMware Converter and do a P2V of the VM. [The post 'P2V with VMware Converter Standalone 5 and sync feature](http://www.vi-tips.com/2011/11/p2v-with-vmware-converter-standalone-5.html)' has a good video on how to do that. Make sure you choose thin for the disk type.

### LINUX

**Solution 1:**

It's almost the same as the "Windows Scenario" but instead of using **sdelete** you can use **zerofree**. So install **zerofree**:

##### Fedora/CentOs/RedHat

	[root@rac1 ~]$ yum install zerofree
	updates/metalink | 12 kB 00:00
	updates | 4.5 kB 00:00
	updates/primary_db | 4.3 MB 00:21
	Setting up Install Process
	Resolving Dependencies
	Running transaction check
	Package zerofree.i686 0:1.0.1-8.fc15 will be installed
	Finished Dependency Resolution

	Dependencies Resolved

	================================================================================
	Package Arch Version Repository Size
	================================================================================
	Installing:
	zerofree i686 1.0.1-8.fc15 fedora 20 k

	Transaction Summary
	================================================================================
	Install 1 Package

	Total download size: 20 k
	Installed size: 20 k
	Is this ok [y/N]: y
	Downloading Packages:
	zerofree-1.0.1-8.fc15.i686.rpm | 20 kB 00:00
	Running Transaction Check
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	Installing : zerofree-1.0.1-8.fc15.i686 1/1

	Installed:
	zerofree.i686 0:1.0.1-8.fc15

	Complete!

##### For Debian/Ubuntu:

	[root@rac1 ~]$ apt-get install zerofree
	Reading package lists... Done
	Building dependency tree
	Reading state information... Done
	The following NEW packages will be installed:
	zerofree
	0 upgraded, 1 newly installed, 0 to remove and 17 not upgraded.
	Need to get 7,272 B of archives.
	After this operation, 61.4 kB of additional disk space will be used.
	Get:1 http://ubuntu.cs.utah.edu/ubuntu/ oneiric/universe zerofree amd64 1.0.1-2ubuntu1 [7,272 B]
	Fetched 7,272 B in 0s (41.5 kB/s)
	Selecting previously deselected package zerofree.
	(Reading database ... 22748 files and directories currently installed.)
	Unpacking zerofree (from .../zerofree_1.0.1-2ubuntu1_amd64.deb) ...
	Processing triggers for man-db ...
	Setting up zerofree (1.0.1-2ubuntu1) ...

Then you need to mount the partition as read-only and run zerofree on it. If you need perform this on your OS/root partition, then power off your VM and attach the OS disk to another Linux VM. Here is how it looks like:

	[root@rac1 ~]$ mount -o remount,ro /dev/mapper/test-lvol0
	[root@rac1 ~]$ zerofree -v /dev/mapper/test-lvol0
	1106/485301/512000

Then Storage vMotion the VM to another datastore with another block size converting the disk to thin.

**NOTE:** Instead of using **rm** to delete files, you can use **shred** and then you wouldn't need to zero out deleted space.

#### **Solution 2:**

Use VMware Converter and do a P2V of the VM. The post [P2V with VMware Converter Standalone 5 and sync feature](http://www.vi-tips.com/2011/11/p2v-with-vmware-converter-standalone-5.html) has a good video on how to do that. Make sure you choose thin for the disk type.

## Scenario 3: Reclaim previously used space from thin disks

**Solution 1:**

If you using windows, use sDelete to reclaim the space and then SvMotion to keep the disk format. If using Linux, use zerofree to reclaim the space and then SvMotion to another datastore with another block size keeping the disk format

**Solution 2:**
Use VMware Converter and P2V the VM. Ensure you use the thin disk.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>

  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="What is the difference between a Redo log and a Snapshot?" href="http://virtuallyhyper.com/2012/09/what-is-the-difference-between-a-redo-log-and-a-snapshot/" rel="bookmark">What is the difference between a Redo log and a Snapshot?</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Advanced Snapshot Troubleshooting: Missing VMDK Descriptors" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-missing-vmdk-descriptors/" rel="bookmark">Advanced Snapshot Troubleshooting: Missing VMDK Descriptors</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title=""Thin on Thin" With VMware Thin Provisioned Disks and EMC Symmetrix Virtual Provisioning" href="http://virtuallyhyper.com/2012/04/thin-on-thin-with-vmware-thin-provisioned-disks-and-emc-symmetrix-virtual-provisioning/" rel="bookmark">"Thin on Thin" With VMware Thin Provisioned Disks and EMC Symmetrix Virtual Provisioning</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Accidently Changed the Disk Size when the VM was Running on Snapshots" href="http://virtuallyhyper.com/2012/04/accidently-changed-the-disk-size-when-the-vm-was-running-on-snapshots/" rel="bookmark">Accidently Changed the Disk Size when the VM was Running on Snapshots</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Advanced Snapshot Troubleshooting: Incorrect VMDK Geometry" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-incorrect-vmdk-geometry/" rel="bookmark">Advanced Snapshot Troubleshooting: Incorrect VMDK Geometry</a>
    </li>
  </ul>
</div>
