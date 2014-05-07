---
title: VLAN issue with IBM VFA, be2net driver, and DVS
author: Joe Chan
layout: post
permalink: /2012/04/vlan-issue-with-ibm-vfa-be2net-driver-and-dvs/
dsq_thread_id:
  - 1405550190
categories:
  - Networking
  - VMware
tags:
  - be2net
  - dvs
  - ibm
  - portgroups
  - vfa
  - vlan
  - vmnic
---
I came across a really strange issue today with one of my customers. A VM would lose network connectivity every time more than 3 VLANs were trunked in a DVUplink portgroup on the VMware Distributed Virtual Switch. He was running an IBM Bladecenter blade server with the <a href="http://www.amazon.com/Emulex-Virtual-Fabric-Adapter-System/dp/B003E7MNWE" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.amazon.com/Emulex-Virtual-Fabric-Adapter-System/dp/B003E7MNWE']);" rel="nofollow">Emulex 10GB Virtual Fabric Adapter (VFA)</a>.

# Configuration

## Physical Switchport

[shell]  
switchport mode trunk  
[/shell]

## DVS Configuration

<div id="attachment_500" style="width: 233px" class="wp-caption alignnone">
  <a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_55-PM.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_55-PM.png']);"><img class="size-full wp-image-500" title="DVS Configuration" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_55-PM.png" alt="Screenshot 3 26 2012 8 06 55 PM VLAN issue with IBM VFA, be2net driver, and DVS" width="223" height="47" /></a><p class="wp-caption-text">
    DVS Configuration
  </p>
</div>

## dvPortgroup Configuration

<div id="attachment_499" style="width: 310px" class="wp-caption alignnone">
  <a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_28-PM.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_28-PM.png']);"><img class="size-medium wp-image-499" title="dvPortgroup Configuration" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_06_28-PM-300x227.png" alt="Screenshot 3 26 2012 8 06 28 PM 300x227 VLAN issue with IBM VFA, be2net driver, and DVS" width="300" height="227" /></a><p class="wp-caption-text">
    dvPortgroup Configuration
  </p>
</div>

## dvUplink Portgroup Configuration

<div id="attachment_501" style="width: 310px" class="wp-caption alignnone">
  <a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_07_53-PM.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_07_53-PM.png']);"><img class="size-medium wp-image-501" title="DVUplink Portgroup Configuration" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/Screenshot-3_26_2012-8_07_53-PM-300x227.png" alt="Screenshot 3 26 2012 8 07 53 PM 300x227 VLAN issue with IBM VFA, be2net driver, and DVS" width="300" height="227" /></a><p class="wp-caption-text">
    DVUplink Portgroup Configuration
  </p>
</div>

If we configured the dvUplink portgroup configuration to trunk 4 or more VLANs, the VMs using the VLAN-22 portgroup would lose network connectivity. Here are examples that would cause this issue:

*   0-4094 (default)
*   22,23,24,25
*   20-24

Here are examples that would allow communication:

*   <span style="line-height: 22px;">22</span>
*   <span style="line-height: 22px;">22,23,24</span>
*   <span style="line-height: 22px;">21-23</span>

# <span style="line-height: 22px;">Diagnostics</span>

Per the &#8220;Known Networking Issues&#8221; found in the <a title="VMware vSphere® 5.0 Release Notes" href="https://www.vmware.com/support/vsphere5/doc/vsphere-esx-vcenter-server-50-release-notes.html#networkingissues" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/vsphere5/doc/vsphere-esx-vcenter-server-50-release-notes.html#networkingissues']);" target="_blank">VMware vSphere® 5.0 Release Notes</a>:

> Using the bundled Emulex BE2/BE2 NICs (be2net driver)  
> When using vSphere 5.0 with Emulex BE2/BE3 NICs (be2net driver) in a HP FlexFabric/Flex-10 or IBM Virtual Fabric Adapter (VFA) environment, connectivity may not work properly on Windows VMs or the server when VLANs are configured.
> 
> Workaround: Do not use the driver bundled with vSphere 5.0. Before upgrading to vSphere 5.0, please obtain an updated driver from Emulex, HP, or IBM that should be used on HP FlexFabric/Flex-10 or IBM VFA systems.

I checked his driver version:

[shell]  
~ # ethtool -i vmnic2  
driver: be2net  
version: 4.0.355.1  
firmware-version: 4.0.1062.0  
bus-info: 0000:08:00.1  
[/shell]

and per the <a title="VMware hardware compatibility list" href="http://www.vmware.com/resources/compatibility/search.php" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/search.php']);" target="_blank">VMware hardware compatibility list</a>, he was running the Inbox driver that came bundled with ESXi 5.

The latest version appears to be be2net version 4.1.334.0, but the download is nowhere to be found. We will be working with the hardware vendor to locate the latest driver version.

In parallel, to confirm that it is a problem with the be2net driver and/or the Virtual Fabric Adapter, we will also try to see if we can replicate the issue with his Broadcom adapters running the bnx2 driver.

UPDATE: The be2net driver version 4.1.334.0 (we found the link <a href="http://downloads.vmware.com/d/details/dt_esxi50_emulex_be2net_413340/dHRAYndld3diZHAlZA " onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://downloads.vmware.com/d/details/dt_esxi50_emulex_be2net_413340/dHRAYndld3diZHAlZA']);" target="_blank">here</a>) did not resolve the issue, but a newer driver update from IBM fixed the issue.

It appears that this is an IBM known issue: <a title="Traffic does not passing with Distributed Virtual Switch and Emulex VFA II when vNICs enabled on VFA II - Emulex 10 Gigabit Ethernet Virtual Fabric Adapter Advanced II for IBM BladeCenter" href="https://www-947.ibm.com/support/entry/portal/docdisplay?lndocid=migr-5089840" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www-947.ibm.com/support/entry/portal/docdisplay?lndocid=migr-5089840']);" target="_blank">Traffic does not passing with Distributed Virtual Switch and Emulex VFA II when vNICs enabled on VFA II &#8211; Emulex 10 Gigabit Ethernet Virtual Fabric Adapter Advanced II for IBM BladeCenter</a>.

> This behavior will be corrected in a future release of the Emulex VFA II driver, using one of the following versions or higher:
> 
> *   ESX 4.x &#8211; 4.0.306.2
> *   ESX 5.0 &#8211; 4.0.355.2

It looks like the issue is resolved in a future release of the driver.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Receiving &#8221; Failed write command to write-quiesced partition&#8221; Messages When Utilizing Qlogic QMI8142 CNA" href="http://virtuallyhyper.com/2012/11/receiving-failed-write-command-to-write-quiesced-partition-messages-when-utilizing-qlogic-qmi8142-cna/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/receiving-failed-write-command-to-write-quiesced-partition-messages-when-utilizing-qlogic-qmi8142-cna/']);" rel="bookmark">Receiving &#8221; Failed write command to write-quiesced partition&#8221; Messages When Utilizing Qlogic QMI8142 CNA</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing be2iscsi Driver Version 4.1.334.3 on HP BL495c G6 with NC553m CNAs Causes ESXi Host to PSOD" href="http://virtuallyhyper.com/2012/11/installing-be2iscsi-version-4-1-334-3-on-bl495c-g6-for-nc553m-cnas-causes-esxi-host-to-psod/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/installing-be2iscsi-version-4-1-334-3-on-bl495c-g6-for-nc553m-cnas-causes-esxi-host-to-psod/']);" rel="bookmark">Installing be2iscsi Driver Version 4.1.334.3 on HP BL495c G6 with NC553m CNAs Causes ESXi Host to PSOD</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Experiencing PSODs on HP 465C G7 Blades with NC551i NICs" href="http://virtuallyhyper.com/2012/11/experiencing-psods-on-hp-465c-g7-blades-with-nc551i-nics/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/experiencing-psods-on-hp-465c-g7-blades-with-nc551i-nics/']);" rel="bookmark">Experiencing PSODs on HP 465C G7 Blades with NC551i NICs</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/vlan-issue-with-ibm-vfa-be2net-driver-and-dvs/" title=" VLAN issue with IBM VFA, be2net driver, and DVS" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:be2net,dvs,ibm,portgroups,vfa,vlan,vmnic,blog;button:compact;">After updating our HP Virtual Connect firmware to version 3.60, our ESXi host we would see the following PSOD after a certain amount of time: Here is the actual backtrace:...</a>
</p>