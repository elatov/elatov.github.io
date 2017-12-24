---
published: false
layout: post
title: "Update a Kubernetes Deployment"
author: Karim Elatov
categories: [containers]
tags: [kubernetes]
---
### Updating a kubernetes deployment

Most of the instructions are here: [Updating a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment). Also looking over:

* [Kubernetes - Rolling updates with deployment](https://tachingchen.com/blog/Kubernetes-Rolling-Update-with-Deployment/)
* [Deploying and Updating Apps with Kubernetes](http://freecontent.manning.com/deploying-and-updating-apps/)

It looks like there are multiple approaches to doing a rolling update. I will talk about 3 different methods:

* **kubectl replace** (pointing to a new yaml file)
	* If you specify **--force**, this would be a disruptive update and will destroy and re-create the resources([Disruptive updates](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#disruptive-updates)) 
	* Similar to **kubectl apply**, check out the above site for some of the differences and also the [Declarative Management of Kubernetes Objects Using Configuration Files](https://kubernetes.io/docs/tutorials/object-management-kubectl/declarative-object-management-configuration/) page.
* **kubectl set image** (pointing to a new image version)
* **kubectl edit** (similar to a first one, but you just update the YAML config in place)

I will use the second approach, as an example but I will probably use the second approach for future updates. With the **kubectl replace** approach the YAML will always be updated, in case I need to start from scratch or something (check out [Kubernetes Object Management](https://kubernetes.io/docs/tutorials/object-management-kubectl/object-management/#trade-offs) for some of the trade-offs between **Imperative commands** and **Imperative object configuration**). 

As a side note it looks like auto update of images in Pods (using the **latest** tag) is not recommended. This is discussed in [Force pods to re-pull an image without changing the image tag](https://github.com/kubernetes/kubernetes/issues/33664), using a specific version or SHA is the preffered method of specifying the **Image**.

#### ReplicaController Vs Deployment
With the new releases of **kubernetes** it's recommend to use **deployments** instead of **ReplicaControllers**. Nice overview between **ReplicaController** and **deployments**: [Rolling updates with Kubernetes: Replication Controllers vs Deployments](https://ryaneschinger.com/blog/rolling-updates-kubernetes-replication-controllers-vs-deployments/)

### Updating jenkins kubernetes deployment
So let's try this out. First let's set the new image:

	<> kubectl set image deployment/jenkins jenkins=jenkins/jenkins:2.73.3
	deployment "jenkins" image updated

Now you will see two **ReplicaSets**:

	<> kubectl get rs
	NAME                 DESIRED   CURRENT   READY     AGE
	jenkins-554f449b64   0         0         0         23h
	jenkins-f557b8866    1         1         1         21s

But only one pod and it will be with a new name:

	<> kubectl get pods
	NAME                      READY     STATUS    RESTARTS   AGE
	jenkins-f557b8866-jjhvr   1/1       Running   0          38s

You can also get a more verbose output:

	<> kubectl describe deployments
	Name:                   jenkins
	Namespace:              default
	CreationTimestamp:      Sat, 02 Dec 2017 19:10:15 -0700
	Labels:                 io.kompose.service=jenkins
	Annotations:            deployment.kubernetes.io/revision=2
	                        kompose.cmd=kompose convert
	                        kompose.version=1.4.0 (c7964e7)
	                        kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"extensions/v1beta1","kind":"Deployment","metadata":{"annotations":{"kompose.cmd":"kompose convert","kompose.version":"1.4.0 (c7964e7)"},...
	Selector:               io.kompose.service=jenkins
	Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
	StrategyType:           RollingUpdate
	MinReadySeconds:        0
	RollingUpdateStrategy:  1 max unavailable, 1 max surge
	Pod Template:
	  Labels:  io.kompose.service=jenkins
	  Containers:
	   jenkins:
	    Image:        jenkins/jenkins:2.73.3
	    Ports:        8080/TCP, 50000/TCP
	    Environment:  <none>
	    Mounts:
	      /var/jenkins_home from jenkins-home (rw)
	  Volumes:
	   jenkins-home:
	    Type:  HostPath (bare host directory volume)
	    Path:  /data/shared/jenkins/jenkins_home
	Conditions:
	  Type           Status  Reason
	  ----           ------  ------
	  Available      True    MinimumReplicasAvailable
	OldReplicaSets:  <none>
	NewReplicaSet:   jenkins-f557b8866 (1/1 replicas created)
	Events:
	  Type    Reason             Age   From                   Message
	  ----    ------             ----  ----                   -------
	  Normal  ScalingReplicaSet  1m    deployment-controller  Scaled up replica set jenkins-f557b8866 to 1
	  Normal  ScalingReplicaSet  1m    deployment-controller  Scaled down replica set jenkins-554f449b64 to 0

If you used **--record** during the initial deployment, you can see what changes are done to the deployment:

	<> kubectl rollout history deployment/jenkins
	deployments "jenkins"
	REVISION  CHANGE-CAUSE
	1         <none>
	2         kubectl apply --filename=jenkins-deployment.yaml --record=true

You should all see the following in the logs:

	<> kubectl logs --namespace=kube-system po/kube-controller-manager-ub
	I1217 22:59:01.066072       1 event.go:218] Event(v1.ObjectReference{Kind:"Deployment", Namespace:"default", Name:"jenkins", UID:"19efeaea-d7cf-11e7-a095-0c4de99d45d5", APIVersion:"extensions", ResourceVersion:"2571230", FieldPath:""}): type: 'Normal' reason: 'ScalingReplicaSet' Scaled up replica set jenkins-7899cc8d4 to 1
	I1217 22:59:01.070936       1 event.go:218] Event(v1.ObjectReference{Kind:"Deployment", Namespace:"default", Name:"jenkins", UID:"19efeaea-d7cf-11e7-a095-0c4de99d45d5", APIVersion:"extensions", ResourceVersion:"2571230", FieldPath:""}): type: 'Normal' reason: 'ScalingReplicaSet' Scaled down replica set jenkins-7484577686 to 0
	I1217 22:59:01.079696       1 event.go:218] Event(v1.ObjectReference{Kind:"ReplicaSet", Namespace:"default", Name:"jenkins-7484577686", UID:"902e2fe2-db9c-11e7-babd-0c4de99d45d5", APIVersion:"extensions", ResourceVersion:"2571234", FieldPath:""}): type: 'Normal' reason: 'SuccessfulDelete' Deleted pod: jenkins-7484577686-7bkrp
	I1217 22:59:01.079731       1 event.go:218] Event(v1.ObjectReference{Kind:"ReplicaSet", Namespace:"default", Name:"jenkins-7899cc8d4", UID:"df0c50f5-e37d-11e7-81ea-0c4de99d45d5", APIVersion:"extensions", ResourceVersion:"2571231", FieldPath:""}): type: 'Normal' reason: 'SuccessfulCreate' Created pod: jenkins-7899cc8d4-fpdhz

You can also run something like this to get each version of the **ReplicaSet**:

	<> for i in $(kubectl get rs --no-headers -o custom-columns=:.metadata.name); do echo $i; kubectl describe rs/$i| grep Image; done
	jenkins-5f7d7d8cf
	    Image:  jenkins/jenkins:2.73.3
	jenkins-7484577686
	    Image:  jenkins/jenkins:2.89.1
	jenkins-7899cc8d4
	    Image:  jenkins/jenkins:2.89.2

You can also use the **kubectl rollout history** to find out the same information:

	<> kubectl rollout history deployment/jenkins --revision=3
	deployments "jenkins" with revision #3
	Pod Template:
	  Labels:	io.kompose.service=jenkins
		pod-template-hash=193838479
	  Annotations:	kubernetes.io/change-cause=kubectl replace --filename=jenkins-deployment.yaml --record=true
	  Containers:
	   jenkins:
	    Image:	jenkins/jenkins:2.73.3
	    Ports:	8080/TCP, 50000/TCP
	    Environment:
	      JENKINS_OPTS:	--prefix=/jenkins
	    Mounts:
	      /var/jenkins_home from jenkins-home (rw)
	  Volumes:
	   jenkins-home:
	    Type:	HostPath (bare host directory volume)
	    Path:	/data/shared/jenkins/jenkins_home
	    HostPathType:
    	    
I also set the **revisionHistoryLimit** to **2** just to make sure I don't keep to many version of the applications:

	spec:
	  replicas: 1
	  strategy: {}
	  revisionHistoryLimit: 2
	  template:
	    metadata:
	      creationTimestamp: null
	      labels:
	        io.kompose.service: jenkins
	    spec:
	      containers:
	      - image: jenkins/jenkins:2.89.2
	        name: jenkins
