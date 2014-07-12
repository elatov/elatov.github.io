---
title: Fixing Android Phone Device Permissions on Fedora 17
author: Karim Elatov
layout: post
permalink: /2013/02/fixing-android-phone-device-permissions-on-fedora-17/
dsq_thread_id:
  - 1404673484
categories: ['os']
tags: ['fedora', 'linux', 'adb',  'htc',  'udev', 'android' ]
---

I was connecting my *HTC* phone to another *Fedora* computer and I realized I didn't have appropriate permissions to the device. After I plugged in the device, **adb** gave me the following error:

    moxz:~>/usr/local/android/platform-tools/adb devices -l
    * daemon not running. starting it now on port 5037 *
    * daemon started successfully *
    List of devices attached
    ???????????? no permissions usb:1-2


*Googling* around I found [page](http://ptspts.blogspot.com/2011/10/how-to-fix-adb-no-permissions-error-on.html) as well. The blog post was for *Ubuntu* and it included a lot of phones, which I didn't really need. So I decided to create my own *udev* rules for my *Fedora* 17 install. The first thing that we need to is figure out the device path of our usb phone. After plugging the phone into the usb slot, we will see the following in **dmesg**:

    moxz:~>dmesg | tail -11
    [1004050.455351] usb 1-2: USB disconnect, device number 18
    [1004060.234058] usb 1-2: new full-speed USB device number 19 using ohci_hcd
    [1004060.426808] usb 1-2: New USB device found, idVendor=0bb4, idProduct=0c86
    [1004060.426816] usb 1-2: New USB device strings: Mfr=2, Product=3, SerialNumber=4
    [1004060.426820] usb 1-2: Product: HTC
    [1004060.426823] usb 1-2: Manufacturer: HTC
    [1004060.426826] usb 1-2: SerialNumber: HT164T500742
    [1004060.434233] scsi18 : usb-storage 1-2:1.0
    [1004061.444207] scsi 18:0:0:0: Direct-Access HTC File-CD Gadget 0000 PQ: 0 ANSI: 2
    [1004061.450206] sd 18:0:0:0: Attached scsi generic sg3 type 0
    [1004061.468162] sd 18:0:0:0: [sdb] Attached SCSI removable disk


We can see that our phone device is **sdb**, now using *udev* we can query the device for more information, like so:

    moxz:~>udevadm info -q all -n /dev/sdb
    P: /devices/pci0000:00/0000:00:02.2/usb1/1-2/1-2:1.0/host18/target18:0:0/18:0:0:0/block/sdb
    N: sdb
    S: disk/by-id/usb-HTC_File-CD_Gadget_HT164T500742-0:0
    S: disk/by-path/pci-0000:00:02.2-usb-0:2:1.0-scsi-0:0:0:0
    E: DEVLINKS=/dev/disk/by-id/usb-HTC_File-CD_Gadget_HT164T500742-0:0 /dev/disk/by-path/pci-0000:00:02.2-usb-0:2:1.0-scsi-0:0:0:0
    E: DEVNAME=/dev/sdb
    E: DEVPATH=/devices/pci0000:00/0000:00:02.2/usb1/1-2/1-2:1.0/host18/target18:0:0/18:0:0:0/block/sdb
    E: DEVTYPE=disk
    E: ID_BUS=usb
    E: ID_INSTANCE=0:0
    E: ID_MODEL=File-CD_Gadget
    E: ID_MODEL_ENC=File-CD\x20Gadget\x20\x20
    E: ID_MODEL_ID=0c86
    E: ID_PATH=pci-0000:00:02.2-usb-0:2:1.0-scsi-0:0:0:0
    E: ID_PATH_TAG=pci-0000_00_02_2-usb-0_2_1_0-scsi-0_0_0_0
    E: ID_REVISION=0000
    E: ID_SERIAL=HTC_File-CD_Gadget_HT164T500742-0:0
    E: ID_SERIAL_SHORT=HT164T500742
    E: ID_TYPE=disk
    E: ID_USB_DRIVER=usb-storage
    E: ID_USB_INTERFACES=:080650:ff4201:
    E: ID_USB_INTERFACE_NUM=00
    E: ID_VENDOR=HTC
    E: ID_VENDOR_ENC=HTC\x20\x20\x20\x20\x20
    E: ID_VENDOR_ID=0bb4
    E: MAJOR=8
    E: MINOR=16
    E: SUBSYSTEM=block
    E: TAGS=:systemd:
    E: UDISKS_PRESENTATION_NOPOLICY=0
    E: USEC_INITIALIZED=1004061498268


The most important information is the following:

    P: DEVPATH=/devices/pci0000:00/0000:00:02.2/usb1/1-2/1-2:1.0/host18/target18:0:0/18:0:0:0/block/sdb
    E: ID_SERIAL_SHORT=HT164T500742
    E: ID_VENDOR=HTC
    E: ID_VENDOR_ID=0bb4


Now based on that information we need to create a *udev* rule to allow *others* to write to the device. Actually using *udev* again, we can print a more 'udev' friendly output, like this:

    moxz:~>udevadm info -a -p /devices/pci0000:00/0000:00:02.2/usb1/1-2
    Udevadm info starts with the device specified by the devpath and then
    walks up the chain of parent devices. It prints for every device
    found, all possible attributes in the udev rules key format.
    A rule to match, can be composed by the attributes of the device
    and the attributes from one single parent device.

    looking at device '/devices/pci0000:00/0000:00:02.2/usb1/1-2':
    KERNEL=="1-2"
    SUBSYSTEM=="usb"
    DRIVER=="usb"
    ATTR{configuration}==""
    ATTR{bNumInterfaces}==" 2"
    ATTR{bConfigurationValue}=="1"
    ATTR{bmAttributes}=="80"
    ATTR{bMaxPower}==" 2mA"
    ATTR{urbnum}=="2662"
    ATTR{idVendor}=="0bb4"
    ATTR{idProduct}=="0c86"
    ATTR{bcdDevice}=="0228"
    ATTR{bDeviceClass}=="00"
    ATTR{bDeviceSubClass}=="00"
    ATTR{bDeviceProtocol}=="00"
    ATTR{bNumConfigurations}=="1"
    ATTR{bMaxPacketSize0}=="64"
    ATTR{speed}=="12"
    ATTR{busnum}=="1"
    ATTR{devnum}=="19"
    ATTR{devpath}=="2"
    ATTR{version}==" 2.00"
    ATTR{maxchild}=="0"
    ATTR{quirks}=="0x0"
    ATTR{avoid_reset_quirk}=="0"
    ATTR{authorized}=="1"
    ATTR{manufacturer}=="HTC"
    ATTR{product}=="HTC"
    ATTR{serial}=="HT164T500742"


Now copying the above output, let's create a new rule file called **/etc/udev/rules.d/51-phone.rules** and put the following into it:

    SUBSYSTEM=="usb",ATTR{idVendor}=="0bb4",GROUP="elatov",MODE="0666"


The reason why the file is numbered 51 is because by default the system *udev* rules change the permission of all USB devices to *664* in rule number 50. Here is the file and line that does that:

    moxz:~>grep usb /lib/udev/rules.d/50-udev-default.rules | grep MODE
    SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0664"


So we need to make sure our rule loads after that one (therefore we are 51).Now let's reload the rules and restart the *udev* daemon:

    moxz:~>sudo udevadm control --reload-rules
    moxz:~>sudo systemctl restart udev
    moxz:~>sudo systemctl status udev
    udev.service - udev Kernel Device Manager
    Loaded: loaded (/usr/lib/systemd/system/udev.service; static)
    Active: active (running) since Tue, 05 Feb 2013 13:28:13 -0800; 5s ago
    Main PID: 28367 (udevd)
    CGroup: name=systemd:/system/udev.service
    └ 28367 /usr/lib/udev/udevd


That looks good. Now we have to uplug the device and plug it back it. First let's check out the current permissions on the USB device. Here is a list of the USB devices on the *Fedora* machine:

    moxz:~>lsusb
    Bus 001 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 001 Device 002: ID 413c:3200 Dell Computer Corp. Mouse
    Bus 001 Device 019: ID 0bb4:0c86 High Tech Computer Corp.


The last one is the phone (bus 001, device 019), now checking out the permissions of the file corresponding to that device, we see this:

    moxz:~>ls -l /dev/bus/usb/001/019
    crw-rw-r-- 1 root root 189, 18 Feb 5 13:06 /dev/bus/usb/001/019


Now unplugging the phone and plugging it back in, we see the following:

    moxz:~>lsusb
    Bus 001 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 001 Device 002: ID 413c:3200 Dell Computer Corp. Mouse
    Bus 001 Device 020: ID 0bb4:0c86 High Tech Computer Corp.


We can see that the device *ID* has changed. Now checking out the permissions of the new file:

    moxz:~>ls -l /dev/bus/usb/001/020
    crw-rw-rw- 1 root root 189, 19 Feb 5 13:31 /dev/bus/usb/001/020


That's all good. Now listing the available devices with **adb**, we see the following:

    moxz:~>adb devices
    List of devices attached
    HT164T500742 device


