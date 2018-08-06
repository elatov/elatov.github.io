---
title: Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive
author: Karim Elatov
layout: post
permalink: /2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/
dsq_thread_id:
  - 1405469623
categories: ['os', 'storage']
tags: ['linux', 'android', 'boxcryptor', 'encfs', 'fedora', 'grive', 'ubuntu']
---

I wanted to share an encrypted file between my Linux workstations and my Android phone. There are a couple of ways to go about this, here is small list:

*   DropBox with TrueCrypt
*   SpiderOak
*   SkyDrive with BoxCryptor

There are a bunch more, check out the following sites for more options:

*   [5 Ways To Securely Encrypt Your Files In The Cloud](http://www.makeuseof.com/tag/5-ways-to-securely-encrypt-your-files-in-the-cloud/)
*   [How to encrypt your cloud storage for free](http://www.pcworld.com/article/2010296/how-to-encrypt-your-cloud-storage-for-free.html)
*   [4 Alternatives to Google Drive for Linux](http://www.howtogeek.com/130465/4-alternatives-to-google-drive-for-linux/)

My **DropBox** account ran out of space recently, so I wanted a solution that could connect to **Google Drive**. The only Android App (that I could find) which can connect to Google Drive and encrypt files is **BoxCryptor**. BoxCryptor can also read files encrypted by **EncFS**. This definitely fit my needs, hence I decided to use EncFS with BoxCryptor and Google Drive.

## 1. Install **Grive** on your Linux WorkStations

Most of the instructions were taken from [here](http://www.linuxjournal.com/content/introducing-grive).

### Install and Setup Grive on Ubuntu

First I added the appropriate repository:

    kerch:~>sudo add-apt-repository ppa:nilarimogard/webupd8


I then updated the repositories:

    kerch:~>sudo apt-get update


Lastly, I installed the **grive** package:

    kerch:~>sudo apt-get install grive


If for some reason you have to install the package from source, here are all the prerequisite packages that need to be installed prior:

    sudo apt-get install git cmake build-essential libgcrypt11-dev libjson0-dev libcurl4-openssl-dev libexpat1-dev libboost-filesystem-dev libboost-program-options-dev binutils-dev


Now to configure the Google Drive Synchronization:

    kerch:~>mkdir .gdrive
    kerch:~>cd .gdrive/
    kerch:~/.gdrive>grive -a
    -----------------------
    Please go to this URL and get an authentication code:

    -----------------------
    Please input the authentication code here:


At this point you can visit the link provided by grive. After you enter the authentication code, the sync will start:

    Reading local directories
    Synchronizing folders
    Reading remote server file list
    Synchronizing files ...


When it's done you will see your Google Drive files:

    kerch:~/.gdrive>ls
    old Scratchpad share


Now let's create a new folder and call it "**enc**" and sync that to Google Drive:

    kerch:~/.gdrive>mkdir enc
    kerch:~/.gdrive>grive
    Reading local directories
    Synchronizing folders
    Reading remote server file list
    Detecting changes from last sync
    Synchronizing files
    sync "./enc" doesn't exist in server, uploading
    Finished!


Now let's do the same thing on the Fedora machine.

### Install and Setup Grive on Fedora

There was no pre-compiled package so I had to compile the application my self. From the above site they list some prerequisites. I was running Fedora 17 so I didn't have to compile the prerequisites. Here is my Fedora version:

    moxz:~>lsb_release -a
    LSB Version: :core-4.1-ia32:core-4.1-noarch:cxx-4.1-ia32:cxx-4.1-noarch:desktop-4.1-ia32:desktop-4.1-noarch :languages-4.1-ia32:languages-4.1-noarch:printing-4.1-ia32:printing-4.1-noarch
    Distributor ID: Fedora
    Description: Fedora release 17 (Beefy Miracle)
    Release: 17
    Codename: BeefyMiracle


And here are the packages I had installed:

    moxz:~>rpm -qa | grep -i cmake
    cmake-2.8.9-1.fc17.i686


And also for the **boost** package:

    moxz:~>rpm -qa | grep boost-1
    boost-1.48.0-13.fc17.i686


If you are at lower versions then follow the instructions in the above document to update those packages to the appropriate versions. I then installed all the necessary packages:

    moxz:~>sudo yum install automake autoconf openssl openssl-devel json-c json-c-devel curl curl-devel libcurl-devel libcurl libarchive libarchive-devel libidn libidn-devel expat expat-devel binutils binutils-devel


After that, I downloaded the source:

    moxz:~>cd /tmp
    moxz:/tmp>git clone https://github.com/Grive/grive.git
    Cloning into 'grive'...
    remote: Counting objects: 2591, done.
    remote: Compressing objects: 100% (865/865), done.
    remote: Total 2591 (delta 1713), reused 2555 (delta 1681)
    Receiving objects: 100% (2591/2591), 750.79 KiB | 140 KiB/s, done.
    Resolving deltas: 100% (1713/1713), done.


Then I configured the application to be installed under **/usr/local/grive**:

    moxz:/tmp>cd grive/
    moxz:/tmp/grive>sudo mkdir /usr/local/grive
    moxz:/tmp/grive>sudo chown elatov:elatov /usr/local/grive
    moxz:/tmp/grive>cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/grive .
    -- The C compiler identification is GNU 4.7.2
    -- The CXX compiler identification is GNU 4.7.2
    -- Check for working C compiler: /bin/cc
    -- Check for working C compiler: /bin/cc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working CXX compiler: /bin/c++
    -- Check for working CXX compiler: /bin/c++ -- works
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Found libgcrypt: -lgcrypt -ldl -lgpg-error
    -- Found JSON-C: /usr/lib/libjson.so
    -- Found CURL: /usr/lib/libcurl.so (found version "7.27.0")
    -- Found EXPAT: /usr/lib/libexpat.so (found version "2.1.0")
    -- Boost version: 1.48.0
    -- Found the following Boost libraries:
    --   program_options
    --   filesystem
    --   system
    -- Found libbfd: /usr/lib/libbfd.so
    -- Found libiberty: /usr/lib/libiberty.a
    -- Found ZLIB: /usr/lib/libz.so (found version "1.2.7")
    -- Boost version: 1.48.0
    -- Found the following Boost libraries:
    --   program_options
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /tmp/grive


Then I compiled the application and installed it:

    moxz:/tmp/grive>make all install
    Scanning dependencies of target grive
    [ 2%] Building CXX object libgrive/CMakeFiles/grive.dir/src/drive/CommonUri.cc.o
    [ 5%] Building CXX object libgrive/CMakeFiles/grive.dir/src/drive/Entry.cc.o
    ...
    ...
    [ 91%] Building CXX object libgrive/CMakeFiles/grive.dir/src/bfd/Debug.cc.o
    [ 94%] Building CXX object libgrive/CMakeFiles/grive.dir/src/bfd/Backtrace.cc.o
    [ 97%] Building CXX object libgrive/CMakeFiles/grive.dir/src/bfd/SymbolInfo.cc.o
    Linking CXX static library libgrive.a
    [ 97%] Built target grive Scanning dependencies of target grive_executable
    [100%] Building CXX object grive/CMakeFiles/grive_executable.dir/src/main.cc.o
    Linking CXX executable grive
    [100%] Built target grive_executable
    Install the project...
    -- Install configuration: ""
    -- Installing: /usr/local/grive/bin/grive
    -- Installing: /usr/local/grive/share/man/man1/grive.1


I then followed similar instructions as I did for Ubuntu to sync up Google Drive contents under **~/.gdrive**. After I was done, I had the following contents:

    moxz:~>ls .gdrive/
    enc old Scratchpad share


## 2. Install EncFS and Encrypt the Google Drive Folder

First let's do this on our Fedora System. There are some good guides on that [here](https://www.howtoforge.com/encrypt-your-data-with-encfs-fedora-18).

### Install and Setup *EncFS* on Fedora

First let's install the package:

    moxz:~>sudo yum install fuse-encfs
    Resolving Dependencies
    ...
    ...
    Installed: fuse-encfs.i686 0:1.7.4-6.fc17
    Dependency Installed:
    fuse-libs.i686 0:2.8.7-2.fc17 rlog.i686 0:1.4-10.fc17
    Complete!


Now let's create a directory where the decrypted data will be mounted:

    moxz:~>mkdir .decrypt


And now let's mount the volume:

    moxz:~>encfs ~/.gdrive/enc/ ~/.decrypt/
    Creating new encrypted volume.
    Please choose from one of the following options:
     enter "x" for expert configuration mode,
     enter "p" for pre-configured paranoia mode,
     anything else, or an empty line will select standard mode.
    ?> p

    Paranoia configuration selected.

    Configuration finished.  The filesystem to be created has
    the following properties:
    Filesystem cipher: "ssl/aes", version 3:0:2
    Filename encoding: "nameio/block", version 3:0:1
    Key Size: 256 bits
    Block Size: 1024 bytes, including 8 byte MAC header
    Each file contains 8 byte header with unique IV data.
    Filenames encoded using IV chaining mode.
    File data IV is chained to filename IV.
    File holes passed through to ciphertext.
    -------------------------- WARNING --------------------------
    The external initialization-vector chaining option has been
    enabled.  This option disables the use of hard links on the
    filesystem. Without hard links, some programs may not work.
    The programs 'mutt' and 'procmail' are known to fail.  For
    more information, please see the encfs mailing list.
    If you would like to choose another configuration setting,
    please press CTRL-C now to abort and start over.
    Now you will need to enter a password for your filesystem.
    You will need to remember this password, as there is absolutely
    no recovery mechanism.  However, the password can be changed
    later using encfsctl.
    New Encfs Password:
    Verify Encfs Password:
    moxz:~>


Let's see if it's mounted:

    moxz:~>df -h -t fuse.encfs
    Filesystem      Size  Used Avail Use% Mounted on
    encfs           56G   45G  9.1G  83% /home/elatov/.decrypt


Now let's create a new file under **~/.decrypt** and check if it gets encrypted:

    moxz:~>cd .decrypt/
    moxz:~/.decrypt>echo "This is a test" > text.txt
    moxz:~/.decrypt>ls -l
    total 4
    -rw-r--r-- 1 elatov elatov 15 Feb 16 16:50 text.txt
    moxz:~/.decrypt>cat text.txt
    This is a test


Now let's check the encrypted side:

    moxz:~/.decrypt>ls -l ../.gdrive/enc/
    total 4
    -rw-r--r-- 1 elatov elatov 31 Feb 16 16:50 T16eyfvtnHbad0XVk23Dlxal
    moxz:~/.decrypt>cat ../.gdrive/enc/T16eyfvtnHbad0XVk23Dlxal
     )Hٴ&o/+jD27Z


That looks perfect. Now let's un-mount the volume and sync the data with Google Drive:

    moxz:~>fusermount -u ~/.decrypt/
    moxz:~>df -h | grep enc
    moxz:~>cd .gdrive/
    moxz:~/.gdrive>/usr/local/grive/bin/grive
    Reading local directories
    Synchronizing folders
    Reading remote server file list
    Detecting changes from last sync
    Synchronizing files
    Synchronizing files
    sync "./enc/.encfs6.xml" doesn't exist in server, uploading
    sync "./enc/T16eyfvtnHbad0XVk23Dlxal" doesn't exist in server, uploading
    Finished!


Notice the **.encfs6.xml** file, this is the configuration file for EncFS and is very important to this setup. Don't worry, without the password this file is useless. From [this](https://forums.boxcryptor.com/topic/strength-of-encryption-security) BoxCryptor forum:

> BoxCryptor uses two keys for file encryption: a master key which is derived from a user supplied password and a volume key. All files are encrypted with a volume key which is generated when a new encrypted directory is created. The volume key is stored encrypted by the master key in a configuration file (.encfs6.xml) at the top level of the source directory. When BoxCryptor mounts an encrypted directory you have to enter the password. The password is used to derive the master key and the master key is used to decrypt the volume key which is then used for file encryption.

Now let's do the same thing on Ubuntu.

### Install and Setup EncFS on Ubuntu

First let's install the package:

    kerch:~>sudo apt-get install encfs
    Reading package lists... Done
    Building dependency tree Reading state information... Done
    The following extra packages will be installed:
      libboost-serialization1.49.0 librlog5
    The following NEW packages will be installed:
      encfs libboost-serialization1.49.0 librlog5 .. ..
    Processing triggers for man-db ...
    Setting up libboost-serialization1.49.0 (1.49.0-3.1ubuntu1.1) ...
    Setting up librlog5 (1.4-2build1) ...
    Setting up encfs (1.7.4-2.4build1) ...
    Processing triggers for libc-bin ...
    ldconfig deferred processing now taking place


Now let's sync our Google Drive contents:

    kerch:~/.gdrive>grive -f
    Reading local directories
    Synchronizing folders
    Reading remote server file list
    Detecting changes from last sync
    Synchronizing files
    sync "./enc/T16eyfvtnHbad0XVk23Dlxal" created in remote. creating local
    sync "./enc/.encfs6.xml" created in remote. creating local
    Finished!


The encrypted file is now there, let's mount the encrypted data:

    kerch:~>encfs ~/.gdrive/enc/ ~/.decrypt/
    EncFS Password:
    kerch:~>df -h | grep enc
    encfs      37G   31G   3.5G 90% /home/elatov/.decrypt


Now let's see if the file is decrypted properly:

    kerch:~>cat .decrypt/test.txt
    This is a test


That is perfect. Now let's un-mount the encrypted volume and make sure nothing is in the un-mounted directory:

    kerch:~>fusermount -u ~/.decrypt/
    kerch:~>ls ~/.decrypt/


Now let's see if we can download this file on our Android phone.

## 3. Install and Configure BoxCryptor on the Android Phone

First, go to **Google Play** and find the App:

![box cryptor google play Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/box_cryptor_google_play.png)

After installing the App and launching it, you will see the following screen:

![box crypt launched Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/box_crypt_launched.png)

Select "Connect to Google Drive" and then choose the account to login as:

![bx crypt login google drive Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/bx_crypt_login_google_drive.png)

Then another window will pop up asking you to give permission to this App to connect to Google Drive:

![allow bx crypt to google drive Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/allow_bx_crypt_to_google_drive.png)

At this point you will see your folders, it will automatically find the encrypted folder and ask you for the password:

![bx crypt enter pass Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/bx_crypt_enter_pass.png)

After you have authenticated, you should see the contents of your folder:

![bx crypt see contents Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/bx_crypt_see_contents.png)

Lastly, click on the text file and make sure you can see the contents:

![bx crypt open txt file Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](https://github.com/elatov/uploads/raw/master/2013/02/bx_crypt_open_txt_file.png)

You can always script something to automate the encrypting, decrypting, and syncing of the files.

### Related Posts

- [Installing VMware Workstation 9.0.2 on Fedora 19](/2013/08/installing-vmware-workstation-9-0-2-on-fedora-19/)

