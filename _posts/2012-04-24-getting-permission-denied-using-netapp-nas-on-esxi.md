---
published: true
title: Getting Permission Denied Using NetApp NAS on ESX(i)
author: Karim Elatov
layout: post
permalink: /2012/04/getting-permission-denied-using-netapp-nas-on-esxi/
categories: ['storage', 'vmware']
tags: ['exports', 'netapp', 'nfs', 'nosuid']
---

A couple of days ago I had an issue with powering on VMs that resided on a NetApp NAS datastore. I logged into the host and tried to see if I had access to the datastore and it was really strange. I could not touch any existing files:

![touch_perm_denied_2](https://github.com/elatov/uploads/raw/master/2012/04/touch_perm_denied_2.png)

however I was able to create new files but the owner of the newly created files was *nfsnobody*. Running 'ls', after I created a new file, looked like this:

![ls_nfsnobody_2](https://github.com/elatov/uploads/raw/master/2012/04/ls_nfsnobody_2.png)

Why are we seeing the *nsfnobody* user owning new files? This is actually the default behavior for an NFS server. Looking over the man page of [exports(5)](http://linux.die.net/man/5/exports), we see the following:

> Very often, it is not desirable that the root user on a client machine is also treated as root when accessing files on the NFS server. To this end, uid 0 is normally mapped to a different id: the so-called anonymous or *nobody* uid. This mode of operation (called 'root squashing') is the default, and can be turned off with *no_root_squash*.

For ESX(i) to properly connect to a NAS server it needs to have read/write permission for the root user. Per the [ESX Configuration Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vsp_41_esx_server_config.pdf), from the "Network Attached Storage" section we see the following:

> ESX does not support the delegate user functionality that enables access to NFS volumes using nonroot credentials.

This may raise some security concerns and the recommendation is to place your NFS traffic on it's own segmented network to add an extra layer of security. Per the article [Best Practices for running VMware vSphere on Network Attached Storage](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-nfs-bestpractices-white-paper-en.pdf)

> Another security concern is that the ESX Server must mount the NFS server with root access. This raises some concerns about hackers getting access to the NFS server. To address the concern, it is best practice to use of either dedicated LAN or VLAN to provide protection and isolation.

Not only does the ESX(i) host require root read/write access but it also requires the *no_root_squash* option set on the export of the NFS server. From the same Best Practices article above we see the following:

> If you do not have the **no_root_squash** option set, you will get the following error when you try to create a virtual machine on the NAS datastore.
> ...
> ...
> This can be confusing since you can still create the datastore, but you will not be able to create any virtual machines on it.
> **Note:** the NetApp equivalent of no_root_squash is anon=0 in the /etc/exports file.

This is pretty much what I was seeing, so we logged into the NetApp array and checked how the exports looked like, and we saw the following:


	NA-NAS05>exportfs
	/vol/vol0/home -sec=sys,rw,root=10.2.1.131,nosuid
	/vol/vol0 -sec=sys,ro,rw=10.2.1.131,root=10.2.1.131,nosuid
	/vol/NA_NFS1 -sec=sys,rw,root=10.2.1.131,nosuid


While I was on the NAS array I decided to double check the qtree settings. I wasn't having locking issues, but just for good measure. More information regarding qtree issues can be seen at VMware KB [1008591](https://knowledge.broadcom.com/external/article?legacyId=1008591), I saw the following qtree settings:


	NA-NAS05>qtree status
	Volume Tree Style Oplocks Status
	-------- -------- ----- -------- ---------
	vol0 ntfs enabled normal
	NA_NFS1 unix enabled normal


The export that I was working with was appropriately set to unix, so that definitely was not causing any issues. Looking at the exportfs output I realized a couple of things:

1. The volume NA_NFS1 allowed any host to read/write to it (rw)
2. The volume NA_NFS1 only allowed root access from one host (root=10.2.1.131)
3. The nosuid flag was set on volume NA_NFS1
4. The volume NA_NFS1 didn't have no_root_squash enabled (anon=0)

To understand what the *nosuid* flag is, we first need to know what *setuid* is. This is commonly used on Unix, from the man page of [setuid(2)](http://linux.die.net/man/2/setuid):

> setuid() sets the effective user ID of the calling process. If the effective UID of the caller is root, the real UID and saved set-user-ID are also set.

So if a user named *elatov* runs an executeable that had the *setuid* flag set, that means his privileges will be elevated to be the same as the owner of that executable (sudo uses this). Now if you don't want that to happen on a certain filesystem (on most unix systems it's common practice to set this for /var, since no one should be running executables there any ways) then you can set the *nosuid* flag on your mount point. From the man page of [execve(2)](http://linux.die.net/man/2/execve) :

> The result of mounting a file system nosuid varies across Linux kernel versions: some will refuse execution of set-user-ID and set-group-ID executables when this would give the user powers she did not have already (and return EPERM), some will just ignore the set-user-ID and set-group-ID bits and exec() successfully.

ESX(i) doesn't have anything to do with *setuid*, so I decided to get rid of that flag from our export. I also decided to limit the read/write permissions to the NFS subnet and also allow root access from the NFS subnet as well. Lastly I decided to enable *no_root_squash* on the export. To edit /etc/exports on the NetApp array, first we need to read the file and see how it looks:


	NA-NAS05>rdfile /etc/exports
	#Auto-generated by setup Mon Apr 16 08:49:47 CDT 2012
	/vol/vol0 -sec=sys,ro,rw=10.2.1.131,root=10.2.1.131,nosuid
	/vol/NA_NFS1 -sec=sys,rw,root=10.2.1.131,nosuid
	/vol/vol0/home -sec=sys,rw,root=10.2.1.131,nosuid


It looked the same as the exportfs output, so then I decided to write file (On NetApp you run 'wrfile /etc/exports' and then you paste the brand new config into the file and it stores the new config)


	NA-NAS05>wrfile /etc/exports
	/vol/vol0/home -sec=sys,rw,root=10.2.1.131,nosuid
	/vol/vol0 -sec=sys,ro,rw=10.2.1.131,root=10.2.1.131,nosuid
	/vol/NA_NFS1 -sec=sys,rw=10.2.1.0/24,root=10.2.1.0/24,anon=0


You then re-export everything from the /etc/exports file by running the following to make your changes take affect:


	NA-NAS05> exportfs -a


After that I was able to touch files under the NFS mount point and all the VMs successfully powered on.

