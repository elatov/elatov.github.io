---
title: VDR Appliance Fails to Complete Integrity Check and Fails to Backup Certain VMs
author: Karim Elatov
layout: post
permalink: /2012/09/vdr-appliance-fails-to-complete-integrity-check-and-fails-to-backup-certain-vms/
categories: ['storage', 'vmware']
tags: [ 'vss', 'cbt', 'rdm', 'vm_snapshot', 'vdr', 'vhw']
---

I recently ran into an issue with the VMware VDR appliance. The Integrity Check was failing and a VM (the Email Server VM) was failing to successfully back up. First I wanted to figure out why the Integrity Check was failing. Luckily we had two backup jobs and two Dedupe stores. The Backup Jobs were called "Email_Server_Backup_Job" (this backed up to Dedupe_Store_1) and "All_Other_VMs_Backup_Job" (this backed up to Dedupe_Store_2). We disabled both jobs to narrow down the issue. Each Dedup store was a 1TB RDM, which is a supported configuration. From the '[VMware Data Recovery Administration Guide 2.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vmware-data-recovery-administrators-guide-20.pdf)'

> While Data Recovery does not impose limits on deduplication store size, other factors limit deduplication shares. As a result, deduplication stores are limited to:
>
> *   500 GB on CIFS network shares
> *   1 TB on VMDKs and RDMs
>
> ...
>
> **Special Data Recovery Compatibility Considerations**
>
> ...
>
> *   Up to two deduplication stores per backup appliance.

We logged into the VDR appliance and looked under the Reports Tab and we saw the following:

