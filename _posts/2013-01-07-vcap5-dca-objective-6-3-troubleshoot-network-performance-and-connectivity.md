---
title: VCAP5-DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/
dsq_thread_id:
  - 1409138249
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify vCLI commands and tools used to troubleshoot vSphere networking configurations

This was covered in "<a href="http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/']);">VCAP5-DCA Objective 2.1</a>"

### Identify logs used to troubleshoot network issues

Here is a good summary:

DHCP issues - /var/log/dhclient.log  
Networking driver issues - /var/log/vmkernel.log  
vCenter Connection issues - /var/log/vpxa.log  
DVS and virtual port assignment issues - /var/log/hostd.log

### Utilize net-dvs to troubleshoot vNetwork Distributed Switch configurations

This command is to be used for querying only and an example of the output is seen in "<a href="http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/']);">VCAP5-DCA Objective 2.1</a>"

### Utilize vSphere CLI commands to troubleshoot ESXi network configurations

Run through the command described in "<a href="http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/']);">VCAP5-DCA Objective 2.1</a>" and if you catch any issue then fix it. For example if the Subnet of a vmkernel interface is wrong then fix it, or if the wrong VLAN is assigned to a port group then fix that as well.

### Troubleshoot Private VLANs

Make sure the upstream switch configuration is correct. Here is a small example:

	  
	interface fa0/3  
	switchport mode private-vlan host  
	switchport private-vlan host-association 10 104  
	!  
	interface fa0/4  
	switchport mode private-vlan host  
	switchport private-vlan host-association 10 104  
	!  
	interface fa0/7  
	switchport mode private-vlan host  
	switchport private-vlan host-association 10 102  
	!  
	interface fa0/8  
	switchport mode private-vlan host  
	switchport private-vlan host-association 10 102  
	

Make you sure to check out the PVLAN settings on the DVS and ensure the appropriate VLAN type is assigned to the appropriate PVLAN number. For example make sure community is PVLAN 102 and promiscuous is PVLAN 104

### Troubleshoot vmkernel related network configuration issues

List all the vmkernel interfaces:

	  
	~ # esxcli network ip interface ipv4 get  
	Name IPv4 Address IPv4 Netmask IPv4 Broadcast Address Type DHCP DNS  
	\---\- --\---\---\---\-- -\---\---\---\--- \---\---\---\---\-- -\---\---\---\-- -\---\----  
	vmk0 192.168.0.103 255.255.255.0 192.168.0.255 STATIC false  
	vmk1 192.168.1.106 255.255.255.0 192.168.1.255 STATIC false  
	vmk2 192.168.3.102 255.255.255.0 192.168.3.255 STATIC false  
	

Figure out which one is used for Management:

	  
	~ # grep -i ManagementIface /etc/vmware/esx.conf  
	/adv/Net/ManagementIface = "vmk0"  
	

Figure out which one is used for vMotion:

	  
	~ # grep -i /migrate /etc/vmware/esx.conf  
	/adv/Migrate/Vmknic = "vmk2"  
	

Figure out which one is used for Fault Tolerance logging:

	  
	~ # grep /FT /etc/vmware/esx.conf  
	/adv/FT/Vmknic = "vmk1"  
	

### Troubleshoot DNS and routing related issues

List the dns search domain:

	  
	~ # esxcli network ip dns search list  
	DNSSearch Domains:  
	

List the DNS servers on the host:

	  
	~ # esxcli network ip dns server list  
	DNSServers:  
	

Add or remove DNS search domains and DNS servers:

	  
	~ # esxcli network ip dns search add -d test.com  
	~ # esxcli network ip dns search list  
	DNSSearch Domains: test.com  
	

Add a DNS server:

	  
	~ # esxcli network ip dns server add -s 192.168.1.30  
	~ # esxcli network ip dns server list  
	DNSServers: 192.168.1.30  
	

