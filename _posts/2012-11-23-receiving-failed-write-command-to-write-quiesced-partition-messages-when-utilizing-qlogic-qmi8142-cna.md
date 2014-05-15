---
title: 'Receiving " Failed write command to write-quiesced partition" Messages When Utilizing Qlogic QMI8142 CNA'
author: Karim Elatov
layout: post
permalink: /2012/11/receiving-failed-write-command-to-write-quiesced-partition-messages-when-utilizing-qlogic-qmi8142-cna/
dsq_thread_id:
  - 1404672902
categories:
  - Storage
  - VMware
tags:
  - FCoE
  - HS22V
  - ibm
  - interrupt remmaping
  - MSI-X
  - qlogic
  - QMI8142
---
I was seeing the following in the logs:

    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 2012-11-12T13:23:50.765Z cpu2:5000)ScsiDeviceIO: 2291: Cmd(0x4124011f9b40) 0x28, CmdSN 0x405e from world 5000 to dev "naa.xxx" failed H:0x8 D:0x0 P:0x0 
    2012-11-12T13:23:50.765Z cpu2:5000)WARNING: ScsiDeviceIO: 3074: Failing command 0x28 (requiredDataLen=9728 bytes) to write-quiesced partition naa.xxx:1 (vmkCmd=0x4124011f9b40 : cmdId.initiator=0x41000e0fb340 cmdId.ser 
    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 
    2012-11-12T13:23:50.765Z cpu2:5000)WARNING: ScsiDeviceIO: 3074: Failing command 0x28 (requiredDataLen=9728 bytes) to write-quiesced partition naa.xxx:1 (vmkCmd=0x4124011f9b40 : cmdId.initiator=0x41000e0fb340 cmdId.ser 
    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 
    2012-11-12T13:23:50.765Z cpu2:5000)WARNING: ScsiDeviceIO: 3074: Failing command 0x28 (requiredDataLen=9728 bytes) to write-quiesced partition naa.xxx:1 (vmkCmd=0x4124011f9b40 : cmdId.initiator=0x41000e0fb340 cmdId.ser 
    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 
    2012-11-12T13:23:50.765Z cpu2:5000)WARNING: ScsiDeviceIO: 3074: Failing command 0x28 (requiredDataLen=9728 bytes) to write-quiesced partition naa.xxx:1 (vmkCmd=0x4124011f9b40 : cmdId.initiator=0x41000e0fb340 cmdId.ser 
    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 
    2012-11-12T13:23:50.765Z cpu2:5000)WARNING: ScsiDeviceIO: 3074: Failing command 0x28 (requiredDataLen=9728 bytes) to write-quiesced partition naa.xxx:1 (vmkCmd=0x4124011f9b40 : cmdId.initiator=0x41000e0fb340 cmdId.ser 
    2012-11-12T13:23:50.765Z cpu2:5000)ALERT: ScsiDeviceIO: 3081: Failed write command to write-quiesced partition naa.xxx:1 
    2012-11-12T13:23:50.765Z cpu2:5000)Fil3: 13385: Max retries (10) exceeded for caller Fil3_FileIO (status 'IO was aborted by VMFS via a virt-reset on the device') 
    2012-11-12T13:23:56.723Z cpu1:5000)BC: 1858: Failed to write (uncached) object '.iormstats.sf': Maximum kernel-level retries exceeded 
    2012-11-12T13:23:57.368Z cpu11:4132)HBX: 231: Reclaimed heartbeat for volume 503f6831-a50ea3f0-bc4c-5ef3fcc3abc7 (LUN301): [Timeout] [HB state abcdef02 offset 4063232 gen 43 stampUS 358012043 uuid 50a0d5d0-96130a3c-4332-e61f131d9a43 jrnl <FB 65400> drv 
    2012-11-12T13:23:58.973Z cpu5:4132)<6>qla2xxx 0000:15:00.2: scsi(1:1:2): Abort command succeeded -- 1 252956.
    

