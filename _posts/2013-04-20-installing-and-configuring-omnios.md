---
title: Installing and Configuring OmniOS
author: Jarret Lavallee
layout: post
permalink: /2013/04/installing-and-configuring-omnios/
dsq_thread_id:
  - 1405287419
categories:
  - Home Lab
  - OS
tags:
  - OmniOS
  - sharectl
  - ZFS
---
Installing OmniOS is pretty straight forward. The installation documentation from OmniOs can be <a href="http://omnios.omniti.com/wiki.php/Installation" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://omnios.omniti.com/wiki.php/Installation']);">found here</a>. From that document:

> Boot the disk and follow the directions. Aside from selecting a disk on which to install and a timezone, there are no options. All configuration of the system happens on first boot by you: the administrator. You use the same tools to initially configure the machine as you would for ongoing maintenance.

After the installation is finished, log into the server. There is no default root password, so we should set one for security reasons:

    root@omnios-bloody:~# passwd root
    New Password:
    Re-enter new Password:
    passwd: password successfully changed for root
    

### Adding a Mirror disk to the rpool

It is a great idea to have some redundancy in the *rpool*. With my recent stretch of lost hard drives, I am going to add a mirrored disk to the *rpool*. First let&#8217;s list the *zpool* and see what disk is attached:

    root@megatron:~# zpool status rpool
      pool: rpool
     state: ONLINE
      scan: none requested
    
    config:
    
            NAME        STATE     READ WRITE CKSUM
            rpool       ONLINE       0     0     0
              c3d0s0    ONLINE       0     0     0
    
    errors: No known data errors
    

Let&#8217;s list the other disks in the system:

    root@megatron:~# echo |format
    Searching for disks...done
    
    
    AVAILABLE DISK SELECTIONS:
           0. c2d1 wdc WD32-  WD-WX30AB9C376-0001-298.09GB
              /pci@0,0/pci-ide@1f,2/ide@0/cmdk@1,0
           1. c3d0 unknown -Unknown-0001 cyl 30398 alt 2 hd 255 sec 63
              /pci@0,0/pci-ide@1f,5/ide@0/cmdk@0,0
    Specify disk (enter its number): Specify disk (enter its number): 
    

So we have *c2d1* that is available for a mirror. Let&#8217;s create a Solaris partition on it, instructions on using **fdisk** can be found in <a href="http://virtuallyhyper.com/2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive/']);">Karim&#8217;s article</a>.

    root@megatron:~# fdisk c2d1
    

Let&#8217;s copy over the slice information from our original drive:

    root@megatron:~# prtvtoc /dev/dsk/c3d0s0 |fmthard -s - /dev/rdsk/c2d1s0
    

Let&#8217;s install grub on the drive:

    root@megatron:~# installgrub /boot/grub/stage1 /boot/grub/stage2 /dev/rdsk/c2d1s0
    

Now we can add it to the zpool:

    root@megatron:~# zpool attach -f rpool c3d0s0 c2d1s0 
    

Make sure to wait until *resilver* is done before rebooting. To check on the *resilver* progress, we can run the following:

    root@megatron:~# zpool status rpool
      pool: rpool
     state: ONLINE
    status: One or more devices is currently being resilvered.  The pool will
            continue to function, possibly in a degraded state.
    action: Wait for the resilver to complete.
      scan: resilver in progress since Sun Mar 17 21:47:50 2013
        186M scanned out of 19.3G at 2.24M/s, 2h25m to go
        185M resilvered, 0.94% done
    

### Configuring the Networking

Since this is a NAS, we want to give it a static network address. First let&#8217;s disable *nwam*:

    root@omnios-bloody:~# svcadm disable nwam
    root@omnios-bloody:~# svcs nwam
    STATE          STIME    FMRI
    disabled       14:42:58 svc:/network/physical:nwam
    

Now let&#8217;s make sure *network/physical:default* is enabled:

    root@omnios-bloody:~# svcadm enable network/physical:default
    root@omnios-bloody:~# svcs network/physical:default
    STATE          STIME    FMRI
    online         14:43:05 svc:/network/physical:default
    

So now we can create the interfaces. I have intel NICs using the *e1000* driver, so the NICs show up as *e1000g0*, *e1000g1*, etc. Different drivers will produce different NIC names. First we need to list the interfaces we will use:

    root@omnios-bloody:~# dladm show-link
    LINK        CLASS     MTU    STATE    BRIDGE     OVER
    e1000g0     phys      1500   up       --         --
    e1000g1     phys      1500   up       --         --
    e1000g2     phys      1500   up       --         --
    

