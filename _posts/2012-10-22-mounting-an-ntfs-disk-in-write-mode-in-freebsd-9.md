---
title: Mounting an NTFS Disk with Write Capabilties in FreeBSD 9
author: Karim Elatov
layout: post
permalink: /2012/10/mounting-an-ntfs-disk-in-write-mode-in-freebsd-9/
dsq_thread_id:
  - 1404673658
categories:
  - Home Lab
  - OS
tags:
  - /dev/da0
  - /etc/rc.conf
  - Fatal trap 12
  - fdisk
  - freebsd
  - fusefs
  - fusefs-ntfs
  - gpart
  - kldstat
  - make extract
  - make fetch
  - makewhatis
  - mount_ntfs
  - NTFS
  - ntfs-3g
  - ntfs-3g.probe
  - pkg_info
---
I was trying to share data between a Windows Machine and FreeBSD machine. They were not connected over the network so I decided to use my USB drive to transfer the data. I formatted the drive NTFS from the Windows side and then tried to transfer the data onto the disk from the FreeBSD machine. When I plugged in the drive into the FreeBSD machine I saw the following:


	elatov@freebsd:~>dmesg | tail -8
	ugen2.2: <SanDisk> at usbus2
	umass0: <SanDisk SanDisk USB, class 0/0, rev 2.00/1.26, addr 2> on usbus2
	umass0: SCSI over Bulk-Only; quirks = 0x4100
	umass0:2:0:-1: Attached to scbus2
	da0 at umass-sim0 bus 0 scbus2 target 0 lun 0
	da0: <SanDisk 1.26> Removable Direct Access SCSI-5 device
	da0: 40.000MB/s transfers
	da0: 7633MB (15633408 512 byte sectors: 255H 63S/T 973C)


Then checking the file system on the disk I saw the following:


	elatov@freebsd:~>sudo fdisk /dev/da0
	*****\** Working on device /dev/da0 *******
	parameters extracted from in-core disklabel are:
	cylinders=973 heads=255 sectors/track=63 (16065 blks/cyl)

	parameters to be used for BIOS calculations are:
	cylinders=973 heads=255 sectors/track=63 (16065 blks/cyl)

	Media sector size is 512
	Warning: BIOS sector numbering starts with sector 1
	Information from DOS bootblock is:
	The data for partition 1 is:
	sysid 7 (0x07),(NTFS, OS/2 HPFS, QNX-2 (16 bit) or Advanced UNIX)
	start 2048, size 15631360 (7632 Meg), flag 0
	beg: cyl 2/ head 31/ sector 12;
	end: cyl 31/ head 0/ sector 21
	The data for partition 2 is:
	<UNUSED>
	The data for partition 3 is:
	<UNUSED>
	The data for partition 4 is:
	<UNUSED>


If you want a more concise view, you can use *gpart*:


	elatov@freebsd:~>gpart show /dev/da0
	=> 63 15633345 da0 MBR (7.5G)
	63 1985 - free - (992k)
	2048 15631360 1 ntfs (7.5G)


So the first partition had NTFS on it. I then tried to mount the NTFS partition and I was actually successful:


	elatov@freebsd:~>sudo mount -t ntfs /dev/da0s1 /mnt/usb
	elatov@freebsd:~>df -h | grep usb
	/dev/da0s1 7.5G 38M 7.4G 1% /mnt/usb
	elatov@freebsd:~>mount | grep da0
	/dev/da0s1 on /mnt/usb (ntfs, local)


But when I tried to write files to it, I couldn't. I then wanted to find any *man* pages regarding NTFS:


	elatov@freebsd:~>man -k ntfs
	mount_ntfs(8) - mount an NTFS file system


Not much there :) Checking out the *man* page, I saw the following:

> **CAVEATS**
> This utility is primarily used for read access to an NTFS volume. See the WRITING section for details about writing to an NTFS volume.
>
> For a full read-write NTFS support consider sysutils/fusefs-ntfs port/package.

