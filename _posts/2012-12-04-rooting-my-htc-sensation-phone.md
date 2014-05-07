---
title: Rooting my HTC Sensation Phone
author: Karim Elatov
layout: post
permalink: /2012/12/rooting-my-htc-sensation-phone/
dsq_thread_id:
  - 1405469582
categories:
  - Home Lab
  - OS
tags:
  - adb backup
  - bootloader
  - ClockWorkMod Recovery
  - ControlBear
  - fastboot
  - HTC CID
  - HTC Sensation
  - S-OFF
  - Wire Trick
---
I wanted to root my HTC Sensation phone, since I have been putting it off for a while. I read some good guides on how to do it, here is a list:

1.  &#8220;<a href="http://www.androidauthority.com/how-to-root-htc-sensation-21697/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.androidauthority.com/how-to-root-htc-sensation-21697/']);">How to Root Your HTC Sensation</a>&#8221; 
2.  &#8220;<a href="http://how2rootandroiddevices.blogspot.com/2012/06/how-to-root-htc-sensation-4g.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://how2rootandroiddevices.blogspot.com/2012/06/how-to-root-htc-sensation-4g.html']);">How to Root HTC Sensation 4G</a>&#8221; 
3.  &#8220;<a href="http://www.blogotechblog.com/2012/04/how-to-root-htc-sensationsensation-xe-running-ice-cream-sandwich/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.blogotechblog.com/2012/04/how-to-root-htc-sensationsensation-xe-running-ice-cream-sandwich/']);">How To Root HTC Sensation/Sensation XE Running Ice Cream Sandwich</a>&#8221; 

### 1. Create Backups

Most of the above links, of course, recommended backing up your data just in case. They recommended using &#8220;Titanimum Backup&#8221; and other solutions as well. But all the tools required the phone to be rooted already. What a &#8216;Catch 22&#8242; situation. So then I ran into <a href="http://blog.shvetsov.com/2012/09/backup-your-android-without-root-or.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.shvetsov.com/2012/09/backup-your-android-without-root-or.html']);">this</a> post, it&#8217;s about creating a back up without using any external apps. Starting with Android 4.0 (Ice Cream Sandwich) you can use *adb backup* to create a backup of your applications and data. Here is what I ran:

    [elatov@klaptop platform-tools]$ ./adb backup -f ~/phone/backup -apk -shared -all -nosystem
    Now unlock your device and confirm the backup operation.
    

I then went to my phone and saw the following screen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/12/phone_backup.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/12/phone_backup.png']);"><img class="alignnone size-full wp-image-5096" title="phone_backup" src="http://virtuallyhyper.com/wp-content/uploads/2012/12/phone_backup.png" alt="phone backup Rooting my HTC Sensation Phone" width="540" height="960" /></a>

I didn&#8217;t enter any password and just hit &#8220;Back up my data&#8221; and the back up process started. In the end, I had the following:

    [elatov@klaptop phone]$ ls -lh
    total 867M
    -rw-r----- 1 elatov elatov 867M Dec  1 13:21 backup
    

I really wanted to find out if the backups were valid. I then ran into <a href="http://nelenkov.blogspot.com/2012/06/unpacking-android-backups.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://nelenkov.blogspot.com/2012/06/unpacking-android-backups.html']);">this</a> blog. It had a very in depth description of how the back up process works and what encryption algorithms are used. It also had a command on how to convert the android backup to a tar file. Here is the command I ran to convert the backup:

    [elatov@klaptop phone]$ dd if=backup bs=1 skip=24 | openssl zlib -d > mybackup.tar
    3078081068:error:29065064:lib(41):BIO_ZLIB_READ:zlib inflate error:c_zlib.c:570:zlib error:data error
    

At first it failed. I later found a couple of documents that mentioned that there was a bug with the back up utility prior to an update of 4.0.4. I was running 4.0.3, so I was probably running into that. The bug manifests it self, when you include *shared* data (contents of the SD-card) with the *adb backup* command. I then made another backup and didn&#8217;t included the SD-card contents and then trying to convert that backup, it was successful:

    [elatov@klaptop phone]$ dd if=backup2 bs=1 skip=24 | openssl zlib -d > mybackup2.tar
    144560293+0 records in
    144560293+0 records out
    144560293 bytes (145 MB) copied, 510.611 s, 283 kB/s
    

