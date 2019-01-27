---
title: Set up simpleSAMLphp as an IdP to be Used in an SP-Initiated SSO with Google Apps
author: Karim Elatov
layout: post
permalink: /2013/05/set-up-simplesamlphp-as-an-idp-to-be-used-in-an-sp-initiated-sso-with-google-apps/
categories: ['os','home_lab']
tags: ['ubuntu', 'linux', 'saml', 'simplesamlphp', 'sso']
---

## SP-Initiated SAML SSO

Hopefully the title of the post isn't too confusing. To clear up what I am trying to achieve let's check out "[SP-initiated Single Sign-On POST/Artifact Bindings](http://saml.xml.org/wiki/sp-initiated-single-sign-on-postartifact-bindings)". Here is a pretty concise description of what SP (Service Provider) Initiated SSO (Single Sign On) means:

> This example describes an SP-initiated SSO exchange. In such an exchange, the user attempts to access a resource on the SP, sp.example.com. However they do not have a current logon session on this site and their federated identity is managed by their IdP, idp.example.org. They are sent to the IdP to log on and the IdP provides a SAML web SSO assertion for the user's federated identity back to the SP.

From the same site here is a step by step process:

> 1.  The user attempts to access a resource on **sp.example.com**. The user does not have a valid logon session (i.e. security context) on this site. The SP saves the requested resource URL in local state information that can be saved across the web SSO exchange.
>
> 2.  The SP sends an HTML form back to the browser in the HTTP response (**HTTP status 200**). The HTML FORM contains a SAML `<authnrequest>` message encoded as the value of a hidden form control named SAMLRequest.
>
>         `<form method="post" action="https://idp.example.org/SAML2/SSO/POST" ...>`
>         `<input type="hidden" name="SAMLRequest" value="request" />`
>         `<input type="hidden" name="RelayState" value="token" />...`
>         `<input type="submit" value="Submit" />`
>         `</form>`
>
>
>     The **RelayState** token is an opaque reference to state information maintained at the service provider. (The **RelayState** mechanism can leak details of the user's activities at the SP to the IdP and so the SP should take care in its implementation to protect the user's privacy.) The value of the SAMLRequest parameter is the *base64* encoding of the following `<samlp:authnrequest>` element:
>
>         `</samlp:authnrequest><samlp:authnrequest `
>         `xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"`
>         `xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"`
>         `ID="identifier_1"`
>         `Version="2.0"`
>         `IssueInstant="2004-12-05T09:21:59Z"`
>         `AssertionConsumerServiceIndex="1">`
>         `<saml:issuer>https://sp.example.com/SAML2</saml:issuer>`
>         `<samlp:nameidpolicy AllowCreate="true"`
>         `Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>`
>         `</samlp:nameidpolicy></samlp:authnrequest>`
>
>
> 3.  For ease-of-use purposes, the HTML FORM typically will be accompanied by script code that will automatically post the form to the destination site (which is the IdP in this case). The browser, due either to a user action or execution of an “auto-submit” script, issues an HTTP POST request to send the form to the identity provider's Single Sign-On Service.
>
>         POST /SAML2/SSO/POST HTTP/1.1
>         Host: idp.example.org
>         Content-Type: application/x-www-form-urlencoded
>         Content-Length: nnn
>         SAMLRequest=request&RelayState=token
>
>
> 4.  The Single Sign-On Service determines whether the user has an existing logon security context at the identity provider that meets the default or requested authentication policy requirements. If not, the IdP interacts with the browser to challenge the user to provide valid credentials.
>
> 5.  The user provides valid credentials and a local logon security context is created for the user at the IdP.
>
> 6.  The IdP Single Sign-On Service issues a SAML assertion representing the user's logon security context and places the assertion within a SAML message. Since in this example, the HTTP Artifact binding will be used to deliver the SAML Response message, it is not mandated that the assertion be digitally signed. The IdP creates an artifact containing the source ID for the **idp.example.org** site and a reference to the message (the MessageHandle). The artifact is delivered to the SP through a browser redirect.
>
> 7.  The SP's **Assertion Consumer Service** now sends a SAML message containing the artifact to the IdP's **Artifact Resolution Service** endpoint. This exchange is performed using a synchronous SOAP message exchange.
>
>         `<samlp:artifactresolve xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"`
>         `xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"`
>         `ID="identifier_2"`
>         `Version="2.0"`
>         `IssueInstant="2004-12-05T09:22:04Z"`
>         `Destination="https://idp.example.org/SAML2/ArtifactResolution">`
>         `<saml:issuer>https://sp.example.com/SAML2</saml:issuer>`
>         `<!-- an ArtifactResolve message SHOULD be signed -->`
>         `<ds:signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">...</ds:signature>`
>         `<samlp:artifact>artifact</samlp:artifact>`
>         `</samlp:artifactresolve>`
>
>
> 8.  The IdP's **Artifact Resolution Service** extracts the MessageHandle from the artifact and locates the original SAML `<response>` message associated with it. This `Response` is then placed inside a SAML `<artifactresponse>` message, which is returned to the SP over the SOAP channel.
>
>         `<samlp:artifactresponse `
>         `xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"`
>         `ID="identifier_3"`
>         `InResponseTo="identifier_2"`
>         `Version="2.0"`
>         `IssueInstant="2004-12-05T09:22:05Z">`
>         `<!-- an ArtifactResponse message SHOULD be signed -->`
>         `<ds:signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">...</ds:signature>`
>         `<samlp:status>`
>         `<samlp:statuscode `
>         `Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>`
>         `</samlp:statuscode></samlp:status>`
>         `<samlp:response>`
>         `.....`
>         `</samlp:response>`
>         `</samlp:artifactresponse>`
>
>
>     The SP extracts and processes the message and then processes the embedded assertion in order to create a local logon security context for the user at the SP. Once this is completed, the SP retrieves the local state information indicated by the **RelayState** data to recall the originally-requested resource URL. It then sends an HTTP redirect response to the browser directing it to access the originally requested resource.
>
> 9.  The SP makes an access check is made to establish whether the user has the correct authorization to access the resource. If the access check passes, the resource is then returned to the browser.

