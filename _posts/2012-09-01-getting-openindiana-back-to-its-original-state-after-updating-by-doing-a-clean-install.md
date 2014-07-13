---
title: "Getting OpenIndiana Back to it's Original State After Updating by Doing a Clean Install"
author: Karim Elatov
layout: post
permalink: /2012/09/getting-openindiana-back-to-its-original-state-after-updating-by-doing-a-clean-install/
categories: ['home_lab', 'storage', 'vmware', 'zfs']
tags: [ 'comstar', 'opensolaris', 'smf', 'iscsi'] 
---

I decided to update from **oi_151a4** to **oi_151a5**. I tried using **pkg**:

    ~# pkg image-update


I followed the instruction laid out in "[Upgrading OpenIndiana](http://wiki.openindiana.org/oi/Upgrading+OpenIndiana)", but nothing worked. I re-setup my publisher, I even tried different publisher, but it just wouldn't update. The above link is actually a forum and people had similar issues and one person fixed his issue by running the following:

    ~# pkg rebuild-index


But unfortunately it didn't help out. So I downloaded the [previous](http://dlc.openindiana.org/isos/151a5/oi-dev-151a5-live-x86.iso) post), I setup up my system pool on the 8GB drive and my data pool to be on the other drive. So during the clean install I just selected the drive which had my system pool and the install just wiped that drive and setup a new pool on it. But my data pool was still in tact. After the install/update finished, I saw the following:

    root@openindiana:~# zpool status
    pool: rpool
    state: ONLINE
    scan: none requested
    config:

    NAME STATE READ WRITE CKSUM
    rpool ONLINE 0 0 0
    c5t0d0s0 ONLINE 0 0 0

    errors: No known data errors

    root@openindiana:~# zfs list
    NAME USED AVAIL REFER MOUNTPOINT
    rpool 3.64G 4.17G 45.5K /rpool
    rpool/ROOT 1.58G 4.17G 31K legacy
    rpool/ROOT/openindiana 1.58G 4.17G 1.57G /
    rpool/dump 1.00G 4.17G 1.00G -
    rpool/export 98K 4.17G 32K /export
    rpool/export/home 66K 4.17G 32K /export/home
    rpool/export/home/elatov 34K 4.17G 34K /export/home/elatov
    rpool/swap 1.06G 5.10G 132M -

    root@openindiana:~# uname -a
    SunOS openindiana 5.11 oi_151a5 i86pc i386 i86pc Solaris


and my network setup was gone as well (This was because during the install I selected "Don't setup Networking"):

    root@openindiana:~# ifconfig -a
    lo0: flags=2001000849<UP,LOOPBACK,RUNNING,MULTICAST,IPv4,VIRTUAL> mtu 8232 index 1
    inet 127.0.0.1 netmask ff000000
    lo0: flags=2002000849<UP,LOOPBACK,RUNNING,MULTICAST,IPv6,VIRTUAL> mtu 8252 index 1
    inet6 ::1/128


My NIC was there it just wasn't setup:

    root@openindiana:~# dladm show-phys
    LINK MEDIA STATE SPEED DUPLEX DEVICE
    e1000g0 Ethernet unknown 0 half e1000g0


Luckily the **nwam** service was already disabled and the **networking** service was enabled:

    root@openindiana:~# svcs network/physical
    STATE STIME FMRI
    disabled 6:35:13 svc:/network/physical:nwam
    online 6:35:21 svc:/network/physical:default


So first I setup networking, and rebooted the OI VM:

    root@openindiana:~# echo "192.168.1.107" > /etc/hostname.e1000g0
    root@openindiana:~# echo "192.168.1.0 255.255.255.0 >> /etc/netmasks
    root@openindiana:~# echo "192.168.1.1 > /etc/defaultrouter
    root@openindiana:~# echo "search my.domain.com" > /etc/resolv.conf
    root@openindiana:~# echo "nameserver 10.131.23.175" >> /etc/resolv.conf
    root@openindiana:~# echo "nameserver 10.131.23.176" >> /etc/resolv.conf
    root@openindiana:~# cp /etc/nsswitch.dns /etc/nsswitch.conf
    root@openindiana:~# svcadm enable dns/client
    root@openindiana:~# init 6


