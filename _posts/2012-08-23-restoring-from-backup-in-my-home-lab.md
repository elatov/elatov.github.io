---
title: Restoring from Backup in my Home Lab
author: Jarret Lavallee
layout: post
permalink: /2012/08/restoring-from-backup-in-my-home-lab/
dsq_thread_id:
  - 1404673481
categories:
  - Home Lab
  - VMware
  - ZFS
tags:
  - COMSTAR
  - iSCSI
  - Nexenta
  - replication
  - sbdadm
  - stmfadm
  - svcffg
  - vdev
  - ZFS
  - zpool
  - zvol
---
Today I woke up to an email telling me that 3 drives failed in my Nexenta Server. This is a result of using old green drives in a raid and heavily using them for years. Unfortunately these drives were in the zpool that served up my lab storage (and out of warranty). I had the zpool as a set of mirrors (like raid 10), so I would have been covered for multiple drive failures. The problem comes in when you lose both disks in a mirror. Sadly I did lose both disks in a single vdev, so the whole zpool went offline. 

After fumbling around trying to get the data off the drives for an hour, I decided to go with my recovery plan. Since this is a reproduction lab I did not put a large emphasis on a recovery plan. I did however set up a simple backup plan that I have previously tested. My backups are simple san based replicas with ZFS. I run a slightly modified version of <a href="http://blog.laspina.ca/ubiquitous/provisioning_disaster_recovery_with_zfs" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.laspina.ca/ubiquitous/provisioning_disaster_recovery_with_zfs']);" target="_blank">this replication script</a>. I modified it to work with zvols and some other small tweaks to the local and remote replication. It is set up to replicate the zvols to another zpool every night at 2 am. So I have an RPO of 1 day, but my full recovery RTO is very high. I do have another alternative though. I have the zvols replicated to another zpool, so I could promote those zvols and present them back to the hosts. Since this is a lab, I decided to just replicate the zvols back to the non failed disks. 

This morning I took the disks that I had left and created a new zpool. With only 6 disks in use I will have a significant decrease in IOPs, but with ZFS I can always add in more <a href="https://blogs.oracle.com/7000tips/entry/vdev_what_is_a_vdev" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.oracle.com/7000tips/entry/vdev_what_is_a_vdev']);" target="_blank">vdevs</a> later.

[code]  
\# zpool status vms  
pool: vms  
state: ONLINE  
scan: none requested  
config:

NAME STATE READ WRITE CKSUM  
vms ONLINE 0 0 0  
mirror-0 ONLINE 0 0 0  
c11t1d0 ONLINE 0 0 0  
c11t6d0 ONLINE 0 0 0  
mirror-1 ONLINE 0 0 0  
c11t7d0 ONLINE 0 0 0  
c12t7d0 ONLINE 0 0 0  
mirror-2 ONLINE 0 0 0  
c9t7d0 ONLINE 0 0 0  
c9t9d0 ONLINE 0 0 0  
cache  
c8t2d0 ONLINE 0 0 0  
spares  
c9t14d0 AVAIL 

errors: No known data errors  
[/code]

Now here are the replicated <a href="http://www.cuddletech.com/blog/pivot/entry.php?id=729" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cuddletech.com/blog/pivot/entry.php?id=729']);" target="_blank">zvols</a>. 

[code]  
\# zfs list |grep vms  
data/vms 1.87T 4.58T 68.8K /data/vms  
data/vms/iscsi_dev 724G 4.58T 278G -  
data/vms/iscsi_dev2 322G 4.58T 197G -  
data/vms/iscsi_infra 312G 4.58T 91.3G -  
data/vms/iscsi_prod 267G 4.58T 190G -  
data/vms/iscsi_templates 41.8G 4.58T 41.8G -  
data/vms/iscsi_view 160G 4.58T 62.6G -  
data/vms/nfs\_templates 89.0G 4.58T 82.0G /data/vms/nfs\_templates  
[/code]

Only about half of the data is current and the other half is snapshot data from the last 30 days. I only need to replicate about 942.7GB of data over to the newly created zpool. My replication rate is generally 100MB/s, so replicating this to the new zpool should take a little under 3 hours. 

First we need to find the most recent snapshot.  
[code]  
\# zfs list -t snapshot |grep 08-19  
data/vms/iscsi_dev@08-19-12-02:02 0 - 278G -  
data/vms/iscsi_dev2@08-19-12-02:02 0 - 197G -  
data/vms/iscsi_infra@08-19-12-02:02 0 - 91.3G -  
data/vms/iscsi_prod@08-19-12-02:02 0 - 190G -  
data/vms/iscsi_view@08-19-12-02:02 0 - 62.6G -  
data/vms/nfs_templates@08-19-12-02:02 0 - 82.0G -  
[/code]

