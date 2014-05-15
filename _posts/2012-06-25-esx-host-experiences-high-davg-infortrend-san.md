---
title: ESX Host Experiences High DAVG to an Infortrend SAN
author: Karim Elatov
layout: post
permalink: /2012/06/esx-host-experiences-high-davg-infortrend-san/
dsq_thread_id:
  - 1407480485
categories:
  - Storage
  - VMware
tags:
  - ALUA
  - claimrules
  - davg
  - Infortrend
  - SATP
---
I ran into an interesting issue the other day. We were seeing high DAVG to the SAN. I first wanted to find out if the SAN was on the HCL and I found the SAN <a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=18911&deviceCategory=san&partner=121&keyword=S16&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=18911&deviceCategory=san&partner=121&keyword=S16&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">here</a>. Next I checked the SATP and PSP settings, I saw the following:

	  
	\# esxcli nmp device list -d naa.600d02310008483bOOOOOOOO7ef9583c  
	naa.600d02310008483bOOOOOOOO7ef9583c  
	Device Display Name: IFT iSCSI Disk (naa.600d02310008483bOOOOOOOO7ef9583c)  
	Storage Array Type: VMW\_SATP\_ALUA  
	Storage Array Type Device Config: {implicit\_support=on;explicit\_support=off; explicit\_allow=on;alua\_followover=on;{TPG\_id=1,TPG\_state=AO}}  
	Path Selection Policy: VMW\_PSP\_MRU  
	Path Selection Policy Device Config: Current Path=vmhba37:CO:T1:L6  
	Working Paths: vmhba37:CO:T1:L6
	
	\# esxcli corestorage device list -d na.600d02310008483bOOOOOOOO7ef9583c  
	naa.600d02310008483bOOOOOOOO7ef9583c  
	Display Name: IFT iSCSI Disk (naa.600d02310008483bOOOOOOOO7ef9583c)  
	Size: 1907468  
	Device Type: Direct-Access  
	Multipath Plugin: NMP  
	Devfs Path: /vmfs/devices/disks/naa.600d02310008483bOOOOOOOO7ef9583c  
	Vendor: IFT  
	Model: S16E-G1240  
	Revision: 373S  
	SCSI Level: 4  
	Is Pseudo: false  
	Status: on  
	Is RDM Capable: true  
	Is Local: false  
	Is Removable: false  
	Attached Filters:  
	VAAI Status: unknown  
	Other UIDs: vml.0200060000600d02310008483bOOOOOOOO7ef9583c533136452d47  
	

The main thing that stood out was the fact that the SATP that claimed this LUN was *VMW\_SATP\_ALUA* and the Pathing Policy is *VMW\_PSP\_MRU*. If VMW\_SATP\_ALUA Claimed the device that means the array responded to our SCSI *INQUIRY* with the *TPGS* flag on. More information on how ALUA works can be found in article <a href="http://deinoscloud.wordpress.com/?s=alua" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://deinoscloud.wordpress.com/?s=alua']);">It All Started With This Question…</a>. Checking out all the SATP rules for ALUA, I saw the following:

	  
	~ # esxcli nmp satp listrules -s VMW\_SATP\_ALUA  
	Name Device Vendor Model Driver Transport Options Claim Options Default PSP PSP Options Description  
	VMW\_SATP\_ALUA NETAPP tpgs\_on VMW\_PSP_RR NetApp arrays with ALUA support  
	VMW\_SATP\_ALUA IBM 2810XIV tpgs\_on VMW\_PSP_RR IBM 2810XIV arrays with ALUA support  
	VMW\_SATP\_ALUA tpgs_on Any array with ALUA support  
	

So for SATP the claim option *tpgs_on* is the same as the *TPGS* flag on. The customer logged into his Infortrend account and download the Manual for the array. From the Manual we found the following:

> TPGS (Target Port Group Support) concern:
> 
> Infortrend’s multi-pathing service supports TPGS and is able to designate specific data paths as Active and the non-optimal paths as Passive. With TPGS, most I/Os will be directed through the Active paths instead of the Passive paths. The passive paths only receive data flow in the event of Active path failures.
> 
> The diagram below shows a dual-controller RAID system with multi-pathing cabling:
> 
> 1.  There are 4 data paths between RAID system and host. 2 from controller A and 2 from controller B.
> 2.  A RAID volume is managed by controller A and associated with both controller A and controller B IDs.
> 3.  TPGS recognizes data links from controller A as Active paths and those from controller B as Passive paths.

