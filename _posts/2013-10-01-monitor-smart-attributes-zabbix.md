---
title: Monitor SMART Attributes with Zabbix
author: Karim Elatov
layout: post
permalink: /2013/10/monitor-smart-attributes-zabbix/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1815259739
categories:
  - OS
  - VMware
tags:
  - pogoplug
  - smartmontools
  - Zabbix
---
In my previous post I setup my pogoplug device as a backup server. Since it was holding somewhat important information, I wanted to monitor the disk that I plugged into the pogoplug device to make sure it't not failing. This is where the **smartmontools** software comes into play. With the **smartmontools** package there comes a utility called **smartctl**, which allows you to query the SMART attributes of the hard drive (if the drive supports it).

### Compile Zabbix Agentd on Pogoplug

Before I checked the SMART attributes, I had to make sure that I was able to run the *zabbix* agent on the device. I ran into a post entitled "<a href="http://weblog.aklmedia.nl/2011/05/install-zabbix-agent-on-synology/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://weblog.aklmedia.nl/2011/05/install-zabbix-agent-on-synology/']);">Install Zabbix Agent on Synology</a>" and it seems that it was possible. Following the instructions laid out in that post, here is what I did to compile *zabbix* on the pogoplug device. First install the prerequisites packages that will be necessary to perform the compile:

    $ ipkg install gcc make bison flex gconv-modules
    

Next create a symlink to **/opt/include** under **/usr**. If you don't do this, the *configure* script won't be able to find the **iconv.h** header file. Here are the commands to accomplish that:

    $ cd /usr
    $ ln -s /opt/include
    

After that let's download the source for zabbix:

    $ cd /opt/tmp
    $ wget http://downloads.sourceforge.net/.../zabbix-2.0.8.tar.gz
    

Now let's extract the source:

    $ tar xzf zabbix-2.0.8.tar.gz
    

Next **configure** the source:

    $ cd zabbix-2.0.8
    $ ./configure --enable-agent --prefix=/opt/zabbix
    

After that is done, compile and install the package:

    make
    make install
    

That's actually it, now you have *zabbix* agentd installed under **/opt/zabbix**.

### Configure Zabbix Agentd on Pogoplug

Now that it's installed let's make sure we can start it. First edit the **/opt/zabbix/zabbix_agentd.conf** file and add/modify the following parameters:

    pogo:~# grep -vE '^$|^#' /opt/zabbix/etc/zabbix_agentd.conf
    PidFile=/opt/var/run/zabbix_agentd.pid
    LogFile=/opt/var/log/zabbix_agentd.log
    Server=192.168.1.XX
    ListenIP=192.168.1.XX
    StartAgents=1
    Hostname=pogo.dnsd.me
    AllowRoot=1
    

If you don't want to run the application as **root** you can add the **zabbix** user and allow him to write under the **/opt/var/run** and **/opt/var/log** directories. This wasn't really meant to be a multi-user platform, so I decided not to go down that route. Plus down the line I needed to allow the user that is running zabbix to be able to execute the **smartctl** command. On regular systems you can do that with **sudo**, but I didn't want to install that. Running **sudo** requires the **suid** bit set, which means I would have to mount the filesystem with the **suid** flag, by default it's mounted with the **nosuid** flag. Call me lazy, but I just didn't feel like it was worth the trouble.

After the config is in place, run the following:

    $ /opt/zabbix/sbin/zabbix_agentd -c /opt/zabbix/etc/zabbix_agentd.conf  
    

The process should start up. You can check using **ps**:

    pogo:~# ps | grep zabb
    16100 zabbix    2936 S    /opt/zabbix/sbin/zabbix_agentd -c /opt/zabbix/etc/za
    16101 zabbix    2936 S    /opt/zabbix/sbin/zabbix_agentd -c /opt/zabbix/etc/za
    16102 zabbix    2936 S    /opt/zabbix/sbin/zabbix_agentd -c /opt/zabbix/etc/za
    

You can also confirm it's listening on 10050 with netstat:

    pogo:~# netstat -antp | grep zabb
    tcp        0      0 192.168.1.104:10050     0.0.0.0:*               LISTEN      16100/zabbix_agentd
    

