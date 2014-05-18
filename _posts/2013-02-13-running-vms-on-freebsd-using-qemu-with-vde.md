---
title: Running VMs On FreeBSD using QEMU with VDE
author: Karim Elatov
layout: post
permalink: /2013/02/running-vms-on-freebsd-using-qemu-with-vde/
dsq_thread_id:
  - 1406836724
categories:
  - Home Lab
  - Networking
  - OS
tags:
  - /dev/tap0
  - /etc/devfs.conf
  - /etc/rc.conf
  - /etc/rc.local
  - /etc/sysctl.conf
  - aio
  - BHyve
  - freebsd
  - ifconfig bridge
  - kldload
  - kldstat
  - KQemu
  - KVM
  - net.link.tap.up_on_open
  - net.link.tap.user_open
  - Qemu
  - qemu-img
  - sysctl
  - tcpdump
  - tigervnc
  - TUN/TAP
  - unixterm
  - VDE
  - vdeqemu
  - vde_switch
  - VirtualBox
---
I decided to run some VMs on my FreeBSD server. Checking over <a href="http://en.wikipedia.org/wiki/Comparison_of_platform_virtual_machines" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Comparison_of_platform_virtual_machines']);">this</a> wikipedia page, it seems that *KVM*, *QUME*, and *VirtualBox* were my only options. I remember using *VirtualBox* with FreeBSD before and even though it's really solid, the compile would take a while. I wanted to try out *KVM* but it seems the project, which was started in 2007, never really took off. You can try to compile the *KVM* module but I didn't want to try something that hasn't been developed since 2007. There is actually a nice conversation about that <a href="http://lists.freebsd.org/pipermail/freebsd-virtualization/2011-July/000730.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://lists.freebsd.org/pipermail/freebsd-virtualization/2011-July/000730.html']);">here</a>. In that same article they mention a new hypervisor that is specifically made for FreeBSD. The project is called <a href="http://bhyve.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bhyve.org/']);">BHyve</a>, apparently it's being developed in collaboration with *NetAPP*. The project is currently supported in FreeBSD 10 and I was running FreeBSD 9. So after all of my research, I decided to give *Qemu*/*KQemu* a try.

Now what exactly is the difference between *Qemu* and *KVM*? from the *KVM* <a href="http://www.linux-kvm.org/page/FAQ#What_is_the_difference_between_KVM_and_QEMU.3F" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linux-kvm.org/page/FAQ#What_is_the_difference_between_KVM_and_QEMU.3F']);">FAQ</a>:

> QEMU uses emulation; KVM uses processor extensions (HVM) for virtualization.

And what about *KQemu*? from the <a href="http://en.wikipedia.org/wiki/QEMU" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/QEMU']);">Qemu</a> wikipedia page:

> QEMU (short for "Quick EMUlator") is a free and open-source software product that performs hardware virtualization.
> 
> QEMU is a hosted virtual machine monitor: It emulates central processing units through dynamic binary translation and provides a set of device models, enabling it to run a variety of unmodified guest operating systems. It also provides an accelerated mode for supporting a mixture of binary translation (for kernel code) and native execution (for user code), in the same fashion VMware Workstation and VirtualBox do. QEMU can also be used purely for CPU emulation for user level processes, allowing applications compiled for one architecture to be run on another.
> 
> ...
> 
> KQEMU was a Linux kernel module, also written by Fabrice Bellard, which notably sped up emulation of x86 or x86-64 guests on platforms with the same CPU architecture. This was accomplished by running user mode code (and optionally some kernel code) directly on the host computer's CPU, and by using processor and peripheral emulation only for kernel mode and real mode code.
> 
> Unlike KVM, for example, KQEMU could execute code from many guest OSes even if the host CPU did not support hardware virtualization.

Lastly from the Qemu's <a href="http://wiki.qemu.org/Main_Page" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.qemu.org/Main_Page']);">main</a> page:

> QEMU is a generic and open source machine emulator and virtualizer.
> 
> When used as a machine emulator, QEMU can run OSes and programs made for one machine (e.g. an ARM board) on a different machine (e.g. your own PC). By using dynamic translation, it achieves very good performance.
> 
> When used as a virtualizer, QEMU achieves near native performances by executing the guest code directly on the host CPU. QEMU supports virtualization when executing under the Xen hypervisor or using the KVM kernel module in Linux. When using KVM, QEMU can virtualize x86, server and embedded PowerPC, and S390 guests.

