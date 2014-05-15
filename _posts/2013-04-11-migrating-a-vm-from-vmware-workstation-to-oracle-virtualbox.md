---
title: Migrating a VM from VMware Workstation to Oracle VirtualBox
author: Karim Elatov
layout: post
permalink: /2013/04/migrating-a-vm-from-vmware-workstation-to-oracle-virtualbox/
dsq_thread_id:
  - 1405474938
categories:
  - Home Lab
  - OS
  - VMware
tags:
  - ovftool
  - VDDK
  - VirtualBox
---
Recently I had migrated laptops and I wanted to move my VMware workstation VMs to VirtualBox. All of my VMs were in the **.vmware** folder so I just copied that to my laptop. Here are the contents of that folder:

    [elatov@klaptop ~]$ ls -1 .vmware/
    ace.dat
    dndlogs
    favorites.vmls
    inventory.vmls
    playerUploadedData.log
    preferences
    preferences-private
    shortcuts
    UCSPM
    unity-helper.conf
    view-preferences
    Windows XP Professional
    workstationUploadedData.log
    

There are only two VMs: UCSPM (the UCS Manager Emulator) and Windows XP Professional (My Windows XP machine). I am just going to convert my Windows XP machine. Inside that folder, I saw the following:

    [elatov@klaptop ~]$ ls -1 .vmware/Windows\ XP\ Professional/
    caches
    vmware-0.log
    vmware-1.log
    vmware-2.log
    vmware.log
    Windows XP Professional.nvram
    Windows XP Professional-s001.vmdk
    Windows XP Professional-s002.vmdk
    Windows XP Professional-s003.vmdk
    Windows XP Professional-s004.vmdk
    Windows XP Professional-s005.vmdk
    Windows XP Professional-s006.vmdk
    Windows XP Professional-s007.vmdk
    Windows XP Professional-s008.vmdk
    Windows XP Professional-s009.vmdk
    Windows XP Professional-s010.vmdk
    Windows XP Professional-s011.vmdk
    Windows XP Professional.vmdk
    Windows XP Professional.vmsd
    Windows XP Professional.vmx
    Windows XP Professional.vmxf
    

Pretty standard stuff, but I realized that when I created that VM I used the 2GB Split Sparse VMDK format. I don't even know why I did that. I was probably thinking that if I was backing up to a FAT32 partition then this might help out. But who uses FAT partitions anymore? <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Migrating a VM from VMware Workstation to Oracle VirtualBox" class="wp-smiley" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /> 

So the first thing I wanted to do, was to convert the 2GB Split Spare VMDKs into a single monolithic VMDK (also reffered to as Monolithic Sparse VMDK). You can check out all the VMDK formats in the <a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vddk51_programming.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vddk51_programming.pdf']);">Virtual Disk Programming Guide Virtual Disk Development Kit (VDDK) 5.1</a>. Here is a table from that pdf:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/VMDK_Types.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/VMDK_Types.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/VMDK_Types.png" alt="VMDK Types Migrating a VM from VMware Workstation to Oracle VirtualBox" width="596" height="534" class="alignnone size-full wp-image-7772" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

### Convert Split Sparse VMDK to a Monolithic Sparse VMDK

Looking over a couple of sites, it looks like **vmware-vdiskmanager** is the way to go:

*   <a href="http://www.eknori.de/2012-11-23/vmware-converting-multiple-vmdk-files-into-one/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.eknori.de/2012-11-23/vmware-converting-multiple-vmdk-files-into-one/']);">VMWARE: Converting Multiple VMDK files into one</a> 
*   <a href="http://technonstop.com/convert-multiple-vmdks-to-one" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technonstop.com/convert-multiple-vmdks-to-one']);">Converting Multiple VMDK (Virtual Machine Disk) files into one</a> 

The **vmware-vdiskmanager** is packaged with the "Virtual Disk Development Kit" which you can download from <a href="http://www.vmware.com/support/developer/vddk/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/developer/vddk/']);">here</a>. Here is screenshot of the available downloads after I logged into the VMware portal:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/vddk_download.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/vddk_download.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/vddk_download.png" alt="vddk download Migrating a VM from VMware Workstation to Oracle VirtualBox" width="1314" height="380" class="alignnone size-full wp-image-7773" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

