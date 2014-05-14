---
title: Presenting a LUN over Fibre Channel from a NetApp FAS 3240 Array to an ESXi 5.0 Host Running on a Cisco UCS B200 Blade
author: Karim Elatov
layout: post
permalink: /2012/11/presenting-a-lun-from-a-netapp-fas-3240-arrya-to-an-esxi-5-0-host-running-on-a-cisco-ucs-b200-blade/
dsq_thread_id:
  - 1404939505
categories:
  - Storage
  - VMware
tags:
  - Cisco UCS B200
  - NetApp FAS3240
  - VMware ESX
---
## Confirming UCS Hardware on ESX(i)

First, let&#8217;s SSH over to the host and confirm the version of ESXi:

    ~ # vmware -lv
    VMware ESXi 5.0.0 build-469512
    VMware ESXi 5.0.0 GA 
    

That looks good, next let&#8217;s confirm the hardware that we are running on:

    ~ # esxcli hardware platform get
    Platform Information
       UUID: 0x74 0xd3 0x36 0x4 0x3c 0xe7 0x11 0xdf 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x11
       Product Name: N20-B6625-1
       Vendor Name: Cisco Systems Inc
       Serial Number: FCH1432V1HY
       IPMI Supported: true
    

Now let&#8217;s login to the UCS Manager via SSH and confirm our blade information as well. I actually wrote a <a href="http://virtuallyhyper.com/2012/08/confirming-ucs-settings-using-command-line/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/confirming-ucs-settings-using-command-line/']);">post</a> about this not too while ago. I knew that the name of my blade was &#8216;p1-b200-64&#8242;, so I searched for that.

    p1-ucsm-A# show service-profile inventory | grep p1-b200-64
    p1-b200-64           Instance          9/1     Assigned   Associated
    

There is my blade, it&#8217;s inside Chassis 9 and it&#8217;s server 1. So going into that server:

    p1-ucsm-A# scope chassis 9
    p1-ucsm-A /chassis # scope server 1
    

and looking over its hardware, I saw the following:

    p1-ucsm-A /chassis/server # show inventory
    Server 9/1:
        Name:
        User Label:
        Equipped PID: N20-B6625-1
        Equipped VID: V01
        Equipped Serial (SN): FCH1432V1HY
        Slot Status: Equipped
        Acknowledged Product Name: Cisco UCS B200 M2
        Acknowledged PID: N20-B6625-1
        Acknowledged VID: V01
        Acknowledged Serial (SN): FCH1432V1HY
        Acknowledged Memory (MB): 49152
        Acknowledged Effective Memory (MB): 49152
        Acknowledged Cores: 12
        Acknowledged Adapters: 1
    

So the hardware for my blade is &#8216;N20-B6625-1&#8242; and Serial is &#8220;FCH1432V1HY&#8221;; both matched, which is good.

## Confirming UCS HBA Connectivity

We are going to be connecting to our NetApp filer over Fibre Channel, so let&#8217;s make sure our WWNs are logged into the Cisco InterConnects. So first checking for the WWN from the ESXi host, we see the following:

    ~ # esxcfg-scsidevs -a
    vmhba0  mptsas            link-n/a  sas.50022bdd8c104000                    (0:1:0.0) LSI Logic / Symbios Logic LSI1064E
    vmhba1  fnic              link-up   fc.20010025b5000046:20000025b50a0046    (0:16:0.0) Cisco Systems Inc Cisco VIC FCoE HBA
    vmhba2  fnic              link-up   fc.20010025b5000046:20000025b50b0046    (0:17:0.0) Cisco Systems Inc Cisco VIC FCoE HBA
    

So we have &#8220;20010025b5000046:20000025b50a0046&#8243; and &#8220;20010025b5000046:20000025b50b0046&#8243; for both of our HBAs. Now checking the same thing from our UCSM, I saw the following:

    p1-ucsm-A /chassis/server # show adapter
    
    Adapter:
        Id         PID          Vendor          Serial          Overall Status
        ---------- ------------ --------------- --------------- --------------
                 1 N20-AC0002   Cisco Systems I QCI1515ACEY     Operable
    

