---
title: Installing MusicCabinet on Top of SubSonic
author: Karim Elatov
layout: post
permalink: /2013/02/installing-musiccabinet-on-top-of-subsonic/
dsq_thread_id:
  - 1406034084
categories:
  - Home Lab
  - OS
tags:
  - /usr/share/subsonic
  - /var/lib/pgsql/data/pg_hba.conf
  - /var/subsonic
  - getent
  - lastfm
  - MusicCabinet
  - PostgreSQL
  - postgresql-setup initdb
  - psql
  - rpm -ql
  - scrobbling
  - subsonic
  - systemctl
  - tar cpvjf
  - unzip
  - wget
  - \password postgres
---
A while back I <a href="http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/']);">posted</a> about installing *subsonic*. While I was using the application, I noticed that the search feature is very limited and I wanted to expand it. So I ran across <a href="http://dilerium.se/musiccabinet/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://dilerium.se/musiccabinet/']);">MusicCabinet</a>, from their webpage:

> Subsonic is a streaming music server, providing instant access to your personal music library. It is written by Sindre Mehus and released under the GPL.
> 
> MusicCabinet is an add-on for Subsonic. It uses the free musical knowledge gathered at Last.fm, to seamlessly: 

It's an add-on for *subsonic* and among other features it expands the searching functionality. 

I couldn't find any good instructions on how to install the add-on. The only link I found was <a href="http://forum.subsonic.org/forum/viewtopic.php?f=8&#038;t=10220" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.subsonic.org/forum/viewtopic.php?f=8&t=10220']);">this</a> forum. The instructions were for an Ubuntu install and I was running Fedora. So I decided to write up instructions on how to install the plugin in Fedora on top of the *subsonic* RPM. Checking out the RPM, here are the files the original *subsonic* package contained:

	  
	$ rpm -ql subsonic-4.7-3105.i386  
	/etc/init.d/subsonic  
	/etc/sysconfig/subsonic  
	/usr/share/subsonic/subsonic-booter-jar-with-dependencies.jar  
	/usr/share/subsonic/subsonic.sh  
	/usr/share/subsonic/subsonic.war  
	/var/subsonic/transcode/ffmpeg  
	/var/subsonic/transcode/lame  
	

Not that much stuff. The database for subsonic is under **/var/subsonic**:

	  
	$ ls /var/subsonic/  
	db jetty subsonic.log subsonic_sh.log transcode  
	db.backup lucene2 subsonic.properties thumbs  
	

You have also need to java version 7 installed. I already had that installed:

	  
	$ java -version  
	java version "1.7.0_09-icedtea"  
	OpenJDK Runtime Environment (fedora-2.3.4.fc17-i386)  
	OpenJDK Client VM (build 23.2-b09, mixed mode)  
	

I covered the install of java in the initial post <a href="http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/']);">here</a>, check it out if necessary. Now let's get started on the *MusicCabinet* install. 

### 1. Install and Setup PostgreSQL

Here is how the install looks like with *YUM*:

	  
	$ sudo yum install postgresql postgresql-server  
	Resolving Dependencies  
	--> Running transaction check  
	---> Package postgresql.i686 0:9.1.7-1.fc17 will be installed  
	...  
	...  
	Installed:  
	postgresql.i686 0:9.1.7-1.fc17 postgresql-server-9.1.7-1.fc17.i686.rpm 
	
	Dependency Installed:  
	postgresql-libs.i686 0:9.1.7-1.fc17 
	
	Complete!  
	

That went well, now let's initialize the database:

	  
	$ sudo postgresql-setup initdb  
	Initializing database ... OK  
	

Next let's enable the **postgresql** service and start it:

	  
	$ sudo systemctl enable postgresql.service  
	ln -s '/usr/lib/systemd/system/postgresql.service' '/etc/systemd/system/multi-user.target.wants/postgresql.service'  
	$ sudo systemctl start postgresql.service  
	

