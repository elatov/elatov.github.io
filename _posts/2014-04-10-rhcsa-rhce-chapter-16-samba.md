---
title: 'RHCSA and RHCE Chapter 16 - Samba'
author: Karim Elatov
layout: post
permalink: /2014/04/rhcsa-rhce-chapter-16-samba/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2601621922
categories:
  - Certifications
  - OS
  - RHCSA and RHCE
tags:
  - rhcsa_and_rhce
  - samba
---
## Samba

From the [Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> Samba is an open source implementation of the Server Message Block (SMB) protocol. It allows the networking of Microsoft Windows, Linux, UNIX, and other operating systems together, enabling access to Windows-based file and printer shares. Samba's use of SMB allows it to appear as a Windows server to Windows clients.

### Samba Features

From the same guide:

> Samba is a powerful and versatile server application. Even seasoned system administrators must know its abilities and limitations before attempting installation and configuration.
>
> What Samba can do:
>
> *   Serve directory trees and printers to Linux, UNIX, and Windows clients
> *   Assist in network browsing (with or without NetBIOS)
> *   Authenticate Windows domain logins
> *   Provide Windows Internet Name Service (WINS) name server resolution
> *   Act as a Windows NT-style Primary Domain Controller (PDC)
> *   Act as a Backup Domain Controller (BDC) for a Samba-based PDC
> *   Act as an Active Directory domain member server
> *   Join a Windows NT/2000/2003/2008 PDC
>
> What Samba cannot do:
>
> *   Act as a BDC for a Windows PDC (and vice versa)
> *   Act as an Active Directory domain controller

### Samba Daemons

From the above guide:

> Samba is comprised of three daemons (**smbd**, **nmbd**, and **winbindd**). Three services (**smb**, **nmb**, and **winbind**) control how the daemons are started, stopped, and other service-related features. These services act as different init scripts. Each daemon is listed in detail below, as well as which specific service has control over it.
>
> *   **smbd** - The **smbd** server daemon provides file sharing and printing services to Windows clients. In addition, it is responsible for user authentication, resource locking, and data sharing through the **SMB** protocol. The default ports on which the server listens for SMB traffic are TCP ports **139** and **445**. The **smbd** daemon is controlled by the **smb** service.
> *   **nmbd** - The **nmbd** server daemon understands and replies to NetBIOS name service requests such as those produced by SMB/Common Internet File System (**CIFS**) in Windows-based systems. These systems include Windows 95/98/ME, Windows NT, Windows 2000, Windows XP, and LanManager clients. It also participates in the browsing protocols that make up the Windows Network Neighborhood view. The default port that the server listens to for **NMB** traffic is **UDP** port **137**. The **nmbd** daemon is controlled by the **nmb** service.
> *   **winbindd** - The **winbind** service resolves user and group information on a server running Windows NT, 2000, 2003 or Windows Server 2008. This makes Windows user / group information understandable by UNIX platforms. This is achieved by using Microsoft RPC calls, Pluggable Authentication Modules (PAM), and the Name Service Switch (NSS). This allows Windows NT domain users to appear and operate as UNIX users on a UNIX machine. Though bundled with the Samba distribution, the **winbind** service is controlled separately from the **smb** service. The **winbindd** daemon is controlled by the **winbind** service and does not require the **smb** service to be started in order to operate. **winbindd** is also used when Samba is an Active Directory member, and may also be used on a Samba domain controller (to implement nested groups and/or interdomain trust).

### Configuring a Samba Server

From the deployment Guide:

> The default configuration file (**/etc/samba/smb.conf**) allows users to view their home directories as a Samba share. It also shares all printers configured for the system as Samba shared printers. In other words, you can attach a printer to the system and print to it from the Windows machines on your network.
>
> Samba uses **/etc/samba/smb.conf** as its configuration file. If you change this configuration file, the changes do not take effect until you restart the Samba daemon with the following command, as root:
>
>     ~]# service smb restart
>
>
> To specify the Windows workgroup and a brief description of the Samba server, edit the following lines in your **/etc/samba/smb.conf** file:
>
>     workgroup = WORKGROUPNAME
>     server string = BRIEF COMMENT ABOUT SERVER
>
>
> Replace **WORKGROUPNAME** with the name of the Windows workgroup to which this machine should belong. The **BRIEF COMMENT ABOUT SERVER** is optional and is used as the Windows comment about the Samba system.
>
> To create a Samba share directory on your Linux system, add the following section to your **/etc/samba/smb.conf** file (after modifying it to reflect your needs and your system):
>
>     [sharename]
>     comment = Insert a comment here
>     path = /home/share/
>     valid users = tfox carole
>     public = no
>     writable = yes
>     printable = no
>     create mask = 0765
>
>
> The above example allows the users **tfox** and **carole** to *read* and *write* to the directory **/home/share**, on the Samba server, from a Samba client.

### Samba Server Types

From the same guide:

> Samba configuration is straightforward. All modifications to Samba are done in the **/etc/samba/smb.conf** configuration file. Although the default **smb.conf** file is well documented, it does not address complex topics such as LDAP, Active Directory, and the numerous domain controller implementations.

#### Samba Stand-alone Server

From the above guide:

> A stand-alone server can be a workgroup server or a member of a workgroup environment. A stand-alone server is not a domain controller and does not participate in a domain in any way. The following examples include several anonymous share-level security configurations and one user-level security configuration
>
> **Anonymous Read-Only**
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement anonymous read-only file sharing. The **security = share** parameter makes a share anonymous. Note, security levels for a single Samba server cannot be mixed. The **security** directive is a global Samba parameter located in the **[global]** configuration section of the **/etc/samba/smb.conf** file.
>
>     [global]
>     workgroup = DOCS
>     netbios name = DOCS_SRV
>     security = share
>     [data]
>     comment = Documentation Samba Server
>     path = /export
>     read only = Yes
>     guest only = Yes
>
>
> **Anonymous Read/Write**
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement anonymous read/write file sharing. To enable anonymous read/write file sharing, set the **read only** directive to **no**. The **force user** and **force group** directives are also added to enforce the ownership of any newly placed files specified in the share.
>
>     [global]
>     workgroup = DOCS
>     netbios name = DOCS_SRV
>     security = share
>     [data]
>     comment = Data
>     path = /export
>     force user = docsbot
>     force group = users
>     read only = No
>     guest ok = Yes
>
>
> **Anonymous Print Server**
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement an anonymous print server. Setting **browseable** to **no** as shown does not list the printer in Windows **Network Neighborhood**. Although hidden from browsing, configuring the printer explicitly is possible. By connecting to **DOCS_SRV** using NetBIOS, the client can have access to the printer if the client is also part of the **DOCS** workgroup. It is also assumed that the client has the correct local printer driver installed, as the **use client driver** directive is set to **Yes**. In this case, the Samba server has no responsibility for sharing printer drivers to the client.
>
>     [global]
>     workgroup = DOCS
>     netbios name = DOCS_SRV
>     security = share
>     printcap name = cups
>     disable spools= Yes
>     show add printer wizard = No
>     printing = cups
>     [printers]
>     comment = All Printers
>     path = /var/spool/samba
>     guest ok = Yes
>     printable = Yes
>     use client driver = Yes
>     browseable = Yes
>

#### Samba as a Domain Member Server

From the Deployment Guide:

> A domain member, while similar to a stand-alone server, is logged into a domain controller (either Windows or Samba) and is subject to the domain's security rules. An example of a domain member server would be a departmental server running Samba that has a machine account on the Primary Domain Controller (PDC). All of the department's clients still authenticate with the PDC, and desktop profiles and all network policy files are included. The difference is that the departmental server has the ability to control printer and network shares.
>
> **Active Directory Domain Member Server**
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement an Active Directory domain member server. In this example, Samba authenticates users for services being run locally but is also a client of the Active Directory. Ensure that your kerberos **realm** parameter is shown in all caps (for example **realm = EXAMPLE.COM**). Since Windows 2000/2003/2008 requires Kerberos for Active Directory authentication, the **realm** directive is required. If Active Directory and Kerberos are running on different servers, the password server directive may be required to help the distinction.
>
>     [global]
>     realm = EXAMPLE.COM
>     security = ADS
>     encrypt passwords = yes
>     # Optional. Use only if Samba cannot determine the Kerberos server automatically.
>     password server = kerberos.example.com
>
>
> In order to join a member server to an Active Directory domain, the following steps must be completed:
>
> *   Configuration of the **/etc/samba/smb.conf** file on the member server
> *   Configuration of Kerberos, including the **/etc/krb5.conf** file, on the member server
> *   Creation of the machine account on the Active Directory domain server
> *   Association of the member server to the Active Directory domain
>
> To create the machine account and join the Windows 2000/2003/2008 Active Directory, Kerberos must first be initialized for the member server wishing to join the Active Directory domain. To create an administrative Kerberos ticket, type the following command as root on the member server:
>
>     kinit administrator@EXAMPLE.COM
>
>
> The **kinit** command is a Kerberos initialization script that references the Active Directory administrator account and Kerberos realm. Since Active Directory requires Kerberos tickets, **kinit** obtains and caches a Kerberos ticket-granting ticket for client/server authentication.
>
> To join an Active Directory server (windows1.example.com), type the following command as root on the member server:
>
>     net ads join -S windows1.example.com -U administrator%password
>
>
> Since the machine **windows1** was automatically found in the corresponding Kerberos realm (the **kinit** command succeeded), the **net** command connects to the Active Directory server using its required administrator account and password. This creates the appropriate machine account on the Active Directory and grants permissions to the Samba domain member server to join the domain.
>
> **Windows NT4-based Domain Member Server**
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement a Windows NT4-based domain member server. Becoming a member server of an NT4-based domain is similar to connecting to an Active Directory. The main difference is NT4-based domains do not use Kerberos in their authentication method, making the **/etc/samba/smb.conf** file simpler. In this instance, the Samba member server functions as a pass through to the NT4-based domain server.
>
>     [global]
>     workgroup = DOCS
>     netbios name = DOCS_SRV
>     security = domain
>     [homes]
>     comment = Home Directories
>     valid users = %S
>     read only = No
>     browseable = No
>     [public]
>     comment = Data
>     path = /export
>     force user = docsbot
>     force group = users
>     guest ok = Yes
>
>
> Having Samba as a domain member server can be useful in many situations. There are times where the Samba server can have other uses besides file and printer sharing. It may be beneficial to make Samba a domain member server in instances where Linux-only applications are required for use in the domain environment. Administrators appreciate keeping track of all machines in the domain, even if not Windows-based. In the event the Windows-based server hardware is deprecated, it is quite easy to modify the **/etc/samba/smb.conf** file to convert the server to a Samba-based PDC. If Windows NT-based servers are upgraded to Windows 2000/2003/2008, the **/etc/samba/smb.conf** file is easily modifiable to incorporate the infrastructure change to Active Directory if needed.
>
> After configuring the **/etc/samba/smb.conf** file, join the domain before starting Samba by typing the following command as root:
>
>     net rpc join -U administrator%password
>
>
> Note that the **-S** option, which specifies the domain server hostname, does not need to be stated in the **net rpc join** command. Samba uses the hostname specified by the workgroup directive in the **/etc/samba/smb.con**f file instead of it being stated explicitly.

#### Samba as a Domain Controller

From the the deployment guide:

> A domain controller in Windows NT is functionally similar to a Network Information Service (NIS) server in a Linux environment. Domain controllers and NIS servers both host user/group information databases as well as related services. Domain controllers are mainly used for security, including the authentication of users accessing domain resources. The service that maintains the user/group database integrity is called the Security Account Manager (**SAM**). The SAM database is stored differently between Windows and Linux Samba-based systems, therefore SAM replication cannot be achieved and platforms cannot be mixed in a PDC/BDC environment.
>
> In a Samba environment, there can be only one PDC and zero or more BDCs.
>
> **Primary Domain Controller (PDC) using tdbsam**
> The simplest and most common implementation of a Samba PDC uses the new default **tdbsam** password database back end. Replacing the aging **smbpasswd** back end. The **passdb backend** directive controls which back end is to be used for the PDC.
>
> The following **/etc/samba/smb.conf** file shows a sample configuration needed to implement a **tdbsam** password database back end.
>
>     [global]
>     workgroup = DOCS
>     netbios name = DOCS_SRV
>     passdb backend = tdbsam
>     security = user
>     add user script = /usr/sbin/useradd -m "%u"
>     delete user script = /usr/sbin/userdel -r "%u"
>     add group script = /usr/sbin/groupadd "%g"
>     delete group script = /usr/sbin/groupdel "%g"
>     add user to group script = /usr/sbin/usermod -G "%g" "%u"
>     add machine script = /usr/sbin/useradd -s /bin/false -d /dev/null  -g machines "%u"
>     # The following specifies the default logon script
>     # Per user logon scripts can be specified in the user
>     # account using pdbedit logon script = logon.bat
>     # This sets the default profile path.
>     # Set per user paths with pdbedit
>     logon drive = H:
>     domain logons = Yes
>     os level = 35
>     preferred master = Yes
>     domain master = Yes
>     [homes]
>       comment = Home Directories
>       valid users = %S
>       read only = No
>     [netlogon]
>       comment = Network Logon Service
>       path = /var/lib/samba/netlogon/scripts
>       browseable = No
>       read only = No
>     # For profiles to work, create a user directory under the
>     # path shown.
>     mkdir -p /var/lib/samba/profiles/john
>     [Profiles]
>       comment = Roaming Profile Share
>       path = /var/lib/samba/profiles
>       read only = No
>       browseable = No
>       guest ok = Yes
>       profile acls = Yes
>     # Other resource shares ... ...
>
>
> To provide a functional PDC system which uses the **tdbsam** follow these steps:
>
> 1.  Use a configuration of the **smb.conf** file as shown in the example above.
> 2.  Add the root user to the Samba password database.
>
>         ~]# smbpasswd -a root
>         Provide the password here.
>
>
> 3.  Start the **smb** service.
>
> 4.  Make sure all **profile**, **user**, and **netlogon** directories are created.
>
> 5.  Add groups that users can be members of.
>
>         ~]# groupadd -f users
>         ~]# groupadd -f nobody
>         ~]# groupadd -f ntadmins
>
>
> 6.  Associate the UNIX groups with their respective Windows groups.
>
>         ~]# net groupmap add ntgroup="Domain Users" unixgroup=users
>         ~]# net groupmap add ntgroup="Domain Guests" unixgroup=nobody
>         ~]# net groupmap add ntgroup="Domain Admins" unixgroup=ntadmins
>
>
> 7.  Grant access rights to a user or a group. For example, to grant the right to add client machines to the domain on a Samba domain controller, to the members to the Domain Admins group, execute the following command:
>
>         ~]# net rpc rights grant 'DOCS\Domain Admins' SetMachineAccountPrivilege -S PDC -U root
>
>
> Keep in mind that Windows systems prefer to have a primary group which is mapped to a domain group such as Domain Users.
>
> Windows groups and users use the same namespace thus not allowing the existence of a group and a user with the same name like in UNIX.

### Samba Security Modes

From the same guide:

> There are only two types of security modes for Samba, **share-level** and **user-level**, which are collectively known as security levels. Share-level security can only be implemented in one way, while user-level security can be implemented in one of four different ways. The different ways of implementing a security level are called security modes.

#### Samba User-Level Security

From the Deployment guide:

> User-level security is the default setting for Samba. Even if the **security = user** directive is not listed in the **/etc/samba/smb.conf** file, it is used by Samba. If the server accepts the client's username/password, the client can then mount multiple shares without specifying a password for each instance. Samba can also accept session-based username/password requests. The client maintains multiple authentication contexts by using a unique UID for each logon.
>
> In the **/etc/samba/smb.conf** file, the **security = user** directive that sets user-level security is:
>
>     [GLOBAL]
>     ...
>     security = user
>     ...
>
>
> **Domain Security Mode (User-Level Security)**
> In domain security mode, the Samba server has a machine account (domain security trust account) and causes all authentication requests to be passed through to the domain controllers. The Samba server is made into a domain member server by using the following directives in the **/etc/samba/smb.conf** file:
>
>     [GLOBAL]
>     ...
>     security = domain
>     workgroup = MARKETING
>     ...
>
>
> **Active Directory Security Mode (User-Level Security)**
> If you have an Active Directory environment, it is possible to join the domain as a native Active Directory member. Even if a security policy restricts the use of NT-compatible authentication protocols, the Samba server can join an ADS using Kerberos. Samba in Active Directory member mode can accept Kerberos tickets.
>
> In the /etc/samba/smb.conf file, the following directives make Samba an Active Directory member server:
>
>     [GLOBAL]
>     ...
>     security = ADS
>     realm = EXAMPLE.COM
>     password server = kerberos.example.com
>     ...
>
>
> **Server Security Mode (User-Level Security)** Server security mode was previously used when Samba was not capable of acting as a domain member server.
>
> It is highly recommended to not use this mode since there are numerous security drawbacks.
>
> In the **/etc/samba/smb.conf**, the following directives enable Samba to operate in server security mode:
>
>     [GLOBAL]
>     ...
>     encrypt passwords = Yes
>     security = server
>     password server = "NetBIOS_of_Domain_Controller"
>     ...
>

#### Samba Share-Level Security

From the above guide:

> With share-level security, the server accepts only a password without an explicit username from the client. The server expects a password for each share, independent of the username. There have been recent reports that Microsoft Windows clients have compatibility issues with share-level security servers. Samba developers strongly discourage use of share-level security.
>
> In the **/etc/samba/smb.conf** file, the **security = share** directive that sets share-level security is:
>
>     [GLOBAL]
>     ...
>     security = share
>     ...
>

### Samba Account Information Databases

From the same guide:

> The latest release of Samba offers many new features including new password database back ends not previously available. Samba version 3.0.0 fully supports all databases used in previous versions of Samba. However, although supported, many back ends may not be suitable for production use.
>
> The following is a list different back ends you can use with Samba. Other back ends not listed here may also be available.
>
> *   **Plain Text** - Plain text back ends are nothing more than the **/etc/passwd** type back ends. With a plain text back end, all usernames and passwords are sent unencrypted between the client and the Samba server. This method is very insecure and is not recommended for use by any means. It is possible that different Windows clients connecting to the Samba server with plain text passwords cannot support such an authentication method.
> *   **smbpasswd** - A popular back end used in previous Samba packages, the **smbpasswd** back end utilizes a plain ASCII text layout that includes the MS Windows LanMan and NT account, and encrypted password information. The **smbpasswd** back end lacks the storage of the Windows NT/2000/2003 SAM extended controls. The **smbpasswd** back end is not recommended because it does not scale well or hold any Windows information, such as RIDs for NT-based groups. The **tdbsam** back end solves these issues for use in a smaller database (250 users), but is still not an enterprise-class solution.
> *   **ldapsam_compat** - The **ldapsam_compat** back end allows continued OpenLDAP support for use with upgraded versions of Samba. This option is normally used when migrating to Samba 3.0.
> *   **tdbsam** - The new default **tdbsam** password back end provides an ideal database back end for local servers, servers that do not need built-in database replication, and servers that do not require the scalability or complexity of LDAP. The **tdbsam** back end includes all of the **smbpasswd** database information as well as the previously-excluded SAM information. The inclusion of the extended SAM data allows Samba to implement the same account and system access controls as seen with Windows NT/2000/2003/2008-based systems.
>
>     The **tdbsam** back end is recommended for 250 users at most. Larger organizations should require Active Directory or LDAP integration due to scalability and possible network infrastructure concerns.
>
> *   **ldapsam** - The **ldapsam** back end provides an optimal distributed account installation method for Samba. LDAP is optimal because of its ability to replicate its database to any number of servers such as the **Red Hat Directory Server** or an **OpenLDAP Server**. LDAP databases are light-weight and scalable, and as such are preferred by large enterprises.
>
>     If you are upgrading from a previous version of Samba to 3.0, note that the OpenLDAP schema file (**/usr/share/doc/samba-<version>/LDAP/samba.schema</version>**) and the Red Hat Directory Server schema file (**/usr/share/doc/samba-<version>/LDAP/samba-schema-FDS.ldif</version>**) have changed. These files contain the attribute syntax definitions and objectclass definitions that the **ldapsam** back end needs in order to function properly.
>
>     As such, if you are using the ldapsam back end for your Samba server, you will need to configure **slapd** to include one of these schema file.

### Stand-alone Samba Server Example

So let's go ahead and setup our RH6 machine to be a stand-alone samba server. First let's install the necessary package:

    [root@rhel1 ~]# yum install samba


By default we have the following configuration:

    [root@rhel1 ~]# grep -vE '^#|^;|^[^I]$|^[^I]#' /etc/samba/smb.conf
    [global]
        workgroup =MYGROUP
        server string = Samba Server Version %v
        log file = /var/log/samba/log.%m
        max log size = 50
        security = user
        passdb backend = tdbsam
        load printers = yes
        cups options = raw

    [homes]
        comment = Home Directories
        browseable = no
        writable = yes
    [printers]
        comment = All Printers
        path = /var/spool/samba
        browseable = no
        guest ok = no
        writable = no
        printable = yes


We can also use **testparm** to list the configuration:

    [root@rhel1 ~]# testparm
    Load smb config files from /etc/samba/smb.conf
    rlimit_max: rlimit_max (1024) below minimum Windows limit (16384)
    Processing section "[homes]"
    Processing section "[printers]"
    Loaded services file OK.
    Server role: ROLE_STANDALONE
    Press enter to see a dump of your service definitions

    [global]
        workgroup = MYGROUP
        server string = Samba Server Version %v
        log file = /var/log/samba/log.%m
        max log size = 50
        cups options = raw

    [homes]
        comment = Home Directories
        read only = No
        browseable = No

    [printers]
        comment = All Printers
        path = /var/spool/samba
        printable = Yes
        browseable = No


The default shares the home directories which is good. I renamed my workgroup and set the netbios name in the configuration. You can list all of the settings, by running **testparm** with a **-v** parameter:

    [root@rhel1 ~]# testparm -v
    Load smb config files from /etc/samba/smb.conf
    rlimit_max: rlimit_max (1024) below minimum Windows limit (16384)
    Processing section "[homes]"
    Processing section "[printers]"
    Loaded services file OK.
    Server role: ROLE_STANDALONE
    Press enter to see a dump of your service definitions

    [global]
        dos charset = CP850
        unix charset = UTF-8
        display charset = LOCALE
        workgroup = LOCAL
        realm =
        netbios name = RHEL1
        netbios aliases =
        netbios scope =
        server string = Samba Server Version %v
        interfaces =
        bind interfaces only = No
        security = USER
        auth methods =
        encrypt passwords = Yes
        update encrypted = No
        client schannel = Auto
        server schannel = Auto
        allow trusted domains = Yes
        map to guest = Never
        null passwords = No
        obey pam restrictions = No
        password server = *
        smb passwd file = /var/lib/samba/private/smbpasswd
        private dir = /var/lib/samba/private
        passdb backend = tdbsam
        algorithmic rid base = 1000
        root directory =
        guest account = nobody
        enable privileges = Yes
        pam password change = No
        passwd program =
        passwd chat = *new*password* %n\n *new*password* %n\n *changed*
        passwd chat debug = No
        passwd chat timeout = 2
        check password script =
        username map =
        password level = 0
        username level = 0
        unix password sync = No
        restrict anonymous = 0
        lanman auth = No
        ntlm auth = Yes
        client NTLMv2 auth = No
        client lanman auth = No
        client plaintext auth = No
        preload modules =
        dedicated keytab file =
        kerberos method = default
        map untrusted to domain = No
        log level = 0
        syslog = 1
        syslog only = No
        log file = /var/log/samba/log.%m
        max log size = 50
        debug timestamp = Yes
        debug prefix timestamp = No
        debug hires timestamp = Yes
        debug pid = No
        debug uid = No
        debug class = No
        enable core files = Yes
        smb ports = 445 139
        large readwrite = Yes
        max protocol = NT1
        min protocol = CORE
        min receivefile size = 0
        read raw = Yes
        write raw = Yes
        disable netbios = No
        reset on zero vc = No
        acl compatibility = auto
        defer sharing violations = Yes
        nt pipe support = Yes
        nt status support = Yes
        announce version = 4.9
        announce as = NT
        max mux = 50
        max xmit = 16644
        name resolve order = lmhosts wins host bcast
        max ttl = 259200
        max wins ttl = 518400
        min wins ttl = 21600
        time server = No
        unix extensions = Yes
        use spnego = Yes
        client signing = auto
        server signing = No
        client use spnego = Yes
        client ldap sasl wrapping = plain
        enable asu support = No
        svcctl list =
        deadtime = 0
        getwd cache = Yes
        keepalive = 300
        lpq cache time = 30
        max smbd processes = 0
        paranoid server security = Yes
        max disk size = 0
        max open files = 16384
        socket options = TCP_NODELAY
        use mmap = Yes
        hostname lookups = No
        name cache timeout = 660
        ctdbd socket =
        cluster addresses =
        clustering = No
        ctdb timeout = 0
        load printers = Yes
        printcap cache time = 750
        printcap name =
        cups server =
        cups encrypt = No
        cups connection timeout = 30
        iprint server =
        disable spoolss = No
        addport command =
        enumports command =
        addprinter command =
        deleteprinter command =
        show add printer wizard = Yes
        os2 driver map =
        mangling method = hash2
        mangle prefix = 1
        max stat cache size = 256
        stat cache = Yes
        machine password timeout = 604800
        add user script =
        rename user script =
        delete user script =
        add group script =
        delete group script =
        add user to group script =
        delete user from group script =
        set primary group script =
        add machine script =
        shutdown script =
        abort shutdown script =
        username map script =
        logon script =
        logon path = \\%N\%U\profile
        logon drive =
        logon home = \\%N\%U
        domain logons = No
        init logon delayed hosts =
        init logon delay = 100
        os level = 20
        lm announce = Auto
        lm interval = 60
        preferred master = No
        local master = Yes
        domain master = Auto
        browse list = Yes
        enhanced browsing = Yes
        dns proxy = Yes
        wins proxy = No
        wins server =
        wins support = No
        wins hook =
        kernel oplocks = Yes
        lock spin time = 200
        oplock break wait time = 0
        ldap admin dn =
        ldap delete dn = No
        ldap group suffix =
        ldap idmap suffix =
        ldap machine suffix =
        ldap passwd sync = no
        ldap replication sleep = 1000
        ldap suffix =
        ldap ssl = start tls
        ldap ssl ads = No
        ldap deref = auto
        ldap follow referral = Auto
        ldap timeout = 15
        ldap connection timeout = 2
        ldap page size = 1024
        ldap user suffix =
        ldap debug level = 0
        ldap debug threshold = 10
        eventlog list =
        add share command =
        change share command =
        delete share command =
        preload =
        lock directory = /var/lib/samba
        state directory = /var/lib/samba
        cache directory = /var/lib/samba
        pid directory = /var/run
        utmp directory =
        wtmp directory =
        utmp = No
        default service =
        message command =
        get quota command =
        set quota command =
        remote announce =
        remote browse sync =
        socket address = 0.0.0.0
        nmbd bind explicit broadcast = Yes
        homedir map = auto.home
        afs username map =
        afs token lifetime = 604800
        log nt token command =
        time offset = 0
        NIS homedir = No
        registry shares = No
        usershare allow guests = No
        usershare max shares = 0
        usershare owner only = Yes
        usershare path = /var/lib/samba/usershares
        usershare prefix allow list =
        usershare prefix deny list =
        usershare template share =
        panic action =
        perfcount module =
        host msdfs = Yes
        passdb expand explicit = No
        idmap backend = tdb
        idmap alloc backend =
        idmap cache time = 604800
        idmap negative cache time = 120
        idmap uid =
        idmap gid =
        template homedir = /home/%D/%U
        template shell = /bin/false
        winbind separator = \
        winbind cache time = 300
        winbind reconnect delay = 30
        winbind max clients = 200
        winbind enum users = No
        winbind enum groups = No
        winbind use default domain = No
        winbind trusted domains only = No
        winbind nested groups = Yes
        winbind expand groups = 1
        winbind nss info = template
        winbind refresh tickets = No
        winbind offline logon = No
        winbind normalize names = No
        winbind rpc only = No
        create krb5 conf = Yes
        comment =
        path =
        username =
        invalid users =
        valid users =
        admin users =
        read list =
        write list =
        printer admin =
        force user =
        force group =
        read only = Yes
        acl check permissions = Yes
        acl group control = No
        acl map full control = Yes
        create mask = 0744
        force create mode = 00
        security mask = 0777
        force security mode = 00
        directory mask = 0755
        force directory mode = 00
        directory security mask = 0777
        force directory security mode = 00
        force unknown acl user = No
        inherit permissions = No
        inherit acls = No
        inherit owner = No
        guest only = No
        administrative share = No
        guest ok = No
        only user = No
        hosts allow =
        hosts deny =
        allocation roundup size = 1048576
        aio read size = 0
        aio write size = 0
        aio write behind =
        ea support = No
        nt acl support = Yes
        profile acls = No
        map acl inherit = No
        afs share = No
        smb encrypt = auto
        block size = 1024
        change notify = Yes
        directory name cache size = 100
        kernel change notify = Yes
        max connections = 0
        min print space = 0
        strict allocate = No
        strict sync = No
        sync always = No
        use sendfile = No
        write cache size = 0
        max reported print jobs = 0
        max print jobs = 1000
        printable = No
        printing = cups
        cups options = raw
        print command =
        lpq command = %p
        lprm command =
        lppause command =
        lpresume command =
        queuepause command =
        queueresume command =
        printer name =
        use client driver = No
        default devmode = Yes
        force printername = No
        printjob username = %U
        default case = lower
        case sensitive = Auto
        preserve case = Yes
        short preserve case = Yes
        mangling char = ~
        hide dot files = Yes
        hide special files = No
        hide unreadable = No
        hide unwriteable files = No
        delete veto files = No
        veto files =
        hide files =
        veto oplock files =
        map archive = Yes
        map hidden = No
        map system = No
        map readonly = yes
        mangled names = Yes
        store dos attributes = No
        dmapi support = No
        browseable = Yes
        access based share enum = No
        blocking locks = Yes
        csc policy = manual
        fake oplocks = No
        locking = Yes
        oplocks = Yes
        level2 oplocks = Yes
        oplock contention limit = 2
        posix locking = Yes
        strict locking = Auto
        share modes = Yes
        dfree cache time = 0
        dfree command =
        copy =
        preexec =
        preexec close = No
        postexec =
        root preexec =
        root preexec close = No
        root postexec =
        available = Yes
        volume =
        fstype = NTFS
        set directory = No
        wide links = No
        follow symlinks = Yes
        dont descend =
        magic script =
        magic output =
        delete readonly = No
        dos filemode = No
        dos filetimes = Yes
        dos filetime resolution = No
        fake directory create times = No
        vfs objects =
        msdfs root = No
        msdfs proxy =

    [homes]
        comment = Home Directories
        read only = No
        browseable = No

    [printers]
        comment = All Printers
        path = /var/spool/samba
        printable = Yes
        browseable = No


