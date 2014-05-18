---
title: RHCSA and RHCE Chapter 5 Networking
author: Karim Elatov
layout: post
permalink: /2013/01/rhcsa-and-rhce-chapter-5-networking/
dsq_thread_id:
  - 1406334271
categories:
  - Certifications
  - Networking
  - RHCSA and RHCE
  - VMware
tags:
  - /etc/hosts
  - /etc/sysconfig/network-scripts/route-eth
  - getent hosts
  - host
  - ICMP
  - ifconfig
  - ifdown
  - ifup
  - ip route
  - lsof -i
  - netstat
  - nsswitch.conf
  - ping
  - route
---
The basics of this were covered in [Chapter 1](http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-1-installation/). Here is quick look at my **ifconfig** output:

    [root@rhel01 ~]# ifconfig
    eth0 Link encap:Ethernet HWaddr 00:50:56:17:1B:A4
    inet addr:10.131.65.22 Bcast:10.131.79.255 Mask:255.255.240.0
    inet6 addr: fe80::250:56ff:fe17:1ba4/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:211512 errors:0 dropped:0 overruns:0 frame:0
    TX packets:1760 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:19554970 (18.6 MiB) TX bytes:313001 (305.6 KiB)
    Interrupt:19 Base address:0x2400

    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:192.168.2.100 Bcast:192.168.2.255 Mask:255.255.255.0
    inet6 addr: fe80::250:56ff:fe17:1ba5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:0 errors:0 dropped:0 overruns:0 frame:0
    TX packets:11 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:0 (0.0 b) TX bytes:678 (678.0 b)
    Interrupt:16 Base address:0x2480

    lo Link encap:Local Loopback
    inet addr:127.0.0.1 Mask:255.0.0.0
    inet6 addr: ::1/128 Scope:Host
    UP LOOPBACK RUNNING MTU:16436 Metric:1
    RX packets:0 errors:0 dropped:0 overruns:0 frame:0
    TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:0
    RX bytes:0 (0.0 b) TX bytes:0 (0.0 b)


We can see that **eth0** has **IP** 10.131.65.22 with a **subnet mask** of 255.255.240.0. **eth1** has **IP** of 192.168.2.100 with a **subnet mask** of 255.255.255.0. The last one (**lo**) is the loopback interface. Check out [Chapter 1](http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-1-installation/) to see how to set up those interfaces.

### Network Interface Actions

Now after you have setup the interfaces you take them down. From "[Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf)":

> First, bring up the bond you created by running **ifconfig** bond up as root:
>
>     # ifconfig bond0 up
>
>
> First, the bond you are configuring must be taken down:
>
>     # ifconfig bond0 down
>

So let's try to take our **eth1** interface down and then bring it back up:

    [root@rhel01 ~]# ifconfig eth1 down
    [root@rhel01 ~]# ifconfig
    eth0 Link encap:Ethernet HWaddr 00:50:56:17:1B:A4
    inet addr:10.131.65.22 Bcast:10.131.79.255 Mask:255.255.240.0
    inet6 addr: fe80::250:56ff:fe17:1ba4/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:215301 errors:0 dropped:0 overruns:0 frame:0
    TX packets:1792 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:19911001 (18.9 MiB) TX bytes:317929 (310.4 KiB)
    Interrupt:19 Base address:0x2400

    lo Link encap:Local Loopback
    inet addr:127.0.0.1 Mask:255.0.0.0
    inet6 addr: ::1/128 Scope:Host
    UP LOOPBACK RUNNING MTU:16436 Metric:1
    RX packets:0 errors:0 dropped:0 overruns:0 frame:0
    TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:0
    RX bytes:0 (0.0 b) TX bytes:0 (0.0 b)


We can see that it is no longer listed in the **ifconfig** output. If we list just that interface:

    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:192.168.2.100 Bcast:192.168.2.255 Mask:255.255.255.0
    BROADCAST MULTICAST MTU:1500 Metric:1
    RX packets:0 errors:0 dropped:0 overruns:0 frame:0
    TX packets:11 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:0 (0.0 b) TX bytes:678 (678.0 b)
    Interrupt:16 Base address:0x2480


Notice next to **BROADCAST** we don't see the **UP**, which of course means that it's down. Now to re-enable the interface:

    [root@rhel01 ~]# ifconfig eth1 up
    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:192.168.2.100 Bcast:192.168.2.255 Mask:255.255.255.0
    inet6 addr: fe80::250:56ff:fe17:1ba5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:0 errors:0 dropped:0 overruns:0 frame:0
    TX packets:14 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:0 (0.0 b) TX bytes:916 (916.0 b)
    Interrupt:16 Base address:0x2480


That looks good. There are also **ifup** and **ifdown** scripts to perform the same functions. From the deployment guide:

> **8.3. Interface Control Scripts**
>
> The interface control scripts activate and deactivate system interfaces. There are two primary interface control scripts that call on control scripts located in the **/etc/sysconfig/network-scripts/** directory: **/sbin/ifdown** and **/sbin/ifup**.
>
> The **ifup** and **ifdown** interface scripts are symbolic links to scripts in the **/sbin/** directory. When either of these scripts are called, they require the value of the interface to be specified, such as:
>
>     ifup eth0
>
>
> Two files used to perform a variety of network initialization tasks during the process of bringing up a network interface are **/etc/rc.d/init.d/functions** and **/etc/sysconfig/networkscripts/network-functions**.
>
> ...
>
> The easiest way to manipulate all network scripts simultaneously is to use the **/sbin/service** command on the network service (**/etc/rc.d/init.d/network**), as illustrated by the following command:
>
>     /sbin/service network action
>
>
> Here, **action** can be either **start**, **stop**, or **restart**.
>
> To view a list of configured devices and currently active network interfaces, use the following command:
>
>     /sbin/service network status
>

Let's check out the status of my networking interfaces:

    [root@rhel01 ~]# service network status
    Configured devices:
    lo eth0 eth1
    Currently active devices:
    lo eth0 eth1


### Change IP of Network Interface

If you want to temporary change the **IP** of you interface without using any files or scripts you can just use **ifconfig**. For example let's change the **IP** of **eth1** to a 172.0.0.2/24 **IP** and then take the interface down and then bring it back up, which will reset the settings. Here is the command to change the **IP** of an interface on the fly:

    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:192.168.2.100 Bcast:192.168.2.255 Mask:255.255.255.0
    inet6 addr: fe80::250:56ff:fe17:1ba5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:70 errors:0 dropped:0 overruns:0 frame:0
    TX packets:17 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:4200 (4.1 KiB) TX bytes:1146 (1.1 KiB)
    Interrupt:16 Base address:0x2480

    [root@rhel01 ~]# ifconfig eth1 172.0.0.2 netmask 255.255.255.0
    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:172.0.0.2 Bcast:172.0.0.255 Mask:255.255.255.0
    inet6 addr: fe80::250:56ff:fe17:1ba5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:70 errors:0 dropped:0 overruns:0 frame:0
    TX packets:17 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:4200 (4.1 KiB) TX bytes:1146 (1.1 KiB)
    Interrupt:16 Base address:0x2480


That looks good, now let's reset the interface:

    [root@rhel01 ~]# ifdown eth1
    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    BROADCAST MULTICAST MTU:1500 Metric:1
    RX packets:70 errors:0 dropped:0 overruns:0 frame:0
    TX packets:17 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:4200 (4.1 KiB) TX bytes:1146 (1.1 KiB)
    Interrupt:16 Base address:0x2480

    [root@rhel01 ~]# ifup eth1
    [root@rhel01 ~]# ifconfig eth1
    eth1 Link encap:Ethernet HWaddr 00:50:56:17:1B:A5
    inet addr:192.168.2.100 Bcast:192.168.2.255 Mask:255.255.255.0
    inet6 addr: fe80::250:56ff:fe17:1ba5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:70 errors:0 dropped:0 overruns:0 frame:0
    TX packets:28 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:4200 (4.1 KiB) TX bytes:1796 (1.7 KiB)
    Interrupt:16 Base address:0x2480


Now it's back to normal.

### Network Static Routes

Now onto routing, from the deployment guide:

> **8.4. Static Routes and the Default Gateway**
>
> Static routes are for traffic that must not, or should not, go through the default gateway. Routing is usually handled by routing devices and therefore it is often not necessary to configure static routes on Red Hat Enterprise Linux servers or clients. Exceptions include traffic that must pass through an encrypted VPN tunnel or traffic that should take a less costly route. The default gateway is for any and all traffic which is not destined for the local network and for which no preferred route is specified in the routing table. The default gateway is traditionally a dedicated network router.
>
> **Static Routes**
>
> Use the **ip route** command to display the IP routing table. If static routes are required, they can be added to the routing table by means of the **ip route add** command and removed using the **ip route del** command. To add a static route to a host address, that is to say to a single IP address, issue the following command as **root**:
>
>     ip route add X.X.X.X
>
>
> where X.X.X.X is the IP address of the host in dotted decimal notation. To add a static route to a network, that is to say to an IP address representing a range of IP addresses, issue the following command as **root**:
>
>     ip route add X.X.X.X/Y
>
>
> where X.X.X.X is the IP address of the network in dotted decimal notation and Y is the network prefix. The network prefix is the number of enabled bits in the subnet mask. This format of network address slash prefix length is referred to as CIDR notation.
>
> Static route configuration is stored per-interface in a **/etc/sysconfig/networkscripts/route-interface** file. For example, static routes for the **eth0** interface would be stored in the **/etc/sysconfig/network-scripts/route-eth0** file. The route-interface file has two formats: IP command arguments and network/netmask directives. These are described below.

