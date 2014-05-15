---
title: Update ChrUbuntu 12.04 to 13.04 on the Samsung Chromebook
author: Karim Elatov
layout: post
permalink: /2013/03/update-chrubuntu-12-04-to-13-04-on-the-samsung-chromebook/
dsq_thread_id:
  - 1404672973
categories:
  - OS
tags:
  - ChromeBook
  - ChrUbuntu
---
The update process is not as smooth as the install process which I blogged about <a href="http://virtuallyhyper.com/2013/03/install-chrubuntu-12-04-on-samsung-chromebook" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/install-chrubuntu-12-04-on-samsung-chromebook']);">here</a>. Most of the instructions are laid at the following two sites:

*   <a href="http://marcin.juszkiewicz.com.pl/2013/02/16/how-to-update-chrubuntu-12-04-to-ubuntu-13-04/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://marcin.juszkiewicz.com.pl/2013/02/16/how-to-update-chrubuntu-12-04-to-ubuntu-13-04/']);">How to update Chrubuntu 12.04 to Ubuntu 13.04</a>
*   <a href="http://www.relurori.com/blog/p/ubuntu-install-on-arm-chromebook.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.relurori.com/blog/p/ubuntu-install-on-arm-chromebook.html']);">Ubuntu Install on ARM Chromebook</a>

### 1. Update Using the Aptitude Repositories

Let's get to it, first let's point the Aptitude repositories to point to the "Raring" release:

    sudo sed -i 's/precise/raring/g' /etc/apt/sources.list
    

Then update the repositories cache:

    sudo apt-get update
    

Then start the upgrade process:

    sudo apt-get dist-upgrade
    

The process will actually fail at the end of the update, but that is okay we can just force it:

    sudo apt-get -f install
    

In the process some packages will be removed unintentionally, so re-install them:

    sudo apt-get install ubuntu-desktop gnome-control-center nautilus nautilus-share nautilus-sendto eog unity libgnome-desktop-3.4 gnome-settings-daemon
    

### 2. Finishing Touches

Let's enable the Chromebook Hacker PPA and install the Chomebook utilities and updates:

    sudo add-apt-repository ppa:chromebook-arm/ppa
    sudo apt-get update
    sudo apt-get install cgpt vboot-kernel-utils linux-image-chromebook
    sudo apt-get autoremove
    sudo apt-get remove flash-kernel
    

Let's sign our kernel:

    echo "console=tty1 printk.time=1 quiet nosplash rootwait root=/dev/mmcblk1p7 rw rootfstype=ext4" > FILE
    

Notice my device is the external SD card (mmcblk1), now for the signature:

    sudo vbutilkernel --pack /boot/chronos-kernel-image --keyblock /usr/share/vboot/devkeys/kernel.keyblock --version 1 --signprivate /usr/share/vboot/devkeys/kerneldatakey.vbprivk --config FILE --vmlinuz /boot/vmlinuz-3.4.0.5-chromebook --arch arm
    

Also let's copy our signed kernel to the SD Card:

    sudo dd if=/boot/chronos-kernel-image of=/dev/mmcblk1p1 bs=4M
    

Now reboot and you will boot into ChrUbuntu 13.04.

### 3. Fix the Window Manager

When the Chromebook reboots, it won't be able to start it's window manager and we have to pick a new one. So press **CTRL+ALT+F1** and log in with the **user**/**user** credentials and first install the new video driver:

    sudo apt-get install xserver-xorg-video-armsoc
    

Then I installed **icewm**:

    sudo apt-get install icewm
    

I, then, made IceWM the default window manager by editing the **/etc/lightdm/lightdm.conf** file and making it looks like this:

    [SeatDefaults]
    user-session=IceWM
    greeter-session=unity-greeter
    #autologin-user=user
    

then I updated the rest of the packages:

    sudo apt-get update
    sudo apt-get upgrade
    

I rebooted one more time, and I was then able to login into IceWM without issues.

### 4. Fix Post-Update Issues

After I rebooted, my sound stopped working for some reason. The **alsamixer** settings were correct but it seemed like **pulseaudio** was messing up my sound, so I removed **pulseaudio** and **alsa-base** like so:

    sudo apt-get remove --purge pulseaudio alsa-base
    

and then I just re-installed the **alsa-base** package:

    sudo apt-get install alsa-base
    

and then my sound started working without issues. Another issue I ran into was with my touchpad, the double tap and triple tap functionality was reversed (ie tripped tap was right click and double tap was middle click) not sure why. After messing around with **synclient**, I discovered the following settings fixed it:

    synclient | grep -i TapBu
    TapButton1 = 1
    TapButton2 = 3
    TapButton3 = 2
    

To make those permanent, I added the following :

    Option "TapButton1" "1"
    Option "TapButton2" "3"
    Option "TapButton3" "2"
    

to the **/usr/share/X11/xorg.conf.d/10-synaptics.conf** file.

The last issue that I ran into was Chromium stopped playing HTML5 audio for some reason. I ran across <a href="http://www.chromestory.com/2012/07/google-music-html5-audio-not-working-in-chromium-here-is-the-fix/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.chromestory.com/2012/07/google-music-html5-audio-not-working-in-chromium-here-is-the-fix/']);">this</a> post, and I fixed the issue by running the following:

    sudo apt-get install chromium-codecs-ffmpeg-extra
    

