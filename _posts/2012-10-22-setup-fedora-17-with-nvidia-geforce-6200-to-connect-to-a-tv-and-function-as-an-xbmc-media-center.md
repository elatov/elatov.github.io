---
title: Setup Fedora 17 with nVidia GeForce 6200 Video Card to Connect to a TV and Function as an XBMC Media Center
author: Karim Elatov
layout: post
permalink: /2012/10/setup-fedora-17-with-nvidia-geforce-6200-to-connect-to-a-tv-and-function-as-an-xbmc-media-center/
dsq_thread_id:
  - 1404673670
categories:
  - Home Lab
  - OS
tags:
  - .xinitrc
  - /etc/default/grub
  - /etc/gdm/custom.conf
  - /etc/sysconfig/desktop
  - /etc/systemd/system/default.target
  - /lib/kbd/consolefonts
  - akmod-nvidia
  - akmods
  - console font
  - 'CPU0: Core temperature above threshold'
  - dracut
  - GDM
  - gfxpayload
  - GRUB_CMDLINE_LINUX
  - GRUB_GFXPAYLOAD_LINUX
  - iptables
  - nouveau
  - Nvidia GeForce 6200
  - nvidia-xconfig
  - RPMFusion
  - setfont
  - setsysfont
  - startx
  - systemd runlevel
  - thermal paste
  - tv-out
  - vga=789
  - XBMC Remote
  - Xorg-Server
  - xorg-x11-drv-nvidia
  - xorg.conf
---
I was getting the following messages on the my Fedora machine:

    [10500.000015] [Hardware Error]: Machine check events logged 
    [10525.702091] CPU0: Core temperature above threshold, cpu clock throttled (total events = 63858) 
    [10525.702995] CPU0: Core temperature/speed normal 
    [10650.000047] [Hardware Error]: Machine check events logged
    

I decided to dust out the machine and to add some new thermal paste to alleviate the over heating. In the process of dusting out the machine, I noticed that the fan on my video card doesn&#8217;t work. Also, after I applied a brand new layer of thermal paste, my retention clip for the heat sink broke. My &#8220;alleviation&#8221; plan was not very successful, to say the least.

I decided to order a brand new video card and a new heat sink ( I couldn&#8217;t find the retention clip by it self, every where I looked it always came with the heat sink). While I was in the ordering mood I decided to get an s-video to composite cable as well. This way I could connect this old PC to my TV so it can connect as a client to my media server. Here the parts I ordered:

*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16814130452&name=Desktop-Graphics-Cards" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16814130452&name=Desktop-Graphics-Cards']);">Nvidia GeForce 6200 AGP Video Card</a>
*   <a href="http://www.amazon.com/dp/B004MUDR36/?tag=virtuallyhyper.com-20" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.amazon.com/dp/B004MUDR36/?tag=virtuallyhyper.com-20']);" rel="nofollow">Intel Aluminum Heat Sink & 2.5&#8243; Fan w/Retention Clip</a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=9SIA0PG08P9430" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=9SIA0PG08P9430']);">S-Video with 3.5mm Audio to 3 RCA Composite Cable</a>

After all the parts came in: I added the video card, applied a new layer of thermal paste, clipped in my new heat sink, and connected the video card using s-video port to the TV with the composite cable.

The machine was just used for sharing files and didn&#8217;t even have Xorg installed on it. So I decided to install Xorg on the machine. I also knew that I would need a display manager so I went with GDM. I then installed both:

    moxz:~> sudo yum install gdm xorg-x11-server-Xorg
    

Next I needed to set the computer to use GDM as my display manager. From the Fedora Documentation &#8220;<a href="http://docs.fedoraproject.org/en-US/Fedora/12/html/Deployment_Guide/s2-x-runlevels-5.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.fedoraproject.org/en-US/Fedora/12/html/Deployment_Guide/s2-x-runlevels-5.html']);">Runlevel 5</a>&#8220;:

> **20.5.2. Runlevel 5**
> 
> When the system boots into runlevel 5, a special X client application called a display manager is launched. A user must authenticate using the display manager before any desktop environment or window managers are launched. Depending on the desktop environments installed on the system, three different display managers are available to handle user authentication.
> 
> *   GNOME — The default display manager for Fedora, GNOME allows the user to configure language settings, shutdown, restart or log in to the system.
> *   KDE — KDE&#8217;s display manager which allows the user to shutdown, restart or log in to the system.
> *   xdm — A very basic display manager which only lets the user log in to the system. When booting into runlevel 5, the prefdm script determines the preferred display manager by referencing the /etc/sysconfig/desktop file

