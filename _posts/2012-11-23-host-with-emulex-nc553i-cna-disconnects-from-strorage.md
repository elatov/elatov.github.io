---
title: ESX(i) Host with Emulex NC553i CNA Disconnects from Strorage
author: Karim Elatov
layout: post
permalink: /2012/11/host-with-emulex-nc553i-cna-disconnects-from-strorage/
categories: ['storage', 'vmware']
tags: ['cna', 'did_requeue', 'fcoe', 'emulex']
---

I was experiencing a lot of disconnects from my storage over FCoE when using HP Blades with a NC553i CNA card. During the issue, I would see the following in the logs:


	2012-11-01T04:12:00.960Z cpu17:4113)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x28 (0x41244109c100, 12535) to dev "naa.xxx" on path "vmhba2:C0:T0:L6" Failed: H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0. Act:NONE
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x41244109c100) 0x28, CmdSN 0x8000006c from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x2a (0x4124403c11c0, 12535) to dev "naa.xxx" on path "vmhba2:C0:T0:L6" Failed: H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0. Act:NONE
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x4124403c11c0) 0x2a, CmdSN 0x80000025 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x4124403ce1c0) 0x2a, CmdSN 0x80000005 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x41244109c400) 0x2a, CmdSN 0x80000072 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:01.299Z cpu2:12086)HBX: 2313: Waiting for timed out [HB state abcdef02 offset 3964928 gen 59 stampUS 6780917733 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 60558> drv 14.54] on vol 'Datastore'
	2012-11-01T04:12:16.969Z cpu12:4108)ScsiDeviceIO: 2322: Cmd(0x4124403ab000) 0x16, CmdSN 0x2646 from world 0 to dev "naa.xxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:16.969Z cpu12:4132)WARNING: HBX: 2697: Reclaiming timed out [HB state abcdef02 offset 3964928 gen 33 stampUS 6516761891 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 511743> drv 14.54] on vol 'Datastore' failed: Timeout
	...
	...
	2012-11-01T04:12:47.511Z cpu8:4132)FS3Misc: 1440: Long VMFS3 rsv time on 'Datastore' (held for 6441 msecs). # R: 1, # W: 1 bytesXfer: 2 sectors


Issue begins with SCSI commands failing with a host status of 0xb (H:0xb):


	2012-11-01T04:12:00.960Z cpu17:4113)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x28 (0x41244109c100, 12535) to dev "naa.xxx" on path "vmhba2:C0:T0:L6" Failed: H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0. Act:NONE


The H:0xb status means DID_REQUEUE, which means the Emulex driver has re-issued the failed command. Check out VMware KB [1029039](https://knowledge.broadcom.com/external/article?legacyId=1029039) for more information on SCSI sense codes.

SCSI commands continue to fail with no fail-over condition reported by the HBA to the ESX multipathing stack.


	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x41244109c100) 0x28, CmdSN 0x8000006c from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x2a (0x4124403c11c0, 12535) to dev "naa.xxx" on path "vmhba2:C0:T0:L6" Failed: H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0. Act:NONE
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x4124403c11c0) 0x2a, CmdSN 0x80000025 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x4124403ce1c0) 0x2a, CmdSN 0x80000005 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:00.960Z cpu17:4113)ScsiDeviceIO: 2309: Cmd(0x41244109c400) 0x2a, CmdSN 0x80000072 from world 12535 to dev "naa.xxx" failed H:0xb D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	2012-11-01T04:12:01.299Z cpu2:12086)HBX: 2313: Waiting for timed out [HB state abcdef02 offset 3964928 gen 59 stampUS 6780917733 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 60558> drv 14.54] on vol 'Datastore'
	2012-11-01T04:12:16.969Z cpu12:4108)ScsiDeviceIO: 2322: Cmd(0x4124403ab000) 0x16, CmdSN 0x2646 from world 0 to dev "naa.xxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.


then eventually the IO times out


	2012-11-01T04:12:41.069Z cpu8:4133)WARNING: HBX: 2697: Reclaiming timed out [HB state abcdef02 offset 3964928 gen 59 stampUS 6780917733 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 60558> drv 14.54] on vol 'Datastore' failed: Timeout
	2012-11-01T04:12:41.070Z cpu2:12086)HBX: 2313: Waiting for timed out [HB state abcdef02 offset 3964928 gen 59 stampUS 6780917733 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 60558> drv 14.54] on vol 'Datastore'
	2012-11-01T04:12:47.511Z cpu8:4132)HBX: 231: Reclaimed heartbeat for volume 4e203815-40b2561a-dd72-0017a477003a (Datastore): [Timeout] [HB state abcdef02 offset 3964928 gen 59 stampUS 6827469158 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB$
	2012-11-01T04:12:47.511Z cpu8:4132)FS3Misc: 1440: Long VMFS3 rsv time on 'Datastore' (held for 6441 msecs). # R: 1, # W: 1 bytesXfer: 2 sectors
	2012-11-01T04:12:47.553Z cpu16:4131)HBX: 231: Reclaimed heartbeat for volume 5009333b-b7a2d1f8-fc26-e4115bb4a813 (Datastore): [Timeout] [HB state abcdef02 offset 3964928 gen 33 stampUS 6827510529 uuid 5091de63-2683f5a0-1ea1-e4115baf243b jrnl <FB 51$


There is a known issue with the Emulex firmware, I ran into [this](https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5215333&docId=emr_na-c03400156-1&lang=en-us&cc=us) HP Advisory which had the following:

> HP Converged Network Adapters - Firmware update required for network adapters to avoid FCoE multipath recovery issues

The firmware fixes another issue as well:

> Firmware version 4.1.402.20 for the HP NC551m, NC553m, NC553i, NC551i, NC550SFP, NC552SFP, NC550m, NC552m, 554FLB, 554FLR-SFP+, 552M, 554M, CN1000E, CN1100E 10 GbE Converged Network Adapters is required to prevent FCoE multipath recovery issues and DMA conflicts on Gen8 ProLiant servers
> ...
> ...
> DMA conflicts with the Emulex Light Pulse Fibre Channel (LPFC) driver on Proliant Gen8 series servers that may cause the adapter to stop responding.

Just download the Firmware from the advisory page and install it. After installing the firmware, the disconnects stopped occurring.