List the routing table on the ESXi host:

	  
	~ # esxcfg-route -l  
	VMkernel Routes:  
	Network Netmask Gateway Interface  
	192.168.0.0 255.255.255.0 Local Subnet vmk0  
	192.168.1.0 255.255.255.0 Local Subnet vmk1  
	192.168.3.0 255.255.255.0 Local Subnet vmk2  
	

Add a static route to reach network 10.12.10.0/24 via 192.168.1.2 gateway:

	  
	~ # esxcfg-route -a 10.12.10.0/24 192.168.1.2  
	Adding static route 10.12.10.0/24 to VMkernel  
	~ # esxcfg-route -l  
	VMkernel Routes:  
	Network Netmask Gateway Interface  
	10.12.10.0 255.255.255.0 192.168.1.2 vmk1  
	192.168.0.0 255.255.255.0 Local Subnet vmk0  
	192.168.1.0 255.255.255.0 Local Subnet vmk1  
	192.168.3.0 255.255.255.0 Local Subnet vmk2  
	

Remove a route from the routing table:

	  
	~ # esxcfg-route -d 10.12.10.0/24 192.168.1.2  
	Deleting static route 10.12.10.0/24 from VMkernel  
	

### Use esxtop/resxtop to identify network performance problems

From <a href="http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf']);">this</a> pdf:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/esxtop_network_problems/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/esxtop_network_problems/']);" rel="attachment wp-att-5313"><img class="alignnone size-full wp-image-5313" alt="esxtop network problems VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_network_problems.png" width="603" height="236" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

Here is a quick summary:

> %DRPTX, %DRPRX: Dropped Transmitted and Received Packets (Trouble when > 1)

### Analyze troubleshooting data to determine if the root cause for a given network problem originates in the physical infrastructure or vSphere environment

From "<a href="http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf']);">Performance Troubleshooting for VMware vSphere 4.1</a>":

> **12.2. Dropped Receive Packets**  
> **12.2.1. Causes**  
> Network packets may get stored (buffered) in queues at multiple points along their route from the source to the destination. Network switches, physical NICs, device drivers, and network stacks may all contain queues where packet data or headers are buffered before being passed to the next step in the delivery process. These queues are finite in size. When they fill up, no more packets can be received at that point on the route, and additional arriving packets must be dropped. TCP/IP networks use congestion-control algorithms that limit, but do not eliminate, dropped packets. When a packet is dropped, TCP/IP's recovery mechanisms work to maintain in-order delivery of packets to applications. However these mechanisms operate at a cost to both networking performance and CPU overhead, a penalty that becomes more severe as the physical network speed increases.
> 
> vSphere presents virtual network-interface devices, such as the vmxnet or virtual e1000 devices, to the guest OS running in a VM. For received packets, the virtual NIC buffers packet data coming from a virtual switch (vSwitch) until it is retrieved by the device-driver running in the guest OS. The vSwitch, in turn, contains queues for packets sent to the virtual NIC.
> 
> If the Guest OS does not retrieve packets from the virtual NIC rapidly enough, the queues in the virtual NIC device can fill up. This can in turn cause the queues within the corresponding vSwitch port to fill. If a vSwitch port receives a packet bound for a VM when its packet queue is full, it must drop the packet. The count of these dropped packets over the selected measurement interval is available in the performance metrics visible from the vSphere Client. In previous versions of VMware ESX, this data was only available from esxtop. The following problems can cause the guest OS to fail to retrieve packets quickly enough from the virtual NIC:
> 
> *   High CPU utilization. When the applications and guest OS are driving the VM to high CPU utilizations, there may be extended delays from the time the guest OS receives notification that receive packets are available until those packets are retrieved from the virtual NIC. In some cases, the high CPU utilization may in fact be caused by high network traffic, since the processing of network packets can place a significant demand on CPU resources.
> *   Guest OS driver configuration. Device-drivers for networking devices often have parameters that are tunable from within the guest OS. These may control behavior such as the use of interrupts versus polling, the number of packets retrieved on each interrupt, and the number of packets a device should buffer before interrupting the OS. Improper configuration of these parameters can cause poor network performance and dropped packets in the networking infrastructure.
> 
> **12.2.2. Solutions**  
> The solutions to the problem of dropped received packets are all related to ways of improving the ability of the guest OS to quickly retrieve packets from the virtual NIC. They are:
> 
> *   Increase the CPU resources provided to the VM. When the VM is dropping receive packets dues to high CPU utilization, it may be necessary to add additional vCPUs in order to provide sufficient CPU resources. If the high CPU utilization is due to network processing, refer to the OS documentation to ensure that the guest OS can take advantage of multiple CPUs when processing network traffic.
> *   Increase the efficiency with which the VM uses CPU resources. Applications which have high CPU utilization can often be tuned to improve their use of CPU resources. See the discussion about increasing VM efficiency in the Solutions section under Host CPU Saturation.
> *   Tune network stack in the Guest OS. It may be possible to tune the networking stack within the guest OS to improve the speed and efficiency with which it handles network packets. Refer to the documentation for the OS.
> *   Add additional virtual NICs to the VM and spread network load across them. In some guest OSes, all of the interrupts for each NIC are directed to a single processor core. As a result, the single processor can become a bottleneck, leading to dropped receive packets. Adding additional virtual NICs to these VMs will allow the processing of network interrupts to be spread across multiple processor cores.

