---
title: Beacon Probes with Port-Channel Causing Mac-Flapping
author: Karim Elatov
layout: post
permalink: /2012/03/beacon-probes-with-port-channel-causing-mac-flapping/
dsq_thread_id:
  - 1407810572
categories:
  - Networking
  - VMware
tags:
  - beacon probes
  - beacon probing
  - beacons
  - flapping
  - port channels
---
Recently, someone asked me why when using VMware ESX with port-channel and beacon probes causes mac-flapping. This is actually a known cause and effect and I would even say that is the expected behavior. You can read more about it at VMware KB article <a href="http://kb.vmware.com/kb/1012819" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1012819']);">1012819</a>. Granted the description of the root cause is not too in-depth, I decided to talk about it. If you want to know more about beacon probes I suggest reading VMware KB article <a href="http://kb.vmware.com/kb/1005577" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005577']);">1005577</a> and the following VMware blog: <a href="http://blogs.vmware.com/networking/2008/12/using-beaconing-to-detect-link-failures-or-beaconing-demystified.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/networking/2008/12/using-beaconing-to-detect-link-failures-or-beaconing-demystified.html']);">Beaconing Demystified: Using Beaconing to Detect Link Failures</a>.  If we don&#8217;t have any port-channel (port aggregation) setup on the upstream switch then we just send a beacon out of each physical NIC that is part of the port-group which has beacon probing enabled (each beacon has its own MAC address). The beacon is reached across the broadcast domain (so if it hits a router, it would stop there). It would kind of look like this with two uplinks (three uplinks are necessary for beacon to work properly, but this image is just for an example):

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_No_Port_Channel.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_No_Port_Channel.jpg']);"><img class="alignnone size-full wp-image-67" title="BP_No_Port_Channel" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_No_Port_Channel.jpg" alt="BP No Port Channel Beacon Probes with Port Channel Causing Mac Flapping" width="514" height="215" /></a>

So Beacon 1 (Blue) is sent out of one of the NICs and the other NIC receive it (in actuality the whole broadcast domain receives it, so any other host on that physical switch would also receive that beacon). Same thing for Beacon 2 (Red). Now if we throw a port-channel in there, it would look something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_With_Port_Channel.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_With_Port_Channel.jpg']);"><img class="alignnone size-full wp-image-69" title="BP_With_Port_Channel" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/BP_With_Port_Channel.jpg" alt="BP With Port Channel Beacon Probes with Port Channel Causing Mac Flapping" width="658" height="215" /></a>

So now each beacon can and will be seen across both of the ports on the switch (for now, VMware&#8217;s standard and distributed switches only support IP/hash for its ether-channel algorithm). Since each beacon has its own MAC address and the hashing algorithm is IP-based, the MAC address of the probes (not having any IP) will be seen across both ports of the switch. Some good work-arounds for this issue include Link-State Tracking (a person from above blog has a good example of this) here a link to his blog: <a href="http://www.bctechnet.com/vmware-link-state-tracking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.bctechnet.com/vmware-link-state-tracking/']);">VMware and Link State Tracking</a>. If you are using blade enclosures, HP&#8217;s provide SmartLink Functionality, and this page describes it in a very succinct way: <a href="http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?objectID=c01780345&lang=en&cc=us&taskId=&prodSeriesId=3794423&prodTypeId=3709945" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?objectID=c01780345&lang=en&cc=us&taskId=&prodSeriesId=3794423&prodTypeId=3709945']);">HP Virtual Connect Flex-10 Ethernet Module &#8211; SmartLink Feature Not Supported on Individual FlexNICs</a>. Don&#8217;t let the name scare you :). As long as you know what SmartLInk is after visiting that page, I will be more than happy :). If that one doesn&#8217;t help out, check this one out: <a href="http://blog.michaelfmcnamara.com/2009/08/hp-virtual-connect-smart-link/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.michaelfmcnamara.com/2009/08/hp-virtual-connect-smart-link/']);">HP Virtual Connect SmartLink</a>.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Possible reasons for RARP storms from an ESX host" href="http://virtuallyhyper.com/2012/03/possible-reasons-for-rarp-storms-from-an-esx-host/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/possible-reasons-for-rarp-storms-from-an-esx-host/']);" rel="bookmark">Possible reasons for RARP storms from an ESX host</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/03/beacon-probes-with-port-channel-causing-mac-flapping/" title=" Beacon Probes with Port-Channel Causing Mac-Flapping" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:beacon probes,beacon probing,beacons,flapping,port channels,blog;button:compact;">I see a lot of different reasons for a RARP storms from an ESX host. The biggest one that I ran into is a PXE boot environment (ie: Citrix Provisioning...</a>
</p>
