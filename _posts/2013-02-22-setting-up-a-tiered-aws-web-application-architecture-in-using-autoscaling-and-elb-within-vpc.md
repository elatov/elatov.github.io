---
title: Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC
author: Joe Chan
layout: post
permalink: /2013/02/setting-up-a-tiered-aws-web-application-architecture-in-using-autoscaling-and-elb-within-vpc/
dsq_thread_id:
  - 1407839982
categories:
  - AWS
tags:
  - aws
  - Elastic Load Balancing
  - Virtual Private Cloud
---
## Sample AWS Web Application Architecture using AutoScaling and ELB within VPC

The purpose of this guide is to help you set up some of the AWS Web Application Architecture using AutoScaling and ELB within VPC.

This build comes from <a href="http://media.amazonwebservices.com/architecturecenter/AWS_ac_ra_web_01.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://media.amazonwebservices.com/architecturecenter/AWS_ac_ra_web_01.pdf']);">this AWS architecture document</a> (except I am only deploying in a single Availability Zone (AZ), but modifying this to support multiple AZ&#8217;s isn&#8217;t too much more difficult and I&#8217;ll provide the parameters that need changing at the end). I&#8217;m only setting up 2 tiers in this example, but you can use the same concepts and commands to easily add a third tier and/or additional redundancy (ie: AZ&#8217;s) as you require.

At the same time, this guide will also show you how to deploy the right-side of the following image (Availability Zone 1B) taken from <a href="http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/UserScenariosForVPC.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/UserScenariosForVPC.html']);">Deploying Elastic Load Balancing in Amazon VPC</a>:

![ELB VPCArchFigure Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC][1]

You can use the similar concepts and commands to create an environment on the left (Availability Zone 1A) if you would like.

# What we&#8217;ll be setting up

*   Everything will reside in the VPC.
*   An Internet-facing ELB will load balance web requests across your Web tier.
*   An internal load balancer will load balance the Web tier across the DB tier.
*   Backend Web and DB instances are hidden from the Internet and reside in a private subnet.
*   AutoScaling will help the Web and DB tiers remain elastic and scale based on load
*   Elastic Load Balancing will load balance requests

# Resources required

*   Public `subnet-65c6780c`, `10.0.0.0/24`, `us-east-1a`
*   Private subnet `subnet-66c6780f`, `10.0.1.0/24`, `us-east-1b`
*   Public ELB SG `sg-06031c6a`
*   Private ELB SG `sg-da031cb6`
*   Web SG `sg-0b031c67`
*   Database SG `sg-05031c69`

For AMIs, I am using the <a href="http://bitnami.org/stack/lamp#cloudImage" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bitnami.org/stack/lamp#cloudImage']);">Bitnami LAMP images</a> (they&#8217;re pretty awesome if you want to get up and running quickly with a LAMP stack and are new to or don&#8217;t want to set up LAMP yourself!):

*   Web Server AMI: `ami-1821ab28`
*   Database AMI: `ami-1821ab28`

# Just give me the commands already!

## Web Tier

Create ELB in public subnet in between web clients and the **Web** tier:

    $ elb-create-lb publicvpcelb  --scheme "internet-facing" --security-groups sg-06031c6a --listener "lb-port=80, instance-port=80, protocol=http, instance-protocol=http" --subnets subnet-65c6780c`
    DNS_NAME  publicvpcelb-705800467.us-west-2.elb.amazonaws.com
    

Create launch configuration for **Web** tier:

    $ as-create-launch-config testweblc --image-id ami-1821ab28 --instance-type t1.micro --key chanjoe --group sg-0b031c67
    OK-Created launch config
    

Create AutoScaling group for **Web** tier:

    $ as-create-auto-scaling-group testwebasg --launch-configuration testweblc --availability-zones "us-west-2a" --min-size 0 --max-size 1 --desired-capacity 1 --vpc-zone-identifier "subnet-66c6780f" --load-balancers privatevpcelb
    

## DB Tier

Create ELB in private subnet between **Web** tier and **DB** tier:

    $ elb-create-lb privatevpcelb  --scheme "internal" --security-groups sg-da031cb6 --listener "lb-port=3306, instance-port=3306, protocol=tcp, instance-protocol=tcp" --subnets subnet-66c6780f
    DNS_NAME  internal-privatevpcelb-65013364.us-west-2.elb.amazonaws.com
    

Create launch configuration for **DB** tier:

    $ as-create-launch-config testdblc --image-id ami-1821ab28 --instance-type t1.micro --key chanjoe --group sg-05031c69
    OK-Created launch config
    

Create AutoScaling group for **DB** tier:

    $ as-create-auto-scaling-group testdbasg --launch-configuration testdblc --availability-zones "us-west-2a" --min-size 0 --max-size 1 --desired-capacity 1 --vpc-zone-identifier "subnet-66c6780f" --load-balancers privatevpcelb
    

# A Common Issue

I get an error when browsing to my ELB:

    HTTP Error 503 (Service Unavailable): The server is currently unable to handle the request. This code indicates this is a temporary condition, and the server will be up again after a delay.
    

or this `HTTP/1.1 503 Service Unavailable: Back-end server is at capacity` via ***curl**:

    $ curl -v publicvpcelb-705800467.us-west-2.elb.amazonaws.com
    * About to connect() to publicvpcelb-705800467.us-west-2.elb.amazonaws.com port 80 (#0)
    *   Trying 50.112.174.229...
    * connected
    * Connected to publicvpcelb-705800467.us-west-2.elb.amazonaws.com (50.112.174.229) port 80 (#0)
    > GET / HTTP/1.1
    > User-Agent: curl/7.24.0 (x86_64-redhat-linux-gnu) libcurl/7.24.0 NSS/3.13.5.0 zlib/1.2.5 libidn/1.18 libssh2/1.2.2
    > Host: publicvpcelb-705800467.us-west-2.elb.amazonaws.com
    > Accept: */*
    >
    < HTTP/1.1 503 Service Unavailable: Back-end server is at capacity
    < Content-Length: 0
    < Connection: keep-alive
    <
    * Connection #0 to host publicvpcelb-705800467.us-west-2.elb.amazonaws.com left intact
    * Closing connection #0
    

*   Check your healthy host counts for the ELB. HTTP 5XX errors can mean that you have no healthy backend instances to serve the request.
*   Remember to open up the security groups to allow traffic from the Internet to the Internet-facing-ELB, from your ELB to the Web tier, from the Web tier to the internal-ELB.
*   For troubleshooting connectivity inside your private subnet, launch an instance into your public subnet that you can reach and confirm you can reach the private instances and ELB.

# Adding additional Availability Zones

*   As I mentioned at the beginning, I did not deploy additional instances in other availability zones. You can do this if you wish by creating additional subnets (1 for each AZ you&#8217;d like to instances in) and adding them to the `--availability-zones` parameter in the `elb-create-lb` and `as-create-auto-scaling-group` commands.

This is certainly not an all-inclusive guide and none of it is new information, but I hope it helps people from having to piece it together from the documentation below! Please let me know if you have any comments or suggestions. <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC" class="wp-smiley" title="Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC" /> 

# Some helpful references

*   <a href="http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/autoscalingsubnets.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/autoscalingsubnets.html']);">Launch Auto Scaling Instances into Amazon VPC</a>
*   <a href="http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/UserScenariosForVPC.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/UserScenariosForVPC.html']);">Deploying Elastic Load Balancing in Amazon VPC</a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/02/setting-up-a-tiered-aws-web-application-architecture-in-using-autoscaling-and-elb-within-vpc/" title=" Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:aws,Elastic Load Balancing,Virtual Private Cloud,blog;button:compact;">Sample AWS Web Application Architecture using AutoScaling and ELB within VPC The purpose of this guide is to help you set up some of the AWS Web Application Architecture using...</a>
</p>

 [1]: http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/images/ELB-VPCArchFigure.png "Setting Up a Tiered AWS Web Application Architecture in using AutoScaling and ELB within VPC"