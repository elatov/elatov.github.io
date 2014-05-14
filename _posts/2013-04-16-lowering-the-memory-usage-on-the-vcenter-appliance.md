---
title: Lowering the Memory Usage on the vCenter Appliance
author: Jarret Lavallee
layout: post
permalink: /2013/04/lowering-the-memory-usage-on-the-vcenter-appliance/
dsq_thread_id:
  - 1404706933
categories:
  - Home Lab
  - OS
  - VMware
tags:
  - ps_mem
  - vcenter
  - VirtualAppliance
---
I set up many virtual labs that include one or more vCenters. In vCenter 5.1+ the default memory allocation has grown to 8GB, which is way more than I want to allocate in a lab.

The problem is that there are more and more services being packed into the vCenter and the majority are written in Java. Java is a great language as it is cross-platform, but it can be seen as bulky. Most of the bulk comes from the Java Virtual Machine(JVM) which is given a memory heap to draw from. The good news is that we can change the heap sizes for each JVM service. <a href="http://defaultreasoning.com/2012/09/27/tweaking-java-exe-memory-usage-on-vcenter-server-5-1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://defaultreasoning.com/2012/09/27/tweaking-java-exe-memory-usage-on-vcenter-server-5-1/']);">Here</a> is a good post on changing these values. You can take that guide and get the vCenter Server down to a good number. In this post we will look a little deeper into the vCenter Server Appliance.

**NOTE:** this procedure is not supported by VMware. Lowering the heap allocations too low will result in *Allocation Errors*, so if you experience issues after lowering the values as described, look for these errors in the logs and increase the memory on the correct components.

## Understanding the Heap

First we need to understand the java heap to be able to tweak it appropriately. <a href="http://javarevisited.blogspot.com/2011/05/java-heap-space-memory-size-jvm.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://javarevisited.blogspot.com/2011/05/java-heap-space-memory-size-jvm.html']);">This article</a> goes over the basics of the java heap. Let&#8217;s take a look at the options that we have to set the heap.

    # java -X |grep -i heap
    -Xms<size>        set initial Java heap size
    -Xmx</size><size>        set maximum Java heap size
    

So we have **-Xms** which is the minimum heap size. This will be the initial heap size given to java when it starts, even if the application is using less memory. VMware has set these to relatively high numbers for these services.

We also have the **-Xmx** which is the maximum heap size. This will be the upper limit to how large the heap can grow for this application. Since different services will have different memory usage patters, we will expect this to range in the configuration.

## Determining Memory Usage

Before we start changing the java heap sizes, we should get an idea on what the memory usage looks like. This will give us a better idea of what we need to cut and how much we can expect to run on.

First, let&#8217;s take a look at the appliance before it has been configured. I will take this as the baseline for the minimum amount of memory it can run in. I deployed a new vCenter Appliance and logged in after it booted. The following shows that we are using 169M of memory.

    localhost:~ # free -m
                 total       used       free     shared    buffers     cached
    Mem:          8002        471       7530          0          8        293
    -/+ buffers/cache:        169       7833
    Swap:        15366          0      15366
    

So 169M is our baseline for low memory. Let&#8217;s see what is running and what services we may be able to get rid of if we wanted to lower the stock footprint.

    localhost:~ # chkconfig |grep on
    auditd                   on
    cron                     on
    dbus                     on
    dcerpcd                  on
    earlysyslog              on
    eventlogd                on
    fbset                    on
    haldaemon                on
    haveged                  on
    irq_balancer             on
    kbd                      on
    ldap                     on
    lsassd                   on
    lwiod                    on
    lwregd                   on
    lwsmd                    on
    netlogond                on
    network                  on
    network-remotefs         on
    nfs                      on
    purge-kernels            on
    random                   on
    rpcbind                  on
    sendmail                 on
    splash                   on
    splash_early             on
    syslog                   on
    syslog-collector         on
    vmci                     on
    vmmemctl                 on
    vmware-netdumper         on
    vmware-tools-services    on
    vsock                    on
    

In the output above we can see many stock services running. This would be a starting point if you wanted to lower the memory footprint by a few MB. I am not going to pursue that here as it will only save a few MB and may break vCenter services.

Let&#8217;s break down these processes by memory size. There is a great utility called **ps_mem** that will take the reservation size from the output of **ps** and show the memory utilization from a set of processes. The script can be found <a href="http://www.pixelbeat.org/scripts/ps_mem.py" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.pixelbeat.org/scripts/ps_mem.py']);">here</a>.

