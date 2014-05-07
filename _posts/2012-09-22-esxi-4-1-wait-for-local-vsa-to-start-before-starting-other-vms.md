---
title: ESXi 4.1 Wait for Local VSA to Start Before Starting Other VMs
author: Jarret Lavallee
layout: post
permalink: /2012/09/esxi-4-1-wait-for-local-vsa-to-start-before-starting-other-vms/
dsq_thread_id:
  - 1409347297
categories:
  - Home Lab
  - VMware
tags:
  - ash
  - auto-backup.sh
  - boot
  - command line
  - ESXi
  - rc.local
  - script
  - vim-cmd
  - VSA
---
I have an interesting siuation in my lab. I have a ESXi 4.1U2 host that uses PCI passthrough to a VSA to provide the storage for the host. The problem is when I reboot the host, the ESXi server does not see the storage and my VMs go invalid. I have set up the VSA to <a href="http://kb.vmware.com/kb/850" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/850']);" target="_blank">Auto Start</a> when the host is booted, but the host will perform a rescan before starting the VSA.

What I need the host to do is start the VSA and then rescan before starting the rest of the VMs. Unforunately this is not built into ESXi, and likely will not be. We can write a script to do this at boot. The rc.local is a script that is called. From the man page of rc.

> rc is the command script that is invoked by init(8) when the system  
> starts up. It performs system housekeeping chores and starts up system  
> daemons. Additionally, rc is intricately tied to the netstart(8) script,  
> which runs commands and daemons pertaining to the network. rc is also  
> used to execute any rc.d(8) scripts defined in rc.conf.local(8). The  
> rc.securelevel, rc.firsttime, and rc.local scripts hold commands which  
> are pertinent only to a specific site. 

The first thing I did was take a look at the /etc/rc.local on the host.

	  
	~ # cat /etc/rc.local
	
	# ! /bin/ash
	
	export PATH=/sbin:/bin
	
	log() {  
	echo &quot;$1&quot;  
	logger init &quot;$1&quot;  
	}
	
	# execute all service retgistered in /etc/rc.local.d
	
	if [ -d /etc/rc.local.d ]; then  
	for filename in `find /etc/rc.local.d/ | sort`  
	do  
	if [ -f $filename ] && [ -x $filename ]; then  
	log &quot;running $filename&quot;  
	$filename  
	fi  
	done  
	fi  
	

The rc.local on the host calls all of the scripts in /etc/rc.local.d. It would be great to just put a script in /etc/rc.local.d. The problem is that any file we add there will not be persistent. Check out <a href="http://www.virtuallyghetto.com/2011/08/how-to-persist-configuration-changes-in.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virtuallyghetto.com/2011/08/how-to-persist-configuration-changes-in.html']);" target="_blank">this blog post</a> on other ways to make the files persistent.

The easiest thing is to edit the /etc/rc.local and have it boot the VM and then run a rescan on the host. The first thing we should do is figure out the ID of the VM what we want to boot. The ID should not change, as it is stuck to this host, but it is a good idea to get this dynamically.

	
	
	# vim-cmd vmsvc/getallvms |grep vsa.vmx
	
	624 vsa  vsa/vsa.vmx solaris10_64Guest vmx-07  
	

Above we can see the ID is 624. Let&#8217;s write a command that will dynamically query the ID for us.

	  
	~ # /bin/vim-cmd vmsvc/getallvms |grep vsa.vmx |cut -d &quot; &quot; -f 1  
	624  
	

Since the rc.local will run before the VMs boot, we will want to power on the VM, then wait for the VM to boot, then rescan for datastores. The problem is that boot times can vary for different VMs, so I wrote a simple for loop to try 5 times to look for new LUNs. Each loop waits for 30 seconds, does a rescan, and checks for any naa or eui LUNs. If it finds any naa or eui LUNs, it will break the for loop.

