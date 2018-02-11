---
published: true
layout: post
title: "Troubleshooting tg3 Driver Issues on MacMini Running CoreOS"
author: Karim Elatov
categories: [network]
tags: [coreos,tg3,ethtool,tso,gso,sg]
---
### tg3 Driver StackTrace

I had my MariaDB Container running on my CoreOS machine (which is installed on a MacMini 6,2) and some services kept disconnecting from the database at random times. I logged into the CoreOS machine and I saw the following from **dmesg**:

	Jul 07 07:30:10 core kernel: WARNING: CPU: 0 PID: 0 at ../source/net/sched/sch_generic.c:316 dev_watchdog+0x220/0x230
	Jul 07 07:30:10 core kernel: NETDEV WATCHDOG: enp1s0f0 (tg3): transmit queue 0 timed out
	Jul 07 07:30:10 core kernel: Modules linked in: xt_nat veth xfrm_user xfrm_algo xt_addrtype iptable_filter xt_conntrack br_netfilter bridge stp llc ipt_MASQUERADE nf_nat_masquerade_ipv4 iptable_nat nf_conntrack_ipv4 nf_defrag_ipv4 nf_nat_ipv4 nf_nat nf_conntrack libcrc32c crc32c_generic vxlan ip6_udp_tunnel udp_tunnel overlay efi_pstore coretemp x86_pkg_temp_thermal nls_ascii nls_cp437 kvm_intel vfat fat kvm mousedev evdev efivars i2c_i801 mei_me irqbypass i2c_core mei button sch_fq_codel hid_generic usbhid hid ext4 crc16 jbd2 fscrypto mbcache dm_verity dm_bufio sd_mod ahci libahci crc32c_intel xhci_pci ehci_pci ehci_hcd xhci_hcd libata aesni_intel tg3 ixgbe aes_x86_64 crypto_simd cryptd glue_helper scsi_mod usbcore sdhci_pci sdhci libphy mmc_core hwmon usb_common ptp pps_core mdio dm_mirror dm_region_hash dm_log
	Jul 07 07:30:10 core kernel:  dm_mod
	Jul 07 07:30:10 core kernel: CPU: 0 PID: 0 Comm: swapper/0 Not tainted 4.11.9-coreos #1
	Jul 07 07:30:10 core kernel: Hardware name: Apple Inc. Macmini6,2/Mac-F65AE981FFA204ED, BIOS MM61.88Z.0106.B04.1309191433 09/19/2013
	Jul 07 07:30:10 core kernel: Call Trace:
	Jul 07 07:30:10 core kernel:  <IRQ>
	Jul 07 07:30:10 core kernel:  dump_stack+0x63/0x90
	Jul 07 07:30:10 core kernel:  __warn+0xd1/0xf0
	Jul 07 07:30:10 core kernel:  warn_slowpath_fmt+0x5a/0x80
	Jul 07 07:30:10 core kernel:  dev_watchdog+0x220/0x230
	Jul 07 07:30:10 core kernel:  ? dev_deactivate_queue.constprop.31+0x60/0x60
	Jul 07 07:30:10 core kernel:  call_timer_fn+0x35/0x140
	Jul 07 07:30:10 core kernel:  run_timer_softirq+0x1db/0x440
	Jul 07 07:30:10 core kernel:  ? sched_clock+0x9/0x10
	Jul 07 07:30:10 core kernel:  ? sched_clock+0x9/0x10
	Jul 07 07:30:10 core kernel:  ? sched_clock_cpu+0x11/0xb0
	Jul 07 07:30:10 core kernel:  __do_softirq+0xf5/0x298
	Jul 07 07:30:10 core kernel:  irq_exit+0xae/0xb0
	Jul 07 07:30:10 core kernel:  smp_apic_timer_interrupt+0x3d/0x50
	Jul 07 07:30:10 core kernel:  apic_timer_interrupt+0x89/0x90
	Jul 07 07:30:10 core kernel: RIP: 0010:cpuidle_enter_state+0x116/0x270
	Jul 07 07:30:10 core kernel: RSP: 0018:ffffffffb2c03dd8 EFLAGS: 00000246 ORIG_RAX: ffffffffffffff10
	Jul 07 07:30:10 core kernel: RAX: ffff88a6af21a440 RBX: ffff88a6af223300 RCX: 000000000000001f
	Jul 07 07:30:10 core kernel: RDX: 0000000000000000 RSI: ffff88a6af217c58 RDI: 0000000000000000
	Jul 07 07:30:10 core kernel: RBP: ffffffffb2c03e10 R08: 0000000000000005 R09: 0000000000003351
	Jul 07 07:30:10 core kernel: R10: ffffffffb2c03da8 R11: ffff88a6af2175e4 R12: 0000000000000005
	Jul 07 07:30:10 core kernel: R13: 0000000000000005 R14: 0000000000000000 R15: 000002255c8f052d
	Jul 07 07:30:10 core kernel:  </IRQ>
	Jul 07 07:30:10 core kernel:  ? cpuidle_enter_state+0xf2/0x270
	Jul 07 07:30:10 core kernel:  cpuidle_enter+0x17/0x20
	Jul 07 07:30:10 core kernel:  call_cpuidle+0x23/0x40
	Jul 07 07:30:10 core kernel:  do_idle+0x17f/0x1f0
	Jul 07 07:30:10 core kernel:  cpu_startup_entry+0x71/0x80
	Jul 07 07:30:10 core kernel:  rest_init+0x77/0x80
	Jul 07 07:30:10 core kernel:  start_kernel+0x45e/0x47f
	Jul 07 07:30:10 core kernel:  ? early_idt_handler_array+0x120/0x120
	Jul 07 07:30:10 core kernel:  x86_64_start_reservations+0x24/0x26
	Jul 07 07:30:10 core kernel:  x86_64_start_kernel+0x147/0x16a
	Jul 07 07:30:10 core kernel:  start_cpu+0x14/0x14
	Jul 07 07:30:10 core kernel: ---[ end trace a872cd2b1f06ea6c ]---
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: transmit timed out, resetting
	Jul 07 07:30:10 core kernel: hrtimer: interrupt took 3281865 ns
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 0x00000000: 0x168614e4, 0x00100406, 0x02000001, 0x00800040
	..
	..
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 0: Host status block [00000001:000000f8:(0000:013d:0000):(0000:0020)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 0: NAPI info [000000f8:000000f8:(000d:0020:01ff):0000:(0004:0000:0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 1: Host status block [00000001:000000c0:(0000:0000:0000):(0229:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 1: NAPI info [000000c0:000000c0:(0000:0000:01ff):0229:(0029:0029:0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 2: Host status block [00000001:000000a3:(0137:0000:0000):(0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 2: NAPI info [000000a3:000000a3:(0000:0000:01ff):0137:(0137:0137:0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 3: Host status block [00000001:000000c4:(0000:0000:0000):(0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 3: NAPI info [000000c4:000000c4:(0000:0000:01ff):03dd:(01dd:01dd:0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 4: Host status block [00000001:000000b4:(0000:0000:03ff):(0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: 4: NAPI info [000000b4:000000b4:(0000:0000:01ff):03ff:(01ff:01ff:0000:0000)]
	Jul 07 07:30:10 core kernel: tg3 0000:01:00.0 enp1s0f0: Link is down
	Jul 07 07:30:10 core systemd-networkd[928]: enp1s0f0: Lost carrier
	Jul 07 07:30:10 core systemd-timesyncd[738]: Network configuration changed, trying to establish connection.
	Jul 07 07:30:13 core kernel: tg3 0000:01:00.0 enp1s0f0: Link is up at 1000 Mbps, full duplex
	Jul 07 07:30:13 core kernel: tg3 0000:01:00.0 enp1s0f0: Flow control is on for TX and on for RX
	Jul 07 07:30:13 core kernel: tg3 0000:01:00.0 enp1s0f0: EEE is disabled
	Jul 07 07:30:13 core systemd-networkd[928]: enp1s0f0: Gained carrier
	Jul 07 07:30:13 core systemd-networkd[928]: enp1s0f0: Configured

### Network Card Modifications

I ran into a couple of sites that matched that backtrace:

* [Broadcom BCM5906M ethernet adapter (tg3) hangs under heavy tcp load when generic segmentation offload (gso) is in use](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/404708)
* [14e4:165f tg3 eth1: transmit timed out, resetting on BCM5720](https://bugs.launchpad.net/dell-poweredge/+bug/1331513)
* [NETDEV WATCHDOG: eth0 (r8169): transmit queue 0 timed out with Tegra R21](https://devtalk.nvidia.com/default/topic/787949/netdev-watchdog-eth0-r8169-transmit-queue-0-timed-out-with-tegra-r21)
* [Ubuntu freeze due to bug in tg3 driver for Broadcom NIC (?)](https://www.claudiokuenzler.com/blog/476/system-freeze-kernel-bug-tg3-driver-broadcom-tg3_stop_block)

There were a couple of suggestions across the different sites and here are the ones I tried.

#### Changing to 100Mbps vs 1000Mbps Speed

At first I tried using *mii-tool* but that didn't work for me:

	~ $ sudo mii-tool -v enp1s0f0
	 negotiated 1000baseT-FD flow-control, link ok
	  product info: vendor 00:d8:97, model 36 rev 0
	  basic mode:   autonegotiation enabled
	  basic status: autonegotiation complete, link ok
	  capabilities: 1000baseT-HD 1000baseT-FD 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD
	  advertising:  1000baseT-HD 1000baseT-FD 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD flow-control
	  link partner: 1000baseT-FD 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD flow-control
	
	~ $ sudo mii-tool -F 100baseTx-FD enp1s0f0

But when I ran that, the NIC just reset back to using 1000Mbps:

	Aug 27 09:08:27 core systemd-networkd[860]: enp1s0f0: Lost carrier
	Aug 27 09:08:27 core systemd-timesyncd[682]: Network configuration changed, trying to establish connection.
	Aug 27 09:08:30 core kernel: tg3 0000:01:00.0 enp1s0f0: Link is up at 1000 Mbps, full duplex
	Aug 27 09:08:30 core kernel: tg3 0000:01:00.0 enp1s0f0: Flow control is on for TX and on for RX
	Aug 27 09:08:30 core kernel: tg3 0000:01:00.0 enp1s0f0: EEE is disabled
	Aug 27 09:08:30 core systemd-networkd[860]: enp1s0f0: Gained carrier


So then I ran the following to apply that and it worked:

	~ $ sudo ethtool -s enp1s0f0 speed 100 duplex full

I saw the following in **dmesg**:

	Aug 27 09:10:18 core kernel: tg3 0000:01:00.0 enp1s0f0: Link is down
	Aug 27 09:10:19 core systemd-networkd[860]: enp1s0f0: Lost carrier
	Aug 27 09:10:22 core kernel: tg3 0000:01:00.0 enp1s0f0: Link is up at 100 Mbps, full duplex
	Aug 27 09:10:22 core kernel: tg3 0000:01:00.0 enp1s0f0: Flow control is on for TX and on for RX
	Aug 27 09:10:22 core kernel: tg3 0000:01:00.0 enp1s0f0: EEE is disabled
	Aug 27 09:10:22 core systemd-networkd[860]: enp1s0f0: Gained carrier
	Aug 27 09:10:22 core systemd-networkd[860]: enp1s0f0: Configured


After leaving that on for a little bit, the issue reoccured again.

#### Disable TSO (TCP Segmentation Offload)
By default the NIC Settings looked like this:

	~ $ sudo ethtool -k enp1s0f0
	Features for enp1s0f0:
	rx-checksumming: on
	tx-checksumming: on
	        tx-checksum-ipv4: on
	        tx-checksum-ip-generic: off [fixed]
	        tx-checksum-ipv6: on
	        tx-checksum-fcoe-crc: off [fixed]
	        tx-checksum-sctp: off [fixed]
	scatter-gather: on
	        tx-scatter-gather: on
	        tx-scatter-gather-fraglist: off [fixed]
	tcp-segmentation-offload: on
	        tx-tcp-segmentation: on
	        tx-tcp-ecn-segmentation: on
	        tx-tcp-mangleid-segmentation: off
	        tx-tcp6-segmentation: on
	udp-fragmentation-offload: off [fixed]
	generic-segmentation-offload: on
	generic-receive-offload: on
	large-receive-offload: off [fixed]
	rx-vlan-offload: on [fixed]
	tx-vlan-offload: on [fixed]
	ntuple-filters: off [fixed]
	receive-hashing: off [fixed]
	highdma: on
	rx-vlan-filter: off [fixed]
	vlan-challenged: off [fixed]
	tx-lockless: off [fixed]
	netns-local: off [fixed]
	tx-gso-robust: off [fixed]
	tx-fcoe-segmentation: off [fixed]
	tx-gre-segmentation: off [fixed]
	tx-gre-csum-segmentation: off [fixed]
	tx-ipxip4-segmentation: off [fixed]
	tx-ipxip6-segmentation: off [fixed]
	tx-udp_tnl-segmentation: off [fixed]
	tx-udp_tnl-csum-segmentation: off [fixed]
	tx-gso-partial: off [fixed]
	tx-sctp-segmentation: off [fixed]
	tx-esp-segmentation: off [fixed]
	fcoe-mtu: off [fixed]
	tx-nocache-copy: off
	loopback: off [fixed]
	rx-fcs: off [fixed]
	rx-all: off [fixed]
	tx-vlan-stag-hw-insert: off [fixed]
	rx-vlan-stag-hw-parse: off [fixed]
	rx-vlan-stag-filter: off [fixed]
	l2-fwd-offload: off [fixed]
	hw-tc-offload: off [fixed]
	esp-hw-offload: off [fixed]
	esp-tx-csum-hw-offload: off [fixed]

So to disable TSO I ran the following:

	~ $ sudo ethtool -K enp1s0f0 tso off

And you can run the following to confirm:

	~ $ sudo ethtool -k enp1s0f0 | grep 'tcp.*segmentation'
	tcp-segmentation-offload: off
	        tx-tcp-segmentation: off
	        tx-tcp-ecn-segmentation: off
	        tx-tcp-mangleid-segmentation: off
	        tx-tcp6-segmentation: off

That didn't help.

#### Disable GSO (Generic Segmentation Offload)

Tried both of these:

	~ $ sudo ethtool -K enp1s0f0 gso off
	~ $ sudo ethtool -K enp1s0f0 gro off

And I saw it disabled:

	~ $ sudo ethtool -k enp1s0f0 | grep generic
	generic-segmentation-offload: off
	generic-receive-offload: off

Didn't help either :(

#### Disable SG (Scatter Gather)

To do that I ran the following:

	~ $ sudo ethtool -K enp1s0f0 sg off

And it was off:

	~ $ sudo ethtool -k enp1s0f0 | grep scatter 
	scatter-gather: off
	        tx-scatter-gather: off
	        tx-scatter-gather-fraglist: off [fixed]

And same result again.

### Using a Thunderbolt to Ethernet Adapter
To rule out any hardware issues, I plugged in an Thunderbolt to Ethernet adapter and switched the CoreOS **cloud-init** config to set that adapter up on boot:

	 ~ # grep ens9.net -A 6 /var/lib//coreos-install/user_data
	    - name: 00-ens9.network
	      runtime: true
	      content: |
	        [Match]
	        Name=ens9
	        [Network]
	        DNS=192.168.1.1

And after rebooting the new NIC was setup and running, and the issue went away as well. I guess I had a faulty built-in NIC.
