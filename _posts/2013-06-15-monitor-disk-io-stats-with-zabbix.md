---
title: Monitor Disk IO Stats with Zabbix
author: Karim Elatov
layout: post
permalink: /2013/06/monitor-disk-io-stats-with-zabbix/
dsq_thread_id:
  - 
categories:
  - Home Lab
  - OS
  - Storage
tags:
  - /proc/diskstats
  - Monitoring
  - Zabbix
---
I wanted to get a feel how much IO my machines are doing each day. As I was going through the **zabbix** graphs I noticed that IO statistics are not included. I did some research and I came across these forums:

*   <a href="http://romain.novalan.fr/wiki/Monitor_a_device_performance_on_Linux_with_Zabbix" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://romain.novalan.fr/wiki/Monitor_a_device_performance_on_Linux_with_Zabbix']);">Monitor a device performance on Linux with Zabbix</a> 
*   <a href="http://www.muck.net/19/getting-hard-disk-performance-stats-from-zabbix" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.muck.net/19/getting-hard-disk-performance-stats-from-zabbix']);">Getting hard disk performance stats from zabbix</a>

Both use the same technique of querying the **/proc/diskstats** file and plotting that information. So let&#8217;s start setting that up.

### Create UserParameters in Zabbix to Query */proc/diskstats*

Both of the above links used the following UserParameters:

    UserParameter=custom.vfs.dev.read.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$4}'
    UserParameter=custom.vfs.dev.read.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$7}'
    UserParameter=custom.vfs.dev.write.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$8}'
    UserParameter=custom.vfs.dev.write.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$11}'
    UserParameter=custom.vfs.dev.io.active[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$12}'
    UserParameter=custom.vfs.dev.io.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$13}'
    UserParameter=custom.vfs.dev.read.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$6}'
    UserParameter=custom.vfs.dev.write.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$10}'
    

Add those to your **/etc/zabbix/zabbix_agentd.conf** file. Here is how my file looked like:

    kerch:~>tail /etc/zabbix/zabbix_agentd.conf
    
    UserParameter=custom.vfs.dev.read.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$4}'
    UserParameter=custom.vfs.dev.read.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$7}'
    UserParameter=custom.vfs.dev.write.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$8}'
    UserParameter=custom.vfs.dev.write.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$11}'
    UserParameter=custom.vfs.dev.io.active[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$12}'
    UserParameter=custom.vfs.dev.io.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$13}'
    UserParameter=custom.vfs.dev.read.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$6}'
    UserParameter=custom.vfs.dev.write.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$10}'
    

Then go ahead and restart the **zabbix-agent** service:

    kerch:~>sudo service zabbix-agent restart
    zabbix-agent stop/waiting
    zabbix-agent start/running, process 26720
    

