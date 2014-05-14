---
title: vCenter 5.1 Service Fails to Start
author: Jarret Lavallee
layout: post
permalink: /2013/02/vcenter-5-1-service-fails-to-start/
dsq_thread_id:
  - 1406799321
categories:
  - VMware
tags:
  - SSO
  - vcenter
---
The other day I tried starting up *vCenter* and it failed to start. I confirmed that the SQL and <a href="http://kb.vmware.com/kb/2034918" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2034918']);">Single Sign On (SSO)</a> Servers were online and the services were started, but *vCenter* would still fail to start. I opened up the **vpxd.log** to see why it was not starting. The *vCenter* log location can be found in this <a href="http://kb.vmware.com/kb/1021804" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021804']);" title="vCenter Log Location" target="_blank">KB article</a>.

In the **vpxd.log** we can see that *vCenter* was backtracing after trying to access the &#8216;SSO&#8217; server.

    2013-02-16T22:20:24.389-05:00 [05884 info 'authvpxdMoSessionManager'\] \[SSO\]\[SessionManagerMo::Init] Admin URI set to: https://PR-SSO:7444/sso-adminserver/sdk 
    2013-02-16T22:20:24.389-05:00 [05884 info 'authvpxdMoSessionManager'\] \[SSO\]\[SessionManagerMo::Init] Downloading STS Root certificates ... 
    2013-02-16T22:20:24.405-05:00 [03520 info 'Default'] Thread attached 
    2013-02-16T22:20:25.528-05:00 [05884 warning 'VpxProfiler'] Vpxd::ServerApp::Init [SessionManagerMo::Init()] took 1139 ms 
    2013-02-16T22:20:25.528-05:00 [05884 error 'vpxdvpxdMain'\] \[Vpxd::ServerApp::Init\] Init failed: Unexpected exception --> Backtrace: 
    --> backtrace[00] rip 000000018018a8ca 
    --> backtrace[01] rip 0000000180102f28 
    --> backtrace[02] rip 000000018010423e 
    --> backtrace[03] rip 000000018008e00b 
    --> backtrace[04] rip 0000000000524971 
    --> backtrace[05] rip 00000000004c1298 
    --> backtrace[06] rip 00000000004c16c9 
    --> backtrace[07] rip 0000000000430fae 
    --> backtrace[08] rip 000000014110e248 
    --> backtrace[09] rip 000000013ffffd68 
    --> backtrace[10] rip 000000013ffffe5a 
    --> backtrace[11] rip 000000013fffff69 
    --> backtrace[12] rip 00000001400002f9 
    --> backtrace[13] rip 0000000140344b43 
    --> backtrace[14] rip 0000000140aee6f9 
    --> backtrace[15] rip 0000000140ae859c 
    --> backtrace[16] rip 0000000140d0a78b 
    --> backtrace[17] rip 000007feff47a82d 
    --> backtrace[18] rip 000000007737652d 
    --> backtrace[19] rip 0000000077a6c521 
    --> 2013-02-16T22:20:25.528-05:00 [05884 warning 'VpxProfiler'] ServerApp::Init [TotalTime] took 4664 ms 
    2013-02-16T22:20:25.528-05:00 [05884 error 'Default'] Failed to intialize VMware VirtualCenter. Shutting down... 
    

At first it looked like the issue described in <a href="http://kb.vmware.com/kb/2036170" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2036170']);">this KB article</a>. After following the process ID in the logs, the events did not correlate to the KB article.

I brought up a web browser and tried to access the same URL that *vCenter* was using. **https://PR-SSO:7444/sso-adminserver/sdk**. The webserver in SSO is working and serving up the right certificate. When the page loaded it showed the following text.

    ServerFaultCodeUnexpected EOF in prolog at [row,col {unknown-source}]: [1,0\]
    

So the SSO service is online and listening on **7443**, which is good. Since we were able to get a response, we also know that there is nothing blocking communication on **7443** between the *vCenter* and SSO servers.

