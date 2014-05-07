---
title: Installing SRM with custom certificates
author: Jarret Lavallee
layout: post
permalink: /2012/08/setting-up-srm-with-custom-certificates/
dsq_thread_id:
  - 1404673273
categories:
  - SRM
  - VMware
tags:
  - CA
  - Certifications
  - how-to
  - installation
  - openssl
  - Root CA
  - srm
  - subjectAltName
  - vcenter
---
<p>Often I will run into a customer that has custom certificates on their vCenter and are having problems setting up and installing SRM. The problem is that SRM and vCenter need to use the same trust method, so we need to have custom certs for SRM as well. Normally this is not a problem, but SRM is <strong>very</strong> picky on how the certs are configured.</p>
<p>In this post, we will go through the process of setting up custom certs for both vCenter and SRM.  In this series I am using sha1 certificates because Windows 2003 does not come with <a href="http://support.microsoft.com/kb/938397" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://support.microsoft.com/kb/938397']);" target="_blank">sha2 until this hotfix</a>.</p>
<p>Below I use <a href="http://www.openssl.org" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openssl.org']);" target="_blank">openssl</a> on a Solaris machine, but Openssl is available across many operating systems. The windows <a href="http://www.openssl.org/related/binaries.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openssl.org/related/binaries.html']);" target="_blank">binaries are here</a>. The openssl commands are operating system independent. Commands like cp and vi, should be replaced with GUI operations.</p>
<h2>Installing the Root CA into the Trusted Root Certification Authorities</h2>
<p>This was one of the biggest frustrations for me. There are many errors that will come up saying that the certificate is not trusted, but when you look at the certificate it may say that it is. The key is to install the certificate to the Local Computer Trusted Root Certification Authorities. When installing a certificate by right clicking on the certificate, it will add it to the user&#8217;s certificates, but not for the local computer.</p>
<p>First we need to get the CA&#8217;s public certificate that we want to install in the Trusted Root CAs. First let&#8217;s open up the certificate and ensure that it is not trusted already.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/CA-Root-not-trusted.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/CA-Root-not-trusted.jpg']);"><img class="aligncenter size-full wp-image-1955" title="CA Root not trusted" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/CA-Root-not-trusted.jpg" alt="CA Root not trusted Installing SRM with custom certificates" width="410" height="510" /></a></p>
<p>After opening the certificate we can see that the CA Root is not trusted. If you run the  &#8220;Install Certificate&#8221; it will install it for your user and not for the local computer, so go ahead and close this window.</p>
<p>Go to Start-&gt; Run and run &#8220;mmc.exe&#8221;. Once in the MMC, we need to add the Certificates snap in. Click on &#8220;File-&gt;Add/Remove Snap-in&#8230;&#8221;.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Console-Add-Snap-in.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Console-Add-Snap-in.png']);"><img class="aligncenter size-full wp-image-1956" title="Console Add Snap-in" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Console-Add-Snap-in.png" alt="Console Add Snap in Installing SRM with custom certificates" width="393" height="302" /></a></p>
<p>On the next screen we want to select Certificates on the Left and hit the add button. Make sure to select the Computer account.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Add-Computer-account-certificates.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Add-Computer-account-certificates.png']);"><img class="aligncenter size-full wp-image-1957" title="Add Computer account certificates" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Add-Computer-account-certificates.png" alt="Add Computer account certificates Installing SRM with custom certificates" width="677" height="469" /></a></p>
<p>When the Certificates Snap-In is added, we want to browse to the &#8220;Trusted Root Certification Authorities -&gt; Certificates&#8221;. In the end we want to see our Root CA Certificate listed here. In my case it is not here, that is why my certificate is not trusted. So we need to import it. Right click on &#8220;Certificates&#8221; and select &#8220;All Tasks-&gt; Import&#8221;.<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-to-Trusted-root.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-to-Trusted-root.png']);"><img class="aligncenter size-full wp-image-1958" title="Import Certificate to Trusted root" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-to-Trusted-root.png" alt="Import Certificate to Trusted root Installing SRM with custom certificates" width="429" height="320" /></a></p>
<p>This will bring up the import certificate wizard. You should browse to the Root CA Certificate we opened initially. We want to ensure it is put into the Trusted Root Certification Authorities.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-into-Trusted-CA.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-into-Trusted-CA.jpg']);"><img class="aligncenter size-full wp-image-1959" title="Import Certificate into Trusted CA" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Import-Certificate-into-Trusted-CA.jpg" alt="Import Certificate into Trusted CA Installing SRM with custom certificates" width="503" height="453" /></a></p>
<p>Once you have imported the CA Root Certificate we should see it listed in the Trusted Root Certification Authorities.  Below we can see that the virtuallyhyper.com certificate is in there.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Cert-in-trusted-root.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Cert-in-trusted-root.png']);"><img class="aligncenter size-full wp-image-1960" title="Cert in trusted root" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Cert-in-trusted-root.png" alt="Cert in trusted root Installing SRM with custom certificates" width="499" height="178" /></a></p>
<p>Let&#8217;s check out the certificate again to confirm that is is now trusted. Go back to where you have stored your Root CA CRT on the server. Double click on the Root CA CRT file to open it again.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Trusted-Root-CA-Cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Trusted-Root-CA-Cert.png']);"><img class="aligncenter size-full wp-image-1962" title="Trusted Root CA Cert" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Trusted-Root-CA-Cert.png" alt="Trusted Root CA Cert Installing SRM with custom certificates" width="410" height="508" /></a></p>
<p>Repeat this process for both vCenter servers and both SRM servers. If this is the Root CA for your domain, you may want to consider adding it to a GPO.</p>
<h2>Generating and Installing vCenter certificates</h2>
<p>There are many set of instructions to follow when generating and installing custom certs for vCenter. <a href="http://kb.vmware.com/kb/1003921" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1003921']);" target="_blank">KB 1003921</a> describes the basic process. I will not go in depth here, but I will list my steps for generating the certificates. If you are looking for some more detail please see <a href="http://geeksilver.wordpress.com/2011/05/13/how-to-use-ca-certificate-to-replace-vmware-certificate-on-esxi-4-and-vcenter/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://geeksilver.wordpress.com/2011/05/13/how-to-use-ca-certificate-to-replace-vmware-certificate-on-esxi-4-and-vcenter/']);" target="_blank">this blog post</a> or <a href="http://www.wooditwork.com/2011/11/30/vsphere-5-certificates-3-replacing-the-default-vcenter-5-server-certificate-2-2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.wooditwork.com/2011/11/30/vsphere-5-certificates-3-replacing-the-default-vcenter-5-server-certificate-2-2/']);" target="_blank">this one</a>.  See <a href="http://longwhiteclouds.com/2012/02/13/vcenter-server-virtual-appliance-changing-ssl-certs-made-easy/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://longwhiteclouds.com/2012/02/13/vcenter-server-virtual-appliance-changing-ssl-certs-made-easy/']);" target="_blank">this blog post</a> if you are using the Linux vCenter appliance.</p>
<p>First we need to generate the CSR. We can do this with openssl. I changed my openssl.cnf, so I do not have to type in the some values, so you should enter your information correctly.</p>
	<p></p>
	<h1>mkdir vcenter-prod &amp;&amp; cd vcenter-prod</h1>
	<h1>openssl req -new -newkey rsa:2048 -sha1  -nodes -out rui.csr -keyout rui.key</h1>
	<p>You are about to be asked to enter information that will be incorporated<br />
	into your certificate request.<br />
	What you are about to enter is what is called a Distinguished Name or a DN.<br />
	There are quite a few fields but you can leave some blank<br />
	For some fields there will be a default value,</p>
	<h2>If you enter '.', the field will be left blank.</h2>
	<p>Country Name (2 letter code) [US]: US<br />
	State or Province Name (full name) [Colorado]: Colorado<br />
	Locality Name (eg, city) [Boulder]: Boulder<br />
	Organization Name (eg, company) [Virtuallyhyper]: Virtuallyhyper<br />
	Organizational Unit Name (eg, section) [Lab]: Lab<br />
	Common Name (eg, YOUR name) []:srm-prod.virtuallyhyper.com<br />
	Email Address :admin'@'virtuallyhyper.com</p>
	<p>Please enter the following 'extra' attributes<br />
	to be sent with your certificate request<br />
	A challenge password []:<br />
	An optional company name []:<br />
	</p>
