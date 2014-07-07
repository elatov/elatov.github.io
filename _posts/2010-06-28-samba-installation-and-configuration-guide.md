---
published: true
title: Samba Installation and Configuration Guide
author: Karim Elatov
layout: post
categories: [os]
tags: [linux, samba]
---
Samba is an Open Source/Free Software suite that provides seamless file and print services to SMB/CIFS clients. In laymen speak, it allows windows machines to connect to a Linux samba share. I will break this guide down into 3 parts: Compile/Install, Setup, and Actually Running the Service.

### Install Instructions

Download the source from the [following](http://www.samba.org/samba/download) URL. You should get a file that looks similar to this: **samba-3.4.0.tar.gz**.

	mv samba-3.4.0.tar.gz /tmp; cd /tmp  
	tar xzf samba-3.4.0.tar.gz; cd samba-3.4.0/source3  

Setup up appropriate environment variables:

- For solaris use /usr/sfw/bin/gcc

		set path = ( /usr/sfw/bin $path )  
		setenv CC "gcc -Wl,-rpath,/usr/local/samba/lib"  

- For Linux

		setenv LD_RUN_PATH /usr/local/samba/lib  
  
Now for the configure

	./configure --localstatedir=/var/adm/log/samba --prefix=/usr/local/samba --with-configdir=/usr/local/adm/config/samba --with privatedir=/usr/local/adm/config/samba/private --with-sendfile-support=no  
	make  
	mkdir /var/adm/log/samba  
	mkdir /usr/local/adm/config/samba  
	make install  

### Post Install

Strip all the binaries to save space:

	find /usr/local/samba/bin/ -type f -perm -100 -exec strip {} ;  
	find /usr/local/samba/sbin/ -type f -perm -100 -exec strip {} ;  

Create the man pages  

- Solaris  
	
		catman -w -M /usr/local/samba/share/man  

- Linux
  
		sudo makewhatis -u -w /usr/local/samba/share/man/  
		cp /var/cache/man/whatis /usr/local/samba/share/man  

Clean up and Create the appropriate links:

	rm -rf /usr/local/samba/swat  
	rm -rf /usr/local/samba/private  
	rm /usr/local/samba/lib/*.msg  
	rm /usr/local/samba/sbin/swat  
	ln -s /usr/local/adm/config/samba/smb.conf /usr/local/samba/lib/smb.conf  
	ln -s /usr/local/adm/config/samba/smbusers /usr/local/samba/lib/smbusers  
	ln -s /var/adm/log/samba /usr/local/samba/var  
	ln -s /usr/local/adm/config/samba/private /usr/local/samba/private  
	chmod a-x /usr/local/samba/include/*  
	chown -R -h 0:0 /usr/local/samba  
	chmod -R go-w /usr/local/samba  


### Start-up Scripts

Now that we have samba compiled and installed we need to make up a startup script. Under **/usr/local/samba/sbin**, we will now have some daemons. Among them, we will have **nmbd** and **smbd**. **nmbd** is a server that understands and can reply to NetBIOS over IP name service requests, like those produced by Windows clients. When windows start up, they may wish to locate an SMB/CIFS server. That is, they wish to know what IP number a specified host is using. **Nmbd** will listen for such requests, and if its own NetBIOS name is specified it will respond with the IP number of the host it is running on. **smbd** is the server daemon that provides filesharing and printing services to Windows clients. (Most of this information can be found in the man pages for **nmdb** and **smbd**). Now then, when you have a samba server it is usually a good idea to start both services: **nmdb** and **smbd**. Here are examples of start-up scripts from a fedora install with my custom changes encorporated :).