### Default Gateway

> **The Default Gateway**
>
> The default gateway is specified by means of the **GATEWAY** directive and can be specified either globally or in interface-specific configuration files. Specifying the default gateway globally has certain advantages especially if more than one network interface is present and it can make fault finding simpler if applied consistently. There is also the **GATEWAYDEV** directive, which is a global option. If multiple devices specify **GATEWAY**, and one interface uses the **GATEWAYDEV** directive, that directive will take precedence. This option is not recommend as it can have unexpected consequences if an interface goes down and it can complicate fault finding.
>
> Global default gateway configuration is stored in the **/etc/sysconfig/network** file. This file specifies gateway and host information for all network interfaces.
>
> **IP Command Arguments Format**
>
> If required in a per-interface configuration file, define a default gateway on the first line. This is only required if the default gateway is not set via DHCP and is not set globally as mentioned above:
>
>     default via X.X.X.X dev interface
>
>
> *X.X.X.X** is the IP address of the default gateway. The **interface** is the interface that is connected to, or can reach, the default gateway. The **dev** option can be omitted, it is optional.
>
> Define a static route. Each line is parsed as an individual route:
>
>     X.X.X.X/Y via X.X.X.X dev interface
>
>
> **X.X.X.X/Y** is the network address and netmask for the static route. **X.X.X.X** and **interface** are the IP address and interface for the default gateway respectively. The X.X.X.X address does not have to be the default gateway IP address. In most cases, X.X.X.X will be an IP address in a different subnet, and interface will be the interface that is connected to, or can reach, that subnet. Add as many static routes as required.
>
> The following is a sample **route-eth0** file using the IP command arguments format. The default gateway is 192.168.0.1, interface eth0. The two static routes are for the 10.10.10.0/24 and 172.16.1.0/24 networks:
>
>     default via 192.168.0.1 dev eth0
>     10.10.10.0/24 via 192.168.0.1 dev eth0
>     172.16.1.0/24 via 192.168.0.1 dev eth0
>
>
> Static routes should only be configured for other subnetworks. The above example is not necessary, since packets going to the 10.10.10.0/24 and 172.16.1.0/24 networks will use the default gateway anyway. Below is an example of setting static routes to a different subnet, on a machine in a 192.168.0.0/24 subnet. The example machine has an **eth0** interface in the 192.168.0.0/24 subnet, and an **eth1** interface (10.10.10.1) in the 10.10.10.0/24 subnet:
>
>     10.10.10.0/24 via 10.10.10.1 dev eth1
>
>
> Specifying an exit interface is optional. It can be useful if you want to force traffic out of a specific interface. For example, in the case of a VPN, you can force traffic to a remote network to pass through a **tun0** interface even when the interface is in a different sub-net to the destination network.

That is most popular way of handling static routes. There is also another method:

> **Network/Netmask Directives Format**
>
> You can also use the network/netmask directives format for **route-interface** files. The following is a template for the network/netmask format, with instructions following afterwards:
>
>     ADDRESS0=X.X.X.X NETMASK0=X.X.X.X GATEWAY0=X.X.X.X
>
>
> *   **ADDRESS0=X.X.X.X** is the network address for the static route.
> *   **NETMASK0=X.X.X.X** is the netmask for the network address defined with **ADDRESS0=X.X.X.X**.
> *   **GATEWAY0=X.X.X.X** is the default gateway, or an IP address that can be used to reach **ADDRESS0=X.X.X.X**
>
> The following is a sample **route-eth0** file using the network/netmask directives format. The default gateway is **192.168.0.1**, interface **eth0**. The two static routes are for the **10.10.10.0/24** and **172.16.1.0/24** networks. However, as mentioned before, this example is not necessary as the **10.10.10.0/24** and **172.16.1.0/24** networks would use the default gateway anyway:
>
>     ADDRESS0=10.10.10.0
>     NETMASK0=255.255.255.0
>     GATEWAY0=192.168.0.1
>     ADDRESS1=172.16.1.0
>     NETMASK1=255.255.255.0
>     GATEWAY1=192.168.0.1
>
>
> Subsequent static routes must be numbered sequentially, and must not skip any values. For example, **ADDRESS0**, **ADDRESS1**, **ADDRESS2**, and so on.

So let's add a static route to the 172.0.0.0/24 network to be accessed via 192.168.2.1 **IP** (in our case via dev **eth1**, since **eth1** has an **IP** which has access to the 192.168.2.0/24 network). First let's do it via **ip route**, and then with the script **/etc/sysconfig/network-scripts/route-eth1** (with the IP Command Arguments Format). Okay let's list all the routes on my machine:

    [root@rhel01 ~]# ip route list
    192.168.2.0/24 dev eth1 proto kernel scope link src 192.168.2.100
    10.131.64.0/20 dev eth0 proto kernel scope link src 10.131.65.22
    default via 10.131.79.254 dev eth0


