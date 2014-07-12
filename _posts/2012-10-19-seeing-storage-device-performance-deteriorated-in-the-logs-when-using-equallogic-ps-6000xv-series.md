---
title: "Seeing 'Storage Device Performance Deteriorated' in the Logs When Using Equallogic PS 6000XV Series"
author: Karim Elatov
layout: post
permalink: /2012/10/seeing-storage-device-performance-deteriorated-in-the-logs-when-using-equallogic-ps-6000xv-series/
categories: ['storage', 'vmware']
tags: ['disk_max_io_size', 'equallogic','iometer', 'performance','iscsi']
---

A customer was seeing 'Storage Device Performance Deteriorated" message in the logs during their backup operation. More information regarding this message can be seen in VMware KB [Configuring VMware vSphere Software iSCSI With Dell EqualLogic PS Series Storage](http://kb.vmware.com/kb/2007236)". Here are a few things that stood out from the document:

> the iSCSI switch environment can be on a different subnet than the public environment or existing service console. Each VMkernel Port will need its own IP Address and they must all be on the same subnet and be on the same subnet as the PS Series Group IP Address.
>
> ...
> ...
>
> In a default configuration assign one VMkernel port for each physical NIC in the system. So if there are 3 NICs, assign 3 VMkernel Ports. This is referred to in the VMware iSCSI document as 1:1 port binding.
>
> ...
> ...
>
> One of the new advanced features that is enabled by configuring the iSCSI Software Initiator the way we have is that now we can take advantage of MPIO by using Round Robin. This combined with the fan out intelligent design of the PS Series group allows for greater and better bandwidth utilization than in previous versions of ESX. I wanted to ensure the iSCSI network was separated from the rest of the network, and it was:

    ~ # esxcfg-vmknic -l
    Interface Port Group IP Address Netmask Broadcast MAC Address MTU
    vmk0 Management Network 10.60.3.217 255.255.252.0 10.60.3.255 84:2b:2b:6d:e9:98 1500
    vmk1 iSCSI1 10.10.3.56 255.255.255.0 10.10.3.255 00:50:56:77:bc:e6 9000
    vmk2 iSCSI2 10.10.3.57 255.255.255.0 10.10.3.255 00:50:56:71:54:08 9000
    vmk3 vMotion 10.11.3.2 255.255.255.0 10.11.3.255 00:50:56:74:8d:ed 1500
    vmk4 iSCSI-heartbeat 10.10.3.55 255.255.255.0 10.10.3.255 00:50:56:73:eb:84 9000


That looked good. Then I wanted to make sure we have a 1:1 port binding and we did:

    ~ # esxcli iscsi networkportal list
    vmhba36:
    Adapter: vmhba36
    Vmknic: vmk1
    MAC Address: 00:1b:21:8e:fb:35
    MAC Address Valid: true
    IPv4: 10.10.3.56
    IPv4 Subnet Mask: 255.255.255.0
    IPv6:
    MTU: 9000
    Vlan Supported: true
    Vlan ID: 0
    Reserved Ports: 63488~65536
    TOE: false
    TSO: true
    TCP Checksum: false
    Link Up: true
    Current Speed: 1000
    Rx Packets: 349438739
    Tx Packets: 374175073
    NIC Driver: igb
    NIC Driver Version: 2.1.11.1
    NIC Firmware Version: 1.5-1
    Compliant Status: compliant
    NonCompliant Message:
    NonCompliant Remedy:
    Vswitch: vSwitch1
    PortGroup: iSCSI1
    VswitchUuid:
    PortGroupKey:
    PortKey:
    Duplex:
    Path Status: active

    vmhba36:
    Adapter: vmhba36
    Vmknic: vmk2
    MAC Address: 00:1b:21:8e:fe:2d
    MAC Address Valid: true
    IPv4: 10.10.3.57
    IPv4 Subnet Mask: 255.255.255.0
    IPv6:
    MTU: 9000
    Vlan Supported: true
    Vlan ID: 0
    Reserved Ports: 63488~65536
    TOE: false
    TSO: true
    TCP Checksum: false
    Link Up: true
    Current Speed: 1000
    Rx Packets: 2234995
    Tx Packets: 52
    NIC Driver: igb
    NIC Driver Version: 2.1.11.1
    NIC Firmware Version: 1.5-1
    Compliant Status: compliant
    NonCompliant Message:
    NonCompliant Remedy:
    Vswitch: vSwitch1
    PortGroup: iSCSI2
    VswitchUuid:
    PortGroupKey:
    PortKey:
    Duplex:
    Path Status: active


