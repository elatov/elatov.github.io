---
title: Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication
author: Jarret Lavallee
layout: post
permalink: /2012/08/using-a-custom-ca-with-vsphere-replication/
dsq_thread_id:
  - 1404673299
categories:
  - SRM
  - Storage
  - VMware
tags:
  - CA
  - Certifications
  - cli
  - command line
  - openssl
  - srm
  - VRMS
  - VRS
  - vSphere Replication
---
<p>A friend of mine recently pointed out this <a href="http://virtualizationinformation.com/srm-certificates-and-sphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtualizationinformation.com/srm-certificates-and-sphere-replication/']);" target="_blank" class="broken_link">blog post</a> when talking about SRM with custom certificates. Oddly enough, I had a similar customer where we hacked away at the VRMS and VRS to get the Root CA into the appliances. Since I just wrote <a href="http://virtuallyhyper.com/2012/08/setting-up-srm-with-custom-certificates/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/setting-up-srm-with-custom-certificates/']);" target="_blank">this blog post</a> about getting SRM installed with a custom Root CA, I figured that I would write one about getting it set up with vSphere replication.</p>
<p><strong>Warning:</strong> I have no idea if this is supported by VMware or not. As far as my personal testing, everything works fine.</p>
<p>Setting up Signed Certificates is normally an easy process if the Root CA is trusted in the VRMS and VRS keystore. The problem is there is not easy way to add a Root CA to the keystores on the VRMS and VRS. So if you have a custom Root CA, or one like <a href="http://www.incommon.org/cert/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.incommon.org/cert/']);" target="_blank">InCommon</a>, which is not in the keystore already you have to hack the appliances.</p>
<p>First, you need to have SRM installed with custom certificates. If you are looking to install SRM with custom certificates, make sure to generate them correctly by following <a href="http://kb.vmware.com/kb/1008390" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1008390']);" target="_blank">this KB</a>. I went over the procedure in <a href="http://virtuallyhyper.com/2012/08/setting-up-srm-with-custom-certificates/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/setting-up-srm-with-custom-certificates/']);" target="_blank">this post</a>. Once you have SRM installed with custom certs and the sites paired, you can start with vSphere replication.</p>
<h2>Configuring the vSphere Replication Management Server (VRMS)</h2>
<h3>Generating Signed Certificates for VRMS</h3>
<p>First off let&#8217;s generate a certificate for the VRMS servers. You will have to generate one for each site.</p>
<p>The documentation is lacking, but you can use the subjectAltName, or use the Common Name (CN) for the certificates. It just needs to match the FQDN. A <a href="http://kb.vmware.com/kb/2013275" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2013275']);" target="_blank">VMware KB</a> article says the following.</p>
<blockquote><p>A valid certificate is signed by a trusted Certificate Authority. VRMS trusts all CAs that the Java Virtual Machine trusts and all certificates stored in opt/vmware/hms/security/hms-truststore.jks file in the new VRMS appliance. The certificate must not be expired, and the certificate subject or alternative subject name must match the FQDN of the server.</p></blockquote>
<p>But it also says</p>
<blockquote><p>The certificate used by each member of a replication server pair must include a Subject Alternative Name attribute. The attribute value is the fully-qualified domain name of the VRMS server host. This value is different for each member of the VRMS server pair. The fully qualified domain name is subject to a case-sensitive comparison. Always use lower case letters when specifying the name during vSphere Replication installation.</p></blockquote>
<p>The current documentation is confusing and severely lacking, but here is what works.</p>
<ul>
<li>The certificate must be a PKCS#12 format with a pfx extension.</li>
<li>You can have either the common name or the subjectAltName match the hostname set in the web interface (VAMI) Either should be sufficient, but having both allows for a custom CA.</li>
<li>The Root CA needs to be added to /opt/vmware/hms/security/hms-truststore.jks.</li>
<li>The certificate cannot have an MD5 signature.</li>
<li>The certificate should have 2048-bit keys.</li>
</ul>
<p>Based on the list above, you can decide how you want to generate the certificate. I will list out the steps that I use below.</p>
<p>So let&#8217;s generate the CSR. First we need to copy over the openssl.cnf locally and edit it for our local changes.</p>
	<p><br />
	# mkdir srm-vrms-prod &amp;amp;&amp;amp; cd srm-vrms-prod<br />
	# cp /etc/ssl/openssl.cnf srm-vrms-prod.cnf<br />
	</p>
