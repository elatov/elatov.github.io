---
published: false
layout: post
title: "Terraform with ESXi and Foreman"
author: Karim Elatov
categories: [vmware,devops]
tags: [terraform,foreman]
---
### Terraform Scripts
After figuring out how to create a VM with **terraform** ([Playing Around with Terraform and Jenkins](/2018/10/playing-around-with-terraform-and-jenkins/)) and also how to use **foreman** to provision VM via a Network Install ([Using Foreman to Provision and Configure Machines](/2018/10/using-foreman-to-provision-and-configure-machines/)), I decided to put the two concepts together. I wanted to use **terraform** to create VM in ESXi and then create a Host in **foreman** (which will create a PXE Boot configuration for the VM) and install/configure the OS on the VM. All the **terraform** files are available [here](https://github.com/elatov/terraform/tree/master/foreman). You will just have to create your own **terraform.tfvars** file specifying the credentials to the ESXi host. I used a couple of cool **terraform** features/directives:

- Used **null_resource** to run a command on Foreman
    - [Allow running provisioner on existing resource](https://github.com/hashicorp/terraform/issues/745)
    - [Destroy provisioners not working if resource is using "create_before_destroy" lifecycle](https://github.com/hashicorp/terraform/issues/13395)
    - [Terraform null_resource](https://www.terraform.io/docs/provisioners/null_resource.html) 
- Added a boot delay to ESXi VM
	- [Terraform vsphere_virtual_machine](https://www.terraform.io/docs/providers/vsphere/r/virtual_machine.html)
- Created **locals**
	- [Terraform Local Value Configuration](https://www.terraform.io/docs/configuration/locals.html)
- Ran **remote-exec** provisioner
	- [Terraform remote-exec Provisioner](https://www.terraform.io/docs/provisioners/remote-exec.html) 

I probably could've gotten away without the **locals** but it was good to know they exist.

### Applying the Terraform Plan
Here is a sample of the output:

	<> terraform  apply -var 'vm_name=test1'
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	data.vsphere_network.vm_lan: Refreshing state...
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  + create
	
	Plan: 2 to add, 0 to change, 0 to destroy.
	
	Do you want to perform these actions?
	  Terraform will perform the actions described above.
	  Only 'yes' will be accepted to approve.
	
	  Enter a value: yes
	
	vsphere_virtual_machine.vm_1: Creating...
	  boot_delay:                                "" => "10000"
	  boot_retry_delay:                          "" => "10000"
	  boot_retry_enabled:                        "" => "true"
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
	  disk.0.label:                              "" => "disk0"
	  disk.0.path:                               "" => "<computed>"
	  disk.0.size:                               "" => "16"
	  disk.0.thin_provisioned:                   "" => "true"
	  disk.0.unit_number:                        "" => "0"
	  disk.0.uuid:                               "" => "<computed>"
	  disk.0.write_through:                      "" => "false"
	  ept_rvi_mode:                              "" => "automatic"
	  firmware:                                  "" => "bios"
	  force_power_off:                           "" => "true"
	  guest_id:                                  "" => "centos7_64Guest"
	  guest_ip_addresses.#:                      "" => "<computed>"
	  host_system_id:                            "" => "<computed>"
	  hv_mode:                                   "" => "hvAuto"
	  imported:                                  "" => "<computed>"
	  memory:                                    "" => "1536"
	  memory_limit:                              "" => "-1"
	  memory_share_count:                        "" => "<computed>"
	  memory_share_level:                        "" => "normal"
	  migrate_wait_timeout:                      "" => "30"
	  name:                                      "" => "test1"
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
	  network_interface.0.network_id:            "" => "HaNetwork-VM_VLAN3"
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
	vsphere_virtual_machine.vm_1: Provisioning with 'local-exec'...
	vsphere_virtual_machine.vm_1 (local-exec): Executing: ["/bin/sh" "-c" "echo 00:0c:29:fd:91:60 > mac.txt"]
	vsphere_virtual_machine.vm_1: Creation complete after 1s (ID: 564d0574-97ef-c56b-73be-a7c63dfd9160)
	null_resource.foreman: Creating...
	null_resource.foreman: Provisioning with 'file'...
	null_resource.foreman: Provisioning with 'remote-exec'...
	null_resource.foreman (remote-exec): Connecting to remote host via SSH...
	null_resource.foreman (remote-exec):   Host: fore.kar.int
	null_resource.foreman (remote-exec):   User: elatov
	null_resource.foreman (remote-exec):   Password: false
	null_resource.foreman (remote-exec):   Private key: true
	null_resource.foreman (remote-exec):   SSH Agent: true
	null_resource.foreman (remote-exec): Connected!
	null_resource.foreman (remote-exec): Host created
	null_resource.foreman: Creation complete after 2s (ID: 7434854180654608654)
	
	Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

If you check you won't see the IP until the VM is fully installed, booted, and vmware tools are able to determine the IP. So the first time the IP is unknown:

	<> terraform show
	data.vsphere_datacenter.dc:
	  id = ha-datacenter
	  name = ha-datacenter
	data.vsphere_datastore.datastore:
	  id = 58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5
	  datacenter_id = ha-datacenter
	  name = datastore1
	data.vsphere_network.vm_lan:
	  id = HaNetwork-VM_VLAN3
	  datacenter_id = ha-datacenter
	  name = VM_VLAN3
	  type = Network
	data.vsphere_resource_pool.pool:
	  id = ha-root-pool
	null_resource.foreman:
	  id = 7434854180654608654
	vsphere_virtual_machine.vm_1:
	  id = 564d0574-97ef-c56b-73be-a7c63dfd9160
	  boot_delay = 10000
	  boot_retry_delay = 10000
	  boot_retry_enabled = true
	  guest_id = centos7_64Guest
	  guest_ip_addresses.# = 0
	  host_system_id = ha-host
  
Then after the VM is fully up, you can run another **apply** and see the IP:

	<> terraform  apply -var 'vm_name=test1'
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	data.vsphere_network.vm_lan: Refreshing state...
	vsphere_virtual_machine.vm_1: Refreshing state... (ID: 564d0574-97ef-c56b-73be-a7c63dfd9160)
	null_resource.foreman: Refreshing state... (ID: 7434854180654608654)
	
	Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

	<> terraform show
	data.vsphere_datacenter.dc:
	  id = ha-datacenter
	  name = ha-datacenter
	data.vsphere_datastore.datastore:
	  id = 58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5
	  datacenter_id = ha-datacenter
	  name = datastore1
	data.vsphere_network.vm_lan:
	  id = HaNetwork-VM_VLAN3
	  datacenter_id = ha-datacenter
	  name = VM_VLAN3
	  type = Network
	data.vsphere_resource_pool.pool:
	  id = ha-root-pool
	null_resource.foreman:
	  id = 7434854180654608654
	vsphere_virtual_machine.vm_1:
	  id = 564d0574-97ef-c56b-73be-a7c63dfd9160
	  boot_delay = 10000
	  boot_retry_delay = 10000
	  boot_retry_enabled = true
	  datastore_id = 58a9d7df-a5cf1eb4-b8b5-705a0f42c3e5
	  default_ip_address = 10.0.0.227

### Confirming Host is Added in Foreman  
You should see the new host added with **hammer** and also provisioned in the logs:

	[elatov@fore ~]$ hammer host list
	---|---------------|------------------|------------|----------|-------------------|--------------|----------------------
	ID | NAME          | OPERATING SYSTEM | HOST GROUP | IP       | MAC               | CONTENT VIEW | LIFECYCLE ENVIRONMENT
	---|---------------|------------------|------------|----------|-------------------|--------------|----------------------
	1  | fore.kar.int  | CentOS 7.4.1708  |            | 10.0.0.7 | 00:0c:29:53:5e:1a |              |
	9  | test1.kar.int | CentOS 7         |            |          | 00:0c:29:fd:91:60 |              |
	---|---------------|------------------|------------|----------|-------------------|--------------|----------------------

And here are the logs for the **tftp** configuration creation:

	[elatov@fore ~]$ tail -f /var/log/foreman/production.log
	2018-02-10 19:33:31 537ed054 [templates] [I] Rendering template 'pxegrub2_chainload'
	2018-02-10 19:33:31 537ed054 [app] [I] Deploying TFTP PXEGrub2 configuration for test1.kar.int
	2018-02-10 19:33:31 537ed054 [templates] [I] Rendering template 'PXELinux default local boot'
	2018-02-10 19:33:31 537ed054 [templates] [I] Rendering template 'pxelinux_chainload'
	2018-02-10 19:33:31 537ed054 [app] [I] Deploying TFTP PXELinux configuration for test1.kar.int
	2018-02-10 19:33:31 537ed054 [templates] [I] Rendering template 'PXEGrub default local boot'
	2018-02-10 19:33:31 537ed054 [templates] [I] Rendering template 'pxegrub_chainload'
	2018-02-10 19:33:31 537ed054 [app] [I] Deploying TFTP PXEGrub configuration for test1.kar.int
	2018-02-10 19:33:31 537ed054 [app] [I] Processed 3 tasks from queue 'Host::Managed Main', completed 3/3
	2018-02-10 19:33:31 537ed054 [app] [I] Completed 201 Created in 232ms (ActiveRecord: 22.3ms)

### Destroying the Terraform Plan
If you run a **destroy**, it will remove the VM from the ESXi host and also from **foreman**:

	<> terraform  destroy -var 'vm_name=test1'
	data.vsphere_datacenter.dc: Refreshing state...
	data.vsphere_resource_pool.pool: Refreshing state...
	data.vsphere_datastore.datastore: Refreshing state...
	data.vsphere_network.vm_lan: Refreshing state...
	vsphere_virtual_machine.vm_1: Refreshing state... (ID: 564d0574-97ef-c56b-73be-a7c63dfd9160)
	null_resource.foreman: Refreshing state... (ID: 7434854180654608654)
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  - destroy
	
	Terraform will perform the following actions:
	
	  - null_resource.foreman
	
	  - vsphere_virtual_machine.vm_1
	
	
	Plan: 0 to add, 0 to change, 2 to destroy.
	
	Do you really want to destroy?
	  Terraform will destroy all your managed infrastructure, as shown above.
	  There is no undo. Only 'yes' will be accepted to confirm.
	
	  Enter a value: yes
	
	null_resource.foreman: Destroying... (ID: 7434854180654608654)
	null_resource.foreman: Provisioning with 'file'...
	null_resource.foreman: Provisioning with 'remote-exec'...
	null_resource.foreman (remote-exec): Connecting to remote host via SSH...
	null_resource.foreman (remote-exec):   Host: fore.kar.int
	null_resource.foreman (remote-exec):   User: elatov
	null_resource.foreman (remote-exec):   Password: false
	null_resource.foreman (remote-exec):   Private key: true
	null_resource.foreman (remote-exec):   SSH Agent: true
	null_resource.foreman (remote-exec): Connected!
	null_resource.foreman (remote-exec): Host deleted
	null_resource.foreman: Destruction complete after 2s
	vsphere_virtual_machine.vm_1: Destroying... (ID: 564d0574-97ef-c56b-73be-a7c63dfd9160)
	vsphere_virtual_machine.vm_1: Destruction complete after 2s
	
	Destroy complete! Resources: 2 destroyed.

You can of course login to your Foreman Host and confirm the host had been removed:

	$ hammer host list
	---|--------------|------------------|------------|----------|-------------------|--------------|----------------------
	ID | NAME         | OPERATING SYSTEM | HOST GROUP | IP       | MAC               | CONTENT VIEW | LIFECYCLE ENVIRONMENT
	---|--------------|------------------|------------|----------|-------------------|--------------|----------------------
	1  | fore.kar.int | CentOS 7.4.1708  |            | 10.0.0.7 | 00:0c:29:53:5e:1a |              |
	---|--------------|------------------|------------|----------|-------------------|--------------|----------------------

Pretty nifty.
