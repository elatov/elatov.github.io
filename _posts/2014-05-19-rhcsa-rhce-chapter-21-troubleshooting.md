---
title: "RHCSA and RHCE Chapter 21 - Troubleshooting"
author: Karim Elatov
layout: post
permalink: "/2014/05/rhcsa-rhce-chapter-21-troubleshooting/"
categories: ['os', 'certifications', 'home_lab', 'networking', 'rhcsa_rhce']
tags: ['mbr', 'grub', 'linux', 'ip_routing', 'rhel', 'linux_rescue']
---


We covered a lot of these over the course of all the chapters. But here is a quick review.

### Reset Root Password

From the [Installation Guide][1]:

> What can you do if you forget your root password? To reset it to a different password, boot into **rescue mode** or **single-user** mode, and use the **passwd** command to reset the root password.

#### Booting into Rescue Mode

From the same guide:

> Rescue mode provides the ability to boot a small Red Hat Enterprise Linux environment entirely from CD-ROM, or some other boot method, instead of the system's hard drive.
>
> As the name implies, rescue mode is provided to rescue you from something. During normal operation, your Red Hat Enterprise Linux system uses files located on your system's hard drive to do everything — run programs, store your files, and more.
>
> However, there may be times when you are unable to get Red Hat Enterprise Linux running completely enough to access files on your system's hard drive. Using rescue mode, you can access the files stored on your system's hard drive, even if you cannot actually run Red Hat Enterprise Linux from that hard drive.
>
> To boot into rescue mode, you must be able to boot the system using one of the following methods:
>
> *   By booting the system from a boot CD-ROM or DVD.
> *   By booting the system from other installation boot media, such as USB flash devices.
> *   By booting the system from the Red Hat Enterprise Linux installation DVD.
>
> Once you have booted using one of the described methods, add the keyword rescue as a kernel parameter. For example, for an x86 system, type the following command at the installation boot prompt:
>
>     linux rescue
>
>
> If your system requires a third-party driver provided on a driver disc to boot, load the driver with the additional option dd:
>
>     linux rescue dd
>
>
> If a driver that is part of the Red Hat Enterprise Linux 6.5 distribution prevents the system from booting, blacklist that driver with the **rdblacklist** option. For example, to boot into rescue mode without the foobar driver, run:
>
>     linux rescue rdblacklist=foobar
>
>
> You are prompted to answer a few basic questions, including which language to use. It also prompts you to select where a valid rescue image is located. Select from **Local CD-ROM**, **Hard Drive**, **NFS image**, **FTP**, or **HTTP**. The location selected must contain a valid installation tree, and the installation tree must be for the same version of Red Hat Enterprise Linux as the Red Hat Enterprise Linux disk from which you booted. If you used a boot CD-ROM or other media to start rescue mode, the installation tree must be from the same tree from which the media was created.
>
> If you select a **rescue** image that does not require a network connection, you are asked whether or not you want to establish a network connection. A network connection is useful if you need to backup files to a different computer or install some RPM packages from a shared network location, for example.
>
> The following message is displayed:
>
> *   The rescue environment will now attempt to find your Linux installation and mount it under the directory **/mnt/sysimage**. You can then make any changes required to your system. If you want to proceed with this step choose 'Continue'. You can also choose to mount your file systems read-only instead of read-write by choosing 'Read-only'. If for some reason this process fails you can choose 'Skip' and this step will be skipped and you will go directly to a command shell.
>
> If you select **Continue**, it attempts to mount your file system under the directory **/mnt/sysimage/**. If it fails to mount a partition, it notifies you. If you select Read-Only, it attempts to mount your file system under the directory **/mnt/sysimage/**, but in read-only mode. If you select **Skip**, your file system is not mounted. Choose **Skip** if you think your file system is corrupted.
>
> Once you have your system in rescue mode, a prompt appears on VC (virtual console) 1 and VC 2 (use the **Ctrl-Alt-F1** key combination to access VC 1 and **Ctrl-Alt-F2** to access VC 2):
>
>     sh-3.00b#
>
>
> If you selected **Continue** to mount your partitions automatically and they were mounted successfully, you are in single-user mode.
>
> Even if your file system is mounted, the default root partition while in rescue mode is a temporary root partition, not the root partition of the file system used during normal user mode (runlevel 3 or 5). If you selected to mount your file system and it mounted successfully, you can change the root partition of the rescue mode environment to the root partition of your file system by executing the following command:
>
>     chroot /mnt/sysimage
>
>
> This is useful if you need to run commands such as **rpm** that require your root partition to be mounted as /. To exit the **chroot** environment, type **exit** to return to the prompt.
>
> If you selected **Skip**, you can still try to mount a partition or LVM2 logical volume manually inside rescue mode by creating a directory such as **/foo**, and typing the following command:
>
>     mount -t ext4 /dev/mapper/VolGroup00-LogVol02 /foo
>
>
> In the above command, /foo is a directory that you have created and **/dev/mapper/VolGroup00-LogVol02** is the LVM2 logical volume you want to mount. If the partition is of type **ext2** or **ext3** replace **ext4** with **ext2** or **ext3** respectively.
>
> If you do not know the names of all physical partitions, use the following command to list them:
>
>     fdisk -l
>
>
> If you do not know the names of all LVM2 physical volumes, volume groups, or logical volumes, use the **pvdisplay**, **vgdisplay** or **lvdisplay** commands, respectively.

