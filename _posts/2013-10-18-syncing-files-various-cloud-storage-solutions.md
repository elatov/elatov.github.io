---
title: Syncing Files with Various Cloud Storage Solutions
author: Karim Elatov
layout: post
permalink: /2013/10/syncing-files-various-cloud-storage-solutions/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1873080541
categories:
  - Home Lab
  - OS
tags:
  - cloud storage
  - seacloud
  - seafile
---
A while ago I wrote <a href="http://virtuallyhyper.com/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/']);">this</a> post on how to use Grive. Grive is a cross platform/architecture client that allowed me to sync files with Google Drive. I really liked the setup, but now I wanted another cloud storage solution, where I could store the not-so-important files and not take up space on my google drive account.

### Desired Cloud Storage Capabilities

I had a couple of criteria that the cloud storage solution had to support:

1.  I could manage the files with a cli (some people called this headless). Whether this was done with the API or something else, it didn&#8217;t really matter to me
2.  It could be used cross platform and architecture. So I wanted to be able to use it on a Mac, Windows, Linux, and Android. For Linux, I wanted to be able to use it on x86, powerpc, ARM or whatever architecture.

### SkyDrive

I haven&#8217;t used **skydrive** before, so I wanted to give it a try. First, what is *skydrive*? from wikipedia:

> SkyDrive (officially Microsoft SkyDrive, previously Windows Live SkyDrive and Windows Live Folders) is a file hosting service that allows users to upload and sync files to a cloud storage and then access them from a Web browser or their local device.

So it&#8217;s Microsoft&#8217;s version of a cloud storage solution. There is a pretty good comparison page from a Microsoft, comparing SkyDrive, iCloud, Google Drive, and DropBox. Here is quick snippet from the <a href="http://windows.microsoft.com/en-us/skydrive/compare" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://windows.microsoft.com/en-us/skydrive/compare']);">page</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/SkyDrive_Comparison.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/SkyDrive_Comparison.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/SkyDrive_Comparison.png" alt="SkyDrive Comparison Syncing Files with Various Cloud Storage Solutions" width="1027" height="357" class="alignnone size-full wp-image-9662" title="Syncing Files with Various Cloud Storage Solutions" /></a>

You can register for the free 7GB SkyDrive account <a href="https://skydrive.live.com" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://skydrive.live.com']);">here</a> . After the registration is finished you can login and see your account:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive-logged-in.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive-logged-in.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive-logged-in.png" alt="skydrive logged in Syncing Files with Various Cloud Storage Solutions" width="452" height="238" class="alignnone size-full wp-image-9663" title="Syncing Files with Various Cloud Storage Solutions" /></a>

There is a python client available for SkyDrive that uses the SkyDrive API. It&#8217;s called **python-skydrive**, here is a link to the <a href="https://pypi.python.org/pypi/python-skydrive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pypi.python.org/pypi/python-skydrive/']);" class="broken_link">client</a>.

#### Python-Skydrive

To use the **python-skypdrive** client, you have to register the SkyDrive application with the &#8220;Live Connect Developer Center&#8221;. First visit the Dev Center, <a href="http://msdn.microsoft.com/en-us/live/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://msdn.microsoft.com/en-us/live/']);">here</a>. Login with the same credentials that you created when you registered for SkyDrive and you should be inside the Dev Center:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_connect_dev_center.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_connect_dev_center.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_connect_dev_center.png" alt="Live connect dev center Syncing Files with Various Cloud Storage Solutions" width="1041" height="396" class="alignnone size-full wp-image-9664" title="Syncing Files with Various Cloud Storage Solutions" /></a>

Click on &#8220;**My Apps**&#8221; and then click on &#8220;**Create Application**&#8220;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_dev_center_my_apps.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_dev_center_my_apps.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/Live_dev_center_my_apps.png" alt="Live dev center my apps Syncing Files with Various Cloud Storage Solutions" width="677" height="330" class="alignnone size-full wp-image-9665" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After clicking &#8220;**Create Application**&#8221; you can call it whatever you want. Then after clicking **Next** it will show your *client ID* and the *client secret*:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive_Api_rgistered_i.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive_Api_rgistered_i.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/skydrive_Api_rgistered_i.png" alt="skydrive Api rgistered i Syncing Files with Various Cloud Storage Solutions" width="999" height="579" class="alignnone size-full wp-image-9666" title="Syncing Files with Various Cloud Storage Solutions" /></a>

Make sure to set **Mobile Client App** to **yes** and then click **Save**. Add both the *Client ID* and *Secret* to your **.lcrc** file:

    $ cat ~/.lcrc
    client:
      id: 0000620A3E4A
      secret: gndrjIOLWYLkOPl0QhW
    

I was actually using my Mac, so I ended using **Mac-Ports** to do the install. First I checked which version of python I have installed:

    kelatov@kmac:~$port list installed | grep python
    python27                       @2.7.5          lang/python27
    python27                       @2.7.5          lang/python27
    python32                       @3.2.5          lang/python32
    python_select                  @0.3            sysutils/python_select
    

