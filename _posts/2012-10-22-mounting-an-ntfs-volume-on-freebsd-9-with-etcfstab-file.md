---
title: Mounting an NTFS Volume in FreeBSD 9 with the /etc/fstab File
author: Karim Elatov
layout: post
permalink: /2012/10/mounting-an-ntfs-volume-on-freebsd-9-with-etcfstab-file/
dsq_thread_id:
  - 1406703090
categories:
  - Home Lab
  - OS
tags:
  - /etc/fstab
  - camcontrol devlist
  - df
  - glabel
  - gpart
  - mount
  - newfs
  - ntfslabel
  - tunefs
---
In my previous <a href="http://virtuallyhyper.com/2012/10/mounting-an-ntfs-disk-in-write-mode-in-freebsd-9/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/mounting-an-ntfs-disk-in-write-mode-in-freebsd-9/']);">post</a>, I blogged about mounting an NTFS volume in FreeBSD. Now I decided to make the process easier by using the */etc/fstab* file. I thought this would be a pretty straightforward process, but it took a while to figure out so I decided to put my notes here. First figure out what is the device identifier of your NTFS disk. For example:

[code highlight="3"]  
elatov@freebsd:~>sudo camcontrol devlist  
<TEAC CD-224E K.9A> at scbus0 target 0 lun 0 (cd0,pass0)  
<SanDisk 1.26> at scbus2 target 0 lun 0 (pass1,da0)  
[/code]

I was actually using a USB disk, so my device is */dev/da0*. Then figure out which partition corresponds to your NTFS partition:

[code highlight="4"]  
elatov@freebsd:~>gpart show /dev/da0  
=> 63 15633345 da0 MBR (7.5G)  
63 1985 - free - (992k)  
2048 15631360 1 ntfs (7.5G)  
[/code]

In the above output we can see it&#8217;s the first one. So I will be mounting */dev/da0s1*. Here is the entry I had to put into my */etc/fstab* file to get the mount point to work:

[code]  
elatov@freebsd:~>grep da0 /etc/fstab  
/dev/da0s1 /mnt/usb ntfs rw,mountprog=/usr/local/bin/ntfs-3g,uid=500,gid=500,late 0 0  
[/code]

With above setup, I could type &#8216;mount /dev/da0s1&#8242; or &#8216;mount /mnt/usb&#8217; and my disk would mount with the appropriate permissions. Here is how it looks like when it&#8217;s mounted:

[code]  
elatov@freebsd:~>sudo mount /mnt/usb  
elatov@freebsd:~>df -h | grep usb  
/dev/fuse0 7.5G 3.3G 4.1G 44% /mnt/usb  
[/code]

Next I actually wanted to label the disk so the entry in the */etc/fstab* file didn&#8217;t depend on the device identifier/node. I got most of the information regarding labeling from &#8220;<a href="http://www.freebsd.org/doc/handbook/geom-glabel.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.freebsd.org/doc/handbook/geom-glabel.html']);">Labeling Disk Devices</a>&#8220;. So first un-mount the disk:

[code]  
elatov@freebsd:~>sudo umount /mnt/usb  
elatov@freebsd:~>  
[/code]

From the above page:

> During system initialization, the FreeBSD kernel will create device nodes as devices are found. This method of probing for devices raises some issues, for instance what if a new disk device is added via USB? It is very likely that a flash device may be handed the device name of da0 and the original da0 shifted to da1. This will cause issues mounting file systems if they are listed in /etc/fstab, effectively, this may also prevent the system from booting.  
> &#8230;  
> &#8230;
> 
> A better solution is available. By using the glabel utility, an administrator or user may label their disk devices and use these labels in /etc/fstab. Because glabel stores the label in the last sector of a given provider, the label will remain persistent across reboots. By using this label as a device, the file system may always be mounted regardless of what device node it is accessed through.  
> &#8230;  
> &#8230;
> 
> There are two types of labels, a generic label and a file system label. Labels can be permanent or temporary. Permanent labels can be created with the tunefs(8) or newfs(8) commands. They will then be created in a sub-directory of /dev, which will be named according to their file system type. For example, UFS2 file system labels will be created in the /dev/ufs directory. Permanent labels can also be created with the *glabel label* command. These are not file system specific, and will be created in the /dev/label directory. 

So there are a couple of ways to label a disk: *newfs*, *tunefs*, and *glabel*. Unfortunately the first two tools are file system specific and will work with ufs. The glabel tool doesn&#8217;t depend on the file system. From the *man* page of *glabel*:

