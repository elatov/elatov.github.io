---
published: true
layout: post
title: "Upgrading kubernetes 1.30.x to 1.31.x with kubespray"
author: Karim Elatov
categories: [containers]
tags: [kubespray, kubernetes]
---
I recently used release [v2.27.0](https://github.com/kubernetes-sigs/kubespray/releases/tag/v2.27.0) of kubespray to upgrade my kubernetes cluster and I ran into an interesting issue.

## Control Plane Upgrade Failure
I just kicked off the upgrade as I usually do:

```
> ansible-playbook -i inventory/home/hosts.yaml -b upgrade-cluster.yml
```

And it failed on the control plane node, since during the `drain` the node hung:

```
TASK [upgrade/pre-upgrade : Set if node needs cordoning] *******************************************************************************************************************
ok: [ma]
Monday 06 January 2025  11:15:09 -0700 (0:00:00.055)       0:08:03.828 ********

TASK [upgrade/pre-upgrade : Cordon node] ***********************************************************************************************************************************
changed: [ma]
Monday 06 January 2025  11:15:10 -0700 (0:00:00.393)       0:08:04.221 ********
FAILED - RETRYING: [ma]: Drain node (3 retries left).

TASK [upgrade/pre-upgrade : Drain node] ************************************************************************************************************************************
fatal: [ma]: UNREACHABLE! => {"changed": false, "msg": "Data could not be sent to remote host \"192.168.1.51\". Make sure this host can be reached over ssh: ", "unreachable": true}
```

But it actually kept going and it tried to upgrade the worker nodes:

```
TASK [upgrade/post-upgrade : Wait for cilium] ******************************************************************************************************************************
fatal: [nd -> ma(192.168.1.51)]: FAILED! => {"changed": true, "cmd": ["/usr/local/bin/kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "wait", "pod", "-n", "kube-system", "-l", "k8s-app=cilium", "--field-selector", "spec.nodeName==nd", "--for=condition=Ready", "--timeout=120s"], "delta": "0:02:00.049765", "end": "2025-01-06 11:50:09.172304", "msg": "non-zero return code", "rc": 1, "start": "2025-01-06 11:48:09.122539", "stderr": "error: timed out waiting for the condition on pods/cilium-h2frs", "stderr_lines": ["error: timed out waiting for the condition on pods/cilium-h2frs"], "stdout": "", "stdout_lines": []}

PLAY RECAP *****************************************************************************************************************************************************************
ma                         : ok=471  changed=50   unreachable=1    failed=0    skipped=526  rescued=0    ignored=0
nc                         : ok=434  changed=45   unreachable=0    failed=0    skipped=632  rescued=0    ignored=1
nd                         : ok=435  changed=47   unreachable=0    failed=1    skipped=626  rescued=0    ignored=1
```

After I recovered the control plane VM I tried to upgrade it again, but it failed with the following error:

```
> ansible-playbook -i inventory/home/hosts.yaml -b upgrade-cluster.yml --limit "ma"
...
ok: [ma]
Monday 06 January 2025  12:43:58 -0700 (0:00:00.618)       0:03:49.198 ********
FAILED - RETRYING: [ma]: Kubeadm | Upgrade first control plane node (3 retries left).
FAILED - RETRYING: [ma]: Kubeadm | Upgrade first control plane node (2 retries left).
FAILED - RETRYING: [ma]: Kubeadm | Upgrade first control plane node (1 retries left).

TASK [kubernetes/control-plane : Kubeadm | Upgrade first control plane node] ***********************************************************************************************
fatal: [ma]: FAILED! => {"attempts": 3, "changed": true, "cmd": ["timeout", "-k", "600s", "600s", "/usr/local/bin/kubeadm", "upgrade", "apply", "-y", "v1.31.4", "--certificate-renewal=True", "--ignore-preflight-errors=", "--allow-experimental-upgrades", "--etcd-upgrade=false", "--force"], "delta": "0:00:15.070363", "end": "2025-01-06 12:45:14.104662", "failed_when_result": true, "msg": "non-zero return code", "rc": 1, "start": "2025-01-06 12:44:59.034299", "stderr": "W0106 12:44:59.088587   28100 utils.go:69] The recommended value for \"clusterDNS\" in \"KubeletConfiguration\" is: [10.233.0.10]; the provided value is: [10.233.0.3]\n[upgrade/health] FATAL: [preflight] Some fatal errors occurred:\n\t[ERROR CreateJob]: Job \"upgrade-health-check-49pw9\" in the namespace \"kube-system\" did not complete in 15s: no condition of type Complete\n[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`\nTo see the stack trace of this error execute with --v=5 or higher", "stderr_lines": ["W0106 12:44:59.088587   28100 utils.go:69] The recommended value for \"clusterDNS\" in \"KubeletConfiguration\" is: [10.233.0.10]; the provided value is: [10.233.0.3]", "[upgrade/health] FATAL: [preflight] Some fatal errors occurred:", "\t[ERROR CreateJob]: Job \"upgrade-health-check-49pw9\" in the namespace \"kube-system\" did not complete in 15s: no condition of type Complete", "[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`", "To see the stack trace of this error execute with --v=5 or higher"], "stdout": "[preflight] Running pre-flight checks.\n[upgrade/config] Reading configuration from the cluster...\n[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'\n[upgrade] Running cluster health checks", "stdout_lines": ["[preflight] Running pre-flight checks.", "[upgrade/config] Reading configuration from the cluster...", "[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'", "[upgrade] Running cluster health checks"]}

