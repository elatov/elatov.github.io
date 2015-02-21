---
published: true
layout: post
title: "Install Gentoo on Samsung Chromebook"
author: Karim Elatov
categories: [OS]
tags: [chromebook,linux,gentoo]
---
So after trying out *chrubuntu* and *arch-linux* on my arm based chromebook I decided to try out *gentoo*. I already had my partitions setup so I didn't have to worry about that. You can check out my previous setups here:

- [Install Arch Linux on Samsung Chromebook](/2014/02/install-arch-linux-samsung-chromebook/)
- [Install ChrUbuntu 12.04 on Samsung Chromebook](/2013/03/install-chrubuntu-12-04-on-samsung-chromebook/)

### Prepare for the Gentoo Install

So I rebooted into ChromeOS and opened up the Crosh Shell. The partitions get automatically mounted on boot:

    localhost ~ # mount | grep 'SD Card'
    /dev/mmcblk1p12 on /media/removable/SD Card type vfat (rw,nosuid,nodev,noexec,relatime,dirsync,uid=1000,gid=1000,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,flush,errors=remount-ro)
    /dev/mmcblk1p2 on /media/removable/SD Card 1 type ext2 (rw,nosuid,nodev,noexec,relatime,dirsync)
    /dev/mmcblk1p3 on /media/removable/SD Card 2 type ext4 (rw,nosuid,nodev,noexec,relatime,dirsync,data=ordered)

So **/media/removable/SD Card 2** is where my root partitions is. First I removed everything from there:

    localhost ~ # cd /media/removable/SD\ Card\ 2
    localhost SD Card 2 # rm -rf *

Depending on your SD card the above might take a while. Now that I have a clean root partition let's get the **stage3** tar from gentoo:

    localhost SD Card 2 # wget http://distfiles.gentoo.org/releases/arm/autobuilds/20141023/stage3-armv7a_hardfp-20141023.tar.bz2

That was the latest at the time, you could run the following at any time to get the latest:

    wget -O - http://distfiles.gentoo.org/releases/arm/autobuilds/$(wget -O - http://distfiles.gentoo.org/releases/arm/autobuilds/latest-stage3-armv7a_hardfp.txt 2>/dev/zero | tail -n1)

After you have the **stage3** tar then extract it:

    localhost SD Card 2 # tar xjf stage3-armv7a_hardfp-20141023.tar.bz2 

After that you will have the necessary directories:

    localhost SD Card 2 # ls 
    bin boot dev etc home lib media mnt opt proc root run sbin stage3-armv7a_hardfp-20141023.tar.bz2 sys tmp usr var

Now let's get the portage files:

    localhost SD Card 2 # wget http://distfiles.gentoo.org/releases/snapshots/current/portage-latest.tar.bz2 

Now let's extract it and put under the **usr** directory within the root partition:

    localhost SD Card 2 # tar xjf portage-latest.tar.bz2 -C usr/

Now let's prepare to chroot into our rootfs:

    localhost ~# mount /dev/mmcblk1p2 /media/removable/SD\ Card\ 2/boot/
    localhost ~ # mount -t proc proc /media/removable/SD\ Card\ 2/proc 
    localhost ~ # mount --rbind /dev /media/removable/SD\ Card\ 2/dev 
    localhost ~ # mount --rbind /sys /media/removable/SD\ Card\ 2/sys 
    localhost ~ # cp -L /etc/resolv.conf /media/removable/SD\ Card\ 2/etc/.

We have to do one more extra thing from ChromeOS and that's enable **exec** on the mounted root partition (this is so we can **chroot**):

    localhost ~ # mount /dev/mmcblk1p3 -o remount,exec

Now to go inside the gentoo chroot:

    localhost ~ # chroot /media/removable/SD\ Card\ 2
    localhost / #

### Prepare for the Kernel Compile 
First let's set the timezone:

    localhost ~ # cp /usr/share/zoneinfo/America/Denver /etc/localtime 
    localhost ~ # echo "America/Denver" > /etc/timezone

As I was checking the profile I realized for some reason the **PORTAGE_CONFIGROOT** was set as the following:

    localhost ~ # env | grep -i roo
    PORTAGE_CONFIGROOT=/usr/local

So I unset it.

    localhost ~ # unset PORTAGE_CONFIGROOT

and after that I saw that my profile is configured appropriately:

    localhost ~ # eselect profile show
    Current /etc/portage/make.profile symlink:
    default/linux/arm/13.0/armv7a