> DESCRIPTION  
> The glabel utility is used for GEOM provider labelization. A label can  
> be set up on a GEOM provider in two ways: &#8220;manual&#8221; or &#8220;automatic&#8221;.  
> When using the &#8220;manual&#8221; method, no metadata are stored on the devices,  
> so a label has to be configured by hand every time it is needed. The  
> &#8220;automatic&#8221; method uses on-disk metadata to store the label and detect  
> it automatically in the future.
> 
> This class also provides volume label detection for file systems. Those  
> labels cannot be set with glabel, but must be set with the appropriate  
> file system utility, e.g. for UFS the file system label is set with  
> tunefs(8). Currently supported file systems are:
> 
> o UFS1 volume names (directory /dev/ufs/).  
> o UFS2 volume names (directory /dev/ufs/).  
> o UFS1 file system IDs (directory /dev/ufsid/).  
> o UFS2 file system IDs (directory /dev/ufsid/).  
> o MSDOSFS (FAT12, FAT16, FAT32) (directory /dev/msdosfs/).  
> o CD ISO9660 (directory /dev/iso9660/).  
> o EXT2FS (directory /dev/ext2fs/).  
> o REISERFS (directory /dev/reiserfs/).  
> o NTFS (directory /dev/ntfs/).
> 
> Support for partition metadata is implemented for:
> 
> o GPT labels (directory /dev/gpt/).  
> o GPT UUIDs (directory /dev/gptid/).
> 
> Generic labels are created in the directory /dev/label/. 

So first let&#8217;s check if our disk already has a label:

[code]  
elatov@freebsd:~>sudo glabel dump /dev/da0s1  
Can't read metadata from /dev/da0s1: Invalid argument.  
glabel: Not fully done.  
[/code]

That looks good (since I didn&#8217;t have a label on the device), next label the disk:

[code]  
elatov@freebsd:~>sudo glabel label usb /dev/da0s1  
[/code]

Now check to see if the label is there:

[code highlight="5"]  
elatov@freebsd:~>sudo glabel dump /dev/da0s1  
Metadata on /dev/da0s1:  
Magic string: GEOM::LABEL  
Metadata version: 2  
Label: usb  
[/code]

Lastly check if the device has been created:

[code]  
elatov@freebsd:~>ls -l /dev/label/  
total 0  
crw-r\----- 1 root operator 0, 105 Oct 21 16:41 usb  
[/code]

Also a more concise view would look like this:

[code]  
elatov@freebsd:~>sudo glabel status  
Name Status Components  
gptid/676a5c5d-0a0b-11e2-aca4-00c09f41c5fa N/A aacd0p1  
label/usb N/A da0s1  
[/code]

Now edit your */etc/fstab* to look like this:

[code]  
elatov@freebsd:~>grep label /etc/fstab  
/dev/label/usb /mnt/usb ntfs noauto,rw,mountprog=/usr/local/bin/ntfs-3g,uid=500,gid=500,late 0 0  
[/code]

Finally, mounting worked without any issues:

[code]  
elatov@freebsd:~>sudo mount /mnt/usb  
elatov@freebsd:~>df -h | grep usb  
/dev/fuse0 7.5G 3.3G 4.1G 44% /mnt/usb  
[/code]

and now I don&#8217;t have to worry about the order that I plug in the device. You can also use the *ntfslabel* tool to label at the file system level:

[code]  
elatov@freebsd:~>sudo ntfslabel /dev/da0s1 usb_ntfs  
[/code]

You can check with the same tool to see if it worked:

[code]  
elatov@freebsd:~>sudo ntfslabel /dev/da0s1  
usb_ntfs  
[/code]

or you can check with the *glabel*

[code]  
elatov@freebsd:~>sudo glabel status  
Name Status Components  
gptid/676a5c5d-0a0b-11e2-aca4-00c09f41c5fa N/A aacd0p1  
label/usb N/A da0s1  
ntfs/usb_ntfs N/A da0s1  
[/code]

So now we have a file system label and a device label. I went ahead and plugged in the disk to my Fedora laptop and here is what I saw:

[code]  
[elatov@klaptop ~]$ sudo ntfslabel /dev/sdb1  
usb_ntfs  
[elatov@klaptop ~]$ blkid | grep usb  
/dev/sdb1: LABEL="usb_ntfs" UUID="218F49247215AD83" TYPE="ntfs"  
[/code]

Now I can create an entry on my Fedora laptop in the /etc/fstab file, like so:

[code]  
LABEL=usb_ntfs /mnt/usb ntfs noauto,uid=500,rw 0 0  
[/code]

and then I can mount the disk, like this:

[code]  
[elatov@klaptop ~]$ sudo mount /mnt/usb  
[elatov@klaptop ~]$ df -hT | grep usb  
/dev/sdb1 fuseblk 7.5G 3.4G 4.2G 45% /mnt/usb  
[/code]

Of course the Windows machines mounted the device just fine as well. 

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/10/mounting-an-ntfs-volume-on-freebsd-9-with-etcfstab-file/" title=" Mounting an NTFS Volume in FreeBSD 9 with the /etc/fstab File" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:/etc/fstab,camcontrol devlist,df,glabel,gpart,mount,newfs,ntfslabel,tunefs,blog;button:compact;">In my previous post, I blogged about mounting an NTFS volume in FreeBSD. Now I decided to make the process easier by using the /etc/fstab file. I thought this would...</a>
</p>