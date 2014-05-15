---
title: RHCSA and RHCE Chapter 17 – FTP
author: Karim Elatov
layout: post
permalink: /2014/04/rhcsa-rhce-chapter-17-ftp/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2614357088
categories:
  - Certifications
  - RHCSA and RHCE
tags:
  - FTP
  - rhcsa_and_rhce
  - vsftpd
---
## FTP

From the <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf']);">Deployment Guide</a>:

> File Transfer Protocol (FTP) is one of the oldest and most commonly used protocols found on the Internet today. Its purpose is to reliably transfer files between computer hosts on a network without requiring the user to log directly into the remote host or have knowledge of how to use the remote system. It allows users to access files on remote systems using a standard set of simple commands.

#### The File Transfer Protocol

From the same guide:

> However, because FTP is so prevalent on the Internet, it is often required to share files to the public. System administrators, therefore, should be aware of the FTP protocol's unique characteristics.
> 
> Unlike most protocols used on the Internet, FTP requires multiple network ports to work properly. When an FTP client application initiates a connection to an FTP server, it opens port 21 on the server — known as the **command** port. This port is used to issue all commands to the server. Any data requested from the server is returned to the client via a **data** port. The port number for data connections, and the way in which data connections are initialized, vary depending upon whether the client requests the data in active or passive mode.
> 
> The following defines these modes:
> 
> *   **active mode** - Active mode is the original method used by the **FTP** protocol for transferring data to the client application. When an active mode data transfer is initiated by the FTP client, the server opens a connection from port 20 on the server to the IP address and a random, unprivileged port (greater than 1024) specified by the client. This arrangement means that the client machine must be allowed to accept connections over any port above 1024. With the growth of insecure networks, such as the Internet, the use of firewalls to protect client machines is now prevalent. Because these client-side firewalls often deny incoming connections from active mode FTP servers, passive mode was devised.
> *   **passive mode** - Passive mode, like active mode, is initiated by the FTP client application. When requesting data from the server, the FTP client indicates it wants to access the data in passive mode and the server provides the IP address and a random, unprivileged port (greater than 1024) on the server. The client then connects to that port on the server to download the requested information. While passive mode resolves issues for client-side firewall interference with data connections, it can complicate administration of the server-side firewall. You can reduce the number of open ports on a server by limiting the range of unprivileged ports on the **FTP** server.

### VSFTPD

From the above guide:

> The *Very Secure FTP Daemon* (**vsftpd**) is designed from the ground up to be fast, stable, and, most importantly, secure. **vsftpd** is the only stand-alone FTP server distributed with Red Hat Enterprise Linux, due to its ability to handle large numbers of connections efficiently and securely.
> 
> The security model used by vsftpd has three primary aspects:
> 
> *   Strong separation of privileged and non-privileged processes — Separate processes handle different tasks, and each of these processes run with the minimal privileges required for the task.
> *   Tasks requiring elevated privileges are handled by processes with the minimal privilege necessary - By leveraging compatibilities found in the **libcap** library, tasks that usually require full root privileges can be executed more safely from a less privileged process.
> *   Most processes run in a **chroot** jail - Whenever possible, processes are change-rooted to the directory being shared; this directory is then considered a **chroot** jail. For example, if the directory **/var/ftp/** is the primary shared directory, vsftpd reassigns **/var/ftp/** to the new root directory, known as **/**. This disallows any potential malicious hacker activities for any directories not contained below the new root directory.
> 
> Use of these security practices has the following effect on how **vsftpd** deals with requests:
> 
> *   The parent process runs with the least privileges required - The parent process dynamically calculates the level of privileges it requires to minimize the level of risk. Child processes handle direct interaction with the **FTP** clients and run with as close to no privileges as possible.
> *   All operations requiring elevated privileges are handled by a small parent process - Much like the Apache **HTTP** Server, **vsftpd** launches unprivileged child processes to handle incoming connections. This allows the privileged, parent process to be as small as possible and handle relatively few tasks.
> *   All requests from unprivileged child processes are distrusted by the parent process — Communication with child processes are received over a socket, and the validity of any information from child processes is checked before being acted on.
> *   Most interaction with **FTP** clients is handled by unprivileged child processes in a **chroot** jail - Because these child processes are unprivileged and only have access to the directory being shared, any crashed processes only allows the attacker access to the shared files.

### vsftpd files

From the Deployment Guide:

> The **vsftpd** RPM installs the daemon (**/usr/sbin/vsftpd**), its configuration and related files, as well as FTP directories onto the system. The following lists the files and directories related to vsftpd configuration:
> 
> *   **/etc/rc.d/init.d/vsftpd** - The initialization script (initscript) used by the **/sbin/service** command to start, stop, or reload vsftpd.
> *   **/etc/pam.d/vsftpd** - The Pluggable Authentication Modules (PAM) configuration file for **vsftpd**. This file specifies the requirements a user must meet to login to the FTP server. 
> *   **/etc/vsftpd/vsftpd.conf** - The configuration file for vsftpd. 
> *   **/etc/vsftpd/ftpusers** - A list of users not allowed to log into **vsftpd**. By default, this list includes the **root**, **bin**, and **daemon** users, among others.
> *   **/etc/vsftpd/user_list** - This file can be configured to either deny or allow access to the users listed, depending on whether the **userlist_deny** directive is set to **YES** (default) or **NO** in **/etc/vsftpd/vsftpd.conf**. If **/etc/vsftpd/user_list** is used to grant access to users, the usernames listed must not appear in **/etc/vsftpd/ftpusers**.
> *   **/var/ftp/** - The directory containing files served by **vsftpd**. It also contains the **/var/ftp/pub/** directory for anonymous users. Both directories are world-readable, but writable only by the root user.

### vsftpd service

From the same guide:

> The **vsftpd** RPM installs the **/etc/rc.d/init.d/vsftpd** script, which can be accessed using the **service** command.
> 
> To start the server, as root type:
> 
>     ~]# service vsftpd start
>     
> 
> To stop the server, as root type:
> 
>     ~]# service vsftpd stop
>     
> 
> The restart option is a shorthand way of stopping and then starting vsftpd. This is the most efficient way to make configuration changes take effect after editing the configuration file for **vsftpd**.
> 
> To restart the server, as root type:
> 
>     ~]# service vsftpd restart
>     
> 
> The condrestart (conditional restart) option only starts **vsftpd** if it is currently running. This option is useful for scripts, because it does not start the daemon if it is not running.
> 
> To conditionally restart the server, as root type:
> 
>     ~]# service vsftpd condrestart
>     
> 
> By default, the **vsftpd** service does not start automatically at boot time. To configure the **vsftpd** service to start at boot time, use an initscript utility, such as **/sbin/chkconfig**.

### vsftpd daemon options

From the above guide:

> The following is a list of directives which control the overall behavior of the **vsftpd** daemon.
> 
> *   **listen** - When enabled, **vsftpd** runs in stand-alone mode. Red Hat Enterprise Linux sets this value to **YES**. This directive cannot be used in conjunction with the **listen_ipv6** directive.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **listen_ipv6** - When enabled, **vsftpd** runs in stand-alone mode, but listens only to **IPv6** sockets. This directive cannot be used in conjunction with the **listen** directive.
>     
>     The default value is **NO**.
> 
> *   **session_support** - When enabled, vsftpd attempts to maintain login sessions for each user through **Pluggable Authentication Modules** (PAM). If session logging is not necessary, disabling this option allows vsftpd to run with less processes and lower privileges.
>     
>     The default value is **YES**.

### vsftpd Log In Options and Access Controls

From the above guide:

> The following is a list of directives which control the login behavior and access control mechanisms.
> 
> *   **anonymous_enable** - When enabled, anonymous users are allowed to log in. The usernames **anonymous** and **ftp** are accepted.
>     
>     The default value is **YES**.
> 
> *   **banned\_email\_file** - If the **deny\_email\_enable** directive is set to **YES**, this directive specifies the file containing a list of anonymous email passwords which are not permitted access to the server.
>     
>     The default value is **/etc/vsftpd/banned_emails**.
> 
> *   **banner_file** - Specifies the file containing text displayed when a connection is established to the server. This option overrides any text specified in the **ftpd_banner** directive.
>     
>     There is no default value for this directive.
> 
> *   **cmds_allowed** - Specifies a comma-delimited list of FTP commands allowed by the server. All other commands are rejected.
>     
>     There is no default value for this directive.
> 
> *   **deny\_email\_enable** - When enabled, any anonymous user utilizing email passwords specified in the **/etc/vsftpd/banned_emails** are denied access to the server. The name of the file referenced by this directive can be specified using the **banned\_email\_file** directive.
>     
>     The default value is **NO**.
> 
> *   **ftpd_banner** - When enabled, the string specified within this directive is displayed when a connection is established to the server. This option can be overridden by the **banner_file** directive.
>     
>     By default **vsftpd** displays its standard banner.
> 
> *   **local_enable** — When enabled, local users are allowed to log into the system.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **pam\_service\_name** - Specifies the PAM service name for **vsftpd**.
>     
>     The default value is **ftp**. On Red Hat Enterprise Linux 6, this option is set to **vsftpd** in the configuration file.
> 
> *   **tcp_wrappers** — When enabled, TCP wrappers are used to grant access to the server. If the FTP server is configured on multiple IP addresses, the **VSFTPD\_LOAD\_CONF** environment variable can be used to load different configuration files based on the IP address being requested by the client.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **userlist_deny** — When used in conjunction with the **userlist_enable** directive and set to **NO**, all local users are denied access unless the username is listed in the file specified by the **userlist_file** directive. Because access is denied before the client is asked for a password, setting this directive to **NO** prevents local users from submitting unencrypted passwords over the network.
>     
>     The default value is **YES**.
> 
> *   **userlist_enable** - When enabled, the users listed in the file specified by the **userlist_file** directive are denied access. Because access is denied before the client is asked for a password, users are prevented from submitting unencrypted passwords over the network.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **userlist_file** — Specifies the file referenced by **vsftpd** when the **userlist_enable** directive is enabled.
>     
>     The default value is **/etc/vsftpd/user_list**, which is created during installation.

### vsftpd Anonymous User Options

From the Deployment Guide:

> The following lists directives which control anonymous user access to the server. To use these options, the **anonymous_enable** directive must be set to **YES**.
> 
> *   **anon\_mkdir\_write_enable** - When enabled in conjunction with the **write_enable** directive, anonymous users are allowed to create new directories within a parent directory which has write permissions.
>     
>     The default value is **NO**.
> 
> *   **anon_root** - Specifies the directory **vsftpd** changes to after an anonymous user logs in.
>     
>     There is no default value for this directive.
> 
> *   **anon\_upload\_enable** - When enabled in conjunction with the **write_enable** directive, anonymous users are allowed to upload files within a parent directory which has write permissions.
>     
>     The default value is **NO**.
> 
> *   **anon\_world\_readable_only** - When enabled, anonymous users are only allowed to download world-readable files.
>     
>     The default value is **YES**.
> 
> *   **ftp_username** - Specifies the local user account (listed in **/etc/passwd**) used for the anonymous FTP user. The home directory specified in **/etc/passwd** for the user is the root directory of the anonymous FTP user.
>     
>     The default value is **ftp**.
> 
> *   **no\_anon\_password** - When enabled, the anonymous user is not asked for a password.
>     
>     The default value is **NO**.
> 
> *   **secure\_email\_list_enable** - When enabled, only a specified list of email passwords for anonymous logins are accepted. This is a convenient way to offer limited security to public content without the need for virtual users.
>     
>     Anonymous logins are prevented unless the password provided is listed in **/etc/vsftpd/email_passwords**. The file format is one password per line, with no trailing white spaces.
>     
>     The default value is **NO**.

### vsftp Local User Options

From the same guide:

> The following lists directives which characterize the way local users access the server. To use these options, the **local_enable** directive must be set to **YES**.
> 
> *   **chmod_enable** - When enabled, the FTP command **SITE CHMOD** is allowed for local users. This command allows the users to change the permissions on files.
>     
>     The default value is **YES**.
> 
> *   **chroot\_list\_enable** - When enabled, the local users listed in the file specified in the **chroot\_list\_file** directive are placed in a chroot jail upon log in.
>     
>     If enabled in conjunction with the **chroot\_local\_user** directive, the local users listed in the file specified in the **chroot\_list\_file** directive are not placed in a chroot jail upon log in.
>     
>     The default value is **NO**.
> 
> *   **chroot\_list\_file** - Specifies the file containing a list of local users referenced when the **chroot\_list\_enable** directive is set to **YES**.
>     
>     The default value is **/etc/vsftpd/chroot_list**.
> 
> *   **chroot\_local\_user** - When enabled, local users are change-rooted to their home directories after logging in.
>     
>     The default value is **NO**.
> 
> *   **guest_enable** - When enabled, all non-anonymous users are logged in as the user guest, which is the local user specified in the **guest_username** directive.
>     
>     The default value is **NO**.
> 
> *   **guest_username** - Specifies the username the guest user is mapped to.
>     
>     The default value is **ftp**.
> 
> *   **local_root** - Specifies the directory **vsftpd** changes to after a local user logs in.
>     
>     There is no default value for this directive.
> 
> *   **local_umask** - Specifies the umask value for file creation. Note that the default value is in octal form (a numerical system with a base of eight), which includes a "0" prefix. Otherwise the value is treated as a base-10 integer.
>     
>     The default value is **077**. On Red Hat Enterprise Linux 6, this option is set to **022** in the configuration file.
> 
> *   **passwd\_chroot\_enable** — When enabled in conjunction with the **chroot\_local\_user** directive, **vsftpd** change-roots local users based on the occurrence of the **/./** in the home directory field within **/etc/passwd**.
>     
>     The default value is **NO**.
> 
> *   **user\_config\_dir** - Specifies the path to a directory containing configuration files bearing the name of local system users that contain specific setting for that user. Any directive in the user's configuration file overrides those found in **/etc/vsftpd/vsftpd.conf**.
>     
>     There is no default value for this directive.

### vsftpd Directory Options

From the Deployment Guide:

> The following lists directives which affect directories.
> 
> *   **dirlist_enable** - When enabled, users are allowed to view directory lists.
>     
>     The default value is **YES**.
> 
> *   **dirmessage_enable** - When enabled, a message is displayed whenever a user enters a directory with a message file. This message resides within the current directory. The name of this file is specified in the **message_file** directive and is **.message** by default.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **force\_dot\_files** - When enabled, files beginning with a dot (**.**) are listed in directory listings, with the exception of the **.** and **..** files.
>     
>     The default value is **NO**.
> 
> *   **hide_ids** - When enabled, all directory listings show **ftp** as the user and group for each file.
>     
>     The default value is NO.
> 
> *   **message_file** - Specifies the name of the message file when using the **dirmessage_enable** directive.
>     
>     The default value is **.message**.
> 
> *   **text\_userdb\_names** - When enabled, text usernames and group names are used in place of UID and GID entries. Enabling this option may slow performance of the server.
>     
>     The default value is NO.
> 
> *   **use_localtime** - When enabled, directory listings reveal the local time for the computer instead of GMT.
>     
>     The default value is **NO**.

### vsftpd File Transfer Options

From the same guide:

> The following lists directives which affect directories.
> 
> *   **download_enable** - When enabled, file downloads are permitted.
>     
>     The default value is **YES**.
> 
> *   **chown_uploads** - When enabled, all files uploaded by anonymous users are owned by the user specified in the **chown_username** directive.
>     
>     The default value is **NO**.
> 
> *   **chown_username** - Specifies the ownership of anonymously uploaded files if the **chown_uploads** directive is enabled.
>     
>     The default value is **root**.
> 
> *   **write_enable** - When enabled, FTP commands which can change the file system are allowed, such as **DELE**, **RNFR**, and **STOR**.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.

### vsftpd Logging Options

From the above guide:

> The following lists directives which affect vsftpd's logging behavior.
> 
> *   **dual\_log\_enable** - When enabled in conjunction with **xferlog_enable**, **vsftpd** writes two files simultaneously: a **wu-ftpd**-compatible log to the file specified in the **xferlog_file** directive (**/var/log/xferlog** by default) and a standard **vsftpd** log file specified in the **vsftpd\_log\_file** directive (**/var/log/vsftpd.log** by default).
>     
>     The default value is **NO**.
> 
> *   **log\_ftp\_protocol** - When enabled in conjunction with **xferlog_enable** and with **xferlog\_std\_format** set to **NO**, all **FTP** commands and responses are logged. This directive is useful for debugging.
>     
>     The default value is **NO**.
> 
> *   **syslog_enable** - When enabled in conjunction with **xferlog_enable**, all logging normally written to the standard **vsftpd** log file specified in the **vsftpd\_log\_file** directive (**/var/log/vsftpd.log** by default) is sent to the system logger instead under the **FTPD** facility.
>     
>     The default value is **NO**.
> 
> *   **vsftpd\_log\_file** - Specifies the **vsftpd** log file. For this file to be used, **xferlog_enable** must be enabled and **xferlog\_std\_format** must either be set to **NO** or, if **xferlog\_std\_format** is set to **YES**, **dual\_log\_enable** must be enabled. It is important to note that if **syslog_enable** is set to **YES**, the system log is used instead of the file specified in this directive.
>     
>     The default value is **/var/log/vsftpd.log**.
> 
> *   **xferlog_enable** - When enabled, **vsftpd** logs connections (**vsftpd** format only) and file transfer information to the log file specified in the **vsftpd\_log\_file** directive (**/var/log/vsftpd.log** by default). If **xferlog\_std\_format** is set to **YES**, file transfer information is logged but connections are not, and the log file specified in **xferlog_file** (**/var/log/xferlog** by default) is used instead. It is important to note that both log files and log formats are used if **dual\_log\_enable** is set to **YES**.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **xferlog_file** - Specifies the **wu-ftpd**-compatible log file. For this file to be used, **xferlog_enable** must be enabled and **xferlog\_std\_format** must be set to **YES**. It is also used if **dual\_log\_enable** is set to **YES**.
>     
>     The default value is **/var/log/xferlog**.
> 
> *   **xferlog\_std\_format** - When enabled in conjunction with **xferlog_enable**, only a **wu-ftpd**-compatible file transfer log is written to the file specified in the **xferlog_file** directive (**/var/log/xferlog** by default). It is important to note that this file only logs file transfers and does not log connections to the server.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.

### vsftpd Network Options

From the Deployment Guide:

> The following lists directives which affect how **vsftpd** interacts with the network.
> 
> *   **accept_timeout** - Specifies the amount of time for a client using passive mode to establish a connection.
>     
>     The default value is **60**.
> 
> *   **anon\_max\_rate** - Specifies the maximum data transfer rate for anonymous users in bytes per second.
>     
>     The default value is ****, which does not limit the transfer rate.
> 
> *   **connect\_from\_port_20** - When enabled, **vsftpd** runs with enough privileges to open port 20 on the server during active mode data transfers. Disabling this option allows **vsftpd** to run with less privileges, but may be incompatible with some FTP clients.
>     
>     The default value is **NO**. On Red Hat Enterprise Linux 6, this option is set to **YES** in the configuration file.
> 
> *   **connect_timeout** - Specifies the maximum amount of time a client using *active mode* has to respond to a data connection, in seconds.
>     
>     The default value is **60**.
> 
> *   **data\_connection\_timeout** - Specifies maximum amount of time data transfers are allowed to stall, in seconds. Once triggered, the connection to the remote client is closed.
>     
>     The default value is **300**.
> 
> *   **ftp\_data\_port** - Specifies the port used for active data connections when **connect\_from\_port_20** is set to **YES**.
>     
>     The default value is **20**.
> 
> *   **idle\_session\_timeout** - Specifies the maximum amount of time between commands from a remote client. Once triggered, the connection to the remote client is closed.
>     
>     The default value is **300**.
> 
> *   **listen_address** - Specifies the IP address on which **vsftpd** listens for network connections.
>     
>     There is no default value for this directive.
> 
> *   **listen_address6** - Specifies the **IPv6** address on which **vsftpd** listens for network connections when **listen_ipv6** is set to **YES**.
>     
>     There is no default value for this directive.
> 
> *   **listen_port** - Specifies the port on which **vsftpd** listens for network connections.
>     
>     The default value is **21**.
> 
> *   **local\_max\_rate** - Specifies the maximum rate data is transferred for local users logged into the server in bytes per second.
>     
>     The default value is ****, which does not limit the transfer rate.
> 
> *   **max_clients** - Specifies the maximum number of simultaneous clients allowed to connect to the server when it is running in standalone mode. Any additional client connections would result in an error message.
>     
>     The default value is ****, which does not limit connections.
> 
> *   **max\_per\_ip** - Specifies the maximum of clients allowed to connected from the same source IP address. The default value is 0, which does not limit connections.
> 
> *   **pasv_address** - Specifies the **IP** address for the public facing IP address of the server for servers behind Network Address Translation (NAT) firewalls. This enables **vsftpd** to hand out the correct return address for passive mode connections.
>     
>     There is no default value for this directive.
> 
> *   **pasv_enable** - When enabled, *passive mode* connects are allowed.
>     
>     The default value is **YES**.
> 
> *   **pasv\_max\_port** - Specifies the highest possible port sent to the FTP clients for *passive mode* connections. This setting is used to limit the port range so that firewall rules are easier to create.
>     
>     The default value is ****, which does not limit the highest passive port range. The value must not exceed **65535**.
> 
> *   **pasv\_min\_port** - Specifies the lowest possible port sent to the FTP clients for passive mode connections. This setting is used to limit the port range so that firewall rules are easier to create.
>     
>     The default value is ****, which does not limit the lowest passive port range. The value must not be lower than **1024**.
> 
> *   **pasv_promiscuous** - When enabled, data connections are not checked to make sure they are originating from the same IP address. This setting is only useful for certain types of tunneling.
>     
>     The default value is **NO**.
> 
> *   **port_enable** - When enabled, active mode connects are allowed.
>     
>     The default value is **YES**.

### vsftpd Server Example

So let's go ahead and try this out. Let's install vsftpd on our RH6 machine and connect to it with our RH5 machine. To install vsftpd, run the following on the server:

    [root@rhel1 ~]# yum install vsftpd
    

By default the following configurations are in place:

    [root@rhel1 ~]# grep -vE '^#|^$' /etc/vsftpd/vsftpd.conf 
    anonymous_enable=YES
    local_enable=YES
    write_enable=YES
    local_umask=022
    dirmessage_enable=YES
    xferlog_enable=YES
    connect_from_port_20=YES
    xferlog_std_format=YES
    listen=YES
    pam_service_name=vsftpd
    userlist_enable=YES
    tcp_wrappers=YES
    

Now let's start the service

    [root@rhel1 ~]# service vsftpd start
    Starting vsftpd for vsftpd:  vsftpd
    

Now let's open the firewall:

    [root@rhel1 ~]#iptables -I INPUT 16 -m state --state NEW -m tcp -p tcp --dport 20 -j ACCEPT
    [root@rhel1 ~]#iptables -I INPUT 16 -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables: 
    

One more one, if we are using passive mode, we need to enable the **ip\_conntrack\_ftp** module so it can keep track of the connections that are outside port 20 and 21. To enable that module, edit the **/etc/sysconfig/iptables-config** file and modify the following line:

    [root@rhel1 ~]# grep -i ftp\" /etc/sysconfig/iptables-config 
    IPTABLES_MODULES="ip_conntrack_ftp"
    

Then restart the iptables service:

    [root@rhel1 ~]# service iptables restart
    iptables: Flushing firewall rules: 
    iptables: Setting chains to policy ACCEPT: filter nat 
    iptables: Unloading modules: 
    iptables: Applying firewall rules: 
    iptables: Loading additional modules: ip_conntrack_ftp 
    

Notice the module is automatically loaded. Now on the client side, install an ftp client:

    [root@rhel2 ~]# yum install ftp
    

On the server side, copy a file to the public directory:

    [root@rhel1 ~]# cp install.log /var/ftp/pub/.
    

Now from the client, let's login anonymously, and download that file:

    [root@rhel2 ~]# ftp rhel1
    Connected to rhel1.local.com.
    220 (vsFTPd 2.2.2)
    530 Please login with USER and PASS.
    530 Please login with USER and PASS.
    KERBEROS_V4 rejected as an authentication type
    Name (rhel1:root): anonymous
    331 Please specify the password.
    Password:
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    227 Entering Passive Mode (192,168,2,2,246,23).
    150 Here comes the directory listing.
    drwxr-xr-x    2 0        0            4096 Apr 06 20:41 pub
    226 Directory send OK.
    ftp> cd pub
    250 Directory successfully changed.
    ftp> ls
    227 Entering Passive Mode (192,168,2,2,170,159).
    150 Here comes the directory listing.
    -rw-r--r--    1 0        0            9493 Apr 06 20:41 install.log
    226 Directory send OK.
    ftp> get install.log
    local: install.log remote: install.log
    227 Entering Passive Mode (192,168,2,2,195,73).
    150 Opening BINARY mode data connection for install.log (9493 bytes).
    226 Transfer complete.
    9493 bytes received in 8.8e-05 seconds (1.1e+05 Kbytes/s)
    

I didn't enter any password for the login. On the server if we can check out the **xferlog** and we should see the download of the **install.log** file:

    [root@rhel1 ~]# tail -1 /var/log/xferlog 
    Sun Apr  6 14:43:08 2014 1 192.168.2.3 9493 /pub/install.log b _ o a ? ftp 0 * c
    

And if check the ftpd.log file, we will see successful logins:

    [root@rhel1 ~]# tail -1 /var/log/ftpd.log 
    Sun Apr 6 14:42:55 MDT 2014 from 192.168.2.3
    

Now if we try to login as a specific user, it will fail:

    [root@rhel2 ~]# ftp rhel1
    Connected to rhel1.local.com.
    220 (vsFTPd 2.2.2)
    530 Please login with USER and PASS.
    530 Please login with USER and PASS.
    KERBEROS_V4 rejected as an authentication type
    Name (rhel1:root): user1
    331 Please specify the password.
    Password:
    500 OOPS: cannot change directory:/home/user1
    Login failed.
    ftp>
    

If we check out the messages log, we will see that SELinux is preventing that login:

    [root@rhel1 ~]# tail -1 /var/log/messages
    Apr  6 14:44:00 rhel1 setroubleshoot: SELinux is preventing the ftp daemon from reading users home directories (/home). For complete SELinux messages. run sealert -l 497302a8-2337-4b73-b7f1-078e01df7c66
    

So check out the alert, lets run the suggested command:

    [root@rhel1 ~]# sealert -l 497302a8-2337-4b73-b7f1-078e01df7c66
    
    Summary:
    
    SELinux is preventing the ftp daemon from reading users home directories
    (/home).
    
    Detailed Description:
    
    SELinux has denied the ftp daemon access to users home directories (/home).
    Someone is attempting to login via your ftp daemon to a user account. If you
    only setup ftp to allow anonymous ftp, this could signal an intrusion attempt.
    
    Allowing Access:
    
    If you want ftp to allow users access to their home directories you need to turn
    on the ftp_home_dir boolean: "setsebool -P ftp_home_dir=1"
    
    Fix Command:
    
    setsebool -P ftp_home_dir=1
    
    Additional Information:
    
    Source Context                unconfined_u:system_r:ftpd_t:s0-s0:c0.c1023
    Target Context                system_u:object_r:home_root_t:s0
    Target Objects                /home [ dir ]
    Source                        vsftpd
    Source Path                   /usr/sbin/vsftpd
    Port                          <Unknown>
    Host                          rhel1.local.com
    Source RPM Packages           vsftpd-2.2.2-6.el6_0.1
    Target RPM Packages           filesystem-2.4.30-2.1.el6
    Policy RPM                    selinux-policy-3.7.19-93.el6
    Selinux Enabled               True
    Policy Type                   targeted
    Enforcing Mode                Enforcing
    Plugin Name                   ftp_home_dir
    Host Name                     rhel1.local.com
    Platform                      Linux rhel1.local.com 2.6.32-131.0.15.el6.i686 #1
                                  SMP Tue May 10 15:42:28 EDT 2011 i686 i686
    Alert Count                   1
    First Seen                    Sun Apr  6 14:43:56 2014
    Last Seen                     Sun Apr  6 14:43:56 2014
    Local ID                      497302a8-2337-4b73-b7f1-078e01df7c66
    Line Numbers                  
    
    Raw Audit Messages            
    
    node=rhel1.local.com type=AVC msg=audit(1396817036.502:2803): avc:  denied  { search } for  pid=22954 comm="vsftpd" name="home" dev=dm-0 ino=388614 scontext=unconfined_u:system_r:ftpd_t:s0-s0:c0.c1023 tcontext=system_u:object_r:home_root_t:s0 tclass=dir
    
    node=rhel1.local.com type=SYSCALL msg=audit(1396817036.502:2803): arch=40000003 syscall=12 success=no exit=-13 a0=105b648 a1=1f4 a2=cd133c a3=16 items=0 ppid=22945 pid=22954 auid=0 uid=0 gid=0 euid=500 suid=500 fsuid=500 egid=500 sgid=500 fsgid=500 tty=(none) ses=381 comm="vsftpd" exe="/usr/sbin/vsftpd" subj=unconfined_u:system_r:ftpd_t:s0-s0:c0.c1023 key=(null)
    

Looks like the fix is included in the alert, so let's run the suggested fix:

    [root@rhel1 ~]# setsebool -P ftp_home_dir=1
    

Now trying to connect as the user again:

    [root@rhel2 ~]# ftp rhel1
    Connected to rhel1.local.com.
    220 (vsFTPd 2.2.2)
    530 Please login with USER and PASS.
    530 Please login with USER and PASS.
    KERBEROS_V4 rejected as an authentication type
    Name (rhel1:root): user1
    331 Please specify the password.
    Password:
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    227 Entering Passive Mode (192,168,2,2,193,177).
    150 Here comes the directory listing.
    -rw-r--r--    1 500      500             0 Feb 08  2013 foo.txt
    -rwxr--r--    1 500      500         29914 Mar 29 22:18 install.log
    drwxrwxr-x    2 500      500          4096 Mar 29 22:23 l
    -rw-r--r--    1 500      500             0 Mar 29 22:23 test
    226 Directory send OK.
    ftp> !ls
    anaconda-ks.cfg  Desktop  install.log  install.log.syslog  repo
    ftp> put anaconda-ks.cfg
    local: anaconda-ks.cfg remote: anaconda-ks.cfg
    227 Entering Passive Mode (192,168,2,2,244,100).
    150 Ok to send data.
    226 Transfer complete.
    1308 bytes sent in 8e-05 seconds (1.6e+04 Kbytes/s)
    ftp> 
    

