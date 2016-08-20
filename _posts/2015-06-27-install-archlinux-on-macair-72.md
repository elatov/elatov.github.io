---
published: true
layout: post
title: "Install ArchLinux on MacAir 7,2"
author: Karim Elatov
categories: [os]
tags: [archlinux]
---
I decided to convert my Fedora install (setup [here](/2015/04/install-fedora-21-on-macair-72/)) into an ArchLinux install. Most of the partitions had been setup by Fedora and here how is they	 looked:

    elatov@macair:~$df -Ph
    Filesystem               Size  Used Avail Use% Mounted on
    devtmpfs                 3.9G     0  3.9G   0% /dev
    tmpfs                    3.9G  128K  3.9G   1% /dev/shm
    tmpfs                    3.9G  960K  3.9G   1% /run
    tmpfs                    3.9G     0  3.9G   0% /sys/fs/cgroup
    /dev/mapper/fedora-root   20G  8.2G   11G  44% /
    tmpfs                    3.9G  692K  3.9G   1% /tmp
    /dev/sda5                477M  140M  308M  32% /boot
    /dev/sda4                200M   16M  185M   8% /boot/efi
    tmpfs                    789M  8.0K  789M   1% /run/user/1000

    elatov@macair:~$sudo fdisk -l

    Disk /dev/sda: 113 GiB, 121332826112 bytes, 236978176 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disklabel type: gpt
    Disk identifier: CDC959FA-64F6-42A1-B6E0-C12080E8F40F

    Device         Start       End   Sectors   Size Type
    /dev/sda1         40    409639    409600   200M EFI System
    /dev/sda2     409640 186509543 186099904  88.8G Apple Core storage
    /dev/sda3  186509544 187779079   1269536 619.9M Apple boot
    /dev/sda4  187781120 188190719    409600   200M Apple HFS/HFS+
    /dev/sda5  188190720 189214719   1024000   500M Linux filesystem
    /dev/sda6  189214720 236976127  47761408  22.8G Linux LVM

    Disk /dev/mapper/fedora-root: 20.4 GiB, 21890072576 bytes, 42754048 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/mapper/fedora-swap: 2.4 GiB, 2520776704 bytes, 4923392 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes

### Arch Linux Bootable USB

Since the MacAir doesn't have a CD-Drive, we can use a USB disk to perform the install. I downloaded the ISO from [here](https://www.archlinux.org/download/) and ended up with the following file:

    elatov@macair:~$ls -l download/archlinux-2015.06.01-dual.iso
    -rw-r-----@ 1 elatov  elatov  667942912 Jun 27 13:28 download/archlinux-2015.06.01-dual.iso

After plugging in the USB disk MacOS X mounted it automatically and I saw the following:

    elatov@macair:~$diskutil list
    /dev/disk0
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *121.3 GB   disk0
       1:                        EFI EFI                     209.7 MB   disk0s1
       2:          Apple_CoreStorage                         95.3 GB    disk0s2
       3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3
       4:                  Apple_HFS Linux HFS+ ESP          209.7 MB   disk0s4
       5: 0FC63DAF-8483-4772-8E79-3D69D8477DE4               524.3 MB   disk0s5
       6:                  Linux LVM                         24.5 GB    disk0s6
    /dev/disk1
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:                  Apple_HFS Macintosh HD           *94.9 GB    disk1
                                     Logical Volume on disk0s2
                                     4A1016AD-AB13-4A6E-9DAE-640AFBB812FB
                                     Unencrypted
    /dev/disk2
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:     FDisk_partition_scheme                        *8.0 GB     disk2
       1:                 DOS_FAT_32 USB                     8.0 GB     disk2s1

