---
published: true
title: What is Seen in the Logs When Logging Into an ESX(i) Host
author: Karim Elatov
layout: post
permalink: /2012/04/what-is-seen-in-the-logs-when-logging-into-an-esxi-host/
categories: ['vmware']
tags: [ 'hostd_log', 'dcui', 'dropbear']
---

I was recently contacted by a company to determine if a certain user had accessed their ESX host. It was a secure environment so no logs were able to be shared. All they wanted to find out was how he logged in and at what time, the rest they could figure out. I decided to run through a couple of scenarios and send them a log snippet of what I saw.

# Logging in via SSH

When logging to an ESXi host directly via ssh you will see the following in /var/log/secure:


	Apr 16 20:28:23 esx_host sshd[20996]: Accepted password for root from 10.16.244.81 port 55941 ssh2
	Apr 16 20:28:23 esx_host sshd[20996]: pam_unix(system-auth-generic:session): session opened for user root by (uid=0)


If you have the wtmp file on your ESXi host, you can copy that file from the host to a Linux machine and run the following on it (because the `last` command does not exist on ESXi, but it does exist on ESX classic):


	# last -f /var/log/wtmp | head
	root pts/2 10.16.244.81 Mon Apr 16 20:28 - 20:31 (00:02)
	root pts/1 10.16.244.81 Mon Apr 16 20:27 still logged in
	root pts/1 10.16.185.12 Fri Apr 13 18:00 - 18:04 (00:03)
	root pts/1 10.16.185.12 Fri Apr 13 11:58 - 14:12 (02:14)


You will notice that it will list the IP and the duration of the login.

When logging into an ESXi host via ssh, you will see the following under /var/log/messages


	Apr 22 13:27:27 dropbear[7302]: Child connection from 10.0.1.1:53262
	Apr 22 13:27:30 dropbear[7302]: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 22 13:27:30 dropbear[7302]: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")
	Apr 22 13:27:30 shell[7721]: Interactive shell session started


If you have physical access to an ESXi host and you log in directly via the console (ALT-F1), you will see the following:


	Apr 22 08:49:37 localhost login: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 22 08:49:37 localhost login: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")
	Apr 22 08:49:39 localhost login: pam_unix(system-auth-generic:session): session opened for user root by LOGIN(uid=0)
	Apr 22 08:49:39 localhost login: ROOT LOGIN ON tty1


And if you have access to the /var/log/wtmp file you can again copy it to a Linux machine and run the following:


	# last -f /var/log/wtmp | head
	root tty1 Sun Apr 22 08:49 still logged in
	root tty1 Sun Apr 22 08:48 - 08:49 (00:00)
	root pts/0 10.0.1.1 Sun Apr 22 08:48 still logged in


