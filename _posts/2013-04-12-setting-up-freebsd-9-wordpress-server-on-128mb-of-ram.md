---
title: Setting up a FreeBSD 9 WordPress Server on 128MB of RAM
author: Jarret Lavallee
layout: post
permalink: /2013/04/setting-up-freebsd-9-wordpress-server-on-128mb-of-ram/
dsq_thread_id:
  - 1406848003
categories:
  - Home Lab
  - OS
tags:
  - freebsd
  - VPS
  - wordpress
---
A while ago I bought a KVM VPS and configured it to run FreeBSD 9. It was meant to replace the OpenVZ VM that currently runs <a href="http://virtuallyhyper.com" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com']);">virtuallyhyper.com</a>. Karim went on to write <a href="http://virtuallyhyper.com/2012/09/blitz-io-tests-against-apache-worker-apache-prefork-apache-with-php-fpm-and-nginx-with-php-fpm/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/blitz-io-tests-against-apache-worker-apache-prefork-apache-with-php-fpm-and-nginx-with-php-fpm/']);">this post</a> about the PHP performance using the server. This post is about setting up the server to run the WordPress site within 128MB of memory.

## Base System

The first thing we should do is install FreeBSD 9. Once it is installed, we should get all the ports(packages) and extract them:

    # portsnap fetch
    # portsnap extract
    

After the ports are extracted, we should update them:

    # portsnap update
    

I prefer to use **portupgrade** to update all the ports, so let&#8217;s install it:

    # cd /usr/ports/ports-mgmt/portupgrade
    # make install clean
    

You could also use **portmanager**, which can be installed as per the instructions below:

    # cd /usr/ports/ports-mgmt/portmanager
    # make install clean
    

We do not want to continue using the root user, so we let&#8217;s install the **sudo** package to give users root privileges:

    # cd /usr/ports/security/sudo
    # make install clean
    

Once installed, let&#8217;s enable a group to have *sudo* rights. First run **visudo**:

    # visudo
    

**visudo** will open the */etc/sudoers* file to be edited. Uncomment the following line:

    %wheel ALL=(ALL) ALL
    

## Installing Packages

We will be using <a href="http://nginx.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://nginx.org']);">Nginx</a>, <a href="http://php-fpm.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://php-fpm.org']);">PHP-FPM</a>, and <a href="http://www.mysql.com" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.mysql.com']);">Mysql</a>.

### Installing Nginx

Next we will want to install our web server. I like *nginx* as it is light weight and stable. Let&#8217;s install it, but first we should configure the package:

    # cd /usr/ports/www/nginx
    # make config-recursive
    

Check the following options.

    [X] HTTP_MODULE Enable HTTP module
    [X] HTTP_ADDITION_MODULE Enable http_addition module
    [X] HTTP_CACHE_MODULE Enable http_cache module
    [X] HTTP_DAV_MODULE Enable http_webdav module
    [X] HTTP_FLV_MODULE Enable http_flv module
    [X] HTTP_GEOIP_MODULE Enable http_geoip module
    [X] HTTP_GZIP_STATIC_MODULE Enable http_gzip_static module
    [X] HTTP_IMAGE_FILTER_MODULE Enable http_image_filter module
    [X] HTTP_PERL_MODULE Enable http_perl module
    [X] HTTP_RANDOM_INDEX_MODULE Enable http_random_index module
    [X] HTTP_REALIP_MODULE Enable http_realip module
    [X] HTTP_REWRITE_MODULE Enable http_rewrite module
    [X] HTTP_SECURE_LINK_MODULE Enable http_secure_link module
    [X] HTTP_SSL_MODULE Enable http_ssl module
    [X] HTTP_STATUS_MODULE Enable http_stub_status module
    [X] HTTP_SUB_MODULE Enable http_sub module
    [X] HTTP_XSLT_MODULE Enable http_xslt module
    

Now we can install the package:

    # make install clean
    

Configure the service to start on boot:

    # echo ‘nginx_enable=”YES”‘ >> /etc/rc.conf
    

### Installing PHP

Next we will install PHP. Based on performance tests, I like to go with PHP5 with FPM:

    # cd /usr/ports/lang/php5
    # make config-recursive
    

Make sure the following options are checked:

    [*] CLI Build CLI version
    [*] CGI Build CGI version
    [*] FPM Build FPM version
    [*] LINKTHR Link thread lib (for threaded extensions)
    

Build the package:

    # make install clean
    

Configure the PHP extensions:

    # cd /usr/ports/lang/php5-extensions
    # make config-recursive
    

