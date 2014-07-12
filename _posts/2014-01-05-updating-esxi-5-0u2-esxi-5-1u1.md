---
title: Updating ESXi 5.0U2 to ESXi 5.1U1
author: Karim Elatov
layout: post
permalink: /2014/01/updating-esxi-5-0u2-esxi-5-1u1/
categories: ['home_lab', 'vmware']
tags: ['esxcli', 'hostd']
---

I decided to update my ESXi host to 5.1 just cause it was time to catch up on updates.

### Using *esxcli* to Perform the Update

I was currently on 5.0U2:

    ~ # vmware -lv
    VMware ESXi 5.0.0 build-914586
    VMware ESXi 5.0.0 Update 2


Reading over the [vSphere Upgrade Guide for vSphere 5.1](http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-51-upgrade-guide.pdf), I saw that **esxcli** was a viable option for the update. From the guide, here is a table of the upgrade paths:

![51 upgrade methp1 Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/51-upgrade-methp1.png)

![51 upgrade methp2 Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/51-upgrade-methp2.png)

There is also [VMware KB 2032757](http://kb.vmware.com/kb/2032757) which summarizes the upgrade guide into a KB. The KB is really helpful except it has a conflicting statement. The KB has a table that says **esxcli** cannot be used when going from 5.0 to 5.1. Here is the table:

![wrong table from Kb Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/wrong_table_from_Kb.png)

Under the **Update a Host with Image Profiles** section of the Upgrade Guide, I saw the following:

> You can update a host with image profiles stored in a software depot that is accessible through a URL or in an offline ZIP depot.
>
> ...
>
> Update the existing image profile to include the VIBs or install new VIBs. ![esxcli update 51 guide Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/esxcli-update-51-guide.png)

I did some research and I came across [A Pretty Cool Method of Upgrading to ESXi 5.1](http://www.virtuallyghetto.com/2012/09/a-pretty-cool-method-of-upgrading-to.html). In that post it describes the process on how to update to 5.1 with **esxcli** and download the upgrade from a VMware hosted VUM depot. In summary here are the steps:

1.  Open firewall to allow outbound HTTP traffic: `esxcli network firewall ruleset set -e true -r httpClient`
2.  Check available "profiles" to be applied: `esxcli software sources profile list -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml`
3.  Apply one of the profiles, in the below example it uses the 5.1 profile: `esxcli software profile update -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml -p ESXi-5.1.0-799733-standard`

In the example from the above post, the blogger goes from 5.0u1 to 5.1 using **esxcli** (not sure why the VMware KB states otherwise).

#### Doing the Update

I checked out the download for 5.1 and I saw the following:

![51 offline bundle 1024x113 Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/51-offline-bundle.png)

The bundle was ~300MB, rather than downloading that using the ESXi host, I decided to first download it to my local desktop and then copy it to the host (just in case the update fails, I wouldn't want to download that again... plus I can save it in my ISOs repository for later use as well). Then uploading the file to my datastore:

    $ scp VMware-ESXi-5.1.0-799733-depot.zip esx:/vmfs/volumes/datastore1/.
    VMware-ESXi-5.1.0-799733-depot.zip            100%  298MB  16.5MB/s   00:18


Checking out the profiles:

    ~ # esxcli software sources profile list --depot=/vmfs/volumes/datastore1/VMware-ESXi-5.1.0-799733-depot.zip
    Name                        Vendor        Acceptance Level
    --------------------------  ------------  ----------------
    ESXi-5.1.0-799733-no-tools  VMware, Inc.  PartnerSupported
    ESXi-5.1.0-799733-standard  VMware, Inc.  PartnerSupported


This actually matched the output from the above blog as well (but in the blog it was showing the profiles stored on the hosted VMware VUM depot).

Let's put the host into maintenance mode:

    ~ # vim-cmd hostsvc/maintenance_mode_enter
    'vim.Task:haTask-ha-host-vim.HostSystem.enterMaintenanceMode-213709113'


And now for the update:

    ~ # esxcli software profile update -d /vmfs/volumes/datastore1/VMware-ESXi-5.1.0-799733-depot.zip -p ESXi-5.1.0-799733-standard
    Update Result
       Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
       Reboot Required: true
       VIBs Installed: VMware_bootbank_ata-pata-amd_0.3.10-3vmw.510.0.0.799733, VMware_bootbank_ata-pata-atiixp_0.4.6-4vmw.510.0.0.799733,...
       VIBs Removed: VMware_bootbank_ata-pata-amd_0.3.10-3vmw.500.0.0.469512, VMware_bootbank_ata-pata-atiixp_0.4.6-3vmw.500.0.0.469512, ....
       VIBs Skipped: VMware_bootbank_net-tg3_3.110h.v50.4-4vmw.510.0.0.799733


I then restarted the host to finish the update.

### Fixing Post Update Issues

At first the update looked really good, the host rebooted and the regular ESXi management logon window didn't show any errors. I tried connecting to the host with a vSphere Client but it would fail. Luckily I had SSH enabled and I was able to check out the logs. After some investigation, I saw that **hostd** would not start up. I would actually see a **backtrace** in the **hostd** logs:

    ~ # tail /var/log/hostd.log
    2014-01-05T19:33:16.296Z [FFAB6D20 info 'Hbrsvc'] Replication Scheduler started; using the 'hybrid' algorithm with max bandwidth = 20000.
    2014-01-05T19:33:16.297Z [FFAB6D20 info 'Hbrsvc'] HBR has started
    2014-01-05T19:33:16.297Z [FFAB6D20 error 'HttpNfcSvc'] Reverse proxy endpoint list is not available
    *** In-memory logs end ***
    error: N5Vmomi5Fault11SystemError9ExceptionE(vmodl.fault.SystemError)
    2014-01-05T19:33:16.303Z [450C1B90 info 'Hbrsvc'] ReplicationScheduler: computing schedule
    backtrace:
    2014-01-05T19:33:16.315Z [44B86B90 info 'Hbrsvc'] ReplicationScheduler: Schedule computed.
    backtrace[00] rip 18dc7333 Vmacore::System::Stacktrace::CaptureWork(unsigned int)
    backtrace[01] rip 18bed698 Vmacore::System::SystemFactoryImpl::CreateQuickBacktrace(Vmacore::Ref<Vmacore::System::Backtrace>&)
    backtrace[02] rip 18b8c0c5 Vmacore::Throwable::Throwable(std::string const&)
    backtrace[03] rip 085844d0 hostd [0x85844d0]
    backtrace[04] rip 085830f5 hostd [0x85830f5]
    backtrace[05] rip 18baa84b Vmacore::Service::AppImpl::StartPlugins()
    backtrace[06] rip 18ba916f Vmacore::Service::InitApp(Vmacore::Service::Config*)
    backtrace[07] rip 09120523 hostd [0x9120523]
    backtrace[08] rip 09116118 hostd [0x9116118]
    backtrace[09] rip 09124542 hostd [0x9124542]
    backtrace[10] rip 1e951efc /lib/libc.so.6(__libc_start_main+0xdc) [0x1e951efc]
    backtrace[11] rip 084960b1 hostd [0x84960b1]


Checking out the VMware Communities, I ran into [this](https://communities.vmware.com/thread/421269) discussion. The person from that discussion ran into a similar issue and fixed the issue by resetting the configurations. So going through the IPMI interface, I tried the same thing:

![reset configuration Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/reset-configuration.png)

After the reset, it started the reboot of the host:

![settings reset g Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/settings-reset_g.png)

After the host rebooted, **hostd** started up fine without issues. I must've made some customization that caused **hostd** to fail. I reconnected to the host and recreated: my vSwitch, iSCSI, and networking settings (it actually didn't take that long, but if you had a lot of settings be careful).

### Update from 5.1 to 5.1U1

While I was in the updating mood, I decided to update to the latest 5.1 version. I want back to the **myvmware** web page and saw the *offline bundle*:

![51 u1 offline bundle 1024x116 Updating ESXi 5.0U2 to ESXi 5.1U1](https://github.com/elatov/uploads/raw/master/2014/01/51_u1_offline-bundle.png)

This was just a regular offline bundle, so after I copied the file to the ESXi host, I ran the following to apply the update:

    ~ # esxcli software vib install -d /vmfs/volumes/datastore1/update-from-esxi5.1-5.1_update01.zip
    Installation Result
       Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
       Reboot Required: true
       VIBs Installed: VMware_bootbank_esx-base_5.1.0-1.12.1065491, VMware_bootbank_esx-xserver_5.1.0-0.11.1063671, ..
       VIBs Removed: VMware_bootbank_esx-base_5.1.0-0.0.799733, VMware_bootbank_esx-xserver_5.1.0-0.0.799733,
       VIBs Skipped: VMware_bootbank_ata-pata-amd_0.3.10-3vmw.510.0.0.799733, ...


Then to reboot the host, I ran the following:

    ~ # esxcli system maintenanceMode set -e true
    ~ # esxcli system shutdown reboot -r update


I already had all the VMs off, so going to *maintenance mode* didn't make a difference. After the reboot here was the final version of ESXi:

    ~ # vmware -lv
    VMware ESXi 5.1.0 build-1065491
    VMware ESXi 5.1.0 Update 1


and luckily **hostd** was up and running:

    ~ # /etc/init.d/hostd status
    hostd is running.