<p>Now we need to sign the CSR. You will do with with your root CA, so the steps will likely be different.</p>
	<p></p>
	<h1>openssl ca -days 3650 -in rui.csr -out rui.crt</h1>
	<p></p>
<p>Next we have to merge the signed certificate and the private key into the PFX file. The PFX will require a password, which will be set to &#8220;testpassword&#8221; in the command. vCenter will expect this to be &#8220;testpassword&#8221;, so please do not change it.</p>
	<p></p>
	<h1>openssl pkcs12 -export -in rui.crt -inkey rui.key -name &quot;rui&quot; -passout pass:testpassword -out rui.pfx</h1>
	<p></p>
<p>Now that we have generated and signed our certificate we need to install it for vCenter. You need to copy the rui.pfx, rui.key and the rui.crt to the SSL directory for vCenter. Make sure to back up the original ones first. The SSL folder is located in the application directory for vCenter.</p>
	<p><br />
	Windows 2003 C:\Documents and Settings\All Users\Application Data\VMware\VMware VirtualCenter\SSL<br />
	Windows 2008/R2 C:\ProgramData\VMware\VMware VirtualCenter\SSL<br />
	</p>
<p>Now we should stop the vCenter service and <a href="http://kb.vmware.com/kb/1003070" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1003070']);" target="_blank">update the database password</a>. Make sure to run the Command Prompt as an Administrator.</p>
	<p><br />
	C:\Documents and Settings\jarret&gt; net stop vpxd<br />
	C:\Documents and Settings\jarret&gt;&quot;c:\Program Files\VMware\Infrastructure\Virtual<br />
	Center Server\vpxd.exe&quot; -p<br />
	C:\Documents and Settings\jarret&gt; net start vpxd<br />
	C:\Documents and Settings\jarret&gt; net start vctomcat<br />
	</p>
