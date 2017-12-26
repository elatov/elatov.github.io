---
published: false
layout: post
title: "Deploy PupppetDB and PuppetBoard with Docker Compose"
author: Karim Elatov
categories: [os,containers]
tags: [puppet,docker-compose,puppetdb]
---
### Puppet in Docker
Most of the instructions/examples are available at [Puppet-in-Docker examples](https://github.com/puppetlabs/puppet-in-docker-examples) and a nice example of the **docker-compose** file is [here](https://github.com/puppetlabs/puppet-in-docker-examples/tree/master/compose).

### Docker-Compose for Puppet

Since I already had a **puppet master** I wanted to deploy the other components in **docker** and connect the running **puppet master** to this instance of **puppetdb**. So I ended with the following **docker-compose** file:

	<> cat docker-compose.yml
	version: '2'
	
	services:
	
	  postgres:
	    container_name: postgres
	    hostname: postgres
	    image: puppet/puppetdb-postgres
	    restart: always
	    environment:
	      - POSTGRES_PASSWORD=puppetdb
	      - POSTGRES_USER=puppetdb
	    ports:
	      - 5432:5432
	    volumes:
	      - /data/shared/puppetboard/postgres/data:/var/lib/postgresql/data/
	    network_mode: bridge
	
	  puppetdb:
	    container_name: puppetdb
	    hostname: puppetdb
	    image: puppet/puppetdb
	    restart: always
	    ports:
	      - 18080:8080
	      - 18081:8081
	    volumes:
	      - /data/shared/puppetboard/puppetdb/ssl:/etc/puppetlabs/puppet/ssl/
	    network_mode: bridge
	    extra_hosts:
	       - "postgres:192.168.1.106"
	
	  puppetboard:
	    container_name: puppetboard
	    hostname: puppetboard
	    image: puppet/puppetboard
	    restart: always
	    environment:
	      - PUPPETDB_HOST=192.168.1.106
	      - PUPPETDB_PORT=18080
	      - PUPPETDB_SSL_VERIFY=False
	    ports:
	      - 8001:8000
	    network_mode: bridge

And then I just started it up:

	<> docker-compose up -d
	Creating puppetdb
	Creating postgres
	Creating puppetboard

And I saw all 3 components running:

	<> docker-compose ps
	   Name                  Command               State                       Ports
	-----------------------------------------------------------------------------------------------------
	postgres      docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
	puppetboard   /bin/sh -c /usr/bin/gunico ...   Up      0.0.0.0:8001->8000/tcp
	puppetdb      dumb-init /docker-entrypoi ...   Up      0.0.0.0:8085->8080/tcp, 0.0.0.0:8086->8081/tcp

### Modifications to the default Puppet Example
I ended up making some changes to the **docker-compose** file to accomodate my setup.

#### PuppetDB Connects to Puppet Master

By default **puppetdb** connects to machine called **puppet** in DNS and tries to do a config apply (it uses [Installing PuppetDB via Puppet module](https://puppet.com/docs/puppetdb/5.1/install_via_module.html) method for the install of **puppetdb**):

	<> docker-compose exec puppetdb /opt/puppetlabs/puppet/bin/puppet config print server
	puppet

So make sure you can resolve **puppet** in DNS (this was already in place from my original deployment [Setting Up Open Source Puppet Master on CentOS 7](/2014/08/setting-up-puppet-master-on-centos-7/)):

	<> host puppet
	puppet has address 10.0.0.6

Also make sure have a **default** node definition on your **puppet master**. [Here](https://github.com/puppetlabs/puppet-in-docker-examples/blob/master/compose/code/environments/production/manifests/site.pp) is a simple example taken from the above page:

	<> cat /etc/puppetlabs/code/environments/production/manifests/site.pp
	File { backup => false }
	
	node default {
	  file { '/tmp/puppet-in-docker':
	    ensure  => present,
	    content => 'This file is for demonstration purposes only',
	  }
	}

After you power on the containers, make sure the **logs** look good:

	<> docker-compose logs -f puppetdb
	Attaching to puppetdb
	puppetdb       | Info: Loading facts
	puppetdb       | Info: Caching catalog for puppetdb
	puppetdb       | Info: Applying configuration version '1514155375'
	puppetdb       | Notice: /Stage[main]/Main/Node[default]/File[/tmp/puppet-in-docker]/ensure: defined content as '{md5}938727d2f2612b38d783932417edf030'
	puppetdb       | Info: Creating state file /opt/puppetlabs/puppet/cache/state/state.yaml
	puppetdb       | Notice: Applied catalog in 0.07 seconds
	puppetdb       | PEM files in /etc/puppetlabs/puppetdb/ssl are missing, we will move them into place for you
	...
	...
	puppetdb       | 2017-12-24 22:43:27,979 INFO  [p.p.c.services] PuppetDB version 5.1.1
	puppetdb       | 2017-12-24 22:43:27,980 WARN  [c.z.h.HikariConfig] The initializationFailFast propery is deprecated, see initializationFailTimeout
	puppetdb       | 2017-12-24 22:43:27,980 INFO  [c.z.h.HikariDataSource] PDBMigrationsPool - Starting...
	puppetdb       | 2017-12-24 22:43:27,981 INFO  [c.z.h.HikariDataSource] PDBMigrationsPool - Start completed.
	puppetdb       | 2017-12-24 22:43:28,036 INFO  [c.z.h.p.PoolBase] PDBMigrationsPool - Driver does not support get/set network timeout for connections. (Method org.postgresql.jdbc.PgConnection.getNetworkTimeout() is not yet implemented.)
	puppetdb       | 2017-12-24 22:43:28,091 INFO  [c.z.h.p.PoolBase] PDBWritePool - Driver does not support get/set network timeout for connections. (Method org.postgresql.jdbc.PgConnection.getNetworkTimeout() is not yet implemented.)
	puppetdb       | 2017-12-24 22:43:28,091 INFO  [c.z.h.p.PoolBase] PDBReadPool - Driver does not support get/set network timeout for connections. (Method org.postgresql.jdbc.PgConnection.getNetworkTimeout() is not yet implemented.)
	puppetdb       | 2017-12-24 22:43:28,112 INFO  [p.p.s.migrate] Applying database migration version 28
	puppetdb       | 2017-12-24 22:43:28,533 INFO  [p.p.s.migrate] Applying database migration version 29
	puppetdb       | 2017-12-24 22:43:28,832 INFO  [p.p.s.migrate] Applying database migration version 30
	puppetdb       | 2017-12-24 22:43:28,833 INFO  [p.p.s.migrate] Applying database migration version 31
	..
	..
	puppetdb       | 2017-12-24 22:43:29,405 INFO  [p.p.s.migrate] Cleaning up orphaned edges
	puppetdb       | 2017-12-24 22:43:29,420 INFO  [p.p.s.migrate] Applying database migration version 61
	puppetdb       | 2017-12-24 22:43:29,434 INFO  [p.p.s.migrate] Applying database migration version 62
	puppetdb       | 2017-12-24 22:43:29,444 INFO  [p.p.s.migrate] Applying database migration version 63
	puppetdb       | 2017-12-24 22:43:29,454 INFO  [p.p.s.migrate] Applying database migration version 64
	puppetdb       | 2017-12-24 22:43:29,455 INFO  [p.p.s.migrate] [1/8] Cleaning up unreferenced facts...
	puppetdb       | 2017-12-24 22:43:29,456 INFO  [p.p.s.migrate] [2/8] Creating new fact storage tables...
	puppetdb       | 2017-12-24 22:43:29,467 INFO  [p.p.s.migrate] [3/8] Copying unique fact values into fact_values
	puppetdb       | 2017-12-24 22:43:29,468 INFO  [p.p.s.migrate] [4/8] Reconstructing facts to refer to fact_values...
	puppetdb       | 2017-12-24 22:43:29,478 INFO  [p.p.s.migrate] [5/8] Cleaning up duplicate null values...
	puppetdb       | 2017-12-24 22:43:29,479 INFO  [p.p.s.migrate]   ... none found
	puppetdb       | 2017-12-24 22:43:29,480 INFO  [p.p.s.migrate] [6/8] Computing fact value hashes...
	puppetdb       | 2017-12-24 22:43:29,489 INFO  [p.p.s.migrate] [7/8] Indexing fact_values table...
	puppetdb       | 2017-12-24 22:43:29,513 INFO  [p.p.s.migrate] [8/8] Indexing facts table...
	puppetdb       | 2017-12-24 22:43:29,538 INFO  [p.p.s.migrate] Applying database migration version 65
	puppetdb       | 2017-12-24 22:43:29,555 INFO  [p.p.s.migrate] Updating table statistics for: fact_paths, fact_values, facts, report_statuses, value_types
	puppetdb       | 2017-12-24 22:43:29,588 INFO  [p.p.s.migrate] Creating additional index `fact_paths_path_trgm`
	puppetdb       | 2017-12-24 22:43:29,592 INFO  [p.p.s.migrate] Creating additional index `fact_values_string_trgm`
	puppetdb       | 2017-12-24 22:43:29,594 INFO  [p.p.s.migrate] Creating additional index `packages_name_trgm`
	puppetdb       | 2017-12-24 22:43:29,597 INFO  [c.z.h.HikariDataSource] PDBMigrationsPool - Shutdown initiated...
	puppetdb       | 2017-12-24 22:43:29,628 INFO  [c.z.h.HikariDataSource] PDBMigrationsPool - Shutdown completed.
	puppetdb       | 2017-12-24 22:43:29,688 INFO  [p.p.c.services] Starting sweep of stale nodes (threshold: 7 days)
	puppetdb       | 2017-12-24 22:43:29,695 INFO  [p.p.pdb-routing] PuppetDB finished starting, disabling maintenance mode
	puppetdb       | 2017-12-24 22:43:29,698 INFO  [p.p.dashboard] Redirecting / to the PuppetDB dashboard
	puppetdb       | 2017-12-24 22:43:29,701 INFO  [o.e.j.s.h.ContextHandler] Started o.e.j.s.h.ContextHandler@1fb67d4{/,null,AVAILABLE}
	puppetdb       | 2017-12-24 22:43:29,706 INFO  [p.p.c.services] Finished sweep of stale nodes (threshold: 7 days)
	puppetdb       | 2017-12-24 22:43:29,712 INFO  [p.p.c.services] Starting purge deactivated and expired nodes (threshold: 14 days)
	puppetdb       | 2017-12-24 22:43:29,723 INFO  [p.p.c.services] Finished purge deactivated and expired nodes (threshold: 14 days)
	puppetdb       | 2017-12-24 22:43:29,724 INFO  [p.p.c.services] Starting sweep of stale reports (threshold: 14 days)
	puppetdb       | 2017-12-24 22:43:29,729 INFO  [p.p.c.services] Finished sweep of stale reports (threshold: 14 days)
	puppetdb       | 2017-12-24 22:43:29,730 INFO  [p.p.c.services] Starting gc packages
	puppetdb       | 2017-12-24 22:43:29,734 INFO  [p.p.c.services] Finished gc packages
	puppetdb       | 2017-12-24 22:43:29,735 INFO  [p.p.c.services] Starting database garbage collection
	puppetdb       | 2017-12-24 22:43:29,750 INFO  [p.p.c.services] Finished database garbage collection

Also if you don't have auto signing configured on the **puppet master**, login and sign the cert:

	<> sudo /opt/puppetlabs/bin/puppet cert list
	  "puppetdb"     (SHA256) 64:E5:12:7B:B0:E9:E8:C3:E2:AC:4B:5E:B1:77:A6:1A:20:77:C2:0F:B8:9F:55:BA:24:6C:5D:D7:87:CE:5D:1F
	<> sudo /opt/puppetlabs/bin/puppet cert sign puppetdb
	Signing Certificate Request for:
	  "puppetdb" (SHA256) 64:E5:12:7B:B0:E9:E8:C3:E2:AC:4B:5E:B1:77:A6:1A:20:77:C2:0F:B8:9F:55:BA:24:6C:5D:D7:87:CE:5D:1F
	Notice: Signed certificate request for puppetdb

#### PuppetDB Connects to Postgres
Another note is that the **puppetdb** node connects to a machine called **postgres**:

	<> docker-compose exec puppetdb grep subname /etc/puppetlabs/puppetdb/conf.d/database.conf
	  subname: ${PUPPETDB_DATABASE_CONNECTION}
	<> docker-compose exec puppetdb env | grep PUPPETDB
	PUPPETDB_VERSION=5.1.1
	PUPPETDB_DATABASE_CONNECTION=//postgres:5432/puppetdb
	PUPPETDB_USER=puppetdb
	PUPPETDB_PASSWORD=puppetdb
	PUPPETDB_JAVA_ARGS=-Djava.net.preferIPv4Stack=true -Xms256m -Xmx256m  
  
So make sure the container can reach that (or change it to whatever you want). I just added an **extra_hosts** option (in the **docker-compose** file) and pointed to the **docker** host and that worked for me (for some reason the **links** feature didn't update the **/etc/hosts** file for me, plus it sounds like the **links** feature is not recommended: [Compose file version 2 reference](https://docs.docker.com/compose/compose-file/compose-file-v2/#links)).

#### Puppet Master Connects to PuppetDB
Make sure the **puppet master** can resolve the name of **puppetdb** to the docker host:

	<> host puppetdb
	puppetdb.kar.int has address 192.168.1.106

Else you will run into an error like this:

	2017-12-24 16:29:10,336 ERROR [qtp1112728823-65] [c.p.h.c.i.PersistentSyncHttpClient] Error executing http request
	javax.net.ssl.SSLPeerUnverifiedException: Host name '192.168.1.106' does not match the certificate subject provided by the peer (CN=puppetdb)
	..
	..
	2017-12-24 16:29:10,338 WARN  [qtp1112728823-65] [puppetserver] Puppet Error connecting to 192.168.1.106 on 18081 at route /pdb/cmd/v1?checksum=36ce279d4e2894a9c313990deb2044bd01a5739c&version=8&certname=m2.kar.int&command=store_report&producer-timestamp=1514158150, error message received was 'Error executing http request'. Failing over to the next PuppetDB server_url in the 'server_urls' list
	2017-12-24 16:29:10,339 ERROR [qtp1112728823-65] [puppetserver] Puppet Failed to execute '/pdb/cmd/v1?checksum=36ce279d4e2894a9c313990deb2044bd01a5739c&version=8&certname=m2.kar.int&command=store_report&producer-timestamp=1514158150' on at least 1 of the following 'server_urls': https://192.168.1.106:18081

This is discussed in [Troubleshooting](https://github.com/puppetlabs/puppet-in-docker-examples/tree/master/compose#troubleshooting) section. You could probably modify the **certname** config on the **puppetdb** container:

	<> docker-compose exec puppetdb head -1 /etc/puppetlabs/puppet/puppet.conf
	certname = puppetdb

And point it to the name of the **docker** host and it would probably work out. My **docker** host was already managed by **puppet master** and I didn't want them to conflict.

#### Make sure you can reach PuppetDB from the Puppet Master

At this point the **puppet master** should be able to reach the **puppetdb** port with **telnet**:

	<> telnet ub.kar.int 18081
	Trying 192.168.1.106...
	Connected to ub.kar.int.
	Escape character is '^]'.
	^CConnection closed by foreign host.

### Configure Puppet Master to use PuppetDB
Now let's connect the running **puppet master** to deployed containers. Most of the instructions are available at [Connecting Puppet masters to PuppetDB](https://puppet.com/docs/puppetdb/latest/connect_puppet_master.html). First let's install the necessary plugins on the **puppet master**:

	<> sudo puppet resource package puppetdb-termini ensure=latest
	[sudo] password for elatov:
	Notice: /Package[puppetdb-termini]/ensure: created
	package { 'puppetdb-termini':
	  ensure => '5.1.3-1.el7',
	}

Next let's create the config files, first figure out where the config directory is:

	<> sudo puppet config print confdir
	/etc/puppetlabs/puppet

Now let's point to the **puppetdb** server:

	<> cat /etc/puppetlabs/puppet/puppetdb.conf
	[main]
	server_urls = https://puppetdb:18081

Next enable the storing of configs and reports in **puppetdb**:

	<> cat /etc/puppetlabs/puppet/puppet.conf
	[master]
	  storeconfigs = true
	  storeconfigs_backend = puppetdb
	  reports = tagmail,puppetdb

And create an appropriate **routes.yaml** file:

	<> cat /etc/puppetlabs/puppet/routes.yaml
	---
	master:
	  facts:
	    terminus: puppetdb
	    cache: yaml
	    
Finally restart the **puppet master** service to apply all the changes:

	<> sudo systemctl restart puppetserver

Then login to any **puppet node** and do a test run (`sudo puppet agent -t`), and in the logs on the **puppet master** you should see something like this:

	<> tail -f /var/log/puppetlabs/puppetserver/puppetserver.log
	2017-12-24 16:30:18,352 INFO  [qtp1910538382-61] [puppetserver] Puppet Compiled catalog for m2.kar.int in environment production in 2.69 seconds
	2017-12-24 16:30:18,353 INFO  [qtp1910538382-61] [puppetserver] Puppet Caching catalog for m2.kar.int
	2017-12-24 16:30:18,663 INFO  [qtp1910538382-61] [puppetserver] Puppet 'replace_catalog' command for m2.kar.int submitted to PuppetDB with UUID 74cfbe17-a41c-4e1c-b9df-c41aee595d7d
	2017-12-24 16:30:31,009 INFO  [qtp1910538382-62] [puppetserver] Puppet Not sending tagmail report; no changes
	2017-12-24 16:30:31,073 INFO  [qtp1910538382-62] [puppetserver] Puppet 'store_report' command for m2.kar.int submitted to PuppetDB with UUID eded75fa-2ddb-46cd-956b-eab9864cdc13

Now if you visit the **puppetboard** (**http://DOCKER_HOST:8001**) you will see a good summary of your **puppet** nodes:

![puppet-board.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/docker-compose-puppetboard/puppet-board.png&raw=1)
