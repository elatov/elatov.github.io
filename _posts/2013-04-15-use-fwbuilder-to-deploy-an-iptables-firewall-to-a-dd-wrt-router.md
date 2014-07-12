---
title: Use FWBuilder to Deploy an IPtables Firewall to a DD-WRT Router
author: Karim Elatov
layout: post
permalink: /2013/04/use-fwbuilder-to-deploy-an-iptables-firewall-to-a-dd-wrt-router/
dsq_thread_id:
  - 1405531416
categories: ['os', 'home_lab', 'networking']
tags: ['linux', 'iptables', 'dd_wrt', 'fwbuilder', 'nat']
---

I decided to learn how [FWBuilder](http://www.fwbuilder.org/) works and what is better than deploying in a home environment and making sure nothing breaks in the process? At home I have a router that is running [DD-WRT](http://www.dd-wrt.com) and FWBuilder works with that. So I decided to use that as my test, a good starting point is the [how-to](http://www.dd-wrt.com/wiki/index.php/Firewall_Builder) from DD-WRT.


### Enable SSH On DD-WRT

The first thing that we need to do is enable SSH on the DD-WRT router. To do so, point your browser to the internal IP of your router. In my case it's **192.168.1.1**. After logging in, I saw the following:

![dd wrt login Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/dd-wrt-login.png)

Then go to "Services" Tab, scroll down, and you will see "Secure Shell":

![ddwrt services sshd Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/ddwrt-services-sshd.png)

Go ahead and enable it:

![ddwrt sshd enabled Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/ddwrt-sshd-enabled.png)

After it's enabled you will be able to login:

    elatov@crbook:~$ ssh 192.168.1.1 -l root
    DD-WRT v24-sp2 std (c) 2010 NewMedia-NET GmbH
    Release: 08/12/10 (SVN revision: 14929)
    root@192.168.1.1's password:
    ==========================================================

     ____  ___    __        ______ _____         ____  _  _
     | _ \| _ \   \ \      / /  _ _   _| __   _|___ \| || |
     || | || ||____\ \ /\ / /| |_) || |   \ \ / / __) | || |_
     ||_| ||_||_____\ V  V / |  _ < | |    \ V / / __/|__   _|
     |___/|___/      _/_/  |_| _\|_|     _/ |_____|  |_|

                           DD-WRT v24-sp2

    http://www.dd-wrt.com

    ==========================================================


    BusyBox v1.13.4 (2010-08-12 12:34:49 CEST) built-in shell (ash)
    Enter 'help' for a list of built-in commands.

    root@DD-WRT:~#


### Default DD-WRT IPtables

At this point we can make a back up of the current **iptables** rules:

    root@DD-WRT:~# iptables -L -n -v
    Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
     pkts bytes target     prot opt in     out     source               destination
     1978  200K ACCEPT     0    --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED
        0     0 DROP       udp  --  vlan2  *       0.0.0.0/0            0.0.0.0/0           udp dpt:520
        0     0 DROP       udp  --  br0    *       0.0.0.0/0            0.0.0.0/0           udp dpt:520
        0     0 ACCEPT     udp  --  *      *       0.0.0.0/0            0.0.0.0/0           udp dpt:520
        5   438 DROP       icmp --  vlan2  *       0.0.0.0/0            0.0.0.0/0
        0     0 DROP       2    --  *      *       0.0.0.0/0            0.0.0.0/0
        1    70 ACCEPT     0    --  lo     *       0.0.0.0/0            0.0.0.0/0           state NEW
     1173 80131 logaccept  0    --  br0    *       0.0.0.0/0            0.0.0.0/0           state NEW
     2828  254K DROP       0    --  *      *       0.0.0.0/0            0.0.0.0/0

    Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
     pkts bytes target     prot opt in     out     source               destination
        0     0 ACCEPT     47   --  *      vlan2   192.168.1.0/24       0.0.0.0/0
        0     0 ACCEPT     tcp  --  *      vlan2   192.168.1.0/24       0.0.0.0/0           tcp dpt:1723
        0     0 ACCEPT     0    --  br0    br0     0.0.0.0/0            0.0.0.0/0
     4053  244K TCPMSS     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           tcp flags:0x06/0x02 TCPMSS clamp to PMTU
     179K  123M lan2wan    0    --  *      *       0.0.0.0/0            0.0.0.0/0
     173K  122M ACCEPT     0    --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED
        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            192.168.1.100       tcp dpt:22
        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            192.168.1.100       tcp dpt:80
        0     0 TRIGGER    0    --  vlan2  br0     0.0.0.0/0            0.0.0.0/0           TRIGGER type:in match:0 relate:0
     6078  383K trigger_out 0   --  br0    *       0.0.0.0/0            0.0.0.0/0
     6054  381K ACCEPT     0    --  br0    *       0.0.0.0/0            0.0.0.0/0           state NEW
       24  2848 DROP       0    --  *      *       0.0.0.0/0            0.0.0.0/0
    ...
    ...


