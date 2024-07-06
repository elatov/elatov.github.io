---
title: VCAP5-DCD Objective 3.1 – Transition from a Logical Design to a vSphere 5 Physical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-3-1-transition-from-a-logical-design-to-a-vsphere-5-physical-design/
categories: ['vcap5_dcd', 'vmware', 'certifications']
tags: ['logical_design', 'physical_design']
---

### Determine and explain design decisions and options selected from the logical design

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> **Physical Design**
>
> *   Uses the Logical Design
> *   Uses Specific Hardware detains and implementation information
> *   Includes port assignments, pci slots, etc...

Here is an example of a physical diagram, taken from "[VMware vCloud Implementation Example](http://www.vmware.com/solutions/cloud-computing/vcat-toolkit.html":

![physical-design-diag](https://github.com/elatov/uploads/raw/master/2012/08/physical-design-diag.png)

### Build functional requirements into the physical design

Let's say we had a need for a DMZ, if this was the case, then we would either get a separate switch to be extra secure, or dedicate a new VLAN for our DMZ traffic. We would then allocate a port on the physical switch for our DMZ traffic. Either or, we have to show which port is allowing DMZ traffic.

### Given a logical design, create a physical design taking into account requirements, assumptions and constraints

Let's say we looked at some of the previous logical diagrams:

![logical-diagram](https://github.com/elatov/uploads/raw/master/2012/08/logical-diagram.png)

Now our physical diagram would include:

*   All the IPs of the hosts
*   Hardware Models of the host , Arrays, and switches/routers
*   What type of link is between the Arrays
*   What type of devices (switches, routers) are between the hosts and sites
*   What ports we are connected on the switch, fiber or ethernet

### Given the operational structure of an organization, identify the appropriate management tools and roles for each staff member

From the [vSphere Security Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-703-security-guide.pdf), here is a list of predefined roles:

> *   No Access
> *   Read Only
> *   Administrator
> *   Virtual Machine Power User
> *   Virtual Machine User
> *   Resource Pool Administrator
> *   Datastore Consumer
> *   Network Consumer

The default should be enough for most cases. It depends on how many people are actually going to be working on the virtualized environment and what policies have been set in place. For example if there is a change control in place for deploying a VM, then have a dedicated "Virtual Machine Power User" role defined to have the ability to create VMs. Also have a bunch of users be in the "Virtual Machine Users" role and they will be only allowed to use the VMs. With both of these in place, you can ensure that one person keeps track of changes ( what VMs are deployed ) and regular users in the "Virtual Machine Users" won't be able to make any changes, but can still use the VMs that are already deployed.

### Related Posts

- [VCAP5-DCD Objective 4.3 – Create an Installation Guide](/2012/09/vcap5-dcd-objective-4-3-create-an-installation-guide/)
- [VCAP5-DCD Objective 4.2 – Create an Implementation Plan](/2012/09/vcap5-dcd-objective-4-2-create-an-implementation-plan/)
- [VCAP5-DCD Objective 4.1 – Create an Execute a Validation Plan](/2012/09/vcap5-dcd-objective-4-1-create-an-execute-a-validation-plan/)
- [VCAP5-DCD Objective 3.6 – Determine Datacenter Management Options for a vSphere 5 Physical Design](/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/)
- [VCAP5-DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design](/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/)

