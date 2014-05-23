---
title: Enabling LDAPS on Windows 2008 Active Directory Server
author: Karim Elatov
layout: post
permalink: /2013/06/enabling-ldaps-on-windows-2008-active-directory-server/
dsq_thread_id:
  - 1405434219
categories:
  - Home Lab
  - OS
tags:
  - Active Directory
  - MozLDAP
  - OpenLDAP
---
I installed Active Directory by selecting the "Active Directory Domain Services" Role from the Server Manager Dialogue. Step by step instructions can be seen in [Deploying a Test Windows Environment in a KVM Infrastucture](http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/).

## Running an *ldapsearch* against a Windows AD Server

After you installed AD you can confirm that it's listening on port **389**:

    C:\Users\Administrator>netstat -abn | findstr :389
      TCP    0.0.0.0:389            0.0.0.0:0              LISTENING
      TCP    127.0.0.1:389          127.0.0.1:49160        ESTABLISHED
      TCP    127.0.0.1:49160        127.0.0.1:389          ESTABLISHED
      TCP    192.168.250.47:389     192.168.250.47:49175   ESTABLISHED
      TCP    192.168.250.47:49175   192.168.250.47:389     ESTABLISHED


We can see it's listening on port **389** and there are some local connections to that port for the AD server. Now let's go ahead and add a test LDAP user for our queries.

### Add New User to AD via the "Active Directory Users and Computers" Console

To start the "Active Directory Users and Computers" Console, execute the following command from the run dialogue:

    dsa.msc


At which point you will see the following window:

![dsa started Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/dsa_started.png)

Then right click in the white space and go to "New" -> "User":

![new user dsa g Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/new_user_dsa_g.png)

Then fill out the User information:

![new user filled out Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/new_user_filled_out.png)

Lastly set the user's password:

![set password Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/set_password.png)

After it's all said and done you will see the following in the "Active Directory Users and Computers" Console:

![user added dsa Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/user_added_dsa.png)

So our test user will be **elatov**.

### Use *ldp.exe* to browse the AD Server

From the run dialogue run:

    ldp.exe


and you will see the following:

![ldp exe started Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldp_exe_started.png)

Now let's *bind* to the AD server, since we are local to the AD server we can just bind with the same user that we are currently logged in:

![ldp exe bind button g Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldp_exe_bind_button_g.png)

and let's leave the defaults:

![bind dialogue Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/bind_dialogue.png)

After clicking OK, you will see the connection go through and the *bind* to the AD server succeed:

![ldp exe bound Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldp_exe_bound.png)

Now let's start browsing the AD server, first let's select the "Tree" view:

![ldp exe tree button g Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldp_exe_tree_button_g.png)

After that we need to choose the **BaseDN**, this is basically where we want to start the search. We will choose **dc=elatov,dc=local**, which is basically the root of the AD server.

![tree view base dn Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/tree_view_base_dn.png)

I just want to see all the available branches/children that are part of the AD server:

![children AD server Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/children_AD_server.png)

Expanding the **User** branch and locating our test user "elatov", we see the following:

![elatov user info ldp exe Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/elatov_user_info_ldp_exe.png)

We can see that the DN (Distinguished Name) of the test user is:

    CN=Karim Elatov,CN=Users,DC=elatov,DC=local


From now one since we know all the users are under "CN=Users,DC=elatov,DC=local" we will use that as our BaseDN, this way we don't have to query the whole AD structure.

### Use *dsquery* to find DNs of Users

There is a command line utility called **dsquery**, which shows a more succinct view. For example to find the DN of our user, we can run the follow command from the command prompt:

    C:\Users\Administrator>dsquery user -name "Karim Elatov"
    "CN=Karim Elatov,CN=Users,DC=elatov,DC=local"


