---
title: 'vSphere Replication Shows Replication as &#8220;not active&#8221;'
author: Jarret Lavallee
layout: post
permalink: /2012/08/vsphere-replication-shows-inactive-replication/
dsq_thread_id:
  - 1407411455
categories:
  - SRM
  - VMware
tags:
  - command line
  - hostd.log
  - logs
  - not active replication
  - srm
  - VRMS
  - VRS
  - vSphere Replication
---
I was messing around in my SRM lab and ran into this issue. It is a common issue that we see, but it has different causes.

I set up replication for the VM, failed it over to the other site. I then removed replication cleaned up the protection group and recovery plan. After a little while I configured replication from the recovery site to the protected site. In the middle of configuring replication, my protected site host dropped out of vCenter. After getting everything on-line again I was able to configure replication on the VM. I went to check the replication status in the GUI and found it stuck in the &#8220;not active&#8221;.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-replication-not-active.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-replication-not-active.png']);"><img class="aligncenter size-full wp-image-2163" title="VRMS replication not active" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-replication-not-active.png" alt="VRMS replication not active vSphere Replication Shows Replication as not active" width="656" height="59" /></a>

The first thing I did was try to &#8220;synchronize now&#8221;, but this failed immediately telling me &#8220;An ongoing Synchronization task already exists&#8221;.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/ongoing-sync-on-VRMS.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/ongoing-sync-on-VRMS.png']);"><img class="aligncenter size-full wp-image-2164" title="ongoing sync on VRMS" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/ongoing-sync-on-VRMS.png" alt="ongoing sync on VRMS vSphere Replication Shows Replication as not active" width="827" height="408" /></a>

So I went to the ESXi host to take a look at the replication status on the VM. What I found was that there is a full sync in progress, but the progress was at 0%.

	  
	~ # vim-cmd vmsvc/getallvms | grep Awesome  
	6 My Awesome VM  My Awesome VM/My Awesome VM.vmx rhel6_64Guest vmx-08  
	~ # vim-cmd hbrsvc/vmreplica.getState 6  
	Retrieve VM running replication state:  
	The VM is configured for replication. Current replication state: Group: GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7 (generation=1655953650859617)  
	Group State: full sync (0% done: checksummed 0 bytes of 16 GB, transferred 0 bytes of 0 bytes)  
	DiskID RDID-ef948351-e4ef-48b1-a19b-78b119bb7490 State: full sync (checksummed 0 bytes of 16 GB, transferred 0 bytes of 0 bytes)  
	

After looking into why it did not report that there was a sync in progress, it looks like the next version will have some better error messages about the state of replication. So the errors should be better in the next version.

A few minutes later I checked on the sync status again and it was still 0%, so there is something wrong.

	  
	~ # vim-cmd hbrsvc/vmreplica.queryReplicationState 6  
	Querying VM running replication state:  
	Current replication state:  
	State: syncing  
	Progress: 0% (checksum: 0/17179869184; transfer: 0/0)  
	

I went ahead and looked at the logs for the host and found that it had not logged anything for 5 days. Ideally I&#8217;d like to look at the hostd logs to see what is going on for the HBR service, but it had not logged since before the VM was on the host. I went to look why this happened and found the reason in the vmkernel log. Below is the last line if the vmkernel.log.

	  
	2012-08-06T08:47:25.950Z cpu1:2108)BC: 4350: Failed to flush 1 buffers of size 8192 each for object 'hostd.log' fa7 36 4 501d94c3 3b3bba1e 500050df c507b056 8 7 ace94104 24 0 0 0: Timeout  
	

