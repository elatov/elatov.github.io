---
title: 'Connecting to a VM using &#8220;Serial Port Over the Network&#8221; With a Moxa Device Server'
author: Karim Elatov
layout: post
permalink: /2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/
dsq_thread_id:
  - 1405544653
categories:
  - Networking
  - OS
  - VMware
tags:
  - Moxa
  - netcat
  - Virtual Serial Port
---
Before we get into how to set this up, let&#8217;s get a good diagram going to better understand how all the components work. Here is what I came up with:

<a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vm_serial_connection_over_network/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vm_serial_connection_over_network/']);" rel="attachment wp-att-5447"><img class="alignnone size-full wp-image-5447" alt="VM Serial Connection Over Network Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/VM_Serial_Connection_Over_Network.jpg" width="937" height="339" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a>

So to configure this from the VM, we can follow instructions laid out in &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-virtual-machine-admin-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-virtual-machine-admin-guide.pdf']);">vSphere Virtual Machine Administration ESXi 5.0</a>&#8220;. From that document:

> **Using Serial Ports with vSphere Virtual Machines**  
> You can set up virtual serial ports connections for vSphere virtual machines in several ways. The connection method that you select depends on the task that you need to accomplish.
> 
> You can set up virtual serial ports to send data in the following ways.
> 
> <a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vserial_port_configuration/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vserial_port_configuration/']);" rel="attachment wp-att-5448"><img class="alignnone size-full wp-image-5448" alt="vserial port configuration Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vserial_port_configuration.png" width="601" height="342" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a>

Then from the same document:

> **Change the Serial Port Configuration in the vSphere Web Client**  
> A virtual machine can use up to four virtual serial ports. You can connect the virtual serial port to a physical serial port or to a file on the host computer. You can also use a host-side named pipe to set up a direct connection between two virtual machines or a connection between a virtual machine and an application on the host computer. In addition, you can use a port or vSPC URI to connect a serial port over the network. Virtual machines can be in a powered-on state during configuration.
> 
> **Procedure**
> 
> 1.  Select a virtual machine. 
> 2.  In the VM Hardware panel, click Edit Settings. 
> 3.  Click Virtual Hardware. 
> 4.  Click the triangle next to the serial port to expand the serial port options. 
> 5.  (Optional) Change the Device status settings.<a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vserial_connected_box/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vserial_connected_box/']);" rel="attachment wp-att-5450"><img class="alignnone size-full wp-image-5450" alt="vserial connected box Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vserial_connected_box.png" width="584" height="98" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a> 
> 6.  Select a connection type.<a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/options_for_serial_port/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/options_for_serial_port/']);" rel="attachment wp-att-5451"><img class="alignnone size-full wp-image-5451" alt="options for serial port Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/options_for_serial_port.png" width="581" height="371" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a> 
> 7.  (Optional) Select Yield on poll. Select this option only for guest operating systems that use serial ports in polled mode. This option prevents the guest from consuming excessive CPUs. 
> 8.  Click OK.
> 
> **Example: Establishing Serial Port Network Connections to a Client or Server**  
> If you do not use vSPC and you configure your virtual machine with a serial port connected as a server with a **telnet://:12345** URI, you can connect to your virtual machine&#8217;s serial port from your Linux or Windows operating system.
> 
>     telnet yourESXiServerIPAddress 12345 
>     
> 
> Similarly, if you run the Telnet Server on your Linux system on port 23 (**telnet://yourLinuxBox:23**), you configure the virtual machine as a client URI.
> 
>     telnet://yourLinuxBox:23 
>     
> 
> The virtual machine initiates the connection to your Linux system on port 23.

From Moxa&#8217;s &#8220;<a href="http://www.moxa.com/resource_file/2036200811171320.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.moxa.com/resource_file/2036200811171320.pdf']);">TCP Server Mode for NPort</a>&#8221; document:

> What is TCP Server Mode?  
> In TCP Server mode, the serial port on the NPort is assigned a port number which must not conflict with any other serial port on the NPort. The host computer initiates contact with the NPort, establishes the connection, and receives data from the serial device. This operation mode also supports up to 8 simultaneous connections, enabling multiple hosts to collect data from the same serial device at the same time. The whole system should connect like this: <a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/moxa_tcp_server_mode/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/moxa_tcp_server_mode/']);" rel="attachment wp-att-5452"><img class="alignnone size-full wp-image-5452" alt="moxa tcp server mode Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/moxa_tcp_server_mode.png" width="556" height="114" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a>

And here is how the actual configuration of the Moxa device is:

> **Configuring the NPort 5000, NPort W2150, and NPort W2250 for TCP Server Mode**  
> Before performing the following steps, restore the NPort device server&#8217;s default settings by holding the reset button down for 10 seconds.
> 
> 1.  Turn the NPort on. The Ready LED should turn green. 
> 2.  Make sure that the NPort and the host PC are properly connected to the network. 
> 3.  Adjust the NPort&#8217;s IP settings as necessary so that it is in the same network as your PC. You may also need to modify the host PC&#8217;s IP configuration. Make sure you can ping the NPort from your host PC.Remember, the IP addresses of the NPort and the PC must be on the same subnet. If one IP address is modified, you may need to modify the other IP address. 
> 4.  On the host PC, connect to the NPort&#8217;s Telnet console by entering telnet *nport&#8217;s* IP address at the command prompt. For example, if your NPort&#8217;s IP address is 192.168.127.254, enter **telnet 192.168.127.254** at the command prompt. 
> 5.  In the Telnet console under (4) Operating Settings, select the serial port that you wish to configure. 
> 6.  Select (1) Operating mode and (2) TCP Server Mode. 
> 7.  Select (a) to assign a local TCP listening port (4001 by default) and (b) to assign a command port (966 by default). 
> 8.  In the main menu under (3) Serial settings, select the serial port that you wish to configure. Adjust the communication parameters as necessary for your serial device, such as 115200, N, 8, 1. 
> 9.  In the main menu, select (s) Save/Restart to restart the NPort with the new settings activated.

So we are going to use the &#8220;Port URI&#8221; since we are not using a vSPC (ie Avocent ACS v6000 Virtual Serial Port Concentrator). More information on that can be seen in VMware KB <a href="http://kb.vmware.com/kb/1022303" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1022303']);">1022303</a>. And as per the Moxa documentation the port that I need to connect to is **4001** . Here is how my VM looked like after the configuration was done:

<a href="http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vm_serial_port_conf/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/connecting-to-a-vm-using-serial-port-over-the-network-with-moxa-device-server/vm_serial_port_conf/']);" rel="attachment wp-att-5453"><img class="alignnone size-full wp-image-5453" alt="vm serial port conf Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vm_serial_port_conf.png" width="696" height="615" title="Connecting to a VM using Serial Port Over the Network With a Moxa Device Server" /></a>

Here is last note from the vSphere documentation:

> **Adding a Firewall Rule Set for Serial Port Network Connections**  
> If you add or configure a serial port that is backed by a remote network connection, ESXi firewall settings can prevent transmissions. Before you connect network-backed virtual serial ports, you must add one of the following firewall rule sets to prevent the firewall from blocking communication:
> 
> *   VM serial port connected to vSPC. Use to connect the serial port output through a network with the Use virtual serial port concentrator option enabled to allow only outgoing communication from the host.
> *   VM serial port connected over network. Use to connect the serial port output through a network without the virtual serial port concentrator. 

Here is where things get interesting. The way that the Virtual Serial Port Connects to our Remote Server is via our management vmkernel interface. The Virtual Serial Port connects to the VMkernel, this then forwards the traffic to the management vmkernel interface (vmk0). The vmk0 is usually bound to a physical nic and which then forwards the connection to a Serial Port Concentrator. Once the connection is established we can use it to remotely manage a VM over the Serial Connection over the network. So there are a lot of layers to setup but it actually works. This is very similar to KVM-over-IP like <a href="http://www.raritan.com/products/kvm-over-ip/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.raritan.com/products/kvm-over-ip/']);">Raritan</a>.

Getting back to our ESXi host, I checked the firewall rules and initially the &#8220;**RemoteSerialPort**&#8221; rule was disabled:

    ~ # esxcli network firewall ruleset list -r remoteSerialPort
    Name              Enabled
    ----------------  -------
    remoteSerialPort    false 
    

And of course the firewall was enabled:

    ~ # esxcli network firewall get
       Default Action: DROP
       Enabled: true
       Loaded: true 
    

Now checking the actual firewall rule we see the following:

    ~ # esxcli network firewall ruleset rule list -r remoteSerialPort
    Ruleset           Direction  Protocol  Port Type  Port Begin  Port End
    ----------------  ---------  --------  ---------  ----------  --------
    remoteSerialPort  Outbound   TCP       Dst                 0     65535
    remoteSerialPort  Inbound    TCP       Dst                23        23
    remoteSerialPort  Inbound    TCP       Dst              1024     65535
    

So the rule allows the host to connect to ports **0-65535** in the outbound direction. I am guessing most of the virtual serial port concentrators don&#8217;t have a defined port, so VMware opens them all up. As long as it&#8217;s not all inbound ports, then that is okay. I enabled that rule and refreshed the firewall:

    ~ # esxcli network firewall ruleset set -r remoteSerialPort -e true
    ~ # esxcli network firewall ruleset list -r remoteSerialPort
    Name              Enabled
    ----------------  -------
    remoteSerialPort     true
    ~ # esxcli network firewall refresh
    

But I could not connect to the VM over the Virtual Serial Port. At this point I downloaded &#8216;netcat&#8217; for windows from <a href="http://joncraton.org/media/files/nc111nt.zip" onclick="javascript:_gaq.push(['_trackEvent','download','http://joncraton.org/media/files/nc111nt.zip']);">here</a>. I then launched it to listen on port **4001**, like so (this was done on my vCenter machine):

    C:\Users\Administrator\Desktop\nc111nt>nc -l -p 4001
    

And confirming that it&#8217;s in listening state:

    C:\Users\Administrator>netstat -an | findstr 4001
      TCP    0.0.0.0:4001           0.0.0.0:0              LISTENING 
    

Now when I manually tried to connect to that port from the ESXi host to my vCenter machine:

    ~ # nc -z 192.168.0.121 4001
    ~ # 
    

But the connection was unsuccessful. I wanted to see if the firewall was causing the issue so I turned it off completely and then tried again:

    ~ # esxcli network firewall set -e false
    ~ # nc -z 192.168.0.121 4001
    Connection to 192.168.0.121 4001 port [tcp/*] succeeded! 
    

It actually worked. Doing a packet capture when the firewall was off, I saw the following:

    ~ # tcpdump-uw -i vmk0 tcp port 4001 -n
    tcpdump-uw: WARNING: SIOCGIFINDEX: Invalid argument
    tcpdump-uw: verbose output suppressed, use -v or -vv for full protocol decode
    listening on vmk0, link-type EN10MB (Ethernet), capture size 96 bytes
    04:03:26.974476 IP 192.168.0.103.60337 > 192.168.0.121.4001: Flags [S], seq 2797491653, win 65535, options [mss 1460,nop,wscale 9,sackOK,TS val 45368682 ecr 0], length 0
    04:03:26.975500 IP 192.168.0.121.4001 > 192.168.0.103.60337: Flags [S.], seq 3292624631, ack 2797491654, win 8192, options [mss 1460,nop,wscale 8,sackOK,TS val 579956405 ecr 45368682], length 0
    04:03:26.975581 IP 192.168.0.103.60337 > 192.168.0.121.4001: Flags [.], ack 1, win 130, options [nop,nop,TS val 45368683 ecr 579956405], length 0
    04:03:26.977645 IP 192.168.0.103.60337 > 192.168.0.121.4001: Flags [F.], seq 1, ack 1, win 130, options [nop,nop,TS val 45368683 ecr 579956405], length 0
    04:03:26.978327 IP 192.168.0.121.4001 > 192.168.0.103.60337: Flags [.], ack 2, win 260, options [nop,nop,TS val 579956406 ecr 45368683], length 0
    04:03:26.978775 IP 192.168.0.121.4001 > 192.168.0.103.60337: Flags [F.], seq 1, ack 2, win 260, options [nop,nop,TS val 579956406 ecr 45368683], length 0
    04:03:26.978826 IP 192.168.0.103.60337 > 192.168.0.121.4001: Flags [.], ack 2, win 130, options [nop,nop,TS val 45368683 ecr 579956406], length 0
    tcpdump-uw: pcap_loop: recvfrom: Interrupted system call
    7 packets captured
    7 packets received by filter
    0 packets dropped by kernel
    

As soon as I turned the firewall on, even with the ruled enabled, I saw the following:

    ~ # tcpdump-uw -i vmk0 tcp port 4001 -n
    tcpdump-uw: WARNING: SIOCGIFINDEX: Invalid argument
    tcpdump-uw: verbose output suppressed, use -v or -vv for full protocol decode
    listening on vmk0, link-type EN10MB (Ethernet), capture size 96 bytes
    04:05:16.739780 IP 192.168.0.103.55167 > 192.168.0.121.4001: Flags [S], seq 2864827401, win 65535, options [mss 1460,nop,wscale 9,sackOK,TS val 45379659 ecr 0], length 0
    04:05:19.745044 IP 192.168.0.103.55167 > 192.168.0.121.4001: Flags [S], seq 2864827401, win 65535, options [mss 1460,nop,wscale 9,sackOK,TS val 45379960 ecr 0], length 0
    04:05:22.955083 IP 192.168.0.103.55167 > 192.168.0.121.4001: Flags [S], seq 2864827401, win 65535, options [mss 1460,nop,wscale 9,sackOK,TS val 45380281 ecr 0], length 0
    04:05:26.165015 IP 192.168.0.103.55167 > 192.168.0.121.4001: Flags [S], seq 2864827401, win 65535, options [mss 1460,sackOK,eol], length 0
    04:05:29.375102 IP 192.168.0.103.55167 > 192.168.0.121.4001: Flags [S], seq 2864827401, win 65535, options [mss 1460,sackOK,eol], length 0
    tcpdump-uw: pcap_loop: recvfrom: Interrupted system call
    5 packets captured
    5 packets received by filter
    0 packets dropped by kernel
    

So the traffic was leaving the **vmk0** interface but it wasn&#8217;t going anywhere. Doing the **nc** connection and checking out the drops at the firewall level, I saw the following; First I started the **nc** connection and left that running, I then ran the query command from another ssh connection:

    ~ # date; nc -z 192.168.0.121 4001
    Sat Dec 22 04:10:44 UTC 2012 
    

Then from the other connection:

    ~ # for i in `seq 1 3`; do date; vsish -e cat /vmkModules/esxfw/filters/vmk0/filterproperties; sleep 3; done
    Sat Dec 22 04:10:45 UTC 2012
    ESXFW filter properties {
       Port ID:16777219
       Filtering enabled?:1
       pkts passed:46274
       pkts dropped:199 < ====
       pkts rejected:0
    }
    Sat Dec 22 04:10:48 UTC 2012
    ESXFW filter properties {
       Port ID:16777219
       Filtering enabled?:1
       pkts passed:46282
       pkts dropped:200 <===
       pkts rejected:0
    }
    Sat Dec 22 04:10:51 UTC 2012
    ESXFW filter properties {
       Port ID:16777219
       Filtering enabled?:1
       pkts passed:46289
       pkts dropped:201 <====
       pkts rejected:0
    }
    

We can clearly see an increase in dropped packets as we try to connect out with our **nc** command. I then followed the instruction laid out in VMware KB <a href="http://kb.vmware.com/kb/2008226" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2008226']);">2008226</a> to add a new rule to just allow outbound traffic to destination port 4001. First let&#8217;s see the last rule in our firewall ruleset:

    /etc/vmware/firewall # tail -14 service.xml 
    <!-- netDump -->
    <service id="0032"> 
    <id>netDump</id> 
    <rule id='0000'> 
    <direction>outbound</direction> 
    <protocol>udp</protocol> 
    <porttype>dst</porttype> 
    <port>6500</port> 
    </rule> 
    <enabled>true</enabled> 
    <required>false</required> 
    </service> 
    

So my last rule is **32**. Now let&#8217;s setup the file to be edited:

    /etc/vmware/firewall # chmod u+w service.xml 
    /etc/vmware/firewall # chmod +t service.xml 
    

I then started editing the file with vi, like so:

    /etc/vmware/firewall # vi service.xml
    

and I added the following into the file, before the line that had &#8220;**ConfigRoot**&#8220;:

    <service id='0033'> 
    <id>moxa</id> 
    <rule id='0000'> 
    <direction>inbound</direction> 
    <protocol>tcp</protocol> 
    <porttype>dst</porttype> 
    <port>4001</port> 
    </rule> 
    <enabled>false</enabled> 
    <required>false</required> 
    </service> 
    

Here is how it looked like in the end:

    /etc/vmware/firewall # tail -13 service.xml
      <service id='0033'>
        <id>Moxa</id>
        <rule id='0000'>
          <direction>outbound</direction>
          <protocol>tcp</protocol>
          <porttype>dst</porttype>
          <port>4001</port>
        </rule>
        <enabled>false</enabled>
        <required>false</required>
      </service>
    

Now reloading the firewall rules:

    ~ # esxcli network firewall refresh 
    

Now looking for our new rule, I see the following:

    ~ # esxcli network firewall ruleset list -r moxa
    Name  Enabled
    ----  -------
    moxa    false
    

Now checking the contents of the rule I saw the following:

    ~ # esxcli network firewall ruleset rule list -r moxa
    Ruleset  Direction  Protocol  Port Type  Port Begin  Port End
    -------  ---------  --------  ---------  ----------  --------
    moxa     Outbound   TCP       Dst              4001      4001
    

That all looked good, I then enabled the rule:

    ~ # esxcli network firewall ruleset set -r moxa -e true
    

Then trying to connect port **4001** from the host:

    ~ # nc -z 192.168.0.121 4001
    Connection to 192.168.0.121 4001 port [tcp/*] succeeded!
    

and voila, it worked. For some reason port ranges for out going traffic didn&#8217;t work. I was using the following version of ESXi:

    ~ # vmware -lv
    VMware ESXi 5.0.0 build-623860
    VMware ESXi 5.0.0 Update 1
    

I then stood up a test 5.1 ESXi host:

    ~ # vmware -lv
    VMware ESXi 5.1.0 build-799733
    VMware ESXi 5.1.0 GA
    

I then checked for the same **remoteSerialPort** rule:

    ~ # esxcli network firewall ruleset list -r remoteSerialPort
    Name              Enabled
    ----------------  -------
    remoteSerialPort    false
    

And the contents looked the same:

    ~ # esxcli network firewall ruleset rule list -r remoteSerialPort
    Ruleset           Direction  Protocol  Port Type  Port Begin  Port End
    ----------------  ---------  --------  ---------  ----------  --------
    remoteSerialPort  Outbound   TCP       Dst                 0     65535
    remoteSerialPort  Inbound    TCP       Dst                23        23
    remoteSerialPort  Inbound    TCP       Dst              1024     65535
    

I then enabled that rule:

    ~ # esxcli network firewall ruleset set -r remoteSerialPort -e true
    

then trying my **nc** connection:

    ~ # nc -z 192.168.0.121 4001
    Connection to 192.168.0.121 4001 port [tcp/*] succeeded! 
    

It worked without any custom firewall rules. Must be a bug in ESXi 5.0u1, but I am glad that it&#8217;s fixed in ESXi 5.1GA. After I added the custom rule to my 5.0 install I was able to connect to my VM over the Moxa device.

