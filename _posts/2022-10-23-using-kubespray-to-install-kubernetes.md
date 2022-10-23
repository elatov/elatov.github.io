---
published: true
layout: post
title: "Using Kubespray to Install Kubernetes"
author: Karim Elatov
categories: [networking, containers]
tags: [kubespray, kubernetes, metallb, nginx-ingress, cilium, ansible]
---
I wanted to try out [kubespray](https://github.com/kubernetes-sigs/kubespray) to see if I can do an update all in one swoop (control plane and nodes). 

## Prequisites
Let's install the prequisites (from [debian](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/debian.md) docs and also the [Installing Ansible on Debian](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html#installing-ansible-on-debian) page), first let's install `ansible`:

```bash
$ echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu focal main' | sudo tee -a /etc/apt/sources.list.d/anisble.list
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
$ sudo apt update
$ sudo apt install ansible
```

Then let's download the source code:

```bash
$ git clone https://github.com/kubernetes-sigs/kubespray.git
$ cd kubespray
# get the version that supports your k8s version, I grabbed the latest at the time
$ git checkout v2.20.0
# or
$ git clone --branch v2.20.0 https://github.com/kubernetes-sigs/kubespray
$ cd kubespray
# let's install the python requirements
$ sudo pip3 install -U -r requirements.txt
```

Now let's generate the inventory files (from [Quick Start](https://github.com/kubernetes-sigs/kubespray#quick-start)):

```bash
# Copy ``inventory/sample`` as ``inventory/mycluster``
$ cp -rfp inventory/sample inventory/home
# Update Ansible inventory file with inventory builder
$ declare -a IPS=(192.168.1.51 192.168.1.52 192.168.1.53)
$ CONFIG_FILE=inventory/home/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

Before running the the install I decided to enable [MetalLB](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/metallb.md):

```bash
# inventory/home/group_vars/k8s_cluster/k8s-cluster.yaml
kube_proxy_strict_arp: true
# inventory/home/group_vars/k8s_cluster/addons.yml
metallb_enabled: true
metallb_speaker_enabled: true
metallb_avoid_buggy_ips: true
# this is range of IPs that is in the same subnet as the k8s nodes
metallb_ip_range:
  - 192.168.1.200-192.168.1.220
```

Also to use [cilium](https://github.com/kubernetes-sigs/kubespray#network-plugins):

```bash
# inventory/home/group_vars/k8s_cluster/k8s-cluster.yaml
kube_network_plugin: cilium
```

And lastly to enable [nginx-ingress](https://github.com/kubernetes-sigs/kubespray/issues/7190):

```bash
# inventory/home/group_vars/k8s_cluster/addons.yml
ingress_nginx_enabled: true
ingress_nginx_host_network: false
ingress_publish_status_address: ""
```

## Installing with kubespray
The install it self was pretty simple, it's covered in
[Setting up your first cluster with Kubespray](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/setting-up-your-first-cluster.md)
and [Getting started](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md):

```bash
$ ansible-playbook -i inventory/home/hosts.yaml  --become --become-user=root cluster.yml
...
...
PLAY RECAP ***********************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ma                         : ok=766  changed=126  unreachable=0    failed=0    skipped=1226 rescued=0    ignored=5
nc                         : ok=486  changed=73   unreachable=0    failed=0    skipped=685  rescued=0    ignored=1
nd                         : ok=486  changed=73   unreachable=0    failed=0    skipped=685  rescued=0    ignored=1

Sunday 16 October 2022  21:06:30 -0600 (0:00:00.088)       0:18:29.934 ********
====================================================================
download : download_container | Download image if required ----------------------------------------------- 141.63s
network_plugin/cilium : Cilium | Wait for pods to run ------------------------------------------------------------- 93.95s
download : download_container | Download image if required ------------------------------------------------- 43.38s
download : download_file | Download item -------------------------------------------------------------------------- 37.10s
download : download_container | Download image if required-------------------------------------------------- 34.66s
kubernetes/kubeadm : Join to cluster ---------------------------------------------------------------------------------- 31.06s
download : download_container | Download image if required -------------------------------------------------- 22.52s
download : download_container | Download image if required -------------------------------------------------- 22.02s
kubernetes/control-plane : kubeadm | Initialize first master ------------------------------------------------------ 18.55s
download : download_container | Download image if required --------------------------------------------------- 17.72s
download : download_container | Download image if required --------------------------------------------------- 16.08s
download : download_container | Download image if required --------------------------------------------------- 15.96s
kubernetes-apps/ansible : Kubernetes Apps | Start Resources ---------------------------------------------------- 12.35s
download : download_container | Download image if required --------------------------------------------------- 11.96s
download : download_file | Download item ---------------------------------------------------------------------------- 11.12s
network_plugin/cilium : Cilium | Start Resources --------------------------------------------------------------------- 10.78s
kubernetes/preinstall : Update package management cache (APT) ---------------------------------------------- 10.00s
download : download_container | Download image if required ----------------------------------------------------- 9.56s
kubernetes/node : install | Copy kubelet binary from download dir ------------------------------------------------ 9.45s
download : download_container | Download image if required ------------------------------------------------------ 9.11s
```

After the install is finished ssh to one of the controller nodes and grab the `kubeconfig`:

```bash
$ sudo cp /etc/kubernetes/admin.conf ~/.kube/config
$ sudo chown $UID:$UID ~/.kube/config
```

At the end here are the pods that were running on the k8s cluster:

```bash
$ k get pods -A
NAMESPACE        NAME                               READY   STATUS    RESTARTS   AGE
ingress-nginx    ingress-nginx-controller-gzs6v     1/1     Running   0          4m5s
ingress-nginx    ingress-nginx-controller-z2sbc     1/1     Running   0          4m38s
ingress-nginx    ingress-nginx-controller-zjwxq     1/1     Running   0          5m10s
kube-system      cilium-fxx2t                       1/1     Running   0          4m2s
kube-system      cilium-hchk2                       1/1     Running   0          4m2s
kube-system      cilium-lj4jx                       1/1     Running   0          4m2s
kube-system      cilium-operator-57bb669bf6-7h5ff   1/1     Running   0          4m3s
kube-system      cilium-operator-57bb669bf6-z4q4q   1/1     Running   0          4m3s
kube-system      coredns-59d6b54d97-4jpbp           1/1     Running   0          116s
kube-system      coredns-59d6b54d97-9v2br           1/1     Running   0          107s
kube-system      dns-autoscaler-78676459f6-45vfs    1/1     Running   0          112s
kube-system      kube-apiserver-ma                  1/1     Running   1          5m32s
kube-system      kube-controller-manager-ma         1/1     Running   1          5m32s
kube-system      kube-proxy-5t2wl                   1/1     Running   0          4m32s
kube-system      kube-proxy-d4spv                   1/1     Running   0          4m32s
kube-system      kube-proxy-d5x9z                   1/1     Running   0          4m32s
kube-system      kube-scheduler-ma                  1/1     Running   1          5m40s
kube-system      metrics-server-65bb5dbd44-9czsz    1/1     Running   0          97s
kube-system      nginx-proxy-nc                     1/1     Running   0          4m34s
kube-system      nginx-proxy-nd                     1/1     Running   0          4m34s
kube-system      nodelocaldns-m4fns                 1/1     Running   0          110s
kube-system      nodelocaldns-nb675                 1/1     Running   0          110s
kube-system      nodelocaldns-p86bk                 1/1     Running   0          110s
metallb-system   controller-789c9bcb6-vtlst         1/1     Running   0          88s
metallb-system   speaker-p4t7v                      1/1     Running   0          88s
metallb-system   speaker-vhqrz                      1/1     Running   0          88s
metallb-system   speaker-xlgwh                      1/1     Running   0          88s
```

Now confirm outbound traffic is working:

```
elatov@ma:~$ kubectl run myshell1 -it --rm --image busybox -- sh
If you don't see a command prompt, try pressing enter.
/ # ping -c 2 google.com
PING google.com (142.250.72.46): 56 data bytes
64 bytes from 142.250.72.46: seq=0 ttl=117 time=31.695 ms
64 bytes from 142.250.72.46: seq=1 ttl=117 time=31.465 ms

--- google.com ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 31.465/31.580/31.695 ms
```

## To perform an upgrade
Most of the instructions are laid out in [Upgrades](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/upgrades.md).
The safest thing to do is either modify the `group_vars` file:

```bash
> grep -r kube_version *
group_vars/k8s_cluster/k8s-cluster.yml:#kube_version: v1.24.6
group_vars/k8s_cluster/k8s-cluster.yml:kube_version: v1.23.9
```

Or you can also pass it into as an extra variable:

```bash
$ ansible-playbook upgrade-cluster.yml -b -i inventory/home/hosts.yaml -e kube_version=v1.19.7
...
PLAY RECAP ****************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ma                         : ok=752  changed=59   unreachable=0    failed=0    skipped=1526 rescued=0    ignored=1
nc                         : ok=478  changed=24   unreachable=0    failed=0    skipped=735  rescued=0    ignored=1
nd                         : ok=478  changed=24   unreachable=0    failed=0    skipped=735  rescued=0    ignored=1

Sunday 16 October 2022  21:42:15 -0600 (0:00:00.089)       0:14:45.172 ********
===============================================================================
kubernetes/control-plane : kubeadm | Upgrade first master -------------------------------------------------------------------------------------------------------------------------------------------- 101.72s
download : download_container | Download image if required -------------------------------------------------------------------------------------------------------------------------------------------- 21.49s
download : download_container | Download image if required -------------------------------------------------------------------------------------------------------------------------------------------- 16.24s
download : download_container | Download image if required -------------------------------------------------------------------------------------------------------------------------------------------- 16.07s
kubernetes-apps/ansible : Kubernetes Apps | Start Resources ------------------------------------------------------------------------------------------------------------------------------------------- 10.40s
kubernetes-apps/ansible : Kubernetes Apps | Start Resources ------------------------------------------------------------------------------------------------------------------------------------------- 10.36s
download : download_container | Download image if required --------------------------------------------------------------------------------------------------------------------------------------------- 9.44s
kubernetes-apps/ansible : Kubernetes Apps | Lay Down CoreDNS templates --------------------------------------------------------------------------------------------------------------------------------- 7.99s
upgrade/pre-upgrade : Drain node ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- 7.46s
kubernetes-apps/ansible : Kubernetes Apps | Lay Down CoreDNS templates --------------------------------------------------------------------------------------------------------------------------------- 7.24s
network_plugin/cilium : Cilium | Start Resources ------------------------------------------------------------------------------------------------------------------------------------------------------- 6.95s
upgrade/pre-upgrade : Drain node ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- 6.73s
network_plugin/cilium : Cilium | Create Cilium node manifests ------------------------------------------------------------------------------------------------------------------------------------------ 6.67s
container-engine/validate-container-engine : Populate service facts ------------------------------------------------------------------------------------------------------------------------------------ 6.46s
kubernetes-apps/metrics_server : Metrics Server | Apply manifests -------------------------------------------------------------------------------------------------------------------------------------- 6.35s
etcd : reload etcd ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 6.34s
kubernetes-apps/metrics_server : Metrics Server | Apply manifests -------------------------------------------------------------------------------------------------------------------------------------- 6.28s
container-engine/validate-container-engine : Populate service facts ------------------------------------------------------------------------------------------------------------------------------------ 6.06s
kubernetes-apps/metrics_server : Metrics Server | Create manifests ------------------------------------------------------------------------------------------------------------------------------------- 6.05s
kubernetes-apps/metrics_server : Metrics Server | Create manifests ------------------------------------------------------------------------------------------------------------------------------------- 6.04s
```


## To Reset
To reset we can follow instructions from [Reset A Kubernetes Cluster Using Kubespray](https://d-nix.nl/2020/06/reset-a-kubernetes-cluster-using-kubespray/):


```bash
# to Reset
ansible-playbook -i inventory/remko/hosts.yaml reset.yml --become --become-user=root
# to reinstall
ansible-playbook -i inventory/home/hosts.yaml cluster.yml --become --become-user=root
```

## Exposing a simple service with an Ingress
Since I am using `MetalLB` and `Nginx Ingress`, first I created a service for the Ingress Controllers
of type `LoadBalancer`:

```bash
apiVersion: v1
kind: Service
metadata:
  labels:
    app: ingress-nginx
  name: ingress-nginx
  namespace: ingress-nginx
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: http
  selector:
    app.kubernetes.io/name: ingress-nginx
```

After creating that I saw the service created:

```bash
$ k get svc -n ingress-nginx
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
ingress-nginx   LoadBalancer   10.233.38.149   192.168.1.200   80:31742/TCP   71m
```

To make sure we can at least reach the LB VIP, we can use `arping` on any machine within the same subnet:

```bash
> sudo arping 192.168.1.200 -c 3
ARPING 192.168.1.200 from 192.168.1.103 eno1
Unicast reply from 192.168.1.200 [00:50:56:90:30:4A]  0.813ms
Unicast reply from 192.168.1.200 [00:50:56:90:30:4A]  1.525ms
Unicast reply from 192.168.1.200 [00:50:56:90:30:4A]  0.997ms
Sent 3 probes (1 broadcast(s))
Received 3 response(s)
```

If you had already reached out to the host directly (via `ssh` or `ping`), you can check out the `arp` table and
you will see which node's MAC address which is responding (in the example below it's `192.168.1.52`):

```bash
> arp -a | grep '4a '
? (192.168.1.200) at 00:50:56:90:30:4a [ether] on eno1
nc.kar.int (192.168.1.52) at 00:50:56:90:30:4a [ether] on eno1
```

Or you can also ping the VIP from another subnet:

```bash
> ping 192.168.1.200 -c 3
PING 192.168.1.200 (192.168.1.200) 56(84) bytes of data.
64 bytes from 192.168.1.200: icmp_seq=1 ttl=63 time=3.19 ms
64 bytes from 192.168.1.200: icmp_seq=2 ttl=63 time=0.431 ms
64 bytes from 192.168.1.200: icmp_seq=3 ttl=63 time=0.595 ms

--- 192.168.1.200 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.431/1.406/3.192/1.264 ms
```

Then I created an ingress:

```bash
$ cat ingress-int.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: baz-int
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: baz.kar.int
    http:
      paths:
      - path: "/"
        pathType: Prefix
        backend:
          service:
            name: baz
            port:
              number: 6880
```

You will see the ingress created:

```bash
$ k get ing
NAME      CLASS    HOSTS         ADDRESS                                  PORTS     AGE
baz-int   <none>   baz.kar.int   192.168.1.51,192.168.1.52,192.168.1.53   80        73s
```

And you will see the addresses of all the nodes. Then as as quick test let's make sure we can reach the
service:

```bash
> curl -I http://192.168.1.200 -H "Host: baz.kar.int"
HTTP/1.1 200 OK
Date: Sat, 22 Oct 2022 19:33:17 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1633
Connection: keep-alive
Access-Control-Allow-Origin: *
```

Very glad that worked out.
