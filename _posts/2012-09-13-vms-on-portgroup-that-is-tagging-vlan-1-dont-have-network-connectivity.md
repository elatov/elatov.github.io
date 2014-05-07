---
title: 'VMs on PortGroup with VLAN Tag 1, Don&#8217;t Have Network Connectivity'
author: Karim Elatov
layout: post
permalink: /2012/09/vms-on-portgroup-that-is-tagging-vlan-1-dont-have-network-connectivity/
dsq_thread_id:
  - 1407803686
categories:
  - Networking
  - VMware
tags:
  - 802.1Q trunk
  - CDP
  - Default VLAN
  - EST
  - Trunk Port
  - VLAN 1
  - VST
---
Recently ran into an issue where some of the VMs on an ESX host didn&#8217;t have network connectivity. Checking out the virtual switch settings I saw the following:

	  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch0 128 4 128 1500 vmnic0
	
	PortGroup Name VLAN ID Used Ports Uplinks  
	VM Network 1 1 vmnic0  
	Management Network 50 1 vmnic0  
	

From the above we can see that &#8220;VM Network&#8221; is the PortGroup setup for our VMs. One thing to notice is that we are actually Tagging this PortGroup with VLAN 1. We usually call this VST (Virtual Switch Tagging). VMware KB <a href="http://kb.vmware.com/kb/1004074" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004074']);">1004074</a> actually describes VST in detail. 

Next thing I wanted to check was the physical switch configuration. To do that we can use CDP (Cisco Discovery Protocol) to first find out what physical switch port we are connected to:

	  
	~ # vim-cmd hostsvc/net/query_networkhint  
	(vim.host.PhysicalNic.NetworkHint) [  
	(vim.host.PhysicalNic.NetworkHint) {  
	dynamicType = <unset>,  
	device = "vmnic0",  
	...  
	...  
	connectedSwitchPort = (vim.host.PhysicalNic.CdpInfo) {  
	dynamicType = <unset>,  
	cdpVersion = 0,  
	timeout = 0,  
	ttl = 169,  
	samples = 2982,  
	devId = "core_switch",  
	address = "192.168.9.18",  
	portId = "GigabitEthernet0/27",  
	

More information regarding CDP can be seen in VMware KB <a href="http://kb.vmware.com/kb/1007069" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1007069']);">1007069</a>. From the above output we can see that we were connected to "GigabitEthernet0/27". So we logged into the switch to check out the configuration and we saw the following:

	  
	core_switch# show run int gi0/27  
	interface GigabitEthernet0/27  
	switchport trunk encapsulation dot1q  
	switchport mode trunk  
	switchport trunk allowed vlan 1,50,60,128  
	spanning-tree portfast trunk  
	

So this was a trunk port and it's allowing/expecting vlans 1,50,60,128 to be tagged. Now with VLAN 1 it's a special case. From "<a href="http://www.cisco.com/en/US/products/hw/switches/ps628/products_configuration_example09186a00800ef797.shtml" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/products/hw/switches/ps628/products_configuration_example09186a00800ef797.shtml']);">Configuring EtherChannel and 802.1Q Trunking Between Catalyst L2 Fixed Configuration Switches and a Router (InterVLAN Routing)</a>":

> Note: Native VLAN is the VLAN that you configure on the Catalyst interface before you configure the trunking on that interface. By default, all interfaces are in VLAN 1. Therefore, VLAN 1 is the native VLAN that you can change. On an 802.1Q trunk, all VLAN packets except the native VLAN are tagged 

Since VLAN 1 is usually the default VLAN, when you trunk the default VLAN it will actually not tag that VLAN. So what we did was, remove the VLAN tag from our PortGroup, so it looked like this after wards:

	  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch0 128 4 128 1500 vmnic0
	
	PortGroup Name VLAN ID Used Ports Uplinks  
	VM Network 0 1 vmnic0  
	Management Network 50 1 vmnic0  
	

So now it was kind of setup as EST (External Switch Tagging). More information regarding EST can be seen in VMware KB <a href="http://kb.vmware.com/kb/1004127" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004127']);">1004127</a>. After making that change the VMs were able to get online without any issue.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Tag Multiple VLANs on Trunk Port on DD-WRT Router" href="http://virtuallyhyper.com/2014/04/tag-multiple-vlans-on-trunk-port-on-dd-wrt-router/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/04/tag-multiple-vlans-on-trunk-port-on-dd-wrt-router/']);" rel="bookmark">Tag Multiple VLANs on Trunk Port on DD-WRT Router</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/vms-on-portgroup-that-is-tagging-vlan-1-dont-have-network-connectivity/" title=" VMs on PortGroup with VLAN Tag 1, Don&#8217;t Have Network Connectivity" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:802.1Q trunk,CDP,Default VLAN,EST,Trunk Port,VLAN 1,VST,blog;button:compact;">I was running an ESXi host in my home network and I wanted to dedicate on NIC of the ESXi for VM traffic. Since I was planning on having different...</a>
</p>