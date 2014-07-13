---
title: 'Update Splunk 6.0 to 6.0.3 on FreeBSD'
author: Karim Elatov
layout: post
permalink: /2014/05/update-splunk-6-0-to-6-0-3/
categories: ['home_lab', 'os']
tags: ['heartbleed', 'freebsd', 'splunk']
---


A new version of splunk came out and I decided to apply it (here are the [release notes][1], it mostly fixes the heartbleed vulnerability). The update process is covered in detail [here][2]. I was using a FreeBSD machine to host Splunk (check out a previous post on that [here][3]) and I first needed to install the **pkg_install** port in order to install the old style package.

### Install pkg_install on FreeBSD

The install itself is pretty easy:

    cd /usr/ports/ports-mgmt/pkg_install
    sudo make install


### Backup Original Splunk Install

To be safe let's go ahead and create a backup of the current setup. To do this, first stop the service:

    sudo service splunk stop


Then to the splunk home location and tar up the install:

    cd /opt
    sudo tar cpjvf splunk_4_15_14.tar.bz splunk


### Update Splunk 6.0 to 6.0.3

After the backup is finished, download the package from splunk site and then install it:

    sudo pkg_add -f splunk-6.0.3-204106-freebsd-7.3-amd64.tgz
    ..
    ..
    This looks like an upgrade of an existing Splunk Server. Attempting to stop the installed Splunk Server...
    splunkweb is not running.
    splunkd is not running.
    complete


Since it was an old style of the package, there were a couple of warnings, but it went through fine (I also ended up using the **-f** flag to force the install, since the old version of the package was already installed).

To check what changes will be made, start the service and you will see the following:

    sudo /opt/splunk/bin/splunk start --accept-license


and you will see the following:

    This appears to be an upgrade of Splunk.
    --------------------------------------------------------------------------------)

    Splunk has detected an older version of Splunk installed on this machine. To
    finish upgrading to the new version, Splunk's installer will automatically
    update and alter your current configuration files. Deprecated configuration
    files will be renamed with a .deprecated extension.

    You can choose to preview the changes that will be made to your configuration
    files before proceeding with the migration and upgrade:

    If you want to migrate and upgrade without previewing the changes that will be
    made to your existing configuration files, choose 'y'.
    If you want to see what changes will be made before you proceed with the
    upgrade, choose 'n'.


    Perform migration and upgrade without previewing configuration changes? [y/n] n

    -- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2014-04-15.12-22-58' --

    Migrating to:
    VERSION=6.0.3
    BUILD=204106
    PRODUCT=splunk
    PLATFORM=FreeBSD-amd64


    ********** BEGIN PREVIEW OF CONFIGURATION FILE MIGRATION **********

    Would copy '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.

    Checking saved search compatibility...

    Checking for possible timezone configuration errors...

    Handling deprecated files...
    hecking script configuration...

    Would copy '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
    Would delete '/opt/splunk/etc/system/local/field_actions.conf.migratePreview'.
    Would move '/opt/splunk/share/splunk/search_mrsparkle/modules' to '/opt/splunk/share/splunk/search_mrsparkle/modules.old.20140415-122258'.
    Would move '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
    Checking for possible UI view conflicts...

    The following files would be created or modified (without the .migratePreview extension):
      /opt/splunk/etc/system/local/eventtypes.conf.migratePreview
      /opt/splunk/etc/system/local/field_actions.conf.migratePreview
      /opt/splunk/etc/system/local/serverclass.conf.migratePreview

    Migration is continuing...

    Clustering migration already complete, no further changes required.


    ********** END PREVIEW OF CONFIGURATION FILE MIGRATION **********

    Stopping because you requested a preview of the configuration files to be
    migrated.  Migration and upgrade will not continue until the configuration files
    have actually been migrated.

    To proceed, run 'splunk start' again and choose 'y'.


I looked over the files and made sure no files that I modified before, were getting replaced. After confirming that, I ran the same command and then selected '**y**' to do the actual install:

    Perform migration and upgrade without previewing configuration changes? [y/n] y

    -- Migration information is being logged to '/opt/splunk/var/log/splunk/migration.log.2014-04-15.12-24-17' --

    Migrating to:
    VERSION=6.0.3
    BUILD=204106
    PRODUCT=splunk
    PLATFORM=FreeBSD-amd64

    Copying '/opt/splunk/etc/myinstall/splunkd.xml' to '/opt/splunk/etc/myinstall/splunkd.xml-migrate.bak'.

    Checking saved search compatibility...

    Checking for possible timezone configuration errors...

    Handling deprecated files...

    Checking script configuration...

    Copying '/opt/splunk/etc/myinstall/splunkd.xml.cfg-default' to '/opt/splunk/etc/myinstall/splunkd.xml'.
    Deleting '/opt/splunk/etc/system/local/field_actions.conf'.
    Moving '/opt/splunk/share/splunk/search_mrsparkle/modules' to '/opt/splunk/share/splunk/search_mrsparkle/modules.old.20140415-122417'.
    Moving '/opt/splunk/share/splunk/search_mrsparkle/modules.new' to '/opt/splunk/share/splunk/search_mrsparkle/modules'.
    Checking for possible UI view conflicts...

    Clustering migration already complete, no further changes required.


    Splunk> Map. Reduce. Recycle.

    Checking prerequisites...
            Checking http port [8000]: open
            Checking mgmt port [8089]: open
            Checking configuration...  Done.
            Checking critical directories...        Done
            Checking indexes...
                    Validated: _audit _blocksignature _internal _thefishbucket history main summary
            Done
            Checking filesystem compatibility...  Done
            Checking conf files for typos...        Done
    All preliminary checks passed.

    Starting splunk server daemon (splunkd)...
    Done

    Starting splunkweb...  Done


    If you get stuck, we're here to help.
    Look for answers here: http://docs.splunk.com

    The Splunk web interface is at http://moxz:8000


That time around it actually applied the update. I logged into splunk and all of the reports and applications that I was using were still working as expected.

 [1]: http://docs.splunk.com/Documentation/Splunk/6.0.3/ReleaseNotes/6.0.3
 [2]: http://docs.splunk.com/Documentation/Splunk/6.0.3/installation/Upgradeto6.0onUNIX
 [3]: /2013/12/installing-splunk-freebsd/