After I downloaded the archive, I had the following file:

    [elatov@klaptop downloads]$ ls *vix*
    VMware-vix-disklib-5.1.0-774844.x86_64.tar.gz
    

So I went ahead and extracted the contents:

    [elatov@klaptop downloads]$ tar xvzf VMware-vix-disklib-5.1.0-774844.x86_64.tar.gz
    

Now let's go ahead and install the package:

    [elatov@klaptop downloads]$ cd vmware-vix-disklib-distrib 
    [elatov@klaptop vmware-vix-disklib-distrib]$ sudo ./vmware-install.pl 
    Creating a new VMware VIX DiskLib API installer database using the tar4 format.
    
    Installing VMware VIX DiskLib API.
    
    You must read and accept the VMware VIX DiskLib API End User License Agreement to continue. 
    Press enter to display it. 
    ... 
    ... 
    What prefix do you want to use to install VMware VIX DiskLib API?
    
    The prefix is the root directory where the other folders such as man, bin, doc, lib, etc. will be placed. [/usr]
    
    The installation of VMware VIX DiskLib API 5.1.0 build-774844 for Linux completed successfully. You can decide to remove this software from your system at any time by invoking the following command: "/usr/bin/vmware-uninstall-vix-disklib.pl".
    
    Enjoy,
    
    ## --the VMware team
    

After the install, I tried to check the consistency of my files and I ran the following:

    [elatov@klaptop Windows XP Professional]$ vmware-vdiskmanager -R Windows\ XP\ Professional.vmdk
    VixDiskLib: Failed to load libvixDiskLibVim.so : Error = libvixDiskLibVim.so: cannot open shared object file: 
    No such file or directory.
    No errors were found on the virtual disk, 'Windows XP Professional.vmdk'.
    

I then re-read the "<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vddk_prog_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vddk_prog_guide.pdf']);">Virtual Disk API Programming Guide</a>", and saw the following:

> **To Install the package on Linux**
> 
> 1.  On the Download page, choose the binary tar.gz for either 32‐bit Linux or 64‐bit Linux.
> 2.  Unpack the archive, which creates the vmware-vix-disklib-distrib subdirectory.
>     
>         tar xvzf VMware-vix-disklib.*.tar.gz
>         
> 
> 3.  Change to that directory and run the installation script as root:
>     
>         cd vmware-vix-disklib-distrib
>         sudo ./vmware-install.pl
>         
> 
> 4.  Read the license terms and type **yes** to accept them.  
>     Software components install in /usr unless you specify otherwise.
>     
>     You might need to edit your **LD_LIBRARY_PATH** environment to include the library installation path, **/usr/lib/vmware-vix-disklib/lib32** (or lib64) for instance. Alternatively, you can add the library location to the list in **/etc/ld.so.conf** and run **ldconfig** as root.

So I went ahead and created a file **/etc/ld.so.conf.d/vmware-vix-64.conf** with the following contents:

    [elatov@klaptop ~]$ cat /etc/ld.so.conf.d/vmware-vix-64.conf
    /usr/lib/vmware-vix-disklib/lib64
    

I then ran **ldconfig** to apply the changes:

    [elatov@klaptop ~]$ sudo ldconfig -v | grep vix 
    /usr/lib/vmware-vix-disklib/lib64: 
       libvixDiskLib.so.5 -> libvixDiskLib.so.5.1.0 
       libvixDiskLibVim.so.5 -> libvixDiskLibVim.so.5.1.0
       libvixMntapi.so.1 -> libvixMntapi.so.1.1.0
    

and I can see the new libraries are now included. If you don't want to mess with the system's libraries you can always just set the **LB_LIBRARY_PATH** variable. Another person had issues by changing the **ld.so.conf** files and ended going that route. The issue and steps around it are described in <a href="http://communities.vmware.com/thread/303517" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/303517']);">this</a> VMware's Communities page.

Now re-running my consistency check, I saw the following:

    [elatov@klaptop Windows XP Professional]$ vmware-vdiskmanager -R Windows\ XP\ Professional.vmdk
    No errors were found on the virtual disk, 'Windows XP Professional.vmdk'.
    

That looks good. Now let's go ahead and convert it. Checking out the `vmware-vdiskmanager --help` output, I saw the following:

     -r <source -disk/>     : convert the specified disk; need to specify
                            destination disk-type.  For local destination disks
                            the disk type must be specified.
    

