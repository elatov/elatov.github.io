---
title: VCAP5-DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/
dsq_thread_id:
  - 1408719630
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify Auto Deploy requirements

From "<a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy</a>":

> **Auto Deploy Requirements**  
> The following components are required for Auto Deploy:
> 
> *   PXE boot infrastructure (DHCP/TFTP)
> *   VMware vSphere PowerCLI 5.0
> *   ESXi installation image (from Image Builder CLI)
> *   vCenter Server 5.0

### Install the Auto Deploy Server

From "<a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy</a>":

> The Auto Deploy Windows Installer is included with the vCenter installation media. From the main installation menu, choose the option to install the Auto Deploy server.
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_installer/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_installer/']);" rel="attachment wp-att-5651"><img class="alignnone size-full wp-image-5651" alt="auto deploy installer VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/auto_deploy_installer.png" width="605" height="442" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>
> 
> During the installation, you will be prompted to provide the login credentials for your vCenter server. This is required in order to allow the installer to register the Auto Deploy server and enable the plug-in.
> 
> **Verify the Auto Deploy Server Installation**  
> After you have installed the Auto Deploy server, or deployed the VCSA, log in to your vSphere Client and verify that the Auto Deploy plug-in is successfully registered by selecting **Plug-ins -> Manage Plug-ins…** from the menu bar. Verify that the Auto Deploy plug-in is listed and is enabled.
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/plug_in_manager_auto_deploy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/plug_in_manager_auto_deploy/']);" rel="attachment wp-att-5652"><img class="alignnone size-full wp-image-5652" alt="plug in manager auto deploy VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/plug_in_manager_auto_deploy.png" width="725" height="250" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>

Also here are the other prerequisites:

> **Set Up the PXE Boot Infrastructure **  
> Auto Deploy uses a PXE to network boot ESXi hosts. The PXE requires a DHCP and TFTP server.  
> **TFTP Server**  
> Auto Deploy can utilize any standard TFTP infrastructure. You will need to copy the Auto Deploy gPXE boot files from your vCenter server into the TFTP home directory (the steps to do this are discussed later). The following example shows the contents of the TFTP home directory on a Linux server that has been configured for Auto Deploy:
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/tftp_contents_for_auto_deploy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/tftp_contents_for_auto_deploy/']);" rel="attachment wp-att-5653"><img class="alignnone size-full wp-image-5653" alt="tftp contents for auto deploy VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/tftp_contents_for_auto_deploy.png" width="637" height="180" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>
> 
> **DHCP Server**  
> Any DHCP server can be used. Ensure that the DHCP server is configured both to provide an IP address and to update the DNS, to include setting up reverse pointer records. It is recommended that you use static IP reservations for Auto Deploy hosts, because this will facilitate IP address tracking and troubleshooting. Within the DHCP configuration, you must set the Boot Server (DHCP option 66) to the IP address of your TFTP server and the Bootfile Name (DHCP option 67) to the file name of the gPXE boot file – undionly.kpxe.vmw-hardwired (this file is included in the files copied from the vCenter to the TFTP server).
> 
> The following example shows the DHCP settings for a windows DHCP server (version 5.2):
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/dhcp_for_auto_deploy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/dhcp_for_auto_deploy/']);" rel="attachment wp-att-5654"><img class="alignnone size-full wp-image-5654" alt="dhcp for auto deploy VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dhcp_for_auto_deploy.png" width="635" height="210" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>

### Utilize Auto Deploy cmdlets to deploy ESXi hosts

From "<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf']);">vSphere Installation and Setup vSphere 5.0</a>":

> Auto Deploy PowerCLI Cmdlet Overview  
> You specify the rules that assign image profiles and host profiles to hosts using a set of PowerCLI cmdlets that are included in VMware PowerCLI.
> 
> You can get help for any command at the PowerShell prompt.
> 
> *   Basic help: Get-Help cmdlet_name
> *   Detailed help: Get-Help cmdlet_name -Detailed
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_powercli_cmdlets/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_powercli_cmdlets/']);" rel="attachment wp-att-5655"><img class="alignnone size-full wp-image-5655" alt="auto deploy powercli cmdlets VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/auto_deploy_powercli_cmdlets.png" width="590" height="760" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>