I looked over the */usr/share/doc/initscripts-9.37.1/sysconfig.txt* file , and I saw the following:

    moxz:~>grep '/desktop' /usr/share/doc/initscripts-9.37.1/sysconfig.txt -A 10 
    /etc/sysconfig/desktop: 
    DESKTOP=GNOME|KDE This determines the default desktop for new users.
    
    Optional values from earlier releases:
    
        DISPLAYMANAGER=GNOME|KDE|WDM|XDM
          This determines display manager started by /etc/X11/prefdm,
          independent of the desktop. This can be accomplished in current
          releases merely by just installing the preferred display manager.
    

So I setup up my */etc/sysconfig/desktop* file to look like this:

    moxz:~>cat /etc/sysconfig/desktop 
    DISPLAYMANAGER=GNOME
    

I then needed to change my init level from 3 to 5. From the Fedora <a href="http://fedoraproject.org/wiki/Systemd#How_do_I_change_the_default_runlevel.3F" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://fedoraproject.org/wiki/Systemd#How_do_I_change_the_default_runlevel.3F']);">Systemd</a> Documentation:

> **How do I change the default runlevel?**
> 
> systemd uses symlinks to point to the default runlevel. You have to delete the existing symlink first before creating a new one
> 
>     rm /etc/systemd/system/default.target
>     
> 
> Switch to runlevel 3 by default
> 
>     ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target
>     
> 
> Switch to runlevel 5 by default
> 
>     ln -sf /lib/systemd/system/graphical.target /etc/systemd/system/default.target
>     
> 
> systemd does not use /etc/inittab file.

I ran the following to setup my Fedora machine to boot into runlevel 5:

    moxz:~>sudo rm /etc/systemd/system/default.target 
    moxz:~>sudo ln -sf /lib/systemd/system/graphical.target /etc/systemd/system/default.target
    

I rebooted my machine, but when X started the display manager just kept scrolling up and down like the refresh rate was off or something. I then ran across this article &#8220;<a href="http://en.wikibooks.org/wiki/NVidia/TV-OUT" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikibooks.org/wiki/NVidia/TV-OUT']);">nVidia/TV-OUT</a>&#8221; and it had a really good step by step process on how to generate a proper *xorg.conf* file for a tv-out setup. After following the instructions, I had created the following *xorg.conf* file:

    moxz:~>cat /etc/X11/xorg.conf 
    Section "Device" 
        Identifier "Card_tv" 
        Driver "nouveau" 
        BusID "PCI:1:0:0" 
        Option "TVOutFormat" "SVIDEO" 
        Option "TVStandard" "PAL-M" 
        Option "ConnectedMonitor" "TV" 
    EndSection
    
    Section "Monitor" 
        Identifier "TV" 
        HorizSync 30-50 
        VertRefresh 60 
    EndSection
    
    Section "Screen" 
        Identifier "Screen_tv" 
        Device "Card_tv" 
        Monitor "TV" 
        DefaultDepth 16 
        SubSection "Display" 
            Depth 16 
            Modes "1024x768" "800x600" 
        EndSubSection 
    EndSection
    
    Section "ServerLayout" 
         Identifier "tv" 
         Screen 0 "Screen_tv" 0 0 
    EndSection
    

Even after that xorg.conf file was in place it still didn&#8217;t help. I then decided to install the nVidia driver. Here a <a href="http://www.nvidia.com/object/linux_display_ia32_1.0-7664.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nvidia.com/object/linux_display_ia32_1.0-7664.html']);">link</a> to the driver. As I tried to install the driver:

    moxz:~>chmod +x NVIDIA-Linux-x86-1.0-7664-pkg1.run 
    moxz:~>sudo init 3 
    moxz:~>sudo ./NVIDIA-Linux-x86-1.0-7664-pkg1.run
    

it would error out with the following message:

    ERROR: Unable to build the NVIDIA kernel module. 
    ERROR: Installation has failed. 
    Please see the file '/var/log/nvidia-installer.log' for details. 
    You may find suggestions on fixing installation problems in the README available on the Linux driver download page at www.nvidia.com.
    

As I ran into that issue I started to think; what would happen if I installed a new kernel? Would I have to track down nVidia issues every time? I wanted to find the nVidia kernel module in the yum repositories so it would be auto installed with every kernel update. So then I ran into the Fedora <a href="http://fedoraproject.org/wiki/Cuda#Install_NVIDIA_libraries" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://fedoraproject.org/wiki/Cuda#Install_NVIDIA_libraries']);">Cuda</a> Documenation. From the page it had instructions on how to install the kernel module:

1.  Enable rpm fusion repository
2.  Install the necessary nVidia libraries
3.  Install the kernel nNidia module