Just for reference here is a list of available profiles:

    localhost ~ # eselect profile list
    Available profile symlink targets:
    [1] default/linux/arm/13.0
    [2] default/linux/arm/13.0/desktop
    [3] default/linux/arm/13.0/desktop/gnome
    [4] default/linux/arm/13.0/desktop/gnome/systemd
    [5] default/linux/arm/13.0/desktop/kde
    [6] default/linux/arm/13.0/desktop/kde/systemd
    [7] default/linux/arm/13.0/developer
    [8] default/linux/arm/13.0/armv4
    [9] default/linux/arm/13.0/armv4/desktop
    [10] default/linux/arm/13.0/armv4/desktop/gnome
    [11] default/linux/arm/13.0/armv4/desktop/kde
    [12] default/linux/arm/13.0/armv4/developer
    [13] default/linux/arm/13.0/armv4t
    [14] default/linux/arm/13.0/armv4t/desktop
    [15] default/linux/arm/13.0/armv4t/desktop/gnome
    [16] default/linux/arm/13.0/armv4t/desktop/kde
    [17] default/linux/arm/13.0/armv4t/developer
    [18] default/linux/arm/13.0/armv5te
    [19] default/linux/arm/13.0/armv5te/desktop
    [20] default/linux/arm/13.0/armv5te/desktop/gnome
    [21] default/linux/arm/13.0/armv5te/desktop/kde
    [22] default/linux/arm/13.0/armv5te/developer
    [23] default/linux/arm/13.0/armv6j
    [24] default/linux/arm/13.0/armv6j/desktop
    [25] default/linux/arm/13.0/armv6j/desktop/gnome
    [26] default/linux/arm/13.0/armv6j/desktop/kde
    [27] default/linux/arm/13.0/armv6j/developer
    [28] default/linux/arm/13.0/armv7a *
    [29] default/linux/arm/13.0/armv7a/desktop
    [30] default/linux/arm/13.0/armv7a/desktop/gnome
    [31] default/linux/arm/13.0/armv7a/desktop/kde
    [32] default/linux/arm/13.0/armv7a/developer
    [33] hardened/linux/arm/armv7a
    [34] hardened/linux/arm/armv6j
    [35] hardened/linux/musl/arm/armv7a
    [36] default/linux/uclibc/arm/armv7a
    [37] hardened/linux/uclibc/arm/armv7a

Before doing anything with **emerge** let's set the default **USE** flags, in the past here is what I ended up with:

    MAKEOPTS="-j2"
    USE="pulseaudio X -ipv6 bindist nvidia alsa \
    bluetooth dbus lm_sensors jpeg lock session udev \
    startup-notification truetype -gnome libnotify bash-completion"
    INPUT_DEVICES="evdev synaptics"

So let's grab **vim** (cause I can't edit files in any other way :) ):

    localhost ~ # emerge -av vim

After installing **vim** I added the above into **/etc/portage/make.conf**.

