---
published: false
layout: post
title: "My Puppet Notes For CentOS 7"
author: Karim Elatov
categories: []
tags: []
---
I usually have a couple of standard steps that I do on my Linux machines. Since CentOS 7 just released came out, instead of do an upgrade I decide to see if I can just use puppet to apply the necessary configurations to a brand new install. Here are all the steps I end up doing.

### Remove *rhgb* from the GRUB config
Luckily there is a module to handle this,  [herculesteam/augeasproviders_grub](https://forge.puppetlabs.com/herculesteam/augeasproviders_grub). The module is a provider for [augeas](http://augeas.net/index.html) to make sure you have that installed prior to using it:

	[elatov@puppet ~]$ rpm -qa | grep augeas
	ruby-augeas-0.4.1-3.el7.x86_64
	augeas-libs-1.1.0-12.el7.x86_64
	
Then go ahead and install the module:

	[elatov@puppet ~]$puppet module install herculesteam-augeasproviders_grub

After that I just added the following to my node:

	kernel_parameter { "rhgb":
			ensure => absent,
	   }

I decided to make a backup of /etc/sysconfig/grub (which is a symlink to /etc/default/grub) before making any changes and here is what I saw:

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

And after that the warning went away. There was also a description on *serverfault* on how to do it manually, check out [this](http://serverfault.com/questions/554092/how-to-update-grub-with-puppet) page for more information. 

### Remove Estraneous Packages
This one was pretty easy, we can just pass in an array to the package resource and it will take care of the rest:

	$pack_remove = [ "NetworkManager-glib", "NetworkManager", "avahi", "firewalld","ModemManager-glib", "teamd","xfsprogs","wpa_supplicant", "alsa-lib"]

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

And the warning is gone. 

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
		  #onlyif => "[ -d ${dir} -a -z `ls -A ${dir}`]", 
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
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man4]/Exec[rm_/usr/local/share/man/man4]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man7]/Exec[rm_/usr/local/share/man/man7]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man2]/Exec[rm_/usr/local/share/man/man2]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man6x]/Exec[rm_/usr/local/share/man/man6x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man3]/Exec[rm_/usr/local/share/man/man3]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man3x]/Exec[rm_/usr/local/share/man/man3x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man5x]/Exec[rm_/usr/local/share/man/man5x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man2x]/Exec[rm_/usr/local/share/man/man2x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man8]/Exec[rm_/usr/local/share/man/man8]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man9x]/Exec[rm_/usr/local/share/man/man9x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man5]/Exec[rm_/usr/local/share/man/man5]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man1x]/Exec[rm_/usr/local/share/man/man1x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man6]/Exec[rm_/usr/local/share/man/man6]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man1]/Exec[rm_/usr/local/share/man/man1]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man8x]/Exec[rm_/usr/local/share/man/man8x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man9]/Exec[rm_/usr/local/share/man/man9]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/mann]/Exec[rm_/usr/local/share/man/mann]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man/man7x]/Exec[rm_/usr/local/share/man/man7x]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/applications]/Exec[rm_/usr/local/share/applications]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/man]/Exec[rm_/usr/local/share/man]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/share/info]/Exec[rm_/usr/local/share/info]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/src]/Exec[rm_/usr/local/src]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/lib64]/Exec[rm_/usr/local/lib64]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/etc]/Exec[rm_/usr/local/etc]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/sbin]/Exec[rm_/usr/local/sbin]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/include]/Exec[rm_/usr/local/include]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/games]/Exec[rm_/usr/local/games]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/lib]/Exec[rm_/usr/local/lib]/returns: executed successfully
	Notice: /Stage[main]/Clean_usr_local/Clean_usr_local::Rm_dir[/usr/local/libexec]/Exec[rm_/usr/local/libexec]/returns: executed successfully
	Notice: Finished catalog run in 8.97 seconds

The defined type allows the exec to go through like a forloop. Check out the hint from [here](http://backdrift.org/puppet-foreach-for-loop-workaround). After it was applied here is how the directory looked like:

	[root@pup-node1 ~]# tree /usr/local
	/usr/local
	└── bin

	1 directory, 0 files

### Add the *wheel* group to be part of *sudoers*
Luckily there is a puppet module for that: it's [saz/sudo](https://forge.puppetlabs.com/saz/sudo). So on the puppet master let's go ahead and install it:

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

Then making sure the user that is part of the **wheel** group can run sudo:

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
There are a couple of modules out there, but at home I have a pretty standard approach to iptables so I decided to have the puppet master host the iptables rules per node and also a default iptables ruleset as well. Here is the class that I put together:

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

Then in the site.pp manifest file, I added the following to my node:

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
