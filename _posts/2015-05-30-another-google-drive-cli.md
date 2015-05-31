---
published: true
layout: post
title: "Another Google Drive CLI"
author: Karim Elatov
categories: [OS]
tags: [linux,macosx]
---
I started getting an error message using the old **grive** CLI (setup instructions for **grive** can be found [here](/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/):

	grive/libgrive/src/protocol/AuthAgent.cc(174): Throw in function long int gr::AuthAgent::CheckHttpResponse(long int, const string&, const gr::http::Header&)
	Dynamic exception type: boost::exception_detail::clone_impl<gr::http::Error>
	[gr::http::HttpResponseTag*] = 400
	[gr::http::UrlTag*] = https://docs.google.com/feeds/default/private/full/-/folder?max-results=50&showroot=true
	[gr::http::HeaderTag*] = Authorization: Bearer ya29.hAHax8Pg3f6Yvs3dOCUw7_Fds8JF65MFyKQ6-bqwlCgsCO63kCvlPmbi5MzvOhyR8xxmQ2x1fvdfSg
	GData-Version: 3.0

I found the issue on the original project's [git page](https://github.com/Grive/grive/issues/311), and it seems that other people have had luck with another tool called [drive](https://github.com/odeke-em/drive) (instead of **grive**). There is also a fork of the original project call [grive2](https://github.com/vitalif/Grive2), but I wanted to try out **drive**.

### Install drive on Mac OS X or Linux

Most of the instructions are laid out [here](https://github.com/odeke-em/drive/blob/master/platform_packages.md). First let's install **go**:

	$ sudo port install go

Now let's compile the package:

	$ mkdir $HOME/go
	$ export GOPATH=$HOME/go
	$ go get github.com/odeke-em/drive/cmd/drive

After it's done you will see the binary under here:

	$ ls ~/go/bin/
	drive

You can just copy it to any standard location:

	$ sudo cp ~/go/bin/drive /usr/local/bin/.

I followed similar steps on my Gentoo Laptop:

	$ sudo emerge -av go
	$ mkdir go
	$ export GOPATH=$HOME/go
	$ go get github.com/odeke-em/drive/cmd/drive
	$ sudo cp go/bin/drive /usr/local/bin/.

### Sync Google Drive files using *drive* CLI

Most of the instructions are laid out [here](https://github.com/odeke-em/drive/blob/master/platform_packages.md), but first create the directory to which you want to sync to:

	$ mkdir gdrive
	$ cd gdrive
	$ drive init
	Visit this URL to get an authorization code
	https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=352074-7rrlnuanmamgg1i4feed12dpuq871bvd.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive
	Paste the authorization code: 4/KuddZ

Then you can *pull* your data with the following:

	$ drive pull --hidden
	..
	..
	+ /notes/BUILD_NOTES/aips/install.pl
	+ /notes/BUILD_NOTES/aips/aips_war
	+ /notes/BUILD_NOTES/aips/AIPS
	Addition count 837 src: 6.82MB
	Proceed with the changes? [Y/n]:y
	7151948 / 7151948 [=============================================] 100.00 % 2m32

If you don't want the *prompt* you can run the following:

	$ drive pull --hidden --no-prompt

If you've modified a file and you want to *push* your changes you can run the following:

	$ cd gdrive
	$ drive push --hidden

### Drive Usage

There are a bunch of commands, you can list them by just running the following (or check the [git project page](https://github.com/odeke-em/drive)):

	$ drive h
	Usage: drive <command>
	
	where <command> is one of:
	  diff            compares local files with their remote equivalent
	  move            move files/folders
	  trash           moves files to trash
	  unpub           revokes public access to a file
	  init            initializes a directory and authenticates user
	  help            Get help for a topic
	  pub             publishes a file and prints its publicly available url
	  quota           prints out information related to your quota space
	  share           share files with specific emails giving the specified users specifies roles and permissions
	  touch           updates a remote file's modification time to that currently on the server
	  version         0.2.2
	  delete          deletes the items permanently. This operation is irreversible
	  copy            copy remote paths to a destination
	  emptytrash      permanently cleans out your trash
	  list            lists the contents of remote path
	  pull            pulls remote changes from Google Drive
	  push            push local changes to Google Drive
	  stat            display information about a file
	  unshare         revoke a user's access to a file
	  about           print out information about your Google drive
	  cp              copy remote paths to a destination
	  features        returns information about the features of your drive
	  ls              lists the contents of remote path
	  mv              move files/folders
	  rename          renames a file/folder
	  untrash         restores files from trash to their original locations
	
	drive <command> -h for subcommand help

And if you need help on a specific command you can run the following:

	$ drive pull -h
	Usage of drive pull:
	  -exclude-ops="": exclude operations
	  -export="": comma separated list of formats to export your docs + sheets files
	  -export-dir="": directory to place exports
	  -force=false: forces a pull even if no changes present
	  -hidden=false: allows pulling of hidden paths
	  -id=false: pull by id instead of path
	  -ignore-checksum=true: avoids computation of checksums as a final check.
	Use cases may include:
		* when you are low on bandwidth e.g SSHFS.
		* Are on a low power device
	  -ignore-conflict=false: turns off the conflict resolution safety
	  -ignore-name-clashes=false: ignore name clashes
	  -matches=false: search by prefix
	  -no-clobber=false: prevents overwriting of old content
	  -no-prompt=false: shows no prompt before applying the pull action
	  -piped=false: if true, read content from stdin
	  -quiet=false: if set, do not log anything but errors
	  -r=true: performs the pull action recursively
	  
I like the **quota** flag:

	$ drive quota
	Name: Blah
	Account type:	LIMITED
	Bytes Used:	10117676             (9.65MB)
	Bytes Free:	16096009684          (14.99GB)
	Bytes InTrash:	0                    (0.00B)
	Total Bytes:	16106127360          (15.00GB)
	
	* Space used by Google Services *
	Service                              Bytes
	DRIVE                                9.61MB
	GMAIL                                15.89MB
	PHOTOS                               5.87MB
	Space used by all Google Apps        31.41MB

I also like how you can download specific files:

	$ drive pull photos/img001.png docs