So to re-phrase my initial sentence: I will be virtualizing/emulating an OS within the FreeBSD kernel and using the *KQemu* acceleration kernel module to improve performance/execution.

Now let's get started with the setup, first let's install *Qemu*, instructions can be found <a href="http://www.linux-kvm.org/page/BSD" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linux-kvm.org/page/BSD']);">here</a> and <a href="https://wiki.freebsd.org/qemu" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.freebsd.org/qemu']);">here</a>:

    elatov@freebsd:~> cd /usr/ports/emulators/qemu 
    elatov@freebsd:/usr/ports/emulators/qemu> make showconfig 
    ===> The following configuration options are available for qemu-0.11.1_11: 
    ADD_AUDIO=off: Emulate more audio hardware (experimental!) 
    ALL_TARGETS=on: Also build non-x86 targets 
    CDROM_DMA=on: IDE 
    CDROM DMA CURL=on: libcurl dependency (remote images) 
    GNS3=off: gns3 patches (udp, promiscuous multicast) 
    GNUTLS=on: gnutls dependency (vnc encryption) 
    KQEMU=on: Build with (alpha!) accelerator module 
    PCAP=on: pcap dependency (networking with bpf) 
    RTL8139_TIMER=off: allow use of re(4) nic with 
    FreeBSD guests SAMBA=off: samba dependency (for -smb) 
    SDL=on: SDL/X dependency (graphical output) 
    ===> Use 'make config' to modify these settings 
    elatov@freebsd:/usr/ports/emulators/qemu> sudo make install clean 
    

After the compile finished you can enable the *KQemu* module to be loaded on boot, this is done by adding the following to the **/etc/rc.conf** file:

    kqemu_enable="YES
    

This will load the *KQemu* module on start up and it will also check if the *aio* module is loaded. If the *aio* module is not loaded, it will also load it.

Before rebooting, load them manually and make sure they load properly:

    elatov@freebsd:~> sudo kldload kqemu 
    elatov@freebsd:~> sudo kldload aio 
    elatov@freebsd:~> kldstat 
    Id Refs Address Size Name 
    1 7 0xc0400000 e9ec64 kernel 
    2 1 0xc6451000 e000 fuse.ko 
    3 1 0xcd147000 21000 kqemu.ko 
    4 1 0xcd168000 8000 aio.ko 
    

That looks good. As a quick test, let's create an *img* file:

    elatov@freebsd:~> cd /data/vms 
    elatov@freebsd:/data/vms> qemu-img create -f raw rhel2.img 8G 
    

The '**-f**' option specifies the format of the image, from the *man* page here are the options:

> "raw"  
> Raw disk image format (default). This format has the advantage of being simple and easily exportable to all other emulators. If your file system supports holes (for example in ext2 or ext3 on Linux or NTFS on Windows), then only the written sectors will reserve space. Use "qemu-img info" to know the real size used by the image or "ls -ls" on Unix/Linux.
> 
> "qcow2"  
> QEMU image format, the most versatile format. Use it to have smaller images (useful if your filesystem does not supports holes, for example on Windows), optional AES encryption, zlib based compression and support of multiple VM snapshots.
> 
> "qcow"  
> Old QEMU image format. Left for compatibility.
> 
> "cow"  
> User Mode Linux Copy On Write image format. Used to be the only growable image format in QEMU. It is supported only for compatibility with previous versions. It does not work on win32.
> 
> "vmdk"  
> VMware 3 and 4 compatible image format.
> 
> "cloop"  
> Linux Compressed Loop image, useful only to reuse directly compressed CD-ROM images present for example in the Knoppix CD- ROMs.

Since I will be running RHEL on the VM (that will use an *ext* filesystem), I decided to use the *raw* format. Now to start the VM using that *img* file as the hard drive:

    elatov@freebsd:/data/vms> qemu -cdrom ../rhel-server-5.5-i386-dvd.iso -hda rhel2.img -m 256 -boot d -kernel-kqemu -vnc :0 -localtime
    

Now to test connectivity, from a Fedora machine I installed a *VNC* client:

    moxz:~> sudo yum install tigervnc
    

