---
published: true
layout: post
title: "Deploying and Using ArgoCD"
author: Karim Elatov
categories: [devops, automation, containers]
tags: [argocd, prometheus, slack]
---
## Install ArgoCD

Most of the instructions are from the [Getting Started Guide](https://argo-cd.readthedocs.io/en/stable/getting_started/)

```bash
> kubectl create namespace argocd
namespace/argocd created
> kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
...
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/appprojects.argoproj.io created
serviceaccount/argocd-application-controller created
```

After a litte bit you should see all the pods deployed:

```bash
> k get pods -n argocd
NAME                                  READY   STATUS    RESTARTS   AGE
argocd-application-controller-0       1/1     Running   0          7m7s
argocd-dex-server-6dcf645b6b-p2xjd    1/1     Running   0          7m7s
argocd-redis-5b6967fdfc-97ttj         1/1     Running   0          7m7s
argocd-repo-server-7598bf5999-mwsbz   1/1     Running   0          7m7s
argocd-server-79f9bc9b44-7fvnv        1/1     Running   0          7m7s
```

I then followed instructions in [Ingress Configuration](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/) to expose the ArgoCD UI:

```bash
> k apply -f ingress.yaml
ingress.networking.k8s.io/argocd-server-ingress created
```

If all is well you should see the following in the events (if you are using `cert-manager`):

```bash
> k get events --sort-by='.metadata.creationTimestamp' -A -w
ingress-nginx   2s          Normal   RELOAD              pod/nginx-ingress-controller-6c8d74ffc-b6nmd          NGINX reload triggered due to a change in configuration
argocd          2s          Normal   Requested           certificate/argocd-secret                             Created new CertificateRequest resource "argocd-secret-wwpsc"
argocd          2s          Normal   Reused              certificate/argocd-secret                             Reusing private key stored in existing Secret resource "argocd-secret"
argocd          2s          Normal   Issuing             certificate/argocd-secret                             Issuing certificate as Secret was previously issued by Issuer.cert-manager.io/
argocd          2s          Normal   OrderPending        certificaterequest/argocd-secret-wwpsc                Waiting on certificate issuance from order argocd/argocd-secret-wwpsc-3668447565: ""
argocd          2s          Normal   OrderCreated        certificaterequest/argocd-secret-wwpsc                Created Order resource argocd/argocd-secret-wwpsc-3668447565
argocd          2s          Normal   cert-manager.io     certificaterequest/argocd-secret-wwpsc                Certificate request has been approved by cert-manager.io
argocd          2s          Normal   CreateCertificate   ingress/argocd-server-ingress                         Successfully created Certificate "argocd-secret"
argocd          1s          Normal   Created             order/argocd-secret-wwpsc-3668447565                  Created Challenge resource "argocd-secret-wwpsc-3668447565-2818668963" for domain "argocd.kar.int"
argocd          0s          Normal   Started             challenge/argocd-secret-wwpsc-3668447565-2818668963   Challenge scheduled for processing
argocd          0s          Normal   Presented           challenge/argocd-secret-wwpsc-3668447565-2818668963   Presented challenge using DNS-01 challenge mechanism
argocd          0s          Normal   Sync                ingress/argocd-server-ingress                         Scheduled for sync
argocd          0s          Normal   DomainVerified      challenge/argocd-secret-wwpsc-3668447565-2818668963   Domain "argocd.kar.int" verified with "DNS-01" validation
argocd          0s          Normal   Complete            order/argocd-secret-wwpsc-3668447565                  Order completed successfully
argocd          0s          Normal   CertificateIssued   certificaterequest/argocd-secret-wwpsc                Certificate fetched from issuer successfully
argocd          0s          Normal   Issuing             certificate/argocd-secret                             The certificate has been successfully issued
```

## Login to ArgoCD

We are going to need the `argocd` binary to configure ArgoCD, so let's get that:

```bash
> curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.1.7/argocd-linux-amd64
> mv argocd-linux-amd64 argocd
> chmod +x argocd
> sudo mv argocd /usr/local/bin/
```

Now let's get the initially created password:

```bash
> kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Now we can login with `admin/above_password`:

```bash
> argocd login argocd.kar.int
Username: admin
Password:
'admin:login' logged in successfully
Context 'argocd.kar.int' updated
```

We can and should change the default password:

```bash
> argocd account update-password
*** Enter current password:
*** Enter new password:
*** Confirm new password:
Password updated
Context 'argocd.kar.int' updated
```

## ArgoCD Configurations

I ended up creating a couple of resources, so let's break them down.

### Adding Kubernetes Cluster

By default ArgoCD able to use the cluster it's deployed on:

```bash
> argocd cluster list
SERVER                          NAME        VERSION  STATUS   MESSAGE
https://kubernetes.default.svc  in-cluster           Unknown  Cluster has no application and not being monitored.
```

If you need to add another cluster make sure `kubectl` is already using the appropriate `kubeconfig` and the context is set. Then you can add a kubernetes cluster of your choice:

```bash
> kubectl config get-contexts -o name
gke_kar-int_us-west4-a_my-gke-cluster
kerch-kube-cluster
```

And then add it:

```bash
> argocd cluster add kerch-kube-cluster
WARNING: This will create a service account `argocd-manager` on the cluster referenced by context `kerch-kube-cluster` with full cluster level admin privileges. Do you want to continue [y/N]? y
INFO[0006] ServiceAccount "argocd-manager" created in namespace "kube-system"
INFO[0006] ClusterRole "argocd-manager-role" created
INFO[0006] ClusterRoleBinding "argocd-manager-role-binding" created
Cluster 'https://kubeapi.kar.int' added
```

After some time it should show an appropriate status of the connection to the cluster:

```bash
> argocd cluster list
SERVER                          NAME                VERSION  STATUS      MESSAGE
https://kubeapi.kar.int         kerch-kube-cluster  1.23     Successful
https://kubernetes.default.svc  in-cluster          1.21     Successful
```

### Add a Github Repo

First let's Generate an ssh key to login to github with:

```bash
> ssh-keygen -t ed25519 -f argocd
```

Then add the key to your github settings. Next we can add a repo:

```bash
> argocd repo add git@github.com:elatov/k8s-prometheus.git --ssh-private-key-path /data/local/ssh-keys/argocd --name prometheus
Repository 'git@github.com:elatov/k8s-prometheus.git' added
```

You can make sure the connection is good by just listing the repos:

```bash
> argocd repo list
TYPE  NAME        REPO                                      INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE
git   prometheus  git@github.com:elatov/k8s-prometheus.git  false     false  false  false  Successful
```

Now let's add an application that uses a [kustomize overlay](https://elatov.github.io/2021/08/using-kustomize/):

```bash
> argocd app create prometheus --repo git@github.com:elatov/k8s-prometheus.git --path overlays/gcp --dest-server https://kubernetes.default.svc --dest-namespace default --sync-policy auto
```

If all is well you should see the app auto synced and healthy:

```bash
> argocd app list
NAME        CLUSTER                         NAMESPACE  PROJECT  STATUS  HEALTH   SYNCPOLICY  CONDITIONS  REPO                                      PATH          TARGET
prometheus  https://kubernetes.default.svc  default    default  Synced  Healthy  Auto        <none>      git@github.com:elatov/k8s-prometheus.git  overlays/gcp
```

You can also use `kubectl` to get similar information:

```bash
> k get applications -n argocd
NAME         SYNC STATUS   HEALTH STATUS
prometheus   Synced        Healthy
```

### Using ArgoCD Metrics with Prometheus

[This page](https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/) has nice descriptions of how to use the metrics:

1. Enable the pod annotations
```bash
> kubectl -n argocd annotate service argocd-metrics prometheus.io/scrape="true"
> kubectl -n argocd annotate service argocd-metrics prometheus.io/port="8082"
> kubectl -n argocd annotate service argocd-server-metrics prometheus.io/scrape="true"
> kubectl -n argocd annotate service argocd-server-metrics prometheus.io/port="8083"
```
2. Using the [Prometheus Operator](https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/metrics.md#prometheus-operator) as described in the link. (I wasn't use the operator so this option wasn't available to me)
3. Add the exposed service as a scape endpoint to the prometheus configuration. (this is the route I went since I didn't want to keep updating my annotations after each `argocd` update.)

So I added the following configuration to my prometheus `scape_config`:

```bash
- job_name: 'argocd-app-metrics'
  scrape_interval: 15s
  static_configs:
  - targets: ['argocd-metrics.argocd.svc.cluster.local:8082']
- job_name: 'argocd-server-metrics'
  scrape_interval: 15s
  static_configs:
  - targets: ['argocd-server-metrics.argocd.svc.cluster.local:8083']
- job_name: 'argocd-repo-metrics'
  scrape_interval: 15s
  static_configs:
  - targets: ['argocd-repo-server.argocd.svc.cluster.local:8084']
```

The [Metrics](https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/metrics.md) page contains a list of all the available metrics, after I added the above I was able to query them in `prometheus`:

![prom-argo-cd-metrics.png](https://res.cloudinary.com/elatov/image/upload/v1639356856/blog-pics/argocd-deploy/prom-argo-cd-metrics.png)

And also adding the [official ArgoCD grafana dashboard](https://grafana.com/grafana/dashboards/14584), made it easy to visualize all the
build components:

![grafana-argocd-dash.png](https://res.cloudinary.com/elatov/image/upload/v1639356856/blog-pics/argocd-deploy/grafana-argocd-dash.png)

### ArgoCD Notifications

Recently the ArgoCD Notifications project became part of the main ArgoCD project. It supports Slack and other services as well. I actually wanted to see how to use slack with it. Some nice examples of the slack are seen [here](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/services/slack/). So let's install the controller first:

```bash
> kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/v1.1.0/manifests/install.yaml
```

And let's install the templates:

```bash
> kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/v1.1.0/catalog/install.yaml
```

After some time you should see the controller deployed:

```bash
> k get pods -l app.kubernetes.io/name=argocd-notifications-controller -n argocd
NAME                                               READY   STATUS    RESTARTS   AGE
argocd-notifications-controller-5c548f8dc9-rgx5n   1/1     Running   0          104s
```
Create a Slack app as per the instructions in [Slack Configuration](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/services/slack/) and don't forget to add the app into the desired channel:

![slack-argocd-app-added.png](https://res.cloudinary.com/elatov/image/upload/v1639356856/blog-pics/argocd-deploy/slack-argocd-app-added.png)

Next let's add the slack token as a secret:

```bash
> export TOKEN="xoxb-xxxxx"
> kubectl apply -n argocd -f - << EOF
apiVersion: v1
kind: Secret
metadata:
  name: argocd-notifications-secret
stringData:
  slack-token: ${TOKEN}
type: Opaque
EOF
```

Now let's register the slack service:

```bash
> kubectl patch cm argocd-notifications-cm -n argocd --type merge -p '{"data": {"service.slack": "{ token: $slack-token }" }}'
```

Now let's enable the notification on one of the apps:

```bash
> kubectl patch app prometheus -n argocd -p '{"metadata": {"annotations": {"notifications.argoproj.io/subscribe.on-sync-succeeded.slack":"general"}}}' --type merge
application.argoproj.io/prometheus patched
```

And you should see a message get to slack right away:

![slack-argocd-message.png](https://res.cloudinary.com/elatov/image/upload/v1639356856/blog-pics/argocd-deploy/slack-argocd-message.png)

You can also enable them globally as described in [Default Subscriptions](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/subscriptions/#default-subscriptions). So I created the following to config to enable all the triggers:

```bash
> cat argocd-notifications-cm-merge.yaml
data:
  # Contains centrally managed global application subscriptions
  subscriptions: |
    # subscription for on-sync-status-unknown trigger notifications
    - recipients:
      - slack:general
      triggers:
      - on-sync-status-unknown
      - on-created
      - on-deleted
      - on-deployed
      - on-health-degraded
      - on-sync-failed
      - on-sync-running
      - on-sync-succeeded
```

And then for the merge:

```bash
> kubectl patch cm argocd-notifications-cm -n argocd --type merge -p "$(cat argocd-notifications-cm-merge.yaml)"
configmap/argocd-notifications-cm patched
```

And I received notifications about all the app deployed in ArgoCD.