---
published: false
layout: post
title: "VMware Remote Console with Vsphere 6.0U2"
author: Karim Elatov
categories: []
tags: []
---

Or you can use the old VNC way:

http://www.virtuallyghetto.com/2012/01/using-vnc-client-to-connect-to-vms-in.html

Don't forget to update the firewall

https://platform9.com/support/enable-vnc-on-vmware-deployments/

ESXi Embedded Host Client is included with 6.0U2! A good excuse to upgrade, once the upgrade is done and the host rebooted, just point your browser to:
https://youresxihostnameorip/ui

and you can also download the client for mac:

https://my.vmware.com/web/vmware/details?downloadGroup=VMRC810&productId=491

After you install it, you can launch launch the remote console from the embedded ui for the VM

Just update using the following commands:

esxcli network firewall ruleset set -e true -r httpClient
esxcli software profile update -p ESXi-6.0.0-20160302001-standard -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml
This 3rd line below is optional, use it if you wish to return the firewall status to how it was before you began this procedure, paste:
esxcli network firewall ruleset set -e false -r httpClient