In our particular example simpleSAMLphp will be the IdP (Identity Provider) and Google Apps will be the SP (Service Provider). Google Apps supports SSO with SAML and that is why I am using it in this example. Actually here is the same process described on their site: "[SAML Single Sign-On (SSO) Service for Google Apps](https://developers.google.com/google-apps/sso/saml_reference_implementation)". For that site here is a diagram of the process:

![gapps sso saml Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/gapps_sso_saml.png)

After we set this up, we will take a look at the HTTP interaction in our Browser.

## Install SimpleSAMLPHP on Ubuntu

I used Ubuntu for my setup, so a simple:

    apt-get install simplesamlphp


Took care of the install. The install creates an Apache config:

    elatov@awsub:~$ head -3 /etc/simplesamlphp/apache.conf
    # simpleSAMLphp example Apache config snippet.
    # To include this in your Apache configuration:
    #   ln -s /etc/simplesamlphp/apache.conf /etc/apache2/conf.d/simplesamlphp.conf


To enable the config, just follow the above instructions:

    elatov@awsub:~$ sudo ln -s /etc/simplesamlphp/apache.conf /etc/apache2/conf.d/simplesamlphp.conf


For good measure, make sure the Apache configuration is okay:

    elatov@awsub:~$ sudo apache2ctl -t
    Syntax OK


Then go ahead and restart the Apache service:

    elatov@awsub:~$ sudo service apache2 restart
     * Restarting web server apache2                                                 ... waiting                                                             [ OK ]


At this point you can check to see if the SimpleSAMLPHP is working by visiting **http://localhost/simplesamlphp**. You should see the following:

![simplesamlphp install page Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesamlphp-install-page.png)

## Configure SimpleSAMLPHP as an IdP (Identity Provider)

