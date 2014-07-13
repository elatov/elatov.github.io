---
title: VCAP5-DCA Objective 7.1 – Secure ESXi Hosts
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-7-1-secure-esxi-hosts/
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['dcui', 'esx_firewall','ssl','esx_conf']
---

### Identify configuration files related to network security

Here are the config files for SSH:


	~ # ls /etc/ssh/
	keys-root ssh_host_dsa_key ssh_host_rsa_key sshd_config
	moduli ssh_host_dsa_key.pub ssh_host_rsa_key.pub


SSH is used to securely manage a host from a remote client. Here are the ssl certificates that used to encrypt data between vCenter and an ESXi host:


	~ # ls /etc/vmware/ssl/
	rui.crt rui.key


Here are the files that contain all the firewall rules for the ESXi host:


	~ # ls /etc/vmware/firewall/
	fdm.xml service.xml


Here are all the network security settings store under */etc/vmware/esx.conf* for all the virtual switches configured on a host:


	~ # grep security /etc/vmware/esx.conf
	/net/vswitch/child[0000]/securityPolicy/forgedTx = "true"
	/net/vswitch/child[0000]/securityPolicy/interPgTx = "true"
	/net/vswitch/child[0000]/securityPolicy/localPackets = "true"
	/net/vswitch/child[0000]/securityPolicy/macChange = "true"
	/net/vswitch/child[0000]/securityPolicy/promiscuous = "false"
	/net/vswitch/child[0001]/securityPolicy/forgedTx = "true"
	/net/vswitch/child[0001]/securityPolicy/interPgTx = "true"
	/net/vswitch/child[0001]/securityPolicy/localPackets = "true"
	/net/vswitch/child[0001]/securityPolicy/macChange = "true"
	/net/vswitch/child[0001]/securityPolicy/promiscuous = "false"
	/net/vswitch/child[0002]/securityPolicy/forgedTx = "true"
	/net/vswitch/child[0002]/securityPolicy/macChange = "true"
	/net/vswitch/child[0002]/securityPolicy/promiscuous = "false"
	/net/vswitch/child[0003]/securityPolicy/forgedTx = "true"
	/net/vswitch/child[0003]/securityPolicy/macChange = "true"
	/net/vswitch/child[0003]/securityPolicy/promiscuous = "false"


Here is a list of supported functions that use pam for authentication:


	~ # ls /etc/pam.d/
	dcui other sshd system-auth-local
	login passwd system-auth vmware-authd
	openwsman sfcb system-auth-generic


### Identify virtual switch security characteristics

These were covered in "[VCAP5-DCA Objective 2.1](/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/)" Here is a concise list:

1.  Promiscuous mode
2.  MAC address change
3.  Forged transmit

### Add/Edit Remove users/groups on an ESXi host

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Add a Local User**
> Adding a user to the users table updates the internal user list that the host maintains.
>
> **Procedure**
>
> 1.  Log in to ESXi using the vSphere Client.
> 2.  Click the Local Users & Groups tab and click Users.
> 3.  Right-click anywhere in the Users table and click Add to open the Add New User dialog box.
> 4.  Enter a login, a user name, a numeric user ID (UID), and a password.
>     *   n Specifying the user name and UID are optional. If you do not specify the UID, the vSphere Client assigns the next available UID.
>     *   n Create a password that meets the length and complexity requirements. The host checks for password compliance using the default authentication plug-in, pam_passwdqc.so. If the password is not compliant, the following error appears: A general system error occurred: passwd: Authentication token manipulation error.
> 5.  To change the user’s ability to access ESXi through a command shell, select or deselect Grant shell access to this user.In general, do not grant shell access unless the user has a justifiable need. Users that access the host only through the vSphere Client do not need shell access.
> 6.  To add the user to a group, select the group name from the Group drop-down menu and click Add.
> 7.  Click OK.

Here is how it looks like from the vSphere Client:
![users groups vscl VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/users_groups-vscl.png)

