---
title: SRM 5.0 Times out on a test failover when using Mirrorview SRA 5.0.1
author: Jarret Lavallee
layout: post
permalink: /2012/08/srm-5-0-times-out-on-a-test-failover-when-using-mirrorview-sra-5-0-1/
dsq_thread_id:
  - 1406784162
categories:
  - SRM
  - Storage
  - VMware
tags:
  - EMC
  - EMC Clariion
  - logs
  - sra
  - srm
  - troubleshooting
---
Recently I had a customer that could not get a test failover to work. The test would fail during &#8220;Prepare Storage&#8221; after 300 seconds. After increasing the timeout to 15 minutes the test would still timeout. This customer was using a CX4-120 with Mirrorview 5.0.1.

The test failover would return the following error. 

[code]  
Failed to create snapshots of replica devices. Timed out (301 seconds) while waiting for SRA to complete &apos;testFailoverStart&apos; command. Failed to create snapshots of replica devices. Timed out (301 seconds) while waiting for SRA to complete &apos;testFailoverStart&apos; command.  
[/code]

I previously wrote an article about how <a href="http://virtuallyhyper.com/2012/03/how-does-srm-communicate-with-the-array/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/how-does-srm-communicate-with-the-array/']);" title="How does SRM communicate with the array?">SRM communicates with the SRA</a>. We can use this knowledge to figure out the problem here, as the &#8220;Prepare Storage&#8221; section in a test failover is when SRM is waiting for the array to fulfill some tasks.

Preparing storage is the part where the SRM server calls a &#8220;testFailoverStart&#8221; to the SRA. The SRA takes the command and tells the array to create a writable snapshot of each of the LUNs and present them to the initiators listed in the input XML document. The command should complete with a return xml document. 

Here is what the customer was seeing when the testFailoverStart was called.

[code]  
2012-07-20T12:41:08.528-07:00 [03428 info 'SraCommand' opID=75FAD1DE-0000014C] Command line for testFailoverStart: "C:\Program Files (x86)\VMware\VMware vCenter Site Recovery Manager\external\perl-5  
.8.8\bin\perl.exe" "C:/Program Files (x86)/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC VNX SRA/command.pl"  
2012-07-20T12:41:08.528-07:00 [03428 verbose 'SraCommand' opID=75FAD1DE-0000014C] Input for testFailoverStart:  
--> <?xml version="1.0" encoding="UTF-8"?>  
--> <Command xmlns="http://www.vmware.com/srm/sra/v2">  
--> <Name>testFailoverStart</Name>  
--> <OutputFile>C:\Windows\TEMP\vmware-SYSTEM\sra-output-20-0</OutputFile>  
--> <StatusFile>C:\Windows\TEMP\vmware-SYSTEM\sra-status-21-0</StatusFile>  
--> <LogLevel>verbose</LogLevel>  
--> <LogDirectory>C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\SRAs\EMC VNX SRA</LogDirectory>  
--> <Connections>  
--> <Connection id="EMC Storage">  
--> <Addresses>  
--> <Address id="emcstorage.address">172.16.0.10</Address>  
--> </Addresses>  
--> <Username>\***</Username>  
--> <Password>\***</Password>  
--> <Opaques>  
--> <Opaque id="mirrorview.address.spb">172.16.0.11</Opaque>  
--> </Opaques>  
--> </Connection>  
--> </Connections>  
--> <TestFailoverStartParameters>  
--> <ArrayId>50:06:01:60:01:23:45:67</ArrayId>  
--> <AccessGroups>  
--> <AccessGroup id="domain-c36">  
--> <Initiator id="21:00:00:00:11:22:AB:CD" type="FC"/>  
--> <Initiator id="21:00:00:00:11:22:AB:EF" type="FC"/>  
--> <Initiator id="21:00:00:00:11:22:AB:01" type="FC"/>  
--> <Initiator id="21:00:00:00:11:22:AB:12" type="FC"/>  
--> <Initiator id="21:00:00:00:11:23:AB:23" type="FC"/>  
--> <Initiator id="21:00:00:00:11:23:AB:34" type="FC"/>  
--> </AccessGroup>  
--> </AccessGroups>  
--> <TargetDevices>  
--> <TargetDevice key="async-LUN 11">  
--> <AccessGroups>  
--> <AccessGroup id="domain-c36"/>  
--> </AccessGroups>  
--> </TargetDevice>  
--> <TargetDevice key="async-LUN 12">  
--> <AccessGroups>  
--> <AccessGroup id="domain-c36"/>  
--> </AccessGroups>  
--> </TargetDevice>  
--> <TargetDevice key="async-LUN 20">  
--> <AccessGroups>  
--> <AccessGroup id="domain-c36"/>  
--> </AccessGroups>  
--> </TargetDevice>  
--> <TargetDevice key="async-Lun 10">  
--> <AccessGroups>  
--> <AccessGroup id="domain-c36"/>  
--> </AccessGroups>  
--> </TargetDevice>  
--> </TargetDevices>  
--> </TestFailoverStartParameters>  
--> </Command>

