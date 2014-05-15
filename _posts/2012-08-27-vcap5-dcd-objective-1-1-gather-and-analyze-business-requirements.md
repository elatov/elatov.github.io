---
title: VCAP5-DCD Objective 1.1 – Gather and analyze business requirements
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-1-1-gather-and-analyze-business-requirements/
dsq_thread_id:
  - 1406205090
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Associate a stakeholder with the information that needs to be collected.

From the <a href="http://portal.sliderocket.com/BLIHZ/VCAP5-DCD-BrownBag---Session-1" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://portal.sliderocket.com/BLIHZ/VCAP5-DCD-BrownBag---Session-1']);">APAC BrownBag Session 1 Slide Deck</a>: <a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/stake-holders.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/stake-holders.png']);"><img class="alignnone  wp-image-2688" title="stake-holders" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/stake-holders.png" alt="stake holders VCAP5 DCD Objective 1.1 – Gather and analyze business requirements" width="814" height="504" /></a>

From <a href="http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/']);">this</a> blog:

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

From the <a href="http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1']);">US BrownBag for Objective 1</a> slide deck:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/5-step-design-process.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/5-step-design-process.png']);"><img class="alignnone size-full wp-image-2690" title="5-step-design-process" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/5-step-design-process.png" alt="5 step design process VCAP5 DCD Objective 1.1 – Gather and analyze business requirements" width="1125" height="794" /></a>

### Analyze customer interview data to explicitly define customer objectives for a conceptual design.

From this <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">blog's notes</a>, I decided to write them out just to make it easier to read:

> **Conceptual Design: Focus on achieving goals and requirements**
> 
> *   Use information from SME/Stakeholder interviews (Scope/Goals/Requirements/assumptions/constraints) and from information gathered in current state analysis
> *   Determine entities affected by project (LOB,users,applications, processes, physical machine, etc)
> *   Determine how goals map to each entity
> *   Design infrastructure that achieves each entity's goal and requirements but stay within constraints (i.e. where do you need availability, scalability, performance,security and manageability
> *   Document with diagrams, tables, and text 

From the same <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">pdf</a>, here is an example of a conceptual diagram:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/conceptual_diag1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/conceptual_diag1.png']);"><img class="alignnone size-full wp-image-2697" title="conceptual_diag1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/conceptual_diag1.png" alt="conceptual diag1 VCAP5 DCD Objective 1.1 – Gather and analyze business requirements" width="1074" height="399" /></a>

### Identify the need for and apply requirements tracking.

From <a href="http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/']);">this</a> blog:

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

Generate a similar conceptual diagram as above. Here is a conceptual diagram from <a href="http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/05/vdcd510-objective-1-1-gather-and-analyze-business-requirements/']);">this</a> blog:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/another-conceptual-diag.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/another-conceptual-diag.png']);"><img class="alignnone size-full wp-image-2698" title="another-conceptual-diag" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/another-conceptual-diag.png" alt="another conceptual diag VCAP5 DCD Objective 1.1 – Gather and analyze business requirements" width="592" height="277" /></a>

### Categorize requirements by infrastructure qualities to prepare for logical design requirements.

From the <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">PDF</a> again:

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

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png']);"><img class="alignnone size-full wp-image-2702" title="logical-diagram" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/logical-diagram.png" alt="logical diagram VCAP5 DCD Objective 1.1 – Gather and analyze business requirements" width="948" height="496" /></a>

I would also suggest to watch the following recordings as well:

*   <a href="http://professionalvmware.com/2012/02/apac-brownbag-follow-up-vcap-dcd-study-group/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://professionalvmware.com/2012/02/apac-brownbag-follow-up-vcap-dcd-study-group/']);">APAC VCAP5-DCD BrownBag Session 1</a>
*   <a href="http://professionalvmware.com/2011/09/brownbag-follow-up-vcap-dcd-objective-1-jason-boche/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://professionalvmware.com/2011/09/brownbag-follow-up-vcap-dcd-objective-1-jason-boche/']);">US VCAP5-DCD BrownBag Objective 1</a>

