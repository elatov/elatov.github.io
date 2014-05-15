---
title: RHCSA and RHCE Chapter 15 – NFS
author: Karim Elatov
layout: post
permalink: /2014/04/rhcsa-rhce-chapter-15-nfs/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2583778687
categories:
  - Certifications
  - RHCSA and RHCE
  - Storage
tags:
  - nfs
  - rhcsa_and_rhce
---
## NFS

From the <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf']);">Storage Administration Guide</a>:

> A Network File System (**NFS**) allows remote hosts to mount file systems over a network and interact with those file systems as though they are mounted locally. This enables system administrators to consolidate resources onto centralized servers on the network.
> 
> Currently, there are three versions of NFS. NFS version 2 (NFSv2) is older and widely supported. NFS version 3 (NFSv3) supports safe asynchronous writes and is more robust at error handling than NFSv2; it also supports 64-bit file sizes and offsets, allowing clients to access more than 2Gb of file data.
> 
> NFS version 4 (NFSv4) works through firewalls and on the Internet, no longer requires an **rpcbind** service, supports ACLs, and utilizes stateful operations. Red Hat Enterprise Linux 6 supports NFSv2, NFSv3, and NFSv4 clients. When mounting a file system via NFS, Red Hat Enterprise Linux uses NFSv4 by default, if the server supports it.
> 
> All versions of NFS can use Transmission Control Protocol (TCP) running over an IP network, with NFSv4 requiring it. NFSv2 and NFSv3 can use the User Datagram Protocol (UDP) running over an IP network to provide a stateless network connection between the client and server.
> 
> When using NFSv2 or NFSv3 with UDP, the stateless UDP connection (under normal conditions) has less protocol overhead than TCP. This can translate into better performance on very clean, non-congested networks. However, because UDP is stateless, if the server goes down unexpectedly, UDP clients continue to saturate the network with requests for the server. In addition, when a frame is lost with UDP, the entire RPC request must be retransmitted; with TCP, only the lost frame needs to be resent. For these reasons, TCP is the preferred protocol when connecting to an NFS server.
> 
> The mounting and locking protocols have been incorporated into the NFSv4 protocol. The server also listens on the well-known TCP port 2049. As such, NFSv4 does not need to interact with **rpcbind** , **lockd**, and **rpc.statd** daemons. The **rpc.mountd** daemon is still required on the NFS server to set up the exports, but is not involved in any over-the-wire operations.

### NFS Related Services

From the same guide:

> Red Hat Enterprise Linux uses a combination of kernel-level support and daemon processes to provide NFS file sharing. All NFS versions rely on Remote Procedure Calls (RPC) between clients and servers. RPC services under Red Hat Enterprise Linux 6 are controlled by the **rpcbind** service. To share or mount NFS file systems, the following services work together depending on which version of NFS is implemented:
> 
> *   **nfs** - `service nfs start` starts the NFS server and the appropriate RPC processes to service requests for shared NFS file systems.
> *   **nfslock** - `service nfslock start` activates a mandatory service that starts the appropriate RPC processes allowing NFS clients to lock files on the server.
> *   **rpcbind** - **rpcbind** accepts port reservations from local RPC services. These ports are then made available (or advertised) so the corresponding remote RPC services can access them. **rpcbind** responds to requests for RPC services and sets up connections to the requested RPC service. This is not used with NFSv4.
> 
> The following RPC processes facilitate NFS services:
> 
> *   **rpc.mountd**- This process is used by an NFS server to process **MOUNT** requests from NFSv2 and NFSv3 clients. It checks that the requested NFS share is currently exported by the NFS server, and that the client is allowed to access it. If the mount request is allowed, the **rpc.mountd** server replies with a **Success** status and provides the **File-Handle** for this NFS share back to the NFS client.
> *   **rpc.nfsd** - **rpc.nfsd** allows explicit NFS versions and protocols the server advertises to be defined. It works with the Linux kernel to meet the dynamic demands of NFS clients, such as providing server threads each time an NFS client connects. This process corresponds to the **nfs** service.
> *   **lockd** - **lockd** is a kernel thread which runs on both clients and servers. It implements the Network Lock Manager (NLM) protocol, which allows NFSv2 and NFSv3 clients to lock files on the server. It is started automatically whenever the NFS server is run and whenever an NFS file system is mounted.
> *   **rpc.statd**- This process implements the Network Status Monitor (NSM) RPC protocol, which notifies NFS clients when an NFS server is restarted without being gracefully brought down. **rpc.statd** is started automatically by the **nfslock** service, and does not require user configuration. This is not used with NFSv4.
> *   **rpc.rquotad**- This process provides user quota information for remote users. **rpc.rquotad** is started automatically by the nfs service and does not require user configuration.
> *   **rpc.idmapd** - **rpc.idmapd** provides NFSv4 client and server upcalls, which map between on-the-wire NFSv4 names (which are strings in the form of **user@domain**) and local UIDs and GIDs. For **idmapd** to function with NFSv4, the **/etc/idmapd.conf** file must be configured. This service is required for use with NFSv4, although not when all hosts share the same DNS domain name.