I did some more digging around and I discovered that for step #3 there are two options. From &#8220;<a href="http://www.unixmen.com/how-to-install-nvidia-drivers-in-fedora-13-and-14/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.unixmen.com/how-to-install-nvidia-drivers-in-fedora-13-and-14/']);">How To Install Nvidia Drivers In Fedora 17 Beefy Miracle</a>&#8220;:

> Now install Nvidia drivers:
> 
>     yum install kmod-nvidia xorg-x11-drv-nvidia-libs.i686
>     
> 
> Or akmod :
> 
> Using akmod-nvidia instead of kmod-nvidia will make the system automatically build the nVidia driver for your kernel if no pre-built binary is available. This can avoid confusing situations where X will not start after a kernel update. akmod builds the required kmod on bootup. Thanks to (vcato)
> 
>     yum install akmod-nvidia xorg-x11-drv-nvidia-libs.i686
>     

The *akmod* option sounded perfect for my setup. I also checked out the RPM Fusion page on <a href="http://rpmfusion.org/Packaging/KernelModules/Akmods" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://rpmfusion.org/Packaging/KernelModules/Akmods']);">Akmods</a>, from the page:

> **Akmods**
> 
> **Quick Overview**
> 
> RPM Fusion/Livna distributes kernel-modules as kmod packages that contain modules precompiled for the latest kernels released by Fedora. That works fine for most people, but it doesn&#8217;t work on systems with use different kernel &#8212; like a self-compiled kernel, an older Fedora kernel or the quickly changing kernels from updates-testing/rawhide. The kmods-srpms can easily be rebuilt for those kernels using rpmbuild with a kmod-specific parameter that defines what kernel to build the kmod for. But that requires some knowledge of how to build rpms; this is what the script akmods tries to make easier for the end user, as it does all the steps required to build a kmod.rpm for the running kernel from a kmod-srpm.
> 
> But the user still needs to do something manually when he needs a kmod for a newly installed kernel. This is what the akmodsd daemon is trying to fix: it&#8217;s a script normally started from init on bootup that checks if all kmods are present. If a kmod is not found then akmods tries to rebuild kmod.srpms found in a certain place in the filesystem; if that works it will install the rebuilt kmod into the running kernel automatically.
> 
> This is similar to dkms, but has one important benefit: one only needs to maintain a single kmod spec file which can be used both in the repos buildsystem and on the clients systems if needed.

I decided to try out the *akmod* install.

So here is what I did to install the nVidia driver:

    moxz:~>yum localinstall --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm 
    moxz:~>yum localinstall --nogpgcheck http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm 
    moxz:~>yum install xorg-x11-drv-nvidia-libs moxz:~>yum install akmod-nvidia
    

After I had installed the nVidia driver, I looked over the nVidia page entitled &#8220;<a href="http://http.download.nvidia.com/XFree86/Linux-x86/1.0-8762/README/chapter-03.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://http.download.nvidia.com/XFree86/Linux-x86/1.0-8762/README/chapter-03.html']);">Configuring X for the NVIDIA Driver</a>&#8221; and from that page:

> **Using nvidia-xconfig to configure the X server**
> 
> nvidia-xconfig will find the X configuration file and modify it to use the NVIDIA X driver. In most cases, you can simply answer &#8220;Yes&#8221; when the installer asks if it should run it. If you need to reconfigure your X server later, you can run nvidia-xconfig again from a terminal. nvidia-xconfig will make a backup copy of your configuration file before modifying it.

I decided to start from scratch just to see what happens, so here is what I did:

    moxz:~>sudo mv /etc/X11/xorg.conf /etc/X11/xorg.conf.orig 
    moxz:~>sudo nvidia-xconfig
    WARNING: Unable to locate/open X configuration file.
    New X configuration file written to '/etc/X11/xorg.conf'
    

