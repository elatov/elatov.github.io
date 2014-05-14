---
title: Installing vCenter 5.5 fails with Invalid Credentials
author: Jarret Lavallee
layout: post
permalink: /2013/10/installing-vcenter-fails-invalid-credentials/
dsq_thread_id:
  - 1893390984
sharing_disabled:
  - 1
categories:
  - VMware
tags:
  - SSO
  - vcenter
---
Recently I was doing a deployment in my lab with vCenter 5.5 and ran into a small issue. After installing vCenter Single Sign On (SSO), I went to install the vSphere Web Client which failed with the `Error 29103. The provided credentials are not valid. Please check VM_ssoreg.log in the system temporary folder for details.` This could happen with the vCenter Inventory service as well.

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/2013-10-07-16_49_49-vDesktop-for-Consultants.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/2013-10-07-16_49_49-vDesktop-for-Consultants.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/2013-10-07-16_49_49-vDesktop-for-Consultants.png" alt="2013 10 07 16 49 49 vDesktop for Consultants Installing vCenter 5.5 fails with Invalid Credentials" width="368" height="170" class="aligncenter size-full wp-image-9653" title="Installing vCenter 5.5 fails with Invalid Credentials" /></a>

The message indicates that I gave it the wrong password for the *Administrator@vsphere.local*. Naturally I could have mistyped i,t so I tried it again only to find the same error. As the error says, we should check the *VM_ssoreg.log* to see more details on the error. *VM_ssoreg.log* can be found in the local data on the server. In my case this is *C:\Users\jarret\AppData\Local\Temp*. The bottom of the log shows the issue.

    [2013-10-07 16:40:01,203 main  DEBUG com.vmware.vim.install.impl.AdminServiceAccess] Creating client for SSO Admin on address: https://VC.moopless.com:7444/sso-adminserver/sdk/vsphere.local
    [2013-10-07 16:40:03,115 main  ERROR com.vmware.vim.sso.client.impl.SoapBindingImpl] SOAP fault
    javax.xml.ws.soap.SOAPFaultException: Invalid credentials
        at com.sun.xml.internal.ws.fault.SOAP11Fault.getProtocolException(Unknown Source)
        at com.sun.xml.internal.ws.fault.SOAPFaultBuilder.createException(Unknown Source)
        at com.sun.xml.internal.ws.client.dispatch.DispatchImpl.doInvoke(Unknown Source)
        at com.sun.xml.internal.ws.client.dispatch.DispatchImpl.invoke(Unknown Source)
        at com.vmware.vim.sso.client.impl.SoapBindingImpl.sendMessage(SoapBindingImpl.java:130)
        at com.vmware.vim.sso.client.impl.SoapBindingImpl.sendMessage(SoapBindingImpl.java:81)
        at com.vmware.vim.sso.client.impl.SecurityTokenServiceImpl$RequestResponseProcessor.sendRequest(SecurityTokenServiceImpl.java:767)
        at com.vmware.vim.sso.client.impl.SecurityTokenServiceImpl$RequestResponseProcessor.executeRoundtrip(SecurityTokenServiceImpl.java:697)
        at com.vmware.vim.sso.client.impl.SecurityTokenServiceImpl.acquireToken(SecurityTokenServiceImpl.java:123)
        at com.vmware.vim.install.impl.AdminServiceAccess.acquireSamlToken(AdminServiceAccess.java:297)
        at com.vmware.vim.install.impl.AdminServiceAccess.<init>(AdminServiceAccess.java:187)
        at com.vmware.vim.install.impl.AdminServiceAccess.createDiscover(AdminServiceAccess.java:238)
        at com.vmware.vim.install.impl.RegistrationProviderImpl.<init>(RegistrationProviderImpl.java:57)
        at com.vmware.vim.install.RegistrationProviderFactory.getRegistrationProvider(RegistrationProviderFactory.java:143)
        at com.vmware.vim.install.RegistrationProviderFactory.getRegistrationProvider(RegistrationProviderFactory.java:60)
        at com.vmware.vim.install.cli.commands.CommandArgumentsParser.createServiceProvider(CommandArgumentsParser.java:241)
        at com.vmware.vim.install.cli.commands.CommandArgumentsParser.parseCommand(CommandArgumentsParser.java:101)
        at com.vmware.vim.install.cli.commands.CommandFactory.createRegisterSolutionCommand(CommandFactory.java:114)
        at com.vmware.vim.install.cli.RegTool.process(RegTool.java:107)
        at com.vmware.vim.install.cli.RegTool.main(RegTool.java:38)
    [2013-10-07 16:40:03,118 main  DEBUG com.vmware.vim.install.impl.AdminServiceAccess] Provided credentials are not valid.
    [2013-10-07 16:40:03,118 main  ERROR com.vmware.vim.install.cli.commands.CommandArgumentsParser] Cannot authenticate user
    [2013-10-07 16:40:03,120 main  INFO  com.vmware.vim.install.cli.RegTool] Return code is: InvalidCredentials
    

Unfortunately the issue is as the other error claimed, the credentials are invalid. Luckily I remembered that there was a similar issue with the SSO installation in vSphere 5.5, where if you had special characters in the password the installation would fail with the generic `Error 29133. Administrator login error.`, `Error 29102: An invalid argument was provided`, or `Error 29158.Node package creation error` errors. The KB for that issue <a href="http://kb.vmware.com/kb/2035820" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2035820']);">is here</a>.In this case I had a special character in the password that was interfering with the SSO registration. Likely it does not sanitize the input and just fails the registration.

I went back and reinstalled SSO with a password as recommended and everything worked out alright. Just remember to use a special character, as is required, but not to use any of the following.

*   ^
*   *
*   $
*   ;
*   &#8220;
*   &#8216;
*   )
*   <
*   >
*   &
*   |
*   \
*   _
*   A trailing &#8221; &#8221; space
*   Non-ASCII characters