### Working with NFS Services

From the above guide:

> To run an NFS server, the **rpcbind** service must be running. To verify that **rpcbind** is active, use the following command:
> 
>     # service rpcbind status
>     
> 
> If the **rpcbind** service is running, then the **nfs** service can be started. To start an NFS server, use the following command:
> 
>     # service nfs start
>     
> 
> **nfslock** must also be started for both the NFS client and server to function properly. To start NFS locking, use the following command:
> 
>     # service nfslock start
>     
> 
> If NFS is set to start at boot, ensure that **nfslock** also starts by running `chkconfig --list nfslock`. If **nfslock** is not set to **on**, this implies that you will need to manually run the `service nfslock start` each time the computer starts. To set **nfslock** to automatically start on boot, use `chkconfig nfslock on`.
> 
> **nfslock** is only needed for NFSv2 and NFSv3.
> 
> To stop the server, use:
> 
>     # service nfs stop
>     
> 
> The restart option is a shorthand way of stopping and then starting NFS. This is the most efficient way to make configuration changes take effect after editing the configuration file for NFS. To restart the server type:
> 
>     # service nfs restart
>     
> 
> The **condrestart** (conditional restart) option only starts nfs if it is currently running. This option is useful for scripts, because it does not start the daemon if it is not running. To conditionally restart the server type:
> 
>     # service nfs condrestart
>     
> 
> To reload the NFS server configuration file without restarting the service type:
> 
>     # service nfs reload
>     

### NFS Server Configuration

From the Storage Administration Guide:

> There are two ways to configure an NFS server:
> 
> *   Manually editing the NFS configuration file, that is, **/etc/exports**, and
> *   through the command line, that is, by using the command **exportfs**

#### /etc/exports Configuration

From the same guide:

> The **/etc/exports** file controls which file systems are exported to remote hosts and specifies options. It follows the following syntax rules:
> 
> *   Blank lines are ignored.
> *   To add a comment, start a line with the hash mark (**#**).
> *   You can wrap long lines with a backslash (\****).
> *   Each exported file system should be on its own individual line.
> *   Any lists of authorized hosts placed after an exported file system must be separated by space characters.
> *   Options for each of the hosts must be placed in parentheses directly after the host identifier, without any spaces separating the host and the first parenthesis.
> 
> Each entry for an exported file system has the following structure:
> 
>     export host(options)
>      
>     
> 
> The aforementioned structure uses the following variables:
> 
> *   **export** - The directory being exported
> *   **host** - The host or network to which the export is being shared
> *   **options** - The options to be used for host
> 
> It is possible to specify multiple hosts, along with specific options for each host. To do so, list them on the same line as a space-delimited list, with each hostname followed by its respective options (in parentheses), as in:
> 
>     export host1(options1) host2(options2) host3(options3)
>     
> 
> In its simplest form, the **/etc/exports** file only specifies the exported directory and the hosts permitted to access it, as in the following example:
> 
>     /exported/directory bob.example.com
>     
> 
> Here, **bob.example.com** can mount **/exported/directory/** from the NFS server. Because no options are specified in this example, NFS will use default settings.
> 
> The default settings are:
> 
> *   **ro** - The exported file system is read-only. Remote hosts cannot change the data shared on the file system. To allow hosts to make changes to the file system (that is, read/write), specify the rw option.
> *   **sync** - The NFS server will not reply to requests before changes made by previous requests are written to disk. To enable asynchronous writes instead, specify the option async.
> *   **wdelay** - The NFS server will delay writing to the disk if it suspects another write request is imminent. This can improve performance as it reduces the number of times the disk must be accesses by separate write commands, thereby reducing write overhead. To disable this, specify the **no_wdelay**. **no_wdelay** is only available if the default **sync** option is also specified.
> *   **root_squash** - This prevents root users connected remotely (as opposed to locally) from having root privileges; instead, the NFS server will assign them the user ID nfsnobody. This effectively "squashes" the power of the remote root user to the lowest local user, preventing possible unauthorized writes on the remote server. To disable root squashing, specify **no\_root\_squash**.
> 
> To squash every remote user (including root), use **all_squash**. To specify the user and group IDs that the NFS server should assign to remote users from a particular host, use the **anonuid** and **anongid** options, respectively, as in:
> 
>     export host(anonuid=uid,anongid=gid)
>     
> 
> Here, **uid** and **gid** are user ID number and group ID number, respectively. The **anonuid** and **anongid** options allow you to create a special user and group account for remote NFS users to share.
> 
> By default, access control lists (ACLs) are supported by NFS under Red Hat Enterprise Linux. To disable this feature, specify the **no_acl** option when exporting the file system.
> 
> Each default for every exported file system must be explicitly overridden. For example, if the **rw** option is not specified, then the exported file system is shared as read-only. The following is a sample line from **/etc/exports** which overrides two default options:
> 
>     /another/exported/directory 192.168.0.3(rw,async)
>     
> 
> In this example **192.168.0.3** can mount **/another/exported/directory/** read/write and all writes to disk are asynchronous.
> 
> Other options are available where no default value is specified. These include the ability to *disable sub-tree checking*, *allow access from insecure ports*, and *allow insecure file locks* (necessary for certain early NFS client implementations).

Here are the hostname formats from the same guide:

> The host(s) can be in the following forms:
> 
> *   **Single machine** - A fully-qualified domain name (that can be resolved by the server), hostname (that can be resolved by the server), or an IP address.
> *   **Series of machines specified with wildcards** - Use the \***** or **?** character to specify a string match. Wildcards are not to be used with IP addresses; however, they may accidentally work if reverse DNS lookups fail. When specifying wildcards in fully qualified domain names, dots (.) are not included in the wildcard. For example, ***.example.com** includes **one.example.com** but does not include **one.two.example.com**.
> *   **IP networks** - Use **a.b.c.d/z**, where **a.b.c.d** is the network and **z** is the number of bits in the netmask (for example **192.168.0.0/24**). Another acceptable format is **a.b.c.d/netmask**, where **a.b.c.d** is the network and **netmask** is the netmask (for example, **192.168.100.8/255.255.255.0**).
> *   **Netgroups** - Use the format **@group-name**, where **group-name** is the NIS netgroup name.

#### exportfs Command

From the same guide:

> Every file system being exported to remote users with NFS, as well as the access level for those file systems, are listed in the **/etc/exports** file. When the **nfs** service starts, the **/usr/sbin/exportfs** command launches and reads this file, passes control to **rpc.mountd** (if NFSv2 or NFSv3) for the actual mounting process, then to **rpc.nfsd** where the file systems are then available to remote users.
> 
> When issued manually, the **/usr/sbin/exportfs** command allows the root user to selectively export or unexport directories without restarting the NFS service. When given the proper options, the **/usr/sbin/exportfs** command writes the exported file systems to **/var/lib/nfs/xtab**. Since **rpc.mountd** refers to the **xtab** file when deciding access privileges to a file system, changes to the list of exported file systems take effect immediately.
> 
> The following is a list of commonly-used options available for **/usr/sbin/exportfs**:
> 
> *   **-r** - Causes all directories listed in **/etc/exports** to be exported by constructing a new export list in **/etc/lib/nfs/xtab**. This option effectively refreshes the export list with any changes made to **/etc/exports**.
> *   **-a** - Causes all directories to be exported or unexported, depending on what other options are passed to **/usr/sbin/exportfs**. If no other options are specified, **/usr/sbin/exportfs** exports all file systems specified in **/etc/exports**.
> *   **-o file-systems** - Specifies directories to be exported that are not listed in **/etc/exports**. Replace **file-systems** with additional file systems to be exported. These file systems must be formatted in the same way they are specified in **/etc/exports**. This option is often used to test an exported file system before adding it permanently to the list of file systems to be exported.
> *   **-i** - Ignores **/etc/exports**; only options given from the command line are used to define exported file systems.
> *   **-u** - Unexports all shared directories. The command `/usr/sbin/exportfs -ua` suspends NFS file sharing while keeping all NFS daemons up. To re-enable NFS sharing, use `exportfs -r`.
> *   **-v** - Verbose operation, where the file systems being exported or unexported are displayed in greater detail when the exportfs command is executed. If no options are passed to the exportfs command, it displays a list of currently exported file systems. 
> 
> In Red Hat Enterprise Linux 6, no extra steps are required to configure NFSv4 exports as any filesystems mentioned are automatically available to NFSv2, NFSv3, and NFSv4 clients using the same path. This was not the case in previous versions.
> 
> To prevent clients from using NFSv4, turn it off by sellecting **RPCNFSDARGS= -N 4** in **/etc/sysconfig/nfs**.

### NFS Behind a Firewall

From the above guide:

> NFS requires **rpcbind**, which dynamically assigns ports for RPC services and can cause problems for configuring firewall rules. To allow clients to access NFS shares behind a firewall, edit the **/etc/sysconfig/nfs** configuration file to control which ports the required RPC services run on.
> 
> The **/etc/sysconfig/nfs** may not exist by default on all systems. If it does not exist, create it and add the following variables, replacing port with an unused port number (alternatively, if the file exists, un-comment and change the default entries as required):
> 
> *   **MOUNTD_PORT=port** - Controls which TCP and UDP port **mountd** (**rpc.mountd**) uses.
> *   **STATD_PORT=port** - Controls which TCP and UDP port status (**rpc.statd**) uses.
> *   **LOCKD_TCPPORT=port** - Controls which TCP port nlockmgr (**lockd**) uses.
> *   **LOCKD_UDPPORT=port** - Controls which UDP port nlockmgr (**lockd**) uses.
> 
> If NFS fails to start, check **/var/log/messages**. Normally, NFS will fail to start if you specify a port number that is already in use. After editing **/etc/sysconfig/nfs**, restart the NFS service using service nfs restart. Run the `rpcinfo -p` command to confirm the changes.
> 
> To configure a firewall to allow NFS, perform the following steps:
> 
> 1.  Allow TCP and UDP port 2049 for NFS.
> 2.  Allow TCP and UDP port 111 (rpcbind/sunrpc).
> 3.  Allow the TCP and UDP port specified with MOUNTD_PORT="port"
> 4.  Allow the TCP and UDP port specified with STATD_PORT="port"
> 5.  Allow the TCP port specified with LOCKD_TCPPORT="port"
> 6.  Allow the UDP port specified with LOCKD_UDPPORT="port"

### NFS and rpcbind

From the Storage Administration Guide:

> **Note:**  
> The following section only applies to NFSv2 or NFSv3 implementations that require the **rpcbind** service for backward compatibility.
> 
> The **rpcbind** utility maps RPC services to the ports on which they listen. RPC processes notify **rpcbind** when they start, registering the ports they are listening on and the RPC program numbers they expect to serve. The client system then contacts **rpcbind** on the server with a particular RPC program number. The **rpcbind** service redirects the client to the proper port number so it can communicate with the requested service.
> 
> Because RPC-based services rely on **rpcbind** to make all connections with incoming client requests, **rpcbind** must be available before any of these services start. The **rpcbind** service uses TCP wrappers for access control, and access control rules for **rpcbind** affect all RPC-based services. Alternatively, it is possible to specify access control rules for each of the NFS RPC daemons.

### NFSv4 Server Example Setup

So let's go ahead and configure an NFS server on our RH6 machine. First let's install the necessary packages:

    [root@rhel1 ~]# yum install nfs-utils
    

Now let's check out the services states:

    [root@rhel1 ~]# chkconfig --list | grep -E 'nfs|rpc'
    nfs             0:off   1:off   2:off   3:off   4:off   5:off   6:off
    nfslock         0:off   1:off   2:off   3:on    4:on    5:on    6:off
    rpcbind         0:off   1:off   2:on    3:on    4:on    5:on    6:off
    rpcgssd         0:off   1:off   2:off   3:on    4:on    5:on    6:off
    rpcidmapd       0:off   1:off   2:off   3:on    4:on    5:on    6:off
    rpcsvcgssd      0:off   1:off   2:off   3:off   4:off   5:off   6:off
    

Now let's enable **nfs** and since I am using version 4, let's disable the **nfslock** service:

    [root@rhel1 ~]# chkconfig nfs on
    [root@rhel1 ~]# chkconfig nfslock off
    

Now let's start the service and make sure it's running:

    [root@rhel1 ~]# service nfs start
    Starting NFS services:  
    Starting NFS daemon:  rpc.nfsd
    Starting NFS mountd:  rpc.mountd
    Starting RPC idmapd:  rpc.idmapd
    [root@rhel1 ~]# service nfs status
    rpc.svcgssd is stopped
    rpc.mountd (pid 13816) is running...
    nfsd (pid 13813 13812 13811 13810 13809 13808 13807 13806) is running...
    

Also let's make sure all the services are correctly registered with RPC:

    [root@rhel1 ~]# rpcinfo -p |  awk '{ if (a[$5]++ == 0) print $0; }' "$@"
       program vers proto   port  service
        100000    4   tcp    111  portmapper
        100003    2   tcp   2049  nfs
        100227    2   tcp   2049  nfs_acl
        100021    1   udp  35352  nlockmgr
        100005    1   udp  34344  mountd
    

Now let's disable everything below version 4. This is done by editing **/etc/sysconfig/nfs** and uncommenting the following:

    # Define which protocol versions mountd
    # will advertise. The values are "no" or "yes"
    # with yes being the default
    MOUNTD_NFS_V2="no"
    MOUNTD_NFS_V3="no"
    
     # Turn off v2 and v3 protocol support
    RPCNFSDARGS="-N 2 -N 3"
    

Now let's restart the services and make sure the changes are applied:

    [root@rhel1 ~]# service nfs restart
    Shutting down NFS mountd: rpc.mountd 
    Shutting down NFS daemon: nfsd 
    Starting NFS services:  
    Starting NFS daemon:  rpc.nfsd
    Starting NFS mountd:  rpc.mountd
    [root@rhel1 ~]# rpcinfo -p |  awk '{ if (a[$5]++ == 0) print $0; }' "$@"
       program vers proto   port  service
        100000    4   tcp    111  portmapper
        100003    4   tcp   2049  nfs
        100021    1   udp  36827  nlockmgr
    

Now we can see that **mountd** is no longer registered with RPC and **nfs** is on version **4**.

Now let's create a directory which we will share with our RH5 client and allow access to that client.

    [root@rhel1 ~]# mkdir /nfs
    [root@rhel1 ~]# echo "nfs test" > /nfs/file
    

Now let's add that directory to our **/etc/exports** file and allow write capabilities:

    [root@rhel1 ~]# cat /etc/exports 
    /nfs 192.168.2.3(rw,sync,sec=sys)
    

Now let's apply those settings:

    [root@rhel1 ~]# exportfs -rv
    exporting 192.168.2.3:/nfs
    

To check all the options assigned to the export we can check out the **/var/lib/nfs/etab** file:

    [root@rhel1 ~]# cat /var/lib/nfs/etab 
    /nfs    192.168.2.3(rw,sync,wdelay,hide,nocrossmnt,secure,root_squash,no_all_squash,no_subtree_check,secure_locks,acl,anonuid=65534,anongid=65534,sec=sys,rw,root_squash,no_all_squash)
    

Lastly let's open up port **2049** since that is all that we need for NFSv4:

    [root@rhel1 ~]# iptables -I INPUT 14 -m state --state NEW -m tcp -p tcp --dport 2049 -j ACCEPT
    [root@rhel1 ~]# service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables: 
    

Now we have an NFS server allowing 1 client to mount **/nfs** using version 4. So let's move to the client section.

### NFS Client configuration

From the Storage Administration Guide:

> The **mount** command mounts NFS shares on the client side. Its format is as follows:
> 
>     # mount -t nfs -o options host:/remote/export /local/directory
>     
> 
> This command uses the following variables:
> 
> *   **options** - A comma-delimited list of mount options
> *   **server** - The hostname, IP address, or fully qualified domain name of the server exporting the file system you wish to mount
> *   **/remote/export** - The file system or directory being exported from the **server**, that is, the directory you wish to mount
> *   **/local/directory** - The client location where **/remote/export** is mounted
> 
> The NFS protocol version used in Red Hat Enterprise Linux 6 is identified by the mount options **nfsvers** or **vers**. By default, **mount** will use NFSv4 with `mount -t nfs`. If the server does not support NFSv4, the client will automatically step down to a version supported by the server. If the **nfsvers/vers** option is used to pass a particular version not supported by the server, the mount will fail. The file system type **nfs4** is also available for legacy reasons; this is equivalent to running `mount -t nfs -o nfsvers=4 host:/remote/export /local/directory`.
> 
> If an NFS share was mounted manually, the share will not be automatically mounted upon reboot. Red Hat Enterprise Linux offers two methods for mounting remote file systems automatically at boot time: the **/etc/fstab** file and the **autofs** service.

We will only cover the fstab approach.

### Mounting NFS Shares with /etc/fstab

From the same guide:

> An alternate way to mount an NFS share from another machine is to add a line to the **/etc/fstab** file. The line must state the hostname of the NFS server, the directory on the server being exported, and the directory on the local machine where the NFS share is to be mounted. You must be root to modify the **/etc/fstab** file.
> 
> The general syntax for the line in **/etc/fstab** is as follows:
> 
>     server:/usr/local/pub    /pub   nfs    defaults 0 0
>     
> 
> The mount point **/pub** must exist on the client machine before this command can be executed. After adding this line to **/etc/fstab** on the client system, use the command `mount /pub`, and the mount point **/pub** is mounted from the server.
> 
> The **/etc/fstab** file is referenced by the **netfs** service at boot time, so lines referencing NFS shares have the same effect as manually typing the **mount** command during the boot process.
> 
> A valid **/etc/fstab** entry to mount an NFS export should contain the following information:
> 
>     server:/remote/export /local/directory nfs options 0 0
>     
> 
> The variables **server**, **/remote/export**, **/local/directory**, and **options** are the same ones used when manually mounting an NFS share.

### NFS Mount options

From the above guide:

> Beyond mounting a file system with NFS on a remote host, it is also possible to specify other options at mount time to make the mounted share easier to use. These options can be used with manual mount commands, **/etc/fstab** settings, and **autofs**.
> 
> The following are options commonly used for NFS mounts:
> 
> *   **intr** - Allows NFS requests to be interrupted if the server goes down or cannot be reached.
> *   **lookupcache=mode** - Specifies how the kernel should manage its cache of directory entries for a given mount point. Valid arguments for **mode** are **all**, **none**, or **pos/positive**.
> *   **nfsvers=version** - Specifies which version of the NFS protocol to use, where **version** is **2**, **3**, or **4**. This is useful for hosts that run multiple NFS servers. If no version is specified, NFS uses the highest version supported by the kernel and mount command.
>     
>     The option **vers** is identical to **nfsvers**, and is included in this release for compatibility reasons.
> 
> *   **noacl** - Turns off all ACL processing. This may be needed when interfacing with older versions of Red Hat Enterprise Linux, Red Hat Linux, or Solaris, since the most recent ACL technology is not compatible with older systems.
> 
> *   **nolock** - Disables file locking. This setting is occasionally required when connecting to older NFS servers.
> 
> *   **noexec** - Prevents execution of binaries on mounted file systems. This is useful if the system is mounting a non-Linux file system containing incompatible binaries.
> 
> *   nosuid - Disables **set-user-identifier** or **set-group-identifier** bits. This prevents remote users from gaining higher privileges by running a **setuid** program.
> 
> *   **port=num** - Specifies the numeric value of the NFS server port. If **num** is **** (the default), then **mount** queries the remote host's **rpcbind** service for the port number to use. If the remote host's NFS daemon is not registered with its rpcbind service, the standard NFS port number of TCP **2049** is used instead.
> 
> *   **rsize=num and wsize=num** - These settings speed up NFS communication for reads (**rsize**) and writes (**wsize**) by setting a larger data block size (**num**, in bytes), to be transferred at one time. Be careful when changing these values; some older Linux kernels and network cards do not work well with larger block sizes. For NFSv2 or NFSv3, the default values for both parameters is set to **8192**. For NFSv4, the default values for both parameters is set to **32768**.
> *   **sec=mode** - Specifies the type of security to utilize when authenticating an NFS connection. Its default setting is **sec=sys**, which uses local UNIX **UIDs** and **GIDs** by using **AUTH_SYS** to authenticate NFS operations.
>     
>     **sec=krb5** uses Kerberos V5 instead of local UNIX UIDs and GIDs to authenticate users.
>     
>     **sec=krb5i** uses Kerberos V5 for user authentication and performs integrity checking of NFS operations using secure checksums to prevent data tampering.
>     
>     **sec=krb5p** uses Kerberos V5 for user authentication, integrity checking, and encrypts NFS traffic to prevent traffic sniffing. This is the most secure setting, but it also involves the most performance overhead.
> 
> *   **tcp** - Instructs the NFS mount to use the TCP protocol.
> 
> *   **udp** - Instructs the NFS mount to use the UDP protocol.

### NFS Client Example

Now let's install the same package on our RH5 machine and try to mount the share from our RH6 server:

    [root@rhel2 ~]# yum install nfs-utils
    

Now let's create a local directory where I will mount the remote directory:

    [root@rhel2 ~]# mkdir /mnt/nfs
    

Since RH5 uses NFSv3 by default during the mount, let's specify the version and mount the remote directory:

    [root@rhel2 ~]# mount -t nfs4 192.168.2.2:/nfs /mnt/nfs
    [root@rhel2 ~]# 
    

We can check stats regarding the mount point with **nfsstat**:

    [root@rhel2 ~]# nfsstat 
    Client rpc stats:
    calls      retrans    authrefrsh
    59         0          0       
    
    Client nfs v4:
    null         read         write        commit       open         open_conf    
    0         0% 2         3% 0         0% 0         0% 5         8% 2         3% 
    open_noat    open_dgrd    close        setattr      fsinfo       renew        
    0         0% 0         0% 2         3% 0         0% 6        10% 0         0% 
    setclntid    confirm      lock         lockt        locku        access       
    2         3% 2         3% 0         0% 0         0% 0         0% 3         5% 
    getattr      lookup       lookup_root  remove       rename       link         
    12       21% 6        10% 3         5% 0         0% 0         0% 0         0% 
    symlink      create       pathconf     statfs       readlink     readdir      
    0         0% 0         0% 0         0% 0         0% 0         0% 2         3% 
    server_caps  delegreturn  
    9        16% 0         0% 
    

As a quick test change the permission of the file to user1 on the server side:

    [root@rhel1 ~]# chown user1:user1 /nfs/file 
    

Then from the client side, as user1, make sure you can write to the file:

    [user1@rhel2 ~]$ echo append >> /mnt/nfs/file 
    [user1@rhel2 ~]$ cat /mnt/nfs/file
    nfs test
    append
    

If we wanted to, we could add the following to the RH5 machine's **/etc/fstab** file to mount the NFS share on boot:

    192.168.2.2:/nfs /mnt/nfs nfs4 rw,sync 0 0
    

### NFSv3 Server Example Setup

Let's switch the roles around and setup the RH5 machine to be an NFSv3 Server and have the RH6 machine be the client. We already have the packages installed on the RH5 system, so let's start the NFS server:

    [root@rhel2 ~]# service nfs start
    Starting NFS services:                                     [  OK  ]
    Starting NFS quotas:                                       [  OK  ]
    Starting NFS daemon:                                       [  OK  ]
    Starting NFS mountd:                                       [  OK  ]
    

Now let's make sure all the RPC services are bound:

    [root@rhel2 ~]# rpcinfo -p |  awk '{ if (a[$5]++ == 0) print $0; }' "$@"
       program vers proto   port
        100000    2   tcp    111  portmapper
        100024    1   udp    925  status
        100011    1   udp    660  rquotad
        100003    2   udp   2049  nfs
        100021    1   udp  45834  nlockmgr
        100005    1   udp    685  mountd
    

Since we want to open up the firewall, let's statically assign ports to the other RPC services. This is done by editing the **/etc/sysconfig/nfs** file and modifying the following lines:

    [root@rhel2 ~]# grep -vE '^$|^#' /etc/sysconfig/nfs
    LOCKD_TCPPORT=32803
    LOCKD_UDPPORT=32769
    RPCNFSDARGS="-N 4"
    MOUNTD_PORT=892
    STATD_PORT=662
    

Notice I also explicitly disabled NFSv4 (with the **RPCNFSDARGS** variable). After a `service nfs restart` and a `service nfslock restart`, I saw the following settings for the RPC services:

    [root@rhel2 ~]# rpcinfo -p |  awk '{ if (a[$5]++ == 0) print $0; }' "$@"
       program vers proto   port
        100000    2   tcp    111  portmapper
        100011    1   udp    762  rquotad
        100003    2   udp   2049  nfs
        100021    1   udp  32769  nlockmgr
        100005    1   udp    892  mountd
        100024    1   udp    662  status
    

Now let's open up the firewall for the defined ports:

    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m tcp -p tcp --dport 2049 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m udp -p udp --dport 2049 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m tcp -p tcp --dport 111 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m udp -p udp --dport 111 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m tcp -p tcp --dport 892 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m udp -p udp --dport 892 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m tcp -p tcp --dport 662 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m udp -p udp --dport 662 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m tcp -p tcp --dport 32803 -j ACCEPT
    [root@rhel2 ~]# iptables -I RH-Firewall-1-INPUT 9 -m state --state NEW -m udp -p udp --dport 32769 -j ACCEPT
    

Finally save the rules:

    [root@rhel2 ~]# service iptables save
    Saving firewall rules to /etc/sysconfig/iptables:          [  OK  ]
    

Now let's setup our export:

    [root@rhel2 ~]# mkdir /nfs
    [root@rhel2 ~]# cat /etc/exports 
    /nfs 192.168.2.2(rw,sync)
    

And then to apply the exports:

    [root@rhel2 ~]# exportfs -rva
    exporting 192.168.2.2:/nfs
    

Here are the options assigned to the export by default:

    [root@rhel2 ~]# cat /var/lib/nfs/etab 
    /nfs    192.168.2.2(rw,sync,wdelay,hide,nocrossmnt,secure,root_squash,no_all_squash,no_subtree_check,secure_locks,acl,mapping=identity,anonuid=65534,anongid=65534)
    

### NFSv3 Client

Now from the RH6 machine let's see what mounts are available. Since we are running **mountd**, we can use **showmount** to check available mounts on a remote server:

    [root@rhel1 ~]# showmount -e 192.168.2.3
    Export list for 192.168.2.3:
    /nfs 192.168.2.2
    

Now to mount the share:

    [root@rhel1 ~]# mkdir /mnt/nfs
    [root@rhel1 ~]# mount -t nfs 192.168.2.3:/nfs /mnt/nfs
    [root@rhel1 ~]#
    

You can also check all the mount options, from the **nfsstat** utility:

    [root@rhel1 ~]# nfsstat -m
    /mnt/nfs from 192.168.2.3:/nfs
     Flags: rw,relatime,vers=3,rsize=32768,wsize=32768,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,mountaddr=192.168.2.3,mountvers=3,mountport=892,mountproto=udp,local_lock=none,addr=192.168.2.3
    

We can see that we are using **version 3**. I also created a file on the server and I was able to see appropriate UIDs:

    [root@rhel1 ~]# ls -l /mnt/nfs
    total 4
    -rw-r--r--. 1 user1 user1 9 Mar 22  2014 file
    

and I was able to add to the file without issues:

    [user1@rhel1 ~]$ echo append >> /mnt/nfs/file 
    [user1@rhel1 ~]$
    

### NFS Security

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Confined_Services/Red_Hat_Enterprise_Linux-6-Managing_Confined_Services-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Managing_Confined_Services/Red_Hat_Enterprise_Linux-6-Managing_Confined_Services-en-US.pdf']);">Managing Confined Services</a>:

> A Network File System (NFS) allows remote hosts to mount file systems over a network and interact with those file systems as though they are mounted locally. This enables system administrators to consolidate resources onto centralized servers on the network.
> 
> In Red Hat Enterprise Linux, the nfs-utils package is required for full NFS support. Run the `rpm -q nfs-utils` command to see if the **nfs-utils** is installed. If it is not installed and you want to use NFS, run the following command as the root user to install it:
> 
>     ~]# yum install nfs-utils
>     
> 
> When running SELinux, the NFS daemons are confined by default. SELinux policy allows NFS to share files by default.