After I rebooted I saw the following:

    root@openindiana:~# ifconfig -a
    lo0: flags=2001000849<UP,LOOPBACK,RUNNING,MULTICAST,IPv4,VIRTUAL> mtu 8232 index 1
    inet 127.0.0.1 netmask ff000000
    e1000g0: flags=1000843<UP,BROADCAST,RUNNING,MULTICAST,IPv4> mtu 1500 index 2
    inet 192.168.1.107 netmask ffffff00 broadcast 192.168.1.255
    ether 0:50:56:17:14:bf
    lo0: flags=2002000849<UP,LOOPBACK,RUNNING,MULTICAST,IPv6,VIRTUAL> mtu 8252 index 1
    inet6 ::1/128

    root@openindiana:~# netstat -rn

    Routing Table: IPv4
    Destination Gateway Flags Ref Use Interface
    -------------------- -------------------- ----- ----- ---------- ---------
    default 192.168.1.1 UG 1 0
    127.0.0.1 127.0.0.1 UH 2 36 lo0
    192.168.1.0 192.168.1.107 U 6 738 e1000g0

    Routing Table: IPv6
    Destination/Mask Gateway Flags Ref Use If
    --------------------------- --------------------------- ----- --- ------- -----
    ::1 ::1 UH 2 0 lo0

    root@openindiana:~# nslookup pkg.openindiana.org
    Server: 10.131.23.175
    Address: 10.131.23.175#53

    Non-authoritative answer:
    Name: pkg.openindiana.org
    Address: 91.194.74.133


The VM was back on the network and I could now *ssh* to it. Now to see if we can **import** our data ZFS pool:

    root@openindiana:~# zpool import
    pool: data
    id: 3063016645842242775
    state: ONLINE
    status: The pool was last accessed by another system.
    action: The pool can be imported using its name or numeric identifier and
    the '-f' flag.
    see: http://illumos.org/msg/ZFS-8000-EY
    config:

    data ONLINE
    c4t0d0s0 ONLINE


Now let's go ahead and import the pool:

    root@openindiana:~# zpool import -f data
    root@openindiana:~# zpool status
    pool: data
    state: ONLINE
    status: The pool is formatted using an older on-disk format. The pool can
    still be used, but some features are unavailable.
    action: Upgrade the pool using 'zpool upgrade'. Once this is done, the
    pool will no longer be accessible on older software versions.
    scan: none requested
    config:

    NAME STATE READ WRITE CKSUM
    data ONLINE 0 0 0
    c4t0d0s0 ONLINE 0 0 0

    errors: No known data errors

    pool: rpool
    state: ONLINE
    scan: none requested
    config:

    NAME STATE READ WRITE CKSUM
    rpool ONLINE 0 0 0
    c5t0d0s0 ONLINE 0 0 0

    errors: No known data errors


So the pool imported fine but it was asking us to update the pool, cause it was running an older version. Just to make sure our ZFS volumes were okay:

    root@openindiana:~# zfs list
    NAME USED AVAIL REFER MOUNTPOINT
    data 238G 11.8G 46K /data
    data/iscsi_share 103G 110G 4.71G -
    data/iscsi_share2 134G 146G 26.5M -
    data/nfs_share 1000M 11.8G 1000M /data/nfs_share
    rpool 3.65G 4.16G 45.5K /rpool
    rpool/ROOT 1.59G 4.16G 31K legacy
    rpool/ROOT/openindiana 1.59G 4.16G 1.58G /
    rpool/dump 1.00G 4.16G 1.00G -
    rpool/export 98.5K 4.16G 32K /export
    rpool/export/home 66.5K 4.16G 32K /export/home
    rpool/export/home/elatov 34.5K 4.16G 34.5K /export/home/elatov
    rpool/swap 1.06G 5.10G 132M -


That looked good. Checking the current versions of my two zpools, I saw the following:

    root@openindiana:~# zpool get version data
    NAME PROPERTY VALUE SOURCE
    data version 28 local
    root@openindiana:~# zpool get version rpool
    NAME PROPERTY VALUE SOURCE
    rpool version - default


Notice that the new pool doesn't have a version. This is expected, from the **oi_151a5** release notes:

> This release includes the async zfs destroy feature from illumos that comes with a new zpool version.
>
> Remember upgrading a zpool is a non-reversable command and any zpools you upgrade may not be readable with previous versions of OI, including other BEs on the same system.
>
> The ZFS feature flags concept is documented here:
> http://blog.delphix.com/csiden/files/2012/01/ZFS_Feature_Flags.pdf.
>
> In this context the "zpool version" becomes a legacy concept, and the number is set to 5000 on existing pools during a "zpool upgrade" run.

