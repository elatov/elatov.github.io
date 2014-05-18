---
title: 'ESXi Host Receives "Warning: Host is running in audit mode. Your configuration will not be persistent across reboots" Error Message'
author: Karim Elatov
layout: post
permalink: /2012/10/esx-host-receives-warning-host-is-running-in-audit-mode-your-configuration-will-not-be-persistent-across-reboots-error-message/
dsq_thread_id:
  - 1409146534
categories:
  - VMware
tags:
  - /bootbank/boot.cfg
  - ESX Audit Mode
  - kernelopt=auditMode=TRUE
---
Recently saw the message outlined in the title from an ESXi host. Logged into the host via ssh and checked out the logs. Here is what I saw:


	/var/log # grep -i audit messages
	Sep 26 18:22:28 vmkernel: TSC: 1899066536 cpu0:0)BootConfig: 110: auditMode = TRUE


It looks like AuditMode was set to true. Checking out the 'boot.cfg' file, I saw the following:


	~ # cat /bootbank/boot.cfg
	kernel=b.z
	kernelopt=auditMode=TRUE
	modules=k.z --- s.z --- c.z --- oem.tgz --- license.tgz --- m.z
	build=4.1.0-800380
	updated=1
	bootstate=0


For some reason this line got in there:


	kernelopt=auditMode=TRUE


After some research found VMware Communities [160722](http://communities.vmware.com/thread/160722) page. They mentioned that the fix is to remove that line. Here are the instructions from that page:

> 1.  enable console support option
>     1.  F2 -> Troubleshoot options -> enable local TSM support
> 2.  ALT+F1 log into console
> 3.  vi /bootbank/boot.cfg
>     1.  press i (for insert)
>     2.  remove the line that has auditMode=TRUE
>     3.  press 'esc' then :w :q (to write changes and quit vi)
> 4.  reboot server to take it out of audit mode

Remove that line per the instructions above and the server rebooted without going into Audit Mode again.