[/code]

From the XML input we can see that the SRM wants LUNs async-LUN 11, async-LUN 12, async-LUN 20 and async-Lun 10 to be snapshoted and presented to the initators. Since this is sent into the SRA, the SRA should parse the xml documents and then run the tasks to accomplish this. SRM then listens for updates to a file to determine when the command done.

Looking above we see the start time is 12:41:08. At 12:46:08 the SRM hits it 5 minute timeout and kills the SRA process.

[code]  
2012-07-20T12:46:08.602-07:00 [03432 warning 'SysCommandLineWin32'] AsyncWaitForExit: timeout occured after '300062000' microseconds  
2012-07-20T12:46:08.602-07:00 [03432 error 'Default'] SysCommand failed to return an exit code - killing it.  
[/code]

So we know that the issue is with the SRA/Array. In SRA v2+ VMware has requested that the SRA vendors log for each command that is run. The Mirrorview SRA does logs each command that was sent in, so we can look at those logs. We find a log named sra\_testFailoverStart\_07-20-2012_12-41-08.668.log, which corresponds with the testFailoverStart that was called at 12:41:08. This log contains the standard output from the SRA command. Each SRA is different, but we can follow the sequence of events and figure out what the SRA is hanging on. 

Following the sequence of events, the first thing we see is the SRA querying the array for it&#8217;s information.

[code]  
2012-07-20 12:41:09,106 [com.emc.sra.mirrorview.MirrorviewCommands]: MirrorView Enabler Version: 5.0.17  
2012-07-20 12:41:09,106 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: arrayname  
2012-07-20 12:41:10,481 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Array Name: CX-SP2), stderr()  
2012-07-20 12:41:10,481 [com.emc.sra.ResponseBuilder]: Using enabler 'Mirrorview'...  
2012-07-20 12:41:10,497 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: getarrayuid  
2012-07-20 12:41:11,840 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Hostname Array UID  
\---\---\-- -\---\---\---  
CX-SP2A 50:06:01:60:01:23:45:67), stderr()  
2012-07-20 12:41:11,840 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: getagent  
2012-07-20 12:41:13,200 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Agent Rev: 7.30.13 (0.99)  
Name: K10  
Desc:  
Node: A-APM00111123456  
Physical Node: K10  
Signature: 2123456  
Peer Signature: 2123457  
Revision: 04.30.000.5.523  
SCSI Id: 0  
Model: CX4-120  
Model Type: Rackmount  
Prom Rev: 5.30.00  
SP Memory: 3040  
Serial No: APM00111123456  
SP Identifier: A  
Cabinet: ABC5), stderr() 

[/code]

It then goes on to query the first LUN.

