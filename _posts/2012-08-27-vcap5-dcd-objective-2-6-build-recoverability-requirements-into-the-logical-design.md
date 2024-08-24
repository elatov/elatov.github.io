---
title: VCAP5-DCD Objective 2.6 – Build Recoverability Requirements into the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-6-build-recoverability-requirements-into-the-logical-design/
dsq_thread_id:
  - 1404673579
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['logical_design']
---

### Understand what recoverability services are provided by VMware solutions

Here is a list of VMware provides for recoverability:

*   Site Recovery Manager (SRM)
    *   Allows for site failures
*   VMware Data Recovery (VDR)
    *   Backup Appliance, allows you to restore VMs that you have backed up
*   vStorage APIs for Data Protection (VADP)
    *   Allows other Vendors (ie Symantec,EMC,Veeam...etc to backup VMs via API calls)

### Identify and differentiate infrastructure qualities (Availability, Manageability, Performance, Recoverability, Security)

Defined in previous objectives

### Differentiate Business Continuity and Disaster Recovery concepts.

Defined in [Objective 2.3](/2012/08/vcap5-dcd-objective-2-3-build-availability-requirements-into-the-logical-design/)

### Describe and differentiate between RTO and RPO

From the [APAC BrownBag Session 4](https://professionalvmware.com/vmware-certifications/):
![rpo_vs_rto](https://github.com/elatov/uploads/raw/master/2012/08/rpo_vs_rto.png)

### Given specific RTO and RPO requirements, build these requirements into the logical design

There is a great VMware article that has SRM Design considerations, and it's of course linked in the blue print. Here is this article "[A Practical Guide to Business Continuity and Disaster Recovery with VMware Infrastructure](https://blogs.vmware.com/vmtn/2008/08/book-a-practica.html)" and here are some excerpts from that article:

> The granularity study will be invaluable in understanding the replication strategy that you want implement. The main considerations here are: rate of change and groupings. Groupings are driven by the granularity study which we referred to above. Then a deeper level of analysis is required to establish the rate of change which determines WAN bandwidth requirements etc. This in conjunction with the Recovery Point Objectives can drive decisions around synchronous and asynchronous replication technologies. With these in mind it is then possible to have detailed discussions with the storage teams to line up the capabilities of the storage layer and its granularity to ensure a good mapping between the two.
>
> Of course there are different ways of achieving the replication, we used the array technology to achieve this step but as long as the RPOs are met it may be possible to achieve a level of replication via a continuous backup recovery cycle using VMware VCB for example instead of using an array based solution.

### Given recoverability requirements, identify the services that will be impacted and provide a recovery plan for impacted services.

From the same PDF as mentioned in the previous objective:

> This virtualization team will also be called upon to work closely with business continuity program (BCP) team members whose responsibility is to work closely with business owners to determine the criticality of the business applications and their respective service level agreements (SLAs) as they relate to recovery point objectives (RPOs) and recovery time objectives (RTOs). The BCP team will also determine how those business applications map to business users who use the business applications services during their daily operations. The list of business application services then gets mapped to both physical and virtual systems, along with their appropriate dependencies. This list of systems forms the basis of the BCDR plan that will be implemented in part by the virtualization team, as well as other IT teams that are responsible for the non-virtualized business applications services.

### Given specific regulatory compliance requirements, build these requirements into the logical design.

If there is a need to have backups every 4 hours for a certain VM due to PCI compiance, then we can set the RPO for a VM to that value. This of course will need more bandwidth, from the same article:

> If the intent is to provide BCDR services based on array-based data replication (as this the intent in this VMbook), then a dedicated point-to-point connection is required between the two sites. The SLAs for WRT to RPO and RTO will ultimately drive the amount of bandwidth that is required to sustain the agreed upon SLAs of the business.

### Based on customer requirements, identify applicable site failure / site recovery use cases

If there is a requirement to have uptime for a certain site to be 95% of the year then SRM can be utilized to make that uptime is respected even during catastrophes.

### Determine recoverability component of SLAs and service level management processes

From the PDF again:

> In a real-world scenario, there would be an interaction with the business owners to establish SLAs and these would drive design considerations. The implementation outlined in this VMbook was designed to apply generically to as many cases as possible and was based in part on interviews with senior architects within the VMware customer base to determine a "level set" in terms of needs,requirements, and so on. Typical questions asked of these architects include the following:
>
> 1.  What type of SLAs do you have with the business?
>     *   Recovery Point Objectives
>     *   Recovery Time Objectives

SRM also allows for site failover and test site failovers. Also during site failures, runbooks are used to make sure everything is up as it was on the production site. SRM allows the automation of these runbooks. From the same PDF:

> BCDR plans have traditionally been documented as runbooks – i.e., what to do if disaster strikes. Increasingly, this runbook is being automated to make the process more predictable and less prone to error. The ability to test this plan is also a key consideration.

Also from "[VMware vCenter Site Recovery Manager 5with vSphere Replication](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-vcenter-site-recovery-manager-with-vsphere-replication-datasheet.pdf)":

> **Simplify the setup of recovery and migration plans.**
> Traditional recovery plans are complex to set up. They are usually captured in manual runbooks, which are error-prone and quickly fall out of sync with configuration changes. With Site Recovery Manager, setting up a recovery plan is simple and can be done in a matter of minutes, instead of the weeks required to set up traditional runbooks. Through an interface that is tightly integrated with vCenter Server, the user simply selects which virtual machines to protect, maps virtual machines to resources at the recovery site and specifies the virtual machine boot sequence. Site Recovery Manager automatically dramatically simplifies recovery plans by automatically coordinating most of the manual steps of traditional recovery plans.
> ...
> ...
> **Automate site recovery and migration processes to ensure fast and reliable RTOs**.
> Site Recovery Manager automates the entire site recovery and migration process. Upon initiation of a disaster failover, business services are automatically recovered with no manual intervention. Because automation eliminates the risk inherent in manual processes, disaster failover can be executed much faster and with highly predictable RTOs. Typical recovery times vary between 30 minutes and a couple of hours, depending on the configuration.
> ...
> ...
> **Setup of recovery plans.** Site Recovery Manager provides an intuitive interface to help users create recovery plans for different failover scenarios. Users can map production resources to recovery resources, specify which virtual machines to protect and their relative boot sequences, and identify low-priority virtual machines to suspend at the failover site. Users can also include custom scripts and automatically reconfigure IP addresses for their virtual machines.

So with runbooks, scripts to setup IPs, and setting up custom RTOs, you can document the appropriate failover procedures and expected time to recovery in case of a disaster.

### Based on customer requirements, create a data retention policy.

With VMware Data Recovery you can define a retention policy. From "[VMware Data Recovery Administration Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vdr_12_admin.pdf)":

> **Retention Policy**
> Data Recovery backups are preserved for a variable period of time. You can choose to keep more or fewer backups for a longer or shorter period of time. Keeping more backups consumes more disk space, but also provides more points in time to which you can restore virtual machines. As backups age, some are automatically deleted to make room for new backups. You can use a predefined retention policy or create a custom policy.

Definitely read over this document to get a good feeling of how to setup SRM and how it applies to business needs (SLAs, RPOs, and RTOs):
[A Practical Guide to Business Continuity and Disaster Recovery with VMware Infrastructure](https://blogs.vmware.com/vmtn/2008/08/book-a-practica.html)

There is a lot of cases studies for SRM found here:
[VMware vCenter Site Recovery Manager](https://www.vmware.com/products/cloud-infrastructure/live-recovery#case-studies)

