---
title: Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch
author: Karim Elatov
layout: post
permalink: /2012/09/fixing-a-ghostedinconsistent-distributed-virtual-switch-by-migrating-to-a-standard-virtual-switch/
dsq_thread_id:
  - 1404761763
categories:
  - Networking
  - VMware
tags:
  - Distributed Virtual Switch
  - esxcfg-vmknic
  - esxcfg-vswitch
  - Inconsistent DVS
  - Invalid Backing
  - locked port time out
  - out-of-sync DVS
  - Standard Virtual Switch
---
There are a couple of steps to this process. First you need to determine if you have an inconsistent/broken/ghosted DVS.

### Determine if you have a ghosted DVS

1. Under &#8220;Host and Clusters&#8221; if you select a host and then go to summary you will see a message similar to this:

> The distributed Virtual Switch corresponding to the proxy switches d5 6e 22 50 dd f2 94 7b-a6 1f b2 c2 e6 aa 0f bf on the host does not exist in vCenter or does not contain the host.

This is discussed in VMware KB <a href="http://kb.vmware.com/kb/1017558" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1017558']);">1017558</a> and in &#8220;<a href="http://www.ntpro.nl/blog/archives/1283-vSphere-DvSwitch-caveats-and-best-practices!.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ntpro.nl/blog/archives/1283-vSphere-DvSwitch-caveats-and-best-practices!.html']);">vSphere DvSwitch caveats and best practices!</a>&#8221;

2. Under &#8220;Host and Clusters&#8221; if you select a Host and then go to Configuration -> Networking -> vNetwork Distributed Switch

You will see something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/dvs_no_uplinks.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/dvs_no_uplinks.png']);"><img class="alignnone size-full wp-image-3817" title="dvs_no_uplinks" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/dvs_no_uplinks.png" alt="dvs no uplinks Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="661" height="307" /></a>

But when you login directly to the host via ssh and run &#8216;esxcfg-vswitch -l&#8217; you will see uplinks attached to the DVS. It will look something like this:

	  
	~ # esxcfg-vswitch -l  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvSwitch 512 42 512 1500 vmnic3,vmnic2
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 1 vmnic2  
	98 0  
	129 1 vmk0  
	130 1 vmk1  
	131 1 vmk2  
	200 1 vm2.eth0  
	201 1 test.eth0  
	

3. If you Edit Setting of your VMs and select the Network Card, under Network Label it shows &#8220;Invalid Backing&#8221;

Taken from <a href="http://communities.vmware.com/thread/323439" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/323439']);">this</a> VMware Communities page. Here is how it looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/VM_Missing_BackingDevice.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/VM_Missing_BackingDevice.png']);"><img class="alignnone size-full wp-image-3818" title="VM_Missing_BackingDevice" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/VM_Missing_BackingDevice.png" alt="VM Missing BackingDevice Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="690" height="437" /></a>

4. Don&#8217;t confuse this as an &#8216;out-of-sync&#8217; scenario

The blog post &#8220;<a href="http://sostech.wordpress.com/2011/06/06/vds-out-of-sync/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sostech.wordpress.com/2011/06/06/vds-out-of-sync/']);">vDS out of sync</a>&#8221; talks about how it looks like. Basically you might see something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/out-of-sync-dvs.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/out-of-sync-dvs.jpg']);"><img class="alignnone size-full wp-image-3819" title="out-of-sync-dvs" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/out-of-sync-dvs.jpg" alt="out of sync dvs Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="640" height="131" /></a>

If the host is up, it should synchronize in 5 minutes, or you can manually synchronize, by right clicking on the host and selecting &#8220;Rectify vNetwork Distributed Switch Host&#8221;, it looks something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/rectify_out_of_sync_dvs.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/rectify_out_of_sync_dvs.jpg']);"><img class="alignnone size-full wp-image-3820" title="rectify_out_of_sync_dvs" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/rectify_out_of_sync_dvs.jpg" alt="rectify out of sync dvs Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="394" height="491" /></a>

Also one more note, don&#8217;t confuse the dvs synchronization with the locked ports time out. The default for that is 24 hours and that can be changed. To change the default time out for locked ports follow the instructions laid out in VMware KB <a href="http://kb.vmware.com/kb/1010913" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1010913']);">1010913</a>

Now, once you have identified an &#8220;Inconsistent&#8221; DVS, let&#8217;s start fixing it.

### Create a Standard Virtual Switch and Migrate an uplink to it

Most of these steps are laid out in &#8220;<a href="http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf']);">VMware vNetwork Distributed Switch: Migration and Configuration</a>&#8221;

1. Create a new Stardard Virtual Switch

	  
	~ # esxcfg-vswitch -a vSwitch3  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch3 128 1 128 1500
	
	PortGroup Name VLAN ID Used Ports Uplinks
	
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 40 512 1500 vmnic2,vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 1 vmnic2  
	...  
	...  
	

