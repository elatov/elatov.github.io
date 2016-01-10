---
published: true
layout: post
title: "Playing Around with Conky on Gentoo"
author: Karim Elatov
categories: [os]
tags: [linux,gentoo,conky]
---
I wanted to try out conky on my gentoo machine, just too see how it looks like. There is a nice tool called [Conky Manager](https://launchpad.net/conky-manager) which allows you to try out different Conky themes with ease, so let's install it.

###Conky Manager Prerequisites

First we need to install **valac**, we can use a utility called **e-file** to find out which package a file belongs to:

	elatov@gen:~$e-file valac
	[I] dev-lang/vala
	    Available Versions: 0.8.1-r0 0.8.1 0.8.0-r0 0.7.10-r0 0.7.9-r0 0.7.8-r0 9999-r0 0.7.7-r0 0.7.5-r0 0.7.4-r0 0.6.1-r0 0.7.10 0.9.8 0.9.5 0.9.3
	    Last Installed Ver: 0.24.0-r1(Thu 11 Dec 2014 10:40:47 PM MST)
	    Homepage:       https://wiki.gnome.org/Vala
	    Description:        Compiler for the GObject type system
	    Matched Files:      /usr/bin/valac;

Now let's install it:

	sudo emerge -av vala

Lastly let's create a symlink

	sudo ln -s /usr/bin/valac-0.24 /usr/bin/valac

We also need the **gee-0.8.pc** file:

	elatov@gen:~$e-file gee-0.8.pc
	[I] dev-libs/libgee
		Available Versions:	0.10.3 0.16.1 0.18.0
		Last Installed Ver:	0.6.8(Sat 21 Feb 2015 01:55:23 PM MST)
		Homepage:		https://live.gnome.org/Libgee
		Description:		GObject-based interfaces and classes for commonly used data structures
		Matched Files:		/usr/lib64/pkgconfig/gee-0.8.pc; /usr/lib/pkgconfig/gee-0.8.pc;

It looks like a specific version has that file, let's see what available versions we can install:

	elatov@gen:~eix libgee
	[I] dev-libs/libgee
	     Available versions:
	     (0)    0.6.7 0.6.8
	     (0.8)  0.14.0 0.16.1(0.8/2) 0.18.0(0.8/2)
	       {+introspection}
	     Installed versions:  0.18.0(0.8)(11:57:50 AM 11/28/2015)(introspection)
	     Homepage:            https://wiki.gnome.org/Projects/Libgee
	     Description:         GObject-based interfaces and classes for commonly used data structures

So from the **e-file** output we can see that versions **0.10.3 0.16.1 0.18.0** of **libgee** have our desired file. And from the **eix** output we can see that **0.8** is the sub version of all the said versions. So we can just install the latest version and we will be okay:

	sudo emerge -av libgee

We also need **gtk+-3** and I already had that installed:

	elatov@gen:~$equery l gtk+:3
	 * Searching for gtk+:3 ...
	[IP-] [  ] x11-libs/gtk+-3.16.7:3

Lastly we need to install **bzr** so we can get the source. I ended up enabling a couple of **use** flags for the package:

	$ cat /etc/portage/package.use/bzr
	dev-vcs/bzr curl

and then installed it with the following command:

	$ sudo emerge -av bzr
	
### Installing Conky Manager

To get the source we can run the following:

	$ bzr branch lp:conky-manager
	You have not informed bzr of your Launchpad ID, and you must do this to
	write to Launchpad or access private data.  See "bzr help launchpad-login".
	Branched 136 revisions.

If you want you can also get the *tar* archive of the source from here:

> http://bazaar.launchpad.net/~teejee2008/conky-manager/trunk/tarball/136?start_revid=136


Now let's build the software:

	$ cd conky-manager
	$ make

By default it wants to install the software under **/usr** let's fix that by modifying the **conky-manager/src/makefile** file as such:

	- prefix=/usr
	+ prefix=/usr/local/conky-manager

And let's prepare the destination install directory:

	$ sudo mkdir /usr/local/conky-manager
	$ sudo chown elatov:elatov /usr/local/conky-manager

To finally install it we can just run the following:

	$ make install

### More Prerequisites
The *Conky Manager* uses external tools to load the themes so let's install them. First is **7zip**:

	$ sudo emerge -av p7zip

Next we need to install the **import** tool from **imagemagick**, I already had that installed and here were my use flags:

	$equery u imagemagick | grep '\+'
	+X
	+bzip2
	+cxx
	+jpeg
	+openmp
	+truetype
	+zlib
	
Other wise you will get errors like this:

	$ /usr/local/conky-manager/bin/conky-manager
	[12:01:52] Error: Commands listed below are not available:
	
	 * import
	
	Please install required packages and try running it again

### Import Conky Themes into Conky Manager

Now let's go ahead and grab all the themes from [Official Theme Pack #1 (15 MB)](http://www.mediafire.com/download/icvmpzhlk7vgejt/default-themes-extra-1.cmtp.7z) 

Then start **conky-manager**:

	$ /usr/local/conky-manager/bin/conky-manager

And import the themes:

![import-themes-button-cm](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/conky-gentoo/import-butttom-cm2.png)

And then you can click on widget and get a preview of how they will look like:

![cm-show-prev](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/conky-gentoo/conky-prev-2.png)

After you are done with choosing and previewing the themes or widgets the conky manager will create a startup script that can be launched at started up. For example here is what I had:

	$ cat .conky/conky-startup.sh
	sleep 20s
	killall conky
	cd "/home/elatov/.conky/Conky Seamod"
	conky -c "/home/elatov/.conky/Conky Seamod/conky_seamod" &
	cd "/home/elatov/.conky/Emays"
	conky -c "/home/elatov/.conky/Emays/conkyrc" &
	cd "/home/elatov/.conky/NvidiaPanel"
	conky -c "/home/elatov/.conky/NvidiaPanel/NvidiaPanel" &

### Conky Screenshots

I ended up using 3 different widgets, one on the right screen:

![conky-1](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/conky-gentoo/conky-1.png)

And the two on the left screen:

![conky-left-screen](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/conky-gentoo/conky-left-screen.png)
