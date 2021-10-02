---
title: RHCSA and RHCE Chapter 14 – Web Services
author: Karim Elatov
layout: post
permalink: /2014/03/rhcsa-rhce-chapter-14-web-services/
categories: ['certifications', 'rhcsa_rhce']
tags: ['linux','apache', 'rhel', 'squid']
---

## Apache

From the [Deployment Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/deployment_guide/red_hat_enterprise_linux-6-deployment_guide-en-us.pdf):

> **HTTP** (Hypertext Transfer Protocol) server, or a web server, is a network service that serves content to a client over the web. This typically means web pages, but any other documents can be served as well.
>
> This section focuses on the Apache HTTP Server 2.2, a robust, full-featured open source web server developed by the Apache Software Foundation, that is included in Red Hat Enterprise Linux 6. It describes the basic configuration of the httpd service, and covers advanced topics such as adding server modules, setting up virtual hosts, or configuring the secure HTTP server.

### Running the httpd Service

From the same guide:

> This section describes how to start, stop, restart, and check the current status of the Apache HTTP Server. To be able to use the httpd service, make sure you have the httpd installed. You can do so by using the following command:
>
>     ~]# yum install httpd
>
>
> To run the httpd service, type the following at a shell prompt:
>
>     ~]# service httpd start
>     Starting httpd:                                            [  OK  ]
>
>
> If you want the service to start automatically at the boot time, use the following command:
>
>     ~]# chkconfig httpd on
>
>
> This will enable the service for runlevel 2, 3, 4, and 5.
>
> To stop the running httpd service, type the following at a shell prompt:
>
>     ~]# service httpd stop
>     Stopping httpd:                                            [  OK  ]
>
>
> To prevent the service from starting automatically at the boot time, type:
>
>     ~]# chkconfig httpd off
>
>
> There are three different ways to restart the running httpd service:
>
> 1.  To restart the service completely, type:
>
>         ~]# service httpd restart
>         Stopping httpd:                                            [  OK  ]
>         Starting httpd:                                            [  OK  ]
>
>
>     This will stop the running httpd service, and then start it again. Use this command after installing or removing a dynamically loaded module such as PHP.
>
> 2.  To only reload the configuration, type:
>
>         ~]# service httpd reload
>
>
>     This will cause the running httpd service to reload the configuration file. Note that any requests being currently processed will be interrupted, which may cause a client browser to display an error message or render a partial page.
>
> 3.  To reload the configuration without affecting active requests, type:
>
>         ~]# service httpd graceful
>
>
>     This will cause the running httpd service to reload the configuration file. Note that any requests being currently processed will use the old configuration.

### Apache Configuration Files

From the above guide:

> When the httpd service is started, by default, it reads the configuration from locations defined below:
>
> ![apache config RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-config.png)
>
> Although the default configuration should be suitable for most situations, it is a good idea to become at least familiar with some of the more important configuration options. Note that for any changes to take effect, the web server has to be restarted first.
>
> To check the configuration for possible errors, type the following at a shell prompt:
>
>     ~]# service httpd configtest
>     Syntax OK
>
>
> To make the recovery from mistakes easier, it is recommended that you make a copy of the original file before editing it.

### Common httpd.conf Directives

Check the Deployment Guide for a full list, I will cover a couple of the ones that I will use:

> **<directory></directory>**
> The *<directory></directory>* directive allows you to apply certain directives to a particular directory only. It takes the following form:
>
>     <Directory directory>
>       directive
>       …
>     </Directory>
>
>
> The **directory** can be either a full path to an existing directory in the local file system, or a wildcard expression.
>
> This directive can be used to configure additional **cgi-bin** directories for server-side scripts located outside the directory that is specified by **ScriptAlias**. In this case, the **ExecCGI** and **AddHandler** directives must be supplied, and the permissions on the target directory must be set correctly (that is, **0755**).
>
> **Example 16.1. Using the <directory> directive</directory>**
>
>     <Directory /var/www/html>
>       Options Indexes FollowSymLinks
>       AllowOverride None
>       Order allow,deny
>       Allow from all
>     </Directory>
>
>
> **<location></location>**
> The *<location></location>* directive allows you to apply certain directives to a particular URL only. It takes the following form:
>
>     <Location url>
>       directive
>       …
>     </Location>
>
>
> The **url** can be either a path relative to the directory specified by the **DocumentRoot** directive (for example, **/server-info**), or an external URL such as **http://example.com/server-info**.
>
> **Example 16.4. Using the <location> directive</location>**
>
>     <Location /server-info>
>       SetHandler server-info
>       Order deny,allow
>       Deny from all
>       Allow from .example.com
>     </Location>
>
>
> **<virtualhost></virtualhost>**
> The *<virtualhost></virtualhost>* directive allows you apply certain directives to particular virtual hosts only. It takes the following form:
>
>     <VirtualHost address[:port]…>
>       directive
>       …
>     </VirtualHost>
>
>
> The address can be an IP address, a fully qualified domain name, or a special form as described in the below table:
>
> ![apache vh options RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-vh-options.png)
>
> **Example 16.6. Using the <virtualhost> directive</virtualhost>**
>
>     <VirtualHost *:80>
>       ServerAdmin webmaster@penguin.example.com
>       DocumentRoot /www/docs/penguin.example.com
>       ServerName penguin.example.com
>       ErrorLog logs/penguin.example.com-error_log
>       CustomLog logs/penguin.example.com-access_log common
>     </VirtualHost>
>
>
> **AccessFileName**
> The *AccessFileName* directive allows you to specify the file to be used to customize access control information for each directory. It takes the following form:
>
>     AccessFileName filename…
>
>
> The **filename** is a name of the file to look for in the requested directory. By default, the server looks for **.htaccess**.
>
> For security reasons, the directive is typically followed by the **Files** tag to prevent the files beginning with **.ht** from being accessed by web clients. This includes the **.htaccess** and **.htpasswd** files.
>
> **Example 16.7. Using the AccessFileName directive**
>
>     AccessFileName .htaccess
>
>     <Files ~ "^\.ht">
>       Order allow,deny
>       Deny from all
>       Satisfy All
>     </Files>
>
>
> **Alias**
> The *Alias* directive allows you to refer to files and directories outside the default directory specified by the **DocumentRoot** directive. It takes the following form:
>
>     Alias url-path real-path
>
>
> The **url-path** must be relative to the directory specified by the **DocumentRoot** directive (for example, **/images/**). The **real-path** is a full path to a file or directory in the local file system.
>
> This directive is typically followed by the **Directory** tag with additional permissions to access the target directory. By default, the **/icons/** alias is created so that the icons from **/var/www/icons/** are displayed in server-generated directory listings.
>
> **Example 16.17. Using the Alias directive**
>
>     Alias /icons/ /var/www/icons/
>
>     <Directory "/var/www/icons">
>       Options Indexes MultiViews FollowSymLinks
>       AllowOverride None
>       Order allow,deny
>       Allow from all
>     <Directory>
>
>
> **Allow**
> The *Allow* directive allows you to specify which clients have permission to access a given directory. It takes the following form:
>
>     Allow from client…
>
>
> The **client** can be a domain name, an IP address (both full and partial), a **network/netmask** pair, or **all** for all clients.
>
> **Example 16.18. Using the Allow directive**
>
>     Allow from 192.168.1.0/255.255.255.0
>
>
> **AllowOverride**
> The *AllowOverride* directive allows you to specify which directives in a **.htaccess** file can override the default configuration. It takes the following form:
>
>     AllowOverride type…
>
>
> The **type** has to be one of the available grouping options as described in the below table:
>
> ![apache allowoverride options RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-allowoverride-options.png)
>
> **Example 16.19. Using the AllowOverride directive**
>
>     AllowOverride FileInfo AuthConfig Limit
>
>
> **Deny**
> The *Deny* directive allows you to specify which clients are denied access to a given directory. It takes the following form:
>
>     Deny from client…
>
>
> The **client** can be a domain name, an IP address (both full and partial), a **network/netmask** pair, or **all** for all clients.
>
> **Example 16.31. Using the Deny directive**
>
>     Deny from 192.168.1.1
>
>
> **DocumentRoot**
> The *DocumentRoot* directive allows you to specify the main directory from which the content is served. It takes the following form:
>
>     DocumentRoot directory
>
>
> The **directory** must be a full path to an existing directory in the local file system. The default option is **/var/www/html/**.
>
> **Example 16.33. Using the DocumentRoot directive**
>
>     DocumentRoot /var/www/html
>
>
> **Listen**
> The **Listen** directive allows you to specify IP addresses or ports to listen to. It takes the following form:
>
>     Listen [ip-address:]port [protocol]
>
>
> The **ip-address** is optional and unless supplied, the server will accept incoming requests on a given **port** from all IP addresses. Since the **protocol** is determined automatically from the port number, it can be usually omitted. The default option is to listen to port **80**.
>
> Note that if the server is configured to listen to a port under 1024, only superuser will be able to start the **httpd** service.
>
> **Example 16.46. Using the Listen directive**
>
>     Listen 80
>
>
> **Order**
> The *Order* directive allows you to specify the order in which the **Allow** and **Deny** directives are evaluated. It takes the following form:
>
>     Order option
>
>
> The **option** has to be a valid keyword as described in the below table:
>
> ![apache order options RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-order-options.png)
>
> **Example 16.53. Using the Order directive**
>
>     Order allow,deny
>
>
> **ServerName**
> The *ServerName* directive allows you to specify the hostname and the port number of a web server. It takes the following form:
>
>     ServerName hostname[:port]
>
>
> The **hostname** has to be a fully qualified domain name (FQDN) of the server. The **port** is optional, but when supplied, it has to match the number specified by the Listen directive. When using this directive, make sure that the IP address and server name pair are included in the **/etc/hosts** file.
>
> **Example 16.60. Using the ServerName directive**
>
>     ServerName penguin.example.com:80
>
>
> **ServerRoot**
> The *ServerRoot* directive allows you to specify the directory in which the server operates. It takes the following form:
>
>     ServerRoot directory
>
>
> The directory must be a full path to an existing directory in the local file system. The default option is **/etc/httpd/**.
>
> **Example 16.61. Using the ServerRoot directive**
>
>     ServerRoot /etc/httpd
>

### Installing and Testing Apache

So let's go ahead and test this out. First let's install apache:

    [root@rhel1 ~]# yum install httpd


Now let's start the apache service:

    [root@rhel1 ~]# service httpd start
    Starting httpd:  httpd


Lastly let's make sure it's listening on port 80:

    [root@rhel1 ~]# lsof -i tcp:80
    COMMAND  PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
    httpd   7392   root    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7394 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7395 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7396 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7397 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7398 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7399 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7400 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)
    httpd   7401 apache    4u  IPv6 1010244      0t0  TCP *:http (LISTEN)


Now let's check out the default configuration:

    [root@rhel1 ~]# grep -vE '^$|#' /etc/httpd/conf/httpd.conf  | grep -vE 'LoadModule|BrowserMatch|AddType|AddLanguage|AddIcon'
    ServerTokens OS
    ServerRoot "/etc/httpd"
    PidFile run/httpd.pid
    Timeout 60
    KeepAlive Off
    Listen 80
    Include conf.d/*.conf
    User apache
    Group apache
    ServerAdmin root@localhost
    UseCanonicalName Off
    DocumentRoot "/var/www/html"
    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>
    <Directory "/var/www/html">
        Options Indexes FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>
    DirectoryIndex index.html index.html.var
    AccessFileName .htaccess
    <Files ~ "^\.ht">
        Order allow,deny
        Deny from all
        Satisfy All
    </Files>
    TypesConfig /etc/mime.types
    DefaultType text/plain
    HostnameLookups Off
    ErrorLog logs/error_log
    LogLevel warn
    CustomLog logs/access_log combined
    ServerSignature On
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
    <Directory "/var/www/cgi-bin">
        AllowOverride None
        Options None
        Order allow,deny
        Allow from all
    </Directory>


We can see that our **DocumentRoot** is under **/var/www/html**. So let's create a simple **html** file under that directory:

    [root@rhel1 ~]# cat /var/www/html/index.html
    THIS IS RHEL1 RUNNING RH6!


Now let's open up port 80 on the firewall:

    [root@rhel1 ~]# iptables -I INPUT 12 -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT


and let's save the iptables configuration:

    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now on the RH5 machine let's run **elinks** and check if we can reach our server:

    [root@rhel2 ~]# elinks http://rhel1


After running that, you will see the following:

![rhel1 apache elinks RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-apache-elinks.png)

If you server is available using a client running a chrome web browser, visiting that same page with chrome will show you the following:

![rhel1 apache chrome RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-apache-chrome.png)

Now let's create a sub-directory under the *DirectoryRoot* (**/var/www/html**) and create another html file there:

    [root@rhel1 ~]# mkdir /var/www/html/dir
    [root@rhel1 ~]# cat /var/www/html/dir/index.html
    THIS IS RHEL1 RUNNING RH6! Under DIR1


Now from the RH5 client, running elinks:

    [root@rhel2 ~]# elinks http://rhel1/dir


I saw the following:

![rhel1 apache with dir elinks RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-apache-with-dir-elinks.png)

We can also check the access log and confirm that a client connected to our site:

    [root@rhel1 ~]# tail -1 /var/log/httpd/access_log 192.168.2.3 - - [15/Mar/2014:12:19:21 -0600] "GET /dir/ HTTP/1.1" 200 38 "http://rhel1/dir" "ELinks/0.11.1 (textmode; Linux; 80x24-2)"


That's us connecting to **apache** with the **elinks** client and we can see that our IP is **192.168.2.3**

### Securing Apache Sites

Let's deny access to the subdirectory that we created above (**dir**) from the rhel5 client with IP of **192.168.2.3**. There are two ways of doing this. The first is with the **Directory** Directive and the second is with **.htaccess** file. Let's do the first one. In the above configuration we see that any configuration file under **/etc/httpd/conf.d** is included, so let's create a configuration for our subdirectory. Here is what I ended up creating:

    [root@rhel1 ~]# cat /etc/httpd/conf.d/dir-secure.conf
    <Directory "/var/www/html/dir">
       Options Indexes FollowSymLinks
       AllowOverride None
       Order deny,allow
       Deny from 192.168.2.3
    </Directory>


Now confirming the configuration is okay and then restarting the apache service:

    [root@rhel1 conf.d]# service httpd configtest
    Syntax OK
    [root@rhel1 conf.d]# service httpd restart
    Stopping httpd: httpd
    Starting httpd: httpd


As a test trying to connect from the rhel5 client with **elinks**, I saw the following:

![apache denied access RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-denied-access.png)

I tried with another client and I was able to access the page. I saw the following in the **error_log** when access was denied:

    [root@rhel1 ~]# tail -1 /var/log/httpd/error_log
    [Sat Mar 15 12:51:36 2014] [error] [client 192.168.2.3] client denied by server configuration: /var/www/html/dir


To use the second option (**.htaccess**), we first have to configure what **options** are allowed to be overridden in that file. From the default configuration (**/etc/httpd/conf/httpd.conf**):

    <Directory "/var/www/html">
       Options Indexes FollowSymLinks
       AllowOverride None
       Order allow,deny
       Allow from all
    </Directory>


We can see that **AllowOverride** is set to **None**, let's allow **Limit** to be set in the **.htaccess** file, here is the configuration for that:

    <Directory "/var/www/html">
       Options Indexes FollowSymLinks
       AllowOverride Limit
       Order allow,deny
       Allow from all
    </Directory>


Then restart apache:

    [root@rhel1 ~]# service httpd restart
    Stopping httpd: httpd
    Starting httpd:  httpd


I then created a **.htaccess** file under our sub-directory with the following contents:

    [root@rhel1 ~]# cat /var/www/html/dir/.htaccess
    Order allow,deny
    Deny from 192.168.2.3
    Allow from all


The rhel5 client was still blocked. This way you could have a website owner control access to his own page, rather than him asking the apache administrator to do it for him.

### Apache Authorization

We can go one step further and create a password file which contains a list of users that are authorized to access a directory or page. The process is described on [this](https://access.redhat.com/solutions/64158) Redhat page. From the page:

> **Issue**
> Apache needs to be configured in such a way that requires authorization via **.htpassword** when requests are made from outside the local area network, while not requiring authorization from requests made from within the local area network.
>
> **Resolution**
> Please note that all commands will need to be run as the root user. First, an "**.htpasswd**" file will need to be created. This file will house the authorized user and password information for Apache.
>
>     # htpasswd -c .htpasswd user
>
>
> In the above command, replace user with the username that Apache should use for external authorization. After running this command, a prompt to create a password will appear. This password will be used in conjunction with the username to gain external authorization from Apache.
>
> Now a file named **.htpasswd** will be located in the current working directory. This file should be moved to a new location under the Apache directory, which will be used to house **.htpasswd** files:
>
>     # mkdir -p /etc/httpd/htpasswd && mv .htpasswd /etc/httpd/htpasswd/
>
>
> For this example, a previously created directory called **secret**, located inside the **/var/www/html** directory will serve as the directory to protect. Further, this example will use a local area network of **192.168.0.x** with a subnet mask of **255.255.255.0**. Using any text editor, the following directives must be added to to **/etc/httpd/conf/httpd.conf**:
>
>     <Directory /var/www/html/secret>
>          AuthType Basic
>          AuthName "Authorized Personnel Only"
>          AuthUserFile /etc/httpd/htpasswd/.htpasswd
>          Order allow,deny
>          Require valid-user
>          Allow from 192.168.0.0/24
>          Satisfy Any
>     </Directory>
>
>
> After saving the changes to **/etc/httpd/conf/httpd.conf**, restart Apache:
>
>     # /sbin/service httpd restart
>
>
> After restarting Apache, a properly configured directory requiring authorization from users requesting access from outside of the local area network will now exist.

### Apache Authorization Example

So let's protect our sub-directory. First let's create a **.htpasswd** file under our sub-directory:

    [root@rhel1 ~]# htpasswd -c /var/www/html/dir/.htpasswd user1
    New password:
    Re-type new password:
    Adding password for user user1


Now let's modify our custom configuration for that sub-directory, here is how mine looked like after I was done:

    [root@rhel1 ~]# cat /etc/httpd/conf.d/dir-secure.conf
    <Directory "/var/www/html/dir">
       Options Indexes FollowSymLinks
       AllowOverride None
       AuthType Basic
       AuthName "Authorized Personnel Only"
       AuthUserFile /var/www/html/dir/.htpasswd
       Require valid-user
       Order allow,deny
       Deny from 192.168.2.3
       Allow from all
       Satisfy any
    </Directory>


After that, visiting the page from the client, I saw the following:

![apache auth required RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-auth-required.png)

To do the same thing with the **.htaccess** we will need to add **authconfig** to the **AllowOverride** list.

### Apache VirtualHost

From the Deployment Guide:

> The Apache HTTP Server's built in virtual hosting allows the server to provide different information based on which IP address, hostname, or port is being requested.
>
> To create a name-based virtual host, find the virtual host container provided in **/etc/httpd/conf/httpd.conf** as an example, remove the hash sign (that is, #) from the beginning of each line, and customize the options according to your requirements as shown below.
>
> **Example 16.80. Sample virtual host configuration**
>
>     NameVirtualHost penguin.example.com:80
>
>     <VirtualHost penguin.example.com:80>
>         ServerAdmin webmaster@penguin.example.com
>         DocumentRoot /www/docs/penguin.example.com
>         ServerName penguin.example.com:80
>         ErrorLog logs/penguin.example.com-error_log
>         CustomLog logs/penguin.example.com-access_log common
>     </VirtualHost>
>
>
> Note that **ServerName** must be a valid DNS name assigned to the machine. The **<virtualhost></virtualhost>** container is highly customizable, and accepts most of the directives available within the main server configuration. Directives that are not supported within this container include User and Group, which were replaced by SuexecUserGroup.
>
> **Changing the port number**
> If you configure a virtual host to listen on a non-default port, make sure you update the **Listen** directive in the global settings section of the **/etc/httpd/conf/httpd.conf** file accordingly.
>
> To activate a newly created virtual host, the web server has to be restarted first.

#### Apache VirtualHost Example

Let's create a new virtualhost configuration. First let's create a new DNS entry for **rhel1-vh** in our **/etc/hosts** on both the client and the server:

Here is the server:

    [root@rhel1 ~]# ping -c 1 rhel1-vh
    PING rhel1.local.com (192.168.2.2) 56(84) bytes of data.
    64 bytes from rhel1.local.com (192.168.2.2): icmp_seq=1 ttl=64 time=0.040 ms
    
    --- rhel1.local.com ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.040/0.040/0.040/0.000 ms


and here is the client:

    [root@rhel2 ~]# ping -c 1 rhel1-vh
    PING rhel1.local.com (192.168.2.2) 56(84) bytes of data.
    64 bytes from rhel1.local.com (192.168.2.2): icmp_seq=1 ttl=64 time=0.138 ms
    
    --- rhel1.local.com ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.138/0.138/0.138/0.000 ms


So now **rhel1-vh** is pointing to our rhel6 machine. Now let's add a directory where we will host the virtualhost:

    [root@rhel1 ~]# mkdir /var/www/html/vh


and then add our test html file:

    [root@rhel1 ~]# cat /var/www/html/vh/index.html
    THIS IS RHEL1-VH RUNNING RH6! Under VH


Now let's create a virtualhost configuration to point to that directory:

    [root@rhel1 ~]# cat /etc/httpd/conf.d/rhel1-vh.conf
    NameVirtualHost rhel1-vh.local.com:80
    
    <VirtualHost rhel1-vh.local.com:80>
        ServerAdmin webmaster@local.com
        DocumentRoot /var/www/html/vh
        ServerName rhel1-vh.local.com:80
        ErrorLog logs/rhel1-vh.local.com-error_log
        CustomLog logs/rhel1-vh.local.com-access_log common
    </VirtualHost>


Now let's make sure our configuration is okay:

    [root@rhel1 ~]# service httpd configtest
    Syntax OK


Lastly restart the service:

    [root@rhel1 ~]# service httpd restart
    Stopping httpd: httpd
    Starting httpd:  httpd


Then connecting from the client to the new DNS name:

    [root@rhel2 ~]# elinks http://rhel1-vh


I saw the following:

![apache vh elinks RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/apache-vh-elinks.png)

### Apache SSL

From the same guide:

> Secure Sockets Layer (SSL) is a cryptographic protocol that allows a server and a client to communicate securely. Along with its extended and improved version called Transport Layer Security (TLS), it ensures both privacy and data integrity. The Apache HTTP Server in combination with **mod_ssl**, a module that uses the OpenSSL toolkit to provide the SSL/TLS support, is commonly referred to as the SSL server.
>
> Unlike a regular HTTP connection that can be read and possibly modified by anybody who is able to intercept it, the use of mod_ssl prevents any inspection or modification of the transmitted content. This section provides basic information on how to enable this module in the Apache HTTP Server configuration, and guides you through the process of generating private keys and self-signed certificates.

#### Enable SSL HTTP Module

From the above guide:

> If you intend to set up an SSL server, make sure you have the mod_ssl (the **mod_ssl** module) and openssl (the OpenSSL toolkit) packages installed. To do so, type the following at a shell prompt:
>
>     ~]# yum install mod_ssl openssl
>
>
> This will create the **mod_ssl** configuration file at **/etc/httpd/conf.d/ssl.conf**, which is included in the main Apache HTTP Server configuration file by default.
>
> If you wish to use an existing key and certificate, move the relevant files to the **/etc/pki/tls/private/** and **/etc/pki/tls/certs/** directories respectively. You can do so by typing the following commands:
>
>     ~]# mv key_file.key /etc/pki/tls/private/hostname.key
>     ~]# mv certificate.crt /etc/pki/tls/certs/hostname.crt
>
>
> Then add the following lines to the **/etc/httpd/conf.d/ssl.conf** configuration file:
>
>     SSLCertificateFile /etc/pki/tls/certs/hostname.crt
>     SSLCertificateKeyFile /etc/pki/tls/private/hostname.key
>
>
> To load the updated configuration, restart the httpd service

#### Generating New SSL Keys for Apache

From the Deployment Guide:

> In order to generate a new key and certificate pair, you must to have the **crypto-utils** package installed in your system. You can install it by typing the following at a shell prompt:
>
>     ~]# yum install crypto-utils
>
>
> This package provides a set of tools to generate and manage SSL certificates and private keys, and includes **genkey**, the Red Hat Keypair Generation utility that will guide you through the key generation process.
>
> To run the utility, use the **genkey** command followed by the appropriate hostname (for example, **penguin.example.com**):
>
>     ~]# genkey hostname
>
>
> Once generated, add the key and certificate locations to the **/etc/httpd/conf.d/ssl.conf** configuration file:
>
>     SSLCertificateFile /etc/pki/tls/certs/hostname.crt
>     SSLCertificateKeyFile /etc/pki/tls/private/hostname.key
>
>
> Finally, restart the **httpd** service

