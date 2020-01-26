---
title: VCAP5-DCD Objective 2.7 – Build Security Requirements into the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-7-build-security-requirements-into-the-logical-design/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['vshield', 'logical_design']
---

### Understand what security services are provided by VMware solutions

vShield is the most popular service. If you need PCI compliance you can check out "[this](https://blogs.vmware.com/security/2014/02/vmware-cpc-releases-pci-dss-3-0-compliance-toolkit-virtual-environments-vcm.html) VMware blog:
![compliance](https://github.com/elatov/uploads/raw/master/2012/08/compliance.png)

VMware also provides hardening guides for each version of ESX, and here a [link](https://www.vmware.com/support/support-resources/hardening-guides.html) to all the different versions.

### Identify and differentiate infrastructure qualities (Availability, Manageability, Performance, Recoverability, Security).

Described in previous objectives

### Describe layered security considerations, including but not limited to Trust Zones

There is actually a [great](http://www.techrepublic.com/blog/it-security/understanding-layered-security-and-defense-in-depth/) blog on this. From that blog:

> **Layered Security**
> A layered approach to security can be implemented at any level of a complete information security strategy. Whether you are the administrator of only a single computer, accessing the Internet from home or a coffee shop, or the go-to guy for a thirty thousand user enterprise WAN, a layered approach to security tools deployment can help improve your security profile.
>
> In short, the idea is an obvious one: that any single defense may be flawed, and the most certain way to find the flaws is to be compromised by an attack — so a series of different defenses should each be used to cover the gaps in the others’ protective capabilities. Firewalls, intrusion detection systems, malware scanners, integrity auditing procedures, and local storage encryption tools can each serve to protect your information technology resources in ways the others cannot.
>
> Security vendors offer what some call vertically integrated vendor stack solutions for layered security. A common example for home users is the Norton Internet Security suite, which provides (among other capabilities):
>
> 1.  an antivirus application
> 2.  a firewall application
> 3.  an anti-spam application
> 4.  parental controls
> 5.  privacy controls

And Regarding Trust Zones, from "[Network Segmentation in Virtualized Environments](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/network_segmentation.pdf)":

> As virtualization becomes the standard infrastructure for server deployments, a growing number of organizations want to consolidate servers that belong to different trust zones. A trust
> zone is loosely defined as a network segment within which data flows relatively freely, whereas data flowing in and out of the trust zone is subject to stronger restrictions. Examples of trust
> zones include:
>
> *   Demilitarized zones (DMZs)
> *   Payment card industry (PCI) cardholder data environment
> *   Site-specific zones, such as segmentation according to department or function
> *   Application-defined zones, such as the three tiers of a Web application

### Identify required roles, create a role-based access model and map roles to services

From the [APAC BrownBag Session 5](http://vimeo.com/38646355) slide deck:

![separation_of_duties](https://github.com/elatov/uploads/raw/master/2012/08/separation_of_duties.png)

### Create a security policy based on existing security requirements and IT governance practices

From this [great](http://communities.vmware.com/servlet/JiveServlet/download/1633024-44565/VMUG%20Presentation.pptx) VMUG presentation by Rob Randell:

![secure_and_compliant](https://github.com/elatov/uploads/raw/master/2012/08/secure_and_compliant.png)

and here is another slide from the above deck:

![securing-examples](https://github.com/elatov/uploads/raw/master/2012/08/securing-examples.png)

### Incorporate customer risk tolerance into the security policy

From the [vSphere Security Guide](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf):

> In addition to implementing the firewall, risks to the hosts are mitigated using other methods.
>
> *   ESXi runs only services essential to managing its functions, and the distribution is limited to the features required to run ESXi.
> *   By default, all ports not specifically required for management access to the host are closed. You must specifically open ports if you need additional services.
> *   By default, weak ciphers are disabled and all communications from clients are secured by SSL. The exact algorithms used for securing the channel depend on the SSL handshake. Default certificates created on ESXi use SHA-1 with RSA encryption as the signature algorithm.
> *   The Tomcat Web service, used internally by ESXi to support access by Web clients, has been modified to run only those functions required for administration and monitoring by a Web client. As a result, ESXi is not vulnerable to the Tomcat security issues reported in broader use.
> *   Insecure services such as FTP and Telnet are not installed, and the ports for these services are closed by default.

So if you don't care if an ESX server gets hacked, then open all the ports. If you do care, take extra care when opening ports on the ESXi firewall. Or if you don't care that you have a 30% of getting a Virus on just of 1 the VMs then don't do anything. If you do care, implement vShield endpoint to lower that percentage to 10%.

### Given security requirements, assess the services that will be impacted and create an access management plan

Let's say you have a requirement for certain VMs not to be access from the internet (ie Database Server, all queries should be made locally). So you end up putting your DB server in a NAT either using vShield or a physical firewall. With this configuration it will be more difficult to access this server and other services (ie web server) could be impacted as well. So plan ahead and open up appropriate ports on the firewall that are used for NAT to allow the necessary ports to have local access.

### Given a regulatory requirement example, determine the proper security solution that would comply with it

From "[Infrastructure Security: Getting to the Bottom of Compliance in the Cloud](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/products/cloud-services/vmware-cloud-services-on-aws-security-overview-white-paper.pdf)", linked in the blue print:

> **Build secure clouds customized to comply with the most rigorous requirements.**
> The secure cloud’s ability to map high-trust zones of systems will enable organizations and cloud providers to customize their clouds to comply specifically with PCI DSS, HIPAA or other highly
> controlled information standards. Then, trusted pools of cloud-based resources – all compliant with the same set of information standards – could be dynamically allocated to optimize workloads. Such a scenario would extend the cloud’s efficiency and scalability benefits to even the most strictly controlled business processes and heavily regulated industries.
>
> Furthermore, cloud services could be fine-tuned to provide different levels of data security. For instance, two clouds could be proven HIPAA-compliant, with one cloud tuned to provide lower-level security at a lower cost for data such as patients’ insurance information. The other HIPAA-compliant cloud, handling sensitive health information such as patient medical histories, would be tuned for maximum security. By tailoring cloud service levels, security and pricing to the value of information handled within each cloud, organizations provisioning private clouds can buy only what they need, making the cost benefits and business case for moving into the cloud even more compelling.

With vShield you can setup NATs, DMZs, Virus Checkers, and much more. There is even a data security scanner, from the "[vShield Administration Guide](http://www.vmware.com/pdf/vshield_50_admin.pdf)":

> **Defining a Data Security Policy**
> To detect sensitive data in your environment, you must create a data security policy. To define a policy, you must specify the following:
>
> 1.  Regulations
>     *   A regulation is a data privacy law for protecting PCI (Payment Card Industry), PHI (Protected Health Information) and PII (Personally Identifiable Information) information. You can select the regulations that your company needs to comply to. When you run a scan, vShield Data Security identifies data that violates the regulations in your policy and is sensitive for your organization.

### Based upon a specified security requirement, analyze the current state for areas of compliance/non-compliance.

From the [VMware Compliance site](https://blogs.vmware.com/security/2014/02/vmware-cpc-releases-pci-dss-3-0-compliance-toolkit-virtual-environments-vcm.html):

> With proper technology based solutions such as VMware vShield and VMware vCenter Configuration Manager, achieving and demonstrating compliance on VMware vSphere based infrastructures is not only possible, but can often be easier than achieving the same on non virtualized environments.

The above mentioned Compliance checker has been integrated into VMware vCenter Configuration Manager, so you can use that to see if you are compliant or not. Here is what the application looks like:
![vcm-compliance](https://github.com/elatov/uploads/raw/master/2012/08/vcm-compliance.png)

### Explain how compliance requirements will impact the logical security design

Just depends on what is required. If you have to setup a DMZ, then an additional network will be added. If you need off site backups for compliance then you WAN architecture might change as well. If you need to use vShield Endpoint for a virus Scanner, then maybe getting hosts with more CPUs would be beneficial.

Recommended readings/recordings:

*   [APAC BrownBag Session 5](http://vimeo.com/38646355)
*   [vSphere Security Guide](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-security-guide.pdf)
*   [VMware Security Briefing](http://communities.vmware.com/servlet/JiveServlet/download/1633024-44565/VMUG%20Presentation.pptx)
*   [Infrastructure Security: Getting to the Bottom of Compliance in the Cloud](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/products/cloud-services/vmware-cloud-services-on-aws-security-overview-white-paper.pdf)

