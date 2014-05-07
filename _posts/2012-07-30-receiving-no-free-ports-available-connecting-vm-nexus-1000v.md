---
title: 'Receiving &#8220;No Free Ports&#8221; Available when Connecting a VM to the Nexus 1000v'
author: Karim Elatov
layout: post
permalink: /2012/07/receiving-no-free-ports-available-connecting-vm-nexus-1000v/
dsq_thread_id:
  - 1404673070
categories:
  - Networking
  - VMware
tags:
  - Ephemeral Port Binding
  - Limit Exceeded
  - max ports dvs
  - Nexus 1000v
  - powercli dvs
  - ProxySwitch
  - Static Port Binding
---
I was trying to get a VM up on the network and I getting getting an error message saying that I don&#8217;t have any free ports on my Nexus 1000v Distributed Switch. Looking at the vCenter logs

> Windows Server 2003 &#8211; C:\Documents and Settings\All Users\Application Data\VMware\VMware VirtualCenter\Logs  
> Windows Server 2008 &#8211; C:\ProgramData\VMware\VMware VirtualCenter\Logs

I saw the following:

	  
	\[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2\] \[MoDVPortGroup::GetFreePortInt\] No free port found in the portgroup [My\_N1K\_DV_PortGroup]  
	\[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2\] \[MoDVSwitch::ProcessVmConfigSpecInt\] No free portin the portgroup . Rolling back the previously reserved ports  
	\[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2]  (My\_Test\_VM) Unexpected exception (vim.fault.ResourceNotAvailable) while reconfiguring VM. Aborting.  
	

Looking on the host, I would see the following in the hostd logs:

	  
	Jul 2 23:39:33 shell[1352806]: [2012-07-02 21:18:45.995 410C2B90 info 'Vmomi' opID=0BDFBD77-0000242A-18] Result:  
	Jul 2 23:39:33 shell[1352806]: (vim.fault.PlatformConfigFault) {  
	Jul 2 23:39:33 shell[1352806]: dynamicType = ,  
	Jul 2 23:39:33 shell[1352806]: faultCause = (vmodl.MethodFault) null,  
	Jul 2 23:39:33 shell[1352806]: text = "Unable to Add Port; Status(bad0006)= Limit exceeded",  
	Jul 2 23:39:33 shell[1352806]: msg = "",  
	Jul 2 23:39:33 shell[1352806]: }  
	

I was getting a &#8216;Limit exceeded&#8217; message. Checking out the &#8216;esxcfg-vswitch -l&#8217; output, I saw the following:

	  
	$ esxcfg-vswitch -l  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	N1K_DVS 256 155 256 1500 vmnic9,vmnic7
	
	DVPort ID In Use Client  
	2063 1 vmnic7  
	2064 1 vmnic9  
	2065 0  
	2066 0  
	2067 0  
	2068 0  
	2069 0  
	2070 0  
	2071 0  
	2072 0  
	2073 0  
	..  
	..  
	19980 1 VM1 ethernet2  
	20537 1 VM1 ethernet1  
	19979 1 VM1 ethernet0  
	1927 1 VM2 ethernet0  
	11221 1 VM2 ethernet0  
	

We can see that the &#8220;Used Ports&#8221; are showing as 155, and that is a little misleading. Since this is a DVS we have different types of port binding. The different kinds of Port Bindings are described in VMware <a href="http://kb.vmware.com/kb/1022312" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1022312']);">KB 1022312</a>. Since this is a Nexus port-profile, it is created with static port binding (same behavior with VMware DVS PortGroups). This means that, from the KB:

> When you connect a virtual machine to a port group configured with static binding, a port is immediately assigned and reserved for it, guaranteeing connectivity at all times. The port is disconnected only when the virtual machine is removed from the port group.

So even when VMs are turned off, they are still taking up ports. To figure out how many ports are reserved, you can use the &#8216;net-dvs&#8217; command. Like so:

	  
	$ net-dvs -l | grep 'port ' | wc -l  
	256  
	

Checking each VMX file for a generated MAC address and counting them, I saw the following:

	  
	$ find /vmfs/volumes -name '*.vmx' -exec grep generatedAddress {} \; | wc -l  
	253  
	

This makes sense, other ports are used for internal communication and we are definitely hitting the 256 port limit per host. We had two things we could try, one is to change the Nexus 1000v port-profiles to ephemeral (this way only powered on VMs will reserve ports). To do this, check out the <a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_2_1_s_v_1_4/port_profile/configuration/guide/n1000v_portprof_2create.html#wp1132232" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_2_1_s_v_1_4/port_profile/configuration/guide/n1000v_portprof_2create.html#wp1132232']);">Cisco Nexus 1000V Port Profile Configuration Guide, Release 4.2(1) SV1(4)</a>. From the Cisco page:

> EXAMPLES  
> This example shows how to configure the ephemeral port binding type for the existing port profile named ephemeral-pp:
> 
> n1000v# config t  
> n1000v(config)# port-profile ephemeral-pp  
> n1000v(config-port-prof)# port-binding ephemeral  
> n1000v(config-port-prof)#

