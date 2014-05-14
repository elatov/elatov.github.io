---
title: Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment
author: Karim Elatov
layout: post
permalink: /2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/
dsq_thread_id:
  - 1404673780
categories:
  - Home Lab
  - OS
tags:
  - Cert_Authority
  - gnomint
  - Group_Policies
---
In <a href="http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/']);">this</a> previous post, I deployed a test IIS Server and used a self signed SSL Certificate to encrypt the HTTP traffic. I am sure everyone have seen this page in Internet Explorer:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/IE_cert_error.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/IE_cert_error.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/IE_cert_error.png" alt="IE cert error Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="776" height="348" class="alignnone size-full wp-image-8438" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

When I clicked &#8220;View Certificate&#8221;, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/view_certificate.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/view_certificate.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/view_certificate.png" alt="view certificate Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="405" height="508" class="alignnone size-full wp-image-8439" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

We can see that certificate is issued by the same entity as the site-name itself. We can also see that the Root CA is not trusted. Since this is a self-signed Certificate, you are the Root CA in a manner of speaking. My goal is to get rid of that message and to become a &#8220;trusted&#8221; Certificate Authority (CA) in my local Windows Environment.

## Choosing a free Certificate Authority software

If we take a look at this <a href="http://en.wikipedia.org/wiki/Certificate_authority#Open_source_implementations" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Certificate_authority#Open_source_implementations']);">wikipedia</a> page, we will see the following list of available software:

> *   <a href="http://pki.fedoraproject.org/wiki/PKI_Main_Page" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pki.fedoraproject.org/wiki/PKI_Main_Page']);">DogTag</a>
> *   <a href="http://www.ejbca.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ejbca.org/']);">EJBCA</a>
> *   <a href="http://gnomint.sourceforge.net/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://gnomint.sourceforge.net/']);">gnoMint</a>
> *   <a href="http://www.openca.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openca.org/']);">OpenCA</a>
> *   <a href="http://www.openssl.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openssl.org/']);">OpenSSL</a>, which is really an SSL/TLS library, but comes with tools allowing its use as a simple certificate authority.
> *   <a href="https://github.com/reaperhulk/r509" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/reaperhulk/r509']);">r509</a>
> *   <a href="http://xca.sourceforge.net/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://xca.sourceforge.net/']);">XCA</a>

There is actually one more that I ran into, it&#8217;s called <a href="http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/']);">tinyCA</a>.

### Using OpenSSL Commands to Setup a CA

*DogTag*, *EJBCA*, and *OpenCA* were full blown Public-Key Infrastructure (PKI) applications and I didn&#8217;t need all of the extra functionally. There are a lot of examples on how to setup your own CA with **openssl**:

*   <a href="http://www.g-loaded.eu/2005/11/10/be-your-own-ca/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.g-loaded.eu/2005/11/10/be-your-own-ca/']);">Be your own Certificate Authority (CA)</a>
*   <a href="http://www.ulduzsoft.com/2012/01/creating-a-certificate-authority-and-signing-the-ssl-certificates-using-openssl/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ulduzsoft.com/2012/01/creating-a-certificate-authority-and-signing-the-ssl-certificates-using-openssl/']);">Creating a Certificate Authority and signing the SSL certificates using openssl</a>
*   <a href="http://archive09.linux.com/feature/38315" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://archive09.linux.com/feature/38315']);">Be your own CA</a>
*   <a href="http://www.davidpashley.com/articles/cert-authority.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.davidpashley.com/articles/cert-authority.html']);">Becoming a X.509 Certificate Authority</a>

I have done that before and when you are managing a lot of different certificates the process is not very scalable. Also, if you don&#8217;t keep doing it, you have to re-trace your steps to remember how the setup works. There is also a **Perl** script that is included to ease the CA setup, that script is called **CA.pl**. Depending on your Linux distribution you have find the right package that contains that script. Here is where I found it on my Fedora install:

    [elatov@klaptop ~]$ yum provides "*/CA.pl*"
    Loaded plugins: langpacks, presto, refresh-packagekit, remove-with-leaves
    1:openssl-perl-1.0.1c-7.fc18.x86_64 : Perl scripts provided with OpenSSL
    Repo        : fedora
    Matched from:
    Filename    : /etc/pki/tls/misc/CA.pl
    Filename    : /usr/share/man/man1/CA.pl.1ssl.gz
    

