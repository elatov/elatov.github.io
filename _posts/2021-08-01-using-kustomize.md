---
published: true
layout: post
title: "Using Kustomize"
author: Karim Elatov
categories: [devops,automation,containers]
tags: [kubernetes,kustomize]
---
# Architecture
From [their site](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/) page:

> * Kustomize helps customizing config files in a template free way.
> * Kustomize provides a number of handy methods like generators to make customization easier.
> * Kustomize uses patches to introduce environment specific changes on an already existing standard config file without disturbing it.

It's a perfect tool to create environment based customizations to your k8s deployments. `kustomize` uses a concept of **bases** and **overlays**, where you define a base and then you create overlays which customize the configuration depending on your environment. There is a pretty cool diagram in [their github](https://github.com/kubernetes-sigs/kustomize):

![overlay.jpg](https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/docs/images/overlay.jpg)

And here is a simple directory hierarchy:

```bash
~/someApp
├── base
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── service.yaml
└── overlays
    ├── development
    │   ├── cpu_count.yaml
    │   ├── kustomization.yaml
    │   └── replica_count.yaml
    └── production
        ├── cpu_count.yaml
        ├── kustomization.yaml
        └── replica_count.yaml
```

It's also a perfect tool to be added into your CI/CD pipeline. From [Workflow for off the shelf applications](https://kubectl.docs.kubernetes.io/guides/config_management/offtheshelf/), here is a nice overview:

![ots.jpg](https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/docs/images/workflowOts.jpg)

So let's run through a couple of examples to see how it works. As a starting point, I created the following directory structure:

```bash
> mkdir -p {overlays/{dev,prod},base}
> touch {base/kustomization.yaml,overlays/{dev,prod}/kustomization.yaml}
> tree
.
├── base
│   └── kustomization.yaml
└── overlays
    ├── dev
    │   └── kustomization.yaml
    └── prod
        └── kustomization.yaml

4 directories, 3 files
```

## Container Images
First let's try out modifying the container image version (this example is covered in [images](https://kubectl.docs.kubernetes.io/references/kustomize/images/)). As an example let's create a simple deployment manifest:

```bash
> cat base/deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: the-deployment
  annotations:
    app: nginx
spec:
  template:
    spec:
      containers:
      - name: nginxapp
        image: nginx:1.7.9
```

And here is a simple `kustomization` to modify the tag:

```bash
> cat base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deploy.yaml

images:
- name: nginx
  newTag: 1.8.0
```

Now to see how it gets parsed, we can use `kubectl kustomize`:

```bash
> k kustomize base           
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    app: nginx
  name: the-deployment
spec:
  template:
    spec:
      containers:
      - image: nginx:1.8.0
        name: nginxapp
```

To actually apply it, we can run `kubectl apply -k` (vs `kubectl apply -f`):

```bash
k apply -k base
deployment.apps/the-deployment created
```

That was pretty easy.

