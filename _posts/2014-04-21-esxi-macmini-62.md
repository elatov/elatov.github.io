---
title: ESXi on MacMini 6,2
author: Karim Elatov
layout: post
permalink: /2014/04/esxi-macmini-62/
categories: ['storage', 'home_lab', 'vmware', 'zfs']
tags: ['comstar', 'iscsi', 'hostd', 'interrupt_remapping','vmware_converter', 'mbr', 'veeam', 'nfc', 'opensolaris', 'macmini', 'ovftool', 'powercli']
---

I decided to install ESXi on MacMini 6,2 ([Late 201](http://support.apple.com/kb/SP659)2). I am definitely not the first one to try this. Check out some notes on other people trying this out:

*   [ESXi 5.x on new Apple Mac Mini 6,2 Late 2012](https://communities.vmware.com/thread/423099)
*   [Running ESXi 5.5/5.5u1 on Apple Mac Mini](http://www.virtuallyghetto.com/2013/09/running-esxi-55-on-apple-mac-mini.html)
*   [ESXi on an Apple Mac Mini Server Late 2012 6,2](http://www.patcup.com/esxi-on-an-apple-mac-mini-server-late-2012-62/)

### Create a Bootable USB Drive with ESXi 5.5

From the above links we can see that disabling Interrupt Remapping is necessary (`esxcli system settings kernel list -o iovDisableIR`) or else we will run into a Purple Screen during the install and during boot. Luckily there is already a prebuilt ISO which has the correct settings configured. The download is available from [here](http://www.virtuallyghetto.com/2013/09/running-esxi-55-on-apple-mac-mini.html). After you have downloaded the ISO, you should have the following file:

    elatov@fed:~$ls -lh downloads/ESXi-5.5u1-MacMini-6-2.iso
    -rw-rw-r-- 1 elatov elatov 329M Apr  3 19:10 downloads/ESXi-5.5u1-MacMini-6-2.iso


Instructions on how to make a bootable USB Disk from a VMware Installer ISO are laid out in: [Format a USB Flash Drive to Boot the ESXi Installation or Upgrade](http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.vsphere.install.doc_50/GUID-33C3E7D5-20D0-4F84-B2E3-5CD33D32EAA8.html). The instructions are as follows:

> 1.  Create a partition table on the USB flash device.
>
>         /sbin/fdisk /dev/sdb
>
>
>     1. Type **d** to delete partitions until they are all deleted.
>     2. Type **n** to create primary partition 1 that extends over the entire disk.
>     3. Type **t** to set the type to an appropriate setting for the FAT32 file system, such as **c**.
>     4. Type **a** to set the active flag on partition 1.
>     5. Type **p** to print the partition table. The result should be similar to the following text:
>
> 			Disk /dev/sdb: 2004 MB, 2004877312 bytes
> 			255 heads, 63 sectors/track, 243 cylinders
> 			Units = cylinders of 16065 * 512 = 8225280 bytes
> 			Device Boot      Start         End      Blocks   Id  System
> 			/dev/sdb1   *           1         243     1951866    c  W95 FAT32 (LBA)
>
>
>     6. Type **w** to write the partition table and quit.
>
> 2.  Format the USB flash drive with the Fat32 file system.
>
>         /sbin/mkfs.vfat -F 32 -n USB /dev/sdb1
>
>
> 3.  Run the following commands.
>
>         /path_to_syslinux-3.86_directory/syslinux-3.86/bin/syslinux /dev/sdb1
>         cat /path_to_syslinux-3.86_directory/syslinux-3.86/usr/share/syslinux/mbr.bin > /dev/sdb
>
>
> 4.  Mount the USB flash drive.
>
>         mount /dev/sdb1 /usbdisk
>
>
> 5.  Mount the ESXi installer ISO image.
>
>         mount -o loop VMware-VMvisor-Installer-5.x.x-XXXXXX.x86_64.iso /esxi_cdrom
>
>
> 6.  Copy the contents of the ISO image to /usbdisk.
>
>         cp -r /esxi_cdrom/* /usbdisk
>
>
> 7.  Rename the **isolinux.cfg** file to **syslinux.cfg**.
>
>         mv /usbdisk/isolinux.cfg /usbdisk/syslinux.cfg
>
>
> 8.  In the file **/usbdisk/syslinux.cfg**, change the line **APPEND -c boot.cfg** to **APPEND -c boot.cfg -p 1**.
>
> 9.  Unmount the USB flash drive.
>
>         umount /usbdisk
>
>
> 10. Unmount the installer ISO image.
>
>         umount /esxi_cdrom
>

I plugged in my USB drive on my fedora box and I saw the following in the logs:

    elatov@fed:~$ dmesg | tail
    [344963.649354] usb-storage 2-2:1.0: USB Mass Storage device detected
    [344963.656236] scsi7 : usb-storage 2-2:1.0
    [344964.660238] scsi 7:0:0:0: Direct-Access     SanDisk                   1.26 PQ: 0 ANSI: 5
    [344964.663088] sd 7:0:0:0: Attached scsi generic sg2 type 0
    [344964.667184] sd 7:0:0:0: [sdb] 15633408 512-byte logical blocks: (8.00 GB/7.45 GiB)
    [344964.668689] sd 7:0:0:0: [sdb] Write Protect is off
    [344964.668693] sd 7:0:0:0: [sdb] Mode Sense: 43 00 00 00
    [344964.669697] sd 7:0:0:0: [sdb] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
    [344964.680956]  sdb: sdb1
    [344964.684574] sd 7:0:0:0: [sdb] Attached SCSI removable disk


We can see that our drive is **/dev/sdb**. Now let's go ahead and create a FA32 partition on the USB disk:

    elatov@fed:~$sudo fdisk /dev/sdb

    Welcome to fdisk (util-linux 2.24.1).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.

    Device does not contain a recognized partition table.

    Created a new DOS disklabel with disk identifier 0x504de632.

    Command (m for help): n

    Partition type:
       p   primary (0 primary, 0 extended, 4 free)
       e   extended
    Select (default p): p
    Partition number (1-4, default 1):
    First sector (2048-15633407, default 2048):
    Last sector, +sectors or +size{K,M,G,T,P} (2048-15633407, default 15633407):

    Created a new partition 1 of type 'Linux' and of size 7.5 GiB.

    Command (m for help): t
    Selected partition 1
    Hex code (type L to list all codes): c
    If you have created or modified any DOS 6.x partitions, please see the fdisk documentation for additional information.
    Changed type of partition 'Linux' to 'W95 FAT32 (LBA)'.

    Command (m for help): a
    Selected partition 1
    The bootable flag on partition 1 is enabled now.

    Command (m for help): p
    Disk /dev/sdb: 7.5 GiB, 8004304896 bytes, 15633408 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x504de632

    Device    Boot Start       End  Blocks  Id System
    /dev/sdb1 *     2048  15633407 7815680   c W95 FAT32 (LBA)

    Command (m for help): w

    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.


Now let's actually format our partition as a FAT32 filesystem:

    elatov@fed:~$sudo mkfs.vfat -F 32 -n USB /dev/sdb1
    mkfs.fat 3.0.26 (2014-03-07)


Now let's put a bootloader on there:

    elatov@fed:~$sudo syslinux /dev/sdb1


Lastly let's but an MBR on there as well:

    elatov@fed:~$sudo dd if=/usr/share/syslinux/mbr.bin of=/dev/sdb bs=4k
    0+1 records in
    0+1 records out
    440 bytes (440 B) copied, 0.0141524 s, 31.1 kB/s


Now let's mount the USB disk:

    elatov@fed:~$sudo mount /dev/sdc1 /mnt/usb
    elatov@fed:~$df -hT -t vfat
    Filesystem     Type  Size  Used Avail Use% Mounted on
    /dev/sdb1      vfat  7.5G   36K  7.5G   1% /mnt/usb


Next let's mount the ISO:

    elatov@fed:~$sudo mount -o loop downloads/ESXi-5.5u1-MacMini-6-2.iso /mnt/iso
    mount: /dev/loop0 is write-protected, mounting read-only


And now let's copy the install files to the USB disk:

    elatov@fed:~$sudo rsync -avzP /mnt/iso/. /mnt/usb/.
    ..
    ...
    sent 337,011,106 bytes  received 2,057 bytes  4,919,900.19 bytes/sec
    total size is 343,461,997  speedup is 1.02


And the last thing is to copy the **syslinux.cfg** file:

    elatov@fed:~$sudo mv /mnt/usb/isolinux.cfg /mnt/usb/syslinux.cfg


Now the USB Disk is ready, so let's go ahead and un-mount the USB and the ISO:

    elatov@fed:~$sudo umount /mnt/iso
    elatov@fed:~$sudo umount /mnt/usb
    elatov@fed:~$sudo sync


Now eject the USB disk and plug into the Mac Mini

### Creating Bootable USB disk with Unebootin

Other people have used the Unebootin utility with success as well. If you don't want to copy the files manually and install the boot loader manually you can use Unebootin. After you have created the FAT32 partition and mounted it on the system, then go ahead and install the necessary package:

    elatov@fed:~$sudo yum install unetbootin


Then run the following to start the install:

    eltov@fed:~$sudo unetbootin method=diskimage isofile="downloads/ESXi-5.5u1-MacMini-6-2.iso"  installtype=USB targetdrive=/dev/sdb1


After you type that you will see a UI pop up, click install and you should see the following:

![installing unetbootin ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/installing-unetbootin.png)

You can see it takes care of most of the setup. After it's finished you will see the following:

![unetbootin finished ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/unetbootin-finished.png)

You don't have reboot, just click **exit** and eject the USB disk.

### Installing ESXi on the MacMini

After you have plugged in the USB drive into the Mac Mini, power it on and as soon as you hear the boot chime click and hold the **Alt/Option** button until you see the boot selection screen:

![mac mini boot screen 1024x577 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/mac-mini-boot-screen.jpg)

Select the "**EFI Boot**" option and the installer will start:

![esxi installer started 1024x305 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxi-installer-started.jpg)

It will ask you which drive to install ESXi, I chose the local SSD drive:

![esxi select disk g 1024x513 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxi-select-disk_g.jpg)

After that the installer will start:

![esxi installing g 1024x261 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxi-installing_g.jpg)

And after the install is successful, you should see the following:

![esxi installed g 1024x517 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxi-installed_g.jpg)

Click Enter to reboot and after it reboots you should see the default ESXi console:

![esxi reboot loca gl 720x1024 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxi-reboot-loca_gl.jpg)

Now your ESXi host is ready.

### Confirm ESXi Settings on Mac Mini

First let's make sure Interrupt Remapping is disabled, since so many people ran into any issue with that:

    ~ # esxcli system settings kernel list -o iovDisableIR
    Name          Type  Description                              Configured  Runtime  Default
    ------------  ----  ---------------------------------------  ----------  -------  -------
    iovDisableIR  Bool  Disable Interrrupt Routing in the IOMMU  true        TRUE     FALSE


That looks good, now let's sure Hyper-Threading is enabled, we should see 8 CPUs:

    ~ # esxcli hardware cpu list | grep ^CPU
    CPU:0
    CPU:1
    CPU:2
    CPU:3
    CPU:4
    CPU:5
    CPU:6
    CPU:7


While we are here let's confirm we have the full 16GB of RAM:

    ~ # esxcli hardware memory get
       Physical Memory: 17081536512 Bytes
       Reliable Memory: 0 Bytes
       NUMA Node Count: 1


And let's make sure we are running on the Mac Mini:

    ~ # esxcli hardware platform get
    Platform Information
       UUID: 0xf9 0x55 0x7 0x8b 0x4f 0xf2 0x58 0x55 0x98 0x36 0xc 0x74 0x1a 0x9e 0x82 0xc3
       Product Name: Macmini6,2
       Vendor Name: Apple Inc.
       Serial Number: XXXXXX
       IPMI Supported: false


We can also check out the SSD drive:

    ~ # esxcli storage core device list
    t10.ATA_____APPLE_SSD_SM256E____S1AANYNF302924______
       Display Name: Local ATA Disk (t10.ATA____APPLE_SSD_SM256E_____S1AANYNF302924____)
       Has Settable Display Name: true
       Size: 239372
       Device Type: Direct-Access
       Multipath Plugin: NMP
       Devfs Path: /vmfs/devices/disks/t10.ATA__APPLE_SSD_SM256E_S1AANYNF302924____
       Vendor: ATA
       Model: APPLE SSD SM256E
       Revision: DXM0
       SCSI Level: 5
       Is Pseudo: false
       Status: on
       Is RDM Capable: false
       Is Local: true
       Is Removable: false
       Is SSD: true
       Is Offline: false
       Is Perennially Reserved: false
       Queue Full Sample Size: 0
       Queue Full Threshold: 0
       Thin Provisioning Status: yes
       Attached Filters:
       VAAI Status: unknown
       Other UIDs: vml.0100000000533141414e594e463330323932342020202020204150504c4520
       Is Local SAS Device: false
       Is Boot USB Device: false
       No of outstanding IOs with competing worlds: 32


### Enable the Thunderbolt Ethernet Adapter

The instructions for that are laid out [here](http://www.virtuallyghetto.com/2013/09/running-esxi-55-on-apple-mac-mini.html). First download the custom VIB:

    elatov@fed:~$wget https://s3.amazonaws.com/virtuallyghetto-download/vghetto-apple-thunderbolder-ethernet.vib


Then copy the VIB to the host:

    elatov@fed:~$scp vghetto-apple-thunderbolder-ethernet.vib root@macm:/vmfs/volumes/datastore1/.


Lastly SSH over to the host and install the VIB. Initially I got the following error:

    ~ # esxcli software vib install -v /vmfs/volumes/datastore1/vghetto-apple-thunde
    rbolder-ethernet.vib
     [DependencyError]
     VIB virtuallyGhetto_bootbank_vghetto-apple-thunderbolt-ethernet_5.5.0-0.0.1's acceptance level is community, which is not compliant with the ImageProfile acceptance level partner
     To change the host acceptance level, use the 'esxcli software acceptance set' command.
     Please refer to the log file for more details.


Let's fix the Acceptance level:

    ~ # esxcli software acceptance set --level=CommunitySupported
    Host acceptance level changed to 'CommunitySupported'.


Then install the VIB:

    ~ # esxcli software vib install -v /vmfs/volumes/datastore1/vghetto-apple-thunde
    rbolder-ethernet.vib
    Installation Result
       Message: Operation finished successfully.
       Reboot Required: false
       VIBs Installed: virtuallyGhetto_bootbank_vghetto-apple-thunderbolt-ethernet_5.5.0-0.0.1
       VIBs Removed:
       VIBs Skipped:


Then after a restart, you should see two network adapters:

    ~ # esxcli network nic list
    Name    PCI Device     Driver  Link  Speed  Duplex  MAC Address         MTU  Description
    ------  -------------  ------  ----  -----  ------  -----------------  ----  -------------------------------------------------------------
    vmnic0  0000:001:00.0  tg3     Up     1000  Full    68:5b:35:c9:96:10  1500  Broadcom Corporation NetXtreme BCM57766 Gigabit Ethernet
    vmnic1  0000:009:00.0  tg3     Up     1000  Full    68:5b:35:91:47:85  1500  Broadcom Corporation NetXtreme BCM57762 Gigabit Ethernet PCIe


### Configure iSCSI Initiator

I was running an iSCSI target on my OmniOS (I covered the setup [iSCSI Storage Setup with ESXCLI](/2014/01/zfs-iscsi-benchmarks-tests/). Let's enable the initiator and confirm it's on:

    ~ # esxcli iscsi software set -e true
    Software iSCSI Enabled
    ~ # esxcli iscsi software get
    true


Now let's figure out which vmhba was assigned for the iSCSI initiator:

    ~ # esxcli iscsi adapter list
    Adapter  Driver     State   UID            Description
    -------  ---------  ------  -------------  ----------------------
    vmhba37  iscsi_vmk  online  iscsi.vmhba37  iSCSI Software Adapter


It looks like it's **vmhba37**. Now let's bind our **vmk1** to it (I created one for the storage connection)

    ~ # esxcli iscsi networkportal add -n vmk1 -A vmhba37
    ~ # esxcli iscsi networkportal list
    vmhba37
       Adapter: vmhba37
       Vmknic: vmk1


Now let's add our iSCSI target:

    ~ # esxcli iscsi adapter discovery sendtarget add -A vmhba37 -a 192.168.1.101:3260


If necessary grab the IQN of the iSCSI initiator:

    ~ # esxcli iscsi adapter get -A vmhba37
    vmhba37
       Name: iqn.1998-01.com.vmware:macm-38de6805
       Alias:
       Vendor: VMware
       Model: iSCSI Software Adapter
       Description: iSCSI Software Adapter


Now let's check out our ZFS server and make sure we are allowed to connect. After you SSH to the machine, check out your LUNs:

    root@zfs:~#sbdadm list-lu
    Found 2 LU(s)

                  GUID       DATA SIZE           SOURCE
    ----------------------  -------------------  ----------------
    600144f0876a9c47000052  322122547200         /dev/zvol/rdsk/data/m2
    600144f0876a9c47000052  214748364800         /dev/zvol/rdsk/other/backups


Now let's check out the view for the desired LUN:

    root@zfs:~#stmfadm list-view -l 600144f0876a9c47000052
    View Entry: 0
        Host group   : All
        Target group : tg1
        LUN          : 7


We can see that All Host groups are allowed to connect to that LUN. If had an explicit host group defined, we would've had to add our IQN to it (but we didn't have to do that). Now that we confirmed that we can connect to the iSCSI target, let's discover the LUNs and rescan our datastores:

    ~ # esxcli iscsi adapter discovery rediscover -A vmhba37
    Rediscovery started
    ~ # esxcli storage core adapter rescan --adapter=vmhba37


In the logs we should see similar messages to these:

    ~ # tail -7 /var/log/vmkernel.log
    2014-04-05T00:38:06.284Z cpu5:219519)iscsi_vmk: iscsivmk_ConnNetRegister: socket 0x41096b6bef60 network resource pool netsched.pools.persist.iscsi associated
    2014-04-05T00:38:06.284Z cpu5:219519)iscsi_vmk: iscsivmk_ConnNetRegister: socket 0x41096b6bef60 network tracker id 168 tracker.iSCSI.192.168.1.101 associated
    2014-04-05T00:38:06.789Z cpu5:219519)WARNING: iscsi_vmk: iscsivmk_StartConnection: vmhba37:CH:0 T:0 CN:0: iSCSI connection is being marked "ONLINE"
    2014-04-05T00:38:06.789Z cpu5:219519)WARNING: iscsi_vmk: iscsivmk_StartConnection: Sess [ISID: 00023d000001 TARGET: iqn.2010-09.org.napp-it:1387343318 TPGT: 1 TSIH: 0]
    2014-04-05T00:38:06.789Z cpu5:219519)WARNING: iscsi_vmk: iscsivmk_StartConnection: Conn [CID: 0 L: 192.168.1.109:57860 R: 192.168.1.101:3260]


Now checking out our devices, we should see the following:

    ~ # esxcfg-scsidevs -c | grep SUN
    naa.600144     Direct-Access    /vmfs/devices/disks/naa.600144  307200MB  NMP     SUN iSCSI Disk (naa.600144)


Now checking the specifics of the device:

    ~ # esxcli storage core device list -d naa.600144f08
    naa.600144f08
       Display Name: SUN iSCSI Disk (naa.600144f08)
       Has Settable Display Name: true
       Size: 204800
       Device Type: Direct-Access
       Multipath Plugin: NMP
       Devfs Path: /vmfs/devices/disks/naa.600144f08
       Vendor: SUN
       Model: COMSTAR
       Revision: 1.0
       SCSI Level: 5
       Is Pseudo: false
       Status: degraded
       Is RDM Capable: true
       Is Local: false
       Is Removable: false
       Is SSD: false
       Is Offline: false
       Is Perennially Reserved: false
       Queue Full Sample Size: 0
       Queue Full Threshold: 0
       Thin Provisioning Status: yes
       Attached Filters:
       VAAI Status: unknown
       Other UIDs: vml.0200000000600144f08
       Is Local SAS Device: false
       Is Boot USB Device: false
       No of outstanding IOs with competing worlds: 32


This volume already had VMFS on it, show we should see it mounted:

    ~ # esxcli storage filesystem list | grep VMFS
    /vmfs/volumes/520-731-c1cc-0100  M2   520-731-c1cc-0100     true  VMFS-5  321854111744  106085482496


Now let's migrate some VMs to the Mac Mini.

### Options to copy a VM without vCenter

I didn't have a vCenter running so I had to do some manual steps. There are a couple of ways of doing this:

*   You can use VMware Converter, [here](http://www.youtube.com/watch?v=Jf4_4sTNBg8) is a pretty cool video on the process
*   You can use **vmkfstools** and cp, like Jarret described [here](http://virtuallyhyper.com/2012/04/cloning-a-vm-from-the-command-line/):

*   Some people have also used Veeam Fast Copy, as described [here](http://www.vmwarevideos.com/video-using-free-fast-veeam-fastscp-transfer-vm-iso-vsphere):
*   Another cool one, that I wanted to try was using ovftool, that process is described [here](http://www.virtuallyghetto.com/2012/06/how-to-copy-vms-directly-between-esxi.html).

### Migrate VM with ovftool

If you want you can follow the instructions laid out [here](http://www.virtuallyghetto.com/2012/05/how-to-deploy-ovfova-in-esxi-shell.html) to copy the binary to the ESXi host and run it from there. If you have **vmware-ovftool** installed on your Linux machine, just run the following to copy the binary:

    elatov@fed:~$scp -r /usr/lib/vmware-ovftool root@esx:/vmfs/volumes/datastore1/.


Then modify the script (**/vmfs/volumes/datastore1/vmware-ovftool/ovftool**) to use **/bin/sh** instead of **/bin/bash**:

    ~ # head -1 /vmfs/volumes/datastore1/vmware-ovftool/ovftool
    #!/bin/sh


Then you can do the rest with the command. I already had **vmware-ovftool** installed on my Linux machine, so I just ran it from there. First determine which VM you want to tranfer:

    elatov@fed:~$ovftool vi://root@esx/
    Accept SSL fingerprint (72:14:A0:55:65:99:C8:21:0F:60:FA:DB:87:1E:B1:7B:A2:19:DA:50) for host esx as source type.
    Fingerprint will be added to the known host file
    Write 'yes' or 'no'
    yes
    Enter login information for source vi://esx/
    Username: root
    Password: ********
    Error: Found wrong kind of object (ResourcePool). Possible completions are:
      Kerch
      Moxz


Then run the following to do the transfer, initially I ran into the following error:

    elatov@fed:~$ovftool -ds=datastore1 vi://root@esx/Kerch vi://root@macm
    Enter login information for source vi://esx/
    Username: root
    Password: ********
    Opening VI source: vi://root@esx:443/Kerch
    Accept SSL fingerprint (1C:3A:31:99:06:8C:57:6F:A5:49:AF:8D:9B:A6:D9:00:76:3D:63:44) for host macm as target type.
    Fingerprint will be added to the known host file
    Write 'yes' or 'no'
    yes
    Enter login information for target vi://macm/
    Username: root
    Password: ********
    Opening VI target: vi://root@macm:443/
    Error: No network mapping specified. OVF networks:   Mgmt_Net. Target networks:   VM Network  VM_Net_VLAN_1
    Completed with errors


I had to create the Virtual Port Group on the Destination host before starting the transfer. So after fixing that, it ran without issues:

    elatov@fed:~$ovftool -ds=datastore1 vi://root@esx/Kerch vi://root@macm
    Enter login information for source vi://esx/
    Username: root
    Password: ********
    Opening VI source: vi://root@esx:443/Kerch
    Enter login information for target vi://macm/
    Username: root
    Password: ********
    Opening VI target: vi://root@macm:443/
    Deploying to VI: vi://root@macm:443/
    Progress: 3%


The process was a little slow. After it was done, it showed the following:

    Transfer Completed
    Completed successfully


Here is an example of a 15GB VM:

    elatov@fed:~$time ovftool -ds=datastore1 vi://root@esx/Moxz vi://root@macm
    Enter login information for source vi://esx/
    Username: root
    Password: ***************
    Opening VI source: vi://root@esx:443/Moxz
    Enter login information for target vi://macm/
    Username: root
    Password: ***********
    Opening VI target: vi://root@macm:443/
    Deploying to VI: vi://root@macm:443/
    Transfer Completed
    Completed successfully

    real    10m41.248s
    user    5m27.957s
    sys     0m51.681s


So it took about 15 minutes. Checking out esxtop, I saw that it was transferring at about 100Mb/s:

![esxtop nfc copy ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/esxtop-nfc-copy.png)

I found a couple of links that talked about NFC (which is used for the transfer) and they talked about NFC (in converter) having slowed down because of enabling SSL:

*   [Disabling SSL for NFC data traffic in vCenter Server](http://kb.vmware.com/kb/2056830)
*   [Enable SSL Certificate Validation Over NFC](http://pubs.vmware.com/vsphere-51/index.jsp?topic=/com.vmware.vsphere.security.doc/GUID-B58A5750-A15C-4051-BD87-49F3B5C762B5.html)
*   [Increasing the cloning performance](https://communities.vmware.com/message/1851162)
*   [Copy VM by ovftool from ESXI 5 to ESXI 5 is slow](https://communities.vmware.com/thread/431090)

I wanted to figure out how to disable SSL on hostd or ovftool, but never had a chance. I think if we disable NFC SSL for hostd we should get better speeds. I am guessing something with the following settings:

    ~ # grep nfc /etc/vmware/config
    authd.proxy.nfc = "vmware-hostd:ha-nfc"
    authd.proxy.nfcssl = "vmware-hostd:ha-nfcssl"
    authd.proxy.vpxa-nfcssl = "vmware-vpxa:vpxa-nfcssl"
    authd.proxy.vpxa-nfc = "vmware-vpxa:vpxa-nfc"


or these:

     # grep nfc /etc/vmware/hostd/config.xml
          <!-- The nfc service -->
          <nfcsvc>
             <path>libnfcsvc.so</path>
          </nfcsvc>
          <httpnfcsvc>
             <path>libhttpnfcsvc.so</path>
          </httpnfcsvc>


I only had 3 VMs to migrate, so I didn't spend too much time with figuring out how to disable SSL with NFC for hostd.

Even though it was slow, it was very easy and it worked without any issues. Next I decided to use PowerCLI to transfer another VM.

### Migrate VM with PowerCLI

There are a lot of cool cmdlets (like [Set-HardDisk](https://www.vmware.com/support/developer/PowerCLI/PowerCLI55/html/Move-VM.html)) that can help. Here are examples of each:

*   [Storage VMotion – The PowerCLI way](http://www.virtu-al.net/2009/06/11/storage-vmotion-the-powercli-way/)
*   [Storage vMotion only one hard disk to another datastore in vSphere](http://ict-freak.nl/2011/04/01/storage-vmotion-only-one-hard-disk-to-another-datastore-in-vsphere/)
*   [PowerShell – The first kiss with VMware PowerCLI](http://geekswithblogs.net/Wchrabaszcz/archive/2013/10/05/powershell--the-first-kiss-with-vmware-powercli.aspx)

Unfortunately all of those required vCenter to work. So I decided to copy the hard disk. So let's get started. Here is the version of PowerCLI that I downloaded:

![powercli ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/powercli.png)

After installing PowerCLI and launching it, I saw the following warning:

![powercli warning policy ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/powercli-warning-policy.png)

I then ran the following to set the appropriate Policy:

    PS C:\> Set-ExecutionPolicy RemoteSigned
    Execution Policy Change
    The execution policy helps protect you from scripts that you do not trust.
    Changing the execution policy might expose you to the security risks described
    in the about_Execution_Policies help topic. Do you want to change the execution
     policy?
    [Y] Yes  [N] No  [S] Suspend  [?] Help (default is "Y"):


Then after relaunching PowerCli and you will see the following:

![powercli started ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/powercli-started.png)

Now let's connect to our original ESXi host:

    PowerCLI C:\> Connect-VIServer esx -User root
    Name                           Port  User
    ----                           ----  ----
    esx                            443   root


Now let's list our VMs:

    PowerCLI C:\> get-vm

    Name                 PowerState Num CPUs MemoryGB
    ----                 ---------- -------- --------
    M2                   PoweredOn  1        3.000
    Moxz                 PoweredOn  1        2.000
    Kerch                PoweredOn  1        1.000


And now let's get the Datastores

    PowerCLI C:\> Get-Datastore

    Name                               FreeSpaceGB      CapacityGB
    ----                               -----------      ----------
    VMs                                    435.369         555.750
    M2                                      98.801         299.750
    datastore1                              61.051          62.000
    backups                                159.043         199.750


Now to get a sense of VMDK usage

    PowerCLI C:\> foreach ($VM in get-vm){$VM | get-HardDisk}

    CapacityGB      Persistence                                            Filename
    ----------      -----------                                            --------
    20.000          Persistent                                     [VMs] M2/M2.vmdk
    200.000         Persistent                                    [M2] M2/M2_1.vmdk
    15.000          Persistent                                 [VMs] Moxz/Moxz.vmdk
    16.000          Persistent                               [VMs] Kerch/Kerch.vmdk


I am planning on moving the **M2** machine to the **M2** datastore. So the VM we are moving (M2) has two hard-disks, one is already on **M2** and the first one is on the **VMs** datastore and it's only 20GB (we have 90GB free on the M2 datastore, so we are okay to do the move. So let's move the **M2** VM to the **M2** datastore. First shutdown the VM (if it has *vmware-tools* installed, else shut it down through the OS):

    PowerCLI C:\> Get-VM M2 | Shutdown-VMGuest

    Perform operation?
    Performing operation "Shutdown VM guest." on VM "M2".
    [Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help
    (default is "Y"):y

    State          IPAddress            OSFullName
    -----          ---------            ----------
    ShuttingDown   {192.168.1.100}      Linux 3.13.7-200.fc20.x86_64 Fedora rele...


Then copy the harddisk

    PowerCLI C:\> Copy-HardDisk -HardDisk (Get-HardDisk -vm M2  | Where {$_.Name -eq "Hard disk 1"}) -DestinationPath "[M2] M2"

    CapacityGB      Persistence                                            Filename
    ----------      -----------                                            --------
    20.000          Unknown                                         [M2] M2/M2.vmdk


I also checked out **esxtop** and it was copying fast (in comparison with NFC), we were transferring at 100MB/s (800Mb/s):

![copy disk esxtop g ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/copy-disk-esxtop_g.png)

Next we are going to copy the VMX file. To copy a file, we need to know the **datacenter** name, here is that:

    PowerCLI C:\> Get-Datacenter
    Name
    ----
    ha-datacenter


Now let's go ahead and copy the VMX file:

    PowerCLI C:\> Copy-DatastoreItem -Item vmstore:\ha-datacenter\VMs\M2\M2.vmx -Des
    tination vmstore:\ha-datacenter\M2\M2\M2.vmx


Now go ahead and remove the VM from the original host's inventory

    PowerCLI C:\> Remove-VM M2

    Perform operation?
    Performing operation 'Removing VM from inventory.' on VM 'M2'
    [Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help
    (default is "Y"):y


Next let's disconnect from this host and connect to the mac mini:

    PowerCLI C:\> Disconnect-VIServer

    Confirm
    Are you sure you want to perform this action?
    Performing operation "Disconnect VIServer" on Target "User: root, Server: esx,
    Port: 443".
    [Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help
    (default is "Y"):y


Now for the re-connect to the new host:

    PowerCLI C:\> Connect-VIServer macm
    Name                           Port  User
    ----                           ----  ----
    macm                           443   root


Let's copy the harddisk to the local datastore of the new host:

    PowerCLI C:\> Copy-HardDisk -HardDisk (Get-HardDisk -Datastore "M2" -DatastorePath "[M2] M2/" | where {$_.Name -eq "M2.vmdk"}) -DestinationPath "[datastore1] M2
    "

    CapacityGB      Persistence                                            Filename
    ----------      -----------                                            --------
    20.000          Unknown                                    [datastore1] M2.vmdk


You will see the following when you execute the copy:

![powecli copy command ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/powecli-copy-command.png)

Also checked out **esxtop** on the new host and the speeds were similar:

![copy disk macm esxtop g 1024x67 ESXi on MacMini 6,2](https://github.com/elatov/uploads/raw/master/2014/04/copy-disk-macm-esxtop_g.png)

And let's go ahead and copy the VMX over:

    PowerCLI C:\> Copy-DatastoreItem -Item vmstore:\ha-datacenter\M2\M2\M2.vmx -Dest
    ination vmstore:\ha-datacenter\datastore1\M2\M2.vmx


Now let's add the VM to nee ESXi's host inventory

    PowerCLI C:\> New-VM -VMFilePath "[datastore1] M2/M2.vmx" -VMHost macm

    Name                 PowerState Num CPUs MemoryGB
    ----                 ---------- -------- --------
    M2                   PoweredOff 1        3.000


Let's make sure the disk locations are correct:

    PowerCLI C:\> get-vm M2 | Get-HardDisk

    CapacityGB      Persistence                                            Filename
    ----------      -----------                                            --------
    20.000          Persistent                              [datastore1] M2/M2.vmdk
    200.000         Persistent                                    [M2] M2/M2_1.vmdk


I was surprised to see this automatically pick up the correct locations, but it did :) (I was thinking that I would have to fix the VM settings with other commands).Then go ahead and start the VM:

    PowerCLI C:\> Start-VM M2
    Start-VM : 4/5/2014 11:42:48 AM    Start-VM        This VM has questions that must be answered before the operation can continue.
    At line:1 char:9
    + Start-VM <<<<  M2
        + CategoryInfo          : InvalidOperation: (:) [Start-VM], VmBlockedByQuestionException
        + FullyQualifiedErrorId : Client20_VmServiceImpl_WrapInVMQuestionWatchingTask_HasQuestions,VMware.VimAutomation.ViCore.Cmdlets.Commands.StartVM


Since we copied the files (we need to let ESX know whether we *moved it* or *copied it*), we can then run the following to answer the question:

    PowerCLI C:\> Get-VMQuestion | Set-VMQuestion -Option 'button.uuid.movedTheVM"


And that's it, the VM is now completely migrated over and it way quicker than the **ovftool** approach. But I still really like the simplicity of the **ovftool**.