![add new user VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/add_new_user.png)

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Add a Group**
> Adding a group to the groups table updates the internal group list maintained by the host.
>
> **Procedure**
>
> 1.  Log in to ESXi using the vSphere Client.
> 2.  Click the Local Users & Groups tab and click Groups.
> 3.  Right-click anywhere in the Groups table and click Add to open the Create New Group dialog box.
> 4.  Enter a group name and numeric group ID (GID).Specifying the ID is optional. If you do not specify an ID, the vSphere Client assigns the next available group ID.
> 5.   From the User list, select user to add and click Add.
> 6.  Click OK

Here is how it looks like from the vSphere Client:

![esx groups VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/esx_groups.png)

![add group VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/add_group.png)

### Customize SSH settings for increased security

From "[Command-Line Management in vSphere 5.0 for Service Console Users](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-management-for-service-console-users.pdf)":

> **Remote Access to ESXi Shell Using SSH**
> If Secure Shell is enabled for the ESXi Shell, you can run shell commands by using a Secure Shell client such as SSH or PuTTY.
>
> **Enabling SSH for the ESXi Shell**
> By default, you cannot access the ESXi Shell using a Secure Shell client. You can enable SSH access from the direct console.
>
> **To enable SSH access in the direct console**
>
> 1.  At the direct console of the ESXi host, press F2 and provide credentials when prompted.
> 2.  Scroll to Troubleshooting Options, and press Enter.
> 3.  Select Enable SSH and press Enter once.On the left, Enable SSH changes to Disable SSH. On the right, SSH is Disabled changes to SSH is Enabled.
> 4.  Press Esc until you return to the main direct console screen.

Here is how it looks like from the Direct Console:

![dcui ssh enabled VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/dcui_ssh_enabled.png)

From the same document:

> You can enable remote command execution from the vSphere Client.
>
> **To enable SSH from the vSphere Client**
>
> 1.  Select the host and click the Configuration tab.
> 2.  Click Security Profile in the Software panel.
> 3.  In the Services section, click Properties.
> 4.  Select SSH and click Options.
> 5.  Change the SSH options.
>     *   To temporarily start or stop the service, click the Start or Stop button.
>     *   To enable SSH permanently, click Start and stop with host. The change takes effect the next time you reboot the host.
> 6.  Click OK.
>
> After you have enabled SSH, you can use an SSH client to log in to the ESXi Shell and run ESXi Shell commands.

Here is how it looks like from vCenter:

![enabled ssh vscl VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/enabled_ssh_vscl.png)

You can also set a timeout for the shell with the following advanced option:


	~ # esxcfg-advcfg -l | grep -i ESXiShell
	/UserVars/ESXiShellTimeOut [Integer] : Timeout for local and remote shell access (in seconds)


### Enable/Disable certificate checking

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Enable Certificate Checking and Verify Host Thumbprints**
> To prevent man-in-the-middle attacks and to fully use the security that certificates provide, certificate checking is enabled by default. You can verify that certificate checking is enabled in the vSphere Client.
>
> **Procedure**
>
> 1.  Log in to the vCenter Server system using the vSphere Client.
> 2.  Select Administration > vCenter Server Settings.
> 3.  Click SSL Settings in the left pane and verify that Check host certificates is selected.
> 4.  If there are hosts that require manual validation, compare the thumbprints listed for the hosts to the thumbprints in the host console.To obtain the host thumbprint, use the Direct Console User Interface (DCUI).
>     *   Log in to the direct console and press F2 to access the System Customization menu.
>     *   Select View Support Information.The host thumbprint appears in the column on the right.
> 5.  If the thumbprint matches, select the Verify check box next to the host. Hosts that are not selected will be disconnected after you click OK.
> 6.  Click OK.

Here is how the setting looks like from vCenter:

![vcenter verify ssl certs VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/vcenter_verify_ssl_certs.png)

### Generate ESXi host certificates

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Generate New Certificates for ESXi**
> You typically generate new certificates only if you change the host name or accidentally delete the certificate. Under certain circumstances, you might be required to force the host to generate new certificates.
>
> **Procedure**
>
> 1.  Log in to the ESXi Shell and acquire root privileges.
>	 2.  In the directory /etc/vmware/ssl, back up any existing certificates by renaming them using the following commands.
>
>         mv rui.crt orig.rui.crt
>         mv rui.key orig.rui.key
>
> 3.  Run the command */sbin/generate-certificates* to generate new certificates.
> 4.  Restart the host after you install the new certificate. Alternatively, you can put the host into maintenance mode, install the new certificate, and then use the Direct Console User Interface (DCUI) to restart the management agents.
>	 5.  Confirm that the host successfully generated new certificates by using the following command and comparing the time stamps of the new certificate files with orig.rui.crt and orig.rui.key.
>
>         ls -la
>

