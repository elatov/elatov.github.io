---
title: Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix
author: Karim Elatov
layout: post
permalink: /2013/12/configure-ipmi-supermicro-server-monitor-ipmi-sensors-zabbix/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2094538676
categories:
  - Home Lab
  - VMware
tags:
  - IPMI
  - SuperMicro
  - Zabbix
---
At home I have a SuperMicro <a href="http://www.supermicro.com/products/motherboard/qpi/5500/x8dtu-f.cfm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.supermicro.com/products/motherboard/qpi/5500/x8dtu-f.cfm']);">X8DTU-F</a> server and I noticed that it has a dedicated NIC for *IPMI* (Intelligent Platform Management Interface).

### Enable IPMI on SuperMicro

The process is described in this <a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/Manual_IPMI.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/12/Manual_IPMI.pdf']);">pdf</a>. If you want to be able to use KVM (Keyboard-Video-Mouse) over LAN, make sure you follow the **Enabling COM Port for SOL (IPMI)** section. All the settings were already enabled on my system, all I had to do was assign the IPMI a static IP. Here are the BIOS settings, after I was done:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/IPMI_static_IP_g.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/IPMI_static_IP_g.jpg']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/IPMI_static_IP_g-1024x705.jpg" alt="IPMI static IP g 1024x705 Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="620" height="426" class="alignnone size-large wp-image-9893" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

I then plugged in an RJ45 Cable into the switch and the IPMI interface and I was able to ping the interface. Now upon pointing the browser to the IP, I was able to see the login page to the IPMI management console:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-login-page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-login-page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-login-page.png" alt="ipmi login page Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="944" height="379" class="alignnone size-full wp-image-9870" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Another quick test would be to use the **ipmitool** utility to query the sensor information. I first installed the utility on my Debian machine:

    $ sudo apt-get install ipmitool
    

and then I was successfully able to query the IPMI interface:

    $ ipmitool -H 192.168.1.110 -U ADMIN -P ADMIN sdr
    CPU1 Temp        | 0 unspecified     | ok
    CPU2 Temp        | 0 unspecified     | ok
    System Temp      | 63 degrees C      | ok
    CPU1 Vcore       | 0.88 Volts        | ok
    CPU2 Vcore       | 0.90 Volts        | ok
    +5V              | 5.06 Volts        | ok
    +5VSB            | 5.09 Volts        | ok
    +12V             | 12.19 Volts       | ok
    -12V             | -11.80 Volts      | ok
    +3.3V            | 3.24 Volts        | ok
    +3.3VSB          | 3.29 Volts        | ok
    VBAT             | 3.26 Volts        | ok
    Fan1             | 6480 RPM          | ok
    Fan2             | 6480 RPM          | ok
    Fan3             | 6480 RPM          | ok
    Fan4             | 6480 RPM          | ok
    Fan5             | no reading        | ns
    Fan6             | no reading        | ns
    Fan7             | no reading        | ns
    Fan8             | no reading        | ns
    P1-DIMM1A Temp   | 44 degrees C      | ok
    P1-DIMM1B Temp   | no reading        | ns
    P1-DIMM2A Temp   | 45 degrees C      | ok
    P1-DIMM2B Temp   | no reading        | ns
    P1-DIMM3A Temp   | 46 degrees C      | ok
    P1-DIMM3B Temp   | no reading        | ns
    P2-DIMM1A Temp   | 34 degrees C      | ok
    P2-DIMM1B Temp   | no reading        | ns
    P2-DIMM2A Temp   | 35 degrees C      | ok
    P2-DIMM2B Temp   | no reading        | ns
    P2-DIMM3A Temp   | 35 degrees C      | ok
    P2-DIMM3B Temp   | no reading        | ns
    Intrusion        | 0 unspecified     | ok
    PS Status        | 0 unspecified     | nc
    

### Updating IPMI Firmware

I realized the IPMI firmware was out of date, so I downloaded the latest one from <a href="http://www.supermicro.com/support/bios/firmware.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.supermicro.com/support/bios/firmware.aspx']);">here</a>. The latest version at the time of writing this post is the following one:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/firmware-update-site.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/firmware-update-site.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/firmware-update-site.png" alt="firmware update site Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="519" height="363" class="alignnone size-full wp-image-9871" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

