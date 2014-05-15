---
title: Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch
author: Karim Elatov
layout: post
permalink: /2012/08/quick-step-by-step-guide-on-how-to-setup-the-nexus1000v-distributed-switch/
dsq_thread_id:
  - 1407622444
categories:
  - Networking
  - VMware
tags:
  - Control VLAN
  - Management VLAN
  - Nexus1000v
  - Packet VLAN
  - Port-Profiles
  - vCenter Plugin-Manager
  - VEM
  - vemcmd
  - vethernet
  - Virtual Ethernet Module
  - Virtual Supervisor Module
  - VSM
---
In this example I used version 4.2(1)SV1(5.1) of the Nexus. First and foremost download the Nexus1000v software. Once you logged in to your Cisco account and found the download, it will look like this:<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/download_n1k.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/download_n1k.png']);"><img class="alignnone size-full wp-image-2075" title="download_n1k" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/download_n1k.png" alt="download n1k Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="1195" height="351" /></a>

After you have downloaded the software to your desktop and extracted it, the contents will look something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/contents_of_n1k.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/contents_of_n1k.png']);"><img class="alignnone size-full wp-image-2076" title="contents_of_n1k" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/contents_of_n1k.png" alt="contents of n1k Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="659" height="311" /></a>

Inside the "VSM" (Virtual Supervisor Module) folder will be the "Install" folder and inside of the "Install" folder will be the "ova" which you can deploy in your vCenter. So login to your vCenter and go to "File" -> "Deploy OVF Template", then browse to your downloaded N1K software. It will look something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/deploy_n1k_ova.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/deploy_n1k_ova.png']);"><img class="alignnone size-full wp-image-2077" title="deploy_n1k_ova" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/deploy_n1k_ova.png" alt="deploy n1k ova Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="713" height="676" /></a>

Click "Next", then "Next" again, then "Accept" and one more "Next". Name the VSM as desired, I just left the default (Nexus1000V-4.2.1.SV1.5.1). Under the configuration, select "Nexus 1000V Installer" (it should be the default). Keep going through the wizard, until you get to the Customization Page, then fill out the required information:

1.  VSM Domain ID (pick anything between 1-4095) this only matters if you plan on having multiple VSMs
2.  Password (make it secure)
3.  Management IP Address ( You will later SSH to this IP)
4.  Management IP Subnet Mask
5.  Management IP Gateway

Here is my configuration looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/custom_settings_N1K.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/custom_settings_N1K.png']);"><img class="alignnone size-full wp-image-2079" title="custom_settings_N1K" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/custom_settings_N1K.png" alt="custom settings N1K Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="719" height="780" /></a>

Then click "Next" and then "Finish". After you are done you should see the N1K deployed as a VM in your inventory. Power the N1K VM on and then you should be able to SSH to it. Here is how my putty session looked like after I logged in:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/putty-to_n1k.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/putty-to_n1k.png']);"><img class="alignnone size-full wp-image-2080" title="putty-to_n1k" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/putty-to_n1k.png" alt="putty to n1k Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="663" height="408" /></a>

