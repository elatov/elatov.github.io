---
title: Pkgng and Freebsd 9
author: Karim Elatov
layout: post
permalink: /2012/10/pkgng-and-freebsd-9/
dsq_thread_id:
  - 1406559376
categories: ['os']
tags: ['freebsd', 'freebsd_pkg', 'pkgng', 'portmaster']
---

I updated my *portmaster* package the other day and I saw the following message:


	elatov@freebsd:~>pkg info -D -x portmaster
	If you are upgrading from the old package format, there are 2
	extra steps required.

	Enable PKGNG as your package format:

	# echo 'WITH_PKGNG=yes' >> /etc/make.conf

	Then convert your /var/db/pkg database to the new pkg format:

	# pkg2ng



I did some research and it seems that the FreeBSD package management tool is getting replaced with a new utility called pkgng (pkg new generation). There is a great blog about this new tool, it's entitled "[pkgng: First look at FreeBSD’s new package manager](http://mebsd.com/make-build-your-freebsd-word/pkgng-first-look-at-freebsds-new-package-manager.html)". If you read over that blog, I am sure you will be excited since FreeBSD is moving to an easier package management. So I decided to give it a try. To do so, first install the new tool:


	elatov@freebsd:~> cd /usr/ports/ports-mgmt/pkg
	elatov@freebsd:/usr/ports/ports-mgmt/pkg> sudo make install clean


Next you can convert your old package management database to the new tool just by running:


	elatov@freebsd:~> sudo pkg2ng


After you run the above command, commands like *pkg_info*, *pkg_version*, and *pkg_add* will become obsolete. You will see the following messages:


	elatov@freebsd:~>pkg_version
	pkg_version: the package info for package 'autoconf-2.69' is corrupt
	pkg_version: the package info for package 'automake-1.12.4' is corrupt
	pkg_version: the package info for package 'bash-4.2.37' is corrupt


But have no fear, all the commands that could be run with the previous tools are available with the *pkg* utility. For instances here are some examples:


	# old way, install binary version of the package
	$ pkg_add -r PKG_NAME

	# New way, install binary version of package
	$ pkg install PKG_NAME
	* You need to setup a repository before running this command (more info in the above blog)

	# old way to list outdated packages
	pkg_version -vIL=

	# New way to list outdated packages
	pkg version -vIL=

	# Old way, list files installed by package
	pkg_info -L PKG_NAME
	# New way, list files installed by package
	pkg info -l PKG_NAME

	# Old way, list package that installed a file
	pkg_info -W /path/to/file

	# New way, list package that installed a file
	pkg which /path/to/file


There are also a lot of new functionality available, like *pkg search*, and *pkg query*. Some examples are seen in the above blog and they look pretty advanced.

After you installed the package and converted the database, you want newly installed ports to be registered with the new packaging system. To do so run the following:


	elatov@freebsd:~> sudo echo 'WITH_PKGNG=yes' >> /etc/make.conf


and lastly recompile your port management tool to do the same. I use *portmaster*, here is how my config looked like after I ran *make config*:


	elatov@freebsd:~>cd /usr/ports/ports-mgmt/portmaster/
	elatov@freebsd:/usr/ports/ports-mgmt/portmaster>sudo make config
	elatov@freebsd:/usr/ports/ports-mgmt/portmaster>sudo make showconfig
	===> The following configuration options are available for portmaster-3.14_6:
	BASH=off: Install programmable completions for Bash
	PKGNGPATCH=on: Enable PKGNG support
	ZSH=off: Install programmable completions for zsh
	===> Use 'make config' to modify these settings
	elatov@freebsd:/usr/ports/ports-mgmt/portmaster> sudo make reinstall


Now every time you install a new port with *portmaster* it will be registered with the new *pkgng* database and you can use the above commands to query all the information you need.
