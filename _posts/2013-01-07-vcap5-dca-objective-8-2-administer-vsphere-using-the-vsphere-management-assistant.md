---
title: VCAP5-DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/
dsq_thread_id:
  - 1411740703
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify vMA prerequisites

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

> **Hardware Requirements**  
> To set up vMA, you must have an ESXi host. Because vMA runs a 64‐bit Linux guest operating system, the ESXi host on which it runs must support 64‐bit virtual machines.  
> The ESXi host must have one of the following CPUs:
> 
> *   AMD Opteron, rev E or later
> *   Intel processors with EM64T support with VT enabled.
> 
> Opteron 64‐bit processors earlier than rev E, and Intel processors that have EM64T support but do not have VT support enabled, do not support a 64‐bit guest operating system.
> 
> By default, vMA uses one virtual processor, and requires 3GB of storage space for the vMA virtual disk. The recommended memory for vMA is 600MB.
> 
> **Software Requirements **  
> You can deploy vMA on the following systems:
> 
> *   vSphere 5.1
> *   vSphere 5.0 and later
> *   vSphere 4.1 and later
> *   vCenter Application 5.0 and later
> 
> You can deploy vMA by using a vSphere Client connected to an ESXi host or by using a vSphere Client connected to vCenter Server 5.1, vCenter Server 5.0 or later, vCenter Server 4.1 or later, or vCenter Application 5.0 and later.
> 
> You can use vMA to target vSphere 4.1 and later, vSphere 5.0 and later, and vSphere 5.1 systems.
> 
> At runtime, the number of targets a single vMA instance can support depends on how it is used.

### Identify vMA specific commands

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_commands/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_commands/']);" rel="attachment wp-att-5580"><img class="alignnone size-full wp-image-5580" alt="vma commands VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_commands.png" width="605" height="246" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

### Determine when vMA is needed

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

> vMA Capabilities  
> vMA provides a flexible and authenticated platform for running scripts and programs.
> 
> *   As administrator, you can add vCenter Server systems and ESXi hosts as targets and run scripts and programs on these targets. Once you have authenticated while adding a target, you need not login again while running a vSphere CLI command or agent on any target.
> *   As a developer, you can use the APIs provided with the VmaTargetLib library to programmatically connect to vMA targets by using Perl or Java.
> *   vMA enables reuse of service console scripts that are currently used for ESXi administration, though minor modifications to the scripts are usually necessary.
> *   vMA comes preconfigured with two user accounts, namely, vi‐admin and vi‐user. 
>     *   As vi‐admin, you can perform administrative operations such as addition and removal of targets. You can also run vSphere CLI commands and agents with administrative privileges on the added targets.
>     *   As vi‐user, you can run the vSphere CLI commands and agents with read‐only privileges on the target.
> *   You can make vMA join an Active Directory domain and log in as an Active Directory user.When you run commands from such a user account, the appropriate privileges given to the user on the vCenter Server system or the ESXi host would be applicable.
> *   vMA can run agent code that make proprietary hardware or software components compatible with VMware ESX. These code currently run in the service console of existing ESX hosts. You can modify most of these agent code to run in vMA, by calling the vSphere API, if necessary. Developers must move any agent code that directly interfaces with hardware into a provider.

So if you want to have a centralized management console, vMA is perfect. You can write script from one location and then apply it to multiple hosts at the same time. You can also create multiple user or join the vMA to a domain and keep track who logged in at what time.

### Install and configure vMA

I decided to install the 5.1 version of VMa just for fun. First download the zip file from My VMware:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_download/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_download/']);" rel="attachment wp-att-5576"><img class="alignnone size-full wp-image-5576" alt="vma download VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_download.png" width="988" height="614" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Then from "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>"::

