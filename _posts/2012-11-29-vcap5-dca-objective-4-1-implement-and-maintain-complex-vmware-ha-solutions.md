---
title: VCAP5-DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-4-1-implement-and-maintain-complex-vmware-ha-solutions/
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['ha']
---

### Identify the three admission control policies for HA

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **vSphere HA Admission Control**
> vCenter Server uses admission control to ensure that sufficient resources are available in a cluster to provide failover protection and to ensure that virtual machine resource reservations are respected.
>
> Three types of admission control are available.
>
> **Host** - Ensures that a host has sufficient resources to satisfy the reservations of all virtual machines running on it.
> **Resource Pool** - Ensures that a resource pool has sufficient resources to satisfy the reservations, shares, and limits of all virtual machines associated with it.
> **vSphere HA** - Ensures that sufficient resources in the cluster are reserved for virtual machine recovery in the event of host failure.

Here are each of the admission control policies described in more detail:

> **Host Failures Cluster Tolerates Admission Control Policy**
> You can configure vSphere HA to tolerate a specified number of host failures. With the Host Failures Cluster Tolerates admission control policy, vSphere HA ensures that a specified number of hosts can fail and sufficient resources remain in the cluster to fail over all the virtual machines from those hosts.
>
> With the Host Failures Cluster Tolerates policy, vSphere HA performs admission control in the following way:
>
> 1.  Calculates the slot size.
>     A slot is a logical representation of memory and CPU resources. By default, it is sized to satisfy the requirements for any powered-on virtual machine in the cluster.
> 2.  Determines how many slots each host in the cluster can hold.
> 3.  Determines the Current Failover Capacity of the cluster.
>     This is the number of hosts that can fail and still leave enough slots to satisfy all of the powered-on virtual machines.
> 4.  Determines whether the Current Failover Capacity is less than the Configured Failover Capacity (provided by the user).
>     If it is, admission control disallows the operation.

Here is the next one:

> **Percentage of Cluster Resources Reserved Admission Control Policy**
> You can configure vSphere HA to perform admission control by reserving a specific percentage of cluster CPU and memory resources for recovery from host failures.
> With the Percentage of Cluster Resources Reserved admission control policy, vSphere HA ensures that a specified percentage of aggregate CPU and memory resources are reserved for failover.
>
> With the Cluster Resources Reserved policy, vSphere HA enforces admission control as follows:
>
> 1.  Calculates the total resource requirements for all powered-on virtual machines in the cluster.
> 2.  Calculates the total host resources available for virtual machines.
> 3.  Calculates the Current CPU Failover Capacity and Current Memory Failover Capacity for the cluster.
> 4.  Determines if either the Current CPU Failover Capacity or Current Memory Failover Capacity is less than the corresponding Configured Failover Capacity (provided by the user).
>     If so, admission control disallows the operation.
>
> vSphere HA uses the actual reservations of the virtual machines. If a virtual machine does not have reservations, meaning that the reservation is 0, a default of 0MB memory and 32MHz CPU is applied

And here is the last policy:

> **Specify Failover Hosts Admission Control Policy**
> You can configure vSphere HA to designate specific hosts as the failover hosts.
>
> With the Specify Failover Hosts admission control policy, when a host fails, vSphere HA attempts to restart its virtual machines on one of the specified failover hosts. If this is not possible, for example the failover hosts have failed or have insufficient resources, then vSphere HA attempts to restart those virtual machines on other
> hosts in the cluster.
>
> To ensure that spare capacity is available on a failover host, you are prevented from powering on virtual machines or using vMotion to migrate virtual machines to a failover host. Also, DRS does not use a failover host for load balancing.

### Identify heartbeat options and dependencies

