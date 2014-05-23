---
title: Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook
author: Karim Elatov
layout: post
permalink: /2013/11/update-chrubuntu-13-04-13-10-samsung-chromebook/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1979997527
categories:
  - OS
tags:
  - ChromeBook
  - ChrUbuntu
  - pulseaudio
---
I logged into my Chromebook with SSH and it displayed a message saying that I can update to Ubuntu 13.10:

    New release '13.10' available.
    Run 'do-release-upgrade' to upgrade to it.


And I thought to myself, why not?

## Upgrade Ubuntu

The upgrade it self, was pretty easy. I actually did it remotely, just cause I knew it would take a while. So ssh over to the machine and run the following:

    $ screen
    $ sudo do-release-upgrade


The **screen** is just in case you lose the connection (at which point you can re-connect to the machine and then restore the screen session by running **screen -r**). After you run the above you will see the following:

    Reading cache
    pcilib: Cannot open /proc/bus/pci
    lspci: Cannot find any working access method.

    Checking package manager

    Continue running under SSH?

    This session appears to be running under ssh. It is not recommended
    to perform a upgrade over ssh currently because in case of failure it
    is harder to recover.

    If you continue, an additional ssh daemon will be started at port
    '1022'.
    Do you want to continue?

    Continue [yN] y

    Starting additional sshd


And the install will keep going. It actually took about 4 hours for the upgrade process.

### Finish the Ubuntu Upgrade with *apt-fast*

