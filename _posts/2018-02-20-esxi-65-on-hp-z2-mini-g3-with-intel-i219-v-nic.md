---
published: true
layout: post
title: "ESXi 6.5 on HP Z2 Mini G3 with Intel I219-V NIC"
author: Karim Elatov
categories: [vmware,networking]
tags: [ne1000,e1000e]
---
### ESXi 6.5 On HP Z2 Mini G3
I ended up installing ESXi 6.5 on the HP Z2 Mini G3 and it actually worked out without any major issues:

	[root@hp:~] esxcli hardware platform get
	Platform Information
	   UUID: 0x24 0x98
	   Product Name: HP Z2 Mini G3 Workstation
	   Vendor Name: HP

Here is what I saw from the web vSphere client:

![vsphere-hp-info.png](https://raw.githubusercontent.com/elatov/upload/master/hp-z2-esxi/vsphere-hp-info.png)

This guy had **i7-6700 CPUs** and 32GB of RAM:

	[root@hp:~] esxcli hardware cpu list | tail -20
	CPU:7
	   Id: 7
	   Package Id: 0
	   Family: 6
	   Model: 94
	   Type: 0
	   Stepping: 3
	   Brand: GenuineIntel
	   Core Speed: 3407999975
	   Bus Speed: 23999998
	   APIC ID: 0x7
	   Node: 0
	   L2 Cache Size: 262144
	   L2 Cache Associativity: 4
	   L2 Cache Line Size: 64
	   L2 Cache CPU Count: 2
	   L3 Cache Size: 8388608
	   L3 Cache Associativity: 16
	   L3 Cache Line Size: 64
	   L3 Cache CPU Count: 2

and here is the RAM information:

	[root@hp:~] esxcli hardware memory get
	   Physical Memory: 34133794816 Bytes
	   Reliable Memory: 0 Bytes
	   NUMA Node Count: 1

### USB 3 Ethernet Adapter
I did end up getting a USB 3 Ethernet Adapter and following the instructions laid out in [USB 3.0 Ethernet Adapter (NIC) driver for ESXi 6.5](http://www.virtuallyghetto.com/2016/11/usb-3-0-ethernet-adapter-nic-driver-for-esxi-6-5.html) to get it working. I ended getting a **Realtek** Based USB adapter but it still worked out with out issues. Here is the information about the device:

	[root@hp:~] lsusb -v -s 002:002

	Bus 002 Device 002: ID 0bda:8153 Realtek Semiconductor Corp. RTL8153 Gigabit Ethernet Adapter
	Device Descriptor:
	  bLength                18
	  bDescriptorType         1
	  bcdUSB               3.00
	  bDeviceClass            0 (Defined at Interface level)
	  bDeviceSubClass         0
	  bDeviceProtocol         0
	  bMaxPacketSize0         9
	  idVendor           0x0bda Realtek Semiconductor Corp.
	  idProduct          0x8153 RTL8153 Gigabit Ethernet Adapter
	  bcdDevice           30.00
	  iManufacturer           1 Realtek
	  iProduct                2 USB 10/100/1000 LAN
	  iSerial                 6 41C9A7000000

[USB Ethernet driver for ESXi 6.5](http://www.devtty.uk/homelab/USB-Ethernet-driver-for-ESXi-6.5/) has the driver for that. Here is what I ran to get that working:

	[root@hp:~] esxcli software vib install -v /vmfs/volumes/datastore1/drivers/r8152-2.06.0-4_esxi65.vib
	[root@hp:~] esxcli system module set -m=vmkusb -e=FALSE

Then after a reboot here is the NIC:

	[root@hp:~] esxcli network nic list
	Name     PCI Device    Driver  Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
	-------  ------------  ------  ------------  -----------  -----  ------  -----------------  ----  ------------------------------------------------
	vmnic0   0000:00:1f.6  ne1000  Up            Up            1000  Full    70:5a:0f:XX:XX:XX  1500  Intel Corporation Ethernet Connection (2) I219-V
	vmnic32  Pseudo        r8152   Up            Up            1000  Full    3c:18:a0:XX:XX:XX  9000  Unknown Unknown

### Intel I219-V NIC Issues
This NIC is on the Vmware HCL([Intel Ethernet Connection (2) I219-LM](https://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=39796&deviceCategory=io&details=1&VID=8086&DID=15b7&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc)).Initially I ran into issues where the NIC would just randomly hang and I would see this message:

	2017-02-22T16:25:09.994Z cpu2:65908)INFO (ne1000): false RX hang detected on vmnic0

I ran into [Strange Ethernet error that I can't find any info on](https://communities.vmware.com/thread/556755) vmware community post and running the following would stop using the default **ne1000** driver and would default to the **e1000e** driver:

	esxcli system module set --enabled=false --module=ne1000

After a reboot I saw the following driver utilized:

	[root@hp:~] ethtool -i vmnic0
	driver: e1000e
	version: 3.2.2.1-NAPI
	firmware-version: 0.8-4
	bus-info: 0000:00:1f.6

This worked out great and fixed the initial issue. But then I ran into another issue, whenever I would update my router and reboot it then the **e1000e** driver would hang with the following error:

	2017-09-30T17:26:50.881Z cpu1:65936)WARNING: LinNet: netdev_watchdog:3688: NETDEV WATCHDOG: vmnic0: transmit timed out
	2017-09-30T17:26:50.881Z cpu1:65936)WARNING: at vmkdrivers/src_92/vmklinux_92/vmware/linux_net.c:3717/netdev_watchdog() (inside vmklinux)
	2017-09-30T17:26:50.881Z cpu1:65936)Backtrace for current CPU #1, worldID=65936, fp=0x430410ce87c0
	2017-09-30T17:26:50.881Z cpu1:65936)0x4390cc81be50:[0x418020d03f71]vmk_LogBacktraceMessage@vmkernel#nover+0x29 stack: 0x430410ce2ac8, 0x4180214838ad, 0xe68, 0x430410ce87c0, 0x43900000101f
	2017-09-30T17:26:50.881Z cpu1:65936)0x4390cc81be70:[0x4180214838ad]watchdog_work_cb@com.vmware.driverAPI#9.2+0x27d stack: 0x43900000101f, 0x4180215b7268, 0x41802148385a, 0x4390cc81bef0, 0xc0000000
	2017-09-30T17:26:50.881Z cpu1:65936)0x4390cc81bed0:[0x4180214a4e28]vmklnx_workqueue_callout@com.vmware.driverAPI#9.2+0xe0 stack: 0x430410d01100, 0x417fc4e0c5c0, 0x8000000000001014, 0x418021483630, 0x4180214a4e1d
	2017-09-30T17:26:50.881Z cpu1:65936)0x4390cc81bf50:[0x418020cc93ee]helpFunc@vmkernel#nover+0x4b6 stack: 0x43007206e050, 0x0, 0x0, 0x0, 0x1014
	2017-09-30T17:26:50.881Z cpu1:65936)0x4390cc81bfe0:[0x418020ec8c95]CpuSched_StartWorld@vmkernel#nover+0x99 stack: 0x0, 0x0, 0x0, 0x0, 0x0
	2017-09-30T17:26:50.881Z cpu1:65936)<3>e1000e 0000:00:1f.6: vmnic0: Reset adapter unexpectedly
	2017-09-30T17:27:29.238Z cpu4:65938)<6>vmnic0 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: Rx/Tx
	2017-09-30T17:27:30.509Z cpu1:65597)NetPort: 1879: disabled port 0x2000002
	2017-09-30T17:27:30.509Z cpu6:817863)NetSched: 628: vmnic0-0-tx: worldID = 817863 exits
	2017-09-30T17:27:30.509Z cpu1:65597)Uplink: 9893: enabled port 0x2000002 with mac 70:5a:0f:XX:XX:XX
	2017-09-30T17:27:30.510Z cpu7:65579)CpuSched: 692: user latency of 817875 vmnic0-0-tx 0 changed by 65579 HELPER_MISC_QUEUE-1-2 -6
	2017-09-30T17:27:31.239Z cpu5:65931)<6>e1000e 0000:00:1f.6: vmnic0: Hardware hanged on TSO context. Reset it.
	2017-09-30T17:27:31.239Z cpu5:65931)<3>e1000e 0000:00:1f.6: vmnic0: Detected Hardware Unit Hang:
	  TDH                  <0>
	  TDT                  <46>
	  next_to_use          <46>
	  next_to_clean        <0>
	buffer_info[next_to_clean]:
	  time_stamp      $

