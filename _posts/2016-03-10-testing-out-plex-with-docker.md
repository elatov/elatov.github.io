---
published: true
layout: post
title: "Testing Out Plex with Docker"
author: Karim Elatov
categories: [docker,os,networking]
tags: [plex,linux,centos]
---
In my [previous post](/2016/02/trying-out-madsonic) I realized that you can't bind a Plex instance to a specific IP. Some people have had luck accomplishing that with **docker**. I have heard many things about **docker** so I decided to give it a try.

### Install Docker 
Let's install **docker**, I was using CentOS 7 and **docker** is part of the default repositories. So the following took care of installing **docker**:

    sudo yum install docker

If you want regular users to be able to run *containers* it's best to create a **docker** group and assign users to it. Here are some references:

* [Quickstart containers](https://docs.docker.com/engine/userguide/basics/)
* [Create a docker group](https://docs.docker.com/engine/installation/centos/#create-a-docker-group)

Let's add a group so users part of that group can run **docker** commands:

    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:35:45]
    └─[6] <> sudo groupadd docker
    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:35:58]
    └─[0] <> sudo usermod -aG docker elatov

Then logout (and login back in) and make sure you are part of the group

    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:37:01]
    └─[0] <> groups
    elatov wheel mail exim ossec docker


So let's go ahead and start the **docker** service:

    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:30:48]
    └─[1] <> sudo systemctl start docker

### Getting a Docker Image
Now let's get the **docker** image for centos7, the repo for that is [here](https://hub.docker.com/_/centos/). To get the image we can use "**docker pull**":

    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:37:02]
    └─[0] <> docker pull centos
    Using default tag: latest
    Trying to pull repository docker.io/library/centos ... latest: Pulling from library/centos
    
    47d44cb6f252: Pull complete
    838c1c5c4f83: Pull complete
    5764f0a31317: Pull complete
    60e65a8e4030: Pull complete
    library/centos:latest: The image you are pulling has been verified. Important: image verification is a tech preview feature and should not be relied on to provide security.
    
    Digest: sha256:8072bc7c66c3d5b633c3fddfc2bf12d5b4c2623f7004d9eed6aae70e0e99fbd7
    Status: Downloaded newer image for docker.io/centos:latest

To confirm the image is there we can use the "**docker images**" command:

    ┌─[elatov@m2] - [/home/elatov] - [2015-12-31 10:45:51]
    └─[0] <> docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    docker.io/centos    latest              60e65a8e4030        7 days ago          196.6 MB

### Creating a Custom Bridge Device for Docker

