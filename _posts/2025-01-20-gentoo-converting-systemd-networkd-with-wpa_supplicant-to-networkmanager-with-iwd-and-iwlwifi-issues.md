---
published: true
layout: post
title: "Gentoo: Converting systemd networkd with wpa_supplicant to NetworkManager with iwd and iwlwifi issues"
author: Karim Elatov
categories: [os, networking]
tags: [gentoo, networkmanager, wifi, iwd, systemd-networkd]
---

## iwlwifi module issues
I came back home one day and my machine running gentoo was having issues connecting to the internet. I looked at the logs and I saw the following:

```
Jan 05 17:44:16 nuc systemd-networkd[645]: wlp0s20f3: Gained carrier
Jan 05 17:44:16 nuc wpa_supplicant[878]: wlp0s20f3: CTRL-EVENT-CONNECTED - Connection to xx:xx:xx:xx:xx:xx completed [id=0 id_str=]
Jan 05 17:44:16 nuc wpa_supplicant[878]: wlp0s20f3: WPA: Key negotiation completed with xx:xx:xx:xx:xx:xx [PTK=CCMP GTK=CCMP]
Jan 05 17:44:16 nuc wpa_supplicant[878]: wlp0s20f3: CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
lines 2651-2709
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x01000000 | umac data1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x804737A2 | umac interruptlink2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x804737A2 | umac interruptlink1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x804561E2 | umac branchlink2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | umac branchlink1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x20000066 | NMI_INTERRUPT_HOST
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Transport status: 0x0000004A, valid: 7
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Start IWL Error Log Dump:
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x000098E0 | flow_handler
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | timestamp
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000009 | lmpm_pmg_sel
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x000000CE | l2p_addr_match
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x0000003F | l2p_mhvalid
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | l2p_duration
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000080 | l2p_control
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00015322 | wait_event
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00550103 | last cmd Id
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | isr4
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00C32818 | isr3
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x08F00002 | isr2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x01000000 | isr1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x20028000 | isr0
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x80AFFD4F | hcmd
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x18C89001 | board version
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000351 | hw version
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x0B4C06AD | uCode version minor
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x0000004D | uCode version major
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000001 | uCode revision type
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00D7483F | time gp2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | time gp1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x0000009C | tsf hi
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x456B27F7 | tsf low
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x18C05A16 | beacon time
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | data3
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x01000000 | data2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00015322 | data1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x004BF3A6 | interruptlink2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x004BF3A6 | interruptlink1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x004C94FA | branchlink2
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000000 | trm_hw_status1
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x0000A2F0 | trm_hw_status0
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: 0x00000084 | NMI_INTERRUPT_UNKNOWN
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Loaded firmware version: 77.0b4c06ad.0 QuZ-a0-hr-b0-77.ucode
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Transport status: 0x0000004A, valid: 6
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Start IWL Error Log Dump:
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Microcode SW error detected. Restarting 0x0.
Jan 05 17:44:26 nuc kernel: iwlwifi 0000:00:14.3: Queue 3 is stuck 0 3
```