PLAY RECAP *****************************************************************************************************************************************************************
ma                         : ok=552  changed=13   unreachable=0    failed=1    skipped=791  rescued=0    ignored=1
```

When I logged into the worker nodes most of the pods were having an issue coming up:

```
> k get po -A | grep cili
kube-system      cilium-4lktc                                                   0/1     Completed                         40             210d
kube-system      cilium-h2frs                                                   0/1     Completed                         45             210d
kube-system      cilium-operator-5c844c548c-5j4kd                               0/1     CreateContainerConfigError        8 (51m ago)    118d
kube-system      cilium-operator-5c844c548c-6b4fk                               0/1     CreateContainerConfigError        0              4m54s
kube-system      cilium-vqgpg                                                   0/1     Init:CreateContainerConfigError   0              25m
```

### Manually Fixing the Control Plane node
I checked out one of the pods:

```
$ k -n kube-system describe pod cilium-operator-5c844c548c-5j4kd
...
...
Normal   Killing         51m                    kubelet  Container cilium-operator definition changed, will be restarted
Normal   Pulled          50m (x5 over 51m)      kubelet  Container image "quay.io/cilium/operator:v1.15.4" already present on machine
Warning  Failed          50m (x5 over 51m)      kubelet  Error: services have not yet been read at least once, cannot construct envvars
Warning  BackOff         49m (x7 over 51m)      kubelet  Back-off restarting failed container cilium-operator in pod cilium-operator-5c844c548c-5j4kd_kube-system(ce37b8b5-084f-41a4-94f6-12df2b00eb68)
Normal   SandboxChanged  48m                    kubelet  Pod sandbox changed, it will be killed and re-created.                                                                                                          
Warning  BackOff         46m (x4 over 47m)      kubelet  Back-off restarting failed container cilium-operator in pod cilium-operator-5c844c548c-5j4kd_kube-system(ce37b8b5-084f-41a4-94f6-12df2b00eb68)
Warning  Failed          45m (x10 over 48m)     kubelet  Error: services have not yet been read at least once, cannot construct envvars
Normal   Pulled          3m12s (x208 over 48m)  kubelet  Container image "quay.io/cilium/operator:v1.15.4" already present on machine
```

I found a recent issue that matched that error [kubelet fails to start pods after upgrade to 1.31.X](https://github.com/kubernetes/kubernetes/issues/127316). It looks like an newer version of `kubelet` cannot connect to an older version of the `kube-apiserver`. Depending on the situation there is a fix in that [same issue](https://github.com/kubernetes/kubernetes/issues/127316#issuecomment-2348662766), however this will only work if the `kube-apiserver` has been upgraded already in an HA configuration and `kubelet` wasn't connecting to the local `kube-apiserver` (and in my situation that was not the case). So then I decided to manually upgrade the control plane to make sure upgraded `kubelet` from worker nodes can start up. I ran the upgrade again and I saw the issue was with the health check failing. As the upgrade was hapenning in the background I saw the pods never succeeding:

```
$ k get po -n kube-system -o wide| grep upgrade
upgrade-health-check-nfl6g-gcwfg   0/1          ContainerCreating    0 n/a   nc          14s
upgrade-health-check-9jl8j-4gmfx   0/1          Terminating          0 n/a   nc          34s
```

I logged into the node where the pod was scheduled and I saw the following:

```
Jan 06 12:44:36 nc kubelet[49129]: E0106 12:44:36.140454   49129 kuberuntime_manager.go:1274] "Unhandled Error" err=<
Jan 06 12:44:36 nc kubelet[49129]:         init container &Container{Name:mount-cgroup,Image:quay.io/cilium/cilium:v1.15.4,Command:[sh -ec cp /usr/bin/cilium-mount /hostbin/cilium-mount;
Jan 06 12:44:36 nc kubelet[49129]:         nsenter --cgroup=/hostproc/1/ns/cgroup --mount=/hostproc/1/ns/mnt "${BIN_PATH}/cilium-mount" $CGROUP_ROOT;
Jan 06 12:44:36 nc kubelet[49129]:         rm /hostbin/cilium-mount
Jan 06 12:44:36 nc kubelet[49129]:         ],Args:[],WorkingDir:,Ports:[]ContainerPort{},Env:[]EnvVar{EnvVar{Name:CGROUP_ROOT,Value:/run/cilium/cgroupv2,ValueFrom:nil,},EnvVar{Name:BIN_PATH,Value:/opt/cni/bin,ValueFrom:nil,},},Resources:ResourceRequirements{Limits:ResourceList{},Requests:ResourceList{},Claims:[]ResourceClaim{},},VolumeMounts:[]VolumeMount{VolumeMount{Name:hostproc,ReadOnly:false,MountPath:/hostproc,SubPath:,MountPropagation:nil,SubPathExpr:,RecursiveReadOnly:nil,},VolumeMount{Name:cni-path,ReadOnly:false,MountPath:/hostbin,SubPath:,MountPropagation:nil,SubPathExpr:,RecursiveReadOnly:nil,},VolumeMount{Name:kube-api-access-8d9hd,ReadOnly:true,MountPath:/var/run/secrets/kubernetes.io/serviceaccount,SubPath:,MountPropagation:nil,SubPathExpr:,RecursiveReadOnly:nil,},},LivenessProbe:nil,ReadinessProbe:nil,Lifecycle:nil,TerminationMessagePath:/dev/termination-log,ImagePullPolicy:IfNotPresent,SecurityContext:&SecurityContext{Capabilities:nil,Privileged:*true,SELinuxOptions:nil,RunAsUser:nil,RunAsNonRoot:nil,ReadOnlyRootFilesystem:nil,AllowPrivilegeEscalation:nil,RunAsGroup:nil,ProcMount:nil,WindowsOptions:nil,SeccompProfile:nil,AppArmorProfile:nil,},Stdin:false,StdinOnce:false,TTY:false,EnvFrom:[]EnvFromSource{},TerminationMessagePolicy:File,VolumeDevices:[]VolumeDevice{},StartupProbe:nil,ResizePolicy:[]ContainerResizePolicy{},RestartPolicy:nil,} start failed in pod cilium-4lktc_kube-system(c96e887f-3eb9-4971-a8a7-9f8c70cfc6a5): CreateContainerConfigError: services have not yet been read at least once, cannot construct envvars
Jan 06 12:44:36 nc kubelet[49129]:  > logger="UnhandledError"
...
...
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.561193   49129 kubelet.go:2407] "SyncLoop ADD" source="api" pods=["kube-system/upgrade-health-check-j4b6t-75v88"]
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.561580   49129 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="kube-system/upgrade-health-check-j4b6t-75v88"
Jan 06 12:44:38 nc systemd[1]: Created slice kubepods-besteffort-podd9f63bcf_f3fc_4078_a421_14784b44de0e.slice - libcontainer container kubepods-besteffort-podd9f63bcf_f3fc_4078_a421_14784b44de0e.slice.
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.610736   49129 reconciler_common.go:245] "operationExecutor.VerifyControllerAttachedVolume started for volume \"kube-api-access-fqqhb\" (UniqueName: \"kubernetes.io/projected/d9f63bcf-f3fc-4078-a421-14784b44de0e-kube-api-access-fqqhb\") pod \"upgrade-health-check-j4b6t-75v88\" (UID: \"d9f63bcf-f3fc-4078-a421-14784b44de0e\") " pod="kube-system/upgrade-health-check-j4b6t-75v88"
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.711136   49129 reconciler_common.go:218] "operationExecutor.MountVolume started for volume \"kube-api-access-fqqhb\" (UniqueName: \"kubernetes.io/projected/d9f63bcf-f3fc-4078-a421-14784b44de0e-kube-api-access-fqqhb\") pod \"upgrade-health-check-j4b6t-75v88\" (UID: \"d9f63bcf-f3fc-4078-a421-14784b44de0e\") " pod="kube-system/upgrade-health-check-j4b6t-75v88"
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.718329   49129 operation_generator.go:637] "MountVolume.SetUp succeeded for volume \"kube-api-access-fqqhb\" (UniqueName: \"kubernetes.io/projected/d9f63bcf-f3fc-4078-a421-14784b44de0e-kube-api-access-fqqhb\") pod \"upgrade-health-check-j4b6t-75v88\" (UID: \"d9f63bcf-f3fc-4078-a421-14784b44de0e\") " pod="kube-system/upgrade-health-check-j4b6t-75v88"
Jan 06 12:44:38 nc kubelet[49129]: I0106 12:44:38.869662   49129 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="kube-system/upgrade-health-check-j4b6t-75v88"
Jan 06 12:44:38 nc containerd[582]: time="2025-01-06T12:44:38.870549425-07:00" level=info msg="RunPodSandbox for &PodSandboxMetadata{Name:upgrade-health-check-j4b6t-75v88,Uid:d9f63bcf-f3fc-4078-a421-14784b44de0e,Namespace:kube-system,Attempt:0,}"
Jan 06 12:44:40 nc kubelet[49129]: I0106 12:44:40.139213   49129 scope.go:117] "RemoveContainer" containerID="2a937da97320703bb33dd8437d6330d5c04e715dc3089f1a9551f491575f749d"
Jan 06 12:44:40 nc kubelet[49129]: I0106 12:44:40.139290   49129 scope.go:117] "RemoveContainer" containerID="221a0e7e99e6b475919424cc7e4fc67c535ee8a5f10a592cdad9997671f56c04"
Jan 06 12:44:40 nc kubelet[49129]: I0106 12:44:40.139300   49129 scope.go:117] "RemoveContainer" containerID="ff8ff142016bad157ead03427ecacc24c2d43b64baf7fcad0c2c430b68c9dc85"
```

And this was the same issue, since the worker nodes were upgraded before the control plane node `cilium` couldn't start and the `upgrade-health-check` pod was failing to complete. So I ran the command manually and saw the same thing:

```
> sudo /usr/local/bin/kubeadm upgrade apply -y v1.31.4 --certificate-renewal=True --ignore-preflight-errors= --allow-experimental-upgrades --etcd-upgrade=false --force
[preflight] Running pre-flight checks.
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
W0106 12:46:43.115467   28126 utils.go:69] The recommended value for "clusterDNS" in "KubeletConfiguration" is: [10.233.0.10]; the provided value is: [10.233.0.3]
[upgrade] Running cluster health checks
[upgrade/health] FATAL: [preflight] Some fatal errors occurred:
	[ERROR CreateJob]: Job "upgrade-health-check-7th59" in the namespace "kube-system" did not complete in 15s: no condition of type Complete
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`
To see the stack trace of this error execute with --v=5 or higher
```

