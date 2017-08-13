---
published: true
layout: post
title: "SSD Performance Degradation and SCSI UNMAP Command"
author: Karim Elatov
categories: [vmware,storage,home_lab,zfs]
tags: [ssd,unmap]
---
### SSD Drives
So I had two sets of SSDs in my VMware setup, one on the local mac mini:


    [root@macm:~] esxcli storage core device list -d t10.ATA_APPLE_SSD_SM256E
    t10.ATA_APPLE_SSD_SM256E
       Display Name: Local ATA Disk (t10.ATA_APPLE_SSD_SM256E)
       Has Settable Display Name: true
       Size: 239372
       Device Type: Direct-Access
       Multipath Plugin: NMP
       Devfs Path: /vmfs/devices/disks/t10.ATA_APPLE_SSD_SM256E
       Vendor: ATA
       Model: APPLE SSD SM256E
       Revision: 2A0Q
       SCSI Level: 5
       Is Pseudo: false
       Status: on
       Is RDM Capable: false
       Is Local: true
       Is Removable: false
       Is SSD: true
       Is VVOL PE: false
       Is Offline: false
       Is Perennially Reserved: false
       Queue Full Sample Size: 0
       Queue Full Threshold: 0
       Thin Provisioning Status: yes
       Attached Filters:
       VAAI Status: unknown
       Other UIDs: vml.0100000000533141414e594e463330323932342020202020204150504c4520
       Is Shared Clusterwide: false
       Is Local SAS Device: false
       Is SAS: false
       Is USB: false
       Is Boot USB Device: false
       Is Boot Device: true
       Device Max Queue Depth: 31
       No of outstanding IOs with competing worlds: 32
       Drive Type: unknown
       RAID Level: unknown
       Number of Physical Drives: unknown
       Protection Enabled: false
       PI Activated: false
       PI Type: 0
       PI Protection Mask: NO PROTECTION
       Supported Guard Types: NO GUARD SUPPORT
       DIX Enabled: false
       DIX Guard Type: NO GUARD SUPPORT
       Emulated DIX/DIF Enabled: false

And a couple on my OmniOS ZFS storage:

    <> sg_vpd -p ai /dev/rdsk/c2t4d0
    ATA information VPD page:
      SAT Vendor identification: ATA     
      SAT Product identification: Samsung SSD 840 
      SAT Product revision level: BB6Q
      Device signature indicates PATA transport
      ATA command IDENTIFY DEVICE response summary:
        model: Samsung SSD 840 EVO 250GB               
        serial number: ftrt     
        firmware revision: EXT0BB6Q

### SSD Performance Degradation
Over a period of 4 years, the SSDs became slow and slower. I noticed that backups would take longer to complete over time. Reading over a couple of pages, it seems that SSD degradation is pretty normal. After some time as the drive fills up it will become slow, and actually doing an **UNMAP** on SSD drives can help out:

- [FAQ: Using SSDs with ESXi (Updated)](https://www.v-front.de/2013/10/faq-using-ssds-with-esxi.html)
- [Exploring the Relationship Between Spare Area and Performance Consistency in Modern SSDs](http://www.anandtech.com/show/6489/playing-with-op)
- [The Myth of SSD Performance Degradation](http://blog.houzz.com/post/115950977148/the-myth-of-ssd-performance-degradation) 

Some notes, from the above sites:

> Over time, our daily production traffic caused the SSDs to become fuller from their perspective. As a result, garbage collection was triggered more and more often until disk performance reached unacceptable levels. One natural way to solve the issue is to tell SSDs which data are deleted. Modern operating systems support an instruction called TRIM to allow file systems to pass the information to the underlying disks.

From another site:

> As the number of known free Flash cells decreases the write performance of the SSD also decreases because it heavily depends on the number of cells that can be simultaneously written to.
>
> To address this issue the ATA TRIM command was introduced many years ago. Modern Operating Systems use the TRIM command to inform the SSD controller when they delete a block so that it can add the associated Flash cell to its free list and knows that it can be overwritten.

And here is the last one:

> It's because of this relationship between write amplification and spare area that we've always recommended setting aside 10 - 20% of your SSD and not filling it up entirely. Most modern controllers will do just fine if you partition the drive and leave the last 10 - 20% untouched. With TRIM support even the partitioning step isn't really necessary, but it does help from a data management standpoint.

### SCSI UNMAP with VMware

On the local drive I confirmed that **UNMAP** is supported (**Delete Status**):

    [root@macm:~] esxcli storage core device vaai status get -d t10.ATA_APPLE_SSD_SM256E
    t10.ATA_APPLE_SSD_SM256E
       VAAI Plugin Name:
       ATS Status: unsupported
       Clone Status: unsupported
       Zero Status: supported
       Delete Status: supported

Then I ran the following to send an **UNMAP** to the VMFS Datastore:

    [root@macm:~] esxcli storage vmfs unmap -l datastore1

That took about 2-3 minutes to complete, and in the logs I saw the following:

    [root@macm:~] tail -f /var/log/vmkernel
    2017-02-19T03:57:25.503Z cpu2:72098 opID=62289008)vmw_ahci[0000001f]: scsiUnmapCommand:Unmap transfer 0x18 byte
    2017-02-19T03:57:26.019Z cpu2:72098 opID=62289008)vmw_ahci[0000001f]: scsiUnmapCommand:Unmap transfer 0x18 byte
    2017-02-19T03:57:26.537Z cpu5:72098 opID=62289008)vmw_ahci[0000001f]: scsiUnmapCommand:Unmap transfer 0x48 byte
    2017-02-19T03:57:27.052Z cpu5:72098 opID=62289008)vmw_ahci[0000001f]: scsiUnmapCommand:Unmap transfer 0x18 byte

