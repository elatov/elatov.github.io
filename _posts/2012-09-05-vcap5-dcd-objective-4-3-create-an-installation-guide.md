---
title: VCAP5-DCD Objective 4.3 – Create an Installation Guide
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-4-3-create-an-installation-guide/
dsq_thread_id:
  - 1404931043
categories: ['certifications','vcap5_dcd', 'vmware']
tags: ['technical_documentation']
---

### Identify standard resources required to construct an installation guide

If you are within an organization which has pre-made templates for this, then definitely check them out. Other than that, VMware provides a lot of evaluation guides which has a step by step process of how to install certain VMware products. Here are a few:

*   [VMware vSphere 5.0 Evaluation Guide Volume One](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-vsphere-evaluation-guide-1-white-paper.pdf)
*   [VMware vSphere 5.0 Evaluation Guide Volume Two – Advanced Storage Features](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/VMware-vSphere-Evaluation-Guide-2-Advanced-Storage.pdf)
*   [VMware vSphere 5.0 Evaluation Guide Volume Three – Advanced Networking Features](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware-vsphere-evaluation-guide-3-advanced-networking-white-paper.pdf)
*   [VMware vSphere 5.0 Evaluation Guide Volume Four – Auto Deploy](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware-vsphere-evaluation-guide-4-auto-deploy-white-paper.pdf)
*   [VMware vCloud Director 1.5 Evaluation Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmw-vcloud-director1_5-evalguide-white-paper.pdf)
*   [VMware Data Protection Evaluation Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-vsphere-data-protection-eval-guide-white-paper.pdf)
*   [VMware vCenter Site Recovery Manager  5.0 Evaluation Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/site_recovery_manager_evaluation_guide_noindex.pdf)

### Consider multiple product installation dependencies to create a validated configuration

Order of installation definitely matters. You can't install vCenter without installing a database server first.

### Recognize opportunities to utilize automated procedures to optimize installation

Check out [Objective 3.6](/2012/09/vcap5-dcd-objective-3-6-determine-datacenter-management-options-for-a-vsphere-5-physical-design/) on how to setup a scripted install for ESXi.

### Create installation documentation specific to the design

Here is how it would look like:

**Installing the ESXi Host**
To install an ESXi host

1.  Configure the host server disk boot order to enable boot from CD.
2.  Boot the ESXi Installer from CD to install ESXi.
    ![install-esxi-1st](https://github.com/elatov/uploads/raw/master/2012/09/install-esxi-1st.png)
3.  Press Enter to start the installer.
    ![esxi-install-2nd](https://github.com/elatov/uploads/raw/master/2012/09/esxi-install-2nd.png)

And the instructions keep going :)

