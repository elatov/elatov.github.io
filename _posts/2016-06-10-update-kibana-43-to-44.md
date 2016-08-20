---
published: true
layout: post
title: "Update Kibana 4.3 to 4.4"
author: Karim Elatov
categories: [os,security]
tags: [kibana,linux,centos]
---
I noticed that a [new update](https://www.elastic.co/guide/en/kibana/current/releasenotes.html) for **kibana** came out, so I decided to update my version.

### Preparing for the Kibana Update
If you remember [my previous](/2016/02/playing-around-with-an-elasticsearchlogstashkibana-elk-stack/) post I ended up getting the **tar.gz** archive and installing it manually under **/opt**. This time around I decided to add a *YUM* repository and install from there. First I exported all of my objects just in case. This is done in **kibana** under **Settings** -> **Objects** -> **Export Everything**:

![kib-obj-export](https://dl.dropboxusercontent.com/u/24136116/blog_pics/kibana-update/kib-obj-export.png)

Now let's stop the **kibana** server:

	sudo systemctl stop kibana

Next let's move our install out of the way:

	sudo mv /opt/kibana /opt/kibana-4.3

The instuctions on how to setup the *YUM* repo are laid out in [Getting Kibana Up and Running](https://www.elastic.co/guide/en/kibana/current/setup.html). First let's import the GPG Key:

	sudo rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch

Next let's create the *YUM* repo:

	┌─[elatov@puppet] - [/home/elatov] - [2016-02-21 09:19:02]
	└─[0] <> cat /etc/yum.repos.d/kibana.repo
	[kibana-4.4]
	name=Kibana repository for 4.4.x packages
	baseurl=http://packages.elastic.co/kibana/4.4/centos
	gpgcheck=1
	gpgkey=http://packages.elastic.co/GPG-KEY-elasticsearch
	enabled=1
	
Now we are ready for the update.

### Install Kibana 4.4
Now that we have the *YUM* repository added let's install **kibana**:

	sudo yum install kibana

That will install most of the contents under **/opt** and also include a new systemd script. I actually checked out the script and I preffered the original so let's overwrite the default one:

	sudo mv /etc/systemd/system/kibana.service /lib/systemd/system/kibana.service

Now let's update **systemd**:

	sudo systemctl daemon-reload
	sudo systemctl disable kibana.service
	sudo systemctl enable kibana.service
	
Now let's copy over the original config:

	sudo cp /opt/kibana/config/kibana.yml /opt/kibana/config/kibana.yml.orig
	sudo cp /opt/kibana-4.3/config/kibana.yml /opt/kibana/config/kibana.yml

Then I just started the service:

	sudo systemctl start kibana

And checking out the logs looked good:

	Feb 21 08:53:35 puppet systemd[1]: Started Kibana 4 Web Interface.
	Feb 21 08:53:35 puppet systemd[1]: Starting Kibana 4 Web Interface...
	Feb 21 08:53:38 puppet kibana4[25523]:{"type":"log","@timestamp":"2016-02-21T15:53:38+00:00","tags":["status","plugin:kibana","info"],"pid":25523,"name":"plugin:kibana","state":"gree
	Feb 21 08:53:38 puppet kibana4[25523]: {"type":"log","@timestamp":"2016-02-21T15:53:38+00:00","tags":["status","plugin:elasticsearch","info"],"pid":25523,"name":"plugin:elasticsearch"
	
After I logged into **kibana** I saw the new version:

![kib-version](https://dl.dropboxusercontent.com/u/24136116/blog_pics/kibana-update/kib-version.png)
