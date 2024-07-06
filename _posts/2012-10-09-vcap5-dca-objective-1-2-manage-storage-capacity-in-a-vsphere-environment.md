---
title: VCAP5-DCA Objective 1.2 – Manage Storage Capacity in a vSphere Environment
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-1-2-manage-storage-capacity-in-a-vsphere-environment/
categories: ['storage','certifications', 'vcap5_dca', 'vmware']
tags: ['thick_provisioning', 'thin_provisioning', 'drs']
---

### Identify storage provisioning methods

For protocols we have Fibre Channel, iSCSI, NFS, FCoE. Check out "[Storage Protocol Comparison – A vSphere Perspective](http://blogs.vmware.com/vsphere/2012/02/storage-protocol-comparison-a-vsphere-perspective.html)" to find out what the differences are. Here is a snippet from that page:

![storage_protocols](https://github.com/elatov/uploads/raw/master/2012/09/storage_protocols.png)

For vmdks we have, Lazy Zeroed Thick, Eager Zeroed Thick, and Thin. From the "[vSphere Storage ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf)":

> **Thick Provision Lazy Zeroed**
>
> Creates a virtual disk in a default thick format. Space required for the virtual disk is allocated when the virtual disk is created. Data remaining on the physical device is not erased during creation, but is zeroed out on demand at a later time on first write from the virtual machine. Using the default flat virtual disk format does not zero out or eliminate the possibility of recovering deleted files or restoring old data that might be present on this allocated space. You cannot convert a flat disk to a thin disk.
>
> **Thick Provision Eager Zeroed**
>
> A type of thick virtual disk that supports clustering features such as Fault Tolerance. Space required for the virtual disk is allocated at creation time. In contrast to the flat format, the data remaining on the physical device is zeroed out when the virtual disk is created. It might take much longer to create disks in this format than to create other types of disks.
>
> **Thin Provision**
>
> Use this format to save storage space. For the thin disk, you provision as much datastore space as the disk would require based on the value that you enter for the disk size. However, the thin disk starts small and at first, uses only as much datastore space as the disk needs for its initial operations. **NOTE** If a virtual disk supports clustering solutions such as Fault Tolerance, do not make the disk thin. If the thin disk needs more space later, it can grow to its maximum capacity and occupy the entire datastore space provisioned to it. Also, you can manually convert the thin disk into a thick disk.

### Identify available storage monitoring tools, metrics and alarms

To check for different storage aspects you can use storage views. Check out "[Using VMware vSphere Storage Views](http://www.virtualizationadmin.com/articles-tutorials/vmware-esx-and-vsphere-articles/storage-management/using-vmware-vsphere-storage-views.html)". Go to "Datastore" View -> Click on a datastore -> Click on the "Storage View" Tab. It should look like this:

![storage_view_vms](https://github.com/elatov/uploads/raw/master/2012/09/storage_view_vms.png)

You can also use the Storage Maps to see how you connections look like. Go to the same view as above and then change the view to "Maps". It might look something like this:

![datastore_maps](https://github.com/elatov/uploads/raw/master/2012/09/datastore_maps.png)

For Alarms regarding storage go to "Datastore" View -> Select a Datastore -> Then Select the "Alarms" Tab. You will see predefined alarms for datastores. Something like this:

![datastore_alarms](https://github.com/elatov/uploads/raw/master/2012/09/datastore_alarms.png)

You can also check out storage metrics by going to the performance tab. It will look something like this:

![performance_tab_datastore](https://github.com/elatov/uploads/raw/master/2012/09/performance_tab_datastore.png)

You can also look at the performance from the host view. Go to "Host and Clusters" View -> Select a Host -> Select the Performance Tab -> Select "Advanced" -> Then Switch to "Disk" or "Datastore". It will look something like this:

![host_disk_performance](https://github.com/elatov/uploads/raw/master/2012/09/host_disk_performance.png)

If you want to really check metrics, fire up esxtop and go to the Disk or LUN view. We will discuss that in detail in later objectives.

### Apply space utilization data to manage storage resources

If you run out of space. You could've discovered this by an alarm, storage view, or maybe just running 'df' on the system. To alleviate the issue, use storage vMotion (cold or live) to make space on the datastore. If you have the ability you should expand the VMFS datastore. From the [vSphere Storage ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf) guide:

> **Increase a VMFS Datastore**
> When you need to create virtual machines on a datastore, or when the virtual machines running on a datastore require more space, you can dynamically increase the capacity of a VMFS datastore. Use one of the following methods to increase a VMFS datastore:
>
> *   Add a new extent. An extent is a partition on a storage device. You can add up to 32 extents of the same storage type to an existing VMFS datastore. The spanned VMFS datastore can use any or all of its extents at any time. It does not need to fill up a particular extent before using the next one.
> *   Grow an extent in an existing VMFS datastore, so that it fills the available adjacent capacity. Only extents with free space immediately after them are expandable.

### Provision and manage storage resources according to Virtual Machine requirements

Check out VCAP5-DCD Objectives [3.5](/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/). Just plan for Space, I/O Workload, and Redundancy.

### Understand interactions between virtual storage provisioning and physical storage provisioning

I actually discussed this in "[vSphere Storage ESXi 5.0](/2012/04/thin-on-thin-with-vmware-thin-provisioned-disks-and-emc-symmetrix-virtual-provisioning/):

> **Array Thin Provisioning and VMFS Datastores**
>
> You can use thin provisioned storage arrays with ESXi. Traditional LUNs that arrays present to the ESXi host, are thick-provisioned. The entire physical space needed to back each LUN is allocated in advance. ESXi also supports thin-provisioned LUNs. When a LUN is thin-provisioned, the storage array reports the LUN's logical size, which might be larger than the real physical capacity backing that LUN. A VMFS datastore that you deploy on the thin-provisioned LUN can detect only the logical size of the LUN. For example, if the array reports 2TB of storage while in reality the array provides only 1TB, the datastore considers 2TB to be the LUN's size. As the datastore grows, it cannot determine whether the actual amount of physical space is still sufficient for its needs. However, when you use the Storage APIs - Array Integration, the host can integrate with physical storage and become aware of underlying thin-provisioned LUNs and their space usage. Using thin provision integration, your host can perform these tasks:
>
> *   Monitor the use of space on thin-provisioned LUNs to avoid running out of physical space. As your datastore grows or if you use Storage vMotion to migrate virtual machines to a thin-provisioned LUN, the host communicates with the LUN and warns you about breaches in physical space and about out-of-space conditions.
> *   Inform the array about the datastore space that is freed when files are deleted or removed from the datastore by Storage vMotion. The array can then reclaim the freed blocks of space

### Apply VMware storage best practices

Same as [Objective 1.1](/2012/10/vcap5-dca-objective-1-1-implement-and-manage-complex-storage-solutions/)

### Configure Datastore Alarms

Go To "File" -> "New" -> "Alarm" and then you will see something like this:

![create_new_alarm](https://github.com/elatov/uploads/raw/master/2012/09/create_new_alarm.png)

Go to the "Trigger" tab -> Right Click on the white space -> Select "New Trigger" -> Select a trigger from the drop down menu. It will look something like this:

![select_trigger_for_alarm](https://github.com/elatov/uploads/raw/master/2012/09/select_trigger_for_alarm.png)

Select the Warning and Alert limits. Under the Actions Tab, select whether you want to "Send a notification email", "Send a notification trap", or "Run a command". And you are all set.

### Analyze Datastore Alarms and errors to determine space availability

Check under Triggered Alarms (Datastore View -> Select Datastore -> Select Alarms Tab -> Select Triggered View). If there is an alarm under there, fix it

### Configure Datastore Clusters

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)"

> **Creating a Datastore Cluster**
> A datastore cluster is a collection of datastores with shared resources and a shared management interface. Datastore clusters are to datastores what clusters are to hosts. When you create a datastore cluster, you can use vSphere Storage DRS to manage storage resources.
>
> When you add a datastore to a datastore cluster, the datastore's resources become part of the datastore cluster's resources. As with clusters of hosts, you use datastore clusters to aggregate storage resources, which enables you to support resource allocation policies at the datastore cluster level.
>
> The following resource management capabilities are also available per datastore cluster.
>
> **Space utilization load balancing** You can set a threshold for space use. When space use on a datastore exceeds the threshold, Storage DRS generates recommendations or performs Storage vMotion migrations to balance space use across the datastore cluster.
>
> **I/O latency load balancing** You can set an I/O latency threshold for bottleneck avoidance. When I/O latency on a datastore exceeds the threshold, Storage DRS generates recommendations or performs Storage vMotion migrations to help alleviate high I/O load.
>
> **Anti-affinity rules** You can create anti-affinity rules for virtual machine disks. For example, the virtual disks of a certain virtual machine must be kept on different datastores. By default, all virtual disks for a virtual machine are placed on the same datastore.
>
> **Initial Placement and Ongoing Balancing** Storage DRS provides initial placement and ongoing balancing recommendations to datastores in a Storage DRS-enabled datastore cluster.
>
> Initial placement occurs when Storage DRS selects a datastore within a datastore cluster on which to place a virtual machine disk. This happens when the virtual machine is being created or cloned, when a virtual machine disk is being migrated to another datastore cluster, or when you add a disk to an existing virtual machine.
>
> Initial placement recommendations are made in accordance with space constraints and with respect to the goals of space and I/O load balancing. These goals aim to minimize the risk of over-provisioning one datastore, storage I/O bottlenecks, and performance impact on virtual machines.
>
> Storage DRS is invoked at the configured frequency (by default, every eight hours) or when one or more datastores in a datastore cluster exceeds the user-configurable space utilization thresholds. When Storage DRS is invoked, it checks each datastore's space utilization and I/O latency values against the threshold. For I/O latency, Storage DRS uses the 90th percentile I/O latency measured over the course of a day to compare against the threshold.
>
> **Storage Migration Recommendations**vCenter Server displays migration recommendations on the Storage DRS Recommendations page for datastore clusters that have manual automation mode.
>
> The system provides as many recommendations as necessary to enforce Storage DRS rules and to balance the space and I/O resources of the datastore cluster. Each recommendation includes the virtual machine name, the virtual disk name, the name of the datastore cluster, the source datastore, the destination datastore, and a reason for the recommendation.
>
> *   Balance datastore space use
> *   Balance datastore I/O load
>
> Storage DRS makes mandatory recommendations for migration in the following situations:
>
> *   The datastore is out of space.
> *   Anti-affinity or affinity rules are being violated.
> *   The datastore is entering maintenance mode and must be evacuated.
>
> In addition, optional recommendations are made when a datastore is close to running out of space or when adjustments should be made for space and I/O load balancing. Storage DRS considers moving virtual machines that are powered off or powered on for space balancing.Storage DRS includes powered-off virtual machines with snapshots in these considerations.

Now to the actual process:

> **Create a Datastore Cluster** You can manage datastore cluster resources using Storage DRS. **Procedure**
>
> 1.  In the Datastores and Datastore Clusters view of the vSphere Client inventory, right-click the Datacenter object and select New Datastore Cluster.
> 2.  Follow the prompts to complete the Create Datastore Cluster wizard.

![right_click_datastore_view](https://github.com/elatov/uploads/raw/master/2012/09/right_click_datastore_view.png)

Fill Out the Name:

![Name_Storage_DRS_Cluster](https://github.com/elatov/uploads/raw/master/2012/09/Name_Storage_DRS_Cluster.png)

Set the Automation Level:

![SDRS_Automation_level](https://github.com/elatov/uploads/raw/master/2012/09/SDRS_Automation_level.png)

Set the Threshold Limits:

![SDRS_Threshold_limits](https://github.com/elatov/uploads/raw/master/2012/09/SDRS_Threshold_limits.png)

Select Cluster to enable Storage DRS on:

![SDRS_Select_Hosts](https://github.com/elatov/uploads/raw/master/2012/09/SDRS_Select_Hosts.png)

Select Datastores to participate in the Storage DRS Cluster:

![SDRS_Select_Datastore](https://github.com/elatov/uploads/raw/master/2012/09/SDRS_Select_Datastore.png)

Click Finish on the Summary Page:

![SDRS_Summary_page](https://github.com/elatov/uploads/raw/master/2012/09/SDRS_Summary_page.png)

You will see the datastore cluster that you created, like so:

![datastore_cluster_view_with_dscl](https://github.com/elatov/uploads/raw/master/2012/09/datastore_cluster_view_with_dscl.png)

Now going back to guide:

> **Enable and Disable Storage DRS**
>
> Storage DRS allows you to manage the aggregated resources of a datastore cluster. When Storage DRS is enabled, it provides recommendations for virtual machine disk placement and migration to balance space and I/O resources across the datastores in the datastore cluster. When you enable Storage DRS, you enable the following functions.
>
> *   Space load balancing among datastores within a datastore cluster.
> *   I/O load balancing among datastores within a datastore cluster.
> *   Initial placement for virtual disks based on space and I/O workload.
>
> The Enable Storage DRS check box in the Datastore Cluster Settings dialog box enables or disables all of these components at once. If necessary, you can disable I/O-related functions of Storage DRS independently of space balancing functions.
>
> When you disable Storage DRS on a datastore cluster, Storage DRS settings are preserved. When you enable Storage DRS, the settings for the datastore cluster are restored to the point where Storage DRS was disabled.
>
> **Procedure**
>
> 1.  In the vSphere Client inventory, right-click a datastore cluster and select Edit Settings.
> 2.  Click General.
> 3.  Select Turn on Storage DRS and click OK.
> 4.  (Optional) To disable only I/O-related functions of Storage DRS, leaving space-related controls enabled, perform the following steps.
>     1.  Select SDRS Runtime Rules.
>     2.  Deselect the Enable I/O metric for Storage DRS check box.
> 5.  Click OK

It will look something like this:

![enable_datastore_cluster](https://github.com/elatov/uploads/raw/master/2012/09/enable_datastore_cluster.png)

After that, whatever Storage DRS settings you setup will be applied.

### Related Posts

- [VCAP5-DCA Objective 2.3 – Deploy and Maintain Scalable Virtual Networking](/2012/10/vcap5-dca-objective-2-3-deploy-and-maintain-scalable-virtual-networking/)
- [VCAP5-DCA Objective 2.2 – Configure and Maintain VLANs, PVLANs and VLAN Settings](/2012/10/vcap5-dca-objective-2-2-configure-and-maintain-vlans-pvlans-and-vlan-settings/)
- [VCAP5-DCA Objective 2.1 – Implement and Manage Complex Virtual Networks](/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/)
- [VCAP5-DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug-ins](/2012/10/vcap5-dca-objective-1-3-configure-and-manage-complex-multipathing-and-psa-plug-ins/)