Download the script.

    localhost:~ # wget http://www.pixelbeat.org/scripts/ps_mem.py
    

Run the script.

    localhost:~ # python ps_mem.py
     Private  +   Shared  =  RAM used       Program
    
    160.0 KiB +  30.0 KiB = 190.0 KiB       irqbalance
    220.0 KiB +  22.0 KiB = 242.0 KiB       dhcpcd
    208.0 KiB +  51.5 KiB = 259.5 KiB       init
    244.0 KiB +  71.0 KiB = 315.0 KiB       cron
    372.0 KiB +  19.5 KiB = 391.5 KiB       klogd
    264.0 KiB + 128.5 KiB = 392.5 KiB       hald-runner
    488.0 KiB +  36.5 KiB = 524.5 KiB       syslog-ng
    332.0 KiB + 272.5 KiB = 604.5 KiB       hald-addon-acpi
    568.0 KiB +  40.5 KiB = 608.5 KiB       dbus-daemon
    340.0 KiB + 301.0 KiB = 641.0 KiB       hald-addon-input
    804.0 KiB +  42.5 KiB = 846.5 KiB       vami-lighttpd
    804.0 KiB + 297.5 KiB =   1.1 MiB       mingetty (5)
    324.0 KiB + 911.0 KiB =   1.2 MiB       udevd (3)
    640.0 KiB + 618.0 KiB =   1.2 MiB       hald-addon-storage (2)
    964.0 KiB + 486.0 KiB =   1.4 MiB       vami_login
      1.3 MiB + 324.0 KiB =   1.6 MiB       console-kit-daemon
      2.0 MiB + 148.0 KiB =   2.1 MiB       bash
      2.4 MiB + 305.5 KiB =   2.7 MiB       hald
      2.5 MiB + 220.5 KiB =   2.7 MiB       vmtoolsd
      2.8 MiB + 785.0 KiB =   3.5 MiB       sshd (2)
      2.8 MiB +   1.3 MiB =   4.1 MiB       vami-sfcbd (8)
      4.2 MiB +  18.0 KiB =   4.2 MiB       haveged
     33.7 MiB + 160.5 KiB =  33.8 MiB       slapd
    ---------------------------------
                             64.6 MiB
    =================================
    

We can see in the output above the user space processes are taking up 64M of memory. The biggest usage is *slapd* which is the <a href="http://www.openldap.org/software/man.cgi?query=slapd" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openldap.org/software/man.cgi?query=slapd']);">openLDAP daemon</a>. Another notable one is the *vami-sfcbd* which is the web interface on port 5840.

Now that we have a baseline, go ahead and configure the appliance the way you want it by connecting to *https://hostname:5840*. I went ahead and configured it with the default settings.

Let&#8217;s take a look at the memory using the **free** command again.

    localhost:~ # free -m
                 total       used       free     shared    buffers     cached
    Mem:          8002       4658       3344          0         71       1487
    -/+ buffers/cache:       3099       4903
    Swap:        15366          0      15366
    

By starting the services, our memory utilization went from 169M to 3099M. So we either have processes that are using that memory or the java initial heaps have been created and the memory is sitting there reserved. Let&#8217;s take a look at the **ps_mem** command again.

    localhost:~ # python ps_mem.py |tail -n 15
      2.5 MiB + 161.5 KiB =   2.6 MiB       vmtoolsd
      2.4 MiB + 272.5 KiB =   2.6 MiB       hald
      1.7 MiB +   1.0 MiB =   2.8 MiB       vami-sfcbd (7)
      1.8 MiB +   1.4 MiB =   3.2 MiB       sendmail (3)
      2.6 MiB + 726.0 KiB =   3.4 MiB       sshd (2)
      2.5 MiB + 993.0 KiB =   3.5 MiB       lsassd
      4.2 MiB +  12.0 KiB =   4.2 MiB       haveged
      4.7 MiB + 421.0 KiB =   5.1 MiB       python2.6
     27.7 MiB + 160.0 KiB =  27.9 MiB       slapd
     45.3 MiB +  12.6 MiB =  57.8 MiB       postmaster (23)
    133.4 MiB + 353.5 KiB = 133.7 MiB       vpxd
      2.9 GiB +  10.4 MiB =   2.9 GiB       java (6)
    ---------------------------------
                              3.2 GiB
    =================================
    

Based on the output above, there are some more services that have been added. The noteable ones are vpxd (vCenter Server daemon) and java. Since this command only takes the binary as the name, 6 processes that are running in java are contained by the 2.9G of memory java is allocated.

