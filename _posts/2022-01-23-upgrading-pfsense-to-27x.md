---
published: true
layout: post
title: "Upgrading pfSense to 2.7.x"
author: Karim Elatov
categories: [networking,security]
tags: [pfsense]
---

I tried to do my usual [upgrade of pfSense from the UI](https://docs.netgate.com/pfsense/en/latest/install/upgrade-guide-update.html#upgrading-using-the-gui) but it timed out and got me into a weird state. So I logged into the device and tried to perform the upgrade manually:

```bash
[2.7.0-RELEASE][root@pf.kar.int]/var/log: pfSense-upgrade -d
ld-elf.so.1: Shared object "libcrypto.so.30" not found, required by "php"
ld-elf.so.1: Shared object "libcrypto.so.30" not found, required by "php"
ld-elf.so.1: Shared object "libcrypto.so.30" not found, required by "php"
/usr/local/libexec/pfSense-upgrade: /usr/local/sbin/-repo-setup: not found
>>> Setting vital flag on php82... 
>>> Updating repositories metadata... 
Updating pfSense-core repository catalogue...
Fetching meta.conf: . done
Fetching packagesite.pkg: . done
Processing entries: . done
pfSense-core repository update completed. 4 packages processed.
Updating pfSense repository catalogue...
Fetching meta.conf: . done
Fetching packagesite.pkg: .... done
Processing entries: 
Processing entries............. done
pfSense repository update completed. 549 packages processed.
All repositories are up to date.
>>> Upgrading -upgrade... 
pkg-static: illegal option -- u
Usage: pkg upgrade [-fInFqUy] [-r reponame] [-Cgix] <pkg-name> ...

For more information see 'pkg help upgrade'.
```

I found a couple of forums that saw the same thing:

- [Upgrade 2.70 to 2.72](https://forum.pfsense.com/topic/184734/upgrade-2-70-to-2-72)
- [Upgrade pfsense CE 2.7.0 to 2.7.1](https://forum.netgate.com/topic/184195/upgrade-pfsense-ce-2-7-0-to-2-7-1/36)
- [Upgraded Package before Upgrading to 2.7.1 - System screwed!](https://forum.netgate.com/topic/184457/upgraded-package-before-upgrading-to-2-7-1-system-screwed)

## Downgrade pfSense using the CLI with pkg-static
In the end following the instructions from [Upgrade not Offered / Library Errors](https://docs.netgate.com/pfsense/en/latest/troubleshooting/upgrades.html#upgrade-not-offered-library-errors) had the best results. Navigate to **System** > **Updates**, Set **Branch** to **Previous stable version**, for me in this instance this was `2.7.0`. Then I ran:

```
# pkg-static clean -ay; pkg-static install -fy pkg pfSense-repo pfSense-upgrade
...
Installed packages to be DOWNGRADED:
        pfSense-repo: 2.7.1 -> 2.7.0_2 [pfSense]
        pfSense-upgrade: 1.2.1 -> 1.0_33 [pfSense]
        pkg: 1.20.8_3 -> 1.19.1_2 [pfSense]
```

Then following instructions from [Forced pkg Reinstall](https://docs.netgate.com/pfsense/en/latest/troubleshooting/upgrades.html#forced-pkg-reinstall), I ran:

```bash
# pkg-static upgrade -f
...
[210/212] Extracting pfSense-kernel-pfSense-2.7.0: 100%
===> Keeping a copy of current kernel in /boot/kernel.old
[211/212] Reinstalling pkg-1.19.1_2...
[211/212] Extracting pkg-1.19.1_2: 100%
```

That pretty much downgraded my install the what I started with: `2.7.0`. 

## Upgrade pfSense using the CLI with pkg-static
Then I repeated the process and upgraded to `2.7.1`: Navigate to **System** > **Updates**, Set **Branch** to **Previous stable version**, for me in this instance this was `2.7.1`. Then I ran:

```
# pkg-static clean -ay; pkg-static install -fy pkg pfSense-repo pfSense-upgrade
...
Installed packages to be UPGRADED:
        pfSense-repo: 2.7.0_2 -> 2.7.1 [pfSense]
        pfSense-upgrade: 1.0_33 -> 1.2.1 [pfSense]

Installed packages to be REINSTALLED:
        pkg-1.20.8_3 [pfSense]
```

Then I did another force upgrade:

```
# pkg-static upgrade -f
...
        pfSense: 2.7.0 -> 2.7.1 [pfSense]
        pfSense-base: 2.7.0 -> 2.7.1 [pfSense-core]
        pfSense-boot: 2.7.0 -> 2.7.1 [pfSense-core]
        pfSense-default-config-serial: 2.7.0 -> 2.7.1 [pfSense]
        pfSense-kernel-pfSense: 2.7.0 -> 2.7.1 [pfSense-core]
```

During the install I still saw a couple of the these:

```bash
[27/219] Extracting php82-pear-1.10.13: 100%
ld-elf.so.1: Shared object "libcrypto.so.30" not found, required by "php"
```

But at the very end, it looked good:

```bash
Configuring package components...
Loading package instructions...
Custom commands...
Executing custom_php_install_command()...done.
Executing custom_php_resync_config_command()...done.
Menu items... done.
Services... done.
Writing configuration... done.
[209/219] Upgrading pfSense from 2.7.0 to 2.7.1...
[209/219] Extracting pfSense-2.7.1: 100%
```

And the upgrade looked good:

```bash
# pfSense-upgrade -d -c
>>> Updating repositories metadata... 
Updating pfSense-core repository catalogue...
Fetching meta.conf: 
Fetching packagesite.pkg: 
pfSense-core repository is up to date.
Updating pfSense repository catalogue...
Fetching meta.conf: 
Fetching packagesite.pkg: 
pfSense repository is up to date.
All repositories are up to date.
Your system is up to date
```

## Upgrade pfSense using the CLI with pfSense-upgrade
So then I made a backup of my config:

```bash
scp /cf/conf/config.xml me@backup:
```

And then navigated to **System** > **Updates**, Set **Branch** to **Latest stable version**, for me in this instance this was `2.7.2`. And then I decided to perform a regular upgrade:

```bash
# pfSense-upgrade -d 
>>> Updating repositories metadata... 
Updating pfSense-core repository catalogue...
Fetching meta.conf: . done
Fetching packagesite.pkg: . done
Processing entries: . done
pfSense-core repository update completed. 4 packages processed.
Updating pfSense repository catalogue...
Fetching meta.conf: . done
Fetching packagesite.pkg: .... done
Processing entries: .......... done
pfSense repository update completed. 549 packages processed.
All repositories are up to date.

The following 9 package(s) will be affected (of 0 checked):

Installed packages to be UPGRADED:
        pfSense: 2.7.1 -> 2.7.2 [pfSense]
        pfSense-base: 2.7.1 -> 2.7.2 [pfSense-core]
        pfSense-boot: 2.7.1 -> 2.7.2 [pfSense-core]
        pfSense-default-config-serial: 2.7.1 -> 2.7.2 [pfSense]
        pfSense-kernel-pfSense: 2.7.1 -> 2.7.2 [pfSense-core]
        pfSense-pkg-suricata: 7.0.2_1 -> 7.0.2_3 [pfSense]
        pfSense-repo: 2.7.1 -> 2.7.2 [pfSense]
        strongswan: 5.9.11_2 -> 5.9.11_3 [pfSense]
        suricata: 7.0.2_4 -> 7.0.2_6 [pfSense]
...
Installed packages to be UPGRADED:
        pfSense-kernel-pfSense: 2.7.1 -> 2.7.2 [pfSense-core]

Number of packages to be upgraded: 1
[1/1] Upgrading pfSense-kernel-pfSense from 2.7.1 to 2.7.2...
[1/1] Extracting pfSense-kernel-pfSense-2.7.2: .......... done
===> Keeping a copy of current kernel in /boot/kernel.old
>>> Removing unnecessary packages... 
Checking integrity... done (0 conflicting)
Nothing to do.
System is going to be upgraded.  Rebooting in 10 seconds.

Broadcast Message from root@pf                                        3
        (/dev/pts/1) at 22:52 MST...                                           

System is going to be upgraded.  Rebooting in 10 seconds.
```

And then luckily the pfsense box came back without issues.      
