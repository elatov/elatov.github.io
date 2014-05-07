---
title: 'SRM fails to install a custom certificate with &#8220;The host name in the Subject Alternative Name of the provided certificate does not match the SRM host name.&#8221; during a modify install'
author: Jarret Lavallee
layout: post
permalink: /2012/08/srm-fails-to-install-a-custom-certificate-with-he-host-name-in-the-subject-alternative-name-of-the-provided-certificate-does-not-match-the-srm-host-name/
dsq_thread_id:
  - 1407443786
categories:
  - SRM
  - VMware
tags:
  - Certifications
  - installation
  - openssl
  - srm
---
I was running through some SRM certificate configuration tests for a customer and ran into this issue. It is actually expected behavior, but the error message is very misleading. I ran into this issue when doing a &#8220;modify&#8221; install and trying to add in my .p12 cert. The message is aggrivating because the subjectAltName was actually the same as the hostname of the SRM server.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/subjectaltname-does-not-match.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/subjectaltname-does-not-match.jpg']);"><img class="aligncenter size-full wp-image-1920" title="subjectaltname does not match" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/subjectaltname-does-not-match.jpg" alt="subjectaltname does not match SRM fails to install a custom certificate with The host name in the Subject Alternative Name of the provided certificate does not match the SRM host name. during a modify install" width="606" height="141" /></a>

Looking at the installer logs (C:\Documents and Settings\jarret\Local Settings\Temp\VMSrmInst.log) we can see error that the installer is complaining about.

	  
	2012-08-02T12:00:54.493-06:00 [04636 info 'Default'] Vmacore::InitSSL: doVersionCheck = true, handshakeTimeoutUs = 20000000  
	Enter password for certificate file C:\Documents and Settings\jarret\Desktop\srm-prod\srm-prod.p12: Error [76]: The DNS of the certificate, does not match the SRM host. The expected DNS name is: srm-prod.virtuallyhyper.com. The provided SRM host is: 192.168.10.72
	
	VMware: Srm::Installation::Utility::LaunchApplication: INFORMATION: Child process stderr:
	
	VMware: Srm::Installation::Utility::LaunchApplication: INFORMATION: Executable finished executing. Result code=76  
	VMware: Srm::Installation::DirectoryChanger::~DirectoryChanger: INFORMATION: Restored directory. Directory=C:\Documents and Settings\jarret\Desktop\srm-prod  
	VMware: Srm::Installation::Utility::GetMsgFromErrorTable: INFORMATION: Error message is The host name in the Subject Alternative Name of the provided certificate does not match the SRM host name.  
	VMware: Srm::Installation::Utility::GetMsgFromErrorTable: INFORMATION: Error message is Failed to validate certificate.%n%nDetails:%n  
	

From the logs we can see that the subjectAltName (srm-prod.virtuallyhyper.com) does not match the SRM host (192.168.10.72), so the error makes perfect sense. The problem is that the message does not indicate why the SRM host is by IP address instead of the FQDN.

When SRM is installed, we have the option to enter an address for the SRM server. The default is the IP address, but we really wanted to enter the FQDN.

I have come up with 3 different ways to get around this issue.

**UPDATE:** A colleague raised some questions about multiple Subject Alternative Name in the certificate. I did <a href="http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/']);" title="SRM 5.x Custom SSL Certificates with Multiple Subject Alternative Names" target="_blank">some experimenting</a> and found that SRM will use the **last** Subject Alternative Name in the certificate. If you have multiple Subject Alternative Names in the SRM certificate, make sure that the SRM host name is the last.

## Modify the configuration files to use the hostname instead of the IP address

We can change the configuration files in order to fix this. On the SRM server, open up the extensions.xml in C:\Program Files (x86)\VMware\VMware vCenter Site Recovery Manager\config. This configuration file holds extensions for SRM. In here we will find the IP as the address to connect to for the extension. Find every entry of the IP address and replace it with the fully qualified domain name and save the file.

Since we updated the extensions in the xml file, we also have to update the extensions in vCenter. To do this we will use the srm-config.exe. Open up a command prompt with administrative privileges and run the following commands.

	  
	C:\> cd C:\Program Files (x86)\VMware\VMware vCenter Site Recovery Manager\bin  
	C:\Program Files (x86)\VMware\VMware vCenter Site Recovery Manager\bin>srm-config.exe -cmd updateext -cfg ..\config\vmware-dr.xml -extcfg ..\config\extension.xml  
	

Now we should restart SRM to ensure that the changes are taken.

	  
	C:\> net stop vmware-dr  
	C:\> net start vmware-dr  
	

Now try to run the &#8220;modify&#8221; installation and insert your custom cert.

## Reinstall and enter the Local host name

This is the easiest option. You can uninstall SRM leaving the database. When you go through the SRM installation, ensure that you enter the FQDN for SRM rather than the IP for the local host entry.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg']);"><img class="aligncenter size-full wp-image-1918" title="SRM installer FQDN" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg" alt="enter the fqdn SRM fails to install a custom certificate with The host name in the Subject Alternative Name of the provided certificate does not match the SRM host name. during a modify install" width="504" height="379" /></a>

With this method you should be able to install the certificate and ensure that the local host name is set to the FQDN rather than the IP address.

## Add the IP address to the subjectAltName in the certificate

Another way is to regenerate the certificate. This way we can put in more subjectAltNames so that they do match. I would suggest the other methods over this one, as they actually fix the issue where as this is a workaround.

When generating the csr for the CA to sign, you had to add a <a href="http://kb.vmware.com/kb/1008390" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1008390']);" target="_blank">subjectAltName as per the requirements</a>. To do this you would put a definition of the subjectAltName in the openssl.cnf (openssl.cfg on windows).

	  
	subjectAltName = DNS: SRM1.example.com  
	

According to the <a href="http://www.openssl.org/docs/apps/x509v3_config.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openssl.org/docs/apps/x509v3_config.html']);" target="_blank">openssl documents</a>, we can add in a subjectAltName of an IP as well. So we can regernerate our CSR with the following lines in the openssl.cnf.

	  
	subjectAltName = DNS: srm-prod.virtuallyhyper.com,IP: 192.168.10.72  
	

Generate the csr again. (Make sure that you still have the clientAuth in the openssl.cnf)

	  
	\# openssl req -new -newkey rsa:2048 -sha256 -nodes -out srm-prod.csr -keyout srm-prod.key -config openssl.cnf  
	

Check the csr for the new alternative names.

	  
	\# openssl req -text -noout -in srm-prod.csr |egrep -A 1 "Subject Alternative Name|Extended Key Usage"  
	X509v3 Subject Alternative Name:  
	DNS:srm-prod.virtuallyhyper.com, IP Address:192.168.10.72  
	X509v3 Extended Key Usage:  
	TLS Web Server Authentication, TLS Web Client Authentication
	
	

Now get the csr signed, converted to a p12 and then try to do the &#8220;modify&#8221; install on SRM. This time the IP should match the SRM name.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/srm-fails-to-install-a-custom-certificate-with-he-host-name-in-the-subject-alternative-name-of-the-provided-certificate-does-not-match-the-srm-host-name/" title=" SRM fails to install a custom certificate with &#8220;The host name in the Subject Alternative Name of the provided certificate does not match the SRM host name.&#8221; during a modify install" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Certifications,installation,openssl,srm,blog;button:compact;">I was running through some SRM certificate configuration tests for a customer and ran into this issue. It is actually expected behavior, but the error message is very misleading. I...</a>
</p>