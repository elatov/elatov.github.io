---
title: 'RHCSA and RHCE Chapter 11 - SELinux'
author: Karim Elatov
layout: post
permalink: /2014/03/rhcsa-rhce-chapter-11-selinux/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2375041786
categories:
  - Certifications
  - RHCSA and RHCE
tags:
  - RHCE
  - RHCSA
  - selinux
---
Most of the information is covered in <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security-Enhanced_Linux/Red_Hat_Enterprise_Linux-6-Security-Enhanced_Linux-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Security-Enhanced_Linux/Red_Hat_Enterprise_Linux-6-Security-Enhanced_Linux-en-US.pdf']);">Security-Enhanced Linux</a> Guide. From the guide here is what SELinux is:

> Security-Enhanced Linux (SELinux) is an implementation of a mandatory access control mechanism in the Linux kernel, checking for allowed operations after standard discretionary access controls are checked. It was created by the National Security Agency and can enforce rules on files and processes in a Linux system, and on their actions, based on defined policies.
> 
> When using SELinux, files, including directories and devices, are referred to as objects. Processes, such as a user running a command or the Mozilla Firefox application, are referred to as subjects. Most operating systems use a Discretionary Access Control (DAC) system that controls how subjects interact with objects, and how subjects interact with each other. On operating systems using DAC, users control the permissions of files (objects) that they own. For example, on Linux operating systems, users could make their home directories world-readable, giving users and processes (subjects) access to potentially sensitive information, with no further protection over this unwanted action.
> 
> Relying on DAC mechanisms alone is fundamentally inadequate for strong system security. DAC access decisions are only based on user identity and ownership, ignoring other security-relevant information such as the role of the user, the function and trustworthiness of the program, and the sensitivity and integrity of the data. Each user typically has complete discretion over their files, making it difficult to enforce a system-wide security policy. Furthermore, every program run by a user inherits all of the permissions granted to the user and is free to change access to the user's files, so minimal protection is provided against malicious software. Many system services and privileged programs run with coarse-grained privileges that far exceed their requirements, so that a flaw in any one of these programs could be exploited to obtain further system access

From the same guide here is quick comparison when SELinux is enabled and when it's not:

> The following is an example of permissions used on Linux operating systems that do not run Security-Enhanced Linux (SELinux). The permissions and output in these examples may differ slightly from your system. Use the **ls -l** command to view file permissions:
> 
>     ~]$ ls -l file1
>     -rwxrw-r-- 1 user1 group1 0 2009-08-30 11:03 file1
>     
> 
> In this example, the first three permission bits, **rwx**, control the access the Linux **user1** user (in this case, the owner) has to **file1**. The next three permission bits, **rw-**, control the access the Linux **group1** group has to **file1**. The last three permission bits, **r-**, control the access everyone else has to **file1**, which includes all users and processes.
> 
> Security-Enhanced Linux (SELinux) adds Mandatory Access Control (MAC) to the Linux kernel, and is enabled by default in Red Hat Enterprise Linux. A general purpose MAC architecture needs the ability to enforce an administratively-set security policy over all processes and files in the system, basing decisions on labels containing a variety of security-relevant information. When properly implemented, it enables a system to adequately defend itself and offers critical support for application security by protecting against the tampering with, and bypassing of, secured applications. MAC provides strong separation of applications that permits the safe execution of untrustworthy applications. Its ability to limit the privileges associated with executing processes limits the scope of potential damage that can result from the exploitation of vulnerabilities in applications and system services. MAC enables information to be protected from legitimate users with limited authorization as well as from authorized users who have unwittingly executed malicious applications
> 
> The following is an example of the labels containing security-relevant information that are used on processes, Linux users, and files, on Linux operating systems that run SELinux. This information is called the SELinux context, and is viewed using the ls -Z command:
> 
>     ~]$ ls -Z file1
>     -rwxrw-r--  user1 group1 unconfined_u:object_r:user_home_t:s0      file1
>     
> 
> In this example, SELinux provides a user (**unconfined_u**), a role (**object_r**), a type (**user_home_t**), and a level (**s0**). This information is used to make access control decisions. With DAC, access is controlled based only on Linux user and group IDs. It is important to remember that SELinux policy rules are checked after DAC rules. SELinux policy rules are not used if DAC rules deny access first.

### SELinux Modes

From the same guide:

> SELinux has three modes:
> 
> *   **Enforcing**: SELinux policy is enforced. SELinux denies access based on SELinux policy rules. 
> *   **Permissive**: SELinux policy is not enforced. SELinux does not deny access, but denials are logged for actions that would have been denied if running in enforcing mode. 
> *   **Disabled**: SELinux is disabled. Only DAC rules are used.
> 
> Use the **setenforce** command to change between enforcing and permissive mode. Changes made with **setenforce** do not persist across reboots. To change to enforcing mode, as the Linux root user, run the **setenforce 1** command. To change to permissive mode, run the **setenforce 0** command. Use the **getenforce** command to view the current SELinux mode.

