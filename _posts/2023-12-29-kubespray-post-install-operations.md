---
published: true
layout: post
title: "Kubespray Post Install Operations"
author: Karim Elatov
categories: [storage,containers]
tags: [kubernetes,kubespray,openebs,iscsi]

---

I've been using [kubespray](https://github.com/kubernetes-sigs/kubespray) for a couple of months now and I've run into a couple of corner cases that I wanted to share.

## Changing the OS of the worker nodes

I initially started with ubuntu and I quickly realized there are just too many updates to keep up with. So I decided to switch to Debian. Under [Adding/replacing a node](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/nodes.md) there are really good instructions. I first started with the worker nodes, here are the steps I took. First drain the node:

```bash
> k drain nd --ignore-daemonsets --delete-emptydir-data --force
```

Then we need to grab all the information about all the nodes:

```bash
> ansible-playbook -i inventory/home/hosts.yaml -b playbooks/facts.yml
```

Then finally remove the node:

```
> ansible-playbook -i inventory/home/hosts.yaml -b remove-node.yml -e node=nd
```

At this point I booted the VM from the ISO and installed Debian on it. I gave the node the same IP as before. Then I cleaned up ssh keys:

```bash
ssh-keygen -f "/home/elatov/.ssh/known_hosts" -R "nd"
ssh-keygen -f "/home/elatov/.ssh/known_hosts" -R "192.168.1.53"
```

I configured my user to sudo without a password:

```
> cat /etc/sudoers.d/10_admins 
%adm ALL=(ALL) NOPASSWD: ALL
```

And I was already part of the `adm` group. Then I pushed the ssh key to new server:

```bash
ssh-copy-id 192.168.1.53
```

And lastly I performed the kubernetes install:

```
> ansible-playbook -i inventory/home/hosts.yaml -b scale.yml --limit=nd
```

To my surprise that actually worked out quite well.

### Changing OS for control plane nodes

This requires multiple nodes running `etcd`, which is definitely a good idea. But I was just running a test cluster and I didn't really want to scale up my `etcd` install. Then we need upgrade the OS and then scale down the `etcd` instance. Especially since scaling down the `etcd` instance has a bunch of caveats listed in [Replacing a first control plane node](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/nodes.md#replacing-a-first-control-plane-node). From the instructions it looks like we need to change the order of the nodes, change some configs..etc etc. So I got a little lazy and I just drained the control plane node and then converted my OS from ubuntu to debian by changing the `/etc/sources.list` repositories. There is actually a nice guide at [ubuntu-deluxe](https://github.com/alexmyczko/autoexec.bat/blob/master/config.sys/ubuntu-deluxe) overall it was pretty straight forward and it worked out.

## Helping with stuck upgrades

