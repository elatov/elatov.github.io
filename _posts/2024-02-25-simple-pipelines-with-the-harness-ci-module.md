---
published: false
layout: post
title: "Simple Pipelines with the Harness CI module"
author: Karim Elatov
categories: [automation, home_lab]
tags: [harness]
---
I have been using [Tekton](https://tekton.dev/) for a while now and I wanted to try another tool just to compare. After some research I decided to try [harness](https://www.harness.io/). They have a free offering with some limits, but I think the [limits](https://developer.harness.io/docs/continuous-integration/get-started/ci-subscription-mgmt#harness-cloud-billing-and-build-credits) are pretty good. For the purpose of this evaluation I will just concentrate on the [Continuous Integration](https://developer.harness.io/docs/continuous-integration) module, since I use [argoCD](https://argo-cd.readthedocs.io/en/stable/) for most of my Continuos Delivery functionatlity. Let's cover some basic use cases.

## Interacting with Git
Harness has a concept of [connectors](https://developer.harness.io/docs/category/connectors) and there are different type of connectors like: cloud providers, artifact registries, code repositories... etc. When connecting to the Git we will use the [code repositories](https://developer.harness.io/docs/category/code-repositories) connectors. I was using github for my repos, but I decided to use the [ssh authentication approach](https://developer.harness.io/docs/platform/connectors/code-repositories/connect-to-code-repo#using-ssh-key-authentication) since it allowed me, not only to pull the repo, but to also push to a repo as well.

### Getting Secrets in a Run Step

## Using Triggers

### Conditional Steps

## Passing information between steps

## Building and Pushing to Dockerhub

## Running Local Builders

