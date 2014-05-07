---
title: Connecting to an OpenVPN Server with Various Clients
author: Karim Elatov
layout: post
permalink: /2013/09/onnecting-to-an-openvpn-server-with-various-clients/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1706299869
categories:
  - Home Lab
  - Networking
tags:
  - Network Manager
  - OpenVPN
  - Tunnelblick
---
## OpenVPN

From their <a href="http://openvpn.net/index.php/open-source/documentation/howto.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://openvpn.net/index.php/open-source/documentation/howto.html']);">how-to</a>:

> OpenVPN is a full-featured SSL VPN which implements OSI layer 2 or 3 secure network extension using the industry standard SSL/TLS protocol, supports flexible client authentication methods based on certificates, smart cards, and/or username/password credentials, and allows user or group-specific access control policies using firewall rules applied to the VPN virtual interface.

### OpenVPN Server

On the Server side we generate the necessary certificates and create a Public Key Infrastructure (PKI). From the same <a href="http://openvpn.net/index.php/open-source/documentation/howto.html#pki" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://openvpn.net/index.php/open-source/documentation/howto.html#pki']);">how-to</a>:

> The first step in building an OpenVPN 2.x configuration is to establish a PKI (public key infrastructure). The PKI consists of:
> 
> *   a separate certificate (also known as a public key) and private key for the server and each client, and
> *   a master Certificate Authority (CA) certificate and key which is used to sign each of the server and client certificates.
> 
> OpenVPN supports bidirectional authentication based on certificates, meaning that the client must authenticate the server certificate and the server must authenticate the client certificate before mutual trust is established.
> 
> Both server and client will authenticate the other by first verifying that the presented certificate was signed by the master certificate authority (CA), and then by testing information in the now-authenticated certificate header, such as the certificate common name or certificate type (client or server).

To setup an OpenVPN server here is a pretty good summary of the configuration:

1.  Generate the master Certificate Authority (CA) certificate & key
    
         rsync -avzP /usr/share/doc/openvpn-*/easy-rsa /etc/openvpn/.
         cd /etc/openvpn/easy-rsa
         vi vars
         . ./vars
         ./clean-all
         ./build-ca
        
    
    *   NOTE: When editing the **vars** file, set the *KEY_COUNTRY*, *KEY_PROVINCE*, *KEY_CITY*, *KEY_ORG*, and *KEY_EMAIL* parameters

2.  Generate certificate & key for server
    
         ./build-key-server server
        

3.  Generate certificates & keys for clients
    
         ./build-key client1
        

4.  Generate Diffie Hellman parameters
    
         ./build-dh
        

5.  Creating configuration files for server and clients
    
         cp /usr/share/doc/openvpn-*/sample-config-files/server.conf /etc/openvpn/.
         vi /etc/openvpn/server.conf
        

6.  Editing the client configuration files
    
         cp /usr/share/doc/openvpn-*/sample-config-files/client.conf /etc/openvpn/client1.conf
         vi /etc/openvpn/client1.conf
        

7.  Start the OpenVPN server
    
         cd /etc/openvpn
         openvpn server.conf
        

After it&#8217;s all done, we should have the following certificates:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_certs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_certs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_certs.png" alt="openvpn certs Connecting to an OpenVPN Server with Various Clients" width="492" height="242" class="alignnone size-full wp-image-9386" title="Connecting to an OpenVPN Server with Various Clients" /></a>

If you need more specifics on the OpenVPN Server configuration, check out the following sites (there is a lot of other functionality included):

*   <a href="http://openvpn.net/index.php/open-source/documentation/howto.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://openvpn.net/index.php/open-source/documentation/howto.html']);">OpenVPN How-To</a>
*   <a href="https://wiki.archlinux.org/index.php/OpenVPN" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.archlinux.org/index.php/OpenVPN']);">ArchLinux OpenVPN</a>
*   <a href="http://www.techrepublic.com/blog/linux-and-open-source/how-to-set-up-an-openvpn-server/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.techrepublic.com/blog/linux-and-open-source/how-to-set-up-an-openvpn-server/']);">How to set up an OpenVPN server</a>