Below is the simple script that can be appended to the /etc/rc.local.

	
	
	# Custom Boot VSA script
	
	# Dynamically get the ID of the VSA
	
	ID=`/bin/vim-cmd vmsvc/getallvms |grep vsa.vmx |cut -d &amp;quot; &amp;quot; -f 1`
	
	# Blindly start the VM
	
	/bin/vim-cmd vmsvc/power.on $ID
	
	# in the loop below we will do 5 iterations of 30 seconds with a rescan. breaking out of the loop if we see some luns.
	
	for i in 1 2 3 4 5  
	do  
	\# Let's sleep while we wait for the VM to come online. Say 30 Seconds.  
	sleep 30
	
	            # Rescan the hbas
	            /sbin/esxcfg-rescan -A
	            # Check to see if we have any LUNs other than the local ones.
	            numluns=`/sbin/esxcfg-mpath -L |egrep -c &amp;quot;naa|eui&amp;quot;`
	            if [ &amp;quot;$numluns&amp;quot; -gt &amp;quot;0&amp;quot; ]; then
	                break
	        fi
	    done
	    
	
	# Rescan for datastores
	
	/sbin/vmkfstools -V
	
	# Restart the services on the host
	
	/sbin/services.sh restart  
	

Now that we have modified the /etc/rc.local, we will see the .#rc.local file that will be backed up by the auto-backup.sh script.

	  
	~ # ls -la /etc/.&#35;rc.local  
	-r-xr-xr-t 1 root root 335 Oct 11 2011 /etc/.#rc.local  
	

Since the .# file is there, we know it will be backed up. Let&#8217;s force this to be backed up by running auto-backup.sh twice.

	  
	~ # /sbin/auto-backup.sh  
	boot type: visor-thin  
	local.tgz  
	etc/dropbear/dropbear\_dss\_host_key  
	etc/dropbear/dropbear\_rsa\_host_key  
	etc/opt/vmware/vpxa/vpxa.cfg  
	etc/security/access.conf  
	etc/vmware/hostd/authorization.xml  
	etc/vmware/hostd/hostsvc.xml  
	etc/vmware/hostd/pools.xml  
	etc/vmware/hostd/vmAutoStart.xml  
	etc/vmware/hostd/vmInventory.xml  
	etc/vmware/hostd/proxy.xml  
	etc/vmware/ssl/rui.crt  
	etc/vmware/ssl/rui.key  
	etc/vmware/vmkiscsid/initiatorname.iscsi  
	etc/vmware/vmkiscsid/vmkiscsid.db  
	etc/vmware/config  
	etc/vmware/dvsdata.db  
	etc/vmware/esx.conf  
	etc/vmware/license.cfg  
	etc/vmware/locker.conf  
	etc/vmware/snmp.xml  
	etc/vmware/settings  
	etc/vmware/vmware.lic  
	etc/group  
	etc/hosts  
	etc/inetd.conf  
	etc/chkconfig.db  
	etc/ntp.conf  
	etc/ntp.drift  
	etc/passwd  
	etc/random-seed  
	etc/resolv.conf  
	etc/syslog.conf  
	etc/dhclient-vmk0.leases  
	etc/shadow  
	etc/sfcb/repository/root/interop/cim_indicationfilter.idx  
	etc/sfcb/repository/root/interop/cim_indicationhandlercimxml.idx  
	etc/sfcb/repository/root/interop/cim_indicationsubscription.idx  
	etc/sfcb/repository/root/interop/cim_listenerdestinationcimxml.idx  
	etc/rc.local  
	

The last line shows the /etc/rc.local file. Before we reboot the host, we should test the script. Power down the VMs on the host and then run the script to confirm that it will do what we want.

	  
	~ # /etc/rc.local  
	

You will see it power on the VM, then wait for at least 30 seconds. After this you will see the rescan output and then the services restart. You may see it rescan multiple times. This is the script waiting for the VSA to come online.

Now go ahead and reboot the server and confrim that everything comes up correctly. In my case, the VSA comes online and then it waits long enough to have the LUNs presented before continuing to boot.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/esxi-4-1-wait-for-local-vsa-to-start-before-starting-other-vms/" title=" ESXi 4.1 Wait for Local VSA to Start Before Starting Other VMs" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:ash,auto-backup.sh,boot,command line,ESXi,rc.local,script,vim-cmd,VSA,blog;button:compact;">I have an interesting siuation in my lab. I have a ESXi 4.1U2 host that uses PCI passthrough to a VSA to provide the storage for the host. The problem...</a>
</p>