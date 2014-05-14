---
title: Load Balancing IIS Sites with NLB
author: Karim Elatov
layout: post
permalink: /2013/04/load-balancing-iis-sites-with-nlb/
dsq_thread_id:
  - 1405433067
categories:
  - Home Lab
  - Networking
tags:
  - nlbmgr
  - Windows IIS
  - Windows NLB
---
Here is quick diagram of what I was trying to achieve:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/NLB_IIS.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/NLB_IIS.jpg']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/NLB_IIS.jpg" alt="NLB IIS Load Balancing IIS Sites with NLB" width="747" height="415" class="alignnone size-full wp-image-8175" title="Load Balancing IIS Sites with NLB" /></a>

**IIS-1**

*   Primary/cluster interface: 192.168.250.47 
*   Secondary Interface: 192.168.250.48

**IIS-2**

*   Primary/Cluster Interface: 192.168.250.49 
*   Secondary Interface: 192.168.250.50

**Cluster**

*   Virtual IP: 192.168.250.51

I setup both of the IIS Servers in same manner as I described in <a href="http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture']);">this</a> post. Since both of the IIS Servers were VMs running on KVM, I was able to easily add a secondary network interfaces to both VMs and ensure that they are on the same network. I will be using NLB in *Unicast* mode and that is why two interfaces is necessary (I will talk more about that later).

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
    

Then go to &#8220;Features&#8221; -> &#8220;Add Features&#8221;. From the list select &#8220;Network Load Balancing&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_manager_NLB_selected.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/server_manager_NLB_selected.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_manager_NLB_selected.png" alt="server manager NLB selected Load Balancing IIS Sites with NLB" width="774" height="569" class="alignnone size-full wp-image-8177" title="Load Balancing IIS Sites with NLB" /></a>

Click &#8220;Next&#8221;, &#8220;Install&#8221;, and let the install go through.

### Configure Network Load Balancing Services

Once NLB is installed on both IIS Servers, go to first IIS server (iis-1) and run

    nlbmgr
    

That will launch the &#8220;Network Load Balancing Manager&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-started.png" alt="nlbmgr started Load Balancing IIS Sites with NLB" width="764" height="533" class="alignnone size-full wp-image-8178" title="Load Balancing IIS Sites with NLB" /></a>

Then from the Menu Bar go to &#8220;Cluster&#8221; -> &#8220;New&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlb_mgr_cluster_new_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlb_mgr_cluster_new_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlb_mgr_cluster_new_g.png" alt="nlb mgr cluster new g Load Balancing IIS Sites with NLB" width="764" height="532" class="alignnone size-full wp-image-8179" title="Load Balancing IIS Sites with NLB" /></a>

In the &#8220;New Cluster&#8221; wizard enter the first IIS Server&#8217;s hostname (in my case it was &#8216;iis-1&#8242;) for the host field and click on &#8220;Connect&#8221;. After you hit connect it will connect to the IIS server and provide a list of available interfaces on the Web Server. Choose the primary interface (192.168.250.47):

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-ints-from-host.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-ints-from-host.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-ints-from-host.png" alt="nlbmgr ints from host Load Balancing IIS Sites with NLB" width="469" height="437" class="alignnone size-full wp-image-8180" title="Load Balancing IIS Sites with NLB" /></a>

After you click &#8220;Next&#8221; you will see the &#8220;Host Parameters&#8221; window, you can leave all the default options here:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params.png" alt="nlbmgr host params Load Balancing IIS Sites with NLB" width="472" height="437" class="alignnone size-full wp-image-8181" title="Load Balancing IIS Sites with NLB" /></a>

Click &#8220;Next&#8221; and it will take you to the &#8220;Cluster IP Addresses&#8221; screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-cluster-ips.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-cluster-ips.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr-cluster-ips.png" alt="nlbmgr cluster ips Load Balancing IIS Sites with NLB" width="470" height="437" class="alignnone size-full wp-image-8182" title="Load Balancing IIS Sites with NLB" /></a>

From here click &#8220;Add&#8221; and enter the IP that will be used as the &#8220;Cluster&#8221; IP address. In my case it was 192.168.250.51:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_ip-ad.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_ip-ad.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_ip-ad.png" alt="nlbmgr add ip ad Load Balancing IIS Sites with NLB" width="361" height="292" class="alignnone size-full wp-image-8183" title="Load Balancing IIS Sites with NLB" /></a>

