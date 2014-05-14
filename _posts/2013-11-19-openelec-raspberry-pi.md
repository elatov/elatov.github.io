---
title: OpenELEC on Raspberry Pi
author: Karim Elatov
layout: post
permalink: /2013/11/openelec-raspberry-pi/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1973971648
categories:
  - OS
tags:
  - OpenELEC
  - Raspberry_Pi
  - xbmc
---
## Raspberry Pi

I received a free Raspberry Pi from <a href="http://www.simplivity.com/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.simplivity.com/']);">Simplivity</a> for being a <a href="http://blogs.vmware.com/vmtn/2013/05/vexpert-2013-awardees-announced.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vmtn/2013/05/vexpert-2013-awardees-announced.html']);">vExpert</a> (Congrats to Joe and Jarret on achieving the same!) It was very nice of them. It was even the <a href="http://downloads.element14.com/raspberryPi1.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://downloads.element14.com/raspberryPi1.html']);">B model</a> and not the A model&#8230; <a href="http://www.simplivity.com/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.simplivity.com/']);">Simplivity</a> doesn&#8217;t mess around <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile OpenELEC on Raspberry Pi" class="wp-smiley" title="OpenELEC on Raspberry Pi" /> After receiving the Raspberry Pi (RPi), I realized that I needed to order the following accessories to be able to use it:

*   Power Supply
*   SD flash card
*   AUX to RCA converter (since I will be using an RCA cable to connect to a TV)

I did some research and I came across <a href="http://elinux.org/RPi_SD_cards#SD_card_performance" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://elinux.org/RPi_SD_cards#SD_card_performance']);">this</a> site for a supported list of Flash Cards for the RPi. Pick one from the list that suits your needs <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile OpenELEC on Raspberry Pi" class="wp-smiley" title="OpenELEC on Raspberry Pi" /> I wasn&#8217;t planning to put movies on the SD Card, it was going to be used for the OS. Here is a list of all the parts (and links) that I ordered for the RPi:

*   <a href="http://www.amazon.com/dp/B007NDL56A/?tag=virtuallyhyper.com-20" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.amazon.com/dp/B007NDL56A/?tag=virtuallyhyper.com-20']);" rel="nofollow">SanDisk 32 GB SDHC Class 10</a> (probably went over board with 32GB, but will be useful for something else&#8230; maybe)
*   <a href="http://www.amazon.com/dp/B005LFXBJG/?tag=virtuallyhyper.com-20" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.amazon.com/dp/B005LFXBJG/?tag=virtuallyhyper.com-20']);" rel="nofollow">Motorola USB Charger</a>
*   <a href="http://www.amazon.com/dp/B00CEVNWM6/?tag=virtuallyhyper.com-20" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.amazon.com/dp/B00CEVNWM6/?tag=virtuallyhyper.com-20']);" rel="nofollow">3.5mm Stereo to 2 RCA Stereo</a>

If you are using HDMI or just regular speakers, the last part is probably unnecessary.

## Raspberry Pi and XBMC

From the get-go I wanted to use the RPi for a media center. I have used XBMC in the past and I really like it. There are actually 3 primary OSes that support running XBMC on the RPi. <a href="http://lifehacker.com/raspberry-pi-xbmc-solutions-compared-raspbmc-vs-openel-1394239600" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://lifehacker.com/raspberry-pi-xbmc-solutions-compared-raspbmc-vs-openel-1394239600']);">Here</a> is a good site that talk about all three:

*   <a href="http://www.raspbmc.com/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.raspbmc.com/']);">Raspbmc</a> 
*   <a href="http://www.xbian.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.xbian.org/']);">XBian</a> 
*   <a href="http://openelec.tv/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://openelec.tv/']);">OpenELEC</a>

From the top link, here is a quick summary for each:

> **Raspbmc**  
> Raspbmc is running a full version of Linux under the hood, so it takes a little while to boot up and takes up a good chunk of your SD card. The interface feels a little sluggish compared to a lighter weight distro like OpenELEC.
> 
> *Pros*: Easiest to install, does a lot out of the box, lots of room for tweaking  
> *Cons*: Slow
> 
> **OpenELEC**  
> OpenELEC has the same main goal as Raspbmc: provide a simple media center for your Raspberry Pi. The main difference between the two is that OpenELEC doesn&#8217;t bother with a Linux distro underneath it, and the entire installation is about 100 MB (Raspbmc is about twice this). OpenELEC is built for one purpose: to be a standalone and lightweight XBMC box.
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

At first, I decided to try Xbian since it seems pretty much in between. The install is fairly simple. Download their image from <a href="http://www.xbian.org/download/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.xbian.org/download/']);">here</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-download.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-download.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-download.png" alt="xbian download OpenELEC on Raspberry Pi" width="963" height="660" class="alignnone size-full wp-image-9752" title="OpenELEC on Raspberry Pi" /></a>

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/Rpi-great.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/Rpi-great.jpg']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/Rpi-great.jpg" alt="Rpi great OpenELEC on Raspberry Pi" width="1840" height="3264" class="alignnone size-full wp-image-9754" title="OpenELEC on Raspberry Pi" /></a>

As soon as you plug in the power cord, the RPi will start to boot. As promised, the configuration was really easy. You can even SSH into xbian, run **xbian-config**, and it will give you an **ncurses** terminal UI to make some of the configuration changes:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-config.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-config.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbian-config.png" alt="xbian config OpenELEC on Raspberry Pi" width="698" height="293" class="alignnone size-full wp-image-9756" title="OpenELEC on Raspberry Pi" /></a>

More information on configuring **Xbian** can be found <a href="http://wiki.xbian.org/Main_Page" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.xbian.org/Main_Page']);">here</a>

I definitely liked the ease of use of **XBian**. I then configured XBMC to play files from my Plex Media Server using UPNP and the playback was pretty smooth. However playing internet streams was a little choppy. When I was using my old XBMC machine, it wasn&#8217;t like that. Since I haven&#8217;t invested too much time with Xbian, I decided to try out OpenELEC.

### OpenElec

The install is very similar for OpenELEC as it was for Xbian. Go the OpenELEC download page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-downloads-page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-downloads-page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-downloads-page.png" alt="openelec downloads page OpenELEC on Raspberry Pi" width="963" height="391" class="alignnone size-full wp-image-9758" title="OpenELEC on Raspberry Pi" /></a>

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
    

That will finish the install. After it&#8217;s done, unplug the SD Card from the laptop and then plug it into the RPi. Plug in the power and it will start to boot. After the boot up process is finished you will see the setup wizard:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-wizard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-wizard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-wizard.png" alt="openelec wizard OpenELEC on Raspberry Pi" width="547" height="321" class="alignnone size-full wp-image-9759" title="OpenELEC on Raspberry Pi" /></a>

Just follow the wizard and configure it to your fit your needs. Playing media via UPNP was smooth. Also watching internet streams was not choppy. So I was pretty happy with the OpenELEC install. After that, I customized the install with little tweaks.

#### Change the Skin to xTV-SAF

From XBMC go to **System** -> **Appearance** -> **Skin** -> **Get More** and install the **xTV-SAF** skin/theme. After it&#8217;s installed, it will look like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xtv-saf-skin-enabled.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xtv-saf-skin-enabled.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xtv-saf-skin-enabled.png" alt="xtv saf skin enabled OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9761" title="OpenELEC on Raspberry Pi" /></a>

I use that skin since my TV has a pretty low resolution and it&#8217;a hard to see some of the options.

#### Change the Font for the xTV-SAF Skin

On top of installing another skin, I also ended up increasing the font to ease reading the tiny sub-options. During the initial configuration wizard, I ended up enabling **ssh** for OpenELEC. So I can ssh into the RPi by using the following credentials:

> user: root  
> passwd: openelec

One bad thing about OpenELEC is that you can&#8217;t change the root password, since the **rootfs** is mounted read-only as **squashfs**:

    pi:~ # mount  | grep ' / '
    rootfs on / type rootfs (rw)
    /dev/loop0 on / type squashfs (ro,relatime)
    