> **To deploy vMA**
> 
> 1.  Use a vSphere Client to connect to a system that is running the supported version of ESXi or vCenter Server.
> 2.  If connected to a vCenter Server system, select the host to which you want to deploy vMA in the inventory pane.
> 3.  Select File > Deploy OVF Template.The Deploy OVF Template wizard appears.
> 4.  Select Deploy from a file or URL if you have already downloaded and unzipped the vMA virtual appliance package.
> 5.  Click Browse, select the OVF, and click Next.
> 6.  Click Next when the OVF template details are displayed.
> 7.  Accept the license agreement and click Next.
> 8.  Specify a name for the virtual machine.You can also accept the default virtual machine name.
> 9.  Select an inventory location for the virtual machine when prompted.If you are connected to a vCenter Server system, you can select a folder.
> 10. If connected to a vCenter Server system, select the resource pool for the virtual machine.By default, the top‐level root resource pool is selected.
> 11. If prompted, select the datastore to store the virtual machine on and click Next.
> 12. Select the required disk format option and click Next.
> 13. Select the network mapping and click Next.
> 14. Review the information and click Finish.
> 
> The wizard deploys the vMA virtual machine to the host that you selected. The deploy process can take several minutes

Here is how what I did to deploy the vMA. After you downloaded from the above site, you will see the following file:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_zip_file/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_zip_file/']);" rel="attachment wp-att-5581"><img class="alignnone size-full wp-image-5581" alt="vma zip file VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_zip_file.png" width="90" height="89" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

After extracting the archive, you will see the following files:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/zip_extracted_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/zip_extracted_vma/']);" rel="attachment wp-att-5582"><img class="alignnone size-full wp-image-5582" alt="zip extracted vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/zip_extracted_vma.png" width="588" height="100" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Now to deploy the 'ovf', we can go to "File -> Deploy OVF Template":

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_template/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_template/']);" rel="attachment wp-att-5583"><img class="alignnone size-full wp-image-5583" alt="deploy ovf template VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/deploy_ovf_template.png" width="237" height="96" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Browsing to our ovf and selecting it, we get this from vCenter:  
<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_template_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_template_vma/']);" rel="attachment wp-att-5584"><img class="alignnone size-full wp-image-5584" alt="deploy ovf template vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/deploy_ovf_template_vma.png" width="714" height="676" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Keep Clicking through the Deployment Wizard:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_vma_wizard/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/deploy_ovf_vma_wizard/']);" rel="attachment wp-att-5585"><img class="alignnone size-full wp-image-5585" alt="deploy ovf vma wizard VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/deploy_ovf_vma_wizard.png" width="716" height="676" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

At end the final screen will look like this:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/final_screen_ovf_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/final_screen_ovf_vma/']);" rel="attachment wp-att-5586"><img class="alignnone size-full wp-image-5586" alt="final screen ovf vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/final_screen_ovf_vma.png" width="718" height="675" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

After the VM is Deployed, you will see it in the inventory:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_vm_vc_inventory/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_vm_vc_inventory/']);" rel="attachment wp-att-5587"><img class="alignnone size-full wp-image-5587" alt="vma vm vc inventory VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_vm_vc_inventory.png" width="196" height="95" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Next we can Power on the VM and open Console to it. And per the instructions from the guide:

> **Configure vMA at First Boot**  
> When you start the vMA virtual machine the first time, you can configure it.  
> **To configure vMA**
> 
> 1.  In the vSphere Client, right‐click the virtual machine, and click Power On.
> 2.  Select the Console tab.
> 3.  Select the appropriate menu option to configure the network settings.You can individually configure the various network settings such as IP address, host name, DNS, proxy server, and default gateway, by selecting the appropriate menu option.The host name can contain 64 alphanumeric characters. You can change the vMA host name later by modifying the /etc/HOSTNAME and /etc/hosts files, as you would for a Linux host. You can also use the vMA console to change the host name. For a DHCP configuration, the host name is obtained from the DNS server.If you use a static IPv4 network configuration to configure the IP address, DNS, default gateway, and hostname, then you must also configure a default IPv6 gateway during the first‐boot network configuration, else the vMA might be unreachable in the network after login.Ensure that you complete the network configuration at the first boot. If you skip the network configuration, the appliance takes the default network configuration from the guest operating system, which may lead to some inconsistencies.
> 4.  When prompted, specify a password for the vi‐admin user.If prompted for an old password, press Enter and continue.The new password must conform to the vMA password policy. The password must have at least: 
>     *   Nine characters
>     *   One upper case character
>     *   One lower case character
>     *   One numeral character
>     *   One symbol such as #, $You can later change the password for the vi‐admin user using the Linux passwd command.This user has root privileges.
> 
> vMA is now configured and the vMA console appears. The console displays the URL from which you can access the Web UI.

