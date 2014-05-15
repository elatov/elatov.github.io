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
I decided to expand on the following VMware blog: <a href="http://blogs.vmware.com/kb/2011/05/how-to-enable-nfs-on-windows-2008-and-present-to-esx.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/kb/2011/05/how-to-enable-nfs-on-windows-2008-and-present-to-esx.html']);">How to Enable NFS on Windows 2008 and Present to ESX</a>. The same warning applies to this post as well:

> **Warning:** Windows Services for UNIX is not a supported storage solution for use with ESX, and the information in this article is provided as-is

### Install NFS Role

#### 1. Start the Server Manager

Start -> Run -> servermanager.msc

#### 2. Choose to add a Role

Actions -> Add Role

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/Add_roles.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/Add_roles.png']);"><img class="alignnone size-full wp-image-1630" title="Add_roles" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/Add_roles.png" alt="Add roles Configure Windows 2008 as NFS share for VMware ESX" width="200" height="176" /></a>

#### 3. Click Next on the "Before you Begin" Screen

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/Before_you_begin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/Before_you_begin.png']);"><img class="alignnone size-full wp-image-1635" title="Before_you_begin" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/Before_you_begin.png" alt="Before you begin Configure Windows 2008 as NFS share for VMware ESX" width="779" height="585" /></a>

#### 4. Select "File Services" Under "Select Server Roles"

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/select_file_server.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/select_file_server.png']);"><img class="alignnone size-full wp-image-1636" title="select_file_server" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/select_file_server.png" alt="select file server Configure Windows 2008 as NFS share for VMware ESX" width="777" height="582" /></a>

#### 5. Click Next on the "File Services" Screen

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/file_services.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/file_services.png']);"><img class="alignnone size-full wp-image-1637" title="file_services" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/file_services.png" alt="file services Configure Windows 2008 as NFS share for VMware ESX" width="778" height="584" /></a>

#### 6. Select "Services For Network File System" under the second "Select Server Roles" screen

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/select_network_file_services.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/select_network_file_services.png']);"><img class="alignnone size-full wp-image-1638" title="select_network_file_services" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/select_network_file_services.png" alt="select network file services Configure Windows 2008 as NFS share for VMware ESX" width="776" height="582" /></a>

#### 7. Click Install on the "Confirm Installation Selections" Screen

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/confirm_installation_selections.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/confirm_installation_selections.png']);"><img class="alignnone size-full wp-image-1639" title="confirm_installation_selections" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/confirm_installation_selections.png" alt="confirm installation selections Configure Windows 2008 as NFS share for VMware ESX" width="777" height="582" /></a>

#### 8. Check out the progress of the install

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_progress.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_progress.png']);"><img class="alignnone size-full wp-image-1640" title="installation_progress" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_progress.png" alt="installation progress Configure Windows 2008 as NFS share for VMware ESX" width="780" height="580" /></a>

#### 9. Click Close under the "Installation results

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_confirmation.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_confirmation.png']);"><img class="alignnone size-full wp-image-1641" title="installation_confirmation" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/installation_confirmation.png" alt="installation confirmation Configure Windows 2008 as NFS share for VMware ESX" width="775" height="582" /></a>

***Make sure the install is successful**

### Edit Local policy to set Everyone's permissions to apply to anonymous users

#### 1. Star the Local Policy Security Console

Start -> Run -> secpol.msc

#### 2. Expand the Local Policies –> Security Options

1.  Expand Local Policies
2.  Click on Security Options
3.  Scroll down to "Network Access: Let Everyone permissions apply to anonymous users"

#### <a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/local_policy_settings.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/local_policy_settings.jpg']);"><img class="alignnone size-full wp-image-1648" title="local_policy_settings" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/local_policy_settings.jpg" alt="local policy settings Configure Windows 2008 as NFS share for VMware ESX" width="800" height="572" /></a>

#### 3. Enable "Let Everyone permissions apply to anonymous users"

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/enable_everyone_permission.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/enable_everyone_permission.jpg']);"><img class="alignnone size-full wp-image-1649" title="enable_everyone_permission" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/enable_everyone_permission-e1338184606868.jpg" alt="enable everyone permission e1338184606868 Configure Windows 2008 as NFS share for VMware ESX" width="419" height="495" /></a>

### Create A folder to Share with NFS

#### 1. Create a folder

In our example I created a folder called "nfs_share"

#### 2. Edit "NFS Sharing" settings of the Folder