<p>Now we need to add the subjectAltName to the srm-vrms-prod.cnf (local copy of the openss.cnf). Since I do not want to put this into the Subject, we need to enable the v3_req extensions. Edit the srm-vrms-prod.cnf and uncomment the following line.</p>
	<p><br />
	req_extensions = v3_req<br />
	</p>
<p>Now find the [ v3_req ] section. In this section we need to add the subjectAltName like the line below.</p>
	<p><br />
	subjectAltName = DNS: srm-vrms-prod.virtuallyhyper.com<br />
	</p>
<p>Save the srm-vrms-prod.cnf file and generate the CSR.</p>
	<p><br />
	# openssl req -new -newkey rsa:2048 -sha1  -nodes -out srm-vrms-prod.csr -keyout srm-vrms-prod.key -config srm-vrms-prod.cnf<br />
	Generating a 2048 bit RSA private key<br />
	...............+++<br />
	................................+++<br />
	writing new private key to 'srm-vrms-prod.key'<br />
	-----<br />
	You are about to be asked to enter information that will be incorporated<br />
	into your certificate request.<br />
	What you are about to enter is what is called a Distinguished Name or a DN.<br />
	There are quite a few fields but you can leave some blank<br />
	For some fields there will be a default value,<br />
	If you enter '.', the field will be left blank.<br />
	-----<br />
	Country Name (2 letter code) [US]:US<br />
	State or Province Name (full name) [Colorado]:Colorado<br />
	Locality Name (eg, city) [Boulder]:Boulder<br />
	Organization Name (eg, company) [Virutallyhyper]:Virtuallyhyper<br />
	Organizational Unit Name (eg, section) [Lab]:Lab<br />
	Common Name (eg, YOUR name) []:srm-vrms-prod.virtuallyhyper.com<br />
	Email Address :admin'@'virtuallyhyper.com<br />
	Please enter the following 'extra' attributes<br />
	to be sent with your certificate request<br />
	A challenge password []:<br />
	An optional company name []:<br />
	</p>
<p>Now we need to sign the certificate. You will likely have to give this to your security admin or request signing from the CA website. Here I am my own CA, so I can sign it locally.</p>
	<p><br />
	# openssl ca -days 3650 -in srm-vrms-prod.csr -out srm-vrms-prod.crt<br />
	</p>
<p>Now let&#8217;s confirm that our CA did not strip off the subjectAltName extension.</p>
	<p><br />
	# openssl x509 -in srm-vrms-prod.crt -text -noout |grep -A1 &amp;quot;Subject Alternative Name&amp;quot;<br />
	            X509v3 Subject Alternative Name:<br />
	                DNS:srm-vrms-prod.virtuallyhyper.com<br />
	</p>
<p>Create the PFX file. Openssl will query you for a password, make sure to use something you will remember.</p>
	<p><br />
	# openssl pkcs12 -export -in srm-vrms-prod.crt -inkey srm-vrms-prod.key -name &amp;quot;srm-vrms-prod&amp;quot; -out srm-vrms-prod.pfx<br />
	</p>
<p>Now we have generated the certificate for the protected site. Please use the same proceedure to create the certificate for the recovery site.</p>
<h3>Installing the certificate into the VRMS</h3>
<p>After getting the SRM servers paired using custom certificates you are ready to deploy the VRMS on both sites. It is best to deploy each VRMS on its respective vCenter to avoid any potential problems. Before deploying the VRMS, make sure you set the &#8220;vCenter Server Managed IP&#8221; in the Runtime Settings of vCenter Server Settings.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/vCenter-Managed-Ip-address.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/vCenter-Managed-Ip-address.png']);"><img class="aligncenter size-full wp-image-1990" title="vCenter Managed Ip address" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/vCenter-Managed-Ip-address.png" alt="vCenter Managed Ip address Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="660" height="643" /></a></p>
<p>Now you can open up the SRM plug-in and click on vSphere replication on the bottom left of the page.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-select-vSphere-Replication.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-select-vSphere-Replication.png']);"><img class="aligncenter size-full wp-image-1991" title="SRM select vSphere Replication" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-select-vSphere-Replication.png" alt="SRM select vSphere Replication Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="292" height="123" /></a></p>
<p>From here you will see the steps to getting vSphere replication going. The first step is to deploy the VRMS. When deploying the appliance you go through a wizard to configure the IP address and set the password.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Deploy-VRMS.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Deploy-VRMS.png']);"><img class="aligncenter size-full wp-image-1992" title="Deploy VRMS" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Deploy-VRMS.png" alt="Deploy VRMS Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="385" height="174" /></a></p>
<p>I would advise deploying the appliances when connected to the respective SRM servers. Then we need to insert the root CA into the java keystore on the VRMS before we configure VRMS.</p>
<p>Once they are deployed on both sites, we will need to ssh into each one of the servers so that we can copy in the certificates. The user name will be root and the password is what you set when deploying the appliance. The problem is that root ssh is disabled by default. So we need to enable root ssh, or create another user on the appliance. Log into the console and run the following commands.</p>
	<p><br />
	# sed -i 's/PermitRootLogon no/PermitRootLogon yes/' /etc/ssh/sshd_config<br />
	# /etc/init.d/sshd restart<br />
	</p>
