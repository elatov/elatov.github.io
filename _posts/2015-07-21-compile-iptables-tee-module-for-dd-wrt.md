---
published: true
layout: post
title: "Compile iptables TEE Module for DD WRT"
author: Karim Elatov
categories: [networking]
tags: [dd_wrt]
---
I was running the following version of dd-wrt:

	root@DD-WRT:~# cat /etc/release 
	25015M

The full setup is covered [here](/2014/11/dd-wrt-on-asus-rt-ac68u-router/). I noticed in that version of DD-WRT the TEE module for iptables doesn't work. I found a couple of links that talk about the issue:

- [iptables features broke (tee)](http://svn.dd-wrt.com/ticket/3499)
- [iptables --tee does not work with my router/fw](http://www.dd-wrt.com/phpBB2/viewtopic.php?t=55128&postdays=0&postorder=asc&highlight=mirror&start=15)
- [Unable to add port mirroring iptables commands to Buffalo DD-WRT wireless router](http://seclists.org/snort/2014/q2/24)


It would just quitely fail without working:

	root@DD-WRT:~# iptables -A PREROUTING -t mangle -d 192.168.1.1 -j ROUTE --gw 10.0.0.3 --tee
	root@DD-WRT:~# iptables -t mangle -L
	Chain PREROUTING (policy ACCEPT)
	target     prot opt source               destination         
	
	Chain INPUT (policy ACCEPT)
	target     prot opt source               destination         
	
	Chain FORWARD (policy ACCEPT)
	target     prot opt source               destination         
	
	Chain OUTPUT (policy ACCEPT)
	target     prot opt source               destination         
	
	Chain POSTROUTING (policy ACCEPT)
	target     prot opt source               destination       


And if I just tried using the TEE module directly it would fail:

	root@DD-WRT:~# iptables -t mangle -A PREROUTING -i br0 -j TEE --gateway 192.168.20.2
	iptables v1.3.7: Unknown arg `--gateway'
	
It seems that it just depends on the version of dd-wrt that you get, if you are lucky you will have the TEE modules for iptables and if you are not, you won't. It seems I was not one of the lucky ones:

	root@DD-WRT:~# find /lib/modules -name "*.ko" | grep -i netfilter
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_802_3.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_among.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_arp.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_arpreply.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_dnat.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_ip.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_ip6.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_limit.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_log.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_mark.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_mark_m.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_nflog.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_pkttype.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_redirect.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_snat.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_stp.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_ulog.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebt_vlan.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebtable_broute.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebtable_filter.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebtable_nat.ko
	/lib/modules/3.10.54/kernel/net/bridge/netfilter/ebtables.ko
	/lib/modules/3.10.54/kernel/net/ipv4/netfilter/nf_nat_pptp.ko
	/lib/modules/3.10.54/kernel/net/ipv4/netfilter/nf_nat_proto_gre.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6_tables.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_MASQUERADE.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_NPT.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_REJECT.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_ah.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_frag.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_ipv6header.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_rpfilter.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6t_rt.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6table_filter.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6table_mangle.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/ip6table_nat.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/nf_conntrack_ipv6.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/nf_defrag_ipv6.ko
	/lib/modules/3.10.54/kernel/net/ipv6/netfilter/nf_nat_ipv6.ko
	/lib/modules/3.10.54/kernel/net/netfilter/nf_conntrack_pptp.ko
	/lib/modules/3.10.54/kernel/net/netfilter/nf_conntrack_proto_gre.ko
	/lib/modules/3.10.54/kernel/net/netfilter/nf_conntrack_sip.ko
	/lib/modules/3.10.54/kernel/net/netfilter/nf_nat_sip.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_DSCP.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_IMQ.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_addrtype.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_cpu.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_devgroup.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_dscp.ko
	/lib/modules/3.10.54/kernel/net/netfilter/xt_physdev.ko

Also only after version **1.4.8** does **iptables** even support the TEE module:

- [ChangeLog IPtables 1.4.8](http://www.netfilter.org/projects/iptables/files/changes-iptables-1.4.8.txt)
- [Update release iptables - 1.4.9](http://svn.dd-wrt.com/ticket/2166)

So let's compile a new version of iptables

### Compile dd-wrt Linux Kernel Modules

Before we can compile **iptables** we need to grab the toolchain and also compile the TEE module. I ran into a couple of pages that describe the process for my router:

- [hw_cdc_driver, e3372 and AC68U](http://www.dd-wrt.com/phpBB2/viewtopic.php?p=973183&sid=6e5dab736679b50c6792f54d86c17738)
- [Compile modules for R7000](http://www.dd-wrt.com/phpBB2/viewtopic.php?p=900316)
- [Error while building the kernel image](https://github.com/boundarydevices/linux-imx6/issues/6)

So here is what I ran to get the toolchain:

	cd /data/work/wrt/
	wget http://download1.dd-wrt.com/dd-wrtv2/downloads/toolchains/toolchains.tar.xz 
	tar -xvf toolchains.tar.xz 

And here is what I did to check the linux source to get the TEE module compiled:

	cd /data/work 
	svn checkout svn://svn.dd-wrt.com/DD-WRT/src/linux/universal/linux-3.10 
	cd linux-3.10 
	cp .config_northstar_smp .config 
	export PATH=$PATH:/data/work/wrt/toolchain-arm_cortex-a9_gcc-4.8-linaro_musl-1.1.5_eabi/bin 

You will also notice that by default the TEE module is not enabled:

	elatov@gen:/data/work/linux-3.10$grep XT_TARGET_TEE .config
	# CONFIG_NETFILTER_XT_TARGET_TEE is not set

So right after that line just add the following line to the **.config** file:

	CONFIG_NETFILTER_XT_TARGET_TEE=m

After that's ready we can try to compile the modules:

	export CROSS_COMPILE=arm-linux-
	export ARCH=arm
	make modules ARCH=arm 

Initially I ran into this:

	scripts/kconfig/conf --silentoldconfig Kconfig
	drivers/net/wireless/Kconfig:284: can't open file "drivers/net/wireless/rt3352/rt2860v2_ap/Kconfig"
	/data/work/linux-3.10/scripts/kconfig/Makefile:36: recipe for target 'silentoldconfig' failed
	make[2]: *** [silentoldconfig] Error 1
	/data/work/linux-3.10/Makefile:510: recipe for target 'silentoldconfig' failed
	make[1]: *** [silentoldconfig] Error 2

That issue is described in [Compiling IPv6 modules from source for DD-WRT](https://blog.jmwhite.co.uk/2013/08/10/compiling-ipv6-modules-from-source-for-dd-wrt/). So I commented out the following:

	#if RALINK_DEVICE
	#source "drivers/net/wireless/rt3352/rt2860v2_ap/Kconfig"
	#source "drivers/net/wireless/rt3352/rt2860v2_sta/Kconfig"
	#endif

from **drivers/net/wireless/Kconfig**, I ran into another compile error and I ended up commenting out the following (in the same file) to get passed it:

	#if SOC_MT7620_OPENWRT || SOC_MT7621_OPENWRT
	#source "drivers/net/wireless/rt7620/rt2860v2_ap/Kconfig"
	#source "drivers/net/wireless/rt7620/rt2860v2_sta/Kconfig"
	#source "drivers/net/wireless/rt5592/Kconfig"
	#source "drivers/net/wireless/rt7612/rlt_wifi/Kconfig"
	#source "drivers/net/wireless/rt7610/Kconfig"
	#endif

After that the **make modules** finished:

	elatov@gen:/data/work/linux-3.10$make modules ARCH=arm
	scripts/kconfig/conf --silentoldconfig Kconfig
	drivers/usb/phy/Kconfig:4:error: recursive dependency detected!
	drivers/usb/phy/Kconfig:4:	symbol USB_PHY is selected by RALINK_USBPHY
	drivers/usb/phy/Kconfig:199:	symbol RALINK_USBPHY depends on USB_PHY
	.config:2278:warning: override: reassigning to symbol PPTP
	.config:2279:warning: override: reassigning to symbol NET_IPGRE
	warning: (PLAT_BCM5301X) selects FPE_FASTFPE which has unmet direct dependencies ((!AEABI || OABI_COMPAT) && !CPU_32v3)
	#
	# configuration written to .config
	#
	warning: (PLAT_BCM5301X) selects FPE_FASTFPE which has unmet direct dependencies ((!AEABI || OABI_COMPAT) && !CPU_32v3)
	  WRAP    arch/arm/include/generated/asm/auxvec.h
	  WRAP    arch/arm/include/generated/asm/bitsperlong.h
	  WRAP    arch/arm/include/generated/asm/cputime.h
	  WRAP    arch/arm/include/generated/asm/current.h
	  WRAP    arch/arm/include/generated/asm/emergency-restart.h
	  WRAP    arch/arm/include/generated/asm/errno.h
	
	...
	...
	  LD [M]  net/sched/sch_fq_codel.ko
	  CC      net/xfrm/xfrm_algo.mod.o
	  LD [M]  net/xfrm/xfrm_algo.ko
	  CC      net/xfrm/xfrm_ipcomp.mod.o
	  LD [M]  net/xfrm/xfrm_ipcomp.ko


You will see the TEE module here:

	elatov@gen:/data/work/linux-3.10$find . -name '*TEE.ko'
	./net/netfilter/xt_TEE.ko

Initially I noticed the module depended on **ipv6**:

	elatov@gen:/data/work/linux-3.10$modinfo ./net/netfilter/xt_TEE.ko
	filename:       /data/work/linux-3.10/./net/netfilter/xt_TEE.ko
	license:        GPL
	depends:        ipv6

So I went back and modified the **.config** file to not compile **ipv6** and after another **make modules** the **modinfo** looked like this:

	elatov@gen:/data/work/linux-3.10$modinfo ./net/netfilter/xt_TEE.ko
	filename:       /data/work/linux-3.10/./net/netfilter/xt_TEE.ko
	license:        GPL
	depends: 

So let's go ahead and copy the **TEE** module over:

	elatov@gen:/data/work/linux-3.10$scp ./net/netfilter/xt_TEE.ko root@wrt:/mnt/sda1/modules/.
	DD-WRT v24-sp2 kongac (c) 2014 NewMedia-NET GmbH
	Release: 09/13/14 (SVN revision: 25015M)
	root@wrt.dnsd.me's password: 
	xt_TEE.ko                           100% 4041     4.0KB/s   4.0KB/s   00:00    


If you disabled **ipv6** then you can just directly insert the module into the kernel:

	root@DD-WRT:~# lsmod | grep -i tee
	root@DD-WRT:~# insmod /mnt/sda1/modules/xt_TEE.ko 
	root@DD-WRT:~# lsmod | grep -i tee
	xt_TEE                  1256  0 [permanent]

If you didn't disable **ipv6** then you have insert that first:

	root@DD-WRT:~# insmod ipv6
	root@DD-WRT:~# insmod /mnt/sda1/modules/xt_TEE.ko


### Compile iptables

I ran into a site that actually went over the process: [Compiling ip6tables DD-WRT](http://www.jonisdumb.com/2011/02/compiling-ip6tables-dd-wrt.html). I also found a patch for **iptables** for the *arm-musl* architecture:

- [iptables build error when using musl-libc and kernel 3.18.x targeting ARM](http://www.spinics.net/lists/netfilter/msg55949.html)
- [iptables-1.4.14-musl-fixes.patch](https://github.com/sabotage-linux/sabotage/blob/master/KEEP/iptables-1.4.14-musl-fixes.patch)

So let's get the 1.4.14 version

	elatov@gen:/data/work/ipt2$wget http://www.netfilter.org/projects/iptables/files/iptables-1.4.14.tar.bz2
	elatov@gen:/data/work/ipt2$tar xjf iptables-1.4.14.tar.bz2
	elatov@gen:/data/work/ipt2$cd iptables-1.4.14
	elatov@gen:/data/work/ipt2/iptables-1.4.14$wget https://raw.githubusercontent.com/sabotage-linux/sabotage/master/KEEP/iptables-1.4.14-musl-fixes.patch
	elatov@gen:/data/work/ipt2/iptables-1.4.14$patch -p1 < iptables-1.4.14-musl-fixes.patch 
	patching file extensions/libip6t_ipv6header.c
	patching file extensions/libxt_TCPOPTSTRIP.c
	patching file include/libiptc/ipt_kernel_headers.h
	patching file include/linux/netfilter_ipv4/ip_tables.h
	patching file iptables/ip6tables-restore.c
	patching file iptables/ip6tables-save.c
	patching file iptables/iptables-restore.c
	patching file iptables/iptables-save.c
	patching file iptables/iptables-xml.c

Now let's make sure we use the same toolchain:

	elatov@gen:/data/work/ipt2/iptables-1.4.14$export PATH=$PATH:/data/work/wrt/toolchain-arm_cortex-a9_gcc-4.8-linaro_musl-1.1.5_eabi/bin

And now let's prepare the package:
 
	elatov@gen:/data/work/ipt2/iptables-1.4.14$./configure --prefix=/opt --host=arm-linux

Let's build it:

	elatov@gen:/data/work/ipt2/iptables-1.4.14$make

And finally let's install it and **tar** it up:

	elatov@gen:/data/work/ipt2/iptables-1.4.14$sudo mkdir /opt
	elatov@gen:/data/work/ipt2/iptables-1.4.14$sudo chown elatov /opt
	elatov@gen:/data/work/ipt2/iptables-1.4.14$make install
	elatov@gen:~$sudo chown -R 0:0 /opt
	elatov@gen:~$sudo tar cpvzf opt-iptables.tar.gz /opt

Now let's get **tar** that over to the dd-wrt router:

	elatov@gen:~$scp /opt-iptables.tar.gz root@dd-wrt:/mnt/sda1/.

Now on the router side let's install the new version under **/opt**:

	root@DD-WRT:~# tar -xzvf /mnt/sda1/opt-iptables.tar.gz -C /
	..
	..
	opt/sbin/iptables
	opt/sbin/ip6tables
	opt/sbin/iptables-save
	opt/sbin/iptables-restore
	opt/sbin/ip6tables-restore
	opt/sbin/ip6tables-save
	opt/bin/
	opt/bin/iptables-xml
	opt/share/
	opt/share/man/ 
	opt/share/man/man8/
	opt/share/man/man8/ip6tables.8
	opt/share/man/man8/iptables-save.8
	opt/share/man/man8/iptables-restore.8
	opt/share/man/man8/ip6tables-save.8
	opt/share/man/man8/ip6tables-restore.8
	opt/share/man/man8/iptables.8
	opt/share/man/man1/
	opt/share/man/man1/iptables-xml.1

after that's done you will see the new version:

	root@DD-WRT:~# /opt/sbin/iptables -v
	iptables v1.4.14: no command specified
	Try `iptables -h' or 'iptables --help' for more information.

I noticed the new version wasn't printing output for some reason:

	root@DD-WRT:~# /opt/sbin/iptables -L
	 prot opt --   
	 --   
	 --   
	 --   
	 --   
	 --   
	 --   
	 --   

But I was able to use the **TEE** module and confirm with the system **iptables**:

	root@DD-WRT:~# /opt/sbin/iptables -t mangle -A PREROUTING -i br0 -j TEE --gateway 10.0.0.3
	root@DD-WRT:~# iptables -L -n -v -t mangle
	Chain PREROUTING (policy ACCEPT 546 packets, 36545 bytes)
	 pkts bytes target     prot opt in     out     source               destination         
	  164 10876 TEE        0    --  br0    *       0.0.0.0/0            0.0.0.0/0           [40 bytes of unknown target data] 

When I ran the same on another Linux machine I saw the following:

	elatov@kerch:~$sudo iptables -L -n -v -t mangle
	Chain PREROUTING (policy ACCEPT 344 packets, 29217 bytes)
	 pkts bytes target     prot opt in     out     source               destination         
	    0     0 TEE        all  --  br0    *       0.0.0.0/0            0.0.0.0/0            TEE gw:10.0.0.3
	    
I noticed after some time that the memory usage spiked up on the router, so I decided not use the TEE module. But hopefully this will help out someone else :)