We can also use the command **route** to show the same thing:

    [root@rhel01 ~]# route -n
    Kernel IP routing table
    Destination Gateway Genmask Flags Metric Ref Use Iface
    192.168.2.0 0.0.0.0 255.255.255.0 U 0 0 0 eth1
    10.131.64.0 0.0.0.0 255.255.240.0 U 0 0 0 eth0
    0.0.0.0 10.131.79.254 0.0.0.0 UG 0 0 0 eth0


So from the above we can just see access to the networks where the interfaces reside and the default gateway which **eth0** has access to. Now to add our desired static route:

    [root@rhel01 ~]# ip route add 172.0.0.0/24 via 192.168.2.1
    [root@rhel01 ~]# ip route list
    172.0.0.0/24 via 192.168.2.1 dev eth1
    192.168.2.0/24 dev eth1 proto kernel scope link src 192.168.2.100
    10.131.64.0/20 dev eth0 proto kernel scope link src 10.131.65.22
    default via 10.131.79.254 dev eth0


and here is the **route** output:

    [root@rhel01 ~]# route -n
    Kernel IP routing table
    Destination Gateway Genmask Flags Metric Ref Use Iface
    172.0.0.0 192.168.2.1 255.255.255.0 UG 0 0 0 eth1
    192.168.2.0 0.0.0.0 255.255.255.0 U 0 0 0 eth1
    10.131.64.0 0.0.0.0 255.255.240.0 U 0 0 0 eth0
    0.0.0.0 10.131.79.254 0.0.0.0 UG 0 0 0 eth0


Now to remove the route:

    [root@rhel01 ~]# ip route del 172.0.0.0/24
    [root@rhel01 ~]# ip route list
    192.168.2.0/24 dev eth1 proto kernel scope link src 192.168.2.100
    10.131.64.0/20 dev eth0 proto kernel scope link src 10.131.65.22
    default via 10.131.79.254 dev eth0


That looks good, now to add a file to make the change persistent:

    [root@rhel01 ~]# touch /etc/sysconfig/network-scripts/route-eth1
    [root@rhel01 ~]# echo "172.0.0.0/16 via 192.168.2.1" > /etc/sysconfig/network-scripts/route-eth1
    [root@rhel01 ~]# cat /etc/sysconfig/network-scripts/route-eth1
    172.0.0.0/16 via 192.168.2.1


That looks good. Now to reset the interface:

    [root@rhel01 ~]# ip route list
    192.168.2.0/24 dev eth1 proto kernel scope link src 192.168.2.100
    10.131.64.0/20 dev eth0 proto kernel scope link src 10.131.65.22
    default via 10.131.79.254 dev eth0
    [root@rhel01 ~]# ifdown eth1
    [root@rhel01 ~]# ifup eth1
    [root@rhel01 ~]# ip route list
    192.168.2.0/24 dev eth1 proto kernel scope link src 192.168.2.100
    10.131.64.0/20 dev eth0 proto kernel scope link src 10.131.65.22
    172.0.0.0/16 via 192.168.2.1 dev eth1
    default via 10.131.79.254 dev eth0


We can now see the route added. The same thing will happen if I reboot the machine.

### DNS configuration

Now let's check out how basic DNS client works in RHEL. From the deployment guide:

> **8.1. Network Configuration Files**
>
> Before delving into the interface configuration files, let us first itemize the primary configuration files used in network configuration. Understanding the role these files play in setting up the network stack can be helpful when customizing a Red Hat Enterprise Linux system.
>
> The primary network configuration files are as follows:
>
> *   **/etc/hosts** - The main purpose of this file is to resolve hostnames that cannot be resolved any other way. It can also be used to resolve hostnames on small networks with no DNS server. Regardless of the type of network the computer is on, this file should contain a line specifying the IP address of the loopback device (127.0.0.1) as localhost.localdomain. For more information, refer to the hosts(5) manual page.
> *   **/etc/resolv.conf** This file specifies the IP addresses of DNS servers and the search domain. Unless configured to do otherwise, the network initialization scripts populate this file. For more information about this file, refer to the resolv.conf(5) manual page