<p>Alternatively to the commands above, you can edit the /etc/ssh/sshd_config file and change &#8220;PermitRootLogon no&#8221; to &#8220;PermitRootLogon yes&#8221; and then restart the sshd service.</p>
<p>Now ssh into the VRMS using the root user name and the password that we used before. Let&#8217;s create a certificate folder that we are going to put the root CA certificates into.</p>
	<p><br />
	# mkdir /root/certs<br />
	# cd /root/certs<br />
	</p>
<p>Now we need to copy over the certificate to the VRMS. If you are using windows you can use <a href="http://winscp.net" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://winscp.net']);" target="_blank">winscp</a> to copy these, on linux you can scp them over.</p>
	<p><br />
	# scp cacert.crt root'@'srm-vrms-prod.virtuallyhyper.com:/root/certs/<br />
	vSphere Replication Management Server<br />
	root at srm-vrms-prod.virtuallyhyper.com's password:<br />
	cacert.crt           100% |*******************************************************************************************|  1651       00:00<br />
	</p>
<p>Now let&#8217;s add the Root CA Cert to the java keystore for the VRMS. To do this we will use keytool. More syntax can be <a href="http://www.sslshopper.com/article-most-common-java-keytool-keystore-commands.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.sslshopper.com/article-most-common-java-keytool-keystore-commands.html']);" target="_blank">found here</a>. The password for the keystore is &#8220;vmware&#8221;.</p>
	<p><br />
	# cd /opt/vmware/hms/security<br />
	# keytool -import -trustcacerts -alias root -file /root/certs/cacert.crt -keystore hms-truststore.jks<br />
	Enter keystore password:<br />
	Owner: EMAILADDRESS=admin'@'virtuallyhyper.com, CN=virtuallyhyper.com, OU=Lab, O=Virtuallyhyper, L=Boulder, ST=Colorado, C=US<br />
	Issuer: EMAILADDRESS=admin'@'virtuallyhyper.com, CN=virtuallyhyper.com, OU=Lab, O=Virtuallyhyper, L=Boulder, ST=Colorado, C=US<br />
	Serial number: 8c456ac6e8d7d055<br />
	Valid from: Sat Aug 04 17:09:39 UTC 2012 until: Tue Aug 02 17:09:39 UTC 2022<br />
	Certificate fingerprints:<br />
		 MD5:  B6:59:FD:70:D9:1E:24:02:B0:26:69:5E:B7:F2:50:8D<br />
		 SHA1: 0E:BC:68:96:F2:D7:F9:FD:7F:95:4C:31:BB:65:19:8B:B0:30:F9:48<br />
		 Signature algorithm name: SHA1withRSA<br />
		 Version: 3<br />
	Extensions:<br />
	#1: ObjectId: 2.5.29.14 Criticality=false<br />
	SubjectKeyIdentifier [<br />
	KeyIdentifier [<br />
	0000: F4 0A A8 D0 EC A1 9D AC   F8 0D C4 56 6B C1 79 1B  ...........Vk.y.<br />
	0010: 34 87 90 45                                        4..E<br />
	]<br />
	]<br />
	#2: ObjectId: 2.5.29.19 Criticality=false<br />
	BasicConstraints:[<br />
	  CA:true<br />
	  PathLen:2147483647&amp;lt; ] #3: ObjectId: 2.5.29.35 Criticality=false AuthorityKeyIdentifier [ KeyIdentifier [ 0000: F4 0A A8 D0 EC A1 9D AC   F8 0D C4 56 6B C1 79 1B  ...........Vk.y. 0010: 34 87 90 45                                        4..E ] [EMAILADDRESS=admin'@'virtuallyhyper.com, CN=virtuallyhyper.com, OU=Lab, O=Virtuallyhyper, L=Boulder, ST=Colorado, C=US] SerialNumber: [    8c456ac6 e8d7d055] ] Trust this certificate? [no]:  yes Certificate was added to keystore </p>