And here are the available disk types:

    Disk types:
          0                   : single growable virtual disk
          1                   : growable virtual disk split in 2GB files
          2                   : preallocated virtual disk
          3                   : preallocated virtual disk split in 2GB files
          4                   : preallocated ESX-type virtual disk
          5                   : compressed disk optimized for streaming
          6                   : thin provisioned virtual disk - ESX 3.x and above
    

So the command for the conversion, looked like this:

    [elatov@klaptop Windows XP Professional]$ vmware-vdiskmanager -r Windows\ XP\ Professional.vmdk -t 0 Windows_XP.vmdk 
    Creating disk 'Windows_XP.vmdk'
    Convert: 4% done.
    

and that went on for a little bit. Notice that the destination VMDK is called *Windows_XP.vmdk*. After the conversion is finished we will see this:

    Convert: 100% done.
    Virtual disk conversion successful.
    

Checking out the final file, I saw the following:

    [elatov@klaptop Windows XP Professional]$ ls -lh Windows_XP.vmdk
    -rw------- 1 elatov elatov 18G Mar 22 15:10 Windows_XP.vmdk
    

and then checking the old files:

    [elatov@klaptop Windows XP Professional]$ du -hsc *-s0*
    2.0G    Windows XP Professional-s001.vmdk
    2.0G    Windows XP Professional-s002.vmdk
    2.0G    Windows XP Professional-s003.vmdk
    2.0G    Windows XP Professional-s004.vmdk
    2.0G    Windows XP Professional-s005.vmdk
    5.1M    Windows XP Professional-s006.vmdk
    2.0G    Windows XP Professional-s007.vmdk
    2.0G    Windows XP Professional-s008.vmdk
    2.0G    Windows XP Professional-s009.vmdk
    1.1G    Windows XP Professional-s010.vmdk
    1022M   Windows XP Professional-s011.vmdk
    18G total
    

The size matched up, which is perfect.

From this point on, I could've probably just added the vmdk to VirtualBox, but I wanted to preserve all the Memory and CPU settings. To save those settings we can package the VMX and VMDK into an OVA template and then import it into VirtualBox.

## Create an OVA Template from a VMware Workstation VM

The VMX file is where all the configurations are stored, and my VMX file was still pointing at the old Split Sparse VMDK:

    [elatov@klaptop Windows XP Professional]$ grep vmdk *.vmx
    scsi0:0.fileName = "Windows XP Professional.vmdk"
    

I edited the VMX file and pointed to the newly converted VMDK. After I was done, I had the following:

    [elatov@klaptop Windows XP Professional]$ grep vmdk Windows\ XP\ Professional.vmx
    scsi0:0.fileName = "Windows_XP.vmdk"
    

Now that my VM is ready to be imported into an OVA, let's check out the <a href="http://www.vmware.com/support/developer/ovf/ovf301/ovftool-301-userguide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/support/developer/ovf/ovf301/ovftool-301-userguide.pdf']);">OVF Tool User Guide</a>. From the guide, here is the install process:

> **To install the VMware OVF Tool**
> 
> 1.  Download VMware OVF Tool as an installer or an archive (zipped/compressed) file:
> 2.  Install using the method for your operating system:

<a href="http://www.vmware.com/support/developer/ovf/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/developer/ovf/']);">Here</a> is the download page for the *ovftool* application. After I logged in, here were the downloads that I saw:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Download_Ovftool.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Download_Ovftool.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Download_Ovftool.png" alt="Download Ovftool Migrating a VM from VMware Workstation to Oracle VirtualBox" width="1307" height="603" class="alignnone size-full wp-image-7780" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

When I was done with the download, I had the following file:

    [elatov@klaptop downloads]$ ls *ovf*
    VMware-ovftool-3.0.1-801290-lin.x86_64.txt
    

Now let's install the ovf tool:

    [elatov@klaptop downloads]$ chmod +x VMware-ovftool-3.0.1-801290-lin.x86_64.txt 
    [elatov@klaptop downloads]$ sudo ./VMware-ovftool-3.0.1-801290-lin.x86_64.txt 
    Extracting VMware Installer.
    