2. Remove the Uplink from the Distributed Virtual Switch and add it to the newly created Standard switch

	  
	~ # esxcfg-vswitch -Q vmnic2 -V 97 dvswitch  
	~ # esxcfg-vswitch -L vmnic2 vSwitch3  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch3 128 2 128 1500 vmnic2
	
	PortGroup Name VLAN ID Used Ports Uplinks
	
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 40 512 1500 vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 0  
	...  
	...  
	

### Create the necessary Port Groups

1. Create the appropriate Port Groups on the Standard Virtual Switch  
Let say you had four types of networks: Mgmt (vlan 100), vMotion (vlan 101), NFS (vlan 102), and VM (103). So let&#8217;s create 4 different Port Groups with the appropriate VLAN Tags.

	  
	~ # esxcfg-vswitch -A Mgmt vSwitch3  
	~ # esxcfg-vswitch -v 100 -p Mgmt vSwitch3  
	~ # esxcfg-vswitch -A vMotion vSwitch3  
	~ # esxcfg-vswitch -v 101 -p vMotion vSwitch3  
	~ # esxcfg-vswitch -A NFS vSwitch3  
	~ # esxcfg-vswitch -v 102 -p NFS vSwitch3  
	~ # esxcfg-vswitch -A VM vSwitch3  
	~ # esxcfg-vswitch -v 103 -p VM vSwitch3  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch3 128 2 128 1500 vmnic2
	
	PortGroup Name VLAN ID Used Ports Uplinks  
	VM 103 0 vmnic2  
	NFS 102 0 vmnic2  
	vMotion 101 0 vmnic2  
	Mgmt 100 0 vmnic2
	
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 40 512 1500 vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 0  
	...  
	...  
	

### Migrate your vmkernel interfaces from the Ghosted Distributed Virtual Switch to the Standard switch

1. Determine the IP settings of your current vmkernel interfaces

	  
	~ # esxcfg-vmknic -l  
	Interface DVPort IP Address Netmask Broadcast MAC Address MTU Enabled  
	vmk0 129 1.1.1.2 255.255.255.0 1.1.1.255 00:50:56:17:21:df 1500 true  
	vmk1 130 1.1.2.2 255.255.255.0 1.1.2.255 00:50:56:70:4c:6f 1500 true  
	vmk2 131 1.1.3.2 255.255.255.0 1.1.3.255 00:50:56:75:4c:6f 1500 true
	
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch3 128 2 128 1500 vmnic2
	
	PortGroup Name VLAN ID Used Ports Uplinks  
	VM 103 0 vmnic2  
	NFS 102 0 vmnic2  
	vMotion 101 0 vmnic2  
	Mgmt 100 0 vmnic2
	
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 40 512 1500 vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 0  
	98 0  
	99 0  
	100 0  
	101 0  
	102 0  
	129 1 vmk0  
	130 1 vmk1  
	131 1 vmk2  
	...  
	...  
	

So vmk0 is Mgmt, vmk1 is vMotion, and vmk2 is NFS.

2. Remove the vmkernel interfaces from the Ghosted Distributed Virtual Switch  
**NOTE** If you were doing the above steps via an SSH session, the below commands will disrupt your Management interface. If you have a DRAC/ILO ( any out-of-band management tool) please use them. This will NOT disrupt your VM traffic.  
	  
	~ # esxcfg-vmknic -d -v 129 -s dvswitch  
	~ # esxcfg-vmknic -d -v 130 -s dvswitch  
	~ # esxcfg-vmknic -d -v 131 -s dvswitch  
	~ # esxcfg-vswitch -l  
	Switch Name Num Ports Used Ports Configured Ports MTU Uplinks  
	vSwitch3 128 2 128 1500 vmnic2
	
	PortGroup Name VLAN ID Used Ports Uplinks  
	VM 103 0 vmnic2  
	NFS 102 0 vmnic2  
	vMotion 101 0 vmnic2  
	Mgmt 100 0 vmnic2
	
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 40 512 1500 vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 0  
	98 0  
	99 0  
	100 0  
	101 0  
	102 0  
	129 0  
	130 0  
	131 0  
	..  
	..  
	

You can see that they are gone from the DvSwitch.

3. Recreate the vmkernel interfaces on the standard virtual switch

	  
	~ # esxcfg-vmknic -a -i 1.1.1.2 -n 255.255.255.0 -p Mgmt  
	[2012-09-22 16:39:03 'NotifyDCUI' warning] Notifying the DCUI of configuration change  
	~ # esxcfg-vmknic -a -i 1.1.2.2 -n 255.255.255.0 -p vMotion  
	[2012-09-22 16:39:21 'NotifyDCUI' warning] Notifying the DCUI of configuration change  
	~ # esxcfg-vmknic -a -i 1.1.3.2 -n 255.255.255.0 -p NFS  
	[2012-09-22 16:39:33 'NotifyDCUI' warning] Notifying the DCUI of configuration change  
	~ # esxcfg-vmknic -l  
	Interface Port Group/DVPort IP Address Netmask Broadcast MAC Address MTU Enabled  
	vmk0 Mgmt 1.1.1.2 255.255.255.0 1.1.1.255 00:50:56:7c:ec:ca 1500 true  
	vmk1 vMotion 1.1.2.2 255.255.255.0 1.1.2.255 00:50:56:7e:69:07 1500 true  
	vmk3 NFS 1.1.3.2 255.255.255.0 1.1.3.255 00:50:56:73:5a:3b 1500 true  
	

