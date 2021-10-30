---
title: VCAP5-DCD Objective 1.2 – Gather and analyze application requirements
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-1-2-gather-and-analyze-application-requirements/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['application_requirements']
---

### Given a scenario, gather and analyze application requirements From the

[US BrownBag Objective 1 slide deck](http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1):

![current-state-analysis](https://github.com/elatov/uploads/raw/master/2012/08/current-state-analysis.png)

### Given a set of applications within a physical environment, determine the requirements for virtualization

This is very application specific. Here are some example from [this](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/VCAP_DCD_Objective_1_2_Gather_and_analyze_application_requirements_Sean_Crookston.pdf) blog:

> *   Oracle
>     *   Use Large Memory Pages-again there are implications of making design decision like this. In the case of using large memory pages you must be aware that this will hinder the use of Transparent Page Sharing for the VMs memory.
>     *   Use Oracle Automatic Storage Management
>     *   Set Memory Reservations equal to size of Oracle SGA
> *   Exchange
>     *   RDMs can be used as a migration strategy from a physical to virtual world.
>     *   Use the Microsoft Exchanges Service Profile Analyzer to estimate workloads.
> *   SQL
>     *   Use Large Memory Pages

### Gather information needed in order to identify application dependencies.

From an old and discontinued blog, we can see that should be done during the Current-State Analysis:

> **Current-State Analysis**
>
> *   Due Diligence, Inventory (Phys & Virt), Process Mapping, Application Mapping.
> *   Use tools to automate: Capacity Planner, ESXTOP, Platespin,vFoglight, vCOPS
> *   Ensure current capacity and workload is collected. Peak / Offpeak, EOM, EOFY
> *   Can be tricky working with past information, especially identifying bottlenecks.
> *   Have at least 1 month of data to analyse. Ensures capture of peak loads.

### Given one or more application requirements, determine the impact of the requirements on the design

This again is very application specific. Just plan ahead and determine what is necessary for an application. Here is a very easy example, if you are using Microsoft Clustering Services, then you know you will need dedicated RDMs, which mean you need to plan accordingly to allocate more LUNs. This way other VMs can have to other LUNs as necessary. Different application have certain RAM prerequisites, plan ahead and make sure you don't over commit your CPU or Memory. Here are some links from the VCAP-DCD Blueprint to application specific requirements:

*   [VMware Virtualizing Oracle Kit](http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJTz&pc=orcl&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=)
*   [VMware Virtualizing Exchange Kit](http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUJ&pc=exch&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=)
*   [VMware Virtualizing SQL Kit](http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUY&pc=sql&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=)
*   [VMware Virtualizing SAP Kit](http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUT&pc=sap&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=)
*   [VMware Virtualizing Enterprise Java Kit](http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUd&pc=java&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=)

