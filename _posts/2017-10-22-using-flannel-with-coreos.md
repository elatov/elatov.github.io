---
published: true
layout: post
title: "Using Flannel with CoreOS"
author: Karim Elatov
categories: [containers,networking]
tags: [docker,docker-compose,coreos,flannel]
---
### CoreOS Update
I recently updated from **1298.7.0** to **1353.6.0** and for some reason some of the **bridge** interfaces for my containers wouldn't start up. I just saw the following interfaces:

	core ~ # ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	2: enp1s0f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
	    inet 192.168.0.106/24 brd 192.168.0.255 scope global enp1s0f0
	       valid_lft forever preferred_lft forever
	5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default
	    inet 10.2.37.0/16 scope global flannel.1
	       valid_lft forever preferred_lft forever
	6: br-4a79a183632a: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
	    inet 172.25.0.1/16 scope global br-4a79a183632a
	       valid_lft forever preferred_lft forever
	7: br-868395bd74c5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
	    inet 172.19.0.1/16 scope global br-868395bd74c5
	       valid_lft forever preferred_lft forever
	8: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
	    inet 172.17.0.1/16 scope global docker0
	       valid_lft forever preferred_lft forever
	9: br-44c028eed818: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
	    inet 172.18.0.1/16 scope global br-44c028eed818

But before the update I had a lot more. Some interfaces just failed to come up.

### Dedicated Bridges with Docker Compose
As I kept looking at the setup, I realized that for each container deployment that I did with a **docker-compose**, there was a dedicated **bridge** and **docker network** created:

	core ~ # docker network ls
	NETWORK ID          NAME                 DRIVER              SCOPE
	749f7512f466        bridge               bridge              local
	a60a4439c7b3        elk_default          bridge              local
	aac3a00b7c01        host                 host                local
	6df70ed8f399        mariadb_default      bridge              local
	b2c32fd3ea00        none                 null                local
	8ba94d526efb        shipyard_default     bridge              local
	44c028eed818        splunk_default       bridge              local
	868395bd74c5        watchtower_default   bridge              local
	f6a4ffcb974a        zabbix_default       bridge              local

