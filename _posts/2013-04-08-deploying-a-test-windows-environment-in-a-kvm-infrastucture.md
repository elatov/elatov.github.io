---
title: Deploying a Test Windows Environment in a KVM Infrastucture
author: Karim Elatov
layout: post
permalink: /2013/04/deploying-a-test-windows-environment-in-a-kvm-infrastucture/
categories: ['home_lab', 'os']
tags: ['linux', 'win2k8r2','libvirt', 'active_directory', 'kvm', 'spice']
---

I was recently playing with KVM and needed to setup a domain controller for testing reasons. A great introduction to KVM can be seen in Jarret's "[Installing KVM as a Virtual Machine on ESXi 5 with Bridged Networking](http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/)" post. It has all the steps on how to set deploy and configure it. All of the below instructions are assuming that you already have a KVM server up and running.


### Connect to the KVM Server with Virtual Machine Manager (virt-manager)

If you don't have [Virtual Machine Manager](http://virt-manager.org/) installed, go ahead and install it:

    sudo yum install virt-manager


Depending on where your ISOs are stored you have a couple of options. If the ISOs are stored on the KVM server then you will have to use SSH X-Forwarding to do the initial setup, and after the initial install you can manage the VMs with **virt-manager** via *qemu+ssh* protocol instead of SSH X-Forwarding. The reason for this is because you can't browse local directories from **virt-manager** remotely. From '[Chapter 12. Managing Storage](https://doc.opensuse.org/documentation/leap/archive/15.0/virtualization/html/book.virt/cha.libvirt.storage.htmll)'

> Using the file browser by clicking on Browse is not possible when operating from remote.

It's possible but all the ISOs would have to be in one big directory without sub-directories, from the same page:

> **CD/DVD ISO images**
>
> In order to be able to access CD/DVD iso images on the VM Host Server from remote, they also need to be placed in a storage pool.

There was an NFS export shared to the KVM server and the ISOs were organized by folders, so adding that directory/export as a storage pool didn't help out since all the ISOs need to be in one big directory. We could add each subdirectory as a storage pool but that would be a lot work. This was discussed in [this](http://www.linuxquestions.org/questions/linux-virtualization-and-cloud-90/virt-manager-save-password-and-recursive-folders-for-storage-volumes-946063/) forum. If the ISOs were local to the your machine, then you can just launch **virt-manager** locally and connect to the KVM server using SSH and then point to the local ISO.

So let's login to our KVM server with SSH with X-Forwarding enabled:

    [elatov@klaptop ~]$ ssh -X virtuser@kvm


Then from the remote machine let's launch **virt-manager**:

    [virtuser@kvm ~]$ virt-manager


At this point you should see the following:

![connected virt manager Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/connected_virt-manager.png)

As you can see it will auto connect to the local instance (if properly configured). You will see a list of the VMs that are currently running and small performance graphs on the right as well. You can go to "Edit" -> "Connection Details":

![virt manager connection details Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/virt_manager_connection_details.png)

After selecting that you will see the following window:

![ssh x kvm conn details g Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/ssh-x-kvm-conn-details_g.png)

From here you can see: connection details, configured Storage Pools, and Configured Networks.

### Create a New VM with Virt-Manager

From the main **virt-manager** window click on the "New" button:

![virt manager create new vm button Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/virt-manager_create-new-vm-button.png)

And that will start the "Create New VM" Wizard:

![create new vm wizard step1 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm-wizard_step1.png)

At the first step: name the VM as you desire, select "Local install media" (since we are going to use the ISO that is locally stored on the KVM server), and then click "Forward":

![create new vm wizard step1 filled out Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_wizard_step1_filled_out.png)

Then you will see the 2nd step of the wizard: ![create new vm wizard step2 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_wizard_step2.png)

Select "Use ISO image", click on "Browse", and then you will see the available Storage Pools:

![create new vm wizard step2 browse storage volumes Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_wizard_step2_browse_storage_volumes.png)

This will show you the *img* files for already running VMs. If we had a storage pool with one big directory of ISOs then you could just select the ISO from that Storage pool (but this wasn't the case for us). Next click on "Browse Local" which is only available if we are connecting locally or with SSH with X-Forwarding. Then we will see the "Browse for ISO" dialogue:

![create new vm step2 locate iso dialogue Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_step2_locate_iso_dialogue.png)

At this point just browse to the location of the ISOs and select your Win2k8 ISO. After that is done, here how step 2 of the wizard will look like:

![create new vm step2 filled out Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_step2_filled_out.png)

Then click "Forward" and then we will get to step 3 of the wizard:

![create new vm step3 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_step3.png)

We have to choose CPU and RAM settings, looking over [this](https://docs.microsoft.com/en-us/windows/deployment/deploy-whats-new) microsoft page, we can see their minimum requirements:

![microsoft min reqs Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/microsoft_min_reqs.png)

I just kept 1CPU and 1GB of RAM and clicked "Forward", at which point I saw step 4 of the wizard:

![create new vm step4 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_step4.png)

I did other installs of the Win2K8R2 and after all the windows updates it ended up using about 20GB, so that is what I setup. Here is how my final step 4 looked like:

![create new vm wizard step4 filled out Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_wizard_step4_filled_out.png)

I then clicked "Forward" and it took to the 5th step (the last step):

![create new vm wizard step5 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_wizard_step5.png)

Here you can select the networking setup for the VM. We were using "bridged" (the same setup that Jarret described in [his](http://virtuallyhyper.com/2012/07/installing-kvm-as-a-virtual-machine-on-esxi5-with-bridged-networking/) post). So I left the defaults and clicked "Finish". At that point the console to the VM started up:


![create new vm console Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_console.png)

Keep going through the install as you would usually do. Here is a screenshot of the install process going:

![create new vm windows install process Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_new_vm_windows_install_process.png)

### Connect to the KVM Server Remotely with virt-manager

After the initial install of the OS is finished you don't need to use SSH X-Forwarding to connect to the KVM server. Install **virt-manager** locally and then fire it up and when it starts up it will try to automatically connect to a hyper-visor:

![searching for available hypervisors Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/searching_for_available_hypervisors.png)

Since we are not running one locally you will get error like this:

![failure to connect to libvirtd Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/failure_to_connect_to_libvirtd.png)

You can just close that and then you will see your **virt-manager** in a disconnected state:

![virt manager not connected Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/virt-manager_not_connected.png)

At this point go to "File" -> "Add Connection":

![virt manager add connection Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/virt-manager_add_connection.png)

Then go ahead and fill out the necessary information:

![add connection filled out Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_connection_filled_out.png)

If you hit connect it will ask for you the virtuser password:

![ssh password g Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/ssh_password_g.png)

It will actually keep asking for the password when you launch VMs. The best thing to do is use SSH keys so you don't have to keep typing in the password. First generate your own pair of SSH keys:

    [elatov@klaptop ~]$ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/elatov/.ssh/id_rsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/elatov/.ssh/id_rsa.
    Your public key has been saved in /home/elatov/.ssh/id_rsa.pub.
    The key fingerprint is:
    a8:42:e5:7e:fd:99:ab:24:94:96:15:e4:da:21:2e:05 elatov@klaptop
    The key's randomart image is:
    +--[ RSA 2048]----+
    |    E  .o        |
    |     . . .       |
    |    . o +        |
    |   o o O .       |
    |  . o O S        |
    | . . = .         |
    |  . o o o        |
    |   . . o . o     |
    |        ..=.     |
    +-----------------+


If you have ssh-agent running then you will just have to type in that password once and you will be set. Now go ahead and add your SSH public key to the KVM server:

    [elatov@klaptop ~]$ ssh-copy-id virtuser@kvm
    virtuser@kvm's password:
    Now try logging into the machine, with "ssh 'virtuser@kvm'", and check in:
    
      ~/.ssh/authorized_keys
    
    to make sure we haven't added extra keys that you weren't expecting.


Now if you try to connect to the KVM server with **virt-manager** via *qemu+ssh* you won't have to enter the virtuser password every time. When you use **virt-manager** remotely you will only see CPU usage like so:

![remote virt manager Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/remote_virt-manager.png)

### Setup a Windows Active Directory Server

Most of the instructions are laid out [here](https://support.rackspace.com/how-to/installing-active-directory-domain-services-on-windows-server-2008-r2-enterprise-64-bit/). After Windows 2008 R2 is installed, launch the Server Manager by entering:

    servermanager.msc


In the run dialog and you will see the following:

![server manager started Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/server_manager_started.png)

Then go to "Roles" and click on "Add Roles":

![blank roles win2k8 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/blank_roles_win2k8.png)

From the list select "Active Directory Domain Services":

![dc role selected Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dc_role_selected.png)

Then click "Next" and couple of times, followed by a "Finish". After the install is done you will see the following:

![dc install finished Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dc_install_finished.png)

Now let's actually configure it. To do that run:

    dcpromo.exe


from the Run dialog and you will see the following:

![ad setup wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/ad_setup_wizard.png)

Click "Next" a couple of times and you see the "Choose Deployment Configuration" window:

![choose deployment conf ad wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/choose_deployment_conf_ad_wizard.png)

I didn't have an existing domain, so I selected "Create a New Domain in a new forest" and clicked next:

![name forest room domain ad wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/name_forest_room_domain_ad_wizard.png)

For my domain I chose "elatov.local":

![elatov local name ad wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/elatov_local_name_ad_wizard.png)

After clicking "Next" I was presented with the following screen:

![set forest functionality lelel ad wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/set_forest_functionality_lelel_ad_wiz.png)

I wasn't planning on using anything below Server 2003, so I left the default option and clicked "Next". At this point I saw the following:

![set domain functional level ad wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/set_domain_functional_level_ad_wiz.png)

Same thing here, I left the default and clicked "Next". I was then asked to setup a DNS server:

![additional domain controller options Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/additional_domain_controller_options.png)

I didn't have a local DNS server in the environment so I decided to set one up. I left the "DNS server" selected and clicked "Next" and saw the following:

![location of db log ad wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/location_of_db_log_ad_wiz.png)

I left the defaults here as well and clicked "Next", at this point I was asked to enter the "Restore Domain Administrator" Password:

![dir ser rest mode admin pass ad wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dir_ser_rest_mode_admin_pass_ad_wiz.png)

After that I was presented with the "Summary" page:

![summary ad wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/summary_ad_wiz.png)

After clicking "Next" the install process started, after the install was finished I saw the following:

![ad setup finished ad wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/ad_setup_finished_ad_wizard.png)

Selecting "Finish" from the above window prompted for a restart. After the restart I saw the following at the login screen:

![ad server joined to domain Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/ad_server_joined_to_domain.png)

Indicating that I was part of the "elatov" domain :) After I logged in I checked the IP settings and I saw the following:

    C:\Users\Administrator>ipconfig /all
    
    Windows IP Configuration
    
       Host Name . . . . . . . . . . . . : dc
       Primary Dns Suffix  . . . . . . . : elatov.local
       Node Type . . . . . . . . . . . . : Hybrid
       IP Routing Enabled. . . . . . . . : No
       WINS Proxy Enabled. . . . . . . . : No
       DNS Suffix Search List. . . . . . : elatov.local
    
    Ethernet adapter Local Area Connection:
    
       Connection-specific DNS Suffix  . :
       Description . . . . . . . . . . . : Realtek RTL8139C+ Fast Ethernet NIC
       Physical Address. . . . . . . . . : 52-54-00-07-BA-A3
       DHCP Enabled. . . . . . . . . . . : No
       Autoconfiguration Enabled . . . . : Yes
       IPv4 Address. . . . . . . . . . . : 192.168.250.47(Preferred)
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.250.1
       DNS Servers . . . . . . . . . . . : 127.0.0.1
       NetBIOS over Tcpip. . . . . . . . : Enabled


### SETUP AN IIS SERVER

Now let's install an IIS Server. From the Run Dialogue, enter

    servermanager.msc


You will then start up the Server Manager:

![servermanager started1 Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/servermanager_started1.png)

Click on "Roles":

![servermanager roles selected Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/servermanager_roles-selected.png)

Then click on "Add Roles", and you will see the "Add Roles Wizard":

![add roles wizard Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_roles_wizard.png)

Select "Web Server (IIS)":

![Web server selected roles wiz Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/Web_server_selected_roles_wiz.png)

Then click "Next" until you get to the "Select Role Services":

![web server role services Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/web_server_role_services.png)

From here you can select the necessary components of IIS that you need. After you have selected the necessary components, click "Next" and then finally click "Install" to start the install:

![iis installing Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/iis_installing.png)

After the install is finished, open Internet Explorer and point it to **http://localhost** you should see the following:

![IE IIS Installed Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/IE_IIS_Installed.png)

Now let's go ahead and enable SSL on our IIS Server. From the Run Dialog enter

    inetmgr


and you will see the following:

![inetmgr started Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/inetmgr_started.png)

Then click on IIS Instance and on the right side you will see a lot of options. Among those options you will see "Server Certificates":

![inetmgr server certificates Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/inetmgr_server_certificates.png)

Then double click on "Server Certificates" and you will see the following:

![server certificated from iis Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/server_certificated_from_iis.png)

Then from the "Right Pane" select "Create Self-Signed Certificate" and the Wizard will start up. Enter the name of the site:

![create self signed certificate Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/create_self_signed_certificate.png)

Then click "OK". You will then see the following under the "Server Certificates":

![server certificates self signed cert created Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/server_certificates_self_signed_cert_created.png)

Now that we have an SSL certificate, we need to enable IIS to listen on port 443. This is done by expanding IIS Instance then expanding the Sites folder and selecting "Default Web Site":

![inetmgr default site selected Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/inetmgr_default_site_selected.png)

On the right you will see an option called "Binding". Click on that and the following will show up:

![inetmgr site bindings Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/inetmgr_site_bindings.png)

Then click "add" and you see the following:

![add site binding inetmgr Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_site_binding_inetmgr.png)

Then change the type to 'https" and select the SSL certificate that we created. In the end it will look like this:

![add site binding filled out inetmgr Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_site_binding_filled_out_inetmgr.png)

Then click "OK" and "Close" and you should be all set. From Internet Explorer go to **https://localhost** and make you see the same page as before:

![IE with https IIS Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/IE_with_https_IIS.png)

### Setup A Windows 7 Client

Install Windows 7 on another VM. Give it an IP and make sure the primary DNS points to the new DC server that we setup. Here is how the IP configuration looked like on my Windows 7 Client:

    C:\Users\elatov>ipconfig /all
    
    Windows IP Configuration
    
       Host Name . . . . . . . . . . . . : client
       Primary Dns Suffix  . . . . . . . :
       Node Type . . . . . . . . . . . . : Hybrid
       IP Routing Enabled. . . . . . . . : No
       WINS Proxy Enabled. . . . . . . . : No
    
    Ethernet adapter Local Area Connection:
    
       Connection-specific DNS Suffix  . :
       Description . . . . . . . . . . . : Realtek RTL8139C+ Fast Ethernet NIC
       Physical Address. . . . . . . . . : 52-54-00-5D-FB-1D
       DHCP Enabled. . . . . . . . . . . : No
       Autoconfiguration Enabled . . . . : Yes
       IPv4 Address. . . . . . . . . . . : 192.168.101.47(Preferred)
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.101.1
       DNS Servers . . . . . . . . . . . : 192.168.250.47
                                           192.168.101.1
       NetBIOS over Tcpip. . . . . . . . : Enabled


Do a test on the client, run **nslookup** to make sure it works:

    C:\Users\elatov>nslookup dc.elatov.local
    Server:  UnKnown
    Address:  192.168.250.47
    
    Name:    dc.elatov.local
    Address:  192.168.250.47


Now let's join our Windows 7 client to our domain. From the Run dialogue type in

    sysdm.cpl


and then you will see the following:

![sys properties client Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/sys_properties_client.png)

Then click "Change" and fill out the Computer Name and the domain you want to join:

![filled out join domain Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/filled_out_join_domain.png)

Then click "OK" and you will need to enter the Domain Administrator's credentials to allow this machine to join:

![join domain security creds Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/join_domain_security_creds.png)

If all is successful you will see the following prompt:

![successful join to domain Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/successful_join_to_domain.png)

And then it will ask you restart the machine. While the machine is restarting go the DC Server and run:

    dsa.msc


That should show you the "Active Directory Users and Computers" dialogue:

![dsa msc Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dsa_msc.png)

Expand your domain (elatov.local), then go to "Computers" and you should see the newly added computer there:

![dsa comp added Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dsa_comp_added.png)

In the same window add a new user by right clicking on the "Users" folder and selecting "Add" -> "User":

![add user from dsa msc g Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_user_from_dsa_msc_g.png)

Here is an example of one user I added:

![add user dialogue Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/add_user_dialogue.png)

After we are done adding the user we will see it in the User's list:

![dsa msc user addedd Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dsa_msc_user_addedd.png)

Then from the client log in with that user, like so:

![login to domain from windows7 client Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/login_to_domain_from_windows7_client.png)

To login to the local user, hit switch user and then type: **.\elatov** along the password:

![login to local windows7 client Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/login_to_local_windows7_client.png)

Another check you can do is make sure the machine was added to DNS. From the DC/DNS Server run:

    dnsmgmt.msc


and you will see the following:

![dnsmgmt started Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dnsmgmt_started.png)

Expand the "Forward Lookup Zones" and then select your domain (elatov.local), on the right side you will see an "A" record for the newly joined machine:

![dnsmgmt added machine Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/dnsmgmt_added_machine.png)

### Connect To KVM Virtual Machines from a Local Machine Using VNCViewer

If you don't want to go through the **virt-manager** to open up a console, you can use **virsh** to determine what *vncdisplay* a VM is using and then connect to that from your local machine. First determine the *vncdisplay* of the desired VM:

    [elatov@klaptop ~]$ virsh -c qemu+ssh://virtuser@kvm/system list
    Id Name State
    ----------------------------------------------------
    1  VM1                 running
    2  VM2                 running
    16 kelatov_win7_client running
    20 kelatov_Win2k8_DC   running
    23 kelatov_win2k8_iis  running


and then this:

    [elatov@klaptop ~]$ virsh -c qemu+ssh://virtuser@kvm/system vncdisplay kelatov_win2k8_iis
    :15


now we know the VNC display is **:15**, so let's connect to that VNC display:

    [elatov@klaptop ~]$ vncviewer kvm:15


If don't want to open up a the firewall to allow the port range for VNC Connections (ie 5900 - 5999), you could use the KVM Host as an SSH tunnel. Here is how the command would look for that:

    [elatov@klaptop ~]$ vncviewer -via virtuser@kvm 127.0.0.1:15


### Enabling Copy and Paste on a Windows KVM VM

To enable Copy and paste within any KVM VM, we need to use **Spice**, more information on Spice can be seen at their home [here](http://spice-space.org/)). This is done by checking if the following RPMs are installed:

    [virtuser@kvm ~]$ rpm -qa | grep spice
    spice-gtk-python-0.6-2.el6.x86_64
    spice-server-0.8.2-5.el6.x86_64
    spice-glib-0.6-2.el6.x86_64
    spice-gtk-0.6-2.el6.x86_64


If those are installed then we can enable Spice on our VMs. To enable Spice on a KVM machine, first shut off the VM. Then from Virt-Manager select the VM, and then go to "Edit" -> "Virtual Machine Details":

![edit vm details Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/edit_vm_details.png)

Notice the VM is a "Shutoff" state, at that point the Console to the VM will open:

![vm details vm off Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_vm_off.png)

Right Next to the "Console" button there is a "Details" button, by clicking that you will see the following:

![vm details window Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_window.png)

From the left pane, select "Video" and you will see this:

![vm details video panel Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_video_panel.png)

Change the Model from "vga" to "qxl":

![vm details change video to glx Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_change_video_to_glx.png)

Then select "Apply" and then select "Display VNC" and you will see the following:

![vm details vnc display panel Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_vnc_display_panel.png)

Then change the "Type" from "VNC" to "Spice", and then click on "Apply", as soon as you hit apply you will see the following pop up:

![vm details change from vnc spice pop up Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_change_from_vnc_spice_pop_up.png)

Click "Yes", after you click "Yes" you will see a new device added called "Channel" like so:

![vm details spice channel added Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/vm_details_spice_channel_added.png)

From there you can click "Run" and the VM will start booting, don't forget to switch from "Details" to "Console" to see the VM's boot process.

After the VM is booted up we need to install the Spice Guest Tools. Open a browse from within the VM and go to **www.spice-space.org/download.html**:

![spice download page from vm Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spice_download_page_from_vm.png)

Scroll down until you see the "Windows guest tools":

![spice guest windows tools from vm in IE Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spice_guest_windows_tools_from_vm_in_IE.png)

Download the tools onto the desktop:

![spice tools downloaded on desktop in VM Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spice_tools_downloaded_on_desktop_in_VM.png)

Then double click on the installer and follow the onscreen instructions:

![spice installer in VM Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spice_installer_in_VM.png)

After the install is done, restart the VM one more time. After the VM reboots you should be able to copy and paste from the console of virt-manager. If you check for running tasks you will see the following processes:

    C:\Users\Administrator>tasklist | findstr vd
    vdservice.exe                  612 Services                   0      3,512 K
    vdagent.exe                    912 Console                    1      3,488 K


I actually copied that from the guest :)

### Using Spice Clients to Connect to Spice-Enabled VMs

If you don't want to use the **virt-manager** console, we can use other Spice clients. First we need to determine what port is used for the Spice connection:

    [elatov@klaptop ~]$ virsh -c qemu+ssh://virtuser@kvm/system dumpxml kelatov_win7_client | grep spice | grep port
    ## <graphics type='spice' port='5913' tlsPort='-1' autoport='yes'></graphics>


So we are on port **5913**, now let's setup an SSH tunnel:

    [elatov@klaptop ~]$ ssh -L 5913:localhost:5913 virtuser@kvm


Then we can use a spice client:

*   spicec (from the *spice-client* package)
*   spicy (from the *spice-gtk-tools* package)
*   remote-viewer (from the *virt-viewer* package)

and connect to **localhost:5913**

Here are examples of each:

    [elatov@klaptop ~]$ spicec -h localhost -p 5913


Here is how it looks like:

![spicec logged in Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spicec_logged_in.png)

or with **remote-viewer**:

    [elatov@klaptop ~]$ remote-viewer spice://localhost:5913


Here is how that will look:

![remote viewer spice Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/remote-viewer_spice.png) and lastly with **spicy**:

    [elatov@klaptop ~]$ spicy


That will launch a GUI and then you can fill out the necessary information, like so:

![sipcy filled out Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/sipcy_filled_out.png)

and then you will see the following:

![spicy connected Deploying a Test Windows Environment in a KVM Infrastucture](https://github.com/elatov/uploads/raw/master/2013/04/spicy_connected.png)

### Related Posts

- [Configure AD Replication with Windows 2008](/2013/06/configure-ad-replication-with-windows-2008/)
- [Enabling LDAPS on Windows 2008 Active Directory Server](/2013/06/enabling-ldaps-on-windows-2008-active-directory-server/)

