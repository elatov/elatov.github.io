---
title: Automating the 3PAR ESXi SATP Rule Creation with PowerCli
author: Jarret Lavallee
layout: post
permalink: /2013/10/automating-3par-satp-rule-creation-powercli/
dsq_thread_id:
  - 1893402537
sharing_disabled:
  - 1
categories:
  - Storage
  - VMware
tags:
  - 3PAR
  - esxcli
  - powercli
---
Recently I was working with a customer to install a new 3PAR array and migrate VMs to it. The 3PAR array will work with the default settings, but it has multiple best practices that should be followed to ensure the best performance and reliability. The best practices can be found in the <a href="http://bizsupport1.austin.hp.com/bc/docs/support/SupportManual/c03290624/c03290624.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://bizsupport1.austin.hp.com/bc/docs/support/SupportManual/c03290624/c03290624.pdf']);">HP 3PAR VMware ESX Implementation Guide</a>. The main points are as follows.

*   Use Persona 11 for VMware LUNs on HP 3PAR OS 3.1.2 and above
*   Add a SATP rule to the ESX host to allow the following 
    *   Setting the default Path Selection Policy (PSP) to Round Robin (VMW\_PSP\_RR)
    *   Setting the default Round Robin IOPS option to 100 instead of 1000
    *   Setting the default SATP for 3PAR as ALUA (VMW\_SATP\_ALUA)

The best practice for the array is to add a new SATP rule on each host to allocate the correct SATP for the 3PAR LUNs. The other way would be to change the default PSP for the SATP which we covered in <a href="http://virtuallyhyper.com/2012/03/changing-the-path-selection-policy-to-round-robin/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/changing-the-path-selection-policy-to-round-robin/']);">this post</a>. Since we want to change the IOPS property and ensure that the new LUNs are claimed properly we will create the new SATP rule. The command for creating this SATP rule for host persona 11 is as follow.

    # esxcli storage nmp satp rule add -s "VMW_SATP_ALUA" -P "VMW_PSP_RR" -O iops=100 -c "tpgs_on" -V "3PARdata" -M "VV" -e "HP 3PAR Custom iSCSI/FC/FCoE ALUA Rule"
    

For host persona 6 the following command would be run.

    # esxcli storage nmp satp rule add -s "VMW_SATP_DEFAULT_AA" -P "VMW_PSP_RR" -O iops=100 -c "tpgs_off" -V "3PARdata" -M "VV" -e "HP 3PAR Custom iSCSI/FC/FCoE ALUA Rule"
    

The difference between the rules is that host persona 11 is ALUA, where as host persona 6 is Active/Active. <a href="http://virtuallyhyper.com/2012/04/seeing-a-high-number-of-trespasses-from-a-clariion-array-with-esx-hosts/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/seeing-a-high-number-of-trespasses-from-a-clariion-array-with-esx-hosts/']);">This post</a> explains ALUA in further detail.

Logging into each ESXi host to create the rule does not seem like a good use of time, so I went looking for some better ways of creating these rules with out having to do it manually. There are multiple ways of adding these rules including <a href="http://www.vmware.com/resources/techresources/10137" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/techresources/10137']);">Host Profiles</a>, <a href="http://www.van-lieshout.com/2011/01/esxcli-powercli/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.van-lieshout.com/2011/01/esxcli-powercli/']);">PowerCli</a>, <a href="http://blogs.vmware.com/vsphere/2012/05/vcli-authentication-options.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2012/05/vcli-authentication-options.html']);">vCLI</a>

