---
title: ZFS iSCSI Benchmark Tests on ESX
author: Karim Elatov
layout: post
permalink: /2014/01/zfs-iscsi-benchmarks-tests/
categories: ['os', 'networking', 'storage', 'vmware', 'zfs']
tags: ['comstar', 'disk_max_io_size', 'opensolaris', 'performance', 'iscsi', 'omnios']
---

Let me just start out by saying that my setup is not perfect, I would actually call it bad. All I have is a 1 1TB SATA disk and 4GB of RAM. There is no redundancy in the setup or a dedicated SSD for ZIL. It's just a regular machine that I had laying around and I wanted to see how OpenSolaris with Comstar would turn out.

### The Hardware

As I mentioned, this is just a regular machine without any PCI controller cards with regular SATA disks. The machine has a dual core CPU:

    root@zfs:~# psrinfo -pv
    The physical processor has 2 virtual processors (0-1)
      x86 (GenuineIntel 6F2 family 6 model 15 step 2 clock 2133 MHz)
            Intel(r) Core(tm)2 CPU          6400  @ 2.13GHz


It is capable of handling 64 bit:

    root@zfs:~# isainfo -bv
    64-bit amd64 applications
            vmx ssse3 cx16 sse3 sse2 sse fxsr mmx cmov amd_sysc cx8 tsc fpu


It has 4GB of RAM:

    root@zfs:~# prtconf | grep Memory
    Memory size: 4094 Megabytes


And here is the information about the SATA disk:

    root@zfs:~# cfgadm -al -s "select=type(disk),cols=ap_id:info" sata1/1::dsk/c2t1d0
    Ap_Id                          Information
    sata1/1::dsk/c2t1d0            Mod: ST1000DM003-1CH162 FRev: CC47 SN: S1DEJVQ5


And lastly here is the S.M.A.R.T information regarding the disk:

    root@zfs:~# smartctl -i -d sat /dev/rdsk/c2t1d0
    smartctl 6.2 2013-07-26 r3841 [i386-pc-solaris2.11] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

    === START OF INFORMATION SECTION ===
    Model Family:     Seagate Barracuda 7200.14 (AF)
    Device Model:     ST1000DM003-1CH162
    Serial Number:    S1DEJVQ5
    LU WWN Device Id: 5 000c50 06c885059
    Firmware Version: CC47
    User Capacity:    1,000,204,886,016 bytes [1.00 TB]
    Sector Sizes:     512 bytes logical, 4096 bytes physical
    Rotation Rate:    7200 rpm
    Device is:        In smartctl database [for details use: -P show]
    ATA Version is:   ACS-2, ACS-3 T13/2161-D revision 3b
    SATA Version is:  SATA 3.1, 6.0 Gb/s (current: 3.0 Gb/s)
    Local Time is:    Sun Dec 22 10:39:36 2013 MST


Nothing crazy or expensive.

## Local Write Benchmarks

