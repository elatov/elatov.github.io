---
title: Installing OpenVZ on CentOS 6 in an ESXi 5 VM
author: Jarret Lavallee
layout: post
permalink: /2012/08/installing-openvz-on-centos-6-in-an-esxi-5-vm/
dsq_thread_id:
  - 1404672911
categories:
  - Home Lab
  - VMware
tags:
  - hypervisor
  - nested
  - openvz
  - selinux
  - sysctl
  - vzctl
---
After <a href="http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/']);" title="Installing KVM as a Virtual Machine on ESXi 5 with Bridged Networking">installing KVM</a>, I wanted to try out some other hypervisors that are common. I have owned multiple <a href="http://wiki.openvz.org/Main_Page" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.openvz.org/Main_Page']);" target="_blank">OpenVZ</a> VPS&#8217;s. In fact this site is currently hosted on one. OpenVZ was one of the easiest deployments yet. The technology is very cool, but more limited than the other hypervisors. I would suggest reading the <a href="http://wiki.openvz.org/Quick_installation" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.openvz.org/Quick_installation']);" target="_blank">quick start guide</a>. The information below is how I installed it.

The first thing we need to do is install CentOS 6 in a <a href="http://www.vladan.fr/vmware-vsphere-5-virtual-machine-hardware-version-8/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vladan.fr/vmware-vsphere-5-virtual-machine-hardware-version-8/']);" target="_blank">hardware version 8 VM</a> on the ESXi host. Make sure that the VM is attached to a port group in <a href="http://kb.vmware.com/kb/1004099" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004099']);" target="_blank">promiscuous mode</a>.

## Configuring the ESXi 5 VM for OpenVZ

As per <a href="http://communities.vmware.com/docs/DOC-8970" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-8970']);" target="_blank">this article</a>, we can set some options in the VMX to allow nested hypervisors. Append the following lines to the VMX file after the VM has been shut down.

[code]  
cpuid.1.ecx=&quot;\----:\----:\----:\----:\----:\----:--h-:\----&quot;  
cpuid.80000001.ecx.amd=&quot;\----:\----:\----:\----:\----:\----:\----:-h--&quot;  
cpuid.8000000a.eax.amd=&quot;hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh&quot;  
cpuid.8000000a.ebx.amd=&quot;hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh&quot;  
cpuid.8000000a.edx.amd=&quot;hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh&quot;  
monitor.virtual_mmu = &quot;hardware&quot;  
monitor.virtual_exec = &quot;hardware&quot;  
[/code]

Now we need to reload the VMX file so the host acknowledges the new changes. We will do this with the <a href="http://kb.vmware.com/kb/1026043" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026043']);" target="_blank">vim-cmd command</a>. 

[code]  
\# vim-cmd vmsvc/getallvms |grep openvz1  
254 openvz1 [iscsi\_dev] openvz1/openvz1.vmx rhel6\_64Guest vmx-08  
\# vim-cmd vmsvc/reload 254  
\# vim-cmd vmsvc/power.on 254  
Powering on VM:  
[/code]

## Installing OpenVZ

Now we can log into the VM and start configuring OpenVZ. The first thing we should do is add the openVZ repo. 

[code]  
\# wget http://download.openvz.org/openvz.repo  
\# mv openvz.repo /etc/yum.repos.d/  
\# rpm --import http://download.openvz.org/RPM-GPG-Key-OpenVZ  
\# yum update  
[/code]

Now we can install the vzkernel and reboot into it.  
[code]  
\# yum install vzkernel  
\# reboot  
[/code]

After the reboot we should confirm that we are running on the right kernel.  
[code]  
\# uname -a  
Linux openvz1 2.6.32-042stab057.1 #1 SMP Fri Jun 22 02:17:07 MSD 2012 x86\_64 x86\_64 x86_64 GNU/Linux  
[/code]

Now we install the OpenVZ tools.

[code]  
\# yum install vzctl vzquota -y  
[/code]

We need to change some kernel parameters for OpenVZ to work correctly. Open up the /etc/sysctl.conf and change/append the following lines.

[code]  
net.ipv4.ip_forward = 1  
net.ipv4.conf.default.proxy_arp = 0  
net.ipv4.conf.all.rp_filter = 1  
kernel.sysrq = 1  
net.ipv4.conf.default.send_redirects = 1  
net.ipv4.conf.all.send_redirects = 0  
net.ipv4.icmp\_echo\_ignore_broadcasts=1  
net.ipv4.conf.default.forwarding=1  
[/code]

We can reload the settings from /etc/sysctl.conf by running the following command.  
[code]  
\# sysctl -p  
[/code]

In this instance I want to allow for <a href="http://www.robertshady.com/content/multiple-subnets-single-ethernet-interface-under-openvz" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.robertshady.com/content/multiple-subnets-single-ethernet-interface-under-openvz']);" target="_blank">multiple subnets</a>, so we can change the following lines in the /etc/vz/vz.conf.