[code]  
2012-07-20 12:41:16,591 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: mirror -async -list -name "LUN 10"  
2012-07-20 12:41:18,637 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(MirrorView Name: LUN 10  
MirrorView Description:  
MirrorView UID: AB:CD:EF:01:23:45:67:89:01:00:00:00:00:00:00:00  
Logical Unit Numbers: 10  
Remote Mirror Status: Secondary Copy  
MirrorView State: Active  
MirrorView Faulted: NO  
MirrorView Transitioning: NO  
Minimum number of images required: 0  
Image Size: 1153433600  
Image Count: 2  
Rollback Throttle: Not Available  
Images:  
Image UID: AB:CD:EF:12:34:56:78:90  
Is Image Primary: YES  
Logical Unit UID: 12:34:56:78:90:AB:CD:EF:FE:DC:BA:98:76:54:32:10  
Image Condition: Primary Image

Image UID: 50:06:01:60:01:23:45:67  
Is Image Primary: NO  
Logical Unit UID: 60:06:01:60:AB:CD:EF:01:34:56:78:91:23:45:56:78  
Image State: Consistent  
Image Condition: Normal  
Recovery Policy: Automatic  
Synchronization Rate: Medium  
Image Faulted: NO  
Image Transitioning: NO  
Synchronizing Progress(%): 100  
Update Type: Manual  
Update Period, in minutes: N/A  
Time in minutes since previous update: 151  
Time in minutes until next update: Not Available  
Last Image Error: Not Available), stderr()  
2012-07-20 12:41:18,637 [com.emc.mirrorview.platform.lun.LunServiceImpl]: Retrieving information for LUN 10...  
2012-07-20 12:41:18,637 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: getlun 10 -name -owner -default -capacity  
2012-07-20 12:41:20,169 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Name LUN 10  
Current owner: SP B  
Default Owner: SP A  
LUN Capacity(Megabytes): 563200  
LUN Capacity(Blocks): 1153433600), stderr()  
2012-07-20 12:41:20,169 [com.emc.mirrorview.platform.lun.HashMapLunRepository]: Caching LUN 10 with name: LUN 10 

[/code]

List snapshots for the array

[code]  
2012-07-20 12:41:20,169 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: snapview -listsnapshots  
2012-07-20 12:41:22,231 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(), stderror()  
[/code]

Since there are no snapshots for this LUN, the SRA creates one.

[code]  
2012-07-20 12:41:22,231 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Creating SnapView snapshot with name: async-LUN 10_SRM-TEST-FAILOVER, of LUN: 10  
2012-07-20 12:41:22,231 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Searching for current SP owner of lun: 10  
2012-07-20 12:41:22,231 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -createsnapshot 10 -snapshotname "async-LUN 10_SRM-TEST-FAILOVER"  
2012-07-20 12:41:25,153 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(), stderr()  
[/code]

List the snapshot we just created.

[code]  
2012-07-20 12:41:25,153 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Retrieving info for SnapView snapshot with name: async-LUN 10_SRM-TEST-FAILOVER  
2012-07-20 12:41:25,153 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -listsnapshots -snapshotname "async-LUN 10_SRM-TEST-FAILOVER"  
2012-07-20 12:41:27,388 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(SnapView logical unit name: async-LUN 10_SRM-TEST-FAILOVER  
SnapView logical unit ID: 60:06:01:60:AB:89:67:56:45:34:23:12:01:AB:CD:EF  
Target Logical Unit: 10  
State: Inactive), stderr()  
[/code]

Start a session for the snapshot LUN and check the session.

[code]  
2012-07-20 12:41:27,388 [com.emc.mirrorview.platform.snapshot.session.SnapviewSessionServiceImpl]: Starting SnapView session with name: async-LUN 10\_SRM-TEST-FAILOVER\_session, for snapshot: async-LUN 10_SRM-TEST-FAILOVER  
2012-07-20 12:41:27,388 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -startsession "async-LUN 10\_SRM-TEST-FAILOVER\_session" -snapshotname "async-LUN 10_SRM-TEST-FAILOVER" -persistence  
2012-07-20 12:41:31,450 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(You must activate a snapshot on this session before you can access it.), stderr()  
2012-07-20 12:41:31,450 [com.emc.mirrorview.platform.snapshot.session.SnapviewSessionServiceImpl]: Retrieving info for SnapView session with name async-LUN 10\_SRM-TEST-FAILOVER\_session  
2012-07-20 12:41:31,450 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -listsessions -name "async-LUN 10\_SRM-TEST-FAILOVER\_session"  
2012-07-20 12:41:33,654 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(Name of the session: async-LUN 10\_SRM-TEST-FAILOVER\_session  
Number of read requests serviced by the snapview cache pool: 0  
Total number of read requests on the snapview logical unit: 0  
Number of reads from the TLU: 0  
Number of writes requests in the session: 0  
Number of writes requests to cache that triggered a COW: 0  
Total number of writes requests on the snapview target logical unit: 0  
Number of writes requests larger than the chunk size: 0  
Cache Capacity in GB: 818.864624  
Session Usage: 0  
List of Target Logical Units: LUN 10  
snap Logical Units UID:  
snap Logical Units Name:  
Session in persistence: YES  
Session creation time: 07/20/12 12:46:22  
Session state: Normal), stderr()  
[/code]

Activate the snapshot and check

