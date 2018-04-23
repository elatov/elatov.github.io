---
published: true
layout: post
title: "Upgrade Puppet 3.x to 4.x"
author: Karim Elatov
categories: [os]
tags: [puppet]
---
I setup **puppet** a while back and I just let it do it's thing. Honestly I wasn't having any issues, I just decided to update to the latest version.

### Upgrading Puppet Server
There is a pretty good overview at [Puppet 3.x to 4.x Server Upgrades](https://puppet.com/docs/puppet/latest/upgrade_major_pre.html). Here is a snippet from the page:

> 1. Install the `puppet-agent` and `puppetserver` packages for your operating system.
> 2. Copy your certificate authority files to the new filesystem location (`/etc/puppetlabs/puppet/ssl)`
> 3. Migrate your code (modules + manifests + hiera) to the new location and directory structure (`/etc/puppetlabs/code`) and prepare the server for Directory Environments.
> 4. Transfer any custom settings that were in your previous puppet.conf to `/etc/puppetlabs/puppet/puppet.conf`. Note: Do not copy the file in-place. Many older settings are removed or their defaults have changed.
> 5. If you were previously using Apache: start running your Puppet master under Puppet Server 2.0.

#### Install the Packages
So first let's go ahead and create a back up of the config files:

    cd /etc/
    sudo tar cpjf puppet-bef-4-3.tar.bz2 puppet

Now let's add the new repo:

    sudo rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm

And next let's remove the old puppet master:

    sudo yum remove puppet-server
    sudo yum remove puppetlabs-release-7-11.noarch

Now let's install the new package:

    ┌─[elatov@puppet] - [/etc] - [2016-02-21 03:46:19]
    └─[0] <> sudo yum install puppetserver
    Loaded plugins: fastestmirror, remove-with-leaves
    Loading mirror speeds from cached hostfile
     * atomic: www8.atomicorp.com
     * base: mirror.compevo.com
     * epel: mirrors.tummy.com
     * extras: mirror.raystedman.net
     * updates: centos.host-engine.com
    Resolving Dependencies
    --> Running transaction check
    ---> Package puppetserver.noarch 0:2.2.1-1.el7 will be installed
    --> Processing Dependency: puppet-agent >= 1.3.0 for package: puppetserver-2.2.1-1.el7.noarch
    --> Running transaction check
    ---> Package facter.x86_64 1:2.4.6-1.el7 will be obsoleted
    ---> Package puppet.noarch 0:3.8.6-1.el7 will be obsoleted
    ---> Package puppet-agent.x86_64 0:1.3.5-1.el7 will be obsoleting
    --> Finished Dependency Resolution
    
    Dependencies Resolved
    
    ================================================================================
     Package            Arch         Version             Repository            Size
    ================================================================================
    Installing:
     puppet-agent       x86_64       1.3.5-1.el7         puppetlabs-pc1        22 M
         replacing  facter.x86_64 1:2.4.6-1.el7
         replacing  puppet.noarch 3.8.6-1.el7
     puppetserver       noarch       2.2.1-1.el7         puppetlabs-pc1        40 M
    
    Transaction Summary
    ================================================================================
    Install  2 Packages
    
    Total download size: 63 M
    Is this ok [y/d/N]: y

This will update/obsolete the old packages. 

#### Migrate the Configuration
Next let's migrate the configuration. The old config is here:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:11:40]
    └─[0] <> ls -l /etc/puppet/puppet.conf.rpmsave
    -rw-r--r-- 1 root root 1135 Dec 30 12:07 /etc/puppet/puppet.conf.rpmsave

and the new one is:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:12:58]
    └─[0] <> ls -l /etc/puppetlabs/puppet/puppet.conf
    -rw-r--r-- 1 root root 691 Feb 21 15:50 /etc/puppetlabs/puppet/puppet.conf

After checking out the options at [Configuration: Short List of Important Settings](https://puppet.com/docs/puppet/latest/config_important_settings.html), here is what I ended up with:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:42:33]
    └─[0] <> cat /etc/puppetlabs/puppet/puppet.conf
    # This file can be used to override the default puppet settings.
    # See the following links for more details on what settings are available:
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_important_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_about_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_file_main.html
    # - https://docs.puppetlabs.com/references/latest/configuration.html
    [master]
        vardir = /opt/puppetlabs/server/data/puppetserver
        logdir = /var/log/puppetlabs/puppetserver
        rundir = /var/run/puppetlabs/puppetserver
        pidfile = /var/run/puppetlabs/puppetserver/puppetserver.pid
        codedir = /etc/puppetlabs/code
        ca = true
        autosign = $confdir/autosign.conf
        dns_alt_names = puppet,puppet.dnsd.me
    #   parser = future
        reports = tagmail
    #   reportfrom = puppet@puppet.dnsd.me
    #   sendmail = /usr/sbin/sendmail
    
    [agent]
        report = true
        noop = true
        server = puppet.dnsd.me

Next let's copy the *autosign* config (my config was pretty simple so I didn't have to modify anything):

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:47:32]
    └─[0] <> sudo cp /etc/puppet/autosign.conf /etc/puppetlabs/puppet/.

