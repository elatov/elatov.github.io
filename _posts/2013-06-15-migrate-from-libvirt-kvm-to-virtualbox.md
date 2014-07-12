---
title: Migrate from Libvirt KVM to Virtualbox
author: Karim Elatov
layout: post
permalink: /2013/06/migrate-from-libvirt-kvm-to-virtualbox/
dsq_thread_id:
  - 1405505875
categories: ['home_lab', 'os', 'vmware']
tags: ['linux', 'virtualbox', 'kvm', 'libvirt']
---

I was recently trying to migrate some VM from our KVM server to my laptop to run in my VirtualBox install locally. As I was going through the process I realized it's not a very easy process, so I decided to jot down my process. It's probably not perfect, but it worked for me.

### Locate Your KVM VM Managed by *libvirt*

We can use **virsh** for this. First let's list all the VMs that belong to me:

    [elatov@klaptop ~]$ virsh -c qemu+ssh://virtuser@kvm01/system list --all| grep kelatov
     5     kelatov_win7_client2           running
     -     kelatov-child-domain-client    shut off
     -     kelatov-haproxy                shut off
     -     kelatov-win2k8-DC2-Repl        shut off
     -     kelatov-Win2k8-IIS2            shut off
     -     kelatov-Win2k8_DC_Repl         shut off
     -     kelatov_Win2k8-Child_DC        shut off
     -     kelatov_Win2k8-DC2             shut off
     -     kelatov_Win2k8_DC              shut off
     -     kelatov_win7_client1           shut off


I have a lot of them, first let's move the *kelatov_Win2k8-DC2* VM.

### Locate the Disk Image Configured for the VM in *libvirt* KVM

**virsh** is your friend for that as well:

    [elatov@klaptop ~]$ virsh -c qemu+ssh://virtuser@kvm01/system domblklist kelatov_Win2k8-DC2
    Target     Source
    ------------------------------------------------
    hda        /images/kelatov_win2k8r2.img
    hdc        -


So our Disk Image file is under **/images/kelatov_win2k8r2.img**.

### Copy Over the Disk Image File to the Local Machine