Here is the SELinux mode on the RHEL machine:

    [root@rhel1 ~]# getenforce 
    Enforcing
    

## SELinux Contexts

From the guide:

> Processes and files are labeled with an SELinux context that contains additional information, such as an SELinux user, role, type, and, optionally, a level. When running SELinux, all of this information is used to make access control decisions. In Red Hat Enterprise Linux, SELinux provides a combination of Role-Based Access Control (RBAC), Type Enforcement (TE), and, optionally, Multi-Level Security (MLS).
> 
> The following is an example showing SELinux context. SELinux contexts are used on processes, Linux users, and files, on Linux operating systems that run SELinux. Use the **ls -Z** command to view the SELinux context of files and directories:
> 
>     ~]$ ls -Z file1
>     -rwxrw-r--  user1 group1 unconfined_u:object_r:user_home_t:s0      file1
>     
> 
> SELinux contexts follow the SELinux **user:role:type:level** syntax. The fields are as follows:
> 
> **SELinux user** - The SELinux user identity is an identity known to the policy that is authorized for a specific set of roles, and for a specific MLS/MCS range. Each Linux user is mapped to an SELinux user via SELinux policy. This allows Linux users to inherit the restrictions placed on SELinux users. The mapped SELinux user identity is used in the SELinux context for processes in that session, in order to define what roles and levels they can enter. Run the **semanage login -l** command as the Linux root user to view a list of mappings between SELinux and Linux user accounts (you need to have the policycoreutils-python package installed):
> 
>     ~]# semanage login -l
>     
>     Login Name                SELinux User              MLS/MCS Range
>     
>     __default__               unconfined_u              s0-s0:c0.c1023
>     root                      unconfined_u              s0-s0:c0.c1023
>     system_u                  system_u                  s0-s0:c0.c1023
>     
> 
> Output may differ slightly from system to system. The **Login Name** column lists Linux users, and the **SELinux User** column lists which SELinux user the Linux user is mapped to. For processes, the SELinux user limits which roles and levels are accessible. The last column, **MLS/MCS Range**, is the level used by Multi-Level Security (MLS) and Multi-Category Security (MCS).
> 
> **role** - Part of SELinux is the Role-Based Access Control (RBAC) security model. The role is an attribute of RBAC. SELinux users are authorized for roles, and roles are authorized for domains. The role serves as an intermediary between domains and SELinux users. The roles that can be entered determine which domains can be entered; ultimately, this controls which object types can be accessed. This helps reduce vulnerability to privilege escalation attacks.
> 
> **type** The type is an attribute of Type Enforcement. The type defines a domain for processes, and a type for files. SELinux policy rules define how types can access each other, whether it be a domain accessing a type, or a domain accessing another domain. Access is only allowed if a specific SELinux policy rule exists that allows it.
> 
> **level** - The level is an attribute of MLS and MCS. An MLS range is a pair of levels, written as **lowlevel-highlevel** if the levels differ, or lowlevel if the levels are identical (**s0-s0** is the same as **s0**). Each level is a sensitivity-category pair, with categories being optional. If there are categories, the level is written as sensitivity:category-set. If there are no categories, it is written as sensitivity.
> 
> If the category set is a contiguous series, it can be abbreviated. For example, **c0.c3** is the same as **c0,c1,c2,c3**. The **/etc/selinux/targeted/setrans.conf** file maps levels (s0:c0) to human-readable form (that is **CompanyConfidential**). Do not edit **setrans.conf** with a text editor: use the **semanage** command to make changes. Refer to the semanage(8) manual page for further information. In Red Hat Enterprise Linux, targeted policy enforces MCS, and in MCS, there is just one sensitivity, **s0**. MCS in Red Hat Enterprise Linux supports 1024 different categories: **c0** through to **c1023**. **s0-s0:c0.c1023** is sensitivity **s0** and authorized for all categories.
> 
> MLS enforces the Bell-La Padula Mandatory Access Model, and is used in Labeled Security Protection Profile (LSPP) environments. To use MLS restrictions, install the **selinux-policy-mls** package, and configure MLS to be the default SELinux policy. The MLS policy shipped with Red Hat Enterprise Linux omits many program domains that were not part of the evaluated configuration, and therefore, MLS on a desktop workstation is unusable (no support for the X Window System); however, an MLS policy from the upstream SELinux Reference Policy can be built that includes all program domains.

### Domain Transitions

Onto domains:

> A process in one domain transitions to another domain by executing an application that has the entrypoint type for the new domain. The entrypoint permission is used in SELinux policy, and controls which applications can be used to enter a domain. The following example demonstrates a domain transition:
> 
> 1.  A user wants to change their password. To do this, they run the **passwd** application. The **/usr/bin/passwd** executable is labeled with the **passwd_exec_t** type:
>     
>         ~]$ ls -Z /usr/bin/passwd
>         -rwsr-xr-x  root root system_u:object_r:passwd_exec_t:s0 /usr/bin/passwd
>         
>     
>     The **passwd** application accesses **/etc/shadow**, which is labeled with the **shadow_t** type:
>     
>         ~]$ ls -Z /etc/shadow
>         -r--------. root root system_u:object_r:shadow_t:s0    /etc/shadow
>         
> 
> 2.  An SELinux policy rule states that processes running in the **passwd_t** domain are allowed to read and write to files labeled with the **shadow_t** type. The **shadow_t** type is only applied to files that are required for a password change. This includes **/etc/gshadow**,**/etc/shadow**, and their backup files.