With the default configuration, here is how the 'show run' looks like:

	  
	switch# show run
	
	!Command: show running-config  
	!Time: Fri Aug 3 23:58:47 2012
	
	version 4.2(1)SV1(5.1)  
	no feature telnet
	
	username admin password 5 $1$o.Nq/qPt$oaW.ZuXxW/EIXeuK2igXr1 role network-admin
	
	banner motd #Nexus 1000v Switch#
	
	ssh key rsa 2048  
	ip domain-lookup  
	snmp-server user admin network-admin auth md5 0x49dbfbc428f9aa50062c0dcba504a6d3  
	priv 0x49dbfbc428f9aa50062c0dcba504a6d3 localizedkey
	
	vrf context management  
	ip route 0.0.0.0/0 10.131.7.254  
	vlan 1
	
	port-channel load-balance ethernet source-mac  
	port-profile default max-ports 32
	
	vdc switch id 1  
	limit-resource vlan minimum 16 maximum 2049  
	limit-resource monitor-session minimum 0 maximum 2  
	limit-resource vrf minimum 16 maximum 8192  
	limit-resource port-channel minimum 0 maximum 768  
	limit-resource u4route-mem minimum 1 maximum 1  
	limit-resource u6route-mem minimum 1 maximum 1  
	limit-resource m4route-mem minimum 58 maximum 58  
	limit-resource m6route-mem minimum 8 maximum 8
	
	interface mgmt0  
	ip address 10.131.6.7/21
	
	interface control0  
	line console  
	boot kickstart bootflash:/nexus-1000v-kickstart-mz.4.2.1.SV1.5.1.bin sup-1  
	boot system bootflash:/nexus-1000v-mz.4.2.1.SV1.5.1.bin sup-1  
	boot kickstart bootflash:/nexus-1000v-kickstart-mz.4.2.1.SV1.5.1.bin sup-2  
	boot system bootflash:/nexus-1000v-mz.4.2.1.SV1.5.1.bin sup-2  
	svs-domain  
	domain id 233  
	control vlan 0  
	packet vlan 0  
	svs mode L2  
	svs connection VC  
	max-ports 8192  
	vsn type vsg global  
	tcp state-checks  
	vnm-policy-agent  
	registration-ip 0.0.0.0  
	shared-secret \***\***\****  
	log-level  
	

We can see that VLAN 1 is defined and the IP that we configured during deployment for management is there as well. This is a very basic setup, so I will use VLAN 1 for my control and packet VLANs. If this was a production setup, I would suggest to get dedicated VLANs for both of those. So let's go ahead and setup the control and packet VLANs:

	  
	switch# conf t  
	Enter configuration commands, one per line. End with CNTL/Z.  
	switch(config)# svs-domain  
	switch(config-svs-domain)# control vlan 1  
	switch(config-svs-domain)# packet vlan 1  
	switch(config-svs-domain)# end  
	

Now let's download the Nexus 1000v extension and register it with your vCenter. This will allow the communication between the VSM and the vCenter. Point your browser to the IP of the VSM and save the Extension to your desktop:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/download-n1k-ext_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/download-n1k-ext_1.png']);"><img class="alignnone size-full wp-image-2084" title="download-n1k-ext_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/download-n1k-ext_1.png" alt="download n1k ext 1 Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="1068" height="819" /></a>

After you have downloaded the extension, install it as a plug-in in your vCenter. In vCenter go to "Plugins" -> "Manage Plugins". Right click on the empty area and select "New Plug-In". Then browse to your extension, you will then see a screen similar to this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/register_n1k_ext.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/register_n1k_ext.png']);"><img class="alignnone size-full wp-image-2085" title="register_n1k_ext" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/register_n1k_ext.png" alt="register n1k ext Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="734" height="642" /></a>

Then click "Register Plug-in", your plug-in manager should look like this after the registration completes:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/plug-in-manager-after-n1k-ext-regis.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/plug-in-manager-after-n1k-ext-regis.png']);"><img class="alignnone size-full wp-image-2086" title="plug-in-manager-after-n1k-ext-regis" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/plug-in-manager-after-n1k-ext-regis.png" alt="plug in manager after n1k ext regis Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="938" height="427" /></a>

Nothing else has to be done for the plug-in. Next configure the Nexus 1000v to connect to your vCenter:

	  
	switch# conf t  
	Enter configuration commands, one per line. End with CNTL/Z.  
	switch(config)# svs connection VC  
	switch(config-svs-conn)# remote ip address 10.131.6.4  
	switch(config-svs-conn)# protocol vmware-vim  
	switch(config-svs-conn)# vmware dvs datacenter-name VDC  
	switch(config-svs-conn)# connect  
	Note: Command execution in progress..please wait  
	

Next we can confirm the connection:

	  
	switch(config-svs-conn)# show svs connections
	
	connection VC:  
	ip address: 10.131.6.4  
	remote port: 80  
	protocol: vmware-vim https  
	certificate: default  
	datacenter name: VDC  
	admin:  
	max-ports: 8192  
	DVS uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	config status: Enabled  
	operational status: Connected  
	sync status: Complete  
	version: VMware vCenter Server 5.0.0 build-455964  
	vc-uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	

