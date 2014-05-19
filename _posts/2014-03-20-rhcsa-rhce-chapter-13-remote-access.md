---
title: RHCSA and RHCE Chapter 13 – Remote Access
author: Karim Elatov
layout: post
permalink: /2014/03/rhcsa-rhce-chapter-13-remote-access/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2469523699
categories:
  - Certifications
  - RHCSA and RHCE
tags:
  - OpenSSH
  - rhcsa_and_rhce
  - VNC
---
## OpenSSH

There are a couple of ways to manage RHEL machines. The primary one is over SSH. SSH is described in the [Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf). From the Deployment Guide:

> **SSH** (Secure Shell) is a protocol which facilitates secure communications between two systems using a client/server architecture and allows users to log into server host systems remotely. Unlike other remote communication protocols, such as FTP or Telnet, SSH encrypts the login session, rendering the connection difficult for intruders to collect unencrypted passwords.
>
> The **ssh** program is designed to replace older, less secure terminal applications used to log into remote hosts, such as **telnet** or **rsh**. A related program called **scp** replaces older programs designed to copy files between hosts, such as **rcp**. Because these older applications do not encrypt passwords transmitted between the client and the server, avoid them whenever possible. Using secure methods to log into remote systems decreases the risks for both the client system and the remote host.
>
> Red Hat Enterprise Linux includes the general OpenSSH package (**openssh**) as well as the OpenSSH server (**openssh-server**) and client (**openssh-clients**) packages. Note, the OpenSSH packages require the OpenSSL package (**openssl**) which installs several important cryptographic libraries, enabling OpenSSH to provide encrypted communications.

From the above guide, here are some reasons to use SSH over other protocols:

> Potential intruders have a variety of tools at their disposal enabling them to disrupt, intercept, and re-route network traffic in an effort to gain access to a system. In general terms, these threats can be categorized as follows:
>
> **Interception of communication between two systems**
>
> The attacker can be somewhere on the network between the communicating parties, copying any information passed between them. He may intercept and keep the information, or alter the information and send it on to the intended recipient.
>
> This attack is usually performed using a packet sniffer, a rather common network utility that captures each packet flowing through the network, and analyzes its content.
>
> **Impersonation of a particular host**
>
> Attacker's system is configured to pose as the intended recipient of a transmission. If this strategy works, the user's system remains unaware that it is communicating with the wrong host.
>
> This attack can be performed using a technique known as DNS poisoning, or via so-called IP spoofing. In the first case, the intruder uses a cracked DNS server to point client systems to a maliciously duplicated host. In the second case, the intruder sends falsified network packets that appear to be from a trusted host.
>
> Both techniques intercept potentially sensitive information and, if the interception is made for hostile reasons, the results can be disastrous. If SSH is used for remote shell login and file copying, these security threats can be greatly diminished. This is because the SSH client and server use digital signatures to verify their identity. Additionally, all communication between the client and server systems is encrypted. Attempts to spoof the identity of either side of a communication does not work, since each packet is encrypted using a key known only by the local and remote systems.

### SSH Encryption

Here more information regarding the encryption mechanisms of SSH:

> The following series of events help protect the integrity of SSH communication between two hosts.
>
> 1.  A cryptographic handshake is made so that the client can verify that it is communicating with the correct server.
> 2.  The transport layer of the connection between the client and remote host is encrypted using a symmetric cipher.
> 3.  The client authenticates itself to the server.
> 4.  The remote client interacts with the remote host over the encrypted connection.
>
> The primary role of the transport layer is to facilitate safe and secure communication between the two hosts at the time of authentication and during subsequent communication. The transport layer accomplishes this by handling the encryption and decryption of data, and by providing integrity protection of data packets as they are sent and received. The transport layer also provides compression, speeding the transfer of information.
>
> Once an SSH client contacts a server, key information is exchanged so that the two systems can correctly construct the transport layer. The following steps occur during this exchange: Keys are exchanged
>
> *   The public key encryption algorithm is determined
> *   The symmetric encryption algorithm is determined
> *   The message authentication algorithm is determined
> *   The hash algorithm is determined
>
> During the key exchange, the server identifies itself to the client with a unique host key. If the client has never communicated with this particular server before, the server's host key is unknown to the client and it does not connect. OpenSSH gets around this problem by accepting the server's host key. This is done after the user is notified and has both accepted and verified the new host key. In subsequent connections, the server's host key is checked against the saved version on the client, providing confidence that the client is indeed communicating with the intended server. If, in the future, the host key no longer matches, the user must remove the client's saved version before a connection can occur.

