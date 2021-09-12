---
title: Quiesced Snapshots Failing in Windows 2008 R2 VMs
author: Karim Elatov
layout: post
permalink: /2012/05/quiesced-snapshots-failing-windows-2008-r2-vms/
categories: ['vmware', 'os']
tags: [ 'vm_snapshot', 'vmware_tools', 'win2k8r2']
---

I ran into a very interesting issue. Whenever we took a quiesced snapshot of Windows 2008 R2 VMs running on an ESX 4.1U2 host we saw the following error in the event viewer and the snapshot would fail:

```bash
Event ID 57 ntfs Warning
The system failed to flush data to the transaction log. Corruption may occur.

Event ID: 137 ntfs Error
The default transaction resource manager on volume \\?\Volume{806289e8-6088-11e0-a168-005056ae003d} encountered a non-retryable error and could not start. The data contains the error code.

Event ID: 12289 VSS Error
Volume Shadow Copy Service error: Unexpected error DeviceIoControl(\\?\fdc#generic_floppy_drive#6&2bc13940&0&0#{53f5630d-b6bf-11d0-94f2-00a0c91efb8b} - 00000000000004A0,0x00560000,0000000000000000,0,0000000000353B50,4096,[0]). hr = 0x80070001, Incorrect function.
```

There is actually an ongoing VMware community thread [309844](http://communities.vmware.com/thread/309844), that keeps talking about the issue. There is no clear solution to this as of yet, but here is what I did to get around the issue:

1. Disable and remove the Floppy device from the VM (it's not used any ways)
2. Downgrade vmware-tools versions from 8.3.7 (ESX 4.1U2) to 8.3.2 (ESX 4.1GA)

To find out your version of vmware-tools follow the instructions in VMware KB [392](http://kb.vmware.com/kb/392). If you are running anything other than 8.3.2 then you can download the older tools from here:

For 32 Bit:

http://packages.vmware.com/tools/esx/4.1/windows/x86/VMware-tools-windows-8.3.2-257589.iso

For 64bit:

http://packages.vmware.com/tools/esx/4.1/windows/x86_64/VMware-tools-windows-8.3.2-257589.iso

Then remove your current version of vmware-tools following the intructions from [ESXi and vCenter Server 5 Documentation > vSphere Upgrade > Upgrading Virtual Machines](http://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vsphere.upgrade.doc_50%2FGUID-6F7BE33A-3B8A-4C57-9C35-656CE05BE22D.html). After you are done with that, mount the ISO that you downloaded from above. To do so, you have many options:

1. Using vSphere Client connect the ISO (locally stored on your local machine) to the VM (instructions found [here](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.vm_admin.doc/GUID-492D6904-7471-4D66-9555-9466CCCA6931.html#GUID-492D6904-7471-4D66-9555-9466CCCA6931))
2. Upload the ISO to a datastore of an ESX host and connect it to the VM (instructions found [here](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.vm_admin.doc/GUID-73D0598A-2F3E-4BBE-88C2-A4EEE6097784.html))
3. Upload the ISO directly to the VM and mount it using a third party tool (ie VIrtualClone Drive and Daemon tools)

After the ISO is mounted just execute setup.exe to install the older version of vmware-tools. Now your quiesced snapshots should work.

