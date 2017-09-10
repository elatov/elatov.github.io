---
published: true
layout: post
title: "Using Splunk with Docker"
author: Karim Elatov
categories: [containers]
tags: [docker,docker-compose,splunk]
---
### Splunk and Docker
The instructions on the setup are covered in: [How to use the Splunk Enterprise Docker image](https://github.com/splunk/docker-splunk/blob/master/enterprise/README.md). I decided to take the **docker-compose** approach.

### Install docker-compose on CoreOS
First we need to install **docker-compose** on CoreOS. There are a couple of sites that talk about the process:

- [Installing Docker Compose in CoreOS](https://www.ericluwj.com/2015/10/20/installing-docker-compose-in-coreos.html)
- [Install docker-compose onto CoreOS](https://gist.github.com/andromedarabbit/75a0d065bff2db32da1921ff1cb624bb)

So following the instructions I just ran this:

    $ curl -L https://github.com/docker/compose/releases/download/1.11.2/docker-compose-`uname -s`-`uname -m` > /opt/bin/docker-compose
    $ chmod +x /opt/bin/docker-compose

### Setup Splunk docker image
Next let's get the splunk image: 

    $ docker pull splunk/splunk:latest

Since I had a non-docker splunk instance running already, I wanted to actually migrate all the data. So I **tar**'ed the **etc** and **var** directories of the splunk install and **scp**'ed them to the CoreOS machine. After that I just placed the archives into place:

    $ mv splunk-etc.tar.bz2 /root/splunk/.
    $ mv splunk-var.tar.bz2 /root/splunk/.

And then I extracted them:

    $ cd /root/splunk
    $ tar xjf splunk-var.tar.bz2
    $ tar xjf splunk-etc.tar.bz2

### Using docker-compose with the Splunk Docker Image
The above site has a pretty good example, I ended up with this one:

    # cat docker-compose.yml 
    version: '2'
    services:
        splunk:
           image: splunk/splunk:latest
           hostname: splunk
           environment:
            SPLUNK_START_ARGS: --accept-license --answer-yes
            SPLUNK_ENABLE_LISTEN: 9997
            SPLUNK_ADD: udp 514
            SPLUNK_USER: root
           volumes:
            - /root/splunk/etc:/opt/splunk/etc
            - /root/splunk/var:/opt/splunk/var
           ports:
            - "8000:8000"
            - "9997:9997"
            - "8088:8088"
            - "514:514/udp"
           restart: always

To confirm the configuration is okay, we can run the following:

    # docker-compose config
    networks: {}
    services:
      splunk:
        environment:
          SPLUNK_ADD: udp 514
          SPLUNK_ENABLE_LISTEN: 9997
          SPLUNK_START_ARGS: --accept-license --answer-yes
          SPLUNK_USER: root
        hostname: splunk
        image: splunk/splunk:latest
        ports:
        - 8000:8000
        - 9997:9997
        - 8088:8088
        - 514:514/udp
        restart: always
        volumes:
        - /root/splunk/etc:/opt/splunk/etc:rw
        - /root/splunk/var:/opt/splunk/var:rw
    version: '2.0'
    volumes: {}

Now let's start it up:

    splunk # docker-compose up
    Creating network "splunk_default" with the default driver
    Creating splunk_splunk_1
    Attaching to splunk_splunk_1
    splunk_1  | 
    splunk_1  | -- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2017-02-26.18-29-31' --
    splunk_1  | Copying '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.
    splunk_1  | 
    splunk_1  | Checking saved search compatibility...
    splunk_1  | 
    splunk_1  | Handling deprecated files...
    splunk_1  | 
    splunk_1  | Checking script configuration...
    splunk_1  | 
    splunk_1  | Copying '/opt/splunk/etc/system/local/indexes.conf' to '/opt/splunk/etc/system/local/indexes.conf.old'.
    splunk_1  | Copying '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
    splunk_1  | Deleting '/opt/splunk/etc/system/local/field_actions.conf'.
    splunk_1  | Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
    splunk_1  | Checking for possible UI view conflicts...
    splunk_1  |  App "splunk_monitoring_console" has an overriding copy of the "dashboards.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_monitoring_console/default/data/ui/views
    splunk_1  |  App "splunk_monitoring_console" has an overriding copy of the "alerts.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_monitoring_console/default/data/ui/views
    splunk_1  |  App "splunk_monitoring_console" has an overriding copy of the "reports.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_monitoring_console/default/data/ui/views
    splunk_1  |  App "splunk_instrumentation" has an overriding copy of the "search.xml" view, thus the new version may not be in effect. location=/opt/splunk/etc/apps/splunk_instrumentation/default/data/ui/views
    splunk_1  | Removing legacy manager XML files...
    splunk_1  | DMC is not set up, no need to migrate nav bar.
    splunk_1  | Removing System Activity dashboards...
    splunk_1  | Removing splunkclouduf XML file...
    splunk_1  | Removing splunkclouduf view XML files...
    splunk_1  | Distributed Search is not configured on this instance
    splunk_1  | 
    splunk_1  | This appears to be an upgrade of Splunk.
    splunk_1  | --------------------------------------------------------------------------------)
    splunk_1  | 
    splunk_1  | Splunk has detected an older version of Splunk installed on this machine. To
    splunk_1  | finish upgrading to the new version, Splunk's installer will automatically
    splunk_1  | update and alter your current configuration files. Deprecated configuration
    splunk_1  | files will be renamed with a .deprecated extension.
    splunk_1  | 
    splunk_1  | You can choose to preview the changes that will be made to your configuration
    splunk_1  | files before proceeding with the migration and upgrade:
    splunk_1  | 
    splunk_1  | If you want to migrate and upgrade without previewing the changes that will be
    splunk_1  | made to your existing configuration files, choose 'y'.
    splunk_1  | If you want to see what changes will be made before you proceed with the
    splunk_1  | upgrade, choose 'n'.
    splunk_1  | 
    splunk_1  | 
    splunk_1  | Perform migration and upgrade without previewing configuration changes? [y/n] y
    splunk_1  | 
    splunk_1  | Migrating to:
    splunk_1  | VERSION=6.5.2
    splunk_1  | BUILD=67571ef4b87d
    splunk_1  | PRODUCT=splunk
    splunk_1  | PLATFORM=Linux-x86_64
    splunk_1  | 
    splunk_1  | 
    splunk_1  | splunkd 1287 was not running.
    splunk_1  | Stopping splunk helpers...
    splunk_1  | 
    splunk_1  | Done.
    splunk_1  | Stopped helpers.
    splunk_1  | Removing stale pid file... done.
    splunk_1  | "/opt/splunk/etc/auth/ca.pem": already a renewed Splunk certificate: skipping renewal
    splunk_1  | "/opt/splunk/etc/auth/cacert.pem": already a renewed Splunk certificate: skipping renewal
    splunk_1  | Clustering migration already complete, no further changes required.
    splunk_1  | 
    splunk_1  | Generating checksums for datamodel and report acceleration bucket summaries for all indexes.
    splunk_1  | If you have defined many indexes and summaries, summary checksum generation may take a long time.
    splunk_1  | Processed 1 out of 8 configured indexes.
    splunk_1  | Processed 2 out of 8 configured indexes.
    splunk_1  | Processed 3 out of 8 configured indexes.
    splunk_1  | Processed 4 out of 8 configured indexes.
    splunk_1  | Processed 5 out of 8 configured indexes.
    splunk_1  | Processed 6 out of 8 configured indexes.
    splunk_1  | Processed 7 out of 8 configured indexes.
    splunk_1  | Processed 8 out of 8 configured indexes.
    splunk_1  | Finished generating checksums for datamodel and report acceleration bucket summaries for all indexes.
    splunk_1  | 
    splunk_1  | Splunk> 4TW
    splunk_1  | 
    splunk_1  | Checking prerequisites...
    splunk_1  | 	Checking http port [8000]: open
    splunk_1  | 	Checking mgmt port [8089]: open
    splunk_1  | 	Checking appserver port [127.0.0.1:8065]: open
    splunk_1  | 	Checking kvstore port [8191]: open
    splunk_1  | 	Checking configuration...  Done.
    splunk_1  | 	Checking critical directories...	Done
    splunk_1  | 	Checking indexes...
    splunk_1  | 		Validated: _audit _internal _introspection _telemetry _thefishbucket history main summary
    splunk_1  | 	Done
    splunk_1  | 	Checking filesystem compatibility...  Done
    splunk_1  | 	Checking conf files for problems...
    splunk_1  | 	Done
    splunk_1  | 	Checking default conf files for edits...
    splunk_1  | 	Validating installed files against hashes from '/opt/splunk/splunk-6.5.2-67571ef4b87d-linux-2.6-x86_64-manifest'
    splunk_1  | File '/opt/splunk/etc/apps/splunk_httpinput/default/inputs.conf' changed.
    splunk_1  | 	Problems were found, please review your files and move customizations to local
    splunk_1  | All preliminary checks passed.
    splunk_1  | 
    splunk_1  | Starting splunk server daemon (splunkd)...  
    splunk_1  | Done
    splunk_1  | 
    splunk_1  | 
    splunk_1  | Waiting for web server at http://127.0.0.1:8000 to be available... Done
    splunk_1  | 
    splunk_1  | 
    splunk_1  | If you get stuck, we're here to help.  
    splunk_1  | Look for answers here: http://docs.splunk.com
    splunk_1  | 
    splunk_1  | The Splunk web interface is at http://splunk:8000
    splunk_1  | 

You can run this to detach from the **docker-compose**

    splunk # docker-compose up -d or docker-compose start
    Starting splunk_splunk_1

If you ever need to stop it you can run the following:

	$ docker-compose stop

And you can check out the logs of the image like so:

    splunk # docker-compose logs
    splunk_1  | Shutting down.  Please wait, as this may take a few minutes.
    splunk_1  | 2017-02-26 18:46:51.655 +0000 Interrupt signal received
    splunk_1  | ..
    splunk_1  | Stopping splunk helpers...
    splunk_1  | 
    splunk_1  | Done.
    splunk_1  | splunkd is not running.
    splunk_1  | 
    splunk_1  | Splunk> 4TW
    splunk_1  | 
    splunk_1  | Checking prerequisites...
    splunk_1  | 	Checking http port [8000]: open
    splunk_1  | 	Checking mgmt port [8089]: open
    splunk_1  | 	Checking appserver port [127.0.0.1:8065]: open
    splunk_1  | 	Checking kvstore port [8191]: open
    splunk_1  | 	Checking configuration...  Done.
    splunk_1  | 	Checking critical directories...	Done
    splunk_1  | 	Checking indexes...
    splunk_1  | 		Validated: _audit _internal _introspection _telemetry _thefishbucket history main summary
    splunk_1  | 	Done
    splunk_1  | 	Checking filesystem compatibility...  Done
    splunk_1  | 	Checking conf files for problems...
    splunk_1  | 	Done
    splunk_1  | 	Checking default conf files for edits...
    splunk_1  | 	Validating installed files against hashes from '/opt/splunk/splunk-6.5.2-67571ef4b87d-linux-2.6-x86_64-manifest'
    splunk_1  | File '/opt/splunk/etc/apps/splunk_httpinput/default/inputs.conf' changed.
    splunk_1  | 	Problems were found, please review your files and move customizations to local
    splunk_1  | All preliminary checks passed.
    splunk_1  | 
    splunk_1  | Starting splunk server daemon (splunkd)...  
    splunk_1  | Done
    splunk_1  | 
    splunk_1  | 
    splunk_1  | Waiting for web server at http://127.0.0.1:8000 to be available.. Done
    splunk_1  | 
    splunk_1  | 
    splunk_1  | If you get stuck, we're here to help.  
    splunk_1  | Look for answers here: http://docs.splunk.com
    splunk_1  | 
    splunk_1  | The Splunk web interface is at http://splunk:8000
    splunk_1  | 

### Updating Splunk Docker Image
To update you can stop the service and do the update:

    # cd /root/splunk
    # docker-compose stop
    # docker pull splunk/splunk:latest or docker-compose pull
    # docker-compose up -d

As I was doing research on how to update with **docker-compose**, I ran into these interesting sites:

- [How to Update a Single Running docker-compose Container](http://staxmanade.com/2016/09/how-to-update-a-single-running-docker-compose-container/)
- [docker-compose up doesn't pull down latest image if the image exists locally](https://github.com/docker/compose/issues/3574)

When you do a pull it will tell you if the image is up to date:

    # docker-compose pull
    Pulling splunk (splunk/splunk:latest)...
    latest: Pulling from splunk/splunk
    Digest: sha256:b3427c513e3df1a3903abc136732ec528c746ff69ffa1ef9579c6ebedadf366f
    Status: Image is up to date for splunk/splunk:latest

