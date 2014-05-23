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
Recently, someone asked me why when using VMware ESX with port-channel and beacon probes causes mac-flapping. This is actually a known cause and effect and I would even say that is the expected behavior. You can read more about it at VMware KB article [Beaconing Demystified: Using Beaconing to Detect Link Failures](http://kb.vmware.com/kb/1012819).  If we don't have any port-channel (port aggregation) setup on the upstream switch then we just send a beacon out of each physical NIC that is part of the port-group which has beacon probing enabled (each beacon has its own MAC address). The beacon is reached across the broadcast domain (so if it hits a router, it would stop there). It would kind of look like this with two uplinks (three uplinks are necessary for beacon to work properly, but this image is just for an example):

![BP_No_Port_Channel](https://github.com/elatov/uploads/raw/master/2012/03/BP_No_Port_Channel.jpg)

So Beacon 1 (Blue) is sent out of one of the NICs and the other NIC receive it (in actuality the whole broadcast domain receives it, so any other host on that physical switch would also receive that beacon). Same thing for Beacon 2 (Red). Now if we throw a port-channel in there, it would look something like this:

![BP_With_Port_Channel](https://github.com/elatov/uploads/raw/master/2012/03/BP_With_Port_Channel.jpg)

So now each beacon can and will be seen across both of the ports on the switch (for now, VMware's standard and distributed switches only support IP/hash for its ether-channel algorithm). Since each beacon has its own MAC address and the hashing algorithm is IP-based, the MAC address of the probes (not having any IP) will be seen across both ports of the switch. Some good work-arounds for this issue include Link-State Tracking (a person from above blog has a good example of this) here a link to his blog: [HP Virtual Connect SmartLink](http://www.bctechnet.com/vmware-link-state-tracking/).

### Related Posts

- [Possible reasons for RARP storms from an ESX host](http://virtuallyhyper.com/2012/03/possible-reasons-for-rarp-storms-from-an-esx-host/)

