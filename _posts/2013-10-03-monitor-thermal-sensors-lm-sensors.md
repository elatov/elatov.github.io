---
title: Monitor Thermal Sensors With lm-sensors
author: Karim Elatov
layout: post
permalink: /2013/10/monitor-thermal-sensors-lm-sensors/
categories: ['os']
tags: ['linux','fedora','ubuntu', 'mac_os_x','monitoring','zabbix','lm_sensors','chromebook']
---

After setting up zabbix to plot hard drive temperatures, I wanted to go further and monitor CPU and MotherBoard (M/B) temperatures as well.

## Install and Configure lm-sensors

To check any thermal information regarding our system board we can use a utility called **lm-sensors**. I had two machines that I wanted to monitor: my really old Fedora desktop and the chromebook laptop running ubuntu. The install is really simple. On my Fedora box, I ran the following:

    sudo yum install lm-sensors


Then I tried to run **sensors** and I got the following warning:

    moxz:~>sensors
    No sensors found!
    Make sure you loaded all the kernel drivers you need.
    Try sensors-detect to find out which these are.


We need to detect what thermal sensors are available, this can be down with the **sensors-detect** command:

    moxz:~>sudo sensors-detect
    # sensors-detect revision 6085 (2012-10-30 18:18:45 +0100)
    # Board: ASUSTeK Computer INC. P4S533

    This program will help you determine which kernel modules you need
    to load to use lm_sensors most effectively. It is generally safe
    and recommended to accept the default answers to all questions,
    unless you know what you're doing.

    Some south bridges, CPUs or memory controllers contain embedded sensors.
    Do you want to scan for them? This is totally safe. (YES/no):


Notice that it shows the board model (ASUSTeK Computer INC. P4S533) during the detection. It will keep asking you a bunch of questions regarding your hardware. If you are not sure and just want to answer **yes** to all the questions, then run the following:

    moxz:~>yes | sudo sensors-detect


At the end of the output you should see something like this:

    Next adapter: NVIDIA i2c adapter 2 at 1:00.0 (i2c-3)
    Do you want to scan it? (yes/NO/selectively):
    Now follows a summary of the probes I have just done.
    Just press ENTER to continue:
    Driver `asb100':
      * Bus `SiS96x SMBus adapter at 0xe600'
        Busdriver `i2c_sis96x', I2C address 0x2d (and 0x48 0x49)
        Chip `Asus ASB100 Bach' (confidence: 8)

    Do you want to overwrite /etc/sysconfig/lm_sensors? (YES/no): Unloading i2c-dev... OK


It looks like it found the **asb100** chip. This was a very old P4 machine, here is M/B information:

    moxz:~>sudo dmidecode -t baseboard
    # dmidecode 2.12
    SMBIOS 2.3 present.

    Handle 0x0002, DMI type 2, 8 bytes
    Base Board Information
        Manufacturer: ASUSTeK Computer INC.
        Product Name: P4S533
        Version: REV 1.xx
        Serial Number: xxxxxxxxxxx