<p>Let&#8217;s confirm that it actually took the certificate. Run the following command and enter the password (&#8220;vmware&#8221;). You will see the CA certificate that we added.</p>
	<p></p>
	<p>So we have added the Root CA Certificate to the java keystore, but we also need to add it to OS keystore. The OS keystore is located at /etc/ssl/certs/. The format for the the certificates in this directory is that there is a symbolic link that links to the file. The symbolic link name is a hash of the certificate with .0 appended. Let&#8217;s look at the existing Go Daddy certificate in this directory to get an idea of the format.</p>
	<p> # ls -l /etc/ssl/certs/219d9499.0 lrwxrwxrwx 1 root root 23 Feb 25 06:34 219d9499.0 -&amp;gt; Go_Daddy_Class_2_CA.pem<br />
	# ls -l /etc/ssl/certs/Go_Daddy_Class_2_CA.pem<br />
	-rw-r--r-- 1 root root 1448 May  5  2010 Go_Daddy_Class_2_CA.pem<br />
	</p>
<p>So what we need is the hash of our certificate to link to the .pem file. Since my certificate is in pem format, I can copy it over to this directory and change the extension.</p>
	<p><br />
	# cd /etc/ssl/certs/<br />
	# cp /root/certs/cacert.crt /etc/ssl/certs/virtuallyhyper.pem<br />
	# chmod 644 /etc/ssl/certs/virtuallyhyper.pem<br />
	</p>
<p>Now let&#8217;s create the hash symlink to the pem file. Before we make the link, let&#8217;s just confirm that we are not going to overwrite anything.</p>
	<p><br />
	# openssl x509 -noout -hash -in /etc/ssl/certs/virtuallyhyper.pem<br />
	41c89313<br />
	# ls -l 41c89313*<br />
	</p>
<p>If the last ls command did not return anything, let&#8217;s create the symlink.</p>
	<p><br />
	# ln -s /etc/ssl/certs/virtuallyhyper.pem `openssl x509 -noout -hash -in /etc/ssl/certs/virtuallyhyper.pem`.0<br />
	# ls -l 41c89313.0<br />
	lrwxrwxrwx 1 root root 27 Aug  5 01:06 41c8913.0 -&amp;gt; /etc/ssl/certs/virtuallyhyper.pem<br />
	</p>
<p>If you want the web interface (VAMI) to use the certificate you can follow the instructions below. This is optional, but you might as well. Copy over the CRT and KEY files for your certificate to the VRMS server. We will concatenate them and use them for the lighthttpd service that runs the VAMI.</p>
	<p><br />
	scp srm-vrms-prod.key srm-vrms-prod.crt root'@'srm51-vrms-prod.virtuallyhyper.com:/root/certs/<br />
	vSphere Replication Management Server<br />
	root at srm51-vrms-prod.virtuallyhyper.com's password:<br />
	srm-vrms-prod.key      100% |*********************************************************************|  1675       00:00<br />
	srm-vrms-prod.crt      100% |*********************************************************************|  4959       00:00<br />
	</p>
<p>Ssh over to the VRMS again. Now we will concatenate the certificates and then replace the existing self signed certificate.</p>
	<p><br />
	# cd /root/certs/<br />
	# cat srm-vrms-prod.key srm-vrms-prod.crt &amp;gt; srm-vrms-prod.pem<br />
	# mv /opt/vmware/etc/lighttpd/server.pem /opt/vmware/etc/lighttpd/server.pem.old<br />
	# cp /root/certs/srm-vrms-dr.pem /opt/vmware/etc/lighttpd/server.pem<br />
	# /etc/init.d/vami-lighttp restart<br />
	</p>
<p>Let&#8217;s disable root ssh for security reasons. Again you can manually edit the /etc/ssh/sshd_config file and change &#8220;PermitRootLogin&#8221; to no, or you can run the command below.</p>
	<p><br />
	# sed -i 's/PermitRootLogon yes/PermitRootLogon no/' /etc/ssh/sshd_config<br />
	</p>