Click &#8220;OK&#8221;, then click &#8220;Next&#8221;, and you will get to the &#8220;Cluster Parameters&#8221; page. On this screen fill in the &#8220;Full Internet Name&#8221; of the cluster (cluster.elatov.local) and leave the Operation Mode in **Unicast** (any mode will work as long as the cluster can converge).

If you select *Multicast* mode your upstream switch will have to support multicast. *Unicast* doesn&#8217;t require any configuration on the upstream switch but does require two Network Interfaces. The reason for this has to do with how NLB operates. When the primary Network Interfaces are setup to be part of an NLB cluster they actually won&#8217;t be able to talk to each other with those interfaces. So we need a second interface on a network that has access to the primary network (the easiest way to accomplish that is put it on the same subnet). More information regarding the Cluster operation modes can be seen in <a href="http://technet.microsoft.com/en-us/library/bb742455.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technet.microsoft.com/en-us/library/bb742455.aspx']);">this</a> Microsoft article, from that article:

> Network Load Balancing&#8217;s unicast mode has the side effect of disabling communication between cluster hosts using the cluster adapters. Since outgoing packets for another cluster host are sent to the same MAC address as the sender, these packets are looped back within the sender by the network stack and never reach the wire. This limitation can be avoided by adding a second network adapter card to each cluster host. In this configuration, Network Load Balancing is bound to the network adapter on the subnet that receives incoming client requests, and the other adapter is typically placed on a separate, local subnet for communication between cluster hosts and with back-end file and database servers. Network Load Balancing only uses the cluster adapter for its heartbeat and remote control traffic.

Here is how my &#8220;Cluster Parameters&#8221; screen looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_clus_params_filled_out.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_clus_params_filled_out.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_clus_params_filled_out.png" alt="nlbmgr clus params filled out Load Balancing IIS Sites with NLB" width="469" height="438" class="alignnone size-full wp-image-8184" title="Load Balancing IIS Sites with NLB" /></a>

After you click &#8220;Next&#8221; you will see the &#8220;Port Rules&#8221; screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_port_rules.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_port_rules.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_port_rules.png" alt="nlbmgr port rules Load Balancing IIS Sites with NLB" width="471" height="437" class="alignnone size-full wp-image-8185" title="Load Balancing IIS Sites with NLB" /></a>

If you click &#8220;Edit&#8221; it will show you the default rule set:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_port_rule.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_port_rule.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_port_rule.png" alt="nlbmgr edit port rule Load Balancing IIS Sites with NLB" width="361" height="444" class="alignnone size-full wp-image-8186" title="Load Balancing IIS Sites with NLB" /></a>

By default it&#8217;s setup to load balance all the ports &#8220;0-65535&#8243; and that will work for our setup. If you wanted to be pedantic you could create one rule to only balance port 80, but the default is okay. Now the *Affinity* setting is noteworthy, cause it basically decides how the load balancing occurs. <a href="http://technet.microsoft.com/en-us/library/cc778263%28v=ws.10%29.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technet.microsoft.com/en-us/library/cc778263%28v=ws.10%29.aspx']);">This</a> Microsoft article explains the different modes, here are the important excerpts:

> *   The **None** option specifies that multiple connections from the same client IP address can be handled by different cluster hosts (no client affinity). In order to allow Network Load Balancing to properly handle IP fragments, you should avoid using None when selecting UDP or Both for your protocol setting.
> *   The **Single** option specifies that Network Load Balancing should direct multiple requests from the same client IP address to the same cluster host. This is the default setting for affinity.
> *   **Class C** affinity specifies that Network Load Balancing direct multiple requests from the same TCP/IP Class C address range to the same cluster host.

Both of the IIS Servers weren&#8217;t using any sessions so the *Affinity* didn&#8217;t really matter in my setup, so I left the default &#8220;Single&#8221; option. At this point we are ready to click &#8220;Finish&#8221; and as soon as we do we will see the first Node getting added to the cluster. If it&#8217;s successful we will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_node1_added.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_node1_added.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_node1_added.png" alt="nlbmgr node1 added Load Balancing IIS Sites with NLB" width="760" height="526" class="alignnone size-full wp-image-8187" title="Load Balancing IIS Sites with NLB" /></a>