<p>Now you can test vCenter to confirm that everything is working and the new certificate is installed. Make sure to generate and install the certificate on both the protected and the recovery sites. Go ahead and reconnect all of the hosts.</p>
<h2>Generating and installing SRM certs</h2>
<p>There is an excellent write up about this that can be found <a href="http://communities.vmware.com/docs/DOC-11411" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-11411']);" target="_blank">here</a>. The requirements are listed in <a href="http://kb.vmware.com/kb/1008390" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1008390']);" target="_blank">this KB article</a>. The problem is that the details are easy to miss and it can be a huge headache. The biggest thing to remember is that the <strong>Subject for both certificates need to be the same</strong>. That means that the <strong>CN,O,OU,C,S and L need to be the same for the certificates for both SRM servers</strong>.</p>
<h3>Generating the Protected Site SRM Certificate</h3>
<p>First lets generate the CSR for the protected site SRM server. I did not set up a separate SRM server in this lab, so I am installing SRM on to the vCenter server. We still need to generate a new certificate for SRM on this server.</p>
<p>We need to make some changes to the openssl.cnf. First lets copy this to our current directory so we can modify some properties for this certificate. If you are using windows, there will be a local copy of openssl.cfg. Copy that to another file name (I.e srm-prod.cnf) and make the changes there.</p>
	<p></p>
	<h1>mkdir srm-prod &amp;&amp; cd srm-prod</h1>
	<h1>cp /etc/ssl/openssl.cnf srm-prod.cnf</h1>
	<p></p>
<p>Open up the srm-dr.cnf and make sure to add a subjectAltName. It should look like the one below. Make sure that it is correct case, as it is case sensitive. We also need to add clientAuth to all for client authentication. This is a requirement for trusted certs with SRM. Make sure not to put the subjectAltName into the subject section ([ req_distinguished_name ]) as the subjects need to be the same for both certs. To get by this we can add it as an extension of the certificate.</p>
<p>Find the line below and uncomment it. It should be found in the [ req ] section</p>
	<p><br />
	req_extensions = v3_req<br />
	</p>
<p>The go down to the [ v3_ca ] section and put in the following lines.</p>
	<p><br />
	subjectAltName=DNS:srm-prod.virtuallyhyper.com<br />
	extendedKeyUsage = serverAuth, clientAuth<br />
	</p>
<p>Now we can generate the CSR. Notice how the CN is &#8220;srm&#8221;. The Subject (all of the fields below) needs to be exactly the same across both SRM certificates. The subjectAltName above is what will define the hostname for SRM. Check out this post about using <a href="http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/']);" title="SRM 5.x Custom SSL Certificates with Multiple Subject Alternative Names" target="_blank">multiple subjectAltNames</a>.</p>
	<p></p>
	<h1>openssl req -new -newkey rsa:2048 -sha1  -nodes -out srm-prod.csr -keyout srm-prod.key -config srm-prod.cnf</h1>
	<p>You are about to be asked to enter information that will be incorporated<br />
	into your certificate request.<br />
	What you are about to enter is what is called a Distinguished Name or a DN.<br />
	There are quite a few fields but you can leave some blank<br />
	For some fields there will be a default value,</p>
	<h2>If you enter '.', the field will be left blank.</h2>
	<p>Country Name (2 letter code) [US]: US<br />
	State or Province Name (full name) [Colorado]: Colorado<br />
	Locality Name (eg, city) [Boulder]: Boulder<br />
	Organization Name (eg, company) [Virtuallyhyper]: Virtuallyhyper<br />
	Organizational Unit Name (eg, section) [Lab]: Lab<br />
	Common Name (eg, YOUR name) []:srm<br />
	Email Address : admin'@'virtuallyhyper.com</p>
	<p>Please enter the following 'extra' attributes<br />
	to be sent with your certificate request<br />
	A challenge password []:<br />
	An optional company name []:<br />
	</p>
