---
title: Backing Up with Rsync to Pogoplug
author: Karim Elatov
layout: post
permalink: /2013/09/backing-rsync-to-pogoplug/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1766382400
categories:
  - OS
tags:
  - optware
  - pogoplug
  - rsync
---
## PogoPlug Series 4

Someone had given me a PogoPlug Series 4 ([PogoPlug_Series4](https://github.com/elatov/uploads/raw/master/2013/09/PogoPlug_Series4.pdf)) and I wanted to utilize it to it's full potential. PogoPlug is a small computer (running an embedded ARM compatible processor) that you can connect USB or SATA Devices to and you will be able to share the contents of those hard drive via the remote **pogoplug.com** site. Some people refer to this as the private cloud. Here is a snippet from their site that might explain it better:

> **How is Pogoplug different from other cloud storage services?**
> Pogoplug provides a Personal Cloud you can touch. When you buy a Pogoplug device, your files stay safe at home or the office while you access them from any browser, smartphone or tablet. Your private cloud has unlimited storage, with the option to grow as you go by adding more or larger hard drives. Pogoplug's secure and private cloud storage solutions include Pogoplug devices, Pogoplug Family, Pogoplug Team and Pogoplug PC.

### Enable SSH on the PogoPlug Device

Go to **pogoplug.com** and login with with the credential that you created during your registration process. After you are logged in you will see the following:

![pogoplug loggedin Backing Up with Rsync to Pogoplug](https://github.com/elatov/uploads/raw/master/2013/09/pogoplug_loggedin.png)

Notice there are two section: the Seagate drive (which is the 60GB 2.5 SATA Drive that I plugged into the pogoplug) and then there is "*Pogoplug Cloud*" section. By default you get 5GB of cloud storage (you can pay to get unlimited storage space, but I was planning on utilizing the 60GB drive for all of my setup).

From the top right corner click on **Settings** and then click on **Security**. Then go ahead and "**Enable SSH access for this Pogoplug Device**":

![pogoplug com security Backing Up with Rsync to Pogoplug](https://github.com/elatov/uploads/raw/master/2013/09/pogoplug_com_security.png)

After you enable SSH, it will ask you to set your password.

### Pogoplug Under the Covers

If you want to go all out, you can actually install ArchLinux on the device. [Here](http://archlinuxarm.org/platforms/armv5/pogoplug-series-4) is the link for that. From that site, here is a little more information regarding the device:

> The Pogoplug Series 4 is the latest generation of hardware from Pogoplug, representing a return to the Marvell Kirkwood platform. This device is based on the 88F6192 SoC, which is a slightly under-powered relative to the 88F6281 found in the other supported ARMv5 devices.
>
> Under the removable top cover, there is a SATA port (3 Gbps) and a USB 2.0 port, as well as an SDHC slot along the side of the device. On the back of the unit, there is a single gigabit ethernet port as well as an event driven eject button (/dev/input/event0). New to plug hardware are two USB 3.0 ports on the back provided by a controller connected to the internal PCIe bus.

#### PCI Controller

Here is the PCI information from the pogoplug device (I ran this command after I SSH'ed into the device):

    pogo:~# lspci -mk
    00:01.0 "Class 0c03" "1b73" "1009" "1b73" "0000" "xhci_hcd"


Looking up the device on the PCI database, I saw the following:

![pci database Backing Up with Rsync to Pogoplug](https://github.com/elatov/uploads/raw/master/2013/09/pci_database.png)

Then clicking on that device:

![vendor ID pcie Backing Up with Rsync to Pogoplug](https://github.com/elatov/uploads/raw/master/2013/09/vendor_ID_pcie.png)

So as advertised, there is an internal PCIe controller for the USB 3.0 ports.

#### USB Ports

Here is the information from **dmesg** regarding the USB 3.0 ports:

    pogo:~# dmesg | grep 'xHCI Host Controller' -A 8
    <6>[    2.080000] xhci_hcd 0000:00:01.0: xHCI Host Controller
    <6>[    2.080000] xhci_hcd 0000:00:01.0: new USB bus registered, assigned bus number 2
    <6>[    2.090000] xhci_hcd 0000:00:01.0: irq 9, io mem 0xe0000000
    <4>[    2.100000] usb usb2: config 1 interface 0 altsetting 0 endpoint 0x81 has no SuperSpeed companion descriptor
    <6>[    2.110000] usb usb2: configuration #1 chosen from 1 choice
    <7>[    2.110000] xHCI xhci_add_endpoint called for root hub
    <7>[    2.110000] xHCI xhci_check_bandwidth called for root hub
    <6>[    2.110000] hub 2-0:1.0: USB hub found
    <6>[    2.120000] hub 2-0:1.0: 4 ports detected


Checking out **dmesg**, I saw the following for the USB 2.0 hub:

    pogo:~# dmesg | grep "USB 2.0 'Enhanced' Host Controller" -A 8
    <6>[    1.990000] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
    <6>[    2.000000] ehci_marvell ehci_marvell.70059: Marvell Orion EHCI
    <6>[    2.000000] ehci_marvell ehci_marvell.70059: new USB bus registered, assigned bus number 1
    <5>[    2.010000] UBI: background thread "ubi_bgt0d" started, PID 462
    <6>[    2.040000] ehci_marvell ehci_marvell.70059: irq 19, io base 0xf1050100
    <6>[    2.060000] ehci_marvell ehci_marvell.70059: USB 2.0 started, EHCI 1.00
    <6>[    2.060000] usb usb1: configuration #1 chosen from 1 choice
    <6>[    2.070000] hub 1-0:1.0: USB hub found
    <6>[    2.070000] hub 1-0:1.0: 1 port detected


So USB 2.0 is on the first bus and USB 3.0 is on the second bus. Here are both buses:

    pogo:~# lsusb
    Bus 001 Device 001: ID 1d6b:0002
    Bus 002 Device 001: ID 1d6b:0002


If you plug in a USB device into the 2.0 USB port, you will see the following:

    pogo:~# lsusb
    Bus 001 Device 001: ID 1d6b:0002
    Bus 002 Device 001: ID 1d6b:0002
    Bus 001 Device 002: ID 0781:5574


Notice the **Bus** is same for the bottom one but it's a different **Device** (You can check the USB device IDs [here](http://www.linux-usb.org/usb.ids)). You will also see the following ins **dmesg**:

    <6>[48003.710000] usb 1-1: new high speed USB device using ehci_marvell and address 2
    <6>[48003.870000] usb 1-1: configuration #1 chosen from 1 choice
    <6>[48003.880000] scsi2 : SCSI emulation for USB Mass Storage devices
    <7>[48003.890000] usb-storage: device found at 2
    <7>[48003.890000] usb-storage: waiting for device to settle before scanning
    <5>[48008.890000] scsi 2:0:0:0: Direct-Access     SanDisk                   1.26 PQ: 0 ANSI: 5


#### CPU Information

Here is the information for the device:

    pogo:~# cat /proc/cpuinfo
    Processor   : Feroceon 88FR131 rev 1 (v5l)
    BogoMIPS    : 799.53
    Features    : swp half thumb fastmult edsp
    CPU implementer : 0x56
    CPU architecture: 5TE
    CPU variant : 0x2
    CPU part    : 0x131
    CPU revision    : 1

    Hardware    : Feroceon-KW
    Revision    : 0000
    Serial      : 0000000000000000


Here is some information from uname:

    pogo:~# uname -a
    Linux pogo.dnsd.me 2.6.31.8 #5 Wed Sep 28 12:09:12 PDT 2011 armv5tel GNU/Linux


So it's 800Mhz armv5 based processor. There was an interesting discussion about the Pogoplug performance in [this](http://archlinuxarm.org/forum/viewtopic.php?f=29&t=2110) Arch Linux Forum. The box has 128M of RAM as well.

#### Disk Information

After I plugged in both of my disks ( the SATA and the USB devices), both were mounted automatically:

    pogo:~# df -h /tmp/.cemnt/sd*1
    Filesystem                Size      Used Available Use% Mounted on
    /tmp/.cemnt/sda1         55.0G     16.1G     36.1G  31% /tmp/.cemnt/mnt_sda1
    /tmp/.cemnt/sdb1          7.5G     89.6M      7.4G   1% /tmp/.cemnt/mnt_sdb1


You can get disk information by checking out /proc/scsi/scsi

    pogo:~# cat /proc/scsi/scsi
    Attached devices:
    Host: scsi0 Channel: 00 Id: 00 Lun: 00
      Vendor: Seagate  Model: ST96812AS        Rev: 3.14
      Type:   Direct-Access                    ANSI  SCSI revision: 05
    Host: scsi2 Channel: 00 Id: 00 Lun: 00
      Vendor: SanDisk  Model:                  Rev: 1.26
      Type:   Direct-Access                    ANSI  SCSI revision: 02


You can of course check out partition information with **fdisk**:

    pogo:~# fdisk -l

    Disk /dev/sda: 60.0 GB, 60011642880 bytes
    64 heads, 32 sectors/track, 57231 cylinders
    Units = cylinders of 2048 * 512 = 1048576 bytes

       Device Boot      Start         End      Blocks  Id System
    /dev/sda1               1       57231    58604528  83 Linux

    Disk /dev/sdb: 8004 MB, 8004304896 bytes
    1 heads, 21 sectors/track, 744448 cylinders
    Units = cylinders of 21 * 512 = 10752 bytes

       Device Boot      Start         End      Blocks  Id System
    /dev/sdb1              98      744448     7815680   7 HPFS/NTFS


Doing a quick comparison of the write speeds; I opened two ssh connections to the pogoplug box. On the first one, I ran the following:

    pogo:~# iostat 1 -xm


On the second one, I ran the following:

    pogo:~# cd /tmp/.cemnt/mnt_sda1/test/
    pogo:/tmp/.cemnt/mnt_sda1/test# time dd if=/dev/zero of=test.dd bs=1M count=1024


Going back to the **iostat** window, I saw the following:

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00  9933.66    0.00  182.18     0.00    34.49   387.70    22.70  114.51   5.05  92.08
    sdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00   73.27   26.73    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00  8972.28    0.00  149.50     0.00    34.52   472.85    39.60  261.66   6.69 100.00
    sdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.99    0.00   68.32   30.69    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00  6957.43    0.00  167.33     0.00    34.66   424.19    34.41  194.79   5.98 100.00
    sdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00


So it was going about 34MB/s. Going back to the **dd** command, here were the results:

    # time dd if=/dev/zero of=test.dd bs=1M count=1024
    1024+0 records in
    1024+0 records out
    real    0m 30.64s
    user    0m 0.02s
    sys 0m 18.87s


So it 30 seconds to write 1G, which matched the speed from **iostat**. Doing the same thing on the USB device, I saw the following:

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
    sdb               0.00     0.00    0.00   40.59     0.00     4.66   234.93    63.38 1509.76  24.63 100.00

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    5.94   94.06    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
    sdb               0.00     0.00    0.00   43.56     0.00     5.00   235.27    62.28 1538.86  22.95 100.00

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    7.92   92.08    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
    sda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
    sdb               0.00     0.00    0.00   43.56     0.00     5.00   235.27    65.43 1576.36  22.95 100.00


and the **dd** results:

    # time dd if=/dev/zero of=test.dd bs=1M count=1024
    1024+0 records in
    1024+0 records out
    real    3m 37.98s
    user    0m 0.01s
    sys 0m 12.52s


so my SanDisk was slower than my 2.5 SATA disk (5MB/s vs 35MB/s) :) The speeds weren't crazy fast, but I wasn't worried about that.

#### Pogoplug Networking

From the **dmesg** output, I saw the following:

    pogo:~# dmesg | grep 'Marvell Ethernet' -A 20
    <4>[    1.410000] Loading Marvell Ethernet Driver:
    <4>[    1.410000]   o Cached descriptors in DRAM
    <4>[    1.420000]   o DRAM SW cache-coherency
    <4>[    1.420000]   o 1 Giga ports supported
    <4>[    1.420000]   o Single RX Queue support - ETH_DEF_RXQ=0
    <4>[    1.430000]   o Single TX Queue support - ETH_DEF_TXQ=0
    <4>[    1.430000]   o TCP segmentation offload (TSO) supported
    <4>[    1.440000]   o Large Receive offload (LRO) supported
    <4>[    1.440000]   o Receive checksum offload supported
    <4>[    1.450000]   o Transmit checksum offload supported
    <4>[    1.450000]   o Network Fast Processing (Routing) supported - (Disabled)
    <4>[    1.460000]   o Driver ERROR statistics enabled
    <4>[    1.470000]   o Proc tool API enabled
    <4>[    1.470000]   o SKB Reuse supported - (Disabled)
    <4>[    1.470000]   o SKB Recycle supported - (Disabled)
    <4>[    1.480000]   o Rx descripors: q0=128
    <4>[    1.480000]   o Tx descripors: q0=532
    <4>[    1.490000]   o Loading network interface(s):
    <4>[    1.490000]      o register under mv88fx_eth platform
    <4>[    1.500000]      o eth0, ifindex = 2, GbE port = 0


It looks like it capable of doing 1GB, although it's plugged into a 100Mbps port:

    pogo:~# dmesg | grep eth0
    <4>[    1.500000]      o eth0, ifindex = 2, GbE port = 0
    <5>[    4.820000] eth0: link down
    <5>[    4.830000] eth0: started
    <5>[    5.940000] eth0: link up, full duplex, speed 100 Mbps


Doing an **iperf** test between two machines, I was able to use the full bandwidth:

    pogo:~# iperf -s -w 1M
    ------------------------------------------------------------
    Server listening on TCP port 5001
    TCP window size:   216 KByte (WARNING: requested 1.00 MByte)
    ------------------------------------------------------------
    [  4] local 192.168.1.104 port 5001 connected with 192.168.1.100 port 43353
    [ ID] Interval       Transfer     Bandwidth
    [  4]  0.0-10.0 sec    113 MBytes  94.1 Mbits/sec


here is the command I ran on the client side:

    deb:~$iperf -c 192.168.1.104 -w 1M
    ------------------------------------------------------------
    Client connecting to 192.168.1.104, TCP port 5001
    TCP window size:  256 KByte (WARNING: requested 1.00 MByte)
    ------------------------------------------------------------
    [  3] local 192.168.1.100 port 43353 connected with 192.168.1.104 port 5001
    [ ID] Interval       Transfer     Bandwidth
    [  3]  0.0-10.0 sec   113 MBytes  94.3 Mbits/sec


Going the other way around looked the same, here is from the server side:

    deb:~$iperf -s -w 1M
    ------------------------------------------------------------
    Server listening on TCP port 5001
    TCP window size:  256 KByte (WARNING: requested 1.00 MByte)
    ------------------------------------------------------------
    [  4] local 192.168.1.100 port 5001 connected with 192.168.1.104 port 55924
    [ ID] Interval       Transfer     Bandwidth
    [  4]  0.0-10.0 sec   112 MBytes  93.4 Mbits/sec


and the client side:

    pogo:~# iperf -c 192.168.1.100 -w 1M
    ------------------------------------------------------------
    Client connecting to 192.168.1.100, TCP port 5001
    TCP window size:   216 KByte (WARNING: requested 1.00 MByte)
    ------------------------------------------------------------
    [  3] local 192.168.1.104 port 55924 connected with 192.168.1.100 port 5001
    [ ID] Interval       Transfer     Bandwidth
    [  3]  0.0-10.0 sec    112 MBytes  93.5 Mbits/sec


For the IPs:

    pogo:~# ip -4 a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue
        inet 127.0.0.1/8 scope host lo
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 532
        inet 169.254.77.39/16 brd 169.254.255.255 scope global eth0:0
        inet 192.168.1.104/24 brd 192.168.1.255 scope global eth0
    3: xce0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1350 qdisc pfifo_fast qlen 500
        inet 10.67.101.1/32 scope global xce0


It looks like our **eth0** has a regular internal network and you will also notice a **xce0** device, that is the VPN tunnel used to communicate back to **pogoplug.com** to display all the information regarding the device. In the beginning it uses DHCP to grab that IP address.

### Assign a Static IP to Pogoplug

Now that we checked out the device, let's configure it for our network. The first thing to do is assign a static IP address to the device. This is done with the **/etc/init.d/rcS** file. Initially the root filesystem is read-only, so first go ahead and remount it with read/write capabilities:

    pogo:~# killall hbwd
    pogo:~# mount / -o remount,rw


The **hdwd** process is the cloud engine daemon that does all the synchronization between your device and the *pogoplug* site. Since it's using the **rootfs**, we have to kill it first prior to re-mounting our *rootfs*. As a side note here are the daemons running:

    pogo:~# ps | grep hb
      653 root      1672 S    /usr/local/cloudengines/bin/hbwd /usr/local/cloudeng
      654 root     18588 S    /usr/local/cloudengines/bin/hbplug


If you want to be able to use the "cloud" aspect of pogoplug (check photos that are on the disks and share those photos), I would leave it running.

You can confirm that **rootfs** is mounted with read/write (rw) capabilities by running the **mount** command again:

    pogo:~# mount | grep ^root
    rootfs on / type rootfs (rw)


That looks good, now go add and edit the **/etc/init.d/rcS** file with **vi**:

    pogo:~# vi /etc/init.d/rcS


Inside the file modify the **hostname** command to set it to our desired hostname, here is what I did:

    hostname pogo.dnsd.me


Then at the end of the file add the following to set the static IP and DNS:

    ifconfig eth0 192.168.1.104 netmask 255.255.255.0
    route add default gw 192.168.1.1
    echo "nameserver 192.168.1.1" > /etc/resolv.conf


Now if you reboot the device, it will come up with the correct **hostname** and it will always come up with a static IP (the cloud engine daemons will start up as well).

### Install OptWare on Pogoplug

#### Remove *noexec* Flag from External Disk in Pogoplug

Since we have only 90M for our *rootfs* let's install **optware** and put it on our SATA disk. The first thing that you will notice, is that all the devices are mounted with the **noexec** flag:

    # mount | grep sd
    /tmp/.cemnt/sda1 on /tmp/.cemnt/mnt_sda1 type ext3 (rw,nosuid,nodev,noexec,noatime,errors=continue,data=writeback)
    /tmp/.cemnt/sdb1 on /tmp/.cemnt/mnt_sdb1 type ufsd (rw,nosuid,nodev,noexec,noatime,nls=utf8,uid=0,gid=0,fmask=22,dmask=22,nocase,sparse,force)


I wasn't planning on using the USB disk and I was going to keep everything on the SATA disk, so let's go ahead and make the mountpoint for the SATA disk allow executables. This is done by running the following command:

    pogo:~# mount /tmp/.cemnt/sda1 -o remount,exec


Confirm the **noexec** flag is gone:

    pogo:~# mount | grep sda
    /tmp/.cemnt/sda1 on /tmp/.cemnt/mnt_sda1 type ext3 (rw,nosuid,nodev,noatime,errors=continue,data=writeback)


That looks perfect. Now in order for us to use OptWare we need to get a newer version of **wget**.

#### Install Newer Version of *wget* for OptWare on Pogoplug

First let's re-mount our *rootfs* with read-write mode:

    pogo:~# killall hbwd
    pogo:~# mount / -o remount,rw


Now let's create an **opt** folder on the SATA disk and create a symbolic link to that folder:

    pogo:~# cd /
    pogo:/# mkdir /tmp/.cemnt/mnt_sda1/opt/
    pogo:/# ln -s /tmp/.cemnt/mnt_sda1/opt/


after it's done it should look like this:

    pogo:/# ls -l | grep opt
    lrwxrwxrwx    1 root     root            25 May 23 22:27 opt -> /tmp/.cemnt/mnt_sda1/opt/


Now let's grab the newer version of the **wget** utility:

    pogo:~# cd /opt
    pogo:/tmp/.cemnt/mnt_sda1/opt# mkdir tmp
    pogo:/tmp/.cemnt/mnt_sda1/opt# cd tmp
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# wget http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/wget_1.12-2_arm.ipk


Let's extract the utility and replace the system one:

    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# tar xf wget_1.12-2_arm.ipk
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# tar xf data.tar.gz
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# mv /usr/bin/wget /usr/bin/wget.orig
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# mv opt/bin/wget /usr/bin/wget


#### Install *ipkg* for OptWare

Let's remove the **wget** package files:

    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# rm -rf *


and let's download the **ipkg** utility:

    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# wget http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/ipkg-opt_0.99.163-10_arm.ipk


Let's extract it and put it under the **/opt** directory:

    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# tar xf ipkg-opt_0.99.163-10_arm.ipk
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# tar xf data.tar.gz
    pogo:/tmp/.cemnt/mnt_sda1/opt/tmp# mv opt/* /opt/.


Now let's configure the **ipkg** package utility to download from the appropriate mirror. Here is the command for that:

    pogo:~# echo "src cross http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable" >> /opt/etc/ipkg.conf


### Configure root user's Environment on Pogoplug

Since all the binaries for *OptWare* will be under **/opt/bin** and **/opt/sbin** let's add them to the PATH variable of the *root* user and while we are at let's change the prompt. This is done by editing **/root/.profile** file and adding/modifying the following:

    pogo:~# cat .profile
    #!/bin/sh
    PATH=/sbin:/usr/sbin:/bin:/usr/bin:/opt/bin:opt/sbin
    TERM=xterm
    PS1='\h:\w\$ '


### Install Packages with ipkg

Now that our path is all setup, let's update the package cache for ipkg:

    pogo:~# ipkg update
    Downloading http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/Packages
    Updated list of available packages in /opt/lib/ipkg/lists/cross
    Successfully terminated.


You can search for specific files like this:

    pogo:~# ipkg search "*/rsync"
    rsync - 3.0.9-1 - /opt/bin/rsync
    rsync - 3.0.9-1 - /opt/etc/default/rsync
    Successfully terminated.


or if you know the package name you can do this:

    pogo:~# ipkg list | grep openssh
    openssh - 5.9p1-1 - a FREE version of the SSH protocol suite of network connectivity tools.
    openssh-sftp-server - 5.9p1-1 - sftp-server only from a FREE version of the SSH protocol suite of network connectivity tools.
    pssh - 2.3-1 - pssh provides parallel versions of openssh tools.


so let's go ahead and install **rsync**:

    pogo:~# ipkg install rsync


after it's done you should be able to **rsync** a file to it. I went ahead and created a **backups** directory on the SATA drive and created a symbolic link to that:

    pogo:~# mkdir /tmp/.cemnt/mnt_sda1/backups
    pogo:~# ln -s /tmp/.cemnt/mnt_sda1/backups/ /backups


Here is the test **rsync**:

    elatov@deb:~$rsync -avzP test.file root@pogo:/backups/.
    sending incremental file list
    test.file
               8 100%    0.00kB/s    0:00:00 (xfer#1, to-check=0/1)

    sent 99 bytes  received 31 bytes  52.00 bytes/sec
    total size is 8  speedup is 0.06


To go the other way we can run the following (since pogoplug uses **dropbear** for it's SSH software, we include the **-e dbclient** parameter):

    pogo:~# rsync -avzP -e dbclient /backups/test.file elatov@192.168.1.100:
    Host '192.168.1.100' is not in the trusted hosts file.
    (fingerprint md5 30:ab:1c:b2:b7:a1:f2:a0:be:09:ef:7e:48:30:63:84)
    Do you want to continue connecting? (y/n) y
    elatov@192.168.1.100's password:
    sending incremental file list
    test.file
               8 100%    0.00kB/s    0:00:00 (xfer#1, to-check=0/1)

    sent 84 bytes  received 31 bytes  15.33 bytes/sec
    total size is 8  speedup is 0.07


I didn't really need to go from pogoplug to any server but it was a good test.

### Configure SSH Authorized_keys on Pogoplug

Since I wanted to automate the backup process, I was going to use SSH keys to login to the pogoplug device. Luckily **dropbear** was already configured to read the **.ssh/authorized_keys** file by default. So I just ran the following from my machines:

    fed:~>ssh-copy-id root@pogo
    /bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
    /bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
    root@pogo.dnsd.me's password:

    Number of key(s) added: 1

    Now try logging into the machine, with:   "ssh 'root@pogo'"
    and check to make sure that only the key(s) you wanted were added.


Then I was able to login without a password:

    fed:~>ssh root@pogo
    pogo:~#


This works if you have **ssh-agent** running and have already added your key to it (or if you generated password-less SSH keys). Also make sure your *rootfs* is read-write capable.

### Make *rsync* executable on Pogoplug after reboot

After you reboot, the files on the SATA disk will not be executable. So we have two options, either remount the filesystem with the **exec** flag right after reboot. This is done by appending the following into the **/etc/init.d/rcS** file:

    sleep 30
    /bin/mount /tmp/.cemnt/sda1 -o remount,exec


Or just copying the **rsync** binary into **/usr/bin** (*rootfs* is executable, just not writable after the reboot):

    pogo:~# cp /opt/bin/rsync /usr/bin/.


Either one will work.

## Configuring Rsync Backups

Since I only had 60GB on my SATA disk, I didn't just want to copy all of my files from my machines. I was backing up 3 machine: Fedora (media server), Ubuntu (laptop), and Debian (web and monitoring server). My plan was going to backup the following directories (from each server):

*   /etc (configs)
*   /home (my regular files)
*   /var (on servers mysql and apache files, on the laptop crontabs and the sorts)
*   /usr/local (my custom built software).

I realized I will end up using the **-exclude-files** flag from the **rsync** utility to have a config per directory and that file will contain which files I want to backup.

### Rsync Exclude files

In the beginning the exclude files might seem a little cryptic. But one you read over "[Beginner to Beginner: rsync exclude-from](http://www.hyperorg.com/blogger/2008/05/10/beginner-to-beginner-rsync-exclude-from/)", it will all make sense. My plan was to create a config file per host and per directory. So each file would be called **host**-*direc_tory*. If a directory had forward slashes (**/**), I would replace them with underscores (**_**).

This way I would setup the destination folder to be the same as second part of the configuration filename after the dash (**-**). For example here how my *ubu* (ubuntu laptop) configuration looked like for the **/var** directory:

    $cat ubu-var
    + spool/
    + spool/cron/***
    + backups/***
    + lib/
    + lib/bluetooth/***
    + lib/NetworkManager/***
    - *


Debian based distros have a **backups** directory (under /var) with **dpkg** information and user information (**passwd**,**group**, and their corresponding shadow files). So I decided to include that. I also grabbed the **crontabs**, other stuff which I found interesting, and ignored the rest. Here is how my *deb* (web server) configuration looked like for the **/usr/local** directory:

    $ cat deb-usr_local
    - backup
    - etc/
    - games/
    - include/
    - lib/
    - man
    - sbin/
    - share/
    - src/


The first one (**backup**) is the backup "package", which contains all the configuration files and the script which puts it all together. I was using **grive** (check out [this](/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/) post for more information) to synchronize that between all the hosts, so there is no need to back it up. The rest are folders created by the OS which I never use. So I drop everything that I don't need and if I install software under that directory later on, it will be included in the backup. Lastly here is how my *fed* (media server) configuration looked like for the **/home/elatov** folder:

    $ cat fed-home_elatov
    - .gstreamer-0.10/
    - .gtk-bookmarks
    - .gtkrc2.0.orig
    - .ICEauthority
    + .java/
    + .java/.userPrefs/
    + .java/.userPrefs/net/
    + .java/.userPrefs/net/sourceforge/
    + .java/.userPrefs/net/sourceforge/app/
    + .java/.userPrefs/net/sourceforge/app/ui/
    + .java/.userPrefs/net/sourceforge/app/ui/rename/
    + .java/.userPrefs/net/sourceforge/app/ui/rename/prefs.xml
    - .java/*
    - .java/.userPrefs/*
    - .java/.userPrefs/net/*
    - .java/.userPrefs/net/sourceforge/*
    - .java/.userPrefs/net/sourceforge/app/*
    - .java/.userPrefs/net/sourceforge/app/ui/*
    - .java/.userPrefs/net/sourceforge/app/ui/rename/*
    - .kde/
    - .lesshst
    - .local/


I excluded most of the dot files that I don't care about and I included files that I care about. The above example was probably the most complicated one that I had to do. After it was said and done, here are all my configuration files:

    elatov@deb:~$ls /usr/local/backup/etc/
    ubu-etc          deb-home_elatov    fed-home_elatov
    ubu-home_elatov  deb-usr_local      fed-usr_lib_systemd_system
    ubu-usr_local    deb-var            fed-usr_local
    ubu-var          fed-boot           fed-usr_share
    deb-etc          fed-etc            fed-var


Each file is unique to the directory it represents. And the whole package contained the following files:

    fed:~>tree /usr/local/backup
    /usr/local/backup
    ├── bin
    │   └── rsync_backup.bash
    └── etc
        ├── ubu-etc
        ├── ubu-home_elatov
        ├── ubu-usr_local
        ├── ubu-var
        ├── deb-etc
        ├── deb-home_elatov
        ├── deb-usr_local
        ├── deb-var
        ├── fed-boot
        ├── fed-etc
        ├── fed-home_elatov
        ├── fed-usr_lib_systemd_system
        ├── fed-usr_local
        ├── fed-usr_share
        └── fed-var

    2 directories, 16 files


As I mentioned before, I used **grive** to synchronize the above across all the machines. So every machine ended up with all of the above files.

### Bash Script to Put together Rsync Exclude files

I then put together a very simple bash script to execute an appropriate exclude file on each host for each directory. Here is the script:

    $ cat /usr/local/backup/bin/rsync_backup.bash
    #!/bin/bash
    command -v rsync &> /dev/null
    command_status=$?

    if [ $command_status -eq 1 ]; then
        echo "We need rsync"
        exit 1
    fi

    if [ $# -gt 0 ]; then
        if [ $1 == "-m" ]; then
            week=1
        fi
    else
        day=$(date +%d)
        week=$(($day / 14))
    fi

    HOSTNAME=$(hostname -s)
    for conf in $(ls /usr/local/backup/etc/)
    do
        arr=(${conf//-/ })
        host=${arr[0]}
        dir=${arr[1]}
        if [[ $dir =~ "_" ]]; then
            dirr=${dir//_/\/}
        else
            dirr=$dir
        fi
        if [ $HOSTNAME == $host ]; then
            echo "$host -- $dir"
            rsync -rpogtlziO /$dirr/. root@pogo:/backups/$HOSTNAME/week$week/$dir/. --exclude-from=/usr/local/backup/etc/$conf --delete-excluded --delete-after
        fi
    done


It's not too fancy but it got the job done. It basically reads in all the configs from **/usr/local/backup/etc/** and breaks each configuration down by the dash (**-**); it assigns the hostname to the first part of the filename (**host-**) and the directory to the second part of the filename (**-direc_tory**). It then checks the directory string and if it sees any underscores (**_**), it will replace them with slashes (**/**). Lastly it checks if the **hostname** of the machine matches the first part of the config filename (**$host**) and then it executes the appropriate configuration.

The last thing that it does is check the *week* variable. I wanted to run the backup every two weeks, so I decided to run my script on the 14th and 28th of every month (I will use **cron** for that). The script checks which day you are running it on and sets the week number accordingly.

### Rsync Parameters

Depending on which host you are on, the script will run the following command:

    rsync -rpogtlziO /usr/share/. root@pogo:/backups/fed/week1/usr_share/. --exclude-from=/usr/local/backup/etc/fed-usr_share --delete --delete-excluded --delete-after


So prior to running the backup, you should have the following structure in place on the destination side (the pogoplug device) for all the hosts:

    pogo:~# tree -L 2 /backups/deb/
    /backups/deb/
    |-- week1
    |   |-- etc
    |   |-- home_elatov
    |   |-- usr_local
    |   `-- var
    `-- week2
        |-- etc
        |-- home_elatov
        |-- usr_local
        `-- var

    10 directories, 0 files


Now to break down the parameters:

*   **-r** recurse into directories
*   **-p** preserve permissions
*   **-o** preserve owner
*   **-g** preserve group
*   **-t** preserve modification times
*   **-l** copy symlinks as symlinks (I wanted to make sure the configuration is the same)
*   **-z** compress file data during the transfer
*   **-i** output a change-summary for all updates (I didn't want to use **-v** since it always showed the "sending incremental file list" message even if it didn't transfer anything)
*   **-O** omit directories from -times (when a file within a directory changes the modification of the parent directory changes, this happens on the home directory all the time, but I didn't want that to show up in the summary of updates)
*   **-exclude-from** read exclude patterns from FILE (this was discussed above)
*   **-delete** delete extraneous files from destination dirs (I didn't want to just keep updating to the backup, I wanted to remove old files as well)
*   **-delete-excluded** also delete excluded files from destination dirs (this would grab newly excluded files if I change my exclude files)
*   **-delete-after** receiver deletes after transfer, not during (I got this error during my testing: `error allocating core memory buffers`, and found a workaround from [this](https://bugzilla.samba.org/show_bug.cgi?id=5811) link.

I could've probably used the **-a** (archive mode; equals -rlptgoD), but I didn't want to transfer sockets or special devices, so I just broke it down by parameters instead.

### Configure Cron Job to Run on Certain Days of the Month

I ran the following to edit root's cron table:

    sudo crontab -e


and I added the following to the file:

    0 5 14,28 * * /usr/local/bin/rsync_backup


That would run the backup on the 14th and 28th of every month at 5:00 AM in the morning. I didn't want all the machines to back up at the same time, so I changed the times around on each machine. By default cron will send output of the script in an email. Here are the contents of a sample email that I received:

    fed -- boot
    fed -- etc
    fed -- home_elatov
    .d....og... ./
    <f.st...... .history
    <f..t...... .couchpotato/cache/python/3fa503986018521065b0f4f963e56e4a
    <f.st...... .couchpotato/logs/CouchPotato.log
    <f.st...... .xbmc/addons/plugin.video.telepoisk.com/cookies.txt
    <f+++++++++ .xbmc/temp/10025-5c57e0b7.fi
    <f+++++++++ .xbmc/temp/10025-9509cf95.fi
    <f.st...... .xbmc/temp/xbmc.log
    <f..t...... .xbmc/userdata/guisettings.xml
    <f..t...... .xbmc/userdata/profiles.xml
    <f..t...... .xbmc/userdata/Database/MyVideos75.db
    fed -- usr_lib_systemd_system
    fed -- usr_local
    fed -- usr_share
    fed -- var
    <f..t...... lib/pgsql/data/pg_stat_tmp/pgstat.stat
    <f.st...... subsonic/subsonic.log
    <f.st...... subsonic/subsonic_sh.log


It told me exactly what I wanted to know. Which files have changed and in which directory. I also added a **-m** parameter to the script and that will run a **m**anual back to the **week1** folder from whatever host you are on.

## Size of Backup

After I ran the backups, I saw the following sizes for each of my machines:

    pogo:~# du -hac -d 0 /backups/fed /backups/deb /backups/ubu
    1.7G    /backups/fed
    4.3G    /backups/deb
    477.5M  /backups/ubu
    6.5G    total


This was just week1, so I need to double that to accommodate for both weeks and I had the space for that.

## Backing up an Android Phone

### *BotSync* for Android

There is an App called **BotSync** which can keep the source directory in sync with the destination over **sftp**. We were using **dropbear** and that doesn't include an *sftp* server.

### Install OpenSSH on Pogoplug

There were a couple of missing parts to the install but it worked eventually. First go ahead and install the **openssh** package:

    ipkg install openssh


after you run that, you might see the following errors:

    /opt/bin/ssh-keygen: error while loading shared libraries: libnsl.so.1: cannot open shared object file: No such file or directory
    Generating RSA Key...
    /opt/bin/ssh-keygen: error while loading shared libraries: libnsl.so.1: cannot open shared object file: No such file or directory
    Generating DSA Key...
    /opt/bin/ssh-keygen: error while loading shared libraries: libnsl.so.1: cannot open shared object file: No such file or directory


To fix the above errors, install the **libnsl** package:

    pogo:~# ipkg install libnsl
    Installing libnsl (2.5-4) to root...
    Downloading http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/libnsl_2.5-4_arm.ipk
    Configuring libnsl
    Configuring openssh
    update-alternatives: Linking //opt/bin/scp to /opt/bin/openssh-scp
    update-alternatives: Linking //opt/bin/ssh to /opt/bin/openssh-ssh

    Generating RSA Key...
    Generating public/private rsa1 key pair.
    Your identification has been saved in /opt/etc/openssh/ssh_host_key.
    Your public key has been saved in /opt/etc/openssh/ssh_host_key.pub.


It will generate most of the keys for you. Next let's change the default port that OpenSSH uses (since **dropbear** is already using 22). I went ahead and changed OpenSSH to start on *2222*. This is accomplished by editing the **/opt/etc/openssh/sshd_config** file and modifying the following line:

    Port 2222


Now if try to start the daemon, you will see the following:

    pogo:~# /opt/etc/init.d/S40sshd start
    Could not load host key: /opt/etc/openssh/ssh_host_ecdsa_key


the daemon actually starts, but it just throws that warning:

    pogo:~# netstat -antp | grep sshd
    tcp        0      0 0.0.0.0:2222            0.0.0.0:*               LISTEN      2247/sshd


To get rid of that warning run the following:

    pogo:~# ssh-keygen -t ecdsa -f /opt/etc/openssh/ssh_h ost_ecdsa_key -N ''


And that will generate the missing keys and it should start without showing that message. To install the **sftp-server** component of OpenSSH, run the following:

    pogo:~# ipkg install openssh-sftp-server


Some clients automatically assume that the **sftp-server** binary is under **/usr/libexec/sftp-server** and if it's not there they will fail out. So create a link to **/opt/libexec** under **/usr**, just in case:

    pogo:~# cd /usr/
    pogo:~# ln -s /opt/libexec/


### Test out *sftp* connection to Pogoplug

From a Linux client run the following to test the connection:

    fed:~>sftp -p2222 root@pogo:/backups
    Connected to pogo.
    Changing to: /backups
    sftp> ls
    ubu              deb               fed


That looks perfect. If you want OpenSSH start automatically, add the following to your **/etc/init.d/rcS** file:

    sleep 30
    /bin/mount /tmp/.cemnt/sda1 -o remount,exec
    /opt/etc/init.d/S40sshd


### Configure BotSync to Upload to PogoPlug

Download the app and configure it like so:

![botsync config Backing Up with Rsync to Pogoplug](https://github.com/elatov/uploads/raw/master/2013/09/botsync_config.png)

The reason why I chose **/sdcard/TitaniumBackup** is because I use *TitaniumBackup* to create a compressed backup of my desired Apps and configurations to that location. If you didn't use *TitaniumBackup* then you can back up the whole **/sdcard** directory. After you are done with the configuration of the App, you can click **start** and it will start the synchronization process.

After it's all done, here is all my backed up data:

    pogo:~# du -hac -d 0 /backups/android /backups/fed /backups/deb /backups/ubu
    81.4M   /backups/android
    1.7G    /backups/fed
    4.3G    /backups/deb
    477.5M  /backups/ubu
    6.6G    total


All the backups, under 7GB... not bad.