By default **docker** creates an internal bridge (**docker0**, more information about docker networking is [here](https://docs.docker.com/v1.8/articles/networking/)) that doesn't have an uplink and uses NAT capabilities from iptables to NAT traffic out or create port forwards (DNAT) to *containers*. Since Plex uses multicast for DLNA I decided to create a custom bridge which will allow *containers* direct access to the network. There are a couple of cool posts that discuss **docker** networking:

* [Setting up a Docker Bridge](https://www.ibm.com/developerworks/community/blogs/powermeup/entry/Setting_up_a_Docker_Bridge?lang=en)
* [Four ways to connect a docker container to a local network](http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/)
* [Docker Networking 101 – Host mode](http://www.dasblinkenlichten.com/docker-networking-101-host-mode/)
* [How to expose docker container's ip and port to outside docker host without port mapping](http://stackoverflow.com/questions/25036895/how-to-expose-docker-containers-ip-and-port-to-outside-docker-host-without-port/25041782#25041782)

If you want to assign static IPs to VMs there are a couple third party scripts which allow you to do that:

* [pipework](https://github.com/jpetazzo/pipework)
* [docker_static_ip.sh](https://gist.github.com/andreyserdjuk/bd92b5beba2719054dfe)

From the sound of it, the static IP feature will probably be part of docker soon though. I didn't need static IPs as I was just playing around with the setup.

Instructions on how to create your own bridge are at [Building your own bridge](https://docs.docker.com/v1.8/articles/networking/#building-your-own-bridge). First let's install the **bridge-utils**:

	sudo yum install bridge-utils

Now I ended up using **ens160** as my uplink to the **bridge** and then creating a brdige device. Here are the files I ended up with:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:38:18]
	└─[0] <> cat /etc/sysconfig/network-scripts/ifcfg-ens160
	TYPE=Ethernet
	BOOTPROTO=none
	IPV6INIT=no
	NAME=ens160
	ONBOOT=yes
	HWADDR=00:0C:29:A3:D4:FA
	#IPADDR=192.168.1.100
	#PREFIX=24
	#GATEWAY=192.168.1.1
	BRIDGE=br0

and here is the bridge device:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:38:29]
	└─[0] <> cat /etc/sysconfig/network-scripts/ifcfg-br0
	DEVICE=br0
	TYPE=Bridge
	BOOTPROTO=none
	IPV6INIT=no
	NAME=br0
	ONBOOT=yes
	IPADDR=192.168.1.100
	PREFIX=24
	GATEWAY=192.168.1.1
	DELAY=0

After a service restart:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:35:21]
	└─[0] <> sudo systemctl restart network

I saw the following IP configuration:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:35:33]
	└─[0] <> ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
	    inet 172.17.42.1/16 scope global docker0
	       valid_lft forever preferred_lft forever
	5: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
	    inet 192.168.1.100/24 brd 192.168.1.255 scope global br0
	       valid_lft forever preferred_lft forever

and using the **brclt** and **bridge** commands I could confirm that my interface is attached to the bridge:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:35:39]
	└─[0] <> brctl show
	bridge name     bridge id               STP enabled     interfaces
	br0             8000.000c29a3d4fa       no              ens160
	docker0         8000.0242471a6cf0       no
	
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:36:32]
	└─[0] <> bridge link
	2: ens160 state UP : <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br0 state forwarding priority 32 cost 2

#### Enable Docker to Use Custom Bridge Device
Now let's configure **docker** to use that bridge, first let's disable the original bridge and **iptables** rules:

	$ sudo systemctl stop docker 
	$ sudo ip link set dev docker0 down
	$ sudo brctl delbr docker0
	$ sudo iptables -t nat -F POSTROUTING

then I modified the options to look like this

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:51:09]
	└─[0] <> grep OPTIONS /etc/sysconfig/docker
	OPTIONS='-b=br0 --ip-masq=false --iptables=false'

I disabled SNAT and DNAT settings since I didn't need them any more. The options are covered [here](https://docs.docker.com/v1.8/articles/networking/#quick-guide-to-the-options). And after starting up the **docker** daemon the other bridge was gone:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:51:38]
	└─[0] <> sudo systemctl start docker
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:52:50]
	└─[0] <> ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	5: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
	    inet 192.168.1.100/24 brd 192.168.1.255 scope global br0
	       valid_lft forever preferred_lft forever
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 11:52:54]
	└─[0] <> brctl show
	bridge name     bridge id               STP enabled     interfaces
	br0             8000.000c29a3d4fa       no              ens160

### Running (and Getting Used) to Containers

Unlike VMs, *containers* don't keep running after the main process you started has stopped (some **docker** basics are covered in [Hello world in a container](https://docs.docker.com/engine/userguide/dockerizing/)). For example let's start a *container* from the centos image using interactive mode (this is the **-it** flags) and background it (that's the **-d** flag):

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:07:00]
	└─[0] <> docker run -it -d docker.io/centos /bin/bash
	5276199a151dee39ad1dcf861969802316038ee09b4d32b9d2d5c11f213ce101

This way the **docker** container will keep running:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:17:41]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	5276199a151d        docker.io/centos    "/bin/bash"         42 seconds ago      Up 42 seconds                           clever_lovelace

You can then attach to that shell, by using the **attach** parameter:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:18:28]
	└─[0] <> docker attach clever_lovelace
	
	[root@5276199a151d /]# ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 03:17 ?        00:00:00 /bin/bash
	root        14     1  0 03:19 ?        00:00:00 ps -ef

