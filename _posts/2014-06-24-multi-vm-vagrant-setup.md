---
published: true
layout: post
title: "Multi VM Vagrant Setup"
author: Karim Elatov
categories: [os,networking]
tags: [vagrant,opensuse,virtualbox]
---
I initialized my *vagrant* environment with the following:

	elatov@kmac:~$mkdir test
	elatov@kmac:~$cd test
	elatov@kmac:~/test$vagrant init elatov/opensuse13-64
	A `Vagrantfile` has been placed in this directory. You are now
	ready to `vagrant up` your first virtual environment! Please read
	the comments in the Vagrantfile as well as documentation on
	`vagrantup.com` for more information on using Vagrant.

Then I modified the **Vagrantfile** to configure multiple VMs:

	elatov@kmac:~/test$cat Vagrantfile
	# -*- mode: ruby -*-
	# vi: set ft=ruby :
	boxes = [
	  { :name => :web,:ip => '192.168.33.1',:ssh_port => 2201,:cpus => 1, :mem => 512},
	  { :name => :db,:ip => '192.168.33.2',:ssh_port => 2202,:cpus => 1,:mem => 512 },
	  ]
	
	# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
	VAGRANTFILE_API_VERSION = "2"
	
	Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	    boxes.each do |opts|
	        config.vm.define opts[:name] do |config|
	    	    config.vm.box       = "elatov/opensuse13-64"
	    	    config.vm.box_url   = "https://vagrantcloud.com/elatov/opensuse13-64/version/1/provider/virtualbox.box"
	    	    config.vm.network  "private_network", ip: opts[:ip]
	    	    config.vm.network  "forwarded_port", guest: 22, host: opts[:ssh_port]
	    	    config.vm.hostname = "%s.vagrant" % opts[:name].to_s
	    	    config.vm.synced_folder "~/stuff", "/vagrant"
		    config.vm.provider "virtualbox" do |vb|
	  	    # Use VBoxManage to customize the VM
	    	        vb.customize ["modifyvm", :id, "--cpus", opts[:cpus] ] if opts[:cpus]
	    	        vb.customize ["modifyvm", :id, "--memory", opts[:mem] ] if opts[:mem]
		    end
	       end
	    end
	end

Upon starting up the environment, I saw the following:

	elatov@kmac:~/test$vagrant up
	Bringing machine 'web' up with 'virtualbox' provider...
	Bringing machine 'db' up with 'virtualbox' provider...
	==> web: You assigned a static IP ending in ".1" to this machine.
	==> web: This is very often used by the router and can cause the
	==> web: network to not work properly. If the network doesn't work
	==> web: properly, try changing this IP.
	==> web: Importing base box 'elatov/opensuse13-64'...
	==> web: Matching MAC address for NAT networking...
	==> web: You assigned a static IP ending in ".1" to this machine.
	==> web: This is very often used by the router and can cause the
	==> web: network to not work properly. If the network doesn't work
	==> web: properly, try changing this IP.
	==> web: Checking if box 'elatov/opensuse13-64' is up to date...
	==> web: Setting the name of the VM: test_web_1402605293166_51170
	==> web: Clearing any previously set network interfaces...
	==> web: Preparing network interfaces based on configuration...
	    web: Adapter 1: nat
	    web: Adapter 2: hostonly
	==> web: Forwarding ports...
	    web: 22 => 2201 (adapter 1)
	    web: 22 => 2222 (adapter 1)
	==> web: Running 'pre-boot' VM customizations...
	==> web: Booting VM...
	==> web: Waiting for machine to boot. This may take a few minutes...
	    web: SSH address: 127.0.0.1:2222
	    web: SSH username: vagrant
	    web: SSH auth method: private key
	    web: Warning: Connection timeout. Retrying...
	    web: Warning: Remote connection disconnect. Retrying...
	    web: Warning: Remote connection disconnect. Retrying...
	==> web: Machine booted and ready!
	==> web: Checking for guest additions in VM...
	==> web: Setting hostname...
	==> web: Configuring and enabling network interfaces...
	The following SSH command responded with a non-zero exit status.
	Vagrant assumes that this means the command failed!
	
	/sbin/ifup eth1 2> /dev/null
	
	Stdout from the command:
	
	
	
	Stderr from the command:

Going into the VM, I saw that our second interface is called **enp0s8**:

	elatov@kmac:~/test$vagrant ssh web
	Last login: Thu Jun 12 13:35:06 2014 from 10.0.2.2
	Have a lot of fun...
	vagrant@web:~> ip link ls
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
	    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
	2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
	    link/ether 08:00:27:ef:b3:96 brd ff:ff:ff:ff:ff:ff
	3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
	    link/ether 08:00:27:66:36:06 brd ff:ff:ff:ff:ff:ff
	    