In vCenter you will see the Distributed Switch created under "Home" -> "Inventory" -> "Networking". Here is how it will looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/n1k_under_vc.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/n1k_under_vc.png']);"><img class="alignnone size-full wp-image-2082" title="n1k_under_vc" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/n1k_under_vc.png" alt="n1k under vc Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="934" height="425" /></a>

You can see the Distributed Switch called "switch" and under summary it has Cisco for the Manufacturer.

Next we create a port-profile of type 'ethernet', this will allow us to link physical uplinks to the N1K. Make sure this is mode "trunk", since we are going to allow multiple VLANs to go through it.

	  
	switch(config)# conf t  
	switch(config)# port-profile type ethernet sys-uplink  
	switch(config-port-prof)# switchport mode trunk  
	switch(config-port-prof)# switchport trunk allowed vlan 1  
	switch(config-port-prof)# system vlan 1  
	switch(config-port-prof)# vmware port-group  
	switch(config-port-prof)# no shutdown  
	

Confirm the port-profile exists:

	  
	switch# show run port-profile sys-uplink
	
	!Command: show running-config port-profile sys-uplink  
	!Time: Sat Aug 4 00:15:24 2012
	
	version 4.2(1)SV1(5.1)  
	port-profile type ethernet sys-uplink  
	vmware port-group  
	switchport mode trunk  
	switchport trunk allowed vlan 1  
	no shutdown  
	system vlan 1  
	state enabled  
	

Notice that we have system VLAN set as 1, usually this would be your control and packet VLANs. But like I mentioned, this is just for lab purposes. Next let's create a port-profile of type 'vethernet', this port-profile will allow us to put VMs on it. This will be mode access, since this is where we are going to tag our traffic:

	  
	switch# conf t  
	switch(config)# port-profile type vethernet control-packet  
	switch(config-port-prof)# switchport mode access  
	switch(config-port-prof)# switchport access vlan 1  
	switch(config-port-prof)# 2012 Aug 4 00:38:00 switch %PORT-PROFILE-1-VLAN_CONFIGURED_CONTROL_VLAN: Port-profile is configured to carry the control VLAN 1. Also configure the vlan as system VLAN in this port-profile and other uplink port-profiles that are configured to carry the VLAN for VSM-VEM traffic.  
	2012 Aug 4 00:38:00 switch %PORT-PROFILE-1-VLAN_CONFIGURED_PACKET_VLAN: Port-profile is configured to carry the packet VLAN 1. Also configure the VLAN as system VLAN in this port-profile and other uplink port-profiles that are configured to carry the VLAN for VSM-VEM traffic.
	
	switch(config-port-prof)# no shutdown  
	switch(config-port-prof)# system vlan 1  
	switch(config-port-prof)# vmware port-group  
	switch(config-port-prof)# state enabled  
	switch(config-port-prof)# end  
	

Notice the warning during the creation of the port-profile. Since we were allowing VLAN 1 (our control VLAN) we were suggested to set the system VLAN as well. This make perfect sense and I followed the recommendation. As a side note, by setting a system VLAN on a port-profile means that this VLAN will be allowed to pass through this port-profile even when the VSM is not up. Now to confirm the port-profile creation and it's settings:

	  
	switch# show run port-profile control-packet
	
	!Command: show running-config port-profile control-packet  
	!Time: Sat Aug 4 00:39:11 2012
	
	version 4.2(1)SV1(5.1)  
	port-profile type vethernet control-packet  
	vmware port-group  
	switchport mode access  
	switchport access vlan 1  
	system vlan 1  
	no shutdown  
	state enabled  
	

