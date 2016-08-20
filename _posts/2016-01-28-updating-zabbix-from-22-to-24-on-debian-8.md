---
published: true
layout: post
title: "Updating Zabbix from 2.2 to 2.4 on Debian 8"
author: Karim Elatov
categories: [os,vmware,home_lab]
tags: [linux,zabbix,debian]
---
I noticed that a while back [zabbix released](https://support.zabbix.com/browse/ZBX-9629) a repo for Debian 8 and I decided to update my Zabbix Server instance.

### Prepare for the Update
Back up the zabbix database if possible, I take weekly backups so I was okay. Next let's go ahead and shutdown the agent and the server:

	sudo systemctl stop zabbix-agent.service
	sudo systemctl stop zabbix-server.service

Then I updated my apt sources files as such:

	┌─[elatov@kerch] - [/home/elatov] - [2015-11-29 10:09:00]
	└─[0] <> cat /etc/apt/sources.list.d/zabbix.list
	deb http://repo.zabbix.com/zabbix/2.4/debian/ jessie main
	deb-src http://repo.zabbix.com/zabbix/2.4/debian/ jessie main
	
Lastly update the package cache:

	sudo apt-get update

### Update Zabbix Agent and Server to Version 2.4
At this point I ran the following to update the agent:

	sudo apt-get upgrade

After I was done with that I updated the server:

	sudo apt-get upgrade zabbix-server-mysql
	
During the update it asked if I wanted to update my configuration files, but they were close enough so I left the original ones in place. I noticed that after the update the services are auto started and the database is updated on first startup:

	$ less /var/log/zabbix/zabbix_server.log
	14513:20151129:101317.477 using configuration file: /etc/zabbix/zabbix_server.conf
	 14513:20151129:101317.485 current database version (mandatory/optional): 02020000/02020001
	 14513:20151129:101317.485 required mandatory version: 02040000
	 14513:20151129:101317.485 starting automatic database upgrade
	 14513:20151129:101317.486 completed 0% of database upgrade
	 14513:20151129:101317.552 completed 1% of database upgrade
	 ..
	 ..
	 14513:20151129:101319.087 completed 99% of database upgrade
	 14513:20151129:101319.087 completed 100% of database upgrade
	 14513:20151129:101319.088 database upgrade fully completed
	 14513:20151129:101319.111 server #0 started [main process]
	 
### Post Update Clean Up

I noticed that the VMware templates have changed and not all the Macros are utilized any more. So I deleted all the discovered VMs and Hypervisors and readded the discovery as described in [Virtual machine monitoring](https://www.zabbix.com/documentation/2.4/manual/vm_monitoring) (just to start from a new slate). It actually worked out pretty well. I lost my old history data, but that's okay for me. After that I noticed some of the performance counters were failing for some reason:

	18029:20151129:123339.447 item "564d2d47-8acb-62e5-8151-f4a924b1670a:vmware.vm.net.if.out[{$URL},{HOST.HOST},4000,bps]" became not supported: Performance counter data is not available.

After looking around I noticed that only some of the VMs are not showing performance data. You can check all the "not supported" items by either running the following SQL command:

	SELECT * FROM zabbix.items WHERE state=1;
	
Or by doing the following in the Zabbix UI (as described in [here](https://www.zabbix.com/forum/showthread.php?p=174743)):

> Click on Configure->Hosts<br /> 
> Now click on Items for any host<br /> 
> Now click on Filter and the filter options will appear<br /> 
> Change the Status drop down to Not Supported and clear the Host field.<br /> 
> Now click the Filter button

Then I logged into the ESXi host and noticed that VMs with **vmxnet3** NICs are not showing any performance data:

![vm-missing-net-perf-data](https://dl.dropboxusercontent.com/u/24136116/blog_pics/zabbix-to-24/vm-missing-net-perf-data.png)

While VMs with e1000 Nics had the performance data:

![vm-contains-net-perf-data](https://dl.dropboxusercontent.com/u/24136116/blog_pics/zabbix-to-24/vm-contains-net-perf-data.png)

Initially I ran into this old VMware KB: [Networking performance data is missing when the VMXNET3 adapter is used (1015402)](http://kb.vmware.com/kb/1015402), but I was on ESXi 6.0 not 4.x. Then by dumb luck I ran into the release notes for [ESXi 6.0 Update 1a](http://pubs.vmware.com/Release_Notes/en/vsphere/60/vsphere-esxi-60u1-release-notes.html#rnetworkingissues) and I saw the following:

> **Virtual machine Network performance data metrics not available for VM configured with VMXNET3 connected to a standard vSwitch**
> 
> You are unable to view the real time performance graph for Network of a virtual machine configured with VMXNET3 adapter in the VMware vSphere Client 6.0 as the option is not available in the Switch to drop-down list. 
> 
> This issue is resolved in this release.

So I decided to update my ESXi host.

### Update from ESXi 6.0b to ESXi 6.0 Update 1a

The process is same as before, shutdown all the running VMs:

	[root@macm:~] vmware -lv
	VMware ESXi 6.0.0 build-2809209
	VMware ESXi 6.0.0 GA
	[root@macm:~] vmware-autostart.sh stop

Put the host into maintenance mode:

	root@macm:~] esxcli system maintenanceMode set -e true

Either download the offline bundle from here:

> my.vmware.com/group/vmware/info?slug=datacenter_cloud_infrastructure/vmware_vsphere/6_0

![vmware-download-6u1a](https://dl.dropboxusercontent.com/u/24136116/blog_pics/zabbix-to-24/vmware-download-6u1a.png)
and then **scp** the bundle to the host:

	┌─[elatov@macair] - [/Users/elatov/Downloads] - [2015-11-29 04:29:47]
	└─[0] <> scp ESXi600-201510001.zip macm:/vmfs/volumes/datastore1/.
	Password:
	ESXi600-201510001.zip

and then install it:

	[root@macm:~] esxcli software profile update -d /vmfs/volumes/datastore1/ESXi600-201510001.zip -p ESXi-6.0.0-20151004001-standard
	Update Result
	   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
	   Reboot Required: true
	   VIBs Installed: VMware_bootbank_esx-base_6.0.0-1.20.3073146, V


Or just download the bundle directly:

	esxcli network firewall ruleset set -e true -r httpClient
	esxcli software profile update -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml -p ESXi-6.0.0-20151004001-standard

I prefer to download the bundle so I can use it later if necessary. Then finally reboot the host:

	[root@macm:~] esxcli system shutdown reboot -r 'update_to_6_0U1a'
	
### Confirm the Perf Data is There
After I rebooted the host and powered on the VM I did end up seeing the performance data (and new version):

	[root@macm:~] vmware -lv
	VMware ESXi 6.0.0 build-3073146
	VMware ESXi 6.0.0 Update 1

![new-vm-perf-data.png](https://dl.dropboxusercontent.com/u/24136116/blog_pics/zabbix-to-24/new-vm-perf-data.png)


After some time I saw the following in the logs of the zabbix server:

	1349:20151129:165139.402 item "564d2d47-8acb-62e5-8151-f4a924b1670a:vmware.vm.
	net.if.out[{$URL},{HOST.HOST},4000,pps]" became supported
	
And also from the Zabbix UI I saw new data come in:

![zabbix-new-data](https://dl.dropboxusercontent.com/u/24136116/blog_pics/zabbix-to-24/zabbix-new-data.png)
