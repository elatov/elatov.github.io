---
title: Setup Apple Wireless Keyboard via Bluetooth on Fedora 17
author: Karim Elatov
layout: post
permalink: /2012/09/setup-apple-wireless-keyboard-via-bluetooth-on-fedora-17/
dsq_thread_id:
  - 1404673613
categories:
  - OS
tags:
  - Apple Wireless Keyboard
  - Bluetooth
  - Bluetooth Pairing
  - Bluez
  - DBUS
  - hciconfig
  - hcitool
  - HID2HCI
  - l2ping
  - rfkill
  - sdbtool
  - simple-agent
---
There are a couple of steps to the setup.

### Step 1: Install and Enable the Bluetooth Service

    [elatov@klaptop ~]$ sudo yum install bluez bluez-libs


After it's installed you should see the following:

    [elatov@klaptop ~]$ rpm -qa | grep bluez
    bluez-libs-4.99-2.fc17.i686
    bluez-4.99-2.fc17.i686


After the package is installed it should be automatically enabled to be started up on boot.

    [elatov@klaptop ~]$ sudo service bluetooth status
    Redirecting to /bin/systemctl status bluetooth.service
    bluetooth.service - Bluetooth Manager
    Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
    Active: active (running) since Sun, 16 Sep 2012 11:13:11 -0600; 26min ago
    Main PID: 589 (bluetoothd)
    CGroup: name=systemd:/system/bluetooth.service
    └ 589 /usr/sbin/bluetoothd -n


If for some reason the service was not auto started after the install and wasn't setup to start on boot up, run the following to start the service and to enable the service to start on boot:

    [elatov@klaptop ~]$sudo service bluetooth enable
    [elatov@klaptop ~]$sudo service bluetooth start


### Step 2: Enable HID2HCI

From the Fedora "[Documentation/Bluetooth](https://fedoraproject.org/wiki/Documentation/Bluetooth)":

> Q: My Dell/Apple laptop (or Logitech dongle) is supposed to have Bluetooth built-in, but doesn't show up.
>
> A: You'll need to un-comment the line HID2HCI_ENABLE=true in the /etc/sysconfig/bluetooth file. Start the bluetooth service again with service bluetooth restart as root (or restart your machine) and the Bluetooth device should now be available.
>
> Note: this is not a configuration option in Fedora 11 (updates), and later versions, it is automatic. For Fedora 16 and later, you will need to install the bluez-hid2hci package to enable this feature.

    [elatov@klaptop ~]$ sudo yum install bluez-hid2hci


After it's installed you should see the following packages:

    [elatov@klaptop ~]$ rpm -qa | grep bluez
    bluez-libs-4.99-2.fc17.i686
    bluez-hid2hci-4.99-2.fc17.i686
    bluez-4.99-2.fc17.i686


If you want more information on how Bluetooth interacts with HID, I would recommend reading "[Manage HID Bluetooth devices in Linux](http://idebian.wordpress.com/2008/07/06/manage-hid-bluetooth-devices-in-linux/)"

### Step 3: Confirm your Bluetooth Device on your Laptop is Enabled and Available

Check to see if **lsusb** shows the device:

    [elatov@klaptop ~]$ lsusb | grep Blue
    Bus 003 Device 002: ID 0a5c:4500 Broadcom Corp. BCM2046B1 USB 2.0 Hub (part of BCM2046 Bluetooth)
    Bus 003 Device 005: ID 413c:8160 Dell Computer Corp. Wireless 365 Bluetooth


Check to make sure the device is enabled:

    [elatov@klaptop ~]$ rfkill list
    0: phy0: Wireless LAN
       Soft blocked: no
       Hard blocked: no
    1: hci0: Bluetooth
       Soft blocked: no
       Hard blocked: no