### OpenSSH Configuration Files

From the same guide:

> There are two different sets of configuration files: those for client programs (that is, **ssh**, **scp**, and **sftp**), and those for the server (the **sshd** daemon).
>
> System-wide SSH configuration information is stored in the **/etc/ssh/** directory. User-specific SSH configuration information is stored in **~/.ssh/** within the user's home directory.
>
> ![etc ssh contents RHCSA and RHCE Chapter 13 – Remote Access](http://virtuallyhyper.com/wp-content/uploads/2014/03/etc_ssh-contents.png)

And here are the user specific files:

> ![user ssh content RHCSA and RHCE Chapter 13 – Remote Access](http://virtuallyhyper.com/wp-content/uploads/2014/03/user_ssh-content.png)

### OpenSSH Service

From the guide:

> In order to run an OpenSSH server, you must have the **openssh-server** and **openssh** packages installed .
>
> To start the sshd daemon, type the following at a shell prompt:
>
>     ~]# service sshd start
>
>
> To stop the running sshd daemon, use the following command:
>
>     ~]# service sshd stop
>
>
> If you want the daemon to start automatically at the boot time, type:
>
>     ~]# chkconfig sshd on
>
>
> This will enable the service for all runlevels.
>
> Note that if you reinstall the system, a new set of identification keys will be created. As a result, clients who had connected to the system with any of the OpenSSH tools before the reinstall will see the following message:
>
>     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
>     @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
>     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
>     IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
>     Someone could be eavesdropping on you right now (man-in-the-middle attack)!
>     It is also possible that the RSA host key has just been changed.
>
>
> To prevent this, you can backup the relevant files from the **/etc/ssh/** directory (as described in the table above), and restore them whenever you reinstall the system.

### Disabling Other Remote Unsecure Services

From the Deployment Guide:

> For SSH to be truly effective, using insecure connection protocols should be prohibited. Otherwise, a user's password may be protected using SSH for one session, only to be captured later while logging in using Telnet. Some services to disable include **telnet**, **rsh**, **rlogin**, and **vsftpd**.
>
> To disable these services, type the following commands at a shell prompt:
>
>     ~]# chkconfig telnet off
>     ~]# chkconfig rsh off
>     ~]# chkconfig rlogin off
>     ~]# chkconfig vsftpd off
>

### Key-Based Authentication

From the same guide:

> To improve the system security even further, you can enforce the key-based authentication by disabling the standard password authentication. To do so, open the **/etc/ssh/sshd_config** configuration file in a text editor such as **vi** or **nano**, and change the **PasswordAuthentication** option as follows:
>
>     PasswordAuthentication no
>
>
> To be able to use **ssh**, **scp**, or **sftp** to connect to the server from a client machine, generate an authorization key pair by following the steps below. Note that keys must be generated for each user separately.

#### Generating Key Pairs

From the guide:

> To generate an RSA key pair for version 2 of the SSH protocol, follow these steps:
>
> 1.  Generate an RSA key pair by typing the following at a shell prompt:
>
>         ~]$ ssh-keygen -t rsa
>         Generating public/private rsa key pair.
>         Enter file in which to save the key (/home/john/.ssh/id_rsa):
>
>
> 2.  Press **Enter** to confirm the default location (that is, **~/.ssh/id_rsa**) for the newly created key.
>
> 3.  Enter a passphrase, and confirm it by entering it again when prompted to do so. For security reasons, avoid using the same password as you use to log in to your account.
>
>     After this, you will be presented with a message similar to this:
>
>         Your identification has been saved in /home/john/.ssh/id_rsa.
>         Your public key has been saved in /home/john/.ssh/id_rsa.pub.
>         The key fingerprint is:
>         e7:97:c7:e2:0e:f9:0e:fc:c4:d7:cb:e5:31:11:92:14 john@penguin.example.com
>         The key's randomart image is:
>         +--[ RSA 2048]----+
>         |             E.  |
>         |            . .  |
>         |             o . |
>         |              . .|
>         |        S .    . |
>         |         + o o ..|
>         |          * * +oo|
>         |           O +..=|
>         |           o*  o.|
>         +-----------------+
>
>
> 4.  Change the permissions of the **~/.ssh/** directory:
>
>         ~]$ chmod 700 ~/.ssh
>
>
> 5.  Copy the content of **~/.ssh/id_rsa.pu**b into the **~/.ssh/authorized_keys** on the machine to which you want to connect, appending it to its end if the file already exists.
>
> 6.  Change the permissions of the ~/.ssh/authorized_keys file using the following command:
>
>         ~]$ chmod 600 ~/.ssh/authorized_keys
>

For other algorithms just specify the algorithm after the **-t** parameter but then follow the same steps:

*   To generate a DSA key pair for version 2 of the SSH protocol

        ~]$ ssh-keygen -t dsa


    *   Copy the content of **~/.ssh/id_dsa.pub** into the **~/.ssh/authorized_keys** on the machine

*   To generate an RSA key pair for version 1 of the SSH protocol

        ~]$ ssh-keygen -t rsa1


    *   Copy the content of **~/.ssh/identity.pub** into the **~/.ssh/authorized_keys** on the machine

Let's try this out. First let's SSH from our rhel5 machine to the rhel6 machine:

    [user1@rhel2 ~]$ ssh rhel1
    The authenticity of host 'rhel1 (192.168.2.2)' can't be established.
    RSA key fingerprint is 06:f0:56:28:af:8a:b7:6b:cb:27:7e:b2:94:fd:92:fd.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added 'rhel1,192.168.2.2' (RSA) to the list of known hosts.
    user1@rhel1's password:
    Last login: Sat Feb  9 02:50:19 2013 from 192.168.1.102
    [user1@rhel1 ~]$


Notice this was the first time we are connecting to the host, so we have to accept the authenticity of that host. After the initial connection is made, the following files are created on the rhel5 machine:

    [user1@rhel2 ~]$ ls -l .ssh
    total 4
    -rw-r--r-- 1 user1 user1 399 Mar  8 09:00 known_hosts


That file should contain the public key of the rhel6 machine since we connected to it. So let's check out that file:

    [user1@rhel2 ~]$ cat .ssh/known_hosts
    rhel1,192.168.2.2 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAnQpDaJo0Nb5Ka1enKdoYyYxSWo8f9ju+gNrScIYxAOqxk6sCGitYo2OwquTevtRixO/y/PBQFC6MX/dz6dMkhNBEl8z/HIk7HAVAqN67G3161hhXy4P/HUkCTpvy93mUb14dDsIPNogqxCg3iikgX1CFyTIC/L4zYxogZVD/D1DnJyM6ls4dFpErS4jy06WKwT6YoeuTUH94QG5Mp0IU/14f5nl3JcDpZ8EzhyA4IovVb5qo4KzNvvY2pVRiJCMJoBNuqpr04HghUvqgiXClHZon4yWLJE9PPRK1RgKKpDzqvW/L7l7Vn06EW2uY658P88vjDSR+49DdommALmnBPw==


That random string is the public part of RSA pair of the rhel6 host. We can confirm that by checking the contents of the public key on the rhel6 machine:

    [root@rhel1 ~]# cat /etc/ssh/ssh_host_rsa_key.pub
    ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAnQpDaJo0Nb5Ka1enKdoYyYxSWo8f9ju+gNrScIYxAOqxk6sCGitYo2OwquTevtRixO/y/PBQFC6MX/dz6dMkhNBEl8z/HIk7HAVAqN67G3161hhXy4P/HUkCTpvy93mUb14dDsIPNogqxCg3iikgX1CFyTIC/L4zYxogZVD/D1DnJyM6ls4dFpErS4jy06WKwT6YoeuTUH94QG5Mp0IU/14f5nl3JcDpZ8EzhyA4IovVb5qo4KzNvvY2pVRiJCMJoBNuqpr04HghUvqgiXClHZon4yWLJE9PPRK1RgKKpDzqvW/L7l7Vn06EW2uY658P88vjDSR+49DdommALmnBPw==


They do match. Now if I make a subsequent connection to the same host, it won't prompt me for the authenticity of the host (since I accepted it on the first connection):

    [user1@rhel2 ~]$ ssh rhel1
    user1@rhel1's password:
    Last login: Sat Mar  8 09:01:08 2014 from rhel2.local.com
    [user1@rhel1 ~]$


You will also notice that I had to type in the password for user1 each time. So let's generate an RSA key pair for the user and use that for our authentication. First let's create the key pair:

    [user1@rhel2 ~]$ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/user1/.ssh/id_rsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/user1/.ssh/id_rsa.
    Your public key has been saved in /home/user1/.ssh/id_rsa.pub.
    The key fingerprint is:
    88:60:ee:9e:72:66:aa:a5:f3:b7:cc:25:20:82:88:d4 user1@local.com


I accepted the defaults on the prompts and I actually didn't create a password for this key since this is just for this lab. After the above process is done, we will see the following files:

    [user1@rhel2 ~]$ ls -l .ssh/
    total 12
    -rw------- 1 user1 user1 1675 Mar  8 09:11 id_rsa
    -rw-r--r-- 1 user1 user1  401 Mar  8 09:11 id_rsa.pub
    -rw-r--r-- 1 user1 user1  399 Mar  8 09:00 known_hosts


The **.pub** file is the public part and the **id_rsa** file is the private key. Now let's copy the public key to our host:

    [user1@rhel2 ~]$ ssh-copy-id -i .ssh/id_rsa.pub rhel1
    15
    user1@rhel1's password:
    Now try logging into the machine, with "ssh 'rhel1'", and check in:

      .ssh/authorized_keys

    to make sure we haven't added extra keys that you weren't expecting.


Now if I try to ssh to the host:

    [user1@rhel2 ~]$ ssh rhel1
    Last login: Sat Mar  8 09:07:35 2014 from rhel2.local.com
    [user1@rhel1 ~]$


Notice I wasn't prompted for the password since it used the RSA key for authentication. Also on the rhel6 machine, we should now have the following file:

    [user1@rhel1 ~]$ ls -l .ssh
    total 4
    -rw-------. 1 user1 user1 401 Mar  8 09:16 authorized_keys


And the contents of that file:

    [user1@rhel1 ~]$ cat .ssh/authorized_keys
    ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAtjKyIMi7f7zwoM1tI+MITUI2lVMe/Dg+ssIBfl3+X1SCZ4hEn8+wIjPuL5gMrXw+x8aw7Cj9r+Xilxihx4sVVEzuriN6owSGAYcrwi5cCJ+VJvJI+1DwRxFCZb5Oniah3Zz8JIEPH/neipzcLFEK5ULCJkDIHOwQAPaDAygeXd26cWbsbF4Xpkr4ziK5e6rYOw3nQIQ6blVIQ4j5/bOJ6s/3no6P4rCZj7yILYTlXCyP0SrvQMeyCtxf0rv/mwFeCMdP3s21AwLnq2Qztmv3BeVy2HSaG8N6vGuK/UHMnOaDlS/EXiO3LA+y+dyXy15+vA/iYWe0gR3xDHHd+H/hdQ== user1@rhel2.local.com


Should match the public part of our RSA key pair on the rhel5 machine:

    [user1@rhel2 ~]$ cat .ssh/id_rsa.pub
    ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAtjKyIMi7f7zwoM1tI+MITUI2lVMe/Dg+ssIBfl3+X1SCZ4hEn8+wIjPuL5gMrXw+x8aw7Cj9r+Xilxihx4sVVEzuriN6owSGAYcrwi5cCJ+VJvJI+1DwRxFCZb5Oniah3Zz8JIEPH/neipzcLFEK5ULCJkDIHOwQAPaDAygeXd26cWbsbF4Xpkr4ziK5e6rYOw3nQIQ6blVIQ4j5/bOJ6s/3no6P4rCZj7yILYTlXCyP0SrvQMeyCtxf0rv/mwFeCMdP3s21AwLnq2Qztmv3BeVy2HSaG8N6vGuK/UHMnOaDlS/EXiO3LA+y+dyXy15+vA/iYWe0gR3xDHHd+H/hdQ== user1@rhel2.local.com


### X11 Forwarding

From the Deployment Guide:

> A secure command line interface is just the beginning of the many ways SSH can be used. Given the proper amount of bandwidth, X11 sessions can be directed over an SSH channel. Or, by using TCP/IP forwarding, previously insecure port connections between systems can be mapped to specific SSH channels.
>
> To open an X11 session over an SSH connection, use a command in the following form:
>
>     ssh -Y username@hostname
>
>
> For example, to log in to a remote machine named penguin.example.com with john as a username, type:
>
>     ~]$ ssh -Y john@penguin.example.com
>     john@penguin.example.com's password:
>
>
> When an X program is run from the secure shell prompt, the SSH client and server create a new secure channel, and the X program data is sent over that channel to the client machine transparently.
>
> X11 forwarding can be very useful. For example, X11 forwarding can be used to create a secure, interactive session of the Printer Configuration utility. To do this, connect to the server using ssh and type:
>
>     ~]$ system-config-printer &
>
>
> The Printer Configuration Tool will appear, allowing the remote user to safely configure printing on the remote system.

To try this out, I installed 3 packages on the rhel6 machine:

    [root@rhel1 ~]# yum install xorg-x11-xauth system-config-printer xorg-x11-fonts-Type1


Upon login, I saw the following:

    elatov@fed:~$ssh -X root@rhel1
    root@rhel1's password:
    Last login: Sat Mar  8 09:42:28 2014 from fed.local.com
    /usr/bin/xauth:  creating new authority file /root/.Xauthority
    [root@rhel1 ~]#


As you can see **xauth** is necessary to authenticate to the Xorg system. Here is the description from the RPM:

    [root@rhel1 ~]# rpm -q --queryformat '%{DESCRIPTION}' xorg-x11-xauth-1.0.2-7.1.el6.i686
    xauth is used to edit and display the authorization information
    used in connecting to an X server.


Then running the following:

    [root@rhel1 ~]# system-config-printer &


Produced a local window on my laptop from the remote host:

![ssh forward system config print RHCSA and RHCE Chapter 13 – Remote Access](http://virtuallyhyper.com/wp-content/uploads/2014/03/ssh-forward-system-config-print.png)

### SSH Port Forwarding

From the Deployment Guide:

> SSH can secure otherwise insecure TCP/IP protocols via port forwarding. When using this technique, the SSH server becomes an encrypted conduit to the SSH client.
>
> Port forwarding works by mapping a local port on the client to a remote port on the server. SSH can map any port from the server to any port on the client. Port numbers do not need to match for this technique to work.
>
> To create a TCP/IP port forwarding channel which listens for connections on the localhost, use a command in the following form:
>
>     ssh -L local-port:remote-hostname:remote-port username@hostname
>
>
> For example, to check email on a server called mail.example.com using POP3 through an encrypted connection, use the following command:
>
>     ~]$ ssh -L 1100:mail.example.com:110 mail.example.com
>
>
> Once the port forwarding channel is in place between the client machine and the mail server, direct a POP3 mail client to use port **1100** on the **localhost** to check for new email. Any requests sent to port **1100** on the client system will be directed securely to the **mail.example.com** server.
>
> If **mail.example.com** is not running an SSH server, but another machine on the same network is, SSH can still be used to secure part of the connection. However, a slightly different command is necessary:
>
>     ~]$ ssh -L 1100:mail.example.com:110 other.example.com
>
>
> In this example, POP3 requests from port **1100** on the client machine are forwarded through the SSH connection on port **22** to the SSH server, **other.example.com**. Then, **other.example.com** connects to port **110** on **mail.example.com** to check for new email. Note that when using this technique, only the connection between the client system and other.example.com SSH server is secure.
>
> Port forwarding can also be used to get information securely through network firewalls. If the firewall is configured to allow SSH traffic via its standard port (that is, port 22) but blocks access to other ports, a connection between two hosts using the blocked ports is still possible by redirecting their communication over an established SSH connection.

There are a lot of examples of this. We are going to cover VNC next, at the end I will use SSH Port Forwarding to Securely Connect over VNC.

## VNC

There is a good Red Hat Magazine Article that covers the process: [Taking your desktop virtual with VNC](http://www.redhat.com/magazine/006apr05/features/vnc/). The article is for an older version of RHEL but the process is very similar. First let's install the vnc server:

    [root@rhel1 ~]# yum install tigervnc-server.i686
    ...
    ...
    Installed:
      tigervnc-server.i686 0:1.0.90-0.15.20110314svn4359.el6

    Dependency Installed:
      libXdmcp.i686 0:1.0.3-1.el6               libxkbfile.i686 0:1.0.6-1.1.el6
      mesa-dri-drivers.i686 0:7.10-1.el6        xkeyboard-config.noarch 0:1.6-7.el6
      xorg-x11-fonts-misc.noarch 0:7.2-9.1.el6  xorg-x11-xauth.i686 1:1.0.2-7.1.el6
      xorg-x11-xkb-utils.i686 0:7.4-6.el6

    Complete!


Notice that installs the **xauth** package as well, along with some fonts. Now let's configure the vnc server for user1 to be on the second port. This is done by editing the **/etc/sysconfig/vncservers** file and adding the following lines:

    [root@rhel1 ~]# tail -2 /etc/sysconfig/vncservers
    VNCSERVERS="2:user1"
    VNCSERVERARGS[2]="-geometry 800x600 -nolisten tcp"