The host could not write to the hostd.log on the scratch partition of the host. Looking further back in the vmkernel.log we can see that local controller was aborting commands to the local disk.

	  
	2012-08-06T08:47:08.587Z cpu1:4477)ScsiDeviceIO: 2309: Cmd(0x4124007cedc0) 0x2a, CmdSN 0x101e9 from world 2108 to dev "mpx.vmhba1:C0:T0:L0" failed H:0x8 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.  
	2012-08-06T08:47:09.892Z cpu0:2141)VMW\_SATP\_LOCAL: satp\_local\_updatePathStates:439: Failed to update path "vmhba1:C0:T0:L0" state. Status=Transient storage condition, suggest retry  
	2012-08-06T08:47:10.766Z cpu1:2063)<6>mptscsih: ioc0: task abort: SUCCESS (sc=0x412401605400)  
	2012-08-06T08:47:13.617Z cpu0:2155)<6>mptscsih: ioc0: attempting task abort! (sc=0x41240160bd00)  
	2012-08-06T08:47:13.617Z cpu0:2155)MPT SPI Host:2:0:0:0 ::  
	<6> command: Write(10): 2a 00 00 1c 25 a2 00 00 80 00  
	2012-08-06T08:47:13.959Z cpu0:2155)<6>mptscsih: ioc0: task abort: SUCCESS (sc=0x41240160bd00)  
	2012-08-06T08:47:13.959Z cpu1:2049)WARNING: NMP: nmp_DeviceRequestFastDeviceProbe:237:NMP device "mpx.vmhba1:C0:T0:L0" state in doubt; requested fast path state update...  
	

I put the host in maintenance mode and rebooted the host as it had stopped communicating with it&#8217;s local disk. After I brought up the host, the replication was still in the same state, but we had hostd logs to take a look at.

	  
	2012-08-11T00:01:17.956Z [2E6C2B90 verbose 'Hbrsvc'] Creating replication group for VM My Awesome VM with spec: {dynamicType = <unset>, generation = 3, vmReplicationId = "GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7", destination = "192.168.10.86", port = 44046, rpo = 240, quiesceGuestEnabled = false, paused = false, oppUpdatesEnabled = false, disk = [{dynamicType = <unset>, key = 2000, diskReplicationId = "RDID-ef948351-e4ef-48b1-a19b-78b119bb7490", }], }  
	2012-08-11T00:01:17.956Z [2E6C2B90 verbose 'Hbrsvc'] Extracted VM RPO=240 from replication spec  
	2012-08-11T00:01:17.956Z [2E6C2B90 info 'Hbrsvc'] Configuring disk (deviceKey=2000)  
	2012-08-11T00:01:17.956Z [2E6C2B90 info 'Hbrsvc'] ReplicationGroup added disk (groupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7) (diskID=RDID-ef948351-e4ef-48b1-a19b-78b119bb7490)  
	2012-08-11T00:01:17.956Z [2E6C2B90 verbose 'Hbrsvc'] Created replication group for VM: My Awesome VM (GroupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7)  
	2012-08-11T00:01:17.956Z [2E6C2B90 verbose 'Hbrsvc'] Replicator: VmFileProviderCallback VM (id=6)  
	2012-08-11T00:01:17.957Z [2E6C2B90 verbose 'Hbrsvc'] Replicator: VM 6 Disk (Key=2000,Id=RDID-ef948351-e4ef-48b1-a19b-78b119bb7490) has psf:  My Awesome VM/hbr-persistent-state-RDID-ef948351-e4ef-48b1-a19b-78b119bb7490.psf  
	2012-08-11T00:01:17.958Z [2E6C2B90 info 'Hbrsvc'] ReplicatedDisk extracted state: full sync (pauseFlag=false needFullSync=false) (diskID=RDID-ef948351-e4ef-48b1-a19b-78b119bb7490) (groupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7) (lastOpID=0)  
	2012-08-11T00:01:17.958Z [2E6C2B90 info 'Hbrsvc'] ReplicatedDisk: Extract state succeeded (diskID=RDID-ef948351-e4ef-48b1-a19b-78b119bb7490) (vmID=6) (groupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7) (state=full sync)  
	2012-08-11T00:01:17.958Z [2E6C2B90 info 'Hbrsvc'] ReplicationGroup initialized replication successfully (state=full sync) (groupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7)  
	2012-08-11T00:01:18.017Z [2ECD7B90 verbose 'Hbrsvc' opID=cc1e3be9-76] Replicator: VmFileProviderCallback VM (id=6)  
	2012-08-11T00:01:18.018Z [2ECD7B90 verbose 'Hbrsvc' opID=cc1e3be9-76] Replicator: VM 6 Disk (Key=2000,Id=RDID-ef948351-e4ef-48b1-a19b-78b119bb7490) has psf:  My Awesome VM/hbr-persistent-state-RDID-ef948351-e4ef-48b1-a19b-78b119bb7490.psf  
	