![recatalog_fails_1](https://github.com/elatov/uploads/raw/master/2012/08/recatalog_fails_1.png)

VMware KB [2014249](http://kb.vmware.com/kb/2014249) talks about this:

> This issue has been resolved in VDR 2.0.1

We updated to the latest version of VDR but unfortunately that didn't help out, the issue persisted. I then found this [article](http://sumoomicrosoft.blogspot.com/2012/07/vmware-data-recovery-error-2241.html) online. Here is what they did to fix the issue:

> 1. increase open file limits. edit /etc/security/limits.conf, add these lines to limits.conf:
>
> 		root hard nofile 100000
> 		root soft nofile 100000
>
> Reboot vdr, check if these settings applied.
>
> 	ulimit -a
>
> 2.Create datarecovery.ini file in /var/vmware/datarecovery/
> (/var/vmware/datarecovery/datarecovery.ini)
>
> Add these lines to the datarecovery.ini file:
>
> 	[Options]
> 	DedupeFullIgnoreDataCheck=1
> 	DedupeIncrementalDoDataCheck=1
>
> optional parameter:
> MaxBackupRestoreTasks=1 (prevents other tasks from running, while running integrity check on datastore)
>
> Hope it helps to save your time

The first part of the solution was already in place in VDR 2.0.1, so we didn't have to do that. After adding the lines to the above file (from part 2), the Integrity Check succeeded, however we found some damaged restore points. We followed the instructions in VMware KB [1013387](http://kb.vmware.com/kb/1013387) to clear the damaged restore points and to run another manual Integrity Check.

We then re-enabled the Email_Server_Backup_Job and it started to fail right away and it actually kept leaving VMware snapshots behind. I then wanted to concentrate on the VMware snapshots failing. The first thing I noticed that that the VM was actually on Virtual HW # 4:


    $ egrep 'virtualHW.v|display' Email.vmx
    virtualHW.version = "4"
    displayName = "Email"


Since VDR uses Change Block Tracking (CBT) to efficiently make backups, the VM actually has to be at Virtual HW # 7 to be able to use CBT. From the VDR admin guide:

> For virtual machines created in vSphere 4.0 or later, the Data Recovery appliance creates a quiesced snapshot of the virtual machine during the backup. The backups use the changed block tracking functionality on the ESX/ESXi hosts. For each virtual disk being backed up, it checks for a prior backup of the virtual disk. It uses the change-tracking functionality on ESX/ESXi hosts to obtain the changes since the last backup. The deduplicated store creates a virtual full backup based on the last backup image and applies the changes to it.
>
> **NOTE** These optimizations apply to virtual machines created with hardware version 7 or later, but they do not apply to virtual machines created with VMware products prior to vSphere 4.0. For example, change block tracking is not used with virtual machines created with Virtual Infrastructure 3.5 or earlier. As a result, Virtual machines created with earlier Hardware versions take longer to back up.

Following the instructions laid out in VMware KB [1010675](http://kb.vmware.com/kb/1010675), we updated the virtual HW to version 7, but it didn't help out. I then looked at the *vmware.log* file as the snapshot deletion process was going and I saw the following:


    2012-07-06T21:01:10.891Z| vcpu-0| DISKLIB-CBT : Opening cbt node /vmfs/devices/cbt/88f0572-cbt
    2012-07-06T21:01:10.893Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:10.893Z| vcpu-0| AIOMGR: AIOMgr_OpenWithRetry: Descriptor file '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' locked (try 0)
    2012-07-06T21:01:11.196Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:11.196Z| vcpu-0| AIOMGR: AIOMgr_OpenWithRetry: Descriptor file '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' locked (try 1)
    2012-07-06T21:01:11.498Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:11.498Z| vcpu-0| AIOMGR: AIOMgr_OpenWithRetry: Descriptor file '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' locked (try 2)
    2012-07-06T21:01:11.798Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:11.798Z| vcpu-0| AIOMGR: AIOMgr_OpenWithRetry: Descriptor file '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' locked (try 3)
    2012-07-06T21:01:12.108Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:12.108Z| vcpu-0| AIOMGR: AIOMgr_OpenWithRetry: Descriptor file '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' locked (try 4)
    2012-07-06T21:01:12.410Z| vcpu-0| AIOGNRC: Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk' : Failed to lock the file (400000003) (0x2013).
    2012-07-06T21:01:12.410Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002-delta.vmdk" : failed to open (Failed to lock the file): AIOMgr_Open failed. Type 8
    2012-07-06T21:01:12.410Z| vcpu-0| DISKLIB-LINK : "/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email000002.vmdk" : failed to open (Failed to lock the file).
    2012-07-06T21:01:12.410Z| vcpu-0| DISKLIB-CHAIN : "/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002.vmdk" : failed to open (Failed to lock the file).
    2012-07-06T21:01:12.410Z| vcpu-0| DISKLIB-LIB : Failed to open '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002.vmdk' with flags 0x8 Failed to lock the file (16392).
    2012-07-06T21:01:12.410Z| vcpu-0| SNAPSHOT:Failed to open disk /vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000002.vmdk : Failed to lock the file (16392)
    2012-07-06T21:01:12.411Z| vcpu-0| DISKLIB-CBT : Shutting down change tracking for untracked fid 233964902.
    2012-07-06T21:01:12.412Z| vcpu-0| DISKLIB-CBT : Successfully disconnected CBT node.
    2012-07-06T21:01:12.420Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000004-delta.vmdk" : closed.
    2012-07-06T21:01:12.420Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000003-delta.vmdk" : closed.
    2012-07-06T21:01:12.420Z| vcpu-0| DISK: Failed to open disk for consolidate '/vmfs/volumes/4d9ad894-9c46d712-92ac-842b2b659fb0/Email/Email-000004.vmdk' : Failed to lock the file (16392) 5345


It seems that we are having a lot of locking issues when cleaning up our snapshots. I was looking over the release notes of [VDDK 5.0U1](https://www.vmware.com/support/developer/vddk/VDDK-501-ReleaseNotes.html), and I noticed this section:

> **Snapshot consolidation failure when cleaning up after HotAdd backup.**
> When VMware Data Recovery (or VADP backup software) tried to clean up after HotAdd backup, snapshot delete failed as the appliance was reconfigured, and an exception was reported. The problem was caused by premature exit of the vpxa process, so vpxa did not inform backup code that HotAdd disks should be removed. Stale HotAdd disks remained, and were not recognized the next time backup software ran. This caused failure of snapshot delete, resulting in a buildup of redo logs. The solution is to wait longer for vpxa to report, and apply heuristics to clean up stale HotAdd disks if they appear. The VDDK 5.0 U1 fix also works with earlier ESX/ESXi versions and for stale redo logs left by earlier VDDK versions.

VDDK 5.0U1 is included in ESXi 5.0U1, from the release notes:

> Backup partners who encounter these issues should encourage customers to run ESXi 5.0 U1 and to replace VDDK with the new build.

We were running 5.0GA, so we went ahead and updated to 5.0U1 (vCenter and ESXi) and the snapshot removal process started working properly without leaving any snapshots behind. This actually explained as to why our Integrity Checks were failing. Our snapshots would always fail and the CBT would only try to back up the last changed blocks but they just kept adding up from previous snapshots and it would cause inconsistent backups. Having discovered that, we added two new RDMs to the VDR appliance and put each of them on a separate SCSI controller (more information on how to do that can be seen in VMware KB [1037094](http://kb.vmware.com/kb/1037094)). We then mounted those two RDMs as two brand new Dedupe Stores.

We re-configured the backup jobs to now point to the new Dedupe Stores and re-enabled the Email_Server_Backup_Job and it still failed to even start the backup. We logged into the VDR appliance via ssh as root and we checked out the */var/vmware/datarecovery/datarecovery-0.log* file. When it was failing we saw the following log entry:


    7/7/2012 18:06:28.000: 0x0123e6a8: $[*20750]Trouble reading files, error -3956 ( operation failed)


As I was logged into the appliance I saw that the hostname of the appliance was *localhost*. If the appliance has the name of *localhost* it usually means that DNS is currently not setup properly, some times that cause random backup issues. From VMware KB [1037995](http://kb.vmware.com/kb/1037995):

> Verify DNS (including Reverse DNS) settings. Confirm that you can:
>
> *   Resolve the IP, FQDN, and shortname for the vCenter Server and all necessary ESX hosts from the VDR appliance.
> *   Resolve the IP, FQDN, and shortname of the VDR appliance from the vCenter Server.
> *   Resolve the IP, FQDN, and shortname of the VDR appliance and the vCenter Server from the vSphere Client computer (if the Client is running elsewhere).

The DNS was all over the place (The VDR appliance didn't have an A record, none of the ESXi host had pointer records, and we were using an old DNS server). After fixing all the DNS related issues, I wanted to change the DNS-Name that showed up in the appliance and ran into VMware communities post [212466,](http://communities.vmware.com/thread/212466) it actually describes how the DNS-Name is set within the appliance:

> There is a script /opt/vmware/share/vami/vami_set_hostname, which gets run during boot. This does a rev dns lookup for the ip address as follows:
>
> 	host -W 10 -T <ip> eth0
>
> If DNS does not resolve this ip addr request, it sets the hostname to localhost.localdom
>
> Make sure that your DNS server can resolve rev (and fwd) lookup entries for this hostname

Since my DNS was all setup, I just rebooted the appliance and then all the DNS checks passed. If you don't have a DNS server and you want to change the DNS-Name of your Appliance, you can follow the instruction laid out in that communities page:

> 	cd /opt/vmware/share/vami
> 	cp vami_set_hostname vami_set_hostname.orig
>
> Comment out the following 4 lines in vami_set_hostname (from line 54 of the file)
>
> 	cp $HOSTFILE ${HOSTFILE}.orig
> 	grep -v '^127.0.0.1\|^::1' < ${HOSTFILE}.orig > $HOSTFILE
> 	echo "127.0.0.1 $HN.$DN $HN localhost" >> $HOSTFILE
> 	echo "$FQDN" > $HOSTNAMEFILE
>
> This will ensure that this script does not overwrite the files everytime the appliance is rebooted.
>
> I have the following settings in my appliance (I am not using DHCP, but have a static ip setting)
>
> a. Update the /etc/hosts file the way you want it
>
> 	127.0.0.1 localhost
>
> b. Update /etc/hostname file with the FQDN
> c. Update the /etc/sysconfig/network to change the following
>
> 	HOSTNAME=<hostname>
> 	DOMAINNAME=<domain-name>
>
> d. Update the /etc/sysconfig/network-scripts to change the following
>
> 	DEVICE=eth0
> 	BOOTPROTO=none
> 	ONBOOT=yes
> 	TYPE=Ethernet
> 	IPADDR=<ip_of_vdr_appliance>
> 	NETMASK=<netmask_of_vdr_appliance>
> 	GATEWAY=<def_gw_of_vdr_appliance>
> 	BROADCAST=<broadcast_of_vdr_appliance>

After working through the DNS issues the Backup still failed with the same log message from */var/vmware/datarecovery/datarecovery-0.log*, but I also checked out the */var/log/datarecovery/vcbAPI-0.log* and I saw the following:


    2012-07-08T18:01:33.608-04:00 [4BFC8940 warning 'Default'] VcbAPI::Snapshot::GetChangeInfo: Cannot look for changes past the end of the disk, disk size: 268506040320, offset: 268506040320.
    2012-07-08T18:04:52.804-04:00 [4B5C7940 error 'Default'] vcbAPI::Snapshot::Read: Main read failed for disk [SAN] Email/Email-000001.vmdk, error: 2338
    2012-07-08T18:04:52.832-04:00 [4B5C7940 error 'Default'] RealPartitionReader: File i/o error ($1)
    2012-07-08T18:06:52.837-04:00 [4B5C7940 error 'Default'] vcbAPI::Snapshot::Read: Main read failed for disk [SAN] Email/Email-000001.vmdk, error: 2338
    2012-07-08T18:06:52.837-04:00 [4B5C7940 error 'Default'] RealPartitionReader: File i/o error ($1)
    2012-07-08T18:06:52.837-04:00 [4B5C7940 info 'Default'] VcbAPI::Snapshot::GetUnusedFileInfo: Could not obtain file blocks for "pagefile.sys" on one of Partitions of path: "[SAN] Email/Email-000001.vmdk", error: 32771
    2012-07-08T18:06:53.452-04:00 [4B5C7940 info 'Default'] VcbAPI::Snapshot::GetChangeInfo: Got InvalidArgument exception: vmodl.fault.InvalidArgument
    2012-07-08T18:06:53.477-04:00 [4B5C7940 error 'Default'] Exception in VCBSnapshot_GetDiskChanges: Error code: 1318
    2012-07-08T18:08:53.513-04:00 [4B5C7940 error 'Default'] vcbAPI::Snapshot::Read: Main read failed for disk [SAN] Email/Email-00001.vmdk, error: 2338
    2012-07-08T18:08:53.513-04:00 [4B5C7940 error 'Default'] Exception in VCBSnapshot_ReadFile: Error code: 1315


I then ran across VMware KB [2013450](http://kb.vmware.com/kb/2013450), which had the following instructions to fix the above issue:

> 1. Open a console or SSH to the VDR Appliance.
> 2. Log in using your credentials. The default credentials are:
>
> 	Username: root
> 	Password: vmw@re
>
> 3. Stop the data recovery service with this command:
>
> 		# service datarecovery stop
>
> 4. Open the /var/vmware/datarecovery/datarecovery.ini file in a plain text editor and ensure it contains these values:
>
> 		[Options]
> 		SetVCBLogging=6
> 		SetVolumesLogging=6
> 		SetRAPILogging=6
> 		BackupUnusedData=1
>
> 	Note: You can create the file if it does not exist. For further/related information, see Editing files on an ESX host using vi or nano (1020302)
>
> 5. Start the data recovery service with this command:
>
> 		# service datarecovery start

After removing the original entries from datarecovery.ini file and replacing them with the above, the backup started to work. We left the backup job running for a couple of days and it was successful for a couple of days, but one of the days it failed with the following:

![failed_to_backup_cause_of_quiesce_1](https://github.com/elatov/uploads/raw/master/2012/08/failed_to_backup_cause_of_quiesce_1.png)

Looking inside the Guest Operating System Event Viewer we saw the following:

![failed_to_flush](https://github.com/elatov/uploads/raw/master/2012/08/failed_to_flush.png)

Searching for that error, I came across Veritas Tech Article [27875](https://www.veritas.com/support/en_US/article.TECH27875). It talks about the following:

> There are some application-specific writers which write the data on request from the requesters; in this case, that can be backup software.
>
> The states of all these writers while taking the backups using VSS technology should be [1] Stable followed by Last Error: No error.
>
> To check the writer status, do the following:
>
> 1. Start > Run, then type cmd and click OK.
> 2. Type VSSADMIN LIST WRITERS at the command line, then press the key.
>
> Resolution:
> 1. If any of the writers' statuses do not return to stable, rebooting the server often resolves the issue.
> 2. If the issue persists, apply the VSS-3 update available as Microsoft KB 940349 ( http://support.microsoft.com/default.aspx?kbid=940349 ). Please note that this does NOT update individual writers, it only updates the framework within which the writers operate.

*vssadmin list writers*, didn't return any errors. Our VM was Win2K3, so we tried the above patch. After the above patch we didn't get any more "quiesced" snapshots errors.

All was well for a while, but then one day one of the Integrity check failed again. Here is what we saw in the reports tabs of VDR.

![vdr-int-check-failing](https://github.com/elatov/uploads/raw/master/2012/08/vdr-int-check-failing.png)
We logged into the appliance again and checking out the */var/vmware/datarecovery/datarecovery-0.log*, we saw the following:


    Aug 17 14:06:13 vdr datarecovery: Can't load restore point tree for 8/17/2012 7:00:56 AM, error -2249 ( could not find restore point)
    Aug 17 14:06:14 vdr datarecovery: Job "Integrity Check" incomplete


I also noticed that earlier in the day this occured in the logs:



    Aug 17 07:14:42 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM0)" completed successfully
    Aug 17 07:26:52 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM1)" completed successfully
    Aug 17 07:28:32 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM2)" completed successfully
    Aug 17 07:32:19 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM3)" completed successfully
    Aug 17 07:35:47 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM4)" completed successfully
    Aug 17 07:48:37 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM5)" completed successfully
    Aug 17 07:49:28 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM6)" completed successfully
    Aug 17 07:50:27 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM7)" completed successfully
    Aug 17 07:59:46 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM8)" completed successfully
    Aug 17 08:00:01 vdr datarecovery: Job terminated at specified stop time.
    Aug 17 08:00:01 vdr last message repeated 4 times
    Aug 17 08:00:05 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM9)" incomplete
    Aug 17 08:03:47 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM10)" incomplete
    Aug 17 08:03:54 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM11)" incomplete
    Aug 17 08:04:11 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM12)" incomplete
    Aug 17 08:04:25 vdr datarecovery: Job "All_Other_VMs_Backup_Job (VM13)" incomplete


It looks like we had backups going but they didn't finish by 8 AM, which is when our backup windows stops, so the jobs were forcefully stopped. That can cause the Intergrity check to fail since we had data that was half backed up. After we increased our backup window, the Integrity Check stopped failing, since all the VMs had enough time to be backed up.
