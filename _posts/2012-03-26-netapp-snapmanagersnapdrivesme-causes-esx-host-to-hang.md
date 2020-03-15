---
published: true
title: NetApp SnapManager/SnapDrive/SME Causes ESX Host to Hang
author: Karim Elatov
layout: post
categories: [ storage, vmware ]
tags: [vm_snapshots, vss, netapp]
---
I had a customer use the following setup/versioning:

{:.kt}
| VMware      | NetApp            | Windows                |
|-------------|-------------------|------------------------|
| ESXi 4.1U1  | Data OnTap 8.01P5 | W2K8 ENT. SP2 64bit    |
| vCenter 4.1 | SME 6.0P2         | OS is vmdk             |
|             | SnapDrive 6.3P2   | Exchange Data RDM LUNs |

That is a lot of components, so let's break them down. NetApp SnapManager for Virtual Infrastructure (SMVI) integrates with VMware vCenter to automate backups of VMs. NetApp describes it best:

> SnapManager® for Virtual Infrastructure works with VMware vCenter, automating and simplifying management of backup and restore operations.

Here is link the main page of SVMI, [NetApp SnapManager for Virtual Infrastructure Demo](http://www.netapp.com/us/products/management-software/vsc/snapmanager-virtual.html). Next we have SnapDrive. SnapDrive is an application that runs from within an OS and allows you to manage (create,delete, resize, and ...etc) LUNs for a NetApp Filer. As always NetApp describes it best:

> Eliminate the time-consuming and error-prone manual management of NetApp storage with our protocol-agnostic solution. Automate storage provisioning tasks and simplify the process of taking error-free, host-consistent data Snapshot copies. Run SnapDrive on your Windows-based hosts in either a physical or virtual environment and integrate it with your Microsoft Cluster Server and Windows failover clustering

Here is main page of SnapDrive, [Connect & Create Luns with SnapDrive](http://www.netapp.com/us/products/management-software/snapdrive-windows.html). SnapDrive also allows you to take array level snapshots of the LUNs presented to the OS.

Lastly, we have SnapManager for Exchange (SME). We know how IO intensive Exchange can be, in order to perform backups of an Exchange Server, we need to freeze the IO for a little bit and then take a backup, so no disruption to Exchange Server occurs and we can have an application level consistent backup. That is exactly for SME does. Here is NetApp's description of the product:

> Simplify your application data management with SnapManager for Microsoft Exchange Server. You can automate complex, manual, and time-consuming processes associated with the backup, recovery, and verification of Exchange Server databases while reducing messaging storage costs, improving manageability, and increasing availability.

Here is the link for to the NetApp webpage, [napManager 2.0 for Virtual Infrastructure Best Practices](http://www.netapp.com/us/products/management-software/snapmanager-exchange.html)):

> *   SMVI, working through the VMware guest VSS stack, provides application-consistent backup and recovery for applications that have VSS writers and store their data on virtual disks (VMDKs). Recovery, in this scenario, is at the full VM level only.
> *   SnapDrive® and application-specific SnapManager products such as SnapManager for Exchange (SME) and SnapManager for SQL (SMSQL) running in the guest OS, provide application consistent backup and fine-grained recovery for applications whose data is stored using Microsoft iSCSI Software Initiator LUNs or RDMs.

But both options can be used together, from the same white paper we see this:

> Today, both solutions can be used together—SMVI to back up/recover the system data and a SnapDrive and application SnapManager combination to back up/recover the mission-critical application data—to get the desired level of data protection required. Customers using the two-solution approach need to be aware of a few configuration considerations:
>
> *   SMVI supports backup and recovery of virtual disks in VMFS and NFS datastores.
> *   The application SnapManager products support backup and recovery of applications whose data is stored on RDM LUNs or Microsoft iSCSI Software Initiator LUNs mapped to the virtual machine.
> *   By default, SMVI uses quiesced VMware snapshots of virtual machines to capture the consistent state of the virtual machines prior to making a Data ONTAP Snapshot copy of the backing storage.
>
> According to VMware KB article #1009073, VMware Tools are unable to create quiesced snapshots of virtual machines that have NPIV RDM LUNs or Microsoft iSCSI Software Initiator LUNs mapped to them (this often results in timeout errors during snapshot creation). Therefore, customers using the Microsoft iSCSI Software Initiator in the guest and running SMVI with VMware snapshots turned on, which is not recommended, are at high risk of experiencing SMVI backup failures due to snapshot timeouts caused by the presence of Microsoft iSCSI Software Initiator LUNs mapped to the virtual machines.
>
> VMware’s general recommendation is to disable both VSS components and the sync driver in VMware Tools (which translates to turning off VMware snapshots for any SMVI backup jobs that include virtual machines mapped with Microsoft iSCSI Software Initiator LUNs) in environments that include both Microsoft iSCSI Software Initiator LUNs in the VM and SMVI, thereby reducing the consistency level of a virtual machine backup to point-in-time consistency. However, by using SDW/SM to back up the application data on the Microsoft iSCSI Software Initiator LUNs mapped to the virtual machine, the reduction in the data consistency level of the SMVI backup has no effect on the application data.
>
> Another recommendation for these environments is to use physical mode RDM LUNs, instead of Microsoft iSCSI Software Initiator LUNs, when provisioning storage in order to get the maximum protection level from the combined SMVI and SDW/SM solution: guest file system consistency for OS images using VSS-assisted SMVI backups, and application-consistent backups and fine-grained recovery for application data using the SnapManager applications.

A lot of people ran into issue with having two VSS writers ([VMware KB 1029963](https://communities.netapp.com/thread/14067) ). The Snapdrive and RDM issues seem to be fixed with the latest versions of all the products ;) The former seems to still come up and it depends on what your goal is, but that last Netapp community page has a good description of what to try.

If you want to see a good picture of the setup with the OS disks being vmdks and Exchange data disks are RDMs, I would suggest looking over this article, [Running Microsoft Enterprise Applications on VMware vSphere, NetApp Unified Storage, and Cisco Unified Fabric](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/partners/netapp/vmware-running-microsoft-enterprise-applications-on-vsphere-netapp-unified.pdf)

So now to the problem at hand. We had the following setup: used SnapDrive to add RDMs to the Exchange Server. Installed SME on the VM and used option two (from above) to take an application consistent backup with SME (not  VMware VSS-assisted backups). This worked just fine. Now the snapshot process for SMVI is a little different from a regular backup software, this document describes the process, [SnapManager 2.0 for Virtual Infrastructure Best Practices](http://www.redbooks.ibm.com/redbooks/pdfs/sg247867.pdf):

> 1.  A backup is initiated within SMVI.
>     i. Individual VM(s) backup – A VMware snapshot will be created for each virtual machine selected for backup that is powered on at the time of backup.
>     ii. Datastore backup – A VMware snapshot will be created for every virtual machine that is powered on within the datastore that has been selected for backup.
>     iii. Regardless of backup type, virtual machines that are powered off during a backup will be backed up; however no VMware snapshot is required.
> 2.  The VMware snapshot preserves the state of the virtual machine and is used by SMVI during restores to revert the virtual machine back to the backup point-in-time state. VMware snapshots initiated by SMVI capture the entire state of the individual virtual machines,including disk and settings state; however additional steps must be taken to quiesce an application within a virtual machine. Information on application consistency is provided in section 9 of this document. SMVI also gives users the option to disable VMware snapshots and just take a NetApp Snapshot copy on the volume underlying the datastore.
> 3.  Once all the VMware snapshots have completed for a datastore, SMVI initiates a NetApp Snapshot copy on the volume underlying the datastore. The NetApp Snapshot copy is at the volume level regardless of the type of backup selected: individual virtual machine(s) or datastore. During the backup of a virtual machine with VMDKs residing upon multiple datastores, SnapManager for Virtual Infrastructure initiates a NetApp Snapshot on all the underlying volumes. As a result, multiple datastores are displayed within SMVI’s restore window regardless of how many datastores were selected for backup.
> 4.  Upon completion of the NetApp Snapshot copy, SMVI removes the VMware vCenter snapshot to reduce space and performance overhead. Although the vCenter snapshot is removed within vCenter, one VMware snapshot is maintained within the backup for each virtual machine that was in a powered-on state. This snapshot is maintained so it can be used by the restore process to revert the virtual machine to its point-in-time state.
> 5.  Upon completion of the local backup, SnapManager for Virtual Infrastructure updates an existing SnapMirror relationship on the volume underlying the datastore if the SnapMirror option was selected. SnapMirror is discussed in further detail in a later section of this document

Since we are not using VMware snapshots, we are going to utilize the SME VSS snapshots. The workflow of this can be seen in the following article, [ Microsoft Exchange Server 2007 Best Practices Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/tr-4033.pdf), figure 3 has a good description of this. It will basically use NTFS Master File Table to update the hardlinks of the backed up files if the transaction logs are the same directory are the snapshot info directory. Now if the transactions logs and the SnapInfo directory are not in the same directory, then a copy will happen, which in turn would be slower than the former.

Going back to the problem at hand again. The backups were working okay, however when the verification process occurred, the ESX host, which had the Exchange VM, would hang. We moved the VM around and the issue followed the VM which was using the described setup. Now what happens in the verification process. This article talks about it in depth, [SnapManager® 6.0 for Microsoft® Exchange Installation and Administration Guide](https://github.com/elatov/uploads/raw/master/2013/02/SnapManager_602_for_Microsoft_Exchange.pdf). I would first check out the picture on page 41, it has a diagram of how it would work if you had a remote verification server. From the same article here is the description of how it works:

> **How remote verification works**
> SnapManager initiates a backup operation at the primary host, which then contacts the remote verification server. The remote verification server then uses SnapDrive for verification and sends the results back to the primary host. The basic steps of this process are as follows:
>
> 1.  The SnapManager backup with verification (or verification only) is initiated on the primary SnapManager host, which is configured to run verifications on the remote verification server.
> 2.  The primary SnapManager host contacts the remote verification server and initiates the verification job.
> 3.  The remote verification server uses SnapDrive to connect to a LUN backed by a Snapshot copy containing the databases to be verified.
> 4.  The remote verification server performs the database verification on the LUN backed by Snapshot copy.
> 5.  When the remote verification server completes the verification, it sends the results back to the primary SnapManager host.

In our setup we didn't have remote verification, we just did local verification, again from the same article:

> Remote verification is performed using the same mechanisms that are used for local verification, except that the verification is performed on a host that is different from the Exchange server that initiated the backup set.

So we would mount the Snapshot LUN from the NetApp Filer to the same Exchange Server and perform the verification (which is apparently not recommended, because it's so resource intensive). Now during this process I saw the following messages in the vmkernel:

    Mar 1 08:53:36 host.com vmkernel: 2:16:49:12.573 cpu3:4099)ScsiDeviceIO: 1672: Command 0x28 to device "naa.xxxxxxxxxxxxx" failed H:0x0 D:0x2 P:0x0 Valid sense data: 0x6 0x3f 0xe.


Now translating the SCSI Sense Code: **2/0 0x6 0x3f 0xe**, I get the following

    Host       0x0       DID_OK - No error
    Device     0x2       CHECK CONDITION
    Sense Key  0x6       UNIT ATTENTION
    ASC/ASCQ*  0x3f/0xe  REPORTED LUNS DATA HAS CHANGED


*ASC additional sense code*
*ASCQ additional sense code qualifier*

To translate SCSI sense codes this is a pretty good KB for that, [2000609](http://kb.vmware.com/kb/289902). From that KB

> Updates the NMP module to add support to the *PREEMPT_AND_ABORT* service action in the *PERSISTENT RESERVE OUT SCSI* command for passthrough RDMs, which is required by the Symantec clustering software.

**UPDATE**: After applying the above patch the issue was not fixed, but it shed more light to the issue. I got another log bundle and I saw the following in the logs:

    Apr 7 17:37:45 esx_host vmkernel: 17:19:49:38.441 cpu6:53888)UserDump: 1587: Userworld coredump complete.
    Apr 7 17:39:16 esx_host Hostd: [2012-04-07 17:39:16.938 FFCFEE80 warning 'HostsvcPlugin'] Unable to initialize vmkernel ssl information : vim.fault.PlatformConfigFault
    Apr 7 17:41:03 esx_host vmkernel: 17:19:52:55.580 cpu7:4182)BC: 3837: Failed to flush 45 buffers of size 8192 each for object '' 1 4 ed6 0 0 0 0 0 0 0 0 0 0 0: No free memory for file data
    Apr 7 17:41:03 esx_host vmkernel: 17:19:52:55.580 cpu7:4182)BC: 3837: Failed to flush 82 buffers of size 8192 each for object '' 1 4 ed6 0 0 0 0 0 0 0 0 0 0 0: No free memory for file data
    Apr 7 17:41:03 esx_host vmkernel: 17:19:52:55.580 cpu7:4182)BC: 3837: Failed to flush 6 buffers of size 8192 each for object '' 1 4 ed3 0 0 0 0 0 0 0 0 0 0 0: No free memory for file data
    Apr 7 17:41:03 esx_host: 17:19:52:55.580 cpu7:4182)BC: 3837: Failed to flush 3 buffers of size 8192 each for object '' 1 4 ed3 0 0 0 0 0 0 0 0 0 0 0: No free memory for file data
    Apr 7 17:41:03 esx_host vmkernel: 17:19:52:55.582 cpu6:3476319)User: 2428: wantCoreDump : vix-async-pipe -enabled : 1
    Apr 7 17:41:03 esx_host vmkernel: 17:19:52:55.726 cpu6:3476319)UserDump: 1485: Dumping cartel 3476251 (from world 3476319) to file /var/core/hostd-worker-zdump.000 ...


Now looking at hostd logs at the same time, I saw the following:

    Apr 7 17:33:20 esx_host Hostd: [2012-04-07 17:33:20.472 32AE9B90 error 'Statssvc'] Error: 'FileIO error: No space left : /var/lib/vmware/hostd/stats/hostAgentStats.idMap'; while adding stat 'ha-host'-'storagePath-read#fc.2001001b32ae0a80:2101001b32ae0a80-fc.500a09808defa78a:500a09819defa78a-naa.xxx'-ROLLUP_NONE (type:STATTYPE_RATE, id:92156)
    Apr 7 17:33:20 esx_host Hostd: [2012-04-07 17:33:20.492 32AE9B90 error 'App'] Backtrace:
    Apr 7 17:33:20 esx_host Hostd: [00] rip 17c6bbf3
    Apr 7 17:33:20 esx_host Hostd: [01] rip 17afda0e
    Apr 7 17:33:20 esx_host Hostd: [02] rip 17c51291
    Apr 7 17:33:20 esx_host Hostd: [03] rip 17c61d43
    Apr 7 17:33:20 esx_host Hostd: [04] rip 17a9f3c6
    Apr 7 17:33:20 esx_host Hostd: [05] rip 042a2daf
    Apr 7 17:33:20 esx_host Hostd: [06] rip 0426f316
    Apr 7 17:33:20 esx_host Hostd: [07] rip 04272026
    Apr 7 17:33:20 esx_host Hostd: [08] rip 0429bd56
    Apr 7 17:33:20 esx_host Hostd: [09] rip 0429c172
    Apr 7 17:33:20 esx_host Hostd: [10] rip 0429cab8
    Apr 7 17:33:20 esx_host Hostd: [11] rip 039749fc
    Apr 7 17:33:20 esx_host Hostd: [12] rip 041a03d9
    Apr 7 17:33:20 esx_host Hostd: [13] rip 041a0841
    Apr 7 17:33:20 esx_host Hostd: [14] rip 17c89d68
    Apr 7 17:33:20 esx_host Hostd: [15] rip 17c89e44
    Apr 7 17:33:20 esx_host Hostd: [16] rip 17c81baf
    Apr 7 17:33:20 esx_host Hostd: [17] rip 17c845c8
    Apr 7 17:33:20 esx_host Hostd: [18] rip 039749fc
    Apr 7 17:33:20 esx_host Hostd: [19] rip 17c79389
    Apr 7 17:33:20 esx_host Hostd: [20] rip 183634fb
    Apr 7 17:33:20 esx_host Hostd: [21] rip 1914cd1e


There was actually another backtrace right after that one too, but this is the important one. From the vmkernel logs and the top line of the hostd logs it looks like we ran out RAM disk space. So I got on the system and ran **vdf** to check the status of the RAM disk, and I saw the following:

    ~ # vdf -h
    Ramdisk Size Used Available Use% Mounted on
    MAINSYS 32M 21M 10M 68% --
    tmp 192M 60K 191M 0% --
    updatestg 750M 24K 749M 0% --
    hostdstats 166M 166M 0B 100% --


So the **hostdstats** part of the RAM disk has become full. I remembered an old KB ([1005884](http://kb.vmware.com/kb/1005884)) that talked about clearing the hostdstats. So I followed the instructions in the KB:

1.  rm -fr /var/lib/vmware/hostd/stats
2.  services.sh restart

When I did that I ran into another issue, I saw the following on the screen when I ran that:

    [1363748] Begin 'hostd ++min=0,swap,group=hostd /etc/vmware/hostd/config.xml', min-uptime = 60, max-quick-failures = 1, max-total-failures = 1000000
    Vobd started.
    Running lbtd restart
    net-lbt started.
    Running slpd restart
    Error running operation: Error interacting with configuration file /etc/vmware/esx.conf: Failed attempting to lock file.  Another process has locked the file for more than 20 seconds. The process holding the lock is hostd (1363758).  This operation will complete if it is run again after the lock is released.
    Starting slpd
    Running wsman restart
    ..
    ..


After some time, **hostd** did start up fine, but it was still concerning that hostd had issue locking the file. I did some additional research and it looks like the locking issue is fixed in ESXi 5.0U1 and 4.1U2. For 4.1 check out KB [VMware ESXi 5.0 Update 1 Release Notes](http://kb.vmware.com/kb/2001457) have a workaround listed:

> **Updated Manually applying a host profile containing a large configuration might timeout**
> Applying a host profile that contains a large configuration, for example, a very large number of vSwitches and port groups, might timeout if the target host is either not configured or only partially configured. In such cases, the user sees the Cannot apply the host configuration error message in the vSphere Client, although the underlying process on ESXi that is applying the configuration might continue to run.
>
> In addition, syslog.log or other log files might have error messages such as the following message:
>
>     Error interacting with configuration file /etc/vmware/esx.conf: Timeout while waiting for lock, /etc/vmware/esx.conf.LOCK, to be released. Another process has kept this file locked for more than 20 seconds. The process currently holding the lock is hostd-worker(5055). This is likely a temporary condition. Please try your operation again.
>
>
> This error is caused by contention on the system while multiple operations attempt to gather system configuration information while the host profiles apply operation sets configuration. Because of these errors and other timeout-related errors, even after the host profiles apply operation completes on the system, the configuration captured in the host profile might not be fully applied. Checking the host for compliance shows which parts of the configuration failed to apply, and perform an Apply operation to fix those remaining non-compliance issues.

The customer didn't want to update to either and only cared about the **hostdstats** filling up to 100%. So for now as test we will apply the workaround listed above every week and see if that helps out. I will keep you posted :)

**Update**: removing the */var/lib/vmware/hostd/stats/hostAgentStats-20.stats* file and restarting the managements agents, helped to workaround the issue.

