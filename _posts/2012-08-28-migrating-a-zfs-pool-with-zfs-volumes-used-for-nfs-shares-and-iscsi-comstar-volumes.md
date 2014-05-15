---
title: Migrating a ZFS Pool with ZFS Volumes Used for NFS Shares and iSCSI Comstar Volumes
author: Karim Elatov
layout: post
permalink: /2012/08/migrating-a-zfs-pool-with-zfs-volumes-used-for-nfs-shares-and-iscsi-comstar-volumes/
dsq_thread_id:
  - 1406675076
categories:
  - Home Lab
  - VMware
  - ZFS
tags:
  - COMSTAR
  - comstar iscsi-target
  - esxcfg-nas
  - sbdadm
  - STMF
  - ZFS
  - ZFS Export
  - ZFS Import
  - ZFS sharenfs
---
If you had a chance to read my previous  regarding migrating the root ZFS pool to a smaller drive, first of all I wanted to apologize for the longevity of that blog, secondly I decided to do some additional steps after the migration. I wanted to rename my zpool from 'rpool1' to 'data'. Usually you can do this with just a zpool export and import, but I was using some of the ZFS volumes as NFS shares and some of them for Comstar iSCSI Volumes, so there were some additional steps necessary to make the migration complete appropriately. First of all here are my zpools:

	  
	root@openindiana:~# zpool status  
	pool: rpool1  
	state: ONLINE  
	scan: none requested  
	config:
	
	NAME STATE READ WRITE CKSUM  
	rpool1 ONLINE 0 0 0  
	c3t0d0s0 ONLINE 0 0 0
	
	errors: No known data errors
	
	pool: syspool  
	state: ONLINE  
	scan: none requested  
	config:
	
	NAME STATE READ WRITE CKSUM  
	syspool ONLINE 0 0 0  
	c4t0d0s0 ONLINE 0 0 0
	
	errors: No known data errors  
	

And here are my ZFS Volumes:

	  
	root@openindiana:~# zfs list -r rpool1  
	NAME USED AVAIL REFER MOUNTPOINT  
	rpool1 238G 11.8G 46K /rpool1  
	rpool1/iscsi_share 103G 110G 4.71G -  
	rpool1/iscsi_share2 134G 146G 26.5M -  
	rpool1/nfs_share 1000M 11.8G 1000M /rpool1/nfs_share  
	

As you have probably guessed 'iscsi_share' and 'iscsi_share2' are used as iSCSI Comstar Volumes, BTW if you want information on Comstar, I would recommend reading the Oracle Documentation "<a href="http://docs.oracle.com/cd/E19963-01/html/821-1459/fncpi.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19963-01/html/821-1459/fncpi.html']);">Configuring COMSTAR (Task Map)</a>":

	  
	root@openindiana:~# sbdadm list-lu
	
	Found 2 LU(s)
	
	GUID DATA SIZE SOURCE  
	\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---\---\---\--- \---\---\---\---\----  
	600144f0928c010000004fc511ec0001 107374182400 /dev/zvol/rdsk/rpool1/iscsi_share  
	600144f0928c010000004fc90a3a0001 139586437120 /dev/zvol/rdsk/rpool1/iscsi_share2  
	

And 'nfs_share' is used as an NFS Share:

	
	
	root@openindiana:~# zfs get sharenfs rpool1/nfs_share  
	NAME PROPERTY VALUE SOURCE  
	rpool1/nfs_share sharenfs rw,root=192.168.1.108 local  
	

Trying to export the ZFS pool, we actually get an error saying that it's in use:

	  
	root@openindiana:~# zpool export rpool1  
	cannot export 'rpool1': pool is busy  
	

This is actually expected, from the Oracle Documenation, '<a href="http://docs.oracle.com/cd/E19963-01/html/821-1448/gaypf.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19963-01/html/821-1448/gaypf.html']);">ZFS Volumes</a>':

> A ZFS volume as an iSCSI target is managed just like any other ZFS dataset except that you cannot rename the dataset, rollback a volume snapshot, or export the pool while the ZFS volumes are shared as iSCSI LUNs

When working with Comstar iSCSI there are usually two services in play. The first one is *stmf*, more information can be found in the Oracle Documentation "<a href="http://docs.oracle.com/cd/E23824_01/html/821-1459/fnnop.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E23824_01/html/821-1459/fnnop.html']);">Configuring iSCSI Devices With COMSTAR</a>", from that documentation:

> COMSTAR uses SMF to store its current, persistent configuration, such as logical unit mapping, host group definitions, and target group definitions. When the service is enabled during boot or when using the svcadm command, it clears any stale configuration data inside the kernel framework, and then reloads the configuration from the SMF repository into the driver. After the configuration is loaded, any changes that are made to the configuration are automatically updated inside the driver database, as well as inside the SMF repository. For example, any changes made through the stmfadm command are automatically updated in both areas.
> 
> The COMSTAR target mode framework runs as the stmf service. By default, the service is disabled. You must enable the service to use COMSTAR functionality. You can identify the service with the svcs command

My service was, of course, online, since I had LUNs provisioned from the Comstar Framework:

	  
	root@openindiana:~# svcs -l stmf  
	fmri svc:/system/stmf:default  
	name STMF  
	enabled true  
	state online  
	next_state none  
	state_time August 22, 2012 02:23:33 AM MDT  
	logfile /var/svc/log/system-stmf:default.log  
	restarter svc:/system/svc/restarter:default  
	dependency require_all/none svc:/system/filesystem/local:default (online)  
	

The second aspect of the COMSTAR Framework is the 'iscsi-target', this used to be handled by the *iscsitadm*, from the Oracle Document "<a href="http://docs.oracle.com/cd/E23824_01/html/E24456/storage-7.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E23824_01/html/E24456/storage-7.html']);">COMSTAR Replaces iSCSI Target Daemon</a>":

> The Oracle Solaris 10 release uses the iSCSI target daemon and the iscsitadm command and the ZFS shareiscsi property to configure iSCSI LUNs.
> 
> In the Oracle Solaris 11 release, the COMSTAR (Common Multiprotocol SCSI Target) features provide the following components:
> 
> *   Support for different types of SCSI targets, not just the iSCSI protocol
> *   ZFS volumes are used as backing store devices for SCSI targets by using one or more of COMSTAR's supported protocols.
> 
> Although the iSCSI target in COMSTAR is a functional replacement for the iSCSI target daemon, no upgrade or update path exist to convert your iSCSI LUNs to COMSTAR LUNs.
> 
> Both the iSCSI target daemon and the shareiscsi property are not available in Oracle Solaris 11. The following commands are used to manage iSCSI targets and LUNs.
> 
> *   The itadm command manages SCSI targets.
> *   The srptadm command manages SCSI RDMA Protocol (SRP) target ports.
> *   The stmfadm command manages SCSI LUNs. Rather than setting a special iSCSI property on the ZFS volume, create the volume and use stmfadm to create the LUN.

But now you can do with the comstar iscsi-target service, from the Oracle documentation:

> The logical unit provider for creating disk-type LUNs is called sbd. However, you must initialize the storage for the logical unit before you can share a disk-type LUN.
> 
> The disk volume provided by the server is referred to as the target. When the LUN is associated with an iSCSI target, it can be accessed by an iSCSI initiator.
> 
> The process for creating SCSI LUNs is as follows:
> 
> *   Initialize the storage for the LUN, also known as the backing store.
> *   Create a SCSI LUN by using the backing store.
> 
> When a LUN is created, it is assigned a global unique identifier (GUID), for example, 600144F0B5418B0000004DDAC7C10001. The GUID is used to refer to the LUN in subsequent tasks, such as mapping a LUN to select hosts.

I can see that my iscsi-target service was running as well:

	  
	root@openindiana:~# svcs -l iscsi/target  
	fmri svc:/network/iscsi/target:default  
	name iscsi target  
	enabled true  
	state online  
	next_state none  
	state_time August 22, 2012 02:23:34 AM MDT  
	logfile /var/svc/log/network-iscsi-target:default.log  
	restarter svc:/system/svc/restarter:default  
	dependency require_any/error svc:/milestone/network (online)  
	dependency require_all/none svc:/system/stmf:default (online)  
	

we can also see that it depends on the stmf service and this makes sense since the stmf creates the LUNs and the iscsi-target serves up the LUNs. Without the LUNs there will nothing to serve. So let's see if we can stop the stmf service and then try to our export one more time.

	  
	root@openindiana:~# zpool export -f rpool1  
	cannot export 'rpool1': pool is busy
	
	root@openindiana:~# svcadm disable stmf  
	root@openindiana:~# svcadm disable iscsi/target
	
	root@openindiana:~# zpool export -f rpool1  
	cannot export 'rpool1': pool is busy  
	

