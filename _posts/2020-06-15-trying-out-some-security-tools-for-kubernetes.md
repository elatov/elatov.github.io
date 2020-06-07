---
published: true
layout: post
title: "Trying Out Some Security Tools for Kubernetes"
author: Karim Elatov
categories: [devops, containers]
tags: [tekton,snyk,trivy,falco]
---

Looking over the [CNCF landscape](https://landscape.cncf.io/) **Security & Compliance** section there are a bunch of tools out there:

![cncf-security-software.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/sec-tool-k8s/cncf-security-software.png)

So I decided to try out a few:

* [falco](https://falco.org/)
    * From [their page](https://falco.org/docs/):
      
      > Falco parses Linux system calls from the kernel at runtime, and asserts the stream against a powerful rules engine. 
* [trivy](https://github.com/aquasecurity/trivy)
    * From their [github page]():
      
      > A Simple and Comprehensive Vulnerability Scanner for Containers, Suitable for CI.
* [Snyk](https://snyk.io/)
    * They have a bunch of products, but I concentrated on the container vulnerabilities features. From [their page](https://snyk.io/product/container-vulnerability-management/):
      
      > Detecting vulnerabilities in containers and Kubernetes applications throughout the SDLC



## Installing and Using Falco
[Falco](https://falco.org/) is a runtime security engine. I used to use [ossec](https://elatov.github.io/2014/04/ossec-freebsd/) and this reminds me of that software but container centric. To install it, we can use a [helm chart](https://github.com/falcosecurity/charts):

```bash
> git clone https://github.com/falcosecurity/charts
> helm template \
  --set ebpf.enabled=true \
  --set falco.jsonOutput=true \
  --set falco.jsonIncludeOutputProperty=true \
  --set falco.programOutput.enabled=true \
  --set falco.programOutput.program=""jq '{text: .output}' | curl -d @- -X POST https://hooks.slack.com/services/see_your_slack_team/apps_settings_for/a_webhook_url \
  charts/falco
```

It creates a *daemonset* and compiles a kernel module on each node. If you check out the logs when the *daemonset* is starting up you will see something like this:

```bash
> k logs -f falco-7gcdl 
* Setting up /usr/src links from host
* Running falco-driver-loader with: driver=bpf, compile=yes, download=yes
* Mounting debugfs
* Found kernel config at /host/boot/config-5.4.0-33-generic
* Trying to compile the eBPF probe (falco_ubuntu-generic_5.4.0-33-generic_37.o)
In file included from /usr/src/falco-96bd9bc560f67742738eb7255aeb4d03046b8045/bpf/probe.c:13:
In file included from ./include/linux/sched.h:14:
...
...
5 warnings generated.
* Skipping download, eBPF probe is already present in /root/.falco/falco_ubuntu-generic_5.4.0-33-generic_37.o
* eBPF probe located in /root/.falco/falco_ubuntu-generic_5.4.0-33-generic_37.o
* Success: eBPF probe symlinked to /root/.falco/falco-bpf.o
Sat Jun  6 02:40:49 2020: Falco initialized with configuration file /etc/falco/falco.yaml
Sat Jun  6 02:40:49 2020: Loading rules from file /etc/falco/falco_rules.yaml:
Sat Jun  6 02:40:50 2020: Loading rules from file /etc/falco/falco_rules.local.yaml:
Sat Jun  6 02:40:55 2020: Starting internal webserver, listening on port 8765
```

Then as a quick test launch a container and open a shell to it:

```bash
> kubectl run -it --rm test --image busybox --restart Never --command -- /bin/sh  
If you don't see a command prompt, try pressing enter.
/ # 
```

And in your slack channel you will see a rule triggered:

![falco-rule-triggered-in-slack.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/sec-tool-k8s/falco-rule-triggered-in-slack.png)

If you want to modify the rules there is a way to **append** rules to add logic to ignore any false positives that may apply to your setup. The process is described in [Appending to Rules](https://falco.org/docs/rules/#appending-to-rules). I ended up creating a *configmap* with the **falco_rules.yaml** and **falco_rules.local.yaml** files and updating them to fit my needs. 

If you are so inclined you can also setup the [falco-exporter](https://github.com/falcosecurity/falco-exporter) to export events for scraping by [prometheus](https://prometheus.io/).

## Using Trivy
I was actually watching the [Trivy Open Source Scanner for Container Images – Just Download and Run!](https://www.cncf.io/webinars/trivy-open-source-scanner-for-container-images-just-download-and-run/) CNCF webinar and I really like what it does and it's upcoming features. I also enjoyed the results of [Open Source CVE Scanner Round-Up: Clair vs Anchore vs Trivy](https://boxboat.com/2020/04/24/image-scanning-tech-compared/) web page. To run it manually and locally you can just install it on any Linux distro. On my [ArchLinux](https://www.archlinux.org/) machine I just ran the following to install it:

```bash
> yay -S aur/trivy
```

Then as a quick test we can run the following:

```bash
> trivy i quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.32.0
2020-06-05T23:02:30.128-0400	INFO	Need to update DB
2020-06-05T23:02:30.128-0400	INFO	Downloading DB...
16.42 MiB / 16.42 MiB [-----------] 100.00% 6.67 MiB p/s 3s
2020-06-05T23:02:33.798-0400	INFO	Detecting Alpine vulnerabilities...

quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.32.0 (alpine 3.11.5)
=====================================================================================
Total: 2 (UNKNOWN: 1, LOW: 0, MEDIUM: 1, HIGH: 0, CRITICAL: 0)

+---------+------------------+----------+-------------------+---------------+--------------------------------+
| LIBRARY | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |             TITLE              |
+---------+------------------+----------+-------------------+---------------+--------------------------------+
| libxml2 | CVE-2019-20388   | MEDIUM   | 2.9.10-r2         | 2.9.10-r3     | libxml2: memory leak           |
|         |                  |          |                   |               | in xmlSchemaPreRun in          |
|         |                  |          |                   |               | xmlschemas.c                   |
+---------+------------------+----------+-------------------+---------------+--------------------------------+
| nghttp2 | CVE-2020-11080   | UNKNOWN  | 1.40.0-r0         | 1.40.0-r1     | In nghttp2 before version      |
|         |                  |          |                   |               | 1.41.0, the overly large       |
|         |                  |          |                   |               | HTTP/2 SETTINGS frame          |
|         |                  |          |                   |               | payload...                     |
+---------+------------------+----------+-------------------+---------------+--------------------------------+
```

They have a database which is updated every 12 hours and they scan from popular locations. From their [vuln-list](https://github.com/aquasecurity/vuln-list) here are the sources they use to generate their database from:


> | Directory   | OS               | Source            | URL                                                                  |
> | ----------- | ---------------- | ---------------------- | ----------------------------------------------------------- |
> | alpine/     | Alpine Linux     | Alpine Linux Bug tracker        | https://bugs.alpinelinux.org/projects/alpine/issues |
> | amazon/1    | Amazon Linux     | Amazon Linux Security Center    | https://alas.aws.amazon.com/                        |
> | amazon/2    | Amazon Linux 2   | Amazon Linux Security Center    | https://alas.aws.amazon.com/alas2.html              |
> | debian/     | Debian GNU/Linux | Security Bug Tracker            | https://security-tracker.debian.org/tracker/        |
> | nvd/        | -                | National Vulnerability Database | https://nvd.nist.gov/                               |
> | oval/debian | Debian GNU/Linux | OVAL                            | https://www.debian.org/security/oval/               |
> | redhat/     | RHEL/CentOS      | Security Data                   | https://www.redhat.com/security/data/metrics/       |
> | ubuntu/     | Ubuntu           | Ubuntu CVE Tracker              | https://people.canonical.com/~ubuntu-security/cve/  |
> | cvrf/suse   | OpenSUSE/SLES    | SUSE Security CVRF              | http://ftp.suse.com/pub/projects/security/cvrf/     |
> | photon/     | Photon           | Photon Security Advisory        | https://vmware.bintray.com/photon_cve_metadata/     |
> | ghsa/       | -                | GitHub Advisory Database        | https://github.com/advisories/                      |
>

I thought it was pretty useful. They also have examples of how to use it in your CI system, the process is described in [Continuous Integration (CI)](Continuous Integration (CI)), you basically run something along the lines of this:

```bash
./trivy --exit-code 0 --severity HIGH --no-progress trivy-ci-test:${COMMIT}
./trivy --exit-code 1 --severity CRITICAL --no-progress trivy-ci-test:${COMMIT}
```

As part of your CI/CD and make a decision whether to stop the build or keep going based on how many vulnaribilities the image has. 

### Adding Trivy to a Tekton Pipeline
I decided to keep just informational and added a new task which I called from a couple of pipelines:

```bash
> cat tasks/trivy-scan.yaml 
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: trivy-scan
spec:
  workspaces:
    - name: git-source
      description: The git repo
  params:
  - name: msg-file
    description: file to be used to send smack message
    type: string
    default: msg.txt
  steps:
  - name: trivy-scan-image
    image: aquasec/trivy
    script: |
      #!/bin/sh
      ## Globals
      GREP="/bin/grep"
      AWK="/usr/bin/awk"
      TRIVY="/usr/local/bin/trivy"
      SOURCE=$(workspaces.git-source.path)
      MSG="${SOURCE}/$(params.msg-file)"

      IMAGES=$(${GREP} -h 'image:' ${SOURCE}/*.yaml | ${AWK} -F ' ' '{ print $2 }')
      for image in ${IMAGES}; do
        echo "*${image}*" >> ${MSG};
        echo '```' >> ${MSG};
        ${TRIVY} -q image -o file.txt ${image} >> ${MSG};
        echo '```' >> ${MSG};
      done
      # debug
      cat ${MSG}

  - name: send-mesg
    image: curlimages/curl:7.68.0
    script: |
      #!/bin/sh
      SED="/bin/sed"
      CURL="/usr/bin/curl"
      CAT="/bin/cat"
      SOURCE=$(workspaces.git-source.path)
      MSG_FILE="${SOURCE}/$(params.msg-file)"
      MSG=$(${CAT} ${MSG_FILE})

      ${CURL} -s -X POST -H 'Content-type: application/json' --data '{"text":"'"${MSG}"'"}' $URL

    env:
    - name: URL
      valueFrom:
        secretKeyRef:
          name: webhook-secret
          key: url
```

And I would get a message in my slack channel with the results :) (check out [previous post](/2020/05/cert-manager-botkube-and-tektonpipelines-with-conditions/#tekton-task) on how to use pipelines and how to [share data between tasks](https://github.com/tektoncd/pipeline/blob/master/docs/workspaces.md#using-workspaces-in-pipelines) in a pipelinerun... also as a side note check out this awesome post [Speed up Maven builds in Tekton Pipelines](https://developers.redhat.com/blog/2020/02/26/speed-up-maven-builds-in-tekton-pipelines/) as well)

## Using Snyk
Snyk takes a different approach and it tries to stay really close to the source code and catch issues there (which is really awesome). I ended up using an awesome tool called [rss2hook](https://github.com/skx/rss2hook).. it's a go script to monitor RSS feeds and post the results to a webhook (like tekton :) ). I actually used [kaniko](https://github.com/GoogleContainerTools/kaniko) to build it with [tekton](https://github.com/tektoncd/pipeline).

### Use Kaniko to Build a Container

There is actually a [catalog](https://github.com/tektoncd/catalog) item which has an example on how to use [kaniko with tekton](https://github.com/tektoncd/catalog/tree/master/kaniko). I ended up using the following task to build a [Dockerfile](https://hub.docker.com/r/firecyberice/rss2hook/dockerfile) (you have to rebuild the `rss2hook` binary if you want to use it with alpine Linux ... this is discussed in [Can not run in docker](https://github.com/skx/rss2hook/issues/4)):

```bash
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: kaniko-dockerhub
spec:
  workspaces:
    - name: git-source
      description: The git repo
  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-secret
      items:
        - key: .dockerconfigjson
          path: config.json
  params:
  - name: IMAGE
    description: Name (reference) of the image to build.
  - name: VERSION
    description: Tag of the image to build.
  - name: DOCKERFILE
    description: Path to the Dockerfile to build.
    default: ./Dockerfile
  - name: CONTEXT
    description: The build context used by Kaniko.
    default: ./
  steps:
  - name: build-and-push
    workingDir: $(workspaces.git-source.path)
    # for debugging, I used this to troubleshoot the docker config
    #image: gcr.io/kaniko-project/executor:debug
    #command: ["/busybox/sh"]
    #args: ["-c", "while true; do echo hello; done"]
    image: gcr.io/kaniko-project/executor
    # specifying DOCKER_CONFIG is required to allow kaniko to detect docker credential
    # https://github.com/tektoncd/pipeline/pull/706
    env:
    - name: DOCKER_CONFIG
      value: /tekton/home/.docker
    command:
    - /kaniko/executor
    - --dockerfile=$(workspaces.git-source.path)/$(params.DOCKERFILE)
    - --context=$(workspaces.git-source.path)/$(params.CONTEXT)
    - --destination=$(params.IMAGE):$(params.VERSION)
    # kaniko assumes it is running as root, which means this example fails on platforms
    # that default to run containers as random uid (like OpenShift). Adding this securityContext
    # makes it explicit that it needs to run as root.
    securityContext:
      runAsUser: 0
    volumeMounts:
      - name: docker-config
        mountPath: /tekton/home/.docker
```

There are also a couple of other examples of using kaniko with tekton:

* [A first look at Tekton Pipelines](https://octopus.com/blog/introduction-to-tekton-pipelines)
* [Build and run container image using Knative + Tekton](https://ruzickap.github.io/k8s-knative-gitlab-harbor/part-07/)

After the pipeline is finished, I see the image available in dockerhub:

![dockerhub-rss2hook.png](https://res.cloudinary.com/elatov/image/upload/v1591497882/blog-pics/sec-tool-k8s/dockerhub-rss2hook.png)

### Integrating Dockerhub with Snyk
The easiest way to integrate with it is to add your [dockerhub](https://hub.docker.com/) account to **snyk**. So login to their website and follow the instructions laid out in [Configure integration for Docker Hub](https://support.snyk.io/hc/en-us/articles/360003916058-Configure-integration-for-Docker-Hub) to add your [dockerhub](https://hub.docker.com/) account and to choose which image you would like to scan. After you are done you will see the image added:

![dockerhub-snyk.png](https://res.cloudinary.com/elatov/image/upload/v1591497820/blog-pics/sec-tool-k8s/dockerhub-snyk.png)

You can also point it directly to your Dockerfile if you ended up adding your github account to snyk ([Prerequisites for Dockerfile analysis](https://support.snyk.io/hc/en-us/articles/360003916198-Prerequisites-for-Dockerfile-analysis)). This is covered in [Adding your Dockerfile and test your base image](https://support.snyk.io/hc/en-us/articles/360003916218-Adding-your-Dockerfile-and-test-your-base-image) and it will make suggestions to prevent vulnaribilites at *Dockerfile Steps* level. In my example I didn't have any vulnaribilities but the possibilities are pretty cool:

![snyk-scan-results.png](https://res.cloudinary.com/elatov/image/upload/v1591497882/blog-pics/sec-tool-k8s/snyk-scan-results.png)

To compare we a can also do a scan with **trivy**:

```bash
> trivy i elatov/rss2hook:0.3
2020-06-06T22:38:02.305-0400	WARN	This OS version is not on the EOL list: alpine 3.12
2020-06-06T22:38:02.305-0400	INFO	Detecting Alpine vulnerabilities...
2020-06-06T22:38:02.305-0400	WARN	This OS version is no longer supported by the distribution: alpine 3.12.0
2020-06-06T22:38:02.306-0400	WARN	The vulnerability detection may be insufficient because security updates are not provided

elatov/rss2hook:0.3 (alpine 3.12.0)
===================================
Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)

```
