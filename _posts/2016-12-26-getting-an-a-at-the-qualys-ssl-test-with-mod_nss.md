---
published: true
layout: post
title: "Getting an A+ at the Qualys SSL Test with mod_nss"
author: Karim Elatov
categories: [os,security]
tags: [apache,debian,mod_nss]
---
I was using the Let's Encrypt Certificate, I talked about that setup [here](/2015/11/setup-an-ssl-site-with-mod_nss-on-debian-8/). By default with **mod_nss** and the Let's Encrypt Cert you will get an A- at the [Qualys SSL Labs Test](https://www.ssllabs.com/ssltest). So let's make some modifications to setup to get an A+.

### Cipher Suite
Mozilla has a pretty good site that talks about different profiles for different browsers with TLS ([Security/Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)). If you check out the **Modern** profile you can see that it only recommends using TLS 1.2 and some of the old browsers won't work. Here is the recommended list from that page:

	0xC0,0x2C  -  ECDHE-ECDSA-AES256-GCM-SHA384  TLSv1.2  Kx=ECDH  Au=ECDSA  Enc=AESGCM(256)    Mac=AEAD
	0xC0,0x30  -  ECDHE-RSA-AES256-GCM-SHA384    TLSv1.2  Kx=ECDH  Au=RSA    Enc=AESGCM(256)    Mac=AEAD
	0xCC,0x14  -  ECDHE-ECDSA-CHACHA20-POLY1305  TLSv1.2  Kx=ECDH  Au=ECDSA  Enc=ChaCha20(256)  Mac=AEAD
	0xCC,0x13  -  ECDHE-RSA-CHACHA20-POLY1305    TLSv1.2  Kx=ECDH  Au=RSA    Enc=ChaCha20(256)  Mac=AEAD
	0xC0,0x2B  -  ECDHE-ECDSA-AES128-GCM-SHA256  TLSv1.2  Kx=ECDH  Au=ECDSA  Enc=AESGCM(128)    Mac=AEAD
	0xC0,0x2F  -  ECDHE-RSA-AES128-GCM-SHA256    TLSv1.2  Kx=ECDH  Au=RSA    Enc=AESGCM(128)    Mac=AEAD
	0xC0,0x24  -  ECDHE-ECDSA-AES256-SHA384      TLSv1.2  Kx=ECDH  Au=ECDSA  Enc=AES(256)       Mac=SHA384
	0xC0,0x28  -  ECDHE-RSA-AES256-SHA384        TLSv1.2  Kx=ECDH  Au=RSA    Enc=AES(256)       Mac=SHA384
	0xC0,0x23  -  ECDHE-ECDSA-AES128-SHA256      TLSv1.2  Kx=ECDH  Au=ECDSA  Enc=AES(128)       Mac=SHA256
	0xC0,0x27  -  ECDHE-RSA-AES128-SHA256        TLSv1.2  Kx=ECDH  Au=RSA    Enc=AES(128)       Mac=SHA256
	
I picked a couple of those and just used them and they bumped me to an A. I realized that if I want to support more browsers I will have to enable some less secure ciphers. A lot of the time to keep **Forward Secrecy** a combination of DHE and ECDHE ciphers will get you there. But I discovered that DHE ciphers just recently became supported with **mod_nss** and they are getting added as we speak ([server support of DHE ciphers](https://fedorahosted.org/mod_nss/ticket/15)). You will notice that DHE support will be in **mod_nss 1.0.13** and on my Debian machine I was at the following:

	<> dpkg -l libapache2-mod-nss
	Desired=Unknown/Install/Remove/Purge/Hold
	| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
	|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
	||/ Name           Version      Architecture Description
	+++-==============-============-============-=================================
	ii  libapache2-mod 1.0.10-3     amd64        NSS-based SSL module for Apache2
	
So to support older browsers I ended up enabling two ciphers (while I wait for the DHE support):

	TLS_RSA_WITH_AES_128_CBC_SHA
	TLS_RSA_WITH_AES_256_CBC_SHA

And also TLS v1.1 and v1.0. In the end here is what I had in my **mod_nss** config:

	<> grep -E '^NSSCipher|^NSSPro' /etc/apache2/mods-enabled/nss.conf
	NSSCipherSuite +ecdhe_rsa_aes_128_sha,+ecdhe_rsa_aes_256_sha,+rsa_aes_128_sha,+rsa_aes_256_sha
	NSSProtocol TLSv1.0,TLSv1.1,TLSv1.2
	
With that in place I got an A and it covered 99% of the browsers, I only missed old IE ones:

![ssl-test-old-brow](https://dl.dropboxusercontent.com/u/24136116/blog_pics/mod_nss_qualys/ssl-test-old-brow.png)

Also if you want to quickly test what ciphers your server supports you can use **nmap**:

	<> nmap --script ssl-enum-ciphers -p 443 www.moxz.tk
	
	Starting Nmap 7.12 ( https://nmap.org ) at 2016-05-22 10:28 MDT
	Nmap scan report for kerch (10.0.0.2)
	Host is up (0.0018s latency).
	rDNS record for 10.0.0.2: www.moxz.tk
	PORT    STATE SERVICE
	443/tcp open  https
	| ssl-enum-ciphers:
	|   TLSv1.2:
	|     ciphers:
	|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
	|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
	|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
	|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
	|     compressors:
	|       NULL
	|     cipher preference: server
	|_  least strength: A
	
	Nmap done: 1 IP address (1 host up) scanned in 0.36 seconds

### Adding the HSTS Header
The thing that got me to the A+ was enabling the [HSTS](https://www.owasp.org/index.php/HTTP_Strict_Transport_Security) header. The config is covered in [HTTP Strict Transport Security for Apache, NGINX and Lighttpd](https://raymii.org/s/tutorials/HTTP_Strict_Transport_Security_for_Apache_NGINX_and_Lighttpd.html). First I enabled the **header** module for apache:

	<> sudo a2enmod headers
	Enabling module headers.
	To activate the new configuration, you need to run:
	  service apache2 restart
	  
And then I added the header to be set in my *virtualhost*:

	<> grep Header /etc/apache2/sites-enabled/35-www.conf
		# Add the HSTS Header
		Header always set Strict-Transport-Security "max-age=15768000; includeSubdomains; preload"
		
Then after one more apache restart

	sudo systemctl restart apache2

I was able to get the A+:

![ssl-test-a-pl](https://dl.dropboxusercontent.com/u/24136116/blog_pics/mod_nss_qualys/ssl-test-a-pl.png)

BTW there is good discussion about other results at [[Freeipa-users] let's encrypt integration and best practices for mod_nss/mod_ssl](https://www.redhat.com/archives/freeipa-users/2015-November/msg00114.html) here is an interesting comment about the **Session Resumption**:

> The main reason this is an "orange" alert in SSLLabs is because the server is assigning Session IDs but then ignoring them; although confusing it is a fairly common default behaviour and doesn't cause any issues with compliant client implementation