The last thing to do is to setup an *init* script. I just copied the **dropbear** start-up script and modified it to fit my needs:

    $ cp /etc/init.d/dropbear.sh /opt/etc/init.d/zabbix-agentd
    $ vi /opt/etc/init.d/zabbix-agentd
    

I really didn't change much, but just for reference <a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix-agentd.sh" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix-agentd.sh']);">here</a> is the script. Lastly to make sure it starts automatically on boot up, add it to the **/etc/init.d/rcS** file:

    /opt/etc/init.d/zabbix-agentd start
    

You can check to make sure *zabbix* agentd starts up without issues by rebooting the pogoplug device.

### Add Swap to Pogoplug

As soon as you add the device to your zabbix server you will get warning about the device missing swap space, so let's add that. We will need the **mkswap** command to format our file as swap, so let's install that first. That utility is part of the **util-linux** package:

    $ ipkg install util-linux
    

After it's installed, let's create the directory where we will store the swap file:

    $ mkdir /opt/etc/swap
    

Now let's create a 256MB file:

    $ dd if=/dev/zero of=/opt/etc/swap/swapfile.img bs=1M count=256
    

Now let's format the file as swap:

    $ /opt/sbin/mkswap /opt/etc/swap/swapfile.img
    

Lastly enable the swap file:

    $ swapon /opt/etc/swap/swapfile.img
    

You can confirm with the free command that the swap file is utilized:

    pogo:~# free -m
                 total       used       free     shared    buffers     cached
    Mem:           115        109          6          0         35         46
    -/+ buffers/cache:         26         88
    Swap:          255          0        255
    

BTW the **free** command comes from the **procps** package. The last thing to do is to enable swap on boot, so edit the **/etc/init.d/rcS** file and add the following to it:

    /sbin/swapon /opt/etc/swap/swapfile.img
    

Reboot the device to make sure swap is added upon boot up.

### Configure Zabbix Agent to Pull SMART Attributes from a Hard Drive