This is actually known behavior and is described in [Compose network configuration not following docker0 network setup](https://github.com/docker/compose/issues/3899). You can specify the following in the **docker-compose.yml** config:

	network_mode: bridge

and it will connect to the **docker0** bridge if you like.

### Flannel with Docker
Since I was already using CoreOS I knew that **flannel** comes pre-installed with it. **Flannel** is an overlay network that allows containers to talk to each other across multiple Docker Hosts. There is actually a nice diagram from [their](https://github.com/coreos/flannel) documentation:

![flannel-packet-flow](https://raw.githubusercontent.com/elatov/upload/master/flannel-coreos/flannel-packet-flow.png)

What I liked about **flannel** is that it sits in front of docker and the containers don't really need to know that they are using an overlay network. You can just configure the containers to use the **docker0** (bridge network) interface and it will work without issues. If you are not using CoreOS the **flannel** setup is covered in the following sites:

1. [Multi-Host Networking Overlay with Flannel](http://docker-k8s-lab.readthedocs.io/en/latest/docker/docker-flannel.html)
2. [Docker overlay network using Flannel](http://blog.shippable.com/docker-overlay-network-using-flannel)
3. [Howto Configure flannel Overlay Network with VXLAN for Docker on Power Servers](http://cloudgeekz.com/1016/configure-flannel-docker-power.html)

The jist of the setup is, first add the **flannel** network into **etcd2**:

	$ etcdctl set /coreos.com/network/config '{"Network": "10.0.0.0/8", "SubnetLen": 20, "SubnetMin": "10.10.0.0","SubnetMax": "10.99.0.0","Backend": {"Type": "vxlan","VNI": 100,"Port": 8472}}'

Then confirm it's set:

	$ etcdctl get /coreos.com/network/config

Then start **flanneld** and specify your external/public IP:

	$ nohup sudo flanneld --iface=192.168.205.10 &

That will create a **flannel.#** interface on the network that you specified. Then start the **docker** daemon and make sure it's on the **flannel** subnet that you defined initially:

	$ sudo service docker stop
	$ source /run/flannel/subnet.env
	$ sudo ifconfig docker0 ${FLANNEL_SUBNET}
	$ sudo docker daemon --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU} &

And then you can just start a container and it will be on the **flannel** network:

	$ sudo docker run -d --name test1  busybox sh -c "while true; do sleep 3600; done"

#### Flannel with CoreOS
With CoreOS all we have to do is configure the **cloud-config.yml** file and apply the configuration. Here is the relevant config for **flannel** (this is covered in [Configuring flannel for container networking](https://coreos.com/flannel/docs/latest/flannel-config.html)):

	flannel:
	    interface: 192.168.0.106
	etcd2:
	    name: "core"
	    #discovery: "https://discovery.etcd.io/<token>"
	    advertise-client-urls: "http://192.168.0.106:2379"
	    initial-advertise-peer-urls: "http://192.168.0.106:2380"
	    listen-client-urls: "http://0.0.0.0:2379,http://0.0.0.0:4001"
	    listen-peer-urls: "http://192.168.0.106:2380,http://192.168.0.106:7001"
	- name: etcd2.service
	      command: start
	      drop-ins:
	        - name: 50-network-config.conf
	          content: |
	            [Service]
	            Restart=always

	            [Install]
	            WantedBy=multi-user.target
	- name: docker.service
	      command: start
	      drop-ins:
	        - name: 50-insecure-registry.conf
	          content: |
	            [Unit]
	            [Service]
	            Environment=DOCKER_OPTS='--insecure-registry="0.0.0.0/0"'

	        - name: 60-docker-wait-for-flannel-config.conf
	          content: |
	            [Unit]
	            After=flanneld.service
	            Requires=flanneld.service

	            [Service]
	            Restart=always

	            [Install]
	            WantedBy=multi-user.target
	- name: flanneld.service
	      command: start
	      drop-ins:
	      - name: 50-network-config.conf
	        content: |
	          [Unit]
	           After=etcd2.service
	           Requires=etcd2.service

	          [Service]
	          ExecStartPre=/usr/bin/etcdctl set /coreos.com/network/config '{"Network":"10.2.0.0/16", "Backend": {"Type": "vxlan"}}'

	          [Install]
	           WantedBy=multi-user.target

Then to apply it we can just run this:

	$ coreos-cloudinit -validate --from-file cloud-config.yaml
	$ coreos-cloudinit --from-file cloud-config.yaml

And if you want it to persist a reboot, you can copy into the install location:

	$ cp cloud-config.yaml /var/lib/coreos-install/user_data

After that's done, you will see the **flanneld** daemon running:

	core ~ # systemctl status flanneld -l --no-pager
	● flanneld.service - flannel - Network fabric for containers (System Application Container)
	   Loaded: loaded (/usr/lib/systemd/system/flanneld.service; disabled; vendor preset: disabled)
	  Drop-In: /etc/systemd/system/flanneld.service.d
	           └─50-network-config.conf
	   Active: active (running) since Wed 2017-04-26 11:07:33 MDT; 5h 1min ago
	     Docs: https://github.com/coreos/flannel
	  Process: 4683 ExecStop=/usr/bin/rkt stop --uuid-file=/var/lib/coreos/flannel-wrapper.uuid (code=exited, status=0/SUCCESS)
	  Process: 4765 ExecStartPre=/usr/bin/etcdctl set /coreos.com/network/config {"Network":"10.2.0.0/16", "Backend": {"Type": "vxlan"}} (code=exited, status=0/SUCCESS)
	  Process: 4734 ExecStartPre=/usr/bin/rkt rm --uuid-file=/var/lib/coreos/flannel-wrapper.uuid (code=exited, status=0/SUCCESS)
	  Process: 4731 ExecStartPre=/usr/bin/mkdir --parents /var/lib/coreos /run/flannel (code=exited, status=0/SUCCESS)
	  Process: 4725 ExecStartPre=/sbin/modprobe ip_tables (code=exited, status=0/SUCCESS)
	 Main PID: 4775 (flanneld)
	    Tasks: 15 (limit: 32768)
	   Memory: 10.0M
	      CPU: 3.959s
	   CGroup: /system.slice/flanneld.service
	           └─4775 /opt/bin/flanneld --ip-masq=true

	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.300976    4775 manager.go:149] Using interface with name enp1s0f0 and address 192.168.0.106
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.300993    4775 manager.go:166] Defaulting external address to interface address (192.168.0.106)
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.313707    4775 local_manager.go:134] Found lease (10.2.37.0/24) for current IP (192.168.0.106), reusing
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.319892    4775 ipmasq.go:47] Adding iptables rule: -s 10.2.0.0/16 -d 10.2.0.0/16 -j RETURN
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.321837    4775 ipmasq.go:47] Adding iptables rule: -s 10.2.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.323857    4775 ipmasq.go:47] Adding iptables rule: ! -s 10.2.0.0/16 -d 10.2.0.0/16 -j MASQUERADE
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.325706    4775 manager.go:250] Lease acquired: 10.2.37.0/24
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.325946    4775 network.go:58] Watching for L3 misses
	Apr 26 11:07:33 core flannel-wrapper[4775]: I0426 17:07:33.325981    4775 network.go:66] Watching for new subnet leases
	Apr 26 11:07:33 core systemd[1]: Started flannel - Network fabric for containers (System Application Container).