<p>Now reboot the VRMS to make sure that all changes take effect. Make sure that you do the steps above on both sites.</p>
<h3>Configuring the VRMS</h3>
<p>We can now configure the VRMS on both sites. In the SRM plug-in click on &#8220;Configure the VRM Server&#8221; to launch the web interface.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Configure-VRMS.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Configure-VRMS.png']);"><img class="aligncenter size-full wp-image-1995" title="Configure VRMS" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Configure-VRMS.png" alt="Configure VRMS Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="398" height="277" /></a></p>
<p>Log in to the web interface using the root username and the password you gave it when deploying. Click on the configuration tab. At the bottom you will have an option to upload a PFX certificate. Upload the one we generated previously. It will ask you for the password. Enter the one you used when generating the P12 file.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-upload-certificate.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-upload-certificate.png']);"><img class="aligncenter size-full wp-image-1997" title="VRMS upload certificate" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-upload-certificate.png" alt="VRMS upload certificate Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="570" height="214" /></a></p>
<p>After the certificate has been uploaded, enter all of the information on the page. Make sure to use the FQDN of the VRMS  in the VRM Host section. This is the name or IP it will use to connect to SRM.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-VRM-Host-name.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-VRM-Host-name.png']);"><img class="aligncenter size-full wp-image-1998" title="VRMS VRM Host name" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-VRM-Host-name.png" alt="VRMS VRM Host name Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="554" height="44" /></a></p>
<p>Also make sure to use FQDN <a href="http://kb.vmware.com/kb/2007463" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2007463']);" target="_blank">vCenter Address</a> (Shameless promotion of my KB. Please rate it well), as it will default to the IP address. Otherwise you will get a 404 error and will have to wipe the database.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-vCenter-Server-Address.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-vCenter-Server-Address.png']);"><img class="aligncenter size-full wp-image-1996" title="VRMS vCenter Server Address" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRMS-vCenter-Server-Address.png" alt="VRMS vCenter Server Address Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="572" height="62" /></a></p>
<p>After filling out the correct information click &#8220;Save and Restart Service&#8221;. The VRMS will gather the vCenter and SRM certs. It will complain about the SRM cert. The error will be &#8220;The certificate was not issued for use with the given hostname: srm-dr.virtuallyhyper.com&#8221;. This is because the common name does not match the hostname. This is expected behavior, so accept the certificate.</p>
<p>After it has completed, VRMS will have registered it&#8217;s self with vCenter. If you get a certificate warning in vCenter, you have generated the certificate wrong for VRMS or miss typed the VRM host field. If this is the case examine the certificate to see what is wrong with it.</p>
<p>Now we can pair the VRMS. Click on the &#8220;Configure VRMS Connection&#8221; to pair the VRMS.<br />
<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-VRMS-pairing.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-VRMS-pairing.png']);"><img class="aligncenter size-full wp-image-2004" title="SRM VRMS pairing" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/SRM-VRMS-pairing.png" alt="SRM VRMS pairing Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="392" height="266" /></a></p>
<h2>Deploying and Configuring vSphere Replication Server (VRS)</h2>
<p>Now that we have the VRMS set up with custom certificates and paired, we can deploy the VRS and set them up for custom certificates. The first thing we should do is deploy a VRS on both sites. Click on &#8220;Deploy a VR Server&#8221; to deploy a VRS on both sites.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Deploy1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Deploy1.png']);"><img class="aligncenter size-full wp-image-2006" title="VRS Deploy" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Deploy1.png" alt="VRS Deploy1 Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="383" height="184" /></a></p>
<p>At this point we have a VRS deployed on both sites. If we have setup our certificates correctly we can register the VRS with out having to put custom certificates on the VRS. If you have problems registering the VRS, then you will need to add the custom certificate to the VRS.</p>
<p>The VRS requires a CRT and a Key instead of a PCKS#12. We will need to generate both certificates for all of the VRS we have. You can have more than one on each site, and it is suggested to have multiple VRS depending on the size of your environment. We generate these in the same manner as we did with the VRMS certificates. The one difference is that we are going to add the IP in as a subjectAltName. This is because the VRS has a problem where the hostname <a href="http://kb.vmware.com/kb/2012535" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2012535']);" target="_blank">is always localhost.localdom</a>.</p>
<p>Make a new directory and copy over the openssl.cnf.</p>
	<p><br />
	# mkdir srm-vrs-prod &amp;amp;&amp;amp; cd srm-vrs-prod<br />
	# cp /etc/ssl/openssl.cnf srm-vrs-prod.cnf<br />
	</p>
<p>Like we did with the VRMS we will make the changes again to enable extensions and add in the subjectAltName. Notice that this time we have included the IP and the DNS name.</p>
<p>Uncomment the line below.</p>
	<p><br />
	req_extensions = v3_req<br />
	</p>