**SMBD**  

	#!/bin/sh  
	#  
	# chkconfig: - 91 35  
	# description: Starts and stops the Samba smbd daemon  
	# used to provide SMB network services.  
	#  
	# pidfile: /var/run/samba/smbd.pid  
	# config: /usr/local/samba/lib/smb.conf

	SMBCONFIG="/usr/local/samba/lib/smb.conf"  
	SMBDOPTIONS="-D -s/usr/local/samba/lib/smb.conf"

	# Source function library.  
	if [ -f /etc/init.d/functions ] ; then  
	. /etc/init.d/functions  
	elif [ -f /etc/rc.d/init.d/functions ] ; then  
	. /etc/rc.d/init.d/functions  
	else  
	exit 1  
	fi

	# Avoid using root's TMPDIR  
	unset TMPDIR

	# Source networking configuration.  
	. /etc/sysconfig/network

	# Check that networking is up.  
	[ ${NETWORKING} = "no" ] && exit 1

	# Check that smb.conf exists.  
	[ -f $SMBCONFIG ] || exit 6

	RETVAL=0

	start() {  
	KIND="SMB"  
	echo -n $"Starting $KIND services: "  
	daemon smbd $SMBDOPTIONS  
	RETVAL=$?  
	echo  
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/smb ||  
	RETVAL=1  
	return $RETVAL  
	} 

	stop() {  
	KIND="SMB"  
	echo -n $"Shutting down $KIND services: "  
	killproc smbd  
	RETVAL=$?  
	echo  
	[ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/smb  
	return $RETVAL  
	} 

	restart() {  
	stop  
	start  
	} 

	# Check that we can write to it... so non-root users stop here  
	[ -w $SMBCONFIG ] || exit 4

	case "$1" in  
	start)  
	start  
	;;  
	stop)  
	stop  
	;;  
	restart)  
	restart  
	;;  
	*)  
	echo $"Usage: $0 {start|stop|restart}"  
	exit 2  
	esac

	exit $?  

**NMDB**  

	#!/bin/sh  
	#  
	# chkconfig: - 91 35  
	# description: Starts and stops the Samba nmbd daemons  
	# used to provide SMB network services.  
	#  
	# pidfile: /var/run/samba/nmbd.pid  
	# config: SMBCONFIG

	SMBCONFIG="/usr/local/samba/lib/smb.conf"  
	NMBDOPTIONS="-D -l/var/log/samba -s/usr/local/samba/lib/smb.conf"

	# Source function library.  
	if [ -f /etc/init.d/functions ] ; then  
	. /etc/init.d/functions  
	elif [ -f /etc/rc.d/init.d/functions ] ; then  
	. /etc/rc.d/init.d/functions  
	else  
	exit 1  
	fi

	# Avoid using root's TMPDIR  
	unset TMPDIR

	# Source networking configuration.  
	. /etc/sysconfig/network

	# Check that networking is up.  
	[ ${NETWORKING} = "no" ] && exit 1

	# Check that smb.conf exists.  
	[ -f SMBCONFIG ] || exit 6

	RETVAL=0

	start() {  
	KIND="NMB"  
	echo -n $"Starting $KIND services: "  
	daemon nmbd $NMBDOPTIONS  
	RETVAL=$?  
	echo  
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/nmb ||  
	RETVAL=1  
	return $RETVAL  
	} 

	stop() {  
	KIND="NMB"  
	echo -n $"Shutting down $KIND services: "  
	killproc nmbd  
	RETVAL=$?  
	echo  
	[ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/nmb  
	return $RETVAL  
	} 

	restart() {  
	stop  
	start  
	} 

	# Check that we can write to it... so non-root users stop here  
	[ -w SMBCONFIG ] || exit 4

	case "$1" in  
	start)  
	start  
	;;  
	stop)  
	stop  
	;;  
	restart)  
	restart  
	;;  
	*)  
	echo $"Usage: $0 {start|stop|restart}"  
	exit 2  
	esac

	exit $?  

Setup the startup scripts.  

	cp smb /etc/init.d/smb  
	cp nmb /etc/init.d/nmb  
	chkconfig --add smb  
	chkconfig --add nmb  

### Creating the smb.conf file

