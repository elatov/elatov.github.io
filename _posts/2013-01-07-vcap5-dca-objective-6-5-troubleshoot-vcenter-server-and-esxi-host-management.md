---
title: VCAP5-DCA Objective 6.5 – Troubleshoot vCenter Server and ESXi Host Management
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-5-troubleshoot-vcenter-server-and-esxi-host-management/
dsq_thread_id:
  - 1405000988
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify CLI commands and tools used to troubleshoot management issues

The easiest thing to try is to restart the management agents. Here is how that looks like:


	~ # services.sh restart
	Running sfcbd stop
	This operation is not supported.
	Please use /etc/init.d/sfcbd-watchdog stop
	Running wsman stop
	Stopping openwsmand
	Running sfcbd-watchdog stop
	Running vpxa stop
	watchdog-vpxa: Terminating watchdog process with PID 3092
	vpxa stopped.
	Running vobd stop
	watchdog-vobd: Terminating watchdog process with PID 3058
	vobd stopped
	Running cdp stop
	watchdog-cdp: Terminating watchdog process with PID 3039
	Running dcbd stop
	watchdog-dcbd: Terminating watchdog process with PID 3019
	Running memscrubd stop
	memscrubd is not running
	Running slpd stop
	Stopping slpd
	Running sensord stop
	sensord is not running
	Running storageRM stop
	watchdog-storageRM: Terminating watchdog process with PID 2875
	storageRM stopped
	Running vprobed stop
	watchdog-vprobed: Terminating watchdog process with PID 2804
	vprobed stopped
	Running hostd stop
	watchdog-hostd: Terminating watchdog process with PID 2782
	hostd stopped.
	Running lbtd stop
	watchdog-net-lbt: Terminating watchdog process with PID 2760
	net-lbt stopped
	Running usbarbitrator stop
	Error running operation: No such file or directory: No such file or directory
	watchdog-usbarbitrator: Terminating watchdog process with PID 2740
	usbarbitrator stopped
	Running SSH stop
	SSH login disabled
	VobUserLib_Init failed with -1
	Running ESXShell stop
	ESXi shell login disabled
	VobUserLib_Init failed with -1
	Running DCUI stop
	Disabling DCUI logins
	VobUserLib_Init failed with -1
	Running DCUI restart
	Enabling DCUI login: runlevel =
	VobUserLib_Init failed with -1
	Running ESXShell restart
	ESXi shell login enabled
	VobUserLib_Init failed with -1
	Running SSH restart
	SSH login enabled
	VobUserLib_Init failed with -1
	Running usbarbitrator restart
	usbarbitrator started
	Running lbtd restart
	net-lbt started
	Running hostd restart
	[5515] Begin 'hostd ++min=0,swap,group=hostd /etc/vmware/hostd/config.xml', min-uptime = 60, max-quick-failures = 1, max-total-failures = 1000000, bg_pid_file = ''
	hostd started.
	Running vprobed restart
	vprobed started
	Running storageRM restart
	storageRM started
	Running sensord restart
	sensord started
	Running slpd restart
	Starting slpd
	Running memscrubd restart
	The checkPages boot option is FALSE, hence memscrubd could not be started.
	Running dcbd restart
	dcbd started
	Running cdp restart
	cdp started
	Running vobd restart
	vobd started
	Running vpxa restart
	[177860] Begin '/usr/lib/vmware/vpxa/bin/vpxa ++min=0,swap,group=vpxa -D /etc/vmware/vpxa', min-uptime = 60, max-quick-failures = 1, max-total-failures = 1000000, bg_pid_file = ''
	Running sfcbd-watchdog restart
	Running wsman restart
	Starting openwsmand
	Running sfcbd restart
	This operation is not supported.
	Please use /etc/init.d/sfcbd-watchdog start


If you want you can also just restart hostd and vpxa, those are used for Host management. Here is how you could do that:


	~ # /etc/init.d/hostd restart
	watchdog-hostd: Terminating watchdog process with PID 5515
	hostd stopped.
	[178454] Begin 'hostd ++min=0,swap,group=hostd /etc/vmware/hostd/config.xml', min-uptime = 60, max-quick-failures = 1, max-total-failures = 1000000, bg_pid_file = ''
	hostd started.


And here is vpxa:


	~ # /etc/init.d/vpxa restart
	watchdog-vpxa: Terminating watchdog process with PID 177860
	vpxa stopped.
	vpxa is running


