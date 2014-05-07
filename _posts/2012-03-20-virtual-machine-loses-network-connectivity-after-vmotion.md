---
title: Virtual Machine Gets Disconnected After vMotion
author: Joe Chan
layout: post
permalink: /2012/03/virtual-machine-loses-network-connectivity-after-vmotion/
dsq_thread_id:
  - 1407607261
categories:
  - Networking
  - VMware
tags:
  - network
  - troubleshooting
  - vmnic
  - vmotion
---
This appears to be a very common issue. The actual root causes vary, but hopefully this can help you isolate the issue.

A virtual machine typically loses network connectivity because it gets bound to a vmnic that does not have access to the network resources the VM requires.

If you are using &#8220;Route based on originating virtual port ID&#8221; or &#8220;Route based on source MAC hash&#8221;, the VM can be bound to any one of the NICs in that team. If you are using &#8220;Route based on IP hash&#8221;, the VM will send traffic out any of the vmnics depending on the source and destination IP addresses (details about that specific process can be found in VMware KB article <a title="Troubleshooting IP-Hash outbound NIC selection" href="http://kb.vmware.com/kb/1007371" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1007371']);" target="_blank">1007371</a>).

Any operation that brings the VM&#8217;s virtual network adapter online can cause that virtual network adapter (vNIC) to bind to a new physical adapter (vmnic) on the vSwitch. Here are a few examples of actions that can cause this to occur:

*   VM powering on
*   connecting the virtual machine&#8217;s network adapter (vNIC)
*   vMotion
*   Changing a vNIC&#8217;s assigned portgroup

# <span style="line-height: 18px;">Example</span>

For my example, let&#8217;s say you vMotioned a virtual machine, &#8220;Test&#8221;, from ESX-A to ESX-B and the VM lost network connectivity.

If the issue is still present, you can SSH into ESX-B and run the following to determine which vmnic the &#8220;Test&#8221; virtual machine is currently being bound to:

- run the following command

[shell]esxtop[/shell]

- type &#8216;n&#8217; (for Networking)

You will be presented with a screen like this:

[shell highlight="10"] 1:07:14am up 2:33, 163 worlds; CPU load average: 0.01, 0.05, 0.02

PORT-ID USED-BY TEAM-PNIC DNAME PKTTX/s MbTX/s PKTRX/s MbRX/s %DRPTX %DRPRX  
16777217 Management n/a vSwitch0 0.00 0.00 0.00 0.00 0.00 0.00  
16777218 vmnic0 &#8211; vSwitch0 27.13 0.07 0.00 0.00 0.00 0.00  
16777219 vmk0 vmnic0 vSwitch0 27.13 0.07 0.00 0.00 0.00 0.00  
33554433 Management n/a vSwitch1 0.00 0.00 0.00 0.00 0.00 0.00  
33554434 vmnic2 &#8211; vSwitch1 0.00 0.00 27.13 0.07 0.00 0.00  
33554435 vmnic3 &#8211; vSwitch1 0.00 0.00 0.00 0.00 0.00 0.00  
33554436 21153:Test vmnic3 vSwitch1 0.00 0.00 0.00 0.00 0.00 0.00[/shell]

Under the USED-BY column, look for the name of your virtual machine. The TEAM-PNIC column will indicate the vmnic it is currently bound to (this does not work if you are using IP hash with port-channels).

In our case, our VM (Test), is bound to vmnic3.

Now, we should test connectivity with the other vmnic in the team. To explicitly bind the VM to another vmnic, you can specify explicit failover in the current portgroup or create a new portgroup for testing purposes and place the VM within it.

In the portgroup settings, you can set vmnic3 to unused and vmnic2 to active to force any VMs within the VM Network portgroup to bind to vmnic2. Here is an example:

<div id="attachment_341" style="width: 528px" class="wp-caption alignnone">
  <a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/ScreenClip.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/ScreenClip.png']);"><img class="size-full wp-image-341" title="Portgroup Properties" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/ScreenClip.png" alt="ScreenClip Virtual Machine Gets Disconnected After vMotion" width="518" height="648" /></a><p class="wp-caption-text">
    Portgroup Properties
  </p>
</div>

If you regain connectivity, then chances are there is a problem communicating over vmnic2 and you should check your configuration and hardware for vmnic2.

These steps can be repeated for however many vmnics you have attached to the portgroup to isolate which adapters are having issues.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="SRM 5.0 Times out on a test failover when using Mirrorview SRA 5.0.1" href="http://virtuallyhyper.com/2012/08/srm-5-0-times-out-on-a-test-failover-when-using-mirrorview-sra-5-0-1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-5-0-times-out-on-a-test-failover-when-using-mirrorview-sra-5-0-1/']);" rel="bookmark">SRM 5.0 Times out on a test failover when using Mirrorview SRA 5.0.1</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Advanced Snapshot Troubleshooting: Invalid parentCID/CID chain" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-invalid-parentcidcid-chain/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-invalid-parentcidcid-chain/']);" rel="bookmark">Advanced Snapshot Troubleshooting: Invalid parentCID/CID chain</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Against Best Practices: vMotion and Management on the Same Network" href="http://virtuallyhyper.com/2012/04/against-best-practices-vmotion-and-management-on-the-same-network/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/against-best-practices-vmotion-and-management-on-the-same-network/']);" rel="bookmark">Against Best Practices: vMotion and Management on the Same Network</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VLAN issue with IBM VFA, be2net driver, and DVS" href="http://virtuallyhyper.com/2012/04/vlan-issue-with-ibm-vfa-be2net-driver-and-dvs/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vlan-issue-with-ibm-vfa-be2net-driver-and-dvs/']);" rel="bookmark">VLAN issue with IBM VFA, be2net driver, and DVS</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Advanced Snapshot Troubleshooting: Non-Linear VMware Snapshot Chain" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/']);" rel="bookmark">Advanced Snapshot Troubleshooting: Non-Linear VMware Snapshot Chain</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/virtual-machine-loses-network-connectivity-after-vmotion/" title=" Virtual Machine Gets Disconnected After vMotion" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:network,troubleshooting,vmnic,vmotion,blog;button:compact;">Recently, I wrote up an article about VMware Snapshot Troubleshooting. In the article we discussed how to do some basic snapshot troubleshooting. Today, we will look a little deeper into...</a>
</p>