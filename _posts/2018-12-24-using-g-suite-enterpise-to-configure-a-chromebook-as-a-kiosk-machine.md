---
published: true
layout: post
title: "Using G-Suite Enterpise to Configure a Chromebook as a Kiosk Machine"
author: Karim Elatov
categories: [os]
tags: [chromebook, g-suite]
---
## G-Suite Enteprise Chrome Management
With G-Suite Enterprise you can turn a Chromebook into a kiosk machine. You can sign up for a trial (more information at [About your free G Suite trial](https://support.google.com/a/answer/6388094?hl=en)). After you signed up, login to the admin console  (**admin.google.com**) and you will see all the settings available for your organization:

![gsuite-admin-console.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/gsuite-admin-console.png)

If you go to **Device Management**, you will see already registered devices and more options:

![gs-dev-mgmt.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/gs-dev-mgmt.png)

You can also click on **Chrome Management** and configure the chrome browser settings at multiple levels.

### Creating a Publish Session
To start off, I modified the **Public Session Settings** and blocked some URLs:

![gs-pub-sess-sets.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/gs-pub-sess-sets.png)

Next, under the **Device Settings**, I pointed to my public session that I created before:

![gs-dev-mgmt-kiosk.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/gs-dev-mgmt-kiosk.png)

### Enrolling your Chromebook
Now on a brand new chromebook, you can follow [Enroll Chrome devices](https://support.google.com/chrome/a/answer/1360534?hl=en) instructions to enroll the device. Initially the login screen looks like this:

![chromebook-default-login.jpg](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chromebook-default-login.jpg)

Then after clicking **Ctrl-Alt-E**, you will see the Enterprise login:

![chromebook-ent-login-page.jpg](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chromebook-ent-login-page.jpg)

Also if the chromebook had initially been entrolled to g-suite enterprise and the **Force Re-Enroll** Option is enabled, then right after booting up the chromebook you will see the Enterprise Enrollment Login with the domain specified:

![chromebook-with-force-re-nroll.jpg](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chromebook-with-force-re-nroll.jpg)

After a successful enrollment it will automatically start to login into the Public Session:

![kiosk-mode-logging-in.jpg](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/kiosk-mode-logging-in.jpg)

At which point you will see the following screen (Notice it will have an **Exit Session** on the bottom right:

![chromeos-pubsession-logged-in.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chromeos-pubsession-logged-in.png)

### Confirm Chromebook is Enrolled into Enterprise Management
To confirm all the policies have been pushed to the device, you can point the chrome browser to **chrome://policy** and you will see all the settings:

![chromebook-chrome-policy-enrolled.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chromebook-chrome-policy-enrolled.png)

You can also scroll down and check out the **URLBlacklist** policy:

![chrome-policy-set.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chrome-policy-set.png)

You can also try to visit a blocked url and you will see the following:

![chrome-gmail-blocked.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chrome-gmail-blocked.png)

If you go back to the Admin Console, under **Device Management** -> **Chrome Device** -> Your Device -> **System Activity and Troubleshooting**, you can see the status of the device. You can also grab logs and reboot it (pretty handy):

![dev-troubleshoot-info.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/dev-troubleshoot-info.png)

### Pushing SSL Certs to Chromebook
You can also push certificates to the chrome devices (most of the instructions are at [Set up SSL inspection on Chrome devices](https://support.google.com/chrome/a/answer/3505249?hl=en)). This can come in handy, if you are using a Proxy to perform URL filtering. Under **Device management** -> **Network** -> **Certificates** you can import your Proxy CA cert:

![gs-ssl-certs.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/gs-ssl-certs.png)

And if the device is on a trusted network it will push the cert to it.

## User Sessions With Chrome Management
On top of device management, you can also configure **User Session** settings. These are settings that are pushed to the chrome browser when a user logs to chrome on any device. So on any browser click on the login button for your profile:

![sign-to-chrome.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/sign-to-chrome.png)

And then login to your managed domain:

![sign-to-enterpise-for-chrome.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/sign-to-enterpise-for-chrome.png)

And then you can create a brand new profile:

![chrome-new-profile.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chrome-new-profile.png)

And you can confirm that chrome instance is managed by an g-suite enterprise, by checking out **chrome://policy**:

![chrome-policy-browser.png](https://raw.githubusercontent.com/elatov/upload/master/gsuite-kiosk/chrome-policy-browser.png)

Same thing happens here, any browser setting that you modified in the **User Session** settings will be pushed to this chrome browser.

## Resetting Chromebook to Factory Settings

If you get stuck an any point you can reset the chromebook to factory settings by following the instructions laid out in [Reset your Chromebook to factory settings](https://support.google.com/chromebook/answer/183084?hl=en&ref_topic=3418733) or in [Wipe device data](https://support.google.com/chrome/a/answer/1360642)
