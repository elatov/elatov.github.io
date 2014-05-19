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

From their [how-to](http://openvpn.net/index.php/open-source/documentation/howto.html):

> OpenVPN is a full-featured SSL VPN which implements OSI layer 2 or 3 secure network extension using the industry standard SSL/TLS protocol, supports flexible client authentication methods based on certificates, smart cards, and/or username/password credentials, and allows user or group-specific access control policies using firewall rules applied to the VPN virtual interface.

### OpenVPN Server

On the Server side we generate the necessary certificates and create a Public Key Infrastructure (PKI). From the same [how-to](http://openvpn.net/index.php/open-source/documentation/howto.html#pki):

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


After it's all done, we should have the following certificates:

![openvpn certs Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_certs.png)

If you need more specifics on the OpenVPN Server configuration, check out the following sites (there is a lot of other functionality included):

*   [OpenVPN How-To](http://openvpn.net/index.php/open-source/documentation/howto.html)
*   [ArchLinux OpenVPN](https://wiki.archlinux.org/index.php/OpenVPN)
*   [How to set up an OpenVPN server](http://www.techrepublic.com/blog/linux-and-open-source/how-to-set-up-an-openvpn-server/)

BTW there is a very interesting article on the differences between **IPsec** and **OpenVPN**: It's called "[Networking with OpenVPN](http://www.packtpub.com/article/networking-with-openvpn)". From that article here is an intriguing comparison:

![ipsec vs openvpn Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/ipsec-vs-openvpn.png)

### OpenVPN Client

For the client side it's pretty easy. Given the configuration files, we just need to start the OpenVPN tunnel. From the OpenVPN [How-To](http://openvpn.net/index.php/open-source/documentation/howto.html#start):

Starting the client

> As in the server configuration, it's best to initially start the OpenVPN server from the command line (or on Windows, by right-clicking on the client.ovpn file), rather than start it as a daemon or service:
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

Now that everything is in place, let's start the tunnel:

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

We saw all the setting fly by the screen, now let's make sure all the networking is configured. First let's make sure we have **tun0** interface with appropriate settings:

    $ ip -4 a show tun0
    9: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN qlen 100
        inet 10.1.0.3 peer 10.1.0.2/32 scope global tun0


So our **tun0** interface has a **10.1.0.3** address and it's peer (the OpenVPN server) is **10.1.0.2**. The latter will be used as the gateway for the network that we are trying to reach. So now checking out the routing table:

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

At this point I went back to the terminal which had my OpenVPN tunnel open and I clicked "Cntr-C" to stop the tunnel. Here is how it looked like:

    Mon Sep  2 12:25:07 2013 Initialization Sequence Completed
    ^CMon Sep  2 12:58:08 2013 event_wait : Interrupted system call (code=4)
    Mon Sep  2 12:58:08 2013 TCP/UDP: Closing socket
    Mon Sep  2 12:58:08 2013 /sbin/route del -net 10.2.0.0 netmask 255.255.0.0
    Mon Sep  2 12:58:08 2013 Closing TUN/TAP interface
    Mon Sep  2 12:58:08 2013 /sbin/ifconfig tun0 0.0.0.0
    Mon Sep  2 12:58:08 2013 SIGINT[hard,] received, process exiting


### Configure OpenVPN Client to Apply DNS Settings Pushed from the OpenVPN Server

I actually ran into [page](https://bugs.launchpad.net/ubuntu/+source/openvpn/+bug/691723). So I added the following into my **client1.conf** file:

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

![nm editor Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-editor.png)

Then click "Add" and you should see the following:

![add connection nm Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/add-connection-nm.png)

From the Connection Type list, select "Import a Saved VPN Configuration":

![choose import saved Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/choose_import_saved.png)

After it's selected, click on "Create":

![import saved Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/import_saved.png)

and it will ask you to point to the configuration file. Let's point to the **client1.conf** file from our OpenVPN configurations:

![file to import nm Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/file_to_import_nm.png)

After it's imported you should see something like this:

![client1 imported nm Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/client1_imported-nm.png)

For some reason, my Network Manager didn't import the multiple OpenVPN servers, so let's change the Name of the VPN connection and add the other OpenVPN server to the list:

![vpn settings two servers Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_settings_two_servers.png)

Lastly click on Advanced and enable the "Randomize Random Hosts" option:

![openvpn advanced Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn_advanced.png)

Click "Save" and you should be all set.

### Connect to the OpenVPN Tunnel with Network Manager

If you are using Gnome, the Network Manager Applet should be automatically running. It looks something like this:

![nm applet running Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/nm-applet_running.png)

If you don't see that in your notification bar, then you can launch the Network Manager applet, by running the following from the command line:

    $ nm-applet


Once you have located the Network Manager Applet, click on it and select your VPN tunnel:

![select vpn connection nm applet Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/select_vpn_connection_nm-applet.png)

After the VPN is established you will see the following message on your screen:

![vpn connection successful Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_connection_successful.png)

You will also see a small lock next to your connection in the Network Manager applet:

![vpn conn successful nm applet Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn_conn_successful_nm-applet.png)

You can actually do the same thing via the command line. Network Manager provides a cli tool, it's called **nmcli**. After we have added the VPN Connection we can check that it exists:

    $nmcli connection list | grep vpn
    NAME      UUID                                   TYPE   TIMESTAMP-REAL
    VPN       9524ca67-db91-4777-a28b-d909c4243315   vpn    Thu 27 Jun 2013 09:25:17 AM MDT


We can get all the configuration of the Connection as well, by specifying its name (in my case it's called "VPN"):

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


So currently is not connected. Now let's go ahead and establish our OpenVPN Tunnel:

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

For Mac OS there is a client called Tunnelblick and it can be downloaded from [here](https://code.google.com/p/tunnelblick/). After you have downloaded and install it, it should be in your Applications folder. Go to your Applications folder (Command-Shift-A) and locate the App:

![tunnelblick icon Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-icon.png)

Launch the App by double clicking on it or pressing *Command-O*. When it launches you will see the following:

![tunnelblick starting Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tunnelblick-starting.png)

After it's finished with the initialization process, you will see the welcome screen:

![tnblk welcome screen Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-welcome_screen.png)

From here we can click on "I have Configuration Files" and then you will see the following:

![tnblk what type of configs Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-what-type-of-configs.png)

Here we can choose "OpenVPN Configurations". Then we will see the following instructions:

![tnblk instructions Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-instructions.png)

and back in Finder you will see the Empty Folder. So go ahead and place the certificate and configuration files into that folder:

![openvpn config in folder Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/openvpn-config-in-folder.png)

Then close the folder,click on the folder, and press "Command-I" or right click on the folder to select "Get Info". At which point you will see the information regarding that folder:

![folder information Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/folder_information.png)

Rename the folder with a **.tblk** extension (in my case I called it VPN.tblk). Upon saving the configuration, you will see the following dialogue:

![change extension of folder Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/change-extension_of_folder.png)

Click "add" and you should see the following on your desktop:

![vpn tblk icon Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/vpn-tblk-icon.png)

Double click on icon and the import process should start and you should see the following:

![tlblk only for user Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tlblk-only_for-user.png)

Since the certificates are specific to me, I selected "Only me" and then I saw the following:

![tb config installed Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tb-config_installed.png)

At this point you can connect on the OpenVPN Tunnel by click on the TunnelBlick Icon from the notification area and selecting the VPN that you want to connect to:

![tnblk connection to tunnel Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tnblk-connection-to-tunnel.png)

After clicking on that you will see the following:

![tnlk authorizing Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tnlk-authorizing.png)

and then after the connection is successful you will see the following:

![tunblk connected Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-connected.png)

To disconnect you can go back to the TunnelBlick icon and select the VPN to disconnect:

![tunblik disconnect Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblik-disconnect.png)

and you will see the following:

![tunblk disconnected Connecting to an OpenVPN Server with Various Clients](http://virtuallyhyper.com/wp-content/uploads/2013/09/tunblk-disconnected.png)