Check out esxtop and if you see any Drops (received or transmitted) it maybe CPU limitation or buffering issue with in the Guest OS. If you check out physical NIC statistics like so:

	  
	~ # ethtool -S vmnic0  
	NIC statistics:  
	rx_packets: 3711232  
	tx_packets: 7100469  
	rx_bytes: 495915330  
	tx_bytes: 1247347860  
	rx_broadcast: 0  
	tx_broadcast: 0  
	rx_multicast: 0  
	tx_multicast: 0  
	rx_errors: 0  
	tx_errors: 0  
	tx_dropped: 0  
	multicast: 0  
	collisions: 0  
	rx_length_errors: 0  
	rx_over_errors: 0  
	rx_crc_errors: 0  
	rx_frame_errors: 0  
	rx_no_buffer_count: 0  
	rx_missed_errors: 0  
	tx_aborted_errors: 0  
	tx_carrier_errors: 0  
	tx_fifo_errors: 0  
	tx_heartbeat_errors: 0  
	tx_window_errors: 0  
	tx_abort_late_coll: 0  
	tx_deferred_ok: 0  
	tx_single_coll_ok: 0  
	tx_multi_coll_ok: 0  
	tx_timeout_count: 0  
	tx_restart_queue: 0  
	rx_long_length_errors: 0  
	rx_short_length_errors: 0  
	rx_align_errors: 0  
	tx_tcp_seg_good: 14887  
	tx_tcp_seg_failed: 0  
	rx_flow_control_xon: 0  
	rx_flow_control_xoff: 0  
	tx_flow_control_xon: 0  
	tx_flow_control_xoff: 0  
	rx_long_byte_count: 495915330  
	rx_csum_offload_good: 3036558  
	rx_csum_offload_errors: 0  
	alloc_rx_buff_failed: 0  
	tx_smbus: 0  
	rx_smbus: 0  
	dropped_smbus: 0  
	

If any of the failed or dropped counters are high, it could be a sign of a bad Nic Driver or some upstream issues. Also if you check out the logs under */var/log/vmkernel.log* and you see driver related errors then it's most like a driver/firmware issue and checking out the vendor recipes is recommended to make sure they are up to the recommended versions.

### Configure and administer Port Mirroring

From "<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf']);">vSphere Networking ESXi 5.0</a>":

