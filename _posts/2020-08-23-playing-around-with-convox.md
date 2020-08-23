---
published: true
layout: post
title: "Playing Around With Convox"
author: Karim Elatov
categories: [devops,containers]
tags: [aws, convox]
---

## Deploying an Initial Convox Rack
For testing purposes I created a free tier account on aws ([AWS Free Tier](https://aws.amazon.com/free/)). After that you can create an API key pair for the account and download it as a CSV file. Then you can link your AWS account to the convox console (check out more detailed documentation in [Console -> AWS Integration](https://convox.com/docs/aws-integration/)). At this point you can deploy a convox Rack, which will deploy a bunch of services in aws. After deploying a rack you will see the following output in convox (instructions laid out in [Deployment -> Installing a Rack](https://convox.com/docs/installing-a-rack/)):

![convox-rack-deployed.png](https://res.cloudinary.com/elatov/image/upload/v1598198255/blog-pics/convox/convox-rack-deployed.png)

### Convox Architecture

There is a pretty good overview of what a rack is at [Introduction -> Convox Rack](https://convox.com/docs/rack/), from that page:

> A Rack creates and manages all of the underlying infrastructure needed to run and monitor your applications. A Rack is the unit of network isolation – applications and services on a Rack can only communicate with other applications and services on the same Rack
>
> ![convox-rack-diagram.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/convox/convox-rack-diagram.png)


You can also checkout some of the resources that were added to your aws subscription (I decided to use [awless](https://github.com/wallix/awless) and [aws cli](https://aws.amazon.com/cli/) for getting some of the information from aws):

```bash
<> awless list instances
|        ID ▲         |    ZONE    |    NAME    |  STATE  |   TYPE   |
|---------------------|------------|------------|---------|----------|
| i-007670c6b3c8e2ee0 | us-east-1a | karim-test | running | t2.small |
| i-07b70fbb192cb6917 | us-east-1b | karim-test | running | t2.small |
| i-0a27256f6e64dea02 | us-east-1a | karim-test | running | t2.small |
| i-0dd4788a2d7e9c77e | us-east-1c | karim-test | running | t2.small |
```

It creates a new vpc for it's networking:

```bash
<> awless list vpcs
|         ID ▲          |    NAME    | DEFAULT |   STATE   |     CIDR      |
|-----------------------|------------|---------|-----------|---------------|
| vpc-0c1755355d04959e2 | karim-test | false   | available | 10.0.0.0/16   |
| vpc-f607518d          |            | true    | available | 172.31.0.0/16 |
```
It also creates some containers:

```bash
<> awless list containers
| NAME ▲  |          DEPLOYMENTNAME                          |  STATE  | CREATED  | LAUNCHED |
|---------|--------------------------------------------------|---------|----------|----------|
| monitor | service:karim-test-ApiMonitorService-OT03DZYYOGON| RUNNING | 22 hours | 22 hours |
| web     | service:karim-test-ApiWebService-UDRJX1DMZ2EV    | RUNNING | 22 hours | 21 hours |
| web     | service:karim-test-ApiWebService-UDRJX1DMZ2EV    | RUNNING | 22 hours | 21 hours |
```

There a bunch more, but you get the point. 

## Deploying an Application into a Rack

Next we can create an app and make sure we see it. There are some simple examples available at [Convox Examples](https://github.com/convox-examples). I decided to try out the [httpd](https://github.com/convox-examples/httpd) one. Let's clone the repo and give it a shot:

```bash
<> git clone https://github.com/convox-examples/httpd.git
<> cd htpd
<> convox apps create karim-httpd
Creating app karim-httpd... CREATING
```

It will be in that status for a little bit:

```bash
<> convox apps info -a karim-httpd
Name        karim-httpd
Status      creating
Generation  2
Release
```

after it's done you should see it running:

```bash
<> convox --rack karim-test/karim-test apps
APP          GEN  STATUS
karim-httpd  2    running
````

Now let's deploy the actual app:

```bash
<> convox deploy --app karim-httpd
Deploying karim-httpd
Creating tarball... OK
Uploading:  22.62 KiB / 22.45 KiB [=======================] 100.77% 0s
Starting build... OK
Authenticating 19XX.dkr.ecr.us-east-1.amazonaws.com: WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded
pulling: httpd
running: docker pull httpd
Using default tag: latest
latest: Pulling from library/httpd
3d77ce4481b1: Pulling fs layer
...
...
7cd2e04cf570: Pull complete
Digest: sha256:f4610c3a1a7da35072870625733fd0384515f7e912c6223d4a48c6eb749a8617
Status: Downloaded newer image for httpd:latest
running: docker tag httpd convox/karim-httpd/web:BFQSVNPXUVL
running: docker tag convox/karim-httpd/web:BFQSVNPXUVL 19XX.dkr.ecr.us-east-1.amazonaws.com/karim-regis-ovc6lz8vjn1k:web.BFQSVNPXUVL
pushing: 19XX.dkr.ecr.us-east-1.amazonaws.com/karim-regis-ovc6lz8vjn1k:web.BFQSVNPXUVL
Release: RJCCONJUAAN
Promoting RJCCONJUAAN... UPDATING
```

### AWS Resources Created for Convox

When we created a rack, it created a couple of container clusters:

```bash
<> awless list containerclusters
|                NAME ▲                 | STATE  | ACTIVESERVICES | PENDINGTASKS | REGISTEREDCONTAINERINSTANCES | RUNNINGTASKS |
|---------------------------------------|--------|----------------|--------------|------------------------------|--------------|
| karim-test-BuildCluster-1VY6RRX71H0EC | ACTIVE | 0              | 0            | 1                            | 0            |
| karim-test-Cluster-15PZO1CID2K5Q      | ACTIVE | 3              | 0            | 3                            | 4            |
```

Here is a description of a container cluster:

> An Amazon ECS cluster is a regional grouping of one or more container instances on which you can run task requests.

The cluster will contain container instances, which are ec2 instances running a container agent and docker. Here also is a description from amazon:

> An Amazon ECS container instance is an Amazon EC2 instance that is running the Amazon ECS container agent and has been registered into a cluster. When you run tasks with Amazon ECS, your tasks using the EC2 launch type are placed on your active container instances.

Here are the container instances (ec2 instances running docker):

```bash
<> awless list containerinstances
|                ID ▲              |      INSTANCE       |             CLUSTER       | STATE  | RUNNINGTASKS | PENDINGTASKS | CREATED  | AGENTCONNECTED |
|----------------------------------|---------------------|---------------------------|--------|--------------|--------------|----------|----------------|
| arn:aws:ecs:us-east-1:19XX: | i-0a27256f6e64dea02 | karim-test-BuildCluster-         | ACTIVE | 0   | 0            | 27 hours | true           |
| arn:aws:ecs:us-east-1:19XX: | i-007670c6b3c8e2ee0 | karim-test-Cluster-15PZO1CID2K5Q | ACTIVE | 2   | 0            | 27 hours | true           |
| arn:aws:ecs:us-east-1:19XX: | i-07b70fbb192cb6917 | karim-test-Cluster-15PZO1CID2K5Q | ACTIVE | 1   | 0            | 27 hours | true           |
| arn:aws:ecs:us-east-1:19XX: | i-0dd4788a2d7e9c77e | karim-test-Cluster-15PZO1CID2K5Q | ACTIVE | 1   | 0            | 27 hours | true           |
```

### Amazon ECS
This page actually goes into pretty good detail on how it works: [What is Amazon Elastic Container Service?](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) From that page, here are some nice terminology definitions:

> Amazon Elastic Container Service (Amazon ECS) is a highly scalable, fast, container management service that makes it easy to run, stop, and manage Docker containers on a cluster. You can host your cluster on a serverless infrastructure that is managed by Amazon ECS by launching your services or tasks using the Fargate launch type. For more control you can host your tasks on a cluster of Amazon Elastic Compute Cloud (Amazon EC2) instances that you manage by using the EC2 launch type.

and here is a nice architecture diagram:

![amazon-ecs-arch.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/convox/amazon-ecs-arch.png)

The above diagram includes fargate, which i don't think my deployment used, but the overall diagram is good to understand the base concepts. Here are some more:


>Task Definitions
>
> To prepare your application to run on Amazon ECS, you create a task definition. The task definition is a text file, in JSON format, that describes one or more containers, up to a maximum of ten, that form your application. It can be thought of as a blueprint for your application. Task definitions specify various parameters for your application. Examples of task definition parameters are which containers to use, which launch type to use, which ports should be opened for your application, and what data volumes should be used with the containers in the task.
>
> Tasks and Scheduling
> 
> A task is the instantiation of a task definition within a cluster. After you have created a task definition for your application within Amazon ECS, you can specify the number of tasks that will run on your cluster.
>
> ![aws-ecs-svc-arch.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/convox/aws-ecs-svc-arch.png)


We can also checkout the tasks running after the convox deploy:

```bash
<> awless list containertasks
|               NAME ▲               | VERSION |       STATE        |          CONTAINERSIMAGES      |           DEPLOYMENTS                          |
|------------------------------------|---------|--------------------|--------------------------------|------------------------------------------------|
| karim-test-build                   | 1       | ready              | build:convox/rack:             |                                                |
| karim-test-karim-httpd-service-web | 1       | 1 service running  | web:19XX.dkr.ecr.      | karim-test-karim-httpd-ServiceWebService       |
| karim-test-monitor                 | 1       | 1 service running  | monitor:convox/rack:           | karim-test-ApiMonitorService                   |
| karim-test-web                     | 1       | 2 services running | web:convox/rack:               | karim-test-ApiWebService                       |
```

You can also filter by the app name:

```bash
<> awless list containers --filter DeploymentName=httpd
| NAME ▲ |         DEPLOYMENTNAME                                         |  STATE     | CREATED | LAUNCHED |
|--------|----------------------------------------------------------------|------------|---------|----------|
| web    | service:karim-test-karim-httpd-ServiceWebService-1U2P72L9RYM2M | RUNNING    | 59 mins | 58 mins  |
```

You can also do a similar thing with the **aws cli**. First list all the ecs clusters:

```bash
<> aws ecs list-clusters --region us-east-1
{
    "clusterArns": [
        "arn:aws:ecs:us-east-1:19XX:cluster/karim-test-BuildCluster-1VY6RRX71H0EC",
        "arn:aws:ecs:us-east-1:19XX:cluster/karim-test-Cluster-15PZO1CID2K5Q"
    ]
}
```

Then we can checkout all the services that are defined on the cluster:

```bash
<> aws ecs list-services --region us-east-1 --cluster karim-test-Cluster-15PZO1CID2K5Q
{
    "serviceArns": [
        "arn:aws:ecs:us-east-1:19XX:service/karim-test-ApiWebService-UDRJX1DMZ2EV",
        "arn:aws:ecs:us-east-1:19XX:service/karim-test-karim-httpd-ServiceWebService-1U2P72L9RYM2M",
        "arn:aws:ecs:us-east-1:19XX:service/karim-test-ApiMonitorService-OT03DZYYOGON"
    ]
}
```

And also all the tasks running on the cluster from the above service:

```bash
<> aws ecs list-tasks --region us-east-1 --cluster karim-test-Cluster-15PZO1CID2K5Q --service-name karim-test-karim-httpd-ServiceWebService-1U2P72L9RYM2M
{
    "taskArns": [
        "arn:aws:ecs:us-east-1:19XX:task/a41421cf-18f7-493f-9701-625f5656bc83"
    ]
}
```

And then you can "describe" that task which lists the actual container running:

```bash
<> aws ecs describe-tasks --tasks a41421cf-18f7-493f-9701-625f5656bc83 --region us-east-1 --cluster karim-test-Cluster-15PZO1CID2K5Q
{
    "tasks": [
        {
            "taskArn": "arn:aws:ecs:us-east-1:19XX:task/a41421cf-18f7-493f-9701-625f5656bc83",
            "clusterArn": "arn:aws:ecs:us-east-1:19XX:cluster/karim-test-Cluster-15PZO1CID2K5Q",
            "taskDefinitionArn": "arn:aws:ecs:us-east-1:19XX:task-definition/karim-test-karim-httpd-service-web:1",
            "containerInstanceArn": "arn:aws:ecs:us-east-1:19XX:container-instance/9addec39-5f24-4b48-94aa-3de902d45095",
            "overrides": {
                "containerOverrides": [
                    {
                        "name": "web"
                    }
                ]
            },
            "lastStatus": "RUNNING",
            "desiredStatus": "RUNNING",
            "cpu": "256",
            "memory": "512",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:us-east-1:19XX:container/66a8d480-f5c1-4f18-9b65-a5bdffcff971",
                    "taskArn": "arn:aws:ecs:us-east-1:19XX:task/a41421cf-18f7-493f-9701-625f5656bc83",
                    "name": "web",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32768,
                            "protocol": "tcp"
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN"
                }
            ],
            "startedBy": "ecs-svc/9223370511661104836",
            "version": 2,
            "connectivity": "CONNECTED",
            "connectivityAt": 1525193674.235,
            "pullStartedAt": 1525193675.426,
            "pullStoppedAt": 1525193683.426,
            "createdAt": 1525193674.235,
            "startedAt": 1525193684.426,
            "group": "service:karim-test-karim-httpd-ServiceWebService-1U2P72L9RYM2M",
            "launchType": "EC2",
            "attachments": [],
            "healthStatus": "UNKNOWN"
        }
    ],
    "failures": []
}
```

You can see from the above output that the container port is 80 and the host port is **32768**.

### AWS ELB Setup

From the above diagram we can see that convox creates an elb to point to the container. So let's drill down the list to track that down. Here are the elbs created:

```bash
<> awless list loadbalancers
|          NAME ▲           |          VPC      | STATE  |                            PUBLICDNS                            | CREATED  |     SCHEME      |
|---------------------------|-------------------|--------|-----------------------------------------------------------------|----------|-----------------|
| karim-Route-1B7H2GIJW6LEN | vpc-0c1755355d049 | active | karim-Route-1B7H2GIJW6LEN-502343295.us-east-1.elb.amazonaws.com | 43 hours | internet-facing |
```

Then checking out the listeners on that ELB:

```bash
<> awless list listeners
|               ID ▲                | PROTOCOL | PORT |           LOADBALANCER            |          TARGETGROUPS          | ALARMACTIONS |
|-----------------------------------|----------|------|-----------------------------------|--------------------------------|--------------|
|  karim-Route-1B7H2GIJW6LEN  | HTTP     | 80   | arn:aws:elasticloadbalancing:us-  | targetgroup/karim-Route-       |              |
|karim-Route-1B7H2GIJW6LEN  | HTTPS    | 443  | arn:aws:elasticloadbalancing:us-  | targetgroup/karim-Route-       |              |
```

We have one for 80 and 443. Using the **aws cli**, we can check out the rules for those listeners:

```bash
<> aws elbv2 describe-rules --region us-east-1 --listener-arn arn:aws:elasticloadbalancing:us-east-1:19XX:listener/app/karim-Route-1B7H2GIJW6LEN/42515dec79b9a90b/75f1f36d5d4a6f76
{
    "Rules": [
        {
            "RuleArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:listener-rule/app/karim-Route-1B7H2GIJW6LEN/42515dec79b9a90b/75f1f36d5d4a6f76/b5cd6538dc70e913",
            "Priority": "18108",
            "Conditions": [
                {
                    "Field": "host-header",
                    "Values": [
                        "web.karim-httpd.karim-test.convox"
                    ]
                }
            ],
            "Actions": [
                {
                    "Type": "forward",
                    "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:targetgroup/karim-Balan-6O2Y7D0PHCFF/387ff7d390b1f7a9"
                }
            ],
            "IsDefault": false
        },
        {
            "RuleArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:listener-rule/app/karim-Route-1B7H2GIJW6LEN/42515dec79b9a90b/75f1f36d5d4a6f76/b0a31de0ecc67d1c",
            "Priority": "23081",
            "Conditions": [
                {
                    "Field": "host-header",
                    "Values": [
                        "karim-httpd-web.karim-Route-1B7H2GIJW6LEN-502343295.us-east-1.convox.site"
                    ]
                }
            ],
            "Actions": [
                {
                    "Type": "forward",
                    "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:targetgroup/karim-Balan-6O2Y7D0PHCFF/387ff7d390b1f7a9"
                }
            ],
            "IsDefault": false
        },
        {
            "RuleArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:listener-rule/app/karim-Route-1B7H2GIJW6LEN/42515dec79b9a90b/75f1f36d5d4a6f76/67e3b1090563dc95",
            "Priority": "default",
            "Conditions": [],
            "Actions": [
                {
                    "Type": "forward",
                    "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:19XX:targetgroup/karim-Route-MEXGH7ABK6U/704eb1cba209b19e"
                }
            ],
            "IsDefault": true
        }
    ]
}
```

We can see that we forward to a target group called **karim-Balan-6O2Y7D0PHCFF**. Checking out that target group:

```bash
<> aws elbv2 describe-target-health --region us-east-1 --target-group-arn arn:aws:elasticloadbalancing:us-east-1:19XX:targetgroup/karim-Balan-6O2Y7D0PHCFF/387ff7d390b1f7a9
{
    "TargetHealthDescriptions": [
        {
            "Target": {
                "Id": "i-007670c6b3c8e2ee0",
                "Port": 32768
            },
            "HealthCheckPort": "32768",
            "TargetHealth": {
                "State": "healthy"
            }
        }
    ]
}
```

We can see that we target the ec2 instance where the container is running and the correct port. We can also get the endpoints from convox:

```bash
> convox apps info --app karim-httpd
Name        karim-httpd
Status      running
Generation  2
Release     RJCCONJUAAN
Processes   web
Endpoints   karim-httpd-web.karim-Route-1B7H2GIJW6LEN-502343295.us-east-1.convox.site:80 (web)
            karim-httpd-web.karim-Route-1B7H2GIJW6LEN-502343295.us-east-1.convox.site:443 (web)
```

And if we visit the endpoints we will see the app deployed:

![convox-app-httpd-brow.png](https://res.cloudinary.com/elatov/image/upload/v1591415062/blog-pics/convox/convox-app-httpd-brow.png)


## Deleting the Convox Rack
After about 2 days of running a convox Rack, I was notified by amazon that my free tier will start getting charged, so I shut down the rack. To clean up you can run the following:

```bash
<> convox uninstall karim-test us-east-1 Downloads/credentials.csv


     ___    ___     ___   __  __    ___   __  _
    / ___\ / __ \ /  _  \/\ \/\ \  / __ \/\ \/ \
   /\ \__//\ \_\ \/\ \/\ \ \ \_/ |/\ \_\ \/>  </
   \ \____\ \____/\ \_\ \_\ \___/ \ \____//\_/\_\
    \/____/\/___/  \/_/\/_/\/__/   \/___/ \//\/_/


Reading credentials from file Downloads/credentials.csv
Resources to delete:
STACK          TYPE      STATUS
convox-events  resource  CREATE_COMPLETE
karim-test     rack      CREATE_COMPLETE

Delete everything? y/N: y

Uninstalling Convox...
Deleting convox-events...
Deleting karim-test...
Deleted ECS TaskDefinition: ApiBuildTasks
Deleted Lambda Function: karim-test-InstancesLifecycleHandler-QKZJ5KGVIVNA
Deleted Routing Table: rtb-081dc2f05395b1148
Deleted Security Group: sg-00fe7f18bf166b6a1
Deleted ECS TaskDefinition: ApiMonitorTasks
Deleted ECS Service: ApiMonitorService
Deleted KMS Alias: alias/convox-karim-test
Deleted SSL Certificate: RouterApiCertificate
Deleted Application Load Balancer: Router
Deleted ECS TaskDefinition: ApiWebTasks
Deleted ECS Service: ApiWebService
Uninstalling Convox...
Skipped S3 Bucket: karim-test-logs-s3rlg8rqvcpf
Deleted KMS Key: EncryptionKey
Deleted S3 Bucket Policy: karim-test-LogsPolicy-18ODJ3GFHNJEY
Deleted Elastic Load Balancer: karim-test
Skipped S3 Bucket: karim-test-settings-1a2mjwyohb092
Deleted CloudWatch Log Group: karim-test-LogGroup-PUBRBTCTRYC
Deleted DynamoDB Table: karim-test-builds
Deleted SQS Queue: https://sqs.us-east-1.amazonaws.com/19XX/karim-test-AccountEvents-TID8BNKTU61U
Deleted AutoScalingGroup: karim-test-BuildInstances-18BM7ZUNSJXIA
Deleted Hosted Zone: Z3B7P5O8NXKJYH
Deleted DynamoDB Table: karim-test-releases
Deleted ECS Cluster: karim-test-BuildCluster-1VY6RRX71H0EC
Deleted Security Group: sg-0261e90a51dbc4359
Deleted SQS Queue: https://sqs.us-east-1.amazonaws.com/19XX/karim-test-CloudformationEvents-1LGDOHS4UIQFS
Uninstalling Convox...
Deleted Security Group: sg-0ec0c508775c95d1d
Uninstalling Convox...
Deleted AutoScalingGroup: karim-test-Instances-XQHFA301VMZH
Deleted Security Group: sg-035b4f34a054d3787
Deleted ECS Cluster: karim-test-Cluster-15PZO1CID2K5Q
Deleted VPC Subnet: subnet-0abe20fb6642130ee
Deleted VPC Subnet: subnet-065b183ef491c862f
Deleted VPC Subnet: subnet-075ba29543e3437b3
Deleted Lambda Function: karim-test-CustomTopic-1QHWXQ277O4YW
Deleted VPC Internet Gateway: igw-0b2c0684823fc1390
Deleted EFS Filesystem: fs-d9d57e91
Emptying S3 Bucket karim-test-settings-1a2mjwyohb092...
Deleting S3 Bucket karim-test-settings-1a2mjwyohb092...
Emptying S3 Bucket karim-test-logs-s3rlg8rqvcpf...
Deleting S3 Bucket karim-test-logs-s3rlg8rqvcpf...
Successfully uninstalled.
```
