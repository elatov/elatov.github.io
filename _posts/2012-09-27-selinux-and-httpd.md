---
title: 'WordPress &#8211; Error establishing a database connection, but able to connect via command line &#8211; SELinux and httpd'
author: Joe Chan
layout: post
permalink: /2012/09/selinux-and-httpd/
dsq_thread_id:
  - 1412256518
categories:
  - OS
tags:
  - drupal
  - httpd
  - linux
  - selinux
  - wordpress
---
I was installing Drupal and WordPress the other day and during the initial setup I came across the following messages:

[code highlight="3"]In order for Drupal to work, and to continue with the installation process, you must resolve all issues reported below. For more help with configuring your database server, see the installation handbook. If you are unsure what any of this means you should probably contact your hosting provider.

Failed to connect to your database server. The server reports the following message: SQLSTATE\[HY000\] \[2003\] Can't connect to MySQL server on 'testdb.joechan.us' (13).

Is the database server running?  
Does the database exist, and have you entered the correct database name?  
Have you entered the correct username and password?  
Have you entered the correct database hostname?  
[/code]

You will see something similar in WordPress:  
[code]  
Error establishing a database connection  
This either means that the username and password information in your wp-config.php file is incorrect or we can't contact the database server at testdb.joechan.us. This could mean your host's database server is down.

Are you sure you have the correct username and password?  
Are you sure that you have typed the correct hostname?  
Are you sure that the database server is running?  
If you're unsure what these terms mean you should probably contact your host. If you still need help you can always visit the WordPress Support Forums.  
[/code]

So I try logging into the MySQL server directly:

[code]  
798ip-10-252-128-9$ mysql -u root -h testdb.joechan.us -p  
Enter password:  
Welcome to the MySQL monitor. Commands end with ; or \g.  
Your MySQL connection id is 62  
Server version: 5.5.27-log Source distribution

Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its  
affiliates. Other names may be trademarks of their respective  
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>  
[/code]

Strange&#8230; it succeeds.

A bit of Googling led me to this <a href="http://stackoverflow.com/questions/4078205/php-cant-connect-to-mysql-with-error-13-but-command-line-can" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://stackoverflow.com/questions/4078205/php-cant-connect-to-mysql-with-error-13-but-command-line-can']);">StackOverflow page</a>.

It turns out there is a special SELinux boolean that specifically blocks Apache (httpd) from talking to databases (more info about the different SELinux booleans <a href="http://wiki.centos.org/TipsAndTricks/SelinuxBooleans" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.centos.org/TipsAndTricks/SelinuxBooleans']);">here</a>):

<pre>httpd_can_network_connect_db (HTTPD Service)
Allow HTTPD scripts and modules to network connect to databases.
</pre>

So I just disabled SELinux per the instructions <a href="http://www.centos.org/docs/5/html/5.2/Deployment_Guide/sec-sel-enable-disable.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.centos.org/docs/5/html/5.2/Deployment_Guide/sec-sel-enable-disable.html']);">here</a>.

To enable temporarily until you reboot, run the following as root:  
[code]  
\# echo 0 >/selinux/enforce  
[/code]

If you want to leave SELinux on, but allow an exception for httpd to talk to your database, you can run the following:  
[code]  
setsebool -P httpd\_can\_network\_connect\_db on  
[/code]

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="CloudFront with ELB and Apache VirtualHosts" href="http://virtuallyhyper.com/2012/11/cloudfront-with-elb-and-apache-virtualhosts/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/cloudfront-with-elb-and-apache-virtualhosts/']);" rel="bookmark">CloudFront with ELB and Apache VirtualHosts</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/selinux-and-httpd/" title=" WordPress &#8211; Error establishing a database connection, but able to connect via command line &#8211; SELinux and httpd" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:drupal,httpd,linux,selinux,wordpress,blog;button:compact;">I was recently trying to set up multiple websites joesite.joechan.us and evesite.joechan.us with Apache VirtualHosts on a single EC2 instance behind an Elastic Load Balancer (ELB), but I also wanted...</a>
</p>