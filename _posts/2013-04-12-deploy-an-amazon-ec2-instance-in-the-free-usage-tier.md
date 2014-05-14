---
title: Deploy an Amazon EC2 instance in the Free Usage Tier
author: Karim Elatov
layout: post
permalink: /2013/04/deploy-an-amazon-ec2-instance-in-the-free-usage-tier/
dsq_thread_id:
  - 1406616989
categories:
  - AWS
tags:
  - Amazon Cloud Watch
  - aws
  - ec2
---
<p>If you want to try out AWS (Amazon Web Services), there is a 12 month (1 year) free trial (Free Usage Tier). Most of the information regarding the Free Usage Tier is outlined in the &#8220;<a href="http://s3.amazonaws.com/awsdocs/gettingstarted/latest/awsgsg-freetier.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://s3.amazonaws.com/awsdocs/gettingstarted/latest/awsgsg-freetier.pdf']);">Getting Started Guide AWS Free Usage Tier</a>&#8220;. From the Guide here is a table of all the available services:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_AWS.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_AWS.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_AWS.png" alt="FUT AWS Deploy an Amazon EC2 instance in the Free Usage Tier" width="820" height="666" class="alignnone size-full wp-image-7842" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>From the same PDF here are some limitations:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Usage_Limits.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Usage_Limits.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Usage_Limits.png" alt="FUT Usage Limits Deploy an Amazon EC2 instance in the Free Usage Tier" width="776" height="305" class="alignnone size-full wp-image-7844" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>Here is more information from the PDF:</p>
<blockquote>
<p>The free usage tier model provides a number of free usage hours per month for these services. For example, the free usage tier pricing model provides 750 usage hours of an Amazon EC2 micro instance per month. (An instance is considered to be running from the time you launch it until the time you terminate it.) You can run one instance continuously for a month, or ten micro instances for 75 hours a month. How you spend your free usage is up to you.</p>
<p>In order to stay within the free usage tier, you’ll need to stay under 15 GB of outbound data transfer.</p>
</blockquote>
<p>Here is list of the limitation:</p>
<ol>
<li>30GB of Space</li>
<li>2M IOPs </li>
<li>15GB Network Throughput</li>
<li>750 hours of CPU</li>
</ol>
<p>There are a max of 744 (31 days in month * 24 hours in a day) hours of execution, so only one continuous instance can be deployed. In my example I decided to just use the Amazon EC2 (Elastic Cloud Computing) instance and no other services. But if you don&#8217;t want a whole VM to play with then other services are available as well.</p>
<h2>Sign up for AWS Free Usage Tier and Check Eligibility</h2>
<p>You can go to &#8220;<strong>http://aws.amazon.com/</strong>&#8221; click on the &#8220;Sign Up&#8221; button:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/sign_up_aws.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/sign_up_aws.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/sign_up_aws.png" alt="sign up aws Deploy an Amazon EC2 instance in the Free Usage Tier" width="719" height="76" class="alignnone size-full wp-image-7846" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>It will ask you for your Credit Card, but don&#8217;t worry as long as you stay within the limitations you won&#8217;t be charged. After you signed up you can go to <strong>http://aws.amazon.com/account/</strong>:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_account.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_account.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_account.png" alt="aws account Deploy an Amazon EC2 instance in the Free Usage Tier" width="984" height="559" class="alignnone size-full wp-image-7847" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>And then Click on &#8220;Account Activity&#8221; and you will see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Eligible.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Eligible.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/FUT_Eligible.png" alt="FUT Eligible Deploy an Amazon EC2 instance in the Free Usage Tier" width="745" height="158" class="alignnone size-full wp-image-7848" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>At this point we can deploy an EC2 Instance.</p>
<h2>Deploy an Amazon EC2 Instance</h2>
<p>From the Getting Starting Guide:</p>
<blockquote>
<p>The easiest way to get started with the Amazon free usage tier is to launch a virtual server, which is referred to as an Amazon EC2 instance. Amazon Elastic Compute Cloud (Amazon EC2) is a powerful component of AWS and central to many cloud-based applications. In the free usage tier, you can launch a micro Amazon EC2 instance. Micro instances provide a small amount of consistent CPU resources and allow you to burst CPU capacity when additional cycles are available. A micro instance is well suited for lower throughput applications and web sites that consume significant compute cycles only occasionally.</p>
</blockquote>
<p>Most of the Instructions on how to Deploy an EC2 instance can be found in &#8220;<a href="http://awsdocs.s3.amazonaws.com/EC2/latest/ec2-ug.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://awsdocs.s3.amazonaws.com/EC2/latest/ec2-ug.pdf']);">Amazon Elastic Compute Cloud User Guide</a>&#8220;</p>
<p>To get this started we have go to the &#8220;Amazon EC2 console&#8221;. To get to the console, we first have to go to the &#8220;AWS Management Console&#8221;. Go to <strong>http://aws.amazon.com</strong> and then click on the &#8220;My Account/Console&#8221; and you will see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_my_account_console.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_my_account_console.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_my_account_console.png" alt="aws my account console Deploy an Amazon EC2 instance in the Free Usage Tier" width="975" height="201" class="alignnone size-full wp-image-7849" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>From the Drop Down Menu select &#8220;AWS Management Console&#8221;, and that will bring you to the following page:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png" alt="aws mgmt console Deploy an Amazon EC2 instance in the Free Usage Tier" width="946" height="542" class="alignnone size-full wp-image-7850" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>This is the central portal to manage all the Amazon Web Services. From here click on &#8220;EC2 Virtual Servers In the Cloud&#8221; and that will take you here:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/EC2_Dashboard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/EC2_Dashboard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/EC2_Dashboard.png" alt="EC2 Dashboard Deploy an Amazon EC2 instance in the Free Usage Tier" width="947" height="513" class="alignnone size-full wp-image-7851" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>To create a new EC2 instance click on the &#8220;Launch Instance&#8221; button:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_instance.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/create_instance.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_instance.png" alt="create instance Deploy an Amazon EC2 instance in the Free Usage Tier" width="724" height="126" class="alignnone size-full wp-image-7852" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>You will then be presented with a choice of wizards:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/New_Instance_Wizard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/New_Instance_Wizard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/New_Instance_Wizard.png" alt="New Instance Wizard Deploy an Amazon EC2 instance in the Free Usage Tier" width="834" height="409" class="alignnone size-full wp-image-7853" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I just left the &#8220;Classic Wizard&#8221; selected and clicked on &#8220;Continue&#8221;. At this point you can select what AMI (Amazon Machine Image) to deploy. If there is a yellow star next to the AMI that means you can deploy it in the Free Usage Tier. Here is a list that I saw:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/select_AMI.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/select_AMI.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/select_AMI.png" alt="select AMI Deploy an Amazon EC2 instance in the Free Usage Tier" width="859" height="542" class="alignnone size-full wp-image-7854" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I selected Ubuntu 12.04 LTS and clicked &#8220;Continue&#8221; and then I was able to see the Instance Details. I selected the &#8220;Instance Type&#8221; and we can see that a micro Instance consists of 613MB of RAM and a single Core CPU. Notice the yellow start next to the Micro Instance, indicating that this is available for the Free Usage Tier:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_details.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_details.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_details.png" alt="Instance details Deploy an Amazon EC2 instance in the Free Usage Tier" width="859" height="576" class="alignnone size-full wp-image-7855" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I left the defaults and clicked &#8220;Continue&#8221; at which point I saw the &#8220;Advanced Instance Details&#8221;. I left the defaults here as well:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/adv_inst_opt.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/adv_inst_opt.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/adv_inst_opt.png" alt="adv inst opt Deploy an Amazon EC2 instance in the Free Usage Tier" width="856" height="571" class="alignnone size-full wp-image-7856" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>After clicking &#8220;Continue&#8221;, I was presented with the &#8220;Storage Device Configuration&#8221; page:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_dev_conf.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_dev_conf.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/storage_dev_conf.png" alt="storage dev conf Deploy an Amazon EC2 instance in the Free Usage Tier" width="860" height="583" class="alignnone size-full wp-image-7857" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>If you click &#8220;Edit&#8221; you can configure EBS (Elastic Block Store) Volumes, from the user Guide:</p>
<blockquote>
<p>Amazon Elastic Block Store (Amazon EBS) provides block level storage volumes for use with Amazon EC2 instances. Amazon EBS volumes are highly available and reliable storage volumes that can be attached to any running instance in the same Availability Zone. The Amazon EBS volumes attached to an Amazon EBS instance are exposed as storage volumes that persist independently from the life of the instance. With Amazon EBS, you only pay for what you use.</p>
<p>Amazon EBS is recommended when data changes frequently and requires long-term persistence. Amazon EBS is particularly well-suited for use as the primary storage for a file system, database, or for any applications that require fine granular updates and access to raw, unformatted block-level storage. Amazon EBS is particularly helpful for database-style applications that frequently encounter many random reads and writes across the data set.</p>
</blockquote>
<p>Here are the available options from the Wizard:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/EBS_Volumes_New_Instance.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/EBS_Volumes_New_Instance.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/EBS_Volumes_New_Instance.png" alt="EBS Volumes New Instance Deploy an Amazon EC2 instance in the Free Usage Tier" width="859" height="579" class="alignnone size-full wp-image-7858" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I was only going to run one instance so I didn&#8217;t add another volume to my VM. You can also change the type of the volume from &#8220;Standard&#8221; to &#8220;Provisioned IOPS&#8221;. From the User Guide:</p>
<blockquote>
<p>To maximize the performance of your I/O-intensive applications, you can use Provisioned IOPS volumes. Provisioned IOPS volumes are designed to meet the needs of I/O-intensive workloads, particularly database workloads, that are sensitive to storage performance and consistency in random access I/O throughput. You specify an IOPS rate when you create the volume, and Amazon EBS provisions that rate for the lifetime of the volume. Amazon EBS currently supports up to 2000 IOPS per volume. You can stripe multiple volumes together to deliver thousands of IOPS per instance to your application.</p>
<p>A Provisioned IOPS volume must be at least 10 GB in size. The ratio of IOPS provisioned to the volume size requested can be a maximum of 10. For example, a volume with 1000 IOPS must be at least 100 GB.</p>
</blockquote>
<p>I only had 2M IOPS on the Free Usage Tier and I didn&#8217;t want to dedicate/reserve any amount of IOPS to my volume since I wasn&#8217;t going to run any IO Intensive Application on my VM. Here is how the options looked like from the Wizard:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Provisioned_IOPS_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Provisioned_IOPS_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Provisioned_IOPS_g.png" alt="Provisioned IOPS g Deploy an Amazon EC2 instance in the Free Usage Tier" width="859" height="585" class="alignnone size-full wp-image-7859" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>8GB of space for my Ubuntu Test VM was good enough for now, so I just clicked &#8220;Continue&#8221;. At this point I was presented with the &#8220;Tags&#8221; page. I just defined one tag and that was the &#8220;Name&#8221; tag like so:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Tags_New_Instance.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Tags_New_Instance.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Tags_New_Instance.png" alt="Tags New Instance Deploy an Amazon EC2 instance in the Free Usage Tier" width="858" height="580" class="alignnone size-full wp-image-7860" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I then clicked &#8220;Continue&#8221; and was presented with the &#8220;Create Key Pair&#8221; page. When you deploy a Linux VM in EC2, an SSH key pair is created so you can use it to login to the VM. I named my key:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Create_new_Key_Pair.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Create_new_Key_Pair.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Create_new_Key_Pair.png" alt="Create new Key Pair Deploy an Amazon EC2 instance in the Free Usage Tier" width="861" height="580" class="alignnone size-full wp-image-7861" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I then clicked &#8220;Create and Download Key&#8221; and the key was downloaded to my download directory:</p>
	elatov@crbook:~$ ls downloads/*.pem
	downloads/Ubuntu_VM.pem
	
<p>This was just the private key of the SSH Key pair:</p>
	elatov@crbook:~$ head -1 downloads/Ubuntu_VM.pem &amp;&amp; tail -1 downloads/Ubuntu_VM.pem 
	-----BEGIN RSA PRIVATE KEY-----
	-----END RSA PRIVATE KEY-----
	
<p>In between are the contents of the private key <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Deploy an Amazon EC2 instance in the Free Usage Tier" class="wp-smiley" title="Deploy an Amazon EC2 instance in the Free Usage Tier" />  It then took me to the &#8220;Security Groups&#8221; Page. From the User Guide:</p>
<blockquote>
<p>A security group defines firewall rules for your instances.These rules specify which incoming network traffic is delivered to your instance. All other traffic is ignored.</p>
<p>If you&#8217;re new to Amazon EC2 and haven&#8217;t set up any security groups yet, AWS defines a default security group for you. The name and description for the group is quicklaunch-x where x is a number associated with your quicklaunch group. The first security group you create using the Quick Launch Wizard is named quicklaunch-1. You can change the name and description using the Edit details button. The group already has basic firewall rules that enable you to connect to the type of instance you choose. For a Linux instance, you connect through SSH on port 22. The quicklaunch-x security group automatically allows SSH traffic on port 22.</p>
</blockquote>
<p>I selected &#8220;Create New Security Group&#8221; and created a new rule to only allow port 22, since for now that is all that I need:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_new_security_group.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/create_new_security_group.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_new_security_group.png" alt="create new security group Deploy an Amazon EC2 instance in the Free Usage Tier" width="859" height="581" class="alignnone size-full wp-image-7863" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>After I clicked &#8220;Continue&#8221; I was presented with the Summary of all the Settings:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Review_new_instance.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Review_new_instance.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Review_new_instance.png" alt="Review new instance Deploy an Amazon EC2 instance in the Free Usage Tier" width="857" height="582" class="alignnone size-full wp-image-7864" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>After I clicked &#8220;Launch&#8221; I was presented with the following dialog:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_is_launching.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_is_launching.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_is_launching.png" alt="Instance is launching Deploy an Amazon EC2 instance in the Free Usage Tier" width="857" height="426" class="alignnone size-full wp-image-7865" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I then went to the EC2 Dashboard and selected &#8220;Instances&#8221; and I saw the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/ec2_intances.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/ec2_intances.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/ec2_intances.png" alt="ec2 intances Deploy an Amazon EC2 instance in the Free Usage Tier" width="1268" height="522" class="alignnone size-full wp-image-7866" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>Now let&#8217;s connect to our EC2 Instance with SSH.</p>
<h2>Assign an Elastic IP to an EC2 Instance</h2>
<p>From the User Guide:</p>
<blockquote>
<p>When you launch an instance in EC2-Classic or a default VPC, we allocate a public IP address for the instance. Public IP addresses are reachable from the Internet. A public IP address is associated with an instance until it is stopped or terminated. If you require a persistent public IP address that can be assigned to and removed from instances as necessary, use an Elastic IP address.</p>
</blockquote>
<p>I didn&#8217;t really want to get a new IP every time I stop my instance. So I decided to setup an EIP (Elastic IP). From the same guide:</p>
<blockquote>
<p>An Elastic IP address (EIP) is a static IP address designed for dynamic cloud computing. With an EIP, you can mask the failure of an instance by rapidly remapping the address to another instance. Your EIP is associated with your AWS account, not a particular instance, and it remains associated with your account until you choose to explicitly release it.</p>
</blockquote>
<p>Also here more information:</p>
<blockquote>
<p>Q: <strong>Is there a charge for Elastic IP addresses?</strong></p>
<p>You are not charged for a single Elastic IP (EIP) address on a running instance . If you associate additional EIPs with that instance, you will be charged for each additional EIP associated with that instance per hour (prorated). Additional EIPs are only available in Amazon VPC.</p>
<p>To ensure efficient use of Elastic IP addresses, we impose a small hourly charge when these IP addresses are not associated with a running instance, or when they are associated with a stopped instance or an unattached network interface.</p>
</blockquote>
<p>So we can use one EIP and if it&#8217;s not associated with a running instance for more than 1 hour we get charged. Something to keep in mind <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Deploy an Amazon EC2 instance in the Free Usage Tier" class="wp-smiley" title="Deploy an Amazon EC2 instance in the Free Usage Tier" />  To associate an EIP with my EC2 instance, from the EC2 Dashboard I clicked on &#8220;Elastic IPs&#8221; and saw the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/EIPs.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/EIPs.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/EIPs.png" alt="EIPs Deploy an Amazon EC2 instance in the Free Usage Tier" width="1266" height="524" class="alignnone size-full wp-image-7867" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I then clicked on &#8220;Allocate New Address&#8221; and the following dialog popped up:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Allow_new_EIP.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Allow_new_EIP.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Allow_new_EIP.png" alt="Allow new EIP Deploy an Amazon EC2 instance in the Free Usage Tier" width="268" height="160" class="alignnone size-full wp-image-7868" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I left the defaults and then clicked on &#8220;Yes, Allocate&#8221; and then under &#8220;Elastic IPs&#8221; the new IP showed up:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/New_EIP.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/New_EIP.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/New_EIP.png" alt="New EIP Deploy an Amazon EC2 instance in the Free Usage Tier" width="1259" height="518" class="alignnone size-full wp-image-7869" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>Now we have to associate our EIP with our EC2 instance, cause if we don&#8217;t and leave it like that for over an hour we will get charged. So from the above screen click on &#8220;Associate Address&#8221; and following dialog showed up:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Associate_EIP_with_Ec2_instance.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Associate_EIP_with_Ec2_instance.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Associate_EIP_with_Ec2_instance.png" alt="Associate EIP with Ec2 instance Deploy an Amazon EC2 instance in the Free Usage Tier" width="379" height="152" class="alignnone size-full wp-image-7870" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>I selected my Instance from the drop down menu and then clicked &#8220;Yes, Associate&#8221;. Then I saw the following in the &#8220;Elastic IPs&#8221; section:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/EIP_Associated.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/EIP_Associated.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/EIP_Associated.png" alt="EIP Associated Deploy an Amazon EC2 instance in the Free Usage Tier" width="1259" height="517" class="alignnone size-full wp-image-7871" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>We can see that is&#8217; associated to our EC2 instance. At this point you can assign the EIP to a more friendly hostname if you have your own DNS service:</p>
	elatov@crbook:~$ host awsub.dnsd.me
	awsub.dnsd.me has address 54.244.249.93
	elatov@crbook:~$ host 54.244.249.93
	93.249.244.54.in-addr.arpa domain name pointer ec2-54-244-249-93.us-west-2.compute.amazonaws.com.
	
<p>Now let&#8217;s connect to our EC2 Instance.</p>
<h3>Connect and Configure EC2 Linux Instance</h3>
<p>We have the private SSH downloaded and we have setup an EIP for our instance, so now we can connect to our VM:</p>
	elatov@crbook:~$ chmod 600 downloads/Ubuntu_VM.pem 
	elatov@crbook:~$ ssh -i downloads/Ubuntu_VM.pem root@54.244.249.93
	Please login as the user "ubuntu" rather than the user "root".
	
	Connection to 54.244.249.93 closed.
	elatov@crbook:~$ ssh -i downloads/Ubuntu_VM.pem ubuntu@54.244.249.93
	Welcome to Ubuntu 12.04.1 LTS (GNU/Linux 3.2.0-36-virtual i686)
	
<p>Now let&#8217;s add a regular user:</p>
	ubuntu@ip-10-248-36-122:~$ sudo adduser elatov
	Adding user `elatov' ...
	Adding new group `elatov' (1001) ...
	Adding new user `elatov' (1001) with group `elatov' ...
	Creating home directory `/home/elatov' ...
	Copying files from `/etc/skel' ...
	Enter new UNIX password: 
	Retype new UNIX password: 
	passwd: password updated successfully
	Changing the user information for elatov
	Enter the new value, or press ENTER for the default
	    Full Name []: 
	    Room Number []: 
	    Work Phone []: 
	    Home Phone []: 
	    Other []: 
	Is the information correct? [Y/n] y
	ubuntu@ip-10-248-36-122:~$ sudo usermod -a -G admin elatov
	
<p>Now let&#8217;s allow regular SSH login, not just via SSH keys:</p>
	ubuntu@ip-10-248-36-122:~$ sudo sed -i 's/PasswordAuthentication\ no/PasswordAuthentication\ yes/' /etc/ssh/sshd_config
	ubuntu@ip-10-248-36-122:~$ sudo service ssh restart
	ssh stop/waiting
	ssh start/running, process 1293
	
<p>Now let&#8217;s try to login as a regular user with password authentication:</p>
	elatov@crbook:~$ ssh elatov@54.244.249.93
	elatov@54.244.249.93's password: 
	Welcome to Ubuntu 12.04.1 LTS (GNU/Linux 3.2.0-36-virtual i686)
	
<p>That is good, now let&#8217;s update the system:</p>
	elatov@ip-10-248-36-122:~$ sudo apt-get update
	elatov@ip-10-248-36-122:~$ sudo apt-get upgrade
	elatov@ip-10-248-36-122:~$ sudo apt-get dist-upgrade
	
<p>And now you can configure a web server or whatever you desire and use it for a year for free. Just keep an eye on your usage.</p>
<h2>Monitor EC2 Instance Usage</h2>
<p>If you want a general over view of the usage you can go to <strong>http://aws.amazon.com</strong> then hover over &#8220;My Account/Console&#8221; and from the drop down menu select &#8220;Account Activity&#8221;. From here scroll down to the &#8220;AWS Service Charges&#8221; and Expand &#8220;Amazon Elastic Compute Cloud&#8221; and &#8220;AWS Data Transfer&#8221;. You will then see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/AWS_Service_charges.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/AWS_Service_charges.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/AWS_Service_charges.png" alt="AWS Service charges Deploy an Amazon EC2 instance in the Free Usage Tier" width="738" height="422" class="alignnone size-full wp-image-7872" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>Here you can see if you are getting close to IOPS or something and shutdown the VM for the rest of the month. If you want a more granular view of the VM. In the EC2 Dashboard you can click &#8220;Instances&#8221; and then select your Instance and then Select the &#8220;Monitoring&#8221; Tab and you will see the following statistics:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_metrics.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_metrics.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Instance_metrics.png" alt="Instance metrics Deploy an Amazon EC2 instance in the Free Usage Tier" width="1345" height="683" class="alignnone size-full wp-image-7873" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<h2>Create an Alarm to Monitor EC2 Instance</h2>
<p>If you want you can create an Alarm to monitor a specific metric. From the Monitoring Tab, you can select &#8220;Create Alarm&#8221; and then choose a metric to monitor:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_an_alarm_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/create_an_alarm_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/create_an_alarm_g.png" alt="create an alarm g Deploy an Amazon EC2 instance in the Free Usage Tier" width="755" height="328" class="alignnone size-full wp-image-7876" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>For example here is alarm that would be triggered if the sum of the outgoing network traffic is more than 1GB in a span of 6 hours. If that keeps going then you will end up going above the limit real fast.</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Alarm-net-out-1gb-6-hours.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Alarm-net-out-1gb-6-hours.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Alarm-net-out-1gb-6-hours.png" alt="Alarm net out 1gb 6 hours Deploy an Amazon EC2 instance in the Free Usage Tier" width="755" height="324" class="alignnone size-full wp-image-7878" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>You can setup 10 Alarms in the Free Usage Tier, from the User Guide:</p>
<blockquote>
<p>Two Amazon CloudWatch alarms and five metrics. You can add up to 10 alarms and 10 basic metrics (at five-minute intervals) within the free usage tier.</p>
</blockquote>
<p>and you can have 100 email notifications sent out for free:</p>
<blockquote>
<p>SNS email notification. By default, no email address is configured to receive email notifications when events happen; however, you can configure an email address, and you can then receive up to 1000 free email notifications each month.</p>
</blockquote>
<p>After the alarm was set I clicked &#8220;Create Alarm&#8221; and the following pop-up showed up:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/Successful_alarm_creation.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/Successful_alarm_creation.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/Successful_alarm_creation.png" alt="Successful alarm creation Deploy an Amazon EC2 instance in the Free Usage Tier" width="459" height="221" class="alignnone size-full wp-image-7880" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>You will also receive a confirmation email to the address that you specified and you need to confirm that you want to receive those notifications. You can confirm your Alarm by going to the &#8220;AWS Management Console&#8221;:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/aws_mgmt_console.png" alt="aws mgmt console Deploy an Amazon EC2 instance in the Free Usage Tier" width="946" height="542" class="alignnone size-full wp-image-7850" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>and then selecting &#8220;CloudWatch&#8221; and then you will see the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/03/cloud_watch_dashboard.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/03/cloud_watch_dashboard.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/03/cloud_watch_dashboard.png" alt="cloud watch dashboard Deploy an Amazon EC2 instance in the Free Usage Tier" width="729" height="507" class="alignnone size-full wp-image-7883" title="Deploy an Amazon EC2 instance in the Free Usage Tier" /></a></p>
<p>You can also click on the Alarm and see the specifics if you want.</p>