The application supported *python2.7*, so let&#8217;s install **pip** for that:

    kelatov@kmac:~$sudo port install py27-pip
    

Now using **pip**, let&#8217;s install the SkyDrive client:

    kelatov@kmac:~$sudo pip-2.7 install 'python-skydrive[standalone]'
    Downloading/unpacking python-skydrive[standalone]
      Downloading python-skydrive-13.08.2.tar.gz
      Running setup.py egg_info for package python-skydrive
    
      Installing extra requirements: 'standalone'
    Downloading/unpacking requests (from python-skydrive[standalone])
      Downloading requests-2.0.0.tar.gz (362kB): 362kB downloaded
      Running setup.py egg_info for package requests
    
    Installing collected packages: python-skydrive, requests
      Running setup.py install for python-skydrive
    
        Installing skydrive-cli script to /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin
      Running setup.py install for requests
    
    Successfully installed python-skydrive requests
    Cleaning up...
    

It looks like I need **python-yaml** to do the authentication, so I installed that as well:

    $ sudo port install py27-yaml
    

The **skydrive-cli** script was placed in a weird location:

    kelatov@kmac:~$find /opt/local -name skydrive-cli /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/skydrive-cli 
    

So I went ahead and added a symbolic link under **/opt/local/bin**:

    kelatov@kmac:~$sudo ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/skydrive-cli /opt/local/bin/skydrive-cli
    

Now it&#8217;s time to authorize our client to be able to access SkyDrive. Here is the command for that:

    kelatov@kmac:~$skydrive-cli auth
    Visit the following URL in any web browser (firefox, chrome, safari, etc),
      authorize there, confirm access permissions, and paste URL of an empty page
      (starting with "https://login.live.com/oauth20_desktop.srf") you will get redirected to in the end.
    Alternatively, use the returned (after redirects) URL with "/opt/local/bin/skydrive-cli auth <URL>" command.
    
    URL to visit: https://login.live.com/oauth20_authorize.srf?scope=wl.skydrive+wl.skydrive_update+wl.offline_access&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=code&client_id=790E
    
    URL after last redirect: https://login.live.com/oauth20_desktop.srf?code=c0c
    API authorization was completed successfully.
    

So first it provides you with a URL to visit and after you allow access, it will throw to a URL with a blank page. You can then copy that URL and paste it in to the command and it will be authorized. At this point you will be able to check the contents of your SkyDrive with the cli:

    kelatov@kmac:~$skydrive-cli tree
    SkyDrive:
      Documents:
      Pictures:
      Public:
    

After I started using the cli, I realized it was like an FTP client for SkyDrive. Here are the available actions:

    Supported operations:
      {auth,quota,recent,info,info_set,link,ls,mkdir,get,put,cp,mv,rm,comments,comment_add,comment_delete,tree}
        auth                Perform user authentication.
        quota               Print quota information.
        recent              List recently changed objects.
        info                Display object metadata.
        info_set            Manipulate object metadata.
        link                Get a link to a file.
        ls                  List folder contents.
        mkdir               Create a folder.
        get                 Download file contents.
        put                 Upload a file.
        cp                  Copy file to a folder.
        mv                  Move file to a folder.
        rm                  Remove object (file or folder).
        comments            Show comments for a file, object or folder.
        comment_add         Add comment for a file, object or folder.
        comment_delete      Delete comment from a file, object or folder.
        tree                Show contents of skydrive (or folder) as a tree of
                            file/folder names. Note that this operation will have
                            to (separately) request a listing of every folder
                            under the specified one, so can be quite slow for
                            large number of these.
    

You can&#8217;t even **put** a directory into SkyDrive, so I would have to write another script to basically recursively put files from a directory. There was also no sync functionality, like with **grive**. I think the client is great and I am sure it will get better with future releases.

### DropBox

At this point I wanted to try the most popular cloud storage solution out there: DropBox. I first installed it on my Mac. The install was pretty straight forward, just download it and launch it, at which point it will ask you to login to dropbox:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_installer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_installer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_installer.png" alt="dropbox installer Syncing Files with Various Cloud Storage Solutions" width="571" height="512" class="alignnone size-full wp-image-9667" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After the install is done, you will see the dropbox status in your notification area:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_notificateion.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_notificateion.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/dropbox_notificateion.png" alt="dropbox notificateion Syncing Files with Various Cloud Storage Solutions" width="48" height="22" class="alignnone size-full wp-image-9668" title="Syncing Files with Various Cloud Storage Solutions" /></a>

That was just for the Mac. I then read up on how to setup dropbox on a headless linux server:

*   <a href="http://www.dropboxwiki.com/tips-and-tricks/install-dropbox-in-an-entirely-text-based-linux-environment" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.dropboxwiki.com/tips-and-tricks/install-dropbox-in-an-entirely-text-based-linux-environment']);">Install Dropbox In An Entirely Text-Based Linux Environment</a>
*   <a href="http://confluence.jc21.com/display/LINUX/Using+Dropbox+on+Linux+headless+server" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://confluence.jc21.com/display/LINUX/Using+Dropbox+on+Linux+headless+server']);">Using Dropbox on Linux headless server</a>
*   <a href="http://ubuntuforums.org/showthread.php?t=1416686" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://ubuntuforums.org/showthread.php?t=1416686']);">How to install headless dropbox (with no GUI frontend) on ubuntu</a>

