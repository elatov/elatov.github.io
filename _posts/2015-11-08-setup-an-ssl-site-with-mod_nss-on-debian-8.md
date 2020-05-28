---
published: true
layout: post
title: "Setup an SSL Site with Mod_NSS on Debian 8 with TLS"
author: Karim Elatov
categories: [security,os]
tags: [mod_nss,linux,debian,apache,tls]
---
So I got my self a certificate from [Let's Encrypt](https://letsencrypt.org/) and I wanted to setup a webserver using **mod_nss**.

### Mod_NSS Install

I was using a Debian machine so first let's install the necessary package:

	root@kerch:~# apt-get install libapache2-mod-nss
	Reading package lists... Done
	Building dependency tree
	Reading state information... Done
	The following extra packages will be installed:
	  libnss3-tools
	The following NEW packages will be installed:
	  libapache2-mod-nss libnss3-tools
	0 upgraded, 2 newly installed, 0 to remove and 1 not upgraded.
	Setting up libnss3-tools (2:3.17.2-1.1+deb8u2) ...
	Setting up libapache2-mod-nss (1.0.10-3) ...
	libapache2-mod-nss certificate database generated.

By default the **nssdb** is pretty small:

	root@kerch:~# certutil -L -d /etc/apache2/nssdb/

	Certificate Nickname                                         Trust Attributes
	                                                             SSL,S/MIME,JAR/XPI

	cacert                                                       CTu,Cu,Cu
	beta                                                         u,pu,u
	alpha                                                        u,pu,u
	Server-Cert                                                  u,u,u

Now let's go ahead and enable the module for apache:

	root@kerch:~# a2enmod nss
	Enabling module nss.
	To activate the new configuration, you need to run:
	  service apache2 restart
	root@kerch:~# a2enmod -q nss
	root@kerch:~# echo $?
	0

### Mod_NSS Configuration
Now let's copy the module config:

	root@kerch:~# cp /etc/apache2/mods-enabled/nss.conf /etc/apache2/sites-enabled/35-www.conf

I ended up modifying the file to be a simple ssl-vhost:

	root@kerch:~# cat /etc/apache2/sites-enabled/35-www.conf
	<IfModule mod_nss.c>
	<VirtualHost 10.0.0.2:443>
		ServerName www.moxz.tk:443
		## Vhost docroot
		DocumentRoot "/var/www"
		NSSEngine on
		NSSNickname www-cert
		NSSCertificateDatabase /etc/apache2/nssdb
		CustomLog "/var/log/apache2/www-moxz-tk-443-access.log" combined
	    ErrorLog "/var/log/apache2/www-moxz-tk-443-error.log"
	    LogLevel warn
	</VirtualHost>
	</IfModule>

I also modified the default config to listen on port **443** and to define the **NSSCipherSuite** list at the global level not just at the *vhost* level. Here is the relevant section from the module config (**/etc/apache2/mods-enabled/nss.conf**):

	Listen 443

	<VirtualHost _default_:443>

	NSSCipherSuite -rsa_rc4_128_md5,-rsa_rc4_128_sha,+rsa_3des_sha,-rsa_des_sha,-rsa_rc4_40_md5,-rsa_rc2_40_md5,-rsa_null_md5,-rsa_null_sha,+fips_3des_sha,-fips_des_sha,-fortezza,-fortezza_rc4_128_sha,-fortezza_null,-rsa_des_56_sha,-rsa_rc4_56_sha,+rsa_aes_128_sha,+rsa_aes_256_sha

	NSSProtocol TLSv1.1,TLSv1.2

### Import SSL Certificate into the NSSDB
Now to import the certificate the best thing to do is to convert into a **p12**
format and then import into to the **mod_nss db**. Here is the conversion into a
**p12** format:

	root@kerch:~# openssl pkcs12 -export -in /etc/letsencrypt/live/www.moxz.tk/cert.pem -inkey /etc/letsencrypt/live/www.moxz.tk/privkey.pem -certfile /etc/letsencrypt/live/www.moxz.tk/chain.pem -out cert.pfx -name "www-cert"
	Enter Export Password:
	Verifying - Enter Export Password:

Notice I pass in the **name** option. This is actually read during the import on
the next command:

	root@kerch:~# pk12util -d /etc/apache2/nssdb/ -i cert.pfx
	Enter password for PKCS12 file:
	pk12util: PKCS12 IMPORT SUCCESSFUL

To confirm the cert is in there you can use the **certuil** command:

	root@kerch:~# certutil -L -d /etc/apache2/nssdb/

	Certificate Nickname                                         Trust Attributes
	                                                             SSL,S/MIME,JAR/XPI

	cacert                                                       CTu,Cu,Cu
	beta                                                         u,pu,u
	www-cert                                                     u,u,u
	alpha                                                        u,pu,u
	Server-Cert                                                  u,u,u
	Let's Encrypt Authority X1 - Digital Signature Trust Co.     ,,

And you will actually notice that the intermediate cert (the bottom one, **Let's
Encrypt**) is in there as well and the trust flags are set to none (**,,,**). This
is actually by design and is expected. From [Managing Certificate Trust flags
in NSS Database](https://blogs.oracle.com/meena/entry/notes_about_trust_flags):

> Flags that apply to CA Certificates
>
> c - its for validity override - It tells even though this certificate doesn't look like a CA certificate - In version 1 certificates like old root CA certificates (that predated X509 v3) its necessary to set this.
>
> C trusted CA flag implies c - This certificate should be treated like a CA certificate but also should be treated as root certificate we trust. By default roots are not trusted. We can take any certificate and mark it with a  "C" so it will be treated as a root CA certificate. When NSS clients/server validates certificate chain we can stop right there. NSS will build chain to send out as far as it reaches a root CA i.e. when it sees "C" flag. So intermediate CA certificates should not have this trust flag "C".

If you want you can check the chain of a specific cert by running the
following:

	root@kerch:~# certutil -O -d /etc/apache2/nssdb/ -n www-cert
	"Builtin Object Token:DST Root CA X3" [CN=DST Root CA X3,O=Digital Signature Trust Co.]

	  "Let's Encrypt Authority X1 - Digital Signature Trust Co." [CN=Let's Encrypt Authority X1,O=Let's Encrypt,C=US]

	    "www-cert" [CN=www.moxz.tk]

You can also make sure the certficate is valid:

	elatov@kerch:~$sudo certutil -V -u V -d /etc/apache2/nssdb/ -n www-cert
	certutil: certificate is valid

### Finalize Mod_NSS Configuration
Lastly let's make sure the configuration is all good:

	root@kerch:~# apache2ctl -t
	Syntax OK

Then restart the apache services:

	root@kerch:/var/log/apache2# systemctl restart apache2.service
	root@kerch:/var/log/apache2# systemctl status apache2.service  -l
	● apache2.service - LSB: Apache2 web server
	   Loaded: loaded (/etc/init.d/apache2)
	   Active: active (running) since Sun 2015-11-08 15:47:25 MST; 3s ago
	  Process: 18903 ExecStop=/etc/init.d/apache2 stop (code=exited, status=0/SUCCESS)
	  Process: 12965 ExecReload=/etc/init.d/apache2 reload (code=exited, status=0/SUCCESS)
	  Process: 18910 ExecStart=/etc/init.d/apache2 start (code=exited, status=0/SUCCESS)
	   CGroup: /system.slice/apache2.service
	           ├─18925 /usr/lib/libapache2-mod-nss/nss_pcache 3211265 off /etc/apache2/nssdb
	           ├─18929 PassengerHelperAgent
	           ├─18934 PassengerLoggingAgent
	           ├─18945 PassengerWatchdog (cleaning up...
	           ├─18946 /usr/sbin/apache2 -k start
	           ├─18949 PassengerWatchdog
	           ├─18952 PassengerHelperAgent
	           ├─18957 PassengerLoggingAgent
	           ├─18968 /usr/sbin/apache2 -k start
	           ├─18969 /usr/sbin/apache2 -k start
	           ├─18970 /usr/sbin/apache2 -k start
	           ├─18971 /usr/sbin/apache2 -k start
	           ├─18972 /usr/sbin/apache2 -k start
	           ├─18973 /usr/sbin/apache2 -k start
	           ├─18974 /usr/sbin/apache2 -k start
	           └─18975 /usr/sbin/apache2 -k start

	Nov 08 15:47:25 kerch apache2[18910]: Starting web server: apache2.

Then upon visiting the site, I saw that it had a valid certificate:

![www-ssl-cert-valid](https://raw.githubusercontent.com/elatov/upload/master/debian-mod-nss/www-ssl-cert-valid.png)


### Confirming TLS Connection
The TLS protocol has a lot of steps involved in the initial handshake. From [SSL Profiles Part 7: Server Name Indication](https://devcentral.f5.com/articles/ssl-profiles-part-7-server-name-indication) here is a pretty nice diagram:

![tls-handshake](https://raw.githubusercontent.com/elatov/upload/master/debian-mod-nss/tls-handshake.png)

What's really interesting is the Server Name Indication (SNI). This is the way TLS handles **name-based** virtual hosts (multiple hostnames on the same IP), more information is [here](https://en.wikipedia.org/wiki/Server_Name_Indication) and from the same page here is a pretty nice diagram:

![tls-sni](https://raw.githubusercontent.com/elatov/upload/master/debian-mod-nss/tls-sni.png)

We can confirm TLS is working appropriately by using a couple of tools, for example we can use **openssl**:

	gen ~ $ openssl s_client -servername www.moxz.tk -tlsextdebug -msg -connect www.moxz.tk:443 | grep "TLS 1.2"
	>>> TLS 1.2  [length 0005]
	>>> TLS 1.2 Handshake [length 014d], ClientHello
	<<< TLS 1.2 Handshake [length 0051], ServerHello
	<<< TLS 1.2 Handshake [length 0d0b], Certificate
	depth=2 O = Digital Signature Trust Co., CN = DST Root CA X3
	verify return:1
	depth=1 C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X1
	verify return:1
	depth=0 CN = www.moxz.tk
	verify return:1
	<<< TLS 1.2 Handshake [length 0004], ServerHelloDone
	>>> TLS 1.2 Handshake [length 0106], ClientKeyExchange
	>>> TLS 1.2 ChangeCipherSpec [length 0001]
	>>> TLS 1.2 Handshake [length 0010], Finished
	<<< TLS 1.2 ChangeCipherSpec [length 0001]
	<<< TLS 1.2 Handshake [length 0010], Finished

**curl** is also capable of helping out:

	gen ~ $ curl -v3 -1 https://www.moxz.tk
	* Rebuilt URL to: https://www.moxz.tk/
	*   Trying 76.25.201.240...
	* Connected to www.moxz.tk (76.25.201.240) port 443 (#0)
	* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
	* successfully set certificate verify locations:
	*   CAfile: /etc/ssl/certs/ca-certificates.crt
	  CApath: /etc/ssl/certs
	* TLSv1.2 (OUT), TLS Unknown, Certificate Status (22):
	* TLSv1.2 (OUT), TLS handshake, Client hello (1):
	* TLSv1.2 (IN), TLS handshake, Server hello (2):
	* TLSv1.2 (IN), TLS handshake, Certificate (11):
	* TLSv1.2 (IN), TLS handshake, Server finished (14):
	* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
	* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
	* TLSv1.2 (OUT), TLS handshake, Finished (20):
	* TLSv1.2 (IN), TLS change cipher, Client hello (1):
	* TLSv1.2 (IN), TLS handshake, Finished (20):
	* SSL connection using TLSv1.2 / AES128-SHA
	* Server certificate:
	* 	 subject: CN=www.moxz.tk
	* 	 start date: 2015-11-08 20:55:00 GMT
	* 	 expire date: 2016-02-06 20:55:00 GMT
	* 	 subjectAltName: www.moxz.tk matched
	* 	 issuer: C=US; O=Let's Encrypt; CN=Let's Encrypt Authority X1
	* 	 SSL certificate verify ok.
	> GET / HTTP/1.1
	> Host: www.moxz.tk
	> User-Agent: curl/7.43.0
	> Accept: */*
	>
	< HTTP/1.1 200 OK
	< Date: Mon, 09 Nov 2015 04:16:19 GMT
	< Server: Apache/2.4.10 (Debian)
	< Last-Modified: Sun, 08 Dec 2013 16:52:45 GMT
	< ETag: "b1-4ed08b568c768"
	< Accept-Ranges: bytes
	< Content-Length: 177
	< Vary: Accept-Encoding
	< Connection: close
	< Content-Type: text/html
	<
	<html><body><h1>It works!</h1>
	<p>This is the default web page for this server.</p>
	<p>The web server software is running but no content has been added, yet.</p>
	</body></html>
	* Closing connection 0
	* TLSv1.2 (OUT), TLS alert, Client hello (1):

BTW if you want to send an SNI along with your **openssl** command we have to use the **-servername** flag:

	gen ~ $ openssl s_client -connect www.moxz.tk:443 -servername www.moxz.tk -msg -debug
	CONNECTED(00000003)
	write to 0x2629510 [0x2629590] (338 bytes => 338 (0x152))
	0000 - 16 03 01 01 4d 01 00 01-49 03 03 d6 ed 4f 38 70   ....M...I....O8p
	0010 - 49 2e 2f e9 eb 38 d9 4e-b7 cf 12 1d 17 2c 8a 89   I./..8.N.....,..
	0020 - df e0 6d 99 e1 2f 51 fd-5f 99 ac 00 00 b6 c0 30   ..m../Q._......0
	0030 - c0 2c c0 28 c0 24 c0 14-c0 0a 00 a5 00 a3 00 a1   .,.(.$..........
	0040 - 00 9f 00 6b 00 6a 00 69-00 68 00 39 00 38 00 37   ...k.j.i.h.9.8.7
	0050 - 00 36 00 88 00 87 00 86-00 85 c0 32 c0 2e c0 2a   .6.........2...*
	0060 - c0 26 c0 0f c0 05 00 9d-00 3d 00 35 00 84 c0 2f   .&.......=.5.../
	0070 - c0 2b c0 27 c0 23 c0 13-c0 09 00 a4 00 a2 00 a0   .+.'.#..........
	0080 - 00 9e 00 67 00 40 00 3f-00 3e 00 33 00 32 00 31   ...g.@.?.>.3.2.1
	0090 - 00 30 00 9a 00 99 00 98-00 97 00 45 00 44 00 43   .0.........E.D.C
	00a0 - 00 42 c0 31 c0 2d c0 29-c0 25 c0 0e c0 04 00 9c   .B.1.-.).%......
	00b0 - 00 3c 00 2f 00 96 00 41-00 07 c0 11 c0 07 c0 0c   .<./...A........
	00c0 - c0 02 00 05 00 04 c0 12-c0 08 00 16 00 13 00 10   ................
	00d0 - 00 0d c0 0d c0 03 00 0a-00 15 00 12 00 0f 00 0c   ................
	00e0 - 00 09 00 ff 02 01 00 00-69 00 00 00 10 00 0e 00   ........i.......
	00f0 - 00 0b 77 77 77 2e 6d 6f-78 7a 2e 74 6b 00 0b 00   ..www.moxz.tk...
	0100 - 04 03 00 01 02 00 0a 00-1c 00 1a 00 17 00 19 00   ................
	0110 - 1c 00 1b 00 18 00 1a 00-16 00 0e 00 0d 00 0b 00   ................
	0120 - 0c 00 09 00 0a 00 23 00-00 00 0d 00 20 00 1e 06   ......#..... ...
	0130 - 01 06 02 06 03 05 01 05-02 05 03 04 01 04 02 04   ................
	0140 - 03 03 01 03 02 03 03 02-01 02 02 02 03 00 0f 00   ................
	0150 - 01 01                                             ..
	>>> TLS 1.2  [length 0005]
	    16 03 01 01 4d
	>>> TLS 1.2 Handshake [length 014d], ClientHello
	    01 00 01 49 03 03 d6 ed 4f 38 70 49 2e 2f e9 eb
	    38 d9 4e b7 cf 12 1d 17 2c 8a 89 df e0 6d 99 e1
	    2f 51 fd 5f 99 ac 00 00 b6 c0 30 c0 2c c0 28 c0
	    24 c0 14 c0 0a 00 a5 00 a3 00 a1 00 9f 00 6b 00
	    6a 00 69 00 68 00 39 00 38 00 37 00 36 00 88 00
	    87 00 86 00 85 c0 32 c0 2e c0 2a c0 26 c0 0f c0
	    05 00 9d 00 3d 00 35 00 84 c0 2f c0 2b c0 27 c0
	    23 c0 13 c0 09 00 a4 00 a2 00 a0 00 9e 00 67 00
	    40 00 3f 00 3e 00 33 00 32 00 31 00 30 00 9a 00
	    99 00 98 00 97 00 45 00 44 00 43 00 42 c0 31 c0
	    2d c0 29 c0 25 c0 0e c0 04 00 9c 00 3c 00 2f 00
	    96 00 41 00 07 c0 11 c0 07 c0 0c c0 02 00 05 00
	    04 c0 12 c0 08 00 16 00 13 00 10 00 0d c0 0d c0
	    03 00 0a 00 15 00 12 00 0f 00 0c 00 09 00 ff 02
	    01 00 00 69 00 00 00 10 00 0e 00 00 0b 77 77 77
	    2e 6d 6f 78 7a 2e 74 6b 00 0b 00 04 03 00 01 02
	    00 0a 00 1c 00 1a 00 17 00 19 00 1c 00 1b 00 18
	    00 1a 00 16 00 0e 00 0d 00 0b 00 0c 00 09 00 0a
	    00 23 00 00 00 0d 00 20 00 1e 06 01 06 02 06 03
	    05 01 05 02 05 03 04 01 04 02 04 03 03 01 03 02
	    03 03 02 01 02 02 02 03 00 0f 00 01 01
	read from 0x2629510 [0x262eaf0] (7 bytes => 7 (0x7))
