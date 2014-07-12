---
published: true
title: Update Zabbix to 2.2 and Monitor VMware
author: Karim Elatov
layout: post
permalink: "/2014/05/update-zabbix-2-2-monitor-vmware/"
categories: ['os', 'home_lab', 'vmware']
tags: ['mysql', 'debian', 'zabbix', 'linux','monitoring']
---

Starting with Version 2.2 of Zabbix, we can now monitor VMware hosts. From [What's new in Zabbix 2.2.0][1]:

> A new feature in Zabbix 2.2.0 is VMware virtual machine monitoring. It allows to monitor VMware vCenter and vSphere installations for various VMware hypervisor and virtual machine properties and statistics.
>
> Zabbix can use low-level discovery rules to automatically discover VMware hypervisors and virtual machines and create hosts to monitor them, based on pre-defined host prototypes. See Virtual machine monitoring for more detailed information.

So I decided to update Zabbix to 2.2 and Monitor VMware hosts.

### Backup current Zabbix Configuration

All the settings for zabbix are stored under **/etc/zabbix**, so let's backup that directory:

    sudo tar cpvjf /tmp/zabbix-conf-back.tar.bz2 /etc/zabbix


If you have the space, backup the MySQL DB as well:

    mysqldump -h localhost -u zabbix -p zabbix > zabbix.sql


### Update Zabbix to 2.2

I was using Debian so the process is pretty easy. First stop the service:

    sudo service zabbix-server stop
    sudo service zabbix-agent stop


Next get the new repository:

    wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb


Then install the new deb package and update all the packages:

    sudo dpkg -i zabbix-release_2.2-1+wheezy_all.deb
    sudo apt-get update
    sudo apt-get dist-upgrade


During the install process it will ask you to setup a Database, **skip** that. The install process will also install new configuration files and will ask you which files you want to keep, choose the following:

    keep the maintainer version


There were a lot of new options and I decided to just keep the new configuration and re-add my original settings into the new version. After the install, the zabbix services are automatically started, so let's go ahead and stop them:

    sudo service zabbix-server stop
    sudo service zabbix-agent stop


Then fix the configuration to include your original settings, here is what I had after I was done:

    $sudo grep -Ev "^#|^$" /etc/zabbix/zabbix_server.conf
    LogFile=/var/log/zabbix/zabbix_server.log
    LogFileSize=1
    PidFile=/var/run/zabbix/zabbix_server.pid
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=password
    DBSocket=/var/run/mysqld/mysqld.sock
    StartIPMIPollers=1
    ListenIP=10.0.0.2
    AlertScriptsPath=/usr/lib/zabbix/alertscripts
    ExternalScripts=/usr/lib/zabbix/externalscripts
    FpingLocation=/usr/bin/fping
    Fping6Location=/usr/bin/fping6


Then do the same thing for the agentd configuration, here is what I had after I was done:

    $sudo grep -Ev "^#|^$" /etc/zabbix/zabbix_agentd.conf
    PidFile=/var/run/zabbix/zabbix_agentd.pid
    LogFile=/var/log/zabbix/zabbix_agentd.log
    LogFileSize=1
    Server=10.0.0.2
    ListenIP=10.0.0.2
    StartAgents=1
    Hostname=me.local.com
    Timeout=15
    Include=/etc/zabbix/zabbix_agentd.d/


The new version installs it's own configuration into apache automatically:

    $ls -l /etc/apache2/conf.d/zabbix
    lrwxrwxrwx 1 root root 23 Feb  8 12:41 /etc/apache2/conf.d/zabbix -> /etc/zabbix/apache.conf


If you had any apache settings for the frontend you can remove them and just use that configuration. Restart apache after you removed (if any) the settings for the zabbix frontend:

    sudo service apache2 restart


Then let's copy our original PHP frontend settings into the new install:

    sudo cp /etc/zabbix/zabbix.conf.php /etc/zabbix/web/.


Then start the zabbix services:

    sudo service zabbix-server start
    sudo service zabbix-agent start


Check out the logs to make sure everything is okay:

    less /var/log/zabbix/zabbix-server.log
    less /var/log/zabbix/zabbix-agent.log


Then visit your PHP frontend (http://localhost/zabbix) and make sure all the information is still there.

### Import VMware Templates

The new VMware Templates are available [here][2]. Go ahead and download them:

    wget https://www.zabbix.org/mw/images/5/50/Template_Virt_VMware-2.2.0.xml
    wget https://www.zabbix.org/mw/images/5/5d/Template_Virt_VMware_Guest-2.2.0.xml
    wget https://www.zabbix.org/mw/images/7/7e/Template_Virt_VMware_Hypervisor-2.2.0.xml


Upon initial import I received the following error:

> Cannot find value map "VMware VirtualMachinePowerState" used for item "Power state" on "Template Virt VMware Guest".

Looks like another person ran into a similar issue [here][3] (it's in German, but you can always translate it) and the fix is to add a couple of values to the MySQL Database as described in [this][4] forum. [Here][5] are the commands that need to be run on the MySQL DB. When I ran the commands they failed, because I was using those values for something else, so I just incremented my **valuemapid** and it worked. Here are the commands I ended up running:

    INSERT INTO `valuemaps` (`valuemapid`,`name`) values ('13','VMware status');
    INSERT INTO `valuemaps` (`valuemapid`,`name`) values ('14','VMware VirtualMachinePowerState');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('75','13','0','gray');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('76','13','1','green');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('77','13','2','yellow');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('78','13','3','red');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('82','14','0','poweredOff');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('83','14','1','poweredOn');
    INSERT INTO `mappings` (`mappingid`,`valuemapid`,`value`,`newvalue`) values ('84','14','2','suspended');


After that, I imported the templates in this order:

1.  Template_Virt_VMware_Hypervisor-2.2.0.xml
2.  Template_Virt_VMware_Guest-2.2.0.xml
3.  Template_Virt_VMware-2.2.0.xml

### Enable the VMware Collector on the Zabbix Server

Now that we have the templates in place, let's enable the VMware collector. First make sure the server is compiled with the **libxml2** option. From [Virtual machine monitoring][6]:

> For virtual machine monitoring to work, Zabbix should be compiled with the --with-libxml2 and --with-libcurl compilation options.

This can be confirmed, by checking the linked libraries of the binary. Here is what I saw:

    elatov@kerch:~$ldd /usr/sbin/zabbix_server | grep -E 'xml|curl'
        libxml2.so.2 => /usr/lib/x86_64-linux-gnu/libxml2.so.2 (0x00007fd56965a000)
        libcurl-gnutls.so.4 => /usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4 (0x00007fd567f29000)


Then to enable the collector I added the following to my **/etc/zabbix/zabbix_server.conf** file:

    StartVMwareCollectors = 1
    VMwareCacheSize = 8M
    VMwareFrequency = 60


I then restarted the service:

    sudo service zabbix_server restart


and I saw the following in the logs under **/var/log/zabbix/zabbix_server.log**:

    17807:20140418:135649.762 Starting Zabbix Server. Zabbix 2.2.3 (revision 44105)
    .
     17807:20140418:135649.762 ****** Enabled features ******
     17807:20140418:135649.762 SNMP monitoring:           YES
     17807:20140418:135649.762 IPMI monitoring:           YES
     17807:20140418:135649.762 WEB monitoring:            YES
     17807:20140418:135649.763 VMware monitoring:         YES
     17807:20140418:135649.763 Jabber notifications:      YES
     17807:20140418:135649.763 Ez Texting notifications:  YES
     17807:20140418:135649.763 ODBC:                      YES
     17807:20140418:135649.763 SSH2 support:              YES
     17807:20140418:135649.763 IPv6 support:              YES
     17807:20140418:135649.763 ******************************
    ...
     17842:20140418:135649.798 server #28 started [vmware collector #1]


### Enable VMware Discovery

To Discover the Hypervisor and VMs, create a new host and leave the default agent interface:

![def-inteface-vmware][7]

Then under Macros, define the following:

*   **{$URL}** - VMware service (vCenter or ESX hypervisor) SDK URL (https://servername/sdk).
*   **{$USERNAME}** - VMware service user name
*   **{$PASSWORD}** - VMware service {$USERNAME} user password

![vm_host_macros][8]

Lastly assign the VMware Template to it:

![vm_host_templates][9]

After some time, you will see the VMs and Hypervisors discovered and their corresponding templates assigned to them. For example here are two VMs that I was running on one of my hosts:

![vmware-vms-discovered][10]

If you go inside the VM, you will see that most of the items are grayed out:

![vmwarevm-discovered-detail][11]

and the host is the UUID of the VM. Same thing was done for the hypervisor, except it attached the **VMware Hypervisor** Template to it, instead of the **VMware Guest** one.

### Expanding the VMware Templates

By default the templates didn't have any graphs defined so I ended up defining graphs for CPU Usage and Memory Usage. I just ended up plotting the already existing items and that was pretty easy. I also ended up creating calculated items to help out with some triggers. Here are the calculated items, I added to the Hypervisor Template:

![added-calculated-items-hv][12]

Here is what I had in the HV CPU Usage Percentage:

![hv-cpu-usage-percent][13]

Here is actual formula:

    last("vmware.hv.cpu.usage[{$URL},{HOST.HOST}]",0)/(last("vmware.hv.hw.cpu.freq[{$URL},{HOST.HOST}]",0)*last("vmware.hv.hw.cpu.threads[{$URL},{HOST.HOST}]",0))


I decided to use **vmware.hv.hw.cpu.threads** to calculate total CPU, but **vmware.hv.hw.cpu.num** is also available (I thought it was appropriate since HyperThreading is enabled).

All of the available VMware keys, are listed [here][14]. For creating calculated items, check out the zabbix documentation [Calculated items][15]. And here was the triggers I ended up creating:

![hv-template-triggers][16]

All the trigger functions are defined in [Supported trigger functions][17]. I also ended up modifying the discovery rules to do graphing for the Datastores and to trigger on high latency. I ended up making similar modifications to the VMware Guest Template. BTW the default keys for the VMware Guest are the following:

![vmware-guest-keys][18]

It's not much but it's a good start. There are already a couple of feature request to get more data. For example [here][19] is a link to one asking for the %RDY of the VM. Now I can tell my ESX host is completely under utilized :)

![cpu-usage-esx][20]

 [1]: https://www.zabbix.com/documentation/2.2/manual/introduction/whatsnew220
 [2]: https://www.zabbix.org/wiki/Zabbix_Templates/Official_Templates#Zabbix_2.2.0
 [3]: https://netzdeponie.de/2014/01/08/import-von-vmware-templates-in-zabbix-schlaegt-fehl/
 [4]: https://www.zabbix.com/forum/showthread.php?p=142941#post142941
 [5]: https://www.zabbix.com/forum/showpost.php?p=142098
 [6]: https://www.zabbix.com/documentation/2.2/manual/vm_monitoring
 [7]: https://github.com/elatov/uploads/raw/master/2014/04/def-inteface-vmware.png
 [8]: https://github.com/elatov/uploads/raw/master/2014/04/vm_host_macros.png
 [9]: https://github.com/elatov/uploads/raw/master/2014/04/vm_host_templates.png
 [10]: https://github.com/elatov/uploads/raw/master/2014/04/vmware-vms-discovered.png
 [11]: https://github.com/elatov/uploads/raw/master/2014/04/vmwarevm-discovered-detail.png
 [12]: https://github.com/elatov/uploads/raw/master/2014/04/added-calculated-items-hv.png
 [13]: https://github.com/elatov/uploads/raw/master/2014/04/hv-cpu-usage-percent.png
 [14]: https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/simple_checks/vmware_keys
 [15]: https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/calculated#usage_examples
 [16]: https://github.com/elatov/uploads/raw/master/2014/04/hv-template-triggers.png
 [17]: https://www.zabbix.com/documentation/2.2/manual/appendix/triggers/functions
 [18]: https://github.com/elatov/uploads/raw/master/2014/04/vmware-guest-keys.png
 [19]: https://support.zabbix.com/browse/ZBXNEXT-2180
 [20]: https://github.com/elatov/uploads/raw/master/2014/04/cpu-usage-esx.png
