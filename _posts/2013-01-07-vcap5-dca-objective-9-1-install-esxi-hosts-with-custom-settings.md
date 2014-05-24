---
title: VCAP5-DCA Objective 9.1 – Install ESXi hosts with custom settings
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-9-1-install-esxi-hosts-with-custom-settings/
dsq_thread_id:
  - 1416325118
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify custom installation options

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf)":

> **Options for Installing ESXi**
> ESXi can be installed in several ways. To ensure the best vSphere deployment, understand the options thoroughly before beginning the installation.
>
> ESXi installations are designed to accommodate a range of deployment sizes.
>
> Depending on the installation method you choose, different options are available for accessing the installation media and booting the installer.
>
> **Interactive ESXi Installation**
> Interactive installations are recommended for small deployments of fewer than five hosts.
>
> You boot the installer from a CD or DVD, from a bootable USB device, or by PXE booting the installer from a location on the network. You follow the prompts in the installation wizard to install ESXi to disk.
>
> **Scripted ESXi Installation**
> Running a script is an efficient way to deploy multiple ESXi hosts with an unattended installation.
>
> The installation script contains the host configuration settings. You can use the script to configure multiple hosts with the same settings.
>
> The installation script must be stored in a location that the host can access by HTTP, HTTPS, FTP, NFS, CDROM, or USB. You can PXE boot the ESXi installer or boot it from a CD/DVD or USB drive.
>
> ![scripted installation VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/scripted_installation.png)
>
> **vSphere Auto Deploy ESXi Installation Option**
> With the vSphere Auto Deploy ESXi Installation, you can provision and reprovision large numbers of ESXi hosts efficiently with vCenter Server.
>
> Using the Auto Deploy feature, vCenter Server loads the ESXi image directly into the host memory. Auto Deploy does not store the ESXi state on the host disk. vCenter Server stores and manages ESXi updates and patching through an image profile, and, optionally, the host configuration through a host profile
>
> **Customizing Installations with ESXi Image Builder CLI**
> You can use ESXi Image Builder CLI to create ESXi installation images with a customized set of updates, patches, and drivers.
>
> ESXi Image Builder CLI is a PowerShell CLI command set that you can use to create an ESXi installation image with a customized set of ESXi updates and patches. You can also include third-party network or storage drivers that are released between vSphere releases.
>
> You can deploy an ESXi image created with Image Builder in either of the following ways:
>
> *   By burning it to an installation DVD.
> *   Through vCenter Server, using the Auto Deploy feature.

### Identify ESXi Image Builder requirements

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf)":

> **Install Image Builder PowerCLI and Prerequisite Software**
> Before you can run Image Builder cmdlets, you must install vSphere PowerCLI and all prerequisite software. The Image Builder snap-in is included with the PowerCLI installation.
> You install Image Builder and prerequisite software on a Microsoft Windows system.
>
> **Procedure**
>
> 1.  Install Microsoft .NET 2.0 from the Microsoft website following the instructions on that website.
> 2.  Install Microsoft PowerShell 1.0 or 2.0. from the Microsoft website following the instructions on that website.
> 3.  Install vSphere PowerCLI, which includes the Image Builder cmdlets.

### Create/Edit Image Profiles

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf)":

> Create an Image Profile
> Cloning a published profile is the easiest way to create a custom image profile. Cloning a profile is especially useful if you want to remove a few VIBs from a profile, or if you want to use hosts from different vendors and want to use the same basic profile, but want to add vendor-specific VIBs. VMware partners or large installations might consider creating a profile from scratch.
>
> Administrators performing this task must have some experience with PowerCLI or Microsoft PowerShell.
>
> **Procedure**
>
> 1.  At the PowerShell prompt, add the depot that contains the profile you want to clone to the current session
>     ![image builder add software depot VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/image_builder_add_software_depot.png)
>     The cmdlet returns one or more SoftwareDepot objects.
> 2.  (Optional) Run the **Get-EsxImageProfile** cmdlet to find the name of the profile that you want to clone.
>
>	     Get-ESXImageProfile
>
>     You can use filtering options with **Get-EsxImageProfile**.
> 3.  Run the **New-EsxImageProfile** cmdlet to create the new profile and use the **-CloneProfile** parameter to specify the profile you want to clone.
>
> 		New-EsxImageProfile -CloneProfile My_Profile -Name "Test Profile 42"
>
>  This example clones the profile named My-Profile and assigns it the name Test Profile 42. You must specify a unique combination of name and vendor for the cloned profile.