Next we need to start the replication to the new zpool. 

[code]  
\# zfs send data/vms/iscsi\_dev@08-19-12-02:02 | zfs recv vms/iscsi\_dev  
\# zfs send data/vms/iscsi\_dev2@08-19-12-02:02 | zfs recv vms/iscsi\_dev2  
\# zfs send data/vms/iscsi\_infra@08-19-12-02:02 | zfs recv vms/iscsi\_infra  
\# zfs send data/vms/nfs\_templates@08-19-12-02:02 | zfs recv vms/nfs\_templates  
\# zfs send data/vms/iscsi\_prod@08-19-12-02:02 |zfs recv vms/iscsi\_prod  
\# zfs send data/vms/iscsi\_view@08-19-12-02:02 | zfs recv vms/iscsi\_view  
[/code]

Now that the devices have been replicated over to the new zpool we need to set up the logical units and create views. First thing I tried was to import the logical unit with the same GUID.

[code]  
\# stmfadm import-lu /dev/zvol/rdsk/vms/iscsi_infra  
stmfadm: meta file error  
[/code]

The problem above is that it the zvol is not detected as a logical unit. Instead of importing the zvol as an existing logical unit, we can create the Logical unit with the same GUID. The modified version of zfs-daily.sh exports the <a href="http://thegreyblog.blogspot.com/2010/02/setting-up-solaris-comstar-and.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://thegreyblog.blogspot.com/2010/02/setting-up-solaris-comstar-and.html']);" target="_blank">COMSTAR</a> configuration and the GUIDs and source path. Here is the output of &#8220;sbdadm list-lu&#8221;, which is saved by the script.

[code]  
\# cat list-lu.08-19-12-02\:02 

Found 11 LU(s)

GUID DATA SIZE SOURCE  
\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---\---\---\--- \---\---\---\---\----  
600144f070cc440000004cd42fa10001 268435456000 /dev/zvol/rdsk/vms/iscsi_vdr2  
600144f070cc440000004cd432260002 1099511627776 /dev/zvol/rdsk/vms/iscsi_dev2  
600144f070cc440000004dd9c9310002 1099511627776 /dev/zvol/rdsk/vms/iscsi_dev  
600144f070cc440000004dd9c9460003 268435456000 /dev/zvol/rdsk/vms/iscsi_infra  
600144f070cc440000004dd9c95f0004 268435456000 /dev/zvol/rdsk/vms/iscsi_prod  
600144f070cc440000004dda7ec40006 268435456000 /dev/zvol/rdsk/vms/iscsi_view  
600144f070cc440000004ddaf6a00008 268435456000 /dev/zvol/rdsk/vms/iscsi_templates  
600144f0e8cb470000004f7f17a70003 26843545600 /dev/zvol/rdsk/vms/iscsi_test  
600144f0e8cb470000004f9ee2590005 268435456000 /dev/zvol/rdsk/data/vdr/iscsi_dedup  
600144f0e8cb470000004fd77a6b0001 107374182400 /dev/zvol/rdsk/vms/iscsi\_vcd15\_infra  
600144f0e8cb470000004fd77a8f0002 107374182400 /dev/zvol/rdsk/vms/iscsi\_vcd15\_vapps  
[/code]

If we did not have this information, it would not be a big deal. The GUID is the NAA of the LUN, so the idea is to set the same GUID to keep the same NAA and thus we would not have to resignature the datastores. 

So let&#8217;s create the logical units with the same GUID. 

[code]  
\# stmfadm create-lu -p GUID=600144f070cc440000004dd9c9460003 /dev/zvol/rdsk/vms/iscsi_infra  
Logical unit created: 600144F070CC440000004DD9C9460003  
[/code]

The old views in COMSTAR should still be there, but we can import it with the export created in the zfs-daily.sh script. More information on exporting and importing COMSTAR config can be found <a href="http://docs.oracle.com/cd/E23824_01/html/821-1459/fnnop.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E23824_01/html/821-1459/fnnop.html']);" target="_blank">here</a>.

[code]  
\# svccfg import COMSTAR.backup.08-19-12-02\:02  
[/code]

Let&#8217;s list the logical units and the views.

[code]  
\# sbdadm list-lu

Found 5 LU(s)