<p>Check to ensure that the subjectAltName and client authentication is in the CSR. You can open the certificate in Windows and visually check it.</p>
	<p></p>
	<h1>openssl req -text -noout  -in srm-prod.csr |egrep -A 1 &quot;Subject Alternative Name|Extended Key Usage&quot;</h1>
		        X509v3 Subject Alternative Name:
		            DNS:srm-prod.virtuallyhyper.com
		        X509v3 Extended Key Usage:
		            TLS Web Server Authentication, TLS Web Client Authentication
		
	<p></p>
<p>Now sign your certificate with your Root CA. This step will be different in your environment. You will likely have to sent the CSR to the security administrator, or insert it into a central Root CA website.</p>
	<p></p>
	<h1>openssl ca -days 3650 -in srm-prod.csr -out srm-prod.crt</h1>
	<p></p>
<p>Let&#8217;s make sure that the CA did not strip off our extensions. Again you can check this visually by opening the certificate in Windows.</p>
	<p></p>
	<h1>openssl x509 -in srm-prod.crt -text -noout |egrep -A 1 &quot;Subject Alternative Name|Extended Key Usage&quot;</h1>
		        X509v3 Subject Alternative Name:
		            DNS:srm-prod.virtuallyhyper.com
		        X509v3 Extended Key Usage:
		            TLS Web Server Authentication, TLS Web Client Authentication
		
	<p></p>
<p>Next we need to create the p12.  ( SRM needs a p12 and vCenter needs a PFX)  When running the command below it will ask you for a password. This will need to be entered when importing the SRM certificate when adding the p12.</p>
	<p></p>
	<h1>openssl pkcs12 -export -in srm-prod.crt -inkey srm-prod.key -out srm-prod.p12</h1>
	<p></p>
<h3>Generating the Recovery Site SRM Certificate</h3>
<p>No we have to generate the recovery site SRM certificate. Let&#8217;s copy over the openssl.cnf into our new folder.</p>
	<p></p>
	<h1>mkdir srm-dr &amp;&amp; cd srm-dr</h1>
	<h1>cp /etc/ssl/openssl.cnf srm-dr.cnf</h1>
	<p></p>
<p>Make the modifications to srm-dr.cnf again.</p>
	<p><br />
	req_extensions = v3_req</p>
	<p>...</p>
	<p>subjectAltName=DNS:srm-dr.virtuallyhyper.com<br />
	extendedKeyUsage = serverAuth, clientAuth<br />
	</p>
<p>Generate the CSR and sign it. Remember this is with the same values as above.</p>
	<p></p>
	<h1>openssl req -new -newkey rsa:2048 -sha1  -nodes -out srm-dr.csr -keyout srm-dr.key -config srm-dr.cnf</h1>
	<p>You are about to be asked to enter information that will be incorporated<br />
	into your certificate request.<br />
	What you are about to enter is what is called a Distinguished Name or a DN.<br />
	There are quite a few fields but you can leave some blank<br />
	For some fields there will be a default value,</p>
	<h2>If you enter '.', the field will be left blank.</h2>
	<p>Country Name (2 letter code) [US]: US<br />
	State or Province Name (full name) [Colorado]: Colorado<br />
	Locality Name (eg, city) [Boulder]: Boulder<br />
	Organization Name (eg, company) [Virtuallyhyper]: Virtuallyhyper<br />
	Organizational Unit Name (eg, section) [Lab]: Lab<br />
	Common Name (eg, YOUR name) []:srm<br />
	Email Address :admin'@'virtuallyhyper.com</p>
	<p>Please enter the following 'extra' attributes<br />
	to be sent with your certificate request<br />
	A challenge password []:<br />
	An optional company name []:</p>
	<h1>openssl ca -days 3650 -in srm-dr.csr -out srm-dr.crt</h1>
	<h1>openssl pkcs12 -export -in srm-dr.crt -inkey srm-dr.key -out srm-dr.p12</h1>
	<p></p>