From the logs above, it looks like everything is good. The host started the full sync. Next we need to check the VRS. The replication goes from the protected side host to the VRS to the DR host, so we will need to check the logs in that order. The logs on the VRS are located at /var/log/vmware/. The username is &#8220;root&#8221; and the password is &#8220;vmware&#8221;. In this case I opened up the hbrsrv.log and found the following.

	  
	2012-08-11T00:03:55.507Z [F6131B70 info 'Setup'] Created ActiveDisk for DiskID: RDID-ef948351-e4ef-48b1-a19b-78b119bb7490 Base path: /vmfs/volumes/501d996c-86c6616  
	9-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk curPath: /vmfs/volumes/501d996c-86c66169-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk  
	2012-08-11T00:03:55.508Z [F6131B70 verbose 'PropertyProvider'] RecordOp ASSIGN: lastError, Hbr.Replica.Datastore.501d996c-86c66169-eea2-005056b007c1  
	2012-08-11T00:03:55.508Z [F6131B70 error 'Main'] HbrError for (datastoreUUID: "501d996c-86c66169-eea2-005056b007c1"), (diskId: "RDID-ef948351-e4ef-48b1-a19b-78b119  
	bb7490"), (flags: on-disk-open) stack:  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[0\] No accessible host for datastore 501d996c-86c66169-eea2-005056b007c1  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[1\] Code set to: Generic storage error.  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[2\] Failed to find host to establish nfc connection  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[3\] Failed to open disk, couldn't create NFC session  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[4\] Set error flag: on-disk-open  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[5\] Failed to open replica (/vmfs/volumes/501d996c-86c66169-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk)  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[6\] Failed to open activeDisk (GroupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7) (DiskID=RDID-ef948351-e4ef-48b  
	1-a19b-78b119bb7490)  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[7\] Can't create replica state (GroupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7) (DiskID=RDID-ef948351-e4ef-48  
	b1-a19b-78b119bb7490)  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[8\] Cannot activate group. Loading disks from database (GroupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7)  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[9\] Connecting to group GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[10\] Failed to activate (groupID=GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7, sessionID=0)  
	2012-08-11T00:03:55.508Z \[F6131B70 error 'Main'\] \[11\] Converting error to wire failure  
	

The problem here is that the VRS cannot find a host that has access to the datastore that we selected to receive replication (501d996c-86c66169-eea2-005056b007c1). So I ssh&#8217;ed into the host we were replicating to and took a look at the datastores that it had mounted.

	  
	~ # esxcfg-scsidevs -m  
	mpx.vmhba1:C0:T0:L0:3 /vmfs/devices/disks/mpx.vmhba1:C0:T0:L0:3 501d93eb-1eb86026-0726-005056b007c1 0 datastore1  
	mpx.vmhba1:C0:T1:L0:1 /vmfs/devices/disks/mpx.vmhba1:C0:T1:L0:1 501d996c-86c66169-eea2-005056b007c1 0 prod  
	

Above we can see that 501d996c-86c66169-eea2-005056b007c1 is mounted as the &#8220;prod&#8221; datastore. Checking the HBR logs in the hostd.log I did not see any mention of a connection for this, so I went back to the VRS and took a look for any connections to the host. I found the following problem connecting to this host.

	  
	2012-08-11T00:18:38.279Z [F71CC6D0 info 'Host'] Heartbeat handler detected dead connection for host: 192.168.10.82  
	2012-08-11T00:18:38.279Z [F71CC6D0 info 'Main'] HbrError stack:  
	2012-08-11T00:18:38.279Z \[F71CC6D0 info 'Main'\] \[0\] ExcError: exception N7Vmacore21InvalidStateExceptionE: No connection (host=192.168.10.82)  
	2012-08-11T00:18:38.279Z \[F71CC6D0 info 'Main'\] \[1\] Failed to get time (host=192.168.10.82)  
	2012-08-11T00:18:38.279Z \[F71CC6D0 info 'Main'\] \[2\] Ignored error.  
	2012-08-11T00:18:38.279Z [F71CC6D0 verbose 'Db'] SQL code: SELECT * FROM GlobalString WHERE (key == 'guestinfo-cache/guestinfo.hbr.hbrsrv-certificate-revoked');  
	2012-08-11T00:18:38.340Z [F71CC6D0 verbose 'HostAgentConnection'] Logging in to 192.168.10.82 using SSL thumbprint.  
	2012-08-11T00:18:38.340Z [F71CC6D0 verbose 'HttpConnectionPool'] HttpConnectionPoolImpl created. maxPoolConnections = 1; idleTimeout = 900000000; maxOpenConnection  
	s = 1; maxConnectionAge = 0  
	2012-08-11T00:18:43.668Z [F71CC6D0 error 'HostAgentConnection'] Connection failed to host 192.168.10.82: vim.fault.InvalidLogin  
	2012-08-11T00:18:43.668Z [F71CC6D0 info 'vmomi.soapStub[1]'] Resetting stub adapter for server TCP:192.168.10.82:80 : Closed  
	2012-08-11T00:18:43.668Z [F71CC6D0 verbose 'PropertyProvider'] RecordOp ASSIGN: lastError, Hbr.Replica.Host.192.168.10.82  
	2012-08-11T00:18:45.544Z [F71CC6D0 verbose 'SessionManager'] hbr.replica.ReplicationManager.GetServerStats: authorized  
	

