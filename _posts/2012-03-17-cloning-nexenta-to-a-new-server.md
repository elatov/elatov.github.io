---
title: Cloning Nexenta to a New Server
author: Jarret Lavallee
layout: post
permalink: /2012/03/cloning-nexenta-to-a-new-server/
dsq_thread_id:
  - 1406879254
categories:
  - Home Lab
  - ZFS
tags:
  - apt-clone
  - dladm
  - Nexenta
  - syspool
  - ZFS
  - zpool
---
I have been upgrading my lab equipment and it has required me to move my back end <a title="NexentaStor" href="http://www.nexenta.com/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nexenta.com/']);">NexentaCore</a> from a physical server to a virtual server. Nexenta is great because it offers <a title="ZFS" href="http://en.wikipedia.org/wiki/ZFS" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/ZFS']);" target="_blank">ZFS</a> on a solaris with apt as a package manager. <a href="http://docs.oracle.com/cd/E19253-01/819-5461/zfsover-2/index.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19253-01/819-5461/zfsover-2/index.html']);" target="_blank">ZFS is great for storage.</a> It has <a title="Comstar" href="https://blogs.oracle.com/vreality/entry/storage_virtualization_with_comstar" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.oracle.com/vreality/entry/storage_virtualization_with_comstar']);" target="_blank">comstar</a>, a built in block level target that can handle FCOE,FC, and iSCSI. NFS and CIFS are also built into ZFS. Soon it will be <a href="http://zfsonlinux.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://zfsonlinux.org/']);" target="_blank">stable on Linux</a>. I would highly recommend ZFS for a storage platform.

Since this is my media server I did not want to reinstall until <a title="Illumian" href="http://illumian.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://illumian.org']);" target="_blank">Illumian</a> is actually stable and working. A clone seems to be the most logical way to migrate it. Since all of the data and export settings are stored on the disks, we can clone over the OS and everything else will come with the disks.

## Install NCP on another server

When installing Nexenta on the target server, the settings are not all that important. The purpose of installing it is to create a zpool mirror for the syspool and install grub. So this can be done with a live cd, but for simplicity I chose to install another system to leverage the installer.

During the install ensure that you set a static IP address. The installer will not start nwam by default, so the system will not get a DHCP lease.

If you chose DHCP, start NWAM after the install.

<pre>root@myhost:~# svcadm enable nwam</pre>

By default, PermitRootLogin will be set to &#8220;no&#8221;. We want to enable root login so that we can replicate the syspool over to this server.

<pre>root@myhost:~# sed -i 's/PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config
root@myhost:~# grep PermitRootLogin /etc/ssh/sshd_config
PermitRootLogin yes</pre>

Restart the ssh service

<pre>root@myhost:~# svcadm restart ssh</pre>

Find the IP address of this server if you used DHCP

<pre>root@myhost:~# ifconfig -a |grep inet
        inet 127.0.0.1 netmask ff000000
        inet 10.0.1.29 netmask ffffff00 broadcast 10.0.1.255
        inet6 ::1/128</pre>

Now confirm that root can ssh into the target server from the source server.

<pre>jarret@fileserver2:~$ ssh 10.0.1.29 -l root
Password:
Last login: Sat Mar 17 01:44:23 2012 from 10.0.1.83
root@myhost:~#</pre>

## Identify the active clone on the source system

On the source we want to identify the current boot volume so that we can clone it to the new server. To do this we will use apt-clone on the nexenta system. In illumian and NexentaStor 4.x this command will be replaced with beadm.

<pre>root@fileserver2:~# apt-clone -l
A C BOOTFS         TITLE
    rootfs-nmu-001 Rollback Checkpoint [nmu-001 : May 22 22:15:36 2011]
o o rootfs-nmu-003 Rollback Checkpoint [nmu-003 : Mar  6 17:46:55 2012]
    rootfs-nmu-000 Nexenta Core Platform "Hardy" [initial]
    rootfs-nmu-002 Upgrade Checkpoint [nmu-002 : Aug 28 17:38:01 2011]</pre>