### Configure Bulk Licensing

> **Set Up Bulk Licensing**  
> You can use the vSphere Client or ESXi Shell to specify individual license keys, or you can set up bulk licensing by using PowerCLI cmdlets. Bulk licensing works for all ESXi hosts, but is especially useful for hosts provisioned with Auto Deploy.
> 
> The following example assigns licenses to all hosts in a data center. You can also associate licenses with hosts and clusters.  
> The following example is for advanced PowerCLI users who know how to use PowerShell variables.
> 
> **Procedure**
> 
> 1.  Connect to the vCenter Server system you want to use and bind the associated license manager to avariable.  
	>       
	>     Connect-VIServer -Server 192.XXX.X.XX -User username -Password password  
	>     $licenseDataManager = Get-LicenseDataManager  
	>     
> 2.  Run a cmdlet that retrieves the datacenter in which the hosts for which you want to use the bulk licensing feature are located.  
	>       
	>     $hostContainer = Get-Datacenter -Name Datacenter-X  
	>     </p> 
>     You can also run a cmdlet that retrieves a cluster to use bulk licensing for all hosts in a cluster, or retrieves a folder to use bulk licensing for all hosts in a folder.</li> 
>     *   Create a new LicenseData object and a LicenseKeyEntry object with associated type ID and license key.  
	>           
	>         $licenseData = New-Object VMware.VimAutomation.License.Types.LicenseData  
	>         $licenseKeyEntry = New-Object Vmware.VimAutomation.License.Types.LicenseKeyEntry  
	>         $licenseKeyEntry.TypeId = "vmware-vsphere”  
	>         $licenseKeyEntry.LicenseKey = "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"  
	>         
>     *   Associate the LicenseKeys attribute of the LicenseData object you created in step 3 with the LicenseKeyEntry object.  
	>           
	>         $licenseData.LicenseKeys += $licenseKeyEntry  
	>         
>     *   Update the license data for the data center with the LicenseData object and verify that the license is associated with the host container.  
	>           
	>         $licenseDataManager.UpdateAssociatedLicenseData($hostContainer.Uid, $licenseData)  
	>         $licenseDataManager.QueryAssociatedLicenseData($hostContainer.Uid)  
	>         
>     *   Provision one or more hosts with Auto Deploy and assign them to the data center or cluster that you assigned the license data to.
>     *   Verify that the host is successfully assigned to the default license XXXXX-XXXXX-XXXXX-XXXXX-XXXXX. 
>         *   Using a vSphere Client, log in to the vCenter Server system.
>         *   Navigate to the Configuration > License Features tab for the host and check that the correct license is displayed
>         
>         .</li> </ol> 
>         All hosts that you assigned to the data center are now licensed automatically</blockquote> 
>         
>         ### Provision/Re-provision ESXi hosts using Auto Deploy
>         
>         From "<a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy</a>":
>         
>         > Create Auto Deploy Rules  
>         > From the vSphere PowerCLI shell you will create the rules to identify the image profile and host profile to use and where in vCenter to place the auto deployed host. The rules use pattern matching to compare the attributes of the host being deployed against the predefined rules. There are a number of attributes that can be used. The following figure shows the list of available attributes that can be used for pattern matching in Auto Deploy.
>         > 
>         > <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_attributes/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/auto_deploy_attributes/']);" rel="attachment wp-att-5657"><img class="alignnone size-full wp-image-5657" alt="auto deploy attributes VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/auto_deploy_attributes.png" width="612" height="241" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>
>         > 
>         > At a minimum, each host needs at least one rule to identify the image profile to install. Additional rules can then be created to optionally apply host profiles and place the host in vCenter.
>         > 
>         > **Create an Image Profile Rule**  
>         > Use the following steps to create an image profile rule. Prior to creating an image profile rule, you must have first created an image profile using vSphere 5.0 Image Builder CLI
>         > 
>         > Start by listing the available image profiles as follows:
>         > 
	>         >   
	>         > PowerCLI C:\> Get-EsxImageProfile
	>         > 
	>         > Name Vendor Last Modified Acceptance Level  
	>         > \---\- --\---\- --\---\---\---\-- -\---\---\---\---\---  
	>         > ESXi-5.0.0-20120301001s-no-... VMware, Inc. 2/17/2012 11... PartnerSupported  
	>         > My_Cloned_Profile VMware, Inc. 12/25/2012 1... PartnerSupported  
	>         > ESXi-5.0.0-20120302001-no-t... VMware, Inc. 2/17/2012 11... PartnerSupported  
	>         > ESXi-5.0.0-20120301001s-sta... VMware, Inc. 2/17/2012 11... PartnerSupported  
	>         > My_Manual_Profile VMware 12/25/2012 1... VMwareCertified  
	>         > ESXi-5.0.0-20120302001-stan... VMware, Inc. 2/17/2012 11... PartnerSupported  
	>         > 