After you download the *zip* archive, you can extract it. Here are the contents of the archive:

    $ unzip X8DTU220.zip 
    Archive:  X8DTU220.zip
      inflating: X8DTU220.ima            
      inflating: DOS 2.4.zip             
      inflating: Linux 2.4.zip           
      inflating: Windows 2.4.zip         
      inflating: IPMI Firmware Update.doc 
    

The instructions on how to update the firmware are in the document from the archive. The gist of it, go to the **maintenance** tab in the IPMI management console and click **Update Firmare**. Then upload the **.ima** file for the update. Also during the update, make sure you un-check the &#8220;**Preserve Configuration**&#8221; setting (this will wipe all the settings to default, but is necessary for the update). Then start the update, here is how the update process looked like for me:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-fw-update.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-fw-update.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-fw-update.png" alt="ipmi fw update Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="1091" height="248" class="alignnone size-full wp-image-9872" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

After that the system information looked up-to-date:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-sys-infor.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-sys-infor.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-sys-infor.png" alt="ipmi sys infor Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="363" height="183" class="alignnone size-full wp-image-9873" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Since the update wipes all the settings, I actually had to go check out my router to find out which DHCP address IPMI grabbed. After I figured that out, I just pointed to that IP in the browser and re-configured all the static IP settings.

### Update BIOS using the IPMI KVM

While I was at it, I decided to update the BIOS as well. I downloaded the new BIOS from <a href="http://www.supermicro.com/support/resources/results.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.supermicro.com/support/resources/results.aspx']);">here</a>. At the time of writing here is the latest version:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/bios-update-super.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/bios-update-super.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/bios-update-super.png" alt="bios update super Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="488" height="351" class="alignnone size-full wp-image-9874" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Checking out the contents of the archive, I saw the following:

    $ unzip X8DTU2_803.zip 
    Archive:  X8DTU2_803.zip
       creating: X8DTU2.803/
      inflating: X8DTU2.803/AFUDOS.smc   
      inflating: X8DTU2.803/ami.bat      
      inflating: X8DTU2.803/Readme for AMI BIOS.txt  
      inflating: X8DTU2.803/X8DTU2.803   
    

The **Readme** had the following instructions:

> b). Extract the files to a DOS bootable device (such as a bootable USB stick, or CD).  
> c). Boot to a DOS prompt and type AMI.BAT filename.xxx.(example AMI.BAT X8DT30.311)

Initially I wanted to create a bootable ISO with a size of a floppy image (the process to do that is described <a href="http://www.nenie.org/misc/flashbootcd.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nenie.org/misc/flashbootcd.html']);">here</a> and <a href="http://idolinux.blogspot.com/2009/10/create-dos-boot-disk-for-cd-or-grub.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://idolinux.blogspot.com/2009/10/create-dos-boot-disk-for-cd-or-grub.html']);">here</a>). The IPMI KVM allows to upload up to the floppy image size:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-virtua-media.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-virtua-media.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-virtua-media.png" alt="ipmi virtua media Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="1256" height="160" class="alignnone size-full wp-image-9875" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

As I was creating the ISO, I realized the size of the BIOS update is bigger than 1.44M:

    $ ls -lh
    total 4.2M
    -r--r--r-- 1 elatov elatov 151K Dec 13  2011 AFUDOS.smc
    -rw-rw-r-- 1 elatov elatov  112 May 22  2012 ami.bat
    -rw-rw-r-- 1 elatov elatov 1.2K Jul 11  2011 Readme for AMI BIOS.txt
    -rw-rw-r-- 1 elatov elatov 4.0M Aug  3  2012 X8DTU2.803
    

It&#8217;s about 4M.

#### Create a DOS Bootable Flash Drive

At this point, I had two choices: create an ISO with a bigger size and share it via Samba or create an ISO and just use my USB stick. I have gone without a samba share all this time, and I didn&#8217;t want to set one up just for a BIOS update (but I was still impressed with the fact that IPMI can connect to a samba share). There is a Russian site which provides custom sized images. <a href="http://bootcd.narod.ru/images.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bootcd.narod.ru/images.htm']);">Here</a> is a link to that site and here is a list of all their images:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/custom-size-images-rus.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/custom-size-images-rus.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/custom-size-images-rus.png" alt="custom size images rus Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="993" height="580" class="alignnone size-full wp-image-9876" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

