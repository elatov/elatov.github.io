---
layout: post
title: "Arch Linux Systemd on ARM Architecture Issue"
author: Karim Elatov
description: ""
categories: [OS]
tags: [Arch Linux, systemd, chromeos]
---
So I was doing my regular updates on my Arch Linux machine (`pacman -Syu`). The update incuded a new version of **systemd** and that wasn't anything new. After I rebooted I recieved the following error:

	systemd[1]: Failed to mount cgroup at /sys/fs/cgroup/systemd: No such file or directory
	
Upon doing a google search I ran into [[Chromebook XE303C12] Systemd doesn't boot after upgrade](http://archlinuxarm.org/forum/viewtopic.php?t=7330&p=40185) (I was running Arch Linux on the Samsung Chromebook), and it matched my issue. 

The fix for now was to downgrade **systemd**. In order to do that, you had to boot from an external source, **chroot** into the original install, and downgrade the package. I actually left my ChromeOS install alone and I always boot from an SD card (check out [this](/2014/02/install-arch-linux-samsung-chromebook/) post on that setup). So I booted back into ChromeOS (on the development screen instead typing **CTRL+U**, I typed **CTRL+D**) and started crosh to gain root access:

1. Press **Ctrl + Alt + T** keys. This will open up the *crosh* shell
2. Type **shell** to get into a bash shell.
3. Type **sudo su** to become root.

By default any external media is automatically mounted in ChromeOS:

	localhost ~ # mount | grep 'SD Card'
	/dev/mmcblk1p12 on /media/removable/SD Card type vfat (rw,nosuid,nodev,noexec,relatime,dirsync,uid=1000,gid=1000,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,flush,errors=remount-ro)
	/dev/mmcblk1p2 on /media/removable/SD Card 1 type ext2 (rw,nosuid,nodev,noexec,relatime,dirsync)
	/dev/mmcblk1p3 on /media/removable/SD Card 2 type ext4 (rw,nosuid,nodev,noexec,relatime,dirsync,data=ordered)
	
So our SD card is **/dev/mmcblk1** and our root partition is **/dev/mmcblk1p3**. In order for us to **chroot** we need to allow **exec**utables on that mount point, so let's remount that partition and enable that:

	localhost ~ # mount /dev/mmcblk1p3 -o remount,exec

Then we need to *bind* the **/proc** directory into the root partition, so while in the chroot the OS can find partitions. This is done with the following command:

	localhost ~ # mount --bind /proc /media/removable/SD\ Card\ 2/proc/

Now we can **chroot** into our Arch Linux install:

	localhost ~ # chroot /media/removable/SD\ Card\ 2/
	[root@localhost /]#
	
Now let's downgrade our **systemd** version:

	[root@localhost /]# pacman -U /var/cache/pacman/pkg/systemd-212-3-armv7h.pkg.tar.xz
	loading packages...
	warning: downgrading package systemd (213-5 => 212-3)
	resolving dependencies...
	looking for inter-conflicts...

	Packages (1): systemd-212-3

	Total Installed Size:   15.64 MiB
	Net Upgrade Size:       -3.79 MiB

	:: Proceed with installation? [Y/n] y
	(1/1) checking keys in keyring      [################################################] 100%
	(1/1) checking package integrity    [################################################] 100%
	(1/1) loading package files         [################################################] 100%
	(1/1) checking for file conflicts   [################################################] 100%
	(1/1) checking available disk space [################################################] 100%
	(1/1) downgrading systemd           [################################################] 100%
	synchronizing filesystem...
	
After that, exit the **chroot**, **reboot** the system, and boot back into Arch Linux (in my case on the SD card). The OS will boot up fine. While I was waiting for the fix, I would update the Arch Linux packages skipping the **systemd** package:

	elatov@crbook:~$sudo pacman -Syu --ignore systemd
	:: Synchronizing package databases...
	 core is up to date
	 extra is up to date
	 community is up to date
	 alarm is up to date
	 aur is up to date
	:: Starting full system upgrade...
	warning: systemd: ignoring package upgrade (212-3 => 213-5)
	resolving dependencies...
	looking for inter-conflicts...

	Packages (4): gnupg-2.0.23-1  libx264-1:142.20140311-4  openssl-1.0.1.h-1
				  x264-1:142.20140311-4

	Total Download Size:    4.15 MiB
	Total Installed Size:   14.56 MiB
	Net Upgrade Size:       0.75 MiB
	
The issue was present in the following versions of **systemd**:

- systemd-213-5
- systemd-213-6
- systemd-213-9

And then updating to this version fixed the issue:

- systemd-213-9.1

Here are the available **systemd** packages on my Arch Linux install:

	elatov@crbook:~$ls -rt /var/cache/pacman/pkg/systemd-21*
	/var/cache/pacman/pkg/systemd-210-2-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-210-3-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-211-1-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-212-1-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-212-2-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-212-3-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-213-5-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-213-6-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-213-9-armv7h.pkg.tar.xz
	/var/cache/pacman/pkg/systemd-213-9.1-armv7h.pkg.tar.xz

And here is the version of **systemd** that I am currently on:

	elatov@crbook:~$pacman -Qi systemd
	Name           : systemd
	Version        : 213-9.1
	Description    : system and service manager
	Architecture   : armv7h
	URL            : http://www.freedesktop.org/wiki/Software/systemd
	Licenses       : GPL2  LGPL2.1  MIT
	Groups         : None
