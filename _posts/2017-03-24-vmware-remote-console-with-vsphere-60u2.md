---
published: false
layout: post
title: "VMware Remote Console with vSphere 6.0U2"
author: Karim Elatov
categories: [vmware]
tags: [vmrc,vnc]
---
### Updating to vSphere 6.0U2

I heard that with the 6.0U2 now the new Web Client (VMware Host Client VS. vSphere Web Client) is available on the ESXi host, not just in vCenter. From the Release Notes, under the **What's New** section:

> VMware Host Client: The VMware Host Client is an HTML5 client that is used to connect to and manage single ESXi hosts. It can be used to perform administrative tasks to manage host resources, such as virtual machines, networking, and storage. The VMware Host Client can also be helpful to troubleshoot individual virtual machines or hosts when vCenter Server and the vSphere Web Client are unavailable.

I thought that was pretty cool, so I decided to give it a try. We can run the following command on the ESXi host to update to 6.0U2:

	esxcli network firewall ruleset set -e true -r httpClient
	esxcli software profile update -p ESXi-6.0.0-20160302001-standard -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml
	esxcli network firewall ruleset set -e false -r httpClient

After you reboot you can check out the new **vib** installed on the system:

	[root@macm:~] esxcli software vib list | grep ui
	esx-ui                              1.0.0-3617585                         VMware           VMwareCertified     2016-08-14

### Using the VMware Remote Console
Now if you go the VMware Host Client (**https://ESXI_IP/ui**), you will see the new client:

![esxi-web-client](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/esxi-web-client.png&raw=1)

And if you login you can open a console to any of the VMs:

![vm-console-opts](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/vm-console-opts.png&raw=1)

And if you open it in the browser you can get a console to the VM and see the VM's display:

![web-console-vm](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/web-console-vm.png&raw=1)

If you want you can also download the stand-alone VMRC. Check out more details at [this](https://kb.vmware.com/kb/2091284) KB. Basically you download the client, and from the Web UI you choose **Launch Remote Console** and if VMRC is installed it will launch automatically, here is how it looked like on my Mac:

![vmrc-launched](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/vmrc-launched.png&raw=1)

And you will see it running on your dock:

![vmrc-on-dock](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/vmrc-on-dock.png&raw=1)

You can check out different settings of the VM in the VMRC as well:

![rd-vmrc-set](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/rd-vmrc-set.png&raw=1)

### Enabling VNC for a VM

Or you can use the old VNC way. I found some old links that talk about the process:

* [Using a VNC Client to Connect to VMs in ESXi 5](http://www.virtuallyghetto.com/2012/01/using-vnc-client-to-connect-to-vms-in.html)
* [Enable VNC on VMware Deployments](https://platform9.com/support/enable-vnc-on-vmware-deployments/)
* [Enabling VNC Access to vSphere 5 VM Guest Consoles](https://www.netiq.com/documentation/cloudmanager22/ncm22_reference/data/bxzaz5n.html)

#### Allow VNC Traffic in the ESXi Firewall
The links from above talks about the process, you can either create a special firewall file on each boot. So edit the following file: **/etc/rc.local.d/local.sh** and add the following to it:

	cat <<EOF > /etc/vmware/firewall/vncServer.xml
	<ConfigRoot>
	  <service>
	    <id>vncServer</id>
	    <rule id='0000'>
	      <direction>inbound</direction>
	      <protocol>tcp</protocol>
	      <porttype>dst</porttype>
	      <port>
	        <begin>5900</begin>
	        <end>5999</end>
	      </port>
	    </rule>
	    <enabled>true</enabled>
	    <required>false</required>
	  </service>
	</ConfigRoot>
	EOF
	esxcli network firewall refresh

And then save the config to have it survive reboots:

	/sbin/auto-backup.sh

Or if you want you can just use the existing Service of **GDB Server**, that will enable more ports than necessary but it will get the job done:

![firewall-opened](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/firewall-opened.png&raw=1)

Or run the following on the command line:

    [root@hp:~] esxcli network firewall ruleset rule list -r gdbserver
    Ruleset    Direction  Protocol  Port Type  Port Begin  Port End
    ---------  ---------  --------  ---------  ----------  --------
    gdbserver  Inbound    TCP       Dst              1000      9999
    gdbserver  Inbound    TCP       Dst             50000     50999
    [root@hp:~] esxcli network firewall ruleset set -e true -r gdbserver
    [root@hp:~] esxcli network firewall ruleset list -r gdbserver
    Name       Enabled
    ---------  -------
    gdbserver     true
    [root@hp:~] esxcli network firewall refresh


#### Enable VNC Access on VM
Now that the firewall is open, we can shutdown the VM and we have to add the following to VMX file:

	RemoteDisplay.vnc.enabled = [true|false]
	RemoteDisplay.vnc.port = [port #]
	RemoteDisplay.vnc.password = [optional]

You can either do this via SSH or just **edit settings** on the VM in the new web client and under the **advanced** section add them there:

![vm-options-added](https://seacloud.cc/d/480b5e8fcd/files/?p=/new-vmrc/vm-options-added.png&raw=1)

Then you can use **vncviewer** (tigervnc) to connect to the VM. On my Mac I can the following:

	$ sudo port install tigervnc
	$ /opt/local/bin/vncviewer ESXI_IP:5902

The VMware Remote Console is the preffered method and is more secure.
