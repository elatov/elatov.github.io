---
published: false
---

### KVM
From the [Virtualization Getting Started Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Virtualization_Getting_Started_Guide/Red_Hat_Enterprise_Linux-6-Virtualization_Getting_Started_Guide-en-US.pdf):

> What is KVM?
>
> KVM (Kernel-based Virtual Machine) is a full virtualization solution for Linux on AMD64 and Intel 64 hardware that is built into the standard Red Hat Enterprise Linux 6 kernel. It can run multiple, unmodified Windows and Linux guest operating systems. The KVM hypervisor in Red Hat Enterprise Linux is managed with the **libvirt** API and tools built for **libvirt** (such as **virt-manager** and **virsh**). Virtual machines are executed and run as multi-threaded Linux processes controlled by these tools.

### Installing The Hypervisor

From the [Hypervisor Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Hypervisor_Deployment_Guide/Red_Hat_Enterprise_Linux-6-Hypervisor_Deployment_Guide-en-US.pdf):

> #### Preparation Instructions
>
> The **rhev-hypervisor** package is needed for installation of Hypervisors. The rhev-hypervisor package contains the Hypervisor CD-ROM image. The following procedure installs the rhev-hypervisor package.
> 
> Entitlements to the **Red Hat Enterprise Virtualization Hypervisor (v.6 x86-64)** channel must be available on your Red Hat Network account to download the Hypervisor image. The channel's label is **rhel-x86_64-server-6-rhevh**.
>
> #### Downloading and Installing the RPM Package
>
> The Red Hat Enterprise Virtualization Hypervisor package contains additional tools for USB and PXE installations as well as the Hypervisor ISO image.
>
> You can download and install the Hypervisor either with **yum** (the recommended approach), or manually. In either case, the Hypervisor ISO image is installed into the **/usr/share/rhev-hypervisor/** directory and named rhev-hypervisor.iso.
>
> The **livecd-iso-to-disk** and **livecd-iso-to-pxeboot** scripts are now included in the livecd-tools sub-package. These scripts are installed to the **/usr/bin** directory.
>
> #### Downloading and installing with yum
>
> 1. Subscribe to the correct channel
>
>  Subscribe to the Red Hat Enterprise Virtualization Hypervisor (v.6 x86_64) channel on Red Hat Network.
>
> 		# rhn-channel --add --channel=rhel-x86_64-server-6-rhevh
>
> 2. Install the Hypervisor
>
> 	Install the rhev-hypervisor package.
>
>		# yum install rhev-hypervisor
>