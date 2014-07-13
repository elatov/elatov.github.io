---
title: VCAP5-DCA Objective 7.2 – Configure and Maintain the ESXi Firewall
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-7-2-configure-and-maintain-the-esxi-firewall/
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['esx_firewall']
---

### Identify esxcli firewall configuration commands

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Firewall Configuration Using the ESXi Shell**
> The vSphere Client graphical user interface provides the preferred means of performing many configuration tasks. However, you can use the ESXi Shell to configure ESXi at the command line if necessary.
>
> ![esxcli firewall commands VCAP5 DCA Objective 7.2 – Configure and Maintain the ESXi Firewall ](https://github.com/elatov/uploads/raw/master/2012/12/esxcli_firewall_commands.png)

### Explain the three firewall security levels

This comes from the old "[ESX Configuration Guide ESX 4.1](http://www.vmware.com/pdf/vsphere4/r41/vsp_41_esx_server_config.pdf)":

![firewall security levels VCAP5 DCA Objective 7.2 – Configure and Maintain the ESXi Firewall ](https://github.com/elatov/uploads/raw/master/2012/12/firewall_security_levels.png)

You can check the default action like so:


	~ # esxcli network firewall get
	Default Action: DROP
	Enabled: true
	Loaded: true


So if the default Action is "DROP" then we are at high. If the the default action is "PASS" then we are at low. If we have an nfs mount point, this opens up all outgoing ports, then we are at medium. From the security guide:

> **NOTE** The behavior of the NFS Client rule set (nfsClient) is different from other rule sets. When the NFS Client rule set is enabled, all outbound TCP ports are open for the destination hosts in the list of allowed IP addresses

### Enable/Disable pre-configured services

From "[vSphere Command-Line Interface Concepts and Examples ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf)":

> **Using esxcli network firewall for ESXi Firewall Management**
> To minimize the risk of an attack through the management interface, ESXi includes a firewall between the management interface and the network. To ensure the integrity of the host, only a small number of firewall ports are open by default. The vSphere Security documentation explains how to set up firewalls for your environment and which ports you might have to temporarily enable for certain traffic.
>
> You manage firewalls by setting up firewall rulesets. vSphere Security documentation explains how to perform these tasks with the vSphere Client. You can also use esxcli network firewall to manage firewall rulesets and to retrieve information about them.
>
> **To limit shell access**
>
> 1. Check firewall status and sshServer ruleset status.
>
>         esxcli <conn_options> network firewall get
>         Default Action: DROP
>         Enabled: true
>         Loaded: true
>
>     and
>
>         esxcli network firewall ruleset list --ruleset-id sshServer
>         Name Enabled
>         --------- -------
>         sshServer true
>
> 2. Enable the sshServer ruleset if it is disabled.
>
>         esxcli network firewall ruleset set --ruleset-id sshServer --enabled true
>

To get a list of available services, you can do the following:


     ~ # esxcli network firewall ruleset list
     Name Enabled
     ------------------ -------
     sshServer true
     sshClient false
     nfsClient true
     dhcp true
     dns true
     snmp true
     ntpClient false
     CIMHttpServer true
     CIMHttpsServer true
     CIMSLP true
     iSCSI true
     vpxHeartbeats true
     updateManager false
     faultTolerance true
     webAccess true
     vMotion true
     vSphereClient true
     activeDirectoryAll false
     NFC true
     HBR true
     ftpClient false
     httpClient true
     gdbserver false
     DVFilter false
     DHCPv6 false
     DVSSync false
     syslog true
     IKED false
     WOL true
     vSPC true
     remoteSerialPort true
     netDump true
     fdm false

To enable or disable any of the above services you can do the following:


     ~ # esxcli network firewall ruleset set -r fdm -e true
     ~ # esxcli network firewall ruleset list -r fdm
     Name Enabled
     ---- -------
     fdm true
     ~ # esxcli network firewall ruleset set -r fdm -e false
     ~ # esxcli network firewall ruleset list -r fdm
     Name Enabled
     ---- -------
     fdm false

### Configure service behavior automation

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf)":

> **Automating Service Behavior Based on Firewall Settings**
> ESXi can automate whether services start based on the status of firewall ports.
>
> Automation helps ensure that services start if the environment is configured to enable their function. For example, starting a network service only if some ports are open can help avoid the situation where services are started, but are unable to complete the communications required to complete their intended purpose.
>
> In addition, having accurate information about the current time is a requirement for some protocols, such as Kerberos. The NTP service is a way of getting accurate time information, but this service only works when required ports are opened in the firewall. The service cannot achieve its goal if all ports are closed. The NTP services provide an option to configure the conditions when the service starts or stops. This configuration includes options that account for whether firewall ports are opened, and then start or stop the NTP service based on those conditions. Several possible configuration options exist, all of which are also applicable to the SSH server.
>
> *   **Start automatically if any ports are open, and stop when all ports are closed**: The default setting for these services that VMware recommends. If any port is open, the client attempts to contact the network resources pertinent to the service in question. If some ports are open, but the port for a particular service is closed, the attempt fails, but there is little drawback to such a case. If and when the applicable outgoing port is opened, the service begins completing its tasks.
> *   **Start and stop with host**: The service starts shortly after the host starts and closes shortly before the host shuts down. Much like Start automatically if any ports are open, and stop when all ports are closed, this option means that the service regularly attempts to complete its tasks, such as contacting the specified NTP server. If the port was closed but is subsequently opened, the client begins completing its tasks shortly thereafter.
> *   **Start and stop manually**: The host preserves the user-determined service settings, regardless of whether ports are open or not. When a user starts the NTP service, that service is kept running as long as the host is powered on. If the service is started and the host is powered off, the service is stopped as part of the shutdown process, but as soon as the host is powered on, the service is started again, preserving the user determined state.

Here is how to actually configure it:

> **Set Service or Client Startup Options**
> By default, daemon processes start when any of their ports are opened and stop when all of their ports are closed. You can change this startup policy for the selected service or client.
> **Procedure**
>
> 1.  Log in to a vCenter Server system using the vSphere Client.
> 2.  Select the host in the inventory panel.
> 3.  Click the Configuration tab and click Security Profile.
> 4.  In the Firewall section, click Properties.The Firewall Properties dialog box lists all the services and management agents you can configure for the host
> 5.  Select the service or management agent to configure and click Options.The Startup Policy dialog box determines when the service starts. This dialog box also provides information about the current state of the service and provides an interface for manually starting, stopping,or restarting the service.
> 6.  Select a policy from the Startup Policy list.
> 7.  Click OK

Here is how it looks like from vCenter:

![security profile view VCAP5 DCA Objective 7.2 – Configure and Maintain the ESXi Firewall ](https://github.com/elatov/uploads/raw/master/2012/12/security_profile_view.png)

![startup policy for service VCAP5 DCA Objective 7.2 – Configure and Maintain the ESXi Firewall ](https://github.com/elatov/uploads/raw/master/2012/12/startup_policy_for_service.png)

### Open/Close ports in the firewall

Every pre-defined service has associated ports with the service. Here is a list of all the services and their corresponding ports:

>
>	     ~ # esxcli network firewall ruleset rule list
>	     Ruleset Direction Protocol Port Type Port Begin Port End
>	     ------------------ --------- -------- --------- ---------- --------
>	     sshServer Inbound TCP Dst 22 22
>	     sshClient Outbound TCP Dst 22 22
>	     nfsClient Outbound TCP Dst 0 65535
>	     dhcp Inbound UDP Dst 68 68
>	     dhcp Outbound UDP Src 68 68
>	     dns Inbound UDP Dst 53 53
>	     dns Outbound UDP Dst 53 53
>	     dns Outbound TCP Dst 53 53
>	     snmp Inbound UDP Dst 161 161
>	     ntpClient Outbound UDP Dst 123 123
>	     CIMHttpServer Inbound TCP Dst 5988 5988
>	     CIMHttpsServer Inbound TCP Dst 5989 5989
>	     CIMSLP Inbound UDP Dst 427 427
>	     CIMSLP Outbound UDP Src 427 427
>	     CIMSLP Inbound TCP Dst 427 427
>	     CIMSLP Outbound TCP Src 427 427
>	     iSCSI Outbound TCP Dst 3260 3260
>	     vpxHeartbeats Outbound UDP Dst 902 902
>	     updateManager Outbound TCP Dst 80 80
>	     updateManager Outbound TCP Dst 9000 9100
>	     faultTolerance Outbound TCP Dst 80 80
>	     faultTolerance Inbound TCP Dst 8100 8100
>	     faultTolerance Outbound TCP Dst 8100 8100
>	     faultTolerance Inbound UDP Dst 8200 8200
>	     faultTolerance Outbound UDP Dst 8200 8200
>	     webAccess Inbound TCP Dst 80 80
>	     vMotion Inbound TCP Dst 8000 8000
>	     vMotion Outbound TCP Dst 8000 8000
>	     vSphereClient Inbound TCP Dst 902 902
>	     vSphereClient Inbound TCP Dst 443 443
>	     activeDirectoryAll Outbound UDP Dst 88 88
>	     activeDirectoryAll Outbound TCP Dst 88 88
>	     activeDirectoryAll Outbound UDP Dst 123 123
>	     activeDirectoryAll Outbound UDP Dst 137 137
>	     activeDirectoryAll Outbound TCP Dst 139 139
>	     activeDirectoryAll Outbound TCP Dst 389 389
>	     activeDirectoryAll Outbound UDP Dst 389 389
>	     activeDirectoryAll Outbound TCP Dst 445 445
>	     activeDirectoryAll Outbound UDP Dst 464 464
>	     activeDirectoryAll Outbound TCP Dst 464 464
>	     activeDirectoryAll Outbound TCP Dst 3268 3268
>	     activeDirectoryAll Outbound TCP Dst 51915 51915
>	     NFC Inbound TCP Dst 902 902
>	     NFC Outbound TCP Dst 902 902
>	     HBR Outbound TCP Dst 31031 31031
>	     HBR Outbound TCP Dst 44046 44046
>	     ftpClient Outbound TCP Dst 21 21
>	     ftpClient Inbound TCP Src 20 20
>	     httpClient Outbound TCP Dst 80 80
>	     httpClient Outbound TCP Dst 443 443
>	     gdbserver Inbound TCP Dst 1000 9999
>	     gdbserver Inbound TCP Dst 50000 50999
>	     DVFilter Inbound TCP Dst 2222 2222
>	     DHCPv6 Outbound TCP Dst 547 547
>	     DHCPv6 Inbound TCP Dst 546 546
>	     DHCPv6 Outbound UDP Dst 547 547
>	     DHCPv6 Inbound UDP Dst 546 546
>	     DVSSync Outbound UDP Dst 8302 8302
>	     DVSSync Inbound UDP Dst 8301 8301
>	     DVSSync Outbound UDP Dst 8301 8301
>	     DVSSync Inbound UDP Dst 8302 8302
>	     syslog Outbound UDP Dst 514 514
>	     syslog Outbound TCP Dst 514 514
>	     syslog Outbound TCP Dst 1514 1514
>	     IKED Outbound UDP Dst 500 500
>	     IKED Inbound UDP Dst 500 500
>	     WOL Outbound UDP Dst 9 9
>	     vSPC Outbound TCP Dst 0 65535
>	     remoteSerialPort Outbound TCP Dst 0 65535
>	     remoteSerialPort Inbound TCP Dst 23 23
>	     remoteSerialPort Inbound TCP Dst 1024 65535
>	     netDump Outbound UDP Dst 6500 6500
>	     fdm Inbound TCP Dst 8182 8182
>	     fdm Outbound TCP Dst 8182 8182
>	     fdm Inbound UDP Dst 8182 8182
>	     fdm Outbound UDP Dst 8182 8182
>
>

If you want to open up any of those port, just enable the service per the instructions laid out above.

### Create a custom service

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf)":

> **Rule Set Configuration Files**
> A rule set configuration file contains firewall rules and describes each rule's relationship with ports and protocols. The rule set configuration file can contain rule sets for multiple services.
>
> Rule set configuration files are located in the /etc/vmware/firewall/ directory. To add a service to the host security profile, VMware partners can create a VIB that contains the port rules for the service in a configuration file. VIB authoring tools are available to VMware partners only.
>
> Each set of rules for a service in the rule set configuration file contains the following information.
>
> *   A numeric identifier for the service, if the configuration file contains more than one service.
> *   A unique identifier for the rule set, usually the name of the service.
> *   For each rule, the file contains one or more port rules, each with a definition for direction, protocol, port type, and port number or range of port numbers.
> *   An indication of whether the service is enabled or disabled when the rule set is applied.
> *   An indication of whether the rule set is required and cannot be disabled.
>
> **Example: Rule Set Configuration File**
>
>     <ConfigRoot>
>     <service id='0000'>
>     <id>serviceName</id>
>     <rule id = '0000'>
>     <direction>inbound</direction>
>     <protocol>tcp</protocol>
>     <porttype>dst</porttype>
>     <port>80</port>
>     </rule>
>     <rule id='0001'>
>     <direction>inbound</direction>
>     <protocol>tcp</protocol>
>     <porttype>src</porttype>
>     <port>
>     <begin>1020</begin>
>     <end>1050</end>
>     </port>
>     </rule>
>     <enabled>true</enabled>
>     <required>false</required>
>     </service>
>     </ConfigRoot>
>

Here is what we can do to create a custom rule. First create a file under /etc/vmware/firewall with the appropriate rule. Here is how mine looked like:


     ~ # cat /etc/vmware/firewall/karim.xml
     <ConfigRoot>
     <service>
     <id>karim</id>
     <rule id='0000'>
     <direction>inbound</direction>
     <protocol>tcp</protocol>
     <porttype>dst</porttype>
     <port>1024</port>
     </rule>
     <enabled>false</enabled>
     <required>false</required>
     </service>
     </ConfigRoot>


Then reload the firewall:


     ~ # esxcli network firewall refresh


Then check to see if the rule is correctly configured:


     ~ # esxcli network firewall ruleset list -r karim
     Name Enabled
     ----- -------
     karim false
     ~ # esxcli network firewall ruleset rule list -r karim
     Ruleset Direction Protocol Port Type Port Begin Port End
     ------- --------- -------- --------- ---------- --------
     karim Inbound TCP Dst 1024 1024

### Set firewall security level

Set the firewall to "PASS" all traffic, setting the security level to low:


     ~ # esxcli network firewall get
     Default Action: DROP
     Enabled: true
     Loaded: true
     ~ # esxcli network firewall set -d true
     ~ # esxcli network firewall get
     Default Action: PASS
     Enabled: true
     Loaded: true



Set it back to DROP, setting the security to high:


     ~ # esxcli network firewall set -d false
     ~ # esxcli network firewall get
     Default Action: DROP
     Enabled: true
     Loaded: true


Find a rule that allows all outgoing ports to be allowed through and enabled it, setting the security level to medium:


     ~ # esxcli network firewall ruleset rule list | grep 65535 | grep Outbound
     nfsClient Outbound TCP Dst 0 65535
     vSPC Outbound TCP Dst 0 65535
     remoteSerialPort Outbound TCP Dst 0 65535


Enable any of the above rules:


     ~ # esxcli network firewall ruleset set -r vSPC -e true
     ~ # esxcli network firewall ruleset list -r vSPC
     Name Enabled
     ---- -------
     vSPC true


Lastly you can completely disable the firewall like so:


     ~ # esxcli network firewall set -e false
     ~ # esxcli network firewall get
     Default Action: DROP
     Enabled: false
     Loaded: true


This would also set the security level to low.
