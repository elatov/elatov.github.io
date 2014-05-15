---
title: Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0
author: Karim Elatov
layout: post
permalink: /2014/01/installing-lsi-cim-providers-megaraid-8704elp-local-controller-esxi/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2094574279
categories:
  - Home Lab
  - Storage
  - VMware
tags:
  - LSI
  - veeam
  - VMware
---
I wanted to check the status of the local LSI controller in the vSphere Client. Going to the **Health Status** Tab and checking the **Sensor** information, I didn't see any Storage Sensors:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-sensors-esxi.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-sensors-esxi.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-sensors-esxi.png" alt="cim sensors esxi Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="573" height="238" class="alignnone size-full wp-image-9942" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

### LSI Local Controller

Checking out the model of the local controller I saw the following information on the ESXi host:

    ~ # esxcli storage core  adapter list | grep vmhba0
    vmhba0    megaraid_sas  link-n/a    unknown.vmhba0                       (0:4:0.0) LSI / Symbios Logic LSI MegaRAID SAS 1078 Controller
    

Checking out the information about one of the local disks yielded a little bit information:

    ~ # esxcli storage core device list -d naa.600605b001f819701a2d10d113694cbf
    naa.600605b001f819701a2d10d113694cbf
       Display Name: Local LSI Disk (naa.600605b001f819701a2d10d113694cbf)
       Has Settable Display Name: true
       Size: 569344
       Device Type: Direct-Access
       Multipath Plugin: NMP
       Devfs Path: /vmfs/devices/disks/naa.600605b001f819701a2d10d113694cbf
       Vendor: LSI
       Model: MegaRAID 8704ELP
       Revision: 1.40
       SCSI Level: 5
       Is Pseudo: false
       Status: on
       Is RDM Capable: false
       Is Local: true
       Is Removable: false
       Is SSD: false
       Is Offline: false
       Is Perennially Reserved: false
       Thin Provisioning Status: unknown
       Attached Filters:
       VAAI Status: unsupported
       Other UIDs: vml.0200000000600605b001f819701a2d10d113694cbf4d6567615241
    

So the **LSI MegaRAID SAS 1078 Controller** is basically the same thing as the **MegaRAID 8704ELP** Model. Apparently the **Dell Perc 5i** does similar re-branding, more on that at <a href="http://vmsysadmin.wordpress.com/2011/12/09/using-perc-5i-with-esxi-5-2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmsysadmin.wordpress.com/2011/12/09/using-perc-5i-with-esxi-5-2/']);">Using Perc 5i with ESXi 5</a>.

### Getting LSI CIM Providers

Checking out the LSI site for that card, there was no CIM providers:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-mgmt-tools.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-mgmt-tools.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-mgmt-tools.png" alt="lsi mgmt tools Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="699" height="393" class="alignnone size-full wp-image-9943" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

It only had the MegaCLI tool for VMware. I ran into a couple of site and they actually used older CIM providers which worked out:

*   <a href="http://vmsysadmin.wordpress.com/2011/12/09/using-perc-5i-with-esxi-5-2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmsysadmin.wordpress.com/2011/12/09/using-perc-5i-with-esxi-5-2/']);">Using Perc 5i with ESXi 5</a>
*   <a href="https://communities.vmware.com/thread/421847" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/421847']);">Monitoring LSI (Russian)</a>

So I downloaded <a href="http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/00_32_V0_02_SMIS_VMware_Installer.zip" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/00_32_V0_02_SMIS_VMware_Installer.zip']);">VMWare SMIS Provider VIB - 5.4</a> and then installed the file.

### Installing VIB on ESXi 5.x

After you download the file, you will have a *zip* archive, here are the contents of the file:

    $ unzip -l 00_32_V0_02_SMIS_VMware_Installer.zip
    Archive:  00_32_V0_02_SMIS_VMware_Installer.zip
      Length      Date    Time    Name
    ---------  ---------- -----   ----
         3611  2012-10-08 10:02   00_32_V0_02_SMIS_VMware_Installer.txt
            0  2012-10-08 09:45   00.32.V0.02/docs/
         3020  2012-09-21 15:25   00.32.V0.02/docs/bulletin.xml
         5677  2012-09-21 15:25   00.32.V0.02/docs/descriptor.xml
         2289  2012-09-21 15:25   00.32.V0.02/docs/Installation.txt
      1286484  2012-09-21 15:25   00.32.V0.02/docs/InternalRAID_13.mof
      7105590  2012-09-21 15:25   00.32.V0.02/vmware-esx-provider-lsiprovider.vib
    ---------                     -------
      8406671                     7 files
    