GUID DATA SIZE SOURCE  
\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---\---\---\--- \---\---\---\---\----  
600144f070cc440000004cd432260002 1099511627776 /dev/zvol/rdsk/vms/iscsi_dev2  
600144f070cc440000004dd9c9310002 1099511627776 /dev/zvol/rdsk/vms/iscsi_dev  
600144f070cc440000004dd9c9460003 268435456000 /dev/zvol/rdsk/vms/iscsi_infra  
600144f070cc440000004dd9c95f0004 268435456000 /dev/zvol/rdsk/vms/iscsi_prod  
600144f070cc440000004dda7ec40006 268435456000 /dev/zvol/rdsk/vms/iscsi_view  
\# stmfadm list-lu |cut -d " " -f 3 |xargs -n 1 stmfadm list-view -l  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 2  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 3  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 0  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 4  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 1  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 11  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 12  
View Entry: 0  
Host group : esx5  
Target group : esx4  
LUN : 8

[/code]

Finally we can setup the NFS exports for the NFS datastores.

[code]  
\# zfs set sharenfs=rw,nosuid,root=@192.168.5.0/24:@10.0.0.0/24:@192.168.10.0/24:@192.168.11.0/24 vms/nfs_templates  
\# zfs get sharenfs vms/nfs_templates  
NAME PROPERTY VALUE SOURCE  
vms/nfs_templates sharenfs rw,nosuid,root=@192.168.5.0/24:@10.0.0.0/24:@192.168.10.0/24:@192.168.11.0/24 local  
[/code]

After a quick reboot of the APD&#8217;ed ESX hosts, we can see the storage again.

[code]  
\# esxcfg-scsidevs -m  
naa.600144f070cc440000004dd9c95f0004:1 /vmfs/devices/disks/naa.600144f070cc440000004dd9c95f0004:1 4dd9cc25-8e513da5-6ede-00e08176b934 0 iscsi_prod  
naa.600144f070cc440000004dda7ec40006:1 /vmfs/devices/disks/naa.600144f070cc440000004dda7ec40006:1 4dda8153-a7bc828b-071e-00e08176b934 0 iscsi_view  
naa.600144f070cc440000004dd9c9460003:1 /vmfs/devices/disks/naa.600144f070cc440000004dd9c9460003:1 4dd9cc03-9964340d-0e96-00e08176b934 0 iscsi_infra  
[/code]

I started booting my VMs and took a look at esxtop to see how my latency was. The pool was cut down from 5 mirrors to 3 mirrors, so I expect to have much fewer IOPs. The nice thing about ZFS is that there is a fair amount of caching, so this will help offset the poor performance of the disks. In the esxtop output below, we can see that there is some latency, but this will decrease as my read cache fills up and the boot storm is over.

[code]  
2:58:48pm up 14 min, 228 worlds; CPU load average: 1.19, 0.88, 0.00

DEVICE DQLEN WQLEN ACTV QUED %USD LOAD CMDS/s READS/s WRITES/s MBREAD/s MBWRTN/s DAVG/cmd KAVG/cmd GAVG/cmd  
naa.600144f070cc440000004cd432260002 32 - 0 0 0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00  
naa.600144f070cc440000004dd9c9310002 32 - 0 0 0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00  
naa.600144f070cc440000004dd9c9460003 128 - 3 0 2 0.02 342.57 290.54 52.03 10.42 0.28 5.43 0.01 5.44  
naa.600144f070cc440000004dd9c95f0004 128 - 0 0 0 0.00 3.97 0.60 3.38 0.00 0.02 10.76 0.01 10.77  
naa.600144f070cc440000004dda7ec40006 128 - 2 0 1 0.02 402.74 399.77 2.98 6.31 0.03 4.56 0.01 4.57  
t10.ATA__\_\\_\_OCZ\_VERTEX2DTURBO\\_\_\_____ 1 - 0 0 0 0.00 0.40 0.20 0.20 0.00 0.00 16.67 0.02 16.69  
t10.ATA__\_\\_\_OCZ\_VERTEX2DTURBO\\_\_\_____ 1 - 0 0 0 0.00 144.18 0.40 143.78 0.00 16.89 0.52 3.62 4.14  
{NFS}isos - - 0 \- - - 0.00 0.00 0.00 0.00 0.00 - - 0.00  
{NFS}vmware isos - - 0 \- - - 0.00 0.00 0.00 0.00 0.00 - - 0.00  
[/code]

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/restoring-from-backup-in-my-home-lab/" title=" Restoring from Backup in my Home Lab" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:COMSTAR,iSCSI,Nexenta,replication,sbdadm,stmfadm,svcffg,vdev,ZFS,zpool,zvol,blog;button:compact;">Today I woke up to an email telling me that 3 drives failed in my Nexenta Server. This is a result of using old green drives in a raid and...</a>
</p>