---
title: VCAP5-DCD Objective 4.1 – Create an Execute a Validation Plan
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-4-1-create-an-execute-a-validation-plan/
dsq_thread_id:
  - 1404902593
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Recall standard functional test areas for design and operational verification

From "[Functional versus Non-functional Requirements](http://communities.vmware.com/docs/DOC-17409)":

> **Functional Requirements**
> The official definition for a functional requirement specifies what the system should do: "A requirement specifies a function that a system or component must be able to perform." Functional requirements specify specific behavior or functions, for example: "Display the heart rate, blood pressure and temperature of a patient connected to the patient monitor."
>
> Typical functional requirements are:
>
> *   Business Rules
> *   Transaction corrections, adjustments, cancellations
> *   Administrative functions
> *   Authentication
> *   Authorization –functions user is delegated to perform
> *   Audit Tracking
> *   External Interfaces
> *   Certification Requirements
> *   Reporting Requirements
> *   Historical Data
> *   Legal or Regulatory Requirements

and from the same document:

> **Non-Functional Requirements**
> The official definition for a non-functional requirement specifies how the system should behave:
> "A non-functional requirement is a statement of how a system must behave, it is a constraint upon the systems behavior."
>
> Non-functional requirements specify all the remaining requirements not covered by the functional
> requirements. They specify criteria that judge the operation of a system, rather than specific behaviors, for example: "Display of the patient's vital signs must respond to a change in the patient's status within 2 seconds."
>
> Typical non-functional requirements are:
>
> *   Performance - Response Time, Throughput, Utilization, Static Volumetric
> *   Scalability
> *   Capacity
> *   Availability
> *   Reliability
> *   Recoverability
> *   Maintainability
> *   Serviceability
> *   Security
> *   Regulatory
> *   Manageability
> *   Environmental
> *   Data Integrity
> *   Usability
> *   Interoperability
>
> Non-functional requirements specify the system’s ‘quality characteristics’ or ‘quality attributes’.
> Potentially many different stakeholders have an interest in getting the non-functional requirements
> right. This is because for many large systems the people buying the system are completely different from those who are going to use it (customers and users).

Depending on a functional test area, let's say the functional requirement is for User to be able to create VMs. So you create a role that can create VMs. Then to test it out you operationally verify that you have fulfilled the functional requirement. You do this by asking a user who is given that role to create a VM. If it works then you are all set.

### Differentiate between operational testing and design verification

I see this as fulfilling either a functional requirement VS fulfilling a non-functional requirement. From "Operational Test Requirements":

> **Operational Test Requirement Cases**
> **Standalone ESX server only**
> Network/Switch Failure
>
> 1.  Conditions - set the test conditions before you start
>     *   Standalone ESX server running ESX 3.5
>     *   6 Pnics in the following configuration
>         1.  vSwitch 1
>             *   Service Console Port Group, Default VLAN, Primary Nic0 and Standby Nic3
>             *   Vmotion Port Group Separate VLAN Primary Nic3 and Standby Nic0
>         2.  vSwitch 2
>             *   IP Storage Port Group, Separate VLAN, Port Group Primary Nic2 and Standby Nic5
>         3.  3. vSwitch3
>             *   VM Network Port Group, Separate VLAN, Port Group, Team Nics 1,4
>         4.  4. All Nics are redundantly connected to seprate physical switches
>     *   No vSwtich is externally connected to one physical nic
> 2.  Triggers - what are the trigger events (these are the events that would happen in "normal" production, and the ones you will pretend / mimic in test - like a network fail)
>     *   Nic Port failure on Service Console Nic0
>     *   Nic Port failure on Vmotion Nic3
>     *   Nic Port failure on IP Storage Port Group Nic2
>     *   Nic Port failure on IP Storage Port Group Nic5
>     *   Nic Port failure on VM Network Port Group Nic1
>     *   Nic Port failure on VM Network Port Group Nic4
>     *   Switch Port Failure on Service Console Nic0
>     *   Switch Port Failure on Vmotion Nic3
>     *   Switch Port Failure on IP Storage Port Group Nic2
>     *   Switch Port Failure on IP Storage Port Group Nic5
>     *   Switch Port Failure on VM Network Port Group Nic1
>     *   Switch Port Failure on VM Network Port Group Nic4
>     *   Swtich 0 Failure
>     *   Switch1 Failure
> 3.  Alerts - what events should you see, and where, and by whom?
>     *   Not sure yet
> 4.  Actions - what actions are required by Support staff?
>     *   Determine failure cause and resolve issue. (VMware Support Team and Network Infrastructure team.)
> 5.  Recovery - what is the recovery procedure
>     *   Replace failed part or fix configuration
>     *   Document root cause and recovery procedure.

Now for a design verification you could have something comply to PCI compliance and setup a DMZ. For this design verification you would put the host in a DMZ and make sure you can ping outside of the DMZ.

### From an existing template, choose the appropriate test areas.

From "[Validation Test Plan](http://www.vmware.com/files/pdf/partners/09Q1_VM_Test_Plan.doc)", here is template that is used for test areas:

> **(Optionally) VMware Infrastructure Testing**
>
> In order to understand how [ISV Product] works with higher level functionality of VMware Infrastructure, we will perform one or more of the following tests.
>
> **VMware vMotion Testing**
>
> While running the workload, VMware vMotion is used to execute manual migration of the database virtual machine from one VMware ESX host to another. During this test, response time and transaction rates are monitored, and any observed slowdown in performance is measured. Five such operations will be executed, and averages are then determined across the five.
>
> **VMware Distributed Resource Scheduler (DRS) Testing**
>
> During this test, virtual machines are assigned to VMware ESX hosts such that the majority of the load will be on one host. In the first test, set the aggressiveness level of VMware DRS to “Conservative.” Start up the test and monitor how VMware DRS moves virtual machines across a cluster to balance the load. Monitor transaction throughput, as well as CPU utilization of the various hosts in the cluster. You should see CPU utilization balance across the hosts with little decrease in throughput. Now run the same test after setting the aggressiveness of VMware DRS to a substantially higher value. Typical deliverables are CPU charts from VMware vCenter Server that reflect the balancing of the load during these tests.
>
> **VMware High Availability (HA) Testing**
>
> Run the workload on a clustered resource pool, and then do a hard shutdown of one host of the configuration. Note how the virtual machines come up on another host in the cluster. Restart the application components if necessary, and functionally verify that the application is working again. Measure the time it takes for the virtual machine to start accepting work again. This work is often most interesting in the case of services that start automatically at reboot, such as Web servers, such that the application will automatically be ready to work as soon as the virtual machine is restarted on another host.

### Identify expected results

This is provided by running some additional testing. Here is an example from "[Validation Test Plan](http://www.vmware.com/files/pdf/partners/09Q1_VM_Test_Plan.doc)":

> **Benchmark Workload**
>
> This section describes the workload used, the load driver technology, and the specific functional transactions included.
>
> The workload is based on. The workload consists of the following transaction scripts (provide relevant workload operations below):
> [<img class="alignnone size-full wp-image-3367" title="app-bench" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/app-bench.png" alt="app bench VCAP5 DCD Objective 4.1 – Create an Execute a Validation Plan " width="667" height="188" />](http://virtuallyhyper.com/wp-content/uploads/2012/09/app-bench.png)

### Demonstrate an ability to track results in an organized fashion

Create test cases for your testing and keep track of each in a table. Here is an example from "[Validation Test Plan](http://www.vmware.com/files/pdf/partners/09Q1_VM_Test_Plan.doc)":

> **Test Cases**
>
> The following use cases will be tested, corresponding to our. Each configuration/workloads is described below:
>
> ** Configuration**
>
> The medium configuration consists of several virtual machines: two Web servers, two application servers, a report server, and the database. The test cases to be run and the data to be collected are as follows:
>
> [<img class="alignnone size-full wp-image-3368" title="test-case-example" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/test-case-example.png" alt="test case example VCAP5 DCD Objective 4.1 – Create an Execute a Validation Plan " width="666" height="160" />](http://virtuallyhyper.com/wp-content/uploads/2012/09/test-case-example.png)

There are also tools to make sure check the health of an environment. Check out Epping's Blog "Health Check tools I use", from that post:

> I personally use the following tools:
>
> *   [Health Check script by A.Mikkelsen](http://sourceforge.net/projects/esxhealthscript/) - for a quick overview of the current situation and setup, small files and easy to carry around, runs from the Service Console.
> *   VMware Health Analyzer Appliance - A linux appliance that can connect to your VC/ESX and analyze log files. At this point in time it’s only available for VMware Employees or Partners with access to Partner Central.
> *   [Report into MS Word](http://communities.vmware.com/docs/DOC-7070) - Alan Renouf created this great reporting powershell scripts. It dumps info into a word document. (And i’ve heard he’s also working on a Visio export)
> *   [Health Check Script](http://www.ivobeerens.nl/2008/08/28/vmware-powershell-healthcheck-script/) - Create an html report with datastore, cpu, memory and snapshot info… and more.
> *   [RVTools](http://www.robware.net/) - Gives a quick overview of current VM setup like snapshots, memory, cpu etc.

### Compare actual and expected results and explain differences

Some times the expected results are obtained from white papers and vendors. Always have an apples to apples comparison. Instead of going off the white paper, get a baseline using physical hosts in the current environment and then run similar tests on the VMs. Make sure the OS versions and underlying hardware is the same. Also make sure the VM is spec'ed with the same vCPUs and vRAM as the physical machine that the baseline was grabbed from.

### Apply validation plan metrics to demonstrate traceability to business objectives

I think this table from "[Validation Test Plan](http://www.vmware.com/files/pdf/partners/09Q1_VM_Test_Plan.doc)":

[<img class="alignnone size-full wp-image-3369" title="app-bench" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/app-bench1.png" alt="app bench1 VCAP5 DCD Objective 4.1 – Create an Execute a Validation Plan " width="667" height="188" />](http://virtuallyhyper.com/wp-content/uploads/2012/09/app-bench1.png)

Shows very good example of tracing the business requirement. You can follow the flow and performance of a business workload. The frequency of execution can be compared to the metrics to make sure they meet the goals set.

