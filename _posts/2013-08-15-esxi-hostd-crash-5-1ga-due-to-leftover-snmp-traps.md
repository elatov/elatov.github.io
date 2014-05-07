---
title: ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps
author: Karim Elatov
layout: post
permalink: /2013/08/esxi-hostd-crash-5-1ga-due-to-leftover-snmp-traps/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1609435444
categories:
  - Networking
  - VMware
tags:
  - hostd
  - snmp
  - VMware
---
## ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps

One day I tried to open console on a VM and I got the **MKS** error:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/08/mks_error.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/08/mks_error.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/08/mks_error.png" alt="mks error ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps" width="307" height="136" class="alignnone size-full wp-image-9296" title="ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps" /></a>

I logged into the host and I tried to run an **esxcli** command and I saw the following:

    ~ # esxcli network 
    Connect to localhost failed: Connection failure
    

It looks like **hostd** wasn&#8217;t happy. I quickly restarted services:

    ~ # services.sh restart
    

and that brought back **hostd** and the **MKS** errors went away. I didn&#8217;t have time to find out what was going on, so I grabbed a log bundle:

    ~ # vm-support
    

I downloaded the log bundle from the ESXi host and put it on my laptop. Here is the file:

    elatov@kmac:~/es$ls *.tgz
    esx-prod-vmware01-2013-08-12--14.06.tgz
    

I extracted the file:

    elatov@kmac:~/es$ tar xvzf esx-prod-vmware01-2013-08-12--14.06.tgz
    

I then put the log files together since they get split apart to save space when the log bundle is generated:

    elatov@kmac:~/es$cd esx-prod-vmware01-2013-08-12--14.06/
    elatov@kmac:~/es/esx-prod-vmware01-2013-08-12--14.06$./reconstruct.sh 
    

First I wanted to see what time we ran the service restart, here is when that happened:

    elatov@kmac:~/es/esx-prod-vmware01-2013-08-12--14.06/var/log$grep 'services.sh restart' shell.log  | tail -1
    2013-08-12T13:55:30Z shell[3389987]: [root]: services.sh restart
    

Around that time I saw the following in the **var/log/hostd.log** file:

    2013-08-12T13:48:25.650Z [6FE81B90 info 'ha-eventmgr'] Event 8573 : The file table of the ramdisk 'root' is full.  As a result, the file /var/run/vmware/tickets/vmtck-5206bb19-94d6-12 could not be created by the application 'hostd-worker'.
    

There was actually an event fired for the &#8220;ramdisk&#8221; is full:

    2013-08-12T13:48:25.645Z [6EEC2B90 error 'Cimsvc'] Connect: Failed to get ticket, not connected to cimom
    2013-08-12T13:48:25.646Z [6FE81B90 info 'VmkVprobSource'] VmkVprobSource::Post event: (vim.event.EventEx) {
    -->    dynamicType = <unset>,
    -->    key = 825110831,
    -->    chainId = 808464928,
    -->    createdTime = "1970-01-01T00:00:00Z",
    -->    userName = "",
    -->    datacenter = (vim.event.DatacenterEventArgument) null,
    -->    computeResource = (vim.event.ComputeResourceEventArgument) null,
    -->    host = (vim.event.HostEventArgument) {
    -->       dynamicType = <unset>,
    -->       name = "prod-vmware01",
    -->       host = 'vim.HostSystem:ha-host',
    -->    },
    -->    vm = (vim.event.VmEventArgument) null,
    -->    ds = (vim.event.DatastoreEventArgument) null,
    -->    net = (vim.event.NetworkEventArgument) null,
    -->    dvs = (vim.event.DvsEventArgument) null,
    -->    fullFormattedMessage = <unset>,
    -->    changeTag = <unset>,
    -->    eventTypeId = "esx.problem.visorfs.ramdisk.inodetable.full",
    -->    severity = <unset>,
    -->    message = <unset>,
    -->    arguments = (vmodl.KeyAnyValue) [
    -->       (vmodl.KeyAnyValue) {
    -->          dynamicType = <unset>,
    -->          key = "1",
    -->          value = "root",
    -->       },
    -->       (vmodl.KeyAnyValue) {
    -->          dynamicType = <unset>,
    -->          key = "2",
    -->          value = "/var/run/vmware/tickets/vmtck-5206bb19-94d6-12",
    -->       },
    -->       (vmodl.KeyAnyValue) {
    -->          dynamicType = <unset>,
    -->          key = "3",
    -->          value = "hostd-worker",
    -->       }
    -->    ],
    -->    objectId = "ha-eventmgr",
    -->    objectType = "vim.HostSystem",
    -->    objectName = <unset>,
    -->    fault = (vmodl.MethodFault) null,
    --> }
    

I found <a href="http://kb.vmware.com/kb/2040707" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2040707']);">this</a> VMware KB, notice some of the symptoms list the following:

> Opening a virtual machine console from the vSphere Client fails with the error:
> 
> Unable to contact the MKS

That is what we saw. Apparently this is caused by enabling SNMPD. From the same KB:

> This issue occurs when SNMPD is enabled and the **/var/spool/snmp** folder is filled with Simple Network Management Protocol (SNMP) trap files.

Looking over the esxi host, I did see SNMPD enabled:

    elatov@kmac:~/es/esx-prod-vmware01-2013-08-12--14.06$cat etc/vmware/snmp.xml
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <config>
     <snmpSettings>
       <enable>true</enable>
       <port>161</port>
       <syscontact></syscontact>
       <syslocation></syslocation>
       <EnvEventSource>indications</EnvEventSource>
       <communities>public</communities>
       <targets>prod-vmware01@161 public</targets>
       <engineid>0000006300</engineid>
       <loglevel>info</loglevel>
       <authProtocol></authProtocol>
       <privProtocol></privProtocol>
     </snmpSettings>
    </config>
    

From KB we can double confirm if that is issue by running the following:

> ls /var/spool/snmp | wc -l
> 
> Note: If the output indicates that the value is 2000 or more, then this may be causing the full inodes.

Running that on the host, we saw the following:

    ~ # ls /var/spool/snmp | wc -l
    5385 
    

That confirmed that we are running into that issue. This is fixed in 5.1u1, again from the KB:

> This issue is resolved in ESXi 5.1 Update 1

Checking over the current version that we were on, I saw the following:

    elatov@kmac:~/es/esx-prod-vmware01-2013-08-12--14.06$cat commands/vmware_-vl.txt
    VMware ESXi 5.1.0 build-799733
    VMware ESXi 5.1.0 GA
    

For now we disabled SNMP logging and also cleaned up the left over SNMP files:

    # cd /var/spool/snmp
    # for i in $(ls | grep trp); do rm -f $i;done
    

After we update to 5.1U1, I am sure the issue will be fixed.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/08/esxi-hostd-crash-5-1ga-due-to-leftover-snmp-traps/" title=" ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:hostd,snmp,VMware,blog;button:compact;">ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps One day I tried to open console on a VM and I got the MKS error: I logged into the host...</a>
</p>