After all the updates have been applied it will ask to reboot. After the restart we can use **apt-fast** to update the rest of the packages (more information regarding **apt-fast** can be found [here](http://www.webupd8.org/2012/10/speed-up-apt-get-downloads-with-apt.html)). First let's install **apt-fast**:

    $ git clone https://github.com/ilikenwf/apt-fast.git
    $ cd apt-fast
    $ sudo cp apt-fast /usr/bin/.
    $ sudo cp apt-fast.conf /etc/.


Now let's disable the download dialog:

    $ sudo vi /etc/apt-fast.conf


and then modify the following line:

    DOWNLOADBEFORE=true


**apt-fast** can use different "download applications", I just picked one and installed it:

    $ sudo apt-get install aria2


Now you can basically replace **apt-get** with **apt-fast**. Here is what I did to update the rest of the packages:

    $ sudo apt-fast update
    $ sudo apt-fast upgrade


## PulseAudio Issues

After I finished the update, I realized that my sound wasn't working. I started **alsamixer** to check the configuration and all the channels that I enabled during the 13.04 [install](http://virtuallyhyper.com/2013/03/update-chrubuntu-12-04-to-13-04-on-the-samsung-chromebook/) were still enabled. It was actually a little weird, I would run the following:

    $ aplay /usr/share/sounds/alsa/Front_Center.wav


At the same time I would run the following to check the status of pulseaudio:

    $pacmd
    Welcome to PulseAudio! Use "help" for usage information.
    >>> list-sinks
    1 sink(s) available.
      * index: 0
        name: <auto_null>
        driver: <module-null-sink.c>
        flags: DECIBEL_VOLUME LATENCY DYNAMIC_LATENCY
        state: RUNNING <===
        suspend cause:
        priority: 1000
        volume: 0: 100% 1: 100%
                0: 0.00 dB 1: 0.00 dB
                balance 0.00
        base volume: 100%
                     0.00 dB
        volume steps: 65537
        muted: no
        current latency: 112.11 ms
        max request: 21 KiB
        max rewind: 21 KiB
        monitor source: 0
        sample spec: s16le 2ch 44100Hz
        channel map: front-left,front-right
                     Stereo
        used by: 1  <====
        linked by: 1 <====
        configured latency: 125.00 ms; range is 0.50 .. 2000.00 ms
        module: 11
        properties:
            device.description = "Dummy Output"
            device.class = "abstract"
            device.icon_name = "audio-card"


We can see that it said it's **running**. I also installed **pavumeter** and launched it as I was running the **aplay** command, I saw activity:

![pulsemeter output Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](https://github.com/elatov/uploads/raw/master/2013/10/pulsemeter_output.png)

So **pulseaudio** is receiving the audio, but for some reason it's not passing it to **alsa**. I then killed the current **pulseaudio** process and started it in verbose mode:

    $ pulseaudio kill
    $ pulseaudio --start -vvvv
    I: [pulseaudio] main.c: Daemon startup successful.


I ran the **aplay** command one more time and here is what I saw in the **/var/log/syslog** file:

    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] module-augment-properties.c: Looking for .desktop file for aplay
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] module-intended-roles.c: Not setting device for stream ALSA Playback, because it lacks role.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c: Trying to change sample rate
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] module-suspend-on-idle.c: Sink auto_null becomes busy, resuming.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink.c: Suspend cause of sink auto_null is 0x0000, resuming
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] module-suspend-on-idle.c: Sink auto_null becomes idle, timeout in 5 seconds.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: Channel matrix:
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c:        I00
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c:     +------
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: O00 | 1.000
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: O01 | 1.000
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] remap.c: Using mono to stereo remapping
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: Using resampler 'speex-float-1'
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: Using float32le as working format.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: Resampler:
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c:   rate 48000 -> 44100 (method speex-float-1),
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c:   format s16le -> s16le (intermediate float32le),
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c:   channels 1 -> 2 (resampling 1)
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] resampler.c: Choosing speex quality setting 1.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] memblockq.c: memblockq requested: maxlength=33554432, tlength=0, base=4, prebuf=0, minreq=1 maxrewind=0
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] memblockq.c: memblockq sanitized: maxlength=33554432, tlength=33554432, base=4, prebuf=0, minreq=4 maxrewind=0
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c: Created input 0 "ALSA Playback" on auto_null with sample spec s16le 1ch 48000Hz and channel map mono
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     media.name = "ALSA Playback"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.name = "ALSA plug-in [aplay]"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     native-protocol.peer = "UNIX socket client"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     native-protocol.version = "28"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.id = "5678"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.user = "elatov"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.host = "crbook.dnsd.me"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.binary = "aplay"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.language = "en_US.UTF-8"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.machine_id = "aa45185cb44c755e350ea523000007a3"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     application.process.session_id = "1"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] sink-input.c:     module-stream-restore.id = "sink-input-by-application-name:ALSA plug-in [aplay]"
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] protocol-native.c: Requested tlength=500.00 ms, minreq=125.00 ms
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] protocol-native.c: Early requests mode enabled, configuring sink latency to minreq.
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] protocol-native.c: Requested latency=125.00 ms, Received latency=125.00 ms
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] memblockq.c: memblockq requested: maxlength=4194304, tlength=48000, base=2, prebuf=12000, minreq=12000 maxrewind=0
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] memblockq.c: memblockq sanitized: maxlength=4194304, tlength=48000, base=2, prebuf=12000, minreq=12000 maxrewind=0
    Oct 20 18:24:44 crbook pulseaudio[5618]: [pulseaudio] protocol-native.c: Final latency 625.00 ms = 250.00 ms + 2*125.00 ms + 125.00 ms