Let's say you wanted to create a custom profile for the 5.0U1 update. First download the offline zip bundle from My VMware:

![5 0U1 offline bundle download VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/5_0U1_offline_bundle_download.png)

Once downloaded you will see the following:

![offline bundle downloaded VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/offline_bundle_downloaded.png)

Then open up PowerCLI and import the zip as an Software Depot:


	PowerCLI C:\> Add-EsxSoftwareDepot C:\Users\Administrator\Desktop\isos\update-from-esxi5.0-5.0_update01.zip

	Depot Url
	---------
	zip:C:\Users\Administrator\Desktop\isos\update-from-esxi5.0-5.0_update01.zip...

To check out available profiles from the Depot you can do this :

	PowerCLI C:\> Get-EsxImageProfile | select Name,Vendor

	Name Vendor
	---- ------
	ESXi-5.0.0-20120302001-standard VMware, Inc.
	ESXi-5.0.0-20120302001-no-tools VMware, Inc.
	ESXi-5.0.0-20120301001s-standard VMware, Inc.
	ESXi-5.0.0-20120301001s-no-tools VMware, Inc.

To see available VIBs (packages) from the Depot, run the following:

	PowerCLI C:\> Get-EsxSoftwarePackage

	Name Version Vendor Release Date
	---- ------- ------ ------------
	net-ixgbe 2.0.84.8.2-10vmw.500.0.0.46... VMware 8/19/2011...
	net-nx-nic 4.0.557-3vmw.500.1.11.623860 VMware 2/17/2012...
	scsi-rste 2.0.2.0088-1vmw.500.1.11.62... VMware 2/17/2012...
	net-e1000 8.0.3.1-2vmw.500.0.7.515841 VMware 12/15/201...
	ehci-ehci-hcd 1.0-3vmw.500.0.0.469512 VMware 8/19/2011...

To see what VIBs are available from a specific profile you can do the following:

	PowerCLI C:\> Get-EsxImageProfile ESXi-5.0.0-20120302001-no-tools | select -ExpandProperty VibList

	Name Version Vendor Release Date
	---- ------- ------ ------------
	ata-pata-atiixp 0.4.6-3vmw.500.0.0.469512 VMware 8/19/2011...
	net-nx-nic 4.0.557-3vmw.500.1.11.623860 VMware 2/17/2012...
	scsi-rste 2.0.2.0088-1vmw.500.1.11.62... VMware 2/17/2012...
	net-e1000 8.0.3.1-2vmw.500.0.7.515841 VMware 12/15/201...

Now if you want to create a profile by cloning an existing one, you can do the following:

	PowerCLI C:\> New-EsxImageProfile -CloneProfile ESXi-5.0.0-20120302001-no-tools -Name My_Cloned_Profile

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Cloned_Profile VMware, Inc. 2/17/2012 11... PartnerSupported

	PowerCLI C:\> Get-EsxImageProfile

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Cloned_Profile VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120302001-stan... VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120302001-no-t... VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120301001s-sta... VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120301001s-no-... VMware, Inc. 2/17/2012 11... PartnerSupported


We can also create profiles manually. There is a good example in "[VMware vSphere 5.0 Evaluation Guide Volume One](http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-1.pdf)". Here is what I did to create a manual profile with just 4 VIBs:

	PowerCLI C:\> New-EsxImageProfile -NewProfile My_Manual_Profile -vendor VMware -SoftwarePackage esx-base

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Manual_Profile VMware 12/25/2012 3... VMwareCertified

	PowerCLI C:\> Add-EsxSoftwarePackage -ImageProfile My_Manual_Profile -SoftwarePackage esx-tboot

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Manual_Profile VMware 12/25/2012 3... VMwareCertified

	PowerCLI C:\> Add-EsxSoftwarePackage -ImageProfile My_Manual_Profile -SoftwarePackage misc-drivers

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Manual_Profile VMware 12/25/2012 3... VMwareCertified

	PowerCLI C:\> Add-EsxSoftwarePackage -ImageProfile My_Manual_Profile -SoftwarePackage net-e1000e

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Manual_Profile VMware 12/25/2012 3... VMwareCertified

