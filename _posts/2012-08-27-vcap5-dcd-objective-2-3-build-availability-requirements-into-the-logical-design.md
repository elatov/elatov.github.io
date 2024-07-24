---
title: VCAP5-DCD Objective 2.3 – Build Availability Requirements into the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-3-build-availability-requirements-into-the-logical-design/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['fault_tolerance', 'vmotion','logical_design']
---

### Understand what logical availability services are provided by VMware solutions

From [this](http://www.virten.net/2012/06/vdcd510-objective-2-3-build-availability-requirements-into-the-logical-design/) blog:

> **VMware Availability Services**
> **vSphere High Availability (HA)** minimizes your downtime by restarting virtual machines on remaining hosts in case of hardware failures.
>
> **vSphere Fault Tolerance (FT)**
> provides continuous availability for virtual machines by creating a live copy of a virtual machine to another physical host.

From the [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/) slide deck:

![availability_features](https://github.com/elatov/uploads/raw/master/2012/08/availability_features.png)

### Identify and differentiate infrastructure qualities (Availability, Manageability, Performance, Recoverability, Security)

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> **Design Criteria**
>
> 1.  Usability
>     1.  Performance - maybe measured by throughput, latency, transaction...etc
>     2.  Availability - defined as access to resources when needed
>         *   Achieved using redundancy
>         *   Defined in SLA
>     3.  Scalability - support future growth while maintaining acceptable performance
> 2.  Manageability
>     *   Easy to deploy
>     *   Easy to administer and maintain
>     *   Easy to update and upgrade
>     *   Simplification is law
>     *   unnecessary complexities can lead to failture, rises in cost... etc
> 3.  Security
>     *   Minimizes risks
>     *   is easy to secure
>     *   good security design typically applies defense in depth
>     *   authentication, firewalls, DMZ, IPS, IDS, filters, VPN... etc
>     *   biometrics, smart cards, tokens... etc
> 4.  Cost
>     *   The design needs to be "good enough" to meet business requirements
>     *   The design needs to fit within the budget

and from [this](http://www.virten.net/2012/06/vdcd510-objective-2-3-build-availability-requirements-into-the-logical-design/) blog:

> **Availability** is the ability of a system or service to perform its required function when required. It is usually calculated as a percentage like 99,9%.
>
> **Manageability** describes the expense of running the system. If you have a huge platform that is managed by a tiny team the operational costs are very low.
>
> **Performance** is the measure of what is delivered by a system. This accomplishment is usually measured against known standards of speed completeness and speed.
>
> **Recoverability** describes the ability to return a system or service to a working state. This is usually required after a system failure and repair.
>
> **Security** is the process of ensuring that services are used in an appropriate way.

### Describe the concept of redundancy and the risks associated with single points of failure

From the same blog again:

> **Redundancy and Single Point of Failure** A single point of failure is a component of a system that, if it fails, will cause the entire system to fail. Systems can be made robust by adding redundancy. A server usually attains internal component redundancy by having multiple hard drives, network connections or power supplies. By having multiple servers attached to a cluster you can achieve server hardware redundancy.

Also from this VMware article "[vSphere High Availability Deployment Best Practices](https://raw.githubusercontent.com/elatov/upload/master/vcap-dcd/2-3/vmw-vsphere-high-availability.pdf)", linked in the blue print:

> **Design Principles for High Availability**
> The key to architecting a highly available computing environment is to eliminate single points of failure. With the potential of occurring anywhere in the environment, failures can affect both hardware and software. Building redundancy at vulnerable points helps reduce or eliminate downtime caused by [implied] hardware failures. These include redundancies at the following layers:
>
> *   Server components such as network adaptors and host bus adaptors (HBAs)
> *   Servers, including blades and blade chassis
> *   Networking components
> *   Storage arrays and storage networking

### Differentiate Business Continuity and Disaster Recovery concepts

From [this](http://www.virten.net/2012/06/vdcd510-objective-2-3-build-availability-requirements-into-the-logical-design/) blog:

> **Differentiate Business Continuity and Disaster Recovery**
> **Business Continuity** is focused on avoiding or mitigateing the impact of a risk. (Proactive)
>
> **Disaster Recovery** is focused on how to restore the services after a outage occurs. (Reactive)

Here a slide from the [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/):

![dr_vs_bc](https://github.com/elatov/uploads/raw/master/2012/08/dr_vs_bc.png)

### Determine availability component of service level agreements (SLAs) and service level management processes

From [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/) slide deck:

![types_of_failures](https://github.com/elatov/uploads/raw/master/2012/08/types_of_failures.png)

Define an SLA for each and design a setup that will accommodate. For example if your SLA for a certain VM failure is 0, then configure that VM for FT. Or if your SLA is a couple minutes then VMware HA should be good enough. If there are other services that you commit to (i.e. performance) then create storage tiers as necessary.

### Explain availability solutions for a logical design based on customer requirements

The popular logical design that we have seen is the remote site replication, here is that diagram:

![srm-logical-diagram](https://github.com/elatov/uploads/raw/master/2012/08/srm-logical-diagram.png)

### Define an availability plan, including maintenance processes.

Another good link from the blue print is "[Business Continuity](http://www.vmware.com/business-continuity/high-availability)". From one of the articles:

> VMware vSphere makes it possible to reduce both planned and unplanned downtime without the cost and complexity of alternative solutions. Organizations using VMware can slash planned downtime by eliminating most scheduled downtime for hardware maintenance. VMware VMotion™ technology, VMware Distributed Resource Scheduler (DRS) maintenance mode, and VMware Storage VMotion™ make it possible to move running workloads from one physical server to another without downtime or service interruption, enabling zero-downtime hardware maintenance.

Depending on what type of failure you are defining a plan for, do it properly. For SRM create an appropriate Run book. This will be used during a site failure. For host upgrades, make a plan to vMotion all the VMs and ensure there are available resources for all the VMs with one host down, then update the host. For VM maintenance take a snapshot and then revert back if the VM upgrade didn't go well.

### Prioritize each service in the Service Catalog according to availability requirements

Using VMware HA set the reboot priority depending on the availability requirements. Most important Services/VMs can have the highest priority during an HA failover. From the "[vSphere Availability](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-703-availability-guide.pdf)" PDF, linked in the blue print:

> **VM Restart Priority Setting**
> VM restart priority determines the relative order in which virtual machines are restarted after a host failure.Such virtual machines are restarted sequentially on new hosts, with the highest priority virtual machines first and continuing to those with lower priority until all virtual machines are restarted or no more cluster resources are available.

### Balance availability requirements with other infrastructure qualities

From the [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/):

![infra_qualities](https://github.com/elatov/uploads/raw/master/2012/08/infra_qualities.png)

From the VMware Article "[Improving Business Continuity with VMware Virtualization](https://github.com/elatov/uploads/raw/master/2012/11/Improving_Business_Continuity_With_VMware_Virtualization.pdf)"

> VMware also helps protect against unplanned downtime from common failures, including:
>
> *   **Network and storage interface failures**. Support for redundant network and storage interfaces is built into VMware ESX™. Redundant network and storage interface cards can be shared by multiple virtual machines on a server, reducing the cost of implementing redundancy. VMware virtualization also makes it easy to create redundant servers without additional hardware purchases by allowing for the provisioning of virtual machines to existing underutilized servers.
> *   **Server failures**. VMware High Availability (HA) and VMware Fault Tolerance deliver protection against server failures without the cost and complexity often associated with implementing and maintaining traditional solutions. VMware HA automatically restarts virtual machines affected by server failures on other servers to reduce downtime from such failures to minutes, while VMware Fault Tolerance ensures continuous availability for virtual machines by using VMware vLockstep technology to create a live shadow instance of a virtual machine on another server and allow instantaneous, stateful failover between the two instances.
> *   **Overloaded servers**. VMware VMotion, VMware Distributed Resource Scheduler (DRS), and VMware Storage VMotion help you to proactively balance workloads across a pool of servers and storage.

Using vMotion,HA, DRS and redundant network and storage components we can balance availability across all the infrastructure components.

I would recommend watching:

*   [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/)

There is also an excellent course on this:

*   [Business Continuity and Disaster Recovery](https://www.udemy.com/course/business-continuity-and-disaster-recovery-b)

It's has a nice overview.