## Determine the Memory Configuration and Usage per process

We can look deeper into the processes and see which one has the largest Resident Set Size (rss). <a href="http://www.commandlinefu.com/commands/view/3/display-the-top-ten-running-processes-sorted-by-memory-usage" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.commandlinefu.com/commands/view/3/display-the-top-ten-running-processes-sorted-by-memory-usage']);">This website</a> provides some commands for viewing the processes and ordering them by usage. Using one of the commands we get the following.

    localhost:~ # ps -eo rss,vsz,pid,cputime,cmd --width 100 --sort rss,vsz | tail --lines 10
    15504 168324  8769 00:00:00 postgres: vc VCDB 127.0.0.1(50889) idle
    16124 162236  4319 00:00:00 postgres: writer process
    29056 182200  8708 00:00:00 /usr/lib/openldap/slapd -h  ldap://localhost   -f /etc/openldap/slapd.co
    103444 819668 7022 00:00:02 /usr/java/jre-vmware/bin/java -Xms128m -Xmx512m -Dcom.vmware.vide.log.di
    137808 365148 8759 00:00:03 /usr/lib/vmware-vpx/vpxd
    272664 857096 9169 00:00:08 /usr/java/jre-vmware/bin/java -Dorg.tanukisoftware.wrapper.WrapperSimple
    488692 3708228 8245 00:00:20 /usr/java/jre-vmware/bin/java -Dorg.tanukisoftware.wrapper.WrapperSimpl
    508980 1766476 8946 00:00:47 /usr/java/jre-vmware/bin/java -Djava.util.logging.config.file=/usr/lib/
    853220 1605380 7634 00:01:39 /usr/java/jre-vmware/bin/java -Xmx1024m -Xms512m -XX:PermSize=128m -XX:
    869924 2884000 5652 00:00:44 /usr/java/jre-vmware/bin/java -Djava.util.logging.config.file=/usr/lib/
    

Of the processes above we can see a few things. The first few are *postgres* processes. vPostgres is the internal database for the vCenter appliance. We then see *slapd* (openLDAP deamon) which will be assisting with the AD authentication. We also see the *vpxd* (vCenter Daemon) again. These processes are not running in the java heap, so we will not be tuning them.

The other 6 processes, which correlate to the 6 we saw with the **ps_mem** command, are the ones that add up to 2.9G of memory allocation.

Let&#8217;s just make sure that the math in **ps_mem** is correct and add up the *rss* for the java processes. The *rss* is the number of pages in physical memory.

    localhost:~ # ps -eo rss,vsz,pid,cputime,cmd --width 100 --sort rss,vsz | tail --lines 10 |grep java |awk '{ SUM += $1;} END { print SUM/1024/1024 }'
    2.97867
    

All of the *rss* of the java processes add up to 2.9G, so these are the processes taking up the majority of our memory.

Just to confirm, let&#8217;s add up the processes that are not based on java and see the memory utilization.

    localhost:~ # ps -eo rss,vsz,pid,cputime,cmd --width 100 --sort rss,vsz |grep -v java |awk '{ SUM += $1;} END { print SUM/1024 }'    
    417.953
    

This comes out to 417M (notice that I removed a */1024* from the awk command to produce Megabytes instead of Gigabytes). So our base system would run 417M before the java processes.

In java, the initial memory allocation will come from the *-Xms* that we discussed above. Let&#8217;s see which processes are using more than their defined *-Xms*.

First let&#8217;s do a better job or correlating the *rss* to the service.

    localhost:~ # ps -eo rss,vsz,pid,cputime,cmd --width 200 --sort rss,vsz | tail --lines 10 |grep java |awk '{ MB = $1/1024; print MB,$3,$6,$7,$8}'
    103.223 7022 -Xms128m -Xmx512m -Dcom.vmware.vide.log.dir=/var/log/vmware/logbrowser/
    283.336 9169 -Dorg.tanukisoftware.wrapper.WrapperSimpleApp.waitForStartMain=FALSE -Dxml.config=../conf/sps-spring-config.xml -XX:+ForceTimeHighResolution
    481.582 8245 -Dorg.tanukisoftware.wrapper.WrapperSimpleApp.waitForStartMain=FALSE -Dvim.logdir=/var/log/vmware/vpx/inventoryservice/ -XX:+ForceTimeHighRes
    501.492 8946 -Djava.util.logging.config.file=/usr/lib/vmware-vpx/tomcat/conf/logging.properties -Xss1024K -Xincgc
    833.309 7634 -Xmx1024m -Xms512m -XX:PermSize=128m
    857.297 5652 -Djava.util.logging.config.file=/usr/lib/vmware-sso/conf/logging.properties -Duser.timezone=+00:00 -Dhazelcast.logging.type=log4j
    

