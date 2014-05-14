---
title: Creating an IPS Repository for OminiOS
author: Jarret Lavallee
layout: post
permalink: /2013/03/creating-an-ips-repository-for-ominios/
dsq_thread_id:
  - 1409123643
categories:
  - OS
tags:
  - IPS
  - irssi
  - OmniOS
---
Recently I moved to OmniOS from Nexenta Core Platform (NCP). I really liked NCP because of the package manager (**apt-get**) and the community had repos for common software. In OmniOS I find that the core has more updates than NCP, but there are very few packages in the repositories. So I end up building some software from source. This works fine, but it adds a manual component for doing any upgrade or package management. I decided to create an <a href="http://docs.oracle.com/cd/E19963-01/html/820-6572/managepkgs.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.oracle.com/cd/E19963-01/html/820-6572/managepkgs.html']);">IPS repo</a>. There is not a lot of software in it and there will not be many updates, but the local repo will help with the management.

## Creating a PKG Repository for OmniOS

<a href="http://omnios.omniti.com/wiki.php/CreatingRepos" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://omnios.omniti.com/wiki.php/CreatingRepos']);">This guide</a> goes over many of the steps to building the repo.

First create a filesystem for the repo.

    jarret@megatron:~$ sudo zfs create data/repo
    

Create the repo and set the settings.

    jarret@megatron:~$ sudo pkgrepo create /data/repo/
    jarret@megatron:~$ sudo pkgrepo set -s /data/repo publisher/prefix=repo.moopless.com
    jarret@megatron:~$ sudo pkgrepo info -s /data/repo/
    PUBLISHER         PACKAGES STATUS           UPDATED
    repo.moopless.com 0        online           2013-03-18T15:22:39.444312Z
    

Set up the web services so the repo can be accessed externally. If I do allow this for external access, it will be behind a reverse proxy on another server in my DMZ.

    jarret@megatron:~$ sudo svcadm disable pkg/server
    jarret@megatron:~$ sudo svccfg -s pkg/server setprop pkg/inst_root = /data/repo
    jarret@megatron:~$ sudo svccfg -s pkg/server setprop pkg/port = 10000
    jarret@megatron:~$ sudo svcadm refresh pkg/server
    jarret@megatron:~$ sudo svcadm enable pkg/server
    

Now the repo is setup and ready to go, but we have no packages. We can pull packages from other repos, but for this one I want to build extraneous software like *irssi*.

## Building packages

There are some good instructions on creating packages that can be <a href="http://omnios.omniti.com/wiki.php/PackagingForOmniOS" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://omnios.omniti.com/wiki.php/PackagingForOmniOS']);">found here</a>.

Before we build the packages, we need to get the package metadata and put it into a build space. I am going to build all of these packages on a separate filesystem. First I will create another filesystem.

    jarret@megatron:~$ sudo zfs create data/scratch/packages
    

Now we can **cd** into that directory and clone the version of the package template, but we need to install **git**

    jarret@megatron:/data/scratch/packages$ sudo pkg install git
    jarret@megatron:/data/scratch/packages$ git clone git://github.com/omniti-labs/omnios-build.git
    jarret@megatron:/data/scratch/packages$ cd omnios-build
    jarret@megatron:/data/scratch/packages$ git checkout template
    

Let&#8217;s configure the *omnios-build* environment that we just cloned. Edit the *lib/config.sh* file and configure it to your environment. I changed the following:

    PREFIX=/usr/local
    TMPDIR=/data/scratch/packages/build_$USER
    

Next we will edit the *lib/site.sh* file to match our site configuration.

    PKGPUBLISHER=repo.moopless.com
    PKGSRVR=file:///data/repo/
    

There are many more settings that can be customized.

### Building irssi

**irssi** is an excellent IRC client that is not currently in the repos. It is uses Perl and is an easy install to start on.

We need to create a new template for irssi so we can run the **new.sh** script to create the build environment for our package:

    jarret@megatron:/data/scratch/packages$ ./new.sh irssi
    Creating new basic build script under ./build/irssi
    jarret@megatron:/data/scratch/packages$ ls build/irssi/
    build.sh  patches
    

The irssi build directory has been created and template files have been added for us to modify. The *build.sh* file is a script that is called to build the package. It contains all of the configuration that we will need to change for this package. Edit the *build/irssi/build.sh* script. The contents below are from my *build.sh*.

    . ../../lib/functions.sh
    
    PROG=irssi
    VER=0.8.15
    PKG=network/irssi
    SUMMARY="$PROG - IRC client with IPv6, proxy, bot, socks and Perl support"
    DESC="$SUMMARY"
    
    DEPENDS_IPS="runtime/perl \
                 library/glib2 \
                 library/ncurses \
                 system/pkg-config"
    
    LDFLAGS=""
    CFLAGS64="$CFLAGS64 -I/usr/include/amd64"
    CONFIGURE_OPTS="--enable-ipv6 \
        --with-socks \
        --with-bot \
        --with-proxy \
        --with-perl=yes \
        --with-perl-lib=vendor \
        --with-ncurses=/usr"
    
    save_function configure32 configure32_orig
    configure32() {
        make_param configure
        configure32_orig
    }
    
    save_function configure64 configure64_orig
    configure64() {
        make_param configure
        configure64_orig
    }
    
    init
    download_source $PROG $PROG $VER
    patch_source
    prep_build
    build
    make_isa_stub
    make_package
    clean_up
    