And we are able to upload a file as well. And here is the **xferlog** entry for our upload:

    [root@rhel1 ~]# tail -1 /var/log/xferlog 
    Sun Apr  6 14:54:18 2014 1 192.168.2.3 1308 /home/user1/anaconda-ks.cfg b _ i r user1 ftp 0 * c
    

Here are all the FTP related SELinux Booleans:

    [root@rhel1 log]# semanage boolean -l | grep ftp | grep -vE 'sftp|tftp'
    ftp_home_dir                   -> on    Allow ftp to read and write files in the user home directories
    allow_ftpd_full_access         -> off   Allow ftp servers to login to local users and read/write all files on the system, governed by DAC.
    allow_ftpd_use_nfs             -> off   Allow ftp servers to use nfs used for public file transfer services.
    allow_ftpd_anon_write          -> on    Allow ftp servers to upload files,  used for public file transfer services. Directories must be labeled public_content_rw_t.
    allow_ftpd_use_cifs            -> off   Allow ftp servers to use cifs used for public file transfer services.
    ftpd_connect_db                -> off   Allow ftp servers to use connect to mysql database
    httpd_enable_ftp_server        -> off   Allow httpd to act as a FTP server by listening on the ftp port.
    

### FTP and SELinux

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Confined_Services/Red_Hat_Enterprise_Linux-6-Managing_Confined_Services-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Confined_Services/Red_Hat_Enterprise_Linux-6-Managing_Confined_Services-en-US.pdf']);">Managing Confined Services</a>

> The **vsftpd** FTP daemon runs confined by default. SELinux policy defines how **vsftpd** interacts with files, processes, and with the system in general. For example, when an authenticated user logs in via FTP, they cannot read from or write to files in their home directories: SELinux prevents **vsftpd** from accessing user home directories by default. Also, by default, **vsftpd** does not have access to NFS or CIFS volumes, and anonymous users do not have write access, even if such write access is configured in **/etc/vsftpd/vsftpd.conf**. Booleans can be enabled to allow the previously mentioned access.

#### FTP SELinux Types

From the same guide:

> By default, anonymous users have read access to files in **/var/ftp/** when they log in via FTP. This directory is labeled with the **public\_content\_t** type, allowing only read access, even if write access is configured in **/etc/vsftpd/vsftpd.conf**. The **public\_content\_t** type is accessible to other services, such as Apache HTTP Server, Samba, and NFS.
> 
> Use one of the following types to share files through FTP:
> 
> *   **public\_content\_t** - Label files and directories you have created with the public\_content\_t type to share them read-only through **vsftpd**. Other services, such as Apache HTTP Server, Samba, and NFS, also have access to files labeled with this type. Files labeled with the **public\_content\_t** type cannot be written to, even if Linux permissions allow write access. If you require write access, use the **public\_content\_rw_t** type.
> *   **public\_content\_rw_t** - Label files and directories you have created with the **public\_content\_rw_t** type to share them with read and write permissions through vsftpd. Other services, such as Apache HTTP Server, Samba, and NFS, also have access to files labeled with this type. Remember that Booleans for each service must be enabled before they can write to files labeled with this type.

#### FTP SELinux Booleans

From the above guide:

> SELinux is based on the least level of access required for a service to run. Services can be run in a variety of ways; therefore, you need to specify how you run your services. > Use the following Booleans to set up SELinux:
> 
> *   **allow\_ftpd\_anon_write** - When disabled, this Boolean prevents **vsftpd** from writing to files and directories labeled with the **public\_content\_rw_t** type. Enable this Boolean to allow users to upload files via FTP. The directory where files are uploaded to must be labeled with the **public\_content\_rw_t** type and Linux permissions set accordingly.
> *   **allow\_ftpd\_full_access** - When this Boolean is on, only Linux (DAC) permissions are used to control access, and authenticated users can read and write to files that are not labeled with the **public\_content\_t** or **public\_content\_rw_t** types.
> *   **allow\_ftpd\_use_cifs** - Having this Boolean enabled allows **vsftpd** to access files and directories labeled with the **cifs_t** type; therefore, having this Boolean enabled allows you to share file systems mounted via Samba through **vsftpd**.
> *   **allow\_ftpd\_use_nfs** - Having this Boolean enabled allows **vsftpd** to access files and directories labeled with the **nfs_t** type; therefore, having this Boolean enabled allows you to share file systems mounted via NFS through **vsftpd**.
> *   **ftp\_home\_dir** - Having this Boolean enabled allows authenticated users to read and write to files in their home directories. When this Boolean is off, attempting to download a file from a home directory results in an error such as **550 Failed to open file**. An SELinux denial is logged.
> *   **ftpd\_connect\_db** - Allow FTP daemons to initiate a connection to a database.
> *   **httpd\_enable\_ftp_server** - Allow httpd to listen on the FTP port and act as a FTP server.
> *   **tftp\_anon\_write** - Having this Boolean enabled allows TFTP access to a public directory, such as an area reserved for common files that otherwise has no special access restrictions.

#### FTP SELinux Configuration Example

From the Managing Confined Services guide:

> The following example creates an FTP site that allows a dedicated user to upload files. It creates the directory structure and the required SELinux configuration changes:
> 
> 1.  Run the `setsebool ftp_home_dir=1` command as the root user to enable access to FTP home directories.
> 2.  Run the `mkdir -p /myftp/pub` command as the root user to create a new top-level directory.
> 3.  Set Linux permissions on the **/myftp/pub/** directory to allow a Linux user write access. This example changes the owner and group from root to owner **user1** and group root. Replace **user1** with the user you want to give write access to:
>     
>         ~]# chown user1:root /myftp/pub
>         ~]# chmod 775 /myftp/pub
>         
>     
>     The **chown** command changes the owner and group permissions. The **chmod** command changes the mode, allowing the **user1** user read, write, and execute permissions, and members of the root group read, write, and execute permissions. Everyone else has read and execute permissions: this is required to allow the Apache HTTP Server to read files from this directory.
> 
> 4.  When running SELinux, files and directories must be labeled correctly to allow access. Setting Linux permissions is not enough. Files labeled with the **public\_content\_t** type allow them to be read by FTP, Apache HTTP Server, Samba, and rsync. Files labeled with the **public\_content\_rw_t** type can be written to by FTP. Other services, such as Samba, require Booleans to be set before they can write to files labeled with the **public\_content\_rw_t** type. Label the top-level directory (**/myftp/**) with the **public\_content\_t** type, to prevent copied or newly-created files under **/myftp/** from being written to or modified by services. Run the following command as the root user to add the label change to file-context configuration:
>     
>         ~]# semanage fcontext -a -t public_content_t /myftp
>         
> 
> 5.  Run the `restorecon -R -v /myftp`/ command to apply the label change:
>     
>         ~]# restorecon -R -v /myftp/
>         restorecon reset /myftp context unconfined_u:object_r:default_t:s0->system_u:object_r:public_content_t:s0
>         
> 
> 6.  Confirm **/myftp** is labeled with the **public\_content\_t** type, and **/myftp/pub/** is labeled with the **default_t** type:
>     
>         ~]$ ls -dZ /myftp/
>         drwxr-xr-x. root root system_u:object_r:public_content_t:s0 /myftp/
>         ~]$ ls -dZ /myftp/pub/
>         drwxrwxr-x. user1 root unconfined_u:object_r:default_t:s0 /myftp/pub/
>         
> 
> 7.  FTP must be allowed to write to a directory before users can upload files via FTP. SELinux allows FTP to write to directories labeled with the **public\_content\_rw_t** type. This example uses **/myftp/pub/** as the directory FTP can write to. Run the following command as the root user to add the label change to file-context configuration:
>     
>         ~]# semanage fcontext -a -t public_content_rw_t "/myftp/pub(/.*)?"
>         
> 
> 8.  Run the `restorecon -R -v /myftp/pub` command as the root user to apply the label change:
>     
>         ~]# restorecon -R -v /myftp/pub
>         restorecon reset /myftp/pub context system_u:object_r:default_t:s0->system_u:object_r:public_content_rw_t:s0
>         
> 
> 9.  The **allow\_ftpd\_anon_write** Boolean must be on to allow vsftpd to write to files that are labeled with the **public\_content\_rw_t** type. Run the following command as the root user to enable this Boolean:
>     
>         ~]# setsebool -P allow_ftpd_anon_write on
>         
>     
>     Do not use the -P option if you do not want changes to persist across reboots.
> 
> The following example demonstrates logging in via FTP and uploading a file. This example uses the **user1** user from the previous example, where user1 is the dedicated owner of the **/myftp/pub/** directory:
> 
> 1.  Run the **cd ~/** command to change into your home directory. Then, run the **mkdir myftp** command to create a directory to store files to upload via FTP.
> 2.  Run the **cd ~/myftp** command to change into the **~/myftp/** directory. In this directory, create an **ftpupload** file. Copy the following contents into this file:
>     
>         File upload via FTP from a home directory.
>         
> 
> 3.  Run the **getsebool allow\_ftpd\_anon_write** command to confirm the **allow\_ftpd\_anon_write** Boolean is on:
>     
>         ~]$ getsebool allow_ftpd_anon_write
>         allow_ftpd_anon_write --> on
>         
>     
>     If this Boolean is off, run the **setsebool -P allow\_ftpd\_anon_write** on command as the root user to enable it. Do not use the **-P** option if you do not want the change to persist across reboots.
> 
> 4.  Run the **service vsftpd start** command as the root user to start vsftpd:
>     
>         ~]# service vsftpd start
>         Starting vsftpd for vsftpd:                                [  OK  ]
>         
> 
> Run the **ftp localhost** command. When prompted for a user name, enter the user name of the user who has write access, then, enter the correct password for that user:
> 
>         ~]$ ftp localhost
>         Connected to localhost (127.0.0.1).
>         220 (vsFTPd 2.1.0)
>         Name (localhost:username):
>         331 Please specify the password.
>         Password: Enter the correct password
>         230 Login successful.
>         Remote system type is UNIX.
>         Using binary mode to transfer files.
>         ftp> cd myftp
>         250 Directory successfully changed.
>         ftp> put ftpupload 
>         local: ftpupload remote: ftpupload
>         227 Entering Passive Mode (127,0,0,1,241,41).
>         150 Ok to send data.
>         226 File receive OK.
>         ftp> 221 Goodbye.
>     
> 
> The upload succeeds as the **allow\_ftpd\_anon_write** Boolean is enabled.