Checking the supported devices from the lm-sensors [page](http://lm-sensors.org/wiki/Devices). I saw the following:

![lm sensors devices asus Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/lm-sensors-devices-asus.png)

It looks like *Asus* is supported by the selected chip. Then running **sensors** again, I saw the following:

    moxz:~>sensors
    asb100-i2c-0-2d
    Adapter: SiS96x SMBus adapter at 0xe600
    in0:          +1.60 V  (min =  +1.20 V, max =  +1.81 V)
    in1:          +1.60 V  (min =  +1.20 V, max =  +1.81 V)
    in2:          +3.30 V  (min =  +3.14 V, max =  +3.47 V)
    in3:          +3.01 V  (min =  +2.83 V, max =  +3.12 V)
    in4:          +3.01 V  (min =  +2.85 V, max =  +3.47 V)
    in5:          +3.01 V  (min =  +0.00 V, max =  +0.00 V)
    in6:          +3.01 V  (min =  +0.00 V, max =  +0.00 V)
    fan1:        2616 RPM  (min = 1997 RPM, div = 4)
    fan2:           0 RPM  (min = 3994 RPM, div = 2)
    fan3:           0 RPM  (min = 3994 RPM, div = 2)
    temp1:        +39.0°C  (high = +80.0°C, hyst = +75.0°C)
    temp2:        +34.5°C  (high = +100.0°C, hyst =  +3.0°C)
    temp3:         -0.5°C  (high = +80.0°C, hyst = +75.0°C)
    temp4:        -44.0°C  (high = +80.0°C, hyst = +75.0°C)
    cpu0_vid:    +1.525 V


The fields were very generic. At this point we would need to check out the manual of the System Board to find out what each of those sensors correspond to. I got lucky and found an example (this was a pretty old board, so I knew someone had an example). From [this](http://lm-sensors.org/svn/lm-sensors/trunk/etc/sensors.conf.eg) site, I found the following example (you can see that it was tested on an Asus P4S333, which was close enough to my board):

    #
    # This example was tested vs. Asus P4S333
    #
    chip "asb100-*"

        label in0 "VCore 1"
        #set in0_min cpu0_vid * 0.95
        #set in0_max cpu0_vid * 1.05

        label in1 "VCore 2"
        ignore in1
        #set in1_min cpu0_vid * 0.95
        #set in1_max cpu0_vid * 1.05

        label in2 "+3.3V"
        #set in2_min 3.3 * 0.95
        #set in2_max 3.3 * 1.05

        label in3 "+5V"
        compute in3 1.68 * @ ,  @ / 1.68
        #set in3_min 5.0 * 0.95
        #set in3_max 5.0 * 1.05

        label in4 "+12V"
        compute in4 3.8 * @ , @ / 3.8
        #set in4_min 12  * 0.90
        #set in4_max 12  * 1.10

        label in5 "-12V (reserved)"
        #ignore in5
        compute in5 -@ * 3.97 ,  -@ / 3.97
        #set in5_max -12 * 0.90
        #set in5_min -12 * 1.10

        label in6 "-5V (reserved)"
        #ignore in6
        compute in6 -@ * 1.666 , -@ / 1.666
        #set in6_max -5  * 0.95
        #set in6_min -5  * 1.05

        label temp1 "M/B Temp"
        #set temp1_max      45
        #set temp1_max_hyst 40

        label temp2 "CPU Temp (Intel)"
        #ignore temp2
        #set temp2_max      60
        #set temp2_max_hyst 50

        # PWRTMP connector on P4S333, for external sensor
        label temp3 "Power Temp"
        #ignore temp3
        #set temp3_max      45
        #set temp3_max_hyst 40


        # Used for Athlon diode, ignore for P4S333
        label temp4 "CPU Temp (AMD)"
        #set temp4_max      60
        #set temp4_max_hyst 50
        #ignore temp4

        label fan1 "CPU Fan"
        #set fan1_div 4
        #set fan1_min 2000

        label fan2 "Chassis Fan"
        #set fan2_div 2
        #set fan2_min 4000

        label fan3 "Power Fan"
        #set fan3_div 2
        #set fan3_min 4000


After adding and modifying the above example into the **/etc/sensors3.conf** file, I ran the following to re-read the configuration:

    moxz:~>sudo sensors -s


then running the **sensors** command one more time, I saw the following:

    moxz:~>sensors
    asb100-i2c-0-2d
    Adapter: SiS96x SMBus adapter at 0xe600
    VCore 1:          +1.58 V  (min =  +1.20 V, max =  +1.81 V)
    +3.3V:            +3.28 V  (min =  +3.14 V, max =  +3.47 V)
    +5V:              +5.05 V  (min =  +4.76 V, max =  +5.24 V)
    +12V:            +11.43 V  (min = +10.82 V, max = +13.19 V)
    -12V (reserved): -11.88 V  (min =  -0.00 V, max =  -0.00 V)
    -5V (reserved):   -4.98 V  (min =  -0.00 V, max =  -0.00 V)
    CPU Fan:         2657 RPM  (min = 1997 RPM, div = 4)
    Chassis Fan:        0 RPM  (min = 3994 RPM, div = 2)
    Power Fan:          0 RPM  (min = 3994 RPM, div = 2)
    M/B Temp:         +42.0°C  (high = +80.0°C, hyst = +75.0°C)
    CPU Temp:         +36.5°C  (high = +100.0°C, hyst =  +3.0°C)
    cpu0_vid:        +1.525 V


That looked better, now I knew exactly what the fields represented (I actually unplugged the Chassis Fan to make sure the labels were correct... and it looked good). I was mainly concerned with the *Temp* and *Fan* fields (I would just plot those in zabbix).

## lm-sensors on Samsung Chromebook in Ubuntu

The install was easier for the Chromebook, I just installed **lm-sensors**:

    sudo apt-get install lm-sensors


and then after running **sensors** I saw the following:

    elatov@crbook:~$sensors
    ncp15wb473-isa-0000
    Adapter: ISA adapter
    temp1:        +32.6°C    sensor = thermistor

    ncp15wb473-isa-0001
    Adapter: ISA adapter
    temp1:        +33.5°C    sensor = thermistor

    ncp15wb473-isa-0002
    Adapter: ISA adapter
    temp1:        +31.5°C    sensor = thermistor

    ncp15wb473-isa-0003
    Adapter: ISA adapter
    temp1:        +32.7°C    sensor = thermistor

    exynos-therm-virtual-0
    Adapter: Virtual device
    temp1:        +38.0°C  (crit = +85.0°C)


At first I thought the ISA adapters were for the CPUs, but I remembered that it's a Dual CPU core. Here is the hardware information regarding the laptop:

    elatov@crbook:~$lshw -class processor -class bus -class system
    crbook.dnsd.me
        description: Computer
        product: Google Snow
        width: 32 bits
      *-core
           description: Motherboard
           physical id: 0
           capabilities: google_snow samsung_exynos5250
         *-cpu:0
              description: CPU
              product: cpu
              physical id: 0
              bus info: cpu@0
              size: 1700MHz
              capacity: 1700MHz
              capabilities: cpufreq
         *-cpu:1
              description: CPU
              product: cpu
              physical id: 1
              bus info: cpu@1
              size: 1700MHz
              capacity: 1700MHz
              capabilities: cpufreq


I wanted to check out the **exynos5250** manual to see what the thermal sensors were on the board and I found [this](https://github.com/elatov/uploads/raw/master/2013/09/Exynos_5_Dual_User_Manaul_Public_REV100-0.pdf) manual, but it didn't shed much light. It just said this:

> 24-bit Thermal Sensor

That was the extent of it.

## Thermal Framework on System-On-Chip (SOC) Systems

I then ran into this presentation: [A simplified thermal framework for ARM platforms](https://github.com/elatov/uploads/raw/master/2013/09/A_New_Simplified_Thermal_Framework_For_ARM_Platforms.pdf). Here are some interesting concepts:

> *   Modern System-on-Chips (SOCs) have considerable higher thermal levels than prior generations.
>     *   System Integration → more transistors, dense gates in the same area and more leakage.
>     *   Performance requirements → much higher processor frequencies and bus speeds.
>     *   More cores → multiple cpu core, multiple gpu core and multiple h/w accelerators.
> *   Cannot cool most SOCs in a traditional sense
>     *   Package size limitations.
>     *   Unavailability of heat sinks, fans, etc.
> *   Very good definition and basic abstraction concepts (Documentation/thermal/sysfs-api.txt).
> *   Concepts of thermal zones, trip points and cooling devices.
> *   Framework to register thermal zone and cooling devices.
> *   Performs a routing function of generic cooling devices to generic thermal zones with the help of very simple thermal management logic.

It seems that thermal monitoring is a little different on the SOC systems. I then ran into this interesting presentation: [PDF](https://github.com/elatov/uploads/raw/master/2013/09/Thermal_Mgmt_using_Generic_thermal_fw.pdf) (thermal zones, cooling devices, and other aspects). Here is a high level overview of the concepts:

![kernel thermal overview Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/kernel_thermal_overview.png)

### Linux Thermal Zones

From the same [PDF](https://github.com/elatov/uploads/raw/master/2013/09/Thermal_Mgmt_using_Generic_thermal_fw.pdf), here is an example of a thermal zone:

![Thermal zone Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/Thermal_zone.png)

Here is some information regarding the thermal zones:

> *   Thermal zone device
>     *   Represents a region managed by thermal framework.
>     *   Includes a thermal sensor and multiple cooling devices.

Here is some information regarding the cooling devices:

> *   Cooling devices
>     *   Actual functional units for cooling down the thermal zone.
>     *   Can be hardware devices and also be software method.
>         *   Hardware : Fans, various physical cooler
>         *   Software : CPU frequency control

For the above concepts there are corresponding **sysfs** nodes. From the same [PDF](https://github.com/elatov/uploads/raw/master/2013/09/Thermal_Mgmt_using_Generic_thermal_fw.pdf):

> *   Nodes under ‘/sys/class/thermal/thermal_zone’
>     *   Get basic information(name, enabling, cooling devices)
>     *   Manage how to work(set governor, trip temperature, passive, hysteresis, emulation)
>     *   Monitor current state
> *   Nodes under ‘/sys/class/thermal/cooling_device’
>     *   Get basic information (name)
>     *   Set/get cooling state

### Thermal Sensors On SOC Systems

I then ran into this: [Inducing Thermal-Awareness in Multicore Systems Using Networks-on-Chip](https://github.com/elatov/uploads/raw/master/2013/09/Inducing_thermal_awareness-InSOC.pdf). From that article:

> Technology scaling imposes an ever increasing temperature stress on digital circuit design due to transistor density, especially on highly integrated systems, such as Multi-Processor Systems-on-Chip (MPSoCs). Therefore, temperature-aware design is mandatory and should be performed at the early design stages. In this paper we present a novel hardware infrastructure to provide thermal control of MPSoC architectures, which is based on exploiting the NoC interconnects of the baseline system as an active component to communicate and coordinate between temperature sensors scattered around the chip, in order to globally monitor the actual temperature. Then, a thermal management unit and clock frequency controllers adjust the frequency and voltage of the processing elements according to the temperature requirements at run-time

And they have a pretty good picture as well:

![thermal sensors on soc Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/thermal_sensors_on_soc.png)

So using multiple sensors on the board, the system can determine what the best course of action to take (ie Scale down the frequency of the CPU).

### Samsung Exynos Thermal Management Unit (TMU)

From "[Samsung at ISSCC: Quad-core Exynos apps processor relies on skillful analog IC design](http://www.eedailynews.com/2012/02/samsung-at-isscc-quad-core-exynos-apps.html)", here is some information regarding the TMU:

> With the popularity of CPU-intensive applications like 3D graphics gaming, there is a real danger that an application processor can burn-out, or at least reach excessive surface temperature within the confines of a mobile device that could impact reliability and usability. To address the issue, Samsung developed a Thermal Management Unit (TMU), which monitors thermal sensors throughout the Exynos chip to detect hotspots, applying thermal throttling through DVFS mechanisms or tripping a shutdown of the chip if necessary. A side benefit of the thermal management is to effect a further reduction in power dissipation.

Putting it all together it looks like Linux defines a thermal Zone which consists of the following:

*   Thermal Sensors
*   Cooling Devices
*   Governor

But with the Exynos Samsung platform there is also:

*   Thermal Management Unit (TMU)

The TMU (which is also a sensor) basically replaces the functionality of the Governor from the Linux Thermal Framework.

## Linux Sysfs Thermal Driver

From "[Generic Thermal Sysfs driver How To](https://www.kernel.org/doc/Documentation/thermal/sysfs-api.txt)":

> The generic thermal sysfs provides a set of interfaces for thermal zone devices (sensors) and thermal cooling devices (fan, processor...) to register with the thermal management solution and to be a part of it.

Here is the structure of **sysfs** for the thermal system:

> Thermal sysfs attributes will be represented under /sys/class/thermal. Hwmon sysfs I/F extension is also available under /sys/class/hwmon, if hwmon is compiled in or built as a module.
>
> Thermal zone device sys I/F, created once it's registered:
>
>     /sys/class/thermal/thermal_zone[0-*]:
>         |---type:         Type of the thermal zone
>         |---temp:         Current temperature
>         |---mode:         Working mode of the thermal zone
>         |---policy:           Thermal governor used for this zone
>         |---trip_point_[0-*]_temp:    Trip point temperature
>         |---trip_point_[0-*]_type:    Trip point type
>         |---trip_point_[0-*]_hyst:    Hysteresis value for this trip point
>         |---emul_temp:        Emulated temperature set node
>
>
> Thermal cooling device sys I/F, created once it's registered:
>
>     /sys/class/thermal/cooling_device[0-*]:
>         |---type:         Type of the cooling device(processor/fan/...)
>         |---max_state:        Maximum cooling state of the cooling device
>         |---cur_state:        Current cooling state of the cooling device
>
>
> Then next two dynamic attributes are created/removed in pairs. They represent the relationship between a thermal zone and its associated cooling device. They are created/removed for each successful execution of thermal_zone_bind_cooling_device/thermal_zone_unbind_cooling_device.
>
>     /sys/class/thermal/thermal_zone[0-*]:
>         |---cdev[0-*]:        [0-*]th cooling device in current thermal zone
>         |---cdev[0-*]_trip_point: Trip point that cdev[0-*] is associated with
>

Here is what I had under my **sysfs** tree:

    elatov@crbook:~$ls -l /sys/class/thermal/thermal_zone0/
    total 0
    lrwxrwxrwx 1 root root    0 Sep 25 19:06 cdev0 -> ../cooling_device1
    -r--r--r-- 1 root root 4096 Sep 25 19:06 cdev0_trip_point
    lrwxrwxrwx 1 root root    0 Sep 25 19:06 cdev1 -> ../cooling_device0
    -r--r--r-- 1 root root 4096 Sep 25 19:06 cdev1_trip_point
    -rw-r--r-- 1 root root 4096 Sep 25 19:06 fan_on_delay
    -rw-r--r-- 1 root root 4096 Sep 25 19:06 mode
    -rw-r--r-- 1 root root 4096 Sep 25 19:06 passive
    drwxr-xr-x 2 root root    0 Sep 25 19:06 power
    lrwxrwxrwx 1 root root    0 Sep 25 07:45 subsystem -> ../../../../class/thermal
    -r--r--r-- 1 root root 4096 Sep 25 19:06 temp
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_0_temp
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_0_type
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_1_temp
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_1_type
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_2_temp
    -r--r--r-- 1 root root 4096 Sep 25 19:06 trip_point_2_type
    -r--r--r-- 1 root root 4096 Sep 25 19:06 type
    -rw-r--r-- 1 root root 4096 Sep 25 07:45 uevent


Notice that I didn't have the **policy** node, this is because I had the TMU and was not using the *Governor* (which is usually part of a *thermal zone*).

So I have one thermal Zone and two cooling devices:

    elatov@crbook:~$ls -l /sys/class/thermal/
    total 0
    lrwxrwxrwx 1 root root 0 Sep 27 07:50 cooling_device0 -> ../../devices/virtual/thermal/cooling_device0
    lrwxrwxrwx 1 root root 0 Sep 27 07:50 cooling_device1 -> ../../devices/virtual/thermal/cooling_device1
    lrwxrwxrwx 1 root root 0 Sep 27 07:50 thermal_zone0 -> ../../devices/virtual/thermal/thermal_zone0


### Linux Kernel and Exynos Thermal Driver

At this point I ran into a couple of different Linux kernel patches. Here was the first one: [thermal: exynos: Add kernel thermal support for exynos platform](http://lwn.net/Articles/473170/). From that article:

> The code added in this patchset adds a thermal interface layer for samsung exynos platforms. This layer is registered from the hwmon based temperature sensor and receives/monitor the temperature from the sensor and informs the generic thermal layer to take the necessary cooling action. Currently this layer can be used to create only one thermal zone and hence only one temperature sensor can register.
>
> Some modifications are done in the temperature sensor driver to export the information needed for the thermal interface to register with the core linux thermal framework and with the cpu frequency based cooling devices.
>
> A simple data/control flow diagrams to illustrate this,
>
>     Core Linux thermal <------->  Exynos thermal  <-------- Temperature Sensor
>         |                             |
>        \|/                            |
>       Cpufreq cooling device <-----
>

Looks like *Exynos* thermal system was added to the Linux thermal Framework. At this point, I wanted to check what was done for cooling.

#### Samsung Exynos Cooling Devices

Checking out my cooling devices I saw the following:

    elatov@crbook:~$ls /sys/class/thermal/cooling_device*/type; cat /sys/class/thermal/cooling_device*/type
    /sys/class/thermal/cooling_device0/type
    /sys/class/thermal/cooling_device1/type
    thermal-cpufreq-0
    thermal-cpufreq-1


So my cooling devices are CPU frequency regulators for each of my CPUs (this was a Dual Core). So the higher the temperature of the thermal zone is, the lower the frequency of the CPUs are set (to slow down the CPUs, so they don't heat up). Here is a similar note from this [PDF](https://github.com/elatov/uploads/raw/master/2013/09/Thermal_Mgmt_using_Generic_thermal_fw.pdf):

> *   CPU cooling device
>     *   Controls CPU frequency according to cooling state.
>     *   Higher cooling state, lower frequency.
>     *   Limits the maximum CPU frequency with updating CPUFREQ policy. (Indirect)

Later on the same PDF talks about the specific Exynos Thermal Driver:

> *   EXYNOS TMU(thermal management unit)
> *   Features
>     *   HW interrupt (Falling/Raising)
>     *   Trip point (hardware)
>     *   Temperature history (currently not using)
>     *   Trimming
>     *   Emulation
> *   Cooling device
>     *   Currently exynos_thermal driver uses CPU cooling device only.
>     *   When create CPU cooling device, it sets 0 for CPU mask. (Core 0)
>     *   At binding time, it creates multiple thermal instances based on number of ACTIVE trips.

So the Exynos thermal driver throttles the CPU determined by the ACTIVE trips that are created. Here is a pretty good diagram of the process:

![exynos thermal driver Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/exynos_thermal_driver.png)

Depending on which one it tripped we throttle the CPU accordingly. Here are the trip values on the laptop:

    elatov@crbook:~$for i in $(ls /sys/class/thermal/thermal_zone0/trip_point_*_temp); do echo $i; cat $i; done
    /sys/class/thermal/thermal_zone0/trip_point_0_temp
    85000
    /sys/class/thermal/thermal_zone0/trip_point_1_temp
    103000
    /sys/class/thermal/thermal_zone0/trip_point_2_temp
    108000


Those are the temperature limits (85C, 103C, and 108C), at which point the CPU frequency will be limited accordingly.

#### Samsung TMU

Here was another Kernel Patch that I ran into: "[thermal: exynos: Register the tmu sensor with the kernel thermal layer](http://lwn.net/Articles/473170/)". From that patch:

> This code added creates a link between temperature sensors, linux thermal framework and cooling devices for samsung Exynos platform. This layer monitors the temperature from the sensor and informs the generic thermal layer to take the necessary cooling action.

So the TMU is seen as another sensor, which corresponded to the last sensor seen in the **sensors** output:

    elatov@crbook:~$sensors | tail -4
    exynos-therm-virtual-0
    Adapter: Virtual device
    temp1:        +35.0°C  (crit = +85.0°C)


We can also confirm by checking the *type* of the thermal zone:

    elatov@crbook:~$cat /sys/class/thermal/thermal_zone0/type
    exynos-therm


#### Samsung Thermal Sensors

It looks like the "regular" thermal sensors are getting registered as hwmon sensors. I ran into "[Linux/Documentation/hwmon/sysfs-interface](http://lxr.free-electrons.com/source/Documentation/hwmon/sysfs-interface)". From that document:

> An alternative method that some programs use is to access the sysfs files directly. This document briefly describes the standards that the drivers follow, so that an application program can scan for entries and access this data in a simple and consistent way. That said, such programs will have to implement conversion, labeling and hiding of inputs. For this reason, it is still not recommended to bypass the library.
>
> Each chip gets its own directory in the sysfs /sys/devices tree. To find all sensor chips, it is easier to follow the device symlinks from /sys/class/hwmon/hwmon*.

With *lm-sensors* for each chip with sensors a **sysfs** node is created under **/sys/class/hwmon**. Checking my **sysfs** nodes, I did indeed see 5 (4, minus the TMU):

    elatov@crbook:~$ls -l /sys/class/hwmon/
    total 0
    lrwxrwxrwx 1 root root 0 Sep 25 07:45 hwmon0 -> ../../devices/platform/ncp15wb473.0/hwmon/hwmon0
    lrwxrwxrwx 1 root root 0 Sep 25 07:45 hwmon1 -> ../../devices/platform/ncp15wb473.1/hwmon/hwmon1
    lrwxrwxrwx 1 root root 0 Sep 25 07:45 hwmon2 -> ../../devices/platform/ncp15wb473.2/hwmon/hwmon2
    lrwxrwxrwx 1 root root 0 Sep 25 07:45 hwmon3 -> ../../devices/platform/ncp15wb473.3/hwmon/hwmon3
    lrwxrwxrwx 1 root root 0 Sep 25 07:45 hwmon4 -> ../../devices/virtual/hwmon/hwmon4


It looks like we have **ncp15wb473** thermistor as thermal sensors on the motherboard. I also ran into this patch: [daisy: thermal: Find enumerated hwmon temperature sensors](http://git.chromium.org/gitweb/?p=chromiumos/overlays/board-overlays.git;a=commitdiff;h=3039a00bb71dffdb083353bed348ac45a745beb4). Here is description from that path:

> This CL refactors locating the temperature sensors for Exynos based designs under the hwmon class. Currently those sensors include:
>
> *   Snow: ncp15wb473 thermistor (hwmon/ntc_thermistor)
> *   Spring: G781 sensor (hwmon/lm90)

### ChromeOS Using Thermal Management on Samsung Chromebook

The last mentioned patch was actually for a script that is available in ChromeOS: it's called **thermal.sh**. The complete script can be found [here](https://github.com/gentoo-arm-ru/overlay/blob/master/bsp-support/chromebook-daisy/files/thermal.sh). From the script:

> Quick hack to monitor thermals on snow platform. Since we only have passive cooling, the only thing we can do is limit CPU temp.

If you look through the script it confirms my belief. The script basically checks the contents of the M/B Sensors (thermistors) and also the TMU (seen as a separate sensor). The thermistors values are here (this is seen in the script):

    declare -a DAISY_THERMISTOR_TEMP=( \
        "/sys/devices/platform/ncp15wb473.0/temp1_input" \
        "/sys/devices/platform/ncp15wb473.1/temp1_input" \
        "/sys/devices/platform/ncp15wb473.2/temp1_input" \
        "/sys/devices/platform/ncp15wb473.3/temp1_input")


And the TMU value is here (also from the script):

    declare -a DAISY_CPU_TEMP=("/sys/class/thermal/thermal_zone0/temp")


We can see that the script just assigned the TMU sensor as the CPU temperature. We also see that the script is not final and it adds the following TODO:

> TODO validate thermistor readings.We should reject anything that is more than 5C off from all others.

Inside ChromeOS when the script is working you will see the following (seen from the [mentioned](http://git.chromium.org/gitweb/?p=chromiumos/overlays/board-overlays.git;a=commitdiff;h=c4b7c694c1d283b145bd77cdfe34385082ae1d4f) patch above):

> boot on Snow (4 thermistors) and thermal server starts and remains running:

    $ grep -i therm /var/log/messages
    2013-02-14T07:51:51.393918-08:00 localhost kernel: [ 1.194676] ntc-thermistor ncp15wb473.0: Thermistor ncp15wb473:0 (type:ncp15wb473/0) successfully probed.
    2013-02-14T07:51:51.393925-08:00 localhost kernel: [ 1.194738] ntc-thermistor ncp15wb473.1: Thermistor ncp15wb473:1 (type: ncp15wb473/0) successfully probed.
    2013-02-14T07:51:51.393931-08:00 localhost kernel: [ 1.194799] ntc-thermistor ncp15wb473.2: Thermistor ncp15wb473:2 (type: ncp15wb473/0) successfully probed.
    2013-02-14T07:51:51.393937-08:00 localhost kernel: [ 1.194856] ntc-thermistor ncp15wb473.3: Thermistor ncp15wb473:3 (type: ncp15wb473/0) successfully probed.
    2013-02-14T07:51:51.393942-08:00 localhost kernel: [ 1.195273] Exynos: Kernel Thermal management registered
    2013-02-14T07:51:57.560020-08:00 localhost thermal.sh: Max CPU Freq set to 1300000 (Celsius: 65 43 48 42 44)
    2013-02-14T07:52:12.621581-08:00 localhost thermal.sh: Max CPU Freq set to 1700000 (Celsius: 50 43 46 42 43)


Notice the script also shows the Temperature readings from the TMU and the other Thermal sensors (upon throttling the CPU).

## lm-sensors Configuration for Samsung Chromebook

For ease of plotting, I decided to label the TMU sensor *CPU temp* and the other NTC thermistors/sensors *M/B # Temp*. Here is what I added to my **/etc/sensors3.conf** file:

    chip "ncp15wb473-isa-0000"
        label temp1 "M/B 1 Temp"

    chip "ncp15wb473-isa-0001"
        label temp1 "M/B 2 Temp"

    chip "ncp15wb473-isa-0002"
        label temp1 "M/B 3 Temp"

    chip "ncp15wb473-isa-0003"
        label temp1 "M/B 4 Temp"

    chip "*-virtual-0"
        label temp1 "CPU Temp"


After adding that into the file and re-reading the configuration:

    $ sudo sensors -s


My output looked like this:

    elatov@crbook:~$sensors
    ncp15wb473-isa-0000
    Adapter: ISA adapter
    M/B 1 Temp:   +31.6°C    sensor = thermistor

    ncp15wb473-isa-0001
    Adapter: ISA adapter
    M/B 2 Temp:   +33.1°C    sensor = thermistor

    ncp15wb473-isa-0002
    Adapter: ISA adapter
    M/B 3 Temp:   +31.0°C    sensor = thermistor

    ncp15wb473-isa-0003
    Adapter: ISA adapter
    M/B 4 Temp:   +33.0°C    sensor = thermistor

    exynos-therm-virtual-0
    Adapter: Virtual device
    CPU Temp:     +34.0°C  (crit = +85.0°C)


Now all that I had to do was plot those values in zabbix :)

## Sensors On MacBook Pro

While in Mac OS X you can install **iStat** and then from the dashboard you can see all the temperature information. Here is how mine looked like:

![i stat dashboard Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/i_stat_dashboard.png)

You can also download the temperature Monitor from [here](http://www.bresink.com/osx/0TemperatureMonitor/download.php5). After you install, it you can run it manually. Here is what I saw when I ran it on my system:

    $/Applications/TemperatureMonitor.app/Contents/MacOS/tempmonitor -a -c -l
    SMART Disk TOSHIBA MK5065GSXF (81RVCAO4T): 29 C
    SMC BATTERY: 28 C
    SMC BATTERY POSITION 2: 28 C
    SMC BATTERY POSITION 3: 26 C
    SMC CPU A DIODE: 58 C
    SMC CPU A PROXIMITY: 49 C
    SMC GPU 1 CHIP: 52 C
    SMC GPU DIODE: 54 C
    SMC LEFT PALM REST: 26 C
    SMC MAIN HEAT SINK 2: 51 C
    SMC MAIN HEAT SINK 3: 47 C
    SMC MAIN LOGIC BOARD: 37 C
    SMC PLATFORM CONTROLLER HUB: 48 C
    SMC SSD BAY: 39 C


Rebooting into Fedora, here is the **lm-sensors** output:

    $sensors
    applesmc-isa-0300
    Adapter: ISA adapter
    Left side  : 2776 RPM  (min = 2000 RPM, max = 6200 RPM)
    Right side : 2781 RPM  (min = 2000 RPM, max = 6200 RPM)
    TB0T:         +30.2°C
    TB1T:         +30.2°C
    TB2T:         +28.8°C
    TC0C:         +71.0°C
    TC0D:         +71.2°C
    TC0E:         +76.0°C
    TC0F:         +77.2°C
    TC0P:         +62.2°C
    TC1C:         +68.0°C
    TC2C:         +68.0°C
    TC3C:         +68.0°C
    TC4C:         +68.0°C
    TCGC:         +68.0°C
    TCSA:         +69.0°C
    TCTD:          -0.2°C
    TG0D:         +68.2°C
    TG0P:         +67.2°C
    THSP:         +45.0°C
    TM0S:         +57.8°C
    TMBS:          +0.0°C
    TP0P:         +61.2°C
    TPCD:         +66.0°C
    TW0P:        -127.0°C
    Th1H:         +60.8°C

    coretemp-isa-0000
    Adapter: ISA adapter
    Physical id 0:  +74.0°C  (high = +86.0°C, crit = +100.0°C)
    Core 0:         +72.0°C  (high = +86.0°C, crit = +100.0°C)
    Core 1:         +74.0°C  (high = +86.0°C, crit = +100.0°C)
    Core 2:         +73.0°C  (high = +86.0°C, crit = +100.0°C)
    Core 3:         +69.0°C  (high = +86.0°C, crit = +100.0°C)


There were a lot of sensors :). I looked around and I found a couple of sites that explained some of the sensors but not all:

*   [How do I interpret the sensor names from apple-smc?](https://discussions.apple.com/thread/4838014?start=0&tstart=0)
*   [MacBookPro5-1_5-2/Lucid](https://help.ubuntu.com/community/MacBookPro5-1_5-2/Lucid)
*   [Sensors (applesmc module)](https://wiki.debian.org/iMacIntel#Sensors_.28applesmc_module.29)
*   [[Mactel-linux-devel] AppleSMC names](http://www.mail-archive.com/mactel-linux-devel@lists.sourceforge.net/msg00526.html)
*   [where is the palm rest temperature sensor located?](http://forums.appleinsider.com/t/114028/where-is-the-palm-rest-temperature-sensor-located)
*   [Logic board temperature sensor?](http://www.ifixit.com/Answers/View/44153/Logic+board+temperature+sensor)

I also tried to find the manual for the motherboard, but I was only able to find the following:

*   [Service Source MacBook Pro](https://github.com/elatov/uploads/raw/master/2013/09/macbook-pro-service-manual.pdf)
*   [MacBook Pro 15-inch Repair Guide](https://github.com/elatov/uploads/raw/master/2013/09/15-inch-macbook-pro-manual.pdf)
*   [Apple Technician Guide MacBook Pro 15](https://github.com/elatov/uploads/raw/master/2013/09/mbp15_mid10.pdf)

They had instructions on how to replace all the sensors but they didn't have a concise list of all the sensors. The best sources were actually the source code for the *iStat* Program (which I used while in MacOS X) and another program called *HwMonitor*. [here](https://github.com/marioestrada/istat-widgets/blob/master/iStat%20nano/iStatNano.bundle/Contents/s/intel/iStatIntelControlleriStatPro.m) is the source for *hwMonitor*. Here are some examples from each program:

    [keyDisplayNames setValue:@"CPU A" forKey:@"TC0H"];
    [keyDisplayNames setValue:@"CPU A" forKey:@"TC0D"];
    [keyDisplayNames setValue:@"CPU B" forKey:@"TC1D"];
    [keyDisplayNames setValue:@"CPU A" forKey:@"TCAH"];
    [keyDisplayNames setValue:@"CPU B" forKey:@"TCBH"];
    [keyDisplayNames setValue:@"GPU" forKey:@"TG0P"];
    [keyDisplayNames setValue:@"Ambient" forKey:@"TA0P"];
    [keyDisplayNames setValue:@"HD Bay 1" forKey:@"TH0P"];
    [keyDisplayNames setValue:@"HD Bay 2" forKey:@"TH1P"];
    [keyDisplayNames setValue:@"HD Bay 3" forKey:@"TH2P"];
    [keyDisplayNames setValue:@"HD Bay 4" forKey:@"TH3P"];
    [keyDisplayNames setValue:@"Optical Drive" forKey:@"TO0P"];
    [keyDisplayNames setValue:@"Heatsink A" forKey:@"Th0H"];
    [keyDisplayNames setValue:@"Heatsink B" forKey:@"Th1H"];
    [keyDisplayNames setValue:@"GPU Diode" forKey:@"TG0D"];
    [keyDisplayNames setValue:@"GPU Heatsink" forKey:@"TG0H"];
    [keyDisplayNames setValue:@"Power supply 2" forKey:@"Tp1C"];
    [keyDisplayNames setValue:@"Power supply 1" forKey:@"Tp0C"];
    [keyDisplayNames setValue:@"Power supply 1" forKey:@"Tp0P"];
    [keyDisplayNames setValue:@"Enclosure Bottom" forKey:@"TB0T"];
    [keyDisplayNames setValue:@"Northbridge 1" forKey:@"TN0P"];
    [keyDisplayNames setValue:@"Northbridge 2" forKey:@"TN1P"];
    [keyDisplayNames setValue:@"Northbridge" forKey:@"TN0H"];


and here is an example from the second one:

    [NSArray arrayWithObjects:@"TC:081D",    @"CPU Die %X", nil],
    [NSArray arrayWithObjects:@"TC:081C",    @"CPU Core %X", nil],
    [NSArray arrayWithObjects:@"TC:A2AC",    @"CPU %X", nil],
    [NSArray arrayWithObjects:@"TC0H",       @"CPU Heatsink", nil],
    [NSArray arrayWithObjects:@"Th0H",       @"CPU Heatsink", nil],
    [NSArray arrayWithObjects:@"TC0P",       @"CPU Proximity", nil],
    [NSArray arrayWithObjects:@"TCPC",       @"CPU Package", nil],
    [NSArray arrayWithObjects:@"TC:A4AH",    @"CPU %X, Heatsink", nil],
    [NSArray arrayWithObjects:@"TCXC",       @"PECI CPU", nil],
    [NSArray arrayWithObjects:@"TCXc",       @"PECI CPU", nil],
    [NSArray arrayWithObjects:@"TCSC",       @"PECI SA", nil],
    [NSArray arrayWithObjects:@"TCSc",       @"PECI SA", nil],
    [NSArray arrayWithObjects:@"TCSA",       @"PECI SA", nil],
    [NSArray arrayWithObjects:@"TCGC",       @"PECI GPU", nil],
    [NSArray arrayWithObjects:@"TCGc",       @"PECI GPU", nil],


Also from the *mactel-linux* email forum there was a nice mapping as well:

    1) #KEY = Key count
       NTOK = Interrupt Ok key

       T = Temperature sensor
       2)
         A = Ambient
         B = Enclosure bottom
         C = CPU
         G = GPU
         H = Harddisk (Bay)
         h = Heatsink
         M = Memory (bank/module)
         m = memory Controller
         N = Northbridge
         O = Optical drive
         p = Power supply
         S = Slot (Expansion)
         s = Slot (PCI express)???

          3)
           0-9,A-Z: Number of sensor
            4)
              C = ??
              D = Diode
              H = Heatsink
              P = ??
              S = ??
              T = ??


After comparing the different sources from above, I ended up adding the following into my **/etc/sensors3.conf** file:

    chip "applesmc-*"
        label fan1 "Chassis-1 Fan"
        label fan2 "Chassis-2 Fan"
        label temp1 "Battery-1 Temp"
        label temp2 "Battery-2 Temp"
        label temp3 "Battery-3 Temp"
        label temp4 "CPU_Package-Die Temp"
        label temp5 "CPU_Package-Diode Temp"
        ignore temp6
        ignore temp7
        label temp8 "CPU_Package-Proximity Temp"
        label temp9 "CPU_Core0-Die Temp"
        label temp10 "CPU_Core1-Die Temp"
        label temp11 "CPU_Core2-Die Temp"
        label temp12 "CPU_Core3-Die Temp"
        label temp13 "PECI-GPU Temp"
        label temp14 "PECI-SA Temp"
        ignore temp15
        label temp16 "GPU0-Die Temp"
        label temp17 "GPU0-Proximity Temp"
        label temp18 "HDD-Bay Temp"
        label temp19 "Memory-Modules Temp"
        label temp20 "Memory-Module_B Temp"
        label temp21 "PCH-Proximity Temp"
        label temp22 "PCH-Die Temp"
        label temp23 "Airport_Wireless-Proximity Temp"
        label temp24 "Heat-Pipe Temp"

    chip "coretemp-*"
        label temp1 "CPU_Package Temp"
        label temp2 "CPU_Core0 Temp"
        label temp3 "CPU_Core1 Temp"
        label temp4 "CPU_Core2 Temp"
        label temp5 "CPU_Core3 Temp"


and then my **sensors** looked like this:

    $sensors
    applesmc-isa-0300
    Adapter: ISA adapter
    Chassis-1 Fan:                   2415 RPM  (min = 2000 RPM, max = 6200 RPM)
    Chassis-2 Fan:                   2409 RPM  (min = 2000 RPM, max = 6200 RPM)
    Battery-1 Temp:                   +35.2°C
    Battery-2 Temp:                   +35.2°C
    Battery-3 Temp:                   +34.0°C
    CPU_Package-Die Temp:             +68.8°C
    CPU_Package-Diode Temp:           +68.5°C
    CPU_Package-Proximity Temp:       +59.2°C
    CPU_Core0-Die Temp:               +70.0°C
    CPU_Core1-Die Temp:               +71.0°C
    CPU_Core2-Die Temp:               +69.0°C
    CPU_Core3-Die Temp:               +69.0°C
    PECI-GPU Temp:                    +70.0°C
    PECI-SA Temp:                     +67.0°C
    GPU0-Die Temp:                    +65.8°C
    GPU0-Proximity Temp:              +65.8°C
    HDD-Bay Temp:                     +43.0°C
    Memory-Modules Temp:              +63.0°C
    Memory-Module_B Temp:              +0.0°C
    PCH-Proximity Temp:               +59.2°C
    PCH-Die Temp:                     +64.0°C
    Airport_Wireless-Proximity Temp: -127.0°C
    Heat-Pipe Temp:                   +62.5°C

    coretemp-isa-0000
    Adapter: ISA adapter
    CPU_Package Temp:  +72.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core0 Temp:    +69.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core1 Temp:    +72.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core2 Temp:    +70.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core3 Temp:    +68.0°C  (high = +86.0°C, crit = +100.0°C)


I realized that my **Memory_Module Bank B** wasn't showing anything (and the **Airport** sensor was way off), so I disabled both and here was my final **sensors** output:

    $sensors
    applesmc-isa-0300
    Adapter: ISA adapter
    Chassis-1 Fan:              3570 RPM  (min = 2000 RPM, max = 6200 RPM)
    Chassis-2 Fan:              3567 RPM  (min = 2000 RPM, max = 6200 RPM)
    Battery-1 Temp:              +35.8°C
    Battery-2 Temp:              +35.8°C
    Battery-3 Temp:              +34.5°C
    CPU_Package-Die Temp:        +69.2°C
    CPU_Package-Diode Temp:      +68.5°C
    CPU_Package-Proximity Temp:  +61.0°C
    CPU_Core0-Die Temp:          +69.0°C
    CPU_Core1-Die Temp:          +69.0°C
    CPU_Core2-Die Temp:          +69.0°C
    CPU_Core3-Die Temp:          +69.0°C
    PECI-GPU Temp:               +68.0°C
    PECI-SA Temp:                +66.0°C
    GPU0-Die Temp:               +65.8°C
    GPU0-Proximity Temp:         +67.0°C
    HDD-Bay Temp:                +42.5°C
    Memory-Modules Temp:         +59.8°C
    PCH-Proximity Temp:          +60.5°C
    PCH-Die Temp:                +65.0°C
    Heat-Pipe Temp:              +63.5°C

    coretemp-isa-0000
    Adapter: ISA adapter
    CPU_Package Temp:  +71.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core0 Temp:    +71.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core1 Temp:    +70.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core2 Temp:    +69.0°C  (high = +86.0°C, crit = +100.0°C)
    CPU_Core3 Temp:    +68.0°C  (high = +86.0°C, crit = +100.0°C)


### MacBook Pro Processor

I decided to use the label **CPU_Package** cause it was the most appropriate. Imagine the CPU chip looking like this:

![cpu chip1 Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/cpu_chip1.png)

In my case there are 4 Cores, but the idea is the same. The whole CPU (confusing term) is the Processor Package (check out [this](http://superuser.com/questions/324284/what-is-meant-by-the-terms-cpu-core-die-and-package) page for definitions of CPU,Core, and Processor Package). The easiest tool that helps the representation of the CPUs is **powertop**. When I ran that tool, here is what I saw:

![powertop1 Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/powertop1.png)

So my laptop has **1** Process Package, which consists of **4** Cores and (since hyper-threading is enabled) we have 2 "virtual cores" per core. I could've just made the label **CPU** and that would make sense as well. What I saw in **powertop**, matched the laptop description:

*   [Apple MacBook Pro "Core i7" 2.2 15" Late 2011 Specs](http://www.everymac.com/systems/apple/macbook_pro/specs/macbook-pro-core-i7-2.2-15-late-2011-unibody-thunderbolt-specs.html)
*   [MacBook Pro (15-inch, Late 2011) - Technical Specifications](http://support.apple.com/kb/sp644)

From the top link:

> The MacBook Pro "Core i7" 2.2 15-Inch (Late 2011) features a 32 nm "Sandy Bridge" 2.2 GHz Intel "Core i7" processor (2675QM), with four independent processor "cores" on a single silicon chip

Also regarding hyper-threading, from [here](http://store.apple.com/sg/learnmore/MD389ZP/A?group=processor_z0nq):

> The Intel Core i7 processors are based on new 22-nanometer process technology with an advanced Core micro-architecture that features an integrated memory controller and level 3 cache, giving the Mac faster, more direct access to memory. In addition, these processors feature:
>
> *   Turbo Boost 2.0 — a dynamic performance technology that automatically boosts the processor clock speed based on workload, giving you extra processing power when you need it.
> *   Hyper-Threading — a technology that allows two threads to run simultaneously on each core. So a quad-core Mac has eight virtual cores, all of which are recognized by OS X. This enables the processor to deliver faster performance by spreading tasks more evenly across a greater number of cores.

### Platform Environment Control Interface (PECI) and Platform Controller Hub (PCH)

As I was labeling the sensors I came across some interesting acronyms. The first one, PECI, is described in ["Intel Celeron Mobile Processor P4000 and U3000 Series Datasheet"](https://github.com/elatov/uploads/raw/master/2013/09/celeron-mobile-p4000-u3000-datasheet.pdf). From that PDF:

> Each processor execution core has an on-die Digital Thermal Sensor (DTS) which detects the cores instantaneous temperature. The DTS is the preferred method of monitoring processor die temperature because:
>
> *   It is located near the hottest portions of the die.
> *   It can accurately track the die temperature and ensure that the Adaptive Thermal Monitor is not excessively activated.
>
> Temperature values from the DTS can be retrieved through 
>
> *   A software interface via processor Model Specific Register (MSR). 
> *   A processor hardware interface as described in Platform Environment Control Interface (PECI)
>
> When temperature is retrieved by processor MSR, it is the instantaneous temperature of the given core. When temperature is retrieved via PECI, it is the average temperature of each execution cores DTS over a programmable window (default window of 256 ms.) Intel recommends using the PECI output reading for fan speed or other platform thermal control.

So PECI is another interface that grabs the average temperature across multiple CPUs (or any thermal sensors) and it's supposed to be more accurate. There was also a **PECI_SA** sensor, that actually corresponds to the *System Agent*. Looking over ["Power management architecture of the 2nd generation Intel Core"](https://github.com/elatov/uploads/raw/master/2013/09/HC23.19.921.SandyBridge_Power_10-Rotem-Intel.pdf), we see this:

![intel peci sa Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/intel_peci_sa.png)

So we have two PECI capable sensors, GPU and SA. The GPU (Graphical Processing Unit.. self explanatory) and SA (the system agent, basically representing the Thermal Environment.. so I am guessing all the CPUs).

The other term is PCH. Here is a pretty good definition from [wikipedia](http://en.wikipedia.org/wiki/Platform_Controller_Hub):

> The Platform Controller Hub (PCH) is a family of Intel microchips, introduced circa 2008. It is the successor to the previous Intel Hub Architecture, which used a northbridge and southbridge instead, and first appeared in the Intel 5 Series.
>
> The PCH controls certain data paths and support functions used in conjunction with Intel CPUs. These include clocking (the system clock), Flexible Display Interface (FDI) and Direct Media Interface (DMI), although FDI is only used when the chipset is required to support a processor with integrated graphics. As such, I/O Functions are reassigned between this new central hub and the CPU compared to the previous architecture: some northbridge functions, the memory controller and PCI-e lanes, were integrated into the CPU while the PCH took over the remaining functions in addition to the traditional roles of the southbridge.

From the [Apple Technician Guide MacBook Pro 15](https://github.com/elatov/uploads/raw/master/2013/09/mbp15_mid10.pdf), here is a good diagram:

![macbookpro 15 PCH Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/macbookpro_15_PCH.png)

So we can see that most of the components go through the PCH. Also from ["Intel 7 Series / C216 Chipset Platform Controller Hub (PCH)"](https://github.com/elatov/uploads/raw/master/2013/09/7-series-chipset-pch-thermal-design-guide.pdf) here is a table of all the components that connect to the PCH:

![PCH Components core I7 Monitor Thermal Sensors With lm sensors](https://github.com/elatov/uploads/raw/master/2013/09/PCH_Components_core_I7.png)

I would say the PCH Temperature basically represents the Temperature of the motherboard.