Notice that under the &#8220;Port Group/DVPort&#8221; column it has the name of the port group from the standard virtual switch instead of the dvPort ID. That is when you know you are on the Standard Virtual Switch instead of the DvSwitch.

### Migrate the VMs off the DvSwitch

If vCenter is up and operational go to &#8220;Inventory&#8221; -> &#8220;Networking&#8221; -> Select your DvSwitch -> Click on the &#8220;Virtual Machine&#8221; Tab. This will list all of your VMs. Also on the Left side of the panel it will list all of your Port Groups (standard and distributed). From this screen you can select multiple VMs, then Drag and Drop them on the Port Group that we called &#8220;VM&#8221;. If you had multiple VM Port groups then you will have to Drag and Drop them to their corresponding newly created standard virtual switch port groups.

If vCenter is not up, then login directly to the host with the vShpere Client and &#8220;Edit Settings&#8221; of the VM and change the &#8220;Network Label&#8221; to the Port Group that you created on the Standard Virtual Switch

After you are done migrating all the VMs off the &#8216;esxcfg-vswitch -l&#8217; output should look like this:

	  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 1 512 1500 vmnic3
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 0  
	98 0  
	99 0  
	100 0  
	101 0  
	102 0  
	129 0  
	130 0  
	131 0  
	200 0  
	201 0  
	

Remember when we started it looks like this:

	  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvSwitch 512 42 512 1500 vmnic3,vmnic2
	
	DVPort ID In Use Client  
	96 1 vmnic3  
	97 1 vmnic2  
	98 0  
	129 1 vmk0  
	130 1 vmk1  
	131 1 vmk2  
	200 1 vm2.eth0  
	201 1 test.eth0  
	

### Remove any left over Uplinks from the DvSwitch

Now that we have migrated everything to the standard switch we need to make sure nothing is using the DvSwitch so we can actually remove it from the host. In my case I only had vmnic3, so I ran the following to remove it:

	  
	~ # esxcfg-vswitch -Q vmnic3 -V 96 dvswitch  
	~ # esxcgf-vswitch -l  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dvswitch 512 0 512 1500 
	
	DVPort ID In Use Client  
	96 0  
	97 0  
	98 0  
	99 0  
	100 0  
	101 0  
	102 0  
	129 0  
	130 0  
	131 0  
	200 0  
	201 0  
	

Notice that your &#8220;Used Ports&#8221; should be &#8217;0&#8242;.

### Remove the DvSwitch from the host

When you are in vCenter and you go to &#8220;Host and Clusters&#8221; -> Select ESXi Host -> Configuration -> Networking -> &#8220;vNetwork Distributed Switch&#8221; it looks like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/vcenter_dvs_view.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/vcenter_dvs_view.png']);"><img class="alignnone size-full wp-image-3821" title="vcenter_dvs_view" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/vcenter_dvs_view.png" alt="vcenter dvs view Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="694" height="93" /></a>

But when you go directly to the host and you go to &#8220;Inventory&#8221; -> Select ESXi Host -> Configuration -> Networking -> &#8220;vNetwork Distributed Switch&#8221;, you will see this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/host_view_dvs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/host_view_dvs.png']);"><img class="alignnone size-full wp-image-3822" title="host_view_dvs" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/host_view_dvs.png" alt="host view dvs Fixing a Ghosted/Inconsistent Distributed Virtual Switch by Migrating to a Standard Virtual Switch" width="664" height="105" /></a>

Notice that there is a &#8220;Remove&#8221; button available. Go ahead and click &#8220;Remove&#8221;, that will remove the Ghosted DVS from the host. If it gives you an error saying that it&#8217;s in use ( and your esxcfg-vswitch -l output showed 0 &#8220;Used Ports&#8221;) then you might have a locked/shadow port. As I mentioned above you can:

*   wait 24 hours for that to clear
*   edit vpxd.cfg and change the default time out and restart vCenter (if it&#8217;s up)
*   reboot the host

Usually the last one fixes the shadow ports issue. Now you are completely off the Ghosted DVS. If you want to re-create the DVS or re-add the host back to the DVS and migrate everything back then you can follow the instructions laid out in &#8220;<a href="http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/vsphere-vnetwork-ds-migration-configuration-wp.pdf']);">VMware vNetwork Distributed Switch: Migration and Configuration</a>&#8220;

