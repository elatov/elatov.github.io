---
title: VCAP5-DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-4-1-implement-and-maintain-complex-vmware-ha-solutions/
dsq_thread_id:
  - 1406786602
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify the three admission control policies for HA

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

> **vSphere HA Admission Control**  
> vCenter Server uses admission control to ensure that sufficient resources are available in a cluster to provide failover protection and to ensure that virtual machine resource reservations are respected.
> 
> Three types of admission control are available.
> 
> **Host** &#8211; Ensures that a host has sufficient resources to satisfy the reservations of all virtual machines running on it.  
> **Resource Pool** &#8211; Ensures that a resource pool has sufficient resources to satisfy the reservations, shares, and limits of all virtual machines associated with it.  
> **vSphere HA** &#8211; Ensures that sufficient resources in the cluster are reserved for virtual machine recovery in the event of host failure.

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

I would say there are 3 types. From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

> **Host Failure Types and Detection**  
> The master host monitors the liveness of the slave hosts in the cluster. This communication is done through the exchange of network heartbeats every second. When the master host stops receiving these heartbeats from a slave host, it checks for host liveness before declaring the host to have failed. The liveness check that the master host performs is to determine whether the slave host is exchanging heartbeats with one of the datastores. Also, the master host checks whether the host responds to ICMP pings sent to its management IP addresses.
> 
> If a master host is unable to communicate directly with the agent on a slave host, the slave host does not respond to ICMP pings, and the agent is not issuing heartbeats it is considered to have failed. The host&#8217;s virtual machines are restarted on alternate hosts. If such a slave host is exchanging heartbeats with a datastore, the master host assumes that it is in a network partition or network isolated and so continues to monitor the host and its virtual machines

In the above, two are described: the network heartbeats and datastore heartbeats. The last one only applies when VM Monitoring is enabled. From the same document:

> **VM and Application Monitoring**  
> VM Monitoring restarts individual virtual machines if their VMware Tools heartbeats are not received within a set time. Similarly, Application Monitoring can restart a virtual machine if the heartbeats for an application it is running are not received. You can enable these features and configure the sensitivity with which vSphere HA monitors non-responsiveness.
> 
> When you enable VM Monitoring, the VM Monitoring service (using VMware Tools) evaluates whether each virtual machine in the cluster is running by checking for regular heartbeats and I/O activity from the VMware Tools process running inside the guest. If no heartbeats or I/O activity are received, this is most likely because the guest operating system has failed or VMware Tools is not being allocated any time to complete tasks. In such a case, the VM Monitoring service determines that the virtual machine has failed and the virtual machine is rebooted to restore service.

So the last type is VMware-tools heartbeats.

### Calculate host failure requirements

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>, here is an example from each policy:

> **Example: Admission Control Using Host Failures Cluster Tolerates Policy**  
> The way that slot size is calculated and used with this admission control policy is shown in an example. Make the following assumptions about a cluster:
> 
> *   The cluster is comprised of three hosts, each with a different amount of available CPU and memory resources. The first host (H1) has 9GHz of available CPU resources and 9GB of available memory, while Host 2 (H2) has 9GHz and 6GB and Host 3 (H3) has 6GHz and 6GB.
> *   There are five powered-on virtual machines in the cluster with differing CPU and memory requirements.VM1 needs 2GHz of CPU resources and 1GB of memory, while VM2 needs 2GHz and 1GB, VM3 needs 1GHz and 2GB, VM4 needs 1GHz and 1GB, and VM5 needs 1GHz and 1GB.
> *   The Host Failures Cluster Tolerates is set to one
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_host_failure_policy_example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_host_failure_policy_example.png']);"><img class="alignnone size-full wp-image-4962" title="ha_host_failure_policy_example" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_host_failure_policy_example.png" alt="ha host failure policy example VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="451" height="316" /></a>
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
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_percentage_example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_percentage_example.png']);"><img class="alignnone size-full wp-image-4964" title="ha_percentage_example" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_percentage_example.png" alt="ha percentage example VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="521" height="303" /></a>
> 
> The total resource requirements for the powered-on virtual machines is 7GHz and 6GB. The total host resources available for virtual machines is 24GHz and 21GB. Based on this, the Current CPU Failover Capacity is 70% ((24GHz &#8211; 7GHz)/24GHz). Similarly, the Current Memory Failover Capacity is 71% ((21GB-6GB)/21GB).
> 
> Because the cluster&#8217;s Configured Failover Capacity is set to 25%, 45% of the cluster&#8217;s total CPU resources and 46% of the cluster&#8217;s memory resources are still available to power on additional virtual machines.

For the last one, not much to calculate there is a stand by host in case of a host failure.

### Configure customized isolation response settings

If you go to the &#8220;Host and Cluster&#8221; View -> Right click on the cluster and select &#8220;Edit Settings&#8221; -> Then Under the &#8220;HA&#8221; section select &#8220;Virtual Machine Options&#8221; you will be able to set an isolation response either per cluster or per VM. Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/custom_isolation_response.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/custom_isolation_response.png']);"><img class="alignnone size-full wp-image-4965" title="custom_isolation_response" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/custom_isolation_response.png" alt="custom isolation response VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="708" height="578" /></a>

Also from <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>, here are some advanced settings for the cluster:

> **vSphere HA Advanced Attributes**  
> You can set advanced attributes that affect the behavior of your vSphere HA cluster.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_settings_isolation.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_settings_isolation.png']);"><img class="alignnone size-full wp-image-4966" title="ha_advanced_settings_isolation" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_settings_isolation.png" alt="ha advanced settings isolation VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="583" height="287" /></a>

Each of these can be edited by going to &#8220;Host and Cluster&#8221; View -> Right click on the cluster and select &#8220;Edit Settings&#8221; -> Then select&#8221;HA&#8221; -> Then select &#8220;Advanced Options&#8221;. This will give you a window where you can enter a option/value combo. Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/advanced_ha_setting_in_vc.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/advanced_ha_setting_in_vc.png']);"><img class="alignnone size-full wp-image-4967" title="advanced_ha_setting_in_vc" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/advanced_ha_setting_in_vc.png" alt="advanced ha setting in vc VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="709" height="577" /></a>

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

From this old white paper &#8220;<a href="http://www.vmware.com/files/pdf/VMwareHA_twp.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/VMwareHA_twp.pdf']);">VMware HA Concepts, Implementation and Best Practices</a>&#8220;, either do this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_nic_teaming.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_nic_teaming.png']);"><img class="alignnone size-full wp-image-4968" title="redundancy_with_nic_teaming" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_nic_teaming.png" alt="redundancy with nic teaming VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="427" height="306" /></a>

or do this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_two_mgmt_ints.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_two_mgmt_ints.png']);"><img class="alignnone size-full wp-image-4970" title="redundancy_with_two_mgmt_ints" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/redundancy_with_two_mgmt_ints.png" alt="redundancy with two mgmt ints VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="422" height="329" /></a>

Since this is for ESXi 5.0 you won&#8217;t have a vswif interface but a vmkernel interface marked as a management interface.

Here is a section regarding datastore heart-beating:

> **Datastore Heartbeating**  
> When the master host in a vSphere HA cluster can not communicate with a slave host over the management network, the master host uses datastore heartbeating to determine whether the slave host has failed, is in a network partition, or is network isolated. If the slave host has stopped datastore heartbeating, it is considered to have failed and its virtual machines are restarted elsewhere.
> 
> vCenter Server selects a preferred set of datastores for heartbeating. This selection is made to maximize the number of hosts that have access to a heartbeating datastore and minimize the likelihood that the datastores are backed by the same storage array or NFS server. To replace a selected datastore, use the Cluster Settings dialog box of the vSphere Client to specify the heartbeating datastores. The Datastore Heartbeating tab lets you specify alternative datastores. Only datastores mounted by at least two hosts are available. You can also see which datastores vSphere HA has selected for use by viewing the Heartbeat Datastores tab of the HA Cluster Status dialog box.
> 
> You can use the advanced attribute das.heartbeatdsperhost to change the number of heartbeat datastores selected by vCenter Server for each host. The default is two and the maximum valid value is five. vSphere HA creates a directory at the root of each datastore that is used for both datastore heartbeating and for persisting the set of protected virtual machines. The name of the directory is .vSphere-HA. Do not delete or modify the files stored in this directory, because this can have an impact on operations. Because more than one cluster might use a datastore, subdirectories for this directory are created for each cluster. Root owns these directories and files and only root can read and write to them. The disk space used by vSphere HA depends on several factors including which VMFS version is in use and the number of hosts that use the datastore for heartbeating. With vmfs3, the maximum usage is approximately 2GB and the typical usage is approximately 3MB. With vmfs5 the maximum and typical usage is approximately 3MB. vSphere HA use of the datastores adds negligible overhead and has no performance impact on other datastore operations.

So you can select a custom datastore to be used for heartbeating if the default is not to your liking. To do so go to the &#8220;Host and Cluster&#8221; View -> Right click on the cluster and select &#8220;Edit Settings&#8221; -> Then Under the &#8220;HA&#8221; section select &#8220;Datastore Heartbeating&#8221;. Here you can select another datastore to be used for heartbeating. Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/datastore_heartbeating_option.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/datastore_heartbeating_option.png']);"><img class="alignnone size-full wp-image-4971" title="datastore_heartbeating_option" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/datastore_heartbeating_option.png" alt="datastore heartbeating option VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="709" height="576" /></a>

You can also change the option *das.heartbeatdsperhost* to change the number of heartbeat datastores selected by vCenter Server for each host. The process on how to do that was covered in the above section.

Lastly here are network partitions:

> **Network Partitions**  
> When a management network failure occurs for a vSphere HA cluster, a subset of the cluster&#8217;s hosts might be unable to communicate over the management network with the other hosts. Multiple partitions can occur in a cluster.
> 
> A partitioned cluster leads to degraded virtual machine protection and cluster management functionality. Correct the partitioned cluster as soon as possible.
> 
> *   Virtual machine protection. vCenter Server allows a virtual machine to be powered on, but it is protected only if it is running in the same partition as the master host that is responsible for it. The master host must be communicating with vCenter Server. A master host is responsible for a virtual machine if it has exclusively locked a system-defined file on the datastore that contains the virtual machine&#8217;s configuration file.
> *   Cluster management. vCenter Server can communicate with only some of the hosts in the cluster, and it can connect to only one master host. As a result, changes in configuration that affect vSphere HA might not take effect until after the partition is resolved. This failure could result in one of the partitions operating under the old configuration, while another uses the new settings.
> 
> If a vSphere HA cluster contains pre-ESXi 5.0 hosts and a partition occurs, vSphere HA might incorrectly power on a virtual machine that was powered off by the user or it might fail to restart a virtual machine that failed.
> 
> &#8230;  
> &#8230;  
> **Other Networking Considerations**  
> Configure the management networks so that the vSphere HA agent on a host in the cluster can reach the agents on any of the other hosts using one of the management networks. If you do not set up such a configuration, a network partition condition can occur after a master host is elected.

So prevent network partitions make sure all the management interfaces can talk to the management interface of other hosts.

### Configure HA related alarms and monitor an HA cluster

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

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

To check on the HA status of the cluster you can go to &#8220;Host and Clusters&#8221; view -> then Select a cluster -> then to go the &#8220;Summary&#8221; tab -> and under the &#8220;vSphere HA&#8221; Section -> select &#8220;Advanced Runtime Info&#8221;. Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_runtime_info.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_runtime_info.png']);"><img class="alignnone size-full wp-image-4991" title="ha_advanced_runtime_info" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_advanced_runtime_info.png" alt="ha advanced runtime info VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="712" height="347" /></a>

From the same section you can click on &#8220;Cluster Status&#8221;, that will show you what host is the master, how many VMs are protected, and what datastores are used for heart-beating. Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_status.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_status.png']);"><img class="alignnone size-full wp-image-4992" title="ha_cluster_status" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_status.png" alt="ha cluster status VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="364" height="408" /></a>

Lastly you can check out the &#8220;Configuration Issues&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_configuration_issues.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_configuration_issues.png']);"><img class="alignnone size-full wp-image-4993" title="ha_cluster_configuration_issues" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/ha_cluster_configuration_issues.png" alt="ha cluster configuration issues VCAP5 DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions " width="809" height="403" /></a>

### Create a custom slot size configuration

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

> **Slot Size Calculation**  
> Slot size is comprised of two components, CPU and memory.
> 
> *   vSphere HA calculates the CPU component by obtaining the CPU reservation of each powered-on virtual machine and selecting the largest value. If you have not specified a CPU reservation for a virtual machine, it is assigned a default value of 32MHz. You can change this value by using the das.vmcpuminmhz advanced attribute.)
> *   vSphere HA calculates the memory component by obtaining the memory reservation, plus memory overhead, of each powered-on virtual machine and selecting the largest value. There is no default valuefor the memory reservation.
> 
> If your cluster contains any virtual machines that have much larger reservations than the others, they will distort slot size calculation. To avoid this, you can specify an upper bound for the CPU or memory component of the slot size by using the **das.slotcpuinmhz** or **das.slotmeminmb** advanced attributes, respectively.

### Understand interactions between DRS and HA

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

> **Using vSphere HA and DRS Together**  
> Using vSphere HA with Distributed Resource Scheduler (DRS) combines automatic failover with load balancing. This combination can result in a more balanced cluster after vSphere HA has moved virtual machines to different hosts.
> 
> When vSphere HA performs failover and restarts virtual machines on different hosts, its first priority is the immediate availability of all virtual machines. After the virtual machines have been restarted, those hosts on which they were powered on might be heavily loaded, while other hosts are comparatively lightly loaded. vSphere HA uses the virtual machine&#8217;s CPU and memory reservation to determine if a host has enough spare capacity to accommodate the virtual machine.
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

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

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

The biggest thing here is reservations and limits that are set for the VMs. Ensure that all the reservations you have set can be accommodated with the current hosts. Check out the over all usage of CPU and Memory and make sure you are not nearing full utilization. Also size of the cluster matters. From &#8220;<a href="http://www.vmware.com/files/pdf/techpaper/vmw-vsphere-high-availability.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/vmw-vsphere-high-availability.pdf']);">vSphere High Availability Deployment Best Practices</a>&#8220;:

> The overall size of a cluster is another important factor to consider. Smaller-sized clusters require a larger relative percentage of the available cluster resources to be set aside as reserve capacity to adequately handle failures. For example, for a cluster of three nodes to tolerate a single host failure, about 33 percent of the cluster  
> resources will be reserved for failover. A 10-node cluster requires that only 10 percent be reserved. 

### Analyze Virtual Machine workload to determine optimum slot size

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>:

> **Admission Control Best Practices**  
> Try to keep virtual machine sizing requirements similar across all configured virtual machines. The Host Failures Cluster Tolerates admission control policy uses slot sizes to calculate the amount of capacity needed to reserve for each virtual machine. The slot size is based on the largest reserved memory and CPU needed for any virtual machine. When you mix virtual machines of different CPU and memory requirements, the slot size calculation defaults to the largest possible, which limits consolidation. 

Determine what the average usage of all the VMs is and set that as you slot size. If you have one monster VM then it will throw off your calculation.

### Analyze HA cluster capacity to determine optimum cluster size

Similar as the previous section

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/11/vcap5-dca-objective-4-1-implement-and-maintain-complex-vmware-ha-solutions/" title=" VCAP5-DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCA,blog;button:compact;">Identify the three admission control policies for HA From vSphere Availability ESXi 5.0: vSphere HA Admission Control vCenter Server uses admission control to ensure that sufficient resources are available in...</a>
</p>