You can see that the application (aplay) wants to use **alsa**, but **pulseaudio** is not using it for some reason (it's using *Sink autonull*). At first I thought it was a permission issue, so I tried using **pulseaudio** in system mode (it basically starts as a designated user and any one can connect to it). This is done by editing the **/etc/init/pulseaudio.conf** file and uncommenting the *start* line:

    # System mode is not the recommended way to run PulseAudio as it has some
    # limitations (such as no shared memory access) and could potentially allow
    # users to disconnect or redirect each others' audio streams. The
    # recommended way to run PulseAudio is as a per-session daemon. For GNOME/KDE/
    # Xfce sessions in Ubuntu Lucid/10.04, /etc/xdg/autostart/pulseaudio.desktop
    # handles this function of automatically starting PulseAudio on login, and for
    # it to work correctly your user must *not* have "autospawn = no" set in
    # ~/.pulse/client.conf (or in /etc/pulse/client.conf). By default, autospawn
    # is enabled. For other sessions, you can simply start PulseAudio with
    # "pulseaudio --daemonize".

    start on runlevel [2345]
    stop on runlevel [016]


Then you can just start it by running the following:

    $ sudo service pulseaudio start


In the same file there is a note about loading modules:

    # Prevent users from dynamically loading modules into the PulseAudio sound
    # server. Dynamic module loading enhances the flexibility of the PulseAudio
    # system, but may pose a security risk.
    # 0 = no, 1 = yes
    env DISALLOW_MODULE_LOADING=1


I even tried enabling that, but it still didn't help. I also added by self to all the necessary groups:

    $groups
    elatov adm sudo audio fuse netdev pulse pulse-access rtkit


At this point I wanted to just load the **alsa** module manually to see if it works at all. This is done by editing the default profile for pulseaudio located in **/etc/pulse/default.pa** and commenting out the following line:

    load-module module-alsa-sink


Then checking out the verbose logs, I saw the following:

    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: Trying default with SND_PCM_NO_AUTO_FORMAT ...
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: Managed to open default
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: cannot disable ALSA period wakeups
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: Maximum hw buffer size is 743 ms
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: Set buffer size first (to 88200 samples), period size second (to 88200 samples).
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-util.c: ALSA period wakeups were not disabled
    Oct 20 18:34:34 crbook kernel: [ 2222.963566] exynos-hdmi-audio exynos-hdmi-audio: hdmi not plugged
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-sink.c: Successfully opened device default.
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-sink.c: Successfully enabled mmap() mode.
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] alsa-sink.c: Successfully enabled timer-based scheduling mode.
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] module-device-restore.c: Restoring volume for sink alsa_output.default.
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] module-device-restore.c: Restored volume: 0:  44% 1:  44%
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c: Created sink 0 "alsa_output.default" with sample spec s16le 2ch 44100Hz and channel map front-left,front-right
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.resolution_bits = "16"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.api = "alsa"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.class = "sound"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.class = "generic"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.subclass = "generic-mix"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.name = ""
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.id = "Playback HiFi-0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.subdevice = "0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.subdevice_name = "subdevice #0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.device = "0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.card = "0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.card_name = "DAISY-I2S"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     alsa.long_card_name = "DAISY-I2S"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.bus_path = "platform-sound.9"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     sysfs.path = "/devices/sound.9/sound/card0"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.string = "default"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.buffering.buffer_size = "131072"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.buffering.fragment_size = "8192"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.access_mode = "mmap+timer"
    Oct 20 18:34:34 crbook pulseaudio[6945]: [pulseaudio] sink.c:     device.description = "DAISY-I2S"


Now we can see that **alsa-sink** is utilized, and I actually heard sound without issues. Since the above fix still utilized *pulseaudio*, I was happy with it working as is.

## Chromium and PepperFlash