### Reset Root Password Example with Single User Mode

We covered booting into Single User mode in [Chapter 2][2]. So let's boot into Single User mode. First reboot the machine and when it starts booting up you should see the Grub Menu:

![grub-menu][3]

Then leave the first one selected and type **e** to edit that entry and you should see the following:

![grub-menu-after-e][4]

Then scroll down to the **kernel** line and type **e** again to edit:

![kernel-line-menu][5]

then append the word **single** to the kernel parameter:

![single-appended][6]

then hit **enter** and then type **b** to boot the current configuration. After it's booted into Single User mode, you will see the following:

![single-user-mode-booted][7]

type the command **passwd** and set the password for the root user:

![password-reset][8]

After that, just type **exit** to reboot the system.

### Reset Root Password Example with Rescue Mode

Insert the install media into the server and boot from the CD/DVD. You should see the following if you booted from the CD successfully:

![dvd-booted][9]

Scroll down and select "Rescue Installed System", after it's done loading it will ask you to select your language:

![boot-cd-select-lang][10]

After selecting English, I saw the keyboard type selection screen:

![boot-cd-keyb-sel][11]

After selecting us, I saw the Rescue Method screen:

![boot-cd-res-method][12]

After selecting "Local CD/DVD", it asked me if I wanted to start networking:

![boot-cd-select-net][13]

I was just resetting the password, so I didn't need networking. After selecting **No**, I saw the the screen which talked about attempting to mount the Linux installation:

![boot-cd-attempt-moount][14]

I selected "Continue" and after successfully mounting the Linux Installation, I saw the following:

![boot-cd-success-mount-linux][15]

Upon clicking **OK** I got another confirmation that it has been mounted:

![boot-cd-mounted-linux][16]

Upon clicking OK again, I saw the "First Aid Kit quickstart menu":

![first-aide-quickstart-menu][17]

I left **shell** selected and click **OK**, at which point it dropped into a shell:

![shell-dropped][18]

I made sure the correct LVM volumes was mounted, I then chrooted into the system, and lastly I reset the password:

![res-chroot-pass-reset][19]

I exited out of the **chroot**, then out of the *\*shell\*, and rebooted the system.

### Re-installing MBR with GRUB Example

There are a couple of ways of doing this (they were both covered in [Chapter 2][2]). You can boot into **rescue** mode as described above and run the **grub** console (from there you can re-install MBR) or you can just run the **grub-install** command. Here is how the long way looks like:

![grub-reinstall-p1][20]

![mbr-reinstall-p2][21]

You can run **quit** to exit the grub console, and then reboot the system.

Or here is the quick way (still from **rescue** mode):

![grub-install][22]

### Running a FileSystem Check Example

If for some reason you think the File System is corrupt then you can run a file system check on it. I try to do it from external media, so boot into **rescue** mode and don't auto detect the file system (since we don't want to mount it). When dropped to the shell activate the LVM volumes and then do the file system check with **fsck**:

![fsck-lvm][23]