I saw an update on [github](https://github.com/mitchellh/vagrant/issues/1997) for vagrant to fix that. It's supposed to be fixed, but we would have to compile the vagrant software. I also ran into the [following](http://unix.stackexchange.com/questions/81834/how-can-i-change-the-default-ens33-network-device-to-old-eth0-on-fedora-19). From that page, we can pass a couple of parameters to the kernel to revert the old network interface names (**eth\***). From that site:

> The easiest way to restore the old way Kernel/modules/udev rename your ethernet interfaces is supplying these kernel parameters to Fedora 19:
> 
> 1. net.ifnames=0
> 2. biosdevname=0
> 
> To do so follow this steps:
> 
> 1. Edit /etc/default/grub
> 2. At the end of GRUB_CMDLINE_LINUX line append "net.ifnames=0 biosdevname=0"
> 3. Save the file
> 4. Type "grub2-mkconfig -o /boot/grub2/grub.cfg"
> 5. Type "reboot"

So let's try it out. Boot into the template VM and add those lines:

	vagrant@linux-nhp0:~> grep GRUB_CMDLINE_LINUX= /etc/default/grub
	GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"

Then rebuild the **initrd** again:

	vagrant@linux-nhp0:~> sudo mkinitrd
	
	Kernel image:   /boot/vmlinuz-3.11.10-11-default
	Initrd image:   /boot/initrd-3.11.10-11-default
	Root device:	/dev/systemVG/LVRoot (mounted on / as ext3)

Then before you reboot, copy the network scripts:

	vagrant@linux-nhp0:~>sudo mv /etc/sysconfig/network/ifcfg-enp0s3 /etc/sysconfig/network/ifcfg-eth0
	vagrant@linux-nhp0:~>sudo mv /etc/sysconfig/network/ifcfg-enp0s8 /etc/sysconfig/network/ifcfg-eth1

Then reboot the OS:

	vagrant@linux-nhp0:~> sudo reboot

After the reboot, you should see the new inteface names:

	vagrant@linux-nhp0:~> ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
	    inet 127.0.0.1/8 brd 127.255.255.255 scope host lo
	       valid_lft forever preferred_lft forever
	2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
	    inet 10.0.2.15/24 brd 10.0.2.255 scope global eth0
	       valid_lft forever preferred_lft forever
	3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
	    inet 192.168.56.101/24 brd 192.168.56.255 scope global eth1
	       valid_lft forever preferred_lft forever
	       
Making that into a box and trying again, the VMs booted up without issues :)

	elatov@kmac:~/test$vagrant up
	Bringing machine 'web' up with 'virtualbox' provider...
	Bringing machine 'db' up with 'virtualbox' provider...
	==> web: You assigned a static IP ending in ".1" to this machine.
	==> web: This is very often used by the router and can cause the
	==> web: network to not work properly. If the network doesn't work
	==> web: properly, try changing this IP.
	==> web: Importing base box 'elatov/opensuse13-64'...
	==> web: Matching MAC address for NAT networking...
	==> web: You assigned a static IP ending in ".1" to this machine.
	==> web: This is very often used by the router and can cause the
	==> web: network to not work properly. If the network doesn't work
	==> web: properly, try changing this IP.
	==> web: Checking if box 'elatov/opensuse13-64' is up to date...
	==> web: Setting the name of the VM: test_web_1402608608115_13797
	==> web: Clearing any previously set network interfaces...
	==> web: Preparing network interfaces based on configuration...
	    web: Adapter 1: nat
	    web: Adapter 2: hostonly
	==> web: Forwarding ports...
	    web: 22 => 2201 (adapter 1)
	    web: 22 => 2222 (adapter 1)
	==> web: Running 'pre-boot' VM customizations...
	==> web: Booting VM...
	==> web: Waiting for machine to boot. This may take a few minutes...
	    web: SSH address: 127.0.0.1:2222
	    web: SSH username: vagrant
	    web: SSH auth method: private key
	    web: Warning: Connection timeout. Retrying...
	    web: Warning: Remote connection disconnect. Retrying...
	    web: Warning: Remote connection disconnect. Retrying...
	==> web: Machine booted and ready!
	==> web: Checking for guest additions in VM...
	==> web: Setting hostname...
	==> web: Configuring and enabling network interfaces...
	==> web: Mounting shared folders...
	    web: /vagrant => /Users/elatov/Documents
	==> db: Importing base box 'elatov/opensuse13-64'...
	==> db: Matching MAC address for NAT networking...
	==> db: Checking if box 'elatov/opensuse13-64' is up to date...
	==> db: Setting the name of the VM: test_db_1402608694207_79161
	==> db: Fixed port collision for 22 => 2222. Now on port 2200.
	==> db: Clearing any previously set network interfaces...
	==> db: Preparing network interfaces based on configuration...
	    db: Adapter 1: nat
	    db: Adapter 2: hostonly
	==> db: Forwarding ports...
	    db: 22 => 2202 (adapter 1)
	    db: 22 => 2200 (adapter 1)
	==> db: Running 'pre-boot' VM customizations...
	==> db: Booting VM...
	==> db: Waiting for machine to boot. This may take a few minutes...
	    db: SSH address: 127.0.0.1:2200
	    db: SSH username: vagrant
	    db: SSH auth method: private key
	    db: Warning: Connection timeout. Retrying...
	    db: Warning: Remote connection disconnect. Retrying...
	    db: Warning: Remote connection disconnect. Retrying...
	==> db: Machine booted and ready!
	==> db: Checking for guest additions in VM...
	==> db: Setting hostname...
	==> db: Configuring and enabling network interfaces...
	==> db: Mounting shared folders...
	    db: /vagrant => /Users/elatov/Documents
	    

Both machines had the right IPs and the *virtualbox* share :

	elatov@kmac:~/test$for m in web db; do vagrant ssh $m -c 'ip -4 a s eth1; df -h -t vboxsf'; done
	3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
	    inet 192.168.33.1/24 brd 192.168.33.255 scope global eth1
	       valid_lft forever preferred_lft forever
	Filesystem      Size  Used Avail Use% Mounted on
	none            414G  217G  198G  53% /vagrant
	Connection to 127.0.0.1 closed.
	3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
	    inet 192.168.33.2/24 brd 192.168.33.255 scope global eth1
	       valid_lft forever preferred_lft forever
	Filesystem      Size  Used Avail Use% Mounted on
	none            414G  217G  198G  53% /vagrant
	Connection to 127.0.0.1 closed.