and here is how the vSwitch looked like:

    Switch Name Num Ports Used Ports Configured Ports MTU Uplinks
    vSwitch1 128 6 128 9000 vmnic11,vmnic7

    PortGroup Name VLAN ID Used Ports Uplinks
    iSCSI-heartbeat 0 1 vmnic11,vmnic7
    iSCSI2 0 1 vmnic11
    iSCSI1 0 1 vmnic7


So **vmk1** was bound to **vmnic7** and **vmk2** was bound to **vmnic11**. Lastly we just needed to make sure the Target was on the same subnet:

    ~ # vmkiscsi-tool -T -l vmhba36 | grep Portal
    Portal 0 : 10.10.3.4:3260


And it was. The customer was also using the Round Robin Pathing Policy for this LUN:

    ~ # esxcli storage nmp device list
    naa.6090a048007daca3efe4f47da571ad50:
    Device Display Name: EQLOGIC iSCSI Disk (naa.6090a048007daca3efe4f47da571ad50)
    Storage Array Type: VMW_SATP_EQL
    Storage Array Type Device Config: SATP VMW_SATP_EQL does not support device configuration.
    Path Selection Policy: VMW_PSP_RR
    Path Selection Policy Device Config: {policy=rr,iops=1000,bytes=10485760,useANO=0;lastPathIndex=1: NumIOsPending=0,numBytesPending=0}
    Path Selection Policy Device Custom Config:
    Working Paths: vmhba36:C1:T0:L0, vmhba36:C0:T0:L0