To activate the LVM volumes, run the following:

1.  **lvm vgscan -v**
2.  **lvm vgvhange -ay**
3.  **lvm lvs --all**

### Restoring a valid FileSystem SuperBlock Example

If you have a corrupt superblock:

    /dev/sda2: Input/output error
    mount: /dev/sda2: can't read superblock


Then you can try to restore one from backups, first check the file system to see where the superblocks are located:

    [root@rhel1 ~]# dumpe2fs /dev/sda1 | grep superblock
    dumpe2fs 1.41.12 (17-May-2010)
      Primary superblock at 1, Group descriptors at 2-3
      Backup superblock at 8193, Group descriptors at 8194-8195
      Backup superblock at 24577, Group descriptors at 24578-24579
      Backup superblock at 40961, Group descriptors at 40962-40963
      Backup superblock at 57345, Group descriptors at 57346-57347
      Backup superblock at 73729, Group descriptors at 73730-73731
      Backup superblock at 204801, Group descriptors at 204802-204803
      Backup superblock at 221185, Group descriptors at 221186-221187
      Backup superblock at 401409, Group descriptors at 401410-401411


To restore a file system with a backup superblock, run the following:

    [root@rhel1 ~]# umount /dev/sda1
    [root@rhel1 ~]# fsck -b 8193 /dev/sda1
    fsck from util-linux-ng 2.17.2
    e2fsck 1.41.12 (17-May-2010)
    One or more block group descriptor checksums are invalid.  Fix<y>?


### Can't Reach a Specific Service on a Remote Machine

Let's say you couldn't SSH into a server. Here are the steps I would take to make sure everything is in order:

1.  Make sure the Service is running on the remote machine

        [root@rhel1 ~]# service sshd status
        openssh-daemon (pid  2188) is running...
        [root@rhel1 ~]# ps -eaf | grep ssh | grep -v grep
        root      2188     1  0 13:52 ?        00:00:00 /usr/sbin/sshd
        root      2425  2188  0 16:08 ?        00:00:00 sshd: root@pts/0


2.  Make sure the service is running on it's correct port. With SSH we use port 22:

        [root@rhel1 ~]# netstat -antp | grep ssh
        tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      2188/sshd
        [root@rhel1 ~]# lsof -i tcp:22
        COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
        sshd    2188 root    3u  IPv4  13965      0t0  TCP *:ssh (LISTEN)


3.  Confirm TCP Wrappers are not blocking any IPs

        [root@rhel1 ~]# grep -vE '^#|^$' /etc/hosts.deny
        [root@rhel1 ~]# grep -vE '^#|^$' /etc/hosts.allow
        vsftpd : 192.168.2.3 \
        : spawn /bin/echo `/bin/date` from %h>>/var/log/ftpd.log \
        : allow


    It looks like only the FTP service is getting blocked and not the sshd service.

4.  Make sure iptables are allow port 22 access:

        [root@rhel1 ~]# iptables -L -n -v | grep 22
            2   120 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22


5.  Check in the logs to see if other users are logging in:

        [root@rhel1 ~]# grep sshd /var/log/secure | grep -i 'accepted password' | tail -2
        May  3 16:14:13 rhel1 sshd[2480]: Accepted password for root from 192.168.1.107 port 40926 ssh2
        May  3 16:15:49 rhel1 sshd[2505]: Accepted password for user1 from 192.168.2.3 port 38294 ssh2


6.  Ensure **sshd** doesn't have *AllowGroups*/*AllowUsers* or *DenyGroups*/*DenyUsers* options set:

        [root@rhel1 ~]# grep -iE 'users|groups' /etc/ssh/sshd_config
        [root@rhel1 ~]#


7.  Check to make sure SELinux is not interfering with the connection:

        [root@rhel1 ~]# grep sshd /var/log/audit/audit.log | grep failed | tail -1
        type=USER_LOGIN msg=audit(1399155767.241:164): user pid=2628 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:sshd_t:s0-s0:c0.c1023 msg='op=login acct="user1" exe="/usr/sbin/sshd" hostname=? addr=192.168.2.3 terminal=ssh res=failed'