Check the following options:

    [*] CTYPE ctype functions
    [*] CURL CURL support
    [*] DOM DOM support
    [*] FILTER input filter support
    [*] HASH HASH Message Digest Framework
    [*] ICONV iconv support
    [*] JSON JavaScript Object Serialization support
    [*] MYSQL MySQL database support
    [*] PDO PHP Data Objects Interface (PDO)
    [*] PDO_SQLITE PDO sqlite driver
    [*] PHAR phar support
    [*] POSIX POSIX-like functions
    [*] SESSION session support
    [*] SIMPLEXML simplexml support
    [*] SQLITE3 sqlite3 support
    [*] TOKENIZER tokenizer support
    [*] XML XML support
    [*] XMLREADER XMLReader support
    [*] XMLWRITER XMLWriter support
    

Build the package and enable it to start on boot:

    # make install clean
    # echo ‘php_fpm_enable=”YES”‘ >> /etc/rc.conf
    

Lastly, we need to build **php5-zlib**:

    # cd /usr/ports/archivers/php5-zlib/
    # make install clean
    

### Installing Mysql

We will be using **mysql** as the database back-end to the WordPress site. We will install *mysql5.5*:

    # cd /usr/ports/databases/mysql55-server
    # make config-recursive
    

Leave the default options and enable the following option:

    [*] OPENSSL Enable SSL support
    

Build and install the package:

    # make -D BUILD_OPTIMIZED install
    

Enable the package to start on boot:

    # echo ‘mysql_enable=”YES”‘ >> /etc/rc.conf
    

### Installing WordPress

Installing WordPress is as simple as getting the newest version and extracting it to our web root. Let&#8217;s get the newest package:

    # wget http://wordpress.org/latest.tar.gz
    

Now we can extract it to our web root:

    # tar zxvf latest.tar.gz -C /usr/local/www/wordpress
    

## Configuring the Services

### Mysql

Mysql will be the database for WordPress. The default configuration comes with multiple choices by default:

*   *my-small.cnf* – for systems with up to 64 Mb of RAM.
*   *my-medium.cnf* – for systems with up to 128 Mb of RAM (ideal for web servers).
*   *my-large.cnf* – for systems with 512 Mb of RAM (dedicated MySQL servers).
*   *my-huge.cnf* – for systems with 1-2 Gb of RAM (datacenters etc.).

In this VPS we have 128MB of memory, so we will use the **my-meduim.cnf** configuration file. Let&#8217;s put the appropriate **my.cnf** file in place:

    # cp /usr/local/share/mysql/my-medium.cnf /var/db/mysql/my.cnf
    

The defaults should be fine, but we can make some modifications to the **mysqld** section to cut back on memory usage. Edit the **my.cnf** file and change the below lines. These changes will disable *InnoDB* and force *MyISAM* to be the database engine:

    key_buffer_size = 8M
    skip-innodb
    default-storage-engine=MyISAM
    query_cache_size = 0
    

Start the **mysql** service:

    # /usr/local/etc/rc.d/mysql-server start
    

Change the **mysql** root password to be more secure:

    # /usr/local/bin/mysqladmin -u root password 'some-strong-password'
    

Let&#8217;s create a database and add a user for our WordPress site:

    # mysql -u root -p
    mysql> create database wordpress;
    mysql> grant all on wordpress.* to wordpress@localhost identified by 'another-strong-password';
    mysql> flush PRIVILEGES;
    

### Configuring PHP

PHP will do all of the processing for our website. We are running the PHP-FPM service, so we need to configure some properties. First, let&#8217;s copy over the default **php.ini** file into place:

    # cp /usr/local/etc/php.ini-production /usr/local/etc/php.ini
    

Then let&#8217;s make some modifications for our environment to limit the memory and change the upload size. Edit the **/usr/local/etc/php.ini** file and change the following lines:

    upload_max_filesize = 200M
    post_max_size = 200M
    memory_limit = 96M
    

Now let&#8217;s change the properties for PHP-FPM. To do this, edit the **/usr/local/etc/php-fpm.conf** file and change the following lines:

    events.mechanism = kqueue
    
    # [www] section
    listen = /var/run/php-fpm.sock
    listen.owner = www
    listen.group = www
    listen.mode = 0666
    pm = ondemand
    pm.process_idle_timeout = 3s;
    

We can now start the service

    # /usr/local/etc/rc.d/php-fpm start
    

### Configuring Nginx

