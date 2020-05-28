---
published: true
layout: post
title: "Installing OpenStack Pike with Kolla Ansible"
author: Karim Elatov
categories: [virtualization, containers]
tags: [openstack, kolla, ansible]
---

### OpenStack Pike with Kolla
I already had a previous install of **openstack** from my [previous testing](/2018/01/openstack-ansible-and-kolla-on-ubuntu-1604/) with **kolla**. The **ocata** version looked like this (note the **4.0.0** version/tag):

	root@osa:~# docker ps
	CONTAINER ID        IMAGE                                                 COMMAND             CREATED             STATUS              PORTS               NAMES
	541fcdfe1c1d        kolla/centos-binary-horizon:4.0.0                     "kolla_start"       6 months ago        Up 6 minutes                            horizon
	d5e056a34968        kolla/centos-binary-heat-engine:4.0.0                 "kolla_start"       6 months ago        Up 6 minutes                            heat_engine
	8833d61e0873        kolla/centos-binary-heat-api-cfn:4.0.0                "kolla_start"       6 months ago        Up 6 minutes                            heat_api_cfn
	aed9da6601b5        kolla/centos-binary-heat-api:4.0.0                    "kolla_start"       6 months ago        Up 6 minutes                            heat_api
	f85b7aac7597        kolla/centos-binary-neutron-metadata-agent:4.0.0      "kolla_start"       6 months ago        Up 6 minutes                            neutron_metadata_agent
	b21ea8839a67        kolla/centos-binary-neutron-l3-agent:4.0.0            "kolla_start"       6 months ago        Up 6 minutes                            neutron_l3_agent
	13b67d701d0c        kolla/centos-binary-neutron-dhcp-agent:4.0.0          "kolla_start"       6 months ago        Up 6 minutes                            neutron_dhcp_agent
	92452b6a66be        kolla/centos-binary-neutron-openvswitch-agent:4.0.0   "kolla_start"       6 months ago        Up 6 minutes                            neutron_openvswitch_agent
	40e8ed916391        kolla/centos-binary-neutron-server:4.0.0              "kolla_start"       6 months ago        Up 6 minutes                            neutron_server
	c27dcdfa48b9        kolla/centos-binary-openvswitch-vswitchd:4.0.0        "kolla_start"       6 months ago        Up 6 minutes                            openvswitch_vswitchd
	747a5703da42        kolla/centos-binary-openvswitch-db-server:4.0.0       "kolla_start"       6 months ago        Up 6 minutes                            openvswitch_db
	66747984b5eb        kolla/centos-binary-nova-compute:4.0.0                "kolla_start"       6 months ago        Up 5 minutes                            nova_compute
	e12b61bccc55        kolla/centos-binary-nova-novncproxy:4.0.0             "kolla_start"       6 months ago        Up 6 minutes                            nova_novncproxy
	e01a402a452d        kolla/centos-binary-nova-consoleauth:4.0.0            "kolla_start"       6 months ago        Up 6 minutes                            nova_consoleauth
	3cd2dd3f7d67        kolla/centos-binary-nova-conductor:4.0.0              "kolla_start"       6 months ago        Up 6 minutes                            nova_conductor
	735355d27fcd        kolla/centos-binary-nova-scheduler:4.0.0              "kolla_start"       6 months ago        Up 6 minutes                            nova_scheduler
	58be193911f7        kolla/centos-binary-nova-api:4.0.0                    "kolla_start"       6 months ago        Up 6 minutes                            nova_api
	d89bedf1d84f        kolla/centos-binary-nova-placement-api:4.0.0          "kolla_start"       6 months ago        Up 6 minutes                            placement_api
	fa7fbd4a97cd        kolla/centos-binary-nova-libvirt:4.0.0                "kolla_start"       6 months ago        Up 6 minutes                            nova_libvirt
	a04d447737e0        kolla/centos-binary-nova-ssh:4.0.0                    "kolla_start"       6 months ago        Up 6 minutes                            nova_ssh
	0de67aa40087        kolla/centos-binary-glance-registry:4.0.0             "kolla_start"       6 months ago        Up 6 minutes                            glance_registry
	55a63464be40        kolla/centos-binary-glance-api:4.0.0                  "kolla_start"       6 months ago        Up 6 minutes                            glance_api
	4733b5150137        kolla/centos-binary-keystone:4.0.0                    "kolla_start"       6 months ago        Up 6 minutes                            keystone
	d00528425061        kolla/centos-binary-rabbitmq:4.0.0                    "kolla_start"       6 months ago        Up 6 minutes                            rabbitmq
	7513180bbfc1        kolla/centos-binary-mariadb:4.0.0                     "kolla_start"       6 months ago        Up 6 minutes                            mariadb
	dee65dd81375        kolla/centos-binary-memcached:4.0.0                   "kolla_start"       6 months ago        Up 6 minutes                            memcached
	d14fedfdca7c        kolla/centos-binary-keepalived:4.0.0                  "kolla_start"       6 months ago        Up 6 minutes                            keepalived
	90550271ecd2        kolla/centos-binary-haproxy:4.0.0                     "kolla_start"       6 months ago        Up 6 minutes                            haproxy
	16eac64e322a        kolla/centos-binary-cron:4.0.0                        "kolla_start"       6 months ago        Up 6 minutes                            cron
	60cfbc64b780        kolla/centos-binary-kolla-toolbox:4.0.0               "kolla_start"       6 months ago        Up 6 minutes                            kolla_toolbox
	26ff99a6ad8b        kolla/centos-binary-fluentd:4.0.0                     "kolla_start"       6 months ago        Up 6 minutes                            fluentd

