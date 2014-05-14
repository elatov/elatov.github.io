---
title: Mini ESXi Lab Hosts
author: Jarret Lavallee
layout: post
permalink: /2013/04/mini-esxi-lab-hosts/
dsq_thread_id:
  - 1404673475
categories:
  - Home Lab
  - VMware
tags:
  - Mini ESXi Hosts
  - VMware Hardware
  - Whitebox
---
**Update 04/2013:** I wrote this post back in August 2012, but never actually published it. I purchased the mini hosts and have been running them for 8 months with great success. I would still recommend these hosts, but with 2 considerations.

1.  The i7 processors were over kill. You can get by fine with a quad core i5 and save ~$100 on each build
2.  The one NIC is very limiting. They still run fine, but it would be much better with a motherboard with dual onboard NICs. Like <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16813121622" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16813121622']);">this motherboard</a> (just be careful with the <a href="http://virtual-drive.in/2012/11/16/enabling-intel-nic-82579lm-on-intel-s1200bt-under-esxi-5-1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtual-drive.in/2012/11/16/enabling-intel-nic-82579lm-on-intel-s1200bt-under-esxi-5-1/']);">82579LM NIC</a>)

Over the last few years, I&#8217;ve had a fun time buying and building out my lab. I have gone through numerous iterations and now it&#8217;s time for a new one. I recently moved to a tiny New York apartment so my requirements are changing, and new design is necessary.

## Choosing a hardware platform

First, I have my requirements for the new lab.

*   It should be scalable
*   It should be able to accommodate virtual Labs
*   It should be quiet
*   It should be energy efficient
*   It should be small enough to fit into a small apartment
*   It needs to be able to run ESXi5 with VT-d

The small and quiet requirements are really the driving factors here. I decided to go with less resourceful hosts and more of them ( this is referred to as scaling out ). I like the idea of scaling out rather than scaling up, because I can add in a new node to grow rather than adding more resources to the boxes. This way I can conform to my space and noise constraints.

In my current lab I have a 4GB of RAM to a single core ratio. I run a lot of virtual ESX hosts which require 2+ vCPUs which causes CPU contention. My *%READY* times are substantial when running multiple virtual labs. For this build I am moving away from AMD processors to the Intel i7 series and keeping the 4GB/core ratio. With the i7 processors I can use hyper-threading to help with the scheduling. I know there is a lot of debate on hyper-threading, but in this case it&#8217;s scheduling contention and not as much computing contention. More information about ESX and hyper-threading can be <a href="http://sudrsn.wordpress.com/2010/07/21/hyper-threading-on-vmware-vsphere/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sudrsn.wordpress.com/2010/07/21/hyper-threading-on-vmware-vsphere/']);">found here</a>.

After a good amount of research I came to find 3 different choices.

### Mac Mini

There are <a href="http://paraguin.com/2012/01/10/the-mac-mini-vmware-esxi-5-server-part-1-research/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://paraguin.com/2012/01/10/the-mac-mini-vmware-esxi-5-server-part-1-research/']);">many people</a> running ESXi5 labs with the Mac Mini. They are small, quiet, and sleek. Along with their small size they have some power packed in. The <a href="http://store.apple.com/us/browse/home/specialdeals/mac/mac_mini" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://store.apple.com/us/browse/home/specialdeals/mac/mac_mini']);">Refurbished Mac Mini</a> is currently running for $850. It comes with dual 500Gb hard drives, 4GB of Memory, and an i7.

![apple mac mini 23ghz core i5 mid 2011 1109373 g1 Mini ESXi Lab Hosts][1]

Here are the specifications for the 2011 i7 model.

![Refurbished Mac mini with Lion Server 2 specs Mini ESXi Lab Hosts][2]

4GB of memory will not cut it, but you can buy <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16820233251" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16820233251']);">16GB of memory</a> for the Mac Mini and have a nice ESXi Host. It would also be nice to add in the <a href="http://www.virtuallyghetto.com/2012/06/thunderbolt-ethernet-adapter-in-apple.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virtuallyghetto.com/2012/06/thunderbolt-ethernet-adapter-in-apple.html']);">Thunderbolt NIC</a> for the Mini to have 2 NICs.

The only problem I find with this solution is that it is just too expensive. There are many features built into the device that I will not use.

*   **Dimensions:** 1.4″ x 7.7″ x 7.7″ ( 1 Mac Mini )
*   **Total price:** $943 (with hard drives)

### Shuttle

The <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16856101117" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16856101117']);">Shuttle SH67H3</a> is a great idea. It is small, powerful, and comes with a 300W power supply. The greatest feature is that the motherboard can support 32Gb of memory with an LGA 1155 socket.

![SH67H3 Mini ESXi Lab Hosts][3]

For the build, I decided on the following components.

*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16856101117" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16856101117']);">Shuttle SH67H3</a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16819115228" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16819115228']);">Intel i7-2600S Sandy Bridge 2.8GHz</a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16820231608" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16820231608']);">G.SKILL Value Series 16GB (2 x 8GB) 240-Pin DDR3</a>

I selected the i7-2600S because it is a 65Watt TDP sandy-bridge processor that supports VT-D. Ivy-bridge is a great idea, but I do not need most of the features on it yet. I have also heard that <a href="http://techreport.com/discussions.x/22859" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://techreport.com/discussions.x/22859']);">Ivy-bridge runs hotter than sandy-bridge</a>. The i7 is a bit over-kill as a i5 would work just fine, but I would rather spend the extra $100 up front for future expansion if necessary.

The thing that I do not like is the built-in power supply. In my experience they are normally pretty loud and not easily replaceable with quieter ones. I end up taking them apart and replacing the fans. It is also significantly larger than the other solutions on here, but it is the only one that has the ability to add expansion cards and can handle up to 32GB of memory.

