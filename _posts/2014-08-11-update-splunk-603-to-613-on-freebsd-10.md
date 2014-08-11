---
published: true
layout: post
title: "Update Splunk 6.0.3 to 6.1.3 On FreeBSD 10"
author: Karim Elatov
categories: [os]
tags: [freebsd,splunk,pkgng]
---

In my previous posts ([Installing Splunk on FreeBSD](/2013/12/installing-splunk-freebsd/) and [Update Splunk 6.0 to 6.0.3 on FreeBSD](/2014/05/update-splunk-6-0-to-6-0-3/)), I used **pkg_install** to install the native splunk package, but it looks like that package has been completely removed (and pretty recently: 5/4/14):

	moxz:/usr/ports>make search name=pkg_install
	Port:	ports-mgmt/pkg_install-devel
	Moved:	ports-mgmt/pkg_install
	Date:	2008-03-31
	Reason:	Port has been unmaintained for a few years
	
	Port:	ports-mgmt/pkg_install
	Moved:
	Date:	2014-05-04
	Reason:	Has expired: Replaced by ports-mgmt/pkg

So this time around I just used the *non-native* splunk package to update splunk. 

### Backup Current Splunk Install
As always before making any changes, let's go ahead and create a backup:

	cd /opt
	sudo tar cpvjf splunk_8_11_2014.tar.bz2 splunk

### PKGNG Vs PKG_Tools
If you try to install the splunk native FreeBSD package with the new **pkg** tool it will fail with the following error:

	moxz:~>sudo pkg add ./splunk-6.1.3-220630-FreeBSD7-amd64.tgz
	pkg: ./splunk-6.1.3-220630-FreeBSD7-amd64.tgz is not a valid package: no manifest found
	
	Failed to install the following 1 package(s): ./splunk-6.1.3-220630-FreeBSD7-amd64.tgz

It's missing the manifests file. From [this](https://wiki.freebsd.org/pkgng) page we can see what is required:

> ## Package format
> 
> A package is a tar archive which can be either uncompressed, or compressed in gzip, bzip2 or xz format. The first elements in a package are the metadata.
> 
> ### Metadata
> 
> ####+MANIFEST
> 
> The manifest is a text file in YAML. It contains all the information concerning a package; it also contains the scripts.
> 
> 
> 	name: foo
> 	version: 1.0
> 	origin: category/foo
> 	comment: this is foo package
> 	arch: i386
> 	www: http://www.foo.org
> 	maintainer: foo@bar.org
> 	prefix: /usr/local
> 	licenselogic: or
> 	licenses: [MIT, MPL]
> 	flatsize: 482120
> 	users: [USER1, USER2]
> 	groups: [GROUP1, GROUP2]
> 	options: { OPT1: off, OPT2: on }
> 	desc: |-
> 	  This is the description
> 	  Of foo
> 	
> 	  A component of bar
> 	categories: [bar, plop]
> 	deps:
> 	  libiconv: {origin: converters/libiconv, version: 1.13.1_2}
> 	  perl: {origin: lang/perl5.12, version: 5.12.4 }
> 	files:
> 	  /usr/local/bin/foo: 'sha256sum'
> 	  /usr/local/bin/i_am_a_link: '-'
> 	  /usr/local/share/foo-1.0/foo.txt: 'sha256sum'
> 	dirs:
> 	- /usr/local/share/foo-1.0
> 	scripts:
> 	  post-install: |-
> 	    #!/bin/sh
> 	    echo post-install
> 	  pre-install: |-
> 	    #!/bin/sh
> 	    echo pre-install

From the same page here is more information about what *scripts* can be included:

> #### Scripts
> 
> Valid scripts are:
> 
> * pre-install
> * post-install
> * install
> * pre-deinstall
> * post-deinstall
> * deinstall
> * pre-upgrade
> * post-upgrade
> * upgrade
> 
> The script MUST be in sh format, otherwise nothing else would work. The shebang is not necessary. pkg-install has/had this rule too, see here and here but did not enforce them as strictly has pkgng does. Also note the args to the scripts are currently:
> 
> * PRE-INSTALL
> * POST-INSTALL
> * DEINSTALL
> * POST-DEINSTALL
> * PRE-UPGRADE
> * POST-UPGRADE
> 
> This inconsistency will be resolved once pkg-install tools are no longer supported.

And here is what happens during an install with **pkgng**:

> #### Installing a package with pkgng
> 
> 1. execute pre_install script if any exists
> 2. execute install script with PRE-INSTALL argument
> 3. extract files directly to the right place
> 4. extract directories directly to the right place
> 5. execute post_install script if any exists
> 6. execute install script with POST-INSTALL arguments

