---
title: VCAP5-DCD Objective 4.2 – Create an Implementation Plan
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-4-2-create-an-implementation-plan/
dsq_thread_id:
  - 1404915081
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Based on key phases of enterprise vSphere 5 implementations, map customer development needs to a standard implementation plan template.

Most organizations have a pre-built template for these designs. Actually Duncan Epping blogged about it in &#8220;<a href="http://www.yellow-bricks.com/2011/02/02/using-the-vsphere-plan-design-kit/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2011/02/02/using-the-vsphere-plan-design-kit/']);">Using the vSphere Plan & Design Kit</a>&#8220;. Here is an example from from the blog:

> Just to give an example of something that I see in 90% of the designs I review:
> 
> *   Max amount of VMs per datastore 15
> *   Datastore size 500GB
> *   Justification: To reduce SCSI reservations

### Evaluate customer implementation requirements and provide a customized implementation plan.

Here is a small example of an implementation plan:

**To implement an infrastructure**

1.  Build the ESXi hosts.
2.  Build the vCenter server.
3.  Install Update Manager.
4.  Install vCenter.
5.  Verify that the infrastructure is installed correctly
6.  Verify that the implemented design conforms

### Incorporate customer objectives into a phased implementation schedule

From &#8220;<a href="http://download3.vmware.com/elq/pdf/wp_roadmaptovirtualinfrastructure.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://download3.vmware.com/elq/pdf/wp_roadmaptovirtualinfrastructure.pdf']);">The Roadmap to Virtual Infrastructure: Practical Implementation Strategies</a>&#8220;:

> **Typical Deployment Phasing**  
> While the goal of virtualization is to improve operations and reduce cost, the best practice in deploying virtualization is to take a phased implementation approach where you focus on the following areas:
> 
> *   Early ROI: Choose first phase candidate workloads that are low risk, high visibility and generate early ROI.
> *   Low Risk: Scope initial projects appropriately to mitigate any inherent risks in deployment
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/deployment_phase.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/deployment_phase.png']);"><img class="alignnone size-full wp-image-3381" title="deployment_phase" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/deployment_phase.png" alt="deployment phase VCAP5 DCD Objective 4.2 – Create an Implementation Plan " width="511" height="428" /></a>

### Match customer skills and abilities to implementation resource requirements

From &#8220;<a href="http://download3.vmware.com/elq/pdf/wp_roadmaptovirtualinfrastructure.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://download3.vmware.com/elq/pdf/wp_roadmaptovirtualinfrastructure.pdf']);">The Roadmap to Virtual Infrastructure: Practical Implementation Strategies</a>&#8220;:

> **Build a Virtualization Center of Excellence (2 to 4 weeks)**  
> Build a core virtualization team. The team should be comprised of individuals with the following characteristics:
> 
> *   Working knowledge of a virtualized environment – this may require supplemental training such as VMware Certified Professional (VCP) training.
> *   Familiarity with current IT infrastructure operations.
> *   Credibility with business application owners as well as IT infrastructure leaders.
> 
> The key roles for the team are listed below.
> 
> *   Relationship Manager – Act as primary interface between application owners and infrastructure groups.
> *   IT Analyst – Identify impacted operational areas and recommend changes.
> *   IT Infrastructure Architect – Translate requirements into architectural designs.
> *   IT Infrastructure Engineer – Provide specific technical design for virtualized solutions.
> 
> The size of the team will vary depending on the scope and size of deployments, but it can be as small as three people or larger where multiple people are acting in each role. These positions should be viewed as relatively senior positions for highly regarded and skilled employees. Suitable candidates can often be found in the current organization (for example, in relationship management, IT infrastructure architecture, or server engineering groups). Once the team is in place, the team members play a central role in the deployment of projects in a virtualized environment.

### Identify and correct implementation plan gaps

If the customer is confused about any of the following:

1.  Build the ESXi hosts.
2.  Build the vCenter server.
3.  Install Update Manager.
4.  Install vCenter.
5.  Verify that the infrastructure is installed correctly
6.  Verify that the implemented design conforms

Try to expand the steps, like this:

1.  Build the ESXi hosts. 
    1.  Use the vSphere Installation and Setup Guide.
    2.  Set the Root Password for the ESXi
    3.  Configure IP Settings for the ESXi host using the DCUI.
    4.  Configure DNS Settings for the ESXi host from the DCUI.