At this point a GUI installer will come up, like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer.png" alt="OVF Installer Migrating a VM from VMware Workstation to Oracle VirtualBox" width="642" height="509" class="alignnone size-full wp-image-7781" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Just hit "Install" and the process with go through pretty quickly. After it's finished you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer_Finished.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer_Finished.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_Installer_Finished.png" alt="OVF Installer Finished Migrating a VM from VMware Workstation to Oracle VirtualBox" width="642" height="509" class="alignnone size-full wp-image-7782" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

In the <a href="http://www.vmware.com/support/developer/ovf/ovf301/ovftool-301-userguide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/support/developer/ovf/ovf301/ovftool-301-userguide.pdf']);">OVF User Guide</a> there are good examples of how to use *ovftool*. Here is what I ran to create my OVA template:

    [elatov@klaptop Windows XP Professional]$ ovftool Windows\ XP\ Professional.vmx Win_XP.ova 
    Opening VMX source: Windows XP Professional.vmx 
    Opening OVA target: Win_XP.ova 
    Writing OVA package: Win_XP.ova
    Progress: 2%
    

It started to create the template. The extension is actually important, if I specify an "ovf" extension then it will create an OVF file along with VMDKs. Where the '.ova' extension encompasses both. From the guide:

> **Converting a VMX to an OVF**
> 
> To convert a virtual machine in VMware runtime format (.vmx) to an OVF package, use the following syntax:
> 
>     ovftool /vms/my_vm.vmx /ovfs/my_vapp.ovf 
>     
> 
> The result is located in /ovfs/my_vapp.[ovf|vmdk]
> 
> **Converting a VMX to an OVA**
> 
> To convert a VMX to an OVA file, use the following syntax:
> 
>     ovftool vmxs/Nostalgia.vmx ovfs/Nostalgia.ova
>     

Also from the same guide:

> Supports both import and generation of OVA packages (OVA is part of the OVF standard, and contains all the files of a virtual machine or vApp in a single file.)

Here is also a table comparison:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_VS_OVA.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_VS_OVA.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/OVF_VS_OVA.png" alt="OVF VS OVA Migrating a VM from VMware Workstation to Oracle VirtualBox" width="568" height="207" class="alignnone size-full wp-image-7783" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

After the process was done, I saw the following:

    [elatov@klaptop Windows XP Professional]$ ovftool Windows\ XP\ Professional.vmx Win_XP.ova 
    Opening VMX source: Windows XP Professional.vmx 
    Opening OVA target: Win_XP.ova 
    Writing OVA package: Win_XP.ova 
    Transfer Completed
    Completed successfully
    

Now checking for the OVA file:

    [elatov@klaptop Windows XP Professional]$ ls -lh Win_XP.ova
    -rw------- 1 elatov elatov 11G Mar 22 13:54 Win_XP.ova
    

To get information about the OVA file you can also use *ovftool* in "probe mode":

    [elatov@klaptop Windows XP Professional]$ ovftool Win_XP.ova
    OVF version:   1.0
    VirtualApp:    false
    Name:          Windows XP Professional
    
    Download Size:    10.66 GB
    
    Deployment Sizes:
      Flat disks:     18.00 GB
      Sparse disks:   17.80 GB
    
    Networks:
      Name:        nat
      Description: The nat network
    
    Virtual Hardware:
      Family:       vmx-09
      Disk Types:   SCSI-buslogic
    

As a last note, an OVA file is just a tar archive, and you can check the contents of the OVA file like so:

    [elatov@klaptop Windows XP Professional]$ tar tvf Win_XP.ova 
    -rw-r--r-- someone/64 6284 2013-03-22 13:42 Win_XP.ovf 
    -rw-r--r-- someone/64 125 2013-03-22 13:42 Win_XP.mf
    -rw-r--r-- someone/64 11445539328 2013-03-22 13:54 Win_XP-disk1.vmdk
    

All of the above looks good, now let's import the OVA template into VirtualBox.

### Import an OVA Template into VirtualBox

We can use the **VBoxManage** to import an OVA Template. From the command line:

    [elatov@klaptop ~]$  VBoxManage import
    Usage:
    
    VBoxManage import           <ovf /ova>
                                [--dry-run|-n]
                                [--options keepallmacs|keepnatmacs]
                                [more options]
                                (run with -n to have options displayed
                                 for a particular OVF)
    

