---
title: VMFS Datastore not Auto-Mounting on an ESX(i) Host because the VMFS Partition is Overwritten
author: Karim Elatov
layout: post
permalink: /2012/09/vmfs-datastore-not-auto-mounting-on-an-esxi-host/
dsq_thread_id:
  - 1408613877
categories:
  - Storage
  - VMware
tags:
  - Dynamic Disks
  - FileSystem ID 42
  - hexdump
  - NTFS
  - partitions
  - SFS
  - vmfs
---
We had two LUNs presented to a host:

	  
	~ # esxcfg-scsidevs -c | grep ^naa  
	naa.600144f0928c010000004fc511ec0001 Direct-Access /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001 102400MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc511ec0001)  
	naa.600144f0928c010000004fc90a3a0001 Direct-Access /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001 133120MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc90a3a0001)  
	

Looking at the volumes that are mounted I saw the following:

	  
	~ # esxcfg-scsidevs -m | grep ^naa  
	naa.600144f0928c010000004fc511ec0001:1 /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001:1 4fc903bb-6298d17d-8417-00505617149e 0 OI_LUN0  
	

So only one of the LUNs was mounted, the other was not. Checking out fdisk for both of the LUNs, I saw the following, for the working one:

	
	
	~ # fdisk -lu /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001
	
	Disk /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001: 107.3 GB, 107374182400 bytes  
	255 heads, 63 sectors/track, 13054 cylinders, total 209715200 sectors  
	Units = sectors of 1 * 512 = 512 bytes
	
	Device Boot Start End Blocks Id System  
	/vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001p1 128 209712509 104856191 fb VMFS  
	