Let's check out the mentioned man pages. Firs the man page for **hosts**:

    HOSTS(5)                   Linux Programmer’s Manual                  HOSTS(5)

    NAME
           hosts - The static table lookup for host names

    SYNOPSIS
           /etc/hosts

    DESCRIPTION
           This manual page describes the format of the /etc/hosts file. This file
           is a simple text file that associates IP addresses with hostnames,  one
           line per IP address. For each host a single line should be present with
           the following information:

                  IP_address canonical_hostname [aliases...]

           Fields of the entry are separated by any number of  blanks  and/or  tab
           characters.  Text  from  a "#" character until the end of the line is a
           comment, and is ignored.  Host  names  may  contain  only  alphanumeric
           characters, minus signs ("-"), and periods (".").  They must begin with
           an  alphabetic  character  and  end  with  an  alphanumeric  character.
           Optional aliases provide for name changes, alternate spellings, shorter
           hostnames, or generic hostnames (for example, localhost).

           The Berkeley Internet Name Domain (BIND) Server implements the Internet
           name  server  for  UNIX systems. It augments or replaces the /etc/hosts
           file or host name lookup, and frees a host from relying  on  /etc/hosts
           being up to date and complete.

           In  modern  systems,  even though the host table has been superseded by
           DNS, it is still widely used for:

           bootstrapping
                  Most systems have a small host table  containing  the  name  and
                  address  information  for  important hosts on the local network.
                  This is useful when DNS is not running, for example during  sys-
                  tem bootup.

           NIS    Sites  that  use NIS use the host table as input to the NIS host
                  database. Even though NIS can be used with DNS, most  NIS  sites
                  still  use the host table with an entry for all local hosts as a
                  backup.

           isolated nodes
                  Very small sites that are isolated from the network use the host
                  table  instead  of DNS. If the local information rarely changes,
                  and the network is not connected to  the  Internet,  DNS  offers
                  little advantage.
    EXAMPLE
            127.0.0.1       localhost
            192.168.1.10    foo.mydomain.org  foo
            192.168.1.13    bar.mydomain.org  bar
            146.82.138.7    master.debian.org      master
            209.237.226.90  www.opensource.org

    NOTE
           Modifications  to this file normally take effect immediately, except in
           cases where the file is cached by applications.

    HISTORICAL NOTES
           RFC 952 gave the original format for the  host  table,  though  it  has
           since changed.

           Before  the advent of DNS, the host table was the only way of resolving
           hostnames on the fledgling Internet. Indeed, this file could be created
           from  the official host data base maintained at the Network Information
           Control Center (NIC), though local changes were often required to bring
           it  up  to date regarding unofficial aliases and/or unknown hosts.  The
           NIC no longer maintains the hosts.txt files, though looking  around  at
           the  time of writing (circa 2000), there are historical hosts.txt files
           on the WWW. I just found three, from 92, 94, and 95.

    FILES
           /etc/hosts


So let’s define a test hostname to have IP **10.10.10.10**. Here is how my **/etc/hosts** file looked like from a basic install:

    [root@rhel01 ~]# cat /etc/hosts
    127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1 localhost localhost.localdomain localhost6 localhost6.localdomain6


Now let's add our test **hostname**:

    [root@rhel01 ~]# echo -e "10.10.10.10\t test.localdomain.com test" >> /etc/hosts
    [root@rhel01 ~]# cat /etc/hosts
    127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
    10.10.10.10  test.localdomain.com test


So let's see what happens we when query that **hostname**:

    [root@rhel01 ~]# getent hosts test
    10.10.10.10 test.localdomain.com test


**Ping** does a similar thing and resolves the **hostname** before pinging:

    [root@rhel01 ~]# ping -c 1 test
    PING test.localdomain.com (10.10.10.10) 56(84) bytes of data.

    --- test.localdomain.com ping statistics ---
    1 packets transmitted, 0 received, 100% packet loss, time 10000ms


Since that **IP** didn't exist we failed to reach it, but we resolved to the correct **IP**. Let's add another entry for our rhel02 lab machine:

    [root@rhel01 ~]# echo "192.168.2.101 rhel02.localdomain.com rhel02 >> /etc/hosts
    [root@rhel01 ~]# ping -c 2 rhel02
    PING rhel02.localdomain.com (192.168.2.101) 56(84) bytes of data.
    64 bytes from rhel02.localdomain.com (192.168.2.101): icmp_seq=1 ttl=64 time=0.561 ms
    64 bytes from rhel02.localdomain.com (192.168.2.101): icmp_seq=2 ttl=64 time=0.978 ms

    --- rhel02.localdomain.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    rtt min/avg/max/mdev = 0.561/0.769/0.978/0.210 ms


