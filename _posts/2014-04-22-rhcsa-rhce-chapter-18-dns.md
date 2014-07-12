---
title: 'RHCSA and RHCE Chapter 18 - DNS'
author: Karim Elatov
layout: post
permalink: /2014/04/rhcsa-rhce-chapter-18-dns/
categories: ['certifications', 'home_lab', 'networking', 'os', 'rhcsa_rhce']
tags: ['bind', 'dns', 'linux','rhel']
---

## DNS

From the [Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> **DNS** (Domain Name System), also known as a *nameserver*, is a network system that associates hostnames with their respective IP addresses. For users, this has the advantage that they can refer to machines on the network by names that are usually easier to remember than the numerical network addresses. For system administrators, using the nameserver allows them to change the IP address for a host without ever affecting the name-based queries, or to decide which machines handle these queries.
>
> DNS is usually implemented using one or more centralized servers that are authoritative for certain domains. When a client host requests information from a nameserver, it usually connects to port 53. The nameserver then attempts to resolve the name requested. If it does not have an authoritative answer, or does not already have the answer cached from an earlier query, it queries other nameservers, called root nameservers, to determine which nameservers are authoritative for the name in question, and then queries them to get the requested name.

### Nameserver Zones

From the same guide:

> In a DNS server such as **BIND** (Berkeley Internet Name Domain), all information is stored in basic data elements called resource records (**RR**). The resource record is usually a fully qualified domain name (**FQDN**) of a host, and is broken down into multiple sections organized into a tree-like hierarchy. This hierarchy consists of a main trunk, primary branches, secondary branches, and so on.
>
> Each level of the hierarchy is divided by a period (that is, **.**). For Example a simple Resource Record is **bob.sales.example.com**, in this case **com** defines the *top-level domain*, **example** its subdomain, and **sales** the subdomain of **example**. In this case, **bob** identifies a resource record that is part of the **sales.example.com** domain. With the exception of the part furthest to the left (that is, **bob**), each of these sections is called a zone and defines a specific namespace.
>
> Zones are defined on authoritative nameservers through the use of zone files, which contain definitions of the resource records in each zone. Zone files are stored on **primary nameservers** (also called *master nameservers*), where changes are made to the files, and **secondary nameservers** (also called *slave* nameservers), which receive zone definitions from the primary nameservers. Both primary and secondary nameservers are authoritative for the zone and look the same to clients. Depending on the configuration, any nameserver can also serve as a primary or secondary server for multiple zones at the same time.

### Nameserver Types

From the above guide:

> There are two nameserver configuration types:
>
> *   **authoritative** - Authoritative nameservers answer to resource records that are part of their zones only. This category includes both primary (master) and secondary (slave) nameservers.
> *   **recursive** - Recursive nameservers offer resolution services, but they are not authoritative for any zone. Answers for all resolutions are cached in a memory for a fixed period of time, which is specified by the retrieved resource record.
>
> Although a nameserver can be both authoritative and recursive at the same time, it is recommended not to combine the configuration types. To be able to perform their work, authoritative servers should be available to all clients all the time. On the other hand, since the recursive lookup takes far more time than authoritative responses, recursive servers should be available to a restricted number of clients only, otherwise they are prone to distributed denial of service (DDoS) attacks.

### BIND Nameserver

From the Deployment Guide:

> BIND consists of a set of DNS-related programs. It contains a nameserver called **named**, an administration utility called **rndc**, and a debugging tool called **dig**.

#### Configuring named

From the same guide:

> When the named service is started, it reads the configuration from the following file:
>
> *   **/etc/named.conf** - The main configuration file.
> *   **/etc/named/** - An auxiliary directory for configuration files that are included in the main configuration file.
>
> The configuration file consists of a collection of statements with nested options surrounded by opening and closing curly brackets. Note that when editing the file, you have to be careful not to make any syntax error, otherwise the named service will not start. A typical **/etc/named.conf** file is organized as follows:
>
>     statement-1 ["statement-1-name"] [statement-1-class] {
>       option-1;
>       option-2;
>       option-N;
>     };
>     statement-2 ["statement-2-name"] [statement-2-class] {
>       option-1;
>       option-2;
>       option-N;
>     };
>     statement-N ["statement-N-name"] [statement-N-class] {
>       option-1;
>       option-2;
>       option-N;
>     };
>

#### Common *named* Statement Types

From the above guide:

> The following types of statements are commonly used in **/etc/named.conf**:
>
> #### acl
>
> The acl (Access Control List) statement allows you to define groups of hosts, so that they can be permitted or denied access to the nameserver. It takes the following form:
>
>     acl acl-name {
>       match-element;
>       ...
>     };
>
>
> The **acl-name** statement name is the name of the access control list, and the **match-element** option is usually an individual IP address (such as **10.0.1.1**) or a CIDR (Classless Inter-Domain Routing) network notation (for example, **10.0.1.0/24**). For a list of already defined keywords, see the below:
>
> *   **any** - Matches every IP address.
> *   **localhost** - Matches any IP address that is in use by the local system.
> *   **localnets** - Matches any IP address on any network to which the local system is connected.
> *   **none** - Does not match any IP address.
>
> The acl statement can be especially useful in conjunction with other statements such as options. The below example defines two access control lists, **black-hats** and **red-hats**, and adds **black-hats** on the blacklist while granting **red-hats** a normal access.
>
>     acl black-hats {
>       10.0.2.0/24;
>       192.168.0.0/24;
>       1234:5678::9abc/24;
>     };
>     acl red-hats {
>       10.0.1.0/24;
>     };
>     options {
>       blackhole { black-hats; };
>       allow-query { red-hats; };
>       allow-query-cache { red-hats; };
>     };
>
>
> #### include
>
> The include statement allows you to include files in the **/etc/named.conf**, so that potentially sensitive data can be placed in a separate file with restricted permissions. It takes the following form:
>
>     include "file-name"
>
>
> The **file-name** statement name is an absolute path to a file.
>
>     include "/etc/named.rfc1912.zones";
>
>
> #### options
>
> The options statement allows you to define global server configuration options as well as to set defaults for other statements. It can be used to specify the location of the **named** working directory, the types of queries allowed, and much more. It takes the following form:
>
>     options {
>       option;
>       ...
>     };
>
>
> For a list of frequently used **option** directives, see the below list:
>
> *   **allow-query** - Specifies which hosts are allowed to query the nameserver for authoritative resource records. It accepts an access control list, a collection of IP addresses, or networks in the CIDR notation. All hosts are allowed by default.
> *   **allow-query-cache** - Specifies which hosts are allowed to query the nameserver for non-authoritative data such as recursive queries. Only **localhost** and **localnets** are allowed by default.
> *   **blackhole** - Specifies which hosts are not allowed to query the nameserver. This option should be used when particular host or network floods the server with requests. The default option is **none**.
> *   **directory** - Specifies a working directory for the **named** service. The default option is **/var/named/**.
> *   **dnssec-enable** - Specifies whether to return DNSSEC related resource records. The default option is **yes**.
> *   **dnssec-validation** - Specifies whether to prove that resource records are authentic via DNSSEC. The default option is **yes**.
> *   **forwarders** - Specifies a list of valid IP addresses for nameservers to which the requests should be forwarded for resolution.
> *   **forward** - Specifies the behavior of the forwarders directive. It accepts the following options:
>
>     *   **first** - The server will query the nameservers listed in the forwarders directive before attempting to resolve the name on its own.
>     *   **only** - When unable to query the nameservers listed in the forwarders directive, the server will not attempt to resolve the name on its own.
>
> *   **listen-on** - Specifies the IPv4 network interface on which to listen for queries. On a DNS server that also acts as a gateway, you can use this option to answer queries originating from a single network only. All IPv4 interfaces are used by default.
>
> *   **listen-on-v6** - Specifies the IPv6 network interface on which to listen for queries. On a DNS server that also acts as a gateway, you can use this option to answer queries originating from a single network only. All IPv6 interfaces are used by default.
>
> *   **max-cache-size** - Specifies the maximum amount of memory to be used for server caches. When the limit is reached, the server causes records to expire prematurely so that the limit is not exceeded. In a server with multiple views, the limit applies separately to the cache of each view. The default option is **32M**.
>
> *   **notify** - Specifies whether to notify the secondary nameservers when a zone is updated. It accepts the following options:
>
>     *   **yes** - The server will notify all secondary nameservers.
>     *   **no** - The server will not notify any secondary nameserver.
>     *   **master-only** - The server will notify primary server for the zone only.
>     *   **explicit** - The server will notify only the secondary servers that are specified in the also-notify list within a zone statement.
>
> *   **pid-file** - Specifies the location of the process ID file created by the **named** service.
>
> *   **recursion** - Specifies whether to act as a recursive server. The default option is **yes**.
>
> *   **statistics-file** Specifies an alternate location for statistics files. The **/var/named/named.stats** file is used by default.
>
> An example of **options** usage:
>
>     options {
>       allow-query       { localhost; };
>       listen-on port    53 { 127.0.0.1; };
>       listen-on-v6 port 53 { ::1; };
>       max-cache-size    256M;
>       directory         "/var/named";
>       statistics-file   "/var/named/data/named_stats.txt";
>
>       recursion         yes;
>       dnssec-enable     yes;
>       dnssec-validation yes;
>     };
>
>
> #### zone
>
> The zone statement allows you to define the characteristics of a zone, such as the location of its configuration file and zone-specific options, and can be used to override the global options statements. It takes the following form:
>
>     zone zone-name [zone-class] {
>       option;
>       ...
>     };
>
>
> The **zone-name** attribute is the name of the zone, **zone-class** is the optional class of the zone, and **option** is a zone statement option as described below.
>
> The **zone-name** attribute is particularly important, as it is the default value assigned for the **$ORIGIN** directive used within the corresponding zone file located in the **/var/named/** directory. The **named** daemon appends the name of the zone to any non-fully qualified domain name listed in the zone file. For example, if a zone statement defines the namespace for **example.com**, use **example.com** as the **zone-name** so that it is placed at the end of hostnames within the **example.com** zone file.
>
> Here is a list of common **options**:
>
> *   **allow-query** - Specifies which clients are allowed to request information about this zone. This option overrides global allow-query option. All query requests are allowed by default.
> *   **allow-transfer** - Specifies which secondary servers are allowed to request a transfer of the zone's information. All transfer requests are allowed by default.
> *   **allow-update** - Specifies which hosts are allowed to dynamically update information in their zone. The default option is to deny all dynamic update requests.
>
>     Note that you should be careful when allowing hosts to update information about their zone. Do not set IP addresses in this option unless the server is in the trusted network. Instead, use TSIG (Transaction SIGnatures) key.
>
> *   **file** - Specifies the name of the file in the **named** working directory that contains the zone's configuration data.
>
> *   **masters** Specifies from which IP addresses to request authoritative zone information. This option is used only if the zone is defined as type slave.
>
> *   **notify** Specifies whether to notify the secondary nameservers when a zone is updated. It accepts the following options:
>
>     *   **yes** - The server will notify all secondary nameservers.
>     *   **no** - The server will not notify any secondary nameserver.
>     *   **master-only** - The server will notify primary server for the zone only.
>     *   **explicit** - The server will notify only the secondary servers that are specified in the also-notify list within a zone statement.
>
> *   **type** Specifies the zone type. It accepts the following options:
>
>     *   **delegation-only** - Enforces the delegation status of infrastructure zones such as COM, NET, or ORG. Any answer that is received without an explicit or implicit delegation is treated as NXDOMAIN. This option is only applicable in TLDs (Top-Level Domain) or root zone files used in recursive or caching implementations.
>     *   **forward** - Forwards all requests for information about this zone to other nameservers.
>     *   **hint** - A special type of zone used to point to the root nameservers which resolve queries when a zone is not otherwise known. No configuration beyond the default is necessary with a hint zone.
>     *   **master** - Designates the nameserver as authoritative for this zone. A zone should be set as the master if the zone's configuration files reside on the system.
>     *   **slave** - Designates the nameserver as a slave server for this zone. Master server is specified in masters directive.
>
> Most changes to the **/etc/named.conf** file of a primary or secondary nameserver involve adding, modifying, or deleting zone statements, and only a small subset of zone statement options is usually needed for a nameserver to work efficiently.
>
> In the below example, the zone is identified as **example.com**, the type is set to **master**, and the **named** service is instructed to read the **/var/named/example.com.zone** file. It also allows only a secondary nameserver (**192.168.0.2**) to transfer the zone.
>
>     zone "example.com" IN {
>       type master;
>       file "example.com.zone";
>       allow-transfer { 192.168.0.2; };
>     };
>
>
> A secondary server's zone statement is slightly different. The type is set to **slave**, and the **masters** directive is telling named the IP address of the master server.
>
> In the below example, the **named** service is configured to query the primary server at the **192.168.0.1** IP address for information about the **example.com** zone. The received information is then saved to the **/var/named/slaves/example.com.zone** file. Note that you have to put all slave zones to **/var/named/slaves** directory, otherwise the service will fail to transfer the zone.
>
>     zone "example.com" {
>       type slave;
>       file "slaves/example.com.zone";
>       masters { 192.168.0.1; };
>     };
>

#### Other *named* Statement Types

From the Deployment Guide:

> The following types of statements are less commonly used in **/etc/named.conf**:
>
> *   **controls** - The **controls** statement allows you to configure various security requirements necessary to use the **rndc** command to administer the named service.
> *   **key** - The **key** statement allows you to define a particular key by name. Keys are used to authenticate various actions, such as secure updates or the use of the rndc command. Two options are used with key:
>
>     *   algorithm **algorithm-name** — The type of algorithm to be used (for example, **hmac-md5**).
>     *   secret "**key-value**" — The encrypted key.
>
> *   **logging** - The logging statement allows you to use multiple types of logs, so called **channels**. By using the channel option within the statement, you can construct a customized type of log with its own file name (file), size limit (size), versioning (version), and level of importance (severity). Once a customized channel is defined, a category option is used to categorize the channel and begin logging when the named service is restarted.
>
>     By default, **named** sends standard messages to the **rsyslog** daemon, which places them in **/var/log/messages**. Several standard channels are built into BIND with various severity levels, such as **default_syslog** (which handles informational logging messages) and **default_debug** (which specifically handles debugging messages). A default category, called **default**, uses the built-in channels to do normal logging without any special configuration.
>
> *   **server** - The server statement allows you to specify options that affect how the named service should respond to remote nameservers, especially with regard to notifications and zone transfers.
>
>     The **transfer-format** option controls the number of resource records that are sent with each message. It can be either **one-answer** (only one resource record), or **many-answers** (multiple resource records). Note that while the **many-answers** option is more efficient, it is not supported by older versions of BIND.
>
> *   **trusted-keys** - The trusted-keys statement allows you to specify assorted public keys used for secure DNS (DNSSEC).
>
> *   **view** - The view statement allows you to create special views depending upon which network the host querying the nameserver is on. This allows some hosts to receive one answer regarding a zone while other hosts receive totally different information. Alternatively, certain zones may only be made available to particular trusted hosts while non-trusted hosts can only make queries for other zones.
>
>     Multiple views can be used as long as their names are unique. The **match-clients** option allows you to specify the IP addresses that apply to a particular view. If the options statement is used within a view, it overrides the already configured global options. Finally, most view statements contain multiple zone statements that apply to the match-clients list.
>
>     Note that the order in which the view statements are listed is important, as the first statement that matches a particular client's IP address is used.

#### Common *named* Directives

From the same guide:

> Directives begin with the dollar sign character followed by the name of the directive, and usually appear at the top of the file. The following directives are commonly used in zone files:
>
> *   **$INCLUDE** - The **$INCLUDE** directive allows you to include another file at the place where it appears, so that other zone settings can be stored in a separate zone file.
>
>         $INCLUDE /var/named/penguin.example.com
>
>
> *   **$ORIGIN** - The **$ORIGIN** directive allows you to append the domain name to unqualified records, such as those with the hostname only. Note that the use of this directive is not necessary if the zone is specified in **/etc/named.conf**, since the zone name is used by default.
>
>     In the below example, any names used in resource records that do not end in a trailing period are appended with **example.com**.
>
>         $ORIGIN example.com.
>
>
> *   **$TTL** - The **$TTL** directive allows you to set the default Time to Live (TTL) value for the zone, that is, how long is a zone record valid. Each resource record can contain its own TTL value, which overrides this directive.
>
>     Increasing this value allows remote nameservers to cache the zone information for a longer period of time, reducing the number of queries for the zone and lengthening the amount of time required to propagate resource record changes.
>
>         $TTL 1D
>

#### Common *named* Resource Records

From the above guide:

> The following resource records are commonly used in zone files:
>
> #### A
>
> The Address record specifies an IP address to be assigned to a name. It takes the following form:
>
>     hostname IN A IP-address
>
>
> If the hostname value is omitted, the record will point to the last specified hostname. In the below example, the requests for **server1.example.com** are pointed to **10.0.1.3** or **10.0.1.5**.
>
>     server1  IN  A  10.0.1.3
>              IN  A  10.0.1.5
>
>
> #### CNAME
>
> The Canonical Name record maps one name to another. Because of this, this type of record is sometimes referred to as an alias record. It takes the following form:
>
>     alias-name IN CNAME real-name
>
>
> **CNAME** records are most commonly used to point to services that use a common naming scheme, such as **www** for Web servers. However, there are multiple restrictions for their usage:
>
> *   **CNAME** records should not point to other CNAME records. This is mainly to avoid possible infinite loops.
> *   **CNAME** records should not contain other resource record types (such as A, NS, MX, etc.). The only exception are DNSSEC related records (that is, RRSIG, NSEC, etc.) when the zone is signed.
> *   Other resource record that point to the fully qualified domain name (FQDN) of a host (that is, NS, MX, PTR) should not point to a CNAME record.
>
> In the below example, the **A** record binds a hostname to an IP address, while the **CNAME** record points the commonly used **www** hostname to it.
>
>     server1  IN  A      10.0.1.5
>     www      IN  CNAME  server1
>
>
> #### MX
>
> The Mail Exchange record specifies where the mail sent to a particular namespace controlled by this zone should go. It takes the following form:
>
>     IN MX preference-value email-server-name
>
>
> The **email-server-name** is a fully qualified domain name (FQDN). The **preference-value** allows numerical ranking of the email servers for a namespace, giving preference to some email systems over others. The **MX** resource record with the lowest preference-value is preferred over the others. However, multiple email servers can possess the same value to distribute email traffic evenly among them. In the below example, the first **mail.example.com** email server is preferred to the **mail2.example.com** email server when receiving email destined for the example.com domain.
>
>     example.com.  IN  MX  10  mail.example.com.
>                   IN  MX  20  mail2.example.com.
>
>
> #### NS
>
> The Nameserver record announces authoritative nameservers for a particular zone. It takes the following form:
>
>     IN NS nameserver-name
>
>
> The **nameserver-name** should be a fully qualified domain name (FQDN). Note that when two nameservers are listed as authoritative for the domain, it is not important whether these nameservers are secondary nameservers, or if one of them is a primary server. They are both still considered authoritative.
>
>     IN  NS  dns1.example.com.
>     IN  NS  dns2.example.com.
>
>
> #### PTR
>
> The Pointer record points to another part of the namespace. It takes the following form:
>
>     last-IP-digit IN PTR FQDN-of-system
>
>
> The **last-IP-digit** directive is the last number in an IP address, and the **FQDN-of-system** is a fully qualified domain name (FQDN).
>
> **PTR** records are primarily used for reverse name resolution, as they point IP addresses back to a particular name.
>
> #### SOA
>
> The Start of Authority record announces important authoritative information about a namespace to the nameserver. Located after the directives, it is the first resource record in a zone file. It takes the following form:
>
>     @  IN  SOA  primary-name-server hostmaster-email (
>            serial-number
>            time-to-refresh
>            time-to-retry
>            time-to-expire
>            minimum-TTL )
>
>
> The directives are as follows:
>
> *   The **@** symbol places the **$ORIGIN** directive (or the zone's name if the $ORIGIN directive is not set) as the namespace being defined by this SOA resource record.
> *   The **primary-name-server** directive is the hostname of the primary nameserver that is authoritative for this domain.
> *   The **hostmaster-email** directive is the email of the person to contact about the namespace.
> *   The **serial-number** directive is a numerical value incremented every time the zone file is altered to indicate it is time for the named service to reload the zone.
> *   The **time-to-refresh** directive is the numerical value secondary nameservers use to determine how long to wait before asking the primary nameserver if any changes have been made to the zone.
> *   The **time-to-retry** directive is a numerical value used by secondary nameservers to determine the length of time to wait before issuing a refresh request in the event that the primary nameserver is not answering. If the primary server has not replied to a refresh request before the amount of time specified in the **time-to-expire** directive elapses, the secondary servers stop responding as an authority for requests concerning that namespace.
> *   In BIND 4 and 8, the **minimum-TTL** directive is the amount of time other nameservers cache the zone's information. In BIND 9, it defines how long negative answers are cached for. Caching of negative answers can be set to a maximum of 3 hours (that is, **3H**).
>
> When configuring BIND, all times are specified in seconds. However, it is possible to use abbreviations when specifying units of time other than seconds, such as minutes (**M**), hours (**H**), days (**D**), and weeks (**W**). The below list shows an amount of time in seconds and the equivalent time in another format.
>
> *   60 - 1M
> *   1800 - 30M
> *   3600 - 1H
> *   10800 - 3H
> *   21600 - 6H
> *   43200 - 12H
> *   86400 - 1D
> *   259200 - 3D
> *   604800 - 1W
> *   31536000 - 365D
>
> Example of an SOA record:
>
>     @  IN  SOA  dns1.example.com.  hostmaster.example.com. (
>            2001062501  ; serial
>            21600       ; refresh after 6 hours
>            3600        ; retry after 1 hour
>            604800      ; expire after 1 week
>            86400 )     ; minimum TTL of 1 day
>

#### *named* simple example

From the Deployment Guide:

> The below example demonstrates the use of standard directives and **SOA** values.
>
>     $ORIGIN example.com.
>     $TTL 86400
>     @         IN  SOA  dns1.example.com.  hostmaster.example.com. (
>                   2001062501  ; serial
>                   21600       ; refresh after 6 hours
>                   3600        ; retry after 1 hour
>                   604800      ; expire after 1 week
>                   86400 )     ; minimum TTL of 1 day
>     ;
>     ;
>               IN  NS     dns1.example.com.
>               IN  NS     dns2.example.com.
>     dns1      IN  A      10.0.1.1
>               IN  AAAA   aaaa:bbbb::1
>     dns2      IN  A      10.0.1.2
>               IN  AAAA   aaaa:bbbb::2
>     ;
>     ;
>     @         IN  MX     10  mail.example.com.
>               IN  MX     20  mail2.example.com.
>     mail      IN  A      10.0.1.5
>               IN  AAAA   aaaa:bbbb::5
>     mail2     IN  A      10.0.1.6
>               IN  AAAA   aaaa:bbbb::6
>     ;
>     ;
>     ; This sample zone file illustrates sharing the same IP addresses
>     ; for multiple services:
>     ;
>     services  IN  A      10.0.1.10
>               IN  AAAA   aaaa:bbbb::10
>               IN  A      10.0.1.11
>               IN  AAAA   aaaa:bbbb::11
>
>     ftp       IN  CNAME  services.example.com.
>     www       IN  CNAME  services.example.com.
>     ;
>     ;
>
>
> In this example, the authoritative nameservers are set as **dns1.example.com** and **dns2.example.com**, and are tied to the **10.0.1.1** and **10.0.1.2** IP addresses respectively using the **A** record.
>
> The email servers configured with the **MX** records point to **mail** and **mail2** via **A** records. Since these names do not end in a trailing period, the **$ORIGIN** domain is placed after them, expanding them to **mail.example.com** and **mail2.example.com**.
>
> Services available at the standard names, such as **www.example.com** (WWW), are pointed at the appropriate servers using the **CNAME** record.
>
> This zone file would be called into service with a **zone** statement in the **/etc/named.conf** similar to the following:
>
>     zone "example.com" IN {
>       type master;
>       file "example.com.zone";
>       allow-update { none; };
>     };
>

#### Reverse Zone *named* example

From the same guide:

> A reverse name resolution zone file is used to translate an IP address in a particular namespace into an fully qualified domain name (FQDN). It looks very similar to a standard zone file, except that the **PTR** resource records are used to link the IP addresses to a fully qualified domain name as shown the below example:
>
>     $ORIGIN 1.0.10.in-addr.arpa.
>     $TTL 86400
>     @  IN  SOA  dns1.example.com.  hostmaster.example.com. (
>            2001062501  ; serial
>            21600       ; refresh after 6 hours
>            3600        ; retry after 1 hour
>            604800      ; expire after 1 week
>            86400 )     ; minimum TTL of 1 day
>     ;
>     @  IN  NS   dns1.example.com.
>     ;
>     1  IN  PTR  dns1.example.com.
>     2  IN  PTR  dns2.example.com.
>     ;
>     5  IN  PTR  server1.example.com.
>     6  IN  PTR  server2.example.com.
>     ;
>     3  IN  PTR  ftp.example.com.
>     4  IN  PTR  ftp.example.com.
>
>
> In this example, IP addresses **10.0.1.1** through **10.0.1.6** are pointed to the corresponding fully qualified domain name.
>
> This zone file would be called into service with a **zone** statement in the **/etc/named.conf** file similar to the following:
>
>     zone "1.0.10.in-addr.arpa" IN {
>       type master;
>       file "example.com.rr.zone";
>       allow-update { none; };
>     };
>
>
> There is very little difference between this example and a standard **zone** statement, except for the zone name. Note that a reverse name resolution zone requires the first three blocks of the IP address reversed followed by **.in-addr.arpa**. This allows the single block of IP numbers used in the reverse name resolution zone file to be associated with the zone.

### *named* primary/master example

So let's try this out. Let's configure our RH6 machine to be a primary (master) DNS server. First let's install the necessary packages:

    [root@rhel1 ~]# yum install bind


By default the service is disabled:

    [root@rhel1 ~]# chkconfig --list named
    named           0:off   1:off   2:off   3:off   4:off   5:off   6:off


Here is the default named configuration:

    [root@rhel1 ~]# cat /etc/named.conf
    //
    // named.conf
    //
    // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
    // server as a caching only nameserver (as a localhost DNS resolver only).
    //
    // See /usr/share/doc/bind*/sample/ for example named configuration files.
    //

    options {
        listen-on port 53 { 127.0.0.1; };
        listen-on-v6 port 53 { ::1; };
        directory   "/var/named";
        dump-file   "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query     { localhost; };
        recursion yes;

        dnssec-enable yes;
        dnssec-validation yes;
        dnssec-lookaside auto;

        /* Path to ISC DLV key */
        bindkeys-file "/etc/named.iscdlv.key";
    };

    logging {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };

    zone "." IN {
        type hint;
        file "named.ca";
    };

    include "/etc/named.rfc1912.zones";


So let's go ahead and disable IPv6, allow queries from the local network, and remove the advanced configuration:

    options {
            listen-on port 53 { 127.0.0.1; 192.168.2.2; };
            directory       "/var/named";
            dump-file       "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
            allow-query     { 127.0.0.1; 192.168.2.0/24; };
            recursion yes;
    };


Now let's add a forward and reverse zone for **local.com** to the **/etc/named.conf**:

    /* local.com forward/standard zone */
    zone "local.com" {
            type master;
            file "local.com.zone";
            allow-update { none; };
    };
    /* reverse lookup for subnet 192.168.2.0/24 */
    zone "2.168.192.in-addr.arpa" {
            type master;
            file "local.com.revzone";
            allow-update { none; };
    };


At this point we can make sure the **named** configuration is okay, by running **named-checkconf**:

    [root@rhel1 ~]# named-checkconf -p
    options {
        directory "/var/named";
        dump-file "/var/named/data/cache_dump.db";
        listen-on port 53 {
            127.0.0.1/32;
            192.168.2.2/32;
        };
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        statistics-file "/var/named/data/named_stats.txt";
        recursion yes;
        allow-query {
            127.0.0.1/32;
            192.168.2.0/24;
        };
    };
    logging {
        channel "default_debug" {
            file "data/named.run";
            severity dynamic;
        };
    };
    zone "." IN {
        type hint;
        file "named.ca";
    };
    zone "local.com" {
        type master;
        file "dynamic/local.com.zone";
        allow-update {
            "none";
        };
    };
    zone "2.168.192.in-addr.arpa" {
        type master;
        file "dynamic/local.com.revzone";
        allow-update {
            "none";
        };
    };
    zone "localhost.localdomain" IN {
        type master;
        file "named.localhost";
        allow-update {
            "none";
        };
    };
    zone "localhost" IN {
        type master;
        file "named.localhost";
        allow-update {
            "none";
        };
    };
    zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
        type master;
        file "named.loopback";
        allow-update {
            "none";
        };
    };
    zone "1.0.0.127.in-addr.arpa" IN {
        type master;
        file "named.loopback";
        allow-update {
            "none";
        };
    };
    zone "0.in-addr.arpa" IN {
        type master;
        file "named.empty";
        allow-update {
            "none";
        };
    };


Notice I prepended the zone file with **dynamic**, this is because starting with RHEL6 the **/var/named** is not writable by **named**:

    [root@rhel1 ~]# ls -ld /var/named
    drwxr-x---. 5 root named 4096 Apr 13 12:22 /var/named
    [root@rhel1 ~]# ls -ld /var/named/dynamic/
    drwxrwx---. 2 named named 4096 Apr 13 12:16 /var/named/dynamic/


If there are no errors and the configuration looks good, then we can proceed. Now let's create the zones files. First for the standard zone file. There is a very simple template under the **/usr/share/doc/bind** directory:

    [root@rhel1 ~]# cat /usr/share/doc/bind-9.7.3/sample/var/named/named.localhost
    $TTL 1D
    @   IN SOA  @ rname.invalid. (
                        0   ; serial
                        1D  ; refresh
                        1H  ; retry
                        1W  ; expire
                        3H )    ; minimum
        NS  @
        A   127.0.0.1
        AAAA    ::1


Now let's copy the configuration :

    [root@rhel1 ~]# cp /usr/share/doc/bind-9.7.3/sample/var/named/named.localhost /var/named/dynamic/local.com.zone


Then edit the file to update the necessary the settings. Here is how my file looked like in the end:

    [root@rhel1 ~]# cat /var/named/dynamic/local.com.zone
    $TTL 1D
    @   IN SOA  rhel1.local.com. root.local.com. (
        0   ; serial
        1D  ; refresh
        1H  ; retry
        1W  ; expire
        3H )    ; minimum

    ; Nameservers
    @   IN  NS  rhel1.local.com.
    @   IN  A   192.168.2.2

    ; Networking Hosts
    rhel1   IN  A   192.168.2.2
    rhel2   IN  A   192.168.2.3
    google  IN  A   192.168.2.4


Now let's create the reverse zone. With this one, we can just copy the standard zone and modify it to include pointer records:

    [root@rhel1 ~]# cp /var/named/dynamic/local.com.zone /var/named/dynamic/local.com.revzone


Then edit the file to have the pointer records:

    [root@rhel1 ~]# cat /var/named/dynamic/local.com.revzone
    $TTL 1D
    @   IN SOA  rhel1.local.com. root.local.com. (
        0   ; serial
        1D  ; refresh
        1H  ; retry
        1W  ; expire
        3H )    ; minimum

    ; Nameservers
    @   IN  NS  rhel1.local.com.

    ; Networking Hosts
    2   IN  PTR rhel1.local.com.
    3   IN  PTR rhel2.local.com.
    4   IN  PTR google.local.com.


After you are done, you can check the zone file to make sure it's correct:

    [root@rhel1 ~]# named-checkzone local.com /var/named/dynamic/local.com.zone
    zone local.com/IN: loaded serial 0
    OK


To check all the zones, you can run the following:

    [root@rhel1 ~]# named-checkconf -z
    zone local.com/IN: loaded serial 0
    zone 2.168.192.in-addr.arpa/IN: loaded serial 0
    zone localhost.localdomain/IN: loaded serial 0
    zone localhost/IN: loaded serial 0
    zone 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa/IN: loaded serial 0
    zone 1.0.0.127.in-addr.arpa/IN: loaded serial 0
    zone 0.in-addr.arpa/IN: loaded serial 0


By default the init script checks all the zone files, you can disable this under the **/etc/sysconfig/named** file:

    [root@rhel1 ~]# tail -5 /etc/sysconfig/named
    # DISABLE_ZONE_CHECKING  -- By default, initscript calls named-checkzone
    #               utility for every zone to ensure all zones are
    #               valid before named starts. If you set this option
    #               to 'yes' then initscript doesn't perform those
    #               checks.


But I would recommend leaving that in place. Now let's open up the necessary DNS ports on the DNS server:

    [root@rhel1 ~]#iptables -I INPUT 18 -p udp -m udp --dport 53 -j ACCEPT
    [root@rhel1 ~]#iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 53 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


For DNS queries we just need the **UDP** port, but since we will be setting up primary and secondary DNS server, the **TCP** port is used for transferring zones between the DNS servers. Lastly make sure our client machine is setup to use our DNS server as it's nameserver (this is done under the **/etc/resolv.conf** file):

    [root@rhel2 ~]# cat /etc/resolv.conf
    search local.com
    nameserver 192.168.2.2


On the server let's start the **named** daemon:

    [root@rhel1 ~]# service named start
    Starting named:  named


If you look under **/var/log/messages**, you should see your zones loaded:

    Apr 13 11:59:14 rhel1 named[4531]: zone 0.in-addr.arpa/IN: loaded serial 0
    Apr 13 11:59:14 rhel1 named[4531]: zone 1.0.0.127.in-addr.arpa/IN: loaded serial
     0
    Apr 13 11:59:14 rhel1 named[4531]: zone 2.168.192.in-addr.arpa/IN: loaded serial
     0
    Apr 13 11:59:14 rhel1 named[4531]: zone 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.
    0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa/IN: loaded serial 0
    Apr 13 11:59:14 rhel1 named[4531]: zone local.com/IN: loaded serial 0
    Apr 13 11:59:14 rhel1 named[4531]: zone localhost.localdomain/IN: loaded serial 0
    Apr 13 11:59:14 rhel1 named[4531]: zone localhost/IN: loaded serial 0


As a quick test, run a DNS query from the client machine:

    [root@rhel2 ~]# dig rhel2.local.com

    ; <<>> DiG 9.3.6-P1-RedHat-9.3.6-4.P1.el5_4.2 <<>> rhel2.local.com
    ;; global options:  printcmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64625
    ;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

    ;; QUESTION SECTION:
    ;rhel2.local.com.       IN  A

    ;; ANSWER SECTION:
    rhel2.local.com.    86400   IN  A   192.168.2.3

    ;; AUTHORITY SECTION:
    local.com.      86400   IN  NS  rhel1.local.com.

    ;; ADDITIONAL SECTION:
    rhel1.local.com.    86400   IN  A   192.168.2.2

    ;; Query time: 0 msec
    ;; SERVER: 192.168.2.2#53(192.168.2.2)
    ;; WHEN: Sun Apr 13 12:03:07 2014
    ;; MSG SIZE  rcvd: 85


When using **dig**, it shows a lot of good information, like who is the authoritative DNS server is (in our case we can see that's **rhel1.local.com**) and of course the response to our query (**192.168.2.3**). Here is a similar response for the reverse lookup:

    [root@rhel2 ~]# dig -x 192.168.2.4

    ; <<>> DiG 9.3.6-P1-RedHat-9.3.6-4.P1.el5_4.2 <<>> -x 192.168.2.4
    ;; global options:  printcmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1784
    ;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

    ;; QUESTION SECTION:
    ;4.2.168.192.in-addr.arpa.  IN  PTR

    ;; ANSWER SECTION:
    4.2.168.192.in-addr.arpa. 86400 IN  PTR google.local.com.

    ;; AUTHORITY SECTION:
    2.168.192.in-addr.arpa. 86400   IN  NS  rhel1.local.com.

    ;; ADDITIONAL SECTION:
    rhel1.local.com.    86400   IN  A   192.168.2.2

    ;; Query time: 0 msec
    ;; SERVER: 192.168.2.2#53(192.168.2.2)
    ;; WHEN: Sun Apr 13 12:05:28 2014
    ;; MSG SIZE  rcvd: 108


If you don't want that much information, the **host** command is really terse:

    [root@rhel2 ~]# host rhel2.local.com
    rhel2.local.com has address 192.168.2.3
    [root@rhel2 ~]# host 192.168.2.4
    4.2.168.192.in-addr.arpa domain name pointer google.local.com.


#### Using the dig Utility

From the Deployment Guide:

> The **dig** utility is a command line tool that allows you to perform DNS lookups and debug a nameserver configuration. Its typical usage is as follows:
>
>     dig [@server] [option...] name type
>
>
> To look up a nameserver for a particular domain, use the command in the following form:
>
>     dig name NS
>
>
> In the below example, the dig utility is used to display nameservers for **example.com**.
>
>     ~]$ dig example.com NS
>
>     ; <<>> DiG 9.7.1-P2-RedHat-9.7.1-2.P2.fc13 <<>> example.com NS
>     ;; global options: +cmd
>     ;; Got answer:
>     ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57883
>     ;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
>
>     ;; QUESTION SECTION:
>     ;example.com.                   IN      NS
>
>     ;; ANSWER SECTION:
>     example.com.            99374   IN      NS      a.iana-servers.net.
>     example.com.            99374   IN      NS      b.iana-servers.net.
>
>     ;; Query time: 1 msec
>     ;; SERVER: 10.34.255.7#53(10.34.255.7)
>     ;; WHEN: Wed Aug 18 18:04:06 2010
>     ;; MSG SIZE  rcvd: 77
>
>
> To look up an IP address assigned to a particular domain, use the command in the following form:
>
>     dig name A
>
>
> In the below example, the **dig** utility is used to display the IP address of **example.com**.
>
>     ~]$ dig example.com A
>
>     ; <<>> DiG 9.7.1-P2-RedHat-9.7.1-2.P2.fc13 <<>> example.com A
>     ;; global options: +cmd
>     ;; Got answer:
>     ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4849
>     ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 0
>
>     ;; QUESTION SECTION:
>     ;example.com.                   IN      A
>
>     ;; ANSWER SECTION:
>     example.com.            155606  IN      A       192.0.32.10
>
>     ;; AUTHORITY SECTION:
>     example.com.            99175   IN      NS      a.iana-servers.net.
>     example.com.            99175   IN      NS      b.iana-servers.net.
>
>     ;; Query time: 1 msec
>     ;; SERVER: 10.34.255.7#53(10.34.255.7)
>     ;; WHEN: Wed Aug 18 18:07:25 2010
>     ;; MSG SIZE  rcvd: 93
>
>
> To look up a hostname for a particular IP address, use the command in the following form:
>
>     dig -x address
>
>
> In the below example, the **dig** utility is used to display the hostname assigned to **192.0.32.10**.
>
>     ~]$ dig -x 192.0.32.10
>
>     ; <<>> DiG 9.7.1-P2-RedHat-9.7.1-2.P2.fc13 <<>> -x 192.0.32.10
>     ;; global options: +cmd
>     ;; Got answer:
>     ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29683
>     ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 5, ADDITIONAL: 6
>
>     ;; QUESTION SECTION:
>     ;10.32.0.192.in-addr.arpa.      IN      PTR
>
>     ;; ANSWER SECTION:
>     10.32.0.192.in-addr.arpa. 21600 IN      PTR     www.example.com.
>
>     ;; AUTHORITY SECTION:
>     32.0.192.in-addr.arpa.  21600   IN      NS      b.iana-servers.org.
>     32.0.192.in-addr.arpa.  21600   IN      NS      c.iana-servers.net.
>     32.0.192.in-addr.arpa.  21600   IN      NS      d.iana-servers.net.
>     32.0.192.in-addr.arpa.  21600   IN      NS      ns.icann.org.
>     32.0.192.in-addr.arpa.  21600   IN      NS      a.iana-servers.net.
>
>     ;; ADDITIONAL SECTION:
>     a.iana-servers.net.     13688   IN      A       192.0.34.43
>     b.iana-servers.org.     5844    IN      A       193.0.0.236
>     b.iana-servers.org.     5844    IN      AAAA    2001:610:240:2::c100:ec
>     c.iana-servers.net.     12173   IN      A       139.91.1.10
>     c.iana-servers.net.     12173   IN      AAAA    2001:648:2c30::1:10
>     ns.icann.org.           12884   IN      A       192.0.34.126
>
>     ;; Query time: 156 msec
>     ;; SERVER: 10.34.255.7#53(10.34.255.7)
>     ;; WHEN: Wed Aug 18 18:25:15 2010
>     ;; MSG SIZE  rcvd: 310
>

#### *named* secondary/slave example

Now let's configure our RH5 machine as a secondary/slave DNS server for the **local.com** domain. First let's install the necessary packages:

    [root@rhel2 ~]# yum install bind


Now let's copy the sample configuration:

    [root@rhel2 ~]# cp /usr/share/doc/bind-9.3.6/sample/etc/named.conf /etc/named.conf


Then edit the configuration and remove any miscellaneous settings. In the end I had the following:

    [root@rhel2 ~]# cat /etc/named.conf
    options
    {
        // Put files that named is allowed to write in the data/ directory:
        directory "/var/named"; // the default
        dump-file       "data/cache_dump.db";
            statistics-file     "data/named_stats.txt";
            memstatistics-file  "data/named_mem_stats.txt";

    };
    logging
    {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };


Now let's add the local zones and the root DNS servers:

    zone "." IN {
            type hint;
            file "named.root";
    };

    zone "localhost." IN {
            type master;
            file "localhost.zone";
            allow-update { none; };
    };

    zone "0.0.127.in-addr.arpa." IN {
            type master;
            file "named.local";
            allow-update { none; };
    };


Then let's copy those zones into the **/var/named** directory:

    [root@rhel2 ~]# cp /usr/share/doc/bind-9.3.6/sample/var/named/{named.root,localhost.zone,named.local} /var/named/.


Lastly let's add the zones that we will be the secondary/slave DNS server for:

    zone "local.com" {
            type slave;
            file "slaves/example.com.zone";
            masters { 192.168.2.2; };
    };

    zone "2.168.192.in-addr.arpa" {
            type slave;
            file "slaves/example.com.revzone";
            masters { 192.168.2.2; };
    };


Let's make sure the configuration is okay:

    [root@rhel2 ~]# named-checkconf
    [root@rhel2 ~]# echo $?
    0


If a status of **1** is returned then something is wrong with the configuration. The last thing to do on the secondary server is to open the firewall for TCP and UDP port 53:

    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 18 -p udp -m udp --dport 53 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 18 -m state --state NEW -m tcp -p tcp --dport 53 -j ACCEPT
    [root@rhel2 ~]# service iptables save
    Saving firewall rules to /etc/sysconfig/iptables:          [  OK  ]


Let's make sure the zones configs are okay and start the service:

    [root@rhel2 ~]# service named configtest
    zone localhost/IN: loaded serial 42
    zone 0.0.127.in-addr.arpa/IN: loaded serial 1997022700
    [root@rhel2 ~]# service named start
    Starting named:                                            [  OK  ]


Initially you will see that the zone transfer has failed:

    [root@rhel2 log]# tail messages
    Apr 13 13:09:37 rhel2 named[8080]: zone localhost/IN: loaded serial 42
    Apr 13 13:09:37 rhel2 named[8080]: running
    Apr 13 13:09:37 rhel2 named[8080]: zone local.com/IN: Transfer started.
    Apr 13 13:09:37 rhel2 named[8080]: transfer of 'local.com/IN' from 192.168.2.2#53: connected using 192.168.2.3#42006
    Apr 13 13:09:37 rhel2 named[8080]: transfer of 'local.com/IN' from 192.168.2.2#53: failed while receiving responses: REFUSED
    Apr 13 13:09:37 rhel2 named[8080]: transfer of 'local.com/IN' from 192.168.2.2#53: end of transfer
    Apr 13 13:09:38 rhel2 named[8080]: zone 2.168.192.in-addr.arpa/IN: Transfer started.
    Apr 13 13:09:38 rhel2 named[8080]: transfer of '2.168.192.in-addr.arpa/IN' from 192.168.2.2#53: connected using 192.168.2.3#39859
    Apr 13 13:09:38 rhel2 named[8080]: transfer of '2.168.192.in-addr.arpa/IN' from 192.168.2.2#53: failed while receiving responses: REFUSED
    Apr 13 13:09:38 rhel2 named[8080]: transfer of '2.168.192.in-addr.arpa/IN' from 192.168.2.2#53: end of transfer


This is expected since, we have setup the master yet. So let's configure our master to allow the zone transfers. Edit the **named.conf** file to look like this:

    /* local.com forward/standard zone */
    zone "local.com" {
            type master;
            file "dynamic/local.com.zone";
            allow-update { none; };
            allow-transfer { 192.168.2.3; };
    };
    /* reverse lookup for subnet 192.168.2.0/24 */
    zone "2.168.192.in-addr.arpa" {
            type master;
            file "dynamic/local.com.revzone";
            allow-update { none; };
            allow-transfer { 192.168.2.3; };
    };


Now if you try to do a manual transfer you should see the following:

    [root@rhel2 ~]# dig @192.168.2.2 local.com -t axfr

    ; <<>> DiG 9.3.6-P1-RedHat-9.3.6-4.P1.el5_4.2 <<>> @192.168.2.2 local.com -t axfr
    ; (1 server found)
    ;; global options:  printcmd
    local.com.      86400   IN  SOA rhel1.local.com. root.local.com. 0 86400 3600 604800 10800
    local.com.      86400   IN  NS  rhel1.local.com..
    local.com.      86400   IN  A   192.168.2.2
    google.local.com.   86400   IN  A   192.168.2.4
    rhel1.local.com.    86400   IN  A   192.168.2.2
    rhel2.local.com.    86400   IN  A   192.168.2.3
    local.com.      86400   IN  SOA rhel1.local.com. root.local.com. 0 86400 3600 604800 10800
    ;; Query time: 2 msec
    ;; SERVER: 192.168.2.2#53(192.168.2.2)
    ;; WHEN: Sun Apr 13 15:06:37 2014
    ;; XFR size: 1 records (messages 1)


If you restart the **named** service, you should see both of the zones files on the secondary server:

    [root@rhel2 ~]# ls -l /var/named/slaves/
    total 8
    -rw-r--r-- 1 named named 388 Apr 13 15:06 example.com.revzone
    -rw-r--r-- 1 named named 394 Apr 13 15:08 example.com.zone


On the primary/master server you will see the following in the logs:

    13-Apr-2014 15:15:51.071 xfer-out: info: client 192.168.2.3#42446: transfer of 'local.com/IN': AXFR started
    13-Apr-2014 15:15:51.072 xfer-out: info: client 192.168.2.3#42446: transfer of 'local.com/IN': AXFR ended


and on the secondary/slave you will see the following:

    Apr 13 15:21:09 rhel2 named[3173]: zone 2.168.192.in-addr.arpa/IN: Transfer started.
    Apr 13 15:21:09 rhel2 named[3173]: transfer of '2.168.192.in-addr.arpa/IN' from 192.168.2.2#53: connected using 192.168.2.3#53458
    Apr 13 15:21:09 rhel2 named[3173]: zone 2.168.192.in-addr.arpa/IN: transferred serial 0
    Apr 13 15:21:09 rhel2 named[3173]: transfer of '2.168.192.in-addr.arpa/IN' from 192.168.2.2#53: end of transfer


#### *named* caching only example

From [DNS Configuration Types](http://www.zytrax.com/books/dns/ch4/):

> A DNS Caching Server (frequently called a Resolver) obtains information from another server (a Zone Master) in response to a host query and then saves (caches) the data locally. On a second or subsequent request for the same data the Caching Server (Resolver) will respond with its locally stored data (the cache) until the time-to-live (TTL) value of the response expires, at which time the server will refresh the data from the zone master.
>
> If the caching server (resolver) obtains its data directly from a zone master it will respond as 'authoritative', if the data is supplied from its cache the response is 'non-authoritative'.
>
> The default BIND behaviour is to cache and this is associated with the recursion parameter (the default is '**recursion yes**'). There are many configuration examples which show caching behaviour being defined using a type hint statement in a zone declaration. These configurations confuse two distinct but related functions. If a server is going to provide caching services then it must support recursive queries and recursive queries need access to the root servers which is provided via the 'type hint' statement.
>
> A caching server will typically have a **named.conf** file which includes the following fragment:
>
>     // options section fragment of named.conf
>     // recursion yes is the default and may be omitted
>     options {
>       directory "/var/named";
>       version "not currently available";
>       recursion yes;
>     };
>     // zone section
>     ....
>     // the DOT indicates the root domain = all domains
>     zone "." IN {
>       type hint;
>       file "root.servers";
>     };
>

So a cache-only DNS server is just a named configuration without any zones (except the root hint zone). So the default configuration of **named** is basically a cache-only server by default.

#### Forwarding *named* configuration

From the same site:

> A forwarding (a.k.a. Proxy, Client, Remote) server is one which simply forwards requests to another DNS and caches the results. On its face this looks like a pretty pointless exercise. It is. however, a frequently undervalued and extremely useful configuration in a number of situations:
>
> 1.  Where access to the external network is slow or expensive:
>
>     1.  Local DNS caching - results are cached in the forwarding server so that frequently requested domains will provide fast results from the cache.
>     2.  The Remote (forwarded to) DNS server provides recursive query support - results in a single query across the network (from the forwarding DNS to the forwared to DNS) thus reducing traffic congestion (on busy networks) and increasing performance (on slow networks).
>
> 2.  Forwarding servers also can be used to ease the burden of local administration by providing a single point at which changes to remote name servers may be managed, rather than having to update all hosts. Thus, all hosts in a particular network section or area can be configured to point to a fixed forwarding DNS which can be configured to stream DNS traffic as desired and changed over time with minimal effort.
>
> 3.  Sanitizing traffic. Especially in larger private networks it may be sensible to stream DNS traffic for local domain access by forwarding to the local DNS servers while forwarding external DNS requests to a dirty or hardened caching DNS (or resolver).
>
> BIND allows configuration of forwarding using the forward and forwarders parameters either at a 'global' level (in an options section) or on a per-zone basis in a zone section of the named.conf file. Both configurations are shown in the examples below:
>
> #### Global Forwarding - All Requests
>
>     // options section fragment of named.conf
>     // forwarders can have multiple choices
>     options {
>       directory "/var/named";
>       version "not currently available";
>       forwarders {10.0.0.1; 10.0.0.2;};
>       forward only;
>     };
>     // zone file sections
>     ....
>
>
> #### Per Domain Forwarding
>
>     // zone section fragment of named.conf
>     zone "example.com" IN {
>       type forward;
>       forwarders {10.0.0.1; 10.0.0.2;};
>     };
>

Similar to a caching-only server, but this time you forward the query to a specific server to cache from.

#### *named* forwarding zone example

Here is an easy way to setup named to forward queries to another server. Here is what I added to my **/etc/named.conf** file:

    zone "local.me" {
            type forward;
            forwarders {10.0.0.1;};
    };


Then from the client, I am able to do queries to that DNS server for the **local.me** domain:

    [root@rhel2 ~]# nslookup mac.local.me
    Server:     192.168.2.2
    Address:    192.168.2.2#53

    Non-authoritative answer:
    Name:   mac.local.me
    Address: 192.168.1.109


Notice I don't get an *authoritative* answer, and this is expected since our named server is not the *authoritative* DNS server for that domain.

### Using the *rndc* Utility

From the [Deployment guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> The **rndc** utility is a command line tool that allows you to administer the **named** service, both locally and from a remote machine. Its usage is as follows:
>
>     rndc [option...] command [command-option]
>
>
> To prevent unauthorized access to the service, **named** must be configured to listen on the selected port (that is, **953** by default), and an identical key must be used by both the service and the rndc utility. Configuration files for rndc:
>
> *   **/etc/named.conf** - The default configuration file for the named service.
> *   **/etc/rndc.conf** - The default configuration file for the rndc utility.
> *   **/etc/rndc.key** - The default key location.
>
> The **rndc** configuration is located in **/etc/rndc.conf**. If the file does not exist, the utility will use the key located in **/etc/rndc.key**, which was generated automatically during the installation process using the **rndc-confgen -a** command.
>
> The **named** service is configured using the **controls** statement in the **/etc/named.conf** configuration file. Unless this statement is present, only the connections from the loopback address (that is, 127.0.0.1**strong text**) will be allowed, and the key located in **/etc/rndc.key** will be used.

#### *rndc* commands

From the same guide:

> To check the current status of the named service, use the following command:
>
>     ~]# rndc status
>     version: 9.7.0-P2-RedHat-9.7.0-5.P2.el6
>     CPUs found: 1
>     worker threads: 1
>     number of zones: 16
>     debug level: 0
>     xfers running: 0
>     xfers deferred: 0
>     soa queries in progress: 0
>     query logging is OFF
>     recursive clients: 0/0/1000
>     tcp clients: 0/100
>     server is up and running
>
>
> To reload both the configuration file and zones, type the following at a shell prompt:
>
>     ~]# rndc reload
>     server reload successful
>
>
> This will reload the zones while keeping all previously cached responses, so that you can make changes to the zone files without losing all stored name resolutions. To reload a single zone, specify its name after the reload command, for example:
>
>     ~]# rndc reload localhost
>     zone reload up-to-date
>
>
> Finally, to reload the configuration file and newly added zones only, type:
>
>     ~]# rndc reconfig
>

#### *rndc* example

So let's try this out. If we try to run the command now, we will see the following failure:

    [root@rhel1 ~]# rndc status
    rndc: neither /etc/rndc.conf nor /etc/rndc.key was found


So first let's generate an **rndc** key:

    [root@rhel1 ~]# rndc-confgen -a -r /dev/urandom -c /etc/rndc.key
    wrote key file "/etc/rndc.key"


Next generate the **rndc** configuration file:

    [root@rhel1 ~]# rndc-confgen -r /dev/urandom > /etc/rndc.conf


After that modify the **/etc/rndc.conf** file and copy the contents of **/etc/rndc.key** into the appropriate section. After I was done, I had the following:

    [root@rhel1 ~]# cat /etc/rndc.conf
    # Start of rndc.conf
    key "rndc-key" {
        algorithm hmac-md5;
        secret "TKp2/7Li9dLrB9kEzOIcNw==";
    };

    options {
        default-key "rndc-key";
        default-server 127.0.0.1;
        default-port 953;
    };
    # End of rndc.conf

    # Use with the following in named.conf, adjusting the allow list as needed:
    # key "rndc-key" {
    #   algorithm hmac-md5;
    #   secret "TKp2/7Li9dLrB9kEzOIcNw==";
    # };
    #
    # controls {
    #   inet 127.0.0.1 port 953
    #       allow { 127.0.0.1; } keys { "rndc-key"; };
    # };
    # End of named.conf