So it looks like VRS cannot log into the host. To alleviate this I went in and re-registered the VRS.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-5-Register-VRS.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-5-Register-VRS.png']);"><img class="aligncenter size-full wp-image-2169" title="SRM 5 Register VRS" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-5-Register-VRS.png" alt="SRM 5 Register VRS vSphere Replication Shows Replication as not active" width="891" height="408" /></a>

After the operation finished, we can see in the VRS logs that it logged into the host and detected the datastores.

	  
	2012-08-11T00:32:47.939Z [F5D03B70 verbose 'StorageMap'] Host 192.168.10.82 added for datastore 501d996c-86c66169-eea2-005056b007c1  
	2012-08-11T00:32:50.228Z [F72236D0 info 'Setup'] Created ActiveDisk for DiskID: RDID-ef948351-e4ef-48b1-a19b-78b119bb7490 Base path: /vmfs/volumes/501d996c-86c6616  
	9-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk curPath: /vmfs/volumes/501d996c-86c66169-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk  
	2012-08-11T00:32:50.228Z [F72236D0 verbose 'HostPicker'] AffinityHostPicker choosing host 192.168.10.82 for context '[] /vmfs/volumes/501d996c-86c66169-eea2-005056  
	b007c1/My Awesome VM'  
	2012-08-11T00:32:50.281Z [F72236D0 info 'Host'] NFC creating session to target: 192.168.10.82 port: 902  
	2012-08-11T00:32:50.546Z [F72236D0 info 'RemoteDisk'] RemoteDisk: Opened path (/vmfs/volumes/501d996c-86c66169-eea2-005056b007c1/My Awesome VM/My Awesome VM.vmdk)  
	(longContentId='bf5a663487d2779dbba94022fffffffe')  
	

I went back to the host where the VM was running and checked replication again. It started the replication correctly.

	  
	~ # vim-cmd hbrsvc/vmreplica.getState 6  
	Retrieve VM running replication state:  
	The VM is configured for replication. Current replication state: Group: GID-3679986f-265f-4f56-8f1d-c7fcb2e9acc7 (generation=8295574602761)  
	Group State: full sync (16% done: checksummed 2.6 GB of 16 GB, transferred 0 bytes of 0 bytes)  
	DiskID RDID-ef948351-e4ef-48b1-a19b-78b119bb7490 State: full sync (checksummed 2.6 GB of 16 GB, transferred 0 bytes of 0 bytes)  
	~ # vim-cmd hbrsvc/vmreplica.queryReplicationState 6  
	Querying VM running replication state:  
	Current replication state:  
	State: syncing  
	Progress: 18% (checksum: 3224371200/17179869184; transfer: 0/0)  
	

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/vsphere-replication-shows-inactive-replication/" title=" vSphere Replication Shows Replication as &#8220;not active&#8221;" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:command line,hostd.log,logs,not active replication,srm,VRMS,VRS,vSphere Replication,blog;button:compact;">I was messing around in my SRM lab and ran into this issue. It is a common issue that we see, but it has different causes. I set up replication...</a>
</p>