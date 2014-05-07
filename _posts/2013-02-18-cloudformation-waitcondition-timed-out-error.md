---
title: CloudFormation WaitCondition Timed Out Error
author: Joe Chan
layout: post
permalink: /2013/02/cloudformation-waitcondition-timed-out-error/
dsq_thread_id:
  - 1410349394
categories:
  - AWS
tags:
  - Amazon Machine Images
  - AWS CloudFormation
---
*Update (05/14/13)*: Amazon no longer supports the AMI I had linked previously. They now bake the helper scripts into the <a href="https://aws.amazon.com/amis/microsoft-windows-server-2008-r2-base" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://aws.amazon.com/amis/microsoft-windows-server-2008-r2-base']);">base Windows AMIs</a>. If you are running an older AMI and don&#8217;t have the helper scripts installed, you can install <a href="http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html']);">them</a> manually or just deploy a new Windows AMI from the AWS Management Console.

## CloudFormation WaitCondition Timed Out Error

I recently ran into an issue with a CloudFormation WaitCondition timed out message. The stack was failing to create with this error:

    #!
    WaitCondition timed out.
    Received 0 conditions when expecting 1
    

## How I got here

I had taken the <a href="https://s3.amazonaws.com/cloudformation-templates-us-east-1/Windows_Single_Server_SharePoint_Foundation.template" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://s3.amazonaws.com/cloudformation-templates-us-east-1/Windows_Single_Server_SharePoint_Foundation.template']);">sample template</a> taken from <a href="http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-windows-stacks-bootstrapping.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-windows-stacks-bootstrapping.html']);">Bootstrapping AWS CloudFormation Windows Stacks</a> and modified it to use one of my custom AMIs.

## Why this happened

Looking at <a href="http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-waitcondition.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-waitcondition.html']);">Creating Wait Conditions in a Template</a>:

    "SharePointFoundationWaitCondition" : {
       "Type" : "AWS::CloudFormation::WaitCondition",
       "DependsOn" : "SharePointFoundation",
       "Properties" : {
         "Handle" : {"Ref" : "SharePointFoundationWaitHandle"},
         "Timeout" : "3600"
       }
    }
    

This means that the `WaitCondition` that is currently awaiting a signal from **cfn-signal.exe**, which comes from this line in <a href="https://s3.amazonaws.com/cloudformation-templates-us-east-1/Windows_Single_Server_SharePoint_Foundation.template" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://s3.amazonaws.com/cloudformation-templates-us-east-1/Windows_Single_Server_SharePoint_Foundation.template']);">my template</a>:

    "cfn-signal.exe -e %ERRORLEVEL% ", { "Fn::Base64" : {
    "Ref" : "SharePointFoundationWaitHandle" }}, "\n"
    

Per the configuration here, the `WaitCondition` timed out after 3600 seconds without getting a signal.

It turns out **cfn-signal.exe** doesn&#8217;t exist in my AMI because per <a href="http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-windows-stacks-bootstrapping.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-windows-stacks-bootstrapping.html']);">Bootstrapping AWS CloudFormation Windows Stacks</a>:

> The Amazon EBS-Backed Windows Server 2008 R2 English 64-bit &#8211; Base for CloudFormation AMI comes supplied with the AWS CloudFormation helper scripts pre-installed in the C:\Program Files (x86)\Amazon\cfn-bootstrap directory.

This template expects the helper scripts to be pre-installed on your AMI, but the AMI I launched with (from the AWS management console quick launch wizard) to create my custom AMI from did not come with the helper scripts pre-installed.

# Solution

I created my own AMI from the Amazon EBS-Backed Windows Server 2008 R2 English 64-bit &#8211; Base for CloudFormation AMI, installed my application, then installed the <a href="http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html']);">helper scripts</a>. Afterwards, I created an AMI from that instance and used that as a base for my CloudFormation template (which expects the helper scripts and existence of **cfn-signal.exe** which now exist!).

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/02/cloudformation-waitcondition-timed-out-error/" title=" CloudFormation WaitCondition Timed Out Error" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Amazon Machine Images,AWS CloudFormation,blog;button:compact;">Update (05/14/13): Amazon no longer supports the AMI I had linked previously. They now bake the helper scripts into the base Windows AMIs. If you are running an older AMI...</a>
</p>