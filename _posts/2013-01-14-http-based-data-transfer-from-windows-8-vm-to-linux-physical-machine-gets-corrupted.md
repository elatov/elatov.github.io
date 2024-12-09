---
title: HTTP Based Data Transfers from Windows 8 VM to Linux Physical Machine are Corrupted
author: Karim Elatov
layout: post
permalink: /2013/01/http-based-data-transfer-from-windows-8-vm-to-linux-physical-machine-gets-corrupted/
categories: ['networking', 'os', 'vmware']
tags: ['performance', 'win8', 'md5sum', 'netsh', 'tso', 'wireshark']
---

We have an application running on a Windows 8 virtual machine which provides a file using HTTP when requested. When accessed from a Linux physical machine, the file is often slightly corrupted. To check the data integrity, I ran the following prior to the download and then after. Here is the md5sum prior to any downloads:

    [elatov@klaptop ~]$ md5sum test
    25e317773f308e446cc84c503a6d1f85 test


After I uploaded the file to the Windows server and then back to my Linux host, I would see the following:

    [elatov@klaptop ~]$ md5sum test
    456d810e2396f34e0cb1024ebf2b88dc test


I grabbed a Wireshark capture on my VM during the transfer process and saw the following:

![SRC Win VM HTTP Based Data Transfers from Windows 8 VM to Linux Physical Machine are Corrupted](https://github.com/elatov/uploads/raw/master/2012/12/SRC_Win_VM.png)

The size of the packet is 8266 bytes and jumbo frames are not setup. If TSO or LRO is enabled then packet sizes in Wireshark are not accurate. From [this](http://wiki.wireshark.org/CaptureSetup/Offloading) wireshark page:

> Some cards can reassemble traffic. This will manifest itself in Wireshark as packets that are larger than expected, such as a 2900-byte packet on a network with a 1500-byte MTU. You can check and change offloading behavior on Linux and Windows using the methods described in the previous section.

I then ran into [this](https://support.microsoft.com/en-us/help/947239/description-of-the-receive-window-auto-tuning-feature-for-http-traffic) Windows article. Here is a snippet from the article:

> When the Receive Window Auto-Tuning feature is enabled for HTTP traffic, older routers, older firewalls, and older operating systems that are incompatible with the Receive Window Auto-Tuning feature may sometimes cause slow data transfer or a loss of connectivity. When this occurs, users may experience slow performance. Or, the applications may crash. These older devices do not comply with the RFC 1323 standard

I then ran into VMware KB [1009517](https://knowledge.broadcom.com/external/article?legacyId=1009517), from that KB:

> When using the VMXNET3 driver and Windows Server 2008 R2, you may experience these symptoms:
>
> *   Poor performance
> *   Packet loss
> *   Network latency
> *   Slow data transfer
>
> The issue may be caused by Windows TCP Stack offloading the usage of the network interface to the CPU. However, since the NIC is not a direct physical NIC, it seems to have issues addressing a vCPU and vNIC. To resolve this issue, disable the TCP Checksum Offload feature, as well as the RSS. Open the command prompt as administrator and run these commands:
>
>     netsh int tcp set global RSS=disabled
>     netsh int tcp set global chimney=disabled
>     netsh int tcp set global autotuninglevel=disabled
>     netsh int tcp set global congestionprovider=None
>     netsh int tcp set global ecncapability=disabled
>     netsh int ip set global taskoffload=disabled
>     netsh int tcp set global timestamps=disabled
>
>
> **Note:** If you do not notice an improvement, you can re-enable the features by re-running the commands, replacing Disabled with Enabled.

After doing some testing it looks like running the following command:

    netsh int tcp set global autotuninglevel=disabled


Stopped the packet corruption. Here is how the default (prior to any changes) configuration looked like on my Windows VM:

    C:\Users\Administrator>netsh int tcp show global
    Querying active state...

    TCP Global Parameters
    ----------------------------------------------
    Receive-Side Scaling State          : enabled
    Chimney Offload State               : automatic
    NetDMA State                        : enabled
    Direct Cache Acess (DCA)            : disabled
    Receive Window Auto-Tuning Level    : normal
    Add-On Congestion Control Provider  : ctcp
    ECN Capability                      : disabled
    RFC 1323 Timestamps                 : disabled


