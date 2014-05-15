---
title: RHCSA and RHCE Chapter 6 Package Management
author: Karim Elatov
layout: post
permalink: /2013/03/rhcsa-and-rhce-chapter-6-package-management/
dsq_thread_id:
  - 1406654434
categories:
  - Certifications
  - RHCSA and RHCE
tags:
  - createrepo
  - rpm
  - rpmbuild
  - yum
---
The easiest way to install software on RHEL is to use RPM.

## RPM

From "<a href="https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf']);">Red Hat Enterprise Linux 6 Deployment Guide</a>":

> **RPM**  
> The RPM Package Manager (RPM) is an open packaging system, which runs on Red Hat Enterprise Linux as well as other Linux and UNIX systems. Red Hat, Inc. and the Fedora Project encourage other vendors to use RPM for their own products. RPM is distributed under the terms of the GPL (GNU General Public License). The RPM Package Manager only works with packages built to work with the RPM format. RPM is itself provided as a pre-installed rpm package. For the end user, RPM makes system updates easy. Installing, uninstalling and upgrading RPM packages can be accomplished with short commands. RPM maintains a database of installed packages and their files, so you can invoke powerful queries and verifications on your system. The RPM package format has been improved for Red Hat Enterprise Linux 6. RPM packages are now compressed using the XZ lossless data compression format, which has the benefit of greater compression and less CPU usage during decompression, and support multiple strong hash algorithms, such as SHA-256, for package signing and verification.

### RPM Installation

More from the same guide:

> **B.2. Using RPM**  
> RPM has five basic modes of operation (not counting package building): installing, uninstalling, upgrading, querying, and verifying. This section contains an overview of each mode. For complete details and options, try **rpm -help** or **man rpm**. 
> 
> **B.2.2. Installing and Upgrading**  
> RPM packages typically have file names like **tree-1.5.3-2.el6.x86_64.rpm**. The file name includes the package name (**tree**), version (**1.5.3**), release (**2**), operating system major version (**el6**) and CPU architecture (**x86_64**). You can use **rpm'**s **-U** option to:
> 
> *   upgrade an existing but older package on the system to a newer version, or 
> *   install the package even if an older version is not already installed.
> 
> That is, **rpm -U rpm_file** is able to perform the function of either upgrading or installing as is appropriate for the package. Assuming the **tree-1.5.3-2.el6.x86_64.rpm** package is in the current directory, log in as root and type the following command at a shell prompt to either upgrade or install the *tree* package as determined by **rpm**:
> 
>     rpm -Uvh tree-1.5.3-2.el6.x86_64.rpm 
>     
> 
> If the upgrade/installation is successful, the following output is displayed:
> 
>     Preparing... ########################################### [100%]
>     1:tree ########################################### [100%]
>     
> 
> **NOTE:** **rpm** provides two different options for installing packages: the aforementioned **-U** option (which historically stands for upgrade), and the **-i** option, historically standing for install. Because the **-U** option subsumes both install and upgrade functions, we recommend to use **rpm -Uvh** with all packages except **kernel** packages. You should always use the **-i** option to simply install a new kernel package instead of upgrading it. This is because using the **-U** option to upgrade a kernel package removes the previous (older) kernel package, which could render the system unable to boot if there is a problem with the new kernel. Therefore, use the **rpm -i kernel_package** command to install a new kernel without replacing any older kernel packages.

So let's go ahead and install the **tree** rpm on our system. Since we copied the whole DVD to the machine, let's find the path of the **tree** RPM:

    [root@rhel1 ~]# find repo/ -name "tree" 
    repo/Packages/tree-1.5.3-2.el6.i686.rpm
    

Now let's install the package:

    [root@rhel1 ~]# rpm -ivh repo/Packages/tree-1.5.3-2.el6.i686.rpm 
    Preparing... ########################################### [100%] 
    1:tree ########################################### [100%]
    

That looks good, now going to the next section of the guide:

> **B.2.2.1. Package Already Installed**  
> If a package of the same name and version is already installed, the following output is displayed:
> 
>     Preparing... ########################################### [100%] 
>     package tree-1.5.3-2.el6.x86_64 is already installed
>     
> 
> However, if you want to install the package anyway, you can use the **-replacepkgs** option, which tells RPM to ignore the error:
> 
>     rpm -Uvh --replacepkgs tree-1.5.3-2.el6.x86_64.rpm
>     
> 
> This option is helpful if files installed from the RPM were deleted or if you want the original configuration files from the RPM to be installed.
> 
> **B.2.2.3. Unresolved Dependency**  
> RPM packages may sometimes depend on other packages, which means that they require other packages to be installed to run properly. If you try to install a package which has an unresolved dependency, output similar to the following is displayed:
> 
>     error: Failed dependencies: bar.so.3()(64bit) is needed by foo-1.0-1.el6.x86_64
>     
> 
> If you are installing a package from the Red Hat Enterprise Linux installation media, such as from a CDROM or DVD, the dependencies may be available. Find the suggested package(s) on the Red Hat Enterprise Linux installation media or on one of the active Red Hat Enterprise Linux mirrors and add it to the command:
> 
>     rpm -Uvh foo-1.0-1.el6.x86_64.rpm bar-3.1.1.el6.x86_64.rpm
>     
> 
> If installation of both packages is successful, output similar to the following is displayed:
> 
>     Preparing... ########################################### [100%] 
>     1:foo ########################################### [ 50%] 
>     2:bar ########################################### [100%]
>     
> 
> You can try the **-whatprovides** option to determine which package contains the required file.
> 
>     rpm -q --whatprovides "bar.so.3" 
>     
> 
> If the package that contains bar.so.3 is in the RPM database, the name of the package is displayed:
> 
>     bar-3.1.1.el6.i586.rpm
>     
> 
> **B.2.3. Configuration File Changes**  
> Because RPM performs intelligent upgrading of packages with configuration files, you may see one or the other of the following messages:
> 
>     saving /etc/foo.conf as /etc/foo.conf.rpmsave
>     
> 
> This message means that changes you made to the configuration file may not be forward-compatible with the new configuration file in the package, so RPM saved your original file and installed a new one. You should investigate the differences between the two configuration files and resolve them as soon as possible, to ensure that your system continues to function properly. Alternatively, RPM may save the package's new configuration file as, for example, **foo.conf.rpmnew**, and leave the configuration file you modified untouched. You should still resolve any conflicts between your modified configuration file and the new one, usually by merging changes from the old one to the new one with a **diff** program. If you attempt to upgrade to a package with an older version number (that is, if a higher version of the package is already installed), the output is similar to the following:
> 
>     package foo-2.0-1.el6.x86_64.rpm (which is newer than foo-1.0-1) is already installed
>     
> 
> To force RPM to upgrade anyway, use the **-oldpackage** option:
> 
>     rpm -Uvh --oldpackage foo-1.0-1.el6.x86_64.rpm
>     

### RPM Removal

From the same guide:

> **B.2.4 . Uninstalling**  
> Uninstalling a package is just as simple as installing one. Type the following command at a shell prompt:
> 
>     rpm -e foo
>     
> 
> You can encounter dependency errors when uninstalling a package if another installed package depends on the one you are trying to remove. For example:
> 
>     rpm -e ghostscript error: 
>     Failed dependencies: 
>     libgs.so.8()(64bit) is needed by (installed) libspectre-0.2.2-3.el6.x86_64 
>     libgs.so.8()(64bit) is needed by (installed) foomatic-4.0.3-1.el6.x86_64 
>     libijs-0.35.so()(64bit) is needed by (installed) gutenprint-5.2.4-5.el6.x86_64 
>     ghostscript is needed by (installed) printer-filters-1.1-4.el6.noarch
>     

### RPM Freshening

> **B.2.5. Freshening**  
> Freshening is similar to upgrading, except that only existent packages are upgraded. Type the following command at a shell prompt:
> 
>     rpm -Fvh foo-2.0-1.el6.x86_64.rpm
>     
> 
> RPM's freshen option checks the versions of the packages specified on the command line against the versions of packages that have already been installed on your system. When a newer version of an already-installed package is processed by RPM's freshen option, it is upgraded to the newer version.However, RPM's freshen option does not install a package if no previously-installed package of the same name exists. This differs from RPM's upgrade option, as an upgrade does install packages whether or not an older version of the package was already installed. Freshening works for single packages or package groups. If you have just downloaded a large number of different packages, and you only want to upgrade those packages that are already installed on your system, freshening does the job. Thus, you do not have to delete any unwanted packages from the group that you downloaded before using RPM. In this case, issue the following with the ***.rpm** glob:
> 
>     rpm -Fvh *.rpm
>     
> 
> RPM then automatically upgrades only those packages that are already installed.

### RPM Querying