Nginx is our web server. We need to configure it to start serving the correct web pages to the PHP service and listen on the correct ports. Let&#8217;s edit the **/usr/local/etc/nginx/nginx.conf** file and change the following lines:

    user www;
    worker_processes 2;
    events {
    worker_connections 1024;
    use kqueue;
    }
    #http section
    server_names_hash_bucket_size 64;
    gzip_http_version 1.1;
    gzip_vary on;
    gzip_comp_level 1;
    gzip_min_length 1100;
    gzip_proxied any;
    gzip_types text/plain text/css application/json application/x-javascript text/x$
    gzip_buffers 16 8k;
    gzip_disable “MSIE [1-6].(?!.*SV1)”;
    

Lower down in this file we will see a **Server** section, we can enable our servers by making the following change:

    ## Server sections
    #default (all will land here except for direct matches
    server {
    listen 80 default_server;
    server_name _; # This is just an invalid value which will never trigger on a real hostname.
    
    root /usr/local/www/wordpress;
    }
    
    # PHP (wordpress)
    server {
    listen 80;
    server_name wordpress.moopless.com wordpress;
    root /usr/local/www/wordpress;
    location / {
    root /usr/local/www/wordpress;
    index index.php index.html index.htm;
    }
    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ .php$ {
    fastcgi_pass unix:/var/run/php-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
    }
    location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|xml)$ {
    access_log off;
    log_not_found off;
    expires max;
    }
    }
    

We can now start the service:

    # /usr/local/etc/rc.d/nginx start
    

### Configuring a Firewall

We will use PF as our firewall. We can close all of the ports that we are not using. First we need to enable PF on boot:

    # echo ‘pf_enable=”YES”‘ >> /etc/rc.conf
    

Next let&#8217;s copy the example config file into place:

    # cp /usr/share/examples/pf/pf.conf /etc/pf.conf
    

Now we can customize the **/etc/pf.conf** file by adding the following lines:

    #Define external interface
    ext_if=”re0″
    
    #Skip the loopback
    set skip on lo
    
    # Packet Normilization
    scrub in
    
    # Block everything coming in
    block in
    pass out keep state
    
    #antispoofing
    antispoof quick for { lo }
    
    # Allow ssh
    pass in on $ext_if proto tcp to ($ext_if) port ssh
    # Allow pings
    pass in inet proto icmp all icmp-type echoreq
    # Allow http/https
    pass in on $ext_if proto tcp to ($ext_if) port { http, https } flags S/SA modulate state
    

We can now start the service:

    # /usr/local/etc/rc.d/pf start
    

Now everything is configured. You should be able to go to your **webserver.com/admin** page and start to configure WordPress with the database credentials that we defined.

## Memory Considerations

Since we are limited on memory we can make some modifications to the system to lower the memory utilization.

### Disable some TTYs to save memory

Since we use SSH as the primary way of connecting to this machine, we can disable some of the TTYs to save some memory. Edit the **/etc/ttys** file and change the TTYs to off. Make sure to leave at least one TTY on.

    ttyv2 “/usr/libexec/getty Pc” xterm off secure
    ttyv3 “/usr/libexec/getty Pc” xterm off secure
    ttyv4 “/usr/libexec/getty Pc” xterm off secure
    ttyv5 “/usr/libexec/getty Pc” xterm off secure
    ttyv6 “/usr/libexec/getty Pc” xterm off secure
    ttyv7 “/usr/libexec/getty Pc” xterm off secure
    ttyv8 “/usr/local/bin/xdm -nodaemon” xterm off secure
    

### No need to run moused

We can disable the **moused** service as we are not using a GUI:

    # echo ‘moused_enable="NO"‘ >> /etc/rc.conf
    

## Further Reading

More information can be found on the following web sites.

*   http://blog.secaserver.com/2011/07/freebsd-nginx-php-fastcgi-installation
*   http://blog.ijun.org/2012/01/install-nginx-php-fpm-and-varnish-on.html
*   http://www.iceflatline.com/2011/11/how-to-install-apache-mysql-php-and-phpmyadmin-on-freebsd
*   http://forums.freebsd.org/showthread.php?t=30268
*   http://www.freebsd.org/doc/handbook/firewalls-pf.html
*   http://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/ports-using.html

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/04/setting-up-freebsd-9-wordpress-server-on-128mb-of-ram/" title=" Setting up a FreeBSD 9 WordPress Server on 128MB of RAM" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:freebsd,VPS,wordpress,blog;button:compact;">A while ago I bought a KVM VPS and configured it to run FreeBSD 9. It was meant to replace the OpenVZ VM that currently runs virtuallyhyper.com. Karim went on...</a>
</p>