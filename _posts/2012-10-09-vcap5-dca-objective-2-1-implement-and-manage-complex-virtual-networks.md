---
title: VCAP5-DCA Objective 2.1 – Implement and Manage Complex Virtual Networks
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/
dsq_thread_id:
  - 1409816398
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify common virtual switch configurations

From <a href="http://www.vmware.com/files/pdf/virtual_networking_concepts.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/virtual_networking_concepts.pdf']);">VMware Virtual Networking Concepts</a>

> **Load Balancing**  
> Load balancing allows you to spread network traffic from virtual machines on a virtual switch across two or more physical Ethernet adapters, giving higher throughput than a single physical adapter could provide. When you set NIC teaming policies, you have the following options for load balancing:
> 
> **Route based on the originating virtual switch port ID**  
> Choose an uplink based on the virtual port where the traffic entered the virtual switch. This is the default configuration and the one most commonly deployed.
> 
> When you use this setting, traffic from a given virtual Ethernet adapter is consistently sent to the same physical adapter unless there is a failover to another adapter in the NIC team. Replies are received on the same physical adapter as the physical switch learns the port association.
> 
> This setting provides an even distribution of traffic if the number of virtual Ethernet adapters is greater than the number of physical adapters.
> 
> A given virtual machine cannot use more than one physical Ethernet adapter at any given time unless it has multiple virtual adapters.
> 
> This setting places slightly less load on the ESX Server host than the MAC hash setting.
> 
> Note: If you select either srcPortID or srcMAC hash, you should not configure the physical switch ports as any type of team or bonded group.
> 
> **Route based on source MAC hash**  
> Choose an uplink based on a hash of the source Ethernet MAC address.
> 
> When you use this setting, traffic from a given virtual Ethernet adapter is consistently sent to the same physical adapter unless there is a failover to another adapter in the NIC team.
> 
> Replies are received on the same physical adapter as the physical switch learns the port association.
> 
> This setting provides an even distribution of traffic if the number of virtual Ethernet adapters is greater than the number of physical adapters.
> 
> A given virtual machine cannot use more than one physical Ethernet adapter at any given time unless it uses multiple source MAC addresses for traffic it sends.
> 
> **Route based on IP hash**  
> Choose an uplink based on a hash of the source and destination IP addresses of each packet. (For non-IP packets, whatever is at those offsets is used to compute the hash.)
> 
> Evenness of traffic distribution depends on the number of TCP/IP sessions to unique destinations. There is no benefit for bulk transfer between a single pair of hosts.
> 
> You can use link aggregation — grouping multiple physical adapters to create a fast network pipe for a single virtual adapter in a virtual machine.
> 
> When you configure the system to use link aggregation, packet reflections are prevented because aggregated ports do not retransmit broadcast or multicast traffic.
> 
> The physical switch sees the client MAC address on multiple ports. There is no way to predict which physical Ethernet adapter will receive inbound traffic.
> 
> All adapters in the NIC team must be attached to the same physical switch or an appropriate set of stacked physical switches. (Contact your switch vendor to find out whether 80.ad teaming is supported across multiple stacked chassis.) That switch or set of stacked switches must be 80.ad-compliant and configured to use that link-aggregation standard in static mode (that is, with no LACP). All adapters must be active. You should make the setting on the virtual switch and ensure that it is inherited by all port groups within that virtual switch

And more from the same document:

> **Failover Configurations**  
> When you configure network failover detection you specify which of the following methods to use for failover detection:
> 
> **Link Status only **  
> Relies solely on the link status provided by the network adapter. This detects failures, such as cable pulls and physical switch power failures, but it cannot detect configuration errors, such as a physical switch port being blocked by spanning tree or misconfigured to the wrong VLAN or cable pulls on the other side of a physical switch.
> 
> **Beacon Probing**  
> Sends out and listens for beacon probes — Ethernet broadcast frames sent by physical adapters to detect upstream network connection failures — on all physical Ethernet adapters in the team, as shown in Figure . It uses this information, in addition to link status, to determine link failure. This detects many of the failures mentioned above that are not detected by link status alone, however beacon  
> probing should not be used as a substitute for a robust redundant Layer  network design. Beacon probing is most useful to detect failures in the closest switch to the ESX Server hosts, where the failure does not cause a link-down event for the host.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/beacon_probes.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/beacon_probes.png']);"><img class="alignnone size-full wp-image-3951" title="beacon_probes" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/beacon_probes.png" alt="beacon probes VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " width="305" height="772" /></a>

