---
title: How does SRM communicate with the array?
author: Jarret Lavallee
layout: post
permalink: /2012/03/how-does-srm-communicate-with-the-array/
dsq_thread_id:
  - 1407439459
categories:
  - SRM
  - VMware
tags:
  - command line
  - command.pl
  - discoverArrays
  - discoverDevices
  - logs
  - sra
  - srm
  - testFailoverStart
  - xml
---
We often get questions on how SRM communicates with the array. I figured that it was time to do a quick write up of the process and some of the basic commands that we will see in the SRM logs. 

The <a href="https://www.vmware.com/support/srm/srm-storage-partners.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/srm/srm-storage-partners.html']);" target="_blank">Storage Replication Adapter</a> (SRA) required for <a href="http://www.vmware.com/products/site-recovery-manager/overview.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/products/site-recovery-manager/overview.html']);" target="_blank">Site Recovery Manager</a> (SRM) with array based replication is responsible for communication between the SRM service and the array. Since SRM supports many vendors, a standard interface was created for communication to the array. VMware published an SRA spec that all certified SRA must adhere to. The version 2, which is required for SRM 5, has many new features that allow for things like <a href="http://blogs.vmware.com/uptime/2011/07/failback-where-is-the-button.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/uptime/2011/07/failback-where-is-the-button.html']);" target="_blank">Reprotect</a>.

When the SRM service starts, it will load the SRA. SRM will call a queryCapabilities command to get a list of the commands that are available to SRM. The way it was implemented was to use XML for data in and out of the SRA. The command.pl is the executable that is responsible for handling communication. (The .pl extension on command.pl may be a bit misleading. Most vendors did not actually write the SRA in perl, but it is part of the SRA v2 specification. So the command.pl is the front end interface for the SRA.)

In order to figure out what the SRA can support, SRM will call queryCapabilities to get the capabilities of the array. An XML document is sent in to every command and an XML document is expected as the return data from every command. Below is the sequence of a full command. All of this information can be found in the <a href="http://kb.vmware.com/kb/1021802" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021802']);" title="SRM Log Locations" target="_blank">SRM Logs</a> after the SRM service is started. 

Call command.pl with a command and send in an XML document.

	 Command line for queryCapabilities: "C:Program Files (x86)VMwareVMware vCenter Site Recovery Managerextern  
	alperl-5.8.8binperl.exe" "C:/Program Files (x86)/VMware/VMware vCenter Site Recovery Manager/storage/sra/EMC Symmetrix/command.pl"  
	2012-03-08T21:40:14.802+02:00 [06052 verbose 'Storage'] Input for queryCapabilities:  
	&#8211;> <?xml version="1.0" encoding="UTF-8"?>  
	&#8211;> <Command xmlns="http://www.vmware.com/srm/sra/v2">  
	&#8211;> <Name>queryCapabilities</Name>  
	&#8211;> <OutputFile>C:UsersVCENTE~1AppDataLocalTempvmware-vcentersrvsra-output-4-0</OutputFile>  
	&#8211;> <StatusFile>C:UsersVCENTE~1AppDataLocalTempvmware-vcentersrvsra-status-5-0</StatusFile>  
	&#8211;> <LogLevel>verbose</LogLevel>  
	&#8211;> <LogDirectory>C:ProgramDataVMwareVMware vCenter Site Recovery ManagerLogsSRAsEMC Symmetrix</LogDirectory>  
	&#8211;> </Command>