For each of the NICs we want to set up, we will need to create them:

    root@omnios-bloody:~# ipadm create-if e1000g0
    root@omnios-bloody:~# ipadm create-if e1000g1
    root@omnios-bloody:~# ipadm create-if e1000g2
    

Now we can configure the static IP addresses:

    root@omnios-bloody:~# ipadm create-addr -T static -a 192.168.5.82/24 e1000g0/v4
    root@omnios-bloody:~# ipadm create-addr -T static -a 10.0.1.82/24 e1000g1/v4
    root@omnios-bloody:~# ipadm create-addr -T static -a 10.0.0.82/24 e1000g2/v4
    

List the addresses to confirm that the changes were taken:

    root@omnios-bloody:~# ipadm show-addr
    ADDROBJ           TYPE     STATE        ADDR
    lo0/v4            static   ok           127.0.0.1/8
    e1000g0/v4        static   ok           192.168.5.82/24
    e1000g1/v4        static   ok           10.0.1.82/24
    e1000g2/v4        static   ok           10.0.0.82/24
    lo0/v6            static   ok           ::1/128
    

Now we need to add the default gateway. In my case I want the traffic to route out of the 192.168.5.1 gateway:

    root@omnios-bloody:~# route -p add default 192.168.5.1
    add net default: gateway 192.168.5.1
    add persistent net default: gateway 192.168.5.1
    

Let&#8217;s check the routing table to make sure that our default gateway is set:

    root@omnios-bloody:~# netstat -rn
    
    Routing Table: IPv4
      Destination           Gateway           Flags  Ref     Use     Interface
    -------------------- -------------------- ----- ----- ---------- ---------
    default              192.168.5.1          UG        1          0
    10.0.0.0             10.0.0.82            U         2          0 e1000g2
    10.0.1.0             10.0.1.82            U         4        535 e1000g1
    127.0.0.1            127.0.0.1            UH        2         24 lo0
    192.168.5.0          192.168.5.82         U         2          0 e1000g0
    

Just to confirm, let&#8217;s ping the gateway:

    root@omnios-bloody:~# ping 192.168.5.1
    192.168.5.1 is alive
    

Next we have to add the DNS servers to the */etc/resolv.conf* file:

    root@omnios-bloody:~# echo 'domain moopless.com' > /etc/resolv.conf
    root@omnios-bloody:~# echo 'nameserver 192.168.5.10' >> /etc/resolv.conf
    root@omnios-bloody:~# echo 'nameserver 8.8.8.8' >> /etc/resolv.conf
    

Now we need to tell the host to use DNS for host resolution:

    root@omnios-bloody:~# cp /etc/nsswitch.dns /etc/nsswitch.conf
    

Let&#8217;s test DNS resolution and network connectivity with a simple ping:

    root@omnios-bloody:~# ping google.com
    google.com is alive
    

You may have noticed that my hostname is *omnios-bloody*. I accepted the defaults during the installation. I will use the command below to change it:

    root@omnios-bloody:~# echo "megatron" > /etc/nodename
    

Now we can reboot the server to make sure that everything comes up on boot:

    root@omnios-bloody:~# reboot
    

After the reboot, log in and check the networking and hostname:

    root@megatron:~# ping virtuallyhyper.com
    virtuallyhyper.com is alive
    

Great, so the networking is working. Let&#8217;s make sure *ssh* is enabled:

    root@megatron:~# svcadm enable ssh  
    root@megatron:~$ svcs ssh
    STATE          STIME    FMRI
    online         15:45:39 svc:/network/ssh:default
    

### Add a local user

We have been logging in as root, so let&#8217;s add a local user. Since I am going to be mounting my existing zpools, I do not want to go back to all of my client machines and change the user IDs. To avoid any ID mismatch I am going to create my user with the same ID as it previously was:

    root@megatron:~# useradd -u 1000 -g 10 -m -d /export/home/jarret -s /bin/bash jarret
    64 blocks
    

If you just want the default UIDs, you can run the command below. The *-m* and *-d* options create the home directory.

    root@megatron:~# useradd -m -d /export/home/username username
    

Let&#8217;s set a password for the new user:

    root@megatron:~# passwd jarret
    New Password:
    Re-enter new Password:
    passwd: password successfully changed for jarret
    

Now I want to add this user to the *sudoers* file. Type **visudo** to safely edit the */etc/sudoers* file. Find the line below and remove the *&#8216;#&#8217;* mark to enable it:

    ## Uncomment to allow members of group sudo to execute any command
    %sudo ALL=(ALL) ALL
    

This will allow any user in the *sudo* group to run **sudo**. Let&#8217;s add the *sudo* group:

    root@megatron:~# groupadd sudo
    