1.  Right Click on the folder and select Properties
2.  Click on the "NFS Sharing" Tab

#### 

#### <a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_folder.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_folder.jpg']);"><img class="alignnone size-full wp-image-1650" title="properties_of_folder" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_folder-e1338184317604.jpg" alt="properties of folder e1338184317604 Configure Windows 2008 as NFS share for VMware ESX" width="364" height="491" /></a>

#### 3.  Click "Manage NFS Sharing" of the Folder

1.  Check "Share This Folder"
2.  Check "Allow Anonymous Access"
3.  Set the Anonymous UID and GUI to '0'

#### 

#### <a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_sharing_properties.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_sharing_properties.jpg']);"><img class="alignnone size-full wp-image-1653" title="nfs_sharing_properties" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_sharing_properties-e1338184408866.jpg" alt="nfs sharing properties e1338184408866 Configure Windows 2008 as NFS share for VMware ESX" width="353" height="325" /></a>

#### 4. Click Permissions From the "NFS Advanced Sharing" Window

1.  Set the "Type of Access" to "Read/Write"
2.  Check "Allow root access"

#### 

#### <a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_share_persmissions.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_share_persmissions.jpg']);"><img class="alignnone size-full wp-image-1654" title="nfs_share_persmissions" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_share_persmissions-e1338184515249.jpg" alt="nfs share persmissions e1338184515249 Configure Windows 2008 as NFS share for VMware ESX" width="444" height="352" /></a>

#### 5. Click OK to apply the settings

### Allow "Everyone" full Control of the Folder

#### 1. Edit Security Settings of the Folder

Right Click on the folder and Select Properties

#### 2. Select the Security Tab of the Properties

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/Security_tab_folder-e1338183872576.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/Security_tab_folder-e1338183872576.jpg']);"><img class="alignnone size-full wp-image-1655" title="Security_tab_folder" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/Security_tab_folder-e1338183872576.jpg" alt="Security tab folder e1338183872576 Configure Windows 2008 as NFS share for VMware ESX" width="360" height="488" /></a>

#### 3. Click "Edit" on the Security Tab

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/edit_permissions_of_folder-e1338184001726.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/edit_permissions_of_folder-e1338184001726.jpg']);"><img class="alignnone size-full wp-image-1656" title="edit_permissions_of_folder" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/edit_permissions_of_folder-e1338184001726.jpg" alt="edit permissions of folder e1338184001726 Configure Windows 2008 as NFS share for VMware ESX" width="363" height="441" /></a>

#### 4. Click "Add" to add a new User

Type "Everyone" in the object Names and select "Check Names

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/Everyone_User.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/Everyone_User.jpg']);"><img class="alignnone size-full wp-image-1657" title="Everyone_User" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/Everyone_User-e1338182928954.jpg" alt="Everyone User e1338182928954 Configure Windows 2008 as NFS share for VMware ESX" width="462" height="245" /></a>

#### 6. Allow Full Control to Everyone

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/allow_full_control_to_everyone.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/allow_full_control_to_everyone.jpg']);"><img class="alignnone size-full wp-image-1658" title="allow_full_control_to_everyone" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/allow_full_control_to_everyone-e1338183007786.jpg" alt="allow full control to everyone e1338183007786 Configure Windows 2008 as NFS share for VMware ESX" width="359" height="435" /></a>

### Set the NFS server to be TCP Only

#### 1. Start the NFS Management Console

Start -> Run -> nfsmgmt.msc

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_mgmt_console.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_mgmt_console.jpg']);"><img class="alignnone size-full wp-image-1659" title="nfs_mgmt_console" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_mgmt_console.jpg" alt="nfs mgmt console Configure Windows 2008 as NFS share for VMware ESX" width="683" height="404" /></a>

#### 2. Edit Settings of the NFS Server

Right Click on "Server for NFS" and click properties

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_nfs_server.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_nfs_server.png']);"><img class="alignnone size-full wp-image-1660" title="properties_of_nfs_server" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/properties_of_nfs_server.png" alt="properties of nfs server Configure Windows 2008 as NFS share for VMware ESX" width="677" height="397" /></a>

#### 3. Change the Transport Protocol to be "TCP"

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_tcp_only.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_tcp_only.jpg']);"><img class="alignnone size-full wp-image-1661" title="nfs_tcp_only" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/nfs_tcp_only-e1338183626137.jpg" alt="nfs tcp only e1338183626137 Configure Windows 2008 as NFS share for VMware ESX" width="405" height="464" /></a>

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
	