just for reference here is my chromium version:

    chromium-browser --version
    Chromium 22.0.1229.94 Built on Ubuntu 12.10, running on Ubuntu 13.04
    

### 5. Some keyboard tweeks

I wanted to use the volume up and volume down keys on the keyboard (they corresponded to F9 and F10), since I was using IceWM it was pretty easy. I just added the following into my **~/.icewm/keys** files and they worked great:

    key "F8" amixer -c 0 set Speaker toggle
    key "F9" amixer -c 0 set Speaker 1%-
    key "F10" amixer -c 0 set Speaker 1%+
    key "Ctrl+F8" amixer -c 0 set Headphone toggle
    key "Ctrl+F9" amixer -c 0 set Headphone 1%-
    key "Ctrl+F10" amixer -c 0 set Headphone 1%+
    

This allowed me to modify the HeadPhone and Speakers volume with the keyboard shortcuts that I defined.

I also wanted to have the brightness keys work as well (those corresponded to F6 and F7). I tried the package **xbacklight** but it didn't work. Later I found that the **/usr/lib/gnome-settings-daemon/gsd-backlight-helper** worked without issues. So I wrote this quick script:

    elatov@crbook:~$ cat /usr/local/bin/chbr
    #!/bin/bash
    cur_bri=$(/usr/bin/pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --get-brightness)
    
    if [ $1 == "up" ] ; then
        /usr/bin/pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --set-brightness $(($cur_bri+100))
    fi
    
    if [ $1 == "down" ] ; then
        /usr/bin/pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --set-brightness $(($cur_bri-100))
    fi
    

and if you pass in **up** or **down** it decreases or increases the brightness by 100. My max brightness was at 2800 so this worked out for me (you can check out the max brightness by running `/usr/lib/gnome-settings-daemon/gsd-backlight-helper --get-max-brightness`). Then I added the following to my **~/.icewm/keys** file:

    key "F6"    /usr/local/bin/chbr down
    key "F7"    /usr/local/bin/chbr up
    

I also noticed that the keyboard button right below the "**Tab**" key (the Search Key) was functioning as a "**Windows**" Key. That is usually the "**Caps_Lock**" key, so I changed the mapping for it to actually be the "**Caps_Lock**" key. Initially I used **xev** to find out what is the keycode of the keyboard button and then I added the following to my **~/.Xmodmap** file:

    elatov@crbook:~$ cat .Xmodmap 
    keycode 133 = Caps_Lock
    

Another thing I noticed was the "Disable Keyboard While Typing" Option wasn't working. Starting up the **syndaemon** fix the issue for me. Here is what I added to my **~/.icewm/startup** file to start the daemon on startup:

    elatov@crbook:~$ grep syn .icewm/startup 
    syndaemon -t -k -i 1 -d
    

Lastly, I didn't have the "Delete", "PageDown", or "Home" keys. In ChromeOS the following keyboard shortcuts existed that helped me.

    Page up                Alt and the up arrow
    Page down              Alt and the down arrow
    Home                   Ctrl+Alt, and the up arrow
    End                    Ctrl+Alt, and the down arrow
    Delete                 Alt and Backspace
    

You can see the full list <a href="http://support.google.com/chromeos/bin/answer.py?hl=en&answer=183101" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://support.google.com/chromeos/bin/answer.py?hl=en&answer=183101']);">here</a>. There is a actually a forum about my exact inquiry <a href="http://askubuntu.com/questions/85850/how-to-remap-a-key-combination-to-a-single-key" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://askubuntu.com/questions/85850/how-to-remap-a-key-combination-to-a-single-key']);">here</a>: To get this working we first need to install **xbindkeys** and **xvkbd**.

    elatov@crbook:~$ sudo apt-get install xbindkeys xvkbd
    

then create a **~.xbindkeysrc** file with the following contents:

    "xvkbd -xsendevent -text '\[Delete]'"
    Alt + BackSpace
    
    "xvkbd -xsendevent -text '\[Home]'"
    Alt + Left
    
    "xvkbd -xsendevent -text '\[End]'"
    Alt + Right
    
    "xvkbd -xsendevent -text '\[Page_Down]'"
    Alt + Down
    
    "xvkbd -xsendevent -text '\[Page_Up]'"
    Alt + Up
    

then start **xbindkeys** by running:

    xbindkeys
    

We can add the above command to the **~/.icewm/startup** file, if we want it to auto-start upon login into IceWM. There are other alternatives to the keyboard shortcuts:

*   <a href="http://askubuntu.com/questions/249760/remap-shortcut-to-a-single-key-cannot-be-used" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://askubuntu.com/questions/249760/remap-shortcut-to-a-single-key-cannot-be-used']);">xmodtool</a>
*   <a href="http://code.google.com/p/autokey/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://code.google.com/p/autokey/']);">autokey</a>

And that's it. Last note, you can check the status of your battery with the **upower** utility:

    elatov@crbook:~$ upower -d | grep -E 'time|percent|state'
        state:               charging
        time to full:        1.4 hours
        percentage:          34.1355%
    