I would say there are 3 types. From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Host Failure Types and Detection**
> The master host monitors the liveness of the slave hosts in the cluster. This communication is done through the exchange of network heartbeats every second. When the master host stops receiving these heartbeats from a slave host, it checks for host liveness before declaring the host to have failed. The liveness check that the master host performs is to determine whether the slave host is exchanging heartbeats with one of the datastores. Also, the master host checks whether the host responds to ICMP pings sent to its management IP addresses.
>
> If a master host is unable to communicate directly with the agent on a slave host, the slave host does not respond to ICMP pings, and the agent is not issuing heartbeats it is considered to have failed. The host's virtual machines are restarted on alternate hosts. If such a slave host is exchanging heartbeats with a datastore, the master host assumes that it is in a network partition or network isolated and so continues to monitor the host and its virtual machines

In the above, two are described: the network heartbeats and datastore heartbeats. The last one only applies when VM Monitoring is enabled. From the same document:

> **VM and Application Monitoring**
> VM Monitoring restarts individual virtual machines if their VMware Tools heartbeats are not received within a set time. Similarly, Application Monitoring can restart a virtual machine if the heartbeats for an application it is running are not received. You can enable these features and configure the sensitivity with which vSphere HA monitors non-responsiveness.
>
> When you enable VM Monitoring, the VM Monitoring service (using VMware Tools) evaluates whether each virtual machine in the cluster is running by checking for regular heartbeats and I/O activity from the VMware Tools process running inside the guest. If no heartbeats or I/O activity are received, this is most likely because the guest operating system has failed or VMware Tools is not being allocated any time to complete tasks. In such a case, the VM Monitoring service determines that the virtual machine has failed and the virtual machine is rebooted to restore service.

So the last type is VMware-tools heartbeats.

### Calculate host failure requirements

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf), here is an example from each policy:

> **Example: Admission Control Using Host Failures Cluster Tolerates Policy**
> The way that slot size is calculated and used with this admission control policy is shown in an example. Make the following assumptions about a cluster:
>
> *   The cluster is comprised of three hosts, each with a different amount of available CPU and memory resources. The first host (H1) has 9GHz of available CPU resources and 9GB of available memory, while Host 2 (H2) has 9GHz and 6GB and Host 3 (H3) has 6GHz and 6GB.
> *   There are five powered-on virtual machines in the cluster with differing CPU and memory requirements.VM1 needs 2GHz of CPU resources and 1GB of memory, while VM2 needs 2GHz and 1GB, VM3 needs 1GHz and 2GB, VM4 needs 1GHz and 1GB, and VM5 needs 1GHz and 1GB.
> *   The Host Failures Cluster Tolerates is set to one
>
> ![ha_host_failure_policy_example](https://github.com/elatov/uploads/raw/master/2012/11/ha_host_failure_policy_example.png)
>
> 1.  Slot size is calculated by comparing both the CPU and memory requirements of the virtual machines and selecting the largest.
>     The largest CPU requirement (shared by VM1 and VM2) is 2GHz, while the largest memory requirement (for VM3) is 2GB. Based on this, the slot size is 2GHz CPU and 2GB memory.
> 2.  Maximum number of slots that each host can support is determined. H1 can support four slots. H2 can support three slots (which is the smaller of 9GHz/2GHz and 6GB/2GB) and H3 can also support three slots.
> 3.  Current Failover Capacity is computed.
>     The largest host is H1 and if it fails, six slots remain in the cluster, which is sufficient for all five of the powered-on virtual machines. If both H1 and H2 fail, only three slots remain, which is insufficient. Therefore, the Current Failover Capacity is one.
>
> The cluster has one available slot (the six slots on H2 and H3 minus the five used slots).

Here is the next policy:

> **Example: Admission Control Using Percentage of Cluster Resources Reserved Policy**
> The way that Current Failover Capacity is calculated and used with this admission control policy is shown with an example. Make the following assumptions about a cluster:
>
> *   The cluster is comprised of three hosts, each with a different amount of available CPU and memory resources. The first host (H1) has 9GHz of available CPU resources and 9GB of available memory, while Host 2 (H2) has 9GHz and 6GB and Host 3 (H3) has 6GHz and 6GB.
> *   There are five powered-on virtual machines in the cluster with differing CPU and memory requirements.VM1 needs 2GHz of CPU resources and 1GB of memory, while VM2 needs 2GHz and 1GB, VM3 needs 1GHz and 2GB, VM4 needs 1GHz and 1GB, and VM5 needs 1GHz and 1GB.
> *   The Configured Failover Capacity is set to 25%.
>
> ![ha_percentage_example](https://github.com/elatov/uploads/raw/master/2012/11/ha_percentage_example.png)
>
> The total resource requirements for the powered-on virtual machines is 7GHz and 6GB. The total host resources available for virtual machines is 24GHz and 21GB. Based on this, the Current CPU Failover Capacity is 70% ((24GHz - 7GHz)/24GHz). Similarly, the Current Memory Failover Capacity is 71% ((21GB-6GB)/21GB).
>
> Because the cluster's Configured Failover Capacity is set to 25%, 45% of the cluster's total CPU resources and 46% of the cluster's memory resources are still available to power on additional virtual machines.

For the last one, not much to calculate there is a stand by host in case of a host failure.

### Configure customized isolation response settings

If you go to the "Host and Cluster" View -> Right click on the cluster and select "Edit Settings" -> Then Under the "HA" section select "Virtual Machine Options" you will be able to set an isolation response either per cluster or per VM. Here is how it looks like in vCenter:

![custom_isolation_response](https://github.com/elatov/uploads/raw/master/2012/11/custom_isolation_response.png)

Also from [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf), here are some advanced settings for the cluster:

> **vSphere HA Advanced Attributes**
> You can set advanced attributes that affect the behavior of your vSphere HA cluster.
>
> ![ha_advanced_settings_isolation](https://github.com/elatov/uploads/raw/master/2012/11/ha_advanced_settings_isolation.png)

Each of these can be edited by going to "Host and Cluster" View -> Right click on the cluster and select "Edit Settings" -> Then select"HA" -> Then select "Advanced Options". This will give you a window where you can enter a option/value combo. Here is how it looks like in vCenter:

![advanced_ha_setting_in_vc](https://github.com/elatov/uploads/raw/master/2012/11/advanced_ha_setting_in_vc.png)

### Configure HA redundancy (Management Network, Datastore Heartbeat, Network partitions)

> **Network Path Redundancy**
> Network path redundancy between cluster nodes is important for vSphere HA reliability. A single management network ends up being a single point of failure and can result in failovers although only the network has failed.
>
> If you have only one management network, any failure between the host and the cluster can cause an unnecessary (or false) failover activity. Possible failures include NIC failures, network cable failures, network cable removal, and switch resets. Consider these possible sources of failure between hosts and try to minimize them, typically by providing network redundancy.
>
> You can implement network redundancy at the NIC level with NIC teaming, or at the management network level. In most implementations, NIC teaming provides sufficient redundancy, but you can use or add management network redundancy if required. Redundant management networking allows the reliable detection of failures and prevents isolation conditions from occurring, because heartbeats can be sent over multiple networks.
>
> Configure the fewest possible number of hardware segments between the servers in a cluster. The goal being to limit single points of failure. Additionally, routes with too many hops can cause networking packet delays for heartbeats, and increase the possible points of failure.
>
> **Network Redundancy Using NIC Teaming**
> Using a team of two NICs connected to separate physical switches improves the reliability of a management network. Because servers connected through two NICs (and through separate switches) have two independent paths for sending and receiving heartbeats, the cluster is more resilient. To configure a NIC team for the management network, configure the vNICs in vSwitch configuration for Active or Standby configuration. The recommended parameter settings for the vNICs are:
>
> *   Default load balancing = route based on originating port ID
> *   Failback = No
>
> After you have added a NIC to a host in your vSphere HA cluster, you must reconfigure vSphere HA on that host.
>
> **Network Redundancy Using a Secondary Network**
> As an alternative to NIC teaming for providing redundancy for heartbeats, you can create a secondary management network connection, which is attached to a separate virtual switch. The primary management network connection is used for network and management purposes. When the secondary management network connection is created, vSphere HA sends heartbeats over both the primary and secondary management network connections. If one path fails, vSphere HA can still send and receive heartbeats over the other path.

From this old white paper "[VMware HA Concepts, Implementation and Best Practices](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/vmw-vsphere-high-availability-whitepaper.pdf)", either do this:

![redundancy_with_nic_teaming](https://github.com/elatov/uploads/raw/master/2012/11/redundancy_with_nic_teaming.png)

or do this:

![redundancy_with_two_mgmt_ints](https://github.com/elatov/uploads/raw/master/2012/11/redundancy_with_two_mgmt_ints.png)

Since this is for ESXi 5.0 you won't have a vswif interface but a vmkernel interface marked as a management interface.

Here is a section regarding datastore heart-beating:

> **Datastore Heartbeating**
> When the master host in a vSphere HA cluster can not communicate with a slave host over the management network, the master host uses datastore heartbeating to determine whether the slave host has failed, is in a network partition, or is network isolated. If the slave host has stopped datastore heartbeating, it is considered to have failed and its virtual machines are restarted elsewhere.
>
> vCenter Server selects a preferred set of datastores for heartbeating. This selection is made to maximize the number of hosts that have access to a heartbeating datastore and minimize the likelihood that the datastores are backed by the same storage array or NFS server. To replace a selected datastore, use the Cluster Settings dialog box of the vSphere Client to specify the heartbeating datastores. The Datastore Heartbeating tab lets you specify alternative datastores. Only datastores mounted by at least two hosts are available. You can also see which datastores vSphere HA has selected for use by viewing the Heartbeat Datastores tab of the HA Cluster Status dialog box.
>
> You can use the advanced attribute das.heartbeatdsperhost to change the number of heartbeat datastores selected by vCenter Server for each host. The default is two and the maximum valid value is five. vSphere HA creates a directory at the root of each datastore that is used for both datastore heartbeating and for persisting the set of protected virtual machines. The name of the directory is .vSphere-HA. Do not delete or modify the files stored in this directory, because this can have an impact on operations. Because more than one cluster might use a datastore, subdirectories for this directory are created for each cluster. Root owns these directories and files and only root can read and write to them. The disk space used by vSphere HA depends on several factors including which VMFS version is in use and the number of hosts that use the datastore for heartbeating. With vmfs3, the maximum usage is approximately 2GB and the typical usage is approximately 3MB. With vmfs5 the maximum and typical usage is approximately 3MB. vSphere HA use of the datastores adds negligible overhead and has no performance impact on other datastore operations.

So you can select a custom datastore to be used for heartbeating if the default is not to your liking. To do so go to the "Host and Cluster" View -> Right click on the cluster and select "Edit Settings" -> Then Under the "HA" section select "Datastore Heartbeating". Here you can select another datastore to be used for heartbeating. Here is how it looks like in vCenter:

![datastore_heartbeating_option](https://github.com/elatov/uploads/raw/master/2012/11/datastore_heartbeating_option.png)

You can also change the option *das.heartbeatdsperhost* to change the number of heartbeat datastores selected by vCenter Server for each host. The process on how to do that was covered in the above section.

Lastly here are network partitions:

> **Network Partitions**
> When a management network failure occurs for a vSphere HA cluster, a subset of the cluster's hosts might be unable to communicate over the management network with the other hosts. Multiple partitions can occur in a cluster.
>
> A partitioned cluster leads to degraded virtual machine protection and cluster management functionality. Correct the partitioned cluster as soon as possible.
>
> *   Virtual machine protection. vCenter Server allows a virtual machine to be powered on, but it is protected only if it is running in the same partition as the master host that is responsible for it. The master host must be communicating with vCenter Server. A master host is responsible for a virtual machine if it has exclusively locked a system-defined file on the datastore that contains the virtual machine's configuration file.
> *   Cluster management. vCenter Server can communicate with only some of the hosts in the cluster, and it can connect to only one master host. As a result, changes in configuration that affect vSphere HA might not take effect until after the partition is resolved. This failure could result in one of the partitions operating under the old configuration, while another uses the new settings.
>
> If a vSphere HA cluster contains pre-ESXi 5.0 hosts and a partition occurs, vSphere HA might incorrectly power on a virtual machine that was powered off by the user or it might fail to restart a virtual machine that failed.
>
> ...
> ...
> **Other Networking Considerations**
> Configure the management networks so that the vSphere HA agent on a host in the cluster can reach the agents on any of the other hosts using one of the management networks. If you do not set up such a configuration, a network partition condition can occur after a master host is elected.

So prevent network partitions make sure all the management interfaces can talk to the management interface of other hosts.

### Configure HA related alarms and monitor an HA cluster

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Setting Alarms to Monitor Cluster Changes**
> When vSphere HA or Fault Tolerance take action to maintain availability, for example, a virtual machine failover, you can be notified about such changes. Configure alarms in vCenter Server to be triggered when these actions occur, and have alerts, such as emails, sent to a specified set of administrators.
>
> Several default vSphere HA alarms are available.
>
> *   Insufficient failover resources (a cluster alarm)
> *   Cannot find master (a cluster alarm)
> *   Failover in progress (a cluster alarm)
> *   Host HA status (a host alarm)
> *   VM monitoring error (a virtual machine alarm)
> *   VM monitoring action (a virtual machine alarm)
> *   Failover failed (a virtual machine alarm)

To check on the HA status of the cluster you can go to "Host and Clusters" view -> then Select a cluster -> then to go the "Summary" tab -> and under the "vSphere HA" Section -> select "Advanced Runtime Info". Here is how it looks like in vCenter:

![ha_advanced_runtime_info](https://github.com/elatov/uploads/raw/master/2012/11/ha_advanced_runtime_info.png)

From the same section you can click on "Cluster Status", that will show you what host is the master, how many VMs are protected, and what datastores are used for heart-beating. Here is how it looks like in vCenter:

![ha_cluster_status](https://github.com/elatov/uploads/raw/master/2012/11/ha_cluster_status.png)

Lastly you can check out the "Configuration Issues":

![ha_cluster_configuration_issues](https://github.com/elatov/uploads/raw/master/2012/11/ha_cluster_configuration_issues.png)

### Create a custom slot size configuration

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Slot Size Calculation**
> Slot size is comprised of two components, CPU and memory.
>
> *   vSphere HA calculates the CPU component by obtaining the CPU reservation of each powered-on virtual machine and selecting the largest value. If you have not specified a CPU reservation for a virtual machine, it is assigned a default value of 32MHz. You can change this value by using the das.vmcpuminmhz advanced attribute.)
> *   vSphere HA calculates the memory component by obtaining the memory reservation, plus memory overhead, of each powered-on virtual machine and selecting the largest value. There is no default valuefor the memory reservation.
>
> If your cluster contains any virtual machines that have much larger reservations than the others, they will distort slot size calculation. To avoid this, you can specify an upper bound for the CPU or memory component of the slot size by using the **das.slotcpuinmhz** or **das.slotmeminmb** advanced attributes, respectively.

### Understand interactions between DRS and HA

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Using vSphere HA and DRS Together**
> Using vSphere HA with Distributed Resource Scheduler (DRS) combines automatic failover with load balancing. This combination can result in a more balanced cluster after vSphere HA has moved virtual machines to different hosts.
>
> When vSphere HA performs failover and restarts virtual machines on different hosts, its first priority is the immediate availability of all virtual machines. After the virtual machines have been restarted, those hosts on which they were powered on might be heavily loaded, while other hosts are comparatively lightly loaded. vSphere HA uses the virtual machine's CPU and memory reservation to determine if a host has enough spare capacity to accommodate the virtual machine.
>
> In a cluster using DRS and vSphere HA with admission control turned on, virtual machines might not be evacuated from hosts entering maintenance mode. This behavior occurs because of the resources reserved for restarting virtual machines in the event of a failure. You must manually migrate the virtual machines off of the hosts using vMotion.
>
> In some scenarios, vSphere HA might not be able to fail over virtual machines because of resource constraints. This can occur for several reasons.
>
> *   HA admission control is disabled and Distributed Power Management (DPM) is enabled. This can result in DPM consolidating virtual machines onto fewer hosts and placing the empty hosts in standby mode leaving insufficient powered-on capacity to perform a failover.
> *   VM-Host affinity (required) rules might limit the hosts on which certain virtual machines can be placed.
> *   There might be sufficient aggregate resources but these can be fragmented across multiple hosts so that they can not be used by virtual machines for failover.
>
> In such cases, vSphere HA can use DRS to try to adjust the cluster (for example, by bringing hosts out of standby mode or migrating virtual machines to defragment the cluster resources) so that HA can perform the failovers.
>
> If DPM is in manual mode, you might need to confirm host power-on recommendations. Similarly, if DRS is in manual mode, you might need to confirm migration recommendations.
>
> If you are using VM-Host affinity rules that are required, be aware that these rules cannot be violated. vSphere HA does not perform a failover if doing so would violate such a rule.

### Analyze vSphere environment to determine appropriate HA admission control policy

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Choosing an Admission Control Policy**
> You should choose a vSphere HA admission control policy based on your availability needs and the characteristics of your cluster. When choosing an admission control policy, you should consider a number of factors.
>
> **Avoiding Resource Fragmentation**
> Resource fragmentation occurs when there are enough resources in aggregate for a virtual machine to be failed over. However, those resources are located on multiple hosts and are unusable because a virtual machine can run on one ESXi host at a time. The Host Failures Cluster Tolerates policy avoids resource fragmentation by defining a slot as the maximum virtual machine reservation. The Percentage of Cluster Resources policy does not address the problem of resource fragmentation. With the Specify Failover Hosts policy, resources are not fragmented because hosts are reserved for failover.
>
> **Flexibility of Failover Resource Reservation**
> Admission control policies differ in the granularity of control they give you when reserving cluster resources for failover protection. The Host Failures Cluster Tolerates policy allows you to set the failover level as a number of hosts. The Percentage of Cluster Resources policy allows you to designate up to 100% of cluster CPU or memory resources for failover. The Specify Failover Hosts policy allows you to specify a set of failover hosts.
>
> **Heterogeneity of Cluster**
> Clusters can be heterogeneous in terms of virtual machine resource reservations and host total resource capacities. In a heterogeneous cluster, the Host Failures Cluster Tolerates policy can be too conservative because it only considers the largest virtual machine reservations when defining slot size and assumes the largest hosts fail when computing the Current Failover Capacity. The other two admission control policies are not affected by cluster heterogeneity.

### Analyze performance metrics to calculate host failure requirements

The biggest thing here is reservations and limits that are set for the VMs. Ensure that all the reservations you have set can be accommodated with the current hosts. Check out the over all usage of CPU and Memory and make sure you are not nearing full utilization. Also size of the cluster matters. From "[vSphere High Availability Deployment Best Practices](http://www.vmware.com/files/pdf/techpaper/vmw-vsphere-high-availability.pdf)":

> The overall size of a cluster is another important factor to consider. Smaller-sized clusters require a larger relative percentage of the available cluster resources to be set aside as reserve capacity to adequately handle failures. For example, for a cluster of three nodes to tolerate a single host failure, about 33 percent of the cluster
> resources will be reserved for failover. A 10-node cluster requires that only 10 percent be reserved.

### Analyze Virtual Machine workload to determine optimum slot size

From [vSphere Availability ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf):

> **Admission Control Best Practices**
> Try to keep virtual machine sizing requirements similar across all configured virtual machines. The Host Failures Cluster Tolerates admission control policy uses slot sizes to calculate the amount of capacity needed to reserve for each virtual machine. The slot size is based on the largest reserved memory and CPU needed for any virtual machine. When you mix virtual machines of different CPU and memory requirements, the slot size calculation defaults to the largest possible, which limits consolidation.

Determine what the average usage of all the VMs is and set that as you slot size. If you have one monster VM then it will throw off your calculation.

### Analyze HA cluster capacity to determine optimum cluster size

Similar as the previous section