In the case above rootfs-nmu-003 is the active clone. Lets check how much space that clone is taking.

<pre>root@fileserver2:~# zfs list syspool/rootfs-nmu-003
NAME                     USED  AVAIL  REFER  MOUNTPOINT
syspool/rootfs-nmu-003   546M  45.9G  3.56G  legacy</pre>

The target server will need to have at least 3.56G free. Lets confirm that it does.

<pre>root@myhost:~# zfs list syspool
NAME      USED  AVAIL  REFER  MOUNTPOINT
syspool  2.99G  4.82G    35K  none</pre>

It has enough space and when we clean up the fresh install of the new system, it will have plenty of free space.

## Take a snapshot on the active clone

Since we have identified our source clone to be syspool/rootfs-nmu-003, we need to take a snapshot that will be replicated to the target server.

<pre>root@fileserver2:~# zfs snapshot syspool/rootfs-nmu-003@replicate</pre>

Confirm that it was taken properly.

<pre>root@fileserver2:~# zfs list -t snapshot |grep "syspool/rootfs-nmu-003"
syspool/rootfs-nmu-003@replicate                                 1.00M      -  3.56G  -</pre>

## Replicate the snapshot over to the new server

There are multiple ways of replicating the data over to the new system. The easiest is to shut down the services that will change on the OS drive and do a single replication. Since the new server does not have the zpools yet, it is best to export them before doing the replication.