This is the Cisco VIC (PALO card), now checking for information regarding the HBA part of the VIC, we see the following:

    p1-ucsm-A /chassis/server # scope adapter 1
    p1-ucsm-A /chassis/server/adapter # show host-fc-if
    
    FC Interface:
        Id         Wwn                     Model      Name       Operability
        ---------- ----------------------- ---------- ---------- -----------
                 1 20:00:00:25:B5:0A:00:46 N20-AC0002 fc0        Operable
                 2 20:00:00:25:B5:0B:00:46 N20-AC0002 fc1        Operable
    

So &#8220;20:00:00:25:B5:0A:00:46&#8243; and &#8220;20:00:00:25:B5:0B:00:46&#8243; match what we saw in ESXi. Usually in UCS Enclosures, you have two fabric inter-connects and each HBA is connected to a different fabric for redundancy purposes. So let&#8217;s ensure that is case with our blade:

    p1-ucsm-A /chassis/server # scope service-profile server 9/1
    p1-ucsm-A /org/service-profile # show vhba
    
    vHBA:
        Name       Fabric ID Dynamic WWPN
        ---------- --------- ------------
        fc0        A         20:00:00:25:B5:0A:00:46
        fc1        B         20:00:00:25:B5:0B:00:46
    

That looks good. Now let&#8217;s connect to the interconnects and check whether our WWNs show up there. First let&#8217;s check what interconnects we have:

    p1-ucsm-A /org/service-profile # show fabric-interconnect
    
    Fabric Interconnect:
        ID   OOB IP Addr     OOB Gateway     OOB Netmask     Operability
        ---- --------------- --------------- --------------- -----------
        A    10.101.100.13   10.101.100.1    255.255.255.0   Operable
        B    10.101.100.15   10.101.100.1    255.255.255.0   Operable
    

So let&#8217;s connect to the Fabric A:

    p1-ucsm-A /org/service-profile # connect nxos a
    Cisco Nexus Operating System (NX-OS) Software
    TAC support: http://www.cisco.com/tac
    Copyright (c) 2002-2012, Cisco Systems, Inc. All rights reserved.
    The copyrights to certain works contained in this software are
    owned by other third parties and used and distributed under
    license. Certain components of this software are licensed under
    the GNU General Public License (GPL) version 2.0 or the GNU
    Lesser General Public License (LGPL) Version 2.1. A copy of each
    such license is available at
    http://www.opensource.org/licenses/gpl-2.0.php and
    
    http://www.opensource.org/licenses/lgpl-2.1.php
    
    p1-ucsm-A(nxos)# show npv flogi-table | inc  20:00:00:25:b5:0a:00:46
    vfc3509   101  0x080051 20:00:00:25:b5:0a:00:46 20:01:00:25:b5:00:00:46 fc2/1
    

So our WWN is connected to virtual interface &#8220;vfc3509&#8243;. Checking out the setting for that interface, I saw the following:

    p1-ucsm-A(nxos)# show run int vfc3509
    
    !Command: show running-config interface vfc3509
    !Time: Sat Nov 24 10:16:46 2012
    
    version 5.0(3)N2(2.1w)
    
    interface vfc3509
      bind interface Vethernet11701
      switchport trunk allowed vsan 101
      switchport description server 9/1, VHBA fc0
      no shutdown
    

Also checking the interface itself, I saw the following:

    p1-ucsm-A(nxos)# show int vfc3509
    vfc3509 is trunking
        Bound interface is Vethernet11701
        Port description is server 9/1, VHBA fc0
        Hardware is Virtual Fibre Channel
        Port WWN is 2d:b4:00:05:73:dc:61:3f
        Admin port mode is F, trunk mode is on
        snmp link state traps are enabled
        Port mode is TF
        Port vsan is 101
        Trunk vsans (admin allowed and active) (101)
        Trunk vsans (up)                       ()
        Trunk vsans (isolated)                 ()
        Trunk vsans (initializing)             (101)
        1 minute input rate 0 bits/sec, 0 bytes/sec, 0 frames/sec
        1 minute output rate 0 bits/sec, 0 bytes/sec, 0 frames/sec
          77727 frames input, 7858896 bytes
            3 discards, 0 errors
          1364012 frames output, 2680397584 bytes
            0 discards, 0 errors
        last clearing of "show interface" counters never
        Interface last changed at Fri Nov  9 08:50:07 2012
    

