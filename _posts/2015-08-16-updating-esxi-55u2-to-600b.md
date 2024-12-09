---
published: true
layout: post
title: "Updating ESXi 5.5u2 to 6.0.0b"
author: Karim Elatov
categories: [vmware,home_lab]
tags: [esxcli,macmini]
---
So I decided it was time to update my *MacMini 6,2* that was running ESXi. It was running at the following version:

    ~ # vmware -lv
    VMware ESXi 5.5.0 build-2068190
    VMware ESXi 5.5.0 Update 2

### Preparing for the Update

Looking over [Methods for upgrading to VMware ESXi 6.0 (2109711)](https://knowledge.broadcom.com/external/article?legacyId=2109711), here are the supported upgrade paths:

> You can upgrade an ESXi 5.0.x, ESXi 5.1.x, or ESXi 5.5.х host directly to 6.0, using any of these methods. For more details, see the Supported Upgrades to ESXi 6.0 section in the vSphere Upgrade Guide.

From the previous update posts [Updating ESXi 5.0U2 to ESXi5.1U1](/2014/01/updating-esxi-5-0u2-esxi-5-1u1/) and [ESXi Patch for HeartBleed](/2014/06/esxi-patch-for-heartbleed/), I usually use **esxcli** to apply the update. We can check the VMware hosted VUM server for available versions:

    ~ # esxcli network firewall ruleset set -e true -r httpClient
    ~ # esxcli software sources profile list -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml | grep ESXi-6.
    ESXi-6.0.0-20150404001-standard   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150704001-standard   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150704001-no-tools   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150404001-no-tools   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-2494585-standard       VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150504001-no-tools   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150701001s-no-tools  VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150701001s-standard  VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150504001-standard   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-2494585-no-tools       VMware, Inc.  PartnerSupported

Then looking over [this page](http://www.virten.net/vmware/esxi-release-build-number-history/#esxi6.0)

![vshpere-6-versions](https://raw.githubusercontent.com/elatov/upload/master/esxi-55u2-to-60b-update/vshpere-6-versions.png)

it looks like **ESXi 6.0b** is latest version and is the way to go since it fixes a bunch of bugs. The release notes for **6.0.0b** can be seen [here](https://www.vmware.com/support/vsphere6/doc/vsphere-esxi-600b-release-notes.html). I did check out the [compatiliby page](http://www.vmware.com/resources/compatibility) and *MacMini 6,2* was not on the list, but I think it will work out (plus looking over [this](https://derflounder.wordpress.com/2015/03/24/setting-up-esxi-6-0-on-a-2012-mac-mini-server/) page and also [this](http://www.virtuallyghetto.com/2015/02/esxi-6-0-works-ootb-for-apple-mac-mini-mac-pro.html) page, gave me confidence as well):

![compatibility-vsphere6-apple](https://raw.githubusercontent.com/elatov/upload/master/esxi-55u2-to-60b-update/compatibility-vsphere6-apple.png)

I found the patch at [my vmware](https://my.vmware.com/group/vmware/patch):

![esxi-patches](https://raw.githubusercontent.com/elatov/upload/master/esxi-55u2-to-60b-update/esxi-patches.png)

After downloading the file, I **scp**'ed it to a datastore on the ESXi host (I know I could've used the public VUM repo, but I want to have the zip for later use if necessary):

    elatov@gen:~/downloads$scp ESXi600-201507001.zip root@macm:/vmfs/volumes/datastore1/updates/.
    ESXi600-201507001.zip               100%  668MB  30.4MB/s  39.0MB/s   00:22

### Updating ESXi
So let's go ahead and shutdown all the VMs. You can get a list of all running VMs using the following command (if it's empty then nothing is running):

    ~ # esxcli vm process list

I setup my VMs to autostart and autostop with the host so I can just run this:

    vmware-autostart.sh stop

and that will shutdown my VMs, if you really want to go crazy you can stop all the VMs and stop all the services with the following command:

    shutdown.sh

But then you won't be able to put the host into maintenance mode. After all the VMs were shut off, I put the host into maintenance mode:

    ~ # esxcli system maintenanceMode set -e true

Then double checking the patch:

    ~ # esxcli software sources profile list -d /vmfs/volumes/datastore1/updates/ESXi600-201507001.zip
    Name                              Vendor        Acceptance Level
    --------------------------------  ------------  ----------------
    ESXi-6.0.0-20150701001s-standard  VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150701001s-no-tools  VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150704001-no-tools   VMware, Inc.  PartnerSupported
    ESXi-6.0.0-20150704001-standard   VMware, Inc.  PartnerSupported

From [VMware ESXi 6.0, Patch Release ESXi600-201507001 (2111982)](https://knowledge.broadcom.com/external/article?legacyId=2111982), here is note about the profiles that have the **s** in them:

> VMware patch and update releases contain general and security-only image profiles. Security-only image profiles are applicable to new security fixes only. No new bug fixes are included, but bug fixes from earlier patch/update releases are included.
>
> The general release image profile supersedes the security-only profile. Application of the general release image profile applies to new security and bug fixes.
>
> The security-only image profiles are identified with the additional "s" identifier in the image profile name.


I wanted all the fixes so I used the general profile, and now for the update:

    ~ # esxcli software profile update -d /vmfs/volumes/datastore1/updates/ESXi600-201507001.zip -p ESXi-6.0.0-20150704001-standard
    Update Result
       Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
       Reboot Required: true
       VIBs Installed: VMWARE_bootbank_mtip32xx-native_3.8.5-1vmw.600.0.0.2494585, VMware_bootbank_ata-pata-amd_0.3.10-3vmw.600.0.0.2494585, VMware_bootbank_ata-pata-atiixp_0.4.6-4vmw.600.0.0.2494585,
      VIBs Removed: VMware_bootbank_ata-pata-amd_0.3.10-3vmw.550.1.15.1623387, VMware_bootbank_ata-pata-atiixp_0.4.6-4vmw.550.1.15.1623387, VMware_bootbank_ata-pata-cmd64x_0.2.5-3vmw.550.1.15.1623387,
    VIBs Skipped:

Then to take the host out of mainteance mode and reboot:

    ~ # esxcli system maintenanceMode set -e false
    ~ # esxcli system shutdown reboot -r 'update_to_6_0'

### Confirm the Update

After the host has rebooted, login via SSH and confirm the new version is installed:

    [root@macm:~] vmware -lv
    VMware ESXi 6.0.0 build-2809209
    VMware ESXi 6.0.0 GA

And the NICs loaded fine:

    [root@macm:~] esxcli network nic list
    Name    PCI Device    Driver  Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
    ------  ------------  ------  ------------  -----------  -----  ------  -----------------  ----  --------------------------------------------------------
    vmnic0  0000:01:00.0  tg3     Up            Up            1000  Full    68:5b:35:c9:96:10  1500  Broadcom Corporation NetXtreme BCM57766 Gigabit Ethernet
    vmnic1  0000:09:00.0  tg3     Up            Up            1000  Full    68:5b:35:91:47:85  1500  Broadcom Corporation NetXtreme BCM57762 Gigabit Ethernet