Now if I type in **exit** the shell will stop and so will the *container*, instead if I type **ctrl-P + ctrl-Q** it will keep the shell running in the background:

	[root@5276199a151d /]# %
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:20:07]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	5276199a151d        docker.io/centos    "/bin/bash"         2 minutes ago       Up 2 minutes                            clever_lovelace

I can also start another shell in the same container:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:20:54]
	└─[1] <> docker exec -it clever_lovelace /bin/bash
	[root@5276199a151d /]# ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 03:17 ?        00:00:00 /bin/bash
	root        15     0  0 03:21 ?        00:00:00 /bin/bash
	root        27    15  0 03:21 ?        00:00:00 ps -ef

If **exit** out of this one the original shell will keep running:

	[root@5276199a151d /]# exit
	exit
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:21:41]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	5276199a151d        docker.io/centos    "/bin/bash"         4 minutes ago       Up 4 minutes                            clever_lovelace

Now if I **attach** back and exit out it will stop running:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:22:21]
	└─[1] <> docker attach clever_lovelace
	[root@5276199a151d /]# exit
	exit
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:22:29]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

We can see the container is not longer running, but if we pass the **-a** paramer to the **ps** option we will see the non-running containers:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:22:31]
	└─[0] <> docker ps -a
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
	5276199a151d        docker.io/centos    "/bin/bash"         5 minutes ago       Exited (0) 42 seconds ago                       clever_lovelace

But if we want, we can start it back up:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:23:11]
	└─[0] <> docker start clever_lovelace
	clever_lovelace
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:23:30]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	5276199a151d        docker.io/centos    "/bin/bash"         5 minutes ago       Up 3 seconds                            clever_lovelace

If we didn't use the **-it** flag then the bash command would quit right away:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:24:34]
	└─[1] <> docker run -d docker.io/centos /bin/bash
	8fb31f991b12d58c1d129f8696b0950776d5b6f38e403b30b2052c393e4aec8b
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:24:57]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:25:01]
	└─[0] <> docker ps -a
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
	8fb31f991b12        docker.io/centos    "/bin/bash"         10 seconds ago      Exited (0) 9 seconds ago                       hungry_wilson

For some reason it took a while for me to get the concept that *containers* are not VMs. Another person had a similar question [here](https://forums.docker.com/t/run-command-in-stopped-container/343/6).

### Creating a Docker Image

Let's create our own image from the centos one with Plex pre-installed (sample setup can be seen at [Creating a Docker Image from an Existing Container](https://docs.oracle.com/cd/E52668_01/E54669/html/section_c5q_n2z_fp.html)). First let's launch the image and connect to it:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:29:40]
	└─[0] <> docker run -it docker.io/centos /bin/bash
	[root@17f3892da040 /]#

Now let's install some tools and clean up the **yum** cache to save space:

	[root@17f3892da040 /]# yum install iproute initscripts
	[root@17f3892da040 /]# yum clean all

Now from the **docker** host let's copy the init script

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:15:22]
	└─[0] <> docker cp /etc/init.d/plexmediaserver berserk_rosalind:/etc/init.d/
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:34:19]
	└─[0] <> docker cp /etc/sysconfig/PlexMediaServer berserk_rosalind:/etc/sysconfig/

Now let's create the **lock** directory:

	[root@17f3892da040 /]# mkdir -p /run/lock/subsys

And let's add the user:

	[root@17f3892da040 /]# groupadd -g 1000 plex
	[root@17f3892da040 /]# useradd -u 1000 -g plex plex
	
Lastly let's create the start up script and make sure it's executable:

	[root@17f3892da040 /]# ls -l /usr/bin/plex.sh
	-rwxr-xr-x 1 root root 122 Jan  1 03:41 /usr/bin/plex.sh
	[root@17f3892da040 /]# cat /usr/bin/plex.sh
	#!/bin/bash
	
	su -s /bin/sh plex -c ". /etc/sysconfig/PlexMediaServer; cd /usr/lib/plexmediaserver; ./Plex\ Media\ Server"


