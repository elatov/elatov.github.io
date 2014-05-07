---
title: Monitor Different Systems with Collectd
author: Karim Elatov
layout: post
permalink: /2013/02/monitor-different-systems-with-collectd/
dsq_thread_id:
  - 1405507582
categories:
  - Home Lab
  - Networking
  - Storage
tags:
  - Collectd
  - Monitoring
---
In my home environment I only have 3 machines. I wanted to monitor them just for my own sake. At my previous job we used **Nagios** for such a task, but we also had thousands of machines and services to monitor. At home that is not the case. I just wanted a simple setup to show me CPU, memory, and network usage and that is about it.

### *nix Systems

My FreeBSD machine:

    freebsd:~>uname -smr 
    FreeBSD 9.1-RELEASE i386
    

My Fedora Machine:

    moxz:~>uname -sr 
    Linux 3.7.8-202.fc18.i686 
    moxz:~>lsb_release -rdc 
    Description: Fedora release 18 (Spherical Cow) 
    Release: 18 
    Codename: SphericalCow
    

My Ubuntu Machine:

    kerch:~>uname -sr 
    Linux 3.2.0-23-powerpc-smp 
    kerch:~>lsb_release -drc 
    Description: Ubuntu 12.10 
    Release: 12.10 
    Codename: quantal
    

### Monitoring Systems

As I kept researching, I discovered that there are many different monitoring applications out there. Most are included in the wikipedia page &#8220;<a href="http://en.wikipedia.org/wiki/Comparison_of_network_monitoring_systems" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Comparison_of_network_monitoring_systems']);">Comparison of network monitoring systems</a>&#8220;. Checking out other sites, I saw many different comparisons:

*   <a href="http://gajendrak.wordpress.com/2012/04/08/best-monitoring-tools-in-linux/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://gajendrak.wordpress.com/2012/04/08/best-monitoring-tools-in-linux/']);">Best Monitoring tools in Linux</a>
*   <a href="http://www.linuxscrew.com/2012/03/22/linux-monitoring-tools/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linuxscrew.com/2012/03/22/linux-monitoring-tools/']);">Top 5 Linux Monitoring Tools. Web Based.</a>
*   <a href="http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/']);">10 Free Server & Network Monitoring Tools that Kick Ass</a>
*   <a href="http://www.linuxlinks.com/article/20101118163040955/Monitoring-Extra.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linuxlinks.com/article/20101118163040955/Monitoring-Extra.html']);">6 More of the Best Free Linux Monitoring Tools</a>

As I mentioned, I have used Nagios before so I wanted to try something new. We also used **Cacti**, alongside with Nagios so I didn&#8217;t want to use that either. I cared about two aspects: simplicity and performance. Having said that, I decided to try out **Collectd**, from <a href="http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/']);">this</a> site:

> Collectd is similar to Munin and Cacti in that it focuses on graphing system metrics. Where it excels in is that it is designed specifically for performance and portability; this ultimately means it’s great on rugged systems, low-end systems, and embedded systems. Being designed for performance and low-system resource use means that Collectd can gather data every 10 seconds without interfering with your server processes, providing extremely high-resolution statistics.

Then I wanted to try out **Monitorix**, from their own <a href="http://www.monitorix.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.monitorix.org/']);">site</a>:

> Monitorix is a free, open source, lightweight system monitoring tool designed to monitor as many services and system resources as possible. It has been created to be used under production Linux/UNIX servers, but due to its simplicity and small size can be used on embedded devices as well.

But then checking out their <a href="http://linux.die.net/man/5/monitorix.conf" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://linux.die.net/man/5/monitorix.conf']);">configuration</a> page, I saw this for their network setup:

    REMOTEHOST_LIST This is a list of the remote servers where Monitorix it's already installed and working and you plan to monitor them from this one. It consists of a pair of values being in the left side the description of each server and in the right side the URL or IP address. An example of this list would be:
    
    our @REMOTEHOST_LIST = ( "WWW Linux", "http://www.example.com", "Backup Linux", "http://192.168.1.4", "SMTP Linux", "http://71.16.11.2:8080", );
    
    As you can see all three entries use URLs to designate the location of each remote server. This means that on each server most also have been installed a CGI capable web server like Apache. 
    

