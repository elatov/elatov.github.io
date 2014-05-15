---
title: VCAP5-DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/
dsq_thread_id:
  - 1406891938
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify vCenter Server log file names and locations

From VMware KB <a href="http://kb.vmware.com/kb/1021804" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021804']);">1021804</a>:

> *   vCenter Server 2.5-5.x on Windows XP, 2000, 2003: %ALLUSERSPROFILE%\Application Data\VMware\VMware VirtualCenter\Logs\
> *   vCenter Server 2.5-5.x on Windows Vista, 7, 2008: %ALLUSERSPROFILE%\VMware\VMware VirtualCenter\Logs\
> *   vCenter Server 5.x Linux Virtual Appliance: /var/log/vmware/vpx/
> *   vCenter Server 5.x Linux Virtual Appliance UI: /var/log/vmware/vami

### Identify ESXi log files names and locations

From VMware KB <a href="http://kb.vmware.com/kb/2004201" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2004201']);">2004201</a>:

> *   /var/log/auth.log: ESXi Shell authentication success and failure.
> *   /var/log/dhclient.log: DHCP client service, including discovery, address lease requests and renewals.
> *   /var/log/esxupdate.log: ESXi patch and update installation logs.
> *   /var/log/hostd.log: Host management service logs, including virtual machine and host Task and Events, communication with the vSphere Client and vCenter Server vpxa agent, and SDK connections.
> *   /var/log/shell.log: ESXi Shell usage logs, including enable/disable and every command entered.
> *   /var/log/boot.gz: A compressed file that contains boot log information and can be read using zcat /var/log/boot.gz|more.
> *   /var/log/syslog.log: Management service initialization, watchdogs, scheduled tasks and DCUI use.
> *   /var/log/usb.log: USB device arbitration events, such as discovery and pass-through to virtual machines.
> *   /var/log/vob.log: VMkernel Observation events, similar to vob.component.event.
> *   /var/log/vmkernel.log: Core VMkernel logs, including device discovery, storage and networking device and driver events, and virtual machine startup.
> *   /var/log/vmkwarning.log: A summary of Warning and Alert log messages excerpted from the VMkernel logs.
> *   /var/log/vmksummary.log: A summary of ESXi host startup and shutdown, and an hourly heartbeat with uptime, number of virtual machines running, and service resource consumption.

### Identify tools used to view vSphere log files

There are a couple of ways to get around this. First you can look from the DCUI, so if you are in front of the physical machine you can hit F2, then enter the root password, you will then be presented with the following screen:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxi_dcui/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxi_dcui/']);" rel="attachment wp-att-5240"><img class="alignnone size-full wp-image-5240" alt="esxi DCUI VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxi_DCUI.png" width="976" height="343" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Scroll down to "View System Logs" and check you can select different logs to look at:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/view_logs_from_dcui/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/view_logs_from_dcui/']);" rel="attachment wp-att-5241"><img class="alignnone size-full wp-image-5241" alt="view logs from dcui VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/view_logs_from_dcui.png" width="861" height="278" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Another way is from the vSphere Client, open one up directly to the host and then Click on "Home" and you will see the following screen:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/home_view_from_host/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/home_view_from_host/']);" rel="attachment wp-att-5242"><img class="alignnone size-full wp-image-5242" alt="home view from host VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/home_view_from_host.png" width="401" height="311" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Then click on "System Log" and you will see the following:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/view_logs_from_vsphere_client/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/view_logs_from_vsphere_client/']);" rel="attachment wp-att-5243"><img class="alignnone size-full wp-image-5243" alt="view logs from vsphere client VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/view_logs_from_vsphere_client.png" width="1135" height="634" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

You can also choose which logs to look at by choosing the desired log from the drop down menu.

### Generate vCenter Server and ESXi log bundles