Then I ran into [KB 2149915](https://kb.vmware.com/kb/2149915) and it had the following:

> This patch updates the ne1000 VIB to resolve the following issues:
>
> When TSO capability is enabled in NE1000 driver, I218 NIC reset frequently in heavy traffic scenario, because of I218 h/w issue. The NE1000 TSO capability for I218 NIC should be disabled.

So I decided to update to ESXi 6.5 U1

### Updating from ESXi 6.5GA to 6.5U1

There are actually pretty good instructions at [How to easily update your VMware Hypervisor from 6.5.x to 6.5 Update 1 (ESXi 6.5 U1)](https://tinkertry.com/easy-upgrade-to-esxi-65u1). Since I had the Realtek custom **VIB** installed, it had to be removed and re-installed after the update. Here are the commands I ran to update the Host:

	# Prepare for the update
	vmware-autostart.sh stop
	# Put into maintenance mode
	esxcli system maintenanceMode set -e true
	# Open up Firewall
	esxcli network firewall ruleset set -e true -r httpClient
	# Install the update (this will remove the custom usb3 driver)
	esxcli software profile install -p ESXi-6.5.0-20170702001-standard -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml --ok-to-remove
	# Re-enable firewall
	esxcli network firewall ruleset set -e false -r httpClient
	# Reboot and usb will be missing
	esxcli system shutdown reboot -r esxi65u1
	# Reinstall the realtek vib
	esxcli software vib install -v /vmfs/volumes/datastore1/drivers/r8152-2.06.0-4_esxi65.vib

Everything was working as before.

### Re-enable ne1000 Driver
So lastly I re-enabled the **ne1000** driver:

	# esxcli system module set --enabled=true --module=ne1000

Then after the reboot I saw the following:

	[root@hp:~] esxcli network nic get -n vmnic0
	   Advertised Auto Negotiation: true
	   Advertised Link Modes: Auto, 10BaseT/Half, 10BaseT/Full, 100BaseT/Half, 100BaseT/Full, 1000BaseT/Full
	   Auto Negotiation: false
	   Cable Type: Twisted Pair
	   Current Message Level: -1
	   Driver Info:
	         Bus Info: 0000:00:1f:6
	         Driver: ne1000
	         Firmware Version: 0.8-4
	         Version: 0.8.0
	   Link Detected: true
	   Link Status: Up
	   Name: vmnic0
	   PHYAddress: 0
	   Pause Autonegotiate: false
	   Pause RX: false
	   Pause TX: false
	   Supported Ports: TP
	   Supports Auto Negotiation: true
	   Supports Pause: false
	   Supports Wakeon: true
	   Transceiver:
	   Virtual Address: 00:50:56:52:c3:e5
	   Wakeon: MagicPacket(tm)

And I confirmed that TSO was disabled:

	[root@hp:~] esxcli network nic tso get
	NIC      Value
	-------  -----
	vmnic0   off
	vmnic32  off

I will keep an eye to see if that's better than the **e1000e** driver. I tried one more reboot of the router and the NIC didn't panic, I just saw this in the logs:

	[root@hp:~] dmesg | tail
	2017-10-03T19:08:22.790Z cpu0:65721)VSCSI: 2891: handle 8203(vscsi0:0):Reset [Retries: 0/0] from (vmm0:gen)
	2017-10-03T19:08:22.890Z cpu0:65721)VSCSI: 2679: handle 8203(vscsi0:0):Completing reset (0 outstanding commands)
	2017-10-06T02:15:43.889Z cpu4:68736)DEBUG (ne1000): checking link for adapter vmnic0
	2017-10-06T02:15:46.891Z cpu1:65954)DEBUG (ne1000): vmnic0: retry to wait for link up
	2017-10-06T02:15:46.892Z cpu1:65954)INFO (ne1000): vmnic0: Link is Up
	2017-10-06T02:15:46.892Z cpu1:65954)DEBUG (ne1000): link status unchanged: skip reporting.
	2017-10-06T02:17:23.823Z cpu3:68901)DEBUG (ne1000): checking link for adapter vmnic0
	2017-10-06T02:17:26.824Z cpu1:65954)DEBUG (ne1000): vmnic0: retry to wait for link up
	2017-10-06T02:17:26.825Z cpu1:65954)INFO (ne1000): vmnic0: Link is Up
	2017-10-06T02:17:26.825Z cpu1:65954)DEBUG (ne1000): link status unchanged: skip reporting.

And it was able to recover.
