---
title: ESXi Backups with ZFS and XSIBackup
author: Karim Elatov
layout: post
permalink: /2014/02/esxi-backups-zfs-xsibackup/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2215089363
categories:
  - Home Lab
  - Storage
  - VMware
  - ZFS
tags:
  - iSCSI
  - XSIBackup
  - ZFS
---
## ZFS Setup

I had two **zpools** in my setup:

    root@zfs:~#zpool list
    NAME    SIZE  ALLOC   FREE  EXPANDSZ    CAP  DEDUP  HEALTH  ALTROOT
    data    928G   238G   690G         -    25%  1.00x  ONLINE  -
    other   928G   248G   680G         -    26%  1.00x  ONLINE  -
    

The *data* pool had a ComStar ZVol presented to an ESXi host and another ZFS Volume used for ISOs shared over NFS:

    root@zfs:~#zfs list -r  data
    NAME        USED  AVAIL  REFER  MOUNTPOINT
    data        551G   363G   184K  /data
    data/isos  37.7G   363G  37.7G  /data/isos
    data/vm     503G   665G   200G  -
    

While the *other* zpool wasn&#8217;t used for anything but was the same size. I decided to use the *other* zpool for backups.

### ESXi VM Configuration

I only had 4 VMs running on the host, 3 of the VMs were running on local storage. The other VM was using the ComStar LUN to store a bunch of data. So I decided to use ZFS capabilities to do a LUN level backup for the ComStar ZVol.

## Send/Receive a ZFS Volume

I found a couple of sites that had instructions on how to copy ZFS Volumes across Zpools:

*   <a href="http://www.hlynes.com/2007/07/09/moving-zfs-filesystems-between-pools/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.hlynes.com/2007/07/09/moving-zfs-filesystems-between-pools/']);">Moving ZFS filesystems between pools</a>
*   <a href="http://www.headdesk.me/index.php?title=ZFS_incremental_replication" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.headdesk.me/index.php?title=ZFS_incremental_replication']);">ZFS incremental replication</a>
*   <a href="http://www.aisecure.net/2012/01/11/automated-zfs-incremental-backups-over-ssh/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.aisecure.net/2012/01/11/automated-zfs-incremental-backups-over-ssh/']);">Automated ZFS Incremental Backups Over SSH</a>

The gist of the commands would be like this:

1.  Take Snapshot of Source ZFS Volume
    
        zfs snapshot data/vm@1
        

2.  Send the snapshot over to the other pool and receive it
    
        zfs send -R data/vm@1 | zfs receive -Fu other/vm-backup
        

3.  If you want to do incremental backups, take another snapshot
    
        zfs snapshot data/vm@2
        

4.  Send an Incremental Snapshot to the Backup Zpool
    
        zfs send -Ri data/vm@1 data/vm@2 | zfs receive -Fu other/vm-backup
        

The **-R** option from the **zfs send** together with the **-F** option from **zfs receive** clean up snapshots on the destination side. The source and destination then look the same, instead of the Destination Volume continuing to aggregate ZFS volume snapshots. To automate the process I wrote a little bash script:

    root@zfs:~#cat vm-backup 
    #!/bin/bash
    ZFS=/usr/sbin/zfs
    ZFS_VOL_SRC=data/vm
    ZFS_VOL_DST=other/vm-backup
    CUR_SNAP=$($ZFS list -r -H -o name -t snapshot $ZFS_VOL_SRC)
    DATE=$(/usr/gnu/bin/date)
    SNAP_DATE=$($DATE +%m-%d)
    NEW_SNAP="$ZFS_VOL_SRC@$SNAP_DATE"
    
    function take_new_snapshot(){
            $ZFS snapshot $NEW_SNAP
    }
    
    take_new_snapshot
    if [ $? -ne 0 ]; then
            echo "snapshot creation failed with status $?"
            exit 1
    fi
    
    function zfs_send_inc(){
            $ZFS send -Ri $CUR_SNAP $NEW_SNAP | $ZFS receive -Fu $ZFS_VOL_DST
    }
    
    zfs_send_inc
    
    if [ $? -ne 0 ]; then
            echo "snapshot send failed with status $?"
            exit 1
    fi
    
    function zfs_cleanup(){
            $ZFS destroy $CUR_SNAP
    }
    
    zfs_cleanup
    
    if [ $? -ne 0 ]; then
            echo "snapshot deletion failed with status $?"
            exit 1
    fi
    
    echo "ZFS Backup Successful on $DATE"
    

