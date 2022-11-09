---
published: true
layout: post
title: "Velero and OpenEBS"
author: Karim Elatov
categories: [storage,containers]
tags: [velero,kubernetes,openebs]
---

I wanted to move one of my openEBS volumes from one cluster to another and I realized I could do it by performing a backup and restore with [velero](https://velero.io/). I deciced to use Google Cloud Storage for the backup storage. So let's configure that first.

## Configure GCP

From [Plugins for Google Cloud Platform (GCP)](https://github.com/vmware-tanzu/velero-plugin-for-gcp#setup). Let's get the right service account:

```bash
PROJECT_ID=$(gcloud config get-value project)
BUCKET="YOUR_BUCKET"

# create account
GSA_NAME=velero
gcloud iam service-accounts create $GSA_NAME \
    --display-name "Velero service account"

# get email of sa
SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts list \
  --filter="displayName:Velero service account" \
  --format 'value(email)')

# Create custom role
ROLE_PERMISSIONS=(
    compute.disks.get
    compute.disks.create
    compute.disks.createSnapshot
    compute.snapshots.get
    compute.snapshots.create
    compute.snapshots.useReadOnly
    compute.snapshots.delete
    compute.zones.get
    storage.objects.create
    storage.objects.delete
    storage.objects.get
    storage.objects.list
)

gcloud iam roles create velero.server \
    --project $PROJECT_ID \
    --title "Velero Server" \
    --permissions "$(IFS=","; echo "${ROLE_PERMISSIONS[*]}")"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role projects/$PROJECT_ID/roles/velero.server

gsutil iam ch serviceAccount:$SERVICE_ACCOUNT_EMAIL:objectAdmin gs://${BUCKET}

# export key
gcloud iam service-accounts keys create credentials-velero \
    --iam-account $SERVICE_ACCOUNT_EMAIL
```

Now let's do the install

```
$ wget https://github.com/vmware-tanzu/velero/releases/download/v1.9.2/velero-v1.9.2-linux-amd64.tar.gz
$ tar xvzf velero-v1.9.2-linux-amd64.tar.gz
$ mv velero-v1.9.2-linux-amd64/velero /usr/local/bin/.
$ velero install \
    --provider gcp \
    --plugins velero/velero-plugin-for-gcp:v1.5.0 \
    --bucket $BUCKET \
    --secret-file ./credentials-velero
```

Initially I tried using the default CSI plugin but the backup didn't work so I kep going without it (From [CSI Support](https://velero.io/docs/v1.9/csi/)):

```
--features=EnableCSI
```

At this point you should see a successful connection to GCP:

```bash
> velero backup-location get
NAME      PROVIDER   BUCKET/PREFIX      PHASE       LAST VALIDATED                 ACCESS MODE   DEFAULT
default   gcp        $BUCKET            Available   2022-10-26 MDT   ReadWrite     true
```

## Install OpenEBS Plugin

From [Velero-plugin for OpenEBS CStor volume](https://github.com/openebs/velero-plugin). First let's enable the plugin:

```bash
velero plugin add openebs/velero-plugin:1.11.0
```

Then let's configure the snapshot location, example is available [here](https://github.com/openebs/velero-plugin/tree/develop/example):

```bash
> cat volume-snapshot.yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: gcp-bucket
  namespace: velero
spec:
  provider: openebs.io/cstor-blockstore
  config:
    bucket: $BUCKET
    prefix: oebs
    provider: gcp
    restApiTimeout: 1m
    namespace: openebs
    autoSetTargetIP: "true"
```

Now let's take a backup including PVCs:

```bash
velero backup create postges-backup -l app=postgres --snapshot-volumes --volume-snapshot-locations=gcp-bucket
```

If all is well you should see the backup:

```bash
> velero backup describe postges-backup
Name:         postges-backup
Namespace:    velero
Labels:       velero.io/storage-location=default
Annotations:  velero.io/source-cluster-k8s-gitversion=v1.25.3
              velero.io/source-cluster-k8s-major-version=1
              velero.io/source-cluster-k8s-minor-version=25

Phase:  Completed
Errors:    0
Warnings:  39

Namespaces:
  Included:  *
  Excluded:  <none>

Resources:
  Included:        *
  Excluded:        <none>
  Cluster-scoped:  auto

Label selector:  app=postgres
Storage Location:  default
Velero-Native Snapshot PVs:  true
TTL:  720h0m0s
Hooks:  <none>
Backup Format Version:  1.1.0
Started:    2022-10-26 12:43:23 -0600 MDT
Completed:  2022-10-26 12:45:38 -0600 MDT
Expiration:  2022-11-25 11:43:23 -0700 MST
Total items to be backed up:  11
Items backed up:              11
Velero-Native Snapshots:  1 of 1 snapshots completed successfully (specify --details for more information)
CSI Volume Snapshots: <none included>
```

If you add `--details`, you will information about the snapshot:

```bash
> velero backup describe postges-backup --details
Name:         postges-backup
Namespace:    velero
Labels:       velero.io/storage-location=default
Annotations:  velero.io/source-cluster-k8s-gitversion=v1.25.3
              velero.io/source-cluster-k8s-major-version=1
              velero.io/source-cluster-k8s-minor-version=25

Phase:  Completed

Errors:    0
Warnings:  39

Namespaces:
  Included:  *
  Excluded:  <none>

Resources:
  Included:        *
  Excluded:        <none>
  Cluster-scoped:  auto
Label selector:  app=postgres
Storage Location:  default
Velero-Native Snapshot PVs:  true
TTL:  720h0m0s
Hooks:  <none>
Backup Format Version:  1.1.0
Started:    2022-10-26 12:43:23 -0600 MDT
Completed:  2022-10-26 12:45:38 -0600 MDT
Expiration:  2022-11-25 11:43:23 -0700 MST
Total items to be backed up:  11
Items backed up:              11
Resource List:
  apps/v1/ReplicaSet:
    - default/postgres-54bc4544cc
    - default/postgres-5c46bff6f7
    - default/postgres-5d96dd444b
    - default/postgres-7fc7bbf7f6
    - default/postgres-868f4bdc9b
  discovery.k8s.io/v1/EndpointSlice:
    - default/postgres-mbw4d
  v1/Endpoints:
    - default/postgres
  v1/PersistentVolume:
    - pvc-1841a854-439f-423e-a54c-bf402128689b
  v1/PersistentVolumeClaim:
    - default/postgres-data-pvc
  v1/Pod:
    - default/postgres-5d96dd444b-d2z2h
  v1/Service:
    - default/postgres

Velero-Native Snapshots:
  pvc-1841a854-439f-423e-a54c-bf402128689b:
    Snapshot ID:        pvc-1841a854-439f-423e-a54c-bf402128689b-velero-bkp-postges-backup
    Type:               cstor-snapshot
    Availability Zone:
    IOPS:               <N/A>

CSI Volume Snapshots: <none included>
```

## Restoring a backup on another cluster
I deployed velero the same way on another cluster:

```bash
## install velero
$ export BUCKET=staging.grand-drive-196322.appspot.com
$ velero install \
    --provider gcp \
    --plugins velero/velero-plugin-for-gcp:v1.5.0 \
    --bucket $BUCKET \
    --secret-file ./credentials-velero \
    --features=EnableCSI
## install the openebs plugin
$ velero plugin add openebs/velero-plugin:1.11.0
## Configure the VolumeStapshotLocation
kubectl apply -f volume-snapshot.yaml
```

Then I saw the backups from that cluster:


```bash
> velero backup get
NAME              STATUS      ERRORS   WARNINGS   CREATED                        EXPIRES   STORAGE LOCATION   SELECTOR
postges-backup   Completed   0        39         2022-10-26 12:43:23 -0600 MDT   29d       default            app=postgres
```

Now let's try the restore:

```bash
> velero restore create --from-backup postges-backup --restore-volumes=true
```

Initially the restore will show up as partially failed:

```
> velero restore get
NAME                            BACKUP           STATUS            STARTED                         COMPLETED                       ERRORS   WARNINGS   CREATED                         SELECTOR
postges-backup-20221026143436   postges-backup   PartiallyFailed   2022-10-26 14:34:36 -0600 MDT   2022-10-26 14:40:31 -0600 MDT   1        1          2022-10-26 14:34:36 -0600 MDT   <none>
```

And this is expected since there is a known issue with the openebs restore and you have to manually set the targetIP (this is covered in [Setting targetip in replica](https://github.com/openebs/velero-plugin#setting-targetip-in-replica)). First get the PV name:

```bash
> PV_NAME=$(k get  pv -o json | jq -r '.items[]| select( .spec.claimRef.name | contains("postgres")).metadata.name')
> echo $PV_NAME
pvc-dc70575e-499f-4737-a148-e511453df233
```

Then get the target IP:

```bash
> TAR_IP=$(kubectl get svc -n openebs $PV_NAME -ojsonpath='{.spec.clusterIP}')
> echo $TAR_IP
10.233.35.19
```

Next get the Disk Pools serving the PVC:

```bash
> DISK_POOLS=( $(for r in $(k get cvr -n openebs -o json | jq -r ".items[]| select( .metadata.name | contains(\"$PV_NAME\"))".metadata.name); do echo $r| sed s/$PV_NAME-//; done) )
> echo $DISK_POOLS
cstor-disk-pool-2qqg cstor-disk-pool-jfz2
```

Now let's get the corresponding pods for those pool instances:

```bash
> POOL_PODS=( $(for dp in $DISK_POOLS; do k get pods -n openebs -o json | jq -r ".items[]| select( .metadata.name | contains(\"$dp\"))".metadata.name; done) )
> echo $POOL_PODS
cstor-disk-pool-2qqg-7857745dc-mjjn2 cstor-disk-pool-jfz2-68c9786bd7-4qmxt
```


Next you can check all the pods to see which disk don't have an IP set for the target:

```
> for pool_pod in $POOL_PODS; do echo $pool_pod; kubectl -n openebs exec -it $pool_pod -c cstor-pool -- bash -c 'zfs get io.openebs:targetip';  done
cstor-disk-pool-2qqg-7857745dc-mjjn2
NAME                                                                                                PROPERTY             VALUE          SOURCE
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2                                                          io.openebs:targetip  -              -
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-087960e4-c718-4227-84f8-d3a6ca423295                 io.openebs:targetip  10.233.30.198  local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-45bb9001-5a14-40b7-8caa-fcae972c31bc                 io.openebs:targetip  10.233.60.140  local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-9670d96c-f1e2-4e6a-a223-25960cf87b44                 io.openebs:targetip  10.233.33.71   local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233                 io.openebs:targetip                
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233@postges-backup  io.openebs:targetip  -              -
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-eacb5ff7-6c28-4ad5-88eb-e877eaa51b56                 io.openebs:targetip  10.233.27.53   local
cstor-disk-pool-jfz2-68c9786bd7-4qmxt
NAME                                                                                                PROPERTY             VALUE          SOURCE
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2                                                          io.openebs:targetip  -              -
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-087960e4-c718-4227-84f8-d3a6ca423295                 io.openebs:targetip  10.233.30.198  local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-1c2664d4-a7e6-4182-8535-1cfad2ec6c0c                 io.openebs:targetip  10.233.52.183  local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-82a81b9a-d585-48b9-9b58-dc3f5b3c2461                 io.openebs:targetip  10.233.48.159  local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-9670d96c-f1e2-4e6a-a223-25960cf87b44                 io.openebs:targetip  10.233.33.71   local
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233                 io.openebs:targetip  
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233@postges-backup  io.openebs:targetip  -              -
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-eacb5ff7-6c28-4ad5-88eb-e877eaa51b56                 io.openebs:targetip  10.233.27.53   local
```

You could also run the following to check all the disk pools:

```bash
> for pool_pod in $(k get pods -l openebs.io/cstor-pool-cluster=cstor-disk-pool -n openebs -o name); do echo $pool_pod; kubectl -n openebs exec -it $pool_pod -c cstor-pool -- bash -c 'zfs get io.openebs:targetip';  done
```

Since I have two replica enabled for my openebs configurations that's why we only see two PVCs with the missing target IP. So now let's update all the PVCs:

```bash
> for pp in $POOL_PODS; do echo $pp; for pvc in $(k exec $pp -c cstor-pool -n openebs -- bash -c "zfs get io.openebs:targetip" | grep io.openebs:targetip | grep $PV_NAME | grep -v '@' | cut -d" " -f1); do echo $pvc; kubectl exec $pp -c cstor-pool -n openebs -- bash -c "zfs set io.openebs:targetip=$TAR_IP $pvc"; done ; done
cstor-disk-pool-2qqg-7857745dc-mjjn2
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233
cstor-disk-pool-jfz2-68c9786bd7-4qmxt
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233
```

To confirm it worked, we can run the following:

```bash
> for pp in $POOL_PODS; do echo $pp; for pvc in $(k exec $pp -c cstor-pool -n openebs -- bash -c "zfs get io.openebs:targetip" | grep io.openebs:targetip | grep $PV_NAME | grep -v '@' | cut -d" " -f1); do k exec $pp -c cstor-pool -n openebs -- bash -c "zfs get io.openebs:targetip $pvc" ;  done ; done
cstor-disk-pool-2qqg-7857745dc-mjjn2
NAME                                                                                 PROPERTY             VALUE         SOURCE
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233  io.openebs:targetip  10.233.35.19  local
cstor-disk-pool-jfz2-68c9786bd7-4qmxt
NAME                                                                                 PROPERTY             VALUE         SOURCE
cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233  io.openebs:targetip  10.233.35.19  local
```

After that you will see the your pod be able to use the PVC:

```bash
openebs     7m32s       Warning   SyncFailed         cstorvolumereplica/pvc-dc70575e-499f-4737-a148-e511453df233-cstor-disk-pool-2qqg   failed to sync CVR error: unable to update snapshot list details in CVR: failed to get the list of snapshots: Output: failed listsnap command for cstor-adfe63f7-5c10-425d-801a-1b299bfa3dc2/pvc-dc70575e-499f-4737-a148-e511453df233 with err 2...
openebs     6m50s       Normal    Degraded           cstorvolume/pvc-dc70575e-499f-4737-a148-e511453df233                               Volume is in Degraded state
openebs     6m20s       Normal    Healthy            cstorvolume/pvc-dc70575e-499f-4737-a148-e511453df233                               Volume is in Healthy state
default     112s        Normal    Scheduled          pod/postgres-5d96dd444b-cpldr                                                      Successfully assigned default/postgres-5d96dd444b-cpldr to nc
default     112s        Normal    SuccessfulCreate   replicaset/postgres-5d96dd444b                                                     Created pod: postgres-5d96dd444b-cpldr
```

And it will marked as used by our pod:

```bash
> k describe pvc postgres-data-pvc
Name:          postgres-data-pvc
Namespace:     default
StorageClass:  cstor-csi-disk
Status:        Bound
Volume:        pvc-dc70575e-499f-4737-a148-e511453df233
Labels:        app.kubernetes.io/instance=postgres-home
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
               volume.beta.kubernetes.io/storage-provisioner: cstor.csi.openebs.io
               volume.kubernetes.io/storage-provisioner: cstor.csi.openebs.io
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      5Gi
Access Modes:  RWO
VolumeMode:    Filesystem
Used By:       postgres-5d96dd444b-cpldr
Events:        <none>
```


## Uninstall Velero
If you ever need to uninstall we can follow the instructions from [Uninstalling Velero](https://velero.io/docs/v1.9/uninstalling/):

```bash
kubectl delete namespace/velero clusterrolebinding/velero
kubectl delete crds -l component=velero
```
