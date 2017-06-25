---
published: false
layout: post
title: "Manually Deploying OpenStack Ocata on Fedora 25"
author: Karim Elatov
categories: []
tags: []
---
### OpenStack
So I decided to try out OpenStack on Fedora 25. I was able to follow the [OpenStack Installation Tutorial for Red Hat Enterprise Linux and CentOS](https://docs.openstack.org/ocata/install-guide-rdo/). The guide is pretty long and I don't want to cover each step in great detail since it's covered in the guide. I also decided to follow the [Networking Option 2: Self-service networks](https://docs.openstack.org/ocata/install-guide-rdo/overview.html#networking-option-2-self-service-networks) setup. Here are the components that get deployed in that scenario:

![networking-option-2-os](networking-option-2-os.png)

And here is how the connectivity looks like (from [Self-service network](https://docs.openstack.org/ocata/install-guide-rdo/launch-instance-networks-selfservice.html)):

![selfservice-network-os-conn](selfservice-network-os-conn.png)

### OpenStack Controller Node
On the Controller node I ran the following commands:



https://docs.openstack.org/developer/devstack/guides/multinode-lab.html

After reading over these links for networking setup:

https://docs.openstack.org/developer/devstack/networking.html
https://docs.openstack.org/developer/devstack/guides/neutron.html#using-linux-bridge-instead-of-open-vswitch


https://stackoverflow.com/questions/36301100/how-do-i-turn-off-the-mysql-password-validation

On the computer node had to downgrade iptables due to a package dependency issue:

https://bugzilla.redhat.com/show_bug.cgi?id=1327786

 dnf install iptables-1.6.0-2.fc25 --allowerasing

Also had to disable selinux for the linuxbridge agent:

https://bugs.launchpad.net/neutron/+bug/1572322

# So after all the services are configured, you should have a hypervisor available:

[root@os-controller ~]# openstack hypervisor list
+----+---------------------+-----------------+---------------+-------+
| ID | Hypervisor Hostname | Hypervisor Type | Host IP       | State |
+----+---------------------+-----------------+---------------+-------+
|  1 | os-compute.kar.int  | QEMU            | 192.168.1.122 | up    |
+----+---------------------+-----------------+---------------+-------+

And you should have all your neutron components connected. I decided to try out the Self Service Network:

[root@os-controller ~]# openstack network agent list
+--------------------+--------------------+--------------------+-------------------+-------+-------+---------------------+
| ID                 | Agent Type         | Host               | Availability Zone | Alive | State | Binary              |
+--------------------+--------------------+--------------------+-------------------+-------+-------+---------------------+
| 66782d58-6586      | L3 agent           | os-                | nova              | True  | UP    | neutron-l3-agent    |
| -4d2c-b34f-        |                    | controller.kar.int |                   |       |       |                     |
| 5b20357c947d       |                    |                    |                   |       |       |                     |
| 8fef4034-409e-     | Metadata agent     | os-                | None              | True  | UP    | neutron-metadata-   |
| 475a-bd4c-         |                    | controller.kar.int |                   |       |       | agent               |
| 2aa661e2c09a       |                    |                    |                   |       |       |                     |
| a9a8b2e2-1be4      | Linux bridge agent | os-                | None              | True  | UP    | neutron-            |
| -434b-901b-        |                    | controller.kar.int |                   |       |       | linuxbridge-agent   |
| c09dd994423b       |                    |                    |                   |       |       |                     |
| a9e222ca-cdca-     | Linux bridge agent | os-compute.kar.int | None              | True  | UP    | neutron-            |
| 41cc-              |                    |                    |                   |       |       | linuxbridge-agent   |
| be23-d311dccca6f6  |                    |                    |                   |       |       |                     |
| ed9cc1cd-f256-45b8 | DHCP agent         | os-                | nova              | True  | UP    | neutron-dhcp-agent  |
| -b8a0-318e92001502 |                    | controller.kar.int |                   |       |       |                     |
+--------------------+--------------------+--------------------+-------------------+-------+-------+---------------------+

And you should have your compute service connected:

[root@os-controller ~]# openstack compute service list
+----+------------------+-----------------------+----------+---------+-------+----------------------------+
| ID | Binary           | Host                  | Zone     | Status  | State | Updated At                 |
+----+------------------+-----------------------+----------+---------+-------+----------------------------+
|  1 | nova-consoleauth | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:26.000000 |
|  2 | nova-scheduler   | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:26.000000 |
|  3 | nova-conductor   | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:27.000000 |
|  8 | nova-compute     | os-compute.kar.int    | nova     | enabled | up    | 2017-06-21T15:55:29.000000 |
+----+------------------+-----------------------+----------+---------+-------+----------------------------+

And throughout the guide you should have imported a test image into your glance image serevice:

[root@os-controller ~]# openstack image list
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| f71063a9-7865-4b10-9216-b213b44f5073 | cirros | active |
+--------------------------------------+--------+--------+

And you should have a bunch of endpoints used for various services:

[root@os-controller ~]# openstack endpoint list
+----------------------------+-----------+--------------+--------------+---------+-----------+----------------------------+
| ID                         | Region    | Service Name | Service Type | Enabled | Interface | URL                        |
+----------------------------+-----------+--------------+--------------+---------+-----------+----------------------------+
| 0b7053adf98b4a9eb6943f37c6 | RegionOne | glance       | image        | True    | public    | http://os-controller:9292  |
| ce2c73                     |           |              |              |         |           |                            |
| 1ad1ec0bedbd427b93c61e55d5 | RegionOne | keystone     | identity     | True    | internal  | http://os-                 |
| f36d55                     |           |              |              |         |           | controller:5000/v3/        |
| 235d8c15d7714a30a0a0e2f0ed | RegionOne | neutron      | network      | True    | admin     | http://os-controller:9696  |
| 36d29a                     |           |              |              |         |           |                            |
| 316be07b8ecb4e0b9d7237e300 | RegionOne | nova         | compute      | True    | public    | http://os-                 |
| 516856                     |           |              |              |         |           | controller:8774/v2.1       |
| 457e51e5db4a4eac98ab27329c | RegionOne | neutron      | network      | True    | internal  | http://os-controller:9696  |
| 0bf29a                     |           |              |              |         |           |                            |
| 4b4a1199711a468daaa2619f1c | RegionOne | nova         | compute      | True    | admin     | http://os-                 |
| 29305b                     |           |              |              |         |           | controller:8774/v2.1       |
| 8577f04d1aac4340a269ec2c02 | RegionOne | placement    | placement    | True    | admin     | http://os-controller:8778  |
| ca7da9                     |           |              |              |         |           |                            |
| 88a082dee97e4717b35b9a81ad | RegionOne | glance       | image        | True    | internal  | http://os-controller:9292  |
| 6e1fc4                     |           |              |              |         |           |                            |
| 90cbc44ea8ec4d658149ca0799 | RegionOne | glance       | image        | True    | admin     | http://controller:9292     |
| 02979f                     |           |              |              |         |           |                            |
| bed33872b765410a823d4ac719 | RegionOne | keystone     | identity     | True    | public    | http://os-                 |
| 3d8750                     |           |              |              |         |           | controller:5000/v3/        |
| c11f01cf078742b39c8653a281 | RegionOne | placement    | placement    | True    | public    | http://os-controller:8778  |
| 75df66                     |           |              |              |         |           |                            |
| c8d196b8a1be47c68e973a4475 | RegionOne | neutron      | network      | True    | public    | http://os-controller:9696  |
| 37ba86                     |           |              |              |         |           |                            |
| dfe64dca8de14f68ad6bf5717b | RegionOne | keystone     | identity     | True    | admin     | http://os-                 |
| 97e72b                     |           |              |              |         |           | controller:35357/v3/       |
| e7c5d75ecc4341cb8906023c58 | RegionOne | placement    | placement    | True    | internal  | http://os-controller:8778  |
| 36ef6c                     |           |              |              |         |           |                            |
| eb7b0daf02f1448da598c5f95d | RegionOne | glance       | image        | True    | admin     | http://os-controller:9292  |
| 61d94b                     |           |              |              |         |           |                            |
| ef2c27195ef24c919a986f184f | RegionOne | nova         | compute      | True    | internal  | http://os-                 |
| 0f0b45                     |           |              |              |         |           | controller:8774/v2.1       |
+----------------------------+-----------+--------------+--------------+---------+-----------+----------------------------+


So now let's create a provider network:

[root@os-controller ~]# openstack network create  --share --external \
>   --provider-physical-network provider \
>   --provider-network-type flat provider
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2017-06-21T15:47:14Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | addf3eeb-ef5d-4222-9cbe-ecd8e782702a |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | False                                |
| mtu                       | 1500                                 |
| name                      | provider                             |
| port_security_enabled     | True                                 |
| project_id                | 835735f545f04650b58c71a583242b35     |
| provider:network_type     | flat                                 |
| provider:physical_network | provider                             |
| provider:segmentation_id  | None                                 |
| qos_policy_id             | None                                 |
| revision_number           | 4                                    |
| router:external           | External                             |
| segments                  | None                                 |
| shared                    | True                                 |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| updated_at                | 2017-06-21T15:47:14Z                 |
+---------------------------+--------------------------------------+

Next create a subnet that will be on the provider network:

[root@os-controller ~]# openstack subnet create --network provider \
>   --allocation-pool start=10.0.0.100,end=10.0.0.120 \
>   --dns-nameserver 10.0.0.1 --gateway 10.0.0.1 \
>   --subnet-range 10.0.0.0/24 provider
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| allocation_pools  | 10.0.0.100-10.0.0.120                |
| cidr              | 10.0.0.0/24                          |
| created_at        | 2017-06-21T16:06:17Z                 |
| description       |                                      |
| dns_nameservers   | 10.0.0.1                             |
| enable_dhcp       | True                                 |
| gateway_ip        | 10.0.0.1                             |
| host_routes       |                                      |
| id                | 9fdb2fe2-79e6-4224-9395-fda93c0fe6d9 |
| ip_version        | 4                                    |
| ipv6_address_mode | None                                 |
| ipv6_ra_mode      | None                                 |
| name              | provider                             |
| network_id        | addf3eeb-ef5d-4222-9cbe-ecd8e782702a |
| project_id        | 835735f545f04650b58c71a583242b35     |
| revision_number   | 2                                    |
| segment_id        | None                                 |
| service_types     |                                      |
| subnetpool_id     | None                                 |
| updated_at        | 2017-06-21T16:06:17Z                 |
+-------------------+--------------------------------------+

Then create a subnet for the self service network:

[root@os-controller ~]#   openstack subnet create --network selfservice \
>   --dns-nameserver 10.0.0.1 --gateway 172.16.1.1 \
>   --subnet-range 172.16.1.0/24 selfservice
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| allocation_pools  | 172.16.1.2-172.16.1.254              |
| cidr              | 172.16.1.0/24                        |
| created_at        | 2017-06-21T16:07:41Z                 |
| description       |                                      |
| dns_nameservers   | 10.0.0.1                             |
| enable_dhcp       | True                                 |
| gateway_ip        | 172.16.1.1                           |
| host_routes       |                                      |
| id                | 19b55184-71f6-4fab-b6da-2309dd7f0de9 |
| ip_version        | 4                                    |
| ipv6_address_mode | None                                 |
| ipv6_ra_mode      | None                                 |
| name              | selfservice                          |
| network_id        | bec99697-2bb8-448a-b1d5-80f73cca4654 |
| project_id        | 835735f545f04650b58c71a583242b35     |
| revision_number   | 2                                    |
| segment_id        | None                                 |
| service_types     |                                      |
| subnetpool_id     | None                                 |
| updated_at        | 2017-06-21T16:07:41Z                 |
+-------------------+--------------------------------------+

Next let's create a router which connect the self service netwokr through the provider network:

[root@os-controller ~]# openstack router create router
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| admin_state_up          | UP                                   |
| availability_zone_hints |                                      |
| availability_zones      |                                      |
| created_at              | 2017-06-21T16:09:33Z                 |
| description             |                                      |
| distributed             | False                                |
| external_gateway_info   | None                                 |
| flavor_id               | None                                 |
| ha                      | False                                |
| id                      | f84d21b1-c643-445a-87fb-b908b437f459 |
| name                    | router                               |
| project_id              | 835735f545f04650b58c71a583242b35     |
| revision_number         | None                                 |
| routes                  |                                      |
| status                  | ACTIVE                               |
| updated_at              | 2017-06-21T16:09:33Z                 |
+-------------------------+--------------------------------------+

Next let's add the self service network as an interface in the router:

[root@os-controller ~]# neutron router-interface-add router selfservice
neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
Added interface c10e45dc-806f-4bde-af26-3207b4352cf2 to router router.

And lastly set the gateway for the router:

[root@os-controller ~]# neutron router-gateway-set router provider
neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
Set gateway for router router

At this point your should see 3 network spaces:

[root@os-controller ~]# ip netns
qrouter-f84d21b1-c643-445a-87fb-b908b437f459 (id: 2)
qdhcp-bec99697-2bb8-448a-b1d5-80f73cca4654 (id: 1)
qdhcp-addf3eeb-ef5d-4222-9cbe-ecd8e782702a (id: 0)

And you can list the ports used on the router:

[root@os-controller ~]# openstack port list --router router
+--------------------------------------+------+-------------------+------------------------------------------+--------+
| ID                                   | Name | MAC Address       | Fixed IP Addresses                       | Status |
+--------------------------------------+------+-------------------+------------------------------------------+--------+
| c10e45dc-806f-4bde-af26-3207b4352cf2 |      | fa:16:3e:04:3c:e2 | ip_address='172.16.1.1',                 | ACTIVE |
|                                      |      |                   | subnet_id='19b55184-71f6-4fab-b6da-      |        |
|                                      |      |                   | 2309dd7f0de9'                            |        |
| e8b0a9e8-3f95-4f67-ae4e-e59c6a926e16 |      | fa:16:3e:ed:c8:98 | ip_address='10.0.0.104', subnet_id='9fdb | ACTIVE |
|                                      |      |                   | 2fe2-79e6-4224-9395-fda93c0fe6d9'        |        |
+--------------------------------------+------+-------------------+------------------------------------------+--------+

And you will have two networks defined:

[root@os-controller ~]# openstack network list
+--------------------------------------+-------------+--------------------------------------+
| ID                                   | Name        | Subnets                              |
+--------------------------------------+-------------+--------------------------------------+
| addf3eeb-ef5d-4222-9cbe-ecd8e782702a | provider    | 9fdb2fe2-79e6-4224-9395-fda93c0fe6d9 |
| bec99697-2bb8-448a-b1d5-80f73cca4654 | selfservice | 19b55184-71f6-4fab-b6da-2309dd7f0de9 |
+--------------------------------------+-------------+--------------------------------------+


Next create your self service network:

[root@os-controller ~]# openstack network create selfservice
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2017-06-21T16:02:22Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | bec99697-2bb8-448a-b1d5-80f73cca4654 |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | None                                 |
| mtu                       | 1450                                 |
| name                      | selfservice                          |
| port_security_enabled     | True                                 |
| project_id                | 835735f545f04650b58c71a583242b35     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 53                                   |
| qos_policy_id             | None                                 |
| revision_number           | 3                                    |
| router:external           | Internal                             |
| segments                  | None                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| updated_at                | 2017-06-21T16:02:22Z                 |
+---------------------------+--------------------------------------+

After that initially I was failing to ping and I saw this:

[root@os-compute ~]# ping 10.0.0.104
PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
From 10.0.0.10 icmp_seq=1 Destination Host Prohibited
From 10.0.0.10 icmp_seq=2 Destination Host Prohibited
From 10.0.0.10 icmp_seq=3 Destination Host Prohibited
^C
--- 10.0.0.104 ping statistics ---
3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2072ms

Since I was getting "Host Prohibited" I was guessing it was a firewall issue. From inside the router it worked;

[root@os-controller ~]# ip netns exec qrouter-f84d21b1-c643-445a-87fb-b908b437f459 ping 10.0.0.104
PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
64 bytes from 10.0.0.104: icmp_seq=1 ttl=64 time=0.033 ms
64 bytes from 10.0.0.104: icmp_seq=2 ttl=64 time=0.025 ms
^C
--- 10.0.0.104 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1009ms
rtt min/avg/max/mdev = 0.025/0.029/0.033/0.004 ms

I then ran into this:

https://bugzilla.redhat.com/show_bug.cgi?id=1191536

And for the workaround I tried this:

iptables -I FORWARD 2 -s 10.0.0.0/24 -j ACCEPT -m comment --comment test

and then the ping started working:

[root@os-compute ~]# ping -c 2 10.0.0.104
PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
64 bytes from 10.0.0.104: icmp_seq=1 ttl=64 time=0.146 ms
64 bytes from 10.0.0.104: icmp_seq=2 ttl=64 time=0.156 ms

--- 10.0.0.104 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1046ms
rtt min/avg/max/mdev = 0.146/0.151/0.156/0.005 ms

# next let's create a small flavor:

[root@os-controller ~]# openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano
+----------------------------+---------+
| Field                      | Value   |
+----------------------------+---------+
| OS-FLV-DISABLED:disabled   | False   |
| OS-FLV-EXT-DATA:ephemeral  | 0       |
| disk                       | 1       |
| id                         | 0       |
| name                       | m1.nano |
| os-flavor-access:is_public | True    |
| properties                 |         |
| ram                        | 64      |
| rxtx_factor                | 1.0     |
| swap                       |         |
| vcpus                      | 1       |
+----------------------------+---------+

And let's create an SSH key pair and upload it to openstack:

[root@os-controller ~]# . demo-setup
[root@os-controller ~]# ssh-keygen -q -N ""
Enter file in which to save the key (/root/.ssh/id_rsa):
[root@os-controller ~]# openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
+-------------+-------------------------------------------------+
| Field       | Value                                           |
+-------------+-------------------------------------------------+
| fingerprint | 5b:47:4d:50:80:7f:6c:93:1a:3e:55:d5:5a:ed:3c:3b |
| name        | mykey                                           |
| user_id     | 21484b2e03ae40d2b79c20b8389473c3                |
+-------------+-------------------------------------------------+

You can confirm the key is imported:

[root@os-controller ~]# openstack keypair list
+-------+-------------------------------------------------+
| Name  | Fingerprint                                     |
+-------+-------------------------------------------------+
| mykey | 5b:47:4d:50:80:7f:6c:93:1a:3e:55:d5:5a:ed:3c:3b |
+-------+-------------------------------------------------+

Next let's allow ICMP and ssh to Instance:

[root@os-controller ~]# openstack security group rule create --proto icmp default
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| created_at        | 2017-06-21T17:13:20Z                 |
| description       |                                      |
| direction         | ingress                              |
| ether_type        | IPv4                                 |
| id                | 89ff0c93-f126-4e17-b5aa-db770038d1d7 |
| name              | None                                 |
| port_range_max    | None                                 |
| port_range_min    | None                                 |
| project_id        | 76315fbcf38f430199b6153da2e6d5b1     |
| protocol          | icmp                                 |
| remote_group_id   | None                                 |
| remote_ip_prefix  | 0.0.0.0/0                            |
| revision_number   | 1                                    |
| security_group_id | 89779c12-7b39-4357-86c4-642fd40f9048 |
| updated_at        | 2017-06-21T17:13:20Z                 |
+-------------------+--------------------------------------+

and here is the SSH rule:

[root@os-controller ~]# openstack security group rule create --proto tcp --dst-port 22 default
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| created_at        | 2017-06-21T17:13:50Z                 |
| description       |                                      |
| direction         | ingress                              |
| ether_type        | IPv4                                 |
| id                | 4b76dd2f-d3b7-446d-9e9b-4fc7a72d2b82 |
| name              | None                                 |
| port_range_max    | 22                                   |
| port_range_min    | 22                                   |
| project_id        | 76315fbcf38f430199b6153da2e6d5b1     |
| protocol          | tcp                                  |
| remote_group_id   | None                                 |
| remote_ip_prefix  | 0.0.0.0/0                            |
| revision_number   | 1                                    |
| security_group_id | 89779c12-7b39-4357-86c4-642fd40f9048 |
| updated_at        | 2017-06-21T17:13:50Z                 |
+-------------------+--------------------------------------+

To launch the instance, we can get all the details first. Get the lit of flavors:

[root@os-controller ~]# . demo-setup
[root@os-controller ~]# openstack flavor list
+----+---------+-----+------+-----------+-------+-----------+
| ID | Name    | RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+---------+-----+------+-----------+-------+-----------+
| 0  | m1.nano |  64 |    1 |         0 |     1 | True      |
+----+---------+-----+------+-----------+-------+-----------+

List the available images:

[root@os-controller ~]# openstack image list
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| f71063a9-7865-4b10-9216-b213b44f5073 | cirros | active |
+--------------------------------------+--------+--------+

List the available networks:

[root@os-controller ~]# openstack network list                                                                             +--------------------------------------+-------------+--------------------------------------+
| ID                                   | Name        | Subnets                              |
+--------------------------------------+-------------+--------------------------------------+
| addf3eeb-ef5d-4222-9cbe-ecd8e782702a | provider    | 9fdb2fe2-79e6-4224-9395-fda93c0fe6d9 |
| dc61d555-2a0f-44e6-873c-db4c108915f3 | selfservice | 152cfc92-e1ba-428f-93d9-a729fc6ec83a |
+--------------------------------------+-------------+--------------------------------------+

And now let's deploy our instance:

[root@os-controller ~]# openstack server create --flavor m1.nano --image cirros --nic net-id=dc61d555-2a0f-44e6-873c-db4c10
8915f3 --security-group default --key-name mykey selfservice-instance
+-----------------------------+-----------------------------------------------+
| Field                       | Value                                         |
+-----------------------------+-----------------------------------------------+
| OS-DCF:diskConfig           | MANUAL                                        |
| OS-EXT-AZ:availability_zone |                                               |
| OS-EXT-STS:power_state      | NOSTATE                                       |
| OS-EXT-STS:task_state       | scheduling                                    |
| OS-EXT-STS:vm_state         | building                                      |
| OS-SRV-USG:launched_at      | None                                          |
| OS-SRV-USG:terminated_at    | None                                          |
| accessIPv4                  |                                               |
| accessIPv6                  |                                               |
| addresses                   |                                               |
| adminPass                   | YzquCDoKn52k                                  |
| config_drive                |                                               |
| created                     | 2017-06-21T17:21:05Z                          |
| flavor                      | m1.nano (0)                                   |
| hostId                      |                                               |
| id                          | 48558e07-6aaf-454e-8f7c-2f17444e99d6          |
| image                       | cirros (f71063a9-7865-4b10-9216-b213b44f5073) |
| key_name                    | mykey                                         |
| name                        | selfservice-instance                          |
| progress                    | 0                                             |
| project_id                  | 76315fbcf38f430199b6153da2e6d5b1              |
| properties                  |                                               |
| security_groups             | name='default'                                |
| status                      | BUILD                                         |
| updated                     | 2017-06-21T17:21:05Z                          |
| user_id                     | 21484b2e03ae40d2b79c20b8389473c3              |
| volumes_attached            |                                               |
+-----------------------------+-----------------------------------------------+

If all is well you should the VM as active:

+------------------+------------------+--------+------------------+------------+
| ID               | Name             | Status | Networks         | Image Name |
+------------------+------------------+--------+------------------+------------+
| 5c923055-37a8-4b | selfservice-     | ACTIVE | selfservice=172. | cirros     |
| 82-a329-869c4d8f | instance         |        | 16.1.5           |            |
| efd4             |                  |        |                  |            |
+------------------+------------------+--------+------------------+------------+

If you get an ERROR status, check out the logs under /var/log/nova to see why it might not have started. You will also see the VM started in libvirtd:

[root@os-compute ~]# virsh list
 Id    Name                           State
----------------------------------------------------
 1     instance-00000002              running

Next we can figure out what the VNC URL is for that vm:

[root@os-controller ~]# openstack console url show selfservice-instance
+-------+----------------------------------------------------------------------+
| Field | Value                                                                |
+-------+----------------------------------------------------------------------+
| type  | novnc                                                                |
| url   | http://192.168.1.121:6080/vnc_auto.html?token=4371c8a8-c7b4-4381-ac8 |
|       | 1-555156cd1ea3                                                       |
+-------+----------------------------------------------------------------------+

And then point your browser to that URL and you will see the console of the VM:


I noticed that I couldn't ping the default gw from the VM. Here is what I saw on the compute node:

[root@os-compute neutron]# tcpdump -i any -nne icmp and not host kerch
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on any, link-type LINUX_SLL (Linux cooked), capture size 262144 bytes
21:54:39.632390  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
21:54:40.625319  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
21:54:41.625206  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
^C
3 packets captured
7 packets received by filter
0 packets dropped by kernel

It looks like another iptables issue. I deleted the default reject rule on the INPUT chain and the pings started working:

[root@os-controller ~]# iptables -L INPUT -n -v --line-numbers
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1     900K  331M neutron-linuxbri-INPUT  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
2     901K  331M nova-api-INPUT  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
3     877K  329M ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            state RELATED,ESTABLISHED
4        1    84 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
5     1571 92572 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
6        3   284 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:22
7       11   636 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:80
8       19  1140 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:5672
9        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:9292
10       1    60 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:9696
11      32  1792 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:35357
12       0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:5000
13      12   701 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:6080
14     470 28200 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:8778
15       0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:11211
16   23194 2150K REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            reject-with icmp-host-prohibited
[root@os-controller ~]# iptables -D INPUT 16

22:07:21.005258  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
22:07:22.005387  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
22:07:51.224434  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
22:07:52.221343  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
22:07:53.221241  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
22:09:57.027575   P fa:16:3e:37:74:b4 ethertype IPv4 (0x0800), length 100: 172.16.1.10 > 172.16.1.1: ICMP echo request, id 40449, seq 0, length 64
22:09:57.027624 Out fa:16:3e:37:74:b4 ethertype IPv4 (0x0800), length 100: 172.16.1.10 > 172.16.1.1: ICMP echo request, id 40449, seq 0, length 64
22:09:57.027768   P fa:16:3e:f3:01:8e ethertype IPv4 (0x0800), length 100: 172.16.1.1 > 172.16.1.10: ICMP echo reply, id 40449, seq 0, length 64
22:09:57.027774 Out fa:16:3e:f3:01:8e ethertype IPv4 (0x0800), length 100: 172.16.1.1 > 172.16.1.10: ICMP echo reply, id 40449, seq 0, length 64

And after another reboot it was able to get an address with DHCP:

[root@os-controller ~]# openstack console log show selfservice-instance | tail -40
=== system information ===
Platform: RDO OpenStack Compute
Container: none
Arch: x86_64
CPU(s): 1 @ 3408.101 MHz
Cores/Sockets/Threads: 1/1/1
Virt-type: AMD-V
RAM Size: 49MB
Disks:
NAME MAJ:MIN       SIZE LABEL         MOUNTPOINT
vda  253:0   1073741824               
vda1 253:1   1061061120 cirros-rootfs /
=== sshd host keys ===
-----BEGIN SSH HOST KEY KEYS-----
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgwCOpN9JDB6JxiwVqNlKPfSOiflbqQUU84Ci7hYgMorudk7FgBbWvBUBy4WzzY74+c1cjH3MF+u5cjz6HUuCbqTcYd/p8EtSLzGAB4wdWn/L2ye++wCyqKHrSqnho7AoXe9p3f6ga7Dx8oQo2SQyFrd4Xee97cP+0NL0OY1SCyxcDhW9 root@selfservice-instance
-----END SSH HOST KEY KEYS-----
=== network info ===
if-info: lo,up,127.0.0.1,8,::1
if-info: eth0,up,172.16.1.10,24,fe80::f816:3eff:fe37:74b4
ip-route:default via 172.16.1.1 dev eth0 
ip-route:169.254.169.254 via 172.16.1.1 dev eth0 
ip-route:172.16.1.0/24 dev eth0  src 172.16.1.10 
=== datasource: ec2 net ===
instance-id: i-0000000a
name: N/A
availability-zone: nova
local-hostname: selfservice-instance.novalocal
launch-index: 0
=== cirros: current=0.3.5 uptime=11.67 ===
  ____               ____  ____
 / __/ __ ____ ____ / __ \/ __/
/ /__ / // __// __// /_/ /\ \ 
\___//_//_/  /_/   \____/___/ 
   http://cirros-cloud.net


login as 'cirros' user. default password: 'cubswin:)'. use 'sudo' for root.
selfservice-instance login: 


And I was able to ping it from the router:

[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c ping -c 1 172.16.1.10
PING 172.16.1.10 (172.16.1.10) 56(84) bytes of data.
64 bytes from 172.16.1.10: icmp_seq=1 ttl=64 time=5.19 ms

--- 172.16.1.10 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 5.194/5.194/5.194/0.000 ms


As a final test let's create a floating IP:

which is covered here:

https://docs.openstack.org/user-guide/cli-manage-ip-addresses.html

[root@os-controller ~]# . demo-setup
[root@os-controller ~]# openstack floating ip create provider
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| created_at          | 2017-06-22T04:32:27Z                 |
| description         |                                      |
| fixed_ip_address    | None                                 |
| floating_ip_address | 10.0.0.109                           |
| floating_network_id | addf3eeb-ef5d-4222-9cbe-ecd8e782702a |
| id                  | 8a8cd86e-bb58-45a1-8af9-e1e9dbcf5cd2 |
| name                | None                                 |
| port_id             | None                                 |
| project_id          | 76315fbcf38f430199b6153da2e6d5b1     |
| revision_number     | 1                                    |
| router_id           | None                                 |
| status              | DOWN                                 |
| updated_at          | 2017-06-22T04:32:27Z                 |
+---------------------+--------------------------------------+
[root@os-controller ~]# openstack floating ip list
+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+
| ID                                 | Floating IP Address | Fixed IP Address | Port | Floating Network                   | Project                          |
+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+
| 8a8cd86e-                          | 10.0.0.109          | None             | None | addf3eeb-ef5d-4222-9cbe-           | 76315fbcf38f430199b6153da2e6d5b1 |
| bb58-45a1-8af9-e1e9dbcf5cd2        |                     |                  |      | ecd8e782702a                       |                                  |
+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+
[root@os-controller ~]# openstack server add floating ip selfservice-instance 10.0.0.109
[root@os-controller ~]# openstack server list
+--------------------------------------+----------------------+--------+-------------------------------------+------------+
| ID                                   | Name                 | Status | Networks                            | Image Name |
+--------------------------------------+----------------------+--------+-------------------------------------+------------+
| 4a3be61d-2350-4304-bbf7-657083cc6ccb | selfservice-instance | ACTIVE | selfservice=172.16.1.10, 10.0.0.109 | cirros     |
+--------------------------------------+----------------------+--------+-------------------------------------+------------+

Now login from a machine that has access to the provider network:

┌─[elatov@arch] - [/home/elatov] - [2017-06-21 10:33:57]
└─[0] <> ping 10.0.0.109
PING 10.0.0.109 (10.0.0.109) 56(84) bytes of data.
64 bytes from 10.0.0.109: icmp_seq=1 ttl=62 time=6.93 ms
64 bytes from 10.0.0.109: icmp_seq=2 ttl=62 time=1.08 ms
^C
--- 10.0.0.109 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.081/4.009/6.938/2.929 ms
┌─[elatov@arch] - [/home/elatov] - [2017-06-21 10:34:01]
└─[0] <> ssh cirros@10.0.0.109
The authenticity of host '10.0.0.109 (10.0.0.109)' can't be established.
RSA key fingerprint is SHA256:3kqW7d2DWjZfCLc+NqqqJbfbmpvQTp2PZLwqOHqzbW4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.0.0.109' (RSA) to the list of known hosts.
cirros@10.0.0.109's password: 
$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue 
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc pfifo_fast qlen 1000
    inet 172.16.1.10/24 brd 172.16.1.255 scope global eth0
$ ping -c 1 google.com
PING google.com (172.217.11.238): 56 data bytes
64 bytes from 172.217.11.238: seq=0 ttl=57 time=5.251 ms

--- google.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 5.251/5.251/5.251 ms

### Troubleshooting Networking
When my ping weren't working, I started looking into the flow of the traffic in openstack. These sites have good examples:

https://docs.openstack.org/ops-guide/ops-network-troubleshooting.html
https://docs.openstack.org/kilo/networking-guide/scenario_legacy_lb.html

Let's track down the flow from their examples:



# then list the security groups:

[root@os-controller ~]# openstack security group list
+--------------------------------------+---------+------------------------+---------+
| ID                                   | Name    | Description            | Project |
+--------------------------------------+---------+------------------------+---------+
| 89779c12-7b39-4357-86c4-642fd40f9048 | default | Default security group |         |
+--------------------------------------+---------+------------------------+---------+

