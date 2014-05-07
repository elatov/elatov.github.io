---
title: 'Snapshots Take a Long Time When &#8220;Keep Memory&#8221; is Enabled'
author: Jarret Lavallee
layout: post
permalink: /2013/04/snapshots-take-a-long-time-when-keep-memory-is-checked/
dsq_thread_id:
  - 1405434180
categories:
  - Storage
  - VMware
tags:
  - Lazy CheckPoint
  - Memory snapshots
  - VMware Snapshots
---
When taking a snapshot with memory, the VM may be unresponsive and the snapshot may take a long time to complete. This is because the ESX host has to dump the VM&#8217;s memory to disk.

When looking in the **vmware.log** file, we will notice that during the snapshot creation something called **Lazy CheckPointing** is utilized. **Lazy CheckPointing** is a feature that allows the VM to continue running while the memory is dumped. It would otherwise have to stop the VM and dump the complete contents of the memory to disk. Instead of completely disrupting operations on the VM, the ESX host can leave the VM running with degraded performance. This **Lazy CheckPointing** mechanism takes a significant amount of time, and as a result we experience degraded performance for a prolonged period of time (this scales with the amount of memory assigned to the VM).

There are 2 options in the *VMX* file that we can use to tune this:

*   **mainMem.ioWait**
*   **mainMem.ioBlockPages**

For some reason they are not well documented. You *may* be able to tune these to get better performance with the following parameters **mainMem.ioBlockPages** and **mainMem.ioWait** in the *VMX* file. You will have to experiment with the values.

First, I got a benchmark with the default parameters configured.

    # grep mainMem vps.vmx 
    # 
    
    # grep -i lazy vmware.log 
    2012-07-27T17:39:45.992Z| Worker#0| MainMem: Begin lazy IO (1048576 pages, 0 done, 1 threads, bio = 0). 
    2012-07-27T17:45:19.942Z| Worker#0| MainMem: End lazy IO (1048576 done, sync = 0, error = 0). 
    2012-07-27T17:45:19.961Z| vmx| MainMem: Completed pending lazy checkpoint save. 
    

The lazy snapshot took over 5 minutes to complete. This is a long time to dump the memory, so I configured the following parameters.

    # grep mainMem vps.vmx 
    mainMem.ioBlockPages = "2048" 
    mainMem.iowait = "2" 
    

I took a memory snapshot and took a look in the **vmware.log** file

    # grep -i lazy vmware.log 
    2012-07-27T17:35:32.793Z| Worker#0| MainMem: Begin lazy IO (1048576 pages, 0 done, 1 threads, bio = 0). 
    2012-07-27T17:36:56.674Z| Worker#0| MainMem: End lazy IO (1048576 done, sync = 0, error = 0). 
    2012-07-27T17:36:56.691Z| vmx| MainMem: Completed pending lazy checkpoint save. 
    

The **Lazy CheckPointing** took 1 minute and 24 seconds, which saves me about 4 minutes.

By default **mainMem.ioBlockPages** is set to 64 pages. Each page is 4k, so 64 would be 256k and 2048 pages would be 8MB. The **ioWait** is set to 25ms by default. The array will preform differently with different write sizes, so you should test to see what works best for your environment.

The way it works is **Lazy CheckPointing** iterates through the memory and writes it to disk. Each iteration of the lazy page-walker writes **mainMem.ioBlockPages** pages and then waits **mainMem.ioWait** milliseconds until the next iteration. For 4GB of memory and the default of 64 pages (256k) it would take 16384 iterations waiting 25ms between iterations. So 25ms * 16384 iterations = ~6 minutes.

By increasing the **ioBlockPages** and decreasing the **ioWait** values, we can cut down on both the number of iterations and waiting time ( which in turn will decrease the total time to dump the memory to disk).

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/04/snapshots-take-a-long-time-when-keep-memory-is-checked/" title=" Snapshots Take a Long Time When &#8220;Keep Memory&#8221; is Enabled" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Lazy CheckPoint,Memory snapshots,VMware Snapshots,blog;button:compact;">When taking a snapshot with memory, the VM may be unresponsive and the snapshot may take a long time to complete. This is because the ESX host has to dump...</a>
</p>