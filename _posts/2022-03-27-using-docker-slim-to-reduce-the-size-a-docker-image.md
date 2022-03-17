---
published: true
layout: post
title: "Using docker slim to reduce the size a docker image"
author: Karim Elatov
categories: [security, containers]
tags: [docker, python]
---

## Slimming down your container images
There are a couple of sites that cover as to why you should keep your container images small:

- [The Quest for Minimal Docker Images, part 3](https://jpetazzo.github.io/2020/04/01/quest-minimal-docker-images-part-3/)
- [Build smaller containers](https://fedoramagazine.org/build-smaller-containers/)
- [Automatically reduce Docker container size using DockerSlim](https://www.slim.ai/blog/automatically-reduce-docker-container-size-using-dockerslim.html)

Usually it's to improve startup time, security and maintenance. So common practices include:

1. Start with a small base (alpine, distroless...etc)
2. Use Multi-Stage Builds (this works well for statically complied software)
3. Remove unnecessary software after the fact (this is what docker-slim does)
4. Use a custom build pipeline to build a custom image (this is like [jib](https://github.com/GoogleContainerTools/jib), [nix](https://nix.dev/tutorials/building-and-running-docker-images), and [build packs](https://github.com/buildpacks/pack))

I decided to try out [docker-slim](https://github.com/docker-slim/docker-slim)
## Trying out docker-slim
There is a pretty nice python example at [Docker Slim example](https://gitlab.com/MShekow/docker-slim-example/-/tree/main), it's simple and gets the point across.  The application itself is very easy to use, you just point it to an existing docker image and it will take care of the rest. By default it expects you to use your application so it can check what files your applications uses. So if you run it without any parameters you will see the following:

```bash
> docker-slim build --http-probe=false library/python-slim:0.0.37
docker-slim: message='join the Gitter channel to ask questions or to share your feedback' info='https://gitter.im/docker-slim/community'
docker-slim: message='join the Discord server to ask questions or to share your feedback' info='https://discord.gg/9tDyxYS'
docker-slim: message='Github discussions' info='https://github.com/docker-slim/docker-slim/discussions'
cmd=build info=exec message='changing continue-after from probe to nothing because http-probe is disabled'
cmd=build info=exec message='changing continue-after to enter'
cmd=build state=started
cmd=build info=params keep.perms='true' tags='' target.type='image' target='library/python-slim:0.0.37' continue.mode='enter' rt.as.user='true'
cmd=build state=image.inspection.start
cmd=build info=image id='sha256:576e6c2e95a898b16f24704ac00ac1fbf587abb02c5e05df81f433f833b0ea67' size.bytes='926493233' size.human='926 MB'
cmd=build info=image.stack index='0' name='library/python-slim:0.0.37' id='sha256:576e6c2e95a898b16f24704ac00ac1fbf587abb02c5e05df81f433f833b0ea67'
cmd=build state=image.inspection.done
cmd=build state=container.inspection.start
cmd=build info=container status='created' name='dockerslimk_17458_20220317163527' id='7e0d5c7f15a7dc3246d3adf63876746a0893c735f4f3104e614c46456becb721'
cmd=build info=container name='dockerslimk_17458_20220317163527' id='7e0d5c7f15a7dc3246d3adf63876746a0893c735f4f3104e614c46456becb721' status='running'
cmd=build info=container message='obtained IP address' ip='172.17.0.3'
cmd=build info=cmd.startmonitor status='sent'
cmd=build info=event.startmonitor.done status='received'
cmd=build info=container name='dockerslimk_17458_20220317163527' id='7e0d5c7f15a7dc3246d3adf63876746a0893c735f4f3104e614c46456becb721' target.port.list='' target.port.info='' message='YOU CAN USE THESE PORTS TO INTERACT WITH THE CONTAINER'
cmd=build info=continue.after mode='enter' message='provide the expected input to allow the container inspector to continue its execution'
cmd=build prompt='USER INPUT REQUIRED, PRESS <ENTER> WHEN YOU ARE DONE USING THE CONTAINER'
```

So at this point you can check for running `docker` processes and `exec` into the one `docker-slim` is using:

```bash
> docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED              STATUS              PORTS                                                NAMES
7e0d5c7f15a7   library/python-slim:0.0.37   "/opt/dockerslim/bin…"   About a minute ago   Up About a minute   0.0.0.0:55015->65501/tcp, 0.0.0.0:55014->65502/tcp   dockerslimk_17458_20220317163527
> docker exec -it 7e0d5c7f15a7  /bin/bash
root@7e0d5c7f15a7:/app# ls
python	requirements.txt
root@7e0d5c7f15a7:/app#
exit
```

We just ran `ls` and it will assume that's all our application needs. Going back to the other terminal where `docker-slim build` was running and hitting `enter` will let `docker-slim` know that we finished using our application, will yield the following results:

```bash
cmd=build state=container.inspection.finishing
cmd=build state=container.inspection.artifact.processing
cmd=build state=container.inspection.done
cmd=build state=building message=building optimized image
cmd=build state=completed
cmd=build info=results status='MINIFIED' by='70.55X' size.original='926 MB' size.optimized='13 MB'
cmd=build info=results has.data='true' image.name='library/python-slim.slim' image.size='13 MB'
cmd=build info=results artifacts.location='/tmp/docker-slim-state/.docker-slim-state/images/576e6c2e95a898b16f24704ac00ac1fbf587abb02c5e05df81f433f833b0ea67/artifacts'
cmd=build info=results artifacts.report='creport.json'
cmd=build info=results artifacts.dockerfile.reversed='Dockerfile.fat'
cmd=build info=results artifacts.dockerfile.optimized='Dockerfile'
cmd=build info=results artifacts.seccomp='library-python-slim-seccomp.json'
cmd=build info=results artifacts.apparmor='library-python-slim-apparmor-profile'
cmd=build state=done
cmd=build info=commands message='use the xray command to learn more about the optimize image'
cmd=build info=report file='slim.report.json'
docker-slim: message='join the Gitter channel to ask questions or to share your feedback' info='https://gitter.im/docker-slim/community'
docker-slim: message='join the Discord server to ask questions or to share your feedback' info='https://discord.gg/9tDyxYS'
docker-slim: message='Github discussions' info='https://github.com/docker-slim/docker-slim/discussions'
```

You will also notice we went from **926 MB** to **13 MB**. That's quite an improvement. Or you can also pass in a script which will mimic the real use of your application in the container. 

```bash
> docker-slim build --http-probe=false --exec-file docker-slim-usage.bash library/python-slim:0.0.37
```

You can also add a parameter to explicitly keep directories that you want, so I just kept all the python libraries:

```bash
> cat preserved-paths.txt
/usr/local/lib/python3.10
> docker-slim build --http-probe=false --exec-file docker-slim-usage.bash --preserve-path-file preserved-paths.txt library/python-slim:0.0.37
```

## Checking out Container images
There are a bunch of tools out that can analyze you container images:

- [dive](https://github.com/wagoodman/dive)
- [container-diff](https://github.com/GoogleContainerTools/container-diff)
- [docker-slim xray][https://github.com/docker-slim/docker-slim#xray-command-options]

If you run `docker-slim xray` it will show you the largest files per layer in the container which is kind of nice:

```bash
> docker-slim xray library/python-slim:0.0.37
..
..
cmd=xray info=layer.objects.top.start
A: mode=-rwxr-xr-x size.human='3.7 MB' size.bytes=3681152 uid=0 gid=0 mtime='2021-09-24T16:10:58Z' H=[A:0] hash=b1965e74b3d8c216e8a4d43463db51c708a67a2c '/usr/bin/perl'
A: mode=-rw-r--r-- size.human='3.1 MB' size.bytes=3076960 uid=0 gid=0 mtime='2021-08-24T08:28:12Z' H=[A:0] hash=3830f28cd6bc8940e4425c664a2bde133111c054 '/usr/lib/x86_64-linux-gnu/libcrypto.so.1.1'
..
..
cmd=xray info=layer.objects.top.start
A: mode=-rw-r--r-- size.human='84 MB' size.bytes=84483096 uid=0 gid=0 mtime='2021-01-06T19:16:26Z' H=[A:7] hash=bcc70cc5849dd8a623cfc6a7539be6edbeb547eb '/usr/lib/x86_64-linux-gnu/libLLVM-11.so.1'
A: mode=-rw-r--r-- size.human='28 MB' size.bytes=28407344 uid=0 gid=0 mtime='2021-06-30T16:07:32Z' H=[A:7] hash=ac8f14104c9a8f1c3c12c3a7baa514479aaa000a '/usr/lib/x86_64-linux-gnu/libicudata.so.67.1'
A: mode=-rw-r--r-- size.human='23 MB' size.bytes=22910144 uid=0 gid=0 mtime='2021-01-29T16:44:09Z' H=[A:7] hash=0a591749e44a14713732d40a445abd7e433d396d '/usr/lib/x86_64-linux-gnu/libz3.so.4'
```

So that can give you an idea of which files you need to get rid of. You can also run `container-diff` across multiple images to see which files were removed:

```bash
> container-diff analyze library/python-slim:0.0.37 -t file > first.txt
> container-diff analyze library/python-slim.slim -t file > second.txt
> diff --side-by-side first.txt second.txt | head -15

-----File-----							                      -----File-----

Analysis for library/python-slim:0.0.37:		      |	Analysis for library/python-slim.slim:
FILE                                              	FILE
/app                                               	/app
/app/python                                        	/app/python
/app/requirements.txt                              	/app/requirements.txt
/bin                                              |	/bin
/bin/bash                                          	/bin/bash
/bin/chgrp                                         <
/bin/chmod                                         <
/bin/chown                                         <
/bin/cp                                            <
```

Which gives you a quick look into what has changed.

### Tracking down dependencies
Most people mention that a lot of application use lazy loading so you might miss some depenedencies that your application actually need. I kind of ran into that. I had a python script that queried some logs in GCP. After using the new image, I received this error:

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.10/site-packages/google/cloud/logging_v2/client.py", line 122, in __init__
    super(Client, self).__init__(
  File "/usr/local/lib/python3.10/site-packages/google/cloud/client/__init__.py", line 318, in __init__
    _ClientProjectMixin.__init__(self, project=project, credentials=credentials)
  File "/usr/local/lib/python3.10/site-packages/google/cloud/client/__init__.py", line 269, in __init__
    raise EnvironmentError(
OSError: Project was not passed and could not be determined from the environment.
```
Since the code is running from a container it will inherit the service account from the underlying node (this is discussed in [Use the default Compute Engine service account](https://cloud.google.com/kubernetes-engine/docs/tutorials/authenticating-to-cloud-platform#use_the_default_service_account)), so I wasn't sure why all of a sudden it was unable to get the GCP credentials. 

So I spun up the old image and ran `strace` on my python script and I saw the following at the end:

```bash
root@python-debug:/app# strace -e openat python3 f.py
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/local/lib/libpython3.10.so.1.0", O_RDONLY|O_CLOEXEC) = 3
..
..
openat(AT_FDCWD, "/usr/local/lib/python3.10/site-packages/google/auth/__pycache__/iam.cpython-310.pyc", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/local/lib/python3.10/site-packages/google/auth/compute_engine/__pycache__/_metadata.cpython-310.pyc", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/nsswitch.conf", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/host.conf", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/resolv.conf", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libnss_files.so.2", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/hosts", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libnss_dns.so.2", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libresolv.so.2", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/hosts", O_RDONLY|O_CLOEXEC) = 3
```

If I remove the `strace` filter, I actaully the see code make some API calls get a token:

```bash
connect(3, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("169.254.169.254")}, 16) = 0
setsockopt(3, SOL_TCP, TCP_NODELAY, [1], 4) = 0
sendto(3, "GET /computeMetadata/v1/project/"..., 139, 0, NULL, 0) = 139
recvfrom(3, "HTTP/1.1 200 OK\r\nMetadata-Flavor"..., 8192, 0, NULL, NULL) = 247
close(3)                                = 0
stat("/root/.config/gcloud/application_default_credentials.json", 0x7ffd7ef7ef00) = -1 ENOENT (No such file or directory)
socket(AF_INET, SOCK_STREAM|SOCK_CLOEXEC, IPPROTO_TCP) = 3
ioctl(3, FIONBIO, [1])                  = 0
connect(3, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("169.254.169.254")}, 16) = -1 EINPROGRESS (Operation now in progress)
```

The **169.254.169.254** address it the metadata server used in GCP for DNS, among other things (this is discussed in [Accessing VMs by internal DNS](https://cloud.google.com/compute/docs/internal-dns#access_by_internal_DNS)). Then doing the same on the slimmed down/broken image I saw the following:

```bash
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libnss_dns.so.2", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/haswell/x86_64/libnss_dns.so.2", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/lib/x86_64-linux-gnu/tls/haswell/x86_64", 0x7ffc5ddc1700) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/haswell/libnss_dns.so.2", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/lib/x86_64-linux-gnu/tls/haswell", 0x7ffc5ddc1700) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/x86_64/libnss_dns.so.2", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/lib/x86_64-linux-gnu/tls/x86_64", 0x7ffc5ddc1700) = -1 ENOENT (No such file or directory)
```

It just kept looking for `libnss_dns.so` but couldn't find it since it's not there. It's unable resolve with DNS and therefore it doesn't get a valid OAuth Token.  So I added the following to my preserved paths:

```
> cat preserved-paths.txt
/usr/local/lib/python3.10
/lib/x86_64-linux-gnu
```

And then it worked as expected. 