So let's save/commit the current changes into a new image. First let's **exit** the current container and it will stop it:

	[root@17f3892da040 /]# exit
	exit
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:38:32]
	└─[5] <> docker ps -a
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
	17f3892da040        docker.io/centos    "/bin/bash"         8 minutes ago       Exited (5) 2 seconds ago                       berserk_rosalind

Now let's create a new image from the stopped container:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:43:24]
	└─[0] <> docker commit berserk_rosalind centos-plex
	16e8ef5f55556df16e1e2477d17394093845e3d0bd6573f07c34bb5af50395f2

And let's confirm the image is there:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:43:44]
	└─[0] <> docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	centos-plex         latest              16e8ef5f5555        6 seconds ago       255.4 MB
	docker.io/centos    latest              60e65a8e4030        7 days ago          196.6 MB

### Running the Plex Docker Container

Plex wants some **ulimits** configured and luckily staring with Docker 1.6 you can pass in **ulimits** into a container (the parameter is described [here](https://docs.docker.com/engine/reference/commandline/run/#set-ulimits-in-container-ulimit)). Since I have Plex installed on the host machine, I didn't want to install it on the containers (this is definitely not best practice, but I was just playing around with the setup). So I decided to mount two folders from the host machine into the container:

* /usr/lib/plexmediaserver
* /var/lib/plexmediaserver

This is accomplished with **-v** flag to the "**docker run**" option. Now let's start a new container from our brand new image and make sure we can start the init script. So here is start another container with using **bash** as the ENTRYPOINT/main process:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:47:17]
	└─[0] <> docker run -v /usr/lib/plexmediaserver:/usr/lib/plexmediaserver -v /var/lib/plexmediaserver:/var/lib/plexmediaserver --ulimit memlock=3072000:3072000 --name=plex -it -h plex centos-plex /bin/bash
	[root@plex /]# ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 03:47 ?        00:00:00 /bin/bash
	root        16     1  0 03:47 ?        00:00:00 ps -ef

Now still in our *container* we can start the **plex** service:

	[root@plex /]# /etc/init.d/plexmediaserver start
	Starting PlexMediaServer:                                  [  OK  ]
	[root@plex /]# ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 03:47 ?        00:00:00 /bin/bash
	root        30     1  0 03:48 ?        00:00:00 su -s /bin/sh plex -c . /etc/sysconfig/PlexMediaServer;
	plex        32    30  0 03:48 ?        00:00:00 sh -c . /etc/sysconfig/PlexMediaServer; cd /usr/lib/plex
	plex        36    32 20 03:48 ?        00:00:01 ./Plex Media Server
	plex        43    36 36 03:48 ?        00:00:02 Plex Plug-in [com.plexapp.system] /usr/lib/plexmediaserv
	plex        84    36  4 03:48 ?        00:00:00 /usr/lib/plexmediaserver/Plex DLNA Server
	plex       138    36 19 03:48 ?        00:00:00 Plex Plug-in [com.plexapp.agents.fanarttv] /usr/lib/plex
	plex       140    36 19 03:48 ?        00:00:00 Plex Plug-in [com.plexapp.agents.htbackdrops] /usr/lib/p
	plex       142    36 19 03:48 ?        00:00:00 Plex Plug-in [com.plexapp.agents.lastfm] /usr/lib/plexme
	root       202     1  0 03:48 ?        00:00:00 ps -ef

That looks good. As soon as I stop the **bash** shell the container will stop. So let's start the container and set the main process as the script we created (**/usr/bin/plex.sh**) to start the plex service. Using the init script with a **systemd** OS was problematic (there are some [workarounds](http://jperrin.github.io/centos/2014/09/25/centos-docker-and-systemd/) but I didn't go down that path). In the end running the following to start the **plex** *container* worked out:

	docker run -v /usr/lib/plexmediaserver:/usr/lib/plexmediaserver -v /var/lib/plexmediaserver:/var/lib/plexmediaserver --ulimit memlock=3072000:3072000 --name=plex -it -h plex -d centos-plex /usr/bin/plex.sh

To make sure it's running:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:02:11]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS               NAMES
	bfc86fc4ed39        centos-plex         "/usr/bin/plex.sh"   33 minutes ago      Up 33 minutes                           plex

and also within the container:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 07:26:14]
	└─[0] <> docker exec plex ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 02:30 ?        00:00:00 /bin/bash /usr/bin/plex.sh
	root         6     1  0 02:30 ?        00:00:00 su -s /bin/sh elatov -c . /etc/sysconfig/PlexMediaServer; cd /usr/lib/plexmediaserver; ./Plex\ Media\ Server
	plex         7     6  0 02:30 ?        00:00:00 sh -c . /etc/sysconfig/PlexMediaServer; cd /usr/lib/plexmediaserver; ./Plex\ Media\ Server
	plex        11     7  0 02:30 ?        00:00:00 ./Plex Media Server
	plex        18    11  0 02:30 ?        00:00:05 Plex Plug-in [com.plexapp.system] /usr/lib/plexmediaserver/Resources/Plug-ins-f38ac80/Framework.bundle/Contents/Resources/Versions/2/Python/bootstrap.pyc --server-version 0.9.12.19.1537-f38ac80 /usr/lib/plexmediaserver/Resources/Plug-ins-f38ac80/System.bundle
	plex        61    11  0 02:30 ?        00:00:00 /usr/lib/plexmediaserver/Plex DLNA Server
	root       336     0  0 02:57 ?        00:00:00 ps -ef