So then I decided to skip the preflight check and just perform the upgrade:

```
> sudo /usr/local/bin/kubeadm upgrade apply -y v1.31.4 --certificate-renewal=True --ignore-preflight-errors="CreateJob" --allow-experimental-upgrades --etcd-upgrade=false --force
[preflight] Running pre-flight checks.
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
W0106 12:48:58.980866   28178 utils.go:69] The recommended value for "clusterDNS" in "KubeletConfiguration" is: [10.233.0.10]; the provided value is: [10.233.0.3]
[upgrade] Running cluster health checks
	[WARNING CreateJob]: Job "upgrade-health-check-2txgq" in the namespace "kube-system" did not complete in 15s: no condition of type Complete
[upgrade/version] You have chosen to change the cluster version to "v1.31.4"
[upgrade/versions] Cluster version: v1.30.4
[upgrade/versions] kubeadm version: v1.31.4
[upgrade/prepull] Pulling images required for setting up a Kubernetes cluster
[upgrade/prepull] This might take a minute or two, depending on the speed of your internet connection
[upgrade/prepull] You can also perform this action beforehand using 'kubeadm config images pull'
[upgrade/apply] Upgrading your Static Pod-hosted control plane to version "v1.31.4" (timeout: 5m0s)...
[upgrade/staticpods] Writing new Static Pod manifests to "/etc/kubernetes/tmp/kubeadm-upgraded-manifests545818905"
[upgrade/staticpods] Preparing for "kube-apiserver" upgrade
[upgrade/staticpods] Renewing apiserver certificate
[upgrade/staticpods] Renewing apiserver-kubelet-client certificate
[upgrade/staticpods] Renewing front-proxy-client certificate
[upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-apiserver.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2025-01-06-12-49-14/kube-apiserver.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This can take up to 5m0s
[apiclient] Found 1 Pods for label selector component=kube-apiserver
[upgrade/staticpods] Component "kube-apiserver" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-controller-manager" upgrade
[upgrade/staticpods] Renewing controller-manager.conf certificate
[upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-controller-manager.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2025-01-06-12-49-14/kube-controller-manager.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This can take up to 5m0s
[apiclient] Found 1 Pods for label selector component=kube-controller-manager
[upgrade/staticpods] Component "kube-controller-manager" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-scheduler" upgrade
[upgrade/staticpods] Renewing scheduler.conf certificate
[upgrade/staticpods] Moving new manifest to "/etc/kubernetes/manifests/kube-scheduler.yaml" and backing up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2025-01-06-12-49-14/kube-scheduler.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This can take up to 5m0s
[apiclient] Found 1 Pods for label selector component=kube-scheduler
[upgrade/staticpods] Component "kube-scheduler" upgraded successfully!
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upgrade] Backing up kubelet config file to /etc/kubernetes/tmp/kubeadm-kubelet-config2888765671/config.yaml
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

[upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.31.4". Enjoy!

[upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
```