I didn&#8217;t want to run a webserver on each of my clients just so I could monitor them. So I decided to skip Monitorix.

I also wanted to try out **Munin**, from <a href="http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sixrevisions.com/tools/10-free-server-network-monitoring-tools-that-kick-ass/']);">this</a> site:

> One of Munin’s greatest strengths is how simple it is to extend. With just a few lines of code, you can write a plugin to monitor almost anything. Being so easy to extend means that Munin is also a good choice for graphing things unrelated to server performance, such as the number of user signups or website popularity.

Also from <a href="http://www.thegeekstuff.com/2009/09/top-5-best-network-monitoring-tools/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.thegeekstuff.com/2009/09/top-5-best-network-monitoring-tools/']);">here</a>:

> The primary emphasis of Munin is on the plug and play architecture for it’s plugin. There are lot of plugins available for Munin, which will just work out-of-the box without lot of tweaking.

Lastly I wanted to compare it to a large application just to see it&#8217;s Pro&#8217;s and Con&#8217;s. Since Nagios and Cacti were out of the picture, I decided to try **Zenoss**. There are a couple of sites that talk about the differences between Nagios and Zenoss, here are a few:

*   <a href="http://community.zenoss.org/docs/DOC-5858" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://community.zenoss.org/docs/DOC-5858']);">Zennos VS. Nagios</a> 
*   <a href="http://www.longitudetech.com/linux-unix/zenoss-we-can-ditch-nagios-now/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.longitudetech.com/linux-unix/zenoss-we-can-ditch-nagios-now/']);">Zenoss: We Can Ditch Nagios Now</a>

Zenoss seemed comparable <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Monitor Different Systems with Collectd" class="wp-smiley" title="Monitor Different Systems with Collectd" /> 

Since I picked 3 different applications, I will break this post into 3 different parts; one per application.

## Collectd

To send information across the network we need to configure a collector (server) and nodes (clients). Instructions on how to configure Collectd for such a setup are here: &#8220;<a href="https://collectd.org/wiki/index.php/Networking_introduction" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://collectd.org/wiki/index.php/Networking_introduction']);">Networking introduction</a>&#8220;

### 1. Install Collectd On Ubuntu and Configure it as a Collector/Server

First let&#8217;s install the software:

    kerch:~>sudo apt-get install collectd
    

After the install finishes, configure it. To do so, edit the **/etc/collectd/collectd.conf** file and enable any plugins you desire. Here is how my setup looked like:

    kerch:~>grep -v -E '^$|^#' /etc/collectd/collectd.conf 
    FQDNLookup true 
    LoadPlugin syslog 
    <plugin syslog> 
      LogLevel info 
    </plugin> 
    LoadPlugin cpu 
    LoadPlugin disk 
    LoadPlugin interface 
    LoadPlugin load 
    LoadPlugin memory 
    LoadPlugin network 
    LoadPlugin nfs 
    LoadPlugin rrdtool 
    LoadPlugin swap 
    <plugin network> 
      Listen "192.168.1.100" 
      <listen "192.168.1.100" > 
        SecurityLevel Sign 
        AuthFile "/etc/collectd/passwd" 
        Interface "eth0" 
      </listen> 
      MaxPacketSize 1452 
      CacheFlush 1800 
    </plugin> 
    <plugin rrdtool> 
      DataDir "/var/lib/collectd/rrd" 
    </plugin> 
    Include "/etc/collectd/filters.conf" 
    Include "/etc/collectd/thresholds.conf"
    

The **SecurityLevel** setup is probably unnecessary, but I wanted to try it out just in case. Here is how my password file looked like:

    kerch:~>cat /etc/collectd/passwd 
    elatov:test
    

I was actually running **iptables** on my Ubuntu machine, so I had to allow nodes/clients to connect to my Collectd collector. To do that, I edited the **/etc/iptables/rules.v4** file and added the following to it:

    -A INPUT -s 192.168.1.0/24 -p udp -m state --state NEW -m udp --dport 25826 -j ACCEPT
    

I then restarted my **iptables** instance to apply the changes:

    kerch:~>sudo service iptables-persistent restart 
    * Loading iptables rules...
    * IPv4...
    * IPv6... [ OK ]
    