*   **Dimensions:** 12.72″ x 8.19″ x 7.72″ ( ~9 Mac Minis )
*   **Total price:** $614.97

### Custom mini-ITX build

The nice thing about a custom mini-ITX build is that it is custom. I love researching all of the parts and building it all from scratch. It just feels good to find a <a href="http://siphon9.net/loune/2011/01/list-of-sandy-bridge-lga1155-h67p67-motherboards-that-support-vt-d/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://siphon9.net/loune/2011/01/list-of-sandy-bridge-lga1155-h67p67-motherboards-that-support-vt-d/']);">random post on a blog</a> mentioning that they have successfully enabled VT-D on a motherboard. The risks are apparent; there are no guarantees that the equipment will work with ESXi 5.x. Personally I generally lean towards this option, but end up going over budget.

Mini-ITX is a small platform that can be quite powerful. The mini-ITX boards range from embedded processors to the LGA 1155 socket. In this case I decided to go with the same chipset as the Shuttle above and find a motherboard that runs the H67 chipset.

*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16819115228" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16819115228']);">Intel i7-2600S Sandy Bridge 2.8GHz</a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16820231608" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16820231608']);">G.SKILL Value Series 16GB (2 x 8GB) 240-Pin DDR3 </a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16813186211" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16813186211']);">Foxconn H67S LGA 1155</a>
*   <a href="http://www.newegg.com/Product/Product.aspx?Item=N82E16811129185" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.newegg.com/Product/Product.aspx?Item=N82E16811129185']);">Antec ISK 110</a>

The foxconn H67S met the requirements and was only $64.99. After a little research it seems that the motherboard <a href="http://siphon9.net/loune/2011/01/list-of-sandy-bridge-lga1155-h67p67-motherboards-that-support-vt-d/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://siphon9.net/loune/2011/01/list-of-sandy-bridge-lga1155-h67p67-motherboards-that-support-vt-d/']);">will do VT-d</a>. As with the Shuttle, I decided on the i7-2600S processor as <a href="http://www.cpu-world.com/Compare/302/Intel_Core_i7_Mobile_i7-2635QM_vs_Intel_Core_i7_i7-2600S.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cpu-world.com/Compare/302/Intel_Core_i7_Mobile_i7-2635QM_vs_Intel_Core_i7_i7-2600S.html']);">compared to the Mac Mini i7</a>.

![Antec ISK 110 VESA Front View Mini ESXi Lab Hosts][4]

The downside of this build is that there is no room for expansion cards in the case, so we are stuck with the onboard Realtek 8168G NIC. This NIC has a driver built into ESXi 5, but it is a Realtek and not an enterprise NIC. The other downside is that the power supply built into the case is 90 Watts with 92% efficiency, so effectively maxing out at ~82 Watts. With a 65Watt TDP processor and no onboard expansion, that leaves the motherboard 17 Watts when the processor is maxed out. It would be tight, but it should work.

*   **Dimensions:** 8.7″ x 3.1″ x 8.4″ ( ~2 Mac Minis)
*   **Total Price:** $524.96

## The Choice

For me it is always about having fun and saving money for these builds. I would be able to afford more resources if I used the Shuttle or the Mini-ITX build. The Shuttle would have provided double the memory for each host, but was about 4.5 times larger than the Mini-ITX build. I decided to go for the Mini-ITX build for the money, space, and noise savings as compared to the other options.

#### Compatibility

After my research I found that this solution is compatible with ESXi 5.0 and ESXi 5.1. It has Intel VT-D capabilities and can run nested ESXi hosts.

#### Power Consumption

One of my big concerns with this build is the power consumption. My previous hosts idled at 50 Watts. I wanted these to be much less than that, as most of the time they will be idle. The other concern was that I would be limited by the 90 Watt power supply. My fears turned out to be unjustified. After the assembly I hooked up one of the boxes to a Kill-A-Watt to get a baseline while it&#8217;s idle. I put a single SRM lab on the host and ran it over night. The host ended up using .23 KW over 9 hours.

    .23KW/9 hours = .025 KWph. 
    

So we can use this as a baseline for the minimum cost for a month.

    .025 Kilowatts per hour * 24 hours per day * 30 Days per month = 18 Kilowatts per month. 
    

At an average of $0.20 per Kilowatt in New York, it would cost $3.6 a month to run the host mostly idle.

With two hosts running idle for the majority of the time I would be looking at around $8 a month. With VMware Distributed Power Management, I will be able to cut this figure down even further. I set up the BIOS of the boards to wake on LAN, and tested out the standby feature in ESXi 5. I was able to successfully bring a host out of standby mode. Using DPM, I should be able to save even more energy consumption based on my host utilization.

Over all I am happy these Mini hosts. They were cost effective and very quiet hosts. They are in my living room and you would never know that they were on and running. I would not use these hosts to run a full environment because of the lack of dual NICs, but they run great for additional resources.


 [1]: http://virtuallyhyper.com/wp-content/uploads/2012/08/apple_mac_mini_23ghz_core_i5_mid_2011_1109373_g1.jpg "Mini ESXi Lab Hosts"
 [2]: http://virtuallyhyper.com/wp-content/uploads/2012/08/Refurbished-Mac-mini-with-Lion-Server-2-specs.png "Mini ESXi Lab Hosts"
 [3]: http://virtuallyhyper.com/wp-content/uploads/2012/08/SH67H3.jpg "Mini ESXi Lab Hosts"
 [4]: http://virtuallyhyper.com/wp-content/uploads/2012/08/Antec-ISK-110-VESA-Front-View.png "Mini ESXi Lab Hosts"