Now we can add our newly created user to the *sudo* group:

    root@megatron:~# usermod -G sudo jarret
    

Now let&#8217;s verify that the user is in the *sudo* group:

    root@megatron:~# id jarret
    uid=1000(jarret) gid=10(staff) groups=10(staff),100(sudo)
    

Ok, so that looks good. Let&#8217;s switch to the *jarret* user and run **sudo**:

    root@megatron:~# su - jarret
    OmniOS 5.11     omnios-dda4bb3  2012.06.14
    jarret@megatron:~$ sudo -l
    Password:
    User jarret may run the following commands on this host:
        (ALL) ALL
    

Now we have a user with a home directory that is able to run elevated commands with **sudo**.

### Configure Extra Repositories

By default OmniOS comes with a package repository, but there are few other repotories out there. A list can be <a href="http://omnios.omniti.com/wiki.php/Packaging" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://omnios.omniti.com/wiki.php/Packaging']);">found here</a>. Out of the ones on there, I will be adding these repositories for their specific packages:

*   http: //pkg.cs.umd.edu for *fail2ban* 
*   http: //scott.mathematik.uni-ulm.de for *smartmontools*

Let&#8217;s list the existing repository:

    root@megatron:~# pkg publisher
    PUBLISHER                             TYPE     STATUS   URI
    omnios                                origin   online   http://pkg.omniti.com/omnios/bloody/
    

Let&#8217;s add the new repositories:

    root@megatron:~# pkg set-publisher -g http://pkg.cs.umd.edu/ cs.umd.edu
    root@megatron:~# pkg set-publisher -g http://scott.mathematik.uni-ulm.de/release/ uulm.mawi
    

Let&#8217;s list the repositories again to confirm the new ones are there:

    root@megatron:~# pkg publisher
    PUBLISHER                             TYPE     STATUS   URI
    omnios                                origin   online   http://pkg.omniti.com/omnios/bloody/
    cs.umd.edu                            origin   online   http://pkg.cs.umd.edu/
    uulm.mawi                             origin   online   http://scott.mathematik.uni-ulm.de/release/
    

The installation ISO is generally behind in packages, depending on when it was released, so let&#8217;s do an update. First we should list the updates that are available:

    root@megatron:~# pkg update -nv
                Packages to remove:       3
               Packages to install:       4
                Packages to update:     387
         Estimated space available: 5.44 GB
    Estimated space to be consumed: 1.08 GB
           Create boot environment:     Yes
         Activate boot environment:     Yes
    Create backup boot environment:      No
              Rebuild boot archive:     Yes
    

The *Create boot environment* means that it will require a reboot to activate the changes. A new *BE* will be created. Karim went into depth about **beadm** in <a href="http://virtuallyhyper.com/2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive/']);">this post.</a> Let&#8217;s run the upgrade:

    root@megatron:~# pkg update -v
    ...
    A clone of omnios exists and has been updated and activated.
    On the next boot the Boot Environment omnios-1 will be
    mounted on '/'.  Reboot when ready to switch to this updated BE.
    

Let&#8217;s go ahead and reboot.

    root@megatron:~# reboot
    

Let&#8217;s log in and check the current *BE*.

    jarret@megatron:~$ beadm list
    BE               Active Mountpoint Space Policy Created
    omnios-1         NR     /          4.69G static 2013-03-14 12:45
    omnios           -      -          33.6M static 2012-08-31 16:54
    

We are running on the omnios-1 as we expected.

### Installing Napp-it

<a href="http://napp-it.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://napp-it.org']);">Napp-it</a> is a web management front end for Solaris. It is not a necessity, but I really like using it to create *Comstar views* rather than running it manually. There are a bunch of features that can be installed with it and it is actively developed and maintained. Let&#8217;s install *napp-it*:

    root@megatron:~# wget -O - www.napp-it.org/nappit | perl
    ...
     ##############################################################################
     -> REBOOT NOW or activate current BE followed by /etc/init.d/napp-it restart!!
     ##############################################################################
        If you like napp-it, please support us and donate at napp-it.org
    

The installer goes through and does many things. The list is below, if you are curious:

1.  Makes a new BE
2.  Adds a user named *napp-it*
3.  Makes some changes to *PAM*
4.  Grabs and unzips the *napp-it* web package
5.  Installs iscsi/target, iperf, bonie++, and parted (if available in the repositories)
6.  Adds some symbolic links for the GNU Compilers (ggc, g++, etc)
7.  Installs gcc
8.  Adds the cs.umd.edu repository
9.  Configures *napp-it* to start on boot

Now we should reboot into the new *BE*:

    root@megatron:~# reboot
    