And here is the IP within the *container*:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:04:46]
	└─[0] <> docker exec plex ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	78: eth0@if79: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP  link-netnsid 0
	    inet 192.168.1.37/24 scope global eth0
	       valid_lft forever preferred_lft forever

And on the host, I saw the virtual interface attached to the bridge:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:05:42]
	└─[0] <> brctl show
	bridge name    bridge id        STP enabled    interfaces
	br0        8000.000c29a3d4fa    no            ens160
	                                              veth907520a

And checking on other media clients I saw the new Plex Server discovered:

	┌─[elatov@gen] - [/home/elatov] - [2015-12-31 05:38:51]
	└─[0] <> gssdp-discover -i enp0s25  --timeout=3 --target=urn:schemas-upnp-org:device:MediaServer:1
	Using network interface enp0s25
	Scanning for resources matching urn:schemas-upnp-org:device:MediaServer:1
	Showing "available" messages
	resource available
	  USN:      uuid:9c675b5f-b102-fda7-fec9-c2e51cbeec5c::urn:schemas-upnp-org:device:MediaServer:1
	  Location: http://192.168.1.104:80/upnpms/dev
	resource available
	  USN:      uuid:ddfb0688-ac14-f8a5-e9c1-3bba365393b6::urn:schemas-upnp-org:device:MediaServer:1
	  Location: http://192.168.1.37:32469/DeviceDescription.xml
	resource available
	  USN:      uuid:61314ed0-059b-fd97-ffff-ffffd7babedf::urn:schemas-upnp-org:device:MediaServer:1
	  Location: http://192.168.1.100:51307/dev/61314ed0-059b-fd97-ffff-ffffd7babedf/desc

### Cleaning up Docker Containers

To stop and remove the container, let's first stop it:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:02:55]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS               NAMES
	bfc86fc4ed39        centos-plex         "/usr/bin/plex.sh"   36 minutes ago      Up 36 minutes                           plex
	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:06:42]
	└─[1] <> docker stop plex
	plex

and finally let's remove it:

	┌─[elatov@m2] - [/home/elatov] - [2015-12-31 08:10:06]
	└─[0] <> docker rm plex
	plex

### Building Docker Images with a DockerFile

If you want you can also use a [DockerFile](https://docs.docker.com/engine/reference/builder/) to help you build the image instead of running the above commands in the image. Here is an example, let's create a directory with all the appropriate files:

	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:22:33]
	└─[0] <> ls
	Dockerfile  PlexMediaServer  plex.sh
	
