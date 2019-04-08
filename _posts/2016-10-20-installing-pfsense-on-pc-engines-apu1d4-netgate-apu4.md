---
published: true
layout: post
title: "Installing pfSense on PC Engines APU 1D4 / Netgate APU4"
author: Karim Elatov
categories: [security,networking]
tags: [freebsd,pfsense,serial]
---
I got a hold of a pretty unique device, it's system board that is designed for a simple router. Check out some sites that talk about the system board:

* [Netgate APU4](http://store.netgate.com/APU4.aspx)
* [apu1d4 System board](http://www.pcengines.ch/apu1d4.htm)

You can even buy a DIY kit: [APU1D4 DIY Kit](http://store.netgate.com/kit-APU1C4.aspx). On top of the Kit I ended up getting an SD card: [Transcend 16GB SDHC Class 10 UHS-1 Flash Memory Card](http://www.amazon.com/Transcend-Class-UHS-1-Memory-TS16GSDHC10U1E/dp/B006LFVKES)

Here is the device when it's all ready:

![apu-upside-down](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/apu-upside-down-s.png&raw=1)

### Support for APU 1D4

I ran into a couple of sites that talked about the device. It looks like **OpenWrt** has some support but it doesn't look finished: [OpenWrt PC Engines APU](https://wiki.openwrt.org/toh/pcengines/apu). I also saw that the **BSD Router Project** had luck with the device: [BSD Router Project PC Engines APU](http://bsdrp.net/documentation/examples/pc_engines_apu). And lastly I ran into a couple of sites that installed **pfSense** on the device:

* [pc engine – pfsense as router / firewall](http://sigtar.com/2015/02/26/pc-engine-pfsense-as-router-firewall/)
* [Build an awesome APU based pfSense Router](https://mathew.id.au/build-an-awesome-apu-based-pfsense-router/)

So I decided to try out **pfSense**.

### Prepare Serial Communication Client

I was lucky and I had an old machine with a serial port. First we can find the device name for the serial port:

	[elatov@localhost ~]$ dmesg | grep -E 'tty|Serial\:'
	[    0.000000] console [tty0] enabled
	[    0.573747] Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
	[    0.594288] 00:04: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A

We can also confirm with the **setserial** command (in my case my serial port is **/dev/ttsS0**):

	[elatov@localhost ~]$ setserial -g /dev/ttyS0
	/dev/ttyS0, UART: 16550A, Port: 0x03f8, IRQ: 4

Next we can configure **minicom** to connnect to our serial port:

	sudo minicom -s
	
We can go to **Serial port setup**:

![serial-port-setup](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/serial-port-setup.png&raw=1)

And configure the options to be:

* Serial Device: **/dev/ttyS0**
* Bps/Par/Bits: **115200 8N1**
* Hardware Flow Control: **No**

![minicom-settings](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-settings.png&raw=1)

Then we can just **Save setup as dfl**, and it will create the config under **/etc/minirc.dfl**. Lastly add yourself to the **dialout** group so you can run **minicom** without **sudo**:

	sudo usermod -a -G dialout elatov
	
### Prepare the pfSense Install USB Drive

I went to the site and chose the following options:

* Computer Archicture: **AMD64 (64bit)**
* Platform: **Memstick image with Installer**
* Console: **Serial**

![pfsen-down.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/pfsen-down.png&raw=1)

After that we can go and extract the image:

	gunzip -d pfSense-CE-memstick-serial-2.3-RELEASE-amd64.img.gz

Before we overwrite our USB drive, let's back it up:
	
	┌─[elatov@gen] - [/home/elatov] - [2016-04-30 01:29:35]
	└─[1] <> sudo dd if=/dev/sdb of=/data/backup/usb-backup.dd bs=1M
	967+0 records in
	967+0 records out
	1013972992 bytes (1.0 GB) copied, 1027.84 s, 987 kB/s

After we are done with the **pfSense** install, I can just copy that image back onto the USB stick. Now let's copy the **pfSense** image to the usb drive:

	┌─[elatov@gen] - [/home/elatov/downloads] - [2016-04-30 01:47:05]
	└─[0] <> sudo dd if=pfSense-CE-memstick-serial-2.3-RELEASE-amd64.img of=/dev/sdb bs=1M
	654+1 records in
	654+1 records out
	685867008 bytes (686 MB) copied, 768.911 s, 892 kB/s

After it's done, the drive looked like this:

	┌─[elatov@gen] - [/home/elatov] - [2016-04-30 06:49:15]
	└─[0] <> sudo fdisk -l /dev/sdb
	Disk /dev/sdb: 967 MiB, 1013972992 bytes, 1980416 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0x90909090
	
	Device     Boot Start   End Sectors  Size Id Type
	/dev/sdb4  *        0 49999   50000 24.4M a5 FreeBSD

### Install pfSense on APU 1D4

I plugged the device into my Serial Port and started up **minicom** (I also saved all the output just in case):

	minicom -C install.txt

After powering on the device I saw the following:

	PC Engines APU BIOS build date: Apr  5 2014
	Reading data from file [bootorder]
	SeaBIOS (version ?-20140405_120742-frink)
	SeaBIOS (version ?-20140405_120742-frink)
	Found coreboot cbmem console @ df150400
	Found mainboard PC Engines APU
	Relocating init from 0x000e8e71 to 0xdf1065e0 (size 39259)
	Found CBFS header at 0xfffffb90
	found file "bootorder" in cbmem
	CPU Mhz=1001
	Found 27 PCI devices (max PCI bus is 05)
	Copying PIR from 0xdf160400 to 0x000f27a0
	Copying MPTABLE from 0xdf161400/df161410 to 0x000f25b0 with length 1ec
	Copying ACPI RSDP from 0xdf162400 to 0x000f2590
	Copying SMBIOS entry point from 0xdf16d800 to 0x000f2570
	Using pmtimer, ioport 0x808
	Scan for VGA option rom
	EHCI init on dev 00:12.2 (regs=0xf7f08420)
	Found 1 lpt ports
	Found 2 serial ports
	AHCI controller at 11.0, iobase f7f08000, irq 11
	EHCI init on dev 00:13.2 (regs=0xf7f08520)
	EHCI init on dev 00:16.2 (regs=0xf7f08620)
	Searching bootorder for: /rom@img/setup

And here is how the **minicom** looked like:

![minicom-apu-botting-up](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-apu-botting-up.png&raw=1)

I hit **F12** and it showed me the boot menu:

![minicom-boot-menu-apu](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-boot-menu-apu.png&raw=1)

I chose the second option, it booted from the usb stick, and here is what I saw:

![minicom-pfsense-usb-boot.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pfsense-usb-boot.png&raw=1)

I left the default option and it started booting into the installer. I also chose the **easy install** and here is the progress of the install:

![minicom-pf-einstall-p1](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pf-einstall-p1.png&raw=1)

![minicom-pf-einstall-p2](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pf-einstall-p2.png&raw=1)

![minicom-pf-einstall-p3](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pf-einstall-p3.png&raw=1)

After the reboot, I removed the USB stick and it started booting from the SD Card:

![minicom-pfsense-reg-boot](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pfsense-reg-boot.png&raw=1)

And after it was done booting up I saw the **pfSense** Menu:

![minicom-pfsense-booted-up](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pfsense-booted-up.png&raw=1)

To leave the **minicom** program you can type in **Ctrl+A X**

### Post Install Setup

After it booted up I reassigned my interface accordingly:

* re0: WAN (connected to the Modem)
* re1: OPT1 (connected to the regular network)
* re2: LAN (connected to my **dd-wrt** router)

![minicom-pfsense-inter-assign](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pfsense-inter-assign.png&raw=1)

And I also changed the LAN network since my **dd-wrt** router already uses that subnet:

![minicom-pfsense-change-lan-net](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/minicom-pfsense-change-lan-net.png&raw=1)

Then I plugged my laptop into **re2** and I was able to get an address and also get to the admin page:

![pfsense-admin-page](https://seacloud.cc/d/480b5e8fcd/files/?p=/apu-pfsense-install/pfsense-admin-page.png&raw=1)

Here is a list of things I ended up configuring before I placed it in front of my router:

1. Disable beeps: **System** > **Advanced** -> **Notifications** -> **Disable the startup/shutdown beep**
	* [Disable Sounds/Beeps](https://doc.pfsense.org/index.php/Disable_Sounds/Beeps)
2. IP the OPT1 Interface (so it has an IP on the internal network): **Interfaces** -> **OPT1**
3. Enable Port Forwards: **Firewall** -> **NAT** -> **Port Forward**
4. Add another GW (so I can reach my internal network): **System** -> **Routing** -> **Gateways**
5. Add a Static Route (To use the above gateway): **System** -> **Routing** -> **Static Routes**
6. Static DHCP Lease (For the **dd-wrt** router): **Services** -> **DHCP Server** -> **LAN** -> **DHCP Static Mappings for this Interface**
7. Send Logs to Remote Syslog: **Status** -> **System Logs** -> **Settings** -> **Enable Remote Logging** (use **OPT1** interface)
8. Add an SSH Key for Root User: **System** -> **User Manager** -> **Edit Admin** -> **Authorized SSH Keys**
9. Enable SSH: **System** -> **Advanced** -> **Admin Access** -> **Secure Shell Server**

### Checking out the pfSense System

When you login via ssh you will see the **pfSense** menu and you can choose option **8** to get a shell:

	┌─[elatov@macair] - [/Users/elatov] - [2016-05-01 11:54:57]
	└─[0] <> ssh root@pf
	*** Welcome to pfSense 2.3-RELEASE-pfSense (amd64) on pf ***
	
	 WAN (wan)       -> re0        -> v4/DHCP4: X.X.X.X/21
	 LAN (lan)       -> re2        -> v4: 192.168.56.1/24
	 OPT1 (opt1)     -> re1        -> v4: 192.168.1.99/24
	
	 0) Logout (SSH only)                  9) pfTop
	 1) Assign Interfaces                 10) Filter Logs
	 2) Set interface(s) IP address       11) Restart webConfigurator
	 3) Reset webConfigurator password    12) pfSense Developer Shell
	 4) Reset to factory defaults         13) Update from console
	 5) Reboot system                     14) Disable Secure Shell (sshd)
	 6) Halt system                       15) Restore recent configuration
	 7) Ping host                         16) Restart PHP-FPM
	 8) Shell
	
	
	Enter an option: 8
	
	[2.3-RELEASE][root@pf.kar.int]/root:


#### Disk Information

Checking out **dmesg** we can see that it picked up the device:

	[2.3-RELEASE][root@pf.kar.int]/root: dmesg | grep da0
	da0 at umass-sim0 bus 0 scbus6 target 0 lun 0
	da0: <Multiple Card  Reader 1.00> Removable Direct Access SPC-2 SCSI device
	da0: Serial Number 058F63666485
	da0: 40.000MB/s transfers


We can also check out the partition information:

	[2.3-RELEASE][root@pf.kar.int]/root: gpart show -p
	=>      63  31520705    da0  MBR  (15G)
	        63  31519467  da0s1  freebsd  [active]  (15G)
	  31519530      1238         - free -  (619K)
	
	=>       0  31519467   da0s1  BSD  (15G)
	         0        16          - free -  (8.0K)
	        16  23130843  da0s1a  freebsd-ufs  (11G)
	  23130859   8388608  da0s1b  freebsd-swap  (4.0G)

So we have two partitions the root and the swap, and here are their corresponding labels:

	[2.3-RELEASE][root@pf.kar.int]/root: glabel status
	                  Name  Status  Components
	ufsid/57251d9e1e64953e     N/A  da0s1a
	           label/swap0     N/A  da0s1b

Here is a quick bench mark:

	[2.3-RELEASE][root@pf.kar.int]/root: diskinfo -t /dev/da0s1a
	/dev/da0s1a
		512         	# sectorsize
		11842991616 	# mediasize in bytes (11G)
		23130843    	# mediasize in sectors
		0           	# stripesize
		40448       	# stripeoffset
		1439        	# Cylinders according to firmware.
		255         	# Heads according to firmware.
		63          	# Sectors according to firmware.
		058F63666485	# Disk ident.
	
	Seek times:
		Full stroke:	  250 iter in   0.221129 sec =    0.885 msec
		Half stroke:	  250 iter in   0.221257 sec =    0.885 msec
		Quarter stroke:	  500 iter in   0.455661 sec =    0.911 msec
		Short forward:	  400 iter in   0.320171 sec =    0.800 msec
		Short backward:	  400 iter in   0.319012 sec =    0.798 msec
		Seq outer:	 2048 iter in   0.863436 sec =    0.422 msec
		Seq inner:	 2048 iter in   0.797668 sec =    0.389 msec
	Transfer rates:
		outside:       102400 kbytes in   2.948517 sec =    34729 kbytes/sec
		middle:        102400 kbytes in   3.035525 sec =    33734 kbytes/sec
		inside:        102400 kbytes in   3.016466 sec =    33947 kbytes/sec

