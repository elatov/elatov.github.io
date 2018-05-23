---
published: true
layout: post
title: "Deploy Kuberbetes with kubeadm on Ubuntu 16.04"
author: Karim Elatov
categories: [containers]
tags: [kubernetes,docker,kubeadm,kubectl]
---
### kubeadm
After manually deploying **kubernetes** on my [CoreOS machine](/2018/05/manually-deploy-kubernetes-on-coreos/), I decided to try out some of the tools that facilitate the **kuberbetes** deployment. The one that stood out the most to me was [kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/). So let's give it a shot.

### Install kubeadm
Most of the instructions are laid out in [Installing kubeadm](https://kubernetes.io/docs/setup/independent/install-kubeadm/). First install **docker**:

	sudo apt update
	sudo apt install -y docker.io

Then install **kubernetes** and **kubeadm**:

	sudo apt update
	sudo apt install -y apt-transport-https
	curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	sudo su -c "cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
	deb http://apt.kubernetes.io/ kubernetes-xenial main
	EOF"
	sudo apt update
	sudo apt install -y kubelet kubeadm kubectl

And that should be it.
### Create the kubernetes cluster with kubeadm

Following the instructions from the above page, I ran the following to initiate the **kubernetes** cluster:

	root@ub:~# kubeadm init --pod-network-cidr=10.244.0.0/16
	[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
	[init] Using Kubernetes version: v1.8.3
	[init] Using Authorization modes: [Node RBAC]
	[preflight] Running pre-flight checks
	[preflight] WARNING: Running with swap on is not supported. Please disable swap or set kubelet's --fail-swap-on flag to false.
	[preflight] Starting the kubelet service
	[kubeadm] WARNING: starting in 1.8, tokens expire after 24 hours by default (if you require a non-expiring token use --token-ttl 0)
	[certificates] Generated ca certificate and key.
	[certificates] Generated apiserver certificate and key.
	[certificates] apiserver serving cert is signed for DNS names [ub kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.1.106]
	[certificates] Generated apiserver-kubelet-client certificate and key.
	[certificates] Generated sa key and public key.
	[certificates] Generated front-proxy-ca certificate and key.
	[certificates] Generated front-proxy-client certificate and key.
	[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
	[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"
	[controlplane] Wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
	[controlplane] Wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
	[controlplane] Wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
	[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
	[init] Waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests"
	[init] This often takes around a minute; or longer if the control plane images have to be pulled.
	[apiclient] All control plane components are healthy after 28.002743 seconds
	[uploadconfig] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
	[markmaster] Will mark node ub as master by adding a label and a taint
	[markmaster] Master ub tainted and labelled with key/value: node-role.kubernetes.io/master=""
	[bootstraptoken] Using token: f37d14.650c3c609175ff3e
	[bootstraptoken] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
	[bootstraptoken] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
	[bootstraptoken] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
	[bootstraptoken] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
	[addons] Applied essential addon: kube-dns
	[addons] Applied essential addon: kube-proxy
	
	Your Kubernetes master has initialized successfully!
	
	To start using your cluster, you need to run (as a regular user):
	
	  mkdir -p $HOME/.kube
	  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	  sudo chown $(id -u):$(id -g) $HOME/.kube/config
	
	You should now deploy a pod network to the cluster.
	Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
	  http://kubernetes.io/docs/admin/addons/
	
	You can now join any number of machines by running the following on each node
	as root:
	
	  kubeadm join --token f37d14.650c3c609175ff3e 192.168.1.106:6443 --discovery-token-ca-cert-hash sha256:05bf820daaa0a8706710257eaea18986124537499a637294d2ddf3141ca0ce26

If you want to fix the **swap** warning, you can follow the steps laid out in [kubeadm init --kubernetes-version=v1.8.0 fail with connection refuse for Get http://localhost:10255/healthz #53333](https://github.com/kubernetes/kubernetes/issues/53333#issuecomment-333965512):

> * kubeadm reset
* add "Environment="KUBELET_EXTRA_ARGS=--fail-swap-on=false"" to /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
* systemctl daemon-reload
* systemctl restart kubelet
* kubeadm init

#### Create the kubectl config
We can just follow the instructions provided from the **kubeadm init** ouput:

	elatov@ub:~$ mkdir -p $HOME/.kube
	elatov@ub:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	elatov@ub:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config

#### Install flannel
I decided to use **flannel** for the overlay network since I was familiar with it from the CoreOS setup:

	elatov@ub:~$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.0/Documentation/kube-flannel.yml
	clusterrole "flannel" created
	clusterrolebinding "flannel" created
	serviceaccount "flannel" created
	configmap "kube-flannel-cfg" created
	daemonset "kube-flannel-ds" created

#### Confirm all the Kubernetes Settings
Next lets allow our master node to deploy pods:

	elatov@ub:~$ kubectl taint nodes --all node-role.kubernetes.io/master-
	node "ub" untainted

After that you should see your node ready:

	elatov@ub:~$ kubectl get nodes
	NAME      STATUS    ROLES     AGE       VERSION
	ub        Ready     master    1h        v1.8.3

And you should see all the pods in a **Running** state:

	elatov@ub:~$ kubectl get pod --all-namespaces
	NAMESPACE     NAME                         READY     STATUS    RESTARTS   AGE
	kube-system   etcd-ub                      1/1       Running   0          3m
	kube-system   kube-apiserver-ub            1/1       Running   0          3m
	kube-system   kube-controller-manager-ub   1/1       Running   0          3m
	kube-system   kube-dns-545bc4bfd4-xgk27    3/3       Running   0          3m
	kube-system   kube-flannel-ds-b9hhx        1/1       Running   0          2m
	kube-system   kube-proxy-xjtrx             1/1       Running   0          3m
	kube-system   kube-scheduler-ub            1/1       Running   0          3m

and you can also confirm your network settings:

	elatov@ub:~$ ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	2: ens9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
	    inet 192.168.1.106/24 brd 192.168.1.255 scope global ens9
	       valid_lft forever preferred_lft forever
	4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
	    inet 172.17.0.1/16 scope global docker0
	       valid_lft forever preferred_lft forever
	5: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default
	    inet 10.244.0.0/32 scope global flannel.1
	       valid_lft forever preferred_lft forever
	6: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000
	    inet 10.244.0.1/24 scope global cni0
	       valid_lft forever preferred_lft forever

You should see 3 additional interfaces:

* **docker0** : Used by the **docker** daemon and will be used if you deploy manual machines (i.e. **with docker-compose**)
* **flannel.1** : This is the *overlay* network
* **cni0** : Used by **kubernetes** for it's deployments and resides on the *overlay* network

That should be it, the cluster is ready.
### Changing the Port range for the API Service
By default **kubernetes** uses the following port range 30000-32767 for it's deployment and
I wanted to expand the port range on the cluster (just to stay organized), so I created the following config:

	elatov@ub:~$ cat kubeadmin-config.yaml
	apiVersion: kubeadm.k8s.io/v1alpha1
	kind: MasterConfiguration
	networking:
	  dnsDomain: "cluster.local"
	  serviceSubnet: "10.96.0.0/12"
	  podSubnet: "10.244.0.0/16"
	apiServerExtraArgs:
	  service-node-port-range: "30000-40000"

and then re-created my setup (first remove):

	root@ub:~# kubeadm reset
	[preflight] Running pre-flight checks
	[reset] Stopping the kubelet service
	[reset] Unmounting mounted directories in "/var/lib/kubelet"
	[reset] Removing kubernetes-managed containers
	[reset] Deleting contents of stateful directories: [/var/lib/kubelet /etc/cni/net.d /var/lib/dockershim /var/run/kubernetes /var/lib/etcd]
	[reset] Deleting contents of config directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
	[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]

Then recreate:

	root@ub:~# kubeadm init --config ~elatov/kubeadmin-config.yaml
	[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
	[init] Using Kubernetes version: v1.8.3
	[init] Using Authorization modes: [Node RBAC]
	[preflight] Running pre-flight checks
	[preflight] Starting the kubelet service
	[kubeadm] WARNING: starting in 1.8, tokens expire after 24 hours by default (if you require a non-expiring token use --token-ttl 0)
	[certificates] Generated ca certificate and key.
	[certificates] Generated apiserver certificate and key.
	[certificates] apiserver serving cert is signed for DNS names [ub kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.1.106]
	[certificates] Generated apiserver-kubelet-client certificate and key.
	[certificates] Generated sa key and public key.
	[certificates] Generated front-proxy-ca certificate and key.
	[certificates] Generated front-proxy-client certificate and key.
	[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
	[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
	[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"
	[controlplane] Wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
	[controlplane] Wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
	[controlplane] Wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
	[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
	[init] Waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests"
	[init] This often takes around a minute; or longer if the control plane images have to be pulled.
	[apiclient] All control plane components are healthy after 28.503097 seconds
	[uploadconfig] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
	[markmaster] Will mark node ub as master by adding a label and a taint
	[markmaster] Master ub tainted and labelled with key/value: node-role.kubernetes.io/master=""
	[bootstraptoken] Using token: 75a0fd.ae8280ca83fbdbc3
	[bootstraptoken] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
	[bootstraptoken] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
	[bootstraptoken] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
	[bootstraptoken] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
	[addons] Applied essential addon: kube-dns
	[addons] Applied essential addon: kube-proxy
	
	Your Kubernetes master has initialized successfully!
	
	To start using your cluster, you need to run (as a regular user):
	
	  mkdir -p $HOME/.kube
	  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	  sudo chown $(id -u):$(id -g) $HOME/.kube/config
	
	You should now deploy a pod network to the cluster.
	Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
	  http://kubernetes.io/docs/admin/addons/
	
	You can now join any number of machines by running the following on each node
	as root:
	
	  kubeadm join --token 75a0fd.ae8280ca83fbdbc3 192.168.1.106:6443 --discovery-token-ca-cert-hash sha256:8a09a0a499d90c1cbac1a37eb939285d22ca30ca17637e4dcb9015d0730c1893

And then you should see the following added to the API service:

	<> sudo grep port- /etc/kubernetes/manifests/kube-apiserver.yaml
	    - --service-node-port-range=30000-40000


Very cool.

### Compiling kubeadm  
For some reason when exposing ports it would never add the **iptables** rules. Checking out the logs I saw this:

	<> kubectl logs --namespace=kube-system po/kube-proxy-xjtrx
	W1117 03:44:50.956040       1 server.go:191] WARNING: all flags other than --config, --write-config-to, and --cleanup are deprecated. Please begin using a config file ASAP.
	time="2017-11-17T03:44:50Z" level=warning msg="Running modprobe ip_vs failed with message: `modprobe: ERROR: ../libkmod/libkmod.c:557 kmod_search_moddep() could not open moddep file '/lib/modules/4.4.0-98-generic/modules.dep.bin'`, error: exit status 1"
	time="2017-11-17T03:44:50Z" level=error msg="Could not get ipvs family information from the kernel. It is possible that ipvs is not enabled in your kernel. Native loadbalancing will not work until this is fixed."
	W1117 03:44:50.962668       1 server_others.go:268] Flag proxy-mode="" unknown, assuming iptables proxy
	I1117 03:44:50.964077       1 server_others.go:122] Using iptables Proxier.
	I1117 03:44:50.971358       1 server_others.go:157] Tearing down inactive rules.
	E1117 03:44:50.991275       1 proxier.go:699] Failed to execute iptables-restore for nat: exit status 1 (iptables-restore: line 7 failed
	)
	I1117 03:44:51.018363       1 conntrack.go:98] Set sysctl 'net/netfilter/nf_conntrack_max' to 262144
	I1117 03:44:51.019014       1 conntrack.go:52] Setting nf_conntrack_max to 262144
	I1117 03:44:51.019055       1 conntrack.go:98] Set sysctl 'net/netfilter/nf_conntrack_tcp_timeout_established' to 86400
	I1117 03:44:51.019087       1 conntrack.go:98] Set sysctl 'net/netfilter/nf_conntrack_tcp_timeout_close_wait' to 3600
	I1117 03:44:51.019558       1 config.go:202] Starting service config controller
	I1117 03:44:51.019572       1 controller_utils.go:1041] Waiting for caches to sync for service config controller
	I1117 03:44:51.020009       1 config.go:102] Starting endpoints config controller
	I1117 03:44:51.020022       1 controller_utils.go:1041] Waiting for caches to sync for endpoints config controller
	I1117 03:44:51.119689       1 controller_utils.go:1048] Caches are synced for service config controller
	I1117 03:44:51.120133       1 controller_utils.go:1048] Caches are synced for endpoints config controller