The easiest way to do this is from the vSphere client. Login to your vCenter and then select the vCenter (the top icon of the hierarchy on the left). Then go to "File" -> "Export" -> "Export System Logs...". It will look like this:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/export_system_logs_from_vcenter/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/export_system_logs_from_vcenter/']);" rel="attachment wp-att-5244"><img class="alignnone size-full wp-image-5244" alt="export system logs from vcenter VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/export_system_logs_from_vcenter.png" width="609" height="308" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Then the next screen will allow you to choose for which host to generate a log bundle and you can choose to "Include information from vCenter and vSphere Client". Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/generate_host_and_vc_logs/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/generate_host_and_vc_logs/']);" rel="attachment wp-att-5245"><img class="alignnone size-full wp-image-5245" alt="generate host and vc logs VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/generate_host_and_vc_logs.png" width="644" height="526" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

### Use esxcli system syslog to configure centralized logging on ESXi hosts

From "<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples</a>":

> The *esxcli system syslog* command allows you to configure the logging behavior of your ESXi system. With vSphere 5.0, you can manage the top‐level logger and subloggers. The command has the following options.
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxcli_system_syslog_commands/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxcli_system_syslog_commands/']);" rel="attachment wp-att-5246"><img class="alignnone size-full wp-image-5246" alt="esxcli system syslog commands VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxcli_system_syslog_commands.png" width="589" height="333" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a> 

I had configured "Syslog Collector" as per the instructions below and then I ran the following to check the syslog settings on the host:

	  
	~ # esxcli system syslog config get  
	Default Rotation Size: 1024  
	Default Rotations: 8  
	Log Output: /scratch/log  
	Log To Unique Subdirectory: false  
	Remote Host:  
	

Now to see if I can connect to our syslog server over port 514:

	  
	~ # nc -z 192.168.0.121 514  
	~ #  
	

It doesn't look like I can connect to that port.

Now checking out the ESXi firewall and looking for the syslog server, I saw these ports part of the rule:

	  
	~ # esxcli network firewall ruleset rule list -r syslog  
	Ruleset Direction Protocol Port Type Port Begin Port End  
	\---\---\- --\---\---\- --\---\--- \---\---\--- \---\---\---\- --\---\---  
	syslog Outbound UDP Dst 514 514  
	syslog Outbound TCP Dst 514 514  
	syslog Outbound TCP Dst 1514 1514  
	

Now checking if the rule is active and I saw the following:

	  
	~ # esxcli network firewall ruleset list -r syslog  
	Name Enabled  
	\---\--- \---\----  
	syslog false  
	

Looks like it's off, now enabling that rule:

	  
	~ # esxcli network firewall ruleset set --ruleset-id=syslog --enabled=true  
	~ # esxcli network firewall refresh  
	

Now checking to see if I can connect to our syslog server, I see it succeeding:

	  
	~ # nc -z 192.168.0.121 514  
	Connection to 192.168.0.121 514 port [tcp/shell] succeeded!  
	

Now to configure the host to log to the syslog collector server, I ran the following:

	  
	~ # esxcli system syslog config set --loghost='tcp://192.168.0.21:514'  
	~ # esxcli system syslog config get  
	Default Rotation Size: 1024  
	Default Rotations: 8  
	Log Output: /scratch/log  
	Log To Unique Subdirectory: false  
	Remote Host: tcp://192.168.0.21:514  
	~ # esxcli system syslog reload  
	

### Test centralized logging configuration

You can run the following command on the ESXi host to send a test message:

	  
	/var/log # esxcli system syslog mark --message="testing_syslog_config"  
	/var/log # grep testing /var/log/syslog.log  
	2012-12-14T18:49:11Z mark: testing_syslog_config
	
	

Now go to the Machine where Syslog Collector is running and open up Explorer to the following location:

	  
	C:\ProgramData\VMware\VMware Syslog Collector\Data\192.168.0.103  
	

You will see something like this:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_logs-2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_logs-2/']);" rel="attachment wp-att-5259"><img class="alignnone size-full wp-image-5259" alt="syslog collector logs1 VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/syslog_collector_logs1.png" width="796" height="268" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Open up the latest file with notepad and then search for the string that you used and you should see it in that file, like so:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/testing_syslog_collection/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/testing_syslog_collection/']);" rel="attachment wp-att-5260"><img class="alignnone size-full wp-image-5260" alt="testing syslog collection VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/testing_syslog_collection.png" width="861" height="134" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

