---
published: true
layout: post
title: "Use Terraform to Deploy a VM in ESXi"
author: Karim Elatov
categories: [vmware,os]
tags: [terraform, powercli]
---
### Terraform
I wanted to try out [teffaform](https://www.terraform.io/intro/index.html). I had a stand alone ESXi host (without vCenter) and so I decided to use **terraform** to create a VM on that ESXi host. I found a bunch of examples:

* [Deploy a VMware vSphere Virtual Machine with Terraform](https://blog.inkubate.io/deploy-a-vmware-vsphere-virtual-machine-with-terraform/)
* [Deploying vSphere VM with Terraform](https://emilwypych.com/2017/02/26/deploying-vsphere-vm-with-terraform/)
* [Terraform and VMWare vSphere: A quick intro](https://insanity.org.uk/2017/10/20/terraform-and-vsphere-a-quick-intro/)
* [A Simple Terraform on vSphere Build](http://blog.codybunch.com/2017/03/08/A-Simple-Terraform-on-vSphere-Build/)

One thing you will notice is that **terraform** can create a VM from a template but it looks like you need to have vCenter for that (discussed here [Is vmware vCenter server necessary for esxi + terraform](https://stackoverflow.com/questions/38796466/is-vmware-vcenter-server-necessary-for-esxi-terraform)). It looks like you can copy a VMDK from the machine you are running **terraform** on ([vsphere_file - error datacenter '' not found](https://github.com/hashicorp/terraform/issues/9253)), but that sounds network intensive. 

Last caveat, it looks like we need to define an empty **resource pool** when using a standalone ESXi host:

* [Create VM ESXi 6.0.0 and 6.5.0 not possible on standalone license!](https://github.com/terraform-providers/terraform-provider-vsphere/issues/268)
* [Create VM fail on ESXi 5.5 standalone](https://github.com/terraform-providers/terraform-provider-vsphere/issues/265)
* [vsphere-resource-pool](https://www.terraform.io/docs/providers/vsphere/d/resource_pool.html#using-with-esxi)

The official documentation on the vSphere **terraform** provider can be found here:

* [VMware vSphere Provider](https://www.terraform.io/docs/providers/vsphere/index.html)
* [vsphere-virtual-machine](https://www.terraform.io/docs/providers/vsphere/r/virtual_machine.html)

So let's just deploy a VM without an OS in ESXi with **terraform**.

### Installing Terraform
I was using a Mac, so running the following took care of the install:

	<> brew install terraform
	<> <> terraform version
	Terraform v0.11.1

#### Installing PowerCLI (Optional)
Initially when I was playing around with the setup, I wanted to figure out what the default datacenter name is on a stand-alone ESXi host. I kept reading that Powershell was ported to Linux, so I decided to give it a shot. On an Ubuntu 16.04 machine, I followed the instructions from these sites:

* [PowerCLI on the mac OS High Sierra?](https://communities.vmware.com/thread/573229) (I needed to get a specific version of the powershell package to use PowerCLI)
* [Package installation instructions](https://github.com/PowerShell/PowerShell/blob/master/docs/installation/linux.md)
* [PowerCLI VMware Fling](https://labs.vmware.com/flings/powercli-core#instructions)

So first let's download the alpha package:

	$ wget https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.18/powershell_6.0.0-alpha.18-1ubuntu1.16.04.1_amd64.deb


Then install the prereqs:

	$ sudo apt install libcurl3 libunwind8
	
And then install the package:

	$ sudo dpkg -i powershell_6.0.0-alpha.18-1ubuntu1.16.04.1_amd64.deb
 
Next let's install PowerCLI, first download the module:

	$ wget https://download3.vmware.com/software/vmw-tools/powerclicore/PowerCLI_Core.zip

Now let's install the module:

	$ mkdir -p ~/.local/share/powershell/Modules
	$ unzip PowerCLI_Core.zip
	$ unzip 'PowerCLI.*.zip' -d ~/.local/share/powershell/Modules

Lastly let's do a test login:

	$ powershell
	PS /home/elatov> Get-Module -ListAvailable PowerCLI* | Import-Module
	PS /home/elatov> Set-PowerCLIConfiguration -InvalidCertificateAction ignore -confirm:$false
	PS /home/elatov> Connect-VIServer -Server 192.168.1.109
	Specify Credential
	Please specify server credential
	User: root
	Password for user root: ********
	
	
	Name                           Port  User
	----                           ----  ----
	192.168.1.109                  443   root

Pretty cool huh :) To get the Datacenter name we can just run the following (after you have logged in):

	PS /home/elatov> Get-Datacenter
	
	Name
	----
	ha-datacenter


### Creating the Terraform Configuration Files
A lot of the basics are covered in:

* [Load Order and Semantics](https://www.terraform.io/docs/configuration/load.html)
  * > Terraform loads all configuration files within the directory specified in alphabetical order.
* [Configuration Syntax](https://www.terraform.io/docs/configuration/syntax.html)
	* > The syntax of Terraform configurations is called HashiCorp Configuration Language (HCL).
* [Interpolation Syntax](https://www.terraform.io/docs/configuration/interpolation.html)
	* > Embedded within strings in Terraform, whether you're using the Terraform syntax or JSON syntax, you can interpolate other values. These interpolations are wrapped in `${}`, such as `${var.foo}`.
* [Data Source Configuration](https://www.terraform.io/docs/configuration/data-sources.html)
  *   > Data sources allow data to be fetched or computed for use elsewhere in Terraform configuration. Use of data sources allows a Terraform configuration to build on information defined outside of Terraform, or defined by another separate Terraform configuration.
*   [Input Variable Configuration](https://www.terraform.io/docs/configuration/variables.html)
	* > For all files which match terraform.tfvars or *.auto.tfvars present in the current directory, Terraform automatically loads them to populate variables.    

So let's create 3 files:

	<> tree test
	test
	├── terraform.tfvars
	├── test.tf
	└── variables.tf
 
*  **terraform.tfvars** contains the credentials for the vsphere login
*  **test.tf** contains most of the infrastructure definition (this is just a single VM in my example, but could be much larger)
*  **variables.tf** contains the variables which can be passed into the **test.tf** file for processing. 

Here is how my files looked like in the end:

	<> cat test/test.tf
	## Configure the vSphere Provider
	provider "vsphere" {
	    vsphere_server = "${var.vsphere_server}"
	    user = "${var.vsphere_user}"
	    password = "${var.vsphere_password}"
	    allow_unverified_ssl = true
	}
	
	## Build VM
	data "vsphere_datacenter" "dc" {
	  name = "ha-datacenter"
	}
	
	data "vsphere_datastore" "datastore" {
	  name          = "datastore1"
	  datacenter_id = "${data.vsphere_datacenter.dc.id}"
	}
	
	data "vsphere_resource_pool" "pool" {}
	
	data "vsphere_network" "mgmt_lan" {
	  name          = "VM_VLAN1"
	  datacenter_id = "${data.vsphere_datacenter.dc.id}"
	}
	
	resource "vsphere_virtual_machine" "test2" {
	  name             = "test2"
	  resource_pool_id = "${data.vsphere_resource_pool.pool.id}"
	  datastore_id     = "${data.vsphere_datastore.datastore.id}"
	
	  num_cpus   = 1
	  memory     = 2048
	  wait_for_guest_net_timeout = 0
	  guest_id = "centos7_64Guest"
	  nested_hv_enabled =true
	  network_interface {
	   network_id     = "${data.vsphere_network.mgmt_lan.id}"
	   adapter_type   = "vmxnet3"
	  }
	
	  disk {
	   size             = 16
	   name             = "test2.vmdk"
	   eagerly_scrub    = false
	   thin_provisioned = true
	  }
	}

And here is the second one:

	<> cat test/variables.tf
	variable "vsphere_server" {}
	variable "vsphere_user" {}
	variable "vsphere_password" {}

And here is the last one:

	<> cat test/terraform.tfvars
	vsphere_server = "192.168.1.109"
	vsphere_user = "root"
	vsphere_password = "password"
	
Now we are ready to create our infrastructure.

### Applying the Terraform Configuration files
First initialize **terraform** which will also install any plugins that you need:

	<> cd test
	<> terraform init
	
	Initializing provider plugins...
	- Checking for available provider plugins on https://releases.hashicorp.com...
	- Downloading plugin for provider "vsphere" (1.1.1)...
	
	The following providers do not have any version constraints in configuration,
	so the latest version was installed.
	
	To prevent automatic upgrades to new major versions that may contain breaking
	changes, it is recommended to add version = "..." constraints to the
	corresponding provider blocks in configuration, with the constraint strings
	suggested below.
	
	* provider.vsphere: version = "~> 1.1"
	
	Terraform has been successfully initialized!
	
	You may now begin working with Terraform. Try running "terraform plan" to see
	any changes that are required for your infrastructure. All Terraform commands
	should now work.
	
	If you ever set or change modules or backend configuration for Terraform,
	rerun this command to reinitialize your working directory. If you forget, other
	commands will detect it and remind you to do so if necessary.

Now let's make sure the plan is okay:

	<> terraform plan
	Refreshing Terraform state in-memory prior to plan...
	The refreshed state will be used to calculate this plan, but will not be
	persisted to local or remote state storage.
	
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	data.vsphere_network.mgmt_lan: Refreshing state...
	
	------------------------------------------------------------------------
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  + create
	
	Terraform will perform the following actions:
	
	  + vsphere_virtual_machine.test2
	      id:                                        <computed>
	      boot_retry_delay:                          "10000"
	      change_version:                            <computed>
	      cpu_limit:                                 "-1"
	      cpu_share_count:                           <computed>
	      cpu_share_level:                           "normal"
	      datastore_id:                              "58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5"
	      default_ip_address:                        <computed>
	      disk.#:                                    "1"
	      disk.0.attach:                             "false"
	      disk.0.device_address:                     <computed>
	      disk.0.disk_mode:                          "persistent"
	      disk.0.disk_sharing:                       "sharingNone"
	      disk.0.eagerly_scrub:                      "false"
	      disk.0.io_limit:                           "-1"
	      disk.0.io_reservation:                     "0"
	      disk.0.io_share_count:                     "0"
	      disk.0.io_share_level:                     "normal"
	      disk.0.keep_on_remove:                     "false"
	      disk.0.key:                                "0"
	      disk.0.name:                               "test2.vmdk"
	      disk.0.size:                               "16"
	      disk.0.thin_provisioned:                   "true"
	      disk.0.unit_number:                        "0"
	      disk.0.write_through:                      "false"
	      ept_rvi_mode:                              "automatic"
	      firmware:                                  "bios"
	      force_power_off:                           "true"
	      guest_id:                                  "centos7_64Guest"
	      guest_ip_addresses.#:                      <computed>
	      host_system_id:                            <computed>
	      hv_mode:                                   "hvAuto"
	      imported:                                  <computed>
	      memory:                                    "2048"
	      memory_limit:                              "-1"
	      memory_share_count:                        <computed>
	      memory_share_level:                        "normal"
	      migrate_wait_timeout:                      "30"
	      name:                                      "test2"
	      nested_hv_enabled:                         "true"
	      network_interface.#:                       "1"
	      network_interface.0.adapter_type:          "vmxnet3"
	      network_interface.0.bandwidth_limit:       "-1"
	      network_interface.0.bandwidth_reservation: "0"
	      network_interface.0.bandwidth_share_count: <computed>
	      network_interface.0.bandwidth_share_level: "normal"
	      network_interface.0.device_address:        <computed>
	      network_interface.0.key:                   <computed>
	      network_interface.0.mac_address:           <computed>
	      network_interface.0.network_id:            "HaNetwork-VM_VLAN1"
	      num_cores_per_socket:                      "1"
	      num_cpus:                                  "1"
	      reboot_required:                           <computed>
	      resource_pool_id:                          "ha-root-pool"
	      run_tools_scripts_after_power_on:          "true"
	      run_tools_scripts_after_resume:            "true"
	      run_tools_scripts_before_guest_shutdown:   "true"
	      run_tools_scripts_before_guest_standby:    "true"
	      scsi_controller_count:                     "1"
	      scsi_type:                                 "pvscsi"
	      shutdown_wait_timeout:                     "3"
	      swap_placement_policy:                     "inherit"
	      uuid:                                      <computed>
	      vmware_tools_status:                       <computed>
	      vmx_path:                                  <computed>
	      wait_for_guest_net_timeout:                "0"
	
	
	Plan: 1 to add, 0 to change, 0 to destroy.
	
	------------------------------------------------------------------------
	
	Note: You didn't specify an "-out" parameter to save this plan, so Terraform
	can't guarantee that exactly these actions will be performed if
	"terraform apply" is subsequently run.

It looks like it will create one 1 VM which greate, so now let's apply it:

	<> terraform apply
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_network.mgmt_lan: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  + create
	
	Terraform will perform the following actions:
	
	  + vsphere_virtual_machine.test2
	      id:                                        <computed>
	      boot_retry_delay:                          "10000"
	      change_version:                            <computed>
	      cpu_limit:                                 "-1"
	      cpu_share_count:                           <computed>
	      cpu_share_level:                           "normal"
	      datastore_id:                              "58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5"
	      default_ip_address:                        <computed>
	      disk.#:                                    "1"
	      disk.0.attach:                             "false"
	      disk.0.device_address:                     <computed>
	      disk.0.disk_mode:                          "persistent"
	      disk.0.disk_sharing:                       "sharingNone"
	      disk.0.eagerly_scrub:                      "false"
	      disk.0.io_limit:                           "-1"
	      disk.0.io_reservation:                     "0"
	      disk.0.io_share_count:                     "0"
	      disk.0.io_share_level:                     "normal"
	      disk.0.keep_on_remove:                     "false"
	      disk.0.key:                                "0"
	      disk.0.name:                               "test2.vmdk"
	      disk.0.size:                               "16"
	      disk.0.thin_provisioned:                   "true"
	      disk.0.unit_number:                        "0"
	      disk.0.write_through:                      "false"
	      ept_rvi_mode:                              "automatic"
	      firmware:                                  "bios"
	      force_power_off:                           "true"
	      guest_id:                                  "centos7_64Guest"
	      guest_ip_addresses.#:                      <computed>
	      host_system_id:                            <computed>
	      hv_mode:                                   "hvAuto"
	      imported:                                  <computed>
	      memory:                                    "2048"
	      memory_limit:                              "-1"
	      memory_share_count:                        <computed>
	      memory_share_level:                        "normal"
	      migrate_wait_timeout:                      "30"
	      name:                                      "test2"
	      nested_hv_enabled:                         "true"
	      network_interface.#:                       "1"
	      network_interface.0.adapter_type:          "vmxnet3"
	      network_interface.0.bandwidth_limit:       "-1"
	      network_interface.0.bandwidth_reservation: "0"
	      network_interface.0.bandwidth_share_count: <computed>
	      network_interface.0.bandwidth_share_level: "normal"
	      network_interface.0.device_address:        <computed>
	      network_interface.0.key:                   <computed>
	      network_interface.0.mac_address:           <computed>
	      network_interface.0.network_id:            "HaNetwork-VM_VLAN1"
	      num_cores_per_socket:                      "1"
	      num_cpus:                                  "1"
	      reboot_required:                           <computed>
	      resource_pool_id:                          "ha-root-pool"
	      run_tools_scripts_after_power_on:          "true"
	      run_tools_scripts_after_resume:            "true"
	      run_tools_scripts_before_guest_shutdown:   "true"
	      run_tools_scripts_before_guest_standby:    "true"
	      scsi_controller_count:                     "1"
	      scsi_type:                                 "pvscsi"
	      shutdown_wait_timeout:                     "3"
	      swap_placement_policy:                     "inherit"
	      uuid:                                      <computed>
	      vmware_tools_status:                       <computed>
	      vmx_path:                                  <computed>
	      wait_for_guest_net_timeout:                "0"
	
	
	Plan: 1 to add, 0 to change, 0 to destroy.
	
	Do you want to perform these actions?
	  Terraform will perform the actions described above.
	  Only 'yes' will be accepted to approve.
	
	  Enter a value: yes
	
	vsphere_virtual_machine.test2: Creating...
	  boot_retry_delay:                          "" => "10000"
	  change_version:                            "" => "<computed>"
	  cpu_limit:                                 "" => "-1"
	  cpu_share_count:                           "" => "<computed>"
	  cpu_share_level:                           "" => "normal"
	  datastore_id:                              "" => "58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5"
	  default_ip_address:                        "" => "<computed>"
	  disk.#:                                    "0" => "1"
	  disk.0.attach:                             "" => "false"
	  disk.0.device_address:                     "" => "<computed>"
	  disk.0.disk_mode:                          "" => "persistent"
	  disk.0.disk_sharing:                       "" => "sharingNone"
	  disk.0.eagerly_scrub:                      "" => "false"
	  disk.0.io_limit:                           "" => "-1"
	  disk.0.io_reservation:                     "" => "0"
	  disk.0.io_share_count:                     "" => "0"
	  disk.0.io_share_level:                     "" => "normal"
	  disk.0.keep_on_remove:                     "" => "false"
	  disk.0.key:                                "" => "0"
	  disk.0.name:                               "" => "test2.vmdk"
	  disk.0.size:                               "" => "16"
	  disk.0.thin_provisioned:                   "" => "true"
	  disk.0.unit_number:                        "" => "0"
	  disk.0.write_through:                      "" => "false"
	  ept_rvi_mode:                              "" => "automatic"
	  firmware:                                  "" => "bios"
	  force_power_off:                           "" => "true"
	  guest_id:                                  "" => "centos7_64Guest"
	  guest_ip_addresses.#:                      "" => "<computed>"
	  host_system_id:                            "" => "<computed>"
	  hv_mode:                                   "" => "hvAuto"
	  imported:                                  "" => "<computed>"
	  memory:                                    "" => "2048"
	  memory_limit:                              "" => "-1"
	  memory_share_count:                        "" => "<computed>"
	  memory_share_level:                        "" => "normal"
	  migrate_wait_timeout:                      "" => "30"
	  name:                                      "" => "test2"
	  nested_hv_enabled:                         "" => "true"
	  network_interface.#:                       "0" => "1"
	  network_interface.0.adapter_type:          "" => "vmxnet3"
	  network_interface.0.bandwidth_limit:       "" => "-1"
	  network_interface.0.bandwidth_reservation: "" => "0"
	  network_interface.0.bandwidth_share_count: "" => "<computed>"
	  network_interface.0.bandwidth_share_level: "" => "normal"
	  network_interface.0.device_address:        "" => "<computed>"
	  network_interface.0.key:                   "" => "<computed>"
	  network_interface.0.mac_address:           "" => "<computed>"
	  network_interface.0.network_id:            "" => "HaNetwork-VM_VLAN1"
	  num_cores_per_socket:                      "" => "1"
	  num_cpus:                                  "" => "1"
	  reboot_required:                           "" => "<computed>"
	  resource_pool_id:                          "" => "ha-root-pool"
	  run_tools_scripts_after_power_on:          "" => "true"
	  run_tools_scripts_after_resume:            "" => "true"
	  run_tools_scripts_before_guest_shutdown:   "" => "true"
	  run_tools_scripts_before_guest_standby:    "" => "true"
	  scsi_controller_count:                     "" => "1"
	  scsi_type:                                 "" => "pvscsi"
	  shutdown_wait_timeout:                     "" => "3"
	  swap_placement_policy:                     "" => "inherit"
	  uuid:                                      "" => "<computed>"
	  vmware_tools_status:                       "" => "<computed>"
	  vmx_path:                                  "" => "<computed>"
	  wait_for_guest_net_timeout:                "" => "0"
	vsphere_virtual_machine.test2: Creation complete after 1s (ID: 564d35b6-17f3-dffe-4236-8294cf3196d0)
	
	Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Now if we login to vsphere client we will see the VM created in the **Events**:

![terraform-create-vm.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/terraform-esxi/terraform-create-vm.png&raw=1)

After a successful deploy, let's destroy the vm (just to clean up):

	<> terraform destroy
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_network.mgmt_lan: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	vsphere_virtual_machine.test2: Refreshing state... (ID: 564d35b6-17f3-dffe-4236-8294cf3196d0)
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  - destroy
	
	Terraform will perform the following actions:
	
	  - vsphere_virtual_machine.test2
	
	
	Plan: 0 to add, 0 to change, 1 to destroy.
	
	Do you really want to destroy?
	  Terraform will destroy all your managed infrastructure, as shown above.
	  There is no undo. Only 'yes' will be accepted to confirm.
	
	  Enter a value: yes
	
	vsphere_virtual_machine.test2: Destroying... (ID: 564d35b6-17f3-dffe-4236-8294cf3196d0)
	vsphere_virtual_machine.test2: Destruction complete after 0s
	
	Destroy complete! Resources: 1 destroyed.

And we will see the corresponding **Events** for that as well:

![terraform-destroy-vm.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/terraform-esxi/terraform-destroy-vm.png&raw=1)
