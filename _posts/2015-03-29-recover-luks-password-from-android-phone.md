---
published: true
layout: post
title: "Recover LUKS Password from Android Phone"
author: Karim Elatov
categories: [os,storage]
tags: [android,adb,luks]
---

I had an old backup of an encrypted SD-Card from my old android phone. I just **dd**'ed the whole SD-Card for backup reason. I was able to mount the img file as a **loop** device and confirm that it was encrypted:

	$ sudo losetup -P loop1 sd.img 
	
Now for the LUKS query:

	$ cryptsetup luksDump /dev/loop0
	LUKS header information for /dev/loop0
	
	Version:       	1
	Cipher name:   	aes
	Cipher mode:   	cbc-plain
	Hash spec:     	sha1
	Payload offset:	4096
	MK bits:       	256
	MK digest:     	46 97 79 28 ed 60 6a fe ad 7e cb d7 67 37 6a ab 89 2d bc fc
	MK salt:       	54 1f 7e a0 ea da e4 d0 f8 af 53 e2 c1 e6 c7 be
	              	1b 18 e8 e0 1c 68 cc 01 3e c8 cd 07 9a ee 5f 8a
	MK iterations: 	38625
	UUID:          	62acffbc-6102-485c-8f37-9d9a9727ad1c
	
	Key Slot 0: ENABLED
	Iterations:         	154775
	Salt:               	67 49 33 d9 ca 5b 3d f4 05 46 6d a9 a0 9e a4 1f
	                      	97 0a 5c 68 72 f1 ad b5 ac dd e0 97 f0 f5 b2 70
	Key material offset:	8
	AF stripes:            	4000
	Key Slot 1: DISABLED
	Key Slot 2: DISABLED
	Key Slot 3: DISABLED
	Key Slot 4: DISABLED
	Key Slot 5: DISABLED
	Key Slot 6: DISABLED
	Key Slot 7: DISABLED

We can also confirm by using **file**:

	$ file /data/phone/sd.img
	/data/phone/sd.img: LUKS encrypted file, ver 1 [aes, cbc-plain, sha1] UUID: 62acffbc-6102-485c-8f37-9d9a9727ad1c

Reading over the "[Revisiting Android disk encryption](http://nelenkov.blogspot.com/2014/10/revisiting-android-disk-encryption.html)" site we can see that AES in CBC mode is indeed used by android phone for disk encryption:

> Full disk encryption (FDE) for Android was introduced in version 3.0 (Honeycomb) and didn't change much until version 4.4 (discussed in the next section). Android's FDE uses the dm-crypt target of Linux's device mapper framework to implement transparent disk encryption for the userdata (mounted as /data) partition. Once encryption is enabled, all writes to disk automatically encrypt data before committing it to disk and all reads automatically decrypt data before returning it to the calling process. The disk encryption key (128-bit, called the 'master key') is randomly generated and protected by the lockscreen password. Individual disk sectors are encrypted by the master key using AES in CBC mode, with ESSIV:SHA256 to derive sector IVs.

My phone was running **cyanogenmod 9.1** which is **andoid 4.0.4**:

	$ adb shell
	shell@android:/ $ getprop ro.build.version.release
	4.0.4
	shell@android:/ $ getprop ro.modversion
	9.1.0-pyramid

The phone was of course **root**ed. So I wanted to mount the disk image on my laptop.