Let&#8217;s check the active *BE* to see if the *napp-it* one is now activated:

    root@megatron:~# beadm list
    BE                                         Active Mountpoint Space Policy Created
    napp-it-0.9a8                              R      -          4.95G static 2013-03-14 13:26
    omnios-1                                   N      /          0     static 2013-03-14 12:45
    omnios                                     -      -          33.6M static 2012-08-31 16:54
    pre_napp-it-0.9a8                          -      -          1.00K static 2013-03-14 13:16
    

We should now have *napp-it* running. It can be accessed at \****. I will touch back later on the configuration using *napp-it*.

### Configuring NFS

One of my favorite features of ZFS is that it stores the NFS settings. The settings will come over with the *zpools*. We just need to enable NFS and tweak any settings that we want before we mount any existing *zpools*. First let&#8217;s see if NFS is running:

    root@megatron:~# svcs *nfs*
    STATE          STIME    FMRI
    disabled       13:01:08 svc:/network/nfs/client:default
    disabled       13:01:08 svc:/network/nfs/nlockmgr:default
    disabled       13:01:08 svc:/network/nfs/cbd:default
    disabled       13:01:08 svc:/network/nfs/mapid:default
    disabled       13:01:08 svc:/network/nfs/status:default
    disabled       13:01:08 svc:/network/nfs/server:default
    disabled       13:01:09 svc:/network/nfs/log:default
    disabled       13:01:27 svc:/network/nfs/rquota:default
    

The NFS services are currently disabled. Let&#8217;s check the settings before we enable the service:

    root@megatron:~# sharectl get nfs
    servers=16
    lockd_listen_backlog=32
    lockd_servers=20
    lockd_retransmit_timeout=5
    grace_period=90
    server_versmin=2
    server_versmax=4
    client_versmin=2
    client_versmax=4
    server_delegation=on
    nfsmapid_domain=
    max_connections=-1
    protocol=ALL
    listen_backlog=32
    device=
    

These settings are the defaults, but they do not lead to good performance. Hardware has improved drastically since those default were defined. This machine is a Intel L5520 with 32GB of RAM, so it should be able to handle more load. I usually tune NFS as outlined in this <a href="http://utcc.utoronto.ca/~cks/space/blog/solaris/SolarisNFSServerTuning" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://utcc.utoronto.ca/~cks/space/blog/solaris/SolarisNFSServerTuning']);">blog article</a>. I have standardized on NFS 3, so I setup the server and clients to use NFS version 3.

In previous versions of Solaris, the NFS properties were stored in the */etc/default/nfs* file. Now we can edit the properties using **sharectl** utility:

    root@megatron:~# sharectl set -p servers=512 nfs
    root@megatron:~# sharectl set -p lockd_servers=128 nfs
    root@megatron:~# sharectl set -p lockd_listen_backlog=256 nfs
    root@megatron:~# sharectl set -p server_versmax=3 nfs
    root@megatron:~# sharectl set -p client_versmax=3 nfs
    

Let&#8217;s check to see if the settings are applied:

    root@megatron:~# sharectl get nfs
    servers=512
    lockd_listen_backlog=256
    lockd_servers=128
    lockd_retransmit_timeout=5
    grace_period=90
    server_versmin=2
    server_versmax=3
    client_versmin=2
    client_versmax=3
    server_delegation=on
    nfsmapid_domain=
    max_connections=-1
    protocol=ALL
    listen_backlog=32
    device=
    

Let&#8217;s start up the services that we need:

     root@megatron:~# svcadm enable -r nfs/server
    

## Import zpools

I tried to import my *zpools* but ran into an issue. When I ran **zpool import** I expected to see a list of the zpools that I could import. Instead the zpool command asserted and failed out. Below is what I saw:

    root@megatron:~# zpool import        
    Assertion failed: rn->rn\_nozpool == B\_FALSE, file ../common/libzfs\_import.c, line 1080, function zpool\_open_func Abort (core dumped)
    

I did a little research and ended up finding <a href="https://www.illumos.org/issues/1778" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.illumos.org/issues/1778']);">this bug</a> which listed a workaround. The work-around mentioned in the bug was to move the */dev/dsk* and */dev/rdsk* folders out of the way and then re-scan for new disks. I gave it a try:

    root@megatron:/dev# mv rdsk rdsk-old 
    root@megatron:/dev# mv dsk dsk-old 
    root@megatron:/dev# mkdir dsk 
    root@megatron:/dev# mkdir rdisk 
    root@megatron:/dev# devfsadm -c disk
    

I ran a *zpool import* and it ran fine, so I then imported the *zpools*:

    root@megatron:/dev# zpool import -f data 
    root@megatron:/dev# zpool import -f vms
    

