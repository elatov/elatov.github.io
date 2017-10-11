---
published: false
layout: post
title: "Creating a VIB to modify a Firewall Rule on an ESXi Host"
author: Karim Elatov
categories: [vmware,containers]
tags: [logstash,vib,docker,vibauthor]
---
### ESXi Logstash Example
I ran into these *filter* examples for *ESXi* logs with **logstash**:

* [Grok ESXi 5.x Pattern (for Logstash) (including puppet format with special escaping!)](https://gist.github.com/martinseener/5238576)
* [sof-elk](https://github.com/philhagen/sof-elk/blob/master/configfiles/1029-preprocess-esxi.conf)


So I decided to implement that. First I created the custom config on the **logstash** side:

	<> cat /etc/logstash/conf.d/esxi.conf
	input {
	  tcp {
	    port => 5004
	    type => "esxi"
	  }
	  udp {
	    port => 5004
	    type => "esxi"
	  }
	}
	
	filter {
	  grok {
	      match => { "message" => "(?:%{SYSLOGTIMESTAMP:timestamp}|%{TIMESTAMP_ISO8601:timestamp8601}) (?:%{SYSLOGHOST:logsource}) (?:%{SYSLOGPROG}): (?<messagebody>(?:\[(?<esxi_thread_id>[0-9A-Z]{8,8}) %{DATA:esxi_loglevel} \'%{DATA:esxi_service}\'\] %{GREEDYDATA:esxi_message}|%{GREEDYDATA}))" }
	    }
	
	   mutate {
	     remove_tag => [ "_grokparsefailure", "_geoip_lookup_failure" ]
	   }
	
	
	}
	
	output {
	  if "esxi" in [type] {
	     elasticsearch { hosts => ["http://core.kar.int:9200"] }
	     file { path => "/var/log/logstash/esxi-syslog.log" codec => rubydebug }
	  }
	#  stdout { codec => rubydebug }
	}

Then I checked to make sure the configuration was okay:

	<> sudo /usr/share/logstash/bin/logstash --config.test_and_exit --path.settings=/etc/logstash/ -f /etc/logstash/conf.d/esxi.conf

Next I restarted the **logstash** service to apply the new config: 

	<> sudo systemctl restart logstash.service

Also, don't forget to open up the firewall in **iptables** on the machine running **logstash**:

	<> sudo iptables -L -n -v | grep 5004
	    1    60 ACCEPT     tcp  --  *      *       192.168.1.0/24       0.0.0.0/0            state NEW tcp dpt:5004 flags:0x17/0x02

### ESXi Remote Syslog
Now I needed to configure the syslog client on the *ESXi* side. First check the current config:
	
	[root@hp:~] esxcli system syslog config get
	Default Network Retry Timeout: 180
	Dropped Log File Rotation Size: 100
	Dropped Log File Rotations: 10
	Enforce SSLCertificates: false
	Local Log Output: /scratch/log
	Local Log Output Is Configured: false
	Local Log Output Is Persistent: true
	Local Logging Default Rotation Size: 1024
	Local Logging Default Rotations: 8
	Log To Unique Subdirectory: false
	Message Queue Drop Mark: 90
	Remote Host: udp://192.168.1.106:514

Then to add my **logstash** host:

	[root@hp:~] esxcli system syslog config set --loghost='tcp://10.0.0.6:5004,udp://192.168.1.106:514'

Next we can confirm the setting is configured:

	[root@hp:~] esxcli system syslog config get
	Default Network Retry Timeout: 180
	Dropped Log File Rotation Size: 100
	Dropped Log File Rotations: 10
	Enforce SSLCertificates: false
	Local Log Output: /scratch/log
	Local Log Output Is Configured: false
	Local Log Output Is Persistent: true
	Local Logging Default Rotation Size: 1024
	Local Logging Default Rotations: 8
	Log To Unique Subdirectory: false
	Message Queue Drop Mark: 90
	Remote Host: tcp://10.0.0.6:5004,udp://192.168.1.106:514

And lastly **reload** the service on the *ESXi* host to actually apply the settings:

	[root@hp:~] esxcli system syslog reload

And that was it. Next I needed to open up the outbound port on the *ESXi* host.

### ESXi Custom Firewall Rule
I wanted to create a custom rule, so I ran into a couple of sites that talked about the process:

* [Creating Custom VIBs For ESXi 5.0 & 5.1 with VIB Author Fling](http://www.virtuallyghetto.com/2012/09/creating-custom-vibs-for-esxi-50-51.html)
* [How to create persistent firewall rules on ESXi](https://www.altaro.com/vmware/how-to-create-persistent-firewall-rules-on-esxi/)
* [User defined xml firewall configurations are not persistent across ESXi host reboots (2007381)](https://kb.vmware.com/kb/2007381)
* [A Docker Container for building custom ESXi VIBs](http://www.virtuallyghetto.com/2015/05/a-docker-container-for-building-custom-esxi-vibs.html)

#### Deploying the VIB Author Container
So I deciced to use the *container* approach. I already had a *CoreOS* machine which
is able to deploy *containers*. So let's create a directory with all the settings
and configurations to be able to deploy the container with **docker-compose** and to run **vibauthor** from inside the *container*:

	coreos <> tree
	.
	├── conf
	│   └── stage
	│       ├── descriptor.xml
	│       └── payloads
	│           └── payload1
	│               └── etc
	│                   └── vmware
	│                       └── firewall
	│                           └── custom-firewall.xml
	└── docker-compose.yml

Here is how each file looked like:

	coreos # cat docker-compose.yml
	version: '2'
	services:
	
	    vib-auth:
	       image: lamw/vibauthor
	       container_name: vib-auth
	       hostname: vib-auth
	       stdin_open: true
	       tty: true
	       command: /bin/bash
	       volumes:
	        - "./conf:/root/conf"
	       network_mode: "bridge"

And here is the **descriptor.xml**:

	coreos # cat conf/stage/descriptor.xml
	<vib version="5.0">
	<type>bootbank</type>
	<name>custom-firewall</name>
	<version>5.0.0-6.5.0</version>
	 <vendor>Home</vendor>
	 <summary>Add Custom Firewall Rules</summary>
	 <description>Adds outbound ports</description>
	 <relationships>
	  <depends></depends>
	  <conflicts/>
	  <replaces/>
	  <provides/>
	  <compatibleWith/>
	 </relationships>
	 <software-tags>
	 </software-tags>
	 <system-requires>
	  <maintenance-mode>false</maintenance-mode>
	 </system-requires>
	 <file-list>
	  <file></file>
	 </file-list>
	 <acceptance-level>community</acceptance-level>
	 <live-install-allowed>true</live-install-allowed>
	 <live-remove-allowed>true</live-remove-allowed>
	 <cimom-restart>false</cimom-restart>
	 <stateless-ready>true</stateless-ready>
	 <overlay>false</overlay>
	 <payloads>
	  <payload name="payload1" type="vgz"></payload>
	 </payloads>
	</vib>

And lastly the custom firewall rule:

	coreos # cat conf/stage/payloads/payload1/etc/vmware/firewall/custom-firewall.xml
	<ConfigRoot>
	<service id='0100'>
	 <id>custom-firewall</id>
	  <rule id='0000'>
	   <direction>outbound</direction>
	   <protocol>tcp</protocol>
	   <porttype>dst</porttype>
	    <port>
	     <begin>5004</begin>
	     <end>5004</end>
	    </port>
	  </rule>
	 <enabled>true</enabled>
	 <required>false</required>
	</service>
	</ConfigRoot>

Now let's start the container and (since we specified in our **docker-compose.yml* to attach to it) attach to it:

	coreos # docker-compose run --rm vib-auth
	Pulling servicename (lamw/vibauthor:latest)...
	latest: Pulling from lamw/vibauthor
	a3ed95caeb02: Pull complete
	   32 B/32 B: Pull complete
	e6ba256426b4: Pull complete
	e1e679c17ede: Pull complete
	4d2bb16cd1c5: Pull complete
	Digest: sha256:5a98efa63042860ddfe17bfb5be7080baf30d04c98bc7601632c9beb21df375c
	Status: Downloaded newer image for lamw/vibauthor:latest
	version: '2'
	Creating vib-auth
	Attaching to vib-auth
	[root@vib-auth ~]# ls
	conf  vmware-esx-vib-author-5.0.0-0.0.847598.i386.rpm

Now let's run the **vibauthor** command (this is inside the **vib-auth** container) to create our **VIB**:

	[root@vib-auth conf]# vibauthor -C -t stage -v custom-fw.vib -f
	Successfully created custom-fw.vib.

Now let's confirm it looks okay:

	[root@vib-auth conf]# vibauthor -i -v custom-fw.vib
	**** Info for VIB: custom-fw.vib ****
	VIB Format:             2.0.0
	VIB ID:                 Home_bootbank_custom-firewall_5.0.0-6.5.0
	VIB Type:               bootbank
	Name:                   custom-firewall
	Version:                5.0.0-6.5.0
	Vendor:                 Home
	Summary:                [Fling] Add Custom Firewall Rules
	Description:            Adds outbound ports
	Creation Date:          2017-10-01 02:11:58.828467+00:00
	Provides:
	        custom-firewall = 5.0.0-6.5.0
	Depends:
	Conflicts:
	Replaces:
	        custom-firewall << 5.0.0-6.5.0
	Software Tags:          []
	MaintenanceMode:        remove/update: False, installation: False
	Signed:                 False
	AcceptanceLevel:        community
	LiveInstallAllowed:     True
	LiveRemoveAllowed:      True
	CimomRestart:           False
	StatelessReady:         True
	Overlay:                False
	Payloads:
	  Name            Type        Boot Size        Checksums
	  payload1        vgz         0    367         sha-256 9f16107f3efe07614059f1df0d74856bbb2ef2d319987a5ba4a1d5f11f973873
	                                               sha-1 53a6a0432279d2c25aa835f60f58e9fe935ce95f

Now we can just **exit** and the *container* will be stopped and destroyed, but since we shared a local *volume* with the *container* our **VIB** will be on the CoreOS machine. 

#### Install Custom VIB on ESXi Host
At this point we can just copy the **VIB** to the *ESXi* machine:

	coreos # scp conf/custom-fw.vib root@hp:/vmfs/volumes/datastore1/drivers/.
	The authenticity of host 'hp (192.168.1.109)' can't be established.
	RSA key fingerprint is SHA256:diFTHho/h4qHDypkR2zQJT9+nOeYgDG1jVENXYVjJ/0.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added 'hp,192.168.1.109' (RSA) to the list of known hosts.
	Password:
	custom-fw.vib                                 100% 1642     2.5MB/s   00:00

Now we can SSH to our ESXi host and finally install the **VIB** on it:

	[root@hp:~] esxcli software vib install -v /vmfs/volumes/datastore1/drivers/custom-fw.vib
	Installation Result
	   Message: Operation finished successfully.
	   Reboot Required: false
	   VIBs Installed: Home_bootbank_custom-firewall_5.0.0-6.5.0
	   VIBs Removed:
	   VIBs Skipped:

You can confirm it's installed:

	[root@hp:~] esxcli software vib list | grep -i custom
	custom-firewall                5.0.0-6.5.0                           Home     CommunitySupported  2017-10-01

Here is the new file:

	[root@hp:~] ls /etc/vmware/firewall/
	custom-firewall.xml  service.xml          vsanhealth.xml

And let's see if the rule loaded:

	[root@hp:~] esxcli network firewall ruleset list | grep cust
	custom-firewall              true

And the actual port that rule opens:

	[root@hp:~] esxcli network firewall ruleset rule list -r custom-firewall
	Ruleset          Direction  Protocol  Port Type  Port Begin  Port End
	---------------  ---------  --------  ---------  ----------  --------
	custom-firewall  Outbound   TCP       Dst              5004      5004

Just for reference this was on *ESXi* 6.5u1:

	[root@hp:~] vmware -lv
	VMware ESXi 6.5.0 build-5969303
	VMware ESXi 6.5.0 Update 1

You might have to run the **reload** command after the firewall rule is in place:

	[root@hp:~]esxcli system syslog reload

### Confirm ESXi logs are getting to Logstash
Since in the configuration above I configured **logstash** to write the logs to the local filesystem, I was able to confirm the logs are getting to **logstash**:

	$ less /var/log/logstash/esxi-syslog.log
	{
	    "syslog_severity_code" => 5,
	         "syslog_facility" => "user-level",
	    "syslog_facility_code" => 1,
	           "timestamp8601" => "2017-10-01T02:20:54.492Z",
	                 "program" => "Hostd",
	                 "message" => "<167>2017-10-01T02:20:54.492Z hp.kar.int Hostd: verbose hostd[B903B70] [Originator@6876 sub=PropertyProvider] RecordOp ASSIGN: guest.disk, 4. Sent notification immediately.",
	                    "type" => "esxi",
	               "logsource" => "hp.kar.int",
	         "syslog_severity" => "notice",
	                    "tags" => [],
	             "messagebody" => "verbose hostd[B903B70] [Originator@6876 sub=PropertyProvider] RecordOp ASSIGN: guest.disk, 4. Sent notification immediately.",
	              "@timestamp" => 2017-10-01T02:21:10.995Z,
	                    "port" => 15737,
	                "@version" => "1",
	                    "host" => "192.168.1.109"
	                    
And that was it.
