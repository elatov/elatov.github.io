---
published: true
layout: post
title: "Deploy Wordpress with Vagrant and Puppet Modules"
author: Karim Elatov
categories: [os]
tags: [vagrant,puppet,mac_os_x,virtualbox]
---
In my [previous](/2014/06/create-test-wordpress-instance-using-puppet-and-vagrant/) post I deployed a wordpress instance (DB and Web VMs) using almost only commands and only one puppet modules (**stdlib**). I decided to give it a shot with more modules to see if it's easier.

### Install Puppet MySQL module

Let's deploying a MySQL server using a puppet module. First let's install the MySQL puppet module:

	elatov@mac:~$puppet module install puppetlabs-mysql
	Notice: Preparing to install into /Users/elatov/.puppet/modules ...
	Notice: Created target directory /Users/elatov/.puppet/modules
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/Users/elatov/.puppet/modules
	└─┬ puppetlabs-mysql (v2.3.0)
	  └── puppetlabs-stdlib (v4.3.0)

Now let's create a vagrant environment:

	elatov@mac:~$mkdir db
	elatov@mac:~$cd db
	elatov@mac:~/db$vagrant box list
	elatov/opensuse13-64 (virtualbox, 0.0.1)
	elatov@mac:~/db$vagrant init elatov/opensuse13-64

Now let's modify the **VagrantFile** and modify the provisioner section to look in the correct location for the modules and the manifests:

	config.vm.provision "puppet" do |puppet|
	    puppet.manifests_path = "manifests"
	    puppet.manifest_file  = "db.pp"
	    puppet.module_path = "~/.puppet/modules"
	end
	    
Now let's create a manifest file for this db machine:

	elatov@mac:~/db$mkdir manifests
	elatov@mac:~/db$vi manifests/db.pp

and let's add the following into the file:

	### Global setttings
	Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
	
	$mysql_password = "testing"
	
	exec { "system-update":
	        command => "zypper update -y",
	        onlyif => "test $(facter uptime_seconds) -lt 300",
	}
	
	$mysql_password = "testing"
	$db_name = "wordpress_db"
	$db_user = "wordpress_user"
	$db_pass = "wordpress"
	$db_access = "192.168.33.%"
	
	class { '::mysql::server':
	  root_password    => $mysql_password,
	  override_options => { 'mysqld' => { 'bind-address' => $ipaddress_eth0 } }
	}
	
	mysql::db { $db_name :
	  user     => $db_user,
	  password => $db_pass,
	  host     => $db_access,
	  grant  => 'ALL',
	}
	
	
Upon running a `vagrant up`, I saw the following:

	==> default: Running provisioner: puppet...
	==> default: Running Puppet with db.pp...
	==> default: Notice: /Stage[main]/Mysql::Client::Install/Package[mysql_client]/ensure: created
	==> default: Notice: /Stage[main]/Mysql::Server::Install/Package[mysql-server]/ensure: created
	==> default: Notice: /Stage[main]/Mysql::Server::Config/File[/etc/mysql]/ensure: created
	==> default: Notice: /Stage[main]/Mysql::Server::Config/File[/etc/my.cnf]/content: content changed '{md5}b738b8a889b08ce1203901712bf653a9' to '{md5}331e8cbd1c1bf8a12bcb30e685b66349'
	==> default: Notice: /Stage[main]/Mysql::Server::Config/File[/etc/my.cnf]/group: group changed 'mysql' to 'root'
	==> default: Notice: /Stage[main]/Mysql::Server::Config/File[/etc/my.cnf]/mode: mode changed '0640' to '0644'
	==> default: Notice: /Stage[main]/Mysql::Server::Config/File[/etc/mysql/conf.d]/ensure: created
	==> default: Notice: /Stage[main]/Mysql::Server::Service/Service[mysqld]/ensure: ensure changed 'stopped' to 'running'
	==> default: Notice: /Stage[main]/Mysql::Server::Root_password/Mysql_user[root@localhost]/password_hash: defined 'password_hash' as '*AC57754462B6D4C373263062D60EDC6E452E574D'
	==> default: Notice: /Stage[main]/Mysql::Server::Root_password/File[/root/.my.cnf]/ensure: defined content as '{md5}027a4fcb65562e03b0ef14582da45076'
	==> default: Notice: /Stage[main]//Mysql::Db[wordpress_db]/Mysql_user[wordpress_user@192.168.33.%]/ensure: created
	==> default: Notice: /Stage[main]//Mysql::Db[wordpress_db]/Mysql_database[wordpress_db]/ensure: created
	==> default: Notice: /Stage[main]//Mysql::Db[wordpress_db]/Mysql_grant[wordpress_user@192.168.33.%/wordpress_db.*]/ensure: created
	==> default: Notice: /Stage[main]//Exec[system-update]/returns: executed successfully
	==> default: Notice: Finished catalog run in 18.44 seconds