So let's use -n to see all the options:

    [elatov@klaptop ~]$ VBoxManage import -n .vmware/Windows\ XP\ Professional/Win_XP.ova 0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
    Interpreting /home/elatov/.vmware/Windows\ XP\ Professional/Win_XP.ova...
    OK.
    Disks:  vmdisk1 18  19109117952 http://www.vmware.com/interfaces/specifications/vmdk.html#streamOptimized   Win_XP-disk1.vmdk   11445539328 -1  
    Virtual system 0:
     0: Suggested OS type: "WindowsXP"
        (change with "--vsys 0 --ostype <type>"; use "list ostypes" to list all possible values)
     1: Suggested VM name "vm"
        (change with "--vsys 0 --vmname <name>")
     2: Number of CPUs: 1
        (change with "--vsys 0 --cpus <n>")
     3: Guest memory: 512 MB
        (change with "--vsys 0 --memory <mb>")
     4: USB controller
        (disable with "--vsys 0 --unit 4 --ignore")
     5: Network adapter: orig nat, config 2, extra type=nat
     6: CD-ROM
        (disable with "--vsys 0 --unit 6 --ignore")
     7: SCSI controller, type BusLogic
        (change with "--vsys 0 --unit 7 --scsitype {BusLogic|LsiLogic}";
        disable with "--vsys 0 --unit 7 --ignore")
     8: IDE controller, type PIIX4
        (disable with "--vsys 0 --unit 8 --ignore")
     9: Hard disk image: source image=Win_XP-disk1.vmdk, target path=/home/elatov/.virt/vm/Win_XP-disk1.vmdk, controller=7;channel=0
        (change target path with "--vsys 0 --unit 9 --disk path";
        disable with "--vsys 0 --unit 9 --ignore")
    

That looks perfect. There is only one Virtual Disk and the Memory, CPU, and other settings are there as well.

Running without the -n (dry run) option looked like this:

    9: Hard disk image: source image=Win_XP-disk1.vmdk, target path=/home/elatov/.virt/vm/Win_XP-disk1.vmdk, controller=7;channel=0 
        (change target path with "--vsys 0 --unit 9 --disk path"; 
        disable with "--vsys 0 --unit 9 --ignore")
    0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
    Successfully imported the appliance.
    

Initially I had an issue with the OVA template, another user ran into the issues and it's described in <a href="https://forums.virtualbox.org/viewtopic.php?f=8&t=49682" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forums.virtualbox.org/viewtopic.php?f=8&t=49682']);">this</a> VirtualBox forum. I got around the issue by re-creating another OVA template. If you still have issues just extract the OVA into a folder and then import the OVF instead. That process seems to be more stable, here is the command you would run if you had extracted the OVA template under a folder called **test**:

    [elatov@klaptop ~]$ VBoxManage import test/Win_XP.ovf
    

Another person had a similar issue when they renamed the ova file. You can read more about it <a href="http://funnymonkey.com/do-not-rename-your-virtualbox-ova-file" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://funnymonkey.com/do-not-rename-your-virtualbox-ova-file']);">here</a>.

After the import is finished, start VirtualBox and you will see you newly imported VM:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/VirtualBox_with_VM_Imported.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/VirtualBox_with_VM_Imported.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/VirtualBox_with_VM_Imported.png" alt="VirtualBox with VM Imported Migrating a VM from VMware Workstation to Oracle VirtualBox" width="772" height="579" class="alignnone size-full wp-image-7784" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

If you want to keep it command line, you can run:

    VBoxManage list -l vms
    

And that will show you a lot of information regarding the VM that you just imported. Here is a shorter version:

    [elatov@klaptop ~]$ VBoxManage list vms
    "vm" {26008c65-d6ef-40d8-8a2e-093a5eb8baa5}
    

After powering on the VM, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/WIN_Boot_Error.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/WIN_Boot_Error.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/WIN_Boot_Error.png" alt="WIN Boot Error Migrating a VM from VMware Workstation to Oracle VirtualBox" width="722" height="470" class="alignnone size-full wp-image-7817" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

## Fixing "Error loading operating system" After Migrating XP VM