### Enable ESXi lockdown mode

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Lockdown Mode Behavior**
> Enabling lockdown mode affects which users are authorized to access host services.
>
> Users who were logged in to the ESXi Shell before lockdown mode was enabled remain logged in and can run commands. However, these users cannot disable lockdown mode. No other users, including the root user and users with the Administrator role on the host, can use the ESXi Shell to log in to a host that is in lockdown mode.
>
> Users with administrator privileges on the vCenter Server system can use the vSphere Client to disable lockdown mode for hosts that are managed by the vCenter Server system. Root users and users with the Administrator role on the host can always log directly in to the host using the Direct Console User Interface (DCUI) to disable lockdown mode. If the host is not managed by vCenter Server or if the host is unreachable, you must reinstall ESXi.
>
> Different services are available to different types of users when the host is running in lockdown mode,compared to when the host is running in normal mode. Non-root users cannot run system commands in the ESXi Shell.
>
> ![lockdown behavior VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/lockdown_behavior.png)
>
> **Lockdown Mode Configurations**
> You can enable or disable remote and local access to the ESXi Shell to create different lockdown mode configurations. The following table lists which services are enabled for three typical configurations.
>
> **CAUTION**: If you lose access to vCenter Server while running in Total Lockdown Mode, you must reinstall ESXi to gain access to the host
>
> ![lockdown conf VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/lockdown_conf.png)

And now how to actually enable lockdown mode:

> **Enable Lockdown Mode Using the vSphere Client**
> Enable lockdown mode to require that all configuration changes go through vCenter Server. You can also enable or disable lockdown mode through the Direct Console User Interface (DCUI). **Procedure**
>
> 1.  Log in to a vCenter Server system using the vSphere Client.
> 2.  Select the host in the inventory panel.
> 3.  Click the Configuration tab and click Security Profile.
> 4.  Click the Edit link next to lockdown mode.The Lockdown Mode dialog box appears.
> 5.  Select Enable Lockdown Mode.
> 6.  Click OK.

Here is how it looks like from vCenter:

![lockdown from host VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/lockdown_from_host.png)

![enable lock down mode VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/enable_lock_down_mode.png)

And here are the instructions from the DCUI:

> **Enable Lockdown Mode from the Direct Console User Interface**
> You can enable lockdown mode from the Direct Console User Interface (DCUI).
>
> **NOTE**: If you enable or disable lockdown mode using the Direct Console User Interface, permissions for users and groups on the host are discarded. To preserve these permissions, you must enable and disable lockdown mode using the vSphere Client connected to vCenter Server.
>
> **Procedure**
>
> 1.  At the Direct Console User Interface of the host, press F2 and log in.
> 2.  Scroll to the Configure Lockdown Mode setting and press Enter.
> 3.  Press Esc until you return to the main menu of the Direct Console User Interface.

Here is how it looks like from the Console:

![lockdown mode dcui VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/lockdown_mode_dcui.png)

![conf lock down mode VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/conf_lock_down_mode.png)

### Replace default certificate with CA-signed certificate

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Replace a Default Host Certificate with a CA-Signed Certificate**
>
> The ESXi host uses automatically generated certificates that are created as part of the installation process. These certificates are unique and make it possible to begin using the server, but they are not verifiable and they are not signed by a trusted, well-known certificate authority (CA).
>
> Using default certificates might not comply with the security policy of your organization. If you require a certificate from a trusted certificate authority, you can replace the default certificate.
>
> ESXi supports only X.509 certificates to encrypt session information sent over SSL connections between server and client components.
>
> **Procedure**
>
> 1.  Log in to the ESXi Shell and acquire root privileges.
>	 2.  In the directory /etc/vmware/ssl, rename the existing certificates using the following commands.
>
>         mv rui.crt orig.rui.crt
>         mv rui.key orig.rui.key
>
> 3.  Copy the new certificate and key to **/etc/vmware/ssl**.
> 4.  Rename the new certificate and key to **rui.crt** and **rui.key**.
> 5.  Restart the host after you install the new certificate. Alternatively, you can put the host into maintenance mode, install the new certificate, and then use the Direct Console User Interface (DCUI) to restart the management agents.