Reading over [Operating Kolla](https://docs.openstack.org/kolla-ansible/latest/user/operating-kolla.html), it looks like we could try an update (but the results vary). I decided to give it a try knowing that it might not work out. We need to update the **/etc/kolla/globals.yml** file and point to the new version. Before I made any changes, here is how it looked like:

	root@osa:~# grep openstack_release /etc/kolla/globals.yml
	openstack_release: "4.0.0"


#### Trying a Kolla Update

So let's update the **kolla-ansible** tool:

	root@osa:~# pip install -U kolla-ansible

Then let's update the version:

	root@osa:~# grep openstack_release /etc/kolla/globals.yml
	openstack_release: "5.0.1"

When I tried doing an *update* I ran into the following error:

	root@osa:~# kolla-ansible upgrade
	Upgrading OpenStack Environment : ansible-playbook -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one -e @/etc/kolla/globals.yml -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  -e action=upgrade -e serial=0 /usr/local/share/kolla-ansible/ansible/site.yml
	ERROR! Unexpected Exception: 'module' object has no attribute 'SSL_ST_INIT'

I ran into [Run error: "'module' object has no attribute 'SSL_ST_INIT'"."](https://github.com/andresriancho/w3af/issues/15260) which talked about fixing the issue by updating the **pyOpenSSL** module (so I did that):

	root@osa:~# pip uninstall pyOpenSSL
	Uninstalling pyOpenSSL-0.15.1:
	  /usr/lib/python2.7/dist-packages/OpenSSL
	  /usr/lib/python2.7/dist-packages/pyOpenSSL-0.15.1.egg-info
	Proceed (y/n)? y
	  Successfully uninstalled pyOpenSSL-0.15.1
	root@osa:~# pip install pyOpenSSL
	Collecting pyOpenSSL
	  Downloading pyOpenSSL-17.5.0-py2.py3-none-any.whl (53kB)
	    100% |████████████████████████████████| 61kB 914kB/s

Next I ran into the following error:

	RUNNING HANDLER [common : Restart fluentd container] ***************************
	fatal: [localhost]: FAILED! => {"changed": true, "failed": true, "msg": "'Traceback (most recent call last):\\n  File \"/tmp/ansible_EwrJnL/ansible_module_kolla_docker.py\", line 799, in main\\n    result = bool(getattr(dw, module.params.get(\\'action\\'))())\\n  File \"/tmp/ansible_EwrJnL/ansible_module_kolla_docker.py\", line 597, in recreate_or_restart_container\\n    self.start_container()\\n  File \"/tmp/ansible_EwrJnL/ansible_module_kolla_docker.py\", line 603, in start_container\\n    self.pull_image()\\n  File \"/tmp/ansible_EwrJnL/ansible_module_kolla_docker.py\", line 456, in pull_image\\n    repository=image, tag=tag, stream=True\\n  File \"/usr/local/lib/python2.7/dist-packages/docker/api/image.py\", line 381, in pull\\n    header = auth.get_config_header(self, registry)\\nAttributeError: \\'module\\' object has no attribute \\'get_config_header\\'\\n'"}

	RUNNING HANDLER [common : Restart kolla-toolbox container] *********************

	RUNNING HANDLER [common : Restart cron container] ******************************
		to retry, use: --limit @/usr/local/share/kolla-ansible/ansible/site.retry

	PLAY RECAP *********************************************************************
	localhost                  : ok=12   changed=7    unreachable=0    failed=1

Next I ran into [get_config_header error on mac](https://github.com/docker/docker-py/issues/1353), which recommended updating the **docker** python module and to remove the **pydocker** module:

	root@osa:~# pip uninstall docker docker-py
	Uninstalling docker-2.7.0:
	Uninstalling docker-py-1.10.6:

Then just installing **docker** module:

	root@osa:~# pip install docker
	Collecting docker
	  Using cached docker-2.7.0-py2.py3-none-any.whl

This was actually discussed in this [bug](https://bugs.launchpad.net/kolla-ansible/+bug/1704569) and also [here](https://bugs.launchpad.net/kolla/+bug/1668346).

#### Kolla Software Versions

Just for reference, here were all the versions I had:

	root@osa:~# docker --version
	Docker version 17.05.0-ce, build 89658be
	root@osa:~# pip --version
	pip 9.0.1 from /usr/local/lib/python2.7/dist-packages (python 2.7)
	root@osa:~# pip show docker
	Name: docker
	Version: 2.7.0
	Summary: A Python library for the Docker Engine API.
	root@osa:~# ansible --version
	ansible 2.3.1.0
	  config file =
	  configured module search path = Default w/o overrides
	  python version = 2.7.12 (default, Nov 20 2017, 18:23:56) [GCC 5.4.0 20160609]
	root@osa:~# pip show kolla-ansible
	Name: kolla-ansible
	Version: 5.0.1
	Summary: Ansible Deployment of Kolla containers

Moving on.

### Building Kolla Docker Images
Trying another update, I ran into this:

	raise cls(e, response=response, explanation=explanation)\\nNotFound: 404 Client Error: Not Found (\"manifest for kolla/centos-binary-fluentd:5.0.0 not found\")\\n'"}

I tried to pull new images:

	root@osa:~# kolla-ansible pull -i  /usr/local/share/kolla-ansible/ansible/inventory/all-in-one

But ran into a similar issue:

	create_api_error_from_http_exception\\n    raise cls(e, response=response, explanation=explanation)\\nNotFound: 404 Client Error: Not Found (\"manifest for kolla/centos-binary-kolla-toolbox:5.0.0 not found\")\\n'"}

Based on [this post](https://ask.openstack.org/en/question/110691/kolla-images-for-pike-with-tag-500-dont-exist-on-docker-hub-registry/) it looks like the images don't yet exist. So I decided to build the images which requires the **tox** tool. All the instructions are laid on in [Building Container Images](https://docs.openstack.org/kolla/latest/admin/image-building.html). After installing **tox** I kep running into another issue where the **kolla-build** binary was not available. I ended following instructions laid out in [Kolla-build: command not found](https://ask.openstack.org/en/question/93967/kolla-build-command-not-found/):

	root@osa:~# git clone https://github.com/openstack/kolla.git
	Cloning into 'kolla'...
	remote: Counting objects: 58018, done.
	remote: Compressing objects: 100% (37/37), done.
	remote: Total 58018 (delta 14), reused 15 (delta 8), pack-reused 57973
	Receiving objects: 100% (58018/58018), 9.12 MiB | 12.91 MiB/s, done.
	Resolving deltas: 100% (35133/35133), done.
	Checking connectivity... done.
	root@osa:~# cd kolla/
	root@osa:~/kolla# git branch -r
	origin/HEAD -> origin/master
	origin/master
	origin/stable/ocata
	origin/stable/pike
	root@osa:~/kolla# git checkout stable/pike
	Branch stable/pike set up to track remote branch stable/pike from origin.
	Switched to a new branch 'stable/pike'
	root@osa:~/kolla# cd kolla/
	root@osa:~/kolla# tox -e genconfig
	genconfig create: /root/kolla/.tox/genconfig
	genconfig installdeps: -r/root/kolla/requirements.txt, -r/root/kolla/test-requirements.txt
	genconfig develop-inst: /root/kolla
	genconfig installed: alabaster==0.7.10,... ... testscenarios==0.5.0,testtools==2.3.0,traceback2==1.4.0,typing==3.6.1,unicodecsv==0.14.1,unittest2==1.1.0,urllib3==1.22,warlock==1.2.0,websocket-client==0.44.0,wrapt==1.10.10
	  genconfig runtests: PYTHONHASHSEED='2131518256'
	  genconfig runtests: commands[0] | oslo-config-generator --config-file etc/oslo-config-generator/kolla-build.conf
	  /root/kolla/.tox/genconfig/local/lib/python2.7/site-packages/oslo_config/types.py:54: UserWarning: converting '[]' to a string
	    warnings.warn('converting \'%s\' to a string' % str_val)
	  ________________________________________________________________________________________________________________ summary ________________________________________________________________________________________________________________
	    genconfig: commands succeeded
	    congratulations :)

Then I was able to build the images:

	root@osa:~/kolla# .tox/genconfig/bin/kolla-build -b centos
	NFO:kolla.image.build:Found the docker image folder at /root/kolla/docker
	INFO:kolla.image.build:Added image base to queue
	INFO:kolla.image.build:Attempt number: 1 to run task: BuildTask(base)
	INFO:kolla.image.build.base:Building
	INFO:kolla.image.build.base:Step 1/31 : FROM centos:7
	INFO:kolla.image.build.base: ---> 3fa822599e10
	INFO:kolla.image.build.base:Step 2/31 : LABEL maintainer "Kolla Project (https://launchpad.net/kolla)" name "base" build-date "20171230"
	INFO:kolla.image.build.base: ---> Running in c14b31ede1fb
	INFO:kolla.image.build.base: ---> e11b0fa371df
	..
	...
	INFO:kolla.image.build.mariadb:Successfully tagged kolla/centos-binary-mariadb:5.0.1
	INFO:kolla.image.build.mariadb:Built
	INFO:kolla.image.build:=========================
	INFO:kolla.image.build:Successfully built images
	INFO:kolla.image.build:=========================
	INFO:kolla.image.build:aodh-api
	INFO:kolla.image.build:aodh-base
	INFO:kolla.image.build:aodh-evaluator
	INFO:kolla.image.build:aodh-expirer
	INFO:kolla.image.build:aodh-listener
	INFO:kolla.image.build:aodh-notifier
	INFO:kolla.image.build:barbican-api
	INFO:kolla.image.build:barbican-base
	...
	...
	INFO:kolla.image.build:tacker-server
	INFO:kolla.image.build:telegraf
	INFO:kolla.image.build:tempest
	INFO:kolla.image.build:tgtd
	INFO:kolla.image.build:trove-api
	INFO:kolla.image.build:trove-base
	INFO:kolla.image.build:trove-conductor
	INFO:kolla.image.build:trove-guestagent
	INFO:kolla.image.build:trove-taskmanager
	INFO:kolla.image.build:watcher-api
	INFO:kolla.image.build:watcher-applier
	INFO:kolla.image.build:watcher-base
	INFO:kolla.image.build:watcher-engine
	INFO:kolla.image.build:zaqar
	INFO:kolla.image.build:zookeeper

The build took a while, but after it's done, you can see all images it built:

	root@osa:~# docker images "kolla/*:5.0.1"
	REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
	kolla/centos-binary-mariadb                         5.0.1               319de57c9ecd        27 hours ago        844MB
	kolla/centos-binary-neutron-server-opendaylight     5.0.1               9c8826e529e9        27 hours ago        841MB
	kolla/centos-binary-ovn-nb-db-server                5.0.1               da6cb4c09f4e        27 hours ago        520MB
	kolla/centos-binary-neutron-server-ovn              5.0.1               0b32f85751e7        27 hours ago        841MB
	kolla/centos-binary-ovn-sb-db-server                5.0.1               d17ff6432e0c        27 hours ago        520MB
	kolla/centos-binary-ovn-controller                  5.0.1               8e3e9fcd9ad0        27 hours ago        520MB
	kolla/centos-binary-ovn-northd                      5.0.1               4fc9736c36dd        27 hours ago        520MB
	kolla/centos-binary-mistral-executor                5.0.1               31715269ae83        27 hours ago        819MB
	kolla/centos-binary-mistral-event-engine            5.0.1               8c94566dc159        27 hours ago        819MB
	kolla/centos-binary-mistral-api                     5.0.1               82982fc41871        27 hours ago        819MB
	kolla/centos-binary-mistral-engine                  5.0.1               1b74eaea544d        27 hours ago        819MB
	kolla/centos-binary-aodh-notifier                   5.0.1               7f8ba07eba29        27 hours ago        764MB
	kolla/centos-binary-aodh-listener                   5.0.1               cb2ea74d534f        27 hours ago        764MB
	kolla/centos-binary-aodh-expirer                    5.0.1               6378a7968628        27 hours ago        764MB
	kolla/centos-binary-aodh-api                        5.0.1               b722e2fb0d6e        27 hours ago        764MB
	kolla/centos-binary-aodh-evaluator                  5.0.1               d3282a444d84        27 hours ago        764MB
	kolla/centos-binary-octavia-health-manager          5.0.1               3af7baee737f        27 hours ago        819MB
	kolla/centos-binary-octavia-api                     5.0.1               ea8c3e2aa18c        27 hours ago        819MB
	kolla/centos-binary-octavia-worker                  5.0.1               0a79e29bdf98        27 hours ago        819MB
	kolla/centos-binary-octavia-housekeeping            5.0.1               575c1e3ad595        27 hours ago        819MB
	kolla/centos-binary-heat-engine                     5.0.1               19251a25d073        27 hours ago        767MB
	kolla/centos-binary-heat-api                        5.0.1               2791566afada        27 hours ago        767MB
	kolla/centos-binary-nova-compute                    5.0.1               27d338faae52        27 hours ago        1.26GB
	kolla/centos-binary-heat-api-cloudwatch             5.0.1               235df438cc88        27 hours ago        767MB
	kolla/centos-binary-heat-all                        5.0.1               48ec52c49d4e        27 hours ago        767MB
	kolla/centos-binary-keystone-ssh                    5.0.1               8e5ff8df6a87        27 hours ago        790MB
	kolla/centos-binary-keystone-fernet                 5.0.1               79fd30d153fd        27 hours ago        771MB
	kolla/centos-binary-cloudkitty-api                  5.0.1               99028370847d        27 hours ago        760MB
	kolla/centos-binary-heat-api-cfn                    5.0.1               9eb6b739f78d        27 hours ago        767MB
	kolla/centos-binary-watcher-api                     5.0.1               c2ade53dff9d        27 hours ago        813MB
	kolla/centos-binary-cloudkitty-processor            5.0.1               20a491f3860e        27 hours ago        708MB
	kolla/centos-binary-nova-compute-ironic             5.0.1               0afd0da8efb7        27 hours ago        1.16GB
	kolla/centos-binary-watcher-applier                 5.0.1               2fd14cee7541        27 hours ago        813MB
	kolla/centos-binary-keystone                        5.0.1               1ddb246d3b01        27 hours ago        748MB
	kolla/centos-binary-watcher-engine                  5.0.1               a11a620d3210        27 hours ago        813MB
	kolla/centos-binary-trove-guestagent                5.0.1               454d76a06388        27 hours ago        710MB
	kolla/centos-binary-trove-conductor                 5.0.1               0052dc950579        27 hours ago        709MB
	kolla/centos-binary-trove-api                       5.0.1               5902ed6fbbd8        27 hours ago        709MB
	kolla/centos-binary-trove-taskmanager               5.0.1               83344566fe92        27 hours ago        709MB
	kolla/centos-binary-gnocchi-statsd                  5.0.1               7d1f7510f2af        27 hours ago        1.03GB
	kolla/centos-binary-gnocchi-metricd                 5.0.1               0b945b529e56        27 hours ago        1.03GB
	kolla/centos-binary-gnocchi-api                     5.0.1               03231dc7e470        27 hours ago        1.03GB
	kolla/centos-binary-nova-placement-api              5.0.1               6c2a1f89adeb        27 hours ago        818MB
	kolla/centos-binary-nova-serialproxy                5.0.1               86f6a54d998e        27 hours ago        766MB
	kolla/centos-binary-nova-conductor                  5.0.1               578a1465c720        27 hours ago        766MB
	kolla/centos-binary-nova-scheduler                  5.0.1               4d6a4b91fe57        27 hours ago        766MB
	kolla/centos-binary-nova-spicehtml5proxy            5.0.1               1bc87e70172a        27 hours ago        807MB
	kolla/centos-binary-nova-ssh                        5.0.1               c8d5b68681ea        27 hours ago        785MB
	kolla/centos-binary-nova-api                        5.0.1               949a2b3d2388        27 hours ago        818MB
	kolla/centos-binary-nova-consoleauth                5.0.1               10b74e04aa96        27 hours ago        766MB
	kolla/centos-binary-manila-share                    5.0.1               bcc926e5fd0e        27 hours ago        896MB
	kolla/centos-binary-nova-novncproxy                 5.0.1               f5c1be5c08eb        27 hours ago        766MB
	kolla/centos-binary-barbican-api                    5.0.1               a50908260c66        27 hours ago        764MB
	kolla/centos-binary-barbican-worker                 5.0.1               1cb41a02bf99        27 hours ago        709MB
	kolla/centos-binary-cinder-api                      5.0.1               3a8e096fdcd3        27 hours ago        1.08GB
	kolla/centos-binary-cinder-volume                   5.0.1               ed128afcb892        27 hours ago        1.02GB
	kolla/centos-binary-barbican-keystone-listener      5.0.1               b6db78ee3fc8        27 hours ago        709MB
	kolla/centos-binary-manila-api                      5.0.1               84a31479fcc8        27 hours ago        714MB
	kolla/centos-binary-manila-data                     5.0.1               5ad2a428bfec        27 hours ago        714MB
	kolla/centos-binary-manila-scheduler                5.0.1               6df1bbc5604e        27 hours ago        714MB
	kolla/centos-binary-cinder-backup                   5.0.1               24a9e72625d6        27 hours ago        1.02GB
	kolla/centos-binary-designate-worker                5.0.1               236ff9527a31        27 hours ago        770MB
	kolla/centos-binary-designate-pool-manager          5.0.1               536be308b31e        27 hours ago        770MB
	kolla/centos-binary-designate-central               5.0.1               706195f51ed9        27 hours ago        741MB
	kolla/centos-binary-designate-mdns                  5.0.1               f870cdca64ab        27 hours ago        741MB
	kolla/centos-binary-designate-api                   5.0.1               b7f4e687c366        27 hours ago        741MB
	kolla/centos-binary-designate-sink                  5.0.1               6688ab72f163        27 hours ago        741MB
	kolla/centos-binary-cinder-scheduler                5.0.1               b9920e6a1376        27 hours ago        987MB
	kolla/centos-binary-designate-backend-bind9         5.0.1               c7e3c82c3ef1        27 hours ago        770MB
	kolla/centos-binary-ironic-conductor                5.0.1               e2d164588fae        27 hours ago        875MB
	kolla/centos-binary-ironic-pxe                      5.0.1               23a39423dd48        27 hours ago        829MB
	kolla/centos-binary-neutron-lbaas-agent             5.0.1               88ca4ec165c0        27 hours ago        790MB
	kolla/centos-binary-tacker-server                   5.0.1               5ca83249e4f5        27 hours ago        709MB
	kolla/centos-binary-ironic-api                      5.0.1               c48d921ed514        27 hours ago        821MB
	kolla/centos-binary-tacker-conductor                5.0.1               1488f658e756        27 hours ago        709MB
	kolla/centos-binary-neutron-vpnaas-agent            5.0.1               551d2809528c        27 hours ago        838MB
	kolla/centos-binary-neutron-linuxbridge-agent       5.0.1               23f146b48966        27 hours ago        811MB
	kolla/centos-binary-neutron-server                  5.0.1               118f1b71256b        27 hours ago        811MB
	kolla/centos-binary-neutron-openvswitch-agent       5.0.1               a8bb909443ca        27 hours ago        810MB
	kolla/centos-binary-neutron-metering-agent          5.0.1               bbc56aad9a9c        27 hours ago        810MB
	kolla/centos-binary-neutron-sriov-agent             5.0.1               81eb1ed1e48e        27 hours ago        810MB
	kolla/centos-binary-neutron-sfc-agent               5.0.1               df0d7abef6dd        27 hours ago        786MB
	kolla/centos-binary-neutron-dhcp-agent              5.0.1               0b19b9e07d39        27 hours ago        786MB
	kolla/centos-binary-sahara-engine                   5.0.1               1c6ccb518d96        27 hours ago        721MB
	kolla/centos-binary-neutron-metadata-agent          5.0.1               a19f9b4112b5        27 hours ago        786MB
	kolla/centos-binary-sahara-api                      5.0.1               e507304b0682        27 hours ago        721MB
	kolla/centos-binary-ceilometer-notification         5.0.1               3d41ada1ff3c        27 hours ago        722MB
	kolla/centos-binary-ceilometer-compute              5.0.1               51b3ac65e316        27 hours ago        770MB
	kolla/centos-binary-ceilometer-collector            5.0.1               4b7a0bea6550        27 hours ago        724MB
	kolla/centos-binary-neutron-l3-agent                5.0.1               103e9b4f30e1        27 hours ago        786MB
	kolla/centos-binary-novajoin-server                 5.0.1               fbf8aa393880        27 hours ago        787MB
	kolla/centos-binary-ceilometer-ipmi                 5.0.1               f23dc402617c        27 hours ago        772MB
	kolla/centos-binary-novajoin-notifier               5.0.1               758f1038b65f        27 hours ago        787MB
	kolla/centos-binary-ceilometer-api                  5.0.1               2e043f70ff83        27 hours ago        777MB
	kolla/centos-binary-ceilometer-central              5.0.1               1c622df60abf        27 hours ago        770MB
	kolla/centos-binary-murano-api                      5.0.1               075cc86f338e        27 hours ago        716MB
	kolla/centos-binary-murano-engine                   5.0.1               9f73ef9baf78        27 hours ago        716MB
	kolla/centos-binary-glance-api                      5.0.1               c333139fda75        27 hours ago        883MB
	kolla/centos-binary-panko-api                       5.0.1               72a691ee1fd1        27 hours ago        778MB
	kolla/centos-binary-magnum-conductor                5.0.1               3c8e442574d7        27 hours ago        878MB
	kolla/centos-binary-magnum-api                      5.0.1               33a28c7ac633        27 hours ago        827MB
	kolla/centos-binary-swift-rsyncd                    5.0.1               1c69c6883e19        27 hours ago        686MB
	kolla/centos-binary-swift-object                    5.0.1               9a4bf0a6419a        27 hours ago        706MB
	kolla/centos-binary-swift-object-expirer            5.0.1               69badccaf52e        27 hours ago        707MB
	kolla/centos-binary-glance-registry                 5.0.1               72778f33842c        27 hours ago        821MB
	kolla/centos-binary-swift-account                   5.0.1               69cef816c327        27 hours ago        706MB
	kolla/centos-binary-congress-api                    5.0.1               d8ce0966fcbe        27 hours ago        698MB
	kolla/centos-binary-congress-policy-engine          5.0.1               a908b72fff4e        27 hours ago        698MB
	kolla/centos-binary-swift-proxy-server              5.0.1               673bedd052f9        27 hours ago        707MB
	kolla/centos-binary-congress-datasource             5.0.1               479a4fccf5b5        27 hours ago        698MB
	kolla/centos-binary-swift-container                 5.0.1               e581759c4f0e        27 hours ago        706MB
	kolla/centos-binary-ovn-base                        5.0.1               9c2bbb67c864        27 hours ago        497MB
	kolla/centos-binary-mistral-base                    5.0.1               ce88db140569        27 hours ago        796MB
	kolla/centos-binary-rally                           5.0.1               62c80a52949a        27 hours ago        752MB
	kolla/centos-binary-aodh-base                       5.0.1               007a3bf5e634        27 hours ago        742MB
	kolla/centos-binary-octavia-base                    5.0.1               f6dcf003f84d        27 hours ago        796MB
	kolla/centos-binary-heat-base                       5.0.1               18ddcf5bc2da        27 hours ago        745MB
	kolla/centos-binary-keystone-base                   5.0.1               7e0811f72fab        27 hours ago        748MB
	kolla/centos-binary-openvswitch-db-server           5.0.1               73f7b877c485        27 hours ago        471MB
	kolla/centos-binary-openvswitch-vswitchd            5.0.1               d8687a3c181d        27 hours ago        471MB
	kolla/centos-binary-cloudkitty-base                 5.0.1               63cf4788ff6d        27 hours ago        686MB
	kolla/centos-binary-watcher-base                    5.0.1               cd7ecc5012b9        27 hours ago        790MB
	kolla/centos-binary-trove-base                      5.0.1               d2ef7e17e058        27 hours ago        687MB
	kolla/centos-binary-gnocchi-base                    5.0.1               01920422c663        27 hours ago        1GB
	kolla/centos-binary-nova-base                       5.0.1               123124c05b96        27 hours ago        743MB
	kolla/centos-binary-manila-base                     5.0.1               ad99de2b1566        27 hours ago        714MB
	kolla/centos-binary-barbican-base                   5.0.1               2d05d14e9edb        27 hours ago        687MB
	kolla/centos-binary-zaqar                           5.0.1               a438d1fcdc16        27 hours ago        776MB
	kolla/centos-binary-cinder-base                     5.0.1               2100c9ec9c17        27 hours ago        987MB
	kolla/centos-binary-designate-base                  5.0.1               7144b9d0ca2d        27 hours ago        718MB
	kolla/centos-binary-tacker-base                     5.0.1               32982af1bf07        27 hours ago        687MB
	kolla/centos-binary-ironic-inspector                5.0.1               7e5beebffccf        27 hours ago        685MB
	kolla/centos-binary-dind                            5.0.1               a36fa2a8f3d8        27 hours ago        656MB
	kolla/centos-binary-ironic-base                     5.0.1               3d0aa9c3d9b4        27 hours ago        746MB
	kolla/centos-binary-horizon                         5.0.1               7457289af658        27 hours ago        944MB
	kolla/centos-binary-tempest                         5.0.1               99d39cbae2b8        27 hours ago        687MB
	kolla/centos-binary-collectd                        5.0.1               f911a619ca73        27 hours ago        680MB
	kolla/centos-binary-opendaylight                    5.0.1               bf6e00350a39        27 hours ago        1.09GB
	kolla/centos-binary-neutron-base                    5.0.1               2e0ff0971695        27 hours ago        786MB
	kolla/centos-binary-novajoin-base                   5.0.1               d856e1d8e184        27 hours ago        787MB
	kolla/centos-binary-sahara-base                     5.0.1               aba95328a1c7        27 hours ago        698MB
	kolla/centos-binary-ceilometer-base                 5.0.1               59c7a733b33c        27 hours ago        700MB
	kolla/centos-binary-murano-base                     5.0.1               31062094b49c        27 hours ago        694MB
	kolla/centos-binary-panko-base                      5.0.1               00ad90c2f5ca        27 hours ago        753MB
	kolla/centos-binary-glance-base                     5.0.1               077359b4fa00        27 hours ago        821MB
	kolla/centos-binary-congress-base                   5.0.1               feb5ed973e7b        27 hours ago        698MB
	kolla/centos-binary-nova-libvirt                    5.0.1               70aa6378108d        27 hours ago        957MB
	kolla/centos-binary-sensu-client                    5.0.1               dbf804f8507d        27 hours ago        605MB
	kolla/centos-binary-magnum-base                     5.0.1               88d7ad6120f1        27 hours ago        804MB
	kolla/centos-binary-ec2-api                         5.0.1               df7e7ef577ab        27 hours ago        728MB
	kolla/centos-binary-kube-controller-manager-amd64   5.0.1               be472da2e2cc        27 hours ago        694MB
	kolla/centos-binary-swift-base                      5.0.1               4fab5a432dae        27 hours ago        685MB
	kolla/centos-binary-kolla-toolbox                   5.0.1               eb8f319e3129        27 hours ago        950MB
	kolla/centos-binary-ceph-mds                        5.0.1               0f3299d2f775        27 hours ago        752MB
	kolla/centos-binary-ceph-rgw                        5.0.1               260b336c5473        27 hours ago        752MB
	kolla/centos-binary-cephfs-fuse                     5.0.1               646e26b5758f        27 hours ago        752MB
	kolla/centos-binary-ceph-mon                        5.0.1               82eadc402283        27 hours ago        752MB
	kolla/centos-binary-ceph-osd                        5.0.1               2692afe8bf39        27 hours ago        752MB
	kolla/centos-binary-prometheus-server               5.0.1               74f6146c2e8a        27 hours ago        498MB
	kolla/centos-binary-prometheus-node-exporter        5.0.1               7b3133da99f1        27 hours ago        439MB
	kolla/centos-binary-prometheus-mysqld-exporter      5.0.1               3a9fd056d14a        27 hours ago        437MB
	kolla/centos-binary-prometheus-haproxy-exporter     5.0.1               308eebb689a6        27 hours ago        436MB
	kolla/centos-binary-kube-proxy-amd64                5.0.1               50dfd7466ba9        27 hours ago        472MB
	kolla/centos-binary-redis                           5.0.1               fce9b9bbf0e1        27 hours ago        449MB
	kolla/centos-binary-kubetoolbox                     5.0.1               95aa00876102        27 hours ago        645MB
	kolla/centos-binary-kube-scheduler-amd64            5.0.1               cb19522f451c        27 hours ago        479MB
	kolla/centos-binary-kube-discovery-amd64            5.0.1               2586f71d0b4f        27 hours ago        433MB
	kolla/centos-binary-kube-apiserver-amd64            5.0.1               b901c39662cf        27 hours ago        551MB
	kolla/centos-binary-kibana                          5.0.1               7260e99f5560        27 hours ago        583MB
	kolla/centos-binary-skydive-analyzer                5.0.1               2cf6577c0f32        27 hours ago        486MB
	kolla/centos-binary-skydive-agent                   5.0.1               177b45e792bb        27 hours ago        486MB
	kolla/centos-binary-redis-sentinel                  5.0.1               98232ea20f7c        27 hours ago        449MB
	kolla/centos-binary-mongodb                         5.0.1               c8f124029320        27 hours ago        619MB
	kolla/centos-binary-keepalived                      5.0.1               186a2782ef0a        27 hours ago        454MB
	kolla/centos-binary-openvswitch-base                5.0.1               eae13b05eedd        27 hours ago        471MB
	kolla/centos-binary-rabbitmq                        5.0.1               0ea07d9286b2        27 hours ago        507MB
	kolla/centos-binary-fluentd                         5.0.1               d1c0c952e7e3        27 hours ago        729MB
	kolla/centos-binary-openstack-base                  5.0.1               392e8386d4fd        27 hours ago        656MB
	kolla/centos-binary-iscsid                          5.0.1               2d0bab2964a0        27 hours ago        452MB
	kolla/centos-binary-multipathd                      5.0.1               4a0f11d01cff        27 hours ago        456MB
	kolla/centos-binary-helm-repository                 5.0.1               253a99b9f3b1        27 hours ago        569MB
	kolla/centos-binary-ceph-base                       5.0.1               c9379d1792f0        27 hours ago        752MB
	kolla/centos-binary-haproxy                         5.0.1               860525944498        27 hours ago        471MB
	kolla/centos-binary-elasticsearch                   5.0.1               d1b41f57c622        27 hours ago        679MB
	kolla/centos-binary-prometheus-base                 5.0.1               03fca8b594da        27 hours ago        426MB
	kolla/centos-binary-grafana                         5.0.1               ce17242cd4d9        27 hours ago        594MB
	kolla/centos-binary-influxdb                        5.0.1               aa6fcb4ef5da        27 hours ago        513MB
	kolla/centos-binary-etcd                            5.0.1               08889f5a6865        27 hours ago        488MB
	kolla/centos-binary-dnsmasq                         5.0.1               eab6170a796c        27 hours ago        447MB
	kolla/centos-binary-sensu-base                      5.0.1               4969c2ca61bf        27 hours ago        463MB
	kolla/centos-binary-zookeeper                       5.0.1               3fe23e884d00        27 hours ago        450MB
	kolla/centos-binary-kube-base                       5.0.1               c09e46dbe9ff        27 hours ago        426MB
	kolla/centos-binary-telegraf                        5.0.1               c319261d6f81        27 hours ago        487MB
	kolla/centos-binary-memcached                       5.0.1               bc029a9a82a8        27 hours ago        448MB
	kolla/centos-binary-chrony                          5.0.1               dbc835c2da0f        27 hours ago        448MB
	kolla/centos-binary-qdrouterd                       5.0.1               7d6077b2a9f4        27 hours ago        450MB
	kolla/centos-binary-tgtd                            5.0.1               9ef88eea3dc2        27 hours ago        428MB
	kolla/centos-binary-cron                            5.0.1               65f563490685        27 hours ago        447MB
	kolla/centos-binary-skydive-base                    5.0.1               3737c876365d        27 hours ago        486MB
	kolla/centos-binary-kubernetes-entrypoint           5.0.1               052585a938fc        27 hours ago        472MB
	kolla/centos-binary-redis-base                      5.0.1               6bf065ef5e04        27 hours ago        426MB
	kolla/centos-binary-base                            5.0.1               be0bd7e35356        27 hours ago        426MB

### Deploying Pike with Kolla
When I tried to do an **update** it failed to start up the new **rabbitmq** service:

	TASK [rabbitmq : Find gospel node] ******************************************************************************************************************************************************************************************************
	fatal: [localhost]: FAILED! => {"changed": true, "cmd": ["docker", "exec", "-t", "rabbitmq", "/usr/local/bin/rabbitmq_get_gospel_node"], "delta": "0:00:02.014192", "end": "2017-12-30 12:34:01.379612", "failed": true, "failed_when_result": true, "rc": 0, "start": "2017-12-30 12:33:59.365420", "stderr": "", "stderr_lines": [], "stdout": "{\"failed\": true, \"changed\": true, \"error\": \"Traceback (most recent call last):\\n  File \\\"/usr/local/bin/rabbitmq_get_gospel_node\\\", line 29, in main\\n    shell=True, stderr=subprocess.STDOUT  # nosec: this command appears\\n  File \\\"/usr/lib64/python2.7/subprocess.py\\\", line 575, in check_output\\n    raise CalledProcessError(retcode, cmd, output=output)\\nCalledProcessError: Command '/usr/sbin/rabbitmqctl eval 'rabbit_clusterer:status().'' returned non-zero exit status 2\\n\"}", "stdout_lines": ["{\"failed\": true, \"changed\": true, \"error\": \"Traceback (most recent call last):\\n  File \\\"/usr/local/bin/rabbitmq_get_gospel_node\\\", line 29, in main\\n    shell=True, stderr=subprocess.STDOUT  # nosec: this command appears\\n  File \\\"/usr/lib64/python2.7/subprocess.py\\\", line 575, in check_output\\n    raise CalledProcessError(retcode, cmd, output=output)\\nCalledProcessError: Command '/usr/sbin/rabbitmqctl eval 'rabbit_clusterer:status().'' returned non-zero exit status 2\\n\"}"]}

	NO MORE HOSTS LEFT **********************************************************************************************************************************************************************************************************************
		to retry, use: --limit @/usr/local/share/kolla-ansible/ansible/site.retry

	PLAY RECAP ******************************************************************************************************************************************************************************************************************************
	localhost                  : ok=67   changed=15   unreachable=0    failed=1

I wasn't sure why that happened so I decided to just do a brand new deployment of **5.0.1** (Later on I ran into [How to upgrade to Pike using Kolla and Kayobe](https://superuser.openstack.org/articles/upgrade-pike-using-kolla-kayobe/) and it might've been related to [this](https://github.com/stackhpc/kayobe/issues/14), but I didn't have a chance to confirm), since that looked like the [latest](https://docs.openstack.org/releasenotes/kolla/pike.html) and the instructions were very similar to **ocata**: [Quick Start Kolla Pike](https://docs.openstack.org/project-deploy-guide/kolla-ansible/pike/quickstart.html). So I destroyed the original deployment:

	root@osa:~# kolla-ansible destroy -i all-in-one --yes-i-really-really-mean-it
	Destroy Kolla containers, volumes and host configuration : ansible-playbook -i all-in-one -e @/etc/kolla/globals.yml -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  /usr/local/share/kolla-ansible/ansible/destroy.yml

	PLAY [Apply role destroy] ***************************************************************************************************************************************************************************************************************

	TASK [Gathering Facts] ******************************************************************************************************************************************************************************************************************
	ok: [localhost]

	TASK [destroy : Creating /kolla-cleanup/tools directory on node] ************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Copying validate-docker-execute.sh file] ********************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Copying cleanup-containers file] ****************************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Copying cleanup-host file] **********************************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Copying cleanup-images file] ********************************************************************************************************************************************************************************************
	skipping: [localhost]

	TASK [destroy : Destroying all Kolla containers and volumes] ****************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Removing Kolla images] **************************************************************************************************************************************************************************************************
	skipping: [localhost]

	TASK [destroy : Destroying Kolla host configuration] ************************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [destroy : Destroying kolla-cleanup folder] ****************************************************************************************************************************************************************************************
	changed: [localhost]

	PLAY RECAP ******************************************************************************************************************************************************************************************************************************
	localhost                  : ok=8    changed=7    unreachable=0    failed=0