Here is how it looked like on first boot:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/first_boot_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/first_boot_vma/']);" rel="attachment wp-att-5589"><img class="alignnone size-full wp-image-5589" alt="first boot vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/first_boot_vma.png" width="725" height="498" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Here is how you can set the IP for the vMA:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/ip_conf_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/ip_conf_vma/']);" rel="attachment wp-att-5590"><img class="alignnone size-full wp-image-5590" alt="ip conf vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/ip_conf_vma.png" width="727" height="496" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

After the boot up process is finished, you will see the following screen on the vMA VM:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_finish_boot.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_finish_boot.png']);" rel="attachment wp-att-5591"><img class="alignnone size-full wp-image-5591" alt="vma finish boot VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_finish_boot.png" width="728" height="500" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Also visiting the management console from the Browser, I saw the following:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_browser/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_browser/']);" rel="attachment wp-att-5592"><img class="alignnone size-full wp-image-5592" alt="vma browser VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_browser.png" width="703" height="368" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Upon logging into the vMA, I the following screen:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_browser_login/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_browser_login/']);" rel="attachment wp-att-5593"><img class="alignnone size-full wp-image-5593" alt="vma browser login VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_browser_login.png" width="830" height="310" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

I tried to login to the vMA via ssh, but I kept the following error in putty:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_ssh_fail/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_ssh_fail/']);" rel="attachment wp-att-5594"><img class="alignnone size-full wp-image-5594" alt="vma ssh fail VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_ssh_fail.png" width="662" height="407" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

I logged in via the VM Console and checked out the messages file and I saw the following:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/tcp_wrappers_vma_login/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/tcp_wrappers_vma_login/']);" rel="attachment wp-att-5595"><img class="alignnone size-full wp-image-5595" alt="tcp wrappers vma login VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " src="http://virtuallyhyper.com/wp-content/uploads/2012/12/tcp_wrappers_vma_login.png" width="727" height="499" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Checking out the file and that line, I saw the following:

	  
	localhost:~ # tail -n +64 /etc/hosts.allow  
	ALL: KNOWN  
	

Then checking out the deny file:

	localhost:~ #cat /etc/hosts.deny
	# /etc/hosts.deny
	# See 'man tcpd' and 'man 5 hosts_access' as well as /etc/hosts.allow
	# for a detailed description.
	http-rman : ALL EXCEPT LOCAL
	ALL: ALL  

Looks like we are blocking everything. So I just moved the 'hosts.deny' file out of the way:

	  
	localhost:~ # mv /etc/hosts.deny /tmp  
	

And then I was able to ssh to the machine with putty without issues:

	  
	Using username 'vi-admin'.  
	Welcome to vSphere Management Assistant  
	vi-admin'@'192.168.2.109's password:  
	Last login: Mon Dec 24 23:30:02 2012 from 192.168.2.110  
	vi-admin'@'localhost:~>  
	

### Add/Remove target servers

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

