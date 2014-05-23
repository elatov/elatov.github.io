---
title: VCAP5-DCD Objective 2.4 – Build Manageability Requirements into the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-4-build-manageability-requirements-into-the-logical-design/
dsq_thread_id:
  - 1408078212
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Understand what management services are provided by VMware solutions

The [APAC BrownBag Session 11](http://professionalvmware.com/2012/04/apac-vbrownbag-follow-up-management-design/) Slide Deck, covers these, here is a list from the slide deck:

> *   vMA
> *   vCenter
> *   PowerCLI
> *   vCLI
> *   vCenter Orchestrator
> *   vSphere API
> *   vSphere HA
> *   vSphere DRS
> *   Auto Deploy
> *   Scheduled Tasks
> *   Host Profiles

### Identify and differentiate infrastructure qualities (Availability, Manageability, Performance, Recoverability, Security)

These were covered in the previous objective

### Build interfaces to existing operations practices into the logical design

Figure out what is currently used for Management and try to integrate vCenter into it. Here is a logical diagram of vCenter managing a vSphere Environment:

![logical-diag-vcenter](https://github.com/elatov/uploads/raw/master/2012/08/logical-diag-vcenter.png)

You can also integrate vCenter into LDAP, this will allow easier manageability.

### Address identified operational readiness deficiencies

If you discovered something during the initial-state analysis then plan to get around the issue. For example let's say there is no notifications available for machines going down. Setup vCenter Alarms and snmp traps to allow for monitoring and send email alerts for critical vCenter Alarms.

### Define Event, Incident and Problem Management practices

From [this](http://www.virten.net/2012/06/vdcd510-objective-2-4-build-manageability-requirements-into-the-logical-design/) blog:

> **Event, Incident and Problem Management**
> This concept is related to the well known ITIL standard.
>
> **Event**: A change of state which might have an influence for the management of a service or system
> **Incident**: An event which is not part of the standard operation. It might cause a service disruption or reduce the productivity.
> **Problem**: The cause of one or more incidents. Problems are usually identified because of multiple incidents.
>
> Please note that an incident might give a hint to the investigation of a Problem, but never become a Problem. Even if the incident is elevated to the 2nd level, it remains an incident. The problem management might manage the resolution of the incident when the incident can only be closed by solving the Problem.

### Define Release Management practices

From this PDF (it's linked in the blue print):

*   [ITIL v3 Introduction and Overview](http://communities.vmware.com/docs/DOC-17410)

It describes the process:

> **Release and Deployment Management**
> The goal of the Release and Deployment Management process is to assemble and position all aspects of services into production and establish effective use of new or changed services. Effective release and deployment delivers significant business value by delivering changes at optimized speed, risk and cost, and offering a consistent, appropriate and auditable implementation of usable and useful business services.
> Release and Deployment Management covers the whole assembly and implementation of new/changed services for operational use, from release planning through to early life support.

Basically define a process to get a service into production. Each company uses their own special tweaks. To make it easier, create one VM with all the tweaks defined and make a template out of it. Also use tools like sysprep and guest customizations to automate the process

### Determine Request Fulfillment processes

From the same ITIL document as above:

> **Request Fulfillment Process**
> A service request is a request from a user for information or advice, or for a standard change, or for access to an IT service. The purpose of Request Fulfillment is to enable users to request and receive
> standard services; to source and deliver these services; to provide information to users and customers about services and procedures for obtaining them; and to assist with general information, complaints and comments.
> All requests should be logged and tracked. The process should include appropriate approval before fulfilling the request.

Define rolls within vCenter, some user can just use VMs some users can deploy VMs. Have a defined roll in the company to be responsible for deploying specific VMs from templates as necessary. This way the environment is kept in good health and all changes are known. Also vCenter Orchestrator can allow for flows. People can login and deploy VMs from there. You can create custom rules to email people upon deploying a new VM. Again, this way you can keep track of your Environment.

### Design Service Asset and Configuration Management (CMDB) systems

From the same ITIL Document:

> **Service Asset and Configuration Management (SACM)**
> SACM supports the business by providing accurate information and control across all assets and relationships that make up an organization’s infrastructure. The purpose of SACM is to identify, control and account for service assets and configuration items (CI), protecting and ensuring their integrity across the
> service lifecycle.
>
> The scope of SACM also extends to non-IT assets and to internal and external service providers, where shared assets need to be controlled. To manage large and complex IT services and infrastructures, SACM requires the use of a supporting system known as the Configuration Management System (CMS).

On top of what was described in the previous objective, also define a roll who can make changes to the golden templates. New changes come in and updates come out, all of these have to be kept up to date. With a defined roll to complete this, all changes are known for tracking purposes. Also VMware provides a product vCenter Configuration Manager, here is how it looks like:

![conf-manager](https://github.com/elatov/uploads/raw/master/2012/08/conf-manager.png)

With this tool you can keep track of all the changes that took place in your environment.

### Define Change Management processes

From the ITIL document:

> **Change Management**
> Change Management ensures that changes are recorded, evaluated, authorized, prioritized, planned, tested, implemented, documented and reviewed in a controlled manner.
>
> The purpose of the Change Management process is to ensure that standardized methods are used for the efficient and prompt handling of all changes, that all changes are recorded in the Configuration Management System and that overall business risk is optimized.
>
> The process addresses all service change. A Service Change is the addition, modification or removal of an authorised, planned or supported service or service component and its associated documentation.

This is really important, and it doesn't only apply to a VMware Environment. It's great for keeping any environment trouble free. Most issues can be tracked down to a new change that took place recently. With all of the changes in one place you can figure what could've caused an issue (the change could be network, storage, or physical machine). There are many tools out there that allow for change control here is an example of one called "[article](http://www.manageengine.com/products/service-desk/itil-change-management.html), here are some examples:

> CHANGE MANAGEMENT FOR VIRTUAL ENVIRONMENTS
> One of the most frequently asked questions we receive from clients around change control is “Should we do a change request for a VMotion.” This is interesting because of all the new things going on in the environment and all the moving parts, the one that gets the most attention is VMotion.
> ...
> ...
> Below is a list of common changes that you will need to consider (that are new to the environment):
>
> *   VMotion – Movement of a VM between hosts,
> *   VM Configuration changes – virtual hardware or share changes
> *   Deployment / introduction of new VMs to the environment
> *   Host configuration changes – Prior to failure or maintenance type change, uses VMotion to move VMs to other hosts, so that the originating server can be repaired (maintenance mode)
> *   Patches and updates for ESX hosts, host hardware maintenance, etc.
> *   DRS – Automatic load‐leveling on hosts using VMotion, could occur daily or hourly
> *   Cluster change – Addition of LUNs, rescan of storage
> *   Cluster change – Removal of LUNs
> *   Cluster change – Upgrade of hosts – Potential impact major – Downtime of VMs not always required
> *   VMTools upgrades (during major host upgrade) requires VM restart on installation of new tools
> *   Addition of hosts to an existing cluster
> *   VirtualCenter updates – no VM changes, but possible loss of access to VMs viaVirtual center

### Based on customer requirements, identify required reporting assets and processes

Determine what needs to be kept track of and monitor that. If you are using a VDI environment, keeping track of any new file placed in a View Client, would be too much and unnecessary. Choose what is important, newly deployed VMs, networking changes, storage pathing changes... etc. Choose the appropriate level of importance/monitoring for each aspect (these could be defined by constraints, requirements, and even SLAs). There are third party applications like [puppet](http://puppetlabs.com/puppet/what-is-puppet/) that use a client-server methodology to keep track of your environment's inventory.

For this objective, I would recommend reading/watching:

*   [ITIL v3 Introduction and Overview](http://communities.vmware.com/docs/DOC-17410)
    *   Defines all the ITIL aspects really well
*   [Four Keys to Managing Your VMware Environment](http://communities.vmware.com/docs/DOC-17397)
    *   Written by Glasshouse, has a good example of how to apply the above in an environment
*   [Operational Readiness Assessment](http://communities.vmware.com/docs/DOC-11457)
    *   Has a list of questions if trying to follow the ITIL methodology
*   [APAC BrownBag Session 11](http://professionalvmware.com/2012/04/apac-vbrownbag-follow-up-management-design/)
    *   Good recording and discussion on how to manage a vSphere Environment

