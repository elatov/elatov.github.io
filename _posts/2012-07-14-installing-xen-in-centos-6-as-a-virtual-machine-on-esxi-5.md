---
title: Installing Xen in CentOS 6 as a Virtual Machine on ESXi 5
author: Jarret Lavallee
layout: post
permalink: /2012/07/installing-xen-in-centos-6-as-a-virtual-machine-on-esxi-5/
dsq_thread_id:
  - 1405247504
categories:
  - Home Lab
  - VMware
tags:
  - libvirt
  - nested Xen
  - Xen
---
I have been installing different hyper-visors in my lab. Since I did not have extra servers lying around, I have been deploying the hyper-visors in ESXi 5.x VMs. Here I cover installing Xen as an ESXi guest.

### Prepare ESX VMs to Run Nested Hyper-visors

Before beginning, we should <a href="http://communities.vmware.com/docs/DOC-8970" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-8970']);">set up the ESX host</a> to allow nested hyper-visors. First set the following option in the **/etc/vmware/config** file:

    vhv.allow = TRUE
    

Next we need to set up a VM and enable hardware virtualization inside the VM. I created a new Centos 6.3 VM with hardware version 8. Also ensure that the network port-group (that the VM is connected to) is set to **promiscuous** mode.

Shut down the VM and add the following lines to the **VMX** file. The first 2 lines set the MMU to be hardware. The next 5 set the CPU flags and the last line is an optimization setting to stop hangs in KVM. See <a href="http://communities.vmware.com/docs/DOC-8970" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-8970']);">this article</a> for more details.

    cpuid.1.ecx=”—-:—-:—-:—-:—-:—-:–h-:—-”
    cpuid.80000001.ecx.amd=”—-:—-:—-:—-:—-:—-:—-:-h–”
    cpuid.8000000a.eax.amd=”hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh”
    cpuid.8000000a.ebx.amd=”hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh”
    cpuid.8000000a.edx.amd=”hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh:hhhh”
    monitor.virtual_mmu = “hardware”
    monitor.virtual_exec = “hardware”
    

After making the changes to the VMX, we need to reload the VM on the ESXi host.

    # vim-cmd vmsvc/getallvms |grep xen1
    255 xen1 [iscsi_dev] xen1/xen1.vmx rhel6_64Guest vmx-08
    # vim-cmd vmsvc/reload 255
    # vim-cmd vmsvc/power.on 255
    

Once the VM is booted, let&#8217;s log in an disable **selinux**. Edit the **/etc/selinux/config** file and change the following line:

    SELINUX=disabled
    

Now reboot the VM to make sure *selinux* is not enabled on boot.

    # reboot
    

### Setup Bridge Networking in Xen

Just like in <a href="http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/']);">this post</a>, we are going to set up a bridged network. I have 2 adapters in this VM, so we will use **eth1** for the bridge. Create the **/etc/sysconfig/network-scripts/ifcfg-br0** file and place the following contents into the file:

    DEVICE=”br0″
    TYPE=Bridge
    DELAY=0
    ONBOOT=”yes”
    BOOTPROTO=static
    IPADDR=192.168.10.46
    NETMASK=255.255.255.0
    NETWORK=192.168.10.0
    GATEWAY=192.168.10.1
    DNS1=192.168.5.10
    PEERDNS=”yes”
    NM_CONTROLLED=no
    

Edit the **/etc/sysconfig/network-scripts/ifcfg-eth1** file and change the contents to the following:

    DEVICE=eth1
    ONBOOT=yes
    BRIDGE=br0
    NM_CONTROLLED=no
    HWADDR=00:50:56:B0:07:A4
    

Now we can restart the networking service to enable the bridge.

    # service network restart
    

Let&#8217;s check to make sure the bridge is working. First we need to install the bridge utilities package.

    # yum install bridge-utils
    

Now we can use the *bridge* tools to show the bridge information:

    # brctl show
    bridge name bridge id STP enabled interfaces
    br0 8000.005056b007a4 no eth1
    

### Install Xen Specific Packages

One of the problems with choosing CentOS 6 is that Xen is not longer included in the repos, so we need to pull it from elsewhere. You can build a kernel from source using <a href="http://wiki.xenproject.org/wiki/RHEL6Xen4Tutorial" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.xenproject.org/wiki/RHEL6Xen4Tutorial']);">these instructions</a> or you can use <a href="http://au1.mirror.crc.id.au/repo" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://au1.mirror.crc.id.au/repo']);">this repo</a> to install an RPM.

    # yum install http://au1.mirror.crc.id.au/repo/kernel-xen-release-6-5.noarch.rpm
    # yum install kernel-xen xen
    

