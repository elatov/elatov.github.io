---
title: Using PolKit to Change Screen Brightness on a Mac BookPro Running Fedora 19
author: Karim Elatov
layout: post
permalink: /2013/08/using-polkit-to-change-screen-brightness-on-a-mac-bookpro-running-fedora-19/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1650332528
categories:
  - Home Lab
  - OS
tags:
  - MacBookPro
  - PolicyKit
  - sudo
---
I wanted to create some keyboard short cuts to change the brightness of my screen (similar to what I did [here](http://virtuallyhyper.com/2013/03/update-chrubuntu-12-04-to-13-04-on-the-samsung-chromebook/)). On my Fedora install I didn't have any gnome components installed, I was just using **lightdm** with **icewm**.

## Change Screen Brightness with Sysfs

First I discovered that using **sysfs**, I can change the brightness of my screen. To do this, first check out the current level:

    elatov@kmac:~$cat /sys/class/backlight/gmux_backlight/brightness
    3700


you can also check out the maximum brightness level like so:

    elatov@kmac:~$cat /sys/class/backlight/gmux_backlight/max_brightness
    82311


Then increase the value by about 700 to increase the brightness and vice versa to decrease the brightness. So to increase the brightness you can run the following:

    elatov@kmac:~$sudo su -c 'echo 4400 > /sys/class/backlight/gmux_backlight/brightness'


You can then confirm that the brightness changed (other than visually) by checking the value again:

    elatov@kmac:~$cat /sys/class/backlight/gmux_backlight/brightness
    4400


and to decrease the brightness you can do the following:

    elatov@kmac:~$sudo su -c 'echo 3700 > /sys/class/backlight/gmux_backlight/brightness'


## Using *sudo* to Change the Brightness Level

I put together a quick script to change the brightness and placed it under **/usr/local/bin**. Here is how the script looked like:

    elatov@kmac:~$cat /usr/local/bin/ch_br
    #!/bin/bash
    cur_bri=$(/usr/bin/cat /sys/class/backlight/gmux_backlight/brightness)

    if [ $1 == "up" ] ; then
        bri=$(($cur_bri+700))
        `echo $bri > /sys/class/backlight/gmux_backlight/brightness`
    fi

    if [ $1 == "down" ] ; then
        bri=$(($cur_bri-700))
        `echo $bri > /sys/class/backlight/gmux_backlight/brightness`
    fi


Since we are editing a file owned by root we need to use **sudo** to elevate our privileges. I was going to use that script with a keyboard shortcut, so I needed to allow myself to execute that script with **sudo** without a password. I was already part of the **wheel** group, which allowed me to run any command with **sudo**. Each distribution has a different group for this, you can check what group you need to belong to by checking the contents of **/etc/sudoers**:

    elatov@kmac:~$sudo grep wheel /etc/sudoers
    ## Allows people in group wheel to run all commands
    %wheel  ALL=(ALL)   ALL


and of course I was part of the wheel group:

    elatov@kmac:~$groups
    elatov wheel


Lastly, you can check what you can run with **sudo** by running the following:

    elatov@kmac:~$sudo -l
    User elatov may run the following commands on this host:
        (ALL) ALL


So I could run any commands, but I would need to type my password to authenticate myself. To add a rule to **sudoers** too allow me to execute my script as root without typing my password, I did the following:

    elatov@kmac:~$sudo vi /etc/sudoers.d/mac_brig


and I placed the following into the file:

    Cmnd_Alias CMDS = /usr/local/bin/ch_br *
    elatov ALL = NOPASSWD: CMDS


then checking my **sudo** list, I saw the following:

    elatov@kmac:~$sudo -l
    User elatov may run the following commands on this host:
        (ALL) ALL
        (root) NOPASSWD: /usr/local/bin/ch_br *


Now when I ran the following:

    elatov@kmac:~$sudo /usr/local/bin/ch_br up


and it just increased the brightness without asking me for my password.

## IceWM KeyBoard Shortcuts

I wanted to create keyboard shortcuts which would decrease the brightness upon typing "Command+F1" and would increase brightness by typing "Command+F2". On Linux the Mac Command key shows up as the Windows Super Key. So adding the following to my **~/.icewm/keys** file should've taken care of this:

    elatov@kmac:~$grep ch_br .icewm/keys
    key "Super+F1"  sudo /usr/local/bin/ch_br down
    key "Super+F2"  sudo /usr/local/bin/ch_br up


But I quickly realized that running any command with **sudo** from the **keys** file didn't work out. So I decided to look for an alternative to **sudo** and I found **PolKit**.

## PolKit

From this ArchWiki page:

> PolicyKit is an application-level toolkit for defining and handling the policy that allows unprivileged processes to speak to privileged processes: It is a framework for centralizing the decision making process with respect to granting access to privileged operations for unprivileged applications. PolicyKit is specifically targeting applications in rich desktop environments on multi-user UNIX-like operating systems. It does not imply or rely on any exotic kernel features.

PolicyKit has gone through a lot of changes and is now called PolKit. From the same wiki page:

> In the development of PolicyKit, major changes were introduced around version 0.92. In order to make the distinction clear between the way the old and the new versions worked, the new ones are referred to as 'polkit' rather than PolicyKit. Searching for PolicyKit on the web will mostly point to outdated documentation and lead to confusion and frustration. The main distinction between PolicyKit and polkit is the abandonment of single-file configuration in favour of directory-based configuration, i.e. there is no PolicyKit.conf.

From [this](http://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html) freedesktop page, here is a good architecture of PolKit:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/08/polkit_arch.png" alt="polkit arch Using PolKit to Change Screen Brightness on a Mac BookPro Running Fedora 19" width="602" height="546" class="alignnone size-full wp-image-9329" title="Using PolKit to Change Screen Brightness on a Mac BookPro Running Fedora 19" />](http://virtuallyhyper.com/wp-content/uploads/2013/08/polkit_arch.png)

From the initial Arch wiki page, here is the structure of PolKit:

> PolicyKit definitions can be divided into three kinds:
>
> *   **Actions** are defined in XML *.policy* files located in **/usr/share/polkit-1/actions**. Each action has a set of default permissions attached to it (e.g. you need to identify as an administrator to use the GParted action). The defaults can be overruled but editing the actions files is NOT the correct way. The files installed under **/usr/share/polkit-1/actions** are not meant to be modified. Instead, you should modify the authorities under **/etc/polkit-1/localauthority/50-local.d**.
> *   **Authorities** are defined in INI-like **.pkla** files. They are found in two places: 3rd party packages can use **/var/lib/polkit-1** (though few if any do) and **/etc/polkit-1** is for local configuration. The **.pkla** files designate a subset of users, refer to one (or more) of the actions specified in the actions files and determine with what restrictions these actions can be taken by that/those user(s). As an example, an authority file could overrule the default requirement for all users to authenticate as an admin when using GParted, determining that some specific user doesn't need to. Or isn't allowed to use GParted at all.
> *   **Admin identities** are set in **/etc/polkit-1/localauthority.conf.d**. One of the basic points of using PolicyKit is determining whether or not a user needs to authenticate (possibly as an administrative user) or not in order to get permission to carry out the action. PolicyKit therefore has a specific configuration for deciding if the user trying to carry out an action is or is not an administrative user. Common definitions are 'only root user' or 'all members of wheel' (the Arch default).

### PolKit Actions

From the Arch wiki page:

> Each action is defined in an <action> tag in a .policy file. The org.archlinux.pkexec.gparted.policy contains a single action and looks like this:</action>
>
>     < ?xml version="1.0" encoding="UTF-8"?>
>     <!DOCTYPE policyconfig PUBLIC
>      "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
>      "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
>     <policyconfig>
>
>       <action id="org.archlinux.pkexec.gparted">
>         <message>Authentication is required to run the GParted Partition Editor</message>
>         <icon_name>gparted</icon_name>
>         <defaults>
>           <allow_any>auth_admin</allow_any>
>           <allow_inactive>auth_admin</allow_inactive>
>           <allow_active>auth_admin</allow_active>
>         </defaults>
>         <annotate key="org.freedesktop.policykit.exec.path">/usr/sbin/gparted</annotate>
>         <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
>       </action>
>
>     </policyconfig>
>
>
> The attribute **id** is the actual command sent to **dbus**, the **message** tag is the explanation to the user when authentification is required and the **icon_name** is sort of obvious. The default tag is where the permissions or lack thereof are located. It contains three settings: **allow_any**, **allow_inactive**, and **allow_active**. Inactive sessions are generally remote sessions (SSH, VNC, etc.) whereas active sessions are logged directly into the machine on a TTY or an X display. Allow_any is the setting encompassing both scenarios. For each of these settings the following options are available:
>
> *   **no**: The user is not authorized to carry out the action. There is therefore no need for authentification.
> *   **yes**: The user is authorized to carry out the action without any authentification.
> *   **auth_self**: Authentication is required but the user need not be an administrative user.
> *   **auth_admin**: Authentication as an administrative user is require.
> *   **auth_self_keep**: The same as auth_self but, like sudo, the authorization lasts a few minutes.
> *   **auth_admin_keep**: The same as auth_admin but, like sudo, the authorization lasts a few minutes.

You can list all the defined actions by running **pkaction**:

    elatov@kmac:~$pkaction  | head
    dk.yumex.backend.pkexec.run
    net.reactivated.fprint.device.enroll
    net.reactivated.fprint.device.setusername
    net.reactivated.fprint.device.verify
    org.blueman.bluez.config
    org.blueman.dhcp.client
    org.blueman.hal.manager
    org.blueman.network.setup
    org.fedoraproject.config.date.pkexec.run
    org.fedoraproject.config.keyboard.pkexec.run


If you want more information about an action, you can run the following:

    elatov@kmac:~$pkaction --action-id org.fedoraproject.config.date.pkexec.run --verbose
    org.fedoraproject.config.date.pkexec.run:
      description:       Run System Config Date
      message:           Authentication is required to run system-config-date
      vendor:            System Config Date
      vendor_url:        http://fedorahosted.org/system-config-date
      icon:              system-config-date
      implicit any:      no
      implicit inactive: no
      implicit active:   auth_admin
      annotation:        org.freedesktop.policykit.exec.path -> /usr/share/system-config-date/system-config-date.py
      annotation:        org.freedesktop.policykit.exec.allow_gui -> true


So if a regular user ran the **system-config-date** command with **pkexec** they would have to authenticate as an *admin* identity.

### PolKit Authorities

Again from the same wiki page:

> Authorizations that overrule the default settings are laid out in a set of directories as described above. For all purposes relating to personal configuration of a single system, only **/etc/polkit-1/localauthority/50-local.d** should be used. The authority files are read in alphabetical/numerical order, where later files take precedence, so that one configuration file can be relied upon to overrule another, e.g.
>
>     10_allow_all_users_group_members_to_automount_without_authentification.pkla
>     15_but_not_jack.pkla
>
>
> The layout of the **.pkla** files is fairly self-explanatory:
>
>     [Ban users jack and jill from using gparted]
>     Identity=unix-user:jack;unix-user:jill
>     Action=org.archlinux.pkexec.gparted
>     ResultAny=no
>     ResultInactive=no
>     ResultActive=no
>
>
> An authorization needs to be preceded by a heading enclosed in square brackets. The follows an identification with pairs of **unix-user** or **unix-group** and the name. Use semicolons to separate the pairs to include more than one user or group. The designating name of the action is the one from the action's id attribute in **/usr/share/polkit-1/actions**. The three Result-settings mirror those from the action definition. Here we have overruled the default **auth_admin** setting and disallowed *jack* and *jill* from running **gparted**.

### PolKit Admin Identities

From the wiki page:

> Like the authorities files, configuration works by letting the last read file take precedence over earlier ones. The default configuration for admin identities is contained in the file **50-localauthority.conf** so any changes to that configuration should be made by copying the file to, say, **60-localauthority.conf** and editing that file.
>
>     /etc/polkit-1/localauthority.conf.d/50-localauthority.conf
>     # Configuration file for the PolicyKit Local Authority.
>     #
>     # DO NOT EDIT THIS FILE, it will be overwritten on update.
>     #
>     # See the pklocalauthority(8) man page for more information
>     # about configuring the Local Authority.
>     #
>
>     [Configuration]
>     AdminIdentities=unix-group:wheel
>
>
> The only part to edit (once copied) is the right part of the equation: As whom should a user authenticate when asked to authenticate as an administrative user? If she herself is a member of the group designated as admins, she only need enter her own password. If some other user, e.g. **root**, is the only admin identity, she would need to enter in root's password. The format of the user identification is the same as the one used in designating authorities. The Arch default is to make all members of the group **wheel** administrators.

### PolKit in Different Linux Distributions

Different distributions use *PolKit* in different ways. On the Fedora laptop, I see that the rules are utilized rather that static authority files. For example we can see that there are no **localauthority** configurations files:

    [root@kmac ~]# tree /etc/polkit-1/
    /etc/polkit-1/
    ├── localauthority
    │   ├── 10-vendor.d
    │   ├── 20-org.d
    │   ├── 30-site.d
    │   ├── 50-local.d
    │   └── 90-mandatory.d
    ├── localauthority.conf.d
    └── rules.d
        ├── 49-polkit-pkla-compat.rules
        └── 50-default.rules

    8 directories, 2 files


Notice only empty directories exist for the **localauthority** configurations. But if we check the default rules file, we see the following:

    [root@kmac ~]# tail -3 /etc/polkit-1/rules.d/50-default.rules
    polkit.addAdminRule(function(action, subject) {
        return ["unix-group:wheel"];
    });


So anyone part of the **wheel** group has admin authority, similar to what **sudoers** does. On my Ubuntu laptop, I see the **localauthority** files used.

    elatov@crbook:~$tree /etc/polkit-1/
    /etc/polkit-1/
    |-- localauthority
    |   |-- 10-vendor.d
    |   |-- 20-org.d
    |   |-- 30-site.d
    |   |-- 50-local.d
    |   `-- 90-mandatory.d
    |-- localauthority.conf.d
    |   |-- 50-localauthority.conf
    |   `-- 51-ubuntu-admin.conf
    `-- nullbackend.conf.d
        `-- 50-nullbackend.conf

    8 directories, 3 files


Now checking out the actual files:

    elatov@crbook:~$tail -2 /etc/polkit-1/localauthority.conf.d/50-localauthority.conf
    [Configuration]
    AdminIdentities=unix-user:0


and here is the other file:

    elatov@crbook:~$tail -2 /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
    [Configuration]
    AdminIdentities=unix-group:sudo;unix-group:admin


So in this case, anyone part of the **sudo** or **admin** groups can authenticate as them selves and will be considered *admins*. Or anyone that can provide the root password will also be considered an *admin*.

### Adding a PolKit Action

Here is what I did to add an action to PolKit. First I created the file, like so:

    elatov@kmac:~$sudo vi /usr/share/polkit-1/actions/org.fedora.pkexec.chbr.policy


and I added the following to the file:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE policyconfig PUBLIC
     "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
     "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
    <policyconfig>

      <action id="org.fedora.pkexec.chbr">
        <message>Authentication is required to Change Brightness</message>
        <icon_name>battery</icon_name>
        <defaults>
          <allow_any>no</allow_any>
          <allow_inactive>no</allow_inactive>
          <allow_active>yes</allow_active>
        </defaults>
        <annotate key="org.freedesktop.policykit.exec.path">/usr/local/bin/ch_br</annotate>
      </action>

    </policyconfig>


I then confirmed the action was added:

    elatov@kmac:~$pkaction  | grep chbr
    org.fedora.pkexec.chbr


and I was also able to get all the information regarding that action:

    elatov@kmac:~$pkaction  --action-id org.fedora.pkexec.chbr --verbose
    org.fedora.pkexec.chbr:
      description:
      message:           Authentication is required to Change Brightness
      vendor:
      vendor_url:
      icon:              battery
      implicit any:      no
      implicit inactive: no
      implicit active:   yes
      annotation:        org.freedesktop.policykit.exec.path -> /usr/local/bin/ch_br


I was then able to run the following:

    elatov@kmac:~$pkexec /usr/local/bin/ch_br up


and the brightness changed without asking me for a password. If I wanted, I could change this line from the policy:

    <allow_active>yes</allow_active>


to this

    <allow_active>auth_admin</allow_active>


and since I was part of the **wheel** group, I would be able to authenticate as myself and be authorized to run the command. Here is how that would look like:

    elatov@kmac:~$pkexec /usr/local/bin/ch_br up
    ==== AUTHENTICATING FOR org.fedora.pkexec.chbr ===
    Authentication is required to Change Brightness
    Authenticating as: KE (elatov)
    Password:
    ==== AUTHENTICATION COMPLETE ===


But if did that, I wouldn't be able to use my keyboard short cuts.

## Change IceWM KeyBoard Shortcuts to Use *pkexec* Rather Than *sudo*

This was pretty simple, here is how my config looked like after the change:

    elatov@kmac:~$grep ch_br .icewm/keys
    key "Super+F1"  pkexec /usr/local/bin/ch_br down
    key "Super+F2"  pkexec /usr/local/bin/ch_br up


After restarting IceWM, I was able to modify the brightness level with "Command+F1" and "Command+F2" without any issues.

## PolKit Vs Sudo

There is an ongoing battle amongst Linux users who say that **sudo** is more secure. From the Arch Wiki page:

> PolicyKit operates on top of the existing permissions systems in linux - group membership, administrator status - it does not replace them. The example above prohibited the user jack from using the GParted action, but it does not preclude him running GParted by some means that do not respect PolicyKit, e.g. the command line. Therefore it's probably better to use PolicyKit to expand access to priviledged services for unpriviledged users, rather than to try using it to curtail the rights of (semi-)privileged users. For security purposes, the sudoers file is still the way to go.

From [this](http://en.wikipedia.org/wiki/Polkit) wikipedia page:

> Whilst contested by its developer, polkit is criticized for contravening the Unix philosophy of doing one task and doing it well as it has a primary task of restricting root processes as an 'authority' and a secondary but easily mistaken for its primary task of allowing users to obtain temporary privileges 'authorization'.
>
> Polkit and its predecessor have stirred up much debate in being criticized for generalizing security functions (actions) and contravening the more code equals more bugs philosophy. The idea being to allow greater peer review of the code running as root, but this requires more code to run as root in itself. So whereby smaller and less popular projects may gain security initially from using polkit. Its continued usage actually limits the potential of an application to be as secure as possible when compared to privilege separated processes utilizing privilege dropping (OpenSSH, truecrypts core service). Therefore cross pollination of reviewed to be secure code itself adaptable to smaller projects specific requirements produces more secure programs but with the added risk of being more likely to be left un-maintaned (unlikely for code running as root which should be as short as possible and need little maintenance in any case).

I do agree that **sudoers** is easier to use and configure, but once you grasp all the PolKit concepts it's not that bad. I think PolKit is not as old/established as **sudo** but it looks like a lot more of different OS aspects are starting to support/include it. Also check out "[Assigning Privileges with sudo and PolicyKit](http://www.admin-magazine.com/Articles/Assigning-Privileges-with-sudo-and-PolicyKit)" for a great comparison of the two.

## Mac Book Pro Keyboard Backlight Brightness with Sysfs

You can use a similar method as above to create keyboard shorts to change brightness of the keyboard backlight. Here is the manual command to change it on the fly:

    $ sudo su -c 'echo 8 > /sys/class/leds/smc::kbd_backlight/brightness'


