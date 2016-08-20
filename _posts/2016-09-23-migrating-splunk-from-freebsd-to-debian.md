---
published: false
layout: post
title: "Migrating Splunk From FreeBSD to Debian"
author: Karim Elatov
categories: [security,os]
tags: [splunk,freebsd,debian]
---
It was recently announced that splunk for FreeBSD would only support the *splunk-forwarder* configuration. From [Install the universal forwarder on FreeBSD](http://docs.splunk.com/Documentation/Splunk/latest/Installation/InstallonFreeBSD):

> Important: Splunk does not offer an installation package for Splunk Enterprise on FreeBSD. It does, however, offer a universal forwarder installation package for FreeBSD versions 9 and 10. These instructions detail how to install the universal forwarder on those versions of FreeBSD.
> 
> To use Splunk Enterprise on FreeBSD, you must download an older version of the Splunk software.

Looking over the [Older Splunk Releases](http://www.splunk.com/page/previous_releases#x86_64freebsd) page it looks like the latest supported version for FreeBSD is **6.2.7**. The latest version of Splunk was **6.4** and I wanted to migrate my install to a supported OS (like Debian) and update it.

### Migrate Install From FreeBSD to Debian
Looking over [Migrating a Splunk installation](https://wiki.splunk.com/Deploy:Migrating_a_Splunk_Install) it looks like the steps are actually pretty easy:

> Migrating a splunk install to a new operating system builds on this, with some caveats. The general idea is as follows.
> 
> 1. Shut down your old Splunk install: `splunk stop`
> 2. Copy (via whatever means, scp, rsync, tar, zip) the Splunk install directory to the desired install location on the new computer.
> 3. Unpack or install the Splunk tar or package for new system on top of the copied files.
> 4. Start it up. `splunk start`
> 
> You can even "upgrade" to the same version you were already using with this method, just to validate that the operating system transition was effective.

So on the FreeBSD machine let's create a backup of the install:

	sudo service splunk stop
	cd /opt
	sudo tar cpjf splunk-freebsd.tar.bz2 splunk

Now let's **rsync** that to the Debian Machine:

	┌─[elatov@moxz] - [/opt] - [2016-04-23 09:51:48]
	└─[0] <> rsync -avzP splunk-freebsd.tar.bz2 kerch:

On the Debian Side let's extract the FreeBSD install under the **/opt** directory:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:53:32]
	└─[0] <> sudo tar xpjf splunk-freebsd.tar.bz2 -C /opt

Then on top of that let's extract the new one:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:58:23]
	└─[130] <> sudo tar xzf splunk-6.4.0-f2c836328108-Linux-x86_64.tgz -C /opt

Then fix the ownership:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:59:47]
	└─[0] <> sudo chown splunk:splunk -R /opt/splunk

### Upgrade and Convert Splunk install to Linux
Now let's just start the splunk service:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 10:00:01]
	└─[0] <> sudo /opt/splunk/bin/splunk start
	                    SOFTWARE LICENSE AGREEMENT
	
	THIS SOFTWARE LICENSE AGREEMENT (“AGREEMENT”) GOVERNS THE LICENSING,
	INSTALLATION AND USE OF SPLUNK SOFTWARE. BY DOWNLOADING AND/OR INSTALLING SPLUNK
	SOFTWARE (A) YOU ARE INDICATING THAT YOU HAVE READ AND UNDERSTAND THIS
	AGREEMENT, AND AGREE TO BE LEGALLY BOUND BY IT ON BEHALF OF THE COMPANY,
	GOVERNMENT, OR OTHER ENTITY FOR WHICH YOU ARE ACTING (FOR EXAMPLE, AS AN
	EMPLOYEE OR GOVERNMENT OFFICIAL) OR, IF THERE IS NO COMPANY, GOVERNMENT OR OTHER
	ENTITY FOR WHICH YOU ARE ACTING, ON BEHALF OF YOURSELF AS AN INDIVIDUAL; AND (B)
	YOU REPRESENT AND WARRANT THAT YOU HAVE THE AUTHORITY TO ACT ON BEHALF OF AND
	BIND SUCH COMPANY, GOVERNMENT OR OTHER ENTITY (IF ANY).
	
	WITHOUT LIMITING THE FOREGOING, YOU (AND YOUR ENTITY, IF ANY) ACKNOWLEDGE THAT
	BY SUBMITTING AN ORDER FOR THE SPLUNK SOFTWARE, YOU (AND YOUR ENTITY (IF ANY))
	HAVE AGREED TO BE BOUND BY THIS AGREEMENT.
	
	As used in this Agreement, “Splunk,” refers to Splunk Inc., a Delaware
	corporation, with its principal place of business at 250 Brannan Street, San
	Francisco, California 94107, U.S.A.; and “Customer” refers to the company,
	government, or other entity on whose behalf you have entered into this Agreement
	or, if there is no such entity, you as an individual.
	
	1.     DEFINITIONS. Capitalized terms used but not otherwise defined in this
	Agreement have the meanings set forth in Exhibit A.
	Do you agree with this license? [y/n]: Y
	
	This appears to be an upgrade of Splunk.
	--------------------------------------------------------------------------------)
	
	Splunk has detected an older version of Splunk installed on this machine. To
	finish upgrading to the new version, Splunk's installer will automatically
	update and alter your current configuration files. Deprecated configuration
	files will be renamed with a .deprecated extension.
	
	You can choose to preview the changes that will be made to your configuration
	files before proceeding with the migration and upgrade:
	
	If you want to migrate and upgrade without previewing the changes that will be
	made to your existing configuration files, choose 'y'.
	If you want to see what changes will be made before you proceed with the
	upgrade, choose 'n'.
	
	
	Perform migration and upgrade without previewing configuration changes? [y/n] Y
	
	-- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2016-04-23.10-00-47' --
	
	Migrating to:
	VERSION=6.4.0
	BUILD=f2c836328108
	PRODUCT=splunk
	PLATFORM=Linux-x86_64
	
	Copying '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.
	
	Checking saved search compatibility...
	
	Handling deprecated files...
	
	Checking script configuration...
	
	Copying '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
	Deleting '/opt/splunk/etc/system/local/field_actions.conf'.
	Moving '/opt/splunk/share/splunk/search_mrsparkle/modules' to '/opt/splunk/share/splunk/search_mrsparkle/modules.old.20160423-100048'.
	Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
	The following apps might contain lookup table files that are not exported to other apps:
	
		TA-Suricata
	
	Such lookup table files could only be used within their source app.  To export them globally and allow other apps to access them, add the following stanza to each /opt/splunk/etc/apps/<app_name>/metadata/local.meta file:
	
		[lookups]
		export = system
	
	For more information, see http://docs.splunk.com/Documentation/Splunk/latest/AdvancedDev/SetPermissions#Make_objects_globally_available.
	Checking for possible UI view conflicts...
	 App "splunk_management_console" has an overriding copy of the "reports.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_management_console/default/data/ui/views
	 App "splunk_management_console" has an overriding copy of the "dashboards.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_management_console/default/data/ui/views
	 App "splunk_management_console" has an overriding copy of the "alerts.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_management_console/default/data/ui/views
	Removing legacy manager XML files...
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/manager/deployment_server.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/manager/deployment_serverclass_status.xml'.
	DMC is not set up, no need to migrate nav bar.
	Removing System Activity dashboards...
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/internal_messages.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/scheduler_savedsearch.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/scheduler_status.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/scheduler_status_errors.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/scheduler_user_app.prod_lite.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/scheduler_user_app.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/search_activity_by_user.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/search_detail_activity.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/search_status.xml'.
	Deleting '/opt/splunk/etc/apps/search/default/data/ui/views/status_index.xml'.
	Distributed Search is not configured on this instance
	
	"/opt/splunk/etc/auth/ca.pem": certificate renewed
	"/opt/splunk/etc/auth/cacert.pem": certificate renewed
	"/opt/splunk/etc/auth/server.pem": certificate renewed
	Clustering migration already complete, no further changes required.
	
	Generating checksums for datamodel and report acceleration bucket summaries for all indexes.
	If you have defined many indexes and summaries, summary checksum generation may take a long time.
	Processed 1 out of 7 configured indexes.
	Processed 2 out of 7 configured indexes.
	Processed 3 out of 7 configured indexes.
	Processed 4 out of 7 configured indexes.
	Processed 5 out of 7 configured indexes.
	Processed 6 out of 7 configured indexes.
	Processed 7 out of 7 configured indexes.
	Finished generating checksums for datamodel and report acceleration bucket summaries for all indexes.
	
	Creating $SPLUNK_HOME/var/run/splunk/csv and moving inputcsv/outputcsv files into the created directory.
	
	Splunk> Be an IT superhero. Go home early.
	
	Checking prerequisites...
		Checking http port [8000]: open
		Checking mgmt port [8089]: open
		Checking appserver port [127.0.0.1:8065]: open
		Checking kvstore port [8191]: open
		Checking configuration...  Done.
		Checking critical directories...	Done
		Checking indexes...
			Validated: _audit _internal _introspection _thefishbucket history main summary
		Done
		Checking filesystem compatibility...  Done
		Checking conf files for problems...
		Done
		Checking default conf files for edits...
		Validating installed files against hashes from '/opt/splunk/splunk-6.4.0-f2c836328108-linux-2.6-x86_64-manifest'
		All installed files intact.
		Done
	All preliminary checks passed.
	
	Starting splunk server daemon (splunkd)...
	Done
	
	
	Waiting for web server at http://127.0.0.1:8000 to be available
	sed: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	grep: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	.sed: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	grep: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	.sed: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	grep: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	.sed: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	grep: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	.sed: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	grep: error while loading shared libraries: /opt/splunk/lib/libpcre.so.3: ELF file OS ABI invalid
	.. Done
	
	
	If you get stuck, we're here to help.
	Look for answers here: http://docs.splunk.com
	
	The Splunk web interface is at http://kerch:8000

The conversion and upgrade were fine but it was complaining about the **libpcre.so** file, I checked it out and the file was pointing to the correct location it just had a leftover file:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 10:04:47]
	└─[0] <> ls -l /opt/splunk/lib | grep pcre
	lrwxrwxrwx  1 splunk splunk      16 Mar 25 21:40 libpcre.so -> libpcre.so.1.2.6
	lrwxrwxrwx  1 splunk splunk      16 Mar 25 21:40 libpcre.so.1 -> libpcre.so.1.2.6
	-r-xr-xr-x  1 splunk splunk  280640 Mar 25 21:45 libpcre.so.1.2.6
	-r-xr-xr-x  1 splunk splunk  264272 Nov 17 18:29 libpcre.so.3