### Configure SSL timeouts

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Configure SSL Timeouts**
> You can configure SSL timeouts for ESXi. Timeout periods can be set for two types of idle connections:
>
> *   The Read Timeout setting applies to connections that have completed the SSL handshake process with port 443 of ESXi.
> *   The Handshake Timeout setting applies to connections that have not completed the SSL handshake process with port 443 of ESXi.
>
> Both connection timeouts are set in milliseconds. Idle connections are disconnected after the timeout period. By default, fully established SSL connections have a timeout of infinity. **Procedure**
>
> 1.  Log in to the ESXi Shell and acquire root privileges.
> 2.  Change to the directory **/etc/vmware/hostd/**.
> 3.  Use a text editor to open the config.xml file.
> 4.  Enter the value in milliseconds. For example, to set the Read Timeout to 20 seconds, enter the following command.
>
>         20000
>
> 5.  Enter the value in milliseconds. For example, to set the Handshake Timeout to 20 seconds, enter the following command.
>
>         20000
>
> 6.  Save your changes and close the file.
> 7.  Restart the hostd process:
>
>         /etc/init.d/hostd restart
>
>
> **Example: Configuration File** The following section from the file */etc/vmware/hostd/config.xml* shows where to enter the SSL timeout settings.
>
>
>     ...
>     20000
>     ...
>     ...
>     20000
>     ...
>

### Configure vSphere Authentication Proxy

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Using vSphere Authentication Proxy**
> When you use the vSphere Authentication Proxy, you do not need to transmit Active Directory credentials to the host. Users supply the domain name of the Active Directory server and the IP address of the authentication proxy server when they add a host to a domain.
>
> **Install the vSphere Authentication Proxy Service**
> To use the vSphere Authentication Proxy service (CAM service) for authentication, you must install the service on a host machine.
>
> You can install the vSphere Authentication Proxy on the same machine as the associated vCenter Server, or on a different machine that has a network connection to the vCenter Server. The vSphere Authentication Proxy is not supported with vCenter Server versions earlier than version 5.0.
>
> The vSphere Authentication Proxy service binds to an IPv4 address for communication with vCenter Server, and does not support IPv6. vCenter Server can be on an IPv4-only, IPv4/IPv6 mixed-mode, or IPv6-only host machine, but the machine that connects to vCenter Server through the vSphere Client must have an IPv4 address for the vSphere Authentication Proxy service to work.
>
> **Procedure**
>
> 1.  On the host machine where you will install the vSphere Authentication Proxy service, install the .NET Framework 3.5.
> 2.  Install vSphere Auto Deploy.You do not have to install Auto Deploy on the same host machine as the vSphere Authentication Proxy service.
> 3.  Add the host machine where you will install the authentication proxy service to the domain.
> 4.  Use the Domain Administrator account to log in to the host machine.
> 5.  In the software installer directory, double-click the autorun.exe file to start the installer.
> 6.  Select VMware vSphere Authentication Proxy and click Install.
> 7.  Follow the wizard prompts to complete the installation.During installation, the authentication service registers with the vCenter Server instance where Auto Deploy is registered.
>
> The authentication proxy service is installed on the host machine.

And more from the same document:

> **Configure a Host to Use the vSphere Authentication Proxy for Authentication**
> After you install the vSphere Authentication Proxy service (CAM service), you must configure the host to use the authentication proxy server to authenticate users.
>
> **Procedure**
>
> 1.  Use the IIS manager on the host to set up the DHCP range. Setting the range allows hosts that are using DHCP in the management network to use the authentication proxy service.
>     ![iis for cam service VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/iis_for_cam_service.png)
> 2.  If a host is not provisioned by Auto Deploy, change the default SSL certificate to a self-signed certificate or to a certificate signed by a commercial certificate authority (CA)
>     ![cam certificate option VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/cam_certificate_option.png)

Now we need to export the certificates from the CAM service and upload it to our ESXi host:

> **Export vSphere Authentication Proxy Certificate**
> To authenticate the vSphere Authentication Proxy to ESXi, you must provide ESXi with the proxy server certificate.
>
> **Procedure**
>
> 1.  On the authentication proxy server system, use the IIS Manager to export the certificate. ![export cam cert with iis VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/export_cam_cert_with_iis.png)
> 2.  Select Details > Copy to File.
> 3.  Select the options **Do Not Export the Private Key** and **Base-64 encoded X.509 (CER)**.
>
> **Import a vSphere Authentication Proxy Server Certificate to ESXi**
> To authenticate the vSphere Authentication Proxy server to ESXi, upload the proxy server certificate to ESXi. You use the vSphere Client user interface to upload the vSphere Authentication Proxy server certificate to ESXi.
>
> **Procedure**
>
> 1.  Select a host in the vSphere Client inventory and click the Summary tab.
> 2.  Upload the certificate for the authentication proxy server to a temporary location on ESXi.
>     1.  Under Resources, right-click a datastore and select Browse Datastore.
>     2.  Select a location for the certificate and select the Upload File button.
>     3.  Browse to the certificate and select Open.
> 3.  Select the Configuration tab and click Authentication Services.
> 4.  Click Import Certificate.
> 5.  Enter the full path to the authentication proxy server certificate file on the host and the IP address of the authentication proxy server.Use the form  file path to enter the path to the proxy server.
> 6.  Click Import.

Lastly use the Proxy to add a host to a domain:

> **Use vSphere Authentication Proxy to Add a Host to a Domain**
> When you join a host to a directory service domain, you can use the vSphere Authentication Proxy server for authentication instead of transmitting user-supplied Active Directory credentials. You can enter the domain name in one of two ways:
>
> *   **name.tld** (for example, **domain.com**): The account is created under the default container.
> *   **name.tld/container/path** (for example, **domain.com/OU1/OU2**): The account is created under a particular organizational unit (OU).
>
> **Procedure**
>
> 1.  In the vSphere Client inventory, select the host.
> 2.  Select the Configuration tab and click Authentication Services.
> 3.  Click Properties.
> 4.  In the Directory Services Configuration dialog box, select the directory server from the drop-down menu.
> 5.  Enter a domain.Use the form **name.tld** or **name.tld/container/path**.
> 6.  Select the Use vSphere Authentication Proxy check box.
> 7.  Enter the IP address of the authentication proxy server.
> 8.  Click Join Domain.
> 9.  Click OK.

### Enable strong passwords and configure password policies

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Host Password Strength and Complexity**
> By default, ESXi uses the pam_passwdqc.so plug-in to set the rules that users must observe when creating passwords and to check password strength.
>
> The pam_passwdqc.so plug-in lets you determine the basic standards that all passwords must meet. By default, ESXi imposes no restrictions on the root password. However, when nonroot users attempt to change their passwords, the passwords they choose must meet the basic standards that pam_passwdqc.so sets.
>
> A valid password should contain a combination of as many character classes as possible. Character classes include lowercase letters, uppercase letters, numbers, and special characters such as an underscore or dash. To configure password complexity, you can change the default value of the following parameters.
>
> *   retry is the number of times a user is prompted for a new password if the password candidate is not sufficiently strong.
> *   N0 is the number of characters required for a password that uses characters from only one character class. For example, the password contains only lowercase letters.
> *   N1 is the number of characters required for a password that uses characters from two character classes.
> *   N2 is used for passphrases. ESXi requires three words for a passphrase. Each word in the passphrase must be 8-40 characters long.
> *   N3 is the number of characters required for a password that uses characters from three character classes.
> *   N4 is the number of characters required for a password that uses characters from all four character classes.
> *   match is the number of characters allowed in a string that is reused from the old password. If the pam_passwdqc.so plug-in finds a reused string of this length or longer, it disqualifies the string from the strength test and uses only the remaining characters.
>
> Setting any of these options to -1 directs the pam_passwdqc.so plug-in to ignore the requirement. Setting any of these options to disabled directs the pam_passwdqc.so plug-in to disqualify passwords with the associated characteristic. The values used must be in descending order except for -1 and disabled.
>
> **Change Default Password Complexity for the pam_passwdqc.so Plug-In**
> Configure the pam_passwdqc.so plug-in to determine the basic standards all passwords must meet.
>
> **Procedure**
>
> 1.  Log in to the ESXi Shell and acquire root privileges.
> 2.  Open the passwd file with a text editor.For example, **vi /etc/pam.d/passwd**
> 3.  Edit the following line.
>
>         password requisite /lib/security/$ISA/pam_passwdqc.so retry=N min=N0,N1,N2,N3,N4
>
> 4.  Save the file.

