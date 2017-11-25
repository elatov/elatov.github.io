---
published: true
layout: post
title: "Manually Deploying OpenStack Ocata on Fedora 25"
author: Karim Elatov
categories: [networking,home_lab]
tags: [openstack,vxlan,network-namespace]
---
### OpenStack
So I decided to try out OpenStack on Fedora 25. I was able to follow the [OpenStack Installation Tutorial for Red Hat Enterprise Linux and CentOS](https://docs.openstack.org/ocata/install-guide-rdo/). The guide is pretty long and I don't want to cover each step in great detail since it's covered in the guide. I also decided to follow the [Networking Option 2: Self-service networks](https://docs.openstack.org/ocata/install-guide-rdo/overview.html#networking-option-2-self-service-networks) (it uses VXLAN for overlay networking) setup. Here are the components that get deployed in that scenario:

![networking-option-2-os](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/networking-option-2-os.png&raw=1)

And here is how the connectivity looks like (from [Self-service network](https://docs.openstack.org/ocata/install-guide-rdo/launch-instance-networks-selfservice.html) page):

![selfservice-network-os-conn](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/selfservice-network-os-conn.png&raw=1)

### OpenStack Controller Node
On the *controller* node I configured the following setttings.

#### OS Network for OpenStack
Here are the commands I ran to prepare Fedora for OpenStack:

	$ systemctl disable NetworkManager
	$ systemctl enable network
	$ vi /etc/sysconfig/network-scripts/ifcfg-ens192
	$ vi /etc/sysconfig/network-scripts/ifcfg-ens224
	$ dnf remove firewalld
	$ dnf install iptables-services
	$ systemctl enable iptables
	$ vi /etc/sysconfig/iptables
	$ systemctl start iptables

And don't forget to configure NTP:
	
	$ dnf install chrony
	$ chronyc sources

#### OpenStack Repo
I just installed the repo and went from there:
	
	$ dnf install https://rdoproject.org/repos/rdo-release.rpm
	$ dnf upgrade
	$ dnf install python-openstackclient
	
### Configure MariaDB
Here are the commands I ran to configure **MariaDB**:

	$ dnf install mariadb mariadb-server python2-PyMySQL
	$ mv /etc/my.cnf.d/cracklib_password_check.cnf ~/
	$ vi /etc/my.cnf.d/openstack.cnf
	---
	[mysqld]
	bind-address = 192.168.1.121
	
	default-storage-engine = innodb
	innodb_file_per_table = on
	max_connections = 4096
	collation-server = utf8_general_ci
	character-set-server = utf8
	---
	$ systemctl enable mariadb.service
	$ systemctl start mariadb.service
	$ mysql_secure_installation
	
#### Configure RabbitMQ
Here is the RabbitMQ setup:

	$ dnf install rabbitmq-server
	$ systemctl enable rabbitmq-server.service
	$ systemctl start rabbitmq-server.service
	$ rabbitmqctl add_user openstack secret
	$ rabbitmqctl set_permissions openstack ".*" ".*" ".*"
	
#### Configure Memcached
Here is the MemCached Setup:

	$ dnf install memcached python-memcached
	$ vi /etc/sysconfig/memcached
	---
	PORT="11211"
	USER="memcached"
	MAXCONN="1024"
	CACHESIZE="64"
	OPTIONS="-l 127.0.0.1,192.168.1.121"
	---
	$ systemctl enable memcached.service
	$ systemctl start memcached.service
	
#### Configure Identity Service (Keystone)
This one can be broken down into multiple parts. First setup the database:

	$ mysql -u root -p
	MariaDB [(none)]> CREATE DATABASE keystone;
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'secret';

Then install the package and configure the settings file:

	$ dnf install openstack-keystone httpd mod_wsgi
	$ grep -vE '^$|^#' /etc/keystone/keystone.conf
	[DEFAULT]
	[assignment]
	[auth]
	[cache]
	[catalog]
	[cors]
	[cors.subdomain]
	[credential]
	[database]
	connection = mysql+pymysql://keystone:secret@192.168.1.121/keystone
	[domain_config]
	[endpoint_filter]
	[endpoint_policy]
	[eventlet_server]
	[federation]
	[fernet_tokens]
	[healthcheck]
	[identity]
	[identity_mapping]
	[kvs]
	[ldap]
	[matchmaker_redis]
	[memcache]
	[oauth1]
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[paste_deploy]
	[policy]
	[profiler]
	[resource]
	[revoke]
	[role]
	[saml]
	[security_compliance]
	[shadow_users]
	[signing]
	[token]
	provider = fernet
	[tokenless_auth]
	[trust]
	
Then sync the settings to the database:

	$ su -s /bin/sh -c "keystone-manage db_sync" keystone
	
Next create the endpoints:

	$ keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
	$ keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
	$ keystone-manage bootstrap --bootstrap-password secret --bootstrap-admin-url http://os-controller:35357/v3/ --bootstrap-internal-url http://os-controller:5000/v3/ --bootstrap-public-url http://os-controller:5000/v3/ --bootstrap-region-id RegionOne
	
Then configure **apache** to serve the endpoints:

	$ vi /etc/httpd/conf/httpd.conf
	---
	ServerName os-controller.kar.int
	---
	$ ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/
	$ systemctl enable httpd.service
	$ systemctl start httpd.service

To prepare for next steps, let's create the **Admin Source Script**:

	$ cat admin-setup
	export OS_USERNAME=admin
	export OS_PASSWORD=secret
	export OS_PROJECT_NAME=admin
	export OS_USER_DOMAIN_NAME=Default
	export OS_PROJECT_DOMAIN_NAME=Default
	export OS_AUTH_URL=http://os-controller:35357/v3
	export OS_IDENTITY_API_VERSION=3

And lastly create some domain, projects, users, and roles:

	$ . admin-setup
	$ openstack project create --domain default --description "Service Project" service
	$ openstack project create --domain default --description "Demo Project" demo
	$ openstack user create --domain default --password-prompt demo
	$ openstack role create user
	$ openstack role add --project demo --user demo user

Also let's prepare the **Demo Source Script**:

	$ cat demo-setup
	export OS_PROJECT_DOMAIN_NAME=Default
	export OS_USER_DOMAIN_NAME=Default
	export OS_PROJECT_NAME=demo
	export OS_USERNAME=demo
	export OS_PASSWORD=secret
	export OS_AUTH_URL=http://os-controller:5000/v3
	export OS_IDENTITY_API_VERSION=3
	export OS_IMAGE_API_VERSION=2
	
#### Configure Image Service (Glance)
Similar setup for **glance**, create the DB:

	$ mysql -u root -p
	MariaDB [(none)]> CREATE DATABASE glance;
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'secret';
	
Connect to **keystone** and enable endpoints:

	$ . admin-setup
	$ openstack user create --domain default --password-prompt glance
	$ openstack role add --project service --user glance admin
	$ openstack service create --name glance --description "OpenStack Image" image
	$ openstack endpoint create --region RegionOne image public http://os-controller:9292
	$ openstack endpoint create --region RegionOne image internal http://os-controller:9292
    $ openstack endpoint create --region RegionOne image admin http://os-controller:9292
    
Configure the settings file:

    $ dnf install openstack-glance
    $ grep -vE '^$|^#' /etc/glance/glance-api.conf
	[DEFAULT]
	[cors]
	[cors.subdomain]
	[database]
	connection = mysql+pymysql://glance:secret@192.168.1.121/glance
	[glance_store]
	stores = file,http
	default_store = file
	filesystem_store_datadir = /var/lib/glance/images
	[image_format]
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = glance
	password = secret
	[matchmaker_redis]
	[oslo_concurrency]
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[paste_deploy]
	flavor = keystone
	[profiler]
	[store_type_location_strategy]
	[task]
	[taskflow_executor]
	$ grep -vE '^$|^#' /etc/glance/glance-registry.conf
	[DEFAULT]
	[database]
	connection = mysql+pymysql://glance:secret@192.168.1.121/glance
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = glance
	password = secret
	[matchmaker_redis]
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_policy]
	[paste_deploy]
	flavor = keystone
	[profiler]
	
And let's sync to the DB:

	$ su -s /bin/sh -c "glance-manage db_sync" glance
	
And lastly enable and start the service:

	$ systemctl enable openstack-glance-api.service   openstack-glance-registry.service
	$ systemctl start openstack-glance-api.service   openstack-glance-registry.service

To test out the image service, let's import a small image to make sure it's working:
	
	$ wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
	$ . admin-setup
	$ openstack image create "cirros" --file cirros-0.3.5-x86_64-disk.img --disk-format qcow2 --container-format bare --public
	
#### Configure Compute Service (Nova)
Prepare the DB:

	$ mysql -u root -p
	MariaDB [(none)]> CREATE DATABASE nova_api;
	MariaDB [(none)]> CREATE DATABASE nova;
	MariaDB [(none)]> CREATE DATABASE nova_cell0;
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost'  IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost'  IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%'  IDENTIFIED BY 'secret';
	
Create users and endpoints:
	
	$ . admin-openrc
	$ openstack user create --domain default --password-prompt nova
	$ openstack role add --project service --user nova admin
	$ openstack service create --name nova --description "OpenStack Compute" compute
	$ openstack endpoint create --region RegionOne compute public http://os-controller:8774/v2.1
	$ openstack endpoint create --region RegionOne compute internal http://os-controller:8774/v2.1
	$ openstack endpoint create --region RegionOne compute admin http://os-controller:8774/v2.1
	$ openstack user create --domain default --password-prompt placement
	$ openstack role add --project service --user placement admin
	$ openstack service create --name placement --description "Placement API" placement
	$ openstack endpoint create --region RegionOne placement public http://os-controller:8778
	$ openstack endpoint create --region RegionOne placement internal http://os-controller:8778
	$ openstack endpoint create --region RegionOne placement admin http://os-controller:8778
	
Configure the settings:
	
	$ dnf install openstack-nova-api openstack-nova-conductor openstack-nova-console openstack-nova-novncproxy openstack-nova-scheduler openstack-nova-placement-api
	$ grep -vE '^$|^#' /etc/nova/nova.conf
	[DEFAULT]
	my_ip=192.168.1.121
	use_neutron=true
	firewall_driver=nova.virt.firewall.NoopFirewallDriver
	enabled_apis=osapi_compute,metadata
	transport_url = rabbit://openstack:secret@192.168.1.121
	[api]
	auth_strategy=keystone
	[api_database]
	connection = mysql+pymysql://nova:secret@192.168.1.121/nova_api
	[barbican]
	[cache]
	[cells]
	[cinder]
	[cloudpipe]
	[conductor]
	[console]
	[consoleauth]
	[cors]
	[cors.subdomain]
	[crypto]
	[database]
	connection = mysql+pymysql://nova:secret@192.168.1.121/nova
	[ephemeral_storage_encryption]
	[filter_scheduler]
	[glance]
	api_servers=http://os-controller:9292
	[guestfs]
	[healthcheck]
	[hyperv]
	[image_file_url]
	[ironic]
	[key_manager]
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = nova
	password = secret
	[libvirt]
	[matchmaker_redis]
	[metrics]
	[mks]
	[neutron]
	url = http://os-controller:9696
	auth_url = http://os-controller:35357
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	region_name = RegionOne
	project_name = service
	username = neutron
	password = secret
	service_metadata_proxy = true
	metadata_proxy_shared_secret = secret
	[notifications]
	[osapi_v21]
	[oslo_concurrency]
	lock_path=/var/lib/nova/tmp
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[pci]
	[placement]
	os_region_name = RegionOne
	project_domain_name = Default
	project_name = service
	auth_type = password
	user_domain_name = Default
	auth_url = http://os-controller:35357/v3
	username = placement
	password = secret
	[quota]
	[rdp]
	[remote_debug]
	[scheduler]
	discover_hosts_in_cells_interval=300
	[serial_console]
	[service_user]
	[spice]
	[ssl]
	[trusted_computing]
	[upgrade_levels]
	[vendordata_dynamic_auth]
	[vmware]
	[vnc]
	enabled=true
	vncserver_listen=$my_ip
	vncserver_proxyclient_address=$my_ip
	[workarounds]
	[wsgi]
	[xenserver]
	[xvp]
	$ vi /etc/httpd/conf.d/00-nova-placement-api.conf
	---
	<Directory /usr/bin>
	   <IfVersion >= 2.4>
	      Require all granted
	   </IfVersion>
	   <IfVersion < 2.4>
	      Order allow,deny
	      Allow from all
	   </IfVersion>
	</Directory>
	---
	$ systemctl restart httpd
	
Sync to DB:
	
	$ su -s /bin/sh -c "nova-manage api_db sync" nova
	$ su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
	$ su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
	$ su -s /bin/sh -c "nova-manage db sync" nova
	$ nova-manage cell_v2 list_cells
	
Enable and start the Service:

	$ systemctl enable openstack-nova-api.service   openstack-nova-consoleauth.service openstack-nova-scheduler.service   openstack-nova-conductor.service openstack-nova-novncproxy.service
	$ systemctl start openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service

#### Configure Networking Service (Neutron)
Prepare the DB:

	$ mysql -u root -p
	MariaDB [(none)] CREATE DATABASE neutron;
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'secret';
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'secret';
	
Create user and endpoints:

	$ . admin-setup
	$ openstack user create --domain default --password-prompt neutron
	$ openstack role add --project service --user neutron admin
	$ openstack endpoint create --region RegionOne network public http://os-controller:9696
	$ openstack endpoint create --region RegionOne network internal http://os-controller:9696
	$ openstack endpoint create --region RegionOne network admin http://os-controller:9696
	
Configure the settings files (I decided to use VXLAN with LinuxBridge... I thought using OVS for a lab setup is a bit of an overkill):
	
	$ dnf install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge ebtables
	$ grep -vE '^$|^#' /etc/neutron/neutron.conf 
	auth_strategy = keystone
	core_plugin = ml2
	service_plugins = router
	allow_overlapping_ips = True
	notify_nova_on_port_status_changes = true
	notify_nova_on_port_data_changes = true
	transport_url = rabbit://openstack:secret@192.168.1.121
	[agent]
	[cors]
	[cors.subdomain]
	[database]
	connection = mysql+pymysql://neutron:secret@192.168.1.121/neutron
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = neutron
	password = secret
	[matchmaker_redis]
	[nova]
	auth_url = http://os-controller:35357
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	region_name = RegionOne
	project_name = service
	username = nova
	password = secret
	[oslo_concurrency]
	lock_path = /var/lib/neutron/tmp
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[qos]
	[quotas]
	[ssl]
	$ grep -vE '^$|^#' /etc/neutron/plugins/ml2/ml2_conf.ini
	[DEFAULT]
	[ml2]
	type_drivers = flat,vlan,vxlan
	tenant_network_types = vxlan
	mechanism_drivers = linuxbridge,l2population
	extension_drivers = port_security
	[ml2_type_flat]
	flat_networks = provider
	[ml2_type_geneve]
	[ml2_type_gre]
	[ml2_type_vlan]
	[ml2_type_vxlan]
	vni_ranges = 1:1000
	[securitygroup]
	enable_ipset = true
	$ grep -vE '^$|^#' /etc/neutron/plugins/ml2/linuxbridge_agent.ini
	[DEFAULT]
	[agent]
	[linux_bridge]
	physical_interface_mappings = provider:ens192
	[securitygroup]
	firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
	enable_security_group = true
	[vxlan]
	enable_vxlan = true
	local_ip = 10.0.0.10
	l2_population = true
	$ grep -vE '^$|^#' /etc/neutron/l3_agent.ini
	[DEFAULT]
	interface_driver = linuxbridge
	[agent]
	[ovs]
	$ grep -vE '^$|^#' /etc/neutron/dhcp_agent.ini
	[DEFAULT]
	interface_driver = linuxbridge
	dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
	enable_isolated_metadata = true
	[agent]
	[ovs]
	$  grep -vE '^$|^#' /etc/neutron/metadata_agent.ini
	[DEFAULT]
	nova_metadata_ip = 192.168.1.121
	metadata_proxy_shared_secret = secret
	[agent]
	[cache]
	$ ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
	
Sync to DB:
	
	$ su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
	
Enable and start the service:
	
	$ systemctl restart openstack-nova-api.service
	$ systemctl enable neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
	$ systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
	$ systemctl enable neutron-l3-agent.service
	$ systemctl start neutron-l3-agent.service
	
#### Install Dashboard (Horizon)
Install the package:

	$ dnf install openstack-dashboard

Configure the settings file:

	$ vi /etc/openstack-dashboard/local_settings
	---
	import os
	from django.utils.translation import ugettext_lazy as _
	from openstack_dashboard.settings import HORIZON_CONFIG
	DEBUG = False
	WEBROOT = '/dashboard/'
	ALLOWED_HOSTS = ['*']
	OPENSTACK_API_VERSIONS = {
	    "identity": 3,
	    "image": 2,
	    "volume": 2,
	}
	OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
	OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'
	LOCAL_PATH = '/tmp'
	SECRET_KEY='f220f91135ddfa5d048b'
	SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
	CACHES = {
	    'default': {
	         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	         'LOCATION': 'os-controller:11211',
	    }
	}
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	OPENSTACK_HOST = "os-controller.kar.int"
	OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST
	OPENSTACK_KEYSTONE_DEFAULT_ROLE = "user"
	OPENSTACK_KEYSTONE_BACKEND = {
	    'name': 'native',
	    'can_edit_user': True,
	    'can_edit_group': True,
	    'can_edit_project': True,
	    'can_edit_domain': True,
	    'can_edit_role': True,
	}
	OPENSTACK_NEUTRON_NETWORK = {
    'enable_router': True,
    'enable_quotas': True,
    'enable_ipv6': True,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_lb': True,
    'enable_firewall': True,
    'enable_vpn': True,
	---
	
Restart the necessary service to apply the settings:

	$ systemctl restart httpd.service memcached.service

You can now login to the demo project and check out some settings:

![openstack-dashboard](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/openstack-dashboard.png&raw=1)
	
And that should be it for the *controller* node. Now it has the following services configured on it:

* Identity Service (Keystone)
* Image Service (Glance)
* Compute Service (Nova)
* Networking Service (Neutron)
* Dashboard (Horizon)


### OpenStack Compute Node
Here are the steps I took on the *compute* Node.

#### Configure OS Networking
Same setup as on the *controller* node:

	$ systemctl disable NetworkManager
	$ systemctl enable network
	$ vi /etc/sysconfig/network-scripts/ifcfg-ens192
	$ vi /etc/sysconfig/network-scripts/ifcfg-ens224
	$ dnf remove firewalld
	$ dnf install iptables-services
	$ systemctl enable iptables
	$vi /etc/sysconfig/iptables
	$ systemctl start iptables

Don't forget to configure NTP:
	
	$ dnf install chrony
	$ chronyc sources

#### OpenStack Repo
I just installed the repo and went from there:
	
	$ dnf install https://rdoproject.org/repos/rdo-release.rpm
	$ dnf upgrade
	$ dnf install python-openstackclient
	
#### Configure the Compute Service

On the *compute* node had to downgrade **iptables** due to a package dependency issue: [Bug 1327786 - iptables-services should not Provide "iptables"](https://bugzilla.redhat.com/show_bug.cgi?id=1327786)

	$ dnf install iptables-1.6.0-2.fc25 --allowerasing
	$ dnf install iptables-services-1.6.0-2.fc25

Also had to disable **selinux** for the LinuxBridge agent: [Neutron failed to spawn rootwrap process Bug #1572322](https://bugs.launchpad.net/neutron/+bug/1572322). After that was able to install the package:

	$ dnf install openstack-nova-compute

Then configured the service:

	$ grep -vE '^$|^#' /etc/nova/nova.conf
	[DEFAULT]
	my_ip=192.168.1.122
	use_neutron=true
	firewall_driver=nova.virt.firewall.NoopFirewallDriver
	enabled_apis=osapi_compute,metadata
	transport_url=rabbit://openstack:secret@192.168.1.121
	[api]
	auth_strategy=keystone
	[api_database]
	[barbican]
	[cache]
	[cells]
	[cinder]
	[cloudpipe]
	[conductor]
	[console]
	[consoleauth]
	[cors]
	[cors.subdomain]
	[crypto]
	[database]
	[ephemeral_storage_encryption]
	[filter_scheduler]
	[glance]
	api_servers=http://os-controller:9292
	[guestfs]
	[healthcheck]
	[hyperv]
	[image_file_url]
	[ironic]
	[key_manager]
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = nova
	password = secret
	[libvirt]
	virt_type=qemu
	cpu_mode=none
	[matchmaker_redis]
	[metrics]
	[mks]
	[neutron]
	url = http://os-controller:9696
	auth_url = http://os-controller:35357
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	region_name = RegionOne
	project_name = service
	username = neutron
	password = secret
	[notifications]
	[osapi_v21]
	[oslo_concurrency]
	lock_path=/var/lib/nova/tmp
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[pci]
	[placement]
	os_region_name = RegionOne
	project_domain_name = Default
	project_name = service
	auth_type = password
	user_domain_name = Default
	auth_url = http://os-controller:35357/v3
	username = placement
	password = secret
	[quota]
	[rdp]
	[remote_debug]
	[scheduler]
	[serial_console]
	[service_user]
	[spice]
	[ssl]
	[trusted_computing]
	[upgrade_levels]
	[vendordata_dynamic_auth]
	[vmware]
	[vnc]
	enabled=true
	vncserver_listen=0.0.0.0
	vncserver_proxyclient_address=$my_ip
	novncproxy_base_url=http://192.168.1.121:6080/vnc_auto.html
	[workarounds]
	[wsgi]
	[xenserver]
	[xvp]

Then enable and start the service:

	$ systemctl enable libvirtd.service openstack-nova-compute.service
	$ systemctl start libvirtd.service openstack-nova-compute.service

#### Configure Network Service (Neutron)
First install the necessary packages:

	$ dnf install openstack-neutron-linuxbridge ebtables ipset

Then configure all the setting files:

	$ grep -vE '^$|^#' /etc/neutron/neutron.conf
	[DEFAULT]
	auth_strategy = keystone
	transport_url = rabbit://openstack:secret@192.168.1.121
	[agent]
	[cors]
	[cors.subdomain]
	[database]
	[keystone_authtoken]
	auth_uri = http://os-controller:5000
	auth_url = http://os-controller:35357
	memcached_servers = os-controller:11211
	auth_type = secret
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = neutron
	password = secret
	[matchmaker_redis]
	[nova]
	[oslo_concurrency]
	lock_path = /var/lib/neutron/tmp
	[oslo_messaging_amqp]
	[oslo_messaging_kafka]
	[oslo_messaging_notifications]
	[oslo_messaging_rabbit]
	[oslo_messaging_zmq]
	[oslo_middleware]
	[oslo_policy]
	[qos]
	[quotas]
	[ssl]
	$ grep -vE '^$|^#' /etc/neutron/plugins/ml2/linuxbridge_agent.ini
	[DEFAULT]
	[agent]
	[linux_bridge]
	physical_interface_mappings = provider:ens192
	[securitygroup]
	enable_security_group = true
	[vxlan]
	enable_vxlan = true
	local_ip = 10.0.0.11
	l2_population = true
	
Then enable and start the service:

	$ systemctl enable neutron-linuxbridge-agent.service
	$ systemctl start neutron-linuxbridge-agent.service

You might have to restart the *compute* service as well:

	$ systemctl restart openstack-nova-compute.service

### Confirm all the Services are available
So after all the services are configured, you should have a **hypervisor** available:

	[root@os-controller ~]# openstack hypervisor list
	+----+---------------------+-----------------+---------------+-------+
	| ID | Hypervisor Hostname | Hypervisor Type | Host IP       | State |
	+----+---------------------+-----------------+---------------+-------+
	|  1 | os-compute.kar.int  | QEMU            | 192.168.1.122 | up    |
	+----+---------------------+-----------------+---------------+-------+

And you should have all your **neutron** components connected. I decided to try out the **self-service** network:

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

And you should have your *compute* (**nova**) service connected:

	[root@os-controller ~]# openstack compute service list
	+----+------------------+-----------------------+----------+---------+-------+----------------------------+
	| ID | Binary           | Host                  | Zone     | Status  | State | Updated At                 |
	+----+------------------+-----------------------+----------+---------+-------+----------------------------+
	|  1 | nova-consoleauth | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:26.000000 |
	|  2 | nova-scheduler   | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:26.000000 |
	|  3 | nova-conductor   | os-controller.kar.int | internal | enabled | up    | 2017-06-21T15:55:27.000000 |
	|  8 | nova-compute     | os-compute.kar.int    | nova     | enabled | up    | 2017-06-21T15:55:29.000000 |
	+----+------------------+-----------------------+----------+---------+-------+----------------------------+

And throughout the guide you should have imported a test image into your **glance** image service:

	[root@os-controller ~]# openstack image list
	+--------------------------------------+--------+--------+
	| ID                                   | Name   | Status |
	+--------------------------------------+--------+--------+
	| f71063a9-7865-4b10-9216-b213b44f5073 | cirros | active |
	+--------------------------------------+--------+--------+

You should also have a bunch of endpoints used for various services:

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

### Launch an Instance in OpenStack
This is broken down into a couple of steps. 

#### Prepare OpenStack Networking
First create a **provider** network (this is done with the **admin** user):
	
	[root@os-controller ~]# . admin-setup
	[root@os-controller ~]# openstack network create  --share --external \
	>   --provider-physical-network provider \
	>   --provider-network-type flat provider

Next, create a subnet that is on the **provider** network:
	
	[root@os-controller ~]# openstack subnet create --network provider \
	>   --allocation-pool start=10.0.0.100,end=10.0.0.120 \
	>   --dns-nameserver 10.0.0.1 --gateway 10.0.0.1 \
	>   --subnet-range 10.0.0.0/24 provider
	
Next create your **self-service** network (this is done with the **demo** user):

	[root@os-controller ~]# . demo-setup
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


Then create a subnet for the **self-service** network:

	[root@os-controller ~]# openstack subnet create --network selfservice \
	>   --dns-nameserver 10.0.0.1 --gateway 172.16.1.1 \
	>   --subnet-range 172.16.1.0/24 selfservice

Next let's create a **router** which will connect the **self-service** network through the **provider** network:

	[root@os-controller ~]# openstack router create router

Next let's add the **self-service** network as an interface in the **router**:

	[root@os-controller ~]# neutron router-interface-add router selfservice
	neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
	Added interface c10e45dc-806f-4bde-af26-3207b4352cf2 to router router.

And lastly set the gateway for the router:

	[root@os-controller ~]# neutron router-gateway-set router provider
	neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
	Set gateway for router router

At this point your should see 3 **network namespaces**:

	[root@os-controller ~]# ip netns
	qrouter-f84d21b1-c643-445a-87fb-b908b437f459 (id: 2)
	qdhcp-bec99697-2bb8-448a-b1d5-80f73cca4654 (id: 1)
	qdhcp-addf3eeb-ef5d-4222-9cbe-ecd8e782702a (id: 0)

And you can list the ports used on the **router**:

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

And you will have two **network**s defined:

	[root@os-controller ~]# openstack network list
	+--------------------------------------+-------------+--------------------------------------+
	| ID                                   | Name        | Subnets                              |
	+--------------------------------------+-------------+--------------------------------------+
	| addf3eeb-ef5d-4222-9cbe-ecd8e782702a | provider    | 9fdb2fe2-79e6-4224-9395-fda93c0fe6d9 |
	| bec99697-2bb8-448a-b1d5-80f73cca4654 | selfservice | 19b55184-71f6-4fab-b6da-2309dd7f0de9 |
	+--------------------------------------+-------------+--------------------------------------+

After that, initially I was failing to **ping** and I saw this:

	[root@os-compute ~]# ping 10.0.0.104
	PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
	From 10.0.0.10 icmp_seq=1 Destination Host Prohibited
	From 10.0.0.10 icmp_seq=2 Destination Host Prohibited
	From 10.0.0.10 icmp_seq=3 Destination Host Prohibited
	^C
	--- 10.0.0.104 ping statistics ---
	3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2072ms

Since I was getting "Host Prohibited" I was guessing it was a firewall issue. From inside the **router** it worked;

	[root@os-controller ~]# ip netns exec qrouter-f84d21b1-c643-445a-87fb-b908b437f459 ping 10.0.0.104
	PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
	64 bytes from 10.0.0.104: icmp_seq=1 ttl=64 time=0.033 ms
	64 bytes from 10.0.0.104: icmp_seq=2 ttl=64 time=0.025 ms
	^C
	--- 10.0.0.104 ping statistics ---
	2 packets transmitted, 2 received, 0% packet loss, time 1009ms
	rtt min/avg/max/mdev = 0.025/0.029/0.033/0.004 ms

I then ran into this bug: [Bug 1191536 - Network traffic from overcloud to internet/outside is blocked by undercloud’s iptables filter](https://bugzilla.redhat.com/show_bug.cgi?id=1191536). And for the workaround I tried this:

	$ iptables -I FORWARD 2 -s 10.0.0.0/24 -j ACCEPT -m comment --comment test

and then the **ping** started working:

	[root@os-compute ~]# ping -c 2 10.0.0.104
	PING 10.0.0.104 (10.0.0.104) 56(84) bytes of data.
	64 bytes from 10.0.0.104: icmp_seq=1 ttl=64 time=0.146 ms
	64 bytes from 10.0.0.104: icmp_seq=2 ttl=64 time=0.156 ms
	
	--- 10.0.0.104 ping statistics ---
	2 packets transmitted, 2 received, 0% packet loss, time 1046ms
	rtt min/avg/max/mdev = 0.146/0.151/0.156/0.005 ms

#### Create an Instance Flavor
Next let's create a small VM **flavor**:

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

#### Create SSH Key Pair
And let's create an SSH key pair and upload it to OpenStack:

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

#### Open up Security Groups
Next let's allow **ICMP** and **SSH** to the instance:

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

#### Launching the Instance
To launch the instance, we can get all the details first. Get the list of **flavor**s:

	[root@os-controller ~]# . demo-setup
	[root@os-controller ~]# openstack flavor list
	+----+---------+-----+------+-----------+-------+-----------+
	| ID | Name    | RAM | Disk | Ephemeral | VCPUs | Is Public |
	+----+---------+-----+------+-----------+-------+-----------+
	| 0  | m1.nano |  64 |    1 |         0 |     1 | True      |
	+----+---------+-----+------+-----------+-------+-----------+

List the available **image**s:

	[root@os-controller ~]# openstack image list
	+--------------------------------------+--------+--------+
	| ID                                   | Name   | Status |
	+--------------------------------------+--------+--------+
	| f71063a9-7865-4b10-9216-b213b44f5073 | cirros | active |
	+--------------------------------------+--------+--------+

List the available **network**s:

	[root@os-controller ~]# openstack network list                                                                             	+--------------------------------------+-------------+--------------------------------------+
	| ID                                   | Name        | Subnets                              |
	+--------------------------------------+-------------+--------------------------------------+
	| addf3eeb-ef5d-4222-9cbe-ecd8e782702a | provider    | 9fdb2fe2-79e6-4224-9395-fda93c0fe6d9 |
	| dc61d555-2a0f-44e6-873c-db4c108915f3 | selfservice | 152cfc92-e1ba-428f-93d9-a729fc6ec83a |
	+--------------------------------------+-------------+--------------------------------------+
	
Then list the **security group**s:

	[root@os-controller ~]# openstack security group list
	+--------------------------------------+---------+------------------------+---------+
	| ID                                   | Name    | Description            | Project |
	+--------------------------------------+---------+------------------------+---------+
	| 89779c12-7b39-4357-86c4-642fd40f9048 | default | Default security group |         |
	+--------------------------------------+---------+------------------------+---------+

And now that we have all the information, let's deploy our instance:

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

If all is well you should the VM as **ACTIVE**:

	[root@os-controller ~]# openstack server list
	+------------------+------------------+--------+------------------+------------+
	| ID               | Name             | Status | Networks         | Image Name |
	+------------------+------------------+--------+------------------+------------+
	| 5c923055-37a8-4b | selfservice-     | ACTIVE | selfservice=172. | cirros     |
	| 82-a329-869c4d8f | instance         |        | 16.1.5           |            |
	| efd4             |                  |        |                  |            |
	+------------------+------------------+--------+------------------+------------+

If you get an ERROR status, check out the logs under **/var/log/nova** to see why it might not have started. You will also see the VM started in **libvirtd**:

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

![vnc-to-vm](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/vnc-to-vm.png&raw=1)

I noticed that I couldn't **ping** the default gw from the VM. Here is what I saw on the compute node:

	[root@os-compute neutron]# tcpdump -i any -nne icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on any, link-type LINUX_SLL (Linux cooked), capture size 262144 bytes
	21:54:39.632390  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	21:54:40.625319  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	21:54:41.625206  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86

It looks like another **iptables** issue. I deleted the default **REJECT** rule on the **INPUT** chain and the **ping**s started working:

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

Here is the **tcpdump** as the issue is fixed:

	22:07:21.005258  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	22:07:22.005387  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	22:07:51.224434  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	22:07:52.221343  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	22:07:53.221241  In 00:0c:29:50:e3:d3 ethertype IPv4 (0x0800), length 122: 10.0.0.10 > 10.0.0.11: ICMP host 10.0.0.10 unreachable - admin prohibited, length 86
	22:09:57.027575   P fa:16:3e:37:74:b4 ethertype IPv4 (0x0800), length 100: 172.16.1.10 > 172.16.1.1: ICMP echo request, id 40449, seq 0, length 64
	22:09:57.027624 Out fa:16:3e:37:74:b4 ethertype IPv4 (0x0800), length 100: 172.16.1.10 > 172.16.1.1: ICMP echo request, id 40449, seq 0, length 64
	22:09:57.027768   P fa:16:3e:f3:01:8e ethertype IPv4 (0x0800), length 100: 172.16.1.1 > 172.16.1.10: ICMP echo reply, id 40449, seq 0, length 64
	22:09:57.027774 Out fa:16:3e:f3:01:8e ethertype IPv4 (0x0800), length 100: 172.16.1.1 > 172.16.1.10: ICMP echo reply, id 40449, seq 0, length 64

And after another reboot of the VM, it was able to get an address with DHCP:

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


And I was able to **ping** it from the **router**:

	[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c ping -c 1 172.16.1.10
	PING 172.16.1.10 (172.16.1.10) 56(84) bytes of data.
	64 bytes from 172.16.1.10: icmp_seq=1 ttl=64 time=5.19 ms
	
	--- 172.16.1.10 ping statistics ---
	1 packets transmitted, 1 received, 0% packet loss, time 0ms
	rtt min/avg/max/mdev = 5.194/5.194/5.194/0.000 ms

As a final test let's create a floating IP, which is covered [here](https://docs.openstack.org/user-guide/cli-manage-ip-addresses.html):

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

Confirm it's added:

	[root@os-controller ~]# openstack floating ip list
	+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+
	| ID                                 | Floating IP Address | Fixed IP Address | Port | Floating Network                   | Project                          |
	+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+
	| 8a8cd86e-                          | 10.0.0.109          | None             | None | addf3eeb-ef5d-4222-9cbe-           | 76315fbcf38f430199b6153da2e6d5b1 |
	| bb58-45a1-8af9-e1e9dbcf5cd2        |                     |                  |      | ecd8e782702a                       |                                  |
	+------------------------------------+---------------------+------------------+------+------------------------------------+----------------------------------+

Then add the floating IP to the test instance:

	[root@os-controller ~]# openstack server add floating ip selfservice-instance 10.0.0.109

And you should see that IP listed for the VM:

	[root@os-controller ~]# openstack server list
	+--------------------------------------+----------------------+--------+-------------------------------------+------------+
	| ID                                   | Name                 | Status | Networks                            | Image Name |
	+--------------------------------------+----------------------+--------+-------------------------------------+------------+
	| 4a3be61d-2350-4304-bbf7-657083cc6ccb | selfservice-instance | ACTIVE | selfservice=172.16.1.10, 10.0.0.109 | cirros     |
	+--------------------------------------+----------------------+--------+-------------------------------------+------------+

Now login from a machine that has access to the **provider** network:

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
When my **ping**s weren't working, I started looking into the flow of the traffic in OpenStack. These sites have good examples:

* [Network Troubleshooting](https://docs.openstack.org/ops-guide/ops-network-troubleshooting.html)
* [Linux bridge: Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html)
* [Networking in too much detail](https://www.rdoproject.org/networking/networking-in-too-much-detail/)
* [Scenario 2: Network host config](http://docs.ocselected.org/openstack-manuals/kilo/networking-guide/content/under_the_hood_linuxbridge_scenario2_network.html)

Let's track down the flow from [their example](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html#north-south-scenario-1-instance-with-a-fixed-ip-address):

![lb-vni-traffic-flow](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/lb-vni-traffic-flow.png&raw=1)

Here is a nice overview of the components as well:

![os-network-components](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/os-network-components.png&raw=1)

### On the Compute Node
Here are the networking functions that occur on the *compute* node. 

#### 1. Instance Sends Packet to LinuxBridge
From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> 1. The instance interface (1) forwards the packet to the self-service bridge instance port (2) via veth pair.

From the [Network Troubleshooting](https://docs.openstack.org/ops-guide/ops-network-troubleshooting.html) page:

> The packet transfers to a Test Access Point (TAP) device on the compute host, such as tap690466bc-92. You can find out what TAP is being used by looking at the /etc/libvirt/qemu/instance-xxxxxxxx.xml file.

Checking out that file, here is what I saw:

	# grep bridge\' /etc/libvirt/qemu/instance-00000003.xml  -A 7
	    <interface type='bridge'>
	      <mac address='fa:16:3e:37:74:b4'/>
	      <source bridge='brqdc61d555-2a'/>
	      <target dev='tap89bce4c6-b0'/>
	      <model type='virtio'/>
	      <driver name='qemu'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
	    </interface>

it looks like we on a *tap* device (**tap89bce4c6-b0**) and it's on the following bridge (**brqdc61d555-2a**). To confirm it gets to the **tap** interface let's do a packet capture there:

	[root@os-compute ~]# tcpdump -i tap89bce4c6-b0 icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on tap89bce4c6-b0, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:20:15.295420 IP 172.16.1.10 > 10.0.0.1: ICMP echo request, id 48129, seq 0, length 64
	12:20:15.295922 IP 10.0.0.1 > 172.16.1.10: ICMP echo reply, id 48129, seq 0, length 64


And the **bridge**:

	[root@os-compute ~]# tcpdump -i brqdc61d555-2a icmp -nne
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on brqdc61d555-2a, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:20:52.059779 fa:16:3e:37:74:b4 > fa:16:3e:f3:01:8e, ethertype IPv4 (0x0800), length 98: 172.16.1.10 > 10.0.0.1: ICMP echo request, id 48385, seq 0, length 64
	12:20:52.060144 fa:16:3e:f3:01:8e > fa:16:3e:37:74:b4, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 172.16.1.10: ICMP echo reply, id 48385, seq 0, length 64


#### 2. Security Groups Handle Firewalling
From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> 2. Security group rules (3) on the self-service bridge handle firewalling and connection tracking for the packet.

I saw the following chain created:

	[root@os-compute ~]# iptables -L nova-compute-FORWARD -v -n
	Chain nova-compute-FORWARD (1 references)
	 pkts bytes target     prot opt in     out     source               destination 
	 1682  185K ACCEPT     all  --  brqdc61d555-2a *       0.0.0.0/0            0.0.0.0/0
	    0     0 ACCEPT     all  --  *      brqdc61d555-2a  0.0.0.0/0            0.0.0.0/0

Which allowed all the instances to be be forwarded on the bridge.

#### 3. The Internal bridge forwards the packet to the VXLAN interface

From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> The self-service bridge forwards the packet to the VXLAN interface (4) which wraps the packet using VNI 101.

Since I was using VXLAN I also noticed that I had an interface for VXLAN traffic (notice the **vxlan id**):

	[root@os-compute ~]# ip -d link show vxlan-58
	7: vxlan-58: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brqdc61d555-2a state UNKNOWN mode DEFAULT group default qlen 1000
	    link/ether 8a:e2:39:3d:0e:d7 brd ff:ff:ff:ff:ff:ff promiscuity 1
	    vxlan id 58 dev ens192 srcport 0 0 dstport 8472 ageing 300 udpcsum noudp6zerocsumtx noudp6zerocsumrx
	    bridge_slave state forwarding priority 32 cost 100 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8002 port_no 0x2 designated_port 32770 designated_cost 0 designated_bridge 8000.8a:e2:39:3d:e:d7 designated_root 8000.8a:e2:39:3d:e:d7 hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535

and it was part of the same bridge that the **tap** interface was on:

	[root@os-compute ~]# brctl show
	bridge name     bridge id               STP enabled     interfaces
	brqdc61d555-2a          8000.8ae2393d0ed7       no      tap89bce4c6-b0
	                                                        vxlan-58

Since we are using VXLAN, we can filter out VXLAN type of traffic with **tcpdump** and make sure it still shows up:

	[root@os-compute ~]# tcpdump -i vxlan-58 -nne -T vxlan icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on vxlan-58, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:21:30.410347 fa:16:3e:37:74:b4 > fa:16:3e:f3:01:8e, ethertype IPv4 (0x0800), length 98: 172.16.1.10 > 10.0.0.1: ICMP echo request, id 48641, seq 0, length 64
	12:21:30.410714 fa:16:3e:f3:01:8e > fa:16:3e:37:74:b4, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 172.16.1.10: ICMP echo reply, id 48641, seq 0, length 64

#### 4. Physical NIC forwards traffic using the overlay VXLAN network
From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> 4. The underlying physical interface (5) for the VXLAN interface forwards the packet to the network node via the overlay network (6).

	[root@os-compute ~]# tcpdump -i ens192 -nne  -T vxlan icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on ens192, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:10:51.121143 fa:16:3e:2e:bb:7b > 78:24:af:7b:1f:08, ethertype IPv4 (0x0800), length 98: 10.0.0.109 > 10.0.0.1: ICMP echo request, id 47361, seq 0, length 64
	12:10:51.121318 78:24:af:7b:1f:08 > fa:16:3e:2e:bb:7b, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 10.0.0.109: ICMP echo reply, id 47361, seq 0, length 64
	
Notice the internal IP of the VM **172.16.1.10** isn't seen on the physical NIC. We can use the **Decode As** feature with wireshark. After you choose the UDP traffic and **decode** it as VXLAN, you will see the following:

![vxlan-wireshark](https://seacloud.cc/d/480b5e8fcd/files/?p=/openstack-manual-fedora/vxlan-wireshark.png&raw=1)

Or we can also use **tshark**, here is the frame without being decoded:

    <> tshark  -r file.pcap "frame.number==17" 
       17   0.348712    10.0.0.11 → 10.0.0.10    UDP 148 42053 → 8472 Len=106
   
And we can see that the actual traffic is ICMP traffic after we **Decode As** VXLAN:

    <> tshark  -d udp.port==8472,vxlan -r file.pcap "frame.number==17"   
       17   0.348712  172.16.1.10 → 10.0.0.1     ICMP 148 Echo (ping) request  id=0xdd01, seq=0/0, ttl=64

We can also see in the wireshark that the **VNI** is set as **58**, which is the correct value. Lastly if we just check using **tcpdump**, we will see it as **OTV overlay**:

    20:54:24.152996 00:0c:29:77:3b:df > 00:0c:29:50:e3:d3, ethertype IPv4 (0x0800), length 148: (tos 0x0, ttl 64, id 42979, offset 0, flags [none], proto UDP (17), length 134)
        10.0.0.11.42053 > 10.0.0.10.8472: OTV, flags [I] (0x08), overlay 0, instance 58
    fa:16:3e:37:74:b4 > fa:16:3e:f3:01:8e, ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 54278, offset 0, flags [DF], proto ICMP (1), length 84)
        172.16.1.10 > 10.0.0.1: ICMP echo request, id 56577, seq 0, length 64

And we can see that the **instance** is labeled as **58**.

### On the Network/Controller Node
Next we can move on to the *controller* node (since my *controller* node is also acting as the *network* node).

#### 1. Physical NIC Receives Overlay VXLAN Traffic
From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> The underlying physical interface (7) for the VXLAN interface forwards the packet to the VXLAN interface (8) which unwraps the packet.

So we can see the packets come in on the physical NIC:

	[root@os-controller ~]# tcpdump -i ens192 -T vxlan -nne icmp and not host kerch
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on ens192, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:17:56.927969 fa:16:3e:2e:bb:7b > 78:24:af:7b:1f:08, ethertype IPv4 (0x0800), length 98: 10.0.0.109 > 10.0.0.1: ICMP echo request, id 47617, seq 0, length 64
	12:17:56.928196 78:24:af:7b:1f:08 > fa:16:3e:2e:bb:7b, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 10.0.0.109: ICMP echo reply, id 47617, seq 0, length 64

And that also get passed to the VXLAN inteface:

	[root@os-controller ~]# tcpdump -i vxlan-58 -T vxlan -nne icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on vxlan-58, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:18:44.122663 fa:16:3e:37:74:b4 > fa:16:3e:f3:01:8e, ethertype IPv4 (0x0800), length 98: 172.16.1.10 > 10.0.0.1: ICMP echo request, id 47873, seq 0, length 64
	12:18:44.123053 fa:16:3e:f3:01:8e > fa:16:3e:37:74:b4, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 172.16.1.10: ICMP echo reply, id 47873, seq 0, length 64

Notice the VXLAN interface forwards the traffic to the internal IP **172.16.1.10** IP of the VM.

#### 2. The Internal bridge forwards the packet to the network interface of the router namespace.

From [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> 2. The self-service bridge router port (9) forwards the packet to the self-service network interface (10) in the router namespace.

From the [Network Troubleshooting](https://docs.openstack.org/ops-guide/ops-network-troubleshooting.html) page:

> 7. The packet then makes it to the l3-agent. This is actually another TAP device within the router’s network namespace. Router namespaces are named in the form qrouter-<router-uuid>. Running 'ip a' within the namespace will show the TAP device name, qr-e6256f7d-31 in this example:


You can check out the namespaces by using `ip netns`. I had the following:

	[root@os-controller ~]# ip netns
	qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c (id: 2)
	qdhcp-dc61d555-2a0f-44e6-873c-db4c108915f3 (id: 1)
	qdhcp-addf3eeb-ef5d-4222-9cbe-ecd8e782702a (id: 0)

You can check out the interfaces in the **router** namespace like so:

	[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c ip a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
	    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	    inet6 ::1/128 scope host
	       valid_lft forever preferred_lft forever
	2: qr-745bc525-6f@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000
	    link/ether fa:16:3e:f3:01:8e brd ff:ff:ff:ff:ff:ff link-netnsid 0
	    inet 172.16.1.1/24 brd 172.16.1.255 scope global qr-745bc525-6f
	       valid_lft forever preferred_lft forever
	    inet6 fe80::f816:3eff:fef3:18e/64 scope link
	       valid_lft forever preferred_lft forever
	3: qg-191d5c4f-cc@if11: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
	    link/ether fa:16:3e:2e:bb:7b brd ff:ff:ff:ff:ff:ff link-netnsid 0
	    inet 10.0.0.108/24 brd 10.0.0.255 scope global qg-191d5c4f-cc
	       valid_lft forever preferred_lft forever
	    inet 10.0.0.109/32 brd 10.0.0.109 scope global qg-191d5c4f-cc
	       valid_lft forever preferred_lft forever
	    inet6 fe80::f816:3eff:fe2e:bb7b/64 scope link
	       valid_lft forever preferred_lft forever
	       
The **qr-** interface is the default gateway for the internal network, it sees all the traffic as well:

	[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c tcpdump -i qr-745bc525-6f not port ssh -nne
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on qr-745bc525-6f, link-type EN10MB (Ethernet), capture size 262144 bytes
	12:33:35.968778 fa:16:3e:37:74:b4 > fa:16:3e:f3:01:8e, ethertype IPv4 (0x0800), length 98: 172.16.1.10 > 10.0.0.1: ICMP echo request, id 49665, seq 0, length 64
	12:33:35.969001 fa:16:3e:f3:01:8e > fa:16:3e:37:74:b4, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 172.16.1.10: ICMP echo reply, id 49665, seq 0, length 64

and from the same [Network Troubleshooting](https://docs.openstack.org/ops-guide/ops-network-troubleshooting.html) page:

> The qg-<n> interface in the l3-agent router namespace sends the packet on to its next hop through physical device.

The IP of **10.0.0.9** is the floating IP that I assigned to my test VM. Here is more information on the step:

> For IPv4, the router performs SNAT on the packet which changes the source IP address to the router IP address on the provider network and sends it to the gateway IP address on the provider network via the gateway interface on the provider network (11).

We can also checkout the **iptables** configuration of the namespace **router**:

	[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c iptables -L neutron-l3-agent-OUTPUT -n -v -t nat
	Chain neutron-l3-agent-OUTPUT (1 references)
	 pkts bytes target     prot opt in     out     source               destination 
	    0     0 DNAT       all  --  *      *       0.0.0.0/0            10.0.0.109           to:172.16.1.10
	    
	    [root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c iptables -L neutron-l3-agent-PREROUTING -n -v -t nat
	Chain neutron-l3-agent-PREROUTING (1 references)
	 pkts bytes target     prot opt in     out     source               destination 
	   16   960 REDIRECT   tcp  --  qr-+   *       0.0.0.0/0            169.254.169.254      tcp dpt:80 redir ports 9697
	    4   288 DNAT       all  --  *      *       0.0.0.0/0            10.0.0.109           to:172.16.1.10

and here is the SNAT:

	[root@os-controller ~]# ip netns exec qrouter-9574c13d-530a-4c8b-9f4c-b459d2f4709c iptables -L neutron-l3-agent-float-snat -n -v -t nat
	Chain neutron-l3-agent-float-snat (1 references)
	 pkts bytes target     prot opt in     out     source               destination 
	   20  1624 SNAT       all  --  *      *       172.16.1.10          0.0.0.0/0            to:10.0.0.109

#### 3. The router forwards the packet to the provider bridge 

From the [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> 3. The router forwards the packet to the provider bridge router port (12).

You will notice that the *controller* node has two bridges:

	[root@os-controller ~]# brctl show
	bridge name     bridge id               STP enabled     interfaces
	brqaddf3eeb-ef          8000.000c2950e3d3       no      ens192
	                                                        tap191d5c4f-cc
	                                                        tap9be73f50-bb
	brqdc61d555-2a          8000.4ef66f836f75       no      tap745bc525-6f
	                                                        tapebe978d7-c2
	                                                        vxlan-58

The **bridge** with the physical NIC in it (**ens192**) is the **provider** network bridge. And the one with the **vxlan** interface in it is the **self-service** bridge. So now we should see the traffic on the **provider** bridge:

	[root@os-controller ~]# tcpdump -i brqaddf3eeb-ef -nne icmp
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on brqaddf3eeb-ef, link-type EN10MB (Ethernet), capture size 262144 bytes
	13:28:48.453515 fa:16:3e:2e:bb:7b > 78:24:af:7b:1f:08, ethertype IPv4 (0x0800), length 98: 10.0.0.109 > 10.0.0.1: ICMP echo request, id 50177, seq 0, length 64
	13:28:48.453718 78:24:af:7b:1f:08 > fa:16:3e:2e:bb:7b, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 10.0.0.109: ICMP echo reply, id 50177, seq 0, length 64
	
#### 4. The provider bridge forwards the packet to the physical network interface 

Here I diverge from the setup a little bit. From the [Self-service networks](https://docs.openstack.org/ocata/networking-guide/deploy-lb-selfservice.html) page:

> The VLAN sub-interface port (13) on the provider bridge forwards the packet to the provider physical network interface (14).

I actually wasn't using VLANs, so in my setup it just goes out of the physical NIC at this point:

	[root@os-controller ~]# tcpdump -i ens192 -nne icmp and not host kerch
	tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	listening on ens192, link-type EN10MB (Ethernet), capture size 262144 bytes
	13:32:24.262250 fa:16:3e:2e:bb:7b > 78:24:af:7b:1f:08, ethertype IPv4 (0x0800), length 98: 10.0.0.109 > 10.0.0.1: ICMP echo request, id 50433, seq 0, length 64
	13:32:24.262474 78:24:af:7b:1f:08 > fa:16:3e:2e:bb:7b, ethertype IPv4 (0x0800), length 98: 10.0.0.1 > 10.0.0.109: ICMP echo reply, id 50433, seq 0, length 64

Pretty intricate setup :)