checking over the file it was the old FreeBSD file:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 10:05:30]
	└─[0] <> file /opt/splunk/lib/libpcre.so.3
	/opt/splunk/lib/libpcre.so.3: ELF 64-bit LSB shared object, x86-64, version 1 	(FreeBSD), dynamically linked, stripped

So I just moved the file out of the way:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 10:05:47]
	└─[0] <> sudo mv /opt/splunk/lib/libpcre.so.3 /tmp/

At this point I decided to use **systemd** to restart and make sure everything was okay:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:38:36]
	└─[0] <> sudo /opt/splunk/bin/splunk enable boot-start
	Init script installed at /etc/init.d/splunk.
	Init script is configured to run at boot.

Let's enable the service:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:43:16]
	└─[1] <> sudo systemctl enable splunk
	Synchronizing state for splunk.service with sysvinit using update-rc.d...
	Executing /usr/sbin/update-rc.d splunk defaults
	Executing /usr/sbin/update-rc.d splunk enable

Then I just restarted the service:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:43:26]
	└─[0] <> sudo systemctl restart splunk
	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:43:44]
	└─[0] <> sudo systemctl status splunk
	● splunk.service - LSB: Start splunk
	   Loaded: loaded (/etc/init.d/splunk)
	   Active: active (running) since Sat 2016-04-23 09:43:44 MDT; 38s ago
	  Process: 8871 ExecStart=/etc/init.d/splunk start (code=exited, status=0/SUCCESS)
	   CGroup: /system.slice/splunk.service
	           ├─8925 splunkd -p 8089 start
	           ├─8926 [splunkd pid=8925] splunkd -p 8089 start [process-runner]
	           ├─8936 mongod --dbpath=/opt/splunk/var/lib/splunk/kvstore/mongo --...
	           ├─8995 /opt/splunk/bin/python -O /opt/splunk/lib/python2.7/site-pa...
	           ├─9010 /opt/splunk/bin/splunkd instrument-resource-usage -p 8089 -...
	           ├─9091 splunkd fsck --log-to--splunkd-log repair --try-warm-then-c...
	           └─9092 splunkd fsck --log-to--splunkd-log repair --try-warm-then-c...
	
	Apr 23 09:43:41 kerch splunk[8871]: Checking conf files for problems... Done
	Apr 23 09:43:41 kerch splunk[8871]: Checking default conf files for edits...
	Apr 23 09:43:42 kerch splunk[8871]: Validating installed files against hashes fr
	Apr 23 09:43:42 kerch splunk[8871]: All installed files intact. Done
	Apr 23 09:43:44 kerch splunk[8871]: All preliminary checks passed.
	Apr 23 09:43:44 kerch splunk[8871]: Starting splunk server daemon (splunkd)...
	Apr 23 09:43:44 kerch splunk[8871]: .. Done
	Apr 23 09:43:44 kerch splunk[8871]: If you get stuck, we're here to help.
	Apr 23 09:43:44 kerch splunk[8871]: Look for answers here: http://docs.splu...om
	Apr 23 09:43:44 kerch splunk[8871]: The Splunk web interface is at http://k...00
	Hint: Some lines were ellipsized, use -l to show in full.