I went searching around for a solution for PowerCli and found <a href="http://tech.philipsellers.com/2013/04/22/3par-storserv-7000-series-best-practices-for-vsphere-5-1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://tech.philipsellers.com/2013/04/22/3par-storserv-7000-series-best-practices-for-vsphere-5-1/']);">this article</a>, it talks about the best practices on the 3PAR and adds some PowerCli scripts to configure these for the 3PAR. Unfortunately the article gives a PowerCli Script that changes the properties on each LUN instead of adding the SATP rule to the ESXi host. While this will work for the existing LUNs, we want it to be the default on all new LUNs as well, so we want a global change rather than a LUN specific change. So I did a little digging into the PowerCli **Get-Esxcli** command and found the <a href="http://pubs.vmware.com/vsphere-55/index.jsp#com.vmware.powercli.cmdletref.doc/Get-EsxCli.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pubs.vmware.com/vsphere-55/index.jsp#com.vmware.powercli.cmdletref.doc/Get-EsxCli.html']);">syntax for the command</a>. <a href="http://yuridejager.wordpress.com/2013/02/07/set-the-path-selection-policy-for-every-device-path-of-every-host-in-your-vsphere-5-05-1-cluster-using-powercli/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://yuridejager.wordpress.com/2013/02/07/set-the-path-selection-policy-for-every-device-path-of-every-host-in-your-vsphere-5-05-1-cluster-using-powercli/']);">This article</a> gives some example PowerCli scripts using **Get-Esxcli**. Unfortunately I did not find an example with the syntax for the command that I wanted, so I went to the command line and queried the **Get-Esxcli** command for the **esxcli storage nmp satp rule add** command. We can see the options below.

    boolean add(boolean boot, string claimoption, string description, string device, string driver, boolean force, string model, string option, string psp, string pspoption, string satp, string transport, string type, string vendor)
    

So we need to fill in the appropriate values for our SATP rule and send in *$null* for the options we want to omit. I came up with the following command to add the rule as per the best practices.

    PowerCLI C:\> $esxcli.storage.nmp.satp.rule.add($null,"tpgs_on","HP 3PAR Custom iSCSI/FC/FCoE ALUA Rule",$null,$null,$null,"VV",$null,"VMW_PSP_RR","iops=100","VMW_SATP_ALUA",$null,$null,"3PARdata")
    true
    

As you can see in the example above, it returned *true* when I ran the command. I do not really trust this, so I need to confirm that the rule actually exists. Let&#8217;s verify that the rule was put in place. The command below will look for any SATP rules that have *3PAR* in the description.

    PowerCLI C:\> $esxcli.storage.nmp.satp.rule.list() | where {$_.description -like "*3par*"}
    
    
    ClaimOptions : tpgs_on
    DefaultPSP   : VMW_PSP_RR
    Description  : HP 3PAR Custom iSCSI/FC/FCoE ALUA Rule
    Device       :
    Driver       :
    Model        : VV
    Name         : VMW_SATP_ALUA
    Options      :
    PSPOptions   : iops=100
    RuleGroup    : user
    Transport    :
    Vendor       : 3PARdata
    

Great that worked, but I have no interest in running this manually on each host, so I wrote up a small script to add it to every host. Please note that I am not an expert in PowerCLi, so there may be some much better ways to implement this script. Let me know if you have a better script and I will post it up here. Note that this script does not do any error checking. If the rule exists, it will try to add it and will fail because the rule already exists.

    #Variables
    $cluster = "NYC Production"
    
    foreach($esx in Get-Cluster $cluster | Get-VMHost){
        $esxcli = Get-EsxCli -VMHost $esx
        # List HP SATP rules
        # $esxcli.storage.nmp.satp.rule.list() | where {$_.description -like "*HP*"}
        # Create A new satp rule for 3PAR
        $result = $esxcli.storage.nmp.satp.rule.add($null,"tpgs_on","HP 3PAR Custom iSCSI/FC/FCoE ALUA Rule",$null,$null,$null,"VV",$null,"VMW_PSP_RR","iops=100","VMW_SATP_ALUA",$null,$null,"3PARdata")
        # List 3PAR Rules
        # $esxcli.storage.nmp.satp.rule.list() | where {$_.description -like "*3par*"}
         Write-Host "Host:", $esx.Name, "Result", $result
    }
    

Running this basic script worked for this environment. All LUNs were claimed properly and with the correct SATP, PSP, and PSP properties.

