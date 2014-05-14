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
I installed Active Directory by selecting the &#8220;Active Directory Domain Services&#8221; Role from the Server Manager Dialogue. Step by step instructions can be seen in <a href="http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/']);">Deploying a Test Windows Environment in a KVM Infrastucture</a>.

## Running an *ldapsearch* against a Windows AD Server

After you installed AD you can confirm that it&#8217;s listening on port **389**:

    C:\Users\Administrator>netstat -abn | findstr :389
      TCP    0.0.0.0:389            0.0.0.0:0              LISTENING
      TCP    127.0.0.1:389          127.0.0.1:49160        ESTABLISHED
      TCP    127.0.0.1:49160        127.0.0.1:389          ESTABLISHED
      TCP    192.168.250.47:389     192.168.250.47:49175   ESTABLISHED
      TCP    192.168.250.47:49175   192.168.250.47:389     ESTABLISHED
    

We can see it&#8217;s listening on port **389** and there are some local connections to that port for the AD server. Now let&#8217;s go ahead and add a test LDAP user for our queries.

### Add New User to AD via the &#8220;Active Directory Users and Computers&#8221; Console

To start the &#8220;Active Directory Users and Computers&#8221; Console, execute the following command from the run dialogue:

    dsa.msc
    

At which point you will see the following window:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/dsa_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/dsa_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/dsa_started.png" alt="dsa started Enabling LDAPS on Windows 2008 Active Directory Server" width="764" height="530" class="alignnone size-full wp-image-8744" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Then right click in the white space and go to &#8220;New&#8221; -> &#8220;User&#8221;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_dsa_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_dsa_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_dsa_g.png" alt="new user dsa g Enabling LDAPS on Windows 2008 Active Directory Server" width="764" height="535" class="alignnone size-full wp-image-8745" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Then fill out the User information:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_filled_out.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_filled_out.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/new_user_filled_out.png" alt="new user filled out Enabling LDAPS on Windows 2008 Active Directory Server" width="433" height="362" class="alignnone size-full wp-image-8746" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Lastly set the user&#8217;s password:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/set_password.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/set_password.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/set_password.png" alt="set password Enabling LDAPS on Windows 2008 Active Directory Server" width="433" height="364" class="alignnone size-full wp-image-8747" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

After it&#8217;s all said and done you will see the following in the &#8220;Active Directory Users and Computers&#8221; Console:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/user_added_dsa.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/user_added_dsa.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/user_added_dsa.png" alt="user added dsa Enabling LDAPS on Windows 2008 Active Directory Server" width="762" height="530" class="alignnone size-full wp-image-8748" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

So our test user will be **elatov**.

### Use *ldp.exe* to browse the AD Server

From the run dialogue run:

    ldp.exe
    

and you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_started.png" alt="ldp exe started Enabling LDAPS on Windows 2008 Active Directory Server" width="765" height="424" class="alignnone size-full wp-image-8749" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Now let&#8217;s *bind* to the AD server, since we are local to the AD server we can just bind with the same user that we are currently logged in:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bind_button_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bind_button_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bind_button_g.png" alt="ldp exe bind button g Enabling LDAPS on Windows 2008 Active Directory Server" width="765" height="425" class="alignnone size-full wp-image-8750" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

and let&#8217;s leave the defaults:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/bind_dialogue.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/bind_dialogue.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/bind_dialogue.png" alt="bind dialogue Enabling LDAPS on Windows 2008 Active Directory Server" width="278" height="249" class="alignnone size-full wp-image-8751" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

After clicking OK, you will see the connection go through and the *bind* to the AD server succeed:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bound.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bound.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_bound.png" alt="ldp exe bound Enabling LDAPS on Windows 2008 Active Directory Server" width="766" height="571" class="alignnone size-full wp-image-8752" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Now let&#8217;s start browsing the AD server, first let&#8217;s select the &#8220;Tree&#8221; view:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_tree_button_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_tree_button_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_tree_button_g.png" alt="ldp exe tree button g Enabling LDAPS on Windows 2008 Active Directory Server" width="768" height="571" class="alignnone size-full wp-image-8753" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