That looks good. The offset is 128 sectors and the File System type is VMFS. If you ever had to recreate a vmfs partition (instructions laid out in VMware KB <a href="http://kb.vmware.com/kb/1002281" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002281']);">1002281</a>), you would tell right away that the above output looks good. Then running the same on the other LUN, I saw the following:

	  
	~ # fdisk -lu /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001
	
	Disk /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001: 139.5 GB, 139586437120 bytes  
	255 heads, 63 sectors/track, 16970 cylinders, total 272629760 sectors  
	Units = sectors of 1 * 512 = 512 bytes
	
	Device Boot Start End Blocks Id System  
	/vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001p1 63 272627069 136313471 42 SFS  
	

That looked a little weird, the Filesystem ID is 42 and the Name is SFS. From the Windows "<a href="http://technet.microsoft.com/en-us/library/cc977219.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technet.microsoft.com/en-us/library/cc977219.aspx']);">Disk Concepts and Troubleshooting</a>" page:

> 0x42 Dynamic disk volume

Windows has two different disk types, basic and dynamic. From "<a href="http://msdn.microsoft.com/en-us/library/windows/desktop/aa363785(v=vs.85).aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://msdn.microsoft.com/en-us/library/windows/desktop/aa363785(v=vs.85).aspx']);">Basic and Dynamic Disks</a>"

> **Basic Disks**  
> Basic disks are the storage types most often used with Windows. The term basic disk refers to a disk that contains partitions, such as primary partitions and logical drives, and these in turn are usually formatted with a file system to become a volume for file storage.  
> ...  
> ...  
> **Dynamic Disks**  
> Dynamic disks provide features that basic disks do not, such as the ability to create volumes that span multiple disks (spanned and striped volumes) and the ability to create fault-tolerant volumes (mirrored and RAID-5 volumes). Like basic disks, dynamic disks can use the MBR or GPT partition styles on systems that support both. All volumes on dynamic disks are known as dynamic volumes. Dynamic disks offer greater flexibility for volume management because they use a database to track information about dynamic volumes on the disk and about other dynamic disks in the computer.

So the partition was of type SFS, I then hexdumped the volume to see what data the LUN contained, and I saw the following:

	  
	~ # hexdump -C /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001 | less  
	00000000 eb 52 90 4e 54 46 53 20 20 20 20 00 02 08 00 00 |.R.NTFS .....|  
	00000010 00 00 00 00 00 f8 00 00 3f 00 ff 00 c5 39 01 00 |........?....9..|  
	00000020 00 00 00 00 80 00 80 00 80 cf a4 02 00 00 00 00 |................|  
	00000030 b9 04 00 00 00 00 00 00 d4 85 00 00 00 00 00 00 |................|  
	00000040 f6 00 00 00 01 00 00 00 d9 01 73 38 30 73 38 22 |..........s80s8"|  
	00000050 00 00 00 00 fa 33 c0 8e d0 bc 00 7c fb b8 c0 07 |.....3.....|....|  
	00000060 8e d8 e8 16 00 b8 00 0d 8e c0 33 db c6 06 0e 00 |..........3.....|  
	00000070 10 e8 53 00 68 00 0d 68 6a 02 cb 8a 16 24 00 b4 |..S.h..hj....$..|  
	00000080 08 cd 13 73 05 b9 ff ff 8a f1 66 0f b6 c6 40 66 |...s......f...@f|  
	00000090 0f b6 d1 80 e2 3f f7 e2 86 cd c0 ed 06 41 66 0f |.....?.......Af.|  
	000000a0 b7 c9 66 f7 e1 66 a3 20 00 c3 b4 41 bb aa 55 8a |..f..f. ...A..U.|  
	000000b0 16 24 00 cd 13 72 0f 81 fb 55 aa 75 09 f6 c1 01 |.$...r...U.u....|  
	000000c0 74 04 fe 06 14 00 c3 66 60 1e 06 66 a1 10 00 66 |t......f...f...f|  
	000000d0 03 06 1c 00 66 3b 06 20 00 0f 82 3a 00 1e 66 6a |....f;. ...:..fj|  
	000000e0 00 66 50 06 53 66 68 10 00 01 00 80 3e 14 00 00 |.fP.Sfh.....>...|  
	000000f0 0f 85 0c 00 e8 b3 ff 80 3e 14 00 00 0f 84 61 00 |........>.....a.|  
	00000100 b4 42 8a 16 24 00 16 1f 8b f4 cd 13 66 58 5b 07 |.B..$.......fX[.|  
	00000110 66 58 66 58 1f eb 2d 66 33 d2 66 0f b7 0e 18 00 |fXfX..-f3.f.....|  
	00000120 66 f7 f1 fe c2 8a ca 66 8b d0 66 c1 ea 10 f7 36 |f......f..f....6|  
	00000130 1a 00 86 d6 8a 16 24 00 8a e8 c0 e4 06 0a cc b8 |......$.........|  
	00000140 01 02 cd 13 0f 82 19 00 8c c0 05 20 00 8e c0 66 |........... ...f|  
	00000150 ff 06 10 00 ff 0e 0e 00 0f 85 6f ff 07 1f 66 61 |..........o...fa|  
	00000160 c3 a0 f8 01 e8 09 00 a0 fb 01 e8 03 00 fb eb fe |................|  
	00000170 b4 01 8b f0 ac 3c 00 74 09 b4 0e bb 07 00 cd 10 |.....<.t........|  
	00000180 eb f2 c3 0d 0a 41 20 64 69 73 6b 20 72 65 61 64 |.....A disk read|  
	00000190 20 65 72 72 6f 72 20 6f 63 63 75 72 72 65 64 00 | error occurred.|  
	000001a0 0d 0a 4e 54 4c 44 52 20 69 73 20 6d 69 73 73 69 |..NTLDR is missi|  
	000001b0 6e 67 00 0d 0a 4e 54 4c 44 52 20 69 73 20 63 6f |ng...NTLDR is co|  
	000001c0 6d 70 72 65 73 73 65 64 00 0d 0a 50 72 65 73 73 |mpressed...Press|  
	000001d0 20 43 74 72 6c 2b 41 6c 74 2b 44 65 6c 20 74 6f | Ctrl+Alt+Del to|  
	000001e0 20 72 65 73 74 61 72 74 0d 0a 00 00 00 00 00 00 | restart........|  
	000001f0 00 00 00 00 00 00 00 00 83 a0 b3 c9 00 00 55 aa |..............U.|  
	00000200 05 00 4e 00 54 00 4c 00 44 00 52 00 04 00 24 00 |..N.T.L.D.R...$.|  
	00000210 49 00 33 00 30 00 00 e0 00 00 00 30 00 00 00 00 |I.3.0......0....|  
	00000220 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	

So yeah, that is Windows NTFS :(. As soon we mentioned that, another administrator said, oh yeah I presented this LUN to a windows machine yesterday... Oops :) We then wanted to check how the mounted vmfs looked like. There is actually a good blog about this "<a href="http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes']);">Understanding VMFS volumes</a>", from that blog:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-header.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-header.png']);"><img class="alignnone size-full wp-image-3571" title="vmfs-hd-header" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-header.png" alt="vmfs hd header VMFS Datastore not Auto Mounting on an ESX(i) Host because the VMFS Partition is Overwritten" width="805" height="430" /></a>