And here is the **DockerFile**:

	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:21:30]
	└─[0] <> cat Dockerfile
	FROM docker.io/centos:latest
	COPY plex.sh /usr/bin/
	COPY PlexMediaServer /etc/sysconfig/
	RUN chmod +x /usr/bin/plex.sh
	RUN groupadd -g 1000 plex
	RUN useradd -u 1000 -g plex plex
	ENTRYPOINT ["/usr/bin/plex.sh"]


Now we can build our new image:

	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:17:36]
	└─[0] <> docker build -t karim/centos-plex:v1 .
	Sending build context to Docker daemon 5.632 kB
	Step 0 : FROM docker.io/centos:latest
	 ---> 60e65a8e4030
	Step 1 : COPY plex.sh /usr/bin/
	 ---> 69d36851df37
	Removing intermediate container da470325f34f
	Step 2 : COPY PlexMediaServer /etc/sysconfig/
	 ---> 8d64d13329b5
	Removing intermediate container 7088c6bdbf07
	Step 3 : RUN chmod +x /usr/bin/plex.sh
	 ---> Running in 659f83565e1d
	 ---> 6b5c3681cc39
	Removing intermediate container 659f83565e1d
	Step 4 : RUN groupadd -g 1000 plex
	 ---> Running in dde8387734c6
	 ---> 4d3f6ce1feae
	Removing intermediate container dde8387734c6
	Step 5 : RUN useradd -u 1000 -g plex plex
	 ---> Running in c60f00b02c1e
	 ---> d55ce2f7fc9f
	Removing intermediate container c60f00b02c1e
	Step 6 : ENTRYPOINT /usr/bin/plex.sh
	 ---> Running in 92db7c6d103c
	 ---> 2b0851723ec4
	Removing intermediate container 92db7c6d103c
	Successfully built 2b0851723ec4

To confirm the image is built we can list out images and see it there:

	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:18:13]
	└─[0] <> docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	karim/centos-plex   v1                  2b0851723ec4        33 seconds ago      196.6 MB

If you want you can use the **inspect** option to check more information about the image:


	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:19:04]
	└─[0] <> docker inspect karim/centos-plex:v1
	[
	{
	    "Id": "2b0851723ec4981c81e630ef75e35723cc95250e2329522df80f34aba44f1c17",
	    "Parent": "d55ce2f7fc9f73417121b6057df612f89a19d4c39f5a5b7189febfd6e11c0ea3",
	    "Comment": "",
	    "Created": "2016-01-05T03:18:11.122812316Z",
	    "Container": "92db7c6d103c852e0af4cb00412032462889ab8e0739d9700f4c521d0f0dd51c",
	    "ContainerConfig": {
	        "Hostname": "f77e60ad5dfc",
	        "Domainname": "",
	        "User": "",
	        "AttachStdin": false,
	        "AttachStdout": false,
	        "AttachStderr": false,
	        "ExposedPorts": null,
	        "PublishService": "",
	        "Tty": false,
	        "OpenStdin": false,
	        "StdinOnce": false,
	        "Env": [
	            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
	        ],
	        "Cmd": [
	            "/bin/sh",
	            "-c",
	            "#(nop) ENTRYPOINT \u0026{[\"/usr/bin/plex.sh\"]}"
	        ],
	        "Image": "d55ce2f7fc9f73417121b6057df612f89a19d4c39f5a5b7189febfd6e11c0ea3",
	        "Volumes": null,
	        "VolumeDriver": "",
	        "WorkingDir": "",
	        "Entrypoint": [
	            "/usr/bin/plex.sh"
	        ],
	        "NetworkDisabled": false,
	        "MacAddress": "",
	        "OnBuild": [],
	        "Labels": {
	            "build-date": "2015-12-23",
	            "license": "GPLv2",
	            "name": "CentOS Base Image",
	            "vendor": "CentOS"
	        }
	    },
	    "DockerVersion": "1.8.2-el7.centos",
	    "Author": "",
	    "Config": {
	        "Hostname": "f77e60ad5dfc",
	        "Domainname": "",
	        "User": "",
	        "AttachStdin": false,
	        "AttachStdout": false,
	        "AttachStderr": false,
	        "ExposedPorts": null,
	        "PublishService": "",
	        "Tty": false,
	        "OpenStdin": false,
	        "StdinOnce": false,
	        "Env": [
	            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
	        ],
	        "Cmd": null,
	        "Image": "d55ce2f7fc9f73417121b6057df612f89a19d4c39f5a5b7189febfd6e11c0ea3",
	        "Volumes": null,
	        "VolumeDriver": "",
	        "WorkingDir": "",
	        "Entrypoint": [
	            "/usr/bin/plex.sh"
	        ],
	        "NetworkDisabled": false,
	        "MacAddress": "",
	        "OnBuild": [],
	        "Labels": {
	            "build-date": "2015-12-23",
	            "license": "GPLv2",
	└─[1] <>
	            "name": "CentOS Base Image",
	            "vendor": "CentOS"
	        }
	    },
	    "Architecture": "amd64",
	    "Os": "linux",
	    "Size": 0,
	    "VirtualSize": 196640548,
	    "GraphDriver": {
	        "Name": "devicemapper",
	        "Data": {
	            "DeviceId": "194",
	            "DeviceName": "docker-253:0-50331734-2b0851723ec4981c81e630ef75e35723cc95250e2329522df80f34aba44f1c17",
	            "DeviceSize": "107374182400"
	        }
	    }
	}
	]