After it's installed, I tried to connect to the VM:

    moxz:~> vncviewer 192.168.1.101:5900
    

A *VNC* window popped up without any issues, and I saw the RHEL CD boot up. Now if we want our VM to have access to the network then we have a couple of options. From the <a href="http://wiki.qemu.org/Documentation/Networking" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.qemu.org/Documentation/Networking']);">Qemu Networking</a> page, we can use "**User Mode Networking**":

> **User Mode Networking** – In this mode, the QEMU virtual machine automatically starts up an internal DHCP server on an internal networkaddress -10.0.2.2/24. This is internal to the guest environment and is not visible from the host environment. If the guest OS is set up for DHCP, the guest will get an IP address from this internal DHCP server. The QEMU virtual machine will also gateway packets onto the host network through 127.0.0.1. In this way, QEMU can provide an automatic network environment for the QEMU user without any manual configuration.

Here is a good diagram of how it works:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/qemu_user_networking.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/qemu_user_networking.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/qemu_user_networking.png" alt="qemu user networking Running VMs On FreeBSD using QEMU with VDE" width="444" height="307" class="alignnone size-full wp-image-6062" title="Running VMs On FreeBSD using QEMU with VDE" /></a>

Second we can use "**TUN/TAP Network Interface**". From <a href="http://bsdwiki.reedmedia.net/wiki/networking_qemu_virtual_bsd_systems.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bsdwiki.reedmedia.net/wiki/networking_qemu_virtual_bsd_systems.html']);">this</a> page:

> **TUN/TAP Network Interface** – In this mode, the QEMU Virtual Machine opens a pre-allocated TUN or TAP device on the host and uses that interface to transfer data to the guest OS. This method involves the standard manual configuration of the guest OS interface using the **ifconfig** command. This method doesn't involve the DHCP server. However, note that the server is still running, it's just not used by an interface using this method.

Lastly we can use the "**VDE**" (Virtual Distributed Ethernet) method:

> The **VDE** networking backend uses the Virtual Distributed Ethernet infrastructure to network guests. From the <a href="http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE']);">VDE</a> page:
> 
> VDE switch  
> Like a physical ethernet switch, a VDE switch has several virtual ports where virtual machines, applications, virtual interfaces, connectivity tools and - why not? - other VDE switch can be virtually plugged in.
> 
> ...
> 
> vde_switch  
> The vde_switch is a virtual switch provided with the vde networking architecture. As vde_switch can interconnect several virtual networking devices multiple vde_switches can be connected together with vde_cables.

