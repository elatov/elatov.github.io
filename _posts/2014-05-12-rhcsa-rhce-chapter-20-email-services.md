---
title: "RHCSA and RHCE Chapter 20 - Email Services"
author: Karim Elatov
layout: post
permalink: "/2014/05/rhcsa-rhce-chapter-20-email-services/"
categories:
  - Certifications
  - Home Lab
  - Networking
  - RHCSA and RHCE
tags:
  - Dovecot
  - Postfix
  - rhcsa_and_rhce
  - SMTP
published: true
---

## Email

From the [Deployment Guide][1]:

> Email was born in the 1960s. The mailbox was a file in a user's home directory that was readable only by that user. Primitive mail applications appended new text messages to the bottom of the file, making the user wade through the constantly growing file to find any particular message. This system was only capable of sending messages to users on the same system.
>
> The first network transfer of an electronic mail message file took place in 1971 when a computer engineer named Ray Tomlinson sent a test message between two machines via ARPANET—the precursor to the Internet. Communication via email soon became very popular, comprising 75 percent of ARPANET's traffic in less than two years.
>
> Today, email systems based on standardized network protocols have evolved into some of the most widely used services on the Internet. Red Hat Enterprise Linux offers many advanced applications to serve and access email. This chapter reviews modern email protocols in use today, and some of the programs designed to send and receive email.

### Email Protocols

From the same guide:

> Today, email is delivered using a client/server architecture. An email message is created using a mail client program. This program then sends the message to a server. The server then forwards the message to the recipient's email server, where the message is then supplied to the recipient's email client.
>
> To enable this process, a variety of standard network protocols allow different machines, often running different operating systems and using different email programs, to send and receive email.

### Mail Transport Protocols

From the above guide:

> Mail delivery from a client application to the server, and from an originating server to the destination server, is handled by the Simple Mail Transfer Protocol (SMTP).

#### SMTP

From the Deployment Guide:

> The primary purpose of SMTP is to transfer email between mail servers. However, it is critical for email clients as well. To send email, the client sends the message to an outgoing mail server, which in turn contacts the destination mail server for delivery. For this reason, it is necessary to specify an SMTP server when configuring an email client.
>
> Under Red Hat Enterprise Linux, a user can configure an SMTP server on the local machine to handle mail delivery. However, it is also possible to configure remote SMTP servers for outgoing mail.
>
> One important point to make about the SMTP protocol is that it does not require authentication. This allows anyone on the Internet to send email to anyone else or even to large groups of people. It is this characteristic of SMTP that makes junk email or spam possible. Imposing relay restrictions limits random users on the Internet from sending email through your SMTP server, to other servers on the internet. Servers that do not impose such restrictions are called open relay servers.
>
> Red Hat Enterprise Linux provides the Postfix and Sendmail SMTP programs.

### Mail Access Protocols

From the same guide:

> There are two primary protocols used by email client applications to retrieve email from mail servers: the Post Office Protocol (POP) and the Internet Message Access Protocol (IMAP).

### POP

Onto POP:

> The default POP server under Red Hat Enterprise Linux is Dovecot and is provided by the **dovecot** package.
>
> When using a **POP** server, email messages are downloaded by email client applications. By default, most **POP** email clients are automatically configured to delete the message on the email server after it has been successfully transferred, however this setting usually can be changed.
>
> **POP** is fully compatible with important Internet messaging standards, such as *Multipurpose Internet Mail Extensions* (MIME), which allow for email attachments. **POP** works best for users who have one system on which to read email. It also works well for users who do not have a persistent connection to the Internet or the network containing the mail server. Unfortunately for those with slow network connections, POP requires client programs upon authentication to download the entire content of each message. This can take a long time if any messages have large attachments.
>
> The most current version of the standard **POP** protocol is **POP3**.
>
> There are, however, a variety of lesser-used POP protocol variants:
>
> *   *APOP* — **POP3** with **MDS** (Monash Directory Service) authentication. An encoded hash of the user's password is sent from the email client to the server rather then sending an unencrypted password.
> *   *KPOP* — **POP3** with Kerberos authentication.
> *   *RPOP* — **POP3** with **RPOP** authentication. This uses a per-user ID, similar to a password, to authenticate POP requests. However, this ID is not encrypted, so RPOP is no more secure than standard POP.
>
> For added security, it is possible to use Secure Socket Layer (SSL) encryption for client authentication and data transfer sessions. This can be enabled by using the **pop3s** service, or by using the **/usr/sbin/stunnel** application.

#### IMAP

And here is IMAP:

> The default **IMAP** server under Red Hat Enterprise Linux is Dovecot and is provided by the dovecot package.
>
> I**M**AP is particularly useful for users who access their email using multiple machines. The protocol is also convenient for users connecting to the mail server via a slow connection, because only the email header information is downloaded for messages until opened, saving bandwidth. The user also has the ability to delete messages without viewing or downloading them.
>
> For convenience, **IMAP** client applications are capable of caching copies of messages locally, so the user can browse previously read messages when not directly connected to the IMAP server.
>
> **IMAP**, like **POP**, is fully compatible with important Internet messaging standards, such as **MIME**, which allow for email attachments.
>
> For added security, it is possible to use **SSL** encryption for client authentication and data transfer sessions. This can be enabled by using the **imaps** service, or by using the **/usr/sbin/stunnel** program.

## Email Program Classifications

From the Deployment Guide:

> In general, all email applications fall into at least one of three classifications. Each classification plays a specific role in the process of moving and managing email messages. While most users are only aware of the specific email program they use to receive and send messages, each one is important for ensuring that email arrives at the correct destination.

### Mail Transport Agent

From the same guide:

> A Mail Transport Agent (**MTA**) transports email messages between hosts using **SMTP**. A message may involve several MTAs as it moves to its intended destination. While the delivery of messages between machines may seem rather straightforward, the entire process of deciding if a particular MTA can or should accept a message for delivery is quite complicated. In addition, due to problems from spam, use of a particular MTA is usually restricted by the MTA's configuration or the access configuration for the network on which the MTA resides.
>
> Many modern email client programs can act as an MTA when sending email. However, this action should not be confused with the role of a true MTA. The sole reason email client programs are capable of sending email like an MTA is because the host running the application does not have its own MTA. This is particularly true for email client programs on non-UNIX-based operating systems. However, these client programs only send outbound messages to an MTA they are authorized to use and do not directly deliver the message to the intended recipient's email server.
>
> Since Red Hat Enterprise Linux offers two MTAs—**Postfix** and **Sendmail**—email client programs are often not required to act as an MTA. Red Hat Enterprise Linux also includes a special purpose MTA called **Fetchmail**.

### Mail Delivery Agent

From the above guide:

> A Mail Delivery Agent (**MDA**) is invoked by the MTA to file incoming email in the proper user's mailbox. In many cases, the MDA is actually a Local Delivery Agent (**LDA**), such as **mail** or **Procmail**.
>
> Any program that actually handles a message for delivery to the point where it can be read by an email client application can be considered an MDA. For this reason, some MTAs (such as **Sendmail** and **Postfix**) can fill the role of an MDA when they append new email messages to a local user's mail spool file. In general, MDAs do not transport messages between systems nor do they provide a user interface; MDAs distribute and sort messages on the local machine for an email client application to access.

### Mail User Agent

From the Deployment Guide.

> A Mail User Agent (**MUA**) is synonymous with an email client application. An MUA is a program that, at the very least, allows a user to read and compose email messages. Many MUAs are capable of retrieving messages via the POP or IMAP protocols, setting up mailboxes to store messages, and sending outbound messages to an MTA.
>
> MUAs may be graphical, such as **Evolution**, or have simple text-based interfaces, such as **pine**.

### Mail Transport Agents

From the same guide:

> Red Hat Enterprise Linux offers two primary MTAs: **Postfix** and **Sendmail**. **Postfix** is configured as the default **MTA**, although it is easy to switch the default MTA to Sendmail. To switch the default MTA to Sendmail, you can either uninstall Postfix or use the following command to switch to Sendmail:
>
>     ~]# alternatives --config mta
>
>
> You can also use the following command to enable/disable the desired service:
>
>     ~]# chkconfig <service> <on/off>
>

### Postfix

From the Deployment Guide:

> Originally developed at IBM by security expert and programmer Wietse Venema, **Postfix** is a **Sendmail**-compatible MTA that is designed to be secure, fast, and easy to configure.
>
> To improve security, **Postfix** uses a modular design, where small processes with limited privileges are launched by a master daemon. The smaller, less privileged processes perform very specific tasks related to the various stages of mail delivery and run in a changed root environment to limit the effects of attacks.
>
> Configuring **Postfix** to accept network connections from hosts other than the local computer takes only a few minor changes in its configuration file. Yet for those with more complex needs, Postfix provides a variety of configuration options, as well as third party add-ons that make it a very versatile and full-featured MTA.
>
> The configuration files for **Postfix** are human readable and support upward of 250 directives. Unlike **Sendmail**, no macro processing is required for changes to take effect and the majority of the most commonly used options are described in the heavily commented files.

#### The Default Postfix Installation

From the same guide:

> The Postfix executable is **/usr/sbin/postfix**. This daemon launches all related processes needed to handle mail delivery.
>
> Postfix stores its configuration files in the **/etc/postfix/** directory. The following is a list of the more commonly used files:
>
> *   **access** - Used for access control, this file specifies which hosts are allowed to connect to Postfix.
> *   **main.cf** - The global Postfix configuration file. The majority of configuration options are specified in this file.
> *   **master.cf** - Specifies how Postfix interacts with various processes to accomplish mail delivery.
> *   **transport** - Maps email addresses to relay hosts.
>
> The **aliases** file can be found in the **/etc/** directory. This file is shared between **Postfix** and **Sendmail**. It is a configurable list required by the mail protocol that describes user ID aliases.
>
> Restart the postfix service after changing any options in the configuration files under the **/etc/postfix** directory in order for those changes to take effect:
>
>     ~]# service postfix restart
>

#### Basic Postfix Configuration

From the Deployment Guide:

> By default, **Postfix** does not accept network connections from any host other than the local host. Perform the following steps as root to enable mail delivery for other hosts on the network:
>
> *   Edit the **/etc/postfix/main.cf** file with a text editor, such as **vi**.
> *   Uncomment the **mydomain** line by removing the hash sign (**#**), and replace **domain.tld** with the domain the mail server is servicing, such as **example.com**.
> *   Uncomment the **myorigin = $mydomain** line.
> *   Uncomment the **myhostname** line, and replace **host.domain.tld** with the **hostname** for the machine.
> *   Uncomment the **mydestination = $myhostname**, **localhost.$mydomain** line.
> *   Uncomment the **mynetworks** line, and replace **168\.100.189.0/28** with a valid network setting for hosts that can connect to the server.
> *   Uncomment the **inet_interfaces = all** line.
> *   Comment the **inet_interfaces = localhost** line.
> *   Restart the postfix service.
>
> Once these steps are complete, the host accepts outside emails for delivery. Postfix has a large assortment of configuration options. One of the best ways to learn how to configure Postfix is to read the comments within the **/etc/postfix/main.cf** configuration file.

#### Postfix Example

So let's go ahead and try this out.Since postfix is the default MTA on RH6, let's confirm it's installed, set as the default MTA, and running:

    [root@rhel1 ~]# rpm -qa | grep postf
    postfix-2.6.6-2.1.el6_0.i686
    [root@rhel1 ~]# alternatives --display mta | grep current
     link currently points to /usr/sbin/sendmail.postfix
    [root@rhel1 ~]# service postfix status
    master (pid  2254) is running...


Here is the default configuration:

    [root@rhel1 ~]# grep -Ev '^$|^#' /etc/postfix/main.cf
    queue_directory = /var/spool/postfix
    command_directory = /usr/sbin
    daemon_directory = /usr/libexec/postfix
    data_directory = /var/lib/postfix
    mail_owner = postfix
    inet_interfaces = localhost
    inet_protocols = all
    mydestination = $myhostname, localhost.$mydomain, localhost
    unknown_local_recipient_reject_code = 550
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases


    debug_peer_level = 2
    debugger_command =
         PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
         ddd $daemon_directory/$process_name $process_id & sleep 5
    sendmail_path = /usr/sbin/sendmail.postfix
    newaliases_path = /usr/bin/newaliases.postfix
    mailq_path = /usr/bin/mailq.postfix
    setgid_group = postdrop
    html_directory = no
    manpage_directory = /usr/share/man
    sample_directory = /usr/share/doc/postfix-2.6.6/samples
    readme_directory = /usr/share/doc/postfix-2.6.6/README_FILES


Looks like be default local delivery should be working, so let's install an MUA (mail) which in some cases can also act as a MDA/LDA (Mail/Local Delivery Agent):

    [root@rhel1 ~]# yum install mailx


Now from the **root** user let's send an email to **user1**:

    [root@rhel1 ~]# mail -s testing user1
    this is a test email
    .
    EOT


Now let's switch user to **user1**, and see if the email is there:

    [root@rhel1 ~]# su - user1
    [user1@rhel1 ~]$ mail
    Heirloom Mail version 12.4 7/29/08.  Type ? for help.
    "/var/spool/mail/user1": 1 message 1 new
    >N  1 root                  Sat Apr 26 11:25  18/566   "testing"
    & p
    Message  1:
    From root@rhel1.local.com  Sat Apr 26 11:25:59 2014
    Return-Path: <root@rhel1.local.com>
    X-Original-To: user1
    Delivered-To: user1@rhel1.local.com
    Date: Sat, 26 Apr 2014 11:25:59 -0600
    To: user1@rhel1.local.com
    Subject: testing
    User-Agent: Heirloom mailx 12.4 7/29/08
    Content-Type: text/plain; charset=us-ascii
    From: root@rhel1.local.com (root)
    Status: R

    this is a test email

    & d
    & h
    No applicable messages
    & q


So (as user1) I checked my mail queue, read the message, and then deleted the message. Now let's try a remote delivery. First let's configure an **MX** record for our domain, so we know which server handles our mail delivery. I added the following to my zone file:

    [root@rhel1 ~]# grep MX /var/named/local.com.zone
    @   IN  MX  10  rhel1.local.com.


I then restarted **named**:

    [root@rhel1 ~]# service named restart
    Stopping named: .
    Starting named:  named


then from the RH5, machine I was able to get the correct response back:

    [root@rhel2 ~]# dig MX local.com

    ; <<>> DiG 9.3.6-P1-RedHat-9.3.6-4.P1.el5_4.2 <<>> MX local.com
    ;; global options:  printcmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7120
    ;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 2

    ;; QUESTION SECTION:
    ;local.com.         IN  MX

    ;; ANSWER SECTION:
    local.com.      86400   IN  MX  10 rhel1.local.com.


Now let's modify the postfix configuration to allow for remote mail. Here is how my **main.cf** file looked like after the changes:

    [root@rhel1 ~]# grep -Ev '^$|^#' /etc/postfix/main.cf
    queue_directory = /var/spool/postfix
    command_directory = /usr/sbin
    daemon_directory = /usr/libexec/postfix
    data_directory = /var/lib/postfix
    mail_owner = postfix
    myhostname = rhel1.local.com
    mydomain = local.com
    inet_interfaces = 192.168.2.2
    inet_protocols = all
    mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
    unknown_local_recipient_reject_code = 550
    mynetworks = 192.168.2.0/24, 127.0.0.0/8
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases


    debug_peer_level = 2
    debugger_command =
         PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
         ddd $daemon_directory/$process_name $process_id & sleep 5
    sendmail_path = /usr/sbin/sendmail.postfix
    newaliases_path = /usr/bin/newaliases.postfix
    mailq_path = /usr/bin/mailq.postfix
    setgid_group = postdrop
    html_directory = no
    manpage_directory = /usr/share/man
    sample_directory = /usr/share/doc/postfix-2.6.6/samples
    readme_directory = /usr/share/doc/postfix-2.6.6/README_FILES


We can also use the **postconf** to list all the configured variables:

    [root@rhel1 ~]# postconf -n
    alias_database = hash:/etc/aliases
    alias_maps = hash:/etc/aliases
    command_directory = /usr/sbin
    config_directory = /etc/postfix
    daemon_directory = /usr/libexec/postfix
    data_directory = /var/lib/postfix
    debug_peer_level = 2
    html_directory = no
    inet_interfaces = 192.168.2.2
    inet_protocols = all
    mail_owner = postfix
    mailq_path = /usr/bin/mailq.postfix
    manpage_directory = /usr/share/man
    mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
    mydomain = local.com
    myhostname = rhel1.local.com
    mynetworks = 192.168.2.0/24, 127.0.0.0/8
    newaliases_path = /usr/bin/newaliases.postfix
    queue_directory = /var/spool/postfix
    readme_directory = /usr/share/doc/postfix-2.6.6/README_FILES
    sample_directory = /usr/share/doc/postfix-2.6.6/samples
    sendmail_path = /usr/sbin/sendmail.postfix
    setgid_group = postdrop
    unknown_local_recipient_reject_code = 550


Now let's check to make sure the configuration is okay:

    [root@rhel1 ~]# postfix check
    [root@rhel1 ~]#


Lastly let's restart the service:

    [root@rhel1 ~]# service postfix restart
    Shutting down postfix:
    Starting postfix:


Now let's open up the firewall:

    [root@rhel1 ~]# iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 25 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now from the RH5 client, let's send an email from *user2* to *user1* to the remote machine:

    [user2@rhel2 ~]$ mail -s "remote test" user1@local.com
    testing
    .
    Cc:


Then on the mail server, check to see if that user has the mail:

    [user1@rhel1 ~]$ mail
    Heirloom Mail version 12.4 7/29/08.  Type ? for help.
    "/var/spool/mail/user1": 1 message 1 new
    >N  1 user2@rhel2.local.co  Sat Apr 26 12:11  21/872   "remote test"
    & p
    Message  1:
    From user2@rhel2.local.com  Sat Apr 26 12:11:46 2014
    Return-Path: <user2@rhel2.local.com>
    X-Original-To: user1@local.com
    Delivered-To: user1@local.com
    Date: Sat, 26 Apr 2014 12:11:46 -0600
    From: user2@rhel2.local.com
    To: user1@local.com
    Subject: remote test
    Status: R

    testing

    & d
    & q


On the RH5, machine we will see the following in the **maillog** file:

    [root@rhel2 ~]# tail /var/log/maillog
    Apr 26 12:11:46 rhel2 sendmail[15891]: s3QIBkVm015891: to=user1@local.com, ctladdr=user2 (501/501), delay=00:00:00, xdelay=00:00:00, mailer=relay, pri=30056, relay=[127.0.0.1] [127.0.0.1], dsn=2.0.0, stat=Sent (s3QIBk6H015892 Message accepted for delivery)
    Apr 26 12:11:46 rhel2 sendmail[15894]: s3QIBk6H015892: to=<user1@local.com>, delay=00:00:00, xdelay=00:00:00, mailer=esmtp, pri=120334, relay=rhel1.local.com. [192.168.2.2], dsn=2.0.0, stat=Sent (Ok: queued as 2471D40E5E)


So basically the local MTA (sendmail, the default on RH5) accepted the message and then forwarded/relayed it to the RH6 machine, which is the destination Email Server. Then on the postfix RH6 machine, I saw the following:

    Apr 26 12:11:46 rhel1 postfix/smtpd[15538]: connect from rhel2.local.com[192.168.2.3]
    Apr 26 12:11:46 rhel1 postfix/smtpd[15538]: 2471D40E5E: client=rhel2.local.com[192.168.2.3]
    Apr 26 12:11:46 rhel1 postfix/cleanup[15541]: 2471D40E5E: message-id=<201404261811.s3QIBkVm015891@rhel2.local.com>
    Apr 26 12:11:46 rhel1 postfix/qmgr[15219]: 2471D40E5E: from=<user2@rhel2.local.com>, size=724, nrcpt=1 (queue active)
    Apr 26 12:11:46 rhel1 postfix/smtpd[15538]: disconnect from rhel2.local.com[192.168.2.3]
    Apr 26 12:11:46 rhel1 postfix/local[15552]: 2471D40E5E: to=<user1@local.com>, relay=local, delay=0.06, delays=0.05/0.01/0/0, dsn=2.0.0, status=sent (delivered to mailbox)
    Apr 26 12:11:46 rhel1 postfix/qmgr[15219]: 2471D40E5E: removed


We can also do a direct connection to the postfix server and send a message with **telnet**:

    [user2@rhel2 ~]$ telnet rhel1 25
    Trying 192.168.2.2...
    Connected to rhel1.local.com (192.168.2.2).
    Escape character is '^]'.
    220 rhel1.local.com ESMTP Postfix
    ehlo local.com
    250-rhel1.local.com
    250-PIPELINING
    250-SIZE 10240000
    250-VRFY
    250-ETRN
    250-ENHANCEDSTATUSCODES
    250-8BITMIME
    250 DSN
    HELO rhel1.local.com
    250 rhel1.local.com
    MAIL FROM: user2@rhel2.local.com
    250 2.1.0 Ok
    RCPT TO: user1@rhel1.local.com
    250 2.1.5 Ok
    DATA
    354 End data with <CR><LF>.<CR><LF>
    Subject: Manual Test
    My Message
    .
    250 2.0.0 Ok: queued as 7B5D140D58
    ^]


Then on the RH6 machine (as user1) we can check the mail:

    [user1@rhel1 ~]$ mail
    Heirloom Mail version 12.4 7/29/08.  Type ? for help.
    "/var/spool/mail/user1": 1 message 1 new
    >N  1 user2@rhel2.local.co  Sat Apr 26 12:21  11/381   "Manual Test"
    & p
    Message  1:
    From user2@rhel2.local.com  Sat Apr 26 12:21:01 2014
    Return-Path: <user2@rhel2.local.com>
    X-Original-To: user1@rhel1.local.com
    Delivered-To: user1@rhel1.local.com
    Subject: Manual Test
    Status: R

    My Message

    & d
    & q


If the mail queue gets stuck you can run the following to check the status:

    [root@rhel1 ~]# mailq
    -Queue ID- --Size-- ----Arrival Time---- -Sender/Recipient-------
    9330D40E5F     2499 Sat Apr 26 12:10:50  MAILER-DAEMON
                    (connect to rhel2.local.com[192.168.2.3]:25: No route to host)
                                             user2@rhel2.local.com

    E802C40E60     2491 Sat Apr 26 15:17:53  MAILER-DAEMON
                    (connect to rhel2.local.com[192.168.2.3]:25: No route to host)
                                             root@rhel2.local.com

    BFF9D40E5C     2495 Sat Apr 26 15:15:44  MAILER-DAEMON
                    (connect to rhel2.local.com[192.168.2.3]:25: No route to host)
                                             root@rhel2.local.com

    -- 7 Kbytes in 3 Requests.


If those are unwanted messages, just run the following to clean up the queue:

    [root@rhel1 ~]# postsuper -d ALL
    postsuper: Deleted: 3 messages
    [root@rhel1 ~]# mailq
    Mail queue is empty


### Dovecot

From the Deployment Guide:

> The **imap-login** and **pop3-login** processes which implement the **IMAP** and **POP3** protocols are spawned by the master dovecot daemon included in the dovecot package. The use of **IMAP** and **POP** is configured through the **/etc/dovecot/dovecot.conf** configuration file; by default dovecot runs **IMAP** and **POP3** together with their secure versions using SSL. To configure dovecot to use **POP**, complete the following steps:
>
> 1.  Edit the **/etc/dovecot/dovecot.conf** configuration file to make sure the **protocols** variable is uncommented (remove the hash sign (**#**) at the beginning of the line) and contains the **pop3** argument. For example:
>
>          protocols = imap imaps pop3 pop3s
>
>
>     When the protocols variable is left commented out, dovecot will use the default values specified for this variable.
>
> 2.  Make that change operational for the current session by running the following command:
>
>         ~]# service dovecot restart
>
>
> 3.  Make that change operational after the next reboot by running the command:
>
>         ~]# chkconfig dovecot on
>
>
> Unlike SMTP, both IMAP and POP3 require connecting clients to authenticate using a username and password. By default, passwords for both protocols are passed over the network unencrypted.
>
> To configure **SSL** on dovecot:
>
> *   Edit the **/etc/pki/dovecot/dovecot-openssl.conf** configuration file as you prefer. However, in a typical installation, this file does not require modification.
> *   Rename, move or delete the files **/etc/pki/dovecot/certs/dovecot.pem** and **/etc/pki/dovecot/private/dovecot.pem**.
> *   Execute the **/usr/libexec/dovecot/mkcert.sh** script which creates the dovecot self signed certificates. These certificates are copied in the **/etc/pki/dovecot/certs** and **/etc/pki/dovecot/private** directories. To implement the changes, restart dovecot: ~]# service dovecot restart

### Dovecot Example

So let's try setting up an IMAP and IMAPS mail server. First let's install dovecot:

    [root@rhel1 ~]# yum install dovecot


Here is the default configuration:

    [root@rhel1 ~]# grep -vE '^$|^ #|^#' /etc/dovecot/dovecot.conf
    dict {
      #quota = mysql:/etc/dovecot/dovecot-dict-sql.conf.ext
      #expire = sqlite:/etc/dovecot/dovecot-dict-sql.conf.ext
    }
    !include conf.d/*.conf


Most of the configurations are under **/etc/dovecot/conf.d**. Here all the configurations:

    [root@rhel1 ~]# grep -vE '^$|^#|^  #' /etc/dovecot/conf.d/*.conf
    /etc/dovecot/conf.d/10-auth.conf:auth_mechanisms = plain
    /etc/dovecot/conf.d/10-auth.conf:!include auth-system.conf.ext
    /etc/dovecot/conf.d/10-director.conf:service director {
    /etc/dovecot/conf.d/10-director.conf:  unix_listener login/director {
    /etc/dovecot/conf.d/10-director.conf:    #mode = 0666
    /etc/dovecot/conf.d/10-director.conf:  }
    /etc/dovecot/conf.d/10-director.conf:  fifo_listener login/proxy-notify {
    /etc/dovecot/conf.d/10-director.conf:    #mode = 0666
    /etc/dovecot/conf.d/10-director.conf:  }
    /etc/dovecot/conf.d/10-director.conf:  unix_listener director-userdb {
    /etc/dovecot/conf.d/10-director.conf:    #mode = 0600
    /etc/dovecot/conf.d/10-director.conf:  }
    /etc/dovecot/conf.d/10-director.conf:  inet_listener {
    /etc/dovecot/conf.d/10-director.conf:    #port =
    /etc/dovecot/conf.d/10-director.conf:  }
    /etc/dovecot/conf.d/10-director.conf:}
    /etc/dovecot/conf.d/10-director.conf:service imap-login {
    /etc/dovecot/conf.d/10-director.conf:}
    /etc/dovecot/conf.d/10-director.conf:service pop3-login {
    /etc/dovecot/conf.d/10-director.conf:}
    /etc/dovecot/conf.d/10-director.conf:protocol lmtp {
    /etc/dovecot/conf.d/10-director.conf:}
    /etc/dovecot/conf.d/10-logging.conf:plugin {
    /etc/dovecot/conf.d/10-logging.conf:}
    /etc/dovecot/conf.d/10-logging.conf:
    /etc/dovecot/conf.d/10-mail.conf:mbox_write_locks = fcntl
    /etc/dovecot/conf.d/10-master.conf:service imap-login {
    /etc/dovecot/conf.d/10-master.conf:  inet_listener imap {
    /etc/dovecot/conf.d/10-master.conf:    #port = 143
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:  inet_listener imaps {
    /etc/dovecot/conf.d/10-master.conf:    #port = 993
    /etc/dovecot/conf.d/10-master.conf:    #ssl = yes
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service pop3-login {
    /etc/dovecot/conf.d/10-master.conf:  inet_listener pop3 {
    /etc/dovecot/conf.d/10-master.conf:    #port = 110
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:  inet_listener pop3s {
    /etc/dovecot/conf.d/10-master.conf:    #port = 995
    /etc/dovecot/conf.d/10-master.conf:    #ssl = yes
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service lmtp {
    /etc/dovecot/conf.d/10-master.conf:  unix_listener lmtp {
    /etc/dovecot/conf.d/10-master.conf:    #mode = 0666
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:    # Avoid making LMTP visible for the entire internet
    /etc/dovecot/conf.d/10-master.conf:    #address =
    /etc/dovecot/conf.d/10-master.conf:    #port =
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service imap {
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service pop3 {
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service auth {
    /etc/dovecot/conf.d/10-master.conf:  unix_listener auth-userdb {
    /etc/dovecot/conf.d/10-master.conf:    #mode = 0600
    /etc/dovecot/conf.d/10-master.conf:    #user =
    /etc/dovecot/conf.d/10-master.conf:    #group =
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service auth-worker {
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-master.conf:service dict {
    /etc/dovecot/conf.d/10-master.conf:  unix_listener dict {
    /etc/dovecot/conf.d/10-master.conf:    #mode = 0600
    /etc/dovecot/conf.d/10-master.conf:    #user =
    /etc/dovecot/conf.d/10-master.conf:    #group =
    /etc/dovecot/conf.d/10-master.conf:  }
    /etc/dovecot/conf.d/10-master.conf:}
    /etc/dovecot/conf.d/10-ssl.conf:ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    /etc/dovecot/conf.d/10-ssl.conf:ssl_key = </etc/pki/dovecot/private/dovecot.pem
    /etc/dovecot/conf.d/15-lda.conf:protocol lda {
    /etc/dovecot/conf.d/15-lda.conf:}
    /etc/dovecot/conf.d/20-imap.conf:protocol imap {
    /etc/dovecot/conf.d/20-imap.conf:}
    /etc/dovecot/conf.d/20-lmtp.conf:protocol lmtp {
    /etc/dovecot/conf.d/20-lmtp.conf:}
    /etc/dovecot/conf.d/20-pop3.conf:protocol pop3 {
    /etc/dovecot/conf.d/20-pop3.conf:}
    /etc/dovecot/conf.d/90-acl.conf:plugin {
    /etc/dovecot/conf.d/90-acl.conf:}
    /etc/dovecot/conf.d/90-acl.conf:plugin {
    /etc/dovecot/conf.d/90-acl.conf:}
    /etc/dovecot/conf.d/90-plugin.conf:plugin {
    /etc/dovecot/conf.d/90-plugin.conf:}
    /etc/dovecot/conf.d/90-quota.conf:plugin {
    /etc/dovecot/conf.d/90-quota.conf:}
    /etc/dovecot/conf.d/90-quota.conf:plugin {
    /etc/dovecot/conf.d/90-quota.conf:}
    /etc/dovecot/conf.d/90-quota.conf:plugin {
    /etc/dovecot/conf.d/90-quota.conf:}
    /etc/dovecot/conf.d/90-quota.conf:plugin {
    /etc/dovecot/conf.d/90-quota.conf:}


Nothing crazy, we can see that the authentication is set as plain. We could use a user database for authentication, but it doesn't look like we are using it. Then there are protocol specific stuff (imap and pop3). So under the main configuration let's enable IMAP and IMAPS. Here is the configuration after I was done:

    [root@rhel1 ~]# grep -vE '^$|^ #|^#' /etc/dovecot/dovecot.conf
    protocols = imap
    listen = 192.168.2.2
    dict {
      #quota = mysql:/etc/dovecot/dovecot-dict-sql.conf.ext
      #expire = sqlite:/etc/dovecot/dovecot-dict-sql.conf.ext
    }
    !include conf.d/*.conf


I also edited the **/etc/dovecot/conf.d/10-mail.conf** and specified the mail location:

    [root@rhel1 ~]# grep -vE '^$|^  #|^#' /etc/dovecot/conf.d/10-mail.conf
      mail_location = mbox:~/mail:INBOX=/var/mail/%u
    mbox_write_locks = fcntl


As a test, I disabled SSL just to get plain IMAP working first:

    [root@rhel1 dovecot]# grep -vE '^$|^  #|^#' /etc/dovecot/conf.d/10-ssl.conf
    ssl = no
    ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    ssl_key = </etc/pki/dovecot/private/dovecot.pem


Lastly I had to allow plain text authentication (we will disable this later):

    [root@rhel1 ~]# grep -vE '^$|^  #|^#' /etc/dovecot/conf.d/10-auth.conf
    disable_plaintext_auth = no
    auth_mechanisms = plain
    !include auth-system.conf.ext


You can get a summary of the enabled configuration by using doveconf:

    [root@rhel1 ~]# doveconf -n
    # 2.0.9: /etc/dovecot/dovecot.conf
    # OS: Linux 2.6.32-131.0.15.el6.i686 i686 Red Hat Enterprise Linux Workstation release 6.1 (Santiago)
    disable_plaintext_auth = no
    listen = 192.168.2.2
    mail_location = mbox:~/mail:INBOX=/var/mail/%u
    mbox_write_locks = fcntl
    passdb {
      driver = pam
    }
    protocols = imap
    ssl = no
    ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    ssl_key = </etc/pki/dovecot/private/dovecot.pem
    userdb {
      driver = passwd
    }


Now let's start it up:

    [root@rhel1 ~]# service dovecot start
    Starting Dovecot Imap:  dovecot
    [root@rhel1 ~]# service dovecot status
    dovecot (pid  16201) is running...


In the log we will see the following:

    [root@rhel1 ~]# tail -1 /var/log/maillog
    Apr 26 16:13:54 rhel1 dovecot: master: Dovecot v2.0.9 starting up (core dumps disabled)


Now let's open up the IMAP port on the firewall:

    [root@rhel1 ~]# iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 143 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now on RH5 machine, run the following to check the email:

    [root@rhel2 ~]# mutt -f imap://user1@rhel1


When I connected the first time, I saw the following error on the dovecot server:

    Apr 26 16:35:49 rhel1 dovecot: imap-login: Login: user=<user1>, method=PLAIN, rip=192.168.2.3, lip=192.168.2.2, mpid=16411
    Apr 26 16:35:49 rhel1 dovecot: imap(user1): Error: chown(/home/user1/mail/.imap/INBOX, -1, 12(mail)) failed: Operation not permitted (egid=500(user1), group based on /var/mail/user1)
    Apr 26 16:35:49 rhel1 dovecot: imap(user1): Error: mkdir(/home/user1/mail/.imap/INBOX) failed: Operation not permitted
    Apr 26 16:35:51 rhel1 dovecot: imap(user1): Connection closed bytes=40/454


Had to set the following in the **/etc/dovecot/10-mail.conf**:

    mail_access_groups = mail


After that, mutt showed me the following:

![mutt-connected-to-imap][2]

Here is the connection to IMAP with telnet:

    [root@rhel2 ~]# telnet rhel1 143
    Trying 192.168.2.2...
    Connected to rhel1.local.com (192.168.2.2).
    Escape character is '^]'.
    * OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN] Dovecot ready.
    01 LOGIN user1 password
    01 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS MULTIAPPEND UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS] Logged in
    02 LIST "" "*"
    * LIST (\NoInferiors \UnMarked) "/" "INBOX"
    02 OK List completed.
    03 EXAMINE INBOX
    * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
    * OK [PERMANENTFLAGS ()] Read-only mailbox.
    * 2 EXISTS
    * 0 RECENT
    * OK [UNSEEN 1] First unseen.
    * OK [UIDVALIDITY 1398552193] UIDs valid
    * OK [UIDNEXT 3] Predicted next UID
    * OK [HIGHESTMODSEQ 1] Highest
    03 OK [READ-ONLY] Select completed.
    04 FETCH 1 BODY[]
    * 1 FETCH (BODY[] {803}
    Return-Path: <root@rhel2.local.com>
    X-Original-To: user1@local.com
    Delivered-To: user1@local.com
    Received: from rhel2.local.com (rhel2.local.com [192.168.2.3])
        by rhel1.local.com (Postfix) with ESMTP id AEB6840933
        for <user1@local.com>; Sat, 26 Apr 2014 15:29:40 -0600 (MDT)
    Received: from rhel2.local.com (localhost.localdomain [127.0.0.1])
        by rhel2.local.com (8.13.8/8.13.8) with ESMTP id s3QLTem2017283
        for <user1@local.com>; Sat, 26 Apr 2014 15:29:40 -0600
    Received: (from root@localhost)
        by rhel2.local.com (8.13.8/8.13.8/Submit) id s3QLTebH017282
        for user1@local.com; Sat, 26 Apr 2014 15:29:40 -0600
    Date: Sat, 26 Apr 2014 15:29:40 -0600
    From: root <root@rhel2.local.com>
    Message-Id: <201404262129.s3QLTebH017282@rhel2.local.com>
    To: user1@local.com
    Subject: testing

    sdflksdfj
    )
    04 OK Fetch completed.
    05 LOGOUT
    * BYE Logging out
    05 OK Logout completed.
    Connection closed by foreign host.


On the IMAP server, we will see the cache for dovecot:

    [root@rhel1 ~]# ls ~user1/mail/.imap/INBOX/
    dovecot.index.cache  dovecot.index.log


### Dovecot SSL Example

Now let's enable SSL for IMAP. First let's create the Self Signed SSl certificate. This is done by editing the **/etc/pki/dovecot/dovecot-openssl.cnf** file and fill in all the information about your organization. Here was the default file from the install:

    [root@rhel1 ~]# cat /etc/pki/dovecot/dovecot-openssl.cnf
    [ req ]
    default_bits = 1024
    encrypt_key = yes
    distinguished_name = req_dn
    x509_extensions = cert_type
    prompt = no

    [ req_dn ]
    # country (2 letter code)
    #C=FI

    # State or Province Name (full name)
    #ST=

    # Locality Name (eg. city)
    #L=Helsinki

    # Organization (eg. company)
    #O=Dovecot

    # Organizational Unit Name (eg. section)
    OU=IMAP server

    # Common Name (*.example.com is also possible)
    CN=imap.example.com

    # E-mail contact
    emailAddress=postmaster@example.com

    [ cert_type ]
    nsCertType = server


Here is all the information that I changed:

    [root@rhel1 ~]# cat /etc/pki/dovecot/dovecot-openssl.cnf
    [ req ]
    default_bits = 1024
    encrypt_key = yes
    distinguished_name = req_dn
    x509_extensions = cert_type
    prompt = no

    [ req_dn ]
    # country (2 letter code)
    C=US

    # State or Province Name (full name)
    ST=Colorado

    # Locality Name (eg. city)
    L=Boulder

    # Organization (eg. company)
    O=HOME

    # Organizational Unit Name (eg. section)
    OU=RHEL_LAB

    # Common Name (*.example.com is also possible)
    CN=rhel1.local.com

    # E-mail contact
    emailAddress=postmaster@local.com

    [ cert_type ]
    nsCertType = server


Now let's backup the original certificate files:

    [root@rhel1 ~]# mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.orig
    [root@rhel1 ~]# mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.orig


Finally let's create the certificate:

    [root@rhel1 ~]# /usr/libexec/dovecot/mkcert.sh
    Generating a 1024 bit RSA private key
    ...++++++
    ......++++++
    writing new private key to '/etc/pki/dovecot/private/dovecot.pem'
    -----

    subject= /C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    SHA1 Fingerprint=57:E9:21:84:13:21:31:D2:1B:97:DB:38:00:62:8E:83:55:6B:89:5C


Now let's enable SSL:

    [root@rhel1 ~]# grep -vE '^$|^  #|^#' /etc/dovecot/conf.d/10-ssl.conf
    ssl = yes
    ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    ssl_key = </etc/pki/dovecot/private/dovecot.pem


let's also disable the plain authenticate without SSL:

    [root@rhel1 ~]# grep -vE '^$|^  #|^#' /etc/dovecot/conf.d/10-auth.conf
    disable_plaintext_auth = yes
    auth_mechanisms = plain
    !include auth-system.conf.ext


Here are the non-default configurations:

    [root@rhel1 ~]# doveconf -n
    # 2.0.9: /etc/dovecot/dovecot.conf
    # OS: Linux 2.6.32-131.0.15.el6.i686 i686 Red Hat Enterprise Linux Workstation release 6.1 (Santiago)
    listen = 192.168.2.2
    mail_access_groups = mail
    mail_location = mbox:~/mail:INBOX=/var/mail/%u
    mbox_write_locks = fcntl
    passdb {
      driver = pam
    }
    protocols = imap
    ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    ssl_key = </etc/pki/dovecot/private/dovecot.pem
    userdb {
      driver = passwd
    }


Notice the SSL stuff (other than the certificates) is not here. This is because SSL is enabled by default. **dovecot -a** shows all the configurations, but it's too much information. Here is the related information to SSL:

    [root@rhel1 ~]# doveconf -a | grep -i SSL
    auth_ssl_require_client_cert = no
    auth_ssl_username_from_cert = no
        ssl = no
        ssl = no
        ssl = yes
        ssl = no
        ssl = yes
    service ssl-params {
      executable = ssl-params
      unix_listener login/ssl-params {
    ssl = yes
    ssl_ca =
    ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
    ssl_cert_username_field = commonName
    ssl_cipher_list = ALL:!LOW:!SSLv2:!EXP:!aNULL
    ssl_key = </etc/pki/dovecot/private/dovecot.pem
    ssl_key_password =
    ssl_parameters_file = ssl-parameters.dat
    ssl_parameters_regenerate = 168
    ssl_verify_client_cert = no
    verbose_ssl = no


If you don't want to restart the whole daemon, we can run the following to reload the configuration without restarting the daemon:

    [root@rhel1 ~]# doveadm reload


The logs, should show the following:

    [root@rhel1 ~]# tail -3 /var/log/maillog
    Apr 26 18:12:35 rhel1 dovecot: master: Warning: SIGHUP received - reloading configuration
    Apr 26 18:13:35 rhel1 dovecot: master: Warning: Processes aren't dying after reload, sending SIGTERM.
    Apr 26 18:13:35 rhel1 dovecot: config: Warning: Killed with signal 15 (by pid=16440 uid=0 code=kill)


Lastly we can make sure, the daemon is listening on 993:

    [root@rhel1 ~]# netstat -antp | grep 993
    tcp        0      0 192.168.2.2:993             0.0.0.0:*                   LISTEN      16440/dovecot


And of course let's open up the firewall:

    [root@rhel1 ~]# iptables -I INPUT 18 -m state --state NEW -m tcp -p tcp --dport 993 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Running the following on the RH5 machine:

    [root@rhel2 ~]# mutt -f imaps://user1@rhel1


and I saw the following warning:

[<img src="https://github.com/elatov/uploads/raw/master/2014/04/mutt-ssl-warning.png" alt="mutt-ssl-warning" width="803" height="458" class="alignnone size-full wp-image-10692" />][3]

After accepting the certificate, I saw my INBOX over IMAPS:

![mutt-connected-to-imap][4]

Here is the connection to the IMAP server over SSL with the **openssl** command:

    [root@rhel2 ~]# openssl s_client -connect rhel1:993 -crlf
    CONNECTED(00000003)
    depth=0 /C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    verify error:num=18:self signed certificate
    verify return:1
    depth=0 /C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    verify return:1
    ---
    Certificate chain
     0 s:/C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
       i:/C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    MIICuzCCAiSgAwIBAgIJALrpER3zu8u4MA0GCSqGSIb3DQEBBQUAMIGTMQswCQYD
    VQQGEwJVUzERMA8GA1UECBMIQ29sb3JhZG8xEDAOBgNVBAcTB0JvdWxkZXIxDTAL
    BgNVBAoTBEhPTUUxETAPBgNVBAsUCFJIRUxfTEFCMRgwFgYDVQQDEw9yaGVsMS5s
    b2NhbC5jb20xIzAhBgkqhkiG9w0BCQEWFHBvc3RtYXN0ZXJAbG9jYWwuY29tMB4X
    DTE0MDQyNzAwMDczOFoXDTE1MDQyNzAwMDczOFowgZMxCzAJBgNVBAYTAlVTMREw
    DwYDVQQIEwhDb2xvcmFkbzEQMA4GA1UEBxMHQm91bGRlcjENMAsGA1UEChMESE9N
    RTERMA8GA1UECxQIUkhFTF9MQUIxGDAWBgNVBAMTD3JoZWwxLmxvY2FsLmNvbTEj
    MCEGCSqGSIb3DQEJARYUcG9zdG1hc3RlckBsb2NhbC5jb20wgZ8wDQYJKoZIhvcN
    AQEBBQADgY0AMIGJAoGBAMcYZFK4oatjtrISUie/LGin1chE+Ad3o+8Rp0OSX7Z7
    3HP2uXpjcKAE34VpCcvdYbaAV6bttBncSslJTC2cdpNgwKg/SiUeBJsQNaWpjTuZ
    y9UKNkCgbgYk+ehkmA8AhdHBYd0R4POQqbD7YOINMEIhJpuVzFi9fqV6KvV+P489
    AgMBAAGjFTATMBEGCWCGSAGG+EIBAQQEAwIGQDANBgkqhkiG9w0BAQUFAAOBgQDG
    gTqKKrEjxSGb4mjLvCaK+BjK0yJGovwv6PHdt6mZ4H+4i/8HdDbLm0rLnhmdK1PX
    wnNDIHn63LQo1gA78wvyVN4MVwVx30VhkUBz1tN4R6IhZ1DJdjclbhm303fo0Xxx
    laM13ztdl4Ob4msokjgis/JIkZIpsBOab4S//MlY0g==
    -----END CERTIFICATE-----
    subject=/C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    issuer=/C=US/ST=Colorado/L=Boulder/O=HOME/OU=RHEL_LAB/CN=rhel1.local.com/emailAddress=postmaster@local.com
    ---
    No client certificate CA names sent
    ---
    SSL handshake has read 1274 bytes and written 319 bytes
    ---
    New, TLSv1/SSLv3, Cipher is DHE-RSA-AES256-SHA
    Server public key is 1024 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : DHE-RSA-AES256-SHA
        Session-ID: 3416BADACE0051DA136A1829707B0D2E4EFDE7224FAD86A0429AE1C4F4042EF2
        Session-ID-ctx:
        Master-Key: 7122A9DAA2B93377999A82B1CA6FE3FD4A5D6623AE49B95B89AF8FF532CCDBBF7C053A65CA5FDF820D00F3214C940B6E
        Key-Arg   : None
        Krb5 Principal: None
        Start Time: 1398558036
        Timeout   : 300 (sec)
        Verify return code: 18 (self signed certificate)
    ---
    * OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN] Dovecot ready.
    01 LOGIN user1 passwd
    01 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS MULTIAPPEND UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS] Logged in
    02 LIST "" "*"
    * LIST (\NoInferiors \Marked) "/" "INBOX"
    02 OK List completed.
    03 EXAMINE INBOX
    * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
    * OK [PERMANENTFLAGS ()] Read-only mailbox.
    * 2 EXISTS
    * 0 RECENT
    * OK [UNSEEN 1] First unseen.
    * OK [UIDVALIDITY 1398552193] UIDs valid
    * OK [UIDNEXT 3] Predicted next UID
    * OK [HIGHESTMODSEQ 1] Highest
    03 OK [READ-ONLY] Select completed.
    04 FETCH 2 BODY[]
    * 2 FETCH (BODY[] {527}
    Return-Path: <root@rhel1.local.com>
    X-Original-To: user1
    Delivered-To: user1@rhel1.local.com
    Received: by rhel1.local.com (Postfix, from userid 0)
        id 46C1640E80; Sat, 26 Apr 2014 16:17:36 -0600 (MDT)
    Date: Sat, 26 Apr 2014 16:17:36 -0600
    To: user1@rhel1.local.com
    Subject: testing
    User-Agent: Heirloom mailx 12.4 7/29/08
    MIME-Version: 1.0
    Content-Type: text/plain; charset=us-ascii
    Content-Transfer-Encoding: 7bit
    Message-Id: <20140426221736.46C1640E80@rhel1.local.com>
    From: root@rhel1.local.com (root)

    test
    )
    04 OK Fetch completed.
    05 LOGOUT
    * BYE Logging out
    05 OK Logout completed.
    closed

 [1]: https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf
 [2]: https://github.com/elatov/uploads/raw/master/2014/04/mutt-connected-to-imap.png
 [3]: https://github.com/elatov/uploads/raw/master/2014/04/mutt-ssl-warning.png
 [4]: https://github.com/elatov/uploads/raw/master/2014/04/mutt-connected-to-imap1.png