At this point you can query disk information. To make sure all of them work fine run the following:

    kerch:~$ for i in $(grep '^UserParameter' /etc/zabbix/zabbix_agentd.conf | cut -d = -f 2 | cut -d [ -f 1); do echo $i; zabbix_get -s 192.168.1.100 -p 10050 -k "$i[sda]"; done
    custom.vfs.dev.read.ops
    93292
    custom.vfs.dev.read.ms
    1214540
    custom.vfs.dev.write.ops
    3328812
    custom.vfs.dev.write.ms
    480210476
    custom.vfs.dev.io.active
    2
    custom.vfs.dev.io.ms
    42178164
    custom.vfs.dev.read.sectors
    2968840
    custom.vfs.dev.write.sectors
    161623584
    

All of that looks good. At this point the above links just create a graph for each disk separately and plot the above data. I had different types and number of disks on each machine, so I didn&#8217;t want to create a graph per device.

## Zabbix AutoDiscovery

Zabbix has call feature called Discovery, where it can discover devices for you. I ran into this forum:

*   <a href="https://www.zabbix.com/forum/showthread.php?p=104719#post104719" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/forum/showthread.php?p=104719#post104719']);">Linux Autodiscovery : services, processes, hard disks</a>

It had examples of how to discover services, process and lastly hard disks (which is what I was looking for). The above forum had a Perl script that output VM Name and it&#8217;s corresponding disks. I edited the file so it just showed disks. I put the script under **/usr/local/bin** and I made sure zabbix could execute the script:

    kerch:~>ls -l /usr/local/bin/discover_disk.pl 
    -rwxr-x--- 1 elatov zabbix 498 Jun  2 15:57 /usr/local/bin/discover_disk.pl
    

After all of that was done, here is how the output looked like:

    kerch:~>/usr/local/bin/discover_disk.pl 
    {
        "data":[
    
        ,
        {
            "{#DISK}":"loop1",
        }
        ,
        {
            "{#DISK}":"sda",
        }
        ,
        {
            "{#DISK}":"sda1",
        }
        ,
        {
            "{#DISK}":"sda2",
        }
        ,
        {
            "{#DISK}":"sda3",
        }
        ,
        {
            "{#DISK}":"sda4",
        }
        ,
        {
            "{#DISK}":"sr0",
        }
    
        ]
    }
    

It spit out the partitions as well, I left it that way in case I might use them later.

### Create a Regular Expression in Zabbix

I didn&#8217;t want disk statistics per partition but per disk, so let&#8217;s add a rule to just catch the disk without the partitions. Login to zabbix and then go to &#8220;Administration&#8221; -> General -> &#8220;Regular Expression&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_g.png" alt="zabbiz reg expression g Monitor Disk IO Stats with Zabbix" width="1167" height="419" class="alignnone size-full wp-image-8934" title="Monitor Disk IO Stats with Zabbix" /></a>

Then click &#8220;Create New Regular Expression&#8221; and under &#8220;Expressions&#8221;, click &#8220;New&#8221; and add the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_create.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_create.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_create.png" alt="zabbiz reg expression create Monitor Disk IO Stats with Zabbix" width="513" height="133" class="alignnone size-full wp-image-8935" title="Monitor Disk IO Stats with Zabbix" /></a>

Save that and on the left side, name the Regular Expression and do a test to make sure it works:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test.png" alt="zabbiz reg expression test Monitor Disk IO Stats with Zabbix" width="973" height="251" class="alignnone size-full wp-image-8936" title="Monitor Disk IO Stats with Zabbix" /></a>

and also put in a partition to make sure it fails:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test_fail.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test_fail.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_test_fail.png" alt="zabbiz reg expression test fail Monitor Disk IO Stats with Zabbix" width="970" height="244" class="alignnone size-full wp-image-8937" title="Monitor Disk IO Stats with Zabbix" /></a>

Save that and if you go back to the regular expression list you will see yours there:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_list.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_list.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbiz_reg_expression_list.png" alt="zabbiz reg expression list Monitor Disk IO Stats with Zabbix" width="907" height="216" class="alignnone size-full wp-image-8939" title="Monitor Disk IO Stats with Zabbix" /></a>

### Create a New Template in Zabbix

Let&#8217;s create a new template for our items and graphs. Go to &#8220;Configuration&#8221; -> &#8220;Template&#8221; -> &#8220;Create Template&#8221;. Fill out the information and add your hosts to the template:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_create_template.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_create_template.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_create_template.png" alt="zabbix create template Monitor Disk IO Stats with Zabbix" width="939" height="383" class="alignnone size-full wp-image-8940" title="Monitor Disk IO Stats with Zabbix" /></a>

### Create a new UserParameter for Disk Discovery

Add the following into **/etc/zabbix/zabbix_agentd.conf**:

    kerch:~>tail -1 /etc/zabbix/zabbix_agentd.conf
    UserParameter=custom.disks.discovery_perl,/usr/local/bin/discover_disk.pl
    

Restart the agent one more time:

    kerch:~>sudo service zabbix-agent restart
    zabbix-agent stop/waiting
    zabbix-agent start/running, process 29357
    

Lastly make sure, we get the our disks from this User parameter:

    kerch:~>zabbix_get -s 192.168.1.100 -k custom.disks.discovery_perl              {
        "data":[
    
        ,
        {
            "{#DISK}":"ram0",
        }
        ,
        {
            "{#DISK}":"ram1",
    

The list kept going, but we now know that works.

### Create a Zabbix Discovery Rule

Go to &#8220;Configuration&#8221; -> &#8220;Templates&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_templates.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_templates.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_templates.png" alt="zabbix templates Monitor Disk IO Stats with Zabbix" width="1351" height="235" class="alignnone size-full wp-image-8941" title="Monitor Disk IO Stats with Zabbix" /></a>

Scroll down and you will see the template that you created earlier. Click on &#8220;Discovery&#8221; -> &#8220;Create Discovery Rule&#8221;. Here we will name the rule, query the *UserParameter* we created, and apply a filter (regular expression) to get just the disk. Here is how my configuration looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule.png" alt="zabbix discovery rule Monitor Disk IO Stats with Zabbix" width="680" height="442" class="alignnone size-full wp-image-8942" title="Monitor Disk IO Stats with Zabbix" /></a>

Save that and if you go back to the discovery rules you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule_list.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule_list.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_discovery_rule_list.png" alt="zabbix discovery rule list Monitor Disk IO Stats with Zabbix" width="1365" height="171" class="alignnone size-full wp-image-8943" title="Monitor Disk IO Stats with Zabbix" /></a>

### Add Item Prototypes to Discovery Rule

Go to &#8220;Configuration&#8221; -> &#8220;Templates&#8221; -> Template\_Linux\_Disk -> &#8220;Discovery&#8221; -> &#8220;Item Prototypes&#8221; -> &#8220;Create Item Prototype&#8221;. Fill out the information. Here is my latency item:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-later.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-later.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-later.png" alt="zab item prototype later Monitor Disk IO Stats with Zabbix" width="558" height="370" class="alignnone size-full wp-image-10411" title="Monitor Disk IO Stats with Zabbix" /></a>

I added both read and write latency. Here is my Disk Rate in Bps:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-after-dr.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-after-dr.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zab-item-prototype-after-dr.png" alt="zab item prototype after dr Monitor Disk IO Stats with Zabbix" width="565" height="360" class="alignnone size-full wp-image-10413" title="Monitor Disk IO Stats with Zabbix" /></a>

I added both read and write disk rates. I also added disk operations (read and write). I ended up defining 6 items in total, here is the list:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_itemprototypes_list.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_itemprototypes_list.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_itemprototypes_list.png" alt="zabbix itemprototypes list Monitor Disk IO Stats with Zabbix" width="1224" height="328" class="alignnone size-full wp-image-8946" title="Monitor Disk IO Stats with Zabbix" /></a>

### Create Graph Prototypes to Plot the Above Items

Go to &#8220;Configuration&#8221; -> &#8220;Templates&#8221; -> Template\_Linux\_Disk -> &#8220;Discovery&#8221; -> &#8220;Graph Prototypes&#8221; -> &#8220;Create Graph Prototype&#8221;. Add both read and write like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_latency.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_latency.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_latency.png" alt="zabbix graphprototypes latency Monitor Disk IO Stats with Zabbix" width="1131" height="561" class="alignnone size-full wp-image-8947" title="Monitor Disk IO Stats with Zabbix" /></a>

Using the same technique I created 3 graph prototypes:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_list.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_list.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graphprototypes_list.png" alt="zabbix graphprototypes list Monitor Disk IO Stats with Zabbix" width="1179" height="245" class="alignnone size-full wp-image-8948" title="Monitor Disk IO Stats with Zabbix" /></a>

## Check out the Graphs

Go to &#8220;Monitoring&#8221; -> &#8220;Graphs&#8221;. Then pick a host and make sure only it&#8217;s corresponding disks show. For example here is what I saw for my Fedora Box which had an LVM setup:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_fedora_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_fedora_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_fedora_g.png" alt="zabbix graph lists fedora g Monitor Disk IO Stats with Zabbix" width="441" height="202" class="alignnone size-full wp-image-8949" title="Monitor Disk IO Stats with Zabbix" /></a>

and here is one graph:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_rate_fedora.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_rate_fedora.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_rate_fedora.png" alt="zabbix disk rate fedora Monitor Disk IO Stats with Zabbix" width="1382" height="612" class="alignnone size-full wp-image-8950" title="Monitor Disk IO Stats with Zabbix" /></a>

And here are the available graphs for my Ubuntu which just had one drive in it:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_ub_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_ub_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_graph_lists_ub_g.png" alt="zabbix graph lists ub g Monitor Disk IO Stats with Zabbix" width="422" height="133" class="alignnone size-full wp-image-8951" title="Monitor Disk IO Stats with Zabbix" /></a>

and here is latency for the disk:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_latency_ubuntu.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_latency_ubuntu.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/zabbix_disk_latency_ubuntu.png" alt="zabbix disk latency ubuntu Monitor Disk IO Stats with Zabbix" width="1378" height="561" class="alignnone size-full wp-image-8952" title="Monitor Disk IO Stats with Zabbix" /></a>

Everything looked perfect.