Now checking over my manual profile, I see the following:

	PowerCLI C:\> Get-EsxImageProfile

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	ESXi-5.0.0-20120301001s-no-... VMware, Inc. 2/17/2012 11... PartnerSupported
	My_Cloned_Profile VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120302001-no-t... VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120301001s-sta... VMware, Inc. 2/17/2012 11... PartnerSupported
	My_Manual_Profile VMware 12/25/2012 1... VMwareCertified
	ESXi-5.0.0-20120302001-stan... VMware, Inc. 2/17/2012 11... PartnerSupported

	PowerCLI C:\> Get-EsxImageProfile My_Manual_Profile | select -ExpandProperty VibList

	Name Version Vendor Release Date
	---- ------- ------ ------------
	net-e1000e 1.1.2-3vmw.500.1.11.623860 VMware 2/17/2012...
	esx-tboot 5.0.0-0.0.469512 VMware 8/19/2011...
	esx-base 5.0.0-1.11.623860 VMware 2/17/2012...
	misc-drivers 5.0.0-1.11.623860 VMware 2/17/2012...

If you want to remove a VIB (package) from a profile, you can do the following:

	PowerCLI C:\> Get-EsxImageProfile My_Manual_Profile | select -ExpandProperty VibList

	Name Version Vendor Release Date
	---- ------- ------ ------------
	net-e1000e 1.1.2-3vmw.500.1.11.623860 VMware 2/17/2012...
	esx-tboot 5.0.0-0.0.469512 VMware 8/19/2011...
	esx-base 5.0.0-1.11.623860 VMware 2/17/2012...
	misc-drivers 5.0.0-1.11.623860 VMware 2/17/2012...

	PowerCLI C:\> Remove-EsxSoftwarePackage -ImageProfile My_Manual_Profile -SoftwarePackage net-e1000e

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Manual_Profile VMware 12/25/2012 3... VMwareCertified

	PowerCLI C:\> Get-EsxImageProfile My_Manual_Profile | select -ExpandProperty VibList

	Name Version Vendor Release Date
	---- ------- ------ ------------
	esx-tboot 5.0.0-0.0.469512 VMware 8/19/2011...
	esx-base 5.0.0-1.11.623860 VMware 2/17/2012...
	misc-drivers 5.0.0-1.11.623860 VMware 2/17/2012...

Once you are done customizing your profile you can export it as a zip (to install with VUM or esxcli) or you can export it as an ISO (from which you can boot and update your esxi install). Here is how each look like:

	PowerCLI C:\> Export-EsxImageProfile -ImageProfile My_Manual_Profile -ExportToIso -FilePath c:\share\myManualProfile.iso
	PowerCLI C:\> Export-EsxImageProfile -ImageProfile My_Manual_Profile -ExportToBundle -FilePath c:\share\myManualProfile.zip

Then checking for the files:

	PowerCLI C:\> dir c:\share | findstr Manual
	-a--- 12/25/2012 3:28 PM 142745600 myManualProfile.iso
	-a--- 12/25/2012 3:29 PM 133309774 myManualProfile.zip

### Install/uninstall custom drivers

