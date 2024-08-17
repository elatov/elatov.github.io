---
title: VCAP5-DCA Objective 5.1 – Implement and Maintain Host Profiles
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-5-1-implement-and-maintain-host-profiles/
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['host_profile']
---

### Use Profile Editor to edit and/or disable policies

From "[vSphere Host Profiles ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vsphere-esxi-vcenter-server-703-host-profiles-guide.pdf)":

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

![host_profile_view](https://github.com/elatov/uploads/raw/master/2012/11/host_profile_view.png)

To edit a host profile we have to create one first. From the same document:

> **Creating a Host Profile**
> You create a new host profile by using the designated reference host's configuration.
> A host profile can be created from:
>
> *   Host Profile main view
> *   host's context menu
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

Here is the process as it's seen in vCenter:

![create_hp_step1](https://github.com/elatov/uploads/raw/master/2012/11/create_hp_step1.png)

then select a host from which you want to create a profile from:

![create_hp_step2](https://github.com/elatov/uploads/raw/master/2012/11/create_hp_step2.png)

Then name your host profile:

![create_hp_step3](https://github.com/elatov/uploads/raw/master/2012/11/create_hp_step3.png)

After that click "Finish" and then you will have a profile under the Host Profile view, like so:

![create_hp](https://github.com/elatov/uploads/raw/master/2012/11/create_hp.png)

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

![edit_host_profile](https://github.com/elatov/uploads/raw/master/2012/11/edit_host_profile.png)

### Create sub-profiles

From "[vSphere Host Profiles ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vsphere-esxi-vcenter-server-703-host-profiles-guide.pdf)":

> **Edit a Policy**
> A policy describes how a specific configuration setting should be applied. The Profile Editor allows you to edit policies belonging to a specific host profile.
>
> On the left side of the Profile Editor, you can expand the host profile. Each host profile is composed of several subprofiles that are designated by functional group to represent configuration instances. Each subprofile contains many policies and compliance checks that describe the configuration that is relevant to the profile.You can configure certain subprofiles, example policies, and compliance checks.
>
> Each policy consists of one or more options that contains one or more parameters. Each parameter consists of a key and a value. The value can be one of a few basic types, for example integer, string, string array, or integer array
>
> ![hp_subprofiles](https://github.com/elatov/uploads/raw/master/2012/11/hp_subprofiles.png)

### Use Host Profiles to deploy vDS

From "[VMware Host Profiles: Technical Overview](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmw-host-profiles-tech-overview-white-paper.pdf)":

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

Expand the "Storage Configuration" under the profile section and change whatever setting necessary. Here are some of the available settings from the vCenter:

![hp-storage_conf](https://github.com/elatov/uploads/raw/master/2012/11/hp-storage_conf.png)

### Manage Answer Files

From "[vSphere Host Profiles ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vsphere-esxi-vcenter-server-703-host-profiles-guide.pdf)":

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

![answer file options VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles](https://github.com/elatov/uploads/raw/master/2012/11/answer_file_options.png)

Also here is how editing the answer file looks like, by selecting "Update Answer File", from vCenter:

![update answer files VCAP5 DCA Objective 5.1 – Implement and Maintain Host Profiles](https://github.com/elatov/uploads/raw/master/2012/11/update_answer_files.png)

