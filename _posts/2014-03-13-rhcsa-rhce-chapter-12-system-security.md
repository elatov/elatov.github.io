---
title: RHCSA and RHCE Chapter 12 – System Security
author: Karim Elatov
layout: post
permalink: /2014/03/rhcsa-rhce-chapter-12-system-security/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2425396195
categories:
  - Certifications
  - RHCSA and RHCE
tags:
  - iptables
  - PAM
  - RHCE
  - RHCSA
  - TCP_Wrappers
---
## TCP Wrappers

From the <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf']);">Security Guide</a>:

> The TCP Wrappers packages (tcp_wrappers and tcp_wrappers-libs) are installed by default and provide host-based access control to network services. The most important component within the package is the **/lib/libwrap.so** or **/lib64/libwrap.so** library. In general terms, a TCP-wrapped service is one that has been compiled against the **libwrap.so** library.
> 
> When a connection attempt is made to a TCP-wrapped service, the service first references the host's access files (**/etc/hosts.allow** and **/etc/hosts.deny**) to determine whether or not the client is allowed to connect. In most cases, it then uses the syslog daemon (**syslogd**) to write the name of the requesting client and the requested service to **/var/log/secure** or **/var/log/messages**.
> 
> If a client is allowed to connect, TCP Wrappers release control of the connection to the requested service and take no further part in the communication between the client and the server.
> 
> In addition to access control and logging, TCP Wrappers can execute commands to interact with the client before denying or releasing control of the connection to the requested network service.
> 
> Because TCP Wrappers are a valuable addition to any server administrator's arsenal of security tools, most network services within Red Hat Enterprise Linux are linked to the **libwrap.so** library. Such applications include **/usr/sbin/sshd**, **/usr/sbin/sendmail**, and **/usr/sbin/xinetd**.

### Check if Service Supports TCP Wrappers

From the Security Guide:

> To determine if a network service binary is linked to **libwrap.so**, type the following command as the root user:
> 
>     ldd binary-name | grep libwrap
>     
> 
> Replace **binary-name** with the name of the network service binary. If the command returns straight to the prompt with no output, then the network service is not linked to **libwrap.so**.
> 
> The following example indicates that **/usr/sbin/sshd** is linked to **libwrap.so**:
> 
>     ~]# ldd /usr/sbin/sshd | grep libwrap
>             libwrap.so.0 => /lib/libwrap.so.0 (0x00655000)
>     

### TCP Wrappers Configuration Files

From the Security Guide:

> To determine if a client is allowed to connect to a service, TCP Wrappers reference the following two files, which are commonly referred to as hosts access files:
> 
> *   /etc/hosts.allow
> *   /etc/hosts.deny
> 
> When a TCP-wrapped service receives a client request, it performs the following steps:
> 
> 1.  It references **/etc/hosts.allow** — The TCP-wrapped service sequentially parses the **/etc/hosts.allow** file and applies the first rule specified for that service. If it finds a matching rule, it allows the connection. If not, it moves on to the next step.
> 2.  It references **/etc/hosts.deny** — The TCP-wrapped service sequentially parses the **/etc/hosts.deny** file. If it finds a matching rule, it denies the connection. If not, it grants access to the service.
> 
> The following are important points to consider when using TCP Wrappers to protect network services:
> 
> *   Because access rules in **hosts.allow** are applied first, they take precedence over rules specified in **hosts.deny**. Therefore, if access to a service is allowed in **hosts.allow**, a rule denying access to that same service in **hosts.deny** is ignored.
> *   The rules in each file are read from the top down and the first matching rule for a given service is the only one applied. The order of the rules is extremely important.
> *   If no rules for the service are found in either file, or if neither file exists, access to the service is granted.
> *   TCP-wrapped services do not cache the rules from the hosts access files, so any changes to **hosts.allow** or **hosts.deny** take effect immediately, without restarting network services.

### Access Rules

From the same guide:

> The format for both **/etc/hosts.allow** and **/etc/hosts.deny** is identical. Each rule must be on its own line. Blank lines or lines that start with a hash (#) are ignored.
> 
> Each rule uses the following basic format to control access to network services:
> 
>     daemon list : client list [: option : option : …]
>     
> 
> *   **daemon list** — A comma-separated list of process names (not service names) or the **ALL** wildcard. The daemon list also accepts operators to allow greater flexibility.
> *   **client list** — A comma-separated list of *hostnames*, *host IP addresses*, *special patterns*, or *wildcards* which identify the hosts affected by the rule. The client list also accepts operators to allow greater flexibility.
> *   **option** — An optional action or colon-separated list of actions performed when the rule is triggered. Option fields support *expansions*, *launch shell commands*, *allow or deny access*, and *alter logging behavior*.

#### Access Rule Examples

From the Security Guide:

> The following is a basic sample hosts access rule:
> 
>     vsftpd : .example.com
>     
> 
> This rule instructs TCP Wrappers to watch for connections to the FTP daemon (**vsftpd**) from any host in the **example.com** domain. If this rule appears in **hosts.allow**, the connection is accepted. If this rule appears in **hosts.deny**, the connection is rejected.
> 
> The next sample hosts access rule is more complex and uses two option fields:
> 
>     sshd : .example.com  \
>       : spawn /bin/echo `/bin/date` access denied>>/var/log/sshd.log \
>       : deny
>     
> 
> Note that each option field is preceded by the backslash (). Use of the backslash prevents failure of the rule due to length.
> 
> This sample rule states that if a connection to the SSH daemon (**sshd**) is attempted from a host in the **example.com** domain, execute the **echo** command to append the attempt to a special log file, and deny the connection. Because the optional deny directive is used, this line denies access even if it appears in the **hosts.allow** file.

#### Access Rules Wildcards

From the guide:

> Wildcards allow TCP Wrappers to more easily match groups of daemons or hosts. They are used most frequently in the client list field of access rules.
> 
> The following wildcards are available:
> 
> *   **ALL** — Matches everything. It can be used for both the *daemon* list and the *client* list.
> *   **LOCAL** — Matches any host that does not contain a period (.), such as localhost.
> *   **KNOWN** — Matches any host where the hostname and host address are known or where the user is known.
> *   **UNKNOWN** — Matches any host where the hostname or host address are unknown or where the user is unknown.
> *   **PARANOID** — A reverse DNS lookup is done on the source IP address to obtain the host name. Then a DNS lookup is performed to resolve the IP address. If the two IP addresses do not match the connection is dropped and the logs are updated

#### Access Rules Patterns

From the Security Guide:

> Patterns can be used in the client field of access rules to more precisely specify groups of client hosts.
> 
> The following is a list of common patterns for entries in the client field:
> 
> *   *Hostname beginning with a period (.)* — Placing a period at the beginning of a hostname matches all hosts sharing the listed components of the name. The following example applies to any host within the **example.com** domain:
>     
>         ALL : .example.com
>         
> 
> *   *IP address ending with a period (.)* — Placing a period at the end of an IP address matches all hosts sharing the initial numeric groups of an IP address. The following example applies to any host within the **192.168.x.x** network:
>     
>         ALL : 192.168.
>         
> 
> *   *IP address/netmask pair* — Netmask expressions can also be used as a pattern to control access to a particular group of IP addresses. The following example applies to any host with an address range of **192.168.0.0** through **192.168.1.255**:
>     
>         ALL : 192.168.0.0/255.255.254.0
>         
> 
> *   *[IPv6 address]/prefixlen pair* — [net]/prefixlen pairs can also be used as a pattern to control access to a particular group of IPv6 addresses. The following example would apply to any host with an address range of **3ffe:505:2:1::** through **3ffe:505:2:1:ffff:ffff:ffff:ffff**:
>     
>         ALL : [3ffe:505:2:1::]/64
>         
> 
> *   *The asterisk (*)* — Asterisks can be used to match entire groups of hostnames or IP addresses, as long as they are not mixed in a client list containing other types of patterns. The following example would apply to any host within the **example.com** domain:
>     
>         ALL : *.example.com
>         
> 
> *   *The slash (/)* — If a client list begins with a slash, it is treated as a file name. This is useful if rules specifying large numbers of hosts are necessary. The following example refers TCP Wrappers to the **/etc/telnet.hosts** file for all Telnet connections:
>     
>         in.telnetd : /etc/telnet.hosts
>         

### TCP Wrappers Options

From the Security Guide:

> In addition to basic rules that allow and deny access, the Red Hat Enterprise Linux implementation of TCP Wrappers supports extensions to the access control language through option fields. By using option fields in hosts access rules, administrators can accomplish a variety of tasks such as *altering log behavior*, *consolidating access control*, and *launching shell commands*.

#### Options for Logging

From the same guide:

> Option fields let administrators easily change the log facility and priority level for a rule by using the severity directive.
> 
> In the following example, connections to the SSH daemon from any host in the **example.com** domain are logged to the default **authpriv syslog** facility (because no facility value is specified) with a priority of emerg:
> 
>     sshd : .example.com : severity emerg
>     
> 
> It is also possible to specify a facility using the severity option. The following example logs any SSH connection attempts by hosts from the **example.com** domain to the **local0** facility with a priority of **alert**:
> 
>     sshd : .example.com : severity local0.alert
>     

#### Options Access Control

From the same guide:

> Option fields also allow administrators to explicitly allow or deny hosts in a single rule by adding the allow or deny directive as the final option.
> 
> For example, the following two rules allow SSH connections from **client-1.example.com**, but deny connections from **client-2.example.com**:
> 
>     sshd : client-1.example.com : allow
>     sshd : client-2.example.com : deny
>     
> 
> By allowing access control on a per-rule basis, the option field allows administrators to consolidate all access rules into a single file: either **hosts.allow** or **hosts.deny**. Some administrators consider this an easier way of organizing access rules.

### Options Shell Commands

From the guide:

> Option fields allow access rules to launch shell commands through the following two directives:
> 
> *   **spawn** — Launches a shell command as a child process. This directive can perform tasks like using **/usr/sbin/safe_finger** to get more information about the requesting client or create special log files using the echo command.
>     
>     In the following example, clients attempting to access Telnet services from the **example.com** domain are quietly logged to a special file:
>     
>         in.telnetd : .example.com \
>           : spawn /bin/echo `/bin/date` from %h>>/var/log/telnet.log \
>           : allow
>         
> 
> *   **twist** — Replaces the requested service with the specified command. This directive is often used to set up traps for intruders (also called "honey pots"). It can also be used to send messages to connecting clients. The **twist** directive must occur at the end of the rule line.
>     
>     In the following example, clients attempting to access FTP services from the **example.com** domain are sent a message using the echo command:
>     
>         vsftpd : .example.com \
>           : twist /bin/echo "421 This domain has been black-listed. Access denied!"
>         

#### Options Expansions

From the Security Guide:

> Expansions, when used in conjunction with the spawn and twist directives, provide information about the client, server, and processes involved.
> 
> The following is a list of supported expansions:
> 
> *   **%a** — Returns the client's IP address.
> *   **%A** — Returns the server's IP address.
> *   **%c** — Returns a variety of client information, such as the username and hostname, or the username and IP address.
> *   **%d** — Returns the daemon process name.
> *   **%h** — Returns the client's hostname (or IP address, if the hostname is unavailable).
> *   **%H** — Returns the server's hostname (or IP address, if the hostname is unavailable).
> *   **%n** — Returns the client's hostname. If unavailable, **unknown** is printed. If the client's hostname and host address do not match, **paranoid** is printed.
> *   **%N** — Returns the server's hostname. If unavailable, **unknown** is printed. If the server's hostname and host address do not match, **paranoid** is printed.
> *   **%p** — Returns the daemon's process ID.
> *   **%s** —Returns various types of server information, such as the daemon process and the host or IP address of the server.
> *   **%u** — Returns the client's username. If unavailable, **unknown** is printed.

So let's create two rules, one to log every ssh connection to a file and 1 to block access to ftp daeamon. First let's confirm both of those support tcp wrappers:

    [root@rhel1 ~]# for i in sshd vsftpd; do echo $i;ldd /usr/sbin/$i| grep wrap; done
    sshd
        libwrap.so.0 => /lib/libwrap.so.0 (0x00e36000)
    vsftpd
        libwrap.so.0 => /lib/libwrap.so.0 (0x00e62000)
    

That looks good. Now let's add two rules into the **/etc/hosts.allow** file with the following content:

    sshd : 192.168.2.3 : severity alert : deny
    vsftpd : 192.168.2.3 \
     : spawn /bin/echo `/bin/date` from %h>>/var/log/ftpd.log \
     : allow
    

Logging in from the rhel5 box with ftp, I saw the following in my log file:

    [root@rhel1 log]# tail /var/log/ftpd.log 
    Sat Mar 1 10:30:26 MST 2014 from 192.168.2.3
    

Trying with ssh, I was blocked access:

    [root@rhel2 ~]# ssh rhel1
    ssh_exchange_identification: Connection closed by remote host
    

and I saw the following in the **/var/log/secure** log:

    [root@rhel1 log]# tail -1 /var/log/secure
    Mar  1 10:32:28 rhel1 sshd[14935]: refused connect from 192.168.2.3 (192.168.2.3)
    

## IPTables

From the Security Guide:

> Included with Red Hat Enterprise Linux are advanced tools for network packet filtering — the process of controlling network packets as they enter, move through, and exit the network stack within the kernel. Kernel versions prior to 2.4 relied on **ipchains** for packet filtering and used lists of rules applied to packets at each step of the filtering process. The 2.4 kernel introduced **iptables** (also called *netfilter*), which is similar to **ipchains** but greatly expands the scope and control available for filtering network packets.

### Packet Filtering

From the same guide:

> The Linux kernel uses the Netfilter facility to filter packets, allowing some of them to be received by or pass through the system while stopping others. This facility is built in to the Linux kernel, and has five built-in tables or rules lists, as follows:
> 
> *   **filter** — The default table for handling network packets.
> *   **nat** — Used to alter packets that create a new connection and used for Network Address Translation (NAT).
> *   **mangle** — Used for specific types of packet alteration.
> *   **raw** — Used mainly for configuring exemptions from connection tracking in combination with the NOTRACK target.
> *   **security** — Used for Mandatory Access Control (MAC) networking rules, such as those enabled by the SECMARK and CONNSECMARK targets.
> 
> Each table has a group of built-in chains, which correspond to the actions performed on the packet by **netfilter**.
> 
> The built-in chains for the **filter** table are as follows:
> 
> *   **INPUT** — Applies to network packets that are targeted for the host.
> *   **OUTPUT** — Applies to locally-generated network packets.
> *   **FORWARD** — Applies to network packets routed through the host.
> 
> The built-in chains for the **nat** table are as follows:
> 
> *   **PREROUTING** — Applies to network packets when they arrive.
> *   **OUTPUT** — Applies to locally-generated network packets before they are sent out.
> *   **POSTROUTING** — Applies to network packets before they are sent out.
> 
> The built-in chains for the **mangle** table are as follows:
> 
> *   **INPUT** — Applies to network packets targeted for the host.
> *   **OUTPUT** — Applies to locally-generated network packets before they are sent out.
> *   **FORWARD** — Applies to network packets routed through the host.
> *   **PREROUTING** — Applies to incoming network packets before they are routed.
> *   **POSTROUTING** — Applies to network packets before they are sent out.
> 
> The built-in chains for the raw table are as follows:
> 
> *   **OUTPUT** — Applies to locally-generated network packets before they are sent out.
> *   **PREROUTING** — Applies to incoming network packets before they are routed.
> 
> The built-in chains for the **security** table are as follows:
> 
> *   **INPUT** — Applies to network packets targeted for the host.
> *   **OUTPUT** — Applies to locally-generated network packets before they are sent out.
> *   **FORWARD** — Applies to network packets routed through the host.
> 
> Every network packet received by or sent from a Linux system is subject to at least one table. However, a packet may be subjected to multiple rules within each table before emerging at the end of the chain. The structure and purpose of these rules may vary, but they usually seek to identify a packet coming from or going to a particular IP address, or set of addresses, when using a particular protocol and network service. The following image outlines how the flow of packets is examined by the **iptables** subsystem:
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2014/03/iptables-process.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/03/iptables-process.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/03/iptables-process.png" alt="iptables process RHCSA and RHCE Chapter 12 – System Security" width="533" height="257" class="alignnone size-full wp-image-10174" title="RHCSA and RHCE Chapter 12 – System Security" /></a>

### Input and Output Chains

From the guide:

> Preventing remote attackers from accessing a LAN is one of the most important aspects of network security. The integrity of a LAN should be protected from malicious remote users through the use of stringent firewall rules.
> 
> However, with a default policy set to block all incoming, outgoing, and forwarded packets, it is impossible for the firewall/gateway and internal LAN users to communicate with each other or with external resources.
> 
> To allow users to perform network-related functions and to use networking applications, administrators must open certain ports for communication.
> 
> For example, to allow access to port 80 on the firewall, append the following rule:
> 
>     ~]# iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
>     
> 
> This allows users to browse websites that communicate using the standard port 80. To allow access to secure websites (for example, https://www.example.com/), you also need to provide access to port 443, as follows:
> 
>     ~]# iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
>     
> 
> There may be times when you require remote access to the LAN. Secure services, for example SSH, can be used for encrypted remote connection to LAN services.
> 
> Administrators with PPP-based resources (such as modem banks or bulk ISP accounts), dial-up access can be used to securely circumvent firewall barriers. Because they are direct connections, modem connections are typically behind a firewall/gateway.
> 
> For remote users with broadband connections, however, special cases can be made. You can configure **iptables** to accept connections from remote SSH clients. For example, the following rules allow remote SSH access:
> 
>     ~]# iptables -A INPUT -p tcp --dport 22 -j ACCEPT
>     ~]# iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
>     
> 
> These rules allow incoming and outbound access for an individual system, such as a single PC directly connected to the Internet or a firewall/gateway. However, they do not allow nodes behind the firewall/gateway to access these services. To allow LAN access to these services, you can use Network Address Translation (NAT) with iptables filtering rules.

### FORWARD and NAT Rules

From the Security Guide:

> Most ISPs provide only a limited number of publicly routable IP addresses to the organizations they serve.
> 
> Administrators must, therefore, find alternative ways to share access to Internet services without giving public IP addresses to every node on the LAN. Using private IP addresses is the most common way of allowing all nodes on a LAN to properly access internal and external network services.
> 
> Edge routers (such as firewalls) can receive incoming transmissions from the Internet and route the packets to the intended LAN node. At the same time, firewalls/gateways can also route outgoing requests from a LAN node to the remote Internet service.
> 
> This forwarding of network traffic can become dangerous at times, especially with the availability of modern cracking tools that can spoof internal IP addresses and make the remote attacker's machine act as a node on your LAN.
> 
> To prevent this, **iptables** provides routing and forwarding policies that can be implemented to prevent abnormal usage of network resources.
> 
> The **FORWARD** chain allows an administrator to control where packets can be routed within a LAN. For example, to allow forwarding for the entire LAN (assuming the firewall/gateway is assigned an internal IP address on eth1), use the following rules:
> 
>     ~]# iptables -A FORWARD -i eth1 -j ACCEPT
>     ~]# iptables -A FORWARD -o eth1 -j ACCEPT
>     
> 
> This rule gives systems behind the firewall/gateway access to the internal network. The gateway routes packets from one LAN node to its intended destination node, passing all packets through its **eth1** device.

#### Kernel Forwarding Packets

From the same guide:

> By default, the IPv4 policy in Red Hat Enterprise Linux kernels disables support for IP forwarding. This prevents machines that run Red Hat Enterprise Linux from functioning as dedicated edge routers. To enable IP forwarding, use the following command as the root user:
> 
>     ~]# sysctl -w net.ipv4.ip_forward=1
>     net.ipv4.ip_forward = 1
>     
> 
> This configuration change is only valid for the current session; it does not persist beyond a reboot or network service restart. To permanently set IP forwarding, edit the **/etc/sysctl.conf** file as follows: Locate the following line:
> 
>     net.ipv4.ip_forward = 0
>     
> 
> Edit it to read as follows:
> 
>     net.ipv4.ip_forward = 1
>     
> 
> As the root user, run the following command to enable the change to the **sysctl.conf** file:
> 
>     ~]# sysctl -p /etc/sysctl.conf
>     net.ipv4.ip_forward = 1
>     net.ipv4.conf.default.rp_filter = 1
>     net.ipv4.conf.default.accept_source_route = 0
>     

### Postrouting and IP Masquerading

From the Guide:

> Accepting forwarded packets via the firewall's internal IP device allows LAN nodes to communicate with each other; however they still cannot communicate externally to the Internet.
> 
> To allow LAN nodes with private IP addresses to communicate with external public networks, configure the firewall for IP *masquerading*, which masks requests from LAN nodes with the IP address of the firewall's external device (in this case, **eth0**):
> 
>     ~]# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
>     
> 
> This rule uses the **NAT** packet matching table (-t nat) and specifies the built-in **POSTROUTING** chain for **NAT** (-A POSTROUTING) on the firewall's external networking device (-o eth0).
> 
> **POSTROUTING** allows packets to be altered as they are leaving the firewall's external device.
> 
> The **-j MASQUERADE** target is specified to mask the private IP address of a node with the external IP address of the firewall/gateway.

### Prerouting

From the Security Guide:

> If you have a server on your internal network that you want make available externally, you can use the **-j DNAT** target of the PREROUTING chain in NAT to specify a destination IP address and port where incoming packets requesting a connection to your internal service can be forwarded.
> 
> For example, if you want to forward incoming HTTP requests to your dedicated Apache HTTP Server at 172.31.0.23, use the following command as the root user:
> 
>     ~]# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to 172.31.0.23:80
>     
> 
> This rule specifies that the nat table use the built-in **PREROUTING** chain to forward incoming HTTP requests exclusively to the listed destination IP address of 172.31.0.23.

### IPTables and Connection Tracking

From the same guide:

> You can inspect and restrict connections to services based on their connection state. A module within iptables uses a method called connection tracking to store information about incoming connections. You can allow or deny access based on the following connection states:
> 
> *   **NEW** — A packet requesting a new connection, such as an HTTP request.
> *   **ESTABLISHED** — A packet that is part of an existing connection.
> *   **RELATED** — A packet that is requesting a new connection but is part of an existing connection. For example, FTP uses port 21 to establish a connection, but data is transferred on a different port (typically port 20).
> *   **INVALID** — A packet that is not part of any connections in the connection tracking table.
> 
> You can use the stateful functionality of iptables connection tracking with any network protocol, even if the protocol itself is stateless (such as UDP). The following example shows a rule that uses connection tracking to forward only the packets that are associated with an established connection:
> 
>     ~]# iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
>     

### Command Options for IPTables

From the guide:

> Rules for filtering packets are created using the iptables command. The following aspects of the packet are most often used as criteria:
> 
> *   **Packet Type** — Specifies the type of packets the command filters.
> *   **Packet Source/Destination** — Specifies which packets the command filters based on the source or destination of the packet.
> *   **Target** — Specifies what action is taken on packets matching the above criteria.

#### Command Options

From the Security Guide:

> Command options instruct **iptables** to perform a specific action. Only one command option is allowed per **iptables** command. With the exception of the help command, all commands are written in upper-case characters.
> 
> The **iptables** commands are as follows:
> 
> *   **-A** — Appends the rule to the end of the specified chain. Unlike the **-I** option described below, it does not take an integer argument. It always appends the rule to the end of the specified chain.
> *   **-D** *integer* | *rule* — Deletes a rule in a particular chain by number (such as 5 for the fifth rule in a chain), or by rule specification. The rule specification must exactly match an existing rule.
> *   **-E** — Renames a user-defined chain. A user-defined chain is any chain other than the default, pre-existing chains. (Refer to the -N option, below, for information on creating user-defined chains.) This is a cosmetic change and does not affect the structure of the table.
> *   **-F** — Flushes the selected chain, which effectively deletes every rule in the chain. If no chain is specified, this command flushes every rule from every chain.
> *   **-h** — Provides a list of command structures, as well as a quick summary of command parameters and options.
> *   **-I** [*integer*] — Inserts the rule in the specified chain at a point specified by a user-defined integer argument. If no argument is specified, the rule is inserted at the top of the chain.
> *   **-L** — Lists all of the rules in the chain specified after the command. To list all rules in all chains in the default filter table, do not specify a chain or table. 
> *   **-N** — Creates a new chain with a user-specified name. The chain name must be unique, otherwise an error message is displayed. **-P** — Sets the default policy for the specified chain, so that when packets traverse an entire chain without matching a rule, they are sent to the specified target, such as ACCEPT or DROP. **-R** — Replaces a rule in the specified chain. The rule's number must be specified after the chain's name. The first rule in a chain corresponds to rule number one. **-X** — Deletes a user-specified chain. You cannot delete a built-in chain. **-Z** — Sets the byte and packet counters in all chains for a table to zero.

#### IPTables Parameter Options

From the Security Guide:

> Certain **iptables** commands, including those used to add, append, delete, insert, or replace rules within a particular chain, require various parameters to construct a packet filtering rule.
> 
> *   **-c** — Resets the counters for a particular rule. This parameter accepts the PKTS and BYTES options to specify which counter to reset.
> *   **-d** — Sets the destination hostname, IP address, or network of a packet that matches the rule. When matching a network, the following IP address/netmask formats are supported:
>     
>     *   **N.N.N.N/M.M.M.M** — Where **N.N.N.N** is the IP address range and **M.M.M.M** is the netmask.
>     *   **N.N.N.N/M** — Where **N.N.N.N** is the IP address range and **M** is the bitmask.
> 
> *   **-f** — Applies this rule only to fragmented packets. You can use the exclamation point character (!) option before this parameter to specify that only unfragmented packets are matched.
> 
> *   **-i** — Sets the incoming network interface, such as eth0 or ppp0. With **iptables**, this optional parameter may only be used with the INPUT and FORWARD chains when used with the filter table and the PREROUTING chain with the nat and mangle tables.
>     
>     This parameter also supports the following special options:
>     
>     *   Exclamation point character (**!**) — Reverses the directive, meaning any specified interfaces are excluded from this rule.
>     *   Plus character (**+**) — A wildcard character used to match all interfaces that match the specified string. For example, the parameter -i eth+ would apply this rule to any Ethernet interfaces but exclude any other interfaces, such as ppp0.
>     
>     If the -i parameter is used but no interface is specified, then every interface is affected by the rule.
> 
> *   **-j** — Jumps to the specified target when a packet matches a particular rule.
>     
>     The standard targets are **ACCEPT**, **DROP**, **QUEUE**, and **RETURN**.
>     
>     Extended options are also available through modules loaded by default with the Red Hat Enterprise Linux iptables RPM package. Valid targets in these modules include **LOG**, **MARK**, and **REJECT**, among others. Refer to the iptables man page for more information about these and other targets.
>     
>     This option can also be used to direct a packet matching a particular rule to a user-defined chain outside of the current chain so that other rules can be applied to the packet.
>     
>     If no target is specified, the packet moves past the rule with no action taken. The counter for this rule, however, increases by one.
> 
> *   **-o** — Sets the outgoing network interface for a rule. This option is only valid for the **OUTPUT** and **FORWARD** chains in the filter table, and the **POSTROUTING** chain in the nat and mangle tables. This parameter accepts the same options as the incoming network interface parameter (-i).
> 
> *   **-p** *protocol* — Sets the IP protocol affected by the rule. This can be either **icmp**, **tcp**, **udp**, or **all**, or it can be a numeric value, representing one of these or a different protocol. You can also use any protocols listed in the **/etc/protocols** file.
>     
>     The "**all**" protocol means the rule applies to every supported protocol. If no protocol is listed with this rule, it defaults to "all".
> 
> *   **-s** — Sets the source for a particular packet using the same syntax as the destination (-d) parameter.

#### TCP Protocol

From the Same Guide:

> These match options are available for the TCP protocol (-p tcp):
> 
> *   **-dport** — Sets the destination port for the packet.
>     
>     To configure this option, use a network service name (such as **www** or **smtp**); a port number; or a range of port numbers.
>     
>     To specify a range of port numbers, separate the two numbers with a colon (**:**). For example: `-p tcp --dport 3000:3200`. The largest acceptable valid range is **0:65535**.
>     
>     Use an exclamation point character (**!**) after the **-dport** option to match all packets that do not use that network service or port.
>     
>     To browse the names and aliases of network services and the port numbers they use, view the **/etc/services** file.
>     
>     The **-destination-port** match option is synonymous with **-dport**.
> 
> *   **-sport** — Sets the source port of the packet using the same options as **-dport**. The **-source-port** match option is synonymous with **-sport**.
> 
> *   **-syn** — Applies to all TCP packets designed to initiate communication, commonly called **SYN** packets. Any packets that carry a data payload are not touched.
>     
>     Use an exclamation point character (**!**) before the **-syn** option to match all non-SYN packets.
> 
> *   **-tcp-flags** "*tested flag list*" "*set flag list*" — Allows TCP packets that have specific bits (flags) set, to match a rule.
>     
>     The **-tcp-flags** match option accepts two parameters. The first parameter is the mask; a comma-separated list of flags to be examined in the packet. The second parameter is a comma-separated list of flags that must be set for the rule to match. The possible flags are:
>     
>     *   **ACK**
>     *   **FIN**
>     *   **PSH**
>     *   **RST**
>     *   **SYN**
>     *   **URG**
>     *   **ALL**
>     *   **NONE**
>     
>     For example, an **iptables** rule that contains the following specification only matches TCP packets that have the **SYN** flag set and the **ACK** and **FIN** flags not set:
>     
>         --tcp-flags ACK,FIN,SYN SYN
>         
>     
>     Use the exclamation point character (**!**) after the **-tcp-flags** to reverse the effect of the match option.
> 
> *   **-tcp-option** — Attempts to match with TCP-specific options that can be set within a particular packet. This match option can also be reversed by using the exclamation point character (**!**) after the option.

#### UDP Protocol

From the guide:

> These match options are available for the UDP protocol (**-p udp**):
> 
> *   **-dport** — Specifies the destination port of the UDP packet, using the service name, port number, or range of port numbers. The **-destination-port** match option is synonymous with **-dport**.
> *   **-sport** — Specifies the source port of the UDP packet, using the service name, port number, or range of port numbers. The **-source-port** match option is synonymous with **-sport**.
> 
> For the **-dport** and **-sport** options, to specify a range of port numbers, separate the two numbers with a colon (**:**). For example: `-p tcp --dport 3000:3200`. The largest acceptable valid range is **0:65535**.

### IPTables Control Scripts

From the Security Guide:

> There are two basic methods for controlling **iptables** in Red Hat Enterprise Linux:
> 
> *   Firewall Configuration Tool (**system-config-firewall**) — A graphical interface for creating, activating, and saving basic firewall rules.
> *   **/sbin/service iptables** "*option*" — Used to manipulate various functions of iptables using its initscript. The following options are available:
> *   **start** — If a firewall is configured (that is, **/etc/sysconfig/iptables** exists), all running iptables are stopped completely and then started using the **/sbin/iptables-restore** command. This option only works if the **ipchains** kernel module is not loaded. To check if this module is loaded, type the following command as root:
>     
>         ~]# lsmod | grep ipchains
>         
>     
>     If this command returns no output, it means the module is not loaded. If necessary, use the **/sbin/rmmod** command to remove the module.
> 
> *   **stop** — If a firewall is running, the firewall rules in memory are flushed, and all iptables modules and helpers are unloaded. If the **IPTABLES_SAVE_ON_STOP** directive in the **/etc/sysconfig/iptables-config** configuration file is changed from its default value to **yes**, current rules are saved to **/etc/sysconfig/iptables** and any existing rules are moved to the file **/etc/sysconfig/iptables.save**.
> 
> *   **reload** — If a firewall is running, the firewall rules are reloaded from the configuration file. The reload command does not unload helpers that have been in use before, but will add new helpers that have been added to **IPTABLES_MODULES** (for IPv4) and **IP6TABLES_MODULES** (for IPv6). The advantage of not flushing the current firewall rules is that if the new rules can not be applied, because of an error in the rules, the old rules are still in place.
> 
> *   **restart** — If a firewall is running, the firewall rules in memory are flushed, and the firewall is started again if it is configured in **/etc/sysconfig/iptables**. This option only works if the **ipchains** kernel module is not loaded. If the **IPTABLES_SAVE_ON_RESTART** directive in the **/etc/sysconfig/iptables-config** configuration file is changed from its default value to **yes**, current rules are saved to **/etc/sysconfig/iptables** and any existing rules are moved to the file **/etc/sysconfig/iptables.save**.
> 
> *   **status** — Displays the status of the firewall and lists all active rules. The default configuration for this option displays IP addresses in each rule. To display domain and hostname information, edit the **/etc/sysconfig/iptables-config** file and change the value of **IPTABLES_STATUS_NUMERIC** to **no**.
> 
> *   **panic** — Flushes all firewall rules. The policy of all configured tables is set to **DROP**. This option could be useful if a server is known to be compromised. Rather than physically disconnecting from the network or shutting down the system, you can use this option to stop all further network traffic but leave the machine in a state ready for analysis or other forensics.
> 
> *   **save** — Saves firewall rules to **/etc/sysconfig/iptables** using **iptables-save**.