The description matches our blade (server 9/1) and the port is operational. When I checked the other Fabric, I saw a similar setup. So we are all good from the enclosure side.

## Confiringm NetAPP Version and Model

Now logging into the array and checking it&#8217;s model and ONTAP version, I saw the following:

    p1-3240cl1-2> version
    NetApp Release 8.0.3P3 7-Mode: Tue Jul  3 22:29:01 PDT 2012
    

and

    p1-3240cl1-2> sysconfig -a
    NetApp Release 8.0.3P3 7-Mode: Tue Jul  3 22:29:01 PDT 2012
    System ID: 1xxxxx (p1-3240cl1-2); partner ID: xxxx (p1-3240cl2-2)
    System Serial Number: 7xxxx (p1-3240cl1-2)
    System Rev: F3
    System Storage Configuration: Multi-Path HA
    System ACP Connectivity: Full Connectivity
    slot 0: System Board 2.3 GHz (System Board XVI F3)
                    Model Name:         FAS3240
                    Part Number:        111-00693
                    Revision:           F3
                    Serial Number:      50xxxx
                    BIOS version:       5.1.1
                    Loader version:     3.2
                    Processors:         4
                    Processor ID:       0x1067a
                    Microcode Version:  0xa0b
                    Processor type:     Intel(R) Xeon(R) CPU           L5410  @ 2.33GHz
                    Memory Size:        8192 MB
                    Memory Attributes:  Bank Interleaving
                                        Hoisting
                                        Chipkill ECC
                    NVMEM Size:         1024 MB of Main Memory Used
                    CMOS RAM Status:    OK
    

So we have a FAS3240 running ONTAP version 8.0.3P3.

## NetAPP ONTAP Overview

Now before we go down further, we should take a look at the logical view of how NetApp handles it&#8217;s storage. From &#8220;<a href="http://www.buynetappstorage.com/download/netapp_fas6200_technical_report.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.buynetappstorage.com/download/netapp_fas6200_technical_report.pdf']);">The Benefits of Converged Networking with NetApp FAS6280 and Intel Xeon Servers</a>&#8220;,we see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ontap_logical_view.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ontap_logical_view.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ontap_logical_view.png" alt="ontap logical view Presenting a LUN over Fibre Channel from a NetApp FAS 3240 Array to an ESXi 5.0 Host Running on a Cisco UCS B200 Blade" title="ontap_logical_view" width="433" height="486" class="alignnone size-full wp-image-5008" /></a>

### ONTAP Aggregates

From the Storage Management Guide, here is a description of aggregates:

> **How aggregates work**  
> To support the differing security, backup, performance, and data sharing needs of your users, you group the physical data storage resources on your storage system into one or more aggregates. These aggregates provide storage to the volume or volumes that they contain. Each aggregate has its own RAID configuration, plex structure, and set of assigned disks or array LUNs. When you create an aggregate without an associated traditional volume, you can use it to hold one or more FlexVol volumes—the logical file systems that share the physical storage resources, RAID configuration, and plex structure of that common containing aggregate. When you create an aggregate with its tightly-bound traditional volume, then it can contain only that volume.

Someone had already created the aggregates for us, so checking out the available aggregates, I saw the following:

    p1-3240cl1-2> aggr status
               Aggr State           Status            Options
              aggr1 online          raid_dp, aggr     raidsize=16
                                    64-bit
              aggr0 online          raid_dp, aggr     root
                                    32-bit
    

So we had two: *aggr0* and *aggr1*. Checking out the size used by each I saw the following:

    p1-3240cl1-2> df -hA
    Aggregate                total       used      avail capacity
    aggr0                    707GB      675GB       32GB      95%
    aggr0/.snapshot           37GB     1015MB       36GB       3%
    aggr1                     25TB      981MB       25TB       0%
    aggr1/.snapshot         1378GB     4892MB     1373GB       0%
    

