---
published: true
layout: post
title: "Improving Ansible Execution Time"
author: Karim Elatov
categories: [automation, devops, os]
tags: [ansible]
---

I ran into a couple of guides on how to improve ansible execution time:

- [8 ways to speed up your Ansible playbooks](https://www.redhat.com/sysadmin/faster-ansible-playbook-execution)
- [Speed Up Ansible](https://dzone.com/articles/speed-up-ansible)
- [How to speed up Ansible playbooks drastically](https://www.linkedin.com/pulse/how-speed-up-ansible-playbooks-drastically-lionel-gurret)
- [How to Speed Up Your Ansible Playbooks Over 600%](https://www.toptechskills.com/ansible-tutorials-courses/speed-up-ansible-playbooks-pipelining-mitogen/)

And I decided to try them out. 

## Get a Benchmark
As described in [Identify slow tasks with callback plugins](https://www.redhat.com/sysadmin/faster-ansible-playbook-execution) we can, at a minimum, enable the following in `/etc/ansible/ansible.cfg`:

```bash
[defaults]
callback_whitelist = profile_tasks
```

And next time you run `ansible-playbook`, it will show you how long each task took:

```bash
Thursday 23 December 2021  22:56:12 +0800 (0:00:00.541) 0:00:14.100 
============================================================= 
deploy-web-server : Install httpd and firewalld ------- 5.42s
deploy-web-server : Git checkout ---------------------- 3.40s
Gathering Facts --------------------------------------- 1.60s
deploy-web-server : Enable and Run Firewalld ---------- 0.82s
deploy-web-server : firewalld permitt httpd service --- 0.72s
deploy-web-server : httpd enabled and running --------- 0.55s
deploy-web-server : Set Hostname on Site -------------- 0.54s
deploy-web-server : Delete content & directory -------- 0.52s
deploy-web-server : Create directory ------------------ 0.41s
Deploy Web service ------------------------------------ 0.04s
```

## Enabling Facts Caching
There is an awesome page that describes the setup process [Local cachíng of Ansible Facts](https://andreas.scherbaum.la/blog/archives/1019-Local-caching-of-Ansible-Facts.html). You just set the following settings in `/etc/ansible/ansible.cfg`:

```bash
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /etc/ansible/facts.json
fact_caching_timeout = 86400
```

And you will notice that the first run will take a while, but the next one will be quicker. Here are back to back `ansible-playbook` executions:

```bash
Sunday 30 January 2022  07:14:18 -0700 (0:00:00.028) 0:03:45.024 
================================================================
Gathering Facts ----------------------------------------- 63.82s

Sunday 30 January 2022  07:18:38 -0700 (0:00:00.038) 0:02:59.448
=================================================================
common : Install common packages -------------------------- 5.13s
```

Saved 60 seconds in execution time.

## Using Mitogen
This made the biggest difference, initially I tried using the old version:

```bash
$ curl -L https://github.com/mitogen-hq/mitogen/archive/refs/tags/v0.2.9.tar.gz
$ tar xvzf v0.2.9.tar.gz
$ mv mitogen-0.2.9 /usr/local/.
```

And then adding the following lines to `/etc/ansible/ansible.cfg`:

```bash
[defaults]
strategy_plugins = /usr/local/mitogen-0.2.9/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

But the `ansible-playbook` failed and I ran into the issue described in [this github](https://github.com/mitogen-hq/mitogen/pull/715) issue and a later version fix it for ansible that is greater than version **2.10**. For some reason on ubuntu I didn't have that version from `apt`, so following instructions from [Installing Ansible on Ubuntu](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu), I enabled the ansible apt repo:

```bash
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo add-apt-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```

And then I got the following version on my ubuntu machine:

```bash
> ansible --version
ansible [core 2.12.1]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/elatov/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /etc/ansible/custom-collections
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
  jinja version = 2.10.1
  libyaml = True
```

Then I downloaded the latest version of [mitogen](https://github.com/mitogen-hq/mitogen/releases):

```bash
$ curl -L https://github.com/mitogen-hq/mitogen/archive/refs/tags/v0.3.2.tar.gz
$ tar xvzf v0.3.2.tar.gz
$ mv mitogen-0.3.2 /usr/local/.
```

And I updated my `ansible.cfg` file:

```bash
[defaults]
callback_whitelist = profile_tasks
strategy_plugins = /usr/local/mitogen-0.3.2/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

And then my `ansible-playbook` went from total of 10 minutes to just 3 minutes.

## Improve Code
After all the changes, I looked at my top tasks and if any of them were over 5 seconds I wanted to see why. All 3 of the troublemakers were tasks that were using `yum` or `package` on a RedHat systems. Reading over some pages:

- [Bundle package installations](https://www.treitos.com/blog/2020/improving-ansible-performance.html)
- [Yum calls are expensive](https://www.linkedin.com/pulse/how-speed-up-ansible-playbooks-drastically-lionel-gurret)

I realized I was doing exactly that and on some tasks I just called the list directly instead of looping and on some I would join the two lists to make sure I can pass that in:

```yaml
- name: yum | kernel-devel install
  package:
    name:
      - "{{ falco_pkgs | join(',') }}"
      - "kernel-devel-{{ ansible_kernel }}"
```

And that helped lower my tasks to be below 6 seconds. After all the different changes, I am definitely happy with the results. One thing I want to try is see if [ansible-pull](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#ansible-pull) is a nice approach... maybe at a later time.
