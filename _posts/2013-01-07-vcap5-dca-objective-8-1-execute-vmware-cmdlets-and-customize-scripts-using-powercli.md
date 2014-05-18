---
title: VCAP5-DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/
dsq_thread_id:
  - 1404673550
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify vSphere PowerCLI requirements

From "[vSphere PowerCLI User’s Guide PowerCLI 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsp_powercli_50_usg.pdf)":

> **PowerCLI Installation Prerequisites**
> To install vSphere PowerCLI, you must have installed the following software
>
> *   .NET 2.0 SP1
> *   Windows PowerShell 1.0/2.0
>
> **Supported Operating Systems**
> VMware vSphere PowerCLI 5.0 is supported on the 32-bit and 64-bit versions of the following Windows operating systems:
>
> *   Windows 7
> *   Windows Server 2008
> *   Windows Vista
> *   Windows XP Service Pack 2
> *   Windows 2003 Server Service Pack 2

### Identify Cmdlet concepts

> **Microsoft PowerShell Basics**
> Microsoft PowerShell is both a command-line and scripting environment, designed for Windows. It leverages the .NET object model and provides administrators with management and automation capabilities. Working with PowerShell, like with any other console environment, is done by typing commands. In PowerShell commands are called cmdlets, which term we will use throughout this guide. vSphere PowerCLI is based on Microsoft PowerShell and uses the PowerShell basic syntax and concepts.
>
> **PowerShell Command-Line Syntax**
> PowerShell cmdlets use a consistent verb-noun structure, where the verb specifies the action and the noun specifies the object to operate on. PowerShell cmdlets follow consistent naming patterns, which makes it easy to figure out how to construct a command if you know the object you want to work with. All command categories take parameters and arguments. A parameter starts with a hyphen and is used to control the behavior of the command. An argument is a data value consumed by the command. A simple PowerShell command has the following syntax:
>
>
>	 command -parameter1 -parameter2 argument1 -argument2
>

### Identify environment variables usage

From the help page:

> about_Environment_Variables
>
> SHORT DESCRIPTION
> Describes how to access Windows environment variables in Windows
> PowerShell.
>
> LONG DESCRIPTION
> Environment variables store information about the operating system
> environment. This information includes details such as the operating
> system path, the number of processors used by the operating system,
> and the location of temporary folders.

Here are some examples.


	# show all environment variables
	get-item -path env:*
	# set $var equal to the $path environment
	$var = $env:path
	# list pwd
	get-item .
	# list all files in current working directory
	get-item *


### Install and configure vSphere PowerCLI

Download the package from My VMware:

[<img class="alignnone size-full wp-image-5534" alt="my vmware powercli VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/my_vmware_powercli.png" width="1005" height="538" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/my_vmware_powercli/" rel="attachment wp-att-5534)

Once downloaded you will see the following in your downloads folder:

[<img class="alignnone size-full wp-image-5535" alt="powercli install package VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/powercli_install_package.png" width="127" height="107" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/powercli_install_package/" rel="attachment wp-att-5535)

Double Click on the install executable and follow the on-screen instructions:

[<img class="alignnone size-full wp-image-5537" alt="powercli install screen VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/powercli_install_screen.png" width="502" height="376" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/powercli_install_screen/" rel="attachment wp-att-5537)

After the install is finished, you will see the following on your Desktop:

[<img class="alignnone size-full wp-image-5538" alt="powercli icon VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/powercli_icon.png" width="121" height="121" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/powercli_icon/" rel="attachment wp-att-5538)

Double Clicking on the "PowerCLi" Icon will start PowerCLI:

[<img class="alignnone size-full wp-image-5539" alt="powercli started VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/powercli_started.png" width="665" height="326" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/powercli_started/" rel="attachment wp-att-5539)

Notice that I also enabled 'remotesigned' execution of scripts.

From "[vSphere PowerCLI User’s Guide PowerCLI 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsp_powercli_50_usg.pdf)":