The first that I did was change the Disk Controller from SCSI to IDE. Here is how the Storage settings initially after the migration:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Storage_Settings_after_Conversion.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Storage_Settings_after_Conversion.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Storage_Settings_after_Conversion.png" alt="Storage Settings after Conversion Migrating a VM from VMware Workstation to Oracle VirtualBox" width="666" height="501" class="alignnone size-full wp-image-7818" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Then I changed the Contoller to IDE and also added my XP ISO, so I could boot from it. Here is how the settings looked like after the changes:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_to_ide.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_to_ide.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_to_ide.png" alt="storage settings to ide Migrating a VM from VMware Workstation to Oracle VirtualBox" width="666" height="501" class="alignnone size-full wp-image-7819" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Reboot the VM and you will see "Press any key to boot from the CD..". I pressed "Enter" and it started booting from the CD and then you will see this screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_welcome_screen.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_welcome_screen.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_welcome_screen.png" alt="xp welcome screen Migrating a VM from VMware Workstation to Oracle VirtualBox" width="722" height="466" class="alignnone size-full wp-image-7820" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

At this point I typed "R" to bring up the "Recovery Command Prompt". At the command prompt, I ran the following:

    fixmbr c:
    fixboot c:
    

Here is how that looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/fixboot_fixmbr.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/fixboot_fixmbr.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/fixboot_fixmbr.png" alt="fixboot fixmbr Migrating a VM from VMware Workstation to Oracle VirtualBox" width="722" height="466" class="alignnone size-full wp-image-7821" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

That should re-install the MBR on the disk. After I rebooted the error was gone, but it just showed a black screen like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/blank-screen-after-fix-boot.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/blank-screen-after-fix-boot.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/blank-screen-after-fix-boot.png" alt="blank screen after fix boot Migrating a VM from VMware Workstation to Oracle VirtualBox" width="722" height="470" class="alignnone size-full wp-image-7822" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

At this point I booted from the Vista Recovery Disk. The disk used to be available for free from "<a href="http://neosmart.net/blog/2008/windows-vista-recovery-disc-download/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://neosmart.net/blog/2008/windows-vista-recovery-disc-download/']);">Windows Vista Recovery Disc Download</a>", but now you have to pay for it. If you have a Vista Install CD, you can use that as well. Here is how my storage settings looked after I added the new ISO:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_with_vista_recovery.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_with_vista_recovery.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_settings_with_vista_recovery.png" alt="storage settings with vista recovery Migrating a VM from VMware Workstation to Oracle VirtualBox" width="666" height="501" class="alignnone size-full wp-image-7823" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Rebooting the VM and pressing "Enter" at the "Press any key to boot from CD....", I saw the following screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/win_vista_install_windows.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/win_vista_install_windows.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/win_vista_install_windows.png" alt="win vista install windows Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7824" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

I then clicked "Next" and saw the following screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair_your_computer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair_your_computer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair_your_computer.png" alt="vista repair your computer Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7825" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Then I clicked "Repair your Computer" and I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair-options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair-options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_repair-options.png" alt="vista repair options Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7826" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

At that screen I clicked "Next" and that yielded this screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_rec-options_command_prompt.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_rec-options_command_prompt.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_rec-options_command_prompt.png" alt="vista rec options command prompt Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7827" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

I then clicked "Command Prompt" and in the command prompt I fixed the MBR again (just for good measure) with following commands:

    bootrec /fixmbr
    bootrec /fixboot
    

Here is how it looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/bootrec_vista.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/bootrec_vista.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/bootrec_vista.png" alt="bootrec vista Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7828" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Looking around some settings, I noticed that the partition is not active, I then ran the following to activate the partition:

    c:\diskpart
    DISKPART>select disk 0
    DISKPART>select partition 1
    DISKPART>active
    

Here is how it looked like in the prompt:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_mark_partition_active.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_mark_partition_active.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/vista_mark_partition_active.png" alt="vista mark partition active Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7829" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

Notice the "*" (star) next to the partition after making it active. Then I rebooted and I saw a successful Windows boot process:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_successful_boot.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_successful_boot.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/xp_successful_boot.png" alt="xp successful boot Migrating a VM from VMware Workstation to Oracle VirtualBox" width="802" height="670" class="alignnone size-full wp-image-7830" title="Migrating a VM from VMware Workstation to Oracle VirtualBox" /></a>

<root>

</root></mb></n></name></type></ovf>

