---
title: After Updating N1K to Version 1.5, Incorrect VLAN Information Displayed Under DV Uplink Port Groups but not Under DV Port Groups
author: Karim Elatov
layout: post
permalink: /2012/05/after-updating-n1k-version-1-5-incorrect-vlan-information-displayed-under-dv-uplink-port-groups-under-dv-port-groups/
dsq_thread_id:
  - 1415995332
categories:
  - Networking
  - VMware
tags:
  - DV Port Group
  - DV Uplink Port Group
  - N1K
  - Nexus 1000v
  - show tech-support svs
  - VLAN ID
---
I had recently ran into an interesting issue with the nexus 1000v switch. After upgrading from 4.2(1)SV1(4a) to 4.2(1)SV1(5.1). Uplink ports are not reporting VLAN IDs correctly when viewed from the VSM->Uplink->Ports tab->VLAN-ID Column. However, the VLAN IDs ARE reporting correctly on the individual VM Distributed PortGroups (VSM->DV-PortGroup->Ports tab->VLAN-ID Column). Here is how the DV Uplink Port Group looked like:
![uplink_1](http://virtuallyhyper.com/wp-content/uploads/2012/04/uplink_1.jpg)
And here is how the DV Port Group looked like:
![dportgroup_1](http://virtuallyhyper.com/wp-content/uploads/2012/04/dportgroup_11.jpg)

We grabbed a '*show tech-support svs*' from the N1K. More information on what a '*show tech-support svs*' is, can be found at the following cisco [web-page](http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_0/troubleshooting/configuration/guide/trouble_18b4contact.html). From the logs we saw the following messages that corresponded to the DV Uplink port Group:


	Event:E_DEBUG, length:351, at 951023 usecs after Fri Apr 13 14:46:54 2012
	[102] msp_vppm_handle_port_profile_update_resp(434): (ERR) profile DV_Uplink_PG update failed: Syserr code: 0x41b1001d,
	user string:
	internal string:


We contacted Cisco and they had identified a known bug on the N1K. If you have cisco account you can check out bug [2025321](http://tools.cisco.com/Support/BugToolKit/search/getBugDetails.do?method=fetchBugDetails&bugId=CSCtz24512))

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>

  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESXi Hosts Show Up as a VEM Module with All Zeros for UUIDs on the Nexus 1000v" href="http://virtuallyhyper.com/2013/01/esxi-hosts-show-up-as-a-vem-module-with-all-zeros-for-uuids-on-the-nexus-1000v/" rel="bookmark">ESXi Hosts Show Up as a VEM Module with All Zeros for UUIDs on the Nexus 1000v</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Nexus 1000v Disconnects from vCenter" href="http://virtuallyhyper.com/2012/09/nexus-1000v-disconnects-from-vcenter/" rel="bookmark">Nexus 1000v Disconnects from vCenter</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Common Commands for Nexus 1000v VSM" href="http://virtuallyhyper.com/2012/08/common-commands-for-nexus-1000v-vsm/" rel="bookmark">Common Commands for Nexus 1000v VSM</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Receiving "No Free Ports" Available when Connecting a VM to the Nexus 1000v" href="http://virtuallyhyper.com/2012/07/receiving-no-free-ports-available-connecting-vm-nexus-1000v/" rel="bookmark">Receiving "No Free Ports" Available when Connecting a VM to the Nexus 1000v</a>
    </li>
  </ul>
</div>