All the images for CDs and I wanted to get one specific for a USB drive. It probably doesn&#8217;t make a difference, but I later ran into FreeDOS and they provided an image specifically for a USB Drive. <a href="http://chtaube.eu/computers/freedos/bootable-usb/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://chtaube.eu/computers/freedos/bootable-usb/']);">Here</a> is a link to the site and here is a list of images:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos_boot-usb.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos_boot-usb.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos_boot-usb.png" alt="freedos boot usb Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="1112" height="373" class="alignnone size-full wp-image-9877" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

So I backed up my USB drive and then I ran the following to put the FreeDOS image on it:

    $ wget http://ftp.chtaube.eu/pub/FreeDOS/bootable-usb/FreeDOS-1.1-memstick-3-30M.img.bz2
    $ bunzip2 FreeDOS-1.1-memstick-3-30M.img.bz2
    $ sudo dd if=FreeDOS-1.1-memstick-3-30M.img of=/dev/sdb bs=512k
    

and that was it. I then mounted the drive and copied all the SuperMicro BIOS updates to the drive:

    $ sudo mount /dev/sdb1 /mnt/usb
    

After it&#8217;s mounted we can see that it&#8217;s a **vfat** filesystem:

    $df -hT | grep usb
    /dev/sdb1           vfat       29M  7.8M   21M  28% /mnt/usb
    

We can also see that it&#8217;s FAT 16:

    $ sudo fdisk -l /dev/sdb
    
    Disk /dev/sdb: 8004 MB, 8004304896 bytes, 15633408 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: dos
    Disk identifier: 0x000615e8
    
       Device Boot      Start         End      Blocks   Id  System
    /dev/sdb1   *           1       58593       29296+   e  W95 FAT16 (LBA)
    