and also this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-vol_name.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-vol_name.png']);"><img class="alignnone size-full wp-image-3572" title="vmfs-hd-vol_name" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/vmfs-hd-vol_name.png" alt="vmfs hd vol name VMFS Datastore not Auto Mounting on an ESX(i) Host because the VMFS Partition is Overwritten" width="809" height="208" /></a>

Checking out our good vmfs volume:

	  
	~ # echo $((0x00110000))  
	1114112  
	~ # hexdump -C -s 1114112 -n 800 /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001  
	00110000 0d d0 01 c0 03 00 00 00 11 00 00 00 02 16 00 00 |................|  
	00110010 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	00110020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 60 01 |................|  
	00110030 44 f0 92 8c 01 00 00 00 4f c5 11 ec 00 01 43 4f |D.......O.....CO|  
	00110040 4d 53 54 41 00 00 00 00 00 00 00 00 00 00 00 00 |MSTA............|  
	00110050 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 fc |................|  
	00110060 e9 ff 18 00 00 00 01 00 00 00 8f 01 00 00 8e 01 |................|  
	00110070 00 00 03 00 00 00 00 00 00 00 00 00 10 01 00 00 |................|  
	00110080 00 00 ba 03 c9 4f 04 31 4a fb f4 54 00 50 56 17 |.....O.1J..T.PV.|  
	00110090 14 9e 2d 12 25 fd 6c c1 04 00 a6 23 29 b1 97 c8 |..-.%.l....#)...|  
	001100a0 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	001100b0 00 00 00 00 00 00 00 00 00 00 c0 a8 00 65 00 00 |.............e..|  
	001100c0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	*  
	00110200 00 00 00 f0 18 00 00 00 90 01 00 00 00 00 00 00 |................|  
	00110210 01 00 00 00 34 66 63 39 30 33 62 61 2d 63 37 30 |....4fc903ba-c70|  
	00110220 31 66 61 62 32 2d 30 35 62 66 2d 30 30 35 30 35 |1fab2-05bf-00505|  
	00110230 36 31 37 31 34 39 65 00 00 00 00 00 00 00 00 00 |617149e.........|  
	00110240 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	00110250 00 00 00 00 ba 03 c9 4f b2 fa 01 c7 bf 05 00 50 |.......O.......P|  
	00110260 56 17 14 9e 01 00 00 00 d2 26 25 fd 6c c1 04 00 |V........&%.l...|  
	00110270 00 00 00 00 8f 01 00 00 00 00 00 00 00 00 00 00 |................|  
	00110280 8e 01 00 00 00 00 00 00 a9 65 2f fd 6c c1 04 00 |.........e/.l...|  
	00110290 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	001102a0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	*  
	