So the configuration looked good. I then decided to figure out if a certain load was causing the latency. Following the instructions laid out in VMware KB [2019131](http://kb.vmware.com/kb/2019131) we ran IOmeter and here were the results:

{:.kt}
| Test         | Read_IOPs | Read_MB | Write_IOPs | Write_MB | Read_Lat | Write_Lat |
| ------------ |:---------:|:-------:|:----------:|:--------:|:--------:| ---------:|
| 4K_100%Read  |  12,898   |   50    |            |          |   2.48   |           |
| 4K_50%Read   |   6,738   |   26    |   6,738    |    26    |   1.84   |      2.89 |
| 4K_0%Read    |           |         |   8,108    |    31    |          |       3.9 |
| 16K_100%Read |   5,359   |   84    |            |          |   5.94   |           |
| 16K_50%Read  |   2,220   |   34    |   2,212    |    34    |   7.43   |      6.99 |
| 16K_0%Read   |           |         |   2,305    |    36    |          |        13 |
| 32K_100%Read |   2,987   |   93    |            |          |    10    |           |
| 32K_50%Read  |   1,184   |   37    |   1,180    |    36    |    23    |        12 |
| 32K_0%Read   |           |         |   1,351    |    42    |          |        23 |

I read over the article ' [EqualLogic PS Series Usability and Performance](http://www.dell.com/us/business/p/equallogic-ps-series)'. They had multiple test cases, I was mostly interested in this on:

> For test case #2, we wanted to measure the sustained throughput IOPS over a longer period of time. Therefore, we created a 100GB volume, left it unformatted, and ran IOMeter with the settings identified in Table 2. In addition, we ran the Windows Performance Monitor utility to measure the Physical Disk Transfers/sec (see Graph 1) over the course of 60 minutes, taking a sampling every 10 seconds. What we observed was a very consistently sustained IOPS throughput rate over the entire test period, with an average IOPS of 12043.

The above test was done with 8K, we didn't exactly match it but we were pretty close. So I didn't see a performance issue with anything lower than **32K** block size. I then ran **IOmeter** manually with random block sizes and then realized that any IO greater than **64K** would cause pretty high latency. The customer mentioned that doing a local copy from the same disk also causes high latency. I fired up **perfmon** as the windows copy was going and here is what I saw:

![windows_copy_with_180Kbs](https://github.com/elatov/uploads/raw/master/2012/07/windows_copy_with_180Kbs.png)

The windows copy had random spikes of different block sizes and sometimes went all the way to 180KB as seen in the above picture. I then came across an interesting Dell Article entitled "[EqualLogic Snapshots and Clones: Best Practices and Sizing Guidelines](http://en.community.dell.com/dell-groups/dtcmedia/m/mediagallery/20097871/download.aspx)". Some interesting things that came out of that paper:

> While performing backups using Windows Server Backup, it was observed that the average block size on reads and writes was 128K. This is similar to many other backup applications which typically read and write data in block sizes ranging from 64K to 256K.
>
> ...
> ...
>
> The base volumes were mounted on one Windows host, and the snapshot volumes on the other. A workload was simultaneously run against the base volumes while running the backup workload on the snapshot volumes to simulate an application. The test started with two volumes and then incremented the volumes and associated snapshots by two until there were 12 total volumes and the latency approached 20 ms. The IOmeter workloads used to simulate the backup application and application workload are shown in the following table.
>
> {:.kt}
> | Workload type | # workers |  I/O type  | Read/Write  mix | Block Size |  Volume  | Volume Access |
> | ---------|:----------:|:----------:|:------------------:|:----------:|:--------:| -------------:|
> | Backup            |     1      | sequential |       100/0        |    128K    | Snapshot |       100.00% |
> | Application       |     8      |   random   |       67/33        |     8K     |   Base   |        10.00% |
>
> ...
> ...
>
> As shown in Figure 12, when increasing the number of volumes, and therefore the workload against both sets of volumes, the latency of the base (source) volume increased as expected. The workload was actively modifying portions of the base volume after the snapshot was created and therefore consuming snapshot reserve. However, because snapshots share data with the base volume, portions of the data were being accessed by both workloads.
>
> Using snapshot volumes as the source for backups may affect the performance of the source volumes. In this case, the latency increased with the application simulation workload and the number of volumes being backed up (i.e., running the backup simulation workload). IOPS continued to scale, indicating the I/O processing abilities of the storage system had not yet been reached. However, had the increase to both workloads continued, eventually a point would be reached where the system would no longer deliver more IOPS and the latency would sharply increase.

There was a community forum on Dell's site "[Equallogic - W2K8 latency with IO larger than 64KB](http://en.community.dell.com/techcenter/storage/f/4466/t/19454019.aspx)" and it seemed like a very similar issue. Here were some suggestions from that article:

> 1.  Delayed ACK DISABLED
> 2.  Large Receive Offload DISABLED
> 3.   Make sure they are using either VMware Round Robin (with IOs per path changed to 3), or preferably MEM 1.1.0.
> 4.   If they have multiple VMDKs (or RDMs) in their VM, each of them (up to 4) needs its own Virtual SCSI adapter.
> 5.  Update to latest build of ESX, to get latest NIC drivers.

We implemented the above suggestions, but they didn't help out. We then engaged Dell and they ran the '[Dell Performance Analysis Collection Kit](http://i.dell.com/sites/content/shared-content/campaigns/en/Documents/dpack-brochure.pdf)' (DPACK). Here were some of the results for the whole array. It breaks it down per host (non-VMware as well). Here was the result from a Win2k Server:

![dpack_win2k_host](https://github.com/elatov/uploads/raw/master/2012/07/dpack_win2k_host.png)

And here is the same thing from a Win2k3 host:

![dpack_win2k3](https://github.com/elatov/uploads/raw/master/2012/07/dpack_win2k3.png)

And here is one from a Win2k8 machine:

![dpack_win2k8r2](https://github.com/elatov/uploads/raw/master/2012/07/dpack_win2k8r2.png)

And lastly here is the one from the ESXi 5.0 host:

![dpack_esxi5](https://github.com/elatov/uploads/raw/master/2012/10/dpack_esxi5.png)

We can see that the higher the block size the higher the latency and the Windows 2K8 R2 machine also had high latency. I then decided to change the **DiskMaxIOSize** per VMware KB [1003469](http://kb.vmware.com/kb/1003469). That stopped the message from happening as often but it still happened once in a while.

In conclusion, we learned that Win2k8 has very high block size (during regular windows copy operations) and the Dell Equallogic doesn't like high block because it incurs high latency. The latency was seen during backups and backups are expected to have high block size so the issue that we were experiencing was expected. With above changes we decreased the frequency of the message but it was still happening at night (during backups) which was expected. Lastly check out this VMware blog "[Large I/O block size operations show high latency on Windows 2008](http://blogs.vmware.com/kb/2012/10/large-io-block-size-operations-show-high-latency-on-windows-2008.html)"where it talks about Win2k8 Guest OSes cause such high latency and it's a false positive.