Since Jarret already did a <a href="http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/']);">post</a> on the bridged/*tap* networking with *KVM*, I decided to try out the *VDE* setup. First let's install the *VDE* Package:

    elatov@freebsd:~> cd /usr/ports/net/vde2 
    elatov@freebsd:/usr/ports/net/vde2> sudo make install clean
    

Here is the config I used:

    elatov@freebsd:/usr/ports/net/vde2> make showconfig 
    ===> The following configuration options are available for vde2-2.3.2: 
    PYTHON=on: Python bindings 
    ===> Use 'make config' to modify these settings
    

After that is installed we should create a *tap* interface to act as an uplink for our *VDE*-switch. Instructions for this can be found <a href="http://bsdwiki.reedmedia.net/wiki/networking_qemu_virtual_bsd_systems.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bsdwiki.reedmedia.net/wiki/networking_qemu_virtual_bsd_systems.html']);">here</a> and <a href="https://wiki.freebsd.org/qemu" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.freebsd.org/qemu']);">here</a>. First let's create the *bridge*:

    elatov@freebsd:~> sudo ifconfig bridge0 create
    

Then let's create the *tap* interface:

    elatov@freebsd:~> sudo ifconfig tap0 create
    

Now let's bridge our physical interface with our *tap* interface:

    elatov@freebsd:~> sudo ifconfig bridge0 addm em0 addm tap0 up
    

Now checking the settings for both interfaces:

    elatov@freebsd:~> ifconfig bridge0 
    bridge0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500 
             ether 02:84:95:2c:24:00 
             nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL> 
             id 00:00:00:00:00:00 priority 32768 hellotime 2 fwddelay 15 
             maxage 20 holdcnt 6 proto rstp maxaddr 100 timeout 1200 
             root id 00:00:00:00:00:00 priority 32768 ifcost 0 port 0 
             member: tap0 flags=143<LEARNING,DISCOVER,AUTOEDGE,AUTOPTP> 
                     ifmaxaddr 0 port 8 priority 128 path cost 2000000 
             member: em0 flags=143<LEARNING,DISCOVER,AUTOEDGE,AUTOPTP> 
                     ifmaxaddr 0 port 1 priority 128 path cost 20000
    

We see both interfaces (**tap0** and **em0**) there, and our **tap0** interface:

    elatov@freebsd:~> ifconfig tap0 
    tap0: flags=8902<BROADCAST,PROMISC,SIMPLEX,MULTICAST> metric 0 mtu 1500 
          options=80000<LINKSTATE> 
          ether 00:bd:e4:d8:f1:00 
          nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>
    

Since we will be connecting to the *tap* device with regular users, let's allow regular users to connect to our *tap* device:

    elatov@freebsd:~> sudo sysctl net.link.tap.user_open=1 
    net.link.tap.user_open: 0 -> 1 
    elatov@freebsd:~> sudo sysctl net.link.tap.up_on_open=1 
    net.link.tap.up_on_open: 0 -> 1
    

Also let's fix the permissions on the file for the **tap0** device:

    elatov@freebsd:~> sudo chown :elatov /dev/tap0 
    elatov@freebsd:~> sudo chmod 660 /dev/tap0
    

Now confirming the permissions:

    elatov@freebsd:~> ls -l /dev/tap0 
    crw-rw---- 1 root elatov 0, 109 Feb 3 16:14 /dev/tap0
    

That looks good. Now let's create a *VDE*-Switch and add **tap0** as our uplink:

    elatov@freebsd:~> sudo vde_switch -d -s /tmp/vde1 -M /tmp/mgmt1 -tap tap0 -m 660 -g elatov --mgmtmode 660 --mgmtgroup elatov 
    

Here are all the arguments explained:

> *   **-d** option tells vde_switch to run as daemon or background process. 
> *   **-s** is the complete path to data socket for the switch. 
> *   **-M** specifies where to create the management socket for the switch. 
> *   **-t** specifies the tap interface name that connected to the switch. 
> *   **-m** specifies mode of data socket -g specified group owner of data socket 
> *   **-mgmtmode** specifies mode of mgmt socket 
> *   **-mgmtgroup** specifies group owner of mgmt socket

Now let's login into the virtual switch:

    elatov@freebsd:~> unixterm /tmp/mgmt1 
    VDE switch V.2.3.2 (C) 
    Virtual Square Team (coord. R. Davoli) 2005,2006,2007 - GPLv2 
    
    vde$ ds/showinfo 
    0000 DATA END WITH '.' 
    ctl dir /tmp/vde1 
    std mode 0660 
    . 
    1000 Success 
    
    vde$ port/allprint 
    0000 DATA END WITH '.' 
    Port 0001 untagged_vlan=0000 ACTIVE - Unnamed Allocatable 
    Current User: NONE Access Control: (User: NONE - Group: NONE)
     -- endpoint ID 0007 module tuntap : tap0 
    . 
    1000 Success 
    
    vde$ vlan/allprint 
    0000 DATA END WITH '.' 
    VLAN 0000 
    -- Port 0001 tagged=0 active=1 status=Forwarding 
    . 
    1000 Success 
    

Most of the information regarding the *VDE* was taken from <a href="http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE#Some_usage_examples" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE#Some_usage_examples']);">here</a>. BTW, there is also a web and telnet client for the *VDE*-switch. Instructions on how to set that up are <a href="http://wiki.v2.cs.unibo.it/wiki/index.php?title=Vdetelweb:_Telnet_and_Web_management_for_VDE" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','']);">here</a>; '**unixterm**' was good enough for me :) 

Now starting up the VM and connecting it to our *VDE*-Switch:

    elatov@freebsd:~>vdeqemu -hda rhel2.img -m 256 -kernel-kqemu -vnc :0 -localtime -no-acpi -net vde,sock=/tmp/vde1 -net nic,model=e1000
    

Now checking out the switch ports:

    elatov@freebsd:~>unixterm /tmp/mgmt1 
    VDE switch V.2.3.2 
    (C) Virtual Square Team (coord. R. Davoli) 2005,2006,2007 - GPLv2 
    
    vde$ port/allprint 
    0000 DATA END WITH '.' 
    Port 0001 untagged_vlan=0000 ACTIVE - Unnamed Allocatable 
    Current User: NONE Access Control: (User: NONE - Group: NONE) 
    -- endpoint ID 0007 module tuntap : tap0 
    Port 0002 untagged_vlan=0000 ACTIVE - Unnamed Allocatable 
    Current User: elatov Access Control: (User: NONE - Group: NONE) 
    -- endpoint ID 0003 module unix prog : vdeqemu 
    user=elatov PID=98624 SSH=192.168.1.102 
    . 
    1000 Success
    

We can see that now our VM is connected to the *VDE*-Switch. Since all the traffic is going through our **tap0** interface, we can actually run **tcpdump** on it to see what traffic our VM is sending. Let's ping a machine on the local subnet from the VM and see what we see on the **tap0** interface. Here is the capture from the FreeBSD host as the ping is going:

    elatov@freebsd:~> sudo tcpdump -i tap0 -n host 192.168.1.110 and icmp 
    tcpdump: WARNING: tap0: no IPv4 address assigned 
    tcpdump: verbose output suppressed, use -v or -vv for full protocol 
    decode listening on tap0, link-type EN10MB (Ethernet), capture size 65535 bytes 
    17:40:01.353744 IP 192.168.1.110 > 192.168.1.102: ICMP echo request, id 12298, seq 1, length 64 
    17:40:01.353957 IP 192.168.1.102 > 192.168.1.110: ICMP echo reply, id 12298, seq 1, length 64
    

If you didn't guess it, the VM's IP is 192.168.1.110. You can also monitor traffic using file sockets. In depth instructions are laid out <a href="http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE#VDE_components" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.v2.cs.unibo.it/wiki/index.php?title=VDE#VDE_components']);">here</a>.

Since we don't want to keep recreating the above settings, let's go ahead and setup all the above options/settings to be auto configured on boot. We already enabled the *kqemu* module to be loaded on boot, now let's setup the bridge and *tap* interfaces to be created on boot. Add the following to the **/etc/rc.conf** file:

    cloned_interfaces="tap0 bridge0" 
    ifconfig_bridge0="addm em0 addm tap0 up"
    