Then doing a **precheck** looked good:

	root@osa:~# kolla-ansible prechecks -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one
	Pre-deployment checking : ansible-playbook -i all-in-one -e @/etc/kolla/globals.yml -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  -e action=precheck /usr/local/share/kolla-ansible/ansible/site.yml
	 [WARNING]: Found variable using reserved name: action
	..
	..
	TASK [octavia : include] ****************************************************************************************************************************************************************************************************************
	skipping: [localhost]

	PLAY [Apply role zun] *******************************************************************************************************************************************************************************************************************
	skipping: no hosts matched

	PLAY [Apply role skydive] ***************************************************************************************************************************************************************************************************************
	skipping: no hosts matched

	PLAY RECAP ******************************************************************************************************************************************************************************************************************************
	localhost                  : ok=45   changed=0    unreachable=0    failed=0

and then the new deploy:

	root@osa:~# kolla-ansible deploy -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one
	Deploying Playbooks : ansible-playbook -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one -e @/etc/kolla/globals.yml -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  -e action=deploy /usr/local/share/kolla-ansible/ansible/site.yml
	 [WARNING]: Found variable using reserved name: action


	PLAY [Gather facts for all hosts] *******************************************************************************************************************************************************************************************************

	TASK [setup] ****************************************************************************************************************************************************************************************************************************
	ok: [localhost]
	..
	..
	TASK [horizon : Check horizon container] ************************************************************************************************************************************************************************************************
	changed: [localhost]

	TASK [horizon : include] ****************************************************************************************************************************************************************************************************************
	skipping: [localhost]

	TASK [horizon : include] ****************************************************************************************************************************************************************************************************************
	skipping: [localhost]

	RUNNING HANDLER [horizon : Restart horizon container] ***********************************************************************************************************************************************************************************
	changed: [localhost]
	...
	...
	TASK [skydive : include] ****************************************************************************************************************************************************************************************************************
	skipping: [localhost]

	PLAY RECAP ******************************************************************************************************************************************************************************************************************************
	localhost                  : ok=224  changed=140  unreachable=0    failed=0