>         > 
>         > Next, identify the IP subnet for the hosts that will be deployed using Auto Deploy. In this example, all the ESXi hosts are on the 10.91.243.0 subnet.  
>         > With the image profile and IP subnet, we can create an Auto Deploy rule to assign the image profile My_Cloned_Profile to any hosts that boot on the 10.91.243.0 IP subnet.
>         > 
	>         >   
	>         > PowerCLI C:\> New-DeployRule -Name AssignImageRule1 -Item My_Manual_Profile -Pattern "ipv4=10.91.243.1-10.91.243.254"
	>         > 
	>         > Name : AssignImageRule1  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {My_Manual_Profile}  
	>         > 
>         > 
>         > After Auto Deploy rules are created, they must be activated. This is done by moving the rule into the active rule set with the Add-DeployRule cmdlet.
>         > 
	>         >   
	>         > PowerCLI C:\> Add-DeployRule AssignImageRule1
	>         > 
	>         > Name : AssignImageRule1  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {My_Manual_Profile}  
	>         > 
>         
>         Now we can create another rule to put all the hosts into a specific cluster. From the same guide:
>         
>         > **Create a vCenter Folder/Cluster Rule**  
>         > As mentioned earlier, Auto Deploy can optionally place the ESXi host into a vCenter folder or cluster. Follow these steps to create a rule to place a host in a vCenter cluster:
>         > 
>         > List the available vCenter clusters using the Get-Cluster cmdlet, as follows:
>         > 
	>         >   
	>         > PowerCLI C:\> get-Cluster
	>         > 
	>         > Name HAEnabled HAFailover DrsEnabled DrsAutomationLe  
	>         > Level vel  
	>         > \---\- --\---\---\- --\---\---\-- -\---\---\--- \---\---\---\---\---  
	>         > vsphere4 False 1 False FullyAutomated  
	>         > vsphere5 False 1 False FullyAutomated  
	>         > 
>         > 
>         > Create an Auto Deploy rule to provision new hosts on the subnet 10.91.243.0 into the cluster vsphere5.
>         > 
	>         >   
	>         > PowerCLI C:\> New-DeployRule -Name AssignClusterRule -Item vsphere5 -Pattern "ip  
	>         > v4=10.91.243.1-10.91.243.254"
	>         > 
	>         > Name : AssignClusterRule  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {vsphere5}  
	>         > 
>         > 
>         > Next, we activate the rule by moving it into the active rule set.
>         > 
	>         >   
	>         > PowerCLI C:\> Add-DeployRule AssignClusterRule
	>         > 
	>         > Name : AssignImageRule1  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {My_Manual_Profile}
	>         > 
	>         > Name : AssignClusterRule  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {vsphere5}  
	>         > 
