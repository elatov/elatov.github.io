---
title: Mount Various File Systems with Autofs on Mac OS X Mountain Lion
author: Karim Elatov
layout: post
permalink: /2013/07/mount-various-file-system-with-autofs-on-mac-os-x-mountain-lion/
dsq_thread_id:
  - 1500640460
categories:
  - Home Lab
tags:
  - autofs
  - mac-ports
  - sshfs
---
I recently go a new Mac and I wanted to setup **autofs** on it, just like I did on my previous Linux Laptops. I am running Mac OS X Mountain Lion (10.8):

    kelatov@kmac:~$sw_vers 
    ProductName:    Mac OS X
    ProductVersion: 10.8.4
    BuildVersion:   12E55
    

## AutoFS

There is a pretty good overview of AutoFS on Mac OS <a href="http://rajeev.name/2007/11/22/autofs-goodness-in-apples-leopard-105-part-i/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://rajeev.name/2007/11/22/autofs-goodness-in-apples-leopard-105-part-i/']);">here</a>:

> Autofs in Leopard consists of the following programs and daemons.
> 
> **autofsd**  
> autofsd runs **automount**, and then waits for network configuration change events and, when such an event occurs, re-runs automount to update the mounts to reflect the current automounter maps. It can also be signalled by **automount_reread** to run **automount**.
> 
> **automountd**  
> automountd is a daemon that responds to requests from **autofs** to mount and unmount network filesystems, and to supply the contents of directories, based on the contents of automounter maps. The **automountd** is started on demand by **launchd**.
> 
> **automount**  
> automount is the actual mount manager. Manages the mounting and unmounting of remote resources using several map files and configuration files. The configuration files used are **/etc/autofs.conf** and **/etc/auto_master**.
> 
> **automount_reread**  
> The man pages for **autofsd** refer to a command called **automount_reread** that can trigger a network change event for **autofs**. However, there is no additional documentation in Leopard on that command and the command itself does not exist.

We can see that by default only **autofsd** is running:

    kelatov@kmac:~$ps -ef | grep auto | grep -v grep
        0    59     1   0  2:44PM ??         0:00.08 autofsd
    

We can also check out if the daemons are started via **launchd**:

    kelatov@kmac:~$sudo launchctl list | grep -E 'automo|autof'
    -   0   com.apple.automountd
    59  -   com.apple.autofsd
    

Lastly we can see what state the daemons are in:

    kelatov@kmac:~$sudo launchctl bslist | grep -E 'automo|autof'
    D  com.apple.automountd
    

The **D** stands for on-demand.

### Autofs Maps

With Mac OS there are a couple of options for **autofs**. From the Mac OS <a href="http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man5/auto_master.5.html#//apple_ref/doc/man/5/auto_master" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man5/auto_master.5.html#//apple_ref/doc/man/5/auto_master']);">man</a> page:

> **Direct Map**  
> A direct map associates filesystem locations directly with directories. The entry key is the full path name of a directory. For example:
> 
>     /usr/local      eng4:/export/local 
>     /src            eng4:/export/src
>     
> 
> Since the direct map as a whole isn&#8217;t associated with a single directory, it is specified in the master map with a dummy directory name of **/-**.
> 
> **Indirect Map**  
> An indirect map is used where a large number of entries are to be associated with a single directory. Each map entry key is the simple name of a directory entry. A good example of this is the auto_home map which determines the entries under the /home directory. For example:
> 
>     bill    argon:/export/home/bill 
>     brent   depot:/export/home/brent 
>     guy     depot:/export/home/guy
>     

I prefer to have everything that is managed by **autofs** in one directory, so I will go with the **Indirect Map** approach.

### Creating an Indirect Map for AutoFS

I will use **/amnt** as the mount point which **autofs** will manage. To set this up, edit the **/etc/auto_master** file and add the following to it:

    /amnt           autofs_amnt
    

