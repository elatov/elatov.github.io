---
published: false
layout: post
title: "Use Packer with VMware Player to build an OVA"
author: Karim Elatov
categories: [vmware]
tags: [packer,ovftool, kickstart]
---
### Packer OVA Examples
I ran into a bunch of good examples that other people had luck with:

* [Infrastructure As Code: Create Linux (RHEL/CentOS) base Images Using Packer](http://technologist.pro/devops/infrastructure-as-code-create-linux-rhelcentos-base-images-using-packer)
* [packer-centos-7](https://github.com/geerlingguy/packer-centos-7)
* [packer-templates](https://github.com/nanliu/packer-templates)
* [automation_examples](https://github.com/UKCloud/automation_examples/tree/master/Packer)
* [packer-centos7-esxi](https://github.com/sdorsett/packer-centos7-esxi)
* [packer-templates](https://github.com/frapposelli/packer-templates)

### Packer Configuration Files
Between all of those examples, I created my own configs and made sure they were okay:

	<> tree
	.
	├── ansible
	│   ├── main.yml
	│   └── requirements.yml
	├── centos7.json
	├── http
	│   └── ks.cfg
	├── iso
	│   └── CentOS-7-x86_64-Minimal-1708.iso
	└── scripts
	    └── post-install.sh

First let's ensure the **packer** configs are okay:

	<> packer validate centos7.json
	Template validated successfully.

I also did the same thing on the **kickstart** file (initially it gave me a warning):

	<> ksvalidator http/ks.cfg
	The following problem occurred on line 5 of the kickstart file:
	
	Unknown command: unsupported_hardware

But then specifying the correct version got rid of the warnings:

	<> ksvalidator -v RHEL7 http/ks.cfg && echo $?
	0

I did have to get the latest version of the python module to get the **kickstart** validation to work (and fix a file to point to the right module: **orderedset** vs **ordered_set**, fix is described in [python-pykickstart](https://aur.archlinux.org/packages/python-pykickstart/)). Here is the version of the module that was installed with **pip**:

	<> pip2 show pykickstart
	---
	Metadata-Version: 1.1
	Name: pykickstart
	Version: 3.7
	Summary: Python module for manipulating kickstart files
	Home-page: http://fedoraproject.org/wiki/pykickstart
	Author: Chris Lumens
	Author-email: clumens@redhat.com
	License: UNKNOWN
	Location: /usr/local/lib/python2.7/dist-packages
	Requires:
	Classifiers:
	  Programming Language :: Python :: 3

### Packer Errors with VMware Player
I ran into a couple of error during the `packer build`, here are the ones that I remember:

#### Missing Vmware-VIX
Initially ran into an error where **vmrum** was not present (that's discussed [here ](https://github.com/hashicorp/packer/issues/1102)). To fix that error, I installed **vmware-vix** :

	<> chmod +x VMware-VIX-1.17.0-6661328.x86_64.bundle
	<> sudo ./VMware-VIX-1.17.0-6661328.x86_64.bundle
	Extracting VMware Installer...done.
	You must accept the VMware VIX API End User License Agreement to
	continue.  Press Enter to proceed.

And then I saw the vmrun executable:

	<> rehash
	<> which vmrun
	/usr/bin/vmrun

And just for reference here is the version of **vmplayer** I was running (this was on ubuntu 16.04):

	<> vmware-installer -l
	Product Name         Product Version
	==================== ====================
	vmware-player        14.1.1.7528167
	vmware-vix           1.17.0.6661328

#### Missing qemu-img
Then I saw the following:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	Build 'vmware-iso' errored: Failed creating VMware driver: Unable to initialize any driver for this platform. The errors
	from each driver are shown below. Please fix at least one driver
	to continue:
	* exec: "vmware": executable file not found in $PATH
	* exec: "vmware": executable file not found in $PATH
	* Neither 'vmware-vdiskmanager', nor 'qemu-img' found in path.
	One of these is required to configure disks for VMware Player.
	* Neither 'vmware-vdiskmanager', nor 'qemu-img' found in path.
	One of these is required to configure disks for VMware Player.

It looks like I was missing **qemu-img** and(or) **vmware-diskmanager** (it looks like I could get **vmware-diskmanager** from the **VMware Virtual Disk Development Kit** as discussed in
[this](https://communities.vmware.com/thread/409532) communities forum). For now I installed the **qemu-img**, cause it was faster:

	<> sudo apt install qemu-utils

#### Missing /etc/vmware/netmap.conf

Then I ran into an issue where it was missing a **vmplayer** configuration file:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Could not find netmap conf file: /etc/vmware/netmap.conf
	==> vmware-iso: Deleting output directory...
	Build 'vmware-iso' errored: Could not find netmap conf file: /etc/vmware/netmap.conf
	
	==> Some builds didn't complete successfully and had errors:
	--> vmware-iso: Could not find netmap conf file: /etc/vmware/netmap.conf
	
	==> Builds finished but no artifacts were created.

So I created a sample file using a copy from [How to Manually Configure VMWARE Networking on Linux Command Line](https://alexbelle.wordpress.com/2017/04/10/how-to-manually-configure-vmware-networking-on-linux-command-line/) site, and it ended up looking like this:

	<> cat /etc/vmware/netmap.conf
	network0.name = "Bridged"
	network0.device = "vmnet0"
	network1.name = "HostOnly"
	network1.device = "vmnet1"
	network2.name = "VMNet2"
	network2.device = "vmnet2"
	network8.name = "NAT"
	network8.device = "vmnet8"

#### Missing ldconfig
Then I ran into this message:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Starting HTTP server on port 8197
	==> vmware-iso: Starting virtual machine...
	    vmware-iso: The VM will be run headless, without a GUI. If you want to
	    vmware-iso: view the screen of the VM, connect via VNC with the password "SXxWhTkw" to
	    vmware-iso: vnc://127.0.0.1:5904
	==> vmware-iso: Error starting VM: VMware error: /usr/lib/vmware/bin/vmware-vmx: error while loading shared libraries: libXcursor.so.1: cannot open shared object file: No such file or directory
	==> vmware-iso: Waiting 4.655373739s to give VMware time to clean up...
	==> vmware-iso: Deleting output directory...
	Build 'vmware-iso' errored: Error starting VM: VMware error: /usr/lib/vmware/bin/vmware-vmx: error while loading shared libraries: libXcursor.so.1: cannot open shared object file: No such file or directory

I located the file 

	<> sudo updatedb
	<> locate libXcursor.so.1
	/usr/lib/vmware/lib/libXcursor.so.1
	/usr/lib/vmware/lib/libXcursor.so.1/libXcursor.so.1
	/usr/lib/vmware-installer/2.1.0/lib/lib/libXcursor.so.1
	/usr/lib/vmware-installer/2.1.0/lib/lib/libXcursor.so.1/libXcursor.so.1

and created the following file to load the library:

	<> cat /etc/ld.so.conf.d/vmware.conf
	/usr/lib/vmware/lib/libXcursor.so.1
	<> sudo ldconfig -v | grep vmware -A 1
	/usr/lib/vmware/lib/libXcursor.so.1:
		libXcursor.so.1 -> libXcursor.so.1

Then the VM started.

#### Incorrect dhcpd.conf file location
Then I ran into one more issue:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Starting HTTP server on port 8383
	==> vmware-iso: Starting virtual machine...
	    vmware-iso: The VM will be run headless, without a GUI. If you want to
	    vmware-iso: view the screen of the VM, connect via VNC with the password "9B6EsmKN" to
	    vmware-iso: vnc://127.0.0.1:5963
	==> vmware-iso: Waiting 10s for boot...
	==> vmware-iso: Connecting to VM via VNC (127.0.0.1:5963)
	==> vmware-iso: Error detecting host IP: Could not find vmnetdhcp conf file: /etc/vmware/vmnet8/dhcp/dhcp.conf
	==> vmware-iso: Stopping virtual machine...
	==> vmware-iso: Deleting output directory...
	Build 'vmware-iso' errored: Error detecting host IP: Could not find vmnetdhcp conf file: /etc/vmware/vmnet8/dhcp/dhcp.conf

It looks like now the file is located here **/etc/vmware/vmnet8/dhcpd/dhcpd.conf** (vs **/etc/vmware/vmnet8/dhcp/dhcp.conf**) , so I just created a **sym link** to the directory and file:

	<> ls -l /etc/vmware/vmnet8/dhcp
	lrwxrwxrwx 1 root root 5 Feb 11 12:39 /etc/vmware/vmnet8/dhcp -> dhcpd
	<> ls -l /etc/vmware/vmnet8/dhcp/dhcp.conf
	lrwxrwxrwx 1 root root 10 Feb 11 12:39 /etc/vmware/vmnet8/dhcp/dhcp.conf -> dhcpd.conf

Then it started the install, and I saw the VM running:

	<> vmrun -T player list
	Total running VMs: 1
	/usr/local/packer/output-ova-vmware-iso/packer-centos-7-x86_64.vmx
	<> ps -ef | grep vmx
	elatov    3592  1372  0 20:22 pts/3    00:00:00 grep --color=auto vmx
	elatov   30788     1 99 20:18 ?        00:04:33 /usr/lib/vmware/bin/vmware-vmx -s vmx.noUIBuildNumberCheck=TRUE -# product=4;name=VMware Player;version=14.0.0;buildnumber=6661328;licensename=VMware Player;licenseversion=14.0; -@ duplex=3;msgs=ui /usr/local/packer/output-ova-vmware-iso/packer-centos-7-x86_64.vmx

### Checking PXE Boot Install Progress

While the **Kickstart** install is going, **packer** was showing this message,

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Starting HTTP server on port 8863
	==> vmware-iso: Starting virtual machine...
	    vmware-iso: The VM will be run headless, without a GUI. If you want to
	    vmware-iso: view the screen of the VM, connect via VNC with the password "O08ybVbP" to
	    vmware-iso: vnc://127.0.0.1:5924
	==> vmware-iso: Waiting 10s for boot...
	==> vmware-iso: Connecting to VM via VNC (127.0.0.1:5924)
	==> vmware-iso: Typing the boot command over VNC...
	==> vmware-iso: Waiting for SSH to become available...

So I decided to connect to the VNC service. First I created an SSH tunnel from my Mac:

	<> ssh -L 1111:localhost:5924 ub

then on my Mac, I ran this:

	<> vncviewer localhost:1111

Then after typing in the password (from the **packer** output), I saw the install going:

![packer-ks-going.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/packer-vmplayer/packer-ks-going.png&raw=1)

It was good to confirm the install was going.

### Issue with Ansible provisioner and Packer

I ran into another issue with the **ansible** provisioner:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Starting HTTP server on port 8844
	==> vmware-iso: Starting virtual machine...
	    vmware-iso: The VM will be run headless, without a GUI. If you want to
	    vmware-iso: view the screen of the VM, connect via VNC with the password "lWgi2eUn" to
	    vmware-iso: vnc://127.0.0.1:5970
	==> vmware-iso: Waiting 10s for boot...
	==> vmware-iso: Connecting to VM via VNC (127.0.0.1:5970)
	==> vmware-iso: Typing the boot command over VNC...
	==> vmware-iso: Waiting for SSH to become available...
	==> vmware-iso: Connected to SSH!
	==> vmware-iso: Provisioning with shell script: scripts/post-install.sh
	..
	..
	==> vmware-iso: Provisioning with Ansible...
	    vmware-iso: Creating Ansible staging directory...
	    vmware-iso: Creating directory: /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb
	    vmware-iso: Uploading main Playbook file...
	    vmware-iso: Uploading galaxy file...
	{
	    vmware-iso: Uploading inventory file...
	    vmware-iso: Executing Ansible Galaxy: cd /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb && ansible-galaxy install -r /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb/requirements.yml -p /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb/roles
	    vmware-iso: - downloading role 'chrony', owned by influxdata
	    vmware-iso: - downloading role from https://github.com/influxdata/ansible-chrony/archive/master.tar.gz
	    vmware-iso: - extracting influxdata.chrony to /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb/roles/influxdata.chrony
	    vmware-iso: - influxdata.chrony (master) was installed successfully
	    vmware-iso: Executing Ansible: cd /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb && ANSIBLE_FORCE_COLOR=1 PYTHONUNBUFFERED=1 ansible-playbook /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb/main.yml --extra-vars \"packer_build_name=vmware-iso packer_builder_type=vmware-iso packer_http_addr=172.16.197.1:8844\"  -c local -i /tmp/packer-provisioner-ansible-local/5a80a166-018b-345f-29cb-6764bc9ad5bb/packer-provisioner-ansible-local746234266
	    vmware-iso: ERROR! the playbook: packer_builder_type=vmware-iso could not be found
	==> vmware-iso: Stopping virtual machine...
	==> vmware-iso: Deleting output directory...
	Build 'vmware-iso' errored: Error executing Ansible: Non-zero exit status: 1

The issue is specific to my **packer** version and is discussed [here](https://github.com/hashicorp/packer/issues/5885) (it's a pretty recent issue, so I will wait for the next version to see if that fixes it).

### Complete Packer Build

As I test I disabled **ansible** and just used the **shell** provisioner, and the *build* succeeded:

	<> packer build centos7.json
	vmware-iso output will be in this color.
	
	==> vmware-iso: Downloading or copying ISO
	    vmware-iso: Downloading or copying: file:///usr/local/packer/iso/CentOS-7-x86_64-Minimal-1708.iso
	==> vmware-iso: Creating virtual machine disk
	==> vmware-iso: Building and writing VMX file
	==> vmware-iso: Starting HTTP server on port 8776
	==> vmware-iso: Starting virtual machine...
	    vmware-iso: The VM will be run headless, without a GUI. If you want to
	    vmware-iso: view the screen of the VM, connect via VNC with the password "jxIgJ53t" to
	    vmware-iso: vnc://127.0.0.1:5976
	==> vmware-iso: Waiting 10s for boot...
	==> vmware-iso: Connecting to VM via VNC (127.0.0.1:5976)
	==> vmware-iso: Typing the boot command over VNC...
	==> vmware-iso: Waiting for SSH to become available...
	==> vmware-iso: Connected to SSH!
	==> vmware-iso: Provisioning with shell script: scripts/post-install.sh
	    vmware-iso: Loaded plugins: fastestmirror
	    vmware-iso: base                                                     | 3.6 kB     00:00
	    vmware-iso: extras                                                   | 3.4 kB     00:00
	    vmware-iso: updates                                                  | 3.4 kB     00:00
	    vmware-iso: (1/4): base/7/x86_64/group_gz                              | 156 kB   00:00
	    vmware-iso: (2/4): extras/7/x86_64/primary_db                          | 166 kB   00:00
	    vmware-iso: (3/4): updates/7/x86_64/primary_db                         | 6.0 MB   00:00
	    vmware-iso: (4/4): base/7/x86_64/primary_db                            | 5.7 MB   00:01
	    vmware-iso: Determining fastest mirrors
	    vmware-iso:  * base: mirror.den1.denvercolo.net
	    vmware-iso:  * extras: mirrors.umflint.edu
	    vmware-iso:  * updates: mirrors.oit.uci.edu
	    vmware-iso: Resolving Dependencies
	    vmware-iso: --> Running transaction check
	    vmware-iso: ---> Package ansible.noarch 0:2.4.2.0-2.el7 will be installed
	    vmware-iso: --> Processing Dependency: sshpass for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python2-jmespath for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-six for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-setuptools for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-passlib for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-paramiko for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-jinja2 for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-httplib2 for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-cryptography for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Processing Dependency: PyYAML for package: ansible-2.4.2.0-2.el7.noarch
	    vmware-iso: --> Running transaction check
	    vmware-iso: ---> Package PyYAML.x86_64 0:3.10-11.el7 will be installed
	    vmware-iso: --> Processing Dependency: libyaml-0.so.2()(64bit) for package: PyYAML-3.10-11.el7.x86_64
	    vmware-iso: ---> Package python-httplib2.noarch 0:0.9.2-1.el7 will be installed
	    vmware-iso: ---> Package python-jinja2.noarch 0:2.7.2-2.el7 will be installed
	    vmware-iso: --> Processing Dependency: python-babel >= 0.8 for package: python-jinja2-2.7.2-2.el7.noarch
	    vmware-iso: --> Processing Dependency: python-markupsafe for package: python-jinja2-2.7.2-2.el7.noarch
	    vmware-iso: ---> Package python-paramiko.noarch 0:2.1.1-2.el7 will be installed
	    vmware-iso: ---> Package python-passlib.noarch 0:1.6.5-2.el7 will be installed
	    vmware-iso: ---> Package python-setuptools.noarch 0:0.9.8-7.el7 will be installed
	    vmware-iso: --> Processing Dependency: python-backports-ssl_match_hostname for package: python-setuptools-0.9.8-7.el7.noarch
	    vmware-iso: ---> Package python-six.noarch 0:1.9.0-2.el7 will be installed
	    vmware-iso: ---> Package python2-cryptography.x86_64 0:1.7.2-1.el7_4.1 will be installed
	    vmware-iso: --> Processing Dependency: python-pyasn1 >= 0.1.8 for package: python2-cryptography-1.7.2-1.el7_4.1.x86_64
	    vmware-iso: --> Processing Dependency: python-idna >= 2.0 for package: python2-cryptography-1.7.2-1.el7_4.1.x86_64
	    vmware-iso: --> Processing Dependency: python-cffi >= 1.4.1 for package: python2-cryptography-1.7.2-1.el7_4.1.x86_64
	    vmware-iso: --> Processing Dependency: python-ipaddress for package: python2-cryptography-1.7.2-1.el7_4.1.x86_64
	    vmware-iso: --> Processing Dependency: python-enum34 for package: python2-cryptography-1.7.2-1.el7_4.1.x86_64
	    vmware-iso: ---> Package python2-jmespath.noarch 0:0.9.0-3.el7 will be installed
	    vmware-iso: ---> Package sshpass.x86_64 0:1.06-2.el7 will be installed
	    vmware-iso: --> Running transaction check
	    vmware-iso: ---> Package libyaml.x86_64 0:0.1.4-11.el7_0 will be installed
	    vmware-iso: ---> Package python-babel.noarch 0:0.9.6-8.el7 will be installed
	    vmware-iso: ---> Package python-backports-ssl_match_hostname.noarch 0:3.4.0.2-4.el7 will be installed
	    vmware-iso: --> Processing Dependency: python-backports for package: python-backports-ssl_match_hostname-3.4.0.2-4.el7.noarch
	    vmware-iso: ---> Package python-cffi.x86_64 0:1.6.0-5.el7 will be installed
	    vmware-iso: --> Processing Dependency: python-pycparser for package: python-cffi-1.6.0-5.el7.x86_64
	    vmware-iso: ---> Package python-enum34.noarch 0:1.0.4-1.el7 will be installed
	    vmware-iso: ---> Package python-idna.noarch 0:2.4-1.el7 will be installed
	    vmware-iso: ---> Package python-ipaddress.noarch 0:1.0.16-2.el7 will be installed
	    vmware-iso: ---> Package python-markupsafe.x86_64 0:0.11-10.el7 will be installed
	    vmware-iso: ---> Package python2-pyasn1.noarch 0:0.1.9-7.el7 will be installed
	    vmware-iso: --> Running transaction check
	    vmware-iso: ---> Package python-backports.x86_64 0:1.0-8.el7 will be installed
	    vmware-iso: ---> Package python-pycparser.noarch 0:2.14-1.el7 will be installed
	    vmware-iso: --> Processing Dependency: python-ply for package: python-pycparser-2.14-1.el7.noarch
	    vmware-iso: --> Running transaction check
	    vmware-iso: ---> Package python-ply.noarch 0:3.4-11.el7 will be installed
	    vmware-iso: --> Finished Dependency Resolution
	    vmware-iso:
	    vmware-iso: Dependencies Resolved
	    vmware-iso:
	    vmware-iso: ================================================================================
	    vmware-iso:  Package                              Arch    Version            Repository
	    vmware-iso:                                                                            Size
	    vmware-iso: ================================================================================
	    vmware-iso: Installing:
	    vmware-iso:  ansible                              noarch  2.4.2.0-2.el7      extras   7.6 M
	    vmware-iso: Installing for dependencies:
	    vmware-iso:  PyYAML                               x86_64  3.10-11.el7        base     153 k
	    vmware-iso:  libyaml                              x86_64  0.1.4-11.el7_0     base      55 k
	    vmware-iso:  python-babel                         noarch  0.9.6-8.el7        base     1.4 M
	    vmware-iso:  python-backports                     x86_64  1.0-8.el7          base     5.8 k
	    vmware-iso:  python-backports-ssl_match_hostname  noarch  3.4.0.2-4.el7      base      12 k
	    vmware-iso:  python-cffi                          x86_64  1.6.0-5.el7        base     218 k
	    vmware-iso:  python-enum34                        noarch  1.0.4-1.el7        base      52 k
	    vmware-iso:  python-httplib2                      noarch  0.9.2-1.el7        extras   115 k
	    vmware-iso:  python-idna                          noarch  2.4-1.el7          base      94 k
	    vmware-iso:  python-ipaddress                     noarch  1.0.16-2.el7       base      34 k
	    vmware-iso:  python-jinja2                        noarch  2.7.2-2.el7        base     515 k
	    vmware-iso:  python-markupsafe                    x86_64  0.11-10.el7        base      25 k
	    vmware-iso:  python-paramiko                      noarch  2.1.1-2.el7        extras   267 k
	    vmware-iso:  python-passlib                       noarch  1.6.5-2.el7        extras   488 k
	    vmware-iso:  python-ply                           noarch  3.4-11.el7         base     123 k
	    vmware-iso:  python-pycparser                     noarch  2.14-1.el7         base     104 k
	    vmware-iso:  python-setuptools                    noarch  0.9.8-7.el7        base     397 k
	    vmware-iso:  python-six                           noarch  1.9.0-2.el7        base      29 k
	    vmware-iso:  python2-cryptography                 x86_64  1.7.2-1.el7_4.1    updates  502 k
	    vmware-iso:  python2-jmespath                     noarch  0.9.0-3.el7        extras    39 k
	    vmware-iso:  python2-pyasn1                       noarch  0.1.9-7.el7        base     100 k
	    vmware-iso:  sshpass                              x86_64  1.06-2.el7         extras    21 k
	    vmware-iso:
	    vmware-iso: Transaction Summary
	    vmware-iso: ================================================================================
	    vmware-iso: Install  1 Package (+22 Dependent packages)
	    vmware-iso:
	    vmware-iso: Total download size: 12 M
	    vmware-iso: Installed size: 60 M
	    vmware-iso: Downloading packages:
	    vmware-iso: (1/23): libyaml-0.1.4-11.el7_0.x86_64.rpm                  |  55 kB   00:00
	    vmware-iso: (2/23): PyYAML-3.10-11.el7.x86_64.rpm                      | 153 kB   00:00
	    vmware-iso: (3/23): python-backports-1.0-8.el7.x86_64.rpm              | 5.8 kB   00:00
	    vmware-iso: (4/23): python-backports-ssl_match_hostname-3.4.0.2-4.el7. |  12 kB   00:00
	    vmware-iso: (5/23): python-cffi-1.6.0-5.el7.x86_64.rpm                 | 218 kB   00:00
	    vmware-iso: (6/23): ansible-2.4.2.0-2.el7.noarch.rpm                   | 7.6 MB   00:01
	    vmware-iso: (7/23): python-idna-2.4-1.el7.noarch.rpm                   |  94 kB   00:00
	    vmware-iso: (8/23): python-babel-0.9.6-8.el7.noarch.rpm                | 1.4 MB   00:01
	    vmware-iso: (9/23): python-enum34-1.0.4-1.el7.noarch.rpm               |  52 kB   00:00
	    vmware-iso: (10/23): python-jinja2-2.7.2-2.el7.noarch.rpm              | 515 kB   00:00
	    vmware-iso: (11/23): python-markupsafe-0.11-10.el7.x86_64.rpm          |  25 kB   00:00
	    vmware-iso: (12/23): python-httplib2-0.9.2-1.el7.noarch.rpm            | 115 kB   00:00
	    vmware-iso: (13/23): python-ipaddress-1.0.16-2.el7.noarch.rpm          |  34 kB   00:00
	    vmware-iso: (14/23): python-setuptools-0.9.8-7.el7.noarch.rpm          | 397 kB   00:00
	    vmware-iso: (15/23): python-six-1.9.0-2.el7.noarch.rpm                 |  29 kB   00:00
	    vmware-iso: (16/23): python-paramiko-2.1.1-2.el7.noarch.rpm            | 267 kB   00:00
	    vmware-iso: (17/23): python-ply-3.4-11.el7.noarch.rpm                  | 123 kB   00:00
	    vmware-iso: (18/23): python-passlib-1.6.5-2.el7.noarch.rpm             | 488 kB   00:00
	    vmware-iso: (19/23): python2-jmespath-0.9.0-3.el7.noarch.rpm           |  39 kB   00:00
	    vmware-iso: (20/23): python-pycparser-2.14-1.el7.noarch.rpm            | 104 kB   00:00
	    vmware-iso: (21/23): python2-cryptography-1.7.2-1.el7_4.1.x86_64.rpm   | 502 kB   00:00
	    vmware-iso: (22/23): sshpass-1.06-2.el7.x86_64.rpm                     |  21 kB   00:00
	    vmware-iso: (23/23): python2-pyasn1-0.1.9-7.el7.noarch.rpm             | 100 kB   00:00
	    vmware-iso: --------------------------------------------------------------------------------
	    vmware-iso: Total                                              6.0 MB/s |  12 MB  00:02
	    vmware-iso: Running transaction check
	    vmware-iso: Running transaction test
	    vmware-iso: Transaction test succeeded
	    vmware-iso: Running transaction
	    vmware-iso:   Installing : python-six-1.9.0-2.el7.noarch                               1/23
	    vmware-iso:   Installing : python2-pyasn1-0.1.9-7.el7.noarch                           2/23
	    vmware-iso:   Installing : python-httplib2-0.9.2-1.el7.noarch                          3/23
	    vmware-iso:   Installing : python-enum34-1.0.4-1.el7.noarch                            4/23
	    vmware-iso:   Installing : python-ipaddress-1.0.16-2.el7.noarch                        5/23
	    vmware-iso:   Installing : libyaml-0.1.4-11.el7_0.x86_64                               6/23
	    vmware-iso:   Installing : PyYAML-3.10-11.el7.x86_64                                   7/23
	    vmware-iso:   Installing : python-backports-1.0-8.el7.x86_64                           8/23
	    vmware-iso:   Installing : python-backports-ssl_match_hostname-3.4.0.2-4.el7.noarch    9/23
	    vmware-iso:   Installing : python-setuptools-0.9.8-7.el7.noarch                       10/23
	    vmware-iso:   Installing : python-babel-0.9.6-8.el7.noarch                            11/23
	    vmware-iso:   Installing : python-passlib-1.6.5-2.el7.noarch                          12/23
	    vmware-iso:   Installing : python-ply-3.4-11.el7.noarch                               13/23
	    vmware-iso:   Installing : python-pycparser-2.14-1.el7.noarch                         14/23
	    vmware-iso:   Installing : python-cffi-1.6.0-5.el7.x86_64                             15/23
	    vmware-iso:   Installing : python-markupsafe-0.11-10.el7.x86_64                       16/23
	    vmware-iso:   Installing : python-jinja2-2.7.2-2.el7.noarch                           17/23
	    vmware-iso:   Installing : python-idna-2.4-1.el7.noarch                               18/23
	    vmware-iso:   Installing : python2-cryptography-1.7.2-1.el7_4.1.x86_64                19/23
	    vmware-iso:   Installing : python-paramiko-2.1.1-2.el7.noarch                         20/23
	    vmware-iso:   Installing : python2-jmespath-0.9.0-3.el7.noarch                        21/23
	    vmware-iso:   Installing : sshpass-1.06-2.el7.x86_64                                  22/23
	    vmware-iso:   Installing : ansible-2.4.2.0-2.el7.noarch                               23/23
	    vmware-iso:   Verifying  : python-jinja2-2.7.2-2.el7.noarch                            1/23
	    vmware-iso:   Verifying  : python-backports-ssl_match_hostname-3.4.0.2-4.el7.noarch    2/23
	    vmware-iso:   Verifying  : sshpass-1.06-2.el7.x86_64                                   3/23
	    vmware-iso:   Verifying  : python-setuptools-0.9.8-7.el7.noarch                        4/23
	    vmware-iso:   Verifying  : python2-cryptography-1.7.2-1.el7_4.1.x86_64                 5/23
	    vmware-iso:   Verifying  : python2-jmespath-0.9.0-3.el7.noarch                         6/23
	    vmware-iso:   Verifying  : python-six-1.9.0-2.el7.noarch                               7/23
	    vmware-iso:   Verifying  : python-idna-2.4-1.el7.noarch                                8/23
	    vmware-iso:   Verifying  : python-markupsafe-0.11-10.el7.x86_64                        9/23
	    vmware-iso:   Verifying  : python-ply-3.4-11.el7.noarch                               10/23
	    vmware-iso:   Verifying  : python-passlib-1.6.5-2.el7.noarch                          11/23
	    vmware-iso:   Verifying  : python-babel-0.9.6-8.el7.noarch                            12/23
	    vmware-iso:   Verifying  : python-backports-1.0-8.el7.x86_64                          13/23
	    vmware-iso:   Verifying  : python-cffi-1.6.0-5.el7.x86_64                             14/23
	    vmware-iso:   Verifying  : python-paramiko-2.1.1-2.el7.noarch                         15/23
	    vmware-iso:   Verifying  : python-pycparser-2.14-1.el7.noarch                         16/23
	    vmware-iso:   Verifying  : libyaml-0.1.4-11.el7_0.x86_64                              17/23
	    vmware-iso:   Verifying  : ansible-2.4.2.0-2.el7.noarch                               18/23
	    vmware-iso:   Verifying  : python-ipaddress-1.0.16-2.el7.noarch                       19/23
	    vmware-iso:   Verifying  : python-enum34-1.0.4-1.el7.noarch                           20/23
	    vmware-iso:   Verifying  : python-httplib2-0.9.2-1.el7.noarch                         21/23
	    vmware-iso:   Verifying  : python2-pyasn1-0.1.9-7.el7.noarch                          22/23
	    vmware-iso:   Verifying  : PyYAML-3.10-11.el7.x86_64                                  23/23
	    vmware-iso:
	    vmware-iso: Installed:
	    vmware-iso:   ansible.noarch 0:2.4.2.0-2.el7
	    vmware-iso:
	    vmware-iso: Dependency Installed:
	    vmware-iso:   PyYAML.x86_64 0:3.10-11.el7
	    vmware-iso:   libyaml.x86_64 0:0.1.4-11.el7_0
	    vmware-iso:   python-babel.noarch 0:0.9.6-8.el7
	    vmware-iso:   python-backports.x86_64 0:1.0-8.el7
	    vmware-iso:   python-backports-ssl_match_hostname.noarch 0:3.4.0.2-4.el7
	    vmware-iso:   python-cffi.x86_64 0:1.6.0-5.el7
	    vmware-iso:   python-enum34.noarch 0:1.0.4-1.el7
	    vmware-iso:   python-httplib2.noarch 0:0.9.2-1.el7
	    vmware-iso:   python-idna.noarch 0:2.4-1.el7
	    vmware-iso:   python-ipaddress.noarch 0:1.0.16-2.el7
	    vmware-iso:   python-jinja2.noarch 0:2.7.2-2.el7
	    vmware-iso:   python-markupsafe.x86_64 0:0.11-10.el7
	    vmware-iso:   python-paramiko.noarch 0:2.1.1-2.el7
	    vmware-iso:   python-passlib.noarch 0:1.6.5-2.el7
	    vmware-iso:   python-ply.noarch 0:3.4-11.el7
	    vmware-iso:   python-pycparser.noarch 0:2.14-1.el7
	    vmware-iso:   python-setuptools.noarch 0:0.9.8-7.el7
	    vmware-iso:   python-six.noarch 0:1.9.0-2.el7
	    vmware-iso:   python2-cryptography.x86_64 0:1.7.2-1.el7_4.1
	    vmware-iso:   python2-jmespath.noarch 0:0.9.0-3.el7
	    vmware-iso:   python2-pyasn1.noarch 0:0.1.9-7.el7
	    vmware-iso:   sshpass.x86_64 0:1.06-2.el7
	    vmware-iso:
	    vmware-iso: Complete!
	==> vmware-iso: Gracefully halting virtual machine...
	    vmware-iso: Waiting for VMware to clean up after itself...
	==> vmware-iso: Deleting unnecessary VMware files...
	    vmware-iso: Deleting: output-ova-vmware-iso/vmware.log
	==> vmware-iso: Compacting the disk image
	==> vmware-iso: Cleaning VMX prior to finishing up...
	    vmware-iso: Unmounting floppy from VMX...
	    vmware-iso: Detaching ISO from CD-ROM device...
	    vmware-iso: Disabling VNC server...
	==> vmware-iso: Skipping export of virtual machine (export is allowed only for ESXi and the format needs to be specified)...
	==> vmware-iso: Running post-processor: shell-local
	==> vmware-iso (shell-local): Post processing with local shell script: /tmp/packer-shell112690227
	    vmware-iso (shell-local): Opening VMX source: output-ova-vmware-iso/packer-centos-7-x86_64.vmx
	    vmware-iso (shell-local): Opening OVA target: output-ova-vmware-iso/test.ova
	    vmware-iso (shell-local): Writing OVA package: output-ova-vmware-iso/test.ova
	    vmware-iso (shell-local): Transfer Completed
	    vmware-iso (shell-local): Completed successfully
	Build 'vmware-iso' finished.
	
	==> Builds finished. The artifacts of successful builds are:
	--> vmware-iso: VM files in directory: output-ova-vmware-iso
	--> vmware-iso:

And I had my OVA created:

	<> tree output-ova-vmware-iso
	output-ova-vmware-iso
	├── disk.vmdk
	├── packer-centos-7-x86_64.nvram
	├── packer-centos-7-x86_64.vmsd
	├── packer-centos-7-x86_64.vmx
	├── packer-centos-7-x86_64.vmxf
	└── test.ova

Pretty cool. I was also able to query the OVA to see it's properties:

	<> ovftool output-ova-vmware-iso/test.ova
	OVF version:   1.0
	VirtualApp:    false
	Name:          packer-centos-7-x86_64
	
	Download Size:  782.63 MB
	
	Deployment Sizes:
	  Flat disks:   16.00 GB
	  Sparse disks: 1.55 GB
	
	Networks:
	  Name:        nat
	  Description: The nat network
	
	Virtual Machines:
	  Name:               packer-centos-7-x86_64
	  Operating System:   centos7_64guest
	  Virtual Hardware:
	    Families:         vmx-13
	    Number of CPUs:   2
	    Cores per socket: 1
	    Memory:           512.00 MB
	
	    Disks:
	      Index:          0
	      Instance ID:    7
	      Capacity:       16.00 GB
	      Disk Types:     SCSI-lsilogic
	
	    NICs:
	      Adapter Type:   E1000
	      Connection:     nat

Looks pretty good.

### Deploying the OVA on an ESXi Host
As a quick test I deployed the OVA on an ESXi host:

	<> ovftool -dm=thin -ds=datastore1 "--net:nat=VM_VLAN3" output-ova-vmware-iso/test.ova "vi://root@hp.kar.int"
	Opening OVA source: output-ova-vmware-iso/test.ova
	The manifest validates
	Enter login information for target vi://hp.kar.int/
	Username: root
	Password: ********
	Opening VI target: vi://root@hp.kar.int:443/
	Deploying to VI: vi://root@hp.kar.int:443/
	Transfer Completed
	Completed successfully

I was able to power on the VM and login with the root user. Here is how the VM looked like in the web-client:

![esxi-packer-ova-deployed.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/packer-vmplayer/esxi-packer-ova-deployed.png&raw=1)

### Packer Options
I ended up setting some options in my packer configuration (all the options are covered in [VMware Builder (from ISO)](https://www.packer.io/docs/builders/vmware-iso.html)):

* I disabled the **tools_upload_flavor** option since I install the **open-vm-tools** package later on in the provisioning process.
* I set the **version** to **13** to match my ESXi version (which is **6.5**) by default it's **9** (which is ESXi **5.1**).
* I manually created the OVA with **ovftool** instead of uploaded it to the ESXi machine, just for testing (and to be able to use it for later use, since I don't have vCenter and I can't store templates):

	    "post-processors": [
	    {
	      "type": "shell-local",
	      "inline": ["ovftool output-ova-vmware-iso/packer-centos-7-x86_64.vmx output-ova-vmware-iso/test.ova"]
	    }
	    ]
* I set the **guest_os_typ** to be **centos7-64** to make sure it shows up as CentOS 7 and not CentOS 5 (the full list of OS types is available [here](https://code.vmware.com/apis/199/storage-policy#https://vdc-repo.vmware.com/vmwb-repository/dcr-public/9fd87c06-14a3-41e5-b28d-277864a80f29/d6112c2a-b124-4fa5-96d7-9fb4b6f1bb50/doc/vim.vm.GuestOsDescriptor.GuestOsIdentifier.html)

That should be it.
