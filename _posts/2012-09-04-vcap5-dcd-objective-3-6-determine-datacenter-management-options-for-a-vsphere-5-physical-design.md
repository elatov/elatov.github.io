---
title: VCAP5-DCD Objective 3.6 – Determine Datacenter Management Options for a vSphere 5 Physical Design
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['kickstart', 'vum', 'vmotion', 'physical_design','ha','drs']
---

### Differentiate and describe client access options

From "[vCenter Server and Host Management ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-management-guide.pdf)":

> **vSphere Client Interfaces**
>
> *   **vSphere Client** A required component and the primary interface for creating, managing, and monitoring virtual machines, their resources, and their hosts. It also provides console access to virtual machines.The vSphere Client is installed on a Windows machine with network access to your ESXi or vCenter Server system installation. The interface displays slightly different options depending on which type of server you are connected to. While all vCenter Server activities are performed by a vCenter Server system, you must use the vSphere Client to monitor, manage, and control the server. A single vCenter Server system or ESXi host can support multiple,simultaneously connected vSphere Clients.
> *   **vSphere Web** Client The vSphere Web Client is a Web application installed on a machine with network access to your vCenter Server installation. In this release, the vSphere Web Client includes a subset of the functionality included in the Windows-based vSphere Client, primarily related to inventory display and virtual machine deployment and configuration.
> *   **vSphere Command-Line Interface** A command-line interface for configuring an ESXi host. The vSphere Command-Line Interface can also be used to perform Storage vMotion operations on both ESXi hosts.

### Based on the service catalog and given functional requirements, for each service: Determine the most appropriate datacenter management options for the design.