I still couldn't export. I even checked the connection table to make sure nothing was mounting the volumes:

	  
	root@openindiana:/var/svc/log# netstat -an -f inet
	
	UDP: IPv4  
	Local Address Remote Address State  
	\---\---\---\---\---\---\-- -\---\---\---\---\---\---\- --\---\-----  
	*.111 Idle  
	*.* Unbound  
	*.57026 Idle  
	*.111 Idle  
	*.* Unbound  
	*.53050 Idle  
	*.* Unbound  
	*.* Unbound  
	*.* Unbound  
	*.4045 Idle  
	*.4045 Idle  
	*.50102 Idle  
	*.53843 Idle  
	*.35042 Idle  
	*.58998 Idle
	
	TCP: IPv4  
	Local Address Remote Address Swind Send-Q Rwind Recv-Q State  
	\---\---\---\---\---\---\-- -\---\---\---\---\---\---\- --\--- \---\--- \---\-- -\---\-- -\---\---\----  
	*.111 *.* 0 0 128000 0 LISTEN  
	*.* *.* 0 0 128000 0 IDLE  
	*.111 *.* 0 0 128000 0 LISTEN  
	*.* *.* 0 0 128000 0 IDLE  
	*.4045 *.* 0 0 1049200 0 LISTEN  
	*.4045 *.* 0 0 1048952 0 LISTEN  
	*.35450 *.* 0 0 128000 0 LISTEN  
	*.46501 *.* 0 0 128000 0 LISTEN  
	*.22 *.* 0 0 128000 0 LISTEN  
	*.65075 *.* 0 0 128000 0 LISTEN  
	*.59457 *.* 0 0 128000 0 LISTEN  
	127.0.0.1.25 *.* 0 0 128000 0 LISTEN  
	127.0.0.1.587 *.* 0 0 128000 0 LISTEN  
	192.168.1.107.22 192.168.1.100.56242 64768 51 128480 0 ESTABLISHED  
	

I then double checked the services, and both were disabled:

	  
	root@openindiana:~# svcs -l iscsi/target  
	fmri svc:/network/iscsi/target:default  
	name iscsi target  
	enabled false  
	state disabled  
	next_state none  
	state_time August 26, 2012 01:14:28 AM MDT  
	logfile /var/svc/log/network-iscsi-target:default.log  
	restarter svc:/system/svc/restarter:default  
	dependency require_any/error svc:/milestone/network (online)  
	dependency require_all/none svc:/system/stmf:default (disabled)
	
	root@openindiana:~# svcs -l stmf  
	fmri svc:/system/stmf:default  
	name STMF  
	enabled false  
	state disabled  
	next_state none  
	state_time August 26, 2012 01:12:27 AM MDT  
	logfile /var/svc/log/system-stmf:default.log  
	restarter svc:/system/svc/restarter:default  
	dependency require_all/none svc:/system/filesystem/local:default (online)  
	

I then rebooted my openindiana VM:

	  
	root@openindiana:~# reboot  
	

After it rebooted my export succeeded without any issues:

	  
	root@openindiana:~# zpool export rpool1  
	root@openindiana:~#  
	

I then re-imported the ZFS Pool with another name:

	  
	root@openindiana:~# zpool import rpool1 data  
	root@openindiana:~# zfs list -r data  
	NAME USED AVAIL REFER MOUNTPOINT  
	data 238G 11.8G 46K /data  
	data/iscsi_share 103G 110G 4.71G -  
	data/iscsi_share2 134G 146G 26.5M -  
	data/nfs_share 1000M 11.8G 1000M /data/nfs_share  
	

That looks good, I then re-enabled the services and checked for my LUNs:

	  
	root@openindiana:~# svcadm enable stmf  
	root@openindiana:~# svcadm enable iscsi/target  
	root@openindiana:~# sbdadm list-lu  
	root@openindiana:~#  
	

Since the LUNs depend on the ZFS Volume full path, I will have to re-add them using the same guid. Jarret actually ran into this recently in his lab, check out his <a href="http://virtuallyhyper.com/2012/08/restoring-from-backup-in-my-home-lab/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/restoring-from-backup-in-my-home-lab/']);">post</a>. Here is what I did to re-add my ZFS volumes back to sdbadm, so they can be seen as LUNs again:

	  
	root@openindiana:~# stmfadm create-lu -p guid=600144f0928c010000004fc511ec0001 /dev/zvol/rdsk/data/iscsi_share  
	Logical unit created: 600144F0928C010000004FC511EC0001
	
	root@openindiana:~# stmfadm create-lu -p guid=600144f0928c010000004fc90a3a0001 /dev/zvol/rdsk/data/iscsi_share2  
	Logical unit created: 600144F0928C010000004FC90A3A0001  
	