All the installs provide an already compiled binary for either x86 or x86_64 architectures but nothing else. I then ran into a couple of CLIs for dropbox:

*   <a href="http://www.dropboxwiki.com/tips-and-tricks/using-the-official-dropbox-command-line-interface-cli" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.dropboxwiki.com/tips-and-tricks/using-the-official-dropbox-command-line-interface-cli']);">Using the Official Dropbox Command Line Interface (CLI)</a> 
*   <a href="http://www.dropboxwiki.com/dropbox-addons/dropbox-linux-cli" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.dropboxwiki.com/dropbox-addons/dropbox-linux-cli']);">Dropbox Linux CLI</a>

But they were just CLIs that depended on **dropboxd** to be already running (which was only provided for x86 and x86_64 architectures). There is a *nautilus-plugin*, which can be compiled (the source can be found <a href="https://www.dropbox.com/help/247/en" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.dropbox.com/help/247/en']);">here</a>), but same thing, it depends on **dropboxd**. There is forum about the lack of support for the ARM architecture <a href="http://www.raspberrypi.org/phpBB3/viewtopic.php?f=63&t=7391" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.raspberrypi.org/phpBB3/viewtopic.php?f=63&t=7391']);">here</a>.

I finally ran into **dropboxuploader.sh**. Here are a couple of guides on using that:

*   <a href="https://github.com/andreafabrizi/Dropbox-Uploader" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/andreafabrizi/Dropbox-Uploader']);">Dropbox Uploader</a> 
*   <a href="http://www.webupd8.org/2013/01/dropbox-uploader-bash-script-useful-for.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.webupd8.org/2013/01/dropbox-uploader-bash-script-useful-for.html']);">DropBox Uploader Bash Script: Useful for Servers, Raspberry PI, and More</a> 
*   <a href="http://www.jobnix.in/dropbox-command-line-interface-cli-client/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.jobnix.in/dropbox-command-line-interface-cli-client/']);">Dropbox Command Line Interface [ CLI ] client</a>

The script was really good, but it also felt like an FTP client for DropBox. Here are the available actions:

    upload [LOCAL_FILE/DIR] <REMOTE_FILE/DIR>
    download [REMOTE_FILE/DIR] <LOCAL_FILE/DIR>
    delete [REMOTE_FILE/DIR]
    move [REMOTE_FILE/DIR] [REMOTE_FILE/DIR]
    copy [REMOTE_FILE/DIR] [REMOTE_FILE/DIR]
    mkdir [REMOTE_DIR]
    list <REMOTE_DIR>
    share [REMOTE_FILE]
    info
    unlink
    -f [FILENAME] Load the configuration file from a specific file
    -s Skip already existing files when download/upload. Default: Overwrite
    -d Enable DEBUG mode
    -q Quiet mode. Don't show progress meter or messages
    -p Show cURL progress meter
    -k Doesn't check for SSL certificates (insecure)
    

This script was better than the SkyDrive one (**skydrive-cli**), since it allowed for uploads of directories and it could skip existing files, but there was still no sync functionality (so if I had updated a text file, it wouldn&#8217;t upload it since it already existed).

### Box

Everyone knows the popular alternative to *DropBox* is *Box*. The install on my Mac was similar to the DropBox install. You just launch the installer and it took care of the rest. The cool thing with Box is that you can access your files via **WebDav**. I ran into some pages that utilized WebDav with Box:

*   <a href="http://seb.so/50gb-of-cloud-space-with-box-automatically-syncd-on-linux-with-webdav/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://seb.so/50gb-of-cloud-space-with-box-automatically-syncd-on-linux-with-webdav/']);">50gb of “cloud” space with Box, automatically sync’d on Ubuntu/Linux with webdav and unison</a>

It had a pretty cool setup, but I later ran into:

*   <a href="https://github.com/noiselabs/box-linux-sync" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/noiselabs/box-linux-sync']);">box-linux-sync &#8211; A naïve Box.com Linux Client</a>

The setup seems reasonable, so I gave it a try. Here is what I did to sync files with Box with **WebDav** on my Debian box. First let&#8217;s install **davfs**:

    $ sudo apt-get install davfs2
    

In order for regular users to be able to mount **davfs**, they need to be part of the **davfs2** group. Here is the command to add myself to that group:

    $ sudo usermod -a -G davfs2 elatov
    

Then I installed some python prerequisites, so we can use the **box-sync** client:

    $ sudo apt-get install python-pkg-resources
    

Now let&#8217;s install the **box-sync** client:

    $ git clone git://github.com/noiselabs/box-linux-sync.git
    $ sudo mv box-linux-sync /usr/local/.
    $ sudo chown elatov:elatov /usr/local/box-linux-sync/
    $ sudo ln -s /usr/local/box-linux-sync/bin/box-sync /usr/local/bin/box-sync
    

Now let&#8217;s check to make sure the client is ready for setup:

    $box-sync check
    Created configuration file '/home/elatov/.noiselabs/box/box-sync.cfg'
    Created example configuration file '/home/elatov/.noiselabs/box/box-sync.cfg.sample'
    * Checking davfs installation...
    * Congratulations. Your Davfs install is OK ;)
    