Make sure the device is up:

    [elatov@klaptop ~]$ hciconfig -a
    hci0:   Type: BR/EDR  Bus: USB
        BD Address: 50:63:13:91:3A:AC  ACL MTU: 1021:8  SCO MTU: 64:1
        UP RUNNING PSCAN
        RX bytes:2870608 acl:158715 sco:0 events:777 errors:0
        TX bytes:8986 acl:322 sco:0 commands:246 errors:0
        Features: 0xff 0xff 0x8f 0xfe 0x9b 0xff 0x79 0x83
        Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3
        Link policy: RSWITCH HOLD SNIFF PARK
        Link mode: SLAVE ACCEPT
        Name: 'fed.dnsd.me-0'
        Class: 0x400100
        Service Classes: Telephony
        Device Class: Computer, Laptop
        HCI Version: 2.1 (0x4)  Revision: 0x50ad
        LMP Version: 2.1 (0x4)  Subversion: 0x423d
        Manufacturer: Broadcom Corporation (15)


Lastly make sure the device is available with **hcitool**:

    [elatov@klaptop ~]$ hcitool dev
    Devices:
       hci0 50:63:13:91:3A:AC


### Step 4: Put the Keyboard in Discoverable Mode and Ensure you Can See it

From "[Bluetooth: How to set up your Apple Wireless Keyboard](http://support.apple.com/kb/HT1809)"

> **Now pair the keyboard with the computer:**
>
> 1.  Press and release the On/Off switch to turn on your wireless keyboard.
> 2.  The green LED should begin blinking if the keyboard is not already paired and connected to another computer. The blinking LED indicates that the keyboard is in the discoverable mode. If you don't pair your keyboard with your Mac within three minutes, the indicator light and keyboard will turn off to preserve battery life. If this happens, press the On/Off switch to turn your keyboard on again.
>
> Note: If the LED doesn't turn on, make sure you have good batteries in the keyboard and that they are properly installed.

While you see the blinking LED, check to see if you can discover the keyboard:

    [elatov@klaptop ~]$ hcitool scan
    Scanning ...
        B8:F6:B1:02:1C:32       Apple Wireless Keyboard


Also check to make sure you can "ping" the device:

    [elatov@klaptop ~] sudo l2ping B8:F6:B1:02:1C:32
    Ping: B8:F6:B1:02:1C:32 from 50:63:13:91:3A:AC (data size 44) ...
    44 bytes from B8:F6:B1:02:1C:32 id 0 time 7.94ms
    44 bytes from B8:F6:B1:02:1C:32 id 1 time 35.19ms
    44 bytes from B8:F6:B1:02:1C:32 id 2 time 35.62ms
    44 bytes from B8:F6:B1:02:1C:32 id 3 time 29.56ms
    ^C4 sent, 4 received, 0% loss


### Step 5: Pair with the Bluetooth Keyboard

There has been a lot of changes between bluez version 3 and 4. Check out "[How Ubuntu’s broken bluetooth support came to be](http://blog.projectnibble.org/2010/08/08/how-ubuntus-broken-bluetooth-support-came-to-be/)". With version 3 you could use the instructions laid out in the following articles:

*   [Using Bluetooth in a Debian system](http://wiki.debian.org/BluetoothUser)
*   [Set up a bluetooth keyboard and mouse in Fedora 10](http://www.techrepublic.com/blog/opensource/set-up-a-bluetooth-keyboard-and-mouse-in-fedora-10/398)
*   [BluetoothSetup](https://help.ubuntu.com/community/BluetoothSetup)

But I was on version 4 and it uses **dbus** to connect to the device. From what I've read you should be able to run '**bluez-simple-agent**', '**simple-agent**' , or '**bluetooth-agent**'. For more info check out:

*   [Bluetooth paring from command line?](http://forums.fedoraforum.org/showthread.php?t=278226)
*   [A Step By Step Guide To Setup A Bluetooth Keyboard And Mouse On The Raspberry PI](http://www.ctheroux.com/2012/08/a-step-by-step-guide-to-setup-a-bluetooth-keyboard-and-mouse-on-the-raspberry-pi/)
*   [Setting up BlueZ with a passkey/PIN](http://www.linuxquestions.org/questions/linux-wireless-networking-41/setting-up-bluez-with-a-passkey-pin-to-be-used-as-headset-for-iphone-816003/)

But on my fedora install I couldn't find any of those tools. I then ran into [Manually using Bluetooth](http://wiki.openmoko.org/wiki/Manually_using_Bluetooth). From that article:

> Please keep in mind that whenever hcid or pand or hidd are mentioned it means that instructions are applicable only to bluez3 systems which is deprecated ages ago. Modern bluez4 uses only one daemon - bluetoothd and you are supposed to use dbus api directly to configure it. For pairing from command line use simple-agent script.

That article also had link to the **simple-agent** script. Here is the [link](http://git.kernel.org/?p=bluetooth/bluez.git;a=blob_plain;f=test/simple-agent;hb=HEAD). It's a python script which runs all the necessary **dbus** calls to pair the devices. You could probably run the **dbus** calls your self, here are some articles which have examples of the **dbus** calls:

*   [Connecting Bluetooth devices from command line](http://zitzlinux.wordpress.com/2011/02/28/connecting-bluetooth-devices-from-command-line/)
*   [Freedom Slim Keyboard](http://wiki.openmoko.org/wiki/Freedom_Slim_Keyboard)

I just downloaded the script and used it to pair the devices:

    [elatov@klaptop ~]$ sudo ./simple-agent.py hci0 B8:F6:B1:02:1C:32
    RequestPinCode (/org/bluez/589/hci0/dev_B8_F6_B1_02_1C_32)
    Enter PIN Code: 1234
    Release New device (/org/bluez/589/hci0/dev_B8_F6_B1_02_1C_32)


When the "Enter PIN Code" shows up, use your regular keyboard to enter a new pin. Then click enter, after that you will just see a blank line, then use your bluetooth keyboard to enter the same PIN and then hit enter. If it works successfully you should see the "Release" message.

### Step 7: Connect to the keyboard

After the pairing is complete, go ahead and connect to the device:

    [elatov@klaptop ~]$ sudo hcitool cc B8:F6:B1:02:1C:32
    [elatov@klaptop ~]$ sudo hcitool auth B8:F6:B1:02:1C:32


### Steps 3-7: Use the GUI

If you don't like the command line, then run "**bluetooth-wizard**" from a terminal and a GUI will show up which will allow you to complete steps 3-7 without the need to download any 'simple-agent' scripts. You can also start '**gnome-control-center**' and then click on **bluetooth**. After you are done, your successful setup should look like this:

[<img class="alignnone size-full wp-image-3616" title="bluetooth" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/bluetooth.png" alt="bluetooth Setup Apple Wireless Keyboard via Bluetooth on Fedora 17" width="675" height="415" />](http://virtuallyhyper.com/wp-content/uploads/2012/09/bluetooth.png)

To use '**bluetooth-wizard**', make sure the following packages are installed:

    [elatov@klaptop etc]$ rpm -qa | grep gnome-bluetooth
    gnome-bluetooth-libs-3.4.2-1.fc17.i686
    gnome-bluetooth-3.4.2-1.fc17.i686


### Step 8: Confirm the Bluetooth Connection

You can use **hcitool** to check for the successful connection:

    [elatov@klaptop ~]$ hcitool con
    Connections:
        > ACL B8:F6:B1:02:1C:32 handle 11 state 1 lm MASTER AUTH ENCRYPT


If you want more information, you can do the following:

    [elatov@klaptop ~]$ hcitool info 7C:ED:8D:68:E1:7D
    Requesting information ...
        BD Address:  B8:F6:B1:02:1C:32
        Device Name: Apple Wireless Keyboard
        LMP Version: 2.0 (0x3) LMP Subversion: 0x31c
        Manufacturer:  Apple, Inc. (76)
        Features: 0xbc 0x02 0x04 0x38 0x08 0x00 0x00 0x00


You can also use '**sdbtool**' to confirm the connection as well:

    $ sdptool browse B8:F6:B1:02:1C:32
    Browsing B8:F6:B1:02:1C:32 ...
    Service Name: Apple Wireless Keyboard Service
    Description: Keyboard
    Service Provider: Apple Inc.
    Service RecHandle: 0x10000
    Service Class ID List:
       "Human Interface Device" (0x1124)
    Protocol Descriptor List:
       "L2CAP" (0x0100)
       PSM: 17 "HIDP" (0x0011)
    Language Base Attr List:
       code_ISO639: 0x656e
       encoding: 0x6a
       base_offset: 0x100
    Profile Descriptor List:
       "Human Interface Device" (0x1124)
        Version: 0x0100


I actually used the bluetooth keyboard to write this post :)

