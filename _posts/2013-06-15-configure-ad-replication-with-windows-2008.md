---
title: Configure AD Replication with Windows 2008
author: Karim Elatov
layout: post
permalink: /2013/06/configure-ad-replication-with-windows-2008/
dsq_thread_id:
  - 1405505844
categories:
  - Home Lab
  - OS
tags:
  - Active Directory
  - AD Replication
  - repadmin
---
## Types of AD replication

With Active Directory (AD) there are multiple types of replication. From "[What Is Active Directory Replication Topology?](http://technet.microsoft.com/en-us/library/cc775549%28WS.10%29.aspx)":

> As such, replication within sites generally occurs at high speeds between domain controllers that are on the same network segment. Similarly, site link objects can be configured to represent the wide area network (WAN) links that connect LANs. Replication between sites usually occurs over these WAN links, which might be costly in terms of bandwidth. To accommodate the differences in distance and cost of replication within a site and replication between sites, the intrasite replication topology is created to optimize speed, and the intersite replication topology is created to minimize cost.
> ...
> ...
> The Knowledge Consistency Checker (KCC) is a distributed application that runs on every domain controller and is responsible for creating the connections between domain controllers that collectively form the replication topology. The KCC uses Active Directory data to determine where (from what source domain controller to what destination domain controller) to create these connections.

So there are two replication methods: *inter-site* and *intra-site*. From the same site:

> The connections that are used for replication within sites are created automatically with no additional configuration. Intrasite replication takes advantage of LAN network speeds by providing replication as soon as changes occur, without the overhead of data compression, thus maximizing CPU efficiency.
> ...
> ...
> Replication between sites is made possible by user-defined site and site link objects that are created in Active Directory to represent the physical LAN and WAN network infrastructure. When Active Directory sites and site links are configured, the KCC creates an intersite topology so that replication flows between domain controllers across WAN links. Intersite replication occurs according to a site link schedule so that WAN usage can be controlled, and is compressed to reduce network bandwidth requirements.

So intra-site replication is automatically setup, while inter-site requires some manual configuration of site links. I will be deploying another Domain Controller within my Virtual KVM environment, so I will setup intra-site replication. Here is a picture that shows both types of replications:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/site-replication.png" alt="site replication Configure AD Replication with Windows 2008" width="560" height="355" class="alignnone size-full wp-image-8809" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/site-replication.png)

## Data Replicated with AD Replication

The article "[How the Active Directory Replication Model Works](http://technet.microsoft.com/en-us/library/cc772726%28v=ws.10%29.aspx)" talk about what data is replicated:

> Different categories of data are stored in replicas of different directory partitions, as follows:
>
> *   Domain data that is stored in domain directory partitions:
>
>     *   Every domain controller stores one writable domain directory partition.
>     *   A domain controller that is a global catalog server stores one writable domain directory partition and a partial, read-only replica of every other domain in the forest. Global catalog read-only replicas contain a partial set of attributes for every object in the domain.
>
> *   Configuration data: Every domain controller stores one writable configuration directory partition that stores forest-wide data controlling site and replication operations.
>
> *   Schema data: Every domain controller stores one writable schema partition that stores schema definitions for the forest. Although the schema directory partition is writable, schema updates are allowed on only the domain controller that holds the role of schema operations master.
>
> *   Application data: Domain controllers that are running Windows Server 2003 can store directory partitions that store application data. Application directory partition replicas can be replicated to any set of domain controllers in a forest, irrespective of domain.

## AD Replication Interval

The interval of the replication depends on your setup as well. From "[Replication within a site](http://technet.microsoft.com/en-us/library/cc728010%28v=ws.10%29.aspx)":

> Directory updates made within a site are likely to have the most direct impact on local clients, so intrasite replication is optimized for speed. Replication within a site occurs automatically on the basis of change notification. Intrasite replication begins when you make a directory update on a domain controller. By default, the source domain controller waits 15 seconds and then sends an update notification to its closest replication partner. If the source domain controller has more than one replication partner, subsequent notifications go out by default at 3 second intervals to each partner. After receiving notification of a change, a partner domain controller sends a directory update request to the source domain controller. The source domain controller responds to the request with a replication operation. The 3 second notification interval prevents the source domain controller from being overwhelmed with simultaneous update requests from its replication partners.

