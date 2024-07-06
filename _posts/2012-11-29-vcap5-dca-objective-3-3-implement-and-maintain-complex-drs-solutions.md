---
title: VCAP5-DCA Objective 3.3 – Implement and Maintain Complex DRS Solutions
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-3-3-implement-and-maintain-complex-drs-solutions/
dsq_thread_id:
  - 1408918922
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['drs']
---

### Explain DRS / storage DRS affinity and anti-affinity rules

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Using DRS Affinity Rules**
> You can control the placement of virtual machines on hosts within a cluster by using affinity rules.
> You can create two types of rules.
>
> *   (VM-Host Affinity Rules) Used to specify affinity or anti-affinity between a group of virtual machines and a group of hosts. An affinity rule specifies that the members of a selected virtual machine DRS group can or must run on the members of a specific host DRS group. An anti-affinity rule specifies that the members of a selected virtual machine DRS group cannot run on the members of a specific host DRS group.
> *   (VM-VM Affinity Rules) Used to specify affinity or anti-affinity between individual virtual machines. A rule specifying affinity causes DRS to try to keep the specified virtual machines together on the same host, for example, for performance reasons. With an anti-affinity rule, DRS tries to keep the specified virtual machines apart, for example, so that when a problem occurs with one host, you do not lose both virtual machines.
>
> When you add or edit an affinity rule, and the cluster's current state is in violation of the rule, the system continues to operate and tries to correct the violation. For manual and partially automated DRS clusters, migration recommendations based on rule fulfillment and load balancing are presented for approval. You are not required to fulfill the rules, but the corresponding recommendations remain until the rules are fulfilled.
>
> To check whether any enabled affinity rules are being violated and cannot be corrected by DRS, select the cluster's DRS tab and click Faults. Any rule currently being violated has a corresponding fault on this page. Read the fault to determine why DRS is not able to satisfy the particular rule. Rules violations also produce a log event.

From the same document:

> **Storage DRS Anti-Affinity Rules**
> You can create Storage DRS anti-affinity rules to control which virtual disks should not be placed on the same datastore within a datastore cluster. By default, a virtual machine's virtual disks are kept together on the same datastore.
>
> When you create an anti-affinity rule, it applies to the relevant virtual disks in the datastore cluster. Antiaffinity rules are enforced during initial placement and Storage DRS-recommendation migrations, but are not enforced when a migration is initiated by a user.
>
> *   Inter-VM Anti-Affinity Rules - Specify which virtual machines should never be kept on the same datastore.
> *   Intra-VM Anti-Affinity Rules - Specify which virtual disks associated with a particular virtual machine must be kept on different datastores.
>
> If you move a virtual disk out of the datastore cluster, the affinity or anti-affinity rule no longer applies to that disk.
>
> When you move virtual disk files into a datastore cluster that has existing affinity and anti-affinity rules, the following behavior applies:
>
> *   Datastore Cluster B has an intra-VM affinity rule. When you move a virtual disk out of Datastore Cluster A and into Datastore Cluster B, any rule that applied to the virtual disk for a given virtual machine in Datastore Cluster A no longer applies. The virtual disk is now subject to the intra-VM affinity rule in Datastore Cluster B.
> *   Datastore Cluster B has an inter-VM anti-affinity rule. When you move a virtual disk out of Datastore Cluster A and into Datastore Cluster B, any rule that applied to the virtual disk for a given virtual machine in Datastore Cluster A no longer applies. The virtual disk is now subject to the inter-VM anti-affinity rule in Datastore Cluster B.
> *   Datastore Cluster B has an intra-VM anti-affinity rule. When you move a virtual disk out of Datastore Cluster A and into Datastore Cluster B, the intra-VM anti-affinity rule does not apply to the virtual disk for a given virtual machine because the rule is limited to only specified virtual disks in Datastore Cluster B.