There are a lot after that, but they are just empty chains. We can also check out the NAT table:

    root@DD-WRT:~# iptables -L -n -v -t nat
    Chain PREROUTING (policy ACCEPT 10638 packets, 792K bytes)
     pkts bytes target     prot opt in     out     source               destination
        0     0 DNAT       icmp --  *      *       0.0.0.0/0            67.172.135.80       to:192.168.1.1
        0     0 DNAT       tcp  --  *      *       0.0.0.0/0            67.172.135.80       tcp dpt:22 to:192.168.1.100:22
        0     0 DNAT       tcp  --  *      *       0.0.0.0/0            67.172.135.80       tcp dpt:80 to:192.168.1.100:80
     3788  287K TRIGGER    0    --  *      *       0.0.0.0/0            67.172.135.80       TRIGGER type:dnat match:0 relate:0

    Chain POSTROUTING (policy ACCEPT 1 packets, 70 bytes)
     pkts bytes target     prot opt in     out     source               destination
     4896  316K SNAT       0    --  *      vlan2   0.0.0.0/0            0.0.0.0/0           to:67.172.135.80
        0     0 RETURN     0    --  *      br0     0.0.0.0/0            0.0.0.0/0           PKTTYPE = broadcast
        1   341 MASQUERADE 0    --  *      br0     192.168.1.0/24       192.168.1.0/24

    Chain OUTPUT (policy ACCEPT 83 packets, 5946 bytes)
     pkts bytes target     prot opt in     out     source               destination


We can see that **vlan2** is used as our public facing interface and **br0** is used as the internal interface.

### DD-WRT Network Interfaces

Checking out all the interfaces I see the following:

    root@DD-WRT:~# ip link
    1: lo: <LOOPBACK,MULTICAST,UP,10000> mtu 16436 qdisc noqueue
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2: eth0: <broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc pfifo_fast
        link/ether 98:fc:11:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    3: eth1: </broadcast><broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc pfifo_fast
        link/ether 98:fc:11:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    4: teql0: <noarp> mtu 1500 qdisc noop
        link/void
    5: tunl0: </noarp><noarp> mtu 1480 qdisc noop
        link/ipip 0.0.0.0 brd 0.0.0.0
    6: gre0: </noarp><noarp> mtu 1476 qdisc noop
        link/gre 0.0.0.0 brd 0.0.0.0
    7: vlan1@eth0: <broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc noqueue
        link/ether 98:fc:11:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    8: vlan2@eth0: </broadcast><broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc noqueue
        link/ether 98:fc:11:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    9: br0: </broadcast><broadcast ,MULTICAST,PROMISC,UP,10000> mtu 1500 qdisc noqueue
        link/ether 98:fc:11:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    10: etherip0: </broadcast><broadcast ,MULTICAST> mtu 1500 qdisc noop
        link/ether 82:60:9c:xx:xx:xx brd ff:ff:ff:ff:ff:ff


So we have two physical interface: **eth0** and **eth1**. Both **vlan1** and **vlan2** are going through **eth0**:

    root@DD-WRT:~# cat /proc/net/vlan/config
    VLAN Dev name    | VLAN ID
    Name-Type: VLAN_NAME_TYPE_PLUS_VID_NO_PAD
    vlan1          | 1  | eth0
    vlan2          | 2  | eth0


And the bridge (**br0**) is for the connection between **vlan1** (which is going through eth0) and **eth1**:

    root@DD-WRT:~# brctl show
    bridge name bridge id       STP enabled interfaces
    br0     8000.98fc11861554   no      vlan1
                                eth1


To confirm my suspicion I checked out the IP addresses assigned to the mentioned interfaces:

    root@DD-WRT:~# ip -4 addr
    1: lo: <loopback ,MULTICAST,UP,10000> mtu 16436 qdisc noqueue
        inet 127.0.0.1/8 brd 127.255.255.255 scope host lo
    8: vlan2@eth0: <broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc noqueue
        inet 67.172.135.80/23 brd 67.172.135.255 scope global vlan2
    9: br0: </broadcast><broadcast ,MULTICAST,PROMISC,UP,10000> mtu 1500 qdisc noqueue
        inet 192.168.1.1/24 brd 192.168.1.255 scope global br0
        inet 169.254.255.1/16 brd 169.254.255.255 scope global br0:0


we can see that **vlan2** is the public IP (**67.172.135.80**) and **br0** is the internal IP (**192.168.1.1**).

### DD-WRT Internal Networking