<p>Let&#8217;s check to ensure that the CA did not strip off our extensions.</p>
	<p></p>
	<h1>openssl x509 -in srm-prod.crt -text -noout |egrep -A 1 &quot;Subject Alternative Name|Extended Key Usage&quot;</h1>
		        X509v3 Subject Alternative Name:
		            DNS:srm-dr.virtuallyhyper.com
		        X509v3 Extended Key Usage:
		            TLS Web Server Authentication, TLS Web Client Authentication
		
	<p></p>
<h3>Installing SRM with the certificates</h3>
<p>Now what we have generated the certificates we need to install SRM with them. Open up the SRM installer as an administrator. Make sure to use FQDN for all of the answers. If you already have SRM installed you can add them by doing a &#8220;Modify&#8221; install.</p>
<p>Make sure to enter the FQDN of the vCenter server and an administrator account on the vCenter Server. It does not have to the local administrator account.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-1-vCenter.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-1-vCenter.png']);"><img class="aligncenter size-full wp-image-1967" title="SRM install Step 1 - vCenter" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-1-vCenter.png" alt="SRM install Step 1 vCenter Installing SRM with custom certificates" width="505" height="380" /></a></p>
<p>A few more pages in, we will see a page asking if you want to use the self generated certificates, or a p12 certificate. Select the p12 certificate option. On the next page you will select the p12 certificate we generated above. Enter the password you used when packing it into a p12.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-3-select-p12-certificate.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-3-select-p12-certificate.png']);"><img class="aligncenter size-full wp-image-1968" title="SRM install Step 3 - select p12 certificate" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-install-Step-3-select-p12-certificate.png" alt="SRM install Step 3 select p12 certificate Installing SRM with custom certificates" width="505" height="380" /></a></p>
<p>When you hit next, it will evaluate the certificate. If you get the error below, you did not add the Root CA Certificate to the Trusted Root Certification Authorities. Please go back to the &#8220;Installing the Root CA into the Trusted Root Certification Authorities&#8221; section.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-Trusted-root.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-Trusted-root.png']);"><img class="aligncenter size-full wp-image-1969" title="Failed to validate certificate - Trusted root" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-Trusted-root.png" alt="Failed to validate certificate Trusted root Installing SRM with custom certificates" width="411" height="178" /></a></p>
<p>The next page will be where we enter the local site name. We need to make sure that what we enter here is the same as we put in the subjectAltName in the certificate. The &#8220;Local Host&#8221; will default to the IP address, so make sure to correct it to the FQDN.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg']);"><img class="aligncenter size-full wp-image-1918" title="SRM installer FQDN" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/enter-the-fqdn.jpg" alt="enter the fqdn Installing SRM with custom certificates" width="504" height="379" /></a></p>
<p>If the Local Host name does not exactly match the one in the subjectAltName we will get the error below. Please check out <a title="SRM fails to install a custom certificate" href="http://virtuallyhyper.com/2012/08/srm-fails-to-install-a-custom-certificate-with-he-host-name-in-the-subject-alternative-name-of-the-provided-certificate-does-not-match-the-srm-host-name" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-fails-to-install-a-custom-certificate-with-he-host-name-in-the-subject-alternative-name-of-the-provided-certificate-does-not-match-the-srm-host-name']);" target="_blank">this post</a> on how to troubleshoot this error.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-FQDN.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-FQDN.png']);"><img class="aligncenter size-full wp-image-1970" title="Failed to validate certificate - FQDN" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Failed-to-validate-certificate-FQDN.png" alt="Failed to validate certificate FQDN Installing SRM with custom certificates" width="405" height="177" /></a></p>
<p>After this you will have to set up the database and finish the installer. Please repeat this step for the recovery site SRM server to have SRM installed on both sites. The installers can run in parallel to save time.</p>
<p>If the installers have completed you can now pair the sites and configure SRM.</p>
<div class="SPOSTARBUST-Related-Posts"><H3>Related Posts</H3><ul class="entry-meta"><li class="SPOSTARBUST-Related-Post"><a title="Certifications" href="http://virtuallyhyper.com/2012/09/certifications/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/certifications/']);" rel="bookmark">Certifications</a></li>
</ul></div><p class="wp-flattr-button"><a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/setting-up-srm-with-custom-certificates/" title=" Installing SRM with custom certificates" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:CA,Certifications,how-to,installation,openssl,Root CA,srm,subjectAltName,vcenter,blog;button:compact;">VCAP5-DCD VCAP5-DCA RHCSA and RHCE</a></p>