The script will perform incremental backups. It&#8217;s under the assumption that you already sent the first backup and that there is only one snapshot on the Source ZFS Volume (which will be deleted after the copy is done). Adding that to **crontab** will automate the back up process for the LUN presented to the ESXi host.

### ZFS refreservation Property

My ZFS Volume was 300GB in size and was using 200GB of space, after I took a snapshot of that Volume I ended up taking 500GB of space:

    root@zfs:~#zfs list -r -t all -o space data/vm
    NAME           AVAIL   USED  USEDSNAP  USEDDS  USEDREFRESERV  USEDCHILD
    data/vm         665G   503G      176K    200G           302G          0
    data/vm@02-03      -   176K         -       -              -          -
    

This is because the **refreservation** flag is set on the volume (and this is preferrable when using ZFS together with iSCSI):

    root@zfs:~#zfs get refreservation data/vm
    NAME     PROPERTY        VALUE      SOURCE
    data/vm  refreservation  302G       local
    

There is a great description at <a href="http://nex7.blogspot.com/2013/03/reservation-ref-reservation-explanation.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://nex7.blogspot.com/2013/03/reservation-ref-reservation-explanation.html']);">Reservation & Ref Reservation &#8211; An Explanation (Attempt)</a> which helped me understand why all that space was utilized. <a href="http://docs.oracle.com/cd/E19253-01/819-5461/gazvb/index.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19253-01/819-5461/gazvb/index.html']);">From Setting ZFS Quotas and Reservations</a>:

> If *refreservation* is set, a snapshot is only allowed if sufficient unreserved pool space exists outside of this reservation to accommodate the current number of referenced bytes in the dataset.

Basically it absolutely ensures you don&#8217;t over provision space and it requires a total of **Reserved** + **Used Space** when a snapshot is taken. So in my scenario it made sense, I had a 300GB LUN which I was presenting over iSCSI and I was using 200GB of that LUN (**Referenced Bytes** or **Used Datasets**). In total that ends up to 500GB.

On the Source Zpool I didn&#8217;t mind, but on the backup Zpool, I only wanted to reserve the used space. So I went ahead and unset that property on the Destination ZFS volume:

    root@zfs:~# zfs set refreservation=none other/vm
    

and then the reserved space was released:

    root@zfs:~#zfs list -r -t all -o space other/vm-backup
    NAME                   AVAIL   USED  USEDSNAP  USEDDS  USEDREFRESERV  USEDCHILD
    other/vm-backup         499G   200G      136K    200G              0          0
    other/vm-backup@02-02      -   136K         -       -              -          -
    other/vm-backup@02-03      -      0         -       -              -          -
    

## VM Backups with XSIBackup

There is a pretty cool script called <a href="http://sourceforge.net/projects/xsibackup/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sourceforge.net/projects/xsibackup/']);">xsibackup</a>. It supports ESXi 5.1 and above, luckily I was on 5.1. The script basically takes a snapshot of VM(s) and then uses **vmkfstool** to clone the **vmdk**(s) to a destination VMFS volume.

### Presenting a ComSTAR ZFS Volume to ESXi

If you want you can use <a href="http://www.napp-it.org/index_en.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.napp-it.org/index_en.html']);">Napp-It</a> (if you are using an OpenSolaris Distribution) to present the backup LUN to ESXi (I described the process <a href="http://virtuallyhyper.com/2014/01/zfs-iscsi-benchmarks-tests/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/01/zfs-iscsi-benchmarks-tests/']);">here</a>). This time around I decided to go command line. Here is the process I followed:

