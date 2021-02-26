---
published: true
layout: post
title: "Upgrade CentOS 8 to RHEL 8"
author: Karim Elatov
categories: [os]
tags: [linux,centos,redhat]
---

With all the news about [CentOS changing it's vision](https://blog.centos.org/2020/12/future-is-centos-stream/) and [RedHat expanding their free subscription model](https://www.redhat.com/en/blog/new-year-new-red-hat-enterprise-linux-programs-easier-ways-access-rhel), I decided to update my CentOS 8 machine to RHEL 8.

## Back Up
Since this was a VM running on an ESXi machine, I decided to create a snapshot of the disk. First SSH to the machine and shut it off:

```bash
> sudo systemctl poweroff
```

Next SSH to the ESXi host and get the **vmid** of the VM (most of these commands are covered in [Consolidating/Committing snapshots in ESXi](https://kb.vmware.com/s/article/1002310)):

```bash
[root@hp:~] vim-cmd vmsvc/getallvms | grep -i m2
6      m2        [datastore1] m2/m2.vmx             centos8_64Guest     vmx-15
```

Now let's create a snapshot:

```bash
[root@hp:~] vim-cmd vmsvc/snapshot.create 6 BeforeRHEL "Snapshot before RHEL8 Migration" 0 0
Create Snapshot:
```

Now let's make sure we see the snapshot:

```bash
[root@hp:~] vim-cmd vmsvc/snapshot.get 6
Get Snapshot:
|-ROOT
--Snapshot Name        : BeforeRHEL
--Snapshot Id        : 23
--Snapshot Desciption  : Snapshot before RHEL 8 Migration
--Snapshot Created On  : 2/26/2021 17:41:7
--Snapshot State       : powered off
```

Now let's power on the VM:

```bash
[root@hp:~] vim-cmd vmsvc/power.on 6
Powering on VM:
```

If you really want to be safe and you have the space, you can create a full clone of the disk:

```bash
[root@hp:~] vmkfstools -i /vmfs/volumes/datastore1/m2/m2-000001.vmdk /vmfs/volumes/backups/m2/m2-bef-rhel8.vmdk
Destination disk format: VMFS zeroedthick
Cloning disk '/vmfs/volumes/datastore1/m2/m2-000001.vmdk'...
Clone: 100% done.
```

## Check RedHat Subscription
Confirm you have a developer subscription in your redhat account:

![rh-subscription.png](https://res.cloudinary.com/elatov/image/upload/v1614368611/blog-pics/centos-to-rhel/rh-subscription.png)

## Performing the Migration
Reading over [How to convert from CentOS Linux or Oracle Linux to RHEL](https://access.redhat.com/articles/2360841), it looks like there is an existing tool that allows us to do the migration, it's called `convert2rhel`. So let's install it:

```bash
> sudo dnf install -y https://github.com/oamg/convert2rhel/releases/download/v0.17/convert2rhel-0.17-1.el8.noarch.rpm
Last metadata expiration check: 0:04:16 ago on Fri 26 Feb 2021 10:52:11 AM MST.
convert2rhel-0.17-1.el8.noarch.rpm              168 kB/s |  95 kB     00:00
Dependencies resolved.
================================================================================
 Package                 Arch        Version            Repository         Size
================================================================================
Installing:
 convert2rhel            noarch      0.17-1.el8         @commandline       95 k
Installing dependencies:
 python3-pexpect         noarch      4.3.1-3.el8        appstream         138 k
 python3-ptyprocess      noarch      0.5.2-4.el8        appstream          31 k

Transaction Summary
================================================================================
Install  3 Packages

Total size: 264 k
Total download size: 169 k
Installed size: 833 k
```

We can run the following and it will prompt us to choose our subscription:

```bash
export RH_USER=$(grep user rh.txt | awk '{print $2}')
export RH_PASS=$(grep pass rh.txt | awk '{print $2}')
> sudo convert2rhel --username $RH_USER --password $RH_PASS

[02/26/2021 11:02:16] TASK - [Prepare: End user license agreement] ******************************
The following text is a copy of the November 18, 2019 version of Red Hat GPLv2-Based End User License Agreement (EULA) [1].
For up-to-date version of the EULA, visit [2].

WARNING - By continuing you accept this EULA.

Continue with the system conversion? [y/n]: y



[02/26/2021 11:02:19] TASK - [Prepare: Gather system information] *******************************
Name:                CentOS Linux
OS version:          8.3
Architecture:        x86_64
Config filename:     centos-8-x86_64.cfg
Running the 'rpm -Va' command which can take several minutes. It can be disabled by using the --no-rpm-va option.
The 'rpm -Va' output has been stored in the /var/log/convert2rhel/rpm_va.log file

[02/26/2021 11:04:57] TASK - [Prepare: Backup System] *******************************************
Backing up /etc/system-release
Copying /etc/system-release to /var/lib/convert2rhel/backup
Backing up /etc/yum.conf
Copying /etc/yum.conf to /var/lib/convert2rhel/backup

[02/26/2021 11:04:57] TASK - [Prepare: Clear YUM/DNF version locks] *****************************
Usage of YUM/DNF versionlock plugin not detected.

[02/26/2021 11:04:57] TASK - [Convert: List third-party packages] *******************************
WARNING - Only packages signed by CentOS Linux are to be reinstalled. Red Hat support won't be provided for the following third party packages:

[02/26/2021 11:05:47] TASK - [Convert: Remove excluded packages] ********************************
Searching for the following excluded packages:

centos-logos* ................................... 1
centos-indexhtml ................................ 0
centos-obsolete-packages ........................ 0
rhn* ............................................ 1
python3-rhn* .................................... 2

[02/26/2021 11:06:07] TASK - [Convert: Subscription Manager - Download packages] ****************
Successfully downloaded the subscription-manager package.
Successfully downloaded the subscription-manager-rhsm-certificates package.
Successfully downloaded the python3-subscription-manager-rhsm package.
Successfully downloaded the dnf-plugin-subscription-manager package.
Successfully downloaded the python3-syspurpose package.

[02/26/2021 11:06:17] TASK - [Convert: Subscription Manager - Subscribe system] *****************
Building subscription-manager command ...
    ... activation key not found, username and password required
    ... username detected
    ... password detected
Registering system by running subscription-manager command ...
Registering to: subscription.rhsm.redhat.com:443/subscription
The system has been registered with ID: $RH_ID
The registered system name is: m2.kar.int
Manually select subscription appropriate for the conversion
Choose one of your subscriptions that is to be used for converting this system to RHEL:

======= Subscription number 1 =======

Enter number of the chosen subscription: 1


Attaching subscription with pool ID $RH_POOL to the system ...
Successfully attached a subscription for: Red Hat Developer Subscription for Individuals

[02/26/2021 11:07:27] TASK - [Convert: Get RHEL repository IDs] *********************************
RHEL repository IDs to enable: rhel-8-for-x86_64-baseos-rpms, rhel-8-for-x86_64-appstream-rpms

[02/26/2021 11:07:27] TASK - [Convert: Subscription Manager - Check required repositories] ******
Verifying needed RHEL repositories are available ...
Repositories available through RHSM:
ansible-2.9-for-rhel-8-x86_64-debug-rpms


[02/26/2021 11:07:55] TASK - [Convert: Remove packages containing repofiles] ********************
Searching for packages containing repofiles or affecting variables in the repofiles:

centos-release* ................................. 0
centos-repos .................................... 0
centos-linux-repos .............................. 1
centos-stream-repos ............................. 0
centos-linux-release ............................ 1
centos-stream-release ........................... 0

[02/26/2021 11:08:32] TASK - [Convert: Import Red Hat GPG keys] *********************************

[02/26/2021 11:08:32] TASK - [Convert: Prepare kernel] ******************************************
Installing RHEL kernel ...

[02/26/2021 11:11:30] TASK - [Convert: Replace packages] ****************************************
Performing update of the CentOS Linux packages ...

[02/26/2021 11:22:50] TASK - [Final: rpm files modified by the conversion] **********************

[02/26/2021 11:24:31] TASK - [Final: Non-interactive mode] **************************************
For the non-interactive use of the tool, run the following command:
convert2rhel -u $RH_USER -p ***** --pool $RH_POOL -y


WARNING - In order to boot the RHEL kernel, restart of the system is needed.
```
And that took care most of it. 

## Confirm Migration is Finished

After a reboot (`systemctl reboot`), I saw the appropriate system info:

```bash
> lsb_release -a
LSB Version:	:core-4.1-amd64:core-4.1-noarch
Distributor ID:	RedHatEnterprise
Description:	Red Hat Enterprise Linux release 8.3 (Ootpa)
Release:	8.3
Codename:	Ootpa
```

And RedHat Subscription:

```bash
> sudo subscription-manager list --consumed
+-------------------------------------------+
   Consumed Subscriptions
+-------------------------------------------+
Subscription Name:   Red Hat Developer Subscription for Individuals
Provides:            Red Hat Enterprise Linux High Availability - Update
                     Services for SAP Solutions
                     Red Hat Enterprise Linux Atomic Host
...
SKU:                 RH007....
Contract:
Account:
Serial:              3....
Pool ID:             8a85f99.....
Provides Management: No
Active:              True
Quantity Used:       1
Service Type:
Roles:
Service Level:       Self-Support
Usage:
Add-ons:
Status Details:      Subscription is current
Subscription Type:   Standard
Starts:              04/01/2020
Ends:                04/01/2021
Entitlement Type:    Physical
```

You can also login to the RedHat Customer portal and confirm that 1 subscription has been assigned:

![rh-sub-registered.png](https://res.cloudinary.com/elatov/image/upload/v1614368611/blog-pics/centos-to-rhel/rh-sub-registered.png)

And under the **Systems** section you can see your machine information:

![rh-sub-system.png](https://res.cloudinary.com/elatov/image/upload/v1614368611/blog-pics/centos-to-rhel/rh-sub-system.png)

### Clean Up
If you feel comfortable with the migration you can remove all the snapshots on the ESXi host for the VM:

```bash
vim-cmd vmsvc/snapshot.removeall 6
```