#### NFS SELinux Types and Booleans

From the same guide:

> By default, mounted NFS volumes on the client side are labeled with a default context defined by policy for NFS. In common policies, this default context uses the **nfs_t** type. The following types are used with NFS. Different types allow you to configure flexible access:
> 
> *   **var\_lib\_nfs_t** - This type is used for existing and new files copied to or created in the **/var/lib/nfs/** directory. This type should not need to be changed in normal operation. To restore changes to the default settings, run the **restorecon -R -v /var/lib/nfs** command as the root user.
> *   **nfsd\_exec\_t** - The **/usr/sbin/rpc.nfsd** file is labeled with the **nfsd\_exec\_t**, as are other system executables and libraries related to NFS. Users should not label any files with this type. **nfsd\_exec\_t** will transition to **nfsd_t**.
> 
> SELinux is based on the least level of access required for a service to run. Services can be run in a variety of ways; therefore, you need to specify how you run your services. Use the following Booleans to set up SELinux:
> 
> *   **allow\_ftpd\_use_nfs** - When enabled, this Boolean allows the **ftpd** daemon to access NFS volumes.
> *   **cobbler\_use\_nfs** - When enabled, this Boolean allows the **cobblerd** daemon to access NFS volumes.
> *   **git\_system\_use_nfs** - When enabled, this Boolean allows the **Git** system daemon to read system shared repositories on NFS volumes.
> *   **httpd\_use\_nfs** - When enabled, this Boolean allows the **httpd** daemon to access files stored on NFS volumes.
> *   **qemu\_use\_nfs** - When enabled, this Boolean allows **Qemu** to use NFS volumes.
> *   **rsync\_use\_nfs** - When enabled, this Boolean allows **rsync** servers to share NFS volumes.
> *   **samba\_share\_nfs** - When enabled, this Boolean allows the **smbd** daemon to share NFS volumes. When disabled, this Boolean prevents **smbd** from having full access to NFS shares via Samba.
> *   **sanlock\_use\_nfs** - When enabled, this Boolean allows the **sanlock** daemon to manage NFS volumes.
> *   **sge\_use\_nfs** - When enabled, this Boolean allows the **sge** scheduler to access NFS volumes.
> *   **use\_nfs\_home_dirs** - When enabled, this Boolean adds support for NFS home directories.
> *   **virt\_use\_nfs** - When enabled, this Boolean allows confident virtual guests to manage files on NFS volumes.
> *   **xen\_use\_nfs** When enabled, this Boolean allows **Xen** to manage files on NFS volumes.
> *   **git\_cgi\_use_nfs** - When enabled, this Boolean allows the Git Common Gateway Interface (CGI) to access NFS volumes.
> *   **tftp\_use\_nfs** - When enabled, this Boolean allows The Trivial File Transfer Protocol (**TFTP**) to read from NFS volumes for public file transfer services.

As mentioned above, by default SELinux allows NFS to share directories. I didn't have to make any changes to my RH5 or RH6 systems. To check out the booleans available for NFS just run the **getseboolean** command. Here were the defaults on my system:

    [root@rhel1 ~]# getsebool -a | grep -i nfs
    allow_ftpd_use_nfs --> off
    allow_nfsd_anon_write --> off
    cobbler_use_nfs --> off
    git_system_use_nfs --> off
    httpd_use_nfs --> off
    nfs_export_all_ro --> on
    nfs_export_all_rw --> on
    qemu_use_nfs --> on
    samba_share_nfs --> off
    use_nfs_home_dirs --> on
    virt_use_nfs --> off
    xen_use_nfs --> off
    

On top of SELinux, we can also use TCP wrappers and IPtables (which we did) to limit access to the NFS Shares (both of these topics were covered in <a href="http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-12-system-security/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-12-system-security/']);">Chapter 12</a>)

