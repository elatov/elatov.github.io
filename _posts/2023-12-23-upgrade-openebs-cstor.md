---
published: true
layout: post
title: "Upgrade OpenEBS cStor"
author: Karim Elatov
categories: [storage,containers]
tags: [kubernetes,openebs]
---

# Upgrading OpenEBS

The upgrade process is split into two steps: Control Plane upgrade and Data Plane upgrade.

## Upgrade the Operator/Control Plane

First we need to upgrade the [cstor operator](https://github.com/openebs/cstor-operators) which is basically the control plane component. You can grab the `yaml` manifest from the [charts repo](https://github.com/openebs/charts/tree/gh-pages). Or you can download the release from [cstor operator](https://github.com/openebs/cstor-operators) repo and use `helm` to perform the upgrade. I tend to use `kustomize`, so I just grabbed the [cstor-operator.yaml](https://github.com/openebs/charts/blob/gh-pages/cstor-operator.yaml) and I applied it:

```bash
> k apply -f https://raw.githubusercontent.com/openebs/charts/gh-pages/cstor-operator.yaml --dry-run=client
namespace/openebs configured (dry run)
serviceaccount/openebs-cstor-operator configured (dry run)
clusterrole.rbac.authorization.k8s.io/openebs-cstor-operator configured (dry run)
...
...
deployment.apps/cspc-operator configured (dry run)
deployment.apps/cvc-operator configured (dry run)
service/cvc-operator-service configured (dry run)
deployment.apps/openebs-cstor-admission-server configured (dry run)
customresourcedefinition.apiextensions.k8s.io/blockdevices.openebs.io configured (dry run)
customresourcedefinition.apiextensions.k8s.io/blockdeviceclaims.openebs.io configured (dry run)
configmap/openebs-ndm-config configured (dry run)
daemonset.apps/openebs-ndm configured (dry run)
deployment.apps/openebs-ndm-operator configured (dry run)
deployment.apps/openebs-ndm-cluster-exporter configured (dry run)
service/openebs-ndm-cluster-exporter-service configured (dry run)
daemonset.apps/openebs-ndm-node-exporter configured (dry run)
service/openebs-ndm-node-exporter-service configured (dry run)
```

After the `cstor-operator` has been upgraded you should see all the pods updated with new time stamps.

```bash
> k get po -n openebs                                    
NAME                                                              READY   STATUS    RESTARTS      AGE
cspc-operator-786cf9c94b-pd5qf                                    1/1     Running   0             2m36s
cstor-disk-pool-2qqg-847bcd77b4-h27b6                             3/3     Running   3 (96d ago)   101d
cstor-disk-pool-5jtv-69d5566f75-zhd24                             3/3     Running   0             101d
cstor-disk-pool-jfz2-d65fb5bcd-wfb4g                              3/3     Running   0             11d
cvc-operator-69559dd754-j8qnv                                     1/1     Running   0             2m34s
openebs-cstor-admission-server-68d8f4ff44-985wh                   1/1     Running   0             2m34s
openebs-cstor-csi-controller-0                                    6/6     Running   0             2m33s
openebs-cstor-csi-node-8zxfv                                      2/2     Running   0             2m7s
openebs-cstor-csi-node-r5klb                                      2/2     Running   0             2m38s
openebs-cstor-csi-node-vgnsx                                      2/2     Running   0             52s
openebs-ndm-cluster-exporter-69ff474f86-8klxk                     1/1     Running   0             2m37s
openebs-ndm-fbnf9                                                 1/1     Running   0             2m12s
openebs-ndm-g4cnh                                                 1/1     Running   0             2m38s
openebs-ndm-node-exporter-88qq5                                   1/1     Running   0             2m17s
openebs-ndm-node-exporter-9zhj8                                   1/1     Running   0             119s
openebs-ndm-node-exporter-x6ctr                                   1/1     Running   0             2m38s
openebs-ndm-operator-68c8b6d56c-rvpgd                             1/1     Running   0             2m37s
openebs-ndm-zghft                                                 1/1     Running   0             2m28s
pvc-087960e4-c718-4227-84f8-d3a6ca423295-target-9dc8b9c69-4g2tr   3/3     Running   0             35d
pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc-target-5f6dd8b5fc5nqb9   3/3     Running   0             35d
pvc-82a81b9a-d585-48b9-9b58-dc3f5b3c2461-target-64dc4f69ffvdtv8   3/3     Running   0             34d
pvc-9670d96c-f1e2-4e6a-a223-25960cf87b44-target-55bfb649cfk5gqf   3/3     Running   0             35d
pvc-dc70575e-499f-4737-a148-e511453df233-target-5558c748fdpnjkq   3/3     Running   0             35d
pvc-eacb5ff7-6c28-4ad5-88eb-e877eaa51b56-target-65674498c-vjrjl   3/3     Running   0             35d
pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd-target-6565bf547btjbpr   3/3     Running   0             35d
```

But from above we can see that the `pvc-` and `cstor-disk-pool-` pods still haven't been upgraded. Let's upgrade them next.

## Upgrade the OpenEBS Resouces/Data plane

The steps to upgrade the rest of the resouces are covered in: [Upgrade OpenEBS](https://github.com/openebs/upgrade/blob/develop/docs/upgrade.md). We have to create two more jobs one for `CSPC pools` and one for `cStor CSI volumes`. So list your pools you can run the following:

```bash
> k get cspc -n openebs
NAME              HEALTHYINSTANCES   PROVISIONEDINSTANCES   DESIREDINSTANCES   AGE
cstor-disk-pool   3                  3                      3                  425d
```

Initially when I ran the `cspc` upgrade, it failed with:

```bash
> k logs -n openebs cstor-cspc-upgrade-kfwnd -f
I1223 18:46:14.053050       1 cstor_cspc.go:66] Upgrading cstor-disk-pool to 3.6.0
I1223 18:46:14.190624       1 deployment.go:78] patching deployment cstor-disk-pool-2qqg
I1223 18:46:14.190707       1 deployment.go:81] deployment already in 3.6.0 version
I1223 18:46:14.190744       1 cspi.go:76] patching cspi cstor-disk-pool-2qqg
I1223 18:46:14.190802       1 cspi.go:79] cspi already in 3.6.0 version
I1223 18:46:15.304463       1 deployment.go:78] patching deployment cstor-disk-pool-5jtv
I1223 18:46:15.304574       1 deployment.go:81] deployment already in 3.6.0 version
I1223 18:46:15.304601       1 cspi.go:76] patching cspi cstor-disk-pool-5jtv
I1223 18:46:15.304667       1 cspi.go:79] cspi already in 3.6.0 version
I1223 18:46:17.504776       1 deployment.go:78] patching deployment cstor-disk-pool-jfz2
I1223 18:46:17.504809       1 deployment.go:81] deployment already in 3.6.0 version
I1223 18:46:17.504820       1 cspi.go:76] patching cspi cstor-disk-pool-jfz2
I1223 18:46:17.505320       1 cspi.go:79] cspi already in 3.6.0 version
I1223 18:46:18.709034       1 cspc.go:76] patching cspc cstor-disk-pool
E1223 18:46:18.724837       1 cstor_cspc.go:74] failed to patch cspc cstor-disk-pool: Internal error occurred: failed calling webhook "admission-webhook.cstor.openebs.io": failed to call webhook: Post "https://openebs-cstor-admission-server.openebs.svc:443/validate?timeout=5s": tls: failed to verify certificate: x509: certificate has expired or is not yet valid: current time 2023-12-23T18:47:40Z is after 2023-10-24T04:03:31Z
F1223 18:46:18.724899       1 cstor_cspc.go:54] Failed to upgrade cStor CSPC cstor-disk-pool
```

I ran into [this github issue](https://github.com/openebs/openebs/issues/3329). The fix in there helped:

```bash
> k delete validatingwebhookconfiguration openebs-cstor-validation-webhook
validatingwebhookconfiguration.admissionregistration.k8s.io "openebs-cstor-validation-webhook" deleted
> k delete -n openebs secret openebs-cstor-admission-secret
secret "openebs-cstor-admission-secret" deleted
> k rollout -n openebs restart deployment openebs-cstor-admission-server
deployment.apps/openebs-cstor-admission-server restarted
```

Then after fixing that and rerunning the job it worked:

```bash
I1223 19:01:16.957926       1 cstor_cspc.go:66] Upgrading cstor-disk-pool to 3.6.0
I1223 19:01:17.071859       1 deployment.go:78] patching deployment cstor-disk-pool-2qqg
I1223 19:01:17.071890       1 deployment.go:81] deployment already in 3.6.0 version
I1223 19:01:17.071902       1 cspi.go:76] patching cspi cstor-disk-pool-2qqg
I1223 19:01:17.071914       1 cspi.go:79] cspi already in 3.6.0 version
I1223 19:01:18.209498       1 deployment.go:78] patching deployment cstor-disk-pool-5jtv
I1223 19:01:18.209525       1 deployment.go:81] deployment already in 3.6.0 version
I1223 19:01:18.209762       1 cspi.go:76] patching cspi cstor-disk-pool-5jtv
I1223 19:01:18.209884       1 cspi.go:79] cspi already in 3.6.0 version
I1223 19:01:20.412175       1 deployment.go:78] patching deployment cstor-disk-pool-jfz2
I1223 19:01:20.412239       1 deployment.go:81] deployment already in 3.6.0 version
I1223 19:01:20.412258       1 cspi.go:76] patching cspi cstor-disk-pool-jfz2
I1223 19:01:20.412276       1 cspi.go:79] cspi already in 3.6.0 version
I1223 19:01:21.609073       1 cspc.go:76] patching cspc cstor-disk-pool
I1223 19:01:21.657720       1 cspc.go:98] cspc cstor-disk-pool patched
I1223 19:01:21.661561       1 cstor_cspc.go:192] Verifying the reconciliation of version for cstor-disk-pool
I1223 19:01:31.669945       1 cstor_cspc.go:77] Successfully upgraded cstor-disk-pool to 3.6.0
Stream closed EOF for openebs/cstor-cspc-upgrade-r9427 (upgrade) 
```

To get a list of your volumes you can run the following:

```bash
> k get cvc -n openebs
NAME                                       CAPACITY   STATUS   AGE
pvc-087960e4-c718-4227-84f8-d3a6ca423295   10Gi       Bound    425d
pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc   1Gi        Bound    423d
pvc-82a81b9a-d585-48b9-9b58-dc3f5b3c2461   10Gi       Bound    425d
pvc-9670d96c-f1e2-4e6a-a223-25960cf87b44   10Gi       Bound    424d
pvc-dc70575e-499f-4737-a148-e511453df233   5Gi        Bound    423d
pvc-eacb5ff7-6c28-4ad5-88eb-e877eaa51b56   50Gi       Bound    425d
pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd   20Gi       Bound    365d
```

The `cstor-volume` job worked without issues:

```bash
> k logs -n openebs cstor-volume-upgrade-w6798 -f
I1223 19:25:47.074741       1 service.go:77] Patching service pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc
I1223 19:25:47.085676       1 service.go:99] Service pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc patched
I1223 19:25:47.085738       1 cv.go:76] patching cv pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc
I1223 19:25:47.118663       1 cv.go:98] cv pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc patched
I1223 19:25:47.132349       1 cstor_volume.go:420] Verifying the reconciliation of version for pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc
I1223 19:25:57.138638       1 cvc.go:76] patching cvc pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc
I1223 19:25:57.160334       1 cvc.go:98] cvc pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc patched
I1223 19:25:57.166214       1 cstor_volume.go:442] Verifying the reconciliation of version for pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc
I1223 19:26:07.181396       1 cstor_volume.go:77] Successfully upgraded pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc to 3.6.0
```

After it's done, all your pods in the `openebs` namespace, should have pretty recent age:

```bash
> k get po -n openebs                            
NAME                                                              READY   STATUS      RESTARTS   AGE
cspc-operator-6fc5b8546b-fkt9v                                    1/1     Running     0          57m
cstor-cspc-upgrade-r9427                                          0/1     Completed   0          28m
cstor-disk-pool-2qqg-6c466c744-j4vnh                              3/3     Running     0          55m
cstor-disk-pool-5jtv-754c67547-8z7fm                              3/3     Running     0          52m
cstor-disk-pool-jfz2-7f9678f6c8-r6ppv                             3/3     Running     0          49m
cstor-volume-upgrade-w6798                                        0/1     Completed   0          13m
cvc-operator-85bd9d569b-l42dr                                     1/1     Running     0          57m
openebs-cstor-admission-server-9fc86bffb-b5kzp                    1/1     Running     0          29m
openebs-cstor-csi-controller-0                                    6/6     Running     0          57m
openebs-cstor-csi-node-f569s                                      2/2     Running     0          57m
openebs-cstor-csi-node-jxtlx                                      2/2     Running     0          57m
openebs-cstor-csi-node-qvr2s                                      2/2     Running     0          56m
openebs-ndm-862tm                                                 1/1     Running     0          57m
openebs-ndm-9fw4f                                                 1/1     Running     0          57m
openebs-ndm-b7r7d                                                 1/1     Running     0          57m
openebs-ndm-cluster-exporter-6bd669f97f-qnfsx                     1/1     Running     0          57m
openebs-ndm-node-exporter-hk7g9                                   1/1     Running     0          57m
openebs-ndm-node-exporter-wbg6j                                   1/1     Running     0          57m
openebs-ndm-node-exporter-xvppn                                   1/1     Running     0          57m
openebs-ndm-operator-686446d979-7vmhr                             1/1     Running     0          57m
pvc-087960e4-c718-4227-84f8-d3a6ca423295-target-c7bdc769-bq984    3/3     Running     0          12m
pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc-target-6d987f5cd5tc2mg   3/3     Running     0          4m4s
pvc-82a81b9a-d585-48b9-9b58-dc3f5b3c2461-target-6bb98988c-d52mb   3/3     Running     0          9m13s
pvc-9670d96c-f1e2-4e6a-a223-25960cf87b44-target-5bcc4c59dc5mzc7   3/3     Running     0          7m56s
pvc-dc70575e-499f-4737-a148-e511453df233-target-5d6f64db86j8d7w   3/3     Running     0          5m21s
pvc-eacb5ff7-6c28-4ad5-88eb-e877eaa51b56-target-58fbdd855-nsmgt   3/3     Running     0          10m
pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd-target-7b79b67bcb55b9l   3/3     Running     0          6m38s
```

## Fix VolumeAttachment Issue
After the upgrade was done, I ran into another issue. One of the pods was stuck in `ContainerCreating` state and when I described the pod I saw this error:

```bash
Warning  FailedMount  42s (x8 over 106s)  kubelet, nd  MountVolume.MountDevice failed for volume "pvc-343ccf62-" : rpc error: code = Internal desc = cstorvolumeattachments.cstor.openebs.io "pvc-343ccf62-" not found
```

I doubl checked and the `cva` didn't exist:

```bash
k get cva -n openebs | grep pvc-343ccf62-
```

On the same node where the pod was stuck I checked out the logs of the `csi-node` pod:

```bash
> k get po -n openebs -l role=openebs-cstor-csi -o wide | grep nd
openebs-cstor-csi-node-x5b78     2/2     Running   0            8h     192.168.1.53    nd     <none>           <none>
```

And for the logs:

```bash
> k logs -n openebs openebs-cstor-csi-node-x5b78 cstor-csi-plugin
...
time="2023-12-26T19:09:47Z" level=error msg="NodeUnPublishVolume: dir /var/lib/kubelet/pods/9883b6d2-ad22-41fc-a27d-910d876b4eb8/volumes/kubernetes.io~csi/pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd/mount does not exist"
```

The directory was indeed missing, but I was surpised that the directory for the pvc existed at all. And in the directory it only had `vol_data.json` file and nothing else. That felt like a left over directory that shouldn't be there, so I deleted it:

```bash
rm -rf /var/lib/kubelet/pods/9883b6d2-ad22-41fc-a27d-910d876b4eb8/volumes/kubernetes.io~csi/pvc-fc6ec633-d0e1-420c-b64b-cfefe3a425bd
```

And I restarted the `csi-node` pod:

```
k delete po -n openebs openebs-cstor-csi-node-x5b78
```

And then the pod came up without issues.