8.  From the client machine, make sure DNS resolves to the correct IP:

        [root@rhel2 ~]# host rhel1
        rhel1.local.com has address 192.168.2.2
        [root@rhel2 ~]# nslookup rhel1
        Server:     192.168.2.2
        Address:    192.168.2.2#53

        Name:   rhel1.local.com
        Address: 192.168.2.2


9.  Make sure you can ping the server from the client:

        [root@rhel2 ~]# ping -c 3 rhel1
        PING rhel1.local.com (192.168.2.2) 56(84) bytes of data.
        64 bytes from rhel1.local.com (192.168.2.2): icmp_seq=1 ttl=64 time=0.087 ms
        64 bytes from rhel1.local.com (192.168.2.2): icmp_seq=2 ttl=64 time=0.298 ms
        64 bytes from rhel1.local.com (192.168.2.2): icmp_seq=3 ttl=64 time=0.228 ms

        --- rhel1.local.com ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2000ms
        rtt min/avg/max/mdev = 0.087/0.204/0.298/0.088 ms


10. Make sure you can reach the destination port:

        [root@rhel2 ~]# telnet rhel1 22
        Trying 192.168.2.2...
        Connected to rhel1.local.com (192.168.2.2).
        Escape character is '^]'.
        SSH-2.0-OpenSSH_5.3
        ^]
        telnet> quit
        Connection closed.


11. Make sure there are no client side settings that could be messing up the connection:

        [root@rhel2 ~]# grep -vE '^#|^$' /etc/ssh/ssh_config
        Host *
            GSSAPIAuthentication yes
            ForwardX11Trusted yes
            SendEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
            SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
            SendEnv LC_IDENTIFICATION LC_ALL


12. If available check the user's home directory for ssh settings as well:

        [root@rhel2 ~]# ls ~user1/.ssh/
        id_rsa  id_rsa.pub  known_hosts


    Usually there is a **~/.ssh/config** file with per-user ssh client configuration.

13. Use verbose logging with the ssh client to see where the error lies:

        [root@rhel2 ~]# ssh -v user1@rhel1
        OpenSSH_4.3p2, OpenSSL 0.9.8e-fips-rhel5 01 Jul 2008
        debug1: Reading configuration data /etc/ssh/ssh_config
        debug1: Applying options for *
        debug1: Connecting to rhel1 [192.168.2.2] port 22.
        debug1: Connection established.
        debug1: permanently_set_uid: 0/0
        debug1: identity file /root/.ssh/identity type -1
        debug1: identity file /root/.ssh/id_rsa type -1
        debug1: identity file /root/.ssh/id_dsa type -1
        debug1: loaded 3 keys
        debug1: Remote protocol version 2.0, remote software version OpenSSH_5.3
        debug1: match: OpenSSH_5.3 pat OpenSSH*
        debug1: Enabling compatibility mode for protocol 2.0
        debug1: Local version string SSH-2.0-OpenSSH_4.3
        debug1: SSH2_MSG_KEXINIT sent
        debug1: SSH2_MSG_KEXINIT received
        debug1: kex: server->client aes128-cbc hmac-md5 none
        debug1: kex: client->server aes128-cbc hmac-md5 none
        debug1: SSH2_MSG_KEX_DH_GEX_REQUEST(1024<1024<8192) sent
        debug1: expecting SSH2_MSG_KEX_DH_GEX_GROUP
        debug1: SSH2_MSG_KEX_DH_GEX_INIT sent
        debug1: expecting SSH2_MSG_KEX_DH_GEX_REPLY
        debug1: Host 'rhel1' is known and matches the RSA host key.
        debug1: Found key in /root/.ssh/known_hosts:1
        debug1: ssh_rsa_verify: signature correct
        debug1: SSH2_MSG_NEWKEYS sent
        debug1: expecting SSH2_MSG_NEWKEYS
        debug1: SSH2_MSG_NEWKEYS received
        debug1: SSH2_MSG_SERVICE_REQUEST sent
        debug1: SSH2_MSG_SERVICE_ACCEPT received
        debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
        debug1: Next authentication method: gssapi-with-mic
        debug1: Unspecified GSS failure.  Minor code may provide more information No credentials cache found

        debug1: Unspecified GSS failure.  Minor code may provide more information No credentials cache found

        debug1: Unspecified GSS failure.  Minor code may provide more information No credentials cache found
        debug1: Next authentication method: publickey
        debug1: Trying private key: /root/.ssh/identity
        debug1: Trying private key: /root/.ssh/id_rsa
        debug1: Trying private key: /root/.ssh/id_dsa
        debug1: Next authentication method: password
        user1@rhel1's password:
        debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
        Permission denied, please try again.