The last command created the following *xorg.conf* file:

    moxz:~>cat /etc/X11/xorg.conf  
    # nvidia-xconfig: X configuration file generated by nvidia-xconfig
    # nvidia-xconfig: version 304.37 (mockbuild@) Tue Aug 14 06:34:11 CEST 2012
    
    Section "ServerLayout" 
        Identifier "Layout0" 
        Screen 0 "Screen0" 
        InputDevice "Keyboard0" "CoreKeyboard" 
        InputDevice "Mouse0" "CorePointer" 
    EndSection
    
    Section "Files" 
    EndSection
    
    Section "InputDevice" 
        # generated from default 
        Identifier "Mouse0" 
        Driver "mouse" 
        Option "Protocol" "auto" 
        Option "Device" "/dev/input/mice" 
        Option "Emulate3Buttons" "no" 
        Option "ZAxisMapping" "4 5" 
    EndSection
    
    Section "InputDevice" 
        # generated from data in "/etc/sysconfig/keyboard" 
        Identifier "Keyboard0" 
        Driver "kbd" 
        Option "XkbLayout" "us" 
        Option "XkbModel" "pc105" 
    EndSection
    
    Section "Monitor" 
        Identifier "Monitor0" 
        VendorName "Unknown" 
        ModelName "Unknown" 
        HorizSync 28.0 - 33.0 
        VertRefresh 43.0 - 72.0 
        Option "DPMS" 
    EndSection
    
    Section "Device" 
        Identifier "Device0" 
        Driver "nvidia" 
        VendorName "NVIDIA Corporation" 
    EndSection
    
    Section "Screen" 
        Identifier "Screen0" 
        Device "Device0" 
        Monitor "Monitor0" 
        DefaultDepth 24 
        SubSection "Display" 
            Depth 24 
            Modes "1024x768" "800x600" "720x480" "640x480" "640x400" 
        EndSubSection 
    EndSection
    

I then rebooted and the boot up process looked better but GDM didn&#8217;t even start. I then ran across this article &#8220;<a href="http://www.if-not-true-then-false.com/2012/fedora-17-nvidia-guide/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.if-not-true-then-false.com/2012/fedora-17-nvidia-guide/']);">Fedora 17 nVidia Drivers Install Guide (disable nouveau driver)</a>&#8220;. From that article:

> 1.  Remove/disable nouveau drivers from kernel initramfs `## Backup old initramfs nouveau image`  
>     `mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r)-nouveau.img`  
>     `## Create new initramfs image`  
>     `dracut /boot/initramfs-$(uname -r).img $(uname -r)`

I followed the above instructions to disable the nouveau driver, to ensure that only nVidia drivers would be used/loaded. Here is what I ran:

    moxz:~>sudo mv /boot/initramfs-`uname -r`.img /boot/initramfs-`uname -r`-nouveau.img moxz:~>sudo dracut -v /boot/initramfs-`uname -r`.img `uname -r` 
    I: Including module: i18n
    I: Including module: rpmversion
    I: Including module: plymouth
    I: Including module: crypt 
    I: Including module: dm
    I: Skipping udev rule: 64-device-mapper.rules 
    I: Including module: dmraid
    I: Including module: kernel-modules 
    I: Possible missing firmware "aic94xx-seq.fw" for kernel module "aic94xx.ko" 
    I: Possible missing firmware "ct2fw.bin" for kernel module "bfa.ko" 
    I: Possible missing firmware "ctfw.bin" for kernel module "bfa.ko" 
    I: Possible missing firmware "cbfw.bin" for kernel module "bfa.ko" 
    I: Possible missing firmware "ql2500_fw.bin" for kernel module "qla2xxx.ko" 
    I: Possible missing firmware "ql2400_fw.bin" for kernel module "qla2xxx.ko" 
    I: Possible missing firmware "ql2322_fw.bin" for kernel module "qla2xxx.ko" 
    I: Possible missing firmware "ql2300_fw.bin" for kernel module "qla2xxx.ko" 
    I: Possible missing firmware "ql2100_fw.bin" for kernel module "qla2xxx.ko" 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver nfs_acl 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Omitting driver lockd 
    I: Including module: lvm 
    I: Skipping udev rule: 64-device-mapper.rules 
    I: Including module: mdraid 
    I: Including module: resume 
    I: Including module: rootfs-block 
    I: Including module: terminfo 
    I: Including module: udev-rules 
    I: Skipping udev rule: 50-udev.rules 
    I: Skipping udev rule: 95-late.rules 
    I: Skipping udev rule: 50-firmware.rules 
    I: Including module: usrmount 
    I: Including module: base 
    I: Including module: fs-lib 
    I: Skipping program jfs_fsck as it cannot be found and is flagged to be optional 
    I: Skipping program reiserfsck as it cannot be found and is flagged to be optional 
    I: Skipping program btrfsck as it cannot be found and is flagged to be optional 
    I: Including module: shutdown 
    I: Skipping program kexec as it cannot be found and is flagged to be optional 
    I: Including modules done  
    I: Creating image file
    I: Wrote /boot/initramfs-3.3.4-5.fc17.i686.img: 
    I: -rw------- 1 root root 16268569 Oct 21 11:50 /boot/initramfs-3.3.4-5.fc17.i686.img
    

