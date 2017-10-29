---
published: false
layout: post
title: "ESXi 6.5 Passthrough Video Card/GPU to Plex VM"
author: Karim Elatov
categories: [vmware,os]
tags: [plex,intel_gpu_top]
---
### Hardware Acceleration with Plex
So I ran into [Using Hardware-Accelerated Streaming](https://support.plex.tv/hc/en-us/articles/115002178853) post from plex. And I found it intriguing, but then I saw this section in the post:

> Can I use Hardware-Accelerated Streaming inside of a virtual machine?
>
> Hardware-Acceleration Streaming is not currently possible inside of virtual machines, as virtual machine hosts do not expose low-level video hardware to the guest operating system.  While some virtual machines expose generic 3D acceleration to the guest OS as a virtual driver, this does not include support for accelerated video decoding or encoding.

But I wanted to find out what would happen if I just passthough the Video Card to the VM?

### Enable Passthrough on Video Card/GPU in ESXi 6.5
The instructions for accomplishing this are laid out in:

* [Virtual Machine Graphics
Acceleration Deployment Guide](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/whitepaper/vmware-horizon-view-graphics-acceleration-deployment-white-paper.pdf)
* [ESXi GPU Passthrough for an HTPC](https://www.webbosworld.co.uk/?p=471)
* [How to enable a VMware Virtual Machine for GPU Pass-through](http://www.dell.com/support/article/us/en/19/sln288103/how-to-enable-a-vmware-virtual-machine-for-gpu-pass-through?lang=en)

I have the following Video Card on my ESXi Host:

	[root@hp:~] lspci | grep -i vga
	00000:000:02.0 VGA compatible controller: Intel Corporation HD Graphics 530

Looking at other forums it looks like people didn't have much luck with that video card:

* [ESXI 6 - PCI passthrough for Intel Sky Lake chipset onboard VGA, SATA](https://communities.vmware.com/thread/533854)
* [NUC5i5MYHE Intel HD Graphics problem (ESXi passthrough)](https://communities.intel.com/thread/113733)

But I guess I got lucky. In the *vSphere Web Client*, I just went to **Host** -> **Manage** -> **Hardware** -> **PCI Devices** -> **Toggle passthough** on the Video Card:

![esxi-passthrough-enabled.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/esxi-passthrough-enabled.png&raw=1)

Then I rebooted the host and under the **Passthough** column I saw **Active**. I didn't have to do any extra configuration for that. After I rebooted I thought the ESXi was hung cause it just showed the following on the boot up:

> vmkapi_v2_2_0_vmkernel_shim successfully loaded

This is actually expected since the Hypervisor enables the passthough at this point and you won't see the boot up process any more. This was discussed in [stuck after reboot: "vmkapei loaded successfully"](https://communities.vmware.com/thread/470911). I did have SSH enabled on the host and I was able to SSH to the host and confirm it booted up fine and the auto start process started booting up all the VMs.

#### Adding Video Card/GPU to VM
This was pretty easy as well. I just shutdown the VM and then in the Web Client I went to **Virtual Machines** -> **VM** -> **Actions** -> **Edit Settings**. Then added a new PCI Device and selected the Video Card from the drop down list:

![vm-pci-passthrough.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/vm-pci-passthrough.png&raw=1)

After I powered on the Linux VM, I actually still saw the console through Vsphere Web Client and the monitor that was connected to the ESXi host didn't show anything. I then realized the VM now had two Video Cards:

	<> ls -l /dev/dri/
	total 0
	crw-rw---- 1 root video 226,   0 Oct 23 20:41 card0
	crw-rw---- 1 root video 226,   0 Oct 23 20:41 card1
	crw-rw---- 1 root video 226, 128 Oct 23 20:41 renderD128
	crw-rw---- 1 root video 226, 129 Oct 23 20:41 renderD129

and here are the two PCI devices:

	<> lspci | grep VGA
	03:00.0 VGA compatible controller: VMware SVGA II Adapter
	04:00.0 VGA compatible controller: Intel Corporation HD Graphics 530 (rev 06)

#### Disabling Primary Video Card on a VM 
At this point I wanted to make sure the VM only has one Video card. As I was looking around for a way to accomplish this, I ran into a parameter in the **vmx** file called **svga.present**. I also some folks try to use that parameter:

* [Remove virtual SVGA adapter](https://communities.vmware.com/thread/495240)
* [ESXi 6.0 SteamOS Radeon GPU Passthrough](https://www.reddit.com/r/SteamOS/comments/4pwjuj/esxi_60_steamos_radeon_gpu_passthrough/)

So I decided to try it out. **Virtual Machines** -> **VM** -> **Actions** -> **Edit Settings** -> **VM Options** -> **Advanced** -> **Configuration Parameters** -> **Edit Configuration** -> Set **svga.present** to **FALSE**:

![vm-svga-disabled.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/vm-svga-disabled.png&raw=1)

Then after another reboot of the VM, I saw the VM boot up process on the monitor that is connected to the ESXi host and inside the VM only one VGA device showed up:

	<> ls -l /dev/dri/
	total 0
	crw-rw---- 1 root video 226,   0 Oct 23 20:41 card0
	crw-rw---- 1 root video 226, 128 Oct 23 20:41 renderD128

And here is the information on the PCI device:

	<> sudo lspci -v -s  04:00.0
	04:00.0 VGA compatible controller: Intel Corporation HD Graphics 530 (rev 06) (prog-if 00 [VGA controller])
		Subsystem: Hewlett-Packard Company Device 82bf
		Physical Slot: 161
		Flags: bus master, fast devsel, latency 64, IRQ 67
		Memory at fc000000 (64-bit, non-prefetchable) [size=16M]
		Memory at d0000000 (64-bit, prefetchable) [size=256M]
		I/O ports at 7000 [size=64]
		Expansion ROM at <unassigned> [disabled]
		Capabilities: [40] Vendor Specific Information: Len=0c <?>
		Capabilities: [70] Express Endpoint, MSI 00
		Capabilities: [ac] MSI: Enable+ Count=1/1 Maskable- 64bit-
		Capabilities: [d0] Power Management version 2
		Capabilities: [100] Process Address Space ID (PASID)
		Capabilities: [200] Address Translation Service (ATS)
		Capabilities: [300] Page Request Interface (PRI)
		Kernel driver in use: i915
		Kernel modules: i915

Very cool.

### Enabling Hardrware Acceleration on Plex
The original link has all the instructions: 

> 2. Enable hardware acceleration
> To use Hardware-Accelerated Streaming in Plex Media Server, you need to enable it using the Plex Web App.
> 1. Open the Plex Web app.
> 2. Navigate to **Settings** > **Server** > **Transcoder** to access the > server settings.
> 3. Turn on **Show Advanced** in the upper-right corner to expose advanced settings.
> 4. Turn on **Use hardware acceleration when available**.
> 5. Click **Save Changes** at the bottom.
>
> You do not need to restart Plex Media Server after saving the changes.

Not too difficult.

#### Confirming Hardrware Acceleration is utilized
I ran into [Hardware-Accelerated Streaming not working on 64-bit Ubuntu 16.04, i7-3770 and PMS 1.9.5.4339](https://forums.plex.tv/discussion/292921/hardware-accelerated-streaming-not-working-on-64-bit-ubuntu-16-04-i7-3770-and-pms-1-9-5-4339) which show sample logs of HW Acceleration. So when I checked out my logs I saw this:

	<> tail -f Plex\ Media\ Server.log | grep -i hardware
	Oct 23, 2017 20:43:40.341 [0x7fc7a67f8700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:43:40.342 [0x7fc7a67f8700] DEBUG - Codecs: hardware transcoding: opening hw device failed - probably not supported by this system, error: Invalid argument
	Oct 23, 2017 20:43:40.342 [0x7fc7a67f8700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:43:40.342 [0x7fc7a67f8700] DEBUG - Codecs: hardware transcoding: opening hw device failed - probably not supported by this system, error: Invalid argument
	Oct 23, 2017 20:43:40.679 [0x7fc7a6ff9700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:43:40.679 [0x7fc7a6ff9700] DEBUG - Codecs: hardware transcoding: opening hw device failed - probably not supported by this system, error: Invalid argument
	Oct 23, 2017 20:43:40.679 [0x7fc7a6ff9700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:43:40.679 [0x7fc7a6ff9700] DEBUG - Codecs: hardware transcoding: opening hw device failed - probably not supported by this system, error: Invalid argument
	Oct 23, 2017 20:43:41.146 [0x7fc7a8ffd700] DEBUG - TPU: hardware transcoding: enabled, but no hardware decode accelerator found
	Oct 23, 2017 20:43:41.146 [0x7fc7a8ffd700] DEBUG - TPU: hardware transcoding: final decoder: , final encoder:

And also this:

	Oct 23, 2017 20:26:03.083 [0x7fd8b6ffb700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:26:03.083 [0x7fd8b6ffb700] ERROR - [FFMPEG] - No VA display found for device: /dev/dri/renderD128.
	Oct 23, 2017 20:26:03.083 [0x7fd8b6ffb700] DEBUG - Codecs: hardware transcoding: opening hw device failed - probably not supported by this system, error: Invalid argument
	Oct 23, 2017 20:26:03.083 [0x7fd8b6ffb700] ERROR - get - invalid frameRate value: 23.976

#### Adding Plex User to be part of the Video group
I then ran into a couple of posts which had similar logs about the hardware transcoding failing:

* [HW Transcoding not working](https://emby.media/community/index.php?/topic/49019-hw-transcoding-not-working/)
* [trouble with intel hwacc vaapi](https://emby.media/community/index.php?/topic/49513-trouble-with-intel-hwacc-vaapi/)
* [Running Emby with hardware accelerated transcoding in Linux Station](https://forum.qnap.com/viewtopic.php?t=129879)

And they recommended adding the **plex** user to be part of the **video** group. So I did that:

	<> sudo gpasswd -a plex video
	Adding user plex to group video

And restarted the **plex** service:

	<> sudo systemctl restart plexmediaserver.service
	
And after that I saw the following in the logs:

	<> tail -f Plex\ Media\ Server.log | grep -i hardware
	Oct 23, 2017 20:47:12.398 [0x7f1ab27f7700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:47:12.416 [0x7f1ab27f7700] DEBUG - Codecs: hardware transcoding: testing API vaapi
	Oct 23, 2017 20:47:13.159 [0x7f1ab47fb700] DEBUG - TPU: hardware transcoding: using hardware decode accelerator vaapi
	Oct 23, 2017 20:47:13.159 [0x7f1ab47fb700] DEBUG - TPU: hardware transcoding: final decoder: vaapi, final encoder:

And also this:

	Oct 23, 2017 21:27:22.257 [0x7f1aaa7f4700] DEBUG - TPU: hardware transcoding: using hardware decode accelerator vaapi
	Oct 23, 2017 21:27:22.257 [0x7f1aaa7f4700] DEBUG - TPU: hardware transcoding: zero-copy support present
	Oct 23, 2017 21:27:22.257 [0x7f1aaa7f4700] DEBUG - TPU: hardware transcoding: using zero-copy transcoding
	Oct 23, 2017 21:27:22.257 [0x7f1aaa7f4700] DEBUG - TPU: hardware transcoding: final decoder: vaapi, final encoder: vaapi

You will also see **HW** when a video is playing in the Plex Web App:

![plex-web-app-hw-accel.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/plex-web-app-hw-accel.png&raw=1)

### Confirming GPU Utilization
Initially I ran **top** to make sure the CPU is not getting utilized as much. And I did see that when **plex** was transcoding:

![top-low-cpu-transcoder.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/top-low-cpu-transcoder.png&raw=1)

I then ran into a tool called **intel_gpu_top** and that is available with the **intel-gpu-tools** package on *CentOS* 7.

	<> sudo yum provides "*/bin/intel_gpu_top"
	Loaded plugins: fastestmirror, remove-with-leaves
	Loading mirror speeds from cached hostfile
	 * atomic: www3.atomicorp.com
	 * base: mirror.cs.uwp.edu
	 * epel: archive.linux.duke.edu
	 * extras: bay.uchicago.edu
	 * updates: mirror.hmc.edu
	intel-gpu-tools-2.99.917-26.20160929.el7.x86_64 : Debugging tools for Intel
	                                                : graphics chips
	Repo        : base
	Matched from:
	Filename    : /usr/bin/intel_gpu_top

When I ran that tool I did see GPU utilization:

![gpu-top-usage.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/gpu-top-usage.png&raw=1)

Lastly I had a **zabbix** agent collecting CPU information on the box, and here are the results from before:

![zabbix-cpu-before.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/zabbix-cpu-before.png&raw=1)

And here are the results watching the same thing after:

![zabbix-cpu-after.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/plex-hw-accel/zabbix-cpu-after.png&raw=1)

It looks pretty good.