Here is an example from the same document:

> **Example: Editing /etc/pam.d/passwd**
>
>
>     password requisite /lib/security/$ISA/pam_passwdqc.so retry=3 min=12,9,8,7,6
>
>
> With this setting in effect, the password requirements are:
>
> *   retry=3: A user is allowed 3 attempts to enter a sufficient password.
> *   N0=12: Passwords containing characters from one character class must be at least 12 characters long.
> *   N1=9: Passwords containing characters from two character classes must be at least nine characters long.
> *   N2=8: Passphrases must contain words that are each at least eight characters long.
> *   N3=7: Passwords containing characters from three character classes must be at least seven characters long.
> *   N4=6: Passwords containing characters from all four character classes must be at least six characters long

### Identify methods for hardening virtual machines

From "[vSphere 5.0 Hardening Guide](http://communities.vmware.com/docs/DOC-19605)"

> **RemoteDisplay.maxConnections**
> By default, remote console sessions can be connected to by more than one user at a time. When multiple sessions are activated, each terminal window gets a notification about the new session. If an administrator in the VM logs in using a VMware remote console during their session, a nonadministrator in the VM might connect to the console and observe the administrator's actions. Also, this could result in an administrator losing console access to a virtual machine. For example if a jump box is being used for an open console session, and the admin loses connection to that box, then the console session remains open. Allowing two console sessions permits debugging via a shared session. For highest security, only one remote console session at a time should be allowed
>
> **tools.setInfo.sizeLimit**
> "The configuration file containing these name-value pairs is limited to a size of 1MB. This 1MB capacity should be sufficient for most cases, but you can change this value if necessary. You might increase this value if large amounts of custom information are being stored in the configuration file. The default limit is 1MB; this limit is applied even when the sizeLimit parameter is not listed in the .vmx file. Uncontrolled size for the VMX file can lead to denial of service if the datastore is filled."
>
> **isolation.tools.copy.disable**
> Copy and paste operations are disabled by default however by explicitly disabling this feature it will enable audit controls to check that this setting is correct.
>
> **isolation.tools.hgfsServerSet.disable**
> Certain automated operations such as automated tools upgrades use a component into the hypervisor called "Host Guest File System" and an attacker could potentially use this to transfer files inside the guest OS
>
> **isolation.monitor.control.disable**
> When Virtual Machines are running on a hypervisor they are "aware" that they are running in a virtual environment and this and this information is available to tools inside the guest OS. This can give attackers information about the platform that they are running on that they may not get from a normal physical server. This option completely disables all hooks for a virtual machine and the guest OS will not be aware that it is running in a virtual environment at all.
>
> **isolation.tools.diskShrink.disable**
> Shrinking a virtual disk reclaims unused space in it. If there is empty space in the disk, this process reduces the amount of space the virtual disk occupies on the host drive. Normal users and processes—that is, users and processes without root or administrator privileges—within virtual machines have the capability to invoke this procedure. However, if this is done repeatedly, the virtual disk can become unavailable while this shrinking is being performed, effectively causing a denial of service. In most datacenter environments, disk shrinking is not done, so you should disable this feature by setting the parameters listed in Table 9. Repeated disk shrinking can make a virtual disk unavailable. Capability is available to nonadministrative users in the guest.
>
> **scsiX:Y.mode**
> The security issue with nonpersistent disk mode is that successful attackers, with a simple shutdown or reboot, might undo or remove any traces that they were ever on the machine. To safeguard against this risk, you should set production virtual machines to use either persistent disk mode or nonpersistent disk mode; additionally, make sure that activity within the VM is logged remotely on a separate server, such as a syslog server or equivalent Windows-based event collector. Without a persistent record of activity on a VM, administrators might never know whether they have been attacked or hacked.
>
> **isolation.tools.autoInstall.disable**
> Tools auto install can initiate an automatic reboot, disabling this option can will prevent tools from being installed automatically and prevent automatic machine reboots
>
> **logging**
> You can use these settings to limit the total size and number of log files. Normally a new log file is created only when a host is rebooted, so the file can grow to be quite large. You can ensure that new log files are created more frequently by limiting the maximum size of the log files. If you want to restrict the total size of logging data, VMware recommends saving 10 log files, each one limited to 1,000KB. Datastores are likely to be formatted with a block size of 2MB or 4MB, so a size limit too far below this size would result in unnecessary storage utilization. Each time an entry is written to the log, the size of the log is checked; if it is over the limit, the next entry is written to a new log. If the maximum number of log files already exists, when a new one is created, the oldest log file is deleted. A denial-of-service attack that avoids these limits might be attempted by writing an enormous log entry. But each log entry is limited to 4KB, so no log files are ever more than 4KB larger than the configured limit. A second option is to disable logging for the virtual machine. Disabling logging for a virtual machine makes troubleshooting challenging and support difficult. You should not consider disabling logging unless the log file rotation approach proves insufficient. Uncontrolled logging can lead to denial of service due to the datastore’s being filled.

