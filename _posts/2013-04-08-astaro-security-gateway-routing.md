---
title: Astaro Security Gateway Routing
author: Joe Chan
layout: post
permalink: /2013/04/astaro-security-gateway-routing/
dsq_thread_id:
  - 1409933412
categories:
  - AWS
  - Networking
  - OS
tags:
  - ASG
  - aws
  - BGP
---
I had an issue where bringing up an <a href="http://aws.amazon.com/articles/1909971399457482" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://aws.amazon.com/articles/1909971399457482']);">Sophos Astaro Security Gateway (ASG)</a> site-to-site VPN connection between VPC&#8217;s caused another connectivity across another VPN connection to fail. Looking into the Astaro Security Gateway routing, we were able to determine that a default BGP route was getting advertised to the common VGW and likely causing issues.

This diagram might help explain better: ![astaro network diagram Astaro Security Gateway Routing][1]

In the end, we were unable to make settings stick on the Astaro instance across stop/start, but we were at least able to figure out how to log into the Astaro instance and view and (temporarily) modify the BGP advertised routes to confirm if that was the issue or not.

The ASG appears to be an Sophos-customized Linux server running the <a href="http://www.nongnu.org/quagga/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nongnu.org/quagga/']);">Quagga Routing Suite</a> so some of the <a href="http://www.nongnu.org/quagga/docs/docs-info.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nongnu.org/quagga/docs/docs-info.html']);">official Quagga documentation</a> might help as well. Anyway, here are the steps I took&#8230;

*Note: The procedure outlined below may be unsupported by Astaro.*

# Logging in

First, we needed to figure out how to log into the Astaro instance. <a href="http://www.sophos.com/en-us/support/knowledgebase/115030.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.sophos.com/en-us/support/knowledgebase/115030.aspx']);">This Astaro KB</a> helped.

So here we go:

    ssh astaro8.domain -l loginuser
    su - root
    

# Viewing current **bgpd** configuration

We determined that the BGP configuration is stored at **/var/chroot-quagga/etc/quagga/bgpd.conf**. From that file, we can figure out the **bgpd** credentials so we can connect to the **bgpd** VTY:

    loginuser@astaro8:/home/login > head /var/chroot-quagga/etc/quagga/bgpd.conf
    hostname astaro8
    password GENIsjjv
    enable password uouCvkmR
    ...
    

From <a href="http://www.nongnu.org/quagga/docs/docs-info.html#Install-the-Software" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nongnu.org/quagga/docs/docs-info.html#Install-the-Software']);">the Quagga documentation</a>, you connect to **bgpd** terminal interface or VTY via port **2605**:

>     bgpd          2605/tcp                # BGPd vty
>     

So we can telnet to the port 2605 to configure **bgpd**:

    loginuser@astaro8:/home/login > telnet 0 2605
    Trying 0.0.0.0...
    Connected to 0.
    Escape character is '^]'.
    Hello, this is Quagga (version 0.99.20).
    Copyright 1996-2005 Kunihiro Ishiguro, et al.
    User Access Verification
    Password: GENIsjjv
    astaro8> en
    Password: uouCvkmR
    astaro8#
    