And here are the running containers after the *deploy* is finished:

	root@osa:~# docker ps
	CONTAINER ID        IMAGE                                                 COMMAND             CREATED              STATUS              PORTS               NAMES
	407f0b50276c        kolla/centos-binary-horizon:5.0.1                     "kolla_start"       About a minute ago   Up About a minute                       horizon
	d1a7732b9f94        kolla/centos-binary-heat-engine:5.0.1                 "kolla_start"       About a minute ago   Up About a minute                       heat_engine
	8c1a7438b965        kolla/centos-binary-heat-api-cfn:5.0.1                "kolla_start"       About a minute ago   Up About a minute                       heat_api_cfn
	eff2ec58a867        kolla/centos-binary-heat-api:5.0.1                    "kolla_start"       About a minute ago   Up About a minute                       heat_api
	44fcfb23da69        kolla/centos-binary-neutron-metadata-agent:5.0.1      "kolla_start"       2 minutes ago        Up 2 minutes                            neutron_metadata_agent
	d9d059a3892f        kolla/centos-binary-neutron-l3-agent:5.0.1            "kolla_start"       2 minutes ago        Up 2 minutes                            neutron_l3_agent
	3e5324911abc        kolla/centos-binary-neutron-dhcp-agent:5.0.1          "kolla_start"       2 minutes ago        Up 2 minutes                            neutron_dhcp_agent
	fb00e5e030de        kolla/centos-binary-neutron-openvswitch-agent:5.0.1   "kolla_start"       2 minutes ago        Up 2 minutes                            neutron_openvswitch_agent
	23d3c895ad80        kolla/centos-binary-neutron-server:5.0.1              "kolla_start"       2 minutes ago        Up 2 minutes                            neutron_server
	2087adc1b549        kolla/centos-binary-openvswitch-vswitchd:5.0.1        "kolla_start"       2 minutes ago        Up 2 minutes                            openvswitch_vswitchd
	384f1d301c7a        kolla/centos-binary-openvswitch-db-server:5.0.1       "kolla_start"       2 minutes ago        Up 2 minutes                            openvswitch_db
	ba7eaf9fb723        kolla/centos-binary-nova-compute:5.0.1                "kolla_start"       13 minutes ago       Up 13 minutes                           nova_compute
	64dc377ea66b        kolla/centos-binary-nova-novncproxy:5.0.1             "kolla_start"       13 minutes ago       Up 13 minutes                           nova_novncproxy
	04051e6e81f1        kolla/centos-binary-nova-consoleauth:5.0.1            "kolla_start"       13 minutes ago       Up 13 minutes                           nova_consoleauth
	436284715e61        kolla/centos-binary-nova-conductor:5.0.1              "kolla_start"       13 minutes ago       Up 13 minutes                           nova_conductor
	9ec5efca879c        kolla/centos-binary-nova-scheduler:5.0.1              "kolla_start"       13 minutes ago       Up 13 minutes                           nova_scheduler
	3c65f2be8ef7        kolla/centos-binary-nova-api:5.0.1                    "kolla_start"       13 minutes ago       Up 13 minutes                           nova_api
	651d8e83ca10        kolla/centos-binary-nova-placement-api:5.0.1          "kolla_start"       13 minutes ago       Up 13 minutes                           placement_api
	7d275d989ee9        kolla/centos-binary-nova-libvirt:5.0.1                "kolla_start"       13 minutes ago       Up 13 minutes                           nova_libvirt
	6404e330831f        kolla/centos-binary-nova-ssh:5.0.1                    "kolla_start"       13 minutes ago       Up 13 minutes                           nova_ssh
	680016b569a0        kolla/centos-binary-glance-registry:5.0.1             "kolla_start"       14 minutes ago       Up 14 minutes                           glance_registry
	f7ed0bebcc4c        kolla/centos-binary-glance-api:5.0.1                  "kolla_start"       14 minutes ago       Up 14 minutes                           glance_api
	9af905247583        kolla/centos-binary-keystone:5.0.1                    "kolla_start"       15 minutes ago       Up 15 minutes                           keystone
	f850f31ac7d3        kolla/centos-binary-rabbitmq:5.0.1                    "kolla_start"       15 minutes ago       Up 15 minutes                           rabbitmq
	c8cdda6258b4        kolla/centos-binary-mariadb:5.0.1                     "kolla_start"       15 minutes ago       Up 15 minutes                           mariadb
	c8e2e8dfebe7        kolla/centos-binary-memcached:5.0.1                   "kolla_start"       16 minutes ago       Up 16 minutes                           memcached
	31d6d371a39a        kolla/centos-binary-keepalived:5.0.1                  "kolla_start"       16 minutes ago       Up 16 minutes                           keepalived
	83384fc70d73        kolla/centos-binary-haproxy:5.0.1                     "kolla_start"       16 minutes ago       Up 16 minutes                           haproxy
	a278b82cafd0        kolla/centos-binary-cron:5.0.1                        "kolla_start"       16 minutes ago       Up 16 minutes                           cron
	2906c3737eaa        kolla/centos-binary-kolla-toolbox:5.0.1               "kolla_start"       16 minutes ago       Up 16 minutes                           kolla_toolbox
	48b819ca400c        kolla/centos-binary-fluentd:5.0.1                     "kolla_start"       16 minutes ago       Up 16 minutes                           fluentd