And the docker daemon will also start up on the new **flannel** network:

	core ~ # systemctl status docker -l --no-pager                                                                               ● docker.service - Docker Application Container Engine
	   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
	  Drop-In: /etc/systemd/system/docker.service.d
	           └─50-insecure-registry.conf, 60-docker-wait-for-flannel-config.conf
	   Active: active (running) since Wed 2017-04-26 11:07:36 MDT; 5h 2min ago
	     Docs: http://docs.docker.com
	 Main PID: 4892 (dockerd)
	    Tasks: 107
	   Memory: 60.6M
	      CPU: 14.329s
	   CGroup: /system.slice/docker.service
	           ├─ 4892 dockerd --host=fd:// --containerd=/var/run/docker/libcontainerd/docker-containerd.sock --insecure-registry=0.0.0.0/0 --bip=10.2.37.1/24 --mtu=1450 --ip-masq=false --selinux-enabled
	           ├─ 5022 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 3306 -container-ip 10.2.37.9 -container-port
	3306

	Apr 26 11:07:36 core dockerd[4892]: time="2017-04-26T11:07:36.101420161-06:00" level=info msg="Loading containers: done."
	Apr 26 11:07:36 core dockerd[4892]: time="2017-04-26T11:07:36.101509944-06:00" level=info msg="Daemon has completed initializ
	ation"
	Apr 26 11:07:36 core dockerd[4892]: time="2017-04-26T11:07:36.101537005-06:00" level=info msg="Docker daemon" commit=d5236f0
	graphdriver=overlay version=1.12.6
	Apr 26 11:07:36 core dockerd[4892]: time="2017-04-26T11:07:36.117838732-06:00" level=info msg="API listen on /var/run/docker.
	sock"
	Apr 26 11:07:36 core systemd[1]: Started Docker Application Container Engine.

And you will see the configuration pushed to **etcd2**:

	core ~ # etcdctl get /coreos.com/network/config
	{"Network":"10.2.0.0/16", "Backend": {"Type": "vxlan"}}