So it looks like I need to install another package to have write permission to an NTFS volume. So let's get to it:


	elatov@freebsd:~>cd /usr/ports/sysutils/fusefs-ntfs
	elatov@freebsd:/usr/ports/sysutils/fusefs-ntfs>sudo make install clean


The install finished, and I wanted to mount it with the new package. First I un-mounted the drive:


	elatov@freebsd:~>sudo umount /mnt/usb
	elatov@freebsd:~>df -h | grep usb
	elatov@freebsd:~>


That looks good, next let's figure out how to use this package to mount the NTFS partition. First update your *man* database and check out the *man* pages:


	elatov@freebsd:~>sudo makewhatis /usr/local/man
	elatov@freebsd:~>man -k ntfs
	mount_ntfs(8) - mount an NTFS file system
	mkntfs(8) - create an NTFS file system
	ntfs-3g(8) - Third Generation Read/Write NTFS Driver
	ntfs-3g.probe(8) - Probe an NTFS volume mountability
	ntfs-3g.secaudit(8) - NTFS Security Data Auditing
	ntfs-3g.usermap(8) - NTFS Building a User Mapping File
	ntfscat(8) - print NTFS files and streams on the standard output
	ntfsclone(8) - Efficiently clone, image, restore or rescue an NTFS
	ntfscluster(8) - identify files in a specified region of an NTFS volume
	ntfscmp(8) - compare two NTFS filesystems and tell the differences
	ntfscp(8) - copy file to an NTFS volume
	ntfsfix(8) - fix common errors and force Windows to check NTFS
	ntfsinfo(8) - dump a file's attributes
	ntfslabel(8) - display/change the label on an ntfs file system
	ntfsls(8) - list directory contents on an NTFS filesystem
	ntfsprogs(8) - tools for doing neat things with NTFS
	ntfsresize(8) - resize an NTFS filesystem without data loss
	ntfsundelete(8) - recover a deleted file from an NTFS volume


From the *man* page:

> **EXAMPLE**
> Test if /dev/sda1 can be mounted read-write:
>
> ntfs-3g.probe -readwrite /dev/sda1
>
> **EXIT CODES**
> The exit codes are as follows:
>
> 0 Volume is mountable.
> 11 Syntax error, command line parsing failed.

Let's see if we are okay:


	elatov@freebsd:~>sudo ntfs-3g.probe --readwrite /dev/da0s1
	elatov@freebsd:~>echo $?



That means we can mount it read/write. Now let's actually mount it. From the *man* page here are some examples:

> **EXAMPLES**
> Mount /dev/sda1 to /mnt/windows:
>
> ntfs-3g /dev/sda1 /mnt/windows
> or
> mount -t ntfs-3g /dev/sda1 /mnt/windows
>
> Mount the ntfs data partition /dev/sda3 to /mnt/data with standard
> Linux permissions applied :
>
> ntfs-3g -o permissions /dev/sda3 /mnt/data
> or
> mount -t ntfs-3g -o permissions /dev/sda3 /mnt/data
>
> Read-only mount /dev/sda5 to /home/user/mnt and make user with uid 1000
> to be the owner of all files:
>
> ntfs-3g /dev/sda5 /home/user/mnt -o ro,uid=1000

Here is what I did to try to mount my NTFS Partition:


	elatov@freebsd:~>sudo ntfs-3g /dev/da0s1 /mnt/usb -o uid=500
	fuse: failed to open fuse device: No such file or directory


I didn't remember the "Install Notice" for the packages, so I decided to refresh my memory:


	elatov@freebsd:~>pkg_info -D -x fusefs-ntfs-2012.1.15
	Information for fusefs-ntfs-2012.1.15:

	Install notice:
	==============================================================================

	NTFS-3G has been installed, for information, known issues and how to report
	bugs see the FreeBSD README:

	/usr/local/share/doc/ntfs-3g/README.FreeBSD

	Also see the official README (but has some Linux specific parts).

	==============================================================================