#### Setup an SSL Apache page

First let's install the SSL Apache module:

    [root@rhel1 ~]# yum install mod_ssl


Now let's check out the configuration that was installed with that package:

    [root@rhel1 ~]# grep -vE '^#|^$' /etc/httpd/conf.d/ssl.conf
    LoadModule ssl_module modules/mod_ssl.so
    Listen 443
    SSLPassPhraseDialog  builtin
    SSLSessionCache         shmcb:/var/cache/mod_ssl/scache(512000)
    SSLSessionCacheTimeout  300
    SSLMutex default
    SSLRandomSeed startup file:/dev/urandom  256
    SSLRandomSeed connect builtin
    SSLCryptoDevice builtin
    <VirtualHost _default_:443>
    ErrorLog logs/ssl_error_log
    TransferLog logs/ssl_access_log
    LogLevel warn
    SSLEngine on
    SSLProtocol all -SSLv2
    SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW
    SSLCertificateFile /etc/pki/tls/certs/localhost.crt
    SSLCertificateKeyFile /etc/pki/tls/private/localhost.key
    <Files ~ "\.(cgi|shtml|phtml|php3?)$">
        SSLOptions +StdEnvVars
    </Files>
    <Directory "/var/www/cgi-bin">
        SSLOptions +StdEnvVars
    </Directory>
    CustomLog logs/ssl_request_log \
              "%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x \"%r\" %b"
    </VirtualHost>