Check to make sure that hostd is running:


	~ # ps -csvt | grep hostd
	178454 178454 sh User,Native WAIT UWAIT 0,1 /bin/sh /sbin/watchdog.sh -s hostd hostd ++min=0,swap,group=hostd /etc/vmware/hostd/config.xml
	178465 178465 hostd-worker User,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178476 178465 hostd-poll User,Clone,Native WAIT UPOL 0,1 hostd /etc/vmware/hostd/config.xml
	178479 178465 hostd-worker User,Clone,Native WAIT USLP 0,1 hostd /etc/vmware/hostd/config.xml
	178480 178465 hostd-worker User,Clone,Native WAIT UPOL 0,1 hostd /etc/vmware/hostd/config.xml
	178483 178483 nssquery User,Native WAIT UPIPER 0,1 /usr/libexec/hostd/nssquery
	178484 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178486 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178515 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178565 178465 hostd-vix-high- User,Clone,Native WAIT UPOL 0,1 hostd /etc/vmware/hostd/config.xml
	178566 178465 hostd-vix-poll User,Clone,Native WAIT UPOL 0,1 hostd /etc/vmware/hostd/config.xml
	178585 178465 hostd-hbr User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178588 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178589 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178590 178465 hostd-worker User,Clone,Native WAIT UFUTEX 0,1 hostd /etc/vmware/hostd/config.xml
	178736 178736 grep User,Native RUN NONE 0,1 grep hostd


Check to make sure ports 443,902, and 80 are ready for connections:


	~ # esxcli network ip connection list | grep -E '443|902|80 ' | grep LISTEN
	tcp 0 0 0.0.0.0:80 0.0.0.0:0 LISTEN 178465 hostd-worker
	tcp 0 0 0.0.0.0:443 0.0.0.0:0 LISTEN 178465 hostd-worker
	tcp 0 0 0.0.0.0:902 0.0.0.0:0 LISTEN 0


Lastly you can check if the host is talking with the vCenter by checking udp traffic on port 902. Heartbeats are send every 10 seconds:


	~ # tcpdump-uw -i vmk0 udp port 902
	tcpdump-uw: WARNING: SIOCGIFINDEX: Invalid argument
	tcpdump-uw: verbose output suppressed, use -v or -vv for full protocol decode
	listening on vmk0, link-type EN10MB (Ethernet), capture size 96 bytes
	00:03:44.359851 IP truncated-ip - 12 bytes missing! 192.168.0.103.57087 > 192.168.0.121.902: UDP, length 66
	00:03:54.362478 IP truncated-ip - 12 bytes missing! 192.168.0.103.57623 > 192.168.0.121.902: UDP, length 66
	00:04:04.364119 IP truncated-ip - 12 bytes missing! 192.168.0.103.56077 > 192.168.0.121.902: UDP, length 66
	tcpdump-uw: pcap_loop: recvfrom: Interrupted system call
	3 packets captured
	3 packets received by filter
	0 packets dropped by kernel


### Troubleshoot vCenter Server service and database connection issues