That looks good, now let&#8217;s run the setup:

    $ box-sync setup
    * Setting up davfs...
    * Created sync directory at '/home/elatov/Box'
    *  Created a personal davfs2 directory at '/home/elatov/.davfs2'
    *  Created a personal cache directory at '/home/elatov/.davfs2/cache'
    * Created a new secrets file in '/home/elatov/.davfs2/secrets'
    * Installed a new davfs config file in '/home/elatov/.davfs2/davfs2.conf'
    * Credentials are missing from /home/elatov/.davfs2/secrets. Please add them:
      $ echo "https://www.box.com/dav MYEMAIL MYPASSWORD" >> /home/elatov/.davfs2/secrets
    
    * Box mount point is missing. Please add this line to your /etc/fstab:
      $ sudo sh -c 'echo "https://www.box.com/dav /home/elatov/Box davfs rw,user,noauto 0 0" >> /etc/fstab'
    
    * '/home/elatov/.davfs2/davfs2.conf' looks good ;)
    

Now let&#8217;s add the credentials to the **~/.davfs2/secrets** file:

    $ echo "https://www.box.com/dav MYEMAIL MYPASSWORD" >> ~/.davfs2/secrets
    

and also let&#8217;s add the mount point to our **/etc/fstab** file:

    $ sudo sh -c 'echo "https://www.box.com/dav /home/elatov/.box davfs rw,users,noauto 0 0" >> /etc/fstab'
    

**Note:** I added the *users* parameter to the **fstab** entry, this will allow regular users to un-mount that volume as well.

Next I changed my default folder to be **.box**, this is done by editing the **~/.noiselabs/box/box-sync.cfg** file and modifying the following line:

    box_dir = .box
    

Now let&#8217;s create the mount point:

    $ mkdir .box
    

and lastly allow regular users to use the **davfs** mount utility, this is done by running the following:

    $ sudo chmod  u+s /usr/sbin/mount.davfs
    

Now to actually access our Box files via **webdav**:

    $ box-sync start
    

To make sure it&#8217;s mounted, you can run the following:

    $ /bin/df -h -t fuse
    Filesystem               Size  Used Avail Use% Mounted on
    https://www.box.com/dav   26G   13G   13G  50% /home/elatov/.box
    

Now you can use **rsync**, or even **unison** (described in the above guide) to keep your files synced up. To un-mount the volume just run the following:

    $ box-sync stop
    

The setup was pretty good, but **davfs** was a little slow. Some times I would run **ls** on the volume and if the directory had over 10 files, it would take a while to display the files. I also didn&#8217;t like the idea of modifying my **/etc/fstab** to get this running. I was still stuck on the simplicity of the **grive** client for google drive.

### Storage Made Easy (SME)

In my efforts to speed up Davfs with Box, I ran into Storage Made Easy (SME). From their FAQ, here is what they do:

> What exactly does Storage Made Easy do?  
> Storage Made Easy Provide a Cloud File Server that can be used by individuals or teams and that unifies information from different file stores and SaaS services to make them easier to access, search, and manage. Over 40 different file clouds and services are supported and unlike other vendors no files need to be moved, copied or replaced to provide this service.

So SME is basically a broker for all different cloud solutions and they just keep metadata of all the files and don&#8217;t actually store the data. They support a bunch of cloud solutions, from their <a href="http://storagemadeeasy.com/cloud_list/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://storagemadeeasy.com/cloud_list/']);">cloud list</a>, here is their supported list:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_cloud_list.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_cloud_list.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_cloud_list.png" alt="sme cloud list Syncing Files with Various Cloud Storage Solutions" width="449" height="621" class="alignnone size-full wp-image-9669" title="Syncing Files with Various Cloud Storage Solutions" /></a>

You can see that SkyDrive, Dropbox, and Box are all supported and a lot of other ones are supported as well. Surprisingly the Ubuntu Client actually worked on my Chromebox (ARM Based). I downloaded the client from <a href="http://storagemadeeasy.com/LinuxDrive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://storagemadeeasy.com/LinuxDrive/']);">here</a>. The install went okay, first install the **deb** package:

    $ sudo dpkg -i storagemadeeasy_4.0.7.deb
    Selecting previously unselected package storagemadeeasy.
    (Reading database ... 167023 files and directories currently installed.)
    Unpacking storagemadeeasy (from storagemadeeasy_4.0.7.deb) ...
    dpkg: dependency problems prevent configuration of storagemadeeasy:
     storagemadeeasy depends on libqt4-core (>= 4.3); however:
      Package libqt4-core is not installed.
     storagemadeeasy depends on fuse-utils; however:
      Package fuse-utils is not installed.
     storagemadeeasy depends on libfuse-perl; however:
      Package libfuse-perl is not installed.
     storagemadeeasy depends on libfilesys-statvfs-perl; however:
      Package libfilesys-statvfs-perl is not installed.
     storagemadeeasy depends on liblchown-perl; however:
      Package liblchown-perl is not installed.
     storagemadeeasy depends on libfuse-dev; however:
      Package libfuse-dev is not installed.
     storagemadeeasy depends on libqt4-gui; however:
      Package libqt4-gui is not installed.
    
    dpkg: error processing storagemadeeasy (--install):
     dependency problems - leaving unconfigured
    Processing triggers for bamfdaemon ...
    Rebuilding /usr/share/applications/bamf-2.index...
    Processing triggers for desktop-file-utils ...
    Processing triggers for gnome-menus ...
    Errors were encountered while processing:
     storagemadeeasy
    

