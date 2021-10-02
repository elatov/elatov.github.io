---
title: RHCSA and RHCE Chapter 7 User Administration
author: Karim Elatov
layout: post
permalink: /2013/03/rhcsa-and-rhce-chapter-7-user-administration/
categories: ['os', 'certifications', 'rhcsa_rhce']
tags: ['rhel', 'linux', 'user_management']
---

Let's get straight to it, from the "[Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/deployment_guide/red_hat_enterprise_linux-6-deployment_guide-en-us.pdf)":

> **Chapter 3. Managing Users and Groups** The control of users and groups is a core element of Red Hat Enterprise Linux system administration. This chapter explains how to add, manage, and delete users and groups in the graphical user interface and on the command line, and covers advanced topics, such as enabling password aging or creating group directories.
>
> **3.1. Introduction to Users and Groups** While users can be either people (meaning accounts tied to physical users) or accounts which exist for specific applications to use, groups are logical expressions of organization, tying users together for a common purpose. Users within a group can read, write, or execute files owned by that group. Each user is associated with a unique numerical identification number called a user ID (**UID**). Likewise, each group is associated with a group ID (**GID**). A user who creates a file is also the owner and group owner of that file. The file is assigned separate read, write, and execute permissions for the owner, the group, and everyone else. The file owner can be changed only by root, and access permissions can be changed by both the root user and file owner.
>
> **3.1.1. User Private Groups** Red Hat Enterprise Linux uses a user private group (UPG) scheme, which makes UNIX groups easier to manage. A user private group is created whenever a new user is added to the system. It has the same name as the user for which it was created and that user is the only member of the user private group. User private groups make it safe to set default permissions for a newly created file or directory, allowing both the user and the group of that user to make modifications to the file or directory. The setting which determines what permissions are applied to a newly created file or directory is called a **umask** and is configured in the **/etc/bashrc** file. Traditionally on UNIX systems, the **umask** is set to *022*, which allows only the user who created the file or directory to make modifications. Under this scheme, all other users, including members of the creator's group, are not allowed to make any modifications. However, under the UPG scheme, this “group protection” is not necessary since every user has their own private group.
>
> **3.1.2. Shadow Passwords** In environments with multiple users, it is very important to use shadow passwords provided by the **shadow-utils** package to enhance the security of system authentication files. For this reason, the installation program enables shadow passwords by default. The following is a list of the advantages shadow passwords have over the traditional way of storing passwords on UNIX-based systems:
>
> *   Shadow passwords improve system security by moving encrypted password hashes from the world-readable **/etc/passwd** file to **/etc/shadow**, which is readable only by the root user.
> *   Shadow passwords store information about password aging.
> *   Shadow passwords allow the **/etc/login.defs** file to enforce security policies.
>
> Most utilities provided by the **shadow-utils** package work properly whether or not shadow passwords are enabled. However, since password aging information is stored exclusively in the **/etc/shadow** file, any commands which create or modify password aging information do not work. The following is a list of utilities and commands that do not work without first enabling shadow passwords:
>
> *   The **chage** utility.
> *   The **gpasswd** utility.
> *   The **usermod** command with the -e or -f option.
> *   The **useradd** command with the -e or -f option.

### Adding a User to RHEL with **useradd**