Now to add the second node. Right click on the cluster and select &#8220;Add Host To Cluster&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_host_to_cluster_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_host_to_cluster_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_add_host_to_cluster_g.png" alt="nlbmgr add host to cluster g Load Balancing IIS Sites with NLB" width="762" height="532" class="alignnone size-full wp-image-8215" title="Load Balancing IIS Sites with NLB" /></a>

In the host field enter the hostname of the second IIS server (iis-2) and click connect. If the connection is successful you will see a list of Interfaces on that Web Server:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_interface_second_node.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_interface_second_node.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_interface_second_node.png" alt="nlbmgr interface second node Load Balancing IIS Sites with NLB" width="470" height="435" class="alignnone size-full wp-image-8216" title="Load Balancing IIS Sites with NLB" /></a>

Select the Primary Interface and click &#8220;Next&#8221; and you will be taken to the &#8220;Host Parameters&#8221; screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_host_params2.png" alt="nlbmgr host params2 Load Balancing IIS Sites with NLB" width="472" height="437" class="alignnone size-full wp-image-8217" title="Load Balancing IIS Sites with NLB" /></a>

Leave the defaults and click &#8220;Next&#8221;. You will then be taken to the same &#8220;Port Rules&#8221; screen. Click Edit and make sure &#8220;Single&#8221; mode is selected for the *Affinity* setting:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_rule_node2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_rule_node2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_edit_rule_node2.png" alt="nlbmgr edit rule node2 Load Balancing IIS Sites with NLB" width="360" height="444" class="alignnone size-full wp-image-8218" title="Load Balancing IIS Sites with NLB" /></a>

All of the above looks correct and we can hit &#8220;OK&#8221; to go to the previous window and then click &#8220;Finish&#8221; to add the Node to the cluster. You will see the node converging and if all goes well you will see both nodes converged:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_converged_node2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_converged_node2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_converged_node2.png" alt="nlbmgr converged node2 Load Balancing IIS Sites with NLB" width="775" height="598" class="alignnone size-full wp-image-8219" title="Load Balancing IIS Sites with NLB" /></a>

### Windows 2003 Weak Host Receive and Send Models(Optional)

If the conversion fails we will need to enable weak host receive and send options on our secondary interface. Most of the information can be seen in <a href="http://kb.vmware.com/kb/1006778" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1006778']);">this</a> VMware KB. Basically we will have to run the following on both IIS Servers:

    netsh interface ipv4 set interface "Local Area Connection 2" weakhostreceive=enable 
    netsh interface ipv4 set interface "Local Area Connection 2" weakhostsend=enable
    

More information regarding Windows Weak Host Receive and Send can be found in <a href="http://technet.microsoft.com/en-us/magazine/2007.09.cableguy.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technet.microsoft.com/en-us/magazine/2007.09.cableguy.aspx']);">this</a> Microsoft article.

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS-1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS-1.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS-1.png" alt="chrome test IIS 1 Load Balancing IIS Sites with NLB" width="787" height="352" class="alignnone size-full wp-image-8188" title="Load Balancing IIS Sites with NLB" /></a>

Since we chose &#8220;Single&#8221; for our Affinity mode, if you go to page again, it will take you to the same IIS server. So let&#8217;s go ahead and stop the node that we are currently going to. As you can see in my case that is IIS-2. So from IIS-1, launch the &#8220;Network Load Balancing Manager&#8221; by running:

    nlbmgr
    

From the NLB Manager right click on our node and go to &#8220;Control Host&#8221; -> &#8220;Stop&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_stop_host.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_stop_host.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_stop_host.png" alt="nlbmgr stop host Load Balancing IIS Sites with NLB" width="1042" height="886" class="alignnone size-full wp-image-8220" title="Load Balancing IIS Sites with NLB" /></a>

If the process is successful you will see the node in a &#8220;Red&#8221; state:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_2nd_node_stopped.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_2nd_node_stopped.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/nlbmgr_2nd_node_stopped.png" alt="nlbmgr 2nd node stopped Load Balancing IIS Sites with NLB" width="773" height="598" class="alignnone size-full wp-image-8221" title="Load Balancing IIS Sites with NLB" /></a>

Now from the client go to the same page (**http://cluster/test.html**) and you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/chrome_test_IIS2.png" alt="chrome test IIS2 Load Balancing IIS Sites with NLB" width="787" height="353" class="alignnone size-full wp-image-8189" title="Load Balancing IIS Sites with NLB" /></a>

Now we know NLB is working properly, go back to the NLB Manager and start the node back up.