To check rules we can use **sesearch** (from the **setools-console** package). To show the rule, we can run the following:

    [root@rhel1 ~]# sesearch -A -s passwd_t -t shadow_t
    Found 1 semantic av rules:
       allow passwd_t shadow_t : file { ioctl read write create getattr setattr lock relabelfrom relabelto append unlink link rename open } ;
    

Onto the next step:

> _3. An SELinux policy rule states that the **passwd_t** domain has **entrypoint** permission to the **passwd_exec_t** type.

Here is the rule for that:

    [root@rhel1 ~]# sesearch -A -s passwd_t -t passwd_exec_t
    Found 1 semantic av rules:
       allow passwd_t passwd_exec_t : file { ioctl read getattr lock execute entrypoint open } ;
    

And to the last step:

> _4. When a user runs the passwd application, the user's shell process transitions to the **passwd_t** domain. With SELinux, since the default action is to deny, and a rule exists that allows (among other things) applications running in the **passwd_t** domain to access files labeled with the **shadow_t** type, the **passwd** application is allowed to access **/etc/shadow**, and update the user's password.

From the same guide:

> This example is not exhaustive, and is used as a basic example to explain domain transition. Although there is an actual rule that allows subjects running in the **passwd_t** domain to access objects labeled with the **shadow_t** file type, other SELinux policy rules must be met before the subject can transition to a new domain. In this example, Type Enforcement ensures:
> 
> *   The **passwd_t** domain can only be entered by executing an application labeled with the **passwd_exec_t** type; can only execute from authorized shared libraries, such as the **lib_t** type; and cannot execute any other applications.
> *   Only authorized domains, such as **passwd_t**, can write to files labeled with the **shadow_t** type. Even if other processes are running with superuser privileges, those processes cannot write to files labeled with the **shadow_t** type, as they are not running in the **passwd_t** domain.
> *   Only authorized domains can transition to the **passwd_t** domain. For example, the sendmail process running in the **sendmail_t** domain does not have a legitimate reason to execute passwd; therefore, it can never transition to the **passwd_t** domain.
> *   Processes running in the **passwd_t** domain can only read and write to authorized types, such as files labeled with the **etc_t** or **shadow_t** types. This prevents the passwd application from being tricked into reading or writing arbitrary files.

### SELinux Contexts for Processes

We can also check contexts of processes. From the same guide:

> Use the **ps -eZ** command to view the SELinux context for processes. For example:
> 
> 1.  Run the **passwd** command. Do not enter a new password.
> 2.  Open a new tab, or another terminal, and run the **ps -eZ | grep passwd** command. The output is similar to the following:
>     
>         unconfined_u:unconfined_r:passwd_t:s0-s0:c0.c1023 13212 pts/1 00:00:00 passwd
>         
> 
> 3.  In the first tab/terminal, press Ctrl+C to cancel the passwd application.
> 
> In this example, when the **passwd** application (labeled with the **passwd_exec_t** type) is executed, the user's shell process transitions to the **passwd_t** domain. Remember that the type defines a domain for processes, and a type for files.
> 
> Use the **ps -eZ** command to view the SELinux contexts for running processes. The following is a truncated example of the output, and may differ on your system:
> 
>     system_u:system_r:dhcpc_t:s0             1869 ?  00:00:00 dhclient
>     system_u:system_r:sshd_t:s0-s0:c0.c1023  1882 ?  00:00:00 sshd
>     system_u:system_r:gpm_t:s0               1964 ?  00:00:00 gpm
>     system_u:system_r:crond_t:s0-s0:c0.c1023 1973 ?  00:00:00 crond
>     system_u:system_r:kerneloops_t:s0        1983 ?  00:00:05 kerneloops
>     system_u:system_r:crond_t:s0-s0:c0.c1023 1991 ?  00:00:00 atd
>     
> 
> The **system_r** role is used for system processes, such as daemons. Type Enforcement then separates each domain.

If you want to check a specific process you can run the following:

    [root@rhel1 ~]# ps -ZC vsftpd
    LABEL                             PID TTY          TIME CMD
    system_u:system_r:ftpd_t:s0-s0:c0.c1023 1126 ? 00:00:00 vsftpd
    

You can also run the **id** command to find out SELinux User you belong to:

    [root@rhel1 ~]# id -Z
    unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
    

### Confined Processes

From the SELinux Guide:

> Almost every service that listens on a network, such as **sshd** or **httpd**, is confined in Red Hat Enterprise Linux. Also, most processes that run as the Linux root user and perform tasks for users, such as the **passwd** application, are confined. When a process is confined, it runs in its own domain, such as the **httpd** process running in the **httpd_t** domain. If a confined process is compromised by an attacker, depending on SELinux policy configuration, an attacker's access to resources and the possible damage they can do is limited.