Confirming that the service is running:

	  
	$ sudo systemctl status postgresql.service  
	postgresql.service - PostgreSQL database server  
	Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled)  
	Active: active (running) since Wed, 30 Jan 2013 17:13:05 -0800; 49s ago  
	Process: 32310 ExecStart=/usr/bin/pg_ctl start -D ${PGDATA} -s -o -p ${PGPORT} -w -t 300 (code=exited, status=0/SUCCESS)  
	Process: 32305 ExecStartPre=/usr/bin/postgresql-check-db-dir ${PGDATA} (code=exited, status=0/SUCCESS)  
	Main PID: 32315 (postgres)  
	CGroup: name=systemd:/system/postgresql.service  
	├ 32315 /usr/bin/postgres -D /var/lib/pgsql/data -p 5432  
	├ 32316 postgres: logger process  
	├ 32318 postgres: writer process  
	├ 32319 postgres: wal writer process  
	├ 32320 postgres: autovacuum launcher process  
	└ 32321 postgres: stats collector process  
	

That all looks good. It looks like the install also creates a **postgres** user:

	  
	$ getent passwd postgres  
	postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash  
	

Then using the **postgres** user, reset the password for itself:

	  
	$ sudo -u postgres psql postgres  
	psql (9.1.7)  
	Type "help" for help.
	
	postgres=# \password postgres  
	Enter new password:  
	Enter it again:  
	postgres-# \q  
	

Lastly, allow logins with local password authentication to the *psql* instance. Edit the following file: **/var/lib/pgsql/data/pg_hba.conf** and change these lines:

	  
	# "local" is for Unix domain socket connections only  
	local all all peer  
	# IPv4 local connections:  
	host all all 127.0.0.1/32 ident  
	

to look like this:

	  
	# "local" is for Unix domain socket connections only  
	local all all md5  
	# IPv4 local connections:  
	host all all 127.0.0.1/32 md5  
	

After the change, restart the *postgresql* service:

	  
	$ sudo systemctl restart postgresql.service  
	

Then you should be able to login with the password you set from any user:

	  
	$ psql -U postgres  
	Password for user postgres:  
	psql (9.1.7)  
	Type "help" for help.
	
	postgres=# \q  
	

Even when you try to connect to the localhost IP:

	  
	$ psql -U postgres -h localhost  
	Password for user postgres:  
	psql (9.1.7)  
	Type "help" for help.
	
	postgres=# \q  
	

That will be it for the **postgresql** setup.

### 2. Backup the Subsonic Database and Install Files

The files are stored under **/var/subsonic**, so let's tar that up. First let's stop the subsonic service:

	  
	$ sudo systemctl stop subsonic.service  
	

Now let's check the status:

	  
	$ sudo systemctl status subsonic.service  
	subsonic.service - LSB: Subsonic daemon  
	Loaded: loaded (/etc/rc.d/init.d/subsonic)  
	Active: inactive (dead) since Wed, 30 Jan 2013 17:28:15 -0800; 5s ago  
	Process: 32425 ExecStop=/etc/rc.d/init.d/subsonic stop (code=exited, status=0/SUCCESS)  
	CGroup: name=systemd:/system/subsonic.service
	
	Jan 23 21:06:47 moxz.dnsd.me subsonic[707]: Starting subsonic ...  
	Jan 23 21:06:48 moxz.dnsd.me subsonic[707]: Started Subsonic [PID 795, /var...]  
	Jan 30 17:28:15 moxz.dnsd.me subsonic[32425]: Stopping subsonic ...[ OK ]  
	

That looks good. Now let's back up the data:

	  
	$ sudo tar cpvjf subsonic_backup.tar.bz2 /var/subsonic/  
	/var/subsonic/thumbs/200/315cff71c50a61d933b3d30c392b0343.jpeg  
	...  
	...  
	

