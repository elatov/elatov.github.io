---
published: true
layout: post
title: "Updating a Port in FreeBSD Ports"
author: Karim Elatov
categories: [os]
tags: [freebsd, ports]
---
I was in need of updating a FreeBSD port and this was the first time I was running through the process so I decided to jot down my process.

## Getting the Source
The overall process is laid out in [Chapter 11. Upgrading a Port](https://docs.freebsd.org/en/books/porters-handbook/upgrading/). I also wanted to use `git` so I also followed the instructions laid out in [11.1. Using Git to Make Patches](https://docs.freebsd.org/en/books/porters-handbook/upgrading/#git-diff) to make my changes. I basically ran the following to get the source:

```bash
> git clone https://git.FreeBSD.org/ports.git freebsd-ports
```

## Switching to Github
The port has since moved to a github repo and FreeBSD ports contains new directives to download source from Github instead of a website. The options are all described in [5.4.3. USE_GITHUB](https://docs.freebsd.org/en/books/porters-handbook/makefiles/#makefile-master_sites-github). After migrating to pull from github we saw the following changes:

```bash
$ git diff 4519b9 4618
diff --git a/net-mgmt/myapp/Makefile b/net-mgmt/myapp/Makefile
index 234ca47a..5b89f106 100644
--- a/net-mgmt/myapp/Makefile
+++ b/net-mgmt/myapp/Makefile
@@ -1,9 +1,8 @@

 PORTNAME=      myapp
-PORTVERSION=   1.2.18
+DISTVERSION=   1.2.19
 CATEGORIES=    net-mgmt
-MASTER_SITES=  https://download.com/myapp/

 MAINTAINER=    you@gmail.com
 COMMENT=       My App
@@ -11,13 +10,17 @@ COMMENT=    My App
 LICENSE=       GPLv2
 LICENSE_FILE=  ${WRKSRC}/COPYING.GPL

 USES=          tar:bzip2
 GNU_CONFIGURE= yes

+USE_GITHUB=    yes
+GH_ACCOUNT=    you
+GH_PROJECT=    myapp
 USE_RC_SUBR=   myapp
```

That's not too bad.

### Generating the distinfo file
This is described in [3.3. Creating the Checksum File](https://docs.freebsd.org/en/books/porters-handbook/quick-porting/#porting-checksum). We just need to run the following:

```bash
export PORTSDIR=~/freebsd-ports
$ make makesum
===>  License GPLv2 accepted by the user
===>  License GPLv2 accepted by the user
===>   myapp-1.2.19 depends on file: /usr/local/sbin/pkg - found
=> you-myapp-1.2.19_GH0.tar.gz doesn't seem to exist in /home/elatov/freebsd-ports/distfiles/.
=> Attempting to fetch https://codeload.github.com/you/myapp/tar.gz/1.2.19?dummy=/you-myapp-1.2.19_GH0.tar.gz
fetch: https://codeload.github.com/you/myapp/tar.gz/1.2.19?dummy=/you-myapp-1.2.19_GH0.tar.gz: size of remote file is not known
you-myapp-1.2.19_GH0.tar.gz                   101 kB  885 kBps    00s
===> Fetching all distfiles required by myapp-1.2.19 for building
```

And you will also see the `distinfo` file updated:

```bash
diff --git a/net-mgmt/myapp/distinfo b/net-mgmt/myapp/distinfo
index 9219ca4b..90cb2abb 100644
--- a/net-mgmt/myapp/distinfo
+++ b/net-mgmt/myapp/distinfo
@@ -1,2 +1,3 @@
-SHA256 (myapp-1.2.18.tar.bz2) = aeaf909585f7f43
-SIZE (myapp-1.2.18.tar.bz2) = 117695
+TIMESTAMP = 1641833619
+SHA256 (you-myapp-1.2.19_GH0.tar.gz) = 371c94cb9c4269e7
+SIZE (you-myapp-1.2.19_GH0.tar.gz) = 103806
```

### Port Formatting and Linting
The [10.2. Portclippy / Portfmt](https://docs.freebsd.org/en/books/porters-handbook/testing/#testing-portclippy) and [10.3. Portlint](https://docs.freebsd.org/en/books/porters-handbook/testing/#testing-portlint) pages have instructions on how to make sure the formatting of the `Makefile` are correct correct. So let's run those:

```bash
> sudo pkg install portfmt portlint
```

Then you can run them to make sure the formatting of the `Makefile` is good. After following the instructions and fixing everything, here is how my end result looked like:

```bash
$ portfmt -i Makefile
$ portlint -A
WARN: Consider to set DEVELOPER=yes in /etc/make.conf
0 fatal errors and 1 warning found.
```
You can also use `portfmt` without the `-i` flag to see what changes are made to the `Makefile`.

### Switching to autoconf
Before the source would contain all the `configure` scripts but now we have the source and we need to run `autoconf` and `autoheader` to generate the `configure` scripts. Luckily the build system contains a built step for this, it's [17.4. autoreconf](https://docs.freebsd.org/en/books/porters-handbook/uses/#uses-autoreconf). After modifying the `Makefile`, here is how it looked like:

```bash
-USES=          tar:bzip2
+USES=          autoreconf
 GNU_CONFIGURE= yes
```

Initially running a `make stage`, I received the following error:

```bash
$ make stage
===>  License GPLv2 accepted by the user
===>   myapp-1.2.19 depends on file: /usr/local/sbin/pkg - found
=> you-myapp-1.2.19_GH0.tar.gz doesn't seem to exist in /home/elatov/freebsd-ports/distfiles/.
=> Attempting to fetch https://codeload.github.com/you/myapp/tar.gz/1.2.19?dummy=/you-myapp-1.2.19_GH0.tar.gz
fetch: https://codeload.github.com/you/myapp/tar.gz/1.2.19?dummy=/you-myapp-1.2.19_GH0.tar.gz: size unknown
fetch: https://codeload.github.com/you/myapp/tar.gz/1.2.19?dummy=/you-myapp-1.2.19_GH0.tar.gz: size of remote file is not known
you-myapp-1.2.19_GH0.tar.gz                   101 kB   33 kBps    03s
===> Fetching all distfiles required by myapp-1.2.19 for building
===>  Extracting for myapp-1.2.19
=> SHA256 Checksum OK for you-myapp-1.2.19_GH0.tar.gz.
===>  Patching for myapp-1.2.19
===>   myapp-1.2.19 depends on package: autoconf>=2.69 - found
===>   myapp-1.2.19 depends on package: automake>=1.16.1 - found
===>  Configuring for myapp-1.2.19
configure.ac:2: error: Autoconf version 2.71 or higher is required
configure.ac:2: the top level
```

It looks like version 2.71 of `autoconf` is not in ports yet and [there is a bug](https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=258046) to eventually add it. So I decided to modify the source to not depend on that version:

```bash
+post-extract:
+       ${REINPLACE_CMD} -e 's/2.71/2.69/g' ${WRKSRC}/configure.ac
+
```

And then the build succeeded:

```bash
$ make stage
===>  License GPLv2 accepted by the user
===>   myapp-1.2.19 depends on file: /usr/local/sbin/pkg - found
===> Fetching all distfiles required by myapp-1.2.19 for building
===>  Extracting for myapp-1.2.19
=> SHA256 Checksum OK for you-myapp-1.2.19_GH0.tar.gz.
/usr/bin/sed -i.bak -e 's/2.71/2.69/g' /usr/home/elatov/freebsd-ports/net-mgmt/myapp/work/myapp-1.2.19/configure.ac
===>  Patching for myapp-1.2.19
===>   myapp-1.2.19 depends on package: autoconf>=2.69 - found
===>   myapp-1.2.19 depends on package: automake>=1.16.1 - found
===>  Configuring for myapp-1.2.19
...
...
===>  Staging for myapp-1.2.19
===>   Generating temporary packing list
/usr/bin/install -c -d /usr/home/elatov/freebsd-ports/net-mgmt/myapp/work/stage/usr/local/sbin
====> Compressing man pages (compress-man)
===> Staging rc.d startup script(s)
```

### Testing the Port
From [3.4. Testing the Port](https://docs.freebsd.org/en/books/porters-handbook/quick-porting/#porting-testing), here are the commands we need to run:

```bash
$ make package
===>  Building package for myapp-1.2.19
elatov@moxz:~/freebsd-ports/net-mgmt/myapp $ make install
===>  Installing for myapp-1.2.19
===>  Checking if myapp is already installed
===>  Switching to root credentials for 'install' target
## Run the new application to test and make it's working as expected
##
elatov@moxz:~/freebsd-ports/net-mgmt/myapp $ sudo /usr/local/sbin/myapp
elatov@moxz:~/freebsd-ports/net-mgmt/myapp $ make deinstall
===>  Switching to root credentials for 'deinstall' target
Password:
===>  Deinstalling for myapp
===>   Deinstalling myapp-1.2.19
Updating database digests format: 100%
Checking integrity... done (0 conflicting)
Deinstallation has been requested for the following 1 packages (of 0 packages in the universe):

Installed packages to be REMOVED:
        myapp: 1.2.19

Number of packages to be removed: 1
[1/1] Deinstalling myapp-1.2.19...
[1/1] Deleting files for myapp-1.2.19: 100%
===>  Returning to user credentials
```

### Generate Patch for Port
If all is well you should be ready to prepare a patch to be submitted as described in [11.1. Using Git to Make Patches](https://docs.freebsd.org/en/books/porters-handbook/upgrading/#git-diff). Let's create a branch:

```bash
> git pull
> git checkout -b my_branch
```

If you took a while between the latest pull and making your patch, make sure you get the latest source:

```bash
$ git fetch origin main
remote: Enumerating objects: 312, done.
remote: Counting objects: 100% (312/312), done.
remote: Compressing objects: 100% (183/183), done.
remote: Total 186 (delta 125), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (186/186), 23.76 KiB | 7.92 MiB/s, done.
Resolving deltas: 100% (125/125), completed with 92 local objects.
From https://git.FreeBSD.org/ports
 * branch                      main       -> FETCH_HEAD
   4519b9e81473..f42f32be2db8  main       -> origin/main
$ git rebase origin/main
Successfully rebased and updated refs/heads/my_branch.
```

And commit the changes to your branch:

```bash
> git add .
> git commit
```

The format of the commit message is described in [5.2.7.1. Commit message formats](https://docs.freebsd.org/zh-tw/books/porters-handbook/upgrading/). Then create the patch:

```bash
> git format-patch main
```

That will create a file in the local directory (in the format of `0001-foo.patch`) and when you create [a bug](https://bugs.freebsd.org/submit/) to update the port, you will attach it to that bug. The steps to create the bug are laid out in [Chapter 11. Upgrading a Port](https://docs.freebsd.org/en/books/porters-handbook/upgrading/). Then that you just hope your change will be added to the ports after appropriate review.