### Compile libvirt with Xen Support

Since CentOS 6 (RHEL6) does not ship with Xen, they did not compile in Xen support for **libvirt**. So we need to compile *libvirt* from the SRPMS and enable Xen support. If you do not use *libvirt*, skip this section. Otherwise we need to do this before booting into the Xen kernel. I would do this on a build machine, or clean up the packages after the build.

To get this started, install *libvirt*:

    # yum install libvirt python-virtinst
    

Next, install the &#8220;Development Tools&#8221;:

    # yum groupinstall ‘Development Tools’
    

Then, install some more development packages:

    # yum install python-devel xen-devel libxml2-devel xhtml1-dtds readline-devel ncurses-devel libtasn1-devel gnutls-devel augeas libudev-devel libpciaccess-devel yajl-devel sanlock-devel libpcap-devel libnl-devel avahi-devel libselinux-devel cyrus-sasl-devel parted-devel device-mapper-devel numactl-devel libcap-ng-devel netcf-devel libcurl-devel audit-libs-devel systemtap-sdt-devel libblkid-devel scrub
    

Find out what version of *libvirt* we are running now:

    # rpm -qa | grep libvirt
    libvirt-python-0.9.10-21.el6_3.1.x86_64
    libvirt-client-0.9.10-21.el6_3.1.x86_64
    libvirt-0.9.10-21.el6_3.1.x86_64
    

Above we can see that we have *libvirt* 0.9.10 installed, so we need to install the 0.9.10 version SRPM. It is not a good idea to build packages as root, but I am doing that here <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Installing Xen in CentOS 6 as a Virtual Machine on ESXi 5" class="wp-smiley" title="Installing Xen in CentOS 6 as a Virtual Machine on ESXi 5" /> 

    # mkdir /root/src
    # cd /root/src
    # wget “ftp://ftp.redhat.com/pub/redhat/linux/enterprise/6Server/en/os/SRPMS/libvirt-0.9.10-21.el6.src.rpm”
    # rpm -i libvirt-0.9.10-21.el6.src.rpm
    

Next we have to enable Xen support. I have included a patch below, but it only changes a single line so we can do it manually. First open the **libvirt.spec** file:

    # cd /root/rpmbuild/SPECS/
    # vi libvirt.spec
    

Now make the changes to the following lines.

    # RHEL-6 has restricted QEMU to x86_64 only, stopped including Xen
    # on all archs. Other archs all have LXC available though
    %if 0%{?rhel} >= 6
    %ifnarch x86_64
    %define with_qemu 0
    %endif
    %define with_xen 1
    %endif
    

Below is the patch that I created. You can learn more about applying and creating patches <a href="http://www.linuxtutorialblog.com/post/introduction-using-diff-and-patch-tutorial" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linuxtutorialblog.com/post/introduction-using-diff-and-patch-tutorial']);">here</a>.

    — libvirt.spec.orig 2012-07-12 14:05:12.287671758 -0600
    +++ libvirt.spec 2012-07-12 14:05:37.390462727 -0600
    @@ -137,7 +137,7 @@
    %ifnarch x86_64
    %define with_qemu 0
    %endif
    -%define with_xen 0
    +%define with_xen 1
    %endif
    
    # Fedora doesn’t have any QEMU on ppc64 – only ppc
    

Now that we have made the changes that we wanted, we can build the package:

    # rpmbuild -bb libvirt.spec
    

If it fails to build with missing dependencies, install them with **yum**. When **rpmbuild** is finished, it will create the RPMs for us and we need to install them. You can use these packages to install on other hosts as well.

    # cd /root/rpmbuild/RPMS/x86_64
    # rpm -iUvh –force libvirt-0.9.10-21.el6.x86_64.rpm libvirt-client-0.9.10-21.el6.x86_64.rpm libvirt-python-0.9.10-21.el6.x86_64.rpm
    

### Setup Grub to Boot from the Xen Kernel

We can now set the Xen kernel to be the default kernel in grub. Edit the **/etc/grub.conf** file to ensure that it is going to boot the Xen kernel. Here are the change that we need to make:

1.  Add the line `kernel /xen.gz dom0_mem=512M cpufreq=xen dom0_max_vcpus=1 dom0_vcpus_pin` 
2.  Change the “kernel” and “initrd” declarations to “module”

**NOTE:** I only gave dom0 (the host OS) 512M of memory. You can increase this by changing the **dom0_mem** parameter. The minimum amount is required to be no less than 256M, this is defined in the **/etc/xen/xend-config.sxp** file. New versions of Xen can go without this option, but then all the memory will allocated to *dom0* and ballooned down (released) as necessary for VMs. I suggest putting in a memory limit for the host OS.

Here is how the final **grub** entry looked like:

    title xen CentOS (2.6.32.57-2.el6xen.x86_64)
    root (hd0,0)
    kernel /xen.gz dom0_mem=512M cpufreq=xen dom0_max_vcpus=1 dom0_vcpus_pin
    module /vmlinuz-2.6.32.57-2.el6xen.x86_64 ro root=/dev/mapper/vg_centos6x64-lv_root rd_LVM_LV=vg_centos6x64/lv_root rd_LVM_LV=vg_centos6x64/lv_swap rd_NO_LUKS rd_NO_MD rd_NO_DM LANG=en_US.UTF-8 SYSFONT=latarcyrheb-sun16 KEYBOARDTYPE=pc KEYTABLE=us crashkernel=auto rhgb
    module /initramfs-2.6.32.57-2.el6xen.x86_64.img
    

Let&#8217;s reboot into the new kernel.

    # reboot
    

### Check Xen Operations

After the reboot, we can log in and check to make sure we are running the new kernel:

    # uname -a
    Linux xen1 2.6.32.57-2.el6xen.x86_64 #1 SMP Fri May 25 14:05:24 EST 2012 x86_64 x86_64 x86_64 GNU/Linux
    

We can also list the VMs running on this host:

    # xm list
    Name ID Mem VCPUs State Time(s)
    Domain-0 0 512 1 r—– 11.6
    

If you want VNC to listen on every network interface instead of just locally, change the following line in the **/etc/xen/xend-config.sxp** file:

    (vnc-listen '0.0.0.0')
    

Let&#8217;s check **libvirt** to ensure it works with Xen:

    # virsh list
    Id Name State
    —————————————————-
    0 Domain-0 running
    

### Adding VMs

There are MANY ways to allocate VMs. Check out <a href="http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture']);">this post</a> from Karim about creating VMs in KVM using *libvirt* or <a href="http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/']);">this post</a> about KVM. In this example I am attaching an ISO to a VM that I copied over to the **/var/lib/libvirt/images** directory.

    # virt-install –name=centos1 –arch=x86_64 –vcpus=1 –ram=512 –os-type=linux –os-variant=rhel6 –hvm –network bridge:br0 –cdrom=/var/lib/libvirt/images/CentOS-6.0-x86_64-minimal.iso –disk path=/vms/centos1.img,size=5 –accelerate –vnc –noautoconsole –keymap=es
    

Let&#8217;s list the running VMs after creating a VM named *centos1*:

    # xm list
    Name ID Mem VCPUs State Time(s)
    Domain-0 0 512 1 r—– 55.0
    centos1 1 512 1 —— 2.0
    

Let&#8217;s use *libvirt* to get the state of the VMs:

    # virsh list
    Id Name State
    —————————————————-
    0 Domain-0 running
    1 centos1 idle
    

We can get the VNC port that the we will use to connect to this VM with by running the following command:

    # virsh vncdisplay centos1
    :0
    

The number above is added to port 5900 to get the VNC port (ie. 5900+0=5900). Let&#8217;s make sure the host is listening on that port.

    # netstat -an |grep 5900
    tcp 0 0 0.0.0.0:5900 0.0.0.0:* LISTEN
    

So now we can connect to that host on port 5900 with a VNC client and configure the VM. Further reading can be found at the following links:

*   https://www.crc.id.au/xen-on-rhel6-scientific-linux-6-centos-6-howto
*   http://www.centos.org/docs/5/html/5.2/Virtualization/sect-Virtualization-Tips&#95;and&#95;tricks-Modifying_etcgrub.conf.html
*   http://wiki.xen.org/wiki/RHEL6&#95;Xen4&#95;Tutorial#Using&#95;libvirt&#95;and&#95;virt-manager&#95;with_Xen
*   http://www.phoenixxie.com/?p=186

