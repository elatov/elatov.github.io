---
published: true
layout: post
title: "Install Guacamole on Docker"
author: Karim Elatov
categories: [containers,os]
tags: [guacamole,mariadb,apache,docker-compose]
---
### Apache Guacamole
From their [home](https://guacamole.apache.org/) page:

> Apache Guacamole is a clientless remote desktop gateway.

It's pretty cool, you can configure RDP, SSH, or VNC connections in **guacamole** and then from a browser you can connect to any of the configured connections.

### Deploy Guacamole in Docker
There are nice instructions on how to configure **guacamole** in [docker](https://guacamole.apache.org/doc/gug/guacamole-docker.html). So let's go that route.

#### Configure MariaDB
The best thing to do is to generate a MySQL/MariaDB install script. This is accomplished by running the following on your **docker** host:

	<> docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --mysql > initdb.sql

Now from a machine that has access to your **MariaDB** server, create the database and user for **guacamole**:

	<> mysql -u root -p -h ub
	Enter password:
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 9454
	Server version: 10.2.10-MariaDB-10.2.10+maria~jessie mariadb.org binary distribution
	
	Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	MariaDB [(none)]> CREATE DATABASE guacamole;
	Query OK, 1 row affected (0.00 sec)
	
	MariaDB [(none)]> CREATE USER 'guac' IDENTIFIED BY 'password';
	Query OK, 0 rows affected (0.00 sec)
	
	MariaDB [(none)]> GRANT SELECT,INSERT,UPDATE,DELETE,CREATE ON guacamole.* TO 'guac'@'%';
	Query OK, 0 rows affected (0.00 sec)
	
	MariaDB [(none)]> FLUSH PRIVILEGES;
	Query OK, 0 rows affected (0.01 sec)
	
	MariaDB [(none)]> quit
	Bye

{% include note.html content="Change the password above." %}

Now that the database and user are ready, let's populate the db:

	<> mysql guacamole -u guac -pguacamole -h ub < initdb.sql

#### Create a docker-compose configs
I just ended up creating the following config:

	<> cat docker-compose.yml
	version: "2"
	services:
	  guacd:
	    image: "guacamole/guacd"
	    container_name: guacd
	    hostname: guacd
	    restart: always
	    volumes:
	      - "/data/shared/guacamole/guacd/data:/data"
	      - "/data/shared/guacamole/guacd/conf:/conf:ro"
	    expose:
	      - "4822"
	    ports:
	      - "4822:4822"
	    network_mode: bridge
	
	  guacamole:
	    image: "guacamole/guacamole"
	    container_name: guacamole
	    hostname: guacamole
	    restart: always
	    volumes:
	      - "/data/shared/guacamole/guacamole/guac-home:/data"
	      - "/data/shared/guacamole/guacamole/conf:/conf:ro"
	    expose:
	      - "8080"
	    ports:
	      - "8084:8080"
	    network_mode: bridge
	    environment:
	      - "GUACD_HOSTNAME=ub.kar.int"
	      - "GUACD_PORT=4822"
	      - "MYSQL_HOSTNAME=192.168.1.106"
	      - "MYSQL_PORT=3306"
	      - "MYSQL_DATABASE=guacamole"
	      - "MYSQL_USER=guac"
	      - "MYSQL_PASSWORD=password"
	      - "GUACAMOLE_HOME=/data"

{% include note.html content="Update the MySQL password and MYSQL Server IP above." %}

At this point if we run `docker-compose up -d` the services should come up and if we go to **http://{DOCKER_HOST}:8084/guacamole/** you will see the login page:

![guac-login-page.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/guacamole-docker/guac-login-page.png&raw=1)

And you can login with the default credentials:

> guacadmin/guacadmin

Change that as soon as you login. After that you can create all the connections you want: RDP, SSH, and VNC.

### Putting Guagamole behind a Reverse Proxy
I have done this in tha past with [splunk](/2013/12/installing-splunk-freebsd/) and [kibana](/2016/05/reverse-proxy-kibana-with-apache/). So I already had an **apache** server running on Debian and luckily it was version 2.4:

	<> apache2ctl -v
	Server version: Apache/2.4.25 (Debian)
	Server built:   2017-09-19T18:58:57

which supports *ws_proxy*. All of the proxy configurations are covered in [Chapter 4. Proxying Guacamole](https://guacamole.apache.org/doc/gug/proxying-guacamole.html). Without **ws-proxy**, I kept getting disconnects on the RDP connections and I saw the following in the logs:

	<> docker-compose logs -f
	guacd        | guacd[1]: INFO:	Connection "$5ae57e16-799e-4ad3-803d-69d0d1185e20" removed.
	guacd        | guacd[1]: INFO:	Creating new client for protocol "rdp"
	guacd        | guacd[1]: INFO:	Connection ID is "$ba54551e-d8ca-4891-a7ee-65d2883609f5"
	guacd        | guacd[90]: INFO:	Security mode: ANY
	guacd        | guacd[90]: INFO:	Resize method: none
	guacd        | guacd[90]: INFO:	User "@a681f5ff-0055-427c-8245-9ba428242edf" joined connection "$ba54551e-d8ca-4891-a7ee-65d2883609f5" (1 users now present)
	guacd        | guacd[90]: INFO:	Loading keymap "base"
	guacd        | guacd[90]: INFO:	Loading keymap "en-us-qwerty"
	guacamole    | 03:16:01.955 [http-nio-8080-exec-3] INFO  o.a.g.tunnel.TunnelRequestService - User "elatov" connected to connection "1".
	guacd        | guacd[90]: INFO:	guacdr connected.
	guacd        | guacd[90]: INFO:	guacsnd connected.
	guacd        | guacd[90]: INFO:	User "@a681f5ff-0055-427c-8245-9ba428242edf" disconnected (0 users remain)
	guacd        | guacd[90]: INFO:	Last user of connection "$ba54551e-d8ca-4891-a7ee-65d2883609f5" disconnected
	guacamole    | 03:16:34.946 [http-nio-8080-exec-8] INFO  o.a.g.tunnel.TunnelRequestService - User "elatov" disconnected from connection "1". Duration: 32990 milliseconds
	guacamole    | Exception in thread "Thread-25" java.lang.IllegalStateException: Message will not be sent because the WebSocket session has been closed
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointImplBase.writeMessagePart(WsRemoteEndpointImplBase.java:381)
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointImplBase.startMessage(WsRemoteEndpointImplBase.java:338)
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointImplBase$TextMessageSendHandler.write(WsRemoteEndpointImplBase.java:730)
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointImplBase.sendPartialString(WsRemoteEndpointImplBase.java:250)
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointImplBase.sendString(WsRemoteEndpointImplBase.java:193)
	guacamole    | 	at org.apache.tomcat.websocket.WsRemoteEndpointBasic.sendText(WsRemoteEndpointBasic.java:37)
	guacamole    | 	at org.apache.guacamole.websocket.GuacamoleWebSocketTunnelEndpoint$2.run(GuacamoleWebSocketTunnelEndpoint.java:167)
	guacd        | guacd[90]: INFO:	Internal RDP client disconnected
	guacd        | connected to gen.kar.int:9000
	guacd        | connected to gen.kar.int:9000
	guacd        | connected to gen.kar.int:9000
	guacd        | guacd[1]: INFO:	Connection "$ba54551e-d8ca-4891-a7ee-65d2883609f5" removed.

So on the Debian machine first enable the **ws_proxy** module:

	<> sudo a2enmod proxy_wstunnel
	Considering dependency proxy for proxy_wstunnel:
	Module proxy already enabled
	Enabling module proxy_wstunnel.
	To activate the new configuration, you need to run:
	  systemctl restart apache2

Then create the following config:

	<> cat /etc/apache2/conf-enabled/guac-proxy.conf
	<Location /guacamole/>
	    Order allow,deny
	    Allow from all
	    ProxyPass http://192.168.1.106:8084/guacamole/ flushpackets=on
	    ProxyPassReverse http://192.168.1.106:8084/guacamole/
	</Location>
	
	<Location /guacamole/websocket-tunnel>
	    Order allow,deny
	    Allow from all
	    ProxyPass ws://192.168.1.106:8084/guacamole/websocket-tunnel
	    ProxyPassReverse ws://192.168.1.106:8084/guacamole/websocket-tunnel
	</Location>

{% include note.html content="Update the IP to point to your Docker host." %}

Then connecting over the proxy worked with out issues:

![guac-with-rdp-session.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/guacamole-docker/guac-with-rdp-session.png&raw=1)
