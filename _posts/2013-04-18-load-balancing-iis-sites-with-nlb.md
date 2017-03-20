---
title: Load Balancing IIS Sites with NLB
author: Karim Elatov
layout: post
permalink: /2013/04/load-balancing-iis-sites-with-nlb/
dsq_thread_id:
  - 1405433067
categories: ['os', 'home_lab', 'networking']
tags: ['win2k8r2','windows_nlb', 'iis']
---

Here is quick diagram of what I was trying to achieve:

![NLB IIS Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/NLB_IIS.jpg)

**IIS-1**

*   Primary/cluster interface: 192.168.250.47
*   Secondary Interface: 192.168.250.48

**IIS-2**

*   Primary/Cluster Interface: 192.168.250.49
*   Secondary Interface: 192.168.250.50

**Cluster**

*   Virtual IP: 192.168.250.51

I setup both of the IIS Servers in same manner as I described in [this](/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture) post. Since both of the IIS Servers were VMs running on KVM, I was able to easily add a secondary network interfaces to both VMs and ensure that they are on the same network. I will be using NLB in *Unicast* mode and that is why two interfaces is necessary (I will talk more about that later).

Just for reference here is the IP configuration for IIS-1 :

    C:\Users\Administrator>ipconfig
    Windows IP Configuration

    Ethernet adapter Local Area Connection 2:

       Connection-specific DNS Suffix  . :
       IPv4 Address. . . . . . . . . . . : 192.168.250.48
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . :

    Ethernet adapter Local Area Connection:

       Connection-specific DNS Suffix  . :
       IPv4 Address. . . . . . . . . . . : 192.168.250.47
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.250.1


Here is the IP configuration for IIS-2:

    C:\Users\administrator>ipconfig
    Windows IP Configuration

    Ethernet adapter Local Area Connection 2:

       Connection-specific DNS Suffix  . :
       IPv4 Address. . . . . . . . . . . : 192.168.250.50
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . :

    Ethernet adapter Local Area Connection:

       Connection-specific DNS Suffix  . :
       IPv4 Address. . . . . . . . . . . : 192.168.250.49
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.250.1


The secondary interface will be used to ensure the cluster nodes can talk to each other. Lastly make sure they can ping each other over the both IPs:

    C:\Users\administrator>ping 192.168.250.47 -n 1

    Pinging 192.168.250.47 with 32 bytes of data:
    Reply from 192.168.250.47: bytes=32 time=2ms TTL=128

    Ping statistics for 192.168.250.47:
        Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
    Approximate round trip times in milli-seconds:
        Minimum = 2ms, Maximum = 2ms, Average = 2ms

    C:\Users\administrator>ping 192.168.250.48 -n 1

    Pinging 192.168.250.48 with 32 bytes of data:
    Reply from 192.168.250.48: bytes=32 time=1ms TTL=128

    Ping statistics for 192.168.250.48:
        Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
    Approximate round trip times in milli-seconds:
        Minimum = 1ms, Maximum = 1ms, Average = 1ms


### Install Network Load Balancing Services

On the first IIS Server start the Server Manager by running:

    servermanager.msc


Then go to "Features" -> "Add Features". From the list select "Network Load Balancing":

![server manager NLB selected Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/server_manager_NLB_selected.png)

Click "Next", "Install", and let the install go through.

### Configure Network Load Balancing Services

Once NLB is installed on both IIS Servers, go to first IIS server (iis-1) and run

    nlbmgr


That will launch the "Network Load Balancing Manager":

![nlbmgr started Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr-started.png)

Then from the Menu Bar go to "Cluster" -> "New":

![nlb mgr cluster new g Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlb_mgr_cluster_new_g.png)

In the "New Cluster" wizard enter the first IIS Server's hostname (in my case it was 'iis-1') for the host field and click on "Connect". After you hit connect it will connect to the IIS server and provide a list of available interfaces on the Web Server. Choose the primary interface (192.168.250.47):

![nlbmgr ints from host Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr-ints-from-host.png)

After you click "Next" you will see the "Host Parameters" window, you can leave all the default options here:

![nlbmgr host params Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_host_params.png)

Click "Next" and it will take you to the "Cluster IP Addresses" screen:

![nlbmgr cluster ips Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr-cluster-ips.png)

From here click "Add" and enter the IP that will be used as the "Cluster" IP address. In my case it was 192.168.250.51:

![nlbmgr add ip ad Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_add_ip-ad.png)

Click "OK", then click "Next", and you will get to the "Cluster Parameters" page. On this screen fill in the "Full Internet Name" of the cluster (cluster.elatov.local) and leave the Operation Mode in **Unicast** (any mode will work as long as the cluster can converge).

