---
published: false
layout: post
title: "Deploying AWX in Kubernetes with AWX Operator"
author: Karim Elatov
categories: [automation, devops, containers]
tags: [awx, ansible, kubernetes]
---

A while back I deployed AWX to run ansible playbooks (this is covered in [Setting Up and Using AWX with docker-compose](/2018/12/setting-up-and-using-awx-with-docker-compose/)). I wanted to refresh that configuration since the deployment model has switched.

## Deploy PostgreSQL in K8S
I recently deployed OpenEBS to allow to create Persistent Volumes that has decent performance (this setup is covered in [Using cStor from OpenEBS](/2021/12/using-cstor-from-openebs/)). Using that as my storage backend I deployed a postgres deployment in kubernetes with persistent storage:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:11
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5432
          name: postgres
          protocol: TCP
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - mountPath: /var/lib/postgresql/data
          name: postgres-data-vol
      volumes:
      - name: postgres-data-vol
        persistentVolumeClaim:
          claimName: posgres-data-pvc
```

There are actually a nice of example of a postgres deployment in kubernetes:

- [How to use Kubernetes to deploy Postgres](https://www.sumologic.com/blog/kubernetes-deploy-postgres/)
- [Deploying PostgreSQL as a StatefulSet in Kubernetes](https://www.bmc.com/blogs/kubernetes-postgresql/)
- [How to Deploy PostgreSQL on Kubernetes](https://phoenixnap.com/kb/postgresql-kubernetes)

Mine was deployed and ready to go:

```bash
> k get all -l app=postgres
NAME                            READY   STATUS    RESTARTS   AGE
pod/postgres-868f4bdc9b-9d8r4   1/1     Running   0          4h50m

NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/postgres   ClusterIP   10.104.155.189   <none>        5432/TCP   3d4h

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/postgres-868f4bdc9b   1         1         1       3d4h
```

## Install the AWX Operator
Most of the setup is in the [readme](https://github.com/ansible/awx-operator/blob/devel/README.md). Here are the quick steps:

```bash
$ git clone https://github.com/ansible/awx-operator.git
$ cd awx-operator
$ export NAMESPACE=awx
$ make deploy
```

Make sure you have `make` and `kustomize` installed on the machine. After that runs, you should see the controller deployed:

```bash
$ kubectl get pods -n $NAMESPACE
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-66ccd8f997-rhd4z   2/2     Running   0          11s
```

## Deploy AWX 
I ended up creating the following configuration:

```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx
spec:
  service_type: ClusterIP
  postgres_configuration_secret: awx-postgres-configuration
  extra_volumes: |
    - name: ansible-cfg
      configMap:
        defaultMode: 420
        items:
          - key: ansible.cfg
            path: ansible.cfg
        name: awx-extra-config
  ee_extra_volume_mounts: |
    - name: ansible-cfg
      mountPath: /etc/ansible/ansible.cfg
      subPath: ansible.cfg
  # control_plane_ee_image: elatov/awx-custom-ee:0.0.2
  ee_images:
    - name: custom-awx-ee
      image: elatov/awx-custom-ee:0.0.4
```

You might not need the `ee_images` options, and I will cover those later. You can checkout the samples for the postgres config map at [External PostgreSQL Service](https://github.com/ansible/awx-operator/tree/devel#external-postgresql-service) and the extra volumes at [Custom Volume and Volume Mount Options](https://github.com/ansible/awx-operator/tree/devel#custom-volume-and-volume-mount-options). When I tried to create my AWX deployment, it would fail and the issue was with the fact that I didn't have a postgres db created, this is covered in [Need some assistance with AWX external postgresql db](https://www.reddit.com/r/ansible/comments/8pdr14/need_some_assistance_with_awx_external_postgresql/). Here are the commands to create the database and credentials:

```bash
> k exec -it $(k get pods -l app=postgres -o name) -- /bin/bash
bash-5.1# psql -h localhost -U postgres
psql (14.1)
Type "help" for help.

