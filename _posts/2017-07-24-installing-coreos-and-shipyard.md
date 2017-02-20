---
published: false
layout: post
title: "Installing CoreOS and Shipyard"
author: Karim Elatov
categories: [containers]
tags: [docker,shipyard,etcd2,coreos]
---
I wanted to try out CoreOS, an OS that is optimized for Docker Containers.

### Installing to disk
Most of the setup is covered in [Installing CoreOS Container Linux to disk](https://coreos.com/os/docs/latest/installing-to-disk.html). Just download the ISO and then **dd** it to a USB stick:

	$ sudo dd if=coreos_production_iso_image.iso of=/dev/sdc bs=1M status=progress

After the machine boots, it automatically logs in as the core user. I set the user's password with the following command:

	$ sudo passwd core

Since the machine was able to get a DHCP addres, then I just ssh'ed into the machine:

    <> ssh core@192.168.1.230
    The authenticity of host '192.168.1.230 (192.168.1.230)' can't be established.
    ECDSA key fingerprint is SHA256:pAGQAOrtD66i/R4WlnTjja7d4k3QECGiMXHHWpynLH8.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '192.168.1.230' (ECDSA) to the list of known hosts.
    Password:
    Last login: Sun Jan 15 22:46:52 UTC 2017 on tty1
    Container Linux by CoreOS stable (1235.6.0)
    Update Strategy: No Reboots
    Failed Units: 1
      tcsd.service
    core@localhost ~ $

And did the rest from there. First find your disk (mine was **/dev/nvme0n1**):

    $ sudo fdisk -l
    Disk /dev/loop0: 233.4 MiB, 244736000 bytes, 478000 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes


    Disk /dev/nvme0n1: 477 GiB, 512110190592 bytes, 1000215216 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x48d52bce

    Device         Boot   Start     End Sectors  Size Id Type
    /dev/nvme0n1p1 *       2048 1050623 1048576  512M  b W95 FAT32
    /dev/nvme0n1p2      1050624 2099199 1048576  512M  b W95 FAT32
    /dev/nvme0n1p3      2099200 3147775 1048576  512M  b W95 FAT32

Then you have to create a **cloud-config.yaml** file to do your install. Here is the cloud config I ended up creating

    localhost ~ # cat ~core/cloud-config.yaml
    #cloud-config
    hostname: core
    coreos:
      update:
        reboot-strategy: etcd-lock
      etcd2:
        name: core
        initial-advertise-peer-urls: http://127.0.0.1:2380
        initial-cluster-token: core_etcd
        initial-cluster: core=http://127.0.0.1:2380
        initial-cluster-state: new
        listen-peer-urls: http://0.0.0.0:2380,http://0.0.0.0:7001
        listen-client-urls: http://0.0.0.0:2379,http://0.0.0.0:4001
        advertise-client-urls:  http://0.0.0.0:2379,http://0.0.0.0:4001
      units:
        - name: etcd2.service
          command: start
        - name: fleet.service
          command: start
        - name: docker-tcp.socket
          command: start
          enable: true
          content: |
            [Unit]
            Description=Docker Socket for the API

            [Socket]
            ListenStream=2375
            BindIPv6Only=both
            Service=docker.service

            [Install]
            WantedBy=sockets.target
        - name: docker.service
          command: start
          drop-ins:
            - name: 50-insecure-registry.conf
              content: |
                [Unit]
                [Service]
                Environment=DOCKER_OPTS='--insecure-registry="0.0.0.0/0"'
        - name: flanneld.service
          command: start
          drop-ins:
          - name: 50-network-config.conf
            content: |
              [Service]
              ExecStartPre=/usr/bin/etcdctl set /coreos.com/network/config '{"Network":"10.2.0.0/16", "Backend": {"Type": "vxlan"}}'
        - name: 00-eno1.network
          runtime: true
          content: |
            [Match]
            Name=eno1

            [Network]
            DNS=192.168.1.1
            DNS=192.168.56.1
            Address=192.168.1.106/24
            Gateway=192.168.1.1
            LinkLocalAddressing=no
            IPv6AcceptRA=no
    write-files:
     - path: /etc/conf.d/nfs
       permissions: '0644'
       content: |
         OPTS_RPC_MOUNTD=""

    users:
      - name: "elatov"
        passwd: "$6$pO1"
        groups:
          - "sudo"
          - "docker"
        ssh-authorized-keys:
          - "ssh-rsa TFnaJYPYKp elatov@me"

    ssh_authorized_keys:
      - ssh-rsa TFnaJYPYKp elatov@me

I had some help from these web sites:

- [Network configuration with networkd](https://coreos.com/os/docs/latest/network-config-with-networkd.html)
- [Using Cloud-Config](https://coreos.com/os/docs/latest/cloud-config.html)


And now for the install:

    localhost ~ # coreos-install -d /dev/nvme0n1 -C stable -c ~core/cloud-config.yaml
    2017/01/15 23:38:32 Checking availability of "local-file"
    2017/01/15 23:38:32 Fetching user-data from datasource of type "local-file"
    Downloading the signature for https://stable.release.core-os.net/amd64-usr/1235.6.0/coreos_production_image.bin.bz2...
    2017-01-15 23:38:33 URL:https://stable.release.core-os.net/amd64-usr/1235.6.0/coreos_production_image.bin.bz2.sig [564/564] -> "/tmp/coreos-install.QCfpdhiZq4/coreos_production_image.bin.bz2.sig" [1]
    Downloading, writing and verifying coreos_production_image.bin.bz2...
    2017-01-15 23:39:05 URL:https://stable.release.core-os.net/amd64-usr/1235.6.0/coreos_production_image.bin.bz2 [276173809/276173809] -> "-" [1]
    gpg: Signature made Tue Jan 10 05:48:31 2017 UTC
    gpg:                using RSA key 48F9B96A2E16137F
    gpg:                issuer "buildbot@coreos.com"
    gpg: key 50E0885593D2DCB4 marked as ultimately trusted
    gpg: checking the trustdb
    gpg: marginals needed: 3  completes needed: 1  trust model: pgp
    gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
    gpg: Good signature from "CoreOS Buildbot (Offical Builds) <buildbot@coreos.com>" [ultimate]
    Installing cloud-config...
    Success! CoreOS stable 1235.6.0 is installed on /dev/nvme0n1

### Installing Shipyard
I then wanted to install Shipyard which can help with managing Docker Containers. Looking over the [Automated Deployment](https://shipyard-project.com/docs/deploy/automated/), it should be as easy as this:

	curl -sSL https://shipyard-project.com/deploy | bash -s

But running that yieled the followed error:

> Error starting userland proxy: listen tcp 0.0.0.0:7001: bind: address already in use.

Then following the instructions laid out in [Install on coreos issues (solved) #755](https://github.com/shipyard/shipyard/issues/755)

Doing it manually worked:

	core ~ # docker run -ti -d --restart=always --name shipyard-swarm-manager swarm:latest manage --host tcp://0.0.0.0:3375 etcd://172.17.0.1:4001
	cfc33357c008d94841e4470b580706203d6d54f6d7c8b3462370f18134587024

To make sure it's able to connect to etc2, find it's id and check out the logs:

	core ~ # docker ps
	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                            NAMES
	cfc33357c008        swarm:latest        "/swarm manage --host"   4 seconds ago       Up 3 seconds        2375/tcp                         shipyard-swarm-manager
	ca24bde9016b        rethinkdb           "rethinkdb --bind all"   38 minutes ago      Up 38 minutes       8080/tcp, 28015/tcp, 29015/tcp   shipyard-rethinkdb

Then check out the logs:

	core ~ # docker logs cfc33357c008
	INFO[0000] Initializing discovery without TLS
	INFO[0000] Listening for HTTP                            addr=0.0.0.0:3375 proto=tcp

I figure out that I should use the IP that the docker0 interface is listening on:

	macm ~ # ip -4 a s dev docker0
	5: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
	    inet 172.17.0.1/16 scope global docker0
	       valid_lft forever preferred_lft forever

Also you can login to one of the containers and make sure you can reach those end points:

	macm ~ # docker exec -it ca24bde9016b /bin/sh
	# curl -L http://172.17.0.1:2375
	{"message":"page not found"}
	# curl -L http://172.17.0.1:4001/v2/keys
	{"action":"get","node":{"dir":true,"nodes":[{"key":"/coreos.com","dir":true,"modifiedIndex":4,"createdIndex":4},{"key":"/docker","dir":true,"modifiedIndex":1409,"createdIndex":1409}]}}

I had to change my **cloud-config.yaml** file and update it to change the config for etcd2 (more on that below). So keep going and deploy the rest of the containers:

	core ~ # docker run \
	>     -ti \
	>     -d \
	>     --restart=always \
	>     --name shipyard-swarm-agent \
	>     swarm:latest \
	>     join --addr 172.17.0.1:2375 etcd://172.17.0.1:2379
	556eac9be28fbe5a5a41d13694c86a56fce65b5cb00e34056c4b4ae606ce5d49

Do the same thing and confirm the logs look good:

	core ~ # docker logs 556eac9be28f
	INFO[0000] Initializing discovery without TLS
	INFO[0000] Registering on the discovery service every 1m0s...  addr=172.17.0.1:2375 discovery=etcd://172.17.0.1:2379

And finally run the controller:

	core ~ # docker run \
	>     -ti \
	>     -d \
	>     --restart=always \
	>     --name shipyard-controller \
	>     --link shipyard-rethinkdb:rethinkdb \
	>     --link shipyard-swarm-manager:swarm \
	>     -p 8080:8080 \
	>     shipyard/shipyard:latest \
	>     server \
	>     -d tcp://swarm:3375
	73252834a961c267e8e54492086f1e2a2df235548b67543730f1f63b127f5263

Now you can go to **http://IP:8080** and login with **admin/shipyard**

### Change the Cloud-Config And Update it

First copy the config that was used during the install:

	core ~ # cp /var/lib/coreos-install/user_data /tmp/cc.yml

Then modify what you need:

	core ~ # vi /tmp/cc.yml

Then apply the confirm the config is okay:

	core ~ # coreos-cloudinit -validate --from-file /tmp/cc.yml
	2017/01/16 00:46:05 Checking availability of "local-file"
	2017/01/16 00:46:05 Fetching user-data from datasource of type "local-file"

And lastly go ahead and apply the config:

	core ~ # coreos-cloudinit --from-file /tmp/cc.yml
	2017/01/16 00:46:28 Checking availability of "local-file"
	2017/01/16 00:46:28 Fetching user-data from datasource of type "local-file"
	2017/01/16 00:46:28 Fetching meta-data from datasource of type "local-file"
	2017/01/16 00:46:28 Parsing user-data as cloud-config
	2017/01/16 00:46:28 Merging cloud-config from meta-data and user-data
	2017/01/16 00:46:28 Set hostname to core
	2017/01/16 00:46:28 User 'elatov' exists, ignoring creation-time fields
	2017/01/16 00:46:28 Setting 'elatov' user's password
	2017/01/16 00:46:28 Authorizing 2 SSH keys for user 'elatov'
	2017/01/16 00:46:28 Authorized SSH keys for core user
	2017/01/16 00:46:28 Writing file to "/etc/conf.d/nfs"
	2017/01/16 00:46:28 Wrote file to "/etc/conf.d/nfs"
	2017/01/16 00:46:28 Wrote file /etc/conf.d/nfs to filesystem
	2017/01/16 00:46:28 Writing file to "/etc/coreos/update.conf"
	2017/01/16 00:46:28 Wrote file to "/etc/coreos/update.conf"
	2017/01/16 00:46:28 Wrote file /etc/coreos/update.conf to filesystem
	2017/01/16 00:46:28 Writing unit "docker-tcp.socket" to filesystem
	2017/01/16 00:46:28 Writing file to "/etc/systemd/system/docker-tcp.socket"
	2017/01/16 00:46:28 Wrote file to "/etc/systemd/system/docker-tcp.socket"
	2017/01/16 00:46:28 Wrote unit "docker-tcp.socket"
	2017/01/16 00:46:28 Enabling unit file "docker-tcp.socket"
	2017/01/16 00:46:28 Enabled unit "docker-tcp.socket"
	2017/01/16 00:46:28 Writing drop-in unit "50-insecure-registry.conf" to filesystem
	2017/01/16 00:46:28 Writing file to "/etc/systemd/system/docker.service.d/50-insecure-registry.conf"
	2017/01/16 00:46:28 Wrote file to "/etc/systemd/system/docker.service.d/50-insecure-registry.conf"
	2017/01/16 00:46:28 Wrote drop-in unit "50-insecure-registry.conf"
	2017/01/16 00:46:28 Writing drop-in unit "50-network-config.conf" to filesystem
	2017/01/16 00:46:28 Writing file to "/etc/systemd/system/flanneld.service.d/50-network-config.conf"
	2017/01/16 00:46:28 Wrote file to "/etc/systemd/system/flanneld.service.d/50-network-config.conf"
	2017/01/16 00:46:28 Wrote drop-in unit "50-network-config.conf"
	2017/01/16 00:46:28 Writing unit "00-eno1.network" to filesystem
	2017/01/16 00:46:28 Writing file to "/run/systemd/network/00-eno1.network"
	2017/01/16 00:46:28 Wrote file to "/run/systemd/network/00-eno1.network"
	2017/01/16 00:46:28 Wrote unit "00-eno1.network"
	2017/01/16 00:46:28 Ensuring runtime unit file "00-eno1.network" is unmasked
	2017/01/16 00:46:28 /run/systemd/network/00-eno1.network is not null or empty, refusing to unmask
	2017/01/16 00:46:28 Ensuring runtime unit file "etcd.service" is unmasked
	2017/01/16 00:46:28 Ensuring runtime unit file "etcd2.service" is unmasked
	2017/01/16 00:46:28 Ensuring runtime unit file "fleet.service" is unmasked
	2017/01/16 00:46:28 Ensuring runtime unit file "locksmithd.service" is unmasked
	2017/01/16 00:46:28 Ensuring runtime unit file "locksmithd.service" is unmasked
	2017/01/16 00:46:28 Restarting systemd-networkd
	2017/01/16 00:46:29 Restarted systemd-networkd (done)
	2017/01/16 00:46:29 Calling unit command "start" on "docker-tcp.socket"'
	2017/01/16 00:46:29 Result of "start" on "docker-tcp.socket": done
	2017/01/16 00:46:29 Calling unit command "start" on "docker.service"'
	2017/01/16 00:46:29 Result of "start" on "docker.service": done
	2017/01/16 00:46:29 Calling unit command "start" on "flanneld.service"'
	2017/01/16 00:46:29 Result of "start" on "flanneld.service": done
	2017/01/16 00:46:29 Calling unit command "restart" on "locksmithd.service"'
	2017/01/16 00:46:29 Result of "restart" on "locksmithd.service": done


After that make sure the services are listening on the right IPs:

	macm ~ # ss -lnt
	State      Recv-Q Send-Q                       Local Address:Port                                      Peer Address:Port
	LISTEN     0      128                             172.17.0.1:2380                                                 *:*
	LISTEN     0      128                             172.17.0.1:7001                                                 *:*
	LISTEN     0      128                                     :::2375                                                :::*
	LISTEN     0      128                                     :::2379                                                :::*
	LISTEN     0      128                                     :::8080                                                :::*
	LISTEN     0      128                                     :::22                                                  :::*
	LISTEN     0      128                                     :::4001                                                :::*

Here are the config locations: [Cloud-Config Locations](https://coreos.com/os/docs/latest/cloud-config-locations.html). Since I was making changes to the **etc2** service, I could confirm it's running:

	macm ~ # systemctl status etcd2
	● etcd2.service - etcd2
	   Loaded: loaded (/usr/lib/systemd/system/etcd2.service; enabled; vendor preset: disabled)
	  Drop-In: /run/systemd/system/etcd2.service.d
	           └─20-cloudinit.conf
	   Active: active (running) since Mon 2017-02-20 06:02:06 UTC; 24min ago
	 Main PID: 2997 (etcd2)
	    Tasks: 14
	   Memory: 18.4M
	      CPU: 5.639s
	   CGroup: /system.slice/etcd2.service
	           └─2997 /usr/bin/etcd2

	Feb 20 06:02:06 macm etcd2[2997]: added member ce2a822cea30bfca [http://localhost:2380 http://localhost:7001] to cluster 7e27652122e8b2ae from
	Feb 20 06:02:06 macm etcd2[2997]: set the cluster version to 2.3 from store
	Feb 20 06:02:06 macm etcd2[2997]: starting server... [version: 2.3.7, cluster version: 2.3]
	Feb 20 06:02:06 macm systemd[1]: Started etcd2.
	Feb 20 06:02:07 macm etcd2[2997]: ce2a822cea30bfca is starting a new election at term 10
	Feb 20 06:02:07 macm etcd2[2997]: ce2a822cea30bfca became candidate at term 11
	Feb 20 06:02:07 macm etcd2[2997]: ce2a822cea30bfca received vote from ce2a822cea30bfca at term 11
	Feb 20 06:02:07 macm etcd2[2997]: ce2a822cea30bfca became leader at term 11
	Feb 20 06:02:07 macm etcd2[2997]: raft.node: ce2a822cea30bfca elected leader ce2a822cea30bfca at term 11
	Feb 20 06:02:07 macm etcd2[2997]: published {Name:0e7ed956df4d4f599f5038340d14867a ClientURLs:[http://192.168.1.109:2379]} to cluster 7e276521

and also check the new service config:

	macm ~ # cat /run/systemd/system/etcd2.service.d/20-cloudinit.conf
	[Service]
	Environment="ETCD_ADVERTISE_CLIENT_URLS=http://192.168.1.109:2379"
	Environment="ETCD_INITIAL_ADVERTISE_PEER_URLS=http://172.17.0.1:2380"
	Environment="ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379,http://0.0.0.0:4001"
	Environment="ETCD_LISTEN_PEER_URLS=http://172.17.0.1:2380,http://172.17.0.1:7001"



### Disable etcd2 Service on CoreOS
If you want you could also disable the **etcd2** service and just install **shipyard** the automated way which installs it's own **etcd** version. This is discussed at [etcd keeps getting started in place of etcd2 #3211](https://github.com/coreos/etcd/issues/3211). Here is relevant config to just unmask the service:

	# cat /var/lib/coreos-install/user_data
	#cloud-config
	hostname: core
	coreos:
	  update:
	    reboot-strategy: etcd-lock
	  units:
	    - name: etcd2.service
	      mask: true
	    - name: docker-tcp.socket
	      command: start

You can then stop all the containers and reboot, to apply the config:

	core ~ # docker stop $(docker ps -a -q)
	73252834a961
	556eac9be28f
	cfc33357c008
	ca24bde9016b
	core ~ # reboot