[code]  
2012-07-20 12:41:33,654 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Activating SnapView snapshot with name: async-LUN 10\_SRM-TEST-FAILOVER, on session: async-LUN 10\_SRM-TEST-FAILOVER_session  
2012-07-20 12:41:33,654 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Searching for current SP owner of lun: 10  
2012-07-20 12:41:33,654 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -activatesnapshot "async-LUN 10\_SRM-TEST-FAILOVER\_session" -snapshotname "async-LUN 10_SRM-TEST-FAILOVER"  
2012-07-20 12:41:35,872 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(), stderr()  
2012-07-20 12:41:35,872 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Searching for current SP owner of lun: 10  
2012-07-20 12:41:35,872 [com.emc.mirrorview.platform.snapshot.SnapviewSnapshotServiceImpl]: Retrieving info for SnapView snapshot with name: async-LUN 10_SRM-TEST-FAILOVER  
2012-07-20 12:41:35,872 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Executing command: snapview -listsnapshots -snapshotname "async-LUN 10_SRM-TEST-FAILOVER"  
2012-07-20 12:41:38,060 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.11 Command result: stdout(SnapView logical unit name: async-LUN 10_SRM-TEST-FAILOVER  
SnapView logical unit ID: 60:06:01:60:AB:89:67:56:45:34:23:12:01:AB:CD:EF  
Target Logical Unit: 10  
State: Active  
Session Name: async-LUN 10\_SRM-TEST-FAILOVER\_session), stderr()  
[/code]

So we have the LUN active and ready to be presented to a host. The SRA then needs to add it to a storage group. The CX/VNX should only have a host in a single storage group, so the SRA scans for existsing storage groups with the initiatiors that we need.

[code]  
2012-07-20 12:41:40,170 [com.emc.mirrorview.platform.storagegroup.HashMapStorageGroupRepository]: Retrieving storage group information...  
2012-07-20 12:41:40,170 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: storagegroup -list  
2012-07-20 12:41:41,748 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Storage Group Name: ABC SRM  
Storage Group UID: DD:CC:BB:AA:00:11:22:33:44:55:66:87:09:AB:DC:FE  
HBA/SP Pairs:

HBA UID SP Name SPPort  
\---\---\- --\---\-- -\-----  
20:00:00:00:11:22:AB:01:21:00:00:00:11:22:AB:01 SP B 1  
20:00:00:00:11:23:AB:23:21:00:00:00:11:23:AB:23 SP A 0  
20:00:00:00:11:23:AB:34:21:00:00:00:11:23:AB:34 SP B 0  
20:00:00:00:11:23:AB:34:21:00:00:00:11:23:AB:34 SP A 1  
20:00:00:00:11:23:AB:23:21:00:00:00:11:23:AB:23 SP B 1  
20:00:00:00:11:22:AB:CD:21:00:00:00:11:22:AB:CD SP A 0  
20:00:00:00:11:22:AB:01:21:00:00:00:11:22:AB:01 SP A 0  
20:00:00:00:11:22:AB:EF:21:00:00:00:11:22:AB:EF SP B 0  
20:00:00:00:11:22:AB:12:21:00:00:00:11:22:AB:12 SP B 0  
20:00:00:00:11:22:AB:EF:21:00:00:00:11:22:AB:EF SP A 1  
20:00:00:00:11:22:AB:12:21:00:00:00:11:22:AB:12 SP A 1  
20:00:00:00:11:22:AB:CD:21:00:00:00:11:22:AB:CD SP B 1

HLU/ALU Pairs:

HLU Number ALU Number  
\---\---\---\- --\---\-----  
70 70  
Shareable: YES), stderr() 

[/code]

Since the &#8220;ABC SRM&#8221; storage group has all of the initiators, the SRA decides to add the snapshot to this group.

[code]  
2012-07-20 12:41:41,748 [com.emc.mirrorview.platform.storagegroup.HashMapStorageGroupRepository]: Adding snapshot async-LUN 10_SRM-TEST-FAILOVER to storage group ABC SRM with hlu 255  
2012-07-20 12:41:41,748 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: storagegroup -addsnapshot -gname "ABC SRM" -snapshotname "async-LUN 10_SRM-TEST-FAILOVER" -hlu 255  
2012-07-20 12:41:43,904 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Error: storagegroup command failed  
The group name entered does not match any storage groups for this array), stderr()  
[/code]

