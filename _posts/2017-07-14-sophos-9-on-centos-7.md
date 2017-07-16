---
published: true
layout: post
title: "Sophos 9 on CentOS 7"
author: Karim Elatov
categories: [security]
tags: [sophos]
---
### Sophos
As I was going through the [lynis suggestions](/2017/06/install-lynis-and-fix-some-suggestions/), I realized that I should install an anti-virus solution on my machine. After reading a couple of sites:

* [AV-Test Lab tests 16 Linux antivirus products against Windows and Linux malware](http://www.networkworld.com/article/2989137/linux/av-test-lab-tests-16-linux-antivirus-products-against-windows-and-linux-malware.html)
* [The 7 Best Free Linux Anti-Virus Programs](http://www.makeuseof.com/tag/free-linux-antivirus-programs/)

I decided to try out [sophos](https://www.sophos.com/en-us/products/free-tools/sophos-antivirus-for-linux.aspx). I have used **clamav** in the past but apparently now it's detection rate is pretty low:

![av-det-rate](https://seacloud.cc/d/480b5e8fcd/files/?p=/sophos-install/av-det-rate.png&raw=1)


### Installing Sophos

The instructions are covered in [Installing the standalone version of SAV for Linux/UNIX](https://community.sophos.com/kb/en-us/14378) and also in the [Sophos Anti-Virus for Linux startup guide](https://www.sophos.com/en-us/medialibrary/pdfs/documentation/savl_9_sgeng.pdf). I downloaded the archive (the [How to Install Sophos Anti-Virus (Free Edition) on CentOS 7 / RHEL 7](http://www.techbrown.com/install-sophos-anti-virus-free-edition-centos-7-rhel-7.shtml) page has good screenshots of the process) and then I extracted the archive:

	<> tar xzf sav-linux-free-9.tgz

Now let's do the install:
	
	<> cd sophos-av
	<> sudo ./install.sh
	
	Sophos Anti-Virus
	=================
	Copyright (c) 1989-2016 Sophos Limited. All rights reserved.
	
	Welcome to the Sophos Anti-Virus installer. Sophos Anti-Virus contains an on-
	access scanner, an on-demand command-line scanner, the Sophos Anti-Virus daemon,
	and the Sophos Anti-Virus GUI.
	
	On-access scanner         Scans files as they are accessed, and grants access
	                          to only those that are threat-free.
	On-demand scanner         Scans the computer, or parts of the computer,
	                          immediately.
	Sophos Anti-Virus daemon  Background process that provides control, logging,
	                          and email alerting for Sophos Anti-Virus.
	Sophos Anti-Virus GUI     User interface accessed through a web browser.
	
	
	Press <return> to display Licence. Then press <spc> to scroll forward.
	Please read the following legally binding License Agreement between Sophos and
	
	Do you accept the licence? Yes(Y)/No(N) [N]
	> Y
	
	Where do you want to install Sophos Anti-Virus? [/opt/sophos-av]
	>
	
	Do you want to enable on-access scanning? Yes(Y)/No(N) [Y]
	>
	
	Sophos recommends that you configure Sophos Anti-Virus to auto-update.
	
	It can update either from Sophos directly (requiring username/password details)
	or from your own server (directory or website (possibly requiring
	username/password)).
	
	Which type of auto-updating do you want? From Sophos(s)/From own server(o)/None(n) [s]
	> s
	
	Updating directly from Sophos.
	Do you wish to install the Free (f) or Supported (s) version of SAV for Linux? [s]
	> f
	
	The Free version of Sophos Anti-Virus for Linux comes with no support.
	Forums are available for our free tools at http://openforum.sophos.com/
	Do you need a proxy to access Sophos updates? Yes(Y)/No(N) [N]
	> n
	
	Fetching free update credentials.
	Installing Sophos Anti-Virus....
	Selecting appropriate kernel support...
	When Sophos Anti-Virus starts, it updates itself to try to find a Sophos kernel interface module update. This might cause a significant delay.
	Sophos Anti-Virus starts after installation.
	
	Installation completed.
	Your computer is now protected by Sophos Anti-Virus.
	
Also as an FYI, it looks likes the UI is no longer available for **sophos** as per [SAV Linux 9.11.0 GUI functionality no longer available](https://community.sophos.com/kb/en-us/122722).

#### Compiling the Talpa Module
Initially the **talpa** module failed to compile:

	[root@m2 kernels]# tail -11 /opt/sophos-av/log/talpaselect.log
	checking for linux/version.h... configure: error: cannot proceed without the required header file
	
	Traceback (most recent call last):
	  File "talpa_select.py", line 2176, in _action
	  File "talpa_select.py", line 1074, in load
	  File "talpa_select.py", line 841, in select
	  File "talpa_select.py", line 1696, in select
	  File "talpa_select.py", line 1780, in build
	  File "talpa_select.py", line 1910, in __try_build
	  File "talpa_select.py", line 1769, in checkConfigureErrors
	SelectException: exc-configure-failed-no-kernel-headers

I was missing the kernel source, so I installed that:

	<> sudo yum install kernel-devel

Re-running the compile worked out:

	[root@m2 ~]# /opt/sophos-av/engine/talpa_select select
	[Talpa-select]
	Copyright (c) 1989-2016 Sophos Limited. All rights reserved.
	Sat Dec 24 17:42:16 2016 GMT
	Linux distribution: [centos]
	Product: [CentOS Linux release 7.3.1611 (Core) ]
	Kernel: [3.10.0-514.2.2.el7.x86_64]
	Multiprocessor support enabled.
	Searching for source pack...
	Searching for suitable binary pack...
	No suitable binary pack available.
	Preparing for build...
	Extracting sources...
	Configuring build of version 1.21.5...
	Building...
	Installing binaries...
	Creating local binary pack...

And now let's load the module:

	[root@m2 sophos-av]# /opt/sophos-av/engine/talpa_select load
	[Talpa-select]
	Copyright (c) 1989-2016 Sophos Limited. All rights reserved.
	Sat Dec 24 17:46:05 2016 GMT
	Linux distribution: [centos]
	Product: [CentOS Linux release 7.3.1611 (Core) ]
	Kernel: [3.10.0-514.2.2.el7.x86_64]
	Multiprocessor support enabled.
	Searching for source pack...
	Searching for suitable binary pack...
	Binary pack was created locally.
	Found suitable binary pack. Using: /opt/sophos-av/talpa/compiled/talpa-binpack-centos-x86_64-3.10.0-514.2.2.el7.x86_64-1smptuedec6230641utc2016.tar.gz
	Loading Talpa kernel modules version 1.21.5...

And to confirm it's loaded:

	[root@m2 sophos-av]# lsmod | grep tal
	talpa_vfshook          39969  0
	talpa_pedconnector     12509  0
	talpa_pedevice         13563  1 talpa_pedconnector
	talpa_vcdevice         13129  0
	talpa_core             91941  3 talpa_vfshook,talpa_vcdevice
	talpa_linux            34583  4 talpa_vfshook,talpa_vcdevice,talpa_core
	talpa_syscallhook      20252  1 talpa_vfshook

### Manually Updating Sophos
The update is configured to run every 60 minutes, but we can do one manually:

	[root@m2 etc]# /opt/sophos-av/bin/savupdate
	Updating from versions - SAV: 9.12.3, Engine: 3.65.2, Data: 5.30
	Updating Sophos Anti-Virus....
	Updating Talpa Binary Packs
	Updating SAVScan on-demand scanner
	Updating Virus Engine and Data
	Updating Talpa Kernel Support
	Updating Manifest
	Selecting appropriate kernel support...
	Update completed.
	Updated to versions - SAV: 9.12.3, Engine: 3.65.2, Data: 5.34
	Successfully updated Sophos Anti-Virus from sdds:SOPHOS

For good measure, let's restart the service after the update:

	<> sudo systemctl restart sav-protect.service

I also double checked the services were enabled:

	[root@m2 ~]# /opt/sophos-av/bin/savdstatus
	Sophos Anti-Virus is active and on-access scanning is running
	[root@m2 ~]# /opt/sophos-av/bin/savconfig query EnableOnStart
	true
	[root@m2 ~]# /opt/sophos-av/bin/savconfig query LiveProtection
	enabled

There are also a couple of services that are disabled (and I think that is okay):

	<> systemctl list-unit-files| grep sav
	sav-protect.service                           enabled
	sav-rms.service                               disabled
	sav-update.service                            disabled

### Configuring Sophos Settings
You can check out the basic settings by running the following:

	[root@m2 ~]# /opt/sophos-av/bin/savconfig query
	Email: root@localhost
	EmailDemandSummaryIfThreat: true
	EmailLanguage: English
	EmailNotifier: true
	EmailServer: localhost:25
	EnableOnStart: true
	ExclusionEncodings: UTF-8
	                    EUC-JP
	                    ISO-8859-1
	LogMaxSizeMB: 100
	NotifyOnUpdate: true
	PrimaryUpdateSourcePath: sophos:
	PrimaryUpdateUsername: ********
	PrimaryUpdatePassword: ********
	UploadSamples: false
	SendErrorEmail: true
	SendThreatEmail: true
	UINotifier: true
	UIpopupNotification: true
	UIttyNotification: true
	UpdatePeriodMinutes: 1440
	NamedScans: weekly
	LiveProtection: enabled
	ScanArchives: mixed

To get a full list you can run the following:

	[root@m2 ~]# /opt/sophos-av/bin/savconfig --advanced query

I enabled the option to be notified on an update:

	[root@m2 ~]# /opt/sophos-av/bin/savconfig set NotifyOnUpdate true
	[root@m2 ~]# /opt/sophos-av/bin/savconfig query NotifyOnUpdate
	true

By default the update period of 60 minutes so I decided to changed that to once a day:

	[root@m2 ~]# /opt/sophos-av/bin/savconfig set UpdatePeriodMinutes 1440

Else you will see this in the logs all the time (and if you enabled the option to be emailed on an update, you will get an email every 60 minutes):

	Dec 24 18:51:39 m2.kar.int systemd[1]: Started "Sophos Anti-Virus update".
	Dec 24 18:51:39 m2.kar.int savd[11120]: update.updated: Successfully updated Sophos Anti-Virus from sdds:SOPHOS
	Dec 24 18:51:39 m2.kar.int savd[11120]: update.updated: Updated to versions - SAV: 9.12.3, Engine: 3.65.2, Data: 5.34
	Dec 24 18:51:39 m2.kar.int savd[11120]: update.updated: Updating Sophos Anti-Virus....
	                                        Updating SAVScan on-demand scanner
	                                        Updating Virus Engine and Data
	                                        Updating Manifest
	                                        Update completed.
	Dec 24 18:51:39 m2.kar.int savd[11120]: update.updated: Updating from versions - SAV: 9.12.3, Engine: 3.65.2, Data: 5.34
	Dec 24 18:51:17 m2.kar.int systemd[1]: Starting "Sophos Anti-Virus update"...

### Running a quick scan manually
You can run a quick scan manually to see how clean your system is:

	> sudo /opt/sophos-av/bin/savscan /
	SAVScan virus detection utility
	Version 5.27.0 [Linux/AMD64]
	Virus data version 5.34, November 2016
	Includes detection for 12414465 viruses, Trojans and worms
	Copyright (c) 1989-2016 Sophos Limited. All rights reserved.
	
	System time 12:08:18 PM, System date 24 December 2016
	
	IDE directory is: /opt/sophos-av/lib/sav
	
	Using IDE file fare-boh.ide
	Using IDE file dride-wf.ide
	Using IDE file rans-dwk.ide
	Using IDE file fare-bol.ide
	Using IDE file chisb-lh.ide
	Using IDE file zeus-k.ide
	...
	...
	Using IDE file docd-gja.ide
	Using IDE file fare-bwv.ide
	Using IDE file locky-yo.ide
	Using IDE file mdro-hrr.ide
	Using IDE file locky-yp.ide
	Using IDE file cerbe-xy.ide
	
	Quick Scanning
	
	Could not open /etc/alternatives/policytool
	Could not open /usr/bin/policytool
	Could not open /usr/lib/modules/3.10.0-327.28.3.el7.x86_64/source
	Could not open /usr/lib/modules/3.10.0-327.36.1.el7.x86_64/source
	Could not open /usr/lib/modules/3.10.0-327.36.2.el7.x86_64/source
	Could not open /usr/lib/modules/3.10.0-327.36.3.el7.x86_64/source
	
	42781 files scanned in 1 minute and 25 seconds.
	6 errors were encountered.
	No viruses were discovered.
	End of Scan.

### Setup a schedule to scan weekly
Thi is covered in [Sophos Anti-Virus for Linux
configuration guide](https://www.sophos.com/en-us/medialibrary/PDFs/documentation/savl_9_cgeng.pdf) and [Sophos Anti-Virus v9.x For Unix/Linux: Scheduled scan options](https://community.sophos.com/kb/en-us/114372
). First create a folder for sheduled jobs:

	[root@m2 ~]# mkdir /opt/sophos-av/etc/jobs

Then copy the example to get started:

	<> sudo cp /opt/sophos-av/doc/namedscan.example.en /opt/sophos-av/etc/jobs/weekly

Modify the job to your needs:

	<> sudo vi /opt/sophos-av/etc/jobs/weekly

And lastly add it to the config:

	<> sudo /opt/sophos-av/bin/savconfig add NamedScans weekly /opt/sophos-av/etc/jobs/weekly

If you need to update it, first update the file (`vi /opt/sophos-av/etc/jobs/weekly`) and then update the config

	<> sudo /opt/sophos-av/bin/savconfig update NamedScans weekly /opt/sophos-av/etc/jobs/weekly

To always get a summary of the scheduled **savscan**, you can set the following option (as per the [Sophos Anti-Virus for Linux/Unix v9: Complete list of email alert settings](https://community.sophos.com/kb/en-us/118385):

	<> sudo /opt/sophos-av/bin/savconfig set EmailDemandSummaryAlways true
	
That should be it, enjoy **sophos**.