And the config was created for **docker** to read:

	core ~ # cat /run/flannel/subnet.env
	FLANNEL_NETWORK=10.2.0.0/16
	FLANNEL_SUBNET=10.2.37.1/24
	FLANNEL_MTU=1450
	FLANNEL_IPMASQ=true
	core ~ # cat /run/flannel/flannel_docker_opts.env
	DOCKER_OPT_BIP="--bip=10.2.37.1/24"
	DOCKER_OPT_IPMASQ="--ip-masq=false"
	DOCKER_OPT_MTU="--mtu=1450"

### Testing out the Flannel Network
Now I can start up a container and make sure I can reach another container on the same bridge:

	core ~ # docker run --rm -it alpine /bin/sh
	/ # ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	59: eth0@if60: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1450 qdisc noqueue state UP
	    inet 10.2.37.13/24 scope global eth0
	       valid_lft forever preferred_lft forever
	/ # ping -c 1 10.2.37.5
	PING 10.2.37.5 (10.2.37.5): 56 data bytes
	64 bytes from 10.2.37.5: seq=0 ttl=64 time=0.125 ms

	--- 10.2.37.5 ping statistics ---
	1 packets transmitted, 1 packets received, 0% packet loss
	round-trip min/avg/max = 0.125/0.125/0.125 ms

And now I just have one **bridge** with mulitple containers connected to it:

	# core ~ # brctl show
	bridge name     bridge id               STP enabled     interfaces
	docker0         8000.024238119fbf       no              veth0f54902
	                                                        veth103c116
	                                                        veth42c1fba
	                                                        veth560dee2
	                                                        veth6943b27
	                                                        veth6f481f3
	                                                        veth7472f10
	                                                        veth7c445fb
	                                                        vethb428e5d
	                                                        vethf78b563
	                                                        vethfb91608

