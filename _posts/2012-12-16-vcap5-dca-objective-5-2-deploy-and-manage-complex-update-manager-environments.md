---
title: VCAP5-DCA Objective 5.2 – Deploy and Manage Complex Update Manager Environments
author: Karim Elatov
layout: post
permalink: /2012/12/vcap5-dca-objective-5-2-deploy-and-manage-complex-update-manager-environments/
dsq_thread_id:
  - 1412406951
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['vum']
---

### Identify firewall access rules for Update Manager

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)", here is table of ports used by update manager:

![vum_net_ports](https://github.com/elatov/uploads/raw/master/2012/12/vum_net_ports.png)

### Install and configure Update Manager Download Service

From "[Reconfiguring VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-651-reconfig-guide.pdf)":

> **Install UMDS and the Update Manager Utility**
> When you install UMDS, the Update Manager Utility is silently installed on your system as an additional component.
> **Prerequisites**
>
> *   Verify that the machine on which you install UMDS has Internet access, so that UMDS can downloadupgrades, patch metadata and patch binaries.
> *   Uninstall UMDS 1.0.x or UMDS 4.x if it is installed on the machine. If such a version of UMDS is already installed, the installation wizard displays an error message and the installation cannot proceed.
> *   Create a database instance and configure it before you install UMDS. When you install UMDS on a 64-bit machine, you must configure a 32-bit DSN and test it from ODBC. The database privileges and preparation steps are the same as the ones used for Update Manager. For more information, see Installing and Administering VMware vSphere Update Manager.
> *   UMDS and Update Manager must be installed on different machines.

Here is more information from the same document:

> **Procedure**
>
> 1.  Insert the VMware vSphere Update Manager installation DVD into the DVD drive of the Windows server that will host UMDS.
> 2.  Browse to the umds folder on the DVD and run VMware-UMDS.exe.
> 3.  Select the language for the installation and click OK.
> 4.  (Optional) If the wizard prompts you, install the required items such as Windows Installer 4.5.
>     This step is required only if Windows Installer 4.5 is not present on your machine and you must perform it the first time you install a vSphere 5.0 product. After the system restarts, the installer launches again.
> 5.  Review the Welcome page and click Next.
> 6.  Read the patent agreement and click Next.
> 7.  Accept the terms in the license agreement and click Next.
> 8.  Select the database options and click Next.
>     *   If you do not have an existing database, select Install a Microsoft SQL Server 2008 R2 Express instance (for small scale deployments).
>     *   If you want to use an existing database, select Use an existing supported database and select your database from the list of DSNs. If the DSN does not use Windows NT authentication, type the user name and password for the DSN and click Next.
> 9.  Specify the Update Manager Download Service proxy settings and click Next.
> 10. Select the Update Manager Download Service installation and patch download directories and click Next
>     If you do not want to use the default locations, you can click Change to browse to a different directory.
>     You can select the patch store to be an existing download directory from a previous UMDS 4.x installation and reuse the applicable downloaded updates in UMDS 5.0. Once you associate an existing download directory with UMDS 5.0, you cannot use it with earlier UMDS versions.
> 11. (Optional) In the warning message about the disk free space, click OK.
> 12. Click Install to begin the installation.
> 13. Click OK in the Warning message notifying you that .NET Framework 3.5 SP1 is not installed.
>     The UMDS installer installs the prerequisite before the actual product installation.
> 14. Click Finish.
>
> UMDS and the Update Manager Utility are installed on your system

Now we can configure UMDS, from "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Setting Up and Using UMDS**
> You can set up UMDS to download upgrades for virtual appliances, or patches and notifications for ESX/ESXi hosts. You can also set up UMDS to download ESX/ESXi 4.x and ESXi 5.0 patch binaries, patch metadata, and notifications from third-party portals.
>
> After you download the upgrades, patch binaries, patch metadata, and notifications, you can export the data to a Web server or a portable media drive and set up Update Manager to use a folder on the Web server or the media drive (mounted as a local disk) as a shared repository.
>
> You can also set up UMDS to download ESX/ESXi 4.x and ESXi 5.0 patches and notifications from third-party portals.
>
> To use UMDS, the machine on which you install it must have Internet access. After you download the data you want, you can copy it to a local Web server or a portable storage device, such as a CD or USB flash drive. The best practice is to create a script to download the patches manually and set it up as a Windows Scheduled Task that downloads the upgrades and patches automatically.

And more from the same document:

> **Set Up the Data to Download with UMDS**
> By default UMDS downloads patch binaries, patch metadata, and notifications for hosts. You can specify which patch binaries and patch metadata to download with UMDS.
> **Procedure**
>
> 1.  Log in to the machine where UMDS is installed, and open a Command Prompt window.
> 2.  Navigate to the directory where UMDS is installed.
>     The default location in 64-bit Windows is C:\Program Files(x86)\VMware\Infrastructure\UpdateManager.
> 3.  Specify the updates to download.
>     *   To set up a download of all ESX/ESXi host updates and all virtual  appliance upgrades, run the following command:
>
>	         vmware-umds -S --enable-host --enable-va
>
>     *   To set up a download of all ESX/ESXi host updates and disable the download of virtual appliance upgrades, run the following command:
>
>	         vmware-umds -S --enable-host --disable-va
>
>     *   To set up a download of all virtual appliance upgrades and disable the download of host updates, run the following command:
>
>	         vmware-umds -S --disable-host --enable-va
>
>     *   To set up a download of only ESX 4.0 and ESXi 4.0 host updates, run the following commands:
>
>	         vmware-umds -S --disable-host
>	         vmware-umds -S -e esx-4.0.0 embeddedEsx-4.0.0
>
>     *   To set up a download of all ESX/ESXi 4.x and ESXi 5.0 updates, and to disable downloading of only ESX 3.5 and ESXi 3.5 host updates, run the following commands:
>
>	         vmware-umds -S --enable-host
>	         vmware-umds -S -d esx-3.5.0 embeddedEsx-3.5.0
>

Also check out "[here](http://www.jasemccarty.com/blog/?p=1859) is the pdf version of that site.

### Configure a shared repository

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Use a Shared Repository as a Download Source**
> You can configure Update Manager to use a shared repository as a source for downloading virtual appliance upgrades, as well as ESX/ESXi patches, extensions, and notifications.
>
> **Prerequisites**
> You must create the shared repository using UMDS and host it on a Web server or a local disk. The UMDS version you use must be of a version compatible with your Update Manager installation.
>
> For more information about the compatibility, see “Compatibility Between UMDS and the Update Manager Server,” on page 58. You can find the detailed procedure about exporting the upgrades, patch binaries, patch metadata, and notifications in “Export the Downloaded Data,” on page 62.
>
> Connect the vSphere Client to a vCenter Server system with which Update Manager is registered, and on the Home page, click Update Manager under Solutions and Applications. If your vCenter Server system is part of a connected group in vCenter Linked Mode, you must specify the Update Manager instance to use, by selecting the name of the corresponding vCenter Server system in the navigation bar.
>
> **Procedure**
>
> 1.  On the Configuration tab, under Settings, click Download Settings.
> 2.  In the Download Sources pane, select Use a shared repository
> 3.  Enter the path or the URL to the shared repository.
>     For example, C:\repository_path\, https://repository_path/, or http://repository_path/
>     In these examples, repository_path is the path to the folder to which you have exported the downloaded upgrades, patches, extensions, and notifications. In an environment where the Update Manager server does not have direct access to the Internet, but is connected to a machine that has Internet access, the folder can be on a Web server.
>     You can specify an HTTP or HTTPS address, or a location on the disk on which Update Manager is installed. HTTPS addresses are supported without any authentication.
> 4.  Click Validate URL to validate the path.
>     You must make sure that the validation is successful. If the validation fails, Update Manager reports a reason for the failure. You can use the path to the shared repository only when the validation is successful.
> 5.  Click Apply.
> 6.  Click Download Now to run the VMware vSphere Update Manager Update Download task and to download the updates immediately.
>
> The shared repository is used as a source for downloading upgrades, patches, and notifications.

Taken from "[VMware vSphere 5 Evaluator's Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware-vsphere-evaluation-guide-1-white-paper.pdf)", here is how it looks like from vCenter:

![shared_repository_vum](https://github.com/elatov/uploads/raw/master/2012/12/shared_repository_vum.png)

### Configure smart rebooting

> **Configure Smart Rebooting**
> Smart rebooting selectively restarts the virtual appliances and virtual machines in the vApp to maintain startup dependencies. You can enable and disable smart rebooting of virtual appliances and virtual machines in a vApp after remediation.
>
> A vApp is a prebuilt software solution, consisting of one or more virtual machines and applications, which are potentially operated, maintained, monitored, and updated as a unit.
>
> Smart rebooting is enabled by default. If you disable smart rebooting, the virtual appliances and virtual machines are restarted according to their individual remediation requirements, disregarding existing startup dependencies
>
> **Prerequisites**
> Connect the vSphere Client to a vCenter Server system with which Update Manager is registered, and on the Home page, click Update Manager under Solutions and Applications. If your vCenter Server system is part of a connected group in vCenter Linked Mode, you must specify the Update Manager instance to use, by selecting the name of the corresponding vCenter Server system in the navigation bar.
>
> **Procedure**
>
> 1.  On the Configuration tab, under Settings, click vApp Settings.
> 2.  Deselect Enable smart reboot after remediation to disable smart rebooting.

Here is how it looks like from vCenter:

![vum_smart-booting](https://github.com/elatov/uploads/raw/master/2012/12/vum_smart-booting.png)

### Manually download updates to a repository

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Import Patches Manually**
> Instead of using a shared repository or the Internet as a download source for patches and extensions, you can import patches and extensions manually by using an offline bundle.
>
> You can import offline bundles only for hosts that are running ESX/ESXi 4.0 or later.
>
> **Prerequisites**
> The patches and extensions you import must be in ZIP format.
>
> To import patches and extensions, you must have the Upload File privilege. For more information about managing users, groups, roles, and permissions, see vCenter Server and Host Management. For a list of Update Manager privileges and their descriptions, see “Update Manager Privileges,” on page 81.
>
> Connect the vSphere Client to a vCenter Server system with which Update Manager is registered, and on the Home page, click Update Manager under Solutions and Applications. If your vCenter Server system is part of a connected group in vCenter Linked Mode, you must specify the Update Manager instance to use, by selecting the name of the corresponding vCenter Server system in the navigation bar.
>
> Procedure
>
> 1.  On the Configuration tab, under Settings, click Download Settings.
> 2.  Click Import Patches at the bottom of the Download Sources pane.
> 3.  On the Select Patches File page of the Import Patches wizard, browse to and select the .zip file containing the patches you want to import.
> 4.  Click Next and wait until the file upload completes successfully.
>     After a successful upload, the Confirm Import page appears.
>     In case of upload failure, check whether the structure of the .zip file is correct or whether the Update Manager network settings are set up correctly.
> 5.  On the Confirm Import page of the Import Patches wizard, review the patches that you have selected to import into the Update Manager repository.
> 6.  Click Finish.
>
> You imported the patches into the Update Manager patch repository. You can view the imported patches on the Update Manager Patch Repository tab.

Here is an example of importing the 5.0u1 update into update manager. First go to Home-> 'Solution and Application' -> 'Update Manager' -> Select 'Patch Repository' tab -> click on 'Import Patches'. You will see the following screen:

![vum-import-patch](https://github.com/elatov/uploads/raw/master/2012/12/vum-import-patch.png)

Click Next to upload the patch, during the upload you will see the progress like so:

![progress_import_patch_vum](https://github.com/elatov/uploads/raw/master/2012/12/progress_import_patch_vum.png)

When the upload is done you will see a list of patches, including yours:

![finished_import_of_patch_vum](https://github.com/elatov/uploads/raw/master/2012/12/finished_import_of_patch_vum.png)

### Perform orchestrated vSphere upgrades

From "[vSphere Upgrade vSphere 5.0 Update 1](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-vcenter-server-703-upgrade-guide.pdf)":

> **Perform an Orchestrated Upgrade of Hosts Using vSphere Update Manager**
> You can use Update Manager to perform orchestrated upgrades of the ESX/ESXi hosts in your vSphere inventory by using a single upgrade baseline, or by using a baseline group.
>
> This workflow describes the overall process to perform an orchestrated upgrade of the hosts in your vSphere inventory. Update Manager 5.0 supports host upgrades to ESXi 5.0 for hosts that are running ESX/ESXi 4.x.
>
> You can perform orchestrated upgrades of hosts at the folder, cluster, or datacenter level.
>
> **Prerequisites**
>
> *   Make sure your system meets the requirements for vCenter Server 5.0, ESXi 5.0, and Update Manager 5.0.
> *   Install or upgrade vCenter Server to version 5.0.
> *   Install or upgrade vSphere Update Manager to version 5.0.
>
> **Procedure**
>
> 1.  Configure Host Maintenance Mode Settings
>     ESX/ESXi host updates might require that the host enters maintenance mode before they can be applied. Update Manager puts the ESX/ESXi hosts in maintenance mode before applying these updates. You can configure how Update Manager responds if the host fails to enter maintenance mode.
> 2.  Configure Cluster Settings
>     For ESX/ESXi hosts in a cluster, the remediation process can run either in a sequence or in parallel. Certain features might cause remediation failure. If you have VMware DPM, HA admission control, or Fault Tolerance enabled, you should temporarily disable these features to make sure that the remediation is successful.
> 3.  Enable Remediation of PXE Booted ESXi 5.0 Hosts
>     You can configure Update Manager to let other software initiate remediation of PXE booted ESXi 5.x hosts. The remediation installs patches and software modules on the hosts, but typically the host updates are lost after a reboot.
> 4.  Import Host Upgrade Images and Create Host Upgrade Baselines
>     You can create upgrade baselines for ESX/ESXi hosts with ESXi 5.x images that you import to the Update Manager repository.
> 5.  Create a Host Baseline Group
>     You can combine one host upgrade baseline with multiple patch or extension baselines, or combine multiple patch and extension baselines in a baseline group.
> 6.  Attach Baselines and Baseline Groups to Objects
>     To view compliance information and remediate objects in the inventory against specific baselines and baseline groups, you must first attach existing baselines and baseline groups to these objects.
> 7.  Manually Initiate a Scan of ESX/ESXi Hosts
>     Before remediation, you should scan the vSphere objects against the attached baselines and baseline groups. To run a scan of hosts in the vSphere inventory immediately, initiate a scan manually.
> 8.  View Compliance Information for vSphere Objects
>     You can review compliance information for the virtual machines, virtual appliances, and hosts against baselines and baseline groups that you attach.
> 9.  Remediate Hosts Against an Upgrade Baseline
>     You can remediate ESX/ESXi hosts against a single attached upgrade baseline at a time. You can upgrade or migrate all hosts in your vSphere inventory by using a single upgrade baseline containing an ESXi 5.0 image.
> 10. Remediate Hosts Against Baseline Groups
>     You can remediate hosts against attached groups of upgrade, patch, and extension baselines. Baseline groups might contain multiple patch and extension baselines, or an upgrade baseline combined with multiple patch and extension baselines.

and from "[VMware vSphere 5.0 Upgrade Best Practices](http://www.vmware.com/files/pdf/techpaper/vSphere-5-Upgrade-Best-Practices-Guide.pdf)" we see the following:

> **Uploading the ESXi Installation ISO**
> Start the upgrade by uploading the ESXi 5.0 installation image into Update Manager. From the Update Manager screen, choose the ESXi Images tab and click the link to Import ESXi Image… . Follow the wizard to import the ESXi 5.0 Image.
>
> ![import_esxi_image_vum](https://github.com/elatov/uploads/raw/master/2012/12/import_esxi_image_vum.png)
>
> **Creating an Upgrade Baseline**
> Create an upgrade baseline using the uploaded ESXi 5.0 image. From the Update Manager screen, choose the Baselines and Groups tab. From the Baselines section on the left, choose Create… to create a new baseline. Follow the wizard to create a new baseline.
>
> ![create_new_baseline_vum](https://github.com/elatov/uploads/raw/master/2012/12/create_new_baseline_vum.png)
>
> ![esxi_image_vum](https://github.com/elatov/uploads/raw/master/2012/12/esxi_image_vum.png)
>
> **Attaching the Baseline to Your Cluster/Host**
> Attach the upgrade baseline to your host or cluster. From the vCenter Hosts and Clusters view, select the Update Manager tab and choose Attach… . Select the upgrade baseline created previously. If you have any other upgrade baselines attached, remove them.
>
> ![host_update_vum_p4](https://github.com/elatov/uploads/raw/master/2012/12/host_update_vum_p4.png)
>
> **Scanning the Cluster/Host**
> Scan your hosts to ensure that the host requirements are met and you are ready to upgrade. From the vCenter Hosts and Clusters view, select the host/cluster, select the Update Manager tab and select Scan... . Wait for the scan to complete.
>
> If the hosts return a status of Non-Compliant, you are ready to proceed with upgrading the host.
>
> ![host_update_vum_p3_1](https://github.com/elatov/uploads/raw/master/2012/12/host_update_vum_p3_1.png)
>
> **Remediating Your Host**
> After the scan completes and your host is flagged as Non-Compliant, you are ready to perform the upgrade. From the Hosts and Clusters view, select the host/cluster, select the Update Manager tab and select Remediate. You will get a pop-up asking if you want to install patches, upgrade, or do both. Choose the upgrade option and follow the wizard to complete the remediation.
>
> ![host_update_vum_p5](https://github.com/elatov/uploads/raw/master/2012/12/host_update_vum_p5.png)
>
> Assuming that DRS is enabled and running in fully automated mode, Update Manager will proceed to place the host into maintenance mode (if not already in maintenance mode) and perform the upgrade. If DRS is not enabled, you must evacuate the virtual machines off the host and put it into maintenance mode before remediating.
>
> After the upgrade, the host will reboot and Update Manager will take it out of maintenance mode and return the host into operation.
>
> **Using Update Manager to Upgrade an Entire Cluster**
> You can use Update Manager to remediate an individual host or an entire cluster. If you choose to remediate an entire cluster, Update Manager will “roll” the upgrade through the cluster, upgrading each host in turn. You have flexibility in determining how Update Manager will treat the virtual machines during the upgrade. You can choose to either power them off or use vMotion to migrate them to another host. If you chose to power off the virtual machines, Update Manager will first power off all the virtual machines in the cluster and then proceed to upgrade the entire cluster in parallel. If you choose to migrate the virtual machines, Update Manager will evacuate as many hosts as it can (keeping within the HA admission control constraints) and upgrade the evacuated hosts in parallel. Then, after they are upgraded, it will move on to the next set of hosts.

### Create and modify baseline groups

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Creating Baselines and Baseline Groups**
> Baselines contain a collection of one or more patches, extensions, service packs, bug fixes, or upgrades, andcan be classified as patch, extension, or upgrade baselines. Baseline groups are assembled from existing baselines.
>
> Host baseline groups can contain a single upgrade baseline, as well as a number of patch and extension baselines.
>
> Virtual machine and virtual appliance baseline groups can contain up to three upgrade baselines: one VMware Tools upgrade baseline, one virtual machine hardware upgrade baseline, and one virtual appliance upgrade baseline.
>
> When you scan hosts, virtual machines, and virtual appliances, you evaluate them against baselines and baseline groups to determine their level of compliance.
>
> Update Manager includes two predefined patch baselines and three predefined upgrade baselines. You cannot edit or delete the three predefined virtual machine and virtual appliance upgrade baselines. You can use the predefined baselines, or create patch, extension, and upgrade baselines that meet your criteria. Baselines you create, as well as predefined baselines, can be combined in baseline groups
>
> **Baseline Types**
> Update Manager supports different types of baselines that you can use when scanning and remediating objects in your inventory.
>
> Update Manager provides upgrade, patch, and extension baselines.
>
> ![vum_upgrade_baselines](https://github.com/elatov/uploads/raw/master/2012/12/vum_upgrade_baselines.png)
>
> ![vum_extension_baselines](https://github.com/elatov/uploads/raw/master/2012/12/vum_extension_baselines.png)

More from the same document:

> Create a Host Baseline Group
> You can combine one host upgrade baseline with multiple patch or extension baselines, or combine multiple patch and extension baselines in a baseline group.
>
> **Prerequisites**
> Connect the vSphere Client to a vCenter Server system with which Update Manager is registered, and on the Home page, click Update Manager under Solutions and Applications. If your vCenter Server system is part of a connected group in vCenter Linked Mode, you must specify the Update Manager instance to use, by selecting the name of the corresponding vCenter Server system in the navigation bar.
>
> **Procedure**
>
> 1.  On the Baselines and Groups tab, click Create above the Baseline Groups pane.
> 2.  Enter a unique name for the baseline group.
> 3.  Under Baseline Group Type, select Host Baseline Group and click Next.
> 4.  Select a host upgrade baseline to include it in the baseline group.
> 5.  (Optional) Create a new host upgrade baseline by clicking Create a new Host Upgrade Baseline at the bottom of the Upgrades page and complete the New Baseline wizard.
> 6.  Click Next.
> 7.  Select the patch baselines that you want to include in the baseline group.
> 8.  (Optional) Create a new patch baseline by clicking Create a new Host Patch Baseline at the bottom of the Patches page and complete the New Baseline wizard.
> 9.  Click Next.
> 10. Select the extension baselines to include in the baseline group.
> 11. (Optional) Create a new extension baseline by clicking Create a new Extension Baseline at the bottom of the Patches page and complete the New Baseline wizard.
> 12. On the Ready to Complete page, click Finish.
>
> The host baseline group is displayed in the Baseline Groups pane.

Screenshots of the above process were seen in the previous objective

### Troubleshoot Update Manager problem areas and issues

In the "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)" guide here is an index of all the available troubleshooting scenarios.

> **Troubleshooting 173**
> Connection Loss with Update Manager Server or vCenter Server in a Single vCenter Server System 173
> Connection Loss with Update Manager Server or vCenter Server in a Connected Group in vCenter Linked Mode 174
> Gather Update Manager Log Bundles 175
> Gather Update Manager and vCenter Server Log Bundles 175
> Log Bundle Is Not Generated 175
> Host Extension Remediation or Staging Fails Due to Missing Prerequisites 176
> No Baseline Updates Available 176
> All Updates in Compliance Reports Are Displayed as Not Applicable 177
> All Updates in Compliance Reports Are Unknown 177
> VMware Tools Upgrade Fails if VMware Tools Is Not Installed 177
> ESX/ESXi Host Scanning Fails 178
> ESXi Host Upgrade Fails 178
> The Update Manager Repository Cannot Be Deleted 178
> Incompatible Compliance State 179
> Updates Are in Conflict or Conflicting New Module State 180
> Updates Are in Missing Package State 180
> Updates Are in Not Installable State 181
> Updates Are in Unsupported Upgrade State 181

### Generate database reports using MS Excel or MS SQL

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Generate Common Reports Using Microsoft Office Excel 2003**
> Using Microsoft Excel, you can connect to the Update Manager database and query the database views to generate a common report
>
> **Prerequisites**
> You must have an ODBC connection to the Update Manager database.
>
> **Procedure**
>
> 1.  Log in to the computer on which the Update Manager database is set up.
> 2.  From the Windows Start menu, select Programs > Microsoft Office > Microsoft Excel.
> 3.  Click Data > Import External Data > New Database Query.
> 4.  In the Choose Data Source window, select VMware Update Manager and click OK.
>     If necessary, in the database query wizard, select the ODBC DSN name and enter the user name and password for the ODBC database connection.
> 5.  In the Query Wizard - Choose Columns window, select the columns of data to include in your query and click Next
>     ![options_for_excel_for_vum](https://github.com/elatov/uploads/raw/master/2012/12/options_for_excel_for_vum.png)
>     For example, if you want to get the latest scan results for all objects in the inventory and all patches for an inventory object, select the following database views and their corresponding columns from the Available tables and columns pane:</p>
>     *   VUMV_UPDATES
>     *   VUMV_ENTITY_SCAN_RESULTS
> 6.  Click OK in the warning message that the query wizard cannot join the tables in your query.
> 7.  In the Microsoft Query window, drag a column name from the first view to the other column to join the columns in the tables manually.
>     For example, join the META_UID column from the VUMV_UPDATES database view with the UPDATE_METAUID column from the VUMV_ENTITY_SCAN_RESULTS database view. A line between the columns selected indicates that these columns are joined.
>
> The data is automatically queried for all inventory objects in the Microsoft Query window

Also from the same document:

> **Generate Common Reports Using Microsoft SQL Server Query**
> Using a Microsoft SQL Server query, you can generate a common report from the Update Manager database.
>
> **Procedure**
>
> *   To generate a report containing the latest scan results for all objects in the inventory and for all patches for an inventory object, run the query in Microsoft SQL Client.
>
>
> 		SELECT r.entity_uid,r.ENTITY_STATUS,
> 		u.meta_uid, u.title, u.description, u.type, u.severity,
> 		(case when u.SPECIAL_ATTRIBUTE is null then 'false'
> 		else 'true'
> 		end) as IS_SERVICE_PACK,
> 		r.scanh_id, r.scan_start_time, r.scan_end_time
> 		FROM VUMV_UPDATES u JOIN VUMV_ENTITY_SCAN_RESULTS r ON (u.meta_uid = r.update_metauid)
> 		ORDER BY r.entity_uid, u.meta_uid
>
>
> The query displays all patches that are applicable to the scanned objects in the inventory.

### Upgrade vApps using Update Manager

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Upgrading Virtual Appliances**
> An upgrade remediation of a virtual appliance upgrades the entire software stack in the virtual appliance,including the operating system and applications. To upgrade the virtual appliance to the latest released or latest critical version, you can use one of the Update Manager predefined upgrade baselines or create your own.
>
> This workflow describes how to upgrade the virtual appliances in your vSphere inventory. You can upgrade virtual appliances at the folder or datacenter level. You can also upgrade a single virtual appliance. This workflow describes the process to upgrade multiple virtual appliances in a container object.
>
> 1.  (Optional) Create a virtual appliance upgrade baseline.
>     You create virtual appliance baselines from the Baselines and Groups tab in the Update Manager Administration view.
> 2.  Attach virtual appliance upgrade baselines to an object containing the virtual appliances that you want to upgrade.
>     To scan and upgrade virtual appliances, attach your virtual appliance upgrade baselines to a container object containing the virtual appliances that you want to upgrade. The container object can be a folder, vApp, or datacenter.
>     *   Scan the container object.
>         After you attach the virtual appliance upgrade baselines to the selected container object, you must scan it to view the compliance state of the virtual appliances in the container. You can scan selected objects manually to start the scanning immediately.
>         You can also scan the virtual appliances in the container object at a time convenient for you by scheduling a scan task.
>         *   Review the scan results displayed in the Update Manager Client Compliance view.
>         *   Remediate the virtual appliances in the container object against the attached virtual appliance upgrade baselines.
>             If virtual appliances are in a Non-Compliant state, remediate the container object of the virtual appliances to make it compliant with the attached baselines. You can start the remediation process manually or schedule a remediation task.
>
>             Update Manager directs the virtual appliances to download the missing updates and controls the remediation process of when and how to remediate, but the virtual appliance downloads and installs the updates itself.
>             The remediated virtual appliances become compliant with the attached baseli
>

Here is an example of updating the vMA appliance. First Create a new Baseline for the Virtual Appliance:

![create_new_baseline_for_va_update](https://github.com/elatov/uploads/raw/master/2012/12/create_new_baseline_for_va_update.png)

Next Create a Vendor Rule:

![create_vendor_rule_for_va_update](https://github.com/elatov/uploads/raw/master/2012/12/create_vendor_rule_for_va_update.png)

Here are the options for the Vendor Rules:

![vendor_rules_options_va_update](https://github.com/elatov/uploads/raw/master/2012/12/vendor_rules_options_va_update.png)

After completion, go the "VMs and Templates" View and select the Appliance and attach your baseline to it. Here is how it will look:

![non-compliant_va_for_update](https://github.com/elatov/uploads/raw/master/2012/12/non-compliant_va_for_update.png)

Click "Scan" from the same screen and select the type of scan:

![va_vum_scan](https://github.com/elatov/uploads/raw/master/2012/12/va_vum_scan.png)

Then click on "Remediate" to actually perform the upgrade:

![remediate_va_update](https://github.com/elatov/uploads/raw/master/2012/12/remediate_va_update.png)

That should be it.

### Utilize Update Manager PowerCLI to export baselines for testing

From "[Installing and Administering VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-672-install-administration-guide.pdf)":

> **Testing Patches or Extensions and Exporting Baselines to Another Update Manager Server**
> Before you apply patches or extensions to ESX/ESXi hosts, you might want to test the patches and extensions by applying them to hosts in a test environment. You can then use Update Manager PowerCLI to export the tested baselines to another Update Manager server instance and apply the patches and extensions to the other hosts.
>
> Update Manager PowerCLI is a command-line and scripting tool built on Windows PowerShell, and provides a set of cmdlets for managing and automating Update Manager. For more information about installing and using Update Manager PowerCLI, see VMware vSphere Update Manager PowerCLI Installation and Administration Guide

From the same document:

> You can export and import patch baselines from one Update Manager server to another by using an Update Manager PowerCLI script. The following example script creates a duplicate of the baseline MyBaseline on the $destinationServer.
> NOTE The script works for fixed and dynamic patch baselines as well as for extension baselines.
>
>
> 	# $destinationServer = Connect-VIServer
> 	# $sourceServer = Connect-VIServer
> 	# $baselines = Get-PatchBaseline MyBaseline -Server $sourceServer
> 	# ExportImportBaselines.ps1 $baselines $destinationServer
> 	Param([VMware.VumAutomation.Types.Baseline[]] $baselines,
> 	[VMware.VimAutomation.Types.VIServer[]]$destinationServers)
> 	$ConfirmPreference = 'None'
> 	$includePatches = @()
> 	$excludePatches = @()
> 	function ExtractPatchesFromServer([VMware.VumAutomation.Types.Patch[]]$patches,
> 	[VMware.VimAutomation.Types.VIServer]$destinationServer){
> 	$result = @()
> 	if ($patches -ne $null){
> 	foreach($patch in $patches){
> 	$extractedPatches = Get-Patch -Server $destinationServer -SearchPhrase
> 	$patch.Name
> 	if ($extractedPatches -eq $null){
> 	Write-Warning -Message "Patch '$($patch.Name)' is not available on the server$destinationServer"
> 	} else {
> 	$isFound = $false
> 	foreach ($newPatch in $extractedPatches){
> 	if ($newPatch.IdByVendor -eq $patch.IdByVendor){
> 	$result += $newPatch
> 	$isFound = $true
> 	}
> 	}
> 	if ($isFound -eq $false) {
> 	Write-Warning -Message "Patch '$($patch.Name)' with VendorId '$($patch.IdByVendor)' is not available on the server $destinationServer"
> 	}
> 	}
> 	}
> 	}
> 	return .$result;
> 	}
> 	function CreateStaticBaseline([VMware.VumAutomation.Types.Baseline]$baseline,
> 	[VMware.VimAutomation.Types.VIServer]$destinationServer){
> 	$includePatches = ExtractPatchesFromServer $baseline.CurrentPatches $destinationServer
> 	if ($includePatches.Count -lt 1){
> 	write-error "Static baseline '$($baseline.Name)' can't be imported. No one of the patches
> 	it contains are available on the server $destinationServer"
> 	} else {
> 	$command = 'New-PatchBaseline -Server $destinationServer -Name $baseline.Name -Description
> 	$baseline.Description -Static -TargetType $baseline.TargetType -IncludePatch $includePatches'
> 	if ($baseline.IsExtension) {
> 	$command += ' -Extension'
> 	}
> 	Invoke-Expression $command
> 	}
> 	}
> 	function  CreateDynamicBaseline([VMware.VumAutomation.Types.Baseline]$baseline,
> 	[VMware.VimAutomation.Types.VIServer]$destinationServer)
> 	{
> 	if ($baseline.BaselineContentType -eq 'Dynamic'){
> 	$command = 'New-PatchBaseline -Server $destinationServer -Name $baseline.Name -Description
> 	$baseline.Description -TargetType $baseline.TargetType -Dynamic -SearchPatchStartDate
> 	$baseline.SearchPatchStartDate - SearchPatchEndDate $baseline.SearchPatchEndDate -
> 	 SearchPatchProduct $baseline.SearchPatchProduct -SearchPatchSeverity
> 	 $baseline.SearchPatchSeverity -SearchPatchVendor $baseline.SearchPatchVendor'
> 	} elseif ($baseline.BaselineContentType -eq 'Both'){
> 	 $includePatches = ExtractPatchesFromServer $baseline.InclPatches $destinationServer
> 	 $excludePatches = ExtractPatchesFromServer $baseline.ExclPatches $destinationServer
> 	 $command = 'New-PatchBaseline -Server $destinationServer -Name $baseline.Name -Description
> 	$baseline.Description -TargetType $baseline.TargetType -Dynamic -SearchPatchStartDate
> 	$baseline.SearchPatchStartDate -SearchPatchEndDate $baseline.SearchPatchEndDate -
> 	SearchPatchProduct $baseline.SearchPatchProduct -SearchPatchSeverity
> 	$baseline.SearchPatchSeverity -SearchPatchVendor $baseline.SearchPatchVendor'
> 	if ($includePatches.Count -gt 0){
> 	$command += ' -IncludePatch $includePatches'
> 	}
> 	if ($excludePatches.Count -gt 0){
> 	 $command += ' -ExcludePatch $excludePatches'
> 	}
> 	 }
> 	 #check for null because there is known issue for creating baseline with null
> 	SearchPatchPhrase
> 	 if ($baseline.SearchPatchPhrase -ne $null){
> 	 $command += ' -SearchPatchPhrase $baseline.SearchPatchPhrase'
> 	}
> 	Invoke-Expression $command
> 	 }
> 	foreach ($destinationServer in $destinationServers) {
> 	 if ($baselines -eq $null) {
> 	 Write-Error "The baselines parameter is null"
> 	 } else {
> 	 foreach($baseline in $baselines){
> 	if ($baseline.GetType().FullName -eq 'VMware.VumAutomation.Types.PatchBaselineImpl'){
> 	 Write-Host "Import '" $baseline.Name "' to the server $destinationServer"
> 	 if($baseline.BaselineContentType -eq 'Static'){
> 	 CreateStaticBaseline $baseline $destinationServer
> 	} else {
> 	CreateDynamicBaseline $baseline $destinationServer
> 	}
> 	} else {
> 	Write-Warning -Message "Baseline '$($baseline.Name)' is not patch baseline and will be skipped."
> 	}
> 	}
> 	}
> 	}


You have now exported the tested baseline to another Update Manager server.

### Utilize the Update Manager Utility to reconfigure vUM settings

From "[Reconfiguring VMware vSphere Update Manager](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-update-manager-651-reconfig-guide.pdf)":

> **Start the Update Manager Utility and Log In**
> To use the Update Manager Utility, you must start the utility and log in
>
> **Prerequisites**
>
> *   Make sure that you have local administrative credentials for the machine on which the Update Manager server is installed.
> *   Stop the Update Manager service.
>
> **Procedure**
>
> 1.  Log in as an administrator to the machine on which the Update Manager server is installed.
> 2.  Navigate to the Update Manager installation directory. The default location is C:\Program Files (x86)\VMware\Infrastructure\Update Manager.
> 3.  Double-click the VMwareUpdateManagerUtility.exe file.
> 4.  Type the vCenter Server machine IP address or host name and the administrative credentials to the vCenter Server system.
> 5.  Click Login.
>
> You successfully logged in to the Update Manager Utility.

You will be presented with the utility, from here you can edit the following:

> **Using the Update Manager Utility**
> By using the Update Manager Utility, you can change the database connection settings and proxy authentication, re-register Update Manager with vCenter Server, and replace the SSL certificate.

Here is a couple of screenshots of some of the available settings:

![1st_window_vum_utility](https://github.com/elatov/uploads/raw/master/2012/12/1st_window_vum_utility.png)

![vum_utility](https://github.com/elatov/uploads/raw/master/2012/12/vum_utility.png)
