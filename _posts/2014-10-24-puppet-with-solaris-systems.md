---
published: true
layout: post
title: "Puppet with OpenSolaris Systems"
author: Karim Elatov
categories: [os]
tags: [puppet,vagrant,opensolaris]
---
I had an OmniOS system and since I was using puppet to automate everything, I decided to automate a couple of things on the OpenSolaris OS as well.

### Getting the OmniOS Vagrant Box

The OmniOS folks provide a Vagrant Box of an OmniOS install so I decided to grab that for testing prior to making changes to my system:

    ~$ wget http://omnios.omniti.com/media/omnios-r151010j.box

Then import the box into the Vagrant catalogue (if you don't have vagrant configured check out my [previous post](/2014/06/simple-vagrant-setup/) on the setup):

    ~$ vagrant box add omnios511-64 download/omnios-r151010j.box
    
Then you should see the box in your list:

	~$ vagrant box list | grep omnios
	omnios511-64         (virtualbox, 0)
	
Now let's create a box environment from that box template:

	~$ mkdir omnios
	~$ cd omnios
	~/omnios$ vagrant init omnios511-64
	~/omnios$ vagrant up

After the machine is fully up you can ssh into it with `vagrant ssh`:

	~/omnios$ vagrant ssh
	Last login: Fri Oct 24 22:47:28 2014 from 10.0.2.2
	OmniOS 5.11     omnios-8c08411  2014.04.28
	vagrant@omnios-vagrant:~$
	
You will notice that this comes with the **OmniIT** *pkg* publisher and that will come in handy when we install puppet:

	vagrant@omnios-vagrant:~$ pkg publisher
	PUBLISHER                             TYPE     STATUS   URI
	omnios                                origin   online   http://pkg.omniti.com/omnios/r151010/
	ms.omniti.com                         origin   online   http://pkg.omniti.com/omniti-ms/
	
### Installing Puppet on OmniOS

I ended up using **ruby** and **gem** install puppet and it worked okay. First let's install the available **ruby** from the **OmniIT** publisher:

	vagrant@omnios-vagrant:~$ sudo pkg install ruby-19
	           Packages to install:  3
	       Create boot environment: No
	Create backup boot environment: No
	
	DOWNLOAD                                  PKGS       FILES    XFER (MB)
	Completed                                  3/3     827/827      5.6/5.6
	
	PHASE                                        ACTIONS
	Install Phase                                999/999
	
	PHASE                                          ITEMS
	Package State Update Phase                       3/3
	Image State Update Phase                         2/2

If you don't have the **OmniIT** publisher you can run the following to enable it:

	~$ pkg set-publisher -g http://pkg.omniti.com/omniti-ms ms.omniti.com

After that we can use **gem** to install puppet:

	vagrant@omnios-vagrant:~$ sudo gem install puppet
	Fetching: facter-2.2.0.gem (100%)
	Fetching: json_pure-1.8.1.gem (100%)
	Fetching: hiera-1.3.4.gem (100%)
	Fetching: puppet-3.7.1.gem (100%)
	Successfully installed facter-2.2.0
	Successfully installed json_pure-1.8.1
	Successfully installed hiera-1.3.4
	Successfully installed puppet-3.7.1
	4 gems installed
	Installing ri documentation for facter-2.2.0...
	Installing ri documentation for json_pure-1.8.1...
	Installing ri documentation for hiera-1.3.4...
	Installing ri documentation for puppet-3.7.1...

Then do a quick test by running **facter** to make sure it's functioning:

	vagrant@omnios-vagrant:~$ sudo /opt/omni/bin/i386/facter
	architecture => i86pc
	bios_release_date => 12/01/2006
	bios_vendor => innotek GmbH
	bios_version => 1.2
	facterversion => 2.2.0
	fqdn => omnios-vagrant
	gid => root
	hardwareisa => i386
	hardwaremodel => i86pc
	
If we are using Vagrant we need the vagrant user to be able to find the puppet script. So I added the **/opt/omni/bin/i386** to my **.bashrc** file:

	vagrant@omnios-vagrant:~$ cat .bashrc
	export PATH=/opt/omni/bin/i386:$PATH
	vagrant@omnios-vagrant:~$ echo $PATH
	/usr/bin:/usr/sbin:/sbin:/usr/gnu/bin:/opt/omni/bin:/opt/omni/bin/i386
	vagrant@omnios-vagrant:~$ which puppet
	/opt/omni/bin/i386/puppet

Also I checked when using **vagrant** and it worked out okay:

	~/omnios$ vagrant ssh -c 'sudo which puppet'
	/opt/omni/bin/i386/puppet
	Connection to 127.0.0.1 closed.
	~/omnios$ vagrant ssh -c 'which puppet'
	/opt/omni/bin/i386/puppet
	Connection to 127.0.0.1 closed.

### Configure the Puppet SMF Service
If you were using a puppet master and you wanted puppet agent to start on boot then follow the next few instructions. If you are just playing around with the Vagrant Box you can skip these steps.

First let's copy the service files into place:

	vagrant@omnios-vagrant:~$ sudo cp /opt/omni/lib/ruby/gems/1.9.1/gems/puppet-3.7.1/ext/solaris/smf/puppetd.xml /var/svc/manifest/puppetd.xml
	vagrant@omnios-vagrant:~$ sudo cp /opt/omni/lib/ruby/gems/1.9.1/gems/puppet-3.7.1/ext/solaris/smf/svc-puppetd /lib/svc/method/svc-puppetd

Now let's modify the files to point to the correct locations, in the **/var/svc/manifest/puppetd.xml** file I made the following changes:

	- exec='/opt/csw/lib/svc/method/svc-puppetd start'
	- exec='/opt/csw/lib/svc/method/svc-puppetd stop'
	- exec='/opt/csw/lib/svc/method/svc-puppetd reload'
	+ exec='/lib/svc/method/svc-puppetd stop'
	+ exec='/lib/svc/method/svc-puppetd start'
	+ exec='/lib/svc/method/svc-puppetd reload'

In the **/lib/svc/method/svc-puppetd** I made the following changes:

	- pidfile=/var/lib/puppet/run/agent.pid
	+ pidfile=/var/run/puppet/agent.pid
	- /opt/csw/sbin/puppetd
	+ /opt/omni/bin/i386/puppet agent

After that I created my **puppet.conf** and it looked like this:

	vagrant@omnios-vagrant:~$ cat /etc/puppet/puppet.conf
	[main]
	    confdir = /etc/puppet
	    vardir = /var/puppet
	    logdir = /var/log/puppet
	    statedir = /var/puppet/state
	    rundir = /var/run/puppet
	    libdir = /var/puppet/lib
	    factpath = /var/puppet/lib/facter:/var/puppet/facts
	[master]
	    ssl_client_header = SSL_CLIENT_S_DN
	    ssl_client_verify_header = SSL_CLIENT_VERIFY
	
	[agent]
	    server=puppet.me.com

Then importing the new service was good:

	vagrant@omnios-vagrant:~$ sudo svccfg -v import /var/svc/manifest/puppetd.xml
	svccfg: Taking "initial" snapshot for svc:/network/puppetd:default.
	svccfg: Taking "last-import" snapshot for svc:/network/puppetd:default.
	svccfg: Refreshed svc:/network/puppetd:default.
	svccfg: Successful import.

Now let's make sure we can start the service:

	vagrant@omnios-vagrant:~$ sudo svcadm enable puppetd
	vagrant@omnios-vagrant:~$ ps -eaf | grep pup
	    root  1165     1   0 17:25:28 ?           0:00 /opt/omni/bin/i386/ruby /opt/omni/bin/i386/puppet agent
	vagrant@omnios-vagrant:~$ svcs -L puppetd
	/var/svc/log/network-puppetd:default.log
	vagrant@omnios-vagrant:~$ tail /var/svc/log/network-puppetd:default.log
	[ Oct 17 17:25:27 Enabled. ]
	[ Oct 17 17:25:27 Executing start method ("/lib/svc/method/svc-puppetd start"). ]
	Starting Puppet client services: puppetd
	[ Oct 17 17:25:28 Method "start" exited with status 0. ]

Same thing for the stop:

	vagrant@omnios-vagrant:~$ sudo svcadm disable puppetd
	vagrant@omnios-vagrant:~$ ps -eaf | grep pup
	vagrant@omnios-vagrant:~$ tail /var/svc/log/network-puppetd:default.log
	[ Oct 17 17:25:27 Enabled. ]
	[ Oct 17 17:25:27 Executing start method ("/lib/svc/method/svc-puppetd start"). ]
	Starting Puppet client services: puppetd
	[ Oct 17 17:25:28 Method "start" exited with status 0. ]
	[ Oct 17 17:27:02 Stopping because service disabled. ]
	[ Oct 17 17:27:02 Executing stop method ("/lib/svc/method/svc-puppetd stop"). ]
	Stopping Puppet client services: puppetd
	[ Oct 17 17:27:02 Method "stop" exited with status 0. ]
	
Lastly we need to add the path of the puppet script to service, so when the puppet master calls the service it will know how to execute it. To do this we can run the following:

	vagrant@omnios-vagrant:~$ sudo svccfg -s puppetd setenv PATH /opt/local/bin/i386:/opt/local/sbin:/opt/local/bin:/bin:/sbin:/usr/bin:/usr/sbin
	
Restart the service:

	vagrant@omnios-vagrant:~$ sudo svcadm refresh puppetd
	vagrant@omnios-vagrant:~$ sudo svcadm restart puppetd

And you can use **pargs** to confirm that the process has the right environment variable (**PATH**) configured:

	vagrant@omnios-vagrant:~$ pargs -e `pgrep -f /opt/omni/bin/i386/ruby`
	2901:   /opt/omni/bin/i386/ruby /opt/omni/bin/i386/puppet agent
	envp[0]: _=*2892*/opt/omni/bin/i386/puppet
	envp[1]: PATH=/opt/local/bin/i386:/opt/local/sbin:/opt/local/bin:/bin:/sbin:/usr/bin:/usr/sbin
	envp[2]: PWD=/
	envp[3]: SHLVL=1
	envp[4]: SMF_FMRI=svc:/network/puppetd:default
	envp[5]: SMF_METHOD=start
	envp[6]: SMF_RESTARTER=svc:/system/svc/restarter:default
	envp[7]: SMF_ZONENAME=global
	envp[8]: TZ=US/Mountain
	envp[9]: A__z="*SHLVL

And that's all good, again if you are just using **vagrant** for this, then you don't really have to worry about it.

### Quick test to make sure Puppet is configured appropriately
At this point we can modify the **Vagrantfile** to use puppet and create a very simple **site.pp** to make sure **puppet** is usable. I added the following to the **Vagrantfile**:

	config.vm.provision "puppet" do |puppet|
	     puppet.manifests_path = "manifests"
	     puppet.manifest_file  = "site.pp"
	#    puppet.options = "--verbose --debug"
	end
	
I leave the *debug* options commented in just in case I will need them later. Now let's create a very simple **site.pp**:

	~/omnios$ cat manifests/site.pp
	notify { "this is a test": }
	
Now let's test it out:

	~/omnios$ vagrant provision
	==> default: Running provisioner: puppet...
	==> default: Running Puppet with site.pp...
	==> default: Notice: Compiled catalog for omnios-vagrant in environment production in 0.15 seconds
	==> default: Notice: this is a test
	==> default: Notice: /Stage[main]/Main/Notify[this is a test]/message: defined 'message' as 'this is a test'
	==> default: Notice: Finished catalog run in 0.05 seconds
	
Yay, that looks good.

### Using pkgin with OmniOS

[pkgsrc](https://www.pkgsrc.org/) is an openbsd package management system, but it also works with OpenSolaris. Instructions on how to install it are laid out in this [SmartOS page](http://wiki.smartos.org/display/DOC/3rd+Party+Software+Repos) (there are also other repos if you want to try them out). But to install **pkgin/pkgsrc** on OmniOS, I ran the following:

	vagrant@omnios-vagrant:~$ cd /tmp; wget http://pkgsrc.joyent.com/packages/SmartOS/bootstrap/bootstrap-2014Q2-x86_64.tar.gz
	vagrant@omnios-vagrant:/tmp$ sudo tar xvzf bootstrap-2014Q2-x86_64.tar.gz -C /
	vagrant@omnios-vagrant:/tmp$ sudo /opt/local/bin/pkg_admin rebuild
	Stored 5224 files and 0 explicit directories from 19 packages in /opt/local/pkg/pkgdb.byfile.db.
	Done.
	vagrant@omnios-vagrant:/tmp$ sudo /opt/local/bin/pkgin -y up
	reading local summary...
	processing local summary...
	updating database: 100%
	pkg_summary.bz2                                                                                                               100% 1918KB 319.7KB/s  40.4KB/s   00:06
	cleaning database from http://pkgsrc.joyent.com/packages/SmartOS/2014Q2/x86_64/All entries...
	processing remote summary (http://pkgsrc.joyent.com/packages/SmartOS/2014Q2/x86_64/All)...
	updating database: 100% 

Now I can install a lot of new packages (or newer versions):

	vagrant@omnios-vagrant:~$ pkgin search boost-libs
	boost-libs-1.55.0nb1 = Free, peer-reviewed portable C++ source libraries (binary libraries)
	
The **pkgin** provider is included with the puppet install:

	vagrant@omnios-vagrant:~$ puppet describe package --providers | /usr/gnu/bin/grep "\*\*pkgin\*\*" -A 6
	- **pkgin**
	    Package management using pkgin, a binary package manager for pkgsrc.
	    * Required binaries: `pkgin`.
	    * Default for `operatingsystem` == `dragonfly, smartos`.
	    * Supported features: `installable`, `uninstallable`, `upgradeable`,
	    `versionable`.
    
Now adding the following to my **site.pp**:

	$cat manifests/site.pp
	package { 'top' :
	    provider => pkgin,
	    ensure   => 'present',
	}

and running `vagrant provision`, I saw the following:

	~/omnios$ vagrant provision
	==> default: Running provisioner: puppet...
	==> default: Running Puppet with site.pp...
	==> default: Notice: Compiled catalog for omnios-vagrant in environment production in 3.86 seconds
	==> default: Notice: /Stage[main]/Main/Package[top]/ensure: created
	==> default: Notice: Finished catalog run in 8.24 seconds

### Using other Solaris Providers
There is an open source Solaris puppet project which has a lot of Solaris specific providers. Currently it's specific for Oracle Solaris 11, but any OpenSolaris fork should be okay. Here are two pages that talk about the puppet providers:

- [Getting Started with Puppet on Oracle Solaris 11](http://www.oracle.com/technetwork/articles/servers-storage-admin/howto-automate-config-datacenter-2212734.html)
- [Solaris-specific Providers for Puppet](https://blogs.oracle.com/observatory/en_US/entry/solaris_specific_providers_for_puppet)

These providers reside in a **mercurial** repository. I ran the following on my Mac OS X machine to grab those:

	~$ sudo port install mercurial
	~$ hg clone https://hg.java.net/hg/solaris-userland~gate userland-gate
	~$ mkdir omnios/modules
	~$ rsync -avzP userland-gate/components/ruby/puppet/files/solaris omnios/modules

I then made the puppet section look like this in my **Vagrantfile**:

	config.vm.provision "puppet" do |puppet|
	     puppet.manifests_path = "manifests"
	     puppet.manifest_file  = "site.pp"
	     puppet.module_path = "modules"
	#    puppet.options = "--verbose --debug"
	 end

Then I wanted to test out the **pkg_publisher** type and I added the following into my **site.pp**:

	$cat manifests/site.pp
	package { 'top' :
	    provider => pkgin,
	    ensure   => 'present',
	}
	
	pkg_publisher { 'uulm.mawi':
	    origin  => 'http://scott.mathematik.uni-ulm.de/release',
	    enable  => true,
	    ensure  => 'present',
	}

Then the `vagrant provision` went through:

	$vagrant provision
	==> default: Running provisioner: puppet...
	==> default: Running Puppet with site.pp...
	==> default: Notice: Compiled catalog for omnios-vagrant in environment production in 0.71 seconds
	==> default: Notice: /Stage[main]/Main/Pkg_publisher[uulm.mawi]/ensure: created
	==> default: Notice: Finished catalog run in 13.01 seconds

If you get the following error:

> Error: Could not find a suitable provider for pkg_publisher

Check to make sure there is no **confine** in the **pkg_publisher.rb** file. That used to be in the old versions of the **lib/puppet/provider/pkg_publisher/pkg_publisher.rb** file and it looked like this:

	confine :operatingsystem => [:solaris]

But newer versions don't have it any more. There are a bunch of other types and providers available, here is the list:

- *boot_environment*
- *pkg_publisher*
- *vnic*
- *dns*
- Datalink Management:   *etherstub*, *ip_tunnel*, *link_aggregation*, *solaris_vlan*
- IP Network Interfaces:  *address_object*, *address_property*, *interface_properties*, *ip_interface*, *ipmp_interface*, *link_properties*, *protocol_properties*, *vni_interface*
- pkg(5) Management:  *pkg_facet*, *pkg_mediator*, *pkg_variant*
- Naming Services:  *nis*, *nsswitch*, *ldap*

They are listed in the site above as well.

### The Logadm Puppet Type

There is a pretty old [puppet page](http://projects.puppetlabs.com/projects/1/wiki/logadm_patterns) which has the provider, but it's one huge file (it's not broken down by **type** and **provider**... but it still works). There is a backup function in the file and removing it allowed me to use the provider. The slimmed down version is available in my github [here](https://raw.githubusercontent.com/elatov/puppet/master/logadm/lib/puppet/type/logadm.rb). Here is what I did to use that *type*:

	~/omnios$ mkdir -p modules/logadm/lib/puppet/type
	~/omnios$ cd modules/logadm/lib/puppet/type
	~/omnios/modules/logadm/lib/puppet/type$ wget https://raw.githubusercontent.com/elatov/puppet/master/logadm/lib/puppet/type/logadm.rb

Then adding the following to my **site.pp**:

	~/omnios$ cat manifests/site.pp
	package { 'top' :
	    provider => pkgin,
	    ensure   => 'present',
	}
	
	pkg_publisher { 'uulm.mawi':
	    origin  => 'http://scott.mathematik.uni-ulm.de/release',
	    enable  => true,
	    ensure  => 'absent',
	}
	
	logadm { '/var/adm/test.log':
	      count          => '5',
	      copy_truncate  => true,
	}

and the `vagrant provision`:

	~/omnios$ vagrant provision
	==> default: Running provisioner: puppet...
	==> default: Running Puppet with site.pp...
	==> default: Notice: Compiled catalog for omnios-vagrant in environment production in 0.76 seconds
	==> default: Notice: /Stage[main]/Main/Logadm[/var/adm/test.log]/ensure: created
	==> default: Notice: Finished catalog run in 6.46 seconds

then checking out the actual **/etc/logadm.conf** in the OS, I saw the following:

	vagrant@omnios-vagrant:~$ grep test /etc/logadm.conf
	# puppet(logadm["/var/adm/test.log"])
	/var/adm/test.log -c -C 5

Also making sure the file is picked up by **logadm**, we can run the following to make sure it shows up:

	vagrant@omnios-vagrant:~$ sudo logadm -V
	/var/log/syslog -C 8 -a 'kill -HUP `cat /var/run/syslog.pid`'
	/var/adm/messages -C 4 -a 'kill -HUP `cat /var/run/syslog.pid`'
	/var/cron/log -c -s 512k -t /var/cron/olog
	/var/lp/logs/lpsched -C 2 -N -t '$file.$N'
	/var/fm/fmd/errlog -M '/usr/sbin/fmadm -q rotate errlog && mv /var/fm/fmd/errlog.0- $nfile' -N -s 2m
	/var/fm/fmd/fltlog -A 6m -M '/usr/sbin/fmadm -q rotate fltlog && mv /var/fm/fmd/fltlog.0- $nfile' -N -s 10m
	smf_logs -C 8 -c -s 1m /var/svc/log/*.log
	/var/adm/pacct -C 0 -N -a '/usr/lib/acct/accton pacct' -g adm -m 664 -o adm -p never
	/var/log/pool/poold -N -a 'pkill -HUP poold; true' -s 512k
	/var/fm/fmd/infolog -A 2y -M '/usr/sbin/fmadm -q rotate infolog && mv /var/fm/fmd/infolog.0- $nfile' -N -S 50m -s 10m
	/var/fm/fmd/infolog_hival -A 2y -M '/usr/sbin/fmadm -q rotate infolog_hival && mv /var/fm/fmd/infolog_hival.0- $nfile' -N -S 50m -s 10m
	/var/adm/mail.log -C 3 -a 'kill -HUP `cat /var/run/syslog.pid`'
	/var/adm/test.log -C 5 -c

And we can see the last entry is what we added.