This matches the output of the blog (our UUID is '4fc903ba-c701fab2-05bf-00505617149e'). Then looking for the volume name in the VMFS LUN, we saw the following:

	  
	~ # echo $((0x01310000))  
	19988480  
	~ # hexdump -C -s 19988480 -n 64 /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001  
	01310000 5e f1 ab 2f 04 00 00 00 2e bb 03 c9 4f 7d d1 98 |^../........O}..|  
	01310010 62 17 84 00 50 56 17 14 9e 02 00 00 00 4f 49 5f |b...PV.......OI_|  
	01310020 4c 55 4e 30 00 00 00 00 00 00 00 00 00 00 00 00 |LUN0............|  
	01310030 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |................|  
	01310040  
	

From the above output we saw the our mounted VMFS LUN was called "OI_LUN0", and we saw that same volume name in the hexdump. Checking for the same information in the other VMFS volume didn't yield any VMFS information.

	  
	~ # hexdump -C -s 1114112 -n 800 /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001  
	00110000 49 4e 44 58 28 00 09 00 62 e6 4e 02 00 00 00 00 |INDX(...b.N.....|  
	00110010 2e 00 00 00 00 00 00 00 28 00 00 00 18 08 00 00 |........(.......|  
	00110020 e8 0f 00 00 00 00 00 00 13 03 01 00 01 00 66 00 |..............f.|  
	00110030 00 00 ca 01 c8 01 61 00 00 00 00 00 00 00 00 00 |......a.........|  
	00110040 8a 06 00 00 00 00 01 00 68 00 56 00 00 00 00 00 |........h.V.....|  
	00110050 1d 00 00 00 00 00 01 00 00 58 a8 19 ba 9d c8 01 |.........X......|  
	00110060 00 58 a8 19 ba 9d c8 01 74 88 36 aa 44 80 ca 01 |.X......t.6.D...|  
	00110070 38 e5 06 52 40 6b cd 01 00 d0 00 00 00 00 00 00 |8..R@k..........|  
	00110080 00 ca 00 00 00 00 00 00 20 00 00 00 00 00 00 00 |........ .......|  
	00110090 0a 03 6d 00 69 00 67 00 70 00 77 00 64 00 2e 00 |..m.i.g.p.w.d...|  
	001100a0 65 00 78 00 65 00 76 00 c0 0a 00 00 00 00 01 00 |e.x.e.v.........|  
	001100b0 70 00 5a 00 00 00 00 00 1d 00 00 00 00 00 01 00 |p.Z.............|  
	001100c0 00 58 a8 19 ba 9d c8 01 00 58 a8 19 ba 9d c8 01 |.X.......X......|  
	001100d0 7e 2d 26 78 44 73 ca 01 38 e5 06 52 40 6b cd 01 |~-&xDs..8..R@k..|  
	001100e0 00 80 00 00 00 00 00 00 00 74 00 00 00 00 00 00 |.........t......|  
	001100f0 20 00 00 00 00 00 00 00 0c 03 6d 00 69 00 6d 00 | .........m.i.m.|  
	00110100 65 00 66 00 69 00 6c 00 74 00 2e 00 64 00 6c 00 |e.f.i.l.t...d.l.|  
	00110110 6c 00 00 00 00 00 01 00 e4 03 00 00 00 00 01 00 |l...............|  
	00110120 68 00 54 00 00 00 00 00 1d 00 00 00 00 00 01 00 |h.T.............|  
	00110130 00 58 a8 19 ba 9d c8 01 00 58 a8 19 ba 9d c8 01 |.X.......X......|  
	00110140 7e 2d 26 78 44 73 ca 01 ec a9 0b 52 40 6b cd 01 |~-&xDs.....R@k..|  
	00110150 00 50 0a 00 00 00 00 00 40 45 0a 00 00 00 00 00 |.P......@E......|  
	00110160 20 00 00 00 00 00 00 00 09 03 6d 00 6c 00 61 00 | .........m.l.a.|  
	00110170 6e 00 67 00 2e 00 64 00 61 00 74 00 72 00 76 00 |n.g...d.a.t.r.v.|  
	00110180 c2 0a 00 00 00 00 01 00 68 00 54 00 00 00 00 00 |........h.T.....|  
	00110190 1d 00 00 00 00 00 01 00 00 58 a8 19 ba 9d c8 01 |.........X......|  
	001101a0 00 58 a8 19 ba 9d c8 01 7e 2d 26 78 44 73 ca 01 |.X......~-&xDs..|  
	001101b0 7e c4 61 db 6a 6e cd 01 00 00 09 00 00 00 00 00 |~.a.jn..........|  
	001101c0 00 f2 08 00 00 00 00 00 20 00 00 00 00 00 00 00 |........ .......|  
	001101d0 09 03 6d 00 6c 00 61 00 6e 00 67 00 2e 00 64 00 |..m.l.a.n.g...d.|  
	001101e0 6c 00 6c 00 6c 00 76 00 e5 03 00 00 00 00 01 00 |l.l.l.v.........|  
	001101f0 68 00 56 00 00 00 00 00 1d 00 00 00 00 00 13 03 |h.V.............|  
	00110200 00 58 a8 19 ba 9d c8 01 00 58 a8 19 ba 9d c8 01 |.X.......X......|  
	00110210 d8 8f 28 78 44 73 ca 01 fa d0 12 52 40 6b cd 01 |..(xDs.....R@k..|  
	00110220 00 10 00 00 00 00 00 00 00 0e 00 00 00 00 00 00 |................|  
	00110230 20 00 00 00 00 00 00 00 0a 03 6d 00 6c 00 6c 00 | .........m.l.l.|  
	00110240 5f 00 68 00 70 00 2e 00 64 00 6c 00 6c 00 76 00 |_.h.p...d.l.l.v.|  
	00110250 e6 03 00 00 00 00 01 00 68 00 58 00 00 00 00 00 |........h.X.....|  
	00110260 1d 00 00 00 00 00 01 00 00 58 a8 19 ba 9d c8 01 |.........X......|  
	00110270 00 58 a8 19 ba 9d c8 01 d8 8f 28 78 44 73 ca 01 |.X........(xDs..|  
	00110280 fa d0 12 52 40 6b cd 01 00 20 00 00 00 00 00 00 |...R@k... ......|  
	00110290 00 1e 00 00 00 00 00 00 20 00 00 00 00 00 00 00 |........ .......|  
	001102a0 0b 03 6d 00 6c 00 6c 00 5f 00 6d 00 74 00 66 00 |..m.l.l._.m.t.f.|  
	001102b0 2e 00 64 00 6c 00 6c 00 e7 03 00 00 00 00 01 00 |..d.l.l.........|  
	001102c0 68 00 58 00 00 00 00 00 1d 00 00 00 00 00 01 00 |h.X.............|  
	001102d0 00 58 a8 19 ba 9d c8 01 00 58 a8 19 ba 9d c8 01 |.X.......X......|  
	001102e0 d8 8f 28 78 44 73 ca 01 fa d0 12 52 40 6b cd 01 |..(xDs.....R@k..|  
	001102f0 00 20 00 00 00 00 00 00 00 16 00 00 00 00 00 00 |. ..............|  
	00110300 20 00 00 00 00 00 00 00 0b 03 6d 00 6c 00 6c 00 | .........m.l.l.|  
	00110310 5f 00 71 00 69 00 63 00 2e 00 64 00 6c 00 6c 00 |_.q.i.c...d.l.l.|  
	00110320  
	

I definitely don't see a UUID, and checking out the section where the VMFS Volume Name resides:

	  
	~ # hexdump -C -s 19988480 -n 64 /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001  
	01310000 46 49 4c 45 30 00 03 00 be b9 08 0d 00 00 00 00 |FILE0...........|  
	01310010 74 00 01 00 38 00 01 00 58 01 00 00 00 04 00 00 |t...8...X.......|  
	01310020 00 00 00 00 00 00 00 00 05 00 00 00 5c 39 00 00 |............\9..|  
	01310030 49 00 00 00 00 00 00 00 10 00 00 00 60 00 00 00 |I...............|  
	01310040  
	

The VMFS file system was overwritten with some random data. Luckily there was just one VM running on that VMFS Datastore, so we used VMware Converter to P2V the VM and all the data was okay.

