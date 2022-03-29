---
published: true
layout: post
title: "Deploying AWX in Kubernetes with AWX Operator"
author: Karim Elatov
categories: [automation, devops, containers]
tags: [awx, ansible, kubernetes]
---

A while back I deployed AWX to run ansible playbooks (this is covered in [Setting Up and Using AWX with docker-compose](/2018/12/setting-up-and-using-awx-with-docker-compose/)). I wanted to refresh that configuration since the deployment model has switched.

## Deploy PostgreSQL in K8S
I recently deployed OpenEBS to allow creation of Persistent Volumes that have decent performance (this setup is covered in [Using cStor from OpenEBS](/2021/12/using-cstor-from-openebs/)). Using that as my storage backend I deployed a postgres deployment in kubernetes with persistent storage:

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

Then I followed similar instructions as in my [previous post](/2018/12/setting-up-and-using-awx-with-docker-compose/) to configure the [project](https://docs.ansible.com/ansible-tower/latest/html/userguide/projects.html), [templates](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html), and [credentials](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html). There are also other sites that cover the process pretty well:

- [Install Ansible AWX on CentOS 8 / Rocky Linux 8](https://computingforgeeks.com/install-and-configure-ansible-awx-on-centos/)
- [Getting started Ansible AWX tower for IT automation run first playbook](http://vcloud-lab.com/entries/devops/getting-started-ansible-awx-tower-for-it-automation-run-first-playbook)

### Adding Custom Roles and Collections
There have been changes on how to include custom collections and role into your ansible playbooks in awx. These pages covers the setup:

- [Ansible best practices: using project-local collections and roles](https://www.jeffgeerling.com/blog/2020/ansible-best-practices-using-project-local-collections-and-roles)
- [Collections](https://github.com/ansible/awx/blob/devel/docs/collections.md)

So I just ended up creating the following in my git repo:

```bash
> cat collections/requirements.yml 
collections:
  - name: community.crypto
  - name: community.general
  - name: community.hashi_vault
  - name: ansible.posix
> cat roles/requirements.yml      
roles:
  - name: robertdebock.epel
```

Then after doing a project sync, my playbooks were able to use all the necessary collections.

## Creating a Custom AWX_EE Image
I was using a hashicorp vault to populate some of the variables and that kept failing since the `hvac` python module is not included in the default EE image. I ran into the [following issue](https://github.com/ansible/awx-operator/issues/588) and it looks like the way to handle that is to create a custom EE image and to include the module there. I ran into a couple of sites that described the process:

- [Building Kubernetes-enabled Tower/AWX Execution Environments Using AWX-EE and ansible-builder](https://thinkingoutcloud.org/2021/12/07/building-kubernetes-enabled-tower-awx-execution-environments-using-awx-ee-and-ansible-builder/)
- [Execution Environments](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html)
- [Creating a custom EE for AWX](https://www.linkedin.com/pulse/creating-custom-ee-awx-phil-griffiths)

First let's get the prereqs:

```bash
> pip install --user ansible-builder
> git clone git@github.com:elatov/awx-ee.git
> cd awx-ee
```

I ended up with the following configs:

```bash
> cat execution-environment.yml 
---
version: 1
dependencies:
  galaxy: _build/requirements.yml
  python: _build/requirements.txt
  system: _build/bindep.txt
build_arg_defaults:
  EE_BASE_IMAGE: 'quay.io/ansible/ansible-runner:stable-2.11-latest'
additional_build_steps:
  append:
    - RUN alternatives --set python /usr/bin/python3
    - COPY --from=quay.io/project-receptor/receptor:latest /usr/bin/receptor /usr/bin/receptor
    - RUN mkdir -p /var/run/receptor
    - ADD run.sh /run.sh
    - CMD /run.sh
    - USER 1000
    - RUN git lfs install
```

And here is the file where you can add your custom python modules:

```bash
> cat _build/requirements.txt 
hvac
```
I ended up customizing the base image and this was to ensure a development version is not included in the image. This is actually discussed in [this issue](https://github.com/ansible/awx-ee/issues/72). To build the image, you can run the following:

```bash
ansible-builder build --tag elatov/awx-custom-ee:0.0.4
```

For the tag specify your container registry. You can then test the image locally really quick:

```bash
> docker run --user 0 --entrypoint /bin/bash -it --rm elatov/awx-custom-ee:0.0.4  
bash-4.4# git clone git@github.com:elatov/ansible-tower-samples.git
bash-4.4# cd ansible-tower-samples
bash-4.4# ansible-playbook -vvv hello_world.yml
```

If everything is working as expected then push the image to your registry:

```bash
> docker push elatov/awx-custom-ee:0.0.4
```

At this point you can either modify the [awx-operator](https://github.com/ansible/awx-operator) config and add the following section:

```bash
---
spec:
  ...
  ee_images:
    - name: custom-awx-ee
      image: elatov/awx-custom-ee:0.0.4
```

Or you can just add the image manually in the UI as per the instructions in [Use an execution environment in jobs](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-ee-in-jobs).

### Adding Mitogen in the Custom AWX_EE Image
While I was creating a custom image, I decided to include [mitogen](https://github.com/mitogen-hq/mitogen/blob/master/docs/ansible_detailed.rst) in it. [This](https://www.reddit.com/r/ansible/comments/k5ur3n/mitogen_strategy_plugin_with_awxtower_question/) made me think it's possible. So I modified the `ansible-builder` config to have the following:

```bash
> cat execution-environment.yml 
---
version: 1
dependencies:
  galaxy: _build/requirements.yml
  python: _build/requirements.txt
  system: _build/bindep.txt
build_arg_defaults:
  EE_BASE_IMAGE: 'quay.io/ansible/ansible-runner:stable-2.11-latest'
additional_build_steps:
  append:
    - RUN alternatives --set python /usr/bin/python3
    - COPY --from=quay.io/project-receptor/receptor:latest /usr/bin/receptor /usr/bin/receptor
    - RUN mkdir -p /var/run/receptor
    - RUN mkdir -p /usr/local/mitogen
    - COPY mitogen-0.3.2 /usr/local/mitogen/
    - ENV ANSIBLE_STRATEGY_PLUGINS=/usr/local/mitogen/ansible_mitogen/plugins/strategy
    - ENV ANSIBLE_STRATEGY=mitogen_linear
    - ADD run.sh /run.sh
    - CMD /run.sh
    - USER 1000
    - RUN git lfs install
```

Initially I tried to specify the `mitogen` configs in the `ansible.cfg` file as described in [Custom Volume and Volume Mount Options](https://github.com/ansible/awx-operator#custom-volume-and-volume-mount-options). But that broke the sync at the project level. The image used for the project syncing is different than the image used for the playbook runs. You can actually modify that as well as described [here](https://github.com/ansible/awx-ee/issues/72#issuecomment-965531641), you basically specify the following in your `awx-operator` config:

```bash
---
spec:
  ...
  control_plane_ee_image: elatov/awx-custom-ee:0.0.4
```

For some reason I didn't want to mess with that yet, in case I do an update I would want it to use the default image. Then I decided to modify my custom ee image build and set the environment variable at image level it self (as you see above), and that worked out great

#### Random mitogen notes

I was getting a weird issue where when `mitogen` was used, the playbook would fail to find the right collection. I then ran into [this page](https://github.com/mitogen-hq/mitogen/issues/794) and it helped out. Basically if I ran the playbook just by itself it worked, but if I ran multiple playbooks then it would fail. So I enabled debug mode on the working and and non-working one and I checked out the differences:

```bash
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
```
It turned out I had a custom `collections/ansible_collection` folder in my github repo. Notice how the working one was getting the collection directly from the project (**/runner/project/collections/**), while the working one was getting it from the location where `requirements.yml` is installed in (**/runner/requirements_collections/**). So I removed that from my git repo and then it started working. Also wanted to share the execution times of the playbooks in awx:

![awx-with-mitogen-improving.png](https://res.cloudinary.com/elatov/image/upload/v1644081199/blog-pics/awx-operator-setup/awx-with-mitogen-improving.png)

The very first one about **40 minutes**, then after caching all the facts it was at **13 minutes** and lastly with `mitogen` enabled it's at **3 minutes** :)