And the last section from the document:

> **Layer 2 Security Features**  
> The virtual switch has the ability to enforce security policies to prevent virtual machines from impersonating other nodes on the network. There are three components to this feature.
> 
> *   **Promiscuous mode** is disabled by default for all virtual machines. This prevents them from seeing unicast traffic to other nodes on the network.
> *   **MAC address change** lockdown prevents virtual machines from changing their own unicast addresses. This also prevents them from seeing unicast traffic to other nodes on the network, blocking a potential security vulnerability that is similar to but narrower than promiscuous mode.
> *   **Forged transmit** blocking, when you enable it, prevents virtual machines from sending traffic that appears to come from nodes on the network other than themselves

### Configure SNMP

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples</a>:

> To configure SNMP communities,run vicfg-snmp -c, specifying a comma‐separated list of communities. For example:
> 
> [code]  
> vicfg-snmp -c public, internal  
> [/code]

From the same document:

> **Configuring the SNMP Agent to Send Traps**  
> You can use the SNMP agent embedded in ESXi to send virtual machine and environmental traps to management systems. To configure the agent to send traps, you must specify a target (receiver) address, the community, and an optional port. If you do not specify a port, the SNMP agent sends traps to UDP port 162 on the target management system by default.
> 
> **To configure a trap destination**  
> 1 Make sure a community is set up.
> 
> [code]  
> vicfg-snmp --show  
> Current SNMP agent settings:  
> Enabled: 1  
> UDP port: 161  
> Communities: public  
> Notification targets:  
> [/code]
> 
> 2 Run vicfg-snmp &#8211;target with the target address, port number, and community.
> 
> [code]  
> vicfg-snmp -t target.example.com@163/public  
> [/code]
> 
> Each time you specify a target with this command, the settings you specify overwrite all previously specified settings. To specify multiple targets, separate them with a comma.
> 
> You can change the port that the SNMP agent sends data to on the target using the &#8211;targets option. That port is UDP 162 by default.
> 
> 3 (Optional) Enable the SNMP agent if it is not yet running.
> 
> [code]  
> vicfg-snmp --enable  
> [/code]
> 
> 4 (Optional) Send a test trap to verify that the agent is configured correctly.
> 
> [code]  
> vicfg-snmp --test  
> [/code]
> 
> The agent sends a warmStart trap to the configured target.

And the last section:

> **Configuring the SNMP Agent for Polling**  
> If you configure the ESXi embedded SNMP agent for polling, it can listen for and respond to requests such as GET requests from SNMP management client systems.
> 
> By default, the embedded SNMP agent listens on UDP port 161 for polling requests from management systems. You can use the vicfg-snmp command to configure an alternative port. To avoid conflicts with other services, use a UDP port that is not defined in /etc/services.
> 
> **To configure the SNMP agent for polling**  
> 1 Run vicfg-snmp &#8211;target with the target address, port number, and community.
> 
> [code]  
> vicfg-snmp -c public -t target.example.com@163/public  
> [/code]
> 
> Each time you specify a target with this command, the settings you specify overwrite all previously specified settings. To specify multiple targets, separate them with a comma.
> 
> You can change the port that the SNMP agent sends data to on the target by using the &#8211;targets option. That port is UDP 162 by default.
> 
> 2 (Optional) Specify a port for listening for polling requests.
> 
> [code]  
> vicfg-snmp -p  
> [/code]
> 
> 3 (Optional) If the SNMP agent is not enabled, enable it.
> 
> [code]  
> vicfg-snmp --enable  
> [/code]
> 
> 4 Run vicfg-snmp &#8211;test to validate the configuration.  
> The following example shows how the commands are run in sequence.
> 
> [code]  
> vicfg-snmp –c public –t example.com@162/private --enable  
> \# next validate your config by doing these things:  
> vicfg-snmp -–test  
> walk –v1 –c public esx-host  
> [/code] 

The above commands have to be run either from VMA or vCLI. If you don&#8217;t want to use any of those tools, you can do it manually. From this blog &#8220;<a href="http://thebashline.wordpress.com/2012/01/14/esxi-add-snmp/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://thebashline.wordpress.com/2012/01/14/esxi-add-snmp/']);">Esxi – Add SNMP</a>&#8220;:

> Log onto esxi CLI
> 
> [code]  
> vi /etc/vmware/snmp.xml  
> [/code]
> 
> Make the following changes detailed below
> 
> [xml]  
> <config>  
> <snmpSettings>  
> <communities>public</communities>  
> <enable>true</enable>  
> <port>161</port>  
> <targets>target.example.com@161 public</targets>  
> </snmpSettings>  
> </config>  
> [/xml]
> 
> Apply the changes by restarting the services:
> 
> [code]  
> services.sh restart  
> [/code]
> 
> The server should now be available to be polled via snmp. 

### Determine use cases for and applying VMware DirectPath I/O

This was covered in the previous section

### Migrate a vSS network to a Hybrid or Full vDS solution

From <a href="http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf']);">VMware vNetwork Distributed Switch: Migration and Configuration</a>

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/vss_to_dvs_migration.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/vss_to_dvs_migration.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/vss_to_dvs_migration.png" alt="vss to dvs migration VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="vss_to_dvs_migration" width="465" height="337" class="alignnone size-full wp-image-3960" /></a>

From the same document:

> **Step 1: Create a vDS**
> 
> vNetwork Distributed Switches are created at the Datacenter level in the vSphere environment. A datacenter is the primary container for inventory objects such as hosts and virtual machines. The starting point is shown below from a vSphere Client attached to a vCenter Server. In the example environment, the Datacenter is labeled Datacenter_09.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvs.png" alt="create dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="create_dvs" width="549" height="228" class="alignnone size-full wp-image-3961" /></a>
> 
> After creating the vDS, the Networking Inventory panel will show a dvSwitch (the default name is chosen here), and an Uplink Group for the uplinks (in this example, this was named dvswitch-DVUplinks-199). Note that both these new items can be renamed to conform to any local naming standards. 
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/after_creating_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/after_creating_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/after_creating_dvs.png" alt="after creating dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="after_creating_dvs" width="244" height="174" class="alignnone size-full wp-image-3962" /></a>
> 
> **Step 2: Create Distributed Virtual Port Groups on vDS to Match Existing or Required Environment**  
> In this step, a Distributed Virtual Port Groups on the vDS is created to match the existing environment and prepare the vDS for migration of the individual ports and Port Groups from the Standard Switches on each of the hosts.
> 
> **Creating the DV Port Groups**  
> 1. From the Network Inventory view, select the vDS. This is labeled dvSwitch in the example environment (see Figure 16). Then select New Port Group. This will bring up a Create Distributed Virtual Port Group panel.
> 
> The first panel in creating the dv-VM01 DV Port Group is shown in Figure 17. Note the number of ports. This defaults to 128 and is the number of ports that this DV port group will allow once created. As this DV Port Group will support VMs, it means up to 128 VMs can use this DV Port Group. Modify this to a higher number if you need to support more VMs within a single DV  
> Port Group. In this example environment, 128 ports are quite adequate.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvportgroup.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvportgroup.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/create_dvportgroup.png" alt="create dvportgroup VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="create_dvportgroup" width="444" height="240" class="alignnone size-full wp-image-3963" /></a>
> 
> **Step 3: Add host to vDS and migrate vmnics, Virtual Ports, and VM Networking**  
> In this step, the Standard Switch environment of one host is migrated to the vDS and DV Port Groups created in steps 1 and 2. The process is described below.  
> **Step 3a: Add Host to vDS**  
> 1. Switch to the Home > Inventory > Networking view  
> 2. Right click on the vDS and select Add Host. This is shown in Figure 19.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/add_host_to_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/add_host_to_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/add_host_to_dvs.png" alt="add host to dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="add_host_to_dvs" width="391" height="274" class="alignnone size-full wp-image-3964" /></a>
> 
> **Step 3b: Select Physical Adapters (vmnics)**  
> Next, select the host being migrated to vDS (esx09a.tml.local in this environment). For this example, all four vmnics are migrated from the Standard Switch on esx09a.tml.local to the vDS at one time. Refer to Figure 20.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/select_host_vmnics_to_migrate_to_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/select_host_vmnics_to_migrate_to_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/select_host_vmnics_to_migrate_to_dvs.png" alt="select host vmnics to migrate to dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="select_host_vmnics_to_migrate_to_dvs" width="580" height="244" class="alignnone size-full wp-image-3965" /></a>
> 
> **Step 3c: Migrate Virtual Adapters**  
> Now the virtual adapters on the Standard Switch with the DV Port Groups created in Step 2 need to be matched up. In this example, the Port Groups and DV Port Groups from Table 2 are matched up. Double check that the VLAN selected for the Management DVPort Group (dv-management in this example) matches that of the Service Console port (vswif0). Any mismatch or mistake with the service console definition could isolate the host and require ILO or console connection to restore connectivity. See Figure 21. 
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/select_Virtual_adapter_to_migrate_to_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/select_Virtual_adapter_to_migrate_to_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/select_Virtual_adapter_to_migrate_to_dvs.png" alt="select Virtual adapter to migrate to dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="select_Virtual_adapter_to_migrate_to_dvs" width="493" height="256" class="alignnone size-full wp-image-3966" /></a>
> 
> **Step 3d: Migrate Virtual Machine Networking**
> 
> Now the VMs can be migrated to the vDS. (The VMs on Port Groups VM01, VM02, and VM03 in this environment). Note that if you are migrating a number of hosts to a vDS, you can optionally leave this until last as you can migrate all Virtual Machine Networking for all hosts on the vDS at once. 
> 
> To begin the process:  
> 1. Right-click on the vDS from Home > Inventory > Networking panel and select Migrate Virtual Machine Networking from the list (see Figure 24).  
> 2. Select the source network from the standard switch and the destination network on the vDS. In this example, the VM01 is migrated to dv-VM01. Refer to Figure 25.  
> 3. Click on Show Virtual Machines. This will present a list of eligible VMs on the source network on the migrated host (or hosts).  
> 4. Select the VMs you wish to migrate (all of them in this case).  
> 5. Repeat for each of the remaining VM networking Port Groups.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/migrate_vms_to_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/migrate_vms_to_dvs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/migrate_vms_to_dvs.png" alt="migrate vms to dvs VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="migrate_vms_to_dvs" width="596" height="440" class="alignnone size-full wp-image-3967" /></a> 