Let's test this out. If you want to enable SELinux logging, install the following packages:

    # yum install policycoreutils-python policycoreutils selinux-policy setroubleshoot-server
    

As you saw above I am actually running **vsftpd**. I also had **/var/www** setup as the anonymous directory:

    [root@rhel1 log]# grep anon_root /etc/vsftpd/vsftpd.conf 
    anon_root=/var/www
    

Now if I try to connect locally, I see the following:

    [root@rhel1 ~]# ftp localhost
    Connected to localhost (127.0.0.1).
    220 (vsFTPd 2.2.2)
    Name (localhost:root): anonymous
    331 Please specify the password.
    Password:
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    227 Entering Passive Mode (127,0,0,1,51,206).
    150 Here comes the directory listing.
    226 Transfer done (but failed to open directory).
    

I actually didn't get any files back. Here is the listing under **/var/www**:

    [root@rhel1 ~]# ls -lZ /var/www
    dr-xr-xr-x. root root unconfined_u:object_r:var_t:s0   pub
    

We already can see that the domain/type is of **var_t** and our process is running as **ftpd_t**. Now checking out the **/var/log/messages**, I saw the following:

    [root@rhel1 ~]# tail -1 /var/log/messages
    Feb 23 14:58:41 rhel1 setroubleshoot: SELinux is preventing /usr/sbin/vsftpd "read" access to /var/www. For complete SELinux messages. run sealert -l 128f1d32-f8c7-4e31-86d2-881ac5928a7e
    

We can also see that we can get more information if we run the following:

    [root@rhel1 ~]# sealert -l 128f1d32-f8c7-4e31-86d2-881ac5928a7e
    
    Summary:
    
    SELinux is preventing /usr/sbin/vsftpd "read" access to /var/www.
    
    Detailed Description:
    
    SELinux denied access requested by vsftpd. /var/www may be a mislabeled.
    /var/www default SELinux type is httpd_sys_content_t, but its current type is
    var_t. Changing this file back to the default type, may fix your problem.
    
    File contexts can be assigned to a file in the following ways.
    
      * Files created in a directory receive the file context of the parent
        directory by default.
      * The SELinux policy might override the default label inherited from the
        parent directory by specifying a process running in context A which creates
        a file in a directory labeled B will instead create the file with label C.
        An example of this would be the dhcp client running with the dhclient_t type
        and creating a file in the directory /etc. This file would normally receive
        the etc_t type due to parental inheritance but instead the file is labeled
        with the net_conf_t type because the SELinux policy specifies this.
      * Users can change the file context on a file using tools such as chcon, or
        restorecon.
    
    This file could have been mislabeled either by user error, or if an normally
    confined application was run under the wrong domain.
    
    However, this might also indicate a bug in SELinux because the file should not
    have been labeled with this type.
    
    If you believe this is a bug, please file a bug report against this package.
    
    Allowing Access:
    
    You can restore the default system context to this file by executing the
    restorecon command. restorecon '/var/www', if this file is a directory, you can
    recursively restore using restorecon -R '/var/www'.
    
    Fix Command:
    
    /sbin/restorecon '/var/www'
    
    Additional Information:
    
    Source Context                system_u:system_r:ftpd_t:s0-s0:c0.c1023
    Target Context                unconfined_u:object_r:var_t:s0
    Target Objects                /var/www [ dir ]
    Source                        vsftpd
    Source Path                   /usr/sbin/vsftpd
    Port                          <Unknown>
    Host                          rhel1.local.com
    Source RPM Packages           vsftpd-2.2.2-6.el6_0.1
    Target RPM Packages           
    Policy RPM                    selinux-policy-3.7.19-93.el6
    Selinux Enabled               True
    Policy Type                   targeted
    Enforcing Mode                Enforcing
    Plugin Name                   restorecon
    Host Name                     rhel1.local.com
    Platform                      Linux rhel1.local.com 2.6.32-131.0.15.el6.i686 #1
                                  SMP Tue May 10 15:42:28 EDT 2011 i686 i686
    Alert Count                   2
    First Seen                    Sun Feb 23 14:46:25 2014
    Last Seen                     Sun Feb 23 14:58:38 2014
    Local ID                      128f1d32-f8c7-4e31-86d2-881ac5928a7e
    Line Numbers                  
    
    Raw Audit Messages            
    
    node=rhel1.local.com type=AVC msg=audit(1393192718.339:126): avc:  denied  { read } for  pid=2989 comm="vsftpd" name="www" dev=dm-0 ino=394931 scontext=system_u:system_r:ftpd_t:s0-s0:c0.c1023 tcontext=unconfined_u:object_r:var_t:s0 tclass=dir
    
    node=rhel1.local.com type=SYSCALL msg=audit(1393192718.339:126): arch=40000003 syscall=5 success=no exit=-13 a0=1aaae28 a1=98800 a2=db233c a3=bfe3b154 items=0 ppid=2987 pid=2989 auid=4294967295 uid=14 gid=50 euid=14 suid=14 fsuid=14 egid=50 sgid=50 fsgid=50 tty=(none) ses=4294967295 comm="vsftpd" exe="/usr/sbin/vsftpd" subj=system_u:system_r:ftpd_t:s0-s0:c0.c1023 key=(null)
    

