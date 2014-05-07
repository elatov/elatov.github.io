---
title: Enabling More Host-Resources Information from the Net-SNMP MIB on ESX Classic
author: Karim Elatov
layout: post
permalink: /2012/04/enabling-more-host-resources-information-from-the-net-snmp-mib-on-esx-classic/
dsq_thread_id:
  - 1405199797
categories:
  - Networking
  - VMware
tags:
  - ESX
  - ESXi
  - Host_Resources_MIB
  - net-snmp
  - snmpwalk
---
I wanted to get more host information from an ESX host when querying the host with snmp. Specifically, I was interested in the Host_Resources MIB (<a href="http://www.net-snmp.org/docs/mibs/host.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.net-snmp.org/docs/mibs/host.html']);">net-snmp HOST-RESOURCES-MIB</a>). Following the instructions from the &#8220;<a href="http://www.vmware.com/pdf/vsp_4_snmp_config.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsp_4_snmp_config.pdf']);">Configuring the Net-SNMP Agent on ESX Hosts</a>&#8221; article, I ran the following to enable snmpd:

[code]  
[root@localhost ~]# service snmpd start  
Starting snmpd: [ OK ]  
[/code]

Now querying for host resources, I only see a limited output:

[code]  
[root@localhost ~]# snmpwalk -v 2c -c public localhost 1.3.6.1.2.1.25  
HOST-RESOURCES-MIB::hrSystemUptime.0 = Timeticks: (2568848477) 297 days, 7:41:24.77  
HOST-RESOURCES-MIB::hrSystemUptime.0 = No more variables left in this MIB View (It is past the end of the MIB tree)  
[/code]

This is actually expected since net-snmp on ESX is not supported as per KB <a href="http://kb.vmware.com/kb/1020649" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1020649']);">1020649</a>. However there is supposed to be a lot more output, checking out the setting for the snmpd service I see the following:

[code]  
[root@localhost ~]# grep 1.3.6.1.2.1.25 /etc/snmp/snmpd.conf  
view systemview included .1.3.6.1.2.1.25.1.1  
[/code]

That MIB is limited, the root OID of the Host-Resources MIB is .1.3.6.1.2.1.25, but we are limiting the OID to be a subset of the OID (.1.3.6.1.2.1.25<span style="text-decoration: underline;"><strong>.1.1</strong></span>). More information regarding how OIDs work can be found <a href="http://en.wikipedia.org/wiki/Object_identifier" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Object_identifier']);">here</a>. So let&#8217;s go ahead and allow the whole MIB to be queried. Edit the file with vi:

[code]  
[root@localhost ~]# vi /etc/snmp/snmpd.conf  
[/code]

Scroll down to the line that looks like this:

[code]  
view systemview included .1.3.6.1.2.1.25.1.1  
[/code]

and make it look like this:

[code]  
view systemview included .1.3.6.1.2.1.25  
[/code]

After you make the change, exit vi (by typing &#8220;:wq&#8221;) and confirm the file was edited properly:

[code]  
[root@localhost ~]# grep 1.3.6.1.2.1.25 /etc/snmp/snmpd.conf  
view systemview included .1.3.6.1.2.1.25  
[/code]

If you see the same output as above then restart the snmpd service to apply the changes:

[code]  
[root@localhost ~]# service snmpd restart  
Stopping snmpd: [ OK ]  
Starting snmpd: [ OK ]  
[/code]

And if you run the same query again:

[code]  
[root@localhost ~]# snmpwalk -v 2c -c public localhost 1.3.6.1.2.1.25  
HOST-RESOURCES-MIB::hrSystemUptime.0 = Timeticks: (2568874428) 297 days, 7:45:44  
.28  
HOST-RESOURCES-MIB::hrSystemDate.0 = STRING: 2012-4-14,22:9:35.0,-7:0  
HOST-RESOURCES-MIB::hrSystemInitialLoadDevice.0 = INTEGER: 1536  
HOST-RESOURCES-MIB::hrSystemInitialLoadParameters.0 = STRING: "ro root=UUID=5ac0  
8fa5-b922-441c-80e1-d22018de2419 mem=800M nousbstorage quiet  
"  
HOST-RESOURCES-MIB::hrSystemNumUsers.0 = Gauge32: 2  
HOST-RESOURCES-MIB::hrSystemProcesses.0 = Gauge32: 103  
HOST-RESOURCES-MIB::hrSystemMaxProcesses.0 = INTEGER: 0  
HOST-RESOURCES-MIB::hrMemorySize.0 = INTEGER: 802360 KBytes  
HOST-RESOURCES-MIB::hrStorageIndex.1 = INTEGER: 1  
...  
...  
[/code]

The output was much larger. This only works for ESX and not for ESXi and as the &#8220;<a href="http://www.vmware.com/pdf/vsp_4_snmp_config.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsp_4_snmp_config.pdf']);">Configuring the Net-SNMP Agent on ESX Hosts</a>&#8221; article mentions, this is actually not supported, so use with care. Checking out KB <a href="http://kb.vmware.com/kb/2005377" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2005377']);">2005377</a>, the Host-Resources MIB is added for ESXi 5.0, so if you want to get that information on an ESXi host, then update to 5.0 <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Enabling More Host Resources Information from the Net SNMP MIB on ESX Classic" class="wp-smiley" title="Enabling More Host Resources Information from the Net SNMP MIB on ESX Classic" /> 

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESXi on MacMini 6,2" href="http://virtuallyhyper.com/2014/04/esxi-macmini-62/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/04/esxi-macmini-62/']);" rel="bookmark">ESXi on MacMini 6,2</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="A Few Words on VOMA" href="http://virtuallyhyper.com/2012/09/a-few-words-on-voma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/a-few-words-on-voma/']);" rel="bookmark">A Few Words on VOMA</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="ESX Host Experiencing High Latency to a Hitachi HDS Array" href="http://virtuallyhyper.com/2012/04/esx-host-experiencing-high-latency-to-a-hitachi-array/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/esx-host-experiencing-high-latency-to-a-hitachi-array/']);" rel="bookmark">ESX Host Experiencing High Latency to a Hitachi HDS Array</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/enabling-more-host-resources-information-from-the-net-snmp-mib-on-esx-classic/" title=" Enabling More Host-Resources Information from the Net-SNMP MIB on ESX Classic" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:ESX,ESXi,Host_Resources_MIB,net-snmp,snmpwalk,blog;button:compact;">Recently I received a call from a European customer saying that they were having performance issues with their VMs. Whenever I hear performance issues, I automatically think esxtop. To check...</a>
</p>