Then, we can list the BGP neighbors (vgw-45c5243c in the <a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/astaro-network-diagram.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/astaro-network-diagram.jpg']);">image</a> above):

    astaro8# show ip bgp sum
    BGP router identifier 169.254.249.26, local AS number 65000
    RIB entries 2, using 128 bytes of memory
    Peers 2, using 5048 bytes of memory
    
    Neighbor V AS MsgRcvd MsgSent TblVer InQ OutQ Up/Down State/PfxRcd
    169.254.249.25 4 7224 64 66 0 0 0 00:10:01 1
    169.254.249.29 4 7224 64 65 0 0 0 00:10:01 1
    
    Total number of neighbors 2
    

*Note: For the below commands, replace all my example BGP neighbor IP addresses below with neighbors you see in your own **sh ip bgp sum**.*

Show advertised routes and verify that we see the default route being advertised to both neighbors:

    astaro8# show ip bgp nei 169.254.249.29 adv
    BGP table version is 0, local router ID is 169.254.249.26
    Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
    r RIB-failure, S Stale, R Removed
    Origin codes: i - IGP, e - EGP, ? - incomplete
    
    Network Next Hop Metric LocPrf Weight Path
    *> 0.0.0.0 169.254.249.30 0 100 32768 i # Here is the default route being advertised to peer 169.254.249.29
    
    Total number of prefixes 1
    
    astaro8# show ip bgp nei 169.254.249.25 adv
    BGP table version is 0, local router ID is 169.254.249.26
    Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
    r RIB-failure, S Stale, R Removed
    Origin codes: i - IGP, e - EGP, ? - incomplete
    
    Network Next Hop Metric LocPrf Weight Path
    *> 0.0.0.0 169.254.249.26 0 100 32768 i # Here is the default route being advertised to peer 169.254.249.25
    *> 10.0.0.0/16 169.254.249.26 100 0 7224 i
    
    Total number of prefixes 2
    

# Modifying default route propagation

To temporarily disable the default route from being advertised there were 2 options:

1.  Modify **/var/chroot-quagga/etc/quagga/bgpd.conf** and restart **bgpd**
2.  Connect to **bgpd** and modify live config

I&#8217;ll show both below:

## 1. Modify **/var/chroot-quagga/etc/quagga/bgpd.conf**

Change:

    access-list term permit 127.0.0.1/32
    access-list term deny any
    

to read:

    access-list term permit 127.0.0.1/32
    access-list term deny any
    ip prefix-list FILTER-DEFAULT-OUT seq 5 deny 0.0.0.0/0
    ip prefix-list FILTER-DEFAULT-OUT seq 10 permit 0.0.0.0/0 le 32
    

Restart **bgpd**:

    astaro8:/root # ps -ef |grep bgpd
    chroot 4381 1 0 19:28 ? 00:00:00 /usr/sbin/bgpd -u chroot -g chroot -d
    root 6747 6736 0 19:55 pts/1 00:00:00 grep bgpd
    astaro8:/root # kill -HUP 4381
    

## 2. Connect to **bgpd** and modify live config:

Block the default route from being advertised:

    astaro8# conf t
    astaro8(config)# ip prefix-list FILTER-DEFAULT-OUT seq 5 deny 0.0.0.0/0
    astaro8(config)# ip prefix-list FILTER-DEFAULT-OUT seq 10 permit 0.0.0.0/0 le 32
    astaro8(config)# end
    

Verify that the **prefix list** has been added:

    astaro8# sh ip prefix-list
    BGP: ip prefix-list FILTER-DEFAULT-OUT: 2 entries
    seq 5 deny 0.0.0.0/0
    seq 10 permit 0.0.0.0/0 le 32
    

Apply the **prefix list** to both neighbors:

    astaro8# conf t
    astaro8(config)# router bgp 65000
    astaro8(config-router)# neighbor 169.254.249.25 prefix-list FILTER-DEFAULT-OUT out
    astaro8(config-router)# end
    astaro8# clear ip bgp 169.254.249.25 soft out
    
    astaro8# conf t
    astaro8(config)# router bgp 65000
    astaro8(config-router)# neighbor 169.254.249.29 prefix-list FILTER-DEFAULT-OUT out
    astaro8(config-router)# end
    astaro8# clear ip bgp 169.254.249.29 soft out
    

Check both neighbors and ensure that **0.0.0.0/0** default route is no longer showing up on either of them:

    astaro8# sh ip bgp nei 169.254.249.25 adv
    astaro8# sh ip bgp nei 169.254.249.29 adv
    BGP table version is 0, local router ID is 169.254.249.26
    Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
    r RIB-failure, S Stale, R Removed
    Origin codes: i - IGP, e - EGP, ? - incomplete
    
    Network Next Hop Metric LocPrf Weight Path
    *> 10.0.0.0/16 169.254.249.30 100 0 7224 i
    
    Total number of prefixes 1
    

We have confirmed the default routes are no longer being advertised.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/04/astaro-security-gateway-routing/" title=" Astaro Security Gateway Routing" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:ASG,aws,BGP,blog;button:compact;">I had an issue where bringing up an Sophos Astaro Security Gateway (ASG) site-to-site VPN connection between VPC&#8217;s caused another connectivity across another VPN connection to fail. Looking into the...</a>
</p>

 [1]: http://virtuallyhyper.com/wp-content/uploads/2013/03/astaro-network-diagram.jpg "Astaro AWS VPN Network Diagram"