You can check out examples from &#8220;<a href="http://www.tipcache.com/tip/Setup_your_own_Certificate_Authority_%28CA%29_11.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.tipcache.com/tip/Setup_your_own_Certificate_Authority_%28CA%29_11.html']);">Setup your own Certificate Authority</a>&#8221; and <a href="http://wls.wwco.com/security/myca.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wls.wwco.com/security/myca.html']);">Becoming a CA Authority</a> on how to use the Perl script; here is a very high level overview:

    #Generate CA Certificate
    CA.pl -newca
    
    #Generate a Certificate Signing Request (CSR)
    CA.pl -newreq
    
    #Sign the CSR with your CA key
    CA.pl -sign
    

### TinyCA

This time around I wanted a pretty GUI that will handle all of the **openssl** commands for me and store the certificate database as well. Maybe I am getting lazy? or hopefully efficient. Among the other applications, TinyCA stood out the most. I found many guides on how to use it:

*   <a href="http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/']);">Create your own Certificate Authority with TinyCA</a> 
*   <a href="http://theworldofapenguin.blogspot.com/2007/06/create-your-own-ca-with-tinyca2-part-1.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://theworldofapenguin.blogspot.com/2007/06/create-your-own-ca-with-tinyca2-part-1.html']);">Create your own CA with TinyCA2 (part 1)</a> 
*   <a href="http://adminadventure.wordpress.com/2012/07/10/create-your-own-certificate-authority-with-tinyca2-and-debian-squeeze/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://adminadventure.wordpress.com/2012/07/10/create-your-own-certificate-authority-with-tinyca2-and-debian-squeeze/']);">Create your own Certificate Authority with TinyCA2 and Debian Squeeze</a>

As I started to install the software I noticed that it wasn&#8217;t part of the Fedora repositories:

    [elatov@klaptop ~]$ yum search tinyca
    Loaded plugins: langpacks, presto, refresh-packagekit, remove-with-leaves
    Warning: No matches found for: tinyca
    No Matches found
    

That didn&#8217;t stop me; I downloaded the application and installed it manually. After setting up my Root CA, the application crashed with the following error:

    Use of uninitialized value $mday in concatenation (.) or string at /usr/share/perl5/Time/Local.pm line 116, <gen11> line 3.
    Day '' out of range 1..31 at /usr/local/tinyca2/lib/OpenSSL.pm line 1050.
    

I found <a href="http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=702233" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=702233']);">this</a> bug and the issue was with a later version of **openssl** (which I had on my Fedora 18 install). The fix was included in Debian based distributions. However I was running Fedora and I didn&#8217;t want to keep patching the software manually, if it kept having issues. So I decided to try out **gnomint**.

## Install Gnomint and Create a Root CA Certificate

Luckily *Gnomint* was part of the Fedora packages, so a simple:

    yum install gnomint
    

Took care of all my troubles. Then running **gnomint** launched the GUI for me:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_started.png" alt="gnomint started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="395" height="268" class="alignnone size-full wp-image-8440" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then I clicked on &#8220;Add Autosigned CA certificate&#8221; and it showed me the &#8220;New CA&#8221; dialog:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca.png" alt="gnomint new ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="548" height="325" class="alignnone size-full wp-image-8441" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Here is what I entered for my new CA certificate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_filledout.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_filledout.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_filledout.png" alt="gnomint new ca filledout Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="548" height="325" class="alignnone size-full wp-image-8504" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then if you click &#8220;Next&#8221; you will see the &#8220;New CA Properties&#8221; window:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_props.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_props.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_new_ca_props.png" alt="gnomint new ca props Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="548" height="325" class="alignnone size-full wp-image-8442" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Choose what you think is necessary; the higher the bit count the better the encryption is. Click &#8220;Next&#8221; and you will be asked to provide the &#8220;CRL Distribution Point&#8221;. This is included with the Root CA Certificate. If a certificate is revoked, people can check for that at this &#8220;Destribution Point&#8221;/Link. I won&#8217;t be a public CA, so I left this blank:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_crl_dist_point.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_crl_dist_point.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_crl_dist_point.png" alt="gnomint crl dist point Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="548" height="325" class="alignnone size-full wp-image-8443" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