And then doing a test run:

	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:21:06]
	└─[1] <> docker run -v /usr/lib/plexmediaserver:/usr/lib/plexmediaserver -v /var/lib/plexmediaserver:/var/lib/plexmediaserver --ulimit memlock=3072000:3072000 -d -it karim/centos-plex:v1
	402f54fc78510401f1434212f2c394bfd38b80dffe4a508cd9c8a00761e1b9e1
	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:21:11]
	└─[0] <> docker ps
	CONTAINER ID        IMAGE                  COMMAND              CREATED             STATUS              PORTS               NAMES
	402f54fc7851        karim/centos-plex:v1   "/usr/bin/plex.sh"   6 seconds ago       Up 5 seconds                            loving_panini
	┌─[elatov@m2] - [/home/elatov/docker] - [2016-01-04 08:21:16]
	└─[0] <> docker exec loving_panini ps -ef
	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 03:21 ?        00:00:00 /bin/bash /usr/bin/plex.sh
	root         6     1  0 03:21 ?        00:00:00 su -s /bin/sh plex -c . /etc/sysconfig/PlexMediaServer; cd /usr/lib/plexmediaserver; ./Plex\ Media\ Server
	plex         7     6  0 03:21 ?        00:00:00 sh -c . /etc/sysconfig/PlexMediaServer; cd /usr/lib/plexmediaserver; ./Plex\ Media\ Server
	plex        11     7 28 03:21 ?        00:00:05 ./Plex Media Server
	root       430     0  0 03:21 ?        00:00:00 ps -ef

When working with **DockerFiles** it's important to know the difference between **CMD** and **ENTRYPOINT** directives. Here are some good links that talk about that:

* [Best practices for writing Dockerfiles](https://docs.docker.com/engine/articles/dockerfile_best-practices/#entrypoint)
* [Dockerfile: ENTRYPOINT vs CMD](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)

I ended up using **ENTRYPOINT** but I could've used **CMD** in my case as well. I will admit this is not the best way to run plex in a *container*, but there are great examples that cover appropriate use cases:

* [Plex server on a VPS Docker setup without port forwarding](http://blog.vpetkov.net/2015/12/17/plex-server-on-a-vps-docker-setup-without-port-forwarding/)
* [docker-plex](https://github.com/timhaak/docker-plex/blob/master/Dockerfile)
* [wernight/plex-media-server](https://hub.docker.com/r/wernight/plex-media-server/~/dockerfile/)
