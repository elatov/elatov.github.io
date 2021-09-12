---
published: true
layout: post
title: "Reverse Proxy Kibana with Apache"
author: Karim Elatov
categories: [os,security]
tags: [linux,debian,apache,kibana]
---
After some time I realized I wanted to protect my kibana dashboard using a password. I did a similar setup with my splunk setup, where I used apache's reverse proxy capability to password protect the application (the setup is covered [here](/2013/12/installing-splunk-freebsd/)). 

### Reverse Proxy with a Dedicated VirtualHost
This setup is covered [here](https://www.jhipster.tech/tips/023_tip_protecting_kibana_with_apache_basic_authent.html). I ended up creating the following configuration:

	┌─[elatov@kerch] - [/home/elatov] - [2016-02-07 09:29:16]
	└─[0] <> cat /etc/apache2/sites-enabled/40-www.conf
	<IfModule mod_nss.c>
	<VirtualHost 10.0.0.2:8443>
		ServerName www.moxz.tk
		## Vhost docroot
		DocumentRoot "/var/www"
		
		### TLS
		NSSEngine on
		NSSNickname www-cert
		NSSCertificateDatabase /etc/apache2/nssdb
		
		# Logging
		CustomLog "/var/log/apache2/web-moxz-tk-8443-access.log" combined
	    ErrorLog "/var/log/apache2/web-moxz-tk-8443-error.log"
	    LogLevel warn
		
		# proxy
		ProxyRequests Off
	
		ProxyPass / http://10.0.0.6:5601/
	    ProxyPassReverse / https://10.0.0.6:5601/
		<Proxy *>
			## Auth
			AuthType Basic
			AuthName "Kibana"
			AuthUserFile /etc/apache2/pass/htpasswd
			Require valid-user
		</Proxy>
	</VirtualHost>
	</IfModule>

This is actually doing SSL Offloading as well so it's pretty sweet. I covered my **mod_nss** setup [here](/2015/11/setup-an-ssl-site-with-mod_nss-on-debian-8/).

### Reverse Proxy with a Dedicated ServerPath/Directory
If you already have a website running and you don't want to waste virtualhosts you can setup kibana to be on a specific server path and you can just reverse proxy that path/directory. This is covered [here](https://discuss.elastic.co/t/4-3-0-how-to-configure-your-nginx-balancer-and-apache-reverse-proxy/37351/2). First enable kibana to have a specific **BasePath** (don't forget to restart **kibana**):

	┌─[elatov@puppet] - [/home/elatov] - [2016-02-07 09:36:06]
	└─[0] <> grep server.basePath /opt/kibana/config/kibana.yml
	server.basePath: "/kibana"

Then modify you apache config to look like this:

	┌─[elatov@kerch] - [/home/elatov] - [2016-02-07 09:29:27]
	└─[0] <> cat /etc/apache2/sites-enabled/35-www.conf
	<IfModule mod_nss.c>
	<VirtualHost 10.0.0.2:443>
		ServerName www.moxz.tk:443
		## Vhost docroot
		DocumentRoot "/var/www"
		# TLS
		NSSEngine on
		NSSNickname www-cert
		NSSCertificateDatabase /etc/apache2/nssdb
		
		# Logging
		CustomLog "/var/log/apache2/www-moxz-tk-443-access.log" combined
		ErrorLog "/var/log/apache2/www-moxz-tk-443-error.log"
		LogLevel warn
	    
	    	# Proxy
		<Location /kibana>
			## Auth
			AuthType Basic
			AuthName "Kibana"
			AuthUserFile /etc/apache2/pass/htpasswd
			Require valid-user
			### Reverse Proxy
			ProxyPass         http://10.0.0.6:5601 retry=0
	  		ProxyPassReverse  http://10.0.0.6:5601
		</Location>
	</VirtualHost>

The only downside of the **BasePath** directive is after that's set you actually can't go directly to the kibana app. I think this is a bug and there is a discussion on it [here](https://github.com/elastic/kibana/pull/5337). Hopefully in the next release it will be fixed.

### Reverse Proxy without Kibana BasePath
If you don't setup the **basePath** you will have to reverse proxy a bunch of locations. The gist of them are covered [here](https://github.com/elastic/kibana/issues/5230). You would need this (I tried it out and was actually okay):

	ProxyRequests Off
	
	ProxyPass /app/kibana http://127.0.0.1:5601/app/kibana
	ProxyPassReverse /app/kibana http://127.0.0.1:5601/app/kibana
	
	ProxyPass /bundles http://127.0.0.1:5601/bundles
	ProxyPassReverse /bundles http://127.0.0.1:5601/bundles
	  
	ProxyPass /status http://127.0.0.1:5601/status
	ProxyPassReverse /status http://127.0.0.1:5601/status
	
	ProxyPass /api/status http://127.0.0.1:5601/api/status
	ProxyPassReverse /api/status http://127.0.0.1:5601/api/status
	
	ProxyPass /elasticsearch http://127.0.0.1:5601/elasticsearch
	ProxyPassReverse /elasticsearch http://127.0.0.1:5601/elasticsearch

And you would also need to go directly to the full url (**https://apache.server/app/kibana**)

