---
published: true
layout: post
title: "Deploy GitLab Runner on GCP with Terraform and Run a Simple CI/CD Job for Firebase"
author: Karim Elatov
categories: [automation, devops, cloud]
tags: [gitlab, terraform, firebase]
---

There are a couple of components to the setup. Let's cover them one by one.

## GCP Terraform

It uses terraform to deploy builders for gitlab. 

### Create a Terraform API Token

Using a remote state is always a good idea, in case multiple people need to apply a terraform change. I ended up using the free terraform cloud provider to hold the state. After you create an account and a project you can use the [Using Terraform Cloud Remote State Management](https://www.hashicorp.com/blog/using-terraform-cloud-remote-state-management/) to get the values to be used with terraform. Update the `backend.tf` file with appropriate values.

### Setup your Terraform Env

Create and download service account private key:

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
gcloud iam service-accounts keys create \
      --iam-account terraform@${PROJECT_ID}.iam.gserviceaccount.com credentials.json
```

The credentials can be provided in multiple ways and each option is covered in [Google Provider Configuration Reference](https://www.terraform.io/docs/providers/google/guides/provider_reference.html#credentials-1), but by default creating a `credentials.json` in the `terraform-gcp` directory will work. Next create a **tfvars** file from the template:

```bash
cp terraform.tfvars.template terraform.auto.tfvars
```

And update the missing parameters, like **gcp_project** and so forth.

### Create the Runner

Run the following to start the install:

```bash
terraform init
terraform plan
tearrform apply -auto-approve
```

If you go to **Settings** -> **CI/CD** -> **Runners** you will see the runner up and registered.

#### Deleting the Runner

By default with Terraform Cloud you need to set an extra environment variable at the project level to allow deletion of terraform resources ( this is covered in [Clean Up Cloud Resources](https://learn.hashicorp.com/terraform/cloud-gettingstarted/tfc_cleanup#set-an-environment-variable)). After that's set then you can run the following to clean up:

```bash
terraform destroy -auto-approve
```

## Creating CI/CD Pipelines in Gitlab

After the installation is finished you can use cloud shell to ssh into the machine for any sort of troubleshooting:

```bash
$ gcloud compute ssh gitlab-ci-runner --zone us-east4-c
```

Then confirm the service is running:

```bash
   Memory: 12.6M
   CGroup: /system.slice/gitlab-runner.service
           └─2602 /usr/lib/gitlab-runner/gitlab-runner run --working-directory /home/gitlab-runner --config /etc/gitlab-runner/config.toml --service gitlab-runner --syslog --user gitlab-runner

Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]: Running in system-mode.
Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]: Running in system-mode.
Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]:
Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]:
Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]: Configuration loaded                                builds=0
Mar 26 21:26:50 gitlab-ci-runner gitlab-runner[2602]: Configuration loaded                                builds=0
```

### Creating a firebase container image

Now let's create a simple job to run a `firebase` command from a builder. This is described in [Deploying to Firebase](https://cloud.google.com/cloud-build/docs/deploying-builds/deploy-firebase). In the cloud shell, create a **Dockerfile** with the following contents:

```bash
# use latest Node LTS
FROM node:alpine
# install Firebase CLI
RUN npm install -g firebase-tools
```

Then build it and push it:

```bash
$ export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
$ gcloud container images list
Listed 0 items.
Only listing images in gcr.io/GCP_PROJECT. Use --repository to list images in other repositories.
$ docker build -t gcr.io/${PROJECT_ID}/firebase-cli .
$ docker push gcr.io/${PROJECT_ID}/firebase-cli
```

Get a firebase token key. From cloud shell run the following:

```bash
$ firebase login:ci --no-localhost
```

Save the output and create a variable in **gitlab** as described in [How to leverage GitLab CI/CD for Google Firebase](https://about.gitlab.com/blog/2020/03/16/gitlab-ci-cd-with-firebase/). 

### Creating a simple .gitlab-ci.yaml
Lastly create a simple `.gitlab-ci.yaml` file which just lists available projects:

```yaml
image: gcr.io/${PROJECT_ID}/firebase-cli

deploy-functions:
  stage: deploy
  tags:
    - docker
    - gce
    - specific
  script:
    - firebase projects:list --token $FIREBASE_TOKEN
  only:
    refs:
      - master
```

If you just commit that to the repo, it will automatically start the build. As a quick test I installed [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/cli.html) and created an [access token for gitlab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) so I could query status of [gitlab pipelines](https://docs.gitlab.com/ee/ci/pipelines/). First get the gitlab project ID and Job IDs. To get the **ProjectID**, you can run the following:

```bash
> gitlab project list --owned TRUE
id: GITLAB_PROJECT_ID
path: repo
```

And to get the **JOB_ID**, you can run the following:

```bash
> gitlab project-job list --project-id ${GITLAB_PROJECT_ID} | head -1
id: GITLAB_JOB_ID
```

When I checked the status of my job I saw the following:

```bash
> gitlab project-job trace --project-id ${GITLAB_PROJECT_ID} --id ${GITLAB_JOB_ID}
Running with gitlab-runner 12.9.0 (4c96e5ad)
  on GCP_PROJECT_ID ToQevJz8
Preparing the "docker" executor
Using Docker executor with image gcr.io/GCP_PROJECT_ID/firebase-cli ...
Authenticating with credentials from /root/.docker/config.json
Pulling docker image gcr.io/GCP_PROJECT_ID/firebase-cli ...
Using docker image sha256:a4b5bdd020624c74aba15a for gcr.io/GCP_PROJECT_ID/firebase-cli ...
Preparing environment
Running on runner-ToQevJz8-project-GITLAB_PROJECT_ID-concurrent-0 via gitlab-ci-runner...
Getting source from Git repository
Fetching changes with git depth set to 50...
Initialized empty Git repository in /builds/NAME/utils/.git/
Created fresh repository.
From https://gitlab.com/NAME/REPO
 * [new ref]         refs/pipelines/GITLAB_JOB_ID -> refs/pipelines/GITLAB_JOB_ID
 * [new branch]      master                   -> origin/master
Checking out 06082c0a as master...

Skipping Git submodules setup
Restoring cache
Downloading artifacts
Running before_script and script
Authenticating with credentials from /root/.docker/config.json
$ firebase projects:list --token $FIREBASE_TOKEN
- Preparing the list of your Firebase projects
✔ Preparing the list of your Firebase projects
┌──────────────────────┬───────────────────┬──────────────────────┐
│ Project Display Name │ Project ID        │ Resource Location ID │
├──────────────────────┼───────────────────┼──────────────────────┤
│ FIREBASE_PROJECT     │ GCP_PROJECT_ID    │ us-central           │
└──────────────────────┴───────────────────┴──────────────────────┘

1 project(s) total.
Running after_script
Saving cache
Uploading artifacts for successful job
Job succeeded
```

Pretty cool to see all the components come together.