The bottom process is Single Sign On (SSO). Let&#8217;s get the full process command.

    localhost:~ # ps -eaf |grep 5652
    ssod      5652     1  2 15:55 ?        00:00:46 /usr/java/jre-vmware/bin/java -Djava.util.logging.config.file=/usr/lib/vmware-sso/conf/logging.properties -Duser.timezone=+00:00 -Dhazelcast.logging.type=log4j -XX:MaxPermSize=256M -Xms2048m -Xmx2048m -XX:ErrorFile=/var/log/vmware/sso/sso_crash_pid%p.log -Djava.security.krb5.conf=/usr/lib/vmware-sso/webapps/ims/WEB-INF/classes/krb5-lw.conf -Dsun.security.jgss.native=true -Dsun.security.jgss.lib=/opt/likewise/lib64/libgssapi_krb5.so -Djava.util.logging.manager=com.springsource.tcserver.serviceability.logging.TcServerLogManager -Djava.endorsed.dirs=/usr/lib/vmware-sso/endorsed -classpath /usr/local/tcserver/vfabric-tc-server-standard/tomcat-7.0.25.B.RELEASE/bin/bootstrap.jar:/usr/local/tcserver/vfabric-tc-server-standard/tomcat-7.0.25.B.RELEASE/bin/tomcat-juli.jar -Dcatalina.base=/usr/lib/vmware-sso -Dcatalina.home=/usr/local/tcserver/vfabric-tc-server-standard/tomcat-7.0.25.B.RELEASE -Djava.io.tmpdir=/usr/lib/vmware-sso/temp org.apache.catalina.startup.Bootstrap start
    

Notice that the process is started by the PID &#8220;1&#8243; which is init. We also see the heap flags as follows.

*   -XX:MaxPermSize=256M
*   -Xms2048m
*   -Xmx2048m

So we have a minimum and maximum heap size of 2048M. We also have a MaxPermSize which has been increased from 64M (Default) to 256M. More information on MaxPermSize can be found <a href="http://indrayanblog.blogspot.com/2011/03/cxv.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://indrayanblog.blogspot.com/2011/03/cxv.html']);">here</a>.

Based on the *rss*, we can reduce the settings for this process a considerable amount. Let&#8217;s lower the minimum heap size of the process to 32M and restart it. We can then see how large it grows.

Edit the */usr/lib/vmware-sso/bin/setenv.sh* file and change the *-Xms* option to 32M in the following line.

    JVM_OPTS="$JVM_OPTS -XX:MaxPermSize=256M -Xms32m -Xmx2048m"
    

Now restart the service.

    localhost:/usr/lib/vmware-sso/bin # /etc/init.d/vmware-sso restart
    

Let&#8217;s find the new PID

    localhost:~ # cat /usr/lib/vmware-sso/logs/tcserver.pid
    2479
    

Now we can get the current *rss* from the service.

    localhost:~ # ps -o rss,vsz,pid,cputime,cmd --width 200 --sort rss,vsz -p 2479 |awk '{ MB = $1/1024; print MB}'
    422.766
    

So the *rss* is now down to 422M for this process. With load the memory pages will vary, but this is likely the minimum we will be able to run with. Using this procedure you can go back and check each service to check the minimum. I would advise checking it under load to see what is an optimum setting for your environment.

## Changing the Default Heap Allocation

Now that we know the new values for our environment, we can go ahead and set them. Below I have listed the places to change the values and what I put in my environment. My environment only uses the most basic services, so these numbers are likely lower than you will get.

### Active VMware Services using Java

#### VMware SSO Service

*/usr/lib/vmware-sso/bin/setenv.sh*

*   -XX:MaxPermSize=128M
*   -Xms256m
*   -Xmx1024m

#### VMware Inventory Service

This is with 2 hosts and only 20 VMs. More VMs will require more memory for the inventory service

*/usr/lib/vmware-vpx/inventoryservice/wrapper/conf/wrapper.conf*

*   wrapper.java.initmemory=64
*   wrapper.java.maxmemory=512

#### VMware vCenter Service

