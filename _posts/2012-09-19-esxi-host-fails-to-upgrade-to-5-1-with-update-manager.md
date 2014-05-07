---
title: ESXi host fails to upgrade to 5.1 with Update Manager
author: Jarret Lavallee
layout: post
permalink: /2012/09/esxi-host-fails-to-upgrade-to-5-1-with-update-manager/
dsq_thread_id:
  - 1404672871
categories:
  - Home Lab
  - VMware
tags:
  - .fseventsd
  - .Spotlight-V100
  - 5.1
  - altbootbank
  - bootbank
  - dpm
  - OSX
  - upgrade
  - VUM
---
Today I was running through some upgrades in my lab to ESXi 5.1 with update manager. One small issue was that after adding a base line to the host and hitting remediate, the host upgrade would fail with the following message.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi5.1-upgrade-fails.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi5.1-upgrade-fails.png']);"><img class="aligncenter size-full wp-image-3534" title="esxi5.1 upgrade fails" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi5.1-upgrade-fails.png" alt="esxi5.1 upgrade fails ESXi host fails to upgrade to 5.1 with Update Manager" width="651" height="56" /></a>

The error message &#8220;The operation is not supported on the selected inventory objects. Check the events for the objects selected for the operation.&#8221; can mean different things. One of them is because the <a href="http://kb.vmware.com/kb/1024331" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1024331']);" target="_blank">admission control is preventing the host from entering maintenance mode</a>.

Looking at the events tab I saw that DPM was causing the operation to fail.  
<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-DPM.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-DPM.png']);"><img class="aligncenter size-full wp-image-3535" title="esx5.1 upgrade DPM" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-DPM.png" alt="esx5.1 upgrade DPM ESXi host fails to upgrade to 5.1 with Update Manager" width="748" height="50" /></a>

To fix this I could disable DPM in the cluster manually, but VUM gives me the option to temporarily disable it while it does the remediation. During the remediation wizard, I had to check the option below.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-disable-dpm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-disable-dpm.png']);"><img class="aligncenter size-full wp-image-3536" title="esx5.1 upgrade disable dpm" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-disable-dpm.png" alt="esx5.1 upgrade disable dpm ESXi host fails to upgrade to 5.1 with Update Manager" width="473" height="38" /></a>

After I did this, I was able to start the upgrade, but it failed with &#8220;Software of system configuration of host esx4.moopless.com is incompatible. Check the scan results for details&#8221;. This is because the host has not been rebooted after the vCenter was upgraded. When the vCenter was upgraded, new host agents would have been installed when the hosts were reconnected. These agents require a reboot before any other patches can be applied to the host.

So I rebooted the host and kicked off another remediation that failed saying that it could not run the update script on the host.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-run-script.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-run-script.png']);"><img class="aligncenter size-full wp-image-3540" title="esx5.1 upgrade run script" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/esx5.1-upgrade-run-script.png" alt="esx5.1 upgrade run script ESXi host fails to upgrade to 5.1 with Update Manager" width="872" height="17" /></a>

So I went searching for the logs. In the vmware-vum-server-log4cpp.log on the <a href="http://kb.vmware.com/kb/1003693" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1003693']);" target="_blank">VUM server</a> and found the following.

	  
	\[2012-09-10 15:14:46:519 'NfcClientWrapper' 2840 INFO\] \[nfcClientWrapper, 155\] Copying file: local = C:/WINDOWS/TEMP/upgradekejxxzsf.tmp/metadata.zip, remote = /tmp/vuaScript-oDoyLu/metadata.zip  
	\[2012-09-10 15:14:46:519 'NfcClientWrapper' 2840 INFO\] \[nfcClientWrapper, 155\] Copying file: local = C:/WINDOWS/TEMP/upgradekejxxzsf.tmp/precheck.py, remote = /tmp/vuaScript-oDoyLu/precheck.py  
	\[2012-09-10 15:14:46:660 'NfcClientWrapper' 2840 INFO\] \[nfcClientWrapper, 155\] Copying file: local = C:/WINDOWS/TEMP/upgradekejxxzsf.tmp/esximage.zip, remote = /tmp/vuaScript-oDoyLu/esximage.zip  
	\[2012-09-10 15:14:53:706 'HU-Upgrader' 2840 ERROR\] \[upgraderImpl, 421\] Script execution failed on host: 192.168.5.33)  
	

The logs above are not very informative, so I went to the host to see why it failed copying the &#8216;esximage.zip&#8217; over to the host. In the vpxa.log I found the following.

	  
	2012-09-11T05:02:32.447Z \[FFCF5B90 verbose 'Default' opID=task-internal-233-fb0a87f0\] \[VpxaDatastoreContext\] No conversion for localpath /tmp/vuaScript-oDoyLu/esximage.zip  
	2012-09-11T05:02:33.337Z \[FFCF5B90 warning 'Libs' opID=task-internal-233-fb0a87f0\] \[NFC ERROR\] NfcFile_ContinueReceive: reached EOF  
	

