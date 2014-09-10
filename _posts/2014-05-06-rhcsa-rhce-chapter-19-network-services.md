---
title: 'RHCSA and RHCE Chapter 19 - Network Services'
author: Karim Elatov
layout: post
permalink: /2014/05/rhcsa-rhce-chapter-19-network-services/
categories: ['os', 'certifications', 'home_lab', 'networking', 'rhcsa_rhce']
tags: ['linux', 'dhcp', 'ntp', 'rhel', 'telnet', 'xinetd']
---

## Xinetd

From the [Security Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf):

> The **xinetd** daemon is a TCP-wrapped *super* service which controls access to a subset of popular network services, including FTP, IMAP, and Telnet. It also provides service-specific configuration options for access control, enhanced logging, binding, redirection, and resource utilization control.
>
> When a client attempts to connect to a network service controlled by xinetd, the super service receives the request and checks for any TCP Wrappers access control rules.
>
> If access is allowed, **xinetd** verifies that the connection is allowed under its own access rules for that service. It also checks that the service is able to have more resources assigned to it and that it is not in breach of any defined rules.
>
> If all these conditions are met (that is, access is allowed to the service; the service has not reached its resource limit; and the service is not in breach of any defined rule), **xinetd** then starts an instance of the requested service and passes control of the connection to it. After the connection has been established, xinetd takes no further part in the communication between the client and the server.

### xinetd Configuration Files

From the same guide:

> The configuration files for **xinetd** are as follows:
>
> *   **/etc/xinetd.conf** — The global **xinetd** configuration file.
> *   **/etc/xinetd.d/** — The directory containing all service-specific files.

#### The /etc/xinetd.conf File

From the above guide:

> The **/etc/xinetd.conf** file contains general configuration settings which affect every service under xinetd's control. It is read when the **xinetd** service is first started, so for configuration changes to take effect, you need to restart the **xinetd** service. The following is a sample **/etc/xinetd.conf** file:
>
>     defaults
>     {
>        instances               = 60
>        log_type                = SYSLOG   authpriv
>        log_on_success          = HOST PID
>        log_on_failure          = HOST
>        cps                     = 25 30
>     }
>     includedir /etc/xinetd.d
>
>
> These lines control the following aspects of **xinetd**:
>
> *   **instances** - Specifies the maximum number of simultaneous requests that **xinetd** can process.
> *   **log_type** - Configures **xinetd** to use the **authpriv** log facility, which writes log entries to the **/var/log/secure** file. Adding a directive such as **FILE /var/log/xinetdlog** would create a custom log file called **xinetdlog** in the **/var/log/** directory.
> *   **log_on_success** - Configures **xinetd** to log successful connection attempts. By default, the remote host's IP address and the process ID of the server processing the request are recorded.
> *   **log_on_failure** - Configures **xinetd** to log failed connection attempts or if the connection was denied.
> *   **cps** - Configures **xinetd** to allow no more than 25 connections per second to any given service. If this limit is exceeded, the service is retired for 30 seconds.
> *   **includedir /etc/xinetd.d/** - Includes options declared in the service-specific configuration files located in the **/etc/xinetd.d/** directory.

#### The /etc/xinetd.d/ Directory

From the Security Guide:

> The **/etc/xinetd.d/** directory contains the configuration files for each service managed by **xinetd** and the names of the files are correlated to the service. As with **xinetd.conf**, this directory is read only when the **xinetd** service is started. For any changes to take effect, the administrator must restart the xinetd service.
>
> The format of files in the **/etc/xinetd.d/** directory use the same conventions as **/etc/xinetd.conf**. The primary reason the configuration for each service is stored in a separate file is to make customization easier and less likely to affect other services.
>
> To gain an understanding of how these files are structured, consider the **/etc/xinetd.d/krb5-telnet** file:
>
>     service telnet
>     {
>        flags           = REUSE
>        socket_type     = stream
>        wait            = no
>        user            = root
>        server          = /usr/kerberos/sbin/telnetd
>        log_on_failure  += USERID
>        disable         = yes
>     }
>
>
> These lines control various aspects of the **telnet** service:
>
> *   **service** - Specifies the service name, usually one of those listed in the **/etc/services** file.
> *   **flags** - Sets any of a number of attributes for the connection. REUSE instructs **xinetd** to reuse the socket for a Telnet connection.
> *   **socket_type** - Sets the network socket type to stream.
> *   **wait** - Specifies whether the service is single-threaded (**yes**) or multi-threaded (**no**).
> *   **user** - Specifies which user ID the process runs under.
> *   **server** - Specifies which binary executable to launch.
> *   **log_on_failure** - Specifies logging parameters for **log_on_failure** in addition to those already defined in **xinetd.conf**.
> *   **disable** - Specifies whether the service is disabled (**yes**) or enabled (**no**).

#### Xinetd Logging Options

From the same guide:

> The following logging options are available for both **/etc/xinetd.conf** and the service-specific configuration files within the **/etc/xinetd.d/** directory.
>
> The following is a list of some of the more commonly used logging options:
>
> *   **ATTEMPT** - Logs the fact that a failed attempt was made (**log_on_failure**).
> *   **DURATION** - Logs the length of time the service is used by a remote system (**log_on_success**).
> *   **EXIT** - Logs the exit status or termination signal of the service (**log_on_success**).
> *   **HOST** - Logs the remote host's IP address (**log_on_failure** and **log_on_success**).
> *   **PID** - Logs the process ID of the server receiving the request (**log_on_success**).
> *   **USERID** - Logs the remote user using the method defined in RFC 1413 for all multi-threaded stream services (**log_on_failure** and **log_on_success**).

#### Xinetd Access Control Options

From the above guide:

> Users of **xinetd** services can choose to use the TCP Wrappers hosts access rules, provide access control via the xinetd configuration files, or a mixture of both.
>
> The **xinetd** hosts access control differs from the method used by TCP Wrappers. While TCP Wrappers places all of the access configuration within two files, **/etc/hosts.allow** and **/etc/hosts.deny**, xinetd's access control is found in each service's configuration file in the **/etc/xinetd.d/** directory.
>
> The following hosts access options are supported by **xinetd**:
>
> *   **only_from** - Allows only the specified hosts to use the service.
> *   **no_access** - Blocks listed hosts from using the service.
> *   **access_times** - Specifies the time range when a particular service may be used. The time range must be stated in 24-hour format notation, **HH:MM-HH:MM**.
>
> The **only_from** and **no_access** options can use a list of IP addresses or host names, or can specify an entire network. Like TCP Wrappers, combining **xinetd** access control with the enhanced logging configuration can increase security by blocking requests from banned hosts while verbosely recording each connection attempt.
>
> For example, the following **/etc/xinetd.d/telnet** file can be used to block Telnet access from a particular network group and restrict the overall time range that even allowed users can log in:
>
>     service telnet
>     {
>        disable         = no
>        flags           = REUSE
>        socket_type     = stream
>        wait            = no
>        user            = root
>        server          = /usr/kerberos/sbin/telnetd
>        log_on_failure  += USERID
>        no_access       = 172.16.45.0/24
>        log_on_success  += PID HOST EXIT
>        access_times    = 09:45-16:15
>     }
>
>
> In this example, when a client system from the **172.16.45.0/24** network, such as **172.16.45.2**, tries to access the Telnet service, it receives the following message:
>
>     Connection closed by foreign host.
>
>
> In addition, their login attempts are logged in **/var/log/messages** as follows:
>
>     Sep  7 14:58:33 localhost xinetd[5285]: FAIL: telnet address from=172.16.45.107
>     Sep  7 14:58:33 localhost xinetd[5283]: START: telnet pid=5285 from=172.16.45.107
>     Sep  7 14:58:33 localhost xinetd[5283]: EXIT: telnet status=0 pid=5285 duration=0(sec)
>
>
> When using TCP Wrappers in conjunction with **xinetd** access controls, it is important to understand the relationship between the two access control mechanisms.
>
> The following is the sequence of events followed by xinetd when a client requests a connection:
>
> 1.  The **xinetd** daemon accesses the TCP Wrappers hosts access rules using a **libwrap.so** library call. If a deny rule matches the client, the connection is dropped. If an allow rule matches the client, the connection is passed to **xinetd**.
> 2.  The **xinetd** daemon checks its own access control rules both for the xinetd service and the requested service. If a deny rule matches the client, the connection is dropped. Otherwise, **xinetd** starts an instance of the requested service and passes control of the connection to that service.

#### Xinetd Binding and Redirection Options

From the Security Guide:

> The service configuration files for **xinetd** support binding the service to an IP address and redirecting incoming requests for that service to another IP address, hostname, or port.
>
> Binding is controlled with the **bind** option in the service-specific configuration files and links the service to one IP address on the system. When this is configured, the bind option only allows requests to the correct IP address to access the service. You can use this method to bind different services to different network interfaces based on requirements.
>
> This is particularly useful for systems with multiple network adapters or with multiple IP addresses. On such a system, insecure services (for example, Telnet), can be configured to listen only on the interface connected to a private network and not to the interface connected to the Internet.
>
> The redirect option accepts an IP address or hostname followed by a port number. It configures the service to redirect any requests for this service to the specified host and port number. This feature can be used to point to another port number on the same system, redirect the request to a different IP address on the same machine, shift the request to a totally different system and port number, or any combination of these options. A user connecting to a certain service on a system may therefore be rerouted to another system without disruption.
>
> The **xinetd** daemon is able to accomplish this redirection by spawning a process that stays alive for the duration of the connection between the requesting client machine and the host actually providing the service, transferring data between the two systems.
>
> The advantages of the **bind** and **redirect** options are most clearly evident when they are used together. By binding a service to a particular IP address on a system and then redirecting requests for this service to a second machine that only the first machine can see, an internal system can be used to provide services for a totally different network. Alternatively, these options can be used to limit the exposure of a particular service on a multi-homed machine to a known IP address, as well as redirect any requests for that service to another machine especially configured for that purpose.
>
> For example, consider a system that is used as a firewall with this setting for its Telnet service:
>
>     service telnet
>     {
>        socket_type        = stream
>        wait           = no
>        server         = /usr/kerberos/sbin/telnetd
>        log_on_success     += DURATION USERID
>        log_on_failure     += USERID
>        bind                    = 123.123.123.123
>        redirect                = 10.0.1.13 23
>     }
>
>
> The **bind** and **redirect** options in this file ensure that the Telnet service on the machine is bound to the external IP address (**123.123.123.123**), the one facing the Internet. In addition, any requests for Telnet service sent to **123.123.123.123** are redirected via a second network adapter to an internal IP address (**10.0.1.13**) that only the firewall and internal systems can access. The firewall then sends the communication between the two systems, and the connecting system thinks it is connected to **123.123.123.123** when it is actually connected to a different machine.
>
> This feature is particularly useful for users with broadband connections and only one fixed IP address. When using Network Address Translation (NAT), the systems behind the gateway machine, which are using internal-only IP addresses, are not available from outside the gateway system. However, when certain services controlled by xinetd are configured with the bind and redirect options, the gateway machine can act as a proxy between outside systems and a particular internal machine configured to provide the service. In addition, the various **xinetd** access control and logging options are also available for additional protection.

#### Xinetd Resource Management Options

From the above guide:

> The **xinetd** daemon can add a basic level of protection from Denial of Service (DoS) attacks. The following is a list of directives which can aid in limiting the effectiveness of such attacks:
>
> *   **per_source** - Defines the maximum number of instances for a service per source IP address. It accepts only integers as an argument and can be used in both **xinetd.conf** and in the service-specific configuration files in the **xinetd.d/** directory.
> *   **cps** — Defines the maximum number of connections per second. This directive takes two integer arguments separated by white space. The first argument is the maximum number of connections allowed to the service per second. The second argument is the number of seconds that **xinetd** must wait before re-enabling the service. It accepts only integers as arguments and can be used in either the **xinetd.conf** file or the service-specific configuration files in the **xinetd.d/** directory.
> *   **max_load** — Defines the CPU usage or load average threshold for a service. It accepts a floating point number argument. The load average is a rough measure of how many processes are active at a given time. See the **uptime**, **who**, and **procinfo** commands for more information about load average.

### Telnet Example with Xinetd

In [Chapter 8](/2013/03/rhcsa-and-rhce-chapter-8-network-installs/), I covered the **tftp** install with **xinetd**, now let's try **telnet** (this is just for demonstration purposes, use **ssh** over **telnet**). First install **xinetd**:

    [root@rhel1 ~]# yum install xinetd


here are the default settings for **xinetd**:

    [root@rhel1 ~]# grep -vE '^$|^#' /etc/xinetd.conf
    defaults
    {
        log_type    = SYSLOG daemon info
        log_on_failure  = HOST
        log_on_success  = PID HOST DURATION EXIT
        cps     = 50 10
        instances   = 50
        per_source  = 10
        v6only      = no
        groups      = yes
        umask       = 002
    }
    includedir /etc/xinetd.d


and here are the default services:

    [root@rhel1 ~]# ls /etc/xinetd.d
    chargen-dgram   daytime-stream  echo-dgram     time-dgram
    chargen-stream  discard-dgram   echo-stream    time-stream
    daytime-dgram   discard-stream  tcpmux-server


By default the super service is enabled:

    [root@rhel1 ~]# chkconfig --list xinetd
    xinetd          0:off   1:off   2:off   3:on    4:on    5:on    6:off


But the services it controls are all disabled:

    [root@rhel1 ~]# chkconfig --list | grep -i 'xinetd based' -A 17
    xinetd based services:
        chargen-dgram:  off
        chargen-stream: off
        daytime-dgram:  off
        daytime-stream: off
        discard-dgram:  off
        discard-stream: off
        echo-dgram:     off
        echo-stream:    off
        tcpmux-server:  off
        time-dgram:     off
        time-stream:    off


So let's install the **telnet-server**:

    [root@rhel1 ~]# yum install telnet-server


Here is the default configuration for the telnet service:

    [root@rhel1 ~]# cat /etc/xinetd.d/telnet
    # default: on
    # description: The telnet server serves telnet sessions; it uses \
    #   unencrypted username/password pairs for authentication.
    service telnet
    {
        flags       = REUSE
        socket_type = stream
        wait        = no
        user        = root
        server      = /usr/sbin/in.telnetd
        log_on_failure  += USERID
        disable     = yes
    }


Let's enable the service, add more logging, and only allow connections from our local network. Here is the configuration I had after I was done:

    [root@rhel1 ~]# cat /etc/xinetd.d/telnet
    # default: on
    # description: The telnet server serves telnet sessions; it uses \
    #   unencrypted username/password pairs for authentication.
    service telnet
    {
        flags       = REUSE IPv4
        socket_type = stream
        wait        = no
        user        = root
        server      = /usr/sbin/in.telnetd
        log_on_failure  += USERID
        log_on_success  += PID HOST EXIT
        only_from   = 192.168.2.0/24
        disable     = no
    }


Now let's start the xinetd service:

    [root@rhel1 ~]# service xinetd start
    Starting xinetd:  xinetd
    [root@rhel1 ~]# service xinetd status
    xinetd (pid  7329) is running...
    [root@rhel1 ~]# ps -eaf | grep xinetd
    root      7329     1  0 17:35 ?        00:00:00 xinetd -stayalive -pidfile /var/run/xinetd.pid


Let's also open up TCP 23 on the firewall:

    [root@rhel1 ~]# iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 23 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Lastly you will notice that there is no telnetd process running:

    [root@rhel1 ~]# ps -eaf | grep telnet
    [root@rhel1 ~]#


But instead **xinetd** is actually waiting for connections on port **23**:

    [root@rhel1 ~]# netstat -antp | grep 23
    tcp        0      0 0.0.0.0:23                  0.0.0.0:*                   LISTEN      7455/xinetd


Now on the client side, install the telnet client:

    [root@rhel2 ~]# yum install telnet


Then connect to our server:

    [root@rhel2 ~]# telnet rhel1
    Trying 192.168.2.2...
    Connected to rhel1.local.com (192.168.2.2).
    Escape character is '^]'.
    Red Hat Enterprise Linux Workstation release 6.1 (Santiago)
    Kernel 2.6.32-131.0.15.el6.i686 on an i686
    login: root
    Password:
    Login incorrect


in the **messages** log, I saw the following:

    [root@rhel1 ~]# tail /var/log/messages
    Apr 19 17:39:16 rhel1 xinetd[7455]: xinetd Version 2.3.14 started with libwrap loadavg labeled-networking options compiled in.
    Apr 19 17:39:16 rhel1 xinetd[7455]: Started working: 1 available service
    Apr 19 17:42:02 rhel1 xinetd[7455]: START: telnet pid=7466 from=192.168.2.3
    Apr 19 17:43:02 rhel1 xinetd[7455]: EXIT: telnet status=0 pid=7466 duration=60(sec)


A **telnet** process was started but my login failed, checking out the secure log, I saw the following:

    [root@rhel1 ~]# tail /var/log/secure
    Apr 19 17:42:05 rhel1 login: pam_securetty(remote:auth): access denied: tty 'pts/1' is not secure !
    Apr 19 17:42:10 rhel1 login: FAILED LOGIN 1 FROM rhel2 FOR root, Authentication failure


It looks like non-secure connections are getting blocked by PAM. To allow this unsecure connection (demonstration only). Add the following:

    pts/0
    pts/1
    pts/2


to the **/etc/securetty** file. After that I was able to login with **telnet**:

    [root@rhel2 ~]# telnet rhel1
    Trying 192.168.2.2...
    Connected to rhel1.local.com (192.168.2.2).
    Escape character is '^]'.
    Red Hat Enterprise Linux Workstation release 6.1 (Santiago)
    Kernel 2.6.32-131.0.15.el6.i686 on an i686
    login: root
    Password:
    Last login: Sat Apr 19 17:42:22 from rhel2
    [root@rhel1 ~]# ps -eaf | grep telnet
    root      7494  7455  0 17:46 ?        00:00:00 in.telnetd: rhel2.local.com
    root      7514  7500  0 17:47 pts/1    00:00:00 grep telnet
    [root@rhel1 ~]# tail /var/log/messages
    Apr 19 17:39:16 rhel1 xinetd[7455]: xinetd Version 2.3.14 started with libwrap loadavg labeled-networking options compiled in.
    Apr 19 17:39:16 rhel1 xinetd[7455]: Started working: 1 available service
    Apr 19 17:42:02 rhel1 xinetd[7455]: START: telnet pid=7466 from=192.168.2.3
    Apr 19 17:43:02 rhel1 xinetd[7455]: EXIT: telnet status=0 pid=7466 duration=60(sec)
    Apr 19 17:46:54 rhel1 xinetd[7455]: START: telnet pid=7494 from=192.168.2.3


After I closed the **telnet** connection, the daemon is stopped:

    [root@rhel1 log]# ps -eaf | grep telnet
    root      7524  6907  0 17:51 pts/0    00:00:00 grep telnet
    [root@rhel1 log]#


Try to connect from another network, I saw the following:

    elatov@fed:~$telnet rhel1
    Trying 192.168.1.109...
    Connected to rhel1.
    Escape character is '^]'.
    Connection closed by foreign host.


and I saw the following in the logs:

    [root@rhel1 ~]# tail -2 /var/log/messages
    Apr 19 17:53:24 rhel1 xinetd[7526]: FAIL: telnet address from=192.168.1.107
    Apr 19 17:53:24 rhel1 xinetd[7455]: EXIT: telnet status=0 pid=7526 duration=0(sec)


## DHCP

From the [Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> Dynamic Host Configuration Protocol (DHCP) is a network protocol that automatically assigns TCP/IP information to client machines. Each DHCP client connects to the centrally located DHCP server, which returns the network configuration (including the IP address, gateway, and DNS servers) of that client.
>
> DHCP is useful for automatic configuration of client network interfaces. When configuring the client system, you can choose DHCP instead of specifying an IP address, netmask, gateway, or DNS servers. The client retrieves this information from the DHCP server. DHCP is also useful if you want to change the IP addresses of a large number of systems. Instead of reconfiguring all the systems, you can just edit one configuration file on the server for the new set of IP addresses. If the DNS servers for an organization changes, the changes happen on the DHCP server, not on the DHCP clients. When you restart the network or reboot the clients, the changes go into effect.
>
> If an organization has a functional DHCP server correctly connected to a network, laptops and other mobile computer users can move these devices from office to office.

#### Configuring a DHCP Server

From the same guide:

> The dhcp package contains an Internet Systems Consortium (ISC) DHCP server. First, install the package as the superuser:
>
>     ~]# yum install dhcp
>
>
> Installing the dhcp package creates a file, **/etc/dhcp/dhcpd.conf**, which is merely an empty configuration file:
>
>     ~]# cat /etc/dhcp/dhcpd.conf
>     #
>     # DHCP Server Configuration file.
>     #   see /usr/share/doc/dhcp*/dhcpd.conf.sample
>
>
> The sample configuration file can be found at **/usr/share/doc/dhcp-<version>/dhcpd.conf.sample</version>**. You should use this file to help you configure **/etc/dhcp/dhcpd.conf**, which is explained in detail below.
>
> DHCP also uses the file **/var/lib/dhcpd/dhcpd.leases** to store the client lease database.

### DHCPD Configuration File

From the above guide:

> The first step in configuring a DHCP server is to create the configuration file that stores the network information for the clients. Use this file to declare options and global options for client systems.
>
> The configuration file can contain extra tabs or blank lines for easier formatting. Keywords are case-insensitive and lines beginning with a hash sign (**#**) are considered comments.
>
> There are two types of statements in the configuration file:
>
> *   **Parameters** - State how to perform a task, whether to perform a task, or what network configuration options to send to the client.
> *   **Declarations** - Describe the topology of the network, describe the clients, provide addresses for the clients, or apply a group of parameters to a group of declarations.
>
> The parameters that start with the keyword **option** are referred to as **options**. These options control DHCP options; whereas, parameters configure values that are not optional or control how the DHCP server behaves.
>
> Parameters (including options) declared before a section enclosed in curly brackets (**{ }**) are considered global parameters. Global parameters apply to all the sections below it.
>
> If the configuration file is changed, the changes do not take effect until the DHCP daemon is restarted with the command **service dhcpd restart**.
>
> Instead of changing a DHCP configuration file and restarting the service each time, using the **omshell** command provides an interactive way to connect to, query, and change the configuration of a DHCP server. By using **omshell**, all changes can be made while the server is running.
>
> In the below example, the **routers**, **subnet-mask**, **domain-search**, **domain-name-servers**, and **time-offset** options are used for any host statements declared below it.
>
> For every **subnet** which will be served, and for every **subnet** to which the DHCP server is connected, there must be one **subnet** declaration, which tells the DHCP daemon how to recognize that an address is on that subnet. A **subnet** declaration is required for each **subnet** even if no addresses will be dynamically allocated to that **subnet**.
>
> In this example, there are global options for every DHCP client in the **subnet** and a **range** declared. Clients are assigned an IP address within the range.
>
>     subnet 192.168.1.0 netmask 255.255.255.0 {
>             option routers                  192.168.1.254;
>             option subnet-mask              255.255.255.0;
>             option domain-search              "example.com";
>             option domain-name-servers       192.168.1.1;
>             option time-offset              -18000;     # Eastern Standard Time
>       range 192.168.1.10 192.168.1.100;
>     }
>
>
> To configure a DHCP server that leases a dynamic IP address to a system within a subnet, modify the below example with your values. It declares a **default lease time**, **maximum lease time**, and **network** configuration values for the clients. This example assigns IP addresses in the **range** 192.168.1.10 and 192.168.1.100 to client systems.
>
>     default-lease-time 600;
>     max-lease-time 7200;
>     option subnet-mask 255.255.255.0;
>     option broadcast-address 192.168.1.255;
>     option routers 192.168.1.254;
>     option domain-name-servers 192.168.1.1, 192.168.1.2;
>     option domain-search "example.com";
>     subnet 192.168.1.0 netmask 255.255.255.0 {
>        range 192.168.1.10 192.168.1.100;
>     }
>
>
> To assign an IP address to a client based on the MAC address of the network interface card, use the **hardware ethernet** parameter within a host declaration. As demonstrated in the below example, the host apex declaration specifies that the network interface card with the MAC address **00:A0:78:8E:9E:AA** always receives the IP address **192.168.1.4**.
>
> Note that you can also use the optional parameter **host-name** to assign a host name to the client.
>
>     host apex {
>        option host-name "apex.example.com";
>        hardware ethernet 00:A0:78:8E:9E:AA;
>        fixed-address 192.168.1.4;
>     }
>
>
> All subnets that share the same physical network should be declared within a **shared-network** declaration as shown in the below example. Parameters within the **shared-network**, but outside the enclosed **subnet** declarations, are considered to be global parameters. The name of the **shared-network** must be a descriptive title for the network, such as using the title '**test-lab**' to describe all the subnets in a test lab environment.
>
>     shared-network name {
>         option domain-search              "test.redhat.com";
>         option domain-name-servers      ns1.redhat.com, ns2.redhat.com;
>         option routers                  192.168.0.254;
>         more parameters for EXAMPLE shared-network
>         subnet 192.168.1.0 netmask 255.255.252.0 {
>             parameters for subnet
>             range 192.168.1.1 192.168.1.254;
>         }
>         subnet 192.168.2.0 netmask 255.255.252.0 {
>             parameters for subnet
>             range 192.168.2.1 192.168.2.254;
>         }
>     }
>
>
> As demonstrated in the below example, the **group** declaration is used to apply global parameters to a group of declarations. For example, shared networks, subnets, and hosts can be grouped.
>
>     group {
>        option routers                  192.168.1.254;
>        option subnet-mask              255.255.255.0;
>        option domain-search              "example.com";
>        option domain-name-servers       192.168.1.1;
>        option time-offset              -18000;     # Eastern Standard Time
>        host apex {
>           option host-name "apex.example.com";
>           hardware ethernet 00:A0:78:8E:9E:AA;
>           fixed-address 192.168.1.4;
>        }
>        host raleigh {
>           option host-name "raleigh.example.com";
>           hardware ethernet 00:A1:DD:74:C3:F2;
>           fixed-address 192.168.1.6;
>        }
>     }
>
>
> You can use the provided sample configuration file as a starting point and add custom configuration options to it. To copy this file to the proper location, use the following command:
>
>     cp /usr/share/doc/dhcp-<version_number>/dhcpd.conf.sample /etc/dhcp/dhcpd.conf
>
>
> ... where **version_number** is the DHCP version number.

### DHCP Lease Database

From the above guide:

> On the DHCP server, the file **/var/lib/dhcpd/dhcpd.leases** stores the DHCP client lease database. Do not change this file. DHCP lease information for each recently assigned IP address is automatically stored in the lease database. The information includes the length of the lease, to whom the IP address has been assigned, the start and end dates for the lease, and the MAC address of the network interface card that was used to retrieve the lease.
>
> All times in the lease database are in Coordinated Universal Time (UTC), not local time.
>
> The lease database is recreated from time to time so that it is not too large. First, all known leases are saved in a temporary lease database. The **dhcpd.leases** file is renamed **dhcpd.leases~** and the temporary lease database is written to **dhcpd.leases**.
>
> The DHCP daemon could be killed or the system could crash after the lease database has been renamed to the backup file but before the new file has been written. If this happens, the **dhcpd.leases** file does not exist, but it is required to start the service. Do not create a new lease file. If you do, all old leases are lost which causes many problems. The correct solution is to rename the **dhcpd.leases~** backup file to **dhcpd.leases** and then start the daemon.

### Starting and stopping the DHCP Server

From the Deployment Guide:

> When the DHCP server is started for the first time, it fails unless the **dhcpd.leases** file exists. Use the command **touch /var/lib/dhcpd/dhcpd.leases** to create the file if it does not exist.
>
> If the same server is also running BIND as a DNS server, this step is not necessary, as starting the named service automatically checks for a **dhcpd.leases** file.
>
> To start the DHCP service, use the command **/sbin/service dhcpd start**. To stop the DHCP server, use the command **/sbin/service dhcpd stop**.
>
> By default, the DHCP service does not start at boot time.
>
> If more than one network interface is attached to the system, but the DHCP server should only be started on one of the interfaces, configure the DHCP server to start only on that device. In **/etc/sysconfig/dhcpd**, add the name of the interface to the list of DHCPDARGS:
>
>     # Command line options here
>     DHCPDARGS=eth0
>
>
> This is useful for a firewall machine with two network cards. One network card can be configured as a DHCP client to retrieve an IP address to the Internet. The other network card can be used as a DHCP server for the internal network behind the firewall. Specifying only the network card connected to the internal network makes the system more secure because users can not connect to the daemon via the Internet.
>
> Other command line options that can be specified in **/etc/sysconfig/dhcpd** include:
>
> *   **-p portnum** - Specifies the UDP port number on which dhcpd should listen. The default is port **67**. The DHCP server transmits responses to the DHCP clients at a port number one greater than the UDP port specified. For example, if the default port **67** is used, the server listens on port **67** for requests and responds to the client on port **68**. If a port is specified here and the DHCP relay agent is used, the same port on which the DHCP relay agent should listen must be specified.
> *   **-f** - Runs the daemon as a foreground process. This is mostly used for debugging.
> *   **-d** - Logs the DHCP server daemon to the standard error descriptor. This is mostly used for debugging. If this is not specified, the log is written to **/var/log/messages**.
> *   **-cf filename** - Specifies the location of the configuration file. The default location is **/etc/dhcp/dhcpd.conf**.
> *   **-lf filename** - Specifies the location of the lease database file. If a lease database file already exists, it is very important that the same file be used every time the DHCP server is started. It is strongly recommended that this option only be used for debugging purposes on non-production machines. The default location is **/var/lib/dhcpd/dhcpd.leases**.
> *   **-q** - Do not print the entire copyright message when starting the daemon.

### DHCP Relay Agent

From the same guide:

> The DHCP Relay Agent (**dhcrelay**) allows for the relay of DHCP and BOOTP requests from a subnet with no DHCP server on it to one or more DHCP servers on other subnets.
>
> When a DHCP client requests information, the DHCP Relay Agent forwards the request to the list of DHCP servers specified when the DHCP Relay Agent is started. When a DHCP server returns a reply, the reply is broadcast or unicast on the network that sent the original request.
>
> The DHCP Relay Agent listens for DHCP requests on all interfaces unless the interfaces are specified in **/etc/sysconfig/dhcrelay** with the **INTERFACES** directive.
>
> To start the DHCP Relay Agent, use the command **service dhcrelay start**.

### Configuring a Multihomed DHCP Server

From the above guide:

> A multihomed DHCP server serves multiple networks, that is, multiple subnets. The examples in these sections detail how to configure a DHCP server to serve multiple networks, select which network interfaces to listen on, and how to define network settings for systems that move networks.
>
> Before making any changes, back up the existing **/etc/sysconfig/dhcpd** and **/etc/dhcp/dhcpd.conf** files.
>
> The DHCP daemon listens on all network interfaces unless otherwise specified. Use the **/etc/sysconfig/dhcpd** file to specify which network interfaces the DHCP daemon listens on. The following **/etc/sysconfig/dhcpd** example specifies that the DHCP daemon listens on the **eth0** and **eth1** interfaces:
>
>     DHCPDARGS="eth0 eth1";
>
>
> If a system has three network interfaces cards - **eth0**, **eth1**, and **eth2** - and it is only desired that the DHCP daemon listens on the **eth0** card, then only specify **eth0** in **/etc/sysconfig/dhcpd**:
>
>     DHCPDARGS="eth0";
>
>
> The following is a basic **/etc/dhcp/dhcpd.conf** file, for a server that has two network interfaces, **eth0** in a **10.0.0.0/24** network, and **eth1** in a **172.16.0.0/24** network. Multiple subnet declarations allow you to define different settings for multiple networks:
>
>     default-lease-time 600;
>     max-lease-time 7200;
>     subnet 10.0.0.0 netmask 255.255.255.0 {
>       option subnet-mask 255.255.255.0;
>       option routers 10.0.0.1;
>       range 10.0.0.5 10.0.0.15;
>     }
>     subnet 172.16.0.0 netmask 255.255.255.0 {
>       option subnet-mask 255.255.255.0;
>       option routers 172.16.0.1;
>       range 172.16.0.5 172.16.0.15;
>     }
>
>
> #### subnet 10.0.0.0 netmask 255.255.255.0;
>
> A **subnet** declaration is required for every network your DHCP server is serving. Multiple subnets require multiple subnet declarations. If the DHCP server does not have a network interface in a range of a subnet declaration, the DHCP server does not serve that network.
>
> If there is only one subnet declaration, and no network interfaces are in the range of that subnet, the DHCP daemon fails to start, and an error such as the following is logged to **/var/log/messages**:
>
>     dhcpd: No subnet declaration for eth0 (0.0.0.0).
>     dhcpd: ** Ignoring requests on eth0.  If this is not what
>     dhcpd:    you want, please write a subnet declaration
>     dhcpd:    in your dhcpd.conf file for the network segment
>     dhcpd:    to which interface eth1 is attached. **
>     dhcpd:
>     dhcpd:
>     dhcpd: Not configured to listen on any interfaces!
>
>
> #### option subnet-mask 255.255.255.0;
>
> The **option subnet-mask** option defines a subnet mask, and overrides the **netmask** value in the **subnet** declaration. In simple cases, the subnet and netmask values are the same.
>
> #### option routers 10.0.0.1;
>
> The **option routers** option defines the default gateway for the subnet. This is required for systems to reach internal networks on a different subnet, as well as external networks.
>
> #### range 10.0.0.5 10.0.0.15;
>
> The **range** option specifies the pool of available IP addresses. Systems are assigned an address from the range of specified IP addresses.

### Configuring a single system for multiple networks

From the Deployment Guide:

> The following **/etc/dhcp/dhcpd.conf** example creates two subnets, and configures an IP address for the same system, depending on which network it connects to:
>
>     default-lease-time 600;
>     max-lease-time 7200;
>     subnet 10.0.0.0 netmask 255.255.255.0 {
>       option subnet-mask 255.255.255.0;
>       option routers 10.0.0.1;
>       range 10.0.0.5 10.0.0.15;
>     }
>     subnet 172.16.0.0 netmask 255.255.255.0 {
>       option subnet-mask 255.255.255.0;
>       option routers 172.16.0.1;
>       range 172.16.0.5 172.16.0.15;
>     }
>     host example0 {
>       hardware ethernet 00:1A:6B:6A:2E:0B;
>       fixed-address 10.0.0.20;
>     }
>     host example1 {
>       hardware ethernet 00:1A:6B:6A:2E:0B;
>       fixed-address 172.16.0.20;
>     }
>
>
> #### host example0
>
> The host declaration defines specific parameters for a single system, such as an IP address. To configure specific parameters for multiple hosts, use multiple **host** declarations.
>
> Most DHCP clients ignore the name in **host** declarations, and as such, this name can be anything, as long as it is unique to other **host** declarations. To configure the same system for multiple networks, use a different name for each **host** declaration, otherwise the DHCP daemon fails to start. Systems are identified by the **hardware ethernet** option, not the name in the host declaration.
>
> #### hardware ethernet 00:1A:6B:6A:2E:0B;
>
> The **hardware ethernet** option identifies the system. To find this address, run the **ip link** command.
>
> #### fixed-address 10.0.0.20;
>
> The **fixed-address** option assigns a valid IP address to the system specified by the **hardware ethernet** option. This address must be outside the IP address pool specified with the **range** option.
>
> If option statements do not end with a semicolon, the DHCP daemon fails to start, and an error such as the following is logged to **/var/log/messages**:
>
>     /etc/dhcp/dhcpd.conf line 20: semicolon expected.
>     dhcpd: }
>     dhcpd: ^
>     dhcpd: /etc/dhcp/dhcpd.conf line 38: unexpected end of file
>     dhcpd:
>     dhcpd: ^
>     dhcpd: Configuration file errors encountered -- exiting
>

### Configuring systems with multiple network interfaces

From the same guide:

> The following **host** declarations configure a single system, which has multiple network interfaces, so that each interface receives the same IP address. This configuration will not work if both network interfaces are connected to the same network at the same time:
>
>     host interface0 {
>       hardware ethernet 00:1a:6b:6a:2e:0b;
>       fixed-address 10.0.0.18;
>     }
>     host interface1 {
>       hardware ethernet 00:1A:6B:6A:27:3A;
>       fixed-address 10.0.0.18;
>     }
>
>
> For this example, **interface0** is the first network interface, and **interface1** is the second interface. The different **hardware ethernet** options identify each interface.
>
> If such a system connects to another network, add more host declarations, remembering to:
>
> *   assign a valid fixed-address for the network the host is connecting to.
> *   make the name in the host declaration unique.
>
> When a name given in a host declaration is not unique, the DHCP daemon fails to start, and an error such as the following is logged to **/var/log/messages**:
>
>     dhcpd: /etc/dhcp/dhcpd.conf line 31: host interface0: already exists
>     dhcpd: }
>     dhcpd: ^
>     dhcpd: Configuration file errors encountered -- exiting
>
>
> This error was caused by having multiple host **interface0** declarations defined in **/etc/dhcp/dhcpd.conf**.

### DHCPD Example

First go ahead and install the server:

    [root@rhel1 ~]# yum install dhcp


As promised the config is blank:

    [root@rhel1 ~]# cat /etc/dhcp/dhcpd.conf
    #
    # DHCP Server Configuration file.
    #   see /usr/share/doc/dhcp*/dhcpd.conf.sample
    #   see 'man 5 dhcpd.conf'
    #


