---
published: true
layout: post
title: "Kubespray random networking troubleshooting"
author: Karim Elatov
categories: [networking, containers]
tags: [kubespray, ipvs, ingress-nginx, metallb]
---

I did my regular kubespray upgrade and after the upgrade some things stopped working. Here are some issues I ran into.

## DNS failures

After the upgrade I started seeing the `nodelocaldns` pods show a bunch of `permission denied` messages:

```
```

As a quick test I decided to disable [that feature](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/dns-stack.md#nodelocal-dns-cache):

```
enable_nodelocaldns: false
```

And then perform an upgrade, but after that `nodelocaldns` was still running. Looking at the [reset.yaml](https://github.com/kubernetes-sigs/kubespray/blob/master/roles/reset/tasks/main.yml), it looks like we delete the interface, so it would've been better to just delete the interface on all the nodes:

```
ip link del nodelocaldns
```

And also delete the `daemonset`:

```
k delete -n kube-system ds nodelocaldns
```

However it also looks like the IP is passed to the `kubeadm` config:

```
> grep clusterDNS /etc/kubernetes/kubeadm-config.yaml -A 1
clusterDNS:
- 10.233.0.3
```

And when I started to take a closer look. Listing the services, I actually had two:

```
> k get svc -n kube-system | grep dns
coredns          ClusterIP   10.233.0.3     <none>        53/UDP,53/TCP,9153/TCP   505d
kube-dns         ClusterIP   10.233.0.10    <none>        53/UDP,53/TCP,9153/TCP   505d
```

Going to the first one failed:

```
> nslookup kubernetes 10.233.0.3
;; UDP setup with 10.233.0.3#53(10.233.0.3) for kubernetes failed: permission denied.
;; no servers could be reached

;; UDP setup with 10.233.0.3#53(10.233.0.3) for kubernetes failed: permission denied.
;; no servers could be reached
```

But going to the second one worked:

```
> nslookup kubernetes 10.233.0.10
Server:		10.233.0.10
Address:	10.233.0.10#53

Name:	kubernetes.default.svc.cluster.local
Address: 10.233.0.1
```

Then by chance, I started comparing the two and I noticed the following difference:

```
> k get svc -n kube-system kube-dns -o jsonpath='{.spec.ports[?(@.name=="dns")]}' | jq
{
  "name": "dns",
  "port": 53,
  "protocol": "UDP",
  "targetPort": 53
}
```

Vs. the non-working one:

```
> k get svc -n kube-system coredns -o jsonpath='{.spec.ports[?(@.name=="dns")]}' | jq
{
  "name": "dns",
  "port": 53,
  "protocol": "UDP",
  "targetPort": "dns-tcp"
}
```

I also found a [known issue](https://github.com/kubernetes-sigs/kubespray/issues/10860) for that. Hopefully it will be fixed in the upcoming release.

## Nginx Ingress unreachable
I kept getting `connection resets` when trying to connect to nginx ingress:

```
> curl https://nginx.kar.int
curl: (7) Failed to connect to nginx.kar.int port 443 after 104 ms: Connection refused
```

### IPVS troubleshooting
Initially I thought it was an issue with `ipvs`. I checked the created `ingress` CRs and they looked good:

```
> k get ing
NAME                CLASS    HOSTS                             ADDRESS        PORTS     AGE
svc-int   <none>   nginx.kar.int                   192.168.1.52   80        68d
```

I then checked out the service and I saw it configured as a load balancer:

```
> k get svc -n ingress-nginx
NAME            TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                      AGE
ingress-nginx   LoadBalancer   10.233.45.20   192.168.1.203   80:31742/TCP,443:31456/TCP   94m
```

When I tried to reach it locally from the node, I received a similar message:

```
> curl -H "Host: nginx.kar.int" https://192.168.1.203/
curl: (7) Failed to connect to nginx.kar.int port 443 after 10 ms: Connection refused
```

I then checked on the local interface and I noticed the `kube-ipvs0` interface is down:

```
> ip -4 -br a
lo               UNKNOWN        127.0.0.1/8
ens18            UP             192.168.1.51/24
kube-ipvs0       DOWN           10.233.0.10/32 10.233.24.81/32 10.233.0.1/32 10.233.31.102/32 192.168.1.202/32 10.233.59.172/32 10.233.21.213/32 10.233.45.95/32 10.233.3.240/32 192.168.1.201/32 10.233.27.160/32 192.168.1.200/32 10.233.36.34/32 10.233.0.3/32 10.233.51.187/32 10.233.39.70/32 10.233.0.107/32 10.233.55.59/32 10.233.45.20/32 10.233.41.13/32 10.233.37.9/32 10.233.24.68/32 10.233.23.197/32 10.233.9.95/32 10.233.59.87/32 10.233.28.206/32 10.233.35.36/32 10.233.51.89/32
cilium_host@cilium_net UP             10.233.64.84/32
```

I initially I thought that was a problem, but then I ran into [this old issue](https://github.com/kubernetes/kubernetes/issues/107662#issuecomment-1017894646) which described why this is expected. Next, I ran into a couple of other issues:

- https://github.com/kubernetes-sigs/kubespray/issues/10572
- https://github.com/kubernetes/kubernetes/issues/121272

These bug helped me to take a look at the `ipvadm` output. And here is what I saw:

```
> sudo ipvsadm -L -n -t 192.168.1.203:443
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  192.168.1.200:443 rr
```

At this point I realized my service doesn't have any endpoints:

```
> k get ep -n ingress-nginx
NAME            ENDPOINTS  AGE
ingress-nginx              120m
```

But I did see the pods running:

```
> k get po -n ingress-nginx
NAME                             READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-ldrdj   1/1     Running   0          64m
ingress-nginx-controller-mjdmp   1/1     Running   0          65m
ingress-nginx-controller-sc88v   1/1     Running   0          63m
```

So i checked out the `selectors`:

```
> k get svc -n ingress-nginx ingress-nginx -o jsonpath={.spec.selector} | jq
{
  "app.kubernetes.io/name": "ingress-nginx"
  "app.kubernetes.io/port-of": "ingress-nginx"
}
```

And then I checked out the daemonset:

```
> k get ds -n ingress-nginx ingress-nginx-controller -o jsonpath={.spec.template.metadata.labels} | jq
{
  "app.kubernetes.io/name": "ingress-nginx",
  "app.kubernetes.io/part-of": "ingress-nginx"
}
```
And this was a [known issues](https://github.com/kubernetes-sigs/kubespray/issues/10969) as well. After fixing the `selector`, I saw the right configuration in `ipvsadm`:

```
> sudo ipvsadm -L -n -t 192.168.1.200:443
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  192.168.1.200:443 rr
  -> 10.233.64.196:443            Masq    1      0          0
  -> 10.233.65.45:443             Masq    1      0          0
  -> 10.233.66.18:443             Masq    1      0          0
```

### External-IP Changed
After fixing the above, I realized I still can't reach the service. I logged into my upstream switch and I realized I was pointing to a different IP:

```
# iptables -L -n -v -t nat | grep 443
79607 4582K DNAT       tcp  --  *      *       0.0.0.0/0            192.168.56.151       tcp dpt:443 to:192.168.1.200  
```

I then discovered that there is a [new feature](https://github.com/kubernetes-sigs/kubespray/pull/10925) that was added to create a service for the ingress-nginx daemonset. This has been a [feature request](https://github.com/kubernetes-sigs/kubespray/issues/10373) for a while. To fix the issue I needed to add a label to use an existing MetalLB:

```
> cat ingress-nginx-svc.yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    metallb.universe.tf/allow-shared-ip: ingress
    metallb.universe.tf/ip-allocated-from-pool: primary
  labels:
    app.kubernetes.io/name: ingress-nginx
  name: ingress-nginx
  namespace: ingress-nginx
spec:
  allocateLoadBalancerNodePorts: true
  loadBalancerIP: 192.168.1.200
```

This is described in the [documentation for MetalLB](https://metallb.universe.tf/usage/#requesting-specific-ips). I hope we can customize the ingress-nginx service further and we can just pass those as a variable to kubespray in later releases.
