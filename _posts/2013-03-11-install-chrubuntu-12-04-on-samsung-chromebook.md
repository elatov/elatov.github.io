---
title: Install ChrUbuntu 12.04 on Samsung Chromebook
author: Karim Elatov
layout: post
permalink: /2013/03/install-chrubuntu-12-04-on-samsung-chromebook/
categories: ['os']
tags: ['xorg', 'linux', 'chromebook', 'ubuntu']
---

There are a bunch of the steps to the process, here are some good links that have most of the instructions:

*   [So You Want ChrUbuntu on a USB / SD Card?](http://chromeos-cr48.blogspot.com/2012/12/so-you-want-chrubuntu-on-external-drive.html)
*   [Complete Guide to Installing Linux on Chromebook](https://itsfoss.com/install-linux-chromebook/)

I had some additional steps to the above guides and they kept piling up, so I decided to put everything in one big guide.

### 1. Put Chromebook in Developer mode

1.  Power off the Chrome Book
2.  Hold the **ESC** and **REFRESH** keys as you press the Power button to get into recovery mode.
3.  Press **CTRL+D** to go into developer mode.

This [site](http://www.amirkurtovic.com/blog/installing-chrubuntu-on-the-samsung-arm-chromebook-a-step-by-step-photo-guide/) has good pictures for the process. I didn't want to mess up the ChromeOS install, so I got an SD card just in case. Therefore all the below processes apply to an install of ChrUbuntu onto an SD Card.

### 2. Install Chrubuntu 12.04 on External SD-Card

Once the Chromebook is in Developer Mode, it will reboot and show you a screen about OS Verification. To start booting into Developer Mode, just press **CTRL+D**. Once booted up, don't even login, just connect to the Wireless Network. Next open up a local TTY by pressing **CTRL+ALT** and the **FORWARD** key. Then for the username type '**chronos**' and it will log you into a shell without a password. Now let's set the BIOS to be in Developer Mode with this command:

    chromeos-firmwareupdate –mode=todev


This will allow us to press **CTRL+U** to boot from SD or USB device. Now to download and install Chrubuntu 12.04 run the following:

    wget http://goo.gl/34v87; sudo bash 34v87 /dev/mmcblk1


The above command will take about 30 minutes to download and extract all the packages and after the process is finished, it will automatically reboot. Then at the OS Verification screen press **CTRL+U** to boot into Ubuntu

### 3. Fix the trackpad

After ChrUbuntu loads you will notice the sensitivity of the touch pad being a little harsh. To fix it, just run these commands:

    xinput set-prop "Cypress APA Trackpad (cyapa)" "Synaptics Finger" 15 20 256
    xinput set-prop "Cypress APA Trackpad (cyapa)" "Synaptics Two-Finger Scrolling" 1 1


or follow the instructions laid out in [this](https://github.com/jbdatko/chrubuntu_trackpad) site and run the following to make the fix permanent:

    mkdir ~/backup
    sudo mv /usr/share/X11/xorg.conf.d/* ~/backup/
    cd /usr/share/X11/xorg.conf.d/
    sudo wget http://craigerrington.com/chrome/x_alarm_chrubuntu.zip
    sudo unzip x_alarm_chrubuntu.zip
    sudo rm x_alarm_chrubuntu.zip
    sudo sed -i 's/gb/us/g' 10-keyboard.conf


### 4. Fix the Sound

You will also notice that the sound doesn't work. To fix it, we can follow the instructions laid out in [this](http://memo4ge15h1.blogspot.com/2014/10/enable-audio-on-arch-linux.html) site. Basically fire up '**alsamixer**' and unmute (by pressing 'm') the following fields:

    Left Speaker Mixer Left DAC1
    Left Speaker Mixer Right DAC1
    Right Speaker Mixer Left DAC1
    Right Speaker Mixer Right DAC1
    Left Headhone Mixer Left DAC1
    Left Headhone Mixer Right DAC1
    Right Headhone Mixer Left DAC1
    Right Headhone Mixer Right DAC1
    Right Speaker Mixer Right DAC1


The above link provides good screenshots of the process if you are not comfortable with the **alsamixer** utility.

### 5. Install Chromium

To install Chromium on ChrUbuntu, we first have to enable the "universe" repositories. Edit the **/etc/apt/source.list** file and comment out the following lines:

    deb http://ports.ubuntu.com/ubuntu-ports/ precise universe
    deb-src http://ports.ubuntu.com/ubuntu-ports/ precise universe
    deb http://ports.ubuntu.com/ubuntu-ports/ precise-updates universe
    deb-src http://ports.ubuntu.com/ubuntu-ports/ precise-updates universe


then update the repos and install the package:

    sudo apt-get update
    sudo apt-get install chromium


### 6. Enable Flash

This is the hardest of the steps. First, reboot into regular ChromeOS and copy the flash plugin to your home directory of the ChrUbuntu install (ChromeOS will automatically mount the SD Card that has ChrUbuntu installed).

After you login into ChromeOS, press **CTRL+ALT+T** and that will start up "crosh":

    Welcome to crosh, type 'help' for a list of commands.
    crosh> shell
    chronos@localhost ~ $


Then copy the flash plugin:

    chronos@localhost ~ $sudo cp /opt/google/chrome/pepper/libpepflashplayer.so /media/removable/External\ Drive\ 1/home/user/.


Also check out the version of the plugin like so:

    chronos@localhost ~ $ cat /opt/google/chrome/pepper/pepper-flash.info
    # Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
    # Use of this source code is governed by a BSD-style license that can be
    # found in the LICENSE file.
    # Registration file for Pepper Flash player.
    FILE_NAME=/opt/google/chrome/pepper/libpepflashplayer.so
    PLUGIN_NAME="Shockwave Flash"
    VERSION="11.6.602.171"
    VISIBLE_VERSION="11.6 r602"
    DESCRIPTION="$PLUGIN_NAME $VISIBLE_VERSION"
    MIME_TYPES="application/x-shockwave-flash"


Then reboot into Ubuntu and it will automatically login with the username of "**user**" and password "**user**". Once logged in, copy the new file to Chromium's plugin directory:

    sudo cp libpepflashplayer.so /usr/lib/chromium-browser/plugins/.


Then edit the **/etc/chromium-browser/default** file and add the following:

    CHROMIUM_FLAGS="--ppapi-flash-path=/usr/lib/chromium-browser/plugins/libpepflashplayer.so --ppapi-flash-version=11.6.602.171 --ppapi-flash-args=enable_hw_video_decode=0,enable_stagevideo_auto=0,enable_trace_to_console=0"


The version in the command matches of what we found in the info file above. That should be it, now you can use ChrUbuntu with almost all the functionality that you need. I am planning to update to ChrUbuntu 13.04, so stay tuned...

### Related Posts

- [Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](/2013/11/update-chrubuntu-13-04-13-10-samsung-chromebook/)
- [Update ChrUbuntu 12.04 to 13.04 on the Samsung Chromebook](/2013/03/update-chrubuntu-12-04-to-13-04-on-the-samsung-chromebook/)