That looked good. Now let's check out the **resolv.conf** man page:

    RESOLV.CONF(5)                                                  RESOLV.CONF(5)

    NAME
           resolv.conf - resolver configuration file

    SYNOPSIS
           /etc/resolv.conf

    DESCRIPTION
           The  resolver is a set of routines in the C library that provide access
           to the Internet Domain Name System (DNS).  The  resolver  configuration
           file  contains  information  that  is read by the resolver routines the
           first time they are invoked by a process.  The file is designed  to  be
           human readable and contains a list of keywords with values that provide
           various types of resolver information.

           On a normally configured system this file should not be necessary.  The
           only name server to be queried will be on the local machine; the domain
           name is determined from the host name and the  domain  search  path  is
           constructed from the domain name.

           The different configuration options are:

           nameserver Name server IP address
                  Internet  address  (in  dot  notation) of a name server that the
                  resolver  should  query.   Up  to  MAXNS   (currently   3,   see
                  <resolv.h>)  name  servers  may  be listed, one per keyword.  If
                  there are multiple servers, the resolver library queries them in
                  the  order  listed.   If  no nameserver entries are present, the
                  default is to use the name server on the  local  machine.   (The
                  algorithm  used  is to try a name server, and if the query times
                  out, try the next, until out of name servers, then repeat trying
                  all  the  name  servers  until  a  maximum number of retries are
                  made.)

           domain Local domain name.
                  Most queries for names within this domain can  use  short  names
                  relative  to  the  local domain.  If no domain entry is present,
                  the domain is determined from the local host  name  returned  by
                  gethostname();  the  domain part is taken to be everything after
                  the first ‘.’.  Finally, if the host name  does  not  contain  a
                  domain part, the root domain is assumed.

     search Search list for host-name lookup.
                  The  search  list  is  normally determined from the local domain
                  name; by default, it contains only the local domain name.   This
                  may be changed by listing the desired domain search path follow-
                  ing the search keyword with spaces or tabs separating the names.
                  Resolver  queries having fewer than ndots dots (default is 1) in
                  them will be attempted using each component of the  search  path
                  in  turn until a match is found.  For environments with multiple
                  subdomains please read options ndots:n below  to  avoid  man-in-
                  the-middle  attacks  and  unnecessary  traffic for the root-dns-
                  servers.  Note that this process may be slow and will generate a
                  lot of network traffic if the servers for the listed domains are
                  not local, and that queries will time out if no server is avail-
                  able for one of the domains.

                  The search list is currently limited to six domains with a total
                  of 256 characters.

           sortlist
                  Sortlist  allows  addresses  returned  by  gethostbyname  to  be
                  sorted.   A  sortlist  is specified by IP address netmask pairs.
                  The netmask is optional and defaults to the natural  netmask  of
                  the net. The IP address and optional network pairs are separated
                  by slashes. Up to 10 pairs may be specified. E.g.,
                    sortlist 130.155.160.0/255.255.240.0 130.155.0.0

     options
                  Options allows certain internal resolver variables to  be  modi-
                  fied.  The syntax is

                         options option ...

                  where option is one of the following:

                  debug  sets RES_DEBUG in _res.options.

                  ndots:n
                         sets a threshold for the number of dots which must appear
                         in a name given to res_query() (see  resolver(3))  before
                         an  initial absolute query will be made.  The default for
                         n is ‘‘1’’, meaning that if there are any dots in a name,
                         the  name  will be tried first as an absolute name before
                         any search list elements are appended to it.

                  timeout:n
                         sets the amount of time the  resolver  will  wait  for  a
                         response  from  a  remote name server before retrying the
                         query via a different name server.  Measured in  seconds,
                         the default is RES_TIMEOUT (currently 5, see <resolv.h>).

                  attempts:n
                         sets the number of times the resolver will send  a  query
                         to  its  name  servers  before giving up and returning an
                         error  to  the  calling  application.   The  default   is
                         RES_DFLRETRY (currently 2, see <resolv.h>).

                  rotate sets RES_ROTATE in _res.options, which causes round robin
                         selection of nameservers from among those  listed.   This
                         has  the  effect  of  spreading  the query load among all
                         listed servers, rather than having all  clients  try  the
                         first listed server first every time.

                  no-check-names
                         sets  RES_NOCHECKNAME in _res.options, which disables the
                         modern BIND checking of  incoming  host  names  and  mail
                         names for invalid characters such as underscore (_), non-
                         ASCII, or control characters.

                  inet6  sets RES_USE_INET6 in _res.options.  This has the  effect
                         of trying a AAAA query before an A query inside the geth-
                         ostbyname() function, and of mapping  IPv4  responses  in
                         IPv6  ‘‘tunnelled form’’ if no AAAA records are found but
                         an A record set exists.

           The domain and search keywords are mutually exclusive.   If  more  than
           one instance of these keywords is present, the last instance wins.

           The  search keyword of a system’s resolv.conf file can be overridden on
           a per-process basis by setting the environment variable ‘‘LOCALDOMAIN’’
           to a space-separated list of search domains.

           The  options keyword of a system’s resolv.conf file can be amended on a
           per-process basis by setting the environment  variable  ‘‘RES_OPTIONS’’
           to  a space-separated list of resolver options as explained above under
           options.

           The keyword and value must appear on a single  line,  and  the  keyword
           (e.g.  nameserver) must start the line.  The value follows the keyword,
           separated by white space.

    FILES
           /etc/resolv.conf, <resolv.h>