So *aggr0* was 707GB and *aggr1* was 25TB; I was going to use *aggr1*.

### ONTAP Raid Groups

Checking out what raid groups *aggr1* consisted of, I saw the following:

    p1-3240cl1-2> aggr status -v aggr1
               Aggr State           Status            Options
              aggr1 online          raid_dp, aggr     nosnap=off, raidtype=raid_dp,
                                    64-bit            raidsize=16,
                                                      ignore_inconsistent=off,
                                                      snapmirrored=off,
                                                      resyncsnaptime=60,
                                                      fs_size_fixed=off,
                                                      snapshot_autodelete=on,
                                                      lost_write_protect=on,
                                                      ha_policy=cfo
                    Volumes: <none>
    
                    Plex /aggr1/plex0: online, normal, active
                        RAID group /aggr1/plex0/rg0: normal
                        RAID group /aggr1/plex0/rg1: normal
                        RAID group /aggr1/plex0/rg2: normal
    

Looks like we had 3 raid groups. To check how many disks we have per raid, we could run the following:

    p1-3240cl1-2> sysconfig -V
    volume aggr1 (3 RAID groups):
            group 2: 11 disks
            group 1: 16 disks
            group 0: 16 disks
    volume aggr0 (1 RAID group):
            group 0: 3 disks
    

To list all the disks for each raid groups we can do this:

    p1-3240cl1-2> aggr status -r aggr1
    Aggregate aggr1 (online, raid_dp) (block checksums)
      Plex /aggr1/plex0 (online, normal, active, pool0)
        RAID group /aggr1/plex0/rg0 (normal)
    
          RAID Disk Device          HA  SHELF BAY CHAN Pool Type  RPM  Used (MB/blks)    Phys (MB/blks)
          --------- ------          ------------- ---- ---- ---- ----- --------------    --------------
          dparity   0a.01.0         0a    1   0   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          parity    5b.00.0         5b    0   0   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.1         0a    1   1   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.1         5b    0   1   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.2         0a    1   2   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.2         5b    0   2   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.3         0a    1   3   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.3         5b    0   3   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.4         0a    1   4   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.4         5b    0   4   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.5         0a    1   5   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.5         5b    0   5   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.6         0a    1   6   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.6         5b    0   6   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.7         0a    1   7   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.7         5b    0   7   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
    
        RAID group /aggr1/plex0/rg1 (normal)
    
          RAID Disk Device          HA  SHELF BAY CHAN Pool Type  RPM  Used (MB/blks)    Phys (MB/blks)
          --------- ------          ------------- ---- ---- ---- ----- --------------    --------------
          dparity   5b.00.8         5b    0   8   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          parity    0a.01.8         0a    1   8   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.9         5b    0   9   SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.9         0a    1   9   SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.10        5b    0   10  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.10        0a    1   10  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.11        5b    0   11  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.11        0a    1   11  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.12        5b    0   12  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.12        0a    1   12  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.13        5b    0   13  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.13        0a    1   13  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.14        5b    0   14  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.14        0a    1   14  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.15        5b    0   15  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.15        0a    1   15  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
    
        RAID group /aggr1/plex0/rg2 (normal)
    
          RAID Disk Device          HA  SHELF BAY CHAN Pool Type  RPM  Used (MB/blks)    Phys (MB/blks)
          --------- ------          ------------- ---- ---- ---- ----- --------------    --------------
          dparity   0a.01.16        0a    1   16  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          parity    5b.00.16        5b    0   16  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.17        0a    1   17  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.17        5b    0   17  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.18        0a    1   18  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.18        5b    0   18  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.19        0a    1   19  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.19        5b    0   19  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.20        0a    1   20  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      5b.00.20        5b    0   20  SA:B   0  BSAS  7200 847555/1735794176 847884/1736466816
          data      0a.01.21        0a    1   21  SA:A   0  BSAS  7200 847555/1735794176 847884/1736466816
    

