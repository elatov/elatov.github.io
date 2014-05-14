---
title: Site Recovery Manager SRDF SRA Fails to Initialize
author: Jarret Lavallee
layout: post
permalink: /2013/10/site-recovery-manager-srdf-sra-fails-initialize/
dsq_thread_id:
  - 1796264186
sharing_disabled:
  - 1
categories:
  - SRM
  - VMware
tags:
  - sra
  - srdf
  - srm
---
While configuring a Site Recovery Manager (SRM) instance for a customer, I ran into an issue with the EMC SRDF 5.1.0.0 SRA. After installing Solutions Enabler and then installing the SRA, everything went smooth until I did a *rescan for SRAs* in the SRM user interface. After the rescan, the SRDF adapter did not show up, but had the following error instead.

> Failed to load SRA from &#8216;D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix&#8217;. SRA command &#8216;queryInfo&#8217; failed. Internal error: &#8216;C:/Program&#8217; is not recognized as an internal or external command, operable program or batch file.

Right away we know that it has to do with the installation path. From the output of the error, we can see that I installed SRM to the &#42;D:&#42; drive instead of the &#42;C:&#42; drive. This has been known to cause problems, but it is a standard practice for this customer and we wanted to follow it. The Mirrorview SRA works fine with this configuration.

So I jumped into the logs at *C:\ProgramData\VMware\VMware Site Recovery Manager\logs* and opened the most recent log. After scanning through the log, I saw the following.

    2013-09-19T16:11:57.583-04:00 [04792 info 'Storage' opID=E910786E-00000014] Command line for queryInfo: "D:\Program Files\VMware\VMware vCenter Site Recovery Manager\external\perl-5.14.2\bin\perl.exe" "D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"
    2013-09-19T16:11:57.583-04:00 [04792 verbose 'Storage' opID=E910786E-00000014] Input for queryInfo:
    --> <?xml version="1.0" encoding="UTF-8"?>
    --> <Command xmlns="http://www.vmware.com/srm/sra/v2">
    -->   <Name>queryInfo</Name>
    -->   <OutputFile>C:\Windows\TEMP\vmware-SYSTEM\sra-output-0-145</OutputFile>
    -->   <StatusFile>C:\Windows\TEMP\vmware-SYSTEM\sra-status-1-191</StatusFile>
    -->   <LogLevel>verbose</LogLevel>
    -->   <LogDirectory>C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\SRAs\EMC Symmetrix</LogDirectory>
    --> </Command>
    2013-09-19T16:11:57.662-04:00 [04792 verbose 'SysCommandWin32' opID=E910786E-00000014] Starting process: "D:\Program Files\VMware\VMware vCenter Site Recovery Manager\external\perl-5.14.2\bin\perl.exe" "D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"
    2013-09-19T16:11:57.708-04:00 [04792 verbose 'Storage' opID=E910786E-00000014] Resetting SRA command timeout to '300' seconds in the future
    2013-09-19T16:11:57.708-04:00 [01728 info 'Default'] Thread attached
    2013-09-19T16:11:57.708-04:00 [01728 info 'ThreadPool'] Thread enlisted
    2013-09-19T16:11:57.740-04:00 [04792 verbose 'Storage' opID=E910786E-00000014] Listening for updates to file 'C:\Windows\TEMP\vmware-SYSTEM\sra-status-1-191'
    2013-09-19T16:11:57.927-04:00 [02996 verbose 'DrTask' opID=E910786E-00000014] Created VC task 'com.vmware.vcDr.dr.storage.StorageManager.reloadAdapters:task-17'
    2013-09-19T16:11:59.271-04:00 [02148 error 'Storage' opID=E910786E-00000014] queryInfo's stderr:
    --> 'C:/Program' is not recognized as an internal or external command,
    --> operable program or batch file.
    --> 
    

This matches up with what displayed in the vSphere Client, but it does give us a more information. SRM is calling `"D:\Program Files\VMware\VMware vCenter Site Recovery Manager\external\perl-5.14.2\bin\perl.exe" "D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"` with the input XML file that is listed below. So we know that the *C:\Program* error is coming from something downstream. That would mean that the SRA it&#8217;s self has some static paths built into it. I ran the command in a new **cmd prompt** to verify the same issue.

    > "D:\Program Files\VMware\VMware vCenter Site Recovery Manager\external\perl-5.14.2\bin\perl.exe" "D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"
    'C:/Program' is not recognized as an internal or external command, operable program or batch file.
    

So we received the error message as SRM did when it called the SRA. So the next thing to try is to open up the *command.pl* perl script to see what is going on. The *command.pl* is the interface to which SRM makes calls. More about the SRA process is described in <a href="http://virtuallyhyper.com/2012/03/how-does-srm-communicate-with-the-array/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/how-does-srm-communicate-with-the-array/']);">this article</a>.

I opened up the *command.pl* and found that there is a static path to `C:\Program Files (x86)\VMware\VMware vCenter Site Recovery<br />
Manager\storage\sra\EMC Symmetrix\`. I updated this to point to the correct path `D:\Program Files (x86)\VMware\VMware vCenter Site Recovery<br />
Manager\storage\sra\EMC Symmetrix\`, but found the same error when running the command manually, except it was *D:\Program* this time.

    > "D:\Program Files\VMware\VMware vCenter Site Recovery Manager\external\perl-5.14.2\bin\perl.exe" "D:/Program Files/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"
    'D:/Program' is not recognized as an internal or external command, operable program or batch file.
    

After a little more research I found <a href="http://blog.stfu.se/?p=308" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.stfu.se/?p=308']);">this blog article</a> describing a similar issue. They seemed to find a workaround by putting the binaries in the correct *C:* location and then installing it back to the &#42;D:&#42; drive. Unfortunately I doubt that EMC would support this in production, so I did not implement it in the customers environment. I went back and reinstalled SRM, Soultions Enabler, and the SRDF SRA on the &#42;C:&#42; drive. After installing everything back on the *C:* drive, everything worked alright for SRDF.

