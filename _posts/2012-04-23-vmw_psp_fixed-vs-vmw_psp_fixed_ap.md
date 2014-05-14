---
title: VMW_PSP_FIXED vs. VMW_PSP_FIXED_AP
author: Jarret Lavallee
layout: post
permalink: /2012/04/vmw_psp_fixed-vs-vmw_psp_fixed_ap/
dsq_thread_id:
  - 1404673033
categories:
  - Storage
  - VMware
tags:
  - fixed
  - psa
  - PSP
  - SATP
  - VMW_SATP_FIXED
  - VMW_SATP_FIXED_AP
  - vtip
---
Recently a vendor asked me what the difference between VMW\_PSP\_FIXED and VMW\_PSP\_FIXED\_AP is. Since VMW\_PSP\_FIXED\_AP is not specifically listed on the <a href="http://vmware.com/go/hcl" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmware.com/go/hcl']);" target="_blank">HCL</a>, the vendor was confused on why the SATP had automatically selected VMW\_PSP\_FIXED\_AP instead of VMW\_PSP_FIXED.

VMW\_PSP\_FIXED\_AP was first implemented in ESX/ESXi 4.1 and in 5.x it was merged into the main VMW\_PSP\_FIXED. The difference here is that VMW\_PSP\_FIXED\_AP has added features for <a href="http://www.yellow-bricks.com/2009/09/29/whats-that-alua-exactly/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2009/09/29/whats-that-alua-exactly/']);" target="_blank">ALUA</a>. VMW\_PSP\_FIXED\_AP will act as VMW\_PSP_FIXED when Array Preference is not implemented.

<a href="http://kb.vmware.com/kb/1011340" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1011340']);">PSPs are Path Selection Policies</a>. All that they do is decide which path to use for I/O given a set of paths. These are implemented to be simple as they have to be used with thousands of different arrays. VMW\_PSP\_FIXED and VMW\_PSP\_FIXED_AP use a priority system to determine the path to be used.

VMW\_PSP\_FIXED_AP will use the following criteria when selecting a path.

1. User Preferred Path.  
2. Array Path Preference. If the array does not implement this, this will be skipped.  
3. Current path state.

The great thing about this is that the array should not let the host use an active non-optimized path.

The real difference is that VMW\_PSP\_FIXED does not implement #2 and VMW\_PSP\_FIXED_AP also implements <a href="http://blogs.vmware.com/vsphere/2012/02/configuration-settings-for-alua-devices.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2012/02/configuration-settings-for-alua-devices.html']);" target="_blank">follow-over</a>. Asymmetric state change is explained <a href="http://deinoscloud.wordpress.com/2011/07/04/it-all-started-with-this-question/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://deinoscloud.wordpress.com/2011/07/04/it-all-started-with-this-question/']);" target="_blank">here</a> in much more detail.

