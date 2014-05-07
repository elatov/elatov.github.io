---
title: Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0
author: Karim Elatov
layout: post
permalink: /2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/
dsq_thread_id:
  - 1405152269
categories:
  - Home Lab
  - OS
  - Storage
  - VMware
tags:
  - apt-xapian-index
  - esxtop
  - io latency
  - iostat
  - ubuntu
---
I have a lab environment where I deploy about 30 VMs on one physical server and run Linux (Ubuntu 11.10) on all the VMs. Here are the specs of the physical machine:

[code]~ # vsish -e cat /hardware/bios/dmiInfo | head -4  
System Information (type1) {  
Product Name:Seabream  
Vendor Name:InventecESC  
Serial Number:P1237010411

~ # vsish -e cat /hardware/cpu/cpuInfo | grep -E 'Number\ of \cores|Number\ of\ CPU'  
Number of cores:8  
Number of CPUs (threads):8

~ # vsish -e cat /hardware/cpu/cpuModelName  
Intel(R) Xeon(R) CPU X5355 @ 2.66GHz

~ # vsish -e cat /memory/comprehensive | head -2  
Comprehensive {  
Physical memory estimate:8388084 KB[/code]

So 8 cores at 2.66GHz and 8GB of RAM, nothing crazy. Each VM has the minimum amount of RAM (192MB) and it actually runs pretty well. I was looking over esxtop and at random period of times, I saw different VMs experiencing high latency. Here is what I saw.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/esxtop_latency.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/esxtop_latency.png']);"><img class="alignnone size-full wp-image-545" title="esxtop_latency" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/esxtop_latency.png" alt="esxtop latency Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0" width="927" height="686" /></a>

To get to this screen just launch esxtop and hit &#8216;v&#8217; for &#8220;disk VMs&#8221;. On ESXi 5.0 the latency is automatically displayed in this view. If you are on 4.x, after selecting &#8216;v&#8217; you can type in &#8216;f&#8217; and that will show you a list of available columns, select the latency columns and you will see the same as above. From the above picture we see VM &#8220;uaclass39&#8243; and &#8220;uaclass17&#8243; experiencing latency up to 20 milliseconds. At certain times 20 VMs would experience the same issue. I saw this lantency be steady for a couple of minutes. More information regarding latency can be seen at this communities page (<a href="http://communities.vmware.com/docs/DOC-11812" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-11812']);">Interpreting esxtop 4.1 Statistics</a>). It has a terrific picture (Section 4.2.2 Latency Statistics) regarding the different layers which can experience latency. The above picture shows the latency experienced by the VM. Another great article that helps with troubleshooting disk latency is &#8220;<a href="http://communities.vmware.com/servlet/JiveServlet/downloadBody/14905-102-1-17952/vsphere41-performance-troubleshooting.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://communities.vmware.com/servlet/JiveServlet/downloadBody/14905-102-1-17952/vsphere41-performance-troubleshooting.pdf']);">Performance Troubleshooting for VMware vSphere™ 4.1</a>&#8220;, check out the section entitled &#8217;7.3.13. Check for Slow or Under-Sized Storage Device&#8217;.

I decided to take a look at what the VM is doing and why it was experiencing such high read and write latency. So I ssh&#8217;ed over to one of the VMs and I launched top, and here is I saw:<a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/Ubuntu_11_10_top.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/Ubuntu_11_10_top.png']);"><img class="alignnone size-full wp-image-546" title="Ubuntu_11_10_top" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/Ubuntu_11_10_top.png" alt="Ubuntu 11 10 top Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0" width="879" height="163" /></a>

Check out the %wa (it&#8217;s 97%). Looking at the man page of &#8216;top&#8217;, I see the following:

[code]  
wa -- iowait  
Amount of time the CPU has been waiting for I/O to complete.  
[/code]

Something is doing a lot of IO and the biggest cpu and memory user is a process called update-apt-xapi. Looking at the man page of &#8216;ps&#8217;, I see the folllowing:

[code]  
PROCESS STATE CODES  
Here are the different values that the s, stat and state output  
specifiers (header "STAT" or "S") will display to describe the state of  
a process:  
D uninterruptible sleep (usually IO)  
R running or runnable (on run queue)  
S interruptible sleep (waiting for an event to complete)  
T stopped, either by a job control signal or because it is being  
traced.  
W paging (not valid since the 2.6.xx kernel)  
X dead (should never be seen)  
Z defunct ("zombie") process, terminated but not reaped by its  
parent.  
[/code]

I wanted to check what is in disk IO state, so I ran the below:

[code]root@uaclass39:~# ps -efly | grep ^D  
D root 1570 1 3 90 10 137492 58296 sleep_ 16:54 ? 00:00:15 /usr/bin/python /usr/sbin/update-apt-xapian-index --force --quiet[/code]

So it looks like the &#8220;update-apt-xapian-index&#8221; is what&#8217;s causing the high disk IO. I then wanted to check how much IO was happening, so I ran the following:

[code]  
root@uaclass39:~# iostat 1 5 /dev/sda  
Linux 3.0.0-17-virtual (uaclass39) 03/29/2012 \_x86\_64_ (1 CPU)

avg-cpu: %user %nice %system %iowait %steal %idle  
1.03 2.09 1.94 44.96 0.00 49.99

Device: tps kB\_read/s kB\_wrtn/s kB\_read kB\_wrtn  
sda 169.03 5636.54 312.89 7418419 411800

avg-cpu: %user %nice %system %iowait %steal %idle  
0.00 1.98 2.97 95.05 0.00 0.00

Device: tps kB\_read/s kB\_wrtn/s kB\_read kB\_wrtn  
sda 609.90 16419.80 91.09 16584 92

avg-cpu: %user %nice %system %iowait %steal %idle  
0.00 2.00 2.00 96.00 0.00 0.00

Device: tps kB\_read/s kB\_wrtn/s kB\_read kB\_wrtn  
sda 563.00 14884.00 40.00 14884 40

avg-cpu: %user %nice %system %iowait %steal %idle  
0.97 1.94 0.97 96.12 0.00 0.00

Device: tps kB\_read/s kB\_wrtn/s kB\_read kB\_wrtn  
sda 779.61 20749.51 38.83 21372 40

avg-cpu: %user %nice %system %iowait %steal %idle  
0.00 7.69 1.92 90.38 0.00 0.00

Device: tps kB\_read/s kB\_wrtn/s kB\_read kB\_wrtn  
sda 658.65 15638.46 319.23 16264 332  
[/code]

We consistently see very high %iowait and our reads are at ~15-20MB/s. Don&#8217;t forget this is on local storage too <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0" class="wp-smiley" title="Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0" />  
I wanted to find out what this apt-xapian process is, I did some research and I found a bug (<a href="https://bugs.launchpad.net/ubuntu/+source/apt-xapian-index/+bug/363695" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://bugs.launchpad.net/ubuntu/+source/apt-xapian-index/+bug/363695']);">363695</a>) from ubuntu. They tried to fix it by throttling the IO by using ionice, my install had that enabled:

[code]  
root@uaclass39:/etc/cron.weekly# grep -i ionice apt-xapian-index  
\# ionice should not be called in a virtual environment  
egrep -q '(envID|VxID):.*[1-9]' /proc/self/status || IONICE=/usr/bin/ionice  
if [ -x "$IONICE" ]  
nice -n 19 $IONICE -c 3 $CMD --quiet  
[/code]

but it still caused an issue and it states that ionice should not be used in a virtualized environment. So I decided to just disable it. Since I had setup ssh keys for grading purposes, I wrote this script to disable apt-xapian-index from auto running weekly:

[code]  
#!/bin/bash

HOSTS="uaclass01 uaclass02 uaclass03 ..."

for i in $HOSTS;do  
echo $i  
/usr/bin/ssh $i '/bin/chmod 0 /etc/cron.weekly/apt-xapian-index'  
done  
[/code]

A more appropriate fix would be to completely remove the package:

[code]  
root@uaclass39:~$ dpkg -l | grep apt-xapian  
ii apt-xapian-index 0.44ubuntu4 maintenance and search tools for a Xapian index of Debian packages

root@uaclass39:~$ apt-get --purge remove apt-xapian-index  
Reading package lists... Done  
Building dependency tree  
Reading state information... Done  
The following packages will be REMOVED:  
apt-xapian-index*  
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.  
After this operation, 483 kB disk space will be freed.  
Do you want to continue [Y/n]? Y  
(Reading database ... 28747 files and directories currently installed.)  
Removing apt-xapian-index ...  
Removing index /var/lib/apt-xapian-index...  
Purging configuration files for apt-xapian-index ...  
Removing index /var/lib/apt-xapian-index...  
Processing triggers for man-db ...  
[/code]

But I didn&#8217;t want to do that just yet. Just as an FYI, here are the spec of each VM:

[code]  
root@uaclass39:~# uname -a  
Linux uaclass39 3.0.0-17-virtual #30-Ubuntu SMP Thu Mar 8 23:45:51 UTC 2012 x86\_64 x86\_64 x86_64 GNU/Linux

root@uaclass39:~# lsb_release -a  
No LSB modules are available.  
Distributor ID: Ubuntu  
Description: Ubuntu 11.10  
Release: 11.10  
Codename: oneiric

root@uaclass39:~# free -m  
total used free shared buffers cached  
Mem: 176 167 8 0 10 107  
-/+ buffers/cache: 50 126  
Swap: 379 35 344

root@uaclass39:~# x86info  
x86info v1.25. Dave Jones 2001-2009

Found 1 CPU  
\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\-----  
EFamily: 0 EModel: 0 Family: 6 Model: 15 Stepping: 7  
CPU Model: Core 2 Quad (Kentsfield)  
Processor name string: Intel(R) Xeon(R) CPU X5355 @ 2.66GHz  
Type: 0 (Original OEM) Brand: 0 (Unsupported)  
Number of cores per physical package=1  
Number of logical processors per socket=1  
Number of logical processors per core=1  
APIC ID: 0x0 Package: 0 Core: 0 SMT ID 0

[/code]

Since the apt-xapian-index just indexes all the aptitude packages, I didn&#8217;t really see a problem with disabling it. After I disabled that cron job, I haven&#8217;t seen any high latency on any of the VMs.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive" href="http://virtuallyhyper.com/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/']);" rel="bookmark">Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Plot Esxtop Data With gnuplot" href="http://virtuallyhyper.com/2013/01/plot-esxtop-data-with-gnuplot/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/plot-esxtop-data-with-gnuplot/']);" rel="bookmark">Plot Esxtop Data With gnuplot</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VMs are Slow to Boot from an HP MSA 2000 Array" href="http://virtuallyhyper.com/2012/11/vms-are-slow-to-boot-from-an-hp-msa-2000-array/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/vms-are-slow-to-boot-from-an-hp-msa-2000-array/']);" rel="bookmark">VMs are Slow to Boot from an HP MSA 2000 Array</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Seeing High KAVG with Microsoft Cluster Services  (MSCS) RDMs" href="http://virtuallyhyper.com/2012/08/seeing-high-kavg-with-microsoft-cluster-services-mscs-rdms/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/seeing-high-kavg-with-microsoft-cluster-services-mscs-rdms/']);" rel="bookmark">Seeing High KAVG with Microsoft Cluster Services (MSCS) RDMs</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/" title=" Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:apt-xapian-index,esxtop,io latency,iostat,ubuntu,blog;button:compact;">I came across an interesting issue the other day. I would randomly see high KAVG and QAVG on my ESX hosts. It would look something like this: We can see...</a>
</p>