Now checking out sbdadm, I saw the following:

	  
	root@openindiana:~# sbdadm list-lu
	
	Found 2 LU(s)
	
	GUID DATA SIZE SOURCE  
	\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---\---\---\--- \---\---\---\---\----  
	600144f0928c010000004fc511ec0001 107374182400 /dev/zvol/rdsk/data/iscsi_share  
	600144f0928c010000004fc90a3a0001 139586437120 /dev/zvol/rdsk/data/iscsi_share2  
	

That looks perfect. Since the GUID stayed the same, I didn't have to worry about my views or target port group settings. I had to use the original GUIDs, so this process would've worked if I didn't have them written down or saved somewhere. Lastly checking the NFS share settings, I saw the following:

	  
	root@openindiana:~# zfs get sharenfs data/nfs_share  
	NAME PROPERTY VALUE SOURCE  
	data/nfs_share sharenfs rw,root=192.168.1.108 local
	
	root@openindiana:~# sharemgr show -vp  
	default nfs=()  
	zfs nfs=()  
	zfs/data/nfs_share nfs=() nfs:sys=(rw="*" root="192.168.1.108")  
	/data/nfs_share  
	

Those settings stuck around, so I didn't have to do anything with that. I went to the esx hosts that were connecting to the openindiana VM and did a rescan and all the iSCSI LUNs showed up just fine. I did check the NFS mount point and it was pointing to the old location:

	  
	~ # esxcfg-nas -l  
	nfs is /rpool1/nfs_share from 192.168.1.107 mounted  
	

But it was actually mounting the NFS share without an issue. It was probably cached or something, just for good measure I went ahead and removed the mount point and remounted it:

	  
	~ # esxcfg-nas -d nfs  
	NAS volume nfs deleted.
	
	~ # esxcfg-nas -a -o 192.168.1.107 -s /data/nfs_share nfs  
	Connecting to NAS volume: nfs  
	nfs created and connected.
	
	~ # esxcfg-nas -l  
	nfs is /data/nfs_share from 192.168.1.107 mounted  
	

That was good. I was able to create files and everything was working as expected. Lastly checking the network connections, I saw all the hosts connected to the openindiana VM:

	  
	root@openindiana:~# netstat -an -f inet | egrep '3260|2049' | grep ESTABLISHED  
	192.168.1.107.3260 192.168.1.109.50823 263536 0 263536 0 ESTABLISHED  
	192.168.1.107.3260 192.168.1.108.60249 263536 0 263536 0 ESTABLISHED  
	192.168.1.107.3260 192.168.1.106.57857 263168 0 263536 0 ESTABLISHED  
	192.168.1.107.2049 192.168.1.108.792 66608 0 1049800 0 ESTABLISHED  
	192.168.1.107.2049 192.168.1.108.793 66608 0 1049800 0 ESTABLISHED  
	

All was back to normal.

**Update:** Jarret pointed me to "<a href="http://docs.oracle.com/cd/E23824_01/html/821-1448/gayne.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E23824_01/html/821-1448/gayne.html']);">Sharing and Unsharing ZFS File Systems</a>". From that article we can see that we can actually set a "share" name for our NFS export and we wouldn't have to remount the NFS share from the ESX host. From that article:

> **New ZFS Sharing Syntax**  
> The new zfs set share command is used to share a ZFS file system over the NFS or SMB protocols. The share is not published until the sharenfs set property is also set on the file system.
> 
> Use the zfs set share command to create an NFS or SMB share of ZFS file system and also set the sharenfs property.
> 
	>   
	> \# zfs create rpool/fs1  
	> \# zfs set share=name=fs1,path=/rpool/fs1,prot=nfs rpool/fs1  
	> name=fs1,path=/rpool/fs1,prot=nfs  
	> 
> 
> The share is not published until the sharenfs or sharesmb property is set to on. For example:
> 
	>   
	> \# zfs set sharenfs=on rpool/fs1  
	> \# cat /etc/dfs/sharetab  
	> /rpool/fs1 fs1 nfs sec=sys,rw  
	> 
> 
> A public NFS share can be created as follows:
> 
	>   
	> \# zfs set share=name=pp,path=/pub,prot=nfs,sec=sys,rw=*,public rpool/public  
	> name=pp,path=/pub,prot=nfs,public=true,sec=sys,rw=*  
	> \# zfs set sharenfs=on rpool/public  
	> \# cat /etc/dfs/sharetab  
	> /pub pp nfs public,sec=sys,rw  
	> 
> 
> You can also create a share of a newly created ZFS file system by using syntax similar to the following:
> 
	>   
	> \# zfs create -o mountpoint=/ds -o sharenfs=on rpool/ds  
	> 

This was kind of hindsight, so I didn't have a chance to plan accordingly and try it out.


 [1]: http://virtuallyhyper.com/2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive