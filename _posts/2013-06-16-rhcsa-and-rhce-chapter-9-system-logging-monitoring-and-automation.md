---
title: 'RHCSA and RHCE Chapter 9 - System Logging, Monitoring, and Automation'
author: Karim Elatov
layout: post
permalink: /2013/06/rhcsa-and-rhce-chapter-9-system-logging-monitoring-and-automation/
categories: ['os','certifications', 'rhcsa_rhce']
tags: ['rhel', 'linux', 'rsyslog', 'performance']
---

## Syslog

From [Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/deployment_guide/red_hat_enterprise_linux-6-deployment_guide-en-us.pdf):

> **Chapter 20. Viewing and Managing Log Files**
> *Log files* are files that contain messages about the system, including the kernel, services, and applications running on it. There are different log files for different information. For example, there is a default system log file, a log file just for security messages, and a log file for cron tasks.
>
> Log files can be very useful when trying to troubleshoot a problem with the system such as trying to load a kernel driver or when looking for unauthorized login attempts to the system. This chapter discusses where to find log files, how to view log files, and what to look for in log files.
>
> Some log files are controlled by a daemon called **rsyslogd**. A list of log files maintained by **rsyslogd** can be found in the **/etc/rsyslog.conf** configuration file.
>
> **rsyslog** is an enhanced, multi-threaded syslog daemon which replaced the **sysklogd** daemon. **rsyslog** supports the same functionality as **sysklogd** and extends it with enhanced filtering, encryption protected relaying of messages, various configuration options, or support for transportation via the **TCP** or **UDP** protocols. Note that **rsyslog** is compatible with **sysklogd**.

Here is how the configuration file is broken down for rsyslog:

> **20.1. Configuring rsyslog**
> The main configuration file for **rsyslog** is **/etc/rsyslog.conf**. It consists of *global directives*, *rules* or comments (any empty lines or any text following a hash sign (#)). Both, global directives and rules are extensively described in the sections below.
>
> **20.1.1. Global Directives**
> Global directives specify configuration options that apply to the **rsyslogd** daemon. They usually specify a value for a specific pre-defined variable that affects the behavior of the rsyslogd daemon or a rule that follows. All of the global directives must start with a dollar sign ($). Only one directive can be specified per line. The following is an example of a global directive that specifies the maximum size of the syslog message queue:
>
>     $MainMsgQueueSize 50000
>
>
> The default size defined for this directive (10,000 messages) can be overridden by specifying a different value (as shown in the example above).
>
> You may define multiple directives in your **/etc/rsyslog.conf** configuration file. A directive affects the behavior of all configuration options until another occurrence of that same directive is detected.
>
> A comprehensive list of all available configuration directives and their detailed description can be found in **/usr/share/doc/rsyslog-*version-number*/rsyslog_conf_global.html**.
>
> **20.1.2. Modules**
> Due to its modular design, **rsyslog** offers a variety of *modules* which provide dynamic functionality. Note that modules can be written by third parties. Most modules provide additional inputs (see Input Modules below) or outputs (see Output Modules below). Other modules provide special functionality specific to each module. The modules may provide additional configuration directives that become available after a module is loaded. To load a module, use the following syntax:
>
>     $ModLoad module
>
>
> where **$ModLoad** is the global directive that loads the specified module and **MODULE** represents your desired module. For example, if you want to load the **Text File Input Module** (**imfile** — enables **rsyslog** to convert any standard text files into syslog messages), specify the following line in your **/etc/rsyslog.conf** configuration file:
>
>     $ModLoad imfile
>
>
> **20.1.3. Rules**
> A rule is specified by a filter part, which selects a subset of syslog messages, and an action part, which specifies what to do with the selected messages. To define a rule in your **/etc/rsyslog.conf** configuration file, define both, a filter and an action, on one line and separate them with one or more spaces or tabs.
>
> **20.1.3.1. Filter Conditions**
> **rsyslog** offers various ways how to filter syslog messages according to various properties. This sections sums up the most used filter conditions.
>
> **Facility/Priority-based filters** The most used and well-known way to filter syslog messages is to use the facility/priority-based filters which filter syslog messages based on two conditions: facility and priority. To create a selector, use the following syntax:
>
>     FACILITY.PRIORITY
>
>
> where:
>
> *   *FACILITY* specifies the subsystem that produces a specific syslog message. For example, the mail subsystem handles all mail related syslog messages. *FACILITY* can be represented by one of these keywords: **auth**, **authpriv**, **cron**, **daemon**, **kern**, **lpr**, **mail**, **news**, **syslog**, **user**, **uucp**, and **local0** through **local7**.
> *   *PRIORITY* specifies a priority of a syslog message. *PRIORITY* can be represented by one of these keywords (listed in an ascending order): **debug**, **info**, **notice**, **warning**, **err**, **crit**, **alert**, and **emerg**. By preceding any priority with an equal sign (=), you specify that only syslog messages with that priority will be selected. All other priorities will be ignored. Conversely, preceding a priority with an exclamation mark (!) selects all syslog messages but those with the defined priority. By not using either of these two extensions, you specify a selection of syslog messages with the defined or higher priority.
>
> In addition to the keywords specified above, you may also use an asterisk (*) to define all facilities or priorities (depending on where you place the asterisk, before or after the dot). Specifying the keyword none serves for facilities with no given priorities.
>
> To define multiple facilities and priorities, simply separate them with a comma (,). To define multiple filters on one line, separate them with a semi-colon (;).
>
> The following are a few examples of simple facility/priority-based filters:
>
>     kern.*    # Selects all kernel syslog messages with any priority
>     mail.crit    # Selects all mail syslog messages with priority crit and higher.
>     cron.!info,!debug    # Selects all cron syslog messages except those with the info or debug priority.
>
>
> **20.1.3.2. Actions**
> Actions specify what is to be done with the messages filtered out by an already-defined selector. The following are some of the actions you can define in your rule:
>
> **Saving syslog messages to log files**
> The majority of actions specify to which log file a syslog message is saved. This is done by specifying a file path after your already-defined selector. The following is a rule comprised of a selector that selects all **cron** syslog messages and an action that saves them into the **/var/log/cron.log** log file:
>
>     cron.* /var/log/cron.log
>
>
> Use a dash mark (-) as a prefix of the file path you specified if you want to omit syncing the desired log file after every syslog message is generated.
>
> Your specified file path can be either static or dynamic. Static files are represented by a simple file path as was shown in the example above. Dynamic files are represented by a template and a question mark (?) prefix.
>
> If the file you specified is an existing tty or /dev/console device, syslog messages are sent to standard output (using special tty-handling) or your console (using special /dev/console-handling) when using the X Window System, respectively.
>
> **Sending syslog messages over the network**
> **rsyslog** allows you to send and receive syslog messages over the network. This feature allows to administer syslog messages of multiple hosts on one machine. To forward syslog messages to a remote machine, use the following syntax:
>
>     @[(option)]host:[port]
>
>
> where:
>
> *   The at sign (@) indicates that the syslog messages are forwarded to a host using the UDP protocol. To use the TCP protocol, use two at signs with no space between them (@@).
> *   The *OPTION* attribute can be replaced with an option such as z*NUMBER*. This option enables zlib compression for syslog messages; the *NUMBER* attribute specifies the level of compression. To define multiple options, simply separate each one of them with a comma (,).
> *   The *HOST* attribute specifies the host which receives the selected syslog messages.
> *   The *PORT* attribute specifies the host machine's port.
>
> When specifying an IPv6 address as the host, enclose the address in square brackets ([, ]).
>
> The following are some examples of actions that forward syslog messages over the network (note that all actions are preceded with a selector that selects all messages with any priority):
>
>     *.* @192.168.0.1    # Forwards messages to 192.168.0.1 via the UDP protocol
>     *.* @@example.com:18    # Forwards messages to "example.com" using port 18 and the TCP protocol
>     *.* @(z9)[2001::1]    # Compresses messages with zlib (level 9 compression)
>                           # and forwards them to 2001::1 using the UDP protocol
>

Here is how the default configuration for rsyslog looks like:

    [root@rhel1 ~]# cat /etc/rsyslog.conf
    #rsyslog v3 config file
    
    # if you experience problems, check
    # http://www.rsyslog.com/troubleshoot for assistance
    
    #### MODULES ####
    
    $ModLoad imuxsock.so    # provides support for local system logging (e.g. via logger command)
    $ModLoad imklog.so  # provides kernel logging support (previously done by rklogd)
    #$ModLoad immark.so # provides --MARK-- message capability
    
    # Provides UDP syslog reception
    #$ModLoad imudp.so
    #$UDPServerRun 514
    
    # Provides TCP syslog reception
    #$ModLoad imtcp.so
    #$InputTCPServerRun 514


    #### GLOBAL DIRECTIVES ####
    
    # Use default timestamp format
    $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
    
    # File syncing capability is disabled by default. This feature is usually not required,
    # not useful and an extreme performance hit
    #$ActionFileEnableSync on


    #### RULES ####
    
    # Log all kernel messages to the console.
    # Logging much else clutters up the screen.
    #kern.*                                                 /dev/console
    
    # Log anything (except mail) of level info or higher.
    # Don't log private authentication messages!
    *.info;mail.none;authpriv.none;cron.none                /var/log/messages
    
    # The authpriv file has restricted access.
    authpriv.*                                              /var/log/secure
    
    # Log all the mail messages in one place.
    mail.*                                                  -/var/log/maillog


    # Log cron stuff
    cron.*                                                  /var/log/cron
    
    # Everybody gets emergency messages
    *.emerg                                                 *
    
    # Save news errors of level crit and higher in a special file.
    uucp,news.crit                                          /var/log/spooler
    
    # Save boot messages also to boot.log
    local7.*                                                /var/log/boot.log
    
    # ### begin forwarding rule ###
    # The statement between the begin ... end define a SINGLE forwarding
    # rule. They belong together, do NOT split them. If you create multiple
    # forwarding rules, duplicate the whole block!
    # Remote Logging (we use TCP for reliable delivery)
    #
    # An on-disk queue is created for this action. If the remote host is
    # down, messages are spooled to disk and sent when it is up again.
    #$WorkDirectory /var/spppl/rsyslog # where to place spool files
    #$ActionQueueFileName fwdRule1 # unique name prefix for spool files
    #$ActionQueueMaxDiskSpace 1g   # 1gb space limit (use as much as possible)
    #$ActionQueueSaveOnShutdown on # save messages to disk on shutdown
    #$ActionQueueType LinkedList   # run asynchronously
    #$ActionResumeRetryCount -1    # infinite retries if host is down
    # remote host is: name/ip:port, e.g. 192.168.0.1:514, port optional
    #*.* @@remote-host:514
    # ### end of the forwarding rule ###


Here is the Command Line Configuration:

> **20.1.4. rsyslog Command Line Configuration**
> Some of **rsyslog**'s functionality can be configured through the command line options, as **sysklogd**'s can. Note that as of version 3 of **rsyslog**, this method was deprecated. To enable some of these option, you must specify the compatibility mode **rsyslog** should run in. However, configuring **rsyslog** through the command line options should be avoided.
>
> To specify the compatibility mode **rsyslog** should run in, use the **-c** option. When no parameter is specified, **rsyslog** tries to be compatible with sysklogd. This is partially achieved by activating configuration directives that modify your configuration accordingly. Therefore, it is advisable to supply this option with a number that matches the major version of rsyslog that is in use and update your **/etc/rsyslog.conf** configuration file accordingly. If you want to, for example, use sysklogd options (which were deprecated in version 3 of **rsyslog**), you can specify so by executing the following command:
>
>     ~]# rsyslogd -c 2
>
>
> Options that are passed to the **rsyslogd** daemon, including the backward compatibility mode, can be specified in the **/etc/sysconfig/rsyslog** configuration file.

Here are the parameters used for my rsyslog daemon:

    [root@rhel1 ~]# ps -ef | grep rsyslog | grep -v grep
    root      1005     1  0 14:27 ?        00:00:00 /sbin/rsyslogd -c 4


## Logrotate

Next we move onto **logrotate**:

> **20.2. Locating Log Files**
> Most log files are located in the **/var/log/** directory. Some applications such as **httpd** and **samba** have a directory within **/var/log/** for their log files.
>
> You may notice multiple files in the **/var/log/** directory with numbers after them (for example, **cron-20100906**). These numbers represent a timestamp that has been added to a rotated log file. Log files are rotated so their file sizes do not become too large. The **logrotate** package contains a cron task that automatically rotates log files according to the **/etc/logrotate.conf** configuration file and the configuration files in the **/etc/logrotate.d/** directory.
>
> **20.2.1. Configuring logrotate**
> The following is a sample **/etc/logrotate.conf** configuration file:
>
>     # rotate log files weekly
>     weekly
>     # keep 4 weeks worth of backlogs
>     rotate 4
>     # uncomment this if you want your log files compressed
>     compress
>
>
> All of the lines in the sample configuration file define global options that apply to every log file. In our example, log files are rotated weekly, rotated log files are kept for the duration of 4 weeks, and all rotated log files are compressed by gzip into the .gz format. Any lines that begin with a hash sign (#) are comments and are not processed
>
> You may define configuration options for a specific log file and place it under the global options. However, it is advisable to create a separate configuration file for any specific log file in the **/etc/logrotate.d/** directory and define any configuration options there.
>
> The following is an example of a configuration file placed in the **/etc/logrotate.d/** directory:
>
>     /var/log/messages {
>         rotate 5
>         weekly
>         postrotate
>         /usr/bin/killall -HUP syslogd
>         endscript
>     }
>
>
> The configuration options in this file are specific for the **/var/log/messages** log file only. The settings specified here override the global settings where possible. Thus the rotated **/var/log/messages** log file will be kept for five weeks instead of four weeks as was defined in the global options.
>
> The following is a list of some of the directives you can specify in your **logrotate** configuration file:
>
> *   weekly — Specifies the rotation of log files on a weekly basis. Similar directives include:
>
>     *   daily
>     *   monthly
>     *   yearly
>
> *   compress — Enables compression of rotated log files. Similar directives include:
>
>     *   nocompress
>     *   compresscmd — Specifies the command to be used for compressing.
>     *   uncompresscmd
>     *   compressext — Specifies what extension is to be used for compressing.
>     *   compressoptions — Lets you specify any options that may be passed to the used compression program.
>     *   delaycompress — Postpones the compression of log files to the next rotation of log files.
>
> *   rotate *INTEGER* — Specifies the number of rotations a log file undergoes before it is removed or mailed to a specific address. If the value 0 is specified, old log files are removed instead of rotated.
>
> *   mail *ADDRESS* — This option enables mailing of log files that have been rotated as many times as is defined by the rotate directive to the specified address. Similar directives include:
>
>     *   nomail
>     *   mailfirst — Specifies that the just-rotated log files are to be mailed, instead of the about-to-expire log files.
>     *   maillast — Specifies that the about-to-expire log files are to be mailed, instead of the just-rotated log files. This is the default option when mail is enabled.

So **cron** runs **logrotate** periodically. Here is the script that cron runs daily:

    [root@rhel1 ~]# cat /etc/cron.daily/logrotate
    #!/bin/sh
    
    /usr/sbin/logrotate /etc/logrotate.conf >/dev/null 2>&1
    EXITVALUE=$?
    if [ $EXITVALUE != 0 ]; then
        /usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
    fi
    exit 0


That basically runs `/usr/sbin/logrotate /etc/logrotate.conf`. Checking out **/etc/logrotate.conf** file:

    [root@rhel1 ~]# cat /etc/logrotate.conf
    # see "man logrotate" for details
    # rotate log files weekly
    weekly
    
    # keep 4 weeks worth of backlogs
    rotate 4
    
    # create new (empty) log files after rotating old ones
    create
    
    # use date as a suffix of the rotated file
    dateext
    
    # uncomment this if you want your log files compressed
    #compress
    
    # RPM packages drop log rotation information into this directory
    include /etc/logrotate.d
    
    # no packages own wtmp and btmp -- we'll rotate them here
    /var/log/wtmp {
        monthly
        create 0664 root utmp
        minsize 1M
        rotate 1
    }
    
    /var/log/btmp {
        missingok
        monthly
        create 0600 root utmp
        rotate 1
    }


That has very generic settings and has settings for **/var/log/wtmp** and **/var/log/btmp** log files. But we also include everything that is the under **/etc/logrotate.d** folder and checking under that directory:

    [root@rhel1 ~]# ls /etc/logrotate.d/
    dracut  setroubleshoot  subscription-manager  syslog  up2date  vsftpd  yum


We can see package specific settings.

## Remote Syslog Server

Let's setup our RHEL6 machine to be a syslog Server to accept logs on UDP 514 and let's configure the RHEL 5 machine to send logs remotely to the RHEL6 machine on UDP 514.

### Syslog Server

On the RHEL 6 machine edit **/etc/rsyslog.conf** and un-comment the following lines:

    # Provides UDP syslog reception
    $ModLoad imudp.so
    $UDPServerRun 514


Restart the rsyslogd daemon:

    [root@rhel1 ~]# service rsyslog restart
    Shutting down system logger: rsyslogd
    Starting system logger:  rsyslogd


Make sure it's listening on UDP 514:

    [root@rhel1 ~]# netstat -anup --inet | grep 514
    udp        0      0 0.0.0.0:514                 0.0.0.0:*                               1524/rsyslogd


Open up the firewall for that port:

    [root@rhel1 ~]# iptables -I INPUT 5 -p udp -m udp --dport 514 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


### Syslog Client

On the RHEL 5 machine, edit **/etc/syslog.conf** and add the following lines:

    # Send logs to remote syslog server
    *.* @192.168.56.102


then restart the syslog services:

    [root@rhel2 ~]# service syslog restart
    Shutting down kernel logger:                               [  OK  ]
    Shutting down system logger:                               [  OK  ]
    Starting system logger:                                    [  OK  ]
    Starting kernel logger:                                    [  OK  ]


Then send a test message from the client:

    [root@rhel2 ~]# logger test


Check **tcpdump** on the syslog server, to make sure the logs are coming in:

    [root@rhel1 ~]# sudo tcpdump -i eth1 udp port 514
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
    18:17:25.347833 IP 192.168.56.103.syslog > 192.168.56.102.syslog: SYSLOG user.notice, length: 15


lastly check the logs in the server to make sure the logs are there:

    [root@rhel1 log]# grep 192.168.56.103 messages
    Jun 11 18:15:59 192.168.56.103 kernel: klogd 1.4.1, log source = /proc/kmsg started.
    Jun 11 18:17:25 192.168.56.103 root: test


There is our test message.

### Send Remote logs to a specific file

If you don't want to seep through **/var/log/message** for remote logs, you can add a rule to put remote logs to another file. On the server add the following to the **/etc/rsyslog.conf** file on top of all the Rules:

    #### RULES ####
    if $fromhost-ip == '192.168.56.103' then /var/log/remote/192-168-56-103.log
    & ~


The bottom line ensures that the logs don't get logged to the regular **/var/log/messages** file as well. Restart rsyslog:

    [root@rhel1 ~]# service rsyslog restart
    Shutting down system logger: rsyslogd
    Starting system logger:  rsyslogd


Do another test and make sure it shows up under the appropriate file:

    [root@rhel1 ~]# tail /var/log/remote/192-168-56-103.log
    Jun 11 18:31:48 192.168.56.103 root: test


That looks good.

### User Login Information

From [this](https://access.redhat.com/site/articles/3009) RHEL Forum:

> The **lastb** command is able to show a list of failed users logins since the creation date of the **/var/log/btmp** file. The **/var/log/btmp** file is a binary file which can not be viewed with a normal text editor.

and from [this](https://access.redhat.com/site/articles/1849) RHEL forum:

> The **last** command will display all users logged into a system along with their current tty's. However, it will only display login information starting from the time **/var/log/wtmp** was created.

There is also another command called lastlog. Here is how each look like:

    [root@rhel1 ~]# lastb
    root     ssh:notty    192.168.56.1     Wed Jun 12 16:26 - 16:26  (00:00)
    
    btmp begins Wed Jun 12 16:26:27 2013


So the latest failed login was from root.

    [root@rhel1 ~]# last
    root     pts/0        192.168.56.1     Wed Jun 12 16:26   still logged in
    root     pts/0        192.168.56.1     Wed Jun 12 16:14 - 16:26  (00:11)
    reboot   system boot  2.6.32-131.0.15. Wed Jun 12 16:13 - 16:42  (00:28)
    root     pts/0        192.168.56.1     Tue Jun 11 18:34 - down   (00:00)
    root     pts/0        192.168.56.1     Tue Jun 11 14:27 - 18:34  (04:06)
    reboot   system boot  2.6.32-131.0.15. Tue Jun 11 14:27 - 18:34  (04:06)
    root     tty1                          Mon Jun 10 18:22 - down   (00:00)


We can see a bunch of logins and their corresponding times.

    [root@rhel1 ~]# lastlog
    Username         Port     From             Latest
    root             pts/0    192.168.56.1     Wed Jun 12 16:26:28 -0600 2013
    bin                                        **Never logged in**
    daemon                                     **Never logged in**
    adm                                        **Never logged in**
    lp                                         **Never logged in**


We can see the last login for each user that exists on the system. We can see some system users were never logged in, which is expected. We can also check out currently logged in users, from [this](https://access.redhat.com/site/articles/1907) RHEL Forum:

> To quickly check who is currently log in on the server and the programs they are currently running, run the 'w' command. This command would also show how they are logged in, if they logged in remotely and the current time, how long the their login session has lasted. Alternatively, you can use the 'who' command. Here is how each looks like:

    [root@rhel1 ~]# w
     16:47:40 up 34 min,  1 user,  load average: 0.00, 0.00, 0.00
    USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
    root     pts/0    192.168.56.1     16:26    0.00s  0.05s  0.00s w


and here is the other one:

    [root@rhel1 ~]# who
    root     pts/0        2013-06-12 16:26 (192.168.56.1)


## Monitoring The System

From [Red Hat Enterprise Linux 6 Performance Tuning Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/performance_tuning_guide/red_hat_enterprise_linux-6-performance_tuning_guide-en-us.pdf):

> **3.3. Built-in Command-line Monitoring Tools**
> In addition to graphical monitoring tools, Red Hat Enterprise Linux provides several tools that can be used to monitor a system from the command line. The advantage of these tools is that they can be used outside run level 5. This section discusses each tool briefly, and suggests the purposes to which each tool is best suited.
>
> top
>
> The **top** tool provides a dynamic, real-time view of the processes in a running system. It can display a variety of information, including a system summary and the tasks currently being managed by the Linux kernel. It also has a limited ability to manipulate processes. Both its operation and the information it displays are highly configurable, and any configuration details can be made to persist across restarts.
>
> By default, the processes shown are ordered by the percentage of CPU usage, giving an easy view into the processes that are consuming the most resources. For detailed information about using **top**, refer to its man page: **man top**.
>
>     ps
>
>
> The **ps** tool takes a snapshot of a select group of active processes. By default this group is limited to processes owned by the current user and associated with the same terminal.
>
> It can provide more detailed information about processes than top, but is not dynamic. For detailed information about using ps, refer to its man page: **man ps**.
>
>     vmstat
>
>
> **vmstat** (Virtual Memory Statistics) outputs instantaneous reports about your system's processes, memory, paging, block I/O, interrupts and CPU activity.
>
> Although it is not dynamic like **top**, you can specify a sampling interval, which lets you observe system activity in near-real time.
>
> For detailed information about using **vmstat**, refer to its man page: **man vmstat**.
>
>     sar
>
>
> **sar** (System Activity Reporter) collects and reports information about today's system activity so far. The default output covers today's CPU utilization at ten minute intervals from the beginning of the day:
>
>     12:00:01 AM CPU %user %nice %system %iowait %steal %idle
>     12:10:01 AM all 0.10 0.00 0.15 2.96 0.00 96.79
>     12:20:01 AM all 0.09 0.00 0.13 3.16 0.00 96.61
>     12:30:01 AM all 0.09 0.00 0.14 2.11 0.00 97.66
>     ...
>
>
> This tool is a useful alternative to attempting to create periodic reports on system activity through **top** or similar tools.
>
> For detailed information about using **sar**, refer to its man page: **man sar**.

Here is how **top** looks like:

    top - 17:03:28 up 50 min,  1 user,  load average: 0.00, 0.00, 0.00
    Tasks:  73 total,   1 running,  72 sleeping,   0 stopped,   0 zombie
    Cpu(s):  0.0%us,  0.0%sy,  0.0%ni,100.0%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
    Mem:    511508k total,   161764k used,   349744k free,     9136k buffers
    Swap:  1048568k total,        0k used,  1048568k free,   101512k cached
    
      PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
     1334 root      20   0 11400 3224 2592 S  0.3  0.6   0:00.20 sshd
     1434 root      20   0  2540 1096  880 R  0.3  0.2   0:00.09 top
        1 root      20   0  2852 1384 1192 S  0.0  0.3   0:00.80 init
        2 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kthreadd
        3 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 migration/0
        4 root      20   0     0    0    0 S  0.0  0.0   0:00.00 ksoftirqd/0
        5 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 migration/0
        6 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 watchdog/0
        7 root      20   0     0    0    0 S  0.0  0.0   0:00.02 events/0
        8 root      20   0     0    0    0 S  0.0  0.0   0:00.00 cpuset
        9 root      20   0     0    0    0 S  0.0  0.0   0:00.00 khelper
       10 root      20   0     0    0    0 S  0.0  0.0   0:00.00 netns
       11 root      20   0     0    0    0 S  0.0  0.0   0:00.00 async/mgr
       12 root      20   0     0    0    0 S  0.0  0.0   0:00.00 pm
       13 root      20   0     0    0    0 S  0.0  0.0   0:00.00 sync_supers
       14 root      20   0     0    0    0 S  0.0  0.0   0:00.00 bdi-default
       15 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kintegrityd/0
       16 root      20   0     0    0    0 S  0.0  0.0   0:00.02 kblockd/0
       17 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kacpid
       18 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kacpi_notify
       19 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kacpi_hotplug
       20 root      20   0     0    0    0 S  0.0  0.0   0:00.00 ata/0
       21 root      20   0     0    0    0 S  0.0  0.0   0:00.00 ata_aux
       22 root      20   0     0    0    0 S  0.0  0.0   0:00.00 ksuspend_usbd
       23 root      20   0     0    0    0 S  0.0  0.0   0:00.00 khubd
       24 root      20   0     0    0    0 S  0.0  0.0   0:00.00 kseriod
       25 root      20   0     0    0    0 S  0.0  0.0   0:00.00 md/0
       26 root      20   0     0    0    0 S  0.0  0.0   0:00.00 md_misc/0


We can see a lot of information from top. CPU usage, Memory Usage and Priority of each process running on the system. From this output we can figure what process is taking the most resources on the system. From the above output, we can see that the system is pretty idle:

    Cpu(s):  0.0%us,  0.0%sy,  0.0%ni,100.0%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st


Our top CPU process is **sshd**:

    PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
     1334 root      20   0 11400 3224 2592 S  0.3  0.6   0:00.20 sshd
     1434 root      20   0  2540 1096  880 R  0.3  0.2   0:00.09 top
        1 root      20   0  2852 1384 1192 S  0.0  0.3   0:00.80 init


And that is a whopping 0.3% :) Here is how **ps** looks like:

    [root@rhel1 ~]# ps aux
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root         1  0.0  0.2   2852  1384 ?        Ss   16:13   0:00 /sbin/init
    root         2  0.0  0.0      0     0 ?        S    16:13   0:00 [kthreadd]
    root         3  0.0  0.0      0     0 ?        S    16:13   0:00 [migration/0]
    root         4  0.0  0.0      0     0 ?        S    16:13   0:00 [ksoftirqd/0]
    root         5  0.0  0.0      0     0 ?        S    16:13   0:00 [migration/0]
    root         6  0.0  0.0      0     0 ?        S    16:13   0:00 [watchdog/0]
    root         7  0.0  0.0      0     0 ?        S    16:13   0:00 [events/0]
    root         8  0.0  0.0      0     0 ?        S    16:13   0:00 [cpuset]
    root         9  0.0  0.0      0     0 ?        S    16:13   0:00 [khelper]
    root        10  0.0  0.0      0     0 ?        S    16:13   0:00 [netns]
    root        11  0.0  0.0      0     0 ?        S    16:13   0:00 [async/mgr]
    root        12  0.0  0.0      0     0 ?        S    16:13   0:00 [pm]
    root        13  0.0  0.0      0     0 ?        S    16:13   0:00 [sync_supers]
    root        14  0.0  0.0      0     0 ?        S    16:13   0:00 [bdi-default]
    root        15  0.0  0.0      0     0 ?        S    16:13   0:00 [kintegrityd/0]
    root        16  0.0  0.0      0     0 ?        S    16:13   0:00 [kblockd/0]
    root        17  0.0  0.0      0     0 ?        S    16:13   0:00 [kacpid]
    root        18  0.0  0.0      0     0 ?        S    16:13   0:00 [kacpi_notify]
    root        19  0.0  0.0      0     0 ?        S    16:13   0:00 [kacpi_hotplug]
    root        20  0.0  0.0      0     0 ?        S    16:13   0:00 [ata/0]
    root        21  0.0  0.0      0     0 ?        S    16:13   0:00 [ata_aux]
    root        22  0.0  0.0      0     0 ?        S    16:13   0:00 [ksuspend_usbd]
    root        23  0.0  0.0      0     0 ?        S    16:13   0:00 [khubd]
    root        24  0.0  0.0      0     0 ?        S    16:13   0:00 [kseriod]
    root        25  0.0  0.0      0     0 ?        S    16:13   0:00 [md/0]
    root        26  0.0  0.0      0     0 ?        S    16:13   0:00 [md_misc/0]
    root        27  0.0  0.0      0     0 ?        S    16:13   0:00 [khungtaskd]
    root        28  0.0  0.0      0     0 ?        S    16:13   0:00 [kswapd0]
    root        29  0.0  0.0      0     0 ?        SN   16:13   0:00 [ksmd]
    root        30  0.0  0.0      0     0 ?        S    16:13   0:00 [aio/0]
    root        31  0.0  0.0      0     0 ?        S    16:13   0:00 [crypto/0]
    root        36  0.0  0.0      0     0 ?        S    16:13   0:00 [kthrotld/0]
    root        38  0.0  0.0      0     0 ?        S    16:13   0:00 [kpsmoused]
    root        39  0.0  0.0      0     0 ?        S    16:13   0:00 [usbhid_resumer]
    root        69  0.0  0.0      0     0 ?        S    16:13   0:00 [kstriped]
    root       208  0.0  0.0      0     0 ?        S    16:13   0:00 [scsi_eh_0]
    root       209  0.0  0.0      0     0 ?        S    16:13   0:00 [scsi_eh_1]
    root       217  0.0  0.0      0     0 ?        S    16:13   0:00 [scsi_eh_2]
    root       272  0.0  0.0      0     0 ?        S    16:13   0:00 [kdmflush]
    root       276  0.0  0.0      0     0 ?        S    16:13   0:00 [kdmflush]
    root       291  0.0  0.0      0     0 ?        S    16:13   0:00 [jbd2/dm-0-8]
    root       292  0.0  0.0      0     0 ?        S    16:13   0:00 [ext4-dio-unwrit]
    root       363  0.0  0.1   2680   956 ?        S    16:13   0:00 /sbin/udevd -d
    root       653  0.0  0.0      0     0 ?        S    16:13   0:00 [jbd2/sda1-8]
    root       654  0.0  0.0      0     0 ?        S    16:13   0:00 [ext4-dio-unwrit]
    root       691  0.0  0.0      0     0 ?        S    16:13   0:00 [kauditd]
    root       858  0.0  0.0      0     0 ?        S    16:13   0:00 [flush-253:0]
    root       981  0.0  0.1  12896   796 ?        S    16:13   0:00 auditd
    root       983  0.0  0.1  13432   768 ?        S    16:13   0:00 /sbin/audispd
    root       987  0.0  0.4  15108  2140 ?        S   16:13   0:00 /usr/sbin/sedispatch
    root       999  0.0  0.3  45792  1548 ?        Sl   16:13   0:00 /sbin/rsyslogd -c 4
    rpc       1018  0.0  0.1   2536   612 ?        Ss   16:13   0:00 rpcbind
    dbus      1029  0.0  0.2  15112  1124 ?        Ssl  16:13   0:00 dbus-daemon --system
    root      1061  0.0  0.1   9256   896 ?        Ss   16:13   0:00 /usr/sbin/sshd
    root      1069  0.0  0.1   3152   876 ?        Ss   16:13   0:00 xinetd -stayalive -pidfile /var/run/xinetd.pid
    root      1080  0.0  0.1   7556   576 ?        Ss   16:13   0:00 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf
    root      1165  0.0  0.4  12312  2428 ?        Ss   16:13   0:00 /usr/libexec/postfix/master
    postfix   1172  0.0  0.4  12388  2388 ?        S    16:13   0:00 pickup -l -t fifo -u
    postfix   1173  0.0  0.4  12456  2428 ?        S    16:13   0:00 qmgr -l -t fifo -u
    root      1175  0.0  0.2   5876  1260 ?        Ss   16:13   0:00 crond
    root      1192  0.0  0.0   1972   388 ?        Ss   16:13   0:00 /usr/bin/rhsmcertd 240
    root      1204  0.0  0.0   1980   484 tty1     Ss+  16:13   0:00 /sbin/mingetty /dev/tty1
    root      1206  0.0  0.0   1980   484 tty2     Ss+  16:13   0:00 /sbin/mingetty /dev/tty2
    root      1208  0.0  0.0   1980   484 tty3     Ss+  16:13   0:00 /sbin/mingetty /dev/tty3
    root      1210  0.0  0.0   1980   480 tty4     Ss+  16:13   0:00 /sbin/mingetty /dev/tty4
    root      1212  0.0  0.0   1980   484 tty5     Ss+  16:13   0:00 /sbin/mingetty /dev/tty5
    root      1214  0.0  0.0   1980   488 tty6     Ss+  16:13   0:00 /sbin/mingetty /dev/tty6
    root      1222  0.0  0.3   3336  1760 ?        S< 16:13   0:00 /sbin/udevd -d
    root      1223  0.0  0.3   3336  1760 ?        S<   16:13   0:00 /sbin/udevd -d
    root      1334  0.0  0.6  11400  3224 ?        Ss   16:26   0:00 sshd: root@pts/0
    root      1339  0.0  0.3   5228  1756 pts/0    Ss   16:26   0:00 -bash
    root      1431  0.0  0.1   2796   592 ?        Ss   17:01   0:00 /usr/sbin/anacron -s
    root      1436  0.0  0.1   4776  1012 pts/0    R+   17:07   0:00 ps aux


If you want to figure out specific information regarding a process then **ps** is your friend. **Top** shows you an overall overview of the system, where **ps** can dig deeper into each process ID. We can even see the full path of the command that was used to start the process, this can be helpful as well. Let's see we wanted to find out any processes that have to do with postfix:

    [root@rhel1 ~]# ps -eaf | grep postfix
    root      1165     1  0 16:13 ?        00:00:00 /usr/libexec/postfix/master
    postfix   1172  1165  0 16:13 ?        00:00:00 pickup -l -t fifo -u
    postfix   1173  1165  0 16:13 ?        00:00:00 qmgr -l -t fifo -u


We can see a couple of processes that are started with the postfix user and the master process started by the root user. Similar tools exist like pidof and pgrep to find out PID of process names. Those tools are usually used in conjuction with **kill**,**pkill**,**nice**, and **renice**. Information regarding each of those can be seen in "[Controlling the system](http://linux.die.net/Linux-CLI/controlling-processes.html)". Here are brief descriptions of each:

> **pgrep**
> This command is useful for finding the process id of a particular process when you know part of its name.
>
> **kill**
> To kill processes on your system, you will need their pid's or id's . Use ps or pstree to find out the process id's (pid's), or use jobs to find out id's.
>
> **killall**
> Kill a process by it's name, uses names instead of process id's (pid's). Use -v to have killall report whether the kill was successful or not and -i for interactive mode (will prompt you before attempting to kill).
>
> **pkill**
> pkill is used to kill processes according to an extended regular expression. Use the -u option to kill using a user name(s) and process name (for example to only kill a process of a certain user). pkill can also send specific signals to processes.
>
> **nice**
> Sets the priority for a process. nice -20 is the maximum priority (only administrative users can assign negative priorities), nice 20 is the minimum priority. You must be root to give a process a higher priority, but you can always lower the priority of your own processes...
>
> **renice**
> Changes the priority of an existing command. You may use the options -u to change the priorities of all processes for a particular user name and -g to change priorities for all processes of a particular group. The default is to change via the process id number.

So let's renice our **rhsmcertd** process and then kill it. First let's take a look at the current process:

    [root@rhel1 ~]# ps -FcC rhsmcertd
    UID        PID  PPID CLS PRI    SZ   RSS PSR STIME TTY          TIME CMD
    root      1192     1 TS   19   493   388   0 16:13 ?        00:00:00 /usr/bin/rhsmcertd 240


We can see that the **Priority** is currently **19** and the **PID** is **1192**. Using the other tools, we can determine the **PID** like so:

    [root@rhel1 ~]# pgrep -l rhsmcertd
    1192 rhsmcertd


we can also use the **renice** command together with **pgrep**, like so:

    [root@rhel1 ~]# renice +4 `pgrep rhsmcertd`
    1192: old priority 0, new priority 4


Here is how the **Priority** looked like after the change:

    [root@rhel1 init.d]# ps -FcC rhsmcertd
    UID        PID  PPID CLS PRI    SZ   RSS PSR STIME TTY          TIME CMD
    root      1192     1 TS   15   493   388   0 17:49 ?        00:00:00 /usr/bin/rhsmcertd 240


So two ways to **kill** our process would be:

    [root@rhel1 ~]# pkill rhsmcertd
    [root@rhel1 ~]# kill `pgrep rhsmcertd`


After I restarted it, here was the new PID:

    [root@rhel1 init.d]# pidof rhsmcertd
    1807


Now that was a very little process managament guide, let's get back to system monitoring. I ran a quick **dd** command on one terminal:

    [root@rhel1 ~]# dd if=/dev/zero of=test.dd bs=1M count=100


on the other terminal I ran the **vmstat** command and here is what I saw:

    [root@rhel1 ~]# vmstat 1 10
    procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----
     r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
     0  0      0 324448  26072 104216    0    0    22     2   21   13  0  0 99  0  0
     0  0      0 324440  26072 104216    0    0     0     0   18    7  0  0 100 0  0
     0  1      0 251268  26128 173076    0    0    56 32776  146   73  0  9 63 28  0
     0  1      0 179596  26128 240448    0    0     0 95448  296  166  0 10 0  90  0
     0  1      0 129128  26136 290608    0    0     8 44064  259  127  0 10 0  90  0
     0  1      0  78040  26136 341160    0    0     0 45856  284  179  0 10 0  90  0
     1  1      0  31788  26136 386600    0    0     0 45760  294  209  1 10 0  89  0
     0  2      0   6180  23636 414972    0    0     4 45744  352  364  0 11 0  89  0
     0  1      0   9172   6848 438548    0    0    22   178   21   14  0  0 99  1  0
     0  0      0   9172   6852 438548    0    0     0     4   22   19  0  0 98  2  0
     0  0      0   9172   6852 438548    0    0     0     0   20   10  0  0 100 0  0
     0  0      0   9196   6852 438548    0    0     0     0   17    9  1  0 99  0  0


We definitely see a decrease in *free* memory (the filesystem caches a lot of the IO), an increase in *IO* (bo = Blocks sent to a block device), and of course an increase in interrupts (system *in*) since we were writing to a disk. For more information regarding IRQs, check out [Interrupts and IRQ Tuning](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html-single/Performance_Tuning_Guide/index.html#s-cpu-irq) from the Performance Tuning guide.

## Automation

From [Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf):

> **Chapter 21. Automating System Tasks**
> Tasks, also known as jobs, can be configured to run automatically within a specified period of time, on a specified date, or when the system load average decreases below 0.8.
>
> Red Hat Enterprise Linux is pre-configured to run important system tasks to keep the system updated. For example, the slocate database used by the locate command is updated daily. A system administrator can use automated tasks to perform periodic backups, monitor the system, run custom scripts, and so on.
>
> Red Hat Enterprise Linux comes with the following automated task utilities: cron, anacron, at, and batch.
>
> Every utility is intended for scheduling a different job type: while Cron and Anacron schedule recurring jobs, At and Batch schedule one-time jobs.
>
> **21.1. Cron and Anacron**
> Both, Cron and Anacron, are daemons that can schedule execution of recurring tasks to a certain point in time defined by the exact time, day of the month, month, day of the week, and week.
>
> Cron jobs can run as often as every minute. However, the utility assumes that the system is running continuously and if the system is not on at the time when a job is scheduled, the job is not executed.
>
> On the other hand, Anacron remembers the scheduled jobs if the system is not running at the time when the job is scheduled. The job is then executed as soon as the system is up. However, Anacron can only run a job once a day.
>
> **21.1.1. Installing Cron and Anacron**
> To install Cron and Anacron, you need to install the cronie package with Cron and the cronie-anacron package with Anacron (cronie-anacron is a sub-package of cronie).
>
> To determine if the packages are already installed on your system, issue the rpm -q cronie cronie-anacron command. The command returns full names of the cronie and cronie-anacron packages if already installed or notifies you that the packages are not available.
>
> To install the packages, use the yum command in the following form:
>
>      yum  install  package
>
>
> For example, to install both Cron and Anacron, type the following at a shell prompt:
>
>     ~]# yum install cronie cronie-anacron
>
>
> Note that you must have superuser privileges (that is, you must be logged in as root) to run this command.

Let's make sure we have it installed:

    [root@rhel1 ~]# rpm -qa cronie*
    cronie-1.4.4-7.el6.i686
    cronie-anacron-1.4.4-7.el6.i686


That looks good, moving on with the guide:

> **21.1.2.1. Starting and Stopping the Cron Service**
> To determine if the service is running, use the command service **crond** status. To run the **crond** service in the current session, type the following at a shell prompt as root:
>
>     service crond start
>
>
> To configure the service to be automatically started at boot time, use the following command:
>
>     chkconfig crond on
>
>
> This command enables the service in runlevel 2, 3, 4, and 5.
>
> **21.1.2.2. Stopping the Cron Service**
> To stop the crond service, type the following at a shell prompt as root
>
>     service crond stop
>
>
> To disable starting the service at boot time, use the following command:
>
>     chkconfig crond off
>
>
> This command disables the service in all runlevels.

Let's make sure the service is started and is setup to be automatically started:

    [root@rhel1 ~]# service crond status
    crond (pid  1175) is running...
    [root@rhel1 ~]# chkconfig --list crond
    crond           0:off   1:off   2:on    3:on    4:on    5:on    6:off


That looks fabuluos. Moving onto anacron:

> **21.1.3. Configuring Anacron Jobs**
> The main configuration file to schedule jobs is the **/etc/anacrontab** file, which can be only accessed by the root user. The file contains the following:
>
>     SHELL=/bin/sh
>     PATH=/sbin:/bin:/usr/sbin:/usr/bin
>     MAILTO=root
>     # the maximal random delay added to the base delay of the jobs
>     RANDOM_DELAY=45
>     # the jobs will be started during the following hours only
>     START_HOURS_RANGE=3-22
>
>     #period in days   delay in minutes   job-identifier   command
>     1         5     cron.daily    nice run-parts /etc/cron.daily
>     7         25    cron.weekly   nice run-parts /etc/cron.weekly
>     @monthly  45    cron.monthly  nice run-parts /etc/cron.monthly
>
>
> The first three lines define the variables that configure the environment in which the anacron tasks run:
>
> *   **SHELL** — shell environment used for running jobs (in the example, the Bash shell)
> *   **PATH** — paths to executable programs
> *   **MAILTO** — username of the user who receives the output of the anacron jobs by email If the **MAILTO** variable is not defined (**MAILTO=**), the email is not sent.
>
> The next two variables modify the scheduled time for the defined jobs:
>
> *   **RANDOM_DELAY** — maximum number of minutes that will be added to the **delay in minutes** variable which is specified for each job The minimum delay value is set, by default, to 6 minutes.
>
>     If **RANDOM_DELAY** is, for example, set to 12, then between 6 and 12 minutes are added to the delay in minutes for each job in that particular anacrontab. **RANDOM_DELAY** can also be set to a value below **6**, including ***||*. When set to ***||*, no random delay is added. This proves to be useful when, for example, more computers that share one network connection need to download the same data every day.
>
> *   **START_HOURS_RANGE** — interval, when scheduled jobs can be run, in hours
>
>     In case the time interval is missed, for example due to a power failure, the scheduled jobs are not executed that day.
>
> The remaining lines in the /etc/anacrontab file represent scheduled jobs and follow this format:
>
>     period in days   delay in minutes   job-identifier   command
>
>
> *   **period in days** — frequency of job execution in days
>     The property value can be defined as an integer or a macro (@daily, @weekly, @monthly), where @daily denotes the same value as integer 1, @weekly the same as 7, and @monthly specifies that the job is run once a month regarless of the length of the month.
> *   **delay in minutes** — number of minutes anacron waits before executing the job
>     The property value is defined as an integer. If the value is set to 0, no delay applies.
> *   **job-identifier** — unique name referring to a particular job used in the log files
> *   **command** — command to be executed
>     The command can be either a command such as ls /proc >> /tmp/proc or a command which executes a custom script.

Looking over the file on the RHEL6 machine, I saw the following:

    [root@rhel1 ~]# cat /etc/anacrontab
    # /etc/anacrontab: configuration file for anacron
    
    # See anacron(8) and anacrontab(5) for details.
    
    SHELL=/bin/sh
    PATH=/sbin:/bin:/usr/sbin:/usr/bin
    MAILTO=root
    # the maximal random delay added to the base delay of the jobs
    RANDOM_DELAY=45
    # the jobs will be started during the following hours only
    START_HOURS_RANGE=3-22
    
    #period in days   delay in minutes   job-identifier   command
    1   5   cron.daily      nice run-parts /etc/cron.daily
    7   25  cron.weekly     nice run-parts /etc/cron.weekly
    @monthly 45 cron.monthly        nice run-parts /etc/cron.monthly


It was the same as the example, anacron just takes care of any scheduling on a daily, weekly, and monthly basis. Here are some things that are run daily on the system:

    [root@rhel1 ~]# ls /etc/cron.daily/
    logrotate  makewhatis.cron  mlocate.cron  rhsm-complianced


Looks like logrotate (which we discussed above), the MAN database, the locate database, and the RHEL compliance check. If we wanted we could add our own script to be daily if we needed to. Moving onto Cron:

> **21.1.4. Configuring Cron Jobs**
> The configuration file for cron jobs is the **/etc/crontab**, which can be only modified by the root user. The file contains the following:
>
>     SHELL=/bin/bash
>     PATH=/sbin:/bin:/usr/sbin:/usr/bin
>     MAILTO=root
>     HOME=/
>     # For details see man 4 crontabs
>     # Example of job definition:
>     # .---------------- minute (0 - 59)
>     # | .------------- hour (0 - 23)
>     # | | .---------- day of month (1 - 31)
>     # | | | .------- month (1 - 12) OR jan,feb,mar,apr ...
>     # | | | | .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
>     # | | | | |
>     # * * * * * username  command to be executed
>
>
> The first three lines contain the same variable definitions as an anacrontab file: **SHELL**, **PATH**, and **MAILTO**.
>
> In addition, the file can define the **HOME** variable. The **HOME** variable defines the directory, which will be used as the home directory when executing commands or scripts run by the job.
>
> The remaining lines in the /etc/crontab file represent scheduled jobs and have the following format:
>
>     minute   hour   day   month   day of week   username   command
>
>
> The following define the time when the job is to be run:
>
> *   **minute** — any integer from 0 to 59
> *   **hour** — any integer from 0 to 23
> *   **day** — any integer from 1 to 31 (must be a valid day if a month is specified)
> *   **month** — any integer from 1 to 12 (or the short name of the month such as jan or feb)
> *   **day of week** — any integer from 0 to 7, where 0 or 7 represents Sunday (or the short name of the week such as sun or mon)
>
> The following define other job properties:
>
> *   **username** — specifies the user under which the jobs are run
> *   **command** — the command to be executed
>
> For any of the above values, an asterisk (*) can be used to specify all valid values. If you, for example, define the month value as an asterisk, the job will be executed every month within the constraints of the other values.
>
> A hyphen (-) between integers specifies a range of integers. For example, **1-4** means the integers 1, 2, 3, and 4.
>
> A list of values separated by commas (,) specifies a list. For example, **3, 4, 6, 8** indicates exactly these four integers.
>
> The forward slash (/) can be used to specify step values. The value of an integer will be skipped within a range following the range with /**integer**. For example, minute value defined as **0-59/2** denotes every other minute in the minute field. Step values can also be used with an asterisk. For instance, if the month value is defined as ***/3**, the task will run every third month.
>
> Any lines that begin with a hash sign (#) are comments and are not processed.
>
> Users other than root can configure cron tasks with the **crontab** utility. The user-defined crontabs are stored in the **/var/spool/cron/** directory and executed as if run by the users that created them.
>
> To create a crontab as a user, login as that user and type the command **crontab -e** to edit the user's crontab with the editor specified in the **VISUAL** or **EDITOR** environment variable. The file uses the same format as **/etc/crontab**. When the changes to the crontab are saved, the crontab is stored according to username and written to the file **/var/spool/cron/username**. To list the contents of your crontab file, use the **crontab -l** command.

Let's create a cron job to run a script which appends the date into a file every 5 minutes. First let's edit the file:

    [root@rhel1 ~]# vi /tmp/script.bash


then add the following into the file:

    #/bin/bash
    # Append date into a file
    /bin/date +"%m-%d-%Y_%H.%M.%S" >> /tmp/date


Now let's make the file executable:

    [root@rhel1 ~]# chmod +x /tmp/script.bash


Now let's run it to make sure it works as expected:

    [root@rhel1 ~]# /tmp/script.bash
    [root@rhel1 ~]# cat /tmp/date
    06-16-2013_17.17.05


That looks good. Now let's check the current cron table for the root user:

    [root@rhel1 ~]# crontab -l
    no crontab for root


We can see that it's currently empty. Now let's edit our cron table:

    [root@rhel1 ~]# crontab -e


That will fire an editor of your choice with an empty file. Then add the following entry into the file:

    */5 * * * * /tmp/script.bash


Save the file and exit your editor. After that is done you should see the following in your cron table:

    [root@rhel1 ~]# crontab -l
    */5 * * * * /tmp/script.bash


You can also see the contents of the cron table by checking out the following file:

    [root@rhel1 ~]# cat /var/spool/cron/root
    */5 * * * * /tmp/script.bash


Wait 10 minutes and check out the output file and you should see the following:

    [root@rhel1 ~]# cat /tmp/date
    06-16-2013_17.17.05
    06-16-2013_17.25.01
    06-16-2013_17.30.01


We can also control access to cron:

> **21.1.5. Controlling Access to Cron**
> To restrict the access to **Cron**, you can use the **/etc/cron.allow** and **/etc/cron.deny** files. These access control files use the same format with one username on each line. Mind that no whitespace characters are permitted in either file.
>
> If the **cron.allow** file exists, only users listed in the file are allowed to use cron, and the **cron.deny** file is ignored.
>
> If the **cron.allow** file does not exist, users listed in the **cron.deny** file are not allowed to use Cron.
>
> The Cron daemon (**crond**) does not have to be restarted if the access control files are modified. The access control files are checked each time a user tries to add or delete a cron job.
>
> The root user can always use cron, regardless of the usernames listed in the access control files.

## At and Batch

From the deployment guide:

> **21.2. At and Batch**
> While Cron is used to schedule recurring tasks, the **At** utility is used to schedule a one-time task at a specific time and the **Batch** utility is used to schedule a one-time task to be executed when the system load average drops below 0.8.
>
> **21.2.1. Installing At and Batch**
> To determine if the **at** package is already installed on your system, issue the **rpm -q at** command. The command returns the full name of the at package if already installed or notifies you that the package is not available.
>
> To install **At** and **Batch**, type the following at a shell prompt:
>
>     ~]# yum install at
>
>
> **21.2.2. Running the At Service**>br> The At and Batch jobs are both picked by the **atd** service. This section provides information on how to start, stop, and restart the atd service, and shows how to enable it in a particular runlevel.
>
> **21.2.2.1. Starting and Stopping the At Service**
> To determine if the service is running, use the command **service atd status**.
>
> To run the atd service in the current session, type the following at a shell prompt as root:
>
>     service atd start
>
>
> To configure the service to start automatically at boot, use the following command:
>
>     chkconfig atd on
>
>
> This command enables the service in runlevel 2, 3, 4, and 5

So let's see if atd is installed:

    [root@rhel1 ~]# rpm -q at
    package at is not installed


It looks like I don't have it installed. So let's go ahead and install it:

    [root@rhel1 ~]# yum install at
    ..
    ..
    Installed:
      at.i686 0:3.1.10-43.el6
    
    Complete!
    [root@rhel1 ~]#


Not let's make sure it enabled and running:

    [root@rhel1 ~]# service atd status
    atd is stopped
    [root@rhel1 ~]# chkconfig --list atd
    atd             0:off   1:off   2:off   3:on    4:on    5:on    6:off


It's enabled but it's not running. So let's start it:

    [root@rhel1 ~]# service atd start
    Starting atd:  atd
    [root@rhel1 ~]# service atd status
    atd (pid  1532) is running...


That looks good. Now let's keep down the deployment guide:

> **21.2.3. Configuring an At Job**
> To schedule a one-time job for a specific time with the **At** utility, do the following:
>
> 1.  On the command line, type the command **at TIME**, where **TIME** is the time when the command is to be executed.
>     The **TIME** argument can be defined in any of the following formats:
>
>     *   **HH:MM** specifies the exact hour and minute; For example, **04:00** specifies 4:00 a.m.
>     *   **midnight** specifies 12:00 a.m.
>     *   **noon** specifies 12:00 p.m.
>     *   **teatime** specifies 4:00 p.m.
>     *   **MONTHDAYYEAR** format; For example, **January 15 2012** specifies the 15th day of January in the year 2012. The year value is optional.
>     *   **MMDDYY**, **MM/DD/YY**, or **MM.DD.YY** formats; For example, **011512** for the 15th day of January in the year 2012.
>     *   **now + TIME** where **TIME** is defined as an integer and the value type: minutes, hours, days, or weeks. For example, **now + 5 days** specifies that the command will be executed at the same time five days from now.
>         The time must be specified first, followed by the optional date. For more information about the time format, refer to the /usr/share/doc/at-VERSION/timespec text file.
>
>     If the specified time has past, the job is executed at the time the next day.
>
> 2.  In the displayed at> prompt, define the job commands:
>
> *   Type the command the job should execute and press **Enter**. Optionally, repeat the step to provide multiple commands.
> *   Enter a shell script at the prompt and press Enter after each line in the script.
>     The job will use the shell set in the user's **SHELL** environment, the user's login shell, or **/bin/sh** (whichever is found first).
>
> 1.  Once finished, press **Ctrl+D** on an empty line to exit the prompt.
>
> If the set of commands or the script tries to display information to standard output, the output is emailed to the user.
>
> To view the list of pending jobs, use the **atq** command.

First let's remove our cron table:

    [root@rhel1 ~]# crontab -r
    [root@rhel1 ~]# crontab -l
    no crontab for root


The table is now empty. Also let's remove the output file:

    [root@rhel1 ~]# rm /tmp/date


Now let's run the same command, that we run from cron, 2 minutes from now:

    [root@rhel1 ~]# date; at now + 2 minutes
    Sun Jun 16 18:15:52 MDT 2013
    at> /tmp/script.bash
    at> EOT
    job 1 at 2013-06-16 18:17


We can see that I started at 18:15 and the job will be run at 18:17. Let's also check the queue:

    [root@rhel1 ~]# atq
    1   2013-06-16 18:17 a root


When the time has passed, we can check out the file:

    [root@rhel1 ~]# cat /tmp/date
    06-16-2013_18.17.00


and the date is correct. The **batch** utility works in the same way except you don't specify the time but the process is the same other than that. You can also block access to **at** just like with **cron**, from the deployment guide:

> **21.2.7. Controlling Access to At and Batch**
> You can restrict the access to the at and batch commands using the **/etc/at.allow** and **/etc/at.deny** files. These access control files use the same format defining one username on each line. Mind that no whitespace are permitted in either file.
>
> If the file **at.allow** exists, only users listed in the file are allowed to use **at** or **batch**, and the **at.deny** file is ignored.
>
> If **at.allow** does not exist, users listed in **at.deny** are not allowed to use **at** or **batch**.
>
> The **at** daemon (**atd**) does not have to be restarted if the access control files are modified. The access control files are read each time a user tries to execute the **at** or **batch** commands.
>
> The root user can always execute **at** and **batch** commands, regardless of the content of the access control files.

