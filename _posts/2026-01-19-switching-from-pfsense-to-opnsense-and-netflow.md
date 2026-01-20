---
published: true
layout: post
title: "Switching from pfSense to OPNSense and NetFlow"
author: Karim Elatov
categories: [networking, home_lab, containers]
tags: [pfsense, opnsense, ktransate, netflow]
---

I decided to install OPNSense on my firewall which has been [running pfSense](/2016/10/installing-pfsense-on-pc-engines-apu1d4-netgate-apu4/) for a couple of years. The majority of pfSense configurations map directly to OPNsense, ensuring high functional parity between the two platforms (they are both using freeBSD under the hood). Here are the settings I applied:

1. Disable beeps: **System** > **Settings** -> **Miscellaneous** -> **Disable the startup/shutdown beep**
2. Configure Port Forwards: **Firewall** -> **NAT** -> **Port Forward**
   1. Enable NAT Reflection: **Firewall** -> **NAT** -> **Settings** (this ensures private networks can reach the public IPs as well)
3. Add another GW (so I can reach my DMZ network): **System** -> **Gateways** -> **Configuration**
4. Add a Static Route (To use the above gateway): **System** -> **Routes** -> **Configuration**
5. Configure DHCP Server(For the router): **Services** -> **Dnsmasq DNS & DHCP** -> **General**
   1. Configure Static DHCP:  **Services** -> **Dnsmasq DNS & DHCP** -> **Leases**
   2. Interesting note, in OPNSense, we have multiple services: `dnsmasq`, `ISC DHCP`, `KEA`, and `unbound`. `ISC DHCP` is getting removed so it should not be used. `KEA` is a enteprise level DHCP server and in a home lab it's probably over kill. So for a home environment, `dnsmasq` is used for DHCP. And then to separate the functionality, `unbound` is used for DNS by default.
6. Send Logs to Remote Syslog: **System** -> **Settings** -> **Logging** -> **Remote** 

Those were pretty much the same in `pfSense`.