### Install Puppet Apache Module	
So the DB part is done. Now let's do the *apache* part. Let's get the *apache* puppet module:

	elatov@usenelatovm1:~$puppet module install puppetlabs-apache
	Notice: Preparing to install into /Users/elatov/.puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/Users/elatov/.puppet/modules
	└─┬ puppetlabs-apache (v1.1.1)
	  ├── puppetlabs-concat (v1.1.0)
	  └── puppetlabs-stdlib (v4.3.0)
	  
After trying out that module with a simple manifest like this:

	### Global setttings
	Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
	
	exec { "system-update":
	        command => "zypper update -y",
	        onlyif => "test $(facter uptime_seconds) -lt 300",
	}
	
	
	# install and configure apache server
	class { 'apache':
	}


I got the following error:

	==> default: Error: Class['apache::version']: Unsupported osfamily: Suse at /tmp/vagrant-puppet-3/modules-0/apache/manifests/version.pp:32 on node linux-mjbf.b

It looks like **puppetlabs-apache** doesn't support openSUSE. So let's try out the **example42/apache** module:

	elatov@usenelatovm1:~$puppet module uninstall puppetlabs-apache
	Notice: Preparing to uninstall 'puppetlabs-apache' ...
	Removed 'puppetlabs-apache' (v1.1.1) from /Users/elatov/.puppet/modules
	elatov@usenelatovm1:~$puppet module install example42-apache
	Notice: Preparing to install into /Users/elatov/.puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/Users/elatov/.puppet/modules
	└─┬ example42-apache (v2.1.7)
	  └── example42-puppi (v2.1.9)
	  
That one installed **apache** without issues. I also installed the **example42/php module** as well to get the **php5-mysql** module and the **apache2-mod_php5** packages installed:

	elatov@usenelatovm1:~$puppet module install example42-php
	Notice: Preparing to install into /Users/elatov/.puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/Users/elatov/.puppet/modules
	└─┬ example42-php (v2.0.18)
	  └── example42-puppi (v2.1.9)
	  
After that I created the following manifest file and it installed all the necessary components:

	elatov@mac:~/web$cat manifests/web.pp
	### Global setttings
	Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
	
	exec { "system-update":
	        command => "zypper update -y",
	        onlyif => "test $(facter uptime_seconds) -lt 300",
	}
	
	
	# install and configure apache
	
	class { 'apache':
		disableboot => false
	}
	
	apache::module { 'mod_php5':
	   install_package => 'apache2-mod_php5',
	}
	
	class { 'php': }
	php::module { 'mysql': }
	
	exec { "enable-php-module":
		command => "sudo a2enmod php5",
		unless => "sudo a2enmod -q php5",
		require => Package["apache2-mod_php5"],
		notify => Service["apache2"],
	}

and here is the puppet output:

	==> default: Running Puppet with web.pp...
	==> default: Notice: /Stage[main]/Apache/Package[apache]/ensure: created
	==> default: Notice: /Stage[main]//Apache::Module[mod_php5]/Package[ApacheModule_mod_php5]/ensure: created
	==> default: Notice: /Stage[main]//Exec[enable-php-module]/returns: executed successfully
	==> default: Notice: /Stage[main]//Php::Module[mysql]/Package[PhpModule_mysql]/ensure: created
	==> default: Notice: /Stage[main]/Apache/Service[apache]/ensure: ensure changed 'stopped' to 'running'
	==> default: Notice: /Stage[main]//Exec[system-update]/returns: executed successfully
	==> default: Notice: Finished catalog run in 13.37 seconds
	