We just need the **VIB** file. So **scp** the file onto the ESXi server:

    $ scp 00.32.V0.02/vmware-esx-provider-lsiprovider.vib esx:/tmp/.
    

Then **ssh** into the ESXi machine and run the following:

    ~ # esxcli software vib install -v /tmp/vmware-esx-provider-lsiprovider.vib --no-sig-check
    Installation Result
       Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
       Reboot Required: true
       VIBs Installed: LSI_bootbank_lsiprovider_500.04.V0.32-0003
       VIBs Removed:
       VIBs Skipped:
    

I then reboot the ESXi host. After the reboot I went back to the **Health Status** tab and saw the LSI Storage Controller information:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-seen-sensors.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-seen-sensors.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/lsi-seen-sensors.png" alt="lsi seen sensors Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="815" height="434" class="alignnone size-full wp-image-9944" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

The Hard Drive information seems wrong (*Unconfigured Good*) but the rest of the information is good. I came across <a href="http://blog.rebelit.net/432" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.rebelit.net/432']);">ESXi 5.1 Dell PERC 6i Health Status Monitoring</a> and the issue is similar in the post. The issue can be fixed by downgrading to lower versions of the LSI CIM Providers.

### Uninstall VIB on ESXi 5.0

I decided to try out the <a href="http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/VMW-ESX-5.0.0-LSIProvider-500.04.V0.24-261033-456178.zip" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/VMW-ESX-5.0.0-LSIProvider-500.04.V0.24-261033-456178.zip']);">v24</a> of the LSI CIM providers. First I removed the v32 Providers, this is done by finding the name of VIB:

    ~ # esxcli software vib list | head -3
    Name                        Version                             Vendor  Acceptance Level  Install Date
    --------------------------  ----------------------------------  ------  ----------------  ------------
    lsiprovider                 500.04.V0.32-0003                   LSI     VMwareAccepted    2014-01-03  
    

Then to remove, just run the following:

    ~ # esxcli software vib remove -n lsiprovider
    

After it's removed, I rebooted and installed v24 providers:

    ~ # esxcli software vib install -v /tmp/vmware-esx-provider-LSIProvider.vib 
    Installation Result
       Message: The update completed successfully, but the system needs to be reboot
    ed for the changes to be effective.
       Reboot Required: true
       VIBs Installed: LSI_bootbank_LSIProvider_500.04.V0.24-261033
       VIBs Removed: 
       VIBs Skipped: 
    

Another reboot and I saw the following under the **Health Status** tab:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-health-status-lsi-24.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-health-status-lsi-24.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/cim-health-status-lsi-24.png" alt="cim health status lsi 24 Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="885" height="240" class="alignnone size-full wp-image-9946" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

Since the controller didn't have a battery (and the status was **unknown**), CIM was throwing an alert. I then ran across <a href="http://www.thomas-krenn.com/en/wiki/Monitoring_LSI_RAID_Controllers_in_VMware" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.thomas-krenn.com/en/wiki/Monitoring_LSI_RAID_Controllers_in_VMware']);">Monitoring LSI RAID Controllers in VMware</a>, and it mentioned that it was known issue and should be fixed in later CIM Providers. So then I installed <a href="http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/00.03.V0.03_SMIS_VMware_Installer.zip" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/00.03.V0.03_SMIS_VMware_Installer.zip']);">v30</a> of the LSI CIM Providers (after I removed v24):

    ~ # esxcli software vib install -v /tmp/vmware-esx-provider-lsiprovider.vib  --no-sig-check
    Installation Result
       Message: The update completed successfully, but the system needs to be reboot
    ed for the changes to be effective.
       Reboot Required: true
       VIBs Installed: LSI_bootbank_lsiprovider_500.04.V0.30-3000000
       VIBs Removed: 
       VIBs Skipped: 
    

and then my sensors looked like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/health-status-lsi-30.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/health-status-lsi-30.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/health-status-lsi-30.png" alt="health status lsi 30 Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="836" height="283" class="alignnone size-full wp-image-9947" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