Then I was able to re-create the rest of the config:

	root@osa:~# kolla-ansible post-deploy
	root@osa:~# pip install -U python-openstackclient
	root@osa:~# cp /usr/local/share/kolla-ansible/init-runonce .
	root@osa:~# vi init-runonce
	root@osa:~# ./init-runonce
	root@osa:~# openstack server create \
	>     --image cirros \
	>     --flavor m1.tiny \
	>     --key-name mykey \
	>     --nic net-id=df9a9e66-ad7e-4362-ad6f-998c541f6577 \
	>     demo1
	root@osa:~# openstack server list
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| ID                                   | Name  | Status | Networks             | Image  | Flavor  |
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	| 7ce3b0a3-73b0-4c52-ab68-60118ae5b874 | demo1 | ACTIVE | demo-net=172.24.0.11 | cirros | m1.tiny |
	+--------------------------------------+-------+--------+----------------------+--------+---------+
	root@osa:~# openstack console log show demo1 | tail -40
	/run/cirros/datasource/data/user-data was not '#!' or executable
	=== system information ===
	Platform: RDO OpenStack Compute
	Container: none
	Arch: x86_64
	CPU(s): 1 @ 3407.936 MHz
	Cores/Sockets/Threads: 1/1/1
	Virt-type: AMD-V
	RAM Size: 491MB
	Disks:
	NAME MAJ:MIN       SIZE LABEL         MOUNTPOINT
	vda  253:0   1073741824
	vda1 253:1   1061061120 cirros-rootfs /
	=== sshd host keys ===
	-----BEGIN SSH HOST KEY KEYS-----
	ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgwC3NvbQahyHLeoZRsUwQ3+kcxKw+L9i6vjT17Z2wZSgJgM9vbLzKiitXuIuV/kuEO9dyrUcdXDTHGX7qfigQ0lqS4uVz+lxL7qmv+mVgeoRSb872Lr7CIoxq/GgpWSc7kf2GzDZctgHlLIslmRVr8Szia8RUzK0UbvMfng+LXgI2Kw1 root@demo1
	ssh-dss AAAAB3NzaC1kc3MAAACBAKezGJp3orZoAZa+rilDsQ0V/MYe4ZdGBYbVW0CQyXeBwtvvQCo65+HzuiKQJW+su6qqcdjRkt/C6hd68Y2cIcV3QqrcyiTay4xvyQqeC/DCFYML/mmI2keMd9kyldLrXX70RW0npVHZt/70DaLW3AlPzujJwjJz1U8+oTTaa3HbAAAAFQCwSj/zQJ66Kp+4A1l87Tidqw8GIwAAAIA0lfyGBo8uFAm8ATivYMuTMZr0uJCdgKcADwq3yEC3ThkSG8I2neLoprgb71mg+HeTetf1MUG9kAxE237bBvEKau/97LB/ur90AXXbYLZzptNf4UwG3MRqiDfiQjz2yw+xnt6wGnx9JZR7B5xABdTiPkJvGqG9am9C2/dwefhtbwAAAIEAkQ+woALAt01DHJqDYl36sFf1lNzDfB/WaKE/9i9/9Ng+fzjY1MYTdesyXzG5tZkyper3G9bETB75KxuYEX4yXa50rwFCMdgb3Rand3D8fQporeeJdAGlxQyFOwJ211xNOESFFz7BhvXn6Nt6V/QNpSstFjJc8tglcwM5XH1MP4I= root@demo1
	-----END SSH HOST KEY KEYS-----
	=== network info ===
	if-info: lo,up,127.0.0.1,8,::1
	if-info: eth0,up,172.24.0.11,24,fe80::f816:3eff:fe94:91c0
	ip-route:default via 172.24.0.1 dev eth0
	ip-route:169.254.169.254 via 172.24.0.2 dev eth0
	ip-route:172.24.0.0/24 dev eth0  src 172.24.0.11
	=== datasource: ec2 net ===
	instance-id: i-00000001
	name: N/A
	availability-zone: nova
	local-hostname: demo1.novalocal
	launch-index: 0
	=== cirros: current=0.3.5 latest=0.4.0 uptime=12.01 ===
	  ____               ____  ____
	 / __/ __ ____ ____ / __ \/ __/
	/ /__ / // __// __// /_/ /\ \
	\___//_//_/  /_/   \____/___/
	   http://cirros-cloud.net


	login as 'cirros' user. default password: 'cubswin:)'. use 'sudo' for root.

