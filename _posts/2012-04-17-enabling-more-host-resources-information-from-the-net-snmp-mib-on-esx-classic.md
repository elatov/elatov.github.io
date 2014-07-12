---
title: Enabling More Host-Resources Information from the Net-SNMP MIB on ESX Classic
author: Karim Elatov
layout: post
permalink: /2012/04/enabling-more-host-resources-information-from-the-net-snmp-mib-on-esx-classic/
dsq_thread_id:
  - 1405199797
categories: ['networking', 'vmware']
tags: ['host_resources_mib', 'snmp']
---

I wanted to get more host information from an ESX host when querying the host with snmp. Specifically, I was interested in the Host_Resources MIB ([Configuring the Net-SNMP Agent on ESX Hosts](http://www.net-snmp.org/docs/mibs/host.html)" article, I ran the following to enable snmpd:


	# service snmpd start
	Starting snmpd: [ OK ]


Now querying for host resources, I only see a limited output:


	# snmpwalk -v 2c -c public localhost 1.3.6.1.2.1.25
	HOST-RESOURCES-MIB::hrSystemUptime.0 = Timeticks: (2568848477) 297 days, 7:41:24.77
	HOST-RESOURCES-MIB::hrSystemUptime.0 = No more variables left in this MIB View (It is past the end of the MIB tree)


This is actually expected since net-snmp on ESX is not supported as per KB [1020649](http://kb.vmware.com/kb/1020649). However there is supposed to be a lot more output, checking out the setting for the snmpd service I see the following:


	# grep 1.3.6.1.2.1.25 /etc/snmp/snmpd.conf
	view systemview included .1.3.6.1.2.1.25.1.1


That MIB is limited, the root OID of the Host-Resources MIB is .1.3.6.1.2.1.25, but we are limiting the OID to be a subset of the OID (.1.3.6.1.2.1.25**.1.1**). More information regarding how OIDs work can be found [here](http://en.wikipedia.org/wiki/Object_identifier). So let's go ahead and allow the whole MIB to be queried. Edit the file with vi:


	# vi /etc/snmp/snmpd.conf


Scroll down to the line that looks like this:


	view systemview included .1.3.6.1.2.1.25.1.1


and make it look like this:


	view systemview included .1.3.6.1.2.1.25


After you make the change, exit vi (by typing ":wq") and confirm the file was edited properly:


	# grep 1.3.6.1.2.1.25 /etc/snmp/snmpd.conf
	view systemview included .1.3.6.1.2.1.25


If you see the same output as above then restart the snmpd service to apply the changes:


	# service snmpd restart
	Stopping snmpd: [ OK ]
	Starting snmpd: [ OK ]


And if you run the same query again:


	# snmpwalk -v 2c -c public localhost 1.3.6.1.2.1.25
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


The output was much larger. This only works for ESX and not for ESXi and as the "[2005377](http://www.vmware.com/pdf/vsp_4_snmp_config.pdf), the Host-Resources MIB is added for ESXi 5.0, so if you want to get that information on an ESXi host, then update to 5.0 :)

### Related Posts

- [ESXi on MacMini 6,2](/2014/04/esxi-macmini-62/)
- [A Few Words on VOMA](http://virtuallyhyper.com/2012/09/a-few-words-on-voma/)

- [ESX Host Experiencing High Latency to a Hitachi HDS Array](/2012/04/esx-host-experiencing-high-latency-to-a-hitachi-array/)