Looks like it's a [known issue](https://github.com/kubernetes/kubernetes/issues/55043) (also it looks like there is [feature request](https://github.com/kubernetes/kubeadm/issues/520) to be able to modify **kube-proxy** with extra parameters since currently there is no way to do that). But the fix hasn't made to a release yet. So I decided to build a test version. First let's the get the source and **checkout** the branch where the fix is available:

	elatov@ub:~$ git clone https://github.com/kubernetes/kubernetes.git
	Cloning into 'kubernetes'...
	remote: Counting objects: 663315, done.
	remote: Compressing objects: 100% (67/67), done.
	remote: Total 663315 (delta 17), reused 19 (delta 13), pack-reused 663235
	Receiving objects: 100% (663315/663315), 509.26 MiB | 9.98 MiB/s, done.
	Resolving deltas: 100% (444421/444421), done.
	Checking connectivity... done.
	elatov@ub:~$ cd kubernetes/
	elatov@ub:~/kubernetes$ git checkout release-1.8
	Branch release-1.8 set up to track remote branch release-1.8 from origin.
	Switched to a new branch 'release-1.8'
	
#### Install Go on Ubuntu

By default Ubuntu comes with Go version 1.6 and for kubernetes we need 1.8 or above. To get a later version we can follow instructions laid out in [GoLang Ubuntu Wiki](https://github.com/golang/go/wiki/Ubuntu). First add their custom repo:

	$ sudo add-apt-repository ppa:gophers/archive
	$ sudo apt update

Then install it:

	$ sudo apt install golang-1.9

And create symlinks for the binary:

	$ cd /usr/local/bin
	elatov@ub:/usr/local/bin$
	elatov@ub:/usr/local/bin$ sudo ln -s /usr/lib/go-1.9/bin/go
	elatov@ub:/usr/local/bin$ sudo ln -s /usr/lib/go-1.9/bin/gofmt

#### Building kubeadm
Next we can check out the build instructions [here](https://github.com/kubernetes/kubernetes/tree/master/build/). To build just the **kubeadm** binary we can run the following:

	elatov@ub:~/kubernetes $ make all WHAT=cmd/kubeadm
	+++ [1118 10:20:36] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:20:37] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~/kubernetes ~/kubernetes/test/e2e/generated
	~/kubernetes/test/e2e/generated
	+++ [1118 10:20:37] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 10:20:49] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:20:49] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~/kubernetes ~/kubernetes/test/e2e/generated
	~/kubernetes/test/e2e/generated
	+++ [1118 10:20:50] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 10:20:54] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:20:55] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~/kubernetes ~/kubernetes/test/e2e/generated
	~/kubernetes/test/e2e/generated
	+++ [1118 10:20:55] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 10:21:00] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:21:00] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~/kubernetes ~/kubernetes/test/e2e/generated
	~/kubernetes/test/e2e/generated
	+++ [1118 10:21:01] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 10:21:08] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:21:08] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~/kubernetes ~/kubernetes/test/e2e/generated
	~/kubernetes/test/e2e/generated
	+++ [1118 10:21:08] Building go targets for linux/amd64:
	    cmd/kubeadm
	+++ [1118 10:21:09] +++ Warning: stdlib pkg with cgo flag not found.
	+++ [1118 10:21:09] +++ Warning: stdlib pkg cannot be rebuilt since /usr/lib/go-1.9/pkg is not writable by elatov
	+++ [1118 10:21:09] +++ Warning: Make /usr/lib/go-1.9/pkg writable for elatov for a one-time stdlib install, Or
	+++ [1118 10:21:09] +++ Warning: Rebuild stdlib using the command 'CGO_ENABLED=0 go install -a -installsuffix cgo std'
	+++ [1118 10:21:09] +++ Falling back to go build, which is slower
	    *