> **Add Target Servers to vMA**  
> After you configure vMA, you can add target servers that run the supported vCenter Server or ESXi version.  
> For vCenter Server and ESXi system targets, you must have the name and password of a user who can connect to that system.
> 
> **To add a vCenter Server system as a vMA target for Active Directory Authentication**
> 
> 1.  Log in to vMA as vi‐admin.
> 2.  Add a server as a vMA target by running the following command:  
>	       
>	     vifp addserver vc1.mycomp.com --authpolicy adauth --username ADDOMAIN\\user1  
>
>     Here, **-authpolicy** adauth indicates that the target needs to use the Active Directory authentication.If you run this command without the -username option, vMA prompts for the name of the user that can connect to the vCenter Server system. You can specify this user name as shown in the following example:
>     
>	     Enter username for machinename.example.com: ADDOMAIN\user1  
>     
>     If **-authpolicy** is not specified in the command, then fpauth is taken as the default authentication  
>     policy.
>
> 3.  Verify that the target server has been added.  
>         The display shows all target servers and the authentication policy used for each target.  
>	           
>	         vifp listservers --long  
>	         server1.mycomp.com ESX adauth  
>	         server2.mycomp.com ESX fpauth  
>	         server3.mycomp.com ESXi adauth  
>	         vc1.mycomp.com vCenter adauth  
>	         
> 4.  Set the target as the default for the current session:  
>	           
>	         vifptarget --set | -s  
>	         
> 5. Verify that you can run a vSphere CLI command without authentication by running a command on one of the ESXi hosts, for example:  
>	           
>	         esxcli --server <VC_server> --vihost <esx_host> network nic list  
>
>  The command runs without prompting for authentication information

Here is how adding vCenter to the vMA looks like:

	vi-admin'@'localhost:~> vifp addserver 192.168.2.110 --username administrator  
	administrator'@'192.168.2.110's password:  
	This will store username and password in credential store which is a security risk. Do you want to continue?(yes/no): yes  
	vi-admin'@'localhost:~> vifp listservers --long  
	192.168.2.110 vCenter fpauth  

Now you can either add the hosts to the vMA or manage the hosts by using vCenter. To manage the host via vCenter from the vMA you must know the name of the hosts. There is actually a communities <a href="http://communities.vmware.com/thread/321162" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/321162']);">thread</a> on this. If you want to list the hosts connected to the vCenter from vMA you can use the script that is provided in the communities page. Here is how it looks like:

	vi-admin'@'localhost:~> vi gethosts.pl  
	vi-admin'@'localhost:~> chmod +x gethosts.pl  
	vi-admin'@'localhost:~> ./gethosts.pl --server 192.168.2.110 --username administrator  
	Enter password:  
	ESX(i) hosts residing on 192.168.2.110  
	192.168.0.103 VMware ESXi 5.0.0 build-623860  
	192.168.0.101 VMware ESXi 4.1.0 build-348481  
	192.168.0.104 VMware ESX 4.0.0 build-208167  

So now if I wanted to list all the nfs mounts on my 5.0 host by going through the vCenter, I can do this:

	vi-admin'@'localhost:~> esxcli -s 192.168.2.110 -h 192.168.0.103 -u administrator storage nfs list  
	Enter password:  
	Volume Name Host Share Accessible Mounted Hardware Acceleration
	========== ==== ==== ======== ====== ======= =========
	nfs 192.168.1.107 /data/nfs_share true true Not Supported  


Notice that I had to type in the admin password to login to the VC. Since I saved the credentials, I can actually use fastpath to connect to the vCenter and from there when I run commands it will automatically run against the vCenter. Here is what we have to do to accomplish that:

	vi-admin'@'localhost:~> vifp listservers -l  
	192.168.2.110 vCenter fpauth  
	vi-admin'@'localhost:~> vifptarget -s 192.168.2.110  
	vi-admin'@'localhost:~[192.168.2.110]> esxcli -h 192.168.0.103 storage nfs list  
	Volume Name Host Share Accessible Mounted Hardware Acceleration
	========== ==== ==== ======== ====== ======= =========
	nfs 192.168.1.107 /data/nfs_share true true Not Supported  

Notice that my prompt changes to the server that I am authenticated against and also notice that I didn't have to type in the password because I am using fastpass. To leave that server from fastpass we can do the following:

	vi-admin'@'localhost:~[192.168.2.110]> vifptarget -c  
	vi-admin'@'localhost:~>  