Samba is a very power service, it can be used as a regular sharing service, it can be setup as a primary domain controller, and much more. It can also use a variety of authentication methods such as **tdbsam** (samba's own database), **smbpasswd** (just a text file with password hashes) , or even against an active directory. I will provide 3 examples: 

1. **smb.conf** as a standard sharing service sharing everyone's home directory
2. **smb.conf** as a primary domain controller
3. **smb.conf** authenticating against an AD server

#### Example as a standard sharing service 

	[global]

	workgroup = MYSMBWG  
	server string = Samba Server Version %v

	# logs split per machine  
	log file = /var/log/samba/log.%m

	# max 50KB per log file, then rotate  
	max log size = 50

	# Verbosity level of logging goes from 0-10  
	# the value below is usually used for debugging  
	log level = 10

	# authentication method  
	security = user  
	passdb backend = tdbsam  
	#============ Share Definitions ===============  
	[homes]  
	comment = Home Directories  
	browseable = no  
	writable = yes  

#### Example as a Primary Domain Controller 

	[global]  
	workgroup = MYSMBWG  
	netbios name = MYMACHINE  
	server string = %h server (Samba)

	# Primary Controller Settings  
	domain logons = yes  
	preferred master = yes  
	wins support = yes

	#Authentication method  
	security = user  
	passdb backend = smbpasswd  
	smb passwd file = /usr/local/samba/private/smbpasswd

	# Default logon: for roaming profiles, this must be here  
	logon drive = H:  
	logon path = %Nprofile%U

	# Useradd scripts: this is custom, so when a new machine  
	# joins this domain, a machine account is created.  
	add machine script = /usr/sbin/useradd -d /dev/null -g 902 -s /bin/false -M -r %u

	# set the loglevel  
	log level = 3

	#============ Share Definitions ===============  
	[homes]  
	comment = Home  
	valid users = %S  
	read only = no  
	browsable = no

	[netlogon]  
	comment = Network Logon Service  
	path = /home/samba/netlogon  
	admin users = Administrator  
	valid users = %U  
	read only = no

	[profile]  
	comment = User profiles  
	path = /home/samba/profiles  
	valid users = %U  
	create mode = 0600  
	directory mode = 0700  
	writable = yes  
	browsable = no  

#### Example with AD authentication 

To use this setup there are many prerequisites. One of the them is that another samba daemon (**winbindd**) must be running. I will write another guide on how to set this up in the future.

	[global]  
	workgroup = AD  
	realm = YOUR.AD.SERVER (DOMAIN.INTERNAL)  
	security = ads  
	password server = your.ads.server1 your.ads.server2 (domainserver.domain.internal)  
	encrypt passwords = yes

	domain logons = no  
	domain master = no

	winbind separator = +  
	# Disable idmapping of Windows SIDs to Unix UIDs  
	idmap config AD:readonly = yes

	log level = 2  
	max log size = 20  
	log file = /var/log/samba/log.%m

	#============ Share Definitions ===============  
	[homes]  
	comment = Home directorys from bechtel  
	guest ok = no  
	read only = no  
	force user = %S

	[example-share-with-ad-users]  
	comment = Temp Share  
	path = /tmp  
	valid users = AD+<ad_user1>,AD+<ad_user2>  
	write list = AD+<ad_user1>,AD+<ad_user2>  
	read list = AD+<ad_user1>,AD+<ad_user2>  
	#ie write list = AD+elatov

	[example-share-with-ad-groups]  
	comment = Temp Share  
	path = /data/tmp  
	writeable=yes  
	browseable=yes  
	valid users = @AD+"<ad_group1>" @AD+"<ad_group2>"  
	#ie valid users = @AD+"Finance Department Users"  

### Starting the samba service 

Once you have the start-up scripts in place and your **smb.conf** all setup it is now time to start the samba services.

Check to make sure not errors exist in the **smb.conf**  

	/usr/local/samba/bin/testparm  

**Note:** If you see any errors, fix them

Start the services  

	service smb start  
	service nmb start  


Check to make sure they are running  

	ps -eaf | grep smbd  
	ps -eaf | grep nmbd  


If the services are not running or the service fails to start, check under **/var/log/samba** for the reasons why it's not running. Also setting the **log level** variable to **10** will help in debugging startup error.
