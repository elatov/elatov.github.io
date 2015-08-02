---
published: true
layout: post
title: "Iptables Mod Tee on DD WRT"
author: Karim Elatov
categories: []
tags: []
---
### compile iptables
http://www.spinics.net/lists/netfilter/msg55949.html
http://www.jonisdumb.com/2011/02/compiling-ip6tables-dd-wrt.html

# wget http://www.netfilter.org/projects/iptables/files/iptables-1.4.10.tar.bz2
# tar -xjvf iptables-1.4.10.tar.bz2
# cd iptables-1.4.10

./configure --prefix=/opt --host=arm-linux

### patch iptables for dd-wrt
https://github.com/sabotage-linux/sabotage/blob/master/KEEP/iptables-1.4.14-musl-fixes.patch