I then clicked &#8220;OK&#8221; and my new Root CA Certificate was created:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_root_ca_created.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_root_ca_created.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_root_ca_created.png" alt="gnomint root ca created Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="618" height="284" class="alignnone size-full wp-image-8444" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

## Generate a new Certificate Request and Sign it with your Root CA Certificate in Gnomint

At this point we can generate a Certificate Signing Request (CSR) by clicking on &#8220;Add CSR&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req.png" alt="gnomint csr req Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="514" height="325" class="alignnone size-full wp-image-8445" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After &#8220;Inheriting CA Fields&#8221; we can click &#8220;Next&#8221; and fill out the Request:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_req_props_filled_out.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_req_props_filled_out.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_req_props_filled_out.png" alt="gnomint req props filled out Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="514" height="325" class="alignnone size-full wp-image-8446" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

I went ahead and requested for a &#8220;wildcard&#8221; (*.domain.com) certificate just to have one certificate cover my test windows domain. This way I can import one Certificate on both of my IIS servers. Clicking &#8220;Next&#8221; will take us to the Encryption details, I left the defaults here (I know with Windows as long as it&#8217;s above 2048 bits then it should work):

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req_enc.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req_enc.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_req_enc.png" alt="gnomint csr req enc Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="514" height="325" class="alignnone size-full wp-image-8447" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Clicking &#8220;OK&#8221; created the CSR:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_created.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_created.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_csr_created.png" alt="gnomint csr created Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="618" height="284" class="alignnone size-full wp-image-8448" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

To &#8220;Sign&#8221; the CSR, just right click on it and select &#8220;Sign&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr.png" alt="gnomint sign csr Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="669" height="370" class="alignnone size-full wp-image-8449" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

and the following window will show up:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_diag.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_diag.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_diag.png" alt="gnomint sign csr diag Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="394" height="336" class="alignnone size-full wp-image-8450" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Click &#8220;Next&#8221; and it will ask you to choose the CA to sign with:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_choose_ca.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_choose_ca.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_choose_ca.png" alt="gnomint sign csr choose ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="394" height="336" class="alignnone size-full wp-image-8451" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After clicking &#8220;Next&#8221; we choose how long the certificate is valid for and what it can be used for:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_uses.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_uses.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_sign_csr_uses.png" alt="gnomint sign csr uses Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="509" height="535" class="alignnone size-full wp-image-8452" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

The defaults were fine with me, clicking &#8220;OK&#8221; finished the process and I now had a signed certificate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_signed_cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_signed_cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_signed_cert.png" alt="gnomint signed cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="710" height="378" class="alignnone size-full wp-image-8453" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

## Check out the Gnomint Database

Save your database in gnomint and a file called **~/.gnomint/default.gnomint** will be created. That is just an **sqlite3** database, so we can check out the contents to make sure it looks good. So go ahead and open up the database:

    [elatov@klaptop .gnomint]$ sqlite3 default.gnomint
    SQLite version 3.7.13 2012-06-11 02:05:22
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite>
    

Next list the available tables:

    sqlite> .tables
    ca_crl         ca_properties  certificates 
    ca_policies    cert_requests  db_properties
    

Lastly check out the **certificates** table:

    sqlite> select * from certificates;
    1|1|01|root-cert-elatov.local|1366488033|1555790433||-----BEGIN CERTIFICATE-----
    xxx
    -----END CERTIFICATE-----
    |1|-----BEGIN RSA PRIVATE KEY-----
    xxx
    -----END RSA PRIVATE KEY-----
    |C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=root-cert-elatov.local|C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=root-cert-elatov.local|0|:||39:3F:52:E5:F4:4F:F1:7F:48:73:A4:73:EB:F3:E0:C6:5A:4A:68:E8|39:3F:52:E5:F4:4F:F1:7F:48:73:A4:73:EB:F3:E0:C6:5A:4A:68:E8
    2|0|02|*.elatov.local|1366489069|1524255469||-----BEGIN CERTIFICATE-----
    yyy
    -----END CERTIFICATE-----
    |1|-----BEGIN RSA PRIVATE KEY-----
    yyy
    -----END RSA PRIVATE KEY-----
    |C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=*.elatov.local|C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=root-cert-elatov.local|1|:1:|||39:3F:52:E5:F4:4F:F1:7F:48:73:A4:73:EB:F3:E0:C6:5A:4A:68:E8
    

That looks good to me.

## Export the Signed Certificate in PKCS #12 Format from Gnomint

Now we need upload our signed Certificate to our IIS server to make sure it works okay. First, let go ahead and export the certificate from Gnomint. This is done by right clicking on our Cerficate and selecting &#8220;Export&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_cert.png" alt="gnomint export cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="710" height="378" class="alignnone size-full wp-image-8460" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After that, you will be presented to choose the format of the certificate. Choose &#8220;Both Parts&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_format.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_format.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_format.png" alt="gnomint export format Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="452" height="438" class="alignnone size-full wp-image-8461" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After clicking &#8220;Next&#8221;, you can choose to save the exported file on your computer. I called the file **wild-elatov-local.pfx** and stored it on my Desktop:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-export_save_diag.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-export_save_diag.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-export_save_diag.png" alt="gnomint export save diag Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="818" height="467" class="alignnone size-full wp-image-8462" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After clicking &#8220;Save&#8221;, you will be asked to password protect the file:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-pass_pro_pfx_file.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-pass_pro_pfx_file.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint-pass_pro_pfx_file.png" alt="gnomint pass pro pfx file Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="515" height="281" class="alignnone size-full wp-image-8463" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Click &#8220;OK&#8221; and you will now have the exported certificate in PKCS #12 format.

### Confirm the Contents of a PKCS #12 Format Certificate

We can just use the **openssl** utility to quickly check out the contents of the certificate:

    [elatov@klaptop Desktop]$ openssl pkcs12 -info -in wild-elatov-local.pfx 
    Enter Import Password:
    MAC Iteration 1
    MAC verified OK
    PKCS7 Encrypted data: pbeWithSHA1And40BitRC2-CBC, Iteration 425
    Certificate bag
    Bag Attributes
        localKeyID: 61 0B C1 4D 47 04 88 1F B9 1D 28 4D 99 18 CC 3C E0 75 2E 94 
        friendlyName: C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=*.elatov.local
    subject=/C=US/ST=Colorado/L=Boulder/O=Home/OU=Me/CN=*.elatov.local
    issuer=/C=US/ST=Colorado/L=Boulder/O=Home/OU=Me/CN=root-cert-elatov.local
    -----BEGIN CERTIFICATE-----
    xxx
    -----END CERTIFICATE-----
    PKCS7 Data
    Shrouded Keybag: pbeWithSHA1And3-KeyTripleDES-CBC, Iteration 299
    Bag Attributes
        localKeyID: 61 0B C1 4D 47 04 88 1F B9 1D 28 4D 99 18 CC 3C E0 75 2E 94 
        friendlyName: C=US,ST=Colorado,L=Boulder,O=Home,OU=Me,CN=*.elatov.local
    Key Attributes: <no Attributes>
    Enter PEM pass phrase:
    Verifying - Enter PEM pass phrase:
    -----BEGIN ENCRYPTED PRIVATE KEY-----
    xxx
    -----END ENCRYPTED PRIVATE KEY-----
    

The Export password and the PEM password are the same one that we used during the &#8220;Export&#8221; process from Gnomint. The above looks good: the **Issuer** is correct and so is the **subject**.

### Import the PKCS #12 Certificate into the IIS Server

Upload the **.pfx** file to the IIS server:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/cert-uploaded-to-win.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/cert-uploaded-to-win.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/cert-uploaded-to-win.png" alt="cert uploaded to win Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="78" height="86" class="alignnone size-full wp-image-8464" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then start up IIS manager:

    inetmgr
    

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmgr_started_iis2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmgr_started_iis2.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmgr_started_iis2.png" alt="inetmgr started iis2 Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="762" height="529" class="alignnone size-full wp-image-8465" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then click on &#8220;Server Certificates&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_inetmgr.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_inetmgr.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_inetmgr.png" alt="server certs inetmgr Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="858" height="599" class="alignnone size-full wp-image-8466" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After you double click on &#8220;Server Certificate&#8221; you will see a list of current certificates, I only have the self signed certificate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_1-self-signed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_1-self-signed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/server_certs_1-self-signed.png" alt="server certs 1 self signed Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="858" height="596" class="alignnone size-full wp-image-8524" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Now click on &#8220;Import&#8221; from the top left and the Import Certificate Dialogue will show up. Hit &#8220;Browse&#8221; and point to our certificate and enter the Export password:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/import_pfx_iis.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/import_pfx_iis.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/import_pfx_iis.png" alt="import pfx iis Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="305" height="217" class="alignnone size-full wp-image-8468" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After you click &#8220;OK&#8221; you will see the newly import Certificate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmer-new-cert-imported.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmer-new-cert-imported.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/inetmer-new-cert-imported.png" alt="inetmer new cert imported Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="913" height="599" class="alignnone size-full wp-image-8528" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Now if you click on &#8220;Default Web Site&#8221; you can click on &#8220;Bindings&#8221; from the left pane:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/def_site_selected.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/def_site_selected.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/def_site_selected.png" alt="def site selected Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="856" height="598" class="alignnone size-full wp-image-8470" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then select the &#8220;https&#8221; binding:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/https_binding_iis.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/https_binding_iis.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/https_binding_iis.png" alt="https binding iis Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="481" height="220" class="alignnone size-full wp-image-8471" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Lastly select &#8220;Edit&#8221; and select the newly imported SSL certificate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/https_change_binding.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/https_change_binding.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/https_change_binding.png" alt="https change binding Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="401" height="213" class="alignnone size-full wp-image-8530" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

To test out the new Certificate, open up the browser to the same site and you will still see the same &#8220;ssl&#8221; warning, but if you click on &#8220;View Certificate&#8221; you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/ie_cert_props.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/ie_cert_props.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/ie_cert_props.png" alt="ie cert props Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="403" height="508" class="alignnone size-full wp-image-8472" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

We can see that the &#8220;Issue By&#8221; and the &#8220;Issue To&#8221; fields look correct.

## Add Your Own Root CA to Trusted Root Certification Authorities on the DC Server

Now that we our own CA we need to import it to our Domain Controller and push it to any machine that is part of our domain. This way any computer part of the Domain will trust our SSL certificates. First we need to export our Root CA from Gnomint.

### Export Root CA Certificate from Gnomint

To export the Root CA Certificate we just have to do the same thing as with the regular Certificate. Right click on the Certificate and select &#8220;Export&#8221;. During the Export process choose &#8220;Public Only&#8221; for the format:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_public_only.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_public_only.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gnomint_export_public_only.png" alt="gnomint export public only Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="452" height="438" class="alignnone size-full wp-image-8475" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

If all is well you should see a succesful export:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/successful_export.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/successful_export.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/successful_export.png" alt="successful export Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="292" height="152" class="alignnone size-full wp-image-8476" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

### Confirm Contents of the Root CA .PEM File

We will again use **openssl** to check the contents of SSL certificate:

    [elatov@klaptop Desktop]$ openssl x509 -in root-ca-elatov-local.pem -text -noout 
    Certificate:
        Data:
            Version: 3 (0x2)
            Serial Number: 1 (0x1)
        Signature Algorithm: sha1WithRSAEncryption
            Issuer: C=US, ST=Colorado, L=Boulder, O=Home, OU=Me, CN=root-cert-elatov.local
            Validity
                Not Before: Apr 20 20:00:33 2013 GMT
                Not After : Apr 20 20:00:33 2019 GMT
            Subject: C=US, ST=Colorado, L=Boulder, O=Home, OU=Me, CN=root-cert-elatov.local
            Subject Public Key Info:
                Public Key Algorithm: rsaEncryption
                    Public-Key: (2048 bit)
                    Modulus:
                        00:d0:2f:05:bd:2a:4c:f0:3c:23:e7:00:b9:67:d9:
                    Exponent: 65537 (0x10001)
            X509v3 extensions:
                X509v3 Basic Constraints: critical
                    CA:TRUE
                X509v3 Key Usage: critical
                    Certificate Sign, CRL Sign
                X509v3 Subject Key Identifier: 
                    39:3F:52:E5:F4:4F:F1:7F:48:73:A4:73:EB:F3:E0:C6:5A:4A:68:E8
                X509v3 Authority Key Identifier: 
                    keyid:39:3F:52:E5:F4:4F:F1:7F:48:73:A4:73:EB:F3:E0:C6:5A:4A:68:E8
    
        Signature Algorithm: sha1WithRSAEncryption
             42:d1:be:db:42:ab:50:25:d2:bd:47:fc:05:f5:01:81:75:27:
    

All of the above looks good to me.

### Import the Root CA into the Windows DC Server

Upload the Root CA Certificate to the DC Server and then launch the &#8220;Group Policy Management&#8221; console:

    gpmc.msc
    

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_started.png" alt="gpmc started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="758" height="528" class="alignnone size-full wp-image-8482" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Next let&#8217;s expand the following hierarchy: Forest -> Domains -> &#8220;elatov.local&#8221; -> &#8220;Group Policy Objects&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_GPOs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_GPOs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/gpmc_GPOs.png" alt="gpmc GPOs Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="761" height="530" class="alignnone size-full wp-image-8483" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Then right click on &#8220;Defaul Domain Policy&#8221; and select &#8220;Edit&#8221; and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/default_domain_policy_gpo_editor.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/default_domain_policy_gpo_editor.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/default_domain_policy_gpo_editor.png" alt="default domain policy gpo editor Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="794" height="566" class="alignnone size-full wp-image-8484" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Now let&#8217;s expand the hierarchy as follows: &#8220;Default Domain Policy&#8221; -> &#8220;Computer Configuration&#8221; -> &#8220;Policies&#8221; -> &#8220;Windows Settings&#8221; -> &#8220;Security Settings&#8221; -> &#8220;Public Key Policies&#8221; -> &#8220;Trusted Root Certification Authorities&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/trca_gpo.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/trca_gpo.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/trca_gpo.png" alt="trca gpo Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="794" height="567" class="alignnone size-full wp-image-8485" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Right click on &#8220;Trusted Root Certification Authorities&#8221; and select &#8220;Import&#8221;, then point to the Root CA:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/import_root-ca.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/import_root-ca.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/import_root-ca.png" alt="import root ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="495" height="444" class="alignnone size-full wp-image-8486" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

After clicking &#8220;Next&#8221; it will let you know that it will add the certificate into the &#8220;Trusted Root Certifications Authorities&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/place_root_ca_in-trca.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/place_root_ca_in-trca.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/place_root_ca_in-trca.png" alt="place root ca in trca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="495" height="442" class="alignnone size-full wp-image-8487" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Lastly click &#8220;Next&#8221; and then &#8220;Finish&#8221; and you will the following message:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/cert_import_successful.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/cert_import_successful.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/cert_import_successful.png" alt="cert import successful Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="218" height="139" class="alignnone size-full wp-image-8488" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

And in the end you will see your root CA imported:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/root-ca-in-trca.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/root-ca-in-trca.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/root-ca-in-trca.png" alt="root ca in trca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="913" height="565" class="alignnone size-full wp-image-8489" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Now you can close the GPO consoles.

### Get the new Group Policies to the Windows Clients

Now that we have added our Root CA Certificate to our Group Policy, we need to update the policy on the client. Open up a command prompt on the Windows 7 client and run:

    C:\Windows\system32>gpupdate /force
    Updating Policy...
    
    User Policy update has completed successfully.
    Computer Policy update has completed successfully.
    

Or you can log out and log back in as well.

### Confirm the Root CA Certificate is on the Domain Joined Windows Client

Now that we have synced the new Group Policies from our Domain controller, we should see our Root CA. On the windows client run:

    certmgr.msc
    

and the &#8220;Certificate Manager&#8221; will start up:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/certmgr_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/certmgr_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/certmgr_started.png" alt="certmgr started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="625" height="442" class="alignnone size-full wp-image-8490" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

If you expand &#8220;Trusted Root Certification Authorities&#8221; -> &#8220;Certificates&#8221;, you should your Root CA in there:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/root_cert_added_win_client.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/root_cert_added_win_client.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/root_cert_added_win_client.png" alt="root cert added win client Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="836" height="481" class="alignnone size-full wp-image-8491" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

Now going to the site: shows me the following page without any warnings:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/iis-https_no-error.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/iis-https_no-error.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/iis-https_no-error.png" alt="iis https no error Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="747" height="486" class="alignnone size-full wp-image-8492" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

And checking out the SSL certificate we see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/trusted_ssl-cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/04/trusted_ssl-cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/04/trusted_ssl-cert.png" alt="trusted ssl cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" width="403" height="509" class="alignnone size-full wp-image-8493" title="Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment" /></a>

It&#8217;s trusted and I feel so much safer.

<root> </root>

