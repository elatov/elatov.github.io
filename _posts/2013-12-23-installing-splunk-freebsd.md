---
title: Installing Splunk on FreeBSD
author: Karim Elatov
layout: post
permalink: /2013/12/installing-splunk-freebsd/
dsq_thread_id:
  - 2050379030
categories:
  - OS
tags:
  - freebsd
  - mod_proxy
  - Splunk
---
I had an old box laying around that wasn't really doing anything. It only had 1GB of RAM, but that is good enough for a splunk install.

### Splunk

I checked the [Splunk System Requirements](http://docs.splunk.com/Documentation/Splunk/6.0/Installation/Systemrequirements) and I was okay:

![splunk hw capacity Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/splunk-hw-capacity.png)

This was just for a home setup, I was only planning to monitor 6-8 machines.

#### Splunk Install

Looking over the download page, I saw that FreeBSD 9 is supported:

![freebsd download Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/freebsd_download.png)

I grabbed the intel/native package and then ran the following to install it:

    $ sudo pkg_add splunk-6.0-182037-freebsd-7.3-intel.tgz


The Splunk Documentation had a couple of post install instructions. From their [install](http://docs.splunk.com/Documentation/Splunk/6.0/Installation/InstallonFreeBSD) page:

> To ensure that Splunk functions properly on FreeBSD, you must:
>
> 1.  Add the following to /boot/loader.conf
>
>         kern.maxdsiz="2147483648" # 2GB
>         kern.dfldsiz="2147483648" # 2GB
>         machdep.hlt_cpus=0
>
>
> 2.  Add the following to /etc/sysctl.conf:
>
>         vm.max_proc_mmap=2147483647
>
>
> A restart of the OS is required for the changes to effect.
>
> If your server has less than 2 GB of memory, reduce the values accordingly.

The second setting (**vm.max_proc_mmap**) no longer existed on FreeBSD 9, so only I added the following to my **/boot/loader.conf** file:

    kern.maxdsiz="1063256064"
    kern.dfldsiz="1063256064"
    machdep.hlt_cpus=0


And restarted the machine to apply the changes.

#### First Start for Splunk

After the reboot I decided to start the splunk service:

    $ cd /opt/splunk/bin
    $ sudo ./splunk start


And I saw the following:

    This appears to be your first time running this version of Splunk.
    Copying '/opt/splunk/etc/openldap/ldap.conf.default' to '/opt/splunk/etc/openldap/ldap.conf'.
    Generating RSA private key, 1024 bit long modulus
    ...........................++++++
    ...++++++
    e is 65537 (0x10001)
    writing RSA key

    Generating RSA private key, 1024 bit long modulus
    .................++++++
    ...............................++++++
    e is 65537 (0x10001)
    writing RSA key

    Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.

    Splunk> Winning the War on Error

    Checking prerequisites...
    WARNING: Data segment size limit (ulimit -d) is set low (1063256064 bytes)  Splunk may not work.
             You may want to run "ulimit -d unlimited" before starting splunk.
    On FreeBSD the system-wide limit may need to be increased by adding the following lines to /boot/loader.conf:
      kern.maxdsiz="2147483648" # 2GB
      kern.dfldsiz="2147483648" # 2GB
    :You will need to reboot for the new defaults to take effect.
            Checking http port [8000]: open
            Checking mgmt port [8089]: open
            Checking configuration...  Done.
                    Creating: /opt/splunk/var/lib/splunk
                    Creating: /opt/splunk/var/run/splunk
                    Creating: /opt/splunk/var/run/splunk/appserver/i18n
                    Creating: /opt/splunk/var/run/splunk/appserver/modules/static/css
                    Creating: /opt/splunk/var/run/splunk/upload
                    Creating: /opt/splunk/var/spool/splunk
                    Creating: /opt/splunk/var/spool/dirmoncache
                    Creating: /opt/splunk/var/lib/splunk/authDb
                    Creating: /opt/splunk/var/lib/splunk/hashDb
            Checking critical directories...        Done
            Checking indexes...
                    Validated: _audit _blocksignature _internal _thefishbucket history main summary
            Done
    New certs have been generated in '/opt/splunk/etc/auth'.
            Checking filesystem compatibility...  Done
            Checking conf files for typos...        Done
    All preliminary checks passed.

    Starting splunk server daemon (splunkd)...
    Done

    Starting splunkweb...  Generating certs for splunkweb server
    Generating a 1024 bit RSA private key
    ......................................++++++
    ............................................................++++++
    writing new private key to 'privKeySecure.pem'
    -----
    Signature ok
    subject=/CN=moxz/O=SplunkUser
    Getting CA Private Key
    writing RSA key
    Done

    If you get stuck, we're here to help.
    Look for answers here: http://docs.splunk.com

    The Splunk web interface is at http://moxz:8000


It did give me a warning about my **ulimit** settings but that's okay since I only had 1GB of RAM. To make sure it's running I ran the following:

    $ sudo ./splunk status
    splunkd is running (PID: 1151).
    splunk helpers are running (PIDs: 1152).
    splunkweb is running (PID: 1193).


That looked good. I went to the Splunk Web Portal and I saw the same thing as in my [previous](http://virtuallyhyper.com/2013/06/install-splunk-and-send-logs-to-splunk-with-rsyslog-over-tcp-with-ssl/) post.

#### Setup Splunk to Receive Syslog Logs over UDP 514

This was going to be internal, so I just wanted to setup the easiest data source. Using **UDP 514** for a Syslog Server is pretty standard. By default the **syslogd** service running on FreeBSD listens on **UDP 514**. First let's disable that, this is done by editing **/etc/rc.conf** file and adding the following to it:

    syslogd_enable="YES"
    syslogd_flags="-ss"


You ran then restart the **syslogd** process to apply the settings:

    $ sudo service syslogd restart


Now we can add a Data Source to listen on UDP 514 for Syslog Logs. From the Splunk Web Portal Home Page click on **Data Inputs** and you should see the following:

![splunk data inputs Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/splunk-data-inputs.png)

Then click on **UDP** and fill out all the settings:

![514 data input Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/514-data-input.png)

Then click **Save** and you should be all set. You can confirm it's listening on that port by running the following on the Splunk server:

    $ sudo /opt/splunk/bin/splunk list udp
    Password:
    Your session is invalid.  Please login.
    Splunk username: admin
    Password:
    Listening for input on the following UDP ports:
        514


#### Configure Machines to Log to Splunk

I only run *nix systems at home, so most of the configurations are the same. Here is what I did on my Linux systems that are running **rsyslogd**:

    $ sudo vi /etc/rsyslog.conf


and then add the following to the bottom:

    *.* @192.168.1.102


And lastly restart the **rsyslog** service to apply the change:

    $ sudo service rsyslog restart


On the WRT router, you can go to the **Services** Tab and configure it to send logs to a remote syslog server : ![wrt syslog Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/wrt-syslog.png)

On OpenELEC, you can go to the OpenELEC settings and under **Services** you can specify a remote syslog server:

![openelec remote syslog Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-remote-syslog.png)

After I was done with the configurations, here are all the hosts seen in splunk (under **Search** -> **Data Summary**):

![data summary g Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/data-summary_g.png)

#### Setup Splunk to Automatically Start on boot

The install comes with a setup script for this. Here is what I ran to enable splunk to start on boot:

    $ sudo /opt/splunk/bin/splunk enable boot-start


After that is done, you can run the following commands:

    $ sudo service splunk {start,stop,restart,status}


You will also see that an entry is added to **rc.conf** file automatically:

    $ grep splunk /etc/rc.conf
    splunk_enable="YES"


#### Lower Splunk Log Retention

By default 6 years worth of logs are kept. From [Set a retirement and archiving policy](http://docs.splunk.com/Documentation/Splunk/6.0/Indexer/Setaretirementandarchivingpolicy):

> **Set attributes for cold to frozen rolling behavior**
> The *maxTotalDataSizeMB* and *frozenTimePeriodInSecs* attributes in indexes.conf help determine when buckets roll from cold to frozen. These attributes are described in detail below.

More information:

> You can use the size of an index to determine when data gets frozen and removed from the index. If an index grows larger than its maximum specified size, the oldest data is rolled to the frozen state.
>
> The default maximum size for an index is 500,000MB. To change the maximum size, edit the maxTotalDataSizeMB attribute in indexes.conf. For example, to specify the maximum size as 250,000MB

And the second parameter:

> You can use the age of data to determine when a bucket gets rolled to frozen. When the most recent data in a particular bucket reaches the configured age, the entire bucket is rolled.
>
> To specify the age at which data should freeze, edit the frozenTimePeriodInSecs attribute in indexes.conf. This attribute specifies the number of seconds to elapse before data gets frozen. The default value is 188697600 seconds, or approximately 6 years.

I decided to set the size to 100GB and the time to be 90 days (7776000 seconds). So if data is more than 90 days, it's removed. If the the index size gets bigger than 100 GB, it will be removed as well. To apply those settings edit the /**opt/splunk/etc/system/default/indexes.conf** file and modify the following parameters:

    frozenTimePeriodInSecs = 7776000
    maxTotalDataSizeMB = 100000


To apply those settings, restart the splunk server:

    $ sudo service splunk restart


I don't want to waste space on old data. I checked my Quota usage under "**Settings**" -> "**Licensing**" -> "**Usage Report**" and I wasn't even close to reaching the quota:

![license usage splunk g Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/license-usage-splunk_g.png)

Unrelated to my above settings, but still good to know.

#### Change the License Group to Free for Splunk

I know I have a 60 day Enterprise trial version, but before I get used to all the neat features, I wanted to setup and use the Free version of Splunk. To change the License Group, go to **Settings** -> **Licensing**:

![system license g Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/system-license_g.png)

Then click on **Change License Group**. Select the Free License and apply. It will restart splunk to apply the change. If you go back to **Settings** -> **Licensing** you should see the following:

![splunk license group Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/splunk-license-group.png)

#### Disable the Welcome Page for Splunk Free Version

As soon as you switch over to the Free License, you will notice that the authentication page is no longer present and splunk will check for an update and if it doesn't find one it will ask you to continue:

![splunk free version welcome screen Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/splunk-free-version-welcome-screen.png)

Upon clicking **Continue**, it will just log you without any sort of authentication. First let's go ahead and disable that page. I ran across [this](http://answers.splunk.com/answers/4981/disabling-welcome-screen) splunk community page, which helped. To get rid of the welcome/update page, edit (or create if it doesn't exist) the **/opt/splunk/etc/system/local/web.conf** file and add the following to it:

    [settings]
     updateCheckerBaseURL = 0


Then restart splunk to apply the changes:

    $ sudo service splunk restart


After that when you visit the Splunk Web Portal it will just log you in without showing that page.

#### Configure a Reverse Proxy for Splunk Free Version

Now that there is no authentication and I wanted to check the splunk web portal externally, I decided to setup a reverse proxy for splunk. The process is described in the "[Placing Splunk behind a Web proxy](http://wiki.splunk.com/Community:SplunkBehindAProxy)" page from the splunk community. I already had an *apache* server running on my Debian box, so I decided to utilize that server as a reverse proxy. First let's install the **mod-proxy** module for **apache**:

    $ sudo apt-get install libapache2-mod-proxy-html


Then enable the proxy modules:

    $ sudo a2enmod proxy
    $ sudo a2enmod proxy_http


Then setup the reverse proxy to keep the hostname of the webserver rather that showing the internal IP of the splunk server. This is done by editing the **/etc/apache2/mods-enabled/proxy.conf** file and adding/modifying the following:

    #ProxyRequests On
    ProxyPreserveHost On


Then setup the **/splunk** location to be proxied, this is done by editing the virtualhost configuration. In my case I only had the default one, so I edited the **/etc/apache2/sites-enabled/000-default** file (edit the appropriate configuration file that applies in your environment), and I added the following to it:

    <Location /splunk>
      ProxyPass                   http://192.168.1.102:8000/splunk retry=0
      ProxyPassReverse            retry=0
    </Location>


Then restart apache and you should all set:

    $ sudo service apache2 restart


#### Change Root Endpoint for Splunk

Since we want all of our requests to start with **/splunk** we need to change the Splunk configuration to reflect that. This is done by editing the **/opt/splunk/etc/system/local/web.conf** file and making it look like this:

    [settings]
     root_endpoint = /splunk
     updateCheckerBaseURL = 0


To apply the settings restart splunk:

    $ sudo service splunk restart


Now if you visit **http://SPLUNK_SERVER:8000**, you should see all the URLs start with **/splunk**, like so:

![splunk url changed g Installing Splunk on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2013/11/splunk-url-changed_g.png)

Now if you visit **http://YOUR_WEBSERVER/splunk**, it should take to the Splunk Web Portal.

#### Password Protect the Splunk Web Portal Location in Apache

Now that the reverse proxy is setup and working, let's password protect the **/splunk** location. This can be accomplished with a regular **htpassword** file (you can even use **htdigest** if you want). First let's create a directory where we will store the password file:

    $ sudo mkdir /etc/apache2/pass
    $ sudo chgrp www-data /etc/apache2/pass
    $ sudo chmod o-rx /etc/apache2/pass


Then let's create the **htpasswd** file:

    $ sudo htpasswd -c /etc/apache2/pass/htpasswd admin


(I made the username be the same as the **admin** used, when I had the Enterprise trial)

Lastly let's make sure only the **www-data** group can read that file:

    $ sudo chmod 640 /etc/apache2/pass/htpasswd
    $ sudo chgrp www-data /etc/apache2/pass/htpasswd


Lastly add the following section to the **/etc/apache2/sites-enabled/000-default** file:

      <Location /splunk>
        ProxyPass                   http://192.168.1.102:8000/splunk retry=0
        ProxyPassReverse            retry=0
        AuthType Basic
        AuthName "Splunk"
        AuthUserFile /etc/apache2/pass/htpasswd
        Require valid-user
      </Location>


Now if you visit to your splunk instance which is behind the reverse proxy, you will be prompted for a password.

#### Configure FreeBSD Firewall to Only Allow Local Network Access to Splunk Web

So let's configure the firewall to only allow **TCP 8000** from the local network. This is done by editing the **/etc/pf.conf** file and adding the following:

    # accept splunk-web sessions
    pass in on $my_int proto tcp from 192.168.1.0/24 to any port 8000 keep state


Then apply the rules:

    $ sudo pfctl -f /etc/pf.conf


and make sure the rule is in place:

    $ sudo pfctl -s rules | grep 8000
    pass in on em0 inet proto tcp from 192.168.1.0/24 to any port = 8000 flags S/SA keep state


That should be it. Only local access is allowed to the Splunk Web Portal directly, and to access the Splunk Web Portal externally you have to go through the reverse proxy which is password protected.

