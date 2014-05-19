---
title: Configure Windows 2008 as NFS share for VMware ESX
author: Karim Elatov
layout: post
permalink: /2012/06/configure-windows-2008-nfs-share-vmware-esx/
dsq_thread_id:
  - 1406492503
categories:
  - Home Lab
  - Storage
  - VMware
tags:
  - Anonymous
  - nfs
  - Server Roles
  - Windows 2008 R2
  - Windows 2008 R2 NFS Server
---
I decided to expand on the following VMware blog: [How to Enable NFS on Windows 2008 and Present to ESX](http://blogs.vmware.com/kb/2011/05/how-to-enable-nfs-on-windows-2008-and-present-to-esx.html). The same warning applies to this post as well:

> **Warning:** Windows Services for UNIX is not a supported storage solution for use with ESX, and the information in this article is provided as-is

### Install NFS Role

#### 1. Start the Server Manager

Start -> Run -> servermanager.msc

#### 2. Choose to add a Role

Actions -> Add Role

![Add_roles](http://virtuallyhyper.com/wp-content/uploads/2012/05/Add_roles.png)

#### 3. Click Next on the "Before you Begin" Screen

![Before_you_begin](http://virtuallyhyper.com/wp-content/uploads/2012/05/Before_you_begin.png)

#### 4. Select "File Services" Under "Select Server Roles"

![select_file_server](http://virtuallyhyper.com/wp-content/uploads/2012/05/select_file_server.png)

#### 5. Click Next on the "File Services" Screen

![file_services](http://virtuallyhyper.com/wp-content/uploads/2012/05/file_services.png)

#### 6. Select "Services For Network File System" under the second "Select Server Roles" screen

![select_network_file_services](http://virtuallyhyper.com/wp-content/uploads/2012/05/select_network_file_services.png)

#### 7. Click Install on the "Confirm Installation Selections" Screen

![confirm_installation_selections](http://virtuallyhyper.com/wp-content/uploads/2012/05/confirm_installation_selections.png)

#### 8. Check out the progress of the install

![installation_progress](http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_progress.png)

#### 9. Click Close under the "Installation results

![installation_confirmation](http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_confirmation.png)

***Make sure the install is successful**

### Edit Local policy to set Everyone's permissions to apply to anonymous users

#### 1. Star the Local Policy Security Console

Start -> Run -> secpol.msc

#### 2. Expand the Local Policies –> Security Options

1.  Expand Local Policies
2.  Click on Security Options
3.  Scroll down to "Network Access: Let Everyone permissions apply to anonymous users"

#### ![local_policy_settings](http://virtuallyhyper.com/wp-content/uploads/2012/05/local_policy_settings.jpg)

#### 3. Enable "Let Everyone permissions apply to anonymous users"

![enable_everyone_permission](http://virtuallyhyper.com/wp-content/uploads/2012/05/enable_everyone_permission-e1338184606868.jpg)

### Create A folder to Share with NFS

#### 1. Create a folder

In our example I created a folder called "nfs_share"

#### 2. Edit "NFS Sharing" settings of the Folder

1.  Right Click on the folder and select Properties
2.  Click on the "NFS Sharing" Tab

####

#### ![properties_of_folder](http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_folder-e1338184317604.jpg)

#### 3.  Click "Manage NFS Sharing" of the Folder

1.  Check "Share This Folder"
2.  Check "Allow Anonymous Access"
3.  Set the Anonymous UID and GUI to '0'

####

#### ![nfs_sharing_properties](http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_sharing_properties-e1338184408866.jpg)

#### 4. Click Permissions From the "NFS Advanced Sharing" Window

1.  Set the "Type of Access" to "Read/Write"
2.  Check "Allow root access"

####

#### ![nfs_share_persmissions](http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_share_persmissions-e1338184515249.jpg)

#### 5. Click OK to apply the settings

### Allow "Everyone" full Control of the Folder

#### 1. Edit Security Settings of the Folder

Right Click on the folder and Select Properties

#### 2. Select the Security Tab of the Properties

![Security_tab_folder](http://virtuallyhyper.com/wp-content/uploads/2012/05/Security_tab_folder-e1338183872576.jpg)

#### 3. Click "Edit" on the Security Tab

![edit_permissions_of_folder](http://virtuallyhyper.com/wp-content/uploads/2012/05/edit_permissions_of_folder-e1338184001726.jpg)

#### 4. Click "Add" to add a new User

Type "Everyone" in the object Names and select "Check Names

![Everyone_User](http://virtuallyhyper.com/wp-content/uploads/2012/05/Everyone_User-e1338182928954.jpg)

#### 6. Allow Full Control to Everyone

![allow_full_control_to_everyone](http://virtuallyhyper.com/wp-content/uploads/2012/05/allow_full_control_to_everyone-e1338183007786.jpg)

### Set the NFS server to be TCP Only

#### 1. Start the NFS Management Console

Start -> Run -> nfsmgmt.msc

![nfs_mgmt_console](http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_mgmt_console.jpg)

#### 2. Edit Settings of the NFS Server

Right Click on "Server for NFS" and click properties

![properties_of_nfs_server](http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_nfs_server.png)

#### 3. Change the Transport Protocol to be "TCP"

![nfs_tcp_only](http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_tcp_only-e1338183626137.jpg)

#### 4. Restart the NFS Server

1.  Right Click on "Server for NFS" and click on "Stop Service"
2.  Right Click on "Server for NFS" and Click on "Start Service"

### Add the NFS Export to the ESX host

#### 1. SSH to the host

Use putty or any ssh client of your choice

#### 2. Add the NFS mount


	~ # esxcfg-nas -a -o 10.131.9.153 -s /nfs_share Win2k8_Share
	Connecting to NAS volume: Win2k8_Share
	Win2k8_Share created and connected.


#### 3. Ensure newly created files are owned by root


	~ # cd /vmfs/volumes/Win2k8_Share/
	/vmfs/volumes/17212d56-03dc308d # ls
	/vmfs/volumes/17212d56-03dc308d # mkdir test
	/vmfs/volumes/17212d56-03dc308d # ls -l
	drwxr-xr-x 1 root root 64 May 28 04:11 test