> **3.3. Using Command Line Tools**
>
> ![user mgmt commands RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/user_mgmt_commands.png)
>
> **3.3.1. Adding a New User**
>
> To add a new user to the system, typing the following at a shell prompt as root:
>
>     useradd [options] username
>
>
> …where options are command line options as described in Table 3.2, “useradd command line options”. By default, the **useradd** command creates a locked user account. To unlock the account, run the following command as root to assign a password:
>
>     passwd username
>
>
> ![useradd options RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/useradd_options.png)
>
> **Explaining the Process**
>
> The following steps illustrate what happens if the command **useradd juan** is issued on a system that has shadow passwords enabled:
>
> 1.  A new line for **juan** is created in **/etc/passwd**:
>
>         juan:x:501:501::/home/juan:/bin/bash
>
>
>     The line has the following characteristics:
>        
>     *   It begins with the username **juan**.
>     *   There is an **x** for the password field indicating that the system is using shadow passwords.
>     *   A **UID** greater than 499 is created. Under Red Hat Enterprise Linux, UIDs below 500 are reserved for system use and should not be assigned to users.
>     *   A **GID** greater than 499 is created. Under Red Hat Enterprise Linux, GIDs below 500 are reserved for system use and should not be assigned to users.
>     *   The optional **GECOS** information is left blank. The **GECOS** field can be used to provide additional information about the user, such as their full name or phone number.
>     *   The home directory for **juan** is set to **/home/juan/**.
>     *   The default shell is set to **/bin/bash**.
>
> 2.  A new line for **juan** is created in **/etc/shadow**:
>
>         juan:!!:14798:0:99999:7:::
>
>
>     The line has the following characteristics:
>        
>     *   It begins with the username **juan**
>     *   Two exclamation marks (**!!**) appear in the password field of the **/etc/shadow file**, which locks the account.
>     *   The password is set to never expire
>
> 3.  A new line for a group named **juan** is created in **/etc/group**:
>
>         juan:x:501:
>
>
>     A group with the same name as a user is called a user private group. The line created in **/etc/group** has the following characteristics:
>        
>     *   It begins with the group name **juan**.
>     *   An **x** appears in the password field indicating that the system is using shadow group passwords.
>     *   The **GID** matches the one listed for user juan in **/etc/passwd**
>
> 4.  A new line for a group named **juan** is created in **/etc/gshadow**:
>
>          juan:!::
>
>
>     The line has the following characteristics:
>        
>     *   It begins with the group name **juan**.
>     *   An exclamation mark (**!**) appears in the password field of the **/etc/gshadow** file, which locks the group.
>     *   All other fields are blank.
>
> 5.  A directory for user **juan** is created in the **/home/** directory:
>
>          ~]# ls -l /home
>          total 4
>          drwx----- 4 juan juan 4096 Mar 3 18:23 juan
>
>
>     This directory is owned by user **juan** and group **juan**. It has read, write, and execute privileges only for the user **juan**. All other permissions are denied.
>
> 6.  The files within the **/etc/skel/** directory (which contain default user settings) are copied into the new **/home/juan/** directory:
>
>          ~]# ls -la /home/juan
>          total 28
>          drwx------. 4 juan juan 4096 Mar 3 18:23 .
>          drwxr-xr-x. 5 root root 4096 Mar 3 18:23 ..
>          -rw-r--r--. 1 juan juan 18 Jun 22 2010 .bash_logout
>          -rw-r--r--. 1 juan juan 176 Jun 22 2010 .bash_profile
>          -rw-r--r--. 1 juan juan 124 Jun 22 2010 .bashrc
>          drwxr-xr-x. 2 juan juan 4096 Jul 14 2010 .gnome2
>          drwxr-xr-x. 4 juan juan 4096 Nov 23 15:09 .mozilla
>
>
>     At this point, a locked account called **juan** exists on the system. To activate it, the administrator must next assign a password to the account using the **passwd** command and, optionally, set password aging guidelines.

Let's go ahead and create two users called *user1* and *user2* and check out their settings:

    [root@rhel1 ~]# useradd user1
    [root@rhel1 ~]# useradd user2


Let's see their corresponding information under **/etc/passwd** and **/etc/shadow**:

    [root@rhel1 ~]# getent passwd user1
    user1:x:500:500::/home/user1:/bin/bash
    [root@rhel1 ~]# getent passwd user2
    user2:x:501:501::/home/user2:/bin/bash
    [root@rhel1 ~]# getent shadow user1
    user1:!!:15744:0:99999:7:::
    [root@rhel1 ~]# getent shadow user2
    user2:!!:15744:0:99999:7:::


Now let's check out their *group* information:

    [root@rhel1 ~]# getent group user1
    user1:x:500:
    [root@rhel1 ~]# getent group user2
    user2:x:501:
    [root@rhel1 ~]# getent gshadow user1
    user1:!::
    [root@rhel1 ~]# getent gshadow
    user2 user2:!::


That looks good, now let's check out their home directories:

    root@rhel1 ~]# tree -a /home
    /home
          ├── user1
               ├── .bash_logout  
               ├── .bash_profile  
               └── .bashrc
          └── user2
               ├── .bash_logout
               ├── .bash_profile
               └── .bashrc
    2 directories, 6 files


That looks good, let's check out under **/etc/skel** to see what files were supposed to be auto copied upon user creation:

    [root@rhel1 ~]# ls -la /etc/skel
    total 20
    drwxr-xr-x. 2  root root 4096 Feb 4 04:25 .
    drwxr-xr-x. 60 root root 4096 Feb 8 06:28 ..
    -rw-r--r--. 1  root root 18   Jan 27 2011 .bash_logout
    -rw-r--r--. 1  root root 176  Jan 27 2011 .bash_profile
    -rw-r--r--. 1  root root 124  Jan 27 2011 .bashrc