### Service doesn't start with "Cannot Bind to Address" Warning Message

This usually means that either the port is already used by another process, or the IP it's trying to bind to is not available on the machine. To track down the issue try the following:

1.  Confirm the IP and Port the service is trying to bind to:

        [root@rhel1 ~]# grep ^inet_interface /etc/postfix/main.cf
        inet_interfaces = 192.168.2.2
        [root@rhel1 ~]# grep ^smtp /etc/postfix/master.cf
        smtp      inet  n       -       n       -       -       smtpd
        smtp      unix  -       -       n       -       -       smtp


    We can see that it will be using the **192\.168.2.2** IP address and the port used for **smtp**. From the **/etc/services** file:

        [root@rhel1 ~]# grep ^smtp /etc/services
        smtp            25/tcp          mail
        smtp            25/udp          mail


    So we are binding to port **25**.

2.  Check the IP of the machine and make sure it matches:

        [root@rhel1 ~]# ip -4 a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
            inet 127.0.0.1/8 scope host lo
        3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
            inet 192.168.2.2/24 brd 192.168.2.255 scope global eth1


3.  Make sure nothing is listening on port 25:

        [root@rhel1 ~]# fuser -uv 25/tcp
                             USER        PID ACCESS COMMAND
        25/tcp:              root       2272 F.... (root)master
        [root@rhel1 ~]# lsof -i tcp:25
        COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
        master  2272 root   12u  IPv4  14166      0t0  TCP rhel1.local.com:smtp (LISTEN)
        [root@rhel1 ~]# netstat -antp | grep 25
        tcp        0      0 192.168.2.2:25              0.0.0.0:*                   LISTEN      2272/master


    We can see 3 different ways of checking if something is listening on port **25**. In the case above, it looks like **postfix** is using port **25**.

### Receiving a Destination Host Prohibited

Let's say you can't ping a host:

    [root@rhel2 ~]# ping google.com
    PING google.com (74.125.239.137) 56(84) bytes of data.
    From rhel1.dnsd.me (192.168.2.2) icmp_seq=1 Destination Host Prohibited
    From rhel1.dnsd.me (192.168.2.2) icmp_seq=2 Destination Host Prohibited
    From rhel1.dnsd.me (192.168.2.2) icmp_seq=3 Destination Host Prohibited

    --- google.com ping statistics ---
    3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2001ms


Try the following to make sure your networking is copacetic:

1.  Make sure the physical media is okay:

        [root@rhel2 ~]# mii-tool -v
        eth0: no link
          product info: vendor 00:50:43, model 2 rev 3
          basic mode:   autonegotiation enabled
          basic status: no link
          capabilities: 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD
          advertising:  100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD
        eth1: negotiated 100baseTx-FD, link ok
          product info: vendor 00:50:43, model 2 rev 3
          basic mode:   autonegotiation enabled
          basic status: autonegotiation complete, link ok
          capabilities: 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD
          advertising:  100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD
          link partner: 100baseTx-FD 100baseTx-HD 10baseT-FD 10baseT-HD


    We can also use **ethtool** for this:

        [root@rhel2 ~]# ethtool eth0
        Settings for eth0:
            Supported ports: [ TP ]
            Supported link modes:   10baseT/Half 10baseT/Full
                                    100baseT/Half 100baseT/Full
                                    1000baseT/Full
            Supports auto-negotiation: Yes
            Advertised link modes:  10baseT/Half 10baseT/Full
                                    100baseT/Half 100baseT/Full
                                    1000baseT/Full
            Advertised auto-negotiation: Yes
            Speed: Unknown!
            Duplex: Unknown! (255)
            Port: Twisted Pair
            PHYAD: 0
            Transceiver: internal
            Auto-negotiation: on
            Supports Wake-on: d
            Wake-on: d
            Current message level: 0x00000007 (7)
            Link detected: no
        [root@rhel2 ~]# ethtool eth1
        Settings for eth1:
            Supported ports: [ TP ]
            Supported link modes:   10baseT/Half 10baseT/Full
                                    100baseT/Half 100baseT/Full
                                    1000baseT/Full
            Supports auto-negotiation: Yes
            Advertised link modes:  10baseT/Half 10baseT/Full
                                    100baseT/Half 100baseT/Full
                                    1000baseT/Full
            Advertised auto-negotiation: Yes
            Speed: 1000Mb/s
            Duplex: Full
            Port: Twisted Pair
            PHYAD: 0
            Transceiver: internal
            Auto-negotiation: on
            Supports Wake-on: d
            Wake-on: d
            Current message level: 0x00000007 (7)
            Link detected: yes


    We can see that **eth0** is **down** and **eth1** is **up**.

