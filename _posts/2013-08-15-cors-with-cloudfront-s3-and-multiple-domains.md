---
title: CORS with CloudFront, S3, and Multiple Domains
author: Joe Chan
layout: post
permalink: /2013/08/cors-with-cloudfront-s3-and-multiple-domains/
dsq_thread_id:
  - 1590044900
categories:
  - AWS
tags:
  - aws
  - cloudfront
  - cors
  - s3
---
Here is a tutorial on how to set up CORS with AWS S3, CloudFront and multiple domains.

## What is CORS?

CORS stands for Cross Origin Resource Sharing and it&#8217;s a W3C specification for allowing cross-site HTTP requests. Here is a description of cross-site HTTP requests from <a href="https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS']);">Mozilla</a>:

> Cross-site HTTP requests are HTTP requests for resources from a different domain than the domain of the resource making the request. For instance, a resource loaded from Domain A (http://domaina.example) such as an HTML web page, makes a request for a resource on Domain B (http://domainb.foo), such as an image, using the img element (http://domainb.foo/image.jpg).

You often will deal with CORS in JavaScript if you ever try load content from any domain other than the one you are visiting (for example in an Ajax request).

## How to set up S3 to support CORS

You can enable CORS on an S3 bucket by following the <a href="http://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html']);">AWS documentation here</a>.

Here is the CORS policy that I used for testing:

    CORS policy:
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
            <MaxAgeSeconds>3000</MaxAgeSeconds>
            <AllowedHeader>Authorization</AllowedHeader>
        </CORSRule>
    </CORSConfiguration>
    

## How to configure CloudFront for CORS support

Here&#8217;s where it gets a little bit tricky if you plan on using your CloudFront distribution for multiple domains.

From the <a href="http://www.w3.org/TR/cors/#resource-implementation" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.w3.org/TR/cors/#resource-implementation']);">CORS spec</a>:

> 6.4 Implementation Considerations Resources that wish to enable themselves to be shared with multiple Origins but do not respond uniformly with &#8220;*&#8221; must in practice generate the Access-Control-Allow-Origin header dynamically in response to every request they wish to allow. As a consequence, authors of such resources should send a Vary: Origin HTTP header or provide other appropriate control directives to prevent caching of such responses, which may be inaccurate if re-used across-origins.

In other words, there are 2 ways for resources to be shared with multiple Origins:

1.  Server returns `Access-Control-Allow-Origin: *` in HTTP response header
2.  Server dynamically generates `Access-Control-Allow-Origin` based on the `Origin` specified in the HTTP request header (this is what S3 does)

In order to allow access from multiple domains, our S3 CORS policy has this wildcard (*) in the CORS configuration line:

                <AllowedOrigin>*</AllowedOrigin>
    

S3 returns `Vary: Origin` in the HTTP response header because it dynamically generates the CORS HTTP response to every request based on the `Origin` header from the HTTP request. You can tell from the **curl** HTTP response headers below, namely `Access-Control-Allow-Origin: https://origin1.joeataws.info`:

    [20:36:00]$ curl -sI -H "Origin: https://origin1.joeataws.info" -H "Access-Control-Request-Method: GET" supernocarebucket.s3.amazonaws.com/public.txt
    HTTP/1.1 200 OK
    x-amz-id-2: /+OzYY9LyTbWw4biV/k39Dnf68hp8ZfnnUQbX+Qu91O4Sp2T/ItXGoJlTdz0fIYI
    x-amz-request-id: CFB29D7903389935
    Date: Fri, 09 Aug 2013 03:36:11 GMT
    Access-Control-Allow-Origin: https://origin1.joeataws.info
    Access-Control-Allow-Methods: GET
    Access-Control-Max-Age: 3000
    Access-Control-Allow-Credentials: true
    Vary: Origin, Access-Control-Request-Headers, Access-Control-Request-Method
    Last-Modified: Wed, 07 Aug 2013 16:16:39 GMT
    ETag: "c4a1be5e4c5527057839d16aa35222e0"
    Accept-Ranges: bytes
    Content-Type: text/plain
    Content-Length: 1615
    Server: AmazonS3
    

S3 doesn&#8217;t offer wildcards (*) in the CORS HTTP response header `Access-Control-Allow-Origin`.

CloudFront doesn&#8217;t offer support for `Vary: Origin`, and will cache whatever `Access-Control-Allow-Origin` response header was returned first from S3.

So how do you work around this and allow CloudFront to differentiate between different domains and the `Origin` headers they send?

**Enable the query string forwarding on your CloudFront distribution and use a unique query string for every domain you plan on sharing resources with.**

CloudFront will cache a seperate object for every query string parameter.

From the <a href="http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/QueryStringParameters.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/QueryStringParameters.html']);">AWS docs</a>:

> If you configure CloudFront to forward query strings to your origin, CloudFront will include the query string portion of the URL when caching the object. For example, the following query strings cause CloudFront to cache three objects. This is true even if your origin always returns the same image.jpg regardless of the query string:
> 
> *   http://d111111abcdef8.cloudfront.net/images/image.jpg?parameter1=a
> *   http://d111111abcdef8.cloudfront.net/images/image.jpg?parameter1=b
> *   http://d111111abcdef8.cloudfront.net/images/image.jpg?parameter1=c

As you can see, running a **curl** with `Origin: https://origin5.joeataws.info` request header causes a `X-Cache: Miss from cloudfront`.

    [09:26:58]$ curl -sI -H "Origin: https://origin4.joeataws.info" -H "Access-Control-Request-Method: GET" https://d11b6x4wyhg7u0.cloudfront.net/public.txt?origin=4
    HTTP/1.1 200 OK
    Content-Type: text/plain
    Content-Length: 1615
    Connection: keep-alive
    Date: Wed, 07 Aug 2013 16:27:12 GMT
    Access-Control-Allow-Origin: https://origin4.joeataws.info
    Access-Control-Allow-Methods: GET
    Access-Control-Max-Age: 3000
    Access-Control-Allow-Credentials: true
    Last-Modified: Wed, 07 Aug 2013 16:16:39 GMT
    ETag: "c4a1be5e4c5527057839d16aa35222e0"
    Accept-Ranges: bytes
    Server: AmazonS3
    Via: 1.0 fcaad488d818a994f233336c3591baa3.cloudfront.net (CloudFront)
    X-Cache: Miss from cloudfront
    X-Amz-Cf-Id: wn4dARGfi_T12juvXaHjYUNfouZX3r25E-BkrRUUxLzQXd7KhrNN5g==
    

Performing another request with the same CloudFront URL but using a different `Origin` request header (`Origin: https://origin5.joeataws.info`), we see the cached (but invalid) HTTP CORS response header returned: `Access-Control-Allow-Origin: https://origin4.joeataws.info`

This is invalid because the browser expects to see a matching domain in the `Access-Control-Allow-Origin` header.

    [09:27:11]$ curl -sI -H "Origin: https://origin5.joeataws.info" -H "Access-Control-Request-Method: GET" https://d11b6x4wyhg7u0.cloudfront.net/public.txt?origin=4
    HTTP/1.1 200 OK
    Content-Type: text/plain
    Content-Length: 1615
    Connection: keep-alive
    Date: Wed, 07 Aug 2013 16:27:12 GMT
    Access-Control-Allow-Origin: https://origin4.joeataws.info
    Access-Control-Allow-Methods: GET
    Access-Control-Max-Age: 3000
    Access-Control-Allow-Credentials: true
    Last-Modified: Wed, 07 Aug 2013 16:16:39 GMT
    ETag: "c4a1be5e4c5527057839d16aa35222e0"
    Accept-Ranges: bytes
    Server: AmazonS3
    Age: 24
    Via: 1.0 c8322bf52b16cf8e2526dd1edd273e42.cloudfront.net (CloudFront)
    X-Cache: Hit from cloudfront
    X-Amz-Cf-Id: tOikeHaUAXUQ-R5HOMdc0WZkzrh_2F5Gzuy1tZRmTJaWKxxKsqFAqQ==
    

Finally, we use the new `Origin: https://origin5.joeataws.info` header with a new query string (`?origin=5`), and we see a miss from CloudFront, and the appropriate `Access-Control-Allow-Origin` returned.

    [09:27:35]$ curl -sI -H "Origin: https://origin5.joeataws.info" -H "Access-Control-Request-Method: GET" https://d11b6x4wyhg7u0.cloudfront.net/public.txt?origin=5
    HTTP/1.1 200 OK
    Content-Type: text/plain
    Content-Length: 1615
    Connection: keep-alive
    Date: Wed, 07 Aug 2013 16:27:47 GMT
    Access-Control-Allow-Origin: https://origin5.joeataws.info
    Access-Control-Allow-Methods: GET
    Access-Control-Max-Age: 3000
    Access-Control-Allow-Credentials: true
    Last-Modified: Wed, 07 Aug 2013 16:16:39 GMT
    ETag: "c4a1be5e4c5527057839d16aa35222e0"
    Accept-Ranges: bytes
    Server: AmazonS3
    Via: 1.0 f92f8f7bfddd48b405cdd59b21a31a08.cloudfront.net (CloudFront)
    X-Cache: Miss from cloudfront
    X-Amz-Cf-Id: rWVTfakBMrh_VL-tMpmIGAzyyhLC_qOW_jeHGfN9XQjE8vFLKXc2kw==
    

## Resources

*   <a href="https://forums.aws.amazon.com/thread.jspa?messageID=446433" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forums.aws.amazon.com/thread.jspa?messageID=446433']);">AWS forum post about this</a>
*   <a href="http://www.w3.org/TR/cors/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.w3.org/TR/cors/']);">CORS W3C spec</a>
*   <a href="http://www.html5rocks.com/en/tutorials/cors/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.html5rocks.com/en/tutorials/cors/']);">Good post from html5rocks.com about CORS</a>
*   <a href="http://matthewgbaldwin.com/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://matthewgbaldwin.com/']);">CloudFront and S3 CORS demo from Matthew Baldwin</a>