And then I saw the new binary:

	elatov@ub:~/kubernetes/_output/local/bin/linux/amd64$ ./kubeadm version
	kubeadm version: &version.Info{Major:"1", Minor:"8+", GitVersion:"v1.8.4-beta.0.63+db27b55eb11901", GitCommit:"db27b55eb11901f7c4f5528fc0c3f9d16f2d2789", GitTreeState:"clean", BuildDate:"2017-11-18T17:21:08Z", GoVersion:"go1.9", Compiler:"gc", Platform:"linux/amd64"}

Here is the default OS one:

	elatov@ub:~/kubernetes/_output/local/bin/linux/amd64$ kubeadm version
	kubeadm version: &version.Info{Major:"1", Minor:"8", GitVersion:"v1.8.3", GitCommit:"f0efb3cb883751c5ffdbe6d515f3cb4fbe7b7acd", GitTreeState:"clean", BuildDate:"2017-11-08T18:27:48Z", GoVersion:"go1.8.3", Compiler:"gc", Platform:"linux/amd64"}

#### Building a kubernetes release
If you really feel patient you can try doing a whole build (it's actually pretty cool, cause it downloads a bunch of docker images and does the build, you don't even need to have **go** installed... pretty slick):

	elatov@ub:~/kubernetes$ make release
	+++ [1118 09:46:29] Verifying Prerequisites....
	+++ [1118 09:46:30] Building Docker image kube-build:build-7d1c126abc-5-v1.8.3-2
	+++ [1118 09:48:14] Creating data container kube-build-data-7d1c126abc-5-v1.8.3-2
	+++ [1118 09:48:14] Syncing sources to container
	+++ [1118 09:48:17] Running build command...
	+++ [1118 09:48:32] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 09:48:32] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 09:48:32] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 09:48:32] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 09:48:33] Building go targets for linux/arm:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 09:48:36] Building go targets for linux/arm64:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 09:48:39] Building go targets for linux/s390x:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 09:48:42] Building go targets for linux/ppc64le:
	    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
	+++ [1118 09:48:51] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 09:48:51] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 09:48:51] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 09:48:52] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 09:48:52] Building go targets for linux/arm:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 09:48:53] Building go targets for linux/arm64:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 09:48:54] Building go targets for linux/s390x:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 09:48:54] Building go targets for linux/ppc64le:
	    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
	+++ [1118 09:49:00] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 09:49:00] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 09:49:00] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 09:49:00] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 09:49:01] Building go targets for linux/arm:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 09:49:02] Building go targets for linux/arm64:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 09:49:03] Building go targets for linux/s390x:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 09:49:03] Building go targets for linux/ppc64le:
	    ./vendor/k8s.io/code-generator/cmd/conversion-gen
	+++ [1118 09:49:10] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 09:49:10] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 09:49:10] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 09:49:11] Building go targets for linux/amd64:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 09:49:13] Building go targets for linux/arm:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 09:49:17] Building go targets for linux/arm64:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 09:49:21] Building go targets for linux/s390x:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 09:49:25] Building go targets for linux/ppc64le:
	    ./vendor/k8s.io/code-generator/cmd/openapi-gen
	+++ [1118 09:49:33] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 09:49:33] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 09:49:34] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 09:49:34] Building go targets for linux/amd64:
	    cmd/kube-proxy
	    cmd/kube-apiserver
	    cmd/kube-controller-manager
	    cmd/cloud-controller-manager
	    cmd/kubelet
	    cmd/kubeadm
	    cmd/hyperkube
	    vendor/k8s.io/kube-aggregator
	    vendor/k8s.io/apiextensions-apiserver
	    plugin/cmd/kube-scheduler
	+++ [1118 09:53:53] Building go targets for linux/arm:
	    cmd/kube-proxy
	    cmd/kube-apiserver
	    cmd/kube-controller-manager
	    cmd/cloud-controller-manager
	    cmd/kubelet
	    cmd/kubeadm
	    cmd/hyperkube
	    vendor/k8s.io/kube-aggregator
	    vendor/k8s.io/apiextensions-apiserver
	    plugin/cmd/kube-scheduler
	+++ [1118 09:58:18] Building go targets for linux/arm64:
	    cmd/kube-proxy
	    cmd/kube-apiserver
	    cmd/kube-controller-manager
	    cmd/cloud-controller-manager
	    cmd/kubelet
	    cmd/kubeadm
	    cmd/hyperkube
	    vendor/k8s.io/kube-aggregator
	    vendor/k8s.io/apiextensions-apiserver
	    plugin/cmd/kube-scheduler
	+++ [1118 10:02:40] Building go targets for linux/s390x:
	    cmd/kube-proxy
	    cmd/kube-apiserver
	    cmd/kube-controller-manager
	    cmd/cloud-controller-manager
	    cmd/kubelet
	    cmd/kubeadm
	    cmd/hyperkube
	    vendor/k8s.io/kube-aggregator
	    vendor/k8s.io/apiextensions-apiserver
	    plugin/cmd/kube-scheduler
	+++ [1118 10:07:03] Building go targets for linux/ppc64le:
	    cmd/kube-proxy
	    cmd/kube-apiserver
	    cmd/kube-controller-manager
	    cmd/cloud-controller-manager
	    cmd/kubelet
	    cmd/kubeadm
	    cmd/hyperkube
	    vendor/k8s.io/kube-aggregator
	    vendor/k8s.io/apiextensions-apiserver
	    plugin/cmd/kube-scheduler
	+++ [1118 10:12:45] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 10:12:45] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:12:45] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 10:12:46] Building go targets for linux/amd64:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:12:50] Building go targets for linux/arm:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:12:54] Building go targets for linux/arm64:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:12:58] Building go targets for linux/s390x:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:13:02] Building go targets for linux/ppc64le:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:13:07] Building go targets for windows/amd64:
	    cmd/kube-proxy
	    cmd/kubelet
	+++ [1118 10:15:39] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 10:15:39] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:15:39] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 10:15:40] Building go targets for linux/amd64:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:15:55] Building go targets for linux/386:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:17:07] Building go targets for linux/arm:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:17:22] Building go targets for linux/arm64:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:17:38] Building go targets for linux/s390x:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:17:52] Building go targets for linux/ppc64le:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:18:08] Building go targets for darwin/amd64:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:19:20] Building go targets for darwin/386:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:20:38] Building go targets for windows/amd64:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:21:15] Building go targets for windows/386:
	    cmd/kubectl
	    federation/cmd/kubefed
	+++ [1118 10:24:40] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 10:24:40] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:24:40] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 10:24:41] Building go targets for linux/amd64:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:25:47] Building go targets for linux/arm:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:26:54] Building go targets for linux/arm64:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:28:02] Building go targets for linux/s390x:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:29:08] Building go targets for linux/ppc64le:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:30:16] Building go targets for darwin/amd64:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:32:41] Building go targets for windows/amd64:
	    cmd/gendocs
	    cmd/genkubedocs
	    cmd/genman
	    cmd/genyaml
	    cmd/genswaggertypedocs
	    cmd/linkcheck
	    federation/cmd/genfeddocs
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e/e2e.test
	+++ [1118 10:36:21] Multiple platforms requested, but available 9G < threshold 11G, building platforms in serial
	+++ [1118 10:36:21] Building the toolchain targets:
	    k8s.io/kubernetes/hack/cmd/teststale
	    k8s.io/kubernetes/vendor/github.com/jteeuwen/go-bindata/go-bindata
	+++ [1118 10:36:21] Generating bindata:
	    test/e2e/generated/gobindata_util.go
	~ ~/test/e2e/generated
	~/test/e2e/generated
	+++ [1118 10:36:21] Building go targets for linux/amd64:
	    cmd/kubemark
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e_node/e2e_node.test
	+++ [1118 10:37:03] Building go targets for linux/arm:
	    cmd/kubemark
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e_node/e2e_node.test
	+++ [1118 10:37:45] Building go targets for linux/arm64:
	    cmd/kubemark
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e_node/e2e_node.test
	+++ [1118 10:38:28] Building go targets for linux/s390x:
	    cmd/kubemark
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e_node/e2e_node.test
	+++ [1118 10:39:09] Building go targets for linux/ppc64le:
	    cmd/kubemark
	    vendor/github.com/onsi/ginkgo/ginkgo
	    test/e2e_node/e2e_node.test
	
	+++ [1118 10:41:32] Syncing out of container
	+++ [1118 10:43:08] Building tarball: src
	+++ [1118 10:43:08] Building tarball: salt
	+++ [1118 10:43:08] Starting tarball: client darwin-386
	+++ [1118 10:43:08] Building tarball: manifests
	+++ [1118 10:43:08] Starting tarball: client darwin-amd64
	+++ [1118 10:43:08] Starting tarball: client linux-386
	+++ [1118 10:43:08] Starting tarball: client linux-amd64
	+++ [1118 10:43:08] Starting tarball: client linux-arm
	+++ [1118 10:43:08] Starting tarball: client linux-arm64
	+++ [1118 10:43:08] Starting tarball: client linux-ppc64le
	+++ [1118 10:43:08] Starting tarball: client linux-s390x
	+++ [1118 10:43:08] Starting tarball: client windows-386
	+++ [1118 10:43:08] Starting tarball: client windows-amd64
	+++ [1118 10:43:08] Waiting on tarballs
	+++ [1118 10:43:21] Building tarball: node linux-amd64
	+++ [1118 10:43:21] Building tarball: server linux-amd64
	+++ [1118 10:43:26] Starting docker build for image: cloud-controller-manager-amd64
	+++ [1118 10:43:26] Starting docker build for image: kube-apiserver-amd64
	+++ [1118 10:43:26] Starting docker build for image: kube-controller-manager-amd64
	+++ [1118 10:43:26] Starting docker build for image: kube-scheduler-amd64
	+++ [1118 10:43:26] Starting docker build for image: kube-aggregator-amd64
	+++ [1118 10:43:26] Starting docker build for image: kube-proxy-amd64
	+++ [1118 10:43:33] Deleting docker image gcr.io/google_containers/kube-aggregator:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:33] Deleting docker image gcr.io/google_containers/kube-scheduler:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:33] Deleting docker image gcr.io/google_containers/cloud-controller-manager:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:34] Building tarball: node linux-arm
	+++ [1118 10:43:37] Deleting docker image gcr.io/google_containers/kube-proxy:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:38] Deleting docker image gcr.io/google_containers/kube-controller-manager:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:38] Deleting docker image gcr.io/google_containers/kube-apiserver:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:43:39] Docker builds done
	+++ [1118 10:43:46] Building tarball: node linux-arm64
	+++ [1118 10:43:57] Building tarball: node linux-s390x
	+++ [1118 10:44:11] Building tarball: node linux-ppc64le
	+++ [1118 10:44:23] Building tarball: node windows-amd64
	+++ [1118 10:44:42] Building tarball: server linux-arm
	+++ [1118 10:44:46] Starting docker build for image: cloud-controller-manager-arm
	+++ [1118 10:44:46] Starting docker build for image: kube-apiserver-arm
	+++ [1118 10:44:46] Starting docker build for image: kube-controller-manager-arm
	+++ [1118 10:44:46] Starting docker build for image: kube-scheduler-arm
	+++ [1118 10:44:46] Starting docker build for image: kube-aggregator-arm
	+++ [1118 10:44:46] Starting docker build for image: kube-proxy-arm
	+++ [1118 10:44:52] Deleting docker image gcr.io/google_containers/kube-scheduler-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:52] Deleting docker image gcr.io/google_containers/kube-aggregator-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:53] Deleting docker image gcr.io/google_containers/cloud-controller-manager-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:53] Deleting docker image gcr.io/google_containers/kube-controller-manager-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:54] Deleting docker image gcr.io/google_containers/kube-apiserver-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:54] Deleting docker image gcr.io/google_containers/kube-proxy-arm:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:44:55] Docker builds done
	+++ [1118 10:45:47] Building tarball: server linux-arm64
	+++ [1118 10:45:50] Starting docker build for image: cloud-controller-manager-arm64
	+++ [1118 10:45:50] Starting docker build for image: kube-apiserver-arm64
	+++ [1118 10:45:50] Starting docker build for image: kube-controller-manager-arm64
	+++ [1118 10:45:50] Starting docker build for image: kube-scheduler-arm64
	+++ [1118 10:45:50] Starting docker build for image: kube-aggregator-arm64
	+++ [1118 10:45:50] Starting docker build for image: kube-proxy-arm64
	+++ [1118 10:45:55] Deleting docker image gcr.io/google_containers/kube-aggregator-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:45:56] Deleting docker image gcr.io/google_containers/kube-scheduler-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:45:57] Deleting docker image gcr.io/google_containers/kube-controller-manager-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:45:57] Deleting docker image gcr.io/google_containers/cloud-controller-manager-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:45:59] Deleting docker image gcr.io/google_containers/kube-proxy-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:46:00] Deleting docker image gcr.io/google_containers/kube-apiserver-arm64:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:46:00] Docker builds done
	+++ [1118 10:46:59] Building tarball: server linux-s390x
	+++ [1118 10:47:04] Starting docker build for image: cloud-controller-manager-s390x
	+++ [1118 10:47:04] Starting docker build for image: kube-apiserver-s390x
	+++ [1118 10:47:04] Starting docker build for image: kube-controller-manager-s390x
	+++ [1118 10:47:04] Starting docker build for image: kube-scheduler-s390x
	+++ [1118 10:47:04] Starting docker build for image: kube-aggregator-s390x
	+++ [1118 10:47:04] Starting docker build for image: kube-proxy-s390x
	+++ [1118 10:47:11] Deleting docker image gcr.io/google_containers/kube-aggregator-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:11] Deleting docker image gcr.io/google_containers/kube-scheduler-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:13] Deleting docker image gcr.io/google_containers/cloud-controller-manager-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:13] Deleting docker image gcr.io/google_containers/kube-controller-manager-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:13] Deleting docker image gcr.io/google_containers/kube-proxy-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:14] Deleting docker image gcr.io/google_containers/kube-apiserver-s390x:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:47:14] Docker builds done
	+++ [1118 10:48:29] Building tarball: server linux-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: cloud-controller-manager-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: kube-apiserver-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: kube-controller-manager-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: kube-scheduler-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: kube-aggregator-ppc64le
	+++ [1118 10:48:32] Starting docker build for image: kube-proxy-ppc64le
	+++ [1118 10:48:38] Deleting docker image gcr.io/google_containers/kube-aggregator-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:38] Deleting docker image gcr.io/google_containers/kube-scheduler-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:39] Deleting docker image gcr.io/google_containers/cloud-controller-manager-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:41] Deleting docker image gcr.io/google_containers/kube-proxy-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:41] Deleting docker image gcr.io/google_containers/kube-controller-manager-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:42] Deleting docker image gcr.io/google_containers/kube-apiserver-ppc64le:v1.8.4-beta.0.63_db27b55eb11901
	+++ [1118 10:48:42] Docker builds done
	+++ [1118 10:49:42] Building tarball: final
	+++ [1118 10:49:42] Building tarball: test