After the command is sent in, SRM will wait for a response. It will listen on a file to see when it is updated. The command above came back with the capabilities of this SRA.

	 queryCapabilities exited with exit code 0  
	2012-03-08T21:40:15.161+02:00 [06052 verbose 'Storage'] queryCapabilities responded with:  
	&#8211;> <?xml version="1.0" encoding="UTF-8" ?>  
	&#8211;> <Response xmlns="http://www.vmware.com/srm/sra/v2">  
	&#8211;> <AdapterCapabilities>  
	&#8211;> <ReplicationSoftwares>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5671</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5771</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5773</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5874</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5875</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> </ReplicationSoftwares>  
	&#8211;> <ArrayModels>  
	&#8211;> <ArrayModel>  
	&#8211;> <Name>DMX-1</Name>  
	&#8211;> <Vendor stringId="AdapterVendor">EMC Symmetrix</Vendor>  
	&#8211;> </ArrayModel>  
	&#8211;> <ArrayModel>  
	&#8211;> <Name>DMX-2</Name>  
	&#8211;> <Vendor stringId="AdapterVendor">EMC Symmetrix</Vendor>  
	&#8211;> </ArrayModel>  
	&#8211;> <ArrayModel>  
	&#8211;> <Name>DMX-3</Name>  
	&#8211;> <Vendor stringId="AdapterVendor">EMC Symmetrix</Vendor>  
	&#8211;> </ArrayModel>  
	&#8211;> <ArrayModel>  
	&#8211;> <Name>DMX-4</Name>  
	&#8211;> <Vendor stringId="AdapterVendor">EMC Symmetrix</Vendor>  
	&#8211;> </ArrayModel>  
	&#8211;> <ArrayModel>  
	&#8211;> <Name>VMAX-1</Name>  
	&#8211;> <Vendor stringId="AdapterVendor">EMC Symmetrix</Vendor>  
	&#8211;> </ArrayModel>  
	&#8211;> </ArrayModels>  
	&#8211;> <Features>  
	&#8211;> <MultiArrayDiscovery />  
	&#8211;> <ConsistencyGroups />  
	&#8211;> <DeviceIdentification>wwn</DeviceIdentification>  
	&#8211;> <Protocols>  
	&#8211;> <Protocol>FC</Protocol>  
	&#8211;> </Protocols>  
	&#8211;> </Features>  
	&#8211;> <Commands>  
	&#8211;> <Command name="queryInfo" />  
	&#8211;> <Command name="queryErrorDefinitions" />  
	&#8211;> <Command name="queryCapabilities" />  
	&#8211;> <Command name="queryConnectionParameters" />  
	&#8211;> <Command name="discoverArrays" />  
	&#8211;> <Command name="discoverDevices" />  
	&#8211;> <Command name="syncOnce">  
	&#8211;> <ExecutionLocation>source</ExecutionLocation>  
	&#8211;> </Command>  
	&#8211;> <Command name="querySyncStatus" />  
	&#8211;> <Command name="checkTestFailoverStart" />  
	&#8211;> <Command name="testFailoverStart" />  
	&#8211;> <Command name="testFailoverStop" />  
	&#8211;> <Command name="checkFailover" />  
	&#8211;> <Command name="prepareFailover" />  
	&#8211;> <Command name="failover" />  
	&#8211;> <Command name="reverseReplication">  
	&#8211;> <ExecutionLocation>source</ExecutionLocation>  
	&#8211;> </Command>  
	&#8211;> <Command name="restoreReplication">  
	&#8211;> <ExecutionLocation>source</ExecutionLocation>  
	&#8211;> </Command>  
	&#8211;> </Commands>  
	&#8211;> </AdapterCapabilities>  
	&#8211;> </Response>  
	2012-03-08T21:40:15.177+02:00 [06052 verbose 'Storage'] XML validation succeeded  
	

The SRM to SRA communication will work in the same way for all of the commands that the SRA is capable of. There are many commands that are used for back end communication and service querying. I will go over some of the ones that we see daily.

The queryErrorDefinitions returns a list of error codes to definitions. This list gets printed in the <a href="http://kb.vmware.com/kb/1021802" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021802']);" title="SRM Log Locations">SRM logs</a> for assistance with troubleshooting these response codes. The error codes are sent to SRM through exit codes.  
	
	
	discoverArrays is a command that will list the parameters of an array and its array peers. It is called when adding an array to array managers and it is also called when pairing multiple arrays.  
	