2.  Make sure you routing table is okay and you can reach your default Gateway:

        [root@rhel2 ~]# netstat -rn
        Kernel IP routing table
        Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
        192.168.2.0     0.0.0.0         255.255.255.0   U         0 0          0 eth1
        169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth1
        0.0.0.0         192.168.2.2     0.0.0.0         UG        0 0          0 eth1
        [root@rhel2 ~]# ip route ls
        192.168.2.0/24 dev eth1  proto kernel  scope link  src 192.168.2.3
        169.254.0.0/16 dev eth1  scope link
        default via 192.168.2.2 dev eth1
        [root@rhel2 ~]# route -n
        Kernel IP routing table
        Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
        192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 eth1
        169.254.0.0     0.0.0.0         255.255.0.0     U     0      0        0 eth1
        0.0.0.0         192.168.2.2     0.0.0.0         UG    0      0        0 eth1


    We can see that there are no manual static routes added and the default gateway is **192\.168.2.2**. Let's make sure we can reach the default gateway:

        [root@rhel2 ~]# ping -c 2 192.168.2.2
        PING 192.168.2.2 (192.168.2.2) 56(84) bytes of data.
        64 bytes from 192.168.2.2: icmp_seq=1 ttl=64 time=0.186 ms
        64 bytes from 192.168.2.2: icmp_seq=2 ttl=64 time=0.334 ms

        --- 192.168.2.2 ping statistics ---
        2 packets transmitted, 2 received, 0% packet loss, time 999ms
        rtt min/avg/max/mdev = 0.186/0.260/0.334/0.074 ms


    If we had static routes, for example let's say we had a route that said we need to use **eth0** to reach a certain IP:

        [root@rhel2 ~]# ip route ls
        74.125.239.14 dev eth0  scope link
        192.168.2.0/24 dev eth1  proto kernel  scope link  src 192.168.2.3
        169.254.0.0/16 dev eth1  scope link
        172.1.0.0/16 dev eth0  proto kernel  scope link  src 172.1.2.12
        default via 192.168.2.2 dev eth1


    The top line is setting a static route to go out of **eth0** if reaching **74\.125.239.14**. You can also use **ip route get** to find out which interface will be used to reach a certain IP:

        [root@rhel2 ~]# ip route get 74.125.239.14
        74.125.239.14 dev eth0  src 172.1.2.12
            cache  expires 21334364sec mtu 1500 advmss 1460 hoplimit 64


    We can see that to reach IP **74\.125.239.14** we will use **eth0** as the source interface. My ping was of course failing:

        [root@rhel2 ~]# ping 74.125.239.14 -c 3
        PING 74.125.239.14 (74.125.239.14) 56(84) bytes of data.
        From 172.1.2.12 icmp_seq=1 Destination Host Unreachable
        From 172.1.2.12 icmp_seq=2 Destination Host Unreachable
        From 172.1.2.12 icmp_seq=3 Destination Host Unreachable

        --- 74.125.239.14 ping statistics ---
        3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2001ms, pipe 3