That looks correct. Lastly, let's check out the settings for *user* creation:

    [root@rhel1 ~]# grep -v -E '^#|^$' /etc/login.defs
    MAIL_DIR /var/spool/mail
    PASS_MAX_DAYS 99999
    PASS_MIN_DAYS 0
    PASS_MIN_LEN 5
    PASS_WARN_AGE 7
    UID_MIN 500
    UID_MAX 60000
    GID_MIN 500
    GID_MAX 60000
    CREATE_HOME yes
    UMASK 077
    USERGROUPS_ENAB yes
    ENCRYPT_METHOD SHA512


We can see that all of the above settings were honored during the creation of the *users*.

### Adding a Group to RHEL with **groupadd**

Now let's move onto *groups*, from the same guide:

> **3.3.2. Adding a New Group**
>
> To add a new group to the system, type the following at a shell prompt as root:
>
>     groupadd [options] group_name
>
>
> …where options are command line options as described in Table 3.3, “groupadd command line options”.
>
> ![groupadd options RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/groupadd_options.png)

So let's add two new groups called *group1* and *group2* and add our users to the groups:

    [root@rhel1 ~]# groupadd group1
    [root@rhel1 ~]# groupadd group2
    [root@rhel1 ~]# getent group group1
    group1:x:502:
    [root@rhel1 ~]# getent group group2
    group2:x:503:
    [root@rhel1 ~]# getent gshadow group1
    group1:!::
    [root@rhel1 ~]# getent gshadow group2
    group2:!::


The creation went well. Now let's add the users to these groups:

    [root@rhel1 ~]# usermod -G group1 user1
    [root@rhel1 ~]# usermod -G group2 user2
    [root@rhel1 ~]# getent group group1
    group1:x:502:user1
    [root@rhel1 ~]# getent group group2
    group2:x:503:user2


To get a concise view of the IDs (**UID** and **ID**) we can use the command **id**, like so:

    root@rhel1 ~]# id -a user1
    uid=500(user1) gid=500(user1) groups=500(user1),502(group1)
    [root@rhel1 ~]# id -a user2
    uid=501(user2) gid=501(user2) groups=501(user2),503(group2)


That all looks good. Lastly let's create a group called *group3* and make both users be part of that group. This way we can share files:

    [root@rhel1 ~]# groupadd group3
    [root@rhel1 ~]# usermod -G group3 user1
    [root@rhel1 ~]# usermod -G group3 user2
    [root@rhel1 ~]# getent group group3
    group3:x:504:user1,user2


That looks good. Now let's switch to *user1* and create a new directory called *test* and make it group writable with *group3*:

    [root@rhel1 ~]# su - user1
    [user1@rhel1 ~]$ mkdir /tmp/test
    [user1@rhel1 ~]$ ls -ld /tmp/test
    drwxrwxr-x. 2 user1 user1 4096 Feb 8 07:00 /tmp/test
    [user1@rhel1 ~]$ chgrp group3 /tmp/test
    [user1@rhel1 ~]$ ls -ld /tmp/test
    drwxrwxr-x. 2 user1 group3 4096 Feb 8 07:00 /tmp/test


Let's do one more thing, let's set the **sgid** bit on the folder, this way any file created within that directory will inherit the group ownership. So here is file creation without the bit set:

    [user1@rhel1 ~]$ touch /tmp/test/file1
    [user1@rhel1 ~]$ ls -l /tmp/test/file1
    -rw-rw-r--. 1 user1 user1 0 Feb 8 07:03 /tmp/test/file1


Now let's set the **sgid** bit:

    [user1@rhel1 ~]$ chmod g+s /tmp/test
    [user1@rhel1 ~]$ ls -ld /tmp/test
    drwxrwsr-x. 2 user1 group3 4096 Feb 8 07:03 /tmp/test


notice the '**s**' in the permissions. Now creating a second file:

    [user1@rhel1 ~]$ touch /tmp/test/file2
    [user1@rhel1 ~]$ ls -l /tmp/test/file2
    -rw-rw-r--. 1 user1 group3 0 Feb 8 07:04 /tmp/test/file2


That looks perfect. Now anything created under that directory will be owned by *group3*. That last thing to look after is the **umask**. **Umask** controls the default permission of a newly created file. Let's check out the **umask** of our user:

    [user1@rhel1 ~]$ umask 002