BTW there is a very interesting article on the differences between **IPsec** and **OpenVPN**: It&#8217;s called &#8220;<a href="http://www.packtpub.com/article/networking-with-openvpn" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.packtpub.com/article/networking-with-openvpn']);">Networking with OpenVPN</a>&#8220;. From that article here is an intriguing comparison:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/ipsec-vs-openvpn.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/ipsec-vs-openvpn.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/ipsec-vs-openvpn.png" alt="ipsec vs openvpn Connecting to an OpenVPN Server with Various Clients" width="564" height="661" class="alignnone size-full wp-image-9385" title="Connecting to an OpenVPN Server with Various Clients" /></a>

### OpenVPN Client

For the client side it&#8217;s pretty easy. Given the configuration files, we just need to start the OpenVPN tunnel. From the OpenVPN <a href="http://openvpn.net/index.php/open-source/documentation/howto.html#start" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://openvpn.net/index.php/open-source/documentation/howto.html#start']);">How-To</a>:

Starting the client

> As in the server configuration, it&#8217;s best to initially start the OpenVPN server from the command line (or on Windows, by right-clicking on the client.ovpn file), rather than start it as a daemon or service:
> 
> `openvpn [client config file]`

Our IT Administrator gave a zip archive will all the necessary files:

    $ unzip -l client.zip
    Archive:  client.zip
      Length      Date    Time    Name
    ---------  ---------- -----   ----
         1314  2013-03-18 15:58   ca.crt
         3947  2013-03-18 15:58   client1.crt
          733  2013-03-18 15:58   client1.csr
          887  2013-03-18 15:58   client1.key
         3479  2013-03-18 15:58   client1.conf
         3479  2013-03-18 15:58   client1.ovpn
    ---------                     -------
        13839                     6 files
    

the **client1.conf** is for linux and **client1.ovpn** is for windows. The contain the exact same information:

    $ diff client1.ovpn client1.conf
    $
    

Here is how the config looks like:

    $ grep -vE '^$|^;|^#' client1.conf
    client
    dev tun
    proto udp
    remote vpn1.server.com 1194
    remote vpn2.server.com 1194
    remote-random
    resolv-retry infinite
    nobind
    persist-key
    persist-tun
    mute-replay-warnings
    ca ca.crt
    cert client1.crt
    key client1.key
    ns-cert-type server
    comp-lzo
    verb 3
    mute 20
    

Pretty standard config, the top line says that this is for the **client**. We will create a **tun**nel **dev**ice, it will probably end up being **tun0**. We define the appropriate certificates: **ca**, **cert**, **key** (all of which reside in the same directory as the config file). We have a list of OpenVPN servers to connect to, these are defined by the **remote** directive (we also choose one at random: **remote-random**). And we will use the standard OpenVPN **proto**col UDP with port 1194.

## Starting the OpenVPN Tunnel

Now that everything is in place, let&#8217;s start the tunnel:

    $ cd vpn
    $ sudo openvpn client1.conf
    ...
    ...
    Mon Sep  2 12:25:05 2013 [vpn.server.com] Peer Connection Initiated with [AF_INET]1.2.3.4:1194
    Mon Sep  2 12:25:07 2013 SENT CONTROL [vpn1.server.com]: 'PUSH_REQUEST' (status=1)
    Mon Sep  2 12:25:07 2013 PUSH: Received control message: 'PUSH_REPLY,route 10.2.0.0 255.255.0.0,dhcp-option DOMAIN vpn.server.com,dhcp-option DNS 10.1.0.5,topology net,ping 10,ping-restart 120,ifconfig 10.1.0.3 10.1.0.2'
    ..
    ..
    Mon Sep  2 12:25:07 2013 /sbin/route add -net 10.2.0.0 netmask 255.255.0.0 gw 10.1.0.2
    Mon Sep  2 12:25:07 2013 Initialization Sequence Completed
    

So we can see that our OpenVPN server is **1.2.3.4**. Here are the settings we received from that server:

    route 10.2.0.0 255.255.0.0
    

add access to the **10.2.0.0/16** network.

    dhcp-option DOMAIN vpn.server.com
    

set the DNS search suffix to be **vpn.server.com**.

    dhcp-option DNS 10.1.0.5
    

