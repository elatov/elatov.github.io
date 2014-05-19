---
title: Install Samhain with Beltane on FreeBSD
author: Karim Elatov
layout: post
permalink: /2014/03/install-samhain-beltane-freebsd/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2515584096
categories:
  - Home Lab
  - OS
tags:
  - beltane
  - freebsd
  - hids
  - samhain
---
I wanted to add extra security to my home lab and I heard good things about the HIDS (Host-based Intrusion Detection System) software called [Samhain](http://www.la-samhna.de/samhain/).

### Samhain

From their site, here is a quick overview of what the software does:

> The Samhain host-based intrusion detection system (HIDS) provides file integrity checking and log file monitoring/analysis, as well as rootkit detection, port monitoring, detection of rogue SUID executables, and hidden processes.
>
> Samhain been designed to monitor multiple hosts with potentially different operating systems, providing centralized logging and maintenance, although it can also be used as standalone application on a single host.

I was planning on setting this up on multiple hosts, so going with the centralized logging was the desired approach for me.

### Beltane

From their site, here is an overview of Beltane:

> Beltane is a web-based central management console for the Samhain file integrity / intrusion detection system. It enables the administrator to browse client messages, acknowledge them, and update centrally stored file signature databases.
>
> As the Samhain daemon keeps a memory of file changes, the file signature database need only be up to date when the daemon restarts and downloads the database from the central server. Beltane allows you to use the information logged by the client in order to update the signature database

Also here are the requirements for Beltane:

> Beltane requires a Samhain (version 1.6.0 or higher) client/server installation, with file signature databases stored on the central server, and logging to an SQL database enabled.
>
> Beltane is a PHP application, with some additional components written in C. It requires PHP version 4.3 or later, compiled as Apache module or as CGI interpreter.

There are two version of Beltane available, the free version and the Paid version. I wanted to try out the free version to see how it works out.

#### Samhain Prerequisites

Since I was planning on using beltane, I needed to setup a MySQL server on my FreeBSD machine. To install MySQL, I ran the following:

    moxz:~>cd /usr/ports/databases/mysql55-server
    moxz:/usr/ports/databases/mysql55-server>sudo make install clean


After that, add the following to the **/etc/rc.conf** file, so we can start the service:

    mysql_enable="YES"


Then to start the service, run the following:

    moxz:~>sudo service mysql-server start


After MySQL starts, secure the installation by running the following:

    moxz:~>sudo /usr/local/bin/mysql_secure_installation


That will ask you to set a password for root and to remove test databases. After it's all secure, create the MySQL database that we will use for Samhain:

    moxz:/opt/work/samhain-3.1.0.yule/sql_init>mysql -u root -p < samhain.mysql.init
    Enter password:


After entering the root password for MySQL, it will create the database. You can check out the database like so:

    moxz:~>mysql -u root -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 145
    Server version: 5.5.36 Source distribution

    Copyright (c) 2000, 2014, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | samhain            |
    +--------------------+
    4 rows in set (0.08 sec)

    mysql> use samhain;
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
    mysql> show tables;
    +-------------------+
    | Tables_in_samhain |
    +-------------------+
    | log               |
    +-------------------+
    1 row in set (0.00 sec)


I ran the following to create the samhain user:

    mysql> grant select, insert, update on samhain.log to samhain@'%' IDENTIFIED BY 'samhain';


I added the **update** permission since it's necessary for the Beltane configuration later on.

#### Install the Samhain Server (Yule)

Here is a [link](http://www.la-samhna.de/samhain/HOWTO-client+server.html) to a pretty good how-to. On my FreeBSD 10 machine I ran the following to get the source:

    moxz:/opt/work>fetch http://www.la-samhna.de/samhain/samhain-current.tar.gz
    samhain-current.tar.gz                        100% of 2067 kB  328 kBps 00m06s


I then extracted it:

    moxz:/opt/work/sam>tar xvzf samhain-current.tar.gz
    x samhain-3.1.0.tar.gz
    x samhain-3.1.0.tar.gz.asc


There are two files, the signature and the source. I just extracted the source from there:

    moxz:/opt/work/sam>tar xzf samhain-3.1.0.tar.gz


Now let's try to compile the source:

    moxz:/opt/work/sam>cd samhain-3.1.0/
    moxz:/opt/work/sam/samhain-3.1.0>./configure --prefix=/usr/local/yule --enable-xml-log --with-database=mysql --enable-network=server


The configure did go through, and at the end I got the summary as follows:

    samhain has been configured as follows:
         System binaries: /usr/local/yule/sbin
      Configuration file: /usr/local/yule/etc/yulerc
            Manual pages: /usr/local/yule/share/man
                    Data: /usr/local/yule/var/lib/yule
                PID file: /usr/local/yule/var/run/yule.pid
                Log file: /usr/local/yule/var/log/yule/yule_log
                Base key: 276553787,1612095713

        Selected rc file: yulerc


Upon running **make**, I saw the following error:

    ./src/sh_tiger1_64.c:375:3: error: ran out of registers during register
          allocation
      tiger_compress_macro(((word64*)str), ((word64*)state));
      ^
    ./src/sh_tiger1_64.c:366:3: note: expanded from macro 'tiger_compress_macro'
      compress; \
      ^
    ./src/sh_tiger1_64.c:327:4: note: expanded from macro 'compress'
              pass5n(a,b,c) \
              ^
    ./src/sh_tiger1_64.c:226:4: note: expanded from macro 'pass5n'
              round5(a,b,c,x0) \
              ^
    ./src/sh_tiger1_64.c:177:2: note: expanded from macro 'round5'
            roundX(a,b,c,x) \
            ^
    ./src/sh_tiger1_64.c:142:27: note: expanded from macro 'roundX'
    #define roundX(a,b,c,x)   \


I ran into [FreeBSD 10 Release Notes](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=701353) :

> On platforms where clang(1) is the default system compiler (such as i386, amd64, arm), GCC and GNU libstdc++ are no longer built by default. clang(1) and libc++ from LLVM are used on these platforms by instead.

More information on the switch over is here:

*   [FreeBSD 10 To Use Clang Compiler, Deprecate GCC](http://www.phoronix.com/scan.php?page=news_item&px=MTEwMjI)
*   [Ports and Clang](https://wiki.freebsd.org/PortsAndClang)

To confirm, I ran the following:

    moxz:/opt/work/sam/samhain-3.1.0>cc -v
    FreeBSD clang version 3.3 (tags/RELEASE_33/final 183502) 20130610
    Target: x86_64-unknown-freebsd10.0
    Thread model: posix


So I went ahead and compiled gcc47:

    moxz:~>cd /usr/ports/lang/gcc47
    moxz:/usr/ports/lang/gcc47>sudo make install


After the compile finished, I set my environment variables as such:

    moxz:/opt/work/sam/samhain-3.1.0>setenv CC gcc47
    moxz:/opt/work/sam/samhain-3.1.0>setenv CPP cpp47
    moxz:/opt/work/sam/samhain-3.1.0>setenv CXX g++47


and then re-configured the package:

    moxz:/opt/work/sam/samhain-3.1.0>./configure --prefix=/usr/local/yule --enable-xml-log --with-database=mysql --enable-network=server


and I got back the same summary:

    samhain has been configured as follows:
         System binaries: /usr/local/yule/sbin
      Configuration file: /usr/local/yule/etc/yulerc
            Manual pages: /usr/local/yule/share/man
                    Data: /usr/local/yule/var/lib/yule
                PID file: /usr/local/yule/var/run/yule.pid
                Log file: /usr/local/yule/var/log/yule/yule_log
                Base key: 1345970140,546504808

        Selected rc file: yulerc


Upon running make again, I got the following error:

    /usr/local/bin/ld: /usr/lib/crt1.o: relocation R_X86_64_32 against `_DYNAMIC' can not be used when making a shared object; recompile with -fPIC
    /usr/lib/crt1.o: error adding symbols: Bad value
    collect2: error: ld returned 1 exit status
    *** Error code 1


I then ran into these page:

*   [latest chromium (14.0.835.163): gcc45 issues](http://lists.freebsd.org/pipermail/freebsd-chromium/2011-September/000245.html)
*   [Error when Compiling on FreeBSD with LibSpoton & unused argumen](http://sourceforge.net/p/dooble/discussion/864481/thread/4418e1f2/)

Both fixed that issue by removing the '**-pie**' argument from LDFLAGS. So I edited the **configure** script and removed the **-pie** option. So I changed the following lines:

    CFLAGS="$CFLAGS -pie -fPIE"
    PIE_CFLAGS="-fPIE"
    PIE_LDFLAGS="-pie"


To just this:

    CFLAGS="$CFLAGS"
    PIE_CFLAGS=""
    PIE_LDFLAGS=""


Then running another **./configure** and **make** actually went through. After that I created the directory and installed the package:

    moxz:/opt/work/sam/samhain-3.1.0>sudo mkdir /usr/local/yule
    moxz:/opt/work/sam/samhain-3.1.0>sudo chown elatov:elatov /usr/local/yule
    moxz:/opt/work/sam/samhain-3.1.0>make install


### Configure Yule

Here is how my configuration looked like:

    moxz:~>grep -Ev '^#|^$' /usr/local/yule/etc/yulerc
    [Log]
    PrintSeverity=none
    LogSeverity = *
    DatabaseSeverity = warn
    [Database]
    SetDBName = samhain
    SetDBTable = log
    SetDBUser = samhain
    SetDBPassword = samhain
    SetDBHost = localhost
    SetDBServerTstamp = True
    [Misc]
    Daemon=yes
    SetLoopTime = 600
    [Clients]


Notice I didn't have any clients yet and I set my **LogSeverity** for everything. I just wanted to get a good feel of the logs, but I would say **warn** should be enough.

Then to start the service run the following

    moxz:~>/usr/local/yule/sbin/yule -S


Checking out the logs you should see the following:

    moxz:~>tail /usr/local/yule/var/log/yule/yule_log
    <log sev="ALRT" tstamp="2014-03-16T09:22:55-0600" msg="START" program="Yule" userid="1000" path="/usr/local/yule/etc/yulerc" hash="D1CBAE6C8030B49293EA530E7EDCD7654B4C8F55F62481AE"  >
    <sig>91A07CFF9A3A94833C69D4A36BAFA98FE43FCC27CCF0FDA4</sig></log>
    <log sev="MARK" tstamp="2014-03-16T09:22:55-0600" msg="Server up, simultaneous connections: 1017" socket_id="3"  >


#### Install Samhain Client

I ended up using the same source directory to build the client:

    moxz:~>cd /opt/work/sam/samhain-3.1.0/


Then I removed the old compiled stuff and re-configured the package (I was still using **gcc47**):

    moxz:/opt/work/sam/samhain-3.1.0>make clean
    rm -f core *.o

    moxz:/opt/work/sam/samhain-3.1.0./configure --prefix=/usr/local/samhain --enable-xml-log --enable-network=client --with-data-file=REQ_FROM_SERVER/usr/local/samhain/var/lib/samhain/samhain_file --with-config-file=REQ_FROM_SERVER/usr/local/samhain/etc/samhainrc --with-logserver=moxz.local.com


After the **configure** was done, I saw the following summary:

    samhain has been configured as follows:
         System binaries: /usr/local/samhain/sbin
      Configuration file: REQ_FROM_SERVER/usr/local/samhain/etc/samhainrc
            Manual pages: /usr/local/samhain/share/man
                    Data: /usr/local/samhain/var/lib/samhain
                PID file: /usr/local/samhain/var/run/samhain.pid
                Log file: /usr/local/samhain/var/log/samhain_log
                Base key: 274317422,1621712888


Running **make** was successful, since I was using the same **configure** script that I modified before.

Then I created the destination directory and installed the package

    moxz:/opt/work/sam/samhain-3.1.0>sudo mkdir /usr/local/samhain/
    moxz:/opt/work/sam/samhain-3.1.0>sudo chown elatov:elatov /usr/local/samhain/
    moxz:/opt/work/sam/samhain-3.1.0>make install


#### Configure the Samhain client

Here is how my configuration file looked like:

    moxz:~>grep -Ev '^#|^$' /usr/local/samhain/etc/samhainrc
    [Misc]
    [ReadOnly]
    dir = 0/
    [Attributes]
    file = /
    file = /proc
    file = /entropy
    file = /tmp
    file = /var
    [Attributes]
    dir = 99/dev
    [IgnoreAll]
    file = /dev/ttyp?
    [Misc]
    IgnoreAdded = /dev/(p|t)typ.*
    IgnoreMissing = /dev/(p|t)typ.*
    [ReadOnly]
    dir = 99/etc
    [ReadOnly]
    dir = 99/boot
    [ReadOnly]
    dir = 99/bin
    dir = 99/sbin
    [ReadOnly]
    dir = 99/lib
    [ReadOnly]
    dir = 99/libexec
    [ReadOnly]
    dir = 99/rescue
    [Attributes]
    dir = 99/root
    [ReadOnly]
    dir = 99/stand
    [ReadOnly]
    dir = 99/usr
    [Attributes]
    dir = /usr/.snap
    dir = /usr/share/man/cat?
    file = /usr/compat/linux/etc
    file = /usr/compat/linux/etc/ld.so.cache
    [IgnoreAll]
    dir = -1/usr/home
    dir = -1/usr/ports

    [Attributes]
    dir = 0/var
    [LogFiles]
    file=/var/run/utmp
    [GrowingLogFiles]
    dir = 99/var/log
    [Attributes]
    file = /var/log/*.[0-9].bz2
    file = /var/log/*.[0-9].log
    file = /var/log/*.[0-9]
    file = /var/log/*.[0-9][0-9]
    file = /var/log/*.old
    file = /var/log/sendmail.st
    [Misc]
    IgnoreAdded = /var/log/.*\.[0-9]+$
    IgnoreAdded = /var/log/.*\.[0-9]+\.gz$
    IgnoreAdded = /var/log/.*\.[0-9]+\.bz2$
    IgnoreAdded = /var/log/.*\.[0-9]+\.log$
    [IgnoreNone]
    [User0]
    [User1]
    [EventSeverity]
    SeverityIgnoreAll=info
    [Log]
    LogSeverity=warn

    [Misc]
    Daemon = yes
    ChecksumTest=check
    SetNiceLevel = 19
    SetIOLimit = 500
    SetLoopTime = 86400
    SetFileCheckTime = 7200
    SyslogFacility=LOG_LOCAL2
    [EOF]


Fell free to change what directories you want to monitor. Also notice that I changed my nice level and I limited the IO. I was getting a lot of warnings on the VM that's it's running out of memory. Setting it with a higher nice level helped out.

#### Add Samhain Client to Samhain Server (Yule)

Before we go any further we need to establish a trust between the client and the server. This is done by embedding a password into the samhain binary. First on the server run the following to generate the password:

    moxz:~>/usr/local/yule/sbin/yule -G
    52D1DF66E5FC5DCC


Then on the client create a new binary and embed that password:

    moxz:~>cd /usr/local/samhain/sbin
    moxz:/usr/local/samhain/sbin>./samhain_setpwd samhain moxz 52D1DF66E5FC5DCC
    INFO   old password found
    INFO   replaced:  f7c312aaaa12c3f7  by:  52d1df66e5fc5dcc
    INFO   finished


Lastly replace the **samhain** binary with newly embedded one:

    moxz:/usr/local/samhain/sbin>cp samhain.moxz samhain


Now add the client to the yule server configuration:

    moxz:~>/usr/local/yule/sbin/yule -P 52D1DF66E5FC5DCC | sed s%HOSTNAME%moxz.local.com% >> /usr/local/yule/etc/yulerc


Now you should have the following added to your **yulerc** file:

    moxz:~>tail -1 /usr/local/yule/etc/yulerc
    Client=moxz.local.com@D534D98453A3F78B@A72D238707B8D5C376AF39138483562FF28EC4BD38C980CD3738C876A02C2D7F9F1C54684EEE9F28D0E8137458D8067812C38F03F892199D336DEEB18ACFE05F5D050D9C3AF1B7C2D29B3458F12394A7EF4017445961929415B613C1CC7D1532E2A152E6A1DABED758064F02C91578F72D2DE24FF8609AA146E94877FBBCEFA3


Since we made a change to yule server configuration let's send a SIGHUP to re-read the configuration:

    moxz:~>pkill -HUP yule


After running that in the logs you will see the following:

    <log sev="CRIT" tstamp="2014-03-16T10:00:09-0600" msg="Runtime configuration rel
    oaded"  >


#### Start the samhain client

Before we can connect to our server, we need to initialize the client. [From Initialize the baseline database](http://www.la-samhna.de/samhain/manual/installation-initialize.html):

> samhain works by comparing the present state of the filesystem against a baseline database. Of course, this baseline database must be initialized first (and preferably from a known good state !). To perform the initialization (i.e. create the baseline database), type:
>
>     sh$ samhain -t init -p info
>
>
> (with -p info, messages of severity 'info' or higher will be printed to your terminal/console).
>
> If the database file already exists, `samhain -t init` will append to it. This is a feature that is intended to help you operating samhain in a slightly more stealthy way: you can append the database e.g. to a JPEG picture (and the picture will still display normally - JPEG ignores appended 'garbage').
>
> **Note:**
>
> It is usually an error to run `samhain -t init` twice, because (a) it will append a second baseline database to the existing one, and (b) only the first baseline database will be used. Use `samhain -t update` for updating the baseline database. Delete or rename the baseline database file if you really want to run `samhain -t init` a second time.

So let's create a baseline database:

    moxz:~>/usr/local/samhain/sbin/samhain -t init -p info
    ALERT  :  [2014-03-16T10:34:26-0600] msg=<START>, program=<Samhain>, userid=<1000>, path=</usr/local/samhain/etc/samhainrc>, hash=<B609FF621721E9DADBE3949077940BBCC92BCE6080E305EB>
    INFO   :  [2014-03-16T10:34:27-0600] msg=<Checking       [ReadOnly]>, path=</>
    CRIT   :  [2014-03-16T10:34:27-0600] msg=<Not accessible or not a regular file (File access error / Permission denied)>, path=</.sujournal>


That might take a while since I modified the Nice Level and Limited the IO. After the database is ready, copy the configuration file and the database over to the server (in my case they were on the same machine, but if that was not the case, we could just use **scp**):

    moxz:~>cp /usr/local/samhain/etc/samhainrc /usr/local/yule/var/lib/yule/rc.moxz.local.com
    moxz:~>cp /usr/local/samhain/var/lib/samhain/samhain_file /usr/local/yule/var/lib/yule/file.moxz.local.com


Now let's start the client:

    moxz:~>/usr/local/samhain/sbin/samhain -D
    <log sev="INFO" tstamp="2014-03-09T15:48:09-0600" msg="Downloading configuration file" />
    <log sev="INFO" tstamp="2014-03-09T15:48:10-0600" msg="Session key negotiated" />
    <log sev="INFO" tstamp="2014-03-09T15:48:10-0600" msg="File download completed" />
    <log sev="ERRO" tstamp="2014-03-09T15:48:10-0600" interface="glob" msg="No matches found" path="/dev/ttyp?" />
    <log sev="ERRO" tstamp="2014-03-09T15:48:10-0600" interface="glob" msg="No matches found" path="/var/log/*.[0-9].log" />
    <log sev="ERRO" tstamp="2014-03-09T15:48:10-0600" interface="glob" msg="No matches found" path="/var/log/*.[0-9][0-9]" />
    <log sev="ERRO" tstamp="2014-03-09T15:48:10-0600" interface="glob" msg="No matches found" path="/var/log/*.old" />
    <log sev="INFO" tstamp="2014-03-09T15:48:10-0600" msg="Downloading database file" />
    <log sev="INFO" tstamp="2014-03-09T15:50:08-0600" msg="File download completed" />


Upon starting the samhain client, I saw the following logs in the yule server:

    moxz:~>tail /usr/local/yule/var/log/yule/yule_log
    <log sev="RCVT" tstamp="2014-03-16 10:16:26-0600" remote_host="moxz" > <log sev="ALRT" tstamp="2014-03-16 10:16:26-0600" msg="LOGKEY" program="Samhain" hash="30988C69A4A79484D0D94C5EA920609E30B0B89E65B81DB7" />
    <sig>4F0929FA4CB8EED7745ED37462F21592F4246DA43FECC183</sig></log>
    <log sev="RCVT" tstamp="2014-03-16 10:16:26-0600" remote_host="moxz" > <log sev="ALRT" tstamp="2014-03-16 10:16:25-0600" msg="START" program="Samhain" userid="1000" path="REQ_FROM_SERVER" hash="8894E0510E351CAE628DC1D3F31D4C576505A3B2ED800662" path_data="REQ_FROM_SERVER" hash_data="DAB8041DC0971CA9D0ACB2B6849140A6497D304E74B6E2DF" />


### Beltane Prerequisites

Initially I used PHP 5.4 but later realized "Beltane I" uses an old *Session* function that is no longer available after PHP 5.3. Here is a [link](http://stackoverflow.com/questions/16082420/call-to-undefined-function-session-register) to a discussion about that. So I ended up installing PHP 5.3. First I install Apache:

    moxz:~>cd /usr/ports/www/apache22
    moxz:/usr/ports/www/apache22>sudo make install clean


Here is the configuration I used for that:

    moxz:/usr/ports/www/apache22>make showconfig
    ===> The following configuration options are available for apache22-2.2.26:
         AUTH_BASIC=on: mod_auth_basic
         AUTH_DIGEST=on: mod_auth_digest
         AUTHN_ALIAS=on: mod_authn_alias
         AUTHN_ANON=on: mod_authn_anon
         AUTHN_DBD=off: mod_authn_dbd
         AUTHN_DBM=on: mod_authn_dbm
         AUTHN_DEFAULT=on: mod_authn_default
         AUTHN_FILE=on: mod_authn_file
         AUTHZ_DBM=on: mod_authz_dbm
         AUTHZ_DEFAULT=on: mod_authz_default
         AUTHZ_GROUPFILE=on: mod_authz_groupfile
         AUTHZ_HOST=on: mod_authz_host
         AUTHZ_OWNER=on: mod_authz_owner
         AUTHZ_USER=on: mod_authz_user
         AUTHNZ_LDAP=off: mod_authnz_ldap
         LDAP=off: connection pooling, result caching
         DBD=off: Manages SQL database connections
         CACHE=on: mod_cache
         DISK_CACHE=on: mod_disk_cache
         FILE_CACHE=on: mod_file_cache
         MEM_CACHE=off: mod_mem_cache
         DAV=off: mod_dav
         DAV_FS=off: mod_dav_fs
         DAV_LOCK=off: mod_dav_lock
         ACTIONS=on: mod_actions
         ALIAS=on: mod_alias
         ASIS=on: mod_asis
         AUTOINDEX=on: mod_autoindex
         CERN_META=on: mod_cern_meta
         CGI=on: mod_cgi
         CGID=off: mod_cgid
         CHARSET_LITE=on: mod_charset_lite
         DEFLATE=on: mod_deflate
         DIR=on: mod_dir
         DUMPIO=on: mod_dumpio
         ENV=on: mod_env
         EXPIRES=on: mod_expires
         HEADERS=on: mod_headers
         IMAGEMAP=on: mod_imagemap
         INCLUDE=on: mod_include
         INFO=on: mod_info
         LOG_CONFIG=on: mod_log_config
         LOGIO=on: mod_logio
         MIME=on: mod_mime
         MIME_MAGIC=on: mod_mime_magic
         NEGOTIATION=on: mod_negotiation
         REWRITE=on: mod_rewrite
         SETENVIF=on: mod_setenvif
         SPELING=on: mod_speling
         STATUS=on: mod_status
         UNIQUE_ID=on: mod_unique_id
         USERDIR=on: mod_userdir
         USERTRACK=on: mod_usertrack
         VHOST_ALIAS=on: mod_vhost_alias
         FILTER=on: mod_filter
         SUBSTITUTE=off: mod_substitute
         VERSION=on: mod_version
         SSL=on: mod_ssl
         SUEXEC=off: mod_suexec
         SUEXEC_RSRCLIMIT=off: suEXEC rlimits based on login class
         SUEXEC_USERDIR=off: suEXEC UserDir support
         REQTIMEOUT=on: mod_reqtimeout
         PROXY=off: mod_proxy
         IPV4_MAPPED=off: Allow IPv6 socket to handle IPv4
         BUCKETEER=off: mod_bucketeer
         CASE_FILTER=off: mod_case_filter
         CASE_FILTER_IN=off: mod_case_filter_in
         EXT_FILTER=off: mod_ext_filter
         LOG_FORENSIC=off: mod_log_forensic
         OPTIONAL_HOOK_EXPORT=off: mod_optional_hook_export
         OPTIONAL_HOOK_IMPORT=off: mod_optional_hook_import
         OPTIONAL_FN_IMPORT=off: mod_optional_fn_import
         OPTIONAL_FN_EXPORT=off: mod_optional_fn_export
    ====> mod_proxy: you have to choose at least one of them
         PROXY_AJP=off: mod_proxy_ajp
         PROXY_BALANCER=off: mod_proxy_balancer
         PROXY_CONNECT=off: mod_proxy_connect
         PROXY_FTP=off: mod_proxy_ftp
         PROXY_HTTP=off: mod_proxy_http
         PROXY_SCGI=off: mod_proxy_scgi
    ===> Use 'make config' to modify these settings


Then I installed PHP 5.3:

    moxz:/>cd /usr/ports/lang/php53
    moxz:/usr/ports/lang/php53>sudo make install clean


Here is the configuration, I used for that:

    moxz:/usr/ports/lang/php53>make showconfig
    ===> The following configuration options are available for php53-5.3.28:
         AP2FILTER=off: Use Apache 2.x filter interface (experimental)
         APACHE=on: Build Apache module
         CGI=on: Build CGI version
         CLI=on: Build CLI version
         DEBUG=off: Build with debugging support
         FPM=off: Build FPM version (experimental)
         IPV6=off: IPv6 protocol support
         LINKTHR=on: Link thread lib (for threaded extensions)
         MAILHEAD=off: mail header patch
         MULTIBYTE=off: zend multibyte support
         SUHOSIN=off: Suhosin protection system
    ===> Use 'make config' to modify these settings


And lastly I compiled the php extensions:

    moxz:~>cd /usr/ports/lang/php53-extensions
    moxz:/usr/ports/lang/php53-extensions>sudo make install clean


Here are the configurations for that:

    moxz:/usr/ports/lang/php53-extensions>make showconfig
    ===> The following configuration options are available for php53-extensions-1.6:
         BCMATH=off: bc style precision math functions
         BZ2=off: bzip2 library support
         CALENDAR=off: calendar conversion support
         CTYPE=on: ctype functions
         CURL=off: CURL support
         DBA=off: dba support
         DOM=on: DOM support
         EXIF=off: EXIF support
         FILEINFO=off: fileinfo support
         FILTER=on: input filter support
         FTP=off: FTP support
         GD=off: GD library support
         GETTEXT=off: gettext library support
         GMP=off: GNU MP support
         HASH=on: HASH Message Digest Framework
         ICONV=on: iconv support
         IMAP=off: IMAP support
         INTERBASE=off: Interbase 6 database support (Firebird)
         JSON=on: JavaScript Object Serialization support
         LDAP=off: OpenLDAP support
         MBSTRING=off: multibyte string support
         MCRYPT=off: Encryption support
         MSSQL=off: MS-SQL database support
         MYSQL=on: MySQL database support
         MYSQLI=off: MySQLi database support
         ODBC=off: ODBC support
         OPENSSL=on: OpenSSL support
         PCNTL=off: pcntl support (CLI only)
         PDF=off: PDFlib support (implies GD)
         PDO=on: PHP Data Objects Interface (PDO)
         PDO_MYSQL=on: PDO MySQL driver
         PDO_PGSQL=off: PDO PostgreSQL driver
         PDO_SQLITE=off: PDO sqlite driver
         PGSQL=off: PostgreSQL database support
         PHAR=on: phar support
         POSIX=on: POSIX-like functions
         PSPELL=off: pspell support
         READLINE=off: readline support (CLI only)
         RECODE=off: recode support
         SESSION=on: session support
         SHMOP=off: shmop support
         SIMPLEXML=on: simplexml support
         SNMP=off: SNMP support
         SOAP=off: SOAP support
         SOCKETS=off: sockets support
         SQLITE=off: sqlite support
         SQLITE3=off: sqlite3 support
         SYBASE_CT=off: Sybase database support
         SYSVMSG=off: System V message support
         SYSVSEM=off: System V semaphore support
         SYSVSHM=off: System V shared memory support
         TIDY=off: TIDY support
         TOKENIZER=on: tokenizer support
         WDDX=off: WDDX support (implies XML)
         XML=on: XML support
         XMLREADER=on: XMLReader support
         XMLRPC=off: XMLRPC-EPI support
         XMLWRITER=on: XMLWriter support
         XSL=off: XSL support (Implies DOM)
         ZIP=off: ZIP support
         ZLIB=off: ZLIB support
    ===> Use 'make config' to modify these settings


I chose the extensions that were described [here](http://la-samhna.de/beltane/beltane_help/installing.html#REQUIREMENTS):

> PHP 4.3 or later, compiled either as apache module, or as CGI program. Your PHP4 must have support for:
>
> *   XML parser functions,
> *   POSIX funtions (note that on SLES 10, these are in a seperate 'php-posix' rpm), and
> *   either MySQL, PostgreSQL, or Oracle, depending on which database you are using.

On top of that I also enabled sessions since it actually uses that. Also make sure PHP is enabled on the **apache** side:

    moxz:~>grep -i php /usr/local/etc/apache22/httpd.conf
    LoadModule php5_module        libexec/apache22/libphp5.so
        DirectoryIndex index.html index.php
        AddType application/x-httpd-php .php
        AddType application/x-httpd-php-source .phps


Then enable the apache service, this is done by adding the following to the **/etc/rc.conf** file:

    apache22_enable="YES"


Then you can start the service by running the following

    moxz:~>sudo service apache22 start


### Install Beltane

This was is pretty easy. Grab the source:

    moxz:/opt/work>fetch http://la-samhna.de/beltane/beltane-1.0.19.tar.gz
    beltane-1.0.19.tar.gz                         100% of  184 kB  150 kBps 00m02s


Then extract it:

    moxz:/opt/work>tar xzf beltane-1.0.19.tar.gz


then go ahead and configure it:

    moxz:/opt/work/beltane-1.0.19>./configure --prefix=/usr/local/beltane --enable-mod-php --with-user=elatov --with-data-dir=/usr/local/yule/var/lib/yule --with-php-dir=/usr/local/beltane/php --with-logfile=/usr/local/beltane/log --with-user-home=/usr/local/beltane --with-php-extension=php


After the configure was done, I saw the following summary:

     beltane has been configured as follows:
               PHP files: /usr/local/beltane/php
         System binaries: /usr/local/beltane/bin
      Configuration file: /usr/local/beltane/.beltanerc
                Log file: /usr/local/beltane/log
                    Data: /usr/local/yule/var/lib/yule
                PHP user: elatov
               PHP group: elatov
          Home directory: /usr/local/beltane
      PHP file extension: php
           PHP is module: yes
               XOR value: 0


I then created the directory and installed it:

    moxz:/opt/work/l/beltane-1.0.19>sudo mkdir /usr/local/beltane
    moxz:/opt/work/l/beltane-1.0.19>sudo chown elatov:elatov /usr/local/beltane/
    moxz:/opt/work/l/beltane-1.0.19>make install


After that I created a configuration for beltane in apache, here is how it looked like:

    moxz:~>cat /usr/local/etc/apache22/Includes/beltane.conf
    <Directory /usr/local/beltane/php/>
        AllowOverride None
        Options +ExecCGI -Includes
    </Directory>


Then tested the config:

    moxz:~>sudo service apache22 configtest
    Performing sanity check on apache22 configuration:
    Syntax OK


and restarted apache:

    moxz:~>sudo service apache22 restart
    Performing sanity check on apache22 configuration:
    Syntax OK
    Stopping apache22.
    Waiting for PIDS: 7495.
    Performing sanity check on apache22 configuration:
    Syntax OK
    Starting apache22.


#### Beltane Permissions

There is a pretty good description [here](http://la-samhna.de/beltane/beltane_help/installing.html#PERMISSIONS) on what permissions are necessary:

> **Webserver access to beltane**
>
> As you have installed the beltane PHP scripts into some directory DIR (configure option -with-php-dir=DIR), you should make sure that the webserver has read access to this directory and everything below it
>
>     bash$ chown -R root   DIR
>     bash$ chmod -R 555    DIR
>
>
> **Access to the yule data directory for user beltane**
>
> For security, we do not give the webserver access to the data directory, but transfer privileges by making the beltane helper applications SUID/SGID beltane/samhain. Accordingly, user 'beltane' needs read/write access, and group 'samhain' (yule) needs read access.
>
>     bash$ chown beltane:samhain   /var/lib/yule
>     bash$ chown beltane:samhain   /var/lib/yule/rc.*
>     bash$ chown beltane:samhain   /var/lib/yule/file.*
>
>
> **Access to the yule HTML status file**
>
> This file is only re-written by yule, so yule will not change the permissions. It needs to be readable from PHP (i.e. for user 'www' in our example).
>
>     bash$ chmod 644 /var/log/yule/yule.html
>
>
> **Access to the database of installed clients**
>
> This is the XML format database of installed clients. It can be created through the beltane interface, but if you are using the samhain deployment system, it is created and maintained automatically by that system.
>
>     bash$ chown beltane /var/lib/yule/profiles
>     bash$ chmod 755     /var/lib/yule/profiles
>     bash$ chown www:samhain /var/lib/yule/profiles/yulerc.install.db
>     bash$ chmod 660         /var/lib/yule/profiles/yulerc.install.db
>
>
> Set helper applications SUID/SGID beltane/samhain
>
>     bash$ chown beltane:samhain /usr/local/bin/beltane_*
>     bash$ chmod 6755            /usr/local/bin/beltane_*
>

I was being impatient, so I gave my apache user access to beltane and yule directories:

    moxz:~>ls -ld /usr/local/{beltane,yule,samhain}
    drwxrwxr-x  4 elatov  www     512 Mar 16 10:13 /usr/local/beltane
    drwxr-xr-x  6 elatov  elatov  512 Mar  9 15:17 /usr/local/samhain
    drwxrwxr-x  6 elatov  www     512 Mar  9 14:35 /usr/local/yule

    moxz:~>ls -l /usr/local/beltane/bin/
    total 52
    -rwsrwsr-x  1 www  elatov  11280 Mar  9 15:43 beltane_cp
    -rwsrwsr-x  1 www  elatov  38088 Mar  9 15:43 beltane_update


I will have to revisit this later on (this is just for home anyways).

#### Configuring Beltane

At this point we should be able to login to beltane. So go **http://moxz/php** and you should see the following:

![beltane login page Install Samhain with Beltane on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2014/03/beltane-login-page.png)

You can login with:

> user: rainer
> passwd: wichmann

At first it won't show anything, since it can't connect to the MySQL database, so click **configure** on the top left corner and update the settings:

![samhain configure mysql db 1024x751 Install Samhain with Beltane on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2014/03/samhain-configure-mysql-db-1024x751.png)

After that you should see some of the logs:

![beltane alert 1024x336 Install Samhain with Beltane on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2014/03/beltane-alert-1024x336.png)

As a test I created a new file and made sure the event was in Beltane:

![test create file 1024x615 Install Samhain with Beltane on FreeBSD](http://virtuallyhyper.com/wp-content/uploads/2014/03/test-create-file-1024x615.png)

Notice you can either **acknowledge** the alarm (this is why beltane needs **update** permission to the MySQL DB) or you can **update** the signature of the file (appropriate permissions for **/usr/local/beltane/bin/beltane_update** are necessary).

The "Beltane I" UI is a little slow and the "Beltane II" project looks a little better, hopefully I will have a chance to try it out soon.