Then to install the missing dependencies, just run the following:

    $ sudo apt-get install -f
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    Correcting dependencies... Done
    The following extra packages will be installed:
      fuse-utils libfilesys-statvfs-perl libfuse-dev libfuse-perl liblchown-perl
      libqt4-core libqt4-gui libselinux1-dev libsepol1-dev
    Suggested packages:
      libunix-mknod-perl
    The following NEW packages will be installed:
      fuse-utils libfilesys-statvfs-perl libfuse-dev libfuse-perl liblchown-perl
      libqt4-core libqt4-gui libselinux1-dev libsepol1-dev
    0 upgraded, 9 newly installed, 0 to remove and 2 not upgraded.
    1 not fully installed or removed.
    Need to get 0 B/496 kB of archives.
    After this operation, 1,949 kB of additional disk space will be used.
    Do you want to continue [Y/n]? 
    

After it&#8217;s installed you can launch the GUI to configure the cloud providers. So from the terminal run:

    $ smeexplorer
    

and it will ask you to authenticate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_explorer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_explorer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_explorer.png" alt="sme explorer Syncing Files with Various Cloud Storage Solutions" width="472" height="312" class="alignnone size-full wp-image-9675" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After your are authenticated, you can add a storage provider. For example I added **box.net**:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_add_cloud_provider.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_add_cloud_provider.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme_add_cloud_provider.png" alt="sme add cloud provider Syncing Files with Various Cloud Storage Solutions" width="833" height="413" class="alignnone size-full wp-image-9676" title="Syncing Files with Various Cloud Storage Solutions" /></a>

Then you can launch the sync center:

    $ smesynccenter
    

You will have to authenticate again and you can define the sync schedule. For example I asked it to sync every 5 minutes:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme-sync-center-5min.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/sme-sync-center-5min.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/sme-sync-center-5min.png" alt="sme sync center 5min Syncing Files with Various Cloud Storage Solutions" width="695" height="657" class="alignnone size-full wp-image-9677" title="Syncing Files with Various Cloud Storage Solutions" /></a>

and then you can link a local folder to a remote folder from any of the providers that you have added. Here I am syncing my local **pic** folder to the **Box.net** provider:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/link_folder-sme.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/link_folder-sme.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/link_folder-sme.png" alt="link folder sme Syncing Files with Various Cloud Storage Solutions" width="560" height="350" class="alignnone size-full wp-image-9678" title="Syncing Files with Various Cloud Storage Solutions" /></a>

You can also mount all the providers with the **smeclient**. Run it with the following command:

    $ smeclient
    

and then choose a mount point and enter your credentials and it will mount it for you:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/smeclient_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/smeclient_1.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/smeclient_1.png" alt="smeclient 1 Syncing Files with Various Cloud Storage Solutions" width="390" height="367" class="alignnone size-full wp-image-9679" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After it&#8217;s done you will see the mount point:

    $df -h -t fuse
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/fuse       4.0T     0  4.0T   0% /home/elatov/.sme
    

It was actually much faster than the **DavFS** mountpoint, but there was no CLI. From the <a href="http://storagemadeeasy.com/faq/#commandlinemount" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://storagemadeeasy.com/faq/#commandlinemount']);">FAQ</a>:

> How do I a headless command line mount of the Linux Drive?  
> You should enter the following command into a bash startup script:
> 
>     su -c "smemount /path/to/folder login:password" user
>     

So the only thing you could do is mount like you did with **davfs** and *box*, but the SME Sync Center couldn&#8217;t be launched without Xorg running. I really liked the product (the idea is fantastic, if I ever want to tranfer between storage cloud solutions, I will definitely use this), but the lack of the CLI pushed me back.

### UbuntuOne

At this point I thought if I could get something running on the ARM Chromebook (which was running Ubuntu), then I will just figure out the rest of the OSes later. So I decided to try out **UbuntuOne**, I have heard of this a while back, but I just never gave it a try. To set it up, first install the client:

    $ sudo apt-get install ubuntuone-client
    

Then let&#8217;t change the default sync directory to be **~/.ubone** instead of **~/Ubuntu One**. This is done by editing the **/etc/xdg/ubuntuone/syncdaemon.conf** file and modifying the following line:

    root_dir.default = ~/.ubone
    