> **B.2.6. Querying**  
> The RPM database stores information about all RPM packages installed in your system. It is stored in the directory **/var/lib/rpm/**, and is used to query what packages are installed, what versions each package is, and to calculate any changes to any files in the package since installation, among other use cases. To query this database, use the **-q** option. The **rpm -q package name** command displays the package name, version, and release number of the installed package *package_name. For example, using **rpm -q tree** to query installed package tree might generate the following output:
> 
>     tree-1.5.2.2-4.el6.x86_64 
>     
> 
> You can also use the following Package Selection Options to further refine or qualify your query:
> 
> *   **-a** — queries all currently installed packages 
> *   **-f file_name** — queries the RPM database for which package owns file_name. Specify the absolute path of the file (for example, **rpm -qf /bin/ls** instead of rpm -qf ls). 
> *   **-p package_file** — queries the uninstalled package package_file There are a number of ways to specify what information to display about queried packages. The following options are used to select the type of information for which you are searching. These are called the Package Query Options.
> *   **-i** displays package information including name, description, release, size, build date, install date, vendor, and other miscellaneous information.
> *   **-l** displays the list of files that the package contains.
> *   **-s** displays the state of all the files in the package.
> *   **-d** displays a list of files marked as documentation (man pages, info pages, READMEs, etc.) in the package.
> *   **-c** displays a list of files marked as configuration files. These are the files you edit after installation to adapt and customize the package to your system (for example, sendmail.cf, passwd, inittab, etc.). For options that display lists of files, add **-v** to the command to display the lists in a familiar **ls -l** format.

### RPM Verification

> **B.2.7. Verifying**  
> Verifying a package compares information about files installed from a package with the same information from the original package. Among other things, verifying compares the file size, MD5 sum, permissions, type, owner, and group of each file. The command **rpm -V** verifies a package. You can use any of the Verify Options listed for querying to specify the packages you wish to verify. A simple use of verifying is **rpm -V tree**, which verifies that all the files in the tree package are as they were when they were originally installed. For example:
> 
> *   To verify a package containing a particular file:
>     
>         rpm -Vf /usr/bin/tree
>         
>     
>     In this example, **/usr/bin/tree** is the absolute path to the file used to query a package.
> 
> *   To verify ALL installed packages throughout the system (which will take some time):
>     
>         rpm -Va
>         
> 
> *   To verify an installed package against an RPM package file:
>     
>         rpm -Vp tree-1.5.3-2.el6.x86_64.rpm
>         
> 
> This command can be useful if you suspect that your RPM database is corrupt If everything verified properly, there is no output. If there are any discrepancies, they are displayed. The format of the output is a string of eight characters (a "c" denotes a configuration file) and then the file name. Each of the eight characters denotes the result of a comparison of one attribute of the file to the value of that attribute recorded in the RPM database. A single period (.) means the test passed. The following characters denote specific discrepancies:
> 
> *   **5** — MD5 checksum
> *   **S** — file size
> *   **L** — symbolic link
> *   **T** — file modification time
> *   **D** — device
> *   **U** — user
> *   **G** — group
> *   **M** — mode (includes permissions and file type)
> *   **?** — unreadable file (file permission errors, for example) 
> 
> If you see any output, use your best judgment to determine if you should remove the package, reinstall it, or fix the problem in another way.

Here is how my RPM Verification looked like:

    [root@rhel1 ~]# rpm -Va 
    ....L.... c /etc/pam.d/fingerprint-auth 
    ....L.... c /etc/pam.d/password-auth 
    ....L.... c /etc/pam.d/smartcard-auth 
    ....L.... c /etc/pam.d/system-auth 
    .......T. c /etc/inittab 
    S.5....T. c /etc/sysconfig/init
    

Since I had made some changes to the above files, this was actually expected.

### RPM Usage Examples

The last section from the guide is the following:

> **B.4. Practical and Common Examples of RPM Usage**  
> RPM is a useful tool for both managing your system and diagnosing and fixing problems. The best way to make sense of all its options is to look at some examples.
> 
> *   Perhaps you have deleted some files by accident, but you are not sure what you deleted. To verify your entire system and see what might be missing, you could try the following command:
>     
>         rpm -Va
>         
>     
>     If some files are missing or appear to have been corrupted, you should probably either re-install the package or uninstall and then re-install the package
> 
> *   At some point, you might see a file that you do not recognize. To find out which package owns it, enter:
>     
>         rpm -qf /usr/bin/ghostscript
>         
>     
>     The output would look like the following:
>     
>         ghostscript-8.70-1.el6.x86_64
>         
> 
> *   We can combine the above two examples in the following scenario. Say you are having problems with **/usr/bin/paste**. You would like to verify the package that owns that program, but you do not know which package owns paste. Enter the following command,
>     
>         rpm -Vf /usr/bin/paste
>         
>     
>     and the appropriate package is verified
> 
> *   Do you want to find out more information about a particular program? You can try the following command to locate the documentation which came with the package that owns that program:
>     
>         rpm -qdf /usr/bin/free
>         
>     
>     The output would be similar to the following:
>     
>         /usr/share/doc/procps-3.2.8/BUGS 
>         /usr/share/doc/procps-3.2.8/FAQ 
>         /usr/share/doc/procps-3.2.8/NEWS 
>         /usr/share/doc/procps-3.2.8/TODO 
>         /usr/share/man/man1/free.1.gz 
>         /usr/share/man/man1/pgrep.1.gz 
>         /usr/share/man/man1/pkill.1.gz 
>         /usr/share/man/man1/pmap.1.gz 
>         /usr/share/man/man1/ps.1.gz 
>         /usr/share/man/man1/pwdx.1.gz 
>         /usr/share/man/man1/skill.1.gz 
>         /usr/share/man/man1/slabtop.1.gz 
>         /usr/share/man/man1/snice.1.gz 
>         /usr/share/man/man1/tload.1.gz 
>         /usr/share/man/man1/top.1.gz 
>         /usr/share/man/man1/uptime.1.gz 
>         /usr/share/man/man1/w.1.gz 
>         /usr/share/man/man1/watch.1.gz 
>         /usr/share/man/man5/sysctl.conf.5.gz 
>         /usr/share/man/man8/sysctl.8.gz 
>         /usr/share/man/man8/vmstat.8.gz
>         
> 
> *   You may find a new RPM, but you do not know what it does. To find information about it, use the following command:
>     
>         rpm -qip crontabs-1.10-32.1.el6.noarch.rpm
>         
>     
>     The output would be similar to the following:
>     
>         Name        : crontabs                     Relocations: (not relocatable)
>         Version     : 1.10                              Vendor: Red Hat, Inc.
>         Release     : 32.1.el6                      Build Date: Thu 03 Dec 2009 02:17:44 AM CET
>         Install Date: (not installed)               Build Host: js20-bc1-11.build.redhat.com
>         Group       : System Environment/Base       Source RPM: crontabs-1.10-32.1.el6.src.rpm
>         Size        : 2486                             License: Public Domain and GPLv2
>         Signature   : RSA/8, Wed 24 Feb 2010 08:46:13 PM CET, Key ID 938a80caf21541eb
>         Packager    : Red Hat, Inc. <http: //bugzilla.redhat.com/bugzilla>
>         Summary     : Root crontab files used to schedule the execution of programs
>         Description :
>         The crontabs package contains root crontab files and directories.
>         You will need to install cron daemon to run the jobs from the crontabs.
>         The cron daemon such as cronie or fcron checks the crontab files to
>         see when particular commands are scheduled to be executed.  If commands
>         are scheduled, it executes them.
>         Crontabs handles a basic system function, so it should be installed on
>         your system
>         
> 
> *   Perhaps you now want to see what files the crontabs RPM package installs. You would enter the following:
>     
>          rpm -qlp crontabs-1.10-32.1.el6.noarch.rpm
>         
>     
>     The output is similar to the following:
>     
>         /etc/cron.daily 
>         /etc/cron.hourly 
>         /etc/cron.monthly 
>         /etc/cron.weekly 
>         /etc/crontab 
>         /usr/bin/run-parts 
>         /usr/share/man/man4/crontabs.4.gz
>         
>     
>     These are just a few examples. As you use RPM, you may find more uses for it

Let's run some of the above queries on our **tree** RPM. First let's see if it's installed:

    [root@rhel1 ~]# rpm -q tree 
    tree-1.5.3-2.el6.i686
    

Now let's see what files are installed by that package:

    [root@rhel1 ~]# rpm -ql tree 
    /usr/bin/tree 
    /usr/share/doc/tree-1.5.3 
    /usr/share/doc/tree-1.5.3/LICENSE 
    /usr/share/doc/tree-1.5.3/README 
    /usr/share/man/man1/tree.1.gz
    

Not let's confirm that the the **/usr/bin/tree** file belongs to the **tree** package:

    [root@rhel1 ~]# rpm -qf /usr/bin/tree 
    tree-1.5.3-2.el6.i686 
    

Lastly let's see the general information about the package:

    [root@rhel1 ~]# rpm -qi tree
    Name        : tree                         Relocations: (not relocatable)
    Version     : 1.5.3                             Vendor: Red Hat, Inc.
    Release     : 2.el6                         Build Date: Wed 03 Mar 2010 04:08:34 AM MST
    Install Date: Wed 06 Feb 2013 08:48:01 AM MST      Build Host: ls20-bc2-14.build.redhat.com
    Group       : Applications/File             Source RPM: tree-1.5.3-2.el6.src.rpm
    Size        : 64903                            License: GPLv2+
    Signature   : RSA/8, Mon 16 Aug 2010 02:13:31 PM MDT, Key ID 199e2f91fd431d51
    Packager    : Red Hat, Inc. </http:><http: //bugzilla.redhat.com/bugzilla>
    URL         : http://mama.indstate.edu/users/ice/tree/
    Summary     : File system tree viewer
    Description :
    The tree utility recursively displays the contents of directories in a
    tree-like format.  Tree is basically a UNIX port of the DOS tree
    utility.
    