So we have 3 raid groups setup as *raid-dp*. More information on *RAID-DP* from the same guide:

> **How Data ONTAP RAID groups work**  
> A RAID group consists of one or more data disks or array LUNs, across which client data is striped and stored, and up to two parity disks, depending on the RAID level of the aggregate that contains the RAID group.
> 
> *   RAID-DP uses two parity disks to ensure data recoverability even if two disks within the RAID group fail.
> *   RAID4 uses one parity disk to ensure data recoverability if one disk within the RAID group fails.
> *   RAID0 does not use any parity disks; it does not provide data recoverability if any disks within the RAID group fail. 

RAID-DP is an equivilant of a regular RAID 6 but with special NetApp functionality.

### ONTAP Volumes

So now let&#8217;s go ahead and create a volume from the above aggregate. Now there are also different volumes, from the &#8220;Storage Management Guide&#8221;:

> **How FlexVol volumes work**  
> A FlexVol volume is a volume that is loosely coupled to its containing aggregate. A FlexVol volume can share its containing aggregate with other FlexVol volumes. Thus, a single aggregate can be the shared source of all the storage used by all the FlexVol volumes contained by that aggregate. Because a FlexVol volume is managed separately from the aggregate, you can create small FlexVol volumes (20 MB or larger), and you can increase or decrease the size of FlexVol volumes in increments as small as 4 KB.
> 
> When a FlexVol volume is created, it reserves a small amount of extra space (approximately 0.5 percent of its nominal size) from the free space of its containing aggregate. This space is used to store the volume&#8217;s metadata. Therefore, upon creation, a FlexVol volume with a space guarantee of volume uses free space from the aggregate equal to its size × 1.005. A newly-created FlexVol volume with a space guarantee of none or file uses free space equal to .005 × its nominal

And also from the same document:

> **How traditional volumes work**  
> A traditional volume is a volume that is contained by a single, dedicated, aggregate. It is tightly coupled with its containing aggregate. No other volumes can get their storage from this containing aggregate. The only way to increase the size of a traditional volume is to add entire disks to its containing aggregate.
> 
> You cannot decrease the size of a traditional volume. The smallest possible traditional volume uses all the space on two disks (for RAID4) or three disks (for RAID-DP). Traditional volumes and their containing aggregates are always of type 32-bit. You cannot grow a traditional volume larger than 16 TB.
> 
> You cannot use SSDs to create a traditional volume.

The FlexVol volume definitely sounds like it&#8217;s the way to go&#8230; it seems more flexible ;). I wanted to create a 500GB Flexible volume, and then carve out a 100GB LUN from that volume. Checking what volumes we currently have:

    p1-3240cl1-2> vol status
             Volume State           Status            Options
               vol0 online          raid_dp, flex     root, create_ucode=on
    

That is just the root volume, since this is inside &#8216;aggr0&#8242;:

    p1-3240cl1-2> vol container vol0
    Volume 'vol0' is contained in aggregate 'aggr0'
    

## Creating a Volume on NetAPP

Now to create my FlexVol Volume:

    p1-3240cl1-2> vol create karim_vol aggr1 500g
    Creation of volume 'karim_vol' with size 500g on containing aggregate
    'aggr1' has completed.
    p1-3240cl1-2> vol status
             Volume State           Status            Options
               vol0 online          raid_dp, flex     root, create_ucode=on
          karim_vol online          raid_dp, flex     create_ucode=on
    

That looks good. Checking out the size of the volume:

    p1-3240cl1-2> vol size karim_vol
    vol size: Flexible volume 'karim_vol' has size 500g.
    p1-3240cl1-2> df -h
    Filesystem               total       used      avail capacity  Mounted on
    /vol/vol0/               537GB     5376MB      532GB       1%  /vol/vol0/
    /vol/vol0/.snapshot      134GB      334MB      133GB       0%  /vol/vol0/.snapshot
    /vol/karim_vol/          400GB      176KB      399GB       0%  /vol/karim_vol/
    /vol/karim_vol/.snapshot      100GB        0TB      100GB       0%  /vol/karim_vol/.snapshot
    