Looks like it creates yet another **virtualhost** to run on port **443** and it also uses existing SSL files:

    SSLCertificateFile /etc/pki/tls/certs/localhost.crt
    SSLCertificateKeyFile /etc/pki/tls/private/localhost.key


So let's go ahead and generate a new SSL pair. First let's install the **crypto-utils** package:

    [root@rhel1 ~]# yum install crypto-utils


Now let's run it:

    [root@rhel1 ~]# genkey rhel1.local.com


Then the wizard will start up:

![genkey p1 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p1.png)

After that you can choose the size of the private key (I went with 2048):

![genkey p2 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p2.png)

Then the generation of the private key will start:

![genkey p3 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p3.png)

If it takes a while to generate random data:

![genkey p4 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p4.png)

Then manually generate some random I/O:

    [root@rhel1 ~]# dd if=/dev/urandom of=test bs=1M count=231
    231+0 records in
    231+0 records out
    242221056 bytes (242 MB) copied, 49.9072 s, 4.9 MB/s


I had to run that a couple of times to get through the random data collection part. You can just loop through it a couple of times like so:

    [root@rhel1 ~]# for i in `seq 1 10`; do echo $i; dd if=/dev/urandom of=test$i bs=1M count=200; rm -f test$i; done


After it was done, it asked if I wanted to sent the CSR to a CA:

![genkey p5 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p5.png)

I just wanted to create a self signed SSL certificate, so I selected **NO** and then it wanted to encrypt the private key:

![genkey p6 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p6.png)

I opted out of that, since I didn't want to enter a passphase every single time I restarted apache. Then I entered the information regarding the server:

![genkey p7 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/genkey-p7.png)

After that the wizard stopped and I saw the following output:

    [root@rhel1 ~]# genkey rhel1.local.com
    /usr/bin/keyutil -c makecert -g 2048 -s "CN=rhel1.local.com, OU=RHEL LAB, O=Home, L=Boulder, ST=Colorado, C=US" -v 1 -a -z /etc/pki/tls/.rand.2539 -o /etc/pki/tls/certs/rhel1.local.com.crt -k /etc/pki/tls/private/local.com.key
    cmdstr: makecert
    
    cmd_CreateNewCert
    command:  makecert
    keysize = 2048 bits
    subject = CN=rhel1.local.com, OU=RHEL LAB, O=Home, L=Boulder, ST=Colorado, C=US
    valid for 1 months
    random seed from /etc/pki/tls/.rand.2539
    output will be written to /etc/pki/tls/certs/rhel1.local.com.crt
    output key written to /etc/pki/tls/private/rhel1.local.com.key


    Generating key. This may take a few moments...
    
    Made a key
    Opened tmprequest for writing
    (null) Copying the cert pointer
    Created a certificate
    Wrote 1682 bytes of encoded data to /etc/pki/tls/private/rhel1.local.com.key
    Wrote the key to:
    /etc/pki/tls/private/rhel1.local.com.key