I ran into this thread [[SOLVED] [GOOGLE NEST] 11n_disable=1 needed](https://bbs.archlinux.org/viewtopic.php?id=278344) and as a quick test I wanted to use my phone as a hot spot to see if that helps out. 

## Connecting to WiFi with systemd-networkd and wpa_supplicant
A while back I configured my machine to connect to my WiFI using [systemd-networkd](https://wiki.gentoo.org/wiki/Systemd/systemd-networkd#Wireless_card). So first I created this file:

```
> cat /etc/systemd/network/51-wifi-dhcp.network
[Match]
Name=wl*

[Network]
DHCP=yes
IgnoreCarrierLoss=3s

[DHCPv4]
RouteMetric=20
```

For DNS, we can configure the following:

```
ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
systemctl enable --now systemd-resolved.service
```

You can check it's working:

```
> resolvectl status wlan0
Link 5 (wlan0)
    Current Scopes: DNS LLMNR/IPv4 LLMNR/IPv6 mDNS/IPv4 mDNS/IPv6
         Protocols: +DefaultRoute +LLMNR +mDNS -DNSOverTLS DNSSEC=allow-downgrade/supported
Current DNS Server: 192.168.1.1
       DNS Servers: 192.168.1.1
        DNS Domain: local.int
```        

Since we are using DHCP we will need to intall [dhcpd](https://wiki.gentoo.org/wiki/Network_management_using_DHCPCD#Setup):

```
emerge --ask net-misc/dhcpcd
```

And then we can start it:

```
systemctl enable dhcpcd
systemctl start dhcpcd
```

Lastly I needed to install `wpa_supplicant`:

```
emerge --ask net-wireless/wpa_supplicant
```

And I needed to create the configuration:

```
cat > /tmp/file.txt <<EOF
# Allow users in the 'wheel' group to control wpa_supplicant
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
 
# Make this file writable for wpa_gui / wpa_cli
update_config=1
EOF
```

Now let's add the password to the configuration file:

```
wpa_passphrase WIRELESS_AP PASSWD12 >> /tmp/file.txt
```

And finally let's store it in the right directory:

```
mv /tmp/file.txt /etc/wpa_supplicant/wpa_supplicant-wlp0s20f3.conf
```

Now let's enable the service:

```
ln -s /lib/systemd/system/wpa_supplicant@.service /etc/systemd/system/multi-user.target.wants/wpa_supplicant@wlp0s20f3.service
systemctl daemon-reload
systemctl start wpa_supplicant@wlp0s20f3
```

After that the wifi should get connected. I also used [iw](https://wiki.gentoo.org/wiki/Wi-Fi#iw_command) to confirm the settings:

```
emerge -avu net-wireless/iw
```

And then:

```
> iw dev wlan0 info
Interface wlan0
	ifindex 5
	wdev 0x2
	addr xx:xx:xx:xx:xx:xx
	ssid WIRELESS_AP
	type managed
	wiphy 0
	channel 140 (5700 MHz), width: 40 MHz, center1: 5710 MHz
	txpower 22.00 dBm
	multicast TXQ:
		qsz-byt	qsz-pkt	flows	drops	marks	overlmt	hashcol	tx-bytes	tx-packets
		0	0	0	0	0	0	0	0		0
```	

Or:

```
> iw dev wlan0 link
Connected to xx:xx:xx:xx:xx:xx (on wlan0)
	SSID: WIRELESS_AP
	freq: 5700.0
	RX: 580528697 bytes (718004 packets)
	TX: 328581524 bytes (183939 packets)
	signal: -45 dBm
	rx bitrate: 300.0 MBit/s MCS 15 40MHz short GI
	tx bitrate: 300.0 MBit/s MCS 15 40MHz short GI
	bss flags: short-slot-time
	dtim period: 3
	beacon int: 100
```	

## Connecting to WiFi with NetworkManager and iwd
In the past I wasn't a big fan of [NetworkManager](https://networkmanager.dev/docs/), but in the recent years I've seen more and more distros use it so I decided to give it a try as well. Most of the setup is covered in [NetworkManager](https://wiki.gentoo.org/wiki/NetworkManager), first enable the `USE` flags:

```
echo "USE=\"\${USE} networkmanager\"" >> /etc/portage/make.conf
```

Then rebuild:

```
emerge --ask --changed-use --deep @world
```

I then needed to enable `iwd` since `networkmamanager` works well with that over `wpa_supplicant`, while I was at it, I decided to keep `dhcpd` (in case I ever want to switch back to the `systemd-networkd` setup):

```
echo "net-misc/networkmanager dhcpcd iwd" >> /etc/portage/package.use/networkmanager
```

Then reinstalled `networkmanager`:

```
emerge --ask --newuse net-misc/networkmanager
```

To allow regular users to connect to the wifi make sure to add them to the `plugdev` user:

```
gpasswd -a USER plugdev
```

### Switching from systemd-networkd to NetworkManager
So let's disable the previous configuration:

```
systemctl disable --now wpa_supplicant
systemctl disable --now systemd-networkd
```

And let's switch over:

```
systemctl enable --now NetworkManager
```

Initially I couldn't see any networks, when I ran `nmcli device wifi list`. And then I realized `rfkill` is blocking the interface:

```
Jan 05 19:31:46 nuc iwd[14198]: Error bringing interface 6 up: Operation not possible due to RF-kill
```

It was just a coincidence since I just read [wpa_supplicant](https://wiki.gentoo.org/wiki/Wpa_supplicant#rfkill:_WLAN_soft_blocked), so I just unblocked it:

```
sudo rfkill unblock 1
```

And then I saw the networks:

```
> nmcli device wifi list
IN-USE  BSSID              SSID                             MODE   CHAN  RATE       SIGNAL  BARS  SECURITY
        xx:xx:xx:xx:xx:xx  Verizon_XXXXXX                   Infra  2     65 Mbit/s  75      ▂▄▆_  WPA2
        xx:xx:xx:xx:xx:xx  Verizon_XXXXXX                   Infra  140   65 Mbit/s  75      ▂▄▆_  WPA2
        xx:xx:xx:xx:xx:xx  DIRECT-91-HP OfficeJet Pro 9010  Infra  2     65 Mbit/s  55      ▂▄__  WPA2
```        

I also made sure I could see the networks with `iwd`:

```
> iwctl adapter list
                                    Adapters
--------------------------------------------------------------------------------
  Name      Powered   Vendor                Model
--------------------------------------------------------------------------------
  phy0      on        Intel Corporation     Comet Lake PCH-LP
                                            CNVi WiFi (Dual Band
                                            Wi-Fi 6(802.11ax)
                                            AX201 160MHz 2x2
                                            [Harrison Peak])
```

To see the name of the interface:

```
> iwctl station list
                            Devices in Station Mode
--------------------------------------------------------------------------------
  Name                  State            Scanning
--------------------------------------------------------------------------------
  wlan0                 connected
```

Then send the `scan` request:

```
> iwctl station wlan0 scan
```

And lastly check out the APs:

```
> iwctl station wlan0 get-networks
                               Available networks
--------------------------------------------------------------------------------
      Network name                      Security            Signal
--------------------------------------------------------------------------------
      Verizon_XXXXXX                    psk                 ****
      XXXXXX_2G                         psk                 ****
      cooliodjddj                       psk                 ****
```

And I was able to use [nm-applet](https://wiki.gentoo.org/wiki/NetworkManager#GTK_GUIs) to connect to the other Wireless AP.

## iwlwifi module options
I started reading up on `iwlwifi` and it looks like there are known issues:

- [iwlwifi](https://wiki.gentoo.org/wiki/Iwlwifi#.22Microcode_SW_error_detected._Restarting_0x0.22_message_in_kernel_logs)
- [Freezing/Lag Spikes caused by iwlwifi [SOLVED]](https://bbs.archlinux.org/viewtopic.php?id=277833)
- [After upgrading to Linux 5.18.11 from 5.18.9, My WiFi problems have](https://bbs.archlinux.org/viewtopic.php?pid=2048944)

I tried a variety of options, and after changing the module parameters, I ran the following to apply the changes

```
sudo rmmod iwlmvm iwlwifi
sudo modprobe iwlwifi
```

But the only thing that helped was `11n_disable=1`, but that would limit my speed to ~10mbps (similar issue is described [here](https://bbs.archlinux.org/viewtopic.php?id=278344) and [here](https://forum.manjaro.org/t/internet-speed-is-slow/103443/26?page=2)). So then as a quick test I only set this option `disable_11ax=1` and then my speeds went up:

```
> speedtest
Retrieving speedtest.net configuration...
Testing from Verizon Fios (xx.xx.xx.xx)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by yaemi.one (Jersey City, NJ) [0.38 km]: 13.653 ms
Testing download speed................................................................................
Download: 330.33 Mbit/s
Testing upload speed......................................................................................................
Upload: 331.72 Mbit/s
```