And let's copy the ssl certs:

    sudo rsync -avzP /var/lib/puppet/ssl/. /etc/puppetlabs/puppet/ssl/.

It seems that **tagmail** has been removed, so let's install a plugin that
accomplishes the same:

    sudo puppet module install puppetlabs-tagmail
    Notice: Preparing to install into /etc/puppetlabs/code/environments/production/modules ...
    Notice: Downloading from https://forgeapi.puppetlabs.com ...
    Notice: Installing -- do not interrupt ...
    /etc/puppetlabs/code/environments/production/modules
    └── puppetlabs-tagmail (v2.1.1)

And then let's create the corresponding **tagmail** conf file:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 05:03:19]
    └─[0] <> cat /etc/puppetlabs/puppet/tagmail.conf
    [transport]
    reportfrom = puppet@puppet.dnsd.me
    sendmail = /usr/sbin/sendmail
    [tagmap]
    all: elatov


#### Migrate From Rack to PuppetServer

It looks like it's recommended to use the direct puppetserver instead of the rack app. From [Puppet 3.x to 4.x: Get Upgrade-Ready](https://puppet.com/docs/puppet/latest/upgrade_major_pre.html): 

> If you’re still using Rack or WEBrick to run your Puppet master, this is the best time to switch to Puppet Server. Puppet Server is designed to be a better-performing drop-in replacement for Rack and WEBrick Puppet masters, which are deprecated as of Puppet 4.1.

So let's disable that:

    sudo mv /etc/httpd/conf.d/puppetmaster.conf /etc/httpd/conf.d/puppetmaster.conf.new-disabled

now let's reload **systemd** configs

    sudo systemctl daemon-reload

And now let's enable the service:

    sudo systemctl enable puppetserver.service

Prior to start it, I lowered the RAM usage as described here: [Puppet Server: Installing From Packages](https://docs.puppetlabs.com/puppetserver/latest/install_from_packages.html):

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 05:13:07]
    └─[0] <> grep JAVA_ARGS /etc/sysconfig/puppetserver
    JAVA_ARGS="-Xms1g -Xmx1g -XX:MaxPermSize=256m"

