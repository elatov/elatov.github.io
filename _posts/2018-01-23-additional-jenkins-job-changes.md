---
published: true
layout: post
title: "Additional Jenkins Job Changes"
author: Karim Elatov
categories: [os]
tags: [jenkins,pipeline]
---
### Jenkins
So after creating my basic pipeline jenkins job in [my previous post](/2017/12/getting-started-with-jenkins/), I decided to expand the setup a little bit.

### Create a job to Trigger another job
I decided to create a job which will check for new releases of [drive](https://github.com/odeke-em/drive) on github and pass the new version as a build parameter to the main job that builds the software. Here are the tools I used for the new job:

- [Pipeline: Build Step](https://jenkins.io/doc/pipeline/steps/pipeline-build-step/)
- [Groovy Matcher Class](http://docs.groovy-lang.org/latest/html/groovy-jdk/java/util/regex/Matcher.html)
- [Parameterized Scheduler Plugin](https://plugins.jenkins.io/parameterized-scheduler/) (which is part of jenkins core now)

Here is the code I ended up with:

    String latest_drive_version = ''
    String current_drive_version= DRIVE_VERSION
    node('puppet'){
        stage("Check for New Version"){
            String git_output = sh(script: "curl -s https://api.github.com/repos/odeke-em/drive/releases/latest | grep tag_name",returnStdout: true)
            String git_string = git_output.trim()
            def ver = (git_string =~ /v[\d.]+/)
            latest_drive_version = ver[0]
            // set ver to nothing since having a matcher object across stages causes random issues
            ver = "blah"
        }
        if (current_drive_version != latest_drive_version){
            println("time to build drive, old version: ${current_drive_version} new version: ${latest_drive_version}")
            sh "if [ -d /etc/puppetlabs/code/environments/production/modules/drive/files/jenkins/${latest_drive_version} ]; then true; else mkdir /etc/puppetlabs/code/environments/production/modules/drive/files/jenkins/${latest_drive_version}; fi"
            stage ('Starting Build job') {
                build job: '02-drive-pipeline', 
                    parameters: [
                        [$class: 'StringParameterValue', 
                         name: 'DRIVE_VERSION', 
                         value: latest_drive_version]],
                    wait: false
            }
        } else {
                println ("No new version released")
        }
    }

The note about *matcher* causing random issues is covered in [Serializing Local Variables](https://github.com/jenkinsci/pipeline-plugin/blob/master/TUTORIAL.md#serializing-local-variables):

> * This occurs because the matcher local variable is of a type (Matcher) not considered serializable by Java. Since pipelines must survive Jenkins restarts, the state of the running program is periodically saved to disk so it can be resumed later (saves occur after every step or in the middle of steps such as sh).
> 
> * The “state” includes the whole control flow including: local variables, positions in loops, and so on. As such: any variable values used in your program should be numbers, strings, or other serializable types, not “live” objects such as network connections.
>  
> * If you must use a nonserializable value temporarily: discard it before doing anything else. When you keep the matcher only as a local variable inside a function, it is automatically discarded as soon as the function returned.

Then I created a build trigger to run it weekly:

![build-trigger-cron](https://seacloud.cc/d/480b5e8fcd/files/?p=/jenkins-mail/build-trigger-cron.png&raw=1)

Of course I could just **Poll SCM**/Git for a new Commit every time:

![build-triggers](https://seacloud.cc/d/480b5e8fcd/files/?p=/jenkins-mail/build-triggers.png&raw=1)

But that would build it too often. I only wanted new releases to cause builds. After that was in place, I saw the following at the beginning of the triggered job:

    Started by upstream project "01-drive-repo-trigger" build number 4
    originally caused by:
     Started by user Jenkins Admin

### Jenkins mail Job Results
I also ended up installing the [mailer plugin](https://plugins.jenkins.io/mailer/):

![jenkins-mailer-plugin-installed](https://seacloud.cc/d/480b5e8fcd/files/?p=/jenkins-mail/jenkins-mailer-plugin-installed.png&raw=1)

And configured the plugin to use my SMTP server (**Manage Jenkins** -> **Configure System** -> **E-mail Notification**) and sent a test email:

![mailer-email-sent](https://seacloud.cc/d/480b5e8fcd/files/?p=/jenkins-mail/mailer-email-sent.png&raw=1)

And then I checked out these pages on how to use it:

- ["Mail" Step for Jenkins Workflow](https://www.previous.cloudbees.com/blog/mail-step-jenkins-workflow)
- [mail: Mail](https://jenkins.io/doc/pipeline/steps/workflow-basic-steps/#code-mail-code-mail)

Then I added a new stage to my pipeline code of the main job:

        stage('Results') {
            echo "Sending email to ${RECIPIENTS}"
            print "recipients: " + RECIPIENTS
            String jobDetails = "${env.JOB_NAME} (${env.BUILD_NUMBER}) \n Please go to ${env.BUILD_URL} \n"
            String subject = "${env.JOB_NAME} results"
            message = jobDetails
            mail bcc: '', body: "${message}", cc: '', charset: 'UTF-8', from: '', mimeType: 'text/plain', subject: "${subject}", to: "${RECIPIENTS}"
       }

There are also some good examples in [Sending Notifications in Pipeline](https://www.previous.cloudbees.com/blog/sending-notifications-pipeline) which uses the [Email-ext plugin](https://plugins.jenkins.io/email-ext/).
