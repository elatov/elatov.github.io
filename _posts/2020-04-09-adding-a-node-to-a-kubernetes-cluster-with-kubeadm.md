---
published: true
layout: post
title: "Adding a node to a Kubernetes cluster with kubeadm"
author: Karim Elatov
categories: [containers]
tags: [calico,containerd,kubernetes]
---

I [initially installed](/2018/05/deploy-kubernetes-with-kubeadm-on-ubuntu-1604/) kubernetes with just a one-node setup and I got some new hardware so I wanted to add one more node to the cluster which I previously used `kubeadm` to install. I installed ubuntu on it and then followed the instructions from [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

## Preparing Ubuntu for Kubernetes
I decided to install [containerd](https://containerd.io/) just see how the experience is different from **docker** (the steps are covered in [Container runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd)). Here are the prereqs:

```bash
cat > /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter

# Setup required sysctl params, these persist across reboots.
cat > /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sysctl --system
```

And here is the install:

```bash
# Install containerd
## Set up the repository
### Install packages to allow apt to use a repository over HTTPS
apt-get update && apt-get install -y apt-transport-https ca-certificates curl software-properties-common

### Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

### Add Docker apt repository.
add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

## Install containerd
apt-get update && apt-get install -y containerd.io

# Configure containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

# Restart containerd
systemctl restart containerd
```

Then I installed all the necessary tools:

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

## Joining the Node to the K8S cluster
Then I needed to join this node to the cluster, the steps for that are covered in [Joining your nodes](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#join-nodes), I basically needed to run this:

```bash
kubeadm join --token <token> <control-plane-host>:<control-plane-port> --discovery-token-ca-cert-hash sha256:<hash>
```

To get the token, I logged into my control-plan/master machine and ran the following:

```bash
> kubeadm token list
> kubeadm token create
W0409 09:30:11.962103   31623 configset.go:202] WARNING: kubeadm cannot validate component configs for API groups [kubelet.config.k8s.io kubeproxy.config.k8s.io]
szkbnz.XXX
> kubeadm token list
TOKEN        TTL   EXPIRES                     USAGES                   DESCRIPTION                                                EXTRA GROUPS
szkbnz.XXX   23h   2020-04-10T09:30:11-06:00   authentication,signing   <none>                                                     system:bootstrappers:kubeadm:default-node-token
```

And to get the hash, I ran the following on the same machine:

```bash
> openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
  openssl dgst -sha256 -hex | sed 's/^.* //'
```

Then on my new node, I ran the following:

```bash
elatov@kub2:~$ sudo kubeadm --v=5 join ub:6443 --token szkbnz.XXX --discovery-token-ca-cert-hash sha256:ae850f34XXX
W0409 16:00:30.822400    7861 join.go:346] [preflight] WARNING: JoinControlPane.controlPlane settings will be ignored when control-plane flag is not set.
I0409 16:00:30.822450    7861 join.go:371] [preflight] found NodeName empty; using OS hostname as NodeName
I0409 16:00:30.822487    7861 initconfiguration.go:103] detected and using CRI socket: /run/containerd/containerd.sock
[preflight] Running pre-flight checks
I0409 16:00:30.822580    7861 preflight.go:90] [preflight] Running general checks
I0409 16:00:30.822613    7861 checks.go:249] validating the existence and emptiness of directory /etc/kubernetes/manifests
I0409 16:00:30.822655    7861 checks.go:286] validating the existence of file /etc/kubernetes/kubelet.conf
I0409 16:00:30.822665    7861 checks.go:286] validating the existence of file /etc/kubernetes/bootstrap-kubelet.conf
I0409 16:00:30.822690    7861 checks.go:102] validating the container runtime
I0409 16:00:30.829307    7861 checks.go:376] validating the presence of executable crictl
I0409 16:00:30.829450    7861 checks.go:335] validating the contents of file /proc/sys/net/bridge/bridge-nf-call-iptables
I0409 16:00:30.829527    7861 checks.go:335] validating the contents of file /proc/sys/net/ipv4/ip_forward
I0409 16:00:30.829622    7861 checks.go:649] validating whether swap is enabled or not
I0409 16:00:30.829739    7861 checks.go:376] validating the presence of executable conntrack
I0409 16:00:30.829838    7861 checks.go:376] validating the presence of executable ip
I0409 16:00:30.829941    7861 checks.go:376] validating the presence of executable iptables
I0409 16:00:30.830046    7861 checks.go:376] validating the presence of executable mount
I0409 16:00:30.830118    7861 checks.go:376] validating the presence of executable nsenter
I0409 16:00:30.830219    7861 checks.go:376] validating the presence of executable ebtables
I0409 16:00:30.830338    7861 checks.go:376] validating the presence of executable ethtool
I0409 16:00:30.830442    7861 checks.go:376] validating the presence of executable socat
I0409 16:00:30.830508    7861 checks.go:376] validating the presence of executable tc
I0409 16:00:30.830596    7861 checks.go:376] validating the presence of executable touch
I0409 16:00:30.830652    7861 checks.go:520] running all checks
I0409 16:00:30.843003    7861 checks.go:406] checking whether the given node name is reachable using net.LookupHost
I0409 16:00:30.843252    7861 checks.go:618] validating kubelet version
I0409 16:00:30.890346    7861 checks.go:128] validating if the service is enabled and active
I0409 16:00:30.898783    7861 checks.go:201] validating availability of port 10250
I0409 16:00:30.899033    7861 checks.go:286] validating the existence of file /etc/kubernetes/pki/ca.crt
I0409 16:00:30.899102    7861 checks.go:432] validating if the connectivity type is via proxy or direct
I0409 16:00:30.899183    7861 join.go:441] [preflight] Discovering cluster-info
I0409 16:00:30.899260    7861 token.go:78] [discovery] Created cluster-info discovery client, requesting info from "ub:6443"
I0409 16:00:30.915015    7861 token.go:116] [discovery] Requesting info from "ub:6443" again to validate TLS against the pinned public key
I0409 16:00:30.923321    7861 token.go:133] [discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "ub:6443"
I0409 16:00:30.923339    7861 discovery.go:51] [discovery] Using provided TLSBootstrapToken as authentication credentials for the join process
I0409 16:00:30.923347    7861 join.go:455] [preflight] Fetching init configuration
I0409 16:00:30.923354    7861 join.go:493] [preflight] Retrieving KubeConfig objects
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
I0409 16:00:30.935467    7861 interface.go:400] Looking for default routes with IPv4 addresses
I0409 16:00:30.935577    7861 interface.go:405] Default route transits interface "ens160"
I0409 16:00:30.935736    7861 interface.go:208] Interface ens160 is up
I0409 16:00:30.935898    7861 interface.go:256] Interface "ens160" has 2 addresses :[192.168.1.108/24 fe80::20c:29ff:feab:4769/64].
I0409 16:00:30.936043    7861 interface.go:223] Checking addr  192.168.1.108/24.
I0409 16:00:30.936186    7861 interface.go:230] IP found 192.168.1.108
I0409 16:00:30.936306    7861 interface.go:262] Found valid IPv4 address 192.168.1.108 for interface "ens160".
I0409 16:00:30.936437    7861 interface.go:411] Found active IP 192.168.1.108
I0409 16:00:30.936578    7861 preflight.go:101] [preflight] Running configuration dependant checks
I0409 16:00:30.936688    7861 controlplaneprepare.go:211] [download-certs] Skipping certs download
I0409 16:00:30.936742    7861 kubelet.go:111] [kubelet-start] writing bootstrap kubelet config file at /etc/kubernetes/bootstrap-kubelet.conf
I0409 16:00:30.937671    7861 kubelet.go:119] [kubelet-start] writing CA certificate at /etc/kubernetes/pki/ca.crt
I0409 16:00:30.938679    7861 kubelet.go:145] [kubelet-start] Checking for an existing Node in the cluster with name "kub2" and status "Ready"
I0409 16:00:30.941040    7861 kubelet.go:159] [kubelet-start] Stopping the kubelet
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.18" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...
I0409 16:00:31.679419    7861 cert_rotation.go:137] Starting client certificate rotation controller
I0409 16:00:31.682917    7861 kubelet.go:194] [kubelet-start] preserving the crisocket information for the node
I0409 16:00:31.682932    7861 patchnode.go:30] [patchnode] Uploading the CRI Socket information "/run/containerd/containerd.sock" to the Node API object "kub2" as an annotation

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

I queried the master and I was able to see the node:

```bash
> k get nodes
NAME   STATUS   ROLES    AGE    VERSION
kub2   Ready    <none>   13m    v1.18.1
ub     Ready    master   373d   v1.18.1
```

I also gave it a `label`, just so I can distinguish the machines:

```bash
> k label node kub2 kubernetes.io/role=node
node/kub2 labeled
> k get nodes
NAME   STATUS   ROLES    AGE    VERSION
kub2   Ready    node     27m    v1.18.1
ub     Ready    master   373d   v1.18.1
```

## Fixing Calico Interface
I am using Calico for my CNI and since it installs it as a **Daemonset**, as soon as the node was ready it tried to deploy it but it was failing:

```bash
> kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName=kub2
NAMESPACE     NAME                  READY   STATUS    RESTARTS   AGE    IP               NODE   NOMINATED NODE   READINESS GATES
default       metricbeat-49mwj      0/1     Running   0          156m   10.244.154.196   kub2   <none>           <none>
default       node-exporter-9bqs6   0/1     Running   0          156m   192.168.1.108    kub2   <none>           <none>
kube-system   calico-node-65mf8     0/1     Running   11          70m    192.168.1.108    kub2   <none>           <none>
kube-system   kube-proxy-h5t2w      1/1     Running   1          174m   192.168.1.108    kub2   <none>           <none>
```

I installed the `calicoctl` binary to see if the peer is listed:

```bash
> curl -O -L  https://github.com/projectcalico/calicoctl/releases/download/v3.13.2/calicoctl
> chmod +x calicoctl
> mv calicoctl /usr/local/bin
```

And I was able to check out the settings:

```bash
> DATASTORE_TYPE=kubernetes KUBECONFIG=~/.kube/config calicoctl get nodes
NAME
kub2
ub
> sudo calicoctl node status
[sudo] password for elatov:
Calico process is running.

IPv4 BGP status
+---------------+-------------------+-------+----------+---------+
| PEER ADDRESS  |     PEER TYPE     | STATE |  SINCE   |  INFO   |
+---------------+-------------------+-------+----------+---------+
| 192.168.1.108 | node-to-node mesh | start | 16:01:10 | Passive |
+---------------+-------------------+-------+----------+---------+

IPv6 BGP status
No IPv6 peers found.
```

If it's able to establish the peer the **state** would show **established**. Checking out the events of the cluster, I actually saw the error from **calico**:

```bash
> k get events --sort-by='.metadata.creationTimestamp' -A | tail
kube-system   1s          Normal    Created            pod/calico-node-kt5dj   Created container calico-node
kube-system   0s          Normal    Started            pod/calico-node-kt5dj   Started container calico-node
kube-system   2m39s       Warning   Unhealthy          pod/calico-node-jkxvk   (combined from similar events): Readiness probe failed: calico/node is not ready: BIRD is not ready: BGP not established with 172.18.0.12020-04-09 17:42:29.565 [INFO][17961] health.go 156: Number of node(s) with BGP peering established = 0
```

You can see the same error if you describe the pod:

```bash
> k describe pod -n kube-system calico-node-jkxvk | grep kub2
Node:                 kub2/192.168.1.108
  Warning  Unhealthy  3m56s (x441 over 77m)  kubelet, kub2  (combined from similar events): Readiness probe failed: calico/node is not ready: BIRD is not ready: BGP not established with 172.18.0.12020-04-09 17:27:29.563 [INFO][15003] health.go 156: Number of node(s) with BGP peering established = 0
```

I noticed that it's trying to reach the **172.18.0.1** IP which is the IP of the *bridge*:

```bash
> ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 192.168.1.106/24 brd 192.168.1.255 scope global ens9
       valid_lft forever preferred_lft forever
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
5: br-b20791438eae: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-b20791438eae
       valid_lft forever preferred_lft forever
69: tunl0@NONE: <NOARP,UP,LOWER_UP> mtu 1440 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.244.35.128/32 brd 10.244.35.128 scope global tunl0
       valid_lft forever preferred_lft forever
```

It looks like someone ran into a similar issue that was discussed in [calico/node is not ready: BIRD is not ready: BGP not established](https://github.com/projectcalico/calico/issues/2561) and it looks like we can specify the **IP_AUTODETECTION_METHOD** option to **calico** and it should use the appropriate interface. So after reading over the [Change the autodetection method](https://docs.projectcalico.org/networking/ip-autodetection#change-the-autodetection-method), I saw that I can run the following to update it:

```bash
> k set env daemonset/calico-node -n kube-system IP_AUTODETECTION_METHOD=interface=en.*
```
And the pods were automatically restarted to apply the new change. I then saw the following:

```bash
> sudo calicoctl node status
Calico process is running.

IPv4 BGP status
+---------------+-------------------+-------+----------+-------------+
| PEER ADDRESS  |     PEER TYPE     | STATE |  SINCE   |    INFO     |
+---------------+-------------------+-------+----------+-------------+
| 192.168.1.108 | node-to-node mesh | up    | 17:45:10 | Established |
+---------------+-------------------+-------+----------+-------------+

IPv6 BGP status
No IPv6 peers found.
```

## Checking out the Running Containers with Containerd
I wanted to make sure I see the containers running on the new node, even after `kubectl` showed them as running, just to see what tools are available for **containerd**. It looks like there is a utility called `ctr` which acts as a client to `containerd`. First you list events to find out what namespace the containers are running under:

```bash
$ ctr events
2020-04-09 17:06:55.92398331 +0000 UTC k8s.io /tasks/exit {"container_id":"22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece","id":"5e4216d6ef213eec558433a60e31e102519bf54938888cf14fa10fd2fcb909d5","pid":23094,"exit_status":137,"exited_at":"2020-04-09T17:06:55.897861206Z"}
2020-04-09 17:06:55.940421199 +0000 UTC k8s.io /tasks/exec-started {"container_id":"22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece","exec_id":"3ee78a65086d4769d02b0820e155b803942545f329ff9aff476d8adb766dcd89","pid":23169}
2020-04-09 17:06:58.213396812 +0000 UTC k8s.io /tasks/exec-started {"container_id":"22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece","exec_id":"97b1677ceae501e033404561793fc577f3b7df0ae1ceb6d66b3ada499b4ec957","pid":23194}
2020-04-09 17:06:58.236533924 +0000 UTC k8s.io /tasks/exit {"container_id":"22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece","id":"97b1677ceae501e033404561793fc577f3b7df0ae1ceb6d66b3ada499b4ec957","pid":23194,"exited_at":"2020-04-09T17:06:58.213351983Z"}
```

You'll noctice it's under **k8s.io**, you could also run the following:

```bash
$ ctr namespaces list
NAME   LABELS
k8s.io
```

The `events` also show that something is starting and stopping. Next we can list all the containers in that namespace:

```bash
$ ctr -n k8s.io c ls
CONTAINER                                                           IMAGE                                                                      RUNTIME
22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece    sha256:dbefecbff1972984f5b1214bdfc2363c965f455b132a3fa130111b0c0d44c31b    io.containerd.runtime.v1.linux
3919babc53160ef34049b89de2c442600793d643dbf79b74a06bc76c9d3464f2    docker.io/calico/node:v3.13.1                                              io.containerd.runtime.v1.linux
4a8413c1150e3976310f52a494622f2f98dcba17ccb74c163468345ae01da0bd    sha256:e5a616e4b9cf68dfcad7782b78e118be4310022e874d52da85c55923fb615f87    io.containerd.runtime.v1.linux
63724d930059ffa97f6cb16cc83d7840cc0ce8247999415c7598f3dd2ae8ad5a    docker.io/calico/cni:v3.13.1                                               io.containerd.runtime.v1.linux
```

You can also check out all the images as well:

```bash
$ ctr -n k8s.io i ls
REF                                                                                                         TYPE                                                      DIGEST                                                                  SIZE      PLATFORMS                                                   LABELS
docker.elastic.co/beats/metricbeat:7.5.1                                                                    application/vnd.docker.distribution.manifest.v2+json      sha256:c41ee1ec9628157adb2455e9a7d3f9e33ffa1704aca151a960a201a407c87c5c 161.2 MiB linux/amd64                                                 io.cri-containerd.image=managed
docker.elastic.co/beats/metricbeat@sha256:c41ee1ec9628157adb2455e9a7d3f9e33ffa1704aca151a960a201a407c87c5c  application/vnd.docker.distribution.manifest.v2+json      sha256:c41ee1ec9628157adb2455e9a7d3f9e33ffa1704aca151a960a201a407c87c5c 161.2 MiB linux/amd64                                                 io.cri-containerd.image=managed
docker.io/calico/cni:v3.13.1                                                                                application/vnd.docker.distribution.manifest.list.v2+json sha256:c699d5ec4d0799ca5785e9134cfb1f55a1376ebdbb607f5601394736fceef7c8 63.4 MiB  linux/amd64,linux/arm64,linux/ppc64le                       io.cri-containerd.image=managed
```

You could do it with an environment variable as well:

```bash
$ export CONTAINERD_NAMESPACE=k8s.io
$ ctr c ls
CONTAINER                                                           IMAGE                                                                      RUNTIME
22289fcb84d31745188db683631c7e49a92b4539fb1b49d5e46a3021ef724ece    sha256:dbefecbff1972984f5b1214bdfc2363c965f455b132a3fa130111b0c0d44c31b    io.containerd.runtime.v1.linux
3919babc53160ef34049b89de2c442600793d643dbf79b74a06bc76c9d3464f2    docker.io/calico/node:v3.13.1                                              io.containerd.runtime.v1.linux
```

### Starting a container with containerd
As I was trying to figure out all the running containers with **containerd**, I decided to deploy an example container just to see how it behaves. Here is how I achieved my goal, first download the image:

```bash
$ ctr i pull docker.io/library/busybox:latest
docker.io/library/busybox:latest:                                                 resolved       |++++++++++++++++++++++++++++++++++++++|
index-sha256:b26cd013274a657b86e706210ddd5cc1f82f50155791199d29b9e86e935ce135:    done           |++++++++++++++++++++++++++++++++++++++|
manifest-sha256:afe605d272837ce1732f390966166c2afff5391208ddd57de10942748694049d: done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:0669b0daf1fba90642d105f3bc2c94365c5282155a33cc65ac946347a90d90d1:    done           |++++++++++++++++++++++++++++++++++++++|
config-sha256:83aa35aa1c79e4b6957e018da6e322bfca92bf3b4696a211b42502543c242d6f:   done           |++++++++++++++++++++++++++++++++++++++|
elapsed: 1.0 s                                                                    total:  3.8 Ki (3.8 KiB/s)
unpacking linux/amd64 sha256:b26cd013274a657b86e706210ddd5cc1f82f50155791199d29b9e86e935ce135...
done
```

Next let's run the image:

```bash
$ ctr run docker.io/library/busybox:latest busybox --rm -d
$ ctr c ls
CONTAINER    IMAGE                               RUNTIME
busybox      docker.io/library/busybox:latest    io.containerd.runtime.v1.linux
```

Next let's `exec` into the container, first find the specific container/**task** from the launched container:

```bash
$ ctr task list
TASK       PID     STATUS
busybox    4196    RUNNING
```

And now for the `exec`:

```bash
$ ctr t exec -t --exec-id exec-test busybox /bin/sh
/ # ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh
   12 root      0:00 /bin/sh
   17 root      0:00 ps
```

And finally let's stop the task:

```bash
$ ctr t kill -s 9 busybox
$ ctr t ls
TASK       PID     STATUS
busybox    4196    STOPPED
```

And finally let's delete the container:

```bash
$ ctr c ls
CONTAINER    IMAGE                               RUNTIME
busybox      docker.io/library/busybox:latest    io.containerd.runtime.v1.linux
$ ctr c  rm busybox
$ ctr c ls
CONTAINER    IMAGE    RUNTIME
```