set the nameserver to **10.1.0.5**

    ifconfig 10.1.0.3 10.1.0.2
    

establish a peer-to-peer tunnel with each endpoints using a **10.1.0.2** and **10.1.0.3** addresses.

### Confirm OpenVPN settings

We saw all the setting fly by the screen, now let&#8217;s make sure all the networking is configured. First let&#8217;s make sure we have **tun0** interface with appropriate settings:

    $ ip -4 a show tun0
    9: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN qlen 100
        inet 10.1.0.3 peer 10.1.0.2/32 scope global tun0
    

So our **tun0** interface has a **10.1.0.3** address and it&#8217;s peer (the OpenVPN server) is **10.1.0.2**. The latter will be used as the gateway for the network that we are trying to reach. So now checking out the routing table:

    $ip route ls | grep tun0
    10.1.0.2 dev tun0  proto kernel  scope link  src 10.1.0.3
    10.2.0.0/16 via 10.1.0.2 dev tun0
    

We can see that to reach the **10.2.0.0/16** network we will go through the **10.1.0.2** address via the **tun0** interface. Lastly we can check out the DNS settings:

    $ cat /etc/resolv.conf
    # Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
    #     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
    nameserver 127.0.1.1
    nameserver 8.8.8.8
    

As you can see the settings were not applied.

### Stop the OpenVPN Tunnel

At this point I went back to the terminal which had my OpenVPN tunnel open and I clicked &#8220;Cntr-C&#8221; to stop the tunnel. Here is how it looked like:

    Mon Sep  2 12:25:07 2013 Initialization Sequence Completed
    ^CMon Sep  2 12:58:08 2013 event_wait : Interrupted system call (code=4)
    Mon Sep  2 12:58:08 2013 TCP/UDP: Closing socket
    Mon Sep  2 12:58:08 2013 /sbin/route del -net 10.2.0.0 netmask 255.255.0.0
    Mon Sep  2 12:58:08 2013 Closing TUN/TAP interface
    Mon Sep  2 12:58:08 2013 /sbin/ifconfig tun0 0.0.0.0
    Mon Sep  2 12:58:08 2013 SIGINT[hard,] received, process exiting
    

### Configure OpenVPN Client to Apply DNS Settings Pushed from the OpenVPN Server

I actually ran into <a href="https://bugs.launchpad.net/ubuntu/+source/openvpn/+bug/691723" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bugs.launchpad.net/ubuntu/+source/openvpn/+bug/691723']);">OpenVPN Client Ignores DNS</a> (it&#8217;s an Ubuntu Bug Report), which talks about using the **update-resolv-conf** script to apply the DNS settings. I saw the same description in the Arch Linux <a href="https://wiki.archlinux.org/index.php/OpenVPN#DNS" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.archlinux.org/index.php/OpenVPN#DNS']);">page</a>. So I added the following into my **client1.conf** file:

    $tail -4 client1.conf
    # Pull DNS
    script-security 2
    up /etc/openvpn/update-resolv-conf
    down /etc/openvpn/update-resolv-conf
    

Then starting up the client again, I saw the following:

    $ sudo openvpn client1.conf
    ...
    ...
    Mon Sep  2 13:02:10 2013 /sbin/ifconfig tun0 10.1.0.3 pointopoint 10.1.0.2 mtu 1500
    Mon Sep  2 13:02:10 2013 /etc/openvpn/update-resolv-conf tun0 1500 1542 10.1.0.3 10.1.0.2 init
    dhcp-option DOMAIN vpn.server.com
    dhcp-option DNS 10.1.0.5
    

Then checking my **/etc/resolv.conf** file, I saw the following:

    $cat /etc/resolv.conf
    # Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
    #     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
    nameserver 10.1.0.5
    nameserver 127.0.1.1
    search vpn.server.com
    nameserver 8.8.8.8  
    

Upon closing the OpenVPN tunnel those settings were reverted.

### Use Network Manager to Establish the OpenVPN Tunnel

Network Manager has a openvpn plugin. Here is what I saw on my Ubuntu laptop:

    $apt-cache search network-manager openvpn
    network-manager-openvpn - network management framework (OpenVPN plugin core)
    network-manager-openvpn-gnome - network management framework (OpenVPN plugin GNOME GUI)
    