There is also a java application called &#8220;Android Backup Extractor&#8221;. Here is <a href="https://github.com/nelenkov/android-backup-extractor" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/nelenkov/android-backup-extractor']);">link</a> to that. And someone also wrote a Perl script to &#8220;decrypt&#8221; the back up. Here is a <a href="http://forum.xda-developers.com/showthread.php?t=1730309" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.xda-developers.com/showthread.php?t=1730309']);">link</a> to that forum. From the last link they also mention the bug that I ran into:

> I had ran into issues with ADB backups performed under Android 4.0.4 before the JB upgrade (on a Samsung Galaxy Nexus).I did include the shared storage (accidentally or intentionally I don&#8217;t remember) and I ran into this bug (Android issue 28303)

I was just happy to know that I have a valid backup and that I could confirm the data. I then mounted the SD-card from my phone to my laptop and created a manual backup of that, just in case. Here are the commands that I ran on my laptop to get a backup of my SD-card (after I mounted it from my phone):

    $ sudo mount /dev/sdb /mnt/usb/
    $ tar cpvjf ~/phone/phone_sd-card.tar.bz2 /mnt/usb 
    

At the end of the backing up, I had the following files:

    [elatov@klaptop phone]$ ls
    backup  backup2  mybackup2.tar  phone_sd_card_sensation.tar.bz2
    

I then realized that the &#8220;rooting&#8221; steps above are for anyone that has not updated to 4.0.3 ICS, and I unfortunately had already done that. So I found other links, cause the instructions are different. Here are some of the links:

*   &#8220;<a href="http://forum.xda-developers.com/showthread.php?t=1870233" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.xda-developers.com/showthread.php?t=1870233']);">How to Root & S-OFF HTC Sensation &#8211; HBOOT 1.27.0000 & Firmware 3.33!</a>&#8220;
*   &#8220;<a href="http://www.techsliver.com/how-to-s-off-root-flash-cwm-recovery-on-htc-sensation-with-hboot-1-27-0000/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.techsliver.com/how-to-s-off-root-flash-cwm-recovery-on-htc-sensation-with-hboot-1-27-0000/']);">How To S-OFF, Root, Flash CWM Recovery On HTC Sensation With HBoot 1.27.0000</a>&#8221; 

I followed mostly the last one.

### 2. Unlock Bootloader, following instructions on http://htcdev.com/bootloader

The website provides their own &#8216;fastboot&#8217; binary. Then you run this:

    [elatov@klaptop downloads]$ chmod +x fastboot
    [elatov@klaptop downloads]$ ./fastboot oem get_identifier_token
    ... INFO
    INFO< Please cut following message >
    INFO< <<< Identifier Token Start >>>>
    INFO015F2941DC2640329F933BC106BA9D94
    INFO18F8DD2079275116654C2BD4E0FFA8D7
    INFOAFD7A21C8xxxxxxxxxxxxxxxxxxxxxxx
    INFOD47D85A7D1EFD4698E698485E53B32FE
    INFO24F6F97A3ABExxxxxxxxxxxxxxxxxxxx
    INFO6F58AE3F5C0896BA0C258425B8269F82
    INFOF6DB54148436D287F891455B6382FF94
    INFO75C5D740xxxxxxxxxxxxxxxxxxxxxxxx
    INFO0C5F7E92FA3F88398E10711751061834
    INFOE6BDD3E04206F8CEF9D7881469C9E70C
    INFO0697454BFF1F95EDA2E7B9AE146547A2
    INFO621A2CAAFD826AEDA17C591ADCC9B784
    INFO2CDD8A592A8B212C8F5C7357A570D2AF
    INFO2E90DA3FC0DF5E5C1CD243D01B6BF751
    INFOExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    INFOxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    INFO< <<<< Identifier Token End >>>>>
    OKAY
    [elatov@klaptop downloads]$
    

You can then upload the above output to their site and they will provide a *.bin* file to unlock your bootloader with the following command:

    [elatov@klaptop downloads]$ ./fastboot  flash unlocktoken Unlock_code.bin
    sending 'unlocktoken' (0 KB)... OKAY
    writing 'unlocktoken'... INFOunlock token check successfully
    OKAY
    

### 3. Install ClockWorkMod Recovery Using Android SDK

Download the \*.img \* file and then run the following to install the image:

    [elatov@klaptop platform-tools]$ ./fastboot flash recovery ~/downloads/recovery.img
    sending 'recovery' (4876 KB)...
    OKAY [  1.160s]
    writing 'recovery'...
    OKAY [ 10.433s]
    finished. total time: 11.594s
    

### 4. Install SuperSU by uploading it to the SD-Card, and then using the ClockWorkMod Recovery to install it

It took a while to find the latest version since the above site had an expired link. But after some *googling* around I found the latest version from <a href="http://www.androidtotal.com/root-install-clockworkmod-recovery-on-htc-sensation-with-android-4.0.3-hboot-1.27.000/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.androidtotal.com/root-install-clockworkmod-recovery-on-htc-sensation-with-android-4.0.3-hboot-1.27.000/']);">here</a>. After you have the file, do the following to install it:

*   Upload the file onto the SD-card.
*   Boot into CWM Recovery.
*   Select install Zip File from SD-card.

### 5. Follow instructions laid out in http://unlimited.io/juopunutbear.htm to turn S-OFF with the &#8220;wire trick&#8221;

Here is how wire trick looked like from the terminal:

    [elatov@klaptop bear]$ sudo ./ControlBear
    ========= ControlBear 0.11 beta for JuopunutBear S-OFF ==========
                  (c) Copyright 2012 Unlimited.IO
          If you have acquired this software from anywhere
          other than our website this version may be out of
          date and unsupported. Please see our website for
        instructions on how to use this tool and for support.
     This program may not be redistributed or included in other
       works without the express permission of Team Unlimited.
    
             www.unlimited.io    |    team'@'unlimited.io
    
    Starting up......
    Testing ADB connection
    Test 1: Rebooting into bootloader
    Waiting fastboot (19/60)
    Waiting.....
    Test 2: Booting device into JuopunutBear boot-mode
    Waiting ADB.... (7/60)
    Device detected.....................
    Connection test ok!
    Searching device.....
    Found device.....
    Backing up......
    Transferring backups....
    Backup ok!!
    Using eMMC dev /dev/block/mmcblk0
    Using MMC dev /dev/block/mmcblk1
    Boot partition is /dev/block/mmcblk0p20
    Recovery partition is /dev/block/mmcblk0p21
    Is information correct?
    You have 5 seconds time to stop process by pressing CTRL+C
    Finding some beer.....
    Found first....
    Found second....
    Found third....
    Hmmmm... where is that last one....... Wait a sec....
    Found fourth....
    Rebooting.......
    === Waiting for device....
    (7/45)
    Found device...
    Waiting for device to settle... Please wait...
    Making room for beer......
    Loading sixpacks on sdcard......
    Loaded......
    Do not remove sdcard from phone
    Do wire-trick now!! Check the instructions at http://unlimited.io
    
    === Waiting for device....
    (11/45)
    Found device...
    Waiting for device to settle... Please wait...
    Getting into bar.....
    Raising Glass
    SUCCESS - Taking a sip.
    SUCCESS - Beer is tasty.
    SUCCESS - Beer is tasty.
    SUCCESS - Beer is tasty.
    SUCCESS - Beer is tasty.
    SUCCESS - Buddies and Beer
    Checking alcohol level......
    Seems to be just right.....
    Let's take one more......
    Aaaah, nice sunny day!!
    Rebooting.......
    === Waiting for device....
    (5/45)
    Found device...
    Waiting for device to settle... Please wait...
    Beer......more beer......more beer...
    Rebooting RUU mode.......
    === Waiting for device....
    (1/45)
    Fastboot detected
    JuopunutBear S-OFF success
    Installing JuopunutBear hboot.....
    Waiting.....
    Flashing.......
    Rebooting......
    JuopunutBear hboot installed
    

### 6. Change CID, so you can install any ROM on your device

All the sites had the same instructions. Here is what I did to accomplish that:

    [elatov@klaptop platform-tools]$ ./adb reboot-bootloader
    [elatov@klaptop platform-tools]$ ./fastboot devices
    HT164T500742    fastboot
    [elatov@klaptop platform-tools]$ ./fastboot getvar cid
    cid: T-MOB010
    finished. total time: 0.002s
    [elatov@klaptop platform-tools]$ ./fastboot oem writecid 11111111
    ...
    (bootloader) Start Verify: 0
    (bootloader) erase sector 65504 ~ 65535 (32)
    (bootloader) mipi_dsi_cmd_config:panel_id=0x940021
    (bootloader) width=540 height=960
    (bootloader) mipi_dsi_cmd_config:panel_id=0x940021
    (bootloader) width=540 height=960
    OKAY [  0.179s]
    finished. total time: 0.180s
    [elatov@klaptop platform-tools]$ ./fastboot reboot-bootloader
    rebooting into bootloader...
    OKAY [  3.312s]
    finished. total time: 3.313s
    [elatov@klaptop platform-tools]$ ./fastboot getvar cid
    cid: 11111111
    finished. total time: 0.002s
    [elatov@klaptop platform-tools]$ ./fastboot reboot
    rebooting...
    
    finished. total time: 1.661s
    

### 7. Pick a custom ROM and install it.

&#8220;<a href="http://www.lifehacker.com.au/2012/06/five-best-android-roms/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.lifehacker.com.au/2012/06/five-best-android-roms/']);">Five Best Android ROMs</a>&#8221; and &#8220;<a href="http://tips4droid.com/top-5-custom-rom-for-htc-rezound/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://tips4droid.com/top-5-custom-rom-for-htc-rezound/']);">Top 5 Custom ROM for HTC Rezound</a>&#8221; talk about the different ROMs. I know that Cyanogen is pretty popular and I have used it with my previous phone. There is also the &#8220;Android Revolution HD&#8221;. All of the instructions on how to install Revolution HD, can be found <a href="http://forum.xda-developers.com/showthread.php?t=1098849" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.xda-developers.com/showthread.php?t=1098849']);">here</a> and also <a href="http://www.techsliver.com/step-by-step-guide-on-how-to-install-android-revolution-hd-6.4.0-ics-rom-on-htc-sensation-4g/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.techsliver.com/step-by-step-guide-on-how-to-install-android-revolution-hd-6.4.0-ics-rom-on-htc-sensation-4g/']);">here</a>. Doing some research it seemed that the Revolution HD looks exactly the same as ICS and it&#8217;s just over clocked for performance and has a great battery life. I wanted to try out another interface so I decided to go with CyanogenMod. Instructions on how to install that can be found <a href="http://wiki.cyanogenmod.org/w/Install_CM_for_pyramid" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.cyanogenmod.org/w/Install_CM_for_pyramid']);">here</a>. Here is a concise list of instructions:

1.  Download the latest CyanogenMod 9 ROM to your computer
2.  Download the latest Google Apps package
3.  Copy the latest CyanogenMod 9 ROM and the Google Apps ZIP files to the root of your HTC Sensation’s SD-card.
4.  Boot into ClockWorkMod Recovery
5.  Make a Nandroid backup of your current ROM by selecting Backup and Restore > Backup.
6.  Select Wipe Data/Factory Reset.
7.  Select the option to Wipe cache partition.
8.  Select Install ZIP from SD-Card > Choose ZIP from SD-Card. Select the latest CyanogenMod 9 ROM.
9.  Select Install ZIP from SD-Card > Choose ZIP from SD-Card again and select the Google Apps package.
10. Reboot the phone. 

After I rebooted I had a brand new Interface to play with; I liked the look.

### 8. Restore Back&#8217;ed up Applications

I then decided to see if my restore would work out. So I connected my phone to laptop and ran the following:

    elatov@klaptop platform-tools]$ ./adb restore ~/phone/backup2 
    Now unlock your device and confirm the restore operation.
    

Then opened up my phone and it asked to allow the restore process and I did. I must say, even though with the back up process it&#8217;s all or nothing (you can&#8217;t choose what apps to restore), the restore went very well. I was able to start up all of my old applications without any issues.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/12/rooting-my-htc-sensation-phone/" title=" Rooting my HTC Sensation Phone" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:adb backup,bootloader,ClockWorkMod Recovery,ControlBear,fastboot,HTC CID,HTC Sensation,S-OFF,Wire Trick,blog;button:compact;">I wanted to root my HTC Sensation phone, since I have been putting it off for a while. I read some good guides on how to do it, here is...</a>
</p>