From "[Understanding Replication Between Sites](http://technet.microsoft.com/en-us/library/cc771251.aspx)":

> AD DS preserves bandwidth between sites by minimizing the frequency of replication and by making it possible for you to schedule the availability of site links for replication. By default, intersite replication across each site link occurs every 180 minutes (3 hours). You can adjust this frequency to match your specific needs.

So intra-site replication is automatic, while inter-site is setup on a interval based schedule. Also from "[Active Directory Replication Technologies](http://technet.microsoft.com/en-us/library/cc776877%28v=ws.10%29.aspx)":

> Replication topology generation is optimized for speed within sites and for cost between sites. Replication between domain controllers in the same site occurs automatically in response to changes and does not require administrative management. Replication within a site is sent uncompressed to reduce processing time. Replication between domain controllers in different sites can be managed to control the scheduling and routing of replication over WAN links. Replication between sites is compressed so that it uses less bandwidth when sent across WAN links, thereby reducing the cost.

## How is AD Replication Triggered?

From "[How the Active Directory Replication Model Works?](http://technet.microsoft.com/en-us/library/cc772726%28v=ws.10%29.aspx)":

> **Originating Updates: Initiating Changes**
> As a Lightweight Directory Access Protocol (LDAP) directory service, Active Directory supports the following four types of update requests:
>
> *   Add an object to the directory.
> *   Modify (add, delete, or replace) attribute values of an object in the directory.
> *   Move an object by changing the name or parent of the object.
> *   Delete an object from the directory.
>
> Each LDAP request generates a separate write transaction. An LDAP directory service processes each write request as an atomic transaction; that is, the transaction is either completed in full or not applied at all. The practical limit to the number of values that can be written in one LDAP transaction is approximately 5,000 values added, modified, or deleted at the same time.

Here is a nice diagram of the process:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/repl_seq.png" alt="repl seq Configure AD Replication with Windows 2008" width="488" height="534" class="alignnone size-full wp-image-8813" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/repl_seq.png)

## Install 2nd Active Directory Server

So now that we know what replication is, let's actually set it up.

### AD Information Before Replication is setup

Before we go any further let's take a snapshot of our users from the current AD server:

    C:\Users\Administrator>dsquery user
    "CN=Administrator,CN=Users,DC=elatov,DC=local"
    "CN=Guest,CN=Users,DC=elatov,DC=local"
    "CN=krbtgt,CN=Users,DC=elatov,DC=local"
    "CN=Karim Elatov,CN=Users,DC=elatov,DC=local"


Also let's see if replication is setup:

    C:\Users\Administrator>repadmin /showrepl

    Repadmin: running command /showrepl against full DC localhost
    Default-First-Site-Name\DC
    DSA Options: IS_GC
    Site Options: (none)
    DSA object GUID: a68c69a8-b015-4254-b81c-dc65782bd1fa
    DSA invocationID: a68c69a8-b015-4254-b81c-dc65782bd1fa


And of course it's not. Also let's check out the DNS Zones defined on the AD server:

    C:\Users\Administrator>dnscmd  /EnumZones

    Enumerated zone list:
            Zone count = 5

     Zone name                      Type       Storage         Properties

     .                              Cache      AD-Domain
     _msdcs.elatov.local            Primary    AD-Forest       Secure
     101.168.192.in-addr.arpa       Primary    AD-Domain       Secure Rev
     250.168.192.in-addr.arpa       Primary    AD-Domain       Secure Rev
     elatov.local                   Primary    AD-Domain       Secure


    Command completed successfully.


And now let's check out our DNS Records:

    C:\Users\Administrator>dnscmd  /EnumRecords elatov.local @ /type A
    Returned records:
    @                [Aging:3614830] 600  A  192.168.250.47
    CLIENT           [Aging:3613844] 1200 A  192.168.101.47
    cluster                          3600 A  192.168.250.51
    dc                               1200 A  192.168.250.47
    haproxy                          3600 A  192.168.250.52
    iis-2            [Aging:3613995] 1200 A  192.168.250.49

    Command completed successfully.


### Install a 2nd AD Server and Replicate Data