Now let's enable the *sysctl* options. Add the following to the **/etc/sysctl.conf** file:

    net.link.tap.user_open=1 
    net.link.tap.up_on_open=1
    

Next let's setup the appropriate permissions for our **tap0** device. Add the following to the **/etc/devfs.conf** file:

    own tap0 root:elatov 
    perm tap0 660
    

Lastly, create the *VDE*-Switch boot. Add the following to the **/etc/rc.local** file:

    /usr/local/bin/vde_switch -d -s /tmp/vde1 -M /tmp/mgmt1 -tap tap0 -m 660 -g elatov --mgmtmode 660 --mgmtgroup elatov
    

So I rebooted the FreeBSD host and I wanted to make sure all the settings look good. First I wanted to make sure my **bridge0** and **tap0** interfaces were setup: 
	
	elatov@freebsd:~> ifconfig tap0 
	tap0: flags=8942<BROADCAST,RUNNING,PROMISC,SIMPLEX,MULTICAST> metric 0 mtu 1500
		  options=80000<LINKSTATE> 
		  ether 00:bd:90:1a:00:00 
		  nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>
	    
	
and the **bridge0** interface:
	
	elatov@freebsd:~> ifconfig bridge0 
	bridge0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500 
			 ether 02:84:95:2c:24:00 
			 nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL> 
			 id 00:00:00:00:00:00 priority 32768 hellotime 2 fwddelay 15 
			 maxage 20 holdcnt 6 proto rstp maxaddr 100 timeout 1200 
			 root id 00:00:00:00:00:00 priority 32768 ifcost 0 port 0 
			 member: tap0 flags=143<LEARNING,DISCOVER,AUTOEDGE,AUTOPTP> 
					 ifmaxaddr 0 port 7 priority 128 path cost 2000000 
			 member: em0 flags=143<LEARNING,DISCOVER,AUTOEDGE,AUTOPTP> 
					 ifmaxaddr 0 port 1 priority 128 path cost 2000000


