---
published: true
layout: post
title: "Random Updates for Tekton"
author: Karim Elatov
categories: [devops, automation]
tags: [kubernetes,tekton]
---

A while back [I installed Tekton](/2020/05/cert-manager-botkube-and-tektonpipelines-with-conditions/) and configured some [EventListeners](https://tekton.dev/docs/triggers/eventlisteners/) to trigger some [Pipelines](https://tekton.dev/docs/pipelines/pipelines/). I just left that configuration in place and it did it's job to update the deployments quite well. I was recently migrating some work loads to GKE and I decided to migrate my Tekton install (and in the process I decided to update it to the latest version). 

## Installing v0.26.0
At the time of writing that was the latest version. When I initially installed it a while back it was just one big manifest file, but now the install is split up into multiple parts:

```bash
# pipelines
curl https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml -o pipeline-release.yaml
# triggers
curl https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml -o trigger-release.yaml
# core interceptors like cel and github
curl https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml -o interceptors-release.yaml
k apply -f .
```

### Allowing webhook validation in private GKE clusters
After installing tekton, I couldn't make any updates, I would just receive the following error:

```bash
Internal error occurred: failed calling webhook "webhook.pipeline.tekton.dev": Post https://tekton-pipelines-webhook.tekton-pipelines.svc:443/defaulting?timeout=30s: dial tcp 10.14.8.18:8443: i/o timeout
```

After some digging around I ran into this [githhub issue](https://github.com/tektoncd/pipeline/issues/2932) which described my scenario. Basically when you have a private GKE cluster the master can't reach the validating webhook and you need to explicitly allow access. This is covered in the GKE documentation ([Adding firewall rules for specific use cases](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules)). Here is what I ran to open up the firewall:

```bash
gcloud compute firewall-rules create allow-webhook-from-gke-master \
    --action ALLOW \
    --direction INGRESS \
    --source-ranges 172.16.0.0/28 \
    --rules tcp:8443 \
    --target-tags gke-nodes
```

{% include note.html content="When I created the cluster I added the `gke-nodes` network tag. If you didn't do that, follow the instructions laid out in the google documentation on how to figure out the default network tags assigned to the GKE node pool." %}

After that the issue went away.

## Converting Conditions to When Expressions
Initially I used [conditions](https://tekton.dev/docs/pipelines/conditions/) to conditionally run certain tasks, but it looks like [when expression](https://tekton.dev/docs/pipelines/pipelines/#guard-task-execution-using-whenexpressions) are going to replace `conditions`. So before I would create a condition like this:

```bash
> cat condition.yaml 
apiVersion: tekton.dev/v1alpha1
kind: Condition
metadata:
  name: check-version-stable
spec:
  params:
    - name: new_version
      type: string
  check:
    image: ubuntu
    script: |
      #!/bin/bash
      PAT='(beta|rc|alpha)'
      if [[ ! $(params.new_version) =~ ${PAT} ]]; then
      	echo "version $(params.new_version) is stable 
      	exit 0
      else
      	echo "Build will be skipped since the version $(params.new_version) is unstable "
      	exit 1
      fi
```

And then in the task I could do something like this:

```yaml
  tasks:
    - name: print-info
      conditions:
      - conditionRef: check-version-stable
        params:
          - name: new_version
            value: "$(params.new_version)"
      taskRef:
        name: my-task
```

Now to accomplish the same, I took the example from [PipelineRun with WhenExpressions](https://github.com/tektoncd/pipeline/blob/main/examples/v1beta1/pipelineruns/pipelinerun-with-when-expressions.yaml) and first created a task which had an `output` of the result:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: check-version-stability
spec:
  params:
    - name: new_version
  results:
    - name: matches
      description: indicates whether the version is stable or not
  steps:
    - name: check-version
      image: ubuntu
      script: |
        #!/bin/bash
        PAT='(beta|rc|alpha)'
        # check
        if [[ ! $(params.new_version) =~ ${PAT} ]]; then
      	  printf yes | tee /tekton/results/matches
        else
      	  printf no | tee /tekton/results/matches
        fi
```

And then in the pipeline, I could use it like so:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: my-pipeline
spec:
  params:
    - name: new_version
      description: "new version of app"
  tasks:
    - name: check-version-stability
      taskRef:
        name: check-version-stability
      params:
      - name: new_version
        value: "$(params.new_version)"
    - name: update-app
      when:
      - input: "$(tasks.check-version-stability.results.matches)"
        operator: in
        values: ["yes"]
      taskRef:
        name: update-app-task
```

And I was able to accomplish the same thing.

## Other Small  Changes
Here are some other changes I had to make.

### New Syntax for TriggerTemplate Params
Before I would use `params.var` and I had t convert them to `tt.params.var`. This is the result of a new update: [Confusing params syntax in trigger templates](https://github.com/tektoncd/triggers/issues/508).  

### EventListener Escaping Quotes
I kept getting `couldn't unmarshal json: invalid character` in my `eventlistener` and it looks like if there a quote (or other special characters) in the **JSON** that is passed to the trigger it will not like it. This is discussed in:

* [Backslash quote in json will crash the trigger parser](https://github.com/tektoncd/triggers/issues/777)
* [v0.10.0: github $(body.head_commit.modified): couldn't unmarshal json: invalid character](https://github.com/tektoncd/triggers/issues/845)

I had to add the following annotation to my `eventlistener` to get around the issue: `triggers.tekton.dev/old-escape-quotes: "true"`.  I think I will have to update the `CEL Interceptor` to use [parseJSON()](https://tekton.dev/docs/triggers/cel_expressions/#list-of-extension-functions) to get the values.

### CEL Interceptor Formatting Changed
The `cel interceptor` format changed. Initially I had something like this:

```bash
      interceptors:
        - cel:
            filter: >- 
               (split(body.link,'/')[2] == 'github.com') && (split(body.link,'/')[7].startsWith('v'))
            overlays:
            - key: extensions.app_name
              expression: "split(body.link,'/')[4]"

```

And now it has it's own `params`:

```bash
      interceptors:
        - ref:
            name: "cel"
          params:
            - name: "filter"
              value: "(body.link.split('/')[2] == 'github.com') && (body.link.split('/')[7].startsWith('v'))"
            - name: "overlays"
              value:
                - key: app_name
                  expression: "body.link.split('/')[4]"
```

This was in the release notes a while back:

* [Cluster interceptor documentation doesn't demonstrate how to invoke existing interceptors in new formation](https://github.com/tektoncd/triggers/issues/1023)
* [Update examples to use both old and new syntax](https://github.com/tektoncd/triggers/pull/1028)

### TriggerBinding Params name change
The above change also forced me to remove the `body` prefix for the` params`, before I would have this in my `triggerbinding`:

```bash
apiVersion: triggers.tekton.dev/v1alpha1
kind: TriggerBinding
metadata:
  name: pipeline-binding
spec:
  params:
  - name: app_name
    value: $(body.extensions.app_name)

```

Then it became this:

```bash
apiVersion: triggers.tekton.dev/v1alpha1
kind: TriggerBinding
metadata:
  name: pipeline-binding
spec:
  params:
  - name: app_name
    value: $(extensions.app_name)
```

I only saw a similar change in this [old github fix](https://github.com/tektoncd/plumbing/pull/687/files). 

### Referencing TriggerBinding in EventListerner Change to be Ref
In the `eventlistener` before we would reference a `triggerbinding` by `name`, like so:

```yaml
      bindings:
        - name: pipeline-binding
      template:
        name: pipeline-template
```

Now we have to use `ref`, like so:

```yaml
      bindings:
        - ref: pipeline-binding
      template:
        ref: pipeline-template
```

This was discussed in:

* [Release v0.5.0 breaks event listeners with name instead of ref](https://github.com/tektoncd/triggers/issues/607).
* [One more breaking change for 0.5.0 release notes](https://github.com/tektoncd/triggers/issues/577)

This definitely made me realize how quick the project is moving and how easy it is to fall behind on all the updates :(