we can also check out the *changelog* for the package:

    [root@rhel1 ~]# rpm -q --changelog tree | head
    * Wed Mar 03 2010 Tim Waugh <twaugh @redhat.com> 1.5.3-2
    - Added comments to all patches.
    * Fri Nov 27 2009 Tim Waugh </twaugh><twaugh @redhat.com> 1.5.3-1
    - 1.5.3 (bug #517342, bug #541255).
    * Sun Jul 26 2009 Fedora Release Engineering <rel -eng@lists.fedoraproject.org> - 1.5.2.2-4
    - Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
    * Wed Jun 10 2009 Tim Waugh <twaugh @redhat.com> 1.5.2.2-3
    

Another cool **rpm** argument is **-last**, you can list all the RPMs in the order of their installed date, like so:

    [root@rhel1 ~]# rpm -qa --last | head 
    tree-1.5.3-2.el6 Wed 06 Feb 2013 07:15:23 AM MST 
    rsync-3.0.6-5.el6_0.1 Wed 06 Feb 2013 04:36:30 AM MST 
    gpg-pubkey-fd431d51-4ae0493b Wed 06 Feb 2013 04:36:10 AM MST 
    gpg-pubkey-2fa658e0-45700c69 Wed 06 Feb 2013 04:36:10 AM MST 
    attr-2.4.44-4.el6 Mon 04 Feb 2013 04:36:34 AM MST 
    acl-2.2.49-4.el6 Mon 04 Feb 2013 04:36:33 AM MST 
    e2fsprogs-1.41.12-7.el6 Mon 04 Feb 2013 04:36:32 AM MST 
    audit-2.1-5.el6 Mon 04 Feb 2013 04:36:31 AM MST 
    sudo-1.7.4p5-5.el6 Mon 04 Feb 2013 04:36:29 AM MST 
    efibootmgr-0.5.4-9.el6 Mon 04 Feb 2013 04:36:28 AM MST
    

We can see that the **tree** package was installed today along with **rsync**. You can also change the format of the results:

    [root@rhel1 ~]# rpm -q --queryformat "%{NAME}-%{ARCH}-%{SIZE}_KB-%{INSTALLTIME:day}\n" 
    tree tree-i686-64903_KB-Wed Feb 06 2013
    

## YUM

Now as great as RPMs are, **yum** is more flexible and actually goes online to download the packages and then installs them. From "<a href="https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf']);">Red Hat Enterprise Linux 6 Deployment Guide</a>":

> **Chapter 5. Yum**  
> **YUM** is the Red Hat package manager that is able to query for information about available packages, fetch packages from repositories, install and uninstall them, and update an entire system to the latest available version. Yum performs automatic dependency resolution on packages you are updating, installing, or removing, and thus is able to automatically determine, fetch, and install all available dependent packages. **Yum** can be configured with new, additional repositories, or package sources, and also provides many plug-ins which enhance and extend its capabilities. Yum is able to perform many of the same tasks that **RPM** can; additionally, many of the command line options are similar. Yum enables easy and simple package management on a single machine or on groups of them. Yum also enables you to easily set up your own repositories of RPM packages for download and installation on other machines.

### YUM Updates

> **5.1. Checking For and Updating Packages**  
> **5.1.1. Checking For Updates**  
> To see which installed packages on your system have updates available, use the following command:
> 
>     yum check-update
>     
> 
> For example:
> 
>     ~]# yum check-update 
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager 
>     Updating Red Hat repositories. 
>     INFO:rhsm-app.repolib:repos updated: 0 
>     PackageKit.x86_64 0.5.8-2.el6            rhel 
>     PackageKit-glib.x86_64 0.5.8-2.el6       rhel 
>     PackageKit-yum.x86_64 0.5.8-2.el6        rhel 
>     PackageKit-yum-plugin.x86_64 0.5.8-2.el6 rhel 
>     glibc.x86_64 2.11.90-20.el6              rhel 
>     glibc-common.x86_64 2.10.90-22           rhel 
>     kernel.x86_64 2.6.31-14.el6              rhel 
>     kernel-firmware.noarch 2.6.31-14.el6     rhel 
>     rpm.x86_64 4.7.1-5.el6                   rhel 
>     rpm-libs.x86_64 4.7.1-5.el6              rhel 
>     rpm-python.x86_64 4.7.1-5.el6            rhel 
>     udev.x86_64 147-2.15.el6                 rhel 
>     yum.noarch 3.2.24-4.el6                  rhel 
>     
> 
> The packages in the above output are listed as having updates available. The first package in the list is **PackageKit**, the graphical package manager. The line in the example output tells us:
> 
> *   **PackageKit** — the name of the package 
> *   **x86_64** — the CPU architecture the package was built for 
> *   **0.5.8** — the version of the updated package to be installed 
> *   **rhel** — the repository in which the updated package is located. 
> 
> The output also shows us that we can update the kernel (the kernel package), Yum and RPM themselves (the yum and rpm packages), as well as their dependencies (such as the kernel-firmware, rpm-libs, and rpm-python packages), all using **yum**.

Here is the actual update process:

> **5.1.2. Updating Packages**  
> You can choose to update a single package, multiple packages, or all packages at once. If any dependencies of the package (or packages) you update have updates available themselves, then they are updated too.
> 
> **Updating a Single Package**  
> To update a single package, run the following command as **root**:
> 
>     yum update package_name
>     
> 
> For example, to update the **udev** package, type:
> 
>     ~]# yum update udev
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Setting up Update Process
>     Resolving Dependencies
>     --> Running transaction check
>     ---> Package udev.x86_64 0:147-2.15.el6 set to be updated
>     --> Finished Dependency Resolution
>     
>     Dependencies Resolved
>     
>     ===========================================================================
>      Package       Arch            Version                 Repository     Size
>     ===========================================================================
>     Updating:
>      udev          x86_64          147-2.15.el6            rhel          337 k
>     
>     Transaction Summary
>     ===========================================================================
>     Install       0 Package(s)
>     Upgrade       1 Package(s)
>     
>     Total download size: 337 k
>     Is this ok [y/N]:
>     
> 
> **Updating All Packages and Their Dependencies**  
> To update all packages and their dependencies, simply enter **yum update** (without any arguments):
> 
>     yum update
>     

### YUM Searching

> **5.2. Packages and Package Groups**  
> **5.2.1. Searching Packages**  
> You can search all RPM package names, descriptions and summaries by using the following command:
> 
>     yum search term…
>     
> 
> This command displays the list of matches for each term. For example, to list all packages that match “meld” or “kompare”, type:
> 
>     ~]# yum search meld kompare
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     ============================ Matched: kompare =============================
>     kdesdk.x86_64 : The KDE Software Development Kit (SDK)
>     Warning: No matches found for: meld
>     
> 
> The yum search command is useful for searching for packages you do not know the name of, but for which you know a related term.
> 
> **5.2.2. Listing Packages**  
> **yum list** and related commands provide information about packages, package groups, and repositories. All of Yum's list commands allow you to filter the results by appending one or more glob expressions as arguments. Glob expressions are normal strings of characters which contain one or more of the wildcard characters * (which expands to match any character multiple times) and ? (which expands to match any one character)
> 
> **yum list glob_expression…** - Lists information on installed and available packages matching all glob expressions. Packages with various ABRT addons and plug-ins either begin with “abrt-addon-”, or “abrt-plugin-”. To list these packages, type the following at a shell prompt:
> 
>     ~]# yum list abrt-addon\* abrt-plugin\*
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Installed Packages
>     abrt-addon-ccpp.x86_64                        1.0.7-5.el6             @rhel
>     abrt-addon-kerneloops.x86_64                  1.0.7-5.el6             @rhel
>     abrt-addon-python.x86_64                      1.0.7-5.el6             @rhel
>     abrt-plugin-bugzilla.x86_64                   1.0.7-5.el6             @rhel
>     abrt-plugin-logger.x86_64                     1.0.7-5.el6             @rhel
>     abrt-plugin-sosreport.x86_64                  1.0.7-5.el6             @rhel
>     abrt-plugin-ticketuploader.x86_64             1.0.7-5.el6             @rhel
>     
> 
> **yum list all** - Lists all installed and available packages.  
> **yum list installed** - Lists all packages installed on your system. The rightmost column in the output lists the repository from which the package was retrieved. To list all installed packages that begin with “krb” followed by exactly one character and a hyphen, type:
> 
>     ~]# yum list installed "krb?-*"
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Installed Packages
>     krb5-libs.x86_64                         1.8.1-3.el6                  @rhel
>     krb5-workstation.x86_64                  1.8.1-3.el6                  @rhel
>     
> 
> **yum list available** - Lists all available packages in all enabled repositories. To list all available packages with names that contain “gstreamer” and then “plugin”, run the following command:
> 
>     ~]# yum list available gstreamer\*plugin\*
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Available Packages
>     gstreamer-plugins-bad-free.i686               0.10.17-4.el6            rhel
>     gstreamer-plugins-base.i686                   0.10.26-1.el6            rhel
>     gstreamer-plugins-base-devel.i686             0.10.26-1.el6            rhel
>     gstreamer-plugins-base-devel.x86_64           0.10.26-1.el6            rhel
>     gstreamer-plugins-good.i686                   0.10.18-1.el6            rhel
>     
> 
> **yum grouplist** - Lists all package groups.  
> **yum repolist** Lists the repository ID, name, and number of packages it provides for each enabled repository.
> 
> **5.2.3. Displaying Package Information**  
> To display information about one or more packages (glob expressions are valid here as well), use the following command:
> 
>     yum info package_name…
>     
> 
> For example, to display information about the abrt package, type:
> 
>     ~]# yum info abrt
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Installed Packages
>     Name       : abrt
>     Arch       : x86_64
>     Version    : 1.0.7
>     Release    : 5.el6
>     Size       : 578 k
>     Repo       : installed
>     From repo  : rhel
>     Summary    : Automatic bug detection and reporting tool
>     URL        : https://fedorahosted.org/abrt/
>     License    : GPLv2+
>     Description: abrt is a tool to help users to detect defects in applications
>                : and to create a bug report with all informations needed by
>                : maintainer to fix it. It uses plugin system to extend its
>                : functionality.
>     

### YUM Installing