The is a lot of good information in VMware KB [1003926](http://kb.vmware.com/kb/1003928). Here is a snippet from 1003926:

> *   If you try to start the VMware VirtualCenter Server service, you may see the errors:
>     *   Could not start the VMware VirtualCenter Server service on Local Computer. Error 1067: The process terminated unexpectedly.
>     *   Could not start the VMware VirtualCenter Server service on Local Computer. Error 1069: The service did not start due to a logon failure.
>     *   The VMware VirtualCenter Server Service on Local Computer started then stopped. Some services stop automatically if they have no work to do, for example the Performance Logs and Alerts service.
> *   In the %ALLUSERSPROFILE%\VMware\VMware VirtualCenter\Logs\vpxd.log file of vCenter Server, you see an entry similar to:
>
>	     [VpxdReverseProxy] Failed to create http proxy: An attempt was made to access a socket in a way forbidden by its access permissions.
>	     [Vpxd::ServerApp::Init] Init failed: VpxdMoReverseProxy::Init()
>	     Failed to intialize VMware VirtualCenter. Shutting down...
>	     Forcing shutdown of VMware VirtualCenter now
>

After that it has a lot of different steps to figure out why the service didn't start. Also try to stop and start the vCenter Service manually and check out the event viewer for any errors:


	C:\Users\Administrator>net stop "VMware VirtualCenter Server"
	The following services are dependent on the VMware VirtualCenter Server service.

	Stopping the VMware VirtualCenter Server service will also stop these services.

	VMware vSphere Profile-Driven Storage Service
	vCenter Inventory Service

	Do you want to continue this operation? (Y/N) [N]: Y
	The VMware vSphere Profile-Driven Storage Service service is stopping...
	The VMware vSphere Profile-Driven Storage Service service was stopped successful
	ly.

	The vCenter Inventory Service service is stopping...
	The vCenter Inventory Service service was stopped successfully.

	The VMware VirtualCenter Server service is stopping.....
	The VMware VirtualCenter Server service was stopped successfully.

	C:\Users\Administrator>net start "VMware VirtualCenter Server"
	The VMware VirtualCenter Server service is starting.........................
	The VMware VirtualCenter Server service was started successfully.


And from KB 1003928:

> **Viewing and modifying the database server and/or database used by vCenter Server (Microsoft SQL)**
>
> To view or modify the database server and/or database that vCenter Server is configured to use when using Microsoft SQL:
>
> 1.  Log into the vCenter Server as an administrator.
> 2.  Click **Start** > **Control Panel** > **Administrative Tools** > **Data Sources (ODBC)**.For vCenter Server 4.0 running on a 64-bit host:
>     Click **Start** > **Run**, type %systemdrive%\Windows\SysWoW64\Odbcad32.exe, and press **Enter**.
>     *   Click the **System DSN** tab.
>     *   Under System Data Sources, select the Data Source that vCenter Server is using, as noted in the previous section of this article.
>     *   Click **Configure**.
>     *   On the Configure pane you see the name of the configured database server in the server text box. To change the database server, type the name or IP address of the new server to be used in this box.
>     *   Click **Next**.
>     *   Enter the appropriate login credentials on the next page.**Note**: The login information here is not saved, it is simply used for the configuration and testing of the Data Source.
>     *   Click **Next**.
>     *   On this pane you see the database that has been configured. To change the database, ensure that the checkbox for **Change the default database to** is selected, and select the database that you want to use for vCenter Server.**Note**: If the database has not been selected, the default database for the account is used. To confirm you have selected the database you need, you must log into SQL.
>     *   Click **Next**.
>     *   Click **Next** on the next screen, making no changes.
>     *   Click **Finish**.
>     *   Click **Test Data Source** to verify the information entered.
>     *   When the test completes, review the information presented and click **OK**.
>     *   If the test was successful, click **OK** to exit the wizard. If the test did not complete successfully, click **Cancel** and review the information entered to ensure it is valid.
>     *   Once the test is successful, click **OK** to exit the ODBC Data Source Administrator window.

### Troubleshoot the ESXi firewall

From "[vSphere Command-Line Interface Concepts and Examples](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf)":

> **To limit shell access**
>
> 1.  Check firewall status and sshServer ruleset status.
>
>         esxcli network firewall get
>         Default Action: DROP
>         Enabled: true
>         Loaded: true
>         esxcli network firewall ruleset list --ruleset-id sshServer
>         Name Enabled
>         --------- -------
>         sshServer true
>
> 2.  Enable the sshServer ruleset if it is disabled.
>
>         esxcli network firewall ruleset set --ruleset-id sshServer --enabled true
>
> 3.  Obtain access to the ESXi Shell and check the status of the allowedAll flag.
>
>         esxcli network firewall ruleset allowedip list --ruleset-id sshServer
>         Ruleset Allowed IP Addresses
>         --------- --------------------
>         sshServer All
>
> 4.  Set the status of the allowedAll flag to false.
>
>         esxcli network firewall ruleset set --ruleset-id sshServer --allowed-all false
>
> 5.  Add the list of allowed IP addresses.
>
>         esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address 192.XXX.1.0/24
>         esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address 192.XXX.10.10
>
> 6.  Check the allowed IP address list.
>
>         esxcli network firewall ruleset allowedip list --ruleset-id sshServer
>         Ruleset Allowed IP Addresses
>         --------- -----------------------------
>         sshServer 192.XXX.10.10, 192.XXX.1.0/24
>

From VMware KB [2008226](http://kb.vmware.com/kb/2008226):

> To enable DNS for TCP, complete these steps:
>
> 1.  Open an SSH connection to the host.
> 2.  List the firewall rules with this command:
>
>         # esxcli network firewall ruleset list
>         Name Enabled
>         -------------------------------
>         sshServer true
>         sshClient false
>         nfsClient true
>         dhcp true
>         dns true
>         snmp true
>         ntpClient false
>         CIMHttpServer true
>         CIMHttpsServer true
>         CIMSLP true
>         iSCSI true
>
> **Note**: On vSphere client, the DNS service is open on port 53 for UDP only.
>
> To enable the DNS service on port 53 for TCP:
>
> 1.  Backup the file **/etc/vmware/firewall/service.xml**.
>     Note: Verify that the service.xml file has enough privileges for the modifications to be saved. Use the chmod command to change the file permissions.
>     *   Add this rule to the **service.xml** file in a plain text editor:
>
>              <service id="0032">
>              <id>DNSTCPOut </id>
>              <rule id='0000'>
>              <direction>outbound</direction>
>              <protocol>tcp</protocol>
>              <porttype>dst</porttype>
>              <port>53</port>
>              </rule>
>              <enabled>true</enabled>
>              <required>false</required>
>              </service>
>
>
> **Example of the rule set configuration file**
>
>         <ConfigRoot>
>         <service id='0000'>
>         <id>serviceName</id>
>         <rule id = '0000'>
>         <direction>inbound</direction>
>         <protocol>tcp</protocol>
>         <porttype>dst</porttype>
>         <port>80</port>
>         </rule>
>         <rule id='0001'>
>         <direction>inbound</direction>
>         <protocol>tcp</protocol>
>         <porttype>src</porttype>
>         <port>
>         <begin>1020</begin>
>         <end>1050</end>
>         </port>
>         </rule>
>         <enabled>true</enabled>
>         <required>false</required>
>         </service>
>         </ConfigRoot>
>
> *   Refresh the firewall rules for the changes to take effect with this command:
>
>          # esxcli network firewall refresh
>
> **Note**: This setting does not persist after a reboot. To make it persistent, refer KB 2011818.
>
> *   List the rules again using this command:
>
>         # esxcli network firewall ruleset list
>         Name Enabled
>         -------------- -----------------
>         sshServer true
>         sshClient false
>         nfsClient true
>         dhcp true
>         dns true
>         snmp true
>         ntpClient false
>         CIMHttpServer true
>         CIMHttpsServer true
>         CIMSLP true
>         iSCSI true
>         DNSTCPOut true
>
>  **Note**: The new firewall rule DNSTCPOut allows outgoing connections on TCP port 53.

### Troubleshoot ESXi host management and connectivity issues

From the host ping another host and the vCenter IPs:


     ~ # vmkping 192.168.0.101 -c 1
     PING 192.168.0.101 (192.168.0.101): 56 data bytes
     64 bytes from 192.168.0.101: icmp_seq=0 ttl=64 time=0.848 ms

     --- 192.168.0.101 ping statistics ---
     1 packets transmitted, 1 packets received, 0% packet loss
     round-trip min/avg/max = 0.848/0.848/0.848 ms

Then find out the IP of vCenter and ping it:

     ~ # grep serverIp /etc/vmware/vpxa/vpxa.cfg
     <serverIp>192.168.0.121</serverIp>
     ~ # vmkping -c 1 192.168.0.121
     PING 192.168.0.121 (192.168.0.121): 56 data bytes
     64 bytes from 192.168.0.121: icmp_seq=0 ttl=128 time=0.906 ms

     --- 192.168.0.121 ping statistics ---
     1 packets transmitted, 1 packets received, 0% packet loss
     round-trip min/avg/max = 0.906/0.906/0.906 ms

Make sure DNS is working as well:

     ~ # nslookup vcenter
     Name: vcenter
     Address 1: 192.168.0.121 vcenter
     ~ # nslookup esx1
     Name: esx1
     Address 1: 192.168.0.101 esx1

From the vCenter make sure you can telnet to hostd of the host:

     C:\Users\Administrator>telnet 192.168.0.103 902
     220 VMware Authentication Daemon Version 1.10: SSL Required, ServerDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , VMXARGS supported


### Determine the root cause of a vSphere management or connectivity issue

Check out the logs under:

- **/var/log/hostd.log** - main management daemon
- **/var/log/vpxa.log** - management daemon that handles request from vCenter and forwards to hostd

You will see disconnects there.

### Utilize Direct Console User Interface (DCUI) and ESXi Shell to troubleshoot, configure, and monitor an environment

This was covered in "[VCAP5-DCA Objective 6.3](http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-3-troubleshoot-network-performance-and-connectivity/)"
