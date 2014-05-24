---
title: "X Server Doesn't Start After Upgrading to Fedora 18 with Nvidia Driver"
author: Karim Elatov
layout: post
permalink: /2013/03/x-server-doesnt-start-after-upgrading-to-fedora-18-with-nvidia-driver/
dsq_thread_id:
  - 1407305461
categories:
  - Home Lab
  - OS
tags:
  - Fedora 18
  - nVidia
---
I updated my machine to Fedora 18 and I had the Nvidia driver installed (check out [this](/2012/10/setup-fedora-17-with-nvidia-geforce-6200-to-connect-to-a-tv-and-function-as-an-xbmc-media-center/) previous post for the Nvidia setup), but after I rebooted, X wouldn't start. Checking out the **/var/log/Xorg.0.log** file, I saw the following:

    [ 44.607] (EE) NVIDIA: Failed to load the NVIDIA kernel module. Please check your
    [ 44.607] (EE) NVIDIA: system's kernel log for additional error messages.
    [ 44.607] (II) UnloadModule: "nvidia"
    [ 44.607] (II) Unloading nvidia
    [ 44.607] (EE) Failed to load module "nvidia" (module-specific error, 0)
    [ 44.607] (EE) No drivers available.


Next, checking out the Nvidia log file **/var/log/nvidia-installer.log**, I saw the following:

    test -e include/generated/autoconf.h -a -e include/config/auto.conf || ( \
    echo; \
    echo " ERROR: Kernel configuration is invalid."; \
    echo " include/generated/autoconf.h or include/config/auto.conf are
    missing.";\


Checking out which package provides those files, I saw the following:

    moxz:~> yum provides "*include/generated/autoconf.h"
    Loaded plugins: remove-with-leaves
    adobe-linux-i386/filelists | 140 kB 00:00:00
    fedora/filelists_db | 22 MB 00:00:24
    google-chrome/filelists | 1.1 kB 00:00:00
    rpmfusion-free/filelists_db | 277 kB 00:00:00
    rpmfusion-free-updates/filelists_db | 88 kB 00:00:00
    rpmfusion-nonfree/filelists_db | 184 kB 00:00:00
    rpmfusion-nonfree-updates/filelists_db | 30 kB 00:00:00
    updates/filelists_db | 9.2 MB 00:00:08
    kernel-PAE-devel-3.6.10-4.fc18.i686 : Development package for building kernel modules to match the PAE kernel
    Repo : fedora
    Matched from:
    Filename : /usr/src/kernels/3.6.10-4.fc18.i686.PAE/include/generated/autoconf.h
    kernel-PAEdebug-devel-3.6.10-4.fc18.i686 : Development package for building kernel modules to match the PAEdebug kernel
    Repo : fedora
    Matched from:
    Filename : /usr/src/kernels/3.6.10-4.fc18.i686.PAEdebug/include/generated/autoconf.h


It looks like those files are provided by the **kernel-devel** package. Checking out my kernel packages:

    moxz:~>rpm -qa | grep kernel
    kernel-tools-3.6.10-4.fc18.i686
    kernel-devel-3.3.4-5.fc17.i686
    kernel-3.3.4-5.fc17.i686
    kernel-headers-3.6.10-4.fc18.i686
    kernel-devel-3.6.10-4.fc18.i686
    kernel-tools-libs-3.6.10-4.fc18.i686
    kernel-3.7.8-202.fc18.i686


I have the **kernel-devel** packages installed but not for my current kernel. My kernel was the following:

    moxz:~>uname -r
    3.7.8-202.fc18.i686


and here were the **kernel-devel** packages:

    moxz:~>rpm -qa | grep kernel-devel
    kernel-devel-3.3.4-5.fc17.i686
    kernel-devel-3.6.10-4.fc18.i686


I tried a **yum update**:

    moxz:~>sudo yum update kernel-devel
    Loaded plugins: remove-with-leaves
    Nothing to do


But it looks like it's not in the YUM repositories. I found the package on [**http://rpm.pbone.net**](http://rpm.pbone.net) and downloaded it. I then installed it manually:

    moxz:~>sudo rpm -ivh kernel-devel-3.7.8-202.fc18.i686.rpm
    Preparing... ################################# [100%]
    Updating / installing...
    1:kernel-devel-3.7.8-202.fc18 ################################# [100%]


Now checking over my **kernel-devel** packages, I saw the following:

    moxz:~>rpm -qa | grep kernel-devel
    kernel-devel-3.3.4-5.fc17.i686
    kernel-devel-3.7.8-202.fc18.i686
    kernel-devel-3.6.10-4.fc18.i686


That looks better. Now we can restart the **akmods** service and that will compile the new kernel module:

    moxz:~>sudo service akmods restart
    Redirecting to /bin/systemctl restart akmods.service


No errors were shown. Now checking out the status:

    moxz:~>sudo service akmods status
    Redirecting to /bin/systemctl status akmods.service
    akmods.service - Builds and install new kmods from akmod packages
         Loaded: loaded (/usr/lib/systemd/system/akmods.service; enabled)
         Active: active (exited) since Sun 2013-02-24 08:44:29 PST; 26s ago
         Process: 13889 ExecStart=/usr/sbin/akmods --from-init (code=exited, status=0/SUCCESS)
    Feb 24 08:43:18 moxz systemd[1]: Starting Builds and install new kmods from akmod packages...
    Feb 24 08:43:18 moxz akmods[13889]: Checking kmods exist for 3.7.8-202.fc18.i686[ OK ]
    Feb 24 08:43:18 moxz runuser[13916]: pam_unix(runuser:session): session opened for user akmods by (uid=0)
    Feb 24 08:44:15 moxz runuser[13916]: pam_unix(runuser:session): session closed for user akmods
    Feb 24 08:44:29 moxz akmods[13889]: Building and installing nvidia-kmod[ OK ]
    Feb 24 08:44:29 moxz systemd[1]: Started Builds and install new kmods from akmod packages.


We can see that the **nvidia-kmod** kernel module compiled fine. Now checking out for last installed RPM, I see this:

    moxz:~>rpm -qa --last | head -1
    kmod-nvidia-3.7.8-202.fc18.i686-304.64-6.fc18.i686 Mon 25 Feb 2013 09:16:38 AM PS


Then checking out that RPM package:

    moxz:~>rpm -qi kmod-nvidia-3.7.8-202.fc18.i686-304.64-6.fc18.i686
    Name : kmod-nvidia-3.7.8-202.fc18.i686
    Epoch : 1
    Version : 304.64
    Release : 6.fc18
    Architecture: i686
    Install Date: Sun 24 Feb 2013 08:44:18 AM PST
    Group : System Environment/Kernel
    Size : 11593588
    License : Redistributable, no modification permitted
    Signature : (none)
    Source RPM : nvidia-kmod-304.64-6.fc18.src.rpm
    Build Date : Sun 24 Feb 2013 08:44:09 AM PST
    Build Host : moxz
    Relocations : (not relocatable)
    URL : http://www.nvidia.com/
    Summary : nvidia kernel module(s) for 3.7.8-202.fc18.i686
    Description :
    This package provides the nvidia kernel modules built for the Linux
    kernel 3.7.8-202.fc18.i686 for the i686 family of processors.


The "Build Host" is the **hostname** of my machine :) Checking out what files the package installed, we see this:

    moxz:~>rpm -ql kmod-nvidia-3.7.8-202.fc18.i686-304.64-6.fc18.i686
    /usr/lib/modules/3.7.8-202.fc18.i686/extra/nvidia
    /usr/lib/modules/3.7.8-202.fc18.i686/extra/nvidia/nvidia.ko


Lastly restarting X:

    moxz:~>sudo init 3
    moxz:~>sudo init 5


or with this command:

    moxz:~>sudo service gdm restart


My X Server started up without any issues and we see the kernel module loaded as well:

    moxz:~>lsmod | grep ^nvidia
    nvidia              10257972  40


**Update: 4/20/13** After some time I realized that my kernel was never getting updated. Looking into it, I discovered that I had excluded the kernel package from being installed via **yum**. I had the following option set:

    moxz:~>grep exclude /etc/yum.repos.d/fedora-updates.repo
    exclude=kernel*


After I removed that line, kernel updates started to work. That was the source of my problem all along.

