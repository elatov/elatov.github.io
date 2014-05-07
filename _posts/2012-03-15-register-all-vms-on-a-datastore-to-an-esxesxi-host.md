---
title: Register All VMs on a Datastore to an ESX/ESXi host
author: Jarret Lavallee
layout: post
permalink: /2012/03/register-all-vms-on-a-datastore-to-an-esxesxi-host/
dsq_thread_id:
  - 1411095852
categories:
  - VMware
  - vTip
tags:
  - cli
  - register vm
  - vtip
---
### ESXi

Register all VMs on a single datastore.

	~ # find /vmfs/volumes/&lt;datastorename&gt;/ -maxdepth 2 -name '*.vmx' -exec vim-cmd solo/registervm "{}" \;
		
Register all VMs on all datastores.
		
	~ # find /vmfs/volumes/ -maxdepth 3 -name '*.vmx' -exec vim-cmd solo/registervm "{}" \;
	
### ESX
	
Register all VMs on a single datastore.
	
	~ # find /vmfs/volumes/&lt;datastorename&gt;/ -maxdepth 2 -name '*.vmx' -exec vmware-cmd -s register "{}" \;
		
Register all VMs on all datastores.
		
	~ # find /vmfs/volumes/ -maxdepth 3 -name '*.vmx' -exec vmware-cmd -s register "{}" \;