**/dev/disk2** is my USB disk. From [here](https://wiki.archlinux.org/index.php/USB_flash_installation_media) it looks like we can just **dd** the ISO onto the USB disk, so let's umount it:

    elatov@macair:~$diskutil unmountDisk /dev/disk2
    Unmount of all volumes on disk2 was successful

Now let's **dd** the iso onto the USB (notice **/dev/disk2** vs **/dev/rdisk2**):

    elatov@macair:~$sudo dd if=download/archlinux-2015.06.01-dual.iso of=/dev/rdisk2 bs=1m
    637+0 records in
    637+0 records out
    667942912 bytes transferred in 124.024175 secs (5385586 bytes/sec)

### Prepare for the Arch Linux Install
After I rebooted, I held the *Option* key and I saw the USB drive as a bootable device. After I booted from it, I saw the following menu:

![ArchLinux_Boot_Menu](https://dl.dropboxusercontent.com/u/24136116/blog_pics/archlinux-macair/ArchLinux_Boot_Menu.jpg)

and after selecting the first menu I saw a shell:

    Arch Linux 4.0.4-2-ARCH (tty1)

    archiso login: root (automatic login)
    root@archiso ~ # 


Since the fedora install named the LVMs with the title of "**fedora**" I went ahead and renamed it to be generic, just so I know what's it used for:

    root@archiso ~ # vgrename fedora vgos
     Volume group "fedora" successfully renamed to "vgos"

I went ahead and mounted the partitions and removed everything from them since they had fedora stuff on them:

    root@archiso ~ # mount /dev/mapper/vgos-root /mnt
    root@archiso ~ # rm -rf /mnt/*
    zsh: sure you want to delete all the files in /mnt [yn]?y
    root@archiso ~ # mkdir /mnt/boot
    root@archiso ~ # mount /dev/sda5 /mnt/boot
    root@archiso ~ # rm -rf /mnt/boot/*
    zsh: sure you want to delete all the files in /mnt/boot [yn]?y
	root@archiso ~ # mkfs.vfat -F 32 /dev/sda4
    mkfs.fat 3.0.27 (2014-11-12)
    root@archiso ~ # mkdir /mnt/boot/efi
    root@archiso ~ # mount /dev/sda4 /mnt/boot/efi

I had a rooted andoid phone so I plugged it in and enabled USB tethering on it and I was able to get an IP:

    root@archiso ~ # ip link
    1: lo <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2. enp0s20u1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
         link/ether 12:34:56:23:34:45 brd ff:ff:ff:ff:ff:ff
    root@archiso ~ # dhcpcd enp0s20u1
    enp0s20u1: adding address fe80::56::5452:3423
    enp0s20u1: waiting for carrier
    enp0s20u1: carrier acquired
    enp0s20u1: IAID 7f:f5:44:9f
    enp0s20u1: soliciting a DHCP lease
    enp0s20u1: soliciting an IPv6 router
    enp0s20u1: offered 192.168.42.172 from 192.168.42.129
    enp0s20u1: leased 192.168.42.173 for 3600 seconds
    enp0s20u1: adding router to 192.168.42.0/24
    enp0s20u1: adding default route via 192.168.42.129
    root@archiso ~ # ip -4 a s enp0s20u1
    2: enp0s20u1: <BROADCAST,MULTICAST> mtu 1500 qdisc fq_codel state UNKNOWN mode DEFAULT group default qlen 1000
       inet 192.168.42.173/24 brd 192.168.42.255 scope global enp0s20u1
           valid_lft forever preffered_lft forever

### Installing Arch Linux

After I was online I ran the following to get the **base** install of Arch Linux:

    root@archiso ~ # pacstrap /mnt base base-devel
    ...
    ...
    pacstrap /mnt base base-devel 28.46s user 8.77s system 5% cpu 10:51.47 total

Then I generated the **fstab** file:

    root@archiso ~ # genfstab -U -p /mnt >> /mnt/etc/fstab
    root@archiso ~ # cat /mnt/etc/fstab
    # /dev/mapper/vgos-root
    UUID=51ad3d0a-d02e-4b31-b57d-2d50187a3c81	/         	ext4      	rw,relatime,data=ordered	0 1

    # /dev/sda5
    UUID=bd516c1b-2337-417f-a201-f9990412f057	/boot     	ext4      	rw,relatime,stripe=4,data=ordered	0 2

    # /dev/sda4
    UUID=087B-BB74      	/boot/efi 	vfat      	rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,errors=remount-ro	0 2

### Chroot and Configure Arch Linux
After that I setup the passwd and timezone for the system:

    root@archiso ~ # arch-chroot /mnt /bin/bash
    [root@archiso /] # passwd
    [root@archiso /] # echo macair > /etc/hostname
    [root@archiso /] # ln -s /usr/share/zoneinfo/America/Denver /etc/localtime
    [root@archiso /] # useradd -m -u 1000 -U -G wheel -s /bin/bash elatov
    [root@archiso /] # passwd elatov

I also enabled the **wheel** group to be able to use **sudo**:

    [root@archiso /] # echo "%wheel ALL=(ALL) ALL" > /etc/sudoers.d/10-grant-wheel-group

To setup the **locale** I modified the **/etc/locale.gen** to enable the desired locales ( and generated them afterwards):

    [root@archiso /] # grep -v '^#' /etc/local.gen
    en_US.UTF-8 UTF-8
    en_US ISO-8859-1
    [root@archiso /] # locale-gen
    Generating locales...
      en_US.UTF-8...done
      en_US.ISO-8859-1 ...
    Generation complete.
    [root@archiso /] # echo 'LANG="en_US.UTF-8"' > /etc/locale.conf

Prior to generating the RAM disk I ensured the **lvm** module is included:

    [root@archiso /] # grep ^HOOKS /etc/mkinitcpio.conf
    HOOKS="base udev autodetect modconf block lmv2 filesystems keyboard fsck"

And now the **mkinicpio** command:

    [root@archiso /] # mkinitcpio -p linux
    ==> Building image from preset: /etc/mkinitcpio.d/linux.preset: 'default'
      -> -k /boot/vmlinuz-linux -c /etc/mkinitcpio.conf -g /boot/initramsfs-linux.img
    ==> Starting build: 4.0.6-1-ARCH
      -> Running build hook: [base]
      -> Running build hook: [udev]
      -> Running build hook: [autodetect]
      -> Running build hook: [modconf]
      -> Running build hook: [block]
      -> Running build hook: [lvm2]
      -> Running build hook: [filesystems]
      -> Running build hook: [keyboard]
      -> Running build hook: [fsck]
    ==> Generating module dependencies
    ==> Creating gzip-compressed initcpio image: /boot/initramfs-linux.img
    ==> Image generation successful
    ==> Building image from preset: /etc/mkinitcpio.d/linux.preset: 'fallback'
      -> -k /boot/vmlinuz-linux -c /etc/mkinitcpio.conf -g /boot/initramsfs-linux-fallback.img -S autodetect
    ==> Starting build: 4.0.6-1-ARCH
      -> Running build hook: [base]
      -> Running build hook: [udev]
      -> Running build hook: [modconf]
      -> Running build hook: [block]
    ==> WARNING: Possibly missing firmware for module wd719x
    ==> WARNING: Possibly missing firmware for module aic94xx
      -> Running build hook: [lvm2]
      -> Running build hook: [filesystems]
      -> Running build hook: [keyboard]
      -> Running build hook: [fsck]
    ==> Generating module dependencies
    ==> Creating gzip-compressed initcpio image: /boot/initramfs-linux-fallback.img
    ==> Image generation successful

### Install Boot Loader
I followed the instructions laid out in [here](https://wiki.archlinux.org/index.php/MacBook#Installing_GRUB_to_EFI_partition_directly) to install GRUB. I already had the correct partition (FAT 32) mounted under **/boot/efi** as per the above commands. Now I just had to install the GRUB tools:

    [root@archiso /] # pacman install grub-efi-x86_64 efibootmgr

Then I ran the following:

    [root@archiso /] # grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=arch_grub --recheck --debug
    ...
    ...
    grub-install: info: copying `/boot/grub/x86_64-efi/core.efi' -> `/boot/efi/EFI/arch_grub/grubx64.efi'.
    grub-install: info: Registering with EFI: distributor = `arch_grub', path = `\EFI\arch_grub\grubx64.efi', ESP at hostdisk//dev/sda,gpt4.
    grub-install: info: executing efibootmgr --version </dev/null >/dev/null.
    grub-install: info: executing modprobe -q efivars.
    grub-install: info: executing efibootmgr -c -d /dev/sda -p 4 -w -L arch_grub -l \EFI\arch_grub\grubx64.efi.
    BootCurrent: 0000
    Timeout: 5 seconds
    BootOrder: 0001,0000,0080
    Boot0000* Fedora
    Boot0080* Mac OS X
    Boot0081* Mac OS X
    BootFFFF* 
    Boot0001* arch_grub
    Installation finished. No error reported.

    [root@archiso /] # cp /boot/grub/locale/en\@quot.mo /boot/grub/locale/en.mo

Lastly I generated the GRUB menu:

    [root@archiso /] #grub-mkconfig -o /boot/grub/grub.cfg
    Generating grub configuration file ...
      /run/lvm/lvmetad.socket: connect failed: No such file or directory
      WARNING: Failed to connect to lvmetad: Falling back to internal scanning.
    Found linux image: /boot/vmlinuz-linux
    Found initrd image: /boot/initramfs-linux.img
    Found fallback initramfs image: /boot/initramfs-linux-fallback.img
      /run/lvm/lvmetad.socket: connect failed: No such file or directory
      WARNING: Failed to connect to lvmetad: Falling back to internal scanning.
    done

At this point I wanted to see if everything worked out, so I exited the **choot**, un-mounted all the partitions, and rebooted:

    [root@archiso /] # exit
    exit
    arch-choot /mnt /bin/bash 16.79s user 7.22s system 0% cpu 44:33.37 total
    root@archiso ~ # umount /mnt/boot/efi
    root@archiso ~ # umount /mnt/boot
    root@archiso ~ # umount /mnt
    root@archiso ~ # reboot

After the reboot I saw the GRUB menu and Arch Linux was the only available option, which is what I had expected.

### Post Install Setup

#### Install Yaourt
I was still using the usb tethering after I rebooted. Let's install the **yaourt** utitility which will allow us to install packages from AUR. We can just enable their repo and then install the necessary packages as per [this](https://wiki.archlinux.org/index.php/Unofficial_user_repositories#archlinuxfr) page:

    [elatov@macair ~]$ tail -3 /etc/pacman.conf 
    [archlinuxfr]
    SigLevel=Never
    Server=http://repo.archlinux.fr/$arch

Now let's refresh all the repos:

    [elatov@macair ~]$ sudo pacman -Sy
    :: Synchronizing package databases...
     core is up to date
     extra is up to date
     community  is up to date
     archlinuxfr 									2.7 MiB   432K/s 00:06 [############################################################] 100%

Now we can just run:

    [elatov@macair ~]$ sudo pacman -S yaourt

#### Install Wireless Driver
Prior to installing the **wl** kernel module, let's get the prereq packages:

    [elatov@macair ~]$sudo pacman -S dkms wpa_supplicant linux-headers

Now let's install the **wl** module so we can use the wireless and stop tethering:

    [elatov@macair ~]$ yaourt -S broadom-wl-dkms
    ...
    ...
    Building module:
    cleaning build area....
    make KERNELRELEASE=4.0.6-1-ARCH -C /usr/lib/modules/4.0.6-1-ARCH/build M=/var/lib/dkms/broadcom-wl/6.30.223.248/build....
    cleaning build area....
    Kernel cleanup unnecessary for this kernel.  Skipping...

    DKMS: build completed.

    wl.ko:
    Running module version sanity check.
     - Original module
       - No original module exists within this kernel
     - Installation
       - Installing to /usr/lib/modules/4.0.6-1-ARCH/kernel/drivers/net/wireless/

    depmod....

    DKMS: install completed.
    It's recommended to execute the following commands to load the module:
    rmmod b43 2>/dev/null
    rmmod b43legacy 2>/dev/null
    rmmod ssb 2>/dev/null
    rmmod bcm43xx 2>/dev/null
    rmmod brcm80211 2>/dev/null
    rmmod brcmfmac 2>/dev/null
    rmmod brcmsmac 2>/dev/null
    rmmod bcma 2>/dev/null
    modprobe wl

    /usr/bin/depmod -a


At this point it's a good idea to enable the **dkms** service so it compiles the module when a new kernel is installed:

    [elatov@macair ~]$ sudo systemctl enable dkms

Now let's make sure none of the conflicting modules are loaded:

    [elatov@macair ~]$ lsmod | grep ssb
    [elatov@macair ~]$ lsmod | grep b43

And now let's load the **wl** module:

    [elatov@macair ~]$ sudo modprobe wl
    [   384.38342  ] wl0: online cpus 1

And now we will see our wireless card:

    [elatov@macair ~]$ ip link
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DORMANT group default qlen 1000
        link/ether ge:ge:ge:ge:ge:ge brd ff:ff:ff:ff:ff:ff

#### Configure Wireless Networking

Now let's connect to a wireless network:

    [elatov@macair ~]$ sudo pacman -S dialog
    [elatov@macair ~]$ sudo wifi-menu -o

Then select your network and enter the password for the wireless network and then enable it to connect on boot:

    [elatov@macair ~]$ netctl list
    * wlp3s0-ap-5g
    [elatov@macair ~]$ sudo netctl enable wlp3s0-ap-5g
    ln -s '/etc/systemd/system/netctl@wlp3s0\x2dap\x2d5g.service' '/etc/systemd/system/multi-user.target.wants/netctl@wlp3s0\x2dap\x2d5g.service'

For good measure you can start it, but the **wifi-menu** should've taken care of that:

    [elatov@macair ~]$ sudo netctl start wpls3-ap-5g

At this point you can enable SSH and do the rest remotely if you so prefer:

    [elatov@macair ~]$sudo pacman -S openssh
    [elatov@macair ~]$sudo systemctl enable sshd
    [elatov@macair ~]$sudo systemctl start sshd

#### Add MaxOS to the GRUB Menu
To add the mac os x grub menu, I followed the instructions from my [previous blog](/2015/04/install-fedora-21-on-macair-72/), I configured a custom menu to chainload the mac osx bootloader:

    [elatov@macair ~]$ cat /etc/grub.d/40_custom
    #!/bin/sh
    exec tail -n +3 $0
    # This file provides an easy way to add custom menu entries.  Simply type the
    # menu entries you want to add after this comment.  Be careful not to change
    # the 'exec tail' line above.
    menuentry "MacOS X Yosemite" {
            insmod hfsplus
            set root=(hd1,gpt3)
            chainloader /System/Library/CoreServices/boot.efi
            boot
    }

and if you want to be the default you can set it the grub config:

    [root@macair ~]# grep ^GRUB_DEFAULT /etc/default/grub
    GRUB_DEFAULT="MacOS X Yosemite"

and rebuilt the config one more time:

    [elatov@macair ~]$ sudo grub-mkconfig -o /boot/grub/grub.cfg
    Generating grub configuration file ...
    Found linux image: /boot/vmlinuz-linux
    Found initrd image: /boot/initramfs-linux.img
    Found fallback initramfs image: /boot/initramfs-linux-fallback.img
    done

After rebooting the Mac OS X menu was the default one in GRUB and I can always select Arch Linux when I need to.

#### Xorg

You can run the following to install **X**:

    [elatov@macair ~]$ sudo pacman -S xorg xf86-input-synaptics

Let's get a simple window manager and display manager installed:

    [elatov@macair ~]$ sudo pacman -S lightdm lightdm-gtk-greeter icewm

Let's enable the display manager to start on boot:

    [elatov@macair ~]$ sudo systemctl enable lightdm
    Created symlink from /etc/systemd/system/display-manager.service to /usr/lib/systemd/system/lightdm.service.

Here is track pad setup that worked well for me:

    [elatov@air ~]$ cat /etc/X11/xorg.conf.d/60-synaptics.conf 
    Section "InputClass"
      Identifier "touchpad"
      Driver "synaptics"
      MatchIsTouchpad "on"
      MatchDevicePath "/dev/input/event*"
      Option "FingerHigh" "10"
      Option "FingerLow" "1"
      Option "RTCornerButton" "0"
      Option "RBCornerButton" "0"
      Option "MinSpeed" "0.7"
      Option "MaxSpeed" "1.7"
      Option "SHMConfig" "on"
      Option "TapAndDragGesture" "on"
      Option "PalmDetect" "on"
      Option "TapButton1" "1"
      Option "TapButton2" "3"
      Option "TapButton3" "2"
      Option "PalmMinWidth" "30"
    EndSection

Other people have had luck with the **xf86-input-mtrack** driver, but I was okay with the **synaptics** one.

To fix the **~** (Tilde) key I ended up adding the following to GRUB menu:

    [elatov@air ~]$  grep LINUX_D /etc/default/grub
    GRUB_CMDLINE_LINUX_DEFAULT="quiet hid_apple.iso_layout=0"

To make sure the **xbacklight** utility works, set the following GRUB option:

    [elatov@macair ~]$ grep LINUX_D /etc/default/grub 
    GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi_backlight=vendor"

For the above options I had to regenerate the GRUB menu.


#### Sound

I end up using **pulseaudio** to install it, I ran the following

    [elatov@macair ~]$ sudo pacman -S pulseaudio pulseaudio-alsa alsa-utils

If **pulseaudio** is not started by the window manager by default, then launch it your self:

    [elatov@macair ~]$ start-pulseaudio-x11

After pulse is running you can test with the following files:

    [elatov@macair ~]$ aplay /usr/share/sounds/alsa/Front_Left.wav
    Playing WAVE '/usr/share/sounds/alsa/Front_Left.wav' : Signed 16 bit Little Endian, Rate 48000 Hz, Mono
    [elatov@macair ~]$ aplay /usr/share/sounds/alsa/Front_Right.wav
    Playing WAVE '/usr/share/sounds/alsa/Front_Right.wav' : Signed 16 bit Little Endian, Rate 48000 Hz, Mono

You should hear something come out of the speakers.

#### Enable swap
I didn't do this during the installation so I decided to catch up. First find out what the UUID of the swap partition is (mine was already there from the previous install):

    [elatov@macair ~]$ sudo blkid  | grep swap
    /dev/mapper/vgos-swap: UUID="4ea5bcf4-b635-48bb-ac79-adeaefa8950a" TYPE="swap"

Then add the following to the **/etc/fstab** file:

    # /dev/mapper/vgos-swap
    UUID=4ea5bcf4-b635-48bb-ac79-adeaefa8950a       swap            swap    defaults        0 0

Then enable it:

    [elatov@macair ~]$ swapon -s
    [elatov@macair ~]$ sudo swapon -a
    [elatov@macair ~]$ swapon -s
    Filename				Type		Size	Used	Priority
    /dev/dm-1                              	partition	2461692	0	-1