If you want to find out all the available groups in an AD server, you can run the following:

    C:\Users\Administrator>dsquery group DC=elatov,DC=local
    "CN=Administrators,CN=Builtin,DC=elatov,DC=local"
    "CN=Users,CN=Builtin,DC=elatov,DC=local"
    "CN=Guests,CN=Builtin,DC=elatov,DC=local"
    "CN=Print Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Backup Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Replicator,CN=Builtin,DC=elatov,DC=local"
    "CN=Remote Desktop Users,CN=Builtin,DC=elatov,DC=local"
    "CN=Network Configuration Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Performance Monitor Users,CN=Builtin,DC=elatov,DC=local"
    "CN=Performance Log Users,CN=Builtin,DC=elatov,DC=local"
    "CN=Distributed COM Users,CN=Builtin,DC=elatov,DC=local"
    "CN=IIS_IUSRS,CN=Builtin,DC=elatov,DC=local"
    "CN=Cryptographic Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Event Log Readers,CN=Builtin,DC=elatov,DC=local"
    "CN=Certificate Service DCOM Access,CN=Builtin,DC=elatov,DC=local"
    "CN=Domain Computers,CN=Users,DC=elatov,DC=local"
    "CN=Domain Controllers,CN=Users,DC=elatov,DC=local"
    "CN=Schema Admins,CN=Users,DC=elatov,DC=local"
    "CN=Enterprise Admins,CN=Users,DC=elatov,DC=local"
    "CN=Cert Publishers,CN=Users,DC=elatov,DC=local"
    "CN=Domain Admins,CN=Users,DC=elatov,DC=local"
    "CN=Domain Users,CN=Users,DC=elatov,DC=local"
    "CN=Domain Guests,CN=Users,DC=elatov,DC=local"
    "CN=Group Policy Creator Owners,CN=Users,DC=elatov,DC=local"
    "CN=RAS and IAS Servers,CN=Users,DC=elatov,DC=local"
    "CN=Server Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Account Operators,CN=Builtin,DC=elatov,DC=local"
    "CN=Pre-Windows 2000 Compatible Access,CN=Builtin,DC=elatov,DC=local"
    "CN=Incoming Forest Trust Builders,CN=Builtin,DC=elatov,DC=local"
    "CN=Windows Authorization Access Group,CN=Builtin,DC=elatov,DC=local"
    "CN=Terminal Server License Servers,CN=Builtin,DC=elatov,DC=local"
    "CN=Allowed RODC Password Replication Group,CN=Users,DC=elatov,DC=local"
    "CN=Denied RODC Password Replication Group,CN=Users,DC=elatov,DC=local"
    "CN=Read-only Domain Controllers,CN=Users,DC=elatov,DC=local"
    "CN=Enterprise Read-only Domain Controllers,CN=Users,DC=elatov,DC=local"
    "CN=DnsAdmins,CN=Users,DC=elatov,DC=local"
    "CN=DnsUpdateProxy,CN=Users,DC=elatov,DC=local"


### Use *openldap* Tools to perform an LDAP Query

There are a couple of versions of LDAP clients for Linux:

*   [Mozilla LDAP Tools](http://www-archive.mozilla.org/directory/tools/ldaptools.html).
*   [OpenLDAP Client Tools](http://www.openldap.org/)
*   [PowerBroker Open](http://www.powerbrokeropen.org/) (formely known as LikeWise Open)

Usually the location of the binary will let you know which one you have. For example here are two binaries on the same system:

    # where ldapsearch
    /usr/bin/ldapsearch
    /usr/lib/mozldap/ldapsearch


RedHat mostly uses the Mozilla version. From "[LDAP Tool Locations](http://www.centos.org/docs/5/html/CDS/ag/8.0/Common_Usage-ldap-tools.html)":

> For all Red Hat Directory Server guides and documentation, the LDAP tools used in the examples, such as **ldapsearch** and **ldapmodify**, are the Mozilla LDAP tools. For most Linux systems, OpenLDAP tools are already installed in the **/usr/bin/** directory.

The two different versions have different arguments so make sure you know which one you are using. Let's perform an LDAP query with **openldap** tools first:

    # ldapsearch -h 192.168.250.47 -b "CN=Users,DC=elatov,DC=local" -s sub -D "administrator@elatov.local" -W "sAMAccountName=elatov"
    Enter LDAP Password:
    # extended LDIF
    #
    # LDAPv3
    # base cn =Users,DC=elatov,DC=local> with scope subtree
    # filter: sAMAccountName=elatov
    # requesting: ALL
    #

    # Karim Elatov, Users, elatov.local
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    objectClass: top
    objectClass: person
    objectClass: organizationalPerson
    objectClass: user
    cn: Karim Elatov
    sn: Elatov
    givenName: Karim
    distinguishedName: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    instanceType: 4
    whenCreated: 20130511230624.0Z
    whenChanged: 20130511230624.0Z
    displayName: Karim Elatov
    uSNCreated: 94257
    uSNChanged: 94262
    name: Karim Elatov
    objectGUID:: w1P90HpQKU2DUtBdEHJ98w==
    userAccountControl: 66048
    badPwdCount: 0
    codePage: 0
    countryCode: 0
    badPasswordTime: 0
    lastLogoff: 0
    lastLogon: 0
    pwdLastSet: 130127871842187500
    primaryGroupID: 513
    objectSid:: AQUAAAAAAAUVAAAA0uO84TKspJERrqPGUgQAAA==
    accountExpires: 9223372036854775807
    logonCount: 0
    sAMAccountName: elatov
    sAMAccountType: 805306368
    userPrincipalName: elatov@elatov.local
    objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=elatov,DC=local
    dSCorePropagationData: 16010101000000.0Z

    # search result
    search: 2
    result: 0 Success

    # numResponses: 2
    # numEntries: 1


We can see that I used "CN=Users,DC=elatov,DC=local" as my **baseDN** and I used the account "administrator@elatov.local" to **bind** to the AD server. I could also use the *elatov* account to bind with, for example:

    # ldapsearch -h 192.168.250.48 -b "CN=Users,DC=elatov,DC=local" -s sub -D "elatov@elatov.local" -W "sAMAccountName=elatov" name
    Enter LDAP Password:
    # extended LDIF
    #
    # LDAPv3
    # base cn =Users,DC=elatov,DC=local> with scope subtree
    # filter: sAMAccountName=elatov
    # requesting: name
    #

    # Karim Elatov, Users, elatov.local
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov

    # search result
    search: 2
    result: 0 Success

    # numResponses: 2
    # numEntries: 1


Notice this time I just grabbed the **name** field to narrow down the search results.

### Use *mozldap* Tools to perform an LDAP Query

Here is the same query as above using the Mozilla LDAP tools:

    # /usr/lib/mozldap/ldapsearch -h 192.168.250.47 -b "CN=Users,DC=elatov,DC=local" -s sub -D "administrator@elatov.local" -w - "sAMAccountName=elatov" name
    Enter bind password:
    version: 1
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov


For now only the password arguments are different.

## Enabling LDAPS on the AD Server

After installing the "Active Directory Domain Services" role, it actually starts the AD Server on the Secure port (**636**):

    C:\Users\Administrator>netstat -abnt | findstr :636
    TCP    0.0.0.0:636            0.0.0.0:0              LISTENING


But since we have not uploaded an appropriate certificate it won't work properly.

### LDAPS Prerequisites

The list is available at [Event ID 1220 — LDAP over SSL](http://technet.microsoft.com/en-us/library/ee411009%28WS.10%29.aspx), from that page:

1.  Certificate must be valid for the purpose of Server Authentication. This means that it must also contains the Server Authentication object identifier (OID): 1.3.6.1.5.5.7.3.1

2.  The Subject name or the first name in the Subject Alternative Name (SAN) must match the Fully Qualified Domain Name (FQDN) of the host machine, such as Subject:CN=server1.contoso.com.

3.  The host machine account must have access to the private key.

I had recently created my own certificate with my own CA. Check out "[certificate_properties.c](http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/) source file here are the different OIDs defined:

    {"1.3.6.1.5.5.7.3.1", "TLS WWW Server"},
    {"1.3.6.1.5.5.7.3.2", "TLS WWW Client"},
    {"1.3.6.1.5.5.7.3.3", "Code signing"},
    {"1.3.6.1.5.5.7.3.4", "Email protection"},
    {"1.3.6.1.5.5.7.3.8", "Time stamping"},
    {"1.3.6.1.5.5.7.3.9", "OCSP signing"},
    {"2.5.29.37.0", "Any purpose"},
    {"2.5.29.9", "Subject Directory Attributes"},
    {"2.5.29.14", "Subject Key Identifier"},
    {"2.5.29.15", "Key Usage"},
    {"2.5.29.16", "Private Key Usage Period"},
    {"2.5.29.17", "Subject Alternative Name"},
    {"2.5.29.19", "Basic Constraints"},
    {"2.5.29.30", "Name Constraints"},
    {"2.5.29.31", "CRL Distribution Points"},
    {"2.5.29.32", "Certificate Policies"},
    {"2.5.29.33", "Policy Mappings"},
    {"2.5.29.35", "Authority Key Identifier"},
    {"2.5.29.36", "Policy Constraints"},
    {"2.5.29.37", "Extended Key Usage"},
    {"2.5.29.46", "Delta CRL Distribution Point"},
    {"2.5.29.54", "Inhibit Any-Policy"},


So let's fire up **gnomint** and check to see if I was lucky enough to allow this certificate to be used for a "TLS WWW Server". To check out if the certificate can be used for that functionality, right click on the certificate and select **Properties**:

![gnomint props cert Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/gnomint_props_cert.png)

Then click on the "Details" tab, expand the "Extensions", and lastly expand the "Extended Key Usage" section:

![cert props gnomint Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/cert-props-gnomint.png)

Yay! I was lucky enough to leave that option enabled. I was using a wild certificate so the subject name would match as well. Now let's follow the instructions from the above Microsoft page to import the certificate.

### Import a Certificate into the AD DS Personal Store

#### 1. Open Microsoft Management Console (MMC).

From the Run dialogue, enter:

    mmc


and you will this:

![mmc started Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/mmc_started.png)

#### 2.Click **File**, click **Add/Remove Snap-in**, select **Certificates** from the available snap-ins, and then click **Add**:

![cert snap int Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/cert-snap-int.png)

#### 3. In **Add or Remove Snap-ins**, click **Service account** to view the certificates that are stored in the service's personal store, and then click **Next**:

![serv acct cert snapin Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/serv_acct_cert_snapin.png)

#### 4. In **Add or Remove Snap-ins**, click **Local computer**, and then click **Next**.

![loc comp cert snapin Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/loc_comp_cert_snapin.png)

#### 5. In **Add or Remove Snap-ins**, click **Active Directory Domain Services**, click **Finish**, and then click **OK**:

![ad ds cert snapin Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ad-ds-cert-snapin.png)

#### 6. In the console tree, expand **Certificates - Service (Active Directory Domain Services)**, expand **Personal**, and then expand **Certificates**:

![ntds cert snapin Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ntds-cert-snapin.png)

#### 7. To import a certificate, right-click the **NTDS\Personal folder**, click **All Tasks**, and then click **Import**:

![cert snapin import cert Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/cert_snapin-import_cert.png)

![import cert Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/import-cert.png)

![include extended props import cert Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/include_extended_props_import_cert.png)

After the certificate is imported you will see the following in the Snap-In:

![ldaps cert imported Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldaps_cert_imported.png)

Since this a self-signed certificate make sure you follow the instructions laid out in "[Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment](http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/)" to import your own CA Certificate under the regular Certificate store. Just launch:

    certmgr.msc


and make sure your CA is in the "Trusted Root Certificate Authorities" folder:

![trusted root ca certs self signed Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/trusted_root_ca_certs_self_signed.png)

### Test LDAPS Connection with **ldp.exe**

Start **ldp.exe**, go to "Connection" -> "Connect", and fill out the necessary information and make sure SSL is chosen:

![ldp exe ssl Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/ldp_exe_ssl.png)

Then click OK and make sure the connection is successful:

![successful ldp exe ssl Enabling LDAPS on Windows 2008 Active Directory Server](https://github.com/elatov/uploads/raw/master/2013/05/successful_ldp_exe_ssl.png)

### Perform LDAPS Query with OpenLDAP tools

If we try the regular search, we will get this error:

    # ldapsearch -x -H ldaps://192.168.250.47:636 -b "CN=Users,DC=elatov,DC=local" -D "administrator@elatov.local" -W - -s sub "(sAMAccountName=elatov)" name
    Enter LDAP Password:
    ldap_bind: Can't contact LDAP server (-1)
        additional info: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed


Since we are using a self-signed certificate, this is expected. From the man page of **ldap.conf**, we have the following options:

    TLS_CACERT filename
                  Specifies  the  file  that  contains certificates for all of the
                  Certificate Authorities the client will recognize.  This is  the
                  preferred  method for specifying the list of Certificate Author-
                  ity certificates.
    ...
    ...

    TLS_CERT filename
                  Specifies  the  file that contains the client certificate.  This
                  is a user-only option.
    ...
    ...

    TLS_REQCERT level
                  Specifies what checks to perform on server certificates in a TLS
                  session, if any. The level can be specified as one of the fol-
                  lowing keywords:

                  never  The  client will not request or check any server certifi-
                         cate.

                  allow  The server certificate is requested. If no certificate is
                         provided,  the  session  proceeds normally. If a bad cer-
                         tificate is provided, it will be ignored and the  session
                         proceeds normally.

                  try    The server certificate is requested. If no certificate is
                         provided, the session proceeds normally. If  a  bad  cer-
                         tificate  is  provided, the session is immediately termi-
                         nated.

                  demand | hard
                         These keywords are equivalent. The server certificate  is
                         requested.  If  no certificate is provided, or a bad cer-
                         tificate is provided, the session is  immediately  termi-
                         nated. This is the default setting.


I had the certificate, but didn't want to bother with the TLS Verification, so I just ignored it:

    # LDAPTLS_REQCERT=never ldapsearch -x -H ldaps://192.168.250.47:636 -b "CN=Users,DC=elatov,DC=local" -D "administrator@elatov.local" -W -s sub "sAMAccountName=elatov" name -LLL
    Enter LDAP Password:
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov


The main difference are between SSL and non-SSL openldap's **ldapsearch** were:

*   **-H** to specify the URI of the AD server
*   **-x** to use simple authentication instead of SASL
*   **-LLL** to get a more succinct search result

### Perform LDAPS Query with MozLDAP tools

Initially the query had the following error:

    # /usr/lib/mozldap/ldapsearch -Z -h 192.168.250.47 -p 636 -D "administrator@elatov.local" -w - -s base -b "CN=Users,DC=elatov,DC=local" "sAMAccountName=elatov" name
    Enter bind password:
    SSL initialization failed: error -8174 (security library: bad database.)


with MozLDAP it actually uses NSS to verify the SSL certificates and unfortunately you can't ignore the verification (or I didn't find a way). So let's go ahead and generate a brand new NSSDB:

    # mkdir -p .pki/nssdb
    # certutil -N -d .pki/nssdb
    Enter a password which will be used to encrypt your keys.
    The password should be at least 8 characters long,
    and should contain at least one non-alphabetic character.

    Enter new password:
    Re-enter password:


Now let's put in our CA into the NSSDB:

    # certutil -d .pki/nssdb -A -n 'elatov-local-root-ca' -i root-ca-elatov-local.pem -t TCP,TCP,TCP


Now let's make sure it's there:

    # certutil -d .pki/nssdb -L
    Certificate Nickname                                         Trust Attributes
                                                                 SSL,S/MIME,JAR/XPI
    elatov-local-root-ca                                         CT,C,C


Now let's do the actual LDAP query with MozLDAP over LDAPS:

    # /usr/lib/mozldap/ldapsearch -h 192.168.250.47 -p 636 -Z -P .pki/nssdb/ -b "CN=Users,DC=elatov,DC=local" -s sub -D "administrator@elatov.local" -w - "sAMAccountName=elatov" name
    Enter bind password:
    version: 1
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov


Now we have confirmed in many different ways that LDAPS on the AD server is working.

