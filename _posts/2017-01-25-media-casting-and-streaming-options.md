---
published: true
layout: post
title: "Media Casting and Streaming Options"
author: Karim Elatov
categories: [networking]
tags: [dial,upnp,airplay,ssdp,kodi,mdns,roap,miracast,wifi-direct,dlna,chromecast]
---
### ScreenCasting Options

It seems in this day and age we have so many options to cast or stream media to our TV.

#### Airplay

Of course everyone is familiar with Apple's **Airplay** technology. The best way to get this working is with an Apple TV. As soon as you configure it on your local network all your Apple Devices will see a mirror capable device and you can cast your whole screen to it:

![at-menu](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/at-menu.png&raw=1)

After you select you Apple TV device it will start casting to it and if you go back to the same menu you will see more options:

![at-casting](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/at-casting.png&raw=1)

And in **iTunes** you will also see it as an audio casting device:

![itunes-cast-menu](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/itunes-cast-menu.png&raw=1)

Airplay uses **mDNS**/**bonjour** for it's discovery capabilties, you can confirm by using **dns-sd** command:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 11:55:15]
	└─[0] <> dns-sd -B _airplay._tcp .
	Browsing for _airplay._tcp
	DATE: ---Sun 12 Jun 2016---
	11:55:20.767  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	11:55:20.768  Add        2   4 local.               _airplay._tcp.       Apple TV
	
	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 11:55:50]
	└─[130] <> dns-sd -B _raop._tcp .
	Browsing for _raop._tcp
	DATE: ---Sun 12 Jun 2016---
	11:55:56.099  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	11:55:56.100  Add        2   4 local.               _raop._tcp.          A0XXXXXXXX@Apple TV

If you query for it directly it will respond accordingly:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 12:00:39]
	└─[130] <> dns-sd -L "Apple TV" _airplay._tcp
	Lookup Apple TV._airplay._tcp.local
	DATE: ---Sun 12 Jun 2016---
	12:00:40.293  ...STARTING...
	12:00:40.572  Apple\032TV._airplay._tcp.local. can be reached at Apple-TV.local.:7000 (interface 4)
	 deviceid=XX:XX:XX:XX:XX:XX features=0x5A7FFFF7,0x1E flags=0x44 model=AppleTV3,2 pk=1xxxxxxxx81f18xxxx92da2d88dxxxxxxxx0808xxx pi=xxxx-xxx-xxxx-xxxx-xxxxxxxx srcvers=220.68 vv=2

You can also get a consise list of the **bonjour** services:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 11:56:54]
	└─[130] <> dns-sd -B _services._dns-sd._udp
	Browsing for _services._dns-sd._udp
	DATE: ---Sun 12 Jun 2016---
	11:56:55.011  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	11:56:55.012  Add        3   4 .                    _tcp.local.          _ssh
	11:56:55.012  Add        3   4 .                    _tcp.local.          _sftp-ssh
	11:56:55.012  Add        3   4 .                    _tcp.local.          _airplay
	11:56:55.012  Add        3   4 .                    _tcp.local.          _raop
	11:56:55.012  Add        2   4 .                    _tcp.local.          _touch-able
	11:56:55.188  Add        3   4 .                    _udp.local.          _sleep-proxy
	11:56:55.188  Add        2   4 .                    _tcp.local.          _workstation

There is actually an unofficial **airplay** guide available at [Unofficial AirPlay Protocol Specification](https://nto.github.io/AirPlay.html) and it covers all the services. For example **RAOP** is **Remote Audio Output Protocol** or **AirTunes**.

#### Airplay with Kodi

I have a Raspberry Pi (with OpenELEC) and it supports old IOS devices but with the new devices **airplay** doesn't work. After enabling it in **Kodi**:

![kodi-airplay-enabled](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/kodi-airplay-enabled.png&raw=1)

I wasn't able to use it for casting, the mirror option would show up but no devices would show up:

![no-kodi-in-menu](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/no-kodi-in-menu.png&raw=1)

I also noticed that it only shows up as an audio device and not a video device. **iTunes** would see it:

![itunes-kodi-menu](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/itunes-kodi-menu.png&raw=1)

And on my iPhone it showed up only for audio:

![iphone-airplay-kodi](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/iphone-airplay-kodi.png&raw=1)

It looks like the latest version of kodi might work out. Check out [Kodi AirPlay working with iOS 9.x devices](http://www.weirynet.com/blog/2016/01/20/kodi-airplay-working-with-ios-9) for more information. For now OpenELEC 6.0.3 is stable with Kodi 15.2 and I will wait for OpenELEC 7.0 to become stable which will be Kodi 16 (some people are waiting for that as [well](http://openelec.tv/forum/90-miscellaneous/80144-jarvis-kodi-version-out-soon)). Doing **bonjour** queries **kodi** responded:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 12:17:41]
	└─[130] <> dns-sd -B _raop._tcp .
	Browsing for _raop._tcp
	DATE: ---Sun 12 Jun 2016---
	12:17:51.789  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	12:17:51.791  Add        2   4 local.               _raop._tcp.          B827EB647504@Kodi (pi)
	
	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 12:17:54]
	└─[130] <> dns-sd -B _airplay._tcp .
	Browsing for _airplay._tcp
	DATE: ---Sun 12 Jun 2016---
	12:18:04.847  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	12:18:04.848  Add        3   4 local.               _airplay._tcp.       Apple TV
	12:18:04.848  Add        2   4 local.               _airplay._tcp.       Kodi (pi)
	
	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 12:18:06]
	└─[130] <> dns-sd -L "Kodi (pi)" _airplay._tcp
	Lookup Kodi (pi)._airplay._tcp.local
	DATE: ---Sun 12 Jun 2016---
	12:18:18.211  ...STARTING...
	12:18:18.436  Kodi\032(pi)._airplay._tcp.local. can be reached at pi.local.:36667 (interface 4)
	 features=0x20F7 srcvers=101.28 model=Xbmc,1 deviceid=XX:XX:XX:XX:XX:XX

But I was unable to screen cast (**airplay** mirror) to it. But it did offer some more services:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 12:17:30]
	└─[130] <> dns-sd -B _services._dns-sd._udp
	Browsing for _services._dns-sd._udp
	DATE: ---Sun 12 Jun 2016---
	12:17:32.560  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	12:17:32.561  Add        3   4 .                    _tcp.local.          _ssh
	12:17:32.561  Add        3   4 .                    _tcp.local.          _sftp-ssh
	12:17:32.561  Add        3   4 .                    _tcp.local.          _airplay
	12:17:32.561  Add        3   4 .                    _tcp.local.          _raop
	12:17:32.561  Add        3   4 .                    _tcp.local.          _touch-able
	12:17:32.561  Add        3   4 .                    _udp.local.          _sleep-proxy
	12:17:32.561  Add        3   4 .                    _tcp.local.          _workstation
	12:17:32.561  Add        3   4 .                    _tcp.local.          _http
	12:17:32.561  Add        3   4 .                    _tcp.local.          _xbmc-jsonrpc-h
	12:17:32.561  Add        3   4 .                    _tcp.local.          _xbmc-jsonrpc
	12:17:32.561  Add        2   4 .                    _udp.local.          _xbmc-events

#### Wi-Fi Direct

I have a Smart Samsung TV and it supports **Wi-Fi Direct** from [Wi-Fi Direct: what it is and why you should care](http://www.techradar.com/us/news/phone-and-communications/mobile-phones/wi-fi-direct-what-it-is-and-why-you-should-care-1065449)

> Wi-Fi Direct devices can connect to each other without having to go through an access point, that is to say you don't need to use your router.
> 
> This is because Wi-Fi Direct devices establish their own ad-hoc networks as and when required, letting you see which devices are available and choose which one you want to connect to.
> 
> If you think that sounds very like Bluetooth, that's because it is... only a lot faster.

More notes:

> Wi-Fi Direct is in DLNA, iOS, Android and BB OS and even your new Xbox
> 
> In November 2011, the Digital Living Network Alliance (DLNA) announced that it was including Wi-Fi Direct in its interoperability guidelines. Since then Google has added Wi-Fi Direct support to all versions of Android since Android 4.0 Ice Cream Sandwich.

The [wiki page](https://en.wikipedia.org/wiki/Wi-Fi_Direct) also has a bunch of good information:

> Mobile devices
> Google announced Wi-Fi Direct support in Android 4.0 in October 2011.[16] While some Android 2.3 devices like Samsung Galaxy S II have had this feature through proprietary operating system extensions developed by OEMs, the Galaxy Nexus (released November 2011) was the first Android device to ship with Google's implementation of this feature and an application programming interface for developers. Ozmo Devices, which developed integrated circuits (chips) designed for Wi-Fi Direct, was acquired by Atmel in 2012.
> 
> Wi-Fi Direct became available With the Blackberry 10.2 upgrade.
> 
> As of March 2016 iPhone devices do not implement Wi-Fi Direct, instead it has its own implementation
> 
> Game consoles
> The Xbox One, released in 2013, supports Wi-Fi Direct.
> 
> NVIDIA's SHIELD controller uses Wi-Fi Direct to connect to compatible devices. NVIDIA claims a reduction in latency and increase in throughput over competing Bluetooth controllers
> 
> Televisions
> In March 2016 Sony, LG and Philips have implemented Wi-Fi Direct on some of their televisions.

From the [How do I connect my smartphone or tablet to my TV using screen mirroring?](http://www.samsung.com/uk/support/skp/faq/1108504) page it talks about how it works:

> The Screen Mirroring feature is compatible with TVs that use WiFi direct technology. The first model that supported screen mirroring was the F range in 2013. You can check the age of your Samsung TV here. If your TV is older than the F range (2013) then you can still use screen mirroring via an Allshare Cast.
> 
> To try it out we can enable screen mirror on the TV and then with my adroind device I saw it an available device to cast to.

I just went to the screen mirroring source on the TV:

![sam-tv-enable-sm](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/sam-tv-enable-sm.jpg&raw=1)

And it showed how to connect the phone to it:

![sam-tv-screen-enabled](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/sam-tv-screen-enabled.jpg&raw=1)

Then from my android I went to the cast menu:

![and-cast-button.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/and-cast-button.png&raw=1)

Then I enabled the wireless display and I saw my TV:

![and-cast-enable-widi](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/and-cast-enable-widi.png&raw=1)

Unfortunately my iPhone wasn't able to use this feature.

#### Miracast

From the [wikipedia page](https://en.wikipedia.org/wiki/Miracast)

> Miracast is standard for peer-to-peer, Wi-Fi Direct wireless connections from devices (such as laptops, tablets, or smartphones) to displays. It allows sending up to 1080p HD video (H.264 codec) and 5.1 surround sound (AAC and AC3 are optional codecs, mandated codec is linear pulse-code modulation — 16 bits 48 kHz 2 channels). The connection is created via WPS and therefore is secured with WPA2. IPv4 is used on the internet layer. On the transport layer, TCP or UDP are used. On the application layer, the stream is initiated and controlled via RTSP, RTP for the data transfer. Adapters are available that plug into HDMI or USB ports that enable Non-Miracast devices to connect via Miracast.

Here is more about specific devices:

> The Wi-Fi Alliance maintains a current list of Miracast-certified devices, which features 5,007 devices as of April 26, 2016.
> 
> Nvidia announced support for it in their Tegra 3 platform, and Freescale Semiconductor, Texas Instruments, Qualcomm, Marvell Technology Group and other chip vendors have also announced their plans to support it.
> 
> Both devices (the sender and the receiver) need to be Miracast certified for the technology to work. However, to stream music and movies to a non-certified device there will be Miracast adapters available that plug into HDMI or USB ports.
> 
> On 29 October 2012, Google announced that Android version 4.2+ (from updated version of Jelly Bean) are supporting the Miracast wireless display standard, and by default have it integrated .
> 
> As of January 8, 2013, the LG Nexus 4 and Sony's Xperia Z, ZL, T and V officially support the function, as does HTC One, Motorola in their Droid Maxx & Ultra flagships, and Samsung in its Galaxy S III and Galaxy Note II under the moniker AllShare Cast. The Galaxy S4 uses Samsung Link for its implementation. In October 2013, BlackBerry released its 10.2.1 update to most of the existing BlackBerry 10 devices available at that time. As of March 2015, the BlackBerry Q10, Q5, Z30, and later models support Miracast streaming; the BlackBerry Z10 does not support Miracast, due to hardware limitations.
> 
> In April 2013, Rockchip unveiled a Miracast adapter powered by the RK2928.
> 
> Microsoft also added support for Miracast in Windows 8.1 (announced in June 2013). This functionality first became available in the Windows 8.1 Preview, and is available on hardware with supported Miracast drivers from hardware (GPU) manufacturers such as those listed above.
> 
> The WDTV Live Streaming Media Player added Miracast support with firmware version 2.02.32
> 
> The Amazon Fire TV Stick, which started shipping on 19 November 2014, also supports Miracast.
> 
> On 28 July 2013, Google announced the availability of the Chromecast powered by a Marvell DE3005-A1, but despite the similarity in name and Google's early support of Miracast in Android, the Chromecast does not support Miracast.
> 
> As of late April of 2016, the Ubuntu Touch powered Meizu Pro 5 supports Miracast in OTA-11.

And here is a note about OS Support:

> Miracast support is built into Android 4.2 or later and starting with Android 4.4, devices can be certified to the Wi-Fi Alliance Display Specification as Miracast compatible.[24] Miracast is also built into BlackBerry 10.2.1 devices and Microsoft Windows Phone 8.1 and Windows 8.1 released on October 2013. although developers can implement Miracast on top of the built-in Wi-Fi Direct support in Windows 7 and Windows 8. Another way to support Miracast in Windows is with Intel's proprietary WiDi (v3.5 or higher). Apple chooses not to support the Miracast standard on iOS or OS X. Apple uses its own proprietary Peer-to-peer AirPlay protocol instead on OS X. For the Linux desktop there exists MiracleCast which provides early support for miracast but is not tied to that single protocol. A software based Miracast receiver for Windows 8.1, AirServer Universal was made available on October 31, 2014 by App Dynamic.

From the Wi-Fi Direct wikipage it looks like **Miracast** is based on **Wi-Fi Direct**. The AllShare cast from Samsung (external HDMI Dongle) supports **Miracast**. **Roku** actually uses **Miracast** for it's screencasting capablities. More information can be seen at [Introducing Roku Screen Mirroring Beta for Microsoft Windows and Android Devices](https://blog.roku.com/blog/2014/10/02/introducing-roku-screen-mirroring-beta-for-microsoft-windows-and-android-devices/)

Just enable screen mirroring on the **Roku** side:

![roku-enable-screenmirror](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/roku-enable-screenmirror.png&raw=1)

and you will see the device available for casting, like on my android Nexus 5 phone:

![and-roku-seen](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/and-roku-seen.png&raw=1)

and I can cast to it:

![and-roku-conn](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/and-roku-conn.png&raw=1)

There are also good guides here for **Roku** Screen Mirroring:

* [How to Mirror Your Windows or Android Device’s Screen on Your Roku](http://www.howtogeek.com/214868/how-to-mirror-your-windows-or-android-devices-screen-on-your-roku/)
* [Screen Mirroring overview](https://support.roku.com/hc/en-us/articles/208754928)

It seems that not a lot of people don't see miracast as a good standard yet, from  [Wireless Display Standards Explained: AirPlay, Miracast, WiDi, Chromecast,and DLNA](http://www.howtogeek.com/177145/wireless-display-standards-explained-airplay-miracast-widi-chromecast-and-dlna/)

> In theory, Miracast is great. In practice, Miracast hasn’t worked out so well. While Miracast is theoretically a standard, there are only a handful of Miracast receivers out there that actually work well in practice. While devices are supposed to interface with other devices that support the standard, many Miracast-certified devices just don’t work (or don’t work well) with Miracast-certified receivers. The standard seems to have collapsed in practice — it’s not really a standard. Check out this table of test results to see just how much of an incompatible mess Miracast seems to be.

and also from  [Airplay, DLNA, Chromecast and miracast…What's the
Difference?](http://creation.com.es/news/wireless-display-standards/)

> The biggest drawback to Miracast, apart from the mess of incompatibilities? It only offers "dumb mirroring". Unlike Apple TV, which hides your playback controls on the TV, Miracast shows everything - playback controls, battery life, signal and wi-fi reception, etc. When Miracast does work, it's ugly.

I haven't seen Apple Devices work with **Miracast**.

#### DIAL

There is a unique protocol that is only available for youtube and netflix, it's called **DIAL** (Discover and Launch). From the [wikipedia page](https://en.wikipedia.org/wiki/Discovery_and_Launch):

> DIAL, an acronym for DIscovery And Launch, is a protocol co-developed by Netflix and YouTube with help from Sony and Samsung. It is a mechanism for discovering and launching applications on a single subnet, typically a home network. It relies on Universal Plug and Play (UPnP), Simple Service Discovery Protocol (SSDP), and HTTP protocols. The protocol works without requiring a pairing between devices. It was formerly used by the Chromecast media streaming adapter that was introduced in July 2013 by Google. (Chromecast now uses mDNS instead of DIAL.)

Since it uses **SSDP** we can query for it. Here is what I saw on my TV:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 02:59:26]
	└─[0] <> gssdp-discover -i en0  --timeout=3 -t urn:dial-multiscreen-org:device:dialreceiver:1
	Using network interface en0
	Scanning for resources matching urn:dial-multiscreen-org:device:dialreceiver:1
	Showing "available" messages
	resource available
	  USN:      uuid:b2fed0ab-2e24-4680-9d2a-75061c85fe23::urn:dial-multiscreen-org:device:dialreceiver:1
	  Location: http://192.168.1.119:7678/nservice/

**Roku** can act as a sender but not as a reciever:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 03:02:47]
	└─[0] <> gssdp-discover -i en0  --timeout=3 -t urn:dial-multiscreen-org:service:dial:1
	Using network interface en0
	Scanning for resources matching urn:dial-multiscreen-org:service:dial:1
	Showing "available" messages
	resource available
	  USN:      uuid:b2fed0ab-2e24-4680-9d2a-75061c85fe23::urn:dial-multiscreen-org:service:dial:1
	  Location: http://192.168.1.119:7678/nservice/
	resource available
	  USN:      uuid:015de0c8-9401-10fa-80d5-b83e59b04353::urn:dial-multiscreen-org:service:dial:1
	  Location: http://192.168.1.121:8060/dial/dd.xml

Both my TV and the **Roku** can act as **DIAL** clients. To use **DIAL** just launch a **youtube** video in chrome and there will be an option to cast that video to a **DIAL** capable device:

![youtu-dial-tv](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/youtu-dial-tv.png&raw=1)

#### DLNA

I have talked about **DLNA** in the [past post](/2012/10/installing-mediatomb-on-freebsd-9-and-connecting-to-it-with-xbmc-from-a-fedora-17-os/). With **DLNA** there are **Media Servers** and Media **Renderers**. **Media Servers** can serve media to you. So I have a **Plex** server and that's my **Media Server**. We can query it with **SSDP**:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 03:19:16]
	└─[0] <> gssdp-discover -i en0  --timeout=3 --target=urn:schemas-upnp-org:device:MediaServer:1
	Using network interface en0
	Scanning for resources matching urn:schemas-upnp-org:device:MediaServer:1
	Showing "available" messages
	resource available
	  USN:      uuid:1d315878-62e5-cd83-6dcb-320fd356c39c::urn:schemas-upnp-org:device:MediaServer:1
	  Location: http://192.168.1.100:32469/DeviceDescription.xml

On the **Kodi** side I went ahead and enabled it to be a **DLNA Renderer**:

![kodi-enable-upnp-mr](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/kodi-enable-upnp-mr.png&raw=1)

and now both my TV and Raspberry Pi can accept media streams:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-12 03:22:08]
	└─[0] <> gssdp-discover -i en0  --timeout=3 -t urn:schemas-upnp-org:device:MediaRenderer:1
	Using network interface en0
	Scanning for resources matching urn:schemas-upnp-org:device:MediaRenderer:1
	Showing "available" messages
	resource available
	  USN:      uuid:1c96c992-45b4-4658-bb39-e7e27f690a3c::urn:schemas-upnp-org:device:MediaRenderer:1
	  Location: http://192.168.1.119:9197/dmr
	resource available
	  USN:      uuid:99ef8607-8994-b032-13a4-3525f3eddc56::urn:schemas-upnp-org:device:MediaRenderer:1
	  Location: http://192.168.1.108:1812/


Now we can use mobile apps like **BubbleUPNP**, **mConnect Free**, and **TV Cast for DLNA** to stream files to either device. In **BubbleUPNP** I see all my **DLNA** devices (Renderers and Servers):

![bu-ren-ser-seen](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/bu-ren-ser-seen.png&raw=1)

And on iPhone, I see both of my devices are Renderers:

![iphone-co-dlna](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/iphone-co-dlna.png&raw=1)

After that I can pick a designated **Renderer** (Kodi or Sasmsung TV) and then I can stream movies from **Plex** to the **Renderer** with my phone as the middle man. This isn't true screencasting but it still helps out.

#### Chromecast
Reading over a bunch of sites, it sounds like **chromecast** might be best option for cross platform support. From [How to Mirror your Android Device to your TV or Second Screen](http://techpp.com/2013/11/21/mirror-android-screen-tv/):

> You should also take a look at Google’s latest product, Chromecast that is able to stream media from any Android device, smartphone or tablet, to a TV.

And from [How to Stream Video to a TV from a Mobile Device or
Computer](http://www.tomsguide.com/us/how-to-stream-to-tv,news-18335.html):

> I Have A Mixture Of Apple Devices And Windows Or Android Devices. What Should I Use To Stream Video?
> Get Google Chromecast or Android TV, but check your hardware and software.

And just for comparison, from [Swordfight! Streaming sticks from Google, Roku, and Amazon compared](http://www.digitaltrends.com/home-theater/chromecast-vs-roku-streaming-stick-vs-amazon-fire-tv-stick)

![media-stick-comparison](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/media-stick-comparison.png&raw=1)

It looks like **chromecast** has the best support. The [Best Miracast and Screen-Mirroring Devices 2016](http://www.tomsguide.com/us/best-miracast-screen-mirroring,review-2286.html) provides recommendation per OS and it might be worth checking out, if you
are a pure windows or apple shop. Most of my streaming needs are covered with **Plex** and **Kodi**, I just wanted to find out if any of my existing devices covers all the platforms and it doesn't look like it. 

For **chromecast**, it supports both **DIAL** and **mDNS** more information is seen in [Chromecast Implementation Documentation WIP](https://github.com/jloutsenhizer/CR-Cast/wiki/Chromecast-Implementation-Documentation-WIP):

> Two protocols are implemented on Chromecast to support discovery, the first is an implementation of the DIAL Protocol over SSDP. This is the primary system used for the old v1 of Google Cast SDK. The second protocol implemented is an mDNS server. This is the primary way of discovering a Chromecast that supports the v2 API.


Here is the **ssdp** query:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-19 10:11:12]
	└─[0] <> gssdp-discover -i en0  --timeout=3 --target=urn:dial-multiscreen-org:device:dial:1
	Using network interface en0
	Scanning for resources matching urn:dial-multiscreen-org:device:dial:1
	Showing "available" messages
	resource available
	  USN:      uuid:27c289a4-b46e-d050-846a-7cdcd1411ecc::urn:dial-multiscreen-org:device:dial:1
	  Location: http://192.168.1.105:8008/ssdp/device-desc.xml

and here is the **mDNS** query:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-19 10:19:17]
	└─[130] <> dns-sd -B _googlecast._tcp .
	Browsing for _googlecast._tcp
	DATE: ---Sun 19 Jun 2016---
	10:19:24.090  ...STARTING...
	Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
	10:19:24.091  Add        2   4 local.               _googlecast._tcp.    K_Chromecast

And here is more information:

	┌─[elatov@macair] - [/Users/elatov] - [2016-06-19 10:19:31]
	└─[130] <> dns-sd -L "K_Chromecast" _googlecast._tcp .
	Lookup K_Chromecast._googlecast._tcp.local
	DATE: ---Sun 19 Jun 2016---
	10:20:18.307  ...STARTING...
	10:20:18.308  K_Chromecast._googlecast._tcp.local. can be reached at K_Chromecast.local.:8009 (interface 4)
	id=xxxxxxxxxxxxxx rm= ve=05 md=Chromecast ic=/setup/icon.png fn=K_Chromecast ca=4101 st=1 bs=XXXXXXX rs=

Once in chrome you can cast any tab or the whole screen:

![c-options-menu](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/c-options-menu.png&raw=1)

Then you can choose what screen to cast:

![c-share-screen](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/c-share-screen.png&raw=1)

And after that the casting will start and you can see the status from the same location:

![c-cast-going](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/c-cast-going.png&raw=1)

You can also download the **Google Cast** mobile app and cast your phone screen to it:

![and-gca-cast](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/and-gca-cast.png&raw=1)

Now adays a lot of apps support chrome cast as well and you will see your casting icon within the app and it will list your **chromecast**. Here is the **plex** app:

![plex-app-cc](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/plex-app-cc.png&raw=1)

and here is **pandora**:

![pan-cast-cc](https://seacloud.cc/d/480b5e8fcd/files/?p=/screen-cast/pan-cast-cc.png&raw=1)