Now let's set a password for my **user1** user:

    [root@rhel1 ~]# smbpasswd -a user1
    New SMB password:
    Retype new SMB password:
    tdbsam_open: Converting version 0.0 database to version 4.0.
    tdbsam_convert_backup: updated /var/lib/samba/private/passdb.tdb file.
    Added user user1.


We can see that it also converted the **tdbsam** password file to a new version. To make sure the user was created we can run the following:

    [root@rhel1 ~]# pdbedit -w -L
    user1:500:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:79D209888F8C2A6373082EA5E12BD307:[U          ]:LCT-5337085C:


If you want more information, you can run the following:

    [root@rhel1 ~]# pdbedit -Lv
    ---------------
    Unix username:        user1
    NT username:
    Account Flags:        [U          ]
    User SID:             S-1-5-21-1403670307-859170049-293030116-1000
    Primary Group SID:    S-1-5-21-1403670307-859170049-293030116-513
    Full Name:
    Home Directory:       \\rhel1\user1
    HomeDir Drive:
    Logon Script:
    Profile Path:         \\rhel1\user1\profile
    Domain:               RHEL1
    Account desc:
    Workstations:
    Munged dial:
    Logon time:           0
    Logoff time:          never
    Kickoff time:         never
    Password last set:    Sat, 29 Mar 2014 11:52:28 MDT
    Password can change:  Sat, 29 Mar 2014 11:52:28 MDT
    Password must change: never
    Last bad password   : 0
    Bad password count  : 0
    Logon hours         : FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


At this point we can start the service.

### Samba Service

From the deployment guide:

> To start a Samba server, type the following command in a shell prompt, as root:
>
>     ~]# service smb start
>
>
> To set up a domain member server, you must first join the domain or Active Directory using the **net join** command before starting the **smb** service.
>
> To stop the server, type the following command in a shell prompt, as root:
>
>     ~]# service smb stop
>
>
> The restart option is a quick way of stopping and then starting Samba. This is the most reliable way to make configuration changes take effect after editing the configuration file for Samba. Note that the restart option starts the daemon even if it was not running originally.
>
> To restart the server, type the following command in a shell prompt, as root:
>
>     ~]# service smb restart
>
>
> The **condrestart** (conditional restart) option only starts **smb** on the condition that it is currently running. This option is useful for scripts, because it does not start the daemon if it is not running.
>
> When the **/etc/samba/smb.conf** file is changed, Samba automatically reloads it after a few minutes. Issuing a manual **restart** or **reload** is just as effective.
>
> To conditionally restart the server, type the following command, as root:
>
>     ~]# service smb condrestart
>
>
> A manual reload of the **/etc/samba/smb.conf** file can be useful in case of a failed automatic reload by the **smb** service. To ensure that the Samba server configuration file is reloaded without restarting the service, type the following command, as root:
>
>     ~]# service smb reload
>
>
> By default, the **smb** service does not start automatically at boot time. To configure Samba to start at boot time, use an initscript utility, such as **/sbin/chkconfig**.

So let's enable the service to start on boot and start the service:

    [root@rhel1 ~]# chkconfig smb on
    [root@rhel1 ~]# service smb start
    Starting SMB services:  smbd
    [root@rhel1 ~]# service nmb start
    Starting NMB services:  nmbd


At this point you can make sure that user can see the appropriate shares:

    [root@rhel1 ~]# net -l share -S rhel1 -U user1
    Enter user1's password:

    Enumerating shared resources (exports) on remote server:


    Share name   Type     Description
    ----------   ----     -----------
    IPC$         IPC      IPC Service (Samba Server Version 3.5.6-86.el6)
    user1        Disk     Home Directories


We will need to open up the firewall as well so a client can mount his home directory over SMB. Here are the ports that I opened:

    [root@rhel1 ~]# iptables -I INPUT 14 -m udp -p udp --dport 137 -j ACCEPT
    [root@rhel1 ~]# iptables -I INPUT 15 -m state --state NEW -m tcp -p tcp --dport 139 -j ACCEPT
    [root@rhel1 ~]# iptables -I INPUT 16 -m state --state NEW -m tcp -p tcp --dport 445 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now the server is ready to accept connections from clients.

### Samba Programs

From the deployment guide:

> *   **findsmb <subnet_broadcast_address></subnet_broadcast_address>** - The **findsmb** program is a Perl script which reports information about SMB-aware systems on a specific subnet. If no subnet is specified the local subnet is used. Items displayed include IP address, NetBIOS name, workgroup or domain name, operating system, and version.
>
>     The following example shows the output of executing findsmb as any valid user on a system:
>
>         ~]$ findsmb
>         IP ADDR       NETBIOS NAME  WORKGROUP/OS/VERSION
>         ------------------------------------------------------------------
>         10.1.59.25    VERVE         [MYGROUP] [Unix] [Samba 3.0.0-15]
>         10.1.59.26    STATION22     [MYGROUP] [Unix] [Samba 3.0.2-7.FC1]
>         10.1.56.45    TREK         +[WORKGROUP] [Windows 5.0] [Windows 2000 LAN Manager]
>         10.1.57.94    PIXEL         [MYGROUP] [Unix] [Samba 3.0.0-15]
>         10.1.57.137   MOBILE001     [WORKGROUP] [Windows 5.0] [Windows 2000 LAN Manager]
>         10.1.57.141   JAWS         +[KWIKIMART] [Unix] [Samba 2.2.7a-security-rollup-fix]
>         10.1.56.159   FRED         +[MYGROUP] [Unix] [Samba 3.0.0-14.3E]
>         10.1.59.192   LEGION       *[MYGROUP] [Unix] [Samba 2.2.7-security-rollup-fix]
>         10.1.56.205   NANCYN       +[MYGROUP] [Unix] [Samba 2.2.7a-security-rollup-fix]
>
>
> *   **net <protocol> <function> <misc_options> <target_options></target_options></misc_options></function></protocol>** - The **net** utility is similar to the **net** utility used for Windows and MS-DOS. The first argument is used to specify the protocol to use when executing a command. The ** <protocol></protocol>** option can be **ads**, **rap**, or **rpc** for specifying the type of server connection. Active Directory uses **ads**, Win9x/NT3 uses **rap**, and Windows NT4/2000/2003/2008 uses **rpc**. If the protocol is omitted, net automatically tries to determine it.
>
>     The following example displays a list the available shares for a host named wakko:
>
>         ~]$ net -l share -S wakko
>         Password:
>         Enumerating shared resources (exports) on remote server:
>         Share name   Type     Description
>         ----------   ----     -----------
>         data         Disk     Wakko data share
>         tmp          Disk     Wakko tmp share
>         IPC$         IPC      IPC Service (Samba Server)
>         ADMIN$       IPC      IPC Service (Samba Server)
>
>
>     The following example displays a list of Samba users for a host named wakko:
>
>         ~]$ net -l user -S wakko
>         root password:
>         User name             Comment
>         -----------------------------
>         andriusb              Documentation
>         joe                   Marketing
>         lisa                  Sales
>
>
> *   **nmblookup <options> <netbios_name></netbios_name></options>** - The **nmblookup** program resolves NetBIOS names into IP addresses. The program broadcasts its query on the local subnet until the target machine replies.
>
>     The following example displays the IP address of the NetBIOS name trek:
>
>         ~]$ nmblookup trek
>         querying trek on 10.1.59.255
>         10.1.56.45 trek<00>
>
>
> *   **pdbedit <options></options>** - The **pdbedit** program manages accounts located in the SAM database. All back ends are supported including **smbpasswd**, **LDAP**, and the **tdb** database library.
>
>     The following are examples of adding, deleting, and listing users:
>
>         ~]$ pdbedit -a kristin
>         new password:
>         retype new password:
>         Unix username:        kristin
>         NT username:
>         Account Flags:        [U          ]
>         User SID:             S-1-5-21-1210235352-3804200048-1474496110-2012
>         Primary Group SID:    S-1-5-21-1210235352-3804200048-1474496110-2077
>         Full Name: Home Directory:       \\wakko\kristin
>         HomeDir Drive:
>         Logon Script:
>         Profile Path:         \\wakko\kristin\profile
>         Domain:               WAKKO
>         Account desc:
>         Workstations: Munged
>         dial:
>         Logon time:           0
>         Logoff time:          Mon, 18 Jan 2038 22:14:07 GMT
>         Kickoff time:         Mon, 18 Jan 2038 22:14:07 GMT
>         Password last set:    Thu, 29 Jan 2004 08:29:28
>         GMT Password can change:  Thu, 29 Jan 2004 08:29:28 GMT
>         Password must change: Mon, 18 Jan 2038 22:14:07 GMT
>         ~]$ pdbedit -v -L kristin
>         Unix username:        kristin
>         NT username:
>         Account Flags:        [U          ]
>         User SID:             S-1-5-21-1210235352-3804200048-1474496110-2012
>         Primary Group SID:    S-1-5-21-1210235352-3804200048-1474496110-2077
>         Full Name:
>         Home Directory:       \\wakko\kristin
>         HomeDir Drive:
>         Logon Script:
>         Profile Path:         \\wakko\kristin\profile
>         Domain:               WAKKO
>         Account desc:
>         Workstations: Munged
>         dial:
>         Logon time:           0
>         Logoff time:          Mon, 18 Jan 2038 22:14:07 GMT
>         Kickoff time:         Mon, 18 Jan 2038 22:14:07 GMT
>         Password last set:    Thu, 29 Jan 2004 08:29:28 GMT
>         Password can change:  Thu, 29 Jan 2004 08:29:28 GMT
>         Password must change: Mon, 18 Jan 2038 22:14:07 GMT
>         ~]$ pdbedit -L
>         andriusb:505:
>         joe:503:
>         lisa:504:
>         kristin:506:
>         ~]$ pdbedit -x joe
>         ~]$ pdbedit -L
>         andriusb:505: lisa:504: kristin:506:
>
>
> *   **rpcclient <server> <options></options></server>** - The **rpcclient** program issues administrative commands using Microsoft RPCs, which provide access to the Windows administration graphical user interfaces (GUIs) for systems management. This is most often used by advanced users that understand the full complexity of Microsoft RPCs.
>
> *   **smbcacls <//server/share> <filename> <options></options></filename>** - The **smbcacls** program modifies Windows ACLs on files and directories shared by a Samba server or a Windows server.
>
> *   **smbclient <//server/share> <password> <options></options></password>** - The **smbclient** program is a versatile UNIX client which provides functionality similar to **ftp**.
>
> *   **smbcontrol -i <options> <destination> <messagetype> <parameters></parameters></messagetype></destination></options>** - The **smbcontrol** program sends control messages to running **smbd**, **nmbd**, or **winbindd** daemons. Executing **smbcontrol -i** runs commands interactively until a blank line or a '**q**' is entered.
>
> *   **smbpasswd <options> <username> <password></password></username></options>** - The **smbpasswd** program manages encrypted passwords. This program can be run by a superuser to change any user's password as well as by an ordinary user to change their own Samba password.
>
> *   **smbspool <job> <user> <title>
>       <br /> <copies> <options> <filename></filename></options></copies><br />
>     </title></user></job>** - The
>
>     **smbspool** program is a CUPS-compatible printing interface to Samba. Although designed for use with CUPS printers, **smbspool** can work with non-CUPS printers as well.
>
> *   **smbstatus <options></options>** - The **smbstatus** program displays the status of current connections to a Samba server.
> *   **smbtar <options></options>** - The **smbtar** program performs backup and restores of Windows-based share files and directories to a local tape archive. Though similar to the **tar** command, the two are not compatible.
> *   **testparm <options> <filename> <hostname IP_address\></hostname></filename></options>** - The **testparm** program checks the syntax of the **/etc/samba/smb.conf** file. If your **/etc/samba/smb.conf** file is in the default location (**/etc/samba/smb.conf**) you do not need to specify the location. Specifying the hostname and IP address to the **testparm** program verifies that the **hosts.allow** and **host.deny** files are configured correctly. The **testparm** program also displays a summary of your **/etc/samba/smb.conf** file and the server's role (stand-alone, domain, etc.) after testing. This is convenient when debugging as it excludes comments and concisely presents information for experienced administrators to read.
>
>     For example:
>
>         ~]$ testparm
>         Load smb config files from /etc/samba/smb.conf
>         Processing section "[homes]"
>         Processing section "[printers]"
>         Processing section "[tmp]"
>         Processing section "[html]"
>         Loaded services file OK.
>         Server role: ROLE_STANDALONE
>         Press enter to see a dump of your service definitions
>         <enter>
>         # Global parameters
>         [global]
>           workgroup = MYGROUP
>           server string = Samba Server
>           security = SHARE
>           log file = /var/log/samba/%m.log
>           max log size = 50
>           socket options = TCP_NODELAY SO_RCVBUF=8192 SO_SNDBUF=8192
>           dns proxy = No
>         [homes]
>           comment = Home Directories
>           read only = No
>           browseable = No
>         [printers]
>           comment = All Printers
>           path = /var/spool/samba
>           printable = Yes
>           browseable = No
>         [tmp]
>           comment = Wakko tmp
>           path = /tmp
>           guest only = Yes
>         [html]
>           comment = Wakko www
>           path = /var/www/html
>           force user = andriusb
>           force group = users
>           read only = No
>           guest only = Yes
>
>
> *   **wbinfo <options></options>** - The **wbinfo** program displays information from the **winbindd** daemon. The **winbindd** daemon must be running for **wbinfo** to work.

### Connecting to Samba Server

From the deployment guide:

> To query the network for Samba servers, use the **findsmb** command. For each server found, it displays its IP address, NetBIOS name, workgroup name, operating system, and SMB server version.
>
> To connect to a Samba share from a shell prompt, type the following command:
>
>     ~]$ smbclient //<hostname>/<sharename> -U <username>
>
>
> Replace **<hostname></hostname>** with the hostname or **IP** address of the Samba server you want to connect to, **<sharename></sharename>** with the name of the shared directory you want to browse, and **<username></username>** with the Samba username for the system. Enter the correct password or press **Enter** if no password is required for the user.
>
> If you see the **smb:>** prompt, you have successfully logged in. Once you are logged in, type **help** for a list of commands. If you wish to browse the contents of your home directory, replace **sharename** with your username. If the **-U** switch is not used, the username of the current user is passed to the Samba server.
>
> To exit **smbclient**, type **exit** at the **smb:>** prompt.

### Mounting a Samba Share

From the same guide:

> Sometimes it is useful to mount a Samba share to a directory so that the files in the directory can be treated as if they are part of the local file system.
>
> To mount a Samba share to a directory, create a directory to mount it to (if it does not already exist), and execute the following command as root:
>
>     ~]# mount -t cifs //<servername>/<sharename> /mnt/point/ -o username=<username>,password=<password>
>
>
> This command mounts **<sharename></sharename>** from **<servername></servername>** in the local directory **/mnt/point/**.
>
> The **mount.cifs** utility is a separate RPM (independent from Samba). In order to use **mount.cifs**, first ensure the **cifs-utils** package is installed on your system by running, as root:
>
>     ~]# yum install cifs-utils
>

### Connecting to a Samba Share with a Client

So let's try to connect to the Samba share from RH5 to RH6. On the RH5 machine let's install the client utilities:

    [root@rhel2 ~]# yum install samba-client


Now let's see if we can see our samba server from the client:

    [root@rhel2 ~]# findsmb
                                    *=DMB
                                    +=LMB
    IP ADDR         NETBIOS NAME     WORKGROUP/OS/VERSION
    ---------------------------------------------------------------------
    192.168.2.2     RHEL1         +[LOCAL] [Unix] [Samba 3.5.6-86.el6]


To anonymously query the server run the following:

    [root@rhel2 ~]# smbclient -L RHEL1 -N
    Anonymous login successful
    Domain=[LOCAL] OS=[Unix] Server=[Samba 3.5.6-86.el6]

        Sharename       Type      Comment
        ---------       ----      -------
        IPC$            IPC       IPC Service (Samba Server Version 3.5.6-86.el6)
    Anonymous login successful
    Domain=[LOCAL] OS=[Unix] Server=[Samba 3.5.6-86.el6]

        Server               Comment
        ---------            -------
        RHEL1                Samba Server Version 3.5.6-86.el6

        Workgroup            Master
        ---------            -------
        LOCAL                RHEL1


To query the server as a user, run the following:

    [root@rhel2 ~]# smbclient -L RHEL1 -U user1
    Password:
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]

    Sharename       Type      Comment
    ---------       ----      -------
    IPC$            IPC       IPC Service (Samba Server Version 3.5.6-86.el6)
    user1           Disk      Home Directories
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]
    Server               Comment
    ---------            -------

    Workgroup            Master
    ---------            -------
    LOCAL                RHEL1


I used the password I set with the **smbpasswd** command when I created the user. But notice this time around I saw my home directory as a share. To connect with an ftp style client, run the following:

    [root@rhel2 ~]# smbclient //RHEL1/user1 -U user1
    Password:
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]
    smb: \> ls
    NT_STATUS_ACCESS_DENIED listing *

            34300 blocks of size 262144. 537 blocks available
    smb: \> quit


As you see initially I ran into an acccess denied issue. This is due to SELinux, running the following fixed the issue:

    [root@rhel1 ~]# setsebool -P samba_enable_home_dirs on


then it worked fine:

    [root@rhel2 ~]# smbclient //RHEL1/user1 -U user1
    Password:
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]
    smb: \> ls
      .                                   D        0  Sat Mar 29 16:06:15 2014
      ..                                  D        0  Sat Feb  9 01:35:56 2013
      .ssh                               DH        0  Sat Mar  8 09:16:28 2014
      .Xauthority                         H      384  Sat Mar  8 12:05:56 2014
      .dbus                              DH        0  Sat Mar  8 11:36:58 2014
      .bash_logout                        H       18  Thu Jan 27 06:41:02 2011
      .vnc                               DH        0  Sat Mar  8 12:10:32 2014
      .bash_history                       H     1711  Sat Mar 29 16:08:12 2014
      .bashrc                             H      124  Thu Jan 27 06:41:02 2011
      l                                   D        0  Sat Mar 29 16:06:15 2014
      foo.txt                                      0  Fri Feb  8 07:24:20 2013
      .bash_profile                       H      176  Thu Jan 27 06:41:02 2011
      .xinitrc                           AH     1486  Sat Mar  8 11:30:02 2014

            34300 blocks of size 262144. 537 blocks available


To make sure writes are working, upload a file:

    smb: \> !ls
    anaconda-ks.cfg  Desktop  install.log  install.log.syslog  repo
    smb: \> put install.log
    putting file install.log as \install.log (1622.9 kb/s) (average 1622.9 kb/s)


On the server side you can check who is connected with the **smbstatus** command:

    [root@rhel1 ~]# smbstatus

    Samba version 3.5.6-86.el6
    PID     Username      Group         Machine
    -------------------------------------------------------------------
    12296     user1         user1         rhel2        (::ffff:192.168.2.3)

    Service      pid     machine       Connected at
    -------------------------------------------------------
    user1        12296   rhel2         Sat Mar 29 16:16:12 2014

    No locked files


To mount the share we can do the following:

    [root@rhel2 ~]# mkdir /mnt/cifs
    [root@rhel2 ~]# mount -t cifs //rhel1/user1 /mnt/cifs -o username=user1
    Password:
    [root@rhel2 cifs]# mount | grep cifs
    //rhel1/user1 on /mnt/cifs type cifs (rw,mand)


We can then make sure we can write a file

    [root@rhel2 ~]# cd /mnt/cifs/
    [root@rhel2 cifs]# ls -l
    total 32
    -rw-r--r-- 1 user1 user1     0 Feb  8  2013 foo.txt
    -rwxr--r-- 1 user1 user1 29914 Mar 29 16:18 install.log
    drwxrwxr-x 2 user1 user1     0 Mar 29 16:23 l
    [root@rhel2 cifs]# touch test
    [root@rhel2 cifs]# ls -l
    total 32
    -rw-r--r-- 1 user1 user1     0 Feb  8  2013 foo.txt
    -rwxr--r-- 1 user1 user1 29914 Mar 29 16:18 install.log
    drwxrwxr-x 2 user1 user1     0 Mar 29 16:23 l
    -rw-r--r-- 1 user1 user1     0 Mar 29 16:23 test


### Samba and SELinux

From [Managing Confined Services](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Confined_Services/Red_Hat_Enterprise_Linux-6-Managing_Confined_Services-en-US.pdf):

> When SELinux is enabled, the Samba server (**smbd**) runs confined by default. Confined services run in their own domains, and are separated from other confined services.
>
> Files must be labeled correctly to allow **smbd** to access and share them. For example, **smbd** can read and write to files labeled with the **samba_share_t** type, but by default, cannot access files labeled with the **httpd_sys_content_t** type, which is intended for use by the Apache HTTP Server. Booleans must be enabled to allow certain behavior, such as allowing home directories and NFS volumes to be exported through Samba, as well as to allow Samba to act as a domain controller.

#### Samba SELinux Types

From the same guide:

> Label files with the **samba_share_t** type to allow Samba to share them. Only label files you have created, and do not relabel system files with the **samba_share_t** type: Booleans can be enabled to share such files and directories. SELinux allows Samba to write to files labeled with the samba_share_t type, as long as /etc/samba/smb.conf and Linux permissions are set accordingly.
>
> The **samba_etc_t** type is used on certain files in **/etc/samba/**, such as **smb.conf**. Do not manually label files with the **samba_etc_t** type. If files in **/etc/samba/** are not labeled correctly, run the **restorecon -R -v /etc/samba** command as the root user to restore such files to their default contexts. If **/etc/samba/smb.conf** is not labeled with the **samba_etc_t** type, the service smb start command may fail and an SELinux denial may be logged.

#### Samba SELinux Booleans

From the above guide:

> SELinux is based on the least level of access required for a service to run. Services can be run in a variety of ways; therefore, you need to specify how you run your services. > Use the following Booleans to set up SELinux:
>
> *   **allow_smbd_anon_write** - Having this Boolean enabled allows **smbd** to write to a public directory, such as an area reserved for common files that otherwise has no special access restrictions.
> *   **samba_create_home_dirs** - Having this Boolean enabled allows Samba to create new home directories independently. This is often done by mechanisms such as PAM.
> *   **samba_domain_controller** - When enabled, this Boolean allows Samba to act as a domain controller, as well as giving it permission to execute related commands such as **useradd**, **groupadd** and **passwd**.
> *   **samba_enable_home_dirs** - Enabling this Boolean allows Samba to share users' home directories.
> *   **samba_export_all_ro** - Export any file or directory, allowing read-only permissions. This allows files and directories that are not labeled with the **samba_share_t** type to be shared through Samba. When the **samba_export_all_ro** Boolean is on, but the **samba_export_all_rw** Boolean is off, write access to Samba shares is denied, even if write access is configured in **/etc/samba/smb.conf**, as well as Linux permissions allowing write access.
> *   **samba_export_all_rw** - Export any file or directory, allowing read and write permissions. This allows files and directories that are not labeled with the **samba_share_t** type to be exported through Samba. Permissions in **/etc/samba/smb.conf** and Linux permissions must be configured to allow write access.
> *   **samba_run_unconfined** - Having this Boolean enabled allows Samba to run unconfined scripts in the **/var/lib/samba/scripts/** directory.
> *   **samba_share_fusefs** - This Boolean must be enabled for Samba to share fusefs file systems.
> *   **samba_share_nfs** - Disabling this Boolean prevents **smbd** from having full access to NFS shares via Samba. Enabling this Boolean will allow Samba to share NFS volumes.
> *   **use_samba_home_dirs** - Enable this Boolean to use a remote server for Samba home directories.
> *   **virt_use_samba** Allow virtual machine access to CIFS files.

#### Samba Share Example with SELinux

From the Managing Confined Services Guide:

> The following example creates a new directory, and shares that directory through Samba:
>
> 1.  Run the **rpm -q samba samba-common samba-client** command to confirm the samba, samba-common, and samba-client packages are installed. If any of these packages are not installed, install them by running the **yum install package-name** command as the root user.
> 2.  Run the **mkdir /myshare** command as the root user to create a new top-level directory to share files through Samba.
> 3.  Run the **touch /myshare/file1** command as the root user to create an empty file. This file is used later to verify the Samba share mounted correctly.
> 4.  SELinux allows Samba to read and write to files labeled with the **samba_share_t** type, as long as **/etc/samba/smb.conf** and Linux permissions are set accordingly. Run the following command as the root user to add the label change to file-context configuration:
>
>         ~]# semanage fcontext -a -t samba_share_t "/myshare(/.*)?"
>
>
> 5.  Run the **restorecon -R -v /myshare** command as the root user to apply the label changes:
>
>         ~]# restorecon -R -v /myshare
>         restorecon reset /myshare context unconfined_u:object_r:default_t:s0->system_u:object_r:samba_share_t:s0
>         restorecon reset /myshare/file1 context unconfined_u:object_r:default_t:s0->system_u:object_r:samba_share_t:s0
>
>
> 6.  Edit **/etc/samba/smb.conf** as the root user. Add the following to the bottom of this file to share the **/myshare/** directory through Samba:
>
>         [myshare]
>         comment = My share
>         path = /myshare
>         public = yes
>         writeable = no
>
>
> 7.  A Samba account is required to mount a Samba file system. Run the **smbpasswd -a username** command as the root user to create a Samba account, where username is an existing Linux user. For example, **smbpasswd -a testuser** creates a Samba account for the Linux **testuser** user:
>
>         ~]# smbpasswd -a testuser
>         New SMB password: Enter a password
>         Retype new SMB password: Enter the same password again
>         Added user testuser.
>
>
>     Running **smbpasswd -a username**, where username is the user name of a Linux account that does not exist on the system, causes a **Cannot locate Unix account for 'username'! error.**
>
> 8.  Run the **service smb start** command as the root user to start the Samba service:
>
>         ~]# service smb start
>         Starting SMB services:                                     [  OK  ]
>
>
> 9.  Run the **smbclient -U username -L localhost** command to list the available shares, where username is the Samba account added in step 7. When prompted for a password, enter the password assigned to the Samba account in step 7 (version numbers may differ):
>
>         ~]$ smbclient -U username -L localhost
>         Enter username's password:
>         Domain=[HOSTNAME] OS=[Unix] Server=[Samba 3.4.0-0.41.el6]
>
>         Sharename       Type      Comment
>         ---------       ----      -------
>         myshare         Disk      My share
>         IPC$            IPC       IPC Service (Samba Server Version 3.4.0-0.41.el6)
>         username        Disk      Home Directories
>         Domain=[HOSTNAME] OS=[Unix] Server=[Samba 3.4.0-0.41.el6]
>
>         Server               Comment
>         ---------            -------
>
>         Workgroup            Master
>         ---------            -------
>
>
> 10. Run the **mkdir /test/** command as the root user to create a new directory. This directory will be used to mount the **myshare** Samba share.
>
> 11. Run the following command as the root user to mount the **myshare** Samba share to **/test/**, replacing username with the user name from step 7:
>
>         ~]# mount //localhost/myshare /test/ -o user=username
>
>
>     Enter the password for username, which was configured in step 7.
>
> 12. Run the **ls /test/** command to view the **file1** file created in step 3:
>
>         ~]$ ls /test/
>         file1
>

So let's try this out. Let's share a directory other than our home directory. First let's add a directory that we will share:

    [root@rhel1 ~]# mkdir /share
    [root@rhel1 ~]# chown user1 /share


Now let's add that directory as a share into our **/etc/samba/smb.conf** file:

    [share]
    comment = My share
    path = /share
    browseable = yes
    writeable = yes
    valid users = user1


let's make sure the configuration is okay:

    [root@rhel1 ~]# testparm -s
    Load smb config files from /etc/samba/smb.conf
    rlimit_max: rlimit_max (1024) below minimum Windows limit (16384)
    Processing section "[homes]"
    Processing section "[printers]"
    Processing section "[share]"
    Loaded services file OK.
    Server role: ROLE_STANDALONE
    [global]
        workgroup = LOCAL
        server string = Samba Server Version %v
        log file = /var/log/samba/log.%m
        max log size = 50
        cups options = raw

    [homes]
        comment = Home Directories
        valid users = %S
        read only = No

    [printers]
        comment = All Printers
        path = /var/spool/samba
        printable = Yes
        browseable = No

    [share]
        comment = My share
        path = /share
        read only = No
            valid users = user1


Now let's reload the service

    [root@rhel1 ~]# service smb reload
    Reloading smb.conf file: smbd


Now from the client let's try to connect to that share:

    [root@rhel2 ~]# smbclient //RHEL1/share -U user1
    Password:
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]
    tree connect failed: NT_STATUS_BAD_NETWORK_NAME


Looks like we are getting blocked. Now now let's set the context for that directory:

    [root@rhel1 ~]# semanage fcontext -a -t samba_share_t "/share(/.*)?"
    [root@rhel1 ~]# restorecon -R -v /share
    restorecon reset /share context unconfined_u:object_r:default_t:s0->system_u:object_r:samba_share_t:s0


Now let's try it again:

    [root@rhel2 ~]# smbclient //RHEL1/share -U user1
    Password:
    Domain=[RHEL1] OS=[Unix] Server=[Samba 3.5.6-86.el6]
    smb: \> ls
      .                                   D        0  Sat Mar 29 16:54:19 2014
      ..                                 DR        0  Sat Mar 29 16:54:19 2014

            34300 blocks of size 262144. 536 blocks available
    smb: \> !ls
    anaconda-ks.cfg  Desktop  install.log  install.log.syslog  repo
    smb: \> put anaconda-ks.cfg
    putting file anaconda-ks.cfg as \anaconda-ks.cfg (159.7 kb/s) (average 159.7 kb/s)


That looks good. And here are my Samba SELinux booleans:

    [root@rhel1 ~]# getsebool -a | grep -E 'smb|samba'
    allow_smbd_anon_write --> off
    samba_create_home_dirs --> off
    samba_domain_controller --> off
    samba_enable_home_dirs --> on
    samba_export_all_ro --> off
    samba_export_all_rw --> off
    samba_run_unconfined --> off
    samba_share_fusefs --> off
    samba_share_nfs --> off
    use_samba_home_dirs --> off
    virt_use_samba --> off


Just for reference here is another pretty good guide: [Deploying a Red Hat Enterprise Linux 6 based Samba Server in a Windows Active Directory Domain](http://www.redhat.com/rhecm/rest-rhecm/jcr/repository/collaboration/jcr:system/jcr:versionStorage/361057860a0526010a1da39b0d2743fc/1/jcr:frozenNode/rh:resourceFile)

