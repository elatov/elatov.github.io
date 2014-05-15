---
title: Extending the System Drive on Windows 2008 Running Under KVM
author: Karim Elatov
layout: post
permalink: /2013/04/extending-the-system-drive-on-windows-2008-running-as-a-kvm-vm/
dsq_thread_id:
  - 1405296261
categories:
  - Home Lab
  - OS
tags:
  - diskmgmt.msc
  - qemu-img resize
  - WIN2k8
---
While I was writing <a href="http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture']);">this</a> post I first allocated 15GB for my Windows install. I quickly realized that after a plethora of updates that is not enough space. Luckily it's pretty easy to remedy that with a two step process.

### 1. Increase the Underlying Hard Disk IMG file Used in KVM

Shutdown the VM and then using **virsh** figure out the full path of the IMG file used by the desired VM. Here is a list of all the VMs that are powered off:

    [virtuser@kvm ~]$ virsh -c qemu:///system list --inactive
     Id Name                 State
    ----------------------------------
      - VM1                  shut off
      - VM2                  shut off
      - kelatov_Win2k8       shut off
      - kelatov_win7_2       shut off
    

Let's see we wanted to resize the Hard Disk of the "kelatov-win7-2" VM. So go ahead and find out where the IMG file is for that VM:

    [virtuser@kvm ~]$ virsh -c qemu:///system domblklist kelatov_win7_2
    Target     Source
    ------------------------------------------------
    hda        /images/kelatov_win7_2.img
    hdc        -  
    

Now let's make sure the size of the file is 15GB like we expect:

    [virtuser@kvm ~]$ ls -lh /images/kelatov_win7_2.img
    -rw-------. 1 root root 16G Jun 21  2012 /images/kelatov_win7_2.img
    

That looks correct. Now let's go ahead and add 5GB to the IMG file:

    [virtuser@kvm images]$ sudo qemu-img resize kelatov_win7_2.img +5G
    Image resized.
    

Let's make sure the new size shows up:

    [virtuser@kvm ~]$ ls -lh /images/kelatov_win7_2.img
    -rw-------. 1 root root 21G Jun 21  2012 /images/kelatov_win7_2.img
    

### 2. Extend the Volume Inside the Windows 2008 OS

Power on the VM and from within Windows run:

    diskmgmt.msc
    

And you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/windows_disk_mgmt.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/windows_disk_mgmt.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/windows_disk_mgmt.png" alt="windows disk mgmt Extending the System Drive on Windows 2008 Running Under KVM" width="635" height="447" class="alignnone size-full wp-image-8058" title="Extending the System Drive on Windows 2008 Running Under KVM" /></a>

Then right click on the **C:** partition and then select "Extend Volume":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/right_click_c-part.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/right_click_c-part.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/right_click_c-part.png" alt="right click c part Extending the System Drive on Windows 2008 Running Under KVM" width="637" height="546" class="alignnone size-full wp-image-8059" title="Extending the System Drive on Windows 2008 Running Under KVM" /></a>

Then the "Extend Volume Wizard" will startup:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/extend_volume_wizard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/extend_volume_wizard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/extend_volume_wizard.png" alt="extend volume wizard Extending the System Drive on Windows 2008 Running Under KVM" width="497" height="394" class="alignnone size-full wp-image-8060" title="Extending the System Drive on Windows 2008 Running Under KVM" /></a>

Click "Next" and it will automatically select the available space on that disk:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/select_disks_extend_volume.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/select_disks_extend_volume.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/select_disks_extend_volume.png" alt="select disks extend volume Extending the System Drive on Windows 2008 Running Under KVM" width="495" height="395" class="alignnone size-full wp-image-8061" title="Extending the System Drive on Windows 2008 Running Under KVM" /></a>

In our case we have 5GB available which as I mentioned is automatically selected. At this point just click "Next" and then "Finish". After the process is finished, you will see the **C:** partition take up the rest of the drive:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/c_part_extended.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/c_part_extended.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/c_part_extended.png" alt="c part extended Extending the System Drive on Windows 2008 Running Under KVM" width="636" height="542" class="alignnone size-full wp-image-8062" title="Extending the System Drive on Windows 2008 Running Under KVM" /></a>

Now we can apply more updates <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Extending the System Drive on Windows 2008 Running Under KVM" class="wp-smiley" title="Extending the System Drive on Windows 2008 Running Under KVM" /> 