Now that I have an SSL certificate for my server let's update the configuration to point to the newly created files. Here were the two lines that modified in the **/etc/httpd/conf.d/ssl.conf** file:

    [root@rhel1 ~]# grep ^SSLCertificate /etc/httpd/conf.d/ssl.conf
    SSLCertificateFile /etc/pki/tls/certs/rhel1.local.com.crt
    SSLCertificateKeyFile /etc/pki/tls/private/rhel1.local.com.key


Now let's check the configuration and list all the VirtualHosts:

    [root@rhel1 ~]# httpd -S
    VirtualHost configuration:
    192.168.2.2:80         is a NameVirtualHost
             default server rhel1-vh.local.com (/etc/httpd/conf.d/rhel1-vh.conf:3)
             port 80 namevhost rhel1-vh.local.com (/etc/httpd/conf.d/rhel1-vh.conf:3)
    wildcard NameVirtualHosts and _default_ servers:
    _default_:443          rhel1.local.com (/etc/httpd/conf.d/ssl.conf:74)
    Syntax OK


To just check the virtualhost configuration, you can run the following:

    [root@rhel1 ~]# httpd -D DUMP_VHOSTS
    VirtualHost configuration:
    192.168.2.2:80         is a NameVirtualHost
             default server rhel1-vh.local.com (/etc/httpd/conf.d/rhel1-vh.conf:3)
             port 80 namevhost rhel1-vh.local.com (/etc/httpd/conf.d/rhel1-vh.conf:3)
    wildcard NameVirtualHosts and _default_ servers:
    _default_:443          rhel1.local.com (/etc/httpd/conf.d/ssl.conf:74)
    Syntax OK


Finally let's restart the service:

    [root@rhel1 ~]# service httpd restart
    Stopping httpd: httpd
    Starting httpd:  httpd


and also let's open port 443 in the firewall:

    [root@rhel1 ~]# iptables -I INPUT 13 -m state --state NEW -m tcp -p tcp --dport 443 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now trying to connect from the client:

    [root@rhel2 ~]# elinks https://rhel1


I saw the following:

![rhel1 elinks https RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-elinks-https.png)

If you connect from an actual browser, you will notice that the connection is not trusted (broken lock), that's because we are using a self signed certificate:

![rhel1 https chrome RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-https-chrome.png)

You can also check the certificate information, by using **openssl**:

    [root@rhel2 ~]# openssl s_client -showcerts -connect rhel1:443
    CONNECTED(00000003)
    depth=0 /C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
    verify error:num=18:self signed certificate
    verify return:1
    depth=0 /C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
    verify return:1
    ---
    Certificate chain
     0 s:/C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
       i:/C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
    -----BEGIN CERTIFICATE-----
    MIIDVTCCAj2gAwIBAgIFAJ6VcGIwDQYJKoZIhvcNAQEEBQAwbDELMAkGA1UEBhMC
    VVMxETAPBgNVBAgTCENvbG9yYWRvMRAwDgYDVQQHEwdCb3VsZGVyMQ0wCwYDVQQK
    EwRIb21lMREwDwYDVQQLEwhSSEVMIExBQjEWMBQGA1UEAxMNcmhlbDEuZG5zZC5t
    ZTAeFw0xNDAzMTUyMTAzMDJaFw0xNDA0MTUyMTAzMDJaMGwxCzAJBgNVBAYTAlVT
    MREwDwYDVQQIEwhDb2xvcmFkbzEQMA4GA1UEBxMHQm91bGRlcjENMAsGA1UEChME
    SG9tZTERMA8GA1UECxMIUkhFTCBMQUIxFjAUBgNVBAMTDXJoZWwxLmRuc2QubWUw
    ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCwmpXmwYiVudwnDnKKSdUo
    6mKGMk/UmwqfmEZf00qKot52uTCPPuxO1sRvnWwk2v5mnhLB3FqJ6YF1cMzywhml
    e0aHJluvM8CpVItW1+6pX/4OD6k9CdODYbOZZBEM/rKa37mQCig8IXgaaKxtj6tU
    BJ3hqMUS2I1f+0UX38rBa5cDVGoe2cQPrvk2VwXCY5Ma8VhmVKHWYa+o6wN2oytu
    yveHTezIV77HzRYkJjklJ3xGi1EoGHLDs6vdRrKJL6rxEnLiCyqt/d1zIgXljdIA
    /lUUQPDd+73+jgIN9G0Rczbn4bxe42zrwr2kA8SoI/M1dE9cO2NXou+7yv+I+uYR
    AgMBAAEwDQYJKoZIhvcNAQEEBQADggEBAFzaubY9YvgKUKTiJNA+jE6OY+K8bT8D
    FSy6KTgFZ4z62+GhsdOLYLQbsOsB2D9N7SqLSQzh/6OLNf0ql+/+TNaM4eGCbu9I
    YCn1iYDTGO1GUbFNvGm1wEpWGqMJz1GW4219yLWjP2783wEqjT3J8EVzPIsGE9FJ
    iQghF9ZxSBvwcgagyOx9Pu3IAdeQoBOsUWDmTpHxYq5EmpYiRYccgFnBhZwO5d+A
    OsTEw/wh+0DhpepR2JfA98LMCa+ikMHh1nmFpQbw7lSSQr+P+Kq1UYIvFhpC/K9E
    HY/pJr8Mpq2Zs4hTIjBo5dCbJt0dbf/T8CpGy7Ft6bQCkd2jAbG7lfs=
    -----END CERTIFICATE-----
    ---
    Server certificate
    subject=/C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
    issuer=/C=US/ST=Colorado/L=Boulder/O=Home/OU=RHEL LAB/CN=rhel1.local.com
    ---
    No client certificate CA names sent
    ---
    SSL handshake has read 1556 bytes and written 319 bytes
    ---
    New, TLSv1/SSLv3, Cipher is DHE-RSA-AES256-SHA
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : DHE-RSA-AES256-SHA
        Session-ID: 5A52AADE872E8CC68B267059CB56B0B10CA98769B5EFBD8376C0311EA430457D
        Session-ID-ctx:
        Master-Key: BC9B805AF456AE1C5A527FCF12504AADCAA37015298CACFEAB51905EC73B52F89293625A7956C7F0E4A988E4F4B72B7F
        Key-Arg   : None
        Krb5 Principal: None
        Start Time: 1394918298
        Timeout   : 300 (sec)
        Verify return code: 18 (self signed certificate)
    ---