[code]  
NEIGHBOUR_DEVS=all  
[/code]

Selinux is <a href="http://wiki.centos.org/HowTos/Virtualization/OpenVZ" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.centos.org/HowTos/Virtualization/OpenVZ']);" target="_blank">incompatible with OpenVZ</a> so we need to disable it. Edit the /etc/sysconfig/selinux and change the following line.

[code]  
SELINUX=disabled  
[/code]

Now that OpenVZ is installed, we should reboot again. This will disable selinux and also confirm that everything comes up on boot.

[code]  
\# reboot  
[/code]

## Deploying VMs in OpenVZ

There are many ways of deploying VMs in OpenVZ. The easiest is to download a prebuilt template. Get a template and put it in the right location. Look <a href="http://wiki.openvz.org/Download/template/precreated" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.openvz.org/Download/template/precreated']);" target="_blank">here</a> for prebuilt templates.

In my case, I am just going to use a debian 6 template from the repository.

[code]  
\# cd /vz/templates/cache  
\# wget http://download.openvz.org/template/precreated/debian-6.0-x86.tar.gz  
[/code]

Now that we have the template we can deploy the VM. When we deploy the VM we will give it a unique id (200 in this case). Check out <a href="http://wiki.openvz.org/Basic_operations_in_OpenVZ_environment" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.openvz.org/Basic_operations_in_OpenVZ_environment']);" target="_blank">this article</a> for the basic operations in OpenVZ.

[code]  
\# vzctl create 200 --ostemplate debian-6.0-x86 --config basic  
Creating container private area (debian-6.0-x86)  
Performing postcreate actions  
CT configuration saved to /etc/vz/conf/200.conf  
Container private area was created  
[/code]

I want this VM to be started when I boot the OpenVZ server.

[code]  
\# vzctl set 200 --onboot yes --save  
CT configuration saved to /etc/vz/conf/200.conf  
[/code]

Now we can configure this VM&#8217;s properties. It is as easy as running a few basic commands to set up the VM. With the commands we will set up the Hostname and ip address, etc. With this you can see how easy it would be to script deployments. 

[code]  
\# vzctl set 200 --hostname debian1.virtuallyhyper.com --save  
CT configuration saved to /etc/vz/conf/200.conf  
[root@openvz1 cache]# vzctl set 200 --ipadd 192.168.10.200 --save  
CT configuration saved to /etc/vz/conf/200.conf  
\# vzctl set 200 --nameserver 192.168.5.10 --save  
CT configuration saved to /etc/vz/conf/200.conf  
\# vzctl set 200 --searchdomain virtuallyhyper.com --ram 128M --diskspace 4G:5G --swap 128M --save  
CT configuration saved to /etc/vz/conf/200.conf  
[/code]

Since everything is configured the way we want it, let&#8217;s power on the VM.

[code]  
\# vzctl start 200  
Starting container ...  
Container is mounted  
Adding IP address(es): 192.168.10.200  
Setting CPU units: 1000  
Container start in progress..  
[/code]

One of the cool features of OpenVZ is that we can execute commands inside the running VM from the hypervisor&#8217;s console. In this case, let&#8217;s change the root password.

[code]  
\# vzctl exec 200 passwd  
Enter new UNIX password: abc123  
Retype new UNIX password: abc123  
passwd: password updated successfully  
[/code]

If running the commands was not enough, we could open a console session with the follwoing command. 

[code]  
\# vzctl enter 200  
[/code]

## Installing a Panel

One of the coolest things about Open Virtualization Software is the number of panels out there. The panel is the web interface that you use to manage and deploy VMs. It is not necessary to have one, but it is worth checking out.

<a href="https://code.google.com/p/ovz-web-panel/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://code.google.com/p/ovz-web-panel/']);" target="_blank">OpenVz Web Panel</a> is an open source panel. It has an incredibly easy install and is worth checking out. 

The OpenVz Web Panel comes with a easy installer script. (It will also install ruby on the system)

[code]  
\# wget -O - http://ovz-web-panel.googlecode.com/svn/installer/ai.sh | sh  
[/code]

Now browse to and login in with the credentials admin/admin.  
After logging in you can manage everything graphically. 

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 11 &#8211; SELinux" href="http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-11-selinux/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-11-selinux/']);" rel="bookmark">RHCSA and RHCE Chapter 11 &#8211; SELinux</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/installing-openvz-on-centos-6-in-an-esxi-5-vm/" title=" Installing OpenVZ on CentOS 6 in an ESXi 5 VM" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:hypervisor,nested,openvz,selinux,sysctl,vzctl,blog;button:compact;">Most of the information is covered in Security-Enhanced Linux Guide. From the guide here is what SELinux is: Security-Enhanced Linux (SELinux) is an implementation of a mandatory access control mechanism...</a>
</p>