Now that we know the location of the disk file, let's copy it over. First let's create a folder and then let's **rsync** the file over:

    [elatov@klaptop ~]$ mkdir vm1
    [elatov@klaptop ~]$ rsync -avzP virtuser@kvm01:/images/kelatov_win2k8r2.img vm1/.
    receiving incremental file list
    kelatov_win2k8r2.img
     21474836480 100%   17.25MB/s    0:19:47 (xfer#1, to-check=0/1)

    sent 30 bytes  received 6353239881 bytes  5350096.77 bytes/sec
    total size is 21474836480  speedup is 3.38


### Generate a *libvirt* Domain XML format Configuration of the KVM VM

**libvirt** uses a special XML format file to keep track of all the configurations for a VM. All the specifics of the XML file are [here](http://libvirt.org/formatdomain.html). Using **virsh**, generating the file is a breeze:

    [elatov@klaptop ~]$ cd vm1/
    [elatov@klaptop vm1]$ virsh -c qemu+ssh://virtuser@kvm01/system dumpxml kelatov_Win2k8-DC2 > kelatov_Win2k8-DC2.xml


The file is pretty long, but just checking the top of the file, we should see something like this:

    [elatov@klaptop vm1]$ head kelatov_Win2k8-DC2.xml
    <domain type='kvm'>
      <name>kelatov_Win2k8-DC2</name>
      <uuid>b5188795-2be0-b229-7538-0fe7f2e930a3</uuid>
      <memory>1048576</memory>
      <currentmemory>1048576</currentmemory>
      <vcpu>1</vcpu>
      <os>
        <type arch='x86_64' machine='rhel6.2.0'>hvm</type>
        <boot dev='hd'></boot>
      </os>


*libvirt* keeps the configuration XML file under **/etc/libvirt/qemu** as well:

    [virtuser@kvm01 ~]$ head /etc/libvirt/qemu/kelatov_Win2k8-DC2.xml
    <!--
    WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
    OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
      virsh edit kelatov_Win2k8-DC2
    or other application using the libvirt API.
    -->

    </domain><domain type='kvm'>
      <name>kelatov_Win2k8-DC2</name>
      <uuid>b5188795-2be0-b229-7538-0fe7f2e930a3</uuid>


So if you really wanted to, you could just **rsync** that file.

### Convert RAW Format Disk Image (.img) to VMDK

Now that we have all the files:

    [elatov@klaptop vm1]$ ls -1
    kelatov_Win2k8-DC2.xml
    kelatov_win2k8r2.img


Let's create an OVF file, so we can import it into VirtualBox. To do this, first we will need to convert our disk image to VMDK format. You can use **qemu-img** to find out the exact format of the disk image file:

    [elatov@klaptop vm1]$ qemu-img info kelatov_win2k8r2.img
    image: kelatov_win2k8r2.img
    file format: raw
    virtual size: 20G (21474836480 bytes)
    disk size: 20G


So we are currently in **RAW** format. Here is the command we can use to convert it to VMDK format:

    [elatov@klaptop vm1]$ qemu-img convert -O vmdk kelatov_win2k8r2.img kelatov_win2k8r2.vmdk -p
        (100.00/100%)


### Convert Domain XML Format Configuration File to libvirt "image" XML Configuration File (virt-image)

For some reason, the **virt-image** and **virt-convert** commands can only convert from the image XML Descriptor file. From the **virt-image** man page:

    virt-image is a command line tool for creating virtual machines from an
           XML image descriptor "IMAGE.XML" (virt-image(5)). Most attributes of
           the virtual machine are taken from the XML descriptor (e.g., where the
           files to back the virtual machine's disks are and how to map them into
           the guest), though certain information must be added on the command
           line, such as the name of the guest.

           The XML descriptor defines most attributes of the guest, making it
           possible to bundle and distribute it together with the files backing
           the guest's disks.


And here is the section from **virt-convert**:

     Conversion Options
           -i format
             Input format. Currently, "vmx", "virt-image", and "ovf" are
             supported.


There have been other people wondering how to convert libvirt domain XML file into other formats like the XML image format (virt-image), VMware VMX, or even OVF. Here are some forums that talk about it:

*   [virt-convert from libvirt to vmware](http://www.redhat.com/archives/virt-tools-list/2010-April/msg00023.html)
*   [[libvirt] Intend to add OVA installation API](http://www.redhat.com/archives/libvir-list/2012-June/msg01012.html)
*   [[libvirt-users] using virsh (or something) to convert from KVM domain XML to vmx...](https://www.redhat.com/archives/libvirt-users/2011-September/msg00042.html)
*   [[fedora-virt] exporting a vm image](http://lists.fedoraproject.org/pipermail/virt/2010-August/002220.html)

but none of the above have been resolved yet.

There is a script that goes from **vmx** to *libvirt* domain XML format: [Virtualization Preview Repository](http://bazaar.launchpad.net/~ubuntu-virt/virt-goodies/trunk/files)". After you install the new **libvirt-client** tools you can then run commands against an ESX host:

    [elatov@klaptop ~]$ virsh -c esx://vmware01/?no_verify=1 dumpxml kelatov-2
    Enter username for vmware01 [root]:
    Enter root's password for vmware01:
    </domain><domain type='vmware'>
      <name>kelatov-2</name>
      <uuid>564d3355-1ee8-ce81-00fa-ef6c1a767850</uuid>
      <memory unit='KiB'>4194304</memory>
      <currentmemory unit='KiB'>4194304</currentmemory>
      <vcpu placement='static'>2</vcpu>
      <os>
        <type arch='x86_64'>hvm</type>
      </os>
      <clock offset='utc'></clock>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>destroy</on_crash>
      <devices>
        <disk type='file' device='disk'>
          <source file='[images] kelatov-2/kelatov-2.vmdk'/>
          <target dev='sda' bus='scsi'></target>
          <address type='drive' controller='0' bus='0' target='0' unit='0'></address>
        </disk>
        <disk type='block' device='cdrom'>
          <source dev='cdrom1'/>
          <target dev='hda' bus='ide'></target>
          <address type='drive' controller='0' bus='0' target='0' unit='0'></address>
        </disk>
        <controller type='scsi' index='0' model='lsilogic'></controller>
        <controller type='ide' index='0'></controller>
        <interface type='bridge'>
          <mac address='00:0c:29:76:78:50'></mac>
          <source bridge='net1'/>
          <model type='e1000'></model>
        </interface>
        <video>
          <model type='vmvga' vram='4096'></model>
        </video>
      </devices>
    </domain>


So if I had started out with ESX and was trying to go to KVM that would have been pretty easy (but at least now I can use **virsh** to query an ESX server). Since no solution has been found, I decided to write my own python script that converts from libvirt Domain XML format to virt-image (XML Image Descriptor) XML format. The format of the XML image descriptor is seen [here](http://manpages.ubuntu.com/manpages/hardy/man5/virt-image.5.html). Here is an example of the format:

     < ?xml version="1.0" encoding="UTF-8"?>
               <image>
                 <name>sysresccd</name>
                 <domain>
                   <boot type="hvm">
                     <guest>
                       <arch>i686</arch>
                     </guest>
                     <os>
                       <loader dev="cdrom"></loader>
                     </os>
                     <drive disk="root.raw" target="hda"></drive>
                     <drive disk="sysresc"></drive>
                   </boot>
                   <devices>
                     <vcpu>1</vcpu>
                     <memory>262144</memory>
                     <interface></interface>
                     <graphics></graphics>
                   </devices>
                 </domain>
                 <storage>
                   <disk file="root.raw" use="scratch" size="100" format="raw"></disk>
                   <disk id="sysresc" file="isos/systemrescuecd.iso"
                         use="system" format="iso"></disk>
                 </storage>
               </image>


Here is what I came up with:

    [elatov@klaptop vm1]$ cat dom2img.py
    #!/usr/bin/env python
    from xml.dom import minidom
    from xml.dom.minidom import Document
    import sys

    # Read in first arguement
    input_file = sys.argv[1]

    # parse our XML file
    xml = minidom.parse(input_file)

    # Get the DomainName or the VM Name
    domainName = xml.getElementsByTagName('name')
    domain_name = domainName[0].childNodes[0].nodeValue

    # Get the hypervisor Type
    domainHType = xml.getElementsByTagName('type')
    h_type = domainHType[0].childNodes[0].nodeValue

    # Get the Arch and OS
    domainOSInfo = xml.getElementsByTagName('type')
    for i in domainOSInfo:
        domain_arch = i.getAttribute('arch')
        domain_os = i.getAttribute('machine')

    # Get Boot Device Type
    domainBootDevType = xml.getElementsByTagName('boot')
    for i in domainBootDevType:
        boot_dev_type = i.getAttribute('dev')

    # Get disk Device location
    for node in xml.getElementsByTagName("disk"):
        if node.getAttribute("device") == "disk":
            source = node.getElementsByTagName('source')
            for s in source:
                disk_loc = s.getAttribute('file')

    # Get Boot Device
    mapping = {}
    for node in xml.getElementsByTagName("disk"):
        dev = node.getAttribute("device")
        target = node.getElementsByTagName('target')
        for t in target:
            mapping[dev] = t.getAttribute('dev')

    if boot_dev_type == 'hd':
        boot_dev = mapping['disk']
    elif boot_dev_type == 'cdrom':
        boot_dev = mapping['cdrom']

    # Get amount of CPUS
    domainVCPUs = xml.getElementsByTagName('vcpu')
    vcpu_count = domainVCPUs[0].childNodes[0].nodeValue

    # Get amount of RAM
    domainMemory = xml.getElementsByTagName('memory')
    memory = domainMemory[0].childNodes[0].nodeValue

    # Create an empty XML Document
    doc = Document()

    # Create the "image" element
    image = doc.createElement("image")
    doc.appendChild(image)

    # Create the Name Element
    name_element = doc.createElement("name")
    image.appendChild(name_element)
    name_text = doc.createTextNode(domain_name)
    name_element.appendChild(name_text)

    # Create the Label Element
    label_element = doc.createElement("label")
    image.appendChild(label_element)
    label_text = doc.createTextNode(domain_name)
    label_element.appendChild(label_text)

    # Create the Description Element
    desc_element = doc.createElement("description")
    image.appendChild(desc_element)
    desc_text = doc.createTextNode(domain_os)
    desc_element.appendChild(desc_text)

    # Create the Domain Element
    domain_element = doc.createElement("domain")
    image.appendChild(domain_element)

    # Create boot element
    boot_element = doc.createElement("boot")
    boot_element.setAttribute("type",h_type )
    domain_element.appendChild(boot_element)

    # Create guest Element
    guest_element = doc.createElement("guest")
    boot_element.appendChild(guest_element)

    # Create the arch attribute
    arch_element = doc.createElement("arch")
    guest_element.appendChild(arch_element)
    arch_text = doc.createTextNode(domain_arch)
    arch_element.appendChild(arch_text)

    # Create OS Element
    os_element = doc.createElement("os")
    boot_element.appendChild(os_element)

    # Create the loader element and set the dev attribute
    loader_element = doc.createElement("loader")
    loader_element.setAttribute("dev",boot_dev_type)
    os_element.appendChild(loader_element)

    # Create drive element and set it's attributes
    drive_element = doc.createElement("drive")
    drive_element.setAttribute("disk", disk_loc)
    drive_element.setAttribute("target", boot_dev)
    boot_element.appendChild(drive_element)

    # Create device Element
    devices_element = doc.createElement("devices")
    domain_element.appendChild(devices_element)

    # Create VCPU text
    vcpu_element = doc.createElement("vcpu")
    devices_element.appendChild(vcpu_element)
    vcpu_text = doc.createTextNode (vcpu_count)
    vcpu_element.appendChild(vcpu_text)

    # Create Memory text
    memory_element = doc.createElement("memory")
    devices_element.appendChild(memory_element)
    memory_text = doc.createTextNode(memory)
    memory_element.appendChild(memory_text)

    # Create interface element
    interface_element = doc.createElement("interface")
    devices_element.appendChild(interface_element)

    # Create graphics element
    graphics_element = doc.createElement("graphics")
    devices_element.appendChild(graphics_element)

    # Create storage element
    storage_element = doc.createElement("storage")
    image.appendChild(storage_element)

    # create disk element and set it's attributes
    disk_element = doc.createElement("disk")
    disk_element.setAttribute("file",disk_loc)
    disk_element.setAttribute("format","vmdk")
    disk_element.setAttribute("use","system")
    storage_element.appendChild(disk_element)

    f = open(input_file + '_converted', 'w')
    f.write (doc.toprettyxml(indent=" ",encoding="utf-8"))
    f.close()


It basically takes in one argument, the domain XML file to be converted, and produces a new file with "converted" appended to the original filename. Here is what I did to run the conversion:

    [elatov@klaptop vm1]$ ./dom2img.py kelatov_Win2k8-DC2.xml


Now to check out both files, here is the original:

    [elatov@klaptop vm1]$ head kelatov_Win2k8-DC2.xml
    <domain type='kvm'>
      <name>kelatov_Win2k8-DC2</name>
      <uuid>b5188795-2be0-b229-7538-0fe7f2e930a3</uuid>
      <memory>1048576</memory>
      <currentmemory>1048576</currentmemory>
      <vcpu>1</vcpu>
      <os>
        <type arch='x86_64' machine='rhel6.2.0'>hvm</type>
        <boot dev='hd'></boot>
      </os>


And here is the converted one:

    [elatov@klaptop vm1]$ head kelatov_Win2k8-DC2.xml_converted
    < ?xml version="1.0" encoding="utf-8"?>
    <image>
     <name>kelatov_Win2k8-DC2</name>
     <label>kelatov_Win2k8-DC2</label>
     <description>rhel6.2.0</description>
     <domain>
      <boot type="hvm">
       <guest>
        <arch>x86_64</arch>
       </guest>
       <os>


### Convert XML Image Descriptor to VMX

Luckily **virt-convert** can handle this:

    [elatov@klaptop vm1]$ virt-convert -i virt-image kelatov_Win2k8-DC2.xml_converted -o vmx kelatov_Win2k8-DC2.vmx
    Generating output in 'vmx' format to /home/elatov/vm1/
    Converting disk '/images/kelatov_win2k8r2.img' to type vmdk...
    Done.


Now checking out the VMX file:

    [elatov@klaptop vm1]$ head -20 kelatov_Win2k8-DC2.vmx

    #!/usr/bin/vmplayer

    # Generated by virt-convert
    # http://virt-manager.org/

    # This is a Workstation 5 or 5.5 config file and can be used with Player
    config.version = "8"
    virtualHW.version = "4"
    guestOS = "other"
    displayName = "kelatov_Win2k8-DC2"
    annotation = "rhel6.2.0"
    guestinfo.vmware.product.long = "kelatov_Win2k8-DC2"
    guestinfo.vmware.product.url = "http://virt-manager.org/"
    guestinfo.vmware.product.class = "virtual machine"
    numvcpus = "1"
    memsize = "1024"
    MemAllowAutoScaleDown = "FALSE"
    MemTrimRate = "-1"
    uuid.action = "create"


That doesn't look too bad.

### Create OVF from VMX and VMDK

Let's first fix the disk location, right now it's still pointing to the **.img** file:

    [elatov@klaptop vm1]$ grep img kelatov_Win2k8-DC2.vmx
    ide0:0.fileName = "/images/kelatov_win2k8r2.img"


Since the VMDK is located in the same directory:

    [elatov@klaptop vm1]$ ls -1
    dom2img.py
    kelatov_Win2k8-DC2.vmx
    kelatov_Win2k8-DC2.xml
    kelatov_Win2k8-DC2.xml_converted
    kelatov_win2k8r2.img
    kelatov_win2k8r2.vmdk


Let's edit the VMX file:

    [elatov@klaptop vm1]$ vi kelatov_Win2k8-DC2.vmx


and fix the location to be relative to the current directory:

    [elatov@klaptop vm1]$ grep vmdk kelatov_Win2k8-DC2.vmx
    ide0:0.fileName = "kelatov_win2k8r2.vmdk"


That looks good, now let's create the OVF. More information regarding installing and using **ovftool** is seen at "[Migrating a VM from VMware Workstation to Oracle VirtualBox](/2013/04/migrating-a-vm-from-vmware-workstation-to-oracle-virtualbox/)". Here is the command I ran to create our OVF:

    [elatov@klaptop vm1]$ ovftool kelatov_Win2k8-DC2.vmx kelatov_Win2k8-DC2.ovf
    Opening VMX source: kelatov_Win2k8-DC2.vmx
    Opening OVF target: kelatov_Win2k8-DC2.ovf
    Writing OVF package: kelatov_Win2k8-DC2.ovf
    Transfer Completed
    Completed successfully


After it was done, I had the following files:

    [elatov@klaptop vm1]$ ls -rt1
    kelatov_win2k8r2.img
    kelatov_Win2k8-DC2.xml
    kelatov_win2k8r2.vmdk
    kelatov_Win2k8-DC2.xml_converted
    dom2img.py
    kelatov_Win2k8-DC2.vmx
    kelatov_Win2k8-DC2-disk1.vmdk
    kelatov_Win2k8-DC2.ovf
    kelatov_Win2k8-DC2.mf


The bottom 3 files were created by the OVF creation process.

### Import OVF into VirtualBox

Doing a VirtualBox dry-run import, I saw the following:

    [elatov@klaptop vm1]$ VBoxManage import -n kelatov_Win2k8-DC2.ovf
    0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
    Interpreting /home/elatov/vm1/kelatov_Win2k8-DC2.ovf...
    OK.
    Disks:  vmdisk1 20  17550934016 http://www.vmware.com/interfaces/specifications/vmdk.html#streamOptimized   kelatov_Win2k8-DC2-disk1.vmdk   6997323776  -1
    Virtual system 0:
     0: Suggested OS type: "Other"
        (change with "--vsys 0 --ostype <type>"; use "list ostypes" to list all possible values)
     1: Suggested VM name "vm"
        (change with "--vsys 0 --vmname <name>")
     2: Description "rhel6.2.0"
        (change with "--vsys 0 --description <desc>")
     3: Number of CPUs: 1
        (change with "--vsys 0 --cpus <n>")
     4: Guest memory: 1024 MB
        (change with "--vsys 0 --memory <mb>")
     5: Network adapter: orig nat, config 2, extra type=nat
     6: IDE controller, type PIIX4
        (disable with "--vsys 0 --unit 6 --ignore")
     7: Hard disk image: source image=kelatov_Win2k8-DC2-disk1.vmdk, target path=/home/elatov/.virt/vm/kelatov_Win2k8-DC2-disk1.vmdk, controller=6;channel=0
        (change target path with "--vsys 0 --unit 7 --disk path";
        disable with "--vsys 0 --unit 7 --ignore")


I liked the outcome: memory, CPU, and hard disk information was correct. I decided to run the import and at the same time I changed the OS type and the name. Here is how the whole process looked like:

    [elatov@klaptop vm1]$ VBoxManage import kelatov_Win2k8-DC2.ovf --vsys 0 --ostype Windows2008_64 --vsys 0 --vmname kelatov_win2k8_DC
    0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
    Interpreting /home/elatov/vm1/kelatov_Win2k8-DC2.ovf...
    OK.
    Disks:  vmdisk1 20  17550934016 http://www.vmware.com/interfaces/specifications/vmdk.html#streamOptimized   kelatov_Win2k8-DC2-disk1.vmdk   6997323776  -1
    Virtual system 0:
     0: OS type specified with --ostype: "Windows2008_64"
     1: VM name specified with --vmname: "kelatov_win2k8_DC"
     2: Description "rhel6.2.0"
        (change with "--vsys 0 --description <desc>")
     3: Number of CPUs: 1
        (change with "--vsys 0 --cpus <n>")
     4: Guest memory: 1024 MB
        (change with "--vsys 0 --memory <mb>")
     5: Network adapter: orig nat, config 2, extra type=nat
     6: IDE controller, type PIIX4
        (disable with "--vsys 0 --unit 6 --ignore")
     7: Hard disk image: source image=kelatov_Win2k8-DC2-disk1.vmdk, target path=/home/elatov/.virt/vm/kelatov_Win2k8-DC2-disk1.vmdk, controller=6;channel=0
        (change target path with "--vsys 0 --unit 7 --disk path";
        disable with "--vsys 0 --unit 7 --ignore")
    0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
    Successfully imported the appliance.


I then launched VirtualBox and powered on the VM, it booted without any issues:

![successful boot after migration Migrate from Libvirt KVM to Virtualbox](https://github.com/elatov/uploads/raw/master/2013/05/successful_boot_after_migration.png)

<root>
</root>