The above basically says that anything under the **/amnt** directory will be configured under the **/etc/autofs_amnt** file. Next let&#8217;s add a **CIFS** share to be automatically mounted **/amnt/smb**.

### Auto Mount SMB with Autofs

Let&#8217;s create the **/etc/autofs_amnt** file with appropriate permissions:

    kelatov@kmac:~$sudo touch /etc/autofs_amnt
    kelatov@kmac:~$sudo chmod 600 /etc/autofs_amnt
    

Now let&#8217;s edit the file and add the following to it:

    smb -fstype=smbfs ://elatov:PASSWORD@cifs.server.com/elatov
    

Now to apply the settings run the following:

    kelatov@kmac:~$sudo automount -vc
    automount: /net updated
    automount: /home updated
    automount: /amnt updated
    automount: no unmounts
    

notice **/amnt** is now included. If everything worked you can **cd** into the directory and it will automatically mount:

    kelatov@kmac:~$cd /amnt/smb
    kelatov@kmac:/amnt/smb$df -Ph .
    Filesystem                           Size   Used  Avail Capacity  Mounted on
    //elatov@cifs.server.com/elatov      3.0Ti  2.6Ti  341Gi    89%    /amnt/smb
    

You can use the **mount** command to find out the options of the mount point:

    kelatov@kmac:~$mount | grep elatov
    //elatov@cifs.server.com/elatov on /amnt/smb (smbfs, nodev, nosuid, automounted, nobrowse, mounted by kelatov)
    

You will also notice **automountd** now running as well:

    kelatov@kmac:/amnt/smb$ps -ef | grep auto | grep -v grep
        0    59     1   0  2:44PM ??         0:00.09 autofsd
        0   930     1   0  2:15PM ??         0:00.01 automountd
    

If you ever want to manually un-mount the share, run the following:

    kelatov@kmac:~$umount /amnt/smb
    

### Auto Mount NFS with Autofs

Edit the **/etc/autofs_amnt** file and add the following:

    iso -fstype=nfs,rw,bg,hard,intr,tcp,resvport nfs.server.com:/data/isos
    

Apply the settings with:

    sudo automount -vc
    

and check to make sure it is auto mounted:

    kelatov@kmac:~$cd /amnt/iso
    kelatov@kmac:/amnt/iso$df -Ph .
    Filesystem                  Size   Used  Avail Capacity  Mounted on
    nfs.server.com:/data/isos  3.0Ti  2.5Ti  341Gi    89%    /amnt/iso
    

and of course **mount** can show you the options:

    kelatov@kmac:~$mount | grep iso
    nfs.server.com:/data/iso on /amnt/iso (nfs, nodev, nosuid, automounted, nobrowse)
    

### Mount SSHFS with Autofs

The first thing that we need to do is install Mac Ports.

#### Install Mac Ports

Go to <a href="http://www.macports.org/install.php" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.macports.org/install.php']);">Installing MacPorts</a> and download the *pkg* installer. Launch installer and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/mac_ports_install.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/mac_ports_install.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/mac_ports_install.png" alt="mac ports install Mount Various File Systems with Autofs on Mac OS X Mountain Lion" width="613" height="434" class="alignnone size-full wp-image-9204" title="Mount Various File Systems with Autofs on Mac OS X Mountain Lion" /></a>

Follow the on-screen instructions install *Mac Ports*.

#### Install X-Code

*X-Code* is necessary for Mac Ports, so go ahead and install it from <a href="https://developer.apple.com/xcode/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://developer.apple.com/xcode/']);">XCode</a>. It will actually start up the *App Store* to do the download. After it&#8217;s done your *App Store* will look like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-install-app-store.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-install-app-store.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-install-app-store.png" alt="xcode install app store Mount Various File Systems with Autofs on Mac OS X Mountain Lion" width="747" height="290" class="alignnone size-full wp-image-9205" title="Mount Various File Systems with Autofs on Mac OS X Mountain Lion" /></a>

