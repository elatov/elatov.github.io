---
title: Blitz.io Tests Against Apache Worker, Apache Prefork, Apache with PHP-FPM, and Nginx with PHP-FPM in a 256MB RAM VPS
author: Karim Elatov
layout: post
permalink: /2012/09/blitz-io-tests-against-apache-worker-apache-prefork-apache-with-php-fpm-and-nginx-with-php-fpm/
categories: ['os']
tags: ['performance', 'linux', 'apache', 'blitz_io', 'fastcgi', 'nginx', 'php', 'vps']
---

We were setting up a VPS with 256MB of RAM and we were trying to figure out which Web Server to use for our limited VPS. You will see many posts out there mentioning that Apache uses a lot more memory than any other Web Server:

*   [Apache vs nginx](http://www.wikivs.com/wiki/Apache_vs_nginx)
*   [Setup NginX Web Server (Not Apache!) on Ubuntu 10.04](http://www.idolbin.com/blog/server-management/vps-setup-guide/setup-nginx-web-server-not-apache-on-ubuntu-10-04/)
*   [WordPress Hosting: Apache or Nginx?](http://wpforce.com/wordpress-hosting-apache-or-nginx/)
*   [nginx vs cherokee vs apache vs lighttpd](http://www.whisperdale.net/11-nginx-vs-cherokee-vs-apache-vs-lighttpd.html)

You can find many others as well. So I decided to run some of my own tests, to see what the hype is about. First off, I will admit I really like Apache. It's simple, it works, and it's secure. Secondly, if we are going to test with performance we should use MPM (Multi-Processing Modules). From "[Multi-Processing Modules](http://httpd.apache.org/docs/2.4/mpm.html)" Apache page:

> Apache 2.0 extends this modular design to the most basic functions of a web server. The server ships with a selection of Multi-Processing Modules (MPMs) which are responsible for binding to network ports on the machine, accepting requests, and dispatching children to handle the requests.

There are actually 3 different MPM modules, from "[Apache Performance Tuning](http://httpd.apache.org/docs/2.4/misc/perf-tuning.html)" page:

> **Choosing an MPM**
> Apache 2.x supports pluggable concurrency models, called Multi-Processing Modules (MPMs). When building Apache, you must choose an MPM to use. There are platform-specific MPMs for some platforms: mpm_netware, mpmt_os2, and mpm_winnt. For general Unix-type systems, there are several MPMs from which to choose. The choice of MPM can affect the speed and scalability of the httpd:
>
> *   The **worker** MPM uses multiple child processes with many threads each. Each thread handles one connection at a time. Worker generally is a good choice for high-traffic servers because it has a smaller memory footprint than the prefork MPM.
> *   The **event** MPM is threaded like the Worker MPM, but is designed to allow more requests to be served simultaneously by passing off some processing work to supporting threads, freeing up the main threads to work on new requests.
> *   The **prefork** MPM uses multiple child processes with one thread each. Each process handles one connection at a time. On many systems, prefork is comparable in speed to worker, but it uses more memory. Prefork's threadless design has advantages over worker in some situations: it can be used with non-thread-safe third-party modules, and it is easier to debug on platforms with poor thread debugging support.

I only tested with the **prefork** and **worker** modules, since the **event** module is still experimental, from "[Apache MPM event](http://httpd.apache.org/docs/2.2/mod/event.html)" page:

> Warning This MPM is experimental, so it may or may not work as expected.

I might test with it, when it becomes stable. To check out what MPM module is currently compiled into your Apache server you can run **apache2ct -l**, like so:

    $ apache2ctl -l
    Compiled in modules:
    core.c
    prefork.c
    http_core.c
    mod_so.c


We can see that in this case it's **prefork** (you can also use **httpd -l** to find out the same information). There are also a lot of sites that have different recommendations on how to tune the *prefork* module:

*   [Apache, Configuring](http://www.freebsdwiki.net/index.php/Apache,_Configuring)
*   [Configuring the Apache MPM on Ubuntu](http://articles.slicehost.com/2010/5/19/configuring-the-apache-mpm-on-ubuntu)
*   [Running Apache On A Memory-Constrained VPS](http://www.kalzumeus.com/2010/06/19/running-apache-on-a-memory-constrained-vps/)
*   [Tuning the Apache Prefork MPM](http://www.hosting.com/support/linux/tuning-the-apache-prefork-mpm)
*   [Performance recommendations](http://docs.moodle.org/23/en/Performance_recommendations)

The best recommendations I found were the following:

> A simple calculation for MaxClients would be:
> (Total Memory – Critical Services Memory) / Size Per Apache process .. ..
>
> Set the **MaxClients** directive correctly. Use this formula to help (which uses 80% of available memory to leave room for spare):
> MaxClients = Total available memory * 80% / Max memory usage of apache process

When I ran a regular [blitz.io](http://blitz.io) against our server and fired up **top**, I noticed that when the server is getting pushed each *apache* process would take up 24MB of memory. So by our equation: 256MB *x* 0.8 / 24MB, we get about **8**. So our **MaxClients** for *prefork* should be around 8. With that setting in mind, I setup the following configuration:

    StartServers        2
    MinSpareServers     2
    MaxSpareServers     4
    MaxClients          8
    ServerLimit         8
    MaxRequestsPerChild   100


I also compiled **mod_php**, installed **mariadb**, and setup **wordpress**. Then I went to [blitz.io](http://blitz.io/) and started load testing apache with *prefork* MPM. At first I only did the following test:

> -p 1-10:60 mysite.com

This will send 1-10 request at out server for 60 seconds. The results were the following:

> 166 HITS WITH 0 ERRORS & 29 TIMEOUTS

I was getting a lot of time outs already. So then I decided to increase the **MaxRequestsPerChild** variable to a 1000 and then re-ran the test and I got the following:

> 190 HITS WITH 0 ERRORS & 12 TIMEOUTS

That actually looked pretty good. I then increased the load and ran the following test:

> -p 1-20:60 mysite.com

and got the following results:

> 146 HITS WITH 0 ERRORS & 181 TIMEOUTS

Now I am getting more time-outs than hits, that is not good. As I was running the test, I noticed that *apache* was firing 8 processes to take care of the load. Since this was a VPS and I was limited on resources, I decided to half my settings:

    StartServers        1
    MinSpareServers     1
    MaxSpareServers     2
    MaxClients          4
    ServerLimit         4
    MaxRequestsPerChild   1000


Ran this test:

> -p 1-10:60 mysite.com

and got the following:

> 195 HITS WITH 0 ERRORS & 12 TIMEOUTS

That is actually not too bad. Then running this test:

> -p 1-20:60

and got the following results:

> 123 HITS WITH 0 ERRORS & 189 TIMEOUTS

Same thing as before, getting more time-outs than hits. Here are some tests that I ran afterwards:

> StartServers 1
> MinSpareServers 1
> MaxSpareServers 2
> MaxClients 20
> ServerLimit 20
> MaxRequestsPerChild 1000
>
> -p 1-20:60 mysite.com
>
> **Results**
> 104 HITS WITH 0 ERRORS & 211 TIMEOUTS
>
> StartServers 5
> MinSpareServers 5
> MaxSpareServers 10
> MaxClients 20
> ServerLimit 20
> MaxRequestsPerChild 1000
>
> -p 1-20:60 mysite.com
>
> **Results**
> 125 HITS WITH 0 ERRORS & 198 TIMEOUTS
>
> StartServers 2
> MinSpareServers 2
> MaxSpareServers 4<br . /> MaxClients 8
> ServerLimit 8
> MaxRequestsPerChild 2000
>
> -p 1-20:60 mysite.com
>
> **Results**
> 161 HITS WITH 0 ERRORS & 160 TIMEOUTS

As you can see increasing **StartServers**, **MaxClients**, **MaxRequestsPerChild**, didn't really help out. The VPS came to a crawl when I increased the **MaxClients** to 20. My sweet spot was the following:

    StartServers        1
    MinSpareServers     1
    MaxSpareServers     2
    MaxClients          4
    ServerLimit         4
    MaxRequestsPerChild   1000


And we could handle about 200 hits per minute when receiving 10 simultaneous requests. Let's move onto Apache with **worker** MPM and **mod_php**. Since we were using FreeBSD it was was pretty easy to compile the new version of *apache*. I did have to recompile PHP as well and the PHP extensions. But overall it took about 15 minutes for the whole process. I tried to apply the same logic for the **worker** module as I did with the **prefork** module, so initially I had the following setup:

    StartServers           1
    MinSpareThreads        1
    MaxSpareThreads        2
    ThreadsPerChild        4
    MaxRequestsPerChild    1000
    MaxClients             8
    ServerLimit            2


Then running the following test:

> -p 1-20:60 mysite.com

The results were the following:

> 503 HITS WITH 0 ERRORS & 1 TIMEOUTS

Compared to **prefork** this is great, but I kept increasing the load until this test:

> -p 1-70:60 mysite.com

and I got the following results:

> 1,268 HITS WITH 0 ERRORS & 122 TIMEOUTS

That is when I decided to read up on the worker MPM to see what values I should use. From "[Apache MPM worker](http://httpd.apache.org/docs/2.2/mod/worker.html)":

> The most important directives used to control this MPM are ThreadsPerChild, which controls the number of threads deployed by each child process and MaxClients, which controls the maximum total number of threads that may be launched.
>
> A single control process (the parent) is responsible for launching child processes. Each child process creates a fixed number of server threads as specified in the ThreadsPerChild directive, as well as a listener thread which listens for connections and passes them to a server thread for processing when they arrive.
>
> The maximum number of clients that may be served simultaneously (i.e., the maximum total number of threads in all processes) is determined by the MaxClients directive. The maximum number of active child processes is determined by the MaxClients directive divided by the ThreadsPerChild directive.
>
> ServerLimit is a hard limit on the number of active child processes, and must be greater than or equal to the MaxClients directive divided by the ThreadsPerChild directive.

From the last statement we can use this equation **ServerLimit** = **MaxClients** \ **ThreadsPerChild**. So basically **ServerLimit** defines how many apache processes will be launched. Then you decide how many simultaneous connections you can handle, this is your **MaxClients** value. Then divide **MaxClient** by **ServerLimit** and that is how many threads will be necessary to handle your desired simultaneous connections per server/apache process (There is also an excel sheet provided from the [linode forums](http://forum.linode.com/viewtopic.php?t=7622) which has the equation setup). So following that equation, I came up with this:

    ServerLimit            4
    StartServers           2
    MinSpareThreads        5
    MaxSpareThreads        10
    ThreadsPerChild        20
    MaxClients             80
    MaxRequestsPerChild    1000


and ran the following test:

> -p 1-150:60 mysite.com

My results were the following:

> 1,643 HITS WITH 0 ERRORS & 918 TIMEOUTS

This test was very theoretical, so if you wanted to handle 80 clients simultaneously and you wanted to limit your processes to be 4 then you would need 20 threads per process/server. When I ran this, my **load avg** spiked up to 9 :(. You will need more CPUs to handle that kind of load. So I ran a bunch of tests and here were my optimal settings:

    StartServers           2
    MinSpareThreads        1
    MaxSpareThreads        2
    ThreadsPerChild        10
    MaxRequestsPerChild    1000
    MaxClients             20
    ServerLimit            4


with the following test:

> -p 1-100:60 mysite.com
> **Results:**
> 1,980 HITS WITH 0 ERRORS & 24 TIMEOUTS

Just for testing, I ran the following test with same configuration and I got the following:

> -p 1-150:60
> **Results:**
> 1,985 HITS WITH 0 ERRORS & 536 TIMEOUTS

Throughout my testing, I saw *apache* use 60MB per process, but that was an extreme case. With my optimal configuration, I was using the same amount as the prefork MPM processes about 24MB per *apache* process. So with apache **worker** MPM and **mod_php** we can handle 2,000 hits when receiving 100 simultaneous requests. This is way better than **prefork**. As I was doing my testing, I ran into the following from the [PHP FAQ](http://www.php.net/manual/en/faq.installation.php#faq.installation.apache2):

> PHP is glue. It is the glue used to build cool web applications by sticking dozens of 3rd-party libraries together and making it all appear as one coherent entity through an intuitive and easy to learn language interface. The flexibility and power of PHP relies on the stability and robustness of the underlying platform. It needs a working OS, a working web server and working 3rd-party libraries to glue together. When any of these stop working PHP needs ways to identify the problems and fix them quickly. When you make the underlying framework more complex by not having completely separate execution threads, completely separate memory segments and a strong sandbox for each request to play in, further weaknesses are introduced into PHP's system.
>
> If you want to use a threaded MPM, look at a FastCGI configuration where PHP is running in its own memory space.

So I decided to test apache with **fastcgi** and **php-fpm**. Every setup I checked out:

*   [Multithreaded Apache In Small VPS](http://itkia.com/multithreaded-apache-in-small-vps/)
*   [Improve Php And Apache2 Performance With Apache2-Mpm-Worker + Mod_fcgid + Php5-Cgi](http://phphints.wordpress.com/2009/01/10/improving-php-performance-with-apache2-mpm-worker-mod_fcgid-2/)
*   [PHP-FPM FastCGI Process Manager with Apache 2](https://blogs.oracle.com/opal/entry/php_fpm_fastcgi_process_manager)
*   [FreeBSD Configure Apache 2.2 PHP with FastCGI mod_fcgi Module](http://www.cyberciti.biz/faq/freebsd-apache22-fastcgi-php-configuration/)
*   [Moving from mod_fastcgi to mod_fcgid](http://personal.x-istence.com/post/2009/08/25/moving-modfastcgi-modfcgid)

They all use a wrapper script to call PHP. I really don't like doing that, it's a security flaw. Like I mentioned, I like Apache cause it's secure. However when you add modules to Apache that make it less secure, then I definitely lose the desire to use Apache. After tinkering around with the setup, I ended up doing this:

    FastCGIExternalServer /usr/local/bin/php-fpm -host 127.0.0.1:9000
    AddHandler php-fastcgi .php

    Action php-fastcgi /usr/local/bin/php-fpm.fcgi
    ScriptAlias /usr/local/bin/php-fpm.fcgi /usr/local/bin/php-fpm

      Options ExecCGI FollowSymLinks
      SetHandler fastcgi-script
      Order allow,deny
      Allow from all


I had to allow the **/usr/local/bin** directory to allow CGI Execution from Apache, since that is where the **php-fpm** binary resided. Maybe I was doing it wrong, but I couldn't get it working any other way. For some reason, I didn't like that. There is a actually an excellent article on securing all of this: "[Apache httpd + suEXEC + chroot + FastCGI + PHP](http://e.metaclarity.org/268/httpdsuexecchrootfastcgiphp/)". But remember, I like simplicity :). Let me re-phrase that: I don't mind complex setups, as long as there is a pay off.

So I set up Apache with **mod_fastcgi** and forwarded that to **php-fpm**. The only thing I changed for **php-fpm** was the following:

    $ grep ^pm php-fpm.conf
    pm = dynamic
    pm.max_children = 4
    pm.start_servers = 2
    pm.min_spare_servers = 1
    pm.max_spare_servers = 3


I ran the following test:

> -p 1-150:60 mysite.com
> **Results:**
> 1,483 HITS WITH 0 ERRORS & 1,060 TIMEOUTS

I then re-enabled **worker** MPM, so now I had Apache MPM **worker** with **mod_fastcgi** going to **php-fpm**, and got the following:

> -p 1-150:60 mysite.com
> **Results:**
> 2,182 HITS WITH 0 ERRORS & 596 TIMEOUTS

I really didn't see that much of an increase. Now there are other *fast-cgi* modules. The blog "[Installing Apache + Mod_FastCGI + PHP-FPM on Ubuntu Server Maverick](http://alexcabal.com/installing-apache-mod_fastcgi-php-fpm-on-ubuntu-server-maverick/)" clarifies that different versions, from the blog:

> **Apache + mod_fastcgi**: FastCGI is a module that allows you to neatly solve mod_php’s big problem, namely that it must spin up and destroy a PHP instance with every request. FastCGI instead keeps an instance of PHP running in the background. When Apache receives a request it forwards it to FastCGI, which feeds it to its already running instance of PHP and sends the result back to Apache. Apache then serves the result.
> Without the constant build-and-destroy of new PHP processes, FastCGI is a great memory saver and performance booster. My Apache + mod_php install, which would constantly bloat to 1000′s of MB in memory usage and invoke OOM-Killer without mercy, has been humming along at a steady ~200MB for the past few months without a single problem after switching to mod_fastcgi.
>
> **Apache + mod_fcgid**: Why, oh why, did someone build an alternative to FastCGI only to call it by the almost-identical name of fcgid? From what I understand, fgcid is a binary-compatible alternative to FastCGI–that is, it does more or less the same thing, but in a different way. It seems that some people prefer mod_fcgid over mod_fastcgi because of better stability and maybe even slightly better performance. But for the kind of traffic I’m getting, there wasn’t any difference.
>
> **Apache + mod_fastcgi + PHP-FPM**: PHP-FPM (A.K.A. PHP5-FPM) is a process manager for PHP. Confusingly, it was only recently bundled with PHP, so you might find some tutorials telling you to download the source and others to just use apt-get. I believe that if you’re using PHP >= 5.3, which you would be if you installed it in Maverick with apt-get, that you don’t need to download the source to get it working. I’ll talk more about this later.
> From what I understand, PHP-FPM is like FastCGI, but with additional PHP-specific optimizations built in. Since it’s specially built for PHP, it should give you the best performance, and so is the best of these three alternatives

There is actually another person that ran some tests with the different modules. Check out "[Benchmark: mod_php -vs- mod_fcgid for WordPress](http://mykospark.net/2010/03/benchmark-mod_php-vs-mod_fcgid-for-wordpress/)", his summary:

> It seems that if you are running heavyweight code like WordPress, it doesn't make much difference which mode you use. If your code is lightweight though, mod_php is capable of cranking out a significant number of requests. I personally prefer worker mode as it will be a little lighter on the resources, and can probably serve static files faster. Also, Apache can take advantage of resource sharing when running in worker mode.

From the two tests that I ran, I would have to agree. The module performance between **mod_fastcgi** and **mod_php** is very small, especially when using them with **worker** MPM. Maybe if you had a lot of RAM it might make a difference, but in our case, we don't have that luxury.

Lastly I tested with **nginx** with **php-fpm**. At first I left the defaults:

    $ grep ^pm php-fpm.conf
    pm = dynamic
    pm.max_children = 5
    pm.start_servers = 2
    pm.min_spare_servers = 1
    pm.max_spare_servers = 3


I saw the following:

> -p 1-100:60 mysite.com
> **Results:**
> 1,766 HITS WITH 0 ERRORS & 442 TIMEOUTS

I tweaked different things, and the only parameter that was worth changing was the **pm.max_children** setting. I changed it to 4 and I got the following:

> -p 1-100:60 mysite.com
> **Results:**
> 1,667 HITS WITH 0 ERRORS & 491 TIMEOUTS

The results were very close, and I saved 24MB of memory, it was worth it. This saved a bunch of memory, **nginx** is way smaller and liked mentioned in the above pages it's *event-driven* and not process driven like *Apache*. In my opinion if are using a VPS with less than a 1GB of RAM then definitely go for **nginx**, if you have more than that, then go with *Apache*. Even though your *Apache* process will take up more RAM, the performance gain with MPM **worker** will be worth it . Now if you still want to increase how many hits your site can handle, you can setup caching:

*   [Install Nginx With APC, Varnish, WordPress And W3 Cache On A 128MB VPS](http://axelsegebrecht.com/how-to/install-nginx-apc-varnish-wordpress-and-w3-cache-128mb-vps/)
*   [10 Million hits a day with WordPress using a $15 server](http://www.ewanleith.com/blog/900/10-million-hits-a-day-with-wordpress-using-a-15-server)
*   [How a little varnish changed my life](http://ariejan.net/2010/03/24/how-a-little-varnish-changed-my-life/)