then create a vnc password for user1:

    [user1@rhel1 ~]$ vncpasswd
    Password:
    Verify:


Now we can start the service:

    [root@rhel1 ~]# service vncserver start
    Starting VNC server: 2:user1
    New 'rhel1.local.com:2 (user1)' desktop is rhel1.local.com:2

    Creating default startup script /home/user1/.vnc/xstartup
    Starting applications specified in /home/user1/.vnc/xstartup
    Log file is /home/user1/.vnc/rhel1.local.com:2.log


If you try to start the service prior to running **vncpassword**, it won't start (since the **~/.vnc** won't exist). At this point you should see the vnc service listening on port 5902:

    [root@rhel1 ~]# netstat -antp | grep 5902
    tcp        0      0 0.0.0.0:5902                0.0.0.0:*                   LISTEN      26525/Xvnc


Let's open up port 5902 to be accessible from our network:

    [root@rhel1 ~]# iptables -I INPUT 11 -m state --state NEW -m tcp -p tcp --dport 5902 -j ACCEPT


Save the rules to make them permanent:

    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:


Now using vncviewer we can connect to the host:

    elatov@fed:~$ yum install tigervnc


Then I connected to the rhel6 machine:

    elatov@fed:~$vncviewer rhel1:2


I did have to install **twm** just for testing and I saw the following:

![vncviewer direct RHCSA and RHCE Chapter 13 – Remote Access](http://virtuallyhyper.com/wp-content/uploads/2014/03/vncviewer-direct.png)

Since VNC is unsecure usually SSH forwarding is used to connect to a VNC server. First we can force to only accept VNC connections from localhost on the VNC Server. This is done by editing **/etc/sysconfig/vncservers** file and making the following adjusting:

    [root@rhel1 ~]# tail -2 /etc/sysconfig/vncservers
    VNCSERVERS="2:user1"
    VNCSERVERARGS[2]="-geometry 800x600 -nolisten tcp -localhost"


Then restarting the VNC server:

    [root@rhel1 ~]# service vncserver restart
    Shutting down VNC server: 2:user1
    Starting VNC server: 2:user1
    New 'rhel1.local.com:2 (user1)' desktop is rhel1.local.com:2

    Starting applications specified in /home/user1/.vnc/xstartup
    Log file is /home/user1/.vnc/rhel1.local.com:2.log


Now if I try to connect directly to the VNC server, I get the following:

    elatov@fed:~$vncviewer rhel1:2

    TigerVNC Viewer 64-bit v1.3.0 (20140121)
    Built on Jan 21 2014 at 09:40:20
    Copyright (C) 1999-2011 TigerVNC Team and many others (see README.txt)
    See http://www.tigervnc.org for information on TigerVNC.

    Sat Mar  8 11:49:27 2014
     CConn:       unable connect to socket: Connection refused (111)


#### VNC with SSH Forwarding

So let's create an SSH Tunnel to our VNC server and map the remote port 5902 to 5902 on our local machine:

    elatov@fed:~$ssh -Nf -L 5902:localhost:5902 user1@rhel1
    user1@rhel1's password:


You should now see the tunnel on the local machine:

    elatov@fed:~$netstat -ant | grep 5902
    tcp        0      0 127.0.0.1:5902          0.0.0.0:*               LISTEN


Then connecting to **localhost** port **5902** connected to the machine:

    elatov@fed:~$vncviewer 127.0.0.1:2


**vncviewer** by default has a option which can create the SSH tunnel on the fly. This is done with the **-via** flag. Here is an example:

    elatov@fed:~$vncviewer -via user1@rhel1 127.0.0.1:2

    TigerVNC Viewer 64-bit v1.3.0 (20140121)
    Built on Jan 21 2014 at 09:40:20
    Copyright (C) 1999-2011 TigerVNC Team and many others (see README.txt)
    See http://www.tigervnc.org for information on TigerVNC.

    Sat Mar  8 11:55:09 2014
     main:        localhost::33422
    user1@rhel1's password:

    Sat Mar  8 11:55:13 2014
     CConn:       connected to host localhost port 33422
     CConnection: Server supports RFB protocol version 3.8
     CConnection: Using RFB protocol version 3.8


Notice it first asks for the **user1** password to establish the SSH tunnel and then establishes the VNC connection.

#### Manually Start VNC Server

If the vnc server package is installed but you don't have sudo to start the vncserver service, then you can start the VNC server manually like this:

    [user1@rhel1 ~]$ vncserver :1

    New 'rhel1.local.com:1 (user1)' desktop is rhe1.local.com:1

    Starting applications specified in /home/user1/.vnc/xstartup
    Log file is /home/user1/.vnc/rhel1.local.com:1.log


You can then confirm the process is running

    [user1@rhel1 ~]$ ps -eaf | grep vnc
    user1     2634     1 22 12:05 pts/0    00:00:02 /usr/bin/Xvnc :1 -desktop rhel1.local.com:1 (user1) -auth /home/user1/.Xauthority -geometry 1024x768 -rfbwait 30000 -rfbauth /home/user1/.vnc/passwd -rfbport 5901 -fp catalogue:/etc/X11/fontpath.d -pn


Since I started this instance on **5901**, we can now connect the new VNC server from a client, by running the following:

    elatov@fed:~$vncviewer -via user1@10.0.0.4 127.0.0.1:1


No firewall rules are necessary to be open since we are using SSH Port-Forwarding. To stop the VNC server you can run the following:

    [user1@rhel1 ~]$ vncserver -kill :1
    Killing Xvnc process ID 2634


Lastly to confirm it's not running:

    [user1@rhel1 ~]$ ps -eaf | grep vnc
    user1     2704  2610  0 12:10 pts/0    00:00:00 grep vnc