And then all the pods came up without issues:

```
> k get po -n kube-system -o wide
NAME                               READY   STATUS    RESTARTS      AGE   IP              NODE   NOMINATED NODE   READINESS GATES
cilium-4px22                       1/1     Running   0             45h   192.168.1.52    nc     <none>           <none>
cilium-nggt9                       1/1     Running   0             45h   192.168.1.51    ma     <none>           <none>
cilium-operator-84579b79bd-8mz8l   1/1     Running   0             44h   192.168.1.52    nc     <none>           <none>
cilium-operator-84579b79bd-qrzc5   1/1     Running   0             45h   192.168.1.53    nd     <none>           <none>
cilium-vnz7v                       1/1     Running   0             45h   192.168.1.53    nd     <none>           <none>
coredns-69df789bc-2d5sp            1/1     Running   0             45h   10.233.65.181   nc     <none>           <none>
coredns-69df789bc-6tcgr            1/1     Running   0             44h   10.233.66.70    nd     <none>           <none>
dns-autoscaler-8576bb9f5b-fpg7q    1/1     Running   0             44h   10.233.66.39    nd     <none>           <none>
kube-apiserver-ma                  1/1     Running   0             45h   192.168.1.51    ma     <none>           <none>
kube-controller-manager-ma         1/1     Running   0             45h   192.168.1.51    ma     <none>           <none>
kube-proxy-c7wkg                   1/1     Running   0             45h   192.168.1.51    ma     <none>           <none>
kube-proxy-p9kd6                   1/1     Running   0             45h   192.168.1.52    nc     <none>           <none>
kube-proxy-xfhkb                   1/1     Running   0             45h   192.168.1.53    nd     <none>           <none>
kube-scheduler-ma                  1/1     Running   0             45h   192.168.1.51    ma     <none>           <none>
metrics-server-6c8bff4c-fq2f5      1/1     Running   0             44h   10.233.65.1     nc     <none>           <none>
nginx-proxy-nc                     1/1     Running   1 (46h ago)   46h   192.168.1.52    nc     <none>           <none>
nginx-proxy-nd                     1/1     Running   1 (46h ago)   46h   192.168.1.53    nd     <none>           <none>
state-metrics-8c55c666b-bjqxg      1/1     Running   0             44h   10.233.65.66    nc     <none>           <none>
```

I re-ran the upgrade using `kubespray` one more time and all was good.