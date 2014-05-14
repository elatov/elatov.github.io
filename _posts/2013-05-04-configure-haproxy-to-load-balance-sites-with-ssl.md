---
title: Configure HAProxy to Load Balance Sites With SSL
author: Karim Elatov
layout: post
permalink: /2013/05/configure-haproxy-to-load-balance-sites-with-ssl/
dsq_thread_id:
  - 1405283642
categories:
  - Home Lab
tags:
  - HAproxy
  - Load Balancing
  - SSL Termination
---
Starting with **HAproxy** version 1.5, SSL is supported. From the main <a href="http://haproxy.1wt.eu/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://haproxy.1wt.eu/']);">Haproxy</a> site:

> Update [2012/09/11] : native SSL support was implemented in 1.5-dev12.

## Prepare System for the HAProxy Install

I was using CentOS for my setup, here is the version of my CentOS install:

    [root@haproxy ~]# lsb_release -a
    LSB Version:    :base-4.0-amd64:base-4.0-noarch:core-4.0-amd64:core-4.0-noarch
    Distributor ID: CentOS
    Description:    CentOS release 6.4 (Final)
    Release:    6.4
    Codename:   Final
    

Since we have to compile the latest version of HAProxy, let&#8217;s go ahead and install the *Development Tools* group package:

    [root@haproxy ~]# yum grouplist -v "development" | grep tools
       Development tools (development)
    [root@haproxy ~]# yum install @development
    

We will also need the **openssl** source files:

    [root@haproxy ~]# yum install openssl-devel
    

## Compile the Latest Version of HAProxy

First go ahead and download the latest version (the download link can be found <a href="http://haproxy.1wt.eu/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://haproxy.1wt.eu/']);">here</a>):

    [root@haproxy ~]# wget http://haproxy.1wt.eu/download/1.5/src/devel/haproxy-1.5-dev18.tar.gz
    --2013-05-04 12:44:42--  http://haproxy.1wt.eu/download/1.5/src/devel/haproxy-1.5-dev18.tar.gz
    Resolving haproxy.1wt.eu... 88.191.124.161, 2a01:e0b:1:124:ca0a:a9ff:fe03:3c37
    Connecting to haproxy.1wt.eu|88.191.124.161|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1132317 (1.1M) [application/x-gzip]
    Saving to: “haproxy-1.5-dev18.tar.gz”
    
    100%[======================================>] 1,132,317   14.2K/s   in 2m 25s  
    
    2013-05-04 12:47:10 (7.62 KB/s) - “haproxy-1.5-dev18.tar.gz” saved [1132317/1132317]
    

Let&#8217;s extract the source code and go inside the source directory:

    [root@haproxy ~]# tar xzf haproxy-1.5-dev18.tar.gz 
    [root@haproxy ~]# cd haproxy-1.5-dev18
    [root@haproxy haproxy-1.5-dev18]#
    

To compile the software run the following:

    [root@haproxy haproxy-1.5-dev18]# make TARGET=linux26 USE_OPENSSL=1 ADDLIB=-lz
    

After the compile is done, make sure the binary is linked to the **openssl** library:

    [root@haproxy haproxy-1.5-dev18]# ldd haproxy | grep ssl
        libssl.so.10 => /usr/lib64/libssl.so.10 (0x00007fb0485e5000)
    

That looks good, now let&#8217;s install the binary:

    [root@haproxy haproxy-1.5-dev18]# make PREFIX=/usr/local/haproxy install
    install -d /usr/local/haproxy/sbin
    install haproxy /usr/local/haproxy/sbin
    install haproxy-systemd-wrapper /usr/local/haproxy/sbin
    install -d /usr/local/haproxy/share/man/man1
    install -m 644 doc/haproxy.1 /usr/local/haproxy/share/man/man1
    install -d /usr/local/haproxy/doc/haproxy
    for x in configuration architecture haproxy-en haproxy-fr; do \
            install -m 644 doc/$x.txt /usr/local/haproxy/doc/haproxy ; \
        done
    

## Configure HAProxy to Load Balance

There are actually a couple approaches to Load balancing SSL. The most popular is *SSL Termination*, here are sample configurations of HAProxy that do exactly that:

*   <a href="https://tech.shareaholic.com/2012/10/26/haproxy-a-substitute-for-amazon-elb/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://tech.shareaholic.com/2012/10/26/haproxy-a-substitute-for-amazon-elb/']);">Using HAProxy to Build a More Featureful Elastic Load Balancer</a>
*   <a href="http://blog.hintcafe.com/post/33851388857/haproxy-ssl-configuration-explained" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.hintcafe.com/post/33851388857/haproxy-ssl-configuration-explained']);">Haproxy SSL configuration explained</a>
*   <a href="http://blog.exceliance.fr/2012/09/10/how-to-get-ssl-with-haproxy-getting-rid-of-stunnel-stud-nginx-or-pound/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.exceliance.fr/2012/09/10/how-to-get-ssl-with-haproxy-getting-rid-of-stunnel-stud-nginx-or-pound/']);">How to get SSL with HAProxy getting rid of stunnel, stud, nginx or pound</a>
*   <a href="http://blog.exceliance.fr/2012/10/03/ssl-client-certificate-management-at-application-level/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.exceliance.fr/2012/10/03/ssl-client-certificate-management-at-application-level/']);">SSL Client certificate management at application level</a>
*   <a href="http://blog.davidmisshula.com/blog/2013/02/04/configure-haproxy-to-scale-multiple-nodes-with-stickiness-and-ssl/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.davidmisshula.com/blog/2013/02/04/configure-haproxy-to-scale-multiple-nodes-with-stickiness-and-ssl/']);">Configure HAProxy to Scale Socket.io Node.js Apps With SSL</a>

Here are some links that explain why SSL termination can be advantageous:

*   <a href="http://www.lullabot.com/blog/articles/setting-ssl-offloading-termination-f5-big-ip-load-balancer" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.lullabot.com/blog/articles/setting-ssl-offloading-termination-f5-big-ip-load-balancer']);">Setting up SSL Offloading (Termination) on an F5 Big-IP Load Balancer</a> 
*   <a href="http://blog.filepicker.io/post/29422604907/improved-https-performance-with-early-ssl-termination" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.filepicker.io/post/29422604907/improved-https-performance-with-early-ssl-termination']);">Improved HTTPS Performance with Early SSL Termination</a>

Some excepts from the above links:

> Instead of distributing our web servers, we did the next best thing: distributing where we terminated our SSL connections. By cutting down all the round trip times except the HTTP request, we can theoretically save 3*96ms = 288ms of latency.
> 
> &#8230;.
> 
> One of the primary reasons for investing in an F5 is for the purpose of SSL Offloading, that is, converting external HTTPS traffic into normal HTTP traffic so that your web servers don&#8217;t need to do the work themselves. HTTPS requests (and more specifically, the SSL handshaking to start the connection) is incredibly expensive, often on the magnitude of at least 10 times slower than normal HTTP requests.

### Configure HAProxy to Load Balance Site with SSL Termination

Here is a very simple configuration that I ended up using:

    [root@haproxy ~]# cat /etc/haproxy.cfg
      global
      log 127.0.0.1 local0
      maxconn 4000
      daemon
      uid 99
      gid 99
    
    defaults
      log     global
      mode    http
      option  httplog
      option  dontlognull
      timeout server 5s
      timeout connect 5s
      timeout client 5s
      stats enable
      stats refresh 10s
      stats uri /stats
    
    frontend https_frontend  
      bind *:443 ssl crt /etc/ssl/certs/elatov-local-cert-key.pem
      mode http
      option httpclose
      option forwardfor
      reqadd X-Forwarded-Proto:\ https
      default_backend web_server
    
    backend web_server
      mode http
      balance roundrobin
      cookie SERVERID insert indirect nocache
      server s1 192.168.250.47:80 check cookie s1
      server s2 192.168.250.49:80 check cookie s2
    

**Note:** The SSL CRT file is a combination of the public certificate and the private key. I used the same SSL files that I generated in this blog <a href="http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/']);">post</a>. Here is the command I ran to concatenate the files together:

*   `$ cat wild-elatov-local-cert.pem wild-elatov-local-priv-key.pem > elatov-local-cert-key.pem`

Going directly to the servers with **curl**, here is what we see in the headers:

    [root@haproxy ~]# curl -I http://192.168.250.47
    HTTP/1.1 200 OK
    Content-Length: 689
    Content-Type: text/html
    Last-Modified: Sun, 07 Apr 2013 19:12:27 GMT
    Accept-Ranges: bytes
    ETag: "8216ffd7c333ce1:0"
    Server: Microsoft-IIS/7.5
    Date: Sat, 04 May 2013 20:58:24 GMT
    
    [root@haproxy ~]# curl -I http://192.168.250.49
    HTTP/1.1 200 OK
    Content-Length: 689
    Content-Type: text/html
    Last-Modified: Sun, 14 Apr 2013 04:04:49 GMT
    Accept-Ranges: bytes
    ETag: "cfc32e35c538ce1:0"
    Server: Microsoft-IIS/7.5
    Date: Sat, 04 May 2013 20:58:39 GMT
    

