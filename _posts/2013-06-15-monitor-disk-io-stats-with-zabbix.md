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

*   [Monitor a device performance on Linux with Zabbix](http://romain.novalan.fr/wiki/Monitor_a_device_performance_on_Linux_with_Zabbix)
*   [Getting hard disk performance stats from zabbix](http://www.muck.net/19/getting-hard-disk-performance-stats-from-zabbix)

Both use the same technique of querying the **/proc/diskstats** file and plotting that information. So let's start setting that up.

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


All of that looks good. At this point the above links just create a graph for each disk separately and plot the above data. I had different types and number of disks on each machine, so I didn't want to create a graph per device.

## Zabbix AutoDiscovery

Zabbix has call feature called Discovery, where it can discover devices for you. I ran into this forum:

*   [Linux Autodiscovery : services, processes, hard disks](https://www.zabbix.com/forum/showthread.php?p=104719#post104719)

It had examples of how to discover services, process and lastly hard disks (which is what I was looking for). The above forum had a Perl script that output VM Name and it's corresponding disks. I edited the file so it just showed disks. I put the script under **/usr/local/bin** and I made sure zabbix could execute the script:

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

I didn't want disk statistics per partition but per disk, so let's add a rule to just catch the disk without the partitions. Login to zabbix and then go to "Administration" -> General -> "Regular Expression":

![zabbiz reg expression g Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbiz_reg_expression_g.png)

Then click "Create New Regular Expression" and under "Expressions", click "New" and add the following:

![zabbiz reg expression create Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbiz_reg_expression_create.png)

Save that and on the left side, name the Regular Expression and do a test to make sure it works:

![zabbiz reg expression test Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbiz_reg_expression_test.png)

and also put in a partition to make sure it fails:

![zabbiz reg expression test fail Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbiz_reg_expression_test_fail.png)

Save that and if you go back to the regular expression list you will see yours there:

![zabbiz reg expression list Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbiz_reg_expression_list.png)

### Create a New Template in Zabbix

Let's create a new template for our items and graphs. Go to "Configuration" -> "Template" -> "Create Template". Fill out the information and add your hosts to the template:

![zabbix create template Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_create_template.png)

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

Go to "Configuration" -> "Templates":

![zabbix templates Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_templates.png)

Scroll down and you will see the template that you created earlier. Click on "Discovery" -> "Create Discovery Rule". Here we will name the rule, query the *UserParameter* we created, and apply a filter (regular expression) to get just the disk. Here is how my configuration looked like:

![zabbix discovery rule Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_discovery_rule.png)

Save that and if you go back to the discovery rules you will see the following:

![zabbix discovery rule list Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_discovery_rule_list.png)

### Add Item Prototypes to Discovery Rule

Go to "Configuration" -> "Templates" -> Template_Linux_Disk -> "Discovery" -> "Item Prototypes" -> "Create Item Prototype". Fill out the information. Here is my latency item:

![zab item prototype later Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zab-item-prototype-later.png)

I added both read and write latency. Here is my Disk Rate in Bps:

![zab item prototype after dr Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zab-item-prototype-after-dr.png)

I added both read and write disk rates. I also added disk operations (read and write). I ended up defining 6 items in total, here is the list:

![zabbix itemprototypes list Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_itemprototypes_list.png)

### Create Graph Prototypes to Plot the Above Items

Go to "Configuration" -> "Templates" -> Template_Linux_Disk -> "Discovery" -> "Graph Prototypes" -> "Create Graph Prototype". Add both read and write like so:

![zabbix graphprototypes latency Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_graphprototypes_latency.png)

Using the same technique I created 3 graph prototypes:

![zabbix graphprototypes list Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_graphprototypes_list.png)

## Check out the Graphs

Go to "Monitoring" -> "Graphs". Then pick a host and make sure only it's corresponding disks show. For example here is what I saw for my Fedora Box which had an LVM setup:

![zabbix graph lists fedora g Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_graph_lists_fedora_g.png)

and here is one graph:

![zabbix disk rate fedora Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_disk_rate_fedora.png)

And here are the available graphs for my Ubuntu which just had one drive in it:

![zabbix graph lists ub g Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_graph_lists_ub_g.png)

and here is latency for the disk:

![zabbix disk latency ubuntu Monitor Disk IO Stats with Zabbix](https://github.com/elatov/uploads/raw/master/2013/06/zabbix_disk_latency_ubuntu.png)

Everything looked perfect.