That should be it.

### Configure vSS and vDS settings using command line tools

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples</a>:

> On ESXi 5.0, ifconfig information should be the information of the VMkernel NIC that attaches to the Management Network port group. You can retrieve information by using ESXCLI commands.
> 
> [code]  
> esxcli network ip interface list  
> esxcli network ip interface ipv4 get -n vmkX  
> esxcli network ip interface ipv6 get -n vmkX  
> esxcli network ip interface ipv6 address list  
> [/code]
> 
> For information corresponding to the Linux netstat command, use the following ESXCLI command.  
> [code]  
> esxcli network ip connection list  
> [/code]
> 
> List all virtual switches and associated port groups.  
> [code]  
> esxcli network vswitch standard list  
> [/code]
> 
> List the network policy settings (security policy, traffic shaping policy, and failover policy) for the virtual switch. The following commands are supported.
> 
> [code]  
> esxcli network vswitch standard policy failover get  
> esxcli network vswitch standard policy security get  
> esxcli network vswitch standard policy shaping get  
> [/code]
> 
> Add a virtual switch.  
> [code]  
> esxcli network vswitch standard add --vswitch-name=vSwitch42  
> [/code]
> 
> You can specify the number of port groups while adding the virtual switch. If you do not specify a value, the default value is used. The system‐wide port count cannot be greater than 4096.  
> [code]  
> esxcli network vswitch standard add --vswitch-name=vSwitch42 --ports=8  
> [/code]
> 
> Delete a virtual switch.  
> [code]  
> esxcli network vswitch standard remove --vswitch-name=vSwitch42  
> [/code]
> 
> Set the MTU for a vSwitch.  
> [code]  
> esxcli network vswitch standard set --mtu=9000 --vswitch-name=vSwitch1  
> [/code]
> 
> Set the CDP value for a vSwitch. You can set status to down, listen, advertise, or both.
> 
> [code]  
> esxcli network vswitch standard set --cdp-status=listen --vswitch-name=vSwitch1  
> [/code]
> 
> List port groups currently associated with a virtual switch.  
> [code]  
> esxcli network vswitch standard portgroup list  
> [/code]
> 
> Add a port group.  
> [code]  
> esxcli network vswitch standard portgroup add --portgroup-name=NAME --vswitch-name=vSwitch1  
> [/code]  
> Delete one of the existing port groups.  
> [code]  
> esxcli network vswitch standard portgroup remove --portgroup-name=NAME --vswitch-name=vSwitch1  
> [/code]
> 
> Connect a port group with an uplink adapter.  
> [code]  
> esxcli network vswitch standard portgroup policy failover set --active-uplinks=vmnic1,vmnic6,vmnic7  
> [/code]
> 
> Make some of the adapters standby instead of active.  
> [code]  
> esxcli network vswitch standard portgroup policy failover set --standby-uplinks=vmnic1,vmnic6,vmnic7  
> [/code]
> 
> Allow port groups to reach port groups located on other VLANs.  
> [code]  
> esxcli network vswitch standard portgroup set -p <pg_name> --vlan-id 4095  
> [/code] 
> 
> List all uplinks and information about each device.  
> [code]  
> esxcli network nic list  
> [/code]
> 
> Bring down one of the uplink adapters.  
> [code]  
> esxcli network nic down --nic-name=vmnic0  
> [/code]
> 
> Add a new VMkernel network interface.  
> [code]  
> esxcli network ip interface add --interface-name=vmkX-portgroup-name=PORTGROUP  
> [/code]
> 
> Configure the interface as an IPv4 interface. You must specify the IP address using &#8211;ip, the netmask, and the name. For the following examples, assume that VMSF‐VMK‐363 is a port group to which you want to add a VMkernel network interface.  
> [code]  
> esxcli network ip interface ipv4 set --ip=<ip_address> --netmask=255.255.255.0 --interface-name=vmkX  
> [/code]
> 
> List information about all VMkernel network interfaces on the system.  
> [code]  
> esxcli network ip interface list  
> [/code] 

