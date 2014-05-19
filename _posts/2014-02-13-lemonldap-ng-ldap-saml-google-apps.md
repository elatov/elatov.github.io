---
title: LemonLDAP-NG With LDAP and SAML Google Apps
author: Karim Elatov
layout: post
permalink: /2014/02/lemonldap-ng-ldap-saml-google-apps/
sharing_disabled:
  - 1
dsq_thread_id:
  - 2261261949
categories:
  - Home Lab
  - OS
tags:
  - 389-Directory-Server
  - LemonLDAP-NG
  - SAML
---
I wanted to try out a WebSSO program and I ran into [Known supported applications](http://lemonldap-ng.org/)

## Install LemonLDAP::NG on CentOS

I had a VPS running CentOS which was perfect for the setup. Most of the install instructions for *lemonldap-ng* are laid out [here](http://lemonldap-ng.org/documentation/1.3/installrpm).

### Install the packages

There is a **YUM** repository available which holds all the *lemonldap-ng* packages. To set that up, add the following into the **/etc/yum.repos.d/lemonldap-ng.repo** file:

    elatov@ccl:~$cat /etc/yum.repos.d/lemonldap-ng.repo
    [lemonldap-ng]
    name=LemonLDAP::NG packages
    baseurl=http://lemonldap-ng.org/rpm6/
    enabled=1
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OW2


I also enabled the [rpmforge](https://fedoraproject.org/wiki/EPEL) repository to get a lot of other packages that are not available in the default CentOS repo. To enable the **epel** repository I ran the following:

    wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo yum localinstall epel-release-6-8.noarch.rpm


and here is what I did to install the **rpmforge** repo:

    wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
    sudo yum localinstall rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm


After enabling all the repositories, I updated my **yum** configuration:

    sudo yum update


I then imported the *lemonldap-ng* **GPG** key:

    wget http://lemonldap-ng.org/_media/rpm-gpg-key-ow2
    sudo rpm --import rpm-gpg-key-ow2


After that was done, I then installed the packages:

    sudo yum install lemonldap-ng --disablerepo=rpmforge


### Install liblasso

Unfortunately the [liblasso](http://lasso.entrouvert.org/) package was not included in any of the above repositories, so I compiled it from source. First let's get the source:

    wget https://dev.entrouvert.org/lasso/lasso-2.3.6.tar.gz --no-check-certificate


Now let's install some of the prerequisites. Here were the ones I was missing:

    sudo yum install glib2-devel libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel


Now let's extract the source and configure the package:

    tar xvzf lasso-2.3.6.tar.gz
    cd lasso-2.3.6
    ./configure


To compile the software, run the following:

    make


and then finally run the following to install it:

    sudo make install


For some reason the [ld-run-path](https://blogs.oracle.com/ali/entry/avoiding_ld_library_path_the) wasn't setting appropriately, and upon loading the **Lasso** perl module it would fail with the following message:

    elatov@ccl:~$perl -MLasso
    Can't load '/usr/local/lib64/perl5/auto/Lasso/Lasso.so' for module Lasso:
    liblasso.so.3: cannot open shared object file:
    No such file or directory at /usr/lib64/perl5/XSLoader.pm line 70.


The file existed under /usr/local/lib:

    elatov@ccl:~$locate liblasso.so.3
    /usr/local/lib/liblasso.so.3
    /usr/local/lib/liblasso.so.3.9.4


So I added that directory to the **ldconfig** configuration, to load it automatically. This is done by creating the **/etc/ld.so.conf.d/lasso.conf** file with the following contents:

    elatov@ccl:~$cat /etc/ld.so.conf.d/lasso.conf
    /usr/local/lib


then running **ldconfig** to apply the settings:

    elatov@ccl:~$sudo ldconfig -v | grep lasso
    liblasso.so.3 -> liblasso.so.3.9.4


After that, I was able to import the Lasso module without issues. BTW *liblasso* is only necessary if you are planning to use the SAML Capabilities within *lemoldap-ng*.

## Configure LemonLDAP::NG

There are a couple of configuration steps to setup *lemonldap-ng*.

### DNS Preparation

There will be 3 hostnames for my configuration. If you are planning to use the reverse proxy functionality you will need more.

First we need to have a DNS name for the manager (management portal) of *lemonldap-ng*. This is where all the configurations changes occur, sometimes referred to as the **administration portal**. I ended up using: **man.dnsd.me**.

Second we need a DNS Name for the application portal, this is where regular users go to access SSO enabled applications, this is sometimes referred to as the **authentication portal**. I ended using **port.dnsd.me**.

Lastly to be able to update configuration from the administration portal, we will need **reload.dnsd.me**. After that is in place we can start configuring *lemonldap-ng*. You can setup each of the components on different servers as shown [here](http://wiki.lemonldap.ow2.org/xwiki/bin/view/NG/Presentation#HArchitecture):

![lemonldap arch LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemonldap-arch.png)

I actually ended up using the same server for all the components of the setup.

### Modify LemonLDAP::NG Configuration Files

Now let's fix the hostnames in the configuration files. Here is what I ran to fix all the setting files:

    sed -i 's/auth\.example\.com/port.dnsd.me/g' /var/lib/lemonldap-ng/conf/lmConf-1 /etc/lemonldap-ng/* /var/lib/lemonldap-ng/test/index.pl
    sed -i 's/manager\.example\.com/man.dnsd.me/g' /var/lib/lemonldap-ng/conf/lmConf-1 /etc/lemonldap-ng/* /var/lib/lemonldap-ng/test/index.pl
    sed -i 's/reload\.example\.com/reload.dnsd.me/g' /var/lib/lemonldap-ng/conf/lmConf-1 /etc/lemonldap-ng/* /var/lib/lemonldap-ng/test/index.pl


Now let's make sure the **apache** rules are good:

    elatov@ccl:~$sudo apachectl configtest
    Syntax OK


Then enable **apache** on boot up and start the service:

    sudo chkconfig httpd on
    sudo service httpd start


Don't forget to open up the firewall for port 80, add the following into the **/etc/sysconfig/iptables** file:

    -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT


To apply the rules, run the following:

    sudo service iptables restart


Lastly add the **reload** name in your **/etc/hosts** file to allow config updates:

    echo "127.0.0.1 reload.dnsd.me" >> /etc/hosts


At this point you can visit the administration console (**http://man.dnsd.me**) and it will redirect you to the authentication portal:

![lemonldap ng auth portal LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemonldap-ng-auth-portal.png)

By default you can login with:

> username: dwho
> password: dwho

After you login, you should see the administration console:

![lemonldp admin console LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemonldp-admin-console.png)

If you visit the authentication portal (**port.dnsd.me**) and login with the same credentials, it will log you to the regular portal:

![lemonldap auth portal LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemonldap-auth-portal.png)

## Install and Configure an LDAP Server for LemonLDAP::NG Authentication

I didn't want to leave the demo account enabled (**dwho**), so I decided to use LDAP for authentication.

### Install 389 Directory Server

The install is pretty simple, here are the steps I took:

    sudo yum install 389-ds openldap-clients
    sudo setup-ds-admin.pl


The setup script has a couple of options. For a step by step guide for the *Directory Server* check out this [this](http://ostechnix.wordpress.com/2013/02/05/setup-ldap-server-389ds-in-centosrhelscientific-linux-6-3-step-by-step/) one.

After the install is finished we can now create users.

### Use the 389 Admin Console to Create a User

You can't access the admin console remotely, so we can use **X-Forwarding** to launch the application from the server it self. To enable SSH X-Forwarding, first make sure you have the following defined in your **/etc/ssh/sshd_config** file:

    AddressFamily inet
    X11Forwarding yes
    X11UseLocalhost yes


and then install **xauth**:

    sudo yum install xauth


and lastly restart the **sshd** service to apply all the settings:

    sudo service sshd restart


Now for your local machine (Linux or Mac) run the following to launch the 389 Admin Console:

    ssh -X elatov@ccl.dnsd.me
    389-console


After entering all the credentials, you should see the following:

![389 console login cres LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/389-console-login-cres.png)

Upon a successful login, you will see the following:

![389 console logged in LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/389-console-logged-in.png)

Then click on the **User and Groups** tab and then click **Create** -> **User**:

![add user 389 console LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/add-user-389-console.png)

After you create the user it should look like this:

![389 console user LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/389-console-user.png)

Notice the email address is **test@moxz.mine.nu**, this actually corresponds to the email address in my Google Apps account (this will come into play when using SAML to login into Google Apps).

### Confirm LDAP User

I did an LDAP query against LDAP, binding to LDAP with the **Directory Manager** Account, and I saw the following:

    elatov@ccl:~$ldapsearch -h localhost -b "dc=dnsd,dc=me" -D "cn=Directory Manager" -W "uid=elatov" -LLL
    Enter LDAP Password:
    dn: uid=elatov,ou=People,dc=dnsd,dc=me
    mail: test@moxz.mine.nu
    uid: elatov
    givenName: K
    objectClass: top
    objectClass: person
    objectClass: organizationalPerson
    objectClass: inetorgperson
    sn: E
    cn: K E
    userPassword:: e1NTSEF9a


That looks good, I could actually bind with test user and do a query against him self as well:

    elatov@ccl:~$ldapsearch -h localhost -b "dc=dnsd,dc=me" -D "uid=elatov,ou=People,dc=dnsd,dc=me" -W "uid=elatov" -LLL
    Enter LDAP Password:
    dn: uid=elatov,ou=People,dc=dnsd,dc=me
    mail: test@moxz.mine.nu
    uid: elatov
    givenName: K
    objectClass: top
    objectClass: person
    objectClass: organizationalPerson
    objectClass: inetorgperson
    sn: E
    cn: K E


Notice this time around the password field is not shown, but obviously I had to type the user's password to perform the bind operation.

### Configure LemonLDAP::NG to Use LDAP For Authentication

Login to the administrative portal and go to **General Parameters** -> **Authentication modules** and set the following:

*   Authentication Module
*   Users Module
*   Password Module

All to be **LDAP**:

![ldap enabled LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/ldap-enabled.png)

Then go to **General Parameters** -> **Authentication Modules** -> **LDAP parameters** -> **Connection** and set the following settings:

*   Server host => **localhost**
*   Server port => **389**
*   Users search base => **ou=People,dc=dnsd,dc=me**
*   Account => **cn=Directory Manager**
*   Password => *The directory Manager Password*

### Allow Access to LemonLDAP:NG Manager to Other Users

As you saw I created a user called **elatov** in LDAP. Also as mentioned, by default the **dwho** user is configured to access the manager console. Let's change that to be the user **elatov**. To configure this go to **Virtual Hosts** -> **man.dnsd.me** -> **Rules**. And change the **default** rule to be `$uid eq "elatov"`:

![lemon ldap change access to man LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemon-ldap-change-access-to-man.png)

Now you can configure *lemonldap-ng* with the **elatov** user.

## SAML with LemonLDAP::NG

Now let's setup *lemonldap-ng* to be a SAML **IDP** (Identity Provider) connecting to the Google Apps **SP** (Service Provider).

### Configure LemonLDAP::NG to be a SAML IDP (Identity Provider)

First let's enable **SAML**. From the managamentment console (**man.dnsd.me**), go to **General Settings** -> **Issuer Module** -> **SAML** -> **Activation** -> **On**:

![enable saml lemonldap LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/enable-saml-lemonldap.png)

Then ensure the **Email NameID Format** is configured to send the **mail** attribute from LDAP. This is done going to **SAML 2 Service** -> **NameID Format** -> **Email** -> **mail**:

![lemonldap mail email format LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemonldap-mail-email-format.png)

Then generate a private SSL key which will be used for the signature of the SAML Assertions. Go to **SAML2 Service** -> **Security parameters** -> **Signature** -> **Private key** -> **Generate**:

![private key generat lemon ldap LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/private-key-generat-lemon-ldap.png)

After it's generated, go ahead and **download** it and save it as **lemondap-priv-key.pem** (we will use this later to generate the public certificate to upload to Google Apps).

For completion, fill out your *Organization* information under **SAML2 Service** -> **Organization** -> **Display Name / Name / URL**:

![lemon ldap org name 1024x365 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/lemon-ldap-org-name-1024x365.png)

### Add Google Apps Service Provider in LemonLDAP::NG

First create a new **Service Provider**, this is done by going to **SAML service provider** -> **New service provider**.

After it's created add Google Apps SAML Metadata. **SAML service provider** -> **gapps** -> **Metadata** and add the following into it:

    <md:EntityDescriptor entityID="google.com" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata">
      <SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://www.google.com/a/moxz.mine.nu/acs" index="1" />
        <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</NameIDFormat>
      </SPSSODescriptor>
    </md:EntityDescriptor>


** Make sure you set the **Location** to your google domain.

![saml metadata for gapps 1024x272 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/saml-metadata-for-gapps-1024x272.png)

Now let's configure to use the **Email** Format for the **NameID** attribute. **SAML service provider** -> **gapps** > **Options** -> **Authentication response** -> **Default NameID format** -> **Email**:

![nameid format lemonldap gapps 1024x373 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/nameid-format-lemonldap-gapps-1024x373.png)

Lastly let's disable the advanced features in *lemonldap-ng*. This is done by going to **SAML service provider** -> **gapps** -> **Options** -> **Signature**. Then disable everything except "**Sign SSO message**":

![sign sso assertion LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/sign-sso-assertion.png)

### Enable SAML SSO in Google Apps

First let's generate the signing certificate. Run the following two commands:

    openssl req -new -key lemondap-priv-key.pem -out lemonldap.csr
    openssl x509 -req -days 3650 -in lemonldap.csr -signkey lemondap-priv-key.pem -out lemonldap.pem


Then login to the Google Apps Domain Admin Console: **google.com/a/moxz.mine.nu** (use your domain as necessary). After you login, go to **Security** -> **Advanced** -> **Set up single sign-on (SSO)**:

![gapps sso settings 1024x266 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/gapps-sso-settings-1024x266.png)

Configure the following settings:

*   Sign-in page URL => **http://port.dnsd.me/saml/singleSignOn**
*   Sign-out page URL => **http://port.dnsd.me/?logout=1**
*   Change password URL => **http://port.dnsd.me**
*   Verification certificate => *upload generated certificate (lemonldap.pem)*

Here is how my configuration looked like:

![gapps sso settings LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/gapps_sso-settings.png)

### Create An Application in LemonLDAP::NG for Google Apps

Since Google Apps uses an SP-Initiated SAML flow, we can just go to Google Apps and it will forward us to *lemonldap-ng* to get authenticated. If you wanted to start out at the *lemonldap-ng* portal, you could fake an IDP initiated flow like this. Go to **General Parameters** -> **Portal** -> **Menu** -> **Categories and applications** -> **1sample** -> **test1** and enter the following:

*   Key => **test1**
*   Display name => **Google Apps**
*   Address => **https://mail.google.com/a/moxz.mine.nu?hl=en**
*   Description => **Google Apps**

![gapps application lemonldap ng LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/gapps-application-lemonldap-ng.png)

### Test out the application

Go to the authentication portal (**port.dnsd.me**) and login as a user which has the same email address as the one set in google apps. After logging in, should see the Google Apps application:

![user loggedin lemonldap 1024x214 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/user-loggedin-lemonldap-1024x214.png)

I logged in with user **elatov** (from above I set his email to be **test@moxz.mine.nu** in LDAP... I of course had a user in Google Apps with that same email set). Then clicking on the **Google Apps** application logged me into Google Apps:

![logged into gmail from lemonldap 1024x134 LemonLDAP NG With LDAP and SAML Google Apps](http://virtuallyhyper.com/wp-content/uploads/2014/01/logged-into-gmail-from-lemonldap-1024x134.png)