Since the application files go under **/usr/share/subsonic**, let's backup those up as well:

	  
	$ sudo tar cpvjf subsonic_usr_backup.tar.bz2 /usr/share/subsonic  
	/usr/share/subsonic/  
	/usr/share/subsonic/subsonic.sh  
	/usr/share/subsonic/subsonic-booter-jar-with-dependencies.jar  
	/usr/share/subsonic/subsonic.war  
	

Here are the two resulting files:

	  
	$ ls -lh subsonic*  
	-rw-r--r-- 1 root root 61M Jan 30 17:33 subsonic_backup.tar.bz2  
	-rw-r--r-- 1 root root 29M Jan 30 17:35 subsonic_usr_backup.tar.bz2  
	

That looks good.

### 3. Download and Extract MusicCabinet

This is pretty easy, let's create a temporary directory and download the install file there:

	  
	$ mkdir files  
	$ cd files/  
	$ wget http://dilerium.se/musiccabinet/subsonic-installer-standalone.zip  
	--2013-01-30 17:39:24-- http://dilerium.se/musiccabinet/subsonic-installer-standalone.zip  
	Resolving dilerium.se (dilerium.se)... 193.202.110.54  
	Connecting to dilerium.se (dilerium.se)|193.202.110.54|:80... connected.  
	HTTP request sent, awaiting response... 200 OK  
	Length: 29481485 (28M)   
	Saving to: \`subsonic-installer-standalone.zip'
	
	100%[=====================================>] 29,481,485 482K/s in 76s 
	
	2013-01-30 17:40:41 (380 KB/s) - \`subsonic-installer-standalone.zip' saved [29481485/29481485]  
	

Now let's extract the contents:

	  
	$ unzip subsonic-installer-standalone.zip  
	Archive: subsonic-installer-standalone.zip  
	creating: subsonic-installer-standalone/  
	inflating: subsonic-installer-standalone/subsonic-main.war  
	inflating: subsonic-installer-standalone/subsonic-booter.jar  
	inflating: subsonic-installer-standalone/Getting Started.html  
	inflating: subsonic-installer-standalone/LICENSE.TXT  
	inflating: subsonic-installer-standalone/README.TXT  
	inflating: subsonic-installer-standalone/subsonic.bat  
	inflating: subsonic-installer-standalone/subsonic.sh  
	

Now to the final steps:

### 4. Copy the Installation Files to the SubSonic Install

We just need to copy over two files. Here are the permissions before copying the files over:

	  
	$ ls -l /usr/share/subsonic/  
	total 30724  
	-rw-r--r-- 1 root root 10801885 Sep 11 13:06 subsonic-booter-jar-with-dependencies.jar  
	-rwxr-xr-x 1 root root 5030 Sep 11 13:06 subsonic.sh  
	-rw-r--r-- 1 root root 20603945 Sep 11 13:06 subsonic.war  
	

Now to copy over the file:

	  
	$ cd subsonic-installer-standalone  
	$ sudo cp subsonic-main.war /usr/share/subsonic/subsonic.war  
	$ sudo cp subsonic-booter.jar /usr/share/subsonic/subsonic-booter-jar-with-dependencies.jar  
	

Here is how the files look after the copy:

	  
	$ ls -l /usr/share/subsonic/  
	total 30016  
	-rw-r--r-- 1 root root 7550525 Jan 30 17:52 subsonic-booter-jar-with-dependencies.jar  
	-rwxr-xr-x 1 root root 5030 Sep 11 13:06 subsonic.sh  
	-rw-r--r-- 1 root root 23130290 Jan 30 17:48 subsonic.war  
	

The permissions looks good. Now let's start the subsonic service:

	  
	$ sudo systemctl start subsonic.service  
	

Now let's make sure it stated up fine:

	  
	$ sudo systemctl status subsonic.service  
	subsonic.service - LSB: Subsonic daemon  
	Loaded: loaded (/etc/rc.d/init.d/subsonic)  
	Active: active (exited) since Wed, 30 Jan 2013 17:53:46 -0800; 5s ago  
	Process: 32425 ExecStop=/etc/rc.d/init.d/subsonic stop (code=exited, status=0/SUCCESS)  
	Process: 32606 ExecStart=/etc/rc.d/init.d/subsonic start (code=exited, status=0/SUCCESS)  
	CGroup: name=systemd:/system/subsonic.service
	
	Jan 30 17:53:45 moxz.dnsd.me subsonic[32606]: Starting subsonic ...  
	Jan 30 17:53:46 moxz.dnsd.me subsonic[32606]: Started Subsonic [PID 32632, ...]  
	

That looks good.

### 5. Configure MusicCabinet via the Browser

Visit the *subsonic* web page and the interface will look different:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-subsonic.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-subsonic.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-subsonic.png" alt="music cabinet subsonic Installing MusicCabinet on Top of SubSonic" width="889" height="478" class="alignnone size-full wp-image-6005" title="Installing MusicCabinet on Top of SubSonic" /></a>

Then go to "Settings" -> "MusicCabinet" and specify the postgres user password:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/subsonic-music-cabinet-settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/subsonic-music-cabinet-settings.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/subsonic-music-cabinet-settings.png" alt="subsonic music cabinet settings Installing MusicCabinet on Top of SubSonic" width="648" height="243" class="alignnone size-full wp-image-6006" title="Installing MusicCabinet on Top of SubSonic" /></a>

After you type in the *postgres* password it will ask you to "Upgrade Database":

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabin_upgrade_db.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabin_upgrade_db.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabin_upgrade_db.png" alt="music cabin upgrade db Installing MusicCabinet on Top of SubSonic" width="737" height="213" class="alignnone size-full wp-image-6007" title="Installing MusicCabinet on Top of SubSonic" /></a>

After it's done updating the database, it will ask you to update your search index:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabinet_update_index.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabinet_update_index.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music_cabinet_update_index.png" alt="music cabinet update index Installing MusicCabinet on Top of SubSonic" width="674" height="331" class="alignnone size-full wp-image-6008" title="Installing MusicCabinet on Top of SubSonic" /></a>

While the scan is going you can check the progress of the scan:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-scan-progress.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-scan-progress.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-scan-progress.png" alt="music cabinet scan progress Installing MusicCabinet on Top of SubSonic" width="657" height="476" class="alignnone size-full wp-image-6009" title="Installing MusicCabinet on Top of SubSonic" /></a>

While it's indexing, you can also enable *lastfm* 'scrobbling' by going to "Settings" -> "Personal", if you scroll down a little bit you will an option to "Configure lastfm scrobbling", like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-lastfm-scrobbling.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-lastfm-scrobbling.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-lastfm-scrobbling.png" alt="music cabinet lastfm scrobbling Installing MusicCabinet on Top of SubSonic" width="658" height="411" class="alignnone size-full wp-image-6033" title="Installing MusicCabinet on Top of SubSonic" /></a>

After the indexing is done, the settings page for *MusicCabinet* will look like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-index-done.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-index-done.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/music-cabinet-index-done.png" alt="music cabinet index done Installing MusicCabinet on Top of SubSonic" width="634" height="493" class="alignnone size-full wp-image-6035" title="Installing MusicCabinet on Top of SubSonic" /></a>

Now if you search for something there will be an option to do an "Advanced Search", here is how it looks like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/advanced_search_music_cabinet.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/advanced_search_music_cabinet.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/advanced_search_music_cabinet.png" alt="advanced search music cabinet Installing MusicCabinet on Top of SubSonic" width="614" height="309" class="alignnone size-full wp-image-6049" title="Installing MusicCabinet on Top of SubSonic" /></a>

You now can also view your library by Tags, I still prefer the File-based browsing but this just adds more functionality. Also, every time you play a song it updates your *lastfm* library as well. I am sure there are a lot more updates, but those are the ones that stood out to me.