<p>Add the subjectAltName to the [ v3_req ] section.</p>
	<p><br />
	subjectAltName = DNS:srm-vrs-prod.virtuallyhyper.com,IP:192.168.10.86<br />
	</p>
<p>Now let&#8217;s generate the CSR using srm-vrs-prod.cnf and then sign it.</p>
	<p><br />
	# openssl req -new -newkey rsa:2048 -sha1  -nodes -out srm-vrs-prod.csr -keyout srm-vrs-prod.key -config srm-vrs-prod.cnf<br />
	Generating a 2048 bit RSA private key<br />
	..............................................+++<br />
	..+++<br />
	writing new private key to 'srm-vrs-prod.key'<br />
	-----<br />
	You are about to be asked to enter information that will be incorporated<br />
	into your certificate request.<br />
	What you are about to enter is what is called a Distinguished Name or a DN.<br />
	There are quite a few fields but you can leave some blank<br />
	For some fields there will be a default value,<br />
	If you enter '.', the field will be left blank.<br />
	-----<br />
	Country Name (2 letter code) [US]:US<br />
	State or Province Name (full name) [Colorado]:Colorado<br />
	Locality Name (eg, city) [Boulder]:Boulder<br />
	Organization Name (eg, company) [Virtuallyhyper]:Virtuallyhyper<br />
	Organizational Unit Name (eg, section) [Lab]:Lab<br />
	Common Name (eg, YOUR name) []:srm-vrs-prod.virtuallyhyper.com<br />
	Email Address :admin'@'virtuallyhyper.com</p>
	<p>Please enter the following 'extra' attributes<br />
	to be sent with your certificate request<br />
	A challenge password []:<br />
	An optional company name []:<br />
	# openssl ca -days 3650 -in srm-vrs-prod.csr -out srm-vrs-prod.crt<br />
	</p>
<p>Now we have to install the CA into VRS the same way we did on the VRMS. We will inset the Root CA Certificate into /etc/ssl/certs and make the symbolic link.</p>
<p>The nice thing about VRS is that root SSH is enabled by default. The first thing we need to do is ssh to the VRS and make a directory to copy over the certificates. The default root password is &#8220;vmware&#8221;</p>
	<p><br />
	# mkdir /root/certs<br />
	</p>
<p>scp the certificates we made and the Root CA certificate over to the VRS.</p>
	<p><br />
	# scp srm-vrs-prod.key srm-vrs-prod.crt cacert.crt root'@'srm-vrs-prod.virtuallyhyper.com:/root/certs/<br />
	</p>
<p>Now we can install the Root CA Certificate into /etc/ssl/certs/</p>
	<p><br />
	# cd /etc/ssl/certs/<br />
	# cp /root/certs/cacert.crt virtuallyhyper.pem<br />
	# ls -l `openssl x509 -noout -hash -in /etc/ssl/certs/virtuallyhyper.pem`*<br />
	# ln -s /etc/ssl/certs/virtuallyhyper.pem `openssl x509 -noout -hash -in /etc/ssl/certs/virtuallyhyper.pem`.0<br />
	</p>
<p>Now we can replace the web interface (VAMI) certificates with the ones we generated. This is optional.</p>
	<p><br />
	# cd /root/certs/<br />
	# cat srm-vrs-prod.key srm-vrs-prod.crt &amp;gt; srm-vrs-prod.pem<br />
	# mv /opt/vmware/etc/lighttpd/server.pem /opt/vmware/etc/lighttpd/server.pem.old<br />
	# cp /root/certs/srm-vrs-prod.pem /opt/vmware/etc/lighttpd/server.pem<br />
	# /etc/init.d/vami-lighttp restart<br />
	</p>
<p>Now log into the web interface for the VRS. You can do this by clicking on the &#8220;Configure VR Server&#8221; link in the SRM plug-in. You can also get there by going to https://srm-vrs-prod.virtuallyhyper.com:5480 (sub in your FQDN). The username is root and the password &#8220;vmware&#8221;. Click on the &#8220;VR Server&#8221; tab. In here you will see a section where you can upload the certificates we generated.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Certificate-upload.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Certificate-upload.png']);"><img class="aligncenter size-full wp-image-2013" title="VRS Certificate upload" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/VRS-Certificate-upload.png" alt="VRS Certificate upload Using Custom Root CA Certificates with VMware SRM 5.x vSphere Replication" width="272" height="186" /></a></p>
<p>Once the certificates are uploaded, go back to the SRM plug-in and register the VRS. Everything should be configured to use the custom certificates.</p>