We get a lot of information. The most important part is the following:

    denied  { read } for  pid=2989 comm="vsftpd" name="www" dev=dm-0 ino=394931 scontext=system_u:system_r:ftpd_t:s0-s0:c0.c1023 tcontext=unconfined_u:object_r:var_t:s0 tclass=dir
    

as we expected the source context (**scontext=system_u:system_r:ftpd_t:s0-s0:c0.c1023**) cannot access the target context (**tcontext=unconfined_u:object_r:var_t:s0**). There is a cool tool called **audit2allow**, it basically parses failures and will provide a way to solve the issue, for example here is what it told me:

    [root@rhel1 ~]# tail /var/log/audit/audit.log | audit2allow  -a -w
    type=AVC msg=audit(1393193843.673:142): avc:  denied  { read } for  pid=3107 comm="vsftpd" name="www" dev=dm-0 ino=394931 scontext=system_u:system_r:ftpd_t:s0-s0:c0.c1023 tcontext=system_u:object_r:httpd_sys_content_t:s0 tclass=dir
        Was caused by:
        One of the following booleans was set incorrectly.
        Description:
        Allow ftp servers to login to local users and read/write all files on the system, governed by DAC.
    
        Allow access by executing:
        # setsebool -P allow_ftpd_full_access 1
        Description:
        Allow ftp to read and write files in the user home directories
    
        Allow access by executing:
        # setsebool -P ftp_home_dir 1
    

It went a little over board and gave anonymous all the access. Let's check out all the available booleans for ftp access. Here is a list of the booleans:

    [root@rhel1 ~]# semanage boolean -l | grep ftp
    ftp_home_dir                   -> off   Allow ftp to read and write files in the user home directories
    tftp_anon_write                -> off   Allow tftp to modify public files used for public file transfer services.
    allow_ftpd_full_access         -> off   Allow ftp servers to login to local users and read/write all files on the system, governed by DAC.
    sftpd_write_ssh_home           -> off   Allow interlnal-sftp to read and write files in the user ssh home directories.
    allow_ftpd_use_nfs             -> off   Allow ftp servers to use nfs used for public file transfer services.
    allow_ftpd_anon_write          -> off    Allow ftp servers to upload files,  used for public file transfer services. Directories must be labeled public_content_rw_t.
    sftpd_enable_homedirs          -> off   Allow sftp-internal to read and write files in the user home directories
    allow_ftpd_use_cifs            -> off   Allow ftp servers to use cifs used for public file transfer services.
    sftpd_full_access              -> off   Allow sftp-internal to login to local users and read/write all files on the system, governed by DAC.
    ftpd_connect_db                -> off   Allow ftp servers to use connect to mysql database
    httpd_enable_ftp_server        -> off   Allow httpd to act as a FTP server by listening on the ftp port.
    sftpd_anon_write               -> off   Allow anon internal-sftp to upload files, used for public file transfer services. Directories must be labeled public_content_rw_t.
    

Let's enable the **anonymous_write** boolean:

    [root@rhel1 ~]# setsebool -P allow_ftpd_anon_write=1
    