It looks like it was failing to copy over the files to the bootbanks. I kicked off another remediation and took a look at the system while it was upgrading. The host creates a new ramdisk to stage the changes. It is called the &#8216;upgradescratch&#8217;.

	  
	\# vdu -h |tail -n 1  
	ramdisk upgradescratch: 300M ( 103 inodes)  
	

I ran a df to see how much space was used in the ram disk.

	  
	\# df -h  
	Filesystem Size Used Available Use% Mounted on  
	...  
	vfat 285.9M 37.8M 248.1M 13% /vmfs/volumes/c968084a-b7429e1a-770c-aa784ee74000  
	

So we know that it was copying over the files. I ran it again and found that it was indeed increasing the used space.

	  
	\# df -h  
	Filesystem Size Used Available Use% Mounted on  
	...  
	vfat 285.9M 240.0M 45.8M 84% /vmfs/volumes/c968084a-b7429e1a-770c-aa784ee74000  
	

Since update manager was copying over the files and it was failing when trying to run the script, I went ahead and took a look at the bootbanks. There are 2 bootbanks in ESXi; /bootbank and /altbootbank. <a href="http://www.vmware.com/files/pdf/ESXi_architecture.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/ESXi_architecture.pdf']);" target="_blank">This document</a> describes boot banks as the following.

> The ESXi system has two independent banks of memory, each  
> of which stores a full system image, as a fail-safe for applying  
> updates. When you upgrade the system, the new version is  
> loaded into the inactive bank of memory, and the system is  
> set to use the updated bank when it reboots. If any problem  
> is detected during the boot process, the system automatically  
> boots from the previously used bank of memory. You can also  
> intervene manually at boot time to choose which image to use  
> for that boot, so you can back out of an update if necessary

In the /bootbank I did an ls -la and found the following files.

	  
	\# ls -la |head -n 5  
	drwxr-xr-x 1 root root 512 Sep 18 05:33 ..  
	drwxr-xr-x 1 root root 8 Jan 1 1970 .Spotlight-V100  
	drwxr-xr-x 1 root root 8 Jan 1 1970 .Trashes  
	-rwx\---\--- 1 root root 4096 Aug 22 21:33 ._.Trashes  
	drwxr-xr-x 1 root root 8 Jan 1 1970 .fseventsd  
	

From this <a href="http://coolestguyplanettech.com/downtown/spotlight-out-control-mac-os-x-lion-107" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://coolestguyplanettech.com/downtown/spotlight-out-control-mac-os-x-lion-107']);" target="_blank" class="broken_link">blog post</a>, you can see that I once <a href="http://www.ghacks.net/2009/08/19/spotlight-v100-and-trashes-folders-on-usb-flash-drives/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ghacks.net/2009/08/19/spotlight-v100-and-trashes-folders-on-usb-flash-drives/']);" target="_blank">attached this usb boot drive to my Mac</a> and the Mac added the .Spotlight-V100, .Trashes, ._.Trashes, and .fseventsd files when it mounted the volume. The truth is that I used OSX to <a href="http://vmwire.com/2011/09/11/creating-vsphere-5-esxi-embedded-usb-stick/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmwire.com/2011/09/11/creating-vsphere-5-esxi-embedded-usb-stick/']);" target="_blank">dd install</a> ESXi 5.0. Once the DD had finished it auto mounted the partitions.

Since these files will never be used in ESXi, I decided to remove them.

	  
	\# rm -rf .fseventsd/ ._.Trashes .Trashes/ .Spotlight-V100/  
	

Since any filesystem that was mounted by OSX would contain these, I decided to clean up the /altbootbank as well. Here are the files in the /altbootbank.

	  
	\# ls -la  
	drwxr-xr-x 1 root root 512 Sep 18 05:36 ..  
	drwxr-xr-x 1 root root 8 Jan 1 1970 .Spotlight-V100  
	drwxr-xr-x 1 root root 8 Jan 1 1970 .fseventsd  
	-rwx\---\--- 1 root root 96 Jun 29 13:49 boot.cfg  
	-rwx\---\--- 1 root root 197 Aug 23 11:53 imgdb.tgz  
	-rwx\---\--- 1 root root 20 Sep 14 08:50 useropts.gz  
	

I removed the .Spotlight-V100 and .fseventsd from the altbootbank

	  
	\# rm -rf .Spotlight-V100/ .fseventsd/  
	

I did another remediation of the upgrade and it went through just fine. So these OSX specific files were disrupting the upgrade.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/esxi-host-fails-to-upgrade-to-5-1-with-update-manager/" title=" ESXi host fails to upgrade to 5.1 with Update Manager" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:.fseventsd,.Spotlight-V100,5.1,altbootbank,bootbank,dpm,OSX,upgrade,VUM,blog;button:compact;">Today I was running through some upgrades in my lab to ESXi 5.1 with update manager. One small issue was that after adding a base line to the host and...</a>
</p>