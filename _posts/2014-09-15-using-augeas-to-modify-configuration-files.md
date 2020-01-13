---
published: true
layout: post
title: "Using Augeas to Modify Configuration Files"
author: Karim Elatov
categories: [os]
tags: [puppet,augeas]
---
As I was playing around with puppet, I also ran into **augeas**. **Augeas** is a powerful configuration editor, actually for [their](http://augeas.net/) main site:


> Augeas is a configuration editing tool. It parses configuration files in their native formats and transforms them into a tree. Configuration changes are made by manipulating this tree and saving it back into native config files.

**Augeas** uses *lenses* (modules) to identify configuration files and determines available options for that configuration file. A list of all the built-in *lenses* are seen in [Stock lenses](http://augeas.net/stock_lenses.html).


### Testing out the Command Line
Before we can start using the **augeas** provider with puppet we need to figure out how the setting is actually modified with the **augeas** library directly. I usually end up using **augtool** to load the configuration manually and once I figure out what I need to know, then I use the **augeas** provider. Here is an example of modifying a JSON file:

	$ augtool -A
	augtool> set /augeas/load/Json/lens Json.lns
	augtool> set /augeas/load/Json/incl /var/lib/transmission/.config/settings.json
	augtool> load
	augtool> print /files/var/lib/transmission/.config/settings.json/dict/entry[.= "watch-dir"]/string
	/files/var/lib/transmission/.config/settings.json/dict/entry[98]/string = "/data/t_down"
	augtool> set /files/var/lib/transmission/.config/settings.json/dict/entry[.= "watch-dir"]/string "/data/test"
	augtool> print /files/var/lib/transmission/.config/settings.json/dict/entry[.= "watch-dir"]/string
	/files/var/lib/transmission/.config/settings.json/dict/entry[98]/string = "/data/test"

The first two commands load the appropriate *lense* and associate a file with that *lense*. Then we load the configuration and check the settings. After we see that the *lense* was appropratiately loaded, then we make a change to the configuration inside the file. Here is one more example:

	$ sudo augtool -A
	augtool> set /augeas/load/Yum/lens Yum.lns
	augtool> set /augeas/load/Yum/incl /etc/yum.repos.d/epel.repo
	augtool> load
	augtool> print /files
	/files
	/files/etc
	/files/etc/yum.repos.d
	/files/etc/yum.repos.d/epel.repo
	/files/etc/yum.repos.d/epel.repo/epel
	/files/etc/yum.repos.d/epel.repo/epel/name = "Extra Packages for Enterprise Linux 7 - $basearch"
	/files/etc/yum.repos.d/epel.repo/epel/mirrorlist = "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-7&arch=$basearch"
	/files/etc/yum.repos.d/epel.repo/epel/enabled = "1"
	/files/etc/yum.repos.d/epel.repo/epel/gpgcheck = "1"
	/files/etc/yum.repos.d/epel.repo/epel/gpgkey = "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7"
	/files/etc/yum.repos.d/epel.repo/epel/failovermethod = "priority"
	/files/etc/yum.repos.d/epel.repo/epel/exclude[1] = "puppet*"
	/files/etc/yum.repos.d/epel.repo/epel/exclude[2] = "*augeas*"
	augtool> set /files/etc/yum.repos.d/epel.repo/epel/includepkgs "ossec-hids*"
	augtool> print /files
	/files
	/files/etc
	/files/etc/yum.repos.d
	/files/etc/yum.repos.d/epel.repo
	/files/etc/yum.repos.d/epel.repo/epel
	/files/etc/yum.repos.d/epel.repo/epel/name = "Extra Packages for Enterprise Linux 7 - $basearch"
	/files/etc/yum.repos.d/epel.repo/epel/mirrorlist = "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-7&arch=$basearch"
	/files/etc/yum.repos.d/epel.repo/epel/enabled = "1"
	/files/etc/yum.repos.d/epel.repo/epel/gpgcheck = "1"
	/files/etc/yum.repos.d/epel.repo/epel/gpgkey = "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7"
	/files/etc/yum.repos.d/epel.repo/epel/failovermethod = "priority"
	/files/etc/yum.repos.d/epel.repo/epel/exclude[1] = "puppet*"
	/files/etc/yum.repos.d/epel.repo/epel/exclude[2] = "*augeas*"
	/files/etc/yum.repos.d/epel.repo/epel/includepkgs = "ossec-hids*"
	/files/etc/yum.repos.d/epel.repo/includepkg = "ossec-hids*"
	augtool> save
	Saved 1 file(s)

Here we load a yum repository file and add a new configuration line. After that we can confirm the change persisted:

	[vagrant@pup-node1 ~]$ cat /etc/yum.repos.d/epel.repo
	[epel]
	name=Extra Packages for Enterprise Linux 7 - $basearch
	mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-7&arch=$basearch
	enabled=1
	gpgcheck=1
	gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
	failovermethod=priority
	exclude=puppet* *augeas*
	includepkgs=ossec-hids*

You can also match configurations using a **star** (*) parameter. For instance here is an example for removing an **ipv6** host entry:

	# augtool -A
	augtool> set /augeas/load/hosts/lens Hosts.lns
	augtool> set /augeas/load/hosts/incl /etc/hosts
	augtool> load
	augtool> print /files/etc/hosts
	/files/etc/hosts
	/files/etc/hosts/1
	/files/etc/hosts/1/ipaddr = "127.0.0.1"
	/files/etc/hosts/1/canonical = "localhost"
	/files/etc/hosts/2
	/files/etc/hosts/2/ipaddr = "127.0.1.1"
	/files/etc/hosts/2/canonical = "pup-node2.me"
	/files/etc/hosts/2/alias = "pup-node2"
	/files/etc/hosts/#comment = "The following lines are desirable for IPv6 capable hosts"
	/files/etc/hosts/3
	/files/etc/hosts/3/ipaddr = "::1"
	/files/etc/hosts/3/canonical = "localhost"
	/files/etc/hosts/3/alias[1] = "ip6-localhost"
	/files/etc/hosts/3/alias[2] = "ip6-loopback"
	augtool> print /files/etc/hosts/*[ipaddr = '::1']
	/files/etc/hosts/3
	/files/etc/hosts/3/ipaddr = "::1"
	/files/etc/hosts/3/canonical = "localhost"
	/files/etc/hosts/3/alias[1] = "ip6-localhost"
	/files/etc/hosts/3/alias[2] = "ip6-loopback"
	augtool> rm /files/etc/hosts/*[ipaddr = '::1']
	rm : /files/etc/hosts/*[ipaddr = '::1'] 5
	augtool> print /files/etc/hosts
	/files/etc/hosts
	/files/etc/hosts/1
	/files/etc/hosts/1/ipaddr = "127.0.0.1"
	/files/etc/hosts/1/canonical = "localhost"
	/files/etc/hosts/2
	/files/etc/hosts/2/ipaddr = "127.0.1.1"
	/files/etc/hosts/2/canonical = "pup-node2.me"
	/files/etc/hosts/2/alias = "pup-node2"
	/files/etc/hosts/#comment = "The following lines are desirable for IPv6 capable hosts"

### Augeas Generic Lenses
There is a list of generic modules list in [Using the Augeas Resource Type](https://puppet.com/docs/puppet/5.5/resources_augeas.html) and in [this](https://www.redhat.com/archives/augeas-devel/2012-March/msg00013.html) RedHat Forum. Here is a list from the former:

- Json.lns: parses JSON, available in Augeas 0.7.0
- Phpvars.lns: parses simple PHP source files used as configs containing “**$key = ‘value’;**”, available in Augeas 0.3.5 (improved in 0.10.0)
- Properties.lns: parses Java properties files, available in Augeas 0.9.0
- Puppet.lns: a generic INI file lens used for puppet.conf, available in Augeas 0.3.1 (see Dput.lns, MySQL.lns for variations)
- Shellvars.lns: parses shell-compatible “**KEY=value**” files such as /etc/sysconfig/*, available since forever though syntax support is regularly improved
- Shellvars_list.lns: same as Shellvars, but splits up values based on whitespace (**KEY=’value1 value2 value3’**), available in Augeas 0.7.2
- Simplevars.lns: parses “**key = value**” files such as wgetrc, available in Augeas 1.0.0
- Simplelines.lns: parses “**key1\nkey2\nkey3**” files such as cron.allow/deny, available in Augeas 1.0.0
- Spacevars.simple_lns: parses simple “**key value**” (space separated) files such as ldap.conf, available in Augeas 0.3.2
- Xml.lns: parses XML, available in Augeas 0.8.0

For example when I was working with FreeBSD machine I ended up using the following configuration:

	augeas{ "rc_conf_setting_pf_enabled":
		incl    => "/etc/rc.conf",
		lens    => 'Shellvars.lns',
		context => "/files/etc/rc_conf",
		changes => "set pf_enabled '\"TRUE\"'",
		onlyif  => "match pf_enabled not_include TRUE",
	}

### Appending to Configuration file
**Augeas** has a **last()** function, which basically represents the last config entry. This comes in pretty useful, when you are adding new configuration entries. For example here is what I did to enable an apache configuration for a Zabbix Server by appending the new config to the end:

	augeas { "${module_name}-modify-php-timezone":
	      lens       => 'Httpd.lns',
	      incl       => '/etc/zabbix/apache.conf',
	      context    => '/files/etc/zabbix/apache.conf',
	      changes    => ["set Directory[arg = '\"/usr/share/zabbix\"']/directive[last()+1] 'php_value'",
	                     "set Directory[arg = '\"/usr/share/zabbix\"']/directive[last()]/arg[1] 'date.timezone'",
	                     "set Directory[arg = '\"/usr/share/zabbix\"']/directive[last()]/arg[2] 'America/Denver'",],
	      onlyif     => "match Directory/directive[arg = 'America/Denver'] size < 1 ",
	    }

The above basically appends a new configuration, only if it sees that the Timezone hasn't been set yet. It took me a while to figure out the quotes, but after working through that, it's pretty nifty.

### Using Augeas in Defintions
I ran into a great slide deck [Configuration Surgery with Augeas](http://www.slideshare.net/PuppetLabs/configuration-with-augeas), which suggested to wrap the **augeas** provider into a definition, which really makes sense. I started to create hashes of configurations and then passing the keys, hash, and configuration file into the definition. Here is a all-in-one example:

	$rc_conffile  = '/etc/rc.conf'
	$config	      = { 'rc_conf'  => { 'sendmail_enable'           => 'NO',
	                                  'sendmail_submit_enable'    => 'NO',
	                                  'sendmail_outbound_enable'  => 'NO',
	                                  'sendmail_msp_queue_enable' => 'NO',
	                                  'exim_enable'               => 'YES', 
	                                 },
	                }
	                
	$rc_conf_keys = keys($config['rc_conf'])
	
	settings { $rc_conf_keys:
		config_file     => $rc_conffile,
		settings_hash   => $config['rc_conf'],
	}
	
	define settings (
	    $key               = $title,
	    $settings_hash,
	    $config_file,
	) {
	
	  $value = $settings_hash[$key]
	
		augeas{"${config_file}_setting_${key}":
			incl    => "${config_file}",
			lens    => 'Shellvars.lns',
			context => "/files${config_file}",
			changes => "set ${key} '\"${value}\"'",
			onlyif  => "match ${key} not_include ${value}",
		}
	}                

This way it basically does a **for** loop over all the keys and sets **key = value** inside the config file that you pass (**/etc/rc.conf**) into the defined type (in my case it's called **settings**). I tend to split the above up into the **params.pp**, **config.pp**, and **settings.pp** manifests (I discussed this briefly in [Writing Better Puppet Modules](/2014/09/writing-better-puppet-modules/))

### Other Augeas Providers
In the puppet forge there are a bunch of other providers, the popular one is [domcleal/augeasproviders](https://forge.puppetlabs.com/domcleal/augeasproviders), it includes a variety of custom **augeas** providers, here is a list from their page:
			
- apache_directive
- apache_setenv
- host
- kernel_parameter (grub)
- kernel_parameter (grub2)
- mailalias
- mounttab (fstab)
- mounttab (vfstab)
- nrpe_command
- pg_hba
- puppet_auth
- shellvar
- sshd_config
- sshd_config_subsystem
- sysctl
- syslog (augeas)
- syslog (rsyslog)

I have actually used the **grub2** one and works quite well. The same team provides pretty good instructions on how to load a specific file: [Loading specific files](https://github.com/hercules-team/augeas/wiki/Loading-specific-files)
