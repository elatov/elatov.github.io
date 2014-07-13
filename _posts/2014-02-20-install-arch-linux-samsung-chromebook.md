---
title: Install Arch Linux on Samsung Chromebook
author: Karim Elatov
layout: post
permalink: /2014/02/install-arch-linux-samsung-chromebook/
categories: ['os']
tags: ['pulseaudio', 'gpt', 'linux', 'arch_linux', 'chromebook']
---

I decided to try out [Arch Linux](https://www.archlinux.org/) on the Samsung Chromebook. Before I was running Ubuntu, to check out the install process for Chrubuntu check out my previous posts:

*   [Install ChrUbuntu 12.04 on Samsung Chromebook](/2013/03/install-chrubuntu-12-04-on-samsung-chromebook/)
*   [Update ChrUbuntu 12.04 to 13.04 on the Samsung Chromebook](/2013/03/update-chrubuntu-12-04-to-13-04-on-the-samsung-chromebook/)
*   [Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](/2013/11/update-chrubuntu-13-04-13-10-samsung-chromebook/)

The Ubuntu install was working out well but I just kept hearing good things about Arch Linux, so I decided to give it a try.

## Installing Arch Linux

The install process is described [here](http://archlinuxarm.org/platforms/armv7/samsung/samsung-chromebook). I already had developer mode and usb boot enabled, so I went to the next steps. Once in ChromeOS open up the crosh shell:

1.  Press Ctrl + Alt + T keys. This will open up the crosh shell
2.  Type **shell** to get into a bash shell.
3.  Type **sudo su** to become root.

Now let's proceed with the install:

1.  Since ChromeOS will automatically mount any partitions it finds, unmount everything now:

        umount /dev/mmcblk1*


2.  Create a new disk label for GPT. Type y when prompted after running:

        parted /dev/mmcblk1 mklabel gpt


3.  Partition the USB drive or SD card:

        cgpt create -z /dev/mmcblk1
        cgpt create /dev/mmcblk1
        cgpt add -i 1 -t kernel -b 8192 -s 32768 -l U-Boot -S 1 -T 5 -P 10 /dev/mmcblk1
        cgpt add -i 2 -t data -b 40960 -s 32768 -l Kernel /dev/mmcblk1
        cgpt add -i 12 -t data -b 73728 -s 32768 -l Script /dev/mmcblk1


4.  To create the rootfs partition, we first need to calculate how big to make the partition using information from cgpt show. Look for the number under the start column for Sec GPT table which is *15633375* in this example:

        localhost / # cgpt show /dev/mmcblk1
               start        size    part  contents
                   0           1          PMBR
                   1           1          Pri GPT header
        ...
               73728       16384      12  Label: "Script"
                                      Type: Linux data
                                      UUID: E3DA8325-83E1-2C43-BA9D-8B29EFFA5BC4
            15633375          32          Sec GPT table
            15633407           1          Sec GPT header


5.  Replace the **xxxxx** string in the following command with that number to create the root partition:

        cgpt add -i 3 -t data -b 106496 -s `expr xxxxx - 106496` -l Root /dev/mmcblk1


6.  Tell the system to refresh what it knows about the disk partitions:

        partprobe /dev/mmcblk1


7.  Format the partitions:

        mkfs.ext2 /dev/mmcblk1p2
        mkfs.ext4 /dev/mmcblk1p3
        mkfs.vfat -F 16 /dev/mmcblk1p12


8.  Download and extract rootfs tarball:

        cd /tmp
        wget http://archlinuxarm.org/os/ArchLinuxARM-chromebook-latest.tar.gz
        mkdir root
        mount /dev/mmcblk1p3 root
        tar -xf ArchLinuxARM-chromebook-latest.tar.gz -C root


9.  Copy the kernel to the kernel partition:

        mkdir mnt
        mount /dev/mmcblk1p2 mnt
        cp root/boot/vmlinux.uimg mnt
        umount mnt


10. Copy the U-Boot script to the script partition:

        mount /dev/mmcblk1p12 mnt
        mkdir mnt/u-boot
        cp root/boot/boot.scr.uimg mnt/u-boot
        umount mnt


11. Install nv-U-Boot:

        wget -O - http://commondatastorage.googleapis.com/chromeos-localmirror/distfiles/nv_uboot-snow.kpart.bz2 | bunzip2 > nv_uboot-snow.kpart
        dd if=nv_uboot-snow.kpart of=/dev/mmcblk1p1


12. Unmount the root partition:

        umount root
        sync


13. Reboot the computer.

14. At the splash screen, instead of pressing Ctrl-D to go to CromeOS, press **Ctrl-U** to boot to the external drive.

15. You will see U-Boot start after a moment and start counting down from 3. Press any key at this time to interrupt the boot process and get a prompt that looks like:

        SMDK5250 #


16. At this prompt type this to reset the environment and save it to flash:

        env default -f
        saveenv


17. Type **reset** and press enter (it'll reboot), pressing **Ctrl-U** at the splash screen again, and let U-Boot count down and load Arch Linux ARM.

### Upgrade Arch Linux

After you boot into Arch Linux you can login with username **root**, and a *blank* password. To get on the wireless network launch:

    wifi-menu mlan0


That will give you an *ncurses* Terminal UI, at which point you can select your desired access point and enter the password if applicable. Before we upgrade the system we need to make sure the *boot* partition is mounted. This is accomplished by editing the **/etc/fstab** file and un-commenting this line:

    /dev/mmcblk1p2  /boot   ext2    defaults        0       0


Then mount **/boot** by running:

    mount -a


To upgrade the system run the following:

    pacman -Syu


After the update is done, reboot your system. Prior to the reboot, you can add your own user if you want and give him **sudo** privileges:

    useradd elatov
    passwd elatov
    pacman -S sudo
    visudo # uncomment the wheel group
    usermod -a -G wheel elatov


## Install Window Manager and Display Manager

I use **icewm** and **lighdm** for my display environment. Let's install the necessary packages.

### Install Xorg

First let's install **Xorg** and the necessary video/synaptics drivers.

    sudo pacman -S xorg-server xorg-xinit xorg-server-utils mesa xf86-video-fbdev xf86-input-synaptics unzip


Now let's apply the appropriate video driver and trackpad settings for the chromebook:

    mkdir ~/backup
    mv /etc/X11/xorg.conf.d/* ~/backup/
    cd /etc/X11/xorg.conf.d/
    wget http://craigerrington.com/chrome/x_alarm_chrubuntu.zip
    unzip x_alarm_chrubuntu.zip
    rm x_alarm_chrubuntu.zip
    sed -i 's/gb/us/g' 10-keyboard.conf


### Install Window Manager

At this point we can manually start **X**, but we don't have a window manager yet. So let's install that:

    sudo pacman -S icewm


If you are really eager, you can add the following into your **~/.xinitrc**:

    exec /usr/bin/icewm-session


then executing:

    startx


will start icewm.

### Install Display Manager

I wanted to use **lightdm** as my display manager, so let's go ahead and install that:

    sudo pacman -S lightdm lightdm-gtk3-greeter


Now let's enable the service on startup:

    sudo systemctl enable lightdm


If you reboot you will notice that all the icons are missing for *lightdm*. To install the icons run the following:

    sudo pacman -S gnome-icon-theme


At this point, I was able to start an **icewm** session from **lightdm** with out issues. I also removed my **~/.xinitrc** file so it wouldn't launch **icewm** a second time after **lightdm** did.

### SSH-Agent with IceWM

I noticed that **ssh-agent** was not starting on login. From [this](https://wiki.archlinux.org/index.php/SSH_Keys#ssh-agent) Arch Linux wiki page, it's recommended to start that from your **bashrc** file, but that would launch multiple **ssh-agents**. So I decided to launch that when **X** starts. I complished that by creating **/etc/X11/xinit/xinitrc.d/40-ssh-agent** and adding the following contents to it:

    elatov@crbook:~$cat /etc/X11/xinit/xinitrc.d/40-ssh-agent
    #!/bin/bash

    eval $(ssh-agent)


I was then able to run **ssh-add** without any issues.

### Desktop Notifications

By default no notification mechanism is enabled, so you might miss out on some OS notification when using IceWM. There are a couple of options available described [here](https://wiki.archlinux.org/index.php/Desktop_Notifications#Notification_servers). I usually use **xfce4-notifyd**, but I decided to try out something else: **notification-daemon**. First let's install the package:

    sudo pacman -S notification-daemon


The package doesn't actually create the appropriate **dbus** configuration files, this is done by creating the **/usr/share/dbus-1/services/org.gnome.Notifications.service** file with the following contents:

    [D-BUS Service]
    Name=org.freedesktop.Notifications
    Exec=/usr/lib/notification-daemon-1.0/notification-daemon


Now any time there is a notification that comes through **dbus**, you will see it. As a quick test run the following to make sure you see the OSD:

    notify-send 'Testing' --icon=dialog-information


## Brightness

**Systemd** comes with [tmpfiles.d](https://wiki.archlinux.org/index.php/systemd#Temporary_files) which can set permissions and contents of any file on the system on boot. With that functionality, let's set a custom brightness level on boot. This is acomplished by creating the **/etc/tmpfiles.d/brightness.conf** file with the following contents:

    f /sys/class/backlight/pwm-backlight.0/brightness 0666 - - - 800


Now upon boot that file will have the permission of **666** (*rw* for all users) and contain the value of **800** (possible values are **** - **2800**).

### Keyboard Shortcuts for Brightness keys

I did a similar setup on Ubuntu. Since I am using *icewm* I added the following into my **.icewm/keys** file:

    key "F6"        /usr/local/bin/chbr down
    key "F7"        /usr/local/bin/chbr up


and the content of my **/usr/local/bin/chbr** is the following:

    elatov@crbook:~$cat /usr/local/bin/chbr
    #!/bin/bash
    cur_bri=$(/usr/bin/cat /sys/class/backlight/pwm-backlight.0/brightness)

    if [ $1 == "up" ] ; then
        bri=$(($cur_bri+200))
        `echo $bri > /sys/class/backlight/pwm-backlight.0/brightness`
    fi

    if [ $1 == "down" ] ; then
        bri=$(($cur_bri-200))
        `echo $bri > /sys/class/backlight/pwm-backlight.0/brightness`
    fi

    if [ $1 == "-s" ]; then
        `echo $2 > /sys/class/backlight/pwm-backlight.0/brightness`
    fi


## Sound Configurations

First let's install **alsa** and make sure we can hear sound from the speakers:

    sudo pacman -S alsa-utils


Then start **alsamixer** and un-mute the following mixers:

> 'Left Speaker Mixer Left DAC1 Switch'
> 'Left Speaker Mixer Right DAC1 Switch'
> 'Right Speaker Mixer Left DAC1 Switch'
> 'Right Speaker Mixer Right DAC1 Switch'
> 'Right Headphone Mixer Left DAC1 Switch'
> 'Right Headphone Mixer Right DAC1 Switch'
> 'Left Headphone Mixer Left DAC1 Switch'
> 'Left Headphone Mixer Right DAC1 Switch'

To un-mute the mixer just type **m** when you are on the mixer. As a quick test run the following and make sure you hear sound:

    aplay /usr/share/sounds/alsa/Front_Left.wav


### Install PulseAudio

I remember I had some trouble in Ubuntu with this, so I wanted to give it another try. First install the necessary packages:

    sudo pacman -S pulseaudio pulseaudio-alsa


Now let's ensure the appropriate alsa sink is loaded. This is done by editing the **/etc/pulse/default.pa** file and un-commenting/modify the following line:

    load-module module-alsa-sink device=sysdefault


Now we can restart **X** or start **pulseaudio** manually

    pulseaudio --start


Your sound should still works as expected.

### Configure Libao to Use PulseAudio

I tried running **pianobar**, but it would fail. The issue is described [here](https://bbs.archlinux.org/viewtopic.php?id=158070). It's fixed by changing the **/etc/libao.conf** file to look like this:

    elatov@crbook:~$cat /etc/libao.conf
    default_driver=pulse


## Keyboard Modifications

I ended up emulating the configuration from the Ubuntu install.

### Change the Search Key to be Caps-Lock

This is done by creating/modifying the **~/.Xmodmap** file with the following contents:

    elatov@crbook:~$cat .Xmodmap
    keycode 133 = Caps_Lock


### Change Fn Keys for Volume

Similar to the way I handled the brightness, I did the same thing for sound. Here is what I added into my **~/.icewm/keys** file:

    key "F8"        amixer -c 0 set Speaker toggle
    key "F9"        amixer -c 0 set Speaker 1dB-
    key "F10"       amixer -c 0 set Speaker 1%+
    key "Ctrl+F8"   amixer -c 0 set Headphone toggle
    key "Ctrl+F9"   amixer -c 0 set Headphone 1%-
    key "Ctrl+F10"  amixer -c 0 set Headphone 1%+


### Enable End and Home Keys with Key Combinations

I ended up using **xbindkeys** with **xvkbd** again:

    sudo pacman -S xbindkeys xvkbd


First find out what they keys are called:

    elatov@crbook:~$xmodmap -pke | grep -E ' Prior | Next | Home | End | Delete '
    keycode 110 = Home NoSymbol Home
    keycode 112 = Prior NoSymbol Prior
    keycode 115 = End NoSymbol End
    keycode 117 = Next NoSymbol Next
    keycode 119 = Delete NoSymbol Delete


Those are our keys. Now capture the key combination, this is done by running the following:

    xbindkeys -mk


and then clicking "Alt + down" and it will show you what those keys correspond to. After we have all the combinations, we can create the **xbindkeys** configuration. First create the initial configuration:

    xbindkeys -d > ~/.xbindkeysrc


Then edit the file and add the following to it (add the combination that you captured above):

    #alt-up
    "xvkbd -xsendevent -text "\[Prior]""
        m:0x8 + c:111
        Alt + Up

    #alt-down
    "xvkbd -xsendevent -text "\[Next]""
        m:0x8 + c:116
        Alt + Down

    "xvkbd -xsendevent -text "\[Delete]""
        m:0x8 + c:22
        Alt + BackSpace

    "xvkbd -xsendevent -text "\[End]""
        m:0x8 + c:114
        Alt + Right

    "xvkbd -xsendevent -text "\[Home]""
        m:0x8 + c:113
        Alt + Left


Now add **/usr/bin/xbindkeys** to the **~/.icewm/startup** file and the shortcuts should be done.

### Power Button

For some reason when I pushed the power button nothing happened. Running **xev** and watching the output, showed me that I was pressing the right key, but nothing would happen. To fix my power button, I installed **acpid**:

    sudo pacman -S acpid


And then added an extra command to the **/etc/acpi/handler.sh** script:

    button/power)
            case "$2" in
                PBTN|PWRF)
                    logger 'PowerButton pressed'
                /usr/bin/systemctl poweroff
                    ;;


After that, pushing the power button would shut down the laptop.

## Configure the Rest of the System

Now for the finishing touches

### Enable rsyslog

**Rsyslog** was not enabled by default. Here is what I ran to install and enable that:

    sudo pacman -S rsyslog
    sudo systemctl enable rsyslog.service
    sudo systemctl start rsyslog.service


### Configure Networking

After you run the **wifi-menu** script a profile is generated automatically. You can check the profiles by running the following:

    elatov@crbook:~$netctl list
    * mlan0-wifi


To enable that profile on boot, just run the following:

    sudo netctl enable mlan0-wifi


By default it uses **dhcp** to grab the IP. To set a static IP, edit the **/etc/netctl/mlan0-wifi** file and add/modify the following:

    IP=static
    Address='192.168.1.116/24'
    Gateway='192.168.1.1'
    DNS=('192.168.1.1')


You will also notice that the password will be clear text in that profile file. We can use **wpa_passphrase** to hide the password. First generate the WPA password:

    elatov@crbook:~$wpa_passphrase wifi testing123
    network={
        ssid="wifi"
        #psk="testing123"
        psk=45511a5f5f172904d61cfd43ecdeb67b0c15368eb2c4b75007b5a4b9e928dd6a
    }


Not grab the string after **psk=** and add it to the **/etc/netctl/mlan0-wifi** file:

    Key=\"45511a5f5f172904d61cfd43ecdeb67b0c15368eb2c4b75007b5a4b9e928dd6a


Now if you restart the machine, it should automatically connect to the wireless network and grab a static IP as well.

### Set the Hostname

This one is pretty easy:

    sudo hostnamectl set-hostname archer.laptop.com


### Set the TimeZone

First list the available timezones:

    elatov@crbook:~$timedatectl list-timezones | grep Denver
    America/Denver


Then set the timezone:

    sudo timedatectl set-timezone America/Denver


### Install from AUR (Arch User Repository)

There are a lot of packages that are available from the user repository. The **pacman** utility doesn't query that repository. To use that repository install **yaourt**:

    sudo pacman -S base-devel yaourt


and then use it the same way you would **pacman** ie:

    # search package
    yaourt -Ss pkg
    # remove package
    sudo yaourt -Rns pkg
    # upgrade the system
    sudo  yaourt -Syu


If the package is not available for your architecture, it will compile it on the fly. You might have to edit the **PKGBUILD** file for best results.

### Mount NFS share

On Ubuntu the the NFS kernel module was not available, but Arch Linux does have it. To mount an NFS share first install the utilities:

    sudo pacman -S nfs-utils


then start the **statd** service:

    sudo systemctl enable rpc-statd.service


Then you can mount with the following command:

    sudo mount nfs:/share /mnt/nfs


### Install Chromium and PepperFlash

Another cool thing I ran across is the fact that *chromium pepper flash* was in the **extra** repository. To install the browser and the plugin run the following:

    sudo pacman -S chromium chromium-pepper-flash


Here are the installed versions:

    elatov@crbook:~$pacman -Q | grep chromium
    chromium 32.0.1700.77-1
    chromium-pepper-flash 11.7.700.225-3


Audio (with pulseaudio) and Video worked fine without any issues.

