---
title: Installing Subsonic on Fedora 17
author: Karim Elatov
layout: post
permalink: /2012/10/installing-subsonic-on-fedora-17/
dsq_thread_id:
  - 1415422076
categories:
  - Home Lab
tags:
  - iptables
  - java-openjdk
  - rpm
  - subsonic
  - systemctl
  - update-alternatives
---
I recently posted on <a href="http://virtuallyhyper.com/2012/10/installing-mediatomb-on-freebsd-9-and-connecting-to-it-with-xbmc-from-a-fedora-17-os/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/installing-mediatomb-on-freebsd-9-and-connecting-to-it-with-xbmc-from-a-fedora-17-os/']);">how to setup MediaTomb on FreeBSD</a>, and I had an extra box laying around which I wanted to dedicate for audio streaming. MediaTomb would take care of Videos but I wanted another dedicated machine to handle my Music streaming. As I was doing some research I found a list of some available audio streaming software from wikipedia: "<a href="http://en.wikipedia.org/wiki/List_of_streaming_media_systems#Servers" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/List_of_streaming_media_systems#Servers']);">List of streaming media systems</a>". Here are the ones that stood out:

*   <a title="Firefly Media Server" href="http://en.wikipedia.org/wiki/Firefly_Media_Server" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Firefly_Media_Server']);">Firefly Media Server</a>
*   <a title="Squeezebox Server" href="http://en.wikipedia.org/wiki/Squeezebox_Server" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Squeezebox_Server']);">Squeezebox Server</a>
*   <a title="Ampache" href="http://en.wikipedia.org/wiki/Ampache" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Ampache']);">Ampache</a>
*   <a title="Subsonic (media server)" href="http://en.wikipedia.org/wiki/Subsonic_(media_server)" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Subsonic_(media_server)']);">Subsonic</a>
*   <a href="http://sourceforge.net/projects/jinzora/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sourceforge.net/projects/jinzora/']);">Jinzora</a>

I kept reading other forums and here is what I came across:

<a href="http://forum.subsonic.org/forum/viewtopic.php?t=564" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.subsonic.org/forum/viewtopic.php?t=564']);">Subsonic vs. Jinzora</a> (+1 Subsonic -1 Jinzora)  
<a href="http://ubuntuforums.org/showthread.php?t=1581344" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://ubuntuforums.org/showthread.php?t=1581344']);">Subsonic vs Ampache</a> (+1 Subsonic -1 AmPache)  
<a href="http://blog.lundscape.com/2009/05/install-subsonic-on-ubuntu-server/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.lundscape.com/2009/05/install-subsonic-on-ubuntu-server/']);">Install Subsonic on Ubuntu Server</a> (+1 SubSonic -1 Firefly -1 Jinzora)

It seemed that everyone was really liking SubSonic. I actually used SqueezeBox a while back and I really liked it , but I wanted to try something new. So I decided to try SubSonic, here are steps I followed to setup SubSonic on my Fedora machine.

### 1. Install the Necessary Pre-requisites

Most of the instructions are laid out in "<a href="http://www.subsonic.org/pages/installation.jsp" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.subsonic.org/pages/installation.jsp']);">Installing Subsonic</a>" page, but I had to make some changes to accommodate to my OS:

	  
	moxz:~> yum install java-1.7.0-openjdk  
	

If you are planning to do some transcoding, install additional codecs. To do so, first enable the repo for free codecs:

	  
	moxz:~>rpm -ivh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm  
	

After that install the necessary codecs:

	  
	moxz:~> yum install lame flac faad2 vorbis-tools ffmpeg  
	

### 2. Install the SubSonic Package

From the install page, download the rpm and then install it:

	  
	moxz:~>sudo rpm -ivh subsonic-4.7.rpm  
	Preparing... ########################################### [100%]  
	1:subsonic ########################################### [100%]  
	Starting subsonic (via systemctl):  
	

The install actually includes it's own transcoding application binaries:

	  
	moxz:~> rpm -ql subsonic-4.7-3105.i386  
	/etc/init.d/subsonic  
	/etc/sysconfig/subsonic  
	/usr/share/subsonic/subsonic-booter-jar-with-dependencies.jar  
	/usr/share/subsonic/subsonic.sh  
	/usr/share/subsonic/subsonic.war  
	/var/subsonic/transcode/ffmpeg  
	/var/subsonic/transcode/lame  
	