Notice how my prompt changed again.

### Perform updates to the vMA

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

> **Update vMA**  
> You can download software updates including security fixes fromVMware and components included in vMA, such as the SUSE Linux Enterprise Server updates and JRE.
> 
> **To update vMA**
> 
> 1.  Access the Web UI.
> 2.  Log in as vi‐admin.
> 3.  Click the Update tab and then the Status tab.
> 4.  Open the Settings tab and then from the Update Repository section, select a repository.
> 5.  Click Check Updates.
> 6.  Click Install Updates.

Here is how it looks like from the web browser:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_update_page/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/vma_update_page/']);" rel="attachment wp-att-5608"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/vma_update_page.png" alt="vma update page VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " width="837" height="242" class="alignnone size-full wp-image-5608" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

Then checking out the Repository settings:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/repository_settings_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/repository_settings_vma/']);" rel="attachment wp-att-5609"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/repository_settings_vma.png" alt="repository settings vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " width="830" height="544" class="alignnone size-full wp-image-5609" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>

The settings looked good, then going back to the status page and Clicking "Check Updates" nothing came up since this was the latest version at the time.

### Use vmkfstools to manage VMFS datastores

vmkfstools has the same options as on the host itself. In my example I will use vMA to create a VMFS datastore with vmkfstools. I have presented two LUNs from my OpenIndiana VM to my 5.0 ESXi host. Lun0 is 100GB and LUN1 is 130GB. Lun0 already had VMFS on it and LUN1 is blank. So first let's see if we can see the LUNS:


	vi-admin@localhost:~> vifp listservers -l  
	192.168.2.110 vCenter fpauth  
	vi-admin'@'localhost:~> vifptarget -s 192.168.2.110  
	vi-admin'@'localhost:~[192.168.2.110]> esxcfg-scsidevs -h 192.168.0.103 -c | grep OI  
	naa.600144f0928c010000004fc90a3a0001 disk /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001 133120MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc90a3a0001)  
	naa.600144f0928c010000004fc511ec0001 disk /vmfs/devices/disks/naa.600144f0928c010000004fc511ec0001 102400MB NMP OI iSCSI Disk (naa.600144f0928c010000004fc511ec0001)  


Those are my 2 LUNs. Now checking out the VMFS datastores, I see the following:

	vi-admin@localhost:~[192.168.2.110]> esxcli -h 192.168.0.103 storage filesystem list | grep VMFS  
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e OI_LUN0 4fc903bb-6298d17d-8417-00505617149e true VMFS-3 107105746944 102479429632  
	/vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb datastore1 4fc3c05b-c677ee28-ba3c-0050561712cb true VMFS-5 63350767616 58986594304  

So the bottom one is the local drive with VMFS5 and the top on is LUN0 of size 100GB with VMFS3 on it. First we need to create a gpt partition table on the LUN. First let's see what information partedUtil can see (this has to be done directly from the host):

	~ # partedUtil getptbl /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001  
	msdos  
	16970 255 63 272629760  


From VMware KB <a href="http://kb.vmware.com/kb/1036609" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1036609']);">1036609</a>:

> The first line is only present in the getptbl form of the command, and displays the disk label identifying the partitioning scheme being used. Common labels are bsd, dvh, gpt, loop, mac, msdos, pc98, and sun. Of these, only the msdos label and vFAT partitioning scheme is used by ESXi/ESX.
> 
> Note: The label msdos does not mean that the device contains a Windows file system or is being used by a Windows machine. It only means that it is a MBR (Master Boot Record) partition.
> 
> The second line displays the disk geometry information read from the underlying device:  
>   
> 17834 255 63 286513152  
> | | | |  
> | | | ----- quantity of sectors  
> | | -------- quantity of sectors per track  
> | ------------ quantity of heads  
> ------------------ quantity of cylinders  


So we have no partitions defined and currently it has an 'msdos' disklabel. Since we are going to create a VMFS-5 volume we will change that to GPT. Also converting the sectors to GB, we get the following:

	(272629760 * 512 / 1024 /1024 /1024) = 130 GB  


