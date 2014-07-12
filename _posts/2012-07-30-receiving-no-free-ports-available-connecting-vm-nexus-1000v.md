---
published: true
title: 'Receiving "No Free Ports" Available when Connecting a VM to the Nexus 1000v'
author: Karim Elatov
layout: post
permalink: /2012/07/receiving-no-free-ports-available-connecting-vm-nexus-1000v/
dsq_thread_id:
  - 1404673070
categories: ['networking', 'vmware']
tags: ['dvs_port_binding', 'dvs', 'nexus_1000v', 'powercli']
---

I was trying to get a VM up on the network and I getting getting an error message saying that I don't have any free ports on my Nexus 1000v Distributed Switch. Looking at the vCenter logs

> Windows Server 2003 - C:\Documents and Settings\All Users\Application Data\VMware\VMware VirtualCenter\Logs
> Windows Server 2008 - C:\ProgramData\VMware\VMware VirtualCenter\Logs

I saw the following:


	[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2] [MoDVPortGroup::GetFreePortInt] No free port found in the portgroup [My_N1K_DV_PortGroup]
	[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2] [MoDVSwitch::ProcessVmConfigSpecInt] No free portin the portgroup . Rolling back the previously reserved ports
	[2012-07-03 13:46:22.586 06604 error 'App' opID=322CAECC-000000A2]  (My_Test_VM) Unexpected exception (vim.fault.ResourceNotAvailable) while reconfiguring VM. Aborting.


Looking on the host, I would see the following in the hostd logs:


	Jul 2 23:39:33 shell[1352806]: [2012-07-02 21:18:45.995 410C2B90 info 'Vmomi' opID=0BDFBD77-0000242A-18] Result:
	Jul 2 23:39:33 shell[1352806]: (vim.fault.PlatformConfigFault) {
	Jul 2 23:39:33 shell[1352806]: dynamicType = ,
	Jul 2 23:39:33 shell[1352806]: faultCause = (vmodl.MethodFault) null,
	Jul 2 23:39:33 shell[1352806]: text = "Unable to Add Port; Status(bad0006)= Limit exceeded",
	Jul 2 23:39:33 shell[1352806]: msg = "",
	Jul 2 23:39:33 shell[1352806]: }


I was getting a 'Limit exceeded' message. Checking out the 'esxcfg-vswitch -l' output, I saw the following:


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


We can see that the "Used Ports" are showing as 155, and that is a little misleading. Since this is a DVS we have different types of port binding. The different kinds of Port Bindings are described in VMware [KB 1022312](http://kb.vmware.com/kb/1022312). Since this is a Nexus port-profile, it is created with static port binding (same behavior with VMware DVS PortGroups). This means that, from the KB:

> When you connect a virtual machine to a port group configured with static binding, a port is immediately assigned and reserved for it, guaranteeing connectivity at all times. The port is disconnected only when the virtual machine is removed from the port group.

So even when VMs are turned off, they are still taking up ports. To figure out how many ports are reserved, you can use the 'net-dvs' command. Like so:


	$ net-dvs -l | grep 'port ' | wc -l
	256


Checking each VMX file for a generated MAC address and counting them, I saw the following:


	$ find /vmfs/volumes -name '*.vmx' -exec grep generatedAddress {} \; | wc -l
	253


This makes sense, other ports are used for internal communication and we are definitely hitting the 256 port limit per host. We had two things we could try, one is to change the Nexus 1000v port-profiles to ephemeral (this way only powered on VMs will reserve ports). To do this, check out the [Cisco Nexus 1000V Port Profile Configuration Guide, Release 4.2(1) SV1(4)](http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_2_1_s_v_1_4/port_profile/configuration/guide/n1000v_portprof_2create.html#wp1132232). From the Cisco page:

> EXAMPLES
> This example shows how to configure the ephemeral port binding type for the existing port profile named ephemeral-pp:
>
> n1000v# config t
> n1000v(config)# port-profile ephemeral-pp
> n1000v(config-port-prof)# port-binding ephemeral
> n1000v(config-port-prof)#

One note regarding this, you have to migrate all the VMs off the port-profile before making this change. This can be accomplished by creating a new port-profile and then using the "Migrate Virtual Machines" function from vCenter.
I was actually in a critical situation and didn't want to make that many changes. Another way to get around the "Limit Exceeded" error is to increase the "Num Ports" or the "Max Ports" on the ProxySwitch. Don't confuse this with the Max ports for the whole DVS. From the [Maximums Guide for 4.1](http://www.vmware.com/pdf/vsphere4/r41/vsp_41_config_max.pdf):

> **vNetwork Standard and Distributed Switch**
> Total virtual network switch ports per host (vDS and vSS ports) 4096 *4*
> Ports per distributed switch 20000
>
> *4th Note- Default is 256 with a maximum of 15 VDS’s running concurrently. If the number of ports is increased to 4096, then only one VDS can exist on the host.

So you can have a total of 20000 ports on the DVS (BTW VMware [link](http://kb.vmware.com/kb/1038193) to his post. He had two methods, one it to edit the vCenter Database and the other was via a Powercli script. I took his script and the script from the above KB and made another one, it looked like this:


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


I tested that on a regular VMware DVS and it worked fine. To use the above PowerCLI script you have to use version 4.1.1, that version has enhanced support for Distributed Switches (you can read more about it at the VMware Blog entitled "[Enhanced Support for Distributed Switches in PowerCLI 4.1.1](http://blogs.vmware.com/vipowershell/2010/12/enhanced-support-for-distributed-switches-in-powercli-411.html)").  It did require a restart but it worked. After the script the 'esxcfg-vswitch -l', looked like this:


	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks
	dVswitch 512 40 512 1500 vmnic3


The sad thing was that it didn't work for the Nexus 1000v. So I edited the VC_DB and then it worked. Here is how my MS-SQL Management Studio looked like prior to the change:

![sql-mgmt-studio](https://github.com/elatov/uploads/raw/master/2012/07/sql-mgmt-studio.png)

The cool thing is that with vCenter 5.0 you can now do this through the vSphere Client. You can go to:

> Host -> Configuration -> Networking -> vSphere Distributed Switch -> Properties

It looks like this:

![VC_5_Change_Ports_per_host](https://github.com/elatov/uploads/raw/master/2012/07/VC_5_Change_Ports_per_host.png)

A reboot of each host is required if done after the creation of the DVS. [VMware KB 2004075](http://kb.vmware.com/kb/2004075) has more instructions on changing the Max ProxySwitch Ports when using vCenter 5.0. Here is a Table of the versions that I was on:

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

