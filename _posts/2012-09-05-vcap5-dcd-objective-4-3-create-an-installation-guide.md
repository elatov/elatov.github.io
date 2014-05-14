---
title: VCAP5-DCD Objective 4.3 – Create an Installation Guide
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-4-3-create-an-installation-guide/
dsq_thread_id:
  - 1404931043
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Identify standard resources required to construct an installation guide

If you are within an organization which has pre-made templates for this, then definitely check them out. Other than that, VMware provides a lot of evaluation guides which has a step by step process of how to install certain VMware products. Here are a few:

*   <a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-1.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-1.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume One</a>
*   <a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-2-Advanced-Storage.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-2-Advanced-Storage.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Two – Advanced Storage Features</a>
*   <a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-3-Advanced-Networking.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-3-Advanced-Networking.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Three – Advanced Networking Features</a>
*   <a href="http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/vsphere/VMware-vSphere-Evaluation-Guide-4-Auto-Deploy.pdf']);">VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy</a>
*   <a href="http://www.vmware.com/files/pdf/techpaper/VMW-vCloud-Director1_5-EvalGuide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/VMW-vCloud-Director1_5-EvalGuide.pdf']);">VMware vCloud Director 1.5 Evaluation Guide</a>
*   <a href="http://www.vmware.com/files/pdf/products/DR/VMware-Data-Recovery-Evaluation-Guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/DR/VMware-Data-Recovery-Evaluation-Guide.pdf']);">VMware Data Recovery 2.0 Evaluation Guide</a>
*   <a href="http://www.vmware.com/files/pdf/products/SRM/VMware-vCenter-Site-Recovery-Manager-Evaluation-Guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/products/SRM/VMware-vCenter-Site-Recovery-Manager-Evaluation-Guide.pdf']);">VMware vCenter Site Recovery Manager  5.0 Evaluation Guide</a>

### Consider multiple product installation dependencies to create a validated configuration

Order of installation definitely matters. You can&#8217;t install vCenter without installing a database server first.

### Recognize opportunities to utilize automated procedures to optimize installation

Check out <a href="http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/']);">Objective 3.6</a> on how to setup a scripted install for ESXi.

### Create installation documentation specific to the design

Here is how it would look like:

**Installing the ESXi Host**  
To install an ESXi host

1.  Configure the host server disk boot order to enable boot from CD.
2.  Boot the ESXi Installer from CD to install ESXi.  
    <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/install-esxi-1st.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/install-esxi-1st.png']);"><img class="alignnone size-full wp-image-3394" title="install-esxi-1st" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/install-esxi-1st.png" alt="install esxi 1st VCAP5 DCD Objective 4.3 – Create an Installation Guide " width="720" height="400" /></a>
3.  Press Enter to start the installer.  
    <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi-install-2nd.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi-install-2nd.png']);"><img class="alignnone size-full wp-image-3395" title="esxi-install-2nd" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/esxi-install-2nd.png" alt="esxi install 2nd VCAP5 DCD Objective 4.3 – Create an Installation Guide " width="1024" height="768" /></a>

And the instructions keep going <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile VCAP5 DCD Objective 4.3 – Create an Installation Guide " class="wp-smiley" title="VCAP5 DCD Objective 4.3 – Create an Installation Guide " /> 

