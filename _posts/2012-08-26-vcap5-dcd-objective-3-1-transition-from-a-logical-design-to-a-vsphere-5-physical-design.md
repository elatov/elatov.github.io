---
title: VCAP5-DCD Objective 3.1 – Transition from a Logical Design to a vSphere 5 Physical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-3-1-transition-from-a-logical-design-to-a-vsphere-5-physical-design/
dsq_thread_id:
  - 1406227705
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Determine and explain design decisions and options selected from the logical design

From <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">this</a> PDF:

> **Physical Design**
> 
> *   Uses the Logical Design 
> *   Uses Specific Hardware detains and implementation information 
> *   Includes port assignments, pci slots, etc&#8230; 

Here is an example of a physical diagram, taken from &#8220;<a href="http://www.vmware.com/files/pdf/VMware-vCloud-Implementation-Example-ServiceProvider.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/VMware-vCloud-Implementation-Example-ServiceProvider.pdf']);">VMware vCloud Implementation Example</a>&#8220;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/physical-design-diag.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/physical-design-diag.png']);"><img class="alignnone size-full wp-image-2861" title="physical-design-diag" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/physical-design-diag.png" alt="physical design diag VCAP5 DCD Objective 3.1 – Transition from a Logical Design to a vSphere 5 Physical Design" width="565" height="338" /></a>

### Build functional requirements into the physical design

Let&#8217;s say we had a need for a DMZ, if this was the case, then we would either get a separate switch to be extra secure, or dedicate a new VLAN for our DMZ traffic. We would then allocate a port on the physical switch for our DMZ traffic. Either or, we have to show which port is allowing DMZ traffic.

### Given a logical design, create a physical design taking into account requirements, assumptions and constraints

Let&#8217;s say we looked at some of the previous logical diagrams:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png']);"><img class="alignnone size-full wp-image-2702" title="logical-diagram" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png" alt="logical diagram VCAP5 DCD Objective 3.1 – Transition from a Logical Design to a vSphere 5 Physical Design" width="948" height="496" /></a>

Now our physical diagram would include:

*   All the IPs of the hosts
*   Hardware Models of the host , Arrays, and switches/routers
*   What type of link is between the Arrays
*   What type of devices (switches, routers) are between the hosts and sites
*   What ports we are connected on the switch, fiber or ethernet

### Given the operational structure of an organization, identify the appropriate management tools and roles for each staff member

From the <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf']);">vSphere Security Guide</a>, here is a list of predefined roles:

> *   No Access
> *   Read Only
> *   Administrator
> *   Virtual Machine Power User
> *   Virtual Machine User
> *   Resource Pool Administrator
> *   Datastore Consumer
> *   Network Consumer 

The default should be enough for most cases. It depends on how many people are actually going to be working on the virtualized environment and what policies have been set in place. For example if there is a change control in place for deploying a VM, then have a dedicated &#8220;Virtual Machine Power User&#8221; role defined to have the ability to create VMs. Also have a bunch of users be in the &#8220;Virtual Machine Users&#8221; role and they will be only allowed to use the VMs. With both of these in place, you can ensure that one person keeps track of changes ( what VMs are deployed ) and regular users in the &#8220;Virtual Machine Users&#8221; won&#8217;t be able to make any changes, but can still use the VMs that are already deployed.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCAP5-DCD Objective 4.3 – Create an Installation Guide" href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-3-create-an-installation-guide/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-3-create-an-installation-guide/']);" rel="bookmark">VCAP5-DCD Objective 4.3 – Create an Installation Guide</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCAP5-DCD Objective 4.2 – Create an Implementation Plan" href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-2-create-an-implementation-plan/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-2-create-an-implementation-plan/']);" rel="bookmark">VCAP5-DCD Objective 4.2 – Create an Implementation Plan</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCAP5-DCD Objective 4.1 – Create an Execute a Validation Plan" href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-1-create-an-execute-a-validation-plan/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-4-1-create-an-execute-a-validation-plan/']);" rel="bookmark">VCAP5-DCD Objective 4.1 – Create an Execute a Validation Plan</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCAP5-DCD Objective 3.6 – Determine Datacenter Management Options for a vSphere 5 Physical Design" href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/']);" rel="bookmark">VCAP5-DCD Objective 3.6 – Determine Datacenter Management Options for a vSphere 5 Physical Design</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VCAP5-DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design" href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/']);" rel="bookmark">VCAP5-DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/vcap5-dcd-objective-3-1-transition-from-a-logical-design-to-a-vsphere-5-physical-design/" title=" VCAP5-DCD Objective 3.1 – Transition from a Logical Design to a vSphere 5 Physical Design" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCD,blog;button:compact;">Describe best practices with respect to CPU family choices From &#8220;Performance Best Practices for VMware vSphere 5.0&#8220;: Hardware CPU Considerations General CPU Considerations When selecting hardware, it is a good...</a>
</p>