That matches our LUN1 size. From the KB here is what is necessary to create a gpt partition:

> For ESXi/ESX 4.1 and later, use the command:  
>   
> partedUtil setptbl '/vmfs/devices/disks/DeviceName' DiskLabel ['partNum startSector endSector type/guid attribute']*  
>  

And here is information regarding all the parameters:

> The **disk label** is only specified in the setptbl form of the command, and sets the disk label identifying the partitioning scheme being used. Common labels are bsd, dvh, gpt, loop, mac, msdos, pc98, and sun. ESXi 5.0 and higher supports both the msdos and gpt label and partitioning schemes, while ESXi/ESX 4.1 and earlier supports the msdos label and partitioning scheme exclusively. 

In our case we will have "gpt" for *DiskLabel*. Moving down the KB we have:

> The list of partitions to apply to the disk must be fully specified on the partedUtil command line. To add additional partitions to a disk with an existing partition, specify both the original and new partitions on the command line. If you do not, the existing partition is lost. The list of partitions are specified as quoted strings, each of which encapsulates a 5-tuple composed of the partition number, starting sector, ending sector, type ID, and attributes: 

Since we want to create just one partition, we will use a value of '1' for *partNum*. Next we have the following:

> The startSector and endSector specify how much contiguous disk space a partition occupies. The starting sector is enforced to be before the ending sector for the same partition, but no guarantee is made that the partition defined does not overlap another partition. 

Our *startSector* will be '2048', since that is the offset for a VMFS-5 partition:

> Volumes that are upgraded from VMFS-3 to VMFS-5 continue to have the VMFS partition starting at sector 128, rather than at sector 2048. 

Since we are taking up the whole partition the *endSector* will be the last sector of usable space. We can check that by running the following:

	~ # partedUtil getUsableSectors /dev/disks/naa.600144f0928c010000004fc90a3a0001  
	1 272629759  

So our *endSector* will be '272629759'. If we keep going:

> The partition type identifies the purpose of a partition, and may be represented by either a a decimal identifier (for example, 251) or a UUID (for example, AA31E02A400F11DB9590000C2911D1B8). Partitions created on ESXi 5.0 and higher with the gpt disklabel must be specified using the GUID. 

To see the full list we can do the following:

	~ # partedUtil showGuids  
	Partition Type GUID  
	vmfs AA31E02A400F11DB9590000C2911D1B8  
	vmkDiagnostic 9D27538040AD11DBBF97000C2911D1B8  
	VMware Reserved 9198EFFC31C011DB8F78000C2911D1B8  
	Basic Data EBD0A0A2B9E5443387C068B6B72699C7  
	Linux Swap 0657FD6DA4AB43C484E50933C84B4F4F  
	Linux Lvm E6D6D379F50744C2A23C238F2A3DF928  
	Linux Raid A19D880F05FC4D3BA006743F0F84911E  
	Efi System C12A7328F81F11D2BA4B00A0C93EC93B  
	Microsoft Reserved E3C9E3160B5C4DB8817DF92DF00215AE  
	Unused Entry 00000000000000000000000000000000  

We are going to be using VMFS so our '*type/guid*' will be "AA31E02A400F11DB9590000C2911D1B8". And lastly:

> The partition attribute is a number which identifies properties of the partition. A common attribute is 128 = 0x80, which indicates that the partition is bootable. Otherwise, most partitions have an attribute value of 0. 

Since we are not going to boot from our VMFS volume, our *attribute* will be '0'. Now putting everything together, we get the following:

	partedUtil setptbl /dev/disks/naa.600144f0928c010000004fc90a3a0001 gpt '1 2048 272629759 AA31E02A400F11DB9590000C2911D1B8 0'  