> **5.2.4 . Installing Packages**  
> Yum allows you to install both a single package and multiple packages, as well as a package group of your choice. To install a single package and all of its non-installed dependencies, enter a command in the following form:
> 
>     yum install package_name
>     
> 
> If you are installing packages on a multilib system, such as an AMD64 or Intel64 machine, you can specify the architecture of the package (as long as it is available in an enabled repository) by appending .arch to the package name. For example, to install the sqlite2 package for i586, type:
> 
>     ~]# yum install sqlite2.i586
>     
> 
> You can use glob expressions to quickly install multiple similarly-named packages:
> 
>     ~]# yum install audacious-plugins-\*
>     
> 
> In addition to package names and glob expressions, you can also provide file names to yum install. If you know the name of the binary you want to install, but not its package name, you can give yum install the path name:
> 
>     ~]# yum install /usr/sbin/named
>     
> 
> **yum** then searches through its package lists, finds the package which provides **/usr/sbin/named**, if any, and prompts you as to whether you want to install it. If you know you want to install the package that contains the named binary, but you do not know in which bin or sbin directory is the file installed, use the **yum provides** command with a glob expression:
> 
>     ~]# yum provides "*bin/named" 
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager 
>     Updating Red Hat repositories. 
>     INFO:rhsm-app.repolib:repos updated: 0 
>     32:bind-9.7.0-4.P1.el6.x86_64 : The Berkeley Internet Name Domain (BIND) : DNS (Domain Name System) server 
>     Repo : rhel 
>     Matched from: 
>     Filename : /usr/sbin/named
>     
> 
> **yum provides "*/file_name"** is a common and useful trick to find the package(s) that contain **file_name**.
> 
> **Installing a Package Group**  
> A package group is similar to a package: it is not useful by itself, but installing one pulls a group of dependent packages that serve a common purpose. A package group has a name and a groupid. The **yum grouplist -v** command lists the names of all package groups, and, next to each of them, their &#42;groupid&#42; in parentheses. The &#42;groupid&#42; is always the term in the last pair of parentheses, such as **kdedesktop** in the following example:
> 
>     ~]# yum -v grouplist kde\*
>     Loading "product-id" plugin
>     Loading "refresh-packagekit" plugin
>     Loading "subscription-manager" plugin
>     Updating Red Hat repositories.
>     INFO:rhsm-app.repolib:repos updated: 0
>     Config time: 0.123
>     Yum Version: 3.2.29
>     Setting up Group Process
>     Looking for repo options for [rhel]
>     rpmdb time: 0.001
>     group time: 1.291
>     Available Groups:
>       KDE Desktop (kde-desktop)
>     Done
>     
> 
> You can install a package group by passing its full group name (without the groupid part) to **groupinstall**:
> 
>     yum groupinstall group_name
>     
> 
> you can also install by groupid:
> 
>     yum groupinstall groupid
>     
> 
> You can even pass the groupid (or quoted name) to the **install** command if you prepend it with an @-symbol (which tells yum that you want to perform a **groupinstall**):
> 
>     yum install @group
>     
> 
> For example, the following are alternative but equivalent ways of installing the **KDE Desktop** group:
> 
>     ~]# yum groupinstall "KDE Desktop" 
>     ~]# yum groupinstall kde-desktop 
>     ~]# yum install @kde-desktop
>     

### YUM Remove

> **5.2.5. Removing Packages**  
> Similarly to package installation, Yum allows you to uninstall (remove in RPM and Yum terminology) both individual packages and a package group.
> 
> **Removing Individual Packages**  
> To uninstall a particular package, as well as any packages that depend on it, run the following command as root:
> 
>     yum remove package_name…
>     
> 
> Similar to **install**, **remove** can take these arguments:
> 
> *   package names 
> *   glob expressions 
> *   file lists 
> *   package provides
> 
> **Removing a Package Group**  
> You can remove a package group using syntax congruent with the install syntax:
> 
>     yum groupremove group 
>     yum remove @group
>     
> 
> The following are alternative but equivalent ways of removing the **KDE Desktop** group:
> 
>     ~]# yum groupremove "KDE Desktop" 
>     ~]# yum groupremove kde-desktop 
>     ~]# yum remove @kde-desktop
>     

### YUM History

> **5.2.6. Working with Transaction History**  
> The **yum history** command allows users to review information about a timeline of Yum transactions, the dates and times they occurred, the number of packages affected, whether transactions succeededor were aborted, and if the RPM database was changed between transactions. Additionally, this command can be used to undo or redo certain transactions.
> 
> **Listing Transactions**  
> To display a list of twenty most recent transactions, as root, either run yum history with no additional arguments, or type the following at a shell prompt:
> 
>     yum history list
>     
> 
> To display all transactions, add the all keyword:
> 
>     yum history list all
>     
> 
> To display only transactions in a given range, use the command in the following form:
> 
>     yum history list start_id..end_id
>     
> 
> You can also list only transactions regarding a particular package or packages. To do so, use the command with a package name or a glob expression:
> 
>     yum history list glob_expression…
>     
> 
> For example, the list of first five transactions may look as follows:
> 
>     ~]# yum history list 1..5
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     ID     | Login user               | Date and time    | Action(s)      | Altered
>     -------------------------------------------------------------------------------
>          5 | Jaromir ... <jhradilek>  | 2011-07-29 15:33 | Install        |    1
>          4 | Jaromir ... </jhradilek><jhradilek>  | 2011-07-21 15:10 | Install        |    1
>          3 | Jaromir ... </jhradilek><jhradilek>  | 2011-07-16 15:27 | I, U           |   73
>          2 | System <unset>           | 2011-07-16 15:19 | Update         |    1
>          1 | System </unset><unset>           | 2011-07-16 14:38 | Install        | 1106
>     history list
>     
> 
> All forms of the yum history list command produce tabular output with each row consisting of the following columns:
> 
> *   **ID** — an integer value that identifies a particular transaction. 
> *   **Login user** — the name of the user whose login session was used to initiate a transaction. This information is typically presented in the Full Name form. For transactions that were not issued by a user (such as an automatic system update), System is used instead. 
> *   **Date and time** — the date and time when a transaction was issued. 
> *   **Action(s)** — a list of actions that were performed during a transaction 
> *   **Altered** — the number of packages that were affected by a transaction 
> 
> Yum also allows you to display a summary of all past transactions. To do so, run the command in the following form as root:
> 
>     yum history summary
>     
> 
> To display only transactions in a given range, type:
> 
>     yum history summary start_id..end_id
>     
> 
> Similarly to the yum history list command, you can also display a summary of transactions regarding a certain package or packages by supplying a package name or a glob expression:
> 
>     yum history summary glob_expression…
>     
> 
> For instance, a summary of the transaction history displayed above would look like the following:
> 
>     ~]# yum history summary 1..5
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Login user                 | Time                | Action(s)        | Altered 
>     -------------------------------------------------------------------------------
>     Jaromir ... <jhradilek>    | Last day            | Install          |        1
>     Jaromir ... </jhradilek><jhradilek>    | Last week           | Install          |        1
>     Jaromir ... </jhradilek><jhradilek>    | Last 2 weeks        | I, U             |       73
>     System <unset>             | Last 2 weeks        | I, U             |     1107
>     history summary
>     
> 
> To list transactions from the perspective of a package, run the following command as root:
> 
>     yum history package-list glob_expression
>     
> 
> For example, to trace the history of subscription-manager and related packages, type the following at a shell prompt:
> 
>     ~]# yum history package-list subscription-manager\*
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     ID     | Action(s)      | Package
>     -------------------------------------------------------------------------------
>          3 | Updated        | subscription-manager-0.95.11-1.el6.x86_64
>          3 | Update         |                      0.95.17-1.el6_1.x86_64
>          3 | Updated        | subscription-manager-firstboot-0.95.11-1.el6.x86_64
>          3 | Update         |                                0.95.17-1.el6_1.x86_64
>          3 | Updated        | subscription-manager-gnome-0.95.11-1.el6.x86_64
>          3 | Update         |                            0.95.17-1.el6_1.x86_64
>          1 | Install        | subscription-manager-0.95.11-1.el6.x86_64
>          1 | Install        | subscription-manager-firstboot-0.95.11-1.el6.x86_64
>          1 | Install        | subscription-manager-gnome-0.95.11-1.el6.x86_64
>     history package-list
>     
> 
> In this example, three packages were installed during the initial system installation: *subscriptionmanager*, *subscription-manager-firstboot*, and *subscription-manager-gnome*. In the third transaction, all these packages were updated from version 0.95.11 to version 0.95.17.
> 
> **Examining Transactions**   
> To display the summary of a single transaction, as root, use the **yum history summary** command in the following form:
> 
>     yum history summary id
>     
> 
> To examine a particular transaction or transactions in more detail, run the following command as root:
> 
>     yum history info id
>     
> 
> The **id** argument is optional and when you omit it, **yum** automatically uses the last transaction. Note that when specifying more than one transaction, you can also use a range:
> 
>     yum history info start_id..end_id
>     
> 
> The following is sample output for two transactions, each installing one new package:
> 
>     ~]# yum history info 4..5
>     Loaded plugins: product-id, refresh-packagekit, subscription-manager
>     Transaction ID : 4..5
>     Begin time     : Thu Jul 21 15:10:46 2011
>     Begin rpmdb    : 1107:0c67c32219c199f92ed8da7572b4c6df64eacd3a
>     End time       :            15:33:15 2011 (22 minutes)
>     End rpmdb      : 1109:1171025bd9b6b5f8db30d063598f590f1c1f3242
>     User           : Jaromir Hradilek <jhradilek>
>     Return-Code    : Success
>     Command Line   : install screen
>     Command Line   : install yum-plugin-fs-snapshot
>     Transaction performed with:
>         Installed     rpm-4.8.0-16.el6.x86_64
>         Installed     yum-3.2.29-17.el6.noarch
>         Installed     yum-metadata-parser-1.1.2-16.el6.x86_64
>     Packages Altered:
>         Install screen-4.0.3-16.el6.x86_64
>         Install yum-plugin-fs-snapshot-1.1.30-6.el6.noarch
>     history info
>     
> 
> **Reverting and Repeating Transactions**  
> Apart from reviewing the transaction history, the yum history command provides means to revert or repeat a selected transaction. To revert a transaction, type the following at a shell prompt as root:
> 
>     yum history undo id
>     
> 
> To repeat a particular transaction, as root, run the following command:
> 
>     yum history redo id
>     
> 
> Both commands also accept the last keyword to undo or repeat the latest transaction.