From VMware KB <a href="http://kb.vmware.com/kb/1008127" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1008127']);">1008127</a>:

> These commands allow you to add or remove network cards (known as uplinks) to or from a vNetwork Distributed Switch (vDS):  
> [code]  
> esxcfg-vswitch -Q vmnic -V dvPort\_ID\_of_vmnic dvSwitch # unlink a DVS uplink  
> esxcfg-vswitch -P vmnic -V unused\_dvPort\_ID dvSwitch # add a DVS uplink  
> [/code]
> 
> To create an ESX Service Console management interface (vswif) and uplink it to the vDS, run the command:  
> [code]  
> esxcfg-vswif -a -i IP\_address -n Netmask -V dvSwitch -P DVPort\_ID vswif0  
> [/code]
> 
> Delete an existing VMkernel port from a vDS with the command:  
> [code]  
> esxcfg-vmknic -d -s DVswitchname -v virtual\_port\_ID  
> [/code]
> 
> To create a VMkernel port and attach it to the DVPort ID on a vDS, run the command:  
> [code]  
> esxcfg-vmknic -a -i IP\_address -n netmask -s DVswitchname -v virtual\_port_ID  
> [/code] 

### Analyze command line output to identify vSS and vDS configuration details

List your vSwitches:

[code]  
~ # esxcli network vswitch standard list  
vSwitch0  
Name: vSwitch0  
Class: etherswitch  
Num Ports: 128  
Used Ports: 3  
Configured Ports: 128  
MTU: 1500  
CDP Status: listen  
Beacon Enabled: false  
Beacon Interval: 1  
Beacon Threshold: 3  
Beacon Required By:  
Uplinks: vmnic0  
Portgroups: Management Network

vSwitch1  
Name: vSwitch1  
Class: etherswitch  
Num Ports: 128  
Used Ports: 3  
Configured Ports: 128  
MTU: 1500  
CDP Status: listen  
Beacon Enabled: false  
Beacon Interval: 1  
Beacon Threshold: 3  
Beacon Required By:  
Uplinks: vmnic1  
Portgroups: ISCSI_1

vSwitch2  
Name: vSwitch2  
Class: etherswitch  
Num Ports: 128  
Used Ports: 2  
Configured Ports: 128  
MTU: 1500  
CDP Status: listen  
Beacon Enabled: false  
Beacon Interval: 1  
Beacon Threshold: 3  
Beacon Required By:  
Uplinks: vmnic3  
Portgroups: VM_Net

vSwitch3  
Name: vSwitch3  
Class: etherswitch  
Num Ports: 128  
Used Ports: 3  
Configured Ports: 128  
MTU: 1500  
CDP Status: listen  
Beacon Enabled: false  
Beacon Interval: 1  
Beacon Threshold: 3  
Beacon Required By:  
Uplinks: vmnic2  
Portgroups: vMotion  
[/code]