From the source server we will replicate the snapshot over to the new target servers syspool (See the <a title="ZFS(1M)" href="http://docs.oracle.com/cd/E19082-01/819-2240/zfs-1m/index.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19082-01/819-2240/zfs-1m/index.html']);" target="_blank">ZFS man page</a> for more details). The command below will take some time as it is sending the zfs volume over ssh. In this case we use the arcfour cipher because it should be a fast cipher (<a title="RC4" href="http://en.wikipedia.org/wiki/RC4" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/RC4']);" target="_blank">More details on arcfour</a>).

<pre>root@fileserver2:~# zfs send syspool/rootfs-nmu-003@replicate |ssh 10.0.1.29 -c arcfour "zfs recv syspool/rootfs-nmu-003"</pre>

While this is sending, we can check the progress on the target server. We can see below that it has created syspool/rootfs-nmu-003 and that it has already transferred 83.7M.

<pre>root@myhost:~# zfs list
NAME                     USED  AVAIL  REFER  MOUNTPOINT
syspool                 3.07G  4.74G    35K  none
syspool/dump             716M  4.74G   716M  -
syspool/rootfs-nmu-000  1.26G  4.74G  1010M  legacy
syspool/rootfs-nmu-003  83.7M  4.74G  83.7M  none
syspool/swap            1.03G  5.77G    16K  -</pre>

After the replication completes we should see the full size of the volume on the target server.

<pre>root@myhost:~# zfs list syspool/rootfs-nmu-003
NAME                     USED  AVAIL  REFER  MOUNTPOINT
syspool/rootfs-nmu-003  3.56G  1.26G  3.56G  none</pre>

## Activate the volume using apt-clone

Now that we have our data over on the target server, we need to activate the cloned volume to be the boot volume.

First lets check to see what the current active boot volume is.

<pre>root@myhost:~# apt-clone -l
A C BOOTFS         TITLE
o o rootfs-nmu-000 Nexenta Core Platform "Hardy" [initial]</pre>

Apt-clone does not list our replicated one, but when we go to activate it the new volume will be imported.

<pre>root@myhost:~# apt-clone -a rootfs-nmu-003
This will set default GRUB entry to 'syspool/rootfs-nmu-003'. Proceed ? (y/n) y

Upgrade changes for clone 'syspool/rootfs-nmu-003' has been activated.
Default GRUB entry '0' will boot 'syspool/rootfs-nmu-003' ZFS clone.</pre>

Grub is updated to include the new boot volume and it is set as the default option. Let confirm that that changes took.

<pre>root@myhost:~# apt-clone -l
A C BOOTFS         TITLE
o o rootfs-nmu-003 Nexenta Core Platform [nmu-003 : Mar 17 02:15:56 2012]
    rootfs-nmu-000 Upgrade Checkpoint [nmu-000 : Mar 16 20:58:06 2012]</pre>

## Reboot to confirm it is working

Now that we have activated our new volume as the boot volume, we can reboot the system and confirm that it comes up with the configuration. The default boot volume in grub is the one we just activated, so there should be no need for manual intervention during the boot. If the boot fails, you can select rootfs-nmu-000 to boot into the fresh install and troubleshoot.

<pre>root@myhost:~# reboot
Connection to 10.0.1.29 closed by remote host.
Connection to 10.0.1.29 closed.</pre>

When the target system boots, it should come up with the boot volume from the source server. Network should be offline unless you were using DHCP before the migration, so you will want to login on the console.

<pre>ZFS Open Storage Appliance (v3.0.5)
fileserver2 console login:</pre>

We can already see that the hostname has changed to the source&#8217;s. If you did not export the zpools before the migration, they will likely be showing failures now.

<pre>root@fileserver2:~# zpool status data
  pool: data
 state: UNAVAIL
status: One or more devices could not be opened.  There are insufficient
        replicas for the pool to continue functioning.
action: Attach the missing device and online it using 'zpool online'.
   see: http://www.sun.com/msg/ZFS-8000-3C
 scan: none requested
config:

        NAME           STATE     READ WRITE CKSUM
        data           UNAVAIL      0     0     0  insufficient replicas
          raidz1-0     UNAVAIL      0     0     0  insufficient replicas
            c5t4d0     UNAVAIL      0     0     0  cannot open
            c5t0d0     UNAVAIL      0     0     0  cannot open
            c5t5d0     UNAVAIL      0     0     0  cannot open
            c5t6d0     UNAVAIL      0     0     0  cannot open
          raidz1-1     UNAVAIL      0     0     0  insufficient replicas
            c4t15d0    UNAVAIL      0     0     0  cannot open
            c5t3d0     UNAVAIL      0     0     0  cannot open
            c4t16d0    UNAVAIL      0     0     0  cannot open
            c5t7d0     UNAVAIL      0     0     0  cannot open
          raidz1-2     UNAVAIL      0     0     0  insufficient replicas
            c4t9d0     UNAVAIL      0     0     0  cannot open
            c4t10d0    UNAVAIL      0     0     0  cannot open
            c5t1d0     UNAVAIL      0     0     0  cannot open
            c5t2d0     UNAVAIL      0     0     0  cannot open</pre>

Export the missing pools.

<pre>root@fileserver2:~# zpool export data
root@fileserver2:~# zpool list
NAME      SIZE  ALLOC   FREE    CAP  DEDUP  HEALTH  ALTROOT
syspool  7.94G  5.62G  2.32G    70%  1.00x  ONLINE  -</pre>

## Fix the network on the target system

The hardware has changed so the NICs will have new MACs and will be numbered differently. Network will likely not work until the interfaces are changed back to the original names or the hostname.interface files are renamed. I chose to rename the interfaces.

Show the current interface names.

<pre>root@fileserver2:~# dladm show-link
LINK        CLASS     MTU    STATE    BRIDGE     OVER
e1000g8     phys      16298  unknown    --         --</pre>

Rename the interface.

<pre>root@fileserver2:~# dladm rename-link e1000g8 e1000g0
root@fileserver2:~# dladm show-link
LINK        CLASS     MTU    STATE    BRIDGE     OVER
e1000g0     phys      16298  unknown    --         --</pre>

At this point I would reboot to confirm that it comes online as expected before cleaning up in the next section.

## Destroy the old clones

Now that we know everything is working on the target server, its time to clean up the base installation that is taking up 1.2G on the boot syspool.

**NOTE:** Make sure that these commands are run on the target server.

Confirm that we still have the new volume as the active one.

<pre>root@fileserver2:~# apt-clone -l
A C BOOTFS         TITLE
o o rootfs-nmu-003 Nexenta Core Platform [nmu-003 : Mar 17 02:15:56 2012]
    rootfs-nmu-000 Upgrade Checkpoint [nmu-000 : Mar 16 20:58:06 2012]</pre>

Remove rootfs-nmu-000 from grub and apt-clone.

<pre>root@fileserver2:~# apt-clone -r rootfs-nmu-000
This will destroy clone 'syspool/rootfs-nmu-000'. Proceed ? (y/n) y

Upgrade changes for clone 'syspool/rootfs-nmu-000' now rolled back/destroyed.</pre>

Delete rootfs-nmu-000 from the syspool.

<pre>root@fileserver2:~# zfs destroy -r syspool/rootfs-nmu-000</pre>

Confirm that the space is reclaimed.

<pre>root@fileserver2:~# zfs list
NAME                     USED  AVAIL  REFER  MOUNTPOINT
syspool                 5.39G  2.42G  35.5K  legacy
syspool/dump             716M  2.42G   716M  -
syspool/rootfs-nmu-003  3.66G  2.42G  3.55G  legacy
syspool/swap            1.03G  3.45G  5.61M  -</pre>

Next lets cleanup the snapshot we created on the target server syspool/rootfs-nmu-003@replicate.

<pre>root@fileserver2:~# zfs destroy syspool/rootfs-nmu-003@replicate</pre>

Now the new system should be booting from the replicated boot volume from the source server. You can now export the zpools on the source server, move disks and import them on the target server.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESXi Backups with ZFS and XSIBackup" href="http://virtuallyhyper.com/2014/02/esxi-backups-zfs-xsibackup/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/02/esxi-backups-zfs-xsibackup/']);" rel="bookmark">ESXi Backups with ZFS and XSIBackup</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="ZFS iSCSI Benchmark Tests on ESX" href="http://virtuallyhyper.com/2014/01/zfs-iscsi-benchmarks-tests/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/01/zfs-iscsi-benchmarks-tests/']);" rel="bookmark">ZFS iSCSI Benchmark Tests on ESX</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing and Configuring OmniOS" href="http://virtuallyhyper.com/2013/04/installing-and-configuring-omnios/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/installing-and-configuring-omnios/']);" rel="bookmark">Installing and Configuring OmniOS</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Getting OpenIndiana Back to it&#8217;s Original State After Updating by Doing a Clean Install" href="http://virtuallyhyper.com/2012/09/getting-openindiana-back-to-its-original-state-after-updating-by-doing-a-clean-install/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/getting-openindiana-back-to-its-original-state-after-updating-by-doing-a-clean-install/']);" rel="bookmark">Getting OpenIndiana Back to it&#8217;s Original State After Updating by Doing a Clean Install</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Migrating a ZFS Pool with ZFS Volumes Used for NFS Shares and iSCSI Comstar Volumes" href="http://virtuallyhyper.com/2012/08/migrating-a-zfs-pool-with-zfs-volumes-used-for-nfs-shares-and-iscsi-comstar-volumes/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/migrating-a-zfs-pool-with-zfs-volumes-used-for-nfs-shares-and-iscsi-comstar-volumes/']);" rel="bookmark">Migrating a ZFS Pool with ZFS Volumes Used for NFS Shares and iSCSI Comstar Volumes</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/cloning-nexenta-to-a-new-server/" title=" Cloning Nexenta to a New Server" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:apt-clone,dladm,Nexenta,syspool,ZFS,zpool,blog;button:compact;">If you had a chance to read my previous blog regarding migrating the root ZFS pool to a smaller drive, first of all I wanted to apologize for the longevity...</a>
</p>