3.  Make sure you don't have any error on the NIC:

        [root@rhel2 ~]# ifconfig eth1
        eth1      Link encap:Ethernet  HWaddr 00:0C:29:4F:A1:EF
                  inet addr:192.168.2.3  Bcast:192.168.2.255  Mask:255.255.255.0
                  inet6 addr: fe80::20c:29ff:fe4f:a1ef/64 Scope:Link
                  UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
                  RX packets:34233 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:46943 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:3974689 (3.7 MiB)  TX bytes:6006739 (5.7 MiB)

        [root@rhel2 ~]# ip -s link show eth1
        3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
            link/ether 00:0c:29:4f:a1:ef brd ff:ff:ff:ff:ff:ff
            RX: bytes  packets  errors  dropped overrun mcast
            3976135    34252    0       0       0       0
            TX: bytes  packets  errors  dropped carrier collsns
            6008929    46958    0       0       0       0


    From above we can see there are no **drops** or **errors**, **ethtool** can show more statistics:

        [root@rhel2 ~]# ethtool -S eth1
        NIC statistics:
             rx_packets: 35469
             tx_packets: 47999
             rx_bytes: 4223053
             tx_bytes: 6297615
             rx_broadcast: 0
             tx_broadcast: 0
             rx_multicast: 0
             tx_multicast: 0
             rx_errors: 0
             tx_errors: 0
             tx_dropped: 0
             multicast: 0
             collisions: 0
             rx_length_errors: 0
             rx_over_errors: 0
             rx_crc_errors: 0
             rx_frame_errors: 0
             rx_no_buffer_count: 0
             rx_missed_errors: 0
             tx_aborted_errors: 0
             tx_carrier_errors: 0
             tx_fifo_errors: 0
             tx_heartbeat_errors: 0
             tx_window_errors: 0
             tx_abort_late_coll: 0
             tx_deferred_ok: 0
             tx_single_coll_ok: 0
             tx_multi_coll_ok: 0
             tx_timeout_count: 0
             tx_restart_queue: 0
             rx_long_length_errors: 0
             rx_short_length_errors: 0
             rx_align_errors: 0
             tx_tcp_seg_good: 3
             tx_tcp_seg_failed: 0
             rx_flow_control_xon: 0
             rx_flow_control_xoff: 0
             tx_flow_control_xon: 0
             tx_flow_control_xoff: 0
             rx_long_byte_count: 4223053
             rx_csum_offload_good: 26620
             rx_csum_offload_errors: 0
             rx_header_split: 0
             alloc_rx_buff_failed: 0
             tx_smbus: 0
             rx_smbus: 0
             dropped_smbus: 0


    We can also check TCP and UDP statistics with **netstat**:

        [root@rhel2 ~]# netstat -st
        IcmpMsg:
            InType0: 439
            InType3: 65
            OutType3: 52
            OutType8: 1986
        Tcp:
            396 active connections openings
            54 passive connection openings
            324 failed connection attempts
            3 connection resets received
            1 connections established
            18824 segments received
            13868 segments send out
            9 segments retransmited
            0 bad segments received.
            321 resets sent
        TcpExt:
            53 TCP sockets finished time wait in fast timer
            116 delayed acks sent
            118 packets directly queued to recvmsg prequeue.
            5049 packets directly received from prequeue
            770 packets header predicted
            24 packets header predicted and directly queued to user
            616 acknowledgments not containing data received
            10674 predicted acknowledgments
            1 congestion windows recovered after partial ack
            0 TCP data loss events
            3 other TCP timeouts
            1 DSACKs received
            2 connections reset due to early user close
        IpExt:
            InMcastPkts: 40
            OutMcastPkts: 48


    Usually the best way to use the above results is to run it once, then try your connection and then run it again to see if your resets, timeouts, or loss events are increasing.