Now let's add the **rndc** configuration into the **named** configuration. Here is what I added:

    controls {
          inet 127.0.0.1 port 953
                  allow { 127.0.0.1; } keys { "rndc-key"; };
    };
    include "/etc/rndc.key";


Lastly let's make sure named can read the rndc key:

    [root@rhel1 ~]# chown named:named /etc/rndc.key


Then make sure the configuration is okay:

    [root@rhel1 ~]# named-checkconf
    [root@rhel1 ~]#


If there are no errors, let's restart the **named** service:

    [root@rhel1 ~]# service named restart
    Stopping named:
    Starting named:  named


Then you can check the status of the named service like so:

    [root@rhel1 ~]# rndc status
    WARNING: key file (/etc/rndc.key) exists, but using default configuration file (/etc/rndc.conf)
    version: 9.7.3-RedHat-9.7.3-2.el6
    CPUs found: 1
    worker threads: 1
    number of zones: 21
    debug level: 0
    xfers running: 0
    xfers deferred: 0
    soa queries in progress: 0
    query logging is OFF
    recursive clients: 0/0/1000
    tcp clients: 0/100
    server is up and running


You can then enable *query* logs:

    [root@rhel1 ~]# rndc querylog
    WARNING: key file (/etc/rndc.key) exists, but using default configuration file (/etc/rndc.conf)


and after doing a query against the server you will see the following under **/var/log/messages**

    13-Apr-2014 18:07:40.274 general: info: received control channel command 'querylog'
    13-Apr-2014 18:07:40.274 general: info: query logging is now on
    13-Apr-2014 18:08:02.195 queries: info: client 192.168.2.3#35653: query: local.com IN A + (192.168.2.2)


Here is quick overview of all the available commands for **rndc**:

    [root@rhel1 data]# rndc
    Usage: rndc [-b address] [-c config] [-s server] [-p port]
        [-k key-file ] [-y key] [-V] command

    command is one of the following:

      reload    Reload configuration file and zones.
      reload zone [class [view]]
            Reload a single zone.
      refresh zone [class [view]]
            Schedule immediate maintenance for a zone.
      retransfer zone [class [view]]
            Retransfer a single zone without checking serial number.
      freeze    Suspend updates to all dynamic zones.
      freeze zone [class [view]]
            Suspend updates to a dynamic zone.
      thaw      Enable updates to all dynamic zones and reload them.
      thaw zone [class [view]]
            Enable updates to a frozen dynamic zone and reload it.
      notify zone [class [view]]
            Resend NOTIFY messages for the zone.
      reconfig  Reload configuration file and new zones only.
      sign zone [class [view]]
            Update zone keys, and sign as needed.
      loadkeys zone [class [view]]
            Update keys without signing immediately.
      stats     Write server statistics to the statistics file.
      querylog  Toggle query logging.
      dumpdb [-all|-cache|-zones] [view ...]
            Dump cache(s) to the dump file (named_dump.db).
      secroots [view ...]
            Write security roots to the secroots file.
      stop      Save pending updates to master files and stop the server.
      stop -p   Save pending updates to master files and stop the server
            reporting process id.
      halt      Stop the server without saving pending updates.
      halt -p   Stop the server without saving pending updates reporting
            process id.
      trace     Increment debugging level by one.
      trace level   Change the debugging level.
      notrace   Set debugging level to 0.
      flush     Flushes all of the server's caches.
      flush [view]  Flushes the server's cache for a view.
      flushname name [view]
            Flush the given name from the server's cache(s)
      status    Display status of the server.
      recursing Dump the queries that are currently recursing (named.recursing)
      validation newstate [view]
            Enable / disable DNSSEC validation.
      *restart  Restart the server.
      addzone ["file"] zone [class [view]] { zone-options }
            Add zone to given view. Requires new-zone-file option.
      delzone ["file"] zone [class [view]]
            Removes zone from given view. Requires new-zone-file option.

    * == not yet implemented
    Version: 9.7.3-RedHat-9.7.3-2.el6


#### *named* security

There are a few things you could do to secure the named install. One is to use ACLs, as was discussed above. Another is to limit the **rndc** utility only from trusted machine or even only locally. Lastly you can run the **named** process in a **chroot** jail. From the deployment guide:

> If you have installed the **bind-chroot** package, the BIND service will run in the **/var/named/chroot** environment. In that case, the initialization script will mount the above configuration files using the **mount -bind** command, so that you can manage the configuration outside this environment. There is no need to copy anything into the /var/named/chroot directory because it is mounted automatically. This simplifies maintenance since you do not need to take any special care of BIND configuration files if it is run in a chroot environment. You can organize everything as you would with BIND not running in a chroot environment.
>
> The following directories are automatically mounted into **/var/named/chroot** if they are empty in the **/var/named/chroot** directory. They must be kept empty if you want them to be mounted into **/var/named/chroot**:
>
> *   **/var/named**
> *   **/etc/pki/dnssec-keys**
> *   **/etc/named**
> *   **/usr/lib64/bind** or **/usr/lib/bind** (architecture dependent).
>
> The following files are also mounted if the target file does not exist in **/var/named/chroot**.
>
> *   **/etc/named.conf**
> *   **/etc/rndc.conf**
> *   **/etc/rndc.key**
> *   **/etc/named.rfc1912.zones**
> *   **/etc/named.dnssec.keys**
> *   **/etc/named.iscdlv.key**
> *   **/etc/named.root.key**