#### Install X-Code Command Line tools:

Go to your Applications (Command-Shift-a) and launch X-Code (accept the license agreement). Then go to the preferences:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-preferences.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-preferences.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-preferences.png" alt="xcode preferences Mount Various File Systems with Autofs on Mac OS X Mountain Lion" width="245" height="144" class="alignnone size-full wp-image-9206" title="Mount Various File Systems with Autofs on Mac OS X Mountain Lion" /></a>

Then go to the &#8220;Downloads&#8221; tab and install command line tools. After they are installed you will see the following under preferences:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-command-line-tools.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-command-line-tools.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/xcode-command-line-tools.png" alt="xcode command line tools Mount Various File Systems with Autofs on Mac OS X Mountain Lion" width="734" height="289" class="alignnone size-full wp-image-9207" title="Mount Various File Systems with Autofs on Mac OS X Mountain Lion" /></a>

#### Update Ports

Go to your &#8220;Utilities&#8221; (Command-Shift-u) and launch the terminal. From the terminal run the following:

    kelatov@kmac:~$sudo port -v selfupdate
    Password:
    --->  Updating MacPorts base sources using rsync
    receiving file list ... done
    
    sent 36 bytes  received 69 bytes  70.00 bytes/sec
    total size is 3594240  speedup is 34230.86
    receiving file list ... done
    
    sent 36 bytes  received 76 bytes  224.00 bytes/sec
    total size is 512  speedup is 4.57
    MacPorts base version 2.1.3 installed,
    MacPorts base version 2.1.3 downloaded.
    --->  Updating the ports tree
    Synchronizing local ports tree from rsync://rsync.macports.org/release/tarballs/ports.tar
    receiving file list ... done
    
    sent 36 bytes  received 70 bytes  70.67 bytes/sec
    total size is 53278720  speedup is 502629.43
    receiving file list ... done
    
    sent 36 bytes  received 77 bytes  226.00 bytes/sec
    total size is 512  speedup is 4.53
    receiving file list ... done
    
    sent 36 bytes  received 70 bytes  212.00 bytes/sec
    total size is 9759879  speedup is 92074.33
    receiving file list ... done
    
    sent 36 bytes  received 77 bytes  75.33 bytes/sec
    total size is 512  speedup is 4.53
    --->  MacPorts base is already the latest version
    
    The ports tree has been updated. To upgrade your installed ports, you should run
      port upgrade outdated
    

Now your ports are all up-to-date. You will also notice that that the Mac Ports install added the following into your **.profile** file:

    elatov@kmac:~$cat ~/.profile
    # MacPorts Installer addition on 2013-07-02_at_10:53:46: adding an appropriate PATH variable for use with MacPorts.
    export PATH=/opt/local/bin:/opt/local/sbin:$PATH
    # Finished adapting your PATH environment variable for use with MacPorts.
    

