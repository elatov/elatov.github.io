---
title: VCAP5-DCD Objective 2.2 – Map Service Dependencies
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-2-map-service-dependencies/
dsq_thread_id:
  - 1407186121
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Identify basic service dependencies for infrastructure and application services

This should be done during the Current-State Analysis process. If you want to automate this process you can use an application called VMware vCenter Application Discovery Manager. More information regarding the product can be found in link that is provided in the blue print.

*   <a href="http://www.vmware.com/files/pdf/vmware-vcenter-app-discovery-mgr-datacenter-ops-WP-EN.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/vmware-vcenter-app-discovery-mgr-datacenter-ops-WP-EN.pdf']);">Datacenter Operational Excellence Through Automated Application Discovery & Dependency Mapping</a>

From that PDF:

> Effective application discovery and dependency mapping requires three primary methods:
> 
> *   **Active discovery** - This method uses common network protocols to remotely query servers in the managed network and obtain supplementary CI data about network hosts. However, using just active discovery can place an unnecessary burden on the network. In addition, large segments of CI data don’t change all that often, making repeated realtime active discovery unnecessary for many. Furthermore, although active discovery uncovers detailed CI data about hosts and services, it doesn’t easily or directly provide information about how they relate to others. But active discovery doesn’t require agents, and delivers a wealth of solid CI data.
> *   **Passive discovery** &#8211; This method provides more of that relationship data. By connecting to core span or mirror ports on network switches and sampling network traffic, passive discovery can identify network hosts and servers, their communications and connections, and what services and protocols are being exchanged at what time. Although another rich source of data, you need some additional capabilities to assemble this raw data into actionable information.
> *   **Discovery analytics** - This third element complements the first two with the ability to perform deep-packet analysis of observed traffic, and to help establish the relationships between passively and actively discovered entities. Analytics with rich data provides little benefit; the same holds true for active and passive discovery.
> 
> Together, active discovery, passive discovery, and discovery analytics deliver a hybrid approach to application discovery and dependency mapping—provides the most complete approach

### Document service relationships and dependencies (Entity Relationship Diagrams)

From <a href="http://www.virten.net/2012/06/vdcd510-objective-2-2-map-service-dependencies/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/06/vdcd510-objective-2-2-map-service-dependencies/']);">this</a> blog:

> **Application Dependency Diagram**  
> An application dependency diagram determines which entities are related with another. While discovering running services during the current state analysis you can use this information to draw down the upstream and downstream relationships. Relationships could be defined in the following terms:
> 
> *   runs on / runs
> *   depends on / used by
> *   contains / contained by
> *   hosts / hosted by

### Identify interfaces to existing business processes and define new business processes

This depends on what you find. Let&#8217;s say for example you found an application that was abusing the production DB server so you virtualize this application and make it have a dedicated DB service. This way you don&#8217;t impact anything else. Now if you make that change you need to notify everyone and make sure everyone knows that if the application goes down, there is no need to restart the production DB server but just the VM it self.

### Given a scenario, identify logical components that have dependencies on certain services

Again from <a href="http://www.virten.net/2012/06/vdcd510-objective-2-2-map-service-dependencies/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/06/vdcd510-objective-2-2-map-service-dependencies/']);">this</a> blog:

> If you have a website for example. The website runs on a webserver which runs on a linux server which is hosted by a VMware Cluster. This is an example of the dependency map: 

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/application-dependency.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/application-dependency.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/08/application-dependency.png" alt="application dependency VCAP5 DCD Objective 2.2 – Map Service Dependencies " title="application-dependency" width="556" height="67" class="alignnone size-full wp-image-2745" /></a>

### Include service dependencies in a vSphere 5 logical design

If you find any service/server dependency include them into the logical design without including too much information, like IP address and the sorts.

### Analyze services to identify upstream and downstream service dependencies

From this blog:

> **Upstream and Downstream Relationships**  
> Everything that happens downstream can have an effect on upstream items. For example, if the webserver crashes, the website upstream is affected and goes down. Neither the operating system, nor the cluster are affected, as this are downstream relationships. To memorize this, you could think of a house. The roof is “up” while basement is “down”. If you break down the basement, the roof upstream” also collapses. 

### Having navigated logical components and their interdependencies, make decisions based upon all service relationships.

Create vApps if necessary to put Web,DB, and Application servers together. You can set the boot order of all the VMs (i.e start DB server first). This way you can ensure proper dependency takes place.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/vcap5-dcd-objective-2-2-map-service-dependencies/" title=" VCAP5-DCD Objective 2.2 – Map Service Dependencies" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCD,blog;button:compact;">Identify basic service dependencies for infrastructure and application services This should be done during the Current-State Analysis process. If you want to automate this process you can use an application...</a>
</p>