Let's install a group, first let's check out the available groups excluding the language groups:

    [root@rhel1 ~]# yum grouplist -v | grep -v Support
    Not loading "rhnplugin" plugin, as it is disabled
    Loading "product-id" plugin
    Loading "subscription-manager" plugin
    Updating Red Hat repositories.
    Config time: 0.790
    Yum Version: 3.2.29
    Setting up Group Process
    rpmdb time: 0.006
    group time: 2.489
    Installed Groups:
       Directory Client (directory-client)
       E-mail server (mail-server)
       System administration tools (system-admin-tools)
    Available Groups:
       Additional Development (additional-devel)
       Backup Client (backup-client)
       Base (base)
       CIFS file server (cifs-file-server)
       Client management tools (client-mgmt-tools)
       Compatibility libraries (compat-libraries)
       Console internet tools (console-internet)
       Debugging Tools (debugging)
       Desktop (basic-desktop)
       Desktop Debugging and Performance Tools (desktop-debugging)
       Desktop Platform (desktop-platform)
       Desktop Platform Development (desktop-platform-devel)
       Development tools (development)
       Directory Server (directory-server)
       Eclipse (eclipse)
       Emacs (emacs)
       Enterprise Identity Server Base (identity-server)
       FCoE Storage Client (storage-client-fcoe)
       FTP server (ftp-server)
       Fonts (fonts)
       General Purpose Desktop (general-desktop)
       Graphical Administration Tools (graphical-admin-tools)
       Graphics Creation Tools (graphics)
       Hardware monitoring utilities (hardware-monitoring)
       Input Methods (input-methods)
       Internet Applications (internet-applications)
       Internet Browser (internet-browser)
       Java Platform (java-platform)
       KDE Desktop (kde-desktop)
       Large Systems Performance (large-systems)
       Legacy UNIX compatibility (legacy-unix)
       Legacy X Window System compatibility (legacy-x)
       Mainframe Access (mainframe-access)
       MySQL Database client (mysql-client)
       MySQL Database server (mysql)
       NFS file server (nfs-file-server)
       Network Infrastructure Server (network-server)
       Network Storage Server (storage-server)
       Network file system client (network-file-system-client)
       Networking Tools (network-tools)
       Office Suite and Productivity (office-suite)
       Performance Tools (performance)
       PostgreSQL Database client (postgresql-client)
       PostgreSQL Database server (postgresql)
       Printing client (print-client)
       Remote Desktop Clients (remote-desktop-clients)
       Scientific support (scientific)
       Security Tools (security-tools)
       Server Platform (server-platform)
       Server Platform Development (server-platform-devel)
       Smart card support (smart-card)
       Storage Availability Tools (storage-client-multipath)
       System Management (system-management)
       Systems Management Messaging Server support (system-management-messaging-server)
       TeX support (tex)
       Technical Writing (technical-writing)
       TurboGears application framework (turbogears)
       Virtualization (virtualization)
       Virtualization Client (virtualization-client)
       Virtualization Platform (virtualization-platform)
       Virtualization Tools (virtualization-tools)
       Web Server (web-server)
       Web Servlet Engine (web-servlet)
       Web-Based Enterprise Management (system-management-wbem)
       X Window System (x11)
       iSCSI Storage Client (storage-client-iscsi)
    Available Language Groups:
    Done
    

Let's try a simple one, **nfs-file-server**:

    [root@rhel1 ~]# yum groupinfo nfs-file-server
    Loaded plugins: product-id, subscription-manager
    Updating Red Hat repositories.
    Setting up Group Process
    Group: NFS file server
     Description: NFS file server.
     Mandatory Packages:
       nfs-utils
       nfs4-acl-tools
    

Now let's install that:

    [root@rhel1 ~]# yum groupinstall nfs-file-server
    Loaded plugins: product-id, subscription-manager
    Updating Red Hat repositories.
    Setting up Group Process
    Resolving Dependencies
    --> Running transaction check
    ---> Package nfs-utils.i686 1:1.2.3-7.el6 will be installed
    --> Processing Dependency: nfs-utils-lib >= 1.1.0-3 for package: 1:nfs-utils-1.2.3-7.el6.i686
    --> Processing Dependency: libevent for package: 1:nfs-utils-1.2.3-7.el6.i686
    --> Processing Dependency: libnfsidmap.so.0 for package: 1:nfs-utils-1.2.3-7.el6.i686
    --> Processing Dependency: libevent-1.4.so.2 for package: 1:nfs-utils-1.2.3-7.el6.i686
    ---> Package nfs4-acl-tools.i686 0:0.3.3-5.el6 will be installed
    --> Running transaction check
    ---> Package libevent.i686 0:1.4.13-1.el6 will be installed
    ---> Package nfs-utils-lib.i686 0:1.1.5-3.el6 will be installed
    --> Finished Dependency Resolution
    
    Dependencies Resolved
    
    =======================================================================================================================================
     Package                              Arch                       Version                               Repository                 Size
    =======================================================================================================================================
    Installing:
     nfs-utils                            i686                       1:1.2.3-7.el6                         dvd                       304 k
     nfs4-acl-tools                       i686                       0.3.3-5.el6                           dvd                        43 k
    Installing for dependencies:
     libevent                             i686                       1.4.13-1.el6                          dvd                        67 k
     nfs-utils-lib                        i686                       1.1.5-3.el6                           dvd                        60 k
    Transaction Summary
    =======================================================================================================================================
    Install       4 Package(s)
    Total download size: 473 k
    Installed size: 1.2 M
    Is this ok [y/N]: y
    Downloading Packages:
    ---------------------------------------------------------------------------------------------------------------------------------------
    Total                                                                                                  1.8 MB/s | 473 kB     00:00     
    Running rpm_check_debug
    Running Transaction Test
    Transaction Test Succeeded
    Running Transaction
      Installing : libevent-1.4.13-1.el6.i686                                                                                          1/4 
      Installing : nfs-utils-lib-1.1.5-3.el6.i686                                                                                      2/4 
      Installing : 1:nfs-utils-1.2.3-7.el6.i686                                                                                        3/4 
      Installing : nfs4-acl-tools-0.3.3-5.el6.i686                                                                                     4/4 
    duration: 1174(ms)
    Installed products updated.
    Installed:
      nfs-utils.i686 1:1.2.3-7.el6                                    nfs4-acl-tools.i686 0:0.3.3-5.el6                                   
    Dependency Installed:
      libevent.i686 0:1.4.13-1.el6                                     nfs-utils-lib.i686 0:1.1.5-3.el6                                    
    Complete!
    

Now let's check out the yum history:

    [root@rhel1 ~]# yum history list
    Loaded plugins: product-id, subscription-manager
    Updating Red Hat repositories.
    ID     | Login user               | Date and time    | Action(s)      | Altered
    -------------------------------------------------------------------------------
        12 | root <root>              | 2013-03-02 10:27 | Install        |    4   
        11 | root </root><root>       | 2013-02-09 05:23 | Install        |    1   
        10 | root </root><root>       | 2013-02-09 02:24 | Install        |    5   
         9 | root </root><root>       | 2013-02-08 02:42 | Install        |    6  
         8 | root </root><root>       | 2013-02-07 12:57 | Install        |   22 > 
         7 | root </root><root>       | 2013-02-06 12:58 | Install        |    1   
         6 | root </root><root>       | 2013-02-06 12:24 | Install        |    3   
         5 | root </root><root>       | 2013-02-06 10:34 | Erase          |    7   
         4 | root </root><root>       | 2013-02-06 09:56 | Install        |    7   
         3 | root </root><root>       | 2013-02-06 08:48 | Reinstall      |    1  <>          
         2 | root </root><root>       | 2013-02-06 04:36 | Install        |    1 > 
         1 | System <unset>           | 2013-02-04 04:22 | Install        |  229   
    history list
    

Let's check out the last entry:

    [root@rhel1 ~]# yum history info 12
    Loaded plugins: product-id, subscription-manager
    Updating Red Hat repositories.
    Transaction ID : 12
    Begin time     : Sat Mar  2 10:27:03 2013
    Begin rpmdb    : 270:c869d46628b6a1c1a64aa23fc9c3f56c490d53f7
    End time       :            10:27:16 2013 (13 seconds)
    End rpmdb      : 274:b2a237f77c64214f3a448209de595e885d2c7513
    User           : root <root>
    Return-Code    : Success
    Command Line   : groupinstall nfs-file-server
    Transaction performed with:
        Installed     rpm-4.8.0-16.el6.i686
        Installed     subscription-manager-0.95.11-1.el6.i686
        Installed     yum-3.2.29-17.el6.noarch
        Installed     yum-metadata-parser-1.1.2-16.el6.i686
    Packages Altered:
        Dep-Install libevent-1.4.13-1.el6.i686
        Install     nfs-utils-1:1.2.3-7.el6.i686
        Dep-Install nfs-utils-lib-1.1.5-3.el6.i686
        Install     nfs4-acl-tools-0.3.3-5.el6.i686
    history info
    

We can see the whole transaction. Now let's undo that transaction. First let's see how many RPMs are currently installed on the system:

    [root@rhel1 ~]# rpm -qa | wc -l
    276
    

