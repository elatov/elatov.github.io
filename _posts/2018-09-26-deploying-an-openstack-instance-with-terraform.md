---
published: false
layout: post
title: "Deploying an OpenStack Instance with Terraform"
author: Karim Elatov
categories: [virtualization]
tags: [openstack,terraform]
---
### Terraform OpenStack Provider

Here are some examples of the usage:

* [Tutorial: How to Use Terraform to Deploy OpenStack Workloads](https://www.stratoscale.com/blog/openstack/tutorial-how-to-use-terraform-to-deploy-openstack-workloads/)
* [Basic OpenStack architecture with networking](https://github.com/terraform-providers/terraform-provider-openstack/tree/master/examples/app-with-networking)
* [Terraform Demo](https://github.com/elastx/terraform-demo)
* [OpenStack infrastructure automation with Terraform – Part 2](https://www.matt-j.co.uk/2015/03/27/openstack-infrastructure-automation-with-terraform-part-2/)
* [Terraform example for OpenStack and Ansible](http://khmel.org/?p=1204)
* [openstack_compute_instance_v2](https://www.terraform.io/docs/providers/openstack/r/compute_instance_v2.html)

### Figure out all the Options for Openstack

Here is the **Region** and the **Auth URL**:

	root@osa:~# openstack endpoint list --service keystone
	+-----+-----------+--------------+--------------+---------+-----------+----------------------------+
	| ID  | Region    | Service Name | Service Type | Enabled | Interface | URL                        |
	+-----+-----------+--------------+--------------+---------+-----------+----------------------------+
	| 897 | RegionOne | keystone     | identity     | True    | internal  | http://192.168.1.126:5000  |
	| 9a8 | RegionOne | keystone     | identity     | True    | public    | http://192.168.1.126:5000  |
	| d71 | RegionOne | keystone     | identity     | True    | admin     | http://192.168.1.126:35357 |
	+-----+-----------+--------------+--------------+---------+-----------+----------------------------+

Here are the available **network**s:

	root@osa:~# openstack network list
	+--------------------------------------+----------+--------------------------------------+
	| ID                                   | Name     | Subnets                              |
	+--------------------------------------+----------+--------------------------------------+
	| 0cd712db-07ba-4a66-b412-cc902d4bed1e | demo-net | e4dac9a4-cd4e-4e1c-90fe-74e27cb6d310 |
	| 11513d67-dc3e-45af-b4a3-4fc56117b55e | public1  | 121d5a18-3e64-4ba9-8612-0d219e68ef68 |
	+--------------------------------------+----------+--------------------------------------+

Here are the **security groups**:

	root@osa:~# openstack security group list
	+--------------------------------------+---------+------------------------+----------------------------------+
	| ID                                   | Name    | Description            | Project                          |
	+--------------------------------------+---------+------------------------+----------------------------------+
	| 31b55999-af17-4ffa-b2d5-00dc78d927f7 | default | Default security group | 894d79b29fc44e458f24d8bb02f44b92 |
	| 8d2aa6fa-5147-4ddd-9e7e-10276cc15356 | default | Default security group |                                  |
	| cb53dd12-a570-417c-9e76-4b7e1c38a075 | default | Default security group | c879d2d22ac44eddb89ec3905afc2578 |
	+--------------------------------------+---------+------------------------+----------------------------------+

Here is the availability zone:

	root@osa:~# openstack availability zone list
	+-----------+-------------+
	| Zone Name | Zone Status |
	+-----------+-------------+
	| internal  | available   |
	| nova      | available   |
	| nova      | available   |
	| nova      | available   |
	+-----------+-------------+

Here are the available **flavor**s:

	root@osa:~# openstack flavor list
	+----+-----------+-------+------+-----------+-------+-----------+
	| ID | Name      |   RAM | Disk | Ephemeral | VCPUs | Is Public |
	+----+-----------+-------+------+-----------+-------+-----------+
	| 1  | m1.tiny   |   512 |    1 |         0 |     1 | True      |
	| 2  | m1.small  |  2048 |   20 |         0 |     1 | True      |
	| 3  | m1.medium |  4096 |   40 |         0 |     2 | True      |
	| 4  | m1.large  |  8192 |   80 |         0 |     4 | True      |
	| 5  | m1.xlarge | 16384 |  160 |         0 |     8 | True      |
	+----+-----------+-------+------+-----------+-------+-----------+

Here is the **image** list:

	root@osa:~# openstack image list
	+--------------------------------------+--------+--------+
	| ID                                   | Name   | Status |
	+--------------------------------------+--------+--------+
	| 4ec62ba8-923d-4daf-a11c-066661aab759 | cirros | active |
	+--------------------------------------+--------+--------+

Make sure to use API v3 to get this:

	root@osa:~# env | grep API
	OS_IDENTITY_API_VERSION=3
	root@osa:~# openstack domain list
	+----------------------------------+------------------+---------+--------------------+
	| ID                               | Name             | Enabled | Description        |
	+----------------------------------+------------------+---------+--------------------+
	| 407250ce0c624058a0bbd3aafffecc9a | heat_user_domain | True    |                    |
	| default                          | Default          | True    | The default domain |
	+----------------------------------+------------------+---------+--------------------+

and here are the variables for the provider:

	root@osa:~# grep -E 'USERN|PASS|TEN|AUT' /etc/kolla/admin-openrc.sh
	export OS_TENANT_NAME=admin
	export OS_USERNAME=admin
	export OS_PASSWORD=3JslywF7EfgRvp9UT9Y9lXlMybj0piH4t9sTISx6
	export OS_AUTH_URL=http://192.168.1.126:35357/v3

### Terraform Code
Here are the files I ended up with. This creates the connection to **OpenStack**:

	<> cat provider.tf
	provider "openstack" {
	  user_name = "${var.openstack_user_name}"
	  tenant_name = "${var.openstack_tenant_name}"
	  password  = "${var.openstack_password}"
	  auth_url  = "${var.openstack_auth_url}"
	  domain_name = "Default"
	}

This files defines most of the variables and leaves the provider credentials out:

	<> cat variables.tf
	variable "openstack_user_name" {}
	variable "openstack_tenant_name" {}
	variable "openstack_password" {}
	variable "openstack_auth_url" {}
	variable "image" {
	  default = "cirros"
	}
	
	variable "flavor" {
	  default = "m1.tiny"
	}
	
	variable "ssh_key_pair" {
	  default = "mykey"
	}
	
	variable "ssh_user_name" {
	  default = "root"
	}
	
	variable "availability_zone" {
		default = "nova"
	}
	
	variable "security_group" {
		default = "default"
	}
	
	variable "network" {
		default  = "demo-net"
	}

Here are the provider credentials:

	<> cat terraform.tfvars
	openstack_user_name = "admin"
	openstack_tenant_name = "admin"
	openstack_password = "3JslywF7EfgRvp9UT9Y9lXlMybj0piH4t9sTISx6"
	openstack_auth_url = "http://192.168.1.126:35357/v3"


This deploys the actual instance and depends on the **variables** defined above:

	<> cat deploy.tf
	resource "openstack_compute_instance_v2" "vm1" {
	  count = "1"
	  name = "demo2"
	  image_name = "${var.image}"
	  availability_zone = "${var.availability_zone}"
	  flavor_name = "${var.flavor}"
	  key_pair = "${var.ssh_key_pair}"
	  security_groups = ["${var.security_group}"]
	  network {
	    name = "${var.network}"
	  }
	  user_data = "${file("test.sh")}"
	}

I also created a simple script just to make sure I can customize the deployed VM:

	<> cat test.sh
	#!/bin/bash
	echo "cool" > /tmp/l.txt

That's it for all the files.
### Using Terraform to deploy an OpenStack Instance
First let's make sure we get the **OpenStack** provider:

	<> terraform init
	
	Initializing provider plugins...
	- Checking for available provider plugins on https://releases.hashicorp.com...
	- Downloading plugin for provider "openstack" (1.1.0)...
	
	The following providers do not have any version constraints in configuration,
	so the latest version was installed.
	
	To prevent automatic upgrades to new major versions that may contain breaking
	changes, it is recommended to add version = "..." constraints to the
	corresponding provider blocks in configuration, with the constraint strings
	suggested below.
	
	* provider.openstack: version = "~> 1.1"
	
	Terraform has been successfully initialized!
	
	You may now begin working with Terraform. Try running "terraform plan" to see
	any changes that are required for your infrastructure. All Terraform commands
	should now work.
	
	If you ever set or change modules or backend configuration for Terraform,
	rerun this command to reinitialize your working directory. If you forget, other
	commands will detect it and remind you to do so if necessary.

Now let's make sure the **plan** is okay:

	<> terraform plan
	Refreshing Terraform state in-memory prior to plan...
	The refreshed state will be used to calculate this plan, but will not be
	persisted to local or remote state storage.
	
	
	------------------------------------------------------------------------
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  + create
	
	Terraform will perform the following actions:
	
	  + openstack_compute_instance_v2.vm1
	      id:                         <computed>
	      access_ip_v4:               <computed>
	      access_ip_v6:               <computed>
	      all_metadata.%:             <computed>
	      availability_zone:          "nova"
	      flavor_id:                  <computed>
	      flavor_name:                "m1.tiny"
	      force_delete:               "false"
	      image_id:                   <computed>
	      image_name:                 "cirros"
	      key_pair:                   "mykey"
	      name:                       "demo2"
	      network.#:                  "1"
	      network.0.access_network:   "false"
	      network.0.fixed_ip_v4:      <computed>
	      network.0.fixed_ip_v6:      <computed>
	      network.0.floating_ip:      <computed>
	      network.0.mac:              <computed>
	      network.0.name:             "demo-net"
	      network.0.port:             <computed>
	      network.0.uuid:             <computed>
	      region:                     <computed>
	      security_groups.#:          "1"
	      security_groups.3814588639: "default"
	      stop_before_destroy:        "false"
	      user_data:                  "80179952cd1bf152cb4bbef9047f7ed1649a7e7d"
	
	
	Plan: 1 to add, 0 to change, 0 to destroy.
	
	------------------------------------------------------------------------
	
	Note: You didn't specify an "-out" parameter to save this plan, so Terraform
	can't guarantee that exactly these actions will be performed if
	"terraform apply" is subsequently run.

And now for the apply:

	<> terraform apply
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	  + create
	
	Terraform will perform the following actions:
	
	  + openstack_compute_instance_v2.vm1
	      id:                         <computed>
	      access_ip_v4:               <computed>
	      access_ip_v6:               <computed>
	      all_metadata.%:             <computed>
	      availability_zone:          "nova"
	      flavor_id:                  <computed>
	      flavor_name:                "m1.tiny"
	      force_delete:               "false"
	      image_id:                   <computed>
	      image_name:                 "cirros"
	      key_pair:                   "mykey"
	      name:                       "demo2"
	      network.#:                  "1"
	      network.0.access_network:   "false"
	      network.0.fixed_ip_v4:      <computed>
	      network.0.fixed_ip_v6:      <computed>
	      network.0.floating_ip:      <computed>
	      network.0.mac:              <computed>
	      network.0.name:             "demo-net"
	      network.0.port:             <computed>
	      network.0.uuid:             <computed>
	      region:                     <computed>
	      security_groups.#:          "1"
	      security_groups.3814588639: "default"
	      stop_before_destroy:        "false"
	      user_data:                  "80179952cd1bf152cb4bbef9047f7ed1649a7e7d"
	
	
	Plan: 1 to add, 0 to change, 0 to destroy.
	
	Do you want to perform these actions?
	  Terraform will perform the actions described above.
	  Only 'yes' will be accepted to approve.
	
	  Enter a value: yes
	
	openstack_compute_instance_v2.vm1: Creating...
	  access_ip_v4:               "" => "<computed>"
	  access_ip_v6:               "" => "<computed>"
	  all_metadata.%:             "" => "<computed>"
	  availability_zone:          "" => "nova"
	  flavor_id:                  "" => "<computed>"
	  flavor_name:                "" => "m1.tiny"
	  force_delete:               "" => "false"
	  image_id:                   "" => "<computed>"
	  image_name:                 "" => "cirros"
	  key_pair:                   "" => "mykey"
	  name:                       "" => "demo2"
	  network.#:                  "" => "1"
	  network.0.access_network:   "" => "false"
	  network.0.fixed_ip_v4:      "" => "<computed>"
	  network.0.fixed_ip_v6:      "" => "<computed>"
	  network.0.floating_ip:      "" => "<computed>"
	  network.0.mac:              "" => "<computed>"
	  network.0.name:             "" => "demo-net"
	  network.0.port:             "" => "<computed>"
	  network.0.uuid:             "" => "<computed>"
	  region:                     "" => "<computed>"
	  security_groups.#:          "" => "1"
	  security_groups.3814588639: "" => "default"
	  stop_before_destroy:        "" => "false"
	  user_data:                  "" => "80179952cd1bf152cb4bbef9047f7ed1649a7e7d"
	openstack_compute_instance_v2.vm1: Still creating... (10s elapsed)
	openstack_compute_instance_v2.vm1: Creation complete after 13s (ID: 227281b2-abd3-427a-8e16-c8b2bc45ad7c)
	
	Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Here is the instance running:

	root@osa:~# openstack server list
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| ID                                   | Name  | Status | Networks             | Image  | Flavor  |
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| 227281b2-abd3-427a-8e16-c8b2bc45ad7c | demo2 | ACTIVE | demo-net=172.24.0.7  | cirros | m1.tiny |
	| b662c4e7-82f3-4ac1-b61e-06a034ae67e1 | demo1 | ACTIVE | demo-net=172.24.0.10 | cirros | m1.tiny |
	+--------------------------------------+-------+--------+----------------------+--------+---------+

#### Fixing user-data
Initially the user-data config failed:

	root@osa:~# openstack console log show demo2 | tail -40
	WARN: /etc/rc3.d/S95-cirros-userdata failed
	=== system information ===

I saw the file getting passed into the OS:

	$ sudo cat /run/cirros/datasource/data/user-data
	#!/bin/bash
	echo "cool" > /tmp/l.txt

and I was able to query for that **user-data** contents:

	$ cat /etc/cirros-init/ds-ec2
	MAX_TRIES=20
	SLEEP_TIME=2
	BURL="http://169.254.169.254/2009-04-04"
	$ curl http://169.254.169.254/2009-04-04/user-data
	#!/bin/bash
	echo "cool" > /tmp/l.txt


then I realized **/bin/bash** wasn't there:

	$ /bin/bash
	-sh: /bin/bash: not found
	$ /bin/sh

So I updated the **test.sh** file. And then running the **plan** it will re-create the resource:

	<> terraform plan
	Refreshing Terraform state in-memory prior to plan...
	The refreshed state will be used to calculate this plan, but will not be
	persisted to local or remote state storage.
	
	openstack_compute_instance_v2.vm1: Refreshing state... (ID: 227281b2-abd3-427a-8e16-c8b2bc45ad7c)
	
	------------------------------------------------------------------------
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	-/+ destroy and then create replacement
	
	Terraform will perform the following actions:
	
	-/+ openstack_compute_instance_v2.vm1 (new resource required)
	      id:                         "227281b2-abd3-427a-8e16-c8b2bc45ad7c" => <computed> (forces new resource)
	      access_ip_v4:               "172.24.0.7" => <computed>
	      access_ip_v6:               "" => <computed>
	      all_metadata.%:             "0" => <computed>
	      availability_zone:          "nova" => "nova"
	      flavor_id:                  "1" => <computed>
	      flavor_name:                "m1.tiny" => "m1.tiny"
	      force_delete:               "false" => "false"
	      image_id:                   "4ec62ba8-923d-4daf-a11c-066661aab759" => <computed>
	      image_name:                 "cirros" => "cirros"
	      key_pair:                   "mykey" => "mykey"
	      name:                       "demo2" => "demo2"
	      network.#:                  "1" => "1"
	      network.0.access_network:   "false" => "false"
	      network.0.fixed_ip_v4:      "172.24.0.7" => <computed>
	      network.0.fixed_ip_v6:      "" => <computed>
	      network.0.floating_ip:      "" => <computed>
	      network.0.mac:              "fa:16:3e:3f:91:88" => <computed>
	      network.0.name:             "demo-net" => "demo-net"
	      network.0.port:             "" => <computed>
	      network.0.uuid:             "0cd712db-07ba-4a66-b412-cc902d4bed1e" => <computed>
	      region:                     "" => <computed>
	      security_groups.#:          "1" => "1"
	      security_groups.3814588639: "default" => "default"
	      stop_before_destroy:        "false" => "false"
	      user_data:                  "80179952cd1bf152cb4bbef9047f7ed1649a7e7d" => "90f8abf748f00aaee3f0d436dea4cbdc46adac63" (forces new resource)
	
	
	Plan: 1 to add, 0 to change, 1 to destroy.
	
	------------------------------------------------------------------------
	
	Note: You didn't specify an "-out" parameter to save this plan, so Terraform
	can't guarantee that exactly these actions will be performed if
	"terraform apply" is subsequently run.

And then appying the new config:

	<> terraform apply
	openstack_compute_instance_v2.vm1: Refreshing state... (ID: 227281b2-abd3-427a-8e16-c8b2bc45ad7c)
	
	An execution plan has been generated and is shown below.
	Resource actions are indicated with the following symbols:
	-/+ destroy and then create replacement
	
	Terraform will perform the following actions:
	
	-/+ openstack_compute_instance_v2.vm1 (new resource required)
	      id:                         "227281b2-abd3-427a-8e16-c8b2bc45ad7c" => <computed> (forces new resource)
	      access_ip_v4:               "172.24.0.7" => <computed>
	      access_ip_v6:               "" => <computed>
	      all_metadata.%:             "0" => <computed>
	      availability_zone:          "nova" => "nova"
	      flavor_id:                  "1" => <computed>
	      flavor_name:                "m1.tiny" => "m1.tiny"
	      force_delete:               "false" => "false"
	      image_id:                   "4ec62ba8-923d-4daf-a11c-066661aab759" => <computed>
	      image_name:                 "cirros" => "cirros"
	      key_pair:                   "mykey" => "mykey"
	      name:                       "demo2" => "demo2"
	      network.#:                  "1" => "1"
	      network.0.access_network:   "false" => "false"
	      network.0.fixed_ip_v4:      "172.24.0.7" => <computed>
	      network.0.fixed_ip_v6:      "" => <computed>
	      network.0.floating_ip:      "" => <computed>
	      network.0.mac:              "fa:16:3e:3f:91:88" => <computed>
	      network.0.name:             "demo-net" => "demo-net"
	      network.0.port:             "" => <computed>
	      network.0.uuid:             "0cd712db-07ba-4a66-b412-cc902d4bed1e" => <computed>
	      region:                     "" => <computed>
	      security_groups.#:          "1" => "1"
	      security_groups.3814588639: "default" => "default"
	      stop_before_destroy:        "false" => "false"
	      user_data:                  "80179952cd1bf152cb4bbef9047f7ed1649a7e7d" => "90f8abf748f00aaee3f0d436dea4cbdc46adac63" (forces new resource)
	
	
	Plan: 1 to add, 0 to change, 1 to destroy.
	
	Do you want to perform these actions?
	  Terraform will perform the actions described above.
	  Only 'yes' will be accepted to approve.
	
	  Enter a value: yes
	
	openstack_compute_instance_v2.vm1: Destroying... (ID: 227281b2-abd3-427a-8e16-c8b2bc45ad7c)
	openstack_compute_instance_v2.vm1: Still destroying... (ID: 227281b2-abd3-427a-8e16-c8b2bc45ad7c, 10s elapsed)
	openstack_compute_instance_v2.vm1: Destruction complete after 11s
	openstack_compute_instance_v2.vm1: Creating...
	  access_ip_v4:               "" => "<computed>"
	  access_ip_v6:               "" => "<computed>"
	  all_metadata.%:             "" => "<computed>"
	  availability_zone:          "" => "nova"
	  flavor_id:                  "" => "<computed>"
	  flavor_name:                "" => "m1.tiny"
	  force_delete:               "" => "false"
	  image_id:                   "" => "<computed>"
	  image_name:                 "" => "cirros"
	  key_pair:                   "" => "mykey"
	  name:                       "" => "demo2"
	  network.#:                  "" => "1"
	  network.0.access_network:   "" => "false"
	  network.0.fixed_ip_v4:      "" => "<computed>"
	  network.0.fixed_ip_v6:      "" => "<computed>"
	  network.0.floating_ip:      "" => "<computed>"
	  network.0.mac:              "" => "<computed>"
	  network.0.name:             "" => "demo-net"
	  network.0.port:             "" => "<computed>"
	  network.0.uuid:             "" => "<computed>"
	  region:                     "" => "<computed>"
	  security_groups.#:          "" => "1"
	  security_groups.3814588639: "" => "default"
	  stop_before_destroy:        "" => "false"
	  user_data:                  "" => "90f8abf748f00aaee3f0d436dea4cbdc46adac63"
	openstack_compute_instance_v2.vm1: Still creating... (10s elapsed)
	openstack_compute_instance_v2.vm1: Creation complete after 16s (ID: 5bf81a28-9625-4e79-b406-e3034dc913ec)
	
	Apply complete! Resources: 1 added, 0 changed, 1 destroyed.

Now looking up the new server (with a new IP):

	root@osa:~# openstack server list
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| ID                                   | Name  | Status | Networks             | Image  | Flavor  |
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| 5bf81a28-9625-4e79-b406-e3034dc913ec | demo2 | ACTIVE | demo-net=172.24.0.5  | cirros | m1.tiny |
	| b662c4e7-82f3-4ac1-b61e-06a034ae67e1 | demo1 | ACTIVE | demo-net=172.24.0.10 | cirros | m1.tiny |
	+--------------------------------------+-------+--------+----------------------+--------+---------+

and checking, I saw the new file created in the instance:

	root@osa:~# ip netns exec qrouter-57752fa4-84f2-48a9-beca-d1218825ee0a ssh cirros@172.24.0.5 cat /tmp/l.txt
	cool

That's awesome.