>         
>         Now we are ready to provision/deploy a host:
>         
>         > Deploy a Host Using Auto Deploy  
>         > With the PXE environment in place, Image Builder CLI installed and image profiles created, the Auto Deploy server installed, and the rules created, you are ready to provision hosts using Auto Deploy.
>         > 
>         > PXE boot the host by powering it on. On boot, the host will contact the DHCP server and get assigned an IP address. The DHCP server will also provide the host with the IP address of the TFTP server and the name of the gPXE boot file. The gPXE boot file will provide the host with the information necessary to initiate an HTTP boot from the Auto Deploy server.
>         > 
>         > <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/pxe_boot_auto_deploy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/pxe_boot_auto_deploy/']);" rel="attachment wp-att-5658"><img class="alignnone size-full wp-image-5658" alt="pxe boot auto deploy VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/pxe_boot_auto_deploy.png" width="606" height="359" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>
>         > 
>         > Once this is complete, the server compares the host information against the rules in the active rule set to determine which image profile to install on the host, which host profile to use to configure the host, and where in vCenter to place the host after it is installed.
>         > 
>         > <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/booting_from_autodeploy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-9-2-install-esxi-hosts-using-auto-deploy/booting_from_autodeploy/']);" rel="attachment wp-att-5659"><img class="alignnone size-full wp-image-5659" alt="booting from autodeploy VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/booting_from_autodeploy.png" width="611" height="424" title="VCAP5 DCA Objective 9.2 – Install ESXi Hosts Using Auto Deploy " /></a>
>         > 
>         > The chosen image profile is then copied over the network, where it is loaded directly into the host’s memory.
>         
>         ### Configure an Auto Deploy reference host
>         
>         From <a href="http://virtuallyhyper.com/2012/11/vcap5-dca-objective-5-1-implement-and-maintain-host-profiles/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/vcap5-dca-objective-5-1-implement-and-maintain-host-profiles/']);">VCAP5-DCA Objective 5.1</a> create a Host Profile and then we can apply it to Auto Deployed Hosts. From "<a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy</a>":
>         
>         > **Create a Host Profile Rule**  
>         > By default, when a new host is provisioned using Auto Deploy, the host will be put into maintenance mode. This requires that the administrator connect to the vCenter to finish the host’s configuration. Auto Deploy can optionally perform the host configuration by applying a predefined host profile. Follow these steps to create a rule to apply a host profile to a newly deployed host.
>         > 
>         > List the host profiles defined on the vCenter server as follows:
>         > 
	>         >   
	>         > PowerCLI C:\> Get-VMHostProfile
	>         > 
	>         > Name Description ReferenceHostId  
	>         > \---\- --\---\---\--- \---\---\---\---\---  
	>         > 5.0_Profile HostSystem-hos...  
	>         > 
>         > 
>         > Create an Auto Deploy rule to apply the host profile 5.0_Profile to hosts provisioned on the 10.91.243.0 subnet as follows:
>         > 
	>         >   
	>         > PowerCLI C:\> New-DeployRule -Name AssignHPRule -Item 5.0_Profile -Pattern "ipv4  
	>         > =10.91.243.1-10.91.243.254"
	>         > 
	>         > Name : AssignHPRule  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {5.0_Profile}  
	>         > 
>         > 
>         > Activate the rule by moving it into the active rule set.
>         > 
	>         >   
	>         > PowerCLI C:\> Add-DeployRule AssignHPRule
	>         > 
	>         > Name : AssignImageRule1  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {My_Manual_Profile}
	>         > 
	>         > Name : AssignClusterRule  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {vsphere5}
	>         > 
	>         > Name : AssignHPRule  
	>         > PatternList : {ipv4=10.91.243.1-10.91.243.254}  
	>         > ItemList : {5.0_Profile}  
	>         > 
>         > 
>         > At this point, we have created the following three Auto Deploy rules:
>         > 
>         > *   **AssignImageRule** assigns the ESXi image profile My_Manual_Profile to hosts in the 10.91.243.0 subnet.
>         > *   **AssignClusterRule** places hosts in the 10.91.243.0 subnet into the vsphere5 cluster.
>         > *   **AssignHostProfileRule** applies the host profile 5.0_Profile to hosts in the 10.91.243.0 subnet.
>         