List your PortGroups:

[code]  
~ # esxcli network vswitch standard portgroup list  
Name Virtual Switch Active Clients VLAN ID  
\---\---\---\---\---\--- \---\---\---\---\-- -\---\---\---\---\- --\-----  
ISCSI_1 vSwitch1 1 0  
Management Network vSwitch0 1 0  
VM_Net vSwitch2 0 0  
vMotion vSwitch3 1 0  
[/code]

List your VMkernel Interfaces

[code]  
~ # esxcli network ip interface list  
vmk0  
Name: vmk0  
MAC Address: 00:50:56:17:12:cb  
Enabled: true  
Portset: vSwitch0  
Portgroup: Management Network  
VDS Name: N/A  
VDS Port: N/A  
VDS Connection: -1  
MTU: 1500  
TSO MSS: 65535  
Port ID: 16777219

vmk1  
Name: vmk1  
MAC Address: 00:50:56:17:16:07  
Enabled: true  
Portset: vSwitch1  
Portgroup: ISCSI_1  
VDS Name: N/A  
VDS Port: N/A  
VDS Connection: -1  
MTU: 1500  
TSO MSS: 65535  
Port ID: 33554435

vmk2  
Name: vmk2  
MAC Address: 00:50:56:17:16:58  
Enabled: true  
Portset: vSwitch3  
Portgroup: vMotion  
VDS Name: N/A  
VDS Port: N/A  
VDS Connection: -1  
MTU: 1500  
TSO MSS: 65535  
Port ID: 67108867  
[/code]

List your arp table:

[code]  
~ # esxcli network ip neighbor list  
Neighbor Mac Address Vmknic Expiry State  
\---\---\---\---\- --\---\---\---\---\--- \---\--- \---\---\-- -\----  
192.168.0.121 00:50:56:17:45:9c vmk0 1183 sec  
192.168.1.107 00:50:56:17:14:bf vmk1 1196 sec  
[/code]

List your active port connections:

[code]  
~ # esxcli network ip connection list  
Proto Recv Q Send Q Local Address Foreign Address State World ID World Name  
\---\-- -\---\-- -\---\-- -\---\---\---\---\---\--- \---\---\---\---\---\---\- --\---\---\--- \---\---\-- -\---\---\---\-----  
tcp 0 0 127.0.0.1:8307 127.0.0.1:53938 ESTABLISHED 2813 hostd-worker  
tcp 0 0 127.0.0.1:53938 127.0.0.1:8307 ESTABLISHED 4374 hostd-worker  
tcp 0 0 127.0.0.1:443 127.0.0.1:52899 ESTABLISHED 2787 hostd-worker  
tcp 0 0 127.0.0.1:52899 127.0.0.1:443 ESTABLISHED 64586 python  
[/code]

List your DVS information:

[code]  
~ # esxcli network vswitch dvs vmware list  
test  
Name: test  
VDS ID: 8a fa 1a 50 90 33 85 47-be 84 61 e0 c4 4c e2 ff  
Class: etherswitch  
Num Ports: 256  
Used Ports: 2  
Configured Ports: 256  
MTU: 1500  
CDP Status: listen  
Beacon Timeout: -1  
Uplinks: vmnic4  
VMware Branded: true  
DVPort:  
Client: vmnic4  
DVPortgroup ID: dvportgroup-102  
In Use: true  
Port ID: 136

Client:  
DVPortgroup ID: dvportgroup-102  
In Use: false  
Port ID: 137

Client:  
DVPortgroup ID: dvportgroup-102  
In Use: false  
Port ID: 138

Client:  
DVPortgroup ID: dvportgroup-102  
In Use: false  
Port ID: 139  
[/code]

Use the unsupported net-dvs command to list all the DVS information:

[code]  
~ # net-dvs -l | less  
switch 8a fa 1a 50 90 33 85 47-be 84 61 e0 c4 4c e2 ff (etherswitch)  
max ports: 256  
global properties:  
com.vmware.common.alias = test , propType = CONFIG  
com.vmware.common.version = 0x 0. 0. 0. 0  
propType = CONFIG  
com.vmware.etherswitch.mtu = 1500 , propType = CONFIG  
com.vmware.etherswitch.cdp = CDP, listen  
propType = CONFIG  
com.vmware.common.uplinkPorts:  
dvUplink1, dvUplink2, dvUplink3, dvUplink4  
propType = CONFIG  
com.vmware.common.respools.list:  
netsched.pools.persist.ft  
netsched.pools.persist.iscsi  
netsched.pools.persist.mgmt  
netsched.pools.persist.nfs  
netsched.pools.persist.vm  
netsched.pools.persist.vmotion  
propType = CONFIG  
com.vmware.common.respools.sched:  
inactive  
propType = CONFIG  
host properties:  
com.vmware.common.host.portset = DvsPortset-0 , propType = CONFIG  
com.vmware.common.host.volatile.status = green , propType = CONFIG  
com.vmware.common.host.uplinkPorts:  
136, 137, 138, 139  
propType = CONFIG  
port 136:  
com.vmware.common.port.alias = dvUplink1 , propType = CONFIG  
com.vmware.common.port.connectid = 503318012 , propType = CONFIG  
com.vmware.common.port.portgroupid = dvportgroup-102 , propType = CONFIG  
com.vmware.common.port.block = false , propType = CONFIG  
com.vmware.common.port.ptAllowed = 0x 0. 0. 0. 0  
propType = CONFIG  
com.vmware.etherswitch.port.teaming:  
load balancing = source virtual port id  
link selection = link state up; link speed>=10Mbps;  
link behavior = notify switch; reverse filter; best effort on failure; shotgun on failure;  
active =  
standby =  
propType = CONFIG  
com.vmware.etherswitch.port.security = deny promiscuous; allow mac change; allow forged frames  
propType = CONFIG  
com.vmware.etherswitch.port.vlan = Guest VLAN tagging  
ranges = 0-4094  
propType = CONFIG  
com.vmware.etherswitch.port.txUplink = normal , propType = CONFIG  
com.vmware.common.port.respools.cfg:  
netsched.pools.persist.ft:50:-1:0  
netsched.pools.persist.iscsi:50:-1:0  
netsched.pools.persist.mgmt:50:-1:0  
netsched.pools.persist.nfs:50:-1:0  
netsched.pools.persist.vm:100:-1:0  
netsched.pools.persist.vmotion:50:-1:0  
propType = CONFIG  
com.vmware.common.port.volatile.vlan = VLAN 0  
ranges = 0-4094  
propType = CONFIG  
com.vmware.common.port.statistics:  
pktsInUnicast = 0  
bytesInUnicast = 0  
pktsInMulticast = 0  
bytesInMulticast = 0  
pktsInBroadcast = 0  
bytesInBroadcast = 0  
pktsOutUnicast = 0  
bytesOutUnicast = 0  
pktsOutMulticast = 0  
bytesOutMulticast = 0  
pktsOutBroadcast = 0  
bytesOutBroadcast = 0  
pktsInDropped = 0  
pktsOutDropped = 0  
pktsInException = 0  
pktsOutException = 0  
propType = CONFIG  
com.vmware.common.port.volatile.status = inUse linkUp portID=83886082 propType = CONFIG  
com.vmware.common.port.volatile.ptstatus = noPassthruReason=1, propType = CONFIG  
[/code]

### Configure NetFlow

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf']);">vSphere Networking ESXi 5.0</a>:

> **Configure NetFlow Settings**  
> NetFlow is a network analysis tool that you can use to monitor network monitoring and virtual machine traffic. NetFlow is available on vSphere distributed switch version 5.0.0 and later.  
> **Procedure**  
> 1 Log in to the vSphere Client and select the Networking inventory view.  
> 2 Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.  
> 3 Navigate to the NetFlow tab.  
> 4 Type the IP address and Port of the NetFlow collector.  
> 5 Type the VDS IP address. With an IP address to the vSphere distributed switch, the NetFlow collector can interact with the vSphere distributed switch as a single switch, rather than interacting with a separate, unrelated switch for each associated host.  
> 6 (Optional) Use the up and down menu arrows to set the Active flow export timeout and Idle flow export timeout.  
> 7 (Optional) Use the up and down menu arrows to set the Sampling rate. The sampling rate determines what portion of data NetFlow collects, with the sampling rate number determining how often NetFlow collects the packets. A collector with a sampling rate of 2 collects data from every other packet. A collector with a sampling rate of 5 collects data from every fifth packet.  
> 8 (Optional) Select Process internal flows only to collect data only on network activity between virtual machines on the same host.  
> 9 Click OK. 