So I went ahead and installed the plugin:

    $ sudo apt-get install network-manager-openvpn
    

You can then launch the nm-connection-editor, like so:

    $nm-connection-editor
    

you should see the following window show up:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-editor.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-editor.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-editor.png" alt="nm editor Connecting to an OpenVPN Server with Various Clients" width="395" height="321" class="alignnone size-full wp-image-9394" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Then click &#8220;Add&#8221; and you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/add-connection-nm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/add-connection-nm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/add-connection-nm.png" alt="add connection nm Connecting to an OpenVPN Server with Various Clients" width="630" height="265" class="alignnone size-full wp-image-9395" title="Connecting to an OpenVPN Server with Various Clients" /></a>

From the Connection Type list, select &#8220;Import a Saved VPN Configuration&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/choose_import_saved.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/choose_import_saved.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/choose_import_saved.png" alt="choose import saved Connecting to an OpenVPN Server with Various Clients" width="625" height="555" class="alignnone size-full wp-image-9397" title="Connecting to an OpenVPN Server with Various Clients" /></a>

After it&#8217;s selected, click on &#8220;Create&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/import_saved.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/import_saved.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/import_saved.png" alt="import saved Connecting to an OpenVPN Server with Various Clients" width="640" height="251" class="alignnone size-full wp-image-9398" title="Connecting to an OpenVPN Server with Various Clients" /></a>

and it will ask you to point to the configuration file. Let&#8217;s point to the **client1.conf** file from our OpenVPN configurations:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/file_to_import_nm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/file_to_import_nm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/file_to_import_nm.png" alt="file to import nm Connecting to an OpenVPN Server with Various Clients" width="780" height="585" class="alignnone size-full wp-image-9399" title="Connecting to an OpenVPN Server with Various Clients" /></a>

After it&#8217;s imported you should see something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/client1_imported-nm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/client1_imported-nm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/client1_imported-nm.png" alt="client1 imported nm Connecting to an OpenVPN Server with Various Clients" width="636" height="596" class="alignnone size-full wp-image-9400" title="Connecting to an OpenVPN Server with Various Clients" /></a>

For some reason, my Network Manager didn&#8217;t import the multiple OpenVPN servers, so let&#8217;s change the Name of the VPN connection and add the other OpenVPN server to the list:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_settings_two_servers.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_settings_two_servers.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_settings_two_servers.png" alt="vpn settings two servers Connecting to an OpenVPN Server with Various Clients" width="636" height="596" class="alignnone size-full wp-image-9401" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Lastly click on Advanced and enable the &#8220;Randomize Random Hosts&#8221; option:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_advanced.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_advanced.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_advanced.png" alt="openvpn advanced Connecting to an OpenVPN Server with Various Clients" width="551" height="403" class="alignnone size-full wp-image-9402" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Click &#8220;Save&#8221; and you should be all set.

### Connect to the OpenVPN Tunnel with Network Manager

If you are using Gnome, the Network Manager Applet should be automatically running. It looks something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-applet_running.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-applet_running.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-applet_running.png" alt="nm applet running Connecting to an OpenVPN Server with Various Clients" width="34" height="25" class="alignnone size-full wp-image-9403" title="Connecting to an OpenVPN Server with Various Clients" /></a>

If you don&#8217;t see that in your notification bar, then you can launch the Network Manager applet, by running the following from the command line:

    $ nm-applet
    

Once you have located the Network Manager Applet, click on it and select your VPN tunnel:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/select_vpn_connection_nm-applet.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/select_vpn_connection_nm-applet.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/select_vpn_connection_nm-applet.png" alt="select vpn connection nm applet Connecting to an OpenVPN Server with Various Clients" width="462" height="136" class="alignnone size-full wp-image-9404" title="Connecting to an OpenVPN Server with Various Clients" /></a>

After the VPN is established you will see the following message on your screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_connection_successful.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_connection_successful.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_connection_successful.png" alt="vpn connection successful Connecting to an OpenVPN Server with Various Clients" width="339" height="84" class="alignnone size-full wp-image-9405" title="Connecting to an OpenVPN Server with Various Clients" /></a>