1.  Create a ZFS Volume
    
        zfs create -V 200G other/backups
        

2.  Associate volume with ComSTAR
    
        sbdadm create-lu /dev/zvol/rdsk/other/backups
        

3.  Create Target group, if it doesn&#8217;t exist (I already had one from the napp-it config)
    
        stmfadm create-tg tg1
        

4.  Add Member (Target System) to Target group (I didn&#8217;t have to do this either, since I was using an existing Target Group). To get a list of targets on the system run the following: `stmfadm list-target`
    
        stmfadm add-tg-member -g tg1 iqn.2010-09.org.na
        

5.  Create a View for LUN to be accessible from the Target Group
    
        stmfadm add-view -t tg1 600144F0876A
        

6.  If you don&#8217;t care about Target Groups, you can just add a view and allow everyone to access the LUN
    
        stmfadm add-view 600144F0876A
        

7.  Enable Write Back Cache on LUN
    
        stmfadm modify-lu -p wcd=false 600144F0876A
        

8.  Do a rescan on the ESXi side to see the new LUN:
    
        esxcli storage core adapter rescan -A vmhba32
        

After the LUN is seen go ahead and put a VMFS volume on the iSCSI LUN (I called it **backups**).

### Install XSIBackup

The install process is described on the main <a href="http://sourceforge.net/projects/xsibackup/files/?source=navbar" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sourceforge.net/projects/xsibackup/files/?source=navbar']);">download</a> page. Here is a quick summary:

1.  Copy the Script to a local datastore
    
        scp xsibackup esx:/vmfs/volume/datastore1
        

2.  Set the script as executable
    
        ~ # chmod 700 /vmfs/volume/datastore1/xsibackup
        

3.  Run a test backup
    
        ~ # /vmfs/volumes/datastore1/xsibackup --backup-point=/vmfs/volumes/backups --backup-type=custom --backup-vms=VM2,VM5,VM7 --mail-from=admin@mail.com --mail-to=elatov@mail.com --smtp-srv=mail.domain.com --smtp-port=25 --smtp-auth=none
        

4.  The output will look something like this:
    
        Found --backup-point at /vmfs/volumes/backups
        Getting list of all VMs...
        VM: Vmid    Name             File          Guest OS               Version   Annotation
        VM: 1      VM1       [VMs] VM1/VM1.vmx     rhel6_64Guest           vmx-08
        VM: 2      VM2       [VMs] VM2/VM2.vmx     freebsd64Guest          vmx-08
        VM: 3      VM3       [VMs] VM3/VM3.vmx     rhel6Guest              vmx-08
        VM: 4      VM4       [VMs] VM4/VM4.vmx     rhel5Guest              vmx-08
        VM: 5      VM5       [VMs] VM5/VM5.vmx     debian6_64Guest         vmx-08
        VM: 6      VM6       [VMs] VM6/VM6.vmx     windows7Server64Guest   vmx-08
        VM: 7      VM7       [VMs] VM7/VM7.vmx     rhel6_64Guest           vmx-08
        VMs to backup:
        2      VM2    [VMs] VM2/VM2.vmx      freebsd64Guest          vmx-08               17507 /vmfs/volumes/529a6c18-ae956476-0872-0030489f1401/VM2
        5      VM5    [VMs] VM5/VM5.vmx     debian6_64Guest         vmx-08               17507 /vmfs/volumes/529a6c18-ae956476-0872-0030489f1401/VM5
        6      VM7    [VMs] VM7/VM7.vmx        windows7Server64Guest   vmx-08               45174 /vmfs/volumes/529a6c18-ae956476-0872-0030489f1401/VM7
        Needed room: 78 Gb.
        Available room: 190 Gb.
        Hot backup selected for VM: VM2 will not be switched off
        Hot backup selected for VM: VM5 will not be switched off
        Hot backup selected for VM: VM7 will not be switched off
        220 mail.domain.com ESMTP Exim 4.80 Sun, 02 Feb 2014 14:13:13 -0700
        250 mail.domain.com Hello esx.domain.com [192.168.1.111]
        250-mail.domain.com Hello esx.domain.com [192.168.1.111]
        250-SIZE 52428800
        250-8BITMIME
        250-PIPELINING
        250 HELP
        250 OK
        250 Accepted
        354 Enter message, ending with "." on a line by itself
        250 OK id=1WA4Lp-0001I4-6K
        221 mail.domain.com closing connection
        

5.  Add XSIBackup script to crontab. First stop the crontab process
    
        /bin/kill $(cat /var/run/crond.pid)
        

6.  Add the following to the **/var/spool/cron/crontabs/root** file
    
        30   5    9,18 *  *   /vmfs/volumes/datastore1/xsibackup --backup-point=/vmfs/volumes/backups --backup-type=custom --backup-vms=VM2,VM5,VM7 --mail-from=admin@mail.com --mail-to=elatov@mail.com --smtp-srv=mail.domain.com --smtp-port=25 --smtp-auth=none > /vmfs/volumes/datastore1/backup.log 2>&1
        

7.  Restart the crond process
    
        /usr/lib/vmware/busybox/bin/busybox crond
        

8.  The above changes are not permanent, and will be removed upon a reboot. To apply the changes on boot, add the following to the **/etc/rc.local.d/local.sh** file:
    
        ~ # cat /etc/rc.local.d/local.sh
        #!/bin/sh
        
        # local configuration options
        
        # Note: modify at your own risk!  If you do/use anything in this
        # script that is not part of a stable API (relying on files to be in
        # specific places, specific tools, specific output, etc) there is a
        # possibility you will end up with a broken system after patching or
        # upgrading.  Changes are not supported unless under direction of
        # VMware support.
        
        /bin/kill $(cat /var/run/crond.pid)
        /bin/echo "30 5 9,18 * * /vmfs/volumes/datastore1/xsibackup --backup-point=/vmfs/volumes/backups --backup-type=custom --backup-vms=VM2,VM5,VM7 --mail-from=admin@mail.com --mail-to=elatov@mail.com --smtp-srv=mail.domain.com --smtp-port=25 --smtp-auth=none > /vmfs/volumes/datastore1/backup.log 2>&1" >> /var/spool/cron/crontabs/root
        /usr/lib/vmware/busybox/bin/busybox crond
        exit 0
        

### SMTP Synchronization Error

At first my emails would fail with the following message:

> exim SMTP protocol synchronization error (input sent without waiting for greeting)

I was using Exim on my Linux box, the fix for that issue is described <a href="http://www.0937686468.com/2012/07/fixed-exim-smtp-protocol.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.0937686468.com/2012/07/fixed-exim-smtp-protocol.html']);">here</a>. I just needed to add the following option to my **exim** configuration:

    smtp_enforce_sync = false
    

After that was in place, I received the following email:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/02/xsi-report-2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/02/xsi-report-2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/02/xsi-report-2.png" alt="xsi report 2 ESXi Backups with ZFS and XSIBackup" width="675" height="188" class="alignnone size-full wp-image-10121" title="ESXi Backups with ZFS and XSIBackup" /></a>

The speeds were really good, I also checked out **esxtop** and latency was pretty good as well:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/02/esxtop-during-backup2_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/02/esxtop-during-backup2_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/02/esxtop-during-backup2_g-1024x96.png" alt="esxtop during backup2 g 1024x96 ESXi Backups with ZFS and XSIBackup" width="620" height="58" class="alignnone size-large wp-image-10122" title="ESXi Backups with ZFS and XSIBackup" /></a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2014/02/esxi-backups-zfs-xsibackup/" title=" ESXi Backups with ZFS and XSIBackup" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:iSCSI,XSIBackup,ZFS,blog;button:compact;">ZFS Setup I had two zpools in my setup: root@zfs:~#zpool list NAME SIZE ALLOC FREE EXPANDSZ CAP DEDUP HEALTH ALTROOT data 928G 238G 690G - 25% 1.00x ONLINE - other...</a>
</p>