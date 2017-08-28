---
published: true
layout: post
title: "Using WP Scan Docker Image with CoreOS"
author: Karim Elatov
categories: [containers]
tags: [docker,wpscan,coreos,systemd-timers]
---
### WPScan
I wanted to run [WPScan](https://wpscan.org/) against my wordpress install just to make sure I don't miss anything obvious. Looking over the prerequisites, it looks like it needs a specific version of **ruby**:

> Ruby >= 2.1.9 - Recommended: 2.3.3

I checked out my *Debian* and *CentOS* machines and I realized they didn't have that version yet:

	<> ruby -v
	ruby 2.1.5p273 (2014-11-13) [x86_64-linux-gnu]
	
	<> ruby -v
	ruby 2.0.0p648 (2015-12-16) [x86_64-linux]

Then I remembered that I have a CoreOS machine with docker on it, and what a perfect way to utilize it (since **WPScan** provides a docker image with the right version of **ruby** installed).

### WPScan Docker Image
To get the image we can just run the following:

	$ docker pull wpscanteam/wpscan

BTW if you want to check out the image you can run the following

	$ docker run -it --entrypoint /bin/sh wpscanteam/wpscan

Since by default it specifies an **entrypoint** in it's **Dockerfile**. So you can't override the command by just passing in arguements (more on that at [Docker RUN vs CMD vs ENTRYPOINT](http://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/)).

Then we can just run this to get our report:

	elatov@core ~ $ docker run --rm wpscanteam/wpscan -u https://kerch.kar.int/wordpress --disable-tls-checks
	
	        __          _______   _____
	        \ \        / /  __ \ / ____|
	         \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
	          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
	           \  /\  /  | |     ____) | (__| (_| | | | |
	            \/  \/   |_|    |_____/ \___|\__,_|_| |_|
	
	        WordPress Security Scanner by the WPScan Team
	                       Version 2.9.2
	          Sponsored by Sucuri - https://sucuri.net
	   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
	_______________________________________________________________
	
	[+] URL: https://kerch.kar.int/wordpress/
	[+] Started: Mon Feb 13 23:01:22 2017
	
	[!] 12 vulnerabilities identified from the version number
	
	[!] Title: WordPress 4.3-4.7 - Potential Remote Command Execution (RCE) in PHPMailer
	    Reference: https://wpvulndb.com/vulnerabilities/8714
	    Reference: https://www.wordfence.com/blog/2016/12/phpmailer-vulnerability/
	    Reference: https://github.com/PHPMailer/PHPMailer/wiki/About-the-CVE-2016-10033-and-CVE-2016-10045-vulnerabilities
	    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
	[i] Fixed in: 4.7.1
	
	[i] Fixed in: 4.7.2
	
	[+] WordPress theme in use: suffusion - v4.4.9
	
	[+] Name: suffusion - v4.4.9
	 |  Latest version: 4.4.9 (up to date)
	 |  Last updated: 2016-01-27T00:00:00.000Z
	 |  Location: https://kerch.kar.int/wordpress/wp-content/themes/suffusion/
	 |  Readme: https://kerch.kar.int/wordpress/wp-content/themes/suffusion/readme.txt
	 |  Style URL: https://kerch.kar.int/wordpress/wp-content/themes/suffusion/style.css
	 |  Referenced style.css: https://www.moxz.tk/wordpress/wp-content/themes/suffusion/style.css
	
	[+] Enumerating plugins from passive detection ...
	[+] No plugins found
	
	[+] Finished: Mon Feb 13 23:01:28 2017
	[+] Requests Done: 69
	[+] Memory used: 17.902 MB
	[+] Elapsed time: 00:00:06

That was great and easy, but now I want to schedule that to run weekly and to send the output over email like **cron** would.

### Using toolbox in CoreOS to send an email

CoreOS provides a **toolbox** container: [Install debugging tools](https://coreos.com/os/docs/latest/install-debugging-tools.html). It basically runs a *Fedora* docker image and mounts the root directory **/** (from the CoreOS host) into **/media/root** inside the container. So first let's try out sending an email using **toolbox**:

	elatov@core ~ $ toolbox
	latest: Pulling from library/fedora
	0fc456f626d7: Pull complete
	Digest: sha256:a99209cbb485b98d17b47be2bf990a7fbd63b4d3fa61395a313308d99a326930
	Status: Downloaded newer image for fedora:latest
	537bbbfbd4aa7a26763463d367b68a5c5dc3688a071fb506d8782d924ee99d17
	elatov-fedora-latest
	Spawning container elatov-fedora-latest on /var/lib/toolbox/elatov-fedora-latest.
	Press ^] three times within 1s to kill container.
	
	[root@core ~]# dnf install mailx
	Last metadata expiration check: 0:01:02 ago on Mon Feb 13 23:31:29 2017.
	Dependencies resolved.
	==============================================================================================================================$
	 Package                    Arch                        Version                              Repository                   Size
	==============================================================================================================================$
	Installing:
	 mailx                      x86_64                      12.5-19.fc24                         fedora                      258 k


I ran into an issue where installing any package would **sigkill** my **toolbox** container:

	Downloading Packages:
	[SKIPPED] mailx-12.5-19.fc24.x86_64.rpm: Already downloaded
	warning: /var/cache/dnf/fedora-310f9d37d74ceec1/packages/mailx-12.5-19.fc24.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID fdb19c98: NOKEY
	Container elatov-fedora-latest terminated by signal KILL.

The problem is discussed here:

* [Can't install package in toolbox #1698](https://github.com/coreos/bugs/issues/1698) 
* [Toolbox quits when any program sends a sigkill not the top level command #1216](https://github.com/coreos/bugs/issues/1216)

There are two workarounds: go back to using **Fedora 24** image for the **toolbox** container or import the **GPG** keys manually, I decided to do the latter:

	elatov@core ~ $ toolbox
	Spawning container elatov-fedora-latest on /var/lib/toolbox/elatov-fedora-latest.
	Press ^] three times within 1s to kill container.
	[root@core ~]# rpm --import /etc/pki/rpm-gpg/RPM*
	[root@core ~]# dnf install mailx
	Last metadata expiration check: 0:04:25 ago on Mon Feb 13 23:31:29 2017.
	Dependencies resolved.
	===============================================================================================================================
	 Package                    Arch                        Version                              Repository                   Size
	===============================================================================================================================
	Installing:
	 mailx                      x86_64                      12.5-19.fc24                         fedora                      258 k
	
	Transaction Summary
	===============================================================================================================================
	Install  1 Package
	
	Total size: 258 k
	Installed size: 479 k
	Is this ok [y/N]: y
	Downloading Packages:
	[SKIPPED] mailx-12.5-19.fc24.x86_64.rpm: Already downloaded
	Running transaction check
	Transaction check succeeded.
	Running transaction test
	Transaction test succeeded.
	Running transaction
	  Installing  : mailx-12.5-19.fc24.x86_64                                                                                  1/1
	  Verifying   : mailx-12.5-19.fc24.x86_64                                                                                  1/1
	
	Installed:
	  mailx.x86_64 12.5-19.fc24
	
	Complete!

Now let's point to an SMTP server and try out sending an email:

	elatov@core ~ $ toolbox
	Spawning container elatov-fedora-latest on /var/lib/toolbox/elatov-fedora-latest.
	Press ^] three times within 1s to kill container.
	[root@core ~]# vi .mailrc
	[root@core ~]# cat .mailrc
	set smtp=smtp://mail.kar.int
	[root@core ~]# mailx -s test elatov@me.com
	cool
	EOT
	[root@core ~]#
	Container elatov-fedora-latest terminated by signal KILL.

And I actually got the email. I then wrote a script within the **toolbox** container to send the email and just ran that (this is for later use):

	elatov@core ~ $ toolbox -q /root/s.sh

The whole filesystem for the toolbox container is under **/var/lib/toolbox/root-fedora-latest/**:

    core ~ # ls /var/lib/toolbox/root-fedora-latest/
    bin   dev  home  lib64       media  opt   root  sbin  sys  usr
    boot  etc  lib   lost+found  mnt    proc  run   srv   tmp  var

Here is the file that I edited inside the container:

    core ~ # cat /var/lib/toolbox/root-fedora-latest/root/.mailrc 
    set smtp=smtp://mail.kar.int


### Using systemd-timers in CoreOS

It looks like **cron** is not available on CoreOS but instead uses **systemd-timers**: [Scheduling tasks with systemd timers](https://coreos.com/os/docs/latest/scheduling-tasks-with-systemd-timers.html). So I wanted to create a **systemd-timer** to run the **WPScan** weekly. First I created a **systemd** service:

	elatov@macm ~ $ cat /etc/systemd/system/wpscan.service
	[Unit]
	Description=Run WP-Scan
	
	[Service]
	User=root
	Type=oneshot
	ExecStart=/opt/bin/wp-scan.sh

Then I created a **timer** for that service:

	elatov@macm ~ $ cat /etc/systemd/system/wpscan.timer
	[Unit]
	Description=Run wp-scan weekly
	
	[Timer]
	OnCalendar=Sat *-*-* 03:00:00
	Persistent=true
	
	[Install]
	WantedBy=timers.target

And the script is quite simple:

	elatov@macm ~ $ cat /opt/bin/wp-scan.sh
	#!/bin/bash
	
	# update the container if necessary
	/bin/docker pull wpscanteam/wpscan:latest
	
	# run docker wp-scan
	/bin/docker run --rm wpscanteam/wpscan -u https://kerch.kar.int/wordpress --disable-tls-checks --no-color --no-banner >> /tmp/wp.txt
	
	# send email
	/bin/toolbox -q "/usr/local/bin/wp-email.sh"
	
	# remove report
	/bin/rm /tmp/wp.txt

And the script inside the **toolbox** container is also pretty simple
	
	elatov@macm ~ $ toolbox -q cat /usr/local/bin/wp-email.sh
	#!/bin/bash
	
	# send email
	/bin/mail -s "WP Results" elatov@me.com < /media/root/tmp/wp.txt

For the **systemd** to pick up the new service and time we need to reload the daemon:

	$ systemctl daemon-reload

Then start the **timer**:

	elatov@macm ~ $ sudo systemctl start wpscan.timer

and you can confirm it's scheduled:

	elatov@macm ~ $ systemctl list-timers wpscan.timer
	NEXT                         LEFT        LAST PASSED UNIT         ACTIVATES
	Thu 2017-03-02 22:05:00 UTC  6 days left n/a  n/a    wpscan.timer wpscan.service

If you make a change: modify the file, reload the daemon, and it will pick up the new time:

	elatov@macm ~ $ sudo systemctl daemon-reload
	elatov@macm ~ $ systemctl list-timers wpscan.timer
	NEXT                         LEFT        LAST PASSED UNIT         ACTIVATES
	Thu 2017-03-02 05:08:00 UTC  6 days left n/a  n/a    wpscan.timer wpscan.service
	
	1 timers listed.

Notice the time changes to **05:08**. After it's has run, make sure you get the results:

	macm ~ # systemctl status wpscan
	● wpscan.service - Run WP-Scan
	   Loaded: loaded (/etc/systemd/system/wpscan.service; static; vendor preset: disabled)
	   Active: inactive (dead) since Fri 2017-02-24 05:31:15 UTC; 23s ago
	  Process: 7155 ExecStart=/opt/bin/wp-scan.sh (code=exited, status=0/SUCCESS)
	 Main PID: 7155 (code=exited, status=0/SUCCESS)
	
	Feb 24 05:31:00 macm systemd[1]: Starting Run WP-Scan...
	Feb 24 05:31:15 macm sudo[7270]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/bin/systemd-nspawn --directory=/var/lib/to
	Feb 24 05:31:15 macm sudo[7270]: pam_unix(sudo:session): session opened for user root by (uid=0)
	Feb 24 05:31:15 macm systemd[1]: Started Run WP-Scan.


### CoreOS Cloud-Config with Systemd-timers
The last thing to do is add that service to the **cloud-config** and re-apply the config. Here is the relevant section in the cloud config:

	coreos:
	  units:
	    - name: wpscan.service
	      content: |
			[Unit]
			Description=Run WP-Scan
	
			[Service]
			User=root
			Type=oneshot
			ExecStart=/opt/bin/wp-scan.sh
	    - name: wpscan.timer
	      command: start
	      content: |
			[Unit]
			Description=Run wp-scan weekly
	
			[Timer]
			OnCalendar=Sat *-*-* 03:00:00
			Persistent=true
	
			[Install]
			WantedBy=timers.target

As always confirm it's a valid config:

	macm ~ # coreos-cloudinit -validate --from-file cloud-config.yaml
	2017/02/24 05:35:03 Checking availability of "local-file"
	2017/02/24 05:35:03 Fetching user-data from datasource of type "local-file"

and then apply it

	macm ~ # coreos-cloudinit --from-file cloud-config.yaml

And you will see the relevant info:

	2017/02/24 05:35:41 Writing unit "wpscan.service" to filesystem
	2017/02/24 05:35:41 Writing file to "/etc/systemd/system/wpscan.service"
	2017/02/24 05:35:41 Wrote file to "/etc/systemd/system/wpscan.service"
	2017/02/24 05:35:41 Wrote unit "wpscan.service"
	2017/02/24 05:35:41 Writing unit "wpscan.timer" to filesystem
	2017/02/24 05:35:41 Writing file to "/etc/systemd/system/wpscan.timer"
	2017/02/24 05:35:41 Wrote file to "/etc/systemd/system/wpscan.timer"
	2017/02/24 05:35:41 Wrote unit "wpscan.timer"
	
And now you have setup a weekly job to scan your wordpress install and to send you an email. Not sure if this is best way to do it with CoreOS (I am pretty new to it), but this worked out okay for me.