That looked better, so I stuck with **v30 LSI CIM Providers** for the **MegaRAID 8704ELP** controller.

### Installing MegaCLI on ESXi 5.x

This was available for my card from the LSI site. I downloaded <a href="http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/8.07.07_MegaCLI.zip" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/8.07.07_MegaCLI.zip']);">MegaCLI 5.5 P1</a> zip file and then checked out the contents:

    $ unzip -l 8.07.07_MegaCLI.zip
    Archive:  8.07.07_MegaCLI.zip
      Length      Date    Time    Name
    ---------  ---------- -----   ----
      1419652  2013-02-12 16:40   windows/MegaCli_windows.zip
       760446  2012-11-21 10:22   DOS/MegaCLI.exe
            0  2013-03-02 10:30   EFI/MegaCli_EFI/
      1235008  2012-11-22 14:38   EFI/MegaCli_EFI/MegaCli.efi
            0  2013-03-02 10:30   EFI/MegaCli_EfiHostCli/
        54272  2012-03-13 11:46   EFI/MegaCli_EfiHostCli/EfiHostCli.efi
       888346  2012-12-19 15:43   freebsd/MegaCLI.zip
       936600  2012-12-19 15:41   freebsd/MegaCli64.zip
      1537768  2012-12-19 15:26   linux/MegaCli-8.07.07-1.noarch.rpm
      5143203  2013-02-24 12:02   solaris/MegaCli_Solaris.zip
       620726  2012-12-19 15:26   Vmware/MegaCLI.zip
       753560  2012-12-19 15:57   VmwareMN/vmware-esx-MegaCli-8.07.07.vib
        46023  2013-03-02 10:42   8.07.07_MegaCLI.txt
    ---------                     -------
     13395604                     13 files
    

We can grab the VIB again and copy it to our ESXi machine:

    $ scp VmwareMN/vmware-esx-MegaCli-8.07.07.vib esx:/tmp
    

Then **ssh**'ed into the ESXi host again and ran the following to install it:

    # esxcli software vib install -v /tmp/vmware-esx-MegaCli-8.07.07.vib --no-sig-check
    Installation Result
       Message: Operation finished successfully.
       Reboot Required: false
       VIBs Installed: LSI_bootbank_vmware-esx-MegaCli-8.07.07_8.07.07-01
       VIBs Removed:
       VIBs Skipped:
    

Running the command yielded at error at first:

    ~ # /opt/lsi/MegaCLI/MegaCli -LDInfo -Lall -aALL
    ./libstorelib.so: cannot open shared object file: No such file or directory
    Exit Code: 0x01
    

Looking for that library, I found it here:

    ~ # find . -name libstorelib.so
    ./usr/lib/cim/libstorelib.so
    ./opt/lsi/MegaCLI/libstorelib.so
    

So then running the following helped out:

    ~ # LD_LIBRARY_PATH=/opt/lsi/MegaCLI /opt/lsi/MegaCLI/MegaCli -LDInfo -Lall -aALL
    
    Adapter 0 -- Virtual Drive Information:
    Virtual Drive: 0 (Target Id: 0)
    Name                :
    RAID Level          : Primary-1, Secondary-0, RAID Level Qualifier-0
    Size                : 67.054 GB
    Sector Size         : 512
    Mirror Data         : 67.054 GB
    State               : Optimal
    Strip Size          : 64 KB
    Number Of Drives    : 2
    Span Depth          : 1
    Default Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Current Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Default Access Policy: Read/Write
    Current Access Policy: Read/Write
    Disk Cache Policy   : Enabled
    Encryption Type     : None
    Is VD Cached: No
    
    Virtual Drive: 1 (Target Id: 1)
    Name                :
    RAID Level          : Primary-0, Secondary-0, RAID Level Qualifier-0
    Size                : 556.0 GB
    Sector Size         : 512
    Parity Size         : 0
    State               : Optimal
    Strip Size          : 64 KB
    Number Of Drives    : 2
    Span Depth          : 1
    Default Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Current Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Default Access Policy: Read/Write
    Current Access Policy: Read/Write
    Disk Cache Policy   : Enabled
    Encryption Type     : None
    Is VD Cached: No
    
    Exit Code: 0x00
    

### Monitoring LSI Raid Status

