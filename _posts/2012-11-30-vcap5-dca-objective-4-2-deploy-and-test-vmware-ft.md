---
title: VCAP5-DCA Objective 4.2 – Deploy and Test VMware FT
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-4-2-deploy-and-test-vmware-ft/
dsq_thread_id:
  - 1407393735
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify VMware FT hardware requirements

From "[vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf)":

> **Host Requirements for Fault Tolerance**
> You must meet the following host requirements before you use Fault Tolerance.
>
> *   Hosts must have processors from the FT-compatible processor group. It is also highly recommended that the hosts' processors are compatible with one another. See the VMware knowledge base article at http://kb.vmware.com/kb/1008027 for information on supported processors.
> *   Hosts must be licensed for Fault Tolerance.
> *   Hosts must be certified for Fault Tolerance. See http://www.vmware.com/resources/compatibility/search.php and select Search by Fault Tolerant Compatible Sets to determine if your hosts are certified.
> *   The configuration for each host must have Hardware Virtualization (HV) enabled in the BIOS.

### Identify VMware FT compatibility requirements

From "[vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf)":

> **Cluster Requirements for Fault Tolerance**
> You must meet the following cluster requirements before you use Fault Tolerance.
>
> *   Host certificate checking enabled.
> *   At least two FT-certified hosts running the same Fault Tolerance version or host build number. The Fault Tolerance version number appears on a host's Summary tab in the vSphere Client.
> *   ESXi hosts have access to the same virtual machine datastores and networks.
> *   Fault Tolerance logging and VMotion networking configured.
> *   vSphere HA cluster created and enabled. vSphere HA must be enabled before you can power on fault tolerant virtual machines or add a host to a cluster that already supports fault tolerant virtual machines.

Also from the same document:

> **Virtual Machine Requirements for Fault Tolerance**
> You must meet the following virtual machine requirements before you use Fault Tolerance.
>
> *   No unsupported devices attached to the virtual machine.
> *   Virtual machines must be stored in virtual RDM or virtual machine disk (VMDK) files that are thick provisioned. If a virtual machine is stored in a VMDK file that is thin provisioned and an attempt is made to enable Fault Tolerance, a message appears indicating that the VMDK file must be converted. To perform the conversion, you must power off the virtual machine.
> *   Incompatible features must not be running with the fault tolerant virtual machines.
> *   Virtual machine files must be stored on shared storage. Acceptable shared storage solutions include ibre Channel, (hardware and software) iSCSI, NFS, and NAS.
> *   Only virtual machines with a single vCPU are compatible with Fault Tolerance.
> *   Virtual machines must be running on one of the supported guest operating systems. See the VMware knowledge base article at http://kb.vmware.com/kb/1008027 for more information

More requirements:

> **vSphere Features Not Supported with Fault Tolerance**
> The following vSphere features are not supported for fault tolerant virtual machines.
>
> *   Snapshots. Snapshots must be removed or committed before Fault Tolerance can be enabled on a virtual machine. In addition, it is not possible to take snapshots of virtual machines on which Fault Tolerance is enabled.
> *   Storage vMotion. You cannot invoke Storage vMotion for virtual machines with Fault Tolerance turned on. To migrate the storage, you should temporarily turn off Fault Tolerance, and perform the storage vMotion action. When this is complete, you can turn Fault Tolerance back on.
> *   Linked clones. You cannot enable Fault Tolerance on a virtual machine that is a linked clone, nor can you create a linked clone from an FT-enabled virtual machine.
> *   Virtual Machine Backups. You cannot back up an FT-enabled virtual machine using Storage API for Data Protection, VMware Data Recovery, or similar backup products that require the use of a virtual machine snapshot, as performed by ESXi. To back up a fault tolerant virtual machine in this manner, you must first disable FT, then re-enable FT after performing the backup. Storage array-based snapshots do not affect FT.

And here is the last set of requirements:

> **Features and Devices Incompatible with Fault Tolerance**
> For a virtual machine to be compatible with Fault Tolerance, the Virtual Machine must not use the following features or devices
>
> [<img class="alignnone size-full wp-image-5021" title="ft_vm_devices_unsupported" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_vm_devices_unsupported.png" alt="ft vm devices unsupported VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" width="585" height="662" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_vm_devices_unsupported.png)

### Modify VM and ESXi host settings to allow for FT compatibility

Just follow the restrictions above and you should be all set. Here are the ones that stand out for ESXi host:

*   Same Build across the hosts
*   Use 1GB NICs for FT-Logging
*   Have Shared Storage (FC, iSCSI, or NAS)
*   Use Supported FT Hardware

Here are the ones for VMs:

*   1 vCPU
*   No RDMs
*   Remember not to take snapshots of the VM or don't include this VM in the backup inventory
*   Use a Supported OS

### Use VMware best practices to prepare a vSphere environment for FT

From "[vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf)":

> **Best Practices for Fault Tolerance**
> To ensure optimal Fault Tolerance results, VMware recommends that you follow certain best practices
>
> **Host Configuration**
> Consider the following best practices when configuring your hosts.
>
> *    Hosts running the Primary and Secondary VMs should operate at approximately the same processor frequencies, otherwise the Secondary VM might be restarted more frequently. Platform power management features that do not adjust based on workload (for example, power capping and enforced low frequency modes to save power) can cause processor frequencies to vary greatly. If Secondary VMs are being restarted on a regular basis, disable all power management modes on the hosts running fault tolerant virtual machines or ensure that all hosts are running in the same power management modes.
> *   Apply the same instruction set extension configuration (enabled or disabled) to all hosts. The process for enabling or disabling instruction sets varies among BIOSes. See the documentation for your hosts' BIOSes about how to configure instruction sets
>
> **Homogeneous Clusters**
> vSphere Fault Tolerance can function in clusters with nonuniform hosts, but it works best in clusters with compatible nodes. When constructing your cluster, all hosts should have the following configuration:
>
> *   Processors from the same compatible processor group.
> *   Common access to datastores used by the virtual machines.
> *   The same virtual machine network configuration.
> *   The same ESXi version.
> *   The same Fault Tolerance version number (or host build number for hosts prior to ESX/ESXi 4.1).
> *   The same BIOS settings (power management and hyperthreading) for all hosts.
>
> Run Check Compliance to identify incompatibilities and to correct them.
>
> **Performance**
> To increase the bandwidth available for the logging traffic between Primary and Secondary VMs use a 10Gbit NIC, and enable the use of jumbo frames.

And the list keeps going:

> **Store ISOs on Shared Storage for Continuous Access**
> Store ISOs that are accessed by virtual machines with Fault Tolerance enabled on shared storage that is accessible to both instances of the fault tolerant virtual machine. If you use this configuration, the CD-ROM in the virtual machine continues operating normally, even when a failover occurs.
>
> For virtual machines with Fault Tolerance enabled, you might use ISO images that are accessible only to the Primary VM. In such a case, the Primary VM can access the ISO, but if a failover occurs, the CD-ROM reports errors as if there is no media. This situation might be acceptable if the CD-ROM is being used for a temporary, noncritical operation such as an installation.
>
> **Avoid Network Partitions**
> A network partition occurs when a vSphere HA cluster has a management network failure that isolates some of the hosts from vCenter Server and from one another. When a partition occurs, Fault Tolerance protection might be degraded.
>
> In a partitioned vSphere HA cluster using Fault Tolerance, the Primary VM (or its Secondary VM) could end up in a partition managed by a master host that is not responsible for the virtual machine. When a failover is needed, a Secondary VM is restarted only if the Primary VM was in a partition managed by the master host responsible for it.
>
> To ensure that your management network is less likely to have a failure that leads to a network partition, follow the recommendations in “Best Practices for Networking,”.
>
> **Upgrade Hosts Used for Fault Tolerance**
> When you upgrade hosts that contain fault tolerant virtual machines, ensure that the Primary and Secondary VMs continue to run on hosts with the same FT version number or host build number (for hosts prior to ESX/ESXi 4.1).
>
> **Prerequisites**
>
> Verify that you have cluster administrator privileges.
>
> Verify that you have sets of four or more ESXi hosts that are hosting fault tolerant virtual machines that are powered on. If the virtual machines are powered off, the Primary and Secondary VMs can be relocated to hosts with different builds.
> NOTE This upgrade procedure is for a minimum four-node cluster. The same instructions can be followed for a smaller cluster, though the unprotected interval will be slightly longer.
>
> **Procedure**
>
> 1.  Using vMotion, migrate the fault tolerant virtual machines off of two hosts.
> 2.  Upgrade the two evacuated hosts to the same ESXi build.
> 3.  Turn off Fault Tolerance on the Primary VM.
> 4.  Using vMotion, move the disabled Primary VM to one of the upgraded hosts.
> 5.  Turn on Fault Tolerance on the Primary VM that was moved.
> 6.  Repeat Step 1 to Step 5 for as many fault tolerant virtual machine pairs as can be accommodated on the upgraded hosts.
> 7.  Using vMotion, redistribute the fault tolerant virtual machines.
>
> All ESXi hosts in a cluster are upgraded.

### Configure FT logging

From "[vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf)":

> **Configure Networking for Host Machines**
> On each host that you want to add to a vSphere HA cluster, you must configure two different networking switches so that the host can also support vSphere Fault Tolerance.
>
> To enable Fault Tolerance for a host, you must complete this procedure twice, once for each port group option to ensure that sufficient bandwidth is available for Fault Tolerance logging. Select one option, finish this procedure, and repeat the procedure a second time, selecting the other port group option.
>
> **Prerequisites**
> Multiple gigabit Network Interface Cards (NICs) are required. For each host supporting Fault Tolerance, you need a minimum of two physical gigabit NICs. For example, you need one dedicated to Fault Tolerance logging and one dedicated to vMotion. VMware recommends three or more NICs to ensure availability.
>
> **Procedure**
>
> 1.  Connect vSphere Client to vCenter Server.
> 2.  In the vCenter Server inventory, select the host and click the Configuration tab.
> 3.  Select Networking under Hardware, and click the Add Networking link.
>     The Add Network wizard appears.
> 4.  Select VMkernel under Connection Types and click Next.
> 5.  Select Create a virtual switch and click Next.
> 6.  Provide a label for the switch.
> 7.  Select either Use this port group for vMotion or Use this port group for Fault Tolerance logging and
>     click Next.
> 8.  Provide an IP address and subnet mask and click Next.
> 9.  Click Finish.
>
> After you create both a vMotion and Fault Tolerance logging virtual switch, you can create other virtual switches, as needed. You should then add the host to the cluster and complete any steps needed to turn on Fault Tolerance

Here is how it looks like from vCenter:

[<img class="alignnone size-full wp-image-5025" title="ft_logging_pg" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_logging_pg.png" alt="ft logging pg VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" width="524" height="644" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_logging_pg.png)

### Prepare the infrastructure for FT compliance

From "[vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf)":

> **Create vSphere HA Cluster and Check Compliance**
> vSphere Fault Tolerance is used in the context of a vSphere HA cluster. After you have configured networking on each host, create the vSphere HA cluster and add the hosts to it. You can check to see if the cluster is configured correctly and complies with the requirements for the successful enablement of Fault Tolerance.
>
> **Procedure**
>
> 1.  Connect vSphere Client to vCenter Server.
> 2.  In the vCenter Server inventory, select the cluster and click the Profile Compliance tab
> 3.  Click Check Compliance Now to run the compliance tests.
>
> To view the tests that are run, click Description.
> The results of the compliance test appear at the bottom of the screen. A host is labeled as either Compliant or Noncompliant.

Here is how it looks like in vCenter:

[<img class="alignnone size-full wp-image-5026" title="profile_compliance_check" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/profile_compliance_check.png" alt="profile compliance check VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" width="900" height="477" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/profile_compliance_check.png)

Also from the same document:

> NOTE When a host is unable to support Fault Tolerance you can view the reasons for this on the host's Summary tab in the vSphere Client. Click the blue caption icon next to theHost Configured for FT field to see a list of Fault Tolerance requirements that the host does not meet.

Here is how it looks like in vCenter:

[<img class="alignnone size-full wp-image-5027" title="host_ft_compliance" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/host_ft_compliance.png" alt="host ft compliance VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" width="720" height="165" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/host_ft_compliance.png)

### Test FT failover, secondary restart, and application fault tolerance in a FT Virtual Machine

I actually don't have CPU capable of supporting FT, but there is a great step by step guide [here](http://en.community.dell.com/techcenter/virtualization/w/wiki/vmware-vsphere-ft-step-by-step-example.aspx). From the community page:

> **VMware vSphere FT Step by Step Example**
>
> 1. Image depicting the Network configuration.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step1_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step1_c" width="632" height="472" class="alignnone size-full wp-image-5038" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step1_c.jpeg)
>
> 2. Turning on FT.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step2_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step2_c" width="577" height="463" class="alignnone size-full wp-image-5039" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step2_c.jpeg)
>
> 3. 54% through setting up FT.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step3_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step3_c" width="577" height="417" class="alignnone size-full wp-image-5040" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step3_c.jpeg)
>
> 4. FT setup complete.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step4_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step4_c" width="573" height="419" class="alignnone size-full wp-image-5041" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step4_c.jpeg)
>
> 5. vLockstep Interval and Log Bandwidth information are now updated.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step5_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step5_c" width="634" height="397" class="alignnone size-full wp-image-5042" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step5_c.jpeg)
>
> 6. Primary VM is located on 10.10.10.146.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step6_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step6_c" width="640" height="119" class="alignnone size-full wp-image-5043" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step6_c.jpeg)
>
> 7. Secondary VM is running on the Secondary Host- 10.10.10.145.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step7_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step7_c" width="635" height="119" class="alignnone size-full wp-image-5044" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step7_c.jpeg)
>
> 8. Testing FT using the built in Test Failover command.
>
> [<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step8_c.jpeg" alt=" VCAP5 DCA Objective 4.2 – Deploy and Test VMware FT" title="ft_step8_c" width="507" height="386" class="alignnone size-full wp-image-5045" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/ft_step8_c.jpeg)

