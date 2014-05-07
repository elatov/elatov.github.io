---
title: How to Make an Anonymous Amazon S3 REST Request
author: Joe Chan
layout: post
permalink: /2013/09/make-anonymous-amazon-s3-rest-request/
dsq_thread_id:
  - 1741297715
categories:
  - AWS
tags:
  - Amazon_S3
  - aws
  - REST
---
## How to make an anonymous S3 REST request

I recently had a problem where the bucket owner could not access or modify an object. It turns out that the object was created with an anonymous (unauthenticated) user and had the following ACL and properties:

**ExampleObject.txt**

*   Bucket owner: Joe
*   Object owner: Anonymous
*   Creator: Anonymous

<table>
  <tr>
    <td>
      <strong>Grantee</strong>
    </td>
    
    <td>
      <strong>Permission</strong>
    </td>
  </tr>
  
  <tr>
    <td>
      Anonymous
    </td>
    
    <td>
      Write
    </td>
  </tr>
</table>

### Solution

To make it so that the bucket owner could access the file again, we need to add ACL rules to the object that look like this:

<table>
  <tr>
    <td>
      <strong>Grantee</strong>
    </td>
    
    <td>
      <strong>Permission</strong>
    </td>
  </tr>
  
  <tr>
    <td>
      Joe
    </td>
    
    <td>
      Read
    </td>
  </tr>
</table>

**Joe**, however, currently can&#8217;t modify the ACL because of the current ACL rules.

To make an anonymous request, we can use the `curl` tool.

From the <a href="http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUTacl.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUTacl.html']);">API docs for Put Acl</a>, an example request looks like this:

**Example request**

>     PUT ExampleObject.txt?acl HTTP/1.1
>     Host: examplebucket.s3.amazonaws.com
>     x-amz-acl: public-read
>     Accept: */*
>     Authorization: AWS AKIAIOSFODNN7EXAMPLE:xQE0diMbLRepdf3YB+FIEXAMPLE=
>     Host: s3.amazonaws.com
>     Connection: Keep-Alive
>     

**Example curl command to grant Joe read access to the ExampleObject.txt**

>     curl -X PUT \
>     -H 'x-amz-grant-read: emailAddress="joe@amazon.com"' \
>     
>     http://examplebucket.s3.amazonaws.com/ExampleObject.txt?acl
>     
>     

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/09/make-anonymous-amazon-s3-rest-request/" title=" How to Make an Anonymous Amazon S3 REST Request" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Amazon_S3,aws,REST,blog;button:compact;">How to make an anonymous S3 REST request I recently had a problem where the bucket owner could not access or modify an object. It turns out that the object...</a>
</p>