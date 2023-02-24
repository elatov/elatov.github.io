---
published: true
layout: post
title: "Building a Nix Package"
author: Karim Elatov
categories: [automation,os]
tags: [nix, nixos, git]
---
# Building a Package for NixOS
There are definitely a bunch of steps and I will just run through them as I discover them.

## Building with Nix
Nix by it self allows for building packages without using the community driven [nixpkgs](https://github.com/NixOS/nixpkgs). There are some nice examples that shows you the basic setup:

- [Working Derivation -> Enough of nix repl](https://nixos.org/guides/nix-pills/working-derivation.html#idm140737320271904)
- [Your First Derivation](https://github.com/justinwoo/nix-shorts/blob/master/posts/your-first-derivation.md)
- [nixpkgs/pkgs/applications/misc/hello/](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/misc/hello/default.nix)
- [How to Learn Nix, Part 11: Okay my actual first derivation](https://ianthehenry.com/posts/how-to-learn-nix/okay-my-actual-first-derivation/)

Nix uses a term **derivation** which is basically a built package that is reproducible, almost like flatpak or snap.
If you want to build your package you can create a nix file which represents your build. For example from the
last link, here is a simple `.nix` file:

```bash
{ lib
, stdenv
, fetchurl
, testVersion
, hello
}:

stdenv.mkDerivation rec {
  pname = "hello";
  version = "2.10";

  src = fetchurl {
    url = "mirror://gnu/hello/${pname}-${version}.tar.gz";
    sha256 = "0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i";
  };

  doCheck = true;

  passthru.tests.version =
    testVersion { package = hello; };

  meta = with lib; {
    description = "A program that produces a familiar, friendly greeting";
    longDescription = ''
      GNU Hello is a program that prints "Hello, world!" when you run it.
      It is fully customizable.
    '';
    homepage = "https://www.gnu.org/software/hello/manual/";
    changelog = "https://git.savannah.gnu.org/cgit/hello.git/plain/NEWS?h=v${version}";
    license = licenses.gpl3Plus;
    maintainers = [ maintainers.eelco ];
    platforms = platforms.all;
  };
}
```

This basically downloads the tar file for [gnu hello](https://www.gnu.org/software/hello/manual/) and builds it. If you want to build it out of `nixpkgs`,
there are some extra steps. For example if you try and build that file, here is what you would get:

```bash
> nix-build default.nix
error: cannot auto-call a function that has an argument without a default value ('lib')
```

This is expected since you need to import the main *nixpkgs* first, this is discussed in:

- [Manual's build example doesn't build](https://github.com/NixOS/nix/issues/2259)
- [Building a Nix Package (The C&C++ Version)](https://gist.github.com/CMCDragonkai/41593d6d20a5f7c01b2e67a221aa0330)
- [[Nix-dev] error: cannot auto-call a function that has an argument without a default value (‘stdenv’)](https://releases.nixos.org/nix-dev/2017-July/024061.html)

So we can build it like this:

```bash
> nix-build -E 'with import <nixpkgs> {}; callPackage ./default.nix {}'
these paths will be fetched (0.04 MiB download, 0.20 MiB unpacked):
  /nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10
copying path '/nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10' from 'https://cache.nixos.org'...
/nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10
```
When the build is finished it prints out the location of the derivation in the [nix store](https://nixos.wiki/wiki/Nix#Nix_store). We can get more information about the package/derivation, by running `nix show-derivation`:

```bash
> nix show-derivation /nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10
{
  "/nix/store/8dr2lhv3kriyw8qhg66dszr0vl3grxya-hello-2.10.drv": {
    "outputs": {
      "out": {
        "path": "/nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10"
      }
    },
    "inputSrcs": [
      "/nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25b-default-builder.sh"
    ],
```

And you can check out the files in the derivation:

```bash
> tree -L 2 /nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10
/nix/store/03y8h6wim78853illk0ylj5v0sy8r5fc-hello-2.10
├── bin
│   └── hello
└── share
    ├── info
    ├── locale
    └── man

5 directories, 1 file
```

So that's a simple example on how to build an existing package. So let's create our own.

## Creating our own nix file
There are a couple of sections, here are the ones I worked on. I wanted to build the new fork of the [fwbuilder](https://github.com/fwbuilder/fwbuilder) application, which uses `cmake` to build it's source. It also uses QT5 for it's UI which actually ended up adding more steps. But from the git page here are the steps to compile the software:

```bash
> sudo apt install git cmake libxml2-dev libxslt-dev libsnmp-dev qt5-default qttools5-dev-tools
> git clone https://github.com/fwbuilder/fwbuilder.git
> mkdir build
> cd build
> cmake ../fwbuilder
> make
> sudo make install
```

So let's convert to the nix.

### Filling out Package info and Meta Attributes
When creating a package we have to include the package information and also where to download it from. Most of the information is covered in [Meta-attributes](https://nixos.org/manual/nixpkgs/stable/#chap-meta), the most challenging was getting the hash, I found some good examples:

- [Building a Nix Package (The C&C++ Version)](https://gist.github.com/CMCDragonkai/41593d6d20a5f7c01b2e67a221aa0330)
- [How to manually replicate/reproduce/obtain the sha256 hash specified in Nix with fetchgit or fetchFromGitHub?](https://github.com/NixOS/nix/issues/1880)
- [Fetching Sources](https://nixos.org/manual/nixpkgs/stable/#sec-sources)

You can either use `nix-prefetch-git`:

```bash
> nix-prefetch-git --url https://github.com/fwbuilder/fwbuilder --rev "v6.0.0-rc1"
Initialized empty Git repository in /tmp/git-checkout-tmp-uLFtVCZd/fwbuilder/.git/
remote: Enumerating objects: 2941, done.
remote: Counting objects: 100% (2941/2941), done.
remote: Compressing objects: 100% (2450/2450), done.
remote: Total 2941 (delta 1347), reused 1204 (delta 468), pack-reused 0
Receiving objects: 100% (2941/2941), 6.75 MiB | 1.13 MiB/s, done.
Resolving deltas: 100% (1347/1347), done.
From https://github.com/fwbuilder/fwbuilder
 * tag               v6.0.0-rc1 -> FETCH_HEAD
Switched to a new branch 'fetchgit'
removing `.git'...

git revision is ea25d1e557d45d10d4354cf1435633b5d37edf3d
path is /nix/store/hf58z7sc7wkdxkpylr529370inhyb9sj-fwbuilder
git human-readable version is -- none --
Commit date is 2021-01-04 00:47:14 +0100
hash is 015pbi6jmqddqmma3ary5igi5nm2294ai0fkdg1dvaraq8cy74cg
{
  "url": "https://github.com/fwbuilder/fwbuilder",
  "rev": "ea25d1e557d45d10d4354cf1435633b5d37edf3d",
  "date": "2021-01-04T00:47:14+01:00",
  "path": "/nix/store/hf58z7sc7wkdxkpylr529370inhyb9sj-fwbuilder",
  "sha256": "015pbi6jmqddqmma3ary5igi5nm2294ai0fkdg1dvaraq8cy74cg",
  "fetchLFS": false,
  "fetchSubmodules": false,
  "deepClone": false,
  "leaveDotGit": false
}
```

or `nix hash-path`:

```bash
> git clone git@github.com:fwbuilder/fwbuilder.git /tmp/fwbuilder
Cloning into '/tmp/fwbuilder'...
remote: Enumerating objects: 68296, done.
remote: Counting objects: 100% (166/166), done.
remote: Compressing objects: 100% (121/121), done.
remote: Total 68296 (delta 89), reused 90 (delta 43), pack-reused 68130
Receiving objects: 100% (68296/68296), 25.33 MiB | 5.91 MiB/s, done.
Resolving deltas: 100% (57731/57731), done.
> mv /tmp/fwbuilder/.git /tmp/.
> nix hash-path /tmp/fwbuilder
sha256-j5HjGcIqq93Ca9OBqEgSotoSXyw+q6Fqxa3hKk1ctwQ=
```

Don't forget to add a `maintainer` field, if this is your first package you will have to add yourself to the `maintainers` file as described in [maintainers](https://nixos.org/manual/nixpkgs/stable/#var-meta-maintainers). 

After it was all said and done, I had the following sections:

```bash
stdenv.mkDerivation rec {
  pname = "fwbuilder";
  version = "6.0.0-rc1";

  meta = with lib; {
    description = "GUI Firewall Management Application";
    homepage    = "https://github.com/fwbuilder/fwbuilder";
    license     = licenses.gpl2;
    platforms   = platforms.linux;
    maintainers = [ maintainers.elatov ];
  };

  src = fetchFromGitHub {
    owner = "fwbuilder";
    repo = "fwbuilder";
    rev = "v${version}";
    hash = "sha256-j5HjGcIqq93Ca9OBqEgSotoSXyw+q6Fqxa3hKk1ctwQ=";
  };
```

### Building a QT package locally
Trying to build a qt5 package using `cmake` as a compile tool in nix had some caveats. There are nice instructions in [Nixpkgs Manual -> QT](https://nixos.org/manual/nixpkgs/stable/#sec-language-qt). We can include `wrapQtAppsHook`, here is the example:

```bash
{ stdenv, lib, qtbase, wrapQtAppsHook }: 

stdenv.mkDerivation {
  pname = "myapp";
  version = "1.0";

  buildInputs = [ qtbase ];
  nativeBuildInputs = [ wrapQtAppsHook ]; 
}
```

On top of that, if you remember we usually have to run this to build a package:

```bash
nix-build -E 'with import <nixpkgs> {}; callPackage ./default.nix {}'
```

It looks like qt5 packages are called in a specific way and this is discussed in:

- [wrapQtAppsHook out of tree?](https://discourse.nixos.org/t/wrapqtappshook-out-of-tree/5619)
- [QT -> Packaging](https://nixos.wiki/wiki/Qt#Packaging)
- [Adding an application to Nixpkgs](https://nixos.org/manual/nixpkgs/stable/#adding-an-application-to-nixpkgs)

so the command becomes the following:

```bash
> nix-build -K -E 'with import <nixpkgs> {}; libsForQt5.callPackage ./default.nix {}'
...
...
stripping (with command strip and flags -S) in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1/bin
patching script interpreter paths in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1
checking for references to /build/ in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1...
postPatchMkspecs
/nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1
```

Without specifying `libsForQt5`, would yield the following failures for me:

```bash
> nix-build -K -E 'with import <nixpkgs> {}; callPackage ./default.nix {}'
these derivations will be built:
  /nix/store/9nc24fa3han4ir6w00v7g852y13l3qhw-fwbuilder-6.0.0-rc1.drv
building '/nix/store/9nc24fa3han4ir6w00v7g852y13l3qhw-fwbuilder-6.0.0-rc1.drv'...
unpacking sources
unpacking source archive /nix/store/npmsrjmp42831nn10n4g2d8p3xn7k0l6-source
source root is source
patching sources
configuring
fixing cmake files...
cmake flags: -DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF -DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF -DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_SKIP_BUILD_RPATH=ON -DBUILD_TESTING=OFF -DCMAKE_INSTALL_LOCALEDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/share/locale -DCMAKE_INSTALL_LIBEXECDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/libexec -DCMAKE_INSTALL_LIBDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/lib -DCMAKE_INSTALL_DOCDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/share/doc/firewallbuilder -DCMAKE_INSTALL_INFODIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/share/info -DCMAKE_INSTALL_MANDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/share/man -DCMAKE_INSTALL_OLDINCLUDEDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/include -DCMAKE_INSTALL_INCLUDEDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/include -DCMAKE_INSTALL_SBINDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/sbin -DCMAKE_INSTALL_BINDIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/bin -DCMAKE_INSTALL_NAME_DIR=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1/lib -DCMAKE_POLICY_DEFAULT_CMP0025=NEW -DCMAKE_OSX_SYSROOT= -DCMAKE_FIND_FRAMEWORK=LAST -DCMAKE_STRIP=/nix/store/gkzmfpb04ddb7phzj8g9sl6saxzprssg-gcc-wrapper-10.3.0/bin/strip -DCMAKE_RANLIB=/nix/store/rbqplhv2s539liymkvm3zbjj9lvgzpd5-binutils-2.35.2/bin/ranlib -DCMAKE_AR=/nix/store/rbqplhv2s539liymkvm3zbjj9lvgzpd5-binutils-2.35.2/bin/ar -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DCMAKE_INSTALL_PREFIX=/nix/store/qn6mpq7ns3cyzlpcmyrd0r5kcz1zgaiy-fwbuilder-6.0.0-rc1
-- The CXX compiler identification is GNU 10.3.0
-- The C compiler identification is GNU 10.3.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /nix/store/gkzmfpb04ddb7phzj8g9sl6saxzprssg-gcc-wrapper-10.3.0/bin/g++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /nix/store/gkzmfpb04ddb7phzj8g9sl6saxzprssg-gcc-wrapper-10.3.0/bin/gcc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
CMake Error at CMakeLists.txt:32 (find_package):
  By not providing "FindQt5Widgets.cmake" in CMAKE_MODULE_PATH this project
  has asked CMake to find a package configuration file provided by
  "Qt5Widgets", but CMake did not find one.
``` 

So in the end my `nix` file looked like this:

```bash
> cat default.nix
{ stdenv, lib, fetchFromGitHub, cmake, qtbase, wrapQtAppsHook }:

stdenv.mkDerivation rec {
  pname = "fwbuilder";
  version = "6.0.0-rc1";

  meta = with lib; {
    description = "GUI Firewall Management Application";
    homepage    = "https://github.com/fwbuilder/fwbuilder";
    license     = licenses.gpl2;
    platforms   = platforms.linux;
    maintainers = [ maintainers.elatov ];
  };

  src = fetchFromGitHub {
    owner = "fwbuilder";
    repo = "fwbuilder";
    rev = "v${version}";
    hash = "sha256-j5HjGcIqq93Ca9OBqEgSotoSXyw+q6Fqxa3hKk1ctwQ=";
  };

  nativeBuildInputs = [
    cmake
    wrapQtAppsHook
  ];
}
```

After it's built, you can run it manually:

```bash
> ./result/bin/fwbuilder
```

Here is how mine looked like after it started:

![fwbuilder-built.png](https://res.cloudinary.com/elatov/image/upload/v1640976795/blog-pics/nixos-build-pkg/fwbuilder-built.png)

Or you can actually add it to your system like this (this is discussed in [Adding Custom Packages](https://nixos.org/manual/nixos/stable/index.html#sec-customising-packages)):

```bash
(pkgs.libsForQt5.callPackage /data/work/nix-build/default.nix {})
```

And then it will be added to the system not just the user:

```bash
> type -a fwbuilder
fwbuilder is /run/current-system/sw/bin/fwbuilder
```

### Redoing a build
Just in case I ran into [How to undo nix-build?](https://discourse.nixos.org/t/how-to-undo-nix-build/5433), and it looks like the best way to do that is:

```bash
> unlink result
> nix-store --delete /nix/store/9j0x8yvi1y8aajiggahxqvmlsf9wpnvk-fwbuilder-6.0.0-rc1
```

Then you can run another build.

## Contributing to nixpkgs

There are a bunch of good sites that cover the topic:

- [Quick Start to Adding a Package](https://nixos.org/manual/nixpkgs/stable/#chap-quick-start)
- [Nixpkgs/Create and debug packages](https://nixos.wiki/wiki/Nixpkgs/Create_and_debug_packages)
- [How to contribute](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md)
- [Nixpkgs/Contributing](https://nixos.wiki/wiki/Nixpkgs/Contributing)


Use `gh` to fork and clone the originial **nixpkgs** repo:

```bash
> gh auth login --web
> cd /data/work
> gh repo fork https://github.com/NixOS/nixpkgs.git --clone
```

Create a branch:

```
> cd nixpkgs
> git checkout -b pkg/fwbuilder
Switched to a new branch 'pkg/fwbuilder'
```

Let's create our package directory:

```
> mkdir tools/security/fwbuilder
> cp ../../nix-build/default.nix tools/security/fwbuilder/.
```

Now let's add into all the packages:

```bash
# check sections of the file
> grep '^  ###' pkgs/top-level/all-packages.nix
  ### Helper functions.
  ### Evaluating the entire Nixpkgs naively will fail, make failure fast
  ### Nixpkgs maintainer tools
  ### Push NixOS tests inside the fixed point
  ### BUILD SUPPORT
  ### TOOLS
  ### APPLICATIONS/TERMINAL-EMULATORS
> vi pkgs/top-level/all-packages.nix
```

Here is my quick change:

```bash
> git --no-pager diff pkgs/top-level/all-packages.nix
diff --git a/pkgs/top-level/all-packages.nix b/pkgs/top-level/all-packages.nix
index 482f17ce47e..b0fc1f36ef7 100644
--- a/pkgs/top-level/all-packages.nix
+++ b/pkgs/top-level/all-packages.nix
@@ -1007,6 +1007,8 @@ with pkgs;

   godspeed = callPackage ../tools/networking/godspeed { };

+  fwbuilder = libsForQt5.callPackage ../tools/security/fwbuilder { };
+
   ksnip = libsForQt5.callPackage ../tools/misc/ksnip { };

   linux-router = callPackage ../tools/networking/linux-router { };
```

### Staying up to date with Fork
This is covered in:

- [Tracking upstream changes and avoiding extra rebuilding](https://nixos.wiki/wiki/Nixpkgs/Create_and_debug_packages#Tracking_upstream_changes_and_avoiding_extra_rebuilding)
- [Maintain your nixpkgs fork](https://nixos.wiki/wiki/Nixpkgs/Contributing#Maintain_your_nixpkgs_fork)

If you take too long you can run the following to get new changes from the upstream fork repo:

```bash
> git remote add upstream https://github.com/NixOS/nixpkgs.git
> git fetch upstream
remote: Enumerating objects: 34, done.
remote: Counting objects: 100% (29/29), done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 34 (delta 16), reused 20 (delta 13), pack-reused 5
Unpacking objects: 100% (34/34), 20.05 KiB | 2.86 MiB/s, done.
From https://github.com/NixOS/nixpkgs
   389f770a20a..092196f12f5  master            -> upstream/master
   8d373df05fb..f6dc47d9d8e  nixos-21.11-small -> upstream/nixos-21.11-small
   f6dc47d9d8e..24677d5db71  release-21.11     -> upstream/release-21.11
> git rebase upstream/master
Successfully rebased and updated refs/heads/pkg/fwbuilder.
```

If you want you can do the same thing to the master branch:

```bash
> git checkout master
Switched to branch 'master'
> git fetch upstream
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 7 (delta 1), reused 1 (delta 1), pack-reused 1
Unpacking objects: 100% (7/7), 132.91 KiB | 1.27 MiB/s, done.
From https://github.com/NixOS/nixpkgs
   8dd46a932cb..64f9d50edff  master     -> upstream/master
> git rebase upstream/master
Successfully rebased and updated refs/heads/master.
```

### Test it locally
This is covered in [How to install from the local repository](https://nixos.wiki/wiki/Nixpkgs/Create_and_debug_packages#How_to_install_from_the_local_repository). Set the location of the checked out code:

```bash
> export NIXPKGS=/data/work/nixpkgs
```

Let's make sure we can find the package:

```bash
> nix-env -f $NIXPKGS -qaP '*' | grep fwbu
fwbuilder                                        fwbuilder-6.0.0-rc1
```

Now let's make sure we can build the package (notice this time we didn't have run any special imports):

```bash
> cd /tmp
> nix-build $NIXPKGS -A fwbuilder
...
...
stripping (with command strip and flags -S) in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1/bin
patching script interpreter paths in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1
checking for references to /build/ in /nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1...
postPatchMkspecs
/nix/store/ml7qlsssic0q7ji856bhms9x8s6y1rw7-fwbuilder-6.0.0-rc1
```

And you will see the same binaries built:

```bash
> ls result/bin
fwbedit     fwb_ipf   fwb_ipt       fwb_nxosacl  fwb_pix           fwbuilder
fwb_iosacl  fwb_ipfw  fwb_junosacl  fwb_pf       fwb_procurve_acl
```

Confirm they work to make sure the build is good.

### Commit changes to your branch
Now we can commit the change, let's make sure the changes are the ones we made/desire:

```bash
> git status
On branch pkg/fwbuilder
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   pkgs/top-level/all-packages.nix

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	pkgs/tools/security/fwbuilder/

no changes added to commit (use "git add" and/or "git commit -a")
```

This is expected, let's add them:

```bash
> git add .
> git commit -m "fwbuilder: init at 6.0.0-rc1"
```

Now let's push our branch:

```bash
 > git push --set-upstream origin pkg/fwbuilder
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 12 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 1.06 KiB | 1.06 MiB/s, done.
Total 9 (delta 6), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (6/6), completed with 6 local objects.
remote:
remote: Create a pull request for 'pkg/fwbuilder' on GitHub by visiting:
remote:      https://github.com/elatov/nixpkgs/pull/new/pkg/fwbuilder
remote:
To github.com:elatov/nixpkgs.git
 * [new branch]              pkg/fwbuilder -> pkg/fwbuilder
Branch 'pkg/fwbuilder' set up to track remote branch 'pkg/fwbuilder' from 'origin'.
```

Then we can go to github and open up a pull request against the [nixpkg repo](https://github.com/NixOS/nixpkgs).

### Adding maintainers
As I mentioned above, if this is the first package you are adding to the [nixpkg repo](https://github.com/NixOS/nixpkgs),
you will need to add yourself to the `nixpkgs/maintainers/maintainer-list.nix` file, it's in the following format:

```bash
handle = {
  # Required
  name = "Your name";
  email = "address@example.org";
  # Optional
  matrix = "@user:example.org";
  github = "GithubUsername";
  githubId = your-github-id;
  keys = [{
    longkeyid = "rsa2048/0x0123456789ABCDEF";
    fingerprint = "AAAA BBBB CCCC DDDD EEEE  FFFF 0000 1111 2222 3333";
  }];
};
```

I didn't know how to get the `githubId` and apparently it's available at:

```bash
https://api.github.com/users/<userhandle>
```

After you submit the pull request, hope for the best :) Also since there are so many pull requests sometimes these get lost in the process. If that happens post a message at the [PRs ready for review discourse channel](https://discourse.nixos.org/t/prs-ready-for-review) and someone will help out.