VMware KB [2005205](http://kb.vmware.com/kb/2005205) talks about the process:

> **To add async drivers to the ESXi installation ISO**:
>
> 1.  Launch the vSphere 5.x PowerCLI command line.
> 2.  Download a copy of the ESXi offline bundle depot and async driver zip file.
> 3.  Extract the contents of the async driver zip file and identify the offline-bundle.zip files(s).
> 4.  Use the **Add-ESXSoftwareDepot** commandlet to add both the ESXi offline bundle and async offline bundle as depots.
>
>        For example:
>
>     	Add-EsxSoftwareDepot C:\path\to\new-async-driver-offline-bundle.zip, C:\path\to\esxi-offline-bundle.zip
>
>       Example for ESXi 5.0:
>
>     	Add-EsxSoftwareDepot C:\path\to\new-async-driver-offline-bundle.zip, C:\path\to\VMware-ESXi-5.0.0-469512-depot.zip
>
>       Example for ESXi 5.0 Update 1:
>
> 		Add-EsxSoftwareDepot C:\path\to\new-async-driver-offline-bundle.zip, C:\path\to\update-from-esxi5.0-5.0_update01.zip
>
>       The output appears similar to:
>
>     	Depot Url
>     	---------
>     	zip:C:\path\to\new-async-driver-offline-bundle.zip?index.xml
>		zip:C:\VMware-ESXi-5.0.0-469512-depot.zip?index.xml
>
> 5. Verify that the async driver is now available as a software package.
>
>       For example:
>
> 		 Get-EsxSoftwarePackage
>
>       The output appears similar to:
>
> 		 Name Version Vendor Release Date
> 		 ------------------- ------- ---------- ------------
> 		 driver-package-name 1.2.3.4 vendorname mm/dd/yyyy
>
> 6. Clone an existing image profile:
>        Use the **Get-EsxImageProfile** commandlet to list available image profiles.
>
>       For example:
>
>		Get-EsxImageProfile
>
>       The output appears similar to:
>
>		Name Vendor Last Modified Acceptance
>		-------------------------- ------ ------------- ---------------
>		ESXi-5.0.0-456551-standard VMware mm/dd/yyyy PartnerSupported
>		ESXi-5.0.0-456551-no-tools VMware mm/dd/yyyy PartnerSupported
>
> 7. Clone an existing available image profile by specifying a new name for the profile.
>       For example:
>
>		New-EsxImageProfile -CloneProfile "ESXi-5.0.0-456551-standard" -name "NewAsyncProfile" -Vendor "MyCorp"
>
>       The output appears similar to:
>
>		Name Vendor Last Modified Acceptance Level
>		--------------- ------ ------------- ----------------
>		NewAsyncProfile MyCorp mm/dd/yyyy PartnerSupported
>
> 8. Use the **Add-EsxSoftwarePackage** commandlet to add the async driver to the new image profile, specifying the package name from step 5.
>
>       For example:
>
>		Add-EsxSoftwarePackage -ImageProfile "NewAsyncProfile" -SoftwarePackage "driver-package-name"
>
>       The output appears similar to:
>
>		Name Vendor Last Modified Acceptance Level
>		--------------- ------ ------------- ----------------
>		NewAsyncProfile VMware today PartnerSupported
>
> 9. Export the new image profile. Run the **Export-EsxImageProfile** command to export the image profile as an ISO.
>       For example:
>
>		Export-EsxImageProfile -ImageProfile "NewAsyncProfile" -ExportToISO -filepath C:\NewAsyncProfile.iso
>
> 10. If necessary, burn the ISO to a new CD. Use the CD or ISO to boot the server and install ESXi. Follow the normal installation procedures.

From the previous objective we have already imported the 5.0U1 offline bundle. Now let's download an offline-bundle for a driver and insert it into a new merged profile that we create. Let say you downloaded a driver and it looked like this:

![igb offline bundle VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/igb_offline_bundle.png)

After extracting the zip you see the following contents:

![igb driver extracted VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/igb_driver_extracted.png)

Now let's import the offline bundle as a Software Depot:


	PowerCLI C:\> Add-EsxSoftwareDepot C:\Users\Administrator\Desktop\isos\igb-3.1.17-455019\igb-3.1.17-offline_bundle-455019.zip

	Depot Url
	---------
	zip:C:\Users\Administrator\Desktop\isos\igb-3.1.17-455019\igb-3.1.17-offline...

	PowerCLI C:\> Get-EsxSoftwarePackage -Name "*igb*"

	Name Version Vendor Release Date
	---- ------- ------ ------------
	net-igb 2.1.11.1-3vmw.500.0.0.469512 VMware 8/19/2011...
	net-igb 3.1.17-1OEM.500.0.0.406165 Intel 7/1/2011 ...

We can see our VIB is the one with the Vendor as "Intel". We had already cloned our 5.0U1 offline bundle, so let's check out what version of net-igb is in there:

	PowerCLI C:\> Get-EsxImageProfile

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	ESXi-5.0.0-20120301001s-no-... VMware, Inc. 2/17/2012 11... PartnerSupported
	My_Cloned_Profile VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120302001-no-t... VMware, Inc. 2/17/2012 11... PartnerSupported
	ESXi-5.0.0-20120301001s-sta... VMware, Inc. 2/17/2012 11... PartnerSupported
	My_Manual_Profile VMware 12/25/2012 1... VMwareCertified
	ESXi-5.0.0-20120302001-stan... VMware, Inc. 2/17/2012 11... PartnerSupported

	PowerCLI C:\> Get-EsxImageProfile My_Cloned_Profile | Select -ExpandProperty VibList | findstr igb
	net-igb 2.1.11.1-3vmw.500.0.0.469512 VMware 8/19/2011...

So it looks like our cloned profile has an older version of the driver. So let's remove the old version and add the new async driver:

	PowerCLI C:\> Remove-EsxSoftwarePackage -ImageProfile My_Cloned_Profile -SoftwarePackage net-igb

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Cloned_Profile VMware, Inc. 12/25/2012 4... PartnerSupported

Since the name of the driver is the same we will need to include the version number as well:

	PowerCLI C:\> Get-EsxSoftwarePackage -Name "*igb*"

	Name Version Vendor Release Date
	---- ------- ------ ------------
	net-igb 2.1.11.1-3vmw.500.0.0.469512 VMware 8/19/2011...
	net-igb 3.1.17-1OEM.500.0.0.406165 Intel 7/1/2011 ...

	PowerCLI C:\> Add-EsxSoftwarePackage -ImageProfile My_Cloned_Profile -SoftwarePackage "net-igb 3.1.*"

	Name Vendor Last Modified Acceptance Level
	---- ------ ------------- ----------------
	My_Cloned_Profile VMware, Inc. 12/25/2012 4... PartnerSupported

	PowerCLI C:\> Get-EsxImageProfile My_Cloned_Profile | Select -ExpandProperty VibList | findstr igb
	net-igb 3.1.17-1OEM.500.0.0.406165 Intel 7/1/2011 ...

And now we can see the new driver included in the profile. You can now export this profile as an offline bundle or an iso. Instructions for that were presented above.

In the same KB it talks about using *esxcli* to install the driver. From the KB:

> **ESXi installation using esxcli and offline bundle async driver zip file**
>
> **To install the async drivers:**
>
> 1.  Extract the contents of the async driver zip file.
> 2.  Identify the offline-bundle.zip file(s).
> 3.  Log into the ESXi host using the vSphere Client with administrator privileges, such as root.
> 4.  Using the Datastore Browser, upload the offline-bundle.zip file(s) to an ESXi host's datastore.
> 5.  Enter the host into maintenance mode.
> 6.  Log in as root to the ESXi console through SSH or iLO/DRAC.
> 7.  Run this command to install drivers using the offline bundle (this requires an absolute path):
>
>		esxcli software vib install –d /path/offline-bundle.zip
>
>     For example:
>
>		esxcli software vib install –d /vmfs/volumes/datastore/offline-bundle.zip
>
> 8.  Reboot the ESXi host.
> 9.  Exit maintenance mode.

So let's say I uploaded the same driver to my datastore:

	~ # ls -l /vmfs/volumes/OI_LUN0/
	drwxr-xr-x 1 root root 2800 Oct 16 00:38 IOAnalyzer1.1
	-rw------- 1 root root 444806 Jul 5 23:45 igb-3.1.17-455019.zip

Now checking out the currently installed version of igb, I see the following:


	~ # esxcli software vib list | grep igb
	net-igb 2.1.11.1-3vmw.500.1.16.721882 VMware VMwareCertified 2012-07-05

So we have the 2.1.11 version installed and we are going to install the 3.1.17 version. First let's create a directory to store our driver files and then extract the contents:

	~ # cd /vmfs/volumes/OI_LUN0/
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e # mkdir driver
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e # mv igb-3.1.17-455019.zip driver/
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e # cd driver/
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e/driver # unzip igb-3.1.17-455019.zip
	Archive: igb-3.1.17-455019.zip
	inflating: igb-3.1.17-offline_bundle-455019.zip
	inflating: net-igb-3.1.17-1OEM.500.0.0.406165.x86_64.vib
	inflating: doc/README.txt
	inflating: source/driver_source_net-igb_3.1.17-1OEM.500.0.0.406165.tgz
	inflating: doc/open_source_licenses_net-igb_3.1.17-1OEM.500.0.0.406165.txt
	inflating: doc/release_note_net-igb_3.1.17-1OEM.500.0.0.406165.txt
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e/driver # ls
	doc net-igb-3.1.17-1OEM.500.0.0.406165.x86_64.vib
	igb-3.1.17-455019.zip source
	igb-3.1.17-offline_bundle-455019.zip

So now we see our offline-bundle. Let's go ahead and install that:

	~ # esxcli software vib install -d /vmfs/volumes/OI_LUN0/driver/igb-3.1.17-offline_bundle-455019.zip
	Installation Result
	Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
	Reboot Required: true
	VIBs Installed: Intel_bootbank_net-igb_3.1.17-1OEM.500.0.0.406165
	VIBs Removed: VMware_bootbank_net-igb_2.1.11.1-3vmw.500.1.16.721882
	VIBs Skipped:

We can see that it removed the old VIB in the process. Here is how the installed VIB list looked like after the reboot of the ESXi host:

	~ # esxcli software vib list | grep igb
	net-igb 3.1.17-1OEM.500.0.0.406165 Intel VMwareCertified 2012-12-25

### Configure advanced boot loader options

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf)":

