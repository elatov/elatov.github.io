---
published: true
layout: post
title: "AWS Lamba Parsing ECS Events"
author: Karim Elatov
categories: [aws, cloud]
tags: [lambda, python]
---

I decided to play around with AWS Lambda to see if it help out to monitor the status of  containers.

## Creating a Lambda Function
The easiest thing to do is to create a sample function. Once logged into AWS go to the Lambda Service section and you should see a list of created lambda functions:

![aws-lambda-fuctions.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/aws-lambda-fuctions.png)

The simplest to do is to just click Create Function and choose a language of your preference:

![lambda-functions-lang.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/lambda-functions-lang.png)

I decided to use **Python 3.6**, since that was the language I was most comfortable with. Then for the role, I decided to use an Existing Role of **lambda_basic_execution**:

![lambda-role-execution.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/lambda-role-execution.png)

After that it will take you to the next page, when you can modify what the function does how it's triggered:

![lambda-function-final-page.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/lambda-function-final-page.png)

As quick test, I decided to just see how the events look like. So I created a very simple function that just prints out the event that is sent to the function:


```python
import json

def lambda_handler(event, context):
    if event["source"] != "aws.ecs":
        raise ValueError("Function only supports input from events with "
                         "a source type of: aws.ecs")
    print("event looks like this {}".format(event))
```

That should be enough to get started.

## Create Rule in CloudWatch to Trigger your Lambda Function

Now what we can do is create a rule in **CloudWatch** to call our function with the event. So in AWS go to CloudWatch Service Section and then navigate to  **Events** -> **Rules**, and you should see a list of configured rules:

![cloudwatch-rules.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/cloudwatch-rules.png)

Let's start by clicking on Create Rule and then choose the following settings:

- Event Source -> Event Pattern
- Service Name -> EC2 Container Service
- Event Type -> State Change
- Detail Type -> Any
- Cluster -> Any
- Target -> Your_Function

![cloudwatch-rule-specifics.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/cloudwatch-rule-specifics.png)

Also if you scroll down, you can see how the events will look like when sent to your function:

![sample-events.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/sample-events.png)

Then if you go to the next page, you ran give your rule a new name and save it:

![cw-rule-creation-final-page.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/cw-rule-creation-final-page.png)

Then you should be getting the new events on your function.

## Testing Out your Lambda Function

Before you enable the cloudwatch events you can also test your function manually. If you go back to your function from the Lambda Service section in AWS, on your top right you can mimic events that are sent to your function. Now that we saw how the events will look like (while we were creating the above rule). Let's copy those **json** examples and mimic sending those over. So click on drop down next to the **Test** button and then choose **configure test events**:

![configure-test-event.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/configure-test-event.png)

Then create a new event, give it a name, and paste one of the json examples:

![sample-event-create.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/sample-event-create.png)

Then after it's created you can choose it from the drop down list and click test and you will see how the results look like:

![results-from-function.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/results-from-function.png)

Since I was planning on sending a message to a slack channel, I wasn't returning the actual message, but if there was another function that was parsing the output of this lambda function I would just return that as a string.

## Checking out your Lambda Function Metrics
You can checkout how many times the function has been called by clicking **Monitoring**:

![graph-ci-lambda-function.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/graph-ci-lambda-function.png)

You will notice from the above output that the CI environment (where I was initially testing), does a LOT of task restarts. We can then click Jump to Logs and you will see the output of each call:

![lambda-function-logs.png](https://res.cloudinary.com/elatov/image/upload/v1633113977/blog-pics/aws-lambda/lambda-function-logs.png)

that's it for now.