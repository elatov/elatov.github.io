---
title: VCAP5-DCA Objective 3.4 – Utilize Advanced vSphere Performance Monitoring Tools
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-3-4-utilize-advanced-vsphere-performance-monitoring-tools/
dsq_thread_id:
  - 1406889220
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify hot keys and fields used with resxtop/esxtop

If you launch Esxtop and type '**h**' it will show you the following:

![esxtop_shortcuts](https://github.com/elatov/uploads/raw/master/2012/11/esxtop_shortcuts.png)

The most important ones are:

> c = cpu
> m = memory
> n = network
> i = interrupts
> d = disk adapter
> u = disk device (includes NFS as of 4.0 Update 2)
> v = disk VM
> p = power states

For the fields, I would check out [vSphere Monitoring and Performance vSphere 5.0](http://communities.vmware.com/docs/DOC-9279)' documentation. It covers all the fields in great detail. You can also go to each panel from above (cpu, memory... etc) and then type in '**f**' and it will show you the available fields. Here is how the LUN fields look like:

![esxtop_lun_fields](https://github.com/elatov/uploads/raw/master/2012/11/esxtop_lun_fields.png)

### Identify fields used with vscsiStats

From "[Storage Workload Characterization and Consolidation in Virtualized Environments](http://communities.vmware.com/docs/DOC-10104)":

> **Seek distance**: a measure of the spatial locality in the workload measured as the minimum distance in terms of sectors or LBN (logical block number) from among the last k number of IOs (k=1 in the data presented here). In the histograms, small distances signify high locality.
> **IO data length**: in different bins of size 512 Bytes, 1KB,2KB and so on.
> **Interarrival period**: histogram of the time interval (microseconds) between subsequent IO requests.
> **Outstanding IOs**: these denote the IO queue length that the hypervisor sees from a VM.
> **IO latency**: measured for each IO from the time it gets issued by the VM till the VM is interrupted for its completion.
> **Read/Write**: All of these data points are maintained for both reads and writes to clearly show any anomaly in the application’s or device’s behavior towards different request types

### Configure esxtop/resxtop custom profiles

From '[vSphere Monitoring and Performance vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf)':

![esxtop_save_profile](https://github.com/elatov/uploads/raw/master/2012/11/esxtop_save_profile.png)

So launch *esxtop* and configure the fields that you would like to see and then save the configuration by typing "**W**", here is how it looks like:

![esxtop_W](https://github.com/elatov/uploads/raw/master/2012/11/esxtop_W.png)

Select the default file name and now the next time you launch *esxtop* it will start with your custom fields.

### Determine use cases for and apply esxtop/resxtop Interactive, Batch and Replay modes

From '[vSphere Monitoring and Performance vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf)':

> **Using esxtop or resxtop in Interactive Mode**
> By default, resxtop and esxtop run in interactive mode. Interactive mode displays statistics in different panels.
>
> A help menu is available for each panel.
>
> .. ..
>
> **Interactive Mode Single-Key Commands**
> When running in interactive mode, resxtop (or esxtop) recognizes several single-key commands.
>
> All interactive mode panels recognize the commands listed in the following table. The command to specify the delay between updates is disabled if the s option is given on the command line. All sorting interactive commands sort in descending order.

More from the same document:

> **Using Batch Mode**
> Batch mode allows you to collect and save resource utilization statistics in a file.
>
> After you prepare for batch mode, you can use esxtop or resxtop in this mode.
>
> .. ..
>
> In batch mode, resxtop (or esxtop) does not accept interactive commands. In batch mode, the utility runs until it produces the number of iterations requested (see command-line option n, below, for more details), or until you end the process by pressing Ctrl+c.

And the last method of running esxtop:

> **Using Replay Mode**
> In replay mode, esxtop replays resource utilization statistics collected using vm-support.
>
> After you prepare for replay mode, you can use esxtop in this mode. See the vm-support man page.
>
> In replay mode, esxtop accepts the same set of interactive commands as in interactive mode and runs until no more snapshots are collected by vm-support to be read or until the requested number of iterations are completed.
>
> .. ..
>
> **Use esxtop in Replay Mode**
> You can use esxtop in replay mode.
>
> Replay mode can be run to produce output in the same style as batch mode (see the command-line option b,below).
>
> NOTE Batch output from esxtop cannot be played back by resxtop.
>
> Snapshots collected by vm-supported can be replayed by esxtop. However, vm-support output generated by ESXi can be replayed only by esxtop running on the same version of ESXi.

If you are experiencing an issue right now then launch *esxtop* and use interactive mode to figure out what the issue is. If you are unsure what the issue is and you want to look at *esxtop* data as the issue is happening after the issue occurred, use esxtop in replay mode. If the issue happens randomly but you don't know when, then run esxtop in batch mode and then plot the data to see where the issue lies.

### Use vscsiStats to gather storage performance data

There is a very good example [here](http://www.gabesvirtualworld.com/using-vscsistats-the-full-how-to/). Here is summary of the command without the output. List your virtual machines on your host by typing:

    ~# vscsistats -l


Start collecting info for all disks on a virtual machine use the following command:

    ~# vscsistats -s -w WORLD_ID


If you want to collect just for one specific disk on a virtual machine do the following:

    ~# vscsistats -s -w WORLD_ID -i HANDLE_ID


The collection will run for 30 minutes. If you want to stop it type:

    ~# vscsistats -x


During or after collection you can use the **-p** switch to show the collected information:

    ~# vscsistats -p ioLength
    ~# vscsistats -p seekDistance
    ~# vscsistats -p outstandingIOs
    ~# vscsistats -p latency
    ~# vscsistats -p interarrival


Results can be produced in a more compact comma-delimited list by adding the optional "**-c**" to the above:

    ~# /usr/lib/vmware/bin/vscsiStats -p HISTO_TYPE -c


or

    ~# vscsiStats -p all -c -w > /tmp/vmstats-VM_NAME.csv


To reset all counters to zero, run:

    ~# /usr/lib/vmware/bin/vscsiStats -r


### Use esxtop/resxtop to collect performance data

From '[vSphere Monitoring and Performance vSphere 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf)':

> **Use esxtop or resxtop in Batch Mode**
> After you have prepared for batch mode, you can use esxtop or resxtop in this mode.
>
> **Procedure**
>
> 1.  Start resxtop (or esxtop) to redirect the output to a file. For example:
>
>         esxtop -b > my_file.csv
>
>
>     The filename must have a .csv extension. The utility does not enforce this, but the post-processing tools require it.
>
> 2.  Process statistics collected in batch mode using tools such as Microsoft Excel and Perfmon.

Or we can use replay mode:

> **Prepare for Replay Mode**
> To run in replay mode, you must prepare for replay mode. >
> **Procedure**
>
> 1.  Run vm-support in snapshot mode in the ESXi Shell. Use the following command.
>
>         vm-support -S -d duration -I interval
>
>
> 2.  Unzip and untar the resulting tar file so that esxtop can use it in replay mode.
>
> ... ...
>
> **Use esxtop in Replay Mode**
> Procedure
>
> 1.  To activate replay mode, enter the following at the command-line prompt.
>
>         esxtop -R VM-SUPPORT_DIR_PATH
>