> **Enter Boot Options to Start an Installation or Upgrade Script**
> You can start an installation or upgrade script by typing boot command-line options at the boot command line.
>
> At boot time you might need to specify options to access the kickstart file. You can enter boot options by pressing **Shift+O** in the boot loader.
>
> A **ks=... option** must be given, to specify the location of the installation script. Otherwise, a scripted installation or upgrade will not start. If **ks=...** is omitted, the text installer will proceed.
>
> **Procedure**
>
> 1.  Start the host.
> 2.  When the ESXi installer window appears, press Shift+O to edit boot options.
>     ![esxi boot screen VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/esxi_boot_screen.png)
> 3.  At the runweasel command prompt, type
>
>     	ks=location of installation script plus boot command line options
>
> **Example: Boot Option**
>
> You type the following boot options:
>
>	ks=http://00.00.00.00/kickstart/ks-osdc-pdp101.cfg nameserver=00.00.0.0 ip=00.00.00.000 netmask=255.255.255.0 gateway=00.00.00.000
>

Here is a list of all the supported boot options:

> **Boot Options**
> When you perform a scripted installation, you might need to specify options at boot time to access the kickstart file.
> **Supported Boot Options**
> ![boot options esxi VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/boot_options_esxi.png)

### Configure kernel options

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf)":

> **About the boot.cfg File**
> The boot loader configuration file boot.cfg specifies the kernel, the kernel options, and the boot modules that the mboot.c32 boot loader uses in an ESXi installation.
>
> The boot.cfg file is provided in the ESXi installer. You can modify the kernelopt line of the boot.cfg file to specify the location of an installation script or to pass other boot options.
>
> The boot.cfg file has the following syntax:
>
> 	# boot.cfg -- mboot configuration file
> 	#
> 	# Any line preceded with '#' is a comment.
> 	title=STRING
> 	kernel=FILEPATH
> 	kernelopt=STRING
> 	modules=FILEPATH1 --- FILEPATH2... --- FILEPATHn
> 	# Any other line must remain unchanged.
>
> The commands in boot.cfg configure the boot loader.
>
> ![boot cfg options VCAP5 DCA Objective 9.1 – Install ESXi hosts with custom settings ](https://github.com/elatov/uploads/raw/master/2012/12/boot_cfg_options.png)

### Given a scenario, determine when to customize a configuration

This was discussed in "[VCAP5-DCD Objective 3.6](/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/)"
