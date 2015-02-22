---
published: true
layout: post
title: "Upgrade Gentoo to Use Systemd"
author: Karim Elatov
categories: [os]
tags: [linux,gentoo,systemd,lvm]
---
By default Gentoo uses **OpenRC** as it's init system. I have used **systemd** in the past so I decided to try converting Gentoo to use **systemd** as it's init system. Most of the steps are laid out [here](http://wiki.gentoo.org/wiki/Systemd).

### Prepare the Kernel

I was using the default linux sources so I just had to enable the following option:

    Gentoo Linux --->
            Support for init systems, system and service managers --->
                    [*] systemd

Here are the steps I took to recompile the kernel (and the modules... just in case):

    cd /usr/src/linux
    sudo make menuconfig **(enable the above option)**
    sudo cp .config ../.
    sudo make distclean
    sudo cp ../.config .
    sudo make oldconfig
    sudo make -j2
    sudo make install
    sudo make modules
    sudo make modules_install

Initially I used **genkernel** to generate the **initramfs** but I kept running into issues with mounting non-root LVM partitions ([systemd and lvm: timed out](http://forums.gentoo.org/viewtopic-t-989624-view-previous.html?sid=820e160dd073733d05d9d365131ab59c)), so I tried **genkernel-next** and the issue went away. Here is what I ran to update **genkernel**:

    sudo emerge -ac genkernel
    sudo emerge -av genkernel-next

And here is what I ran to generate the new **initramfs**:

    sudo genkernel --install --udev --lvm --no-ramdisk-modules initramfs

To ensure LVM partitions work out either enable **lvmetad** by having the following option in **/etc/lvm/lvm/conf**:

    use_lvmetad = 1

Or just enable the following services (after **systemd** is installed):

    sudo systemctl enable lvm2-lvmetad
    sudo systemctl enable lvm2-monitor

Last thing to do is create a symlink for **/etc/mtab**:

    sudo ln -sf /proc/self/mounts /etc/mtab

### Installing Systemd
I decided to enable the **systemd** USE flag globally, here is what I enabled (and disabled):

    sudo euse -E systemd
    sudo euse -D consolekit

and I also enabled the following at the package level:

    $ cat /etc/portage/package.use/systemd
    sys-apps/systemd gudev policykit

Now if I run **emerge** with the **--newuse** flag it will install the necessary packages. Here is what I ran to accomplish that:

    sudo emerge -avDN @world

### GRUB Configuration
To enable GRUB2 to use **systemd** we need to modify the following option under the **/etc/default/grub** file:

    $grep ^GRUB_CMDLINE_LINUX /etc/default/grub 
    GRUB_CMDLINE_LINUX="dolvm init=/usr/lib/systemd/systemd"

and then we need to regenerate the GRUB configuration:

    sudo grub2-mkconfig -o /boot/grub/grub.cfg

At this point we can reboot and the OS will boot up.

### Post systemd install
After I rebooted I noticed that networking didn't come up nor did the Display Manager (**lightdm**). So here is what I did to get gentoo back to the original state.

#### Configure Static IP
**Systemd** has a service (**systemd-networkd**) that can take of this, so first let's create the config:

    $ cat /etc/systemd/network/static.network
    [Match]
    Name=enp0s25

    [Network]
    Address=192.168.1.114/24
    Gateway=192.168.1.1

Then I enabled the service to start on boot and lastly I started the service:

    sudo systemctl enable systemd-networkd.service
    sudo systemctl start systemd-networkd.service

Lastly I set the hostname:

    sudo hostnamectl set-hostname gentoo.dnsd.me

#### Start missing services
Here are the services that had to re-enable after switching to **systemd**:

    sudo systemctl enable lightdm.service
    sudo systemctl enable bluetooth.service
    sudo systemctl enable syslog-ng.service
    sudo systemctl enable vixie-cron.service

#### Disable IPv6
For some reason **systemd** kept trying to enable the **ipv6** module during boot up (I didn't have anything under **/etc/modules-load.d** or **/usr/lib/modules-load.d**) so I ended creating a blacklist config:

    $cat /etc/modprobe.d/blacklist.conf 
    blacklist ipv6

And then after regenerating initramfs one more time:

    sudo genkernel --install --udev --lvm --no-ramdisk-modules initramfs

After a reboot the modules wasn't loaded any more, I had a static IP, and **lightdm** loaded .