That looked good. Next I wanted to make sure my *VDE*-Switch was created:
	
	elatov@freebsd:~> unixterm /tmp/mgmt1 
	VDE switch V.2.3.2 
	(C) Virtual Square Team (coord. R. Davoli) 2005,2006,2007 - GPLv2 

	vde$ ds/showinfo 
	0000 DATA END WITH '.' 
	ctl dir /tmp/vde1 
	std mode 0660 
	. 
	1000 Success 

	vde$ port/allprint 
	0000 DATA END WITH '.' 
	Port 0001 untagged_vlan=0000 ACTIVE - Unnamed Allocatable 
	Current User: NONE Access Control: (User: NONE - Group: NONE) 
	-- endpoint ID 0007 module tuntap : tap0 
	. 
	1000 Success 


That also looked good, we even see the **tap0** device connected. Then I wanted to make sure the persmission on my **tap0** device were correct:

	elatov@freebsd:~> ls -l /dev/tap0 
	crw-rw---- 1 root elatov 0, 102 Feb 3 18:00 /dev/tap0

and I wanted to make sure the *sysctl* settings looked good as well:

	elatov@freebsd:~> sysctl net.link.tap.user_open 
	net.link.tap.user_open: 1 
	elatov@freebsd:~> sysctl net.link.tap.up_on_open 
	net.link.tap.up_on_open: 1

And lastly I wanted to make sure the kernel modules were loaded:

	elatov@freebsd:~>kldstat 
	Id Refs Address Size Name 
	1 13 0xc0400000 e9ec64 kernel 
	2 1 0xc62de000 5000 if_tap.ko 
	3 1 0xc6302000 9000 if_bridge.ko 
	4 1 0xc630b000 6000 bridgestp.ko 
	5 1 0xc647c000 e000 fuse.ko 
	6 1 0xc64ef000 8000 aio.ko 
	7 1 0xc64fa000 21000 kqemu.ko

Everything looked good. As Jarret mentioned in his <a href="http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/']);">post</a>, there are a lot of ways to go about managing VMs. Here is <a href="http://www.linux-kvm.org/page/Management_Tools" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linux-kvm.org/page/Management_Tools']);">web-page</a> with all the different tools. Checking over the FreeBSD ports, I only found the following:

*   virt-manager
*   virtinst
*   aqemu
*   virsh 
	
All of the above (except **aqemu**) depend on the **libvirt** libraries. After further investigation it turned out that *libvirt* and *VDE* don't work together... yet. From <a href="https://gist.github.com/1787749" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://gist.github.com/1787749']);">here</a>, a snippet:
	
> For generic situations libvirt and virt-manager are useful tools to help manage VM clusters. ubuntu-vm-builder is useful for creating VMs and adding them to libvirt hosts. VDE and libvirt Don't Play Together
> 
> Unfortunately libvirt doesn't currently support VDE networks, although it is possible for someone to implement a VDE interface using the libvirt network API.

I was planning on only running 2 VMs, so this wasn't a big deal for me. Running the follow two commands to start my VMs is pretty easy:

	elatov@freebsd:~>vdeqemu -hda rhel1.img -m 512 -kernel-kqemu -vnc :0 -localtime -no-acpi -net nic,model=e1000,macaddr=52:54:00:12:34:56 -net vde,sock=/tmp/vde1 & 
	elatov@freebsd:~>vdeqemu -hda rhel2.img -m 256 -kernel-kqemu -vnc :1 -localtime -no-acpi -net nic,model=e1000,macaddr=52:54:00:12:34:57 -net vde,sock=/tmp/vde1 &

<div class="SPOSTARBUST-Related-Posts">
  <H3>
	Related Posts
  </H3>

  <ul class="entry-meta">
	<li class="SPOSTARBUST-Related-Post">
	  <a title="Migrating a VM from VMware Workstation to Oracle VirtualBox" href="http://virtuallyhyper.com/2013/04/migrating-a-vm-from-vmware-workstation-to-oracle-virtualbox/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/migrating-a-vm-from-vmware-workstation-to-oracle-virtualbox/']);" rel="bookmark">Migrating a VM from VMware Workstation to Oracle VirtualBox</a>
	</li>
  </ul>
</div>