And you can&#8217;t remount **squashfs** read/write on the fly. To change the password you have mount the SD card on another machine and make changes there. The process is described <a href="http://wrightrocket.blogspot.com/2012/06/openelec-on-raspberry-pi.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wrightrocket.blogspot.com/2012/06/openelec-on-raspberry-pi.html']);">here</a>. This is only for my home, so I didn&#8217;t care about that.

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

I read a couple of sites that talked about **dirty regions**. More information on dirty regions can be seen <a href="http://wiki.xbmc.org/index.php?title=Dirty_regions" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.xbmc.org/index.php?title=Dirty_regions']);">here</a>. From that page:

> Enable dirty-region processing. Dirty regions are any parts of the screen that have changed since the last frame. By not re-rendering what hasn&#8217;t changed, big speed gains can be seen. Because all GPUs work differently, only Mode 3, combined with nofliptimeout=0, is guaranteed to be safe for everyone.

I also saw a couple of other posts that had similar goals:

*   <a href="http://lokir.wordpress.com/2013/01/12/openelec-raspberry-pi-tweaks/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://lokir.wordpress.com/2013/01/12/openelec-raspberry-pi-tweaks/']);">OpenElec Raspberry PI – tweaks</a> 
*   <a href="http://mrpfister.com/journal/setting-up-openelec-on-the-raspberry-pi/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://mrpfister.com/journal/setting-up-openelec-on-the-raspberry-pi/']);">Setting up OpenELEC on the Raspberry Pi</a>
*   <a href="http://wiki.openelec.tv/index.php?title=Building_and_Installing_OpenELEC_for_Raspberry_Pi#Enable_dirty_region_redraw_in_XBMC" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.openelec.tv/index.php?title=Building_and_Installing_OpenELEC_for_Raspberry_Pi#Enable_dirty_region_redraw_in_XBMC']);">Building and Installing OpenELEC for Raspberry Pi</a>

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
    

So far I haven&#8217;t seen any issues, but I might have to play with the setting more to see if something changes.

Restart OpenELEC to apply the above changes.

#### Enable Automatic Updates

If you didn&#8217;t select Automatic update during the configuration wizard you can enable it later. Go to **Add-Ons** -> **Programs** -> **OpenELEC Settings** -> **System** and make sure &#8220;**Automatic Update**&#8221; is set to **auto**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-settings.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-settings.png" alt="openelec settings OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9784" title="OpenELEC on Raspberry Pi" /></a>

#### Install optware on OpenELEC

I did this on the **pogoplug** device <a href="http://virtuallyhyper.com/2013/09/backing-rsync-to-pogoplug/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/09/backing-rsync-to-pogoplug/']);">before</a>, so I decided to try it out on OpenELEC. The process is very similar. First download the main **ipkg** package

    pi:~ # mkdir -p opt/tmp
    pi:~ # cd opt/tmp
    pi:~/opt/tmp # wget http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable/ipkg-opt_0.99.163-10_arm.ipk
    pi:~/opt/tmp # tar xf ipkg-opt_0.99.163-10_arm.ipk
    pi:~/opt/tmp # tar xf data.tar.gz
    pi:~/opt/tmp # mv opt/* ../opt/.
    

Our **opt** directory is ready, since we can&#8217;t change **rootfs**, we can just mount on top of **/opt** from the home directory. It looks like **/opt** has some files in it:

    pi:~ # ls -R /opt
    /opt:
    vc
    
    /opt/vc:
    lib
    

So before we mount on top of **/opt**, let&#8217;s copy the information into our **opt** directory:

    pi:~ # cp -r /opt/. opt/.
    

Now let&#8217;s mount our directory:

    pi:~ # mount /storage/opt /opt
    pi:~ # mount | grep opt
    /dev/mmcblk0p2 on /opt type ext4 (rw,noatime,data=ordered)
    pi:~ # df -h | grep opt
    /dev/mmcblk0p2           29.0G    356.9M     27.2G   1% /opt
    