We should done with the basic setup, so let's commit our configuration

	  
	switch# copy run start  
	[########################################] 100%  
	

Last thing to do is to install the VEM (Virtual Ethernet Module) on the host and connect the host to the N1K. To install the VEM, point your browser to the IP of the VSM and right click on the version of ESX that you need to install the VEM on and save the bundle that are you going to install:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/save_vem_bundle_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/save_vem_bundle_1.png']);"><img class="alignnone size-full wp-image-2088" title="save_vem_bundle_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/save_vem_bundle_1.png" alt="save vem bundle 1 Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="1070" height="819" /></a>

Upload the zip bundle to your host via the datastore browser. After you are done you should be able to  
SSH to the host and install the VEM. First check to see if the file is there,

	  
	~ # ls -l /vmfs/volumes/OI_ISCSI/  
	-rw\---\---- 1 root root 3677460 Aug 4 00:29 cisco-vem-v140-4.2.1.1.5.1.0-3.0.1.zip  
	

Next confirm that no other VEM module exists on the host:

	  
	~ # esxcli software vib list | egrep 'cisco|vem'  
	~ #  
	

Then proceed with the install:

	  
	~ # esxcli software vib install -d /vmfs/volumes/OI_ISCSI/cisco-vem-v140-4.2.1.1.5.1.0-3.0.1.zip  
	Installation Result  
	Message: Operation finished successfully.  
	Reboot Required: false  
	VIBs Installed: Cisco_bootbank_cisco-vem-v140-esx_4.2.1.1.5.1.0-3.0.1  
	VIBs Removed:  
	VIBs Skipped:  
	

Check to make sure it's installed:

	  
	~ # esxcli software vib list | egrep 'cisco|vem'  
	cisco-vem-v140-esx 4.2.1.1.5.1.0-3.0.1 Cisco PartnerSupported 2012-08-06  
	

Next make sure the VEM module is running properly:

	  
	~ # vem status
	
	VEM modules are loaded
	
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch0 128 5 128 1500 vmnic0  
	vSwitch1 128 5 128 1500 vmnic1  
	

That all looks good. Now go ahead and add the host to your N1K. From vCenter go to "Home" -> "Inventory" -> "Networking". Right click on the DVS and select "Add Host". Check the host you want to add and provide an uplink to the sys-uplink:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/add-host-to-n1k.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/add-host-to-n1k.png']);"><img class="alignnone size-full wp-image-2089" title="add-host-to-n1k" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/add-host-to-n1k.png" alt="add host to n1k Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="820" height="622" /></a>

Click "Next", we don't need to migrate any vmkernel interfaces to the N1K. Click "Next" again, we don't need to migrate any of the VMs either. Then click "Finish". Make sure the task succeeds. Then from vCenter go to "Home" -> "Inventory" -> "Networking". Select the N1K switch, and then select the "Hosts" tab, you should see your hosts connected to the N1K there:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/check-host-on-n1k.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/check-host-on-n1k.png']);"><img class="alignnone size-full wp-image-2091" title="check-host-on-n1k" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/check-host-on-n1k.png" alt="check host on n1k Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch" width="929" height="725" /></a>

Then go to the host and make sure the VEM sees the new DVS:

	  
	~ # vem status
	
	VEM modules are loaded
	
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch0 128 8 128 1500 vmnic0  
	vSwitch1 128 1 128 1500  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	switch 256 15 256 1500 vmnic1
	
	VEM Agent (vemdpa) is running  
	

Then go ahead and migrate the first Nic of the N1K VM to the port-group (control-packet) we created. Another side note, each interface is used for different functions (1st vNic for control, 2nd for Management, and 3rd for Packet). They are in alphabetical order. After that make sure the ports are up:

	  
	~ # vemcmd show port  
	LTL VSM Port Admin Link State PC-LTL SGID Vem Port Type  
	18 Eth3/2 UP UP FWD 0 vmnic1  
	49 Veth1 UP UP FWD 0 vCloud_Director_RHEL5.6.eth1  
	50 Veth2 UP UP FWD 0 Nexus1000V-4.2.1.SV1.5.1.eth0  
	

On the N1K, check to make sure the module (host) is there:

	  
	switch# show mod  
	Mod Ports Module-Type Model Status  
	\--- \---\-- -\---\---\---\---\---\---\---\---\---\---\- --\---\---\---\---\---\- --\---\---\----  
	1 0 Virtual Supervisor Module Nexus1000V active *  
	3 248 Virtual Ethernet Module NA other
	
	Mod Sw Hw  
	\--- \---\---\---\---\---\--- \---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	1 4.2(1)SV1(5.1) 0.0  
	3 4.2(1)SV1(5.1) VMware ESXi 5.0.0 Releasebuild-469512 (3.0)
	
	Mod MAC-Address(es) Serial-Num  
	\--- \---\---\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---  
	1 00-19-07-6c-5a-a8 to 00-19-07-6c-62-a8 NA  
	3 02-00-0c-00-03-00 to 02-00-0c-00-03-80 NA
	
	Mod Server-IP Server-UUID Server-Name  
	\--- \---\---\---\---\--- \---\---\---\---\---\---\---\---\---\---\---\--- \---\---\---\---\---\-----  
	1 10.131.6.7 NA NA  
	3 10.131.1.98 80c34566-7e89-b601-b4f9-001a64dc9054 my-esxi-host
	
	* this terminal session  
	

In the logs of the VSM, you will also see the following:

	  
	2012 Aug 6 21:49:28 switch %VEM_MGR-2-VEM_MGR_DETECTED: Host my-esxi-host detected as module 3  
	2012 Aug 6 21:49:28 switch %VEM_MGR-2-MOD_ONLINE: Module 3 is online  
	

And lastly ensure the virtual port for the Control Interface of the VSM is present on the VSM itself. From the above 'vemcmd show port' we can see that Veth2 is the interface that is used for that. So check out that interface:

	  
	switch# show run int veth2
	
	!Command: show running-config interface Vethernet2  
	!Time: Mon Aug 6 20:56:31 2012
	
	version 4.2(1)SV1(5.1)
	
	interface Vethernet2  
	inherit port-profile control-packet  
	description Nexus1000V-4.2.1.SV1.5.1, Network Adapter 1  
	vmware dvport 100 dvswitch uuid "21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97  
	f4"  
	vmware vm mac 0050.56B3.252B  
	

That looks good: it has the correct MAC, it's on the "control-packet" Port-profile and it's the first interface of the N1K VM. Lastly make sure it's up:

	  
	switch# show int veth2  
	Vethernet2 is up  
	Port description is Nexus1000V-4.2.1.SV1.5.1, Network Adapter 1  
	Hardware: Virtual, address: 0050.56b3.252b (bia 0050.56b3.252b)  
	Owner is VM "Nexus1000V-4.2.1.SV1.5.1", adapter is Network Adapter 1  
	Active on module 3  
	VMware DVS port 100  
	Port-Profile is control-packet  
	Port mode is access  
	5 minute input rate 2872 bits/second, 1 packets/second  
	5 minute output rate 21432 bits/second, 23 packets/second  
	Rx  
	28185 Input Packets 105119 Unicast Packets  
	236 Multicast Packets 103947 Broadcast Packets  
	6115703 Bytes  
	Tx  
	712607 Output Packets 52114 Unicast Packets  
	20643 Multicast Packets 2407023 Broadcast Packets 347217 Flood Packets  
	148056022 Bytes  
	236 Input Packet Drops 0 Output Packet Drops  
	

You can also check what VLANs are used:

	  
	~ # vemcmd show port vlans  
	Native VLAN Allowed  
	LTL VSM Port Mode VLAN State Vlans  
	18 Eth3/2 T 1 FWD 1  
	49 Veth1 A 1 FWD 1  
	50 Veth2 A 1 FWD 1  
	

This is all going through VLAN 1. Notice the Mode Column (T stands for Trunk, and A stands for Access). This makes sense, since the physical port is in trunk mode and the virtual ports are in access mode, this corresponds so the port-profile that they are connected to.

If you are not using VLANs upstream or you are connected to an access port, you can setup your type ethernet port-profile be mode access like so:

	  
	switch# show run port-profile sys-uplink-access
	
	!Command: show running-config port-profile sys-uplink-access  
	!Time: Mon Aug 6 22:15:34 2012
	
	version 4.2(1)SV1(5.1)  
	port-profile type ethernet sys-uplink-access  
	vmware port-group  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	system vlan 1  
	state enabled  
	

Then on your host you will see the following:

	  
	~ # vemcmd show port vlans  
	Native VLAN Allowed  
	LTL VSM Port Mode VLAN State Vlans  
	18 Eth3/2 A 1 FWD 1  
	49 Veth1 A 1 FWD 1  
	50 Veth2 A 1 FWD 1  
	

Notice the Mode of the physical port is 'A', which in production will never work out, but in the lab it will be fine.

