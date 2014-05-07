---
title: CloudFront with ELB and Apache VirtualHosts
author: Joe Chan
layout: post
permalink: /2012/11/cloudfront-with-elb-and-apache-virtualhosts/
dsq_thread_id:
  - 1404673679
categories:
  - AWS
tags:
  - apache
  - aws
  - cloudfront
  - ec2
  - elb
  - httpd
  - vhosts
  - virtualhosts
  - web
  - webserver
---
I was recently trying to set up multiple websites `joesite.joechan.us` and `evesite.joechan.us` with Apache VirtualHosts on a single EC2 instance behind an Elastic Load Balancer (ELB), but I also wanted that content to be cached by CloudFront similar to this diagram below.

![cloudfront&#95;dynamic&#95;web&#95;sites&#95;full 1 CloudFront with ELB and Apache VirtualHosts][1]

In setting this up, I ran into an issue where the VirtualHosts weren&#8217;t working as expected. I would always get sent to the same site, regardless of which subdomain I was pointing to. Going to evesite.joechan.us kept pointing me to the contents of joesite.joechan.us.

## My old configuration

In my old configuration, I had 2 subdomains, pointing to 2 CF distributions, with each CF distribution pointing to a single ELB.

*   Old DNS records
    
        joesite.joechan.us. 300 IN CNAME d1byny1djxkk2x.cloudfront.net.
        evesite.joechan.us. 300 IN CNAME d2ey6g4539mma3.cloudfront.net.
        

*   Old CF Distribution settings
    
        Distribution Domain Name: d1byny1djxkk2x.cloudfront.net
        Alternate Domain Names(CNAMEs): joesite.joechan.us
        Origin Domain Name:  elb-1603695720.us-west-2.elb.amazonaws.com (ELB)
        Distribution Domain Name: d2ey6g4539mma3.cloudfront.net
        Alternate Domain Names(CNAMEs): evesite.joechan.us
        Origin Domain Name:  elb-1603695720.us-west-2.elb.amazonaws.com (ELB)
        

*   Old Apache vHosts configuration
    
        <VirtualHost *:80>
        DocumentRoot /var/www/html/joesite
        ServerName joesite.joechan.us
        ErrorLog logs/test.joechan.us-error_log
        CustomLog logs/test.joechan.us-access_log common
        </VirtualHost>
        
        <VirtualHost *:80>
        DocumentRoot /var/www/html/evesite
        ServerName evesite.joechan.us
        ErrorLog logs/test.joechan.us-error_log
        CustomLog logs/test.joechan.us-access_log common
        </VirtualHost>
        

# Solution

It turns out that CloudFront will pass what is configured in the &#8216;Origin Domain Name&#8217; field of the CloudFront settings (in my case, the ELB hostname) as the HTTP Host header to ELB, which will then get forwarded to Apache and Apache doesn&#8217;t have a VirtualHost set up for my ELB hostname (elb-1603695720.us-west-2.elb.amazonaws.com).

Here is the fix:

*   Create 2 new CNAME records (one for each site), and use those as the CloudFront Origin Domain Names. 
*   Modify VirtualHost configuration to expect the proper CloudFront Origin Domain Names in the HTTP Host header. 

## My end configuration

In my new configuration, I have each original subdomain pointing to a CF distribution, which points to a new &#8220;vHosts&#8221; subdomain (like joestuff.joechan.us), which points to my single ELB. The ELB will forward the HTTP host header from the Origin Domain Name (<joe|eve>stuff.joechan.us), which is what I configure Apache to look for.

*   New DNS records
    
        joesite.joechan.us. 300 IN CNAME d1byny1djxkk2x.cloudfront.net.
        evesite.joechan.us. 300 IN CNAME d2ey6g4539mma3.cloudfront.net.
        joestuff.joechan.us. 300 IN CNAME elb-1603695720.us-west-2.elb.amazonaws.com.
        evestuff.joechan.us. 300 IN CNAME elb-1603695720.us-west-2.elb.amazonaws.com.
        New CF Distribution settings
        

*   New CF Distribution settings
    
        d1byny1djxkk2x.cloudfront.net
        Alternate Domain Names(CNAMEs): joesite.joechan.us
        Origin Domain Name:  joestuff.joechan.us
        d2ey6g4539mma3.cloudfront.net
        Alternate Domain Names(CNAMEs): evesite.joechan.us
        Origin Domain Name:  evestuff.joechan.us
        

*   New Apache vHosts configuration
    
        <VirtualHost *:80>
        DocumentRoot /var/www/html/joesite
        ServerName joestuff.joechan.us
        ErrorLog logs/test.joechan.us-error_log
        CustomLog logs/test.joechan.us-access_log common
        </VirtualHost>
        
        <VirtualHost *:80>
        DocumentRoot /var/www/html/evesite
        ServerName evestuff.joechan.us
        ErrorLog logs/test.joechan.us-error_log
        CustomLog logs/test.joechan.us-access_log common
        </VirtualHost>
        

I hope that this helps some of you out there trying to configure CloudFront with ELB and Apache VirtualHosts. If you guys have any thoughts or questions, please feel free to leave a comment!

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 14 – Web Services" href="http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-14-web-services/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-14-web-services/']);" rel="bookmark">RHCSA and RHCE Chapter 14 – Web Services</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="How to Make an Anonymous Amazon S3 REST Request" href="http://virtuallyhyper.com/2013/09/make-anonymous-amazon-s3-rest-request/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/09/make-anonymous-amazon-s3-rest-request/']);" rel="bookmark">How to Make an Anonymous Amazon S3 REST Request</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="CORS with CloudFront, S3, and Multiple Domains" href="http://virtuallyhyper.com/2013/08/cors-with-cloudfront-s3-and-multiple-domains/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/08/cors-with-cloudfront-s3-and-multiple-domains/']);" rel="bookmark">CORS with CloudFront, S3, and Multiple Domains</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Deploy an Amazon EC2 instance in the Free Usage Tier" href="http://virtuallyhyper.com/2013/04/deploy-an-amazon-ec2-instance-in-the-free-usage-tier/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploy-an-amazon-ec2-instance-in-the-free-usage-tier/']);" rel="bookmark">Deploy an Amazon EC2 instance in the Free Usage Tier</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Astaro Security Gateway Routing" href="http://virtuallyhyper.com/2013/04/astaro-security-gateway-routing/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/astaro-security-gateway-routing/']);" rel="bookmark">Astaro Security Gateway Routing</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/11/cloudfront-with-elb-and-apache-virtualhosts/" title=" CloudFront with ELB and Apache VirtualHosts" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:apache,aws,cloudfront,ec2,elb,httpd,vhosts,virtualhosts,web,webserver,blog;button:compact;">I had an issue where bringing up an Sophos Astaro Security Gateway (ASG) site-to-site VPN connection between VPC&#8217;s caused another connectivity across another VPN connection to fail. Looking into the...</a>
</p>

 [1]: http://media.amazonwebservices.com/blog/cloudfront&#95;dynamic&#95;web&#95;sites&#95;full_1.jpg "CloudFront with ELB and Apache VirtualHosts"