We get about 30MB/s which is pretty good:

	[2.3-RELEASE][root@pf.kar.int]/root: dd if=/dev/zero of=1g.dd bs=1M count=100
	100+0 records in
	100+0 records out
	104857600 bytes transferred in 3.317718 secs (31605338 bytes/sec)

Here is the Card Reader information:

	[2.3-RELEASE][root@pf.kar.int]/root: camcontrol devlist
	<Multiple Card  Reader 1.00>       at scbus6 target 0 lun 0 (pass0,da0)
	
	[2.3-RELEASE][root@pf.kar.int]/root: usbconfig list | grep -i flash
	ugen6.2: <Flash Card ReaderWriter Generic> at usbus6, cfg=0 md=HOST spd=HIGH (480Mbps) pwr=ON (100mA)

And more information:

	[2.3-RELEASE][root@pf.kar.int]/root: usbconfig -u 6 -a 2 dump_device_desc
	ugen6.2: <Flash Card ReaderWriter Generic> at usbus6, cfg=0 md=HOST spd=HIGH (480Mbps) pwr=ON (100mA)
	
	  bLength = 0x0012
	  bDescriptorType = 0x0001
	  bcdUSB = 0x0201
	  bDeviceClass = 0x0000  <Probed by interface class>
	  bDeviceSubClass = 0x0000
	  bDeviceProtocol = 0x0000
	  bMaxPacketSize0 = 0x0040
	  idVendor = 0x058f
	  idProduct = 0x6366
	  bcdDevice = 0x0100
	  iManufacturer = 0x0001  <Generic>
	  iProduct = 0x0002  <Flash Card Reader/Writer>
	  iSerialNumber = 0x0003  <058F63666485>
	  bNumConfigurations = 0x0001
  