Then finally I copied the files onto the USB drive:

    $ sudo rsync -rvzP X8DTU2.803/. /mnt/usb/.
    sending incremental file list
    AFUDOS.smc
          154432 100%   16.58MB/s    0:00:00 (xfer#1, to-check=3/5)
    Readme for AMI BIOS.txt
            1170 100%  163.23kB/s    0:00:00 (xfer#2, to-check=2/5)
    X8DTU2.803
         4194304 100%   31.25MB/s    0:00:00 (xfer#3, to-check=1/5)
    ami.bat
             112 100%    0.85kB/s    0:00:00 (xfer#4, to-check=0/5)
    
    sent 1075151 bytes  received 88 bytes  2150478.00 bytes/sec
    total size is 4350018  speedup is 4.05
    

And that&#8217;s it. I then un-mounted the usb drive, unplugged it from my laptop, and plugged into the SuperMicro Server.

#### Update BIOS Process

I logged into the IPMI Management console and went to the **Remote Control** tab:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/remote-control-tab-ipmi.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/remote-control-tab-ipmi.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/remote-control-tab-ipmi.png" alt="remote control tab ipmi Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="382" height="329" class="alignnone size-full wp-image-9878" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Upon clicking **Remote Console**, I saw the server:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/jviewer-started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/jviewer-started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/jviewer-started.png" alt="jviewer started Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="1051" height="401" class="alignnone size-full wp-image-9879" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

I then put the host into maintenance mode and rebooted the server. Upon boot, I made sure it&#8217;s booting from the USB. After it booted from the USB, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos-booted.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos-booted.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/freedos-booted.png" alt="freedos booted Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="648" height="428" class="alignnone size-full wp-image-9880" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

I then started the BIOS update:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/start-bios-update.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/start-bios-update.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/start-bios-update.png" alt="start bios update Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="642" height="426" class="alignnone size-full wp-image-9881" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

After a couple of minutes the BIOS update finished:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/bio-update-done.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/bio-update-done.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/bio-update-done.png" alt="bio update done Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="728" height="429" class="alignnone size-full wp-image-9882" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

That should be it. You can reboot the server by sending a **Ctr-Alt-Del**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/send-cad_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/send-cad_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/send-cad_g.png" alt="send cad g Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="381" height="371" class="alignnone size-full wp-image-9883" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

### Send IPMI Alerts Through an SMTP server

The IPMI has the capability to send email alerts. To set this up you need to have an SMTP server (which I already had). From the IPMI Management Console go to the **Configuration** tab and click on **SMTP**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/impi-config-tab.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/impi-config-tab.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/impi-config-tab.png" alt="impi config tab Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="441" height="593" class="alignnone size-full wp-image-9884" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Then configure your SMTP server settings:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/smtp-settings-impi.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/smtp-settings-impi.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/smtp-settings-impi.png" alt="smtp settings impi Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="234" height="195" class="alignnone size-full wp-image-9885" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Then under the **Configuration** tab click on **Alerts** and select the level of alerts that you want sent (I setup informational and above):

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/alerts-impi.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/alerts-impi.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/alerts-impi.png" alt="alerts impi Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="545" height="194" class="alignnone size-full wp-image-9886" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

That should be it. If you want to make sure your SMTP configuration is working, under **alerts** you can click on &#8220;**Send Test Alert**&#8221; and make sure you get an email.

### Monitor IPMI Sensors with Zabbix

Surprisingly there is no IPMI SuperMicro Template, so I ended up creating my items manually. First create a host and select the IPMI interface:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/zabbix-impi-interfaces.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/zabbix-impi-interfaces.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/zabbix-impi-interfaces.png" alt="zabbix impi interfaces Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="844" height="188" class="alignnone size-full wp-image-9887" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Enter the credentials to login into the IPMI system. Here is how my IPMI tab looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-tab-zabbix.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-tab-zabbix.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/ipmi-tab-zabbix.png" alt="ipmi tab zabbix Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="383" height="264" class="alignnone size-full wp-image-9901" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

Then create an item for that host and under the **IPMI Sensor** put in the value that you see under the **ipmitool** output:

    $ ipmitool -H ipmi -U ADMIN -P ADMIN sensor
    CPU1 Temp        | 0x0        | discrete   | 0x0000| na        | na        | na        | na        | na        | na        
    CPU2 Temp        | 0x0        | discrete   | 0x0000| na        | na        | na        | na        | na        | na        
    System Temp      | 64.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 77.000    | 79.000    
    CPU1 Vcore       | 0.880      | Volts      | ok    | 0.808     | 0.816     | 0.824     | 1.352     | 1.360     | 1.368     
    CPU2 Vcore       | 0.896      | Volts      | ok    | 0.808     | 0.816     | 0.824     | 1.352     | 1.360     | 1.368     
    +5V              | 5.056      | Volts      | ok    | 4.416     | 4.448     | 4.480     | 5.536     | 5.568     | 5.600     
    +5VSB            | 5.088      | Volts      | ok    | 4.416     | 4.448     | 4.480     | 5.536     | 5.568     | 5.600     
    +12V             | 12.190     | Volts      | ok    | 10.600    | 10.653    | 10.706    | 13.250    | 13.303    | 13.356    
    -12V             | -11.804    | Volts      | ok    | -13.550   | -13.356   | -13.162   | -10.834   | -10.640   | -10.446   
    +3.3V            | 3.240      | Volts      | ok    | 2.880     | 2.904     | 2.928     | 3.648     | 3.672     | 3.696     
    +3.3VSB          | 3.288      | Volts      | ok    | 2.880     | 2.904     | 2.928     | 3.648     | 3.672     | 3.696     
    VBAT             | 3.264      | Volts      | ok    | 2.880     | 2.904     | 2.928     | 3.648     | 3.672     | 3.696     
    Fan1             | 6480.000   | RPM        | ok    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan2             | 6480.000   | RPM        | ok    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan3             | 6480.000   | RPM        | ok    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan4             | 5940.000   | RPM        | ok    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan5             | na         | RPM        | na    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan6             | na         | RPM        | na    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan7             | na         | RPM        | na    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    Fan8             | na         | RPM        | na    | 405.000   | 540.000   | 675.000   | 34155.000 | 34290.000 | 34425.000 
    P1-DIMM1A Temp   | 44.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P1-DIMM1B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P1-DIMM2A Temp   | 46.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P1-DIMM2B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P1-DIMM3A Temp   | 46.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P1-DIMM3B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM1A Temp   | 35.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM1B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM2A Temp   | 35.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM2B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM3A Temp   | 36.000     | degrees C  | ok    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    P2-DIMM3B Temp   | na         | degrees C  | na    | -9.000    | -7.000    | -5.000    | 75.000    | 80.000    | 85.000    
    Intrusion        | 0.000      | unspecified | ok    | na        | na        | na        | na        | na        | na        
    PS Status        | 0.000      | unspecified | nc    | na        | na        | na        | na        | na        | na   
    

To make sure you get the right Sensor, you can do a **get** on it, like so:

    $ ipmitool -H ipmi -U ADMIN -P ADMIN sensor get "System Temp"
    Locating sensor record...
    Sensor ID              : System Temp (0x3)
     Entity ID             : 7.1
     Sensor Type (Analog)  : Temperature
     Sensor Reading        : 65 (+/- 0) degrees C
     Status                : ok
     Lower Non-Recoverable : -9.000
     Lower Critical        : -7.000
     Lower Non-Critical    : -5.000
     Upper Non-Critical    : 75.000
     Upper Critical        : 77.000
     Upper Non-Recoverable : 79.000
     Assertion Events      : 
     Assertions Enabled    : lnc- lcr- lnr- unc+ ucr+ unr+ 
     Deassertions Enabled  : lnc- lcr- lnr- unc+ ucr+ unr+ 
    

Here is what I entered to define the **System Temp** item in **zabbix**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/system-temp-item-zabbix.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/system-temp-item-zabbix.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/system-temp-item-zabbix.png" alt="system temp item zabbix Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="483" height="166" class="alignnone size-full wp-image-9888" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

After I was done adding all the Fans and Temperatures, I was able to see the graphs:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/12/cpu-plot-ipmi-zabbix.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/12/cpu-plot-ipmi-zabbix.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/12/cpu-plot-ipmi-zabbix.png" alt="cpu plot ipmi zabbix Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" width="887" height="450" class="alignnone size-full wp-image-9889" title="Configure IPMI On SuperMicro Server and Monitor IPMI Sensors with Zabbix" /></a>

If you want to be able to get discrete values you have to use zabbix 2.1. Here is an example of a discrete value:

    $ ipmitool -H ipmi -U ADMIN -P ADMIN sensor get "CPU1 Temp"
    Locating sensor record...
    Sensor ID              : CPU1 Temp (0x1)
     Entity ID             : 3.1
     Sensor Type (Discrete): Unknown (0xC0)
    

There is a bug on it, <a href="https://support.zabbix.com/browse/ZBXNEXT-300" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://support.zabbix.com/browse/ZBXNEXT-300']);">here</a> is a link to the bug. You can use a temporary workaround described in <a href="http://lab4.org/wiki/Zabbix_Items_Daten_per_IMPI_sammeln" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://lab4.org/wiki/Zabbix_Items_Daten_per_IMPI_sammeln']);">this</a> German site.

### CIM on ESXi

ESXi comes with a CIM agent. You can use the **cim-diagnostic.sh** script to check for IPMI sensors like so:

    ~ # cim-diagnostic.sh | sed -n '/^OMC_NumericSensor/,/^$/p' | grep -E " Name =| CurrentReading ="
                              Name = P2-DIMM3A Temp(106.0.32.99)
                    CurrentReading = 3600
                              Name = P2-DIMM2A Temp(104.0.32.99)
                    CurrentReading = 3600
                              Name = P2-DIMM1A Temp(102.0.32.99)
                    CurrentReading = 3500
                              Name = P1-DIMM3A Temp(100.0.32.99)
                    CurrentReading = 4700
                              Name = P1-DIMM2A Temp(98.0.32.99)
                    CurrentReading = 4600
                              Name = P1-DIMM1A Temp(96.0.32.99)
                    CurrentReading = 4500
                              Name = Fan4(17.0.32.99)
                    CurrentReading = 648000
                              Name = Fan3(16.0.32.99)
                    CurrentReading = 648000
                              Name = Fan2(15.0.32.99)
                    CurrentReading = 648000
                              Name = Fan1(14.0.32.99)
                    CurrentReading = 648000
                              Name = VBAT(13.0.32.99)
                    CurrentReading = 326
                              Name = +3.3VSB(12.0.32.99)
                    CurrentReading = 328
                              Name = +3.3V(11.0.32.99)
                    CurrentReading = 324
                              Name = -12V(10.0.32.99)
                    CurrentReading = -1180
                              Name = +12V(9.0.32.99)
                    CurrentReading = 1218
                              Name = +5VSB(8.0.32.99)
                    CurrentReading = 508
                              Name = +5V(7.0.32.99)
                    CurrentReading = 505
                              Name = CPU2 Vcore(5.0.32.99)
                    CurrentReading = 89
                              Name = CPU1 Vcore(4.0.32.99)
                    CurrentReading = 88
                              Name = System Temp(3.0.32.99)
                    CurrentReading = 6500
    