If you select *Multicast* mode your upstream switch will have to support multicast. *Unicast* doesn't require any configuration on the upstream switch but does require two Network Interfaces. The reason for this has to do with how NLB operates. When the primary Network Interfaces are setup to be part of an NLB cluster they actually won't be able to talk to each other with those interfaces. So we need a second interface on a network that has access to the primary network (the easiest way to accomplish that is put it on the same subnet). More information regarding the Cluster operation modes can be seen in [this](http://technet.microsoft.com/en-us/library/bb742455.aspx) Microsoft article, from that article:

> Network Load Balancing's unicast mode has the side effect of disabling communication between cluster hosts using the cluster adapters. Since outgoing packets for another cluster host are sent to the same MAC address as the sender, these packets are looped back within the sender by the network stack and never reach the wire. This limitation can be avoided by adding a second network adapter card to each cluster host. In this configuration, Network Load Balancing is bound to the network adapter on the subnet that receives incoming client requests, and the other adapter is typically placed on a separate, local subnet for communication between cluster hosts and with back-end file and database servers. Network Load Balancing only uses the cluster adapter for its heartbeat and remote control traffic.

Here is how my "Cluster Parameters" screen looked like:

![nlbmgr clus params filled out Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_clus_params_filled_out.png)

After you click "Next" you will see the "Port Rules" screen:

![nlbmgr port rules Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_port_rules.png)

If you click "Edit" it will show you the default rule set:

![nlbmgr edit port rule Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_edit_port_rule.png)

By default it's setup to load balance all the ports "0-65535" and that will work for our setup. If you wanted to be pedantic you could create one rule to only balance port 80, but the default is okay. Now the *Affinity* setting is noteworthy, cause it basically decides how the load balancing occurs. [This](http://technet.microsoft.com/en-us/library/cc778263%28v=ws.10%29.aspx) Microsoft article explains the different modes, here are the important excerpts:

> *   The **None** option specifies that multiple connections from the same client IP address can be handled by different cluster hosts (no client affinity). In order to allow Network Load Balancing to properly handle IP fragments, you should avoid using None when selecting UDP or Both for your protocol setting.
> *   The **Single** option specifies that Network Load Balancing should direct multiple requests from the same client IP address to the same cluster host. This is the default setting for affinity.
> *   **Class C** affinity specifies that Network Load Balancing direct multiple requests from the same TCP/IP Class C address range to the same cluster host.

Both of the IIS Servers weren't using any sessions so the *Affinity* didn't really matter in my setup, so I left the default "Single" option. At this point we are ready to click "Finish" and as soon as we do we will see the first Node getting added to the cluster. If it's successful we will see the following:

![nlbmgr node1 added Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_node1_added.png)

Now to add the second node. Right click on the cluster and select "Add Host To Cluster":

![nlbmgr add host to cluster g Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_add_host_to_cluster_g.png)

In the host field enter the hostname of the second IIS server (iis-2) and click connect. If the connection is successful you will see a list of Interfaces on that Web Server:

![nlbmgr interface second node Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_interface_second_node.png)

Select the Primary Interface and click "Next" and you will be taken to the "Host Parameters" screen:

![nlbmgr host params2 Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_host_params2.png)

Leave the defaults and click "Next". You will then be taken to the same "Port Rules" screen. Click Edit and make sure "Single" mode is selected for the *Affinity* setting:

![nlbmgr edit rule node2 Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_edit_rule_node2.png)

All of the above looks correct and we can hit "OK" to go to the previous window and then click "Finish" to add the Node to the cluster. You will see the node converging and if all goes well you will see both nodes converged:

![nlbmgr converged node2 Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_converged_node2.png)

### Windows 2003 Weak Host Receive and Send Models(Optional)

If the conversion fails we will need to enable weak host receive and send options on our secondary interface. Most of the information can be seen in [this](https://kb.vmware.com/kb/1556) VMware KB. Basically we will have to run the following on both IIS Servers:

    netsh interface ipv4 set interface "Local Area Connection 2" weakhostreceive=enable
    netsh interface ipv4 set interface "Local Area Connection 2" weakhostsend=enable


More information regarding Windows Weak Host Receive and Send can be found in [this](http://technet.microsoft.com/en-us/magazine/2007.09.cableguy.aspx) Microsoft article.

### Testing NLB

Add an **A** record in your DNS Server for your cluster IP to be the hostname (cluster.elatov.local) that we chose and make sure it resolves fine from the client:

    C:\Users\elatov>nslookup cluster
    Server:  UnKnown
    Address:  192.168.250.47

    Name:    cluster.elatov.local
    Address:  192.168.250.51


To test it out, create a test file under **c:\inetpub\wwwroot\test.html** on IIS-1 and place the following contents into the file:

> This is IIS-1

On the IIS-2 create the same file (**c:\inetpub\wwwroot\test.html**) with the following contents:

> This is IIS-2

Now from the client machine in the Browser go to **http://cluster/test.html**. At this point one of the nodes will be picked and you will see this:

![chrome test IIS 1 Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/chrome_test_IIS-1.png)

Since we chose "Single" for our Affinity mode, if you go to page again, it will take you to the same IIS server. So let's go ahead and stop the node that we are currently going to. As you can see in my case that is IIS-2. So from IIS-1, launch the "Network Load Balancing Manager" by running:

    nlbmgr


From the NLB Manager right click on our node and go to "Control Host" -> "Stop":

![nlbmgr stop host Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_stop_host.png)

If the process is successful you will see the node in a "Red" state:

![nlbmgr 2nd node stopped Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/nlbmgr_2nd_node_stopped.png)

Now from the client go to the same page (**http://cluster/test.html**) and you should see the following:

![chrome test IIS2 Load Balancing IIS Sites with NLB](https://github.com/elatov/uploads/raw/master/2013/04/chrome_test_IIS2.png)

Now we know NLB is working properly, go back to the NLB Manager and start the node back up.

