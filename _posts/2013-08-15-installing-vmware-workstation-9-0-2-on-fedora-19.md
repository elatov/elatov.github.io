---
title: Installing VMware Workstation 9.0.2 on Fedora 19
author: Karim Elatov
layout: post
permalink: /2013/08/installing-vmware-workstation-9-0-2-on-fedora-19/
dsq_thread_id:
  - 1609432349
categories:
  - Home Lab
  - OS
  - VMware
tags:
  - fedora
  - vmware-gksu
  - VMware_Workstation
---
I ran into some issues setting up my VMware Workstation on my Fedora 19 install, so I decided to put together all the notes on how I got around them.

## VMware WorkStation Installer

After you have downloaded the installer from VMware, you will see the following in your *downloads* folder:

    elatov@kmac:~/downloads$ls | grep Work
    VMware-Workstation-Full-9.0.2-1031769.x86_64.txt


Make the file executable and run the installer with **sudo**:

    elatov@kmac:~/downloads$sudo ./VMware-Workstation-Full-9.0.2-1031769.x86_64.txt
    Extracting VMware Installer...done.
    You must accept the VMware OVF Tool component for Linux End User
    License Agreement to continue.  Press Enter to proceed.
    ..
    ..
    Installing VMware Workstation 9.0.2
        Configuring...
    [######################################################################] 100%
    Installation was successful.


## Compile the VMware Workstation Kernel Modules

Before we do that, let's install all the necessary pre-requisites:

    elatov@kmac:~$sudo yum install kernel-headers gcc kernel-devel


After those are installed, try to compile the kernel modules with the following command:

    elatov@kmac:~$sudo vmware-modconfig --console --install-all


Initially my compile failed with the following error messages:

    /tmp/modconfig-c2Eiux/vmnet-only/hub.c:366:28: error: dereferencing pointer to incomplete type
                 jack->procEntry->read_proc = VNetHubProcRead;
                                ^
    /tmp/modconfig-c2Eiux/vmnet-only/hub.c:367:28: error: dereferencing pointer to incomplete type
                 jack->procEntry->data = jack;
    ..
    ..
    /tmp/modconfig-c2Eiux/vmnet-only/bridge.c: In function ‘VNetBridge_Create’:
    /tmp/modconfig-c2Eiux/vmnet-only/bridge.c:331:34: error: dereferencing pointer to incomplete type
           bridge->port.jack.procEntry->read_proc = VNetBridgeProcRead;
                                      ^
    /tmp/modconfig-c2Eiux/vmnet-only/bridge.c:332:34: error: dereferencing pointer to incomplete type
           bridge->port.jack.procEntry->data = bridge;
                                      ^
    make[2]: *** [/tmp/modconfig-c2Eiux/vmnet-only/bridge.o] Error 1
    make[1]: *** [_module_/tmp/modconfig-c2Eiux/vmnet-only] Error 2
    make[1]: Leaving directory `/usr/src/kernels/3.10.4-300.fc19.x86_64'
    make: *** [vmnet.ko] Error 2


Doing some research I ran into [this](https://communities.vmware.com/thread/453956) Arch Linux page. From that page:

> **VMware module patches and installation**
> VMware Workstation 9 and Player 5 both support kernels up to 3.9. Any later requires patching of the VMware modules.
>
> **3.10 kernels**
> The call create_proc_entry() has been dropped from 3.10 in favor of proc_create(). This requires patching of the vmblock and vmnet modules that use them. The patches (including the optional fuse patch) can be found here and here:
>
>     $ cd /tmp
>     $ curl -O http://pkgbuild.com/git/aur-mirror.git/plain/vmware-patch/vmblock-9.0.2-5.0.2-3.10.patch
>     $ curl -O http://pkgbuild.com/git/aur-mirror.git/plain/vmware-patch/vmnet-9.0.2-5.0.2-3.10.patch
>     $ cd /usr/lib/vmware/modules/source
>     $ tar -xvf vmblock.tar
>     $ tar -xvf vmnet.tar
>     $ patch -p0 -i /tmp/vmblock-9.0.2-5.0.2-3.10.patch
>     $ patch -p0 -i /tmp/vmnet-9.0.2-5.0.2-3.10.patch
>     $ tar -cf vmblock.tar vmblock-only
>     $ tar -cf vmnet.tar vmnet-only
>     $ rm -r vmblock-only
>     $ rm -r vmnet-only
>     $ vmware-modconfig --console --install-all
>

And I was running Kernel 3.10:

    elatov@kmac:~$uname -r
    3.10.5-201.fc19.x86_64


Similar patches can be found [here](http://mysticalzero.blogspot.com/2013/07/vmblock-patch-for-linux-310-vmware.html). After I ran the above commands to apply the patches, the compile went through.

## Entering the License Number

At this point I ran **vmware** from the command line and workstation started up fine. I wanted to enter my license key since the trial only runs for 30 days. I went to Help -> "Enter License Key.." and I saw the following:

![vmware ws enter license key Installing VMware Workstation 9.0.2 on Fedora 19](http://virtuallyhyper.com/wp-content/uploads/2013/08/vmware-ws-enter-license-key.png)

I would click on "Enter License Key.." but nothing would happen. I found two sites that ran into the same issue:

*   [Can't add serial code/activate VMware in Ubuntu 13.04](http://askubuntu.com/questions/285373/cant-add-serial-code-activate-vmware-in-ubuntu-13-04)
*   [Fix: Unable to click on Enter license key for VMWare Workstation](http://platonic.techfiz.info/2013/05/fix-unable-to-click-on-enter-license-key-for-vmware-workstation/)

Both listed a fix, you can either run this:

    $ sudo /usr/lib/vmware/bin/vmware-vmx --new-sn KEY


or you can run this:

    $ sudo /usr/lib/vmware/bin/vmware-enter-serial


The latter will launch a GUI, and you can enter the key into it. I used the first method and it worked without an issue.

## Launch the VMware WorkStation Virtual Network Editor

I tried to run the Virtual Network Editor from the VMware WorkStation but it wouldn't do anything. I checked out **dmesg** and I saw the following:

    elatov@kmac:~$dmesg -T | tail -1
    [Wed Aug 14 18:51:11 2013] vmware-gksu[6702]: segfault at 7fd0bfda24ab ip 00007fd0c4615196 sp 00007fff8df1f608 error 4 in libc-2.17.so[7fd0c44e4000+1b5000]


It looks like **vmware-gksu** is crashing. **vmware-gksu** is a utility that comes with workstation and it's gui to alleviate user's privileges (kind of like **sudo**). Also checking out the application logs (under **/tmp**) I saw the following:

    elatov@kmac:/tmp/vmware-elatov$tail vmware-apploader-9319.log
    2013-08-14T19:07:48.046-07:00| appLoader| I120: GLib: glib_minor_version: Comparing 36 with 36
    2013-08-14T19:07:48.046-07:00| appLoader| I120: libglib-2.0.so.0 validator returned true.
    2013-08-14T19:07:48.046-07:00| appLoader| I120: Marking libglib-2.0.so.0 node as SYSTEM.
    2013-08-14T19:07:48.046-07:00| appLoader| I120: -- Finished processing libglib-2.0.so.0 --
    2013-08-14T19:07:48.046-07:00| appLoader| I120: Marking libgksu2.so.0 node as SHIPPED.
    2013-08-14T19:07:48.046-07:00| appLoader| I120: Marking libgtop-2.0.so.7 node as SHIPPED.
    2013-08-14T19:07:48.046-07:00| appLoader| I120: Marking libXau.so.6 node as SYSTEM.
    2013-08-14T19:07:48.689-07:00| appLoader| W110: Child process was terminated with signal 11.
    2013-08-14T19:07:48.689-07:00| appLoader| W110: Unable to load dependencies for /usr/lib/vmware/lib/libvmware-gksu.so/libvmware-gksu.so
    2013-08-14T19:07:48.689-07:00| appLoader| W110: Unable to execute /usr/lib/vmware/bin/vmware-gksu.


It saw showing the same issue, **vmware-gksu** was having issues. From the *segfault* we can see that we are having an issue with **libc**. I found a lot of people mentioning that there are a lot of bugs with **vmware-gksu** and **libc**. [Here](http://www.kubuntuforums.net/showthread.php?62913) is one example. Manually elevating my privileges with **sudo** worked for me. So I ran this:

    elatov@kmac:~$sudo vmware-netcfg


and then I saw the following:

![network editor started Installing VMware Workstation 9.0.2 on Fedora 19](http://virtuallyhyper.com/wp-content/uploads/2013/08/network-editor-started.png)

I was able to make all the changes that I needed.