Then I started the **collectd** Service:

    kerch:~>sudo service collectd start 
    Starting statistics collection and monitoring daemon: collectd.
    

### 2. Install Collectd on FreeBSD and set it up as Client

Let&#8217;s find the software:

    freebsd:~>whereis collectd 
    collectd: /usr/ports/net-mgmt/collectd
    

Now let&#8217;s go ahead and install it:

    freebsd:~>cd /usr/ports/net-mgmt/collectd 
    freebsd:/usr/ports/net-mgmt/collectd>sudo make install clean
    

At that point the compile process will fire up and install the software. Just for reference here are the configurations for the **collectd** package and it&#8217;s prerequisites:

    freebsd:/usr/ports/net-mgmt/collectd>make showconfig
    ===> The following configuration options are available for collectd-4.10.8_3:
         BIND=off: Enable BIND 9.5+ statistics
         CGI=on: Install collection.cgi (requires RRDTOOL)
         DEBUG=off: Enable debugging
         GCRYPT=on: Build with libgcrypt
         VIRT=off: Build with libvirt
    ====> Options available for the group INPUT
         APACHE=off: Apache mod_status (libcurl)
         APCUPS=off: APC UPS (apcupsd)
         CURL=off: CURL generic web statistics
         CURL_JSON=off: CURL JSON generic web statistics
         CURL_XML=off: CURL XML generic web statistics
         DBI=off: database abstraction library
         DISK=on: Disk performance statistics
         NUTUPS=off: NUT UPS daemon
         INTERFACE=on: Network interfaces (libstatgrab)
         MBMON=off: MBMon
         MEMCACHED=off: Memcached
         MYSQL=off: MySQL
         NGINX=off: Nginx
         OPENVPN=off: OpenVPN statistics
         PDNS=off: PowerDNS
         PGSQL=off: PostgreSQL
         PING=on: Network latency (liboping)
         PYTHON=off: Python plugin
         ROUTEROS=off: RouterOS plugin
         SNMP=on: SNMP
         TOKYOTYRANT=off: Tokyotyrant database
         XMMS=off: XMMS
    ====> Options available for the group OUTPUT
         RRDTOOL=on: RRDTool
         RRDCACHED=on: RRDTool Cached (require RRDTOOL)
         WRITE_HTTP=off: write_http
    ===> Use 'make config' to modify these settings
    

Here is the config for **rrdtool**:

    freebsd:/usr/ports/databases/rrdtool>make showconfig
    ===> The following configuration options are available for rrdtool-1.4.7_2:
         DEJAVU=off: Use DejaVu fonts (requires X11)
         JSON=off: Support of json export
         MMAP=on: Use mmap in rrd_update
         PERL_MODULE=on: Build PERL module
         PYTHON_MODULE=off: Build PYTHON bindings
         RUBY_MODULE=off: Build RUBY bindings
    ===> Use 'make config' to modify these settings
    

Lastly here is the configuration for **net-snmp**:

    freebsd:/usr/ports/net-mgmt/net-snmp>make showconfig
    ===> The following configuration options are available for net-snmp-5.7.2_2:
         AX_SOCKONLY=off: Disable UDP/TCP transports for agentx
         DMALLOC=off: Enable dmalloc debug memory allocator
         DUMMY=on: Enable dummy values as placeholders
         IPV6=off: IPv6 protocol
         MFD_REWRITES=off: Build with 64-bit Interface Counters
         MYSQL=off: MySQL database
         PERL=on: Perl scripting language
         PERL_EMBEDDED=on: Build embedded perl
         PYTHON=off: Python bindings
         TKMIB=off: Install graphical MIB browser
         UNPRIVILEGED=off: Allow unprivileged users to execute net-snmp
    ===> Use 'make config' to modify these settings
    