I installed a second Active Directory Server by selecting the “Active Directory Domain Services” Role from the Server Manager Dialogue. Step by step instructions can be seen in [Deploying a Test Windows Environment in a KVM Infrastucture](http://virtuallyhyper.com/2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/). After that was installed I ran the following from the run dialogue:

    dcpromo.exe


And I saw the following screen:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard.png" alt="ad wizard Configure AD Replication with Windows 2008" width="497" height="471" class="alignnone size-full wp-image-8816" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard.png)

Let's choose to "Add a domain controller to an existing domain":

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/existing_forest.png" alt="existing forest Configure AD Replication with Windows 2008" width="496" height="471" class="alignnone size-full wp-image-8817" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/existing_forest.png)

Enter the name of the Domain and enter the admin password for that Domain:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/enter_domain_name.png" alt="enter domain name Configure AD Replication with Windows 2008" width="498" height="469" class="alignnone size-full wp-image-8818" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/enter_domain_name.png)

If the connection to the primary DC is successful, you will see the following:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/existing_DC.png" alt="existing DC Configure AD Replication with Windows 2008" width="495" height="468" class="alignnone size-full wp-image-8819" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/existing_DC.png)

We won't be doing any inter-site setup, so selecting the default site name is okay here:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/default_site_ad_setup.png" alt="default site ad setup Configure AD Replication with Windows 2008" width="496" height="469" class="alignnone size-full wp-image-8820" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/default_site_ad_setup.png)

Next let's setup a DNS server on the new DC and let's NOT make it Read only (RODC):

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/additional_dc_options.png" alt="additional dc options Configure AD Replication with Windows 2008" width="494" height="467" class="alignnone size-full wp-image-8821" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/additional_dc_options.png)

Next, let's go ahead and replicate the AD configuration from the primary DC:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/replicate_data_ad_wizrd.png" alt="replicate data ad wizrd Configure AD Replication with Windows 2008" width="495" height="469" class="alignnone size-full wp-image-8822" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/replicate_data_ad_wizrd.png)

Click "Next" a couple of times and at the end, you will get to the summary page:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard_summary.png" alt="ad wizard summary Configure AD Replication with Windows 2008" width="496" height="469" class="alignnone size-full wp-image-8823" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard_summary.png)

After you click "Next", the replication will start:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/replicating_data.png" alt="replicating data Configure AD Replication with Windows 2008" width="425" height="293" class="alignnone size-full wp-image-8824" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/replicating_data.png)

After it's done, you will see the following:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard_finished.png" alt="ad wizard finished Configure AD Replication with Windows 2008" width="495" height="468" class="alignnone size-full wp-image-8826" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/ad_wizard_finished.png)

Click "Finish" and restart the machine.

## Confirm the Replication Worked

After the machine is rebooted you will see that it's part of the domain and it's setup as a "Backup DC":

    C:\Users\Administrator.ELATOV>systeminfo | findstr "Domain"
    OS Configuration:          Additional/Backup Domain Controller
    Domain:                    elatov.local


Now let's make sure the same users exist on the this machine as well:

    C:\Users\Administrator.ELATOV>dsquery user
    "CN=Administrator,CN=Users,DC=elatov,DC=local"
    "CN=Guest,CN=Users,DC=elatov,DC=local"
    "CN=krbtgt,CN=Users,DC=elatov,DC=local"
    "CN=Karim Elatov,CN=Users,DC=elatov,DC=local"


Checking the DNS Records on the new machine, I saw the following:

    C:\Users\Administrator.ELATOV>dnscmd /EnumRecords elatov.local @ /type A
    Returned records:
    @                [Aging:3614831] 600  A  192.168.250.54
                     [Aging:3614830] 600  A  192.168.250.47
    CLIENT           [Aging:3613844] 1200 A  192.168.101.47
    cluster                          3600 A  192.168.250.51
    dc                               3600 A  192.168.250.47
    dc2                              3600 A  192.168.250.54
    haproxy                          3600 A  192.168.250.52
    iis-2            [Aging:3613995] 1200 A  192.168.250.49

    Command completed successfully.


We can see that our machine (dc2) was automatically added to DNS. Checking for that record on the primary DC, I saw the following:

    C:\Users\Administrator>dnscmd /EnumRecords elatov.local dc2 /type A
    Returned records:
    @                    [Aging:3614831] 3600 A  192.168.250.54

    Command completed successfully.


That looks good. Now to check the status of the replication:

    C:\Users\Administrator.ELATOV>repadmin /replsummary
    Replication Summary Start Time: 2013-05-18 16:43:23

    Beginning data collection for replication summary, this may take awhile:
      .....


    Source DSA          largest delta    fails/total %%   error
     DC                        12m:11s    0 /   5    0
     DC2                       11m:29s    0 /   5    0


    Destination DSA     largest delta    fails/total %%   error
     DC                        11m:29s    0 /   5    0
     DC2                       12m:11s    0 /   5    0


No errors are seen. We can also see all the data that has been replicated:

    C:\Users\Administrator>repadmin /showrepl

    Repadmin: running command /showrepl against full DC localhost
    Default-First-Site-Name\DC
    DSA Options: IS_GC
    Site Options: (none)
    DSA object GUID: a68c69a8-b015-4254-b81c-dc65782bd1fa
    DSA invocationID: a68c69a8-b015-4254-b81c-dc65782bd1fa

    ==== INBOUND NEIGHBORS ======================================

    DC=elatov,DC=local
        Default-First-Site-Name\DC2 via RPC
            DSA object GUID: f3d68c86-ec97-42d0-8aef-f62e8c70f347
            Last attempt @ 2013-05-18 16:33:47 was successful.

    CN=Configuration,DC=elatov,DC=local
        Default-First-Site-Name\DC2 via RPC
            DSA object GUID: f3d68c86-ec97-42d0-8aef-f62e8c70f347
            Last attempt @ 2013-05-18 16:35:57 was successful.

    CN=Schema,CN=Configuration,DC=elatov,DC=local
        Default-First-Site-Name\DC2 via RPC
            DSA object GUID: f3d68c86-ec97-42d0-8aef-f62e8c70f347
            Last attempt @ 2013-05-18 16:31:54 was successful.

    DC=DomainDnsZones,DC=elatov,DC=local
        Default-First-Site-Name\DC2 via RPC
            DSA object GUID: f3d68c86-ec97-42d0-8aef-f62e8c70f347
            Last attempt @ 2013-05-18 16:31:54 was successful.

    DC=ForestDnsZones,DC=elatov,DC=local
        Default-First-Site-Name\DC2 via RPC
            DSA object GUID: f3d68c86-ec97-42d0-8aef-f62e8c70f347
            Last attempt @ 2013-05-18 16:31:54 was successful.


We can see that DNS is included as well. This is expected since we have AD-intergrated DNS. From "[Active Directory-Integrated DNS Zones](http://technet.microsoft.com/en-us/library/cc731204%28v=ws.10%29.aspx)":

> Domain Name System (DNS) servers running on domain controllers can store their zones in Active Directory Domain Services (AD DS). In this way, it is not necessary to configure a separate DNS replication topology that uses ordinary DNS zone transfers because all zone data is replicated automatically by means of Active Directory replication.

I thought that was pretty convenient. We can also make sure the two server are in the same site. From the run dialogue execute the following:

    dssite.msc


Expand "Sites" -> "Default Site" -> "Servers" and make sure you see both servers:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/dssite_msc.png" alt="dssite msc Configure AD Replication with Windows 2008" width="483" height="225" class="alignnone size-full wp-image-8842" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/dssite_msc.png)

If we were doing inter-site replication, we would have to create different site and replication schedules here.

## Test Our Replication

To test out replication we can create a snapshot of the data by running the following from the command prompt:

    C:\Users\Administrator.ELATOV>repadmin /showchanges . dc=elatov,dc=local /cookie:config.txt
    ...
    ...
    DC2,CN=Domain System Volume (SYSVOL share),CN=File Replication Service,CN=System
    ,DC=elatov,DC=local
    New cookie written to file config.txt (132 bytes)


That will create a "cookie" file with the data inside of it, in my case the file is called *config.txt*. Then let's go ahead and add a new User to the primary DC, and see if that user gets replicated. From the run dialogue execute:

    dsa.msc


And select "New" -> "User":

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/dsa_msc_new_user.png" alt="dsa msc new user Configure AD Replication with Windows 2008" width="761" height="531" class="alignnone size-full wp-image-8828" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/dsa_msc_new_user.png)

Let's call our user "test":

[<img src="http://virtuallyhyper.com/wp-content/uploads/2013/05/test_user_dsa_msc.png" alt="test user dsa msc Configure AD Replication with Windows 2008" width="433" height="363" class="alignnone size-full wp-image-8829" title="Configure AD Replication with Windows 2008" />](http://virtuallyhyper.com/wp-content/uploads/2013/05/test_user_dsa_msc.png)

After the user is created run the above command again:

    C:\Users\Administrator.ELATOV>repadmin /showchanges . dc=elatov,dc=local /cookie:config.txt

    Repadmin: running command /showchanges against full DC localhost
    Using cookie from file config.txt (132 bytes)
    ==== SOURCE DSA: localhost ====
    Objects returned: 1
    (0) add CN=test,CN=Users,DC=elatov,DC=local
        1> parentGUID: 8793942d-d052-4a2f-9eaa-c44f45715be0
        1> objectGUID: a94935e4-ca0a-4699-b01b-b4e84e9f4b12
        4> objectClass: top; person; organizationalPerson; user
        1> givenName: tes
        1> instanceType: 0x4 = ( WRITE )
        1> whenCreated: 5/18/2013 6:22:49 PM Pacific Daylight Time
        1> displayName: tes
        1> nTSecurityDescriptor: O:DAGddfdfgdfgdfg
        1> name: tes
        1> userAccountControl: 0x10200 = ( NORMAL_ACCOUNT | DONT_EXPIRE_PASSWD )
        1> codePage: 0
        1> countryCode: 0
        0> dBCSPwd:
        0> logonHours:
        0> unicodePwd:
        0> ntPwdHistory:
        1> pwdLastSet: 5/18/2013 6:22:49 PM Pacific Daylight Time
        1> primaryGroupID: 513 = ( GROUP_RID_USERS )
        0> supplementalCredentials:
        1> objectSid: S-1-5-21-3787252690-2443488306-3332615697-1109
        1> accountExpires: (never)
        0> lmPwdHistory:
        1> sAMAccountName: test
        1> sAMAccountType: 805306368 = ( NORMAL_USER_ACCOUNT )
        1> userPrincipalName: test@elatov.local
        1> objectCategory: guid =278ebe8ed9bd3f469b97d822790af4fc;CN=Person,CN=Schema,CN=Configuration,DC=elatov,DC=local
    New cookie written to file config.txt (132 bytes)


We can see that the difference in the cookie file since it was last run is the newly added test user. Also checking to make sure the user exists:

    C:\Users\Administrator.ELATOV>dsquery user
    "CN=Guest,CN=Users,DC=elatov,DC=local"
    "CN=krbtgt,CN=Users,DC=elatov,DC=local"
    "CN=Administrator,CN=Users,DC=elatov,DC=local"
    "CN=Karim Elatov,CN=Users,DC=elatov,DC=local"
    "CN=test,CN=Users,DC=elatov,DC=local"


I added a new user called 'test2' and made sure it was replicated. I then removed the user, ran the same command, and here is what I saw:

    C:\Users\Administrator.ELATOV>repadmin /showchanges . dc=elatov,dc=local /cookie:config.txt

    Repadmin: running command /showchanges against full DC localhost
    Using cookie from file config.txt (132 bytes)
    ==== SOURCE DSA: localhost ====
    Objects returned: 1
    (0) delete CN=test2\0ADEL:a94935e4-ca0a-4699-b01b-b4e84e9f4b12,CN=Deleted Objects,DC=elatov,DC=local
        1> parentGUID: 5a9f62a2-0205-4100-8eac-4ccb60a75f7a
        1> objectGUID: a94935e4-ca0a-4699-b01b-b4e84e9f4b12
        0> givenName:
        1> instanceType: 0x4 = ( WRITE )
        0> displayName:
        1> isDeleted: TRUE
        1> name: test2
    DEL:a94935e4-ca0a-4699-b01b-b4e84e9f4b12
        0> codePage:
        0> countryCode:
        0> unicodePwd:
        0> ntPwdHistory:
        0> pwdLastSet:
        0> primaryGroupID:
        0> supplementalCredentials:
        0> accountExpires:
        0> lmPwdHistory:
        0> sAMAccountType:
        0> userPrincipalName:
        1> lastKnownParent: guid =2d94938752d02f4a9eaac44f45715be0;CN=Users,DC=elatov,DC=local
        0> objectCategory:
        1> isRecycled: TRUE
    New cookie written to file config.txt (132 bytes)


We again see the changes.