It looks like the volume is 500GB and 100GB is used for snapshots.

## Creating a LUN From a FlexVol Volume on NetAPP

Now to create a 100GB LUN inside my volume:

    p1-3240cl1-2> lun create -s 100g -t vmware /vol/karim_vol/my_lun
    p1-3240cl1-2> lun show -v
            /vol/karim_vol/my_lun        100g (107374182400)  (r/w, online)
                    Serial#: dn//FJnoB7oU
                    Share: none
                    Space Reservation: enabled
                    Multiprotocol Type: vmware
                    Occupied Size:       0 (0)
                    Creation Time: Sat Nov 24 14:51:47 EST 2012
                    Cluster Shared Volume Information: 0x0
    

## Creating an iGroup on NetAPP

Now we need to create an *igroup* (initiator group) and map the LUN to it. This will contain a list of WWNs allowed to connect to this LUN. First let&#8217;s check the Array HBAs:

    p1-3240cl1-2> fcp show adapter
    Slot:                    2a
    Description:             Fibre Channel Target Adapter 2a (Dual-channel, QLogic CNA 8112 (8152) rev. 2)
    Adapter Type:            Local
    Status:                  OFFLINE
    FC Nodename:             50:0a:09:80:8d:11:cf:94 (500a09808d11cf94)
    FC Portname:             50:0a:09:81:8d:11:cf:94 (500a09818d11cf94)
    Standby:                 No
    
    Slot:                    2b
    Description:             Fibre Channel Target Adapter 2b (Dual-channel, QLogic CNA 8112 (8152) rev. 2)
    Adapter Type:            Local
    Status:                  OFFLINE
    FC Nodename:             50:0a:09:80:8d:11:cf:94 (500a09808d11cf94)
    FC Portname:             50:0a:09:82:8d:11:cf:94 (500a09828d11cf94)
    Standby:                 No
    
    Slot:                    0c
    Description:             Fibre Channel Target Adapter 0c (Dual-channel, QLogic 2432 (2462) rev. 2)
    Adapter Type:            Local
    Status:                  ONLINE
    FC Nodename:             50:0a:09:80:8d:11:cf:94 (500a09808d11cf94)
    FC Portname:             50:0a:09:83:8d:11:cf:94 (500a09838d11cf94)
    Standby:                 No
    
    Slot:                    0d
    Description:             Fibre Channel Target Adapter 0d (Dual-channel, QLogic 2432 (2462) rev. 2)
    Adapter Type:            Local
    Status:                  ONLINE
    FC Nodename:             50:0a:09:80:8d:11:cf:94 (500a09808d11cf94)
    FC Portname:             50:0a:09:84:8d:11:cf:94 (500a09848d11cf94)
    Standby:                 No
    

Looks like the bottom two are actually online, while the top two are down. So we will be connecting to 50:0a:09:80:8d:11:cf:94 and 50:0a:09:80:8d:11:cf:94. Now checking over the host now, we see the following LUNs:

    ~ # esxcfg-scsidevs -c
    Device UID                            Device Type      Console Device                                            Size      Multipath PluginDisplay Name
    naa.600508e000000000fb1078bd19366d0c  Direct-Access    /vmfs/devices/disks/naa.600508e000000000fb1078bd19366d0c  69618MB   NMP     LSILOGIC Serial Attached SCSI Disk (naa.600508e000000000fb1078bd19366d0c)
    

Just the local disk. Now checking out the paths, I saw the following:

    ~ # esxcfg-mpath -b
    naa.600508e000000000fb1078bd19366d0c : LSILOGIC Serial Attached SCSI Disk (naa.600508e000000000fb1078bd19366d0c)
       vmhba0:C1:T0:L0 LUN:0 state:active sas Adapter: 50022bdd8c104000  Target: c6d3619bd7810fb
    