> **Setting the Properties to Support Remote Signing**
> For security reasons, Windows PowerShell supports an execution policy feature. It determines whether scripts are allowed to run and whether they must be digitally signed. By default, the execution policy is set to Restricted, which is the most secure policy. If you want to run scripts or load configuration files, you can change the execution policy by using the Set-ExecutionPolicy cmdlet.
>
> **To set the PowerShell execution policy**
>
> 1. Choose Start > Programs > VMware > VMware vSphere PowerCLI> VMware vSphere PowerCLI. The vSphere PowerCLI console window opens.
> 2. In the vSphere PowerCLI console window, type:
>
>	     Set-ExecutionPolicy RemoteSigned
>

After enabling the appropriate Execution policy, the powercli console will look like this when started:

[<img class="alignnone size-full wp-image-5541" alt="powercli without issues VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/powercli_without_issues.png" width="663" height="325" title="VCAP5 DCA Objective 8.1 – Execute VMware Cmdlets and Customize Scripts Using PowerCLI " />](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-1-execute-vmware-cmdlets-and-customize-scripts-using-powercli/powercli_without_issues/" rel="attachment wp-att-5541)

### Install and configure Update Manager PowerShell Library

From "[VMware vSphere Update Manager PowerCLI Installation and Administration Guide PowerCLI 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-update-manager-powercli-50-inst-admg.pdf)":

> **Install Update Manager PowerCLI**
> You can download the Update Manager PowerCLI installer package from the product landing page at https://www.vmware.com/support/developer/ps-libs/vumps/.
>
> **To install the Update Manager PowerCLI**
>
> 1.  Start the Update Manager PowerCLI installer.
> 2.  Click Next in the Welcome page to continue with the installation.
> 3.  Read and accept the license agreement terms.
> 4.  Click Install.
> 5.  Click Finish to complete the installation process.

From the same document:

> **Getting Started with Update Manager PowerCLI**
> To get started with Update Manager PowerCLI, open the vSphere PowerCLI console from the Windows Start menu or by clicking the vSphere PowerCLI shortcut icon.
> You can get a list of all Update Manager PowerCLI cmdlets by running the Get-Command command with the -PSSnapin parameter:
>
>
>	 Get-Command -PSSnapin VMware.VumAutomation
>

### Use basic and advanced Cmdlets to manage VMs and ESXi Hosts

> **Basic Cmdlets Usage**
> This section provides some examples of basic vSphere PowerCLI cmdlets usage.
>
> **Display Help for a Cmdlet**
> You can get help for a specific cmdlet by supplying the Get-Help command in the vSphere PowerCLI console.
> To get information on a cmdlet
>
> 1.  Run the Get-Help cmdlet with the specific cmdlet name:
>
>	     Get-Help Add-VMHost
>
> 2.  (opt) Retrieve more detailed information by using the -full parameter:
>
>	     Get-Help Add-VMHost -full
>
>
> **Connect to a Server**
> In vSphere PowerCLI, you can have more than one connections to the same server. To disconnect from a server, you must close all active connections to this server running the Disconnect-VIServer cmdlet.
> **To connect to a local server**
>
> 1.  Run the Connect-VIServer cmdlet with the server name:
>
>	     Connect-VIServer -Server esx3.example.com
>
>
> The cmdlet prompts for user credentials, as they are not passed as parameters.

Here is how that looks like from PowerCLI:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Connect-VIServer 192.168.0.103
	WARNING: There were one or more problems with the server certificate:

	* The X509 chain could not be built up to the root certificate.

	* The certificate's CN name does not match the passed value.

	Name Port User
	---- ---- ----
	192.168.0.103 443 root


More examples from the same document:

> **Basic Virtual Machine Operations**
> The following scenario shows how to retrieve information of available virtual machines and their operation system. It also demonstrates how to shut down a virtual machine guest operating system and to power off the virtual machine using vSphere PowerCLI cmdlets.
>
> **To manage virtual machines**
>
> 1.  After establishing a connection to a server, list all virtual machines on the target system:
>
>	     Get-VM
>
> 2.  Save the name and the power state properties of the virtual machines in the ResourcePool resource pool into a file named myVMProperties.txt:
>
>	     $respool = Get-ResourcePool ResourcePool
>	     Get-VM -Location $respool | Select-Object Name, PowerState > myVMProperties.txt
>
> 3.  Start the VM virtual machine:
>
>	     Get-VM VM | Start-VM
>
> 4.  Retrieve information of the guest OS of the VM virtual machine:
>
>	     Get-VMGuest VM | fc
>
> 5.  Shutdown the OS of the VM virtual machine:
>
>	     Shutdown-VMGuest VM
>
> 6.  Power off the VM virtual machine:
>
>	     Stop-VM VM
>
> 7.  Move the virtual machine VM from the Host01 host to the Host02 host:
>
>	     Get-VM -Name VM -Location Host01 | Move-VM –Destination Host02
>