After the update flash video stopped working. So I downgraded chromium to the version that I know works and then flash started working again. [Here](https://launchpad.net/ubuntu/+source/chromium-browser/25.0.1364.160-0ubuntu3/+build/4456155) is the version that I downloaded:

    $ ls -1 chro*
    chromium-browser_25.0.1364.160-0ubuntu3_armhf.deb
    chromium-codecs-ffmpeg-extra_25.0.1364.160-0ubuntu3_armhf.deb


I then uninstalled the current version:

    $ sudo apt-get remove chromium-browser chromium-codecs-ffmpeg-extra


and installed the previous working version:

    $ sudo dpkg -i chromium-browser_25.0.1364.160-0ubuntu3_armhf.deb chromium-codecs-ffmpeg-extra_25.0.1364.160-0ubuntu3_armhf.deb


I then **held** the packages at that version, so they wouldn't get automatically updated:

    $ sudo apt-mark hold chromium-browser
    $ sudo apt-mark hold chromium-codecs-ffmpeg-extra


You can confirm what packages are held, by running the following:

    $apt-mark showhold
    chromium-browser
    chromium-codecs-ffmpeg-extra


You can also check what versions of a package are available with the following command:

    $apt-cache showpkg chromium-browser | awk '/Versions:/,/Reverse Depends:/' | grep ^[0-9] | awk '{print $1}'
    29.0.1547.65-0ubuntu2
    25.0.1364.160-0ubuntu3


If I see a new version of the browser I will try again. Or whenever a newer version of the pepper flash comes out, I will try that as well.

Lastly, the sound for flash stopped working as well. With the above fix, all the local media players were fine but flash didn't work with pulseaudio. I found a couple links that stated that flash doesn't support pulseaudio yet ([link1](https://wiki.archlinux.org/index.php/PulseAudio#Flash_content)). So I decided to get rid pulseaudio for now:

    $ sudo apt-get remove pulse-audio --purge
    $ sudo apt-get autoremove --purge


and then my sound was working with flash. Here is the version of flash that I was using:

![chromium flash Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](https://github.com/elatov/uploads/raw/master/2013/10/chromium_flash.png)

## Network Manager Scanning Every Two minutes

After the update I noticed a network lag everyone once in a while and I saw the following in the **/var/log/kern.log** file:

    Oct 20 14:06:59 crbook kernel: [ 8128.338599] RTM_NEWLINK: idx=2, flags=0x11043, deliver=3, fail=0, congest=0
    Oct 20 14:08:59 crbook kernel: [ 8248.280424] RTM_NEWLINK: idx=2, flags=0x11043, deliver=3, fail=0, congest=0
    Oct 20 14:10:59 crbook kernel: [ 8368.294991] RTM_NEWLINK: idx=2, flags=0x11043, deliver=3, fail=0, congest=0
    Oct 20 14:12:59 crbook kernel: [ 8488.306522] RTM_NEWLINK: idx=2, flags=0x11043, deliver=3, fail=0, congest=0


We can see that our network driver is doing something every two minutes. I found a couple of forums that talked about the issue:

*   [NetworkManager disconnects/reconnects every 2 minutes and sometimes gets "mad"](https://bugzilla.redhat.com/show_bug.cgi?id=490493)
*   [Disable scanning in NetworkManager when connected](http://nilvec.com/disable-scanning-in-networkmanager-when-connected.html)
*   [network-manager fails periodically , on backgound networks scan?](https://bugs.launchpad.net/ubuntu/+source/network-manager/+bug/373680)

In summary, this is by design. NetworkManager does a scan every two minutes so it can show you access points as they show up (or if you move to another area). There are two ways around this:

1.  You can recompile NetworkManager with a patch.
2.  You can disable automatic connection to your access point and by specifying the BSSID in the configuration.

I decided to take the latter approach. So start the network-manager connection editor:

    $ nm-connection-editor


Then click on your acess point and select **Edit**. Then go the **General** tab and uncheck "Automatically connect to this network when it is available":

![gen tab con editor Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](https://github.com/elatov/uploads/raw/master/2013/10/gen-tab-con-editor.png)

and under the **Wi-Fi** tab choose the *BSSID* from the dropdown:

![wi fi tab con edit g Update ChrUbuntu 13.04 to 13.10 on the Samsung Chromebook](https://github.com/elatov/uploads/raw/master/2013/10/wi-fi-tab-con-edit_g.png)

Now that it won't connect automatically, you can either run the following at boot (**/etc/rc.local**) or at login (**~/.icewm/startup**):

    $ /usr/bin/nmcli c up id ACCCES_POINT


After I set that up, the network lags stop and it was still automatically connecting to the network. If I ever need to connect to another Access Point, I can launch the **nm-applet** and it will manually kick off a scan.

## Lightdm Greeter Requires two logins

For some reason, after the update, the greeter kept asking me for my password twice, and only after that it would log me in. I found a bug on that, here is the [link](https://bugs.launchpad.net/unity-greeter/+bug/1202539) to that, but it hasn't been fixed yet. To get around that, I installed the *gtk greeter* and it fixed my issue:

    $ sudo apt-get install lightdm-gtk-greeter


Now to enable the new greeter, we edit the **/etc/lightdm/lightdm.conf** file and modify the following line:

    greeter-session=lightdm-gtk-greeter


I then rebooted and saw the new greeter and it didn't ask for my password twice.

## X11 Crashes when Opening another TTY

Sometimes I would want to troubleshoot an issue and I would click "Cntr-Alt-F2". Rather than giving me another TTY, it would kill my **Xorg** Server and would not show me the TTY. It would just always throw back to the **lightdm** greeter. Checking out the **/var/log/Xorg.0.log.old** file, I just saw the following:

    [    18.510] (EE)
    [    18.511] (EE) Backtrace:
    [    18.512] (EE)
    [    18.513] (EE) Segmentation fault at address 0x0
    [    18.514] (EE)
    Fatal server error:
    [    18.515] (EE) Caught signal 11 (Segmentation fault). Server aborting
    [    18.516] (EE)
    [    18.516] (EE)
    Please consult the The X.Org Foundation support
             at http://wiki.x.org
     for help.


Wasn't very useful. Usually Xorg crashes due to Video Driver issues, so I decided disable the **armsoc** driver. I did this by editing the **/usr/share/X11/xorg.conf.d/10-monitor.conf** file and modify the following lines:

    Section "Device"
            Identifier      "Mali FBDEV"
    #       Driver          "armsoc"
            Driver          "fbdev"


After another restart I was able to open other TTYs without issues. I will admit I wasn't doing anything crazy with display, plus with **glxgears** I didn't see that much of performance decrease. Here is with the **armsoc** driver:

    $ glxgears
    libGL error: failed to load driver: armsoc
    libGL error: Try again with LIBGL_DEBUG=verbose for more details.
    508 frames in 5.0 seconds = 101.521 FPS
    506 frames in 5.0 seconds = 101.108 FPS
    479 frames in 5.0 seconds = 95.703 FPS
    509 frames in 5.0 seconds = 101.664 FPS


and here is without:

    $ glxgears
    564 frames in 5.0 seconds = 112.789 FPS
    597 frames in 5.0 seconds = 119.206 FPS


Anyways, I didn't feel that much of a difference.

## *Moc* SegFaults

For some reason, **mocp** stated to seg fault after the update:

    $/usr/bin/mocp
    Segmentation fault (core dumped)


So I compiled a new version without ffmpeg support and it started up without issues. Here are the steps I took to compile that. First grab the source:

    $ wget http://ftp.daper.net/pub/soft/moc/stable/moc-2.4.4.tar.bz2


Now let's grab the prerequites:

    $ sudo apt-fast install libncurses5-dev libid3tag0-dev


Now to configure the package:

    $ tar xvjf moc-2.4.4.tar.bz2; cd moc-2.4.4
    $ ./configure --prefix=/usr/local/moc --without-ffmpeg


To compile the package

    $ make -j 2


And finally to install the package:

    $ sudo mkdir /usr/local/moc
    $ sudo chown elatov:elatov /usr/local/moc
    $ make install


If you have **/usr/local/bin/** in your path, you can create a symlink as well:

    $ sudo ln -s /usr/local/moc/bin/mocp /usr/local/bin/mocp


## Cuse Module not found

After the update, I would see the following message during boot up:

    FATAL: cuse module not found


It turned out that the **osspd** package was trying to load it for some reason. I was just using **alsa** anyways, so I just uninstalled that package and the error went away:

    $ sudo apt-get remove --purge osspd


And now my update is done :) If I discover any new issues, I will try to post them as they come up.