A typical output XML file from discoverArrays is below. We can see that it lists the array ID, vendor, replication software and version. For the purposes of pairing arrays it returns the ID of arrays that it replicate to it or it replicates to. 

	 discoverArrays exited with exit code 0  
	2012-03-08T21:40:30.964+02:00 [02768 verbose 'SraCommand' opID=656d3ec] discoverArrays responded with:  
	&#8211;> <?xml version="1.0" encoding="UTF-8" ?>  
	&#8211;> <Response xmlns="http://www.vmware.com/srm/sra/v2">  
	&#8211;> <Arrays>  
	&#8211;> <Array id="000292601234">  
	&#8211;> <Name>000292601234</Name>  
	&#8211;> <Model>  
	&#8211;> <Name>VMAX-1</Name>  
	&#8211;> <Vendor>EMC Corp</Vendor>  
	&#8211;> </Model>  
	&#8211;> <ReplicationSoftware>  
	&#8211;> <Name>SRDF</Name>  
	&#8211;> <Version>5875</Version>  
	&#8211;> </ReplicationSoftware>  
	&#8211;> <PeerArrays>  
	&#8211;> <PeerArray id="000292602345" />  
	&#8211;> </PeerArrays>  
	&#8211;> </Array>  
	&#8211;> </Arrays>  
	&#8211;> </Response>  
	

discoveryDevices (discoverLuns in SRA v1) returns a list of replicated LUNs. This is called on array pairing and when the &#8220;Recomputing Datastore Groups&#8221; task is showing in vCenter. It is a good place to start if there is missing LUNs/datastores in SRM.  
	
	
	syncOnce is a new feature in SRM 5 that allows for SRM to force a sync (single replication). You can see the check box at the bottom of the Recovery Test and Planned Migration menu.  
	

testFailoverStart is a command that asks the array to present pseudo LUNs to the hosts. The XML input contains LUNs and initiators to present the pseudo LUNs to. The back end technology will be different depending on the vendor.  
	
	
	failover is the actual failover command. This command is sent when a recovery is run. It will break replication and promote the LUNs on the DR site. The LUNs will then be presented to the ESX hosts on the DR site.  
	

reverseReplication is a new command that is built in for reprotect. This command is sent when a reprotect is requested for the GUI. It will reverse the replication of a LUN.  
	
	
	<div class="SPOSTARBUST-Related-Posts">
	  <H3>
	    Related Posts
	  </H3>
	  
	  <ul class="entry-meta">
	    <li class="SPOSTARBUST-Related-Post">
	      <a title="Site Recovery Manager SRDF SRA Fails to Initialize" href="http://virtuallyhyper.com/2013/10/site-recovery-manager-srdf-sra-fails-initialize/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/10/site-recovery-manager-srdf-sra-fails-initialize/']);" rel="bookmark">Site Recovery Manager SRDF SRA Fails to Initialize</a>
	    </li>
	    <li class="SPOSTARBUST-Related-Post">
	      <a title="Migrate from Libvirt KVM to Virtualbox" href="http://virtuallyhyper.com/2013/06/migrate-from-libvirt-kvm-to-virtualbox/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/06/migrate-from-libvirt-kvm-to-virtualbox/']);" rel="bookmark">Migrate from Libvirt KVM to Virtualbox</a>
	    </li>
	    <li class="SPOSTARBUST-Related-Post">
	      <a title="ESXi 4.1 Wait for Local VSA to Start Before Starting Other VMs" href="http://virtuallyhyper.com/2012/09/esxi-4-1-wait-for-local-vsa-to-start-before-starting-other-vms/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/esxi-4-1-wait-for-local-vsa-to-start-before-starting-other-vms/']);" rel="bookmark">ESXi 4.1 Wait for Local VSA to Start Before Starting Other VMs</a>
	    </li>
	    <li class="SPOSTARBUST-Related-Post">
	      <a title="SRM 5.x Custom SSL Certificates with Multiple Subject Alternative Names" href="http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-5-x-custom-ssl-certificates-with-multiple-subject-alternative-names/']);" rel="bookmark">SRM 5.x Custom SSL Certificates with Multiple Subject Alternative Names</a>
	    </li>
	    <li class="SPOSTARBUST-Related-Post">
	      <a title="Changing the User and Password that VRMS Uses to Connect to vCenter" href="http://virtuallyhyper.com/2012/08/srm-5-vrms-change-username-to-connect-to-vc/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/srm-5-vrms-change-username-to-connect-to-vc/']);" rel="bookmark">Changing the User and Password that VRMS Uses to Connect to vCenter</a>
	    </li>
	  </ul>
	</div>
	