After saving the **build.sh**, we can run it to build the software. The only problem is that it will fail to download the source. By default the script will look at ** for the software packages. Before it looks on that server, it will look for the local package in the temp directory. So the easiest way to get the package is to download it into the build directory before running **build.sh**.

    jarret@megatron:/data/scratch/packages/build_jarret$ wget http://www.irssi.org/files/irssi-0.8.15.tar.gz
    

Let&#8217;s try to build the package. If there is a problem with the build, check the build.log for additional details.

    jarret@megatron:/data/scratch/packages$ cd ../build/irssi/
    jarret@megatron:/data/scratch/packages/build/irssi$ ./build.sh
    ===== Build started at Mon Mar 18 16:22:23 EDT 2013 =====
    Package name: network/irssi
    Selected flavor: None (use -f to specify a flavor)
    Selected build arch: both
    Extra dependency: None (use -d to specify a version)
    Verifying dependencies
    Checking for source directory
    --- Source directory not found
    Checking for irssi source archive
    --- irssi source archive found
    Extracting archive: irssi-0.8.15.tar.gz
    Checking for patches in patches/ (in order to apply them)
    --- No series file (list of patches) found
    --- Not applying any patches
    Preparing for build
    --- Creating temporary install dir
    Building 32-bit
    --- make (dist)clean
    --- *** WARNING *** make (dist)clean Failed
    --- make configure
    --- configure (32-bit)
    --- make
    --- make install
    Building 64-bit
    --- make (dist)clean
    --- make configure
    --- configure (64-bit)
    --- make
    --- make install
    Making isaexec stub binaries
    --- bin
    ------ botti
    ------ irssi
    Making package
    --- Generating package manifest from /data/scratch/packages/build_jarret/network_irssi_pkg
    ------ Running: /usr/bin/pkgsend generate /data/scratch/packages/build_jarret/network_irssi_pkg > /data/scratch/packages/build_jarret/network_irssi.p5m.int
    --- Generating package metadata
    ------ Adding dependencies
    --- Applying transforms
    --- Publishing package
    Intentional pause: Last chance to sanity-check before publication!
    Do you wish to continue anyway? (y/n)
    

At this point the package has been built and it is asking us if we want to push the package to the repo. Before we do that we should test the package and make sure it is actually working correctly. Open up a new screen tab or a new window and **cd** into the temp build space. You should see files similar to the ones below.

    jarret@megatron:/scratch/packages/build_jarret$ ls
    irssi-0.8.15
    irssi-0.8.15.tar.gz
    network_irssi.mog
    network_irssi.p5m
    network_irssi.p5m.int
    network_irssi_pkg
    

The *network\_irssi\_pkg* is the package that we want to test. It is called *network_irssi* because that is what we defined the package to be in the build script. **cd** into the *network\_irssi\_pkg/usr/local/bin* folder and test the binaries.

    jarret@megatron:/scratch/packages/build_jarret/network_irssi_pkg/usr/local/bin$ ./irssi
    

At this point you would see irssi start. Try connecting to *chat.freenode.net* by typing **/connect chat.freenode.net**. Next you should join our channel by typing **/join #virtuallyhyper**. Feel free to say hello. You can quit the software by typing **/quit**.

Now that we know that irssi works correctly, we can go back to the original window and type **y** to publish the package to our local repo.

    Do you wish to continue anyway? (y/n) y
    ===== User elected to continue after prompt. =====
    --- Published network/irssi@0.8.15,5.11-0.151005
    Cleaning up
    --- Removing temporary install directory /data/scratch/packages/build_jarret/network_irssi_pkg
    --- Cleaning up temporary manifest and transform files
    Done.
    

Before we can see the package on the repo, we need to refresh it.

    jarret@megatron:~$ pkgrepo refresh -s/data/repo/
    

Let&#8217;s add our local repo.

    jarret@megatron:~$ pkg set-publisher -g http://localhost:10000 repo.moopless.com
    

Now we can check the repo for our package.

    jarret@megatron:~$ pkg list -g http://localhost:10000
    NAME (PUBLISHER)                                  VERSION                    IFO
    network/irssi (repo.moopless.com)                 0.8.15-0.151005            i--
    

Since it is on there, we can now install it.

    jarret@megatron:~$ pkg install irssi
    

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Installing and Configuring Fail2Ban on OmniOS" href="http://virtuallyhyper.com/2013/04/installing-and-configuring-fail2ban-on-omnios/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/04/installing-and-configuring-fail2ban-on-omnios/']);" rel="bookmark">Installing and Configuring Fail2Ban on OmniOS</a>
    </li>
  </ul>
</div>