Next we can launch the GUI to get authenticated:

    $ ubuntuone-control-panel-qt
    

And you will see the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/ubone_setup.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/ubone_setup.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/ubone_setup.png" alt="ubone setup Syncing Files with Various Cloud Storage Solutions" width="736" height="525" class="alignnone size-full wp-image-9685" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After that click on &#8220;**Sign me in with my existing account**&#8221; and it will ask you to authenticate:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/ubon_auth.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/ubon_auth.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/ubon_auth.png" alt="ubon auth Syncing Files with Various Cloud Storage Solutions" width="640" height="525" class="alignnone size-full wp-image-9680" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After you are authenticated it will show you which folder it will sync with and the one we have set it perfect:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/ub_one_sync.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/ub_one_sync.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/ub_one_sync.png" alt="ub one sync Syncing Files with Various Cloud Storage Solutions" width="736" height="525" class="alignnone size-full wp-image-9681" title="Syncing Files with Various Cloud Storage Solutions" /></a>

After you are done with the configuration, you should see the **syncdaemon** running:

    $ps -ef | grep ubuntuone
    elatov   22259     1  0 13:02 ?        00:00:02 /usr/bin/python /usr/lib/ubuntuone-client/ubuntuone-syncdaemon
    

And you can also check the status but using the CLI:

    $u1sdtool -s
    State: QUEUE_MANAGER
        connection: With User With Network
        description: processing the commands pool
        is_connected: True
        is_error: False
        is_online: True
        queues: IDLE
    

There are also instructions on how to get authenticated on a headless Linux server. The instructions are laid out <a href="http://askubuntu.com/questions/95591/how-do-i-configure-ubuntu-one-on-a-server" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://askubuntu.com/questions/95591/how-do-i-configure-ubuntu-one-on-a-server']);">here</a>. You just have to use a python script to get authenticated. I ran into some forums on how to set it up for Fedora and Debian, which were my two other machines (UbuntuOne had clients for MacOS and Windows as well):

*   <a href="http://www.maxiberta.com.ar/blog/ubuntuone-packages-fedora" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.maxiberta.com.ar/blog/ubuntuone-packages-fedora']);">UbuntuOne Packages for Fedora</a> 
*   <a href="http://blog.pinguinplanet.de/2012/05/ubuntu-one-on-debian-wheezy.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.pinguinplanet.de/2012/05/ubuntu-one-on-debian-wheezy.html']);">Ubuntu One on Debian Wheezy</a> 
*   <a href="http://forums.debian.net/viewtopic.php?f=16&t=63310" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forums.debian.net/viewtopic.php?f=16&t=63310']);">Howto: Ubuntu One in Debian Wheezy</a>