Lastly let's add the appropriate type as well (as mentioned for this specific boolean):

    [root@rhel1 ~]# chcon -vt public_content_rw_t /var/www
    changing security context of `/var/www'
    

Now let's try the ftp access again:

    [root@rhel1 ~]# ftp localhost
    Connected to localhost (127.0.0.1).
    220 (vsFTPd 2.2.2)
    Name (localhost:root): anonymous
    331 Please specify the password.
    Password:
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    227 Entering Passive Mode (127,0,0,1,119,64).
    150 Here comes the directory listing.
    dr-xr-xr-x    9 0        0            4096 Mar 22  2010 pub
    226 Directory send OK.
    

To reset the context to it's original state, run the following:

    [root@rhel1 ~]# restorecon -v /var/www
    restorecon reset /var/www context system_u:object_r:public_content_rw_t:s0->system_u:object_r:httpd_sys_content_t:s0
    

The SELinux Guide had a similar example but with apache.

### Unconfined Processes

From the Guide:

> Unconfined processes run in unconfined domains, for example, init programs run in the unconfined **initrc_t** domain, unconfined kernel processes run in the **kernel_t** domain, and unconfined Linux users run in the **unconfined_t** domain. For unconfined processes, SELinux policy rules are applied, but policy rules exist that allow processes running in unconfined domains almost all access. Processes running in unconfined domains fall back to using DAC rules exclusively. If an unconfined process is compromised, SELinux does not prevent an attacker from gaining access to system resources and data, but of course, DAC rules are still used. SELinux is a security enhancement on top of DAC rules – it does not replace them.

Here is the example:

> 1.  The **chcon** command relabels files; however, such label changes do not survive when the file system is relabeled. For permanent changes that survive a file system relabel, use the **semanage** command, which is discussed later. As the Linux root user, run the following command to change the type to a type used by Samba:
>     
>         ~]# chcon -t samba_share_t /var/www/html/testfile
>         
>     
>     Run the **ls -Z /var/www/html/testfile** command to view the changes:
>     
>         ~]$ ls -Z /var/www/html/testfile
>         -rw-r--r--  root root unconfined_u:object_r:samba_share_t:s0 /var/www/html/testfile
>         
> 
> 2.  Run the **service httpd status** command to confirm that the httpd process is not running:
>     
>         ~]$ service httpd status
>         httpd is stopped
>         
>     
>     If the output differs, run the **service httpd stop** command as the Linux root user to stop the httpd process:
>     
>         ~]# service httpd stop
>         Stopping httpd:                                            [  OK  ]
>         
> 
> 3.  To make the **httpd** process run unconfined, run the following command as the Linux root user to change the type of **/usr/sbin/httpd**, to a type that does not transition to a confined domain:
>     
>         ~]# chcon -t unconfined_exec_t /usr/sbin/httpd
>         
> 
> 4.  Run the **ls -Z /usr/sbin/httpd** command to confirm that **/usr/sbin/httpd** is labeled with the **unconfined_exec_t** type:
>     
>         ~]$ ls -Z /usr/sbin/httpd
>         -rwxr-xr-x  root root system_u:object_r:unconfined_exec_t:s0 /usr/sbin/httpd
>         
> 
> 5.  As the Linux root user, run the **service httpd start** command to start the **httpd** process. The output is as follows if httpd starts successfully:
>     
>         ~]# service httpd start
>         Starting httpd:                 [  OK  ]
>         
> 
> 6.  Run the **ps -eZ | grep httpd** command to view the httpd running in the unconfined_t domain:
>     
>         ~]$ ps -eZ | grep httpd
>         unconfined_u:unconfined_r:unconfined_t:s0 7721 ?      00:00:00 httpd
>         unconfined_u:unconfined_r:unconfined_t:s0 7723 ?      00:00:00 httpd
>         
> 
> 7.  Change into a directory where your Linux user has write access to, and run the **wget http://localhost/testfile** command. Unless there are changes to the default configuration, this command succeeds:
>     
>         ~]$ wget http://localhost/testfile
>         --2009-05-07 01:41:10--  http://localhost/testfile
>         Resolving localhost... 127.0.0.1
>         Connecting to localhost|127.0.0.1|:80... connected.
>         HTTP request sent, awaiting response... 200 OK
>         Length: 0 [text/plain]
>         Saving to: `testfile.1'
>         
>         [ <=>                            ]--.-K/s   in 0s      
>           
>         2009-05-07 01:41:10 (0.00 B/s) - `testfile.1' saved [0/0]
>         
>     
>     Although the **httpd** process does not have access to files labeled with the **samba_share_t** type, **httpd** is running in the unconfined **unconfined_t** domain, and falls back to using DAC rules, and as such, the **wget** command succeeds. Had **httpd** been running in the confined **httpd_t** domain, the **wget** command would have failed.
> 
> 8.  The **restorecon** command restores the default SELinux context for files. As the Linux root user, run the **restorecon -v /usr/sbin/httpd** command to restore the default SELinux context for **/usr/sbin/httpd**:
>     
>         ~]# restorecon -v /usr/sbin/httpd
>         restorecon reset /usr/sbin/httpd context system_u:object_r:unconfined_exec_t:s0->system_u:object_r:httpd_exec_t:s0
>         
>     
>     Run the **ls -Z /usr/sbin/httpd** command to confirm that **/usr/sbin/httpd** is labeled with the **httpd_exec_t** type:
>     
>         ~]$ ls -Z /usr/sbin/httpd
>         -rwxr-xr-x  root root system_u:object_r:httpd_exec_t:s0 /usr/sbin/httpd
>         
> 
> 9.  As the Linux root user, run the **service httpd restart** command to restart **httpd**. After restarting, run the **ps -eZ | grep httpd** command to confirm that httpd is running in the confined **httpd_t** domain:
>     
>         ~]# service httpd restart
>         Stopping httpd:                                            [  OK  ]
>         Starting httpd:                                            [  OK  ]
>         ~]# ps -eZ | grep httpd
>         unconfined_u:system_r:httpd_t:s0    8883 ?        00:00:00 httpd
>         unconfined_u:system_r:httpd_t:s0    8884 ?        00:00:00 httpd
>         
> 
> 10. As the Linux root user, run the **rm -i /var/www/html/testfile** command to remove testfile:
>     
>         ~]# rm -i /var/www/html/testfile
>         rm: remove regular empty file `/var/www/html/testfile'? y
>         
> 
> 11. If you do not require **httpd** to be running, as the Linux root user, run the **service httpd stop** command to stop **httpd**:
>     
>         ~]# service httpd stop
>         Stopping httpd:                                            [  OK  ]
>         
> 
> The examples in these sections demonstrate how data can be protected from a compromised confined-process (protected by SELinux), as well as how data is more accessible to an attacker from a compromised unconfined-process (not protected by SELinux).