### Analyze log entries to obtain configuration information

You can check */var/log/syslog* to see how we logged into an iSCSI array. You will see something like this:

	  
	2012-12-14T18:59:58Z iscsid: Login Success: iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb if=default addr=192.168.1.107:3260 (TPGT:1 ISID:0x1)  
	2012-12-14T18:59:58Z iscsid: connection 1:0 (iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb if=default addr=192.168.1.107:3260 (TPGT:1 ISID:0x1) (T0 C0)) is operational  
	

From the above we see that we are connecting to IP "192.168.1.107" and the iqn of the array is "iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb" which is an openIndiana OpenSolaris serving up iSCSI LUNs. Fiber Channel which show similar logins and you can determine the wwnp and wwnn values of the array.

### Analyze log entries to identify and resolve issues

This is a per-issue kind of scenario. It really depends on what you are searching for and what issues you are facing. VMware KB <a href="http://kb.vmware.com/kb/1019238" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1019238']);">1019238</a> has examples of logs snippets to determine why a host restarted. Here is small summary from the KB:

> When a user or script reboots a VMware ESX host, it generates a series events under /var/log/messages similar to:
> 
	>   
	> Mar 9 10:01:49 localhost logger: (1265803308) hb: vmk loaded, 1746.98, 1745.148, 0, 208167, 208167, 0, vmware-h-59580, sfcbd-7660, sfcbd-3524  
	> Mar 9 10:24:42 localhost vmkhalt: (1268148282) Rebooting system...  
	> Mar 9 10:26:13 localhost vmkhalt: (1268148374) Starting system...  
	> Mar 9 10:26:47 localhost logger: (1268148407) loaded VMkernel
	> 
	> Hostd: [2010-03-16 12:51:54.284 27D13B90 info 'TaskManager'] Task Created : haTask-ha-host-vim.HostSystem.reboot-50  
	> 
> 
> Determine if the VMware ESX host was deliberately shut down. When a user or script shuts down a VMware ESX host, it generates a series events similar to:
> 
	>   
	> Mar 9 10:01:49 localhost logger: (1265803308) hb: vmk loaded, 1746.98, 1745.148, 0, 208167, 208167, 0, vmware-h-59580, sfcbd-7660, sfcbd-3524  
	> Mar 9 10:42:34 localhost vmkhalt: (1268149354) Halting system...  
	> Mar 9 10:44:46 localhost vmkhalt: (1268149486) Starting system...  
	> Mar 9 10:45:40 localhost logger: (1268149540) loaded VMkernel  
	> 
> 
> Determine if the ESX host experienced a kernel error. When an ESX host experiences a kernel error, it generates a series of events similar to:
> 
	>   
	> Sep 1 02:01:09 vsphere5 logger: (1251788469) hb: vmk loaded, 3597562.98, 3597450.113, 13, 164009, 164009, 356, vmware-h-79976, vpxa-54148, sfcbd-12600  
	> Sep 1 04:26:35 vsphere5 vmkhalt: (1251797195) Starting system...  
	> Sep 1 04:26:46 vsphere5 logger: (1251797206) VMkernel error  
	> Sep 1 04:27:41 vsphere5 logger: (1251797261) loaded VMkernel  
	> 

### Install and configure VMware syslog Collector and ESXi Dump Collector