There are a lot more in the guide. To edit any of the above options do the following:

1.  Choose the virtual machine in the inventory panel.
2.  Click Edit Settings. Click Options > Advanced/General.
3.  Click Configuration Parameters to open the configuration parameters dialog box.

Here is how it looks like in vCenter:

![VM advanced parameters VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/VM_advanced_parameters.png)

### Analyze logs for security-related messages

Most of those will be in the **/var/log/vmkernel.log** file. For example when I run tcpdump on a vmk inside a vSwitch that doesn't have promiscuos mode enabled, I always see this:


	2012-12-23T01:12:51.889Z cpu0:352565)etherswitch: L2Sec_EnforcePortCompliance:226: client vmk0 requested promiscuous mode on port 0x1000003, disallowed by vswitch policy


If you want to check out the commands that were executed on the host, you can check out **/var/log/shell.log**:


	~ # tail /var/log/shell.log
	2012-12-22T23:26:54Z shell[277438]: esxcfg-resgrp -l
	2012-12-22T23:27:00Z shell[277438]: esxcfg-resgrp -l | less
	2012-12-23T00:10:48Z shell[277438]: cd /etc/pam.d/
	2012-12-23T00:10:49Z shell[277438]: ls
	2012-12-23T00:11:05Z shell[277438]: grep passwd passwd
	2012-12-23T01:12:51Z shell[277438]: tcpdump-uw -i vmk0
	2012-12-23T01:12:57Z shell[277438]: tail /var/log/vmkernel.log
	2012-12-23T01:14:02Z shell[277438]: tail /var/log/shell.log
	2012-12-23T01:14:14Z shell[277438]: cd
	2012-12-23T01:14:16Z shell[277438]: tail /var/log/shell.log


### Manage Active Directory integration

From "[vSphere Security ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-security-guide.pdf)":

> **Add a Host to a Directory Service Domain**
> To use a directory service, you must join the host to the directory service domain.
> You can enter the domain name in one of two ways:
>
> *   **name.tld** (for example, **domain.com**): The account is created under the default container.
> *   **name.tld/container/path** (for example, **domain.com/OU1/OU2**): The account is created under a particular organizational unit (OU).
>
> **Procedure**
>
> 1.  Select a host in the vSphere Client inventory, and click the Configuration tab.
> 2.  Click Properties.
> 3.  In the Directory Services Configuration dialog box, select the directory service from the drop-down menu.
> 4.  Enter a domain.
>     Use the form **name.tld** or **name.tld/container/path**.
>     *   Click Join Domain.
>     *   Enter the user name and password of a directory service user who has permissions to join the host to the domain, and click OK.
>     *   Click OK to close the Directory Services Configuration dialog box
>     Here is how it looks like from vCenter:
>
>     ![ad integration VCAP5 DCA Objective 7.1 – Secure ESXi Hosts ](https://github.com/elatov/uploads/raw/master/2012/12/ad_integration.png)
>
