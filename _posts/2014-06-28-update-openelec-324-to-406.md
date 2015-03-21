---
published: true
layout: post
title: "Update OpenELEC 3.2.4 to 4.0.6"
author: Karim Elatov
description: ""
categories: [os]
tags: [linux,openelec,raspberry_pi,xbmc]
---

I noticed that there was a new version of OpenELEC, so I decided to give it a try. From their [release](http://openelec.tv/news/22-releases/125-openelec-4-0-released) page, it doesn't look you can do an automatic update and it's recommended to do a manual update:

> ####How To Upgrade To OpenELEC 4.0 Release
> If you are going to update from one of our older releases, we STRONGLY advise that you make a backup of your XBMC data and manual update . There was reports regarding new database versions, settings, addons and addon repos, which can cause issues if you are using updating from OpenELEC 3.2 or older. You can use our OpenELEC Settings addon if you are using OpenELEC-3.2 to backup your data and then reset it. If you are on an older build, you will need to do this manually:
> 
> 	mv /storage/.xbmc /storage/.xbmc-backup

And from the [update](http://wiki.openelec.tv/index.php/Updating_OpenELEC#Manually_Updating_OpenELEC) page, here are the instructions for the actual update:

> #### Copying the Update Files
> 
> To update you must download the corresponding install depending on your hardware. To download click here. If you are unsure which version you need, click here.
> 
> When you download the file you will be presented with a **.tar** file. You will need to extract this tar file and get the four files int the target folder (**SYSTEM** **KERNEL** **SYSTEM.md5** **KERNEL.md5**).

### Updating OpenELEC to 4.0
After I downloaded the latest version, I had the following:

	elatov@crbook:~$ls -lh download/*.tar
	-rw-r--r-- 1 elatov elatov 108M Jun 27 22:30 download/l/OpenELEC-RPi.arm-4.0.6.tar
	
Then extracting the **tar** file, I had the following files:

	elatov@crbook:~/download$tree OpenELEC-RPi.arm-4.0.6
	OpenELEC-RPi.arm-4.0.6
	├── 3rdparty
	│   └── bootloader
	│       ├── bootcode.bin
	│       ├── config.txt
	│       ├── fixup.dat
	│       ├── LICENCE.broadcom
	│       └── start.elf
	├── CHANGELOG
	├── create_sdcard
	├── INSTALL
	├── licenses
	│   ├── APSL.txt
	│   ├── Artistic.txt
	│   ├── ATI.txt
	│   ├── BSD_2_Clause.txt
	│   ├── BSD_3_Clause.txt
	│   ├── BSD_4_Clause.txt
	│   ├── BSD.txt
	│   ├── Clarified_Artistic.txt
	│   ├── FDL1_2.txt
	│   ├── FDL1_3.txt
	│   ├── FDL.txt
	│   ├── GPL2.txt
	│   ├── GPL3.txt
	│   ├── GPL.txt
	│   ├── Info-ZIP.txt
	│   ├── LGPL2_1.txt
	│   ├── LGPL2.txt
	│   ├── LGPL3.txt
	│   ├── MIT_Modified.txt
	│   ├── MIT.txt
	│   ├── MPL1_1.txt
	│   ├── NVIDIA.txt
	│   ├── OFL1_1.txt
	│   ├── Public_Domain.txt
	│   └── Radeon_rlc.txt
	├── openelec.ico
	├── README.md
	├── RELEASE
	└── target
		├── KERNEL
		├── KERNEL.md5
		├── SYSTEM
		└── SYSTEM.md5

	4 directories, 40 files

We just need to grab all the files under the **target** directory and put under the **/storage/.update** directory on the current OpenELEC machine. So I SSH'ed into my OpenELEC machine and ran the following to copy the files (I had the **rsync** plugin):

	pi:~ # rsync -avP crbook:download/OpenELEC-RPi.arm-4.0.6/target/. .update/.
	receiving incremental file list
	./
	KERNEL
		 5997936 100%  993.45kB/s    0:00:05 (xfer#1, to-check=3/5)
	KERNEL.md5
			  48 100%    0.06kB/s    0:00:00 (xfer#2, to-check=2/5)
	SYSTEM
	   102686720 100%  941.88kB/s    0:01:46 (xfer#3, to-check=1/5)
	SYSTEM.md5
			  48 100%    0.05kB/s    0:00:00 (xfer#4, to-check=0/5)

	sent 106 bytes  received 108711569 bytes  941226.62 bytes/sec
	total size is 108684752  speedup is 1.00
	
Then I moved the current configuration out of the way as per the recommendation:

	pi:~ # mv .xbmc .xbmc-backup

Lastly I just rebooted:

	pi:~ # reboot
	
After it rebooted the new version was installed. 

### Re-Apply the Original Settings
I then went back to my [OpenELEC on Raspberry Pi](/2013/11/openelec-raspberry-pi/) post and re-applied my old settings:

1. Apply the IP settings and finish the Initial Setup Wizard
2. Install the xTV-SAF Skin
  - Copy the font settings over `cp .xbmc.backup/addons/skin.xtv-saf/720p/Font.xml .xbmc/addons/skin.xtv-saf/720p/Font.xml`
3. Enable the Web Server Service. **System** -> **Services** -> **Webserver** (you don't have do this manually any more)
4. Add my Plex Movies Libraty via UPNP. **Movies** -> **Add Movies** -> **Browse** -> **UPNP**
5. Fix the Time Zone. **System** -> **Appearance** -> **International**

   ![openelec-time-settings](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/openelec-update-4/2014-06-openelec-time-settings.png)
   
The rest of the stuff was okay, like **optware** and **snmpd** (check out [this](/2013/11/openelec-raspberry-pi/) post on that setup). 

### New Performance Tuning Settings

I ran into [this](http://www.htpcbeginner.com/raspberry-pi-openelec-tweaks/) site, which had a lot of good recommendation. Here are the ones I followed.


#### OverClock the Raspberry Pi
Here are the steps for that:

1. Mount **/flash** as *read/write*

		pi:~ # mount /flash -o remount,rw

2. Edit the **config.txt** file

		pi:~ # vi /flash/config.txt

3. Add the following parameters:

		arm_freq=800
		core_freq=300
	
For a more in depth guide, check out [How to overclock Raspberry Pi running OpenELEC?](http://www.htpcbeginner.com/overclock-raspberry-pi-openelec/). After I rebooted I saw the following under the **Hardware** section:

![openelec-new-hardware](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/openelec-update-4/2014-06-openelec-new-hardware_g.png)

Notice the new **Speed**, you can also **ssh** into the RPi and check out **dmesg** output:

	pi:~ # dmesg | grep cpufreq
	[    1.564118] bcm2835-cpufreq: min=700000 max=800000 cur=700000

To make sure I wasn't abusing the CPU, I played a movie and checked out **top**:

![top-xbmc-playing-video](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/openelec-update-4/2014-06-top-xbmc-playing-video.png)

I wasn't pegging the CPU to max or anything. So the overclocking wasn't abusing my CPU.

#### Improve Buffer Settings
This one is pretty easy as well, modify/create the **advancedsettings.xml** file:

	pi:~ # vi .xbmc/userdata/advancedsettings.xml

and add the following:

	<advancedsettings>
	<network>
	<buffermode>1</buffermode> <!-- Comment: Default is 1 -->
	<cachemembuffersize>0</cachemembuffersize> <!-- Comment: Default is 20971520 bytes or 20 MB -->
	<readbufferfactor>4.0</readbufferfactor> <!-- Comment: Default is 1.0 -->
	</network>
	</advancedsettings>

All of the above setting are discussed in detail at [Strategies to fix XBMC buffering issues on Raspberry Pi](http://www.htpcbeginner.com/fix-raspberry-pi-xbmc-buffering-issues/). The most noteable one is the **cachemembuffersize** option (I had a pretty decent SD card). From the above page:

> Alternatively, you could set the cachemembuffersize to 0, which would force XBMC to use your local storage (SD Card) for caching videos. In this case, the cache size is only limited by the amount of free space available. Upon stopping the video the cache is automatically cleared to free up space. Note that this will increase the read/write on your SD card, which may reduce its lifespan. But SD cards are cheap and doing this can help low RAM devices such as Raspberry Pi. 

So I was okay to store the cache locally:

	pi:~ # df -h .
	Filesystem                Size      Used Available Use% Mounted on
	/dev/mmcblk0p2           29.0G    821.4M     26.7G   3% /storage

#### Other Advanced Settings
We will modify the same file for these:

	pi:~ # vi .xbmc/userdata/advancedsettings.xml

and here are the settings that I ended up with:

	<loglevel hide="true">0</loglevel>
	<nodvdrom>true</nodvdrom>
	<videolibrary>
		<cleanonupdate>true</cleanonupdate>
		<importwatchedstate>true</importwatchedstate>
	</videolibrary>
	<videoscanner>
		<ignoreerrors>true</ignoreerrors>
	</videoscanner>
	<video>
		<timeseekforward>15</timeseekforward>
		<timeseekbackward>-15</timeseekbackward>
		<subsdelayrange>240</subsdelayrange>
	</video>
	
I decided to leave the logging just to see what's going on. But if you want to completely disable logging set the **logvelel** option to **-1**. All of the setttings are covered in detail in [advancedsettings.xml](http://kodi.wiki/view/advancedsettings.xml)

### Other Tweaks
I also ran into [10 Tweaks to improve XBMC performance on Raspberry Pi](http://www.htpcbeginner.com/10-tweaks-to-improve-xbmc-performance-on-raspberry-pi/). Here are some of the settings I applied from that page.

#### Disable Un-used Services
Go to **System** -> **Services** and disable anything you don't use. I disabled the following:

1. Samba
2. Bluetooth
3. ZeroConf
4. Weather (**System** -> **Weather**)

#### Disable Actor and Video Thumbnails

This one is found under **System** -> **Videos** -> **Library**:

![openelec-dont-get-actor-thumb](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/openelec-update-4/2014-06-openelec-dont-get-actor-thumb.png)

If you are planning to play a lot of music you can uncheck the **Disable Tag Reading** option.

### Downgrading to 4.0.2
Everything was working out well, until I started watching some tv streams. XBMC would just restart on it's own. I only saw the following in the logs, right prior to the restart:

	pi:~ # tail -f .xbmc/temp/xbmc.log
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (65536->49152)
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (49152->65536)
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (65536->49152)
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (49152->65536)
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (65536->49152)
	13:59:04 T:2750211152   ERROR: COMXAudioCodecOMX::GetData Unexpected change of size (49152->65536)
	
I was only able to find [the following](http://forum.xbmc.org/showthread.php?tid=196936) (Openelec 4.0.3 Screen goes black during Live TV) forum that matched my error message. In the forum they mentioned that it's known issue and going back to 4.0.2 should fix the issue(and hopefully 4.0.4 fixes the issue). Given the fact that I was on 4.0.6 and the issue was still happening, I decided to downgrade to 4.0.2. 

With the new version of OpenELEC (4.0), we just copy the **tar** file into the update folder and the update process will proceed. From [Updating OpenELEC](http://wiki.openelec.tv/index.php/Updating_OpenELEC#Manually_Updating_OpenELEC_3.x_to_4.0)

> Manually updating OopenELEC Gotham has become easier as well. You are no longer required to extract the system files yourselves, this is all done by OpenELEC internally. This means, that you only have to copy the downloaded .tar file into the Update folder, and have OpenELEC reboot. The .tar file will be extracted and tested, after which the necessary components will be copied to the SYSTEM partition as before. A second boot will follow to finalize the upgrade process.

So I mozied over to the [archives](http://archive.openelec.tv/) page for openelec and downloaded the 4.0.2 version:

	elatov@crbook:~/download$ls -lh OpenELEC-RPi.arm-4.0.2.tar 
	-rw-r--r-- 1 elatov elatov 109M May 27 12:33 OpenELEC-RPi.arm-4.0.2.tar
	
Then I **ssh**'ed into the RPi and I copied the file over:

	pi:~ # rsync -avP crbook:download/OpenELEC-RPi.arm-4.0.2.tar .update/.
	receiving incremental file list
	OpenELEC-RPi.arm-4.0.2.tar
	   113664000 100%    1.63MB/s    0:01:06 (xfer#1, to-check=0/1)

	sent 42 bytes  received 113691864 bytes  1505853.06 bytes/sec
	total size is 113664000  speedup is 1.00
	
Then after I rebooted, the 4.0.2 version was installed (rebooting a second time finished the downgrade). So I am currently on 4.0.2:

	pi:~ # cat /etc/version 
	4.0.2

Since I have been on 4.0.2, I haven't seen xbmc restart and the TV streams are working without issues.