I was at the state where I was before the update.

### Deploying with the "pike" tag

Later on I realized that the **pike** tag is used instead of **5.0.0** in [dockerhub](https://hub.docker.com/r/kolla/centos-binary-nova-api/tags/). So I updated the globals files:

	root@osa:~# grep openstack_release /etc/kolla/globals.yml
	#openstack_release: "5.0.1"
	openstack_release: "pike"

And then the **pull** worked:

	root@osa:~# kolla-ansible pull
	Pulling Docker images : ansible-playbook -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one -e @/etc/kolla/globals.yml -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  -e action=pull /usr/local/share/kolla-ansible/ansible/site.yml
	 [WARNING]: Found variable using reserved name: action


	PLAY [Gather facts for all hosts] *******************************************************************************************************************************************************************************************************

	TASK [setup] ****************************************************************************************************************************************************************************************************************************
	ok: [localhost]
	...
	...
	TASK [common : Pulling common images] ***************************************************************************************************************************************************************************************************
	changed: [localhost] => (item={'key': u'cron', 'value': {u'environment': {u'DUMMY_ENVIRONMENT': u'kolla_useless_env'}, u'image': u'kolla/centos-binary-cron:pike', u'volumes': [u'/etc/kolla//cron/:/var/lib/kolla/config_files/:ro', u'/etc/localtime:/etc/localtime:ro', u'kolla_logs:/var/log/kolla/'], u'container_name': u'cron'}})
	changed: [localhost] => (item={'key': u'fluentd', 'value': {u'environment': {u'KOLLA_CONFIG_STRATEGY': u'COPY_ALWAYS'}, u'image': u'kolla/centos-binary-fluentd:pike', u'volumes': [u'/etc/kolla//fluentd/:/var/lib/kolla/config_files/:ro', u'/etc/localtime:/etc/localtime:ro', u'kolla_logs:/var/log/kolla/'], u'container_name': u'fluentd'}})
	changed: [localhost] => (item={'key': u'kolla-toolbox', 'value': {u'environment': {u'ANSIBLE_LIBRARY': u'/usr/share/ansible', u'ANSIBLE_NOCOLOR': u'1'}, u'image': u'kolla/centos-binary-kolla-toolbox:pike', u'privileged': True, u'volumes': [u'/etc/kolla//kolla-toolbox/:/var/lib/kolla/config_files/:ro', u'/etc/localtime:/etc/localtime:ro', u'/dev/:/dev/', u'/run/:/run/:shared', u'kolla_logs:/var/log/kolla/'], u'container_name': u'kolla_toolbox'}})

	TASK [common : Registering common role has run] *****************************************************************************************************************************************************************************************
	ok: [localhost]
	...
	...
	TASK [skydive : include] ****************************************************************************************************************************************************************************************************************
	skipping: [localhost]

	PLAY RECAP ******************************************************************************************************************************************************************************************************************************
	localhost                  : ok=28   changed=12   unreachable=0    failed=0

Then doing a re-deploy:

	root@osa:~# kolla-ansible destroy -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one --yes-i-really-really-mean-it
	root@osa:~# kolla-ansible deploy -i /usr/local/share/kolla-ansible/ansible/inventory/all-in-one

Worked out and I had the following versions running:

	root@osa:~# docker ps
	CONTAINER ID        IMAGE                                                COMMAND             CREATED              STATUS              PORTS               NAMES
	e80c8c34c7b2        kolla/centos-binary-horizon:pike                     "kolla_start"       40 seconds ago       Up 39 seconds                           horizon
	853fb098b689        kolla/centos-binary-heat-engine:pike                 "kolla_start"       47 seconds ago       Up 46 seconds                           heat_engine
	668f74204b1d        kolla/centos-binary-heat-api-cfn:pike                "kolla_start"       48 seconds ago       Up 47 seconds                           heat_api_cfn
	f2e0eda99aaa        kolla/centos-binary-heat-api:pike                    "kolla_start"       49 seconds ago       Up 48 seconds                           heat_api
	b8330cfcab88        kolla/centos-binary-neutron-metadata-agent:pike      "kolla_start"       About a minute ago   Up About a minute                       neutron_metadata_agent
	b303160017d1        kolla/centos-binary-neutron-l3-agent:pike            "kolla_start"       About a minute ago   Up About a minute                       neutron_l3_agent
	8aafaa7e1df7        kolla/centos-binary-neutron-dhcp-agent:pike          "kolla_start"       About a minute ago   Up About a minute                       neutron_dhcp_agent
	18dda178d1d8        kolla/centos-binary-neutron-openvswitch-agent:pike   "kolla_start"       About a minute ago   Up About a minute                       neutron_openvswitch_agent
	2663ea7fbc52        kolla/centos-binary-neutron-server:pike              "kolla_start"       About a minute ago   Up About a minute                       neutron_server
	3dfdbf997c18        kolla/centos-binary-openvswitch-vswitchd:pike        "kolla_start"       2 minutes ago        Up About a minute                       openvswitch_vswitchd
	80e7262c9e3d        kolla/centos-binary-openvswitch-db-server:pike       "kolla_start"       2 minutes ago        Up 2 minutes                            openvswitch_db
	d1c24b538372        kolla/centos-binary-nova-compute:pike                "kolla_start"       2 minutes ago        Up 2 minutes                            nova_compute
	ae12ff8d5a0d        kolla/centos-binary-nova-novncproxy:pike             "kolla_start"       2 minutes ago        Up 2 minutes                            nova_novncproxy
	0051f11a399f        kolla/centos-binary-nova-consoleauth:pike            "kolla_start"       2 minutes ago        Up 2 minutes                            nova_consoleauth
	f834fbfe0aea        kolla/centos-binary-nova-conductor:pike              "kolla_start"       2 minutes ago        Up 2 minutes                            nova_conductor
	93b4e465d08c        kolla/centos-binary-nova-scheduler:pike              "kolla_start"       2 minutes ago        Up 2 minutes                            nova_scheduler
	685a019fe51d        kolla/centos-binary-nova-api:pike                    "kolla_start"       2 minutes ago        Up 2 minutes                            nova_api
	43a90fa504e8        kolla/centos-binary-nova-placement-api:pike          "kolla_start"       2 minutes ago        Up 2 minutes                            placement_api
	667cf68fb857        kolla/centos-binary-nova-libvirt:pike                "kolla_start"       2 minutes ago        Up 2 minutes                            nova_libvirt
	dc32facdac9e        kolla/centos-binary-nova-ssh:pike                    "kolla_start"       2 minutes ago        Up 2 minutes                            nova_ssh
	67fbba06ca23        kolla/centos-binary-glance-registry:pike             "kolla_start"       3 minutes ago        Up 3 minutes                            glance_registry
	b691c85041c9        kolla/centos-binary-glance-api:pike                  "kolla_start"       3 minutes ago        Up 3 minutes                            glance_api
	e900317f4b71        kolla/centos-binary-keystone:pike                    "kolla_start"       4 minutes ago        Up 4 minutes                            keystone
	9d6d82590621        kolla/centos-binary-rabbitmq:pike                    "kolla_start"       4 minutes ago        Up 4 minutes                            rabbitmq
	1ed59fba8e11        kolla/centos-binary-mariadb:pike                     "kolla_start"       4 minutes ago        Up 4 minutes                            mariadb
	74b6e6ae0557        kolla/centos-binary-memcached:pike                   "kolla_start"       5 minutes ago        Up 5 minutes                            memcached
	6276b52a4c7f        kolla/centos-binary-keepalived:pike                  "kolla_start"       5 minutes ago        Up 5 minutes                            keepalived
	099c74158151        kolla/centos-binary-haproxy:pike                     "kolla_start"       5 minutes ago        Up 5 minutes                            haproxy
	ece2011696f3        kolla/centos-binary-cron:pike                        "kolla_start"       5 minutes ago        Up 5 minutes                            cron
	4cb41bdd9ff1        kolla/centos-binary-kolla-toolbox:pike               "kolla_start"       5 minutes ago        Up 5 minutes                            kolla_toolbox
	5c6e20f6c6f2        kolla/centos-binary-fluentd:pike                     "kolla_start"       5 minutes ago        Up 5 minutes                            fluentd

Logging into the **horizon** dashboard, I saw all the components:

![openstack-horizon-pike.png](https://raw.githubusercontent.com/elatov/upload/master/kolla-pike/openstack-horizon-pike.png)