### IPtables Examples

So let's try this out. First let's list the current rules:

    [root@rhel1 ~]# iptables -L -n -v --line-numbers
    Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1      148 11008 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED 
    2        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
    3        0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
    4        1   100 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22 
    5        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           tcp dpt:21 
    6        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           tcp dpt:20 
    7       0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    
    Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1        0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    
    Chain OUTPUT (policy ACCEPT 80 packets, 12336 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    

It looks like for the inbound traffic I allow **ESTABLISHED** and **RELATED** traffic (rule # 1). I then allow all icmp (ping) traffic as well (rule # 2). Then I allow everything to the localhost interface (rule #3). Rules 4 through 6 are allowing SSH and FTP. And the last rule (#7) is to block the rest. For the FORWARD CHAIN everything is blocked for now. And for the outbound (OUTPUT) everything is allowed.

Since I am allowing port 21, I should be able to connect to that port from my rhel5 machine:

    [root@rhel2 ~]# telnet rhel1 21
    Trying 192.168.2.2...
    Connected to rhel1.local.com (192.168.2.2).
    Escape character is '^]'.
    220 (vsFTPd 2.2.2)
    ^]
    

That looks good, now let's remove that rule and see if it gets blocked:

    [root@rhel1 ~]# iptables -D INPUT 5
    [root@rhel1 ~]# iptables -L -n -v | grep 21
    [root@rhel1 ~]#
    

Now let's test again:

    [root@rhel2 ~]# telnet rhel1 21
    Trying 192.168.2.2...
    telnet: connect to address 192.168.2.2: No route to host
    telnet: Unable to connect to remote host: No route to host
    

Looking at a packet capture on the server side, I saw the following:

    [root@rhel1 log]# tcpdump -i eth1 tcp port 21 -nn
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
    20:27:27.123519 IP 192.168.2.3.44803 > 192.168.2.2.21: Flags [S], seq 3480557426, win 5840, options [mss 1460,sackOK,TS val 426634483 ecr 0,nop,wscale 6], length 0
    

We can see the client (192.168.2.3) tried connecting to the server (192.168.2.2) on port 21 but there is no response to the request. That usually means the firewall blocked the traffic. As a quick test let's reload the firewall:

    [root@rhel1 ~]# service iptables restart
    iptables: Flushing firewall rules: 
    iptables: Setting chains to policy ACCEPT: filter 
    iptables: Unloading modules: 
    iptables: Applying firewall rules: 
    iptables: Loading additional modules: ip_conntrack_ftp 
    [root@rhel1 ~]# iptables -L -n -v | grep 21
        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           tcp dpt:21 
    

Our rule is back now. Now let's stop the **vsftpd** service and see what happens:

    [root@rhel1 ~]# service vsftpd stop
    Shutting down vsftpd: vsftpd
    

Now for the connection attempt:

    [root@rhel2 ~]# telnet rhel1 21
    Trying 192.168.2.2...
    telnet: connect to address 192.168.2.2: Connection refused
    telnet: Unable to connect to remote host: Connection refused
    

Now we get a "**connection refused**" instead of a "**no route to host**". And here is a packet capture during the previous attempt:

    [root@rhel1 ~]# tcpdump -i eth1 tcp port 21 -nn
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
    20:32:08.972886 IP 192.168.2.3.41472 > 192.168.2.2.21: Flags [S], seq 3783938818, win 5840, options [mss 1460,sackOK,TS val 426916331 ecr 0,nop,wscale 6], length 0
    20:32:08.972931 IP 192.168.2.2.21 > 192.168.2.3.41472: Flags [R.], seq 0, ack 3783938819, win 0, length 0
    

We actually respond to let the client know that nothing is listening on that port. If you check above we are allowing everyone to connect to ports 20 and 21. Let's remove those rules and only allow our internal network to connect to those ports. To delete those rules, run the following:

    [root@rhel1 ~]# iptables -D INPUT 6
    [root@rhel1 ~]# iptables -D INPUT 5
    

Let's sure those are gone:

    [root@rhel1 ~]# iptables -L -n -v | grep -E '21|20'
    [root@rhel1 ~]# 
    

Now to re-add the rules, our last rule (which blocks everything) is number 5 :

    [root@rhel1 ~]# iptables -L -n -v --line-number 
    Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1      621 47188 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED 
    2        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
    3        0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
    4        1   100 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22 
    5        0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    

So let's input the rule starting at 5 and then to 6:

    [root@rhel1 ~]# iptables -I INPUT 5 -s 192.168.2.0/24 -p tcp --dport 21 -j ACCEPT
    [root@rhel1 ~]# iptables -I INPUT 6 -s 192.168.2.0/24 -p tcp --dport 20 -j ACCEPT
    [root@rhel1 ~]# iptables -L -n -v --line-number 
    Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1     1133 89605 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED 
    2        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
    3        0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
    4        1   100 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22  
    5        2   120 ACCEPT     tcp  --  *      *       192.168.2.0/24       0.0.0.0/0           tcp dpt:21 
    6       0     0 ACCEPT     tcp  --  *      *       192.168.2.0/24       0.0.0.0/0           tcp dpt:20 
    7       0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    

Now let's save the rules and restart **iptables** to make sure the rules are still in place:

    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables: 
    [root@rhel1 ~]# service iptables restart
    iptables: Flushing firewall rules: 
    iptables: Setting chains to policy ACCEPT: filter 
    iptables: Unloading modules: 
    iptables: Applying firewall rules: 
    iptables: Loading additional modules: ip_conntrack_ftp 
    [root@rhel1 ~]# iptables -L -n -v --line-numbers
    Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1       81  6084 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED 
    2        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
    3        0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
    4        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22  
    5        0     0 ACCEPT     tcp  --  *      *       192.168.2.0/24       0.0.0.0/0           tcp dpt:21 
    6        0     0 ACCEPT     tcp  --  *      *       192.168.2.0/24       0.0.0.0/0           tcp dpt:20 
    7        0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    

### IPTables Masquerade NAT

My RHEL6 box has two interfaces, one on the "public" network and one on the private network (public = 10.0.0.0/24, and private = 192.168.2.0/24). Here are the two interfaces on each network:

    [root@rhel1 ~]# ip -4 a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN 
        inet 127.0.0.1/8 scope host lo
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        inet 10.0.0.4/24 brd 10.0.0.255 scope global eth0
    3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        inet 192.168.2.2/24 brd 192.168.2.255 scope global eth1
    

My RHEL5 machine only has an interface on the private interface:

    [root@rhel2 ~]# ip -4 a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue 
        inet 127.0.0.1/8 scope host lo
    3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
        inet 192.168.2.3/24 brd 192.168.2.255 scope global eth1
    

The RHEL5 machine can't reach the internet:

    [root@rhel2 ~]# ping -c 2 google.com
    PING google.com (74.125.239.37) 56(84) bytes of data.
    
    --- google.com ping statistics ---
    2 packets transmitted, 0 received, 100% packet loss, time 999ms
    

Let's use our RHEL6 as an edge router and setup a Masquerade SNAT on it. First let's make sure the kernel is allowing the Forwarding of packets:

    [root@rhel1 ~]# cat /proc/sys/net/ipv4/ip_forward 
    0
    

That's a negative. To temporarily enable that we can run the following:

    [root@rhel1 ~]# echo 1 > /proc/sys/net/ipv4/ip_forward
    

To make it persistent add the following to **/etc/sysctl.conf**:

    [root@rhel1 ~]# grep ip_forward /etc/sysctl.conf 
    net.ipv4.ip_forward = 1
    

and then run the following to apply it:

    [root@rhel1 ~]# sysctl -p | grep ip_forw
    net.ipv4.ip_forward = 1
    

Since our FORWARD Chain is currently blocking everything, let's allow traffic to flow through our private interface (eth1). This is done with the following two rules:

    [root@rhel1 ~]# iptables -I FORWARD 1 -i eth1 -j ACCEPT
    [root@rhel1 ~]# iptables -I FORWARD 2 -o eth1 -j ACCEPT
    

Let's make sure they are in place:

    [root@rhel1 ~]# iptables -L FORWARD -n -v
    Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
     pkts bytes target     prot opt in     out     source               destination         
        0     0 ACCEPT     all  --  eth1   *       0.0.0.0/0            0.0.0.0/0           
        0     0 ACCEPT     all  --  *      eth1    0.0.0.0/0            0.0.0.0/0           
        5   695 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited 
    

Lastly let's add a rule to the POSTROUTING Chain of the NAT table to enable the Masquerading of IPs:

    [root@rhel1 ~]# iptables -t nat -A POSTROUTING -o eth0 -s 192.168.2.0/24 -j MASQUERADE
    

Let's make sure the rule is in place:

    [root@rhel1 ~]# iptables -t nat -L -n -v --line-numbers
    Chain PREROUTING (policy ACCEPT 3 packets, 213 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    
    Chain POSTROUTING (policy ACCEPT 1 packets, 73 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1        1    84 MASQUERADE  all  --  *      eth0    192.168.2.0/24       0.0.0.0/0           
    
    Chain OUTPUT (policy ACCEPT 1 packets, 73 bytes)
    num   pkts bytes target     prot opt in     out     source               destination   
    

Now from our internal RHEL5 machine let's check if we can reach the internet:

    [root@rhel2 ~]# ping -c 2 google.com
    PING google.com (74.125.239.128) 56(84) bytes of data.
    64 bytes from nuq05s02-in-f0.1e100.net (74.125.239.128): icmp_seq=1 ttl=53 time=41.1 ms
    64 bytes from nuq05s02-in-f0.1e100.net (74.125.239.128): icmp_seq=2 ttl=53 time=39.2 ms
    
    --- google.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1000ms
    rtt min/avg/max/mdev = 39.286/40.213/41.140/0.927 ms
    

That looks good.

### IPTables DNAT Example

For now the internal RHEL5 machine can reach out the internet but nothing can reach it from the internet (unless it'a an existing/established connection. So let's forward any traffic that comes to port 3333 of our RHEL6 (Edge Router) to port 22 of the RHEL5 (internal machine). That way I can ssh directly to our internal test machine. To accomplish this, we will now use the PREROUTING Chain of the NAT table. Here is the command to do this:

    [root@rhel1 ~]# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 3333 -j DNAT --to 192.168.2.3:22
    

Let's make sure the rule is in place:

    [root@rhel1 ~]# iptables -t nat -L PREROUTING -n -v --line-numbers
    Chain PREROUTING (policy ACCEPT 47 packets, 2870 bytes)
    num   pkts bytes target     prot opt in     out     source               destination         
    1        2   120 DNAT       tcp  --  eth0   *       0.0.0.0/0            0.0.0.0/0           tcp dpt:3333 to:192.168.2.3:22 
    

Lastly from an external machine try to ssh to rhel1 on port 3333:

    elatov@fed:~$ssh -p 3333 rhel1 -l root
    root@rhel1's password: 
    Last login: Sat Mar  1 21:11:41 2014 from fed
    [root@rhel2 ~]# 
    

Notice I sent the request to *rhel1*, but in the end reached *rhel2*.

## Pluggable Authentication Module (PAM)

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Smart_Cards/Red_Hat_Enterprise_Linux-6-Managing_Smart_Cards-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Smart_Cards/Red_Hat_Enterprise_Linux-6-Managing_Smart_Cards-en-US.pdf']);">Managing Single Sign-On and Smart Cards</a> here is what PAM is:

> Programs that grant users access to a system use authentication to verify each other's identity (that is, to establish that a user is who they say they are).
> 
> Historically, each program had its own way of authenticating users. In Red Hat Enterprise Linux, many programs are configured to use a centralized authentication mechanism called **Pluggable Authentication Modules (PAM)**.
> 
> PAM uses a pluggable, modular architecture, which affords the system administrator a great deal of flexibility in setting authentication policies for the system. PAM is a useful system for developers and administrators for several reasons:
> 
> *   PAM provides a common authentication scheme that can be used with a wide variety of applications.
> *   PAM provides significant flexibility and control over authentication for both system administrators and application developers.
> *   PAM provides a single, fully-documented library which allows developers to write programs without having to create their own authentication schemes.
> 
> PAM has an extensive documentation set with much more detail about both using PAM and writing modules to extend or integrate PAM with other applications. Almost all of the major modules and configuration files with PAM have their own manpages. Additionally, the **/usr/share/doc/pam-version#** directory contains a System Administrators' Guide, a Module Writers' Manual, and the Application Developers' Manual, as well as a copy of the PAM standard, DCE-RFC 86.0.
> 
> The libraries for PAM are available at *http://www.kernel.org/pub/linux/libs/pam/*. This is the primary distribution website for the Linux-PAM project, containing information on various PAM modules, frequently asked questions, and additional PAM documentation.

### PAM Configuration Files

From the same guide:

> The **/etc/pam.d/** directory contains the PAM configuration files for each PAM-aware application.
> 
> Each PAM-aware application or service has a file in the **/etc/pam.d/** directory. Each file in this directory has the same name as the service to which it controls access.
> 
> The PAM-aware program is responsible for defining its service name and installing its own PAM configuration file in the **/etc/pam.d/** directory. For example, the login program defines its service name as **login** and installs the **/etc/pam.d/login** PAM configuration

#### PAM Configuration Format

From the guide:

> Each PAM configuration file contains a group of directives that define the module and any controls or arguments with it.
> 
> The directives all have a simple syntax that identifies the module purpose (interface) and the configuration settings for the module.
> 
>     module_interface control_flag module_name module_arguments
>     

#### PAM Modules

From the Managing Single Sign-On and Smart Cards Guide:

> Four types of PAM module interface are available. Each of these corresponds to a different aspect of the authorization process:
> 
> *   **auth** — This module interface authenticates use. For example, it requests and verifies the validity of a password. Modules with this interface can also set credentials, such as group memberships or Kerberos tickets.
> *   **account** — This module interface verifies that access is allowed. For example, it checks if a user account has expired or if a user is allowed to log in at a particular time of day.
> *   **password** — This module interface is used for changing user passwords.
> *   **session** — This module interface configures and manages user sessions. Modules with this interface can also perform additional tasks that are needed to allow access, like mounting a user's home directory and making the user's mailbox available.
> 
> In a PAM configuration file, the module interface is the first field defined. For example:
> 
>     auth  required    pam_unix.so
>     
> 
> This instructs PAM to use the pam_unix.so module's auth interface.
> 
> Module interface directives can be stacked, or placed upon one another, so that multiple modules are used together for one purpose. If a module's control flag uses the sufficient or requisite value, then the order in which the modules are listed is important to the authentication process.
> 
> Stacking makes it easy for an administrator to require specific conditions to exist before allowing the user to authenticate. For example, the reboot command normally uses several stacked modules, as seen in its PAM configuration file:
> 
>     [root@MyServer ~]# cat /etc/pam.d/reboot
>     #%PAM-1.0
>     auth  sufficient  pam_rootok.so
>     auth  required    pam_console.so
>     #auth include     system-auth
>     account   required    pam_permit.so
>     
> 
> The first line is a comment and is not processed.
> 
> *   **auth sufficient pam_rootok.so** — This line uses the **pam_rootok.so** module to check whether the current user is root, by verifying that their UID is 0. If this test succeeds, no other modules are consulted and the command is executed. If this test fails, the next module is consulted.
> *   **auth required pam_console.so** — This line uses the **pam_console.so** module to attempt to authenticate the user. If this user is already logged in at the console, pam_console.so checks whether there is a file in the /etc/security/console.apps/ directory with the same name as the service name (reboot). If such a file exists, authentication succeeds and control is passed to the next module.
> *   **#auth include system-auth** — This line is commented and is not processed.
> *   **account required pam_permit.so** — This line uses the pam_permit.so module to allow the root user or anyone logged in at the console to reboot the system.

#### PAM Control Flags

From the same guide:

> All PAM modules generate a success or failure result when called. Control flags tell PAM what do with the result. Modules can be stacked in a particular order, and the control flags determine how important the success or failure of a particular module is to the overall goal of authenticating the user to the service.
> 
> There are several simple flags, which use only a keyword to set the configuration:
> 
> *   **required** — The module result must be successful for authentication to continue. If the test fails at this point, the user is not notified until the results of all module tests that reference that interface are complete.
> *   **requisite** — The module result must be successful for authentication to continue. However, if a test fails at this point, the user is notified immediately with a message reflecting the first failed required or requisite module test.
> *   **sufficient** — The module result is ignored if it fails. However, if the result of a module flagged sufficient is successful and no previous modules flagged required have failed, then no other results are required and the user is authenticated to the service.
> *   **optional** — The module result is ignored. A module flagged as optional only becomes necessary for successful authentication when no other modules reference the interface.
> *   **include** — Unlike the other controls, this does not relate to how the module result is handled. This flag pulls in all lines in the configuration file which match the given parameter and appends them as an argument to the module.
> 
> There are many complex control flags that can be set. These are set in *attribute=value* pairs; a complete list of attributes is available in the **pam.d** manpage.

### Sample PAM Configuration File

From the same Guide:

> Simple PAM Configuration
> 
>     #%PAM-1.0
>     auth      required  pam_securetty.so
>     auth      required  pam_unix.so nullok
>     auth      required  pam_nologin.so
>     account       required  pam_unix.so
>     password  required  pam_cracklib.so retry=3
>     password  required  pam_unix.so shadow nullok use_authtok
>     session   required  pam_unix.so
>     
> 
> *   The first line is a comment, indicated by the hash mark (#) at the beginning of the line.
> *   Lines two through four stack three modules for login authentication.
> *   **auth required pam_securetty.so** — This module ensures that if the user is trying to log in as root, the tty on which the user is logging in is listed in the **/etc/securetty** file, if that file exists.
>     
>     If the tty is not listed in the file, any attempt to log in as root fails with a **Login incorrect** message.
> 
> *   **auth required pam_unix.so nullok** — This module prompts the user for a password and then checks the password using the information stored in **/etc/passwd** and, if it exists, **/etc/shadow**.
>     
>     The argument **nullok** instructs the pam_unix.so module to allow a blank password.
> 
> *   **auth required pam_nologin.so** — This is the final authentication step. It checks whether the **/etc/nologin** file exists. If it exists and the user is not root, authentication fails.
> 
> *   **account required pam_unix.so** — This module performs any necessary account verification. For example, if shadow passwords have been enabled, the account interface of the **pam_unix.so** module checks to see if the account has expired or if the user has not changed the password within the allowed grace period.
> 
> *   **password required pam_cracklib.so retry=3** — If a password has expired, the password component of the **pam_cracklib.so** module prompts for a new password. It then tests the newly created password to see whether it can easily be determined by a dictionary-based password cracking program.
>     
>     The argument **retry=3** specifies that if the test fails the first time, the user has two more chances to create a strong password.
> 
> *   **password required pam_unix.so shadow nullok use_authtok** — This line specifies that if the program changes the user's **password**, using the password interface of the **pam_unix.so** module.
>     
>     *   The argument **shadow** instructs the module to create shadow passwords when updating a user's password.
>     *   The argument **nullok** instructs the module to allow the user to change their password from a blank password, otherwise a null password is treated as an account lock.
>     *   The final argument on this line, **use_authtok**, provides a good example of the importance of order when stacking PAM modules. This argument instructs the module not to prompt the user for a new password. Instead, it accepts any password that was recorded by a previous password module. In this way, all new passwords must pass the **pam_cracklib.so** test for secure passwords before being accepted.
> 
> *   **session required pam_unix.so** — The final line instructs the session interface of the **pam_unix.so** module to manage the session. This module logs the user name and the service type to **/var/log/secure** at the beginning and end of each session. This module can be supplemented by stacking it with other session modules for additional functionality.

### Other PAM Examples

The <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security_Guide/Red_Hat_Enterprise_Linux-6-Security_Guide-en-US.pdf']);">Security Guide</a>, has a lot of the PAM examples as well:

> **Forcing Strong Passwords**
> 
> To protect the network from intrusion it is a good idea for system administrators to verify that the passwords used within an organization are strong ones. When users are asked to create or change passwords, they can use the command line application **passwd**, which is **Pluggable Authentication Modules (PAM)** aware and therefore checks to see if the password is too short or otherwise easy to crack. This check is performed using the **pam_cracklib.so** PAM module. In Red Hat Enterprise Linux, the **pam_cracklib** PAM module can be used to check a password's strength against a set of rules. It can be stacked alongside other PAM modules in the password component of the **/etc/pam.d/passwd** file to configure a custom set of rules for user login. The **pam_cracklib**'s routine consists of two parts: it checks whether the password provided is found in a dictionary, and, if that's not the case, it continues with a number of additional checks. For a complete list of these checks, refer to the **pam_cracklib**(8) manual page.
> 
> **Configuring password strength-checking with pam_cracklib**
> 
> To require a password with a minimum length of 8 characters, including all four classes of characters, add the following line to the password section of the **/etc/pam.d/passwd** file:
> 
>     password   required     pam_cracklib.so retry=3 minlen=8 minclass=4
>     
> 
> To set a password strength-check for consecutive or repetitive characters, add the following line to the **password** section of the **/etc/pam.d/passwd** file:
> 
>     password   required     pam_cracklib.so retry=3 maxsequence=3 maxrepeat=3
>     
> 
> In this example, the password entered cannot contain more than 3 consecutive characters, such as "abcd" or "1234". Additionally, the number of identical consecutive characters is limited to 3.

### Locking Inactive Accounts with PAM

From the Security Guide:

> The **pam_lastlog** PAM module is used to lock out users who have not logged in recently enough, or to display information about the last login attempt of a user. The module does not perform a check on the root account, so it is never locked out.
> 
> The **lastlog** command displays the last login of the user, аs opposed to the **last** command, which displays all current and previous login sessions. The commands read respectively from the **/var/log/lastlog** and **/var/log/wtmp** files where the data is stored in binary format.
> 
> *   To display the number of failed login attempts prior to the last successful login of a user, add, as root, the following line to the session **section** in the **/etc/pam.d/login** file: session optional pam_lastlog.so silent noupdate showfailed 
> 
> Account locking due to inactivity can be configured to work for the console, GUI, or both:
> 
> *   To lock out an account after 10 days of inactivity, add, as root, the following line to the **auth** section of the **/etc/pam.d/login** file:
>     
>         auth  required  pam_lastlog.so inactive=10
>         
> 
> *   To lock out an account for the GNOME desktop environment, add, as root, the following line to the **auth** section of the **/etc/pam.d/gdm** file:
>     
>         auth  required  pam_lastlog.so inactive=10
>         

### Customizing Access Control with PAM

From the Security Guide:

> The **pam_access** PAM module allows an administrator to customize access control based on login names, host or domain names, or IP addresses. By default, the module reads the access rules from the **/etc/security/access.conf** file if no other is specified. For a complete description of the format of these rules, refer to the **access.conf**(5) manual page. By default, in Red Hat Enterprise Linux, **pam_access** is included in the **/etc/pam.d/crond** and **/etc/pam.d/atd** files. To deny the user **john** from accessing system from the console and the graphic desktop environment, follow these steps:
> 
> 1.  Include the following line in the account section of both **/etc/pam.d/login** and &#42;&#42;/etc/pam.d/gdm-&#42;&#42;* files:
>     
>         account     required     pam_access.so
>         
> 
> 2.  Specify the following rule in the **/etc/security/access.conf** file:
>     
>         - : john : ALL
>         
>     
>     This rule prohibits all logins from user john from any location.
> 
> To grant access to all users attempting to log in via SSH except the user john from the **1.2.3.4** IP address, follow these steps:
> 
> 1.  Include the following line in the account section of **/etc/pam.d/sshd**:
>     
>         account     required     pam_access.so
>         
> 
> 2.  Specify the following rule in the /etc/security/access.conf file:
>     
>         + : ALL EXCEPT john : 1.2.3.4
>         
> 
> In order to limit access from other services, the **pam_access.so** module should be **required** in the respective file in the **/etc/pam.d** directory.
> 
> It is possible to call the **pam_access** module for all services that call the system wide PAM configuration files (***-auth** files in the **/etc/pam.d** directory) using the following command:
> 
>     authconfig --enablepamaccess --update
>     
> 
> Alternatively, you can enable the **pam_access** module using the Authentication Configuration utility. To start this utility, select **System** -> **Administration** -> **Authentication** from the top menu. From the Advanced Options tab, check the "**enable local access control option**". This will add the **pam_access** module to the systemwide PAM configuration.

### Time-based Restriction of Access with PAM

From the Security Guide:

> The **pam_time** PAM module is used to restrict access during a certain time of the day. It can also be configured to control access based on specific days of a week, user name, usage of a system service, and more. By default, the module reads the access rules from the **/etc/security/time.conf** file. For a complete description of the format of these rules, refer to the **time.conf**(5) manual page.
> 
> To restrict all users except the root user from logging in from 05:30 PM to 08:00 AM on Monday till Friday and Saturday and Sunday, follow these steps:
> 
> 1.  Include the following line in the account section of the **/etc/pam.d/login** file:
>     
>         account     required     pam_time.so
>         
> 
> 2.  Specify the following rule in the **/etc/security/time.conf** file:
>     
>         login ; ALL ; !root ; tty* ; !Wk1730-0800
>         
> 
> To allow user **john** to use the SSH service during working hours and working days only (starting with Monday), follow these steps:
> 
> 1.  Add the following line to the **/etc/pam.d/sshd** file:
>     
>         account     required     pam_time.so
>         
> 
> 2.  Specify the following rule in the **/etc/security/time.conf** file:
>     
>         sshd ; john ; tty* ; Wk0800-1730
>         

### PAM In Action

So let's try this out. I want to lock a user out after 3 failed login attempts. We were playing around with account management before, let's see if they are still on the system:

    [root@rhel2 ~]# tail -2 /etc/passwd
    user1:x:500:500::/home/user1:/bin/bash
    user2:x:501:501::/home/user2:/bin/bash
    

So let's check out the available PAM modules on the system:

    [root@rhel2 ~]# ls /lib/security/
    pam_access.so     pam_keyinit.so    pam_permit.so       pam_tally2.so
    pam_ccreds.so     pam_krb5          pam_pkcs11.so       pam_tally.so
    pam_chroot.so     pam_krb5afs.so    pam_postgresok.so   pam_time.so
    pam_console.so    pam_krb5.so       pam_pwhistory.so    pam_timestamp.so
    pam_cracklib.so   pam_lastlog.so    pam_rhosts_auth.so  pam_tty_audit.so
    pam_debug.so      pam_ldap.so       pam_rhosts.so       pam_umask.so
    pam_deny.so       pam_limits.so     pam_rootok.so       pam_unix_acct.so
    pam_echo.so       pam_listfile.so   pam_rps.so          pam_unix_auth.so
    pam_env.so        pam_localuser.so  pam_securetty.so    pam_unix_passwd.so
    pam_exec.so       pam_loginuid.so   pam_selinux.so      pam_unix_session.so
    pam_faildelay.so  pam_mail.so       pam_shells.so       pam_unix.so
    pam_filter        pam_mkhomedir.so  pam_smb_auth.so     pam_userdb.so
    pam_filter.so     pam_motd.so       pam_smbpass.so      pam_warn.so
    pam_ftp.so        pam_namespace.so  pam_stack.so        pam_wheel.so
    pam_group.so      pam_nologin.so    pam_stress.so       pam_winbind.so
    pam_issue.so      pam_passwdqc.so   pam_succeed_if.so   pam_xauth.so
    

Now let's check out which module can lock accounts:

    [root@rhel2 ~]# grep -i lock /usr/share/doc/pam-0.99.6.2/txts/* | awk '{print $1}' | uniq
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_console:while
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_console:which
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_cracklib:
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_debug:authtok_err,
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_deny:pam_deny
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_ftp:#
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_listfile:to
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally:Setting
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally:become
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally:
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally:Add
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2:
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2:checks:
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2:account
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2:blocked
    /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2:for
    

After checking out some of the files, it looks like **pam_tally2** is what we are looking for:

    [root@rhel2 ~]# head -5 /usr/share/doc/pam-0.99.6.2/txts/README.pam_tally2
    SUMMARY:
      pam_tally2.so:
    
            Maintains a count of attempted accesses, can reset count on success,
                    can deny access if too many attempts fail.
    

After looking through that file, it looks like we need the following:

    auth        required      pam_tally2.so  file=/var/log/tallylog deny=3 unlock_time=1200
    

But where to put it? First let's see how our **passwd** pam configuration looks like:

    [root@rhel2 ~]# cat /etc/pam.d/passwd 
    #%PAM-1.0
    auth       include  system-auth
    account    include  system-auth
    password   include  system-auth
    

It looks like it uses the **system-auth** configuration, so let's check out the **auth** sections of that file:

    [root@rhel2 ~]# grep ^auth /etc/pam.d/system-auth
    auth        required      pam_env.so
    auth        sufficient    pam_unix.so nullok try_first_pass
    auth        requisite     pam_succeed_if.so uid >= 500 quiet
    auth        required      pam_deny.so
    

That looks like it's our file. So let's add our line to the top. Then let's add the following to the account section:

    account     required      pam_tally2.so
    

Here is how my configuration looked like in the end

    [root@rhel2 ~]# grep -E '^auth|^account' /etc/pam.d/system-auth
    auth        required      pam_tally2.so  file=/var/log/tallylog deny=3 unlock_time=1200
    auth        required      pam_env.so
    auth        sufficient    pam_unix.so nullok try_first_pass
    auth        requisite     pam_succeed_if.so uid >= 500 quiet
    auth        required      pam_deny.so
    account     required      pam_unix.so
    account     sufficient    pam_succeed_if.so uid < 500 quiet
    account     required      pam_permit.so
    account     required      pam_tally2.so
    

Now trying to login 3 times with the wrong password:

    [root@rhel1 ~]# ssh rhel2 -l user1
    user1@rhel2's password: 
    Permission denied, please try again.
    user1@rhel2's password: 
    Permission denied, please try again.
    user1@rhel2's password: 
    Permission denied (publickey,gssapi-with-mic,password).
    

If you login as root to that system you can check the count:

    [root@rhel2 ~]# pam_tally2 --user=user1
    Login           Failures Latest failure     From
    user1               3    03/02/14 09:23:32  rhel1.local.com
    

You will also see the following in the **/var/log/secure** log:

    Mar  2 09:25:09 rhel2 sshd[9389]: pam_tally2(sshd:auth): user user1 (500) tally 4, deny 3
    

If you don't want to wait 20 minutes to release the lock you can manually reset the user's failed login count:

    [root@rhel2 ~]# pam_tally2 --user=user1 -r
    Login           Failures Latest failure     From
    user1               4    03/02/14 09:25:09  rhel1.local.com
    

Then if you try to login, you will see the following message:

    [root@rhel1 ~]# ssh rhel2 -l user1
    user1@rhel2's password: 
    Permission denied, please try again.
    user1@rhel2's password: 
    Permission denied, please try again.
    user1@rhel2's password: 
    Your account is locked. Maximum amount of failed attempts was reached.
    Your account is locked. Maximum amount of failed attempts was reached.
    Last login: Sun Mar  2 09:15:37 2014 from rhel1.local.com
    [user1@rhel2 ~]$
    

### PAM in Action again

Now let's block *user2* from logging in via ssh and allow *user1* to only login from a specific IP. This was actually covered in the security guide but in separate steps. First let's enable the **pam_access** module for sshd. This is done by adding the following to the **/etc/pam.d/sshd** file:

    account     required     pam_access.so
    

Lastly let's add the following to the **/etc/security/access.conf** file:

    + : user1 : 192.168.2.2
    - : user2 : ALL
    

Now trying to login as user1, from the approriate IP, I get in:

    [root@rhel1 ~]# ssh rhel2 -l user1
    user1@rhel2's password: 
    Last login: Sun Mar  2 09:34:48 2014 from rhel1.local.com
    [user1@rhel2 ~]$ logout
    

However trying the same thing with user2, I can't login:

    [root@rhel1 ~]# ssh rhel2 -l user2
    user2@rhel2's password: 
    Connection closed by 192.168.2.3
    [root@rhel1 ~]# 
    

Also on the rhel2 machine, we will see the following in the logs:

    [root@rhel2 ~]# tail -1 /var/log/secure
    Mar  2 09:35:24 rhel2 sshd[9506]: fatal: Access denied for user user2 by PAM account configuration
    

Lastly don't forget that you can change default password age and length using the **/etc/login.defs** file. This was covered in <a href="http://virtuallyhyper.com/2013/03/rhcsa-and-rhce-chapter-7-user-administration/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/03/rhcsa-and-rhce-chapter-7-user-administration/']);">RHCSA and RHCE Chapter 7</a>