*/etc/vmware-vpx/tomcat-java-opts.cfg*

*   -Xmx256m
*   -XX:MaxPermSize=128m 

*/usr/lib/vmware-vpx/tomcat/bin/setenv.sh*

Leave the options as is, unless you want to lower the Xss (Thread Stack Size) than 1M

*/usr/lib/vmware-vpx/sps/wrapper/conf/wrapper.conf*

*   wrapper.java.initmemory=64
*   wrapper.java.maxmemory=128

#### Log Browser

*/etc/init.d/vmware-logbrowser*

*   -Xms64m 
*   -Xmx128m

#### vSphere Web Client

*/usr/lib/vmware-vsphere-client/server/bin/dmk.sh*

*   -Xmx512m
*   -Xms128m
*   -XX:PermSize=64m
*   -XX:MaxPermSize=128m 

### Final Memory Consumption

The final memory consumption is much lower than it was previously. By changing the minimum and maximum heap sizes we can reduce the memory footprint. Here is the output from the **free** command after the changes.

    localhost:~ # free -m
                 total       used       free     shared    buffers     cached
    Mem:          8002       3803       4199          0         32       1332
    -/+ buffers/cache:       2437       5564
    Swap:        15366          0      15366
    

We are now using 2.4G of memory for the system instead of 3.2G before

    localhost:~ # python ps_mem.py |tail -n 15
      2.4 MiB + 161.5 KiB =   2.6 MiB       vmtoolsd
      2.4 MiB + 271.5 KiB =   2.6 MiB       hald
      1.8 MiB + 917.5 KiB =   2.7 MiB       vami-sfcbd (7)
      1.8 MiB +   1.4 MiB =   3.2 MiB       sendmail (3)
      2.6 MiB + 681.0 KiB =   3.3 MiB       sshd (2)
      2.5 MiB + 943.0 KiB =   3.4 MiB       lsassd
      4.2 MiB +  12.0 KiB =   4.2 MiB       haveged
      4.3 MiB + 635.5 KiB =   4.9 MiB       python2.6
     28.5 MiB + 162.5 KiB =  28.6 MiB       slapd
     34.2 MiB +   9.2 MiB =  43.4 MiB       postmaster (21)
    132.8 MiB + 350.5 KiB = 133.2 MiB       vpxd
      2.1 GiB +  10.3 MiB =   2.1 GiB       java (6)
    ---------------------------------
                              2.4 GiB
    =================================
    

The java services have been lowered from 2.9G to 2.1G. The biggest change is on the maximum amount of memory. Instead of being able to take 8G we are now down much lower. If we add up the numbers we put in for the maximum heap sizes and MaxPermSizes we get 2688M. So the java heaps should run under 3G of memory. That added with our 512M of system processes, we should be able to run comfortably at 4GB with out any swapping. You can now lower the amount of memory on the vCenter Appliance in the vSphere Client.

## Stopping Unused Processes

Since these are lab vCenters, I do not need all of the processes to run on them. We will stop some of these services from starting at boot.

Let&#8217;s list the services.

    vc:~ # chkconfig
    ...
    vmware-inventoryservice  on
    vmware-logbrowser        on
    vmware-netdumper         on
    vmware-rbd-watchdog      off
    vmware-sps               off
    vmware-sso               on
    vmware-tools-services    on
    vmware-vpostgres         on
    vmware-vpxd              on
    vsock                    on
    vsphere-client           on
    

I still use the thick client for most operations, so I am going to disable the vsphere-client service.

    vc:~ # chkconfig vsphere-client off
    

I am not going to be use the <a href="http://kb.vmware.com/kb/2032888" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2032888']);">Log Browser</a> or the <a href="http://kb.vmware.com/kb/1032051" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1032051']);">Netdumper</a> services.

    vc:~ # chkconfig vmware-logbrowser off
    vc:~ # chkconfig vmware-netdumper off
    

Let&#8217;s stop those services.

    vc:~ # service vsphere-client stop
    vc:~ # service vmware-logbrowser stop
    vc:~ # service vmware-netdumper stop
    

Now we can check the memory on the appliance using the **free** command again.

    vc:~ # free -m
                 total       used       free     shared    buffers     cached
    Mem:          3962       2528       1433          0         27        782
    -/+ buffers/cache:       1718       2244
    Swap:        15366          0      15366
    

We are down to 1.7G utilization on this server. I have 2 hosts and 15 VMs attached to this vCenter Appliance. I have lowered the RAM to 3G and it works great. </size>

