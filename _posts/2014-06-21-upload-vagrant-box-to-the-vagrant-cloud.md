---
layout: post
title: "Upload Vagrant Box to the Vagrant Cloud"
author: Karim Elatov
description: ""
categories: [os]
tags: [vagrant,virtualbox]
---
In order for your Vagrant Box to support versioning, you have to use the vagrant cloud (create an account on **https://vagrantcloud.com**). From [Creating A Base Box](http://docs.vagrantup.com/v2/boxes/base.html):

> You can distribute the box file however you'd like. However, if you want to support versioning, putting multiple providers at a single URL, pushing updates, analytics, and more, we recommend you add the box to Vagrant Cloud.
> 
> You can upload both public and private boxes to this service.

Another note is that you have to use vagrant version 1.5 or above, from [Box Versioning](http://docs.vagrantup.com/v2/boxes/versioning.html):

> Since Vagrant 1.5, boxes support versioning. This allows the people who make boxes to push updates to the box, and the people who use the box have a simple workflow for checking for updates, updating their boxes, and seeing what has changed.

So login to the [vagrantcloud](https://vagrantcloud.com/) site and click on "Create One":

![vagrant-cloud-create-one-button](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-create-one-button.png)

Fill out all the information (like name and description of box):

![vagrant-cloud-name-box](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-name-box.png)

Give the Box a version and create a comment for the version:

![vagrant-cloud-version-box](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-version-box.png)

Assign a provider to the box:

![vagrant-cloud-vb-provider](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-vb-provider.png)

I created this one for VirtualBox. Then provide a URL of the box file, to upload to the vagrant cloud you need to have a paid account. I uploaded my vagrant box to my test google drive account:

![vagrant-cloud-provider-url](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-provider-url.png)

After that you have to release that version of the vagrant box:

![vagrant-release-box](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-release-box.png)

After it's successful, you will see the successful page:

![vagrant-cloud-successfully-released](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vagrant-cloud-successfully-released.png)

At this point you can add that box to your local vagrant instance like so:

	elatov@kmac:~$vagrant box add elatov/opensuse13-32
	==> box: Loading metadata for box 'elatov/opensuse13-32'
	    box: URL: https://vagrantcloud.com/elatov/opensuse13-32
	==> box: Adding box 'elatov/opensuse13-32' (v0.0.1) for provider: virtualbox
	    box: Downloading: https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box
	==> box: Successfully added box 'elatov/opensuse13-32' (v0.0.1) for 'virtualbox'!
	
Now if I go back to vagrant cloud, I can add a new version. Fist click on your box in vagrant cloud:

![boxes-in-vc](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/boxes-in-vc.png)

Then click on "create a version +":

![vg-new-version-button](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vg-new-version-button.png)

Then name the version:

![vc-new-version-box](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vc-new-version-box.png)

Then configure the provider for the new version:

![vc-new-verion-provider](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vc-new-verion-provider.png)

The go ahead and release the new version:

![vc-release-new-version](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vc-release-new-version.png)

If successful, you will see the following:

![vc-new-version-released](https://googledrive.com/host/0B4vYKT_-8g4IQzlMV2pSZXNrTHM/vc-new-version-released.png)

Now in your local vagrant instance you can check if any of your boxes are out of date:

	elatov@kmac:~$vagrant box outdated --global
	* 'opensuse13-32' wasn't added from a catalog, no version information
	* 'hashicorp/precise32' (v1.0.0) is up to date
	* 'elatov/opensuse13-32' is outdated! Current: 0.0.1. Latest: 0.0.2

We can see that the opensuse from the vagrant cloud is now outdated. To update the box to the latest version, you can run the following:

	elatov@kmac:~$vagrant box update -b elatov/opensuse13-32
	Checking for updates to 'elatov/opensuse13-32'
	Latest installed version: 0.0.1
	Version constraints: > 0.0.1
	Provider: virtualbox
	Updating 'elatov/opensuse13-32' with provider 'virtualbox' from version
	'0.0.1' to '0.0.2'...
	Loading metadata for box 'https://vagrantcloud.com/elatov/opensuse13-32'
	Adding box 'elatov/opensuse13-32' (v0.0.2) for provider: virtualbox
	Downloading: https://vagrantcloud.com/elatov/opensuse13-32/version/2/provider/virtualbox.box
	Successfully added box 'elatov/opensuse13-32' (v0.0.2) for 'virtualbox'!
	
It doesn't actually check the versions of the file and it will download the box again, even if it's the same (the download takes about 5mins, 700MB from gdrive... not bad). Here is a **wget** of the file:

	elatov@kmac:~/test2$wget https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box
	-2014-06-11 14:08:27--  https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box
	Resolving vagrantcloud.com (vagrantcloud.com)... 54.209.4.164, 107.23.21.165
	Connecting to vagrantcloud.com (vagrantcloud.com)|54.209.4.164|:443... connected.
	HTTP request sent, awaiting response... 302 Found
	Location: https://googledrive.com/host/0B4vYKT_-8g4IdzQ0eHV5YWZtQU0/vagrant-opensuse13-32.box [following]
	--2014-06-11 14:08:28--  https://googledrive.com/host/0B4vYKT_-8g4IdzQ0eHV5YWZtQU0/vagrant-opensuse13-32.box
	Resolving googledrive.com (googledrive.com)... 74.125.225.171, 74.125.225.172, 74.125.225.170, ...
	Connecting to googledrive.com (googledrive.com)|74.125.225.171|:443... connected.
	HTTP request sent, awaiting response... 200 OK
	Length: 721075604 (688M) [application/x-gzip]
	Saving to: ‘virtualbox.box’
	100%[======================================>] 721,075,604 2.57MB/s   in 3m 15s

	2014-06-11 14:11:43 (3.53 MB/s) - ‘virtualbox.box’ saved [721075604/721075604]
	
	FINISHED --2014-06-11 14:11:43--
	Total wall clock time: 3m 17s
	Downloaded: 1 files, 688M in 3m 15s (3.53 MB/s)


At this point you will have two different versions of the vmdks as well:

	elatov@kmac:~$tree .vagrant.d/boxes/elatov-VAGRANTSLASH-opensuse13-32/
	.vagrant.d/boxes/elatov-VAGRANTSLASH-opensuse13-32/
	├── 0.0.1
	│   └── virtualbox
	│       ├── Vagrantfile
	│       ├── box-disk1.vmdk
	│       ├── box.ovf
	│       └── metadata.json
	├── 0.0.2
	│   └── virtualbox
	│       ├── Vagrantfile
	│       ├── box-disk1.vmdk
	│       ├── box.ovf
	│       └── metadata.json
	└── metadata_url
	
	4 directories, 9 files
	
And vagrant will list them as separate boxes:

	elatov@kmac:~$vagrant box list
	elatov/opensuse13-32 (virtualbox, 0.0.1)
	elatov/opensuse13-32 (virtualbox, 0.0.2)
	hashicorp/precise32  (virtualbox, 1.0.0)
	opensuse13-32        (virtualbox, 0)
	
To remove the old version you can run the following (to save space on the local machine):

	elatov@kmac:~$vagrant box remove elatov/opensuse13-32 --box-version 0.0.1
	Removing box 'elatov/opensuse13-32' (v0.0.1) with provider 'virtualbox'...
	
If for whatever reason you wanted to download the old version you could do the following:

	elatov@kmac:~$vagrant box add elatov/opensuse13-32 --box-version 0.0.1
	==> box: Loading metadata for box 'elatov/opensuse13-32'
	    box: URL: https://vagrantcloud.com/elatov/opensuse13-32
	==> box: Adding box 'elatov/opensuse13-32' (v0.0.1) for provider: virtualbox
	    box: Downloading: https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box
	==> box: Successfully added box 'elatov/opensuse13-32' (v0.0.1) for 'virtualbox'!

If you want to init an old box, you can specify the URL for the first version like so:

	elatov@kmac:~/test2$vagrant init elatov/opensuse13-32 https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box
	A `Vagrantfile` has been placed in this directory. You are now
	ready to `vagrant up` your first virtual environment! Please read
	the comments in the Vagrantfile as well as documentation on
	`vagrantup.com` for more information on using Vagrant.
	elatov@kmac:~/test2$vagrant up
	Bringing machine 'default' up with 'virtualbox' provider...
	==> default: Importing base box 'elatov/opensuse13-32'...
	==> default: Matching MAC address for NAT networking...
	==> default: Checking if box 'elatov/opensuse13-32' is up to date...
	
You will notice the URL defined in the **Vagrantfile** of the old version and not in the new version:

	elatov@kmac:~$grep box_url test1/Vagrantfile test2/Vagrantfile
	test2/Vagrantfile:  config.vm.box_url = "https://vagrantcloud.com/elatov/opensuse13-32/version/1/provider/virtualbox.box"

Another note, if you don't want to keep downloading the box file, you can repackage the downloaded box file and store it locally as well. This is accomplished with the following command:

	elatov@kmac:~$vagrant box repackage elatov/opensuse13-32 virtualbox 0.0.2

then in the current directory you will have a **package.box** file:

	elatov@kmac:~$ls -lh pack*
	-rw-r--r--  1 elatov  staff   688M Jun 11 14:30 package.box

I also ran into a cool git hub project to host your own vagrant cloud: [vagrant-catalog](https://github.com/vube/vagrant-catalog). As long as the server/location has a valid json it should allow versioning of the box as per [this](https://groups.google.com/forum/#!topic/vagrant-up/NV_2FUPNjjg) google forum.