Here is how that looks like from PowerCLI:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> get-vm

	Name PowerState Num CPUs Memory (MB)
	---- ---------- -------- -----------
	test PoweredOff 1 4096

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Get-HardDisk test

	CapacityKB Persistence Filename
	---------- ----------- --------
	5242880 Persistent  test/test.vmdk


Here are more examples from the guide:

> **Basic Host Operations**
> The following examples illustrate some basic operations with hosts, like adding a host to a vCenter Server, putting a host into maintenance mode, shutting down, and removing a host from the vCenter Server.
>
> **To add a standalone host to the vCenter Server**
>
> 1.  List all hosts on the target VMware vSphere server that you have established a connection with:
>
>	     Get-VMHost
>
> 2.  Add the Host standalone host:
>
>	     Add-VMHost -Name Host -Location (Get-Datacenter DC) -User root -Password pass
>
>
> **To activate maintenance mode for a host**
>
> 1.  Save the Host host object as a variable:
>
>	     $host = Get-VMHost -Name Host
>
> 2.  Retrieve the cluster to which Host belongs and save the cluster object as a variable:
>
>	     $hostCluster = Get-Cluster -VMHost $host
>
> 3.  Initialize a task that activates maintenance mode for the Host host and save the task object as a variable:
>
>	     $updateHostTask = Set-VMHost -VMHost $host -State "Maintenance" -RunAsync
>
> 4.  Retrieve and apply the recommendations generated by DRS:
>
>	     Get-DrsRecommendation -Cluster $hostCluster | where {$_.Reason -eq "Host is entering maintenance mode"} | Apply-DrsRecommendation
>
> 5.  Retrieve the task output object and save it as a variable:
>
>	     $myUpdatedHost = Wait-Task $updateHostTask
>

Here is how it looks like from PowerCLI:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Get-VMHost | fl

	State : Connected
	ConnectionState : Connected
	PowerState : PoweredOn
	VMSwapfileDatastoreId :
	VMSwapfilePolicy : InHostDatastore
	ParentId : Folder-ha-folder-host
	IsStandalone : True
	Manufacturer : VMware, Inc.
	Model : VMware Virtual Platform
	NumCpu : 2
	CpuTotalMhz : 4792
	CpuUsageMhz : 1632
	MemoryTotalMB : 4095
	MemoryUsageMB : 975
	ProcessorType : Intel(R) Xeon(R) CPU E5540 @ 2.53GHz
	HyperthreadingActive : False
	TimeZone : UTC
	Version : 5.0.0
	Build : 623860
	Parent : host
	VMSwapfileDatastore :
	StorageInfo : HostStorageSystem-storageSystem
	NetworkInfo : localhost:
	DiagnosticPartition : mpx.vmhba1:C0:T0:L0
	FirewallDefaultPolicy : VMHostFirewallDefaultPolicy:HostSystem-ha-host
	ApiVersion : 5.0
	Name : 192.168.0.103
	CustomFields : {}
	ExtensionData : VMware.Vim.HostSystem
	Id : HostSystem-ha-host
	Uid : /VIServer=root'@'192.168.0.103:443/VMHost=HostSystem-ha-host/


And more examples from the same guide:

> **Advanced Cmdlets Usage**
> This section contains examples that illustrate how to use advanced functionality provided by the vSphere PowerCLI cmdlets:
>
> **Create vSphere Objects**
> The following scenario illustrates common methods for creating folders, datacenters, clusters, resource pools, and virtual machines by using vSphere PowerCLI cmdlets.
>
> **To create inventory objects**
>
> 1.  Establish a connection to a vCenter Server system:
>
>	     Connect-VIServer -Server 192.168.10.10
>
>     When prompted, provide the administrator's user name and password to authenticate access on the server.
>
> 2. Get the inventory root folder and create a new folder called Folder in it:
>
>		$folder = Get-Folder -NoRecursion | New-Folder -Name Folder
>
> 	Note that the information about the location of the new folder is specified through the pipeline.
>
> 3. Create a new datacenter called DC in the Folder folder:
>
> 		New-Datacenter -Location $folder -Name DC
>
> 4. Create a folder called Folder1 under DC:
>
>         Get-Datacenter DC | New-Folder -Name Folder1
>         $folder1 = Get-Folder -Name Folder1
>
> 5.  Create a new cluster Cluster1 in the Folder1 folder:
>
>		 New-Cluster -Location $folder1 -Name Cluster1 -DrsEnabled -DrsAutomationLevel FullyAutomated
>
> 6.  Add a host in the cluster using the Add-VMHost command, which prompts you for credentials:
>
>		 $host1 = Add-VMHost -Name 10.23.112.345 -Location ( Get-Cluster Cluster1 )
>
>  The parentheses interpolate the object returned by the Get-Cluster command into Location parameter.
>
> 7. Create a resource pool in the cluster's root resource pool:
>
>         $myClusterRootRP = Get-ResourcePool -Location ( Get-Cluster Cluster1 ) -Name Resources New-ResourcePool -Location $clusterRootRP -Name MyRP01 -CpuExpandableReservation $true  -CpuReservationMhz 500 -CpuSharesLevel high -MemExpandableReservation $true -MemReservationMB 500 -MemSharesLevel high
>
> 8. Create a virtual machine synchronously:
>
>		 New-VM -Name VM1 -VMHost $host1 -ResourcePool MyRP01 -DiskMB 4000 -MemoryMB 256
>
> 9. Create a virtual machine asynchronously:
>
>		$vmCreationTask = New-VM -Name VM2 -VMHost $host1 -ResourcePool MyRP01 -DiskMB 4000 -MemoryMB 256 -RunAsync
>
>   The **-RunAsync** parameter specifies that the command runs asynchronously. This means that in contrast to a synchronous operation, you do not have to wait for the process to complete before supplying the next command in the command line.

### Use Web Service Access Cmdlets
From "[vSphere PowerCLI User’s Guide PowerCLI 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsp_powercli_50_usg.pdf)":

> **API Access Cmdlets**
> The vSphere PowerCLI list of cmdlets includes two API Access cmdlets:
>
> *   Get-View
> *   Get-VIObjectByVIView
>
> They enable access to the programming model of the vSphere SDK for .NET from PowerShell and can be used to initiate vSphere .NET objects. Each object:
>
> *   Is a static copy of a server-side managed object and is not automatically updated when the object on the server changes.
> *   Includes properties and methods that correspond to the properties and operations of the server-side managed object.
>
> Using the API Access cmdlets for low-level VMware vSphere management requires some knowledge of both PowerShell scripting and the VMware vSphere API.

Get-View provides a lower level of functionality and is faster to execute the commands. From "[Get-view, list viewtypes, filter usage, Get-VIObjectbyVIView, and get-vm in powercli](http://psvmware.wordpress.com/2012/10/30/powershell-list-view-filter-and-viewtypes)":