Let's see what happens when we run it:

	~ # partedUtil setptbl /dev/disks/naa.600144f0928c010000004fc90a3a0001 gpt '1 2048 272629759 AA31E02A400F11DB9590000C2911D1B8 0'  
	gpt  
	0 0 0 0  
	1 2048 272629759 AA31E02A400F11DB9590000C2911D1B8 0  
	Error: Unable to satisfy all constraints on the partition.  


Looks like it failed. Since I had an msdos disklabel, I decided to first change it to GPT and see if that helps out:

	~ # partedUtil mklabel /dev/disks/naa.600144f0928c010000004fc90a3a0001 gpt  
	~ # partedUtil getptbl /dev/disks/naa.600144f0928c010000004fc90a3a0001  
	gpt  
	16970 255 63 272629760  

That looks better. Now checking the usable sectors again:

	~ # partedUtil getUsableSectors /dev/disks/naa.600144f0928c010000004fc90a3a0001  
	34 272629726  

My last usable sector is different, so changing my command and running it, I got the following:

	~ # partedUtil setptbl /dev/disks/naa.600144f0928c010000004fc90a3a0001 gpt '1 2048 272629726 AA31E02A400F11DB9590000C2911D1B8 0'  
	gpt  
	0 0 0 0  
	1 2048 272629726 AA31E02A400F11DB9590000C2911D1B8 0  
	~ # partedUtil getptbl /dev/disks/naa.600144f0928c010000004fc90a3a0001  
	gpt  
	16970 255 63 272629760  
	1 2048 272629726 AA31E02A400F11DB9590000C2911D1B8 vmfs 0  

That looks much better, now back to our vMA console and to create our VMFS-5 Datastore.


	vi-admin'@'localhost:~[192.168.2.110]> vmkfstools -h 192.168.0.103 -C vmfs5 /vmfs/devices/disks/naa.600144f0928c010000004fc90a3a0001:1 -S OI_LUN1

	Creating vmfs5 file system on naa.600144f0928c010000004fc90a3a0001:1 with blockSize 1048576 and volume label OI_LUN1

	Successfully created new volume:50da04db-949786bb-eece-0050561712cb  
	vi-admin'@'localhost:~[192.168.2.110]> esxcli -h 192.168.0.103 storage filesystem list | grep VMFS  
	/vmfs/volumes/4fc903bb-6298d17d-8417-00505617149e OI_LUN0 4fc903bb-6298d17d-8417-00505617149e true VMFS-3 107105746944 102479429632  
	/vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb datastore1 4fc3c05b-c677ee28-ba3c-0050561712cb true VMFS-5 63350767616 58986594304  
	/vmfs/volumes/50da04db-949786bb-eece-0050561712cb OI_LUN1 50da04db-949786bb-eece-0050561712cb true VMFS-5 139318001664 138299834368  

That looks good.

### Use vmware-cmd to manage VMs

The commands are the same as they were before, here is a list of options:

	vi-admin@localhost:~[192.168.2.110]> vmware-cmd  
	Usage: vmware-cmd <options> <vm-cfg-path> <vm-action> <arguments>  
	vmware-cmd -s <options> <server-action> <arguments>

	Options:
	Connection Options:
	-H or --server <host>            specifies an ESX host or a vCenter Server
	-h or --vihost <target host>     specifies a target host if host is a virtual center
	-O <port>                        specifies an alternative port
	-Q <protocol>                    specifies an alternative protocol
	-U or --username <username>      specifies a username
	-P or --password <password>      specifies a password
	--sessionfile                    specifies a sessionfile path
	--passthroughauth                specifies a login by sspi option
	--credstore                      specifies to fetch Credential store information
	--encoding                       specifies encoding option
	General Options:
	-h More detailed help.
	-q Quiet. Minimal output
	-v Verbose.

	Server Operations:
	vmware-cmd -l
	vmware-cmd -s register <config_file_path> <datacenter> <resource pool>
	vmware-cmd -s unregister <config_file_path>

	VM Operations:
	vmware-cmd <cfg> getstate
	vmware-cmd <cfg> start <powerop_mode>
	vmware-cmd <cfg> stop <powerop_mode>
	vmware-cmd <cfg> reset <powerop_mode>
	vmware-cmd <cfg> suspend <powerop_mode>
	vmware-cmd <cfg> setguestinfo <variable> <value>
	vmware-cmd <cfg> getguestinfo <variable>
	vmware-cmd <cfg> getproductinfo <prodinfo>
	vmware-cmd <cfg> connectdevice <device_name>
	vmware-cmd <cfg> disconnectdevice <device_name>
	vmware-cmd <cfg> getconfigfile
	vmware-cmd <cfg> getuptime
	vmware-cmd <cfg> answer
	vmware-cmd <cfg> gettoolslastactive
	vmware-cmd <cfg> hassnapshot
	vmware-cmd <cfg> createsnapshot <name> <description> <quiesce> <memory>
	vmware-cmd <cfg> revertsnapshot
	vmware-cmd <cfg> removesnapshots

