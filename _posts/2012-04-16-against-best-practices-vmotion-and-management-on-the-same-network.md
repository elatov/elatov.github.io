---
title: 'Against Best Practices: vMotion and Management on the Same Network'
author: Joe Chan
layout: post
permalink: /2012/04/against-best-practices-vmotion-and-management-on-the-same-network/
dsq_thread_id:
  - 1404673824
categories:
  - Networking
  - VMware
tags:
  - advanced configuration
  - best practice
  - management
  - routing table
  - tips
  - vmk
  - vmkernel
  - vmotion
---
I recently spoke with someone who was running into the <a title="vMotion Causes Unicast Flooding" href="http://virtuallyhyper.com/index.php/2012/03/vmotion-causes-unicast-flooding/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/index.php/2012/03/vmotion-causes-unicast-flooding/']);">vMotion Causes Unicast Flooding</a> issue Karim blogged about.

As he states, it is mentioned in many of VMware&#8217;s best practice documents that vMotion should on a seperate network devoted to vMotion (for example this [ESXi 4.1 server configuration guide][1]):

> Keep the vMotion connection on a separate network devoted to vMotion. When migration with vMotion  
> occurs, the contents of the guest operating system’s memory is transmitted over the network. You can do this either by using VLANs to segment a single physical network or separate physical networks (the latter is preferable).

and if you don&#8217;t follow the best practices and place vMotion and Management traffic on the same network, you may see vMotion traffic getting sent out the Management interface.

If you do not want to adhere to best practices and would like to avoid that problem, one thing you can try is setting in the advanced settings of the ESX host (Configuration tab -> Advanced Settings -> Migrate), Migrate.BindToVmknic to 1.

For the folks who live in the command line, here is how you set Migrate.BindToVmknic to 1 via the console/SSH.

	  
	~ # esxcfg-advcfg -s 1 /Migrate/BindToVmknic  
	~ #  
	

Verify that it is actually set properly:

	  
	~ # esxcfg-advcfg -g /Migrate/BindToVmknic  
	Value of BindToVmknic is 1  
	

or

	  
	~ # grep Migrate /etc/vmware/esx.conf  
	/adv/Migrate/BindToVmknic = "1"  
	

This should force the vMotion to go over the vmkernel port that vMotion is enabled on, rather than consulting the vmkernel routing table to determine which vmkernel interface to send traffic out.

Please keep in mind that this is still not something I would recommend. But if you have some reason where you ABSOLUTELY CAN NOT separate the vMotion network onto a different network, this little tip may help you configure your host so that vMotion will behave as expected.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/against-best-practices-vmotion-and-management-on-the-same-network/" title=" Against Best Practices: vMotion and Management on the Same Network" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:advanced configuration,best practice,management,routing table,tips,vmk,vmkernel,vmotion,blog;button:compact;">I recently spoke with someone who was running into the vMotion Causes Unicast Flooding issue Karim blogged about. As he states, it is mentioned in many of VMware&#8217;s best practice...</a>
</p>

 [1]: http://www.vmware.com/pdf/vsphere4/r41/vsp_41_esxi_server_config.pdf