We can see that it's a self signed certificate.

## Squid Web Proxy

From [Managing Confined Services](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/managing_confined_services/red_hat_enterprise_linux-6-managing_confined_services-en-us.pdf):

> Squid is a high-performance proxy caching server for web clients, supporting FTP, Gopher, and HTTP data objects. It reduces bandwidth and improves response times by caching and reusing frequently-requested web pages.
>
> In Red Hat Enterprise Linux, the squid package provides the Squid Caching Proxy. Run the rpm -q squid command to see if the squid package is installed. If it is not installed and you want to use squid, run the following command as the root user to install it:
>
>     ~]# yum install squid
>

I also ran into a great RedHat Magazine article entitled [Squid in 5 minutes](http://magazine.redhat.com/2007/04/11/squid-in-5-minutes/). Here is the guide:

> There are many great tools that Squid has to offer, but when I need to redirect http traffic to a caching server for performance increases or security, squid’s my pick. Squid has built in proxy and caching tools that are simple, yet effective.
>
> I recently used Squid for a secure subnet that did not allow outgoing port 80 http access to external IP addresses. Many organizations will block external port 80 access at the router level. This is a great way to eliminate a huge security hole, but a headache when a systems administrator needs to reach the outside world temporarily to download a file. Another scenario: redirect all computers in a home network to a local caching server to increase website query performance and save on bandwidth.
>
> The situations described above are when the five minute Squid configuration comes in very handy. All requests for external http access can be handled by squid through a simple proxy configuration on each client machine. Sounds complicated? It isn’t. Let’s get into the details next.
>
> ### Install
>
> On a Red Hat Enterprise Linux or Fedora Core operating system, it is easy to check if Squid is installed using the rpm system. Type the command:
>
>     rpm -q squid
>
>
> If Squid is already installed, you will get a response similar to:
>
>     squid-2.5.STABLE6-3.4E.12
>
>
> If Squid isn’t installed, then you can use **Yum** to install it. Thanks to **Yum** the installation is quite easy.
>
> Just type at a command line:
>
>     yum install squid
>
>
> If you happen to have downloaded the **rpm** you can also type something like:
>
>     rpm -ivh squid-2.5.STABLE6-3.4E.12.i386.rpm
>
>
> ### Configure
>
> Squid’s main configuration file lives in **/etc/squid/squid.conf**. The 3,339 line configuration file is intimidating, but the good news is that it is very simple to setup a proxy server that forward http, https, and ftp requests to Squid on the default port of **3128** and caches the data.
>
> #### Back up the configuration file
>
> It is always good policy to backup a configuration file before you edit it. If you haven’t been burned yet, you haven’t edited enough configuration files. Make a backup from the command line or the gui and rename the original file something meaningful. I personally like to append a **bck.datestamp**. For example:
>
>     cp /etc/squid/squid.conf /etc/squid/squid.conf.bck.02052007
>
>
> If it is the original configuration file you might choose to do:
>
>     cp /etc/squid/squid.conf /etc/squid/squid.conf.org.02052007
>
>
> ### Edit the file
>
> Open **/etc/squid/squid.conf** with your favorite text editor. I use **vim**, but **nano** is a good beginner’s command line text editor. If you do use **nano**, make sure you use the **nano –nowrap** option to turn off line wrapping when editing things like configuration files. A gui editor like **Gedit** will also work.
>
> ### Five minute configuration
>
> There are many fancy options for squid that we will not enable, specifically acls (access control lists) or authentication. We are going to set up a caching proxy server with no access control. This server would be suitable for a home network behind a firewall.
>
> The default squid configuration is almost complete, but a few small changes should be made. You will need to either find and uncomment entries, or modify existing uncommented lines in the squid configuration file. Use your favorite text editor or a text find to quickly locate these lines:
>
>     visible_hostname machine-name
>     http_port 3128
>     cache_dir ufs /var/spool/squid 1000 16 256
>     cache_access_log /var/log/squid/access.log
>
>
> In the acl section near the bottom add:
>
>     acl intranet 192.168.0.0/24
>     http_access allow intranet
>
>
> Let me explain what each of these six lines means:
>
> **visible_hostname** – Create this entry and set this to the hostname of the machine. To find the hostname, use the command hostname. Not entering a value may cause squid to fail as it may not be able to automatically determine the fully qualified hostname of your machine.
>
> **http_port 3128** – Uncomment this line but there is no need to edit it unless you want to change the default port for http connections.
>
> **cache_dir ufs /var/spool/squid 1000 15 256** – Uncomment this line. You may want to append a zero to the value 100 which will make the cache size 1000MB instead of 100MB. The last two values stand for the default folder depth the cache will create on the top and subdirectories respectively. They do not need modification.
>
> **cache_access_log** – Uncomment this line. This is where all requests to the proxy server will get logged.
>
> **acl intranet 192.168.0.0/24** – This entry needs to be added. It should correspond to whatever your local network range is. For example, if your Fedora server is 192.168.2.5 then the entry should be acl intranet 192.168.2.0/24
>
> **http_access allow intranet** – This allows the acl named intranet to use the proxy server. Make sure to put allow directives above the last ‘http_access deny all’ entry, as it will overide any allow directives below it.
>
> ### Turning on squid
>
> Enable the proper run levels:
>
>     chkconfig squid on
>
>
> Start the service:
>
>     service squid start
>
>
> Verify that squid is running:
>
>     service squid status
>
>
> Note, if you have problems starting squid, open a separate shell and run:
>
>     tail -f /var/log/messages
>
>
> Then start the squid service in your original window:
>
>     service squid start
>
>
> The **tail** command should show an error for squid that can help you solve the problem. One common error is that the swap (cache) directory doesn’t exist. To solve this problem, run squid with the **-z** option to automatically create the directories:
>
>     /usr/sbin/squid -z
>
>
> Make sure that squid has write permission to the swap directory or this command won’t work.
>
> ### Configuring the clients
>
> If you are using Firefox or Mozilla you will need to add the proxy server as follows:
>
>     Go to Preferences>Network>Settings
>
>
> Add the name of your new proxy server and port 3128 to the http proxy field (under manual configuration).
>
> Open a shell to your proxy server so you can observe the log file being written to. Use **tail**, as before:
>
>     tail -f /var/log/squid/access.log
>
>
> Now surf the web through your proxy server. You should see entries flying by in real time as you surf different http addresses. Congratulations, you now have a caching proxy server setup!

### Squid Example

So let's try this out. First let's block port 80 traffic to our RHEL6 machine, in our example we will reach the above sites that we created via the squid proxy. To remove the rule, run the following:

    [root@rhel1 ~]# iptables -D INPUT 12


Now from our rhel5 machine, let's try to connect to our site with **elinks**:

    [root@rhel2 ~]# elinks http://rhel1-vh


and I got the following error:

![rhel1 elinks blocked2 RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/rhel1-elinks-blocked2.png)

Now on the RH6 machine let's install **squid**:

    [root@rhel1 ~]# yum install squid


Checking out the default configuration, here is what I saw:

    [root@rhel1 ~]# grep -Ev '^$|^#' /etc/squid/squid.conf
    acl manager proto cache_object
    acl localhost src 127.0.0.1/32 ::1
    acl to_localhost dst 127.0.0.0/8 0.0.0.0/32 ::1
    acl localnet src 10.0.0.0/8 # RFC1918 possible internal network
    acl localnet src 172.16.0.0/12  # RFC1918 possible internal network
    acl localnet src 192.168.0.0/16 # RFC1918 possible internal network
    acl localnet src fc00::/7       # RFC 4193 local private network range
    acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines
    acl SSL_ports port 443
    acl Safe_ports port 80      # http
    acl Safe_ports port 21      # ftp
    acl Safe_ports port 443     # https
    acl Safe_ports port 70      # gopher
    acl Safe_ports port 210     # wais
    acl Safe_ports port 1025-65535  # unregistered ports
    acl Safe_ports port 280     # http-mgmt
    acl Safe_ports port 488     # gss-http
    acl Safe_ports port 591     # filemaker
    acl Safe_ports port 777     # multiling http
    acl CONNECT method CONNECT
    http_access allow manager localhost
    http_access deny manager
    http_access deny !Safe_ports
    http_access deny CONNECT !SSL_ports
    http_access allow localnet
    http_access allow localhost
    http_access deny all
    http_port 3128
    hierarchy_stoplist cgi-bin ?
    coredump_dir /var/spool/squid
    refresh_pattern ^ftp:       1440    20% 10080
    refresh_pattern ^gopher:    1440    0%  1440
    refresh_pattern -i (/cgi-bin/|\?) 0 0%  0
    refresh_pattern .       0   20% 4320


It looks like we have an ACL for our network:

    acl localnet src 192.168.0.0/16


and we also allow HTTP access for that network:

    http_access allow localnet


and the port is setup to be 3128:

    http_port 3128


Let's start it up and see if it starts up:

    [root@rhel1 ~]# service squid start
    Starting squid: .[  OK  ]
    [root@rhel1 ~]# service squid status
    squid (pid  8960) is running...


Now let's open up port **3128** on the firewall:

    [root@rhel1 ~]# iptables -I INPUT 13 -m state --state NEW -m tcp -p tcp --dport 3128 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now let's configure the rhel5 machine to go through the proxy:

    [root@rhel2 ~]# http_proxy=rhel1:3128 elinks http://rhel1-vh


and I was able to see the page:

![elinks thru squid proxy RHCSA and RHCE Chapter 14 – Web Services](https://github.com/elatov/uploads/raw/master/2014/03/elinks-thru-squid-proxy.png)

Looking at the **access.log**, I saw the following:

    [root@rhel1 squid]# tail access.log
    1394926079.928      2 192.168.2.3 TCP_MISS/200 431 GET http://rhel1-vh/ - DIRECT/192.168.2.2 text/html
    1394926115.289      0 192.168.2.3 TCP_MEM_HIT/200 438 GET http://rhel1-vh/ - NONE/- text/html


Notice the first time I got a TCP_MISS (this was my first visit), and the next I hit the Cache. But both times I was able to reach a web site going through the proxy. Also checking out the access log on the apache side, I saw the following:

    [root@rhel1 ~]# tail /var/log/httpd/rhel1-vh.dnsd.me-access_log
    192.168.1.107 - - [15/Mar/2014:14:05:17 -0600] "HEAD / HTTP/1.1" 200 -
    192.168.1.107 - - [15/Mar/2014:14:05:20 -0600] "GET / HTTP/1.1" 200 39
    192.168.1.107 - - [15/Mar/2014:14:05:20 -0600] "GET /favicon.ico HTTP/1.1" 404 284
    192.168.2.3 - - [15/Mar/2014:14:08:25 -0600] "GET / HTTP/1.1" 200 39
    192.168.2.2 - - [15/Mar/2014:17:27:47 -0600] "GET / HTTP/1.1" 200 39
    192.168.2.2 - - [15/Mar/2014:17:27:59 -0600] "GET / HTTP/1.1" 200 39


The bottom two are the once going through the proxy and we can see that the IP (**192.168.2.2**) is the same as the server it self. This makes sense since the proxy server is running locally.

/
