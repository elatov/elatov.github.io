---
title: VCAP5-DCD Objective 1.1 – Gather and analyze business requirements
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-1-1-gather-and-analyze-business-requirements/
dsq_thread_id:
  - 1406205090
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['business_requirements']
---

### Associate a stakeholder with the information that needs to be collected.

From the ![stake-holders](https://github.com/elatov/uploads/raw/master/2012/08/stake-holders.png)

From [this](http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/) blog:

> **Project participants (SMEs / Key Stakeholders)**
> A design project manager has to determine a list of SMEs and project stakeholders who can provide information about the design requirements. This list typically includes:
>
> *   Network administrators
> *   Storage administrators
> *   Server hardware administrators
> *   Operating system administrators
> *   Application administrators
> *   Security Officer
> *   HR representatives
> *   C-Level executives (CEO, CTO, CIO,…)
> *   Representatives
>
> It is important to lists the people involved in this project and their contact information. This list should include:
>
> *   Name
> *   Title
> *   Organisation
> *   E-Mail address
> *   Phone number
> *   Reachability
>
> Having contact information available will help to make progress without unnecessary interruption during the design process.
>
> *   Stakeholder = A person with an interest in a project
> *   SME = A subject-matter expert is a person who is an expert in a particular area

### Utilize customer inventory and assessment data from a current environment to define a baseline state.

From the [US BrownBag for Objective 1](http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1) slide deck:

![5-step-design-process](https://github.com/elatov/uploads/raw/master/2012/08/5-step-design-process.png)

### Analyze customer interview data to explicitly define customer objectives for a conceptual design.

From this [blog's notes](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf), I decided to write them out just to make it easier to read:

> **Conceptual Design: Focus on achieving goals and requirements**
>
> *   Use information from SME/Stakeholder interviews (Scope/Goals/Requirements/assumptions/constraints) and from information gathered in current state analysis
> *   Determine entities affected by project (LOB,users,applications, processes, physical machine, etc)
> *   Determine how goals map to each entity
> *   Design infrastructure that achieves each entity's goal and requirements but stay within constraints (i.e. where do you need availability, scalability, performance,security and manageability
> *   Document with diagrams, tables, and text

From the same [pdf](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf), here is an example of a conceptual diagram:

![conceptual_diag1](https://github.com/elatov/uploads/raw/master/2012/08/conceptual_diag1.png)

### Identify the need for and apply requirements tracking.

From [this](http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/) blog:

> **Requirement tracking**
> It is important to document all requirements. This could be done in an excel sheet for example. Every single requirement should contain at least a unique number, desciption, timestap, priority and the originator.

### Given results of a requirements gathering survey, identify requirements for a conceptual design.

From the above pdf again:

> **Architectural Analysis: Deeper Dive into current infrastucture**
> Perform 2 activities
>
> 1.  Current State Analysis:
>     *   Gather and analyze information on current servers,storage,network
>     *   Gather and analyze application and operating system
>     *   Gather resource consumption data
> 2.  Envision target state required to meet organizational goals while factoring in requirements, assumptions, and constraints.

Generate a similar conceptual diagram as above. Here is a conceptual diagram from [this](http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/) blog:

![another-conceptual-diag](https://github.com/elatov/uploads/raw/master/2012/08/another-conceptual-diag.png)

### Categorize requirements by infrastructure qualities to prepare for logical design requirements.

From the [PDF](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) again:

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

Here is an example of a logical diagram taken from the pdf:

![logical-diagram](https://github.com/elatov/uploads/raw/master/2012/08/logical-diagram.png)

I would also suggest to watch the following recordings as well:

*   [APAC VCAP5-DCD BrownBag Session 1](https://professionalvmware.com/vmware-certifications/)
*   [US VCAP5-DCD BrownBag Objective 1](https://professionalvmware.com/vmware-certifications/)