So here is how my **/etc/resolv.conf** looked like, after a basic install:

    [root@rhel01 ~]# cat /etc/resolv.conf
    [root@rhel01 ~]#


It was empty. So let's define a DNS server which we can send queries to and also define our **search** list to be "localdomain.com":

    [root@rhel01 ~]# echo -e "nameserver\t10.131.23.175\nsearch\tlocaldomain.com" >> /etc/resolv.conf
    [root@rhel01 ~]# cat /etc/resolv.conf
    nameserver  10.131.23.175
    search  localdomain.com


Now let's use **nslookup** to determine the **IP** of a **hostname**. First let's install **nslookup**:

    [root@rhel01 ~]# yum whatprovides "*bin/nslookup"
    Loaded plugins: product-id, subscription-manager
    Updating certificate-based repositories.
    Unable to read consumer identity
    32:bind-utils-9.8.2-0.10.rc1.el6.i686 : Utilities for querying DNS name servers
    Repo : dvd
    Matched from:
    Filename : /usr/bin/nslookup


Now let's install the package:

    [root@rhel01 ~]# yum install bind-utils


Now let's see if we can query the **hostname**:

    [root@rhel01 ~]# nslookup rhel02
    Server:  10.131.23.175
    Address:    10.131.23.175#53

    Non-authoritative answer:
    Name:   rhel02.localdomain.com
    Address: 98.124.198.1


Another cool tool is **host**, it gives you a concise response:

    [root@rhel01 ~]# host rhel02
    rhel02.localdomain.com has address 98.124.198.1


Notice that my DNS server actually has an entry for rhel02 but it's pointing to **IP** 98.124.198.1. Now the important response is from **getent**, in our case we get the following;

    [root@rhel01 ~]# getent hosts rhel02
    192.168.2.101 rhel02.localdomain.com rhel02


If I try to **ssh** by **hostname**, I get the following:

    [root@rhel01 ~]# ssh rhel02
    The authenticity of host 'rhel02 (192.168.2.101)' can't be established.
    RSA key fingerprint is bf:2c:12:8f:b5:fd:f1:15:43:1f:da:20:6d:7c:e5:1f.


Notice that I am going to the 192.168.2.101 **IP**, the one defined in **/etc/hosts** not the one from the DNS query result. So the DNS utilities (**nslookup** and **host**) always check **/etc/resolv.conf** and resolve the **hostname** by querying to the DNS servers. Other utilities (**ping** and **ssh**) actually consult **nsswitch.conf** file to see where to resolve the **hostname** first. The default install has the following line:

    [root@rhel01 ~]# grep ^hosts /etc/nsswitch.conf
    hosts: files dns


So first we check **files** (**/etc/hosts**) and if we can't resolve the **hostname** from there we then query the dns server defined in **/etc/resolv.conf** and use response provided by DNS server. So before any change, I see the following:

    [root@rhel01 ~]# grep ^hosts /etc/nsswitch.conf
    hosts: files dns
    [root@rhel01 ~]# ping -c 1 rhel02
    PING rhel02.localdomain.com (192.168.2.101) 56(84) bytes of data.
    64 bytes from rhel02.localdomain.com (192.168.2.101): icmp_seq=1 ttl=64 time=1.15 ms

    --- rhel02.localdomain.com ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 1ms
    rtt min/avg/max/mdev = 1.158/1.158/1.158/0.000 ms


So I queried **/etc/hosts** and found an **IP** there and then **ping**'ed that **IP**. Now after I made a change:

    [root@rhel01 ~]# grep ^hosts /etc/nsswitch.conf
    hosts: dns files
    [root@rhel01 ~]# ping -c 1 rhel02
    PING rhel02.localdomain.com (98.124.198.1) 56(84) bytes of data.

    --- rhel02.localdomain.com ping statistics ---
    1 packets transmitted, 0 received, 100% packet loss, time 10000ms


So now we queried the DNS server and used that **IP** from that response. Lastly you can check your own hostname, by running **hostname**:

    [root@rhel01 ~]# hostname
    rhel01.localdomain.com


### Network Port Information

Now let's move onto other cool networking utilities that can help troubleshoot networking issues. From "[Red Hat Enterprise Linux 6 Security Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf)"