4.  Make sure you external routing is okay

    Let's make sure you can reach the server traversing all the routers:

         [root@rhel2 ~]# traceroute -n google.com
         traceroute to google.com (74.125.224.132), 30 hops max, 40 byte packets
         1  192.168.2.2  0.201 ms  0.142 ms  0.110 ms
         2  10.0.0.1  0.556 ms  0.650 ms  0.667 ms
         3  67.172.134.1  26.219 ms  26.329 ms  29.218 ms
         4  68.86.105.57  12.217 ms  19.078 ms  19.189 ms
         5  68.86.103.25  21.125 ms  21.099 ms  21.007 ms
         6  68.85.89.250  21.283 ms 68.86.179.154  20.592 ms 68.85.89.250  21.097 ms
         7  68.86.92.25  20.852 ms 68.86.90.149  22.510 ms 68.86.92.25  20.845 ms
         8  68.86.84.126  20.976 ms  19.288 ms  13.930 ms
         9  23.30.206.106  14.053 ms  17.440 ms  17.130 ms
        10  72.14.234.59  17.112 ms 72.14.234.57  16.811 ms  16.845 ms
        11  216.239.46.146  17.320 ms 216.239.46.148  21.086 ms  22.138 ms
        12  216.239.46.153  51.552 ms  49.946 ms  48.613 ms
        13  64.233.175.151  47.352 ms  43.530 ms 64.233.174.189  50.222 ms
        14  209.85.250.251  45.630 ms  45.758 ms  45.889 ms
        15  74.125.224.132  45.691 ms  45.525 ms  45.193 ms


    If along the way anything is timing out, then there might an external routing issue. Here is me getting blocked locally:

         [root@rhel2 ~]# traceroute -n google.com
         traceroute to google.com (74.125.239.7), 30 hops max, 40 byte packets
         1  192.168.2.2  0.141 ms  0.138 ms  0.149 ms
         2  192.168.2.2  0.096 ms !X  0.150 ms !X  0.145 ms !X


5.  Confirm DNS is working

        [root@rhel2 ~]# nslookup google.com | head -6
        Server:     192.168.2.2
        Address:    192.168.2.2#53

        Non-authoritative answer:
        Name:   google.com
        Address: 74.125.224.129


6.  Lastly ensure you can see your destination IP:

        [root@rhel2 ~]# ping -n -c 3 google.com
        PING google.com (74.125.224.102) 56(84) bytes of data.
        64 bytes from 74.125.224.102: icmp_seq=1 ttl=52 time=42.3 ms
        64 bytes from 74.125.224.102: icmp_seq=2 ttl=52 time=42.5 ms
        64 bytes from 74.125.224.102: icmp_seq=3 ttl=52 time=45.1 ms

        --- google.com ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2003ms
        rtt min/avg/max/mdev = 42.353/43.353/45.109/1.268 ms


There are many more things to try if you are trying a specific application. You can try to get a packet capture with **tcpdump** (covered in [Chapter 5][24]) and check to see what is happening at layer 7 of the OSI stack.

 [1]: https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf
 [2]: /2013/01/rhcsa-and-rhce-chapter-2-system-initialization/
 [3]: https://github.com/elatov/uploads/raw/master/2014/05/grub-menu.png
 [4]: https://github.com/elatov/uploads/raw/master/2014/05/grub-menu-after-e.png
 [5]: https://github.com/elatov/uploads/raw/master/2014/05/kernel-line-menu.png
 [6]: https://github.com/elatov/uploads/raw/master/2014/05/single-appended.png
 [7]: https://github.com/elatov/uploads/raw/master/2014/05/single-user-mode-booted.png
 [8]: https://github.com/elatov/uploads/raw/master/2014/05/password-reset.png
 [9]: https://github.com/elatov/uploads/raw/master/2014/05/dvd-booted.png
 [10]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-select-lang.png
 [11]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-keyb-sel.png
 [12]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-res-metho.png
 [13]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-select-net.png
 [14]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-attempt-moount.png
 [15]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-success-mount-linux.png
 [16]: https://github.com/elatov/uploads/raw/master/2014/05/boot-cd-mounted-linux.png
 [17]: https://github.com/elatov/uploads/raw/master/2014/05/first-aide-quickstart-menu.png
 [18]: https://github.com/elatov/uploads/raw/master/2014/05/shell-dropped.png
 [19]: https://github.com/elatov/uploads/raw/master/2014/05/res-chroot-pass-reset.png
 [20]: https://github.com/elatov/uploads/raw/master/2014/05/grub-reinstall-p1.png
 [21]: https://github.com/elatov/uploads/raw/master/2014/05/mbr-reinstall-p2.png
 [22]: https://github.com/elatov/uploads/raw/master/2014/05/grub-install.png
 [23]: https://github.com/elatov/uploads/raw/master/2014/05/fsck-lvm.png
 [24]: /2013/01/rhcsa-and-rhce-chapter-5-networking/
