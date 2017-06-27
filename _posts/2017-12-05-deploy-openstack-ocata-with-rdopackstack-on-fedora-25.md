---
published: false
layout: post
title: "Deploy OpenStack Ocata with RDO/PackStack on Fedora 25"
author: Karim Elatov
categories: [home_lab, networking, os]
tags: [openstack, packstack, puppet]
---
### OpenStack Installers
So after [manually deploying Openstack](/2017/11/manually-deploying-openstack-ocata-on-fedora-25/), I decided to check out the options for automating that install. Here are some good sites that compare the installers:

* [Comparison of OpenStack Installers](http://ijiset.com/vol2/v2s9/IJISET_V2_I9_92.pdf)
* [DevOps Installers](https://wiki.openstack.org/wiki/Get_OpenStack#DevOps_Installers)
* [OpenStack all-in-one: test cloud services in one laptop](http://www.brianlinkletter.com/openstack-on-one-machine/)

After reading over all the different installers, I decided to try out RDO which uses **Packstack** since it supported Fedora and I already had a VM with that intalled.

### VMware Snapshots
Since I was installing **OpenStack** multiple times, I created a snapshot of the VM prior to the install and then I would revert back to re-test the installer. Here are the commands I used to revert a snapshot on a VMware VM.

	## Get the VMID:
	[root@esxi:~] vim-cmd vmsvc/getallvms
	Vmid   Name          File             Guest OS        Version   
	10     os-comp       os-compute.vmx   fedora64Guest   vmx-13
	11     os-test       os-test.vmx      fedora64Guest   vmx-13
	
	## Get the snapshot ID
	[root@esxi:~] vim-cmd vmsvc/snapshot.get 11
	Get Snapshot:
	|-ROOT
	--Snapshot Name        : before-packstack-with-mariadb
	--Snapshot Id        : 3
	--Snapshot Desciption  :
	--Snapshot Created On  : 6/22/2017 16:18:14
	--Snapshot State       : powered off
	
	## Revert:
	[root@esxi:~] vim-cmd vmsvc/snapshot.revert 11 3 0
	Revert Snapshot:
	|-ROOT
	--Snapshot Name        : before-packstack-with-mariadb
	--Snapshot Id        : 3
	--Snapshot Desciption  :
	--Snapshot Created On  : 6/22/2017 16:18:14
	--Snapshot State       : powered off
	
	## Power on
	[root@esxi:~] vim-cmd vmsvc/power.on 11


### PackStack
I decided to mimic my previous setup and not use **OVS** and just use **LinuxBridge** for it's networking. The setup with OVS is covered here:

* [Install OpenStack Juno on CentOS 7 / RHEL 7](http://www.tuxfixer.com/install-openstack-on-centos-7-rhel-7/)
* [Neutron with existing external network](https://www.rdoproject.org/networking/neutron-with-existing-external-network/)

Following the instructions laid out [here](https://www.rdoproject.org/install/packstack/) to install, I ran the following to install the package:

	$ dnf install -y https://rdoproject.org/repos/rdo-release.rpm
	$ dnf upgrade
	$ dnf install -y openstack-packstack

And then for the install, it should be as simple as this:

	packstack --allinone

Initially when I ran that, I saw the following error:


	[root@packstack ~]# packstack --allinone
	Welcome to the Packstack setup utility
	
	The installation log file is available at: /var/tmp/packstack/20170621-144129-mO5ppO/openstack-setup.log
	Packstack changed given value  to required value /root/.ssh/id_rsa.pub
	
	Installing:
	Clean Up                                             [ DONE ]
	Discovering ip protocol version                      [ DONE ]
	Setting up ssh keys                                  [ DONE ]
	Preparing Aodh entries                               [ DONE ]
	Preparing Puppet manifests                           [ DONE ]
	Copying Puppet modules and manifests                 [ DONE ]
	Applying 192.168.1.123_controller.pp
	192.168.1.123_controller.pp:                      [ ERROR ]
	Applying Puppet manifests                         [ ERROR ]
	ERROR : Error appeared during Puppet run: 192.168.1.123_controller.pp
	Error: Execution of '/usr/bin/mysql --database=mysql -e SET PASSWORD FOR 'root'@'localhost' = '*BFA8DD4F1E291E5EB4015D$
	730281B4AD4EE9C6C'' returned 1: ERROR 1290 (HY000) at line 1: The MariaDB server is running with the --strict-password$
	validation option so it cannot execute this statement
	You will find full trace in log /var/tmp/packstack/20170621-144129-mO5ppO/manifests/192.168.1.123_controller.pp.log
	Please check log file /var/tmp/packstack/20170621-144129-mO5ppO/openstack-setup.log for more information
	Additional information:
	 * A new answerfile was created in: /root/packstack-answers-20170621-144129.txt

I ran into the issue b/c newer versions of **MariaDB** run with passsord enforment. To disable the envorcement just move the config out of the way:

	[root@packstack ~]# mv /etc/my.cnf.d/cracklib_password_check.cnf ~
	[root@packstack ~]# systemctl restart mariadb

And now that I had a answer file, I just re-used that:

	[root@packstack ~]# cp /root/packstack-answers-20170621-144129.txt ans1.txt

And modified that for my needs:

	[root@packstack ~]# cat ans1.txt
	[general]
	CONFIG_SSH_KEY=/root/.ssh/id_rsa.pub
	CONFIG_DEFAULT_PASSWORD=secret
	CONFIG_SERVICE_WORKERS=%{::processorcount}
	CONFIG_MARIADB_INSTALL=y
	CONFIG_GLANCE_INSTALL=y
	CONFIG_CINDER_INSTALL=n
	CONFIG_MANILA_INSTALL=n
	CONFIG_NOVA_INSTALL=y
	CONFIG_NEUTRON_INSTALL=y
	CONFIG_HORIZON_INSTALL=y
	CONFIG_SWIFT_INSTALL=n
	CONFIG_CEILOMETER_INSTALL=n
	CONFIG_AODH_INSTALL=n
	CONFIG_GNOCCHI_INSTALL=n
	CONFIG_PANKO_INSTALL=n
	CONFIG_SAHARA_INSTALL=n
	CONFIG_HEAT_INSTALL=n
	CONFIG_MAGNUM_INSTALL=n
	CONFIG_TROVE_INSTALL=n
	CONFIG_IRONIC_INSTALL=n
	CONFIG_CLIENT_INSTALL=y
	CONFIG_NTP_SERVERS=
	CONFIG_NAGIOS_INSTALL=n
	EXCLUDE_SERVERS=
	CONFIG_DEBUG_MODE=n
	CONFIG_CONTROLLER_HOST=192.168.1.123
	CONFIG_COMPUTE_HOSTS=192.168.1.123
	CONFIG_NETWORK_HOSTS=192.168.1.123
	CONFIG_VMWARE_BACKEND=n
	CONFIG_UNSUPPORTED=n
	CONFIG_USE_SUBNETS=n
	CONFIG_USE_EPEL=n
	CONFIG_ENABLE_RDO_TESTING=n                                                                                   
	CONFIG_RH_OPTIONAL=n
	CONFIG_AMQP_BACKEND=rabbitmq
	CONFIG_AMQP_HOST=192.168.1.123
	CONFIG_AMQP_ENABLE_SSL=n
	CONFIG_AMQP_ENABLE_AUTH=n
	CONFIG_MARIADB_HOST=192.168.1.123
	CONFIG_MARIADB_USER=root
	CONFIG_MARIADB_PW=1d0b650c25d747b0
	CONFIG_KEYSTONE_DB_PW=033d66db896240c7
	CONFIG_KEYSTONE_DB_PURGE_ENABLE=True
	CONFIG_KEYSTONE_REGION=RegionOne
	CONFIG_KEYSTONE_ADMIN_TOKEN=d3afbcbd69204a9584eaa08f48a4a183
	CONFIG_KEYSTONE_ADMIN_EMAIL=root@localhost
	CONFIG_KEYSTONE_ADMIN_USERNAME=admin
	CONFIG_KEYSTONE_ADMIN_PW=18514cde3aef48c9
	CONFIG_KEYSTONE_DEMO_PW=15c721e1168f4890
	CONFIG_KEYSTONE_API_VERSION=v3
	CONFIG_KEYSTONE_TOKEN_FORMAT=FERNET
	CONFIG_KEYSTONE_IDENTITY_BACKEND=sql
	CONFIG_GLANCE_DB_PW=4bc84587a1e247a8
	CONFIG_GLANCE_KS_PW=54d5917730d64076
	CONFIG_GLANCE_BACKEND=file
	CONFIG_NOVA_DB_PURGE_ENABLE=True
	CONFIG_NOVA_DB_PW=a8bf0cae919243a9
	CONFIG_NOVA_KS_PW=2283ad92febb4664
	CONFIG_NOVA_MANAGE_FLAVORS=y
	CONFIG_NOVA_SCHED_CPU_ALLOC_RATIO=16.0
	CONFIG_NOVA_SCHED_RAM_ALLOC_RATIO=1.5
	CONFIG_NOVA_COMPUTE_MIGRATE_PROTOCOL=tcp
	CONFIG_NOVA_COMPUTE_MANAGER=nova.compute.manager.ComputeManager
	CONFIG_NOVA_LIBVIRT_VIRT_TYPE=%{::default_hypervisor}
	CONFIG_NEUTRON_KS_PW=9225367a990b4c23
	CONFIG_NEUTRON_DB_PW=1d824d32afa04aa9
	CONFIG_NEUTRON_L3_EXT_BRIDGE=br-ex
	CONFIG_NEUTRON_METADATA_PW=ed151f0c94ce4b16
	CONFIG_LBAAS_INSTALL=n
	CONFIG_NEUTRON_METERING_AGENT_INSTALL=n
	CONFIG_NEUTRON_FWAAS=n
	CONFIG_NEUTRON_VPNAAS=n
	CONFIG_NEUTRON_ML2_TYPE_DRIVERS=vxlan,flat
	CONFIG_NEUTRON_ML2_TENANT_NETWORK_TYPES=vxlan
	CONFIG_NEUTRON_ML2_MECHANISM_DRIVERS=openvswitch
	CONFIG_NEUTRON_ML2_FLAT_NETWORKS=ens192
	CONFIG_NEUTRON_ML2_VLAN_RANGES=ens192
	CONFIG_NEUTRON_ML2_VNI_RANGES=10:100
	CONFIG_NEUTRON_L2_AGENT=openvswitch
	CONFIG_NEUTRON_ML2_SUPPORTED_PCI_VENDOR_DEVS=['15b3:1004', '8086:10ca']
	CONFIG_NEUTRON_OVS_BRIDGE_MAPPINGS=extnet:br-ex
	CONFIG_NEUTRON_OVS_BRIDGE_IFACES=br-ex:ens192
	CONFIG_NEUTRON_OVS_BRIDGES_COMPUTE=
	CONFIG_NEUTRON_OVS_EXTERNAL_PHYSNET=extnet
	CONFIG_NEUTRON_OVS_TUNNEL_IF=
	CONFIG_NEUTRON_OVS_TUNNEL_SUBNETS=172.24.6.0/24
	CONFIG_NEUTRON_OVS_VXLAN_UDP_PORT=4789
	CONFIG_HORIZON_SSL=n
	CONFIG_HORIZON_SECRET_KEY=f59bc88a4f2b4c01af94954eda5c38b7
	CONFIG_HEAT_CLOUDWATCH_INSTALL=n
	CONFIG_HEAT_CFN_INSTALL=n
	CONFIG_PROVISION_DEMO=y
	CONFIG_PROVISION_TEMPEST=n
	CONFIG_PROVISION_DEMO_FLOATRANGE=172.24.4.0/24
	CONFIG_PROVISION_IMAGE_NAME=cirros
	CONFIG_PROVISION_IMAGE_URL=http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
	CONFIG_PROVISION_IMAGE_FORMAT=qcow2
	CONFIG_PROVISION_IMAGE_SSH_USER=cirros
	CONFIG_PROVISION_UEC_IMAGE_NAME=cirros-uec
	CONFIG_PROVISION_UEC_IMAGE_KERNEL_URL=http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-kernel
	CONFIG_PROVISION_UEC_IMAGE_RAMDISK_URL=http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-initramfs
	CONFIG_PROVISION_UEC_IMAGE_DISK_URL=http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
	CONFIG_RUN_TEMPEST=n
	CONFIG_PROVISION_OVS_BRIDGE=y

Then I can just re-use the file:

	# packstack --answer-file ans.txt

The next issue I ran into was with **httpd**:

	[root@packstack ~]# systemctl status httpd -l --no-pager
	● httpd.service - The Apache HTTP Server
	   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
	  Drop-In: /usr/lib/systemd/system/httpd.service.d
	           └─openstack-dashboard.conf
	   Active: failed (Result: exit-code) since Wed 2017-06-21 15:55:16 MDT; 7h ago
	  Process: 30903 ExecStartPre=/usr/bin/python /usr/share/openstack-dashboard/manage.py collectstatic --noinput --clear -v0 (code=exited, status=1/FAILURE)
	Jun 21 15:55:16 packstack.kar.int python[30903]:     logging_config_func(logging_settings)
	Jun 21 15:55:16 packstack.kar.int python[30903]:   File "/usr/lib64/python2.7/logging/config.py", line 794, in dictConfig
	Jun 21 15:55:16 packstack.kar.int python[30903]:     dictConfigClass(config).configure()
	Jun 21 15:55:16 packstack.kar.int python[30903]:   File "/usr/lib64/python2.7/logging/config.py", line 576, in configure
	Jun 21 15:55:16 packstack.kar.int python[30903]:     '%r: %s' % (name, e))
	Jun 21 15:55:16 packstack.kar.int python[30903]: ValueError: Unable to configure handler 'null': Cannot resolve 'django.utils.log.NullHandler': No module named NullHandler
	Jun 21 15:55:16 packstack.kar.int systemd[1]: httpd.service: Control process exited, code=exited status=1
	Jun 21 15:55:16 packstack.kar.int systemd[1]: Failed to start The Apache HTTP Server.
	Jun 21 15:55:16 packstack.kar.int systemd[1]: httpd.service: Unit entered failed state.
	Jun 21 15:55:16 packstack.kar.int systemd[1]: httpd.service: Failed with result 'exit-code'.

So I disabled the dashboard configuration, just to move on:

	[root@packstack ~]# mv /usr/lib/systemd/system/httpd.service.d/openstack-dashboard.conf ~
	[root@packstack ~]# systemctl daemon-reload
	[root@packstack ~]# systemctl start httpd
	[root@packstack ~]# systemctl status httpd
	● httpd.service - The Apache HTTP Server
	   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
	   Active: active (running) since Wed 2017-06-21 22:58:30 MDT; 4s ago
	 Main PID: 15438 (httpd)
	   Status: "Processing requests..."

Next it failed to install the packages for the compute node:

	ERROR : Error appeared during Puppet run: 192.168.1.123_compute.pp
	Error: Execution of '/usr/bin/yum -d 0 -e 0 -y install openstack-nova-compute' returned 1: Redirecting to '/usr/bin/dnf -d 0 -e 0 -y install openstack-nova-compute' (see 'man yum2dnf')

This was the same problem as before, so I just had to downgrade the **iptables** packages:

	$ dnf install iptables-1.6.0-2.fc25 --allowerasing
	$ dnf install iptables-services-1.6.0-2.fc25

After that the install worked out.

### PackStack with Parameters
After some playing around, I ended up running the following to get the options that I needed:

	[root@packstack ~]# packstack --allinone --provision-demo=n --os-neutron-ml2-type-drivers=flat,vxlan --os-neutron-ml2-mechanism-drivers=linuxbridge --os-neutron-ml2-flat-networks=physnet0 --os-neutron-l2-agent=linuxbridge --os-neutron-lb-interface-mappings=physnet0:ens192 --os-neutron-ml2-tenant-network-types='vxlan' --nagios-install=n --os-manila-install=n --os-horizon-install=n --os-swift-install=n --os-ceilometer-install=n --os-aodh-install=n --os-gnocchi-install=n --os-neutron-l3-ext-bridge="" --os-neutron-metering-agent-install=n --os-neutron-ovs-bridge-interfaces='' --provision-ovs-bridge=n --default-password=openstacksecret --gen-answer-file=ans.txt

I didn't really need the answer file, but I kept it for later use. With the above options specified it generated a brand new answer file and I was able to use it to complete the install:

	[root@packstack ~]# packstack --answer-file=ans.txt                                                                     
	Welcome to the Packstack setup utility
	
	The installation log file is available at: /var/tmp/packstack/20170623-123808-0nFhg9/openstack-setup.log
	
	Installing:
	Clean Up                                             [ DONE ]
	Discovering ip protocol version                      [ DONE ]
	Setting up ssh keys                                  [ DONE ]                                                                  Preparing servers                        [ DONE ]
	Pre installing Puppet and discovering hosts' details [ DONE ]
	Preparing pre-install entries                        [ DONE ]
	Setting up CACERT                                    [ DONE ]
	Preparing AMQP entries                               [ DONE ]
	Preparing MariaDB entries                            [ DONE ]
	Fixing Keystone LDAP config parameters to be undef if empty[ DONE ]
	Preparing Keystone entries                           [ DONE ]
	Preparing Glance entries                             [ DONE ]
	Checking if the Cinder server has a cinder-volumes vg[ DONE ]
	Preparing Cinder entries                             [ DONE ]
	Preparing Nova API entries                           [ DONE ]
	Creating ssh keys for Nova migration                 [ DONE ]
	Gathering ssh host keys for Nova migration           [ DONE ]
	Preparing Nova Compute entries                       [ DONE ]
	Preparing Nova Scheduler entries                     [ DONE ]
	Preparing Nova VNC Proxy entries                     [ DONE ]
	Preparing OpenStack Network-related Nova entries     [ DONE ]
	Preparing Nova Common entries                        [ DONE ]
	Preparing Neutron LBaaS Agent entries                [ DONE ]
	Preparing Neutron API entries                        [ DONE ]
	Preparing Neutron L3 entries                         [ DONE ]
	Preparing Neutron L2 Agent entries                   [ DONE ]
	Preparing Neutron DHCP Agent entries                 [ DONE ]
	Preparing Neutron Metering Agent entries             [ DONE ]
	Checking if NetworkManager is enabled and running    [ DONE ]
	Preparing OpenStack Client entries                   [ DONE ]
	Preparing Puppet manifests                           [ DONE ]
	Copying Puppet modules and manifests                 [ DONE ]
	Applying 192.168.1.123_controller.pp
	192.168.1.123_controller.pp:                         [ DONE ]
	Applying 192.168.1.123_network.pp
	192.168.1.123_network.pp:                            [ DONE ]
	Applying 192.168.1.123_compute.pp
	192.168.1.123_compute.pp:                            [ DONE ]
	Applying Puppet manifests                            [ DONE ]
	Finalizing                                           [ DONE ]
	
	**** Installation completed successfully ******
	
	Additional information:
	 * Time synchronization installation was skipped. Please note that unsynchronized time on server instances might be problem for
	 some OpenStack components.
	 * File /root/keystonerc_admin has been created on OpenStack client host 192.168.1.123. To use the command line tools you need
	to source the file.
	 * The installation log file is available at: /var/tmp/packstack/20170623-123808-0nFhg9/openstack-setup.log
	 * The generated manifests are available at: /var/tmp/packstack/20170623-123808-0nFhg9/manifests

And it finished successfully.

### Finishing the OpenStack Setup
At this point the install is finished and we are ready to create our networks and VMs. Most of the instructions are covered in [PackStack All-in-One DIY Configuration](https://www.rdoproject.org/documentation/packstack-all-in-one-diy-configuration/). 

#### OpenStack Network

First let's create the **external/provider** network.

	[root@packstack ~]# . keystonerc_admin
	[root@packstack ~(keystone_admin)]# openstack network create public-network --share --external --default --provider-network-type flat --provider-physical-network physnet0
	[root@packstack ~(keystone_admin)]# openstack subnet create public-subnet --dhcp  --subnet-range 10.0.0.0/24 --allocation-pool start=10.0.0.200,end=10.0.0.210  --gateway 10.0.0.1 --dns-nameserver 10.0.0.1 --network public-network

Next let's create the test **image**:

	[root@packstack ~]# curl http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img | glance image-create --name='cirros image' --visibility=public --container-format=bare --disk-format=qcow2

Now let's create out project and user

	[root@packstack ~]# openstack project create --domain default --description "Demo Project" demo
	[root@packstack ~]# openstack user create --domain default --password-prompt demo
	[root@packstack ~]# openstack role create user
	[root@packstack ~]# openstack role add --project demo --user demo user

Let'c create the **source file** for the demo user and make sure you can authenticate:

	[root@packstack ~(keystone_admin)]# . keystonerc_demo
	[root@packstack ~(keystone_demo)]# openstack image list
	+--------------------------------------+--------------+--------+
	| ID                                   | Name         | Status |
	+--------------------------------------+--------------+--------+
	| 2af5af07-baba-45a4-9406-fd84a0ff4359 | cirros image | active |
	+--------------------------------------+--------------+--------+

Next let's create a **router** and set a **gateway** for it:

	[root@packstack ~(keystone_demo)]# openstack router create router1
	[root@packstack ~(keystone_demo)]# openstack router set --external-gateway public-network router1

Now let's create a **private network** and let it go through the newly created **router**:

	[root@packstack ~(keystone_demo)]# openstack network create private_network
	[root@packstack ~(keystone_demo)]# openstack subnet create --dhcp --subnet-range 172.12.0.0/24 --network private_network private_subnet
	[root@packstack ~(keystone_demo)]# openstack router add subnet router1 private_subnet

#### OpenStack Launce Instance

Now to launch an instance let's do the same thing as before. Create a **flavor**:

	[root@packstack ~(keystone_admin)]# openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano

Get a **key pair** going:

	[root@packstack ~(keystone_admin)]# . keystonerc_demo
	[root@packstack ~(keystone_demo)]# openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey

Get the basic **security group** going:

	[root@packstack ~(keystone_demo)]# openstack security group rule create --proto icmp default
	[root@packstack ~(keystone_demo)]# openstack security group rule create --proto tcp --dst-port 22 default

And now let's launch our instance:

	[root@packstack ~(keystone_demo)]# openstack server create --flavor m1.nano --image "cirros image" --nic net-id=private_network --security-group default --key-name mykey test

Initially I ran into a NIC *binding* issue. And I saw the following in the logs:

	2017-06-23 14:44:58.725 21416 ERROR neutron.plugins.ml2.managers [req-bda7a9c1-c344-4ca6-bcaf-c4278f6d2944 - - - - -] Failed to bind port 2b3e7a33-8764-418f-951c-a883196cf97a on host packstack.kar.int for vnic_type normal using segments [{'segmentation_id': 48, 'physical_network': None, 'id': u'f9d4049c-cfff-47d6-a6b6-72d8d36a6ca9', 'network_type': u'vxlan'}]

And I noticed that my **bridges** were missing, but my **router namespace** was there:

	[root@packstack ~]# brctl show
	bridge name     bridge id               STP enabled     interfaces
	[root@packstack ~]# ip netns
	qrouter-13e859a7-a6de-4e4a-b55b-bd2b68224b50 (id: 0)

So I modified the **neutron** settings to look like this:

	[root@packstack ~(keystone_demo)]# grep -vE '^$|^#' /etc/neutron/neutron.conf
	[DEFAULT]
	bind_host=0.0.0.0
	auth_strategy=keystone
	core_plugin=ml2
	service_plugins=router
	allow_overlapping_ips=True
	notify_nova_on_port_status_changes=True
	notify_nova_on_port_data_changes=True
	api_workers=4
	rpc_workers=4
	router_scheduler_driver=neutron.scheduler.l3_agent_scheduler.ChanceScheduler
	l3_ha=False
	max_l3_agents_per_router=3
	debug=False
	log_dir=/var/log/neutron
	transport_url=rabbit://guest:guest@192.168.1.123:5672/
	rpc_backend=rabbit
	control_exchange=neutron
	[agent]
	root_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf
	[cors]
	[cors.subdomain]
	[database]
	connection=mysql+pymysql://neutron:openstacksecret@192.168.1.123/neutron
	[keystone_authtoken]
	auth_uri=http://192.168.1.123:5000/v3
	auth_type=password
	auth_url=http://192.168.1.123:35357
	username=neutron
	password=openstacksecret
	user_domain_name=Default
	project_name=services
	project_domain_name=Default
	[matchmaker_redis]
	[nova]
	region_name=RegionOne
	auth_url=http://192.168.1.123:35357
	auth_type=password
	password=openstacksecret
	project_domain_id=default
	project_domain_name=Default
	project_name=services
	tenant_name=services
	user_domain_id=default
	user_domain_name=Default
	username=nova
	[oslo_concurrency]
	lock_path=$state_path/lock
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	rabbit_use_ssl=False
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	policy_file=/etc/neutron/policy.json
	[qos]
	[quotas]
	[ssl]
	[service_providers]
	
	[root@packstack ~(keystone_demo)]# grep -vE '^$|^#' /etc/neutron/plugins/ml2/ml2_conf.ini
	[DEFAULT]
	[ml2]
	type_drivers = flat,vxlan
	tenant_network_types = vxlan
	mechanism_drivers =linuxbridge,l2population
	path_mtu = 0
	[ml2_type_flat]
	flat_networks = physnet0
	[ml2_type_geneve]
	[ml2_type_gre]
	[ml2_type_vlan]
	[ml2_type_vxlan]
	vni_ranges =10:100
	vxlan_group = 224.0.0.1
	[securitygroup]
	firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver
	enable_security_group = True
	
	[root@packstack ~(keystone_demo)]# grep -vE '^$|^#' /etc/neutron/plugins/ml2/linuxbridge_agent.ini
	[DEFAULT]
	[agent]
	tunnel_types=vxlan
	[linux_bridge]
	physical_interface_mappings =physnet0:ens192
	[securitygroup]
	firewall_driver = iptables
	[vxlan]
	enable_vxlan = true
	local_ip = 10.0.0.12
	l2_population = true
	
	[root@packstack ~(keystone_demo)]# grep -vE '^$|^#' /etc/neutron/l3_agent.ini
	[DEFAULT]
	interface_driver = linuxbridge
	agent_mode = legacy
	debug = False
	[agent]
	[ovs]

Then I restarted all the services to apply the changes:

	[root@packstack ~(keystone_demo)]# systemctl restart neutron-l3-agent neutron-linuxbridge-agent neutron-metadata-agent neutron-server

And then the VM booted up:

	[root@packstack ~(keystone_demo)]# openstack server list
	+-----------------------+------+--------+-----------------------+--------------+| ID                    | Name | Status | Networks              | Image Name   |+-----------------------+------+--------+-----------------------+--------------+| ca8dcb76-a0bb-4127    | test | ACTIVE | private_network=172.1 | cirros image || -a07d-2392b8629969    |      |        | 2.0.2                 |              |
	+-----------------------+------+--------+-----------------------+--------------+

#### Confirm VM Connectivity
I was able to SSH into the VM:

	[root@packstack ~(keystone_demo)]# ip netns exec qrouter-13e859a7-a6de-4e4a-b55b-bd2b68224b50 ssh cirros@172.12.0.2
	The authenticity of host '172.12.0.2 (172.12.0.2)' can't be established.
	RSA key fingerprint is SHA256:Zmx1TcjiK3cDezWoOtl0MSuz1lYfTMO9boOE93PVLMk.
	RSA key fingerprint is MD5:f4:c2:97:8c:e5:1d:0d:4a:e4:13:21:ce:97:8d:0c:a4.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added '172.12.0.2' (RSA) to the list of known hosts.
	$ ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue
	    inet 127.0.0.1/8 scope host lo
	2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc pfifo_fast qlen 1000
	    inet 172.12.0.2/24 brd 172.12.0.255 scope global eth0

And I after I applied the same work-around for iptables:

	[root@packstack ~(keystone_demo)]# iptables -I FORWARD 5 -s 10.0.0.0/24 -j ACCEPT -m comment --comment test

Then I was able to ping the external network from the VM:

	[root@packstack ~]# tcpdump -i any -nne 
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on any, link-type LINUX_SLL (Linux cooked), capture size 262144 bytes
	10:28:40.509194   P fa:16:3e:cd:ed:fc ethertype IPv4 (0x0800), length 100: 172.12.0.2 > 10.0.0.1: ICMP echo request, id 25089, seq 0, length 64
	10:28:40.509216 Out fa:16:3e:cd:ed:fc ethertype IPv4 (0x0800), length 100: 172.12.0.2 > 10.0.0.1: ICMP echo request, id 25089, seq 0, length 64
	10:28:40.509247   P fa:16:3e:15:27:92 ethertype IPv4 (0x0800), length 100: 10.0.0.200 > 10.0.0.1: ICMP echo request, id 25089, seq 0, length 64
	10:28:40.509254 Out fa:16:3e:15:27:92 ethertype IPv4 (0x0800), length 100: 10.0.0.200 > 10.0.0.1: ICMP echo request, id 25089, seq 0, length 64
	10:28:40.509427   P 78:24:af:7b:1f:08 ethertype IPv4 (0x0800), length 100: 10.0.0.1 > 10.0.0.200: ICMP echo reply, id 25089, seq 0, length 64
	10:28:40.509436 Out 78:24:af:7b:1f:08 ethertype IPv4 (0x0800), length 100: 10.0.0.1 > 10.0.0.200: ICMP echo reply, id 25089, seq 0, length 64
	10:28:40.509463   P fa:16:3e:6e:d9:79 ethertype IPv4 (0x0800), length 100: 10.0.0.1 > 172.12.0.2: ICMP echo reply, id 25089, seq 0, length 64

PackStack definitely eased the setup :)