Now checking to make sure our **haproxy** configuration is okay:

    [root@haproxy ~]# /usr/local/haproxy/sbin/haproxy -c -f /etc/haproxy.cfg 
    Configuration file is valid
    

That is all good, now let&#8217;s go ahead and start up **haproxy**:

    [root@haproxy ~]# /usr/local/haproxy/sbin/haproxy -f /etc/haproxy.cfg 
    

Lastly let&#8217;s make sure it&#8217;s listening on the expected port:

    [root@haproxy ~]# lsof -i tcp:443
    COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    haproxy 16332 nobody    4u  IPv4  51979      0t0  TCP *:https (LISTEN)
    

Now let&#8217;s see what happens with **curl**:

    [root@haproxy ~]# curl -k -L -I  https://192.168.250.52
    HTTP/1.1 200 OK
    Content-Length: 13
    Content-Type: text/html
    Last-Modified: Sun, 14 Apr 2013 03:49:16 GMT
    Accept-Ranges: bytes
    ETag: "facd179c338ce1:0"
    Server: Microsoft-IIS/7.5
    Date: Sat, 04 May 2013 21:27:57 GMT
    Set-Cookie: SERVERID=s1; path=/
    Cache-control: private
    

After visiting the site a couple of times, I saw the following statistic page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/haproxy_stats.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/haproxy_stats.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/haproxy_stats.png" alt="haproxy stats Configure HAProxy to Load Balance Sites With SSL" width="970" height="382" class="alignnone size-full wp-image-8676" title="Configure HAProxy to Load Balance Sites With SSL" /></a>

We can see that the round robin is working pretty well. I ended up using **Session Cookies** for persistence (we can see the **Set-Cookie** header set). Other load-balancing examples can be seen at &#8220;<a href="http://blog.exceliance.fr/2012/03/29/load-balancing-affinity-persistence-sticky-sessions-what-you-need-to-know/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.exceliance.fr/2012/03/29/load-balancing-affinity-persistence-sticky-sessions-what-you-need-to-know/']);">Load balancing, affinity, persistence, sticky sessions: what you need to know</a>&#8220;. This is the same setup that I used for my <a href="http://virtuallyhyper.com/2013/04/load-balancing-iis-sites-with-nlb/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/load-balancing-iis-sites-with-nlb/']);">NLB</a> post. So when I visited the **test.html** page, I saw the following:

    [root@haproxy ~]# date; curl -k -L https://192.168.250.52
    Sat May  4 14:14:28 MDT 2013
    This is IIS-1
    [root@haproxy ~]# date; curl -k -L https://192.168.250.52
    Sat May  4 14:14:31 MDT 2013
    This is IIS-2
    

While I was testing, I checked out the logs and I saw the interactions logged:

    [root@haproxy log]# tail -1 messages 
    May  4 14:18:19 localhost haproxy[16344]: 192.168.101.47:58781 [04/May/2013:14:18:14.757] https_frontend~ web_server/s2 20/0/2/3/5026 200 236 - - cD-- 0/0/0/0/0 0/0 "GET /test.html HTTP/1.1"
    

Lastly to make sure the **X-Forwarded-For** header was working, I ran the following command on the *haproxy* machine:

    [root@haproxy ~]# tcpdump -i eth0 -s 1024 -A tcp port 80
    

and I saw the following in the packet capture:

    15:16:19.937463 IP 192.168.250.52.32788 > 192.168.250.49.http: Flags [P.], seq 1:354, ack 1, win 229, options [nop,nop,TS val 10520125 ecr 854233], length 353
    E...t.@.@.N....4...1...P....nR3\....w?.....
    ..GET /favicon.ico HTTP/1.1
    Host: 192.168.250.52
    User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    X-Forwarded-Proto: https
    X-Forwarded-For: 192.168.101.47
    Connection: close
    

So everything was working as expected. A lot of application depend on the **X-Forwarded-For** Header to Access Control Lists.

The setup was pretty slick and really easy to configure.

### Configure HAProxy to Load Balance Site with SSL PassThrough

Another method of load balancing SSL is to just pass through the traffic. With this approach since everything is encrypted, you won&#8217;t be able to monitor and tweak HTTP headers/traffic. Here are a couple of sample setups:

*   <a href="http://blog.exceliance.fr/2011/07/12/send-user-to-the-same-backend-for-both-http-and-https/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.exceliance.fr/2011/07/12/send-user-to-the-same-backend-for-both-http-and-https/']);">Send user to the same backend for both HTTP and HTTPS</a>
*   <a href="http://blog.exceliance.fr/2011/07/04/maintain-affinity-based-on-ssl-session-id/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.exceliance.fr/2011/07/04/maintain-affinity-based-on-ssl-session-id/']);">Maintain affinity based on SSL session ID</a>
*   <a href="http://cbonte.github.io/haproxy-dconv/configuration-1.5.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://cbonte.github.io/haproxy-dconv/configuration-1.5.html']);">HAProxy Configuration Manual</a>

Here is the config I chose:

    [root@haproxy log]# cat /etc/haproxy.cfg
    global
      log 127.0.0.1 local0
      maxconn 4000
      daemon
      uid 99
      gid 99
    
    defaults
      log     global
      timeout server 5s
      timeout connect 5s
      timeout client 5s
    
    frontend https_frontend  
      bind *:443
      mode tcp
      default_backend web_server
    
    backend web_server
      mode tcp
      balance roundrobin
      stick-table type ip size 200k expire 30m
      stick on src
      server s1 192.168.250.47:443
      server s2 192.168.250.49:443
    

With the above setup, it uses the Source IP for affinity. So when I tried two connections it went to same host:

    [root@haproxy ~]# date ; curl -k https://192.168.250.52
    Sat May  4 17:08:41 MDT 2013
    This is IIS-1
    [root@haproxy ~]# date ; curl -k https://192.168.250.52
    Sat May  4 17:08:42 MDT 2013
    This is IIS-1
    

If you want &#8220;real&#8221; load-balancing of HTTPS sessions, you can use this configuration (taken from <a href="http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-stick%20store-response" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-stick%20store-response']);">HAProxy Configuration Manual &#8211; Stick store-response</a>):

    [root@haproxy log]# cat /etc/haproxy.cfg
    global
      log 127.0.0.1 local0
      maxconn 4000
      daemon
      uid 99
      gid 99
      stats socket /tmp/haproxy.stats level admin
    
    defaults
      log     global
      timeout server 5s
      timeout connect 5s
      timeout client 5s
    
    frontend https_frontend  
      bind *:443
      mode tcp
      default_backend web_server
    
    backend web_server
      mode tcp
      balance roundrobin
      stick-table type binary len 32 size 30k expire 30m
    
      acl clienthello req_ssl_hello_type 1
      acl serverhello rep_ssl_hello_type 2
    
      tcp-request inspect-delay 5s
      tcp-request content accept if clienthello
    
      tcp-response content accept if serverhello
      stick on payload_lv(43,1) if clienthello
      stick store-response payload_lv(43,1) if serverhello
    
      server s1 192.168.250.47:443
      server s2 192.168.250.49:443
    

Trying to connect with **curl**, it load-balanced:

    [root@haproxy ~]# date ; curl -k https://192.168.250.52
    Sat May  4 17:14:19 MDT 2013
    This is IIS-1
    [root@haproxy ~]# date ; curl -k https://192.168.250.52
    Sat May  4 17:14:21 MDT 2013
    This is IIS-2
    

In the logs, I just saw the following:

    [root@haproxy log]# tail -1 messages 
    May  4 17:04:49 localhost haproxy[16749]: Connect from 192.168.250.52:35542 to 192.168.250.52:443 (https_frontend/TCP)
    

Again since this is encrypted, we won&#8217;t see as much information. Here are how the headers looked like in *Google Chrome* with *Developer Tools* under the *Network* tab:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/chrome-with-haproxy-headers.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/chrome-with-haproxy-headers.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/chrome-with-haproxy-headers.png" alt="chrome with haproxy headers Configure HAProxy to Load Balance Sites With SSL" width="993" height="707" class="alignnone size-full wp-image-8695" title="Configure HAProxy to Load Balance Sites With SSL" /></a>

Lastly, after I connected a couple of times, I saw the following stats:

    [root@haproxy ~]# echo "show table web_server" | socat unix-connect:/tmp/haproxy.stats stdio
    # table: web_server, type: binary, size:30720, used:6
    0x18a1ff4: key=160D0000AF0C use=0 exp=1798448 server_id=2
    0x18a1e54: key=272E00009969 use=0 exp=1731048 server_id=2
    0x18a1d84: key=8D4300007167 use=0 exp=1568181 server_id=1
    0x18993e4: key=B94700003E52 use=0 exp=1258469 server_id=2
    0x1899314: key=C72800008651 use=0 exp=1255548 server_id=1
    0x18a1f24: key=DB0200001F65 use=0 exp=1797731 server_id=1
    

We can see that multiple servers are utilized.