LSI provides the <a href="http://kb.vmware.com/kb/2004166" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2004166']);">Megaraid Storage Monitor</a> and the install process for that is described in <a href="http://www.omniweb.com/wordpress/?p=636" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.omniweb.com/wordpress/?p=636']);">Configuring alerts with MegaRAID Storage Manager for LSI 9260-4i controller onESXi 5.0</a>. There were a lot of steps in the process and for some reason, I didn't feel like it was worth the trouble (there was also a fix related to multicast vs unicast and it's described in <a href="https://communities.vmware.com/message/2105886#2105886" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/message/2105886#2105886']);">VMware Communities Discussion 2105886</a>). I only had one host, so I didn't have vCenter installed. I wanted to configure alarms like you can in vCenter, but without vCenter. This way I could not only monitor the LSI RAID status but other ESXi related functions as well.

I came across <a href="http://www.veeam.com/virtual-server-management-one-free.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.veeam.com/virtual-server-management-one-free.html']);">Veeam One</a> Free Edition. It's like a little mini-vCenter without all the bells and whistles. It definitely fit my needs: it provided performance graphs and it had a lot of pre-configured alarms which could be sent via an SMTP server. Check out <a href="http://rickrbyrne.wordpress.com/2012/09/22/veeam-one-free-edition-and-more/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://rickrbyrne.wordpress.com/2012/09/22/veeam-one-free-edition-and-more/']);">Veeam One Free Edition and More</a> for a step-by-step install guide. Another cool thing about *Veeam One* is that it can integrate with <a href="http://www.veeam.com/virtual-machine-backup-solution-free.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.veeam.com/virtual-machine-backup-solution-free.html']);">Veeam Backup</a> (there is a free version as well).

After I had setup *Veeam*, I saw the same Hardware Sensors as I did in the vSphere Client:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-hw-monitor.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-hw-monitor.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-hw-monitor.png" alt="veeam hw monitor Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="982" height="654" class="alignnone size-full wp-image-9948" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

#### Test Out Drive Failure

One of the *Virtual Disks* was setup as a RAID-1:

    # ./MegaCli -LDInfo -L0 -a0             
    Adapter 0 -- Virtual Drive Information:
    Virtual Drive: 0 (Target Id: 0)
    Name                :
    RAID Level          : Primary-1, Secondary-0, RAID Level Qualifier-0
    Size                : 67.054 GB
    Sector Size         : 512
    Mirror Data         : 67.054 GB
    State               : Optimal
    Strip Size          : 64 KB
    Number Of Drives    : 2
    Span Depth          : 1
    Default Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Current Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Default Access Policy: Read/Write
    Current Access Policy: Read/Write
    Disk Cache Policy   : Enabled
    Encryption Type     : None
    Is VD Cached: No
    

and here is the information regarding both disks:

    # ./MegaCli -PDInfo -PhysDrv [6:0] -aALL                               
    Enclosure Device ID: 6
    Slot Number: 0
    Drive's position: DiskGroup: 0, Span: 0, Arm: 0
    Enclosure position: N/A
    Device Id: 4
    WWN: 
    Sequence Number: 2
    Media Error Count: 0
    Other Error Count: 0
    Predictive Failure Count: 0
    Last Predictive Failure Event Seq Number: 0
    PD Type: SAS
    
    Raw Size: 68.366 GB [0x88bb998 Sectors]
    Non Coerced Size: 67.866 GB [0x87bb998 Sectors]
    Coerced Size: 67.054 GB [0x861c000 Sectors]
    Sector Size:  0
    Firmware state: Online, Spun Up
    Device Firmware Level: 0005
    Shield Counter: 0
    Successful diagnostics completion on :  N/A
    SAS Address(0): 0x5000c500097b0fdd
    SAS Address(1): 0x0
    Connected Port Number: 0(path0) 
    Inquiry Data: SEAGATE ST973452SS      00053TA1737G            
    FDE Capable: Not Capable
    FDE Enable: Disable
    Secured: Unsecured
    Locked: Unlocked
    Needs EKM Attention: No
    Foreign State: None 
    Device Speed: 6.0Gb/s 
    Link Speed: 3.0Gb/s 
    Media Type: Hard Disk Device
    Drive Temperature :35C (95.00 F)
    PI Eligibility:  No 
    Drive is formatted for PI information:  No
    PI: No PI
    Port-0 :
    Port status: Active
    Port's Linkspeed: 3.0Gb/s 
    Port-1 :
    Port status: Active
    Port's Linkspeed: Unknown 
    Drive has flagged a S.M.A.R.T alert : No
    

