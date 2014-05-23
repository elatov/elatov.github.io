---
title: VCAP5-DCD Objective 2.1 –Map Business Requirements to the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-1-map-business-requirements-to-the-logical-design/
dsq_thread_id:
  - 1405451582
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Explain the common components of logical design

I covered this in the previous objective, but I will use the same material:

> **Logical Design**
>
> *   Design includes relationships between all major components of the infrastructure.
> *   Considers the conceptual design, constraints, and risks
> *   Useful for understanding and evaluating the design of the infrastructure
>     *   Does it meet the requirements but stay within the constraints?
> *   Does NOT include physical details like port assignments, hardware, vendors, IPs, etc
> *   illustrate how to arrange infrastructure components
> *   don't get lost in the configuration details
> *   be aware of capacity analysis, but include things like LUN sizing, CPU, etc
> *   document in diagrams, tables, and text

### List the detailed steps that go into the makeup of a common logical design

Same as the previous objective

### Differentiate functional and non-functional requirements for the design

From [this](http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/) blog:

> **Functional requirements** are tasks or processes that must be performed by the system. For example, a functional requirement of a vSphere platform is “must allow multi tenancy” or “users must be able to create virtual machines”.
>
> **Non-functional requirements** are standards that the system under must have or comply with. For example, a non-functional requirements for a vSphere platform is “must be built for a total cost of $500.000″. Non-Functional requirements are also called constraints.

### Build non-functional requirements into a specific logical design

If we checkout a picture from the previous objective:
![another-conceptual-diag](https://github.com/elatov/uploads/raw/master/2012/08/another-conceptual-diag.png)
We can see that our non-functional requirement was that the web-server has to be in a DMZ, but we don't really have specific IPs of all the firewalls involved in the setup.

### Translate given business requirements and the current state of a customer environment into a logical design

If we again look at this picture from the previous objectives:
![logical-diagram](https://github.com/elatov/uploads/raw/master/2012/08/logical-diagram.png)

We can see that a non-functional requirement was to allow for a protected site. We don't really mention if SRM will be used or if we will be using Array Based replication or vSphere Based Replication. We just have a logical diagram of a protected site that is replicated.

### Create a Service Catalog

From this blog:

> **Service Catalog**
> A new part in this objective and derived from ITIL is the service catalog. A service catalog is a list of services that a company provides to its customers. The catalog should provide the following information:
>
> *   Service name (Extended Support)
> *   Service description (Maintenance and support of servers and components)
> *   Services included (Patch management, upgrades, incident support)
> *   Services not included (Non-standard changes)
> *   Services availability  (24x7x365)

If you want more information on Service Catalog, I would suggest reading this paper mentioned in the blue print:

*   [ITIL v3 Introduction and Overview](http://communities.vmware.com/docs/DOC-17410)

