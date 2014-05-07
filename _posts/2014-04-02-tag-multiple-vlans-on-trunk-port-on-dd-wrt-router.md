---
title: Tag Multiple VLANs on Trunk Port on DD-WRT Router
author: Karim Elatov
layout: post
permalink: /2014/04/tag-multiple-vlans-on-trunk-port-on-dd-wrt-router/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2445708368
categories:
  - Home Lab
  - Networking
  - VMware
tags:
  - DD-WRT
  - Trunk Port
---
I was running an ESXi host in my home network and I wanted to dedicate on NIC of the ESXi for VM traffic. Since I was planning on having different networks, I decide to plug this NIC into a trunk port of the dd-wrt router. This way, I can just assign the VM to an appropriate virtual network and it will have access to it&#8217;s corresponding network.

### Add another VLAN to dd-wrt

So I decided to allow vlans 1 and 3 to go through port 4 of the dd-wrt router. First let&#8217;s add vlan 3 to the dd-wrt configuration and assign a 10.0.0.0/24 network range to this vlan. This is done in the management UI. Point your browser to the dd-wrt router, after you login you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-admin-ui.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-admin-ui.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-admin-ui.png" alt="dd wrt admin ui Tag Multiple VLANs on Trunk Port on DD WRT Router" width="628" height="441" class="alignnone size-full wp-image-10322" title="Tag Multiple VLANs on Trunk Port on DD WRT Router" /></a>

Now let&#8217;s add vlan3 to port 4:

1.  Go to **Setup** -> **VLANs**.
2.  Uncheck port 4. 
3.  Place port 4 into VLAN3.
4.  Click **Save**, then **Apply Settings**.

Next let&#8217;s configure vlan 3&#8242;s network:

1.  Go to **Setup** -> **Networking** -> **Port Setup**
2.  Set Vlan3 to **unbridged**
3.  Set the IP address to 10.0.0.1
4.  Set the Subnet Mask to 255.255.255.0
5.  **Save** the configuration

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-port-setup.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-port-setup.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-port-setup.png" alt="dd wrt port setup Tag Multiple VLANs on Trunk Port on DD WRT Router" width="458" height="372" class="alignnone size-full wp-image-10323" title="Tag Multiple VLANs on Trunk Port on DD WRT Router" /></a>

Let&#8217;s also enable DHCP for VLAN3:

1.  Go to **Setup** -> **Networking** -> **DHCPD**
2.  Set DHCP 0 to vlan3 with a Leasetime of 3600.
3.  Click Save and Apply Settings

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-dhcp.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-dhcp.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-dhcp.png" alt="dd wrt dhcp Tag Multiple VLANs on Trunk Port on DD WRT Router" width="592" height="143" class="alignnone size-full wp-image-10326" title="Tag Multiple VLANs on Trunk Port on DD WRT Router" /></a>

Now let&#8217;s bring up the vlan3 interface on boot. To do this:

1.  Go to **Administration** -> **Commands** 
2.  Enter the following in the **commands** text field
    
    <pre class="brush: /bin/ash; notranslate">PATH="/sbin:/usr/sbin:/bin:/usr/bin:${PATH}"
ifconfig vlan3 10.0.0.1 netmask 255.255.255.0
ifconfig vlan3 up
</pre>

3.  Click **Save Startup**

After it&#8217;s done you should see the following under the **Start up** section:

<a href="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-startup-commands.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-startup-commands.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/03/dd-wrt-startup-commands.png" alt="dd wrt startup commands Tag Multiple VLANs on Trunk Port on DD WRT Router" width="587" height="357" class="alignnone size-full wp-image-10327" title="Tag Multiple VLANs on Trunk Port on DD WRT Router" /></a>

If you have SSH enabled on the router you can run the following to assign vlan3 to port 4:

    nvram set vlan1ports="3 2 1 8*"
    nvram set vlan3ports="4 8"
    nvram set vlan3hwname="et0"
    

Since I was enabling DHCP and defining the network range, I just did that in the UI.

#### Enabling Trunk VLANs on port 4

These commands have to be run from the command line. To enable SSH on the dd-wrt, follow the instruction laid out <a href="http://virtuallyhyper.com/2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/']);">here</a>. Before making any changes, I checked out my vlan configuration and here is what I saw:

    root@DD-WRT:~# nvram show | grep "vlan.ports"
    vlan2ports=0 8
    vlan3ports=4 8
    vlan1ports=3 2 1 8*
    
    root@DD-WRT:~# nvram show | grep "port.vlans"
    port5vlans=1 2 3 16
    port3vlans=1 18 19
    port1vlans=1 18 19
    port4vlans=3 18 19
    port2vlans=1 18 19
    port0vlans=2 18 19
    

The ports are described <a href="http://www.dd-wrt.com/wiki/index.php/Switched_Ports" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.dd-wrt.com/wiki/index.php/Switched_Ports']);">here</a>. From that page:

> 0 = WAN  
> 1 = port 1  
> 2 = port 2  
> 3 = port 3  
> 4 = port 4
> 
> **Gigabit routers**
> 
> [0-4] = Can be forward or reverse like above  
> 8 = CPU internal  
> 8* = CPU internal default

Here are the other numbers mean:

> 16 = Tagged is checked  
> 17 = Auto-Negotiate is unchecked  
> 18 = 100 Mbit is unchecked or greyed because Auto-Negotiate is checked  
> 19 = Full-Duplex is unchecked or greyed because Auto-Negotiate is checked  
> 20 = Enabled is unchecked.

So from the above we can see port 4 allows *vlan3*, which is perfect. Now let&#8217;s set up *vlan1* and *vlan3* to come in tagged on port 4 and then enable both VLANS on that port. This can be accomplished with the following:

    nvram set vlan1ports="4t 3 2 1 8*"
    nvram set vlan3ports="4t 8"
    nvram set port4vlans="1 3 18 19"
    

Then apply the change and reboot the router:

    nvram commit
    reboot
    

#### Allow Vlan3 to talk to the internet

The following commands will allow access to the WAN for vlan3:

    iptables -I FORWARD -i vlan2 -o vlan3 -j ACCEPT
    iptables -I FORWARD -i vlan3 -o vlan2 -j ACCEPT
    iptables -I FORWARD -i br0 -o vlan3 -j ACCEPT
    iptables -I FORWARD -i vlan3 -o br00 -j ACCEPT
    iptables -I INPUT -i vlan3 -j ACCEPT
    

I was using <a href="http://virtuallyhyper.com/2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/']);">fwbuilder</a>, so I had to add the vlan3 interface to the configuration and allow access to and from it.

Now I can configure two Virtual PortGroups on my Virtual Switch and tag vlans 1 and 3 on them. Then I can put any VM on any of those networks just by assigning their nics to the appropriate port group.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2014/04/tag-multiple-vlans-on-trunk-port-on-dd-wrt-router/" title=" Tag Multiple VLANs on Trunk Port on DD-WRT Router" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:DD-WRT,Trunk Port,blog;button:compact;">I was running an ESXi host in my home network and I wanted to dedicate on NIC of the ESXi for VM traffic. Since I was planning on having different...</a>
</p>