The files under the '/var/subsonic/transcode' folder are the custom binaries. You can change which binaries it uses if it's necessary.

For some reason with my setup, subsonic would fail to start with the following message:

	  
	java not found  
	

I had to update my java config to fix that, here is the command I ran:

	  
	moxz:~> update-alternatives --set java /usr/lib/jvm/jre-1.7.0-openjdk/bin/java  
	

### 3. Customize the SubSonic settings

I didn't have many things to change, I just changed the user it ran as and bound it to my IP. I edited /etc/sysconfig/subsonic and made the following changes:

	  
	SUBSONIC_ARGS="--host=192.168.1.102 --max-memory=150"  
	SUBSONIC_USER=elatov  
	

### 4. Restart the service and make sure it starts up

After I fixed my java issue and made some changes to the settings, I wanted to make sure everything was okay:

	  
	moxz:~>systemctl restart subsonic.service  
	moxz:~>ps -eaf | grep subsonic | grep -v grep  
	elatov 2153 1 27 15:51 ? 00:00:05 java -Xmx150m -Dsubsonic.home=/var/subsonic -Dsubsonic.host=192.168.1.102 -Dsubsonic.port=4040 -Dsubsonic.httpsPort=0 -Dsubsonic.contextPath=/ -Dsubsonic.defaultMusicFolder=/var/music -Dsubsonic.defaultPodcastFolder=/var/music/Podcast -Dsubsonic.defaultPlaylistFolder=/var/playlists -Djava.awt.headless=true -verbose:gc -jar subsonic-booter-jar-with-dependencies.jar  
	

That looked good.

### 5. Open up the Firewall to Allow Clients to Connect to SubSonic Management Portal

Since there is Web Management portal, we need to open up the port with iptables:

	  
	moxz:~> iptables -I INPUT 5 -m state --state NEW -m tcp -p tcp --dport 4040 -j ACCEPT  
	

Then save the iptables config:

	  
	moxz:~>sudo /usr/libexec/iptables.init save  
	iptables: Saving firewall rules to /etc/sysconfig/iptables:  
	

### 6. Connect to SubSonic with you browser

Fire up a browser of your choice and enter http://IP\_OF\_SUBSONIC:4040, you will see a page similar to this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_login_page.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_login_page.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_login_page.png" alt="subsonic login page Installing Subsonic on Fedora 17" title="subsonic_login_page" width="261" height="168" class="alignnone size-full wp-image-4238" /></a>

You can login with username 'admin' and password 'admin', but it will ask you to change that upon login.

### 7. Add a folder to the SubSonic where you Media is Stored

Go to "Settings" -> "Media Folder" and add a folder then click "Save", it will look something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_media_folders.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_media_folders.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/10/subsonic_media_folders.png" alt="subsonic media folders Installing Subsonic on Fedora 17" title="subsonic_media_folders" width="683" height="426" class="alignnone size-full wp-image-4237" /></a>

After that if you go to your Home screen and you should see your music library there.

### 8. Connect to SubSonic with other applications

The cool thing about SubSonic is the variety of applications that can be used to connect to it. There are even mobile apps available. Check out the full list <a href="http://www.subsonic.org/pages/apps.jsp" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.subsonic.org/pages/apps.jsp']);">here</a>.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 6 Package Management" href="http://virtuallyhyper.com/2013/03/rhcsa-and-rhce-chapter-6-package-management/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/rhcsa-and-rhce-chapter-6-package-management/']);" rel="bookmark">RHCSA and RHCE Chapter 6 Package Management</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Fixing Android Phone Device Permissions on Fedora 17" href="http://virtuallyhyper.com/2013/02/fixing-android-phone-device-permissions-on-fedora-17/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/fixing-android-phone-device-permissions-on-fedora-17/']);" rel="bookmark">Fixing Android Phone Device Permissions on Fedora 17</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing MusicCabinet on Top of SubSonic" href="http://virtuallyhyper.com/2013/02/installing-musiccabinet-on-top-of-subsonic/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/installing-musiccabinet-on-top-of-subsonic/']);" rel="bookmark">Installing MusicCabinet on Top of SubSonic</a>
    </li>
  </ul>
</div>

