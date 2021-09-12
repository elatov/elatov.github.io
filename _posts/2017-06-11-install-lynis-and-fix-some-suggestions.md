---
published: true
layout: post
title: "Install Lynis and Fix Some Suggestions"
author: Karim Elatov
categories: [security]
tags: [lynis,auditd,psacct]
---
### Lynis
I kept reading good things about [lynis](https://cisofy.com/lynis/):

* [Tiger is History, Long Live Modern Alternatives!](https://linux-audit.com/tiger-is-history-long-live-modern-alternatives/)
* [Lynis 2.2.0 Released – Security Auditing and Scanning Tool for Linux Systems](http://www.tecmint.com/linux-security-auditing-and-scanning-with-lynis-tool/)
* [Essential tools for hardening and securing Unix based Environments](http://www.linuxsecurity.com/content/view/164493/171/)

So I decided to give it a try.

### Installing Lynis on CentOS 7
The install is pretty easy, just setup the repo as per the instructions in [Software Repository](https://packages.cisofy.com/#centos-fedora-rhel) and then you can just use **yum** to install it. Here is my repo:

	<> cat /etc/yum.repos.d/lynis.repo
	[lynis]
	name=CISOfy Software - Lynis package
	baseurl=https://packages.cisofy.com/community/lynis/rpm/
	enabled=1
	gpgkey=https://packages.cisofy.com/keys/cisofy-software-rpms-public.key
	gpgcheck=1

Then we can run these command to install **lynis**:

	$ sudo yum makecache fast
	$ sudo yum install lynis

Next we can quickly create a quick audit report:

	$ sudo lynis audit system

You will see the results in your shell and also under **/var/log/lynis-report.dat**. You can also check out the log file under **/var/log/lynis.log**.

#### Lynis Cron Job
There is a pretty good example of the cron job in [Lynis Documentation](https://cisofy.com/documentation/lynis/#cronjobs), so I ended up with the following:

	<> cat /etc/cron.weekly/lynis
	#!/bin/sh
	
	AUDITOR="automated"
	DATE=$(date +%Y%m%d)
	HOST=$(hostname -s)
	LOG_DIR="/var/log/lynis"
	REPORT="$LOG_DIR/report-${HOST}.${DATE}"
	DATA="$LOG_DIR/report-data-${HOST}.${DATE}.txt"
	LYNIS=/usr/bin/lynis
	
	# Run Lynis
	${LYNIS} audit system --auditor "${AUDITOR}" --cronjob > ${REPORT}
	
	# Optional step: Move report file if it exists
	if [ -f /var/log/lynis-report.dat ]; then
	    mv /var/log/lynis-report.dat ${DATA}
	fi
	
	# Send report via email
	MAIL=/usr/bin/mail
	EMAILTO=me
	
	${MAIL} -s "Lynis Report for ${HOST}" ${EMAILTO} < ${REPORT}
	
	# The End

### Lynis Suggestions
After running the audit report on my Centos 7 machine, I first got the following suggestions:

>  -[ Lynis 2.4.0 Results ]-
> 
>   Great, no warnings
> 
>   Suggestions (30):
>   
> ----------------------------
>   
>   * Configure minimum password age in /etc/login.defs [AUTH-9286]
>       https://cisofy.com/controls/AUTH-9286/
> 
>   * Configure maximum password age in /etc/login.defs [AUTH-9286]
>       https://cisofy.com/controls/AUTH-9286/
> 
>   * Default umask in /etc/profile or /etc/profile.d/custom.sh could be more strict (e.g. 027) [AUTH-9328]
>       https://cisofy.com/controls/AUTH-9328/
> 
>   * To decrease the impact of a full /home file system, place /home on a separated partition [FILE-6310]
>       https://cisofy.com/controls/FILE-6310/
> 
>   * To decrease the impact of a full /tmp file system, place /tmp on a separated partition [FILE-6310]
>       https://cisofy.com/controls/FILE-6310/
> 
>   * Disable drivers like USB storage when not used, to prevent unauthorized storage or data theft [STRG-1840]
>       https://cisofy.com/controls/STRG-1840/
> 
>   * Disable drivers like firewire storage when not used, to prevent unauthorized storage or data theft [STRG-1846]
>       https://cisofy.com/controls/STRG-1846/
> 
>   * Add the IP name and FQDN to /etc/hosts for proper name resolving [NAME-4404]
>       https://cisofy.com/controls/NAME-4404/
> 
>   * Consider running ARP monitoring software (arpwatch,arpon) [NETW-3032]
>       https://cisofy.com/controls/NETW-3032/
> 
>   * Check iptables rules to see which rules are currently not used [FIRE-4513]
>       https://cisofy.com/controls/FIRE-4513/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : AllowTcpForwarding (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : ClientAliveCountMax (3 --> 2)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : Compression (DELAYED --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : LogLevel (INFO --> VERBOSE)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : MaxAuthTries (6 --> 1)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : MaxSessions (10 --> 2)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : PermitRootLogin (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : Port (22 --> )
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : TCPKeepAlive (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : UseDNS (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : X11Forwarding (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Consider hardening SSH configuration [SSH-7408]
>   	* Details  : AllowAgentForwarding (YES --> NO)
>       https://cisofy.com/controls/SSH-7408/
> 
>   * Add a legal banner to /etc/issue, to warn unauthorized users [BANN-7126]
>       https://cisofy.com/controls/BANN-7126/
> 
>   * Add legal banner to /etc/issue.net, to warn unauthorized users [BANN-7130]
>       https://cisofy.com/controls/BANN-7130/
> 
>   * Enable process accounting [ACCT-9622]
>       https://cisofy.com/controls/ACCT-9622/
> 
>   * Audit daemon is enabled with an empty ruleset. Disable the daemon or define rules [ACCT-9630]
>       https://cisofy.com/controls/ACCT-9630/
> 
>   * Determine if automation tools are present for system management [TOOL-5002]
>       https://cisofy.com/controls/TOOL-5002/
> 
>   * One or more sysctl values differ from the scan profile and could be tweaked [KRNL-6000]
>       https://cisofy.com/controls/KRNL-6000/
> 
>   * Harden compilers like restricting access to root user only [HRDN-7222]
>       https://cisofy.com/controls/HRDN-7222/
> 
>   * Harden the system by installing at least one malware scanner, to perform periodic file system scans [HRDN-7230]
>   	* Solution : Install a tool like rkhunter, chkrootkit, OSSEC
>       https://cisofy.com/controls/HRDN-7230/

If you follow the links it will give you a pretty start on what to do to fix it. Let's fix some of these.

#### Default umask in /etc/profile or /etc/profile.d/custom.sh could be more strict (e.g. 027) [AUTH-9328]

You will notice that by default the **umask** is **002** under **/etc/profile**, so we can just update that to be **027**. So in that file, change this section:

	if [ $UID -gt 199 ] && [ "`id -gn`" = "`id -un`" ]; then
	    umask 002
	else
	    umask 022
	fi

to this:

	if [ $UID -gt 199 ] && [ "`id -gn`" = "`id -un`" ]; then
	    umask 027
	else
	    umask 027
	fi


Do the same thing in the **/etc/bashrc** and **/etc/csh.cshrc** files.

#### To decrease the impact of a full /tmp file system, place /tmp on a separated partition [FILE-6310]

There is a pretty good site that talks about the setup for CentOS 7: [RHEL7: How to configure /tmp on tmpfs](https://www.certdepot.net/rhel7-how-to-configure-tmp-on-tmpfs/). All we have to do is just enable the right service:

	$ sudo systemctl enable tmp.mount

Then you can double check it's enabled:

	<> df -Ph /tmp
	Filesystem      Size  Used Avail Use% Mounted on
	tmpfs           921M   36K  921M   1% /tmp


#### Disable drivers like USB storage when not used, to prevent unauthorized storage or data theft [STRG-1840]

This was a VM so disabling USB storage was a great idea. The setup is covered in: [Linux Disable USB Devices (Disable loading of USB Storage Driver)](https://www.cyberciti.biz/faq/linux-disable-modprobe-loading-of-usb-storage-driver/). I just created the following file to disable the USB kernel module:

	<> cat /etc/modprobe.d/usb.conf
	blacklist usb-storage

Then reboot to apply.

#### Disable drivers like firewire storage when not used, to prevent unauthorized storage or data theft [STRG-1846]

Similar to the USB one, we just need to disable the kernel module. The setup is covered in: [Kernel hardening: Disable and blacklist Linux modules](https://linux-audit.com/kernel-hardening-disable-and-blacklist-linux-modules/). I ended up creating this file:

	<> cat /etc/modprobe.d/firewire.conf
	blacklist firewire-core

Then a reboot would apply that. If you don't want to reboot you can unload the module on the fly:

	$ sudo modprobe -r <module>

#### Consider running ARP monitoring software (arpwatch,arpon) [NETW-3032]

I decided to install **arpwatch**, the setup is covered in: [Arpwatch Tool to Monitor Ethernet Activity in Linux](http://www.tecmint.com/monitor-ethernet-activity-in-linux/). Here are the steps:

	### install arp watch
	$ sudo yum install arpwatch
	### (change email if necessary)
	sudo vi /etc/sysconfig/arpwatch 
	### enable and start
	sudo systemctl enable arpwatch
	sudo systemctl start arpwatch

#### Consider hardening SSH configuration [SSH-7408]
A couple of the suggestions I didn't really want to apply cause sometimes I SSH to a machine from multiple machines, but here are some of the configs that I changed in the **/etc/ssh/sshd_config** file:

	PermitRootLogin without-password
	X11Forwarding no
	AllowAgentForwarding no
	UseDNS yes

This site goes over the settings pretty well: [Audit and harden your SSH configuration](https://linux-audit.com/audit-and-harden-your-ssh-configuration/). You can then confirm the settings:

	$ sudo sshd -T

Lastly restart the daemon to apply the settings:

	$ sudo systemctl restart sshd

You can also disable any tests that you don't want to show up in the results. To do this modify the **/etc/lynis/default.prf** file and add the following to it:

	skip-test=AUTH-9286
	skip-test=SSH-7408:clientalivecountmax
	skip-test=SSH-7408:compression
	skip-test=SSH-7408:loglevel

#### Add a legal banner to /etc/issue, to warn unauthorized users [BANN-7126]

This site has good examples of banners: [TipsAndTricks -> BannerFiles](https://wiki.centos.org/TipsAndTricks/BannerFiles). I ended up modifying the file to look like this:

	<> cat /etc/issue
	Unauthorized access to this machine is prohibited
	Press <Ctrl-D> if you are not an authorized user

Don't forget to modify the **sshd_config** to point to that file (or add the above to **/etc/motd** file and you won't have to modify the config file):

	<> sudo grep ^Banner /etc/ssh/sshd_config
	Banner /etc/issue

And you can get as creative as you want: [
Cent OS: How to Make a Custom SSH Banner with Current System Statistics](http://www.question-defense.com/2010/04/03/cent-os-how-to-make-a-custom-ssh-banner-with-current-system-statistics)

#### Enable process accounting [ACCT-9622]
This site goes over the setup pretty well: [How to Monitor User Activity with psacct or acct Tools](http://www.tecmint.com/how-to-monitor-user-activity-with-psacct-or-acct-tools/). Here is what I did:

	### install it
	sudo yum install psacct
	### then enable it and start it
	sudo systemctl enable psacct.service
	sudo systemctl start psacct.service

After that you can manually run command to get system information:

	<> ac -p
		elatov                             553.69
		total      553.69

And more:

	<> sudo lastcomm elatov | awk '{print $1}' | sort | uniq -c | sort -nr | head
	   1798 man
	    478 zsh
	    252 git
	     94 grep
	     60 uname
	     48 id
	     36 hostname
	     28 Plex
	     26 which
	     24 env

I ended up creating a **cronjob** which would send me a couple of statistics monthly:

	<> sudo cat /etc/cron.monthly/psacct
	#!/bin/sh
	echo -e "User stats\n"
	/bin/ac -p
	echo -e "elatov commands\n"
	/bin/lastcomm elatov | /bin/awk '{print $1}' | /bin/sort | /bin/uniq -c  | /bin/sort -nr | /bin/head
	echo -e "User Logins\n"
	/bin/last | /bin/awk '{print $1}' | /bin/sort | /bin/uniq -c  | /bin/sort -nr | /bin/head
	echo -e "Host Logins\n"
	/bin/last | /bin/awk '{print $3}' | /bin/sort | /bin/uniq -c  | /bin/sort -nr | /bin/head

### Audit daemon is enabled with an empty ruleset. Disable the daemon or define rules [ACCT-9630]

The [suggestion link](https://cisofy.com/controls/ACCT-9630/) has a good config file to use. I just had to modify the **puppet** line since it's moved to a different location. Here is the file I ended up with:

	<> sudo cat /etc/audit/rules.d/audit.rules
	# This is an example configuration suitable for most systems
	# Before running with this configuration:
	# - Remove or comment items which are not applicable
	# - Check paths of binaries and files
	
	###################
	# Remove any existing rules
	###################
	
	-D
	
	###################
	# Buffer Size
	###################
	# Might need to be increased, depending on the load of your system.
	-b 8192
	
	###################
	# Failure Mode
	###################
	# 0=Silent
	# 1=printk, print failure message
	# 2=panic, halt system
	-f 1
	
	###################
	# Audit the audit logs.
	###################
	-w /var/log/audit/ -k auditlog
	
	###################
	## Auditd configuration
	###################
	## Modifications to audit configuration that occur while the audit (check your paths)
	-w /etc/audit/ -p wa -k auditconfig
	-w /etc/libaudit.conf -p wa -k auditconfig
	-w /etc/audisp/ -p wa -k audispconfig
	
	###################
	# Monitor for use of audit management tools
	###################
	# Check your paths
	-w /sbin/auditctl -p x -k audittools
	-w /sbin/auditd -p x -k audittools
	
	###################
	# Special files
	###################
	-a exit,always -F arch=b32 -S mknod -S mknodat -k specialfiles
	-a exit,always -F arch=b64 -S mknod -S mknodat -k specialfiles
	
	###################
	# Mount operations
	###################
	-a exit,always -F arch=b32 -S mount -S umount -S umount2 -k mount
	-a exit,always -F arch=b64 -S mount -S umount2 -k mount
	
	###################
	# Changes to the time
	###################
	-a exit,always -F arch=b32 -S adjtimex -S settimeofday -S stime -S clock_settime -k time
	-a exit,always -F arch=b64 -S adjtimex -S settimeofday -S clock_settime -k time
	-w /etc/localtime -p wa -k localtime
	
	###################
	# Use of stunnel
	###################
	-w /usr/sbin/stunnel -p x -k stunnel
	
	###################
	# Schedule jobs
	###################
	-w /etc/cron.allow -p wa -k cron
	-w /etc/cron.deny -p wa -k cron
	-w /etc/cron.d/ -p wa -k cron
	-w /etc/cron.daily/ -p wa -k cron
	-w /etc/cron.hourly/ -p wa -k cron
	-w /etc/cron.monthly/ -p wa -k cron
	-w /etc/cron.weekly/ -p wa -k cron
	-w /etc/crontab -p wa -k cron
	-w /var/spool/cron/crontabs/ -k cron
	
	## user, group, password databases
	-w /etc/group -p wa -k etcgroup
	-w /etc/passwd -p wa -k etcpasswd
	-w /etc/gshadow -k etcgroup
	-w /etc/shadow -k etcpasswd
	-w /etc/security/opasswd -k opasswd
	
	###################
	# Monitor usage of passwd command
	###################
	-w /usr/bin/passwd -p x -k passwd_modification
	
	###################
	# Monitor user/group tools
	###################
	-w /usr/sbin/groupadd -p x -k group_modification
	-w /usr/sbin/groupmod -p x -k group_modification
	-w /usr/sbin/addgroup -p x -k group_modification
	-w /usr/sbin/useradd -p x -k user_modification
	-w /usr/sbin/usermod -p x -k user_modification
	-w /usr/sbin/adduser -p x -k user_modification
	
	###################
	# Login configuration and stored info
	###################
	-w /etc/login.defs -p wa -k login
	-w /etc/securetty -p wa -k login
	-w /var/log/faillog -p wa -k login
	-w /var/log/lastlog -p wa -k login
	-w /var/log/tallylog -p wa -k login
	
	###################
	# Network configuration
	###################
	-w /etc/hosts -p wa -k hosts
	-w /etc/network/ -p wa -k network
	
	###################
	## system startup scripts
	###################
	-w /etc/inittab -p wa -k init
	-w /etc/init.d/ -p wa -k init
	-w /etc/init/ -p wa -k init
	
	###################
	# Library search paths
	###################
	-w /etc/ld.so.conf -p wa -k libpath
	
	###################
	# Kernel parameters and modules
	###################
	-w /etc/sysctl.conf -p wa -k sysctl
	-w /etc/modprobe.conf -p wa -k modprobe
	###################
	
	###################
	# PAM configuration
	###################
	-w /etc/pam.d/ -p wa -k pam
	-w /etc/security/limits.conf -p wa  -k pam
	-w /etc/security/pam_env.conf -p wa -k pam
	-w /etc/security/namespace.conf -p wa -k pam
	-w /etc/security/namespace.init -p wa -k pam
	
	###################
	# Puppet (SSL)
	###################
	-w /etc/puppetlabs/puppet/ssl -p wa -k puppet_ssl
	
	###################
	# Postfix configuration
	###################
	-w /etc/aliases -p wa -k mail
	-w /etc/postfix/ -p wa -k mail
	###################
	
	###################
	# SSH configuration
	###################
	-w /etc/ssh/sshd_config -k sshd
	
	###################
	# Hostname
	###################
	-a exit,always -F arch=b32 -S sethostname -k hostname
	-a exit,always -F arch=b64 -S sethostname -k hostname
	
	###################
	# Changes to issue
	###################
	-w /etc/issue -p wa -k etcissue
	-w /etc/issue.net -p wa -k etcissue
	
	###################
	# Log all commands executed by root
	###################
	-a exit,always -F arch=b64 -F euid=0 -S execve -k rootcmd
	-a exit,always -F arch=b32 -F euid=0 -S execve -k rootcmd
	
	###################
	## Capture all failures to access on critical elements
	###################
	-a exit,always -F arch=b64 -S open -F dir=/etc -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/bin -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/home -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/sbin -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/srv -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/usr/bin -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/usr/local/bin -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/usr/sbin -F success=0 -k unauthedfileacess
	-a exit,always -F arch=b64 -S open -F dir=/var -F success=0 -k unauthedfileacess
	
	###################
	## su/sudo
	###################
	-w /bin/su -p x -k priv_esc
	-w /usr/bin/sudo -p x -k priv_esc
	-w /etc/sudoers -p rw -k priv_esc
	
	###################
	# Poweroff/reboot tools
	###################
	-w /sbin/halt -p x -k power
	-w /sbin/poweroff -p x -k power
	-w /sbin/reboot -p x -k power
	-w /sbin/shutdown -p x -k power
	
	###################
	# Make the configuration immutable
	###################
	-e 2
	
	# EOF

After that you can restart the service

	$ sudo service auditd restart

You can get a bunch of summaries using the **aureport** utility. I ended up creating a daily job for some summary reports:

	<> cat /etc/cron.daily/aureports
	#!/bin/sh
	/sbin/aureport -au
	/sbin/aureport -l
	/sbin/aureport -x --summary | /bin/head -20
	/sbin/aureport -f --summary | /bin/head -20
	/sbin/aureport -u -i --summary
	/sbin/aureport --failed

Also this site has a **python** script that accomplishes similar tasks: [SELinux audit reports script](https://www.g-loaded.eu/2006/12/20/selinux-audit-reports-script/)

#### Determine if automation tools are present for system management [TOOL-5002]

I actually had **puppet** installed but it wouldn't pick up the binary. From [Lynis Releases](https://github.com/CISOfy/lynis/releases) (under the *Lynis 2.3.3* section) you can use **--bin-dirs** to specify the paths which will be scanned for binaries, but rather than appending it just overwrites it. You could do something like this with the cronjob

	 <> grep bindir /etc/cron.weekly/lynis
	${LYNIS} audit system --auditor "${AUDITOR}" --cronjob  --bindirs "/usr/bin /usr/sbin /opt/puppetlabs/bin/ /var/ossec/bin"> ${REPORT}

The default paths are in the **consts** file in the **BIN_PATH** variable:

	<> sudo grep BIN_PATH /usr/share/lynis/include/consts -A 4
	BIN_PATHS="/bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin \
	          /usr/local/libexec /usr/libexec /usr/sfw/bin /usr/sfw/sbin \
	          /usr/sfw/libexec /opt/sfw/bin /opt/sfw/sbin /opt/sfw/libexec \
	          /usr/xpg4/bin /usr/css/bin /usr/ucb /usr/X11R6/bin /usr/X11R7/bin \
	          /usr/pkg/bin /usr/pkg/sbin"

If you don't want to mess with **--bin-dirs** you can created a *symlink* under **/usr/bin/**

	<> sudo ln -s /opt/puppetlabs/bin/puppet /usr/bin/puppet

Notice I also added **/var/ossec/bin/** to the **bindirs**, parameter since that's where the **ossec** binary reside.

### Harden the system by installing at least one malware scanner, to perform periodic file system scans [HRDN-7230]

I ended up installing **sophos** and here is [post](/2017/07/sophos-9-on-centos-7/) on the setup.

### One or more sysctl values differ from the scan profile and could be tweaked [KRNL-6000]

A lot of these are covered here:
[Security Features in the Kernel from Security and Hardening Guide](https://documentation.suse.com/sles/12-SP3/html/SLES-all/cha-sec-prot-general.html). First get a backup of the default settings just in case:

	<> sudo sysctl -a > /tmp/sysctl-defaults.conf

Then create the config file:

	<> sudo cat /etc/sysctl.d/80-lynis.conf
	kernel.kptr_restrict = 2
	kernel.sysrq = 0
	net.ipv4.conf.all.accept_redirects = 0
	net.ipv4.conf.all.log_martians = 1
	net.ipv4.conf.all.send_redirects = 0
	net.ipv4.conf.default.accept_redirects = 0
	net.ipv4.conf.default.log_martians = 1
	#net.ipv4.tcp_timestamps = 0
	net.ipv6.conf.all.accept_redirects = 0
	net.ipv6.conf.default.accept_redirects = 0

And then apply the settings:

	<> sudo sysctl --system
	* Applying /usr/lib/sysctl.d/00-system.conf ...
	* Applying /usr/lib/sysctl.d/50-default.conf ...
	...
	...
	* Applying /etc/sysctl.d/80-lynis.conf ...
	kernel.kptr_restrict = 2
	kernel.sysrq = 0
	net.ipv4.conf.all.accept_redirects = 0
	net.ipv4.conf.all.log_martians = 1
	net.ipv4.conf.all.send_redirects = 0
	net.ipv4.conf.default.accept_redirects = 0
	net.ipv4.conf.default.log_martians = 1
	net.ipv6.conf.all.accept_redirects = 0
	net.ipv6.conf.default.accept_redirects = 0
	* Applying /etc/sysctl.d/99-sysctl.conf ...
	* Applying /etc/sysctl.conf ...

I decided to keep the tcp timestamps option as is after reading [this](http://stackoverflow.com/questions/7880383/what-benefit-is-conferred-by-tcp-timestamp) post. To disable that check, just comment out this line in your profile:

	<> grep tcp_times /etc/lynis/default.prf
	config-data=sysctl;net.ipv4.tcp_timestamps;0;1;Do not use TCP time stamps;-;category:security;

### Harden compilers like restricting access to root user only [HRDN-7222]

Let's disallow **other**s from using **/usr/bin/gcc**:

	┌─[elatov@m2] - [/home/elatov] - [2016-12-27 12:15:29]
	└─[0] <> which gcc
	/usr/bin/gcc
	┌─[elatov@m2] - [/home/elatov] - [2016-12-27 12:16:49]
	└─[0] <> ls -l /usr/bin/gcc
	-rwxr-xr-x 2 root root 768616 Nov  4 09:19 /usr/bin/gcc
	┌─[elatov@m2] - [/home/elatov] - [2016-12-27 12:16:54]
	└─[0] <> sudo chmod o-rx /usr/bin/gcc
	┌─[elatov@m2] - [/home/elatov] - [2016-12-27 12:17:10]
	└─[0] <> gcc
	zsh: permission denied: gcc

Let's do same thing for **/usr/bin/as**

	<> sudo chmod o-rx /usr/bin/as

You can get a list of discovered compilers in the log

	<> grep compiler /var/log/lynis.log
	2016-12-27 12:19:05   Found known binary: as (compiler) - /usr/bin/as
	2016-12-27 12:19:05   Found known binary: gcc (compiler) - /usr/bin/gcc


### End Results
In the end got the following results:

>  -[ Lynis 2.4.0 Results ]-
> 
>   Great, no warnings
> 
>   Suggestions (1):
>   
>   ----------------------------
>   
>   * Check iptables rules to see which rules are currently not used [FIRE-4513]
>       https://cisofy.com/controls/FIRE-4513/
> 
>   Follow-up:
>   
>  ----------------------------
>   
>   - Show details of a test (lynis show details TEST-ID)
>   - Check the logfile for all details (less /var/log/lynis.log)
>   - Read security controls texts (https://cisofy.com)
>   - Use --upload to upload data to central system (Lynis Enterprise users)
> 
> ================================================================================
> 
>   Lynis security scan details:
> 
>   Hardening index : 91 [##################  ]
>   
>   Tests performed : 201
>   
>   Plugins enabled : 0

The firewall one suggests running **iptables -L -n -v** and checking for any rules that has **0 bytes** processed. But I had some rules that are valid, like block ICMP but they were just never triggered. But it's good reminder to check out your rules, cause some rules do get out of date. Also just for reference when you are testing out your configurations you can run one specific test like so:

	<> sudo lynis audit system --tests ACCT-9622

That should be it, now my system is super secure and everyone knows about it :)