I built the chromeos kernel previously as descibed [here](/2014/11/install-chromeos-kernel-38-on-samsung-chromebook/) and I noticed there is an [overlay for the chromiumos kernel](http://gpo.zugaina.org/sys-kernel/chromeos-kernel). So I decided to install **layman** and add that **overlay** (similar approach as [this](http://wiki.gentoo.org/wiki/Project:Hardened_musl)). Before we install the **layman** tools let's check out the available **USE** flags for that package (to get **equery** we need to install **gentoolkit**, so first install it with `emerge -av gentoolkit`):

    localhost ~ # equery u layman
    [ Legend : U - final flag setting for installation]
    [        : I - package is installed with flag     ]
    [ Colors : set, unset                             ]
     * Found these USE flags for app-portage/layman-2.0.0-r3:
     U I
     - - bazaar                   : Support dev-vcs/bzr based overlays
     - - cvs                      : Support dev-vcs/cvs based overlays
     + + git                      : Support dev-vcs/git based overlays
     - - mercurial                : Support dev-vcs/mercurial based overlays
     + + python_targets_python2_7 : Build with Python 2.7
     + - subversion               : Support dev-vcs/subversion based overlays
     - - test                     : Workaround to pull in packages needed to run
                                    with FEATURES=test. Portage-2.1.2 handles this
                                    internally, so don't set it in
                                    make.conf/package.use anymore


I wanted layman to support **subversion** and **git** repos, so I created the following **package.use** for **layman**:

    localhost ~ # mkdir /etc/portage/package.use
    localhost ~ # cat /etc/portage/package.use/layman 
    app-portage/layman subversion git

It took about an hour to build all the dependencies:

    localhost ~ # time emerge -av layman
    real 62m9.751s
    user 29m8.785s
    sys 9m19.120s

Then I added the following to **/etc/portage/make.conf** (so **emerge** can install packages from the overlays)

    source /var/lib/layman/make.conf

Then run the following to list the available overlays and to cache them:

    localhost ~ # layman -L

You will see our overlay in the list:

    localhost ~ # layman -L | grep chromi
    * chromiumos [Git ] (http://git.chromium.org/chromiumo...)

Now let's add our overlay

    localhost ~ # layman -a chromiumos

    * Adding overlay,...
    * Warning: an installed db file was not found at: ['/var/lib/layman/installed.xml']
    * Running Git... # ( cd /var/lib/layman && /usr/bin/git clone http://git.chromium.org/chromiumos/overlays/chromiumos-overlay.git/ /var/lib/layman/chromiumos )
    Cloning into '/var/lib/layman/chromiumos'...
    remote: Counting objects: 836823, done.
    remote: Compressing objects: 100% (232899/232899), done.
    remote: Total 836823 (delta 603322), reused 828012 (delta 595801)
    Receiving objects: 100% (836823/836823), 507.51 MiB | 347.00 KiB/s, done.
    Resolving deltas: 100% (603322/603322), done.
    Checking connectivity... done.
    Checking out files: 100% (2933/2933), done.
    * Running Git... # ( cd /var/lib/layman/chromiumos && /usr/bin/git config user.name "layman" )
    * Running Git... # ( cd /var/lib/layman/chromiumos && /usr/bin/git config user.email "layman@localhost" )
    Unavailable repository 'portage-stable' referenced by masters entry in '/var/lib/layman/chromiumos/metadata/layout.conf'
    * Successfully added overlay(s) chromiumos.

After that we should see the desired packages:

    localhost ~ # emerge -s chromeos-kernel
    Searching... 
    [ Results for search key : chromeos-kernel ]
    [ Applications found : 2 ]

    * sys-kernel/chromeos-kernel
    Latest version available: 3.4-r2421
    Latest version installed: [ Not Installed ]
    Size of files: 0 kB
    Homepage: http://www.chromium.org/
    Description: Chrome OS Kernel
    License: GPL-2

    * sys-kernel/chromeos-kernel-next
    Latest version available: 3.8.11-r735
    Latest version installed: [ Not Installed ]
    Size of files: 0 kB
    Homepage: http://www.chromium.org/
    Description: Chrome OS Kernel-next
    License: GPL-2

So then I created the following **USE** flags for the **chromeos-kernel-next** package:

    localhost ~ # cat /etc/portage/package.use/chromeos-kernel-next
    sys-kernel/chromeos-kernel-next board_use_daisy_snow device_tree nfs vfat 

Also before we compile the kernel let's get the **mkimage** binary installed as well

    localhost ~ # emerge -av u-boot-tools

and for the kernel source install

    localhost ~ # emerge -av chromeos-kernel-next

    * IMPORTANT: 8 news items need reading for repository 'gentoo'.
    * Use eselect news to read news items.


    These are the packages that would be merged, in order:

    Calculating dependencies... done!
    [ebuild N ] sys-kernel/chromeos-kernel-next-3.8.11-r735::chromiumos USE="board_use_daisy_snow device_tree nfs vfat -blkdevram -board_use_amd64-corei7 -board_use_amd64-drm -board_use_amd64-generic -board_use_amd64-host -board_use_aries -board_use_arm-generic -board_use_bayleybay -board_use_beaglebone -board_use_beltino -board_use_blackwall -board_use_bolt -board_use_butterfly -board_use_cardhu -board_use_chronos -board_use_daisy -board_use_daisy-drm -board_use_daisy_spring -board_use_dalmore -board_use_emeraldlake2 -board_use_falco -board_use_fb1 -board_use_fox -board_use_fox_baskingridge -board_use_fox_wtm1 -board_use_fox_wtm2 -board_use_ironhide -board_use_kiev -board_use_klang -board_use_leon -board_use_link -board_use_lumpy -board_use_nyan -board_use_panda -board_use_parrot -board_use_parrot32 -board_use_parrot64 -board_use_peach -board_use_peach_kirby -board_use_peach_pit -board_use_peppy -board_use_puppy -board_use_raspberrypi -board_use_ricochet -board_use_slippy -board_use_sonic -board_use_stout -board_use_stout32 -board_use_stumpy -board_use_stumpy_pico -board_use_tegra2 -board_use_tegra2_aebl -board_use_tegra2_arthur -board_use_tegra2_asymptote -board_use_tegra2_dev-board -board_use_tegra2_dev-board-opengl -board_use_tegra2_kaen -board_use_tegra2_seaboard -board_use_tegra2_wario -board_use_tegra3-generic -board_use_waluigi -board_use_wolf -board_use_x32-generic -board_use_x86-agz -board_use_x86-alex -board_use_x86-alex32 -board_use_x86-alex32_he -board_use_x86-alex_he -board_use_x86-alex_hubble -board_use_x86-dogfood -board_use_x86-drm -board_use_x86-fruitloop -board_use_x86-generic -board_use_x86-mario -board_use_x86-mario64 -board_use_x86-pineview -board_use_x86-wayland -board_use_x86-zgb -board_use_x86-zgb32 -board_use_x86-zgb32_he -board_use_x86-zgb_he -ca0132 -cifs -cros_host -cros_workon_tree_7223ac70621a5e856d579090a6d196acea7e2e58 -dyndebug -fbconsole -gdmwimax -gobi -highmem -i2cdev -initramfs -kgdb -kvm -mbim -netboot_ramfs -pcserial -profiling -qmi -realtekpstor -samsung_serial -systemtap -tpm -wifi_testbed_ap -wireless34 -x32" 0 kB

    Total: 1 package (1 new), Size of downloads: 0 kB

    Would you like to merge these packages? [Yes/No] y

    >>> Verifying ebuild manifests

    >>> Emerging (1 of 1) sys-kernel/chromeos-kernel-next-3.8.11-r735 from chromiumos
    * Determining the location of the kernel source code
    * Unable to find kernel sources at /usr/src/linux
    * Please make sure that /usr/src/linux points at your running kernel, 
    * (or the kernel you wish to build against).
    * Alternatively, set the KERNEL_DIR environment variable to the kernel sources location
    * Unable to calculate Linux Kernel version for build, attempting to use running version
    >>> Unpacking source...
    Cloning into bare repository '/usr/portage/distfiles/egit-src/chromiumos/third_party/kernel-next'...
    remote: Counting objects: 3180375, done.
    remote: Compressing objects: 100% (484502/484502), done.
    remote: Total 3180375 (delta 2669534), reused 3177004 (delta 2666534)
    Receiving objects: 100% (3180375/3180375), 679.15 MiB | 433.00 KiB/s, done.
    Resolving deltas: 100% (2669534/2669534), done.
    Checking connectivity... done.
    GIT NEW clone -->
    repository: http://git.chromium.org/chromiumos/third_party/kernel-next.git
    at the commit: 
    commit: 98d6fa96d08dbb08a2150dcd48a6b2a8773172e0
    branch: 
    storage directory: "/usr/portage/distfiles/egit-src/chromiumos/third_party/kernel-next"
    checkout type: bare repository
    Cloning into '/var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work/chromeos-kernel-next-3.8.11'...
    done.
    Checking out files: 100% (43170/43170), done.
    Switched to a new branch 'tree-98d6fa96d08dbb08a2150dcd48a6b2a8773172e0'
    >>> Unpacked to /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work/chromeos-kernel-next-3.8.11
    >>> Source unpacked in /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work
    >>> Preparing source in /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work/chromeos-kernel-next-3.8.11 ...
    >>> Source prepared.
    >>> Configuring source in /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work/chromeos-kernel-next-3.8.11 ...
    * Using kernel config: chromiumos-arm
    chromeos/scripts/prepareconfig: line 17: /var/cache/portage/sys-kernel/chromeos-kernel-next/.config: Permission denied
    * ERROR: sys-kernel/chromeos-kernel-next-3.8.11-r735::chromiumos failed (configure phase):
    * (no error message)

It might fail out on the prepare and that's okay, as long as we got the source. So let's link that kernel source to **/usr/src/linux**:

    localhost ~ # ln -s /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work/chromeos-kernel-next-3.8.11 /usr/src/linux

If you want you can even copy the version over:

    localhost work # pwd
    /var/tmp/portage/sys-kernel/chromeos-kernel-next-3.8.11-r735/work
    localhost work # rsync -avzP chromeos-kernel-next-3.8.11 /usr/src/.
    localhost work # /usr/src
    localhost src # ln -s chromeos-kernel-next-3.8.11 linux
    localhost src # ls -l
    total 4
    drwxr-xr-x 25 portage portage 4096 Feb  4 12:07 chromeos-kernel-next-3.8.11
    lrwxrwxrwx  1 root    root      27 Feb  5 11:21 linux -> chromeos-kernel-next-3.8.11

### Compile the Kernel
So let's prepare the kernel source (I just followed the same steps as I did [before](/2014/11/install-chromeos-kernel-38-on-samsung-chromebook/))

    localhost ~ # cd /usr/src/linux
    localhost linux # ./chromeos/scripts/prepareconfig chromeos-exynos5

Then make sure the config is good:

    localhost linux # make oldconfig

I then enabled some extra options in the kernel:

    localhost linux # make menuconfig

Here are the options I enabled:

**NFS**

    File systems  --->
       Network File Systems  --->
          <M>   NFS client support
          [M]     NFS client support for NFS version 4
          <M>     NFS client support for NFS version 2 (NEW)
          <M>     NFS client support for NFS version 3 (NEW)

    File systems --->
        [*] Dnotify support

**Autofs**

    File systems --->
        <M> Kernel automounter version 4 support (also supports v3)

And here is what I disabled:

**Warnings as Errors**

    Kernel Hacking --->
        [ ] Treat compiler warnings as errors  

**Buffer Overflow Detection**

    Kernel Features --->
      [ ] Enable -fstack-protector buffer overflow detection 

**Chromium OS Security**

    Security Options --->
      < > Chromium OS Security Module


Now let's build the kernel

    localhost linux # time make uImage
    CHK include/generated/uapi/linux/version.h
    CHK include/generated/utsrelease.h
    make[1]: 'include/generated/mach-types.h' is up to date.
    CALL scripts/checksyscalls.sh
    CHK include/generated/compile.h
    Kernel: arch/arm/boot/Image is ready
    Kernel: arch/arm/boot/zImage is ready
    UIMAGE arch/arm/boot/uImage
    Image Name: Linux-3.8.11
    Created: Sun Feb 1 18:18:07 2015
    Image Type: ARM Linux Kernel Image (uncompressed)
    Data Size: 3596560 Bytes = 3512.27 kB = 3.43 MB
    Load Address: 40008000
    Entry Point: 40008000
    Image arch/arm/boot/uImage is ready

    real 21m42.837s
    user 24m30.555s
    sys 2m47.515s

Only 21 minutes :) Now let's build the modules:

    localhost linux # time make modules
    CC sound/usb/snd-usb-audio.mod.o
    LD [M] sound/usb/snd-usb-audio.ko
    CC sound/usb/snd-usbmidi-lib.mod.o
    LD [M] sound/usb/snd-usbmidi-lib.ko

    real 13m43.842s
    user 8m47.570s
    sys 0m59.675s

Now let's install the modules

    localhost linux # make modules_install

Now let's create the device tree files:

    localhost linux # make dtbs

Now let's copy the kernel (uImage) and kernel device tree db into place:

    localhost linux # cp arch/arm/boot/uImage /boot/vmlinux.uimg
    localhost linux # cp arch/arm/boot/dts/exynos5250-snow.dtb /boot/exynos5250-snow.dtb

I configured **nv-u-boot** to be able to read those file and boot from them (so I didn't have to sign them or combine them into one file). The setup was covered [here](/2014/11/install-chromeos-kernel-38-on-samsung-chromebook/). 

### Prepare Gentoo for boot

Let's go ahead and create the **fstab** file:

    localhost ~ # cat /etc/fstab 
    /dev/mmcblk1p3		/		ext4		noatime		0 1
    /dev/mmcblk1p2		/boot		ext2		defaults	1 2
    #/dev/SWAP		none		swap		sw		0 0


Let's setup the networking

    localhost ~ # ln -s /etc/init.d/net.lo /etc/init.d/net.mlan0
    localhost ~ # echo 'hostname="crbook"' > /etc/conf.d/hostname
    localhost ~ # cat /etc/conf.d/net
    modules_mlan0="wpa_supplicant"
    config_mlan0="dhcp"
    localhost ~ # rc-update add net.mlan0 default
    * service net.mlan0 added to runlevel default

Since I only have a wireless card let's install **wpa_supplicant** and **dhcp**:

    localhost ~ # cat /etc/portage/package.use/wpa_supplicant 
    net-wireless/wpa_supplicant wps
    localhost ~ # time emerge -av wpa_supplicant
    real 44m10.542s
    user 18m28.330s
    sys 7m2.500s
    localhost ~ # cat /etc/portage/package.use/dhcp 
    net-misc/dhcp -server
    localhost ~ # emerge -av dhcp

Now let's configure the WPA password:

    localhost ~ # wpa_passphrase wireless 
    # reading passphrase from stdin
    password
    network={
    ssid="wireless"
    #psk="password"
    psk=3776fc67aedd6a6de6
    }

and here is the **wpa_supplicant** config

    localhost ~ # cat /etc/wpa_supplicant/wpa_supplicant.conf 
    network={
    ssid="wireless"
    psk=3776fc67aedd6a6de6
    scan_ssid=1
    proto=WPA2
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    priority=5
    }

Set the root password:

    localhost ~ # passwd 
    New password: 
    Retype new password: 
    passwd: password updated successfully

Let's install **syslog-ng** in case we need troubleshoot anything:

    localhost ~ # time emerge -av syslog-ng
    real 6m57.220s
    user 3m4.085s
    sys 1m11.430s

lastly install the **linux-firmware** files (this way the wireless card can load)

    localhost ~ # emerge -av linux-firmware

At this point your can exit the **chroot**, **unmount** every directory from the rootfs, and **reboot**. You should see **openrc** start appropriate services and then a prompt will be presented where you can login with the **root** user.

### Post Install Configs
After the reboot you can login and confirm the wireless connected:

    crbook ~ # wpa_cli list_networks
    Selected interface 'mlan0'
    network id / ssid / bssid / flags
    0   wireless   any [CURRENT]

Let's generate the locale:

    crbook ~ # grep -vE '^$|^#' /etc/locale.gen
    en_US ISO-8859-1
    en_US.UTF-8 UTF-8
    crbook ~ # locale-gen
     * Generating 2 locales (this might take a while) with 1 jobs
     *  (1/2) Generating en_US.ISO-8859-1 ... [ ok ]
     *  (2/2) Generating en_US.UTF-8 ... [ ok ]
     * Generation complete

Let's also install the dns utils:

    crbook ~ # emerge -av bind-tools

#### Install PFL
There is a utility called **e-file** which can tell you which package provides a certain file, it's part of the **pfl** package so let's install that:

    crbook ~ # emerge -av pfl

Prior to using we have to build the cache:

    crbook ~ # pfl
    ...
    ...
    working on (604 of 607) dev-db/libzdb-3.0
    working on (605 of 607) mail-mta/ssmtp-2.64-r2
    working on (606 of 607) sys-process/psmisc-22.21-r2
    working on (607 of 607) sys-process/procps-3.3.9-r2
    writing xml file /tmp/pfltp8OCc.xml ...
    uploading xml file /tmp/pfltp8OCc.xml ...
    deleting xml file /tmp/pfltp8OCc.xml ...

After that you can run the following:

    crbook ~ # e-file sd8797_uapsta.bin
    [I] sys-kernel/linux-firmware
        Available Versions: 20130728 20130711 20130530 20130421 99999999 20141009 20140902 20140809 20140603 20131230
        Last Installed Ver: 20140902(Sun 01 Feb 2015 08:55:30 PM MST)
        Homepage:       http://git.kernel.org/?p=linux/kernel/git/firmware/linux-firmware.git
        Description:        Linux firmware files
        Matched Files:      /usr/lib/firmware/mrvl/sd8797_uapsta.bin; /lib/firmware/mrvl/sd8797_uapsta.bin;

There is also an updated version which can tell you which files a remote package owns. To install let's download the script:

    crbook ~ # wget https://raw.githubusercontent.com/richardgv/e-file-py/master/e-file-py.py

Then let's install it under **/usr/bin**:

    crbook ~ # cp e-file-py.py /usr/bin/
    crbook ~ # ln -s /usr/bin/e-file-py.py /usr/bin/e-file-py
    crbook ~ # chmod +x /usr/bin/e-file-py.py

It uses the python **beautifulsoup** module so let's install that:

    crbook ~ # emerge -av beautifulsoup

After that you can do things like this:

    crbook ~ # e-file-py -l dev-libs/libgee-0.6.8
    /usr/include/gee-1.0/gee.h
    ..
    ..
    /usr/lib/libgee.so
    /usr/lib/libgee.so.2
    /usr/lib/libgee.so.2.0.0
    /usr/lib/pkgconfig/gee-1.0.pc
    /usr/lib64/girepository-1.0/Gee-1.0.typelib
    /usr/lib64/libgee.so
    /usr/lib64/libgee.so.2
    /usr/lib64/libgee.so.2.0.0
    /usr/lib64/pkgconfig/gee-1.0.pc

#### Install eix
There is another cool tool called **eix** which gives a pretty concise view of what versions and USE flags a certain package contains. So let's install that:

    crbook ~ # emerge -av eix

To just create the cache for eix we can run the following:

    crbook ~ # eix-update
    Reading Portage settings ..
    Building database (/var/cache/eix/portage.eix) ..
    [0] 'gentoo' /usr/portage/ (cache: metadata-md5-or-flat)
         Reading category 166|166 (100%) Finished             
    Applying masks ..
    Calculating hash tables ..
    Writing database file /var/cache/eix/portage.eix ..
    Database contains 18219 packages in 166 categories.

To sync portage and then run **eix-update** we can run the following:

    crbook ~ # eix-sync

This will run the following

    emerge --sync
    eix-update
    eix-diff

If you want the **eix-sync** command to update **overlays** (ie run **layman -S**), then create the following

    crbook ~ # cat /etc/eix-sync.conf
    *

Then the **eix-sync** command will do this

    emerge --sync
    laymans -S
    eix-update
    eix-diff

I ended up adding the following to **crontab** (after instaling **vixie-cron**):

    crbook ~ # crontab -l | grep -i eix
    00 04 * * * /usr/bin/eix-update -q

After it's ready you can check versions like this:

    crbook ~ # eix libgee
    * dev-libs/libgee
         Available versions:  
         (0)    0.6.7 0.6.8
         (0.8)  0.14.0 ~0.16.1(0.8/2)
           {+introspection}
         Homepage:            https://wiki.gnome.org/Projects/Libgee
         Description:         GObject-based interfaces and classes for commonly used data structures

#### Install hwinfo

Let's instal **hwinfo** since **lspci** doesn't work. First we need to allow that package to be complied on our platform, that's done with the **package.accept_keywords**. So I created the following file:

    crbook ~ # cat /etc/portage/package.accept_keywords/hwinfo
    sys-apps/hwinfo **

And then install the package

    crbook ~ # emerge -av hwinfo

Now we cancheck out a summary of the machine:

    crbook ~ # hwinfo --short
    cpu:
                           CPU
                           CPU
    keyboard:
      /dev/input/event0    cros-ec-i2c
    network interface:
      mlan0                Ethernet network interface
      uap0                 Ethernet network interface
      p2p0                 Ethernet network interface
      lo                   Loopback network interface
    disk:
      /dev/mmcblk0rpmb     Disk
      /dev/mmcblk0boot0    Disk
      /dev/mmcblk0boot1    Disk
      /dev/mmcblk0         Disk
      /dev/mmcblk1         Disk
    partition:
      /dev/mmcblk0p1       Partition
      /dev/mmcblk0p2       Partition
      /dev/mmcblk0p3       Partition
      /dev/mmcblk0p4       Partition
      /dev/mmcblk0p5       Partition
      /dev/mmcblk0p6       Partition
      /dev/mmcblk0p7       Partition
      /dev/mmcblk0p8       Partition
      /dev/mmcblk0p9       Partition
      /dev/mmcblk0p10      Partition
      /dev/mmcblk0p11      Partition
      /dev/mmcblk0p12      Partition
      /dev/mmcblk1p1       Partition
      /dev/mmcblk1p2       Partition
      /dev/mmcblk1p3       Partition
      /dev/mmcblk1p12      Partition
    hub:
                           Linux 3.8.11 ehci_hcd S5P EHCI Host Controller
                           Standard Microsystems Hub
                           Linux 3.8.11 ohci_hcd EXYNOS OHCI Host Controller
                           Linux 3.8.11 xhci-hcd xHCI Host Controller
                           Linux 3.8.11 xhci-hcd xHCI Host Controller
    memory:
                           Main Memory
    unknown:
                           Generic WebCam SC-03FFM12339N

You can also just get the CPU information:

    crbook ~ # hwinfo --cpu
    01: None 00.0: 10103 CPU                                        
      [Created at cpu.269]
      Unique ID: rdCR.j8NaKXDZtZ6
      Hardware Class: cpu
      Arch: ARM
      Vendor: "ARM Limited"
      Model: 0.4.0 ""
      Platform: "SAMSUNG EXYNOS5 (Flattened Device Tree)"
      Features: swp,half,thumb,fastmult,vfp,edsp,thumbee,neon,vfpv3,tls,vfpv4,idiva,idivt,
      BogoMips: 199.30
      Config Status: cfg=new, avail=yes, need=no, active=unknown

    02: None 01.0: 10103 CPU
      [Created at cpu.269]
      Unique ID: wkFv.j8NaKXDZtZ6
      Hardware Class: cpu
      Arch: ARM
      Vendor: "ARM Limited"
      Model: 0.4.0 ""
      Platform: "SAMSUNG EXYNOS5 (Flattened Device Tree)"
      Features: swp
      BogoMips: 199.30
      Config Status: cfg=new, avail=yes, need=no, active=unknown

#### Setup Video
The defaults are okay so let's just emerge Xorg-Server:

    crbook ~ # time emerge -av xorg-server
    real    98m56.704s
    user    134m16.475s
    sys 15m27.490s

The main reason it took so long is because it had to compile **llvm**. If you ever
want to find out how long a compile took you can use the **genlop** utility. First install it:

    crbook ~ # emerge -av genlop

and then you can run the following to find out how long a specific package took to compile:

    crbook ~ # genlop -t llvm
     * sys-devel/llvm

         Mon Feb  2 05:49:38 2015 >>> sys-devel/llvm-3.5.0
           merge time: 51 minutes and 54 seconds.

If there is an emerge going in the background you can check how it will take to finish (estimating from the last compile time):

    crbook ~ # genlop -c

     Currently merging 1 out of 1

     * www-client/chromium-41.0.2272.16

           current merge time: 1 hour, 14 minutes and 44 seconds.
           ETA: 8 hours, 9 minutes and 8 seconds.

For the window manager I use **icewm**, I ended up installing an older version cause the latest one was causing Focus issues:

    crbook ~ # emerge -av =x11-wm/icewm-1.3.8

I then held (**masked**) the other version by creating the following file:

    crbook ~ # cat /etc/portage/package.mask/icewm
    =x11-wm/icewm-1.3.9

This way if a newer version comes out, the emerge world will pick up an update but skip that specific version. And now let's get the display manager

    crbook ~ # time emerge -av lightdm
    real    89m53.930s
    user    92m24.960s
    sys     18m43.525s

To enable the display manager to start on boot we have to enable the following services:

    crbook ~ # rc-update add dbus default
     * service dbus added to runlevel default
    crbook ~ # rc-update add xdm default
     * service xdm added to runlevel default

and set the following option:

    crbook ~ # grep DISPLAY /etc/conf.d/xdm
    DISPLAYMANAGER="lightdm"

For the configs I just copied the old configs from my arch linux machine (but the setup was covered [here](/2013/03/install-chrubuntu-12-04-on-samsung-chromebook/)). Here is the jist of it:

    mkdir ~/backup
    mv /etc/X11/xorg.conf.d/* ~/backup/
    cd /etc/X11/xorg.conf.d/
    wget http://craigerrington.com/chrome/x_alarm_chrubuntu.zip
    unzip x_alarm_chrubuntu.zip
    rm x_alarm_chrubuntu.zip
    sed -i 's/gb/us/g' 10-keyboard.conf

After a reboot I was able to login and start an icewm-session without issue. I also added the following **udev** rule to dim the brightness on boot, the default one is the highest one and it's just a waste of battery:

    crbook ~ # cat /etc/udev/rules.d/81-backlight.rules
    SUBSYSTEM=="backlight", ACTION=="add", KERNEL=="backlight.10", ATTR{brightness}="1000"

#### Configure Audio
Let's install **pulseaudio** and **alsa**

    crbook ~ # emerge -av pulseaudio

For alsa create the following **package.use** settings:

    crbook ~ # cat /etc/portage/package.use/alsa-plugins
    media-plugins/alsa-plugins libsamplerate
    crbook ~ # time emerge -av alsa-utils alsa-plugins
    real    4m0.621s
    user    2m32.865s
    sys     0m40.975s

If you want any changes you made in **alsamixer** to stick during reboot we need to enable the following service:

    crbook ~ # rc-update add alsasound boot
     * service alsasound added to runlevel boot

And make sure restore and save options are enabled:

    crbook ~ # grep -Ev '^#|^$' /etc/conf.d/alsasound
    RESTORE_ON_START="yes"
    SAVE_ON_STOP="yes"

After that you should see the available sound cards with **aplay**:

    crbook ~ # aplay -l
    **** List of PLAYBACK Hardware Devices ****
    card 0: DAISYI2S [DAISY-I2S], device 0: Playback HiFi-0 []
      Subdevices: 1/1
      Subdevice #0: subdevice #0
    card 0: DAISYI2S [DAISY-I2S], device 1: Capture HiFi-1 []
      Subdevices: 1/1
      Subdevice #0: subdevice #0

You can also make sure the UCM profile is appropriately used for the Daisy Sound Card (this ensures the appropriate channels are already um-muted):

    crbook ~ # alsaucm listcards
      0: DAISY-I2S
        Daisy internal card
      1: PandaBoard
      2: PandaBoardES
      3: SDP4430
      4: tegraalc5632

Lastly enable **alsa** to be loaded by **pulseaudio**:

    crbook ~ # grep alsa-sink /etc/pulse/default.pa 
    load-module module-alsa-sink

#### Configure Browser

I ended compiling **chromium**, first I had to enable all the right options for all the packages:

    crbook ~ # cat /etc/portage/package.use/harfbuzz
    media-libs/harfbuzz icu
    crbook ~ # cat /etc/portage/package.use/zlib
    sys-libs/zlib minizip
    crbook ~ # cat /etc/portage/package.use/libxml2
    dev-libs/libxml2 icu
    crbook ~ # cat /etc/portage/package.use/chromium
    www-client/chromium -bindist neon
    crbook ~ # cat /etc/portage/package.accept_keywords/re2
    dev-libs/re2 ~arm
    crbook ~ # cat /etc/portage/package.accept_keywords/jsoncpp
    dev-libs/jsoncpp ~arm
    crbook ~ # cat /etc/portage/package.accept_keywords/chromium
    www-client/chromium ~arm

The compile took 9 hours:

    crbook ~ # time emerge -av chromium
    real    565m29.370s
    user    999m18.375s
    sys     78m33.000s

To get the flash I ended borrowing the package from arch linux:

    crbook ~ # wget http://us.mirror.archlinuxarm.org/armv7h/alarm/chromium-pepper-flash-12.0.0.77-1-armv7h.pkg.tar.xz

Then I extracted it:

    crbook ~ # tar xvzf chromium-pepper-flash-12.0.0.77-1-armv7h.pkg.tar.xz

and the copied it to **/usr/lib**:

    crbook ~ # rsync -avzP usr/lib/. /usr/lib/.

Lastly configured the browser to look for that version:

    crbook ~ # cat /etc/chromium/default
    # Default settings for chromium. This file is sourced by /bin/bash from
    # the chromium launcher.

    # Options to pass to chromium.
    #CHROMIUM_FLAGS=""
    CHROMIUM_FLAGS=" --ppapi-flash-path=/usr/lib/PepperFlash/libpepflashplayer.so --ppapi-flash-version=12.0.0.77"

After that flash worked on the chromium browser.


#### Misc Configs

To enable **rc.log** (just to see what services fail during boot), I ended up modifying the following:

    crbook ~ # $ grep ^rc_log /etc/rc.conf
    rc_logger="YES"
    rc_log_path="/var/log/rc.log"

To enable the power button to actually shutdown the laptop just had to install **acpid**:

    crbook ~ # emerge -av acpid
    crbook ~ # service acpid start
    crbook ~ # rc-update add acpid default

Ran into an issue with **freerdp** (it kept trying to use the wrong float abi... the issue is described [here](https://github.com/FreeRDP/FreeRDP/issues/980)). So I just manually compiled it, first got the source:

    crbook ~ # git clone https://github.com/FreeRDP/FreeRDP.git
    crbook ~ # cd FreeRDP

Here is the command to prepare the source (I included the **-DARM_FP_ABI=hard** flag):

    crbook FreeRDP #cmake -DCMAKE_INSTALL_PREFIX=/usr -DWITH_ALSA=ON -DWITH_CLIENT=ON -DWITH_CUPS=OFF -DWITH_DEBUG_ALL=OFF -DWITH_MANPAGES=OFF -DWITH_FFMPEG=OFF -DWITH_GSTREAMER_1_0=OFF -DWITH_JPEG=ON -DWITH_PULSE=ON -DWITH_SERVER=OFF -DWITH_PCSC=OFF -DWITH_SSE2=OFF -DCHANNEL_URBDRC=OFF -DWITH_X11=ON -DWITH_XINERAMA=OFF -DWITH_XV=OFF -DBUILD_TESTING=OFF -DWITH_WAYLAND=OFF -DARM_FP_ABI=hard

To install just run the following:

    crbook FreeRDP # make install

After compiling **keepass** it failed to start with the following error:

    mini-codegen.c:807, condition `i == sel' not met

I found a couple of bugs on that:

- [mono doesn't work on hard float abi on ARM](https://bugzilla.xamarin.com/show_bug.cgi?id=7938)
- [Mono < 3.4.0 - 3.8.x fails on armhf platforms with Windows Form including textbox](https://bugzilla.xamarin.com/show_bug.cgi?id=20239)

and it's the same as the **freerdp** issue, it's not compiling using the hard float abi. It seems later versions fix the issue. I found an *overlay* which contained later versions. So first I added the overlay:

    crbook ~ # layman -a dotnet

Then create the appropriate **packake.accept_keywords**:

    crbook ~ # cat /etc/portage/package.accept_keywords/mono 
    dev-lang/mono ~arm

I found the latest version with **eix**:

    crbook ~ # eix dev-lang/mono
    [?] dev-lang/mono
         Available versions:  *2.10.9-r2^t ~*3.0.7 ~*3.2.3 ~*3.2.8 ~*3.10.0[1] ~*3.12.0[1] **9999[1] {debug doc minimal nls pax_kernel xen}
         Installed versions:  3.12.0[1](04:16:58 PM 02/15/2015)(nls -debug -doc -minimal -pax_kernel -xen)
         Homepage:            http://www.mono-project.com/Main_Page
         Description:         Mono runtime and class libraries, a C# compiler/interpreter

    * dev-lang/mono-basic
         Available versions:  *2.10^t
         Homepage:            http://www.mono-project.com/VisualBasic.NET_support
         Description:         Visual Basic .NET Runtime and Class Libraries

    [1] "dotnet" /var/lib/layman/dotnet

and the installed the latest version:

    crbook ~ # emerge -av =dev-lang/mono-3.12.0

This would've worked too:

    crbook ~ # emerge -av mono

Then after recompiling **keepass** and it started up without issues:

    crbook ~ # emerge -av keepass

Installed the Oracle Embedded Java version, first downloaded it from their site and extracted it:

    crbook ~ # tar xzf jdk-8u33-linux-arm-vfp-hflt.tar.gz

Then put it under **/usr/local**

    crbook ~ # mv jdk1.8.0_33/ /usr/local/.

Now let's create the link to java

    crbook ~ # ln -s /usr/local/jdk1.8.0_33/bin/java /usr/local/bin/java

Here is the version:

    crbook ~ # java -version
    java version "1.8.0_33"
    Java(TM) SE Runtime Environment (build 1.8.0_33-b05)
    Java HotSpot(TM) Client VM (build 25.33-b05, mixed mode)

I was able to use that version with other application without issues. 

I added the following configuration to switch to **tty1** if the system is shutting down:

    crbook ~ # cat /etc/local.d/00_shutdown.stop
    /usr/bin/chvt 1

This way I could see what services are shutting down during a system halt or reboot.
