---
layout: post
title: "Simple Vagrant Setup"
author: Karim Elatov
description: ""
categories: [OS]
tags: [vagrant, virtualbox]
---
I kept hearing good things about **vagrant**. Vagrant, from [their](http://www.vagrantup.com/) site, allows you to:

> Create and configure lightweight, reproducible, and portable development environments.

Basically utilizing existing virtualization products (Virtualbox, VMware, AWS ... etc) you are able to spin up an environment from a template for your personal use. If you are in need of a quick test enrvironmet, which you can remove after you are done, then vagrant is for you. Let's try out vagrant, first go to the [download](https://www.vagrantup.com/downloads.html) page and download the software:

![vagrant-download-page](https://googledrive.com/host/0B4vYKT_-8g4ISmlueEE3R0ZuR0U/vagrant-download-page.png)

Then install the software:

![vagrant-installer](https://googledrive.com/host/0B4vYKT_-8g4ISmlueEE3R0ZuR0U/vagrant-installer.png)

Here is a successfull install:

![vargrant-successfully-installed](https://googledrive.com/host/0B4vYKT_-8g4ISmlueEE3R0ZuR0U/vargrant-successfully-installed.png)

After it's installed you can open a terminal and you should see the executable available in your path:

	elatov@kmac:~$which vagrant
	/usr/bin/vagrant
	elatov@kmac:~$vagrant --version
	Vagrant 1.6.3

As a test run the following to create a very basic **VagrantFile**:

	elatov@kmac:~$vagrant init hashicorp/precise32
	A `Vagrantfile` has been placed in this directory. You are now
	ready to `vagrant up` your first virtual environment! Please read
	the comments in the Vagrantfile as well as documentation on
	`vagrantup.com` for more information on using Vagrant.
	
Here are the contents of the file without all the comments:

	elatov@kmac:~$grep -vE '  #|^$' Vagrantfile
	# -*- mode: ruby -*-
	# vi: set ft=ruby :
	# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
	VAGRANTFILE_API_VERSION = "2"
	Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	  config.vm.box = "hashicorp/precise32"
	end

Then go ahead and fire up the test machine (Make sure you also have [VirtualBox](https://www.virtualbox.org/) installed, since the below will create a VM in the VirtualBox Inventory):

	elatov@kmac:~$vagrant up
	Bringing machine 'default' up with 'virtualbox' provider...
	==> default: Box 'hashicorp/precise32' could not be found. Attempting to find and install...
	    default: Box Provider: virtualbox
	    default: Box Version: >= 0
	==> default: Loading metadata for box 'hashicorp/precise32'
	    default: URL: https://vagrantcloud.com/hashicorp/precise32
	==> default: Adding box 'hashicorp/precise32' (v1.0.0) for provider: virtualbox
	    default: Downloading: https://vagrantcloud.com/hashicorp/precise32/version/1/provider/virtualbox.box
	==> default: Successfully added box 'hashicorp/precise32' (v1.0.0) for 'virtualbox'!
	==> default: Importing base box 'hashicorp/precise32'...
	==> default: Matching MAC address for NAT networking...
	==> default: Checking if box 'hashicorp/precise32' is up to date...
	==> default: Setting the name of the VM: elatov_default_1402421505875_51723
	==> default: Clearing any previously set network interfaces...
	==> default: Preparing network interfaces based on configuration...
	    default: Adapter 1: nat
	==> default: Forwarding ports...
	    default: 22 => 2222 (adapter 1)
	==> default: Booting VM...
	==> default: Waiting for machine to boot. This may take a few minutes...
	    default: SSH address: 127.0.0.1:2222
	    default: SSH username: vagrant
	    default: SSH auth method: private key
	==> default: Machine booted and ready!
	==> default: Checking for guest additions in VM...
	    default: The guest additions on this VM do not match the installed version of
	    default: VirtualBox! In most cases this is fine, but in rare cases it can
	    default: prevent things such as shared folders from working properly. If you see
	    default: shared folder errors, please make sure the guest additions within the
	    default: virtual machine match the version of VirtualBox you have installed on
	    default: your host and reload your VM.
	    default:
	    default: Guest Additions Version: 4.2.0
	    default: VirtualBox Version: 4.3
	==> default: Mounting shared folders...
	    default: /vagrant => /Users/elatov
	    
That will spin up an Ubuntu 12.04 LTS 32-bit VM (downloaded from the vagrant cloud) in your local VirtualBox instance. You can see the VM, by using **VboxManage**:

	elatov@kmac:~$VBoxManage list vms
	"Win_7" {bcae8e7d-df73-46d7-ae34-2f3ffa12faa4}
	"elatov_default_1402421505875_51723" {4c0c2687-7e3c-475a-a0cc-05386321ac20}

The first one is my default windows VM, and the second one is the one that **vagrant** created. The vagrant command also creates a **.vargrant** directory with the VM information. For example here is the ID information for the VM it created:

	elatov@kmac:~$cat .vagrant/machines/default/virtualbox/id
	4c0c2687-7e3c-475a-a0cc-05386321ac20

You can also check the status of the VM with the **vagrant** command:

	elatov@kmac:~$vagrant status
	Current machine states:
	
	default                   running (virtualbox)
	
	The VM is running. To stop this VM, you can run `vagrant halt` to
	shut it down forcefully, or you can run `vagrant suspend` to simply
	suspend the virtual machine. In either case, to restart it again,
	simply run `vagrant up`.

Lastly we can confirm the process is running by checking out the process table:

	elatov@kmac:~$ps -eaf | grep -i Headless
	 1000  2125  2084   0 11:31AM ??         0:39.63 /Applications/VirtualBox.app/Contents/MacOS/VBoxHeadless --comment elatov_default_1402421505875_51723 --startvm 4c0c2687-7e3c-475a-a0cc-05386321ac20 --vrde config

You can get more information regarding the VirtualBox VM, by using **VboxManage** again:

	elatov@kmac:~$VBoxManage guestproperty enumerate elatov_default_1402421505875_51723
	Name: /VirtualBox/GuestInfo/OS/Product, value: Linux, timestamp: 1402421514359792000, flags:
	Name: /VirtualBox/GuestInfo/Net/0/V4/IP, value: 10.0.2.15, timestamp: 1402421514364254000, flags:
	Name: /VirtualBox/HostInfo/GUI/LanguageID, value: en_US, timestamp: 1347600794142581000, flags:
	Name: /VirtualBox/GuestInfo/Net/0/MAC, value: 080027129698, timestamp: 1402421514365424000, flags:
	Name: /VirtualBox/GuestInfo/OS/ServicePack, value: , timestamp: 1402421514361487000, flags:
	Name: /VirtualBox/HostInfo/VBoxVerExt, value: 4.3.12, timestamp: 1402421507100618000, flags: TRANSIENT, RDONLYGUEST
	Name: /VirtualBox/GuestInfo/Net/0/V4/Netmask, value: 255.255.255.0, timestamp: 1402421514365011000, flags:
	Name: /VirtualBox/GuestInfo/OS/Version, value: #36-Ubuntu SMP Tue Apr 10 22:19:09 UTC 2012, timestamp: 1402421514360847000, flags:
	Name: /VirtualBox/GuestAdd/VersionExt, value: 4.2.0, timestamp: 1402421514362328000, flags:
	Name: /VirtualBox/GuestAdd/Revision, value: 80737, timestamp: 1402421514362838000, flags:
	Name: /VirtualBox/HostGuest/SysprepExec, value: , timestamp: 1402421507098976000, flags: TRANSIENT, RDONLYGUEST
	Name: /VirtualBox/GuestInfo/OS/LoggedInUsers, value: 0, timestamp: 1402424134859693000, flags: TRANSIENT, TRANSRESET
	Name: /VirtualBox/GuestInfo/Net/0/Status, value: Up, timestamp: 1402421514365818000, flags:
	Name: /VirtualBox/HostGuest/SysprepArgs, value: , timestamp: 1402421507099160000, flags: TRANSIENT, RDONLYGUEST
	Name: /VirtualBox/GuestAdd/Version, value: 4.2.0, timestamp: 1402421514361925000, flags:
	Name: /VirtualBox/HostInfo/VBoxRev, value: 93733, timestamp: 1402421507100717000, flags: TRANSIENT, RDONLYGUEST
	Name: /VirtualBox/GuestInfo/Net/0/V4/Broadcast, value: 10.0.2.255, timestamp: 1402421514364641000, flags:
	Name: /VirtualBox/HostInfo/VBoxVer, value: 4.3.12, timestamp: 1402421507100484000, flags: TRANSIENT, RDONLYGUEST
	Name: /VirtualBox/GuestInfo/Net/Count, value: 1, timestamp: 1402424144863313000, flags:
	Name: /VirtualBox/GuestInfo/OS/Release, value: 3.2.0-23-generic-pae, timestamp: 1402421514360448000, flags:
	Name: /VirtualBox/GuestInfo/OS/NoLoggedInUsers, value: true, timestamp: 1402424134860434000, flags: TRANSIENT, TRANSRESET

From the above output we can see that it's IP is **10.0.2.15**, which is the default IP, when Vbox is using the NAT. If you want more in depth information about the VM, you can run the following:

	elatov@kmac:~$VBoxManage showvminfo elatov_default_1402421505875_51723
	Name:            elatov_default_1402421505875_51723
	Groups:          /
	Guest OS:        Ubuntu (32 bit)
	UUID:            4c0c2687-7e3c-475a-a0cc-05386321ac20
	Config file:     /Users/elatov/.virt/elatov_default_1402421505875_51723/elatov_default_1402421505875_51723.vbox
	Snapshot folder: /Users/elatov/.virt/elatov_default_1402421505875_51723/Snapshots
	Log folder:      /Users/elatov/.virt/elatov_default_1402421505875_51723/Logs
	Hardware UUID:   4c0c2687-7e3c-475a-a0cc-05386321ac20
	Memory size:     384MB
	Page Fusion:     off
	VRAM size:       8MB
	CPU exec cap:    100%
	HPET:            off
	Chipset:         piix3
	Firmware:        BIOS
	Number of CPUs:  1
	PAE:             on
	Long Mode:       on
	Synthetic CPU:   off
	CPUID overrides: None
	Boot menu mode:  message and menu
	Boot Device (1): HardDisk
	Boot Device (2): DVD
	Boot Device (3): Not Assigned
	Boot Device (4): Not Assigned
	ACPI:            on
	IOAPIC:          off
	Time offset:     0ms
	RTC:             UTC
	Hardw. virt.ext: on
	Nested Paging:   on
	Large Pages:     on
	VT-x VPID:       on
	VT-x unr. exec.: on
	State:           running (since 2014-06-10T17:31:47.680000000)
	Monitor count:   1
	3D Acceleration: off
	2D Video Acceleration: off
	Teleporter Enabled: off
	Teleporter Port: 0
	Teleporter Address:
	Teleporter Password:
	Tracing Enabled: off
	Allow Tracing to Access VM: off
	Tracing Configuration:
	Autostart Enabled: off
	Autostart Delay: 0
	Default Frontend:
	Storage Controller Name (0):            IDE Controller
	Storage Controller Type (0):            PIIX4
	Storage Controller Instance Number (0): 0
	Storage Controller Max Port Count (0):  2
	Storage Controller Port Count (0):      2
	Storage Controller Bootable (0):        on
	Storage Controller Name (1):            SATA Controller
	Storage Controller Type (1):            IntelAhci
	Storage Controller Instance Number (1): 0
	Storage Controller Max Port Count (1):  30
	Storage Controller Port Count (1):      1
	Storage Controller Bootable (1):        on
	IDE Controller (0, 0): Empty
	IDE Controller (1, 0): Empty
	SATA Controller (0, 0): /Users/elatov/.virt/elatov_default_1402421505875_51723/box-disk1.vmdk (UUID: 51187fe9-7c0d-46b4-9db4-9869dd5a7413)
	NIC 1:           MAC: 080027129698, Attachment: NAT, Cable connected: on, Trace: off (file: none), Type: 82540EM, Reported speed: 0 Mbps, Boot priority: 0, Promisc Policy: deny, Bandwidth group: none
	NIC 1 Settings:  MTU: 0, Socket (send: 64, receive: 64), TCP Window (send:64, receive: 64)
	NIC 1 Rule(0):   name = ssh, protocol = tcp, host ip = 127.0.0.1, host port = 2222, guest ip = , guest port = 22
	NIC 2:           disabled
	NIC 3:           disabled
	NIC 4:           disabled
	NIC 5:           disabled
	NIC 6:           disabled
	NIC 7:           disabled
	NIC 8:           disabled
	Pointing Device: PS/2 Mouse
	Keyboard Device: PS/2 Keyboard
	UART 1:          disabled
	UART 2:          disabled
	LPT 1:           disabled
	LPT 2:           disabled
	Audio:           disabled
	Clipboard Mode:  disabled
	Drag'n'drop Mode: disabled
	Session type:    headless
	Video mode:      640x480x32 at 0,0
	VRDE:            disabled
	USB:             disabled
	EHCI:            disabled
	
	USB Device Filters:
	
	<none>
	
	Available remote USB devices:
	
	<none>
	
	Currently Attached USB Devices:
	
	<none>
	
	Bandwidth groups:  <none>
	
	Shared folders:
	
	Name: 'vagrant', Host path: '/Users/elatov' (machine mapping), writable
	
	VRDE Connection:    not active
	Clients so far:     0
	
	Video capturing:    not active
	Capture screens:    0
	Capture file:       /Users/elatov/.virt/elatov_default_1402421505875_51723/elatov_default_1402421505875_51723.webm
	Capture dimensions: 1024x768
	Capture rate:       512 kbps
	Capture FPS:        25
	
	Guest:
	
	Configured memory balloon size:      0 MB
	OS type:                             Linux26
	Additions run level:                 2
	Additions version:                   4.2.0 r80737
	
	
	Guest Facilities:
	
	Facility "VirtualBox Base Driver": active/running (last update: 2014/06/10 17:31:53 UTC)
	Facility "VirtualBox System Service": active/running (last update: 2014/06/10 17:31:54 UTC)
	Facility "Seamless Mode": not active (last update: 2014/06/10 17:31:53 UTC)
	Facility "Graphics Mode": not active (last update: 2014/06/10 17:31:53 UTC)
 
From the `vagrant up` command we can see that it created a port forward from **127.0.0.1:2222** to port **22** of the spun up VM and it created an ssh key for the **vagrant** user. So let's try the manual way of logging into the vm:

	elatov@kmac:~$ssh vagrant@localhost -p 2222 -i .vagrant.d/insecure_private_key
	The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
	ECDSA key fingerprint is 32:53:5d:95:d9:2b:c0:92:ab:1d:a4:87:95:a6:5a:e2.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added '[localhost]:2222' (ECDSA) to the list of known hosts.
	Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)
	
	 * Documentation:  https://help.ubuntu.com/
	Welcome to your Vagrant-built virtual machine.
	Last login: Tue Jun 10 17:39:16 2014 from 10.0.2.2
	vagrant@precise32:~$

An easy way to access the VM is with the `vagrant ssh` command, like so:

	elatov@kmac:~$vagrant ssh default
	Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)
	
	 * Documentation:  https://help.ubuntu.com/
	Welcome to your Vagrant-built virtual machine.
	Last login: Fri Sep 14 06:22:31 2012 from 10.0.2.2
	vagrant@precise32:~$
	
After you done with the VM, you can shut it down:

	elatov@kmac:~$vagrant halt
		==> default: Attempting graceful shutdown of VM...

and then remove the VM:

	elatov@kmac:~$vagrant destroy
		    default: Are you sure you want to destroy the 'default' VM? [y/N] y
		==> default: Destroying VM and associated drives...
		
This will remove the VM from VirtualBox's Inventory (and it's associated virtual disk), but the box (**hashicorp/precise32**) that you downloaded from the vagrant cloud will be stored in your local disk. This way when you need to spin up another VM it will just use the template box / base image (more on this in the next post).  