postgres=# CREATE USER awx WITH ENCRYPTED PASSWORD 'awxpass';
postgres=# CREATE DATABASE awx OWNER awx;
```

After that the deployment finished and I had an AWX instance deployed:

```bash
> k get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-9b6df9459-7p79d                                4/4     Running   0          2d5h
awx-operator-controller-manager-7f56f8b69c-fqqds   2/2     Running   0          2d5h
```
### Create a user manually for AWX Web UI
There is a [known issue](https://github.com/ansible/awx-operator/issues/123) where the default credentials don't work, even if you follow the instuctions to get the password:

```bash
$ k -n awx get secret awx-admin-password -o jsonpath="{.data.password}" | base64 -d
```

So I just created one manually:

```bash
> k exec -n awx -it $(k get pods -n awx -l app.kubernetes.io/component=awx -o name) -c awx-web -- /bin/bash
bash-4.4$ awx-manage createsuperuser
Username: test
Email address:
Password:
Password (again):
Superuser created successfully.
```

Then I followed similar instructions as in my [previous post](/2018/12/setting-up-and-using-awx-with-docker-compose/) to configure the project and templates. There are also other sides that cover the process pretty well:

- [Install Ansible AWX on CentOS 8 / Rocky Linux 8](https://computingforgeeks.com/install-and-configure-ansible-awx-on-centos/)
- [Getting started Ansible AWX tower for IT automation run first playbook(http://vcloud-lab.com/entries/devops/getting-started-ansible-awx-tower-for-it-automation-run-first-playbook)

### Adding Custom Roles and Collections

## Creating a Custom AWX_EE Image
### Adding Mitogen in the Custom AWX_EE Image

# this made me think it's possible
https://www.reddit.com/r/ansible/comments/k5ur3n/mitogen_strategy_plugin_with_awxtower_question/
https://github.com/ansible/awx-ee/issues/72
https://thinkingoutcloud.org/2021/12/07/building-kubernetes-enabled-tower-awx-execution-environments-using-awx-ee-and-ansible-builder/
https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html
https://www.linkedin.com/pulse/ansible-execution-environments-phil-griffiths
https://www.linkedin.com/pulse/creating-custom-ee-awx-phil-griffiths
# this gave me an idea to use env at the EE base image level
https://github.com/mitogen-hq/mitogen/issues/559
# you can also specify the version of the control plane ee image
https://github.com/ansible/awx-ee/issues/72#issuecomment-965531641
# first I tried the ansible.cfg approach
https://github.com/ansible/awx-operator#custom-volume-and-volume-mount-options
# but that broke my project sync from git
# same thing with the env approach
https://github.com/ansible/awx-operator#exporting-environment-variables-to-containers
#then I decided to modify my custom ee image build and set the environment variable at that level
And that worked out great
# I also specified the default ee custom image
https://github.com/ansible/awx-operator#deploying-a-specific-version-of-awx
# here is the progression in awx
awx-with-mitogen-improving.png
# I was getting a weird issue with mitogen failing to find the right collection
# This page helped out https://github.com/mitogen-hq/mitogen/issues/794
# it turned out I had a custom collections/ansible_collection in my github repo
checking out the diff between my runs I saw the following
> diff job_122.txt job_125.txt | head
1c1
< Identity added: /runner/artifacts/122/ssh_key_data (root@nb)
---
> Identity added: /runner/artifacts/125/ssh_key_data (root@nb)
93c93
< Loading collection ansible.posix from /runner/project/collections/ansible_collections/ansible/posix
---
> Loading collection ansible.posix from /runner/requirements_collections/ansible_collections/ansible/posix
104,357d103
< statically imported: /runner/project/roles/common/tasks/main-install.yaml

# notice how the working one was getting it from the project, while the working
# one was getting it from the location where requirements.yaml install in.
# So I removed that from my git repo and then it started working.