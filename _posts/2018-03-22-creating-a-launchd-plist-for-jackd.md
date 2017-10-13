---
published: false
layout: post
title: "Creating a Launchd Plist for jackd"
author: Karim Elatov
categories: [os]
tags: [launchd,launchctl,homebrew,jackd]
---
### Moc with Homebrew
When you install **moc** with **homebrew** (`brew install moc`) you will see the following message:

	To have launchd start jack now and restart at login:
	   brew services start jack
	Or, if you don't want/need a background service you can just run:
	   jackd -d coreaudio

I had installed the [homebrew-services](https://github.com/Homebrew/homebrew-services) *tap* and that integrates certain packages with *launchd*. 

### Launchd Logging
I ran the suggested command:

	<> brew services start jack
	==> Successfully started `jack` (label: homebrew.mxcl.jack)

But it wasn't actually running:

	<> ps -ef | grep jack
	1000 11364 10834   0  5:24PM ttys007    0:00.00 grep --color=auto jack

In the logs I just saw this:

	<> tail -f /var/log/system.log
	Oct  8 11:04:45 macair com.apple.xpc.launchd[1] (homebrew.mxcl.jack): This service is defined to be constantly running and is inherently inefficient.
	Oct  8 11:04:45 macair com.apple.xpc.launchd[1] (homebrew.mxcl.jack): Service only ran for 0 seconds. Pushing respawn out by 10 seconds.
	Oct  8 11:04:55 macair com.apple.xpc.launchd[1] (homebrew.mxcl.jack): Service only ran for 0 seconds. Pushing respawn out by 10 seconds.
	Oct  8 11:05:05 macair com.apple.xpc.launchd[1] (homebrew.mxcl.jack): Service only ran for 0 seconds. Pushing respawn out by 10 seconds.

It wasn't very helpful. I then ran into [MOC on OS X](https://gist.github.com/RobertAudi/6045338) which had the manual steps on how to create the service. So I removed the one from the **homebrew**:

	<> brew services stop jack
	Stopping `jack`... (might take a while)
	==> Successfully stopped `jack` (label: homebrew.mxcl.jack)

And started troubleshooting it manually. First I ran into [Logging with Launchd](http://erikslab.com/2011/02/04/logging-with-launchd/) and that had instructions on how to add some logging outputs. So with that information, I created the following **plist**:

	<> cat Library/LaunchAgents/org.jackaudio.jackd.plist
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
	  <key>EnvironmentVariables</key>
	  <key>Label</key>
	  <string>org.jackaudio.jackd</string>
	  <key>WorkingDirectory</key>
	  <string>/usr/local/Cellar/jack/0.125.0_1</string>
	  <key>ProgramArguments</key>
	  <array>
	    <string>/usr/local/bin/jackd</string>
	    <string>-v</string>
	    <string>-d</string>
	    <string>coreaudio</string>
	  </array>
	  <key>StandardOutPath</key>
	  <string>/usr/local/var/log/jackd.log</string>
	  <key>StandardErrorPath</key>
	  <string>/usr/local/var/log/jackd-error.log</string>
	  <key>RunAtLoad</key>
	  <true/>
	  <key>KeepAlive</key>
	  <true/>
	</dict>
	</plist>

I also added **-v** arguement to the **jackd** command to see more information. Then I loaded the script:

	<> launchctl load -w ~/Library/LaunchAgents/org.jackaudio.jackd.plist

And in the logs I saw the following:

	<> tail /usr/local/var/log/jackd.log
	jackd 0.125.0
	Copyright 2001-2009 Paul Davis, Stephane Letz, Jack O'Quinn, Torben Hohn and others.
	jackd comes with ABSOLUTELY NO WARRANTY
	This is free software, and you are welcome to redistribute it
	under certain conditions; see the file COPYING for details
	
	getting driver descriptor from /usr/local/Cellar/jack/0.125.0_1/lib/jack/jack_dummy.so
	getting driver descriptor from /usr/local/Cellar/jack/0.125.0_1/lib/jack/jack_coreaudio.so
	getting driver descriptor from /usr/local/Cellar/jack/0.125.0_1/lib/jack/jack_net.so
	JACK compiled with POSIX SHM support.
	registered builtin port type 32 bit float mono audio
	registered builtin port type 8 bit raw midi

And this:

    <> tail /usr/local/var/log/jackd-error.log
    Unable to get tmpdir in user dir
    Unable to get tmpdir in engine
    cannot create server sockets
    cannot create engine

And also this:

	<> tail -f /var/log/system.log
	Oct  8 17:04:13 macair com.apple.xpc.launchd[1] (org.jackaudio.jackd[9491]): Service could not initialize: 17A: xpcproxy + 11572 [1522][43FABD]: 0x2
	Oct  8 17:04:13 macair com.apple.xpc.launchd[1] (org.jackaudio.jackd): Service only ran for 0 seconds. Pushing respawn out by 10 seconds.

### Environment Variables with Launchd

Then I ran into [PATCH: use a fixed jackd path for tmpdir query](http://jack-audio.10948.n7.nabble.com/PATCH-use-a-fixed-jackd-path-for-tmpdir-query-td15160.html), and from that page, it seems that the **PATH** variable wasn't set right and **jackd** couldn't be found to run `jackd -l`, which shows where the **tmp** directory is:

	<> /usr/local/bin/jackd -l
	/tmp

So then I ran into [Use an environment variable in a launchd script](https://serverfault.com/questions/111391/use-an-environment-variable-in-a-launchd-script) and there was an example on how to set environment variables in **launchd** **plist** files. So after that I created the following **plist**:

	<> cat Library/LaunchAgents/org.jackaudio.jackd.plist
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
	  <key>EnvironmentVariables</key>
	  <dict>
	         <key>TMPDIR</key>
	         <string>/tmp</string>
	         <key>PATH</key>
	         <string>/usr/local/bin</string>
	  </dict>
	  <key>Label</key>
	  <string>org.jackaudio.jackd</string>
	  <key>WorkingDirectory</key>
	  <string>/usr/local/Cellar/jack/0.125.0_1</string>
	  <key>ProgramArguments</key>
	  <array>
	    <string>/usr/local/bin/jackd</string>
	    <string>-d</string>
	    <string>coreaudio</string>
	  </array>
	  <key>StandardOutPath</key>
	  <string>/usr/local/var/log/jackd.log</string>
	  <key>StandardErrorPath</key>
	  <string>/usr/local/var/log/jackd-error.log</string>
	  <key>RunAtLoad</key>
	  <true/>
	  <key>KeepAlive</key>
	  <true/>
	</dict>
	</plist>

Then I reloaded the script:

	<> launchctl unload -w ~/Library/LaunchAgents/org.jackaudio.jackd.plist
	<> launchctl load -w ~/Library/LaunchAgents/org.jackaudio.jackd.plist

And then **jackd** was running:

	<> ps -ef | grep jack
	1000 10763     1   0  5:15PM ??         0:27.48 /usr/local/bin/jackd -d coreaudio
	1000 11717  4885   0  5:39PM ttys003    0:00.00 grep --color=auto jack

You can confirm the *environment* variables set for a **launchd** script by running the following:

	<> launchctl print gui/1000/org.jackaudio.jackd
	org.jackaudio.jackd = {
	    active count = 3
	    path = /Users/elatov/Library/LaunchAgents/org.jackaudio.jackd.plist
	    state = running
	
	    program = /usr/local/bin/jackd
	    arguments = {
	            /usr/local/bin/jackd
	            -d
	            coreaudio
	    }
	
	    working directory = /usr/local/Cellar/jack/0.125.0_1
	
	    stdout path = /usr/local/var/log/jackd.log
	    stderr path = /usr/local/var/log/jackd-error.log
	    inherited environment = {
	            Apple_PubSub_Socket_Render => /private/tmp/com.apple.launchd.lIHQklt3qF/Render
	            SSH_AUTH_SOCK => /private/tmp/com.apple.launchd.VL11NowySr/Listeners
	    }
	
	    default environment = {
	            PATH => /usr/bin:/bin:/usr/sbin:/sbin
	    }
	
	    environment = {
	            PATH => /usr/local/bin
	            TMPDIR => /tmp
	            XPC_SERVICE_NAME => org.jackaudio.jackd
	    }

I left the logging on just in case I will need to troubleshoot later, and after it was working I just saw this in the logs:

	<> tail /usr/local/var/log/jackd-error.log
	server `default' registered
	Error calling AudioUnitSetProperty - kAudioUnitProperty_StreamFormat kAudioUnitScope_Output
	poll failed (Bad file descriptor)
	cleaning up shared memory
	cleaning up files
	unregistering server `default'
	Error calling AudioUnitSetProperty - kAudioUnitProperty_StreamFormat kAudioUnitScope_Output

Which is what I would see when I would run the command manually in my terminal.