and lastly we could start it by running the following (but I wouldn't do that yet):

    sudo systemctl start puppetserver.service

#### Keep Using Rack Application
I noticed the puppetserver is pretty RAM intensive so if you really want to go against the grain you can still use the Rack App version. First let's back up the original config:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:09:43]
    └─[0] <> sudo mv /usr/share/puppet/rack/puppetmasterd /usr/share/puppet/rack/puppetmasterd.orig

Next let's create the original directory structure:

    sudo mkdir -p /usr/share/puppet/rack/puppetmasterd
    sudo mkdir /usr/share/puppet/rack/puppetmasterd/public /usr/share/puppet/rack/puppetmasterd/tmp
    wget https://raw.github.com/puppetlabs/puppet/stable/ext/rack/config.ru
    sudo cp config.ru /usr/share/puppet/rack/puppetmasterd/
    sudo chown puppet:puppet /usr/share/puppet/rack/puppetmasterd/config.ru
    
Here is how my **config.ru** looked like:

    # a config.ru, for use with every rack-compatible webserver.
    # SSL needs to be handled outside this, though.
    
    # if puppet is not in your RUBYLIB:
    #$LOAD_PATH.unshift('/opt/puppet/lib')
    $LOAD_PATH.unshift('/opt/puppetlabs/puppet/lib/ruby/vendor_ruby')
    
    $0 = "master"
    
    # if you want debugging:
    # ARGV << "--debug"
    
    ARGV << "--rack"
    
    # Rack applications typically don't start as root.  Set --confdir, --vardir,
    # --logdir, --rundir to prevent reading configuration from
    # ~/ based pathing.
    ARGV << "--confdir" << "/etc/puppetlabs/puppet"
    ARGV << "--vardir"  << "/opt/puppetlabs/server/data/puppetserver"
    ARGV << "--logdir"  << "/var/log/puppetlabs/puppetserver"
    ARGV << "--rundir"  << "/var/run/puppetlabs/puppetserver"
    ARGV << "--codedir"  << "/etc/puppetlabs/code"
    
    # always_cache_features is a performance improvement and safe for a master to
    # apply. This is intended to allow agents to recognize new features that may be
    # delivered during catalog compilation.
    ARGV << "--always_cache_features"
    
    # NOTE: it's unfortunate that we have to use the "CommandLine" class
    #  here to launch the app, but it contains some initialization logic
    #  (such as triggering the parsing of the config file) that is very
    #  important.  We should do something less nasty here when we've
    #  gotten our API and settings initialization logic cleaned up.
    #
    # Also note that the "$0 = master" line up near the top here is
    #  the magic that allows the CommandLine class to know that it's
    #  supposed to be running master.
    #
    # --cprice 2012-05-22
    
    require 'puppet/util/command_line'
    # we're usually running inside a Rack::Builder.new {} block,
    # therefore we need to call run *here*.
    run Puppet::Util::CommandLine.new.execute

Then I moved the passenger config out of the way:

    sudo mv /etc/httpd/conf.d/puppetmaster.conf /etc/httpd/conf.d/puppetmaster.conf.orig

And created a new one:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 04:17:07]
    └─[0] <> cat /etc/httpd/conf.d/puppetmaster.conf
    # RHEL/CentOS:
    LoadModule passenger_module /usr/local/share/gems/gems/passenger-4.0.48/buildout/apache2/mod_passenger.so
    PassengerRoot /usr/local/share/gems/gems/passenger-4.0.48
    PassengerRuby /usr/bin/ruby
    
    # And the passenger performance tuning settings:
    # Set this to about 1.5 times the number of CPU cores in your master:
    PassengerMaxPoolSize 12
    # Recycle master processes after they service 1000 requests
    PassengerMaxRequests 1000
    # Stop processes if they sit idle for 10 minutes
    PassengerPoolIdleTime 600
    
    Listen 8140
    <VirtualHost *:8140>
        # Make Apache hand off HTTP requests to Puppet earlier, at the cost of
        # interfering with mod_proxy, mod_rewrite, etc. See note below.
        PassengerHighPerformance On
    
        SSLEngine On
    
        # Only allow high security cryptography. Alter if needed for compatibility.
        SSLProtocol ALL -SSLv2 -SSLv3
        SSLCipherSuite EDH+CAMELLIA:EDH+aRSA:EECDH+aRSA+AESGCM:EECDH+aRSA+SHA384:EECDH+aRSA+SHA256:EECDH:+CAMELLIA256:+AES256:+CAMELLIA128:+AES128:+SSLv3:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!DSS:!RC4:!SEED:!IDEA:!ECDSA:kEDH:CAMELLIA256-SHA:AES256-SHA:CAMELLIA128-SHA:AES128-SHA
        SSLHonorCipherOrder     on
    
        SSLCertificateFile      /etc/puppetlabs/puppet/ssl/certs/puppet-server.example.com.pem
        SSLCertificateKeyFile   /etc/puppetlabs/puppet/ssl/private_keys/puppet-server.example.pem
        SSLCertificateChainFile /etc/puppetlabs/puppet/ssl/ca/ca_crt.pem
        SSLCACertificateFile    /etc/puppetlabs/puppet/ssl/ca/ca_crt.pem
        SSLCARevocationFile     /etc/puppetlabs/puppet/ssl/ca/ca_crl.pem
        SSLCARevocationCheck     chain
        SSLVerifyClient         optional
        SSLVerifyDepth          1
        SSLOptions              +StdEnvVars +ExportCertData
    
        # These request headers are used to pass the client certificate
        # authentication information on to the Puppet master process
        RequestHeader set X-SSL-Subject %{SSL_CLIENT_S_DN}e
        RequestHeader set X-Client-DN %{SSL_CLIENT_S_DN}e
        RequestHeader set X-Client-Verify %{SSL_CLIENT_VERIFY}e
    
        DocumentRoot /usr/share/puppet/rack/puppetmasterd/public
    
        <Directory /usr/share/puppet/rack/puppetmasterd/>
          Options None
          AllowOverride None
          # Apply the right behavior depending on Apache version.
          <IfVersion < 2.4>
            Order allow,deny
            Allow from all
          </IfVersion>
          <IfVersion >= 2.4>
            Require all granted
          </IfVersion>
        </Directory>
    
        ErrorLog /var/log/httpd/puppet-server.example.com_ssl_error.log
        CustomLog /var/log/httpd/puppet-server.example.com_ssl_access.log combined
    </VirtualHost>