## Patching
`kustomize` has two approaches to patching files: [strategic merge patch](https://kubectl.docs.kubernetes.io/references/kustomize/patchesstrategicmerge/) and [json 6902 patch](https://kubectl.docs.kubernetes.io/references/kustomize/patchesjson6902/).

### Strategic Merge Patch
This is useful if you are making a lot of changes, so you can just provide a YAML file that looks like a k8s manifest file with all the resources you want to add/change. From the [Patching multiple resources at once](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/patchMultipleObjects.md) example, let's inject a side car container into our deployment in our `dev` overlay. First let's add a `kustomization.yaml` file into the `dev` overlay:

```bash
> cat overlays/dev/kustomization.yaml 
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

patches:
- path: deploy-patch.yaml
```

And now let's add the `patch` file to specify the container we want to add:

```bash
> cat overlays/dev/deploy-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: the-deployment
spec:
  template:
    spec:
      containers:
        - name: istio-proxy
          image: docker.io/istio/proxyv2
          args:
          - proxy
          - sidecar
```

And here is how the parsed manifest will end up looking like:

```bash
> k kustomize overlays/dev           
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    app: nginx
  name: the-deployment
spec:
  template:
    spec:
      containers:
      - args:
        - proxy
        - sidecar
        image: docker.io/istio/proxyv2
        name: istio-proxy
      - image: nginx:1.8.0
        name: nginxapp
```

That looks good.

### JSON 6902 Patch
This is good for adding/modifying one field at a time (also the parent path has to exist, so it doesn't create sub fields, for more information check out [this github feature request](https://github.com/kubernetes-sigs/kustomize/issues/2986)). Let's say I want add a new `annotation` and to a `serviceaccount`, we could create the following patch:

```bash
> cat overlays/dev/deploy-more-patch.yaml
- op: add
  path: /metadata/annotations/app.io~1owner
  value: "me"
- op: add
  path: /spec/template/spec/serviceAccountName
  value: app
```

Notice that I had to use `~1` to specify a forward slash `/` (this is covered in this [github issue](https://github.com/kubernetes-sigs/kustomize/issues/1256)). And here is update `kustomization.yaml` to include the new patch file. Notice that I also added a target to specify which resource to modify:

```bash
> cat overlays/dev/kustomization.yaml 
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

patches:
- path: deploy-patch.yaml
- path: deploy-more-patch.yaml
  target:
    kind: Deployment
```

And now here is the resulted manifest:

```bash
> k kustomize overlays/dev                
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    app: nginx
    app.io/owner: me
  name: the-deployment
spec:
  template:
    spec:
      containers:
      - args:
        - proxy
        - sidecar
        image: docker.io/istio/proxyv2
        name: istio-proxy
      - image: nginx:1.8.0
        name: nginxapp
      serviceAccountName: app
```

yay, that worked out as well.

## ConfigGenerator
Let's cover one more example, the [configMapGenerator](https://kubectl.docs.kubernetes.io/references/kustomize/configmapgenerator/), this supports multiple approaches as well. I will cover two.

### Using Literals to Specify Configs as Strings
There is also a nice example at [ConfigMap generation and rolling updates](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/configGeneration.md). Let's say I create the following in my `base`:

```bash
> cat base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deploy.yaml

images:
- name: nginx
  newTag: 1.8.0

configMapGenerator:
- name: config
  literals:
    - common="Common Variable"
```

Now at the overlay `kustomization`:

```bash
> cat overlays/dev/kustomization.yaml 
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

patches:
- path: deploy-patch.yaml
- path: deploy-more-patch.yaml
  target:
    kind: Deployment

configMapGenerator:
- name: config
  behavior: merge
  literals:
    - custom="My Custom Config"
```

Now I can modify the the `deployment` in the base to add the `common` `configMap`:

```bash
> cat base/deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: the-deployment
  annotations:
    app: nginx
spec:
  template:
    spec:
      containers:
      - name: nginxapp
        image: nginx:1.7.9
        env:
        - name: COMMON
          valueFrom:
            configMapKeyRef:
              name: config
              key: common
```

And then I added a `patch` in the `overlay` to append the environment variable (since I my sidecar proxy patch from before added up adding the container first, I had to basically append it to the second container of my deployment... **0** is the first and **1** is the second):

```bash
> cat overlays/dev/deploy-more-patch.yaml 
- op: add
  path: /metadata/annotations/app.io~1owner
  value: "me"
- op: add
  path: /spec/template/spec/serviceAccountName
  value: app
- op: add
  path: /spec/template/spec/containers/1/env/-
  value:
      name: CUSTOM
      valueFrom:
        configMapKeyRef:
          name: config
          key: custom
```

Parsing the config, here is what it creates:

```bash
> k kustomize overlays/dev
apiVersion: v1
data:
  common: Common Variable
  custom: My Custom Config
kind: ConfigMap
metadata:
  name: config-k96cb96f75
---
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    app: nginx
    app.io/owner: me
  name: the-deployment
spec:
  template:
    spec:
      containers:
      - args:
        - proxy
        - sidecar
        image: docker.io/istio/proxyv2
        name: istio-proxy
      - env:
        - name: COMMON
          valueFrom:
            configMapKeyRef:
              key: common
              name: config-k96cb96f75
        - name: CUSTOM
          valueFrom:
            configMapKeyRef:
              key: custom
              name: config-k96cb96f75
        image: nginx:1.8.0
        name: nginxapp
      serviceAccountName: app
```

We can see it creates a dynamic `configMap` name and adds it to our container accordingly... that is pretty cool :)

### Using Files to Specify Configs
Another approach is to provide configuration files in the `configMaps`. Each file ends up being a new data entry in the `configMap`.  Another cool example at [Demo: combining config data from devops and developers](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/combineConfigs.md). Let's add it to our **prod** `overlay`. First let's modify our `base` and add a new `configMapGenerator`:

```bash
> cat base/kustomization.yaml 
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deploy.yaml

images:
- name: nginx
  newTag: 1.8.0

configMapGenerator:
- name: config
  literals:
    - common="Common Variable"
- name: file-config
  files:
    - common.properties
```

Now let's add it to our base`deployment` as a volume, so each entry is added as a file under the `config` directory:

```bash
> cat base/deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: the-deployment
  annotations:
    app: nginx
spec:
  template:
    spec:
      containers:
      - name: nginxapp
        image: nginx:1.7.9
        env:
        - name: COMMON
          valueFrom:
            configMapKeyRef:
              name: config
              key: common
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: config-volume
        configMap:
          name: file-config

```

Now in the `overlay`, let's add to our `configMapGenerator`:

```bash
> cat overlays/prod/kustomization.yaml 
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

configMapGenerator:
- name: file-config
  behavior: merge
  files:
  - custom.properties
```

And now generating the config here is how it looks like:

```bash
> k kustomize overlays/prod 
apiVersion: v1
data:
  common: Common Variable
kind: ConfigMap
metadata:
  name: config-mdd5k4b6c5
---
apiVersion: v1
data:
  common.properties: |-
    common=common_config
    other_common=common2_config
  custom.properties: |-
    custom1=custom1_config
    custom2=custom2_config
kind: ConfigMap
metadata:
  name: file-config-965d47772g
---
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    app: nginx
  name: the-deployment
spec:
  template:
    spec:
      containers:
      - env:
        - name: COMMON
          valueFrom:
            configMapKeyRef:
              key: common
              name: config-mdd5k4b6c5
        image: nginx:1.8.0
        name: nginxapp
        volumeMounts:
        - mountPath: /etc/config
          name: config-volume
      volumes:
      - configMap:
          name: file-config-965d47772g
        name: config-volume
```

Now the container can parse all the files specified under the `/etc/config` directory... all in all `kustomize` is pretty cool :) There are actually a lot more that it does, and this was just a quick overview of some of the functions.
