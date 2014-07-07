---
published: true
title: ProcMail Installation and Configuration Guide
author: Karim Elatov
layout: post
categories: [os]
tags: [linux,procmail,spamassassin]
---

ProcMail stands for Mail Processing, it allows you to process your incoming mail and then sort it into separate folders/file. ProcMail can be used to setup a vacation message or to forward your mail to another email address. All in all, it can be used for many things and I don't even know them all :) I will break this guide into two parts: install and setup.

### Install ProcMail

Download the source from the [following](http://www.procmail.org) URL. You should get a file that looks similar to this **procmail-3.22.tar.gz**. Now let's begin installing. 

	mv procmail-3.22.tar.gz /tmp; cd /tmp  
	tar xzf procmail-3.22.tar.gz; cd procmail-3.22  
	make  
	make BASENAME=/usr/local/procmail install  

### After Install Instructions

	sudo chown 0:0 -R /usr/local/procmail  
	sudo chmod 6755 /usr/local/procmail/bin/procmail  
	sudo chmod 2755 /usr/local/procmail/bin/lockfile  

### Setup Instructions

Any time mail comes to the server, whether the mail server is running **sendmail** or **exim** or any other mail server software, by default most of the mail services look at the **~/.forward** file. If the file exists then mail is either forwarded to the email address that is in the **.forward** file, or the mail server executes whatever is in that file. To use **procmail** we need to add an entry in **.forward** so it is executed whenever any email comes in. So if we place the following into our **~/.forward** file we should be all set.

	"|IFS=' '&&exec /usr/local/procmail/bin/procmail -f-||exit 75 #username"

**note:** replace *username* with your username

### Example to use SpamAssassin with ProcMail

**Spamassassin** is a linux utility which finds spam in mail and adds a header to the email message to mark as spam. Spamassassin is a perl-based application. Using your favorite text editor put the following into your **~/.procmailrc**


	# .procmailrc  
	#  
	DEFAULT=/var/mail/$LOGNAME  
	UMASK=007

	# Look for spam  
	:0fw  
	| /usr/local/perl/bin/spamassassin  
	:0  
	*^X-Spam-Flag:Yes  
	*^Subject: POTENTIAL SPAM:  
	$HOME/mail/spam

	:0:  
	$DEFAULT

Here is what happens, each message is run through the **spamassassin** utility which checks if it is spam. If it's spam it will mark it so by adding the **X-Spam-Flag:Yes** header field and prepend **POTENTIAL SPAM:** to the subject line. So after we run the message through **spamassassin** and  if the above has been set, we can then move the message to the spam folder ... see that was simple, wasn't it ?

### Example to forward messages to your gmail account

Place the following into your **~/.procmailrc**:

	#  
	# .procmailrc  
	#  
	DEFAULT=/var/mail/$LOGNAME  
	UMASK=007

	# Forward all mail to gmail  
	:0c  
	! your_gmail_address@gmail.com

	:0:  
	$DEFAULT