Let's do the Syslog Collector First. Start the vCenter Installer. It looks something like this:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/vcenter_installer/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/vcenter_installer/']);" rel="attachment wp-att-5247"><img class="alignnone size-full wp-image-5247" alt="vcenter installer VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vcenter_installer.png" width="689" height="504" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Select "VMware Syslog Collector" and click "Install":

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/select_syslog_collector/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/select_syslog_collector/']);" rel="attachment wp-att-5248"><img class="alignnone size-full wp-image-5248" alt="select syslog collector VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/select_syslog_collector.png" width="686" height="501" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Then the installer will start up, click Next a couple of times and accept the "License Agreement". After that you will get to this screen:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_configuration/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_configuration/']);" rel="attachment wp-att-5249"><img class="alignnone size-full wp-image-5249" alt="syslog collector configuration VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/syslog_collector_configuration.png" width="502" height="375" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Choose the appropriate size and rotation settings for your logs and click Next. After that choose which installation you fall under:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_installation_type/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_installation_type/']);" rel="attachment wp-att-5250"><img class="alignnone size-full wp-image-5250" alt="syslog collector installation type VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/syslog_collector_installation_type.png" width="500" height="375" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Then keep the default port settings:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_port_settings/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_collector_port_settings/']);" rel="attachment wp-att-5251"><img class="alignnone size-full wp-image-5251" alt="syslog collector port settings VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/syslog_collector_port_settings.png" width="499" height="376" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Then click Next and then Finish. After that you will see the service starts under "services.msc":

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_service_started/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/syslog_service_started/']);" rel="attachment wp-att-5252"><img class="alignnone size-full wp-image-5252" alt="syslog service started VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/syslog_service_started.png" width="671" height="68" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

You can also check if the ports are in a listening state on the windows machine:

	  
	C:\Users\Administrator>netstat -ab | findstr 514  
	TCP 0.0.0.0:514 WIN-2K5GMV25I0E:0 LISTENING  
	TCP 0.0.0.0:1514 WIN-2K5GMV25I0E:0 LISTENING  
	UDP 0.0.0.0:514 *:*  
	

Now you can configure hosts to log to this syslog collector. This setup for that was covered in previous objectives

The ESXi Dump collector is very similar. Start up the vCenter installer and then follow the on-screen instructions. This <a href="http://blogs.vmware.com/vsphere/2011/07/setting-up-the-esxi-50-dump-collector.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2011/07/setting-up-the-esxi-50-dump-collector.html']);">VMware</a> Blog has a very good step-by-step guide. Here is the content from that blog:

> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/vcenter_install_dump_collector/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/vcenter_install_dump_collector/']);" rel="attachment wp-att-5266"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vcenter_install_dump_collector.png" alt="vcenter install dump collector VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="757" height="554" class="alignnone size-full wp-image-5266" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a> 

During the install you will be asked where on the host you want to store the core dumps, by default the dump repository is 2GB, which should be sufficient for most environments.

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/dump_collector_install_size/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/dump_collector_install_size/']);" rel="attachment wp-att-5267"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dump_collector_install_size.png" alt="dump collector install size VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="698" height="519" class="alignnone size-full wp-image-5267" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

You will also be asked if you want to do a Standalone installation or integrate the dump collector with vCenter. If you choose the VMware vCenter Server Installation it will register the Dump Collector plug-in with the vCenter server.

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/dump_collector_install_type/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/dump_collector_install_type/']);" rel="attachment wp-att-5268"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/dump_collector_install_type.png" alt="dump collector install type VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="697" height="521" class="alignnone size-full wp-image-5268" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

The final step is to use the ESXCLI to configure each host to use the Dump Collector. The screen shot below shows the commands to do this.

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxcli_core_dump/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/esxcli_core_dump/']);" rel="attachment wp-att-5269"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxcli_core_dump.png" alt="esxcli core dump VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="938" height="254" class="alignnone size-full wp-image-5269" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

Now anytime your ESXi 5.0 host generates a core dump the file will be saved on the network server and available for analysis. The screen shots below show the file being copied to the network server when my ESXi host PSODs. I also provided a listing of the corefile for reference.

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/psod_dump_collector/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/psod_dump_collector/']);" rel="attachment wp-att-5270"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/psod_dump_collector.png" alt="psod dump collector VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="876" height="358" class="alignnone size-full wp-image-5270" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/ls_core_dump/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/ls_core_dump/']);" rel="attachment wp-att-5271"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/ls_core_dump.png" alt="ls core dump VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " width="847" height="119" class="alignnone size-full wp-image-5271" title="VCAP5 DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files " /></a>