So in this version of OpenIndiana zpool versions become a "legacy concept". I went a ahead and updated by data pool:

    root@openindiana:~# zpool upgrade data
    This system supports ZFS pool feature flags.

    Successfully upgraded 'data' from version 28 to version 5000


Now no more warnings are given when checking the status of the zpool:

    root@openindiana:~# zpool status
    pool: data
    state: ONLINE
    scan: none requested
    config:

    NAME STATE READ WRITE CKSUM
    data ONLINE 0 0 0
    c4t0d0s0 ONLINE 0 0 0

    errors: No known data errors

    pool: rpool
    state: ONLINE
    scan: none requested
    config:

    NAME STATE READ WRITE CKSUM
    rpool ONLINE 0 0 0
    c5t0d0s0 ONLINE 0 0 0

    errors: No known data errors


That is all good. I was using Comstar to serve my ZFS volumes as iSCSI LUNs, as I was checking to make sure I have the two components installed, I noticed that **iscsi/target** was not installed:

    root@openindiana:~# svcs -a | grep stmf
    disabled 11:19:18 svc:/system/stmf:default
    root@openindiana:~# svcs -a | grep iscsi
    online 11:19:22 svc:/network/iscsi/initiator:default


and the **smtf** service is disabled. I first wanted to install the **iscsi/target** package, so I checked out my *publishers*.

    root@openindiana:~# pkg publisher
    PUBLISHER TYPE STATUS URI
    openindiana.org origin online http://pkg.openindiana.org/dev/
    opensolaris.org origin online http://pkg.openindiana.org/legacy/