#### Starting Puppet Server
At this point you can either restart **apache** (if you are still using the Rack App):

    sudo systemctl restart httpd

Or start the **puppetserver** service:

    sudo systemctl start puppetserver

This will make sure your options are okay.

#### Migrating the Puppet Code

Moving the code is pretty easy:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 05:05:44]
    └─[0] <> sudo rsync -avzP /etc/puppet/modules/. /etc/puppetlabs/code/environments/production/modules/.

And let's do the same thing for the manifests:

    ┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 05:05:44]
    └─[0] <> sudo rsync -avzP /etc/puppet/manifests/.
    /etc/puppetlabs/code/environments/production/manifests/.

But I ran into a bunch of different issues with the new parser. Here is a quick summary:

**Error #1:**

    This Array Expression has no effect. A Host Class Definition can not end with a value-producing expression without other effect at

**Fix #1:**
Remove space for class definition

    #From
    Class ['rsyslog']
    #To
    Class['rsyslog']

**Error #2:**

    Error: Could not retrieve catalog from remote server: Error 400 on SERVER: Evaluation Error: Error while evaluating a Function Call, Failed to parse template zabbix/zabbix_agentd.conf.erb:
      Filepath: /etc/puppetlabs/code/environments/production/modules/zabbix/templates/zabbix_agentd.conf.erb
      Line: 97
      Detail: undefined method `[]' for nil:NilClass
     at /etc/puppetlabs/code/environments/production/modules/zabbix/manifests/agent/config.pp:222:16 on node puppet.dnsd.me

**Fix #2:**
Had to access the hash keys with scope

    #From
    <% if @settings]['allow_root'] -%>
    #To
    <% if scope['zabbix::agent::settings']['allow_root'] -%>


**Error #3:**

    Error 400 on SERVER: Syntax error at '['
    
**Fix #3:**
Another Space issue

    #From
    require => File [$smartd::config_dir],
    #To
    require => File[$smartd::config_dir],

**Error #4:**

    Error 400 on SERVER: Evaluation Error: Comparison of: String >= Integer, is not possible. Caused by 'A String is not comparable to a non String'.

**Fix #4:**
Had to explicitly convert a Integer to a String prior to comparing a string that was just an integer:

    #From
    if $::operatingsystemmajrelease >= 7 {
    #To
    if (versioncmp($::operatingsystemmajrelease, '7') >= 0)

That's is all that I had to do on the Puppet Server Side.

### Updating Puppet Agents
Next I moved on to my agents. Most of the steps are covered in [Installing Puppet Agent: Linux](https://puppet.com/docs/puppet/latest/install_linux.html)

#### Update Centos Agents
First let's remove the old package:

    ┌─[elatov@m2] - [/home/elatov] - [2016-02-22 08:57:42]
    └─[0] <> sudo yum remove puppetlabs-release-7-11.noarch

And let's install the new repo

    sudo rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm

Next let's install and update the agent:

    ┌─[elatov@m2] - [/home/elatov] - [2016-02-22 08:58:11]
    └─[0] <> sudo yum install puppet-agent
    Loaded plugins: fastestmirror, remove-with-leaves
    puppetlabs-pc1                                           | 2.5 kB     00:00
    puppetlabs-pc1/x86_64/primary_db                           |  42 kB   00:00
    Loading mirror speeds from cached hostfile
     * atomic: www3.atomicorp.com
     * base: denver.gaminghost.co
     * epel: mirrors.tummy.com
     * extras: bay.uchicago.edu
     * updates: dallas.tx.mirror.xygenhosting.com
    Resolving Dependencies
    --> Running transaction check
    ---> Package facter.x86_64 1:2.4.6-1.el7 will be obsoleted
    ---> Package puppet.noarch 0:3.8.6-1.el7 will be obsoleted
    ---> Package puppet-agent.x86_64 0:1.3.5-1.el7 will be obsoleting
    --> Finished Dependency Resolution
    
    Dependencies Resolved
    
    ================================================================================
     Package            Arch         Version             Repository            Size
    ================================================================================
    Installing:
     puppet-agent       x86_64       1.3.5-1.el7         puppetlabs-pc1        22 M
         replacing  facter.x86_64 1:2.4.6-1.el7
         replacing  puppet.noarch 3.8.6-1.el7

For the config, here is what I ended up with

    ┌─[elatov@m2] - [/home/elatov] - [2016-02-22 09:10:22]
    └─[0] <> cat /etc/puppetlabs/puppet/puppet.conf
    # This file can be used to override the default puppet settings.
    # See the following links for more details on what settings are available:
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_important_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_about_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_file_main.html
    # - https://docs.puppetlabs.com/references/latest/configuration.html
    [agent]
        report = true
        server = puppet.dnsd.me
        noop = false

Now let's copy the ssl certs:

    ┌─[elatov@m2] - [/home/elatov] - [2016-02-22 09:12:25]
    └─[0] <> sudo rsync -avzP /var/lib/puppet/ssl /etc/puppetlabs/puppet/.

A this point you can confirm the agent can pull it's manifest and apply all the settings:

    sudo puppet agent -t

### Update Debian Agents
Let's remove the original repo:

    sudo apt-get remove --purge puppetlabs-release

Add the new one:

    wget https://apt.puppetlabs.com/puppetlabs-release-pc1-jessie.deb
    sudo dpkg -i puppetlabs-release-pc1-jessie.deb

Let's update the **apt** cache:

    sudo apt-get update

And update the packages:

    ┌─[elatov@kerch] - [/home/elatov] - [2016-02-22 09:28:59]
    └─[0] <> sudo apt-get install puppet-agent
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    The following packages were automatically installed and are no longer required:
      libaugeas-ruby libaugeas-ruby1.9.1 libjson-ruby ruby-shadow virt-what
    Use 'apt-get autoremove' to remove them.
    The following packages will be REMOVED:
      facter hiera puppet puppet-common
    The following NEW packages will be installed:
      puppet-agent
    0 upgraded, 1 newly installed, 4 to remove and 0 not upgraded.
    Need to get 13.1 MB of archives.
    After this operation, 63.3 MB of additional disk space will be used.
    Do you want to continue? [Y/n] Y

Similar thing for the config file:

    ┌─[elatov@kerch] - [/home/elatov] - [2016-02-22 09:33:03]
    └─[0] <> cat /etc/puppetlabs/puppet/puppet.conf
    # This file can be used to override the default puppet settings.
    # See the following links for more details on what settings are available:
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_important_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_about_settings.html
    # - https://docs.puppetlabs.com/puppet/latest/reference/config_file_main.html
    # - https://docs.puppetlabs.com/references/latest/configuration.html
    [agent]
    server = puppet.dnsd.me
    noop = true
    report    = false
    #debug = true

Let's copy the certs:

    ┌─[elatov@kerch] - [/home/elatov] - [2016-02-22 09:35:45]
    └─[0] <> sudo rsync -avzP /var/lib/puppet/ssl /etc/puppetlabs/puppet/.

And now you can test out the config:

    sudo puppet agent -t

#### Update FreeBSD Agent
First I completely removed the original version:

    sudo service puppet stop
    sudo pkg remove puppet

Then I installed the new version:

    sudo pkg install puppet4

The config location actually didn't change:

    ┌─[elatov@moxz] - [/home/elatov] - [2016-02-23 08:45:16]
    └─[0] <> cat /usr/local/etc/puppet/puppet.conf
    [agent]
        server = puppet.dnsd.me
        noop = true
        report = true

And the **ssldir** was actually the same so I didn't have to copy that:

    ┌─[elatov@moxz] - [/home/elatov] - [2016-02-23 08:45:21]
    └─[0] <> sudo puppet config print ssldir
    /var/puppet/ssl

Then again testing the configuration worked out:

    sudo puppet agent -t

#### Update OpenSolaris Agent
First let's completely remove the agent:

    gem uninstall puppet

Then let's install the latest version:

    gem install puppet --no-ri --no-rdoc

Here is the configuration I ended up with:

    ┌─[root@zfs] - [/root] - [2016-02-23 09:06:09]
    └─[0] <> cat /etc/puppetlabs/puppet/puppet.conf
    [agent]
        server=puppet.dnsd.me
        noop = true
        report = true

Next let's copy the certs:

    ┌─[root@zfs] - [/root] - [2016-02-23 09:06:47]
    └─[0] <> rsync -avzP /etc/puppet/ssl/. /etc/puppetlabs/puppet/ssl/.
    
And lastly make sure the test works:

	puppet agent -t

### Fix Floppy Errors
After Migrating to the latest version of puppet I noticed that I kept getting floppy errors in the logs. So I decided to disable the floppy module since I don't use floppy disks. 

#### Disable Floppy Module on Debian
Here is the error I kept getting in the logs:

	[1535714.035925] end_request: I/O error, dev fd0, sector 0

To fix it, let's black list the module:

	┌─[elatov@kerch] - [/home/elatov] - [2016-02-25 06:48:34]
	└─[0] <> cat /etc/modprobe.d/nofloppy.conf
	blacklist floppy

And then rebuild **initrd**

	sudo depmod -ae
	sudo update-initramfs -u

To apply just reboot:

	sudo rebooot

If you don't want to reboot you can just disable the module on the fly:

	sudo modprobe -r floppy

#### Disable Floppy Module on CentOS
Here is the error I kept getting in the logs:

	blk_update_request: I/O error, dev fd0, sector 0

To disable the module, add the following to **GRUB**:

	┌─[elatov@m2] - [/home/elatov] - [2016-02-25 06:49:57]
	└─[0] <> grep flopp /etc/sysconfig/grub
	GRUB_CMDLINE_LINUX="vconsole.keymap=us crashkernel=auto  vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos_m2c/root rd.lvm.lv=centos_m2c/swap quiet modprobe.blacklist=floppy"

Then regenerate the **grub** config:

	sudo grub2-mkconfig -o /boot/grub2/grub.cfg

And lastly reboot:

	sudo reboot

Or disable on the fly:

	sudo modprobe -r floppy