Checking out the package and it's files I saw this:


	elatov@freebsd:~>pkg_info | grep ntfs
	fusefs-ntfs-2012.1.15 Mount NTFS partitions (read/write) and disk images
	elatov@freebsd:~>pkg_info -L fusefs-ntfs-2012.1.15 | grep -i read
	/usr/local/share/doc/ntfs-3g/README
	/usr/local/share/doc/ntfs-3g/README.FreeBSD


From the README, I saw the following:

> To mount at startup you need to have the following line in /etc/rc.conf:
>
> fusefs_enable="YES"

so I added that to my *rc.conf* and then started the *service*:


	elatov@freebsd:~>sudo /usr/local/etc/rc.d/fusefs start
	Starting fusefs.


You will also see the *fuse* module loaded now:


	elatov@freebsd:~>kldstat | grep fuse
	2 1 0xc6467000 e000 fuse.ko


Now trying to mount the NTFS volume:


	elatov@freebsd:~>sudo ntfs-3g /dev/da0s1 /mnt/usb -o uid=500
	elatov@freebsd:~>df -h | grep usb
	/dev/fuse0 7.5G 38M 7.4G 1% /mnt/usb
	elatov@freebsd:~>mount | grep usb
	/dev/fuse0 on /mnt/usb (fusefs, local, synchronous)


That looked good, and I was able to write to the usb disk:


	elatov@freebsd:~>cd /mnt/usb/
	elatov@freebsd:/mnt/usb>ls
	elatov@freebsd:/mnt/usb>touch test
	elatov@freebsd:/mnt/usb>ls -l
	total 0
	-rwxrwxrwx 1 elatov wheel 0 Oct 13 13:58 test


That was it. However when I tried to copy files to the NTFS volume, I would get a kernel panic. Here is a screenshot:

![freebsd_kernel_panic_copy_ntfs](http://virtuallyhyper.com/wp-content/uploads/2012/10/freebsd_kernel_panic_copy_ntfs.png)

Another person had the issue as well, [here](http://forums.freebsd.org/showthread.php?t=31161) a link to his kernel panic. No one actually answered the previous post, here is a copy of his back trace:

> Fatal trap 12: page fault while in kernel mode
> fault virtual address = 0x0
> fault code = supervisor read, page not present
> instruction pointer = 0x20:0x0
> stack pointer = 0x28:0xeae1ec48
> frame pointer = 0x28:0xeae1ec70
> code segment = base 0x0, limit 0xfffff, type 0x1b
> = DPL 0, pres 1, def32 1, gran 1
> processor eflags = interrupt enabled, resume, IOPL = 0
> current process = 2390 (mv)
> trap number = 12

Later I found [this](http://www.mail-archive.com/freebsd-users-jp@jp.freebsd.org/msg04947.html) post. It's in Japanese but you can always translate it. In this post there is actually a patch to the *fusefs-kmod* package to fix the issue, since there are issues with *chown* and *chmod* when it tries to copy files to an NTFS volume. So let's patch the source and see if it helps out. First download the source if you don't have it:


	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>sudo make fetch
	===> Found saved configuration for fusefs-kmod-0.3.9.p1.20080208_11
	=> 498acaef33b0.tar.gz doesn't seem to exist in /usr/ports/distfiles/fuse4bsd.
	=> Attempting to fetch ftp://ftp.FreeBSD.org/pub/FreeBSD/ports/distfiles/fuse4bsd/498acaef33b0.tar.gz
	498acaef33b0.tar.gz 100% of 113 kB 171 kBps


Then extract the source:


	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>sudo make extract
	===> Found saved configuration for fusefs-kmod-0.3.9.p1.20080208_11
	===> Extracting for fusefs-kmod-0.3.9.p1.20080208_11
	=> SHA256 Checksum OK for fuse4bsd/498acaef33b0.tar.gz.
	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>ls -lrt
	total 24
	-rw-r--r-- 1 root wheel 75 Feb 10 2006 pkg-descr
	-rw-r--r-- 1 root wheel 150 Mar 19 2011 distinfo
	-rw-r--r-- 1 root wheel 1035 Nov 29 2011 pkg-plist
	-rw-r--r-- 1 root wheel 3092 Sep 20 17:52 Makefile
	drwxr-xr-x 2 root wheel 512 Sep 29 08:30 files
	drwxr-xr-x 3 root wheel 512 Oct 14 08:02 work


After you extract the source you will see a '*work*' directory. The patch process is described [here](http://www.freebsd.org/doc/en_US.ISO8859-1/books/porters-handbook/slow-patch.html). From the FreeBSD page:

> Each patch you wish to apply should be saved into a file named patch-* where * indicates the pathname of the file that is patched, such as patch-Imakefile or patch-src-config.h. These files should be stored in PATCHDIR (usually files/, from where they will be automatically applied. All patches must be relative to WRKSRC (generally the directory your port's tarball unpacks itself into, that being where the build is done).
> ..
> ..
> Note that if the path of a patched file contains an underscore (_) character, the patch needs to have two underscores instead in its name. For example, to patch a file named src/freeglut_joystick.c, the corresponding patch should be named patch-src-freeglut__joystick.c.

So we were patching the "fuse_vnops.c" file. First let's find it's location in the source:


	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>find . -name 'fuse_vnops.c'
	./work/fuse4bsd-498acaef33b0/fuse_module/fuse_vnops.c


Now checking out the distfile directory, I actually saw a patch for that file:


	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>ls -l files/ | grep vn
	-rw-r--r-- 1 root wheel 443 Sep 21 2011 extra-patch-fuse_module__fuse_vnops.c
	-rw-r--r-- 1 root wheel 269 May 11 01:08 extrapatch-fuse_module__fuse_vnops.c
	-rw-r--r-- 1 root wheel 2221 Sep 20 17:52 patch-fuse_module__fuse_vnops.c


so I went ahead and edited the 'patch-fuse_module__fuse_vnops.c' file and added the changes described in the above page. [Here](http://virtuallyhyper.com/wp-content/uploads/2012/10/patch-fuse_module__fuse_vnops.c) is my final patch file. I then removed both packages:


	elatov@freebsd:> sudo /usr/local/etc/rc.d/fusefs stop
	elatov@freebsd:>cd /usr/ports/sysutils/fusefs-kmod
	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>sudo make deinstall
	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod>cd ../fusefs-ntfs
	elatov@freebsd:/usr/ports/sysutils/fusefs-nfts>sudo make deinstall


I then applied my new patch file:


	elatov@freebsd:~>fetch http://virtuallyhyper.com/wp-content/uploads/2012/10/patch-fuse_module__fuse_vnops.c
	elatov@freebsd:~>sudo cp patch-fuse_module\__fuse_vnops.c /usr/ports/sysutils/fusefs-kmod/files/patch-fuse_module__fuse_vnops.c


And then re-installed both:


	elatov@freebsd:>cd /usr/ports/sysutils/fusefs-kmod
	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod> sudo make install clean
	elatov@freebsd:/usr/ports/sysutils/fusefs-kmod> cd ../fusefs-ntfs
	elatov@freebsd:/usr/ports/sysutils/fusefs-ntfs> sudo make install clean
	elatov@freebsd:> sudo /usr/local/etc/rc.d/fusefs start


After that I was able to copy files just fine :)


	elatov@freebsd:~>touch test
	elatov@freebsd:~>cp test /mnt/usb/.
	elatov@freebsd:~>ls -l /mnt/usb/
	total 0
	-rwxrwxrwx 1 elatov wheel 0 Oct 14 17:15 test


And no kernel panic occurred.