### Ansible Automation
For `pfSense` I used [pfsensible](https://galaxy.ansible.com/ui/repo/published/pfsensible/core/) and it was actually able to automate most of the settings in `pfSense`. For `OPNSense` it looks like [oxlorg.opnsense](https://galaxy.ansible.com/ui/repo/published/oxlorg/opnsense/) is the best collection, however I think `OPNSense` is going through a lot of architectural changes so the collection is not that stable. I am hoping in the next couple of years all the issues can be ironed out.

### Netflow / Network Insights

This is one thing that I noticed was a little bit better with `OPNSense` (you can enable `netflow` and use it for additional traffic monitoring and statistics, something that I didn't see in `pfSense` natively). The configuration is broken into two parts. Under **Reporting** -> **Netflow** you can enable `netflow` on specific interfaces. There is an extra option **Capture local** (this stores the `netflow` data locally and allows you to see graphs under **Reporting** -> **Insight**). If you just enable `netflow` without enabling the **Capture local** option. You will have the following:

1. Kernel (`ng_netflow`) watches the packets on `re0` (or your configured interface)
   
   ```
   root@fw:~ # ngctl list
   There are 6 total nodes:
     Name: ksocket_netflow_re0 Type: ksocket         ID: 000000a3   Num hooks: 1
     Name: re0             Type: ether           ID: 00000004   Num hooks: 2
     Name: re1             Type: ether           ID: 00000005   Num hooks: 0
     Name: re2             Type: ether           ID: 00000006   Num hooks: 0
     Name: ngctl93969      Type: socket          ID: 000000b3   Num hooks: 0
     Name: netflow_re0     Type: netflow         ID: 0000009d   Num hooks: 3
   ```

   You can check the current flows going through a `netgraph`:
   
   ```
   root@fw:~ # flowctl netflow_re0: show human | head
   SrcIf         SrcIPaddress    DstIf         DstIPaddress    Proto  SrcPort  DstPort     Pkts
   re2           xx.xx.xx.112    re0           173.194.193.129     6    53628      443       16
   re2           xx.xx.xx.112    re0           45.179.243.227      6      443    29848        6
   re2           xx.xx.xx.112    re0           173.194.193.95     17    62332      443       15
   re2           xx.xx.xx.112    re0           142.250.69.234     17    29403      443        9
   re0           45.179.243.16   lo0           161.97.231.112      6    53220      443        1
   re2           xx.xx.xx.112    re0           45.179.243.33       6      443    29749        6
   re0           142.250.69.238  lo0           xx.xx.xx.112       17      443    59705       21
   re2           xx.xx.xx.112    re0           74.125.132.94      17     9182      443        8
   re2           xx.xx.xx.112    re0           45.179.243.74       6      443    30137        6
   ```
2. Sends those flows to `127.0.0.1:2055`
   
   ```
   root@fw:~ # ngctl msg ksocket_netflow_re0: getpeername
   Rec'd response "getpeername" (6) from "[e4]:":
   Args: inet/127.0.0.1:2055
   ```
3. `Samplicate` listens on `:2055` and "clones" the packets to a configured destination (in my instance it's `192.168.1.202:9995` which is `ktranslate`)
   
   ```
   root@fw:~ # ps auwwx | grep sampli
   root    71996   0.0  0.1   13768  2264  -  Is   20:29      0:00.00 daemon: /usr/local/bin/samplicate[72099] (daemon)
   nobody  72099   0.0  0.1   13664  2188  -  S    20:29      0:00.04 /usr/local/bin/samplicate -s 127.0.0.1 -p 2055 192.168.1.202/9995 127.0.0.1/2056
   ```

#### Netflow with Local Capture
If the **Local Capture** option is enabled then an additional flow will be configured:

1. An additional destination for netflow will be configured (`127.0.0.1:2056`)

2. `flowd` (the additional collector) will be enabled to listen on `127.0.0.1:2056`:
   
   ```
   root@fw:~ # service flowd status
   flowd is running as pid 62168 62516.
   root@fw:~ # cat /usr/local/etc/flowd.conf
   logfile "/var/log/flowd.log"
   listen on 127.0.0.1:2056
   flow source 0.0.0.0/0
   store ALL
   ```

3. `flowd` will store the raw `netflow` data under `/var/logl/flowd.log.*` and we can use `flowd-reader` to see the data
   
   ```
   root@fw:~ # ls /var/log/flowd.log*
   /var/log/flowd.log      /var/log/flowd.log.000003  /var/log/flowd.log.000006  /var/log/flowd.log.000009
   /var/log/flowd.log.000001  /var/log/flowd.log.000004  /var/log/flowd.log.000007  /var/log/flowd.log.000010
   /var/log/flowd.log.000002  /var/log/flowd.log.000005  /var/log/flowd.log.000008
   root@fw:~ # flowd-reader /var/log/flowd.log | tail -n 1
   FLOW recv_time 2026-01-12T21:39:35.690477 proto 6 tcpflags 12 tos 00 agent [127.0.0.1] src [xx.xx.xx.112]:443 dst [179.49.184.159]:43410 packets 6 octets 312
   ```
4. `flowd_aggregate` (the aggregator that processes logs into a database for the "Insight" reporting tool) will be enabled.
   
   ```
   root@fw:~ # service flowd_aggregate status
   flowd_aggregate is running as pid 54675.
   ```
   
   The aggregator is a python script that parses those files and then writes to a bunch of sqlite dbs

   ```
   root@fw:~ # ls -1 /var/netflow/
   dst_port_000300.sqlite
   interface_000030.sqlite
   metadata.sqlite
   src_addr_086400.sqlite
   src_addr_details_086400.sqlite
   ```

### Using ktranslate to receive remote netflow data and export it for prometheus
I never really used `netflow` in my lab in the past but after switching to `OPNsense` I decided to give it a try. I used to use [darkstat](https://redmine.pfsense.org/issues/12658). After doing some research I realized [ktranslate](https://github.com/kentik/ktranslate) can help me [export the metrics to prometheus](https://kb.kentik.com/docs/using-kentik-firehose#ktranslate-output-examples). We can just run the following:

```
docker run -p 8082:8082 kentik/ktranslate:v2 -format prometheus -sinks prometheus -prom_listen=:8084 -listen=0.0.0.0:8082
```

I deployed it to my kubernetes cluster and initially I couldn't see any of the metrics. I enabled debug mode and switched `ktranslate` to print locally for debugging:

```
spec:
containers:
- name: ktranslate
  image: kentik/ktranslate:v2.2.35
  args:
    ### Use this for troubleshooting
    # - -format=flat_json
    # - -format=json
    # - -tee_logs=true
```

And I saw that the `in_bytes` parameter was always 0:

```
{
  "timestamp": 1768184452623720200,
  "dst_as": 15169,
  "dst_geo": "US",
  "header_len": 0,
  "in_bytes": 0,
  "in_pkts": 0,
  "input_port": 3,
  "ip_size": 0,
  "dst_addr": "142.250.72.193",
  "src_addr": "xx.xx.xx.112",
  "l4_dst_port": 443,
  "l4_src_port": 35050,
  "output_port": 1,
  "protocol": "TCP",
  "sampled_packet_size": 0,
  "src_as": 393552,
  "src_geo": "US",
  "tcp_flags": 30,
  "tos": 0,
  "vlan_in": 0,
  "vlan_out": 0,
  "next_hop": "",
  "mpls_type": 0,
  "out_bytes": 0,
  "out_pkts": 0,
  "tcp_rx": 0,
  "src_flow_tags": "",
  "dst_flow_tags": "",
  "sample_rate": 1,
  "device_id": 0,
  "device_name": "10.233.66.182",
  "company_id": 0,
  "dst_bgp_as_path": "",
  "dst_bgp_comm": "",
  "src_bpg_as_path": "",
  "src_bgp_comm": "",
  "src_nexthop_as": 0,
  "dst_nexthop_as": 0,
  "src_geo_region": "",
  "dst_geo_region": "",
  "src_geo_city": "",
  "dst_geo_city": "",
  "dst_nexthop": "",
  "src_nexthop": "",
  "src_route_prefix": "",
  "dst_route_prefix": "",
  "src_second_asn": 0,
  "dst_second_asn": 0,
  "src_third_asn": 0,
  "dst_third_asn": 0,
  "src_eth_mac": "",
  "dst_eth_mac": "",
  "input_int_desc": "",
  "output_int_desc": "",
  "input_int_alias": "",
  "output_int_alias": "",
  "input_int_capacity": 0,
  "output_int_capacity": 0,
  "input_int_ip": "",
  "output_int_ip": "",
  "custom_str": {
    "Type": "NETFLOW_V9",
    "SamplerAddress": "10.233.66.182",
    "FlowDirection": "ingress",
    "src_endpoint": "xx.xx.xx.112:35050",
    "dst_endpoint": "142.250.72.193:443",
    "src_as_name": "COL-LPC",
    "dst_as_name": "GOOGLE",
    "application": "https"
  },
  "eventType": "KFlow",
  "provider": "kentik-flow-device",
  "har_file": null
}
```

I found an [OPNsense Forum](https://forum.opnsense.org/index.php?topic=48539.0) that talks about the issue and apparently that's expected. So I switched to **Netflow v5** and then I started getting data exported:

```
> curl -s http://netflow.kar.int:8084/metrics | grep kflow | head -3
# HELP kflow_bytes_total
# TYPE kflow_bytes_total gauge
kflow_bytes_total{dst_addr="100.50.246.235",l4_dst_port="443",protocol="TCP",src_addr="xx.xx.xx.112"} 3156
```

Pretty nifty setup.