Here is how it looks like in the GUI:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/netflow_settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/netflow_settings.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/netflow_settings.png" alt="netflow settings VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="netflow_settings" width="692" height="530" class="alignnone size-full wp-image-3972" /></a>

The topic is also discussed in the VMware Blogs &#8220;<a href="http://blogs.vmware.com/vsphere/2011/08/vsphere-5-new-networking-features-netflow.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2011/08/vsphere-5-new-networking-features-netflow.html']);">vSphere 5 New Networking Features – NetFlow</a>&#8221;

### Determine appropriate discovery protocol (CDP, LLDP)

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf']);">vSphere Networking ESXi 5.0</a>&#8220;:

> **Switch Discovery Protocol**  
> Switch discovery protocols allow vSphere administrators to determine which switch port is connected to a given vSphere standard switch or vSphere distributed switch.
> 
> vSphere 5.0 supports Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP). CDP is available for vSphere standard switches and vSphere distributed switches connected to Cisco physical switches. LLDP is available for vSphere distributed switches version 5.0.0 and later.
> 
> When CDP or LLDP is enabled for a particular vSphere distributed switch or vSphere standard switch, you can view properties of the peer physical switch such as device ID, software version, and timeout from the vSphere Client. 

From the same document:

> **Enable Cisco Discovery Protocol on a vSphere Distributed Switch**  
> Cisco Discovery Protocol (CDP) allows vSphere administrators to determine which Cisco switch port connects to a given vSphere standard switch or vSphere distributed switch. When CDP is enabled for a particular vSphere distributed switch, you can view properties of the Cisco switch (such as device ID, software version,  
> and timeout) from the vSphere Client.
> 
> **Procedure**  
> 1 Log in to the vSphere Client and select the Networking inventory view.  
> 2 Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.  
> 3 On the Properties tab, select Advanced.  
> 4 Select Enabled from the Status drop-down menu.  
> 5 Select Cisco Discovery Protocol from the Type drop-down menu.  
> 6 Select the CDP mode from the Operation drop-down menu.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/CPD_Options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/CPD_Options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/CPD_Options.png" alt="CPD Options VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="CPD_Options" width="563" height="167" class="alignnone size-full wp-image-3983" /></a>
> 
> 7 Click OK 

Here is how it looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/cdp_dvs_options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/cdp_dvs_options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/cdp_dvs_options.png" alt="cdp dvs options VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="cdp_dvs_options" width="695" height="534" class="alignnone size-full wp-image-3984" /></a>

And again from the same document:

> Enable Link Layer Discovery Protocol on a vSphere Distributed Switch With Link Layer Discovery Protocol (LLDP), vSphere administrators can determine which physical switch port connects to a given vSphere distributed switch. When LLDP is enabled for a particular distributed switch, you can view properties of the physical switch (such as chassis ID, system name and description, and device capabilities) from the vSphere Client.
> 
> LLDP is available only on vSphere distributed switch version 5.0.0 and later.
> 
> **Procedure**  
> 1 Log in to the vSphere Client and select the Networking inventory view.  
> 2 Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.  
> 3 On the Properties tab, select Advanced.  
> 4 Select Enabled from the Status drop-down menu.  
> 5 Select Link Layer Discovery Protocol from the Type drop-down menu  
> 6 Select the LLDP mode from the Operation drop-down menu.  
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_options.png" alt="lddp options VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="lddp_options" width="563" height="167" class="alignnone size-full wp-image-3985" /></a>  
> 7 Click OK. 

Here is how it looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_dvs_options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_dvs_options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/lddp_dvs_options.png" alt="lddp dvs options VCAP5 DCA Objective 2.1 – Implement and Manage Complex Virtual Networks " title="lddp_dvs_options" width="690" height="532" class="alignnone size-full wp-image-3986" /></a>

Pick the one that matches your physical environment. If you have Cisco switches then use CDP, if you have a non-cisco environment then use LLDP.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/" title=" VCAP5-DCA Objective 2.1 – Implement and Manage Complex Virtual Networks" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCA,blog;button:compact;">Identify common virtual switch configurations From VMware Virtual Networking Concepts Load Balancing Load balancing allows you to spread network traffic from virtual machines on a virtual switch across two or...</a>
</p>