You will also see a small lock next to your connection in the Network Manager applet:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_conn_successful_nm-applet.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_conn_successful_nm-applet.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_conn_successful_nm-applet.png" alt="vpn conn successful nm applet Connecting to an OpenVPN Server with Various Clients" width="33" height="24" class="alignnone size-full wp-image-9406" title="Connecting to an OpenVPN Server with Various Clients" /></a>

You can actually do the same thing via the command line. Network Manager provides a cli tool, it&#8217;s called **nmcli**. After we have added the VPN Connection we can check that it exists:

    $nmcli connection list | grep vpn
    NAME      UUID                                   TYPE   TIMESTAMP-REAL
    VPN       9524ca67-db91-4777-a28b-d909c4243315   vpn    Thu 27 Jun 2013 09:25:17 AM MDT
    

We can get all the configuration of the Connection as well, by specifying its name (in my case it&#8217;s called &#8220;VPN&#8221;):

    $nmcli connection list id VPN
    connection.id:                          VPN
    connection.uuid:                        9524ca67-db91-4777-a28b-d909c4243315
    connection.type:                        vpn
    connection.autoconnect:                 yes
    connection.timestamp:                   1378154582
    connection.read-only:                   no
    connection.permissions:
    connection.zone:                        --
    connection.master:                      --
    connection.slave-type:                  --
    connection.secondaries:
    ipv4.method:                            auto
    ipv4.dns:
    ipv4.dns-search:                        
    ipv4.addresses:
    ipv4.routes:
    ipv4.ignore-auto-routes:                no
    ipv4.ignore-auto-dns:                   no
    ipv4.dhcp-client-id:                    --
    ipv4.dhcp-send-hostname:                yes
    ipv4.dhcp-hostname:                     --
    ipv4.never-default:                     no
    ipv4.may-fail:                          yes
    vpn.service-type:                       org.freedesktop.NetworkManager.openvpn
    vpn.user-name:                          --
    vpn.data:                               key = /home/elatov/vpn/client1.key, cert = /home/elatov/vpn/client1.crt, ca = /home/elatov/vpn/ca.crt, cert-pass-flags = 0, comp-lzo = yes, remote = vpn1.server.com,vpn2.server.com, connection-type = tls, remote-random = yes
    vpn.secrets:
    

We can also check the status of the connection:

    $nmcli connection status id VPN
    Error: 'VPN' is not an active connection.
    

So currently is not connected. Now let&#8217;s go ahead and establish our OpenVPN Tunnel:

    $nmcli connection up id VPN
    $
    

Now checking the status of the connection we should see it active:

    $nmcli connection status id VPN
    GENERAL.NAME:                           VPN
    GENERAL.UUID:                           9524ca67-db91-4777-a28b-d909c4243315
    GENERAL.DEVICES:                        mlan0
    GENERAL.STATE:                          activated
    GENERAL.DEFAULT:                        yes
    GENERAL.DEFAULT6:                       no
    GENERAL.VPN:                            yes
    GENERAL.ZONE:                           --
    GENERAL.DBUS-PATH:                      /org/freedesktop/NetworkManager/ActiveConnection/7
    GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/Settings/8
    GENERAL.SPEC-OBJECT:                    /org/freedesktop/NetworkManager/ActiveConnection/0
    GENERAL.MASTER-PATH:                    /org/freedesktop/NetworkManager/Devices/0
    ...
    ...
    VPN.TYPE:                               openvpn
    VPN.USERNAME:                           --
    VPN.GATEWAY:                            vpn1.server.com,vpn2.server.com
    VPN.BANNER:
    VPN.VPN-STATE:                          5 - VPN connected
    VPN.CFG[1]:                             key = /home/elatov/vpn/client1.key
    VPN.CFG[2]:                             cert = /home/elatov/vpn/client1.crt
    VPN.CFG[3]:                             ca = /home/elatov/vpn/ca.crt
    VPN.CFG[4]:                             cert-pass-flags = 0
    VPN.CFG[5]:                             comp-lzo = yes
    VPN.CFG[6]:                             remote = vpn1.server.com,vpn2.server.com
    VPN.CFG[7]:                             connection-type = tls
    VPN.CFG[8]:                             remote-random = yes
    

In the logs (on my Ubuntu laptop, this was under **/var/log/syslog**) we will also see the following:

    Sep  2 14:46:20 crbook NetworkManager[831]: <info>   Static Route: 10.2.0.0/16   Next Hop: 10.1.0.2
    Sep  2 14:46:20 crbook NetworkManager[831]: <info>   Forbid Default Route: no
    Sep  2 14:46:20 crbook NetworkManager[831]: <info>   Internal DNS: 10.1.0.5
    Sep  2 14:46:20 crbook NetworkManager[831]: <info>   DNS Domain: 'vpn.server.com'
    Sep  2 14:46:20 crbook NetworkManager[831]: <info> No IPv6 configuration
    Sep  2 14:46:20 crbook nm-openvpn[16480]: Initialization Sequence Completed
    Sep  2 14:46:21 crbook NetworkManager[831]: <info> VPN connection 'VPN' (IP Config Get) complete.
    Sep  2 14:46:21 crbook NetworkManager[831]: <info> Policy set 'VPN' (tun0) as default for IPv4 routing and DNS.
    Sep  2 14:46:21 crbook NetworkManager[831]: <info> Writing DNS information to /sbin/resolvconf
    Sep  2 14:46:21 crbook dnsmasq[1335]: setting upstream servers from DBus
    Sep  2 14:46:21 crbook dnsmasq[1335]: using nameserver 10.1.0.5#53
    Sep  2 14:46:21 crbook dbus[275]: [system] Activating service name='org.freedesktop.nm_dispatcher' (using servicehelper)
    Sep  2 14:46:21 crbook NetworkManager[831]: <info> VPN plugin state changed: started (4)
    Sep  2 14:46:22 crbook dbus[275]: [system] Successfully activated service 'org.freedesktop.nm_dispatcher'
    

We can see the static routes getting added and the DNS information was added as well. Network Manager handled the **dhcp-option** (sent from the OpenVPN Server) settings without the need of any extra hooks, which is awesome. I even removed the lines that I added to make it work from the command line and it still worked fine. You can stop the VPN tunnel by running the following:

    $nmcli connection down id VPN
    

## OpenVPN Client for Mac OS X

For Mac OS there is a client called Tunnelblick and it can be downloaded from <a href="https://code.google.com/p/tunnelblick/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://code.google.com/p/tunnelblick/']);">here</a>. After you have downloaded and install it, it should be in your Applications folder. Go to your Applications folder (Command-Shift-A) and locate the App:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-icon.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-icon.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-icon.png" alt="tunnelblick icon Connecting to an OpenVPN Server with Various Clients" width="171" height="62" class="alignnone size-full wp-image-9414" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Launch the App by double clicking on it or pressing *Command-O*. When it launches you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-starting.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-starting.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-starting.png" alt="tunnelblick starting Connecting to an OpenVPN Server with Various Clients" width="383" height="186" class="alignnone size-full wp-image-9415" title="Connecting to an OpenVPN Server with Various Clients" /></a>

After it&#8217;s finished with the initialization process, you will see the welcome screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-welcome_screen.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-welcome_screen.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-welcome_screen.png" alt="tnblk welcome screen Connecting to an OpenVPN Server with Various Clients" width="823" height="415" class="alignnone size-full wp-image-9416" title="Connecting to an OpenVPN Server with Various Clients" /></a>

From here we can click on &#8220;I have Configuration Files&#8221; and then you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-what-type-of-configs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-what-type-of-configs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-what-type-of-configs.png" alt="tnblk what type of configs Connecting to an OpenVPN Server with Various Clients" width="823" height="359" class="alignnone size-full wp-image-9417" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Here we can choose &#8220;OpenVPN Configurations&#8221;. Then we will see the following instructions:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-instructions.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-instructions.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-instructions.png" alt="tnblk instructions Connecting to an OpenVPN Server with Various Clients" width="534" height="572" class="alignnone size-full wp-image-9418" title="Connecting to an OpenVPN Server with Various Clients" /></a>

and back in Finder you will see the Empty Folder. So go ahead and place the certificate and configuration files into that folder:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn-config-in-folder.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn-config-in-folder.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn-config-in-folder.png" alt="openvpn config in folder Connecting to an OpenVPN Server with Various Clients" width="629" height="188" class="alignnone size-full wp-image-9419" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Then close the folder,click on the folder, and press &#8220;Command-I&#8221; or right click on the folder to select &#8220;Get Info&#8221;. At which point you will see the information regarding that folder:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/folder_information.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/folder_information.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/folder_information.png" alt="folder information Connecting to an OpenVPN Server with Various Clients" width="379" height="910" class="alignnone size-full wp-image-9420" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Rename the folder with a **.tblk** extension (in my case I called it VPN.tblk). Upon saving the configuration, you will see the following dialogue:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/change-extension_of_folder.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/change-extension_of_folder.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/change-extension_of_folder.png" alt="change extension of folder Connecting to an OpenVPN Server with Various Clients" width="534" height="273" class="alignnone size-full wp-image-9421" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Click &#8220;add&#8221; and you should see the following on your desktop:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn-tblk-icon.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn-tblk-icon.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn-tblk-icon.png" alt="vpn tblk icon Connecting to an OpenVPN Server with Various Clients" width="89" height="102" class="alignnone size-full wp-image-9422" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Double click on icon and the import process should start and you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tlblk-only_for-user.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tlblk-only_for-user.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tlblk-only_for-user.png" alt="tlblk only for user Connecting to an OpenVPN Server with Various Clients" width="564" height="289" class="alignnone size-full wp-image-9423" title="Connecting to an OpenVPN Server with Various Clients" /></a>

Since the certificates are specific to me, I selected &#8220;Only me&#8221; and then I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tb-config_installed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tb-config_installed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tb-config_installed.png" alt="tb config installed Connecting to an OpenVPN Server with Various Clients" width="534" height="272" class="alignnone size-full wp-image-9424" title="Connecting to an OpenVPN Server with Various Clients" /></a>

At this point you can connect on the OpenVPN Tunnel by click on the TunnelBlick Icon from the notification area and selecting the VPN that you want to connect to:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-connection-to-tunnel.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-connection-to-tunnel.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-connection-to-tunnel.png" alt="tnblk connection to tunnel Connecting to an OpenVPN Server with Various Clients" width="200" height="160" class="alignnone size-full wp-image-9425" title="Connecting to an OpenVPN Server with Various Clients" /></a>

After clicking on that you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnlk-authorizing.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tnlk-authorizing.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tnlk-authorizing.png" alt="tnlk authorizing Connecting to an OpenVPN Server with Various Clients" width="248" height="192" class="alignnone size-full wp-image-9426" title="Connecting to an OpenVPN Server with Various Clients" /></a>

and then after the connection is successful you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-connected.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-connected.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-connected.png" alt="tunblk connected Connecting to an OpenVPN Server with Various Clients" width="250" height="187" class="alignnone size-full wp-image-9428" title="Connecting to an OpenVPN Server with Various Clients" /></a>

To disconnect you can go back to the TunnelBlick icon and select the VPN to disconnect:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblik-disconnect.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblik-disconnect.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblik-disconnect.png" alt="tunblik disconnect Connecting to an OpenVPN Server with Various Clients" width="191" height="161" class="alignnone size-full wp-image-9427" title="Connecting to an OpenVPN Server with Various Clients" /></a>

and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-disconnected.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-disconnected.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-disconnected.png" alt="tunblk disconnected Connecting to an OpenVPN Server with Various Clients" width="250" height="182" class="alignnone size-full wp-image-9429" title="Connecting to an OpenVPN Server with Various Clients" /></a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/09/onnecting-to-an-openvpn-server-with-various-clients/" title=" Connecting to an OpenVPN Server with Various Clients" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Network Manager,OpenVPN,Tunnelblick,blog;button:compact;">OpenVPN From their how-to: OpenVPN is a full-featured SSL VPN which implements OSI layer 2 or 3 secure network extension using the industry standard SSL/TLS protocol, supports flexible client authentication...</a>
</p>