### Getting the Master Key File
I ran into [this](http://k0rx.com/blog/2013/03/luks.html) site which talked about cracking the master key. It talked about installing a module called [LiME](https://github.com/504ensicsLabs/LiME) which allows you to dump the contents of your phone's RAM into a file.

### Installing LiME

Compiling LiME has a couple of steps, I found good sites that go over the process:

- [LiME – Linux Memory Extractor](https://github.com/504ensicsLabs/LiME/tree/master/doc)
- [LiME](http://sgros-students.blogspot.ca/2014/04/lime.html)
- [AndroidMemoryForensics](https://code.google.com/p/volatility/wiki/AndroidMemoryForensics)  

So let's get started on that.

#### Install Android NDK

You can download it from [here](http://developer.android.com/tools/sdk/ndk/index.html). At the time of writing I was able to get this one:

	$ wget http://dl.google.com/android/ndk/android-ndk-r10d-linux-x86_64.bin

To install it, I first made the installer executable and then ran the installer:

	$ chmod +x android-ndk-r10d-linux-x86_64.bin
	$ ./android-ndk-r10d-linux-x86_64.bin
	Extracting  android-ndk-r10d/build/gmsl
	Extracting  android-ndk-r10d/build/core
	Extracting  android-ndk-r10d/build/awk
	Extracting  android-ndk-r10d/build
	Extracting  android-ndk-r10d
	
	Everything is Ok

After that I put it under **/usr/local**:

	$ sudo mv android-ndk-r10d /usr/local/.
	$ sudo ln -s /usr/local/android-ndk-r10d /usr/local/and-ndk

#### Install Android sdk

You can download the SDK from [here](http://developer.android.com/sdk/index.html#Other). At the time of writing I got the following version:

	$ wget http://dl.google.com/android/android-sdk_r24.0.2-linux.tgz

Then I extracted it:

	$ tar xvzf android-sdk_r24.0.2-linux.tgz

And lastly I installed in under **/usr/local**:

	$ sudo mv android-sdk-linux/ /usr/local/.
	$ sudo ln -s /usr/local/android-sdk-linux/ /usr/local/and-sdk

#### Get the Kernel Source

My phone was running 3.0 version of the kernel:

	$ adb shell
	shell@android:/ $ uname -a
	Linux localhost 3.0.36-g7290c7f #2 SMP PREEMPT Sun Jul 1 00:25:26 PDT 2012 armv7l GNU/Linux

After some research I found the source in the following locations:

- [Kernel Source Code, Binaries and Updates for HTC Android Phones](http://www.htcdev.com/devcenter/downloads) 
- [HTC MSM8660 kernels](https://github.com/htc-msm8660/android_kernel_htc_msm8660) 

My phone was an HTC Sensation:

	shell@android:/ $ getprop ro.product.model
	HTC Sensation

So I decided to just clone the git repo (and it worked out):

	$ git clone https://github.com/htc-msm8660/android_kernel_htc_msm8660.git -b android-msm-pyramid-3.0

#### Get the Source Code for LiME
This one is pretty easy just run the following to clone the git repo:

	$ git clone https://github.com/504ensicsLabs/LiME.git
	
I just left it in my home directory.

#### Prepare the Environment for Compiling

First we need to set up all the environment variables:

	export SDK_PATH=/usr/local/and-sdk/
	export NDK_PATH=/usr/local/and-ndk/
	export KSRC_PATH=/data/work/android_kernel_htc_msm8660/
	export CC_PATH=/usr/local/and-ndk/toolchains/arm-linux-androideabi-4.8/prebuilt/linux-x86_64/bin/
	export LIME_SRC=~/LiME/src/

Now let's pull the kernel config from phone:

	$ adb pull /proc/config.gz

Now let's extract it
	
	$ gunzip config.gz
	
And let's copy it into the kernel source

	$ cp config /data/work/android_kernel_htc_msm8660/.config

Before preparing the source I had to modify the wrapper script to use python 2.7 (by default my **gentoo** box uses python 3), the issue was discussed [here](http://forum.xda-developers.com/showthread.php?t=1821869). So I modified the following file: **/data/work/android_kernel_htc_msm8660/scripts/gcc-wrapper.py** and made the following change:


	- #! /usr/bin/env python
	+ #! /usr/bin/env python2.7

I was then able to prepare the source without any warnings:

	$ cd /data/work/android_kernel_htc_msm8660
	$ make ARCH=arm CROSS_COMPILE=$CC_PATH/arm-linux-androideabi- modules_prepare

#### Compile LiME
Now let's modify the **Makefile** for LiME, I edited the  **~/LiME/src/Makefile** file and made the following changes:

	PWD := $(shell pwd)
	
	+ KDIR := /data/work/android_kernel_htc_msm8660/
	+ CCPATH := /usr/local/android-ndk-r10d/toolchains/arm-linux-androideabi-4.8/prebuilt/linux-x86_64/bin/
	
	default:
	-   $(MAKE) -C /lib/modules/$(KVER)/build M=$(PWD) modules
	-   strip --strip-unneeded lime.ko
	-   mv lime.ko lime-$(KVER).ko
	+ #   $(MAKE) -C /lib/modules/$(KVER)/build M=$(PWD) modules
	+ #   strip --strip-unneeded lime.ko
	+ #   mv lime.ko lime-$(KVER).ko
	+    $(MAKE) ARCH=arm CROSS_COMPILE=$(CCPATH)/arm-linux-androideabi- -C $(KDIR) EXTRA_CFLAGS=-fno-pic M=$(PWD) modules
	+    mv lime.ko lime-pyramid.ko

Then running **make** worked without issues:

	$ cd ~LiME/src
	$ make

#### Try loading the LiME module on the Android Phone

Let's push the module to the phone:

	$adb push lime-pyramid.ko /sdcard/lime.ko
	1520 KB/s (347364 bytes in 0.223s)


Upon loading the module I saw the following: 

	$ adb shell
	shell@android:/ $ su -
	root@android:/ # cd sdcard
	root@android:/sdcard # insmod lime.ko
	insmod: init_module 'lime.ko' failed (Exec format error)
	255|

I ran **dmesg** and I saw the following:

	<3>[656653.599731] lime: version magic '3.0.36-g7290c7f-dirty SMP preempt mod_unload ARMv7 ' should be '3.0.36-g7290c7f SMP preempt mod_unload ARMv7 '

#### Fixing Kernel Version for LiME Module
It looks like another person ran into the same and his discoveries are [here](http://neosysforensics.blogspot.com/2012/09/creando-volcados-de-memoria-en-android.html). We need to make sure the kernel version of the module matches the kernel version running on the phone. So the one I built had the following information:

	~/LiME/src$ modinfo ./lime-pyramid.ko
	filename:       ~/LiME/src/./lime-pyramid.ko
	license:        GPL
	depends:
	vermagic:       3.0.36-g7290c7f-dirty SMP preempt mod_unload ARMv7
	parm:           path:charp
	parm:           dio:int
	parm:           format:charp

So I specified the version in the kerner source make file here **/data/work/android_kernel_htc_msm8660/Makefile**:

	VERSION = 3
	PATCHLEVEL = 0
	SUBLEVEL = 36
	EXTRAVERSION = -g7290c7f
	NAME = Sneaky Weasel

Then re-prepared the kernel source:

	$ cd /data/work/android_kernel_htc_msm8660
	$ make ARCH=arm CROSS_COMPILE=$CC_PATH/arm-linux-androideabi- clean
	$ make ARCH=arm CROSS_COMPILE=$CC_PATH/arm-linux-androideabi- modules_prepare

And then rebuilding the LiME module:

	$ cd ~LiME/src
	$ make clean
	$ rm lime-pyramid.ko
	$ make

Double checking the module it had the following information:

	~/LiME/src$ modinfo ./lime-pyramid.ko 
	filename:       ~/LiME/src/./lime-pyramid.ko
	license:        GPL
	depends:
	vermagic:       3.0.36-g7290c7f SMP preempt mod_unload ARMv7
	parm:           path:charp
	parm:           dio:int
	parm:           format:charp

### Getting the RAM contents from the phone

Then after pushing the new module it loaded fine:

	root@android:/ # insmod /sdcard/lime.ko "path=/sdcard/lime.dump format=lime"
	root@android:/sdcard # ls -la /sdcard/lime.dump
	----rwxr-x system   sdcard_rw 627048480 2015-03-15 10:05 lime.dump

Then I just grabbed the whole file

	$ adb pull /sdcard/lime.dump
	3119 KB/s (627048480 bytes in 196.314s)

It took about 3 mins (it wasn't that much)

### Compile *aeskeyfind*

I just grabbed the source:

	$ wget http://ftp.ubuntu.com/ubuntu/pool/universe/a/aeskeyfind/aeskeyfind_1.0.0.orig.tar.gz

Then extracted it:

	$ tar xzf aeskeyfind_1.0.0.orig.tar.gz

And the compile was pretty easy:

	$ cd aeskeyfind/
	aeskeyfind$ make
	cc -Wall -O4 -std=c99   -c -o aeskeyfind.o aeskeyfind.c
	cc -Wall -O4 -std=c99   -c -o aes.o aes.c
	cc -Wall -O4 -std=c99   -c -o util.o util.c
	cc -o aeskeyfind aeskeyfind.o aes.o util.o

### Getting the master key from the LiME Dump
Now that I have the **aeskeyfind** and the LiME dump on the same machine I can just run the following to get the key:

	aeskeyfind$./aeskeyfind -v ~/lime.dump
	FOUND POSSIBLE 256-BIT KEY AT BYTE d666c60
	
	KEY: 487c537e76e0eb1aac6becfe9a93dbb1995e3ba1ce239c78e4fea6ec9becedb7 <---
	
	EXTENDED KEY:
	487c537e76e0eb1aac6becfe9a93dbb1
	995e3ba1ce239c78e4fea6ec9becedb7
	8729fa6af1c911705da2fd8ec731263f
	5f99ccd491ba50ac7544f640eea81bf7
	47869242b64f8332ebed7ebc2cdc5883
	2e1fa638bfa5f694cae100d424491b23
	7829b474ce663746258b49fa09571179
	2f44248e90e1d21a5a00d2ce7e49c9ed
	4bf4e1878592d6c1a0199f3ba94e8e42
	fc6b3da26c8aefb8368a3d7648c3f49b
	754bf5d5f0d9231450c0bc2ff98e326d
	65721e9e09f8f1263f72cc5077b138cb
	9d4cea206d95c9343d55751bc4db4776
	79cbbea670334f804f4183d038f0bb1b
	51a645273c338c130166f908c5bdbe7e
	
	CONSTRAINTS ON ROWS:
	0000000000000000000000000000000000000000000000000000000000000000
	0000000000000000000000000000000000000000000000000000000000000000
	0000000000000000000000000000000000000000000000000000000000000000
	0000000000000000000000000000000000000000000000000000000000000000
	0000000000000000000000000000000000000000000000000000000000000000
	0000000000000000000000000000000000000000000000000000000000000000
	00000000000000000000000000000000
	110b84a00c81083346f8f40d8470daa3154dba3b11f24e23ecd4fe53a08240f2
	2bc9081b4577838cba0332218ab1b60172424fc6f1ff0c07207361290db2a319
	1449acbf57f2c8f2ff74b1ad30b2842045236cd72ace95b6d18c6d2e2dc1c230
	df0da3daee94ad1ea886795fcfc6358dea825eba4950bfeefb42f898fc4daf1e
	dfb3863bbc58e3694612d44167404cd25132c4668c188e9ab2124776070f5786
	2d9318383c22c5aafa4a3728215298938329a390c45c32853e0ac9ecb51d10f0
	1bd15b85f7aedb01c668f282db18afbb29ecb4a3b58b617854a72ae779095c75
	
	Keyfind progress: 100%

#### Mount the encrypted LUKS disk
First let's create the master key file:

	$ echo "487c537e76e0eb1aac6becfe9a93dbb1995e3ba1ce239c78e4fea6ec9becedb7" | xxd -r -p > mf.key

Now let's decrypt the disk:

	$ sudo cryptsetup luksOpen --master-key-file mf.key /dev/loop0 phone
	
Lastly let's mount the decrypted disk:

	$ sudo mount /dev/mapper/phone /mnt/phone