Here is the second one:

    # ./MegaCli -PDInfo -PhysDrv [6:1] -aALL                           
    Enclosure Device ID: 6
    Slot Number: 1
    Drive's position: DiskGroup: 0, Span: 0, Arm: 1
    Enclosure position: N/A
    Device Id: 5
    WWN: 
    Sequence Number: 2
    Media Error Count: 0
    Other Error Count: 0
    Predictive Failure Count: 0
    Last Predictive Failure Event Seq Number: 0
    PD Type: SAS
    
    Raw Size: 68.366 GB [0x88bb998 Sectors]
    Non Coerced Size: 67.866 GB [0x87bb998 Sectors]
    Coerced Size: 67.054 GB [0x861c000 Sectors]
    Sector Size:  0
    Firmware state: Online, Spun Up
    Device Firmware Level: 0005
    Shield Counter: 0
    Successful diagnostics completion on :  N/A
    SAS Address(0): 0x5000c500097afd61
    SAS Address(1): 0x0
    Connected Port Number: 1(path0) 
    Inquiry Data: SEAGATE ST973452SS      00053TA173BK            
    FDE Capable: Not Capable
    FDE Enable: Disable
    Secured: Unsecured
    Locked: Unlocked
    Needs EKM Attention: No
    Foreign State: None 
    Device Speed: 6.0Gb/s 
    Link Speed: 3.0Gb/s 
    Media Type: Hard Disk Device
    Drive Temperature :32C (89.60 F)
    PI Eligibility:  No 
    Drive is formatted for PI information:  No
    PI: No PI
    Port-0 :
    Port status: Active
    Port's Linkspeed: 3.0Gb/s 
    Port-1 :
    Port status: Active
    Port's Linkspeed: Unknown 
    Drive has flagged a S.M.A.R.T alert : No
    

So I decided to **offline** the second drive in the Raid:

    # ./MegaCli -PDOffline -PhysDrv [6:1] -a0                                     
    Adapter: 0: EnclId-6 SlotId-1 state changed to OffLine.
    

Of course as soon as I did that the Alarm went off :). So I ran the following to silence that:

    # ./MegaCli -AdpSetProp AlarmSilence -a0                                  
    Adapter 0: Set alarm to Silenced success.
    

Now, as expected, the status of the Raid is **Degraded**:

    ./MegaCli -LDInfo -L0 -a0
    Adapter 0 -- Virtual Drive Information:
    Virtual Drive: 0 (Target Id: 0)
    Name                :
    RAID Level          : Primary-1, Secondary-0, RAID Level Qualifier-0
    Size                : 67.054 GB
    Sector Size         : 512
    Mirror Data         : 67.054 GB
    State               : Degraded
    Strip Size          : 64 KB
    Number Of Drives    : 2
    Span Depth          : 1
    Default Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Current Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Default Access Policy: Read/Write
    Current Access Policy: Read/Write
    Disk Cache Policy   : Enabled
    Encryption Type     : None
    Is VD Cached: No
    

Checking out vSphere client, I now saw *warnings*:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/offlined-disk-cim.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/offlined-disk-cim.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/offlined-disk-cim.png" alt="offlined disk cim Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="636" height="434" class="alignnone size-full wp-image-9949" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

And checking out *Veeam One*, an alarm was fired for that:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-on-hardware-alarm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-on-hardware-alarm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-on-hardware-alarm.png" alt="veeam on hardware alarm Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="867" height="878" class="alignnone size-full wp-image-9950" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

and if an SMTP server is configurde then an email is sent for the corresponding alarm. Then I went ahead and brought the drive back **online**:

    #./MegaCli -PDOnline -PhysDrv [6:1] -a0                   
    EnclId-6 SlotId-1 state changed to OnLine.
    