After I ran that I also noticed that the *nouveau* module was actually blacklisted by the *rpmfusion* install:

    moxz:~>cat /etc/modprobe.d/blacklist-nouveau.conf
    # RPM Fusion blacklist for nouveau driver - you need to run as root:
    # dracut -f /boot/initramfs-$(uname -r).img $(uname -r)
    # if nouveau is loaded despite this file.
    blacklist nouveau
    

One more reboot and my GDM finally started up without refresh issues.I then tried to login, but my keyboard wasn&#8217;t working. I checked out */var/log/Xorg.0.log* file and I saw the following:

    [ 44868.805] (EE) Failed to load module "evdev" (module does not exist, 0) 
    [ 44868.805] (EE) No input driver matching `evdev' 
    [ 44868.805] (II) config/udev: Adding input device NMB Dell USB 7HK Keyboard (/d ev/input/event2) 
    [ 44868.805] (**) NMB Dell USB 7HK Keyboard: Applying InputClass "evdev keyboard catchall" 
    [ 44868.805] (**) NMB Dell USB 7HK Keyboard: Applying InputClass "system-setup-keyboard"
    

I then installed the **evdev** module:

    moxz:~> yum search evdev 
    ============================== N/S Matched: evdev ============================== 
    xorg-x11-drv-evdev.i686 : Xorg X11 evdev input driver 
    xorg-x11-drv-evdev-devel.i686 : Xorg X11 evdev input driver development package.
    
    Name and summary matches only, use "search all" for everything. 
    moxz:~> sudo yum install -y xorg-x11-drv-evdev.i686
    

After that, I restarted and the keyboard started to work with Xorg just fine. I also wanted to ensure that the *nouveau* wasn&#8217;t loaded:

    moxz:~>lsmod | grep nouveau 
    moxz:~>lsmod | grep nvidia 
    nvidia 10245243 40 
    i2c_sis96x,nvidia,asb100
    

That confirmed it. Then I logged in and installed xbmc:

    moxz:~> sudo yum install xbmc
    

I was able to launch XBMC and all was working as expected.

However when I wanted to check out some settings on the machine by hitting CTLR-ALT-F3 (the local tty) the text was very garbled and I could not see what I was typing at all. So the Xorg font was okay but the console font was a out of sync. I wanted to see if the text was also looking bad during boot so I decided to disable graphical boot. To do so, I followed the instructions laid out in the <a href="http://docs.fedoraproject.org/en-US/Fedora/17/html/Installation_Guide/ch10s04.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.fedoraproject.org/en-US/Fedora/17/html/Installation_Guide/ch10s04.html']);">Fedora Install Guide</a>. From the guide:

> **10.4.1. Trouble With the Graphical GRUB Screen on an x86-based System?**
> 
> If you are experiencing problems with GRUB, you may need to disable the graphical boot screen. To do this, temporarily alter the setting at boot time before changing it permanently. * At boot time, press **Esc** to reach the GRUB splash screen. Select the GRUB line, and type **e**. * Edit the kernel line to remove **rhgb**. \* Press Enter to exit the editing mode. \* Once the boot loader screen has returned, type **b** to boot the system.
> 
> If your problems with GRUB are now resolved and you want to make the change permanent,
> 
> *   become the root user and edit the /etc/default/grub file.
> *   Within the grub file, comment out the line which begins with GRUB_TERMINAL=console by inserting the # character at the beginning of the line.
> *   Refresh the grub.cfg file by running grub2-mkconfig with root privileges. The changes you have made will then take effect. 
> 
> You may re-enable the graphical boot screen by uncommenting (or adding) the above line back into the /etc/default/grub file.

I edited my */etc/default/grub* file and changed the following lines to look like this:

    GRUB_CMDLINE_LINUX="quiet" 
    GRUB_TERMINAL="console"
    

I then generated a new grub menu:

    moxz:~>sudo grub2-mkconfig -o /boot/grub2/grub.cfg 
    Generating grub.cfg ... 
    Found linux image: /boot/vmlinuz-3.3.4-5.fc17.i686 
    Found initrd image: /boot/initramfs-3.3.4-5.fc17.i686.img 
    Found Microsoft Windows XP Professional on /dev/sda1 done
    

After I rebooted the font actually looked readable but it was really small. I tried to increase the font but for some reason I couldn&#8217;t make it anything above size 16. I ssh&#8217;ed to the machine and I checked out the available fonts:

    moxz:~>ls /lib/kbd/consolefonts/ | grep latar 
    latarcyrheb-sun16.psfu.gz 
    latarcyrheb-sun32.psfu.gz
    

I tried setting a smaller font, and I saw the change on the screen:

    moxz:~>sudo setfont -v latarcyrheb-sun16 -C /dev/tty3 
    Loading 512-char 8x16 font from file /lib/kbd/consolefonts/latarcyrheb-sun16.psfu.gz 
    Loading Unicode mapping table...
    

but as soon as I would try anything higher it didn&#8217;t work:

    moxz:~> sudo setfont -v latarcyrheb-sun32 -C /dev/tty3 
    Loading 512-char 16x32 font from file /lib/kbd/consolefonts/latarcyrheb-sun32.psfu.gz 
    putfont: KDFONTOP: Invalid argument
    

I thought it might have been a font issue, so I searched for some console fonts:

    moxz:~> yum search console font 
    ========================== N/S Matched: console, font ========================== 
    bitmap-console-fonts.noarch : Selected set of bitmap fonts 
    terminus-fonts-console.noarch : Clean fixed width font (console version)
    
    Full name and summary matches only, use "search all" for everything.
    

I already had the top one, so I went ahead and installed the *terminus* fonts. After I installed the font I checked out the README file and I saw the following:

    moxz:~>cat /lib/kbd/consolefonts/README.terminus
    
    names   mappings        covered codepage(s)
    
    ter-1*  iso01, iso15, cp1252    ISO8859-1, ISO8859-15, Windows-1252
    ter-2*  iso02, cp1250       ISO8859-2, Windows-1250
    ter-7*  iso07, cp1253       ISO8859-7, Windows-1253
    ter-9*  iso09, cp1254       ISO8859-9, Windows-1254
    ter-c*  cp1251, iso05       Windows-1251, ISO8859-5
    ter-d*  iso13, cp1257       ISO8859-13, Windows-1257
    ter-g*  iso16           ISO8859-16
    ter-i*  cp437           IBM-437
    ter-k*  koi8r           KOI8-R
    ter-m*  mik         Bulgarian-MIK
    ter-p*  pt154           Paratype-PT154
    ter-u*  koi8u           KOI8-U
    ter-v*  all listed above    all listed above and many others (about 110
                and many others     language sets), 8 foreground colors
    
    names   style
    
    ter-*n  normal
    ter-*b  bold
    ter-*f  framebuffer-bold
    

So I tried loading the &#8216;&#42;ter-v&#42;*&#8217; one (since it included most of the fonts and encodings), like so:

    moxz:~>sudo setfont -v ter-v32n -C /dev/tty3 
    Loading 512-char 16x32 font from file /lib/kbd/consolefonts/ter-v32n.psf.gz putfont: 
    KDFONTOP: Invalid argument
    

But it still gave me the same error. I then ran across <a href="http://ubuntuforums.org/showthread.php?t=1667602" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://ubuntuforums.org/showthread.php?t=1667602']);">this</a> Ubuntu forum. They fixed the issue by changing the console resolution via the *vga=792* option in their grub configuration. I wanted to find out what setting I should use . After some googling around I ran into this article &#8220;<a href="http://forum.linuxcareer.com/threads/1661-Change-tty-font-size-with-Grub-2-boot-console-resolution" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.linuxcareer.com/threads/1661-Change-tty-font-size-with-Grub-2-boot-console-resolution']);">Change tty font size with Grub 2 boot console resolution</a>&#8220;. From the article:

> Increasing/decreasing font size on tty consoles is linked to a console resolution. Therefore, to increase your font size you need to decrease a console screen resolution by changing grub2 default settings. Please note that your Ubuntu Linux is using grub2 so looking inside /boot/grub/menu.lst would not do any help. Instead we concentrate on /etc/default/grub file.

There is also a pretty good table of the desired resolutions:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/console_resolution_tab.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/console_resolution_tab.png']);"><img class="alignnone size-full wp-image-4347" title="console_resolution_tab" src="http://virtuallyhyper.com/wp-content/uploads/2012/10/console_resolution_tab.png" alt="console resolution tab Setup Fedora 17 with nVidia GeForce 6200 Video Card to Connect to a TV and Function as an XBMC Media Center" width="404" height="169" /></a>

So I made the following change to my */etc/default/grub* file:

    GRUB_CMDLINE_LINUX="quiet vga=789"
    

and then I regenerated my *grub.cfg* file:

    moxz:~> sudo grub2-mkconfig -o /boot/grub2/grub.cfg 
    Generating grub.cfg ... 
    Found linux image: /boot/vmlinuz-3.3.4-5.fc17.i686 
    Found initrd image: /boot/initramfs-3.3.4-5.fc17.i686.img 
    Found Microsoft Windows XP Professional on /dev/sda1 done
    

I then rebooted and I was able to change my font to anything I wanted. I hit CTRL-ALT-F3 on the machine, and then I ssh&#8217;ed to the machine and ran the following:

    moxz:~>sudo setfont -v latarcyrheb-sun32 -C /dev/tty3 
    Loading 512-char 16x32 font from file /lib/kbd/consolefonts/latarcyrheb-sun32.psfu.gz 
    Loading Unicode mapping table... 
    moxz:~>sudo setfont -v ter-v32n -C /dev/tty3 
    Loading 512-char 16x32 font from file /lib/kbd/consolefonts/ter-v32n.psf.gz 
    Loading Unicode mapping table...
    

I saw the font change on the TV as I was running the above commands. I actually liked the terminus font, so I left that one. I rebooted one more time and I actually noticed a message that said:

    VGA=789 is deprecated. Use set gfxpayload=800x600x24, 800x600 using the linux command instead
    

Searching for that error on goodle, I saw <a href="http://askubuntu.com/questions/61233/what-does-grub-setting-grub-gfxpayload-linux-text" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://askubuntu.com/questions/61233/what-does-grub-setting-grub-gfxpayload-linux-text']);">this</a> article. From that article:

> **13.1.9 gfxpayload**
> 
> If this variable is set, it controls the video mode in which the Linux kernel starts up, replacing the ‘vga=’ boot option (see linux). It may be set to ‘text’ to force the Linux kernel to boot in normal text mode, ‘keep’ to preserve the graphics mode set using ‘gfxmode’, or any of the permitted values for ‘gfxmode’ to set a particular graphics mode (see gfxmode).
> 
> Depending on your kernel, your distribution, your graphics card, and the phase of the moon, note that using this option may cause GNU/Linux to suffer from various display problems, particularly during the early part of the boot sequence. If you have problems, set this variable to ‘text’ and GRUB will tell Linux to boot in normal text mode.
> 
> The default is platform-specific. On platforms with a native text mode (such as PC BIOS platforms), the default is ‘text’. Otherwise the default may be ‘auto’ or a specific video mode.
> 
> This variable is often set by &#8220;GRUB\_GFXPAYLOAD\_LINUX&#8221;

I then ran across <a href="https://help.ubuntu.com/community/ChangeTTYResolution" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://help.ubuntu.com/community/ChangeTTYResolution']);">ChangeTTYResolution</a>. From that article:

> 1.  Karmic Koala has switched to GRUB 2, and now the settings can be found in the file /etc/default/grub
> 2.  Resolutions available to GRUB 2 can be displayed by typing vbeinfo in the GRUB 2 command line. The command line is accessed by typing &#8220;c&#8221; when the main GRUB 2 menu screen is displayed. (Hold the left shift key pressed before ubuntu loads to access it)
> 3.  Open /etc/default/grub with your text editor with root privilege. Add the following new line using your preferred resolution-depth from the list that vbeinfo gave you. It should be like this if you have a 1280&#215;800 screen:
>     
>         GRUB_GFXPAYLOAD_LINUX=1280x800
>         
> 
> 4.  Save the file and exit. (If you can&#8217;t save the file you haven&#8217;t opened it as root, go back and execute gksudo gedit /etc/default/grub providing your password.)
> 
> 5.  Execute the command
>     
>         sudo update-grub
>         
> 
> 6.  Restart your computer.

I rebooted the machine and then in grub menu typed &#8216;c&#8217;. That went into the grub shell. From there I ran the following:

    set pager=1 
    vbeinfo
    

That gave me a list of all the available resolutions. I decided to set it to 800&#215;600 since that is what the message showed :). I rebooted and then edited my */etc/default/grub* file to have the following:

    GRUB_CMDLINE_LINUX="quiet" 
    GRUB_GFXPAYLOAD_LINUX=800x600
    

And then I rebuilt the grub configuration:

    moxz:~> sudo grub2-mkconfig -o /boot/grub2/grub.cfg 
    Generating grub.cfg ... 
    Found linux image: /boot/vmlinuz-3.3.4-5.fc17.i686
    Found initrd image: /boot/initramfs-3.3.4-5.fc17.i686.img
    Found Microsoft Windows XP Professional on /dev/sda1 done
    

After I rebooted the font looked awesome. To change the font permanently you can edit your */etc/sysconfig/i18n* file and make the following change:

    SYSFONT="ter-v32n"
    

and the font change will stay across reboots. After you make the above change, you can make sure it&#8217;s working by running:

    moxz:~>sudo setsysfont
    

From the man page of *setsysfont*:

> DESCRIPTION setsysfont sets the console font for current virtual terminal. The font setting is read from /etc/sysconfig/i18n.

So *setsysfont* will read the defined font from */etc/sysconfig/i18n* and apply that font to the current terminal.

The last thing I wanted to do is setup XBMC to login automatically. After I installed GDM, I noticed that one of the drop down options for a window manager was XBMC. So all I had to do was run *gdmsetup* and set my user to auto login to that session. I was surprised to learn that *gdmsetup* was deprecated and the replacement utility is currently under development. For more information check out <a href="https://bugzilla.redhat.com/show_bug.cgi?id=439881" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bugzilla.redhat.com/show_bug.cgi?id=439881']);">this</a> RHEL bug. From the bugzilla page:

> http://fedoraproject.org/wiki/Features/NewGdm has the enlightening text for &#8220;Release notes&#8221;: Explain that gdmsetup got replaced by a yet-to-be-written new configuration tool

After looking over &#8220;<a href="https://wiki.archlinux.org/index.php/GDM#GDM_Will_Not_Load_After_Attempting_to_Set-Up_Automatic_Login" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.archlinux.org/index.php/GDM#GDM_Will_Not_Load_After_Attempting_to_Set-Up_Automatic_Login']);">Custom GDM Configuration For Auto And Timed Login</a>&#8221; and <a href="https://help.gnome.org/admin/gdm/stable/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://help.gnome.org/admin/gdm/stable/']);">Gnome Display Manager Reference Manual</a>, I ended up adding the following:

    [daemon] 
    AutomaticLoginEnable=true 
    AutomaticLogin=elatov 
    TimedLoginEnable=true 
    TimedLogin=elatov 
    TimedLoginDelay=0 
    DefaultSession=XBMC.desktop
    

to the */etc/gdm/custom.conf* file. You can get a list of available desktop sessions by doing the following:

    moxz:~>ls /usr/share/xsessions/ 
    icewm.desktop 
    XBMC.desktop
    

So I only had icewm and XBMC installed. After I added the above and rebooted, the XMBC &#8220;window manager&#8221; started up automatically.

If for whatever reason, you need to have a second non-XBMC X-session, you can hit CTRL-ALT-F3, login as a regular user, and define a window manager you want to use by default. This is done by creating a *.xinitrc* file and specifying the window manager of your choice. Here is how mine looked like:

    moxz:~>cat .xinitrc 
    icewm-session
    

Then you can run:

    moxz:~>startx -- :1
    

That will start a second X server with icewm as a window manager. When you are done, just stop that X server by running CTRL-ALT-BACKSPACE and that will get you back to your terminal (tty).

After everything was setup I went ahead and installed an app on my android phone to remotely control the XBMC Media Center. Here is a <a href="http://code.google.com/p/android-xbmcremote" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://code.google.com/p/android-xbmcremote']);">link</a> to the app.

After I installed &#8220;XBMC Remote&#8221; on my phone, I enabled the &#8220;XBMC Media Center&#8221; to be controlled remotely. To do that, you have to go to &#8220;System&#8221; -> &#8220;Settings&#8221; -> &#8220;Network&#8221; -> &#8220;Services&#8221; -> and check &#8220;Allow Control of XBMC via HTTP&#8221;. Also set a password for authentication purposes. Here is a screenshot of how the config looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/xbmc_remote_control.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/xbmc_remote_control.png']);"><img class="alignnone size-full wp-image-4348" title="xbmc_remote_control" src="http://virtuallyhyper.com/wp-content/uploads/2012/10/xbmc_remote_control.png" alt="xbmc remote control Setup Fedora 17 with nVidia GeForce 6200 Video Card to Connect to a TV and Function as an XBMC Media Center" width="1280" height="800" /></a>

Then I opened up port 8080 on the server so my android phone can connect to it over the wireless network at my home. Here is the command I used to allow access to the port:

    moxz:~>sudo iptables -I INPUT 4 -s 192.168.1.0/24 -m tcp -p tcp --dport 8080 -j ACCEPT
    

I then saved the *iptables* settings.

    moxz:~>sudo /usr/libexec/iptables.init save 
    iptables: Saving firewall rules to /etc/sysconfig/iptables:
    

And that is all it took <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Setup Fedora 17 with nVidia GeForce 6200 Video Card to Connect to a TV and Function as an XBMC Media Center" class="wp-smiley" title="Setup Fedora 17 with nVidia GeForce 6200 Video Card to Connect to a TV and Function as an XBMC Media Center" /> I was able to watch videos on my TV from my PC and use my phone as a remote control for my PC.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 2 System Initialization" href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-2-system-initialization/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-2-system-initialization/']);" rel="bookmark">RHCSA and RHCE Chapter 2 System Initialization</a>
    </li>
  </ul>
</div>