The Array did have two controllers so ALUA is enabled by default and there is no way to disable it. From the above HCL page the only supported SATP and PSP for that array were *VMW\_SATP\_DEFAULT_AA* and *VMW\_PSP\_FIXED,* respectively. The manual was pretty old and the array is now an A/A array instead of on an A/P array. So we decided to add a new SATP rule to match the above array and mark it as an Active/Active Array instead of an ALUA array. I found VMware KB <a href="http://kb.vmware.com/kb/1026157" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026157']);">1026157</a> which had instructions on how to add a new SATP rule. First we had to determine the vendor and model of the array. That can be done by issuing an *esxcfg-rescan* and then looking at the logs, here is what we saw:

	  
	May 10 18:04:36 vmkernel: 429:22:55:15.800 cpu23:83814135)SCSIScan: 1062: Path 'vmhba37:C0:T1:L7': Type: 0x0, ANSI rev: 4, TPGS: 1 (implicit only)  
	May 10 18:04:36 vmkernel: 429:22:55:15.817 cpu23:83814135)SCSIScan: 1059: Path 'vmhba37:CO:T1:L8': Vendor: 'IFT ' Model: 'S16E-G1240 ' Rev: '373S'  
	May 10 18:04:36 vmkernel: 429:22:55:15.817 cpu23:83814135)SCSIScan: 1062: Path 'vmhba37:CO:T1:L8': Type: OxO, ANSI rev: 4, TPGS: 1 (implicit only)  
	May 10 18:04:36 vmkernel: 429:22:55:15.835 cpu23:83814135)SCSIScan: 1059: Path 'vmhba37:CO:T1:L9': Vendor: 'IFT ' Model: 'S16E-G1240 ' Rev: '373S'  
	May 10 18:04:36 vmkernel: 429:22:55:15.835 cpu23:83814135)SCSIScan: 1062: Path 'vmhba37:CO:T1:L9': Type: OxO, ANSI rev: 4, TPGS: 1 (implicit only)  
	May 10 18:04:36 vmkernel: 429:22:55:15.849 cpu23:83814135)SCSIScan: 1059: Path 'vmhba37:CO:TO:LO': Vendor: 'IFT ' Model: 'S16E-G1240 ' Rev: '3730'  
	May 10 18:04:36 vmkernel: 429:22:55:15.849 cpu23:83814135)SCSIScan: 1062: Path 'vmhba37:CO:TO:LO': Type: Oxd, ANSI rev: 4, TPGS: 1 (implicit only)  
	May 10 18:05:08 shell[83810119]: grep SCSIScan /var/log/messages  
	

From the above output, we put together the following SATP rule for the Array:

	  
	~ # esxcli nmp satp addrule -V 'IFT' -M 'S16E-G1240' -o tpgs\_on -e 'Infortrend' -s VMW\_SATP\_DEFAULT\_AA  
	

We then double checked that the rule has been added:

	  
	~ # esxcli nmp satp listrules -s VMW\_SATP\_DEFAULT_AA | grep IFT  
	VMW\_SATP\_DEFAULT\_AA IFT S16E-G1240 tpgs\_on Infortrend  
	

After that we unclaimed one LUN to make sure it's working:

	  
	~ # esxcli corestorage claiming unclaim -t location -A vmbha37 -C O -T 1 -L 6  
	

To check that the 'unclaim' worked, we try to see if we can get information regarding that LUN and we fail:

	  
	~ # esxcli nmp device list -d naa.600d02310008483bOOOOOOOO7ef9583c  
	Errors:  
	Unknown device naa.600d02310008483bOOOOOOOO7ef9583c  
	

That looks good. As a side note, if you had multiple paths for a LUN you can unclaim them and reclaim them with one big swoop by running the following:

	  
	~ # esxcli corestorage claiming reclaim -d naa.600d02310008483bOOOOOOOO7ef9583c  
	

But I had one path so it didn't make a difference. We then ran an *esxcfg-rescan* to reclaim the device and then double checked the settings to see the following:

	  
	~ # esxcfg-rescan vmhba37  
	~ # esxcli nmp device list -d naa.600d02310008483bOOOOOOOO7ef9583c  
	naa.600d02310008483bOOOOOOOO7ef9583c  
	Device Display Name: IFT iSCSI Disk (naa.600d02310008483bOOOOOOOO7ef9583c)  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type Device Config: SATP\_VMW\_SATP\_DEFAULT\_AA does not support device configuration.  
	Path Selection Policy: VMW\_PSP\_FIXED  
	Path Selection Policy Device Config: {preferred= vmhba37:CO:T1:L6;current= vmhba37:CO:T1:L6}  
	Working Paths: vmhba37:CO:T1:L6  
	

We could've reclaimed all the LUNs by running the following:

	  
	\# for i in \`ls /vmfs/devices/disks/ | grep naa.600d\` ; do esxcli corestorage claiming reclaim -d $i ;done  
	

But I decided to reboot the host to make sure everything worked as expected. After the reboot we saw the following:

	  
	~ # esxcli nmp device list | grep 'Storage Array Type:'  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_LOCAL  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_LOCAL  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	Storage Array Type: VMW\_SATP\_DEFAULT_AA  
	

No SATP of *VMW\_SATP\_ALUA* was seen and the DAVG to the array lowered.

