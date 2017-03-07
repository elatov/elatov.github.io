---
published: true
layout: post
title: "Compile OpenVAS 7 on CentOS 6"
author: Karim Elatov
categories: [os,security]
tags: [linux,openvas,centos]
---
After updating OpenVAS from the atomic YUM repository, I realized I wasn't able to launch Greenbone Security Assistant (**gsad**). The issue is discussed [here](http://osdir.com/ml/openvas-security-network/2014-06/msg00078.html). Upon starting the service I saw the following error:

    Starting greenbone-security-assistant: /usr/sbin/gsad: error while loading shared libraries: libgnutls.so.28:
    cannot open shared object file: No such file or directory

The above could be fixed with the following:

    echo "/opt/atomic/atomic-gnutls3/root/usr/lib64 > /etc/ld.so.conf.d/gnutls3.conf"

But then that caused another issue, so I decided to compile my own version.

### OpenVAS 7 Architecture

I talked about the architecture for OpenVAS 6 in my [previous post](/2014/05/openvas-centos/), but it seems that it has changed, from [this](http://www.openvas.org/about.html) OpenVAS page:

![openvas7-arch](https://seacloud.cc/d/480b5e8fcd/files/?p=/openvas7-compile/openvas7-arch.png&raw=1)

Notice that the *administrator* is no longer part of the deployment, that got merged into the *manager*. From "[Install OpenVAS from Source Code](http://www.openvas.org/install-source.html)":

> {:.kt}
> | OpenVAS-5| OpenVAS-6 | OpenVAS-7|
> |:---------------|:--------------|:---------------|
> |Libraries 5.0.4 |Libraries 6.0.2| Libraries 7.0.2|
> |Scanner 3.3.1   |Scanner 3.4.1  |Scanner 4.0.1   |
> |Manager 3.0.7   |Manager 4.0.5  |Manager 5.0.2   |
> |Administrator 1.2.2 | Administrator 1.3.2| Merged into Manager|
> |Greenbone Security Assistant (GSA) 3.0.3 | Greenbone Security Assistant (GSA) 4.0.2 | Greenbone Security Assistant (GSA) 5.0.1|
> | Greenbone Security Desktop (GSD) 1.2.2 | Greenbone Security Desktop (GSD) 1.2.2| *) Not supported anymore| 
> | Commandline Interface (CLI) 1.1.5 | Commandline Interface (CLI) 1.2.0 | Commandline Interface (CLI) 1.3.0 |

### Compile OpenVAS Libraries

So let's try this out. First get the source:

    elatov@m2:/opt/work$wget http://wald.intevation.org/frs/download.php/1671/openvas-libraries-7.0.2.tar.gz
    elatov@m2:/opt/work$tar xzf openvas-libraries-7.0.2.tar.gz
    elatov@m2:/opt/work$cd openvas-libraries-7.0.2/
    
Looking over the **INSTALL** file, here were the prerequites:

> General build environment:
> 
> * a C compiler (e.g. gcc)
> * bison
> * flex
> * cmake
> * pkg-config
> 
> Specific development libraries:
> 
> * libglib >= 2.16
> * libgnutls >= 2.8
> * zlib
> * libpcap
> * libgpgme >= 1.1.2
> * uuid-dev (from e2fsprogs)
> 
> Prerequisites for building documentation:
> 
> * doxygen
> * xmltoman (optional, for building man page)
> * sqlfairy (optional, for producing database diagram)
> 
> Recommended to have WMI support:
> 
> * wmiclient library (see doc/wmi-howto.txt)
> 
> Recommended to have improved SSH support:
> 
> * libssh >= 0.5.0
> 
> Recommended to have improved SSL support:
> 
> * libksba >= 1.0.7
> 
> Recommended to have LDAP support:
> 
> * libldap >= 2.4.11
>   (LDAP can be disabled with -DBUILD_WITHOUT_LDAP=1)

So let's get the prerequisites first:

    elatov@m2:~$sudo yum install gcc bison flex cmake28 pkgconfig glib2-devel gnutls-devel libpcap-devel gpgme-devel libuuid-devel doxygen libksba-devel

Now to prepare the source:

    elatov@m2:/opt/work/openvas-libraries-7.0.2$mkdir build
    elatov@m2:/opt/work/openvas-libraries-7.0.2$cd build
    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Libraries...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/cc
    -- Check for working C compiler: /usr/bin/cc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 2.8.5
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.26.1
    -- checking for module 'wmiclient>=1.3.14'
    --   package 'wmiclient>=1.3.14' not found
    -- checking for module 'wincmd>=0.80'
    --   package 'wincmd>=0.80' not found
    -- checking for module 'libssh>=0.5.0'
    --   package 'libssh>=0.5.0' not found
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Looking for pcap-config...
    -- Looking for pcap-config... /usr/bin/pcap-config
    -- Looking for gpgme...
    -- Looking for gpgme... /usr/lib64/libgpgme.so
    -- Looking for ksba...
    -- Looking for ksba... /usr/lib64/libksba.so
    -- Looking for zlib...
    -- Looking for zlib... /usr/lib64/libz.so
    -- Looking for uuid...
    -- Looking for uuid... /usr/lib64/libuuid.so
    -- Looking for libldap...
    --   No ldap library found - ldap support disabled
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-libraries-7.0.2/buil

When I tried to build the software I ran into the following error:

    [ 28%] Building C object misc/CMakeFiles/openvas_misc_shared.dir/openvas_server.c.o
    /opt/work/openvas-libraries-7.0.2/misc/openvas_server.c:227: error: expected declaration specifiers or ‘...’ before ‘gnutls_retr2_st’
    /opt/work/openvas-libraries-7.0.2/misc/openvas_server.c: In function ‘client_cert_callback’:
    /opt/work/openvas-libraries-7.0.2/misc/openvas_server.c:239: error: ‘st’ undeclared (first use in this function)
    /opt/work/openvas-libraries-7.0.2/misc/openvas_server.c:239: error: (Each undeclared identifier is reported only once
    
Looks like it didn't like the **gnutls** defined object. So I decided to install my own version of **gnutls**. 

#### Compile gnutls
First let's remove the previous installed *devel* package:

    elatov@m2:~$sudo yum remove gnutls-devel
    
Now let's get the source:

	elatov@m2:/opt/work$wget ftp://ftp.gnutls.org/gcrypt/gnutls/v3.2/gnutls-3.2.14.tar.xz
	elatov@m2:/opt/work$tar xJvf gnutls-3.2.14.tar.xz
	elatov@m2:/opt/work$cd gnutls-3.2.14/

From the **README**, looks like we need the following for gnutls:

> The library depends on libnettle and gmplib.
> 
>  * gmplib: for big number arithmetic
>      http://gmplib.org/
>      
>  * nettle: for cryptographic algorithms
>      http://www.lysator.liu.se/~nisse/nettle/

**gmp** was part of the base YUM repo, so let's install that:

    elatov@m2:~$sudo yum install gmp-devel

Now let's compile **nettle**:

    elatov@m2:/opt/work$wget http://ftp.gnu.org/gnu/nettle/nettle-2.7.tar.gz
    elatov@m2:/opt/work$tar xvzf nettle-2.7.tar.gz
    elatov@m2:/opt/work$cd nettle-2.7/

Now to prepare the source:

    elatov@m2:/opt/work/nettle-2.7$export CC="gcc -Wl,-rpath,/usr/local/openvas/lib64"
    elatov@m2:/opt/work/nettle-2.7$./configure --prefix=/usr/local/openvas
    ...
    ...
    configure: summary of build options:
    
      Version:           nettle 2.7
      Host type:         x86_64-unknown-linux-gnu
      ABI:               64
      Assembly files:    x86_64
      Install prefix:    /usr/local/openvas
      Library directory: ${exec_prefix}/lib64
      Compiler:          gcc -Wl,-rpath,/usr/local/openvas/lib64
      Static libraries:  yes
      Shared libraries:  yes
      Public key crypto: yes
      Documentation:     no      

To install run the following:

    elatov@m2:/opt/work/nettle-2.7$make && make install

After that you can check the version of **nettle**:

    elatov@m2:/opt/work/nettle-2.7$/usr/local/openvas/bin/nettle-hash --version
    nettle-hash (nettle 2.7)

Now back to **gnutls**:

    elatov@m2:/opt/work/gnutls-3.2.14$export PKG_CONFIG_PATH=/usr/local/openvas/lib64/pkgconfig
    elatov@m2:/opt/work/gnutls-3.2.14$export CC="gcc -Wl,-rpath,/usr/local/openvas/lib64"
    elatov@m2:/opt/work/gnutls-3.2.14$./configure --prefix=/usr/local/openvas
    ..
    ..
    configure: summary of build options:
    
      version:              3.2.14 shared 58:5:30
      Host/Target system:   x86_64-unknown-linux-gnu
      Build system:         x86_64-unknown-linux-gnu
      Install prefix:       /usr/local/openvas
      Compiler:             gcc -Wl,-rpath,/usr/local/openvas/lib64
      CFlags:               -g -O2
      Library types:        Shared=yes, Static=yes
      Local libopts:        yes
      Local libtasn1:       yes
      Use nettle-mini:      no
    
    configure: External hardware support:
    
      /dev/crypto:          no
      Hardware accel:       x86-64
      PKCS#11 support:      no
      TPM support:          no
    
    configure: Optional features:
    (note that included applications might not compile properly
    if features are disabled)
    
      DTLS-SRTP support:    yes
      ALPN support:         yes
      OCSP support:         yes
      OpenPGP support:      yes
      SRP support:          yes
      PSK support:          yes
      DHE support:          yes
      ECDHE support:        yes
      Anon auth support:    yes
      Heartbeat support:    yes
      Unicode support:      yes
      Non-SuiteB curves:    yes
    
    configure: Optional applications:
    
      crywrap app:          yes
    
    configure: Optional libraries:
    
      Guile wrappers:       no
      C++ library:          yes
      DANE library:         no
      OpenSSL compat:       yes
    
    configure: System files:
    
      Trust store pkcs11:
      Trust store file:     /etc/pki/tls/cert.pem
      Blacklist file:
      CRL file:
      DNSSEC root key file: /etc/unbound/root.key
      
And now to build and install the software:

    elatov@m2:/opt/work/gnutls-3.2.14$make && make install
    
Now rebuild **openvas-libraries**:

    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$export PKG_CONFIG_PATH=/usr/local/openvas/lib/pkgconfig:$PKG_CONFIG_PATH
    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$export CFGLAGS='-L/usr/local/openvas/lib -I/usr/local/openvas/include'
    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$rm -rf *
    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Libraries...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.26.1
    -- checking for module 'wmiclient>=1.3.14'
    --   package 'wmiclient>=1.3.14' not found
    -- checking for module 'wincmd>=0.80'
    --   package 'wincmd>=0.80' not found
    -- checking for module 'libssh>=0.5.0'
    --   package 'libssh>=0.5.0' not found
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Looking for pcap-config...
    -- Looking for pcap-config... /usr/bin/pcap-config
    -- Looking for gpgme...
    -- Looking for gpgme... /usr/lib64/libgpgme.so
    -- Looking for ksba...
    -- Looking for ksba... /usr/lib64/libksba.so
    -- Looking for zlib...
    -- Looking for zlib... /usr/lib64/libz.so
    -- Looking for uuid...
    -- Looking for uuid... /usr/lib64/libuuid.so
    -- Looking for libldap...
    --   No ldap library found - ldap support disabled
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-libraries-7.0.2/build

Notice this time around it picked a new version of gnutls (`found gnutls, version 3.2.14`). 

And the **make** finished without issues:

    elatov@m2:/opt/work/openvas-libraries-7.0.2/build$make
    ...
    ...
    Linking C shared library libopenvas_nasl.so
    [ 95%] Built target openvas_nasl_shared
    Scanning dependencies of target openvas-nasl
    [ 96%] Building C object nasl/CMakeFiles/openvas-nasl.dir/nasl.c.o
    Linking C executable openvas-nasl
    [ 96%] Built target openvas-nasl
    Scanning dependencies of target openvas-nasl-lint
    [ 97%] Building C object nasl/CMakeFiles/openvas-nasl-lint.dir/nasl-lint.c.o
    Linking C executable openvas-nasl-lint
    [ 97%] Built target openvas-nasl-lint
    Scanning dependencies of target openvas_omp_shared
    [ 98%] Building C object omp/CMakeFiles/openvas_omp_shared.dir/xml.c.o
    [100%] Building C object omp/CMakeFiles/openvas_omp_shared.dir/omp.c.o
    Linking C shared library libopenvas_omp.so
    [100%] Built target openvas_omp_shared
    
To make sure all the libraries as linked appropriately run the following as a precaution:

    elatov@m2:/usr/local/openvas$find {bin,lib,lib64} -executable \! -type d -print -exec ldd {} \;  | grep -i found
    
If anything is returned check out the library to find which one is not linked appropriately. You can also run this to check for libraries that are not executable:

    elatov@m2:/usr/local/openvas$find . -name "*.so" -exec ldd {} \; | grep found
    ldd: warning: you do not have execution permission for `./lib64/libhogweed.so'
    ldd: warning: you do not have execution permission for `./lib64/libnettle.so'
    
### Compile OpenVAS Scanner
Get the source:

    elatov@m2:/opt/work$wget http://wald.intevation.org/frs/download.php/1640/openvas-scanner-4.0.1.tar.gz
    elatov@m2:/opt/work$tar xzvf openvas-scanner-4.0.1.tar.gz
    elatov@m2:/opt/work$cd openvas-scanner-4.0.1/
    
Prepare the source:

    elatov@m2:/opt/work/openvas-scanner-4.0.1$mkdir build
    elatov@m2:/opt/work/openvas-scanner-4.0.1$cd build
    elatov@m2:/opt/work/openvas-scanner-4.0.1/build$export CC='gcc -Wl,-rpath,/usr/local/openvas/lib64 -Wl,-rpath,/usr/local/openvas/lib'
    elatov@m2:/opt/work/openvas-scanner-4.0.1/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Scanner...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'libopenvas>=7.0.0'
    --   found libopenvas, version 7.0.2
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.26.1
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-scanner-4.0.1/build
    
The **make install** went through without issues:

    elatov@m2:/opt/work/openvas-scanner-4.0.1/build$make
    Scanning dependencies of target openvassd
    [  5%] Building C object src/CMakeFiles/openvassd.dir/attack.c.o
    [ 10%] Building C object src/CMakeFiles/openvassd.dir/comm.c.o
    [ 15%] Building C object src/CMakeFiles/openvassd.dir/hosts.c.o
    [ 21%] Building C object src/CMakeFiles/openvassd.dir/locks.c.o
    [ 26%] Building C object src/CMakeFiles/openvassd.dir/log.c.o
    [ 31%] Building C object src/CMakeFiles/openvassd.dir/nasl_plugins.c.o
    [ 36%] Building C object src/CMakeFiles/openvassd.dir/ntp.c.o
    [ 42%] Building C object src/CMakeFiles/openvassd.dir/openvassd.c.o
    [ 47%] Building C object src/CMakeFiles/openvassd.dir/otp.c.o
    [ 52%] Building C object src/CMakeFiles/openvassd.dir/piic.c.o
    [ 57%] Building C object src/CMakeFiles/openvassd.dir/pluginlaunch.c.o
    [ 63%] Building C object src/CMakeFiles/openvassd.dir/pluginload.c.o
    [ 68%] Building C object src/CMakeFiles/openvassd.dir/pluginscheduler.c.o
    [ 73%] Building C object src/CMakeFiles/openvassd.dir/plugs_req.c.o
    [ 78%] Building C object src/CMakeFiles/openvassd.dir/preferences.c.o
    [ 84%] Building C object src/CMakeFiles/openvassd.dir/processes.c.o
    [ 89%] Building C object src/CMakeFiles/openvassd.dir/save_kb.c.o
    [ 94%] Building C object src/CMakeFiles/openvassd.dir/sighand.c.o
    [100%] Building C object src/CMakeFiles/openvassd.dir/utils.c.o
    Linking C executable openvassd
    [100%] Built target openvassd
    elatov@m2:/opt/work/openvas-scanner-4.0.1/build$make install
    [100%] Built target openvassd
    Install the project...
    -- Install configuration: "Debug"
    -- Installing: /usr/local/openvas/sbin/openvassd
    -- Installing: /usr/local/openvas/sbin/openvas-mkcert
    -- Installing: /usr/local/openvas/sbin/openvas-mkcert-client
    -- Installing: /usr/local/openvas/sbin/openvas-nvt-sync
    -- Installing: /usr/local/openvas/sbin/greenbone-nvt-sync
    -- Installing: /usr/local/openvas/share/man/man8/openvassd.8
    -- Installing: /usr/local/openvas/share/man/man8/openvas-mkcert.8
    -- Installing: /usr/local/openvas/share/man/man8/openvas-nvt-sync.8
    -- Installing: /usr/local/openvas/share/man/man8/greenbone-nvt-sync.8
    -- Installing: /usr/local/openvas/var/lib/openvas/plugins
    -- Installing: /usr/local/openvas/var/cache/openvas

### Compile OpenVAS Manager
Get the source:

    elatov@m2:/opt/work$wget wget http://wald.intevation.org/frs/download.php/1667/openvas-manager-5.0.2.tar.gz
    elatov@m2:/opt/work$tar xzf openvas-manager-5.0.2.tar.gz
    elatov@m2:/opt/work$cd openvas-manager-5.0.2/
    
Now let's prepare the source:

    elatov@m2:/opt/work/openvas-manager-5.0.2$export CC='gcc -Wl,-rpath,/usr/local/openvas/lib64 -Wl,-rpath,/usr/local/openvas/lib'
    elatov@m2:/opt/work/openvas-manager-5.0.2$export PKG_CONFIG_PATH=/usr/local/openvas/lib/pkgconfig:/usr/local/openvas/lib64/pkgconfig
    elatov@m2:/opt/work/openvas-manager-5.0.2$export CFLAGS="-I/usr/local/openvas/include"
    elatov@m2:/opt/work/openvas-manager-5.0.2$mkdir build
    elatov@m2:/opt/work/openvas-manager-5.0.2$cd build

For this one we also need **sqlite3**, so let's install that:

    elatov@m2:~$sudo yum install sqlite-devel

And finally for the **cmake**:

    elatov@m2:/opt/work/openvas-manager-5.0.2/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Manager...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'libopenvas>=7.0.1'
    --   found libopenvas, version 7.0.2
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.26.1
    -- checking for module 'sqlite3'
    --   found sqlite3, version 3.6.20
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Looking for gpgme...
    -- Looking for gpgme... /usr/lib64/libgpgme.so
    -- Looking for xmltoman...
    -- Looking for xmltoman... XMLTOMAN_EXECUTABLE-NOTFOUND
    -- Looking for xmlmantohtml... XMLMANTOHTML_EXECUTABLE-NOTFOUND
    -- Looking for SQLFairy...
    -- Looking for SQLFairy... SQLT-DIAGRAM_EXECUTABLE-NOTFOUND, SQLT_EXECUTABLE-NOTFOUND
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- WARNING: xmltoman is required to generate manpage.
    -- WARNING: xmlmantohtml is required for manpage in HTML docs.
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-manager-5.0.2/build
    
Upon trying to build the software, I ran into this error:

    [ 55%] Building C object src/CMakeFiles/manage.dir/manage_config_system_discovery.c.o
    [ 60%] Building C object src/CMakeFiles/manage.dir/manage_sql.c.o
    /opt/work/openvas-manager-5.0.2/src/manage_sql.c: In function ‘init_manage_process’:
    /opt/work/openvas-manager-5.0.2/src/manage_sql.c:8853: error: ‘SQLITE_FCNTL_CHUNK_SIZE’ undeclared (first use in this function)
    /opt/work/openvas-manager-5.0.2/src/manage_sql.c:8853: error: (Each undeclared identifier is reported only once
    /opt/work/openvas-manager-5.0.2/src/manage_sql.c:8853: error: for each function it appears in.)
    make[2]: *** [src/CMakeFiles/manage.dir/manage_sql.c.o] Error 1
    make[1]: *** [src/CMakeFiles/manage.dir/all] Error 2
    make: *** [all] Error 2
    
So I removed the **sqlite-devel** package from yum and compiled my own version:

    elatov@m2:~$sudo yum remove sqlite-devel
    
Now for the source:

    elatov@m2:/opt/work$wget http://www.sqlite.org/2014/sqlite-autoconf-3080500.tar.gz
    elatov@m2:/opt/work$tar xzf sqlite-autoconf-3080500.tar.gz
    elatov@m2:/opt/work$cd sqlite-autoconf-3080500/
    elatov@m2:/opt/work/sqlite-autoconf-3080500$./configure --prefix=/usr/local/openvas

The build and install went through without issues:

    elatov@m2:/opt/work/sqlite-autoconf-3080500$make && make install

Now back to the manager:

    elatov@m2:/opt/work/openvas-manager-5.0.2/build$rm -rf *
    elatov@m2:/opt/work/openvas-manager-5.0.2/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Manager...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'libopenvas>=7.0.1'
    --   found libopenvas, version 7.0.2
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.26.1
    -- checking for module 'sqlite3'
    --   found sqlite3, version 3.8.5
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Looking for gpgme...
    -- Looking for gpgme... /usr/lib64/libgpgme.so
    -- Looking for xmltoman...
    -- Looking for xmltoman... XMLTOMAN_EXECUTABLE-NOTFOUND
    -- Looking for xmlmantohtml... XMLMANTOHTML_EXECUTABLE-NOTFOUND
    -- Looking for SQLFairy...
    -- Looking for SQLFairy... SQLT-DIAGRAM_EXECUTABLE-NOTFOUND, SQLT_EXECUTABLE-NOTFOUND
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- WARNING: xmltoman is required to generate manpage.
    -- WARNING: xmlmantohtml is required for manpage in HTML docs.
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-manager-5.0.2/build

And now the new version of **sqlite3** is there (`found sqlite3, version 3.8.5`). Then I ran into another compilation issue:

    [ 70%] Building C object src/CMakeFiles/manage.dir/lsc_user.c.o
    [ 75%] Building C object src/CMakeFiles/manage.dir/lsc_crypt.c.o
    Linking C static library libmanage.a
    [ 75%] Built target manage
    Scanning dependencies of target omp
    [ 80%] Building C object src/CMakeFiles/omp.dir/omp.c.o
    cc1: warnings being treated as errors
    /opt/work/openvas-manager-5.0.2/src/omp.c: In function ‘buffer_notes_xml’:
    /opt/work/openvas-manager-5.0.2/src/omp.c:9714: error: implicit declaration of function ‘g_utf8_substring’
    /opt/work/openvas-manager-5.0.2/src/omp.c:9714: error: initialization makes pointer from integer without a cast
    /opt/work/openvas-manager-5.0.2/src/omp.c: In function ‘buffer_overrides_xml’:
    /opt/work/openvas-manager-5.0.2/src/omp.c:9947: error: initialization makes pointer from integer without a cast
    make[2]: *** [src/CMakeFiles/omp.dir/omp.c.o] Error 1
    make[1]: *** [src/CMakeFiles/omp.dir/all] Error 2
    make: *** [all] Error 2
    
This one is related to **glib2**, so let's remove the yum version:

    elatov@m2:~$sudo yum remove glib2-devel

And let's compile **glib2** from source:

    elatov@m2:/opt/work$wget http://ftp.gnome.org/pub/gnome/sources/glib/2.40/glib-2.40.0.tar.xz
    elatov@m2:/opt/work$tar xJf glib-2.40.0.tar.xz
    elatov@m2:/opt/work$cd glib-2.40.0/
    
From the **README** file it looks like we need libffi:

> GObject includes a generic marshaller, g_cclosure_marshal_generic.
>   To use it, simply specify NULL as the marshaller in g_signal_new().
>   The generic marshaller is implemented with libffi, and consequently
>   GObject depends on libffi now.

So let's install that:

    elatov@m2:~$sudo yum install libffi-devel

Now to prepare the source:

    elatov@m2:/opt/work/glib-2.40.0$./configure --prefix=/usr/local/openvas

The build and install went without a hitch:

    elatov@m2:/opt/work/glib-2.40.0$make && make install
    
Now back to the **openvas-manager** source:

    elatov@m2:/opt/work/openvas-manager-5.0.2/build$rm -rf *
    elatov@m2:/opt/work/openvas-manager-5.0.2/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Configuring the Manager...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Install prefix: /usr/local/openvas
    -- checking for module 'libopenvas>=7.0.1'
    --   found libopenvas, version 7.0.2
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.40.0
    -- checking for module 'sqlite3'
    --   found sqlite3, version 3.8.5
    -- Looking for pcap...
    -- Looking for pcap... /usr/lib64/libpcap.so
    -- Looking for gpgme...
    -- Looking for gpgme... /usr/lib64/libgpgme.so
    -- Looking for xmltoman...
    -- Looking for xmltoman... XMLTOMAN_EXECUTABLE-NOTFOUND
    -- Looking for xmlmantohtml... XMLMANTOHTML_EXECUTABLE-NOTFOUND
    -- Looking for SQLFairy...
    -- Looking for SQLFairy... SQLT-DIAGRAM_EXECUTABLE-NOTFOUND, SQLT_EXECUTABLE-NOTFOUND
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- WARNING: xmltoman is required to generate manpage.
    -- WARNING: xmlmantohtml is required for manpage in HTML docs.
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/openvas-manager-5.0.2/build

The new version of **glib2** is there (`found glib-2.0, version 2.40.0`). The compile then went through:

    elatov@m2:/opt/work/openvas-manager-5.0.2/build$make
    ..
    ..
    [ 75%] Building C object src/CMakeFiles/manage.dir/lsc_crypt.c.o
    Linking C static library libmanage.a
    [ 75%] Built target manage
    Scanning dependencies of target omp
    [ 80%] Building C object src/CMakeFiles/omp.dir/omp.c.o
    Linking C static library libomp.a
    [ 80%] Built target omp
    Scanning dependencies of target otp
    [ 85%] Building C object src/CMakeFiles/otp.dir/otp.c.o
    Linking C static library libotp.a
    [ 85%] Built target otp
    Scanning dependencies of target ovas-mngr-comm
    [ 90%] Building C object src/CMakeFiles/ovas-mngr-comm.dir/ovas-mngr-comm.c.o
    Linking C static library libovas-mngr-comm.a
    [ 90%] Built target ovas-mngr-comm
    Scanning dependencies of target openvasmd
    [ 95%] Building C object src/CMakeFiles/openvasmd.dir/openvasmd.c.o
    [100%] Building C object src/CMakeFiles/openvasmd.dir/ompd.c.o
    Linking C executable openvasmd
    [100%] Built target openvasmd
    
And the install was fine as well:

    elatov@m2:/opt/work/openvas-manager-5.0.2/build$make install
    
### Compile Greenbone Security Assistant
As always, let's get the source:

    elatov@m2:/opt/work$wget http://wald.intevation.org/frs/download.php/1675/greenbone-security-assistant-5.0.1.tar.gz
    elatov@m2:/opt/work$tar xzf greenbone-security-assistant-5.0.1.tar.gz
    elatov@m2:/opt/work$cd greenbone-security-assistant-5.0.1/
    
From the **INSTALL** file I saw the following prerequisites:

> Prerequisites:
> 
> * openvas-libraries (>= 7.0.0)
> * gnutls (>= 2.8)
> * cmake
> * glib-2.0 (>= 2.16)
> * libxml
> * libxslt
> * libmicrohttpd (>= 0.9.0)
> * libexslt
> * pkg-config
> * xsltproc

At first I used the **libmicrohttpd** version from yum:

    elatov@m2:~$sudo yum list libmicrohttpd-devel
    [sudo] password for elatov:
    Loaded plugins: fastestmirror, remove-with-leaves
    Loading mirror speeds from cached hostfile
     * atomic: www5.atomicorp.com
     * base: mirrors.loosefoot.com
     * epel: mirror.steadfast.net
     * extras: mirror.fdcservers.net
     * rpmfusion-free-updates: mirrors.tummy.com
     * rpmfusion-nonfree-updates: mirror.nexcess.net
     * updates: mirror.spro.net
    Available Packages
    libmicrohttpd-devel.i686                      0.9.22-1.el6                    epel
    libmicrohttpd-devel.x86_64                    0.9.22-1.el6                    epel
    
But I ran into the following warnings in the logs:

	MHD: Failed to receive data: The TLS connection was non-properly terminated.

So then I compiled **libmicrohttpd** from source:

    elatov@m2:/opt/work$wget http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.36.tar.gz
    elatov@m2:/opt/work$tar xzf libmicrohttpd-0.9.36.tar.gz
    elatov@m2:/opt/work$cd libmicrohttpd-0.9.36/

Now let's prepare the source:

    elatov@m2:/opt/work/libmicrohttpd-0.9.36$./configure --prefix=/usr/local/openvas --with-gnutls=/usr/local/openvas
    ..
    ..
    configure: Configuration Summary:
      Operating System:  linux-gnu
      Threading lib:     posix
      libcurl (testing): yes
      Target directory:  /usr/local/openvas
      Messages:          yes
      Basic auth.:       yes
      Digest auth.:      yes
      Postproc:          yes
      HTTPS support:     yes (using libgnutls and libgcrypt)
      epoll support:     yes
      build docs:        yes
      build examples:    yes
      libmicrospdy:      yes
      spdylay (testing): no
      
The build and install didn't have any errors pop up:

    elatov@m2:/opt/work/libmicrohttpd-0.9.36$make && make install
    
The other prerequites can be installed with the following:

    elatov@m2:~$sudo yum install libxslt-devel libxml2-devel
    
Now back to **gsad**:

    elatov@m2:/opt/work/greenbone-security-assistant-5.0.1$mkdir build
    elatov@m2:/opt/work/greenbone-security-assistant-5.0.1$cd build
    elatov@m2:/opt/work/greenbone-security-assistant-5.0.1/build$cmake -DCMAKE_INSTALL_PREFIX=/usr/local/openvas -DCMAKE_INSTALL_RPATH=/usr/local/openvas/lib ..
    -- Found PkgConfig: /usr/bin/pkg-config (found version "0.23")
    -- Configuring greenbone-security-assistant...
    -- The C compiler identification is GNU 4.4.7
    -- Check for working C compiler: /usr/bin/gcc
    -- Check for working C compiler: /usr/bin/gcc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Looking for pkg-config... /usr/bin/pkg-config
    -- checking for module 'libmicrohttpd>=0.9.0'
    --   found libmicrohttpd, version 0.9.36
    -- checking for module 'libxml-2.0'
    --   found libxml-2.0, version 2.7.6
    -- checking for module 'glib-2.0>=2.16'
    --   found glib-2.0, version 2.40.0
    -- checking for module 'libexslt'
    --   found libexslt, version 0.8.15
    -- checking for module 'libopenvas>=7.0.0'
    --   found libopenvas, version 7.0.2
    -- checking for module 'libxslt'
    --   found libxslt, version 1.1.26
    -- checking for module 'gnutls>=2.8'
    --   found gnutls, version 3.2.14
    -- Looking for libgcrypt...
    -- Looking for libgcrypt... /usr/lib64/libgcrypt.so
    -- Install prefix: /usr/local/openvas
    -- External XSL transformations, with xsltproc.
    -- Found Doxygen: /usr/bin/doxygen (found version "1.6.1")
    -- Looking for xmltoman...
    -- Looking for xmltoman... XMLTOMAN_EXECUTABLE-NOTFOUND
    -- Looking for xmlmantohtml... XMLMANTOHTML_EXECUTABLE-NOTFOUND
    -- WARNING: xmltoman is required to generate manpage.
    -- WARNING: xmlmantohtml is required for manpage in HTML docs.
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /opt/work/greenbone-security-assistant-5.0.1/build

The **libmicrohttpd**, **glib2**, and **gnutls** versions look good. After that the build and install worked fine:

    elatov@m2:/opt/work/greenbone-security-assistant-5.0.1/build$make && make install
    
### Post Install Configuration for OpenVAS 7
There are a couple of steps after you have the software installed.

#### Generate SSL Certs for OpenVAS 

    sudo /usr/local/openvas/sbin/openvas-mkcert

#### Download NVTs
The script (**/usr/local/openvas/sbin/openvas-nvt-sync**) looks for the default **openvassd** binary, so before running the script I modified it and pointed it to the correct location:

    OPENVASSD=/usr/local/openvas/sbin/openvassd
    NVT_DIR=`/usr/local/openvas/sbin/openvassd -s | awk -F" = " '/^plugins_folder/ { print $2 }'`

Then you can run the script:

    sudo /usr/local/openvas/sbin/openvas-nvt-sync
    ...
    ...
    zope_zclass.nasl
    zope_zclass.nasl.asc
    zyxel_http_pwd.nasl
    zyxel_http_pwd.nasl.asc
    zyxel_pwd.nasl
    zyxel_pwd.nasl.asc
    [i] Download complete
    [i] Checking dir: ok
    [i] Checking MD5 checksum: ok

#### Let the Scanner process the NVTs
Here is process for that:

    elatov@m2:~$sudo /usr/local/openvas/sbin/openvassd
    elatov@m2:~$ps -eaf | grep open
    root     12163     1 47 14:52 ?        00:00:03 openvassd: Reloaded 1050 of 35241 NVTs (2% / ETA: 03:15)
    root     12164 12163  0 14:52 ?        00:00:00 openvassd (Loading Handler)
    elatov   12166 10832  0 14:52 pts/2    00:00:00 grep --color=auto open

After it's done you will see the following

    elatov@m2:~$ps -eaf | grep open
    root     12163     1 50 14:52 ?        00:02:29 openvassd: Waiting for incoming connections
    elatov   12392 10832  0 14:57 pts/2    00:00:00 grep --color=auto open
    
#### Generate Client SSL Certs for OpenVAS Manager

    elatov@m2:~$sudo /usr/local/openvas/sbin/openvas-mkcert-client -n -i

#### Build the OpenVAS Manager Database

Now you can initialize the OpenVAS Manager database. You need a running OpenVAS Scanner (**openvassd**) for this as the Manager will retrieve all NVT details from the Scanner.

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvasmd --rebuild

#### Create admin user and encrypt credentials

Next let's create an admin user

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvasmd --create-user=admin
	User created with password 'a192f8e7-54a2-4894-bf'.
	
Now let's create an encryption key:

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvasmd --create-credentials-encryption-key
	Key creation succeeded.

We can confirm the key is created:

	elatov@m2:~$sudo gpg --homedir /usr/local/openvas/var/lib/openvas/gnupg --list-secret-keys
	gpg: WARNING: unsafe ownership on homedir `/usr/local/openvas/var/lib/openvas/gnupg'
	gpg: checking the trustdb
	gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
	gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
	/usr/local/openvas/var/lib/openvas/gnupg/secring.gpg
	----------------------------------------------------
	sec   2048R/870E0A38 2014-06-17
	uid                  OpenVAS Credential Encryption

Now let's encrypt all credentials:

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvasmd --encrypt-all-credentials
	Encryption succeeded.
	
#### Download SCAP Database
This script (**/usr/local/openvas/sbin/openvas-scapdata-sync**) doesn't use any *openvas* binaries so we don't have to modify it, we can just run it:

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvas-scapdata-sync
	[i] This script synchronizes a SCAP data directory with the OpenVAS one.
	[i] SCAP dir: /usr/local/openvas/var/lib/openvas/scap-data
	[i] Will use rsync
	[i] Using rsync: /usr/bin/rsync
	[i] Configured SCAP data rsync feed: rsync://feed.openvas.org:/scap-data
	OpenVAS feed server - http://www.openvas.org/
	This service is hosted by Intevation GmbH - http://intevation.de/
	..
	...
	oval/5.10/org.mitre.oval/v/family/unix.xml.asc
	         198 100%    0.36kB/s    0:00:00 (xfer#51, to-check=2/63)
	oval/5.10/org.mitre.oval/v/family/windows.xml
	    42211550 100%    6.63MB/s    0:00:06 (xfer#52, to-check=1/63)
	oval/5.10/org.mitre.oval/v/family/windows.xml.asc
	         198 100%    0.25kB/s    0:00:00 (xfer#53, to-check=0/63)
	
	sent 1105 bytes  received 624960144 bytes  7309488.29 bytes/sec
	total size is 624880035  speedup is 1.00
	[i] Initializing scap database
	[i] Updating CPEs
	[i] Updating /usr/local/openvas/var/lib/openvas/scap-data/nvdcve-2.0-2002.xml
	[i] Updating /usr/local/openvas/var/lib/openvas/scap-data/nvdcve-2.0-2003.xml
	[i] Updating /usr/local/openvas/var/lib/openvas/scap-data/nvdcve-2.0-2004.xml
	[i] Updating /usr/local/openvas/var/lib/openvas/scap-data/nvdcve-2.0-2005.xml
	[i] Updating /usr/local/openvas/var/lib/openvas/scap-data/nvdcve-2.0-2006.xml

#### Download the Cert Database
We need to fix this script (**/usr/local/openvas/sbin/openvas-certdata-sync**) as well:

	OPENVASSD=/usr/local/openvas/sbin/openvassd
	SCAP_DIR=`/usr/local/openvas/sbin/openvassd -s | awk -F" = " '/^plugins_folder/ { print $2 }' | sed -s 's/\(^.*\)\/plugins/\1/'`

Then run the script:

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvas-certdata-sync
	[i] This script synchronizes a CERT advisory directory with the OpenVAS one.
	[i] CERT dir: /usr/local/openvas/var/lib/openvas/cert-data
	[i] Will use rsync
	[i] Using rsync: /usr/bin/rsync
	[i] Configured CERT data rsync feed: rsync://feed.openvas.org:/cert-data
	OpenVAS feed server - http://www.openvas.org/
	This service is hosted by Intevation GmbH - http://intevation.de/
	All transactions are logged.
	
	Please report synchronization problems to openvas-feed@intevation.de.
	If you have any other questions, please use the OpenVAS mailing lists
	or the OpenVAS IRC chat. See http://www.openvas.org/ for details.
	
	receiving incremental file list
	./
	
	sent 62 bytes  received 716 bytes  311.20 bytes/sec
	total size is 8793411  speedup is 11302.58
	[i] Skipping /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2008.xml, file is older than last revision
	[i] Skipping /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2009.xml, file is older than last revision
	[i] Skipping /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2010.xml, file is older than last revision
	[i] Skipping /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2011.xml, file is older than last revision
	[i] Skipping /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2012.xml, file is older than last revision
	[i] Updating /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2013.xml
	[i] Updating /usr/local/openvas/var/lib/openvas/cert-data/dfn-cert-2014.xml
	[i] Updating Max CVSS for DFN-CERT
	
### Setup the init scripts
I just copied the the scripts from the atomic repo with slight modifications. Here is the **openvas-scanner**:

	elatov@m2:~$cat /etc/init.d/openvas-scanner
	#!/bin/sh
	#
	# openvas-scanner    This starts and stops the OpenVAS scanner.
	#
	# chkconfig:   35 75 25
	# description: This starts and stops the OpenVAS scanner.
	# processname: /usr/sbin/openvassd
	# config:      /etc/openvas/openvassd.conf
	# pidfile:     /var/run/openvassd.pid
	#
	### BEGIN INIT INFO
	# Provides: $openvas-scanner
	### END INIT INFO
	
	# Source function library.
	. /etc/rc.d/init.d/functions
	
	EXEC="/usr/local/openvas/sbin/openvassd"
	PROG=$(basename $EXEC)
	
	# Check for missing binaries (stale symlinks should not happen)
	# Note: Special treatment of stop for LSB conformance
	test -x $EXEC || { echo "$EXEC not installed";
		if [ "$1" = "stop" ]; then exit 0;
		else exit 5; fi; }
	
	# Check for existence of needed config file
	OPENVASSD_CONFIG=/etc/sysconfig/openvas-scanner
	test -r $OPENVASSD_CONFIG || { echo "$OPENVASSD_CONFIG does not exist";
		if [ "$1" = "stop" ]; then exit 0;
		else exit 6; fi; }
	
	# Read config
	. $OPENVASSD_CONFIG
	
	# Build parameters
	[ "$SCANNER_ADDRESS" ] && PARAMS="$PARAMS --listen=$SCANNER_ADDRESS"
	[ "$SCANNER_PORT" ]    && PARAMS="$PARAMS --port=$SCANNER_PORT"
	
	LOCKFILE=/var/lock/subsys/$PROG
	
	start() {
	    echo -n $"Starting openvas-scanner: "
	    daemon $EXEC $PARAMS
	    RETVAL=$?
	    echo
	    [ $RETVAL -eq 0 ] && touch $LOCKFILE
	    return $RETVAL
	}
	
	stop() {
	    echo -n $"Stopping openvas-scanner: "
	    killproc $PROG
	    RETVAL=$?
	    echo
	    [ $RETVAL -eq 0 ] && rm -f $LOCKFILE
	    return $RETVAL
	}
	
	restart() {
	    stop
	    start
	}
	
	reload() {
	    echo -n $"Reloading openvas-scanner: "
	    killproc $PROG -HUP
	    RETVAL=$?
	    echo
	    return $RETVAL
	}
	
	force_reload() {
	    restart
	}
	
	fdr_status() {
	    status $PROG
	}
	
	case "$1" in
	    start|stop|restart|reload)
	        $1
	        ;;
	    force-reload)
	        force_reload
	        ;;
	    status)
	        fdr_status
	        ;;
	    condrestart|try-restart)
	        [ ! -f $LOCKFILE ] || restart
	        ;;
	    *)
	        echo $"Usage: $0 {start|stop|status|restart|try-restart|reload|force-reload}"
	        exit 2
	esac
	
Here is the **openvas-manager**:

	elatov@m2:~$cat /etc/init.d/openvas-manager
	#!/bin/bash
	
	# This is an implementation of a start-script for OpenVAS Manager
	
	# chkconfig: - 92 10
	# Description: OpenVAS Manager is a vulnerability Scanner management daemon
	#
	
	### BEGIN INIT INFO
	# Provides: openvas-manager
	# Required-Start: $local_fs $network $syslog
	# Required-Stop: $local_fs $network $syslog
	# Default-Start:
	# Default-Stop: 0 1 2 3 4 5 6
	# Short-Description: start|stop|status|restart|condrestart OpenVAS Manager
	# Description: control OpenVAS Manager
	### END INIT INFO
	
	# Source function library.
	. /etc/rc.d/init.d/functions
	
	exec="/usr/local/openvas/sbin/openvasmd"
	prog="openvasmd"
	progname="openvas-manager"
	lockfile=/var/lock/subsys/openvasmd
	
	[ -e /etc/sysconfig/$progname ] && . /etc/sysconfig/$progname
	
	rh_status() {
		# run checks to determine if the service is running or use generic status
		status -p /usr/local/openvas/var/run/$prog.pid -l $lockfile $progname
	}
	
	rh_status_q() {
		rh_status >/dev/null 2>&1
	}
	
	start() {
		echo "Starting $progname:"
		daemon --pidfile=/var/run/$prog.pid $exec $OPTIONS
		RETVAL=$?
		echo
		[ $RETVAL -eq 0 ] && touch $lockfile
		return $RETVAL
	}
	
	stop() {
		echo -n "Stopping $progname: "
		killproc $prog
		RETVAL=$?
		echo
		[ $RETVAL -eq 0 ] && rm -f $lockfile
		return $RETVAL
	}
	
	restart() {
		stop
		start
	}
	
	
	case "$1" in
		start)
			rh_status_q && exit 0
			$1
			;;
	
		stop)
			rh_status_q || exit 0
			$1
	                ;;
	
		restart)
			$1
			;;
	
		condrestart|try-restart)
			rh_status_q || exit 0
			$1
			;;
	
		status)
			status -p /usr/local/openvas/var/run/$prog.pid -l $lockfile $progname
	                ;;
	
		*)
			echo "Usage: $0 {start|stop|status|restart|condrestart}"
			exit 1
	esac
	
	exit 0
	
Here is **gsad**:

	elatov@m2:~$cat /etc/init.d/gsad
	#!/bin/sh
	#
	# gsad    This starts and stops the Greenbone Security Assistant.
	#
	# chkconfig:   35 75 25
	# description: This starts and stops the Greenbone Security Assistant.
	# processname: /usr/sbin/gsad
	# config:      /etc/openvas/gsad.conf
	# pidfile:     /var/run/gsad.pid
	#
	### BEGIN INIT INFO
	# Provides: $greenbone-security-assistant
	### END INIT INFO
	
	# Source function library.
	. /etc/rc.d/init.d/functions
	
	EXEC="/usr/local/openvas/sbin/gsad"
	PROG=$(basename $EXEC)
	
	# Check for missing binaries (stale symlinks should not happen)
	# Note: Special treatment of stop for LSB conformance
	test -x $EXEC || { echo "$EXEC not installed";
		if [ "$1" = "stop" ]; then exit 0;
		else exit 5; fi; }
	
	# Check for existence of needed config file
	GSAD_CONFIG=/etc/sysconfig/gsad
	test -r $GSAD_CONFIG || { echo "$GSAD_CONFIG not existing";
		if [ "$1" = "stop" ]; then exit 0;
		else exit 6; fi; }
	
	# Read config
	. $GSAD_CONFIG
	
	# Build parameters
	[ "$GSA_ADDRESS" ] && PARAMS="--listen=$GSA_ADDRESS"
	[ "$GSA_PORT" ] && PARAMS="$PARAMS --port=$GSA_PORT"
	[ "$GSA_SSL_PRIVATE_KEY" ] && PARAMS="$PARAMS --ssl-private-key=$GSA_SSL_PRIVATE_KEY"
	[ "$GSA_SSL_CERTIFICATE" ] && PARAMS="$PARAMS --ssl-certificate=$GSA_SSL_CERTIFICATE"
	[ "$GSA_REDIRECT" ] && [ "$GSA_REDIRECT" == 1 ] && PARAMS="$PARAMS --redirect"
	[ "$GSA_REDIRECT_PORT" ] && PARAMS="$PARAMS --rport=$GSA_REDIRECT_PORT"
	[ "$MANAGER_ADDRESS" ] && PARAMS="$PARAMS --mlisten=$MANAGER_ADDRESS"
	[ "$MANAGER_PORT" ] && PARAMS="$PARAMS --mport=$MANAGER_PORT"
	
	LOCKFILE=/var/lock/subsys/$PROG
	
	start() {
	    echo -n $"Starting greenbone-security-assistant: "
	    daemon $EXEC $PARAMS
	    RETVAL=$?
	    echo
	    [ $RETVAL -eq 0 ] && touch $LOCKFILE
	    return $RETVAL
	}
	
	stop() {
	    echo -n $"Stopping greenbone-security-assistant: "
	    killproc $PROG
	    RETVAL=$?
	    echo
	    [ $RETVAL -eq 0 ] && rm -f $LOCKFILE
	    return $RETVAL
	}
	
	restart() {
	    stop
	    start
	}
	
	reload() {
	    echo -n $"Reloading greenbone-security-assistant: "
	    killproc $PROG -HUP
	    RETVAL=$?
	    echo
	    return $RETVAL
	}
	
	force_reload() {
	    restart
	}
	
	fdr_status() {
	    status $PROG
	}
	
	case "$1" in
	    start|stop|restart|reload)
	        $1
	        ;;
	    force-reload)
	        force_reload
	        ;;
	    status)
	        fdr_status
	        ;;
	    condrestart|try-restart)
	        [ ! -f $LOCKFILE ] || restart
	        ;;
	    *)
	        echo $"Usage: $0 {start|stop|status|restart|try-restart|reload|force-reload}"
	        exit 2
	esac
	
Each of those had a corresponding **sysconfig** file:

	elatov@m2:~$cat /etc/sysconfig/openvas-scanner
	# Options to pass to the openvassd daemon
	OPTIONS="-p 9391"
	
	# Set to yes if plugins should be automatically updated via a cron job
	auto_plugin_update=yes
	
	# Notify OpenVAS scanner after update by seding it SIGHUP?
	notify_openvas_scanner=yes
	
	# Method to use to get updates. The default is via rsync
	# Note that only wget and curl support retrieval via proxy
	# update_method=rsync|wget|curl
	
	# Additionaly, you can specify the following variables
	#NVT_DIR		where to extract plugins (absolute path)
	#OV_RSYNC_FEED		URL of rsync feed
	#OV_HTTP_FEED		URL of http feed
	
	# First time install token
	FIRSTBOOT=no

Here is the **openvas-manager** one:

	elatov@m2:~$cat /etc/sysconfig/openvas-manager
	OPTIONS="--port 9390 --sport 9391 -v"
	
And lastly the **gsad** one:

	elatov@m2:~$grep -vE '^$|^#' /etc/sysconfig/gsad
	GSA_ADDRESS=0.0.0.0
	GSA_PORT=9392
	MANAGER_ADDRESS=127.0.0.1
	MANAGER_PORT=9390
	
Lastly here are the cron jobs for the automated syncing:

	elatov@m2:~$for i in $(ls /etc/cron.d/openvas-sync-*); do echo $i; cat $i; done
	/etc/cron.d/openvas-sync-cert
	# start plugin sync daily at 130am
	30 1 * * * root /bin/nice -n 19 /usr/bin/ionice -c2 -n7 /usr/local/openvas/sbin/openvas-certdata-sync > /dev/null
	/etc/cron.d/openvas-sync-plugins
	# start plugin sync daily at midnight
	0 0 * * * root /bin/nice -n 19 /usr/bin/ionice -c2 -n7 /usr/local/openvas/sbin//openvas-nvt-sync > /dev/null
	/etc/cron.d/openvas-sync-scap
	# start plugin sync daily at 1am
	0 1 * * * root /bin/nice -n 19 /usr/bin/ionice -c2 -n7 /usr/local/openvas/sbin/openvas-scapdata-sync > /dev/null
	
### Confirming the OpenVAS Install is good
There is a pretty nifty script that can check all the necessary components are running. It's called [openvas-check-setup](https://svn.wald.intevation.org/svn/openvas/trunk/tools/openvas-check-setup). Here is what I did to run it:

	elatov@m2:~$wget --no-check-certificate https://svn.wald.intevation.org/svn/openvas/trunk/tools/openvas-check-setup
	elatov@m2:~$chmod +x openvas-check-setup
	elatov@m2:~$sudo -b env PATH="/usr/local/openvas/bin:/usr/local/openvas/sbin:$PATH" ./openvas-check-setup --server
	elatov@m2:~$openvas-check-setup 2.2.5
	  Test completeness and readiness of OpenVAS-7
	  (add '--v4', '--v5', '--v6' or '--v8'
	   if you want to check for another OpenVAS version)
	
	  Please report us any non-detected problems and
	  help us to improve this check routine:
	  http://lists.wald.intevation.org/mailman/listinfo/openvas-discuss
	
	  Send us the log-file (/tmp/openvas-check-setup.log) to help analyze the problem.
	
	Step 1: Checking OpenVAS Scanner ...
	        OK: OpenVAS Scanner is present in version 4.0.1.
	        OK: OpenVAS Scanner CA Certificate is present as /usr/local/openvas/var/lib/openvas/CA/cacert.pem.
	        OK: NVT collection in /usr/local/openvas/var/lib/openvas/plugins contains 35241 NVTs.
	        WARNING: Signature checking of NVTs is not enabled in OpenVAS Scanner.
	        SUGGEST: Enable signature checking (see http://www.openvas.org/trusted-nvts.html).
	        OK: The NVT cache in /usr/local/openvas/var/cache/openvas contains 35241 files for 35241 NVTs.
	Step 2: Checking OpenVAS Manager ...
	        OK: OpenVAS Manager is present in version 5.0.2.
	        OK: OpenVAS Manager client certificate is present as /usr/local/openvas/var/lib/openvas/CA/clientcert.pem.
	        OK: OpenVAS Manager database found in /usr/local/openvas/var/lib/openvas/mgr/tasks.db.
	        OK: Access rights for the OpenVAS Manager database are correct.
	        OK: sqlite3 found, extended checks of the OpenVAS Manager installation enabled.
	        OK: OpenVAS Manager database is at revision 123.
	        OK: OpenVAS Manager expects database at revision 123.
	        OK: Database schema is up to date.
	        OK: OpenVAS Manager database contains information about 35241 NVTs.
	        OK: OpenVAS SCAP database found in /usr/local/openvas/var/lib/openvas/scap-data/scap.db.
	        OK: OpenVAS CERT database found in /usr/local/openvas/var/lib/openvas/cert-data/cert.db.
	        OK: xsltproc found.
	Step 3: Checking user configuration ...
	        WARNING: Your password policy is empty.
	        SUGGEST: Edit the /usr/local/openvas/etc/openvas/pwpolicy.conf file to set a password policy.
	Step 4: Checking Greenbone Security Assistant (GSA) ...
	        OK: Greenbone Security Assistant is present in version 5.0.1.
	Step 5: Checking OpenVAS CLI ...
	        SKIP: Skipping check for OpenVAS CLI.
	Step 6: Checking Greenbone Security Desktop (GSD) ...
	        SKIP: Skipping check for Greenbone Security Desktop.
	Step 7: Checking if OpenVAS services are up and running ...
	       OK: netstat found, extended checks of the OpenVAS services enabled.
	        OK: OpenVAS Scanner is running and listening on all interfaces.
	        OK: OpenVAS Scanner is listening on port 9391, which is the default port.
	        OK: OpenVAS Manager is running and listening on all interfaces.
	        OK: OpenVAS Manager is listening on port 9390, which is the default port.
	        OK: Greenbone Security Assistant is running and listening on all interfaces.
	        OK: Greenbone Security Assistant is listening on port 9392, which is the default port.
	Step 8: Checking nmap installation ...
	        OK: nmap is present in version 5.51.
	Step 9: Checking presence of optional tools ...
	        OK: pdflatex found.
	        OK: PDF generation successful. The PDF report format is likely to work.
	        OK: ssh-keygen found, LSC credential generation for GNU/Linux targets is likely to work.
	        OK: rpm found, LSC credential package generation for RPM based targets is likely to work.
	        WARNING: Could not find alien binary, LSC credential package generation for DEB based targets will not work.
	        SUGGEST: Install alien.
	        OK: nsis found, LSC credential package generation for Microsoft Windows targets is likely to work.
	        OK: SELinux is disabled.
	
	It seems like your OpenVAS-7 installation is OK.
	
	If you think it is not OK, please report your observation
	and help us to improve this check routine:
	http://lists.wald.intevation.org/mailman/listinfo/openvas-discuss
	Please attach the log-file (/tmp/openvas-check-setup.log) to help us analyze the problem.

### Generate default OpenVAS Scanner Configuration file

If you are planning on modifying the default setting for the scanner, first generate the default settings:

	elatov@m2:~$sudo /usr/local/openvas/sbin/openvassd -s > /usr/local/openvas/etc/openvas/openvassd.conf

Just for reference here are the defaults:

	elatov@m2:~$/usr/local/openvas/sbin/openvassd -s
	plugins_folder = /usr/local/openvas/var/lib/openvas/plugins
	cache_folder = /usr/local/openvas/var/cache/openvas
	include_folders = /usr/local/openvas/var/lib/openvas/plugins
	max_hosts = 30
	max_checks = 10
	be_nice = no
	logfile = /usr/local/openvas/var/log/openvas/openvassd.messages
	log_whole_attack = no
	log_plugins_name_at_load = no
	dumpfile = /usr/local/openvas/var/log/openvas/openvassd.dump
	cgi_path = /cgi-bin:/scripts
	optimize_test = yes
	checks_read_timeout = 5
	network_scan = no
	non_simult_ports = 139, 445
	plugins_timeout = 320
	safe_checks = yes
	auto_enable_dependencies = yes
	use_mac_addr = no
	nasl_no_signature_check = yes
	drop_privileges = no
	unscanned_closed = yes
	vhosts = 
	vhosts_ip = 
	report_host_details = yes
	cert_file = /usr/local/openvas/var/lib/openvas/CA/servercert.pem
	key_file = /usr/local/openvas/var/lib/openvas/private/CA/serverkey.pem
	ca_file = /usr/local/openvas/var/lib/openvas/CA/cacert.pem
	config_file = /usr/local/openvas/etc/openvas/openvassd.conf

Then modify as necessary. You should be done, at this point make sure all the services are running:

	elatov@m2:~$sudo service openvas-scanner status
	openvassd (pid 15894 15751) is running...
	elatov@m2:~$sudo service openvas-manager status
	openvas-manager (pid  4405) is running...
	elatov@m2:~$sudo service gsad status
	gsad (pid 15420) is running...
	elatov@m2:~$ps -eaf | grep openvas
	root      4304     1  0 10:48 ?        00:00:38 openvassd: Waiting for incoming connections
	root      4405     1  0 10:50 ?        00:00:02 openvasmd
	root     15420     1  0 12:35 ?        00:00:00 /usr/local/openvas/sbin/gsad --listen=0.0.0.0 --port=9392 --mlisten=127.0.0.1 --mport=9390 -v
	root     15751  4304  0 12:40 ?        00:00:52 openvassd: Serving 127.0.0.1

And then you can point your browser to the OpenVAS server and run scans just like described in my [previous post](/2014/05/openvas-centos/). 