Now looking over the old **pkg_tools**, here is the [install](http://www.freebsd.org/doc/en/books/porters-handbook/pkg-install.html) process:

> If your port needs to execute commands when the binary package is installed with pkg add or pkg install you can do this via the pkg-install script. This script will automatically be added to the package, and will be run twice by pkg the first time as ${SH} pkg-install ${PKGNAME} PRE-INSTALL before the package is installed and the second time as ${SH} pkg-install ${PKGNAME} POST-INSTALL after it has been installed. $2 can be tested to determine which mode the script is being run in. The PKG_PREFIX environmental variable will be set to the package installation directory.

If you want to check out more difference between **pkgng** and **pkg_install** check out [this](https://glenbarber.us/2012/06/11/Maintaining-Your-Own-pkgng-Repository.html) post. Or if you want more information regarding the **pkgng** format check out [this](https://wiki.freebsd.org/pkgng) page.

Looking over the native splunk Freebsd package, I saw the following:

	moxz:~>tar tvzf splunk-6.1.3-220630-freebsd-7.3-amd64.tgz | head
	-rw-r--r--  0 root   wheel 1013608 Jul 29 17:06 +CONTENTS
	-rw-r--r--  0 root   wheel     328 Jul 29 17:06 +COMMENT
	-rw-r--r--  0 root   wheel       8 Jul 29 17:06 +DESC
	-rwxr-xr-x  0 root   wheel    2942 Jul 29 17:06 +INSTALL
	-rwxr-xr-x  0 root   wheel    6086 Jul 29 17:06 +POST-INSTALL
	-rwxr-xr-x  0 root   wheel     713 Jul 29 17:06 +DEINSTALL
	-rwxr-xr-x  0 root   wheel     119 Jul 29 17:06 +POST-DEINSTALL
	-r--r--r--  0 root   wheel     506 Jul 29 17:06 splunk/README-splunk.txt
	-r-xr-xr-x  0 root   wheel   40056 Jul 29 17:06 splunk/bin/bloom
	-r-xr-xr-x  0 root   wheel   40056 Jul 29 17:06 splunk/bin/btool

I extracted the **+INSTALL** and **+POST-INSTALL** files to check what they did and they just make sure that the **splunk** user exists and automatically start up the **splunk** service.... I think I can handle that. 

Also we see that the splunk native package doesn't contain the YAML **+MANIFEST** file and that's why the new **pkgng** is failing to install it. So I went ahead and used the *non-native* package to proceed with the update. 

### Updating Splunk

I just extracted the archive on top of the current install:

	moxz:~>sudo tar xvzf splunk-6.1.3-220630-FreeBSD7-amd64.tgz -C /opt

Then checking out what the install will do:

	moxz:~>sudo /opt/splunk/bin/splunk start --accept-license
	
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
	
	
	Perform migration and upgrade without previewing configuration changes? [y/n] n
	
	-- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2014-08-11.10-21-49' --
	
	Migrating to:
	VERSION=6.1.3
	BUILD=220630
	PRODUCT=splunk
	PLATFORM=FreeBSD-amd64
	
	
	********** BEGIN PREVIEW OF CONFIGURATION FILE MIGRATION **********
	
	Would copy '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.
	
	Checking saved search compatibility...
	
	Handling deprecated files...
	
	Checking script configuration...
	
	Would copy '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
	Would delete '/opt/splunk/etc/system/local/field_actions.conf.migratePreview'.
	Would move '/opt/splunk/share/splunk/search_mrsparkle/modules' to '/opt/splunk/share/splunk/search_mrsparkle/modules.old.20140811-102149'.
	Would move '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
	Checking for possible UI view conflicts...
	
	The following files would be created or modified (without the .migratePreview extension):
	  /opt/splunk/etc/system/local/field_actions.conf.migratePreview
	
	Migration is continuing...
	
	Clustering migration already complete, no further changes required.
	
	
	********** END PREVIEW OF CONFIGURATION FILE MIGRATION **********
	
	Stopping because you requested a preview of the configuration files to be
	migrated.  Migration and upgrade will not continue until the configuration files
	have actually been migrated.
	
	To proceed, run 'splunk start' again and choose 'y'.
	
The changes looks good to me, I just ran the command again and selected ***y*** to perform the update and it went through without issues:


	- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2014-08-11.10-32-06' --
	
	Migrating to:
	VERSION=6.1.3
	BUILD=220630
	PRODUCT=splunk
	PLATFORM=FreeBSD-amd64
	
	Copying '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.
	
	Checking saved search compatibility...
	
	Handling deprecated files...
	
	Checking script configuration...
	
	Copying '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
	Deleting '/opt/splunk/etc/system/local/field_actions.conf'.
	Moving '/opt/splunk/share/splunk/search_mrsparkle/modules' to '/opt/splunk/share/splunk/search_mrsparkle/modules.old.20140811-103206'.
	Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
	Checking for possible UI view conflicts...
	
	Clustering migration already complete, no further changes required.
	
	
	Splunk> Winning the War on Error
	
	Checking prerequisites...
		Checking http port [8000]: open
		Checking mgmt port [8089]: open
		Checking configuration...  Done.
		Checking critical directories...	Done
		Checking indexes...
			Validated: _audit _blocksignature _internal _introspection _thefishbucket history main summary
		Done
		Checking filesystem compatibility...  Done
		Checking conf files for problems...
		Done
	All preliminary checks passed.
	
	Starting splunk server daemon (splunkd)...
	Done
	
	Starting splunkweb...  Done
	
	
	If you get stuck, we're here to help.
	Look for answers here: http://docs.splunk.com
	
	The Splunk web interface is at http://moxz.local.com:8000
	
After visiting the Splunk Web interface, I was able to confirm the old settings were still intact. 