One note regarding this, you have migrate all the VMs off the port-profile before making this change. This can be accomplished by creating a new port-profile and then using the &#8220;Migrate Virtual Machines&#8221; function from vCenter.  
I was actually in a critical situation and didn&#8217;t want to make that many changes. Another way to get around the &#8220;Limit Exceeded&#8221; error is to increase the &#8220;Num Ports&#8221; or the &#8220;Max Ports&#8221; on the ProxySwitch. Don&#8217;t confuse this with the Max ports for the whole DVS. From the <a href="http://www.vmware.com/pdf/vsphere4/r41/vsp_41_config_max.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere4/r41/vsp_41_config_max.pdf']);">Maximums Guide for 4.1</a>:

> **vNetwork Standard and Distributed Switch**  
> Total virtual network switch ports per host (vDS and vSS ports) 4096 \*4\*  
> Ports per distributed switch 20000
> 
> *4th Note&#8211; Default is 256 with a maximum of 15 VDS’s running concurrently. If the number of ports is increased to 4096, then only one VDS can exist on the host.

So you can have a total of 20000 ports on the DVS (BTW VMware <a href="http://kb.vmware.com/kb/1038193" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1038193']);">KB 1038193</a> talks about increasing that value, since by default it&#8217;s 8192 on DVS 4.1 and below), but we are changing the max ports for the ProxySwitch (which exists on each host when using the Distributed switch). Another person was actually trying to do the same thing in the VMware communities. Here is a <a href="http://communities.vmware.com/message/1997179" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/message/1997179']);">link</a> to his post. He had two methods, one it to edit the vCenter Database and the other was via a Powercli script. I took his script and the script from the above KB and made another one, it looked like this:

	  
	Connect-VIServer -server 127.0.0.1
	
	$dvs = Get-VirtualSwitch -Distributed -Name DVSName | Get-View  
	$cfg = New-Object -TypeName VMware.Vim.DVSConfigSpec  
	foreach ($myhost in $dvs.Config.Host) {  
	$host_conf = New-Object -TypeName VMware.Vim.DistributedVirtualSwitchHostMemberConfigSpec  
	$host_conf.host = $myhost.config.host  
	$host_conf.maxProxySwitchPorts = 512  
	$host_conf.operation = 'edit'  
	$cfg.host +=$host_conf  
	}  
	$cfg.configVersion = $dvs.config.configVersion  
	$dvs.ReconfigureDvs_Task($cfg)  
	

I tested that on a regular VMware DVS and it worked fine. To use the above PowerCLI script you have to use version 4.1.1, that version has enhanced support for Distributed Switches (you can read more about it at the VMware Blog entitled &#8220;<a href="http://blogs.vmware.com/vipowershell/2010/12/enhanced-support-for-distributed-switches-in-powercli-411.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vipowershell/2010/12/enhanced-support-for-distributed-switches-in-powercli-411.html']);">Enhanced Support for Distributed Switches in PowerCLI 4.1.1</a>&#8220;).  It did require a restart but it worked. After the script the &#8216;esxcfg-vswitch -l&#8217;, looked like this:

	  
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks  
	dVswitch 512 40 512 1500 vmnic3  
	

The sad thing was that it didn&#8217;t work for the Nexus 1000v. So I edited the VC_DB and then it worked. Here is how my MS-SQL Management Studio looked like prior to the change:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/07/sql-mgmt-studio.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/07/sql-mgmt-studio.png']);"><img class="alignnone size-full wp-image-1747" title="sql-mgmt-studio" src="http://virtuallyhyper.com/wp-content/uploads/2012/07/sql-mgmt-studio.png" alt="sql mgmt studio Receiving No Free Ports Available when Connecting a VM to the Nexus 1000v" width="1022" height="726" /></a>

The cool thing is that with vCenter 5.0 you can now do this through the vSphere Client. You can go to:

> Host -> Configuration -> Networking -> vSphere Distributed Switch -> Properties

It looks like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/07/VC_5_Change_Ports_per_host.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/07/VC_5_Change_Ports_per_host.png']);"><img class="alignnone size-full wp-image-1748" title="VC_5_Change_Ports_per_host" src="http://virtuallyhyper.com/wp-content/uploads/2012/07/VC_5_Change_Ports_per_host.png" alt="VC 5 Change Ports per host Receiving No Free Ports Available when Connecting a VM to the Nexus 1000v" width="1022" height="527" /></a>

A reboot of each host is required if done after the creation of the DVS. <a href="http://kb.vmware.com/kb/2004075" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2004075']);">VMware KB 2004075</a> has more instructions on changing the Max ProxySwitch Ports when using vCenter 5.0. Here is a Table of the versions that I was on:

<table border="0">
  <tr>
    <td>
      ESX
    </td>
    
    <td>
      vCenter
    </td>
    
    <td>
      Nexus 1000v
    </td>
  </tr>
  
  <tr>
    <td>
      build 721871 ESXi4.1EP3
    </td>
    
    <td>
      build 491557 VC 4.1U2
    </td>
    
    <td>
       VSM 4.2(1)SV1(4b)
    </td>
  </tr>
</table>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/07/receiving-no-free-ports-available-connecting-vm-nexus-1000v/" title=" Receiving &#8220;No Free Ports&#8221; Available when Connecting a VM to the Nexus 1000v" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Ephemeral Port Binding,Limit Exceeded,max ports dvs,Nexus 1000v,powercli dvs,ProxySwitch,Static Port Binding,blog;button:compact;">I was trying to get a VM up on the network and I getting getting an error message saying that I don&#8217;t have any free ports on my Nexus 1000v...</a>
</p>