From the above output we know that we installed 4 packaged for the **nfs-file-server** group. If we undo that transaction we should see 272 RPMs installed. So let's give it a try:

    [root@rhel1 ~]# yum history undo 12
    Loaded plugins: product-id, subscription-manager
    Updating Red Hat repositories.
    Undoing transaction 12, from Sat Mar  2 10:27:03 2013
        Dep-Install libevent-1.4.13-1.el6.i686
        Install     nfs-utils-1:1.2.3-7.el6.i686
        Dep-Install nfs-utils-lib-1.1.5-3.el6.i686
        Install     nfs4-acl-tools-0.3.3-5.el6.i686
    Resolving Dependencies
    --> Running transaction check
    ---> Package libevent.i686 0:1.4.13-1.el6 will be erased
    ---> Package nfs-utils.i686 1:1.2.3-7.el6 will be erased
    ---> Package nfs-utils-lib.i686 0:1.1.5-3.el6 will be erased
    ---> Package nfs4-acl-tools.i686 0:0.3.3-5.el6 will be erased
    --> Finished Dependency Resolution
    Dependencies Resolved
    =======================================================================================================================================
     Package                              Arch                       Version                              Repository                  Size
    =======================================================================================================================================
    Removing:
     libevent                             i686                       1.4.13-1.el6                         @dvd                       226 k
     nfs-utils                            i686                       1:1.2.3-7.el6                        @dvd                       778 k
     nfs-utils-lib                        i686                       1.1.5-3.el6                          @dvd                       122 k
     nfs4-acl-tools                       i686                       0.3.3-5.el6                          @dvd                        99 k
    Transaction Summary
    =======================================================================================================================================
    Remove        4 Package(s)
    Installed size: 1.2 M
    Is this ok [y/N]: y
    Downloading Packages:
    Running rpm_check_debug
    Running Transaction Test
    Transaction Test Succeeded
    Running Transaction
      Erasing    : nfs-utils-lib-1.1.5-3.el6.i686                                                                                      1/4 
      Erasing    : 1:nfs-utils-1.2.3-7.el6.i686                                                                                        2/4 
      Erasing    : libevent-1.4.13-1.el6.i686                                                                                          3/4 
      Erasing    : nfs4-acl-tools-0.3.3-5.el6.i686                                                                                     4/4 
    duration: 243(ms)
    Installed products updated.
    Removed:
      libevent.i686 0:1.4.13-1.el6   nfs-utils.i686 1:1.2.3-7.el6   nfs-utils-lib.i686 0:1.1.5-3.el6   nfs4-acl-tools.i686 0:0.3.3-5.el6  
    Complete!
    

Now for the count of the packages after undoing the install:

    [root@rhel1 ~]# rpm -qa | wc -l
    272 
    

And that looks perfect.

### Createrepo

Now let's get to creating a custom repository, I had an example of how to create one from the Install DVD in <a href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-3-disks-and-partitioning/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-3-disks-and-partitioning/']);">Chapter 3</a>. But what if we wanted to create one with custom packages. From the Deployment guide:

> **5.3.6. Creating a Yum Repository**   
> To set up a Yum repository, follow these steps:
> 
> 1.  Install the createrepo package:
>     
>         yum install createrepo
>         
> 
> 2.  Copy all of the packages into one directory, such as /**mnt/local_repo**
> 
> 3.  Run the createrepo -database command on that directory:
>     
>         ~]# createrepo --database /mnt/local_repo
>         
> 
> This will create the necessary metadata for your Yum repository, as well as the sqlite database for speeding up yum operations.

So let's create a repository called "my_repo" and just put the package **tcsh** there and then setup a repo from that:

    [root@rhel1 ~]# mkdir my_repo
    [root@rhel1 ~]# cp repo/Packages/tcsh-6.17-12.el6.i686.rpm my_repo/.
    

Now let's install the **createrepo** package and create a database from the 'my_repro' directory:

    [root@rhel1 ~]# yum install createrepo
    

Now for the magic:

    [root@rhel1 ~\]# createrepo -d my_repo/ 
    1/1 - tcsh-6.17-12.el6.i686.rpm 
    Saving Primary metadata 
    Saving file lists metadata 
    Saving other metadata 
    Generating sqlite DBs 
    Sqlite DBs complete
    [root@rhel1 ~]# ls my_repo/ 
    repodata tcsh-6.17-12.el6.i686.rpm 
    

Now we see a **repodata** folder inside the repository directory. You can also add new files to the repository directory and update the repository database:

    [root@rhel1 ~]# cp repo/Packages/aspell-0.60.6-12.el6.i686.rpm my_repo/. 
    [root@rhel1 ~]# createrepo --update my_repo/ 
    2/2 - tcsh-6.17-12.el6.i686.rpm 
    Saving Primary metadata 
    Saving file lists metadata 
    Saving other metadata
    

Now to add this repository to yum. From the guide:

> **5.3.2. Setting [repository] Options**  
> The **[repository]** sections, where repository is a unique repository ID such as **my&#95;personal&#95;repo** (spaces are not permitted), allow you to define individual Yum repositories. The following is a bare-minimum example of the form a **[repository]** section takes:
> 
>     [repository]
>     name=repository_name
>     baseurl=repository_url
>     
> 
> Every **[repository]** section must contain the following directives:
> 
> *   **name=repository_name** - …where **repository_name** is a human-readable string describing the repository. 
> *   **baseurl=repository_url**- …where **repository_url** is a URL to the directory where the repodata directory of a repository is located: 
>     *   If the repository is available over HTTP, use: **http://path/to/repo**
>     *   If the repository is available over FTP, use: **ftp://path/to/repo**
>     *   If the repository is local to the machine, use: **file:///path/to/local/repo**
>     *   If a specific online repository requires basic HTTP authentication, you can specify your username and password by prepending it to the URL as **username:password@link**. For example, if a repository on http://www.example.com/repo/ requires a username of “user” and a password of “password”, then the **baseurl** link could be specified as **http://user:password@www.example.com/repo/**. Usually this URL is an HTTP link, such as: `baseurl=http://path/to/repo/releases/$releasever/server/$basearch/os/`
> 
> Another useful **[repository]** directive is the following:
> 
> *   **enabled=value** - …where **value** is one of: 
>     *   **O** — Do not include this repository as a package source when performing updates and installs. This is an easy way of quickly turning repositories on and off, which is useful when you desire a single package from a repository that you do not want to enable for updates or installs. 
>     *   **1** — Include this repository as a package source. 
>         Turning repositories on and off can also be performed by passing either the -enablerepo=repo&#95;name or -disablerepo=repo&#95;name option to yum, or through the Add/Remove Software window of the PackageKit utility</li> </ul> </li> </ul> 
>         Many more **[repository]** options exist. For a complete list, refer to the **[repository]** **OPTIONS** section of the **yum.conf(5)** manual page.</blockquote> 
>         
>         So let's create a file called "**my_repo.repo**" under **/etc/yum.repos.d/** and have the following content:
>         
>             [root@rhel1 ~]# cat /etc/yum.repos.d/my_repo.repo 
>             [my_repo] 
>             baseurl=file:///root/my_repo 
>             name=my_repo
>             
>         
>         Now checking the **repolist**, we see this:
>         
>             [root@rhel1 ~]# yum repolist
>             Loaded plugins: product-id, subscription-manager
>             Updating Red Hat repositories.
>             dvd                           | 4.0 kB     00:00 ... 
>             my_repo                       | 1.3 kB     00:00 ... 
>             repo id                 repo name          status
>             dvd                     rhel_dvd           2,977
>             my_repo                 my_repo            2
>             repolist: 2,979
>             
>         
>         We can see that we have 2 packages in "my_repo" repository. Since the same package exists in two repositories, we have to disable one like so:
>         
>             [root@rhel1 ~]# yum list tcsh --disablerepo=dvd
>             Loaded plugins: product-id, subscription-manager
>             Updating Red Hat repositories.
>             Installed Packages
>             tcsh.i686                6.17-12.el6    @my_repo
>             
>         
>         Now to actually install we can do this:
>         
>             [root@rhel1 ~]# yum install tcsh --disablerepo=dvd
>             
>         
>         And that is how we can create our own YUM repository.
>         
>         ## RPMBuild
>         
>         Now let's see how we can create our own RPM package. There is great Fedora link about this: "<a href="http://fedoraproject.org/wiki/How_to_create_an_RPM_package" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://fedoraproject.org/wiki/How_to_create_an_RPM_package']);">How to create an RPM package</a>". From that page:
>         
>         > **Preparing your system**  
>         > Before you create RPM packages on Fedora, you need to install some core development tools and set up the account(s) you will use:
>         > 
>         >     yum install rpm-build rpmdevtools
>         >     
>         > 
>         > You can create a dummy user specifically for creating RPM packages so that a build process gone wrong can't trash your files or send your private keys to the world. Create a new user named **makerpm**, add the user to the '**mock**' group, set a password, and login as that user:
>         > 
>         >     # /usr/sbin/useradd makerpm 
>         >     # usermod -a -G mock makerpm 
>         >     # passwd makerpm
>         >     
>         
>         ### RPMBuild Structure
>         
>         > Once you're logged in as the build/dummy user, create the required directory structure in your home directory by executing:
>         > 
>         >     $ rpmdev-setuptree
>         >     
>         > 
>         > The **rpmdev-setuptree** program will create the *~/rpmbuild* directory and a set of subdirectories (e.g. SPECS and BUILD), which you will use for creating your packages. The *~/.rpmmacros* file is also created, which can be used for setting various options.
>         > 
>         > **The basics of building RPM packages**  
>         > To create an RPM package, you will need to create a ".spec" text file that provides information about the software being packaged. You then run the **rpmbuild** command on the SPEC file, which will go through a series of steps to produce your packages. Normally, you should place your original (pristine) sources, such as *.tar.gz* files from the original developers, into the **~/rpmbuild/SOURCES** directory. Place your .spec file in the **~/rpmbuild/SPECS** directory and name it "NAME.spec", where NAME is the base name of the package. To create both binary and source packages, change directory to **~/rpmbuild/SPECS** and run:
>         > 
>         >     $ rpmbuild -ba NAME.spec
>         >     
>         > 
>         > When invoked this way, **rpmbuild** will read the .spec file and go through in order the stages listed below. Names beginning with % are predefined macros (see the next table down). <a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/rpmbuild_stages.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/02/rpmbuild_stages.png']);"><img class="alignnone size-full wp-image-6169" alt="rpmbuild stages RHCSA and RHCE Chapter 6 Package Management" src="http://virtuallyhyper.com/wp-content/uploads/2013/02/rpmbuild_stages.png" width="1056" height="330" title="RHCSA and RHCE Chapter 6 Package Management" /></a>  
>         > As you can tell, certain directories have certain purposes in **rpmbuild**. These are:   
>         > <a href="http://virtuallyhyper.com/wp-content/uploads/2013/02/rpmbuild_directories.png</unset></root></jhradilek></unset></jhradilek></unset></jhradilek></twaugh></rel></twaugh></http:>"><img class=" onclick="javascript:\_gaq.push(['\_trackEvent','outbound-article','']);"alignnone size-full wp-image-6170" alt="rpmbuild directories RHCSA and RHCE Chapter 6 Package Management" src="http://virtuallyhyper.com/wp-content/uploads/2013/02/rpmbuild_directories.png" width="833" height="169" title="RHCSA and RHCE Chapter 6 Package Management" /></a>  
>         > If a stage fails, look at the output to see why it falied and change the .spec file (or other input) as needed.
>         
>         ### RPMBuild SPEC File
>         
>         > **Creating a SPEC file**  
>         > You now need to create a SPEC file in the **~/rpmbuild/SPECS** directory. You should name it after the program name (e.g. "program.spec"). Use the archive name or the name advocated by the software author where you can. **SPEC templates** When you're creating a SPEC file for the first time, vim or emacs will automatically create a template for you:
>         > 
>         >     $ cd ~/rpmbuild/SPECS 
>         >     $ vim program.spec
>         >     
>         > 
>         > Here's an example of what that template will look like:
>         > 
>         >     Name:     
>         >     Version:  
>         >     Release:  1%{?dist}
>         >     Summary:  
>         >     Group:        
>         >     License:  
>         >     URL:      
>         >     Source0:  
>         >     BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
>         >     
>         >     BuildRequires:    
>         >     Requires: 
>         >     
>         >     %description
>         >     
>         >     %prep
>         >     %setup -q
>         >     
>         >     %build
>         >     %configure
>         >     make %{?_smp_mflags}
>         >     
>         >     %install
>         >     rm -rf %{buildroot}
>         >     make install DESTDIR=%{buildroot}
>         >     
>         >     %clean
>         >     rm -rf %{buildroot}
>         >     
>         >     %files
>         >     %defattr(-,root,root,-)
>         >     %doc
>         >     
>         >     %changelog
>         >     
>         > 
>         > You can use $RPM&#95;BUILD&#95;ROOT instead of %{buildroot}. Both are acceptable, but just be consistent. You may also use the **rpmdev-newspec** command to create a SPEC file for you. **rpmdev-newspec NAME-OF-NEW-PACKAGE** can create an initial SPEC file for a new package, tailored to various types of packages. It will guess what kind of template to use based on the package name, or you can specify a particular template. See **/etc/rpmdevtools/spectemplate-*.spec** for available templates, and see **rpmdev-newspec -help** for more information. For example, to create a new SPEC file for a python module:
>         > 
>         >     cd ~/rpmbuild/SPECS 
>         >     rpmdev-newspec python-antigravity 
>         >     vi python-antigravity.spec
>         >     
>         > 
>         > **SPEC example**  
>         > Here's a simple example showing a Fedora 16 SPEC file for the eject program:
>         > 
>         >     Summary:            A program that ejects removable media using software control
>         >     Name:               eject
>         >     Version:            2.1.5
>         >     Release:            21%{?dist}
>         >     License:            GPLv2+
>         >     Group:              System Environment/Base
>         >     Source:             %{name}-%{version}.tar.gz
>         >     Patch1:             eject-2.1.1-verbose.patch
>         >     Patch2:             eject-timeout.patch
>         >     Patch3:             eject-2.1.5-opendevice.patch
>         >     Patch4:             eject-2.1.5-spaces.patch
>         >     Patch5:             eject-2.1.5-lock.patch
>         >     Patch6:             eject-2.1.5-umount.patch
>         >     URL:                
>         >     ExcludeArch:        s390 s390x
>         >     BuildRequires:      gettext
>         >     BuildRequires:      libtool
>         >     
>         >     %description
>         >     The eject program allows the user to eject removable media (typically
>         >     CD-ROMs, floppy disks or Iomega Jaz or Zip disks) using software
>         >     control. Eject can also control some multi-disk CD changers and even
>         >     some devices' auto-eject features.
>         >     
>         >     Install eject if you'd like to eject removable media using software
>         >     control.
>         >     
>         >     %prep
>         >     %setup -q -n %{name}
>         >     %patch1 -p1
>         >     %patch2 -p1
>         >     %patch3 -p1
>         >     %patch4 -p1
>         >     %patch5 -p1
>         >     %patch6 -p1
>         >     
>         >     %build
>         >     %configure
>         >     make %{?_smp_mflags}
>         >     
>         >     %install
>         >     make DESTDIR=%{buildroot} install
>         >     
>         >     install -m 755 -d %{buildroot}/%{_sbindir}
>         >     ln -s ../bin/eject %{buildroot}/%{_sbindir}
>         >     
>         >     %find_lang %{name}
>         >     
>         >     %files -f %{name}.lang
>         >     %doc README TODO COPYING ChangeLog
>         >     %{_bindir}/*
>         >     %{_sbindir}/*
>         >     %{_mandir}/man1/*
>         >     
>         >     %changelog
>         >     * Tue Feb 08 2011 Fedora Release Engineering <rel -eng@lists.fedoraproject.org> - 2.1.5-21
>         >     - Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
>         >     
>         >     * Fri Jul 02 2010 Kamil Dudka <kdudka '@'redhat.com> 2.1.5-20
>         >     - handle multi-partition devices with spaces in mount points properly (#608502)
>         >     
>         > 
>         > **SPEC file overview**  
>         > The major tags are listed below. Note that the macros **%{name}**, **%{version}** and **%{release}** can be used to refer to the Name, Version and Release tags respectively. When you change the tag, the macros automatically update to use the new value.
>         > 
>         > *   **Name:** - The (base) name of the package, which should match the SPEC file name. 
>         > *   **Version:** - The upstream version number.If the version contains tags that are non-numeric (contains tags that are not numbers), you may need to include the additional non-numeric characters in the Release tag. If upstream uses full dates to distinguish versions, consider using version numbers of the form yy.mm&#91;dd&#93; (e.g. 2008-05-01 becomes 8.05). 
>         > *   **Release:** - The initial value should normally be 1%{?dist}. Increment the number every time you release a new package for the same version of software. When a new upstream version is released, change the Version tag to match and reset the Release number to 1. 
>         > *   **Summary:** - A brief, one-line summary of the package. Use American English. Do not end in a period. 
>         > *   **Group:** - This needs to be a pre-existing group, like "Applications/Engineering"; run "**less /usr/share/doc/rpm-*/GROUPS**" to see the complete list. Use the group "Documentation" for any sub-packages (e.g. kernel-doc) containing documentation. Note: This tag is deprecated since Fedora 17. 
>         > *   **License:** - The license, which must be an open source software license. Do not use the old Copyright tag. Use a standard abbreviation (e.g. "GPLv2+") and be specific (e.g. use "GPLv2+" for GPL version 2 or greater instead of just "GPL" or "GPLv2" where it's true). You can list multiple licenses by combining them with "and" and "or" (e.g. "GPLv2 and BSD"). 
>         > *   **URL:** - The full URL for more information about the program (e.g. the project website). Note: This is not where the original source code came from which is meant for the Source0 tag below. 
>         > *   **Source0:** - The full URL for the compressed archive containing the (original) pristine source code, as upstream released it. "Source" is synonymous with "Source0". If you give a full URL (and you should), its basename will be used when looking in the SOURCES directory. If possible, embed %{name} and %{version}, so that changes to either will go to the right place. Preserve timestamps when downloading source files. If there is more than one source, name them Source1, Source2 and so on. If you're adding whole new files in addition to the pristine sources, list them as sources after the pristine sources. A copy of each of these sources will be included in any SRPM you create, unless you specifically direct otherwise. 
>         > *   **Patch0:** - The name of the first patch to apply to the source code. If you need to patch the files after they've been uncompressed, you should edit the files and save their differences as a "patch" file in your **~/rpmbuild/SOURCES** directory. Patches should make only one logical change each, so it's quite possible to have multiple patch files. 
>         > *   **BuildArch:** - If you're packaging files that are architecture-independent (e.g. shell scripts, data files), then add "BuildArch: noarch". The architecture for the binary RPM will then be "noarch". 
>         > *   **BuildRoot:** - This is where files will be "installed" during the **%install** process (after the **%build** process). This is now redundant in Fedora and is only needed for EPEL5. By default, the build root is placed in "**%{_topdir}/BUILDROOT/**". 
>         > *   **BuildRequires:** - A comma-separated list of packages required for building (compiling) the program. This field can be (and is commonly) repeated on multiple lines. These dependencies are not automatically determined, so you need to include everything needed to build the program. Some common packages can be omitted, such as gcc. You can specify a minimum version if necessary (e.g. "ocaml >= 3.08"). If you need the file /EGGS, determine the package that owns it by running "**rpm -qf /EGGS**". If you need the program EGGS, determine the package that owns it by running "**rpm -qf &#96;which EGGS&#96;**". Keep dependencies to a minimum (e.g. use sed instead of perl if you don't really need perl's abilities), but beware that some applications permanently disable functions if the associated dependency is not present; in those cases you may need to include the additional packages. The auto-buildrequires package may be helpful. 
>         > *   **Requires:** - A comma-separate list of packages that are required when the program is installed. Note that the **BuildRequires** tag lists what is required to build the binary RPM, while the Requires tag lists what is required when installing/running the program; a package may be in one list or in both. In many cases, rpmbuild automatically detects dependencies so the Requires tag is not always necessary. However, you may wish to highlight some specific packages as being required, or they may not be automatically detected. 
>         > *   **%description:** - A longer, multi-line description of the program. Use American English. All lines must be 80 characters or less. Blank lines indicate a new paragraph. Some graphical user interface installation programs will reformat paragraphs; lines that start with whitespace will be treated as preformatted text and displayed as is, normally with a fixed-width font. 
>         > *   **%prep:** Script commands to "prepare" the program (e.g. to uncompress it) so that it will be ready for building. Typically this is just "**%setup -q**"; a common variation is "**%setup -q -n NAME**" if the source file unpacks into NAME. 
>         > *   **%build:** - Script commands to "build" the program (e.g. to compile it) and get it ready for installing. The program should come with instructions on how to do this. 
>         > *   **%check**: Script commands to "test" the program. This is run between the **%build** and **%install** procedures, so place it there if you have this section. Often it simply contains "make test" or "make check". This is separated from **%build** so that people can skip the self-test if they desire. 
>         > *   **%install:** - Script commands to "**install**" the program. The commands should copy the files from the BUILD directory **%{_builddir}** into the buildroot directory, **%{buildroot}**. 
>         > *   **%clean:** - Instructions to clean out the build root. Note that this section is now redundant in Fedora and is only necessary for EPEL. Typically this contains only: 
>         >     *   `rm -rf %{buildroot}`
>         > *   **%files:** The list of files that will be installed.
>         > *   **%changelog:** - Changes in the package. Use the format example above.
>         > *   **ExcludeArch:** If the package does not successfully compile, build or work on a particular architecture, list those architectures under this tag. You can add sections so that code will run when packages are installed or removed on the real system (as opposed to just running the **%install** script, which only does a pseudo-install to the build root). These are called "scriptlets", and they are usually used to update the running system with information from the package. RPM also supports the creation of several packages (called subpackages) from a single SPEC file, such as name-libs and name-devel packages. 
>         
>         So let's try it out. First, let's install the necessary packages:
>         
>             [root@rhel1 ~]# yum install rpm-build rpmdevtools
>             
>         
>         I know it's recommended to setup a non-root user, but since this was just for testing, I decided to just use root. First let's create a **tar** archive with just a file:
>         
>             [root@rhel1 ~]# mkdir myrpm-1.0 
>             [root@rhel1 ~]# touch myrpm-1.0/test.txt 
>             [root@rhel1 ~]# tar cpvzf myrpm-1.0.tar.gz myrpm-1.0/ 
>             myrpm-1.0/ 
>             myrpm-1.0/test.txt
>             
>         
>         Now let's create the appropriate tree structure:
>         
>             [root@rhel1 ~]# rpmdev-setuptree 
>             [root@rhel1 ~]# ls rpmbuild/ 
>             BUILD RPMS SOURCES SPECS SRPMS
>             
>         
>         Now let's copy our "source" file to the SOURCES directory:
>         
>             [root@rhel1 ~]# mv myrpm-1.0.tar.gz rpmbuild/SOURCES/.
>             
>         
>         Now let's create a template **spec** file for our rpm:
>         
>             [root@rhel1 ~]# cd rpmbuild/SPECS/ 
>             [root@rhel1 SPECS]# rpmdev-newspec myrpm.spec 
>             Skeleton specfile (minimal) has been created to "myrpm.spec".
>             
>         
>         I then edited the file with vi:
>         
>             [root@rhel1 SPECS]# vi myrpm.spec 
>             
>         
>         Here is how the *spec* file looked like after I was done:
>         
>             [root@rhel1 SPECS]# cat myrpm.spec 
>             Name:           myrpm
>             Version:        1.0
>             Release:        1%{?dist}
>             Summary:        MyRPM
>             Group:         Development/Tools 
>             License:       GPL 
>             URL:           www.example.com
>             Source0:       myrpm-1.0.tar.gz
>             BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
>             %description
>             Description of myrpm
>             %prep
>             %setup -q
>             %build
>             %install
>             rm -rf $RPM_BUILD_ROOT
>             install -d $RPM_BUILD_ROOT/opt/myrpm-1.0
>             install test.txt $RPM_BUILD_ROOT/opt/myrpm-1.0/test.txt
>             %clean
>             rm -rf $RPM_BUILD_ROOT
>             %files
>             %defattr(-,root,root,-)
>             /opt/myrpm-1.0/test.txt
>             
>         
>         That should extract the source "myrpm.tar.gz" and put it under **/opt/myrpm**. There is also another application which can check a *spec* file, it's called **rpmlint**, let's install it:
>         
>             [root@rhel1 ~]# yum install rpmlint
>             
>         
>         Now let's check out the *spec* file:
>         
>             [root@rhel1 ~]# rpmlint -v rpmbuild/SPECS/myrpm.spec
>             rpmbuild/SPECS/myrpm.spec:4: W: mixed-use-of-spaces-and-tabs (spaces: line 1, tab: line 4)
>             rpmbuild/SPECS/myrpm.spec: W: invalid-url Source0: myrpm-1.0.tar.gz
>             0 packages and 1 specfiles checked; 0 errors, 2 warnings.
>             
>         
>         I just have some formatting issues, other than that it looks good. Now let's create just the binary for the rpm (without the source rpm):
>         
>             [root@rhel1 ~]# rpmbuild -v -bb rpmbuild/SPECS/myrpm.spec
>             Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.9ekT1s
>             + umask 022
>             + cd /root/rpmbuild/BUILD
>             + cd /root/rpmbuild/BUILD
>             + rm -rf myrpm-1.0
>             + /bin/tar -xf -
>             + /usr/bin/gzip -dc /root/rpmbuild/SOURCES/myrpm-1.0.tar.gz
>             + STATUS=0
>             + '[' 0 -ne 0 ']'
>             + cd myrpm-1.0
>             + /bin/chmod -Rf a+rX,u+w,g-w,o-w .
>             + exit 0
>             Executing(%build): /bin/sh -e /var/tmp/rpm-tmp.BFgcK2
>             + umask 022
>             + cd /root/rpmbuild/BUILD
>             + cd myrpm-1.0
>             + exit 0
>             Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.CiG8YC
>             + umask 022
>             + cd /root/rpmbuild/BUILD
>             + cd myrpm-1.0
>             + rm -rf /root/rpmbuild/BUILDROOT/myrpm-1.0-1.el6.i386
>             + install -d /root/rpmbuild/BUILDROOT/myrpm-1.0-1.el6.i386/opt/myrpm-1.0
>             + install test.txt /root/rpmbuild/BUILDROOT/myrpm-1.0-1.el6.i386/opt/myrpm-1.0/test.txt
>             + /usr/lib/rpm/check-rpaths /usr/lib/rpm/check-buildroot
>             + /usr/lib/rpm/brp-compress
>             + /usr/lib/rpm/brp-strip
>             + /usr/lib/rpm/brp-strip-static-archive
>             + /usr/lib/rpm/brp-strip-comment-note
>             Processing files: myrpm-1.0-1.el6.i386
>             Requires(rpmlib): rpmlib(CompressedFileNames) < = 3.0.4-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
>             Checking for unpackaged file(s): /usr/lib/rpm/check-files /root/rpmbuild/BUILDROOT/myrpm-1.0-1.el6.i386
>             Wrote: /root/rpmbuild/RPMS/i386/myrpm-1.0-1.el6.i386.rpm
>             Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.F7pXOY
>             + umask 022
>             + cd /root/rpmbuild/BUILD
>             + cd myrpm-1.0
>             + rm -rf /root/rpmbuild/BUILDROOT/myrpm-1.0-1.el6.i386
>             + exit 0
>             
>         
>         We can see every step of the build process, and we notice that the '-1.0' suffix of the directory is very important and the build process actually depends on it. Now let's checkout our newly created rpm:
>         
>             [root@rhel1 ~]# rpm -qip rpmbuild/RPMS/i386/myrpm-1.0-1.el6.i386.rpm
>             Name        : myrpm                        Relocations: (not relocatable)
>             Version     : 1.0                               Vendor: (none)
>             Release     : 1.el6                         Build Date: Sun 03 Mar 2013 02:30:33 AM MST
>             Install Date: (not installed)               Build Host: rhel1.local.com
>             Group       : Development/Tools             Source RPM: myrpm-1.0-1.el6.src.rpm
>             Size        : 0                                License: GPL
>             Signature   : (none)
>             URL         : www.example.com
>             Summary     : MyRPM
>             Description :
>             Description of myrpm
>             
>         
>         We can also check out the permissions of the files that will be installed, by running **rpmls** on the rpm, like so:
>         
>             [root@rhel1 ~]# rpmls -l rpmbuild/RPMS/i386/myrpm-1.0-1.el6.i386.rpm
>             -rwxr-xr-x  root     root     /opt/myrpm-1.0/test.txt
>             
>         
>         That looks correct. Now let's try to install the package and make sure the files are copied appropriately:
>         
>             [root@rhel1 ~]# ls /opt
>             [root@rhel1 ~]# rpm -ivh rpmbuild/RPMS/i386/myrpm-1.0-1.el6.i386.rpm
>             Preparing...                ########################################### [100%]
>                1:myrpm                  ########################################### [100%]
>             [root@rhel1 ~]# tree /opt
>             /opt
>             └── myrpm-1.0
>                 └── test.txt
>             1 directory, 1 file
>             
>         
>         Now to confirm what files were installed by our rpm:
>         
>             [root@rhel1 ~]# rpm -ql myrpm
>             /opt/myrpm-1.0/test.txt
>             
>         
>         That's all good.
>         
>         <root> </kdudka></rel></root>
>         
