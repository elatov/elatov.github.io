---
published: true
layout: post
title: "Update Debian and XBMC on Late 2006 MacMini"
author: Karim Elatov
categories: [os,networking]
tags: [debian,kodi,xbmc,systemd]
---
A while ago I ended up installing Debian 7 on an old MacMini (check out [this](/2014/09/install-debian-7-on-macmini-late-2006/) post on the Debian Install and [this](/2014/11/running-xbmc-11-on-mac-mini-late-2006/) one for the XMBC setup), and I decided to updated the OS and XBMC to Kodi.

### Update to Debian 8
I ended following similar instructions as I did in the past (the steps are covered in [this](/2015/06/upgrade-debian-wheezy7-to-jessie8/) post). Create backups:

	dpkg --get-selections "*" > /tmp/dpkg-jessie.txt
	sudo tar cpvjf deb-jess.tar.bz2 /etc /var/lib/dpkg /var/lib/apt/extended_states /tmp/dpkg-jessie.txt

Check consistency of packages:

	sudo  dpkg --audit

Check to make sure no packages are onhold

	aptitude search "~ahold"

Update the apt repos
	
	sudo sed -i "s/wheezy/jessie/" /etc/apt/sources.list

Now let's update the apt repos cache

	sudo apt-get update

Upgrade all the packages

	sudo apt-get upgrade

Next let's upgrade the system

	sudo apt-get dist-upgrade

Then reboot and make sure it comes up okay

	sudo reboot

After the reboot I removed unused packages

	sudo apt-get autoremove --purge

### Update XBMC to Kodi
I didn't have much configured so I uninstalled xbmc completely

	sudo service xbmc stop
	sudo apt-get remove xbmc xbmc-bin --purge

Since I was planning on using **systemd** now, I also removed the init script:

	elatov@deb:~$ sudo update-rc.d xbmc remove
	elatov@deb:~$ sudo mv /etc/init.d/xbmc .

Now let's install kodi, first we need to enable backports as desribed per [this](http://kodi.wiki/view/HOW-TO:Install_Kodi_for_Linux) page. This is done by adding this line to the **/etc/apt/sources.list** file :

	# jessie backports
	deb http://http.debian.net/debian jessie-backports main

Then update the apt cache:

	sudo apt-get update

Then we will see the kodi package:

	elatov@deb:~$ apt-cache showpkg kodi | grep ^Versions -A 1
	Versions:
	15.2+dfsg1-1~bpo8+1 (/var/lib/apt/lists/http.debian.net_debian_dists_jessie-backports_main_binary-i386_Packages)

Now let's install it:

	sudo apt-get install kodi

Then remove old packages:

	sudo apt-get autoremove --purge

