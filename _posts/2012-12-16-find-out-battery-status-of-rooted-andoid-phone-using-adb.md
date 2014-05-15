---
title: Find Out Battery Status of Rooted Andoid Phone Using ADB
author: Karim Elatov
layout: post
permalink: /2012/12/find-out-battery-status-of-rooted-andoid-phone-using-adb/
dsq_thread_id:
  - 1405779178
categories:
  - Home Lab
tags:
  - /sys/class/power_supply/battery/batt_attr_text
  - adb
  - Android
  - battery status
  - cat
  - dumpsys
---
There are two ways to go about finding out battery status of a rooted Android phone. One is simple and uses *cat*, the other is android specific. Here is how the output of the first one looks like:

	  
	$ ./adb shell cat /sys/class/power_supply/battery/batt_attr_text  
	vref: 1248  
	batt_id: 4  
	batt_vol: 4155  
	batt_current: 229  
	batt_discharge_current: 0  
	batt_temperature: 391  
	Pd_M: 0  
	I_MBAT: 229  
	percent_last(RP): 99  
	percent_update: 90  
	level: 90  
	first_level: 15  
	full_level: 100  
	capacity: 1520  
	charging_source: USB  
	charging_enabled: Slow  
	

That gives most of the battery information. If you just want to find out the current percentage, you can always do this:

	  
	$ ./adb shell cat /sys/class/power_supply/battery/batt_attr_text | grep ^level  
	level: 92  
	

Another way is using the *dumpsys* utility, like so:

	  
	$ ./adb shell dumpsys battery  
	Current Battery Service state:  
	AC powered: false  
	USB powered: true  
	status: 2  
	health: 2  
	present: true  
	level: 92  
	scale: 100  
	voltage:4191  
	temperature: 348  
	technology: Li-ion  
	

This is a little bit more organized. Again, if you want to just see the percentage then *grep* is your friend:

	  
	$ ./adb shell dumpsys battery | grep level  
	level: 92  
	