That took about 1.5 hours and here is the total space usage (between just building **kubeadm** and doing **release** build):

	elatov@ub:~$ du -sh kube*
	1.1G  kubernetes2
	35G   kubernetes

To get back all the space you can run the following:

	elatov@ub:~/kubernetes$ make clean
	+++ [1120 14:04:30] Verifying Prerequisites....
	+++ [1120 14:04:32] Removing _output directory
	Removing .dockerized-kube-version-defs
	Removing pkg/generated/openapi/zz_generated.openapi.go

#### Confirming the new kubeadm fix
After I removed the original **kubernetes** cluster and recreated a new one with the new binary:

	root@ub:~# kubeadm reset
	root@ub:~# /usr/local/bin/kubeadm init --config ~elatov/kubeadmin-config.yaml

And I saw the rules added to the NAT table:

	elatov@ub:~$ sudo iptables -L -n -v -t nat | grep 30443
	    0     0 KUBE-MARK-MASQ  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            /* kube-system/kubernetes-dashboard: */ tcp dpt:30443
	    0     0 KUBE-SVC-XGLOHA7QRQ3V22RZ  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            /* kube-system/kubernetes-dashboard: */ tcp dpt:30443

### Deploy kubernetes Dashboard
I ended up downloading the latest version of the YAML file and modified it to use [NodePort](https://github.com/kubernetes/dashboard/wiki/Accessing-Dashboard---1.7.X-and-above#nodeport) so I can reach it internally:

	elatov@ub:~$ wget https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
	elatov@ub:~$ vi kubernetes-dashboard.yaml
	elatov@ub:~$ kubectl apply -f kubernetes-dashboard.yaml

I also realized that with the new RBAC configuration, I needed to follow instructions laid out in [Access-control - admin privileges](https://github.com/kubernetes/dashboard/wiki/Access-control#admin-privileges) to be able to login to the dashboard without using a token:

	elatov@ub:~$ cat dashboard-admin.yaml
	apiVersion: rbac.authorization.k8s.io/v1beta1
	kind: ClusterRoleBinding
	metadata:
	name: kubernetes-dashboard
	labels:
	 k8s-app: kubernetes-dashboard
	roleRef:
	apiGroup: rbac.authorization.k8s.io
	kind: ClusterRole
	name: cluster-admin
	subjects:
	- kind: ServiceAccount
	name: kubernetes-dashboard
	namespace: kube-system
	elatov@ub:~$ kubectl apply -f dashboard-admin.yaml
	
Then I was able to see the dashboard from a machine on the local subnet:

![kubernetes-dashboard-kubeadm.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/kubeadm-kubernetes/kubernetes-dashboard-kubeadm.png&raw=1)

### Converting Docker-compose Jenkins to Kubernetes

There is a cool tool called [kompose](https://kubernetes.io/docs/tools/kompose/user-guide/) which can convert **docker-compose.yml** into **kubenertes** files. I decided to give it a try, so taking something like this:

	elatov@ub:~$ cat docker-compose.yml
	version: '2'
	services:
	
	    jenkins:
	       image: jenkins/jenkins:lts
	       container_name: jenkins
	       hostname: jenkins.kar.int
	       restart: always
	       expose:
	        - "8081"
	        - "50000"
	       ports:
	        - "8081:8080"
	        - "50000:50000"
	       network_mode: "bridge"

And here is what it does:

	elatov@ub:~$ kompose convert
	WARN Unsupported hostname key - ignoring
	WARN Unsupported network_mode key - ignoring
	INFO Kubernetes file "jenkins-service.yaml" created
	INFO Kubernetes file "jenkins-deployment.yaml" created

And it will create the following:

	elatov@ub:~$ cat jenkins-deployment.yaml
	apiVersion: extensions/v1beta1
	kind: Deployment
	metadata:
	  annotations:
	    kompose.cmd: kompose convert
	    kompose.version: 1.4.0 (c7964e7)
	  creationTimestamp: null
	  labels:
	    io.kompose.service: jenkins
	  name: jenkins
	spec:
	  replicas: 1
	  strategy: {}
	  template:
	    metadata:
	      creationTimestamp: null
	      labels:
	        io.kompose.service: jenkins
	    spec:
	      containers:
	      - image: jenkins/jenkins:lts
	        name: jenkins
	        ports:
	        - containerPort: 8080
	        - containerPort: 50000
	        resources: {}
	      restartPolicy: Always
	status: {}

and this:

	elatov@ub:~$ cat jenkins-service.yaml
	apiVersion: v1
	kind: Service
	metadata:
	  annotations:
	    kompose.cmd: kompose convert
	    kompose.version: 1.4.0 (c7964e7)
	  creationTimestamp: null
	  labels:
	    io.kompose.service: jenkins
	  name: jenkins
	spec:
	  ports:
	  - name: "8081"
	    port: 8081
	    targetPort: 8080
	  - name: "50000"
	    port: 50000
	    targetPort: 50000
	  selector:
	    io.kompose.service: jenkins
	status:
	  loadBalancer: {}

Then modifying the configs to use **NodePort** and adding a local volume (via the **hostPath**):

	elatov@ub:~$ cat jenkins-deployment.yaml
	apiVersion: extensions/v1beta1
	kind: Deployment
	metadata:
	  annotations:
	    kompose.cmd: kompose convert
	    kompose.version: 1.4.0 (c7964e7)
	  creationTimestamp: null
	  labels:
	    io.kompose.service: jenkins
	  name: jenkins
	spec:
	  replicas: 1
	  strategy: {}
	  template:
	    metadata:
	      creationTimestamp: null
	      labels:
	        io.kompose.service: jenkins
	    spec:
	      containers:
	      - image: jenkins/jenkins:lts
	        name: jenkins
	        ports:
	        - containerPort: 8080
	        - containerPort: 50000
	        resources: {}
	        volumeMounts:
	        - mountPath: /var/jenkins_home
	          name: jenkins-home
	      restartPolicy: Always
	      volumes:
	      - name: jenkins-home
	        hostPath:
	          path: /data/shared/jenkins/jenkins_home
	status: {}

And also the service:

	elatov@ub:~$ cat jenkins-service.yaml
	apiVersion: v1
	kind: Service
	metadata:
	  annotations:
	    kompose.cmd: kompose convert
	    kompose.version: 1.4.0 (c7964e7)
	  creationTimestamp: null
	  labels:
	    io.kompose.service: jenkins
	  name: jenkins
	spec:
	  type: NodePort
	  ports:
	  - name: "8081"
	    port: 8081
	    targetPort: 8080
	    nodePort: 38081
	  - name: "50001"
	    port: 50001
	    targetPort: 50000
	  selector:
	    io.kompose.service: jenkins
	status:
	  loadBalancer: {}

That's why I wanted to increase the port range in the beginning of the guide. So I can have a direct translation between ports (just prepend the original port with **3** or **30**). Anyways... lastly starting up the deployment:

	elatov@ub:~$ kubectl apply -f jenkins-deployment.yaml
	deployment "jenkins" created

and the service:

	elatov@ub:~$ kubectl apply -f jenkins-service.yaml
	service "jenkins" created

And I saw the following running:

	elatov@ub:~$ kubectl get all
	NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
	deploy/jenkins   1         1         1            1           30s
	
	NAME                    DESIRED   CURRENT   READY     AGE
	rs/jenkins-554f449b64   1         1         1         30s
	
	NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
	deploy/jenkins   1         1         1            1           30s
	
	NAME                    DESIRED   CURRENT   READY     AGE
	rs/jenkins-554f449b64   1         1         1         30s
	
	NAME                          READY     STATUS    RESTARTS   AGE
	po/jenkins-554f449b64-jrnjs   1/1       Running   0          30s
	
	NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                          AGE
	svc/jenkins      NodePort    10.99.227.209   <none>        8081:38081/TCP,50001:33551/TCP   16s
	svc/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP                          13m

And the **iptables** were in place as well:

	elatov@ub:~$ sudo iptables -L -n -v -t nat | grep 8081
	    0     0 KUBE-MARK-MASQ  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            /* default/jenkins:8081 */ tcp dpt:38081
	    0     0 KUBE-SVC-HVZEUKESD6U3NLSO  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            /* default/jenkins:8081 */ tcp dpt:38081
	    0     0 KUBE-MARK-MASQ  all  --  *      *       10.244.0.52          0.0.0.0/0            /* default/jenkins:8081 */
	    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            /* default/jenkins:8081 */ tcp to:10.244.0.52:8080
	    0     0 KUBE-SVC-HVZEUKESD6U3NLSO  tcp  --  *      *       0.0.0.0/0            10.99.227.209        /* default/jenkins:8081 cluster IP */ tcp dpt:8081
	    0     0 KUBE-SEP-5UOPD5PWCIJ2C5BZ  all  --  *      *       0.0.0.0/0            0.0.0.0/0            /* default/jenkins:8081 */

And I was able to reach it the **jenkins** service from my machine on the IP of the host:

![jenkins-on-kub-port.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/kubeadm-kubernetes/jenkins-on-kub-port.png&raw=1)