Then create the systemd script, taken from [here](http://kodi.wiki/view/HOW-TO:Autostart_XBMC_for_Linux):


	elatov@deb:~$ cat /etc/systemd/system/kodi.service
	[Unit]
	Description = Kodi Media Center
	
	# if you don't need the MySQL DB backend, this should be sufficient
	After = systemd-user-sessions.service network.target sound.target
	
	# if you need the MySQL DB backend, use this block instead of the previous
	# After = systemd-user-sessions.service network.target sound.target mysql.service
	# Wants = mysql.service
	
	[Service]
	User = kodi
	Group = kodi
	Type = simple
	#PAMName = login # you might want to try this one, did not work on all systems
	ExecStart = /usr/bin/xinit /usr/bin/dbus-launch --exit-with-session /usr/bin/kodi-standalone -- :0 -nolisten tcp vt7
	Restart = on-abort
	RestartSec = 5
	
	[Install]
	WantedBy = multi-user.target

I was missing the **dbus-launch** command and I installed it

	sudo apt-get install dbus-x11

After that all the commands were all there:

	elatov@deb:~$ which xinit
	/usr/bin/xinit
	elatov@deb:~$ which dbus-launch
	/usr/bin/dbus-launch
	elatov@deb:~$ which kodi-standalone
	/usr/bin/kodi-standalone

Then make sure it works

	sudo systemctl start kodi

And lastly enable it to start on boot

	sudo systemctl enable kodi

To make sure everything is working as expected reboot one more time:

	sudo reboot

### Enable Wireless Connection With Systemd
**Systemd** provides another daemon which can take care of the a wireless connection. It's called **networkd**, I ran into a couple of sites which had instructions on the setup: 

* [systemd-networkd with wpa_supplicant to manage wireless with roaming support](https://beaveris.me/systemd-networkd-with-roaming/)
* [Switching to systemd-networkd](https://www.joachim-breitner.de/blog/664-Switching_to_systemd-networkd)
* [Using systemd-networkd with wpa_supplicant to manage wireless network configuration with roaming](http://blog.volcanis.me/2014/06/01/systemd-networkd/)

Since we are using **systemd**, let's try to configure wireless networking with it. First let's create the wpa configuration

	elatov@deb:~$ cat /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
	ctrl_interface=/var/run/wpa_supplicant
	eapol_version=1
	ap_scan=1
	fast_reauth=1

Then add your password info to it

	root@deb:~# wpa_passphrase my_access_point pw >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

Then create the interface configuration:

	elatov@deb:~$ cat /etc/systemd/network/wlan0.network
	[Match]
	Name=wlan0
	[Network]
	#DHCP=yes
	DNS=192.168.1.1
	Address=192.168.1.115/24
	Gateway=192.168.1.1

Lastly let's create a service for WPA per interface:

	elatov@deb:~$ cat /lib/systemd/system/wpa_supplicant@.service
	[Unit]
	Description=WPA supplicant daemon (interface-specific version)
	Requires=sys-subsystem-net-devices-%i.device
	After=sys-subsystem-net-devices-%i.device
	
	[Service]
	Type=simple
	ExecStart=/sbin/wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant-%I.conf -i%I -Dwext
	
	[Install]
	Alias=multi-user.target.wants/wpa_supplicant@%i.service

Then let's remove **resolv.conf** since that's created by **systemd**:

	elatov@deb:~$ sudo mv /etc/resolv.conf ~/.

Now let's enable the appropriate services:

	sudo systemctl enable systemd-networkd
	sudo systemctl enable wpa_supplicant@wlan0
	sudo systemctl enable systemd-resolved

Finally you can start up the services:

	sudo systemctl start systemd-networkd
	sudo systemctl start wpa_supplicant@wlan0
	sudo systemctl start systemd-resolved

And now let's create the symlink:

	sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

Also let's go ahead and setup NTP, first let's disable RTC:

	elatov@deb:~$ sudo timedatectl set-local-rtc 0

Next let's enable NTP:

	elatov@deb:~$ sudo timedatectl set-ntp 1

Lastly let's confirm it's working:

	elatov@deb:~timedatectl status
	      Local time: Sun 2016-02-14 10:25:00 MST
	  Universal time: Sun 2016-02-14 17:25:00 UTC
	        RTC time: Sun 2016-02-14 10:25:00
	       Time zone: America/Denver (MST, -0700)
	     NTP enabled: yes
	NTP synchronized: yes
	 RTC in local TZ: no
	      DST active: no
	 Last DST change: DST ended at
	                  Sun 2015-11-01 01:59:59 MDT
	                  Sun 2015-11-01 01:00:00 MST
	 Next DST change: DST begins (the clock jumps one hour forward) at
	                  Sun 2016-03-13 01:59:59 MST
	                  Sun 2016-03-13 03:00:00 MDT

And also confirm your wireless nic is up:

	elatov@deb:~$ ip link show wlan0
	3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DORMANT group default qlen 1000
	    link/ether 00:17:f2:53:e0:59 brd ff:ff:ff:ff:ff:ff

And the IP assigned:

	elatov@deb:~$ ip -4 a s wlan0
	3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
	    inet 192.168.1.115/24 brd 192.168.1.255 scope global wlan0
	       valid_lft forever preferred_lft forever
	
	welatov@deb:~$ iwconfig wlan0
	wlan0     IEEE 802.11abg  ESSID:"my_access_point"
	          Mode:Managed  Frequency:5.26 GHz  Access Point: 78:24:AF:7B:1F:0C
	          Bit Rate=54 Mb/s   Tx-Power=30 dBm
	          Retry short limit:7   RTS thr:off   Fragment thr:off
	          Power Management:off
	          Link Quality=63/70  Signal level=-47 dBm
	          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
	          Tx excessive retries:0  Invalid misc:4   Missed beacon:0

If you had anything in the **/etc/network/interfaces** file, remove it by commenting it out.

I feel like the combination of Debian 8 and Kodi 15 on the Late 2006 MacMini added a bunch of stuttering to HD videos with higher qualities, so if you like the original setup, I would leave it and not update it.