After that we need to choose the **BaseDN**, this is basically where we want to start the search. We will choose **dc=elatov,dc=local**, which is basically the root of the AD server.

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/tree_view_base_dn.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/tree_view_base_dn.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/tree_view_base_dn.png" alt="tree view base dn Enabling LDAPS on Windows 2008 Active Directory Server" width="432" height="126" class="alignnone size-full wp-image-8777" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

I just want to see all the available branches/children that are part of the AD server:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/children_AD_server.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/children_AD_server.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/children_AD_server.png" alt="children AD server Enabling LDAPS on Windows 2008 Active Directory Server" width="767" height="574" class="alignnone size-full wp-image-8754" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Expanding the **User** branch and locating our test user &#8220;elatov&#8221;, we see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/elatov_user_info_ldp_exe.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/elatov_user_info_ldp_exe.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/elatov_user_info_ldp_exe.png" alt="elatov user info ldp exe Enabling LDAPS on Windows 2008 Active Directory Server" width="792" height="637" class="alignnone size-full wp-image-8755" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

We can see that the DN (Distinguished Name) of the test user is:

    CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    

From now one since we know all the users are under &#8220;CN=Users,DC=elatov,DC=local&#8221; we will use that as our BaseDN, this way we don&#8217;t have to query the whole AD structure.

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

*   <a href="http://www-archive.mozilla.org/directory/tools/ldaptools.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www-archive.mozilla.org/directory/tools/ldaptools.html']);">Mozilla LDAP Tools</a>.
*   <a href="http://www.openldap.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.openldap.org/']);">OpenLDAP Client Tools</a>
*   <a href="http://www.powerbrokeropen.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.powerbrokeropen.org/']);">PowerBroker Open</a> (formely known as LikeWise Open)

Usually the location of the binary will let you know which one you have. For example here are two binaries on the same system:

    # where ldapsearch
    /usr/bin/ldapsearch
    /usr/lib/mozldap/ldapsearch
    

RedHat mostly uses the Mozilla version. From &#8220;<a href="http://www.centos.org/docs/5/html/CDS/ag/8.0/Common_Usage-ldap-tools.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.centos.org/docs/5/html/CDS/ag/8.0/Common_Usage-ldap-tools.html']);">LDAP Tool Locations</a>&#8220;:

> For all Red Hat Directory Server guides and documentation, the LDAP tools used in the examples, such as **ldapsearch** and **ldapmodify**, are the Mozilla LDAP tools. For most Linux systems, OpenLDAP tools are already installed in the **/usr/bin/** directory.

The two different versions have different arguments so make sure you know which one you are using. Let&#8217;s perform an LDAP query with **openldap** tools first:

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
    

We can see that I used &#8220;CN=Users,DC=elatov,DC=local&#8221; as my **baseDN** and I used the account &#8220;administrator@elatov.local&#8221; to **bind** to the AD server. I could also use the *elatov* account to bind with, for example:

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

After installing the &#8220;Active Directory Domain Services&#8221; role, it actually starts the AD Server on the Secure port (**636**):

    C:\Users\Administrator>netstat -abnt | findstr :636
    TCP    0.0.0.0:636            0.0.0.0:0              LISTENING
    

But since we have not uploaded an appropriate certificate it won&#8217;t work properly.

### LDAPS Prerequisites

The list is available at <a href="http://technet.microsoft.com/en-us/library/ee411009%28WS.10%29.aspx" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://technet.microsoft.com/en-us/library/ee411009%28WS.10%29.aspx']);">Event ID 1220 — LDAP over SSL</a>, from that page:

1.  Certificate must be valid for the purpose of Server Authentication. This means that it must also contains the Server Authentication object identifier (OID): 1.3.6.1.5.5.7.3.1

2.  The Subject name or the first name in the Subject Alternative Name (SAN) must match the Fully Qualified Domain Name (FQDN) of the host machine, such as Subject:CN=server1.contoso.com.

3.  The host machine account must have access to the private key.

I had recently created my own certificate with my own CA. Check out &#8220;<a href="http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/']);">Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment</a>&#8221; for more information. I wanted to make sure the certificate I had created had the appropriate OID enabled. From the <a href="http://gnomint.sourcearchive.com/documentation/0.9.1/certificate__properties_8c-source.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://gnomint.sourcearchive.com/documentation/0.9.1/certificate__properties_8c-source.html']);">certificate_properties.c</a> source file here are the different OIDs defined:

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
    

So let&#8217;s fire up **gnomint** and check to see if I was lucky enough to allow this certificate to be used for a &#8220;TLS WWW Server&#8221;. To check out if the certificate can be used for that functionality, right click on the certificate and select **Properties**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/gnomint_props_cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/gnomint_props_cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/gnomint_props_cert.png" alt="gnomint props cert Enabling LDAPS on Windows 2008 Active Directory Server" width="606" height="426" class="alignnone size-full wp-image-8756" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Then click on the &#8220;Details&#8221; tab, expand the &#8220;Extensions&#8221;, and lastly expand the &#8220;Extended Key Usage&#8221; section:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-props-gnomint.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-props-gnomint.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-props-gnomint.png" alt="cert props gnomint Enabling LDAPS on Windows 2008 Active Directory Server" width="766" height="770" class="alignnone size-full wp-image-8787" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Yay! I was lucky enough to leave that option enabled. I was using a wild certificate so the subject name would match as well. Now let&#8217;s follow the instructions from the above Microsoft page to import the certificate.

### Import a Certificate into the AD DS Personal Store

#### 1. Open Microsoft Management Console (MMC).

From the Run dialogue, enter:

    mmc
    

and you will this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/mmc_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/mmc_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/mmc_started.png" alt="mmc started Enabling LDAPS on Windows 2008 Active Directory Server" width="762" height="529" class="alignnone size-full wp-image-8758" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 2.Click **File**, click **Add/Remove Snap-in**, select **Certificates** from the available snap-ins, and then click **Add**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-snap-int.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-snap-int.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert-snap-int.png" alt="cert snap int Enabling LDAPS on Windows 2008 Active Directory Server" width="670" height="463" class="alignnone size-full wp-image-8759" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 3. In **Add or Remove Snap-ins**, click **Service account** to view the certificates that are stored in the service&#8217;s personal store, and then click **Next**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/serv_acct_cert_snapin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/serv_acct_cert_snapin.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/serv_acct_cert_snapin.png" alt="serv acct cert snapin Enabling LDAPS on Windows 2008 Active Directory Server" width="514" height="373" class="alignnone size-full wp-image-8760" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 4. In **Add or Remove Snap-ins**, click **Local computer**, and then click **Next**.

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/loc_comp_cert_snapin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/loc_comp_cert_snapin.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/loc_comp_cert_snapin.png" alt="loc comp cert snapin Enabling LDAPS on Windows 2008 Active Directory Server" width="519" height="375" class="alignnone size-full wp-image-8761" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 5. In **Add or Remove Snap-ins**, click **Active Directory Domain Services**, click **Finish**, and then click **OK**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ad-ds-cert-snapin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ad-ds-cert-snapin.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ad-ds-cert-snapin.png" alt="ad ds cert snapin Enabling LDAPS on Windows 2008 Active Directory Server" width="518" height="373" class="alignnone size-full wp-image-8762" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 6. In the console tree, expand **Certificates &#8211; Service (Active Directory Domain Services)**, expand **Personal**, and then expand **Certificates**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ntds-cert-snapin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ntds-cert-snapin.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ntds-cert-snapin.png" alt="ntds cert snapin Enabling LDAPS on Windows 2008 Active Directory Server" width="762" height="530" class="alignnone size-full wp-image-8763" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

#### 7. To import a certificate, right-click the **NTDS\Personal folder**, click **All Tasks**, and then click **Import**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert_snapin-import_cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/cert_snapin-import_cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/cert_snapin-import_cert.png" alt="cert snapin import cert Enabling LDAPS on Windows 2008 Active Directory Server" width="764" height="532" class="alignnone size-full wp-image-8764" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/import-cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/import-cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/import-cert.png" alt="import cert Enabling LDAPS on Windows 2008 Active Directory Server" width="496" height="446" class="alignnone size-full wp-image-8765" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/include_extended_props_import_cert.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/include_extended_props_import_cert.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/include_extended_props_import_cert.png" alt="include extended props import cert Enabling LDAPS on Windows 2008 Active Directory Server" width="494" height="444" class="alignnone size-full wp-image-8766" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

After the certificate is imported you will see the following in the Snap-In:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldaps_cert_imported.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldaps_cert_imported.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldaps_cert_imported.png" alt="ldaps cert imported Enabling LDAPS on Windows 2008 Active Directory Server" width="761" height="530" class="alignnone size-full wp-image-8767" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Since this a self-signed certificate make sure you follow the instructions laid out in &#8220;<a href="http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/setup-your-own-certificate-authority-ca-on-linux-and-use-it-in-a-windows-environment/']);">Setup Your Own Certificate Authority (CA) on Linux and Use it in a Windows Environment</a>&#8221; to import your own CA Certificate under the regular Certificate store. Just launch:

    certmgr.msc
    

and make sure your CA is in the &#8220;Trusted Root Certificate Authorities&#8221; folder:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/trusted_root_ca_certs_self_signed.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/trusted_root_ca_certs_self_signed.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/trusted_root_ca_certs_self_signed.png" alt="trusted root ca certs self signed Enabling LDAPS on Windows 2008 Active Directory Server" width="870" height="452" class="alignnone size-full wp-image-8768" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

### Test LDAPS Connection with **ldp.exe**

Start **ldp.exe**, go to &#8220;Connection&#8221; -> &#8220;Connect&#8221;, and fill out the necessary information and make sure SSL is chosen:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_ssl.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_ssl.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ldp_exe_ssl.png" alt="ldp exe ssl Enabling LDAPS on Windows 2008 Active Directory Server" width="746" height="443" class="alignnone size-full wp-image-8769" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

Then click OK and make sure the connection is successful:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/05/successful_ldp_exe_ssl.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/05/successful_ldp_exe_ssl.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/successful_ldp_exe_ssl.png" alt="successful ldp exe ssl Enabling LDAPS on Windows 2008 Active Directory Server" width="755" height="603" class="alignnone size-full wp-image-8770" title="Enabling LDAPS on Windows 2008 Active Directory Server" /></a>

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
    

I had the certificate, but didn&#8217;t want to bother with the TLS Verification, so I just ignored it:

    # LDAPTLS_REQCERT=never ldapsearch -x -H ldaps://192.168.250.47:636 -b "CN=Users,DC=elatov,DC=local" -D "administrator@elatov.local" -W -s sub "sAMAccountName=elatov" name -LLL
    Enter LDAP Password: 
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov
    

The main difference are between SSL and non-SSL openldap&#8217;s **ldapsearch** were:

*   **-H** to specify the URI of the AD server
*   **-x** to use simple authentication instead of SASL
*   **-LLL** to get a more succinct search result

### Perform LDAPS Query with MozLDAP tools

Initially the query had the following error:

    # /usr/lib/mozldap/ldapsearch -Z -h 192.168.250.47 -p 636 -D "administrator@elatov.local" -w - -s base -b "CN=Users,DC=elatov,DC=local" "sAMAccountName=elatov" name
    Enter bind password: 
    SSL initialization failed: error -8174 (security library: bad database.)
    

with MozLDAP it actually uses NSS to verify the SSL certificates and unfortunately you can&#8217;t ignore the verification (or I didn&#8217;t find a way). So let&#8217;s go ahead and generate a brand new NSSDB:

    # mkdir -p .pki/nssdb
    # certutil -N -d .pki/nssdb
    Enter a password which will be used to encrypt your keys.
    The password should be at least 8 characters long,
    and should contain at least one non-alphabetic character.
    
    Enter new password: 
    Re-enter password: 
    

Now let&#8217;s put in our CA into the NSSDB:

    # certutil -d .pki/nssdb -A -n 'elatov-local-root-ca' -i root-ca-elatov-local.pem -t TCP,TCP,TCP
    

Now let&#8217;s make sure it&#8217;s there:

    # certutil -d .pki/nssdb -L 
    Certificate Nickname                                         Trust Attributes
                                                                 SSL,S/MIME,JAR/XPI
    elatov-local-root-ca                                         CT,C,C
    

Now let&#8217;s do the actual LDAP query with MozLDAP over LDAPS:

    # /usr/lib/mozldap/ldapsearch -h 192.168.250.47 -p 636 -Z -P .pki/nssdb/ -b "CN=Users,DC=elatov,DC=local" -s sub -D "administrator@elatov.local" -w - "sAMAccountName=elatov" name
    Enter bind password: 
    version: 1
    dn: CN=Karim Elatov,CN=Users,DC=elatov,DC=local
    name: Karim Elatov
    

Now we have confirmed in many different ways that LDAPS on the AD server is working.