Let's copy the sample:

    [root@rhel1 ~]# cp /usr/share/doc/dhcp*/dhcpd.conf.sample /etc/dhcp/dhcpd.conf
    cp: overwrite `/etc/dhcp/dhcpd.conf'? y


Here is the sample configuration:

    [root@rhel1 ~]# grep -vE '^$|^#' /etc/dhcp/dhcpd.conf
    option domain-name "example.org";
    option domain-name-servers ns1.example.org, ns2.example.org;
    default-lease-time 600;
    max-lease-time 7200;
    log-facility local7;
    subnet 10.152.187.0 netmask 255.255.255.0 {
    }
    subnet 10.254.239.0 netmask 255.255.255.224 {
      range 10.254.239.10 10.254.239.20;
      option routers rtr-239-0-1.example.org, rtr-239-0-2.example.org;
    }
    subnet 10.254.239.32 netmask 255.255.255.224 {
      range dynamic-bootp 10.254.239.40 10.254.239.60;
      option broadcast-address 10.254.239.31;
      option routers rtr-239-32-1.example.org;
    }
    subnet 10.5.5.0 netmask 255.255.255.224 {
      range 10.5.5.26 10.5.5.30;
      option domain-name-servers ns1.internal.example.org;
      option domain-name "internal.example.org";
      option routers 10.5.5.1;
      option broadcast-address 10.5.5.31;
      default-lease-time 600;
      max-lease-time 7200;
    }
    host passacaglia {
      hardware ethernet 0:0:c0:5d:bd:95;
      filename "vmunix.passacaglia";
      server-name "toccata.fugue.com";
    }
    host fantasia {
      hardware ethernet 08:00:07:26:c0:a5;
      fixed-address fantasia.fugue.com;
    }
    class "foo" {
      match if substring (option vendor-class-identifier, 0, 4) = "SUNW";
    }
    shared-network 224-29 {
      subnet 10.17.224.0 netmask 255.255.255.0 {
        option routers rtr-224.example.org;
      }
      subnet 10.0.29.0 netmask 255.255.255.0 {
        option routers rtr-29.example.org;
      }
      pool {
        allow members of "foo";
        range 10.17.224.10 10.17.224.250;
      }
      pool {
        deny members of "foo";
        range 10.0.29.10 10.0.29.230;
      }
    }


Let's clean up the file and create a very basic configuration:

    [root@rhel1 dhcp-4.1.1]# cat /etc/dhcp/dhcpd.conf
    # dhcpd.conf
    #
    # Sample configuration file for ISC dhcpd
    #
    default-lease-time 600;
    max-lease-time 7200;
    subnet 192.168.2.0 netmask 255.255.255.0 {
        option domain-name "local.com";
        option domain-name-servers       192.168.2.1;
        option subnet-mask 255.255.255.0;
        option routers 192.168.2.2;
        range 192.168.2.3 192.168.2.9;
    }
    option domain-name-servers ns1.example.org, ns2.example.org;

    log-facility local7;


Now let's limit the DHCP server to only listen on our **eth1** interface. This is done by modifying the following line in the **/etc/sysconfig/dhcpd** file:

    [root@rhel1 ~]# grep DHCP /etc/sysconfig/dhcpd
    DHCPDARGS="eth1"


Now let's open up the firewall to allow UDP port 67:

    iptables -I INPUT 14 -m udp -p udp --dport 67 -j ACCEPT
    service iptables save


Lastly let's make sure the configuration is okay and then start the service:

    [root@rhel1 ~]# service dhcpd configtest
    Syntax: OK
    [root@rhel1 ~]# service dhcpd start
    Starting dhcpd:  dhcpd
    [root@rhel1 ~]# service dhcpd status
    dhcpd (pid  7651) is running...


From the client, try to get an IP really fast with the **dhclient** utility:

    [root@rhel2 ~]# yum install dhclient
    [root@rhel2 ~]# dhclient eth1
    Internet Systems Consortium DHCP Client V3.0.5-RedHat
    Copyright 2004-2006 Internet Systems Consortium.
    All rights reserved.
    For info, please visit http://www.isc.org/sw/dhcp/

    Listening on LPF/eth1/00:0c:29:4f:a1:ef
    Sending on   LPF/eth1/00:0c:29:4f:a1:ef
    Sending on   Socket/fallback
    DHCPDISCOVER on eth1 to 255.255.255.255 port 67 interval 6
    DHCPOFFER from 192.168.2.2
    DHCPREQUEST on eth1 to 255.255.255.255 port 67
    DHCPACK from 192.168.2.2
    bound to 192.168.2.3 -- renewal in 232 seconds.


After you get the IP, you will see your **/etc/resolv.conf** file modified:

    [root@rhel2 ~]# cat /etc/resolv.conf
    ; generated by /sbin/dhclient-script
    search local.com
    nameserver 192.168.2.1


Then on the server side, make sure the DHCP lease database is updated:

    [root@rhel1 ~]# cat /var/lib/dhcpd/dhcpd.leases
    # The format of this file is documented in the dhcpd.leases(5) manual page.
    # This lease file was written by isc-dhcp-4.1.1-P1

    server-duid "\000\001\000\001\032\345\326g\000\014)\024\205I";

    lease 192.168.2.3 {
      starts 0 2014/04/20 00:53:36;
      ends 0 2014/04/20 01:03:36;
      cltt 0 2014/04/20 00:53:36;
      binding state active;
      next binding state free;
      hardware ethernet 00:0c:29:4f:a1:ef;
    }


And in the logs on the server side, I saw the following:

    [root@rhel1 log]# tail /var/log/messages
    Apr 19 18:50:47 rhel1 dhcpd: Copyright 2004-2010 Internet Systems Consortium.
    Apr 19 18:50:47 rhel1 dhcpd: All rights reserved.
    Apr 19 18:50:47 rhel1 dhcpd: For info, please visit https://www.isc.org/software/dhcp/
    Apr 19 18:50:47 rhel1 dhcpd: Wrote 0 leases to leases file.
    Apr 19 18:50:47 rhel1 dhcpd: Listening on LPF/eth1/00:0c:29:14:85:49/192.168.2.0/24
    Apr 19 18:50:47 rhel1 dhcpd: Sending on   LPF/eth1/00:0c:29:14:85:49/192.168.2.0/24
    Apr 19 18:50:47 rhel1 dhcpd: Sending on   Socket/fallback/fallback-net
    Apr 19 18:53:35 rhel1 dhcpd: DHCPDISCOVER from 00:0c:29:4f:a1:ef via eth1
    Apr 19 18:53:36 rhel1 dhcpd: DHCPOFFER on 192.168.2.3 to 00:0c:29:4f:a1:ef via eth1
    Apr 19 18:53:36 rhel1 dhcpd: DHCPREQUEST for 192.168.2.3 (192.168.2.2) from 00:0c:29:4f:a1:ef via eth1
    Apr 19 18:53:36 rhel1 dhcpd: DHCPACK on 192.168.2.3 to 00:0c:29:4f:a1:ef via eth1


On the client itself, I saw the following in the logs:

    Apr 19 18:53:35 rhel2 dhclient: Internet Systems Consortium DHCP Client V3.0.5-RedHat
    Apr 19 18:53:35 rhel2 dhclient: Copyright 2004-2006 Internet Systems Consortium.
    Apr 19 18:53:35 rhel2 dhclient: All rights reserved.
    Apr 19 18:53:35 rhel2 dhclient: For info, please visit http://www.isc.org/sw/dhcp/
    Apr 19 18:53:35 rhel2 dhclient:
    Apr 19 18:53:35 rhel2 avahi-daemon[2863]: Leaving mDNS multicast group on interface eth1.IPv4 with address 192.168.2.3.
    Apr 19 18:53:35 rhel2 avahi-daemon[2863]: iface.c: interface_mdns_mcast_join() called but no local address available.
    Apr 19 18:53:35 rhel2 avahi-daemon[2863]: Interface eth1.IPv4 no longer relevant for mDNS.
    Apr 19 18:53:35 rhel2 dhclient: Listening on LPF/eth1/00:0c:29:4f:a1:ef
    Apr 19 18:53:35 rhel2 dhclient: Sending on   LPF/eth1/00:0c:29:4f:a1:ef
    Apr 19 18:53:35 rhel2 dhclient: Sending on   Socket/fallback
    Apr 19 18:53:35 rhel2 dhclient: DHCPDISCOVER on eth1 to 255.255.255.255 port 67 interval 6
    Apr 19 18:53:36 rhel2 dhclient: DHCPOFFER from 192.168.2.2
    Apr 19 18:53:36 rhel2 dhclient: DHCPREQUEST on eth1 to 255.255.255.255 port 67
    Apr 19 18:53:36 rhel2 dhclient: DHCPACK from 192.168.2.2
    Apr 19 18:53:36 rhel2 avahi-daemon[2863]: New relevant interface eth1.IPv4 for mDNS.
    Apr 19 18:53:36 rhel2 avahi-daemon[2863]: Joining mDNS multicast group on interface eth1.IPv4 with address 192.168.2.3.
    Apr 19 18:53:36 rhel2 NET[5938]: /sbin/dhclient-script : updated /etc/resolv.conf
    Apr 19 18:53:36 rhel2 dhclient: bound to 192.168.2.3 -- renewal in 232 seconds.
    Apr 19 18:53:36 rhel2 avahi-daemon[2863]: Registering new address record for 192.168.2.3 on eth1.


### Configuring a DHCP Client

If you want to configure your client to use DHCP permanently, we have to do the following. From the Deployment guide:

> To configure a DHCP client manually, modify the **/etc/sysconfig/network** file to enable networking and the configuration file for each network device in the **/etc/sysconfig/network-scripts** directory. In this directory, each device should have a configuration file named **ifcfg-eth0**, where **eth0** is the network device name.
>
> Make sure that the **/etc/sysconfig/network-scripts/ifcfg-eth0** file contains the following lines:
>
>     DEVICE=eth0
>     BOOTPROTO=dhcp
>     ONBOOT=yes
>
>
> To use DHCP, set a configuration file for each device.
>
> Other options for the network script include:
>
> *   **DHCP_HOSTNAME** - Only use this option if the DHCP server requires the client to specify a hostname before receiving an IP address.
> *   **PEERDNS=answer**, where **answer** is one of the following:
>     *   **yes** - Modify **/etc/resolv.conf** with information from the server. If using DHCP, then yes is the default.
>     *   **no** - Do not modify **/etc/resolv.conf**.

## NTP

From the [Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> The Network Time Protocol (NTP) enables the accurate dissemination of time and date information in order to keep the time clocks on networked computer systems synchronized to a common reference over the network or the Internet. Many standards bodies around the world have atomic clocks which may be made available as a reference. The satellites that make up the Global Position System contain more than one atomic clock, making their time signals potentially very accurate. Their signals can be deliberately degraded for military reasons. An ideal situation would be where each site has a server, with its own reference clock attached, to act as a site-wide time server. Many devices which obtain the time and date via low frequency radio transmissions or the Global Position System (GPS) exist. However for most situations, a range of publicly accessible time servers connected to the Internet at geographically dispersed locations can be used. These **NTP** servers provide “Coordinated Universal Time” (UTC). Information about these time servers can found at *www.pool.ntp.org*.
>
> Accurate time keeping is important for a number of reasons in IT. In networking for example, accurate time stamps in packets and logs are required. Logs are used to investigate service and security issues and so timestamps made on different systems must be made by synchronized clocks to be of real value. As systems and networks become increasingly faster, there is a corresponding need for clocks with greater accuracy and resolution. In Linux systems, NTP is implemented by a daemon running in user space. The default NTP daemon in Red Hat Enterprise Linux 6 is **ntpd**.
>
> The user space daemon updates the system clock, which is a software clock running in the kernel. Linux uses a software clock as its system clock for better resolution than the typical embedded hardware clock referred to as the “Real Time Clock” (RTC). See the **rtc**(4) and **hwclock**(8) man pages for information on hardware clocks. The system clock can keep time by using various clock sources. Usually, the Time Stamp Counter (TSC) is used. The TSC is a CPU register which counts the number of cycles since it was last reset. It is very fast, has a high resolution, and there are no interrupts. On system start, the system clock reads the time and date from the RTC. The time kept by the RTC will drift away from actual time by up to 5 minutes per month due to temperature variations. Hence the need for the system clock to be constantly synchronized with external time references and to update the RTC on system shut down. When the system clock is being synchronized by **ntpd**, the kernel will in turn update the RTC every 11 minutes automatically.

### NTP Strata

From the same guide:

> **NTP** servers are classified according to their synchronization distance from the atomic clocks which are the source of the time signals. The servers are thought of as being arranged in layers, or strata, from 1 at the top down to 15. Hence the word stratum is used when referring to a specific layer. Atomic clocks are referred to as Stratum 0 as this is the source, but no Stratum 0 packet is sent on the Internet, all stratum 0 atomic clocks are attached to a server which is referred to as stratum 1. These servers send out packets marked as Stratum 1. A server which is synchronized by means of packets marked stratum **n** belongs to the next, lower, stratum and will mark its packets as stratum **n+1**. Servers of the same stratum can exchange packets with each other but are still designated as belonging to just the one stratum, the stratum one below the best reference they are synchronized to. The designation Stratum 16 is used to indicate that the server is not currently synchronized to a reliable time source.
>
> Note that by default **NTP** clients act as servers for those systems in the stratum below them.
>
> Here is a summary of the NTP Strata:
>
> *   **Stratum 0**- Atomic Clocks and their signals broadcast over Radio and GPS
>
>     *   GPS (Global Positioning System)
>     *   Mobile Phone Systems
>     *   Low Frequency Radio Broadcasts WWVB (Colorado, USA.), JJY-40 and JJY-60 (Japan), DCF77 (Germany), and MSF (United Kingdom)
>
>     These signals can be received by dedicated devices and are usually connected by RS-232 to a system used as an organizational or site-wide time server.
>
> *   **Stratum 1** - Computer with radio clock, GPS clock, or atomic clock attached
>
> *   **Stratum 2** - Reads from stratum 1; Serves to lower strata
>
> *   **Stratum 3** - Reads from stratum 2; Serves to lower strata
>
> *   **Stratum n+1** - Reads from stratum n; Serves to lower strata
> *   **Stratum 15** - Reads from stratum 14; This is the lowest stratum.
>
> This process continues down to Stratum 15 which is the lowest valid stratum. The label Stratum 16 is used to indicated an unsynchronized state.

### NTPD

From the above guide:

> The version of NTP used by Red Hat Enterprise Linux is as described in *RFC 1305 Network Time Protocol (Version 3) Specification, Implementation and Analysis and RFC 5905 Network Time Protocol Version 4: Protocol and Algorithms Specification*
>
> This implementation of NTP enables sub-second accuracy to be achieved. Over the Internet, accuracy to 10s of milliseconds is normal. On a Local Area Network (LAN), 1 ms accuracy is possible under ideal conditions. This is because clock drift is now accounted and corrected for, which was not done in earlier, simpler, time protocol systems. A resolution of 233 picoseconds is provided by using 64-bit timestamps: 32-bits for seconds, 32-bits for fractional seconds.
>
> NTP represents the time as a count of the number of seconds since 00:00 (midnight) 1 January, 1900 GMT. As 32-bits is used to count the seconds, this means the time will “roll over” in 2036. However **NTP** works on the difference between timestamps so this does not present the same level of problem as other implementations of time protocols have done. If a hardware clock accurate to better than 68 years is available at boot time then **NTP** will correctly interpret the current date. The **NTP4** specification provides for an “Era Number” and an “Era Offset” which can be used to make software more robust when dealing with time lengths of more than 68 years. Note, please do not confuse this with the Unix Year 2038 problem.
>
> The **NTP** protocol provides additional information to improve accuracy. Four timestamps are used to allow the calculation of round-trip time and server response time. In order for a system in its role as **NTP** client to synchronize with a reference time server, a packet is sent with an “originate timestamp”. When the packet arrives, the time server adds a “receive timestamp”. After processing the request for time and date information and just before returning the packet, it adds a “transmit timestamp”. When the returning packet arrives at the **NTP** client, a “receive timestamp” is generated. The client can now calculate the total round trip time and by subtracting the processing time derive the actual traveling time. By assuming the outgoing and return trips take equal time, the single-trip delay in receiving the NTP data is calculated. The full **NTP** algorithm is much more complex then presented here.
>
> Each packet containing time information received is not immediately acted upon, but is subject to validation checks and then used together with several other samples to arrive at a reasonably good estimate of the time. This is then compared to the system clock to determine the time offset, that is to say, the difference between the system clock's time and what **ntpd** has determined the time should be. The system clock is adjusted slowly, at most at a rate of 0.5ms per second, to reduce this offset by changing the frequency of the counter being used. It will take at least 2000 seconds to adjust the clock by 1 second using this method. This slow change is referred to as slewing and cannot go backwards. If the time offset of the clock is more than 128ms (the default setting), **ntpd** can “**step**” the clock forwards or backwards. If the time offset at system start is greater than 1000 seconds then the user, or an installation script, should make a manual adjustment. With the **-g** option to the **ntpd** command (used by default), any offset at system start will be corrected, but during normal operation only offsets of up to 1000 seconds will be corrected.
>
> Some software may fail or produce an error if the time is changed backwards. For systems that are sensitive to step changes in the time, the threshold can be changed to 600s instead of 128ms using the **-x** option (unrelated to the **-g** option). Using the **-x** option to increase the stepping limit from 0.128s to 600s has a drawback because a different method of controlling the clock has to be used. It disables the kernel clock discipline and may have a negative impact on the clock accuracy. The **-x** option can be added to the **/etc/sysconfig/ntpd** configuration file.

### NTPD Drift File

From the deployment guide:

> The drift file is used to store the frequency offset between the system clock running at its nominal frequency and the frequency required to remain in synchronization with UTC. If present, the value contained in the drift file is read at system start and used to correct the clock source. Use of the drift file reduces the time required to achieve a stable and accurate time. The value is calculated, and the drift file replaced, once per hour by **ntpd**. The drift file is replaced, rather than just updated, and for this reason the drift file must be in a directory for which the **ntpd** has write permissions.

### Timezones

From the same guide:

> As NTP is entirely in UTC (Universal Time, Coordinated), Timezones and DST (Daylight Saving Time) are applied locally by the system. The file **/etc/localtime** is a copy of, or symlink to, a zone information file from **/usr/share/zoneinfo**. The RTC may be in localtime or in UTC, as specified by the 3rd line of **/etc/adjtime**, which will be one of LOCAL or UTC to indicate how the RTC clock has been set. Users can easily change this setting using the checkbox **System Clock Uses UTC** in the **system-config-date** graphical configuration tool. Running the RTC in UTC is recommended to avoid various problems when daylight saving time is changed.

### NTPD Configuration Files

From the above guide:

> The daemon, **ntpd**, reads the configuration file at system start or when the service is restarted. The default location for the file is **/etc/ntp.conf** and you can view the file by entering the following command:
>
>     ~]$ less /etc/ntp.conf
>
>
> Here follows a brief explanation of the contents of the default configuration file:
>
> *   **The driftfile entry** - A path to the drift file is specified, the default entry on Red Hat Enterprise Linux is:
>
>         driftfile /var/lib/ntp/drift
>
>
>     If you change this be certain that the directory is writable by **ntpd**. The file contains one value used to adjust the system clock frequency after every system or service start.
>
> *   **The access control entries** - The following lines setup the default access control restrictions:
>
>         restrict default kod nomodify notrap nopeer noquery
>         restrict -6 default kod nomodify notrap nopeer noquery
>
>
>     The **kod** option means a “Kiss-o'-death” packet is to be sent to reduce unwanted queries. The **nomodify** options prevents any changes to the configuration. The **notrap** option prevents **ntpdc** control message protocol traps. The **nopeer** option prevents a peer association being formed. The **noquery** option prevents **ntpq** and **ntpdc** queries, but not time queries, from being answered. The **-6** option is required before an IPv6 address.
>
>     Addresses within the range **127.0.0.0/8** range are sometimes required by various processes or applications. As the "restrict default" line above prevents access to everything not explicitly allowed, access to the standard loopback address for IPv4 and IPv6 is permitted by means of the following lines:
>
>         # the administrative functions.
>         restrict 127.0.0.1
>         restrict -6 ::1
>
>
>     Addresses can be added underneath if specifically required by another application. The **-6** option is required before an IPv6 address.
>
>     Hosts on the local network are not permitted because of the "restrict default" line above. To change this, for example to allow hosts from the **192.0.2.0/24** network to query the time and statistics but nothing more, a line in the following format is required:
>
>         restrict 192.0.2.0 mask 255.255.255.0 nomodify notrap nopeer
>
>
>     To allow unrestricted access from a specific host, for example **192.0.2.250/24**, a line in the following format is required:
>
>         restrict 192.0.2.250
>
>
>     A mask of **255.255.255.255** is applied if none is specified.
>
>     The restrict commands are explained in the **ntp_acc**(5) man page.
>
> *   **The public servers entry** - By default, as of Red Hat Enterprise 6.5, the **ntp.conf** file contains four public server entries:
>
>         server 0.rhel.pool.ntp.org iburst
>         server 1.rhel.pool.ntp.org iburst
>         server 2.rhel.pool.ntp.org iburst
>         server 3.rhel.pool.ntp.org iburst
>
>
>     If upgrading from a previous minor release, and your **/etc/ntp.conf** file has been modified, then the upgrade to Red Hat Enterprise Linux 6.5 will create a new file **/etc/ntp.conf.rpmnew** and will not alter the existing **/etc/ntp.conf** file.

### NTPD Sysconfig File

From the Deployment Guide:

> The file will be read by the **ntpd** init script on service start. The default contents is as follows:
>
>     # Drop root to id 'ntp:ntp' by default.
>     OPTIONS="-u ntp:ntp -p /var/run/ntpd.pid -g"
>
>
> The **-g** option enables ntpd to ignore the offset limit of 1000s and attempt to synchronize the time even if the offset is larger than 1000s, but only on system start. Without that option ntpd will exit if the time offset is greater than 1000s. It will also exit after system start if the service is restarted and the offset is greater than 1000s even with the **-g** option.
>
> The **-p** option sets the path to the pid file and **-u** sets the user and group to which the daemon should drop the root privileges.

### Checking the Status of NTP

From the same guide:

> To check if **ntpd** is configured to run at system start, issue the following command:
>
>     ~]$ chkconfig --list ntpd
>     ntpd              0:off   1:off   2:on    3:on    4:on    5:on    6:off
>
>
> By default, when **ntpd** is installed, it is configured to start at every system start.
>
> To check if **ntpd** is running, issue the following command:
>
>     ~]$ ntpq -p
>          remote           refid      st t when poll reach   delay   offset  jitter
>     ==============================================================================
>     +clock.util.phx2 .CDMA.           1 u  111  128  377  175.495    3.076   2.250
>     *clock02.util.ph .CDMA.           1 u   69  128  377  175.357    7.641   3.671
>      ms21.snowflakeh .STEP.          16 u    - 1024    0    0.000    0.000   0.000
>      rs11.lvs.iif.hu .STEP.          16 u    - 1024    0    0.000    0.000   0.000
>      2001:470:28:bde .STEP.          16 u    - 1024    0    0.000    0.000   0.000
>
>
> The command lists connected time servers and displays information indicating when they were last polled and the stability of the replies. The column headings are as follows:
>
> *   **remote and refid** - remote NTP server, and its NTP server
> *   **st** - stratum of server
> *   **t** - type of server (local, unicast, multicast, or broadcast)
> *   **poll** - how frequently to query server (in seconds)
> *   **when** - how long since last poll (in seconds)
> *   **reach** - octal bitmask of success or failure of last 8 queries (left-shifted); 377 = 11111111 = all recent queries were successful; 257 = 10101111 = 4 most recent were successful, 5 and 7 failed
> *   **delay** - network round trip time (in milliseconds)
> *   **offset** - difference between local clock and remote clock (in milliseconds)
> *   **jitter** - difference of successive time values from server (high jitter could be due to an unstable clock or, more likely, poor network performance)
>
> To obtain a brief status report from **ntpd**, issue the following command:
>
>     ~]$ ntpstat
>     unsynchronised
>       time server re-starting
>        polling server every 64 s
>     ~]$ ntpstat
>     synchronised to NTP server (10.5.26.10) at stratum 2
>        time correct to within 52 ms
>        polling server every 1024 s
>

### ntpdate Servers

From the above guide:

> The purpose of the **ntpdate** service is to set the clock during system boot. This can be used to ensure that the services started after **ntpdate** will have the correct time and will not observe a jump in the clock. The use of **ntpdate** and the list of **step-tickers** is considered deprecated and so **Red Hat Enterprise Linux 6** uses the **-g** option to the **ntpd** command by default and not **ntpdate**. However, the **-g** option only enables ntpd to ignore the offset limit of 1000s and attempt to synchronize the time. It does not guarantee the time will be correct when other programs or services are started. Therefore the **ntpdate** service can be useful when **ntpd** is disabled or if there are services which need to be started with the correct time and not observe a jump in the clock.
>
> To check if the ntpdate service is enabled to run at system start, issue the following command:
>
>     ~]$ chkconfig --list ntpdate
>     ntpdate           0:off   1:off   2:on    3:on    4:on    5:on    6:off
>
>
> To enable the service to run at system start, issue the following command as root:
>
>     ~]# chkconfig ntpdate on
>
>
> To configure ntpdate servers, using a text editor running as root, edit **/etc/ntp/step-tickers** to include one or more host names as follows:
>
>     clock1.example.com
>     clock2.example.com
>
>
> The number of servers listed is not very important as **ntpdate** will only use this to obtain the date information once when the system is starting. If you have an internal time server then use that host name for the first line. An additional host on the second line as a backup is sensible. The selection of backup servers and whether the second host is internal or external depends on your risk assessment. For example, what is the chance of any problem affecting the fist server also affecting the second server? Would connectivity to an external server be more likely to be available than connectivity to internal servers in the event of a network failure disrupting access to the first server?
>
> The **ntpdate** service has a file that must contain a list of NTP servers to be used on system start. It is recommend to have at last four servers listed to reduce the chance of a “false ticker” (incorrect time source) influencing the quality of the time offset calculation. However, publicly accessible time sources are rarely incorrect.

#### NTPD Options

From the above guide:

> To change the default configuration of the NTP service, use a text editor running as root user to edit the **/etc/ntp.conf** file. This file is installed together with **ntpd** and is configured to use time servers from the Red Hat pool by default. The man page **ntp.conf**(5) describes the command options that can be used in the configuration file apart from the access and rate limiting commands which are explained in the **ntp_acc**(5) man page.
>
> #### Configure Access Control to an NTP Service
>
> To restrict or control access to the NTP service running on a system, make use of the restrict command in the **ntp.con**f file. See the commented out example:
>
>     # Hosts on local network are less restricted.
>     #restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
>
>
> The restrict command takes the following form:
>
>     restrict option
>
>
> where option is one or more of:
>
> *   **ignore** — All packets will be ignored, including **ntpq** and **ntpdc** queries.
> *   **kod** — a “Kiss-o'-death” packet is to be sent to reduce unwanted queries.
> *   **limited** — do not respond to time service requests if the packet violates the rate limit specified by the discard command. **ntpq** and **ntpdc** queries are not affected.
> *   **lowpriotrap** — traps set by matching hosts to be low priority.
> *   **nomodify** — prevents any changes to the configuration.
> *   **noquery** — prevents **ntpq** and **ntpdc** queries, but not time queries, from being answered.
> *   **nopeer** — prevents a peer association being formed.
> *   **noserve** — deny all packets except ntpq and ntpdc queries.
> *   **notrap** — prevents ntpdc control message protocol traps.
> *   **notrust** — deny packets that are not cryptographically authenticated.
> *   **ntpport** — modify the match algorithm to only apply the restriction if the source port is the standard NTP UDP port 123.
> *   **version** — deny packets that do not match the current NTP version.
>
> #### Configure Rate Limiting Access to an NTP Service
>
> To rate limit access to the NTP service running on a system, make use of the **discard** command in the **ntp.conf** file. See the commented out example:
>
>     # Hosts on local network are less restricted.
>     #restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
>
>
> The **discard** command takes the following form:
>
>     discard option argument
>
>
> where option is one or more of:
>
> *   **average** — specifies the minimum average packet spacing to be permitted, it accepts an argument in log2 seconds. The default value is 3 (23 equates to 8 seconds).
> *   **minimum** — specifies the minimum packet spacing to be permitted, it accepts an argument in log2 seconds. The default value is 1 (21 equates to 2 seconds).
> *   **monitor** — specifies the discard probability for packets once the permitted rate limits have been exceeded. The default value is 3000 seconds. This option is intended for servers that receive 1000 or more requests per second.
>
> #### Adding a Peer Address
>
> To add the address of a **peer**, that is to say, the address of a server running an NTP service of the same stratum, make use of the **peer** command in the **ntp.conf** file.
>
> The **peer** command takes the following form:
>
>     peer address
>
>
> where address is an IP unicast address or a DNS resolvable name. The address must only be that of a system known to be a member of the same stratum. Peers should have at least one time source that is different to each other. Peers are normally systems under the same administrative control.
>
> #### Adding a Server Address
>
> To add the address of a server, that is to say, the address of a server running an **NTP** service of a higher stratum, make use of the **server** command in the **ntp.conf** file.
>
> The **server** command takes the following form:
>
>     server address
>
>
> where **address** is an **IP** unicast address or a DNS resolvable name. The address of a remote reference server or local reference clock from which packets are to be received.
>
> #### Configuring the Burst Option
>
> Using the **burst** option against a public server is considered abuse. Do not use this option with public **NTP** servers. Use it only for applications within your own organization.
>
> To increase the average quality of time offset statistics, add the following option to the end of a server command:
>
>     burst
>
>
> At every poll interval, send a **burst** of eight packets instead of one, when the server is responding. For use with the **server** command to improve the average quality of the time offset calculations.
>
> #### Configuring the iburst Option
>
> To improve the time taken for initial synchronization, add the following option to the end of a server command:
>
>     iburst
>
>
> At every poll interval, send a **burst** of eight packets instead of one. When the server is not responding, packets are sent 16s apart. When the server responds, packets are sent every 2s. For use with the **server** command to improve the time taken for initial synchronization. As of **Red Hat Enterprise Linux 6.5**, this is now a default option in the configuration file.
>
> #### Configuring the Poll Interval
>
> To change the default poll interval, add the following options to the end of a **server** or **peer** command:
>
>     minpoll value and maxpoll value
>
>
> Options to change the default poll interval, where the interval in seconds will be calculated by raising 2 to the power of **value**, in other words, the interval is expressed in log2 seconds. The default **minpoll** value is 6, 2^6 equates to 64s. The default value for **maxpoll** is 10, which equates to 1024s. Allowed values are in the range 3 to 17 inclusive, which equates to 8s to 36.4h respectively. These options are for use with the **peer** or **server**. Setting a shorter maxpoll may improve clock accuracy.
>
> #### Configuring Server Preference
>
> To specify that a particular server should be preferred above others of similar statistical quality, add the following option to the end of a **server** or **peer** command:
>
>     prefer
>
>
> Use this server for synchronization in preference to other servers of similar statistical quality. This option is for use with the **peer** or **server** commands.
>
> #### Configuring the Time-to-Live for NTP Packets
>
> To specify that a particular time-to-live (TTL) value should be used in place of the default, add the following option to the end of a server or peer command:
>
>     ttl value
>
>
> Specify the time-to-live value to be used in packets sent by broadcast servers and multicast NTP servers. Specify the maximum time-to-live value to use for the “expanding ring search” by a manycast client. The default **value** is 127.
>
> #### Configuring the NTP Version to Use
>
> To specify that a particular version of **NTP** should be used in place of the default, add the following option to the end of a server or peer command:
>
>     version value
>
>
> Specify the version of NTP set in created NTP packets. The value can be in the range 1 to 4. The **default** is 4.

### Configuring the Hardware Clock Update

From the Deployment Guide:

> To configure the system clock to update the hardware clock once after executing **ntpdate**, add the following line to **/etc/sysconfig/ntpdate**:
>
>     SYNC_HWCLOCK=yes
>
>
> To update the hardware clock from the system clock, issue the following command as root:
>
>     ~]# hwclock --systohc
>

### NTPD Example

So let's try this out. First let's install **ntpd**:

    [root@rhel1 ~]# yum install ntp


That actually installs both **ntpdate** and **ntpd**:

    [root@rhel1 ~]# rpm -qa | grep ntp
    ntp-4.2.4p8-2.el6.i686
    ntpdate-4.2.4p8-2.el6.i686


Here is how the default configuration looks like for **ntpd**:

    [root@rhel1 ~]# grep -vE '^$|^#' /etc/ntp.conf
    driftfile /var/lib/ntp/drift
    restrict default kod nomodify notrap nopeer noquery
    restrict -6 default kod nomodify notrap nopeer noquery
    restrict 127.0.0.1
    restrict -6 ::1
    server 0.rhel.pool.ntp.org
    server 1.rhel.pool.ntp.org
    server 2.rhel.pool.ntp.org
    includefile /etc/ntp/crypto/pw
    keys /etc/ntp/keys

Let's allow local machine to query this server, we just have to modify the **restrict** options. In the end I had the following:

	[root@rhel1 ~]# grep -vE '^$|^#' /etc/ntp.conf
	driftfile /var/lib/ntp/drift
	restrict 192.168.2.0 mask 255.255.255.0 nomodify notrap
	server 0.rhel.pool.ntp.org
	server 1.rhel.pool.ntp.org
	server 2.rhel.pool.ntp.org
	includefile /etc/ntp/crypto/pw
	keys /etc/ntp/keys

That looks pretty good, so let's start it:

    [root@rhel1 ~]# service ntpd start
    Starting ntpd:  ntpd
    [root@rhel1 ~]# service ntpd status
    ntpd (pid  8597) is running...


In the logs, I saw the following:

    [root@rhel1 ~]# tail /var/log/messages
    Apr 20 12:23:14 rhel1 ntpd[8596]: ntpd 4.2.4p8@1.1612-o Thu May 13 14:38:22 UTC
     2010 (1)
    Apr 20 12:23:14 rhel1 ntpd[8597]: precision = 0.358 usec
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #0 wildcard, 0.0.0.0#123 Disabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #1 wildcard, ::#123 Disabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #2 eth0, fe80::20c:29ff:fe14:853f#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #3 eth1, fe80::20c:29ff:fe14:8549#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #4 lo, ::1#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #5 lo, 127.0.0.1#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #6 eth0, 192.168.1.3#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on interface #7 eth1, 192.168.2.2#123 Enabled
    Apr 20 12:23:14 rhel1 ntpd[8597]: Listening on routing socket on fd #24 for interface updates
    Apr 20 12:23:14 rhel1 ntpd[8597]: kernel time sync status 2040


Checking out the status:

    [root@rhel1 ~]# ntpq  -p
         remote           refid      st t when poll reach   delay   offset  jitter
    ==============================================================================
    *ccadmin.cycores 209.51.161.238   2 u   57   64   7  100.345   -3.427   3.177
    +falcon.ca.us.sl 199.102.46.73    2 u   53   64   7   42.187  -18.274   5.467
    +repos.lax-noc.c 69.25.96.13      2 u   52   64   7   45.102  -18.694   5.575


Converting the **reach** to binary:

    [root@rhel1 ~]# echo "obase=2; 7" | bc
    111


it looks like the last 3 attempts were successful. Lastly make sure it's synchronized:

    [root@rhel1 ~]# ntpstat
    synchronised to NTP server (216.66.0.142) at stratum 3
       time correct to within 475 ms
       polling server every 64 s


Now let's use this server as an NTP server for the RH5 machine. On the RH5 machine let's install **ntp**:

    [root@rhel2 ~]# yum install ntp


Here is the default configuration file for **ntpd**:

    [root@rhel2 ~]# grep -vE '^$|^#' /etc/ntp.conf
    restrict default kod nomodify notrap nopeer noquery
    restrict -6 default kod nomodify notrap nopeer noquery
    restrict 127.0.0.1
    restrict -6 ::1
    server 0.rhel.pool.ntp.org
    server 1.rhel.pool.ntp.org
    server 2.rhel.pool.ntp.org
    server  127.127.1.0 # local clock
    fudge   127.127.1.0 stratum 10
    driftfile /var/lib/ntp/drift
    keys /etc/ntp/keys


So let's only have one server (our own local one):

    [root@rhel2 ~]# grep -vE '^$|^#' /etc/ntp.conf
    restrict default kod nomodify notrap nopeer noquery
    restrict -6 default kod nomodify notrap nopeer noquery
    restrict 127.0.0.1
    restrict -6 ::1
    server 192.168.2.2
    driftfile /var/lib/ntp/drift
    keys /etc/ntp/keys


Now on the server side, let's allow queries from local network. This is done by adding a **restrict** line **/etc/ntp.conf**:

    [root@rhel1 ~]# grep -vE '^$|^#' /etc/ntp.conf
    driftfile /var/lib/ntp/drift
    restrict default kod nomodify notrap nopeer noquery
    restrict -6 default kod nomodify notrap nopeer noquery
    restrict 192.168.2.0 mask 255.255.255.0 nomodify notrap
    restrict 127.0.0.1
    restrict -6 ::1
    server 0.rhel.pool.ntp.org
    server 1.rhel.pool.ntp.org
    server 2.rhel.pool.ntp.org
    includefile /etc/ntp/crypto/pw
    keys /etc/ntp/keys


Now let's restart the service

    [root@rhel1 ~]# service ntpd restart
    Shutting down ntpd: ntpd
    Starting ntpd:  ntpd


And now let's open up the firewall to allow ntp:

    [root@rhel1 ~]# iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 123 -j ACCEPT
    [root@rhel1 ~]# iptables -I INPUT 18 -m udp -p udp --dport 123 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now on our client let's do a manual sync first and then start the **ntpd** service:

    [root@rhel2 ~]# ntpdate rhel1
    20 Apr 12:49:38 ntpdate[17407]: adjust time server 192.168.2.2 offset 0.000001 sec
    [root@rhel2 ~]# service ntpd start
    Starting ntpd:                                             [  OK  ]
    [root@rhel2 ~]# service ntpd status
    ntpd (pid  17287) is running...


Now to check the status (give it some time to sync), we can run the following:

    [root@rhel2 ~]# ntpq -p
         remote           refid      st t when poll reach   delay   offset  jitter
    ==============================================================================
    *rhel1.local.com   155.101.3.113    4 u   56   64   37    0.131   10.560  13.513
    [root@rhel2 ~]# ntpstat
    synchronised to NTP server (192.168.2.2) at stratum 5
       time correct to within 762 ms
       polling server every 64 s


Also in the logs of the client, I saw the following:

    [root@rhel2 ~]# tail -2 /var/log/messages
    Apr 20 13:22:17 rhel2 ntpd[18049]: synchronized to 192.168.2.2, stratum 4
    Apr 20 13:22:17 rhel2 ntpd[18049]: kernel time sync enabled 0001