Then checking the *Virtual Drive* information, I was back to **Optimal**:

    # ./MegaCli -LDInfo -L0 -a0
    Adapter 0 -- Virtual Drive Information:
    Virtual Drive: 0 (Target Id: 0)
    Name                :
    RAID Level          : Primary-1, Secondary-0, RAID Level Qualifier-0
    Size                : 67.054 GB
    Sector Size         : 512
    Mirror Data         : 67.054 GB
    State               : Optimal
    Strip Size          : 64 KB
    Number Of Drives    : 2
    Span Depth          : 1
    Default Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Current Cache Policy: WriteThrough, ReadAheadNone, Direct, No Write Cache if Bad BBU
    Default Access Policy: Read/Write
    Current Access Policy: Read/Write
    Disk Cache Policy   : Enabled
    Encryption Type     : None
    Is VD Cached: No
    

Also checking out the events, I saw the following:

    #./MegaCli -AdpEventLog -GetEvents -f /tmp/events.log -aALL && tail -40 /tmp/events.log
    
    Time: Sat Jan  4 18:22:56 2014
    
    Code: 0x00000072
    Class: 0
    Locale: 0x02
    Event Description: State change on PD 05(e0x06/s1) from OFFLINE(10) to ONLINE(18)
    Event Data:
    ===========
    Device ID: 5
    Enclosure Index: 6
    Slot Number: 1
    Previous state: 16
    New state: 24
    
    
    seqNum: 0x00001283
    Time: Sat Jan  4 18:22:56 2014
    
    Code: 0x00000051
    Class: 0
    Locale: 0x01
    Event Description: State change on VD 00/0 from DEGRADED(2) to OPTIMAL(3)
    Event Data:
    ===========
    Target Id: 0
    Previous state: 2
    New state: 3
    
    
    seqNum: 0x00001284
    Time: Sat Jan  4 18:22:56 2014
    
    Code: 0x000000f9
    Class: 0
    Locale: 0x01
    Event Description: VD 00/0 is now OPTIMAL
    Event Data:
    ===========
    Target Id: 0
    

And the alarm was automatically resolved on the *Veeam* side (and an email sent as well):

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-alarms-back.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-alarms-back.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/01/veeam-alarms-back.png" alt="veeam alarms back Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" width="857" height="554" class="alignnone size-full wp-image-9951" title="Installing LSI CIM Providers for MegaRaid 8704ELP Local Controller on ESXi 5.0" /></a>

and of course the warning was cleared on the vSphere Client side as well. Checking out the logs on the ESXi host, I saw the following:

    ~ # grep megasas /var/log/vmkernel.log 
    2014-01-04T18:03:34.000Z cpu7:2648)<6>megasas_hotplug_work[0]: aen event code 0x0072
    2014-01-04T18:03:34.157Z cpu1:2661)<6>megasas_hotplug_work[0]: aen event code 0x0051
    2014-01-04T18:03:34.157Z cpu1:2661)<6>megasas_hotplug_work[0]: scanning ...
    2014-01-04T18:03:34.203Z cpu2:2661)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:03:34.205Z cpu2:2661)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:03:34.206Z cpu2:2661)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:03:34.208Z cpu2:2661)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:03:35.242Z cpu5:2650)<6>megasas_hotplug_work[0]: aen event code 0x00fb
    2014-01-04T18:22:09.967Z cpu4:2646)<6>megasas_hotplug_work[0]: aen event code 0x0007
    2014-01-04T18:22:19.525Z cpu7:2648)<6>megasas_hotplug_work[0]: aen event code 0x0008
    2014-01-04T18:23:03.797Z cpu2:2647)<6>megasas_hotplug_work[0]: aen event code 0x0072
    2014-01-04T18:23:03.937Z cpu3:2651)<6>megasas_hotplug_work[0]: aen event code 0x0051
    2014-01-04T18:23:03.937Z cpu3:2651)<6>megasas_hotplug_work[0]: scanning ...
    2014-01-04T18:23:03.982Z cpu3:2651)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:23:03.984Z cpu2:2651)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:23:03.986Z cpu2:2651)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:23:03.987Z cpu2:2651)megasas_slave_configure: do not export physical disk devices to upper layer.
    2014-01-04T18:23:05.022Z cpu3:2660)<6>megasas_hotplug_work[0]: aen event code 0x00f9
    

We can see that last event code is **0x00f9**, from the above MegaCLI events, we can see that corresponds to *VirtualDisk is Optimal*. BTW a full list of *megasas* events can be seen in <a href="http://virtuallyhyper.com/wp-content/uploads/2014/01/A_Event_Info.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2014/01/A_Event_Info.pdf']);">this PDF</a>.