#### CLOG Logs

Most of the logs on pfSense are in CLOG format and therefore we need to use **clog** to read the logs: [Working with Binary Circular Logs (clog)](https://www.netgate.com/docs/pfsense/monitoring/working-with-binary-circular-logs-clog.html)

So we can do this:

	[2.3-RELEASE][root@pf.kar.int]/root: clog /var/log/filter.log | tail -4
	May  1 12:17:04 pf filterlog: 5,16777216,,1000000103,re0,match,block,in,4,0x20,,49,0,0,DF,17,udp,129,84.26.107.234,X.X.X.X,50321,5475,109
	May  1 12:17:31 pf filterlog: 5,16777216,,1000000103,re0,match,block,in,4,0x20,,108,22353,0,none,17,udp,129,86.110.152.179,X.X.X.X,9654,65350,109
	May  1 12:17:34 pf filterlog: 5,16777216,,1000000103,re0,match,block,in,4,0x20,,44,60752,0,none,1,icmp,114,114.30.173.30,X.X.X.X,unreach,host 192.168.200.102 unreachable94
	May  1 12:17:38 pf filterlog: 5,16777216,,1000000103,re0,match,block,in,4,0x20,,107,10590,0,none,17,udp,131,149.126.31.61,X.X.X.X,26491,65350,111


#### Memory Information
I ended up using an old perl script:

	[2.3-RELEASE][root@pf.kar.int]/root: free
	SYSTEM MEMORY INFORMATION:
	mem_wire:         263172096 (    250MB) [  6%] Wired: disabled for paging out
	mem_active:  +     40529920 (     38MB) [  0%] Active: recently referenced
	mem_inactive:+     75386880 (     71MB) [  1%] Inactive: recently not referenced
	mem_cache:   +            0 (      0MB) [  0%] Cached: almost avail. for allocation
	mem_free:    +   3723980800 (   3551MB) [ 90%] Free: fully available for allocation
	mem_gap_vm:  +            0 (      0MB) [  0%] Memory gap: UNKNOWN
	-------------- ------------ ----------- ------
	mem_all:     =   4103069696 (   3912MB) [100%] Total real memory managed
	mem_gap_sys: +    122908672 (    117MB)        Memory gap: Kernel?!
	-------------- ------------ -----------
	mem_phys:    =   4225978368 (   4030MB)        Total real memory available
	mem_gap_hw:  +     68988928 (     65MB)        Memory gap: Segment Mappings?!
	-------------- ------------ -----------
	mem_hw:      =   4294967296 (   4096MB)        Total real memory installed
	
	SYSTEM MEMORY SUMMARY:
	mem_used:         495599616 (    472MB) [ 11%] Logically used memory
	mem_avail:   +   3799367680 (   3623MB) [ 88%] Logically available memory
	-------------- ------------ ----------- ------
	mem_total:   =   4294967296 (   4096MB) [100%] Logically total memory

But it looks like the memory utilization is pretty small, can't wait to put **suricata** on here and see how it fairs.

#### System Information

Here is a sample **dmidecode** output:

	[2.3-RELEASE][root@pf.kar.int]/root: dmidecode -t system
	# dmidecode 3.0
	Scanning /dev/mem for entry point.
	SMBIOS 2.7 present.
	
	Handle 0x0001, DMI type 1, 27 bytes
	System Information
		Manufacturer: PC Engines
		Product Name: APU
		Version: 1.0
		Serial Number: ddd
		UUID: Not Settable
		Wake-up Type: Reserved
		SKU Number: 4 GB
		Family: None Provided
	
	Handle 0x0004, DMI type 32, 11 bytes
	System Boot Information
		Status: No errors detected

And here is the CPU info:

	[2.3-RELEASE][root@pf.kar.int]/root: dmidecode -t processor
	# dmidecode 3.0
	Scanning /dev/mem for entry point.
	SMBIOS 2.7 present.
	
	Handle 0x0003, DMI type 4, 42 bytes
	Processor Information
		Socket Designation: P0
		Type: Central Processor
		Family: Pentium Pro
		Manufacturer: AuthenticAMD
		ID: 20 0F 50 00 FF FB 8B 17
		Signature: Type 0, Family 20, Model 2, Stepping 0
		Flags:
			FPU (Floating-point unit on-chip)
			VME (Virtual mode extension)
			DE (Debugging extension)
			PSE (Page size extension)
			TSC (Time stamp counter)
			MSR (Model specific registers)
			PAE (Physical address extension)
			MCE (Machine check exception)
			CX8 (CMPXCHG8 instruction supported)
			APIC (On-chip APIC hardware supported)
			SEP (Fast system call)
			MTRR (Memory type range registers)
			PGE (Page global enable)
			MCA (Machine check architecture)
			CMOV (Conditional move instruction supported)
			PAT (Page attribute table)
			PSE-36 (36-bit page size extension)
			CLFSH (CLFLUSH instruction supported)
			MMX (MMX technology supported)
			FXSR (FXSAVE and FXSTOR instructions supported)
			SSE (Streaming SIMD extensions)
			SSE2 (Streaming SIMD extensions 2)
			HTT (Multi-threading)
		Version: AMD G-T40E Processor
		Voltage: Unknown
		External Clock: 200 MHz
		Max Speed: 1600 MHz
		Current Speed: 1600 MHz
		Status: Populated, Enabled
		Upgrade: None
		L1 Cache Handle: Not Provided
		L2 Cache Handle: Not Provided
		L3 Cache Handle: Not Provided
		Serial Number: Not Specified
		Asset Tag: Not Specified
		Part Number: Not Specified
		Core Count: 2
		Characteristics: None

#### Installing Pkgs

Looking over [Installing FreeBSD Packages](https://doc.pfsense.org/index.php/Installing_FreeBSD_Packages) and it looks like **pfSense** has a custom **pkgng** repo and it actually has some good stuff:

	[2.3-RELEASE][root@pf.kar.int]/root: pkg search suricata
	pfSense-pkg-suricata-3.0_7     pfSense package suricata
	suricata-3.0_1                 High Performance Network IDS, IPS and Security Monitoring engine
	[2.3-RELEASE][root@pf.kar.int]/root: pkg search snort
	pfSense-pkg-snort-3.2.9.1_12   pfSense package snort
	snort-2.9.8.0                  Lightweight network intrusion detection system
	[2.3-RELEASE][root@pf.kar.int]/root: pkg search barnyard
	barnyard2-1.13                 Interpreter for Snort unified2 binary output files

### Other Similar Products

Even though this device is 2 years old it still looks pretty good. It looks like you can get a newer device from **pfSense**: [SG-2440](https://store.netgate.com/SG-2440.aspx). I think if this one starts to slow down, I might take a look at the newer devices coming out.