There is a really good guide from **zabbix** on how to set it up: <a href="https://www.zabbix.com/wiki/howto/monitor/os/linux/smart" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.zabbix.com/wiki/howto/monitor/os/linux/smart']);">S.M.A.R.T. HDD Monitoring with Zabbix</a>. Here is the jist of the setup. First create a script that will grab values depending on the drive and attribute that you pass in to it. Here is the script:

    $ cat /usr/local/bin/getsv
    #!/bin/bash
    if [ $# -ne 2 ];
    then
    echo "Usage: $0 <device> <parameter>"
    exit
    fi
    
    sudo smartctl -A $1 | grep $2 | tr -s ' ' | sed "s/^[[:space:]]*\(.*\)[[:space:]]*$/\1/" | cut -d " " -f 10
    

If **smartmontools** are not installed, go ahead and install it:

    $ sudo yum install smartmontools
    

Confirm your drive returns SMART attributes:

    $ sudo smartctl -A /dev/sda
    smartctl 6.0 2012-10-10 r3643 [i686-linux-3.11.1-200.fc19.i686] (local build)
    Copyright (C) 2002-12, Bruce Allen, Christian Franke, www.smartmontools.org
    
    === START OF READ SMART DATA SECTION ===
    SMART Attributes Data Structure revision number: 16
    Vendor Specific SMART Attributes with Thresholds:
    ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
      3 Spin_Up_Time            0x0027   182   182   063    Pre-fail  Always       -       24757
      4 Start_Stop_Count        0x0032   253   253   000    Old_age   Always       -       235
      5 Reallocated_Sector_Ct   0x0033   253   253   063    Pre-fail  Always       -       0
      6 Read_Channel_Margin     0x0001   253   253   100    Pre-fail  Offline      -       0
      7 Seek_Error_Rate         0x000a   253   252   000    Old_age   Always       -       0
      8 Seek_Time_Performance   0x0027   244   233   187    Pre-fail  Always       -       55830
      9 Power_On_Minutes        0x0032   136   136   000    Old_age   Always       -       260h+36m
     10 Spin_Retry_Count        0x002b   253   252   157    Pre-fail  Always       -       0
     11 Calibration_Retry_Count 0x002b   253   252   223    Pre-fail  Always       -       0
     12 Power_Cycle_Count       0x0032   252   252   000    Old_age   Always       -       469
    192 Power-Off_Retract_Count 0x0032   253   253   000    Old_age   Always       -       0
    193 Load_Cycle_Count        0x0032   253   253   000    Old_age   Always       -       0
    194 Temperature_Celsius     0x0032   040   253   000    Old_age   Always       -       44
    195 Hardware_ECC_Recovered  0x000a   253   252   000    Old_age   Always       -       5848
    196 Reallocated_Event_Count 0x0008   253   253   000    Old_age   Offline      -       0
    197 Current_Pending_Sector  0x0008   253   253   000    Old_age   Offline      -       0
    198 Offline_Uncorrectable   0x0008   253   253   000    Old_age   Offline      -       0
    199 UDMA_CRC_Error_Count    0x0008   144   001   000    Old_age   Offline      -       406
    200 Multi_Zone_Error_Rate   0x000a   253   252   000    Old_age   Always       -       0
    201 Soft_Read_Error_Rate    0x000a   253   252   000    Old_age   Always       -       0
    202 Data_Address_Mark_Errs  0x000a   253   252   000    Old_age   Always       -       0
    203 Run_Out_Cancel          0x000b   253   252   180    Pre-fail  Always       -       0
    204 Soft_ECC_Correction     0x000a   253   252   000    Old_age   Always       -       0
    205 Thermal_Asperity_Rate   0x000a   253   252   000    Old_age   Always       -       0
    207 Spin_High_Current       0x002a   253   252   000    Old_age   Always       -       0
    208 Spin_Buzz               0x002a   253   252   000    Old_age   Always       -       0
    209 Offline_Seek_Performnce 0x0024   242   242   000    Old_age   Offline      -       142
    210 Unknown_Attribute       0x0032   253   252   000    Old_age   Always       -       0
    211 Unknown_Attribute       0x0032   253   252   000    Old_age   Always       -       0
    212 Unknown_Attribute       0x0032   253   252   000    Old_age   Always       -       0
    

Next allow the **zabbix** user to execute **smartctl** with **sudo** without a password. Run the following command:

    $ sudo visudo
    

and add/modify the following in the **/etc/sudoers** file:

    #Defaults    requiretty
    zabbix  ALL= NOPASSWD: /usr/sbin/smartctl
    

Then run the command manually to make sure it works:

    $ sudo su - zabbix -s /bin/bash -c '/usr/local/bin/getsv /dev/sda Temperature_Celsius'
    46
    

That looks good. Now let' add the corresponding **UserParameter** scripts to the *agentd* configuration (I just chose two, but you can pick any attribute you desire, <a href="http://www.argotronic.com/en/smart.php" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.argotronic.com/en/smart.php']);">this</a> site talks about what all the different values are). Edit the **/etc/zabbix/zabbix_agentd.conf** file and add the following to it:

    $ tail -3 /etc/zabbix_agentd.conf
    UserParameter=smart.temp[*],/usr/local/bin/getsv /dev/$1 Temperature_Celsius
    UserParameter=smart.reallocated_sec_cnt[*],/usr/local/bin/getsv /dev/$1 Reallocated_Sector_Ct
    UserParameter=custom.disks.discovery_perl2,/usr/local/bin/discover_disk.pl
    

I will follow my previous post (<a href="http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/']);">Monitor Disk IO Stats with Zabbix</a>) to setup auto-discovery of the disks and then plot the values from the discovered values. To apply the above **UserParameters**, restart the **zabbix** agentd process and try the query the above values from the Zabbix Server. So on the client run the following:

    $ sudo service zabbix-agent restart
    Redirecting to /bin/systemctl restart  zabbix-agent.service
    

Then on the Zabbix server run the following:

    $ zabbix_get -s 192.168.1.102 -k smart.temp[sda]
    44
    

If the value is returned then it's all good. At this point you can follow my previous <a href="http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/06/monitor-disk-io-stats-with-zabbix/']);">post</a> to add the following to the zabbix front end:

*   Regular Expression (we only want /dev/sd\* or /dev/hd\*, in my previous post I also grabbed sd-cards /dev/mmcblk1)
*   Template
*   Discovery Rule (here add the custom.disks.discovery_perl2 as the key since you can't have duplicates)
*   Item Prototypes (for both the temperature and reallocated sector count)
*   Graph Prototype (only for the temperature)
*   Trigger Prototype (only for the smart.reallocated\_sec\_cnt)

### Add a Trigger Prototype to a Zabbix Discovery Rule

The only new thing that I added was the trigger prototype. The **Reallocated\_Sector\_Ct** attribute should be zero all the time unless the drive is failing. So rather than plotting a graph full of zeroes, I decided to add a trigger which will send a warning message if the value is bigger than 0. To do this from the Zabbix Front End go to "Templates" -> Select the Template you had created -> "Discovery Rules" -> Click on the Discovery Rule you had created -> "Trigger prototypes" -> "Create trigger prototype" and then configure it like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_trigger_prototype.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_trigger_prototype.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_trigger_prototype.png" alt="zabbix trigger prototype Monitor SMART Attributes with Zabbix" width="724" height="422" class="alignnone size-full wp-image-9558" title="Monitor SMART Attributes with Zabbix" /></a>

Now we will get notified if that value is above zero.

### Install Smartmontools on Pogoplug

There is a prebuilt **smartmontools** package:

    pogo:~# ipkg list | grep smart
    smartmontools - 5.40-3 - Utility programs to control and monitor (SMART) built into most modern ATA and SCSI hard disks.
    

But when I tried to run it, it would **seg fault**. I ran into another post with the name of: <a href="http://banzhaf.homeip.net/mediawiki/index.php/Projekt_Qnap" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://banzhaf.homeip.net/mediawiki/index.php/Projekt_Qnap']);">History of my QNAP TS-419PII</a>. Following the instructions laid out in that post, I was able to compile **smartmontools** on pogoplug. Here are the commands I ran to accomplish that. First download the latest version:

    $ cd /opt/tmp
    $ wget http://downloads.sourceforge.net/..../smartmontools-6.2.tar.gz
    

Then I extract the source:

    $ tar xvzf smartmontools-6.2.tar.gz
    

Next I configured the source:

    $ cd smartmontools-6.2
    $ ./configure CXXFLAGS='-g -O2 -fno-toplevel-reorder -Wall -W' --prefix=/opt/smart
    

Lastly I compiled and installed the software:

    $ make
    $ make install
    

The install went through without a hitch. Next I needed to check to make sure I could get the attributes. I had to specify the **-d sat** to get it to work. Here is how it looked like:

    pogo:~# /opt/smart/sbin/smartctl -d sat -A /dev/sda
    smartctl 6.2 2013-07-26 r3841 [armv5tel-linux-2.6.31.8] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
    
    === START OF READ SMART DATA SECTION ===
    SMART Attributes Data Structure revision number: 10
    Vendor Specific SMART Attributes with Thresholds:
    ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
      1 Raw_Read_Error_Rate     0x000f   100   253   006    Pre-fail  Always       -       0
      3 Spin_Up_Time            0x0003   098   097   000    Pre-fail  Always       -       0
      4 Start_Stop_Count        0x0032   099   099   020    Old_age   Always       -       1431
      5 Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Always       -       0
      7 Seek_Error_Rate         0x000f   075   060   030    Pre-fail  Always       -       41254693
      9 Power_On_Hours          0x0032   096   096   000    Old_age   Always       -       4017
     10 Spin_Retry_Count        0x0013   100   069   034    Pre-fail  Always       -       0
     12 Power_Cycle_Count       0x0032   099   099   020    Old_age   Always       -       1392
    187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
    189 High_Fly_Writes         0x003a   100   100   000    Old_age   Always       -       0
    190 Airflow_Temperature_Cel 0x0022   065   052   045    Old_age   Always       -       35 (Min/Max 35/48)
    192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       72
    193 Load_Cycle_Count        0x0032   041   041   000    Old_age   Always       -       118819
    194 Temperature_Celsius     0x0022   035   048   000    Old_age   Always       -       35 (0 12 0 0 0)
    195 Hardware_ECC_Recovered  0x001a   056   047   000    Old_age   Always       -       27286480
    197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
    198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
    199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0
    200 Multi_Zone_Error_Rate   0x0000   100   253   000    Old_age   Offline      -       0
    202 Data_Address_Mark_Errs  0x0032   100   253   000    Old_age   Always       -       0
    

Most of the other OSes had a script to start the **smartd** process to automatically monitor the hard drive and log anything that fails. By default **smartd** logs to syslog, but I didn't have that running on the pogoplug device. So first I configured the file to monitor only the **sda** device. I edited the **/opt/smart/etc/smartd.conf** file and added/modified the following:

    #DEVICESCAN
    /dev/sda -a -d sat
    

Now start the **smartd** process with the following command:

    $ /opt/smart/sbin/smartd -c /opt/smart/etc/smartd.conf -d > /opt/var/log/smart.log &
    

If you check the log file after some time you should see the following:

    pogo:~# tail /opt/var/log/smart.log
    Device: /dev/sda [SAT], SMART Usage Attribute: 194 Temperature_Celsius changed from 38 to 37
    Device: /dev/sda [SAT], opened ATA device
    Device: /dev/sda [SAT], opened ATA device
    Device: /dev/sda [SAT], opened ATA device
    Device: /dev/sda [SAT], SMART Usage Attribute: 190 Airflow_Temperature_Cel changed from 63 to 64
    Device: /dev/sda [SAT], SMART Usage Attribute: 194 Temperature_Celsius changed from 37 to 36
    Device: /dev/sda [SAT], opened ATA device
    Device: /dev/sda [SAT], SMART Usage Attribute: 190 Airflow_Temperature_Cel changed from 64 to 65
    Device: /dev/sda [SAT], SMART Usage Attribute: 194 Temperature_Celsius changed from 36 to 35
    Device: /dev/sda [SAT], opened ATA device
    

### Enable *Smartctl* Zabbix Checks on Pogoplug

I didn't really want to install **perl** on the pogoplug device, so I ended up making my *discovery* script look like the following:

    pogo:~# cat /opt/local/bin/discover_disk.pl
    #!/bin/sh
    echo '{"data":[,{"{#DISK}":"sda",}]}'
    

It will just monitor one disk, which I am okay with. There is only one slot in the pogoplug, I won't be adding new drives to it. And here is how my **getsv** script looked like:

    pogo:~# cat /opt/local/bin/getsv
    #!/bin/sh
    if [ $# -ne 2 ];
    then
    echo "Usage: $0 <device> <parameter>"
    exit
    fi
    
    /opt/smart/sbin/smartctl -d sat -A $1 | grep $2 | tr -s ' ' | sed "s/^[[:space:]]*\(.*\)[[:space:]]*$/\1/" | cut -d " " -f 10
    

I didn't change that much, just removed **sudo** (since I won't be using it) and added the full path of the **smartctl** utility (could've taken care of this with symlinks). Then I added the following to **/opt/zabbix/etc/zabbix_agentd.conf**:

    pogo:~# tail -12 /opt/zabbix/etc/zabbix_agentd.conf
    UserParameter=custom.vfs.dev.read.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$4}'
    UserParameter=custom.vfs.dev.read.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$7}'
    UserParameter=custom.vfs.dev.write.ops[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$8}'
    UserParameter=custom.vfs.dev.write.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$11}'
    UserParameter=custom.vfs.dev.io.active[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$12}'
    UserParameter=custom.vfs.dev.io.ms[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$13}'
    UserParameter=custom.vfs.dev.read.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$6}'
    UserParameter=custom.vfs.dev.write.sectors[*],cat /proc/diskstats | grep $1 | head -1 | awk '{print $$10}'
    UserParameter=custom.disks.discovery_perl,/opt/local/bin/discover_disk.pl
    UserParameter=smart.temp[*],/opt/local/bin/getsv /dev/$1 Temperature_Celsius
    UserParameter=smart.reallocated_sec_cnt[*],/opt/local/bin/getsv /dev/$1 Reallocated_Sector_Ct
    UserParameter=custom.disks.discovery_perl2,/opt/local/bin/discover_disk.pl
    

And that was it, I then restart the *agentd* process:

    pogo:~# /opt/etc/init.d/zabbix-agentd restart
    Stopping zabbix agent:           Success (Killed)
    Starting zabbix agent:           Success
    

and after some time, I saw the following graph in zabbix:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_pogo_hd_temp.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_pogo_hd_temp.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/zabbix_pogo_hd_temp.png" alt="zabbix pogo hd temp Monitor SMART Attributes with Zabbix" width="1187" height="490" class="alignnone size-full wp-image-9580" title="Monitor SMART Attributes with Zabbix" /></a>