That means a file will be created with permission of (777 - 002 = *775*). Which means that the the group has write permissions, which is good for our above setup. But what if our **umask** was 022? That would make our default permission be *755* and at this point the group wouldn't have write permission and this would defeat the purpose of sharing files with our group members. So let's change our **umask** and see what happens:

    [user1@rhel1 ~]$ umask 022
    [user1@rhel1 ~]$ touch /tmp/test/file3
    [user1@rhel1 ~]$ ls -l /tmp/test/file3
    -rw-r--r--. 1 user1 group3 0 Feb 8 07:16 /tmp/test/file3


Now the group can't write to the file, so if you're sharing files with groups members ensure your **umask** is set appropriately.

## RHEL File Permissions and Ownership

To get into permissions more, let's check out this old "[Red Hat Enterprise Linux Step By Step Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/rhcsa-and-rhce/Red_Hat_Enterprise_Linux-4-Step_by_Step_Guide-en-US.pdf)":

> **4.11. Ownership and Permissions**
>
> As a regular user, try to enter root's home directory by entering the command **cd /root/.** Note the error message:
>
>     bash$ cd /root/
>     Permission denied
>
>
> That was one demonstration of Linux security features. Linux, like UNIX, is a multi-user system and file permissions are one way the system protects against malicious tampering. One way to gain entry when you are denied permission is to enter the command **su -**. This is because whoever knows the root password has complete access However, switching to the superuser is not always convenient or recommended, since it is easy to make mistakes and alter important configuration files as the superuser.
>
> All directories are *owned* by the person who created them. You created "foo.txt" in your login directory, so foo.txt belongs to you. That means you can specify who is allowed to read the file, write to the file, or (if it is an application instead of a text file) who can execute the file. **Reading**, **writing**, and **executing** are the three main settings in permissions. Since users are placed into a group when their accounts are created, you can also specify whether certain groups can read, write to, or execute a file. Take a closer look at *foo.txt* with the **ls** command using the **-l** option:
>
>     [user1@rhel1 ~]$ ls -l foo.txt
>     -rw-rw-r--. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> A lot of detail is provided here. You can see who can **read (r)** and **write** to (**w**) the file as well as who created the file (**user1**), and to which group the owner belongs (**user1**). (By default, the name of your group is the same as your login name.) Other information to the right of the group includes the **file size**, **date**, and **time** of file creation, and **file name**. The first column shows current permissions; it has ten slots. The first slot represents the type of file. The remaining nine slots are actually three sets of permissions for three different categories of users. For example:
>
>     -rw-rw-r--
>
>
> Those three sets are the **owner** of the file, the **group** in which the file belongs, and "**others**," meaning other users on the system.
>
>     - (rw-) (rw-) (r--) 1 user1 user1
>
>
> The first item, which specifies the file type, will probably be one of the following:
>
> *   **d** a directory
> *   **-** a regular file (rather than directory or link)
> *   **l** a symbolic link to another program or file elsewhere on the system Others are possible, but are beyond the scope of this manual.
>
> Beyond the first item, in each of the following three sets, you may see one of the following:
>
> *   **r** file can be read
> *   **w** file can be written to
> *   **x** file can be executed (if it is a program)
> *   **-** specific permission has not been assigned When you see a dash in **owner**, **group**, or **others**, it means that particular permission has not been granted.
>
> Look again at the first column of foo.txt and identify its permissions.
>
>     ls -l foo.txt
>     -rw-rw-r--. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> The file's **owner** (in this case, **user1**) has permission to read and write to the file. The **group**, **user1**, has permission to read and write to *foo.txt*, as well. It is not a program, so neither the **owner** or the **group** has permission to **execute** it.

The command that allows you to change permissions of a file is called **chmod**. From the same guide:

> **4.11.1. The chmod Command**
>
> Use the **chmod** command to change permissions. This example shows how to change the permissions on foo.txt with the **chmod** command. The original file looks like this, with its initial permissions settings:
>
>     -rw-rw-r--. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> If you are the owner of the file or are logged into the root account, you can change any permissions for the **owner**, **group**, and **others**. Right now, the owner and group can read and write to the file. Anyone outside of the group can only read the file **(r-)**. In the following example, you want to allow everyone (**others**) to write to the file, so they can read it, write notes in it, and save it. That means you must change the "**others**" section of the file permissions:
>
>     [user1@rhel1 ~]$ chmod o+w foo.txt
>
>
> The **o+w** command tells the system you want to give **others** write permission to the file *foo.txt*. To check the results, list the file's details again. Now, the file looks like this:
>
>     [user1@rhel1 ~]$ ls -l foo.txt
>     -rw-rw-rw-. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> Now, everyone can read and write to the file. Think of these settings as a kind of shorthand when you want to change permissions with **chmod**, because all you really have to do is remember a few symbols and letters with the **chmod** command.Here is a list of what the shorthand represents:
>
> Identities
>
> *   **u** the user who owns the file (that is, the owner)
> *   **g** the group to which the user belongs
> *   **o** others (not the owner or the owner's group)
> *   **a** everyone or all (**u**, **g**, and **o**)
>
> Permissions
>
> *   **r** read access
> *   **w** write access
> *   **x** execute access
>
> Actions
>
> *   **+** adds the permission
> *   **-** removes the permission
> *   **=** makes it the only permission Here are some common examples of settings that can be used with
>
> **chmod**:
>
> *   **g+w** adds write access for the group
> *   **o-rwx** removes all permissions for others
> *   **u+x** allows the file owner to execute the file
> *   **a+rw** allows everyone to read and write to the file
> *   **ug+r** allows the owner and group to read the file
> *   **g=rx** allows only the group to read and execute (not write)
>
> By adding the **-R** option, you can change permissions for entire directory trees. Because you can not really "**execute**" a directory as you would an application, when you add (or remove) the **execute** permission for a directory, you are really allowing (or denying) permission to search through that directory

Another way of using **chmod** is with octal numbers, from the same guide:

> **4.11.2. Changing Permissions With Numbers**
>
> Another way to change permissions uses numeric representations. Go back to the original permissions for *foo.txt*:
>
>     [user1@rhel1 ~]$ ls -l foo.txt
>     -rw-rw-r--. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> Each permission setting can be represented by a numerical value:
>
> *   **r** = 4
> *   **w** = 2
> *   **x** = 1
> *   **-** = 0
>
> When these values are added together, the total is used to set specific permissions. For example, if you want **read** and **write** permissions, you would have a value of **6**; **4** (**read**) + **2** (**write**) = **6**. For *foo.txt*, here are the numerical permissions settings:
>
>     - (rw-) (rw-) (r--)
>
>
> The total for the **user** is six(**4**+**2**+**O**), the total for the **group** is six(**4**+**2**+**O**), and the total for **others** is four(**4**+**O**+**O**). The permissions setting is read as **664**. If you want to change *foo.txt* so those in your **group** do not have **write** access, but can still **read** the file, remove the access by subtracting two (**2**) from that set of numbers. The numerical values then become six, four, and four (**644**). To implement these new settings, type:
>
>     [user1@rhel1 ~]$ chmod 644 foo.txt
>
>
> Now verify the changes by listing the file. Type:
>
>     [user1@rhel1 ~]$ ls -l foo.txt
>     -rw-r--r--. 1 user1 user1 0 Feb 8 07:24 foo.txt
>
>
> Now, neither the **group** nor **others** have write permission to *foo.txt*.

The last thing that we should cover is the 'sticky' bits. From the old "[Red Hat Enterprise Linux 4 Introduction To System Administration](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/4/pdf/introduction_to_system_administration/red_hat_enterprise_linux-4-introduction_to_system_administration-en-us.pdf)":

> There are three such special permissions within Red Hat Enterprise Linux. They are:
>
> *   **setuid** — used only for binary files (applications), this permission indicates that the file is to be executed with the permissions of the owner of the file, and not with the permissions of the user executing the file (which is the case without **setuid**). This is indicated by the character **s** in the place of the **x** in the owner category. If the owner of the file does not have execute permissions, a capital **S** reflects this fact.
> *   **setgid** — used primarily for binary files (applications), this permission indicates that the file is executed with the permissions of the **group** owning the file and not with the permissions of the **group** of the user executing the file (which is the case without **setgid**). If applied to a directory, all files created within the directory are owned by the group owning the directory, and not by the group of the user creating the file. The setgid permission is indicated by the character **s** in place of the **x** in the group category. If the group owning the file or directory does not have execute permissions, a capital **S** reflects this fact.
> *   **sticky bit** — used primarily on directories, this bit dictates that a file created in the directory can be removed only by the user that created the file. It is indicated by the character **t** in place of the **x** in the everyone category. If the everyone category does not have execute permissions, the **T** is capitalized to reflect this fact. Under Red Hat Enterprise Linux, the sticky bit is set by default on the **/tmp/** directory for exactly this reason.

Hopefully the above helps with permissions.

### Sharing Files with Group Members in RHEL

We discussed sharing files with group members by using the **sgid** bit on a folder and with appropriate **umask** settings. Another way of sharing files is to setup a group password and allow users to login to that group. From "[Red Hat Enterprise Linux 4 Introduction To System Administration](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/4/pdf/introduction_to_system_administration/red_hat_enterprise_linux-4-introduction_to_system_administration-en-us.pdf)":

> **6.3.2.4 . /etc/gshadow**
>
> The **/etc/gshadow** file is readable only by the root user and contains an encrypted password for each group, as well as group membership and administrator information. Just as in the **/etc/group** file, each group's information is on a separate line. Each of these lines is a colon delimited list including the following information:
>
> *   **Group name** — The name of the group. Used by various utility programs as a human-readable identifier for the group.
> *   **Encrypted password** — The encrypted password for the group. If set, non-members of the group can join the group by typing the password for that group using the **newgrp** command. If the value of this field is **!**, then no user is allowed to access the group using the **newgrp** command. A value of **!!** is treated the same as a value of **!** — however, it also indicates that a password has never been set before. If the value is null, only group members can log into the group.
> *   **Group administrators** — Group members listed here (in a comma delimited list) can add or remove group members using the **gpasswd** command.
> *   **Group members** — Group members listed here (in a comma delimited list) are regular, nonadministrative members of the group. Here is an example line from **/etc/gshadow**:
>     `general:!!:shelley:juan,bob`
>     This line shows that the **general** group has no password and does not allow non-members to join using the **newgrp** command. In addition, **shelley** is a group administrator, and **juan** and **bob** are regular, non-administrative members.

So let's make **user1** be an administrator of **group1**:

    [root@rhel1 ~]# gpasswd -A user1 group1
    [root@rhel1 ~]# getent gshadow group1
    group1:!:user1:


Also let's add **user1** as a member as well:

    [root@rhel1 ~]# gpasswd -a user1 group1
    Adding user user1 to group group1
    [root@rhel1 ~]# getent gshadow group1
    group1:!:user1:user1


Now let's switch to that user and set the password for the group:

    [root@rhel1 ~]# su - user1
    [user1@rhel1 ~]$ gpasswd group1
    Changing the password for group group1
    New Password:
    Re-enter new password:
    [user1@rhel1 ~]$ getent group group1
    group1:x:502:user1


We now see an '**x**' instead of an '**!**', so we know the password is set. Now let's create a new directory called **test2** and make the group owner **group1**:

    [user1@rhel1 ~]$ mkdir /tmp/test2
    [user1@rhel1 ~]$ chgrp group1 /tmp/test2
    [user1@rhel1 ~]$ ls -ld /tmp/test2
    drwxrwxr-x. 2 user1 group1 4096 Feb 9 01:19 /tmp/test2


That looks good, now let's become **user2** and login to **group1** with the password that we just set:

    [root@rhel1 ~]# su - user2
    [user2@rhel1 ~]$ id -a
    uid=501(user2) gid=501(user2) groups=501(user2),503(group2)


Just checking out current **gid**:

    [user2@rhel1 ~]$ id -g
    501


We can see that currently we are part of **user2** (our private group) and **group2**, which is what we setup above. Now let's login to **group1**:

    [user2@rhel1 ~]$ newgrp group1
    Password:
    [user2@rhel1 ~]$ id -g
    502


Now creating a new file under our **tmp** directory:

    [user2@rhel1 ~]$ umask 0002
    [user2@rhel1 ~]$ touch /tmp/test2/file
    [user2@rhel1 ~]$ ls -l /tmp/test2/file
    -rw-rw-r-- 1 user2 group1 0 Feb 9 04:18 /tmp/test2/file


We accomplished the same thing without using the **sgid** bit.

### RHEL Password Aging

Getting back to the "[Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/pdf/deployment_guide/red_hat_enterprise_linux-6-deployment_guide-en-us.pdf)":

> **3.3.3. Enabling Password Aging**
>
> For security reasons, it is advisable to require users to change their passwords periodically. This can either be done when adding or editing a user on the Password Info tab of the User Manager application, or by using the **chage** command. To configure password expiration for a user from a shell prompt, run the following command as root:
>
>      chage [options] username
>
>
> …where options are command line options as described in Table 3.4, “chage command line options”. When the **chage** command is followed directly by a username (that is, when no command line options are specified), it displays the current password aging values and allows you to change them interactively. ![chage options RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/chage_options.png)
>
> You can configure a password to expire the first time a user logs in. This forces users to change passwords immediately.
>
> 1.  Set up an initial password. There are two common approaches to this step: you can either assign a default password, or you can use a null password. To assign a default password, type the following at a shell prompt as root:
>
>         passwd username
>         juan:x:501:501::/home/juan:/bin/bash
>
>
>     To assign a null password instead, use the following command:
>        
>         passwd -d username
>
>
> 2.  Force immediate password expiration by running the following command as root:
>
>         chage -d 0 username
>
>
>     This command sets the value for the date the password was last changed to the **epoch** (January 1, 1970). This value forces immediate password expiration no matter what password aging policy, if any, is in place. Upon the initial log in, the user is now prompted for a new password.

So let's check out the policies our **user1**:

    [root@rhel1 ~]# chage -l user1
    Last password change : Feb 08, 2013
    Password expires : never
    Password inactive : never
    Account expires : never
    Minimum number of days between password change : 0
    Maximum number of days between password change : 99999
    Number of days of warning before password expires : 7


All of the above settings are stored in **/etc/shadow**. Let's set the password to expire today, and set a warning message to be displayed when the password is expiring one day before the expiration date:

    [root@rhel1 ~]# date Sat Feb 9 01:55:28 MST 2013
    [root@rhel1 ~]# chage -E 2013-02-09 -M 1 user1
    [root@rhel1 ~]# chage -l user1
    Last password change : Feb 09, 2013
    Password expires : Feb 10, 2013
    Password inactive : never
    Account expires : Feb 09, 2013
    Minimum number of days between password change : 0
    Maximum number of days between password change : 1
    Number of days of warning before password expires : 7


Now let's switch user to **user1**, and see if we get the message:

    [user2@rhel1 ~]$ su - user1
    Password:
    Warning: your password will expire in 1 day


You can also manually lock user accounts by using the **passwd** utility:

    [root@rhel1 ~]# getent shadow user1
    user1:$6$IPcp2gLd$mhQKFrXYQDGFPDEDDXeOfz5ObWCMpAKvK4X/3fTUknO:15745:0::7:::
    [root@rhel1 ~]# passwd -l user1
    Locking password for user user1.
    Success
    [root@rhel1 ~]# getent shadow user1
    user1:!!$6$IPcp2gLd$mhQKFrXYQDGFPDEDDXeOfz5ObWCMpAKvK4X/3fTUkn0:15745:0::7:::


Notice the '**!!**' in front of the hash of the password, signifying that the account is locked.

### RHEL Check Integrity of Password and Group Files

The other two utilities mentioned in the guide were **pwck** and **gpwck**. Both utilities just check to see if **/etc/passwd**, **/etc/shadow** and **/etc/group**, **/etc/gshadow** have proper syntax and are in sync. Here the commands run on the test machines:

    [root@rhel1 ~]# pwck
    user 'adm': directory '/var/adm' does not exist
    user 'uucp': directory '/var/spool/uucp' does not exist
    user 'gopher': directory '/var/gopher' does not exist
    user 'ftp': directory '/var/ftp' does not exist
    user 'saslauth': directory '/var/empty/saslauth' does not exist
    pwck: no changes
    [root@rhel1 ~]# grpck
    [root@rhel1 ~]#


It looks like for some users the home directory doesn't exist, but that is okay and my groups and group password are okay.

### RHEL System Authentication

Lastly there is "System Authentication", from the deployment guide:

> **Chapter 10. Configuring Authentication**
>
> Authentication is the way that a user is identified and verified to a system. The authentication process requires presenting some sort of identity and credentials, like a username and password. The credentials are then compared to information stored in some data store on the system. In Red Hat Enterprise Linux, the Authentication Configuration Tool helps configure what kind of data store to use for user credentials, such as **LDAP**. For convenience and potentially part of single sign-on, Red Hat Enterprise Linux can use a central daemon to store user credentials for a number of different data stores. The System Security Services Daemon (**SSSD**) can interact with **LDAP**, **Kerberos**, and external applications to verify user credentials. The Authentication Configuration Tool can configure **SSSD** along with **NIS**, **Winbind**, and **LDAP**, so that authentication processing and caching can be combined.
>
> **10.1. Configuring System Authentication** When a user logs into a Red Hat Enterprise Linux system, that user presents some sort of credential to establish the user identity. The system then checks those credentials against the configured authentication service. If the credentials match and the user account is active, then the user is authenticated. (Once a user is authenticated, then the information is passed to the access control service to determine what the user is permitted to do. Those are the resources the user is authorized to access.) The information to verify the user can be located on the local system or the local system can reference a user database on a remote system, such as **LDAP** or **Kerberos**. The system must have a configured list of valid account databases for it to check for user authentication. On Red Hat Enterprise Linux, the Authentication Configuration Tool has both GUI and command-line options to configure any user data stores. A local system can use a variety of different data stores for user information, including Lightweight Directory Access Protocol (**LDAP**), Network Information Service (**NIS**), and **Winbind**. Additionally, both **LDAP** and **NIS** data stores can use **Kerberos** to authenticate users.

First let's check out NIS:

> **10.1.2.2. Configuring NIS Authentication**
>
> Install the **ypbind** package. This is required for **NIS** services, but is not installed by default.
>
>     [root@server ~]# yum install ypbind
>
>
> When the ypbind service is installed, the **portmap** and **ypbind** services are started and enabled to start at boot time ... ...
>
> **10.1.4 .3. Configuring NIS User Stores**
>
> To use a **NIS** identity store, use the **-enablenis**. This automatically uses **NIS** authentication, unless the **Kerberos** parameters are explicitly set, so it uses **Kerberos** authentication. The only parameters are to identify the **NIS** server and **NIS** domain; if these are not used, then the **authconfig** service scans the network for **NIS** servers.
>
>     authconfig --enablenis --nisdomain=EXAMPLE --nisserver=nis.example.com --update
>

The **authconfig** command line can get pretty advanced, so I decided to use **authconfig-tui** just for ease and time saving. So setup **NIS** authentication on our test machine:

    [root@rhel1 ~]# yum install ypbind
    ...
    ...
    Installed: ypbind.i686 3:1.20.4-29.el6
    Dependency Installed:
    libgssglue.i686 0:0.1-11.el6 libtirpc.i686 0:0.2.1-3.el6 rpcbind.i686 0:0.2.0-8.el6 yp-tools.i686 0:2.9-10.el6
    Complete!


Let's enable both daemons to be started on boot:

    [root@rhel1 ~]# chkconfig rpcbind on
    [root@rhel1 ~]# chkconfig ypbind on


Now let's configure the machine to authenticate with a **NIS** server (itself for now):

![authconfig tui NIS RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/authconfig_tui_NIS.png)

![auth tui NIS settings RHCSA and RHCE Chapter 7 User Administration](https://github.com/elatov/uploads/raw/master/2013/02/auth_tui_NIS_settings.png)

If I had actually setup a **NIS** server, the rest would just fall into place. After I hit next **authconfig-tui** tried to start the appropriate services, but failed, cause there was no **NIS** server:

    [root@rhel1 ~]# authconfig-tui
    Starting rpcbind: rpcbind
    Starting NIS service: ypbind
    Binding NIS service: .....................
    Shutting down NIS service: ypbind


To confirm the settings were applied, we can check out the **nsswitch.conf** file:

    [root@rhel1 ~]# grep -E '^passwd|^shadow|^group' /etc/nsswitch.conf
    passwd: files nis
    shadow: files nis
    group: files nis


We can also see the **NIS** settings by looking at **/etc/yp.conf**:

    [root@rhel1 ~]# grep -v -E '^#|^$' /etc/yp.conf
    domain local.com
    server 192.168.1.110


Similar steps can be taken to setup **LDAP** authentication. From the same guide:

> **10.1.2.1. Configuring LDAP Authentication**
>
> Either the **openldap-clients** package or the sssd package is used to configure an LDAP server for the user database. Both packages are installed by default.
>
> .. ..
>
> **10.1.4 .2. Configuring LDAP User Stores**
>
> To use an LDAP identity store, use the **-enableldap**. To use LDAP as the authentication source, use **-enableldapauth** and then the requisite connection information, like the LDAP server name, base DN for the user suffix, and (optionally) whether to use TLS. The **authconfig** command also has options to enable or disable RFC 2307bis schema for user entries, which is not possible through the Authentication Configuration UI. Be sure to use the full **LDAP** URL, including the protocol (*ldap* or *ldaps*) and the port number. Do not use a secure **LDAP** URL (*ldaps*) with the **-enableldaptls** option.
>
>     authconfig --enableldap --enableldapauth --ldapserver=ldap://ldap.example.com:389,ldap://ldap2.example.com:389 --ldapbasedn="ou=people,dc=example,dc=com" --enableldaptls --ldaploadcacert=https://ca.server.example.com/caCert.crt --update
>

### Related Posts

- [RHCSA and RHCE Chapter 10 - The Kernel](/2013/07/rhcsa-and-rhce-chapter-10-the-kernel/)
- [RHCSA and RHCE Chapter 9 - System Logging, Monitoring, and Automation](/2013/06/rhcsa-and-rhce-chapter-9-system-logging-monitoring-and-automation/)
- [RHCSA and RHCE Chapter 8 Network Installs](/2013/03/rhcsa-and-rhce-chapter-8-network-installs/)

