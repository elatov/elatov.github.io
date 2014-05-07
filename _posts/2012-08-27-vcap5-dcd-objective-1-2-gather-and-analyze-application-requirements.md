---
title: VCAP5-DCD Objective 1.2 – Gather and analyze application requirements
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-1-2-gather-and-analyze-application-requirements/
dsq_thread_id:
  - 1410480912
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Given a scenario, gather and analyze application requirements From the

<a href="http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.slideshare.net/ProfessionalVMware/professionalvmware-brownbag-jason-boche-vcapdcd-objective-1']);">US BrownBag Objective 1 slide deck</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/current-state-analysis.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/current-state-analysis.png']);"><img class="alignnone size-full wp-image-2712" title="current-state-analysis" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/current-state-analysis.png" alt="current state analysis VCAP5 DCD Objective 1.2 – Gather and analyze application requirements " width="1100" height="788" /></a>

### Given a set of applications within a physical environment, determine the requirements for virtualization

This is very application specific. Here are some example from <a href="http://www.seancrookston.com/blog/2011/02/08/vcap-dcd-objective-1-2-gather-and-analyze-application-requirements/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.seancrookston.com/blog/2011/02/08/vcap-dcd-objective-1-2-gather-and-analyze-application-requirements/']);">this</a> blog:

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

From <a href="http://www.virtualnetworkdesign.com/vcap5-dcd-study-guide/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virtualnetworkdesign.com/vcap5-dcd-study-guide/']);">this</a> blog, we can see that should be done during the Current-State Analysis:

> **Current-State Analysis**
> 
> *   Due Diligence, Inventory (Phys & Virt), Process Mapping, Application Mapping. 
> *   Use tools to automate: Capacity Planner, ESXTOP, Platespin,vFoglight, vCOPS 
> *   Ensure current capacity and workload is collected. Peak / Offpeak, EOM, EOFY 
> *   Can be tricky working with past information, especially identifying bottlenecks. 
> *   Have at least 1 month of data to analyse. Ensures capture of peak loads.

### Given one or more application requirements, determine the impact of the requirements on the design

This again is very application specific. Just plan ahead and determine what is necessary for an application. Here is a very easy example, if you are using Microsoft Clustering Services, then you know you will need dedicated RDMs, which mean you need to plan accordingly to allocate more LUNs. This way other VMs can have to other LUNs as necessary. Different application have certain RAM prerequisites, plan ahead and make sure you don&#8217;t over commit your CPU or Memory. Here are some links from the VCAP-DCD Blueprint to application specific requirements:

*   <a href="http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJTz&pc=orcl&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJTz&pc=orcl&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=']);">VMware Virtualizing Oracle Kit</a>
*   <a href="http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUJ&pc=exch&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUJ&pc=exch&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=']);">VMware Virtualizing Exchange Kit</a>
*   <a href="http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUY&pc=sql&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUY&pc=sql&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=']);">VMware Virtualizing SQL Kit</a>
*   <a href="http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUT&pc=sap&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUT&pc=sap&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=']);">VMware Virtualizing SAP Kit</a>
*   <a href="http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUd&pc=java&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://info.vmware.com/content/12581_VirtApps_reg?cid=70180000000wJUd&pc=java&src=APPS-WEB-SOLN&elq=URLPage=139&xyz=']);">VMware Virtualizing Enterprise Java Kit</a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/vcap5-dcd-objective-1-2-gather-and-analyze-application-requirements/" title=" VCAP5-DCD Objective 1.2 – Gather and analyze application requirements" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCD,blog;button:compact;">Given a scenario, gather and analyze application requirements From the US BrownBag Objective 1 slide deck: Given a set of applications within a physical environment, determine the requirements for virtualization...</a>
</p>