During upgrades I enable the `upgrade_node_post_upgrade_confirm` as per [Pausing the upgrade](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/upgrades.md#pausing-the-upgrade) instructions. This gives me the chance to upgrade all the nodes and reboot them. Since usually there are new kernels that needed to be applied. This works great for me, it's not fully automated but that's okay. At certain times a node gets stuck draining:

```bash
TASK [upgrade/pre-upgrade : Cordon node] ******************************************************************************************************************************************
changed: [nd -> ma(192.168.1.51)]
Saturday 23 December 2023  17:11:03 -0700 (0:00:00.477)       0:28:50.605 *****
Saturday 23 December 2023  17:11:04 -0700 (0:00:00.036)       0:28:50.641 *****
Saturday 23 December 2023  17:11:04 -0700 (0:00:00.037)       0:28:50.679 *****
FAILED - RETRYING: [nd -> ma]: Drain node (3 retries left). 
```

I ssh'ed to the node and I saw the following:

```bash
> journalctl -ft kubelet                                                                                                                        
Dec 23 17:18:22 nd kubelet[17565]: I1223 17:18:22.555027   17565 reconciler_common.go:172] "operationExecutor.UnmountVolume started for volume \"plex-config-lib-vol\" (UniqueName: \"kubernetes.io/csi/cstor.csi.openebs.io^pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd\") pod \"bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e\" (UID: \"bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e\") "
Dec 23 17:18:22 nd kubelet[17565]: E1223 17:18:22.558786   17565 nestedpendingoperations.go:348] Operation for "{volumeName:kubernetes.io/csi/cstor.csi.openebs.io^pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd podName:bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e nodeName:}" failed. No retries permitted until 2023-12-23 17:20:24.558747541 -0700 MST m=+8817894.563114988 (durationBeforeRetry 2m2s). Error: UnmountVolume.TearDown failed for volume "plex-config-lib-vol" (UniqueName: "kubernetes.io/csi/cstor.csi.openebs.io^pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd") pod "bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e" (UID: "bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e") : kubernetes.io/csi: Unmounter.TearDownAt failed to clean mount dir [/var/lib/kubelet/pods/bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e/volumes/kubernetes.io~csi/pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd/mount]: kubernetes.io/csi: failed to remove dir [/var/lib/kubelet/pods/bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e/volumes/kubernetes.io~csi/pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd/mount]: remove /var/lib/kubelet/pods/bcdfe2c7-9b1a-41ed-a9dc-0d944af88e5e/volumes/kubernetes.io~csi/pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd/mount: directory not empty
```

I confirmed and I didn't see any pods related to plex there:

```bash
> crictl ps
CONTAINER           IMAGE               CREATED             STATE               NAME                        ATTEMPT             POD ID              POD
f737b7992dee2       21dd3d6f9c60d       2 hours ago         Running             kube-proxy                  0                   b11264ef1174a       kube-proxy-4lqqg
16c278ece2fce       62a15423256f1       6 hours ago         Running             cstor-csi-plugin            0                   2b74b9873dfd2       openebs-cstor-csi-node-jxtlx
5f30e09fc52ef       f84707403d427       6 hours ago         Running             csi-node-driver-registrar   0                   2b74b9873dfd2       openebs-cstor-csi-node-jxtlx
d02204191fed3       5ab2c114fe2e9       6 hours ago         Running             node-disk-exporter          0                   791cd28847a3a       openebs-ndm-node-exporter-wbg6j
d98edffdb0f2f       297e6f2690c43       6 hours ago         Running             node-disk-manager           0                   2a6ca35321347       openebs-ndm-9fw4f
d70f690674eb8       2e5cab9e2a0b4       10 days ago         Running             metricbeat                  0                   4cf5be3e14686       metricbeat-27wxr
1e2f242652aad       72c9c20889862       5 weeks ago         Running             node-exporter               0                   cd5efeacf2635       node-exporter-xsmp5
b8854df8b673b       d00a7abfa71a6       3 months ago        Running             cilium-agent                23                  7f8c48efcbb01       cilium-qmqkd
95aa5e48b74fb       697605b359357       3 months ago        Running             speaker                     0                   880cfbf17f830       speaker-5kctw
6ca932e4914f0       825aff16c20cc       3 months ago        Running             ingress-nginx-controller    0                   d066513d4c9dc       ingress-nginx-controller-kdd8s
5a016218e5d2a       ff71cd4ea5ae5       3 months ago        Running             node-cache                  0                   1566707acf680       nodelocaldns-v95zf
7ec2c23ff8662       433dbc17191a7       3 months ago        Running             nginx-proxy                 0                   258e150442698       nginx-proxy-nd
```

But I did see the `iscsi` disks still mounted:

```bash
> df -Ph | grep sd
Filesystem               Size  Used Avail Use% Mounted on
/dev/sda1                455M  182M  249M  43% /boot
/dev/sde                  20G  554M   19G   3% /var/lib/kubelet/plugins/kubernetes.io/csi/cstor.csi.openebs.io/0bfa291b3fe5bf57fa003d745a27c4c722568ac610e60939590dc5511a09c0ea/globalmount
/dev/sdd                 4.9G  354M  4.5G   8% /var/lib/kubelet/plugins/kubernetes.io/csi/cstor.csi.openebs.io/ef0ce5fb17e2057fcec38d9beada84b657dfc89390cfd6ad62cf0bf0f3b0e533/globalmount
```

I restarted `kubelet` and that fixed the mount issue:

```bash
> sudo systemctl restart kubelet
```

I also ran into a couple of known issues:

- [Cstor Unable to save data](https://github.com/openebs/openebs/issues/3508)
- [multi-attach error during node reboot or shutdown](https://github.com/openebs/openebs/issues/2536)
- [iSCSI volume is not unmounted when pod terminates](https://github.com/kubernetes/kubernetes/issues/42889)

And if I run into this again I think I need to take a closer look at why it was stuck. I should've looked the `iscsid` closer:

```bash
## check status
iscsiadm -m session
systemctl status iscsid

### initiate a rescan to see if that helps
iscsiadm -m session -R
```

Also I want to try and unmount the volume manually to see if that works:

```
mount | grep pvc
umount /var/lib/kubelet/plugins/kubernetes.io/csi/cstor.csi.openebs.io/ef0ce5fb17e2057fcec38d9beada84b657dfc89390cfd6ad62cf0bf0f3b0e533/globalmount
```

I also want to check out the logs of the csi driver:

```bash
## get the po
> k get po -n openebs -l role=openebs-cstor-csi -o wide | grep nd
openebs-cstor-csi-node-fkcsr     2/2     Running   0             18h   192.168.1.53    nd     <none>           <none>

## check out logs
> k logs -n openebs openebs-cstor-csi-node-fkcsr cstor-csi-plugin
```

And lastly get the logs from the iscsi target. From the error in `kubelet` we can see which pvc it has the issue with:

```
## get the po
> k get po -n openebs | grep pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd                           
pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd-target-7b79b67bcbnwjg5   3/3     Running   0             19h

## check the logs
> k logs -n openebs pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd-target-7b79b67bcbnwjg5 cstor-istgt
```