The operation does not throw anything in stderror, but does not add the LUN to the group because it cannot find the group. The SRA then queries the storage groups again to see if this LUN was added in (hlu 255)

[code]  
2012-07-20 12:41:43,904 [com.emc.mirrorview.platform.storagegroup.HashMapStorageGroupRepository]: Retrieving storage group information...  
2012-07-20 12:41:43,904 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: storagegroup -list  
2012-07-20 12:41:45,435 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Storage Group Name: ABC SRM  
Storage Group UID: DD:CC:BB:AA:00:11:22:33:44:55:66:87:09:AB:DC:FE  
HBA/SP Pairs:

HBA UID SP Name SPPort  
\---\---\- --\---\-- -\-----  
20:00:00:00:11:22:AB:01:21:00:00:00:11:22:AB:01 SP B 1  
20:00:00:00:11:23:AB:23:21:00:00:00:11:23:AB:23 SP A 0  
20:00:00:00:11:23:AB:34:21:00:00:00:11:23:AB:34 SP B 0  
20:00:00:00:11:23:AB:34:21:00:00:00:11:23:AB:34 SP A 1  
20:00:00:00:11:23:AB:23:21:00:00:00:11:23:AB:23 SP B 1  
20:00:00:00:11:22:AB:CD:21:00:00:00:11:22:AB:CD SP A 0  
20:00:00:00:11:22:AB:01:21:00:00:00:11:22:AB:01 SP A 0  
20:00:00:00:11:22:AB:EF:21:00:00:00:11:22:AB:EF SP B 0  
20:00:00:00:11:22:AB:12:21:00:00:00:11:22:AB:12 SP B 0  
20:00:00:00:11:22:AB:EF:21:00:00:00:11:22:AB:EF SP A 1  
20:00:00:00:11:22:AB:12:21:00:00:00:11:22:AB:12 SP A 1  
20:00:00:00:11:22:AB:CD:21:00:00:00:11:22:AB:CD SP B 1

HLU/ALU Pairs:

HLU Number ALU Number  
\---\---\---\- --\---\-----  
70 70  
Shareable: YES), stderr() 

[/code]

There is no 255 in the HLU output, so the SRA tries to add it again.

[code]  
2012-07-20 12:41:45,435 [com.emc.mirrorview.platform.storagegroup.HashMapStorageGroupRepository]: Adding snapshot async-LUN 10_SRM-TEST-FAILOVER to storage group ABC SRM with hlu 255  
2012-07-20 12:41:45,435 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Executing command: storagegroup -addsnapshot -gname "ABC SRM" -snapshotname "async-LUN 10_SRM-TEST-FAILOVER" -hlu 255  
2012-07-20 12:41:47,420 [com.emc.mirrorview.platform.naviseccli.NaviseccliConnection]: 172.16.0.10 Command result: stdout(Error: storagegroup command failed  
The group name entered does not match any storage groups for this array), stderr()  
[/code]

The adding the lun to the storage group and checking for it continues in a loop over and over until SRM kills the process at 12:46:08. So the reason for the timeout was that the SRA was in an infinte loop trying to add the snapshot LUN to a storage group. No matter how long we set the timeout, the operation would still fail because of this problem.

It seems like the SRA does not check for the failed operation, or that naviseccli does not return errors to stderror. Either way, we can correct the trigger for this issue to resolve it. 

The error from the &#8220;storagegroup addsnapshot&#8221; command was &#8220;The group name entered does not match any storage groups for this array&#8221;. We can see that the name of the group is &#8220;ABC SRM&#8221; and that it was called in with quotes. For some reason naviseccli is not interpreting the double spaces correctly. 

To correct this we went into unisphere and selected the hostgroup and clicked edit. We changed the name to get rid of the double spaces and replace them with a single underscore to make the new name &#8220;ABC_SRM&#8221;. I was able to change the storage group name live, but I would suggest talking with EMC on best practices.

After making the change, we ran the test failover again and it worked with out any problems. 

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/srm-5-0-times-out-on-a-test-failover-when-using-mirrorview-sra-5-0-1/" title=" SRM 5.0 Times out on a test failover when using Mirrorview SRA 5.0.1" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:EMC,EMC Clariion,logs,sra,srm,troubleshooting,blog;button:compact;">Recently I had a customer that could not get a test failover to work. The test would fail during &#8220;Prepare Storage&#8221; after 300 seconds. After increasing the timeout to 15...</a>
</p>