Nothing special, just the local disk. Now we know the Host WWNs are the following: 20:00:00:25:B5:0A:00:46 and 20:00:00:25:B5:0B:00:46. So let&#8217;s add those WWNs to an igroup:

    p1-3240cl1-2> igroup create -f -t vmware esx_hosts 20:00:00:25:b5:0a:00:46 20:00:00:25:b5:0b:00:46
    p1-3240cl1-2> igroup show
        esx_hosts (FCP) (ostype: vmware):
            20:00:00:25:b5:0a:00:46 (not logged in)
            20:00:00:25:b5:0b:00:46 (not logged in)
    

## Mapping a LUN to iGroup on NetAPP

Now let&#8217;s map our LUN to this igroup:

    p1-3240cl1-2> lun map /vol/karim_vol/my_lun esx_hosts
    Sat Nov 24 15:15:29 EST [p1-3240cl1-2: lun.map:info]: LUN /vol/karim_vol/my_lun was mapped to initiator group esx_hosts=0
    p1-3240cl1-2>  24 15:15:29 EST [p1-3240cl1-2: lun.map:info]: LUN /vol/karim_vol/my_lun was mapped to initiator group esx_hosts=0
    

Checking to make sure it&#8217;s mapped:

    p1-3240cl1-2> lun show -m
    LUN path                            Mapped to          LUN ID  Protocol
    -----------------------------------------------------------------------
    /vol/karim_vol/my_lun               esx_hosts               0       FCP
    

## Confirming LUN Access from ESX(i) to a NetAPP FCP LUN

That looks good. I did a rescan on the hosts:

    ~ # esxcfg-rescan -A
    Rescanning all adapters..
    

And then I saw this on the filer in the logs:

    Sat Nov 24 15:32:05 EST [p1-3240cl1-2: scsitarget.ispfct.portLogin:notice]: FCP login on Fibre Channel adapter '0c' from '20:00:00:25:b5:0a:00:46', address 0x80051.
    Sat Nov 24 15:32:09 EST [p1-3240cl1-2: scsitarget.ispfct.portLogin:notice]: FCP login on Fibre Channel adapter '0d' from '20:00:00:25:b5:0b:00:46', address 0x6a0039.
    

Then checking out the igroups, I saw the following:

    p1-3240cl1-2> igroup show
     esx_hosts (FCP) (ostype: vmware):
         20:00:00:25:b5:0a:00:46 (logged in on: vtic, 0c)
         20:00:00:25:b5:0b:00:46 (logged in on: vtic, 0d)
    

Obviously the SAN switch had proper zoning setup, but I was not part of that setup, since I didn&#8217;t have access to them. Now checking out the setting on the host:

    ~ # esxcfg-scsidevs -c
    Device UID                            Device Type      Console Device                                            Size      Multipath PluginDisplay Name
    naa.600508e000000000fb1078bd19366d0c  Direct-Access    /vmfs/devices/disks/naa.600508e000000000fb1078bd19366d0c  69618MB   NMP     LSILOGIC Serial Attached SCSI Disk (naa.600508e000000000fb1078bd19366d0c)
    naa.60a980006467435a673469554f385770  Direct-Access    /vmfs/devices/disks/naa.60a980006467435a673469554f385770  1048576MB   NMP     NETAPP Fibre Channel Disk (naa.60a980006467435a673469554f385770)
    

Checking out the paths for that LUN, I saw the following:

    ~ # esxcfg-mpath -b -d naa.60a980006467435a673469554f385770
    naa.60a980006467435a673469554f385770 : NETAPP Fibre Channel Disk (naa.60a980006467435a673469554f385770)
       vmhba2:C0:T2:L0 LUN:0 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:46 WWPN: 20:00:00:25:b5:0b:00:46 Target: WWNN: 50:0a:09:80:8d:11:cf:94  WWPN: 50:0a:09:83:8d:11:cf:94   
       vmhba1:C0:T0:L0 LUN:0 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:46 WWPN: 20:00:00:25:b5:0a:00:46 Target: WWNN:50:0a:09:80:8d:11:cf:94 WWPN: 50:0a:09:84:8d:11:cf:94
    

After that, you can put VMFS on that LUN or present it as an RDM to a VM.

<root> </root>