Before we present an iSCSI LUN to our ESXi host let's see what speeds we get locally. I actually installed **napp-it** on my **omnios** install (if you need help with that, check out [Jarret's post here](http://virtuallyhyper.com/2013/04/installing-and-configuring-omnios/)). In the *napp-it* web-gui there are a bunch of available tests:


![napp it benchmarks g ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/napp-it-benchmarks_g.png)

Doing a quick **DD** test yielded the following:

![napp it dd test ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/napp-it-dd-test.png)

I was actually impressed. Checking out the [data sheet](http://www.seagate.com/www-content/product-content/barracuda-fam/desktop-hdd/barracuda-7200-14/en-gb/docs/desktop-hdd-data-sheet-ds1770-1-1212gb.pdf) of the hardrive, I saw the following:

![hd specs ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/hd-specs.png)

The **Avg Data** rate is **156MB/s**, the **Max Data** rate is **210 MB/s** and I got **177MB/s**. This was a regular DD test, I am sure if I did a **bonnie++** I would get closer to the **210MB/s** mark. But I wanted a realistic test, with FileSystem Cache and OS limitations involved. Doing the same test from the command line, I saw the following:

    root@zfs:~# dd if=/dev/zero of=/data/dd.tst bs=1M count=5K
    5120+0 records in
    5120+0 records out
    5368709120 bytes (5.4 GB) copied, 25.7934 s, 208 MB/s


And checking out the IO stats as the above test was going, I saw the following:

    root@zfs:~# iostat -xM sd1 1
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       9.9 1474.2    0.1  172.2  8.3  0.8    6.2  88  83
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       0.0 1699.9    0.0  210.9  9.0  1.0    5.8 100  98
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       2.0 1501.4    0.1  173.9  7.8  0.9    5.8  90  88
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       0.0 1686.9    0.0  209.3  9.0  1.0    5.9 100  98


The **iostat** columns are described in the **man** page quite well:

    wait
               average number of transactions waiting for service
               (queue length)

               This is the number of I/O operations held  in  the
               device  driver queue waiting for acceptance by the
               device.

     actv
               average number of transactions actively being ser-
               viced  (removed  from  the  queue but not yet com-
               pleted)

               This is the number of I/O operations accepted, but
               not yet serviced, by the device.
    svc_t
               average response time  of  transactions,  in  mil-
               liseconds

               The svc_t  output  reports  the  overall  response
               time,  rather  than the service time, of a device.
               The overall time includes the time  that  transac-
               tions  are in queue and the time that transactions
               are being serviced.  The time spent  in  queue  is
               shown  with  the  -x  option  in the wsvc_t output
               column. The time spent servicing  transactions  is
               the true service time.  Service time is also shown
               with the -x option and appears in the asvc_t  out-
               put column of the same report.

     %w
               percent of time there are transactions waiting for
               service (queue non-empty)

     %b
               percent of time the disk is busy (transactions  in
               progress)


We can see that the device was definitely pushed to the max: the percent busy (**%b**) was almost 100% and same for the percent wait (**%w**). But the service time (**svc_t**) was still really good, below *6.5 ms* and below the **avg seek time** as mentioned in the data sheet above. Just for fun I ran the **iozone 1gb** test and here is what I saw:

![iozon test ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/iozon-test.png)

The sequential write was about the same speed **175MB/s**. A **bonnie++** test, yielded slightly higher speeds:

![bonnie test ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/bonnie_test.png)

### Network Benchmark

At home I had a 1GB un-managed switch and I wanted to see if a Linux machine on the same switch could get close to that speed when bench-marking against the *onmnios* server. Since *omnios* was just a regular machine, I only had one NIC:

    root@zfs:~# dladm show-phys
    LINK         MEDIA                STATE      SPEED  DUPLEX    DEVICE
    e1000g0      Ethernet             up         1000   full      e1000g0


The setup is getting less perfect as we keep going :). The **iperf** binary comes with the **napp-it** install, so let's test it out. On the zfs machine I started the server and then connected from the local Linux machine as the **iperf** client. Here were the results:

    root@zfs:~# /var/web-gui/data/tools/iperf/iperf -s -w 2m
    ------------------------------------------------------------
    Server listening on TCP port 5001
    TCP window size:  125 KByte (WARNING: requested 2.00 MByte)
    ------------------------------------------------------------
    [  4] local 192.168.1.101 port 5001 connected with 192.168.1.107 port 40146
    [ ID] Interval       Transfer     Bandwidth
    [  4]  0.0-10.0 sec  1.09 GBytes   933 Mbits/sec


Not too shabby.

Next I wanted to try a similar test between the **omnios** machine and the **ESXi** machine. Back in the day I compiled a static **netperf** binary on a **CentOS 4.8** Linux distribution and it actually worked on an ESXi host (another person did a similar compile with **ipmitool** as described [here](http://johnsofteng.wordpress.com/2013/09/17/make-ipmitool-working-for-esxi-5-1/)). So first I followed the instructions laid out in [this](https://blogs.oracle.com/observatory/entry/netperf) blog on how to compile **netperf** for solaris. After I compiled **netperf-2.4.5**, I started the server on the *omnios* machine:

    root@zfs:~# netserver
    Starting netserver at port 12865
    Starting netserver at hostname 0.0.0.0 port 12865 and family AF_UNSPEC


Then I copied the old binary to the ESXi machine and it still worked out :) Here are my results:

    ~ # /tmp/netperf -H zfs
    TCP STREAM TEST to zfs
    Recv   Send    Send
    Socket Socket  Message  Elapsed
    Size   Size    Size     Time     Throughput
    bytes  bytes   bytes    secs.    10^6bits/sec

    128000  32768  32768    10.00     935.09


Similar results, I was pushing close the full 1GB through the switch.

### ESXi Network iSCSI setup

I had two NICs on the ESXi server, so I dedicated 1 Nic to the VM and Mgmt traffic, and the other NIC to the iSCSI connection. I probably didn't have to do this since the iSCSI network was already separate from the other networks, but I went ahead and bound the **vmk** that I used for the iSCSI connection to the physical NIC that was assigned to the vSwitch:

    ~ # esxcli iscsi networkportal list
    vmhba32
       Adapter: vmhba32
       Vmknic: vmk1


## iSCSI Benchmark

Using **napp-it** I went ahead and presented a LUN using Comstar, the process was pretty easy:

1.  create volume (under the **Disks** section)
2.  create a volume LU (under the **Comstar** section)
3.  create a Target
4.  create a Target Group with Target as member
5.  create a view ( To allow LU to be accessed by the TG we created above, and by host group if you have one)

After a **rescan** on the ESXi host, the LUN was present:

    ~ # esxcli storage core adapter rescan -A vmhba32
    ~ # esxcfg-scsidevs -c | grep SUN
    naa.600144f0876a9c47000052b744210009  Direct-Access    /vmfs/devices/disks/naa.600144f0876a9c47000052b744210009  10240MB   NMP     SUN iSCSI Disk (naa.600144f0876a9c47000052b744210009)


Here is a little more information about the device:

    ~ # esxcli storage core device list -d naa.600144f0876a9c47000052b744210009
    naa.600144f0876a9c47000052b744210009
       Display Name: SUN iSCSI Disk (naa.600144f0876a9c47000052b744210009)
       Has Settable Display Name: true
       Size: 10240
       Device Type: Direct-Access
       Multipath Plugin: NMP
       Devfs Path: /vmfs/devices/disks/naa.600144f0876a9c47000052b744210009
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
       Thin Provisioning Status: yes
       Attached Filters:
       VAAI Status: unknown
       Other UIDs: vml.0200000000600144f0876a9c47000052b744210009434f4d535441


I went ahead and put VMFS on it and then I did a quick **dd** test from the ESXi test. I know it's not a valid test, but I wanted to see even an estimate:

    ~ # time dd if=/dev/zero of=/vmfs/volumes/test/dd.tst bs=1M count=2K
    2048+0 records in
    2048+0 records out
    real    10m 12.82s
    user    0m 4.26s
    sys 0m 0.00s


As the above test was running I ran **esxtop** and here is what I saw:

![dd first try g ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/dd-first-try_g.png)

That didn't look good at all. I also checked out **iostat** on the *omnios* machine and I saw the following:

    root@zfs:~# iostat -xM sd1 1
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       2.0  266.0    0.1   12.6  0.4  0.1    1.9  34  10
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       0.0  242.8    0.0   17.8  1.0  0.1    4.6  95  12
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       0.0  176.2    0.0    6.9  0.7  0.1    4.1  62   6
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1       0.0  281.0    0.0   10.8  0.1  0.1    0.6   5   8


That is really slow, but it's not like the *omnios* machine was over loaded or anything.

### iSCSI ZFS with WriteBack Cache

So then I checked out the LUN and I saw that **write-back cache** was not enabled. Per [this](http://kb.vmware.com/kb/1006602) VMware KB, it's recommended to enable that. So inside *napp-it*, I went ahead and enabled that:

![enable write cache ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/enable-write-cache.png)

After I enabled that I went ahead and did another **dd** test:

    ~ # time dd if=/dev/zero of=/vmfs/volumes/test/dd.tst bs=1M count=3K
    3072+0 records in
    3072+0 records out
    real    0m 40.40s
    user    0m 5.92s
    sys 0m 0.00s


Also checked out **esxtop** and saw the following:

![davg after wirte cache enabled ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/davg-after-wirte-cache-enabled.png)

That is way better, now I am writing at **~80MB/s**.

### IOmeter Tests with iSCSI

I then installed a windows VM and installed **IOmeter** on it. I then added a **VMDK** to the VM that resided on my test LUN. After that I followed the instructions laid out in [this](http://kb.vmware.com/kb/2019131) VMware KB to do some performance testing. The KB provides a predefined set of *IOmeter* tests; they are mostly **4K-32K**, Read and Write tests. The output of *IOmeter* is in CSV format and you can use *Excel* to check out the results. There is also a pretty [cool perl](http://pvenezia.com/iw/iometer-parse-html.pl) script which grabs a couple of columns and generates an HTML file of those columns. I modified the script to grab latency stats as well. I also modified the *IOmeter* results to only include sequential tests (excluded the random tests). Here is the result of my initial test:

![iometer results reg test1 ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/iometer-results-reg-test1.png)

That is actually pretty good, I am getting about **105-111 MB/s** for small IO sizes between **4K** and **32K**. We can see that the latency looks good as well **1-9ms**. And of course as the block size increases so does the latency :) I decided to do a test with larger IO. I modified the test to include **128K-1M** sequential read and writes. Here were the results:

![iometer big tests1 ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/iometer-big-tests1.png)

The results are really impressive but so is the latency. Our bandwidth is **107-178MB/s** but our latency varies from **24ms** to **408ms**

### Performance from a Linux VM

At this point I wanted to see how the iSCSI LUN would fair against a Linux VM. After I added the *VMDK* to the VM, I saw the disk inside the OS:

    $dmesg -T | tail -4
    [Sun Dec 22 14:34:03 2013]  sdb: unknown partition table
    [Sun Dec 22 14:34:03 2013] sd 3:0:0:0: [sdb] Cache data unavailable
    [Sun Dec 22 14:34:03 2013] sd 3:0:0:0: [sdb] Assuming drive cache: write through
    [Sun Dec 22 14:34:03 2013] sd 3:0:0:0: [sdb] Attached SCSI disk


Then doing a **dd** test just to the disk, I saw the following:

    ~# dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 54.911 s, 58.7 MB/s


At the same time checking out **esxtop** here is what I saw:

![linux vm dd g ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/linux_vm_dd_g.png)

That wasn't so good. As I ran the **dd** test, I also ran an **iostat** within the VM and here is what I saw:

    $iostat -xm sdb 1
    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 10403.19    0.00   87.23     0.00    43.62  1024.00   151.91 1320.93    0.00 1320.93  12.20 106.38

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               1.03    0.00    6.19   92.78    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 16758.76    0.00  174.23     0.00    87.11  1024.00   144.03 1378.67    0.00 1378.67   5.92 103.09

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    3.23   96.77    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 18025.81    0.00   92.47     0.00    46.24  1024.00   150.16  849.49    0.00  849.49  11.63 107.53

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               1.05    0.00    2.11   96.84    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 12833.68    0.00  105.26     0.00    52.63  1024.00   155.04 1462.88    0.00 1462.88  10.00 105.26


We can also see the latency is pretty high with the OS. We can also see that the **avgrq-sz** and **avgqu-sz** which are defined from the **man** page as such:

    avgrq-sz
           The average size (in sectors) of the requests that were issued to the device.

    avgqu-sz
           The average queue length of the requests that were issued to the device.


Are pretty high, the **avg request size** is 1024 sectors (512KB) and the **avg queue length** is ~150. Actually all the **iostat** columns are described [here](http://www.pythian.com/blog/basic-io-monitoring-on-linux/):

*   **r/s** and **w/s**— respectively, the number of read and write requests issued by processes to the OS for a device.
*   **rsec/s** and **wsec/s** — sectors read/written (each sector 512 bytes).
*   **rkB/s** and **wkB/s** — kilobytes read/written.
*   **avgrq-sz** — average sectors per request (for both reads and writes). Do the math — *(rsec + wsec) / (r + w) = (134.13+178.84)/(10.18+9.78)=15.6798597*
    *   If you want it in kilobytes, divide by 2.
    *   If you want it separate for reads and writes — do you own math using rkB/s and wkB/s.
*   **avgqu-sz** — average queue length for this device.
*   **await** — average response time (ms) of IO requests to a device. The name is a bit confusing as this is the total response time including wait time in the requests queue (let call it qutim), and service time that device was working servicing the requests (see next column — svctim).So the formula is *await = qutim + svctim*.
*   **svctim** — average time (ms) a device was servicing requests. This is a component of total response time of IO requests.
*   **%util** — this is a pretty confusing value. The man page defines it as, Percentage of CPU time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to 100%. A bit difficult to digest. Perhaps it’s better to think of it as percentage of time the device was servicing requests as opposed to being idle. To understand it better here is the formula:
    *   *utilization = ( (read requests + write requests) * service time in ms / 1000 ms ) * 100%*
    *   *%util = ( r + w ) * svctim /10 = ( 10.18 + 9.78 ) * 8.88 = 17.72448*

From the above output we can see that **avg wait time** is pretty high (**~1000ms**). So we are sending a lot of large IO to the device (**512kb**) and a lot of simultaneous requests (**~128**), the device is taking a while to process this IO and therefore the **avg wait time** is high.

### Lower IO Size and Request Numbers in Linux VM

The IO size and the queue length are controlled by these two **sysfs** variables:

    $cat /sys/block/sdb/queue/max_sectors_kb
    512
    $cat /sys/block/sdb/queue/nr_requests
    128


From the [sysfs](https://www.kernel.org/doc/Documentation/block/queue-sysfs.txt) documentation:

    max_sectors_kb (RW)
    -------------------
    This is the maximum number of kilobytes that the block layer will allow
    for a filesystem request. Must be smaller than or equal to the maximum
    size allowed by the hardware.
    ...
    ...
    nr_requests (RW)
    ----------------
    This controls how many requests may be allocated in the block layer for
    read or write requests. Note that the total allocated number may be twice
    this amount, since it applies only to reads or writes (not the accumulated
    sum).


So let's go ahead and change the IO size to **32KB** and see if that helps out at all:

    # echo 32 > /sys/block/sdb/queue/max_sectors_kb


Now running the **dd** command again:

    # dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 56.1516 s, 57.4 MB/s


The speed was the same, but when I checked out **esxtop**, I saw **DAVG** go down:

![linux vm dd 32bit max sec g ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/linux_vm_dd_32bit_max_sec_g.png)

Checking out **iostat** from within the VM I saw the following:

    $ iostat -xm sdb 1
    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 12957.45    0.00 1855.32     0.00    57.98    64.00   156.00   81.42    0.00   81.42   0.57 106.38

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    2.20   97.80    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 12369.23    0.00 1780.22     0.00    55.63    64.00   157.79   95.12    0.00   95.12   0.62 109.89

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    3.26   96.74    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 14091.30    0.00 2006.52     0.00    62.70    64.00   159.10   76.70    0.00   76.70   0.54 108.70


We can see that the **avrtq-sz** changed to **64** (32kb), which is good and we now see that the **avg wait time** went down to **~80ms** (from **~1000ms**). Lowering the number of requests to **4**:

    # echo 4 > /sys/block/sdb/queue/nr_requests


lowered the **DAVG** to practically nothing, but the speed wasn't that great. Here is the **dd** test:

    ~# dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 64.5064 s, 49.9 MB/s


and here is **iostat**:

    $iostat -xm sdb 1
    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 10666.67    0.00 1519.79     0.00    47.46    63.96     9.49    3.53    0.00    3.53   0.69 104.17

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.00    0.00    2.08   97.92    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 13234.38    0.00 1893.75     0.00    59.13    63.94    12.18    5.73    0.00    5.73   0.55 104.17

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               2.06    0.00    2.06   95.88    0.00    0.00

    Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sdb               0.00 10716.49    0.00 1531.96     0.00    47.87    64.00    12.12    3.88    0.00    3.88   0.67 103.09


We can see that the **wait** time is now **~4ms**.

### Change Zpool Block Size

When I created the zfs volume, I set the block size to **128KB**:

    root@zfs:~# zfs get volblocksize data/test
    NAME          PROPERTY      VALUE     SOURCE
    data/test     volblocksize  128K      -


After reading a couple of sites:

![zfs block sizes ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/zfs-block-sizes.png)

![zfs ds examples ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/zfs-ds-examples.png)

[FreeNAS 9.10 on VMware ESXi 6.0 Guide](https://b3n.org/freenas-9-3-on-vmware-esxi-6-0-guide/)

*   I use 64K block-size based on some benchmarks I’ve done comparing 16K (the default), 64K, and 128K.  64K blocks didn’t really hurt random I/O but helped some on sequential performance, and also gives a better compression ratio.  128K blocks had the best better compression ratio but random I/O started to suffer so I think 64K is a good middle-ground.  Various workloads will probably benefit from different block sizes.

[Set I/O block size](http://myqtest.blogspot.com/2009/08/set-io-block-size.html)

*   You must also consider I/O block size before creating a ZFS store this is not something that can be changed later so now is the time. It’s done by adding the –b 64K to the ZFS create command. I chose to use 64k for the block size which aligns with VMWare default allocation size thus optimizing performance.

It seems that the default value of 64K is better. I also ran into this forum: [Block alignment and sizing in ZFS volumes for iSCSI to vSphere 5](http://zfs.illumos.narkive.com/BNfldguT/block-alignment-and-sizing-in-zfs-volumes-for-iscsi-to-vsphere-5). From that forum:

> Latest best practice documents suggest 8k block size with iscsi. At least the ones I know with latest VMware file systems in vsphere5.
>
> This is ok for ZFS backends, but anything up to 32k for iSCSI should work fine. In a ZFS system the balance is between metadata and data: small data block size means more metadata is needed. In general 4K is too small, 8-16-32 are generally ok.

I tried setting it on the fly, but it failed:

    root@zfs:~# zfs set volblocksize=32K data/testing
    cannot set property for 'data/testing': 'volblocksize' is readonly


So I deleted the volume and re-created it. I tested with both 64KB and 32KB, for me **32KB** worked out a little better. Here are a couple of **dd** tests (these were without any changes to the Linux OS):

    # dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 34.476 s, 93.4 MB/s


this was for **64KB** and here is the **32KB** one:

    # dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 31.1633 s, 103 MB/s


The **DAVG** was pretty high for both (**~70ms**). Modifying the **max_sectors_kb** and **nr_requests** to **32** and **4** respectively , yielded very low latency but the bandwidth was lower as well:

    # dd if=/dev/zero of=/dev/sdb bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 47.1101 s, 68.4 MB/s


Still better than 128KB ZVol Block size. If you don't mind a little latency then leave the default values for **max_sectors_kb** and **nr_requests** sysfs variables.

### Linux VM File System performance tweaks

After I put a file system on the disk and tried the same **dd** test, I saw the following:

    # dd if=/dev/zero of=/mnt/test/dd.tst bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 31.1195 s, 104 MB/s


Looking over [this](http://blog.nkadesign.com/2010/admin-linux-file-server-performance-boost-ext4-version/) site, I decided to try out some mount options:

    # mount /dev/sdb1 /mnt/test -o noatime,data=writeback


That yielded very little increase:

    # dd if=/dev/zero of=/mnt/test/dd.tst bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 29.8348 s, 108 MB/s


The above options helped out my Fedora box more than my Debian VM.

### Other Tweaks

Throughout my testing I did a couple of things. I would say the below had minimal if no impact on the performance:

1.  Install VMware tools
2.  From [VMware KB 1017652](http://kb.vmware.com/kb/1017652) use the **pvscsi** virtual adapter
3.  From [Linux 2.6 kernel-based virtual machines experience slow disk I/O performance](http://kb.vmware.com/kb/2011861) set the I/O Scheduler to **noop** (`echo noop > /sys/block/sdb/queue/scheduler`).
4.  Per [this](http://kb.vmware.com/kb/1003469) HP KB, change the **MaxIOSize** option in VMware (`esxcli system settings advanced set -o /Disk/DiskMaxIOSize -i 128`)
5.  Modify the following ZFS settings on the ZFS Volume, taken from [this](http://www.serverfocus.org/zfs-evil-tuning-guide) blog.
    1.  Turn off the **checksum** (`zfs set checksum=off data/test`)
    2.  Change **Primary Cache** (`zfs set primarycache=metadata data/test`)
6.  Disable **sync** (there is a discussion [here](http://forums.freenas.org/threads/data-integritry-nfs-vs-iscsi-on-zfs-with-vmware.12241/)), it seems that it mostly applies to NFS, but I decided to give it a try just to see if it helps out(`zfs set sync=disabled data/test`)

### Summary

In summary, I think the following settings made the biggest impact:

1.  Enable Write Back Cache
2.  Use 64KB or 32KB block size on the ZFS Volume
3.  If latency is important to you, change the IO size from within the Linux OS (**max_sectors_kb** and **nr_requests**)

In the end here was my final dd result from my Linux VM:

    # dd if=/dev/zero of=/mnt/test/dd.tst bs=1M count=3K
    3072+0 records in
    3072+0 records out
    3221225472 bytes (3.2 GB) copied, 27.5574 s, 117 MB/s


And checking out my NIC Utilization during the above test:

![nic usage ZFS iSCSI Benchmark Tests on ESX](https://github.com/elatov/uploads/raw/master/2013/12/nic-usage.png)

Almost the full pipe :) Lastly here is how the *omnios* **iostat** looked like:

    root@zfs:~# iostat -xM sd1 1
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1      41.0  881.1    0.2  103.4  4.4  0.9    5.8  98  93
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1      24.0  811.1    0.1  100.1  5.6  0.8    7.6  98  75
                     extended device statistics
    device    r/s    w/s   Mr/s   Mw/s wait actv  svc_t  %w  %b
    sd1      25.0  868.7    0.1  102.2  3.0  1.0    4.5  99  98


Good enough for me.