After the software is installed, we need to configure it. Edit the **/usr/local/etc/collectd.conf** file and make the necessary changes. Here is how my file looked like:

    freebsd:~>grep -v -E '^$|^#' /usr/local/etc/collectd.conf 
    Hostname "freebsd.dnsd.me" 
    FQDNLookup true 
    LoadPlugin syslog 
    <plugin syslog> 
      LogLevel info 
    </plugin> 
    LoadPlugin cpu 
    LoadPlugin disk 
    LoadPlugin interface 
    LoadPlugin load 
    LoadPlugin memory 
    LoadPlugin network 
    LoadPlugin rrdtool 
    LoadPlugin swap 
    <plugin network> 
      # client setup: 
      Server "192.168.1.100" 
      <server "192.168.1.100"> 
        SecurityLevel Encrypt 
        Username "elatov" 
        Password "test" 
      </server> 
      CacheFlush 1800 
    </plugin> 
    <plugin rrdtool> 
      DataDir "/var/lib/collectd/rrd" 
      CacheTimeout 120 
      CacheFlush 900 
    </plugin>
    

Now let&#8217;s enable the daemon, this is done by editing **/etc/rc.conf** and adding the following:

    collectd_enable="YES"
    

Now let&#8217;s start the **collectd** daemon:

    freebsd:~>sudo /usr/local/etc/rc.d/collectd start
    

At this point we can check to make sure the files are now getting uploaded to the collector machine (our Ubuntu Machine):

    kerch:~>ls -1 /var/lib/collectd/rrd/ 
    freebsd.dnsd.me 
    kerch.dnsd.me
    

That looks good, now let&#8217;s install a web GUI for Collectd.

### 3. Install Collectd-Web Front End on the Collector

There are multiple options, <a href="https://collectd.org/wiki/index.php/List_of_front-ends" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://collectd.org/wiki/index.php/List_of_front-ends']);">this</a> page has a list of available front ends for Collectd.

I decided to go with **Collectd-Web** cause it seemed simple. Instructions on how to install the software can be found <a href="http://collectdweb.appspot.com/documentation/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://collectdweb.appspot.com/documentation/']);">here</a>. First download the necessary files:

    kerch:~>git clone git://github.com/httpdss/collectd-web.git
    

then make sure all the dependencies look good:

    kerch:~>cd collectd-web 
    kerch:~/collectd-web>./check_deps.sh 
    Carp looks ok 
    CGI looks ok 
    CGI::Carp looks ok 
    HTML::Entities looks ok 
    URI::Escape looks ok 
    RRDs looks ok 
    Data::Dumper looks ok 
    JSON looks ok
    

Now let&#8217;s just copy the whole directory to a folder where your web Server (I was using *Apache* for other uses) can host the files:

    kerch:~>sudo rsync -avzP collectd-web/. /var/www/cw/.
    

Lastly make sure *collectd* looks under the correct location (where the *RRD* files are stored):

    kerch:~>cat /etc/collectd/collection.conf 
    datadir: "/var/lib/collectd/rrd/" 
    libdir: "/usr/lib/collectd/"
    

