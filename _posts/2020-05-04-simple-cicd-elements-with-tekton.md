---
published: true
layout: post
title: "Simple CI/CD Elements with Tekton"
author: Karim Elatov
categories: [devops]
tags: [tekton]
---
## Tekton Pipelines
[Tekton](https://github.com/tektoncd/pipeline), well from their page, is:

> Tekton is a Kubernetes-native, continuous integration and delivery (CI/CD) framework that enables you to create containerized, composable, and configurable workloads declaratively through CRDs.

As I ran into the project I decided to give it a quick test.

### Installing Tekton Pipelines
The install process is covered in [Installing Tekton Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/install.md) and it's actually pretty easy, you can just run the following:

```bash
k apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

After the install is done you will have a new namespace called `tekton-pipelines` and you can check out the [pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) that are deployed there:

```bash
> k get pods -n tekton-pipelines
NAME                                           READY   STATUS    RESTARTS   AGE
tekton-pipelines-controller-57c7799c8b-6t4r2   1/1     Running   0          23h
tekton-pipelines-webhook-6fc8499666-tmhm8      1/1     Running   0          23h
```

If you need to save output artifacts don't forget to create the necessary configuration and that's covered in [Configuring artifact storage](https://github.com/tektoncd/pipeline/blob/master/docs/install.md#configuring-artifact-storage). You can also customize the install by creating a [configmap](https://kubernetes.io/docs/concepts/configuration/configmap/) and the instructions for that are covered in [Customizing basic execution parameters](https://github.com/tektoncd/pipeline/blob/master/docs/install.md#customizing-basic-execution-parameters). I just wanted a simple configuration so I left the defaults. 

### Running a Simple Task with TaskRun
With **tekton** we have a couple of new resources/entities that are introduced and they are covered in the documentation:

* [Tasks](https://github.com/tektoncd/pipeline/blob/master/docs/tasks.md)
	* > A Task is a collection of Steps that you define and arrange in a specific order of execution as part of your continuous integration flow. A Task executes as a Pod on your Kubernetes cluster. A Task is available within a specific namespace, while a ClusterTask is available across the entire cluster. 
	* There is a nice example of building a docker image in [Building and pushing a Docker image](https://github.com/tektoncd/pipeline/blob/master/docs/tasks.md#building-and-pushing-a-docker-image)
* [TaskRuns](https://github.com/tektoncd/pipeline/blob/master/docs/taskruns.md)
	* > A TaskRun allows you to instantiate and execute a Task on-cluster.
	* Nice examples: [TaskRun with a referenced Task](https://github.com/tektoncd/pipeline/blob/master/docs/taskruns.md#example-taskrun-with-a-referenced-task) and [TaskRun with an embedded Task](https://github.com/tektoncd/pipeline/blob/master/docs/taskruns.md#example-taskrun-with-a-referenced-task)
* [Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/pipelines.md)
	* > A Pipeline is a collection of Tasks that you define and arrange in a specific order of execution as part of your continuous integration flow. Each Task in a Pipeline executes as a Pod on your Kubernetes cluster. You can configure various execution conditions to fit your business needs.
	* Nice example is at [Configuring the Task execution order](https://github.com/tektoncd/pipeline/blob/master/docs/pipelines.md#configuring-the-task-execution-order)
* [PipelineRuns](https://github.com/tektoncd/pipeline/blob/master/docs/pipelineruns.md)
	
	* > A PipelineRun allows you to instantiate and execute a Pipeline on-cluster. A PipelineRun automatically creates corresponding TaskRuns for every Task in your Pipeline. 

As a simple exampe let's run a simple task as described in [Tekton Pipelines Tutorial](https://github.com/tektoncd/pipeline/blob/master/docs/tutorial.md). First let's create a **task** to just `echo` out a message:

```yaml
> cat task.yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: echo-hello-world
spec:
  steps:
    - name: echo
      image: ubuntu
      command:
        - echo
      args:
        - "Hello World"
```

Then we can apply it:

```bash
> k apply -f task.yaml
```

You can of course check all the `tasks`:

```bash
> k get tasks
NAME               AGE
echo-hello-world   24h
```

You can also download the *cli* and get more info:

```bash
> curl -LO https://github.com/tektoncd/cli/releases/download/v0.9.0/tkn_0.9.0_Linux_x86_64.tar.gz
> tar xvzf tkn_0.9.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn
```

Then we can run the following to see the task:

```bash
> tkn t list
NAME               DESCRIPTION   AGE
echo-hello-world                 1 day ago
```

Then you can create a `taskrun` to execute the defined `task`:

```yaml
> cat taskrun.yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: echo-hello-world-task-run
spec:
  taskRef:
    name: echo-hello-world
```

Now let's run it:

```bash
> k apply -f taskrun.yaml
```

After it's done you will see the `task` status:

```bash
> tkn t describe  echo-hello-world
Name:        echo-hello-world
Namespace:   default

📨 Input Resources
 No input resources
📡 Output Resources
 No output resources
⚓ Params
 No params
🦶 Steps
 ∙ echo
🗂  Taskruns
NAME                        STARTED     DURATION     STATUS
echo-hello-world-task-run   1 day ago   16 seconds   Succeeded
```

You can also check out the logs:

```bash
> tkn t logs  echo-hello-world
[echo] Hello World
```

You can check out the same with the `taskrun`:

```bash
> tkn tr describe echo-hello-world-task-run
Name:        echo-hello-world-task-run
Namespace:   default
Task Ref:    echo-hello-world
Timeout:     1h0m0s
Labels:
 app.kubernetes.io/managed-by=tekton-pipelines
 tekton.dev/task=echo-hello-world
🌡️  Status
STARTED     DURATION     STATUS
1 day ago   16 seconds   Succeeded
📨 Input Resources
 No input resources
📡 Output Resources
 No output resources
⚓ Params
 No params
🦶 Steps
 NAME     STATUS
 ∙ echo   ---
🚗 Sidecars
No sidecars
```

and the logs as well:

```bash
> tkn tr logs  echo-hello-world-task-run
[echo] Hello World
```

I won't get into **pipelines** in this post but maybe later.

## Tekton Triggers
There is actually another project within the **tekton** umbrella: [Tekton Triggers](https://github.com/tektoncd/triggers). From that page:

> Triggers is a Kubernetes Custom Resource Definition (CRD) controller that allows you to extract information from events payloads (a "trigger") to create Kubernetes resources.

And this consists of 3 more new constructs:

* [EventListener](https://github.com/tektoncd/triggers/blob/master/docs/eventlisteners.md)
	* > EventListener is a Kubernetes custom resource that allows users a declarative way to process incoming HTTP based events with JSON payloads. EventListeners expose an addressable "Sink" to which incoming events are directed.
	  >
	  > Triggers within an `EventListener` can optionally specify **interceptors**, to modify the behavior or payload of Triggers.
	* For now the following **interceptors** are supported: [Webhook Interceptors](https://github.com/tektoncd/triggers/blob/master/docs/eventlisteners.md#Webhook-Interceptors), [GitHub Interceptors](https://github.com/tektoncd/triggers/blob/master/docs/eventlisteners.md#GitHub-Interceptors), [GitLab Interceptors](https://github.com/tektoncd/triggers/blob/master/docs/eventlisteners.md#GitLab-Interceptors), [CEL Interceptors](https://github.com/tektoncd/triggers/blob/master/docs/eventlisteners.md#CEL-Interceptors)
	
* [TriggerBindings](https://github.com/tektoncd/triggers/blob/master/docs/triggerbindings.md)
	* > TriggerBindings enable you to capture fields from an event and store them as parameters.
	* Nice example is seen in [Multiple Bindings](https://github.com/tektoncd/triggers/blob/master/docs/triggerbindings.md#multiple-bindings)
* [TriggerTemplates](https://github.com/tektoncd/triggers/blob/master/docs/triggertemplates.md)
	* > A TriggerTemplate is a resource that can template resources. TriggerTemplates have parameters that can be substituted anywhere within the resource template.
	  >
	  > Similar to [Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/pipelines.md),`TriggerTemplate`s do not do any actual work, but instead act as the blueprint for what resources should be created.

So let's give them a shot.

### Installing Tekton Triggers
Very similar to the **Tekton Pipelines** install we can run the following to install them (covered in [Installing Tekton Triggers](https://github.com/tektoncd/triggers/blob/master/docs/install.md)):

```bash
> k apply -f https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
```

And now you will see more pods:

```bash
> k get pods -n tekton-pipelines
NAME                                           READY   STATUS    RESTARTS   AGE
tekton-pipelines-controller-57c7799c8b-6t4r2   1/1     Running   0          23h
tekton-pipelines-webhook-6fc8499666-tmhm8      1/1     Running   0          23h
tekton-triggers-controller-697c9b844d-rdzx8    1/1     Running   0          4h58m
tekton-triggers-webhook-6bcb96f965-fx2n5       1/1     Running   0          4h58m
```

Now let's create a simple trigger to print out the parameters that are **POST**'ed to it.

### Create a Tekton Trigger to Print Sent Parameters 
First let's create an **eventlistener**:

```yaml
> cat eventlistener.yaml
apiVersion: triggers.tekton.dev/v1alpha1
kind: EventListener
metadata:
  name: listener
spec:
  triggers:
    - name: foo-trig
      bindings:
        - name: pipeline-binding
      template:
        name: pipeline-template
```

Let's apply it:

```bash
k apply -f eventlistener.yaml
```

You can check the status of it with the `tkn` cli:

```bash
> tkn eventlistener describe listener
Name:                      listener
Namespace:                 default
URL:                       http://el-listener.default.svc.cluster.local:8080
EventListnerServiceName:   el-listener

EventListenerTriggers
 NAME
 ∙ foo-trig
 BINDING NAME         KIND             APIVERSION
 ∙ pipeline-binding   TriggerBinding
 TEMPLATE NAME         APIVERSION
 ∙ pipeline-template
```

Now let's create a **pipeline** binding to just save the whole body and different parts that are **POST**'ed:

```yaml
> cat triggerbinding.yaml
apiVersion: triggers.tekton.dev/v1alpha1
kind: TriggerBinding
metadata:
  name: pipeline-binding
spec:
  params:
  - name: body
    value: $(body)
  - name: title
    value: $(body.title)
  - name: link
    value: $(body.link)
  - name: contenttype
    value: $(header.Content-Type)
```

Now let's apply that:

```bash
> k apply -f triggerbinding.yaml
```

And lastly let's create a **triggertemplate** to run a **task** to print those out:

```yaml
> cat triggertemplate.yaml
apiVersion: triggers.tekton.dev/v1alpha1
kind: TriggerTemplate
metadata:
  name: pipeline-template
spec:
  params:
  - name: title
    description: "Title"
    default: "test"
  - name: body
    description: "Body of Mesg (For testing)"
    default: "Test body"
  - name: link
    description: "Link of Mesg"
    default: "http://who.com"
  - name: contenttype
    description: "Headers of event"
    default: "json"
  resourcetemplates:
    - apiVersion: tekton.dev/v1alpha1
      kind: TaskRun
      metadata:
        generateName: task-run-
      spec:
        taskSpec:
          steps:
            - image: ubuntu
              script: |
                #! /bin/bash
                echo $(params.body)
                echo $(params.title)
                echo $(params.link)
                echo $(params.contenttype)
```

And let's apply it:

```bash
k apply -f triggertemplate.yaml
```

Now from the above output we can see that the internal service that has been exposed is called `el-listener`, here is more information about it:

```bash
> k get svc -l eventlistener=listener
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
el-listener   ClusterIP   10.105.11.172   <none>        8080/TCP   6h42m
```

By default it's of type [ClusterIP](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) and there are instructions on how to expose it externally with an [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) (it's covered in [Exposing EventListeners Externally](https://github.com/tektoncd/triggers/blob/master/docs/exposing-eventlisteners.md)), but I skipped that since I didn't need it available externally. So then I **POST**'ed to my **listener**:

```bash
> curl -X POST -d '{"title":"test","link":"http://f"}' 10.105.11.172:8080
{"eventListener":"listener","namespace":"default","eventID":"cgzzc"}
```

Then checking out the **taskruns**, I saw more:

```bash
> tkn taskruns list
NAME                        STARTED          DURATION     STATUS
task-run-8c9wc              39 seconds ago   5 seconds    Succeeded
echo-hello-world-task-run   1 day ago        16 seconds   Succeeded
```

Checking out the logs I saw the following:

```bash
> tkn taskruns logs task-run-8c9wc
[unnamed-0] link:http://f title:test
[unnamed-0] test
[unnamed-0] http://f
[unnamed-0] application/x-www-form-urlencoded
```

That was sweet. You can also check out the logs of the **tekton-pipelines-controller** for more information:

```bash
> k logs -n tekton-pipelines -f -l app=tekton-pipelines-controller
{"level":"info","logger":"tekton.taskrun-controller","caller":"taskrun/taskrun.go:314","msg":"Cloud Events: []","commit":"ab391e7","knative.dev/controller":"taskrun-controller"}
{"level":"info","logger":"tekton.taskrun-controller","caller":"taskrun/taskrun.go:403","msg":"Successfully reconciled taskrun task-run-ztbdg/default with status: &apis.Condition{Type:\"Succeeded\", Status:\"True\", Severity:\"\", LastTransitionTime:apis.VolatileTime{Inner:v1.Time{Time:time.Time{wall:0xbfa4481dce3c8dcc, ext:93308434659041, loc:(*time.Location)(0x2eb33e0)}}}, Reason:\"Succeeded\", Message:\"All Steps have completed executing\"}","commit":"ab391e7","knative.dev/controller":"taskrun-controller"}
{"level":"info","logger":"tekton.taskrun-controller.event-broadcaster","caller":"record/event.go:274","msg":"Event(v1.ObjectReference{Kind:\"TaskRun\", Namespace:\"default\", Name:\"task-run-ztbdg\", UID:\"b9cd8b1a-e7c7-499d-b034-7bbef7ef6ff0\", APIVersion:\"tekton.dev/v1alpha1\", ResourceVersion:\"59559830\", FieldPath:\"\"}): type: 'Normal' reason: 'Succeeded' All Steps have completed executing","commit":"ab391e7","knative.dev/controller":"taskrun-controller"}
{"level":"info","logger":"tekton.taskrun-controller","caller":"controller/controller.go:403","msg":"Reconcile succeeded. Time taken: 12.66091ms.","commit":"ab391e7","knative.dev/controller":"taskrun-controller","knative.dev/traceid":"5ded1131-ca4e-4517-88ec-63fca78b03d2","knative.dev/key":"default/task-run-ztbdg"}
{"level":"info","logger":"tekton.taskrun-controller","caller":"taskrun/taskrun.go:115","msg":"taskrun done : task-run-ztbdg \n","commit":"ab391e7","knative.dev/controller":"taskrun-controller"}
{"level":"info","logger":"tekton.taskrun-controller","caller":"controller/controller.go:403","msg":"Reconcile succeeded. Time taken: 5.56325ms.","commit":"ab391e7","knative.dev/controller":"taskrun-controller","knative.dev/traceid":"5e5f1b9b-4d8c-459b-8936-f8c7a9223d94","knative.dev/key":"default/task-run-ztbdg"}
```
