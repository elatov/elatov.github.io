---
title: Setup Fedora 14 Machine as a Wireless Gateway for an Internal Network
author: Karim Elatov
layout: post
permalink: /2012/10/setup-fedora-14-machine-as-a-wireless-gateway-for-your-internal-network/
dsq_thread_id:
  - 1407265485
categories:
  - Home Lab
  - Networking
  - OS
tags:
  - BCM4321
  - DNAT
  - MASQUERADE NAT
---
First of all, let me explain why I did this. I used to have a basement and in the basement I had a couple of physical machines. I wanted to use these machines as an internal lab, just for some testing. One machine had a wireless card and no physical cable could go down to the basement. So I decided to connect the machine with the wireless card to the wireless router and then connect it's physical ethernet NIC to a switch and have it act a gateway for my internal lab. Here is a good diagram of what the setup looked like:

![wireless_gateway](http://virtuallyhyper.com/wp-content/uploads/2012/09/wireless_gateway.png)

First, I had to make sure my wireless card was working with Fedora. Here is the model of my card:

    moxz:~>lspci | grep -i broad
    00:09.0 Network controller: Broadcom Corporation BCM4321 802.11b/g/n (rev 01)


I actually found an article regarding setting up my card in Fedora. Here is a [link](http://forums.fedoraforum.org/showthread.php?t=239922) to that article. All I had to do is install the following packages:

*   b43-fwcutter
*   kmod-wl
*   broadcom-wl

Here is how I installed them:

    moxz:~> yum install b43-fwcutter kmod-wl broadcom-wl


After the install was done, I had the following packages installed:

    moxz:~>rpm -qa | grep -E 'b43-fw|kmod-wl|com-wl'
    kmod-wl-2.6.35.14-103.fc14.i686-5.100.82.38-1.fc14.10.i686
    b43-fwcutter-013-2.fc14.i686
    broadcom-wl-5.100.82.38-1.fc14.noarch


When I ran **iwconfig**, I saw the following:

    moxz:~>iwconfig
    lo        no wireless extensions.

    eth0      no wireless extensions.

    eth1      IEEE 802.11  Nickname:""
              Access Point: Not-Associated
              Link Quality:5  Signal level:0  Noise level:0
              Rx invalid nwid:0  invalid crypt:0  invalid misc:0


So my card was ready to connect to a wireless network. Since I wanted my wireless card to have a static DHCP IP, I setup the wireless router to assign a static IP to the MAC Address of my Wireless Card. I was using *dd-wrt* and the setup was pretty simple. If you want to see screenshots, check out "[Static DHCP](http://www.dd-wrt.com/wiki/index.php/Static_DHCP)". In my setup, I assigned the IP of "192.168.1.16" to my Wireless adapter.

Next I wanted to make sure I could actually see the wireless network:

    moxz:~> iwlist scanning
    lo        Interface doesn't support scanning.

    eth0      Interface doesn't support scanning.

    eth1      Scan completed :
              Cell 01 - Address: 98:FC:11:86:15:56
                        ESSID:"MY_ESSID"
                        Mode:Managed
                        Frequency:2.437 GHz (Channel 6)
                        Quality:2/5  Signal level:-72 dBm  Noise level:-92 dBm
                        IE: WPA Version 1
                            Group Cipher : TKIP
                            Pairwise Ciphers (1) : TKIP
                            Authentication Suites (1) : PSK
                        Encryption key:on
                        Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 18 Mb/s
                                  24 Mb/s; 36 Mb/s; 54 Mb/s; 6 Mb/s; 9 Mb/s
                                  12 Mb/s; 48 Mb/s


That looked good, because WEP keys are not secure, I use WPA encryption. Since I use WPA, I have to install the **wpa_supplicant** utility to join a wireless access point.

Here is what I did to join to my wireless access point (if you are using WEP, you can follow instructions laid out in [this](http://forums.fedoraforum.org/showthread.php?t=206686) fedora forum )

### 1. Install the Necessary Software

    moxz:~> yum install wpa_supplicant dhclient


### 2. Setup the interface that will be used for the wireless connection with WPA_Supplicant

In order to do that, you need to edit the **/etc/sysconfig/wpa_supplicant** file and setup the appropriate interface. Here is how my config file looked like:

    moxz:~>cat /etc/sysconfig/wpa_supplicant
    # Use the flag "-i" before each of your interfaces, like so:
    #  INTERFACES="-ieth1 -iwlan0"
    INTERFACES="-ieth1"

    # Use the flag "-D" before each driver, like so:
    #  DRIVERS="-Dwext"
    DRIVERS="Dwext"

    # Other arguments
    #   -u   Enable the D-Bus interface (required for use with NetworkManager)
    #   -f   Log to /var/log/wpa_supplicant.log
    #   -P   Write pid file to /var/run/wpa_supplicant.pid
    #        required to return proper codes by init scripts (e.g. double "start" action)
    #        -B to daemonize that has to be used together with -P is already in wpa_supplicant.init.d
    OTHER_ARGS="-u -f /var/log/wpa_supplicant.log -P /var/run/wpa_supplicant.pid"


### 3. Setup your Access Point and WPA password for WPA_Supplicant

To do this, first we need to generate a PSK of your WPA password. This is done like so:

    moxz:~>wpa_passphrase MY_ESSID mypassword
    network={
        ssid="MY_ESSID"
        #psk="mypassword"
        psk=62f1a7e69d04f5c47d8b7ac9384509482a8f94e0fef07ddfc6a2708b13f1dc7c
    }


Next we need to edit the **/etc/wpa_supplicant/wpa_supplicant.conf** file to add the appropriate configurations. Here is how my file looked like:

    moxz:~>cat /etc/wpa_supplicant/wpa_supplicant.conf
    ctrl_interface=/var/run/wpa_supplicant
    ctrl_interface_group=0
    eapol_version=1
    ap_scan=1
    fast_reauth=1
    network={
    # Set scan_ssid=1 if the access point is hidden.
    scan_ssid=0
    proto=WPA RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    group=CCMP TKIP
    ssid="MY_ESSID"
    #psk="mypassword"
    psk=62f1a7e69d04f5c47d8b7ac9384509482a8f94e0fef07ddfc6a2708b13f1dc7c
    }


Lastly, make sure only root can read the file:

    moxz:~>chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf


### 4. Setup the Wireless Interface to obtain it's IP via DCHP

For this we will need to edit the **/etc/sysconfig/network-scripts/ifcfg-eth1** file, here is how my file looks like:

    moxz:~>cat /etc/sysconfig/network-scripts/ifcfg-eth1
    # Please read /usr/share/doc/initscripts-*/sysconfig.txt
    # for the documentation of these parameters.
    DEVICE=eth1
    BOOTPROTO=dhcp
    TYPE=Wireless
    HWADDR=00:18:f8:2b:8a:a9
    ONBOOT=yes
    IPV6INIT=no
    USERCTL=no


### 5. Setup the Appropriate Start-up Services

This one is pretty easy:

    moxz:~> service NetworkManager stop
    moxz:~> chkconfig NetworkManager off
    moxz:~> service wpa_supplicant start
    moxz:~> chkconfig wpa_supplicant on
    moxz:~> service network restart
    moxz:~> chkconfig network on


### 6. Try to connect to the wireless manually

Restart the **wpa_supplicant** service:

    moxz:~>service wpa_supplicant restart
    Stopping wpa_supplicant:                                   [  OK  ]
    Starting wpa_supplicant: /etc/wpa_supplicant/wpa_supplicant[  OK  ]ieth1, Dwext


Grab a DHCP address from the wireless router:

    moxz:~>dhclient eth1


Check to see that you got your static IP:

    moxz:~>ifconfig eth1
    eth1      Link encap:Ethernet  HWaddr 00:18:F8:2B:8A:A9
              inet addr:192.168.1.16  Bcast:192.168.1.255  Mask:255.255.255.0
              inet6 addr: fe80::218:f8ff:fe2b:8aa9/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:34 errors:0 dropped:0 overruns:0 frame:69
              TX packets:25 errors:35 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:5109 (4.9 KiB)  TX bytes:4622 (4.5 KiB)
              Interrupt:17


Check your **wpa_supplicant** logs to make sure it successfully connected:

    moxz:~>tail /var/log/wpa_supplicant.log
    Trying to associate with 98:fc:11:86:15:56 (SSID='MY_ESSID' freq=2437 MHz)
    Associated with 98:fc:11:86:15:56
    WPA: Key negotiation completed with 98:fc:11:86:15:56 [PTK=TKIP GTK=TKIP]
    CTRL-EVENT-CONNECTED - Connection to 98:fc:11:86:15:56 completed (reauth) [id=0 id_str=]


Also the **iwconfig** output should look like this:

    moxz:~>iwconfig eth1
    eth1      IEEE 802.11  ESSID:"MY_ESSID"
              Mode:Managed  Frequency:2.437 GHz  Access Point: 98:FC:11:86:15:56
              Bit Rate=54 Mb/s   Tx-Power=15 dBm
              Retry  long limit:7   RTS thr:off   Fragment thr:off
              Power Management:off
              Link Quality=57/70  Signal level=-53 dBm
              Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
              Tx excessive retries:0  Invalid misc:34   Missed beacon:0


Now reboot the machine and make sure it comes up with your static DHCP IP address. If it doesn't work automatically, the order of **wpa_supplicant** and the **network** service might be off. You can edit your **/etc/rc.local** file to sleep for some time and then run the **dhclient** command from there. Here is a fedora [thread](http://forums.fedoraforum.org/showthread.php?t=235989) that talks about the process.

Next we need our Fedora Machine to act as NAT. When talking about NAT, there are a couple of types. From "[Structure Of Iptables](http://www.iptables.info/en/structure-of-iptables.html)":

> The **DNAT** target is mainly used in cases where you have a public IP and want to redirect accesses to the firewall to some other host (on a DMZ for example). In other words, we change the destination address of the packet and reroute it to the host.
>
> **SNAT** is mainly used for changing the source address of packets. For the most part you'll hide your local networks or DMZ, etc. A very good example would be that of a firewall of which we know outside IP address, but need to substitute our local network's IP numbers with that of our firewall. With this target the firewall will automatically SNAT and De-SNAT the packets, hence making it possible to make connections from the LAN to the Internet. If your network uses 192.168.0.0/netmask for example, the packets would never get back from the Internet, because IANA has regulated these networks (among others) as private and only for use in isolated LANs.
>
> The **MASQUERADE** target is used in exactly the same way as SNAT, but the MASQUERADE target takes a little bit more overhead to compute. The reason for this, is that each time that the MASQUERADE target gets hit by a packet, it automatically checks for the IP address to use, instead of doing as the SNAT target does - just using the single configured IP address. The MASQUERADE target makes it possible to work properly with Dynamic DHCP IP addresses that your ISP might provide for your PPP, PPPoE or SLIP connections to the Internet.

So *SNAT* is a static NAT, where *MASQUERADE* is dynamic NAT. I wasn't sure if I will add more machines to my internal network, but I if I would, I wouldn't want to tinker with my NAT setup. Also I didn't have any public IP addresses, so I decided to set up a MASQUERADE NAT instead of SNAT.

The process is actually pretty easy. From "[Quick-Tip: Linux NAT in Four Steps using iptables](http://www.revsys.com/writings/quicktips/nat.html)" here are the commands that I ran:

    moxz:~> echo 1 > /proc/sys/net/ipv4/ip_forward
    moxz:~> iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
    moxz:~> iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
    moxz:~> iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT


If you wanted the top line to be persistent across reboots, you need to edit the **/etc/sysctl.conf** file, and make sure this line is present:

    net.ipv4.ip_forward = 1


Lastly, I wanted the internal machines to have access to DNS, so I installed **dnsmasq** on the Fedora Machine:

    moxz:~> yum install dnsmasq
    moxz:~> chkconfig dnsmasq on


Under the **/etc/dnsmasq.conf** file, I made the following change:

    # If you want dnsmasq to listen for DHCP and DNS requests only on
    # specified interfaces (and the loopback) give the name of the
    # interface (eg eth0) here.
    # Repeat the line for more than one interface.
    interface=eth0


I also needed to allow DNS queries (UDP 53) to go through my internal interface, so I added the appropriate rule to **iptables**:

    moxz:~>iptables -I INPUT -i eth0 -p udp -m udp --dport 53 -j ACCEPT


I wanted access to some of the machines inside the internal network from the outside, so I ended up using *DNAT* with **iptables** as well. This included a two step process. First enable port forwarding on your wireless router. The process is described in detail in "[Port Forwarding](http://www.dd-wrt.com/wiki/index.php/Port_Forwarding)" (if you are using *dd-wrt*).

For example, let's say that someone connects to port 333 from the outside network to your public IP. You would port-forward port 333 to the Fedora Machine (192.168.1.16) on the same port. When that came to the Fedora Machine you would again port-forward (or DNAT) it to the internal machine on the port of your choice. Here is how the command looked like on the Fedora Machine:

    moxz:~> iptables -I PREROUTING -i eth1 -p tcp -m tcp --dport 333 -j DNAT --to-destination 10.100.10.6:22


Here is a good diagram of traffic flow:

![double_nat](http://virtuallyhyper.com/wp-content/uploads/2012/09/double_nat.png)

Finally I saved the iptables setup:

    moxz:~> service iptables save


In the end, here is how my **iptables** configuration file looked like:

    moxz:~>cat /etc/sysconfig/iptables
    # Generated by iptables-save v1.4.9 on Sat Nov 26 17:08:56 2011
    *nat
    :PREROUTING ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    :POSTROUTING ACCEPT [0:0]
    # If traffic comes to public interface (eth1) on port 333 forward it to IP 10.100.10.6 to port 22
    -A PREROUTING -i eth1 -p tcp -m tcp --dport 333 -j DNAT --to-destination 10.100.10.6:22
    # Setup MASQUERADE NAT, allow internal IPs to be seen as one public IP and go online
    -A POSTROUTING -o eth1 -j MASQUERADE
    COMMIT
    # Completed on Sat Nov 26 17:08:56 2011
    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [169:8796]
    :OUTPUT ACCEPT [3700965:366350266]
    # Allow already established connections
    -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
    # Allow pings
    -A INPUT -p icmp -j ACCEPT
    # Allow anything on the local interface
    -A INPUT -i lo -j ACCEPT
    # Allow ssh access to the Fedora Machine
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
    # Allow DNS queries to the Fedora Machine
    -A INPUT -i eth0 -p udp -m udp --dport 53 -j ACCEPT
    # Block the rest
    -A INPUT -j REJECT --reject-with icmp-host-prohibited
    # If already established allow to go through our MASQUERADE NAT
    -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    # allow anything from the internal interface (eth0) to the external interface (eth1)
    -A FORWARD -i eth0 -o eth1 -j ACCEPT
    COMMIT


The setup worked out quite well for my needs.

