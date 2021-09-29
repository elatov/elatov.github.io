---
published: true
layout: post
title: "Using Hashicorp Vault on Kubernetes"
author: Karim Elatov
categories: [containers]
tags: [kubernetes, vault, csi]
---
I wanted to deploy hashicorp **vault** on a kubernetes clusters just to see how the integration works out. Here are some of the steps I took to deploy **vault** in my kubernetes cluster.

## Prereqs
Here are some tools I need to install prior to running through the setup.
### Install helm
First we need to install `helm`, the setup is covered in [Installing Helm](https://helm.sh/docs/intro/install/#from-apt-debianubuntu):

```bash
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

## Setting up Vault
There are a bunch of steps, so let's break them down into sections:

### Installing Vault in K8S
Most instructions are available at [Vault on Kubernetes Deployment Guide](https://learn.hashicorp.com/tutorials/vault/kubernetes-raft-deployment-guide). First we need to add the **helm** repo:

```bash
> helm repo add hashicorp https://helm.releases.hashicorp.com
"hashicorp" has been added to your repositories
```

Then we can check out the latest version of package:

```bash
> helm search repo hashicorp/vault
NAME           	CHART VERSION	APP VERSION	DESCRIPTION
hashicorp/vault	0.16.0       	1.8.2      	Official HashiCorp Vault Chart
```

Now we can use `helm` to get all the k8s manifests:

```bash
> helm template vault hashicorp/vault --set "injector.enabled=false"
```

After I got all resources templated out, I used `kustomize` to apply them:

```bash
> k apply -k base
serviceaccount/vault created
clusterrolebinding.rbac.authorization.k8s.io/vault-server-binding created
configmap/vault-config created
service/vault created
statefulset.apps/vault created
```

### Post Install Configuration of Vault
Now let's initialze the **vault**:

```
> kubectl exec --stdin=true --tty=true vault-0 -- vault operator init
Unseal Key 1: KEPop9G9Qi+3ypNks1KqpE4qydVf1TB/5aDd/NDVMeI7
Unseal Key 2: H5QLGcEiOxcXuynA6zilQs6DCiad0z6AHz4Gtz6/vcLx
Unseal Key 3: +/GXkOC2W9Ne+SEywnBJWStT7uwUXzAJFhpOJIhksdVt
Unseal Key 4: uhHsX82gzcJovLCnsYxj099uMvZK1u67hoXHuKePqiEN
Unseal Key 5: N4wBz1BEG4NhPtho5MDusyTIwGK3RbgfBWajvEeJjXZN

Initial Root Token: s.qiz9McA66XL2U0YAc5FXqL0M

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated master key. Without at least 3 keys to
reconstruct the master key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```

Next we need to **unseal** the vault:

```bash
> kubectl exec --stdin=true --tty=true vault-0 -- vault operator unseal
Unseal Key (will be hidden):
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    1/3
Unseal Nonce       c6fef280-a3c5-1d6f-f89f-48a097a13f0f
Version            1.8.2
Storage Type       file
HA Enabled         false
> kubectl exec --stdin=true --tty=true vault-0 -- vault operator unseal
Unseal Key (will be hidden):
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    2/3
Unseal Nonce       c6fef280-a3c5-1d6f-f89f-48a097a13f0f
Version            1.8.2
Storage Type       file
HA Enabled         false
> kubectl exec --stdin=true --tty=true vault-0 -- vault operator unseal
Unseal Key (will be hidden):
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         1.8.2
Storage Type    file
Cluster Name    vault-cluster-2ba9762b
Cluster ID      4d5e7c9e-356c-38f1-34e6-6ba813ada808
HA Enabled      false
```

After that all the pods should be in a **READY** state:

```bash
> kubectl get pods -l app=vault
NAME      READY   STATUS    RESTARTS   AGE
vault-0   1/1     Running   0          33m
```

### Creating a secret in vault

First we have to authenticate with the root token, which was provided when we unsealed the vault:

```bash
> kubectl exec -it vault-0 -- /bin/sh
/ $ vault login
Token (will be hidden):
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                s.qiz9McA66XL2U0YAc5FXqL0M
token_accessor       6LJVwnIE5W0WhJxrp2bLrm6M
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

Now let's enable the kv engine:

```bash
/ $ vault secrets enable -path=secret kv-v2
Success! Enabled the kv-v2 secrets engine at: secret/
```

Now let's create a simple secret:

```bash
vault kv put secret/app-pass password="coolio"
```

Now let's confirm it's set:

```bash
/ $ vault kv get secret/app-pass
====== Metadata ======
Key              Value
---              -----
created_time     2021-09-29T17:57:33.485749067Z
deletion_time    n/a
destroyed        false
version          1

====== Data ======
Key         Value
---         -----
password    coolio
```

Not too shabby :)
## Exposing Secrets to Pods
There are a couple of ways of accomplishing this. The first one is using the vault agent. Basically you have a side car container running next to your application container and it takes care of presenting the secret to the application container. From [Vault Agent with Kubernetes](vault-agent-arch.png) here is a nice overview:

![vault-agent-arch.png](https://res.cloudinary.com/elatov/image/upload/v1632942009/blog-pics/k8s-vault/vault-agent-arch.png)

We can also use the CSI provider and the guide is at [Mount Vault Secrets through Container Storage Interface (CSI) Volume](https://learn.hashicorp.com/tutorials/vault/kubernetes-secret-store-driver). Also here is a nice diagram from [Retrieve HashiCorp Vault Secrets with Kubernetes CSI](https://www.hashicorp.com/blog/retrieve-hashicorp-vault-secrets-with-kubernetes-csi):


![vault-csi-arch.png](https://res.cloudinary.com/elatov/image/upload/v1632942012/blog-pics/k8s-vault/vault-csi-arch.png)

And lasty we can call the API directly using client libraries (Nice example with python is seen at [Securing secrets with python and vault](https://modularsystems.io/blog/securing-secrets-python-vault/))

### Vault CSI Driver in K8S

Let's try to use the CSI driver to get a secret into a pod, steps are covered [Mount Vault Secrets through Container Storage Interface (CSI) Volume](https://learn.hashicorp.com/tutorials/vault/kubernetes-secret-store-driver). First we need to install the necessary system components into K8S, we can do that by using `helm` to generate the templates:

```bash
helm template vault hashicorp/vault --set "injector.enabled=false" \
  --set "csi.enabled=true"
```

And then to apply your custom configs with `kustomize`:

```bash
> k apply -k base
serviceaccount/vault-csi-provider created
clusterrole.rbac.authorization.k8s.io/vault-csi-provider-clusterrole created
clusterrolebinding.rbac.authorization.k8s.io/vault-csi-provider-clusterrolebinding created
daemonset.apps/vault-csi-provider created
```

At this point you should see your **daemonset** deploy all the pods across all the nodes:

```bash
> k get pods -l app=vault-csi
NAME                       READY   STATUS    RESTARTS   AGE
vault-csi-provider-5dtd9   1/1     Running   0          92s
vault-csi-provider-cfvb8   1/1     Running   0          92s
vault-csi-provider-sdn7r   1/1     Running   0          92s
```

Now to install the CSI driver (this is covered in [The Secrets Store CSI Driver Book](https://secrets-store-csi-driver.sigs.k8s.io/getting-started/installation.html)):

```
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm template secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system
```

And here are the resources deployed:

```bash
> k apply -k base
customresourcedefinition.apiextensions.k8s.io/secretproviderclasses.secrets-store.csi.x-k8s.io created
customresourcedefinition.apiextensions.k8s.io/secretproviderclasspodstatuses.secrets-store.csi.x-k8s.io created
serviceaccount/secrets-store-csi-driver created
clusterrole.rbac.authorization.k8s.io/secretproviderclasses-role created
clusterrolebinding.rbac.authorization.k8s.io/secretproviderclasses-rolebinding created
daemonset.apps/secrets-store-csi-driver created
csidriver.storage.k8s.io/secrets-store.csi.k8s.io created
```

Let's make sure they are running:

```bash
> k get pods -n kube-system -l app=secrets-store-csi-driver
NAME                             READY   STATUS    RESTARTS   AGE
secrets-store-csi-driver-2rzqq   3/3     Running   0          3m8s
secrets-store-csi-driver-ns42p   3/3     Running   0          3m8s
secrets-store-csi-driver-zdhb8   3/3     Running   0          3m8s
```

Now that we have the system components deployed, let's move on to the next steps.

### Enable K8S Authentication
Vault has integration with K8S authentication, all we need to do is point to the k8s token and the CA:

```bash
> kubectl exec -it vault-0 -- /bin/sh
/ $ vault auth enable kubernetes
Success! Enabled kubernetes auth method at: kubernetes/
/ $ vault write auth/kubernetes/config \
>     issuer="https://kubernetes.default.svc.cluster.local" \
>     token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
>     kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
>     kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
Success! Data written to: auth/kubernetes/config
```

Next we need to create a policy to all to read the secret and also assign that policy to a Kubernetes service account, so that a pod running as that service account can read that secret:

```bash
/ $ vault policy write internal-app - <<EOF
> path "secret/data/app-pass" {
>   capabilities = ["read"]
> }
> EOF
Success! Uploaded policy: internal-app
/ $ vault write auth/kubernetes/role/app \
>     bound_service_account_names=app-sa \
>     bound_service_account_namespaces=default \
>     policies=internal-app \
>     ttl=20m
Success! Data written to: auth/kubernetes/role/app
```

Now we have to create a CSI configuration to link the vault secret to the K8S secret:

```bash
cat > spc-vault-app.yaml <<EOF
apiVersion: secrets-store.csi.x-k8s.io/v1alpha1
kind: SecretProviderClass
metadata:
  name: vault-app
spec:
  provider: vault
  parameters:
    vaultAddress: "http://vault.default:8200"
    roleName: "app"
    objects: |
      - objectName: "app-password"
        secretPath: "secret/data/app-pass"
        secretKey: "password"
EOF
> k apply -f spc-vault-app.yaml
secretproviderclass.secrets-store.csi.x-k8s.io/vault-app created
```

Now onto the latest steps.

### Create a Pod with the Secret Mounted
First let's create the service account that we allowed read capablity to our vault secret:

```bash
> kubectl create serviceaccount app-sa
serviceaccount/app-sa created
```

Then for the pod manifest which runs as our service account and mounts the secret:

```bash
cat > app-pod.yaml <<EOF
kind: Pod
apiVersion: v1
metadata:
  name: app
spec:
  serviceAccountName: app-sa
  containers:
  - image: busybox
    name: webapp
    command: ["/bin/sh"]
    args: ["-c", "while true; do sleep 300;done"]
    volumeMounts:
    - name: secrets-store-inline
      mountPath: "/mnt/secrets-store"
      readOnly: true
  volumes:
    - name: secrets-store-inline
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: "vault-app"
EOF
> k apply -f app-pod.yaml
pod/app created
```

And now for the final test:

```bash
> k exec -it app -- cat /mnt/secrets-store/app-password
coolio
```

Phew, I am glad that worked out.
