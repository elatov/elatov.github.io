---
published: true
layout: post
title: "Using rook ceph"
author: Karim Elatov
categories: [storage, containers]
tags: [kubernetes, ceph, velero]
---

With the recent news about openEBS getting archived by CNCF [OpenEBS: Lessons We Learned from Open Source](https://thenewstack.io/openebs-lessons-we-learned-from-open-source/), I decided this was the time to try out another storage provider and I decided to try [rook-ceph](https://rook.io/docs/rook/latest-release/Getting-Started/intro/). I've heard so much about ceph in the past but I never really tried it... so this time around I decided to give it a chance. I have a pretty small k8s cluster with just 3 VMs running on a Proxmox server so I basically did the reverse of [Migrate a K3S cluster storage from Rook to OpenEBS, with Velero](https://www.cloudnative.quest/posts/kubernetes/2023-01-22/migrate-k3s-cluster-storage-from-rook-to-openebs-with-velero/).

## Backup applications with PVCs

In the past I used [velero](/2022/11/velero-and-openebs/) and it works quite well, so to be safe I backed up my applications:

```shell
velero backup create postges-backup -l app=postgres --snapshot-volumes --volume-snapshot-locations=default
velero backup create plex-backup -l app=plexserver --snapshot-volumes --volume-snapshot-locations=default
```

And I confirmed the backups were successful:

```shell
> velero backup get                    
NAME             STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
postges-backup   Completed   0        1          2024-07-13 08:33:18 -0600 MDT   29d       default            app=postgres
```

I also made app level backups for some of the applications:

```shell
# postgres
pg_dumpall -h postgres.kar.int -U postgres > all_pg_dbs.sql

# plex
k cp plexserver-7f8c78b456-xr4hn:/config plex-config-backup
```

I then deleted the applications that were using those PVCs (I knew I was going to be switching over storage classes so I wanted to make sure there are no conflicting configurations or left over objects). I use [argocd](/2021/12/deploying-and-using-argocd/) to manage all of my applications so I just logged into the UI and deleted them. But that's basically the same thing as :

```shell
kubectl delete deployment my_deployment
kubectl delete pvc my_pvc
```

## Uninstall openEBS

If you installed [openebs](https://openebs.io/docs/main/quickstart-guide/installation#installation-via-helm) with `helm` then it's as easy as :

```shell
helm uninstall openebs -n openebs
```

But if you are like me and installed it a while back or maybe just didn't use `helm`, then you can follow instructions from [Uninstalling OpenEBS](https://openebs.io/docs/3.10.x/user-guides/uninstall) and since I was also using the `cstor` volumes then we also have to follow instructions in [cStor User Guide - Clean Up](https://openebs.io/docs/3.10.x/user-guides/cstor/clean-up). You basically have to make sure to delete all the CRs that `openEBS` uses:

- `spc`
- `bdc`
- `cvr`
- `cstorvolume`
- `bd`
- `cspc`
- `cspi`

After you are done, delete the `openebs` namespace and if all the CRs are gone the `ns` will delete. If there are left over resources the namespace will be [stuck in Terminating state](https://github.com/openebs/openebs/issues/1901) and if you `describe` it will give you a hint as to which resources are still around:

```shell
kubectl desribe ns openebs
```

After the `ns` and `crds` are gone you should be all set

### Wiping the disks

After the uninstall I saw that the `zfs` file system was left behind on the disks:

```shell
> lsblk -f
NAME FSTYPE FSVER LABEL                  UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sdb                                                                                          
└─sdb1
     zfs_me 5000  cstor-62d0ad14-57c9-4571-95e3-84dec193c047
                                         1524832950104593316
```

And I had to wipe it twice:

```shell
> sudo wipefs -a /dev/sdb
/dev/sdb: 8 bytes were erased at offset 0x00000200 (gpt): 45 46 49 20 50 41 52 54
/dev/sdb: 8 bytes were erased at offset 0x18fffffe00 (gpt): 45 46 49 20 50 41 52 54
/dev/sdb: 2 bytes were erased at offset 0x000001fe (PMBR): 55 aa
/dev/sdb: calling ioctl to re-read partition table: Success
```

After the first one there were still some remnants of `zfs` left:

```shell
> lsblk -f               
NAME   FSTYPE     FSVER   LABEL                                      UUID                                   FSAVAIL FSUSE% MOUNTPOINTS
sdb    zfs_member 5000    cstor-62d0ad14-57c9-4571-95e3-84dec193c047 10313661773127100217
```

Then I wiped it a second time:

```shell
> sudo wipefs -a /dev/sdb
/dev/sdb: 8 bytes were erased at offset 0x18fffbfc00 (zfs_member): 0c b1 ba 00 00 00 00 00
/dev/sdb: 8 bytes were erased at offset 0x18fffbf800 (zfs_member): 0c b1 ba 00 00 00 00 00
/dev/sdb: 8 bytes were erased at offset 0x18fffbf400 (zfs_member): 0c b1 ba 00 00 00 00 00
```

Then it was clean:

```shell
> lsblk -f               
NAME FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sdb
```

This is a [Ceph Prerequisite](https://rook.io/docs/rook/latest-release/Getting-Started/Prerequisites/prerequisites/?h=#ceph-prerequisites)

## Installing rook-ceph

It looks like there are instructions with [manifest files](https://rook.io/docs/rook/latest-release/Getting-Started/quickstart/) and [helm charts](https://rook.io/docs/rook/latest-release/Helm-Charts/helm-charts/). I decided to use the `helm` chart with argoCD. 

### Troubleshooting Install Issues

After the `cephcluster` was deployed via `helm`, I saw it was unhealthy:

```shell
> k get cephclusters -A
NAMESPACE   NAME        DATADIRHOSTPATH   MONCOUNT   AGE   PHASE         MESSAGE                 HEALTH   EXTERNAL   FSID
rook-ceph   rook-ceph   /var/lib/rook     3          28m   Progressing   Configuring Ceph Mons 
```

Describing the cluster:

```shell
> k describe cephclusters -n rook-ceph rook-ceph
Events:
  Type     Reason           Age   From                          Message
  ----     ------           ----  ----                          -------
  Warning  ReconcileFailed  24m   rook-ceph-cluster-controller  failed to reconcile CephCluster "rook-ceph/rook-ceph". failed to reconcile cluster "rook-ceph": failed to configure local ceph cluster: failed to create cluster: failed to start ceph monitors: failed to assign pods to mons: failed to schedule mons
```

Looking at the `pods`:

```shell
> k get po -n rook-ceph
NAME                                           READY   STATUS     RESTARTS      AGE
csi-rbdplugin-kpngn                            2/2     Running    1 (27m ago)   27m
csi-rbdplugin-lpc27                            2/2     Running    0             27m
csi-rbdplugin-provisioner-7c6dcb4dff-l6rr4     5/5     Running    2 (26m ago)   27m
csi-rbdplugin-provisioner-7c6dcb4dff-v5cp7     5/5     Running    3 (25m ago)   27m
csi-rbdplugin-tbc5c                            2/2     Running    1 (28m ago)   27m
rook-ceph-crashcollector-ma-f896477f4-hmx9j    1/1     Running    0             21m
rook-ceph-crashcollector-nc-7cbcc6fc4c-89fnq   1/1     Running    0             21m
rook-ceph-crashcollector-nd-694d688894-w4f9j   1/1     Running    0             21m
rook-ceph-exporter-ma-5c9558cfc9-8nzlg         0/1     Init:0/1   0             21m
rook-ceph-exporter-nc-845cd8bcdb-nqqvn         0/1     Init:0/1   0             21m
rook-ceph-exporter-nd-74f4d4894c-69tph         0/1     Init:0/1   0             21m
rook-ceph-mon-a-67865c4b7-w7trk                2/2     Running    0             22m
rook-ceph-mon-b-79664fccb5-qtbb4               2/2     Running    0             22m
rook-ceph-mon-c-fc5cd47bb-wc72d                2/2     Running    0             22m
rook-ceph-operator-7b786cb7fd-94bvb            1/1     Running    0             11h
rook-ceph-tools-7bddb946bd-66swh               1/1     Running    0             29m
```

The `mon` pods are actually up. I checked the logs and nothing crazy stood out. So using the `ceph-tools`, pod I checked out the `ceph status`:

```shell
> k exec -it -n rook-ceph rook-ceph-tools-7bddb946bd-66swh -- /bin/bash
bash-4.4$ ceph status
  cluster:
    id:     346c16bc-307c-4324-8f6d-5c1d782aadda
    health: HEALTH_WARN
            mons are allowing insecure global_id reclaim
            clock skew detected on mon.b, mon.c
            mons a,b are low on available space

  services:
    mon: 3 daemons, quorum a,b,c (age 24m)
    mgr: no daemons active
    osd: 0 osds: 0 up, 0 in

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs: 
```

I was surprised to see the low space warning, I then ran into [this issue](https://github.com/rook/rook/issues/11130), it looks like by default it checks to make sure you have at least `30%` free space, this was just a lab setup and I didn't have that much space, so I modified my `values.yaml` and added the following:

```yaml
configOverride: |
  [global]
  mon_data_avail_warn = 10
```

I also realized 3 `mon` pods might be too much for my lab, so I also modified that:

```yaml
cephClusterSpec:
  crashCollector:
    disable: true
  mon:
    count: 1
  mgr:
    count: 1
```

There are some nice options defined in the [rook/deploy/examples
/cluster-test.yaml](https://github.com/rook/rook/blob/master/deploy/examples/cluster-test.yaml) file, if you running a non-production cluster (I think this can save some resources, if you are willing to risk an outage)

Then I deleted and reinstalled using `helm` and I saw all the pods healthy:

```shell
> k get po -n rook-ceph 
NAME                                         READY   STATUS      RESTARTS        AGE
csi-rbdplugin-2wn5l                          2/2     Running     0               4h42m
csi-rbdplugin-48j9h                          2/2     Running     2 (4h26m ago)   4h42m
csi-rbdplugin-824jg                          2/2     Running     0               4h42m
csi-rbdplugin-provisioner-7c6dcb4dff-mn7s4   5/5     Running     0               4h22m
csi-rbdplugin-provisioner-7c6dcb4dff-v994d   5/5     Running     0               4h42m
rook-ceph-exporter-ma-5c9558cfc9-bhh45       1/1     Running     0               4h30m
rook-ceph-exporter-nc-845cd8bcdb-fl5p6       1/1     Running     0               4h22m
rook-ceph-exporter-nd-74f4d4894c-b54pk       1/1     Running     0               4h26m
rook-ceph-mgr-a-5b8f65d64b-9kpp9             2/2     Running     0               96m
rook-ceph-mon-a-7bbfff855b-fh8lg             2/2     Running     0               4h31m
rook-ceph-operator-7b786cb7fd-zp9lz          1/1     Running     0               4h26m
rook-ceph-osd-0-57cbdfc6b4-kcq2m             2/2     Running     0               4h30m
rook-ceph-osd-1-7897c855f9-xqrxx             2/2     Running     0               4h30m
rook-ceph-osd-2-56545b5ff-ptpsl              2/2     Running     0               4h26m
rook-ceph-osd-prepare-ma-2czsq               0/1     Completed   0               94m
rook-ceph-osd-prepare-nc-f8b5p               0/1     Completed   0               94m
rook-ceph-osd-prepare-nd-b6dfb               0/1     Completed   0               94m
rook-ceph-tools-7bddb946bd-nk7lv             1/1     Running     0               4h26m
```

As a last test I cheched to make sure the health and disk space is correct:

```shell
> k exec -it -n rook-ceph rook-ceph-tools-7bddb946bd-nk7lv -- /bin/bash
bash-4.4$ ceph health
HEALTH_OK
bash-4.4$ ceph df
--- RAW STORAGE ---
CLASS     SIZE    AVAIL     USED  RAW USED  %RAW USED
hdd    300 GiB  294 GiB  6.5 GiB   6.5 GiB       2.16
TOTAL  300 GiB  294 GiB  6.5 GiB   6.5 GiB       2.16

--- POOLS ---
POOL            ID  PGS   STORED  OBJECTS     USED  %USED  MAX AVAIL
.rgw.root        1   32      0 B        0      0 B      0     93 GiB
ceph-blockpool   2   32  1.5 GiB      441  4.6 GiB   1.62     93 GiB
.mgr             3    1  577 KiB        2  1.7 MiB      0     93 GiB
```

Even though I have 1 `mon`, I decided to still use 3 for the `osd_pool_size`, that way it will replicate across multiple nodes/`osd`. As expected we can see I have a total of `300G` of raw storage but only `95G` from the available spaces in my pool.

### Disabled SSL on the ceph dashboard

Since it's just an internal deployment, I didn't really need to enable `ssl` on the dashboard. Initially I just disabled it, but it still didn't work. I ran into [this old issue](https://github.com/rook/rook/issues/13577) and it looks like if you disable SSL you have to specify the port. So I updated my `values.yaml`:

```yaml
  dashboard:
    enabled: true
    ssl: false
    port: 8080
    urlPrefix: /
```

And let `argoCD` reapply that and then I was able to reach the dashboard without issues. To get the default admin password we can use the instructions from [Ceph Dashboard](https://rook.io/docs/rook/latest-release/Storage-Configuration/Monitoring/ceph-dashboard/#login-credentials), and grab it from the secret:

```shell
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
```

And I saw the dashboard with a healthy cluster:

![ceph-dashboard.png](https://res.cloudinary.com/elatov/image/upload/v1720906403/blog-pics/openebs-to-rook/ddbljy4pq25dyfnqomi9.png)

## Restoring the applications

I reinstalled the applications using argoCD and for the data I actually just left the velero backups in the storage bucket for now and I manually restored my postgres db:

```shell
# back everything up
pg_dumpall -h postgres.kar.int -U postgres > all_pg_dbs.sql

# restore
psql -h postgres.kar.int -U postgres -f all_pg_dbs.sql
```

And for my plex instance, I just backed up the `Library` directory and copied it back:

```shell
# backup
k cp plexserver-7f8c78b456-xr4hn:/config plex-config-backup

# restore
k cp plex-config-backup/Library plexserver-7f8c78b456-f72zl:/config/
```

I will play around with the restoration from velero for the other apps next.
