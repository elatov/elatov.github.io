---
published: true
layout: post
title: "Suricata on FreeBSD 10"
author: Karim Elatov
categories: [os,security]
tags: [freebsd,suricata]
---
After playing around with **snort** I decided to try out **suricata** (which is the multi-threaded alternative to **snort**). From their [main](http://suricata-ids.org/) page:

> Suricata is a high performance Network IDS, IPS and Network Security Monitoring engine. Open Source and owned by a community run non-profit foundation, the Open Information Security Foundation (OISF). Suricata is developed by the OISF and its supporting vendors.

#### Suricata Install

The FreeBSD version is pretty updated:

    elatov@moxz:~$pkg search ^suricata
    suricata-2.0.5

Installing it is pretty easy:

    elatov@moxz:~$sudo pkg install suricata

#### Grabbing the rules
Suricata supports the Snort VRT rules and the Emerging Threats rules as well. Although not all the VRT rules are supported so if you are using the VRT rules you will get a couple of errors. You can pick and choose which VRT rules to use. The [guide](https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Basic_Setup) from Suricata only uses the ET rules.

##### Oinkmaster
If you just want to use the Emerging Threat rules then you can just use **oinkmaster**. First install it:

    elatov@moxz:~$sudo pkg install oinkmaster

After that add the URL for Emerging Threats in the **oinkmaster** config file (**/usr/local/etc/oinkmaster.conf**):

    url =  http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz

The rule set had some empty rules, so I added the following to skip them:

    skipfile deleted.rules
    skipfile emerging-deleted.rules
    skipfile rbn.rules
    skipfile rbn-malvertisers.rules
    skipfile files.rules
    skipfile emerging-icmp.rules

After that we can run the following to get the rules:

    elatov@moxz:~$oinkmaster -o rules/
    Loading /usr/local/etc/oinkmaster.conf
    Downloading file from http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz... done.
    Archive successfully downloaded, unpacking... done.
    Setting up rules structures... done.
    Processing downloaded rules... disabled 0, enabled 0, modified 0, total=18120
    Setting up rules structures... done.
    Comparing new files to the old ones... done.
    Updating local rules files... done.

    [***] Results from Oinkmaster started 20150104 15:27:16 [***]

    [*] Rules modifications: [*]
        None.

    [*] Non-rule line modifications: [*]
        None.

    [+] Added files (consider updating your snort.conf to include them if needed): [+]

        -> botcc.portgrouped.rules
        -> botcc.rules
        -> BSD-License.txt
        -> ciarmy.rules
        -> classification.config
        -> compromised-ips.txt
        -> compromised.rules
        -> decoder-events.rules
        -> drop.rules
        -> dshield.rules
        -> emerging-activex.rules
        -> emerging-attack_response.rules
        -> emerging-chat.rules
        -> emerging-current_events.rules
        -> emerging-dns.rules
        -> emerging-dos.rules
        -> emerging-exploit.rules
        -> emerging-ftp.rules
        -> emerging-games.rules
        -> emerging-icmp_info.rules
        -> emerging-imap.rules
        -> emerging-inappropriate.rules
        -> emerging-info.rules
        -> emerging-malware.rules
        -> emerging-misc.rules
        -> emerging-mobile_malware.rules
        -> emerging-netbios.rules
        -> emerging-p2p.rules
        -> emerging-policy.rules
        -> emerging-pop3.rules
        -> emerging-rpc.rules
        -> emerging-scada.rules
        -> emerging-scan.rules
        -> emerging-shellcode.rules
        -> emerging-smtp.rules
        -> emerging-snmp.rules
        -> emerging-sql.rules
        -> emerging-telnet.rules
        -> emerging-tftp.rules
        -> emerging-trojan.rules
        -> emerging-user_agents.rules
        -> emerging-voip.rules
        -> emerging-web_client.rules
        -> emerging-web_server.rules
        -> emerging-web_specific_apps.rules
        -> emerging-worm.rules
        -> emerging.conf
        -> gen-msg.map
        -> gpl-2.0.txt
        -> http-events.rules
        -> reference.config
        -> sid-msg.map
        -> smtp-events.rules
        -> stream-events.rules
        -> suricata-open.txt
        -> tls-events.rules
        -> tor.rules
        -> unicode.map

Now in the **suricata** configuration we need to add all those rules. So under the **/usr/local/suricata/suricata.yaml** file make sure you have something like this:

    default-rule-path: /usr/local/etc/suricata/rules
    rule-files:
     - botcc.portgrouped.rules
     - botcc.rules
     - ciarmy.rules
     - compromised.rules
     - decoder-events.rules
     - drop.rules
     - dshield.rules
     - emerging-activex.rules
     - emerging-attack_response.rules
     - emerging-chat.rules
     - emerging-current_events.rules
     - emerging-dns.rules
    ..
    ...

You will also notice that the rules archive included the following files:

- sid-msg.map
- gen-msg.map
- classification.config
- reference.config

Those are files used by **barnyard2** when adding events to the MySQL DB to make sure the description and classification (and etc) of the event are correct. So make sure you have the following in your **barnyard2** config (**/usr/local/etc/barnyard2.conf**):

    config reference_file:      /usr/local/etc/suricata/rules/reference.config
    config classification_file: /usr/local/etc/suricata/rules/classification.config
    config gen_file:            /usr/local/etc/suricata/rules/gen-msg.map
    config sid_file:            /usr/local/etc/suricata/rules/sid-msg.map

##### Pulledpork

With pulledport you can do both (VRT and ET rules), if you want to automate getting the latest version you actually need the **snort** binary, cause it uses that to discover which version you are on, and if your **snort** is at the latest version then you it will grab the lastest **snort** VRT rules. Here is my pulledpork config:

    elatov@moxz:~$grep -Ev '^$|^#' /usr/local/etc/pulledpork/pulledpork.conf
    rule_url=https://www.snort.org/rules/|snortrules-snapshot.tar.gz|<oinkcode>
    rule_url=https://rules.emergingthreatspro.com/open/suricata/|emerging.rules.tar.gz|open
    ignore=deleted.rules,experimental.rules,local.rules
    temp_path=/tmp
    rule_path=/usr/local/etc/suricata/rules/et.rules
    local_rules=/usr/local/etc/suricata/rules/local.rules
    sid_msg=/usr/local/etc/suricata/sid-msg.map
    sid_msg_version=1
    sid_changelog=/var/log/suricata/sid_changes.log
    snort_path=/usr/local/bin/snort
    distro=FreeBSD-9-0
    black_list=/usr/local/etc/suricata/rules/iplists/default.blacklist
    IPRVersion=/usr/local/etc/suricata/rules/iplists
    engine=suricata
    version=0.7.0

Then we can get both rule sets in one big file (**/usr/local/etc/suricata/rules/et.rules**):

    elatov@moxz:~$pulledpork.pl -c /usr/local/etc/pulledpork/pulledpork.conf -vv

        http://code.google.com/p/pulledpork/
          _____ ____
         `----,\    )
          `--==\\  /    PulledPork v0.7.0 - Swine Flu!
           `--==\\/
         .-~~~~-.Y|\\_  Copyright (C) 2009-2013 JJ Cummings
      @_/        /  66\_  cummingsj@gmail.com
        |    \   \   _(")
         \   /-| ||'--'  Rules give me wings!
          \_\  \_\\
     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Config File Variable Debug /usr/local/etc/pulledpork/pulledpork.conf
        snort_path = /usr/local/bin/snort
        sid_msg_version = 1
        ignore = deleted.rules,experimental.rules,local.rules
        local_rules = /usr/local/etc/suricata/rules/local.rules
        rule_url = ARRAY(0x8532df48)
        distro = FreeBSD-9-0
        sid_msg = /usr/local/etc/suricata/sid-msg.map
        temp_path = /tmp
        sid_changelog = /var/log/suricata/id_changes.log
        black_list = /usr/local/etc/suricata/rules/default.blacklist
        engine = suricata
        rule_path = /usr/local/etc/suricata/rules
        IPRVersion = /usr/local/etc/suricata/rules/iplists
        version = 0.7.0
    MISC (CLI and Autovar) Variable Debug:
        arch Def is: x86-64
        Config Path is: /usr/local/etc/pulledpork/pulledpork.conf
        Distro Def is: FreeBSD-9-0
        Disabled policy specified
        local.rules path is: /usr/local/etc/suricata/rules/local.rules
        Rules file is: /tmp/rules
        sid changes will be logged to: /var/log/suricata/id_changes.log
        sid-msg.map Output Path is: /usr/local/etc/suricata/sid-msg.map
        Snort Version is: 2.9.7.0
        Snort Path is: /usr/local/bin/snort
        Will process SO rules
        Extra Verbose Flag is Set
        Verbose Flag is Set
        Base URL is: https://www.snort.org/rules/|snortrules-snapshot.tar.gz|<oinkcode> https://rules.emergingthreatspro.com/open/suricata/|emerging.rules.tar.gz|open
    Checking latest MD5 for snortrules-snapshot-2970.tar.gz....
        Fetching md5sum for: snortrules-snapshot-2970.tar.gz.md5
    ** GET https://www.snort.org/reg-rules/snortrules-snapshot-2970.tar.gz.md5/<oinkcode> ==> 200 OK (1s)
        most recent rules file digest: 455a8281b7cfca05526356d0f16c4362
    Rules tarball download of snortrules-snapshot-2970.tar.gz....
        Fetching rules file: snortrules-snapshot-2970.tar.gz
    ** GET https://www.snort.org/reg-rules/snortrules-snapshot-2970.tar.gz/<oinkode> ==> 302 Found

        storing file at: /tmp/snortrules-snapshot-2970.tar.gz

        current local rules file  digest: 455a8281b7cfca05526356d0f16c4362
        The MD5 for snortrules-snapshot-2970.tar.gz matched 455a8281b7cfca05526356d0f16c4362

    Checking latest MD5 for emerging.rules.tar.gz....
        Fetching md5sum for: emerging.rules.tar.gz.md5
    ** GET https://rules.emergingthreatspro.com/open/suricata//emerging.rules.tar.gz.md5 ==> 200 OK (1s)
        most recent rules file digest: f54360373f97d972a154742e39289b1c
    Rules tarball download of emerging.rules.tar.gz....
        Fetching rules file: emerging.rules.tar.gz
    ** GET https://rules.emergingthreatspro.com/open/suricata//emerging.rules.tar.gz ==> 200 OK (4s)
        storing file at: /tmp/emerging.rules.tar.gz

        current local rules file  digest: f54360373f97d972a154742e39289b1c
        The MD5 for emerging.rules.tar.gz matched f54360373f97d972a154742e39289b1c

    Prepping rules from emerging.rules.tar.gz for work....
        extracting contents of /tmp/emerging.rules.tar.gz...
        Ignoring plaintext rules: deleted.rules
        Ignoring plaintext rules: experimental.rules
        Ignoring plaintext rules: local.rules
        Extracted: /tha_rules/ET-emerging-netbios.rules
        Extracted: /tha_rules/ET-http-events.rules
        Extracted: /tha_rules/ET-emerging-tftp.rules
        Extracted: /tha_rules/ET-emerging-telnet.rules
        Extracted: /tha_rules/ET-botcc.portgrouped.rules
        Extracted: /tha_rules/ET-emerging-ftp.rules
        Extracted: /tha_rules/ET-emerging-shellcode.rules
        Extracted: /tha_rules/ET-emerging-imap.rules
        Extracted: /tha_rules/ET-emerging-deleted.rules
        Extracted: /tha_rules/ET-emerging-games.rules
        Extracted: /tha_rules/ET-tls-events.rules
        Extracted: /tha_rules/ET-emerging-misc.rules
        Extracted: /tha_rules/ET-emerging-dos.rules
        Extracted: /tha_rules/ET-emerging-worm.rules
        Extracted: /tha_rules/ET-smtp-events.rules
        Extracted: /tha_rules/ET-emerging-rpc.rules
        Extracted: /tha_rules/ET-botcc.rules
        Extracted: /tha_rules/ET-emerging-p2p.rules
        Extracted: /tha_rules/ET-emerging-malware.rules
        Extracted: /tha_rules/ET-emerging-exploit.rules
        Extracted: /tha_rules/ET-emerging-policy.rules
        Extracted: /tha_rules/ET-emerging-activex.rules
        Extracted: /tha_rules/ET-emerging-scan.rules
        Extracted: /tha_rules/ET-compromised.rules
        Extracted: /tha_rules/ET-emerging-current_events.rules
        Extracted: /tha_rules/ET-emerging-inappropriate.rules
        Extracted: /tha_rules/ET-rbn.rules
        Extracted: /tha_rules/ET-ciarmy.rules
        Extracted: /tha_rules/ET-stream-events.rules
        Extracted: /tha_rules/ET-emerging-icmp.rules
        Extracted: /tha_rules/ET-decoder-events.rules
        Extracted: /tha_rules/ET-emerging-chat.rules
        Extracted: /tha_rules/ET-emerging-icmp_info.rules
        Extracted: /tha_rules/ET-rbn-malvertisers.rules
        Extracted: /tha_rules/ET-emerging-web_client.rules
        Extracted: /tha_rules/ET-emerging-user_agents.rules
        Extracted: /tha_rules/ET-files.rules
        Extracted: /tha_rules/ET-emerging-trojan.rules
        Extracted: /tha_rules/ET-emerging-dns.rules
        Extracted: /tha_rules/ET-emerging-pop3.rules
        Extracted: /tha_rules/ET-emerging-scada.rules
        Extracted: /tha_rules/ET-emerging-smtp.rules
        Extracted: /tha_rules/ET-emerging-attack_response.rules
        Extracted: /tha_rules/ET-emerging-info.rules
        Extracted: /tha_rules/ET-emerging-sql.rules
        Extracted: /tha_rules/ET-drop.rules
        Extracted: /tha_rules/ET-emerging-mobile_malware.rules
        Extracted: /tha_rules/ET-emerging-snmp.rules
        Extracted: /tha_rules/ET-emerging-web_specific_apps.rules
        Extracted: /tha_rules/ET-tor.rules
        Extracted: /tha_rules/ET-dshield.rules
        Extracted: /tha_rules/ET-emerging-voip.rules
        Extracted: /tha_rules/ET-emerging-web_server.rules
    Prepping rules from snortrules-snapshot-2970.tar.gz for work....
        extracting contents of /tmp/snortrules-snapshot-2970.tar.gz...
        Ignoring plaintext rules: deleted.rules
        Ignoring plaintext rules: experimental.rules
        Ignoring plaintext rules: local.rules
        Extracted: /tha_rules/VRT-snmp.rules
        Extracted: /tha_rules/VRT-exploit.rules
        Extracted: /tha_rules/VRT-exploit-kit.rules
        Extracted: /tha_rules/VRT-pua-p2p.rules
        Extracted: /tha_rules/VRT-browser-chrome.rules
        Extracted: /tha_rules/VRT-malware-tools.rules
        Extracted: /tha_rules/VRT-file-flash.rules
        Extracted: /tha_rules/VRT-os-solaris.rules
        Extracted: /tha_rules/VRT-file-image.rules
        Extracted: /tha_rules/VRT-rservices.rules
        Extracted: /tha_rules/VRT-protocol-scada.rules
        Extracted: /tha_rules/VRT-browser-webkit.rules
        Extracted: /tha_rules/VRT-malware-cnc.rules
        Extracted: /tha_rules/VRT-os-other.rules
        Extracted: /tha_rules/VRT-telnet.rules
        Extracted: /tha_rules/VRT-scada.rules
        Extracted: /tha_rules/VRT-dns.rules
        Extracted: /tha_rules/VRT-web-misc.rules
        Extracted: /tha_rules/VRT-multimedia.rules
        Extracted: /tha_rules/VRT-app-detect.rules
        Extracted: /tha_rules/VRT-sql.rules
        Extracted: /tha_rules/VRT-indicator-obfuscation.rules
        Extracted: /tha_rules/VRT-web-coldfusion.rules
        Extracted: /tha_rules/VRT-policy-multimedia.rules
        Extracted: /tha_rules/VRT-imap.rules
        Extracted: /tha_rules/VRT-sensitive-data.rules
        Extracted: /tha_rules/VRT-icmp-info.rules
        Extracted: /tha_rules/VRT-ftp.rules
        Extracted: /tha_rules/VRT-web-attacks.rules
        Extracted: /tha_rules/VRT-misc.rules
        Extracted: /tha_rules/VRT-policy.rules
        Extracted: /tha_rules/VRT-tftp.rules
        Extracted: /tha_rules/VRT-protocol-imap.rules
        Extracted: /tha_rules/VRT-spyware-put.rules
        Extracted: /tha_rules/VRT-protocol-ftp.rules
        Extracted: /tha_rules/VRT-finger.rules
        Extracted: /tha_rules/VRT-server-other.rules
        Extracted: /tha_rules/VRT-other-ids.rules
        Extracted: /tha_rules/VRT-browser-ie.rules
        Extracted: /tha_rules/VRT-protocol-other.rules
        Extracted: /tha_rules/VRT-rpc.rules
        Extracted: /tha_rules/VRT-malware-other.rules
        Extracted: /tha_rules/VRT-bad-traffic.rules
        Extracted: /tha_rules/VRT-content-replace.rules
        Extracted: /tha_rules/VRT-shellcode.rules
        Extracted: /tha_rules/VRT-oracle.rules
        Extracted: /tha_rules/VRT-file-executable.rules
        Extracted: /tha_rules/VRT-smtp.rules
        Extracted: /tha_rules/VRT-file-java.rules
        Extracted: /tha_rules/VRT-server-mssql.rules
        Extracted: /tha_rules/VRT-server-mail.rules
        Extracted: /tha_rules/VRT-chat.rules
        Extracted: /tha_rules/VRT-web-client.rules
        Extracted: /tha_rules/VRT-browser-other.rules
        Extracted: /tha_rules/VRT-virus.rules
        Extracted: /tha_rules/VRT-file-other.rules
        Extracted: /tha_rules/VRT-file-office.rules
        Extracted: /tha_rules/VRT-protocol-services.rules
        Extracted: /tha_rules/VRT-protocol-nntp.rules
        Extracted: /tha_rules/VRT-server-webapp.rules
        Extracted: /tha_rules/VRT-pop3.rules
        Extracted: /tha_rules/VRT-x11.rules
        Extracted: /tha_rules/VRT-pua-other.rules
        Extracted: /tha_rules/VRT-dos.rules
        Extracted: /tha_rules/VRT-browser-firefox.rules
        Extracted: /tha_rules/VRT-web-frontpage.rules
        Extracted: /tha_rules/VRT-protocol-pop.rules
        Extracted: /tha_rules/VRT-os-mobile.rules
        Extracted: /tha_rules/VRT-preprocessor.rules
        Extracted: /tha_rules/VRT-server-samba.rules
        Extracted: /tha_rules/VRT-indicator-scan.rules
        Extracted: /tha_rules/VRT-indicator-shellcode.rules
        Extracted: /tha_rules/VRT-os-windows.rules
        Extracted: /tha_rules/VRT-pop2.rules
        Extracted: /tha_rules/VRT-protocol-voip.rules
        Extracted: /tha_rules/VRT-malware-backdoor.rules
        Extracted: /tha_rules/VRT-browser-plugins.rules
        Extracted: /tha_rules/VRT-phishing-spam.rules
        Extracted: /tha_rules/VRT-server-mysql.rules
        Extracted: /tha_rules/VRT-scan.rules
        Extracted: /tha_rules/VRT-protocol-telnet.rules
        Extracted: /tha_rules/VRT-policy-social.rules
        Extracted: /tha_rules/VRT-web-cgi.rules
        Extracted: /tha_rules/VRT-attack-responses.rules
        Extracted: /tha_rules/VRT-protocol-rpc.rules
        Extracted: /tha_rules/VRT-protocol-tftp.rules
        Extracted: /tha_rules/VRT-blacklist.rules
        Extracted: /tha_rules/VRT-nntp.rules
        Extracted: /tha_rules/VRT-mysql.rules
        Extracted: /tha_rules/VRT-server-apache.rules
        Extracted: /tha_rules/VRT-protocol-finger.rules
        Extracted: /tha_rules/VRT-voip.rules
        Extracted: /tha_rules/VRT-p2p.rules
        Extracted: /tha_rules/VRT-specific-threats.rules
        Extracted: /tha_rules/VRT-pua-toolbars.rules
        Extracted: /tha_rules/VRT-file-pdf.rules
        Extracted: /tha_rules/VRT-server-oracle.rules
        Extracted: /tha_rules/VRT-web-iis.rules
        Extracted: /tha_rules/VRT-indicator-compromise.rules
        Extracted: /tha_rules/VRT-netbios.rules
        Extracted: /tha_rules/VRT-botnet-cnc.rules
        Extracted: /tha_rules/VRT-protocol-snmp.rules
        Extracted: /tha_rules/VRT-file-multimedia.rules
        Extracted: /tha_rules/VRT-ddos.rules
        Extracted: /tha_rules/VRT-policy-spam.rules
        Extracted: /tha_rules/VRT-decoder.rules
        Extracted: /tha_rules/VRT-pua-adware.rules
        Extracted: /tha_rules/VRT-icmp.rules
        Extracted: /tha_rules/VRT-file-identify.rules
        Extracted: /tha_rules/VRT-policy-other.rules
        Extracted: /tha_rules/VRT-web-php.rules
        Extracted: /tha_rules/VRT-protocol-icmp.rules
        Extracted: /tha_rules/VRT-backdoor.rules
        Extracted: /tha_rules/VRT-server-iis.rules
        Extracted: /tha_rules/VRT-info.rules
        Extracted: /tha_rules/VRT-protocol-dns.rules
        Extracted: /tha_rules/VRT-web-activex.rules
        Extracted: /tha_rules/VRT-os-linux.rules
        Reading rules...
    Cleanup....
        removed 173 temporary snort files or directories from /tmp/tha_rules!
    Setting Flowbit State....
        Enabled 63 flowbits
        Done
    Writing /tmp/rules....
        Done
    Generating sid-msg.map....
        Done
    Writing v1 /tmp/sid-msg.map....
        Done
    Writing /tmp/id_changes.log....
        Done
    Rule Stats...
        New:-------42899
        Deleted:---0
        Enabled Rules:----22469
        Dropped Rules:----0
        Disabled Rules:---20429
        Total Rules:------42898
    No IP Blacklist Changes

    Done
    Please review /var/log/suricata/id_changes.log for additional details
    Fly Piggy Fly!

At this point we can modify the suricata config file (**/usr/local/etc/suricata/suricata.yaml**) and just define one rule file and comment out the rest:

    default-rule-path: /usr/local/etc/suricata/rules
    rule-files:
      - et.rules
    #  - botcc.portgrouped.rules
    #  - botcc.rules
    #  - ciarmy.rules
    #  - compromised.rules

Now we can mofify the **barnyard2** config (**/usr/local/etc/barnyard2.conf**) to point to the correct classification files (most of these are available from the suricata install, they are just called ***file*.template**):

	config reference_file:      /usr/local/etc/suricata/reference.config
    config classification_file: /usr/local/etc/suricata/classification.config
    config gen_file:            /usr/local/etc/suricata/gen-msg.map
    config sid_file:            /usr/local/etc/suricata/sid-msg.map

Now the configuration is ready for the rules part. 

If you really want to you can use both in conjunction (**oinkmaster** for ET and **pulledpork** for VRT). You would have to use the **create-sidmap.pl** script (available in the **oinkmaster** source) to generate **sid-mgs.map** file from the **rules** directiores. The usage is descbibed in the oinkmaster [FAQs](http://oinkmaster.sourceforge.net/faq.shtml):

    create-sidmap.pl /etc/snort/rules/official/ \ 
                          /etc/snort/rules/bleeding/ \
                          /etc/snort/rules/local/    \
                          > /etc/snort/sid-msg.map

If you ever need to generate the **gen-sid.map** file manually the process is described here:

    cat /etc/snort/rules/sid-msg.map | awk -F '|' '{print "1 || "$1" || "$3}' > /etc/snort/rules/gen-msg.map

**Pulledpork** already takes care of the **sid-msg.map** file and it sounds like it will get to the **gen-msg.map** file eventually as well.

#### Suricata Configuration

Since we will be using **barnyard2** let's configure **suricata** to log output in *unified2* format:

    outputs:

      # a line based alerts log similar to Snort's fast.log
      - fast:
          enabled: yes
          filename: fast.log
          append: yes

      - unified2-alert:
          enabled: yes
          filename: merged.log

Since we will be running in daemon mode let's disable console mode:

    logging:

     outputs:
      - console:
          enabled: no
      - file:
          enabled: yes
          filename: /var/log/suricata/suricata.log
      - syslog:
          enabled: no
          facility: local5
          format: "[%i] <%d> -- "

With Suricata you can actually reload rules without restarting the whole daemon (pretty cool). Here is the setting for that:

    detect-engine:
      - profile: medium
      - custom-values:
          toclient-src-groups: 2
          toclient-dst-groups: 2
          toclient-sp-groups: 2
          toclient-dp-groups: 3
          toserver-src-groups: 2
          toserver-dst-groups: 4
          toserver-sp-groups: 2
          toserver-dp-groups: 25
      - sgh-mpm-context: auto
      - inspection-recursion-limit: 3000
      # When rule-reload is enabled, sending a USR2 signal to the Suricata process
      # will trigger a live rule reload. Experimental feature, use with care.
      - rule-reload: true

Lastly make sure the configuration is okay:

    elatov@moxz:~$sudo suricata -c /usr/local/etc/suricata/suricata.yaml -T -i em0
    4/1/2015 -- 16:05:52 - <Info> - Running suricata under test mode

Then add the following to **/etc/rc.conf** to enable the suricata daemon:

    elatov@moxz:~$grep suricata /etc/rc.conf
    suricata_enable="YES"
    suricata_interface="em0"
    suricata_flags="-D -v"

Then you can start the service with the following:

    elatov@moxz:~$sudo service suricata start

and don't forget to start **barnyard2** (btw the full setup for that and snorby are [here](/2014/12/snort-on-freebsd-10/)):

    elatov@moxz:~$sudo service barnyard2 start

If you update the rules, you can run the following to reload them. First find out the PID:

    elatov@moxz:~$ps -auwwx | grep suri
    root     27081 107.9 31.4 741544 650528  -  Ss    4:10PM     0:10.27 /usr/local/bin/suricata -D -v -i em0 --pidfile /var/run/suricata_em0.pid -c /usr/local/etc/suricata/suricata.yaml

and then send a **USR2** signal to the procees:

    elatov@moxz:~$sudo kill -USR2 27081

and if you check out the logs (**/var/log/suricata/suricata.log**) you will see the following:


    4/1/2015 -- 16:10:47 - <Notice> - rule reload starting
    4/1/2015 -- 16:10:47 - <Info> - IP reputation disabled

    4/1/2015 -- 16:10:52 - <Info> - 1 rule files processed. 21150 rules successfully loaded, 1319 rules failed
    4/1/2015 -- 16:10:52 - <Info> - 21158 signatures processed. 1075 are IP-only rules, 7314 are inspecting packet payload, 15524 inspect application layer, 72 are decoder event only
    4/1/2015 -- 16:10:52 - <Info> - building signature grouping structure, stage 1: preprocessing rules... complete
    4/1/2015 -- 16:10:53 - <Info> - building signature grouping structure, stage 2: building source address list... complete
    4/1/2015 -- 16:10:56 - <Info> - building signature grouping structure, stage 3: building destination address lists... complete
    4/1/2015 -- 16:10:58 - <Info> - Threshold config parsed: 0 rule(s) found
    4/1/2015 -- 16:10:58 - <Info> - Live rule swap has swapped 1 old det_ctx's with new ones, along with the new de_ctx
    4/1/2015 -- 16:10:58 - <Info> - cleaning up signature grouping structure... complete
    4/1/2015 -- 16:10:58 - <Notice> - rule reload complete

You will notice some rules failed to load and those are the VRT rules that are not written specificly for Suricata but only Snort. After some time you will see new events getting fired:

    elatov@moxz:~$ls -lart /var/log/suricata/ | tail -4
    -rw-r--r--  1 root   wheel  1852307 Jan  4 16:10 suricata.log
    -rw-r-----  1 root   wheel      194 Jan  4 16:15 merged.log.1420413029
    -rw-r-----  1 root   wheel     4513 Jan  4 16:15 fast.log
    -rw-r--r--  1 snort  snort     2056 Jan  4 16:15 barnyard2.waldo

I enabled the **fast.log** just for now so I could see what alerts are getting fired without checking snorby or the DB. And I saw the following:

    elatov@moxz:~$tail -4 /var/log/suricata/fast.log 
    01/04/2015-08:08:39.990476  [**] [1:2210016:1] SURICATA STREAM CLOSEWAIT FIN out of window [**] [Classification: (null)] [Priority: 3] {TCP} 10.0.0.3:10050 -> 10.0.0.2:52628
    01/04/2015-12:24:02.543448  [**] [1:2100366:8] GPL ICMP_INFO PING *NIX [**] [Classification: Misc activity] [Priority: 3] {ICMP} 192.168.1.114:8 -> 10.0.0.3:0
    01/04/2015-14:02:00.402123  [**] [1:2522386:2079] ET TOR Known Tor Relay/Router (Not Exit) Node Traffic group 194 [**] [Classification: Misc Attack] [Priority: 2] {UDP} 173.255.194.200:123 -> 10.0.0.3:123
    01/04/2015-16:15:16.557229  [**] [1:2100366:8] GPL ICMP_INFO PING *NIX [**] [Classification: Misc activity] [Priority: 3] {ICMP} 192.168.1.114:8 -> 10.0.0.3:0


Notice I have a ping test alert.