> **Working With Port Mirroring**  
> Port mirroring allows you to mirror a distributed port's traffic to other distributed ports or specific physical switch ports.  
> **Create a Port Mirroring Session**  
> Create a port mirroring session to mirror vSphere distributed switch traffic to specific physical switch ports.  
> **Prerequisites**  
> Create a vSphere distributed switch version 5.0.0 or later.  
> **Procedure**  
> **Specify Port Mirroring Name and Session Details**  
> Specify the name, description, and session details for the new port mirroring session.  
> **Procedure**
> 
> 1.  Log in to the vSphere Client and select the Networking inventory view.
> 2.  Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.
> 3.  On the Port Mirroring tab, click Add.
> 4.  Enter a Name and Description for the port mirroring session.
> 5.  (Optional) Select Allow normal IO on destination ports to allow normal IO traffic on destination ports.If you do not select this option, mirrored traffic will be allowed out on destination ports, but no traffic will be allowed in.
> 6.  (Optional) Select Encapsulation VLAN to create a VLAN ID that encapsulates all frames at the destination ports.If the original frames have a VLAN and Preserve original VLAN is not selected, the encapsulation VLAN replaces the original VLAN.
> 7.  (Optional) Select Preserve original VLAN to keep the original VLAN in an inner tag so mirrored frames are double encapsulated.This option is available only if you select Encapsulation VLAN.
> 8.  (Optional) Select Mirrored packet length to put a limit on the size of mirrored frames.If this option is selected, all mirrored frames are truncated to the specified length.
> 9.  Click Next.

Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/create_port_mirror/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/create_port_mirror/']);" rel="attachment wp-att-5316"><img class="alignnone size-full wp-image-5316" alt="create port mirror VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/create_port_mirror.png" width="821" height="548" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

Here are the next steps from the above guide:

> **Choose Port Mirroring Sources**  
> Select sources and traffic direction for the new port mirroring session.  
> **Procedure**
> 
> 1.  Choose whether to use this source for Ingress or Egress traffic, or choose Ingress/Egress to use this source for both types of traffic.
> 2.  Type the source port IDs and click >> to add the sources to the port mirroring session.Separate multiple port IDs with a comma.
> 3.  Click Next.

So first choose a port you want mirror, by looking under "Networking" View -> Select DVS -> Select "Ports" tab and you will see the following:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/choose_port_from_dvs/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/choose_port_from_dvs/']);" rel="attachment wp-att-5317"><img class="alignnone size-full wp-image-5317" alt="choose port from dvs VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/choose_port_from_dvs.png" width="757" height="357" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

Then in the Create Mirror Session Wizard use that port number, like so:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_select_port/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_select_port/']);" rel="attachment wp-att-5318"><img class="alignnone size-full wp-image-5318" alt="mirror session select port VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/mirror_session_select_port.png" width="818" height="546" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

And more steps from the guide:

> **Choose Port Mirroring Destinations**  
> Select ports, or uplinks as destinations for the port mirroring session.
> 
> Port Mirroring is checked against the VLAN forwarding policy. If the VLAN of the original frames is not equal  
> to or trunked by the destination port, the frames are not mirrored.
> 
> **Procedure**
> 
> 1.  Choose the Source type.  
>     <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_source_type/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_source_type/']);" rel="attachment wp-att-5320"><img class="alignnone size-full wp-image-5320" alt="mirror session source type VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/mirror_session_source_type.png" width="562" height="97" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>
> 2.  Click >> to add the selected destinations to the port mirroring session.
> 3.  (Optional) Repeat the above steps to add multiple destinations.
> 4.  Click Next.

Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_select_destination_port/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_select_destination_port/']);" rel="attachment wp-att-5321"><img class="alignnone size-full wp-image-5321" alt="mirror session select destination port VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/mirror_session_select_destination_port.png" width="817" height="545" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

In the above example I chose an uplink to be the destination of the mirror session. And here are more steps from the same guide:

> **Verify New Port Mirroring Settings**  
> Verify and enable the new port mirroring session.  
> **Procedure**
> 
> 1.  Verify that the listed name and settings for the new port mirroring session are correct.
> 2.  (Optional) Click Back to make any changes.
> 3.  (Optional) Click Enable this port mirroring session to start the port mirroring session immediately.
> 4.  Click Finish.

Here is how it looks like from vCenter:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_verify_settings/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_verify_settings/']);" rel="attachment wp-att-5322"><img class="alignnone size-full wp-image-5322" alt="mirror session verify settings VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/mirror_session_verify_settings.png" width="821" height="552" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

And here are the last steps from the guide:

> **View Port Mirroring Session Details**  
> View port mirroring session details, including status, sources, and destinations.  
> **Procedure**
> 
> 1.  Log in to the vSphere Client and select the Networking inventory view.
> 2.  Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.
> 3.  On the Port Mirroring tab, select the port mirroring session to view.Details for the selected port mirroring session appear under Port Mirroring Session Details.
> 4.  (Optional) Click Edit to edit the details for the selected port mirroring session.
> 5.  (Optional) Click Delete to delete the selected port mirroring session.
> 6.  (Optional) Click Add to add a new port mirroring session.

Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_check_settings/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/mirror_session_check_settings/']);" rel="attachment wp-att-5324"><img class="alignnone size-full wp-image-5324" alt="mirror session check settings VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/mirror_session_check_settings.png" width="692" height="531" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

### Utilize Direct Console User Interface (DCUI) and ESXi Shell to troubleshoot, configure, and monitor ESXi networking

From "<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf']);">vSphere Installation and Setup vSphere 5.0</a>":

> **Configure IP Settings from the Direct Console**  
> If you have physical access to the host or remote access to the direct console, you can use the direct console to configure the IP address, subnet mask, and default gateway.  
> **Procedure**
> 
> 1.  Select Configure Management Network and press Enter.
> 2.  Select IP Configuration and press Enter.
> 3.  Select Set static IP address and network configuration.
> 4.  Enter the IP address, subnet mask, and default gateway and press Enter

Here is how it looks like in the DCUI:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_ip_config/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_ip_config/']);" rel="attachment wp-att-5325"><img class="alignnone size-full wp-image-5325" alt="dcui ip config VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dcui_ip_config.png" width="620" height="260" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

More information from the same guide:

> **Configure DNS Settings from the Direct Console**  
> If you have physical access to the host or remote access to the direct console, you can use the direct console to configure DNS information.  
> **Procedure**
> 
> 1.  Select Configure Management Network and press Enter.
> 2.  Select DNS Configuration and press Enter.
> 3.  Select Use the following DNS server addresses and hostname.
> 4.  Enter the primary server, an alternative server (optional), and the host name.
> 
> **Configure DNS Suffixes**  
> If you have physical access to the host, you can use the direct console to configure DNS information. By default, DHCP acquires the DNS suffixes.  
> **Procedure**
> 
> 1.  From the direct console, select Configure Management Network.
> 2.  Select Custom DNS Suffixes and press Enter.
> 3.  Enter new DNS suffixes

Here is how it looks like from the DCUI:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_dns_settings/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_dns_settings/']);" rel="attachment wp-att-5326"><img class="alignnone size-full wp-image-5326" alt="dcui dns settings VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dcui_dns_settings.png" width="616" height="259" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

More from the same guide:

> **Test the Management Network**  
> You can use the direct console to do simple network connectivity tests.  
> The direct console performs the following tests.
> 
> *   Pings the default gateway
> *   Pings the primary DNS name server
> *   Pings the secondary DNS nameserver
> *   Resolves the configured host name
> 
> **Procedure**
> 
> 1.  From the direct console, select Test Management Network and press Enter.
> 2.  Press Enter to start the test.

Here is how the test setup looks like from DCUI:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/test_mgmt_network_dcui/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/test_mgmt_network_dcui/']);" rel="attachment wp-att-5327"><img class="alignnone size-full wp-image-5327" alt="test mgmt network dcui VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/test_mgmt_network_dcui.png" width="556" height="217" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

And here is how the results look like:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_test_mgmt_net_results/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_test_mgmt_net_results/']);" rel="attachment wp-att-5328"><img class="alignnone size-full wp-image-5328" alt="dcui test mgmt net results VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dcui_test_mgmt_net_results.png" width="595" height="198" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

Some more stuff to try:

> **Restart the Management Agents**  
> The management agents synchronize VMware components and let you access the ESXi host through the vSphere Client or vCenter Server. They are installed with the vSphere software. You might need to restart the management agents if remote access is interrupted.
> 
> Restarting the management agents restarts all management agents and services that are installed and running in /etc/init.d on the ESXi host. Typically, these agents include hostd, ntpd, sfcbd, slpd, wsman, and vobd. The software also restarts Fault Domain Manager (FDM) if it is installed.
> 
> Users accessing this host through the vSphere Client or vCenter Server lose connectivity when you restart management agents.  
> **Procedure**
> 
> 1.  From the direct console, select Troubleshooting Options and press Enter.
> 2.  Select Restart Management Agents and press Enter.
> 3.  Press F11 to confirm the restart.
> 
> The ESXi host restarts the management agents and services

Here is how it looks like from DCUI:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/restart_mgmt_agents_dcui/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/restart_mgmt_agents_dcui/']);" rel="attachment wp-att-5329"><img class="alignnone size-full wp-image-5329" alt="restart mgmt agents dcui VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/restart_mgmt_agents_dcui.png" width="562" height="179" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a><a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/restart_mgmt_agents_success/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/restart_mgmt_agents_success/']);" rel="attachment wp-att-5330"><img class="alignnone size-full wp-image-5330" alt="restart mgmt agents success VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/restart_mgmt_agents_success.png" width="560" height="182" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>

Here are the rest of the options:

> **Restart the Management Network**  
> Restarting the management network interface might be required to restore networking or to renew a DHCP lease.
> 
> Restarting the management network will result in a brief network outage that might temporarily affect running virtual machines.
> 
> If a renewed DHCP lease results in a new network identity (IP address or host name), remote management software will be disconnected.  
> **Procedure**
> 
> 1.  From the direct console, select Restart Management Network and press Enter.
> 2.  Press F11 to confirm the restart.
> 
> **Disable the Management Network**  
> The management network synchronizes VMware components and lets you access the ESXi host through the vSphere Client or vCenter Server. It is installed with the vSphere software. You might need to disable the management network to isolate a host from the vCenter Server inventory.  
> Users who access this host through the vSphere Client or vCenter Server lose connectivity when you disable the management network.
> 
> One reason to disable the management network is to isolate an ESXi host from an HA and DRS cluster, without losing your static IP and DNS configurations or rebooting the host.  
> This operation does not require downtime for virtual machines. The virtual machines continue to run while the host is disconnected from vCenter Server and the vSphere Client.  
> **Procedure**
> 
> 1.  From the direct console, select Disable Management Network and press Enter.
> 2.  Press F11 to confirm.
> 
> **Restoring the Standard Switch**  
> A vSphere Distributed Switch functions as a single virtual switch across all associated hosts. Virtual machines can maintain a consistent network configuration as they migrate across multiple hosts. If you migrate an existing standard switch, or virtual adapter, to a Distributed Switch and the Distributed Switch becomes unnecessary or stops functioning, you can restore the standard switch to ensure that the host remains accessible.
> 
> When you restore the standard switch, a new virtual adapter is created and the management network uplink that is currently connected to Distributed Switch is migrated to the new virtual switch. You might need to restore the standard switch for the following reasons:
> 
> *   The Distributed Switch is not needed or is not functioning.
> *   The Distributed Switch needs to be repaired to restore connectivity to vCenter Server and the hosts need to remain accessible.
> *   You do not want vCenter Server to manage the host. When the host is not connected to vCenter Server, most Distributed Switch features are unavailable to the host.
> 
> **Prerequisites**  
> Verify that your management network is connected to a distributed switch.  
> **Procedure**
> 
> 1.  1 From the direct console, select Restore Standard Switch and press Enter. 
>     If the host is on a standard switch, this selection is dimmed, and you cannot select it.</li> 
>     *   Press F11 to confirm.</ol> </blockquote> 
>     Here are all the options as seen in the DCUI:
>     
>     <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_options/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/dcui_options/']);" rel="attachment wp-att-5331"><img class="alignnone size-full wp-image-5331" alt="dcui options VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dcui_options.png" width="1011" height="239" title="VCAP5 DCA Objective 6.3 – Troubleshoot Network Performance and Connectivity " /></a>
>     
