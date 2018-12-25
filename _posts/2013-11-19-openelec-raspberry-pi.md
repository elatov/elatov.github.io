---
title: OpenELEC on Raspberry Pi
author: Karim Elatov
layout: post
permalink: /2013/11/openelec-raspberry-pi/
categories: ['os']
tags: ['mmcblk0', 'optware', 'upnp', 'linux', 'openelec', 'raspberry_pi', 'xbmc']
---
{% include note.html content="It looks like OpenElec is [no longer maintained](https://kodi.wiki/view/Archive:OpenELEC) and LibreElec is recommended" %}
## Raspberry Pi

I received a free Raspberry Pi from [Simplivity](http://www.simplivity.com)  for being a [vExpert](http://blogs.vmware.com/vmtn/2013/05/vexpert-2013-awardees-announced.html) (Congrats to Joe and Jarret on achieving the same!) It was very nice of them. It was even the [B model](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) and not the A model... [Simplivity](http://www.simplivity.com) doesn't mess around :). After receiving the Raspberry Pi (RPi), I realized that I needed to order the following accessories to be able to use it:

*   Power Supply
*   SD flash card
*   AUX to RCA converter (since I will be using an RCA cable to connect to a TV)

I did some research and I came across [this](http://elinux.org/RPi_SD_cards#SD_card_performance) site for a supported list of Flash Cards for the RPi. Pick one from the list that suits your needs :) I wasn't planning to put movies on the SD Card, it was going to be used for the OS. Here is a list of all the parts (and links) that I ordered for the RPi:

*   [SanDisk 32 GB SDHC Class 10](http://www.amazon.com/dp/B007NDL56A/?tag=virtuallyhyper.com-20") (probably went over board with 32GB, but will be useful for something else... maybe)
*   [Motorola USB Charger](http://www.amazon.com/dp/B005LFXBJG/?tag=virtuallyhyper.com-20")
*   [3.5mm Stereo to 2 RCA Stereo](http://www.amazon.com/dp/B00CEVNWM6/?tag=virtuallyhyper.com-20")

If you are using HDMI or just regular speakers, the last part is probably unnecessary.

## Raspberry Pi and XBMC

From the get-go I wanted to use the RPi for a media center. I have used XBMC in the past and I really like it. There are actually 3 primary OSes that support running XBMC on the RPi. [Here](http://lifehacker.com/raspberry-pi-xbmc-solutions-compared-raspbmc-vs-openel-1394239600) is a good site that talk about all three:

*   [Raspbmc -- now OSMC](https://osmc.tv/)
*   [XBian](http://www.xbian.org/)
*   [LibreELEC](https://libreelec.tv/)

From the top link, here is a quick summary for each:

> **Raspbmc**
> Raspbmc is running a full version of Linux under the hood, so it takes a little while to boot up and takes up a good chunk of your SD card. The interface feels a little sluggish compared to a lighter weight distro like OpenELEC.
>
> *Pros*: Easiest to install, does a lot out of the box, lots of room for tweaking
> *Cons*: Slow
>
> **OpenELEC**
> OpenELEC has the same main goal as Raspbmc: provide a simple media center for your Raspberry Pi. The main difference between the two is that OpenELEC doesn't bother with a Linux distro underneath it, and the entire installation is about 100 MB (Raspbmc is about twice this). OpenELEC is built for one purpose: to be a standalone and lightweight XBMC box.
>
> *Pros*: Very fast
> *Cons*: More difficult installation, not a lot of room for tweaking
>
> **XBian**
> XBian is all about two things: constant updates and new features. Like OpenELEC, XBian is simple and small. This makes XBian fast to boot, easy to install, and easy to use. Xbian is built on top of Raspbian, the main operating system for the Raspberry Pi.
>
> XBian also supports packaged installers where you can download entire sets of software in one click. This means you can set up something like Samba, Couch Potato, or Sick Beard easily, perfect for a mini home server
>
> *Pros*: Fast, highly configurable, easy to install, gets features earlier than anyone else
> *Cons*: Possibility for bugs on the bleeding edge

### XBian

At first, I decided to try Xbian since it seems pretty much in between. The install is fairly simple. Download their image from [here](http://www.xbian.org/getxbian/):

![xbian download OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbian-download.png)

I just grabbed the latest version at the time. After the download was finished, I had the following file on my laptop:

    elatov@fed:~/downloads$ls -l *.7z
    -rw-rw-r-- 1 elatov elatov 215575566 Oct 26 10:39 XBian_1.0_Beta_1.1.7z


Exacting the file looked like this:

    elatov@fed:~/downloads$$7za x XBian_1.0_Beta_1.1.7z
    7-Zip (A) [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,2 CPUs)

    Processing archive: XBian_1.0_Beta_1.1.7z

    Extracting  XBian_1.0_Beta_1.1.img

    Everything is Ok

    Size:       534773760
    Compressed: 215575566


I then plugged in the Flash Card into the laptop and I saw the following in **dmesg**:

    elatov@fed:~$ dmesg | tail -16
    [ 1639.674437] mmc0: new high speed SDHC card at address e624
    [ 1639.776374] mmcblk0: mmc0:e624 SU32G 29.7 GiB
    [ 1639.780554] mmcblk0: error -123 sending status command, retrying
    [ 1639.782592] mmcblk0: error -123 sending status command, retrying
    [ 1639.784618] mmcblk0: error -123 sending status command, aborting
    [ 1639.791952] ldm_validate_partition_table(): Disk read failed.
    [ 1639.792111] Dev mmcblk0: unable to read RDB block 0
    [ 1639.792133]  mmcblk0: unable to read partition table
    [ 1639.966131] mmc0: card e624 removed
    [ 1642.257850] mmc0: new high speed SDHC card at address e624
    [ 1642.259458] mmcblk0: mmc0:e624 SU32G 29.7 GiB
    [ 1642.266301]  mmcblk0: p1
    [ 1643.751614] mmc0: card e624 removed
    [ 1647.889694] mmc0: new high speed SDHC card at address e624
    [ 1647.890583] mmcblk0: mmc0:e624 SU32G 29.7 GiB
    [ 1647.899235]  mmcblk0: p1


So my device showed up as **/dev/mmcblk0**. Now for the actual install:

    elatov@fed:~/downloads$ sudo dd if=XBian_1.0_Beta_1.1.img of=/dev/mmcblk0


After the install finished, I eject the SD Card from my laptop and then plugged into the RPi. BTW here is how the final RPi looked like:

![Rpi great OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/Rpi-great.jpg)

As soon as you plug in the power cord, the RPi will start to boot. As promised, the configuration was really easy. You can even SSH into xbian, run **xbian-config**, and it will give you an **ncurses** terminal UI to make some of the configuration changes:

![xbian config OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbian-config.png)

More information on configuring **Xbian** can be found [here](http://wiki.xbian.org/doku.php)

I definitely liked the ease of use of **XBian**. I then configured XBMC to play files from my Plex Media Server using UPNP and the playback was pretty smooth. However playing internet streams was a little choppy. When I was using my old XBMC machine, it wasn't like that. Since I haven't invested too much time with Xbian, I decided to try out OpenELEC.

### OpenElec

The install is very similar for OpenELEC as it was for Xbian. Go the OpenELEC download page:

![openelec downloads page OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/openelec-downloads-page.png)

After the download is finished, you should have the following file:

    elatov@fed:~/downloads$ls -l *.tar
    -rw-rw-r-- 1 elatov elatov 101253120 Oct 27 08:26 OpenELEC-RPi.arm-3.2.3.tar


Extract the archive:

    elatov@fed:~/downloads$tar xf OpenELEC-RPi.arm-3.2.3.tar


The archive contains an installer which will basically create the necessary partitions and then **dd** the OpenELEC image onto the device that you provide as an argument to the install script. You can check what utilities are necessary for the install script by running the following:

    elatov@fed:~/downloads$ cd OpenELEC-RPi.arm-3.2.3
    elatov@fed:~/downloads/OpenELEC-RPi.arm-3.2.3$ grep which create_sdcard
      which parted > /dev/null
      which mkfs.vfat > /dev/null
      which mkfs.ext4 > /dev/null
      which partprobe > /dev/null
      which md5sum > /dev/null


If you have all of the above tools already installed, then run the following:

    elatov@fed:~/downloads/OpenELEC-RPi.arm-3.2.3$ sudo ./create_sdcard /dev/mmcblk0


That will finish the install. After it's done, unplug the SD Card from the laptop and then plug it into the RPi. Plug in the power and it will start to boot. After the boot up process is finished you will see the setup wizard:

![openelec wizard OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/openelec-wizard.png)

Just follow the wizard and configure it to your fit your needs. Playing media via UPNP was smooth. Also watching internet streams was not choppy. So I was pretty happy with the OpenELEC install. After that, I customized the install with little tweaks.

#### Change the Skin to xTV-SAF

From XBMC go to **System** -> **Appearance** -> **Skin** -> **Get More** and install the **xTV-SAF** skin/theme. After it's installed, it will look like this:

![xtv saf skin enabled OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xtv-saf-skin-enabled.png)

I use that skin since my TV has a pretty low resolution and it'a hard to see some of the options.

#### Change the Font for the xTV-SAF Skin

On top of installing another skin, I also ended up increasing the font to ease reading the tiny sub-options. During the initial configuration wizard, I ended up enabling **ssh** for OpenELEC. So I can ssh into the RPi by using the following credentials:

> user: root
> passwd: openelec

One bad thing about OpenELEC is that you can't change the root password, since the **rootfs** is mounted read-only as **squashfs**:

    pi:~ # mount  | grep ' / '
    rootfs on / type rootfs (rw)
    /dev/loop0 on / type squashfs (ro,relatime)


And you can't remount **squashfs** read/write on the fly. To change the password you have mount the SD card on another machine and make changes there. The process is described [here](http://wrightrocket.blogspot.com/2012/06/openelec-on-raspberry-pi.html). This is only for my home, so I didn't care about that.

To change the font for the **xTV-SAF** skin, edit the following file:

    pi:~ # vi .xbmc/addons/skin.xtv-saf/720p/Font.xml


and modify the following section:

    <fontset id="XBMC Default" idloc="31577" unicode="true">
                    <font>
                            <name>rss20</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font11</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font12</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font13</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font18</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font20</name>
                            <filename>arial.ttf</filename>
                            <size>36</size>
                    </font>
                    <font>
                            <name>font22</name>
                            <filename>arial.ttf</filename>
                            <size>38</size>
                    </font>
                    <font>
                            <name>font28</name>
                            <filename>arial.ttf</filename>
                            <size>48</size>
                    </font>
            </fontset>


Restart OpenELEC to apply the above changes.

#### Enable the XBMC Webserver

Usually this is available in the regular XBMC settings, but with OpenELEC we have to edit the **.xbmc/userdata/guisettings.xml** file and add the following to it:

    <webserver>true</webserver>
    <webserverpassword>password</webserverpassword>
    <webserverport>8080</webserverport>
    <webserverusername>elatov</webserverusername>
    <webskin>webinterface.default</webskin>


Restart OpenELEC to apply the above changes.

#### OpenELEC Performance Tweaks

I read a couple of sites that talked about **dirty regions**. More information on dirty regions can be seen [here](http://kodi.wiki/view/HOW-TO:Modify_dirty_regions). From that page:

> Enable dirty-region processing. Dirty regions are any parts of the screen that have changed since the last frame. By not re-rendering what hasn't changed, big speed gains can be seen. Because all GPUs work differently, only Mode 3, combined with nofliptimeout=0, is guaranteed to be safe for everyone.

I also saw a couple of other posts that had similar goals:

*   [OpenElec Raspberry PI – tweaks](http://lokir.wordpress.com/2013/01/12/openelec-raspberry-pi-tweaks/)
*   [HOW-TO:Modify dirty regions](http://kodi.wiki/view/Dirty_regions)

In the end, I added the following to my **.xbmc/userdata/advancedsettings.xml** file:

    <?xml version="1.0" encoding="UTF-8"?>
    <advancedsettings>
      <network>
        <cachemembuffersize>30242880</cachemembuffersize>
      </network>
      <fanartheight>560</fanartheight>
      <thumbsize>256</thumbsize>
      <gui>
        <algorithmdirtyregions>3</algorithmdirtyregions>
        <nofliptimeout>0</nofliptimeout>
      </gui>
      <bginfoloadermaxthreads>2</bginfoloadermaxthreads>
    </advancedsettings>


So far I haven't seen any issues, but I might have to play with the setting more to see if something changes.

Restart OpenELEC to apply the above changes.

#### Enable Automatic Updates

If you didn't select Automatic update during the configuration wizard you can enable it later. Go to **Add-Ons** -> **Programs** -> **OpenELEC Settings** -> **System** and make sure "**Automatic Update**" is set to **auto**:

![openelec settings OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/openelec-settings.png)

#### Install optware on OpenELEC

I did this on the **pogoplug** device [before](/2013/09/backing-rsync-to-pogoplug/), so I decided to try it out on OpenELEC. The process is very similar. First download the main **ipkg** package

    pi:~ # mkdir -p opt/tmp
    pi:~ # cd opt/tmp
    pi:~/opt/tmp # wget http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/ipkg-opt_0.99.163-10_arm.ipk
    pi:~/opt/tmp # tar xf ipkg-opt_0.99.163-10_arm.ipk
    pi:~/opt/tmp # tar xf data.tar.gz
    pi:~/opt/tmp # mv opt/* ../opt/.


Our **opt** directory is ready, since we can't change **rootfs**, we can just mount on top of **/opt** from the home directory. It looks like **/opt** has some files in it:

    pi:~ # ls -R /opt
    /opt:
    vc

    /opt/vc:
    lib


So before we mount on top of **/opt**, let's copy the information into our **opt** directory:

    pi:~ # cp -r /opt/. opt/.


Now let's mount our directory:

    pi:~ # mount /storage/opt /opt
    pi:~ # mount | grep opt
    /dev/mmcblk0p2 on /opt type ext4 (rw,noatime,data=ordered)
    pi:~ # df -h | grep opt
    /dev/mmcblk0p2           29.0G    356.9M     27.2G   1% /opt


Now let's enable the repository to download the packages from:

    pi:~ # echo "src cross http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable" >> /opt/etc/ipkg.conf


Also let's add **/opt/bin/** to our path:

    pi:~ # cat .profile
    PATH=$PATH:/opt/bin


Now you can install your regular packages. First let's make sure **ipkg** is working:

    pi:~ # ipkg update
    Downloading http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/Packages
    Updated list of available packages in /opt/lib/ipkg/lists/cross
    Successfully terminated.


I ended installing **rsync** just for testing, and it worked out:

    pi:~ # ipkg install rsync


If you want **/opt** to be automatically mounted on boot, add the following to your **.config/autostart.sh** file :

    pi:~ # cat .config/autostart.sh
    #!/bin/sh
    /bin/mount /storage/opt /opt


#### Monitor OpenELEC with SNMP

Since I was pretty low on ram:

    pi:~ # vcgencmd get_mem arm && vcgencmd get_mem gpu
    arm=384M
    gpu=128M


I had 384M for the OS and 128M for the GPU, and XBMC was using most of that.

I decided to monitor the RPi with SNMP and not with the zabbix agent. Although the zabbix server can query either. To install SNMP I just used **optware**:

    pi:~ # ipkg install net-snmp
    Installing net-snmp (5.4.2.1-1) to root...
    Downloading http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/net-snmp_5.4.2.1-1_arm.ipk
    Configuring net-snmp
    Successfully terminated.


If you want to change something, you can check out the configuration for SNMP here:

    pi:~ # vi /opt/etc/snmpd.conf


I didn't change anything. To start **snmpd**, just run the following:

    pi:~ # /opt/etc/init.d/S70net-snmp


Make sure it's running by doing the following:

    pi:~ # ps -eaf | grep snmp
    22705 root       0:00 /opt/sbin/snmpd -c /opt/etc/snmpd.conf


Also do a quick test query:

    pi:~ # snmpwalk -v 2c -c public 127.0.0.1 system
    SNMPv2-MIB::sysDescr.0 = STRING: Linux pi 3.10.16 #1 PREEMPT Thu Oct 17 10:24:10 CEST 2013 armv6l
    SNMPv2-MIB::sysObjectID.0 = OID: NET-SNMP-MIB::netSnmpAgentOIDs.10
    DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (15205) 0:02:32.05
    SNMPv2-MIB::sysContact.0 = STRING: "KE"
    SNMPv2-MIB::sysName.0 = STRING: pi
    SNMPv2-MIB::sysLocation.0 = STRING: "Home"
    SNMPv2-MIB::sysORLastChange.0 = Timeticks: (3) 0:00:00.03
    ...
    ...


Then when adding the machine to Zabbix for monitoring just select SNMP as the protocol. After some time you will be able to see CPU usage and network usage:

![pi cpu usage OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/pi-cpu-usage.png)

and here is the network:

![pi eth0 usage OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/pi-eth0-usage.png)

If you want **snmpd** to be started automatically, make sure your **.config/autostart.sh** looks likes this:

    pi:~ # cat .config/autostart.sh
    #!/bin/sh
    /bin/mount /storage/opt /opt
    sleep 3
    /opt/etc/init.d/S70net-snmp


#### Backup XBMC

If you want to back up XBMC (which is what OpenELEC basically consists of), then we can use the **XBMC Backup** add-on, it's part of the XBMC repository. [Here](http://kodi.wiki/view/Backup) is a link to the add-on. From that link here are the instructions to install the add-on:

1.  Settings
2.  Add-ons
3.  Get add-ons
4.  XBMC.org Add-ons
5.  Program Add-ons
6.  XBMC Backup
7.  Install

After it's installed go to Add-ons section:

![addons enabled addons OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/addons-enabled-addons.png)

Then click on **Enabled-Addons**, scroll down to the **XBMC Backup** Addon, select it, and you should see this:

![xbmc backup configure OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-backup-configure.png)

Then click on **configure** and you will see the following:

![xbmc backup general OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-backup_general.png)

Notice I configured it to do local backups to the **/storage/backups** directory. If you have a remote NFS or Samba server (you can even back up to dropbox) then you can do that:

![xbmc backup browse directory OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-backup-browse-directory.png)

You can also choose what to back up and setup a schedule for your backups. After we are done with the configuration we can do a manual back up. From the main screen go to **Add-Ons** -> **Programs**:

![xbmc program OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-program.png)

Select **XBMC Backup**:

![xbmc backup manual backup OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-backup-manual-backup.png)

Then select **Backup** and you should see the backup start:

![xbmc backup manual backup going OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-backup-manual-backup_going.png)

After the backup is finished you should see the backup in the folder that we set:

    pi:~ # du -h backups/ -d 1
    68.2M   backups/20131116
    68.2M   backups/


That looks good. Now we can setup a **cron job** to **rsync** the data off to our back up server. To create the cron job, just run the following:

    pi:~ # crontab -e


and a **nano** window will pop up, at which point you can enter the following:

![crontab openelec OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/crontab-openelec.png)

After you done with you configurations, save and close the file. So I will backup to the remote server every month on the 2nd day of the month. You can confirm your **crontab** is in place by running the following:

    pi:~ # crontab -l
    30 3 2 * * /opt/bin/rsync -azq backups/. 192.168.1.104:/backups/pi/.


#### Install the Rsync Add-on

If you won't want to mess with **optware** but still want **rsync** on OpenELEC you can use the unofficial repository to install the **rsync** add-on (which basically installs the rsync binary in a weird location). First download the zip for the repository from [here](http://unofficial.addon.pro/):

![openelec unoff repo OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/openelec-unoff-repo.png)

After you have the zip, **scp** it over to the RPi:

    elatov@fed:~/downloads$scp repository.unofficial.addon.pro-3.0.0.zip pi:


Now to install zip, go to **Add-ons** -> **Install from Zip**:

![xbmc addon install from zip OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-addon-install-from-zip.png)

Then browse to your home directory and select the zip archive:

![select unof repo zip OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/select-unof-repo-zip.png)

After it's installed you should see the following:

![unof repo enabled OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/unof-repo-enabled.png)

That should enable the Unofficial OpenELEC Repository. Next let's install **rsync** from that repository. Go to **Add-ons** -> **Get Add-ons**:

![addon screen get addons OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/addon-screen-get-addons.png)

Then select the **Unofficial OpenELEC Repository**:

![select unof repo for addons OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/select-unof-repo-for-addons.png)

Then select **Program Add-ons**:

![program addons from unof repo OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/program-addons-from-unof-repo.png)

and then select **rsync**:

![select rsync plugin from unof repo OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/select-rsync-plugin-from-unof-repo.png)

After it's installed you should see the following:

![rsync plugin installed OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/rsync-plugin-installed.png)

For some reason initially the rsync binary was not executable for me:

    pi:~ # rsync
    -sh: rsync: Permission denied


Maybe I need to restart OpenELEC, but I just ended up manually changing the permissions on it. First find the binary:

    pi:~ # type rsync
    rsync is a tracked alias for /storage/.xbmc/addons/network.backup.rsync/bin/rsync


Then make that executable:

    pi:~ # chmod +x /storage/.xbmc/addons/network.backup.rsync/bin/rsync


After that I was able to use **rsync**. In your **crontab** entry use the above path if you are **rsyncing** backups from the above setup.

#### OpenELEC Information

The GUI has most of the information. If you go to **System** -> **System Info**, here is what is seen under the **General** section:

![xbmc general settings OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-general-settings.png)

Here is the **Hardware** information:

![xbmc hardware info OpenELEC on Raspberry Pi](https://github.com/elatov/uploads/raw/master/2013/11/xbmc-hardware-info.png)

You can get most of the information from the command line as well. Here are two commands that can show you the temperature:

    pi:~ # vcgencmd measure_temp
    temp=50.8'C

    pi:~ # sensors
    bcm2835_thermal-virtual-0
    Adapter: Virtual device
    temp1:        +50.8 C


I was actually surprised to see the sensors module working. You can also check what codecs are enabled like so:

    pi:~ # for codec in H264 MPG2 WVC1 MPG4 MJPG WMV9 ; do echo -e "$codec:\t$(vcgen
    cmd codec_enabled $codec)" ;done
    H264:   H264=enabled
    MPG2:   MPG2=disabled
    WVC1:   WVC1=disabled
    MPG4:   MPG4=enabled
    MJPG:   MJPG=enabled
    WMV9:   WMV9=disabled


You can check the current resolution with the following command:

    pi:~ # tvservice -s
    state 0x40001 [NTSC 4:3], 720x480 @ 60Hz, interlaced


