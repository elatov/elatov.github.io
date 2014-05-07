---
title: How to Update the AWS CLI Tools (Linux)
author: Joe Chan
layout: post
permalink: /2013/04/how-to-update-the-aws-cli-tools-linux/
dsq_thread_id:
  - 1450259439
categories:
  - AWS
tags:
  - aws
  - cli
  - ec2
  - linux
  - vtip
---
## How to Update the AWS CLI Tools (Linux)

This is a reference on how to to Update the AWS CLI tools running on Linux. This is specifically for the <a href="http://aws.amazon.com/cli/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://aws.amazon.com/cli/']);">AWS CLI</a>.

### Check Existing Version

    $ aws --version
    aws-cli/0.5.0 Python/2.6.8 Linux/3.2.37-2.47.amzn1.x86_64
    

### Download Latest Version of the AWS CLI tools from the Git Repository

    $ git clone https://github.com/aws/aws-cli.git
    Cloning into aws-cli...
    remote: Counting objects: 2984, done.
    remote: Compressing objects: 100% (1487/1487), done.
    remote: Total 2984 (delta 1900), reused 2551 (delta 1473)
    Receiving objects: 100% (2984/2984), 1.09 MiB | 624 KiB/s, done.
    Resolving deltas: 100% (1900/1900), done.
    

### Install

    $ cd ~/aws-cli
    $ sudo python setup.py install
    

### Verify Version has been Upgraded

    $ aws --version
    aws-cli/0.8.1 Python/2.6.8 Linux/3.2.37-2.47.amzn1.x86_64
    

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/04/how-to-update-the-aws-cli-tools-linux/" title=" How to Update the AWS CLI Tools (Linux)" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:aws,cli,ec2,linux,vtip,blog;button:compact;">How to Update the AWS CLI Tools (Linux) This is a reference on how to to Update the AWS CLI tools running on Linux. This is specifically for the AWS...</a>
</p>