Now let&#8217;s enable the repository to download the packages from:

    pi:~ # echo "src cross http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable" >> /opt/etc/ipkg.conf
    

Also let&#8217;s add **/opt/bin/** to our path:

    pi:~ # cat .profile 
    PATH=$PATH:/opt/bin
    

Now you can install your regular packages. First let&#8217;s make sure **ipkg** is working:

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
    

I didn&#8217;t change anything. To start **snmpd**, just run the following:

    pi:~ # /opt/etc/init.d/S70net-snmp 
    

Make sure it&#8217;s running by doing the following:

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-cpu-usage.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-cpu-usage.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-cpu-usage.png" alt="pi cpu usage OpenELEC on Raspberry Pi" width="1170" height="490" class="alignnone size-full wp-image-9762" title="OpenELEC on Raspberry Pi" /></a>

and here is the network:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-eth0-usage.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-eth0-usage.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/pi-eth0-usage.png" alt="pi eth0 usage OpenELEC on Raspberry Pi" width="1080" height="511" class="alignnone size-full wp-image-9763" title="OpenELEC on Raspberry Pi" /></a>

If you want **snmpd** to be started automatically, make sure your **.config/autostart.sh** looks likes this:

    pi:~ # cat .config/autostart.sh 
    #!/bin/sh
    /bin/mount /storage/opt /opt
    sleep 3
    /opt/etc/init.d/S70net-snmp
    

#### Backup XBMC

If you want to back up XBMC (which is what OpenELEC basically consists of), then we can use the **XBMC Backup** add-on, it&#8217;s part of the XBMC repository. <a href="http://wiki.xbmc.org/index.php?title=Add-on:XBMC_Backup" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','']);">Here</a> is a link to the add-on. From that link here are the instructions to install the add-on:

1.  Settings 
2.  Add-ons
3.  Get add-ons 
4.  XBMC.org Add-ons 
5.  Program Add-ons 
6.  XBMC Backup 
7.  Install

After it&#8217;s installed go to Add-ons section:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/addons-enabled-addons.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/addons-enabled-addons.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/addons-enabled-addons.png" alt="addons enabled addons OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9764" title="OpenELEC on Raspberry Pi" /></a>

Then click on **Enabled-Addons**, scroll down to the **XBMC Backup** Addon, select it, and you should see this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-configure.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-configure.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-configure.png" alt="xbmc backup configure OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9765" title="OpenELEC on Raspberry Pi" /></a>

Then click on **configure** and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup_general.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup_general.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup_general.png" alt="xbmc backup general OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9766" title="OpenELEC on Raspberry Pi" /></a>

Notice I configured it to do local backups to the **/storage/backups** directory. If you have a remote NFS or Samba server (you can even back up to dropbox) then you can do that:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-browse-directory.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-browse-directory.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-browse-directory.png" alt="xbmc backup browse directory OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9767" title="OpenELEC on Raspberry Pi" /></a>

You can also choose what to back up and setup a schedule for your backups. After we are done with the configuration we can do a manual back up. From the main screen go to **Add-Ons** -> **Programs**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-program.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-program.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-program.png" alt="xbmc program OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9768" title="OpenELEC on Raspberry Pi" /></a>

Select **XBMC Backup**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup.png" alt="xbmc backup manual backup OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9769" title="OpenELEC on Raspberry Pi" /></a>

Then select **Backup** and you should see the backup start:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup_going.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup_going.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-backup-manual-backup_going.png" alt="xbmc backup manual backup going OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9770" title="OpenELEC on Raspberry Pi" /></a>

After the backup is finished you should see the backup in the folder that we set:

    pi:~ # du -h backups/ -d 1
    68.2M   backups/20131116
    68.2M   backups/
    

That looks good. Now we can setup a **cron job** to **rsync** the data off to our back up server. To create the cron job, just run the following:

    pi:~ # crontab -e
    