At this point you might ask: so where is the wireless interface? Well that is actually **eth1**. You can confirm by running the following:

    root@DD-WRT:~# nvram get wl0_ifname
    eth1


When we SSH over to a DD-WRT router we are actually not seeing the full picture. There is an excellent description of how networking is setup on the DD-WRT router [here](http://www.dd-wrt.com/wiki/index.php/Default_Configuration_Overview), here is a picture from that article:

![dd wrt internals Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/dd-wrt-internals.png)

You will notice the vlans don't match but those are just representations. From the above article:

> Within the switch entity there are defined two VLANs - vlan0 and vlan1, [**vlan1** and **vlan2**]. Vlan0, [**Vlan1**] is the one on which all of the numbered (1-4) RJ45 sockets on the back belong to. Vlan1, [**Vlan2**] is the one on which the WAN socket resides.

And here is more information regarding the wireless device:

> The wireless device is on a separate interface called eth1. This interface, which is not part of the switch, is available to routing logic just as eth0 and the vlans are. However, DD-WRT by default does not use routing logic per se to move traffic between vlan0, [**vlan1**] and eth1; rather, it employs a bridge device - who's interface is called br0 - that logically combines vlan0, [**vlan1**] and eth1 into a single interface.

There is actually a good community [post](http://www.dd-wrt.com/phpBB2/viewtopic.php?p=431294#431294) on simplifying the above article, here are the important excerpts:

> *   The switch's ports are divided into port 0-3 (physical LAN ports are numbered differently) for the local LAN and Port 4 for the WAN
> *   To separate the WAN traffic from the LAN traffic, the switch is divided into virtual LANs called VLANs. VLAN0 is LAN traffic (ports 0-3) and VLAN1 is WAN traffic (port 4).
> *   The connection between the switch (port 5) and the router (eth0) is called a trunk. A trunk is a connection that allows multiple VLAN traffic to pass through. In order for the trunk to identify which VLAN the data belongs to, the data frame is tagged with the VLAN number.
> *   Traffic between the two VLANs is controlled by the router using iptables and ip route commands
> *   Lastly, the wireless port eth1 (because it is not part of the switch) is bridged (using br0) to VLAN0 and is treated the same as any other port of the switch

The person from the above community post actually created another diagram to ease the above explanation:

![dd wrt internal simple Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/dd-wrt-internal-simple.png)

Don't get hung up on the **eth0.x** VLAN representations, from the same article:

> NOTE: I've labelled the tagged VLANs as eth0.0 and eth0.1 on the following diagram which is a standard way of representing VLANs as subinterfaces on eth0 in routing BUT this is not the way that dd-wrt documentation represents them. The eth0.0 represents VLAN 0 and the eth0.1 represents VLAN 1

Looking at it from a firewall aspect: **vlan2** represents the external/public interface and **br0** (combination of eth1/wireless and vlan1/LAN interfaces) is our internal/private interface. For good measure checking out the routing table, we see the following:

    root@DD-WRT:~# ip route
    67.172.134.1    dev vlan2  scope link
    192.168.1.0/24  dev br0    proto kernel  scope link  src 192.168.1.1
    67.172.134.0/23 dev vlan2  proto kernel  scope link  src 67.172.135.80
    169.254.0.0/16  dev br0    proto kernel  scope link  src 169.254.255.1
    127.0.0.0/8     dev lo     scope link
    default         via 67.172.134.1 dev vlan2


Nothing crazy, **vlan2** is used for the public IP space and **br0** is used for the private IP space :)

### Enabling JFFS on DD-WRT

There are two ways to use FWBuilder with DD-WRT. One is to setup the **iptables** to run from **nvram** and the other is to store the **iptables** configs in **JFFS** and run them from there. The latter seemed more pleasant, from the FWBuilder [user-guide](http://www.fwbuilder.org/4.0/docs/users_guide5/dd-wrt.shtml):

> **12.3.1. DD-WRT (nvram)**
> In this mode generated script is shorter and does not support command-line arguments "start", "stop", "status". The script does not try to load iptables modules on the firewall but configures inetrface addresses, vlans, bridge ports and bonding interfaces. When you set host OS of the firewall object to "DD-WRT (nvram)", built-in policy installer saves the script in nvram variable "fwb" and configures nvram variable "rc_firewall" to run this script.

And here is the description for **JFFS**:

> When the firewall is configured with host OS "DD-WRT (jffs)", built-in policy installer copies generated script to the file "/jffs/firewall/firewall.fs" on the firewall and configures nvram variable "rc_firewall" to call this script.

So let's go ahead and enable **JFFS**. Most of the instructions are laid out [here](http://www.dd-wrt.com/wiki/index.php/Journalling_Flash_File_System). Once logged into DD-WRT, go to the "Administration" tab, scroll down and enable the "JFFS2 Support" and "Clean JFFS2" options. Then click "Apply Settings" and not "Save". After it's enabled, SSH over to the router and make sure it's mounted:

    root@DD-WRT:~# df -h
    Filesystem                Size      Used Available Use% Mounted on
    /dev/root                 3.5M      3.5M         0 100% /
    /dev/mtdblock/4           2.9M    260.0K      2.6M   9% /jffs


That looks good. Now go back and disable "Clean JFFS2" and click "Save":

![jffs2 clean disabled Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/jffs2-clean-disabled.png)

Now reboot the router to make sure everything is good. After the reboot you should still see **JFFS** mounted:

    root@DD-WRT:~# uptime
     19:38:54 up 3 min, load average: 0.04, 0.06, 0.02
    root@DD-WRT:~# df -h
    Filesystem                Size      Used Available Use% Mounted on
    /dev/root                 3.5M      3.5M         0 100% /
    /dev/mtdblock/4           2.9M    240.0K      2.6M   8% /jffs


### Prepare DD_WRT For FWBuilder

There are a couple of tweaks that need to be done for FW-Builder to work properly, they are listed [here](http://www.dd-wrt.com/wiki/index.php/Firewall_Builder):

1.  Create the **firewall** directory:

         root@DD-WRT:~# mkdir /jffs/firewall


2.  Create a symbolic link for **iptables-save**:

         root@DD-WRT:~# mkdir /jffs/bin
         root@DD-WRT:~# ln -s /usr/sbin/iptables /jffs/bin/iptables-save


At this point you can actually create a backup of the rules and copy them to your local workstation:

    root@DD-WRT:~# iptables-save > /tmp/fw.txt


and then **scp** them off:

    elatov@crbook:~$ scp root@192.168.1.1:/tmp/fw.txt .
    DD-WRT v24-sp2 std (c) 2010 NewMedia-NET GmbH
    Release: 08/12/10 (SVN revision: 14929)
    root@192.168.1.1's password:
    fw.txt                                        100% 3252     3.2KB/s   00:00


Lastly, make sure the rules are there:

    elatov@crbook:~$ head -20 fw.txt
    # Generated by iptables-save v1.3.7 on Sun Apr 14 19:26:05 2013
    *raw
    :PREROUTING ACCEPT [193870515:159108806829]
    :OUTPUT ACCEPT [3128300:253591831]
    COMMIT
    # Completed on Sun Apr 14 19:26:05 2013
    # Generated by iptables-save v1.3.7 on Sun Apr 14 19:26:05 2013
    *nat
    :PREROUTING ACCEPT [3902:369895]
    :POSTROUTING ACCEPT [3:178]
    :OUTPUT ACCEPT [158:10284]
    -A PREROUTING -d 67.172.135.80 -p icmp -j DNAT --to-destination 192.168.1.1
    -A PREROUTING -d 67.172.135.80 -p tcp -m tcp --dport 22 -j DNAT --to-destination 192.168.1.100:22
    -A PREROUTING -d 67.172.135.80 -p tcp -m tcp --dport 80 -j DNAT --to-destination 192.168.1.100:80
    -A PREROUTING -d 67.172.135.80 -j TRIGGER --trigger-proto --trigger-match 0-0 --trigger-relate 0-0
    -A POSTROUTING -o vlan2 -j SNAT --to-source 67.172.135.80
    -A POSTROUTING -o br0 -m pkttype --pkt-type broadcast -j RETURN
    -A POSTROUTING -s 192.168.1.0/255.255.255.0 -d 192.168.1.0/255.255.255.0 -o br0 -j MASQUERADE
    COMMIT


### Install and Launch FWBuilder

FWBuilder is available on most Linux distros, install as necessary:

    apt-get install fwbuilder
    yum install fwbuilder


After it's installed you can launch it by running:

    fwbuilder


at which point you will see the following window:

![fwbuilder started Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fwbuilder_started.png)

Then click on "Create Firewall" and fill out the specs of our firewall. Here is how mine looked like:

![fwbldr new fw dd wrt Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fwbldr_new_fw_dd-wrt.png)

From the Templates I chose the "DDWRT Template":

![ddwrt template chose Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/ddwrt-template-chose.png)

On the "Objects" screen, I renamed **vlan1** to **vlan2**, but the left the rest as is:

![fw bldr create objects Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw_bldr_create_objects.png)

At this point you will see the following firewall policy: ![fw bldr dd wrt policy Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw-bldr-dd-wrt-policy.png)

### FWBuilder Firewall Rule Break-Down

We can break down each rule, just to make sure we know what is going on. If we "Save" the project and then "Compile" the rule, we can then inspect the actual generated file:

![inspect fw script Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/inspect_fw_script.png)

Here is what **Rule 0** does:

    $IPTABLES -A INPUT -i vlan2   -s $i_vlan2   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A INPUT -i vlan2   -s 192.168.1.1   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A INPUT -i vlan2   -s 192.168.1.0/24   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A FORWARD -i vlan2   -s $i_vlan2   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A FORWARD -i vlan2   -s 192.168.1.1   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A FORWARD -i vlan2   -s 192.168.1.0/24   -m state --state NEW  -j In_RULE_0
    $IPTABLES -A In_RULE_0  -j LOG  --log-level info --log-prefix "RULE 0 -- DENY "
    $IPTABLES -A In_RULE_0  -j DROP


So basically if anything comes into our public interface with a private ip (192.168.1.0/24), it will be dropped. This is good since we should never see the private IP space from the internet. Here is **Rule 1**:

    $IPTABLES -A INPUT -i lo   -m state --state NEW  -j ACCEPT
    $IPTABLES -A OUTPUT -o lo   -m state --state NEW  -j ACCEPT


This just allows traffic to and from the loopback interface. Here is **Rule 2**:

    $IPTABLES -A OUTPUT -p udp -m udp  -m multiport  -d 255.255.255.255   --dports 68,67  -m state --state NEW  -j DROP
    $IPTABLES -A INPUT -p udp -m udp  -m multiport  -d 255.255.255.255   --dports 68,67  -m state --state NEW  -j DROP


This blocks Broadcast DHCP Requests, I am actually not sure why this is setup. Here is **Rule 3**:

    $IPTABLES -N Cid4244X4059.0
    $IPTABLES -A INPUT  -s 192.168.1.0/24   -m state --state NEW  -j Cid4244X4059.0
    $IPTABLES -A Cid4244X4059.0 -p icmp  -m icmp  --icmp-type 8/0   -j ACCEPT
    $IPTABLES -A Cid4244X4059.0 -p tcp -m tcp  -m multiport  --dports 80,2869,22,5000,5431  -j ACCEPT
    $IPTABLES -A Cid4244X4059.0 -p udp -m udp  -m multiport  --dports 1900,68,67  -j ACCEPT


This rules allows UPNP,SSH,HTTP,DHCP, and ICMP from the internal network to our firewall. Here is **Rule 4**:

    $IPTABLES -N Cid4276X4059.0
    $IPTABLES -A OUTPUT  -d 192.168.1.0/24   -j Cid4276X4059.0
    $IPTABLES -A Cid4276X4059.0 -p icmp  -m icmp  --icmp-type 0/0   -j ACCEPT
    $IPTABLES -A Cid4276X4059.0 -p icmp  -m icmp  --icmp-type 11/0   -j ACCEPT


This allows outbound ICMP traffic from the internal Network. This is to allow internal IPs to receive ping replies from the external network. Here is **Rule 5**:

    $IPTABLES -A INPUT  -s $i_vlan2   -m state --state NEW  -j ACCEPT
    $IPTABLES -A INPUT  -s 192.168.1.1   -m state --state NEW  -j ACCEPT
    $IPTABLES -A OUTPUT  -m state --state NEW  -j ACCEPT


This allows all new traffic from the firewall to the internal network. Here is **Rule 6**:

    $IPTABLES -A OUTPUT  -d $i_vlan2   -m state --state NEW  -j RULE_6
    $IPTABLES -A OUTPUT  -d 192.168.1.1   -m state --state NEW  -j RULE_6
    $IPTABLES -A INPUT  -m state --state NEW  -j RULE_6
    $IPTABLES -A RULE_6  -j LOG  --log-level info --log-prefix "RULE 6 -- DENY "
    $IPTABLES -A RULE_6  -j DROP


This is kind of a "catch all other" rule, so if anything is not matched from above, then block that traffic that is destined to the firewall's private interface. Here is **Rule 7**:

    $IPTABLES -A OUTPUT -p icmp  -m icmp  -d 192.168.1.0/24   --icmp-type 3  -m state --state NEW  -j ACCEPT
    $IPTABLES -A INPUT -p icmp  -m icmp  -d 192.168.1.0/24   --icmp-type 3  -m state --state NEW  -j ACCEPT
    $IPTABLES -A FORWARD -p icmp  -m icmp  -d 192.168.1.0/24   --icmp-type 3  -m state --state NEW  -j ACCEPT


Allow the ICMP Unreachable type to the internal network. This is to notify the internal machines that their ping failed to any IP (internal or external). Here is **Rule 8**:

    $IPTABLES -A INPUT  -s 192.168.1.0/24   -m state --state NEW  -j ACCEPT
    $IPTABLES -A OUTPUT  -s 192.168.1.0/24   -m state --state NEW  -j ACCEPT
    $IPTABLES -A FORWARD  -s 192.168.1.0/24   -m state --state NEW  -j ACCEPT


Allow any traffic that is sourced from our internal network, this is good to have for NAT and other things like that. And here is the last **Rule (9)**:

    $IPTABLES -N RULE_9
    $IPTABLES -A OUTPUT  -m state --state NEW  -j RULE_9
    $IPTABLES -A INPUT  -m state --state NEW  -j RULE_9
    $IPTABLES -A FORWARD  -m state --state NEW  -j RULE_9
    $IPTABLES -A RULE_9  -j LOG  --log-level info --log-prefix "RULE 9 -- DENY "
    $IPTABLES -A RULE_9  -j DROP


Deny the rest :) Without looking at the specific **iptables** commands, you can just look at the **Policy** and get the same feel of the rules.

### Allow DNS Queries to the Firewall

I noticed that we don't allow DNS to our DD-WRT firewall and **dnsmasq** is running on the DD-WRT Router . So let's add that, change the library from "user" to "standard" and go to "Service" > "UDP" and you will see a service called "domain":

![domain service std library Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/domain_service_std_library.png)

Now let's go ahead and drag-and-drop that into our 3rd Rule:

![drag drop dns to policy Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/drag_drop_dns_to_policy.png)

Usually DNS uses UDP for quieries and TCP for zone transfers, but I allowed both just in case:

![domain added policy Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/domain_added_policy.png)

Later on I discovered that there is a DNS groups that contains both already:

![DNS group fwbuilder Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/DNS_group_fwbuilder.png)

Now go ahead and compile the firewall:

![Compile rules fwbldr Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Compile_rules_fwbldr.png)

Once you hit the "Compile" button you will be presented with available firewalls to compile:

![Select fw to compile Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Select_fw_to_compile.png)

Select the only one you have and click "Next", if the compile is successful you will see the following:

![Compile succesful Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Compile_succesful.png)

You can click "Inspect Generated Files" and make sure the new **Rule 3** looks something like this:

    # Rule 3 (global)
    #
    echo "Rule 3 (global)"
    #
    # SSH Access to firewall is permitted
    # only from internal network
    $IPTABLES -N Cid4244X4059.0
    $IPTABLES -A INPUT  -s 192.168.1.0/24   -m state --state NEW  -j Cid4244X4059.0
    $IPTABLES -A Cid4244X4059.0 -p icmp  -m icmp  --icmp-type 8/0   -j ACCEPT
    $IPTABLES -A Cid4244X4059.0 -p tcp -m tcp  -m multiport  --dports 53,80,2869,22,5000,5431  -j ACCEPT
    $IPTABLES -A Cid4244X4059.0 -p udp -m udp  -m multiport  --dports 1900,68,67,53  -j ACCEPT


Notice both **UDP** and **TCP** **53** are now in there.

### FWBuilder Backup Plan

It's always a good idea to always allow a specific IP to connect to our firewall (in case we break something and lock ourselves out). To set this up, double click on the Firewall and you will see the following:

![fw bldr fw selected Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw-bldr_fw_selected.png)

Then click on "Firewall Settings" and you will see the following:

![fw settings Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw_settings.png)

Check the box that says "Always permit ssh access from the management workstation with this address" and enter the desired IP:

![fw settings ssh back door Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw_settings_ssh_back_door.png)

### Deploy the New Firewall to the DD_WRT Router

Under the "Firewall Settings", make sure "Compiler" Tab looks like this:

![Compiler tab fw sts Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Compiler_tab_fw_sts.png)

and the "Installer" Tab looks like this:

![Installer Tab firewall sts Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Installer_Tab_firewall_sts.png)

If you chose the "DD-WRT (JFFS)" for the OS those should be the default. You can also check out the installer scripts for DD-WRT from the FWBuilder package:

    elatov@crbook:/usr/share/fwbuilder-5.1.0.3599/configlets/dd-wrt-jffs$ pwd
    /usr/share/fwbuilder-5.1.0.3599/configlets/dd-wrt-jffs
    elatov@crbook:/usr/share/fwbuilder-5.1.0.3599/configlets/dd-wrt-jffs$ tail installer_commands_root

    {{if run}}
    echo '{{$fwbprompt}}';
    chmod +x {{$fwdir}}/{{$fwscript}};
    /usr/sbin/nvram unset rc_firewall;
    /usr/sbin/nvram set rc_firewall="{{$fwdir}}/{{$fwscript}}";
    /usr/sbin/nvram commit;
    sh {{$fwdir}}/{{$fwscript}} && echo 'Policy activated'
    {{endif}}


Looks like we are going to set the appropriate settings on the DD-WRT Router. Then go ahead and click on the "Install" button:

![fw builder install button Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/fw_builder_install_button.png)

It will launch the wizard and you can select which firewall to install (we only have one). Then it will "Compile" the rules and then it will ask for the SSH credentials:

![Install Options for dd wrt Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Install_Options_for_dd-wrt.png)

After I hit "Install", I saw the following:

    Installation plan:
    Copy file: /home/elatov/firewall.fw --> /jffs/firewall/firewall.fw
    Run script echo '--**--**--';
    chmod +x /jffs/firewall/firewall.fw;
    /usr/sbin/nvram unset rc_firewall;
    /usr/sbin/nvram set rc_firewall="/jffs/firewall/firewall.fw";
    /usr/sbin/nvram commit;
    sh /jffs/firewall/firewall.fw && echo 'Policy activated'

    Copying /home/elatov/firewall.fw -> 192.168.1.1:/jffs/firewall/firewall.fw
    Running command '/usr/bin/fwbuilder -Y scp -o ConnectTimeout=30 -q /home/elatov/firewall.fw root@192.168.1.1:/jffs/firewall/firewall.fw'
    Firewall Builder GUI 5.1.0.3599
    root@192.168.1.1's password:
    SSH session terminated, exit status: 0
    Running command '/usr/bin/fwbuilder -X ssh -o ServerAliveInterval=10 -t -t -v -l root 192.168.1.1 echo '--**--**--';
    chmod +x /jffs/firewall/firewall.fw;
    /usr/sbin/nvram unset rc_firewall;
    /usr/sbin/nvram set rc_firewall="/jffs/firewall/firewall.fw";
    /usr/sbin/nvram commit;
    sh /jffs/firewall/firewall.fw && echo 'Policy activated''
    Firewall Builder GUI 5.1.0.3599


The above looked good and after it finished I saw the following:

![Successful install Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Successful_install.png)

I then logged into the DD-WRT Router via SSH (Luckily I was still able to), and checked out the firewall:

    root@DD-WRT:~# iptables -L -n -v
    Chain INPUT (policy DROP 2 packets, 188 bytes)
     pkts bytes target     prot opt in     out     source               destination
      961 88504 ACCEPT     0    --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED
        0     0 ACCEPT     tcp  --  *      *       192.168.1.100        0.0.0.0/0           tcp dpt:22 state NEW,ESTABLISHED
        0     0 In_RULE_0  0    --  vlan2  *       67.172.135.80        0.0.0.0/0           state NEW
        0     0 In_RULE_0  0    --  vlan2  *       192.168.1.1          0.0.0.0/0           state NEW
        0     0 In_RULE_0  0    --  vlan2  *       192.168.1.0/24       0.0.0.0/0           state NEW
        1    64 ACCEPT     0    --  lo     *       0.0.0.0/0            0.0.0.0/0           state NEW
       29  9544 DROP       udp  --  *      *       0.0.0.0/0            255.255.255.255     udp multiport dports 68,67 state NEW
      290 19775 Cid4244X4059.0 0 --  *     *       192.168.1.0/24       0.0.0.0/0           state NEW
        0     0 ACCEPT     0    --  *      *       67.172.135.80        0.0.0.0/0           state NEW
        0     0 ACCEPT     0    --  *      *       192.168.1.1          0.0.0.0/0           state NEW
      123 12406 RULE_6     0    --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW
        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            192.168.1.0/24      icmp type 3 state NEW
        0     0 ACCEPT     0    --  *      *       192.168.1.0/24       0.0.0.0/0           state NEW
        0     0 RULE_9     0    --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW


The new rules were definitely in place and my network didn't come to a screaming halt. I didn't configure any NAT'ing so my NAT table was very small:

    root@DD-WRT:~# iptables -L -n -v -t nat
    Chain PREROUTING (policy ACCEPT 18914 packets, 1784K bytes)
     pkts bytes target     prot opt in     out     source               destination

    Chain POSTROUTING (policy ACCEPT 124 packets, 9193 bytes)
     pkts bytes target     prot opt in     out     source               destination
      189 12778 MASQUERADE  0    --  *      vlan2   192.168.1.0/24       0.0.0.0/0

    Chain OUTPUT (policy ACCEPT 459 packets, 31067 bytes)
     pkts bytes target     prot opt in     out     source               destination


I also noticed that the install script removed the **169.254.255** address:

    root@DD-WRT:~# ip -4 a
    1: lo: <loopback ,MULTICAST,UP,10000> mtu 16436 qdisc noqueue
        inet 127.0.0.1/8 brd 127.255.255.255 scope host lo
    8: vlan2@eth0: <broadcast ,MULTICAST,UP,10000> mtu 1500 qdisc noqueue
        inet 67.172.135.80/23 brd 67.172.135.255 scope global vlan2
    9: br0: </broadcast><broadcast ,MULTICAST,PROMISC,UP,10000> mtu 1500 qdisc noqueue
        inet 192.168.1.1/24 brd 192.168.1.255 scope global br0


That shouldn't break anything... I hope. Also checking to make sure the script is setup:

    root@DD-WRT:~# nvram get rc_firewall
    /jffs/firewall/firewall.fw


That all looks good, I then rebooted the router one more time to make sure the rules come up on boot.

### Allow DHCP from the Internal Network

After I rebooted I realized I wasn't able to get a DHCP address from the wireless network. So I noticed that the DHCP server actually runs on the public interface:

    root@DD-WRT:~# ps | grep dh
     1974 root       984 S    udhcpc -i vlan2 -p /var/run/udhcpc.pid -s /tmp/udhcpc


I tried to change that but I couldn't (without running multiple DHCP Servers). So **Rule 2** was blocking the private network from broadcasting to the public interface. To get around this I modified **Rule 2** to look like this:

![rule2 changed Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/rule2-changed.png)

After I compiled the firewall I saw the following rule generated:

    $IPTABLES -A INPUT -i br0  -p udp -m udp  -m multiport  -d 255.255.255.255   --dports 68,67  -m state --state NEW  -j ACCEPT
    $IPTABLES -A OUTPUT -o br0  -p udp -m udp  -m multiport  -d 255.255.255.255   --dports 68,67  -m state --state NEW  -j ACCEPT


I still saw some "Denies" to the public interface:

    root@DD-WRT:~# dmesg
    RULE 6 -- DENY IN=vlan2 OUT= MAC=ff:ff:ff:ff:ff:ff:00:01:5c:22:b2:01:08:00:45:00:01:4c SRC=73.252.30.1 DST=255.255.255.255 LEN=332 TOS=0x00 PREC=0x00 TTL=64 ID=1950 PROTO=UDP SPT=67 DPT=68 LEN=312
    RULE 6 -- DENY IN=vlan2 OUT= MAC=ff:ff:ff:ff:ff:ff:00:01:5c:22:b2:01:08:00:45:00:01:48 SRC=73.252.30.1 DST=255.255.255.255 LEN=328 TOS=0x00 PREC=0x00 TTL=64 ID=2053 PROTO=UDP SPT=67 DPT=68 LEN=308


The above were from the external network, and I was able to get a DHCP address from the internal network just fine.

### Configure Port-Forwarding(DNAT) Using FWBuilder

By default we have the following rule for our NAT:

![Nat Rules def Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Nat_Rules_def.png)

Creating DNAT rules is outlines in [this](http://www.fwbuilder.org/4.0/docs/users_guide5/destination-address-translation.shtml) FWBuilder guide. So let's forward port 80 to our web server which has the Internal IP of **192.168.1.100**. Here is NAT rule that I created for that:

![dnat port 80 Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/dnat_port_80.png)

On top of that I also added the following rule to main policy:

![Forward for web server policy Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/Forward_for_web_server_policy.png)

After you compile and install the firewall you will see these two rules in **iptables**:

    root@DD-WRT:~# iptables -L FORWARD -n -v | grep 'dpt:80'
        0     0 In_RULE_0  tcp  --  +      *       0.0.0.0/0            192.168.1.100       tcp dpt:80 state NEW
    root@DD-WRT:~# iptables -L -n -v -t nat | grep 'dpt:80'
        0     0 DNAT       tcp  --  *      *       0.0.0.0/0            67.172.135.80       tcp dpt:80 to:192.168.1.100:80


As a side note, if you want the webserver to be accessible using the public IP from both external and internal networks then add the following NAT rule:

![dnat from internal Use FWBuilder to Deploy an IPtables Firewall to a DD WRT Router](https://github.com/elatov/uploads/raw/master/2013/04/dnat_from_internal.png)

That will generate the following rules:

    root@DD-WRT:~# iptables -L -n -v -t nat | grep 'dpt:80'
        6   360 DNAT       tcp  --  *      *       0.0.0.0/0            67.172.135.80       tcp dpt:80 to:192.168.1.100:80
        6   360 SNAT       tcp  --  *      br0     0.0.0.0/0            192.168.1.100       tcp dpt:80 to:192.168.1.1


This is covered in the FWBuilder chapter entitled "[RFC](http://www.fwbuilder.org/4.0/docs/users_guide5/dnat_to_same_network.shtml), here is what we see:

> Hairpinning allows two endpoints on the internal side of the NAT to communicate even if they only use each other's external IP addresses and ports.

Now I have completely replaced the default **iptables** firewall on the DD-WRT Router with the firewall I built with FWBuilder. Now if I need to make any changes I can just fire up FWBuilder and drag-and-drop objects to create my new rules and feel like I am a enterprise network administrator :)

<root> </root>

### Related Posts

- [Snort On Debian](/2014/04/snort-debian/)