So let's list the VMs currently registered on our 5.0 host and check the state of each VM:

	vi-admin@localhost:~[192.168.2.110]> vmware-cmd -h 192.168.0.103 -l

	/vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb/test/test.vmx  
	/vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb/vMA5_1/vMA5_1.vmx  


Now to check the state of the VMs:

	vi-admin'@'localhost:~[192.168.2.110]> vmware-cmd -h 192.168.0.103 /vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb/test/test.vmx getstate  
	getstate() = off  
	vi-admin'@'localhost:~[192.168.2.110]> vmware-cmd -h 192.168.0.103 /vmfs/volumes/4fc3c05b-c677ee28-ba3c-0050561712cb/vMA5_1/vMA5_1.vmx getstate  
	getstate() = on  

You can obviously power on and off any VMs that you want with the vmware-cmd command, if you just follow the options that are available.

### Use esxcli to manage ESXi Host configurations

Any command that you can use on the host with esxcli you can do from the vMA as well. Here is a list of all the available options:

	vi-admin@localhost:~[192.168.2.110]> esxcli -h 192.168.0.103  
	Usage: esxcli 

	Available Namespaces:  
	esxcli 		Commands that operate on the esxcli system itself allowing users to get additional information.  
	fcoe 		VMware FCOE commands.  
	hardware 	VMKernel hardware properties and commands for  configuring hardware.  
	iscsi 		VMware iSCSI commands.  
	network 	Operations that pertain to the maintenance of   networking on an ESX host. This includes a wide  variety of commands to manipulate virtual networking  components (vswitch, portgroup, etc) as well as local  host IP, DNS and general host networking settings.  
	software 	Manage the ESXi software image and packages  
	storage 	VMware storage commands.  
	system 		VMKernel system properties and commands for configuring properties of the kernel core system.  
	vm		A small number of operations that allow a user to Control Virtual Machine operations.  

Most of these were covered throughout the whole blue print.

### Troubleshoot common vMA errors and conditions

From "<a href="http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-51/topic/com.vmware.ICbase/PDF/vma_51_guide.pdf']);">vSphere Management Assistant Guide vSphere 5.1</a>":

> **Troubleshooting vMA**  
> You can find troubleshooting information for all VMware products in VMware Knowledge Base articles and information about vMA known issues in the release notes. Table 2‐3 explains a few commonly encountered issues that are easily resolved.
> 
> <a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/troubleshooting_vma/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-8-2-administer-vsphere-using-the-vsphere-management-assistant/troubleshooting_vma/']);" rel="attachment wp-att-5610"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/troubleshooting_vma.png" alt="troubleshooting vma VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " width="592" height="491" class="alignnone size-full wp-image-5610" title="VCAP5 DCA Objective 8.2 – Administer vSphere Using the vSphere Management Assistant " /></a>
> 
> This release of vMA provides the vma-support script that enables you to collect various system configuration information and other logs. You can run this script by issuing the following command:  
>
> 	sudo vma-support  
>
> The script generates the information and log bundle and appends it to the vmware.log file on the ESXi host on which vMA is deployed. 