and a **nano** window will pop up, at which point you can enter the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/crontab-openelec.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/crontab-openelec.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/crontab-openelec.png" alt="crontab openelec OpenELEC on Raspberry Pi" width="798" height="456" class="alignnone size-full wp-image-9771" title="OpenELEC on Raspberry Pi" /></a>

After you done with you configurations, save and close the file. So I will backup to the remote server every month on the 2nd day of the month. You can confirm your **crontab** is in place by running the following:

    pi:~ # crontab -l
    30 3 2 * * /opt/bin/rsync -azq backups/. 192.168.1.104:/backups/pi/.
    

#### Install the Rsync Add-on

If you won&#8217;t want to mess with **optware** but still want **rsync** on OpenELEC you can use the unofficial repository to install the **rsync** add-on (which basically installs the rsync binary in a weird location). First download the zip for the repository from <a href="http://unofficial.addon.pro/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://unofficial.addon.pro/']);">here</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-unoff-repo.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-unoff-repo.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/openelec-unoff-repo.png" alt="openelec unoff repo OpenELEC on Raspberry Pi" width="344" height="281" class="alignnone size-full wp-image-9772" title="OpenELEC on Raspberry Pi" /></a>

After you have the zip, **scp** it over to the RPi:

    elatov@fed:~/downloads$scp repository.unofficial.addon.pro-3.0.0.zip pi:
    

Now to install zip, go to **Add-ons** -> **Install from Zip**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-addon-install-from-zip.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-addon-install-from-zip.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-addon-install-from-zip.png" alt="xbmc addon install from zip OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9773" title="OpenELEC on Raspberry Pi" /></a>

Then browse to your home directory and select the zip archive:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-zip.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-zip.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-zip.png" alt="select unof repo zip OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9774" title="OpenELEC on Raspberry Pi" /></a>

After it&#8217;s installed you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/unof-repo-enabled.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/unof-repo-enabled.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/unof-repo-enabled.png" alt="unof repo enabled OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9775" title="OpenELEC on Raspberry Pi" /></a>

That should enable the Unofficial OpenELEC Repository. Next let&#8217;s install **rsync** from that repository. Go to **Add-ons** -> **Get Add-ons**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/addon-screen-get-addons.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/addon-screen-get-addons.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/addon-screen-get-addons.png" alt="addon screen get addons OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9776" title="OpenELEC on Raspberry Pi" /></a>

Then select the **Unofficial OpenELEC Repository**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-for-addons.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-for-addons.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-unof-repo-for-addons.png" alt="select unof repo for addons OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9777" title="OpenELEC on Raspberry Pi" /></a>

Then select **Program Add-ons**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/program-addons-from-unof-repo.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/program-addons-from-unof-repo.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/program-addons-from-unof-repo.png" alt="program addons from unof repo OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9778" title="OpenELEC on Raspberry Pi" /></a>

and then select **rsync**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-rsync-plugin-from-unof-repo.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/select-rsync-plugin-from-unof-repo.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/select-rsync-plugin-from-unof-repo.png" alt="select rsync plugin from unof repo OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9779" title="OpenELEC on Raspberry Pi" /></a>

After it&#8217;s installed you should see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/rsync-plugin-installed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/rsync-plugin-installed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/rsync-plugin-installed.png" alt="rsync plugin installed OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9780" title="OpenELEC on Raspberry Pi" /></a>

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-general-settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-general-settings.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-general-settings.png" alt="xbmc general settings OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9785" title="OpenELEC on Raspberry Pi" /></a>

Here is the **Hardware** information:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-hardware-info.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-hardware-info.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/11/xbmc-hardware-info.png" alt="xbmc hardware info OpenELEC on Raspberry Pi" width="720" height="480" class="alignnone size-full wp-image-9786" title="OpenELEC on Raspberry Pi" /></a>

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
    

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/11/openelec-raspberry-pi/" title=" OpenELEC on Raspberry Pi" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:OpenELEC,Raspberry_Pi,xbmc,blog;button:compact;">Raspberry Pi I received a free Raspberry Pi from Simplivity for being a vExpert (Congrats to Joe and Jarret on achieving the same!) It was very nice of them. It...</a>
</p>