I found a Cisco Community <a href="https://supportforums.cisco.com/docs/DOC-23667" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://supportforums.cisco.com/docs/DOC-23667']);">page</a> which matched the issue. We were not using Cisco UCS but instead the IBM HS22V blades. The suggestion in the previous page was to disable interrupt remapping as per VMware KB <a href="http://kb.vmware.com/kb/1030265" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1030265']);">1030265</a>. We tried disabling the option, but it didn't help out. I then ran across VMware KB <a href="http://kb.vmware.com/kb/2009482" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2009482']);">2009482</a>. The KB wasn't very helpful, here is some content from the KB:

> **Cause**  
> This message is logged, usually for write operations, when an ESX/ESXi host needs to stop I/O going to a device/LUN. A Virtual Device Reset is used to stop the I/O in order to maintain VMFS data integrity.  
> **Resolution**  
> To resolve this issue, you must investigate the reason why the ESX host issued the Virtual Device Reset. Typically there will be SCSI or other storage related errors before the virt-reset error message which should indicate the reason why the host needed to stop the I/O.

From the above logs, we can see that we had IO failing to the array. Here is the information regarding our CNA:

    ~ # cat /proc/scsi/qla2xxx/1 | head -6 
    QLogic PCI Express to FCoE Converged Network Adapter for QMI8142: 
    FC Firmware version 5.03.05 (8d4), Chip Type: QMI814x 
    MPI Firmware Version: 1.40.00 (66561) 
    Driver version 934.5.4.0-1vmw 
    
    Host Device Name vmhba0 
    

I did a couple of searches and I came across VMware KB <a href="http://kb.vmware.com/kb/2014323" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2014323']);">2014323</a>, VMware KB <a href="http://kb.vmware.com/kb/1018255" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1018255']);">1018255</a>, and Qlogic <a href="https://qlogic.secure.force.com/SupportCenter/articles/FAQ/MSI-X-in-ESXi-5-0-Causes-Pause-Frames-on-QLE81xx-and-QMI81xx-CNAs" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://qlogic.secure.force.com/SupportCenter/articles/FAQ/MSI-X-in-ESXi-5-0-Causes-Pause-Frames-on-QLE81xx-and-QMI81xx-CNAs']);">article</a>. All of them were regarding the QLE81xx or QMI81xx CNAs having issues with ESXi. All of the above KBs recommended to disable MSI-X Interrupts. This can be done by running the following on the host:

    ### For ESXi 5.x 
    ~ # esxcli system module parameters set -m qla2xxx --parameter-string "ql2xenablemsi24xx=0" 
    ### For ESXi 4.x 
    ~ # esxcfg-module -s "ql2xenablemsi=1" qla2xxx 
    

We were on 5.0, so we ran the top command. After running the above command the messages were not as frequent but still happening. Lastly I ran into VMware KB <a href="http://kb.vmware.com/kb/2008044" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2008044']);">2008044</a>. We didn't run into that issue but there was a recommendation to update the firmware to at least 5.06.05. From the above output we were at 5.03.05, so we were a little behind. I then found firmware version 5.07.00 from this Qlogic <a href="http://driverdownloads.qlogic.com/QLogicDriverDownloads_UI/SearchByProduct.aspx?ProductCategory=322&Product=1102&Os=167" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://driverdownloads.qlogic.com/QLogicDriverDownloads_UI/SearchByProduct.aspx?ProductCategory=322&Product=1102&Os=167']);">link</a> (Here is a <a href="http://filedownloads.qlogic.com/files/BootCode/84028/FirmwareReleaseNotes.txt" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://filedownloads.qlogic.com/files/BootCode/84028/FirmwareReleaseNotes.txt']);">link</a> to the release notes). After applying that firmware version, the messages stopped.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESX(i) Host with Emulex NC553i CNA Disconnects from Strorage" href="http://virtuallyhyper.com/2012/11/host-with-emulex-nc553i-cna-disconnects-from-strorage/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/host-with-emulex-nc553i-cna-disconnects-from-strorage/']);" rel="bookmark">ESX(i) Host with Emulex NC553i CNA Disconnects from Strorage</a>
    </li>
  </ul>
</div>