I noticed that the service wasn't getting automatically enabled and that's because systemd is used in openSUSE. So I modified the **example42/apache** module to use that ***provider***:

	vi ~/.puppet/modules/apache/manifests/init.pp

and added the following:

	service { 'apache':
	    provider   => "systemd",
	    
Should probably modify the class definition to support passing in the *provider* parameter ( maybe another day). 

### Install Puppet Wordpress Module
So let's try out a wordpress module:

	elatov@mac:~$puppet module install hunner-wordpress
	Notice: Preparing to install into /Users/elatov/.puppet/modules ...
	Notice: Downloading from https://forgeapi.puppetlabs.com ...
	Notice: Installing -- do not interrupt ...
	/Users/elatov/.puppet/modules
	└─┬ hunner-wordpress (v0.6.0)
	  ├── puppetlabs-concat (v1.1.0)
	  ├── puppetlabs-mysql (v2.3.0)
	  └── puppetlabs-stdlib (v4.3.0)
	  
After that I added the following to the manifest file:

	$db_name = "wordpress_db"
	$db_user = "wordpress_user"
	$db_pass = "wordpress"
	$db_host = "192.168.33.2"
	
	class { 'wordpress':
	  wp_owner    => 'wwwrun',
	  wp_group    => 'www',
	  db_name     => "$db_name",
	  db_user        => "$db_user",
	  db_password    => "$db_pass",
	  create_db      => false,
	  create_db_user => false,
	  install_dir => '/srv/www/htdocs/wp',
	  db_host => "$db_host"
	}

Then applying that manifest, I saw the following:

	==> default: Running Puppet with web.pp...
	==> default: Notice: /Stage[main]/Concat::Setup/File[/var/lib/puppet/concat]/ensure: created
	==> default: Notice: /Stage[main]/Concat::Setup/File[/var/lib/puppet/concat/bin]/ensure: created
	==> default: Notice: /Stage[main]/Concat::Setup/File[/var/lib/puppet/concat/bin/concatfragments.sh]/ensure: defined content as '{md5}7bbe7c5fce25a5ddd20415d909ba44fc'
	==> default: Notice: /Stage[main]/Apache/Package[apache]/ensure: created
	==> default: Notice: /Stage[main]//Apache::Module[mod_php5]/Package[ApacheModule_mod_php5]/ensure: created
	==> default: Notice: /Stage[main]//Exec[enable-php-module]/returns: executed successfully
	==> default: Notice: /Stage[main]//Php::Module[mysql]/Package[PhpModule_mysql]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/File[/srv/www/htdocs/wp]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Exec[Download wordpress]/returns: executed successfully
	==> default: Notice: /Stage[main]/Wordpress::App/Exec[Extract wordpress]/returns: executed successfully
	==> default: Notice: /Stage[main]/Wordpress::App/File[/srv/www/htdocs/wp/wp-keysalts.php]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php/fragments]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php/fragments.concat.out]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php/fragments.concat]/ensure: created
	==> default: Notice: /Stage[main]/Wordpress::App/Exec[Change ownership]: Triggered 'refresh' from 1 events
	==> default: Notice: /Stage[main]/Apache/Service[apache]/ensure: ensure changed 'stopped' to 'running'
	==> default: Notice: /Stage[main]/Wordpress::App/Concat::Fragment[wp-config.php body]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php/fragments/20_wp-config.php body]/ensure: defined content as '{md5}541b7060a3f025c4bacbc0f5942da2d1'
	==> default: Notice: /Stage[main]//Exec[system-update]/returns: executed successfully
	==> default: Notice: /Stage[main]/Wordpress::App/Concat::Fragment[wp-config.php keysalts]/File[/var/lib/puppet/concat/_srv_www_htdocs_wp_wp-config.php/fragments/10_wp-config.php keysalts]/ensure: defined content as '{md5}2629ccba733fd7f38a8f9ec9e90d7273'
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/Exec[concat_/srv/www/htdocs/wp/wp-config.php]/returns: executed successfully
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/Exec[concat_/srv/www/htdocs/wp/wp-config.php]: Triggered 'refresh' from 4 events
	==> default: Notice: /Stage[main]/Wordpress::App/Concat[/srv/www/htdocs/wp/wp-config.php]/File[/srv/www/htdocs/wp/wp-config.php]/ensure: defined content as '{md5}cf0c559bcc11a976abf8450500376699'
	==> default: Notice: Finished catalog run in 82.25 seconds

