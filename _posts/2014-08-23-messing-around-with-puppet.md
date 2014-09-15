---
published: true
layout: post
title: "Messing Around with Puppet"
author: Karim Elatov
categories: [os]
tags: [puppet,linux,centos,augeas]
---
I usually have a couple of standard steps that I do on my Linux machines. Since CentOS 7 just released came out, instead of do an upgrade I decide to see if I can just use **puppet** to apply the necessary configurations to a brand new install. Here are all the steps I end up doing. This was just to play with the functionality of puppet. My modules are poorly written and I will cover how to write better puppet modules later. For now let's see what I was able to accomplish.

### Remove *rhgb* from the GRUB config
Luckily there is a module to handle this,  [herculesteam/augeasproviders_grub](https://forge.puppetlabs.com/herculesteam/augeasproviders_grub). The module is a provider for [augeas](http://augeas.net/index.html) so make sure you have that installed prior to using it:

	[elatov@puppet ~]$ rpm -qa | grep augeas
	ruby-augeas-0.4.1-3.el7.x86_64
	augeas-libs-1.1.0-12.el7.x86_64
	
Then go ahead and install the module:

	[elatov@puppet ~]$puppet module install herculesteam-augeasproviders_grub

After that I just added the following to my node:

	kernel_parameter { "rhgb":
			ensure => absent,
	   }

I decided to make a backup of **/etc/sysconfig/grub** (which is a symlink to **/etc/default/grub**) before making any changes and here is what I saw:

	[root@pup-node1 ~]# cp /etc/sysconfig/grub /etc/sysconfig/grub.orig
	[root@pup-node1 ~]# puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Warning: Found multiple default providers for kernel_parameter: grub2, grub; using grub2
	Info: Applying configuration version '1408809198'
	Notice: /Stage[main]/Main/Node[pup-node1.dnsd.me]/Kernel_parameter[rhgb]/ensure: removed
	Notice: Finished catalog run in 7.23 seconds
	[root@pup-node1 ~]# diff /etc/sysconfig/grub /etc/sysconfig/grub.orig 
	6c6
	< GRUB_CMDLINE_LINUX="rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us quiet net.ifnames=0 biosdevname=0"
	---
	> GRUB_CMDLINE_LINUX="rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us rhgb quiet net.ifnames=0 biosdevname=0"
	
That was perfect. There was a warning about having two providers. I ended up removing the **grub** provider cause I didn't have any machine using the legacy GRUB:

	[elatov@puppet ~]$ sudo mv /etc/puppet/modules/augeasproviders_grub/lib/puppet/provider/kernel_parameter/grub.rb /tmp/.

And after that the warning went away. There was also a description on *serverfault* on how to remove any kernel parameter from the grub configuration manually, check out [this](http://serverfault.com/questions/554092/how-to-update-grub-with-puppet) page for more information (there is also the augeas method, for more information check out [Using augeas and puppet to modify grub.conf](https://www.ghostar.org/2014/07/using-augeas-and-puppet-to-modify-grub-conf/)). 

### Remove Extraneous Packages
This one was pretty easy, we can just pass in an array to the package resource and it will take care of the rest:

	$pack_remove = [ "NetworkManager-glib", "NetworkManager", "avahi", "firewalld","ModemManager-gliqb", "teamd","xfsprogs","wpa_supplicant", "alsa-lib"]

	package { "$pack_remove":
		ensure => "absent",
	}


Upon testing the manifest, I received the following warning:

	[root@pup-node1 ~]# puppet agent -t
	Notice: Ignoring --listen on onetime run
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Warning: The package type's allow_virtual parameter will be changing its default value from false to true in a future release. If you do not want to allow virtual packages, please explicitly set allow_virtual to false.
	   (at /usr/share/ruby/vendor_ruby/puppet/type.rb:816:in `set_default')
	Info: Applying configuration version '1408814634'
	Notice: /Stage[main]/Main/Node[pup-node1.dnsd.me]/Package[teamd]/ensure: removed
	Notice: Finished catalog run in 1.56 seconds

There is a discussion puppetlabs that describes how to get around the issue. Here is a [link](https://ask.puppetlabs.com/question/6640/warning-the-package-types-allow_virtual-parameter-will-be-changing-its-default-value-from-false-to-true-in-a-future-release/) to page, there are a couple of fixes for the above warning:

	if versioncmp($::puppetversion,'3.6.1') >= 0 {

	  $allow_virtual_packages = hiera('allow_virtual_packages',false)

	  Package {
		allow_virtual => $allow_virtual_packages,
	  }
	}

Or just the following:

	Package {  allow_virtual => false, }

Rather than filling up the **site.pp** file I decided to write a quick module to take in an array and remove all the packages in the array and disable **allow_virtual** option if above a certain version of puppet. Here is the module's **init.pp** file :

	[root@puppet ~]# cat /etc/puppet/modules/rmpkg/manifests/init.pp 
	class rmpkg ($pkgs){
		if versioncmp($::puppetversion,'3.6.1') >= 0 {
		$allow_virtual_packages = hiera('allow_virtual_packages',false)
		Package { allow_virtual => $allow_virtual_packages, }
		}

		validate_array($pkgs)
		package { $pkgs: ensure => absent }
	}

And here is what I had in the **site.pp**:

	$pack_remove = [ "NetworkManager-glib", "NetworkManager", "avahi", "firewalld","ModemManager-glib", "teamd","xfsprogs","wpa_supplicant", "alsa-lib"]

	class { 'rmpkg':
		pkgs => $pack_remove
	 }
	 
You could easily pass in another variable called  **state** and remove or add packages depending on **state** variable. Here is how the apply looked like:

	[root@pup-node1 ~]# puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1408817075'
	Notice: /Stage[main]/Rmpkg/Package[teamd]/ensure: removed
	Notice: Finished catalog run in 1.35 seconds

And the warning is gone. The best way to do this would be with the **ensure_packages** function from the [stdlib](https://forge.puppetlabs.com/puppetlabs/stdlib) module. 

### Clean up */usr/local*

Usually there is a bunch of stuff in **/usr/local** that I clean up. So by default the directory structure looks like this:

	[vagrant@pup-node1 local]$ tree
	.
	├── bin
	├── etc
	├── games
	├── include
	├── lib
	├── lib64
	├── libexec
	├── sbin
	├── share
	│   ├── applications
	│   ├── info
	│   └── man
	│       ├── man1
	│       ├── man1x
	│       ├── man2
	│       ├── man2x
	│       ├── man3
	│       ├── man3x
	│       ├── man4
	│       ├── man4x
	│       ├── man5
	│       ├── man5x
	│       ├── man6
	│       ├── man6x
	│       ├── man7
	│       ├── man7x
	│       ├── man8
	│       ├── man8x
	│       ├── man9
	│       ├── man9x
	│       └── mann
	└── src

	32 directories, 0 files

They are all empty directories. I want to remove every directory except **bin** but **only if** the directory is empty.  I ended up writing a class with a new defined type. Here is how my class definition looked like:

	[root@puppet ~]# cat /etc/puppet/modules/clean_usr_local/manifests/init.pp 
	class clean_usr_local {

	  define rm_dir ($dir=$title) {
		exec { "rm_${$dir}":
		  path => "/bin:/usr/bin",
		  provider => "shell",
		  command => "rmdir ${dir}",
		  onlyif => "test -d ${dir} && test -z \"\$(ls -A ${dir})\"", 
		}
	 }

	  $man_dirs = [ "/usr/local/share/man/man1","/usr/local/share/man/man1x","/usr/local/share/man/man2","/usr/local/share/man/man2x","/usr/local/share/man/man3","/usr/local/share/man/man3x","/usr/local/share/man/man4","/usr/local/share/man/man4x","/usr/local/share/man/man5","/usr/local/share/man/man5x","/usr/local/share/man/man6","/usr/local/share/man/man6x","/usr/local/share/man/man7","/usr/local/share/man/man7x","/usr/local/share/man/man8","/usr/local/share/man/man8x","/usr/local/share/man/man9","/usr/local/share/man/man9x","/usr/local/share/man/mann"]
	  $share_dirs = ["/usr/local/share/applications","/usr/local/share/info","/usr/local/share/man"]
	  $other_dirs = ["/usr/local/lib","/usr/local/lib64","/usr/local/sbin","/usr/local/etc","/usr/local/games","/usr/local/include","/usr/local/libexec","/usr/local/src","/usr/local/share"]

	  rm_dir { $man_dirs:;
	  } ->  
	  rm_dir { $share_dirs:
	  }->  
	  rm_dir {$other_dirs:;}

	}
	
Then a simple `include clean_usr_local` in the **site.pp** for my node would take care of the rest. Here is the apply:

	[root@pup-node1 ~]# puppet agent -t 
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1408835700'
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man4x]/Exec[rm_/usr/local/share/man/man4x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/applications]/Exec[rm_/usr/local/share/applications]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/lib]/Exec[rm_/usr/local/lib]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/libexec]/Exec[rm_/usr/local/libexec]/returns: executed successfully
	Notice: Finished catalog run in 8.97 seconds

The **defined** type allows the **exec** to go through like a *for* loop. Check out the hint from [here](http://backdrift.org/puppet-foreach-for-loop-workaround). After it was applied here is how the directory looked like:

	[root@pup-node1 ~]# tree /usr/local
	/usr/local
	└── bin

	1 directory, 0 files

If you don't care about the contents, you could always just **exec** "rm -rf", but that would too easy.

### Add the *wheel* group to be part of *sudoers*
Luckily there is a **puppet** module for that: it's [saz/sudo](https://forge.puppetlabs.com/saz/sudo). So on the puppet master let's go ahead and install it:

	[root@puppet ~]# puppet module install saz/sudo
	Notice: Preparing to install into /etc/puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/etc/puppet/modules
	└─┬ saz-sudo (v3.0.6)
	  └── puppetlabs-stdlib (v4.3.2)
	  
Then in the **site.pp**, I just added the following:

	class { 'sudo': 
		config_file_replace => false,
	}
	sudo::conf { 'admins':
		priority => 10,
		content  => "%wheel ALL=(ALL) ALL",
	}

Here is the pull from the master:

	[root@pup-node1 etc]# puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1408839651'
	Notice: /Stage[main]/Sudo/File[/etc/sudoers.d/]/mode: mode changed '0750' to '0550'
	Notice: /Stage[main]/Main/Node[pup-node1.dnsd.me]/Sudo::Conf[admins]/File[10_admins]/ensure: created
	Info: /Stage[main]/Main/Node[pup-node1.dnsd.me]/Sudo::Conf[admins]/File[10_admins]: Scheduling refresh of Exec[sudo-syntax-check for file /etc/sudoers.d/10_admins]
	Notice: /Stage[main]/Main/Node[pup-node1.dnsd.me]/Sudo::Conf[admins]/Exec[sudo-syntax-check for file /etc/sudoers.d/10_admins]: Triggered 'refresh' from 1 events
	Notice: Finished catalog run in 5.27 seconds

Then making sure the user that is part of the **wheel** group can run **sudo**:

	[root@pup-node1 ~]# sudo su - elatov
	Last login: Sat Aug 23 18:24:39 MDT 2014 on pts/1
	[elatov@pup-node1 ~]$ sudo -l
	[sudo] password for elatov: 
	Matching Defaults entries for elatov on this host:
		!requiretty, !visiblepw, always_set_home, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE INPUTRC KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE
		LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY", secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

	User elatov may run the following commands on this host:
		(ALL) ALL

It just creates a new config under **/etc/sudoers.d/** with the appropriate configurations:

	[root@pup-node1 ~]# cat /etc/sudoers.d/10_admins 
	%wheel ALL=(ALL) ALL

and it doesn't change the configuration file under **/etc/sudoers**.

### Apply an *iptables* Firewall
There are a couple of modules out there, but at home I have a pretty standard approach to **iptables** so I decided to have the puppet master host the **iptables** rules per node and also a default iptables ruleset as well. Here is the class that I put together:

	[elatov@puppet ~]$ cat /etc/puppet/modules/my_iptables/manifests/init.pp 
	class my_iptables ($host) {
	  case $::operatingsystem {
		/(?i:CentOS)/: { 
		  if ($::operatingsystemmajrelease == '7') { 
			$iptables_pkg = 'iptables-services'
			$iptables_config = '/etc/sysconfig/iptables'
			$iptables_service = 'iptables'
			$remove_firewalld = true
			$iptables_config_source = "puppet:///modules/my_iptables/${host}-iptables-conf"
		  } else { 
			$iptables_pkg = 'iptables'
			$iptables_config = '/etc/sysconfig/iptables'
			$iptables_service = 'iptables'
			$iptables_config_source = "puppet:///modules/my_iptables/${host}-iptables-conf"
		  }
		}
		/(?i:fedora)/: { 
		  $iptables_pkg = 'iptables-services'
		  $iptables_config = '/etc/sysconfig/iptables'
		  $iptables_service = 'iptables'
		  $remove_firewalld = true
		  $iptables_config_source = "puppet:///modules/my_iptables/${host}-iptables-conf"
		}
		/(?i:Debian|Ubuntu)/: { 
		  $iptables_pkg = 'iptables-persistent'
		  $iptables_config = '/etc/iptables/rules.v4'
		  $iptables_service = 'iptables-persistent'
		  $iptables_config_source = "puppet:///modules/my_iptables/${host}-iptables-conf"
		}
		default: {
		  $iptables_pkg = 'iptables'
		  $iptables_config = '/etc/sysconfig/iptables'
		  $iptables_config_source = "puppet:///modules/my_iptables/def-iptables-conf"
		}
	  }
	  if ($remove_firewalld) {
		package {'firewalld':
		  ensure => "absent",
		}
	  }
	  package { "$iptables_pkg":
		ensure => "present",
	  }

	  service { "$iptables_service":
		enable => true,
		ensure => "running",
	  }


	  # Debug
	  #notify {"here are my configs source = $iptables_config_source iptables_pkg = $iptables_pkg iptables_config_file = $iptables_config iptables_service = $iptables_service":;}
	  file { "iptables.conf":
		ensure => file,
		path => $iptables_config,
		source => $iptables_config_source,
		require => Package [$iptables_pkg],
		notify => Service [$iptables_service],
		owner => root,
		group => root,
	  }

Then in the **site.pp** manifest file, I added the following to my node:

	class { 'my_iptables': 
			host => 'm2',
	}

And I had the corresponding firewall under the modules directory:

	[elatov@puppet ~]$ ls /etc/puppet/modules/my_iptables/files/m2-iptables-conf 
	/etc/puppet/modules/my_iptables/files/m2-iptables-conf

Here is the apply with the new firewall in place:

	[root@pup-node1 ~]# puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1408925933'
	Notice: /Stage[main]/My_iptables/File[iptables.conf]/content: 
	--- /etc/sysconfig/iptables	2014-06-09 23:02:35.000000000 -0600
	+++ /tmp/puppet-file20140824-14610-1fas3rd	2014-08-24 18:19:44.131478423 -0600
	@@ -1,14 +1,28 @@
	-# sample configuration for iptables service
	-# you can edit this manually or use system-config-firewall
	-# please do not ask us to add additional ports/services to this default configuration
	+# Firewall configuration written by system-config-firewall
	+# Manual customization of this file is not recommended.
	 *filter
	 :INPUT ACCEPT [0:0]
	 :FORWARD ACCEPT [0:0]
	 :OUTPUT ACCEPT [0:0]
	--A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
	+-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	 -A INPUT -p icmp -j ACCEPT
	 -A INPUT -i lo -j ACCEPT
	--A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
	+-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
	+-A INPUT -p tcp -m state --state NEW -m tcp --dport 10050 -j ACCEPT
	+#-A INPUT -j LOG --log-prefix "FW-REJECT " --log-level warning
	 -A INPUT -j REJECT --reject-with icmp-host-prohibited
	--A FORWARD -j REJECT --reject-with icmp-host-prohibited
	 COMMIT

	Info: /Stage[main]/My_iptables/File[iptables.conf]: Filebucketed /etc/sysconfig/iptables to puppet with sum e628a913aa0d84645947744ea55d8556
	Notice: /Stage[main]/My_iptables/File[iptables.conf]/content: content changed '{md5}e628a913aa0d84645947744ea55d8556' to '{md5}fbb20b030ceb997e0578d7b56a490289'
	Info: /Stage[main]/My_iptables/File[iptables.conf]: Scheduling refresh of Service[iptables]
	Notice: /Stage[main]/My_iptables/Service[iptables]: Triggered 'refresh' from 1 events
	Notice: Finished catalog run in 5.89 seconds

Double checking and my new rule was in place:

	[root@pup-node1 ~]# iptables -L -n -v | grep 10050
		0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:10050

### Disable Selinux
There is actually a module for this as well. So let's go ahead and install it on the puppet master:

	[elatov@puppet ~]$ sudo puppet module install spiette-selinux
	Notice: Preparing to install into /etc/puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/etc/puppet/modules
	└── spiette-selinux (v0.5.4)

To disable selinux for the node, we just have to add the following to the node definition:

	class { 'selinux':
	   mode => 'permissive'
	}

Here is the apply from the node:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Error: Could not retrieve catalog from remote server: Error 400 on SERVER: comparison of String with 7 failed at /etc/puppet/modules/selinux/manifests/params.pp:16 on node pup-node1.dnsd.me
	Warning: Not using cache on failed catalog
	Error: Could not retrieve catalog; skipping run
	
It looks like **line 16** is having an issue, let's check out that line:

	[elatov@puppet ~]$ sed -n '16 p' /etc/puppet/modules/selinux/manifests/params.pp
		  if $::operatingsystemrelease < '7' {
		  
Checking out the **facts** on the node, I saw the following:

	[vagrant@pup-node1 ~]$ sudo facter | grep -i release
	bios_release_date => 12/01/2006
	kernelrelease => 3.10.0-123.6.3.el7.x86_64
	operatingsystemmajrelease => 7
	operatingsystemrelease => 7.0.1406
	
It looks like the **operatingsystemrelease** *fact* is seen as a string since it contains periods, so let's just use the **operatingsystemmajrelease** *fact* instead. After fixing that line, I saw the following:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409333297'
	Notice: /Stage[main]/Selinux/File[/var/lib/puppet/selinux]/ensure: created
	Notice: /Stage[main]/Selinux::Config/File[/etc/selinux/config]/content: 
	--- /etc/selinux/config	2014-08-29 10:59:02.220037885 -0600
	+++ /tmp/puppet-file20140829-2251-1r9d6ci	2014-08-29 11:28:22.285064483 -0600
	@@ -4,11 +4,9 @@
	 #     enforcing - SELinux security policy is enforced.
	 #     permissive - SELinux prints warnings instead of enforcing.
	 #     disabled - No SELinux policy is loaded.
	-SELINUX=permissive
	+SELINUX=disabled
	 # SELINUXTYPE= can take one of these two values:
	 #     targeted - Targeted processes are protected,
	 #     minimum - Modification of targeted policy. Only selected processes are protected. 
	 #     mls - Multi Level Security protection.
	 SELINUXTYPE=targeted 
	-
	-

	Info: /Stage[main]/Selinux::Config/File[/etc/selinux/config]: Filebucketed /etc/selinux/config to puppet with sum 9743cfd3d26e1f5ff815213185103e0e
	Notice: /Stage[main]/Selinux::Config/File[/etc/selinux/config]/content: content changed '{md5}9743cfd3d26e1f5ff815213185103e0e' to '{md5}028229ec717ba63a39f2f4233ba3626c'
	Notice: /Stage[main]/Selinux::Config/File[/etc/selinux/config]/mode: mode changed '0644' to '0444'
	Notice: Finished catalog run in 5.06 seconds
	
That looks good.

### Disable IPv6
We can just drop a file under **/etc/sysctl.d** with all the necessary configuration. There is another module that uses augeas ([domcleal-augeasproviders](https://forge.puppetlabs.com/domcleal/augeasproviders)) that can handle **sysctl** configurations as well. So let's grab the module:

	[elatov@puppet ~]$ sudo puppet module install domcleal/augeasproviders
	Notice: Preparing to install into /etc/puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/etc/puppet/modules
	└─┬ domcleal-augeasproviders (v1.2.0)
	  └── puppetlabs-stdlib (v4.3.2)


Using that module I used the following to apply the configuration:

	class { 'augeasproviders::instances':
		sysctl_hash => { 'net.ipv6.conf.all.disable_ipv6' => { 
			'value' => '1',
			'target' => "/etc/sysctl.d/90-dis_ipv6.conf",
			},
		'net.ipv6.conf.default.disable_ipv6' => { 
			'value' => '1',
			'target' => "/etc/sysctl.d/90-dis_ipv6.conf",  
			},
		},
	}

And the apply from the node:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409337780'
	Notice: /Stage[main]/Augeasproviders::Instances/Sysctl[net.ipv6.conf.default.disable_ipv6]/ensure: created
	Notice: /Stage[main]/Augeasproviders::Instances/Sysctl[net.ipv6.conf.all.disable_ipv6]/ensure: created
	Notice: Finished catalog run in 5.20 seconds

We can also confirm the settings are in place:

	[vagrant@pup-node1 ~]$ cat /etc/sysctl.d/90-dis_ipv6.conf 
	net.ipv6.conf.default.disable_ipv6 = 1
	net.ipv6.conf.all.disable_ipv6 = 1

we can also confirm the settings were applied on the system:

	[vagrant@pup-node1 ~]$ sudo sysctl -a | grep -i disable_ipv6
	net.ipv6.conf.all.disable_ipv6 = 1
	net.ipv6.conf.default.disable_ipv6 = 1

After that I needed to modify the **sshd_config** file to only use IPv4. On the node to see how the configuration looks like we can install **augeas** and use **augtool** on the config file. First for the install:

	[vagrant@pup-node1 ~]$ sudo yum install augeas

Now check the address option in the **sshd_config** file:

	[vagrant@pup-node1 ~]$ sudo augtool print /files/etc/ssh/sshd_config | grep -i address
	/files/etc/ssh/sshd_config/#comment[13] = "AddressFamily any"
	
We can see that it's currently commented out. So let's set **AddressFamily** to **inet** with augeas provider. Here is the puppet config I used:

	class { 'augeasproviders::instances':
		sshd_config_hash => { 'AddressFamily' => { 'ensure' => 'present','value'  => "inet",},},
		notify 		 => Service["sshd"],
		}
	}
	service { "sshd":
		name 	=> $operatingsystem ? {/(?i:Debian|Ubuntu)/ => "ssh",default => "sshd",},
		require => Class["augeasproviders::instances"],
		enable 	=> true,
		ensure 	=> running,
	}

Now let's back up the configuration and then apply the puppet changes:

	[vagrant@pup-node1 ~]$ sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.orig
	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409341068'
	Notice: /Stage[main]/Augeasproviders::Instances/Sshd_config[AddressFamily]/ensure: created
	Info: Class[Augeasproviders::Instances]: Scheduling refresh of Service[sshd]
	Notice: /Stage[main]/Dis_ipv6/Service[sshd]: Triggered 'refresh' from 1 events
	Notice: Finished catalog run in 6.98 seconds
	[vagrant@pup-node1 ~]$ sudo diff /etc/ssh/sshd_config /etc/ssh/sshd_config.orig
	19d18
	< AddressFamily inet

That looks correct, so now let's modify the **postfix** configuration to not use IPv6, here is the setting we have to modify:

	[vagrant@pup-node1 ~]$ sudo augtool print /files/etc/postfix/main.cf | grep -i protocols
	/files/etc/postfix/main.cf/inet_protocols = "all"
	
I didn't see an agueas provider for postfix so I decided to use the **augeas** resource from puppet directly. Here is what ended up using in puppet:

	augeas { "main_cf_config":
		context => "/files/etc/postfix/main.cf",
		changes => ["set inet_protocols ipv4",],
		notify => Service["postfix"],
	}

and here is the result on the node:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409347854'
	Notice: Augeas[main_cf_config](provider=augeas): 
	--- /etc/postfix/main.cf	2014-06-09 19:39:24.000000000 -0600
	+++ /etc/postfix/main.cf.augnew	2014-08-29 15:31:36.942338834 -0600
	@@ -116,7 +116,7 @@
	 inet_interfaces = localhost

	 # Enable IPv4, and IPv6 if supported
	-inet_protocols = all
	+inet_protocols = ipv4

	 # The proxy_interfaces parameter specifies the network interface
	 # addresses that this mail system receives mail on by way of a

	Notice: /Stage[main]/Dis_ipv6/Augeas[main_cf_config]/returns: executed successfully
	Info: /Stage[main]/Dis_ipv6/Augeas[main_cf_config]: Scheduling refresh of Service[postfix]
	Notice: /Stage[main]/Dis_ipv6/Service[postfix]: Triggered 'refresh' from 1 events
	Notice: Finished catalog run in 11.06 seconds

If you are planning to manage the postfix service with puppet it would be better to modify the ipv6 config there. This way you won't end up with duplicate declarations.

### Setup a cronjob
This was pretty easy, there is already a **cron** *type*. So just needed the following:

	package { "ntpdate":
		ensure => "present",
	}

	cron { "ntp":
		command => "/usr/sbin/ntpdate -s 0.north-america.pool.ntp.org",
		user => "root",
		minute => "05",
	}
	
Then the puppet test:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409352753'
	Notice: /Stage[main]/Cronjobs/Package[ntpdate]/ensure: created
	Notice: /Stage[main]/Cronjobs/Cron[ntp]/ensure: created
	Notice: Finished catalog run in 17.35 seconds

and finally to confirm:

	[vagrant@pup-node1 ~]$ sudo crontab -l
	# HEADER: This file was autogenerated at 2014-08-29 16:52:49 -0600 by puppet.
	# HEADER: While it can still be managed manually, it is definitely not recommended.
	# HEADER: Note particularly that the comments starting with 'Puppet Name' should
	# HEADER: not be deleted, as doing so could cause duplicate cron jobs.
	# Puppet Name: ntp
	5 * * * * /usr/sbin/ntpdate -s 0.north-america.pool.ntp.org

### Add the EPEL YUM repository
There is a module for this:

	[elatov@puppet ~]$ sudo puppet module install stahnma-epel
	Notice: Preparing to install into /etc/puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/etc/puppet/modules
	└── stahnma-epel (v0.1.1)

I wasn't overriding any parameters so I just included the class and then the puppet test did the rest:

	[vagrant@pup-node1 ~]$ sudo puppet agent -t
	Info: Retrieving pluginfacts
	Info: Retrieving plugin
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/facter_dot_d.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/pe_version.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/puppet_vardir.rb
	Info: Loading facts in /etc/puppet/modules/stdlib/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/facter_dot_d.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/root_home.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/puppet_vardir.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/pe_version.rb
	Info: Loading facts in /var/lib/puppet/lib/facter/os_maj_version.rb
	Info: Caching catalog for pup-node1.dnsd.me
	Info: Applying configuration version '1409353773'
	Notice: /Stage[main]/Epel/File[/etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7]/ensure: defined content as '{md5}58fa8ae27c89f37b08429f04fd4a88cc'
	Notice: /Stage[main]/Epel/Epel::Rpm_gpg_key[EPEL-7]/Exec[import-EPEL-7]/returns: executed successfully
	Notice: /Stage[main]/Epel/Yumrepo[epel-testing-debuginfo]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel-testing-debuginfo.repo from 600 to 644
	Notice: /Stage[main]/Epel/Yumrepo[epel-source]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel-source.repo from 600 to 644
	Notice: /Stage[main]/Epel/Yumrepo[epel]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel.repo from 600 to 644
	Notice: /Stage[main]/Epel/Yumrepo[epel-testing-source]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel-testing-source.repo from 600 to 644
	Notice: /Stage[main]/Epel/Yumrepo[epel-debuginfo]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel-debuginfo.repo from 600 to 644
	Notice: /Stage[main]/Epel/Yumrepo[epel-testing]/ensure: created
	Info: changing mode of /etc/yum.repos.d/epel-testing.repo from 600 to 644
	Notice: Finished catalog run in 8.04 seconds
	
Lastly to make sure I can install from the EPEL Repository:

	[vagrant@pup-node1 ~]$ sudo yum list cdpr
	Loaded plugins: fastestmirror
	Loading mirror speeds from cached hostfile
	 * base: centos.mirror.constant.com
	 * epel: mirrors.tummy.com
	 * extras: mirrors.unifiedlayer.com
	 * updates: repos.dfw.quadranet.com
	Available Packages
<<<<<<< HEAD:_posts/2014-08-23-messing-around-with-puppet.md
	cdpr.x86_64                            2.4-6.el7      epel

That's all that I needed to to. Let me reiterate that this is not the perfect setup and this is just what I did to start playing with puppet. Onto the next adventures.
=======
	cdpr.x86_64                            2.4-6.el7                            epel

# By this point you will realize that it's inevitable that you will have to write a puppet module. To get started check out [this](https://docs.puppetlabs.com/guides/module_guides/bgtm.html) page (there is good 3 part blog series [here](http://puppetlabs.com/blog/best-practices-building-puppet-modules) as well. The module should break down into 5 files:

1. init.pp
2. params.pp
3. install.pp
4. config.pp
5. service.pp

There are also tools out there to create templates of a module [puppet module skeletons](http://www.puppetbestpractices.com/modules/style/module-skeleton.html).

You will also notice that there are different methods to do ordering of the class execution. For example from [here](http://www.devco.net/archives/2012/12/13/simple-puppet-module-structure-redux.php):

class ntp(
   $version = "present",
   $ntpservers = ["1.pool.ntp.org", "2.pool.ntp.org"],
   $enable = true,
   $start = true
) {
   class{'ntp::install': } ->
   class{'ntp::config': } ~>
   class{'ntp::service': } ->
   Class["ntp"]
}

Or even the [first guide](https://docs.puppetlabs.com/guides/module_guides/bgtm.html) that I mentioned has the following:

Best practices recommend basing your requires, befores, and other ordering-related dependencies on classes rather than resources. Class-based ordering allows you to shield the implementation details of each class from the other classes. You can do things like:

    file { 'configuration':
      ensure  => present,
      require => Class['module::install'],
    }

and from the same guide, you can use containment and anchoring. Here is anchoring:

    Anchor['module::begin'] ->
      Class['module::install'] ->
      Class['module::config']  ->
      Class['module::service'] ->
    Anchor['module::end']

and here is containement:

class { 'ssh::server::install': } ->
  class { 'ssh::server::config': } ~>
  class { 'ssh::server::service': }

  contain ssh::server::install
  contain ssh::server::config
  contain ssh::server::service

If you decide to use the [first one](https://github.com/garethr/puppet-module-skeleton), you can just install it with the following commands:

git clone https://github.com/garethr/puppet-module-skeleton
cd puppet-module-skeleton
find skeleton -type f | git checkout-index --stdin --force --prefix="$HOME/.puppet/var/puppet-module/" --

Then creating a module template will look like this:

elatov@fed:~$puppet module generate test-test
Notice: Generating module at /home/elatov/test-test
test-test
test-test/.fixtures.yml
test-test/.gitignore
test-test/.rspec
test-test/.travis.yml
test-test/CHANGELOG
test-test/CONTRIBUTING.md
test-test/CONTRIBUTORS
test-test/Gemfile
test-test/Guardfile
test-test/LICENSE
test-test/Modulefile
test-test/README.markdown
test-test/Rakefile
test-test/files
test-test/files/.gitkeep
test-test/lib
test-test/lib/puppet
test-test/lib/puppet/provider
test-test/lib/puppet/provider/.gitkeep
test-test/lib/puppet/type
test-test/lib/puppet/type/.gitkeep
test-test/manifests
test-test/manifests/config.pp
test-test/manifests/init.pp
test-test/manifests/install.pp
test-test/manifests/params.pp
test-test/manifests/service.pp
test-test/metadata.json
test-test/spec
test-test/spec/acceptance
test-test/spec/acceptance/class_spec.rb
test-test/spec/acceptance/nodesets
test-test/spec/acceptance/nodesets/centos-64-x64.yml
test-test/spec/acceptance/nodesets/default.yml
test-test/spec/acceptance/nodesets/ubuntu-server-12042-x64.yml
test-test/spec/classes
test-test/spec/classes/coverage_spec.rb
test-test/spec/classes/example_spec.rb
test-test/spec/spec_helper.rb
test-test/spec/spec_helper_acceptance.rb
test-test/templates
test-test/templates/.gitkeep
test-test/tests
test-test/tests/init.pp

Now you can import that directory into geppetto and modify the 5 files that we menetinoed before.

### augeas notes
http://www.slideshare.net/PuppetLabs/configuration-with-augeas
http://serverfault.com/questions/314847/appending-a-line-to-a-file-if-it-doesnt-exist-using-puppet
http://projects.puppetlabs.com/projects/1/wiki/puppet_augeas
https://github.com/hercules-team/augeas/wiki/Loading-specific-files

# sometimes using a generic ini module is helpful
https://www.redhat.com/archives/augeas-devel/2012-March/msg00013.html

# all the stock lenses
http://augeas.net/stock_lenses.html

# why is editing per line better
http://stackoverflow.com/questions/14885267/why-config-files-shouldt-be-changed-line-by-line-with-chef-puppet
##
##

## Bloated params
http://garylarizza.com/blog/2013/12/08/when-to-hiera/
>>>>>>> 39cc5e8c905bf2993e22d8736f5ee30a90dbed68:_posts/2014-08-23-my-puppet-notes-for-centos-7.md
