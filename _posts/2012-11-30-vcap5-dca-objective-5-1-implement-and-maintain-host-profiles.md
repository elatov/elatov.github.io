---
title: VCAP5-DCA Objective 5.1 – Implement and Maintain Host Profiles
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-5-1-implement-and-maintain-host-profiles/
dsq_thread_id:
  - 1409208979
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Use Profile Editor to edit and/or disable policies

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf']);">vSphere Host Profiles ESXi 5.0</a>&#8220;:

> **Access Host Profiles View**  
> The Host Profiles main view lists all available profiles. Administrators can also use the Host Profiles main view to perform operations on host profiles and configure profiles.
> 
> The Host Profiles main view should be used by experienced administrators who wish to perform host profile operations and configure advanced options and policies. Most operations such as creating new profiles, attaching entities, and applying profiles can be performed from the Hosts and Clusters view.
> 
> **Procedure**
> 
> *   Select View > Management > Host Profiles.
> 
> Any existing profiles are listed on the left side in the profiles list. When a profile is selected from the profile list, the details of that profile are displayed on the right side.

Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/host_profile_view.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/host_profile_view.png']);"><img class="alignnone size-full wp-image-5055" title="host_profile_view" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/host_profile_view.png" alt="host profile view VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="1041" height="570" /></a>

To edit a host profile we have to create one first. From the same document:

> **Creating a Host Profile**  
> You create a new host profile by using the designated reference host&#8217;s configuration.  
> A host profile can be created from:
> 
> *   Host Profile main view
> *   host&#8217;s context menu
> 
> **Create a Host Profile from Host Profiles View**  
> You can create a host profile from the Host Profiles main view using the configuration of an existing host.  
> **Prerequisites**  
> You must have a vSphere installation and at least one properly configured host in the inventory.  
> **Procedure**
> 
> 1.  In the Host Profiles main view, click Create Profile.  
>     The Create Profile wizard appears.
> 2.  Select the option to create a new profile and click Next.
> 3.  Select the host you want to designate as the reference host for the new host profile and click Next.  
>     The reference host must be a valid host.
> 4.  Type the name and enter a description for the new profile and click Next.
> 5.  Review the summary information for the new profile and click Finish to complete creating the profile.
> 
> The new profile appears in the profile list.

Here is the process as it&#8217;s seen in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step1.png']);"><img class="alignnone size-full wp-image-5057" title="create_hp_step1" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step1.png" alt="create hp step1 VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="700" height="513" /></a>

then select a host from which you want to create a profile from:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step2.png']);"><img class="alignnone size-full wp-image-5058" title="create_hp_step2" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step2.png" alt="create hp step2 VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="698" height="513" /></a>

Then name your host profile:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step3.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step3.png']);"><img class="alignnone size-full wp-image-5059" title="create_hp_step3" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp_step3.png" alt="create hp step3 VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="701" height="516" /></a>

After that click &#8220;Finish&#8221; and then you will have a profile under the Host Profile view, like so:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp.png']);"><img class="alignnone size-full wp-image-5060" title="create_hp" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/create_hp.png" alt="create hp VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="542" height="127" /></a>

Now From the VMware documentation:

> **Edit a Host Profile**  
> You can view and edit host profile policies, select a policy to be checked for compliance, and change the policy name or description.  
> **Procedure**
> 
> 1.  In the Host Profiles main view, select the profile to edit from the profile list.
> 2.  Click Edit Host Profile.
> 3.  (Optional) Change the profile name or description in the fields at the top of the Profile Editor.
> 4.  Edit the policy.
> 5.  (Optional) Enable or disable the policy compliance check.
> 6.  Click OK to close the Profile Editor.

Here is how editing of the Host Profile looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/edit_host_profile.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/edit_host_profile.png']);"><img class="alignnone size-full wp-image-5061" title="edit_host_profile" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/edit_host_profile.png" alt="edit host profile VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="993" height="543" /></a>

### Create sub-profiles

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf']);">vSphere Host Profiles ESXi 5.0</a>&#8220;:

> **Edit a Policy**  
> A policy describes how a specific configuration setting should be applied. The Profile Editor allows you to edit policies belonging to a specific host profile.
> 
> On the left side of the Profile Editor, you can expand the host profile. Each host profile is composed of several subprofiles that are designated by functional group to represent configuration instances. Each subprofile contains many policies and compliance checks that describe the configuration that is relevant to the profile.You can configure certain subprofiles, example policies, and compliance checks.
> 
> Each policy consists of one or more options that contains one or more parameters. Each parameter consists of a key and a value. The value can be one of a few basic types, for example integer, string, string array, or integer array
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/hp_subprofiles.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/hp_subprofiles.png']);"><img class="alignnone size-full wp-image-5063" title="hp_subprofiles" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/hp_subprofiles.png" alt="hp subprofiles VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="591" height="768" /></a>

### Use Host Profiles to deploy vDS

From &#8220;<a href="http://www.vmware.com/files/pdf/techpaper/VMW-Host-Profiles-Tech-Overview.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/VMW-Host-Profiles-Tech-Overview.pdf']);">VMware Host Profiles: Technical Overview</a>&#8220;:

> **Use Case 5: Using Host Profiles to Configure Hosts to Use VMware vNetwork Distributed Switch**  
> Host Profiles can be used to capture the vNetwork Standard Switch (vSS) and vNetwork Distributed Switch configuration of a VMware ESX host, and then apply and propagate that configuration to a number of other VMware ESX or ESXi hosts.
> 
> Host Profiles is the preferred and easiest method for deploying a Distributed Switch across a large population of hosts. The following use case assumes that you are starting with a population of hosts, each with a single Standard Switch.
> 
> Migrate reference host to Distributed Switch.
> 
> 1.  Create Distributed Switch (without any associated hosts).
> 2.  Create Distributed Virtual Port Groups on Distributed Switch to match existing or required environment.
> 3.  Add host to Distributed Switch and migrate vmnics to dvUplinks and Virtual Ports to DV Port Groups.
> 4.  Delete Standard Switch from host.  
>     At the completion of Step 4, we will have a single host with its networking environment completely migrated to Distributed Switch. The following three steps allow us to create a host profile of this migrated host and then apply it to a number of hosts in one step (Step 7).
> 5.  Create host profile of Reference Host.
> 6.  Attach and apply the host profile to the candidate hosts.
> 7.  Migrate virtual machine networking for virtual machines and take the hosts out of Maintenance Mode.
> 
> Variation on Using Host Profiles for Migration  
> The previously outlined process can be time consuming for a large number of virtual machines. An alternative method, which reduces the per–virtual machine edit process but requires a reapplication of a modified host profile, is as follows:
> 
> 1.  Retain the Standard Switch on each host (and, therefore, the Port Groups) during migration, using Host Profiles. Do not perform Step 4 (so you create a host profile of a host with a Standard Switch and a Distributed Switch and then apply that profile to the hosts).
> 2.  Right-click on the Distributed Switch and select Migrate Virtual Machine Networking… and then migrate all virtual machines for each Port Group in one step per Port Group.
> 3.  Delete the Standard Switch from the host profile using the edit host profile function (or just delete the Standard Switch from the reference host and create a fresh host profile).
> 4.  Reapply this host profile to the hosts in the cluster.

### Use Host Profiles to deploy vStorage policies

Expand the &#8220;Storage Configuration&#8221; under the profile section and change whatever setting necessary. Here are some of the available settings from the vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/hp-storage_conf.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/hp-storage_conf.png']);"><img class="alignnone size-full wp-image-5065" title="hp-storage_conf" src="http://virtuallyhyper.com/wp-content/uploads/2012/11/hp-storage_conf.png" alt="hp storage conf VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" width="328" height="271" /></a>

### Manage Answer Files

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-host-profiles-guide.pdf']);">vSphere Host Profiles ESXi 5.0</a>&#8220;:

> To apply a host profile to a host, the host must be placed into maintenance mode. During this process, the user is prompted to type answers for policies that are specified during host profile creation.
> 
> Placing the host into maintenance mode each time you apply a profile to the host can be costly and time consuming. A host provisioned with Auto Deploy can be rebooted while the host profile is attached to the host. After rebooting values stored in the answer file help the host provisioned with Auto Deploy to apply the profile. An answer file is created that contains a series of key value pairs for the user input options.
> 
> **Check Answer File Status**  
> The answer file status indicates the state of the answer file. The status of an answer file can be complete, incomplete, missing, or unknown.  
> **Prerequisites**  
> The answer file status can only be checked when the host profile is attached to a host.  
> **Procedure**
> 
> *   In the host profiles view, click Check Answer File.
> 
> The Answer File Status for the host profile is updated. The status indicates one of the following states:
> 
> *   **Incomplete** The answer file is missing some of the required user input answers.
> *   **Complete** The answer file has all of the user input answers needed.
> *   **Unknown** The host and associated profile exist but the status of the answer file is not known. This is the initial state of an answer file.

More from the same document:

> **Update Answer File**  
> You can update or change the user input parameters for the host profiles policies in the answer file.  
> **Procedure**
> 
> *   Right-click the host entity and select Update Answer File.
> *   When prompted, enter or change the user input parameter, and click Next.
> *   Click Update when finished entering changes.
> 
> **Import Answer File**  
> You can import a previously exported answer file to associate with a host profile.  
> **Prerequisites**  
> The imported answer file must be associated with at least one host.  
> **Procedure**
> 
> *   Right-click the host entity and select Import Answer File.
> *   Select the answer file to import.
> 
> **Export Answer File**  
> You can export an answer file so that it can be imported and used by another host profile.
> 
> The answer file might contain sensitive information such as passwords and IP addresses. If exported, this information is vulnerable to unauthorized access. During the export process all passwords are removed from the answer file. When the answer file is imported, the password information must be re-entered.  
> **Procedure**
> 
> *   Right-click the host entity and select Export Answer File.
> *   Select the location to save the answer file.

Here is how the options for answer file looks like from vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/answer_file_options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/answer_file_options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/answer_file_options.png" alt="answer file options VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" title="answer_file_options" width="1120" height="344" class="alignnone size-full wp-image-5066" /></a>

Also here is how editing the answer file looks like, by selecting &#8220;Update Answer File&#8221;, from vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/update_answer_files.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/update_answer_files.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/update_answer_files.png" alt="update answer files VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles" title="update_answer_files" width="995" height="734" class="alignnone size-full wp-image-5067" /></a>