> In few words… While installing powercli you receive a set of cmdlets. You can get info about vms,datastores,clusters etc, etc… You can run verb cmdlets like set/new/invoke/move/restart/start/stop... etc. Well you can see it yourself executing ‘get-vicommand’ how many of those there are But in case that’s not enough you can access vsphere objects using views. You will discover that they provide even more options than cmdlets. Some things can’t be done using powercli cmdlets, and they need to be executed using views and their methods.
>
> ...
> ...
>
> I think that the most common mistake in my opinion is to get the view from get-vm. Well i was doing it myself too:
>
> 	$MyVMsViews=get-vm|get-view
>
> So then i could have an array with all views.
> Now this not necessary to pass get-vm objects via pipeline to get-view. It works ok, but get-view can get virtual machines on it’s own.
>
> 	$MyVMsViews=get-view -viewtype virtualmachine
>
> You can ask now how did i know that there was a viewtype like this. For example :
>
> 	get-vm -name testvm
>
>
> takes 1 second and 994 milliseconds, where
>
> 	get-view -viewtype virtualmachine -filter @{‘name’='testvm’}
>
>
> takes 0 second and 455 milliseconds. Those measurements were taken on a small scale infra ~1000 vms.

Here is a quick example:

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Measure-Command {get-vmhost | get-view}

	Days : 0
	Hours : 0
	Minutes : 0
	Seconds : 3 <==
	Milliseconds : 270 <==
	Ticks : 32703600
	TotalDays : 3.78513888888889E-05
	TotalHours : 0.000908433333333333
	TotalMinutes : 0.054506
	TotalSeconds : 3.27036
	TotalMilliseconds : 3270.36

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Measure-Command {Get-View -ViewType HostSystem}

	Days : 0
	Hours : 0
	Minutes : 0
	Seconds : 2 <==
	Milliseconds : 528 <==
	Ticks : 25281556
	TotalDays : 2.92610601851852E-05
	TotalHours : 0.000702265444444444
	TotalMinutes : 0.0421359266666667
	TotalSeconds : 2.5281556
	TotalMilliseconds : 2528.1556


Both produce the following output:

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Get-View -ViewType HostSystem

	Runtime : VMware.Vim.HostRuntimeInfo
	Summary : VMware.Vim.HostListSummary
	Hardware : VMware.Vim.HostHardwareInfo
	Capability : VMware.Vim.HostCapability
	LicensableResource : VMware.Vim.HostLicensableResourceInfo
	ConfigManager : VMware.Vim.HostConfigManager
	Config : VMware.Vim.HostConfigInfo
	Vm : {VirtualMachine-1}
	Datastore : {Datastore-4fc903bb-6298d17d-8417-00505617149e, Datastore-4fc3c05b-c677ee28-ba3c-0050561712cb, Datastore-192.168.1.107:/data/nfs_share}
	Network : {Network-HaNetwork-VM_Net, DistributedVirtualPortgroup-DVPG-ca a4 1a 50 66 29 eb 9b-59 89 a1 2c cd a9 bb 96-dvportgroup-14, DistributedVirtualPortgroup-DVPG-ca a4 1a 50 6 6 29 eb 9b-59 89 a1 2c cd a9 bb 96-dvportgroup-144}
	DatastoreBrowser : HostDatastoreBrowser-ha-host-datastorebrowser
	SystemResources : VMware.Vim.HostSystemResourceInfo
	LinkedView :
	Parent : ComputeResource-ha-compute-res
	CustomValue : {}
	OverallStatus : green
	ConfigStatus : yellow
	ConfigIssue : {5, 6}
	EffectiveRole : {-1}
	Permission : {}
	Name : localhost.localdomain
	DisabledMethod : {DisconnectHost_Task, ReconnectHost_Task, ReconfigureHost, ForDAS_Task, PowerUpHostFromStandBy_Task...}
	RecentTask : {}
	DeclaredAlarmState : {}
	TriggeredAlarmState : {}
	AlarmActionsEnabled : False
	Tag : {}
	Value : {}
	AvailableField : {}
	MoRef : HostSystem-ha-host
	Client : VMware.Vim.VimClient

Also [here](http://communities.vmware.com/thread/263375) is a good example from the VMware communities. From that page:

>	Original script 100.0 %
> 	Get-View 9.7 %
> 	Get-View & Property 3.9 %
>

Here is the original script:

	$outputFileVM = 'D:\PowerShell_scripts\Inventory.csv'
	$VMReport = @()
	get-vm | sort name | %{
	$VM = Get-View $_.ID
	$row = "" | Select-Object VM_Name, VM_Host, VM_Host_Model, VM_Memory, VM_vCpu, VM_CpuLimit, VM_CpuShares
	$row.VM_Name = $VM.Config.Name
	$row.VM_Host = Get-VMHost -VM $_
	$row.VM_Host_Model = Get-VMHost -VM $_ | Get-View | % {$_.Hardware.SystemInfo.Model}
	$row.VM_Memory = $VM.Config.Hardware.memoryMB
	$row.VM_vCpu = $VM.Config.Hardware.numCPU
	$row.VM_CpuLimit = $VM.Config.CpuAllocation.Limit
	$row.VM_CpuShares = $VM.Config.CpuAllocation.Shares.Shares
	$VMReport += $row
	}
	$VMReport | Export-Csv $outputFileVM -NoTypeInformation


Here is the fixed/fast script:


	$outputFileVM = 'D:\PowerShell_scripts\Inventory.csv'
	$VMReport = @()
	Get-View -ViewType VirtualMachine -Property Name,Runtime.Host,Config.Hardware,Config.CpuAllocation | Sort-Object -Property Name | %{
	$row = "" | Select-Object VM_Name, VM_Host, VM_Host_Model, VM_Memory, VM_vCpu, VM_CpuLimit, VM_CpuShares
	$row.VM_Name = $_.Name
	$esx = Get-View $_.Runtime.Host -Property Name,Hardware.SystemInfo.Model
	$row.VM_Host = $esx.Name
	$row.VM_Host_Model = $esx.Hardware.SystemInfo.Model
	$row.VM_Memory = $_.Config.Hardware.memoryMB
	$row.VM_vCpu = $_.Config.Hardware.numCPU
	$row.VM_CpuLimit = $_.Config.CpuAllocation.Limit
	$row.VM_CpuShares = $_.Config.CpuAllocation.Shares.Shares
	$VMReport += $row
	}
	$VMReport | Export-Csv $outputFileVM -NoTypeInformation


### Use Datastore and Inventory Providers

> **The Datastore Provider**
> The Datastore Provider (VimDatastore) is designed to provide access to the contents of one or more datastores. The items in a datastore are files that contain configuration, virtual disk, and the other data associated with a virtual machine.All file operations are case-sensitive.
>
> When you connect to a server with Connect-VIServer, the cmdlet builds two default datastore drives: vmstores and vmstore. The vmstore drive displays the datastores available on the last connected vSphere server. The vmstores drive contains all datastores available on all vSphere servers connected within the current vSphere PowerCLI session.
>
> You can use the default inventory drives or create custom drives based on the default ones.
>
> **Basic functions of the Datastore Provider**
> The following procedures illustrate some basic functions of the Datastore Provider.
>
> **To browse default datastore drives**
>
> 1.  Access the vmstore drive:
>
> 		cd vmstore:
>
> 2.  Access the vmstores drives:
>
> 		cd vmstores:
>
> 3.  List the drive content:
>
> 		dir
>

Here is how it looks like from PowerCLI:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> cd vmstore:
	PowerCLI vmstore:\> dir

	Name Type Id
	---- ---- --
	ha-datacenter Datacenter Datacenter-h...
	PowerCLI vmstore:\> cd ha-datacenter
	PowerCLI vmstore:\ha-datacenter> dir

	Name FreeSpaceMB CapacityMB
	---- ----------- ----------
	OI_LUN0 97732 102144
	datastore1 58657 60416
	nfs 12091 13091

	PowerCLI vmstore:\ha-datacenter> cd OI_LUN0
	PowerCLI vmstore:\ha-datacenter\OI_LUN0> dir

	Datastore path: [OI_LUN0]

	LastWriteTime Type Length Name
	------------- ---- ------ ----
	10/15/2012 6:38 PM Folder IOAnalyzer1.1
	7/5/2012 5:47 PM Folder doc
	7/5/2012 5:47 PM Folder source
	12/16/2012 2:23 PM Folder .vSphere-HA

And here is more from the same guide:

> **To create a new custom datastore drive**
>
> 1.  Get a datastore by its name and assign it to the $datastore variable:
>
> 		$datastore = Get-Datastore Storage1
>
> 2.  Create a new PowerShell drive ds: in $datastore:
>
> 		New-PSDrive -Location $datastore -Name ds -PSProvider VimDatastore -Root '\'
>

Here is how it looks like from PowerCLI:

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> $ds=Get-Datastore OI_LUN0
	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> New-PSDrive -Location $ds -Name ds -PSProvider VimDatastore -Root '\'

	WARNING: column "CurrentLocation" does not fit into the display and was removed.

	Name Used (GB) Free (GB) Provider Root
	---- --------- --------- -------- ----
	ds VimDatastore \192.168.0.103@443\ha-d...

And here is the last section from the guide:

> **To manage datastores through datastore drives**
>
> 1.  Navigate to a specific folder on the ds: drive:
>
> 		cd VirtualMachines\XPVirtualMachine
>
> 2.  List the files of the folder, using the ls command:
>
> 		ls
>
>        **ls** is the UNIX style alias of the Get-ChildItem cmdlet.
>
> 3.  Rename a file, using the Rename-Item cmdlet or its alias ren.
>     For example, to change the name of the vmware-3.log file to vmware-3old.log, run the following command:
>
>     	ren vmware-3.log vmware-3old.log
>
>     All file operations apply only on files in the current folder.
> 4.  Delete a file, using the Remove-Item cmdlet or its alias del.
>     For example, to remove the vmware-3old.log file from the XPVirtualMachine folder, use the following command:
>
>     	del ds:\VirtualMachines\XPVirtualMachine\vmware-2.log
>
> 5.  Copy a file, using the Copy-Item cmdlet or its alias copy:
>
>     	copy ds:\VirtualMachines\XPVirtualMachine\vmware-3old.log ds:\VirtualMachines\vmware-3.log
>
> 6.  Copy a file to another datastore, using the Copy-Item cmdlet or its alias copy:
>
>     	copy ds:\Datacenter01\Datastore01\XPVirtualMachine\vmware-1.log ds:\Datacenter01\Datastore02\XPVirtualMachine02\vmware.log
>
> 7.  Create a new folder, using the New-Item cmdlet or its alias mkdir:
>
>     	mkdir -Path ds:\VirtualMachines -Name Folder01 -Type Folder
>
> 8.  Download a file to the local machine using the Copy-DatastoreItem cmdlet:
>
>     	Copy-DatastoreItem ds:\VirtualMachines\XPVirtualMachine\vmware-3.log C:\Temp\vmware-3.log
>
> 9.  Upload a file from the local machine, using the Copy-DatastoreItem cmdlet:
>
>     	Copy-DatastoreItem C:\Temp\vmware-3.log ds:\VirtualMachines\XPVirtualMachine\vmware-3new.log
>

Here is how it looks like from PowerCLI:

	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> dir ds:

	Datastore path: [OI_LUN0]

	LastWriteTime Type Length Name
	------------- ---- ------ ----
	10/15/2012 6:38 PM Folder IOAnalyzer1.1
	7/5/2012 5:47 PM Folder doc
	7/5/2012 5:47 PM Folder source
	12/16/2012 2:23 PM Folder .vSphere-HA
	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> dir ds:/IOAnalyzer1.1

	Datastore path: [OI_LUN0] IOAnalyzer1.1

	LastWriteTime Type Length Name
	------------- ---- ------ ----
	6/11/2012 6:51 PM VmLogFile 57213 vmware-7.log
	7/5/2012 5:05 PM VmLogFile 113177 vmware-10.log
	7/5/2012 5:05 PM VmLogFile 104886 vmware-9.log
	7/5/2012 4:58 PM VmLogFile 94657 vmware-8.log
	7/14/2012 3:37 PM VmLogFile 93532 vmware-11.log
	7/14/2012 3:31 PM VmNvramFile 8684 IOAnalyzer1.1.nvram
	6/11/2012 6:48 PM VmDiskFile 495 IOAnalyzer1.1_1.vmdk
	7/5/2012 5:03 PM VmDiskFile 527 IOAnalyzer1.1.vmdk
	8/21/2012 11:13 AM VmLogFile 107708 vmware-12.log
	10/25/2012 3:34 PM VmLogFile 52656 vmware.log
	8/21/2012 11:07 AM File 43 IOAnalyzer1.1.vmsd
	8/21/2012 11:08 AM File 13 IOAnalyzer1.1-aux...
	6/11/2012 6:48 PM File 1073741824 IOAnalyzer1.1-129...
	10/25/2012 3:32 PM File 3350 IOAnalyzer1.1.vmx
	10/25/2012 3:32 PM File 268 IOAnalyzer1.1.vmxf
	7/14/2012 3:37 PM File 1 IOAnalyzer1.1-129...
	7/14/2012 3:55 PM File 104857600 IOAnalyzer1.1_1-f...
	12/23/2012 4:32 PM File 2147483648 IOAnalyzer1.1-fla...
	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Copy-DatastoreItem ds:/IOAnalyzer1.1/vmware-7.log c:\vmware-7.log


### Given a sample script, modify the script to perform a given action

Let's say you had the following script to list all the VMs that have snapshots:


	$vcenter = "servername"

	Connect-VIServer $vcenter

	$snapshots = get-vm | get-snapshot

	foreach ($snap in $snapshots) {
	Write-Host "VM: " $snap.VM.Name "Name: " $snap.Name "Size: " $snap.SizeMB
	}


Upon running that, you got the following output:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> C:\Users\Administrator\Desktop\snap.ps1

	Name Port User
	---- ---- ----
	192.168.0.103 443 root
	VM: test Name: ws Size: 0.04


Let't say now you wanted to also print out the date of when the snapshot was created and also save the output in a file. So first let's find out what available members we have from 'get-snapshot':


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> Get-VM | Get-Snapshot | Get-Member

	TypeName: VMware.VimAutomation.ViCore.Impl.V1.VM.SnapshotImpl

	Name MemberType Definition
	---- ---------- ----------
	Equals Method bool Equals(System.Object obj)
	GetHashCode Method int GetHashCode()
	GetType Method type GetType()
	ToString Method string ToString()
	Children Property VMware.VimAutomation.ViCore.Types.V1.VM.Snapsho...
	Created Property System.DateTime Created {get;}
	Description Property System.String Description {get;}
	ExtensionData Property System.Object ExtensionData {get;}
	Id Property System.String Id {get;}
	IsCurrent Property System.Boolean IsCurrent {get;}
	IsReplaySupported Property System.Boolean IsReplaySupported {get;}
	Name Property System.String Name {get;}
	Parent Property VMware.VimAutomation.ViCore.Types.V1.VM.Snapsho...
	ParentSnapshot Property VMware.VimAutomation.ViCore.Types.V1.VM.Snapsho...
	ParentSnapshotId Property System.String ParentSnapshotId {get;}
	PowerState Property VMware.VimAutomation.ViCore.Types.V1.Inventory....
	Quiesced Property System.Boolean Quiesced {get;}
	SizeMB Property System.Double SizeMB {get;}
	Uid Property System.String Uid {get;}
	VM Property VMware.VimAutomation.ViCore.Types.V1.Inventory....
	VMId Property System.String VMId {get;}

So it looks like there is an option called "Created", that is probably what we need. Also there is an 'Out-File' cmdlet in powershell. Here is the information on that:


	PowerCLI C:\Program Files (x86)\VMware\Infrastructure\vSphere PowerCLI> get-help out-file

	NAME
	Out-File

	SYNOPSIS
	Sends output to a file.

	SYNTAX
	Out-File [-FilePath] <string> [[-Encoding] <string>] [-Append] [-Force] [-InputObject <psobject>] [-NoClobber] [-Width <int>] [-Confirm] [-WhatIf] [<CommonParameters>]

	DESCRIPTION
	The Out-File cmdlet sends output to a file. You can use this cmdlet instead
	of the redirection operator (>) when you need to use its parameters.


Putting it all together, we get this:

	$outfile = "c:\info.txt"
	$vcenter = "servername"

	Connect-VIServer $vcenter

	$snapshots = get-vm | get-snapshot

	foreach ($snap in $snapshots) {
	Write-Output "VM: " $snap.VM.Name "Name: " $snap.Name "Size: " $snap.SizeMB "Date Created:" $snap.created | Out-File -FilePath $outfile -Append
	}

Notice I also changed from "Write-Host" to "Write-Output". Do a 'get-help' on that to find out why. Here are the contents of my file after I ran the script:

	C:\>type info.txt
	VM:
	test
	Name:
	ws
	Size:
	0.04
	Date Created:
	Sunday, December 23, 2012 4:55:26 PM
