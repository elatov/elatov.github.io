---
title: VCD-NI Network Pools with the Cisco Nexus1000v Distributed Switch
author: Karim Elatov
layout: post
permalink: /2012/08/vcd-ni-network-pools-with-the-cisco-nexus1000v/
dsq_thread_id:
  - 1404673369
categories:
  - Networking
  - VMware
tags:
  - bridge-domains
  - Mac-in-Mac Encapsulation
  - multicast
  - Network Pool
  - Network Segmentation Manager
  - network segments
  - Organization Network
  - vApp Network
  - VCD-NI
  - vCloud
  - vCloud Director Network Isolation Networks
  - vShield Manager
---
I was recently messing around with my vCloud Lab and I decided to see how the Nexus 1000v integrates with vCloud Director. After figuring out how it works, I decided to post my findings. Most of the instructions can be seen in the article &#8220;<a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_2_1_s_v_1_5_1/nsm/configuration/guide/n1000v_nsm_2configuring_nsm.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_2_1_s_v_1_5_1/nsm/configuration/guide/n1000v_nsm_2configuring_nsm.html']);">Configuring Network Segmentation Manager</a>&#8220;. First thing to note is that this works on vCloud Director 1.5 and N1K version 4.2(1)SV1(5.1). Now for the fun stuff.

First enable the segmentation features on the N1K:

	  
	switch# conf t  
	switch(config)# feature network-segmentation-manager  
	switch(config)# feature segmentation  
	switch# show network-segment manager switch  
	switch: default_switch  
	state: enabled  
	dvs-uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	dvs-name: switch  
	mgmt-srv-uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	reg status: unregistered  
	last alert: - seconds ago  
	connection status: disconnected
	
	switch# show feature | grep seg  
	network-segmentation 1 enabled  
	segmentation 1 enabled  
	

Next create a Port Profile which will be used for your type of Network Segmentation Policies:

	  
	switch# conf t  
	switch(config)# port-profile type vethernet profile\_for\_segmentation  
	switch(config-port-prof)# no shutdown  
	switch(config-port-prof)# state enabled  
	switch(config-port-prof)# switchport mode access  
	switch(config-port-prof)# switchport access vlan 2002  
	switch(config-port-prof)# show running-config port-profile profile\_for\_segmentation
	
	!Command: show running-config port-profile profile\_for\_segmentation  
	!Time: Sun Aug 5 17:54:07 2012
	
	version 4.2(1)SV1(5.1)  
	port-profile type vethernet profile\_for\_segmentation  
	switchport mode access  
	switchport access vlan 2002  
	no shutdown  
	state enabled  
	

***Note** make sure you have a uplink (type ethernet) port-profile that allows the above VLAN

Next we create a Network Segmentation Policy, this actually depends on your Tenant ID of your Organization Instance from vCloud director. To obtain the Tenant ID follow the instructions laid out in VMware KB <a href="http://kb.vmware.com/kb/2012943" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2012943']);">2012943</a>. My Tenant ID is &#8220;e461e9cc-1205-40f4-9f36-ad0e841d9c73&#8243;, so here is how the creating of the policy looked like:

	  
	switch# conf t  
	switch(config)# network-segment policy vcd-ni-pol  
	switch(config-network-segment-policy)# description policy\_for\_vcd_ni  
	switch(config-network-segment-policy)# type segmentation  
	switch(config-network-segment-policy)# id e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	switch(config-network-segment-policy)# import port-profile profile\_for\_segmentation  
	switch(config-network-segment-policy)# show run network-segment policy vcd-ni-pol
	
	!Command: show running-config network-segment policy vcd-ni-pol  
	!Time: Sun Aug 5 18:02:59 2012
	
	version 4.2(1)SV1(5.1)  
	feature network-segmentation-manager
	
	network-segment policy vcd-ni-pol  
	id e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	description policy\_for\_vcd_ni  
	type segmentation  
	import port-profile profile\_for\_segmentation  
	

Next we register the Nexus1000v Network Segmentation Manager with vShield Manager as a switch provider. Here is step by step process taken from the Cisco article:

> 1.  In the vShield Manager, navigate to the Settings and Report window.
> 2.  In the Setting and Reports pane, click Configuration.
> 3.  Click Networking. The Edit Settings window opens.
> 4.  Enter the segment ID pool. The segment ID pool should be greater than 4097.
> 5.  Enter the multicast address range.
> 6.  Click OK.
> 7.  In the vShield Manager, navigate to the External Switch Providers window.
> 8.  Click Add Switch Provider. The External Switch Provider window opens.
> 9.  Enter the name of the switch.
> 10. Enter the NSM API service URL (https://Cisco-VSM-IP-Address/n1k/services/NSM).
> 11. Enter the network administrator username and password.
> 12. Accept the SSL thumbprint.
> 13. In the External Switch Providers window, a green check mark in the Status column indicates that the connection between vShield Manager and NSM is established.

Here is how my vShield Manager looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/vsm_multicast_settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/vsm_multicast_settings.png']);"><img class="alignnone size-full wp-image-2024" title="vsm_multicast_settings" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/vsm_multicast_settings.png" alt="vsm multicast settings VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="417" height="189" /></a>

Since VCD-NI uses multicast to encapsulate traffic, we define the range of multicast used and we also define how many different multicast groups we can possibly have (5000-8000), the values have to be starting from above 4096. In the nexus these are called bridge-domains. We will see them after we are done with the setup. And here is the configuration used to connect to the Nexus 1000v looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/nsm_connection.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/nsm_connection.png']);"><img class="alignnone size-full wp-image-2027" title="nsm_connection" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/nsm_connection.png" alt="nsm connection VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="748" height="304" /></a>

After connecting to the Nexus, here is what I saw on the VSM (Virtual Supervisor Module):

	  
	switch# show network-segment manager switch  
	switch: default_switch  
	state: enabled  
	dvs-uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	dvs-name: switch  
	mgmt-srv-uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	reg status: registered  
	last alert: 103 seconds ago  
	connection status: connected  
	

Now that this is all setup, we can setup a vCloud Organization to use it. First we need to add a new Network Pool of type &#8220;Network Isolation-Backed&#8221;, to do so follow these instructions:

1.  Login to your vCloud Director as administrator
2.  Click on System
3.  Click on &#8220;Manage and Monitor&#8221;
4.  Expand &#8220;Cloud Resources&#8221;
5.  Click on &#8220;Network Pools&#8221;
6.  Right Click on the Empty Area, and select &#8220;Add Network Pool&#8221;

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/vcloud_add_net_pool_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/vcloud_add_net_pool_1.png']);"><img class="alignnone size-full wp-image-2033" title="vcloud_add_net_pool_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/vcloud_add_net_pool_1.png" alt="vcloud add net pool 1 VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1067" height="517" /></a>

Follow the wizard to add the pool:

1.  Select &#8220;Network Isolation-Backed&#8221; and click Next
2.  Fill out, # of VCD Isolated networks
3.  Put in the VLAN that is used for VCD-NI (this vlan has to be setup on your upstream devices)
4.  Select your vCenter
5.  Select the N1K Distributed Switch

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/conf_ib_pool.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/conf_ib_pool.png']);"><img class="alignnone size-full wp-image-2034" title="conf_ib_pool" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/conf_ib_pool.png" alt="conf ib pool VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="964" height="652" /></a>

Click Next, and Name your Pool (I called mine &#8220;N1K\_VCD-NI\_Pool&#8221;). Then finally click Finish.

You are now finished with creating your pool. Now let&#8217;s make your Organization use this pool by default. To do that follow these instructions:

1.  Login to your vCloud Director as administrator
2.  Click on System
3.  Click on &#8220;Manage and Monitor&#8221;
4.  Click on &#8220;Organization&#8221;
5.  Right Click on your Organization and Select &#8220;Open&#8221;

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/open_org.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/open_org.png']);"><img class="alignnone size-full wp-image-2035" title="open_org" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/open_org.png" alt="open org VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1069" height="410" /></a>

Or you can login to the Organization Instance with your Organization Administrator credentials (So go to instead of https://10.131.6.1/cloud ). Either way, after you are on the Organization tab instead of the System tab, do the following:

1.  Select &#8220;Administration&#8221;
2.  Expand &#8220;Cloud Resources&#8221;
3.  Click on &#8220;Virtual Datacenters&#8221;
4.  Right Click on your Virtual Datacenter and select &#8220;Properties&#8221;<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/prop_vdc.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/prop_vdc.png']);"><img class="alignnone size-full wp-image-2036" title="prop_vdc" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/prop_vdc.png" alt="prop vdc VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1038" height="371" /></a>
5.  Click on the Network Pool Tab
6.  Select the VCD-NI Pool that you just created<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/change_net_pool_of_vdc.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/change_net_pool_of_vdc.png']);"><img class="alignnone size-full wp-image-2037" title="change_net_pool_of_vdc" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/change_net_pool_of_vdc.png" alt="change net pool of vdc VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="752" height="653" /></a>

Now if we create a new vApp with in this Organization and create a new vApp Network for this vApp it will use this pool. I created a new vApp called &#8220;vApp\_admin\_1&#8243; and I created a new vApp network for this vApp, I called the vApp Network &#8220;test&#8221;. Here is how the Network looked like for this vApp:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/new_vapp_with_vapp_network.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/new_vapp_with_vapp_network.png']);"><img class="alignnone size-full wp-image-2038" title="new_vapp_with_vapp_network" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/new_vapp_with_vapp_network.png" alt="new vapp with vapp network VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1062" height="468" /></a>

Upon powering on this vApp, I saw the the new DvPortgroup created and the VM added to it. Then checking out the N1K, I saw the following:

	  
	switch# show network-segment policy usage
	
	network-segment policy default\_segmentation\_template
	
	network-segment policy default\_vlan\_template
	
	network-segment policy vcd-ni-pol  
	dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f  
	

We can see that from our &#8220;vcd-ni-policy&#8221; network segment a new port-group has been created with the vApp Network Name in it (test). Checking out the multi-cast groups, I saw the following:

	  
	switch# show bridge-domain
	
	Bridge-domain dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f  
	(1 ports in all)  
	Segment ID: 5000 (Manual/Active)  
	Group IP: 224.0.4.1  
	State: UP Mac learning: Enabled  
	Veth3  
	

We can see that it starts with Segment ID 5000 and the group IP is &#8220;224.0.4.1&#8243;. This makes sense since this these are the settings we applied when adding the N1K as a switch provider to the vShield Manager. We can see that &#8220;veth3&#8243; is in that bridge domain. Checking out that virtual interface we can see that it corresponds to our VM from the vApp:

	  
	switch# show run int vethernet 3
	
	!Command: show running-config interface Vethernet3  
	!Time: Mon Aug 6 21:57:33 2012
	
	version 4.2(1)SV1(5.1)
	
	interface Vethernet3  
	inherit port-profile dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f  
	description OI (3adadd61-75c1-4af2-9d76-ff467e42e965), Network Adapter 1  
	vmware dvport 161 dvswitch uuid &quot;21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97  
	f4&quot;  
	vmware vm mac 0050.5601.0002  
	

On the host we can see that virtual port looks like this:

	  
	~ # vemcmd show segment  
	Number of valid BDS: 7  
	BD 6, vdc 1, segment id 5000, segment group IP 224.0.4.1, swbd 4096, 1 ports, &quot;dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f&quot;  
	Portlist:
	
	~ # vemcmd show bd 6  
	BD 6, vdc 1, segment id 5000, segment group IP 224.0.4.1, swbd 4096, 1 ports, &quot;dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f&quot;  
	Portlist:  
	49 OI (3adadd61-7...7e42e965).eth0  
	

We can see our segment (5000) belong to BD (Broadcast Domain) 6, then checking that BD we can see our VM is in it.

And lastly here is the generic information about our ports:

	  
	~ # vemcmd show pd-port  
	LTL Port DVport Type Link-valid State Duplex Speed PG-Name Status Client-Name  
	18 50331672 0 PHYS 1 UP 1 1000 dvportgroup-88 Success vmnic1  
	49 50331673 161 VIRT 0 0 0 dvportgroup-85 Success OI (3adadd61-75c1-4af2-9d76-ff467e42e965).eth0  
	

That all looks good.

What you could also do is create an Organization Network and setup it up to use the VCD-NI network pool and setup your vApp to use that Network. To setup the Org Network, follow these steps:

1.  Login to your vcloud director instance (not your organization instance) as the admin 
    1.  So go to instead of 
2.  Click on System
3.  Click on &#8220;Manage and Monitor&#8221;
4.  Click on &#8220;Organizations&#8221;
5.  Right Click on your Organization and Select &#8220;Open&#8221;

Once you have opened your Organization, then:

1.  Select Administration
2.  Expand Cloud Resources
3.  Click on &#8220;Networks&#8221;
4.  Right Click on the Empty area and select &#8220;Add Network&#8221;

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/add_org_network.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/add_org_network.png']);"><img class="alignnone size-full wp-image-2040" title="add_org_network" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/add_org_network.png" alt="add org network VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1062" height="465" /></a>

Then Follow the wizard:

1.  Select what type of Network you would like this to be (internal, routed, or direct)
2.  Select the N1K pool that we created to be used by this Org network<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/select_pool_for_org_network.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/select_pool_for_org_network.png']);"><img class="alignnone size-full wp-image-2041" title="select_pool_for_org_network" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/select_pool_for_org_network.png" alt="select pool for org network VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="934" height="687" /></a>
3.  Select the IP range for this network
4.  Name this Org network, I called mine &#8220;org\_net\_using\_n1k\_vcd-ni_pool&#8221;

I then deployed a new vApp, added a new VM to the vApp and put the nic of this VM on my newly created Org network. Here is how the network Diagram looked like for this vApp:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/vapp_conn_to_org_network_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/vapp_conn_to_org_network_1.png']);"><img class="alignnone size-full wp-image-2042" title="vapp_conn_to_org_network_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/vapp_conn_to_org_network_1.png" alt="vapp conn to org network 1 VCD NI Network Pools with the Cisco Nexus1000v Distributed Switch" width="1065" height="663" /></a>

Now checking out the settings on the N1K, I saw the following:

	
	
	switch# show network-segment policy usage
	
	network-segment policy default\_segmentation\_template
	
	network-segment policy default\_vlan\_template
	
	network-segment policy vcd-ni-pol  
	dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565  
	dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f  
	

Now we have two dvPortGroups: one for the test vApp Network and second for the &#8220;org\_net\_using\_n1k\_vcd-ni_pool&#8221; Org Network. Then for the bridge domains:

	
	
	switch# show bridge-domain
	
	Bridge-domain dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38  
	b429f3565 (1 ports in all)  
	Segment ID: 5001 (Manual/Active)  
	Group IP: 224.0.4.2  
	State: UP Mac learning: Enabled  
	Veth4
	
	Bridge-domain dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f  
	(1 ports in all)  
	Segment ID: 5000 (Manual/Active)  
	Group IP: 224.0.4.1  
	State: UP Mac learning: Enabled  
	Veth3  
	

Now we have two of those, which also makes sense. One more thing, I noticed the following on the upstream switch:

	  
	D04\_5010\_A# sho mac-address-table vlan 2002  
	VLAN MAC Address Type Age Port  
	\---\---\---+\---\---\---\---\-----+\---\----+\---\---\---+\---\---\---\---\---\---\---\---\---\---  
	2002 0013.f501.00f3 dynamic 30 Po112  
	2002 0013.f501.0103 dynamic 0 Po112  
	Total MAC Addresses: 2  
	

And also the following on the VEM:

	  
	~ # vemcmd show l2 all | grep '00:13:f5'  
	Dynamic 00:13:f5:01:00:f3 18 197  
	Dynamic 00:13:f5:01:01:03 18 21  
	

Check out the 00:13:f5 prefix for the Mac addresses. When VCD-NI is used you will not see the regular 00:50:56 prefix since Mac-in-Mac encapsulation is utilized. That is why only one vlan is necessary to use a VCD-NI network pool. If you want know more information on how VCD-NI works, check out <a href="http://blog.ioshints.info/2011/04/vcloud-director-networking.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.ioshints.info/2011/04/vcloud-director-networking.html']);">vCloud Director Networking Infrastructure (VCDNI) Scalability</a>, <a href="http://www.borgcube.com/blogs/2011/03/vcd-network-isolation-vcdni/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.borgcube.com/blogs/2011/03/vcd-network-isolation-vcdni/']);">vCD Network Isolation-vCDNI</a>, or VMware Communities Forum <a href="http://communities.vmware.com/thread/286475?start=15&tstart=0" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/286475?start=15&tstart=0']);">286475</a>. The last link actually has a sample pcap file, which you can examine and see the same Mac Address prefix that I see above.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/vcd-ni-network-pools-with-the-cisco-nexus1000v/" title=" VCD-NI Network Pools with the Cisco Nexus1000v Distributed Switch" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:bridge-domains,Mac-in-Mac Encapsulation,multicast,Network Pool,Network Segmentation Manager,network segments,Organization Network,vApp Network,VCD-NI,vCloud,vCloud Director Network Isolation Networks,vShield Manager,blog;button:compact;">I was recently messing around with my vCloud Lab and I decided to see how the Nexus 1000v integrates with vCloud Director. After figuring out how it works, I decided...</a>
</p>