I logged onto the SSO server to check that everything is working correctly. I found <a href="http://kb.vmware.com/kb/2036170" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2036170']);">this KB</a> which provides a command to discover the identity sources for SSO. I ran the command to test that the service is providing services.

    C:\Program Files\VMware\Infrastructure\SSOServer\utils>ssocli.cmd configure-riat -a discover-is -u admin -p [password] Executing action: 'discover-is'
    
    Discovering identity sources
    
    Error: Could not access HTTP invoker remote service at \[https://pr-sso:7444/ims/CommandServer]; nested exception is org.apache.commons.httpclient.HttpException: Did not receive successful HTTP response: status code = 404, status message = [Not Found\] 
    

The output from this command indicates that the *IMS* service is not running correctly. After running the command I went to take a look at the SSO logs. The SSO log location can be found in this <a href="http://kb.vmware.com/kb/2033430" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2033430']);">KB article</a>. In the **localhost** log I saw the real error: The SSO service was timing out trying to connect to the SQL server.

    16-Feb-2013 23:03:57.176 SEVERE [pool-3-thread-1] org.apache.catalina.core.StandardContext.listenerStart Exception sending context initialized event to listener instance of class com.rsa.ims.components.servlets.ContextLoaderListener 
    org.springframework.beans.factory.access.BootstrapException: Unable to return specified BeanFactory instance: factory key [ims], from group with resource name [classpath:beanRefContext.xml]; nested exception is 
    org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'ims' defined in class path resource [beanRefContext.xml]: Instantiation of bean failed; nested exception is
    org.springframework.beans.BeanInstantiationException: Could not instantiate bean class [com.rsa.ims.components.spring.SecurityAwareClassPathXmlApplicationContext]: Constructor threw exception; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'DatabaseMetadataBean' defined in class path resource [ims-components-common.xml]: Instantiation of bean failed; nested exception is 
    org.springframework.beans.BeanInstantiationException: Could not instantiate bean class [com.rsa.ims.common.DatabaseMetadataBean]: Constructor threw exception; nested exception is 
    org.apache.commons.dbcp.SQLNestedException: Cannot create PoolableConnectionFactory (Network error IOException: Connection timed out: connect) at org.springframework.beans.factory.access.SingletonBeanFactoryLocator.useBeanFactory(SingletonBeanFactoryLocator.java:409) 
    

I double checked that the service was running on the SQL server and verified that I could ping between servers. I verified the DNS resolution as well. I ran across <a href="http://communities.vmware.com/thread/426536" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/thread/426536']);">a communities thread</a> where they were using dynamic ports on the SQL server. They had the same symptoms as I did, so I went to go check the port configuration on the SQL server. I discovered that the SQL server was statically assigned to **1433**.

<img src="http://virtuallyhyper.com/wp-content/uploads/2013/02/SQL-TCP-ports.jpg" alt="SQL TCP ports vCenter 5.1 Service Fails to Start" width="395" height="435" class="aligncenter size-full wp-image-6310" title="vCenter 5.1 Service Fails to Start" />

So I went back to the SSO server to confirm that it was configured on the correct port and that it has the correct address. <a href="http://kb.vmware.com/kb/2033516" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2033516']);">This KB article</a> gave me the command to change the database configuration. I ran it with the correct information.

    C:\Program Files\VMware\Infrastructure\SSOServer\utils>ssocli.cmd configure-riat -a configure-db --database-host PR-SSO.domain.com --database-port 1433 -m [password]
    
    ERROR: org.springframework.jbdc.CannotGetJbdcConnectionException: Could not get JDBC Connection; nested exception is java.sql.SQLException: Network error IOException: Connection timed out: connect
    

So the SSO service could not connect to the SQL service. I fired up a command prompt and tried to telnet to the SQL server on port **1433** and the connection timed out. I found that the windows firewall was blocking **1433** on the SQL server. After opening that port and restarting the SSO, I was able to start the *vCenter* service. As it turns out, the SSO service will start without a connection to it&#8217;s database.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Set up simpleSAMLphp as an IdP to be Used in an SP-Initiated SSO with Google Apps" href="http://virtuallyhyper.com/2013/05/set-up-simplesamlphp-as-an-idp-to-be-used-in-an-sp-initiated-sso-with-google-apps/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/05/set-up-simplesamlphp-as-an-idp-to-be-used-in-an-sp-initiated-sso-with-google-apps/']);" rel="bookmark">Set up simpleSAMLphp as an IdP to be Used in an SP-Initiated SSO with Google Apps</a>
    </li>
  </ul>
</div>