### Complete Vagrant and Puppet Setup

Here are the finished manifests:

	elatov@mac:~/web$cat manifests/web.pp
	### Global setttings
	Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
	
	exec { "system-update":
	        command => "zypper update -y",
	        onlyif => "test $(facter uptime_seconds) -lt 300",
	}
	
	$db_name = "wordpress_db"
	$db_user = "wordpress_user"
	$db_pass = "wordpress"
	$db_host = "192.168.33.2"
	
	# install and configure apache server
	
	class { 'apache':
		disableboot => false
	}
	
	# install mod-php for apache
	apache::module { 'mod_php5':
	   install_package => 'apache2-mod_php5',
	}
	
	# install the mysql-php module
	class { 'php': }
	php::module { 'mysql': }
	
	# enable the php module on apache unless already enabled
	exec { "enable-php-module":
		command => "sudo a2enmod php5",
		unless => "sudo a2enmod -q php5",
		require => Package["apache2-mod_php5"],
		notify => Service["apache2"],
	}
	
	class { 'wordpress':
	  wp_owner    => 'wwwrun',
	  wp_group    => 'www',
	  db_name     => "$db_name",
	  db_user        => "$db_user",
	  db_password    => "$db_pass",
	  create_db      => false,
	  create_db_user => false,
	  install_dir => '/srv/www/htdocs/wp',
	  db_host => "$db_host"
	}
	
And here is second one:

	elatov@mac:~/db$cat manifests/db.pp
	### Global setttings
	Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
	
	exec { "system-update":
	        command => "zypper update -y",
	        onlyif => "test $(facter uptime_seconds) -lt 300",
	}
	
	$mysql_password = "testing"
	$db_name = "wordpress_db"
	$db_user = "wordpress_user"
	$db_pass = "wordpress"
	$db_access = "192.168.33.%"
	
	# install and configure mysql-server and configure it to listen on the network
	class { '::mysql::server':
	  root_password    => $mysql_password,
	  override_options => { 'mysqld' => { 'bind-address' => $ipaddress_eth1 } }
	}
	
	# create the wordpress database and give permission to the wordpress user
	mysql::db { $db_name:
	  user     => $db_user,
	  password => $db_pass,
	  host     => $db_access,
	  grant  => 'ALL',
	}
	
And the **VagrantFile** was the same as before, it just included the **puppet.module_path** directive. To try the above setup, run the following:

1. Get the Base box: `vagrant box add elatov/opensuse13-64`
2. Install the necessary puppet modules: `puppet module install hunner-wordpress && puppet module install example42-apache && puppet module install puppetlabs-mysql && puppet module install example42-php module`
3. Get the **VagrantFile** and the *manifests*: `git clone https://github.com/elatov/vagrant-wp-mods.git`
4. Start up the environment: `cd vagrant-wp-mods; vagrant up`

Here is how long it took to provision the ***db*** VM:

	==> db: Notice: Finished catalog run in 84.75 seconds

and here is the ***web*** VM:

	==> web: Notice: Finished catalog run in 78.81 seconds
	
In the [previous](/2014/06/create-test-wordpress-instance-using-puppet-and-vagrant/) post, I didn't use any modules and using those original configurations here is how long it took to provision those VMs. First the db VM:

	==> db: Notice: Finished catalog run in 59.53 seconds

and here is the web VM:

	==> web: Notice: Finished catalog run in 59.43 seconds

So with the modules it does take a little longer to deploy but the configuration is much simpler since the modules take care most of the heavy lifting.