One thing to note is that all the requests will come in from the **docker0** interface or the default gateway. You can do another quick test to confirm:

	core ~ # docker run --rm -it -e 12345 -p 12345:12345 alpine /bin/sh
	/ # apk update
	fetch http://dl-cdn.alpinelinux.org/alpine/v3.5/main/x86_64/APKINDEX.tar.gz
	fetch http://dl-cdn.alpinelinux.org/alpine/v3.5/community/x86_64/APKINDEX.tar.gz
	v3.5.2-55-g4a95ad60e8 [http://dl-cdn.alpinelinux.org/alpine/v3.5/main]
	v3.5.2-49-g2cff35f5fc [http://dl-cdn.alpinelinux.org/alpine/v3.5/community]
	OK: 7964 distinct packages available
	/ # apk add tcpdump
	(1/2) Installing libpcap (1.7.4-r1)
	(2/2) Installing tcpdump (4.9.0-r0)
	Executing busybox-1.25.1-r0.trigger
	OK: 5 MiB in 13 packages
	/ # tcpdump -i eth0 tcp port 12345 -nne
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
	22:31:56.539387 02:42:38:11:9f:bf > 02:42:0a:02:25:0d, ethertype IPv4 (0x0800), length 74: 10.2.37.1.54980 > 10.2.37.13.12345: Flags [S], seq 3436635296, win 29200, options [mss 1460,sackOK,TS val 7733117 ecr 0,nop,wscale 7], length 0
	22:31:56.539425 02:42:0a:02:25:0d > 02:42:38:11:9f:bf, ethertype IPv4 (0x0800), length 54: 10.2.37.13.12345 > 10.2.37.1.54980: Flags [R.], seq 0, ack 3436635297, win 0, length 0

So if any converted containers were using the old bridge IPs they will have to be updated.

### Converting docker-compose.yml to use the network bridge

To do the conversion, I just stopped all the containers:

	# docker stop $(docker ps -a -q)

Then deleted the old networks:

	# docker network rm elk_default mariadb_default shipyard_default splunk_default

Then added the following line to all the **docker-compose.yml** files:

	network_mode: bridge

and lastly started them up:

	# docker-compose up -d

### Iptables Configuration
You will notice that for each port your **expose** an **iptables** rule is added to allow that port to reach the host (in the **DOCKER** chain):

	core ~ # iptables -L -n -v
	Chain INPUT (policy ACCEPT 1185 packets, 207K bytes)
	 pkts bytes target     prot opt in     out     source               destination

	Chain FORWARD (policy ACCEPT 189 packets, 32822 bytes)
	 pkts bytes target     prot opt in     out     source               destination
	1154K  517M DOCKER-ISOLATION  all  --  *      *       0.0.0.0/0            0.0.0.0/0
	 740K  155M DOCKER     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0
	 151K   32M ACCEPT     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
	 414K  363M ACCEPT     all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0
	   46  2784 ACCEPT     all  --  docker0 docker0  0.0.0.0/0            0.0.0.0/0

	Chain OUTPUT (policy ACCEPT 974 packets, 448K bytes)
	 pkts bytes target     prot opt in     out     source               destination

	Chain DOCKER (1 references)
	 pkts bytes target     prot opt in     out     source               destination
	 395K   52M ACCEPT     tcp  --  !docker0 docker0  0.0.0.0/0            10.2.37.9            tcp dpt:3306
	    0     0 ACCEPT     tcp  --  !docker0 docker0  0.0.0.0/0            10.2.37.5            tcp dpt:9300
	Chain DOCKER-ISOLATION (1 references)
	 pkts bytes target     prot opt in     out     source               destination
	1154K  517M RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0

And since I was also specifying external **ports** in my configuration, I saw **DNAT**s (in the **PREROUTING/DOCKER** chain) and **MASQUERADE**s (in the **POSTROUTING** chain) added as well (to allow outbound and inbound traffic from the outside):

	core ~ # iptables -L -n -v -t nat
	Chain PREROUTING (policy ACCEPT 96 packets, 11911 bytes)
	 pkts bytes target     prot opt in     out     source               destination
	23111 1457K DOCKER     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

	Chain INPUT (policy ACCEPT 94 packets, 11775 bytes)
	 pkts bytes target     prot opt in     out     source               destination

	Chain OUTPUT (policy ACCEPT 8 packets, 1496 bytes)
	 pkts bytes target     prot opt in     out     source               destination
	    2   120 DOCKER     all  --  *      *       0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

	Chain POSTROUTING (policy ACCEPT 8 packets, 1496 bytes)
	 pkts bytes target     prot opt in     out     source               destination
	  492  103K RETURN     all  --  *      *       10.2.0.0/16          10.2.0.0/16
	  311 19896 MASQUERADE  all  --  *      *       10.2.0.0/16         !224.0.0.0/4
	23095 1456K MASQUERADE  all  --  *      *      !10.2.0.0/16          10.2.0.0/16
	    0     0 MASQUERADE  tcp  --  *      *       10.2.37.9            10.2.37.9            tcp dpt:3306
	    0     0 MASQUERADE  tcp  --  *      *       10.2.37.5            10.2.37.5            tcp dpt:9300
	Chain DOCKER (2 references)
	 pkts bytes target     prot opt in     out     source               destination
	 4623  277K DNAT       tcp  --  !docker0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:3306 to:10.2.37.9:3306
	    0     0 DNAT       tcp  --  !docker0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:9300 to:10.2.37.5:9300

### CoreOS issue with docker network bridges

Later on as I was doing some research I ran into [this](https://github.com/coreos/bugs/issues/1936) CoreOS issue. And it looks like with the new CoreOS version (**1353.6.0**) there was a race condition with interface claiming between **docker** and the **systemd** network service. And the following modification:

	[Match]
	 Type=bridge
	-Name=docker*
	+Name=docker* br-*

In the the **50-docker.network** file, would've probably fixed my original issue, but I was still happy to move my containers to **flannel** for future expansion. And it looks like version [1353.7.0](https://coreos.com/releases/#1353.7.0) fixes that specific issue as well.