From [APAC BrownBag Session 11](https://professionalvmware.com/vmware-certifications/):

![vmware-mgmg-tools](https://github.com/elatov/uploads/raw/master/2012/09/vmware-mgmg-tools.png)

If the skill set is available from the company and one of the above tools can used with ease then definitely offer the option and see how the customer reacts. PowerCLI is a very advanced tool and can be utilized very efficiently to produce reports of usage and performance. It just depends on the willingness of the customer to program the necessary components. Also, the PowerCLI community is huge, so you can find most of the tools already pre-made.

### Analyze cluster availability requirements for HA and FT Check out

[this](/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/) PDF:

> **HA Network Redundancy:**
>
> *   Always configure it
> *   A switch failure could trigger a datacenter-wide isolation response
> *   2 choices:
>     *   2 separate networks, separate subnets... etc
>     *   Single Mgmt network with NIC teaming to multiple switches
> *   HA will use all mgmt interfaces to send heartbeats
> *   In ESXi all vmkernel interfaces expect those marked for vMotion will send out heartbeats
> *   If there are 2 management networks, use das.isolationaddress to add an isolation test address for each mgmt network
>     *   Eliminates isolation test address as a single point of failure
>
> **VMware FT**
>
> *   Only Single CPU Workloads
> *   FT VMs cannot have snapshots, DRS, or storage vMotion
> *   FT VMs need to be in clusters with at least 3 hosts
>     *   Ensures redundancy if a host fails
> *   Use hosts with the same CPU speeds
> *   Disable CPU Power Scaling in BIOS, on hosts running FT VMs
> *   Configure 1Gb Nics for FT logging
> *   With 1Gb Nics, no more than 4 VMs protected by FT on that host
> *   Distribute primary VMs among hosts to reduce contention at the logging level
>     *   Logging is assymentric, Primary -> Secondary
> *   Create Redundant Logging networks

### Analyze cluster performance requirements for DRS and vMotion

From "[Performance Best Practices for VMware vSphere 5.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf)":

> **VMware vMotion**
>
> *   ESXi 5.0 introduces virtual hardware version 8. Because virtual machines running on hardware version 8 can’t run on prior versions of ESX/ESXi, such virtual machines can be moved using VMware vMotion only to other ESXi 5.0 hosts. ESXi 5.0 is also compatible with virtual machines running on virtual hardware version 7 and earlier, however, and these machines can be moved using VMware vMotion to ESX/ESXi 4.x hosts.
> *   vMotion performance will increase as additional network bandwidth is made available to the vMotion network. Consider provisioning 10Gb vMotion network interfaces for maximum vMotion performance.
> *   Multiple vMotion vmknics, a new feature in ESXi 5.0, can provide a further increase in network bandwidth available to vMotion.
> *   All vMotion vmknics on a host should share a single vSwitch. Each vmknic's portgroup should be configured to leverage a different physical NIC as its active vmnic. In addition, all vMotion vmknics should be on the same vMotion network.
> *   While a vMotion operation is in progress, ESXi opportunistically reserves CPU resources on both the source and destination hosts in order to ensure the ability to fully utilize the network bandwidth. ESXi will attempt to use the full available network bandwidth regardless of the number of vMotion operations being performed. The amount of CPU reservation thus depends on the number of vMotion NICs and their speeds; 10% of a processor core for each 1Gb network interface, 100% of a processor core for each 10Gb network interface, and a minimum total reservation of 30% of a processor core. Therefore leaving some unreserved CPU capacity in a cluster can help ensure that vMotion tasks get the resources required in order to fully utilize available network bandwidth.
> *    vMotion performance could be reduced if host-level swap files are placed on local storage

From the same document:

> **VMware Distributed Resource Scheduler (DRS)**
> This section lists Distributed Resource Scheduler (DRS) practices and configurations recommended by VMware for optimal performance.
>
> **Cluster Configuration Settings**
>
> *   When deciding which hosts to group into DRS clusters, try to choose hosts that are as homogeneous as possible in terms of CPU and memory. This improves performance predictability and stability.When heterogeneous systems have compatible CPUs, but have different CPU frequencies and/or amounts of memory, DRS generally prefers to locate virtual machines on the systems with more memory and higher CPU frequencies (all other things being equal), since those systems have more capacity to accommodate peak loads.
> *   VMware vMotion is not supported across hosts with incompatible CPU's. Hence with ‘incompatible CPU’ heterogeneous systems, the opportunities DRS has to improve the load balance across the cluster are limited.
> *   To ensure CPU compatibility, make sure systems are configured with the same CPU vendor, with similar CPU families, and with matching SSE instruction-set capability. For more information on this topic see VMware KB articles 1991, 1992, and 1993.
> *   You can also use Enhanced vMotion Compatibility (EVC) to facilitate vMotion between different CPU generations. For more information on this topic see VMware vMotion and CPU Compatibility and VMware KB article 1003212.
> *   The more vMotion compatible ESXi hosts DRS has available, the more choices it has to better balance the DRS cluster. Besides CPU incompatibility, there are other misconfigurations that can block vMotion between two or more hosts. For example, if the hosts' vMotion network adapters are not connected by a Gigabit (or faster) Ethernet link then the vMotion might not occur between the hosts. Other configuration settings to check for are virtual hardware version compatibility, misconfiguration of the vMotion gateway, incompatible security policies between the source and destination host vMotion network adapter, and virtual machine network availability on the destination host. Refer to vSphere vCenter Server and Host Management for further details.
> *   Virtual machines with smaller memory sizes and/or fewer vCPUs provide more opportunities for DRS to migrate them in order to improve balance across the cluster. Virtual machines with larger memory sizes and/or more vCPUs add more constraints in migrating the virtual machines. This is one more reason to configure virtual machines with only as many vCPUs and only as much virtual memory as they need.
> *   Have virtual machines in DRS automatic mode when possible, as they are considered for cluster load balancing migrations across the ESXi hosts before the virtual machines that are not in automatic mode. Powered-on virtual machines consume memory resources—and typically consume some CPU resources—even when idle. Thus even idle virtual machines, though their utilization is usually small, can affect DRS decisions. For this and other reasons, a marginal performance increase might be obtained by shutting down or suspending virtual machines that are not being used.
> *   Resource pools help improve manageability and troubleshooting of performance problems. We recommend, however, that resource pools and virtual machines not be made siblings in a hierarchy. Instead, each level should contain only resource pools or only virtual machines. This is because by default resource pools are assigned share values that might not compare appropriately with those assigned to virtual machines, potentially resulting in unexpected performance.
> *   DRS affinity rules can keep two or more virtual machines on the same ESXi host (“VM/VM affinity”) or make sure they are always on different hosts (“VM/VM anti-affinity”). DRS affinity rules can also be used to make sure a group of virtual machines runs only on (or has a preference for) a specific group of ESXi hosts (“VM/Host affinity”) or never runs on (or has a preference against) a specific group of hosts (“VM/Host anti-affinity”).
>
> **Cluster Sizing and Resource Settings**
>
> *   Exceeding the maximum number of hosts, virtual machines, or resource pools for each DRS cluster specified in Configuration Maximums for VMware vSphere 5.0 is not supported. Even if it seems to work, doing so could adversely affect vCenter Server or DRS performance.
> *   Carefully select the resource settings (that is, reservations, shares, and limits) for your virtual machines. Setting reservations too high can leave few unreserved resources in the cluster, thus limiting the options DRS has to balance load.
> *   Setting limits too low could keep virtual machines from using extra resources available in the cluster to improve their performance.Use reservations to guarantee the minimum requirement a virtual machine needs, rather than what you might like it to get. Note that shares take effect only when there is resource contention.
> *   Note also that additional resources reserved for virtual machine memory overhead need to be accounted for when sizing resources in the cluster.
> *   If the overall cluster capacity might not meet the needs of all virtual machines during peak hours, you can assign relatively higher shares to virtual machines or resource pools hosting mission-critical applications to reduce the performance interference from less-critical virtual machines.
> *   If you will be using vMotion, it’s a good practice to leave some unused CPU capacity in your cluster. As described in “VMware vMotion” on page 51, when a vMotion operation is started, ESXi reserves some CPU resources for that operation. When using vMotion setup multi-nic vMotion if possible for performance and redundancy. If possible use 10Gb Nics. For DRS make sure you set your reservation appropriately and you can vMotion VMs without disrupting any VM after the vMotion. Use EVC if your CPU models are different but the CPU families are the same.

### Analyze cluster storage performance requirements for SDRS and Storage vMotion

Check out [Performance Best Practices for VMware vSphere 5.0](/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/)":

> **VMware Storage vMotion**
>
> *   VMware Storage vMotion performance depends strongly on the available storage infrastructure bandwidth between the ESXi host where the virtual machine is running and both the source and destination data stores.
> *   During a Storage vMotion operation the virtual disk to be moved is being read from the source data store and written to the destination data store. At the same time the virtual machine continues to read from and write to the source data store while also writing to the destination data store.This additional traffic takes place on storage that might also have other I/O loads (from other virtual machines on the same ESXi host or from other hosts) that can further reduce the available bandwidth.
> *   Storage vMotion will have the highest performance during times of low storage activity (when available storage bandwidth is highest) and when the workload in the virtual machine being moved is least active.
> *   During a Storage vMotion operation, the benefits of moving to a faster data store will be seen only when the migration has completed. However, the impact of moving to a slower data store will gradually be felt as the migration progresses.
> *   Storage vMotion will often have significantly better performance on VAAI-capable storage arrays Both technologies depend on the back end array for performance. Storage vMotion will definitely benefit from a VAAI capable array. For SDRS, VASA would help out significantly to determine the capabilities of the array and migrate VMs depending on those capabilities.

### Determine the appropriate vCenter Server design and sizing requirements: vCenter Server Linked Mode, vCenter Server Virtual Appliance, vCenter Server heartbeat

From "[vCenter Server and Host Management ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-host-management-guide.pdf)":

> **Using vCenter Server in Linked Mode**
> You can join multiple vCenter Server systems using vCenter Linked Mode to allow them to share information. When a server is connected to other vCenter Server systems using Linked Mode, you can connect to that vCenter Server system and view and manage the inventories of the linked vCenter Server systems.Linked Mode uses Microsoft Active Directory Application Mode (ADAM) to store and synchronize data across multiple vCenter Server systems. ADAM is installed as part of vCenter Server installation. Each ADAM instance stores data from the vCenter Server systems in the group, including information about roles andlicenses. This information is replicated across all of the ADAM instances in the connected group to keep them in sync.
>
> When vCenter Server systems are connected in Linked Mode, you can perform the following actions:
>
> *   Log in simultaneously to vCenter Server systems for which you have valid credentials.
> *   Search the inventories of the vCenter Server systems in the group.
> *   View the inventories of the vCenter Server systems in the group in a single inventory view. So if you have multiple vCenter instances to manage different sites, for site recovery or just different locations, then vCenter Linked mode will help out with managing of all the different sites under one location

From "[vSphere Installation and Setup vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-installation-setup-guide.pdf)":

> **Download and Deploy the VMware vCenter Server Appliance**
> As an alternative to installing vCenter Server on a Windows machine, you can download the VMware vCenter Server Appliance. The vCenter Server Appliance is a preconfigured Linux-based virtual machine optimized for running vCenter Server and associated services.
>
> The vCenter Server Appliance has the default user name root and password **vmware**.
>
> Microsoft SQL Server and IBM DB2 are not supported for the vCenter Server Appliance.
>
> **NOTE** Version 5.0.1 of the vCenter Server Appliance uses PostgreSQL for the embedded database instead of IBM DB2, which was used in vCenter Server Appliance 5.0.
>
> The vCenter Server Appliance does not support Linked Mode configuration. The vCenter Server Appliance does not support IPv6.
>
> **IMPORTANT** The embedded database is not configured to manage an inventory that contains more than 5 hosts and 50 virtual machines. If you use the embedded database with the vCenter Server Appliance, exceeding these limits can cause numerous problems, including causing vCenter Server to stop responding

Duncan Epping has a good blog about the topic "[vCenter Appliance](http://www.yellow-bricks.com/2011/08/10/vcenter-appliance/)", from the blog:

> I was playing around in my lab and figured I would give the vCenter Appliance (VCVA) a try. I realize that today there are limitations when it comes to the vCenter Appliance and I wanted to list those to get them out in the open:
>
> *   No Update Manager
> *   No Linked-Mode
> *   No support for the VSA (vSphere Storage Appliance)
> *   Only support for Oracle as the external database
> *   Embedded database, DB2, only supports 5 hosts and 50 VMs
> *   No support for vCenter Heartbeat
>
> Now that you’ve seen the limitations why would you even bother testing it? You will still need Windows if you are running VUM and you can only use Oracle for large environments… Those are probably the two biggest constraints for 80% of you reading this and I agree they are huge constraints. But I am not saying that you should go ahead and deploy this in production straight away, I do feel that the VCVA deserves to be tested as it is the way forward in my opinion! Why? Most importantly, it is very simple to implement

From "[What’s New in VMware vSphere 5.0 - Availability](http://www.vmware.com/files/pdf/techpaper/Whats-New-VMware-vSphere-50-Availability-Technical-Whitepaper.pdf)":

> **Management Availability**
> Being the primary management point of a VMware environment, the availability of VMware vCenter™ Server is a critical consideration when constructing a highly available environment. Providing this availability for VMware vCenter Server is the primary function of VMware vCenter Server Heartbeat.
> With the latest release, several enhancements have been incorporated within VMware vCenter Server Heartbeat. These feature enhancements are the result of the focus of VMware in three key areas — manageability, usability, and application support.

From the same document:

![vc-heartbeat](https://github.com/elatov/uploads/raw/master/2012/09/vc-heartbeat.png)

> **Application Support**
> In addition to providing availability for VMware vCenter Server 5.0, VMware vCenter Server Heartbeat now also provides availability of VMware View Composer and Microsoft SQL Server 2008 R2. This support increases the platform support to match common customer deployment preferences.

It's basically a clustering software that allows vCenter to be fault tolerant. It does require two vCenter Installs and it will synchronize between the two instances. Not only does it allow you to synchronize the vCenter Service but since vCenter can use a MSQL, you can also synchronize that as well. If you have the resources and you need 100% availability of the vCenter then vCenter Heartbeat will be your best bet.

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> **vCenter Protection**
>
> *   Manual - initially cheap, long term expensive, complex, high overhead, and failure downtime
> *   Cluster with Heart Beat - initially expensive, but automatic and fast
> *   Backup/Restore - Too long of RTO
> *   VMware HA - Always use
> *   High Availability of Database Server - Use vendor tools (MSCS) if possible, otherwise use VMware HA

### Determine appropriate access control settings, create roles and assign users to roles

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf)":

> **Managing vSphere Users**
> A user is an individual authorized to log in to either ESXi or vCenter Server. ESXi users fall into two categories: those who can access the host through vCenter Server and those who can access by directly logging in to the host from the vSphere Client, a third-party client, or a command shell.
>
> **Authorized vCenter Server users**
>
> *   Authorized users for vCenter Server are those included in the Windows domain list that vCenter Server references or are local Windows users on the vCenter Server host. You cannot use vCenter Server to manually create, remove, or otherwise change users. You must use the tools for managing your Windows domain. Any changes you make are reflected in vCenter Server. However, the user interface does not provide a user list for you to review.
>
> **Direct-access users**
>
> *   Users authorized to work directly on the host are those added to the internal user list by a system administrator.An administrator can perform a variety of management activities for these users, such as changing passwords, group memberships, and permissions as well as adding and removing users. The user list that ESXi maintains locally is separate from the users known to vCenter Server, which are either local Windows users or users that are part of the Windows domain. If Active Directory authentication has been configured on the host, then the same Windows domain users known to vCenter Server will be available on the ESXi host.
>
> **Best Practices for vSphere Users**
> Use best practices for creating and managing users to increase the security and manageability of your vSphere environment. VMware recommends several best practices for creating users in your vSphere environment:
>
> *   Do not create a user named ALL. Privileges associated with the name ALL might not be available to all users in some situations. For example, if a user named ALL has Administrator privileges, a user with ReadOnly privileges might be able to log in to the host remotely. This is not the intended behavior.
> *   Use a directory service or vCenter Server to centralize access control, rather than defining users on individual hosts.
> *   Choose a local Windows user or group to have the Administrator role in vCenter Server.
> *   Because of the confusion that duplicate naming can cause, check the vCenter Server user list before you create ESXi host users to avoid duplicating names. To check for vCenter Server users, review the Windows domain list.

From the same document:

> **Managing vSphere Groups**
> A group is a set of users that share a common set of rules and permissions. When you assign permissions to a group, all users in the group inherit them, and you do not have to work with the user profiles individually.
>
> The group lists in vCenter Server and the ESXi host are drawn from the same sources as their respective user lists. The group lists in vCenter Server are drawn from the local users or any trusted domain, and the group lists for the host are drawn from the local user list or from any trusted Windows domain.
>
> As an administrator, decide how to structure groups to achieve your security and usage goals. For example, three part-time sales team members work different days, and you want them to share a single virtual machine but not use the virtual machines belonging to sales managers. In this case, you might create a group called SalesShare that includes the three sales people and give the group permission to interact with only one object, the shared virtual machine. They cannot perform any actions on the sales managers’ virtual machines.
>
> **Best Practices for vSphere Groups**
> Use best practices for managing groups to increase the security and manageability of your vSphere environment. VMware recommends several best practices for creating groups in your vSphere environment:
>
> *   Use a directory service or vCenter Server to centralize access control, rather than defining groups on individual hosts.
> *   Choose a local Windows user or group to have the Administrator role in vCenter Server.
> *   Create new groups for vCenter Server users. Avoid using Windows built-in groups or other existing groups.
> *   If you use Active Directory groups, make sure that they are security groups and not distribution groups.
> *   Permissions assigned to distribution groups are not enforced by vCenter Server. For more information about security groups and distribution groups, see the Microsoft Active Directory documentation.

From the same document:

> **Assigning Permissions** For ESXi and vCenter Server, permissions are defined as access roles that consist of a user and the user’s assigned role for an object such as a virtual machine or ESXi host. Permissions grant users the right to perform the activities specified by the role on the object to which the role is assigned.
>
> For example, to configure memory for the host, a user must be granted a role that includes the Host.Configuration.Memory Configuration privilege. By assigning different roles to users or groups for different objects, you can control the tasks that users can perform in your vSphere environment.
>
> By default, all users who are members of the Windows Administrators group on the vCenter Server system have the same access rights as a user assigned to the Administrator role on all objects. When connecting directly to the host, the root and vpxuser user accounts have the same access rights as any user assigned the Administrator role on all objects.
>
> All other users initially have no permissions on any objects, which means they cannot view these objects or perform operations on them. A user with Administrator privileges must assign permissions to these users to allow them to perform tasks.
>
> Many tasks require permissions on more than one object. These rules can help you determine where you must assign permissions to allow particular operations:
>
> *   Any operation that consumes storage space, such as creating a virtual disk or taking a snapshot, requires the Datastore. Allocate Space privilege on the target datastore, as well as the privilege to perform the operation itself.
> *   Moving an object in the inventory hierarchy requires appropriate privileges on the object itself, the source parent object (such as a folder or cluster), and the destination parent object.
> *   Each host and cluster has its own implicit resource pool that contains all the resources of that host or cluster. Deploying a virtual machine directly to a host or cluster requires the Resource.Assign Virtual Machine to Resource Pool privilege.
>
> The list of privileges is the same for both ESXi and vCenter Server, and you use the same method to configure permissions.
>
> You can create roles and set permissions through a direct connection to the ESXi host.
>
> **Hierarchical Inheritance of Permissions**
> When you assign a permission to an object, you can choose whether the permission propagates down the object hierarchy. You set propagation for each permission. Propagation is not universally applied. Permissions defined for a child object always override the permissions that are propagated from parent objects. The figure illustrates inventory hierarchy and the paths by which permissions can propagate.
>
> ![hierarchy-perms](https://github.com/elatov/uploads/raw/master/2012/09/hierarchy-perms.png)
>
> Most inventory objects inherit permissions from a single parent object in the hierarchy. For example, a datastore inherits permissions from either its parent datastore folder or parent datacenter. Virtual machines inherit permissions from both the parent virtual machine folder and the parent host, cluster, or resource pool simultaneously. To restrict a user’s privileges on a virtual machine, you must set permissions on both the parent folder and the parent host, cluster, or resource pool for that virtual machine.
>
> To set permissions for a distributed switch and its associated distributed port groups, set permissions on a parent object, such a folder or datacenter. You must also select the option to propagate these permissions to child objects.

I think the next part from the same document is the best part:

> **Best Practices for Roles and Permissions**
> Use best practices for roles and permissions to maximize the security and manageability of your vCenter Server environment. VMware recommends the following best practices when configuring roles and permissions in your vCenter Server environment:
>
> *   Where possible, grant permissions to groups rather than individual users.
> *   Grant permissions only where needed. Using the minimum number of permissions makes it easier to understand and manage your permissions structure.
> *   If you assign a restrictive role to a group, check that the group does not contain the Administrator user or other users with administrative privileges.
> *   Otherwise, you could unintentionally restrict administrators' privileges in parts of the inventory hierarchy where you have assigned that group the restrictive role.
> *   Use folders to group objects to correspond to the differing permissions you want to grant for them.
> *   Use caution when granting a permission at the root vCenter Server level. Users with permissions at the root level have access to global data on vCenter Server, such as roles, custom attributes, vCenter Server settings, and licenses. Changes to licenses and roles propagate to all vCenter Server systems in a Linked Mode group, even if the user does not have permissions on all of the vCenter Server systems in the group.
> *   In most cases, enable propagation on permissions. This ensures that when new objects are inserted in to the inventory hierarchy, they inherit permissions and are accessible to users.
> *   Use the No Access role to masks specific areas of the hierarchy that you don’t want particular users to have access to.

Then comes a pretty good example for necessary permission for certain tasks:

> **Required Privileges for Common Tasks**
> Many tasks require permissions on more than one object in the inventory. You can review the privileges required to perform the tasks and, where applicable, the appropriate sample roles. The following table lists common tasks that require more than one privilege. You can use the Applicable Roles on the inventory objects to grant permission to perform these tasks, or you can create your own roles with the equivalent required privileges. ![pemissions-to-create-vms](https://github.com/elatov/uploads/raw/master/2012/09/pemissions-to-create-vms.png)

Lastly here are roles from the same document:

> **Assigning Roles**
> vCenter Server and ESXi grant access to objects only to users who are assigned permissions for the object. When you assign a user or group permissions for the object, you do so by pairing the user or group with a role. A role is a predefined set of privileges.
>
> ESXi hosts provide three default roles, and you cannot change the privileges associated with these roles. Each subsequent default role includes the privileges of the previous role. For example, the Administrator role inherits the privileges of the Read Only role. Roles you create yourself do not inherit privileges from any of the default roles.
>
> You can create custom roles by using the role-editing facilities in the vSphere Client to create privilege sets that match your user needs. If you use the vSphere Client connected to vCenter Server to manage ESXi hosts, you have additional roles to choose from in vCenter Server. Also, the roles you create directly on a host are not accessible within vCenter Server. You can work with these roles only if you log in to the host directly from the vSphere Client.
>
> NOTE When you add a custom role and do not assign any privileges to it, the role is created as a Read Only role with three system-defined privileges: System.Anonymous, System.View, and System.Read.
>
> If you manage ESXi hosts through vCenter Server, maintaining custom roles in the host and vCenter Server can result in confusion and misuse. In this type of configuration, maintain custom roles only in vCenter Server.
>
> You can create roles and set permissions through a direct connection to the ESXi host
>
> **Using Roles to Assign Privileges**
> A role is a predefined set of privileges. Privileges define individual rights that a user requires to perform actions and read properties.
>
> When you assign a user or group permissions, you pair the user or group with a role and associate that pairing with an inventory object. A single user might have different roles for different objects in the inventory. For example, if you have two resource pools in your inventory, Pool A and Pool B, you might assign a particular user the Virtual Machine User role on Pool A and the Read Only role on Pool B. These assignments would allow that user to turn on virtual machines in Pool A, but not those in Pool B. The user would still be able to view the status of the virtual machines in Pool B.
>
> The roles created on a host are separate from the roles created on a vCenter Server system. When you manage a host using vCenter Server, the roles created through vCenter Server are available. If you connect directly to the host using the vSphere Client, the roles created directly on the host are available. vCenter Server and ESXi hosts provide default roles:
>
> **System roles**
>
> *   System roles are permanent. You cannot edit the privileges associated with these roles.
>
> **Sample roles**
>
> *   VMware provides sample roles for convenience as guidelines and suggestions. You can modify or remove these roles.
>
> You can also create roles. All roles permit the user to schedule tasks by default. Users can schedule only tasks they have permission to perform at the time the tasks are created.
>
> **NOTE** Changes to permissions and roles take effect immediately, even if the users involved are logged in. The exception is searches, where permission changes take effect after the user has logged out and logged back in.

This was also discussed in [Objective 3.1](/2012/08/vcap5-dcd-objective-3-1-transition-from-a-logical-design-to-a-vsphere-5-physical-design/)

### Based on the logical design, identify and implement asset and configuration management technologies.

There are a couple of application that can do asset management. The first one is VWare GO. From [VMworld 2012: Introducing the New VMware Go Pro for SMBs!](https://blogs.vmware.com/go/2012/08/vmworld-2012-introducing-the-new-vmware-go-pro-for-smbs.html):

> ![vmware-go](https://github.com/elatov/uploads/raw/master/2012/09/vmware-go.png)
> **Comprehensive Infrastructure Protection**
> VMware Go Pro offers automated patch management across physical and virtual machines for both Microsoft and third-party applications to ensure that organizations are up-to-date with all of the latest software upgrades, thus mitigating the organization’s vulnerability to the latest IT threats. An integrated Help Desk with built-in analytics also helps improve IT productivity and service, automatically prioritizing issues by level of severity. Go Pro also offers a rich asset management capability, which provides control over all software and hardware assets.

There is also VMware Service Manager. From "[VMware Service Manager Cloud Provisioning](https://www.vmware.com/products/service-manager.html)":

> How Does VMware Service Manager Work with vCloud Director?
> The VMware Service Manager connector to vCloud Director provides additional functionality to vCloud Director:
>
> *   Service catalog customer portal.
> *   Configurable and extendable request forms.
> *   Change-request management for owned items.
> *   Flexible and powerful workflow engine.
>
> VMware Service Manager can also utilize its connectors to vCenter Orchestrator and vCenter Configuration Manager to automate additional modifications to cloud infrastructure.

And for the [features](http://www.vmware.com/products/datacenter-virtualization/service-manager/features.html) page:

> Give cloud consumers a unified experience and dramatically simplify the process of requesting cloud resources.
>
> *   Remove bottlenecks while enforcing approval policies through service automation.
> *   Process approvals, provision and track the entire cloud life cycle.
> *   Control access to resources while providing the flexibility to choose and easily modify services.
>
> **Service Catalog**
>
> *   Provide a user portal for requesting and changing cloud resources
> *   Standardize service offerings with a service catalogue
> *   Assists in determining the cost of delivering services
>
> **Workflow Automation**
>
> *   Service Modeling across the entire service lifecycle
> *   Workflow automation from approvals provisioning, through de-provisioning
> *   Automatically sends email notifications and approval requests Lastly here is a snapshot of the application from "

[VMware Service Manager 9 - Asset Management](http://www.slideshare.net/khanyasmin/vmware-service-manager-9-asset-management)":

![vm-serv-mana-sub-request](https://github.com/elatov/uploads/raw/master/2012/09/vm-serv-mana-sub-request.png)

Lastly you can use the 'Asset Tag' option for a VM to keep track of VMs manually. You can also use PowerCLI to look for VMs with certain tag as well. VMware Blog "[Objective 2.4](http://blogs.vmware.com/vsphere/2012/03/acessing-virtual-machine-advanced-settings.html)

### Based on the logical design, identify and implement release management technologies, such as Update Manager.

From "[VMware vCenter Update Manager 5.0 Performance and Best Practices](http://www.vmware.com/techpapers/2011/vmware-vcenter-update-manager-50-performance-and-10208.html)":

> VMware vCenter™ Update Manager (also known as VUM) provides a patch management framework for VMware vSphere®. IT administrators can use it to patch and upgrade:
>
> *   VMware ESX and VMware ESXi™ hosts
> *   VMware Tools and virtual hardware for virtual machines
> *   Virtual appliances.
>
> ...
> ...
>
> **Update Manager Server Host Deployment**
> There are three Update Manager server host deployment models where:
>
> *   Model 1 - vCenter Server and the Update Manager server share both a host and a database instance.
> *   Model 2 -  Recommended for data centers with more than 300 virtual machines or 30 ESX/ESXi hosts. In this model, the vCenter server and the Update Manager server still share a host, but use separate database instances.
> *   Model 3 - Recommended for data centers with more than 1,000 virtual machines or 100 ESX/ESXi hosts. In this model, the vCenter server and the Update Manager server run on different hosts, each with its own database instance.
>
> ...
> ...
>
> **Performance Tips**
>
> *   Separate the Update Manager database from the vCenter database when there are 300+ virtual machines or 30+ hosts.
> *   Separate both the Update Manager server and the Update Manager database from the vCenter Server system and the vCenter Server database when there are 1000+ virtual machines or 100+ hosts.
> *   Make sure the Update Manager server host has at least 2GB of RAM to cache frequently used patch files in memory.
> *   Allocate separate physical disks for the Update Manager patch store and the Update Manager database.

Use VUM depending on the size of your environment. Also to determine the size of the database necessary for VUM check out "[VMware vSphere Update Manager Database Sizing Estimator](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-update-manager-50-sizing-estimator.xls)". VUM is it's own product and it will definitely add more management over head. However if you have over 30 hosts then it will definitely be worth setting it up and using for patching your vSphere environment.

On top of that there is a Update Manager Download Service, from "[Installing and Administering VMware vSphere Update Manager 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-update-manager-50-install-administration-guide.pdf)":

> **Installing, Setting Up, and Using Update Manager Download Service**
> VMware vSphere Update Manager Download Service (UMDS) is an optional module of Update Manager. UMDS downloads upgrades for virtual appliances, patch metadata, patch binaries, and notifications that would not otherwise be available to the Update Manager server.
>
> For security reasons and deployment restrictions, vSphere, including Update Manager, might be installed in a secured network that is disconnected from other local networks and the Internet. Update Manager requires access to patch information to function properly. In such an environment, you can install UMDS on a computer that has Internet access to download upgrades, patch binaries, and patch metadata, and then export the downloads to a portable media drive so that they become accessible to the Update Manager server.
>
> In a deployment where the machine on which Update Manager is installed has no Internet access, but is connected to a server that has Internet access, you can automate the export process and transfer files from UMDS to the Update Manager server by using a Web server on the machine on which UMDS is installed.
>
> UMDS 5.0 supports patch recalls and notifications. A patch is recalled if the released patch has problems or potential issues. After you download patch data and notifications with UMDS, and export the downloads so that they become available to the Update Manager server, Update Manager deletes the recalled patches and displays the notifications on the Update Manager Notifications tab.

This helps out if you have a secure environment and your VUM service and(or) hosts don't have access to internet. You can then setup UMDS on another network and then export the repository to a file or over the network. You can then configure the VUM service to use that repository, from "[Installing and Administering VMware vSphere Update Manager 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-update-manager-50-install-administration-guide.pdf)":

> **Configuring the Update Manager Download Sources**
> You can configure the Update Manager server to download patches and extensions for ESX/ESXi hosts or upgrades for virtual appliances either from the Internet or from a shared repository of UMDS data. You can also import patches and extensions for ESX/ESXi hosts manually from a ZIP file.
>
> If your deployment system is connected to the Internet, you can use the default settings and links for downloading upgrades, patches, and extensions to the Update Manager repository. You can also add URL addresses to download virtual appliance upgrades or third-party patches and extensions. Third-party patches and extensions are applicable only to hosts that are running ESX/ESXi 4.0 and later.

You can also use PowerCLI to automate testing and download of patches. Check out the VMware Blog "[Now Available: PowerCLI cmdlets for vCenter Update Manager!](http://blogs.vmware.com/PowerCLI/2010/03/now-available-powercli-cmdlets-for-vcenter-update-manager.html)".

If you don't want to use VUM because you don't have a big environment there are alternatives. First you can create your own custom image with Image Builder. For more information check out the VMware blog "[VMware vSphere 5.0 Evaluation Guide Volume One](http://blogs.vmware.com/vsphere/2012/04/using-the-vsphere-esxi-image-builder-cli.html)". From that document, here is a good image that depicts Image Builder:

![image_builder](https://github.com/elatov/uploads/raw/master/2012/09/image_builder.png).

You can also just use powerCLI, vCLI, vMA, or esxcli to install patches manually. All of the examples are listed in VMware blog "[Quickest Way to Patch an ESX/ESXi Using the Command-line](http://blogs.vmware.com/vsphere/2012/02/quickest-way-to-patch-an-esxesxi-using-the-command-line.html)". From the blog:

> Here is an example of using the local esxcli utility for an ESXi 5.0 host. The patch bundle needs to be uploaded to ESXi host using scp or winSCP and then specifying the full path on the command-line:
>
>     $ esxcli software vib install –depot=/vmfs/volumes/datastore1/ESXi500-201112001.zip
>
>
> Here is an example of using the remote esxcli utility for an ESXi 5 host, you will need to specify the ESXi host using the –server parameter and –username/–password for remote authenication. You may choose to leave off –password and you will be prompted to enter your credentials. The patch bundle needs to be uploaded to ESXi host using scp/winSCP or vCLI’s vifs utility and then specifying the full path on the command-line:
>
>     $ vifs –server [ESXI-FQDN] –username [USERNAME] -p ESXi500-201112001.zip "[datastore1] ESXi500-201112001.zip"
>     $ esxcli –server [ESXI-FQDN] –username [USERNAME] software vib install –depot=/vmfs/volumes/datastore1/ESXi500-201112001.zip
>
>
> Here is an example of using Install-VMHostPatch utility for an ESXi host:
>
>     Get-VMHost ESXI-FQDN | Set-VMHost -State Maintenance
>     $DS = Get-VMHost ESXI-FQDN | Get-Datastore datastore1
>     Copy-DatastoreItem C:\tmp\ESXi500-201112001\ $DS.DatastoreBrowserPath -Recurse
>     Get-VMHost ESX-FQDN | Install-VMHostPatch -Hostpath "/vmfs/volumes/datastore1/ESXi500-201112001/metadata.zip"
>

With all of those options you can choose what is best for the customer. I think the size of the environment is the biggest factor in that decision.

### Determine appropriate host and virtual machine deployment options

For hosts, you have a couple of options:

*   You can use PXE to boot Hosts
*   You can install using a scripted install
*   You can use Image Builder as mentioned above
*   You can use Auto Deploy to PXE boot
*   You can just install from iso

From "vSphere Installation and Setup vSphere 5.0":

> **PXE Booting the ESXi Installer**
> You use the preboot execution environment (PXE) to boot a host and launch the ESXi installer from a network interface.
>
> ESXi 5.0 is distributed in an ISO format that is designed to install to flash memory or to a local hard drive. You can extract the files and boot using PXE.
>
> PXE uses DHCP and Trivial File Transfer Protocol (TFTP) to boot an operating system over a network.
>
> PXE booting requires some network infrastructure and a machine with a PXE-capable network adapter. Most machines that are capable of running ESXi have network adapters that are able to PXE boot.
>
> ...
> ...
>
> ![pxe-boot-esxi](https://github.com/elatov/uploads/raw/master/2012/09/pxe-boot-esxi.png)

After that the paper goes into a step by step process on how to set that. From the same document, regarding scripted installs:

> **Installing, Upgrading, or Migrating Hosts Using a Script**
> You can quickly deploy ESXi hosts using scripted, unattended installations or upgrades. Scripted installations, upgrades, or migrations provide an efficient way to deploy multiple hosts.
>
> The installation or upgrade script contains the installation settings for ESXi. You can apply the script to all hosts that you want to have a similar configuration.
>
> For a scripted installation, upgrade, or migration, you must use the supported commands to create a script and edit the script to change settings that are unique for each host.
>
> The installation or upgrade script can reside in one of the following locations:
>
> *   FTP
> *   HTTP/HTTPS
> *   NFS
> *   USB flash drive
> *   CDROM

You basically boot from your media (cd or usb) and then enter the Kickstart file location. You can also modify the ISO to contain your custom kickstart file as well. All of the information is included in the above paper.

Now for Auto Deploy, from the same document:

> **vSphere Auto Deploy ESXi Installation Option**
> With the vSphere Auto Deploy ESXi Installation, you can provision and reprovision large numbers of ESXi hosts efficiently with vCenter Server.
>
> Using the Auto Deploy feature, vCenter Server loads the ESXi image directly into the host memory. Auto Deploy does not store the ESXi state on the host disk. vCenter Server stores and manages ESXi updates and patching through an image profile, and, optionally, the host configuration through a host profile. You can create image profiles with ESXi Image Builder CLI, and host profiles using the vSphere Client
>
> ...
> ...
>
> **Understanding vSphere Auto Deploy**
> vSphere Auto Deploy can provision hundreds of physical hosts with ESXi software. You can specify the image to deploy and the hosts to provision with the image. Optionally, you can specify host profiles to apply to the hosts, and a vCenter Server location (folder or cluster) for each host.
>
> **Introduction to Auto Deploy**
> When you start a physical host set up for Auto Deploy, Auto Deploy uses a PXE boot infrastructure in conjunction with vSphere host profiles to provision and customize that host. No state is stored on the host itself, instead, the Auto Deploy server manages state information for each host.
>
> **State Information for ESXi Hosts**
> Auto Deploy stores the information for the ESXi hosts to be provisioned in different locations. Information about the location of image profiles and host profiles is initially specified in the rules that map machines to image profiles and host profiles. When a host boots for the first time, the vCenter Server system creates a corresponding host object and stores the information in the database.
>
> ...
> ...
>
> ![auto-deploy-architecture](https://github.com/elatov/uploads/raw/master/2012/09/auto-deploy-architecture.png)

Also here is boot process of Auto Deploy for first time and then the subsequent boots:

> ![auto-deploy-fb](https://github.com/elatov/uploads/raw/master/2012/09/auto-deploy-fb.png)
>
> and
>
> ![auto-deploy-sb](https://github.com/elatov/uploads/raw/master/2012/09/auto-deploy-sb.png)

Now for Image builder, from the same document:

> **Customizing Installations with ESXi Image Builder CLI**
> You can use ESXi Image Builder CLI to create ESXi installation images with a customized set of updates, patches, and drivers.
>
> ESXi Image Builder CLI is a PowerShell CLI command set that you can use to create an ESXi installation image with a customized set of ESXi updates and patches. You can also include third-party network or storage drivers that are released between vSphere releases.
>
> You can deploy an ESXi image created with Image Builder in either of the following ways:
>
> *   By burning it to an installation DVD.
> *   Through vCenter Server, using the Auto Deploy feature

The simple way, from the same document:

> **Interactive ESXi Installation**
> Interactive installations are recommended for small deployments of fewer than five hosts. You boot the installer from a CD or DVD, from a bootable USB device, or by PXE booting the installer from a location on the network. You follow the prompts in the installation wizard to install ESXi to disk.

Depending on the environment, you can choose which way to go. Like mentioned in the above article, if you have about 5 hosts, then just download the ISO and install ESXi on it. Each install takes about 15 minutes, and if you have Remote Access (ie DRAC or ILO) then you don't have even have to be in front of the machine. If there had been updates since the ISO install, then definitely use Image Builder to insert the updates into the ISO and use that iSO to install ESXi on all the hosts. Now if you are doing a lot of installs (ie 10-20), then instead of clicking through the installer 20 times, create a kickstart file and use it for the installs. If you want to, create 20 scripts (all you would have to change, is the IP setting) and host them all. Then boot all the hosts and point to the appropriate kickstart script. This will definitely save a bunch of time.

Kickstart is helpful and it works if you are just doing a bunch of installs in the beginning and then you are done. Now if you plan to add new hosts pretty frequently then PXE boot might be the way. With PXE boot, additional servers are required but you just have to set them up once. So setup the necessary servers (ie DHCP, TFTP, and Web) and then just set your ESXi hosts to boot from the NIC and you are done. Very automated process but does require some admin over head.

Lastly there is the Auto Deploy, if you plan to deploy 100 hosts and if you don't want to depend on your local disk, this is the way to go. It also auto adds the host to vCenter and each host contains an answer file to make it unique. So this is almost a 100% automated process to get a host up and running in your environment. It does require knowledge of Image Builder and PowerCLI, so admin over head goes way up (when stuff breaks). It's a very good idea but unfortunately this is a single point of failure. If your Auto deploy server is down and you reboot your hosts, none of them will come back (uh oh).

For VMs, you have a couple of options as well:

*   You can create a template (or OVF) and then deploy from there
*   You can use Citrix PVS to PXE boot VMs
*   You can just use PXE to boot VMs
*   You can deploy one VM at a time and have an ISO repository from which you can install the necessary OS

From "[vSphere Virtual Machine Administration ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-virtual-machine-admin-guide.pdf)":

> **About Provisioning Virtual Machines**
> VMware provides several methods to provision vSphere virtual machines. The optimal method for your environment depends on factors such as the size and type of your infrastructure and the goals that you are trying to achieve.
>
> Create a single virtual machine if no other virtual machines in your environment have the requirements you are looking for, such as a particular operating system or hardware configuration. For example, you might need a virtual machine that is configured only for testing purposes. You can also create a single virtual machine and install an operating system on it, then use that virtual machine as a template to clone other virtual machines from.
>
> Deploy and export virtual machines, virtual appliances, and vApps stored in Open Virtual Machine Format (OVF) to use a preconfigured virtual machine. A virtual appliance is a prebuilt virtual machine that typically has an operating system and other software already installed. You can deploy virtual machines from local file systems, such as local disks (such as C:), removable media (such as CDs or USB keychain drives), and shared network drives.
>
> Create a template to deploy multiple virtual machines from. A template is a master copy of a virtual machine that you can use to create and provision virtual machines. Templates can be a real time saver. If you have a virtual machine that you want to clone frequently, make that virtual machine a template.
>
> Cloning a virtual machine can save time if you are deploying many similar virtual machines. You can create, configure, and install software on a single virtual machine and clone it multiple times, rather than creating and configuring each virtual machine individually.

For PXE booting, from the same document:

> **Using PXE with Virtual Machines**
> You can start a virtual machine from a network device and remotely install a guest operating system using a Preboot Execution Environment (PXE). You do not need the operating system installation media. When you turn on the virtual machine, the virtual machine detects the PXE server.
>
> PXE booting is supported for Guest Operating Systems that are listed in the VMware Guest Operating System Compatibility list and whose operating system vendor supports PXE booting of the operating system.
>
> The virtual machine must meet the following requirements:
>
> *   Have a virtual disk without operating system software and with enough free disk space to store the intended system software.
> *   Have a network adapter connected to the network where the PXE server resides.

Also from the same document:

> **Install a Guest Operating System from Media**
> You can install a guest operating system from a CD-ROM or from an ISO image. Installing from an ISO image is typically faster and more convenient than a CD-ROM installation.

Lastly for Citrix PVS check out "[Design Considerations for Virtualizing Citrix Provisioning Services](http://support.citrix.com/servlet/KbServlet/download/26450-102-665163/Design%20Considerations%20for%20vPVS%20v2.1.pdf)". It basically allows you to provision VMs quickly and store windows Profiles on the provisioning server. This way you don't have to depend on local media.

Each option has it's ups and downs. If you decide to PXE boot, with Citrix PVS or any other third party software, then make sure you have a dedicated person to manage that. And again this will be your single point of failure. If the PXE boot server is down then VMs won't boot. Or if your PVS server is lost, then all of the Windows profiles are lost as well. But this does allow for fast provisioning, so if a new windows patch comes out, then update the base image and push it to you clients. Next time the VM is is rebooted, the system components are updates and the users profiles and their settings are preserved. Now with regular installation you will have to update each VM manually.

Templates help out tremendously cause you don't want to install each of your VMs from scratch and re-setup your settings. With templates or OVFs, install the OS that you want, customize it as you desire and then convert it to a template. Next time you need a VM with that OS just deploy from template. This will definitely save time. If you are just setting up a one time VM, then make sure you an ISO repository with the desired OSes, then for those one off VMs, just boot from the ISO and do an installation as necessary.

### Based on the logical design identify and implement event, incident and problem management technologies.

There is a great white paper on this, "[Proactive Incident and Problem Management](http://www.vmware.com/files/pdf/services/VMware-Proactive-Incident-Whitepaper.pdf)", from that white paper:

> **Executive Summary**
> As the IT infrastructure has grown, the approach to managing incidents and problems has evolved, from help desk to tiered support to integrated management. However, these approaches have all been reactive, essentially devising better and faster ways to fix broken components. The cloud makes a reactive approach untenable for several reasons:
>
> 1.  The typical enterprise data center has far too many objects to manage with spreadsheets and configuration management databases (CMDBs).
> 2.  Virtualization—a key enabling technology for the cloud—abstracts the physical infrastructure, making it difficult to identify the physical component responsible for a service outage or performance problem.
> 3.  Public cloud services, an essential element of a hybrid cloud strategy, hide the details of the physical implementation from customers.
>
> A proactive approach to incident and problem management is an essential capability that allows organizations to realize the full range of benefits—efficiency, agility, and reliability—from cloud computing. Proactive management relies on intelligent analytics to automate control of the cloud infrastructure. Correlating metrics from a number of tools, analytics can identify trends that help to pinpoint potential problems early and allow corrective action before problems occur. Intelligent analytics assure the quality of business services, improve the user experience, and increase utilization of platform resources. Unlike the reactive system, IT can now handle exceptions and potential problems through regular maintenance cycles in an orderly and predictable way.
>
> Migrating to a proactive system requires a carefully orchestrated plan that includes a pilot program and phased cut over. There are organizational considerations involved in proactivity, including the establishment of a Cloud Infrastructure Operations Center of Excellence and changes to individual job functions. These changes must be carefully planned and effectively communicated across the organization to ensure a successful transition to a proactive system.

The paper talks about being pro-active, defining roles for different layers, and having integrated management. All of these thing are true and there are a lot of third party application that already do this. I talked about these in [VMware Service Manager: Implementing Incident Problem Management](/2012/08/vcap5-dcd-objective-2-4-build-manageability-requirements-into-the-logical-design/)" class data sheet:

> **Course Overview**
> VMware® Service Manager (VSM) is a service management tool for managing and controlling customer calls received through a service desk.
>
> This three-day course is suitable for customers implementing the service desk module of VSM and covers the operational and administrative functions of the service desk.
>
> ...
> ...
>
> **Objectives:**
>
> *   Log and action a call and IPK workflow rules
> *   Link and clone calls; find related calls
> *   Manage calls and call queues; search for calls
> *   Setup and use call delegation
> *   Create reports, configure monitors, and setup dashboards
> *   Configure global settings for and define key fields within IPK management
> *   Set up officer roles and manage officer records
> *   Configure IPK workflow rules and forums, customer portal and proactive problem management, and partitioning and time zones
> *   Setup messaging and edit email templates
> *   Administer officer delegation and create call templates and officer scripts
> *   Define service commitments, escalation, and breach events
> *   Create matrix templates to control escalations
> *   Create and administer service level agreements
> *   Describe the business rules applied to Service Level Management

So if the customer is big enough, ask them to go through the above class so they can have a staff that will be dedicated to keep track of problem reports. If the class and the product is too much for the customer then find a third party application that will suite the customer needs.

### Based on the logical design, identify and implement logging, monitoring and reporting technologies.

From "[vSphere Monitoring and Performance vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf)":

> **Monitoring Events, Alarms, and Automated Actions**
> vSphere includes a user-configurable events and alarms subsystem. This subsystem tracks events happening throughout vSphere and stores the data in log files and the vCenter Server database. This subsystem also enables you to specify the conditions under which alarms are triggered. Alarms can change state from mild warnings to more serious alerts as system conditions change, and can trigger automated alarm actions. This functionality is useful when you want to be informed, or take immediate action, when certain events or conditions occur for a specific inventory object, or group of objects.
>
> **Events** Events are records of user actions or system actions that occur on objects in vCenter Server or on a host. Actions that might be recordered as events include, but are not limited to, the following examples:
>
> *   A license key expires
> *   A virtual machine is powered on
> *   A user logs in to a virtual machine
> *   A host connection is lost
>
> Event data includes details about the event such as who generated it, when it occurred, and what type of event it is. There are three types of events:
>
> *   Information
> *   Warning
> *   Error
>
> Event data is displayed in Tasks and Events tab for the selected inventory object.
>
> **Alarms**
> Alarms are notifications that are activated in response to an event, a set of conditions, or the state of an inventory object. An alarm definition consists of the following elements:
>
> *   Name and description - Provides an identifying label and description.
> *   Alarm type - Defines the type of object that will be monitored.
> *   Triggers - Defines the event, condition, or state that will trigger the alarm and defines the notification severity.
> *   Tolerance thresholds (Reporting) - Provides additional restrictions on condition and state triggers thresholds that must be exceeded before the alarm is triggered.
> *   Actions - Defines operations that occur in response to triggered alarms. VMware provides sets of predefined actions that are specific to inventory object types.
>
> Alarms have the following severity levels:
>
> *   Normal – green
> *   Warning – yellow
> *   Alert – red
>
> Alarm definitions are associated with the object selected in the inventory. An alarm monitors the type of inventory objects specified in its definition.
>
> For example, you might want to monitor the CPU usage of all virtual machines in a specific host cluster. You can select the cluster in the inventory, and add a virtual machine alarm to it. When enabled, that alarm will monitor all virtual machines running in the cluster and will trigger when any one of them meets the criteria defined in the alarm. If you want to monitor a specific virtual machine in the cluster, but not others, you would select that virtual machine in the inventory and add an alarm to it. One easy way to apply the same alarms to a group of objects is to place those objects in a folder and define the alarm on the folder.
>
> **Alarm Actions**
> Alarm actions are operations that occur in response to the trigger. For example, you can have an email notification sent to one or more administrators when an alarm is triggered.

Setup Alarms for critical events and make sure you set an action to email the VMware admins. From the same document:

> **Monitoring Networked Devices with SNMP and vSphere**
> Simple Network Management Protocol (SNMP) allows management programs to monitor and control a variety of networked devices.
>
> Managed systems run SNMP agents, which can provide information to a management program in at least one of the following ways:
>
> *   In response to a GET operation, which is a specific request for information from the management system.
> *   By sending a trap, which is an alert sent by the SNMP agent to notify the management system of a particular event or condition.
>
> Optionally, you can configure ESXi hosts to convert CIM indications to SNMP traps, allowing this information to be received by SNMP monitoring systems.
>
> Management Information Base (MIB) files define the information that can be provided by managed devices. The MIB files contain object identifiers (OIDs) and variables arranged in a hierarchy.
>
> vCenter Server and ESXi have SNMP agents. The agent provided with each product has differing capabilities.
>
> **Using SNMP Traps with vCenter Server**
> The SNMP agent included with vCenter Server can be used to send traps when the vCenter Server system is started and when an alarm is triggered on vCenter Server. The vCenter Server SNMP agent functions only as a trap emitter and does not support other SNMP operations, such as GET.
>
> The traps sent by vCenter Server are typically sent to other management programs. You must configure your management server to interpret the SNMP traps sent by vCenter Server.
>
> To use the vCenter Server SNMP traps, configure the SNMP settings on vCenter Server and configure your management client software to accept the traps from vCenter Server.
>
> ...
> ...
>
> **Configure SNMP for ESXi**
> ESXi includes an SNMP agent embedded in hostd that can both send traps and receive polling requests such as GET requests. This agent is referred to as the embedded SNMP agent.
>
> **Configure the SNMP Agent to Send Traps**
> You can use the ESXi embedded SNMP agent to send virtual machine and environmental traps to management systems. To configure the agent to send traps, you must specify a target address and community. To send traps with the SNMP agent, you must configure the target (receiver) address, community, and an optional port. If you do not specify a port, the SNMP agent sends traps to UDP port 162 on the target management system by default.
>
> **Configure the SNMP Agent for Polling**
> If you configure the ESXi embedded SNMP agent for polling, it can listen for and respond to requests from SNMP management client systems, such as GET requests.
>
> By default, the embedded SNMP agent listens on UDP port 161 for polling requests from management systems. You can use the vicfg-snmp command to configure an alternative port. To avoid conflicting with other services, use a UDP port that is not defined in /etc/services.

If there is already a tool in place in the environment that does SNMP polling (ie Nagios, SolarWinds, or Cacti) then definitely add vCenter and ESX SNMP traps to go to that software. A lot of networking admins want to know whenever a node is down on the network, and SNMP is definitely the best way to keep on eye on that. If there is no such setup in place then Alarms might be okay, it just depends on how quickly they want to get notified of the issue. Also alarms are not as dependable. If vCenter goes down, how is it going to fire an alarm? So having an external application polling with SNMP is definitely more reliable.

Lastly, definitely setup a syslog server. Now with vSphere 5, there is a product called "Syslog Collector" and can be installed along side of vCenter. More information can be seen in VMware Blog "Setting up the ESXi Syslog Collector", from the blog:

> Syslog collector also addresses the issue of an Auto Deployed host not having a local disk. With no local disk the log files are stored on a ramdisk, which means each time the server boots the logs are lost. Not having persistent logs can complicate troubleshooting. Use the syslog collector to capture the ESXi host’s log on a network server.
>
> Just like with the dump collector the syslog collector is very easy to install and configure. The syslog collector is bundled with the vCenter Server Appliance (VCSA) and requires no extra setup (by default the logs are stored in /var/log/remote/). To install the syslog collector on Windows simply load the vCenter installation media, launch autorun and from the main install menu choose “Syslog Collector”.

After that, the blog shows you snapshots of the installation process. If there is already an syslog server in place, then configure all of your ESXi host to log to the syslog server. From the same VMware blog:

> Once the syslog collector has been installed the next step is to simply configure the ESXi hosts to use the server as its loghost:
>
>     ~# esxcli system syslog config set –loghost=x.x.x.x
>     ~# esxcli system syslog reload
>
>
> (you can also set the loghost from the vSphere client by going to configuration -> advanced settings -> syslog -global)

Syslog will help you in any troubleshooting scenarios, and personally I think it should be configured regardless of the amount of hosts that you have.