Since Mac Ports installs everything under **/opt/local** it needs to add **/opt/local/bin/** and **/opt/local/sbin/** to the path.

#### Install SSHFS

Mac Ports are like any package manager, it allows you to search for packages and install them. For example here is what I did to search for *sshfs*:

    kelatov@kmac:~$port search sshfs
    sshfs @2.4 (fuse)
        SSH filesystem for FUSE
    
    sshfs-gui @1.3 (fuse)
        OS X GUI for sshfs
    
    Found 2 ports.
    

I don&#8217;t care about the GUI version. You can also check if the package has &#8220;variants&#8221;:

    kelatov@kmac:~$port variants sshfs
    sshfs has the variants:
       universal: Build for multiple architectures
    

There aren&#8217;t that many options. A good example is something like this:

    kelatov@kmac:~$port variants mysql56
    mysql56 has the variants:
       debug: Enable debug binaries
       openssl: Enable OpenSSL support
       universal: Build for multiple architectures
    

So if I wanted to enable *debug* binaries for the **mysql56** package I would run the following:

    sudo port install mysql56 +debug
    

Anyways, to install *sshfs*, run the following:

    sudo port install sshfs
    

#### Prepare SSHFS for Autofs

First make sure you can mount with the **sshfs** command:

    kelatov@kmac:~$which sshfs
    /opt/local/bin/sshfs
    kelatov@kmac:~$sudo mkdir /mnt/ssh
    kelatov@kmac:~$sudo chown kelatov /mnt/ssh
    

Now for the actual mount:

    kelatov@kmac:~$sshfs elatov@ssh.server.com:/mnt/data /mnt/ssh
    kelatov@kmac:~$df -Ph -T fuse4x
    Filesystem                        Size   Used  Avail Capacity  Mounted on
    elatov@ssh.server.com:/mnt/data  190Gi   80Gi  101Gi    45%    /mnt/ssh
    

You can un-mount the *sshfs* mount point like this:

    kelatov@kmac:~$umount /mnt/ssh
    

The way that *autofs* works is the type of the file system is always prepended with the *mount_* prefix and that is run to actually mount that file system. So if you specify **smbfs**, there must be a **mount_smbfs** command. Here are the available **mount** commands on the system:

    kelatov@kmac:~$compgen -c | grep ^mount
    mount
    mount_acfs
    mount_afp
    mount_cd9660
    mount_cddafs
    mount_devfs
    mount_exfat
    mount_fdesc
    mount_ftp
    mount_hfs
    mount_msdos
    mount_nfs
    mount_ntfs
    mount_smbfs
    mount_udf
    mount_webdav
    

So we need to create a *mount_sshfs* command. We can just create a *symlink* to the **sshfs** command like so:

    kelatov@kmac:~$sudo ln -s /opt/local/bin/sshfs /sbin/mount_sshfs
    

Now let&#8217;s edit the **/etc/autofs_amnt** file and add the following:

    ssh -fstype=sshfs,defer_permissions,allow_other,auto_cache elatov@ssh.server.com:/mnt/data
    

As always, refresh **automount** by running the following:

    sudo automount -vc
    

Now check to make sure **autofs** works:

    kelatov@kmac:~$cd /amnt/ssh 
    kelatov@kmac:/amnt/ssh$df -Ph .
    Filesystem                     Size   Used  Avail Capacity  Mounted on
    elatov@ssh.server.:/mnt/data  190Gi   80Gi  101Gi    45%    /amnt/ssh
    

That looks good, you can check the command that was executed by autofs to mount the sshfs mountpoint:

    kelatov@kmac:/amnt/ssh2$ps -ef | grep sshfs | grep -v grep
      502  1536     1   0  3:36PM ??         0:00.00 /sbin/mount_sshfs -o nobrowse -o nosuid,nodev -o defer_permissions,allow_other,auto_cache -o automounted elatov@ssh.server.com:/mnt/data /amnt/ssh
    

If it fails for some reason, grab that command and try to mount it manually to track down any issues. If you have any mount points that are stuck, try to restart both the **autofsd** and **automountd** daemons:

    kelatov@kmac:~$sudo launchctl stop com.apple.autofsd 
    kelatov@kmac:~$sudo launchctl start com.apple.autofsd 
    kelatov@kmac:~$sudo launchctl stop com.apple.automountd
    kelatov@kmac:~$sudo launchctl start com.apple.automountd
    

**autofsd** is automatically restart by **launchd**, so you can just stop it, and it will restart it. **Automountd** is started by **autofsd** so you can just stop that as well, and as soon as you try to auto mount something, it will automatically start up. If you want to get a feeling of all the file systems that are mounted you can run the following:

    kelatov@kmac:~$lsvfs 
    Filesystem                        Refs Flags
    -------------------------------- ----- ---------------
    nfs                                  1 
    hfs                                  1 local, dovolfs
    devfs                                0 
    autofs                               3 
    smbfs                                1 
    fuse4x                               1
    