I realized that I had the opensolaris publisher. From ""[Upgrading OpenIndiana](http://wiki.openindiana.org/oi/Upgrading+OpenIndiana)":

> **opensolaris.org publisher**
> If you currently have the opensolaris.org publisher set, we would highly recommend unsetting it by running:
>
>     # pfexec pkg unset-publisher opensolaris.org
>

So I went ahead and disabled it:

    root@openindiana:~# pkg unset-publisher opensolaris.org
    root@openindiana:~# pkg publisher
    PUBLISHER TYPE STATUS URI
    openindiana.org origin online http://pkg.openindiana.org/dev/


Then I wanted to install the comstar packages. From "[Configuring COMSTAR (Task Map)](http://docs.oracle.com/cd/E19963-01/html/821-1459/fncpi.html)":

> Install the COMSTAR storage server software.
>
>     target# pkg install storage-server
>

I was actually need to use a proxy to get outside of our local network, so here is what I ran to install Comstar:

    root@openindiana:~# http_proxy=http://proxy.mycompany.com:3128 pkg install storage-server
    Packages to install: 21
    Create boot environment: No
    Create backup boot environment: Yes
    Services to change: 1

    DOWNLOAD PKGS FILES XFER (MB)
    Completed 21/21 903/903 48.8/48.8

    PHASE ACTIONS
    Install Phase 1816/1816

    PHASE ITEMS
    Package State Update Phase 21/21
    Image State Update Phase 2/2


and now to confirm I have all the components installed:

    root@openindiana:~# svcs -a | egrep 'iscsi|stmf'
    disabled 11:19:18 svc:/system/stmf:default
    disabled 12:11:36 svc:/network/iscsi/target:default
    online 11:19:22 svc:/network/iscsi/initiator:default


I won't be using the initiator service from this machine it's just going to be an iSCSI target, so I did the following:

    root@openindiana:~# svcadm enable stmf
    root@openindiana:~# svcadm enable iscsi/target
    root@openindiana:~# svcadm disable iscsi/initiator


First let's create an iSCSI target:

    root@openindiana:~# itadm create-target
    Target iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb successfully created


Let's make sure it's created:

    root@openindiana:~# itadm list-target -v
    TARGET NAME STATE SESSIONS
    iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb online 0
    alias: -
    auth: none (defaults)
    targetchapuser: -
    targetchapsecret: unset
    tpg-tags: default


Next let's create a host group so we can add our esx hosts to it:

    root@openindiana:~# stmfadm create-hg esx


Next go to each host and find out their corresponding IQNs, here are mine:

    ~ # vmkiscsi-tool -I -l vmhba33
    iSCSI Node Name: iqn.1998-01.com.vmware:localhost-428367f3

    [root@esx40u1 ~]# vmkiscsi-tool -I -l vmhba33
    iSCSI Node Name: iqn.1998-01.com.vmware:esx40u1-5da6606e

    ~ # vmkiscsi-tool -I -l vmhba33
    iSCSI Node Name: iqn.1998-01.com.vmware:localhost-57ecf193


Then add each IQN as an initiator and add it to our host group:

    root@openindiana:~# itadm create-initiator iqn.1998-01.com.vmware:esx40u1-5da6606e
    root@openindiana:~# itadm create-initiator iqn.1998-01.com.vmware:localhost-57ecf193
    root@openindiana:~# itadm create-initiator iqn.1998-01.com.vmware:localhost-428367f3

    root@openindiana:~# stmfadm add-hg-member -g esx iqn.1998-01.com.vmware:esx40u1-5da6606e
    root@openindiana:~# stmfadm add-hg-member -g esx iqn.1998-01.com.vmware:localhost-57ecf193
    root@openindiana:~# stmfadm add-hg-member -g esx iqn.1998-01.com.vmware:localhost-428367f3


Let's make sure they are added properly:

    root@openindiana:~# stmfadm list-hg -v
    Host Group: esx
    Member: iqn.1998-01.com.vmware:esx40u1-5da6606e
    Member: iqn.1998-01.com.vmware:localhost-57ecf193
    Member: iqn.1998-01.com.vmware:localhost-428367f3


Now we can re-add our ZFS volumes to Comstar using the old GUID. I actually had to do this in this [previous](/2012/08/migrating-a-zfs-pool-with-zfs-volumes-used-for-nfs-shares-and-iscsi-comstar-volumes/) post of mine. So here is what I did to add my LUNs:

    root@openindiana:~# stmfadm create-lu -p guid=600144f0928c010000004fc511ec0001 /dev/zvol/rdsk/data/iscsi_share
    Logical unit created: 600144F0928C010000004FC511EC0001

    root@openindiana:~# stmfadm create-lu -p guid=600144f0928c010000004fc90a3a0001 /dev/zvol/rdsk/data/iscsi_share2
    Logical unit created: 600144F0928C010000004FC90A3A0001


List your LUNs to make sure they are there:

    root@openindiana:~# sbdadm list-lu

    Found 2 LU(s)

    GUID DATA SIZE SOURCE
    -------------------------------- ------------------- ----------------
    600144f0928c010000004fc511ec0001 107374182400 /dev/zvol/rdsk/data/iscsi_share
    600144f0928c010000004fc90a3a0001 139586437120 /dev/zvol/rdsk/data/iscsi_share2


That looks good, now let's add a "view" to allow the hostgroup "esx" to access the above LUNS:

    root@openindiana:~# stmfadm add-view -h esx 600144f0928c010000004fc511ec0001
    root@openindiana:~# stmfadm add-view -h esx 600144f0928c010000004fc90a3a0001


Check to make sure the views looks good:

    root@openindiana:~# stmfadm list-view -l 600144f0928c010000004fc511ec0001
    View Entry: 0
    Host group : esx
    Target group : All
    LUN : 0

    root@openindiana:~# stmfadm list-view -l 600144f0928c010000004fc90a3a0001
    View Entry: 0
    Host group : esx
    Target group : All
    LUN : 1


That looks good. After doing a rescan on all the hosts, my LUNs came back without any issues:

    ~ # esxcfg-rescan
    ~ # esxcfg-scsidevs -m | grep OI
    naa.600144f0928c010000004fc511ec0001:1 /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001:1 4fc903bb-6298d17d-8417-00505617149e 0 OI_LUN0


I was using one as a VMFS datastore (OI_LUN0) and the other as an RDM. Here are both of the LUNs on the host:

    ~ # esxcfg-scsidevs -c | grep OI
    naa.600144f0928c010000004fc511ec0001 Direct-Access /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001 102400MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc511ec0001)
    naa.600144f0928c010000004fc90a3a0001 Direct-Access /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001 133120MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc90a3a0001)


the NAAs even match :) For NFS, nothing had to be done since the path stayed the same:

    root@openindiana:~# zfs get sharenfs data/nfs_share
    NAME PROPERTY VALUE SOURCE
    data/nfs_share sharenfs rw,root=192.168.1.108 local
    root@openindiana:~# sharemgr show -pv
    default nfs=()
    zfs nfs=()
    zfs/data/nfs_share nfs=() nfs:sys=(rw="*" root="192.168.1.108")
    /data/nfs_share


and the host already auto-mounted the NFS share:

    ~ # esxcfg-nas -l
    nfs is /data/nfs_share from 192.168.1.107 mounted