Notice it shows tty1 instead of pts/0 (compared to when you logged in via SSH). From the man page of [console(4)](http://linux.die.net/man/4/console).

> A Linux system has up to 63 virtual consoles (character devices with major number 4 and minor number 1 to 63), usually called /dev/ttyn with 1 ..
> ..
> Common ways to switch consoles are: (a) use Alt+Fn or Ctrl+Alt+Fn to switch to console n; AltGr+Fn might bring you to console n+12 ;

So when you are physically in front of a Linux machine, you get a virtual console and you can switch between them by clicking ALT-F#. Depending on which # you select that will be your virtual console # (ie tty1, tty2.,etc...). Now from the man page of [pts(4)](http://linux.die.net/man/4/pts):

> The file /dev/ptmx is a character file with major number 5 and minor number 2, usually of mode 0666 and owner.group of root.root. It is used to create a pseudoterminal master and slave pair.
> When a process opens /dev/ptmx, it gets a file descriptor for a pseudoterminal master (PTM), and a pseudoterminal slave (PTS) device is created in the /dev/pts directory.
> ..
> ..
> In practice, pseudoterminals are used for implementing terminal emulators such as xterm(1), in which data read from the pseudoterminal master is interpreted by the application in the same way a real terminal would interpret the data, and for implementing remote-login programs such as sshd(8), in which data read from the pseudoterminal master is sent across the network to a client program that is connected to a terminal or terminal emulator.

So if you login to a Linux machine via SSH you get a pseudoterminal and it get incremented with the number of logins (ie first login will be on /dev/pts/0, second login will be on /dev/pts/1, and so on). So from the same output as before:


	# last -f /var/log/wtmp | head
	root     tty1                          Sun Apr 22 08:49   still logged in
	root     tty1                          Sun Apr 22 08:48 - 08:49  (00:00)
	root     pts/0        10.0.1.1         Sun Apr 22 08:48   still logged in


We can see that someone had physical access to the ESX host and he clicked "ALT-F1" (ended up utilizing the virtual terminal tty1) and logged in, one minute later logged off. He then loggged back in and is still logged in. We also see that one machine with IP 10.0.1.1 logged via ssh (ended up using a pseudoterminal pts/0) and is also still logged in.

# Logging in via DCUI

If you have physical access to an ESXi host and you connect directly to the DCUI (Direct Console User Interface), you will see the following under /var/log/messages:


	Apr 22 13:32:21 DCUI: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 22 13:32:21 DCUI: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")
	Apr 22 13:32:21 DCUI: pam_unix(system-auth-generic:auth): authentication failure; logname= uid=0 euid=0 tty= ruser= rhost= user=root
	Apr 22 13:32:26 DCUI: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 22 13:32:26 DCUI: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")
	Apr 22 13:32:26 DCUI: authentication of user root succeeded


From the DCUI, you can enable Tech Support Mode (TSM) and then login to get an interactive shell by clicking ALT-F1. More information regarding TSM and how to enable it, can be found in VMware KB [1017910](https://knowledge.broadcom.com/external/article?legacyId=1017910). If you do that then you will see the following logs in your /var/log/messages file:


	Apr 22 13:36:06 root: TSM Displaying TSM login: runlevel =
	Apr 22 13:36:06 init: init: process '/sbin/initterm.sh TTY1 /sbin/techsupport.sh ++min=0,swap' (pid 13818) exited. Scheduling it for restart.
	Apr 22 13:36:06 init: init: starting pid 13868, tty '/dev/tty1': '/bin/sh'
	Apr 22 13:36:06 root: techsupport VMware Tech Support Mode available
	Apr 22 13:36:15 login[13876]: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 22 13:36:15 login[13876]: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")
	Apr 22 13:36:17 login[13876]: pam_unix(system-auth-generic:session): session opened for user root by (uid=0)
	Apr 22 13:36:17 login[13876]: pam_env(system-auth-generic:setcred): Unable to open config file: /etc/security/pam_env.conf: No such file or directory
	Apr 22 13:36:17 login[13876]: root login on 'UNKNOWN'
	Apr 22 13:36:17 shell[13876]: Interactive shell session started


# Logging in via vSphere Client (to ESX host)

Now if you login to the ESX or ESXi host via the vsphere client, you will see the following in your /var/log/vmware/hostd.log:


	[2012-04-16 20:35:04.594 F6417B90 info 'Vimsvc'] [Auth]: User root
	[2012-04-16 20:35:04.594 F6417B90 info 'ha-eventmgr'] Event 35 : User root 10.131.3.116 logged in


You will also see the following in /var/log/messages:


	Apr 16 20:35:04 esx_host /usr/lib/vmware/bin/vmware-hostd[23877]: Accepted password for user root from 10.131.3.116


and finally you will see the following in /var/log/secure (only under ESX and not on ESXi):


	Apr 16 20:35:04 esx_host /usr/lib/vmware/bin/vmware-hostd[23877]: pam_per_user: create_subrequest_handle(): doing map lookup for user "root"
	Apr 16 20:35:04 esx_host /usr/lib/vmware/bin/vmware-hostd[23877]: pam_per_user: create_subrequest_handle(): creating new subrequest (user="root", service="system-auth-generic")


# Logging in via vSphere Client (to vCenter)

If you connect to the vCenter using the vSphere client, you will only see the login attempt on the vCenter it self and not on the ESX(i) host. That will be under C:\Documents and Settings\AllUsers\Application Data\VMware\VMware VirtualCenter\Logs\vpxd.log. You will see the following in the logs:


	[2012-04-16 21:42:11.096 02584 info 'App'] [VpxLRO] -- BEGIN task-internal-1788204 -- -- vim.SessionManager.loginBySSPI -- 0CCF336E-E963-44C9-8AF6-90D4B10EFE74
	[2012-04-16 21:42:11.096 02584 info 'App'] [Auth]: User NETLAB\kelatov
	[2012-04-16 21:42:11.111 02584 info 'App'] [VpxLRO] -- FINISH task-internal-1788204 -- -- vim.SessionManager.loginBySSPI -- 0CCF336E-E963-44C9-8AF6-90D4B10EFE74


**Note:** Log location depends on your Windows version, please consult VMware KB [1021804](https://knowledge.broadcom.com/external/article?legacyId=1021804) to make sure you are looking at the correct location.

### Related Posts

- [ESX(i) Host  Randomly Disconnects from vCenter Server due to Hostd Backtracing](/2012/10/esxi-host-randomly-disconnects-from-vcenter-server-due-to-hostd-back-tracing/)