Luckily there is a pretty good guide from SimpleSAMLPHP: [Setting up a simpleSAMLphp SAML 2.0 IdP to use with Google Apps for Education](https://simplesamlphp.org/docs/stable/simplesamlphp-googleapps). So let's go through the guide.

### Enabling the Identity Provider functionality in SimpleSAMLPHP

Edit the **/etc/simplesamlphp/config.php** file and make the following changes:

    'enable.saml20-idp' => true,
    'enable.shib13-idp' => false,


### Setting up an SSL signing certificate

First generate the certificate with the following commands:

    openssl genrsa -des3 -out googleappsidp.key 1024
    openssl rsa -in googleappsidp.key -out googleappsidp.pem
    openssl req -new -key googleappsidp.key -out googleappsidp.csr
    openssl x509 -req -days 9999 -in googleappsidp.csr -signkey googleappsidp.key -out googleappsidp.crt


**Note:** simpleSAMLphp will only work with *RSA* and not *DSA* certificates.

Fill out the request as you desire. Lastly go ahead and copy the private key (without the password) and the certificate to the SSL Certificate database/directory. For Ubuntu this is under **/etc/ssl/certs** and **/etc/ssl/private**. I will add both under **/etc/ssl/certs**, this way SimpleSAMLPHP will be able read them:

    elatov@awsub:~$ sudo cp googleappsidp.crt /etc/ssl/certs/.
    elatov@awsub:~$ sudo cp googleappsidp.pem /etc/ssl/certs/.


### Configuring the authentication source in SimpleSAMLPHP

SimpleSAMLPHP can connect to an *LDAP* server for an authentication source. I didn't want to setup an LDAP server on the same machine, so I just used the **exampleauth:UserPass** authentication source provided by SimpleSAMLPHP. First let's enable the **exampleauth** module, this is done by running the following:

    elatov@awsub:~$ sudo touch /usr/share/simplesamlphp/modules/exampleauth/enable


Next, edit the **/etc/simplesamlphp/authsources.php** file and add the following section under the **example-userpass** section:

    'example-userpass' => array( 'exampleauth:UserPass',
                    'test:password' => array( 'uid' => array('test'),),),


That will add a user called *test* with a password of **password**. After the user is logged the attribute of **uid** will be returned (in our case it's the same as the username: **test**). This has to match the username that is created in Google apps.

### Testing *Example-Userpass* Authentication Source

Now that we added a **test** user, let's make sure we can login with the **test** credentials. Point your browser to the SimpleSAMLPHP install (in my case it was **http://awsub.dnsd.me/simplesamlphp**) and then click on the "Authentication" tab. You will see the following:

![simplesaml php auth tab Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesaml-php-auth-tab.png)

Then click on "Test configured authentication sources" and you will see the following:

![simplesamlplhp test auth sources Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesamlplhp-test_auth-sources.png)

Then click on "example-userpass" and you will see the following:

![simplesamlphp enter user and pass Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesamlphp-enter-user-and-pass.png)

Then enter your credentials and if it successfully authenticates, you will see the following:

![simplesamlphp logged in Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesamlphp-logged-in.png)

That looks good and it's returning the appropriate attribute.

### Configuring SAML 2.0 IdP Hosted Metadata

So we already enabled SimpleSAMLPHP to act as an IdP, now let's configure it. Edit the **/etc/simplesamlphp/metadata/saml20-idp-hosted.php** file and add the following to the file:

    elatov@awsub:~$ cat /etc/simplesamlphp/metadata/saml20-idp-hosted.php
    < ?php
    $metadata['__DYNAMIC:1__'] = array(
        // The hostname of the server (VHOST) that this SAML entity will use.
        'host'              =>  '__DEFAULT__',

        // X.509 key and certificate. Relative to the cert directory.
        'privatekey'   => 'googleappsidp.pem',
        'certificate'  => 'googleappsidp.crt',

        'auth' => 'example-userpass',
    );


### Configuring SAML 2.0 SP Remote Metadata

Now let's configure the SP (Service Provider) that we are going trust and authenticate for in our setup ( in our case it's Google Apps). Edit the /**etc/simplesamlphp/metadata/saml20-sp-remote.php** file and add the following to it:

    elatov@awsub:~$ cat /etc/simplesamlphp/metadata/saml20-sp-remote.php
    < ?php
    $metadata['google.com'] = array(
        'AssertionConsumerService'   => 'https://www.google.com/a/moxz.mine.nu/acs',
        'NameIDFormat'               => 'urn:oasis:names:tc:SAML:2.0:nameid-format:email',
        'simplesaml.nameidattribute' => 'uid',
        'simplesaml.attributes'      => false
    );


Populate the **AssertionConsumerService** appropriately, change the domain to match the domain of your Google Apps (in my case it was **moxz.mine.nu**).

## Enable SSO for Google Apps

These instructions are also laid out in the same SimpleSAMLPHP [page](https://simplesamlphp.org/docs/stable/simplesamlphp-googleapps).

### Login to your Google Apps Admin Portal/Dashboard

Go to your domain's Google Apps page, mine is **http://www.google.com/a/moxz.nine.nu** and you will see something like this:

![moxz mine nu gapps Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/moxz_mine_nu_gapps.png)

After you login as the Administrator you will see the following:

![google apps dashboard Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/google_apps_dashboard.png)

### Configure SSO For Google Apps

Then click on the "Advanced tools" tab:

![adv tools tab gapps Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/adv-tools-tab-gapps.png)

Then click on "Set up single sign-on (SSO)" and fill out all the necessary information:

![gapps sso settings Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/gapps_sso_settings.png)

Here are all the values:

*   **Sign-in page URL**

    *   http://awsub.dnsd.me/simplesamlphp/saml2/idp/SSOService.php

*   **Sign-out page URL**

    *   http://awsub.dnsd.me/simplesamlphp/saml2/idp/initSLO.php?RelayState=/simplesamlphp/logout.php

*   **Change password URL**

    *   http://awsub.dnsd.me

*   **Verification certificate**

    *   googleappsidp.crt

### Add a User to your Google Apps Domain

Click on the "Users" tab in the Google Apps Dashboard and then click on "Create User":

![testuser gapps Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/testuser_gapps.png)

After it's created you will see your *test* user. Make sure the **username** for the user matches the **uid** that you created in SimpleSAMLPHP in the *Example-Userpass* Authentication Source (in my case it was **test**). Here is my **test** user in Google Apps:

![users tab gapps Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/users-tab-gapps.png)

## Test out SSO

Go to **gmail.com** and try to login to your domain with the test user:

![gmail login Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/gmail_login.png)

After you try to login, you see the following message:

![gmail sso turned on Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/gmail_sso_turned_on.png)

This is the SP telling us to go to the IdP to get authenticated. As soon as you hit "Sign In", you will see the following:

![simplesamlphp authenticate Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesamlphp-authenticate.png)

After you authenticate it will redirect you back to Gmail:

![loggedin gmail test Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/loggedin_gmail_test.png)

Another note, if you go directly to **mail.google.com/a/moxz.mine.nu** it will redirect you directly to the IdP. If you sign out of *gmail*:

![gmail signout Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/gmail-signout.png)

You will be take to the IdP's log-out page:

![simplesaml php loggedout Set up simpleSAMLphp as an IdP to be Used in an SP Initiated SSO with Google Apps](https://github.com/elatov/uploads/raw/master/2013/04/simplesaml-php-loggedout.png)

And everything worked out okay.

## Checking out HTTP Headers in an SP-Initiated SAML SSO Exchange

There are many tools out there that can help with this:

*   [HTTPFox](https://discourse.mozilla.org/t/httpfox-add-on-not-available-in-new-firefox-version/22566)
*   [Charles Proxy](http://www.charlesproxy.com/)
*   [Chrome Developer Tools](https://developer.chrome.com/devtools)
*   [Fiddler](http://fiddler2.com/)
*   [Live HTTP Headers](https://addons.mozilla.org/en-US/firefox/addon/http-header-live/)

I prefer Charles Proxy because it's a stand alone application. You point your browser to proxy all of it's traffic through Charles and you can see everything. While the other tools, attach themselves to the Browser and show you the traffic. For ease of use, I will use *Live HTTP Headers* cause it easy to copy Header information from it :)

Here is what I saw after I hit "Sign In" from gmail:

    https://accounts.google.com/ServiceLoginAuth

    POST /ServiceLoginAuth HTTP/1.1
    Host: accounts.google.com
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: https://accounts.google.com/ServiceLoginAuth
    Cookie: GAPS=1:M4Q7EObe_W5EWEt
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 693

    HTTP/1.1 302 Moved Temporarily
    Cache-Control: private, max-age=0
    Content-Encoding: gzip
    Content-Length: 704
    Content-Type: text/html; charset=UTF-8
    Date: Sat, 27 Apr 2013 21:13:20 GMT
    Expires: Sat, 27 Apr 2013 21:13:20 GMT
    Location: http://awsub.dnsd.me/simplesamlphp/saml2/idp/SSOService.php?SAMLRequest=fVLJTsMwEL0j8Q%2BR71lBAllNUAEhKrFENHDg5iaTxJU9Dh6nBb4eNwUBB7g%2Bv3nLeGZnr1oFG7AkDeYsjRIWANamkdjl7LG6Ck%2FZWXF4MCOh1cDno%2BvxAV5GIBf4SSQ%2BPeRstMiNIEkchQbirubL%2Be0Nz6KED9Y4UxvFgsVlztZrIUWnBlC9ggZF1%2Fd6aA32K0SB637VaqNRefbTV6xsF2tBNMICyQl0HkrSozA5DrOTKkt5esSz5JkF5afTucR9g%2F9irfYk4tdVVYbl%2FbKaBDayAXvn2TnrjOkURLXRO%2FtSEMmNh1uhCFgwJwLrfMALgzRqsEuwG1nD48NNznrnBuJxvN1uo2%2BZWMTavL5HWiJEOMaiJlZMu%2BVTPftjqf%2BHF1%2FmrPiWn8U%2FpIrPP9tVWVyWRsn6LZgrZbYXFoTzPZwdfY0rY7Vwf7ulUTohsgnbicpHpAFq2UpoWBAXe9ffx%2BFP5gM%3D&RelayState=https%3A%2F%2Faccounts.google.com%2FCheckCookie%3Fcontinue%3Dhttp%253A%252F%252Fmail.google.com%252Fmail%252F%26service%3Dmail%26ltmpl%3Ddefault
    Server: GSE


This is basically Step 2 and 3 from the above picture. We post to google:

    https://accounts.google.com/ServiceLoginAuth
    POST /ServiceLoginAuth HTTP/1.1


and that redirects us to the IdP with the SAML request included:

    HTTP/1.1 302 Moved Temporarily
    Location: http://awsub.dnsd.me/simplesamlphp/saml2/idp/SSOService.php?SAMLRequest=fVLJTsMwEL0j8Q%2BR71lBAllNUAEhKrFENHDg5iaTxJU9Dh6nBb4eNwUBB7g%2Bv3nLeGZnr1oFG7AkDeYsjRIWANamkdjl7LG6Ck%2FZWXF4MCOh1cDno%2BvxAV5GIBf4SSQ%2BPeRstMiNIEkchQbirubL%2Be0Nz6KED9Y4UxvFgsVlztZrIUWnBlC9ggZF1%2Fd6aA32K0SB637VaqNRefbTV6xsF2tBNMICyQl0HkrSozA5DrOTKkt5esSz5JkF5afTucR9g%2F9irfYk4tdVVYbl%2FbKaBDayAXvn2TnrjOkURLXRO%2FtSEMmNh1uhCFgwJwLrfMALgzRqsEuwG1nD48NNznrnBuJxvN1uo2%2BZWMTavL5HWiJEOMaiJlZMu%2BVTPftjqf%2BHF1%2FmrPiWn8U%2FpIrPP9tVWVyWRsn6LZgrZbYXFoTzPZwdfY0rY7Vwf7ulUTohsgnbicpHpAFq2UpoWBAXe9ffx%2BFP5gM%3D&RelayState=https%3A%2F%2Faccounts.google.com%2FCheckCookie%3Fcontinue%3Dhttp%253A%252F%252Fmail.google.com%252Fmail%252F%26service%3Dmail%26ltmpl%3Ddefault


Decoding the SAML Request (using this [tool](https://rnd.feide.no/2012/08/29/announcing-new-sparkling-saml-2-0-debugger/)) since it's base64 encoded, we get this:

    < ?xml version="1.0" encoding="UTF-8"?>
    <samlp:authnrequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    ID="jjaiaglpelhlednaghhmpfonhbnnanjhbfmomnll"
    Version="2.0"
    IssueInstant="2013-04-27T21:13:20Z"
    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    ProviderName="google.com"
    IsPassive="false"
    AssertionConsumerServiceURL="https://www.google.com/a/moxz.mine.nu/acs">
    <saml:issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">google.com</saml:issuer>
    <samlp:nameidpolicy AllowCreate="true"
    Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"></samlp:nameidpolicy>
    </samlp:authnrequest>


**Note:** I grabbed the string between **SAMLRequest=** and **&RelayState**

From the above we can see the Provider name is **google.com**, the **ACS URL** (Assertion Consumer Service) is **https://www.google.com/a/moxz.mine.nu/acs**, and other variables are defined as well. Then we see the actual data go to the IdP:

    GET /simplesamlphp/saml2/idp/SSOService.php?SAMLRequest=fVLJTsMwEL0j8Q%2BR7 HTTP/1.1
    Host: awsub.dnsd.me
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Connection: keep-alive

    HTTP/1.1 302 Found
    Date: Sat, 27 Apr 2013 21:13:25 GMT
    Server: Apache/2.2.22 (Ubuntu)
    X-Powered-By: PHP/5.3.10-1ubuntu3.6
    Set-Cookie: PHPSESSID=f089638ddc840835fb47879ad5ec68ee; path=/
    Expires: Thu, 19 Nov 1981 08:52:00 GMT
    Cache-Control: no-cache, must-revalidate
    Pragma: no-cache
    Location: http://awsub.dnsd.me/simplesamlphp/module.php/core/loginuserpass.php?AuthState=_f4ef5d3c522ed1754e98aeb999b424e3f915c5aefc%3Ahttp%3A%2F%2Fawsub.dnsd.me%2Fsimplesamlphp%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dgoogle.com%26cookieTime%3D1367097205%26RelayState%3Dhttps%253A%252F%252Faccounts.google.com%252FCheckCookie%253Fcontinue%253Dhttp%25253A%25252F%25252Fmail.google.com%25252Fmail%25252F%2526service%253Dmail%2526ltmpl%253Ddefault
    Vary: Accept-Encoding
    Content-Encoding: gzip
    Content-Length: 598
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html


We get a **302 Found** which is good. At this point the IdP takes care of the authentication. Here is login process on the IdP:

    POST /simplesamlphp/module.php/core/loginuserpass.php? HTTP/1.1
    Host: awsub.dnsd.me
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://awsub.dnsd.me/simplesamlphp/module.php/core/loginuserpass.php?AuthState=_a5482b21099f41743ad139014fb0794a02ea18521b%3Ahttp%3A%2F%2Fawsub.dnsd.me%2Fsimplesamlphp%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dgoogle.com%26cookieTime%3D1367098785%26RelayState%3Dhttps%253A%252F%252Faccounts.google.com%252FCheckCookie%253Fcontinue%253Dhttp%25253A%25252F%25252Fmail.google.com%25252Fmail%25252F%2526service%253Dmail%2526ltmpl%253Ddefault
    Cookie: PHPSESSID=f089638ddc840835fb47879ad5ec68ee
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 403
    username=test&password=password&AuthState=_a5482b21099f41743ad139014fb0794a02ea18521b%3Ahttp%3A%2F%2Fawsub.dnsd.me%2Fsimplesamlphp%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dgoogle.com%26cookieTime%3D1367098785%26RelayState%3Dhttps%253A%252F%252Faccounts.google.com%252FCheckCookie%253Fcontinue%253Dhttp%25253A%25252F%25252Fmail.google.com%25252Fmail%25252F%2526service%253Dmail%2526ltmpl%253Ddefault

    HTTP/1.1 200 OK
    Date: Sat, 27 Apr 2013 21:39:52 GMT
    Server: Apache/2.2.22 (Ubuntu)
    X-Powered-By: PHP/5.3.10-1ubuntu3.6
    Expires: Thu, 19 Nov 1981 08:52:00 GMT
    Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
    Pragma: no-cache
    Set-Cookie: SimpleSAMLAuthToken=_61b4c67a6300f1c2c27d50537b1421f4073f8fc158; path=/
    Vary: Accept-Encoding
    Content-Encoding: gzip
    Content-Length: 4516
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html


We ca see our super cool creds (**test/password**) and the **RelayState** is kept so we know which session this authentication process corresponds to. And here is the response that is sent from the IdP to the SP:

    https://www.google.com/a/moxz.mine.nu/acs

    POST /a/moxz.mine.nu/acs HTTP/1.1
    Host: www.google.com
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer:
    Cookie: GMAIL_RTT=1063; GMAIL_LOGIN=T1367097141172/1367097141172/1367097200128
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 7341
    SAMLResponse=PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSJwZnhkYWNhNjAwNC0wNGE3LWYyMjktNzhhYi1iNTdmZDgzZTQyZTUiIFZlcnNpb249IjIuMCIgSXNzdWVJbnN0YW50PSIyMDEzLTA0LTI3VDIxOjM5OjUyWiIgRGVzdGluYXRpb249Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20vYS9tb3h6Lm1pbmUubnUvYWNzIj48c2FtbDpJc3N1ZXI%2BaHR0cDovL2F3c3ViLmRuc2QubWUvc2ltcGxlc2FtbHBocC9zYW1sMi9pZHAvbWV0YWRhdGEucGhwPC9zYW1sOklzc3Vlcj48ZHM6U2lnbmF0dXJlIHhtbG5zOmRzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjIj4KICA8ZHM6U2lnbmVkSW5mbz48ZHM6Q2Fub25pY2FsaXphdGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyIvPgogICAgPGRzOlNpZ25hdHVyZU1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNyc2Etc2hhMSIvPgogIDxkczpSZWZlcmVuY2UgVVJJPSIjcGZ4ZGFjYTYwMDQtMDRhNy1mMjI5LTc4YWItYjU3ZmQ4M2U0MmU1Ij48ZHM6VHJhbnNmb3Jtcz48ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnI2VudmVsb3BlZC1zaWduYXR1cmUiLz48ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8xMC94bWwtZXhjLWMxNG4jIi8%2BPC9kczpUcmFuc2Zvcm1zPjxkczpEaWdlc3RNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjc2hhMSIvPjxkczpEaWdlc3RWYWx1ZT5VcFdaZ3phVzVZdk1FdnVBYysyQk1CUXVMREk9PC9kczpEaWdlc3RWYWx1ZT48L2RzOlJlZmVyZW5jZT48L2RzOlNpZ25lZEluZm8%2BPGRzOlNpZ25hdHVyZVZhbHVlPm4za2hoS2ZhSURRWXdlZTNZaEtkZTkzNjgrczlpL2VxODNweFNkektQUXo5SFZNUlYxS1RmVWVPSjFLeVN6RzBqTTdBdlRnTUZDcndUb1hNZ2RTRWsrSEhDUHFHMzJQazJyRG5YditzRHpuL1hLcE0yRDYzQWVkUTREZDFDekNiNWdCdjN4WkRGMU54dXlPOERHUVlPb0VvMnlmZURORFdSQkVQRUpkQVFScz08L2RzOlNpZ25hdHVyZVZhbHVlPgo8ZHM6S2V5SW5mbz48ZHM6WDUwOURhdGE%2BPGRzOlg1MDlDZXJ0aWZpY2F0ZT5NSUlDaXpDQ0FmUUNDUUM2TXhQNGJSaTdlakFOQmdrcWhraUc5dzBCQVFVRkFEQ0JpVEVMTUFrR0ExVUVCaE1DVlZNeEVUQVBCZ05WQkFnTUNFTnZiRzl5WVdSdk1SQXdEZ1lEVlFRSERBZENiM1ZzWkdWeU1RMHdDd1lEVlFRS0RBUkliMjFsTVEwd0N3WURWUVFMREFSTmIzaDZNUll3RkFZRFZRUUREQTFoZDNOMVlpNWtibk5rTG0xbE1SOHdIUVlKS29aSWh2Y05BUWtCRmhCbGJHRjBiM1pBWjIxaGFXd3VZMjl0TUI0WERURXpNRFF5TVRFNU1USTFPVm9YRFRRd01Ea3dOVEU1TVRJMU9Wb3dnWWt4Q3pBSkJnTlZCQVlUQWxWVE1SRXdEd1lEVlFRSURBaERiMnh2Y21Ga2J6RVFNQTRHQTFVRUJ3d0hRbTkxYkdSbGNqRU5NQXNHQTFVRUNnd0VTRzl0WlRFTk1Bc0dBMVVFQ3d3RVRXOTRlakVXTUJRR0ExVUVBd3dOWVhkemRXSXVaRzV6WkM1dFpURWZNQjBHQ1NxR1NJYjNEUUVKQVJZUVpXeGhkRzkyUUdkdFlXbHNMbU52YlRDQm56QU5CZ2txaGtpRzl3MEJBUUVGQUFPQmpRQXdnWWtDZ1lFQXRaazlxamxjbHRDSjBRT2dFbmx6WHhsOEorWFhzblovSjRyNTNBektrR2laYVlqenNvTHVxamJWRklUN25md1VmekF3ajN4VDNNZTNIZEMxamI1eXBOZDMvc0N5VVYxcnUrNm5RSzZERHpHWkxycXEzWXFjRC90Vmw4NTVRSi96VzdwbGJpakRWQlc4OUlvRURFWlBEcFFSU0doVWQwRE5UclhpZXJ4eXgxTUNBd0VBQVRBTkJna3Foa2lHOXcwQkFRVUZBQU9CZ1FDelgwZjZFaFdOZWo4K2hxMnpmTHZDVDhyQ0hEY21xKzZtTDIxOVVJU3RpRnlyQ1JLc3ZtNVgxekphYmltSDFXZmJWeFJFUUNTNmUwak5GdkF0RytpWVgrbUVibHFrOHFPSTJOMVpReE5ORUZPUHUrS3ZZTzNmVWlPTUFyazh3UjdZTUFEYXBuY0FQUTMxc0ZVSXc2UXh4RkhNSEowcnJEb2t6OVZxMTFvUzRnPT08L2RzOlg1MDlDZXJ0aWZpY2F0ZT48L2RzOlg1MDlEYXRhPjwvZHM6S2V5SW5mbz48L2RzOlNpZ25hdHVyZT48c2FtbHA6U3RhdHVzPjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiLz48L3NhbWxwOlN0YXR1cz48c2FtbDpBc3NlcnRpb24geG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSIgeG1sbnM6eHM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hIiBJRD0icGZ4YWQyZTY0ODItMzk5MC1lZjkxLWUwOWEtYmMzMjZlNzNhODA2IiBWZXJzaW9uPSIyLjAiIElzc3VlSW5zdGFudD0iMjAxMy0wNC0yN1QyMTozOTo1MloiPjxzYW1sOklzc3Vlcj5odHRwOi8vYXdzdWIuZG5zZC5tZS9zaW1wbGVzYW1scGhwL3NhbWwyL2lkcC9tZXRhZGF0YS5waHA8L3NhbWw6SXNzdWVyPjxkczpTaWduYXR1cmUgeG1sbnM6ZHM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyMiPgogIDxkczpTaWduZWRJbmZvPjxkczpDYW5vbmljYWxpemF0aW9uTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8xMC94bWwtZXhjLWMxNG4jIi8%2BCiAgICA8ZHM6U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnI3JzYS1zaGExIi8%2BCiAgPGRzOlJlZmVyZW5jZSBVUkk9IiNwZnhhZDJlNjQ4Mi0zOTkwLWVmOTEtZTA5YS1iYzMyNmU3M2E4MDYiPjxkczpUcmFuc2Zvcm1zPjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjZW52ZWxvcGVkLXNpZ25hdHVyZSIvPjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiLz48L2RzOlRyYW5zZm9ybXM%2BPGRzOkRpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNzaGExIi8%2BPGRzOkRpZ2VzdFZhbHVlPmJKYm9Ccm9DdFBJcEVUQmZleERsSWpZOURiaz08L2RzOkRpZ2VzdFZhbHVlPjwvZHM6UmVmZXJlbmNlPjwvZHM6U2lnbmVkSW5mbz48ZHM6U2lnbmF0dXJlVmFsdWU%2BQ05XNU1sQUYxU1FpWlljUFdrY0JUY0hvekF2WFVjZ3JsbXBEV1AxSkR0L013ZGtjWnVPbXFlUFhVUFYrZktUbVpBMmQ5SWsvbnpkY3M1SExxSGtJMnJxNWtzYWhPTll1K3pSRUdjQ0c1ZEI2L2t3bmM4cDdBcUFEQ1ZDMzNzNW5DSnYrbGJSTjdlUnZnTnVBY1E4VlF4NGt3ZEpHSTVpNVo0SGVjYWM3RzVBPTwvZHM6U2lnbmF0dXJlVmFsdWU%2BCjxkczpLZXlJbmZvPjxkczpYNTA5RGF0YT48ZHM6WDUwOUNlcnRpZmljYXRlPk1JSUNpekNDQWZRQ0NRQzZNeFA0YlJpN2VqQU5CZ2txaGtpRzl3MEJBUVVGQURDQmlURUxNQWtHQTFVRUJoTUNWVk14RVRBUEJnTlZCQWdNQ0VOdmJHOXlZV1J2TVJBd0RnWURWUVFIREFkQ2IzVnNaR1Z5TVEwd0N3WURWUVFLREFSSWIyMWxNUTB3Q3dZRFZRUUxEQVJOYjNoNk1SWXdGQVlEVlFRRERBMWhkM04xWWk1a2JuTmtMbTFsTVI4d0hRWUpLb1pJaHZjTkFRa0JGaEJsYkdGMGIzWkFaMjFoYVd3dVkyOXRNQjRYRFRFek1EUXlNVEU1TVRJMU9Wb1hEVFF3TURrd05URTVNVEkxT1Zvd2dZa3hDekFKQmdOVkJBWVRBbFZUTVJFd0R3WURWUVFJREFoRGIyeHZjbUZrYnpFUU1BNEdBMVVFQnd3SFFtOTFiR1JsY2pFTk1Bc0dBMVVFQ2d3RVNHOXRaVEVOTUFzR0ExVUVDd3dFVFc5NGVqRVdNQlFHQTFVRUF3d05ZWGR6ZFdJdVpHNXpaQzV0WlRFZk1CMEdDU3FHU0liM0RRRUpBUllRWld4aGRHOTJRR2R0WVdsc0xtTnZiVENCbnpBTkJna3Foa2lHOXcwQkFRRUZBQU9CalFBd2dZa0NnWUVBdFprOXFqbGNsdENKMFFPZ0VubHpYeGw4SitYWHNuWi9KNHI1M0F6S2tHaVphWWp6c29MdXFqYlZGSVQ3bmZ3VWZ6QXdqM3hUM01lM0hkQzFqYjV5cE5kMy9zQ3lVVjFydSs2blFLNkREekdaTHJxcTNZcWNEL3RWbDg1NVFKL3pXN3BsYmlqRFZCVzg5SW9FREVaUERwUVJTR2hVZDBETlRyWGllcnh5eDFNQ0F3RUFBVEFOQmdrcWhraUc5dzBCQVFVRkFBT0JnUUN6WDBmNkVoV05lajgraHEyemZMdkNUOHJDSERjbXErNm1MMjE5VUlTdGlGeXJDUktzdm01WDF6SmFiaW1IMVdmYlZ4UkVRQ1M2ZTBqTkZ2QXRHK2lZWCttRWJscWs4cU9JMk4xWlF4Tk5FRk9QdStLdllPM2ZVaU9NQXJrOHdSN1lNQURhcG5jQVBRMzFzRlVJdzZReHhGSE1ISjByckRva3o5VnExMW9TNGc9PTwvZHM6WDUwOUNlcnRpZmljYXRlPjwvZHM6WDUwOURhdGE%2BPC9kczpLZXlJbmZvPjwvZHM6U2lnbmF0dXJlPjxzYW1sOlN1YmplY3Q%2BPHNhbWw6TmFtZUlEIFNQTmFtZVF1YWxpZmllcj0iZ29vZ2xlLmNvbSIgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbWFpbCI%2BdGVzdDwvc2FtbDpOYW1lSUQ%2BPHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbiBNZXRob2Q9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpjbTpiZWFyZXIiPjxzYW1sOlN1YmplY3RDb25maXJtYXRpb25EYXRhIE5vdE9uT3JBZnRlcj0iMjAxMy0wNC0yN1QyMTo0NDo1MloiIFJlY2lwaWVudD0iaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9hL21veHoubWluZS5udS9hY3MiLz48L3NhbWw6U3ViamVjdENvbmZpcm1hdGlvbj48L3NhbWw6U3ViamVjdD48c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMjAxMy0wNC0yN1QyMTozOToyMloiIE5vdE9uT3JBZnRlcj0iMjAxMy0wNC0yN1QyMTo0NDo1MloiPjxzYW1sOkF1ZGllbmNlUmVzdHJpY3Rpb24%2BPHNhbWw6QXVkaWVuY2U%2BZ29vZ2xlLmNvbTwvc2FtbDpBdWRpZW5jZT48L3NhbWw6QXVkaWVuY2VSZXN0cmljdGlvbj48L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTMtMDQtMjdUMjE6Mzk6NTJaIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDEzLTA0LTI4VDA1OjM5OjUyWiIgU2Vzc2lvbkluZGV4PSJfYjAxNDg1N2Y2ODBiNGJiMzkzNTVhM2I2OWVhYThkODU2ZTFmMGMyODJhIj48c2FtbDpBdXRobkNvbnRleHQ%2BPHNhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY%2BdXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFjOmNsYXNzZXM6UGFzc3dvcmQ8L3NhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY%2BPC9zYW1sOkF1dGhuQ29udGV4dD48L3NhbWw6QXV0aG5TdGF0ZW1lbnQ%2BPC9zYW1sOkFzc2VydGlvbj48L3NhbWxwOlJlc3BvbnNlPg%3D%3D&RelayState=https%3A%2F%2Faccounts.google.com%2FCheckCookie%3Fcontinue%3Dhttp%253A%252F%252Fmail.google.com%252Fmail%252F%26service%3Dmail%26ltmpl%3Ddefault

    HTTP/1.1 200 OK
    Cache-Control: private, max-age=0
    Content-Encoding: gzip
    Content-Length: 790
    Content-Type: text/html; charset=UTF-8
    Date: Sat, 27 Apr 2013 21:39:48 GMT
    Expires: Sat, 27 Apr 2013 21:39:48 GMT
    Server: GSE
    X-Content-Type-Options: nosniff
    X-XSS-Protection: 0
    X-Firefox-Spdy: 3


This is basically steps 4-6 from the diagram. Decoding that SAML Response we get the following:

    <samlp:response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    ID="pfxdaca6004-04a7-f229-78ab-b57fd83e42e5"
    Version="2.0"
    IssueInstant="2013-04-27T21:39:52Z"
    Destination="https://www.google.com/a/moxz.mine.nu/acs"><saml:issuer>http://awsub.dnsd.me/simplesamlphp/saml2/idp/metadata.php</saml:issuer>
    <ds:signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
      <ds:signedinfo><ds:canonicalizationmethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:canonicalizationmethod>
        <ds:signaturemethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:signaturemethod>
      <ds:reference URI="#pfxdaca6004-04a7-f229-78ab-b57fd83e42e5"><ds:transforms><ds:transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:transform>
    <ds:transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:transform>
    </ds:transforms><ds:digestmethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:digestmethod><ds:digestvalue>UpWZgzaW5YvMEvuAc+2BMBQuLDI=</ds:digestvalue>
    </ds:reference>
    </ds:signedinfo><ds:signaturevalue>n3khhKfaIDQYwee3YhKde9368+yfeDNDWRBEPEJdAQRs=</ds:signaturevalue>
    <ds:keyinfo><ds:x509data>
    <ds:x509certificate>MIICizCg==</ds:x509certificate>
    </ds:x509data></ds:keyinfo>
    </ds:signature><samlp:status>
    <samlp:statuscode Value="urn:oasis:names:tc:SAML:2.0:status:Success"></samlp:statuscode>< /samlp:Status><saml:assertion xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    ID="pfxad2e6482-3990-ef91-e09a-bc326e73a806"
    Version="2.0"
    IssueInstant="2013-04-27T21:39:52Z">
    <saml:issuer>http://awsub.dnsd.me/simplesamlphp/saml2/idp/metadata.php</saml:issuer>
    <ds:signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
      <ds:signedinfo><ds:canonicalizationmethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:canonicalizationmethod>
        <ds:signaturemethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:signaturemethod>
      <ds:reference URI="#pfxad2e6482-3990-ef91-e09a-bc326e73a806"><ds:transforms><ds:transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:transform>
    <ds:transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:transform>
    </ds:transforms><ds:digestmethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:digestmethod><ds:digestvalue>bJboBroCtPIpETBfexDlIjY9Dbk=</ds:digestvalue>
    </ds:reference></ds:signedinfo><ds:signaturevalue>CNW5MlAF1SQiZYcPWcQ8VQx4kwdJGI5i5Z4Hecac7G5A=</ds:signaturevalue>
    <ds:keyinfo><ds:x509data>
    <ds:x509certificate>MI==</ds:x509certificate>
    </ds:x509data></ds:keyinfo></ds:signature>
    <saml:subject>
    <saml:nameid SPNameQualifier="google.com"
    Format="urn:oasis:names:tc:SAML:2.0:nameid-format:email">test</saml:nameid>
    <saml:subjectconfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
    <saml:subjectconfirmationdata NotOnOrAfter="2013-04-27T21:44:52Z"
    Recipient="https://www.google.com/a/moxz.mine.nu/acs"></saml:subjectconfirmationdata>
    </saml:subjectconfirmation>
    </saml:subject>
    <saml:conditions NotBefore="2013-04-27T21:39:22Z"
    NotOnOrAfter="2013-04-27T21:44:52Z">
    <saml:audiencerestriction>
    <saml:audience>google.com</saml:audience>
    </saml:audiencerestriction></saml:conditions>
    <saml:authnstatement AuthnInstant="2013-04-27T21:39:52Z"
    SessionNotOnOrAfter="2013-04-28T05:39:52Z"
    SessionIndex="_b014857f680b4bb39355a3b69eaa8d856e1f0c282a">
    <saml:authncontext>
    <saml:authncontextclassref>urn:oasis:names:tc:SAML:2.0:ac:classes:Password</saml:authncontextclassref>
    </saml:authncontext>
    </saml:authnstatement>
    </saml:assertion>
    </samlp:status></samlp:response>


We can see the certificate used for the signature and the signature it self. We also see the expiration dates for the assertion. The most important thing to check for is the following:

    `Format="urn:oasis:names:tc:SAML:2.0:nameid-format:email">test`


This ensures that this is for the **test** user. And finally Google confirms the SAML Assertion and directs us to the gmail page:

    https://mail.google.com/mail/?auth=DQAAAIMAAABnua9GG0M

    GET /mail/?auth=DQAAAIMAAABnua9GG0MT-tvplNuWWHYhDzdqQujRwZbBajn88VRr9KtXR-oQZDzJQi2t7UH_4KOdZRZ2jpjd-KpqgMG6K-YFN2zDL5z6T_6mAybLzrTeLojLFoawA4j4JEvW0BfVElT26tYAliaLP4imdvRRnb_2lAEopz8bRZ8TQG0xED5mE0Via9PWezMwIoNavsU_DjM HTTP/1.1
    Host: mail.google.com
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: https://www.google.com/a/moxz.mine.nu/acs
    Cookie: S=gmail=UZch6hOEVFj1Y-8w4g93qA; GMAIL_RTT=1063; GMAIL_LOGIN=T1367097141172/1367097141172/1367097200128; SID=DQAAAMUBAACoKZ4UcaFV-lyXqIdorzHbOArd3SMzxlHet0q4NaNgbgSMsh4sawE8rYSJU1xOrmOFHM9ArI0_CCjZEd7T5YLTLtNk5mFJ4jJUhA8bYp12xHrx4B5foOchdyo5vncNTnTniHoH73M8gYAdbvunwRL3kQGcKD7xmGZRAeNu0nnsB_aWM-MS3ftVd8ZG0BzahfstuJDuvCCyzqn3y2euzxNUAeJ3A-yHygcwlng_JiUGfzEyKE_Pvhq5S9aC5hvFhO0Wn5NNGuwdVgc5kPmW6ffAaw9w_tJ5VBbyAs_R5rQw3QoKuuTDDw93pKGGK0eDHOAmrelgBE0w1_8UyLjWQtl6ZQLB6Lp5WaKTpYahKwy_bo_2UxNcrBEDyJhjvvDa6H0Hg5ZvxomllM-aM4glNvfbT4oNiAlbqMuhCRru6qoSXxeWPemOfTGz4tIF9nskF4FLV9SIw8TYJ0oTwoum1g2xphflTJwnLsCsogkiAZKBb8CAZBbZTVkBGlw81gaTle09Y5QAWsYJdQ_GtkmjoAXH9XyXWT-1WvhM1IZJ5Ksb0ezwgpNyNIbq56iApyYo5vSiaczI4__DAYkd1pHo-VgHokNoFRNW6H1vsjiZ5mu18g; HSID=A_hmoPSGe8g9siTJM; SSID=AZHTNvqum9BfiZIuk; APISID=epkxgMmhGOstSn0C/AnAzZCRJDPz1eaz5_; SAPISID=RyzoBwecpP229So7/ADdaqYsMKoejHc1RZ
    Connection: keep-alive

    HTTP/1.1 302 Moved Temporarily
    Cache-Control: no-cache, no-store, max-age=0, must-revalidate
    Content-Length: 0
    Content-Type: text/html; charset=UTF-8
    Date: Sat, 27 Apr 2013 21:39:50 GMT
    Expires: Fri, 01 Jan 1990 00:00:00 GMT
    Location: https://mail.google.com/mail/?shva=1
    Pragma: no-cache
    Server: GSE
    Set-Cookie: GX=DQAAAMYBAAB8ORkGyNU34j6pdtXOnqCj6lmHpvtRVa-aVUYFr8AQXPPS_Hc4sghJ5CA5hXKJY0ydluz1UldO1jryxBZfqTESpRSZ66MjlJZDhnj5B2a21IshnTjyshZs3TLPV_KucK9kLRCZLqea5B90SCPTeDJXqqKhXaq7URorb71qXoz5ESat6JIO0Bz7T35BpuZOlP4R0d7Ebp32IklIGAPT2q8EjLKMYRAAoMsgcvqT3L-NCiU5kovpjmxWC6_QFjlsGwx1b2Hkbn-a00EXe7GnrEqIFeu5DOhQCHnuiVMKeaTSEvKDuYgpyQqtK9v3TZ8S7g8LuulodwGM-tndsY5yPWaopeDBR8AIhQdrwyS3cRM-JQD4R4j2_RW6H_GR5EK_XhKJb0I17Cg1t0GdPT9-G4njMVxPS50nmTJXIl0n0nZpi2cYEXTEfVpcVwy_lxymUUnS2kXa6Qz2jqqqMW4inia5Z7TodRLfOHCb89eRt_0RRlm_9p1xuqKaiwZUovcKOxzUbH05663U0N4G6KBq68NSFUbgUK_46doaHi5IvJhHobDGSYZES3fa_JfjXX9igq_T-nyHiK0-u3VNY9YO8hmIopo5GB9Nih4B1K4WJ4ynCA; Domain=mail.google.com; Path=/mail; Secure; HttpOnly
    Set-Cookie: GMAIL_RTT=EXPIRED; Domain=.google.com; Expires=Fri, 26-Apr-2013 21:39:50 GMT; Path=/; Secure
    Set-Cookie: GMAIL_AT=AF6bupOaXFBvTJxTlJ-nZ713t3pZ5Jz6QQ; Path=/mail; Secure
    X-Content-Type-Options: nosniff
    X-Frame-Options: SAMEORIGIN
    X-XSS-Protection: 1; mode=block
    X-Firefox-Spdy: 3


This is steps 7 and 8 from the diagram. Using Cookies and **RelayState** we are forwarded to the appropriate session. I will try to do an IdP (Identity Provider) Initiated SAML SSO Exchange in another post.

### Related Posts

- [LemonLDAP-NG With LDAP and SAML Google Apps](/2014/02/lemonldap-ng-ldap-saml-google-apps/)