The Fedora one seemed okay, just had to add a repository but the Debian setup seemed surprisingly complicated. As I started to configuration on Fedora, I ran into an issue where the **NetworkManager** had to be running (<a href="http://askubuntu.com/questions/95591/how-do-i-configure-ubuntu-one-on-a-server" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://askubuntu.com/questions/95591/how-do-i-configure-ubuntu-one-on-a-server']);">link</a>). Some of these had static IPs and had no need to run that. Rather then installing NetworkingManager on all of my machines, I decided to move one. So far, I really liked UbuntuOne, if you are using Ubuntu Laptops, I would definitely recommend it, but if you are using another distribution, it might be a little difficult to setup.

### Others and Seafile

At this point I just started doing some random research.

#### Syncany

The first one I ran into was Syncany, from <a href="http://www.syncany.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.syncany.org/']);">their</a> site:

> Syncany is an open-source cloud storage and filesharing application. It allows users to backup and share certain folders of their workstations using any kind of storage, e.g. FTP, Amazon S3 or Google Storage.
> 
> While the basic idea is similar to Dropbox and JungleDisk, Syncany is open-source and additionally provides data encryption and more flexibility in terms of storage type and provider

The idea was similar to SME, but it was opensource. I couldn&#8217;t find any CLI, just GUI for this application. And it seemed that they are trying to integrate with SparkleShare:

> 7 Mar 2013: We&#8217;re still hanging in there. Even though the direction is now a different one. We&#8217;re first trying to integrate Syncany with SparkleShare as a backend. Check out a detailed status in my recent mailing list post.

#### SparkleShare

SparkleShare seemed pretty cool, from <a href="http://sparkleshare.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sparkleshare.org/']);">their</a> site:

> How does it work?  
> SparkleShare creates a special folder on your computer. You can add remotely hosted folders (or &#8220;projects&#8221;) to this folder. These projects will be automatically kept in sync with both the host and all of your peers when someone adds, removes or edits a file.

It&#8217;s almost like a private dropbox setup. You run a server and then you connect clients to the server and every one synchronizes between each other. When I was reading about it, I thought of **git** right away (it seemed so similar), as I kept reading I saw the following:

> SparkleShare uses the version control system Git under the hood, so setting up a host yourself is relatively easy. Using your own host gives you more privacy and control, as well as lots of cheap storage space and higher transfer speeds.

This seemed really cool, but I actually like having the idea of having the files online somewhere, just for back up reasons.

#### DVCS-Autosync

Another similar tool to SparleShare is DVCS-Autosync. From <a href="http://www.mayrhofer.eu.org/dvcs-autosync" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.mayrhofer.eu.org/dvcs-autosync']);">their</a> site:

> dvcs-autosync is a project to create an open source replacement for Dropbox/Wuala/Box.net/etc. based on distributed version control systems (DVCS). It offers nearly instantaneous mutual updates when a file is added or changed on one side but with the added benefit of (local, distributed) versioning and that it does not rely on a centralized service provider, but can be used with any DVCS hosting option including a completely separate server &#8211; your data remains your own.

It actually used XMMP for it&#8217;s communication and it could use other tools than git, more from their site:

> Synchronization of directories is based on DVCS repositories. Git is used for main development and is being tested most thoroughly as the backend storage, but other DVCS such as Mercurial are also supported. dvcs-autosync is comparable to SparkleShare in terms of overall aim, but takes a more minimalistic approach. A single Python script monitors the configured directory for live changes, commits these changes to the DVCS (such as git) and synchronizes with other instances using XMPP messages.

So you would actually need an XMPP server to make it work (or use gtalk). The idea seems really cool as well but I wasn&#8217;t really looking for hosting my own private storage cloud solution

#### OwnCloud

This application could almost do anything. It runs on PHP and allows you to upload files to it and also connect to other storage cloud providers (like SME) and supports WebDAV. It&#8217;s basically your own private Box.net and then some. From <a href="http://owncloud.org/about/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://owncloud.org/about/']);">their</a> site:

> ownCloud gives you universal access to your files through a web interface or WebDAV. It also provides a platform to easily view & sync your contacts, calendars and bookmarks across all your devices and enables basic editing right on the web. Installation has minimal server requirements, doesn’t need special permissions and is quick. ownCloud is extendable via a simple but powerful API for applications and plugins.

There are also client available for all the platforms and you can compile your own if you wanted to. If I really wanted to host my own dropbox-like service, I would definitely give this a try&#8230; maybe for another day.

#### SeaFile

At this point I ran into **Seafile**. What was cool about **seafile** is that you can setup your own storage cloud if you want, or you could use their storage cloud called **SeaCloud**. Here is information regarding seacloud, from <a href="https://seacloud.cc/group/2/wiki/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://seacloud.cc/group/2/wiki/']);">their</a> site:

> SeaCloud is a place for managing your documents with team members. You can create public/private groups with file syncing, wiki, discussion and other functions. SeaCloud is hosted on Amazon Web Services.
> 
> Based on the open source file-syncing tool Seafile

And here is information regarding SeaFile, for <a href="https://github.com/haiwen/seafile" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/haiwen/seafile']);">their</a> git page:

> Dropbox is good for file syncing and sharing, but is not an ideal place for collaboration. So we build Seafile, a better place for managing documents together.
> 
> In Seafile, you can create groups with file syncing, wiki, discussion and tasks. It enables you to easily collaborate around documents within a team. In addition, it is open source. So you can build a private cloud freely for your organization.

More information:

> Seafile is a full-fledged document collaboration platform. It has following features:
> 
> 1.  Groups with file syncing, wiki, discussion and tasks. 
> 2.  Managing files into libraries. Each library can be synced separately. 
> 3.  Sync with existing folders. 
> 4.  File revisions. 
> 5.  Library encryption with a user chosen password.

This also works in a similar way to Git:

> Seafile uses GIT&#8217;s version control model, but simplified for automatic synchronization, and doesn&#8217;t depend on GIT. Every library is like a GIT repository. It has its own unique history, which consists of a list of commits. A commit points to the root of a file system snapshot. The snapshot consists of directories and files. Files are further divided into blocks for more efficient network transfer and storage usage.

So if I wanted my own private storage cloud, I would definitely give this a try as well. Actually there were a couple of sites, that compared ownCloud, SparkelShare, and Seafile and they all liked Seafile:

*   <a href="http://www.webupd8.org/2013/02/seafile-robust-file-synchronization-and.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.webupd8.org/2013/02/seafile-robust-file-synchronization-and.html']);">Seafile: Robust File Synchronization and Collaboration Tool that you Can Run on your Linux Server</a>
*   <a href="http://blog.patshead.com/2013/04/self-hosted-cloud-storage-solution-owncloud-vs-sparkleshare.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.patshead.com/2013/04/self-hosted-cloud-storage-solution-owncloud-vs-sparkleshare.html']);">Self-Hosted Cloud Storage: ownCloud vs. SparkleShare vs. BitTorrent Sync vs Seafile</a>
*   <a href="http://stevenhickson.blogspot.com/2013/04/cloud-storage-on-raspberry-pi.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://stevenhickson.blogspot.com/2013/04/cloud-storage-on-raspberry-pi.html']);">Cloud storage on the Raspberry Pi</a>

### Seafile Cli Install

So I decided to try out **Seafile** but not for it&#8217;s server capabilities but rather for the Linux Cli connecting to their *seacloud*. Here is what I did to install the **seafile** cli on my Debian box, most of the instructions are laid out <a href="https://github.com/haiwen/seafile/wiki/Build-and-use-seafile-client-from-source" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/haiwen/seafile/wiki/Build-and-use-seafile-client-from-source']);">here</a>. First install the prerequisites:

    $ sudo apt-get install libglib2.0-dev
    

Then grab the source and extract it:

    $ wget http://seafile.googlecode.com/files/seafile-latest.tar.gz
    $ tar xzf seafile-latest.tar.gz
    

Now let&#8217;s compile **libsearpc** (initially I tried with the **&#8211;prefix** option when running **./configure**, but it gave me an error during the complie, that issue is currently getting looked at, here is the <a href="https://groups.google.com/forum/#!msg/seafile/vO7CCdsMwxE/PxCTDv4XotwJ" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://groups.google.com/forum/#!msg/seafile/vO7CCdsMwxE/PxCTDv4XotwJ']);">link</a> for the bug report). By default the compile puts all the files under **/usr/local** and that was good enough for me. I could&#8217;ve probably changed the configure scripts around but I didn&#8217;t feel like messing with it. So first go inside the source code:

    $ cd seafile-1.8.2/libsearpc
    

For some reason the linking of the libraries is messed up as well, so run the following to include libraries that will be under **/usr/local/lib**:

    $ setenv CC "gcc -Wl,-rpath,/usr/local/lib"
    

Now for the configure:

    ./configure --enable-compile-demo=no
    

and now for the compile:

    $ make
    

and finally for the install:

    $ sudo make install
    

Here is what I ran to compile **ccnet**:

    $ cd seafile-1.8.2/ccnet
    $ sudo apt-get install uuid-dev libevent-dev libsqlite3-dev
    $ ./configure --enable-compile-demo=no
    $ make
    $ sudo make install
    

And here is what I ran to install **seafile**:

    $ cd seafile-1.8.2
    $ ./configure --enable-client --disable-gui
    $ make
    $ sudo make install
    

Now here are the commands to initialize the client:

    $ sudo apt-get install python-simplejson
    $ mkdir .config/seafile
    $ seaf-cli init -d .config/seafile/
    done
    Successly create configuration dir /home/elatov/.ccnet.
    Writen seafile data directory /home/elatov/.config/seafile/seafile-data to /home/elatov/.ccnet/seafile.ini
    

Now start the daemon:

    $seaf-cli start
    starting ccnet daemon ...
    Started: ccnet daemon ...
    starting seafile daemon ...
    Started: seafile daemon ...
    

Now login to your **seacloud** management console and click on your library and it will show your repo ID for your library:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_repo_url.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_repo_url.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_repo_url.png" alt="seafile repo url Syncing Files with Various Cloud Storage Solutions" width="605" height="119" class="alignnone size-full wp-image-9672" title="Syncing Files with Various Cloud Storage Solutions" /></a>

The string after repo if what you need. Now to synchronize with that library create a local directory and run the following to synchronize your local directory with the remote library:

    $ mkdir .sea
    $ seaf-cli sync -l 30070853-17fe-4fd5 -s https://seacloud.cc -d .sea -u mylogin@me.com
    

You will be able to check the status by running the following:

    $ seaf-cli status
    # Name  Status  Progress
    
    # Name  Status
    files       downloading
    

You can also check which library is synchronized with which local folder by running the following:

    $ seaf-cli list
    Name    ID      Path
    files 30070853-17fe-4fd5 /home/elatov/.sea
    

That&#8217;s it, now I can just run `seaf-cli start` on start up and my files will always synchronized. There are also Mac OS, Android, and Windows clients (all have installers). The is also a Linux Applet available. To compile the **seafile-applet**, run the following during the configure:

    $ ./configure --enable-client --disable-server
    

You can launch the applet, by running the following:

    $ seafile-applet &
    

After executing that, it will check if the **seafile-daemon** is running. If it is, it&#8217;ll just attach it self to that. If the **seafile-daemon** is not running, then it will start it up and then attach it self to that. Here is seafile running in the notification area:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_applet.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_applet.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_applet.png" alt="seafile applet Syncing Files with Various Cloud Storage Solutions" width="27" height="27" class="alignnone size-full wp-image-9682" title="Syncing Files with Various Cloud Storage Solutions" /></a>

This definitely fit my needs and I was happy with the setup. Lastly you can check on the local **seafile** daemon, by visiting **https://localhost:13420** to see the status:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_client_browser.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_client_browser.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/10/seafile_client_browser.png" alt="seafile client browser Syncing Files with Various Cloud Storage Solutions" width="639" height="191" class="alignnone size-full wp-image-9673" title="Syncing Files with Various Cloud Storage Solutions" /></a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/10/syncing-files-various-cloud-storage-solutions/" title=" Syncing Files with Various Cloud Storage Solutions" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:cloud storage,seacloud,seafile,blog;button:compact;">A while ago I wrote this post on how to use Grive. Grive is a cross platform/architecture client that allowed me to sync files with Google Drive. I really liked...</a>
</p>