The **libprce.so** messages were gone and it looks like there was a **fsck** kicked off:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 09:43:55]
	└─[0] <> ps -ef | grep splunk
	root      8925     1  9 09:43 ?        00:00:01 splunkd -p 8089 start
	root      8926  8925  0 09:43 ?        00:00:00 [splunkd pid=8925] splunkd -p 8089 start [process-runner]
	root      8936  8926  2 09:43 ?        00:00:00 mongod --dbpath=/opt/splunk/var/lib/splunk/kvstore/mongo --port=8191 --timeStampFormat=iso8601-utc --smallfiles --oplogSize=200 --keyFile=/opt/splunk/var/lib/splunk/kvstore/mongo/splunk.key --setParameter=enableLocalhostAuthBypass=0 --replSet=6482AC22-1D3F-4B24-B7CB-9E0A56E26F2B --sslAllowInvalidHostnames --sslMode=preferSSL --sslPEMKeyFile=/opt/splunk/etc/auth/server.pem --sslPEMKeyPassword=xxxxxxxx --nounixsocket
	root      8995  8926  9 09:43 ?        00:00:01 /opt/splunk/bin/python -O /opt/splunk/lib/python2.7/site-packages/splunk/appserver/mrsparkle/root.py --proxied=127.0.0.1,8065,8000
	root      9010  8926  0 09:43 ?        00:00:00 /opt/splunk/bin/splunkd instrument-resource-usage -p 8089 --with-kvstore
	root      9091  8926 92 09:43 ?        00:00:12 splunkd fsck --log-to--splunkd-log repair --try-warm-then-cold --one-bucket --index-name=main --bucket-name=db_1458739617_1458272425_151 --ignore-read-error
	root      9092  9091  0 09:43 ?        00:00:00 splunkd fsck --log-to--splunkd-log repair --try-warm-then-cold --one-bucket --index-name=main --bucket-name=db_1458739617_1458272425_151 --ignore-read-error
	elatov    9200  7719  0 09:43 pts/2    00:00:00 grep --color=auto splunk

Then going to the splunk admin console (**http://SPLUNK_IP:8000**) showed all the old data.

### Post Install Fixes

Ended up adding a new input for *ossec*, since the *ossec* server was running on a remote machine now:

	┌─[elatov@kerch] - [/home/elatov] - [2016-04-23 12:57:02]
	└─[0] <> sudo cat /opt/splunk/etc/system/local/inputs.conf
	[default]
	host = kerch.kar.int
	
	[udp://10.0.0.3:5002]
	disabled = false
	sourcetype = ossec
	connection_host = none
	host = moxz.kar.int
	
I also updated my hostname under **Settings** -> **Server Settings** -> **General Settings**:

![update-hostname-splunk](https://dl.dropboxusercontent.com/u/24136116/blog_pics/splunk-mig-to-deb/update-hostname-splunk.png)