Then my performance on the local drive came back. I was able to write a file pretty quickly:

    [root@macm:/vmfs/volumes/533e29ae-e243ce90-39a5-685b35c99610] time vmkfstools -c
     15G -d eagerzeroedthick test.vmdk
    Creating disk 'test.vmdk' and zeroing it out...
    Create: 100% done.
    real	0m 34.59s
    user	0m 4.75s
    sys	0m 0.00s

Before running the **UNMAP** command, the above took 3 minutes.

### SCSI UNMAP with ZFS/Solaris

Reading over [OmniOS r151014](https://omnios.omniti.com/wiki.php/ReleaseNotes/r151014), it looks like with OmniOS version **r151014** it can handle **UNMAP**, which is great:

> New tunables:
- zfs_free_max_blocks (can reduce for less free blocks per transaction)
- zvol_unmap_enabled (can set to 0 to ignore UNMAP requests which can be slow)
- metaslabs_per_vdev (an upper limit per vdev, currently 200, now tunable)

And I did confirm that the ESXi host can see the **UNMAP** Primitive (the **Delete Status**) for the volume/LUN presented over iSCSI with Comstar:

    [root@macm:~] esxcli storage core device vaai status get -d naa.600144f070cc4400
    naa.600144f070cc44000
       VAAI Plugin Name:
       ATS Status: unsupported
       Clone Status: unsupported
       Zero Status: supported
       Delete Status: supported

However when I sent the **UNMAP** command to the LUN it ran really fast and it felt like it didn't do anything. I then ran into this interesting page: [ZFS and Intelligent Storage](https://blog.docbert.org/zfs-and-intelligent-storage/). Which talks about how **UNMAP** with ZFS doesn't work very well:

> By sending UNMAP/TRIM commands, ZFS can notify the array that a particular block of storage is no longer required, which on most arrays will trigger the array to re-thin-provision that block of storage, freeing the space it was using.
>
> Unfortunately that's where the good news ends. Solaris/ZFS added support for UNMAP in the Solaris 11.1 release, however their implementation was so horribly broken that they recommended disabling it in the release notes for the very same version! In a release soon after they disabled it by default, and despite it now being almost 4 years and 2 Solaris release later, they still do not recommend ever turning it on.
>
> Re-formatting the LUN and starting all over again gave exactly the same results - a few minutes into the random workload the pool once again reported data corruption - confirming Oracle's advice that turning on UNMAP for ZFS is not a good idea!

I then remembered a recommendation from napp-it: [Tuning/ best use](https://www.napp-it.org/manuals/tuning.html)

> Do not fill up SSDs as performance degrades. Use reservations or do a "secure erase" on SSDs that are not new, followed by overprovision SSDs with Host protected Areas,

### Formating SSD Drives in Solaris
I removed the LUN, I removed the volume, and I deleted the pool. Then I formatted the disks:

    <> format
    Searching for disks...done


    AVAILABLE DISK SELECTIONS:
           0. c2t0d0 <ATA-ST3808110AS-H cyl 9726 alt 2 hd 255 sec 63>
              /pci@0,0/pci1043,8534@1f,2/disk@0,0
           1. c2t1d0 <ATA-ST1000DM003-1CH162-CC47-931.51GB>
              /pci@0,0/pci1043,8534@1f,2/disk@1,0
           2. c2t2d0 <ATA-ST1000DM003-1CH162-CC47-931.51GB>
              /pci@0,0/pci1043,8534@1f,2/disk@2,0
           3. c2t3d0 <ATA-ST1000DM003-1ER162-CC45-931.51GB>
              /pci@0,0/pci1043,8534@1f,2/disk@3,0
           4. c2t4d0 <Samsung-SSD 840 EVO 250GB-EXT0BB6Q-232.89GB>
              /pci@0,0/pci1043,8534@1f,2/disk@4,0
           5. c2t5d0 <Samsung-SSD 840 EVO 250GB-EXT0BB6Q-232.89GB>
              /pci@0,0/pci1043,8534@1f,2/disk@5,0
    Specify disk (enter its number): 4
    selecting c2t4d0
    [disk formatted]

    FORMAT MENU:                                                             [33/57]
            disk       - select a disk
            type       - select (define) a disk type
            partition  - select (define) a partition table
            current    - describe the current disk
            format     - format and analyze the disk
            fdisk      - run the fdisk program
            repair     - repair a defective sector
            label      - write label to the disk
            analyze    - surface analysis
            defect     - defect list management
            backup     - search for backup labels
            verify     - read and display labels
            inquiry    - show vendor, product and revision
            volname    - set 8-character volume name
            !<cmd>     - execute <cmd>, then return
            quit
    format> analyze

    ANALYZE MENU:
            read     - read only test   (doesn't harm SunOS)
            refresh  - read then write  (doesn't harm data)
            test     - pattern testing  (doesn't harm data)
            write    - write then read      (corrupts data)
            compare  - write, read, compare (corrupts data)
            purge    - write, read, write   (corrupts data)
            verify   - write entire disk, then verify (corrupts data)
            print    - display data buffer
            setup    - set analysis parameters
            config   - show analysis parameters
            !<cmd>   - execute <cmd> , then return
            quit

    analyze> purge
    The purge command runs for a minimum of 4 passes plus a last pass if the
    first 4 passes were successful.
    Ready to purge (will corrupt data). This takes a long time,
    but is interruptible with CTRL-C. Continue? y

            pass 0 - pattern = 0xaaaaaaaa
       488397042  64  44

            pass 1 - pattern = 0x55555555
       488397042

            pass 2 - pattern = 0xaaaaaaaa
       488397042

            pass 3 - pattern = 0xaaaaaaaa
       488397042

    The last 4 passes were successful, running alpha pattern pass
            pass 4 - pattern = 0x40404040
       488397042

    Total of 0 defective blocks repaired.

Then I re-created the pool, volume, and LUN (more on the process check out the [ZFS iSCSI Benchmark Tests on ESX](/2014/01/zfs-iscsi-benchmarks-tests/) post). Before re-adding it to the ESXi host I ran a quick **bonnie++** and I got the following:

![zfs-bon-results](https://seacloud.cc/d/480b5e8fcd/files/?p=/ssd-unmap/zfs-bon-results.png&raw=1)

Before running the **purge** with the **format** utility, I got 60MB/s Write and 700MB/s for Read. I am glad to see my write performance back.

### Automatic UNMAP with vSphere 6.5
Then I read that with vSphere 6.5 and VMFS-6, **UNMAP** is automatic. From [What’s new in vSphere 6.5 Core Storage](http://cormachogan.com/2016/10/18/whats-new-vsphere-6-5-core-storage/):

> This is a feature I know that many of you have been waiting for. There is now automatic UNMAP with VMFS-6 and vSphere 6.5. This automated UNMAP crawler mechanism will reclaim what is termed “dead” or “stranded” space on VMFS-6 datastores. Blocks that have been freed will be reclaimed within 12 hours by the crawler. 

But unfortunately you can't do an upgrade: [Migrating VMFS 5 datastore to VMFS 6 datastore](https://kb.vmware.com/kb/2147824). So I moved everything off the local datastore and formatted it with VMFS-6. I also readded the ZFS LUN, formatted it with VMFS-6 from the get-go, and I was able to confirm that it's enabled:

    [root@core:~] esxcli storage vmfs reclaim config get -l datastore1
       Reclaim Granularity: 1048576 Bytes
       Reclaim Priority: low

BTW more information on that feature is here:

- [Automatic space reclamation (UNMAP) is back in vSphere 6.5](http://vsphere-land.com/news/automatic-space-reclamation-unmap-is-back-in-vsphere-6-5.html)
- [Using the esxcli storage vmfs unmap command to reclaim VMFS deleted blocks on thin-provisioned LUNs](https://kb.vmware.com/kb/2057513)
- [UNMAP](https://storagehub.vmware.com/#!/vsphere-core-storage/vsphere-6-5-storage/unmap)

If you run that on a VMFS-5 datastore you will see the following:

    [root@macm:~] esxcli storage vmfs reclaim config get -l  datastore1
    Failed to retrieve unmap property for filesystem, VMkernel log may contain more details.
    Reason: VMFS with version 5 does not support unmap property

Now hopefully with that enabled, the performance won't degrade as bad (but still 4 years on an SSD is great)