This should be the default, but just in case. Now visiting the Collectd-Web portal (**http://localhost/cw**), I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-first-page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-first-page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-first-page.png" alt="collectd web first page Monitor Different Systems with Collectd" width="456" height="227" class="alignnone size-full wp-image-6346" title="Monitor Different Systems with Collectd" /></a>

Selecting the remote host (freebsd) and then the CPU option, allowed me to see the CPU stats of my FreeBSD machine:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-cpu.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-cpu.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-cpu.png" alt="collectd web freebsd cpu Monitor Different Systems with Collectd" width="959" height="409" class="alignnone size-full wp-image-6347" title="Monitor Different Systems with Collectd" /></a>

Now let&#8217;s configure the Fedora machine to send information to the collector.

### 4. Install Collectd on Fedora and Configure it as a Client

First install the **collectd** package:

    moxz:~>sudo yum install collectd collectd-rrdtool
    

Then I edited the **/etc/collectd.conf** and configured the same things as before:

    moxz:~>grep -v -E '^#|^$' /etc/collectd.conf 
    Hostname "moxz.dnsd.me" 
    FQDNLookup true 
    LoadPlugin syslog 
    <plugin syslog> 
    LogLevel info 
    </plugin> 
    LoadPlugin cpu 
    LoadPlugin disk 
    LoadPlugin interface 
    LoadPlugin load 
    LoadPlugin memory 
    LoadPlugin network 
    LoadPlugin nfs 
    LoadPlugin rrdtool 
    <plugin network> 
      Server 192.168.1.100 
      <server "192.168.1.100"> 
        SecurityLevel Encrypt 
        Username "elatov" 
        Password "test" 
        Interface "eth0" 
      </server> 
      CacheFlush 1800 
    </plugin> 
    Include "/etc/collectd.d"
    <plugin rrdtool> 
      DataDir "/var/lib/collectd/rrd" 
      CacheTimeout 120 
      CacheFlush 900 
    </plugin>
    

I then enabled the service:

    moxz:~>sudo systemctl enable collectd 
    ln -s '/usr/lib/systemd/system/collectd.service' '/etc/systemd/system/multi-user.target.wants/collectd.service'
    

Starting the service looked like this:

    moxz:~>sudo systemctl start collectd 
    moxz:~>sudo systemctl status collectd
    collectd.service - Collectd
              Loaded: loaded (/usr/lib/systemd/system/collectd.service; enabled)
              Active: active (running) since Wed 2013-02-27 13:08:06 PST; 2 days ago
            Main PID: 711 (collectd)
              CGroup: name=systemd:/system/collectd.service
                      └─711 /usr/sbin/collectd -C /etc/collectd.conf -f
    

I then visited the same Collectd-Web portal and saw the new host&#8217;s stats.

All of the above was for Collectd version 4. A newer version is out, version 5, and migration steps are available <a href="https://collectd.org/wiki/index.php/V4_to_v5_migration_guide" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://collectd.org/wiki/index.php/V4_to_v5_migration_guide']);">here</a>. Make sure at least the collector is at version 5, but it would be best to have both collector and nodes be at the same version.

The last thing I wanted to do was check on the status of my raid on the FreeBSD machine.

### 5. Configure a Custom Script On the FreeBSD Collectd Client

There is a command line program called **arcconf** which allows you to see the status. Here is how it looks:

    freebsd:~>sudo arcconf getconfig 1
    Controllers found: 1
    ----------------------------------------------------------------------
    Controller information
    ----------------------------------------------------------------------
       Controller Status                        : Optimal
       Channel description                      : SATA
       Controller Model                         : CERC SATA1.5/6ch
       Controller Serial Number                 : BBE5AA
       Installed memory                         : 64 MB
       Copyback                                 : Disabled
       Background consistency check             : Enabled
       Automatic Failover                       : Enabled
       Stayawake period                         : Disabled
       Spinup limit internal drives             : 0
       Spinup limit external drives             : 0
       Defunct disk drive count                 : 0
       Logical devices/Failed/Degraded          : 1/0/0
       --------------------------------------------------------
       Controller Version Information
       --------------------------------------------------------
       BIOS                                     : 4.1-0 (7417)
       Firmware                                 : 4.1-0 (7417)
       Driver                                   : 2.1-9 (1)
       Boot Flash                               : 0.0-0 (0)
       --------------------------------------------------------
       Controller Battery Information
       --------------------------------------------------------
       Status                                   : Not Installed
    
    ----------------------------------------------------------------------
    Logical device information
    ----------------------------------------------------------------------
    Logical device number 0
       Logical device name                      : DATA 1
       RAID level                               : 1
       Status of logical device                 : Optimal
       Size                                     : 152554 MB
       Read-cache mode                          : Enabled
       Write-cache mode                         : Disabled (write-through)
       Write-cache setting                      : Disabled (write-through)
       Partitioned                              : Yes
       Protected by Hot-Spare                   : No
       Bootable                                 : Yes
       Failed stripes                           : No
       Power settings                           : Disabled
       --------------------------------------------------------
       Logical device segment information
       --------------------------------------------------------
       Segment 0                                : Present (Controller:1,Channel:0,Device:1) Y450QB3E
       Segment 1                                : Present (Controller:1,Channel:0,Device:0) Y450QA0E
    
    
    ----------------------------------------------------------------------
    Physical Device information
    ----------------------------------------------------------------------
       Channel #0:
          Transfer Speed                        : SATA 1.5 Gb/s
          Device #0
             Device is a Hard drive
             State                              : Online
             Supported                          : Yes
             Transfer Speed                     : SATA 1.5 Gb/s
             Reported Channel,Device(T:L)       : 0,0(0:0)
             Vendor                             : Maxtor
             Model                              : 6Y160M0
             Firmware                           : YAR5
             Serial number                      : Y450QA0E
             Size                               : 152587 MB
             Write Cache                        : Unknown
             FRU                                : None
             S.M.A.R.T.                         : No
             S.M.A.R.T. warnings                : 0
             NCQ status                         : Disabled
          Device #1
             Device is a Hard drive
             State                              : Online
             Supported                          : Yes
             Transfer Speed                     : SATA 1.5 Gb/s
             Reported Channel,Device(T:L)       : 0,1(1:0)
             Vendor                             : Maxtor
             Model                              : 6Y160M0
             Firmware                           : YAR5
             Serial number                      : Y450QB3E
             Size                               : 152587 MB
             Write Cache                        : Unknown
             FRU                                : None
             S.M.A.R.T.                         : No
             S.M.A.R.T. warnings                : 0
             NCQ status                         : Disabled
    Command completed successfully.
    

There are no SMART capabilities, so the only thing I can check is whether the disks are online. Here is a concise view:

    freebsd:~>arcconf getconfig 1 PD| grep State 
    State : Online 
    State : Online
    

we have two disks that are online. Collectd has a plugin called **exec**, it allows you to run a command and plot values from the results of that command. More information can be seen <a href="http://collectd.org/documentation/manpages/collectd-exec.5.shtml" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://collectd.org/documentation/manpages/collectd-exec.5.shtml']);">here</a> and <a href="https://collectd.org/wiki/index.php/Plugin:Exec" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','']);">here</a>. If we had SMART capabilities, we could use the scripts created from <a href="http://devel.dob.sk/collectd-scripts/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://devel.dob.sk/collectd-scripts/']);">this</a> post. But I will settle with just plotting how many disks are currently online. So I wrote this script:

<pre>#!/usr/local/bin/bash
HOST=$(hostname -f)
INTERVAL=300
while sleep "$INTERVAL"; do
        val=$(/usr/local/sbin/arcconf getconfig 1 PD | grep State | grep Online| /usr/bin/wc -l)
        echo "PUTVAL \"$HOST/exec-raid/gauge\" interval=$INTERVAL N:$(eval echo \$val)"
done
</pre>

Nothing fancy, it just counts how many disks are online and sets the interval to be 300 (5 minutes). As a quick test change the interval value to 10 and run the script, it should produce something similar to this:

    freebsd:~>./arc.sh 
    PUTVAL "freebsd.dnsd.me/exec-raid/gauge" interval=10 N:2 
    PUTVAL "freebsd.dnsd.me/exec-raid/gauge" interval=10 N:2
    

Now let&#8217;s enable this to be executed from Collectd. Edit **/usr/local/etc/collectd.conf** and add/modify the following

    <plugin exec>
            Exec "elatov:elatov" "/home/elatov/arc.sh"
    </plugin>
    

After some time the graph started to populate with data. Here is a very small sample of how it looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-raid-gauge.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-raid-gauge.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/collectd-web-freebsd-raid-gauge.png" alt="collectd web freebsd raid gauge Monitor Different Systems with Collectd" width="962" height="375" class="alignnone size-full wp-image-6353" title="Monitor Different Systems with Collectd" /></a>

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor Disk IO Stats with Zabbix" href="http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/']);" rel="bookmark">Monitor Disk IO Stats with Zabbix</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor Different Systems with Zabbix" href="http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zabbix/']);" rel="bookmark">Monitor Different Systems with Zabbix</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor Different Systems with Zenoss" href="http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zenoss/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/monitor-different-systems-with-zenoss/']);" rel="bookmark">Monitor Different Systems with Zenoss</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Monitor Different Systems with Munin" href="http://virtuallyhyper.com/2013/03/monitor-different-systems-with-munin/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/monitor-different-systems-with-munin/']);" rel="bookmark">Monitor Different Systems with Munin</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/02/monitor-different-systems-with-collectd/" title=" Monitor Different Systems with Collectd" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Collectd,Monitoring,blog;button:compact;">This is the second part and continuation of the &#8216;Network Monitoring Software Comparison&#8217; series. Here is the link to the first part. Let&#8217;s go ahead and check out our software:...</a>
</p>