### Identify required hardware components to support DPM

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Managing Power Resources**
> The vSphere Distributed Power Management (DPM) feature allows a DRS cluster to reduce its power consumption by powering hosts on and off based on cluster resource utilization.
>
> vSphere DPM monitors the cumulative demand of all virtual machines in the cluster for memory and CPU resources and compares this to the total available resource capacity of all hosts in the cluster. If sufficient excess capacity is found, vSphere DPM places one or more hosts in standby mode and powers them off after migrating their virtual machines to other hosts. Conversely, when capacity is deemed to be inadequate, DRS brings hosts out of standby mode (powers them on) and uses vMotion to migrate virtual machines to them. When making these calculations, vSphere DPM considers not only current demand, but it also honors any user-specified virtual machine resource reservations.
>
> vSphere DPM can use one of three power management protocols to bring a host out of standby mode: Intelligent Platform Management Interface (IPMI), Hewlett-Packard Integrated Lights-Out (iLO), or Wake-OnLAN (WOL). Each protocol requires its own hardware support and configuration. If a host does not support any of these protocols it cannot be put into standby mode by vSphere DPM. If a host supports multiple protocols, they are used in the following order: IPMI, iLO, WOL.
>
> **Configure IPMI or iLO Settings for vSphere DPM**
> IPMI is a hardware-level specification and Hewlett-Packard iLO is an embedded server management technology. Each of them describes and provides an interface for remotely monitoring and controlling computers.
>
> You must perform the following procedure on each host.
>
> **Prerequisites**
> Both IPMI and iLO require a hardware Baseboard Management Controller (BMC) to provide a gateway for accessing hardware control functions, and allow the interface to be accessed from a remote system using serial or LAN connections. The BMC is powered-on even when the host itself is powered-off. If properly enabled, the BMC can respond to remote power-on commands.
>
> If you plan to use IPMI or iLO as a wake protocol, you must configure the BMC. BMC configuration steps vary according to model. See your vendor’s documentation for more information. With IPMI, you must also ensure that the BMC LAN channel is configured to be always available and to allow operator-privileged commands. On some IPMI systems, when you enable "IPMI over LAN" you must configure this in the BIOS and specify a particular IPMI account.
>
> vSphere DPM using only IPMI supports MD5- and plaintext-based authentication, but MD2-based authentication is not supported. vCenter Server uses MD5 if a host's BMC reports that it is supported and enabled for the Operator role. Otherwise, plaintext-based authentication is used if the BMC reports it is supported and enabled. If neither MD5 nor plaintext authentication is enabled, IPMI cannot be used with the host and vCenter Server attempts to use Wake-on-LAN.

### Identify EVC requirements, baselines and components

From "[vCenter Server and Host Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-host-management-guide.pdf)":

> **CPU Compatibility and EVC**
> vCenter Server performs a number of compatibility checks before allowing migration of running or suspended virtual machines to ensure that the virtual machine is compatible with the target host.
>
> vMotion transfers the running state of a virtual machine between underlying ESXi systems. Successful live migration requires that the processors of the target host be able to provide the same instructions to the virtual machine after migration that the processors of the source host provided before migration. Clock speed, cache size, and number of cores can differ between source and target processors, but the processors must come from the same vendor class (AMD or Intel) to be vMotion compatible.
>
> Migrations of suspended virtual machines also require that the virtual machine be able to resume execution on the target host using equivalent instructions.
>
> When you initiate a migration with vMotion or a migration of a suspended virtual machine, the Migrate Virtual Machine wizard checks the destination host for compatibility and produces an error message if there are compatibility problems that will prevent migration.
>
> The CPU instruction set available to the operating system and applications running in a virtual machine is determined at the time that a virtual machine is powered on. This CPU "feature set" is determined based on the following items:
>
> *   Host CPU family and model
> *   Settings in the BIOS that might disable CPU features
> *   The ESX/ESXi version running on the host
> *   The virtual machine's virtual hardware version
> *   The virtual machine's guest operating system
>
> To improve CPU compatibility between hosts of varying CPU feature sets, some host CPU features can be "hidden" from the virtual machine by placing the host in an Enhanced vMotion Compatibility (EVC) cluster

More from the same document:

> **About Enhanced vMotion Compatibility**
> You can use the Enhanced vMotion Compatibility (EVC) feature to help ensure vMotion compatibility for the hosts in a cluster. EVC ensures that all hosts in a cluster present the same CPU feature set to virtual machines, even if the actual CPUs on the hosts differ. Using EVC prevents migrations with vMotion from failing because of incompatible CPUs.
>
> Configure EVC from the cluster settings dialog box. When you configure EVC, you configure all host processors in the cluster to present the feature set of a baseline processor. This baseline feature set is called the EVC mode. EVC leverages AMD-V Extended Migration technology (for AMD hosts) and Intel FlexMigration technology (for Intel hosts) to mask processor features so that hosts can present the feature set of an earlier generation of processors. The EVC mode must be equivalent to, or a subset of, the feature set of the host with the smallest feature set in the cluster.
>
> EVC masks only those processor features that affect vMotion compatibility. Enabling EVC does not prevent a virtual machine from taking advantage of faster processor speeds, increased numbers of CPU cores, or hardware virtualization support that might be available on newer hosts.
>
> EVC cannot prevent virtual machines from accessing hidden CPU features in all circumstances. Applications that do not follow CPU vendor recommended methods of feature detection might behave unexpectedly in an EVC environment. VMware EVC cannot be supported with ill-behaved applications that do not follow the
> CPU vendor recommendations.

and lastly here are the requirements from the same document:

> **EVC Requirements**
> Hosts in an EVC cluster must meet certain requirements.
> To enable EVC on a cluster, the cluster must meet the following requirements:
>
> n All virtual machines in the cluster that are running on hosts with a feature set greater than the EVC mode you intend to enable must be powered off or migrated out of the cluster before EVC is enabled.
>
> *   All hosts in the cluster must have CPUs from a single vendor, either AMD or Intel.
> *   All hosts in the cluster must be running ESX/ESXi 3.5 Update 2 or later.
> *   All hosts in the cluster must be connected to the vCenter Server system.
> *   All hosts in the cluster must have advanced CPU features, such as hardware virtualization support (AMDV or Intel VT) and AMD No eXecute (NX) or Intel eXecute Disable (XD), enabled in the BIOS if they are available.
> *   All hosts in the cluster should be configured for vMotion.
> *   All hosts in the cluster must have supported CPUs for the EVC mode you want to enable.

### Understand the DRS / storage DRS migration algorithms, the Load Imbalance Metrics, and their impact on migration recommendations

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Creating a DRS Cluster**
> A DRS cluster is a collection of ESXi hosts and associated virtual machines with shared resources and a shared management interface. Before you can obtain the benefits of cluster-level resource management you must create a DRS cluster.
>
> When you add a host to a DRS cluster, the host’s resources become part of the cluster’s resources. In addition to this aggregation of resources, with a DRS cluster you can support cluster-wide resource pools and enforce cluster-level resource allocation policies. The following cluster-level resource management capabilities are also available.
>
> Load Balancing - The distribution and usage of CPU and memory resources for all hosts and virtual machines in the cluster are continuously monitored. DRS compares
> these metrics to an ideal resource utilization given the attributes of the cluster’s resource pools and virtual machines, the current demand, and the imbalance
> target. It then performs (or recommends) virtual machine migrations accordingly. When you first power on a virtual machine in the cluster, DRS attempts to maintain proper load balancing by either placing the virtual machine on an appropriate host or making a recommendation.
>
> Power management - When the vSphere Distributed Power Management (DPM) feature is enabled,DRS compares cluster- and host-level capacity to the demands of the cluster’s virtual machines, including recent historical demand. It places (or recommends placing) hosts in standby power mode if sufficient excess capacity is found or powering on hosts if capacity is needed. Depending on the resulting host power state recommendations, virtual machines might need to be migrated to and
> from the hosts as well.

More from the same document:

> **Admission Control and Initial Placement**
> When you attempt to power on a single virtual machine or a group of virtual machines in a DRS-enabled cluster, vCenter Server performs admission control. It checks that there are enough resources in the cluster to support the virtual machine(s).
>
> If the cluster does not have sufficient resources to power on a single virtual machine, or any of the virtual machines in a group power-on attempt, a message appears. Otherwise, for each virtual machine, DRS generates a recommendation of a host on which to run the virtual machine and takes one of the following actions
>
> *   Automatically executes the placement recommendation.
> *   Displays the placement recommendation, which the user can then choose to accept or override.

And more information from the same document:

> **Virtual Machine Migration**
> Although DRS performs initial placements so that load is balanced across the cluster, changes in virtual
> machine load and resource availability can cause the cluster to become unbalanced. To correct such imbalances,
> DRS generates migration recommendations.
> If DRS is enabled on the cluster, load can be distributed more uniformly to reduce the degree of this imbalance.
> For example, the three hosts on the left side of the following figure are unbalanced. Assume that Host 1, Host 2,
> and Host 3 have identical capacity, and all virtual machines have the same configuration and load (which
> includes reservation, if set). However, because Host 1 has six virtual machines, its resources might be overused
> while ample resources are available on Host 2 and Host 3. DRS migrates (or recommends the migration of)
> virtual machines from Host 1 to Host 2 and Host 3. On the right side of the diagram, the properly load balanced
> configuration of the hosts that results appears.
>
> ![drs_load_balancing](https://github.com/elatov/uploads/raw/master/2012/10/drs_load_balancing.png)
>
> When a cluster becomes unbalanced, DRS makes recommendations or migrates virtual machines, depending on the default automation level:
>
> *   If the cluster or any of the virtual machines involved are manual or partially automated, vCenter Server does not take automatic actions to balance resources. Instead, the Summary page indicates that migration recommendations are available and the DRS Recommendations page displays recommendations for changes that make the most efficient use of resources across the cluster.
> *   If the cluster and virtual machines involved are all fully automated, vCenter Server migrates running virtual machines between hosts as needed to ensure efficient use of cluster resources.

One more section from the document:

> **Migration Recommendations**
> If you create a cluster with a default manual or partially automated mode, vCenter Server displays migration recommendations on the DRS Recommendations page.
>
> The system supplies as many recommendations as necessary to enforce rules and balance the resources of the cluster. Each recommendation includes the virtual machine to be moved, current (source) host and destination host, and a reason for the recommendation. The reason can be one of the following:
>
> *   Balance average CPU loads or reservations.
> *   Balance average memory loads or reservations.
> *   Satisfy resource pool reservations.
> *   Satisfy an affinity rule.
> *   Host is entering maintenance mode or standby mode.

For Storage DRS, here some information from the same document:

> **Creating a Datastore Cluster**
> A datastore cluster is a collection of datastores with shared resources and a shared management interface. Datastore clusters are to datastores what clusters are to hosts. When you create a datastore cluster, you can use vSphere Storage DRS to manage storage resources.
>
> When you add a datastore to a datastore cluster, the datastore's resources become part of the datastore cluster's resources. As with clusters of hosts, you use datastore clusters to aggregate storage resources, which enables you to support resource allocation policies at the datastore cluster level. The following resource management capabilities are also available per datastore cluster.
>
> Space utilization load balancing - You can set a threshold for space use. When space use on a datastore exceeds the threshold, Storage DRS generates recommendations or performs Storage vMotion migrations to balance space use across the datastore cluster.
>
> I/O latency load balancing - You can set an I/O latency threshold for bottleneck avoidance. When I/O latency on a datastore exceeds the threshold, Storage DRS generates recommendations or performs Storage vMotion migrations to help alleviate high I/O load.
>
> Anti-affinity rules - You can create anti-affinity rules for virtual machine disks. For example, the virtual disks of a certain virtual machine must be kept on different datastores. By default, all virtual disks for a virtual machine are placed on the same datastore.

Here is some information for the algorithm:

> **Initial Placement and Ongoing Balancing**
> Storage DRS provides initial placement and ongoing balancing recommendations to datastores in a Storage DRS-enabled datastore cluster.
>
> Initial placement occurs when Storage DRS selects a datastore within a datastore cluster on which to place a virtual machine disk. This happens when the virtual machine is being created or cloned, when a virtual machine disk is being migrated to another datastore cluster, or when you add a disk to an existing virtual machine.
>
> Initial placement recommendations are made in accordance with space constraints and with respect to the goals of space and I/O load balancing. These goals aim to minimize the risk of over-provisioning one datastore, storage I/O bottlenecks, and performance impact on virtual machines.
>
> Storage DRS is invoked at the configured frequency (by default, every eight hours) or when one or more datastores in a datastore cluster exceeds the user-configurable space utilization thresholds. When Storage DRS is invoked, it checks each datastore's space utilization and I/O latency values against the threshold. For I/O latency, Storage DRS uses the 90th percentile I/O latency measured over the course of a day to compare against the threshold.

and here are the migration recommendations:

> **Storage Migration Recommendations**
> vCenter Server displays migration recommendations on the Storage DRS Recommendations page for datastore clusters that have manual automation mode.
>
> The system provides as many recommendations as necessary to enforce Storage DRS rules and to balance the space and I/O resources of the datastore cluster. Each recommendation includes the virtual machine name, the virtual disk name, the name of the datastore cluster, the source datastore, the destination datastore, and a
> reason for the recommendation.
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
> In addition, optional recommendations are made when a datastore is close to running out of space or when adjustments should be made for space and I/O load balancing.
>
> Storage DRS considers moving virtual machines that are powered off or powered on for space balancing. Storage DRS includes powered-off virtual machines with snapshots in these considerations

### Properly configure BIOS and management settings to support DPM

The Bios Settings are Host specific, but for the Managements settings, from "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Configure IPMI or iLO Settings for vSphere DPM**
> Procedure
>
> 1.  Select the host in the vSphere Client inventory.
> 2.  Click the Configuration tab.
> 3.  Click Power Management
> 4.  Click Properties.
> 5.  Enter the following information.
>     *   User name and password for a BMC account. (The user name must have the ability to remotely power the host on.)
>     *   IP address of the NIC associated with the BMC, as distinct from the IP address of the host. The IP address should be static or a DHCP address with infinite lease.
>     *   MAC address of the NIC associated with the BMC.
> 6.  Click OK.

### Test DPM to verify proper configuration

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Test Wake-on-LAN for vSphere DPM**
> The use of Wake-on-LAN (WOL) for the vSphere DPM feature is fully supported, if you configure and successfully test it according to the VMware guidelines. You must perform these steps before enabling vSphere DPM for a cluster for the first time or on any host that is being added to a cluster that is using vSphere DPM.
>
> **Prerequisites**
>
> *   Your cluster must contain at least two ESX 3.5 (or ESX 3i version 3.5) or later hosts.
> *   Each host's vMotion networking link must be working correctly. The vMotion network should also be a single IP subnet, not multiple subnets separated by routers.
> *   The vMotion NIC on each host must support WOL. To check for WOL support, first determine the name of the physical network adapter corresponding to the VMkernel port by selecting the host in the inventory panel of the vSphere Client, selecting the Configuration tab, and clicking Networking. After you have this information, click on Network Adapters and find the entry corresponding to the network adapter. The Wake On LAN Supported column for the relevant adapter should show Yes.
> *   To display the WOL-compatibility status for each NIC on a host, select the host in the inventory panel of the vSphere Client, select the Configuration tab, and click Network Adapters. The NIC must show Yes in the Wake On LAN Supported column.
> *   The switch port that each WOL-supporting vMotion NIC is plugged into should be set to auto negotiate the link speed, and not set to a fixed speed (for example, 1000 Mb/s). Many NICs support WOL only if they can switch to 100 Mb/s or less when the host is powered off.
>
> After you verify these prerequisites, test each ESXi host that is going to use WOL to support vSphere DPM. When you test these hosts, ensure that the vSphere DPM feature is disabled for the cluster.
>
> **Procedure**
>
> 1.  Click the Enter Standby Mode command on the host's Summary tab in the vSphere Client. This action powers down the host.
> 2.  Try to bring the host out of standby mode by clicking the Power Oncommand on the host's Summary tab.
> 3.  Observe whether or not the host successfully powers back on.
> 4.  For any host that fails to exit standby mode successfully, select the host in the cluster Settings dialog box’s Host Options page and change its Power Management setting to Disabled.
>
> After you do this, vSphere DPM does not consider that host a candidate for being powered off.

### Configure appropriate DPM Threshold to meet business requirements

From "[vCenter Server and Host Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-host-management-guide.pdf)":

> **vSphere DPM Threshold**
> The power state (host power on or off) recommendations generated by the vSphere DPM feature are assigned priorities that range from priority-one recommendations to priority-five recommendations.
>
> These priority ratings are based on the amount of over- or under-utilization found in the DRS cluster and the improvement that is expected from the intended host power state change. A priority-one recommendation is mandatory, while a priority-five recommendation brings only slight improvement.
>
> The threshold is configured under Power Management in the cluster’s Settings dialog box. Each level you move the vSphere DPM Threshold slider to the right allows the inclusion of one more lower level of priority in the set of recommendations that are executed automatically or appear as recommendations to be manually
> executed. At the Conservative setting, vSphere DPM only generates priority-one recommendations, the next level to the right only priority-two and higher, and so on, down to the Aggressive level which generates priority-five recommendations and higher (that is, all recommendations.)

Here is how the configuration looks from the vCenter:

![dpm_cluster_settings](https://github.com/elatov/uploads/raw/master/2012/10/dpm_cluster_settings.png)

### Configure EVC using appropriate baseline

From VMware KB [1003212](http://kb.vmware.com/kb/1003212) here is are the baselines:

![evc_baselines](https://github.com/elatov/uploads/raw/master/2012/10/evc_baselines.png)

and here is a table from the same KB:

![evc_baselines_table](https://github.com/elatov/uploads/raw/master/2012/10/evc_baselines_table.png)

### Change the EVC mode on an existing DRS cluster

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Change the EVC Mode for a Cluster**
> If all the hosts in a cluster are compatible with the new mode, you can change the EVC mode of an existing EVC cluster. You can raise the EVC mode to expose more CPU features, or lower the EVC mode to hide CPU features and increase compatibility.
>
> To raise the EVC mode from a CPU baseline with fewer features to one with more features, you do not need to turn off any running virtual machines in the cluster. Virtual machines that are running do not have access to the new features available in the new EVC mode until they are powered off and powered back on. A full
> power cycling is required. Rebooting the guest operating system or suspending and resuming the virtual machine is not sufficient.
>
> To lower the EVC mode from a CPU baseline with more features to one with fewer features, you must first power off any virtual machines in the cluster that are running at a higher EVC mode than the one you intend to enable, and power them back on after the new mode has been enabled.
>
> **Prerequisites**
> If you intend to lower the EVC mode, power off any currently running virtual machines with a higher EVC mode than the one you intend to enable.
> The cluster cannot contain a disconnected host. All hosts in the cluster must be connected and registered on the vCenter Server.
>
> **Procedure**
>
> 1.  Display the cluster in the inventory.
> 2.  Right-click the cluster and select Edit Settings.
> 3.  In the left panel, select VMware EVC. The dialog box displays the current EVC settings.
> 4.  To edit the EVC settings, click Change.
> 5.  From the VMware EVC Mode drop-down menu, select the baseline CPU feature set you want to enable for the cluster. If the selected EVC Mode cannot be selected, the Compatibility pane displays the reason or reasons why, along with the relevant hosts for each reason.
> 6.  Click OK to close the EVC Mode dialog box, and click OK to close the cluster settings dialog box.

Here is how the settings looks like in vCenter:

![change_evc_mode](https://github.com/elatov/uploads/raw/master/2012/10/change_evc_mode.png)

### Create DRS and DPM alarms

The Bios Settings are Host specific, but for the Managements settings, from "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Monitoring vSphere DPM**
> You can use event-based alarms in vCenter Server to monitor vSphere DPM.
>
> The most serious potential error you face when using vSphere DPM is the failure of a host to exit standby mode when its capacity is needed by the DRS cluster. You can monitor for instances when this error occurs by using the preconfigured Exit Standby Error alarm in vCenter Server. If vSphere DPM cannot bring a host out of
> standby mode (vCenter Server event DrsExitStandbyModeFailedEvent), you can configure this alarm to send an alert email to the administrator or to send notification using an SNMP trap. By default, this alarm is cleared after vCenter Server is able to successfully connect to that host.
>
> ![dpm_events](https://github.com/elatov/uploads/raw/master/2012/10/dpm_events.png)
>
> To monitor vSphere DPM activity, you can also create alarms for the following vCenter Server events.
>
> If you use monitoring software other than vCenter Server, and that software triggers alarms when physical hosts are powered off unexpectedly, you might have a situation where false alarms are generated when vSphere DPM places a host into standby mode. If you do not want to receive such alarms, work with your vendor to
> deploy a version of the monitoring software that is integrated with vCenter Server. You could also use vCenter Server itself as your monitoring solution, because starting with vSphere 4.x, it is inherently aware of vSphere DPM and does not trigger these false alarms

For DRS there are options when you create an Alarm. Here are the available alarms in vCenter:

![create_alarm_for_DRS](https://github.com/elatov/uploads/raw/master/2012/10/create_alarm_for_DRS.png)

### Configure applicable power management settings for ESXi hosts

> **Host Power Management Policies**
> ESXi can take advantage of several power management features that the host hardware provides to adjust the trade-off between performance and power use. You can control how ESXi uses these features by selecting a power management policy.
>
> In general, selecting a high-performance policy provides more absolute performance, but at lower efficiency (performance per watt). Lower-power policies provide less absolute performance, but at higher efficiency.
>
> ESXi provides five power management policies. If the host does not support power management, or if the BIOS settings specify that the host operating system is not allowed to manage power, only the Not Supported policy is available.
>
> You select a policy for a host using the vSphere Client. If you do not select a policy, ESXi uses Balanced by default.
>
> ![power_mgmt_policies](https://github.com/elatov/uploads/raw/master/2012/10/power_mgmt_policies.png)
>
> When a CPU runs at lower frequency, it can also run at lower voltage, which saves power. This type of power management is typically called Dynamic Voltage and Frequency Scaling (DVFS). ESXi attempts to adjust CPU frequencies so that virtual machine performance is not affected.
>
> When a CPU is idle, ESXi can take advantage of deep halt states (known as C-states). The deeper the C-state, the less power the CPU uses, but the longer it takes for the CPU to resume running. When a CPU becomes idle, ESXi applies an algorithm to predict how long it will be in an idle state and chooses an appropriate C-state to enter. In power management policies that do not use deep C-states, ESXi uses only the shallowest halt state(C1) for idle CPUs
>
> **Select a CPU Power Management Policy**
>
> 1.  In the vSphere Client inventory panel, select a host and click the Configuration tab.
> 2.  Under Hardware, select Power Management and select Properties.
> 3.  Select a power management policy for the host and click OK.

### Properly size virtual machines and clusters for optimal DRS efficiency

This was covered in [DCD Objective 3.4](/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/)

### Properly apply virtual machine automation levels based upon application requirements

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Set a Custom Automation Level for a Virtual Machine**
> After you create a DRS cluster, you can customize the automation level for individual virtual machines to override the cluster’s default automation level.
>
> For example, you can select Manual for specific virtual machines in a cluster with full automation, or Partially Automated for specific virtual machines in a manual cluster.
>
> If a virtual machine is set to Disabled, vCenter Server does not migrate that virtual machine or provide migration recommendations for it. This is known as pinning the virtual machine to its registered host
>
> **Procedure**
>
> 1.  In the vSphere Client, right-click the cluster in the inventory and select Edit Settings.
> 2.  In the left pane under vSphere DRS, select Virtual Machine Options.
> 3.  Select the Enable individual virtual machine automation levels check box.
> 4.  (Optional) To temporarily disable any individual virtual machine overrides, deselect the Enable individual virtual machine automation levels check box. Virtual machine settings are restored when the check box is selected again.
> 5.  (Optional) To temporarily suspend all vMotion activity in a cluster, put the cluster in manual mode and deselect the Enable individual virtual machine automation levels check box.
> 6.  Select one or more virtual machines.
> 7.  Click the Automation Level column and select an automation level from the drop-down menu.![drs_automation_levels](https://github.com/elatov/uploads/raw/master/2012/10/drs_automation_levels.png)
> 8.  Click OK.

Here is how it looks like in vCenter:

![vm_automation_levels](https://github.com/elatov/uploads/raw/master/2012/10/vm_automation_levels.png)

### Create and administer ESXi host and Datastore Clusters

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Create a DRS Cluster**
> Create a DRS cluster using the New Cluster wizard in the vSphere Client.
> **Prerequisites**
> You can create a cluster without a special license, but you must have a license to enable a cluster for vSphere DRS (or vSphere HA).
> **Procedure**
>
> 1.  Right-click a datacenter or folder in the vSphere Client and select New Cluster.
> 2.  Name the cluster in the Name text box. This name appears in the vSphere Client inventory panel.
> 3.  Enable the DRS feature by clicking the vSphere DRS box. You can also enable the vSphere HA feature by clicking vSphere HA.
> 4.  Click Next.
> 5.  Select a default automation level for DRS.![drs_automatiion_levels](https://github.com/elatov/uploads/raw/master/2012/10/drs_automatiion_levels.png)
> 6.  Set the migration threshold for DRS.
> 7.  Click Next.
> 8.  Specify the default power management setting for the cluster. If you enable power management, select a vSphere DPM threshold setting.
> 9.  Click Next.
> 10. If appropriate, enable Enhanced vMotion Compatibility (EVC) and select the mode it should operate in.
> 11. Click Next.
> 12. Select a location for the swapfiles of your virtual machines. You can either store a swapfile in the same directory as the virtual machine itself, or a datastore specified by the host (host-local swap)
> 13. Click Next.
> 14. Review the summary page that lists the options you selected.
> 15. Click Finish to complete cluster creation, or click Back to go back and make modifications to the cluster setup.

From the same document:

> **Create a Datastore Cluster**
> You can manage datastore cluster resources using Storage DRS.
> **Procedure**
> 1 In the Datastores and Datastore Clusters view of the vSphere Client inventory, right-click the Datacenter object and select New Datastore Cluster.
> 2 Follow the prompts to complete the Create Datastore Cluster wizard.

### Administer DRS / Storage DRS

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)" here are some things you can do to a Storage DRS Cluster:

> **Using Datastore Clusters to Manage Storage Resources**
>
> After you create a datastore cluster, you can customize it and use it to manage storage I/O and space utilization resources.
>
> This chapter includes the following topics:
>
> *   “Using Storage DRS Maintenance Mode,”
> *   “Applying Storage DRS Recommendations,”
> *   “Change Storage DRS Automation Level for a Virtual Machine,”
> *   “Set Up Off-Hours Scheduling for Storage DRS,”
> *   “Storage DRS Anti-Affinity Rules,”
> *   “Clear Storage DRS Statistics,”
> *   “Storage vMotion Compatibility with Datastore Clusters,”

From the same document, here are some things you can do with a DRS Cluster:

> **Using DRS Clusters to Manage Resources**
>
> After you create a DRS cluster, you can customize it and use it to manage resources.
> To customize your DRS cluster and the resources it contains you can configure affinity rules and you can add and remove hosts and virtual machines. When a cluster’s settings and resources have been defined, you should ensure that it is and remains a valid cluster. You can also use a valid DRS cluster to manage power resources and interoperate with vSphere HA.
>
> This chapter includes the following topics:
>
> *   “Adding Hosts to a Cluster,”
> *   “Adding Virtual Machines to a Cluster,”
> *   “Removing Virtual Machines from a Cluster,”
> *   “Removing a Host from a Cluster,”
> *   “DRS Cluster Validity,”
> *   “Managing Power Resources,”
> *   “Using DRS Affinity Rules,”