## SELinux Packages

From the SELinux Guide:

> In Red Hat Enterprise Linux, the SELinux packages are installed by default, in a full installation, unless they are manually excluded during installation. If performing a minimal installation in text mode, the policycoreutils-python and the policycoreutils-gui package are not installed by default. Also, by default, SELinux targeted policy is used, and SELinux runs in enforcing mode. The following is a brief description of the SELinux packages that are installed on your system by default:
> 
> *   **policycoreutils** provides utilities such as **restorecon**, **secon**, **setfiles**, **semodule**, **load_policy**, and **setsebool**, for operating and managing SELinux.
> *   **selinux-policy** provides the SELinux Reference Policy. The SELinux Reference Policy is a complete SELinux policy, and is used as a basis for other policies, such as the SELinux targeted policy; refer to the Tresys Technology SELinux Reference Policy page for further information. This package also provides the **/usr/share/selinux/devel/policygentool** development utility, as well as example policy files.
> *   **selinux-policy-targeted** provides the SELinux targeted policy.
> *   **libselinux** – provides an API for SELinux applications.
> *   **libselinux-utils** provides the **avcstat**, **getenforce**, **getsebool**, **matchpathcon**, **selinuxconlist**, **selinuxdefcon**, **selinuxenabled**, **setenforce**, and **togglesebool** utilities.
> *   **libselinux-python** provides Python bindings for developing SELinux applications.
> *   **setroubleshoot-server** translates denial messages, produced when access is denied by SELinux, into detailed descriptions that are viewed with the **sealert** utility, also provided by this package.
> *   **setools-console** – this package provides the Tresys Technology SETools distribution, a number of tools and libraries for analyzing and querying policy, audit log monitoring and reporting, and file context management. The setools package is a meta-package for SETools. The **setools-gui** package provides the **apol**, **seaudit**, and **sediffx** tools. The setools-console package provides the **seaudit-report**, **sechecker**, **sediff**, **seinfo**, **sesearch**, **findcon**, **replcon**, and **indexcon** command-line tools. Refer to the Tresys Technology SETools page for information about these tools.
> *   **mcstrans** translates levels, such as **s0-s0:c0.c1023**, to an easier to read form, such as **SystemLow-SystemHigh**. This package is not installed by default.
> *   **policycoreutils-python** provides utilities such as **semanage**, **audit2allow**, **audit2why**, and **chcat**, for operating and managing SELinux.
> *   **policycoreutils-gui** provides **system-config-selinux**, a graphical tool for managing SELinux.

### SELinux Log File

From the Guide:

> In Red Hat Enterprise Linux 6, the **dbus** and **audit** packages are installed by default, unless they are removed from the default package selection. The **setroubleshoot-server** must be installed via Yum (the **yum install setroubleshoot** command).
> 
> If the **auditd** daemon is running, SELinux denial messages, such as the following, are written to **/var/log/audit/audit.log** by default:
> 
>     type=AVC msg=audit(1223024155.684:49): avc:  denied  { getattr } for  pid=2000 comm="httpd" path="/var/www/html/file1" dev=dm-0 ino=399185 scontext=unconfined_u:system_r:httpd_t:s0 tcontext=system_u:object_r:samba_share_t:s0 tclass=file
>     

More from the guide:

> SELinux decisions, such as allowing or disallowing access, are cached. This cache is known as the **Access Vector Cache** (AVC). Denial messages are logged when SELinux denies access. These denials are also known as "AVC denials", and are logged to a different location, depending on which daemons are running:
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2014/02/selinux-log-files1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2014/02/selinux-log-files1.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2014/02/selinux-log-files1.png" alt="selinux log files1 RHCSA and RHCE Chapter 11   SELinux" width="714" height="136" class="alignnone size-full wp-image-10151" title="RHCSA and RHCE Chapter 11   SELinux" /></a>
> 
> If DAC rules (standard Linux permissions) allow access, check **/var/log/messages** and **/var/log/audit/audit.log** for "SELinux is preventing" and "denied" errors respectively. This can be done by running the following commands as the Linux root user:
> 
>     ~]# grep "SELinux is preventing" /var/log/messages
>     ~]# grep "denied" /var/log/audit/audit.log
>     

### SELinux Status

From the SELinux Guide:

> The **/etc/selinux/config** file is the main SELinux configuration file. It controls the SELinux mode and the SELinux policy to use:
> 
>     # This file controls the state of SELinux on the system.
>     # SELINUX= can take one of these three values:
>     #       enforcing - SELinux security policy is enforced.
>     #       permissive - SELinux prints warnings instead of enforcing.
>     #       disabled - No SELinux policy is loaded.
>     SELINUX=enforcing
>     # SELINUXTYPE= can take one of these two values:
>     #       targeted - Targeted processes are protected,
>     #       mls - Multi Level Security protection.
>     SELINUXTYPE=targeted
>     
> 
> **SELINUX=enforcing** - The SELINUX option sets the mode SELinux runs in. SELinux has three modes: **enforcing**, **permissive**, and **disabled**. When using enforcing mode, SELinux policy is enforced, and SELinux denies access based on SELinux policy rules. Denial messages are logged. When using **permissive** mode, SELinux policy is not enforced. SELinux does not deny access, but denials are logged for actions that would have been denied if running SELinux in **enforcing** mode. When using **disabled** mode, SELinux is **disabled** (the SELinux module is not registered with the Linux kernel), and only DAC rules are used.
> 
> **SELINUXTYPE=targeted** - The SELINUXTYPE option sets the SELinux policy to use. **Targeted** policy is the default policy. Only change this option if you want to use the MLS policy.

To check the status we can run the following:

> Use the **getenforce** or **sestatus** commands to check the status of SELinux. The **getenforce** command returns Enforcing, Permissive, or Disabled.
> 
> The **sestatus** command returns the SELinux status and the SELinux policy being used:
> 
>     ~]$ sestatus
>     SELinux status:                 enabled
>     SELinuxfs mount:                /selinux
>     Current mode:                   enforcing
>     Mode from config file:          enforcing
>     Policy version:                 24
>     Policy from config file:        targeted
>     

To disable or enable SELinux update the **/etc/selinux/config** file accordingly.

### SELinux Booleans

From the Guide:

> Booleans allow parts of SELinux policy to be changed at runtime, without any knowledge of SELinux policy writing. This allows changes, such as allowing services access to NFS volumes, without reloading or recompiling SELinux policy.
> 
> For a list of Booleans, an explanation of what each one is, and whether they are on or off, run the **semanage boolean -l** command as the Linux root user. The following example does not list all Booleans:
> 
>     ~]# semanage boolean -l
>     SELinux boolean                          Description
>     
>     ftp_home_dir                   -> off   Allow ftp to read and write files in the user home directories
>     xen_use_nfs                    -> off   Allow xen to manage nfs files
>     xguest_connect_network         -> on    Allow xguest to configure Network Manager
>     
> 
> The **getsebool -a** command lists Booleans, whether they are on or off, but does not give a description of each one. The following example does not list all Booleans:
> 
>     ~]$ getsebool -a
>     allow_console_login --> off
>     allow_cvs_read_shadow --> off
>     allow_daemons_dump_core --> on
>     
> 
> Run the **setsebool** utility in the **setsebool boolean_name on/off** form to enable or disable Booleans.
> 
> To temporarily enable Apache HTTP Server scripts and modules to connect to database servers, run the **setsebool httpd_can_network_connect_db on** command as the Linux root user.
> 
> Use the **getsebool httpd_can_network_connect_db** command to verify the Boolean is enabled:
> 
>     ~]$ getsebool httpd_can_network_connect_db
>     httpd_can_network_connect_db --> on
>     
> 
> This change is not persistent across reboots. To make changes persistent across reboots, run the **setsebool -P boolean-name on** command as the Linux root user:
> 
>     ~]# setsebool -P httpd_can_network_connect_db on
>     

### SELinux Change Context

The Guide:

> The **chcon** command changes the SELinux context for files. However, changes made with the **chcon** command do not survive a file system relabel, or the execution of the restorecon command. SELinux policy controls whether users are able to modify the SELinux context for any given file. When using chcon, users provide all or part of the SELinux context to change. An incorrect file type is a common cause of SELinux denying access.
> 
> Run the **chcon -t samba_share_t file1** command to change the type to **samba_share_t**. The **-t** option only changes the type. View the change with **ls -Z file1**:
> 
>     ~]$ ls -Z file1 
>     -rw-rw-r--  user1 group1 unconfined_u:object_r:samba_share_t:s0 file1
>     
> 
> Use the **restorecon -v file1** command to restore the SELinux context for the **file1** file. Use the **-v** option to view what changes:
> 
>     ~]$ restorecon -v file1
>     restorecon reset file1 context unconfined_u:object_r:samba_share_t:s0->system_u:object_r:user_home_t:s0
>     

If you want to change the context permanently then we can do this:

> The **semanage fcontext** command is used to change the SELinux context of files. When using targeted policy, changes are written to files located in the **/etc/selinux/targeted/contexts/files/** directory:
> 
> *   The **file_contexts** file specifies default contexts for many files, as well as contexts updated via **semanage fcontext**.
> *   The **file_contexts.local** file stores contexts to newly created files and directories not found in file_contexts.
> 
> Two utilities read these files. The **setfiles** utility is used when a file system is relabeled and the **restorecon** utility restores the default SELinux contexts. This means that changes made by **semanage fcontext** are persistent, even if the file system is relabeled. SELinux policy controls whether users are able to modify the SELinux context for any given file.

Here is example usage:

> To make SELinux context changes that survive a file system relabel:
> 
> 1.  Run the **semanage fcontext -a options file-name|directory-name** command, remembering to use the full path to the file or directory.
> 2.  Run the **restorecon -v file-name|directory-name** command to apply the context changes.