> **2.2.8. Verifying Which Ports Are Listening**
>
> After configuring network services, it is important to pay attention to which ports are actually listening on the system's network interfaces. Any open ports can be evidence of an intrusion.
>
> There are two basic approaches for listing the ports that are listening on the network. The less reliable approach is to query the network stack using commands such as **netstat -an** or **lsof -i**. This method is less reliable since these programs do not connect to the machine from the network, but rather check to see what is running on the system. For this reason, these applications are frequent targets for replacement by attackers. Crackers attempt to cover their tracks if they open unauthorized network ports by replacing **netstat** and **lsof** with their own, modified versions.
>
> A more reliable way to check which ports are listening on the network is to use a port scanner such as **nmap**. Let's check out how it looks like on my machine:

    [root@rhel01 ~]# netstat -antp
    Active Internet connections (servers and established)
    Proto Recv-Q Send-Q Local Address Foreign Address State PID/Program name
    tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN 1234/sshd
    tcp 0 0 127.0.0.1:25 0.0.0.0:* LISTEN 1311/master
    tcp 0 0 10.131.65.22:22 10.16.186.69:46213 ESTABLISHED 1366/sshd
    tcp 0 0 :::22 :::* LISTEN 1234/sshd
    tcp 0 0 ::1:25 :::* LISTEN 1311/master


Looks like I only have **sshd** and an **smtp** server running. Here is a similar output from **lsof**:

    [root@rhel01 ~]# lsof -i
    COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
    sshd 1234 root 3u IPv4 11045 0t0 TCP *:ssh (LISTEN)
    sshd 1234 root 4u IPv6 11052 0t0 TCP *:ssh (LISTEN)
    master 1311 root 12u IPv4 11245 0t0 TCP localhost:smtp (LISTEN)
    master 1311 root 13u IPv6 11247 0t0 TCP localhost:smtp (LISTEN)
    sshd 1366 root 3r IPv4 11802 0t0 TCP 10.131.65.22:ssh-> 10.16.186.69:46213 (ESTABLISHED)


#### Nmap the Port Scanner

Now let's try the last one, **nmap**:

    [root@rhel01 ~]# yum install -y nmap


Nmap is network scanner so let's run **nmap** against a remote machine, our rhel02 machine:

    [root@rhel01 ~]# nmap -P0 rhel02

    Starting Nmap 5.51 ( http://nmap.org ) at 2013-01-09 19:04 MST
    Nmap scan report for rhel02 (192.168.2.101)
    Host is up (0.00049s latency).
    rDNS record for 192.168.2.101: rhel02.localdomain.com
    Not shown: 999 filtered ports
    PORT STATE SERVICE
    22/tcp open ssh
    MAC Address: 00:50:56:17:1B:A8 (VMware)

    Nmap done: 1 IP address (1 host up) scanned in 5.14 seconds


It looks like we only see one port open on the remote machine, that is probably because there is a firewall and only port 22 is allowed through the firewall. Running it against **localhost**, I saw the following:

    [root@rhel01 ~]# nmap -P0 localhost

    Starting Nmap 5.51 ( http://nmap.org ) at 2013-01-09 19:06 MST
    Nmap scan report for localhost (127.0.0.1)
    Host is up (0.000012s latency).
    Other addresses for localhost (not scanned): 127.0.0.1
    Not shown: 998 closed ports
    PORT STATE SERVICE
    22/tcp open ssh
    25/tcp open smtp

    Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds


### Packet Captures with *tcpdump*

The last tool that I will cover is **tcpdump**. **Tcpdump** allows you to see the traffic sent across an interface. For example let's **ping** rhel01 from rhel02 and see what type of traffic we see. I ran this from rhel02:

    [root@rhel02 ~]# ping -c 2 192.168.2.100
    PING 192.168.2.100 (192.168.2.100) 56(84) bytes of data.
    64 bytes from 192.168.2.100: icmp_seq=1 ttl=64 time=0.474 ms
    64 bytes from 192.168.2.100: icmp_seq=2 ttl=64 time=0.445 ms

    --- 192.168.2.100 ping statistics ---
    2 packets transmitted, 2 received, 0 duplicates, 0% packet loss, time 1000ms
    rtt min/avg/max/mdev = 0.445/0.470/0.493/0.031 ms


and I ran the following on rhel01 at the same time:

    [root@rhel01 ~]# tcpdump -i eth1 host rhel02 and not port ssh
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
    19:09:42.166591 IP rhel02.localdomain.com > 192.168.2.100: ICMP echo request, id 48916, seq 1, length 64
    19:09:42.166626 IP 192.168.2.100 > rhel02.localdomain.com: ICMP echo reply, id 48916, seq 1, length 64
    19:09:42.166685 IP rhel02.localdomain.com > 192.168.2.100: ICMP echo request, id 48916, seq 1, length 64
    19:09:42.166693 IP 192.168.2.100 > rhel02.localdomain.com: ICMP echo reply, id 48916, seq 1, length 64


Notice that I excluded **ssh** traffic. Since I **ssh**'ed from rhel01 to rhel02, **tcpdump** would show the SSH traffic and I didn't want to fill the **tcpdump** output with extra traffic. But from the above output we can see **ICMP** requests and **ICMP** replies. This is what **ping** uses to confirm connectivity between two nodes on a network.

