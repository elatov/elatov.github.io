---
published: true
layout: post
title: "Run Script Before Shutdown with VMware Tools"
author: Karim Elatov
categories: [vmware,os]
tags: [vim-cmd,vmware-tools]
---
As a continuation of my efforts from my [previous post](/2017/11/running-a-windows-vm-in-virtualbox-in-a-vmware-gentoo-vm/) about VirtualBox with VMware, I wanted the VM to be part of auto power on and off process. After I enabled the setting on the VM ([Automating the process of starting and stopping virtual machines on VMware ESX\ESXi (850)](https://kb.vmware.com/kb/850), I realized **vmware-tools** would just send a guest shutdown command to the VM and the Gentoo would just shutdown the OS without gracefully shutting down any VMs running in VirtualBox. So I decided to fix that.

### Run Command on Poweroff with VMware Tools

I ran into [Execute Commands During Power Off or Reset of a Virtual Machine](https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vmtools.install.doc%2FGUID-24F145A4-383F-47B7-8ED5-079F469CA755.html) and [Use Custom VMware Tools Scripts](https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vmtools.install.doc%2FGUID-35F34AE7-78E0-4BCF-B7C4-EFC29DE18824.html), these two sites helped me to get started.

#### PowerOff Scipts
First find out what script is executed on poweroff:

	<> sudo vmware-toolbox-cmd script shutdown current
	/etc/vmware-tools/poweroff-vm-default

Then if you check out that file you will see the following:


	# Handy reference/shorthand used in this doc/scripts:
	#    TOOLS_CONFDIR ::= Depends on platform and installation settings.  Likely
	#                      "/etc/vmware-tools" or
	#                      "/Library/Application Support/VMware Tools"
	#    powerOp       ::= One of "poweron-vm", "poweroff-vm", "suspend-vm", and
	#                      "resume-vm".
	#    vmwScriptDir  ::= $TOOLS_CONFDIR/scripts/vmware
	#    userScriptDir ::= $TOOLS_CONFDIR/scripts/${powerOp}-default.d
	#
	# End users may install scripts of their own under $userScriptDir.  They
	# are executed in alphabetical order with "$powerOp" as the only argument.

It looks like we can create a user script directory which gets executed on certain power operations, so I created the following:

	<> ls /etc/vmware-tools/scripts/poweroff-vm-default.d/vbox-shutdown.sh
	/etc/vmware-tools/scripts/poweroff-vm-default.d/vbox-shutdown.sh

And that script just powered off my VirtualBox VM gracefully. I got the inspiration for the script from [Bash script to wait for Virtualbox VM shutdown?](https://superuser.com/questions/547980/bash-script-to-wait-for-virtualbox-vm-shutdown):

	<> cat /etc/vmware-tools/scripts/poweroff-vm-default.d/vbox-shutdown.sh
	#!/bin/bash
	# Global Variables
	VBOXMANAGE=/opt/bin/VBoxManage
	SU=/bin/su
	SUUSER="elatov"
	VM="win10"
	
	# shutdown VM
	${SU} ${SUUSER} -c "${VBOXMANAGE} controlvm  ${VM} acpipowerbutton"
	
	# Wait till the VM is fully off
	echo "Waiting for machine ${VM} to poweroff..."
	
	until $(${SU} ${SUUSER} -c "${VBOXMANAGE} showvminfo --machinereadable ${VM}" | grep -q ^VMState=.poweroff.)
	do
	  sleep 1
	done

#### VMware Tools Logging
Another thing to do is to enable **vmware-tools** logging so you can confirm **vmware-tools** is running the scripts (I found the settings in [Enabling debug logging for VMware Tools within a guest operating system (1007873)](https://kb.vmware.com/kb/1007873):

	<> cat /etc/vmware-tools/tools.conf
	[logging]
	log = true

#### Sending a Guest Shutdown Command from an ESXi Host
Next we can login to the ESXi host and first let's find our VM:

	[root@hp:~] vim-cmd vmsvc/getallvms | grep gen
	7      gen                    [datastore1] gen/gen.vmx                                     otherLinux64Guest   vmx-13

Looks like VM with ID **7** is our guy. And now let's send a guest shutdown to the VM using **vmware-tools**:

	[root@hp:~] vim-cmd vmsvc/power.shutdown 7

On the VM, I saw the following:

	<> tail -f /var/log/vmware-vmsvc.log
	[Oct 11 15:16:55.907] [ message] [vmsvc] Core dump limit set to -1
	[Oct 11 15:16:55.907] [ message] [vmtoolsd] Tools Version: 10.1.10.63510 (build-6082533)
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'hgfsServer' initialized.
	[Oct 11 15:16:55.918] [ message] [vix] QueryVGAuthConfig: vgauth usage is: 1
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'vix' initialized.
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'guestInfo' initialized.
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'powerops' initialized.
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'timeSync' initialized.
	[Oct 11 15:16:55.918] [ message] [vmtoolsd] Plugin 'vmbackup' initialized.
	[Oct 11 15:16:55.922] [ message] [vix] VixTools_ProcessVixCommand: command 62
	[Oct 11 15:25:42.084] [ message] [powerops] Executing script: '/etc/vmware-tools/poweroff-vm-default'
	[Oct 11 15:25:45.558] [ message] [powerops] Script exit code: 0, success = 1
	[Oct 11 15:25:45.558] [ message] [powerops] Initiating halt.
	
	Broadcast message from root@gen (Wed Oct 11 15:25:45 2017):
	
	The system is going down for system halt NOW!

I also had a remote desktop session connected to the Windows 10 VM to confirm the shutdown is graceful. You can confirm it's off by running the following:

	[root@hp:~] vim-cmd vmsvc/power.getstate 7
	Retrieved runtime info
	Powered off

and then you can also power the VM back on (after you have confirmed the shutdown was graceful):

	[root@hp:~] vim-cmd vmsvc/power.on 7
	Powering on VM:



