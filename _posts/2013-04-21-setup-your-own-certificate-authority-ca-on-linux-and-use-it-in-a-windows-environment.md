---
title: Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment
author: Karim Elatov
layout: post
permalink: /2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/
dsq_thread_id:
  - 1404673780
categories: ['home_lab', 'os']
tags: ['linux','win2k8r2','ssl', 'gnomint', 'windows_group_policies']
---

In [this](/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/) previous post, I deployed a test IIS Server and used a self signed SSL Certificate to encrypt the HTTP traffic. I am sure everyone have seen this page in Internet Explorer:

![IE cert error Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/IE_cert_error.png)

When I clicked "View Certificate", I saw the following:

![view certificate Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/view_certificate.png)

We can see that certificate is issued by the same entity as the site-name itself. We can also see that the Root CA is not trusted. Since this is a self-signed Certificate, you are the Root CA in a manner of speaking. My goal is to get rid of that message and to become a "trusted" Certificate Authority (CA) in my local Windows Environment.

## Choosing a free Certificate Authority software

If we take a look at this [wikipedia](http://en.wikipedia.org/wiki/Certificate_authority#Open_source_implementations) page, we will see the following list of available software:

> *   [DogTag](http://pki.fedoraproject.org/wiki/PKI_Main_Page)
> *   [EJBCA](http://www.ejbca.org/)
> *   [gnoMint](http://gnomint.sourceforge.net/)
> *   [OpenCA](https://pki.openca.org/)
> *   [OpenSSL](http://www.openssl.org/), which is really an SSL/TLS library, but comes with tools allowing its use as a simple certificate authority.
> *   [r509](https://github.com/reaperhulk/r509)
> *   [XCA](http://xca.sourceforge.net/)

There is actually one more that I ran into, it's called [tinyCA](http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/).

### Using OpenSSL Commands to Setup a CA

*DogTag*, *EJBCA*, and *OpenCA* were full blown Public-Key Infrastructure (PKI) applications and I didn't need all of the extra functionally. There are a lot of examples on how to setup your own CA with **openssl**:

*   [Be your own Certificate Authority (CA)](http://www.g-loaded.eu/2005/11/10/be-your-own-ca/)
*   [Creating a Certificate Authority and signing the SSL certificates using openssl](http://www.ulduzsoft.com/2012/01/creating-a-certificate-authority-and-signing-the-ssl-certificates-using-openssl/)
*   [Be your own CA](http://archive09.linux.com/feature/38315)
*   [Becoming a X.509 Certificate Authority](http://www.davidpashley.com/articles/cert-authority.html)

I have done that before and when you are managing a lot of different certificates the process is not very scalable. Also, if you don't keep doing it, you have to re-trace your steps to remember how the setup works. There is also a **Perl** script that is included to ease the CA setup, that script is called **CA.pl**. Depending on your Linux distribution you have find the right package that contains that script. Here is where I found it on my Fedora install:

    [elatov@klaptop ~]$ yum provides "*/CA.pl*"
    Loaded plugins: langpacks, presto, refresh-packagekit, remove-with-leaves
    1:openssl-perl-1.0.1c-7.fc18.x86_64 : Perl scripts provided with OpenSSL
    Repo        : fedora
    Matched from:
    Filename    : /etc/pki/tls/misc/CA.pl
    Filename    : /usr/share/man/man1/CA.pl.1ssl.gz


You can check out examples from "[CA.pl - friendlier interface for OpenSSL certificate programs](https://www.openssl.org/docs/apps/CA.pl.html) on how to use the Perl script; here is a very high level overview:

    #Generate CA Certificate
    CA.pl -newca

    #Generate a Certificate Signing Request (CSR)
    CA.pl -newreq

    #Sign the CSR with your CA key
    CA.pl -sign


### TinyCA

This time around I wanted a pretty GUI that will handle all of the **openssl** commands for me and store the certificate database as well. Maybe I am getting lazy? or hopefully efficient. Among the other applications, TinyCA stood out the most. I found many guides on how to use it:

*   [Create your own Certificate Authority with TinyCA](http://www.ghacks.net/2009/09/16/create-your-own-certificate-authority-with-tinyca/)
*   [Create your own CA with TinyCA2 (part 1)](http://theworldofapenguin.blogspot.com/2007/06/create-your-own-ca-with-tinyca2-part-1.html)
*   [Create your own Certificate Authority with TinyCA2 and Debian Squeeze](http://adminadventure.wordpress.com/2012/07/10/create-your-own-certificate-authority-with-tinyca2-and-debian-squeeze/)

As I started to install the software I noticed that it wasn't part of the Fedora repositories:

    [elatov@klaptop ~]$ yum search tinyca
    Loaded plugins: langpacks, presto, refresh-packagekit, remove-with-leaves
    Warning: No matches found for: tinyca
    No Matches found


That didn't stop me; I downloaded the application and installed it manually. After setting up my Root CA, the application crashed with the following error:

    Use of uninitialized value $mday in concatenation (.) or string at /usr/share/perl5/Time/Local.pm line 116, <gen11> line 3.
    Day '' out of range 1..31 at /usr/local/tinyca2/lib/OpenSSL.pm line 1050.


I found [this](http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=702233) bug and the issue was with a later version of **openssl** (which I had on my Fedora 18 install). The fix was included in Debian based distributions. However I was running Fedora and I didn't want to keep patching the software manually, if it kept having issues. So I decided to try out **gnomint**.

## Install Gnomint and Create a Root CA Certificate

Luckily *Gnomint* was part of the Fedora packages, so a simple:

    yum install gnomint


Took care of all my troubles. Then running **gnomint** launched the GUI for me:

![gnomint started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_started.png)

Then I clicked on "Add Autosigned CA certificate" and it showed me the "New CA" dialog:

![gnomint new ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_new_ca.png)

Here is what I entered for my new CA certificate:

![gnomint new ca filledout Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_new_ca_filledout.png)

Then if you click "Next" you will see the "New CA Properties" window:

![gnomint new ca props Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_new_ca_props.png)

Choose what you think is necessary; the higher the bit count the better the encryption is. Click "Next" and you will be asked to provide the "CRL Distribution Point". This is included with the Root CA Certificate. If a certificate is revoked, people can check for that at this "Destribution Point"/Link. I won't be a public CA, so I left this blank:

![gnomint crl dist point Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_crl_dist_point.png)

I then clicked "OK" and my new Root CA Certificate was created:

![gnomint root ca created Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_root_ca_created.png)

## Generate a new Certificate Request and Sign it with your Root CA Certificate in Gnomint

At this point we can generate a Certificate Signing Request (CSR) by clicking on "Add CSR":

![gnomint csr req Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_csr_req.png)

After "Inheriting CA Fields" we can click "Next" and fill out the Request:

![gnomint req props filled out Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_req_props_filled_out.png)

I went ahead and requested for a "wildcard" (*.domain.com) certificate just to have one certificate cover my test windows domain. This way I can import one Certificate on both of my IIS servers. Clicking "Next" will take us to the Encryption details, I left the defaults here (I know with Windows as long as it's above 2048 bits then it should work):

![gnomint csr req enc Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_csr_req_enc.png)

Clicking "OK" created the CSR:

![gnomint csr created Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_csr_created.png)

To "Sign" the CSR, just right click on it and select "Sign":

![gnomint sign csr Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_sign_csr.png)

and the following window will show up:

![gnomint sign csr diag Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_sign_csr_diag.png)

Click "Next" and it will ask you to choose the CA to sign with:

![gnomint sign csr choose ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_sign_csr_choose_ca.png)

After clicking "Next" we choose how long the certificate is valid for and what it can be used for:

![gnomint sign csr uses Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_sign_csr_uses.png)

The defaults were fine with me, clicking "OK" finished the process and I now had a signed certificate:

![gnomint signed cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_signed_cert.png)

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

Now we need upload our signed Certificate to our IIS server to make sure it works okay. First, let go ahead and export the certificate from Gnomint. This is done by right clicking on our Cerficate and selecting "Export":

![gnomint export cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_export_cert.png)

After that, you will be presented to choose the format of the certificate. Choose "Both Parts":

![gnomint export format Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_export_format.png)

After clicking "Next", you can choose to save the exported file on your computer. I called the file **wild-elatov-local.pfx** and stored it on my Desktop:

![gnomint export save diag Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint-export_save_diag.png)

After clicking "Save", you will be asked to password protect the file:

![gnomint pass pro pfx file Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint-pass_pro_pfx_file.png)

Click "OK" and you will now have the exported certificate in PKCS #12 format.

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


The Export password and the PEM password are the same one that we used during the "Export" process from Gnomint. The above looks good: the **Issuer** is correct and so is the **subject**.

### Import the PKCS #12 Certificate into the IIS Server

Upload the **.pfx** file to the IIS server:

![cert uploaded to win Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/cert-uploaded-to-win.png)

Then start up IIS manager:

    inetmgr


![inetmgr started iis2 Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/inetmgr_started_iis2.png)

Then click on "Server Certificates":

![server certs inetmgr Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/server_certs_inetmgr.png)

After you double click on "Server Certificate" you will see a list of current certificates, I only have the self signed certificate:

![server certs 1 self signed Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/server_certs_1-self-signed.png)

Now click on "Import" from the top left and the Import Certificate Dialogue will show up. Hit "Browse" and point to our certificate and enter the Export password:

![import pfx iis Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/import_pfx_iis.png)

After you click "OK" you will see the newly import Certificate:

![inetmer new cert imported Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/inetmer-new-cert-imported.png)

Now if you click on "Default Web Site" you can click on "Bindings" from the left pane:

![def site selected Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/def_site_selected.png)

Then select the "https" binding:

![https binding iis Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/https_binding_iis.png)

Lastly select "Edit" and select the newly imported SSL certificate:

![https change binding Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/https_change_binding.png)

To test out the new Certificate, open up the browser to the same site and you will still see the same "ssl" warning, but if you click on "View Certificate" you will see the following:

![ie cert props Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/ie_cert_props.png)

We can see that the "Issue By" and the "Issue To" fields look correct.

## Add Your Own Root CA to Trusted Root Certification Authorities on the DC Server

Now that we our own CA we need to import it to our Domain Controller and push it to any machine that is part of our domain. This way any computer part of the Domain will trust our SSL certificates. First we need to export our Root CA from Gnomint.

### Export Root CA Certificate from Gnomint

To export the Root CA Certificate we just have to do the same thing as with the regular Certificate. Right click on the Certificate and select "Export". During the Export process choose "Public Only" for the format:

![gnomint export public only Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gnomint_export_public_only.png)

If all is well you should see a succesful export:

![successful export Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/successful_export.png)

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

Upload the Root CA Certificate to the DC Server and then launch the "Group Policy Management" console:

    gpmc.msc


![gpmc started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gpmc_started.png)

Next let's expand the following hierarchy: Forest -> Domains -> "elatov.local" -> "Group Policy Objects":

![gpmc GPOs Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/gpmc_GPOs.png)

Then right click on "Defaul Domain Policy" and select "Edit" and you will see the following:

![default domain policy gpo editor Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/default_domain_policy_gpo_editor.png)

Now let's expand the hierarchy as follows: "Default Domain Policy" -> "Computer Configuration" -> "Policies" -> "Windows Settings" -> "Security Settings" -> "Public Key Policies" -> "Trusted Root Certification Authorities":

![trca gpo Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/trca_gpo.png)

Right click on "Trusted Root Certification Authorities" and select "Import", then point to the Root CA:

![import root ca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/import_root-ca.png)

After clicking "Next" it will let you know that it will add the certificate into the "Trusted Root Certifications Authorities":

![place root ca in trca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/place_root_ca_in-trca.png)

Lastly click "Next" and then "Finish" and you will the following message:

![cert import successful Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/cert_import_successful.png)

And in the end you will see your root CA imported:

![root ca in trca Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/root-ca-in-trca.png)

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


and the "Certificate Manager" will start up:

![certmgr started Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/certmgr_started.png)

If you expand "Trusted Root Certification Authorities" -> "Certificates", you should your Root CA in there:

![root cert added win client Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/root_cert_added_win_client.png)

Now going to the site: shows me the following page without any warnings:

![iis https no error Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/iis-https_no-error.png)

And checking out the SSL certificate we see the following:

![trusted ssl cert Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](https://github.com/elatov/uploads/raw/master/2013/04/trusted_ssl-cert.png)

It's trusted and I feel so much safer.

<root> </root>

